# Build and reproduce the revised manuscript

This is the anonymous author-review revision on `codex/aamas2027-review-revision`, based on `342599f8e6884bafb333fa0bf99b0543352d88ed`. It has not been submitted. `main.tex` is the paper; `supplementary.tex` is its separate technical supplement. See [REVISION_NOTES.md](REVISION_NOTES.md) for the response to the mock review and measurements that remain missing.

## Official format

Both documents use `\documentclass[sigconf,anonymous]{aamas}`. The bundled `aamas.cls` (**2026/06/27 v2.19**), `ACM-Reference-Format.bst`, and `by.pdf` were compared byte-for-byte with the unmodified [official AAMAS 2027 author kit](https://warwick.ac.uk/fac/sci/dcs/aamas2027/aamas_2027_template.zip). The class, bibliography style, and page-layout parameters have not been modified. The copyright block and conference metadata follow the official sample: **3–7 May 2027, Hanoi, Vietnam**. This build does not rely on a “layout-equivalent” generic `acmart` class.

The [official submission instructions](https://warwick.ac.uk/fac/sci/dcs/aamas2027/guidelines-and-policies/instructions/) require LaTeX, anonymous PDF review, at most eight main-text pages, and allow subsequent reference-only pages. The separate supplementary ZIP must be at most 25 MB; essential evaluation information belongs in the main paper. The current checked PDFs have **8 total pages including references** for `main.pdf` and **2 pages** for `supplementary.pdf`. The main paper has substantive content through page 8, including the final comparison table; it is not a six-page main text plus references. Recheck these counts and visual layout after any further edit or a change of TeX environment.

`\acmSubmissionID{To be assigned}` is an intentional placeholder. Replace it with the actual OpenReview ID before formal submission; do not invent one. Preserve anonymous artifact access and review the final PDF metadata and supplementary contents.

## PDF build

Run from this directory with **Tectonic 0.17.0** (the engine used for the checked build):

```bash
tectonic main.tex
tectonic supplementary.tex
```

Tectonic manages the bibliography and repeated passes. Its first run may need to fetch standard TeX packages; this makes no experimental model or evaluator call.

Alternatively, with a complete TeX Live installation:

```bash
pdflatex -interaction=nonstopmode -halt-on-error main.tex
bibtex main
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error supplementary.tex
pdflatex -interaction=nonstopmode -halt-on-error supplementary.tex
```

The final checked build has no undefined citations, missing glyphs, or overfull text/table horizontal boxes. One main-paper overfull vertical-box warning of 1.166 pt remains; the rendered pages were checked without visible overlap or clipping. This is not a warning-free build.

Keep `aamas.cls`, `ACM-Reference-Format.bst`, `by.pdf`, and `references.bib` alongside the TeX sources. Check for undefined references/citations and overfull text, then render and inspect both PDFs. No private trajectories, credentials or provider access are required to compile the documents.

## Saved evidence and read-only recomputation

The source bundle includes safe derived CSV/JSON tables and the two recomputation scripts. These files make the displayed calculations inspectable without private traces. **The compact source ZIP is not a standalone copy of all experiment inputs or Git history**: full recomputation requires the repository with the saved public summary and historical controlled-study Git objects described below. Paper compilation itself does not require Git.

From the repository root, using Python 3 and its standard library:

```bash
PYTHONPATH=. python3 scripts/recompute_aamas2027_public_tables.py --help
PYTHONPATH=. python3 scripts/recompute_aamas2027_controlled_clusters.py --help
PYTHONPATH=. python3 scripts/recompute_aamas2027_public_tables.py \
  --episodes artifacts/aamas2027_e2a_combined/derived/episode_summary.json.gz \
  --output artifacts/aamas2027_paper_revision
PYTHONPATH=. python3 scripts/recompute_aamas2027_controlled_clusters.py \
  --repo . \
  --output artifacts/aamas2027_paper_revision/controlled_cluster_reanalysis.json \
  --cluster-csv artifacts/aamas2027_paper_revision/controlled_task_clusters.csv \
  --verify-against artifacts/aamas2027_paper_revision/recognizer_controlled.json
```

The controlled script reads safe episode and task-cluster evidence from Git commit `9615ca34d166c8c9f75c0c037626956512b0c251`; a shallow checkout missing that object is insufficient. The public script reads the supplied saved summary path. Neither script imports a live runner, calls a provider, reruns a benchmark evaluator, or overwrites source outcomes. Outputs are descriptive revision artifacts under `artifacts/aamas2027_paper_revision/`:

- `e2a_public_utility_tables.csv`, `.json`, and `e2a_public_utility_table.tex`: all 12 public utility groups and source-denominator accounting.
- `controlled_cluster_reanalysis.json` and `controlled_task_clusters.csv`: six-cluster post-hoc analysis and its safe cluster evidence.
- `recognizer_controlled.json`: the initial saved controlled-outcome audit used for consistency checking; it is not a detector-accuracy dataset.

The secure-completion conjunction and cluster intervals are explicitly **post hoc**. They do not replace any original primary metric. Automated public privacy remains **0 TRUE / 421 FALSE / 299 UNKNOWN**. The separate private UNKNOWN raw-review archive, full trajectories, credentials and hidden reasoning are excluded from this source delivery; no manual adjudication is included.
