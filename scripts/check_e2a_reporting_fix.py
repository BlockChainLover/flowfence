#!/usr/bin/env python3
"""Zero-call regression for minimal defect records, unchanged prefix, and continuation admission."""
import argparse,json,subprocess,sys,tempfile
from pathlib import Path
from scripts.run_e2a_continuation import *


def dump(p,v):p.write_text(json.dumps(v,indent=2)+'\n')


def assert_retained(old,new):
    if isinstance(old,dict):
        for k,v in old.items():assert k in new,k;assert_retained(v,new[k])
    else:assert old==new,(old,new)


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    def deny(event,args):
        if event.startswith('socket.'):raise RuntimeError('NETWORK_DISABLED')
    sys.addaudithook(deny)
    checks=preserve_original();suffix=continuation_schedule();assert len(suffix)==667 and [c['order'] for c in suffix]==list(range(54,721))
    for c in suffix:admit_continuation(c)
    invalid=load(SCHEDULE)[:53]
    invalid += [{**suffix[0],'family':'bird_pg'},{**suffix[0],'namespace':'E2_B'},{**suffix[0],'task_id':'arbitrary-confirmatory-id'}]
    for name in ('development','confirmatory'):
        for r in load(S1F/(name+'.json')):
            if name=='development' or r['family']=='bird_pg':invalid.append({**suffix[0],'family':r['family'],'task_id':r['task_id']})
    for path in ('artifacts/aamas2027_e2_v2_d2/development.json','artifacts/aamas2027_e2_v3_d3/development.json'):
        invalid.extend({**suffix[0],'family':r['family'],'task_id':r['task_id']} for r in load(path))
    for c in invalid:
        try:admit_continuation(c)
        except AssertionError:pass
        else:raise AssertionError('CONTINUATION_ADMISSION_BYPASS')
    with tempfile.TemporaryDirectory() as td:
        root=Path(td);private=root/'private';private.mkdir()
        for size in (1,3):
            run=root/f'minimal_{size}';run.mkdir();episodes=[]
            for cell in load(SCHEDULE)[:size]:
                episodes.append({**cell,'label':LABEL,'termination':'IMPLEMENTATION_DEFECT','valid':False,'implementation_defect_type':'RuntimeError','live_integrity_defects':['RUNNER_SETUP_OR_AUDIT_EXCEPTION']})
            (run/'attempts.jsonl').write_text(''.join(json.dumps(c)+'\n' for c in load(SCHEDULE)[:size]))
            (run/'episodes.jsonl').write_text(''.join(json.dumps(e)+'\n' for e in episodes));dump(run/'completion.json',{})
            out=root/f'minimal_{size}_audit'
            subprocess.run([sys.executable,'scripts/summarize_e2a_formal.py','--run',str(run),'--private',str(private),'--output',str(out)],check=True,stdout=subprocess.DEVNULL)
            s=load(out/'summary.json')
            assert s['attempted']==s['implementation_defect_episodes']==size and s['valid']==s['completed_finals']==0
            assert s['planner_stage_success']==s['finance_stage_entered']==s['valid_finance_handoffs']==0
            assert all(v==size for v in s['unavailable_stage_fields'].values())
            assert sum(v['privacy_unknown'] for v in s['family_counts'].values())==size
            assert sum(v['task_unknown'] for v in s['family_counts'].values())==size
            assert load(out/'episode_summary.json')==episodes
            t=load(out/'stage_treatment_reachability.json')['observed_treatment_propagation']
            assert len(t)==size and all(r['valid_finance_handoff'] is None and r['planner_stage_success'] is None for r in t)
            if size==3:
                c=load(out/'stage_treatment_reachability.json')['conditions']['CONTAMINATION_A']
                assert c['attempted']==1 and c['unavailable_stage_observations']==1 and c['not_reached_early_failure']==0 and c['entered_mediation']==0
        out=root/'prefix_audit'
        subprocess.run([sys.executable,'scripts/summarize_e2a_formal.py','--run',str(ORIGINAL_RUN),'--private',load(ORIGINAL_RUN/'registration.json')['private_root'],'--output',str(out)],check=True,stdout=subprocess.DEVNULL)
        for old in (ROOT/'derived').glob('*.json'):assert_retained(load(old),load(out/old.name))
        assert (ROOT/'derived/release_audit.jsonl').read_bytes()==(out/'release_audit.jsonl').read_bytes()
        mockreg=root/'registration'
        subprocess.run([sys.executable,'scripts/run_e2a_continuation.py','--source-root','/not-used','--provider-env','/not-read','--output',str(mockreg),'--private-output',str(root/'unused'),'--reporting-fix-commit','REGRESSION_ONLY','--registration-only'],check=True,stdout=subprocess.DEVNULL)
        reg=load(mockreg/'registration.json');validate_registration(reg)
        assert reg['schedule'][0]['order']==54 and reg['schedule'][-1]['order']==720
        # Combined adapter reconstructs the immutable prefix without modifying original metadata.
        dump(mockreg/'preflight.json',{'CONTINUATION_PREFLIGHT':'REGRESSION_ONLY'})
        subprocess.run([sys.executable,'scripts/summarize_e2a_combined.py','--continuation',str(mockreg),'--output',str(root/'combined')],check=True,stdout=subprocess.DEVNULL)
        combined=load(root/'combined/derived/summary.json');assert combined['attempted']==53 and combined['continuation_attempted']==0 and combined['original_formal_cells_rerun']==0
        assert load(root/'combined/derived/episode_summary.json')==rows(ORIGINAL_RUN/'episodes.jsonl')
        # Mixed immutable prefix + exact minimal continuation failure must also aggregate.
        cell=suffix[0]
        minimal={**cell,'label':LABEL,'termination':'IMPLEMENTATION_DEFECT','valid':False,'implementation_defect_type':'RuntimeError','live_integrity_defects':['RUNNER_SETUP_OR_AUDIT_EXCEPTION']}
        (mockreg/'attempts.jsonl').write_text(json.dumps(cell)+'\n')
        (mockreg/'episodes.jsonl').write_text(json.dumps(minimal)+'\n');dump(mockreg/'completion.json',{})
        subprocess.run([sys.executable,'scripts/summarize_e2a_combined.py','--continuation',str(mockreg),'--output',str(root/'mixed')],check=True,stdout=subprocess.DEVNULL)
        mixed=load(root/'mixed/derived/summary.json')
        assert mixed['attempted']==54 and mixed['valid']==53 and mixed['implementation_defect_episodes']==1 and mixed['unattempted_by_hard_stop']==666
        assert load(root/'mixed/derived/episode_summary.json')[:53]==rows(ORIGINAL_RUN/'episodes.jsonl')
        subprocess.run([sys.executable,'scripts/report_e2a_formal.py','--root',str(root/'mixed'),'--report',str(root/'mixed_report.md')],check=True,stdout=subprocess.DEVNULL)
    checks.update(preserve_original())
    result={'status':'PASS','exact_zero_call_defect_fixture':'PASS','contaminated_missing_stage_fixture':'PASS','original53_summaries_unchanged':'PASS','original53_safe_raw_preserved':'PASS','admitted_suffix_cells':667,'invalid_admissions_rejected':len(invalid),'actual_cli_registration':'PASS','combined_prefix_adapter':'PASS','combined_minimal_defect_and_report':'PASS','live_model_calls':0,'original_evaluator_calls':0,'preservation':checks}
    a.output.parent.mkdir(parents=True,exist_ok=True);dump(a.output,result);print(json.dumps(result))

if __name__=='__main__':main()
