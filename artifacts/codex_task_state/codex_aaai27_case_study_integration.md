# Codex Task State: aaai27-case-study-integration

## Goal

Integrate the new safe-trace qualitative case studies under `artifacts/case_studies_safe_trace/` into the standalone AAAI-27 FlowFence-Lite paper draft. Keep the integration accurate, concise, anonymous, and scoped. Do not run experiments or call providers.

## Branch

`codex/aaai27-case-study-integration`

## Inputs Inspected

- `AGENTS.md`
- `papers/aaai27_flowfence_draft/README.md`
- `papers/aaai27_flowfence_draft/main.tex`
- `papers/aaai27_flowfence_draft/sections/05_results.tex`
- `papers/aaai27_flowfence_draft/sections/06_analysis.tex`
- `papers/aaai27_flowfence_draft/sections/08_limitations.tex`
- `papers/aaai27_flowfence_draft/claim_traceability.md`
- `papers/aaai27_flowfence_draft/open_review_risks.md`
- `papers/aaai27_flowfence_draft/compile_notes.md`
- `artifacts/case_studies_safe_trace/README.md`
- `artifacts/case_studies_safe_trace/redacted_case_studies_with_safe_traces.md`
- `artifacts/case_studies_safe_trace/redacted_case_studies_with_safe_traces.json`
- `artifacts/case_studies_safe_trace/case_1_no_defense_workspace_leak_trace.md`
- `artifacts/case_studies_safe_trace/case_2_prompt_filter_paraphrase_failure_trace.md`
- `artifacts/case_studies_safe_trace/case_3_flowfence_safe_view_success_trace.md`
- `artifacts/case_studies_safe_trace/case_4_nonoracle_heldout_success_trace.md`
- `artifacts/case_studies_safe_trace/case_study_traceability.md`
- `artifacts/case_studies_safe_trace/case_study_review_notes.md`
- `artifacts/case_studies_safe_trace/integration_recommendation.md`
- `artifacts/codex_task_state/codex_aaai27_case_study_fix_with_safe_traces.md`

## Safe Trace Confirmation

Confirmed from `redacted_case_studies_with_safe_traces.json`:

- `case_count=4`
- `safe_trace_snippets_used=18`
- `summary_fallback_count=0`
- `raw_traces_used=false`
- `provider_outputs_used=false`
- `synthetic_secret_markers_present=false`

The old summary-only directory `artifacts/case_studies/` was not used for integration.

## Paper Changes

- Added `tables/table_case_studies.tex`.
- Added `Section: Redacted safe-trace case studies` to `sections/06_analysis.tex`.
- Added a Results pointer sentence in `sections/05_results.tex`.
- Added limitations language in `sections/08_limitations.tex`.
- Updated `README.md`, `claim_traceability.md`, `open_review_risks.md`, and `compile_notes.md`.
- Did not modify `main.tex`; the table is included through `sections/06_analysis.tex`.

## Compile Check

Attempted from `papers/aaai27_flowfence_draft/` with `/tmp/aaai27_case_compile` as output directory:

- `pdflatex -interaction=nonstopmode -output-directory=/tmp/aaai27_case_compile main.tex`
- `latexmk -pdf -interaction=nonstopmode -outdir=/tmp/aaai27_case_compile main.tex`

Both commands failed because the tools are unavailable in this environment. No PDF or LaTeX build outputs were generated in the repository.

## Known Limitations

- Case studies are redacted safe-trace illustrations, not raw transcripts and not additional experiments.
- Evidence remains MiniMax-only where provider calls are represented.
- Scope remains synthetic deterministic MAS runtime.
- No production safety, real browser/desktop computer-use deployment, arbitrary attack robustness, or non-MiniMax generalization is supported.
- Compile layout/page count could not be checked locally because LaTeX tools were unavailable.

## Resume Instructions

If continuing, run LaTeX compilation in an environment with `pdflatex` or `latexmk`, check table width/page count, and polish the case-study paragraph if it is too long. Do not read raw traces, raw prompts, provider outputs, policy logs, provider logs, `.env` files, or generated run directories.
