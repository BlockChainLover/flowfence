#!/usr/bin/env python3
"""Execute only frozen D3 cells002–054 in a new continuation run; never rerun cell001."""
import argparse
import json
import os
from pathlib import Path
import subprocess
from src.e2_live.d3 import *
from src.e2_live.transport_v2 import LiveProviderV2
from scripts.run_e2_development_pilot import append


SCIENTIFIC_NAMESPACE='E2_DEVELOPMENT_V3_D3'
RUN_INSTANCE='E2_DEVELOPMENT_V3_D3_CONTINUATION_001'
FIRST_RUNNER='792620bb7cea6ac1e697aaae5f2fe721a1ba37b5'
ORIGINAL_HEAD='07c2e629114b88546cccbe14eb1491fc1e9947bd'
ORIGINAL_RUN=Path('artifacts/aamas2027_e2_v3_d3_live/run')


def admit_continuation(cell):
    admit_d3(cell)
    assert cell in load(D3/'CELL_SCHEDULE.json')[1:],'NOT_CONTINUATION_SUFFIX'


def continuation_schedule():
    full=load(D3/'CELL_SCHEDULE.json')
    assert len(full)==54 and [c['order'] for c in full]==list(range(1,55))
    old=[json.loads(x) for x in (ORIGINAL_RUN/'attempts.jsonl').read_text().splitlines()]
    assert len(old)==1 and all(old[0][k]==v for k,v in full[0].items()),'ORIGINAL_ATTEMPT_MISMATCH'
    suffix=full[1:]
    for cell in suffix:admit_continuation(cell)
    return suffix


def validate_registration(registration):
    assert registration['namespace']==registration['scientific_namespace']==SCIENTIFIC_NAMESPACE,'REGISTRATION_NAMESPACE_MISMATCH'
    assert registration['run_instance_id']==RUN_INSTANCE
    assert registration['schedule']==continuation_schedule(),'CONTINUATION_SCHEDULE_MISMATCH'
    assert load(D3/'selection_provenance.json')['namespace']==SCIENTIFIC_NAMESPACE
    for row in load(D3/'development.json'):assert row['namespace']==SCIENTIFIC_NAMESPACE
    for cell in load(D3/'CELL_SCHEDULE.json'):assert cell['namespace']==SCIENTIFIC_NAMESPACE
    for cell in registration['schedule']:
        admit_continuation(cell)
        assert cell['namespace']==registration['namespace']


def make_registration(first_runner_commit,fix_commit,checks,private_output):
    registration={'namespace':SCIENTIFIC_NAMESPACE,'scientific_namespace':SCIENTIFIC_NAMESPACE,
        'run_instance_id':RUN_INSTANCE,'label':LABEL,'started_utc':utc(),'d1_head':D1,'selection_rule_commit':RULE,
        'first_runner_commit':first_runner_commit,'registration_fix_commit':fix_commit,'integrity':checks,
        'schedule':continuation_schedule(),'private_root':str(private_output),'retries':0,'confirmatory_tasks_executed':0,
        'original_run_ref':str(ORIGINAL_RUN),'cell001_registration_metadata_defect':True,'cell001_rerun':False}
    validate_registration(registration)
    return registration


def preserve_original():
    prefix='artifacts/aamas2027_e2_v3_d3_live'
    paths=subprocess.check_output(['git','ls-tree','-r','--name-only',ORIGINAL_HEAD,prefix],text=True).splitlines()
    for path in paths:assert Path(path).read_bytes()==subprocess.check_output(['git','show',ORIGINAL_HEAD+':'+path]),path
    original=load(ORIGINAL_RUN/'registration.json');assert original['namespace']=='E2_DEVELOPMENT_V2_D3'
    ep=json.loads((ORIGINAL_RUN/'episodes.jsonl').read_text())
    assert ep['termination']=='PROTOCOL_FAILURE' and ep['valid'] and ep['privacy'] is None and not ep['completed_final']
    for item in load(Path(prefix)/'derived/artifact_index.json')['private_files']:
        assert sha(Path(item['path']).read_bytes())==item['sha256'],'ORIGINAL_PRIVATE_EVIDENCE_CHANGED'
    return {'original_safe_files_preserved':len(paths),'original_raw_evidence_preserved':True,'cell001_status':'VALID_DEVELOPMENT_OBSERVATION_WITH_REGISTRATION_METADATA_DEFECT'}


def main():
    p=argparse.ArgumentParser(description=__doc__)
    for name in ('source-root','schema','provider-env','output','private-output'):p.add_argument('--'+name,type=Path,required=True)
    p.add_argument('--first-runner-commit',required=True)
    p.add_argument('--registration-fix-commit',required=True)
    p.add_argument('--registration-only',action='store_true',help='Generate/validate prospective registration without loading credentials or dispatching.')
    a=p.parse_args()
    registration=make_registration(a.first_runner_commit,a.registration_fix_commit,{},a.private_output)
    if a.registration_only:
        assert not a.output.exists()
        a.output.mkdir(parents=True)
        (a.output/'registration.json').write_text(json.dumps(registration,indent=2)+'\n')
        print(json.dumps({'registration_only':'PASS','cells':len(registration['schedule']),'live_calls':0}))
        return
    assert a.first_runner_commit==FIRST_RUNNER
    subprocess.run(['git','merge-base','--is-ancestor',a.registration_fix_commit,'HEAD'],check=True)
    remote=subprocess.check_output(['git','ls-remote','--heads','origin','codex/aamas2027-e2-development-v3'],text=True).split()[0]
    assert remote==a.registration_fix_commit,'FIX_COMMIT_NOT_REMOTE_HEAD'
    assert subprocess.check_output(['git','branch','--show-current'],text=True).strip()=='codex/aamas2027-e2-development-v3'
    assert not subprocess.check_output(['git','diff','HEAD','--name-only']),'UNCOMMITTED_TRACKED_CHANGES'
    subprocess.run(['git','merge-base','--is-ancestor',a.first_runner_commit,'HEAD'],check=True)
    for file in ('scripts/run_e2_d3_live.py','src/e2_live/d3.py'):
        assert subprocess.check_output(['git','show',a.registration_fix_commit+':'+file])==Path(file).read_bytes()
    checks=verify(a.source_root);checks.update(preserve_original())
    assert sha(a.schema.read_bytes())==load('artifacts/aamas2027_e2_v2_d2_live/environment_validation.json')['source_schema_sha256'],'SOURCE_SCHEMA_CHANGED'
    schema=load(a.schema);tasks,policies,golds=d3_inputs(a.source_root,schema)
    schedule=continuation_schedule()
    registration=make_registration(a.first_runner_commit,a.registration_fix_commit,checks,a.private_output)
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
    (a.output/'registration.json').write_text(json.dumps(registration,indent=2)+'\n')
    (a.output/'preflight.json').write_text(json.dumps({'D3_CONTINUATION_PREFLIGHT':'PASS','registration_invariant':'PASS','remaining_cells':53,'remote_fix_commit':remote,**checks},indent=2)+'\n')
    completed=0
    for cell in schedule:
        # Read-only admission file or externally saved STOP closes the next cell, never retries.
        if (a.output/'STOP').exists():break
        admit_continuation(cell);append(a.output/'attempts.jsonl',{**cell,'started_utc':utc()})
        private=a.private_output/cell['cell_id'];private.mkdir(mode=0o700)
        try:
            key=cell['family'],cell['task_id']
            ep=ObservedD3Episode(cell,tasks[key],policies[key],schema,provider,evaluator,private)
            result=ep.execute()
        except Exception as exc:
            result={**cell,'termination':'IMPLEMENTATION_DEFECT','valid':False,'implementation_defect_type':type(exc).__name__,'live_integrity_defects':['RUNNER_SETUP_OR_AUDIT_EXCEPTION']}
            write_private(private/'setup_failure.json',result)
        append(a.output/'episodes.jsonl',result);completed+=1
        (a.output/'status.json').write_text(json.dumps({'completed':completed,'latest_cell':cell['cell_id'],'termination':result['termination']})+'\n')
        print(json.dumps({'cell':cell['order'],'family':cell['family'],'arm':cell['defense'],'condition':cell['condition'],'termination':result['termination'],'calls':len(result.get('calls',[])),'treatment':result.get('treatment'),'principals':result.get('principal_invocations')}),flush=True)
        if result.get('live_integrity_defects') or result['termination']=='IMPLEMENTATION_DEFECT':
            (a.output/'STOP').write_text('IMPLEMENTATION_DEFECT\n');break
    (a.output/'completion.json').write_text(json.dumps({'finished_utc':utc(),'attempted':completed,'unattempted_by_hard_stop':53-completed,'all53attempted':completed==53,'run_instance_id':RUN_INSTANCE,'confirmatory_tasks_executed':0,'formal_model_runs_executed':0,'reruns':0},indent=2)+'\n')
if __name__=='__main__':main()
