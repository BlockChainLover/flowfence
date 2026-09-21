#!/usr/bin/env python3
"""Execute only human-approved E2-A cells054–720 in a separate run, once."""
import argparse
import json
import os
import subprocess
from pathlib import Path
from src.e2_live.e2a import *
from src.e2_live.pilot import Evaluator, utc, sha, write_private
from src.e2_live.transport_v2 import LiveProviderV2
from scripts.run_e2_development_pilot import append

ORIGINAL_HEAD='f5f6fa8849df45c67de351dc719abab9e070e83b'
PREREG='2a8e3910a133862a0df9f53a47131d798da047c1'
ORIGINAL_RUN=ROOT/'run'
RUN_INSTANCE='E2A_FORMAL_CONTINUATION_054_720_001'


def rows(path):return [json.loads(x) for x in Path(path).read_text().splitlines() if x.strip()]


def continuation_schedule():
    schedule=load(SCHEDULE)
    assert schedule==make_schedule() and len(schedule)==720
    original=rows(ORIGINAL_RUN/'attempts.jsonl')
    assert len(original)==53 and all(all(row[k]==v for k,v in cell.items()) for row,cell in zip(original,schedule[:53]))
    return schedule[53:]


def admit_continuation(cell):
    admit(cell)
    assert cell in continuation_schedule(),'NOT_AUTHORIZED_CONTINUATION_CELL'


def preserve_original():
    paths=subprocess.check_output(['git','ls-tree','-r','--name-only',ORIGINAL_HEAD,str(ROOT)],text=True).splitlines()
    for path in paths:assert Path(path).read_bytes()==subprocess.check_output(['git','show',ORIGINAL_HEAD+':'+path]),path
    private_index=load(ROOT/'derived/artifact_index.json')['private_files']
    for item in private_index:assert sha(Path(item['path']).read_bytes())==item['sha256'],'ORIGINAL_PRIVATE_EVIDENCE_CHANGED'
    episodes=rows(ORIGINAL_RUN/'episodes.jsonl')
    assert len(episodes)==53 and all(e['valid'] for e in episodes)
    assert load(ORIGINAL_RUN/'registration.json')['E2A_FORMAL_PREREG_COMMIT']==PREREG
    return {'original_safe_files_preserved':len(paths),'original_private_files_preserved':len(private_index),'original_cells_retained':53,'original_cells_rerun':0}


def registration(fix_commit,private,checks=None):
    value=dict(namespace=NAMESPACE,scientific_namespace=NAMESPACE,run_instance_id=RUN_INSTANCE,label=LABEL,
        E2A_FORMAL_PREREG_COMMIT=PREREG,E2A_REPORTING_FIX_COMMIT=fix_commit,private_root=str(private),
        schedule=continuation_schedule(),original_run_ref=str(ORIGINAL_RUN),original_cells_retained=53,
        original_cells_rerun=0,retries=0,repairs=0,E2_B_STATUS='DEFERRED_NOT_SELECTED',integrity=checks or {})
    validate_registration(value)
    return value


def validate_registration(value):
    assert value['namespace']==value['scientific_namespace']==NAMESPACE
    assert value['run_instance_id']==RUN_INSTANCE
    assert value['E2A_FORMAL_PREREG_COMMIT']==PREREG
    assert value['schedule']==continuation_schedule() and len(value['schedule'])==667
    for cell in value['schedule']:admit_continuation(cell)


def main():
    p=argparse.ArgumentParser(description=__doc__)
    for name in ('source-root','provider-env','output','private-output'):p.add_argument('--'+name,type=Path,required=True)
    p.add_argument('--reporting-fix-commit',required=True)
    p.add_argument('--registration-only',action='store_true',help='Validate/save registration without reading credentials or dispatching.')
    a=p.parse_args()
    reg=registration(a.reporting_fix_commit,a.private_output)
    if a.registration_only:
        assert not a.output.exists();a.output.mkdir(parents=True)
        (a.output/'registration.json').write_text(json.dumps(reg,indent=2)+'\n')
        print(json.dumps({'registration_only':'PASS','cells':667,'live_calls':0}));return
    head=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()
    assert head==a.reporting_fix_commit
    assert subprocess.check_output(['git','branch','--show-current'],text=True).strip()==BRANCH
    assert not subprocess.check_output(['git','diff','HEAD','--name-only'])
    remote=subprocess.check_output(['git','ls-remote','--heads','origin',BRANCH],text=True).split()[0]
    assert remote==head,'REPORTING_FIX_NOT_PUSHED'
    checks=verify(a.source_root);checks.update(preserve_original())
    for path in subprocess.check_output(['git','ls-tree','-r','--name-only',ORIGINAL_HEAD,'src','experiments','E2A_FORMAL_CELL_SCHEDULE.json','E2A_PREREGISTRATION_AMENDMENT.md','scripts/run_e2a_formal.py'],text=True).splitlines():
        assert Path(path).read_bytes()==subprocess.check_output(['git','show',ORIGINAL_HEAD+':'+path]),path
    tasks,policies,golds=inputs(a.source_root)
    schedule=continuation_schedule()
    assert not a.output.exists() and not a.private_output.exists(),'NO_RERUN_OR_RESUME'
    for path in (a.output,a.private_output):path.mkdir(parents=True,mode=0o700)
    os.chmod(a.private_output,0o700)
    credentials={}
    for line in a.provider_env.read_text().splitlines():
        if '=' in line and not line.lstrip().startswith('#'):
            key,value=line.split('=',1);credentials[key.strip()]=value.strip().strip('\"\'')
    provider=LiveProviderV2(credentials['MINIMAX_API_KEY']);evaluator=Evaluator(a.source_root,golds)
    reg=registration(head,a.private_output,checks);reg.update(started_utc=utc(),remote_fix_commit=remote)
    (a.output/'registration.json').write_text(json.dumps(reg,indent=2)+'\n')
    (a.output/'preflight.json').write_text(json.dumps({'CONTINUATION_PREFLIGHT':'PASS','cells':667,'E2A_REPORTING_FIX_COMMIT':head,**checks},indent=2)+'\n')
    completed=0
    for cell in schedule:
        if (a.output/'STOP').exists():break
        admit_continuation(cell)
        append(a.output/'attempts.jsonl',{**cell,'started_utc':utc()})
        private=a.private_output/cell['cell_id'];private.mkdir(mode=0o700)
        try:
            key=cell['family'],cell['task_id']
            result=FormalEpisode(cell,tasks[key],policies[key],{},provider,evaluator,private).execute()
        except Exception as exc:
            result={**cell,'label':LABEL,'termination':'IMPLEMENTATION_DEFECT','valid':False,
                    'implementation_defect_type':type(exc).__name__,'live_integrity_defects':['RUNNER_SETUP_OR_AUDIT_EXCEPTION']}
            write_private(private/'setup_failure.json',result)
        append(a.output/'episodes.jsonl',result);completed+=1
        (a.output/'status.json').write_text(json.dumps({'completed':completed,'latest_cell':cell['cell_id'],'termination':result['termination']})+'\n')
        print(json.dumps({'cell':cell['order'],'family':cell['family'],'defense':cell['defense'],'condition':cell['condition'],'repetition':cell['repetition'],'termination':result['termination']}),flush=True)
        if result.get('live_integrity_defects') or result['termination']=='IMPLEMENTATION_DEFECT':
            (a.output/'STOP').write_text('IMPLEMENTATION_DEFECT\n');break
    (a.output/'completion.json').write_text(json.dumps({'finished_utc':utc(),'attempted':completed,'unattempted_by_hard_stop':667-completed,'all667attempted':completed==667,'run_instance_id':RUN_INSTANCE,'reruns':0,'BIRD_FORMAL_EPISODES_EXECUTED':0,'E2_B_STATUS':'DEFERRED_NOT_SELECTED'},indent=2)+'\n')

if __name__=='__main__':main()
