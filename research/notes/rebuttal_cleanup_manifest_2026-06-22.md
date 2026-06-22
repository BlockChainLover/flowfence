# Rebuttal Cleanup Manifest - 2026-06-22

## Purpose

This manifest records the reviewed cleanup candidates for the two-paper rebuttal organization goal. It is retained as an audit trail after physical cleanup.

## Canonical Paper Directories To Keep

- `papers/emnlp2026_flowfence/`
- `papers/wine2026_flowfence/`
- `papers/README.md`

## Paper Cleanup Candidates

These paths are superseded by the two active paper directories and the new experiment evidence maps:

- `papers/aaai27_flowfence_draft/`
- `papers/aaai27_template/`
- `papers/icde2027_flowfence/`
- `papers/templates/`
- `papers/figures/`
- `papers/claims_checklist.md`
- `papers/draft_full_v1.md`
- `papers/draft_v0.md`
- `papers/draft_v1.md`
- `papers/experiment_narrative_agentpoison_minimax.md`
- `papers/experiment_results_summary.md`
- `papers/figures_todo.md`
- `papers/outline.md`
- `papers/overhead_agentpoison_minimax.md`
- `papers/overhead_agentpoison_minimax_measured.md`
- `papers/result_table_agentpoison_minimax.md`
- `papers/.DS_Store`

Rationale: the retained EMNLP and WINE paper directories contain the current drafts. Rebuttal evidence lookup now lives under `experiments/emnlp2026_flowfence/README.md` and `experiments/wine2026_flowfence/README.md`.

## Canonical Results And Artifacts To Keep

Keep these until a replacement evidence package exists:

- `artifacts/emnlp2026_p0/`
- `artifacts/emnlp2026_p1/`
- `artifacts/icde2027_supplemental/`
- `artifacts/paper_tables/`
- `artifacts/minimax_p1_coverage_3seed/`
- `artifacts/nonoracle_heldout_deterministic/`
- `artifacts/minimax_nonoracle_heldout_targeted/`
- `artifacts/case_studies_safe_trace/`
- `artifacts/mas_p1_deterministic_matrix/status.json`
- `results/baseline_agentpoison_fullreact_minimax27_small_matrix_summary.json`
- `results/ablation_agentpoison_fullreact_minimax27_quarantine_only_vs_actioncanon_summary.json`
- `results/baseline_agentpoison_fullreact_minimax27_rewrite_only_weak_comparator_summary.json`
- `results/baseline_agentpoison_fullreact_minimax27_static_keyword_filter_weak_comparator_summary.json`
- `results/baseline_agentpoison_fullreact_minimax27_heldout_instruction_matrix_summary.json`
- `results/overhead_agentpoison_fullreact_minimax27_same_axis_proxy_summary.json`
- `results/overhead_agentpoison_fullreact_minimax27_same_axis_measured_summary.json`
- raw `results/` roots listed in `artifacts/emnlp2026_p0/results/emnlp_p0_cross_provider_runs.csv`
- raw `results/` roots listed in `artifacts/icde2027_supplemental/results/poison_pressure_runs.csv`
- raw `results/` roots listed in `artifacts/icde2027_supplemental/results/paraphrase_family_runs.csv`
- raw `results/` roots listed in `artifacts/icde2027_supplemental/results/false_positive_runs.csv`
- adaptive-pilot raw roots matching `results/emnlp_p1_adaptive_*_kimi25_v1/`
- same-axis comparator roots matching `results/emnlp_p0_same_axis_*`
- measured overhead roots matching `results/overhead_agentpoison_fullreact_minimax27_triggerquery_*`

## Result Cleanup Candidates

These result families are not canonical for the retained EMNLP/WINE evidence maps:

- `results/smoke_*`
- `results/diagnostic_*`
- `results/baseline_asb_*`
- `results/baseline_agentdojo_*`
- `results/emnlp_p0_dryrun_*`
- `results/baseline_agentpoison_qwen36_*`
- `results/method_flowfence_lite_qwen36_*`
- `results/method_flowfence_lite_tuned_qwen36_*`
- `results/method_nodefense_qwen36_*`
- `results/premethod_summary_agentpoison_strategyqa_premethod_v2.json`
- `results/templates/`
- `results/.DS_Store`
- older official-context AgentPoison roots not referenced by the EMNLP map:
  - `results/baseline_agentpoison_fullreact_dpr_strategyqa_v1/`
  - `results/baseline_agentpoison_fullreact_dpr_strategyqa_v1_parsefix/`
  - `results/baseline_agentpoison_fullreact_dpr_strategyqa_v1_parsefix2/`
  - `results/baseline_agentpoison_fullreact_dpr_strategyqa_kimi25_triggerquery_v1/`
  - `results/method_flowfence_lite_fullreact_kimi25_triggerquery_*`
  - `results/method_flowfence_lite_fullreact_minimax27_triggerquery_quarantine_cleanscontext_*`
  - `results/method_flowfence_lite_fullreact_minimax27_triggerquery_quarantine_recoveryhint_v1/`
  - `results/method_flowfence_lite_fullreact_minimax27_phase1_actioncanon_summary.json`

For the concrete deletion audit trail, use `results/cleanup_candidates_manifest.csv`. It classifies all 97 cleanup-candidate top-level `results/` entries and now records zero existing cleanup candidates. Retained entries are listed in `results/canonical_evidence_manifest.csv`.

## Safe Cleanup Procedure

1. Confirm the two evidence maps are acceptable:
   - `experiments/emnlp2026_flowfence/README.md`
   - `experiments/wine2026_flowfence/README.md`
2. Dry-run the reviewed cleanup script:
   - `python3 scripts/rebuttal_cleanup.py --scope papers`
   - `python3 scripts/rebuttal_cleanup.py --scope results`
3. Run `git status --short` and confirm there are no unexpected user edits in cleanup paths.
4. Delete paper cleanup candidates in one small commit:
   - `python3 scripts/rebuttal_cleanup.py --scope papers --execute --confirm DELETE_REBUTTAL_CLEANUP`
5. Delete result cleanup candidates in a separate small commit:
   - `python3 scripts/rebuttal_cleanup.py --scope results --execute --confirm DELETE_REBUTTAL_CLEANUP`
6. Re-run `find papers -maxdepth 1 -mindepth 1 -print | sort`, manifest checks, and `git status --short`.

## Current Status

- Evidence maps and per-paper contracts were added.
- `scripts/rebuttal_cleanup.py` was added as a dry-run-first reviewed cleanup path.
- Reviewed paper cleanup was executed with `python3 scripts/rebuttal_cleanup.py --scope papers --execute --confirm DELETE_REBUTTAL_CLEANUP`.
- Reviewed result cleanup was executed with `python3 scripts/rebuttal_cleanup.py --scope results --execute --confirm DELETE_REBUTTAL_CLEANUP`.
- Post-cleanup dry-runs report 17 missing paper candidates, 97 missing result candidates, and zero existing cleanup candidates.
