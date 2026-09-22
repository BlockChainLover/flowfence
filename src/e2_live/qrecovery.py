"""Additive task-state recovery. No quarantined payload enters the policy API."""
from copy import deepcopy
from dataclasses import dataclass
from pathlib import Path
import json
from src.e2_live.v3 import EpisodeV3
from src.e2_live.pilot import End, canonical, write_private, sha, load

BASE = '342599f8e6884bafb333fa0bf99b0543352d88ed'
PREREG = '677f32a'
ROOT = Path('artifacts/aamas2027_qrecovery')


def schedule():
    old = load('E2A_FORMAL_CELL_SCHEDULE.json')
    clean = [c for c in old if c['defense'] == 'FLOWFENCE_R2' and c['condition'] == 'CLEAN' and c['repetition'] == 1]
    contaminated = [c for c in old if c['defense'] == 'FLOWFENCE_R2' and c['condition'] != 'CLEAN']
    out = []
    for group, cells in [('CLEAN', clean), ('CONTAMINATED', contaminated)]:
        for i, cell in enumerate(cells, 1):
            out.append({**cell, 'namespace': 'QRECOVERY_FORMAL', 'cell_id': f'QRECOVERY_{group}_{i:03d}',
                        'order': len(out)+1, 'defense': 'FLOWFENCE_RECOVERY', 'historical_cell_id': cell['cell_id']})
    assert len(clean) == 40 and len(contaminated) == 240
    assert len({c['cell_id'] for c in out}) == 280
    return out


@dataclass(frozen=True)
class QuarantineEvent:
    artifact_id: str
    reason_code: str = 'FROZEN_RECOGNIZER_QUARANTINE'


@dataclass
class RecoveredWriterInput:
    values: list
    provenance: dict


class TrustedStateRecoveryPolicy:
    def recover(self, immutable_task_input, trusted_structured_state, quarantine_event):
        # Inputs are serialized before ANY agent generation. No free-form object argument.
        if not isinstance(immutable_task_input, str) or trusted_structured_state != {}:
            raise ValueError('RECOVERY_PROVENANCE_FAILURE')
        task = json.loads(immutable_task_input)
        if not isinstance(task, dict) or not isinstance(task.get('question'), str) or not task['question']:
            raise ValueError('RECOVERY_EMPTY_STATE')
        if not isinstance(quarantine_event, QuarantineEvent):
            raise ValueError('RECOVERY_SCHEMA_FAILURE')
        fields = [{'field': f'values[0].{key}', 'source_type': 'immutable_task_input',
                   'source_id': 'task:initial', 'source_path': [key]} for key in sorted(task)]
        return RecoveredWriterInput([task], {'fields': fields, 'artifact_sources': []})


class RecoveryEpisode(EpisodeV3):
    def __init__(self, cell, task, *args, **kwargs):
        assert cell['defense'] == 'FLOWFENCE_RECOVERY'
        self.immutable_task = canonical(task)
        self.recovered = None
        self.quarantine = None
        self.recovery = {'attempted': False, 'provenance_valid': None, 'input_delivered': False,
                         'writer_invoked': False, 'artifact_reentry': None, 'writer_exposure': None}
        # Select existing R2 without mutating global ARMS or frozen source.
        super().__init__({**cell, 'defense': 'FLOWFENCE_R2'}, task, *args, **kwargs)
        self.cell = deepcopy(cell)

    def publish_finance(self, payload):
        begin = len(self.rt.release_events)
        try:
            return super().publish_finance(payload)
        except End as exc:
            events = self.rt.release_events[begin:]
            quarantined = [e for e in events if e['boundary'] == 'B2' and e['producer'] == 'finance_agent'
                           and e['recipient'] == 'doc_writer_agent' and (e['decision'] or {}).get('decision') == 'quarantine']
            if exc.code != 'POLICY_REJECTION' or len(quarantined) != 1:
                raise
            event = quarantined[0]
            assert not event['accepted'] and not self.pending['doc_writer_agent']
            self.quarantine = QuarantineEvent(event['artifact'])
            self.recovery['attempted'] = True
            # Neither payload nor event['attempted']/decision text is passed to recover.
            self.recovered = TrustedStateRecoveryPolicy().recover(self.immutable_task, {}, self.quarantine)
            self.recovered.provenance.update(episode_id=self.cell['cell_id'],
                quarantined_artifact_id=self.quarantine.artifact_id,
                recovery_input_id=self.cell['cell_id']+':recovered-input')
            self.recovery['provenance_valid'] = self.validate_provenance()
            if not self.recovery['provenance_valid']:
                raise RuntimeError('RECOVERY_PROVENANCE_FAILURE')
            write_private(self.private/'recovery_sources.json', {'task_initial': json.loads(self.immutable_task),
                'structured_state': {}, 'reconstructed_values': self.recovered.values,
                'provenance': self.recovered.provenance})
            self.stage_events.append('trusted_state_reconstructed')

    def validate_provenance(self):
        if self.recovered is None:
            return False
        expected = TrustedStateRecoveryPolicy().recover(self.immutable_task, {}, self.quarantine)
        p = self.recovered.provenance
        return (p['artifact_sources'] == [] and p['fields'] == expected.provenance['fields']
                and self.recovered.values == expected.values)

    def snapshot(self, actor):
        if actor != 'doc_writer_agent' or self.recovered is None:
            return super().snapshot(actor)
        if not self.validate_provenance():
            raise RuntimeError('RECOVERY_PROVENANCE_FAILURE')
        # B1 task-only mediation; never consume a mailbox, history, finance or planner artifact.
        snapshot = self.service(actor, 'context', keys=['task'])
        if snapshot['values'] != self.recovered.values:
            raise RuntimeError('RECOVERY_TASK_SOURCE_MISMATCH')
        refs = snapshot['invocation']['context']
        if len(refs) != 1 or refs[0]['category'] != 'TASK_STATE' or refs[0]['source_principal'] != 'runtime':
            raise RuntimeError('RECOVERY_PROVENANCE_FAILURE')
        self.recovered.provenance['runtime_task_artifact_id'] = refs[0]['artifact_ref']
        snapshot['values'] = deepcopy(self.recovered.values)
        snapshot['invocation']['model_profile_ref'] = 'E2_P1_MINIMAX_M27'
        snapshot['invocation']['tool_permissions'] = []
        snapshot.update(history=[], trusted_stage='writer', finance_sql_actions_used=self.budget.counts['tool'])
        write_private(self.private/'recovered_writer_input.json', {'snapshot': snapshot, 'provenance': self.recovered.provenance})
        return snapshot

    def provider_action(self, actor, snapshot):
        before = len(self.calls)
        try:
            return super().provider_action(actor, snapshot)
        finally:
            if actor == 'doc_writer_agent' and self.recovered is not None and len(self.calls) > before:
                actual = json.loads(self.calls[-1]['request']['json']['messages'][1]['content'])
                if actual != snapshot or actual['values'] != self.recovered.values or actual['history']:
                    raise RuntimeError('RECOVERY_PROVENANCE_FAILURE')
                self.recovery.update(input_delivered=True, writer_invoked=True, artifact_reentry=False, writer_exposure=False)

    def execute(self):
        result = super().execute()
        defects = []
        if self.quarantine:
            qid = self.quarantine.artifact_id
            released = any(e['artifact'] == qid and e['accepted'] for e in self.rt.release_events)
            records = {r['artifact']['artifact_id']: r['artifact'] for r in self.rt.records() if r['record_type'] == 'ArtifactRecord'}
            def ancestors(ref, visited=None):
                visited = set() if visited is None else visited
                if ref in visited: return visited
                visited.add(ref)
                for parent in records.get(ref, {}).get('parent_artifacts', []): ancestors(parent, visited)
                return visited
            writer_calls = [c for c in self.calls if c['principal'] == 'doc_writer_agent']
            exposure = False
            for c in writer_calls:
                snap = json.loads(c['request']['json']['messages'][1]['content'])
                exposure |= any(qid in ancestors(x['artifact_ref']) for x in snap['invocation']['context'])
                if snap['values'] != self.recovered.values or snap['history']: defects.append('WRITER_SOURCE_MISMATCH')
            self.recovery.update(quarantined_artifact_released=released, writer_exposure=exposure,
                                 artifact_reentry=not self.validate_provenance())
            if released or exposure or self.recovery['artifact_reentry']: defects.append('RECOVERY_PROVENANCE_FAILURE')
            if self.treatment['scheduled'] and (self.treatment['entries'] != 1 or self.treatment['released'] or self.treatment['delivered']):
                defects.append('TREATMENT_INTEGRITY')
        else:
            self.recovery['quarantined_artifact_released'] = None
        if result['termination'] == 'IMPLEMENTATION_DEFECT':
            defects.append(result.get('implementation_defect_type') or 'UNCLASSIFIED')
        result.update(namespace='QRECOVERY_FORMAL', label='QRECOVERY FORMAL SUPPLEMENT',
                      recovery=deepcopy(self.recovery), provenance=deepcopy(self.recovered.provenance) if self.recovered else None,
                      live_integrity_defects=defects)
        if defects: result.update(termination='IMPLEMENTATION_DEFECT', valid=False)
        # Preserve native failure category and add a recovery-stage classifier.
        result['recovery_failure'] = ('RECOVERY_WRITER_FAILURE' if self.recovered and not self.complete else None)
        raw = load(self.private/'trajectory.json')
        raw.update(recovery=result['recovery'], recovery_provenance=result['provenance'], live_integrity_defects=defects)
        write_private(self.private/'trajectory.json', raw)
        result['trajectory_sha256'] = sha((self.private/'trajectory.json').read_bytes())
        return result
