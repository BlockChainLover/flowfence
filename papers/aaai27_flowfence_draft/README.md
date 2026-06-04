# AAAI-27 FlowFence-Lite Draft - Polished v2

This directory contains a standalone anonymous AAAI-27 draft for FlowFence-Lite. This polished v2 draft expands the earlier skeleton with formal problem definitions, two propositions, a non-oracle method description, a risk-scoring pipeline, stronger experiment/result analysis, a Figure 1 pipeline diagram, cleaned references, and reviewer-facing claim/risk notes.

The draft is not camera-ready and is not integrated into any existing EMNLP paper directory. It uses committed evidence tables, claims, and high-level summary artifacts only. Raw traces, raw provider outputs, prompts, event JSONL, policy JSONL, per-run metrics, credentials, and secrets are not included.

MiniMax is the only real provider represented. All MiniMax claims are scoped to MiniMax-backed synthetic-runtime evidence. Human review is required before submission or integration into another paper tree.

Key files:

- `main.tex`
- `sections/*.tex`
- `tables/*.tex`
- `figures/flowfence_pipeline.png`
- `references.bib`
- `claim_traceability.md`
- `open_review_risks.md`
- `reviewer_polish_notes.md`
- `compile_notes.md`

Version v2 keeps the official AAAI-27 style files copied from the downloaded author kit and does not modify `papers/emnlp2026_flowfence/`.

## Compile status

In the editing environment, the draft compiled successfully with `pdflatex` and `/usr/bin/bibtex.original`.

- PDF produced: yes
- Page count: 8
- Unresolved citations: 0
- Unresolved references: 0
- Remaining layout issues: several overfull/underfull boxes from dense tables and narrow columns; no visible clipping was observed in rendered pages.

The generated PDF is supplied separately. The source zip does not include LaTeX auxiliary files.
