#!/usr/bin/env python3
"""Run the preregistered 40 clean + 240 contaminated recovery cells once, no retries."""
import argparse
import gzip
import json
import os
import subprocess
from pathlib import Path
from src.e2_live.qrecovery import BASE, PREREG, ROOT, schedule, RecoveryEpisode
from src.e2_live.e2a import inputs
from src.e2_live.d3 import verify
from src.e2_live.pilot import load, sha, utc, write_private, Evaluator
from src.e2_live.transport_v2 import LiveProviderV2
from scripts.run_e2_development_pilot import append


def preservation(source):
    checks = verify(source)
    # Every historical tracked file except the explicitly evolving progress/task records.
    paths = subprocess.check_output(['git','ls-tree','-r','--name-only',BASE], text=True).splitlines()
    protected = [p for p in paths if p.startswith(('src/','experiments/','configs/','artifacts/aamas2027_e2a','scripts/')) or p.startswith('E2A_')]
    changed = subprocess.check_output(['git','diff',BASE,'--name-only','--diff-filter=MD'],text=True).splitlines()
    assert not set(changed) & set(protected), 'HISTORICAL_TRACKED_FILE_CHANGED'
    index = json.loads(gzip.decompress(Path('artifacts/aamas2027_e2a_combined/derived/artifact_index.json.gz').read_bytes()))
    for item in index['private_files']:
        p = Path(item['path'])
        assert p.is_file() and sha(p.read_bytes()) == item['sha256'], 'HISTORICAL_PRIVATE_EVIDENCE_CHANGED'
    historical = json.loads(gzip.decompress(Path('artifacts/aamas2027_e2a_combined/derived/episode_summary.json.gz').read_bytes()))
    old_schedule = load('E2A_FORMAL_CELL_SCHEDULE.json')
    assert len(historical) == 720 and [e['cell_id'] for e in historical] == [c['cell_id'] for c in old_schedule]
    checks.update(historical_executions=720, historical_private_files_verified=len(index['private_files']),
                  protected_tracked_files=len(protected), existing_evidence_unchanged=True)
    return checks


def main():
    p = argparse.ArgumentParser(description=__doc__)
    for name in ('source-root','output','private-output'):
        p.add_argument('--'+name, type=Path, required=True)
    p.add_argument('--provider-env', type=Path)
    p.add_argument('--implementation-commit')
    p.add_argument('--preflight-only', action='store_true')
    a = p.parse_args()
    checks = preservation(a.source_root)
    tasks, policies, golds = inputs(a.source_root)
    cells = schedule()
    assert len(tasks) == 40
    assert load(ROOT/'unit_preflight.json')['status'] == 'PASS'
    checks.update(status='PASS', cells=280, clean=40, contaminated=240, task_count=40, live_calls=0)
    if a.preflight_only:
        a.output.mkdir(parents=True,exist_ok=True)
        (a.output/'preflight.json').write_text(json.dumps(checks,indent=2)+'\n')
        print(json.dumps(checks)); return
    head = subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()
    prereg = subprocess.check_output(['git','rev-parse',PREREG],text=True).strip()
    assert head == a.implementation_commit
    assert subprocess.check_output(['git','branch','--show-current'],text=True).strip() == 'codex/aamas2027-qrecovery'
    assert not subprocess.check_output(['git','diff','HEAD','--name-only'])
    subprocess.run(['git','merge-base','--is-ancestor',prereg,head],check=True)
    assert not a.output.exists() and not a.private_output.exists(), 'NO_RERUN_OR_RESUME'
    assert a.provider_env is not None
    for path in (a.output,a.private_output): path.mkdir(parents=True,mode=0o700)
    os.chmod(a.private_output,0o700)
    credentials = {}
    for line in a.provider_env.read_text().splitlines():
        if '=' in line and not line.lstrip().startswith('#'):
            key,value = line.split('=',1);credentials[key.strip()] = value.strip().strip('\"\'')
    provider = LiveProviderV2(credentials['MINIMAX_API_KEY'])
    evaluator = Evaluator(a.source_root,golds)
    registration = dict(namespace='QRECOVERY_FORMAL', started_utc=utc(), preregistration_commit=prereg,
        implementation_commit=head, base_evidence_commit=BASE, schedule=cells, private_root=str(a.private_output),
        source_root=str(a.source_root), retries=0, repairs=0, replacements=0, integrity=checks)
    (a.output/'registration.json').write_text(json.dumps(registration,indent=2)+'\n')
    (a.output/'preflight.json').write_text(json.dumps(checks,indent=2)+'\n')
    results = []
    for cell in cells:
        if (a.output/'STOP').exists(): break
        if cell['order'] == 41:
            assert len(results) == 40 and not any(r.get('live_integrity_defects') for r in results)
            (a.output/'clean_regression_check.json').write_text(json.dumps({'status':'PASS','attempted':40,
                'implementation_defects':0,'recovery_triggered':sum(r.get('recovery',{}).get('attempted',False) for r in results),
                'ordinary_failures_retained':sum(r['termination']!='SUCCESSFUL_FINAL' for r in results)},indent=2)+'\n')
        append(a.output/'attempts.jsonl',{**cell,'started_utc':utc()})
        private = a.private_output/cell['cell_id']; private.mkdir(mode=0o700)
        try:
            key = cell['family'],cell['task_id']
            result = RecoveryEpisode(cell,tasks[key],policies[key],{},provider,evaluator,private).execute()
        except Exception as exc:
            result = {**cell,'termination':'IMPLEMENTATION_DEFECT','valid':False,
                      'implementation_defect_type':type(exc).__name__,'live_integrity_defects':['SETUP_OR_AUDIT_EXCEPTION']}
            write_private(private/'setup_failure.json',result)
        append(a.output/'episodes.jsonl',result); results.append(result)
        status = {'finished':len(results),'latest_cell':cell['cell_id'],'termination':result['termination']}
        (a.output/'status.json').write_text(json.dumps(status)+'\n')
        print(json.dumps(status),flush=True)
        if result.get('live_integrity_defects') or result['termination']=='IMPLEMENTATION_DEFECT':
            (a.output/'STOP').write_text('IMPLEMENTATION_DEFECT\n')
            (a.output/'defect_report.json').write_text(json.dumps({'status':'HUMAN_REVIEW_REQUIRED','cell':cell,
                'defects':result.get('live_integrity_defects'),'rerun_or_fix_authorized':False},indent=2)+'\n')
            break
    (a.output/'completion.json').write_text(json.dumps({'finished_utc':utc(),'scheduled':280,'attempted':len(results),
        'finished':len(results),'unattempted':280-len(results),'implementation_defects':sum(r['termination']=='IMPLEMENTATION_DEFECT' for r in results),
        'retries':0,'reruns':0},indent=2)+'\n')
if __name__ == '__main__': main()
