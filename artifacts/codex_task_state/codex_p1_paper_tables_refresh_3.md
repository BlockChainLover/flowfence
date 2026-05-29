# Codex Task State: p1-paper-tables-refresh-3

## Goal

Refresh paper-facing result tables after the successful non-oracle held-out FlowFence validation, adding non-oracle held-out validation and no-semantic-pattern ablation evidence while preserving existing P0, deterministic P1, and canonical 252-run MiniMax coverage tables.

## Branch

`codex/p1-paper-tables-refresh-3`

## Inputs Inspected

- `AGENTS.md`
- `results/evidence_index/current_evidence_index.md`
- `papers/claims_checklist.md`
- `artifacts/evidence_index/p1_claims_refresh_5.md`
- `artifacts/codex_task_state/codex_p1_claims_refresh_5.md`
- `artifacts/paper_tables/README.md`
- `artifacts/paper_tables/paper_tables_summary.json`
- `artifacts/paper_tables/paper_tables_summary.md`
- `artifacts/paper_tables_review/table_review_report.json`
- `artifacts/paper_tables_review/table_review_report.md`
- `artifacts/nonoracle_heldout_deterministic/README.md`
- `artifacts/nonoracle_heldout_deterministic/run_manifest.json`
- `artifacts/nonoracle_heldout_deterministic/summary.json`
- `artifacts/nonoracle_heldout_deterministic/summary.md`
- `artifacts/nonoracle_heldout_deterministic/comparison_by_defense.csv`
- `artifacts/nonoracle_heldout_deterministic/comparison_by_attack_defense.csv`
- `artifacts/nonoracle_heldout_deterministic/nonoracle_oracle_delta.csv`
- `artifacts/nonoracle_heldout_deterministic/ablation_summary.csv`
- `artifacts/nonoracle_heldout_deterministic/failure_breakdown.jsonl`
- `artifacts/minimax_nonoracle_heldout_targeted/README.md`
- `artifacts/minimax_nonoracle_heldout_targeted/run_manifest.json`
- `artifacts/minimax_nonoracle_heldout_targeted/summary.json`
- `artifacts/minimax_nonoracle_heldout_targeted/summary.md`
- `artifacts/minimax_nonoracle_heldout_targeted/comparison_by_defense.csv`
- `artifacts/minimax_nonoracle_heldout_targeted/comparison_by_attack_defense.csv`
- `artifacts/minimax_nonoracle_heldout_targeted/failure_breakdown.jsonl`
- `scripts/export_paper_tables.py`
- `scripts/review_paper_tables.py`
- `tests/test_export_paper_tables.py`
- `tests/test_review_paper_tables.py`

## Completed

- Updated `scripts/export_paper_tables.py` to generate two new paper-facing tables:
  - `table_7_nonoracle_heldout_validation`
  - `table_8_nonoracle_mechanism_ablation`
- Updated `table_4_claims_matrix` rows for non-oracle validation, oracle-label removal, targeted MiniMax validation, no-semantic-pattern ablation, and arbitrary-attack unsupported boundaries.
- Updated `table_5_evidence_boundaries` with deterministic non-oracle, targeted MiniMax non-oracle, and no-semantic-pattern ablation rows.
- Updated `scripts/review_paper_tables.py` to review the new tables against committed high-level evidence.
- Updated table exporter/reviewer tests for the new tables and unsupported-claim checks.
- Regenerated `artifacts/paper_tables/` and `artifacts/paper_tables_review/`.

## Generated Tables

- `artifacts/paper_tables/table_7_nonoracle_heldout_validation.csv`
- `artifacts/paper_tables/table_7_nonoracle_heldout_validation.md`
- `artifacts/paper_tables/table_8_nonoracle_mechanism_ablation.csv`
- `artifacts/paper_tables/table_8_nonoracle_mechanism_ablation.md`

Existing tables 1-6 were regenerated from the updated exporter. `table_3_minimax_3seed_coverage` remains the canonical MiniMax main-coverage table. `table_3_minimax_postfix_smoke` remains legacy/superseded context.

## Review Results

- ERROR count: 0
- WARN count: 0
- INFO count: 9
- Table values inconsistent with source evidence: false
- Unsupported claim overmarked: false
- Raw secret appeared: false

## Validation Commands

- `python scripts/export_paper_tables.py --help`
- `python scripts/review_paper_tables.py --help`
- `python scripts/export_paper_tables.py --output-dir artifacts/paper_tables`
- `python scripts/review_paper_tables.py --tables-dir artifacts/paper_tables --output-dir artifacts/paper_tables_review`
- `python -m unittest tests/test_export_paper_tables.py`
- `python -m unittest tests/test_review_paper_tables.py`
- `python -m compileall scripts src`
- `git diff --check`
- `git status --short`

## Known Limitations

- MiniMax remains the only real provider represented.
- Non-oracle deterministic validation uses provider calls disabled.
- Targeted non-oracle MiniMax validation is synthetic-runtime with MiniMax final writer.
- The new held-out evidence supports configured paraphrase attacks only; arbitrary attack robustness remains unsupported.
- Non-MiniMax generalization, production safety, and real browser/desktop/computer-use evidence remain unsupported.
- Raw traces, prompts, provider outputs, event JSONL, policy JSONL, and individual per-run metrics are intentionally not included.

## Resume Instructions

If continuing from this goal, inspect the regenerated paper tables and review report first. If review remains passing, the next goal should revise the Results-section draft to incorporate the non-oracle held-out validation and ablation evidence.
