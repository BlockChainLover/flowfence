#!/usr/bin/env python3
"""Offline regression of actual D3 CLI registration and continuation-only admission."""
import argparse,json,subprocess,sys,tempfile
from copy import deepcopy
from pathlib import Path
from scripts.run_e2_d3_live import (make_registration,validate_registration,admit_continuation,
    continuation_schedule,preserve_original,FIRST_RUNNER,SCIENTIFIC_NAMESPACE,RUN_INSTANCE,D3,load)


def rejected(fn):
    try:fn()
    except AssertionError:return
    raise AssertionError('INVALID_REGISTRATION_OR_ADMISSION_ACCEPTED')


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    def deny(event,args):
        if event.startswith('socket.'):raise RuntimeError('OFFLINE_TEST_NO_NETWORK')
    sys.addaudithook(deny)
    original=preserve_original();schedule=continuation_schedule();assert len(schedule)==53
    with tempfile.TemporaryDirectory() as td:
        out=Path(td)/'registration'
        command=[sys.executable,'scripts/run_e2_d3_live.py','--registration-only','--first-runner-commit',FIRST_RUNNER,'--registration-fix-commit','OFFLINE_TEST',
            '--source-root','DO_NOT_READ','--schema','DO_NOT_READ','--provider-env','DO_NOT_READ','--private-output','DO_NOT_CREATE','--output',str(out)]
        subprocess.run(command,check=True,stdout=subprocess.DEVNULL)
        reg=load(out/'registration.json');validate_registration(reg)
        assert reg['namespace']==reg['scientific_namespace']==SCIENTIFIC_NAMESPACE
        assert reg['run_instance_id']==RUN_INSTANCE and reg['run_instance_id']!=reg['namespace']
        assert [c['order'] for c in reg['schedule']]==list(range(2,55))
        for c in schedule:admit_continuation(c);assert c['namespace']==reg['namespace']
        rejected(lambda:admit_continuation(load(D3/'CELL_SCHEDULE.json')[0]))
        for namespace in ('E2_DEVELOPMENT_V1','E2_DEVELOPMENT_V2_D2','E2_DEVELOPMENT_V2_D3','E2_CONFIRMATORY'):
            bad=deepcopy(reg);bad['namespace']=namespace;bad['scientific_namespace']=namespace
            rejected(lambda:validate_registration(bad))
            rejected(lambda:admit_continuation({**schedule[0],'namespace':namespace}))
        bad=deepcopy(reg);bad['schedule'][0]['namespace']='E2_DEVELOPMENT_V2_D3';rejected(lambda:validate_registration(bad))
        excluded=load('artifacts/aamas2027_e2_source_s1f/development.json')+load('artifacts/aamas2027_e2_source_s1f/confirmatory.json')+load('artifacts/aamas2027_e2_v2_d2/development.json')
        for r in excluded:rejected(lambda r=r:admit_continuation({**schedule[0],'family':r['family'],'task_id':r['task_id']}))
        rejected(lambda:admit_continuation({**schedule[0],'task_id':'arbitrary'}))
        assert not Path('DO_NOT_CREATE').exists()
    assert preserve_original()==original
    result={'status':'PASS','actual_cli_registration_generated':True,'scientific_namespace':SCIENTIFIC_NAMESPACE,'run_instance_id':RUN_INSTANCE,
        'schedule_namespace_match':True,'selection_namespace_match':True,'all_admitted_cell_namespaces_match':True,
        'old_and_confirmatory_namespaces_rejected':True,'cell001_rejected':True,'only_002_to_054_admitted':True,'admitted_cells':53,'prior_task_ids_rejected':len(excluded),
        'original_evidence_preservation':original,'credential_file_read':False,'live_calls':0,'scientific_configuration_changed':False}
    a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
if __name__=='__main__':main()
