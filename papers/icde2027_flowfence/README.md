# ICDE 2027 FlowFence-Lite Draft

This directory contains an ICDE-oriented LaTeX draft based on the IEEE conference template in `papers/conference-latex-template.zip`.

## Files

- `main.tex`: ICDE-facing draft.
- `references.bib`: draft citation database. Author fields still need cleanup before submission.
- `IEEEtran.cls`: copied from the provided IEEE template.
- `figures/flowfence_architecture.png`: selected architecture figure copied from `papers/figures/FlowFence_figure_v1.png`. This is the current Figure 1 because it shows the full runtime containment boundary, before/after contrast, quarantine path, protected path, and normalized writeback path.

## ICDE Scope Framing

The draft frames FlowFence-Lite as a data engineering system for agentic retrieval pipelines:

- vector/retrieval data management,
- data provenance and workflow auditability,
- data quality and curation for poisoned memory,
- responsible data management,
- data security and privacy,
- foundation models for data engineering.

The draft deliberately avoids unsupported claims about broad multi-domain generalization, topology sensitivity, or full official AgentPoison reproduction. The main claim is scoped to runtime containment before prompt construction on the adapted AgentPoison MiniMax retrieval-memory axis.

## Current Revision Notes

- The explicit claims table was removed because it looked unlike a mature top-conference paper.
- Claims are now stated in prose and tied to Q1--Q4 in the evaluation section.
- The draft was expanded with a fuller problem model, design principles, mechanism discussion, failure modes, and stronger data-management related work.
- The 2026-05-07 revision removes repository-internal paths from the paper body and replaces them with a paper-facing experimental design table.
- The evaluation now presents AgentPoison as the main memory-poisoning baseline axis, then adds static-filter and rewrite-only comparators, quarantine/action-canonicalization ablations, held-out poisoned-instruction stress test, overhead proxies, measured overhead slice, and AgentDojo as a complementary benchmark axis.
- Result tables now report the main three-run matrix with min--max ranges and a fuller held-out stress-test table with utility/intervention metrics.

## Submission Notes

- ICDE 2027 research papers use IEEE format.
- Research and EAB papers must not exceed 12 pages excluding references and AI-generated content acknowledgement.
- No appendix is allowed.
- The final submission needs ORCIDs, artifact availability, COI checks, and an AI-generated content disclosure if applicable.
