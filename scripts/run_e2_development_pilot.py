#!/usr/bin/env python3
"""Execute only the 54 preregistered E2 development cells; never retry/resume."""
import argparse
import json
import os
from pathlib import Path
import subprocess
from src.e2_live.pilot import Episode, Evaluator, LiveProvider, CONFIG, PREREG, load, inputs, integrity, admit, write_private, utc


def append(path,value):
    with path.open('a') as f:
        f.write(json.dumps(value,ensure_ascii=False,allow_nan=False)+'\n');f.flush();os.fsync(f.fileno())

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--source-root',type=Path,required=True);p.add_argument('--schema',type=Path,required=True)
    p.add_argument('--provider-env',type=Path,required=True);p.add_argument('--output',type=Path,required=True)
    p.add_argument('--private-output',type=Path,required=True);p.add_argument('--first-runner-commit',required=True)
    p.add_argument('--hotpot-amendment-commit',required=True)
    a=p.parse_args()
    assert subprocess.check_output(['git','branch','--show-current'],text=True).strip()=='codex/aamas2027-e2-development-pilot'
    for commit in (PREREG,a.first_runner_commit,a.hotpot_amendment_commit):subprocess.run(['git','merge-base','--is-ancestor',commit,'HEAD'],check=True)
    assert not subprocess.check_output(['git','diff','--name-only','HEAD']), 'UNCOMMITTED_TRACKED_CHANGES'
    assert subprocess.check_output(['git','show',a.first_runner_commit+':src/e2_live/pilot.py'])==Path('src/e2_live/pilot.py').read_bytes()
    checks=integrity(a.source_root);schema=load(a.schema);tasks,policies,golds=inputs(a.source_root,schema)
    schedule=load(CONFIG/'DEVELOPMENT_CELL_SCHEDULE.json');assert len(schedule)==54
    for cell in schedule:admit(cell,schedule,tasks)
    assert len({(x['family'],x['task_id'],x['condition'],x['defense'],x['repetition']) for x in schedule})==54
    for path in (a.output,a.private_output):
        assert not path.exists(),'NO_RETRY_OR_RESUME_EXISTING_OUTPUT'
        path.mkdir(parents=True,mode=0o700)
    values={}
    for line in a.provider_env.read_text().splitlines():
        if line.strip().startswith('#') or '=' not in line:continue
        key,value=line.split('=',1);values[key.strip()]=value.strip().strip('\"\'')
    assert values.get('MINIMAX_API_KEY'),'CREDENTIAL_UNAVAILABLE'
    provider=LiveProvider(values['MINIMAX_API_KEY']);evaluator=Evaluator(a.source_root,golds)
    registration={'label':'DEVELOPMENT_ONLY — NOT CONFIRMATORY EVIDENCE','started_utc':utc(),
       'pre_run_prereg_commit':PREREG,'first_live_runner_commit':a.first_runner_commit,
       'hot_pot_metric_freeze_commit':a.hotpot_amendment_commit,'integrity':checks,
       'cells':schedule,'private_root':str(a.private_output),'retries':0,'confirmatory_tasks_executed':0,'formal_model_runs_executed':0}
    (a.output/'registration.json').write_text(json.dumps(registration,indent=2)+'\n')
    # Manifest is public metadata only, provider key never enters any artifact.
    for cell in schedule:
        admit(cell,schedule,tasks)
        cell_id=f"cell_{cell['order']:03d}";private=a.private_output/cell_id
        private.mkdir(mode=0o700)
        append(a.output/'attempts.jsonl',{**cell,'started_utc':utc()})
        key=cell['family'],cell['task_id']
        try:
            episode=Episode(cell,tasks[key],policies[key],schema,provider,evaluator,private)
            result=episode.execute()
        except Exception as exc:
            result={**cell,'termination':'IMPLEMENTATION_DEFECT','valid':False,'implementation_defect_type':type(exc).__name__}
            write_private(private/'setup_failure.json',result)
        append(a.output/'episodes.jsonl',result)
        (a.output/'status.json').write_text(json.dumps({'attempted':cell['order'],'latest_termination':result['termination'],'latest_cell':cell_id,'model_requests_so_far_in_cell':len(result.get('calls',[]))})+'\n')
        print(json.dumps({'cell':cell['order'],'family':cell['family'],'defense':cell['defense'],'termination':result['termination'],'calls':len(result.get('calls',[]))}),flush=True)
        if result['termination']=='IMPLEMENTATION_DEFECT':
            print('HARD_STOP_IMPLEMENTATION_DEFECT',flush=True);break
    (a.output/'completion.json').write_text(json.dumps({'finished_utc':utc(),'last_cell':cell['order'],'hard_stop':result['termination']=='IMPLEMENTATION_DEFECT','integrity':integrity(a.source_root),'confirmatory_tasks_executed':0,'formal_model_runs_executed':0},indent=2)+'\n')

if __name__=='__main__':main()
