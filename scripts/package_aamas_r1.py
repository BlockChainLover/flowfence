#!/usr/bin/env python3
"""Package R1 safe evidence plus existing allowlisted replay dependencies."""
import argparse
import json
import zipfile
from pathlib import Path
from scripts.package_aamas2027 import bundle_files,validate_safe_artifacts


def package(repo,output):
    root=repo/'artifacts/aamas2027'
    files=set(bundle_files(repo,root))
    sources=['src/experiments/aamas_metrics.py','src/experiments/aamas_binding_semantic.py','scripts/recompute_aamas_metrics.py','scripts/run_aamas_binding_semantic.py','scripts/summarize_aamas_binding_semantic.py','scripts/integrate_aamas_r1.py','scripts/package_aamas_r1.py','tests/test_aamas_binding_semantic.py','artifacts/codex_task_state/codex_aamas2027_r1.md']
    files.update(repo/s for s in sources)
    files.update((repo/'configs/experiment/aamas2027').glob('e6_*.json'))
    files.update(p for p in root.glob('R1_*') if p.is_file() and p.name!='R1_BUNDLE_MANIFEST.json')
    for d in ('R1_corrected_metrics','R1_validation'):
        files.update(p for p in (root/d).glob('*') if p.is_file() and p.suffix in ('.json','.jsonl','.md','.txt'))
    e6=root/'E6_binding_semantic';files.add(e6/'README.md')
    runs={'episodes.jsonl','events.jsonl','call_attempts.jsonl','generated_attempts.jsonl','registration.json','completion.json'}
    for phase in ('pilot','formal'):
        files.update(p for p in (e6/phase).glob('*') if p.name in runs)
    for phase in ('dry_run',):
        files.update(p for p in (e6/phase).glob('*') if p.name in ('registration.json','completion.json'))
    files.update(p for p in (e6/'derived').glob('*') if p.name in ('summary.json','groups.csv','paired.csv','failures.safe.json','REPORT.md'))
    status=root/'E5_topology_ablation/R1_status.json'
    if status.exists():files.add(status)
    files=sorted(files)
    if any(not p.is_file() or p.is_symlink() or not p.resolve().is_relative_to(repo.resolve()) for p in files):
        raise ValueError('Package member absent or outside repository')
    validate_safe_artifacts(files,root)
    inventory={'experiment_source_sha':'a34dc1bd7e135c2f6b0f903b59604b19bbff6b46','scope':'Safe E0–E6 records and executable replay dependencies; private full traces excluded; old E0–E4 formal records unmodified. Public synthetic fixtures are in executable source, never raw result text. Dry-run metadata is diagnostic precommit wiring, not formal evidence.','files':[{'path':str(p.relative_to(repo)),'bytes':p.stat().st_size} for p in files]}
    manifest=root/'R1_BUNDLE_MANIFEST.json';manifest.write_text(json.dumps(inventory,indent=2)+'\n');files.append(manifest)
    output.parent.mkdir(parents=True,exist_ok=True)
    with zipfile.ZipFile(output,'w',compression=zipfile.ZIP_DEFLATED) as z:
        for p in files:z.write(p,str(p.relative_to(repo)))
    with zipfile.ZipFile(output) as z:assert z.testzip() is None
    return {'files':len(files),'zip_bytes':output.stat().st_size,'output':str(output)}


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output',type=Path,default=Path('aamas2027_r1_experiment_bundle_20260912.zip'))
    a=p.parse_args();print(json.dumps(package(Path.cwd(),a.output)))
if __name__=='__main__':main()
