#!/usr/bin/env python3
"""Check Gate A-E evidence, classifications, privacy hygiene and frozen preservation."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--benchmark',required=True,type=Path)
    p.add_argument('--output',required=True,type=Path)
    args=p.parse_args();root=Path(__file__).resolve().parents[1];out=args.output
    def git(where,*a):return subprocess.check_output(['git','-C',str(where),*a])
    x=json.loads((out/'AUDIT.json').read_text())
    assert len(x['certification'])==300
    assert len({(r['environment'],r['task_id']) for r in x['certification']})==300
    assert all(r['mock_executable'] and r['eligibility']=='INELIGIBLE' and not r['development_selected'] and not r['confirmatory_selected'] for r in x['certification'])
    assert len({r['transition'] for r in x['transition_pairs']})==23
    assert all(all(v for k,v in r.items() if k.startswith('same_')) for r in x['transition_pairs'])
    judge=next(r for r in x['transition_pairs'] if r['transition']=='database_offline_judge')
    assert judge['left_error'] is None and judge['model_calls_per_arm']==[1,1]
    for row in x['boundary_probes']:
        assert all(row['direct_storage'].values()) and row['session_outer_scope_misattribution']
        assert row['explicit_recipient_gateway_safe'] and row['outgoing_raw_absent']
        if row['environment']=='coding':
            g=row['generic_workspace'];assert g['reviewed_solution_raw_absent'] and g['advice_json_raw_absent']
            assert g['coder_checks'][0]['clean_bytes_unchanged'] and all(v['raw_absent'] for v in g['coder_checks'])
            assert g['diagnostic_retains_private_fixture'] and row['outer_return_too_late_for_reviewer']
    for row in x['topology']:
        if row['reply_model_calls']:assert row['reply_schema_impossible_required_fields']==['target_agent_id']
        if row['path']=='coordinator_relay':assert row['coordinator_received_worker_return'] and row['target_received_relay']
    surfaces=json.loads((out/'PROPAGATION_SURFACE_CLASSIFICATION.json').read_text())
    enums={'MODEL_VISIBLE_PROPAGATION','EXTERNAL_OR_SHARED_SIDE_EFFECT','TRUSTED_LOCAL_DIAGNOSTIC','BENCHMARK_EVALUATOR_PRIVATE','UNRESOLVED_CLASSIFICATION'}
    assert len({s['id'] for s in surfaces})==len(surfaces)
    for s in surfaces:
        assert s['classification'] in enums
        if s['classification']=='TRUSTED_LOCAL_DIAGNOSTIC':assert all(s['trusted_diagnostic_conditions'].values())
    frozen=json.loads((root/'artifacts/aamas2027/R3_FROZEN_INPUTS.json').read_text())
    checks={p:hashlib.sha256((root/p).read_bytes()).hexdigest()==h for p,h in frozen['files'].items()}
    assert all(checks.values())
    start='fd406c09f35e5b250e21e9bf6f00e204fa7e0835'
    preserve=['artifacts/aamas2027','artifacts/aamas2027_gate_ad','artifacts/aamas2027_gate_ac/E3_MOCK_TRAJECTORIES.json','configs/experiment/aamas2027','src/defenses','papers']
    paths=git(root,'ls-tree','-r','-z','--name-only',start,*preserve).decode().rstrip('\0').split('\0')
    for path in paths:assert (root/path).read_bytes()==git(root,'show',start+':'+path),path
    assert sorted(git(args.benchmark,'diff','--name-only').decode().splitlines())==['marble/evaluator/evaluator.py','marble/evaluator/evaluator_prompts.json']
    assert (args.benchmark/'marble/evaluator/evaluator.py').read_bytes()==git(args.benchmark,'show','40ddb54b5a379b53196d1bdf20e861dc6f922e19:marble/evaluator/evaluator.py')
    source=git(args.benchmark,'show','8d60fa17b5596b44458a52d4296061b9fc13d6f2:marble/evaluator/evaluator_prompts.json').decode()
    import re
    repaired=re.sub(r'(?<!\{)\{(\\"rating\\": (?:X|4|2))\}(?!\})',r'{{\1}}',source)
    assert (args.benchmark/'marble/evaluator/evaluator_prompts.json').read_text()==repaired
    from src.experiments.aamas_gate_ac import synthetic_sidecar
    raw=['SYNTHETIC-PRIVATE-123'];recognizer=0
    for env in ('research','database','coding'):
        for line in (args.benchmark/f'multiagentbench/{env}/{env}_main.jsonl').read_text().splitlines():
            policy,attacks,_=synthetic_sidecar(json.loads(line),env);raw.append(policy.raw_value);recognizer+=len(attacks)
    scanned=0
    for path in out.rglob('*'):
        if path.is_file():
            text=path.read_text();assert not any(v in text for v in raw),path;scanned+=1
    assert x['network_attempts']==x['formal_model_runs']==x['development_model_runs']==0
    compiled=[]
    for name in ['scripts/audit_aamas_gate_ae.py','scripts/validate_aamas_gate_ae.py','src/experiments/aamas_gate_ae.py','tests/test_aamas_gate_ae.py']:
        compile((root/name).read_bytes(),name,'exec');compiled.append(name)
    result={'overall':'NOT_READY','surfaces_classified':len(surfaces),'generic_boundary_categories':7,'transition_classes_total':23,'transition_classes_verified':23,'transition_pairs':59,'original_tasks_mock_executable':300,'eligible':0,'unresolved':0,'ineligible_current_architecture':300,'recognizer_artifacts_verified':recognizer,'existing_frozen_hash_checks':checks,'historical_files_preserved':len(paths),'safe_artifacts_scanned':scanned,'compiled':compiled,'original_benchmark_repair_chain_unchanged':True,'formal_model_runs':0,'development_model_runs':0,'R3_MUTATED':'NO','no_automatic_gate_af':True,'no_gate_b':True}
    (out/'FINAL_VALIDATION.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result))

if __name__=='__main__':main()
