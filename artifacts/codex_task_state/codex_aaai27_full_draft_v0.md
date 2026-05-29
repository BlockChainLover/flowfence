# Codex Task State: aaai27-full-draft-v0

## Goal

Create a standalone anonymous AAAI-27 paper draft v0 for FlowFence-Lite from committed evidence, claims, reviewed tables, and standalone Results draft artifacts. Do not modify the existing EMNLP paper files, implementation code, configs, raw results, or research logs.

## Branch

- Branch: `codex/aaai27-full-draft-v0`
- Base commit inspected: `52298a543816b9baedc4d0c14afdab98d5fc8e06`

## Author Kit Download

- Official AAAI source page: `https://aaai.org/conference/aaai/aaai-27/`
- Official author kit URL used: `https://aaai.org/authorkit27/`
- Download succeeded: yes
- Downloaded archive: `papers/aaai27_template/original_download/authorkit27.zip`
- Extracted directory: `papers/aaai27_template/extracted/AuthorKit27/`
- Style file found: `aaai2027.sty`
- Bibliography style found: `aaai2027.bst`
- Download notes: `papers/aaai27_template/DOWNLOAD_NOTES.md`

## Inputs Inspected

- `AGENTS.md`
- `results/evidence_index/current_evidence_index.md`
- `papers/claims_checklist.md`
- `artifacts/evidence_index/p1_claims_refresh_5.md`
- `artifacts/paper_drafts/results_section_v2.md`
- `artifacts/paper_drafts/results_section_v2_latex_snippet.tex`
- `artifacts/paper_drafts/results_section_v2_claim_traceability.md`
- `artifacts/paper_drafts/results_section_v2_open_risks.md`
- `artifacts/paper_tables/table_1_p0_agentpoison.md`
- `artifacts/paper_tables/table_2_p1_synthetic.md`
- `artifacts/paper_tables/table_3_minimax_3seed_coverage.md`
- `artifacts/paper_tables/table_4_claims_matrix.md`
- `artifacts/paper_tables/table_5_evidence_boundaries.md`
- `artifacts/paper_tables/table_6_minimax_3seed_seed_stability.md`
- `artifacts/paper_tables/table_7_nonoracle_heldout_validation.md`
- `artifacts/paper_tables/table_8_nonoracle_mechanism_ablation.md`
- `artifacts/paper_tables_review/table_review_report.md`
- `artifacts/nonoracle_heldout_deterministic/summary.md`
- `artifacts/minimax_nonoracle_heldout_targeted/summary.md`
- `artifacts/codex_task_state/codex_p1_results_section_revise_after_nonoracle.md`
- `research/contract/01_problem_definition.md`
- `research/contract/02_literature_survey.md`
- `research/contract/03_selected_idea_and_risks.md`
- `research/contract/04_baseline_and_experiment_plan.md`
- `research/contract/05_paper_claims_checklist.md`

## Draft Files Created

- `papers/aaai27_flowfence_draft/README.md`
- `papers/aaai27_flowfence_draft/main.tex`
- `papers/aaai27_flowfence_draft/sections/01_introduction.tex`
- `papers/aaai27_flowfence_draft/sections/02_problem.tex`
- `papers/aaai27_flowfence_draft/sections/03_method.tex`
- `papers/aaai27_flowfence_draft/sections/04_benchmark.tex`
- `papers/aaai27_flowfence_draft/sections/05_results.tex`
- `papers/aaai27_flowfence_draft/sections/06_analysis.tex`
- `papers/aaai27_flowfence_draft/sections/07_related_work.tex`
- `papers/aaai27_flowfence_draft/sections/08_limitations.tex`
- `papers/aaai27_flowfence_draft/sections/09_conclusion.tex`
- `papers/aaai27_flowfence_draft/tables/table_p0_agentpoison.tex`
- `papers/aaai27_flowfence_draft/tables/table_minimax_3seed.tex`
- `papers/aaai27_flowfence_draft/tables/table_nonoracle.tex`
- `papers/aaai27_flowfence_draft/tables/table_evidence_boundaries.tex`
- `papers/aaai27_flowfence_draft/references.bib`
- `papers/aaai27_flowfence_draft/compile_notes.md`
- `papers/aaai27_flowfence_draft/claim_traceability.md`
- `papers/aaai27_flowfence_draft/open_review_risks.md`

## Compile Check

- `latexmk` available: no
- `pdflatex` available: no
- Compile attempted: no
- Result recorded in `papers/aaai27_flowfence_draft/compile_notes.md`

## Validation Commands

- `command -v latexmk`
- `command -v pdflatex`
- `git diff --check`
- `python -m compileall scripts src`
- `git status --short`

## Known Limitations

- The draft is source-only until compiled in an environment with a LaTeX distribution.
- Bibliography entries are conservative placeholders and need human verification before submission.
- The draft remains anonymous and not camera-ready.
- Claims remain scoped to committed evidence: MiniMax-only real-provider evidence, synthetic deterministic MAS runtime, no production safety claim, no real browser/desktop/computer-use evidence, no arbitrary attack robustness, and no non-MiniMax generalization.
- Existing EMNLP paper files were not modified.

## Resume Instructions

1. Install or use a LaTeX environment with `latexmk` or `pdflatex`.
2. Compile from `papers/aaai27_flowfence_draft/`.
3. Replace placeholder bibliography metadata with verified citations.
4. Review AAAI anonymity and formatting requirements against the official author kit.
5. If compile errors are style/table related, create a focused `aaai27-latex-fix` goal.
