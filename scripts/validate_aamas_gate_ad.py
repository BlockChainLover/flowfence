#!/usr/bin/env python3
"""Validate saved offline Gate A-D evidence and preservation; never generates models."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--benchmark', required=True, type=Path)
    parser.add_argument('--output', required=True, type=Path)
    args=parser.parse_args()
    root=Path(__file__).resolve().parents[1]
    def git(where,*a):
        return subprocess.check_output(['git','-C',str(where),*a])
    report=json.loads((args.output/'recovery/INTEGRATION_AUDIT.json').read_text())
    rows=json.loads((args.output/'recovery/CERTIFICATION.json').read_text())
    assert len(rows)==300 and len({(r['environment'],r['task_id']) for r in rows})==300
    assert all(r['eligibility']=='UNRESOLVED' and not r['development_candidate'] and not r['confirmatory_candidate'] for r in rows)
    assert len(report['scheduler_checks'])==300 and all(r['successful'] and r['model_contexts_equal'] for r in report['scheduler_checks'])
    assert len(report['coding_bypasses'])==200 and not any(r['raw_written_before_outer_return'] for r in report['coding_bypasses'])
    assert len(report['coding_clean_checks'])==200 and all(r['same_bytes'] and r['same_return'] for r in report['coding_clean_checks'])
    assert all(r['pass_'] for r in report['parity_pairs'])
    assert report['network_attempts']==report['formal_model_runs']==report['development_model_runs']==0
    frozen=json.loads((root/'artifacts/aamas2027/R3_FROZEN_INPUTS.json').read_text())
    existing_hash_checks={p:hashlib.sha256((root/p).read_bytes()).hexdigest()==h for p,h in frozen['files'].items()}
    assert all(existing_hash_checks.values())
    preserved=[]
    for path in git(root,'ls-tree','-r','-z','--name-only','0184b9ec801d2b22c62e988bf689c9a865d60157','artifacts/aamas2027','configs/experiment/aamas2027','papers','src/defenses','artifacts/aamas2027_gate_ac/E3_MOCK_TRAJECTORIES.json').decode().rstrip('\0').split('\0'):
        assert (root/path).read_bytes()==git(root,'show','0184b9ec801d2b22c62e988bf689c9a865d60157:'+path),path
        preserved.append(path)
    changed=git(args.benchmark,'diff','--name-only').decode().splitlines()
    assert sorted(changed)==['marble/evaluator/evaluator.py','marble/evaluator/evaluator_prompts.json']
    assert (args.benchmark/'marble/evaluator/evaluator.py').read_bytes()==git(args.benchmark,'show','40ddb54b5a379b53196d1bdf20e861dc6f922e19:marble/evaluator/evaluator.py')
    compiled=0
    for path in args.benchmark.rglob('*.py'):
        if '.git' not in path.parts:
            compile(path.read_bytes(),str(path),'exec');compiled+=1
    from src.experiments.aamas_gate_ac import synthetic_sidecar
    raw=[]
    for env in ('research','database','coding'):
        for line in (args.benchmark/f'multiagentbench/{env}/{env}_main.jsonl').read_text().splitlines():
            policy,_,_=synthetic_sidecar(json.loads(line),env);raw.append(policy.raw_value)
    scanned=0
    for path in args.output.rglob('*'):
        if path.is_file():
            text=path.read_text()
            assert not any(value in text for value in raw),path
            scanned+=1
    summary=dict(verdict='NOT_READY',records=300,eligible=0,unresolved=300,mock_scheduler_executions=600,
                 checked_clean_runtime_parity_pairs=300,coding_create_solution_protected_checks=200,coding_clean_equivalence_checks=200,
                 benchmark_python_files_compiled=compiled,benchmark_changes=changed,existing_frozen_hash_checks=existing_hash_checks,
                 historical_files_byte_preserved=len(preserved),safe_artifacts_scanned=scanned,R3_MUTATED='NO',
                 FORMAL_MODEL_RUNS_EXECUTED=0,DEVELOPMENT_MODEL_RUNS_EXECUTED=0,network_attempts=0,
                 complete_mediation='NOT_VERIFIED',full_capability_parity='NOT_VERIFIED',topology_redesign='UNRESOLVED')
    (args.output/'FINAL_VALIDATION.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps(summary))

if __name__=='__main__':main()
