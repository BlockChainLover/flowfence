# Codex Task State: p1-paper-tables-refresh-2

## Goal

Refresh paper-facing result tables after the completed 252/252 MiniMax-only 3-seed P1 MAS coverage experiment. The refresh updates reproducible table-generation and table-review code, regenerates paper-facing tables from committed high-level evidence, and reruns the table review without running experiments or calling providers.

## Branch

`codex/p1-paper-tables-refresh-2`

## Inputs Inspected

- `AGENTS.md`
- `research/contract/`
- `research/logs/roadmap.md`
- `research/logs/progress.md`
- `results/evidence_index/current_evidence_index.md`
- `papers/claims_checklist.md`
- `artifacts/evidence_index/p1_claims_refresh_4.md`
- `artifacts/codex_task_state/codex_p1_claims_refresh_4.md`
- `artifacts/paper_tables/README.md`
- `artifacts/paper_tables/paper_tables_summary.json`
- `artifacts/paper_tables/paper_tables_summary.md`
- `artifacts/paper_tables_review/table_review_report.json`
- `artifacts/paper_tables_review/table_review_report.md`
- `artifacts/minimax_p1_coverage_3seed/run_manifest.json`
- `artifacts/minimax_p1_coverage_3seed/coverage_summary.json`
- `artifacts/minimax_p1_coverage_3seed/coverage_by_defense.csv`
- `artifacts/minimax_p1_coverage_3seed/coverage_by_topology.csv`
- `artifacts/minimax_p1_coverage_3seed/coverage_by_attack.csv`
- `artifacts/minimax_p1_coverage_3seed/coverage_by_attack_defense.csv`
- `artifacts/minimax_p1_coverage_3seed/coverage_by_seed.csv`
- `artifacts/minimax_p1_coverage_3seed/flowfence_clean_matrix.csv`
- `artifacts/minimax_p1_coverage_3seed/failure_breakdown.jsonl`
- `artifacts/minimax_p1_coverage_3seed_debug/retry_manifest.json`
- `scripts/export_paper_tables.py`
- `scripts/review_paper_tables.py`
- `tests/test_export_paper_tables.py`
- `tests/test_review_paper_tables.py`

## Completed

- Preserved existing P0, P1 deterministic synthetic, and legacy MiniMax 18-run smoke table exports.
- Marked `table_3_minimax_postfix_smoke` as legacy/superseded by the 252-run coverage.
- Added canonical `table_3_minimax_3seed_coverage` for the completed 252/252 MiniMax-backed synthetic-runtime coverage.
- Added `table_6_minimax_3seed_seed_stability` for seed-level stability and FlowFence clean-count reporting.
- Updated claims matrix and evidence boundaries tables to reflect p1-claims-refresh-4.
- Updated review checks for the new 252-run table, seed stability table, timeout retry details, required caveats, unsupported claims, and raw secret markers.
- Regenerated table and review artifacts under `artifacts/paper_tables/` and `artifacts/paper_tables_review/`.

## Generated Tables

- `artifacts/paper_tables/table_1_p0_agentpoison.csv` and `.md`: P0 adapted AgentPoison containment and comparator summary.
- `artifacts/paper_tables/table_2_p1_synthetic.csv` and `.md`: deterministic and strengthened synthetic MAS evidence.
- `artifacts/paper_tables/table_3_minimax_postfix_smoke.csv` and `.md`: legacy/superseded MiniMax 18-run smoke context.
- `artifacts/paper_tables/table_3_minimax_3seed_coverage.csv` and `.md`: canonical 252-run MiniMax 3-seed coverage table.
- `artifacts/paper_tables/table_4_claims_matrix.csv` and `.md`: claims matrix with 252-run coverage claims and unsupported boundaries.
- `artifacts/paper_tables/table_5_evidence_boundaries.csv` and `.md`: scope and evidence-boundary table.
- `artifacts/paper_tables/table_6_minimax_3seed_seed_stability.csv` and `.md`: seed-level stability and FlowFence clean subset table.

## Review Results

- Review status: pass.
- ERROR count: 0.
- WARN count: 0.
- INFO count: 7.
- Values matched committed source evidence where checked.
- Unsupported claims remained unsupported.
- Raw synthetic secret markers were not found.

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

- Tables are generated from committed high-level summaries only.
- Raw traces, raw provider outputs, prompts, event JSONL, policy JSONL, and per-run metrics are intentionally excluded.
- The canonical MiniMax table is MiniMax-only synthetic deterministic MAS runtime evidence.
- The tables do not support non-MiniMax generalization, production safety, or real browser/desktop/computer-use deployment claims.
- Human paper-table review is still recommended before copying numbers into a manuscript.

## Resume Instructions

Next recommended goal: `p1-paper-results-section-draft`.

Use the refreshed table artifacts and review report as the source for drafting a results section. Keep the 252-run MiniMax result scoped as MiniMax-backed multi-agent synthetic-runtime coverage, not real-world deployment or production safety evidence.
