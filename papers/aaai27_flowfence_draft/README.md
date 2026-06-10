# AAAI-27 FlowFence-Lite Draft - Method/Results Polish

This directory contains a standalone anonymous AAAI-27 draft for FlowFence-Lite. The current polish pass tightens the method, benchmark, results, analysis, limitations, and key tables while preserving the evidence boundaries from the committed artifacts. It keeps the draft focused on runtime-observable containment, MiniMax-backed synthetic-runtime evidence, and redacted safe-trace qualitative examples.

The draft is not camera-ready and is not integrated into any existing EMNLP paper directory. It uses committed evidence tables, claims, and high-level summary artifacts only. Raw traces, raw provider outputs, prompts, event JSONL, policy JSONL, per-run metrics, credentials, and secrets are not included.

MiniMax is the only real provider represented. All MiniMax claims are scoped to MiniMax-backed synthetic-runtime evidence. Human review is required before submission or integration into another paper tree.

## Safe-trace case-study integration

The draft now includes concise redacted safe-trace illustrations in the Analysis section. The source artifacts are under `artifacts/case_studies_safe_trace/`, including `redacted_case_studies_with_safe_traces.json` and four individual redacted case files. These are safe-trace illustrations, not raw traces, raw transcripts, provider outputs, production logs, or additional experiments.

Main-paper integration status:

- Cases 1 and 3 are integrated as a paired no-defense failure / FlowFence containment vignette.
- Case 4 is integrated as a non-oracle held-out validation vignette.
- Case 2 is mentioned as a prompt-filter paraphrase baseline note and remains appendix-level if space is tight.

Human review is still required before submission.

## Method/results polish status

The method section now presents the paper-facing defense as non-oracle and runtime-observable. The earlier attack-annotation signal is described as an engineering validity risk addressed by `flowfence_lite_nonoracle`, not as part of the final method. The results section now separates the canonical 252-run MiniMax-backed multi-agent synthetic-runtime coverage experiment from the targeted MiniMax-backed synthetic-runtime validation and explains why ties and non-zero cascade size are compatible with successful containment.

The analysis section uses the redacted safe-trace examples as short qualitative bridges from aggregate tables to event paths. The examples are explicitly scoped as redacted safe-trace illustrations, not raw transcripts, provider outputs, production logs, or additional experiments.

Several dense tables were compressed by shortening headers, replacing long monospaced identifiers with readable names, and moving caveats into captions/prose where possible.

Key files:

- `main.tex`
- `sections/*.tex`
- `tables/*.tex`
- `figures/flowfence_pipeline.png`
- `references.bib`
- `claims_results_coverage_audit.md`
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

After the method/results polish pass in this environment, `latexmk` and `pdflatex` were both unavailable, so no fresh PDF/page-count/layout warning check could be produced locally. See `compile_notes.md`.

## Claims/results coverage audit

`claims_results_coverage_audit.md` summarizes the current experiment results, maps claims to evidence artifacts, and records whether the AAAI draft includes each claim. It also records two deliberate presentation decisions: P0 overhead evidence remains traceable but not headline, and historical MiniMax smoke/84-run evidence is superseded by the 252-run MiniMax-backed multi-agent synthetic-runtime coverage experiment.
