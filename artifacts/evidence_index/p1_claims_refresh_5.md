# P1 Claims Refresh 5

## Inputs inspected

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

## What changed since p1-claims-refresh-4

The project added a non-oracle held-out validation goal after the 252-run MiniMax coverage. That goal diagnosed an internal-validity risk in the default `flowfence_lite` path, added `flowfence_lite_nonoracle`, added a no-semantic-pattern ablation, added held-out paraphrase attacks, and produced both deterministic and targeted MiniMax high-level summaries.

## Oracle-signal risk diagnosis

The default FlowFence path used `attack_annotation.applied` inside `src/defenses/mas_flowfence.py` by OR-ing it into the poison signal. `src/runtime/orchestrator.py` passed attack annotations during seed defense and final-send defense. This is now recorded as an internal-validity risk in the evidence index and claims checklist.

## Non-oracle FlowFence validation

`flowfence_lite_nonoracle` ignores `attack_annotation.applied`, `attack_id`, `attack_mode`, and oracle attack labels. Its decision metadata records `oracle_annotation_used=false`.

Deterministic validation:

- Expected/completed/failed: 540/540/0
- `flowfence_lite_nonoracle task_success_rate=1.0`
- `flowfence_lite_nonoracle unauthorized_raw_leakage_mean=0.0`
- `flowfence_lite_nonoracle external_leakage_mean=0.0`
- Oracle annotation violation count: 0
- Versus no-defense: raw improves 81/ties 9; external improves 81/ties 9; no underperforms.
- Versus static ACL: raw improves 66/ties 24; external improves 48/ties 42; no underperforms.
- Versus prompt-filter: raw improves 54/ties 36; external improves 54/ties 36; no underperforms.

Targeted MiniMax-backed synthetic-runtime validation:

- Expected/completed/failed: 72/72/0
- `flowfence_lite_nonoracle task_success_rate=1.0`
- `flowfence_lite_nonoracle unauthorized_raw_leakage_mean=0.0`
- `flowfence_lite_nonoracle external_leakage_mean=0.0`
- Oracle annotation violation count: 0
- Versus no-defense: raw improves 15/ties 3; external improves 10/ties 8; no underperforms.
- Versus static ACL: raw improves 15/ties 3; external improves 9/ties 9; no underperforms.
- Versus prompt-filter: raw improves 16/ties 2; external improves 10/ties 8; no underperforms.

## Held-out paraphrase attack validation

The deterministic held-out paraphrase subset produced baseline pressure: prompt-filter paraphrase failures=27 and no-defense leakage=81. The targeted MiniMax validation also showed baseline pressure while `flowfence_lite_nonoracle` kept raw and external leakage at 0.0.

## No-semantic-pattern ablation finding

The deterministic `flowfence_lite_nonoracle_no_semantic_patterns` ablation tied `flowfence_lite_nonoracle` on external leakage and task success but had higher raw leakage. Its raw leakage mean was `1.5` versus `0.0` for `flowfence_lite_nonoracle`. This suggests semantic pattern detection contributes to raw-leakage containment, while policy, fanout, and safe-view mechanisms still matter.

## Claims now supported

- The default FlowFence path had an oracle-annotation internal-validity risk.
- `flowfence_lite_nonoracle` avoids oracle attack annotations and records `oracle_annotation_used=false`.
- Deterministic non-oracle held-out validation supports a clean `flowfence_lite_nonoracle` subset across the configured 540-run matrix.
- Targeted MiniMax-backed synthetic-runtime validation supports a clean `flowfence_lite_nonoracle` subset across the configured 72-run held-out matrix.
- Non-oracle FlowFence improves or ties no-defense, static ACL, and prompt-filter on raw/external leakage in the configured held-out matrices.

## Claims partially supported

- Mechanism attribution is partially supported: semantic pattern detection appears useful for raw-leakage containment, but policy, fanout, and safe-view mechanisms still contribute. This should not be phrased as a full module ablation.
- Held-out robustness is supported for the configured paraphrase attacks only, not arbitrary paraphrases or adaptive attacks.

## Claims still unsupported

- Arbitrary attack robustness.
- Non-MiniMax generalization.
- Production safety.
- Real browser/desktop/computer-use evidence.
- Full official AgentPoison reproduction.
- Learned graph risk scorer.
- Broader real-world deployment.
- Claims that semantic detection is unnecessary.

## Current risk interpretation

The non-oracle held-out validation substantially mitigates the oracle-annotation concern for the configured held-out matrices. It strengthens the internal-validity story for the MiniMax-backed synthetic-runtime evidence, but it does not remove the MiniMax-only, synthetic-runtime, and non-production caveats.

## Recommended next goal

`p1-paper-tables-refresh-3`

Reason: the evidence package now includes non-oracle held-out deterministic and targeted MiniMax validation, so the paper-facing result tables should be refreshed before revising the Results section.
