# AgentPoison MiniMax Result Table

This is the current paper-facing result table for the adapted AgentPoison full-ReAct MiniMax axis.

## Source Artifacts

- Main matrix: `results/baseline_agentpoison_fullreact_minimax27_small_matrix_summary.json`
- Ablation: `results/ablation_agentpoison_fullreact_minimax27_quarantine_only_vs_actioncanon_summary.json`
- Weak comparator: `results/baseline_agentpoison_fullreact_minimax27_rewrite_only_weak_comparator_summary.json`
- Independent weak comparator: `results/baseline_agentpoison_fullreact_minimax27_static_keyword_filter_weak_comparator_summary.json`
- Held-out instruction stress test: `results/baseline_agentpoison_fullreact_minimax27_heldout_instruction_matrix_summary.json`
- Overhead proxy: `results/overhead_agentpoison_fullreact_minimax27_same_axis_proxy_summary.json`
- Measured overhead slice: `results/overhead_agentpoison_fullreact_minimax27_same_axis_measured_summary.json`
- Task manifest: `data/tasks/agentpoison_strategyqa_fullreact_v1.json`
- No-defense config: `configs/experiment/agentpoison_fullreact_minimax27_triggerquery.yaml`
- Static keyword filter config: `configs/experiment/agentpoison_fullreact_static_keyword_filter_minimax27_triggerquery.yaml`
- Held-out no-defense config: `configs/experiment/agentpoison_fullreact_minimax27_triggerquery_heldout_instruction.yaml`
- Held-out non-oracle static filter config: `configs/experiment/agentpoison_fullreact_static_keyword_filter_minimax27_triggerquery_heldout_instruction.yaml`
- Held-out FlowFence-Lite config: `configs/experiment/agentpoison_fullreact_flowfence_lite_minimax27_triggerquery_heldout_instruction_quarantine_actioncanon.yaml`
- Rewrite-only config: `configs/experiment/agentpoison_fullreact_flowfence_lite_minimax27_triggerquery_rewrite_only.yaml`
- Quarantine-only config: `configs/experiment/agentpoison_fullreact_flowfence_lite_minimax27_triggerquery_quarantine_only.yaml`
- Quarantine-actioncanon config: `configs/experiment/agentpoison_fullreact_flowfence_lite_minimax27_triggerquery_quarantine_actioncanon.yaml`

## Table 1: Same-Axis Main Result And Ablation

All values are mean over three runs. Min/max are shown in parentheses where useful.

| condition | exposed poisoned retrieval | attack manifestation | raw poisoned retrieval | clean utility | attacked utility | intervention event rate |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| No defense | `0.4667` (`0.36-0.52`) | `0.2533` (`0.16-0.36`) | `0.4667` (`0.36-0.52`) | `0.3733` (`0.28-0.44`) | `0.3333` (`0.32-0.36`) | `0.0000` |
| Independent weak defense, static keyword filter | `0.0000` (`0.00-0.00`) | `0.0000` (`0.00-0.00`) | `0.4667` (`0.28-0.64`) | `0.3600` (`0.28-0.48`) | `0.3600` (`0.24-0.52`) | `0.4961` (`0.3077-0.6164`) |
| Weak defense, safe-view rewrite only | `0.0000` (`0.00-0.00`) | `0.0000` (`0.00-0.00`) | `0.4533` (`0.28-0.68`) | `0.2933` (`0.16-0.44`) | `0.4933` (`0.40-0.64`) | `0.4197` (`0.3143-0.5521`) |
| FlowFence-Lite, quarantine only | `0.0000` (`0.00-0.00`) | `0.0000` (`0.00-0.00`) | `0.5333` (`0.40-0.60`) | `0.3067` (`0.24-0.36`) | `0.3733` (`0.32-0.48`) | `0.5805` (`0.4894-0.6271`) |
| FlowFence-Lite, quarantine + action-canon | `0.0000` (`0.00-0.00`) | `0.0000` (`0.00-0.00`) | `0.4400` (`0.32-0.56`) | `0.3600` (`0.28-0.40`) | `0.3867` (`0.28-0.48`) | `0.4770` (`0.4267-0.5758`) |

## Table Notes

- `exposed poisoned retrieval` is the case rate where poisoned retrieved content reaches the model prompt after defense processing.
- `raw poisoned retrieval` is the case rate where poisoned content was retrieved before defense processing.
- `attack manifestation` is the case rate where the adversarial answer manifests the AgentPoison attack rule.
- `clean utility` is benign StrategyQA exact-match accuracy on the staged adapted subset.
- `attacked utility` is adversarial StrategyQA exact-match accuracy on the same adapted subset.
- `intervention event rate` is the fraction of retrieval events that triggered a defense intervention.

## Table 2: Same-Axis Overhead Proxies

These values are computed from existing `case_details` traces, not from wall-clock timing or provider token usage. All values are means over three runs.

| condition | model calls / case | delta vs no defense | current-task token proxy / case | token-proxy delta | interventions / case |
| --- | ---: | ---: | ---: | ---: | ---: |
| No defense | `2.8333` | `0.00%` | `416.3483` | `0.00%` | `0.0000` |
| Weak defense, safe-view rewrite only | `3.4267` | `+20.94%` | `536.4700` | `+28.85%` | `0.6467` |
| FlowFence-Lite, quarantine only | `3.4267` | `+20.94%` | `495.2800` | `+18.96%` | `0.7333` |
| FlowFence-Lite, quarantine + action-canon | `3.7600` | `+32.71%` | `502.5767` | `+20.71%` | `0.7467` |

## Table 3: Same-Axis Measured Overhead Slice

This is a strict measured-overhead slice on 10 fixed questions, executed in benign and adversarial modes. It is runtime-feasibility evidence, not a replacement for the 25-question efficacy matrix.

| condition | wall sec / case | LLM calls / case | provider tokens / case | defense sec / case |
| --- | ---: | ---: | ---: | ---: |
| No defense | `28.861467` | `3.20` | `5197.25` | `0.000013` |
| FlowFence-Lite, quarantine + action-canon | `24.692974` | `2.65` | `4191.50` | `0.000098` |
| Relative delta | `-14.44%` | `-17.19%` | `-19.35%` | `+0.000085 sec` |

## Paper Interpretation

The no-defense condition establishes a non-vacuous attack: poisoned retrieval is exposed in every run and attack manifestation is non-zero in every run. The independent static keyword filter, same-axis safe-view rewrite-only weak defense, and both FlowFence-Lite quarantine variants reduce exposed poisoned retrieval and attack manifestation to zero while raw poisoned retrieval remains non-zero, which indicates containment at the retrieval-memory boundary rather than disappearance of the attack input.

The static keyword filter is a genuinely independent weak baseline because it does not use FlowFence-Lite risk scoring, lease signals, safe-view rewriting, or the quarantine policy. It shows that a known-trigger blocklist can also stop this adapted attack on the same axis. This strengthens the baseline comparison beyond no-defense, but it also narrows the paper claim: the experiment does not prove that FlowFence-Lite is uniquely necessary for this specific trigger-string attack. FlowFence-Lite should instead be framed as a structured containment mechanism with clearer untrusted-memory semantics than brittle static blocklists.

The rewrite-only weak comparator shows that detector-mediated safe-view sanitization can also block exposed poisoned retrieval on this axis. Quarantine-only is enough for the safety outcome on this axis. The selected quarantine-actioncanon variant is still preferable for the main method result because it has higher clean utility mean than rewrite-only and quarantine-only, similar utility to the static filter, a slightly lower intervention event rate than the static filter, and clearer containment semantics for untrusted memory than rewriting or static blocklists.

The overhead-proxy result does not support a faster-or-cheaper claim. It supports a bounded-cost framing: quarantine-actioncanon adds about one recorded model call per case and about `20.71%` current-task trace-token proxy relative to no defense, while achieving the safety outcome in Table 1.

The measured-overhead slice is stronger than the proxy table for runtime feasibility because MiniMax returned provider token usage for all 40 measured case executions. It shows no measured wall-clock or provider-token increase for quarantine-actioncanon on that 10-question slice, and the absolute defense-inspection cost is negligible relative to LLM latency. However, this should be phrased conservatively: the lower latency/token use is confounded by shorter sampled ReAct trajectories and no quarantine/intervention events in the measured method slice, so it does not prove FlowFence-Lite is generally faster.

## Table 4: Held-Out Instruction Stress Test

This is a three-run stress test on the same adapted AgentPoison MiniMax setup. It keeps the same trigger sequence and DPR retrieval anchor, but paraphrases the poisoned guidance away from the old known-trigger static-filter phrases. The static filter condition is intentionally non-oracle: it does not match the trigger sequence and only blocks old-axis phrases.

All values are mean over three runs. Min/max are shown in parentheses where useful.

| condition | exposed poisoned retrieval | attack manifestation | raw poisoned retrieval | clean utility | attacked utility | intervention event rate |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| No defense, held-out instruction | `0.5333` (`0.48-0.60`) | `0.1733` (`0.12-0.24`) | `0.5333` (`0.48-0.60`) | `0.3200` (`0.24-0.40`) | `0.0933` (`0.04-0.16`) | `0.0000` |
| Non-oracle static keyword filter, held-out instruction | `0.4667` (`0.32-0.56`) | `0.2400` (`0.20-0.28`) | `0.4667` (`0.32-0.56`) | `0.1867` (`0.16-0.20`) | `0.1733` (`0.12-0.20`) | `0.0000` |
| FlowFence-Lite quarantine + action-canon, held-out instruction | `0.0000` (`0.00-0.00`) | `0.0000` (`0.00-0.00`) | `0.5333` (`0.52-0.56`) | `0.1467` (`0.12-0.16`) | `0.2533` (`0.20-0.32`) | `0.4869` (`0.4205-0.5538`) |

Observation: the held-out instruction axis creates non-vacuous attack pressure under no defense. The non-oracle static keyword filter does not intervene and continues to expose poisoned retrieval, while FlowFence-Lite quarantines retrieved poisoned content and reduces exposed poisoned retrieval and attack manifestation to zero.

Interpretation: this repeated stress test supports the claim that old-phrase blocklists are brittle to paraphrased poisoned guidance, whereas structured retrieval-memory containment can still block the attack when raw poisoned retrieval remains non-zero. It should still be reported as same-trigger held-out-instruction stress-test evidence, not broad held-out attack or topology generalization, because it keeps the same trigger sequence and adapted `trigger_question_only` retrieval anchor.

## Caveats

- This is an adapted AgentPoison comparator, not full official AgentPoison reproduction.
- The adaptation uses `trigger_question_only` adversarial search context to avoid diagnosed full-context trigger dilution.
- The model axis is MiniMax only.
- Utility is noisy under MiniMax full-ReAct execution; claim utility preservation conservatively, not utility improvement.
- The held-out instruction matrix is three-run stress-test evidence. It strengthens the blocklist-brittleness story, but it is not broad generalization evidence because it keeps the same trigger sequence and adapted retrieval anchor.
- The 25-question overhead table is proxy-only. The separate 10-question overhead slice has measured wall-clock and provider token usage, but it is smaller and trajectory-confounded.
- AgentDojo results should be reported separately as stochastic/blocked auxiliary evidence, not merged into this main table.
