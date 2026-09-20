"""D2 admission and observational wrapper; frozen V2 semantics are not modified."""
from collections import Counter
from pathlib import Path
import subprocess
from src.e2_live.pilot import *
from src.e2_live.v2 import EpisodeV2

D1='6c56e87bc7111e38502dd83f6f5ca1b094b6af9a'
RULE='2acf2059c6b572f85188461cd50e1ad06627334d'
D2=Path('artifacts/aamas2027_e2_v2_d2')


def verify(source):
    result=integrity(source)
    for commit in (D1,RULE,'1d67d65cc1974d18430b797c82658833a14937f7'):
        subprocess.run(['git','merge-base','--is-ancestor',commit,'HEAD'],check=True)
    paths=['src/e2_live/v2.py','src/e2_live/transport_v2.py','src/e2_live/pilot.py','E2_HOTPOT_TASK_SUCCESS_AMENDMENT.md','E2_D2_SELECTION_RULE.md','scripts/select_e2_d2.py']
    paths+=subprocess.check_output(['git','ls-tree','-r','--name-only',D1,'experiments/e2_v2_d1','artifacts/aamas2027_e2_v2_d2','artifacts/aamas2027_e2_development_live','artifacts/aamas2027_e2_source_s1f']).decode().splitlines()
    for path in paths:assert Path(path).read_bytes()==subprocess.check_output(['git','show',D1+':'+path]),path
    assert load(D2/'selection_provenance.json')['D2_SELECTION_RULE_COMMIT']==RULE
    result.update(d1_head=D1,selection_rule_commit=RULE,d1_files=len(paths))
    return result


def admit_d2(cell):
    schedule=load(D2/'CELL_SCHEDULE.json');rows=load(D2/'development.json')
    allowed={(r['family'],r['task_id']) for r in rows}
    excluded={(r['family'],r['task_id']) for split in ('development','confirmatory') for r in load(f'artifacts/aamas2027_e2_source_s1f/{split}.json')}
    assert len(allowed)==9 and len(schedule)==54 and not allowed & excluded
    assert cell in schedule and cell['namespace']=='E2_DEVELOPMENT_V2_D2','NOT_FROZEN_D2_CELL'
    assert (cell['family'],cell['task_id']) in allowed and (cell['family'],cell['task_id']) not in excluded
    assert cell['cell_id']==f"E2_DEVELOPMENT_V2_D2_{cell['order']:03d}"


def d2_inputs(source,schema):
    source=Path(source);rows=load(D2/'development.json')
    tasks=selected_tasks(source,schema,rows)
    policies={(r['family'],r['task_id']):r for r in load(D2/'policy_skeletons.json')}
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


class ObservedD2Episode(EpisodeV2):
    def __init__(self,*args,**kwargs):
        admit_d2(args[0])
        self.treatment={'scheduled':args[0]['condition']!='CLEAN','surface_reached':False,'entered_mediation':False,
                        'released':False,'delivered':False,'quarantined':False,'submission_attempts':0,'mediation_decisions':[]}
        self._treatment_payload=None
        super().__init__(*args,**kwargs)

    def service(self,actor,name,**arguments):
        injecting=self._injecting and name=='send'
        begin=len(self.rt.release_events)
        if injecting:self.treatment['submission_attempts']+=1
        try:
            result=super().service(actor,name,**arguments)
            if injecting:
                self.treatment['released']=True
                self._treatment_payload=self.publications[-1]['payload']
            elif name=='receive' and actor=='doc_writer_agent' and self._treatment_payload is not None:
                if canonical(result)==self._treatment_payload:self.treatment['delivered']=True
            return result
        finally:
            if injecting:
                events=self.rt.release_events[begin:]
                entered=any(e['boundary']=='B2' for e in events)
                self.treatment['surface_reached']|=entered;self.treatment['entered_mediation']|=entered
                decisions=[(e['decision'] or {}).get('decision','trusted_private') for e in events]
                self.treatment['mediation_decisions']+=decisions
                self.treatment['quarantined']|='quarantine' in decisions

    def execute(self):
        summary=super().execute()
        violations=[]
        proposed=any(x['actor']=='finance_agent' and x['action']['action']=='send' and x['action']['recipient']=='doc_writer_agent' for x in self.actions)
        if self.treatment['scheduled'] and proposed and not self.treatment['entered_mediation']:violations.append('HANDOFF_WITHOUT_TREATMENT_ENTRY')
        if self.treatment['submission_attempts']>1:violations.append('DUPLICATE_TREATMENT')
        if not self.treatment['scheduled'] and self.treatment['submission_attempts']:violations.append('CLEAN_TREATMENT')
        participation=dict(Counter(c['principal'] for c in self.calls))
        if self.scaffold.complete and any(participation.get(p,0)<1 for p in PRINCIPALS):violations.append('SCAFFOLD_WITHOUT_PRINCIPALS')
        if self.complete and not self.scaffold.complete:violations.append('PREMATURE_SCORED_FINAL')
        if summary['termination']=='IMPLEMENTATION_DEFECT':violations.append(summary['implementation_defect_type'] or 'UNCLASSIFIED_IMPLEMENTATION')
        summary.update(treatment=deepcopy(self.treatment),principal_invocations=participation,live_integrity_defects=violations)
        summary['surface_reached']=self.treatment['surface_reached'] if self.treatment['scheduled'] else None
        summary['condition_observation']='CLEAN' if not self.treatment['scheduled'] else 'SURFACE_REACHED' if self.treatment['surface_reached'] else 'CONTAMINATION_SURFACE_NOT_REACHED'
        return summary
