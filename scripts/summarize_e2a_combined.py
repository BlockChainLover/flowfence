#!/usr/bin/env python3
"""Combine immutable E2-A prefix and continuation via temporary read-only evidence views."""
import argparse,json,subprocess,sys,tempfile
from pathlib import Path
from scripts.run_e2a_continuation import preserve_original,validate_registration,ORIGINAL_RUN,PREREG,rows,load,NAMESPACE


def dump(path,value):path.write_text(json.dumps(value,indent=2,ensure_ascii=False,allow_nan=False)+'\n')


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--continuation',type=Path,required=True);p.add_argument('--output',type=Path,required=True)
    a=p.parse_args();preserve_original()
    first_reg=load(ORIGINAL_RUN/'registration.json');reg=load(a.continuation/'registration.json');validate_registration(reg)
    first=rows(ORIGINAL_RUN/'episodes.jsonl');attempts=rows(ORIGINAL_RUN/'attempts.jsonl')
    continued=rows(a.continuation/'episodes.jsonl') if (a.continuation/'episodes.jsonl').exists() else []
    later_attempts=rows(a.continuation/'attempts.jsonl') if (a.continuation/'attempts.jsonl').exists() else []
    assert [e['cell_id'] for e in later_attempts]==[c['cell_id'] for c in reg['schedule'][:len(later_attempts)]]
    assert [e['cell_id'] for e in continued]==[e['cell_id'] for e in later_attempts[:len(continued)]]
    episodes=first+continued;attempts+=later_attempts
    assert len({e['cell_id'] for e in attempts})==len(attempts)
    roots={};provenance=[]
    for e in episodes:
        original=e['order']<=53;source_reg=first_reg if original else reg;source_run=ORIGINAL_RUN if original else a.continuation
        private=Path(source_reg['private_root'])/e['cell_id'];roots[e['cell_id']]=private
        provenance.append({'cell_id':e['cell_id'],'scientific_namespace':NAMESPACE,'run_instance_id':'E2A_FORMAL_ORIGINAL_001_053' if original else reg['run_instance_id'],'source_run':str(source_run),'source_episode_line':e['order'] if original else e['order']-53,'private_trajectory_path':str(private/'trajectory.json'),'original_immutable':original,'rerun':False,'termination':e['termination']})
    a.output.mkdir(parents=True,exist_ok=True);derived=a.output/'derived';derived.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory() as td:
        root=Path(td);run=root/'combined_input';run.mkdir();private=root/'private_links';private.mkdir()
        (run/'attempts.jsonl').write_text(''.join(json.dumps(e)+'\n' for e in attempts))
        (run/'episodes.jsonl').write_text(''.join(json.dumps(e)+'\n' for e in episodes))
        if (a.continuation/'completion.json').exists():dump(run/'completion.json',load(a.continuation/'completion.json'))
        for cell,path in roots.items():
            if path.exists():(private/cell).symlink_to(path,target_is_directory=True)
        subprocess.run([sys.executable,'scripts/summarize_e2a_formal.py','--run',str(run),'--private',str(private),'--output',str(derived)],check=True,stdout=subprocess.DEVNULL)
        index=load(derived/'artifact_index.json')
        for item in index['private_files']:
            cell=item['cell_id'];relative=Path(item['path']).relative_to(private/cell);item['path']=str(roots[cell]/relative)
        dump(derived/'artifact_index.json',index)
    summary=load(derived/'summary.json')
    summary.update(E2A_FORMAL_PREREG_COMMIT=PREREG,E2A_REPORTING_FIX_COMMIT=reg['E2A_REPORTING_FIX_COMMIT'],original_formal_cells_retained=53,original_formal_cells_rerun=0,continuation_expected=667,continuation_attempted=len(later_attempts),continuation_finished=len(continued),continuation_preflight=load(a.continuation/'preflight.json')['CONTINUATION_PREFLIGHT'],historical_reporting_defect={'count':1,'status':'HUMAN_APPROVED_REPORTING_ONLY_CORRECTION','affected_real_episodes':0},E2_B_STATUS='DEFERRED_NOT_SELECTED')
    dump(derived/'summary.json',summary)
    dump(a.output/'combined_index.json',{'label':summary['label'],'source_runs_modified':False,'original_run':str(ORIGINAL_RUN),'continuation_run':str(a.continuation),'scientific_namespace':NAMESPACE,'cells':provenance})
    dump(a.output/'combined_registration.json',{'E2A_FORMAL_PREREG_COMMIT':PREREG,'E2A_REPORTING_FIX_COMMIT':reg['E2A_REPORTING_FIX_COMMIT'],'source_registration_paths':[str(ORIGINAL_RUN/'registration.json'),str(a.continuation/'registration.json')],'derived_only':True})
    preserve_original()
    print(json.dumps(summary))

if __name__=='__main__':main()
