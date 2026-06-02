# Codex Task State: aaai27-draft-v1-substantive-rewrite

## Goal

Perform a substantive AAAI-27 draft v1 rewrite of the standalone FlowFence-Lite paper using committed high-level evidence and the official AAAI-27 template. Do not modify EMNLP paper files, implementation code, configs, raw results, or research logs.

## Branch

- Branch: `codex/aaai27-draft-v1-substantive-rewrite`

## Inputs Inspected

- `AGENTS.md`
- `papers/aaai27_flowfence_draft/README.md`
- `papers/aaai27_flowfence_draft/main.tex`
- `papers/aaai27_flowfence_draft/compile_notes.md`
- `papers/aaai27_flowfence_draft/references.bib`
- `papers/aaai27_flowfence_draft/claim_traceability.md`
- `papers/aaai27_flowfence_draft/open_review_risks.md`
- `papers/aaai27_flowfence_draft/sections/*.tex`
- `papers/aaai27_flowfence_draft/tables/*.tex`
- `papers/aaai27_flowfence_draft/figures/README.md`
- `results/evidence_index/current_evidence_index.md`
- `papers/claims_checklist.md`
- `artifacts/evidence_index/p1_claims_refresh_5.md`
- `artifacts/paper_tables/table_3_minimax_3seed_coverage.md`
- `artifacts/paper_tables/table_5_evidence_boundaries.md`
- `artifacts/paper_tables/table_6_minimax_3seed_seed_stability.md`
- `artifacts/paper_tables/table_7_nonoracle_heldout_validation.md`
- `artifacts/paper_tables/table_8_nonoracle_mechanism_ablation.md`
- `artifacts/paper_tables_review/table_review_report.md`
- `artifacts/paper_drafts/results_section_v2.md`
- Read-only method context: `src/runtime/topology.py`, `src/attacks/summary_poisoning.py`, `src/attacks/workspace_poisoning.py`, `src/attacks/comm_hijack.py`

## Main Revisions

- Converted Figure 1 from a planned text note into a formal LaTeX figure placeholder using only `fbox`, `minipage`, and `tabular`.
- Added explicit risk scoring formula `r(e)=min(1,max(0,sum_i w_i f_i(e)))` to the method section.
- Added `table_seed_stability.tex` and integrated it into the Results section so Table 6 evidence is represented in the standalone draft.
- Expanded Results to explain why cascade size need not be zero, why raw/external leakage and privilege reach matter, and why improvements/ties are reported separately.
- Expanded Analysis with runtime design implications and a tie/improvement interpretation.
- Strengthened Limitations by explaining why raw traces and provider outputs are not committed.
- Added information-flow and least-privilege related work references.
- Updated README, figures README, claim traceability, open review risks, and compile notes.

## Bibliography Status

- BibTeX entries: 12.
- Placeholder `Anonymous and others` entries remaining: 0.
- Remaining TODO citations in related work: 0.
- Added classic information-flow/least-privilege references: Denning 1976 and Saltzer-Schroeder 1975.

## Compile Check

- `latexmk -pdf -interaction=nonstopmode main.tex` attempted.
- `pdflatex -interaction=nonstopmode main.tex` attempted.
- `bibtex main` attempted.
- All three commands failed before compilation with `command not found`.
- Static citation-key check found 12 cited keys, 12 BibTeX keys, 0 missing, and 0 unused.
- No PDF was produced or committed.

## Files Changed

- `papers/aaai27_flowfence_draft/README.md`
- `papers/aaai27_flowfence_draft/claim_traceability.md`
- `papers/aaai27_flowfence_draft/compile_notes.md`
- `papers/aaai27_flowfence_draft/figures/README.md`
- `papers/aaai27_flowfence_draft/open_review_risks.md`
- `papers/aaai27_flowfence_draft/references.bib`
- `papers/aaai27_flowfence_draft/sections/03_method.tex`
- `papers/aaai27_flowfence_draft/sections/05_results.tex`
- `papers/aaai27_flowfence_draft/sections/06_analysis.tex`
- `papers/aaai27_flowfence_draft/sections/07_related_work.tex`
- `papers/aaai27_flowfence_draft/sections/08_limitations.tex`
- `papers/aaai27_flowfence_draft/tables/table_seed_stability.tex`
- `artifacts/codex_task_state/codex_aaai27_draft_v1_substantive_rewrite.md`

## Known Limitations

- Local LaTeX compilation is unavailable, so page count, unresolved references, and overfull boxes cannot be checked locally.
- Figure 1 is a functional placeholder, not a polished vector figure.
- Evidence remains MiniMax-only and synthetic-runtime scoped.
- The draft does not claim production safety, real browser/desktop/computer-use deployment evidence, non-MiniMax generalization, arbitrary attack robustness, official AgentPoison reproduction, or learned graph risk scoring.

## Resume Instructions

1. Compile `papers/aaai27_flowfence_draft/main.tex` in a LaTeX-capable environment.
2. Check page count, unresolved citations/references, and overfull boxes over 5pt.
3. Polish Figure 1 into a vector diagram if the draft moves toward submission.
4. Perform final BibTeX venue formatting cleanup after compilation.
