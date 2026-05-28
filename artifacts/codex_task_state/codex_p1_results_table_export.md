# Codex Task State: p1-results-table-export

## Goal

Export paper-facing result tables from committed high-level evidence artifacts. The goal creates reproducible table-generation code plus small committed Markdown, CSV, and JSON table artifacts for P0 AgentPoison, P1 deterministic synthetic MAS, strengthened synthetic MAS, and P1 MiniMax smoke evidence.

## Branch

`codex/p1-results-table-export`

## Inputs Inspected

- `AGENTS.md`
- `results/evidence_index/current_evidence_index.md`
- `papers/claims_checklist.md`
- `artifacts/evidence_index/p1_claims_refresh_3.md`
- `artifacts/codex_task_state/codex_p1_claims_refresh_3.md`
- P0 committed AgentPoison summary JSON files under `results/`
- P1 deterministic and strengthened synthetic task-state files under `artifacts/codex_task_state/`
- P1 MiniMax post-fix smoke summaries under `artifacts/minimax_p1_smoke_postfix/`
- P1 MiniMax post-fix audit summaries under `artifacts/minimax_p1_smoke_postfix_audit/`

## Completed

- Added `scripts/export_paper_tables.py`.
- Added `tests/test_export_paper_tables.py`.
- Generated CSV and Markdown tables under `artifacts/paper_tables/`.
- Generated `artifacts/paper_tables/paper_tables_summary.json`.
- Generated `artifacts/paper_tables/paper_tables_summary.md`.
- Generated `artifacts/paper_tables/README.md`.
- Did not run experiments.
- Did not call MiniMax or any provider.
- Did not read or commit raw traces, provider outputs, prompts, event JSONL, policy JSONL, per-run metrics, credentials, or secrets.

## Generated Tables

- `table_1_p0_agentpoison.csv` / `table_1_p0_agentpoison.md`: P0 adapted AgentPoison containment and weak-comparator evidence.
- `table_2_p1_synthetic.csv` / `table_2_p1_synthetic.md`: P1 deterministic and strengthened synthetic MAS evidence boundaries and comparison status.
- `table_3_minimax_postfix_smoke.csv` / `table_3_minimax_postfix_smoke.md`: P1 clean post-fix MiniMax 18-run smoke aggregate, defense subsets, and prompt-filter failure groups.
- `table_4_claims_matrix.csv` / `table_4_claims_matrix.md`: major supported, partial, and unsupported claim rows.
- `table_5_evidence_boundaries.csv` / `table_5_evidence_boundaries.md`: evidence scopes, unsupported boundaries, and next evidence required.
- `paper_tables_summary.json` / `paper_tables_summary.md`: source artifacts, generated files, warnings, and next step.

## Validation Commands

- `python scripts/export_paper_tables.py --help`
- `python scripts/export_paper_tables.py --output-dir artifacts/paper_tables`
- `python -m unittest tests/test_export_paper_tables.py`
- `python -m compileall scripts src`
- `git diff --check`
- `git status --short`

## Known Limitations

- Tables are paper-facing drafts and must be manually reviewed before use in a paper.
- Table 2 uses committed task-state summaries because no structured strengthened deterministic summary JSON is committed.
- MiniMax evidence remains a small one-seed 18-run smoke.
- No non-MiniMax generalization, production safety, or broad real-model robustness claim is supported.
- Unsupported claims remain explicitly unsupported.

## Resume Instructions

Next recommended goal: `p1-paper-table-review`.

Review `artifacts/paper_tables/` against `results/evidence_index/current_evidence_index.md` and `papers/claims_checklist.md`. Do not broaden claims during review unless new committed evidence supports the change.
