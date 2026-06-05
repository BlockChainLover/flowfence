# Codex Task State: aaai27-case-study-fix-with-safe-traces

## Goal

Create a stronger redacted qualitative FlowFence-Lite case-study package using safe-trace snippets where available. Do not integrate into the paper, do not modify `main.tex`, do not modify runtime behavior, and do not call MiniMax or any provider.

## Branch

`codex/aaai27-case-study-fix-with-safe-traces`

## Inputs Inspected

- `AGENTS.md`
- Existing summary-only case studies under `artifacts/case_studies/`
- `artifacts/codex_task_state/codex_aaai27_redacted_case_studies.md`
- `artifacts/minimax_p1_coverage_3seed/coverage_summary.md`
- `artifacts/minimax_p1_coverage_3seed/failure_breakdown.jsonl`
- `artifacts/minimax_p1_coverage_3seed/flowfence_clean_matrix.md`
- `artifacts/nonoracle_heldout_deterministic/summary.md`
- `artifacts/minimax_nonoracle_heldout_targeted/summary.md`
- `artifacts/paper_tables/table_3_minimax_3seed_coverage.md`
- `artifacts/paper_tables/table_7_nonoracle_heldout_validation.md`
- `artifacts/paper_tables/table_8_nonoracle_mechanism_ablation.md`
- `papers/aaai27_flowfence_draft/sections/05_results.tex`
- `papers/aaai27_flowfence_draft/sections/06_analysis.tex`
- `papers/aaai27_flowfence_draft/open_review_risks.md`
- `papers/aaai27_flowfence_draft/claim_traceability.md`
- `scripts/export_redacted_case_studies.py`
- `tests/test_export_redacted_case_studies.py`

## Safe Trace Availability

Local `/tmp` safe roots were not available. Remote safe-only roots on `wentian-server` were available for:

- `/tmp/flowfence_mas_p1_coverage_3seed_252run`
- `/tmp/flowfence_minimax_nonoracle_heldout_72run`

The deterministic non-oracle held-out root `/tmp/flowfence_nonoracle_heldout_deterministic` was unavailable remotely. Case 2 therefore uses an available targeted MiniMax-backed synthetic-runtime validation safe trace for `blackboard_4 / workspace_poisoning_paraphrase / prompt_filter / seed=1` rather than generating a deterministic fallback run.

Only these safe-only files were copied to local `/tmp/flowfence_case_safe_roots/`:

- `meta.json`
- `metrics.json`
- `events.safe.jsonl`

No full traces, prompts, provider responses, policy logs, individual generated run directories, `.env` files, or provider logs were copied or committed.

## Case Studies Created

Generated under `artifacts/case_studies_safe_trace/`:

- Case 1: no-defense workspace propagation leak, 6 safe snippets.
- Case 2: prompt-filter paraphrase failure, 6 safe snippets.
- Case 3: FlowFence safe-view/quarantine success, 3 safe snippets.
- Case 4: non-oracle FlowFence held-out success, 3 safe snippets.

The combined JSON records:

- `case_count=4`
- `safe_trace_snippets_used=18`
- `summary_fallback_count=0`
- `raw_traces_used=false`
- `provider_outputs_used=false`
- `synthetic_secret_markers_present=false`

## Redaction Scan

Scanned `artifacts/case_studies_safe_trace/` for:

- `$4800`
- `supplier breach investigation`
- `CUST-8831-PRIVATE`
- `sk-internal-demo-token`
- `raw provider output`
- `full raw prompt`
- `events.full.jsonl`
- `raw_observation`
- `full_trajectory`

Result: 10 files scanned, 0 findings.

## Validation Commands

- `python scripts/export_redacted_case_studies_from_safe_traces.py --help`
- `python -m unittest tests/test_export_redacted_case_studies_from_safe_traces.py`
- `python scripts/export_redacted_case_studies_from_safe_traces.py --output-dir artifacts/case_studies_safe_trace --coverage-runs-root /tmp/flowfence_case_safe_roots/coverage --nonoracle-runs-root /tmp/flowfence_case_safe_roots/nonoracle --summary-root artifacts --include-summary-fallback --max-events 6 --max-preview-chars 180`
- redaction/privacy scan over `artifacts/case_studies_safe_trace/`
- `python -m compileall scripts src`
- `git diff --check`
- `git status --short`

All listed validation commands completed successfully.

## Known Limitations

- Case studies are qualitative illustrations, not new experimental evidence.
- Safe snippets are redacted previews, not raw transcripts.
- Evidence remains MiniMax-only where provider calls are represented.
- Scope remains synthetic deterministic MAS runtime.
- No production safety, real browser/desktop computer-use deployment, arbitrary attack robustness, or non-MiniMax generalization is supported.
- Case 2 uses targeted MiniMax safe trace because deterministic safe traces were unavailable.

## Resume Instructions

If continuing this goal, inspect `artifacts/case_studies_safe_trace/`, rerun validation, and keep all outputs redacted. Do not read or commit full traces, raw prompts, provider responses, policy decisions, per-run generated metrics, provider logs, `.env` files, or secrets.
