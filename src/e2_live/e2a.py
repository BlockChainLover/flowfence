"""Formal-tranche admission and metadata adapter over unchanged V3 and D3 observer."""
from collections import Counter
from pathlib import Path
from src.e2_live.d3 import ObservedD3Episode, verify
from src.e2_live.v3 import EpisodeV3
from src.e2_live.pilot import load
from src.e2_s1.adapters import task_input

NAMESPACE = 'E2A_FORMAL_CONFIRMATORY'
LABEL = 'FORMAL CONFIRMATORY EVIDENCE — PARTIAL E2 TRANCHE'
BASE = '585143c718492be0ead9c0beda3095fd3c82cfcb'
BRANCH = 'codex/aamas2027-e2a-formal'
ROOT = Path('artifacts/aamas2027_e2a_formal')
SCHEDULE = Path('E2A_FORMAL_CELL_SCHEDULE.json')
S1F = Path('artifacts/aamas2027_e2_source_s1f')


def selected_rows():
    rows = [r for r in load(S1F/'confirmatory.json') if r['family'] in ('tatqa', 'hotpot')]
    assert len(rows) == len({(r['family'], r['task_id']) for r in rows}) == 40
    assert Counter(r['family'] for r in rows) == {'tatqa': 20, 'hotpot': 20}
    assert Counter(r['fact_type'] for r in rows) == {'P1': 15, 'P2': 15, 'P3': 10}
    return sorted(rows, key=lambda r: (r['family'], r['task_id']))


def make_schedule():
    # Round-robin families, then cyclic conditions; adjacent arms alternate first position.
    rows = selected_rows()
    by_family = {f: [r for r in rows if r['family'] == f] for f in ('hotpot', 'tatqa')}
    ordered = [by_family[f][i] for i in range(20) for f in ('hotpot', 'tatqa')]
    cells = []
    for rep in range(1, 4):
        for phase in range(3):
            for index, row in enumerate(ordered):
                condition = ('CLEAN', 'CONTAMINATION_A', 'CONTAMINATION_B')[(phase + index + rep - 1) % 3]
                arms = ['EXACT_IFC', 'FLOWFENCE_R2']
                if (phase + index + rep - 1) % 2: arms.reverse()
                for arm in arms:
                    order = len(cells) + 1
                    cells.append(dict(namespace=NAMESPACE, cell_id=f'{NAMESPACE}_{order:03d}', order=order,
                                      family=row['family'], task_id=row['task_id'], condition=condition,
                                      defense=arm, repetition=rep))
    return cells


def admit(cell):
    schedule = load(SCHEDULE)
    assert schedule == make_schedule(), 'FORMAL_SCHEDULE_CHANGED'
    assert cell in schedule, 'NOT_FROZEN_E2A_CELL'


def inputs(source):
    import pyarrow.parquet as pq
    source = Path(source)
    selected = {(r['family'], r['task_id']) for r in selected_rows()}
    tasks, golds = {}, {}
    for context in load(source/'tatqa/dataset_raw/tatqa_dataset_dev.json'):
        for row in context['questions']:
            key = ('tatqa', row['uid'])
            if key in selected:
                tasks[key] = task_input('tatqa', row, context=context)
                golds[key] = row
    hot_ids = sorted(tid for f, tid in selected if f == 'hotpot')
    for row in pq.read_table(source/'data/hotpot_distractor_validation.parquet', filters=[('id', 'in', hot_ids)]).to_pylist():
        key = ('hotpot', row['id'])
        tasks[key] = task_input('hotpot', row)
        golds[key] = row
    policies = {(r['family'], r['task_id']): r for r in load(S1F/'policy_skeletons.json')
                if r['split'] == 'confirmatory' and (r['family'], r['task_id']) in selected}
    assert set(tasks) == set(golds) == set(policies) == selected
    return tasks, policies, golds


class FormalEpisode(ObservedD3Episode):
    def __init__(self, *args, **kwargs):
        admit(args[0])
        self.submission_attempts = 0
        self.treatment_decisions = []
        self.edge_defects = []
        EpisodeV3.__init__(self, *args, **kwargs)

    def execute(self):
        result = super().execute()
        # Only historical hardcoded reporting fields change; the saved trajectory keeps the formal cell.
        assert result['namespace'] == 'E2_DEVELOPMENT_V3_D3'
        result.update(namespace=NAMESPACE, label=LABEL)
        assert all(result[k] == v for k, v in self.cell.items())
        return result
