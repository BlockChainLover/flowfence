#!/usr/bin/env python3
"""Audit live E6-v2 pilot paths and private-input boundaries; emit booleans only."""
import argparse
import json
from pathlib import Path
from src.experiments.aamas_binding_v2 import check_pilot, load_config
from src.runtime.policy import default_secret_policies
from scripts.package_aamas2027 import validate_safe_artifacts


def audit(folder, private):
    config, _, _, _ = load_config(Path('configs/experiment/aamas2027/e6_v2_pilot.json'))
    try:
        gate = check_pilot(folder, config)
    except ValueError:
        gate = False
    rows = [json.loads(l) for f in private.glob('*.jsonl') for l in f.read_text().splitlines() if l]
    requests = [r for r in rows if r.get('stage') == 'request']
    cap = next(p.raw_value for p in default_secret_policies() if p.secret_id == 'secret_budget_cap')
    finance = [r for r in requests if r['prompt'].startswith('ROLE: finance_agent\n')]
    others = [r for r in requests if not r['prompt'].startswith('ROLE: finance_agent\n')]
    boundary = bool(finance) and all(cap in r['prompt'] for r in finance) and all(cap not in r['prompt'] for r in others)
    permissions = private.stat().st_mode & 0o777 == 0o700 and all(f.stat().st_mode & 0o777 == 0o600 for f in private.glob('*.jsonl'))
    validate_safe_artifacts([f for f in folder.glob('*') if f.is_file()], folder)
    calls = {r['call_id']: r for r in (json.loads(l) for l in (folder/'call_attempts.jsonl').read_text().splitlines())}
    result = {'pilot_gate_pass': gate and boundary and permissions, 'paths_and_responses_pass': gate,
              'finance_only_private_cap_context': boundary, 'private_file_permissions_pass': permissions,
              'private_request_records': len(requests), 'finance_context_records': len(finance),
              'safe_scan_pass': True, 'finish_reason_length': sum(c.get('finish_reason')=='length' for c in calls.values()),
              'raw_private_content_emitted': False}
    return result


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--input',type=Path,required=True);p.add_argument('--private-input',type=Path,required=True)
    p.add_argument('--output',type=Path,required=True)
    a=p.parse_args();result=audit(a.input,a.private_input)
    a.output.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))

if __name__=='__main__':main()
