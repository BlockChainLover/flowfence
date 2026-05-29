# Codex Task State: p1-results-section-revise-after-nonoracle

## Goal

Revise the standalone paper Results section after the successful non-oracle held-out FlowFence validation and refreshed paper-facing tables. The revised draft incorporates Tables 7 and 8, explains the oracle-annotation risk and non-oracle mitigation, and keeps claims scoped to MiniMax-backed synthetic-runtime evidence.

## Branch

`codex/p1-results-section-revise-after-nonoracle`

## Inputs Inspected

- `AGENTS.md`
- `results/evidence_index/current_evidence_index.md`
- `papers/claims_checklist.md`
- `artifacts/evidence_index/p1_claims_refresh_5.md`
- `artifacts/paper_drafts/README.md`
- `artifacts/paper_drafts/results_section_v1.md`
- `artifacts/paper_drafts/results_section_latex_snippet.tex`
- `artifacts/paper_drafts/results_section_claim_traceability.md`
- `artifacts/paper_drafts/results_section_open_risks.md`
- `artifacts/paper_tables/README.md`
- `artifacts/paper_tables/paper_tables_summary.md`
- `artifacts/paper_tables/table_1_p0_agentpoison.md`
- `artifacts/paper_tables/table_2_p1_synthetic.md`
- `artifacts/paper_tables/table_3_minimax_3seed_coverage.md`
- `artifacts/paper_tables/table_4_claims_matrix.md`
- `artifacts/paper_tables/table_5_evidence_boundaries.md`
- `artifacts/paper_tables/table_6_minimax_3seed_seed_stability.md`
- `artifacts/paper_tables/table_7_nonoracle_heldout_validation.md`
- `artifacts/paper_tables/table_8_nonoracle_mechanism_ablation.md`
- `artifacts/paper_tables_review/table_review_report.md`
- `artifacts/codex_task_state/codex_p1_nonoracle_heldout_ablation.md`

## Completed

- Created a revised standalone Results draft with RQ6 and RQ7 for non-oracle validation and mechanism ablation.
- Created a revised LaTeX-ready snippet with placeholders for Tables 1-8.
- Created a v2 claim traceability table.
- Created a v2 open-risks file.
- Created a v1-to-v2 change log.
- Updated the paper draft README to reference v2 artifacts.
- Did not modify `main.tex`.

## Draft Artifacts

- `artifacts/paper_drafts/results_section_v2.md`
- `artifacts/paper_drafts/results_section_v2_latex_snippet.tex`
- `artifacts/paper_drafts/results_section_v2_claim_traceability.md`
- `artifacts/paper_drafts/results_section_v2_open_risks.md`
- `artifacts/paper_drafts/results_section_v1_to_v2_change_log.md`

## Validation Commands

- `git diff --check`
- `python -m compileall scripts src`
- `git status --short`

## Known Limitations

- MiniMax is the only real provider represented.
- P1 evidence remains synthetic deterministic MAS runtime evidence.
- MiniMax is used as final writer, not as a full autonomous browser/desktop/computer-use stack.
- Non-oracle held-out validation covers configured paraphrase attacks only.
- Non-MiniMax generalization, production safety, real browser/desktop/computer-use evidence, arbitrary attack robustness, official AgentPoison reproduction, learned graph risk scoring, and human-user claims remain unsupported.

## Resume Instructions

If continuing, review `results_section_v2.md`, `results_section_v2_latex_snippet.tex`, and `results_section_v2_claim_traceability.md` before integrating any text into `main.tex`. The likely next goal is paper-results integration or adding redacted qualitative case studies if the human wants examples first.
