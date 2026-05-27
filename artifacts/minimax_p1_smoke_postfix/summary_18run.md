# MiniMax P1 Post-Fix 18-Run Smoke

This is the clean post-debug MiniMax 18-run smoke after the final-writer prompt and utility-evaluator fixes. It is a small real-provider smoke, not a full real-model experiment.

## Matrix

- Provider: MiniMax
- Provider calls enabled: `true`
- Agent backend: `minimax_final_writer`
- Topologies: `chain_4`, `blackboard_4`
- Attacks: `none`, `summary_poisoning_indirect`, `workspace_poisoning_indirect`
- Defenses: `none`, `prompt_filter`, `flowfence_lite`
- Seed: `1`
- Expected runs: `18`

## Overall Results

- Completed runs: `18`
- Failed runs: `0`
- Task success rate: `0.888889`
- Unauthorized raw leakage mean: `4.111111`
- External leakage mean: `0.444444`
- Cascade size mean: `3.333333`
- Cascade depth mean: `2.666667`
- Privilege reach mean: `2.222222`
- Topology effect observed: `true`

## Defense Slices

| defense | run count | task success | raw leakage | external leakage | cascade size | privilege reach |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `flowfence_lite` | 6 | 1.0 | 0.0 | 0.0 | 2.0 | 0.0 |
| `none` | 6 | 1.0 | 5.0 | 0.333333 | 4.0 | 3.333333 |
| `prompt_filter` | 6 | 0.666667 | 7.333333 | 1.0 | 4.0 | 3.333333 |

## FlowFence Comparisons

- Versus no defense on unauthorized raw leakage: improves `4/6`, ties `2/6`, underperforms `0/6`.
- Versus no defense on external leakage: improves `2/6`, ties `4/6`, underperforms `0/6`.
- Versus prompt filter on unauthorized raw leakage: improves `4/6`, ties `2/6`, underperforms `0/6`.
- Versus prompt filter on external leakage: improves `3/6`, ties `3/6`, underperforms `0/6`.

## Caveats

The overall task success rate is `0.888889`, lower than the prior debug smoke's `1.0`. The FlowFence-Lite subset remains at `1.0`, while the `prompt_filter` subset is `0.666667`. Treat this as official small post-fix smoke evidence plus a reason to inspect prompt-filter/no-defense task failures before broader MiniMax coverage.

Raw traces, prompts, provider outputs, event JSONL files, policy JSONL files, individual per-run `metrics.json` files, credentials, and secrets are intentionally not committed.
