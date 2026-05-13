# EMNLP 2026 / ARR Draft

This directory contains an EMNLP/ARR-oriented rewrite of the FlowFence paper.

## Source Requirements

- EMNLP 2026 main conference submissions go through ARR.
- Long papers are up to 8 pages of content, with unlimited references and a required `Limitations` section.
- The draft uses the official ACL style files from `acl-org/acl-style-files`.
- The downloaded template zip is stored at `papers/templates/acl-style-files-master.zip`.

## Files

- `main.tex`: EMNLP/ARR draft rewritten around LLM agents, retrieval-memory poisoning, ReAct containment, and paraphrase robustness.
- `acl.sty`: official ACL style file copied from the template zip.
- `acl_natbib.bst`: official ACL bibliography style copied from the template zip.
- `custom.bib`: current bibliography copied from the ICDE draft; it still needs an EMNLP-focused citation cleanup pass.
- `flowfence_architecture.png`: current FlowFence architecture figure reused from the ICDE draft.

## Current Caveats

- This is a first venue-reframing draft, not a submission-ready version.
- Bibliography entries should be cleaned before submission, especially agent-safety entries that currently have incomplete author metadata.
- The draft has not been compiled locally because no LaTeX engine is installed in the current environment.
- Before submission, check ARR anonymization, Responsible NLP Checklist answers, limitations placement, and whether to add one more model/comparator experiment.
