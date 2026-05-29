# Results Draft v1 to v2 Change Log

## Inputs added

- `artifacts/paper_tables/table_7_nonoracle_heldout_validation.md`
- `artifacts/paper_tables/table_8_nonoracle_mechanism_ablation.md`
- `artifacts/nonoracle_heldout_deterministic/summary.md`
- `artifacts/nonoracle_heldout_deterministic/comparison_by_defense.md`
- `artifacts/nonoracle_heldout_deterministic/nonoracle_oracle_delta.md`
- `artifacts/nonoracle_heldout_deterministic/ablation_summary.md`
- `artifacts/minimax_nonoracle_heldout_targeted/summary.md`
- `artifacts/minimax_nonoracle_heldout_targeted/comparison_by_defense.md`
- `artifacts/codex_task_state/codex_p1_nonoracle_heldout_ablation.md`

## Main claim changes

- Added the non-oracle validation result: `flowfence_lite_nonoracle` remains clean in the 540-run deterministic held-out matrix and the 72-run targeted MiniMax-backed synthetic-runtime validation.
- Added the mechanism-ablation result: disabling semantic patterns increases raw leakage in deterministic results while tying external leakage and task success.
- Clarified that the default `flowfence_lite` path had an oracle-annotation internal-validity risk and that v2 treats the non-oracle validation as the relevant mitigation.

## New RQs added

- RQ6: Does FlowFence-Lite still work without oracle attack annotations?
- RQ7: Which mechanism matters: semantic detection or policy/fanout/safe-view containment?

## Claims strengthened

- The internal-validity story is stronger because Table 7 shows zero oracle annotation violations for `flowfence_lite_nonoracle`.
- Held-out evidence is stronger because Table 7 includes configured paraphrased attacks under both deterministic and targeted MiniMax-backed synthetic-runtime validation.
- Mechanism discussion is stronger because Table 8 separates semantic pattern contribution from policy/fanout/safe-view behavior.

## Claims softened

- Held-out results are explicitly limited to configured paraphrases and do not support arbitrary attack robustness.
- Mechanism claims are framed as partial ablation evidence, not full component isolation.
- MiniMax-backed results remain synthetic-runtime evidence, not real-world deployment or production safety evidence.

## Remaining caveats

- MiniMax-only provider evidence.
- Synthetic deterministic MAS runtime.
- MiniMax final-writer path, not full autonomous real computer-use stack.
- No non-MiniMax generalization.
- No production safety.
- No real browser/desktop/computer-use evidence.
- No official AgentPoison reproduction.
- No arbitrary attack robustness.
- No learned graph risk scorer.

## Files created

- `artifacts/paper_drafts/results_section_v2.md`
- `artifacts/paper_drafts/results_section_v2_latex_snippet.tex`
- `artifacts/paper_drafts/results_section_v2_claim_traceability.md`
- `artifacts/paper_drafts/results_section_v2_open_risks.md`
- `artifacts/paper_drafts/results_section_v1_to_v2_change_log.md`

`paper main.tex` was not modified.
