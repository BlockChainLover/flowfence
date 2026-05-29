# Codex Task State: p1-claims-refresh-5

## Goal

Refresh the evidence index, claims checklist, and evidence-boundary documentation after the successful non-oracle held-out FlowFence validation.

## Branch

`codex/p1-claims-refresh-5`

## Inputs Inspected

- `AGENTS.md`
- `results/evidence_index/current_evidence_index.md`
- `papers/claims_checklist.md`
- `artifacts/evidence_index/p1_claims_refresh_4.md`
- `artifacts/paper_drafts/results_section_open_risks.md`
- `artifacts/paper_drafts/results_section_claim_traceability.md`
- `artifacts/nonoracle_heldout_deterministic/README.md`
- `artifacts/nonoracle_heldout_deterministic/run_manifest.json`
- `artifacts/nonoracle_heldout_deterministic/summary.json`
- `artifacts/nonoracle_heldout_deterministic/summary.md`
- `artifacts/nonoracle_heldout_deterministic/comparison_by_defense.csv`
- `artifacts/nonoracle_heldout_deterministic/comparison_by_attack_defense.csv`
- `artifacts/nonoracle_heldout_deterministic/nonoracle_oracle_delta.csv`
- `artifacts/nonoracle_heldout_deterministic/ablation_summary.csv`
- `artifacts/minimax_nonoracle_heldout_targeted/README.md`
- `artifacts/minimax_nonoracle_heldout_targeted/run_manifest.json`
- `artifacts/minimax_nonoracle_heldout_targeted/summary.json`
- `artifacts/minimax_nonoracle_heldout_targeted/summary.md`
- `artifacts/minimax_nonoracle_heldout_targeted/comparison_by_defense.csv`
- `artifacts/minimax_nonoracle_heldout_targeted/comparison_by_attack_defense.csv`
- `artifacts/codex_task_state/codex_p1_nonoracle_heldout_ablation.md`

## Completed

- Added non-oracle held-out validation evidence to the current evidence index.
- Added claim rows for oracle-signal diagnosis, non-oracle deterministic validation, targeted MiniMax validation, and no-semantic-pattern ablation.
- Created `artifacts/evidence_index/p1_claims_refresh_5.md`.
- Updated non-oracle deterministic and targeted MiniMax README claim-use notes.
- Updated paper draft open risks and claim traceability.

## Changed Files

- `results/evidence_index/current_evidence_index.md`
- `papers/claims_checklist.md`
- `artifacts/evidence_index/p1_claims_refresh_5.md`
- `artifacts/nonoracle_heldout_deterministic/README.md`
- `artifacts/minimax_nonoracle_heldout_targeted/README.md`
- `artifacts/paper_drafts/results_section_open_risks.md`
- `artifacts/paper_drafts/results_section_claim_traceability.md`
- `artifacts/codex_task_state/codex_p1_claims_refresh_5.md`

## Validation Commands

- `git diff --check`
- `python -m compileall scripts src`
- `git status --short`

## Claim Status Changes

- The oracle-annotation risk is now recorded as an addressed internal-validity limitation.
- Deterministic non-oracle held-out validation supports a clean `flowfence_lite_nonoracle` subset across 540/540 configured runs.
- Targeted MiniMax-backed synthetic-runtime validation supports a clean `flowfence_lite_nonoracle` subset across 72/72 configured runs.
- The no-semantic-pattern ablation is recorded as evidence that semantic pattern detection contributes to raw-leakage containment while policy, fanout, and safe-view mechanisms still matter.

## Known Limitations

- MiniMax remains the only real provider.
- The targeted MiniMax validation is synthetic-runtime with MiniMax final writer, not real browser/desktop/computer-use evidence.
- The held-out support is limited to configured paraphrase attacks.
- Arbitrary attack robustness, production safety, and non-MiniMax generalization remain unsupported.

## Resume Instructions

Next goal should refresh paper-facing tables to include the non-oracle held-out deterministic and targeted MiniMax validation before revising the Results section.
