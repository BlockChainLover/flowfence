#!/usr/bin/env python3
"""Read-only combined D3 audit: immutable original001 plus continuation suffix; no dispatch."""
import argparse,json,subprocess,sys,tempfile
from pathlib import Path
from scripts.run_e2_d3_live import preserve_original,validate_registration,ORIGINAL_RUN,D3,load


def rows(p):return [json.loads(x) for x in p.read_text().splitlines() if x.strip()]
def dump(p,v):p.write_text(json.dumps(v,indent=2,ensure_ascii=False,allow_nan=False)+'\n')


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--continuation',type=Path,required=True);p.add_argument('--output',type=Path,required=True)
    a=p.parse_args();preserve_original()
    original_reg=load(ORIGINAL_RUN/'registration.json');continuation_reg=load(a.continuation/'registration.json');validate_registration(continuation_reg)
    assert original_reg['namespace']=='E2_DEVELOPMENT_V2_D3'
    originals=rows(ORIGINAL_RUN/'episodes.jsonl');assert len(originals)==1
    continued=rows(a.continuation/'episodes.jsonl') if (a.continuation/'episodes.jsonl').exists() else []
    original_attempts=rows(ORIGINAL_RUN/'attempts.jsonl');continuation_attempts=rows(a.continuation/'attempts.jsonl') if (a.continuation/'attempts.jsonl').exists() else []
    schedule=load(D3/'CELL_SCHEDULE.json')
    assert [e['cell_id'] for e in continuation_attempts]==[c['cell_id'] for c in schedule[1:1+len(continuation_attempts)]]
    assert [e['cell_id'] for e in continued]==[e['cell_id'] for e in continuation_attempts[:len(continued)]]
    episodes=originals+continued;attempts=original_attempts+continuation_attempts
    assert len({e['cell_id'] for e in attempts})==len(attempts)
    roots={};provenance=[]
    for ep in episodes:
        first=ep['order']==1;reg=original_reg if first else continuation_reg;run=ORIGINAL_RUN if first else a.continuation
        private=Path(reg['private_root'])/ep['cell_id'];roots[ep['cell_id']]=private
        provenance.append({'cell_id':ep['cell_id'],'scientific_namespace':ep['namespace'],'run_root':str(run),'run_instance_id':reg.get('run_instance_id'),
            'registration_path':str(run/'registration.json'),'recorded_registration_namespace':reg['namespace'],'registration_metadata_defect':first,
            'status':'VALID_DEVELOPMENT_OBSERVATION_WITH_REGISTRATION_METADATA_DEFECT' if first else 'CONTINUATION_DEVELOPMENT_OBSERVATION',
            'termination':ep['termination'],'rerun':False,'private_trajectory_path':str(private/'trajectory.json')})
    a.output.mkdir(parents=True,exist_ok=True)
    with tempfile.TemporaryDirectory() as td:
        root=Path(td);run=root/'combined_input';run.mkdir();private=root/'private_links';private.mkdir()
        (run/'attempts.jsonl').write_text(''.join(json.dumps(e)+'\n' for e in attempts))
        (run/'episodes.jsonl').write_text(''.join(json.dumps(e)+'\n' for e in episodes))
        if (a.continuation/'completion.json').exists():dump(run/'completion.json',load(a.continuation/'completion.json'))
        for cell,source in roots.items():(private/cell).symlink_to(source,target_is_directory=True)
        subprocess.run([sys.executable,'scripts/summarize_e2_d3_live.py','--run',str(run),'--private',str(private),'--output',str(a.output)],check=True,stdout=subprocess.DEVNULL)
        index=load(a.output/'artifact_index.json')
        for item in index['private_files']:
            cell=item['cell_id'];relative=Path(item['path']).relative_to(private/cell);item['path']=str(roots[cell]/relative)
        dump(a.output/'artifact_index.json',index)
    summary=load(a.output/'summary.json')
    summary.update(cell001_status='VALID_DEVELOPMENT_OBSERVATION_WITH_REGISTRATION_METADATA_DEFECT',cell001_registration_metadata_defect=True,
        cell001_rerun=False,registration_fix_commit=continuation_reg['registration_fix_commit'],registration_integrity='PROSPECTIVE_FIX_VERIFIED_ORIGINAL_DEFECT_DISCLOSED',
        historical_implementation_defects=[{'code':'REGISTRATION_NAMESPACE_MISMATCH','resolution':'HUMAN_ACCEPTED_ORIGINAL_OBSERVATION_PROSPECTIVE_METADATA_FIX','original_preserved':True}],
        continuation_attempted=len(continuation_attempts),continuation_finished=len(continued),implementation_fixes_after_first_D3_outcome='REGISTRATION_METADATA_FIX_ONLY',
        continuation_preflight=load(a.continuation/'preflight.json')['D3_CONTINUATION_PREFLIGHT'])
    # No new utility/treatment threshold. Existing episode integrity checks govern readiness.
    assert all(e['treatment']['entries']==1 for e in continued if e['treatment']['scheduled'] and e['valid_finance_handoff'])
    dump(a.output/'summary.json',summary)
    dump(a.output/'combined_index.json',{'label':summary['label'],'original_run_root':str(ORIGINAL_RUN),'continuation_run_root':str(a.continuation),
        'scientific_namespace':'E2_DEVELOPMENT_V3_D3','source_runs_modified':False,'cell001_rerun':False,'cells':provenance})
    preserve_original()
    print(json.dumps(summary))
if __name__=='__main__':main()
