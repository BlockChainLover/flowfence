#!/usr/bin/env python3
"""Recompute descriptive E2-A manuscript tables from saved public episode summaries.

This stdlib-only reader makes no model or evaluator calls and never writes the source.
The supplementary observed-secure-success count is post hoc and is not a semantic
privacy adjudication: it requires saved task_success=True and saved privacy=False.
"""
import argparse
import csv
import gzip
import json
from collections import Counter
from pathlib import Path


def aggregate(rows):
    metrics = [r['source_metrics'] for r in rows if r['source_metrics'] is not None]
    families = {r['family'] for r in rows}
    metric = {'tatqa': 'em', 'hotpot': 'joint_em'}[next(iter(families))] if len(families) == 1 else None
    return {
        'attempted': len(rows),
        'completed_final': sum(r['completed_final'] is True for r in rows),
        'scored': len(metrics),
        'task_success': sum(r['task_success'] is True for r in rows),
        'task_failure': sum(r['task_success'] is False for r in rows),
        'task_unknown': sum(r['task_success'] is None for r in rows),
        'policy_rejection': sum(r['termination'] == 'POLICY_REJECTION' for r in rows),
        'privacy_true': sum(r['privacy'] is True for r in rows),
        'privacy_false': sum(r['privacy'] is False for r in rows),
        'privacy_unknown': sum(r['privacy'] is None for r in rows),
        'observed_secure_success_posthoc': sum(r['task_success'] is True and r['privacy'] is False for r in rows),
        'task_success_with_privacy_unknown': sum(r['task_success'] is True and r['privacy'] is None for r in rows),
        'source_metric': metric,
        'mean_source_metric_over_scored': sum(m[metric] for m in metrics) / len(metrics) if metric and metrics else None,
        'termination_counts': dict(sorted(Counter(r['termination'] for r in rows).items())),
    }


def latex(rows):
    lines = [r'% Generated from public saved episode summaries; no evaluator rerun.',
        r'\begin{tabular}{lllrrrrrr}', r'\toprule',
        r'Family & Cond. & Defense & Final & Scored & Success & Quar. & Unknown & Mean \\',
        r'\midrule']
    for r in rows:
        family = {'tatqa': 'TAT-QA', 'hotpot': 'HotpotQA'}[r['family']]
        condition = {'CLEAN': 'Clean', 'CONTAMINATION_A': 'A', 'CONTAMINATION_B': 'B'}[r['condition']]
        defense = {'EXACT_IFC': 'IFC', 'FLOWFENCE_R2': 'R2'}[r['defense']]
        mean = r['mean_source_metric_over_scored']
        mean_text = '--' if mean is None else f'{100*mean:.1f}'
        lines.append(f"{family} & {condition} & {defense} & {r['completed_final']} & {r['scored']} & {r['task_success']} & {r['policy_rejection']} & {r['privacy_unknown']} & {mean_text} " + r'\\')
    lines.extend([r'\bottomrule', r'\end{tabular}',
        r'% Each row has 60 attempted cells: 20 tasks x 3 repeats. These are not independent task samples.',
        r'% Mean is source EM (TAT-QA) or joint EM (HotpotQA), percent, over scored finals only; -- means no scored final.',
        r'% Success is a count over all 60 attempts; quarantine is terminal and produces no scored final.',
        r'% In these saved observations every task success also has automated privacy FALSE, so the post-hoc observed-secure-success count equals Success.',
        r'% FALSE means complete observation without the frozen raw-publication violation; UNKNOWN is retained separately, not safety or semantic correctness.'])
    return '\n'.join(lines) + '\n'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--episodes', type=Path, required=True, help='Saved public episode_summary.json or .json.gz')
    parser.add_argument('--output', type=Path, default=Path('artifacts/aamas2027_paper_revision'), help='Directory for newly derived public outputs')
    args = parser.parse_args()
    opener = gzip.open if args.episodes.suffix == '.gz' else open
    with opener(args.episodes, 'rt', encoding='utf-8') as f:
        episodes = json.load(f)
    assert len({r['cell_id'] for r in episodes}) == len(episodes) == 720
    assert all(r['namespace'] == 'E2A_FORMAL_CONFIRMATORY' for r in episodes)
    groups = []
    for family in ('tatqa', 'hotpot'):
        for condition in ('CLEAN', 'CONTAMINATION_A', 'CONTAMINATION_B'):
            for defense in ('EXACT_IFC', 'FLOWFENCE_R2'):
                selected = [r for r in episodes if (r['family'], r['condition'], r['defense']) == (family, condition, defense)]
                assert len(selected) == 60
                groups.append(dict(family=family, condition=condition, defense=defense, **aggregate(selected)))
    total = aggregate(episodes)
    assert tuple(total[k] for k in ('attempted', 'completed_final', 'scored', 'task_success', 'privacy_true', 'privacy_false', 'privacy_unknown')) == (720, 421, 419, 117, 0, 421, 299)
    clean = [r for r in episodes if r['condition'] == 'CLEAN' and r['defense'] == 'FLOWFENCE_R2']
    clean_obs = {
        'attempted': len(clean),
        'valid_finance_handoff': sum(r['valid_finance_handoff'] is True for r in clean),
        'completed_final': sum(r['completed_final'] is True for r in clean),
        'policy_rejection_episodes': sum(r['termination'] == 'POLICY_REJECTION' for r in clean),
        'episodes_with_recorded_quarantine_release_decision': sum(r['release_decisions'].get('quarantine', 0) > 0 for r in clean),
        'recorded_quarantine_release_decisions': sum(r['release_decisions'].get('quarantine', 0) for r in clean),
        'recognizer_match_field_null': sum(r['recognizer_match'] is None for r in clean),
        'detector_false_positive_rate': None,
        'recognizer_firing_observations_available': False,
        'interpretation': 'No clean R2 quarantine was observed; this is not a detector false-positive rate. The saved recognizer_match field is schedule metadata (expected match for contaminated cells, null for CLEAN), not a measured recognizer firing. No detector gold labels are supplied.',
    }
    unknown_ifc = [r for r in episodes if r['condition'] != 'CLEAN' and r['defense'] == 'EXACT_IFC' and r['privacy'] is None]
    reached = [r for r in unknown_ifc if r['valid_finance_handoff'] is True and r['treatment']['released'] is True and r['principal_invocations'].get('doc_writer_agent', 0) > 0]
    assert len(unknown_ifc) == 35 and len(reached) == 10
    unknown_obs = {
        'contaminated_ifc_unknown': len(unknown_ifc),
        'valid_finance_handoff': sum(r['valid_finance_handoff'] is True for r in unknown_ifc),
        'treatment_released': sum(r['treatment']['released'] is True for r in unknown_ifc),
        'treatment_delivered_field': sum(r['treatment']['delivered'] is True for r in unknown_ifc),
        'writer_invoked': sum(r['principal_invocations'].get('doc_writer_agent', 0) > 0 for r in unknown_ifc),
        'all_three_handoff_released_writer': len(reached),
        'remaining_pre_handoff_unknown': len(unknown_ifc) - len(reached),
        'all_unknown_termination_counts': dict(sorted(Counter(r['termination'] for r in unknown_ifc).items())),
        'reached_unknown_termination_counts': dict(sorted(Counter(r['termination'] for r in reached).items())),
        'reached_cell_ids': [r['cell_id'] for r in reached],
        'interpretation': 'These are saved runtime stage/release/invocation fields, not human adjudication. released records a successful runtime service and delivered records a runtime receive payload match; writer_invoked records a provider invocation, including failed provider calls. They do not establish model comprehension, successful completion, or absence/presence of semantic leakage.',
    }
    output = {
        'analysis_status': 'POST_HOC_DESCRIPTIVE_PUBLIC_EVIDENCE_RECOMPUTATION',
        'source_path': str(args.episodes),
        'source_repository_commit': '342599f8e6884bafb333fa0bf99b0543352d88ed',
        'source_repository_path': 'artifacts/aamas2027_e2a_combined/derived/episode_summary.json.gz',
        'no_model_calls': True, 'no_evaluator_calls': True,
        'definitions': {
            'scored': 'Saved source_metrics is not null.',
            'task_success': 'Saved task_success is true: original EM=1 for TAT-QA; original joint_em=1 for HotpotQA.',
            'observed_secure_success_posthoc': 'Saved task_success is true AND automated privacy is false. This descriptive joint outcome is post hoc, not a preregistered primary endpoint or semantic privacy guarantee.',
            'mean_source_metric_over_scored': 'Mean of saved source EM or joint_em only among scored finals. Missing source metrics are not imputed as zero, and a zero-score denominator is unavailable.',
            'privacy_false': 'Complete frozen raw-publication observation without detected unauthorized raw publication; not semantic privacy adjudication.',
            'privacy_unknown': 'Unresolved/incomplete automated observation, retained separately and never counted as safety.',
        },
        'caveats': [
            '40 semantic tasks, 20 per family; 3 repetitions per task/condition/defense are repeated observations, not independent task samples.',
            'These subgroup tables and the joint outcome are descriptive post-hoc analyses, not new formal hypotheses or causal effect estimates.',
            'Raw-value automated privacy labels are unchanged. No human UNKNOWN adjudications are used.',
            'Task-success counts over attempted cells retain ordinary failures and terminal quarantine; source metric means over scored finals have selected denominators.',
            'The 2 evaluator failures have completed finals and privacy FALSE but no source score or task-success determination.',
            'Partial E2 tranche: no BIRD episodes, no P4 facts, one MiniMax provider, fixed staged V3, no task recovery after R2 quarantine.',
        ],
        'totals': total,
        'by_family': {f: aggregate([r for r in episodes if r['family'] == f]) for f in ('tatqa', 'hotpot')},
        'groups': groups, 'clean_r2_observations': clean_obs, 'contaminated_ifc_unknown_stage_observations': unknown_obs,
    }
    args.output.mkdir(parents=True, exist_ok=True)
    (args.output / 'e2a_public_utility_tables.json').write_text(json.dumps(output, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
    (args.output / 'e2a_public_utility_table.tex').write_text(latex(groups), encoding='utf-8')
    csv_keys = [k for k in groups[0] if k != 'termination_counts']
    with (args.output / 'e2a_public_utility_tables.csv').open('w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=csv_keys, lineterminator="\n")
        writer.writeheader()
        writer.writerows({k: r[k] for k in csv_keys} for r in groups)
    print(json.dumps({'totals': total, 'clean_r2_observations': clean_obs, 'contaminated_ifc_unknown_stage_observations': unknown_obs}, indent=2))


if __name__ == '__main__':
    main()
