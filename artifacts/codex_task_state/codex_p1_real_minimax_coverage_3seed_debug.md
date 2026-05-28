# Codex Task State: p1-real-minimax-coverage-3seed-debug

## Goal

Debug the single MiniMax read timeout from the 3-seed P1 MAS coverage experiment, retry only the failed/missing run if safe, and refresh high-level coverage artifacts.

## Branch

`codex/p1-real-minimax-coverage-3seed-debug`

## Inputs Inspected

- `artifacts/minimax_p1_coverage_3seed/README.md`
- `artifacts/minimax_p1_coverage_3seed/run_manifest.json`
- `artifacts/minimax_p1_coverage_3seed/coverage_summary.json`
- `artifacts/minimax_p1_coverage_3seed/coverage_summary.md`
- `artifacts/minimax_p1_coverage_3seed/failure_breakdown.jsonl`
- `artifacts/codex_task_state/codex_p1_real_minimax_coverage_3seed.md`
- `configs/experiment/mas_p1_minimax_coverage_3seed.yaml`
- `src/runner/sweep_mas.py`
- Remote high-level status and metrics-file presence under `/tmp/flowfence_mas_p1_coverage_3seed_252run`

## Failed Run Diagnosis

- Failed run: `mas_p1__enterprise_assistant_001__chain_4__summary_poisoning_direct__prompt_filter__seed1`
- Topology: `chain_4`
- Attack: `summary_poisoning_direct`
- Defense: `prompt_filter`
- Seed: `1`
- Failure type: MiniMax read timeout
- Diagnosis: transient provider timeout. The run directory existed remotely but lacked `metrics.json` before retry.

## Resume/Retry Strategy

`sweep_mas.py` already skips run directories that contain `metrics.json` when run without `--force`. Therefore no runtime code change was needed.

Retry command used the same output root without `--force`, so 251 completed runs were skipped and only the missing run executed.

## Provider-call Safety Check

The coverage sweep without `--allow-provider-calls` failed before any MiniMax request, as expected.

## Retry Result

- Executed: yes
- Completed before retry: 251
- Failed before retry: 1
- Retry completed runs: 1
- Retry skipped runs: 251
- Retry failed runs: 0
- Completed after retry: 252
- Failed after retry: 0
- Canonical coverage artifacts refreshed: yes

## Updated Coverage Artifacts

- `artifacts/minimax_p1_coverage_3seed/README.md`
- `artifacts/minimax_p1_coverage_3seed/run_manifest.json`
- `artifacts/minimax_p1_coverage_3seed/coverage_summary.json`
- `artifacts/minimax_p1_coverage_3seed/coverage_summary.md`
- `artifacts/minimax_p1_coverage_3seed/coverage_by_defense.csv`
- `artifacts/minimax_p1_coverage_3seed/coverage_by_defense.md`
- `artifacts/minimax_p1_coverage_3seed/coverage_by_topology.csv`
- `artifacts/minimax_p1_coverage_3seed/coverage_by_topology.md`
- `artifacts/minimax_p1_coverage_3seed/coverage_by_attack.csv`
- `artifacts/minimax_p1_coverage_3seed/coverage_by_attack.md`
- `artifacts/minimax_p1_coverage_3seed/coverage_by_attack_defense.csv`
- `artifacts/minimax_p1_coverage_3seed/coverage_by_attack_defense.md`
- `artifacts/minimax_p1_coverage_3seed/coverage_by_seed.csv`
- `artifacts/minimax_p1_coverage_3seed/coverage_by_seed.md`
- `artifacts/minimax_p1_coverage_3seed/flowfence_clean_matrix.csv`
- `artifacts/minimax_p1_coverage_3seed/flowfence_clean_matrix.md`
- `artifacts/minimax_p1_coverage_3seed/failure_breakdown.jsonl`

## Validation Commands

```bash
python scripts/debug_minimax_coverage_timeout.py --help
python scripts/audit_minimax_coverage.py --help
PYTHONPATH=. python src/runner/sweep_mas.py --help
PYTHONPATH=. python src/runner/summarize_mas_p1.py --help
python -m unittest tests/test_debug_minimax_coverage_timeout.py
python -m unittest tests/test_audit_minimax_coverage.py
python -m unittest tests/test_minimax_coverage_config.py
python -m compileall scripts src
git diff --check
git status --short
```

## Known Limitations

- This remains MiniMax-only evidence.
- Raw traces and raw provider outputs are intentionally not committed.
- Non-MiniMax generalization and production safety remain unsupported.
- Claims and paper-facing tables should be refreshed after this artifact update.

## Resume Instructions

Use `artifacts/minimax_p1_coverage_3seed/coverage_summary.json` as the refreshed canonical 3-seed coverage summary. The timeout debug evidence is in `artifacts/minimax_p1_coverage_3seed_debug/`. Do not inspect or commit raw provider outputs.
