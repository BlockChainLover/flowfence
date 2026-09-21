"""D3 admission and observational wrapper; frozen V3 semantics are not modified."""
from collections import Counter
from pathlib import Path
import subprocess
from src.e2_live.pilot import *
from src.e2_live.v3 import EpisodeV3

D1='dc40ab91d3cc06bcce56841b52044f6847d3826e'
RULE='9e142e7a2ff282e986798da096ec525c0b03bb37'
D3=Path('artifacts/aamas2027_e2_v3_d3')


def verify(source):
    result=integrity(source)
    for commit in (D1,RULE,'1d67d65cc1974d18430b797c82658833a14937f7'):
        subprocess.run(['git','merge-base','--is-ancestor',commit,'HEAD'],check=True)
    paths=['src/e2_live/v3.py','src/e2_live/transport_v2.py','src/e2_live/pilot.py','E2_HOTPOT_TASK_SUCCESS_AMENDMENT.md','E2_D3_SELECTION_RULE.md','scripts/select_e2_d3.py']
    paths+=subprocess.check_output(['git','ls-tree','-r','--name-only',D1,'experiments/e2_v3_d1','artifacts/aamas2027_e2_v3_d3','artifacts/aamas2027_e2_development_live','artifacts/aamas2027_e2_source_s1f','artifacts/aamas2027_e2_v2_d2','artifacts/aamas2027_e2_v2_d2_live','src/e2_live/v2.py','E2_V3_CONSTRUCT_VALIDITY_AMENDMENT.md']).decode().splitlines()
    for path in paths:assert Path(path).read_bytes()==subprocess.check_output(['git','show',D1+':'+path]),path
    assert load(D3/'selection_provenance.json')['D3_SELECTION_RULE_COMMIT']==RULE
    result.update(d1_head=D1,selection_rule_commit=RULE,d1_files=len(paths))
    return result


def admit_d3(cell):
    schedule=load(D3/'CELL_SCHEDULE.json');rows=load(D3/'development.json')
    allowed={(r['family'],r['task_id']) for r in rows}
    excluded={(r['family'],r['task_id']) for split in ('development','confirmatory') for r in load(f'artifacts/aamas2027_e2_source_s1f/{split}.json')}
    excluded.update((r['family'],r['task_id']) for r in load('artifacts/aamas2027_e2_v2_d2/development.json'))
    assert len(excluded)==78
    assert len(allowed)==9 and len(schedule)==54 and not allowed & excluded
    assert cell in schedule and cell['namespace']=='E2_DEVELOPMENT_V3_D3','NOT_FROZEN_D3_CELL'
    assert (cell['family'],cell['task_id']) in allowed and (cell['family'],cell['task_id']) not in excluded
    assert cell['cell_id']==f"E2_DEVELOPMENT_V3_D3_{cell['order']:03d}"


def d3_inputs(source,schema):
    source=Path(source);rows=load(D3/'development.json')
    tasks=selected_tasks(source,schema,rows)
    policies={(r['family'],r['task_id']):r for r in load(D3/'policy_skeletons.json')}
    golds={}
    for row in load(source/'data/birdsql__bird_mini_dev__data__mini_dev_pg-00000-of-00001.json'):
        key=('bird_pg',str(row['question_id']))
        if key in tasks:golds[key]=row
    for ctx in load(source/'tatqa/dataset_raw/tatqa_dataset_dev.json'):
        for row in ctx['questions']:
            if ('tatqa',row['uid']) in tasks:golds['tatqa',row['uid']]=row
    import pyarrow.parquet as pq
    for row in pq.read_table(source/'data/hotpot_distractor_validation.parquet',filters=[('id','in',[tid for f,tid in tasks if f=='hotpot'])]).to_pylist():golds['hotpot',row['id']]=row
    assert set(tasks)==set(policies)==set(golds) and len(tasks)==9
    return tasks,policies,golds


class ObservedD3Episode(EpisodeV3):
    """Observe frozen V3; classify integrity violations without altering execution."""
    def __init__(self,*args,**kwargs):
        admit_d3(args[0])
        self.submission_attempts=0;self.treatment_decisions=[];self.edge_defects=[]
        super().__init__(*args,**kwargs)

    def service(self,actor,name,**arguments):
        injecting=self._injecting and name=='send'
        begin=len(self.rt.release_events)
        if injecting:
            self.submission_attempts+=1
            if actor!='finance_agent' or arguments.get('recipient')!='doc_writer_agent' or not self.finance_valid:
                self.edge_defects.append('INVALID_TREATMENT_EDGE_OR_EARLY_ENTRY')
        try:return super().service(actor,name,**arguments)
        finally:
            if injecting:self.treatment_decisions.extend((e['decision'] or {}).get('decision','trusted_private') for e in self.rt.release_events[begin:])

    def execute(self):
        summary=super().execute();violations=list(self.edge_defects)
        t=self.treatment;participation=dict(Counter(c['principal'] for c in self.calls))
        if t['scheduled'] and self.finance_valid and t['entries']!=1:violations.append('VALID_HANDOFF_WITHOUT_EXACT_ONE_TREATMENT')
        if self.submission_attempts>1 or t['entries']>1:violations.append('DUPLICATE_TREATMENT')
        if not t['scheduled'] and (self.submission_attempts or t['entries']):violations.append('CLEAN_TREATMENT')
        if t['entries'] and not self.finance_valid:violations.append('TREATMENT_BEFORE_VALID_HANDOFF')
        actors=[c['principal'] for c in self.calls]
        expected=['planner_agent']+['finance_agent']*participation.get('finance_agent',0)+['doc_writer_agent']*participation.get('doc_writer_agent',0)
        if actors and (actors!=expected or participation.get('doc_writer_agent',0)>1):violations.append('STAGE_ORDER')
        semantic='semantic_handoff_published' in self.stage_events
        if participation.get('doc_writer_agent',0) and not semantic:violations.append('WRITER_WITHOUT_SEMANTIC_HANDOFF')
        if self.complete and (not self.writer_valid or not semantic):violations.append('PREMATURE_FINAL')
        if t['quarantined'] and (semantic or participation.get('doc_writer_agent',0) or t['released'] or t['delivered'] or summary['termination']!='POLICY_REJECTION'):
            violations.append('QUARANTINE_CONTINUATION')
        if summary['termination']=='IMPLEMENTATION_DEFECT':violations.append(summary['implementation_defect_type'] or 'UNCLASSIFIED_IMPLEMENTATION')
        summary.update(principal_invocations=participation,live_integrity_defects=violations,
            planner_stage_success='planner_valid_output' in self.stage_events,
            finance_stage_entered=participation.get('finance_agent',0)>0,
            semantic_handoff_published=semantic,
            treatment={**deepcopy(t),'entered_mediation':bool(t['entries']),'surface_reached':bool(t['entries']),
                       'submission_attempts':self.submission_attempts,'mediation_decisions':self.treatment_decisions},
            condition_observation='CLEAN' if not t['scheduled'] else 'TREATMENT_ENTERED_MEDIATION' if t['entries'] else 'TREATMENT_NOT_REACHED_PRE_HANDOFF_FAILURE')
        if violations:summary.update(termination='IMPLEMENTATION_DEFECT',valid=False,original_termination=summary['termination'])
        return summary
