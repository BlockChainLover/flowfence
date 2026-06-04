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

## Known TODOs Before Submission

- Hand-polish dense tables for final AAAI layout.
- Prefer a vector redraw of Figure 1 before final submission.
- Human-verify every BibTeX entry and venue field.
- Confirm final AAAI-27 page limit, anonymity rules, and supplemental-material instructions against the latest author kit.
- Consider adding redacted qualitative case studies or deeper module ablations if reviewers are expected to ask for mechanism evidence.
