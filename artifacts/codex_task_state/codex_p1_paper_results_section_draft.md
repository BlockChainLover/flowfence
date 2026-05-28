# Codex Task State: p1-paper-results-section-draft

## Goal

Draft a standalone paper-facing Results section from reviewed evidence tables and claims. The draft is conservative, evidence-bound, and explicitly separates P0 adapted AgentPoison evidence, P1 deterministic synthetic evidence, and P1 MiniMax-backed synthetic-runtime coverage evidence.

## Branch

`codex/p1-paper-results-section-draft`

## Inputs Inspected

- `AGENTS.md`
- `research/contract/`
- `research/logs/roadmap.md`
- `research/logs/progress.md`
- `results/evidence_index/current_evidence_index.md`
- `papers/claims_checklist.md`
- `artifacts/evidence_index/p1_claims_refresh_4.md`
- `artifacts/codex_task_state/codex_p1_claims_refresh_4.md`
- `artifacts/paper_tables/README.md`
- `artifacts/paper_tables/paper_tables_summary.json`
- `artifacts/paper_tables/paper_tables_summary.md`
- `artifacts/paper_tables/table_1_p0_agentpoison.md`
- `artifacts/paper_tables/table_2_p1_synthetic.md`
- `artifacts/paper_tables/table_3_minimax_3seed_coverage.md`
- `artifacts/paper_tables/table_4_claims_matrix.md`
- `artifacts/paper_tables/table_5_evidence_boundaries.md`
- `artifacts/paper_tables/table_6_minimax_3seed_seed_stability.md`
- `artifacts/paper_tables_review/table_review_report.json`
- `artifacts/paper_tables_review/table_review_report.md`
- `artifacts/minimax_p1_coverage_3seed/README.md`
- `artifacts/minimax_p1_coverage_3seed/run_manifest.json`
- `artifacts/minimax_p1_coverage_3seed/coverage_summary.json`
- `artifacts/minimax_p1_coverage_3seed/coverage_summary.md`
- `artifacts/minimax_p1_coverage_3seed/coverage_by_defense.md`
- `artifacts/minimax_p1_coverage_3seed/coverage_by_topology.md`
- `artifacts/minimax_p1_coverage_3seed/coverage_by_attack.md`
- `artifacts/minimax_p1_coverage_3seed/coverage_by_attack_defense.md`
- `artifacts/minimax_p1_coverage_3seed/coverage_by_seed.md`
- `artifacts/minimax_p1_coverage_3seed/flowfence_clean_matrix.md`

## Completed

- Created a Markdown Results draft.
- Created a LaTeX-ready snippet that is not integrated into `main.tex`.
- Created a claim-traceability table mapping key Results claims to evidence, allowed wording, and forbidden wording.
- Created an open-risks document for paper integration.
- Created this durable task-state file.
- Did not run experiments, call providers, inspect raw traces, or modify `main.tex`.

## Draft Artifacts

- `artifacts/paper_drafts/README.md`
- `artifacts/paper_drafts/results_section_v1.md`
- `artifacts/paper_drafts/results_section_latex_snippet.tex`
- `artifacts/paper_drafts/results_section_claim_traceability.md`
- `artifacts/paper_drafts/results_section_open_risks.md`

## Validation Commands

- `git diff --check`
- `python -m compileall scripts src`
- `git status --short`

## Known Limitations

- The draft is not integrated into `main.tex`.
- The draft uses committed high-level evidence tables and summaries only.
- The draft preserves the MiniMax-only and synthetic-runtime caveats.
- The draft does not support non-MiniMax generalization, production safety, real browser/desktop/computer-use deployment evidence, official AgentPoison reproduction, or learned graph risk scorer claims.
- Human review is required before paper integration.

## Resume Instructions

Recommended next goal: `p1-experiment-gap-analysis`.

Before integrating the Results draft into a manuscript, review whether the current evidence package is sufficient or whether additional experiments, ablations, or baseline clarifications are needed.
