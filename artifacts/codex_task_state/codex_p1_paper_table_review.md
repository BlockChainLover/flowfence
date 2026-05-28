# Codex Task State: p1-paper-table-review

## Goal

Review paper-facing result tables in `artifacts/paper_tables/` against committed high-level evidence artifacts. Verify value consistency, caveat scope, MiniMax-only provider boundaries, unsupported-claim boundaries, and privacy hygiene. Produce a committed review report.

## Branch

`codex/p1-paper-table-review`

## Inputs Inspected

- `AGENTS.md`
- `artifacts/paper_tables/README.md`
- `artifacts/paper_tables/paper_tables_summary.json`
- `artifacts/paper_tables/paper_tables_summary.md`
- `artifacts/codex_task_state/codex_p1_results_table_export.md`
- `results/evidence_index/current_evidence_index.md`
- `papers/claims_checklist.md`
- `artifacts/evidence_index/p1_claims_refresh_3.md`
- Generated tables under `artifacts/paper_tables/`
- P0 committed summary JSON artifacts under `results/`
- P1 deterministic and strengthened synthetic task-state artifacts
- P1 MiniMax post-fix smoke and audit summary artifacts

## Review Checks Completed

- Checked required CSV and Markdown table files exist.
- Checked Table 1 P0 values against committed AgentPoison summary JSON where structured values are available.
- Checked Table 1 weak-comparator and held-out caveats for known-trigger, same-axis, weak-comparator, and stress-test boundaries.
- Checked Table 2 deterministic synthetic rows for provider calls disabled and synthetic-only scope.
- Checked Table 3 MiniMax post-fix smoke aggregate, defense subset, and failure-group values against committed smoke/audit summaries.
- Checked Table 4 claims matrix keeps unsupported claims unsupported.
- Checked Table 5 evidence-boundary rows for P0 scope, deterministic-provider disabled status, MiniMax-only evidence, non-MiniMax unsupported status, browser/desktop not-done status, and learned graph-risk scorer not-done status.
- Checked generated table and review outputs for raw synthetic secret markers.

## Issues Found

- ERROR: 0.
- WARN: 6.
- INFO: 5.
- No table values were inconsistent with source evidence.
- No unsupported claim was overmarked as supported.
- No raw synthetic secret appeared in generated table or review outputs.
- WARN issues all concern Table 3 row-level caveats that could more explicitly say "not broad real-model robustness"; the rows already state small-smoke or subset-audit scope, so no table/exporter fix was applied.

## Fixes Applied

No table/exporter fixes were needed.

The review script redacts raw synthetic secret markers in review issue payloads, so negative tests can prove detection without writing raw secret strings into committed review reports.

## Generated Review Artifacts

- `artifacts/paper_tables_review/README.md`
- `artifacts/paper_tables_review/table_review_report.json`
- `artifacts/paper_tables_review/table_review_report.md`
- `artifacts/paper_tables_review/table_issues.jsonl`

## Validation Commands

- `python scripts/export_paper_tables.py --output-dir artifacts/paper_tables`
- `python scripts/review_paper_tables.py --tables-dir artifacts/paper_tables --output-dir artifacts/paper_tables_review`
- `python -m unittest tests/test_review_paper_tables.py`
- `python -m unittest tests/test_export_paper_tables.py`
- `python -m compileall scripts src`
- `git diff --check`
- `git status --short`

## Known Limitations

- The review checks table consistency against committed high-level summaries, not raw traces or raw provider outputs.
- Table 2 still depends on committed task-state text because no structured strengthened deterministic summary JSON is committed.
- The MiniMax evidence remains a small one-seed 18-run smoke.
- Tables still require human review before being copied into a paper.

## Resume Instructions

Recommended next goal: `p1-paper-results-section-draft`.

Use `artifacts/paper_tables/` and `artifacts/paper_tables_review/` as the evidence package for drafting a conservative results section. Keep all MiniMax claims scoped to small-smoke evidence and all deterministic MAS claims scoped to synthetic evidence.
