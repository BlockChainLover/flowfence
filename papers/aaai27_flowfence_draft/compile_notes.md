# Compile Notes

## Author Kit

- Official author kit downloaded: yes.
- Source URL: `https://aaai.org/authorkit27/`.
- Archive: `papers/aaai27_template/original_download/authorkit27.zip` in the original repository context.
- AAAI style file found: yes, `aaai2027.sty`.
- AAAI bibliography style found: yes, `aaai2027.bst`.
- Draft-local style files: `aaai2027.sty` and `aaai2027.bst`.

## Polished v2 Compile Check

- Figure inserted: `figures/flowfence_pipeline.png`.
- Figure reference label: `fig:flowfence_pipeline`.
- Compile environment: ChatGPT editing container.
- `pdflatex` available: yes.
- `bibtex` symlink issue: the environment uses `/usr/bin/bibtex.original`.
- Successful compile sequence:
  - `pdflatex -interaction=nonstopmode main.tex`
  - `/usr/bin/bibtex.original main`
  - `pdflatex -interaction=nonstopmode main.tex`
  - `pdflatex -interaction=nonstopmode main.tex`
- PDF produced: yes.
- PDF page count: 8 pages.
- Unresolved citations after final pass: 0.
- Unresolved references after final pass: 0.
- Remaining layout warnings: several overfull/underfull boxes caused mainly by dense tables and narrow AAAI two-column layout. Rendered pages were inspected and no obvious clipping was observed.

## Polishing Changes in v2

- Added two formal propositions:
  - policy-preserving safe-view invariant
  - topology fanout amplification
- Expanded problem definition and threat model.
- Expanded FlowFence-Lite method section with risk scoring, algorithm-style mediation steps, safe-view/quarantine details, and non-oracle framing.
- Expanded benchmark and results sections.
- Added clearer analysis of static ACL, prompt filter, topology effects, non-oracle validation, and no-semantic-pattern ablation.
- Replaced placeholder bibliography entries with concrete references where available.
- Added reviewer-oriented claim traceability and open risk notes.

## Safe-Trace Case-Study Integration

- Added concise redacted safe-trace case-study discussion to `sections/06_analysis.tex`.
- Added pointer sentence in `sections/05_results.tex`.
- Added limitations language clarifying that case studies are redacted safe-trace illustrations, not raw transcripts or additional experiments.
- Added compact case-study table: `tables/table_case_studies.tex`.
- Updated claim traceability and open review risks.
- Compilation attempted after integration: yes.
- Compile commands attempted:
  - `pdflatex -interaction=nonstopmode -output-directory=/tmp/aaai27_case_compile main.tex`
  - `latexmk -pdf -interaction=nonstopmode -outdir=/tmp/aaai27_case_compile main.tex`
- Compile result: not completed because `pdflatex` and `latexmk` were unavailable in this environment.
- PDF produced after integration: no.
- Page count after integration: not available.
- Overfull warnings over 5pt after integration: not available.
- Unresolved citations/references after integration: not available.

## Known TODOs Before Submission

- Hand-polish dense tables for final AAAI layout.
- Prefer a vector redraw of Figure 1 before final submission.
- Human-verify every BibTeX entry and venue field.
- Confirm final AAAI-27 page limit, anonymity rules, and supplemental-material instructions against the latest author kit.
- Consider adding redacted qualitative case studies or deeper module ablations if reviewers are expected to ask for mechanism evidence.

## Method/Results Polish Compile Check

- Timestamp: `2026-06-10T04:34:49Z`.
- Polished files: method, benchmark, results, analysis, limitations, conclusion, README, claim/risk notes, and dense result tables.
- Main layout intent:
  - shorten table headers and comparison text,
  - replace long monospaced case identifiers with readable names,
  - keep caveats in captions/prose rather than table cells where possible,
  - make redacted safe-trace examples concise enough for AAAI two-column layout.
- Preferred compile command attempted:
  - `latexmk -pdf -interaction=nonstopmode main.tex`
- Preferred compile result:
  - failed; `latexmk` was not available in this environment.
- Fallback compile command attempted:
  - `pdflatex -interaction=nonstopmode main.tex`
- Fallback compile result:
  - failed; `pdflatex` was not available in this environment.
- Fresh PDF produced after method/results polish: no.
- Fresh page count after method/results polish: not available.
- Fresh unresolved citation/reference count: not available.
- Fresh overfull hbox warning count over 5pt: not available.
- Expected remaining layout risk:
  - dense tables may still require a LaTeX-capable layout pass, but the edited tables should be less prone to overfull boxes than the prior case-study integrated draft.

## Claims/Results Sync Notes

- Added claims/results coverage audit: `claims_results_coverage_audit.md`.
- Added held-out instruction stress row to `tables/table_p0_agentpoison.tex`.
- Added Results prose explaining the P0 static-keyword caveat, held-out instruction stress, and why P0 overhead is traceable but not headline.
- Added `tables/table_evidence_boundaries.tex` to the Limitations section so paper-body text explicitly states what the evidence does and does not support.
- No fresh compile was attempted during the claims/results sync beyond the prior tool-availability check, because this environment still lacks `latexmk` and `pdflatex`.
