# Codex Task State: aaai27-draft-v1-revision

## Goal

Revise the standalone anonymous AAAI-27 FlowFence-Lite draft from v0 to v1 using committed high-level evidence, reviewed tables, claims, and the official AAAI-27 template already downloaded. Do not modify EMNLP paper files, implementation code, configs, raw results, or research logs.

## Branch

- Branch: `codex/aaai27-draft-v1-revision`

## Inputs Inspected

- `AGENTS.md`
- `research/logs/roadmap.md`
- `research/logs/progress.md`
- `papers/aaai27_flowfence_draft/README.md`
- `papers/aaai27_flowfence_draft/main.tex`
- `papers/aaai27_flowfence_draft/sections/*.tex`
- `papers/aaai27_flowfence_draft/tables/*.tex`
- `papers/aaai27_flowfence_draft/references.bib`
- `papers/aaai27_flowfence_draft/claim_traceability.md`
- `papers/aaai27_flowfence_draft/open_review_risks.md`
- `papers/aaai27_flowfence_draft/compile_notes.md`
- `results/evidence_index/current_evidence_index.md`
- `papers/claims_checklist.md`
- `artifacts/evidence_index/p1_claims_refresh_5.md`
- `artifacts/paper_tables/table_1_p0_agentpoison.md`
- `artifacts/paper_tables/table_2_p1_synthetic.md`
- `artifacts/paper_tables/table_3_minimax_3seed_coverage.md`
- `artifacts/paper_tables/table_4_claims_matrix.md`
- `artifacts/paper_tables/table_5_evidence_boundaries.md`
- `artifacts/paper_tables/table_6_minimax_3seed_seed_stability.md`
- `artifacts/paper_tables/table_7_nonoracle_heldout_validation.md`
- `artifacts/paper_tables/table_8_nonoracle_mechanism_ablation.md`
- `artifacts/paper_tables_review/table_review_report.md`
- `artifacts/paper_drafts/results_section_v2.md`
- `artifacts/paper_drafts/results_section_v2_claim_traceability.md`
- `artifacts/paper_drafts/results_section_v2_open_risks.md`
- Read-only method/code context: `src/defenses/mas_flowfence.py`, `src/runtime/orchestrator.py`, `src/runtime/events.py`, `src/runtime/policy.py`, and evaluator files.

## Main Revisions

- Expanded abstract and introduction into a clearer AAAI-style argument about privacy leakage as runtime propagation rather than final-output-only leakage.
- Strengthened problem definition with formal system notation, policy model, threat channels, metrics, and out-of-scope boundaries.
- Strengthened method section with an event-interception pipeline, risk-signal table, safe-view/quarantine policies, privilege/fanout signals, non-oracle variant, no-semantic-pattern ablation, and pseudo-code.
- Added `table_experiment_matrix.tex` and `table_risk_signals.tex`.
- Revised benchmark setup to separate P0 adapted AgentPoison, deterministic synthetic MAS, MiniMax 252-run coverage, deterministic non-oracle validation, and targeted MiniMax non-oracle validation.
- Revised results and analysis around Table 3 canonical MiniMax coverage, Table 7 non-oracle held-out validation, and Table 8 mechanism ablation.
- Strengthened limitations and evidence-boundary language.
- Updated README, figure placeholder notes, claim traceability, open review risks, compile notes, and bibliography.

## Bibliography Status

- Reference count: 10.
- Placeholder anonymous references remaining: 0.
- Remaining TODO citations in related work: 0.
- Metadata was checked against arXiv/ACL Anthology pages where available, but final venue/camera-ready formatting should still be reviewed manually.

## Compile Check

- `latexmk` availability checked.
- `pdflatex` availability checked.
- Compile not attempted because neither executable is available in the local environment.
- Compile status recorded in `papers/aaai27_flowfence_draft/compile_notes.md`.

## Known Limitations

- The draft remains source-only until compiled in a LaTeX-capable environment.
- Tables and float placement require visual review after compilation.
- Figure 1 is currently a text placeholder, not a final vector diagram.
- Evidence remains MiniMax-only and synthetic-runtime scoped.
- No production safety, non-MiniMax generalization, real browser/desktop/computer-use evidence, arbitrary attack robustness, official AgentPoison reproduction, learned graph scorer, or human-user study is claimed.

## Resume Instructions

1. Compile `papers/aaai27_flowfence_draft/main.tex` in an environment with `latexmk` or `pdflatex`.
2. Fix table width, float placement, and citation formatting errors if compilation fails.
3. Replace the Figure 1 text placeholder with a clean vector diagram if the draft is moving toward review.
4. Run a focused bibliography cleanup if venue metadata needs polishing.
