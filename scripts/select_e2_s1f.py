#!/usr/bin/env python3
"""Apply the committed S1-F metadata-only rule; never invoke a model/runtime."""
import argparse
import collections
import csv
import gzip
import hashlib
import json
from pathlib import Path
import subprocess

CONFIG = Path('experiments/e2_source_s1f/selection_config.json')
TEMPLATES = Path('experiments/e2_source_s1f/policy_templates.json')
RULE_FILES = [CONFIG, TEMPLATES, Path('E2_SELECTION_RULE.md'),
              Path('E2_FACT_TYPE_AMENDMENT.md'), Path('scripts/select_e2_s1f.py')]


def require(condition, message):
    if not condition:
        raise ValueError(message)


def git(*args):
    return subprocess.check_output(['git', *args]).decode().strip()


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def save(path, value):
    path.write_text(json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + '\n')


def load_inputs(source_root, config):
    # Only pinned id/type parquet columns are decoded. Gold/SQL/questions are unused.
    import pyarrow.parquet as pq
    manifest = json.loads(Path(config['source_manifest']).read_text())
    for relative, expected in manifest['files'].items():
        require(digest(source_root / relative) == expected, 'Source changed: ' + relative)
    for directory, expected in manifest['code_pins'].items():
        actual = subprocess.check_output(['git', '-C', str(source_root / directory), 'rev-parse', 'HEAD']).decode().strip()
        require(actual == expected, 'Source code pin changed: ' + directory)
    with gzip.open(config['eligibility'], 'rt') as handle:
        records = [json.loads(line) for line in handle]
    eligible = {(r['family'], r['task_id']): r for r in records}
    require(len(eligible) == len(records) == 9573, 'Pool IDs/count changed')
    expected_types = {'bird_pg': ['P4'], 'tatqa': ['P1', 'P3'], 'hotpot': ['P2', 'P3']}
    for r in records:
        require(r['status'] == 'ELIGIBLE' and r['naturalness'] == 'NATURAL', 'Accepted admission changed')
        require(r['compatible_types'] == expected_types[r['family']], 'Retained compatibility changed')
    with gzip.open(config['clusters'], 'rt') as handle:
        clusters = list(csv.DictReader(handle))
    require(len(clusters) == len(eligible), 'Cluster count mismatch')
    meta = {(r['family'], r['task_id']): r for r in clusters}
    require(set(meta) == set(eligible), 'Cluster/admission ID mismatch')
    categories = {r['id']: r['type'] for r in pq.read_table(
        source_root / 'data/hotpot_distractor_validation.parquet', columns=['id', 'type']).to_pylist()}
    hot = {tid: json.loads(r['cluster']) for (family, tid), r in meta.items() if family == 'hotpot'}
    require(set(categories) == set(hot), 'Hotpot category IDs mismatch')
    parent = {tid: tid for tid in hot}

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    title_owner = {}
    title_counts = collections.Counter()
    for tid, titles in hot.items():
        for title in set(titles):
            title_counts[title] += 1
            if title in title_owner:
                a, b = find(tid), find(title_owner[title])
                parent[max(a, b)] = min(a, b)
            else:
                title_owner[title] = tid
    components = collections.defaultdict(list)
    for tid in hot:
        components[find(tid)].append(tid)
    components = {k: sorted(v) for k, v in components.items()}
    component_of = {tid: key for key, tids in components.items() for tid in tids}
    singleton_categories = collections.Counter(categories[v[0]] for v in components.values() if len(v) == 1)
    db_counts = collections.Counter(r['cluster'].split('|')[0] for r in clusters if r['family'] == 'bird_pg')
    contexts = {r['cluster'] for r in clusters if r['family'] == 'tatqa'}
    capacity = {
        'status': 'VERIFIED', 'uses_selected_IDs': False,
        'eligible_counts': dict(collections.Counter(r['family'] for r in records)),
        'compatible_types': expected_types, 'bird_database_capacities': dict(sorted(db_counts.items())),
        'tatqa_context_capacity': len(contexts),
        'hotpot_component_capacity': len(components),
        'hotpot_singleton_category_capacities': dict(singleton_categories),
        'hotpot_unique_titles': len(title_counts),
        'hotpot_shared_titles': sum(n > 1 for n in title_counts.values()),
        'hotpot_distinct_title_sets': len({tuple(sorted(set(t))) for t in hot.values()}),
        'hotpot_largest_component': max(map(len, components.values())),
        'required_confirmatory': config['confirm_types'], 'required_development': config['dev_types'],
        'proof': 'Every retained family type is compatible. Each of 11 BIRD databases has >=3 tasks, supporting 3 distinct-DB dev plus 20 confirm at max2/DB and all11 coverage. >=23 distinct TAT contexts support 3+20. >=12 bridge and >=11 comparison singleton Hotpot components suffice for the 12 bridge/11 comparison slots even without multi-record components.'
    }
    require(capacity['eligible_counts'] == {'bird_pg': 500, 'tatqa': 1668, 'hotpot': 7405}, 'Family pool sizes changed')
    require(len(db_counts) == 11 and min(db_counts.values()) >= 3, 'BIRD capacity FAILED')
    require(len(contexts) >= 23, 'TAT capacity FAILED')
    require(singleton_categories['bridge'] >= 12 and singleton_categories['comparison'] >= 11, 'Hotpot capacity FAILED')
    return eligible, meta, categories, hot, components, component_of, manifest, capacity


def select(config, meta, categories, components):
    selected = {split: {f: [] for f in config['families']} for split in ['development', 'confirmatory']}
    bird = collections.defaultdict(list)
    tat = collections.defaultdict(list)
    for (family, tid), row in sorted(meta.items()):
        if family == 'bird_pg':
            bird[row['cluster'].split('|')[0]].append(tid)
        elif family == 'tatqa':
            tat[row['cluster']].append(tid)
    used = set()
    for db in sorted(bird)[:3]:
        tid = bird[db][0]
        selected['development']['bird_pg'].append(tid)
        used.add(tid)
    for _ in range(config['bird_max_confirm_per_db']):
        for db in sorted(bird):
            if len(selected['confirmatory']['bird_pg']) == 20:
                break
            tid = next(t for t in bird[db] if t not in used)
            used.add(tid)
            selected['confirmatory']['bird_pg'].append(tid)
    tat_ids = [tat[context][0] for context in sorted(tat)[:23]]
    selected['development']['tatqa'] = tat_ids[:3]
    selected['confirmatory']['tatqa'] = tat_ids[3:]
    used_components = set()
    for split, slots in [('development', config['hotpot_dev_categories']), ('confirmatory', config['hotpot_confirm_categories'])]:
        for category in slots:
            for component, tids in sorted(components.items()):
                if component in used_components:
                    continue
                candidates = [t for t in tids if categories[t] == category]
                if candidates:
                    selected[split]['hotpot'].append(candidates[0])
                    used_components.add(component)
                    break
            else:
                raise ValueError('Hotpot selection FAILED, no relaxation allowed')
    return selected


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source-root', type=Path, required=True)
    parser.add_argument('--rule-commit', required=True, help='Commit containing rule/config/script before any selection')
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    rule_commit = git('rev-parse', args.rule_commit + '^{commit}')
    git('merge-base', '--is-ancestor', rule_commit, 'HEAD')
    for file in RULE_FILES:
        relative = file.as_posix()
        committed = subprocess.check_output(['git', 'show', rule_commit + ':' + relative])
        require(committed == file.read_bytes(), 'Rule differs from preselection commit: ' + relative)
    config = json.loads(CONFIG.read_text())
    templates = json.loads(TEMPLATES.read_text())
    # Accepted inputs and certification/defense sources are immutable from S1-R.
    for file in [config['eligibility'], config['clusters'], config['source_manifest'], 'src/defenses/mas_flowfence.py']:
        require(subprocess.check_output(['git', 'show', config['accepted_parent'] + ':' + file]) == Path(file).read_bytes(), 'Accepted input changed: ' + file)
    require(digest('src/defenses/mas_flowfence.py') == config['recognizer_sha256'], 'Recognizer changed')
    eligible, meta, categories, hot, components, component_of, manifest, capacity = load_inputs(args.source_root, config)
    selected = select(config, meta, categories, components)
    rows = {'development': [], 'confirmatory': []}
    source_pins = {
        'bird_pg': {'code': manifest['code_pins']['bird_mini'], 'data': manifest['data_pins']['bird']},
        'tatqa': {'code': manifest['code_pins']['tatqa'], 'data': manifest['code_pins']['tatqa']},
        'hotpot': {'code': manifest['code_pins']['hotpot'], 'data': manifest['data_pins']['hotpot']}}
    for split in rows:
        for family in config['families']:
            types = config['dev_types'][family] if split == 'development' else [p for p, count in config['confirm_types'][family].items() for _ in range(count)]
            require(len(types) == len(selected[split][family]), 'Selection count mismatch')
            for position, (tid, fact_type) in enumerate(zip(selected[split][family], types), 1):
                entry, annotation = meta[(family, tid)], eligible[(family, tid)]
                require(fact_type in annotation['compatible_types'], 'Incompatible assignment')
                require(entry['authorized_principal'] == 'finance_agent' and entry['forbidden'] == 'doc_writer_agent;final_output' and entry['contamination_surface'] == 'internal_message', 'Policy annotation changed')
                rows[split].append({
                    'split': split, 'family': family, 'task_id': tid, 'selection_position_in_family': position,
                    'context_cluster_id': entry['cluster'], 'fact_type': fact_type,
                    'authorized_principal': entry['authorized_principal'],
                    'forbidden_principals': ['doc_writer_agent'], 'forbidden_surfaces': ['final_output'],
                    'contamination_surface': entry['contamination_surface'], 'source_pin': source_pins[family],
                    'evaluator_identifier': config['evaluator_ids'][family],
                    'naturalness': annotation['naturalness'], 'eligibility': annotation['status'],
                    'compatible_types': annotation['compatible_types'],
                    'source_category': categories[tid] if family == 'hotpot' else entry['cluster'].split('|')[-1] if family == 'bird_pg' else None,
                    'overlap_component_id': component_of[tid] if family == 'hotpot' else None,
                    'overlap_component_size': len(components[component_of[tid]]) if family == 'hotpot' else None})
    all_rows = rows['development'] + rows['confirmatory']
    require(len(all_rows) == 69 and len({(r['family'], r['task_id']) for r in all_rows}) == 69, 'Duplicate IDs')
    require(len({r['task_id'] for r in all_rows}) == 69, 'Unqualified source ID collision')
    require(len({r['context_cluster_id'] for r in all_rows if r['family'] == 'tatqa'}) == 23, 'TAT context overlap')
    hot_rows = [r for r in all_rows if r['family'] == 'hotpot']
    require(len({r['overlap_component_id'] for r in hot_rows}) == 23, 'Hotpot component overlap')
    titles = [title for r in hot_rows for title in set(hot[r['task_id']])]
    require(len(titles) == len(set(titles)), 'Hotpot title overlap')
    bird_counts = collections.Counter(r['context_cluster_id'].split('|')[0] for r in rows['confirmatory'] if r['family'] == 'bird_pg')
    require(len(bird_counts) == config['bird_confirm_db_coverage'] and max(bird_counts.values()) <= config['bird_max_confirm_per_db'], 'BIRD concentration')
    type_counts = dict(collections.Counter(r['fact_type'] for r in rows['confirmatory']))
    require(type_counts == {'P1': 15, 'P2': 15, 'P3': 10, 'P4': 20}, 'Confirmatory quota failed')
    hot_categories = dict(collections.Counter(r['source_category'] for r in rows['confirmatory'] if r['family'] == 'hotpot'))
    require(hot_categories == {'bridge': 10, 'comparison': 10}, 'Hotpot category balance failed')
    policies = []
    for ordinal, row in enumerate(sorted(all_rows, key=lambda r: (r['family'], r['task_id'])), 1):
        fact_template = templates['fact_templates'][row['fact_type']]
        require(row['family'] in fact_template['families'], 'Invalid policy family')
        policy = {k: v for k, v in templates.items() if k not in ['fact_templates', 'ordinal_rule', 'secret_id_rule', 'limitations']}
        policy.update({'family': row['family'], 'task_id': row['task_id'], 'split': row['split'],
                       'fact_type': row['fact_type'], 'fact_generation_template': fact_template,
                       'generation_ordinal': ordinal, 'secret_id': f"e2_private_{row['family']}_{row['task_id']}_{row['fact_type']}"})
        policies.append(policy)
    bird_dev = {r['context_cluster_id'].split('|')[0] for r in rows['development'] if r['family'] == 'bird_pg'}
    certificate = {
        'FACT_BALANCE_FEASIBILITY': 'VERIFIED', 'DEV_CONFIRM_DISJOINT': 'YES',
        'capacity_proof': capacity, 'constructive_witness': ['development.json', 'confirmatory.json'],
        'dev_counts': dict(collections.Counter(r['family'] for r in rows['development'])),
        'confirm_counts': dict(collections.Counter(r['family'] for r in rows['confirmatory'])),
        'confirm_fact_counts': type_counts, 'bird_confirm_db_counts': dict(bird_counts),
        'bird_permitted_shared_split_databases': sorted(bird_dev & set(bird_counts)),
        'tatqa_selected_contexts': 23, 'tatqa_shared_contexts': 0,
        'hotpot_selected_components': 23, 'hotpot_shared_titles': 0,
        'hotpot_confirm_categories': hot_categories,
        'hotpot_selected_component_sizes': [r['overlap_component_size'] for r in hot_rows],
        'all_selected_eligible_natural_compatible': True, 'development_never_promoted': True,
        'policy_skeleton_count': len(policies), 'raw_values_instantiated': False,
        'formal_model_runs': 0, 'development_model_runs': 0,
        'statistical_independence_claimed': False}
    provenance = {'rule_commit': rule_commit, 'accepted_parent': config['accepted_parent'],
                  'selection_inputs': {p: digest(p) for p in [str(CONFIG), str(TEMPLATES), config['eligibility'], config['clusters'], config['source_manifest']]},
                  'source_pins': source_pins, 'recognizer_sha256': config['recognizer_sha256'],
                  'forbidden_selection_inputs_used': False, 'raw_values_instantiated': False}
    args.output.mkdir(parents=True, exist_ok=True)
    for name, value in [('development', rows['development']), ('confirmatory', rows['confirmatory']),
                        ('policy_skeletons', policies), ('allocation_certificate', certificate), ('selection_provenance', provenance)]:
        save(args.output / (name + '.json'), value)
    print(json.dumps({'FACT_BALANCE_FEASIBILITY': 'VERIFIED', 'development': 9, 'confirmatory': 60,
                      'DEV_CONFIRM_DISJOINT': 'YES', 'confirm_fact_counts': type_counts, 'rule_commit': rule_commit}))


if __name__ == '__main__':
    main()
