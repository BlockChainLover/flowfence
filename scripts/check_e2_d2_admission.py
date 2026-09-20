#!/usr/bin/env python3
"""Offline D2 runner admission and all-cell instantiation tests."""
import argparse,json,sys,tempfile
from pathlib import Path
from src.e2_live.d2 import *
from src.e2_live.v2 import build_request
from scripts.check_e2_live_runner import FakeProvider,FakeEvaluator
from scripts.check_e2_v2_runtime import DELEGATE,HANDOFF,FINALS

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--source-root',type=Path,required=True);p.add_argument('--schema',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    def deny(event,details):
        if event.startswith('socket.'):raise RuntimeError('NO_NETWORK')
    sys.addaudithook(deny)
    checks=verify(a.source_root);schema=load(a.schema);tasks,policies,golds=d2_inputs(a.source_root,schema);schedule=load(D2/'CELL_SCHEDULE.json')
    denied=0
    invalid=[]
    for split in ('development','confirmatory'):
        invalid.extend({**schedule[0],'family':r['family'],'task_id':r['task_id']} for r in load(f'artifacts/aamas2027_e2_source_s1f/{split}.json'))
    invalid.extend([{**schedule[0],'task_id':'arbitrary'}, {**schedule[0],'cell_id':'wrong'}, {**schedule[0],'order':54},{**schedule[0],'condition':'unfrozen'}])
    for cell in invalid:
        try:admit_d2(cell)
        except AssertionError:denied+=1
        else:raise AssertionError('ADMISSION_BYPASS')
    pairs={};results=[]
    with tempfile.TemporaryDirectory() as td:
        for cell in schedule:
            key=cell['family'],cell['task_id'];actions=[DELEGATE,HANDOFF,{'action':'finalize','output':FINALS[cell['family']]}]
            ep=ObservedD2Episode(cell,tasks[key],policies[key],schema,FakeProvider(actions),FakeEvaluator(),Path(td)/cell['cell_id'])
            snap=ep.snapshot('planner_agent');req=canonical(build_request('planner_agent',cell['family'],snap));pair=key,cell['condition']
            if pair in pairs:assert pairs[pair]==req
            pairs[pair]=req
            result=ep.execute();assert not result['live_integrity_defects'],result
            assert result['termination'] in ('SUCCESSFUL_FINAL','POLICY_REJECTION','CONTEXT_LIMIT'),result['termination']
            if result['termination']=='POLICY_REJECTION':assert result['treatment']['entered_mediation']
            results.append({'cell_id':cell['cell_id'],'termination':result['termination'],'treatment':result['treatment']})
    out={'status':'PASS','all54_instantiated':len(results),'equal_initial_pairs':len(pairs),'invalid_admissions_rejected':denied,'frozen_integrity':checks,'mock_terminations':dict(Counter(r['termination'] for r in results)),'cases':results,'live_calls':0}
    a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k!='cases'}))
if __name__=='__main__':main()
