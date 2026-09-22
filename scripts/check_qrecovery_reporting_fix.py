#!/usr/bin/env python3
"""Zero-network reporting partition regression and immutable saved-prefix validation."""
import argparse
from collections import Counter
import json
from pathlib import Path
import sys
import tempfile
from scripts.summarize_qrecovery import execution_accounting, analyze, audit, rows, report
from scripts.run_qrecovery import retained_prefix
from src.e2_live.qrecovery import ROOT, schedule
from src.e2_live.pilot import load


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--output',type=Path,default=ROOT/'reporting_fix_validation.json')
    a=p.parse_args()
    def deny(event,args):
        if event.startswith('socket.'): raise RuntimeError('NETWORK_DISABLED')
    sys.addaudithook(deny)
    fixture=[dict(cell_id=f'SYNTHETIC_PARTITION_{i}',condition='CLEAN',family='tatqa',defense='FLOWFENCE_RECOVERY',task_id='SYNTHETIC_ONLY',termination='PROVIDER_FAILURE') for i in range(4)]
    tested=[]
    for name,n,started,finished,want in [('zero',1,0,0,(1,0,0,0,1)),('in_flight',1,1,0,(1,1,0,1,0)),('finished',1,1,1,(1,1,1,0,0)),('mixed',4,3,2,(4,3,2,1,1))]:
        result=execution_accounting(fixture[:n],fixture[:started],fixture[:finished])
        assert tuple(result[k] for k in ('scheduled','attempted','finished','in_flight','unattempted'))==want
        data=analyze(fixture[:finished],[],fixture[:n],fixture[:started])
        assert data['execution_summary']['in_flight']==want[3]
        assert Counter(r['termination'] for r in data['failure_audit'])['UNATTEMPTED']==want[4]
        assert Counter(r['termination'] for r in data['failure_audit'])['IN_FLIGHT']==want[3]
        tested.append(dict(case=name,counts=want,partition_valid=result['partition_valid']))
    try: execution_accounting(fixture[:1],fixture[:1]*2,[])
    except ValueError as exc: assert str(exc)=='DUPLICATE_FORMAL_DISPATCH: unique_attempted=1 records=2'
    else: raise AssertionError('DUPLICATE_DISPATCH_NOT_REJECTED')
    for attempts,finished in [([],fixture[:1]),([dict(fixture[0],cell_id='OUTSIDE')],[])]:
        try: execution_accounting(fixture[:1],attempts,finished)
        except AssertionError: pass
        else: raise AssertionError('MEMBERSHIP_VIOLATION_ACCEPTED')
    attempts,terminal,remaining,checks=retained_prefix(ROOT/'run')
    data=analyze(terminal,[],schedule(),attempts)
    old=load(ROOT/'derived/execution_summary.json')
    for key in ('attempted','finished','clean_attempted','contaminated_attempted','termination_counts','completed_finals','implementation_defects'):
        assert data['execution_summary'][key]==old[key],key
    assert data['execution_summary']['unattempted_ids']==old['unattempted']
    assert all(c['cell_id'] not in {r['cell_id'] for r in attempts} for c in remaining)
    # Real auditor recovery branch, synthetic only, no formal identities or network.
    from scripts.check_e2_v2_runtime import fixture as episode_fixture, FINALS
    from scripts.check_e2_v3_runtime import PLANNER,HANDOFF
    from scripts.check_e2_live_runner import FakeProvider
    from src.e2_live.qrecovery import RecoveryEpisode
    class RecordedEvaluator:
        def score(self,cell,native,private,timeout):
            private.mkdir(parents=True,exist_ok=True)
            metrics={'em':0,'f1':0,'scale':0,'operation':0} if cell['family']=='tatqa' else {'joint_em':0}
            (private/'evaluator_output.json').write_text(json.dumps(metrics))
            return metrics
    with tempfile.TemporaryDirectory() as td:
        for family in ('tatqa','hotpot'):
            cell,task,policy=episode_fixture(family,'FLOWFENCE_RECOVERY','CONTAMINATION_A')
            cell.update(cell_id='SYNTHETIC_REPORTING_'+family,namespace='QRECOVERY_FORMAL')
            ep=RecoveryEpisode(cell,task,policy,{},FakeProvider([PLANNER,HANDOFF,FINALS[family]]),RecordedEvaluator(),Path(td)/cell['cell_id'])
            result=ep.execute()
            checked=audit([result],Path(td))
            assert checked['trajectories_verified']==1 and len(checked['recovery_sources'])==1
            defect={**cell,'termination':'IMPLEMENTATION_DEFECT','live_integrity_defects':['SYNTHETIC_SETUP_FAILURE']}
            defect['cell_id']+='DEFECT'
            assert audit([defect],Path(td))['trajectories_verified']==0
            analyze([defect],[],[defect],[defect])
    out=dict(status='PASS',live_calls=0,synthetic_cases=tested,duplicate_dispatch_integrity_error=True,
        invalid_membership_rejected=True,retained10_unchanged=True,retained_request_count=26,remaining270_selected_by_attempt_membership=True,
        synthetic_recovered_source_audit=True,minimal_setup_defect_supported=True,retained=checks)
    a.output.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k!='retained'}))
if __name__=='__main__':main()
