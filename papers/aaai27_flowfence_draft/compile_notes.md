# Compile Notes

## Author Kit

- Official author kit downloaded: yes.
- Source URL: `https://aaai.org/authorkit27/`.
- Archive: `papers/aaai27_template/original_download/authorkit27.zip`.
- Extracted directory: `papers/aaai27_template/extracted/AuthorKit27/`.
- AAAI style file found: yes, `aaai2027.sty`.
- AAAI bibliography style found: yes, `aaai2027.bst`.
- Draft-local style files: `papers/aaai27_flowfence_draft/aaai2027.sty` and `papers/aaai27_flowfence_draft/aaai2027.bst`.

## v1 Compile Attempt

- `latexmk` available: no.
- `pdflatex` available: no.
- Compile attempted: yes, but both commands failed before LaTeX execution because the executables are unavailable.
- Requested compile command: `latexmk -pdf -interaction=nonstopmode main.tex`.
- Fallback command: `pdflatex -interaction=nonstopmode main.tex`.
- Actual commands:
  - `latexmk -pdf -interaction=nonstopmode main.tex`
  - `pdflatex -interaction=nonstopmode main.tex`
  - `bibtex main`
- Result: all three commands returned `command not found`; compilation still needs to be checked in an environment with a LaTeX distribution.
- PDF produced: no.
- Page count: unavailable.
- Unresolved references/citations: not checkable locally without LaTeX.

## Bibliography Status

- v1 reference count: 12.
- Placeholder `Anonymous` author entries remaining: 0.
- Remaining TODO citations in `sections/07_related_work.tex`: 0.
- Static citation-key check: 12 cited keys, 12 BibTeX keys, 0 missing, 0 unused.
- Bibliography metadata was checked against arXiv/ACL Anthology pages where available and includes classic information-flow/least-privilege references. Final venue formatting still needs human verification before submission.

## Known TODOs

- Human-review table formatting after a LaTeX compile is available.
- Confirm final AAAI anonymity details against the latest author-kit instructions before submission.
- Replace the text placeholder for Figure 1 with a vector diagram if the draft moves toward submission.
