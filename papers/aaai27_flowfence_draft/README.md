# AAAI-27 FlowFence-Lite Draft v1

This directory contains a standalone anonymous AAAI-27 draft for FlowFence-Lite. Version v1 revises the initial skeleton into a fuller AAAI-style draft with expanded problem framing, method description, benchmark setup, results interpretation, limitations, tables, and bibliography.

The draft is not camera-ready and is not integrated into any existing EMNLP paper directory. It uses committed evidence tables, claims, and standalone draft artifacts only. Raw traces, raw provider outputs, prompts, event JSONL, policy JSONL, per-run metrics, credentials, and secrets are not included.

MiniMax is the only real provider represented. All MiniMax claims are scoped to MiniMax-backed synthetic-runtime evidence. Human review is required before submission or integration into another paper tree.

Key files:

- `main.tex`
- `sections/*.tex`
- `tables/*.tex`
- `figures/README.md`
- `references.bib`
- `claim_traceability.md`
- `open_review_risks.md`
- `compile_notes.md`

Version v1 keeps the official AAAI-27 style files copied from the downloaded author kit and does not modify `papers/emnlp2026_flowfence/`.

The current local environment does not provide `latexmk`, `pdflatex`, or `bibtex`, so compile status is source-only until checked in a LaTeX-capable environment.
