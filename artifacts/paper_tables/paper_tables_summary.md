# Paper Tables Summary

## Generated tables
- `table_1_p0_agentpoison.csv`
- `table_1_p0_agentpoison.md`
- `table_2_p1_synthetic.csv`
- `table_2_p1_synthetic.md`
- `table_3_minimax_postfix_smoke.csv`
- `table_3_minimax_postfix_smoke.md`
- `table_3_minimax_3seed_coverage.csv`
- `table_3_minimax_3seed_coverage.md`
- `table_4_claims_matrix.csv`
- `table_4_claims_matrix.md`
- `table_5_evidence_boundaries.csv`
- `table_5_evidence_boundaries.md`
- `table_6_minimax_3seed_seed_stability.csv`
- `table_6_minimax_3seed_seed_stability.md`
- `table_7_nonoracle_heldout_validation.csv`
- `table_7_nonoracle_heldout_validation.md`
- `table_8_nonoracle_mechanism_ablation.csv`
- `table_8_nonoracle_mechanism_ablation.md`
- `README.md`

## Source artifacts used
- `results/baseline_agentpoison_fullreact_minimax27_small_matrix_summary.json`
- `results/ablation_agentpoison_fullreact_minimax27_quarantine_only_vs_actioncanon_summary.json`
- `results/baseline_agentpoison_fullreact_minimax27_rewrite_only_weak_comparator_summary.json`
- `results/baseline_agentpoison_fullreact_minimax27_static_keyword_filter_weak_comparator_summary.json`
- `results/baseline_agentpoison_fullreact_minimax27_heldout_instruction_matrix_summary.json`
- `results/overhead_agentpoison_fullreact_minimax27_same_axis_measured_summary.json`
- `results/overhead_agentpoison_fullreact_minimax27_same_axis_proxy_summary.json`
- `artifacts/codex_task_state/codex_p1_mas_sweep.md`
- `artifacts/codex_task_state/codex_p1_benchmark_strengthening.md`
- `artifacts/minimax_p1_smoke_postfix/summary_18run.json`
- `artifacts/minimax_p1_coverage_3seed/run_manifest.json`
- `artifacts/minimax_p1_smoke_postfix_audit/audit_summary.json`
- `artifacts/minimax_p1_coverage_3seed/failure_breakdown.jsonl`
- `artifacts/minimax_p1_coverage_3seed/coverage_summary.json`
- `artifacts/minimax_p1_coverage_3seed/coverage_by_defense.csv`
- `artifacts/minimax_p1_coverage_3seed/coverage_by_topology.csv`
- `artifacts/minimax_p1_coverage_3seed/coverage_by_attack.csv`
- `artifacts/minimax_p1_coverage_3seed/coverage_by_attack_defense.csv`
- `artifacts/minimax_p1_coverage_3seed/coverage_by_seed.csv`
- `artifacts/minimax_p1_coverage_3seed/flowfence_clean_matrix.csv`
- `artifacts/minimax_p1_coverage_3seed_debug/retry_manifest.json`
- `artifacts/nonoracle_heldout_deterministic/run_manifest.json`
- `artifacts/nonoracle_heldout_deterministic/summary.json`
- `artifacts/nonoracle_heldout_deterministic/comparison_by_defense.csv`
- `artifacts/nonoracle_heldout_deterministic/comparison_by_attack_defense.csv`
- `artifacts/nonoracle_heldout_deterministic/nonoracle_oracle_delta.csv`
- `artifacts/nonoracle_heldout_deterministic/ablation_summary.csv`
- `artifacts/nonoracle_heldout_deterministic/failure_breakdown.jsonl`
- `artifacts/minimax_nonoracle_heldout_targeted/run_manifest.json`
- `artifacts/minimax_nonoracle_heldout_targeted/summary.json`
- `artifacts/minimax_nonoracle_heldout_targeted/comparison_by_defense.csv`
- `artifacts/minimax_nonoracle_heldout_targeted/comparison_by_attack_defense.csv`
- `artifacts/minimax_nonoracle_heldout_targeted/failure_breakdown.jsonl`
- `results/evidence_index/current_evidence_index.md`
- `papers/claims_checklist.md`
- `artifacts/evidence_index/p1_claims_refresh_3.md`
- `artifacts/evidence_index/p1_claims_refresh_4.md`
- `artifacts/evidence_index/p1_claims_refresh_5.md`

## Warnings
- None

## Evidence boundaries

These tables use committed high-level summaries only. MiniMax is the only real provider represented. The canonical MiniMax main-coverage result remains `table_3_minimax_3seed_coverage`; `table_3_minimax_postfix_smoke` is retained as legacy/superseded smoke context. `table_7_nonoracle_heldout_validation` and `table_8_nonoracle_mechanism_ablation` add non-oracle held-out validation and no-semantic-pattern ablation evidence. Unsupported claims remain unsupported.

## Recommended next step

`p1-results-section-revise-after-nonoracle`
