#!/usr/bin/env python3
"""Offline D3 runner admission and all-cell instantiation tests."""
import argparse,json,sys,tempfile,subprocess
from pathlib import Path
from src.e2_live.d3 import *
from src.e2_live.v3 import build_stage_request
from scripts.check_e2_live_runner import FakeProvider,FakeEvaluator
from scripts.check_e2_v3_runtime import PLANNER,finance_output,FINALS

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--source-root',type=Path,required=True);p.add_argument('--schema',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    def deny(event,details):
        if event.startswith('socket.'):raise RuntimeError('NO_NETWORK')
    sys.addaudithook(deny)
    checks=verify(a.source_root);schema=load(a.schema);tasks,policies,golds=d3_inputs(a.source_root,schema);schedule=load(D3/'CELL_SCHEDULE.json')
    denied=0
    invalid=[]
    for split in ('development','confirmatory'):
        invalid.extend({**schedule[0],'family':r['family'],'task_id':r['task_id']} for r in load(f'artifacts/aamas2027_e2_source_s1f/{split}.json'))
    invalid.extend({**schedule[0],'family':r['family'],'task_id':r['task_id']} for r in load('artifacts/aamas2027_e2_v2_d2/development.json'))
    invalid.append({**schedule[0],'namespace':'E2_CONFIRMATORY'})
    invalid.extend([{**schedule[0],'task_id':'arbitrary'}, {**schedule[0],'cell_id':'wrong'}, {**schedule[0],'order':54},{**schedule[0],'condition':'unfrozen'}])
    for cell in invalid:
        try:admit_d3(cell)
        except AssertionError:denied+=1
        else:raise AssertionError('ADMISSION_BYPASS')
    class RecordedFixtureEvaluator:
        def score(self,cell,native,private,timeout):
            keys={'bird_pg':['sql_idx','res'],'tatqa':['em','f1','scale','operation'],'hotpot':['em','f1','prec','recall','sp_em','sp_f1','sp_prec','sp_recall','joint_em','joint_f1','joint_prec','joint_recall']}[cell['family']]
            metrics={k:0 for k in keys};private.mkdir(parents=True,exist_ok=True)
            (private/'evaluator_output.json').write_text(json.dumps(metrics))
            return metrics
    pairs={};results=[];machine=[]
    with tempfile.TemporaryDirectory() as td:
        for cell in schedule:
            key=cell['family'],cell['task_id'];actions=[PLANNER,finance_output(cell['family']),FINALS[cell['family']]]
            ep=ObservedD3Episode(cell,tasks[key],policies[key],schema,FakeProvider(actions),RecordedFixtureEvaluator(),Path(td)/cell['cell_id'])
            snap=ep.snapshot('planner_agent');req=canonical(build_stage_request('planner',cell['family'],snap));pair=key,cell['condition']
            if pair in pairs:assert pairs[pair]==req
            pairs[pair]=req
            result=ep.execute();assert not result['live_integrity_defects'],result
            assert result['termination'] in ('SUCCESSFUL_FINAL','POLICY_REJECTION','CONTEXT_LIMIT'),result['termination']
            if result['termination']=='POLICY_REJECTION':assert result['treatment']['entered_mediation']
            machine.append(result)
            results.append({'cell_id':cell['cell_id'],'termination':result['termination'],'treatment':result['treatment']})
        run=Path(td)/'run';run.mkdir()
        (run/'attempts.jsonl').write_text(''.join(json.dumps(c)+'\n' for c in schedule))
        (run/'episodes.jsonl').write_text(''.join(json.dumps(c)+'\n' for c in machine))
        (run/'completion.json').write_text('{}')
        subprocess.run([sys.executable,'scripts/summarize_e2_d3_live.py','--run',str(run),'--private',td,'--output',str(Path(td)/'derived')],check=True,stdout=subprocess.DEVNULL)
        mock_audit=load(Path(td)/'derived/summary.json');assert mock_audit['readiness']=='READY_FOR_CONFIRMATORY_REVIEW'
    out={'mock_saved_evidence_audit':'PASS','status' :'PASS','all54_instantiated':len(results),'equal_initial_pairs':len(pairs),'invalid_admissions_rejected':denied,'frozen_integrity':checks,'mock_terminations':dict(Counter(r['termination'] for r in results)),'cases':results,'live_calls':0}
    a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k!='cases'}))
if __name__=='__main__':main()
