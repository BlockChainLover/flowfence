# Results

This directory keeps raw or near-raw run outputs that support the two retained papers. Rebuttal navigation starts from the paper maps, not from browsing this directory by hand:

- `experiments/emnlp2026_flowfence/README.md`
- `experiments/wine2026_flowfence/README.md`

## Generated Manifests

- `results/evidence_manifest_summary.md`: count summary for retained and cleanup-candidate entries.
- `results/canonical_evidence_manifest.csv`: all retained top-level `results/` entries and the evidence source requiring each one.
- `results/cleanup_candidates_manifest.csv`: non-canonical top-level `results/` entries and their deletion rationale.
- `experiments/emnlp2026_flowfence/results_manifest.csv`: EMNLP-facing retained result subset.
- `experiments/wine2026_flowfence/results_manifest.csv`: WINE-facing retained result subset.

Dry-run reviewed cleanup with:

```bash
python3 scripts/rebuttal_cleanup.py --scope results
```

Actual deletion requires both `--execute` and `--confirm DELETE_REBUTTAL_CLEANUP`.

Current status: the reviewed result cleanup was executed on 2026-06-22. The cleanup manifest is retained as an audit trail and should report zero existing cleanup candidates.

## Canonical Result Groups

Keep these groups unless a replacement evidence package is created:

- EMNLP cross-provider and MiniMax P0 raw roots listed in `artifacts/emnlp2026_p0/results/emnlp_p0_cross_provider_runs.csv`.
- EMNLP mechanism, held-out, same-axis, adaptive, pressure, paraphrase, false-positive, and overhead roots listed in `experiments/emnlp2026_flowfence/README.md`.
- WINE P0 inherited MiniMax roots listed in `experiments/wine2026_flowfence/README.md`.
- WINE P1 high-level summaries under `artifacts/minimax_p1_coverage_3seed/`, `artifacts/nonoracle_heldout_deterministic/`, `artifacts/minimax_nonoracle_heldout_targeted/`, `artifacts/paper_tables/`, and `artifacts/case_studies_safe_trace/`.

## Deleted Non-Canonical Historical Material

The following result families were not canonical for the retained EMNLP/WINE papers and were removed after manifest review:

- `smoke_*`
- `diagnostic_*`
- `baseline_asb_*`
- `baseline_agentdojo_*`
- `emnlp_p0_dryrun_*`
- old simplified `qwen36` pre-method roots such as `baseline_agentpoison_qwen36_*`, `method_*_qwen36_*`, and `premethod_summary_agentpoison_strategyqa_premethod_v2.json`
- older official-context or recovery-trial AgentPoison roots not listed in the EMNLP evidence map

## Minimum Contents Per Retained Raw Run

- `run_manifest.json` or equivalent config snapshot.
- `resolved_config.yaml` where available.
- `status.txt` or recorded completion state.
- `metrics.json` or `baseline_summary.json`.
- `case_results.jsonl` and per-case details when those are the raw audit source.
- `stdout.log` / `stderr.log` or equivalent failure notes when the run was partial.

## Audit Rule

Every retained result must be referenced by a paper evidence map, a high-level summary artifact under `artifacts/`, or `research/logs/progress.md`. If no retained paper uses it, it should be deleted or moved out of the paper-facing repository.
