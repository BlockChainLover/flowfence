#!/usr/bin/env python3
"""Execute the pushed 720-cell E2-A schedule once with unchanged V3 semantics."""
import argparse
import json
import os
import subprocess
from pathlib import Path
from src.e2_live.e2a import *
from src.e2_live.pilot import Evaluator, utc, sha, write_private
from src.e2_live.transport_v2 import LiveProviderV2
from scripts.run_e2_development_pilot import append


def main():
    p = argparse.ArgumentParser(description=__doc__)
    for name in ('source-root', 'provider-env', 'output', 'private-output'):
        p.add_argument('--'+name, type=Path, required=True)
    p.add_argument('--prereg-commit', required=True)
    a = p.parse_args()
    head = subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True).strip()
    assert head == a.prereg_commit
    assert subprocess.check_output(['git', 'branch', '--show-current'], text=True).strip() == BRANCH
    assert not subprocess.check_output(['git', 'diff', 'HEAD', '--name-only'])
    remote = subprocess.check_output(['git', 'ls-remote', '--heads', 'origin', BRANCH], text=True).split()[0]
    assert remote == head, 'PREREGISTRATION_NOT_PUSHED'
    checks = verify(a.source_root)
    # Git preserves all existing scientific files, including D3 observer and R3 evidence.
    for path in subprocess.check_output(['git', 'ls-tree', '-r', '--name-only', BASE], text=True).splitlines():
        if path.startswith(('src/', 'experiments/', 'artifacts/')):
            assert Path(path).read_bytes() == subprocess.check_output(['git', 'show', BASE+':'+path]), path
    tasks, policies, golds = inputs(a.source_root)
    schedule = load(SCHEDULE)
    assert schedule == make_schedule() and len(schedule) == 720
    assert not a.output.exists() and not a.private_output.exists(), 'NO_RERUN_OR_RESUME'
    a.output.mkdir(parents=True, mode=0o700)
    a.private_output.mkdir(parents=True, mode=0o700)
    os.chmod(a.private_output, 0o700)
    credentials = {}
    for line in a.provider_env.read_text().splitlines():
        if '=' in line and not line.lstrip().startswith('#'):
            key, value = line.split('=', 1)
            credentials[key.strip()] = value.strip().strip('\"\'')
    provider = LiveProviderV2(credentials['MINIMAX_API_KEY'])
    evaluator = Evaluator(a.source_root, golds)
    registration = dict(namespace=NAMESPACE, label=LABEL, started_utc=utc(), E2A_FORMAL_PREREG_COMMIT=head,
                        remote_prereg_commit=remote, schedule=schedule, integrity=checks,
                        private_root=str(a.private_output), retries=0, repairs=0, bird_episodes=0,
                        E2_B_STATUS='DEFERRED_NOT_SELECTED')
    (a.output/'registration.json').write_text(json.dumps(registration, indent=2)+'\n')
    completed = 0
    for cell in schedule:
        if (a.output/'STOP').exists(): break
        admit(cell)
        append(a.output/'attempts.jsonl', {**cell, 'started_utc': utc()})
        private = a.private_output/cell['cell_id']
        private.mkdir(mode=0o700)
        try:
            key = cell['family'], cell['task_id']
            result = FormalEpisode(cell, tasks[key], policies[key], {}, provider, evaluator, private).execute()
        except Exception as exc:
            result = {**cell, 'label': LABEL, 'termination': 'IMPLEMENTATION_DEFECT', 'valid': False,
                      'implementation_defect_type': type(exc).__name__, 'live_integrity_defects': ['RUNNER_SETUP_OR_AUDIT_EXCEPTION']}
            write_private(private/'setup_failure.json', result)
        append(a.output/'episodes.jsonl', result)
        completed += 1
        (a.output/'status.json').write_text(json.dumps(dict(completed=completed, latest_cell=cell['cell_id'], termination=result['termination']))+'\n')
        print(json.dumps(dict(cell=cell['order'], family=cell['family'], defense=cell['defense'], condition=cell['condition'], repetition=cell['repetition'], termination=result['termination'])), flush=True)
        if result.get('live_integrity_defects') or result['termination'] == 'IMPLEMENTATION_DEFECT':
            (a.output/'STOP').write_text('IMPLEMENTATION_DEFECT\n')
            break
    (a.output/'completion.json').write_text(json.dumps(dict(finished_utc=utc(), attempted=completed,
        unattempted_by_hard_stop=720-completed, all720attempted=completed==720, reruns=0,
        BIRD_FORMAL_EPISODES_EXECUTED=0, E2_B_STATUS='DEFERRED_NOT_SELECTED'), indent=2)+'\n')

if __name__ == '__main__': main()
