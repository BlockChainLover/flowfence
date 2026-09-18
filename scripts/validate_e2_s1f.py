#!/usr/bin/env python3
"""Independently check frozen S1-F assignments, policy bindings and replay bytes."""
import argparse
from collections import Counter, defaultdict
import csv
import gzip
import hashlib
import json
from pathlib import Path
import subprocess


def check(value, message):
    if not value:
        raise ValueError(message)


def read(path):
    return json.loads(Path(path).read_text())


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--artifacts', type=Path, default=Path('artifacts/aamas2027_e2_source_s1f'))
    parser.add_argument('--replay-dir', type=Path, required=True)
    parser.add_argument('--verify-manifest', action='store_true')
    args = parser.parse_args()
    root = args.artifacts
    config = read('experiments/e2_source_s1f/selection_config.json')
    templates = read('experiments/e2_source_s1f/policy_templates.json')
    dev, confirm, policies = [read(root / (n + '.json')) for n in ['development', 'confirmatory', 'policy_skeletons']]
    provenance = read(root / 'selection_provenance.json')
    certificate = read(root / 'allocation_certificate.json')
    pre = read(root / 'preselection_capacity.json')
    rows = dev + confirm
    check(len(dev) == 9 and len(confirm) == 60 and len(policies) == 69, 'Wrong total')
    check(len({r['task_id'] for r in rows}) == 69, 'Repeated source ID')
    check(Counter(r['family'] for r in dev) == dict.fromkeys(config['families'], 3), 'Dev family counts')
    check(Counter(r['family'] for r in confirm) == dict.fromkeys(config['families'], 20), 'Confirm family counts')
    for family in config['families']:
        check(Counter(r['fact_type'] for r in confirm if r['family'] == family) == config['confirm_types'][family], 'Family/type quota')
    with gzip.open(config['eligibility'], 'rt') as handle:
        admitted = {(r['family'], r['task_id']): r for r in map(json.loads, handle)}
    with gzip.open(config['clusters'], 'rt') as handle:
        metadata = {(r['family'], r['task_id']): r for r in csv.DictReader(handle)}
    for row in rows:
        key = row['family'], row['task_id']
        original = admitted[key]
        check(original['status'] == row['eligibility'] == 'ELIGIBLE', 'Eligibility')
        check(original['naturalness'] == row['naturalness'] == 'NATURAL', 'Naturalness')
        check(row['compatible_types'] == original['compatible_types'] and row['fact_type'] in original['compatible_types'], 'Compatible type')
        check(row['context_cluster_id'] == metadata[key]['cluster'], 'Original cluster')
        check(row['authorized_principal'] == metadata[key]['authorized_principal'], 'Principal')
        check(row['forbidden_principals'] + row['forbidden_surfaces'] == metadata[key]['forbidden'].split(';'), 'Forbidden annotations')
        check(row['contamination_surface'] == metadata[key]['contamination_surface'], 'Surface')
        check(row['source_pin'] == provenance['source_pins'][row['family']], 'Source pin')
        check(row['evaluator_identifier'] == config['evaluator_ids'][row['family']], 'Evaluator')
    bird_confirm = Counter(r['context_cluster_id'].split('|')[0] for r in confirm if r['family'] == 'bird_pg')
    check(len(bird_confirm) == 11 and max(bird_confirm.values()) == 2, 'BIRD database balance')
    check(len({r['context_cluster_id'].split('|')[0] for r in dev if r['family'] == 'bird_pg'}) == 3, 'BIRD dev database diversity')
    check(len({r['context_cluster_id'] for r in rows if r['family'] == 'tatqa'}) == 23, 'TAT split context leakage')
    hot_rows = [r for r in rows if r['family'] == 'hotpot']
    title_list = [t for r in hot_rows for t in set(json.loads(r['context_cluster_id']))]
    check(len(title_list) == len(set(title_list)), 'Hotpot title leakage')
    # Independent graph traversal, not selector union-find or certificate assertions.
    titles_by_id = {tid: set(json.loads(r['cluster'])) for (f, tid), r in metadata.items() if f == 'hotpot'}
    tasks_by_title = defaultdict(set)
    for tid, titles in titles_by_id.items():
        for title in titles:
            tasks_by_title[title].add(tid)
    component_by_id = {}
    component_sizes = {}
    for start in sorted(titles_by_id):
        if start in component_by_id:
            continue
        pending, members, visited_titles = [start], {start}, set()
        while pending:
            current = pending.pop()
            for title in titles_by_id[current] - visited_titles:
                visited_titles.add(title)
                for other in tasks_by_title[title] - members:
                    members.add(other)
                    pending.append(other)
        key = min(members)
        component_sizes[key] = len(members)
        for member in members:
            component_by_id[member] = key
    check(len({component_by_id[r['task_id']] for r in hot_rows}) == 23, 'Hotpot component leakage')
    for row in hot_rows:
        key = component_by_id[row['task_id']]
        check(row['overlap_component_id'] == key and row['overlap_component_size'] == component_sizes[key], 'Component metadata')
    check(Counter(r['source_category'] for r in confirm if r['family'] == 'hotpot') == {'bridge': 10, 'comparison': 10}, 'Hotpot categories')
    check(len({p['secret_id'] for p in policies}) == 69, 'Policy ID uniqueness')
    by_key = {(p['family'], p['task_id']): p for p in policies}
    check(len(by_key) == 69, 'Policy task uniqueness')
    for ordinal, row in enumerate(sorted(rows, key=lambda r: (r['family'], r['task_id'])), 1):
        policy = by_key[(row['family'], row['task_id'])]
        check(policy['split'] == row['split'] and policy['fact_type'] == row['fact_type'], 'Policy assignment')
        check(policy['generation_ordinal'] == ordinal and 'raw_value' not in policy and policy['raw_value_instantiated'] is False, 'Future generation rule')
        check(policy['fact_generation_template'] == templates['fact_templates'][row['fact_type']], 'Fact template')
        check(policy['secret_id'] == f"e2_private_{row['family']}_{row['task_id']}_{row['fact_type']}", 'Secret identifier rule')
        for key in ['authorized_principals', 'forbidden_principals', 'forbidden_surfaces', 'allowed_abstraction', 'AB_templates', 'expected_frozen_recognizer_match', 'privacy_observation_surfaces', 'contamination_surface']:
            check(policy[key] == templates[key], 'Policy template field: ' + key)
    for key, digest in provenance['selection_inputs'].items():
        check(hashlib.sha256(Path(key).read_bytes()).hexdigest() == digest, 'Input digest: ' + key)
    check(pre['hotpot_singleton_category_counts'] == certificate['capacity_proof']['hotpot_singleton_category_capacities'], 'Preselection capacity')
    check(pre['eligible_counts'] == certificate['capacity_proof']['eligible_counts'], 'Preselection pool counts')
    check(certificate['dev_counts'] == Counter(r['family'] for r in dev), 'Certificate dev counts')
    check(certificate['confirm_counts'] == Counter(r['family'] for r in confirm), 'Certificate confirm counts')
    check(certificate['confirm_fact_counts'] == Counter(r['fact_type'] for r in confirm), 'Certificate fact counts')
    check(certificate['FACT_BALANCE_FEASIBILITY'] == 'VERIFIED' and certificate['DEV_CONFIRM_DISJOINT'] == 'YES', 'Certificate verdict')
    replay_files = ['development.json', 'confirmatory.json', 'policy_skeletons.json', 'allocation_certificate.json', 'selection_provenance.json']
    for name in replay_files:
        check((root / name).read_bytes() == (args.replay_dir / name).read_bytes(), 'Replay differs: ' + name)
    rule_files = ['scripts/select_e2_s1f.py', 'E2_SELECTION_RULE.md', 'E2_FACT_TYPE_AMENDMENT.md', 'experiments/e2_source_s1f/selection_config.json', 'experiments/e2_source_s1f/policy_templates.json']
    for name in rule_files:
        check(Path(name).read_bytes() == subprocess.check_output(['git', 'show', provenance['rule_commit'] + ':' + name]), 'Rule altered after commit')
    historical = ['src', 'configs', 'artifacts/aamas2027_e2_source_s1', 'artifacts/aamas2027_e2_source_s1r', 'experiments/e2_source_s1', 'E2_TASK_CLUSTERING_SPEC.md', 'E2_TASK_ELIGIBILITY_SPEC.md']
    unchanged = subprocess.check_output(['git', 'diff', '--name-only', config['accepted_parent'], '--', *historical]).decode().strip()
    check(not unchanged, 'Accepted implementation or annotations changed: ' + unchanged)
    recognizer = hashlib.sha256(Path('src/defenses/mas_flowfence.py').read_bytes()).hexdigest()
    check(recognizer == config['recognizer_sha256'], 'Recognizer hash')
    if args.verify_manifest:
        entries = read(root / 'frozen_manifest.json')['files']
        for name, expected in entries.items():
            check(hashlib.sha256(Path(name).read_bytes()).hexdigest() == expected, 'Manifest mismatch: ' + name)
    report = {
        'status': 'PASS', 'development': 9, 'confirmatory': 60, 'policy_skeletons': 69,
        'DEV_CONFIRM_DISJOINT': 'YES', 'confirm_fact_counts': dict(Counter(r['fact_type'] for r in confirm)),
        'replay_files_byte_identical': replay_files, 'independent_component_graph_verified': True,
        'rule_files_match_preselection_commit': provenance['rule_commit'],
        'accepted_runtime_sources_configs_annotations_unchanged': True,
        'frozen_recognizer_sha256': recognizer, 'R3_mutated': False,
        'formal_model_runs': 0, 'development_model_runs': 0,
        'raw_fact_values_instantiated': False,
        'verification_scope': 'Metadata, fixed assignments and artifact integrity only; not a pilot or new runtime certification.'}
    # Stable report permits the same command to verify the manifest on later replay.
    report_path = root / 'validation.json'
    report_bytes = (json.dumps(report, indent=2, sort_keys=True) + '\n').encode()
    if args.verify_manifest:
        check(report_path.read_bytes() == report_bytes, 'Recorded validation differs')
    else:
        report_path.write_bytes(report_bytes)
    print(json.dumps(report, sort_keys=True))


if __name__ == '__main__':
    main()
