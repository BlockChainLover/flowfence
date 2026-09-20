#!/usr/bin/env python3
"""Execute the frozen 54 D2 development cells once. Never resume or run V1/confirmatory."""
import argparse
import json
import os
from pathlib import Path
import subprocess
from src.e2_live.d2 import *
from src.e2_live.transport_v2 import LiveProviderV2
from scripts.run_e2_development_pilot import append


def main():
    p=argparse.ArgumentParser(description=__doc__)
    for name in ('source-root','schema','provider-env','output','private-output'):p.add_argument('--'+name,type=Path,required=True)
    p.add_argument('--first-runner-commit',required=True);a=p.parse_args()
    assert subprocess.check_output(['git','branch','--show-current'],text=True).strip()=='codex/aamas2027-e2-development-v2'
    assert not subprocess.check_output(['git','diff','HEAD','--name-only']),'UNCOMMITTED_TRACKED_CHANGES'
    subprocess.run(['git','merge-base','--is-ancestor',a.first_runner_commit,'HEAD'],check=True)
    for file in ('scripts/run_e2_d2_live.py','src/e2_live/d2.py'):
        assert subprocess.check_output(['git','show',a.first_runner_commit+':'+file])==Path(file).read_bytes()
    checks=verify(a.source_root);schema=load(a.schema);tasks,policies,golds=d2_inputs(a.source_root,schema)
    schedule=load(D2/'CELL_SCHEDULE.json')
    for cell in schedule:admit_d2(cell)
    a.private_output.parent.mkdir(parents=True,exist_ok=True,mode=0o700)
    os.chmod(a.private_output.parent,0o700)
    for path in (a.output,a.private_output):
        assert not path.exists(),'NO_RERUN_OR_RESUME'
        path.mkdir(parents=True,mode=0o700)
    credentials={}
    for line in a.provider_env.read_text().splitlines():
        if '=' in line and not line.lstrip().startswith('#'):
            key,value=line.split('=',1);credentials[key.strip()]=value.strip().strip('\"\'')
    provider=LiveProviderV2(credentials['MINIMAX_API_KEY']);evaluator=Evaluator(a.source_root,golds)
    registration={'namespace':'E2_DEVELOPMENT_V2_D2','label':LABEL,'started_utc':utc(),'d1_head':D1,'selection_rule_commit':RULE,
                  'first_runner_commit':a.first_runner_commit,'integrity':checks,'schedule':schedule,'private_root':str(a.private_output),'retries':0,'confirmatory_tasks_executed':0}
    (a.output/'registration.json').write_text(json.dumps(registration,indent=2)+'\n')
    completed=0
    for cell in schedule:
        # Read-only admission file or externally saved STOP closes the next cell, never retries.
        if (a.output/'STOP').exists():break
        admit_d2(cell);append(a.output/'attempts.jsonl',{**cell,'started_utc':utc()})
        private=a.private_output/cell['cell_id'];private.mkdir(mode=0o700)
        try:
            key=cell['family'],cell['task_id']
            ep=ObservedD2Episode(cell,tasks[key],policies[key],schema,provider,evaluator,private)
            result=ep.execute()
        except Exception as exc:
            result={**cell,'termination':'IMPLEMENTATION_DEFECT','valid':False,'implementation_defect_type':type(exc).__name__,'live_integrity_defects':['RUNNER_SETUP_OR_AUDIT_EXCEPTION']}
            write_private(private/'setup_failure.json',result)
        append(a.output/'episodes.jsonl',result);completed+=1
        (a.output/'status.json').write_text(json.dumps({'completed':completed,'latest_cell':cell['cell_id'],'termination':result['termination']})+'\n')
        print(json.dumps({'cell':cell['order'],'family':cell['family'],'arm':cell['defense'],'condition':cell['condition'],'termination':result['termination'],'calls':len(result.get('calls',[])),'treatment':result.get('treatment'),'principals':result.get('principal_invocations')}),flush=True)
        if result.get('live_integrity_defects') or result['termination']=='IMPLEMENTATION_DEFECT':
            (a.output/'STOP').write_text('IMPLEMENTATION_DEFECT\n');break
    (a.output/'completion.json').write_text(json.dumps({'finished_utc':utc(),'attempted':completed,'unattempted_by_hard_stop':54-completed,'all54attempted':completed==54,'confirmatory_tasks_executed':0,'formal_model_runs_executed':0,'reruns':0},indent=2)+'\n')
if __name__=='__main__':main()
