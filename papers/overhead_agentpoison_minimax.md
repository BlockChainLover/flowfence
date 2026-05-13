# Same-Axis Overhead Proxy: AgentPoison MiniMax

## Source Artifact

- Summary: `results/overhead_agentpoison_fullreact_minimax27_same_axis_proxy_summary.json`
- Script: `src/runner/summarize_agentpoison_overhead_proxy.py`
- Axis: adapted AgentPoison full-ReAct MiniMax, `trigger_question_only`, `data/tasks/agentpoison_strategyqa_fullreact_v1.json`

## Measurement Status

This is an overhead-proxy analysis from existing saved traces. The original runs did not persist per-call wall-clock timestamps or provider token-usage fields. Therefore, this artifact should not be described as measured latency or measured token overhead.

The available proxies are:

- `model_call_count_per_case`: recorded `n_calls` from the full-ReAct runner; best available latency proxy.
- `actual_task_react_steps_per_case`: current-task ReAct action count, excluding fixed few-shot examples.
- `actual_task_trajectory_token_proxy_per_case`: current-task trajectory characters divided by four; coarse token proxy, not provider usage.
- `observation_char_delta_per_case`: defense-induced observation length change over retrieval events.

## Main Proxy Table

All values are means over three runs.

| condition | model calls / case | delta vs no defense | actual task steps / case | task token proxy / case | token-proxy delta | interventions / case | obs char delta / case |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| No defense | `2.8333` | `0.00%` | `2.2000` | `416.3483` | `0.00%` | `0.0000` | `0.00` |
| Weak defense, safe-view rewrite only | `3.4267` | `+20.94%` | `2.9333` | `536.4700` | `+28.85%` | `0.6467` | `-145.40` |
| FlowFence-Lite, quarantine only | `3.4267` | `+20.94%` | `3.0467` | `495.2800` | `+18.96%` | `0.7333` | `-247.87` |
| FlowFence-Lite, quarantine + action-canon | `3.7600` | `+32.71%` | `3.1733` | `502.5767` | `+20.71%` | `0.7467` | `-248.24` |

## Observations

All detector-mediated defenses add model-call overhead in the saved traces. The selected quarantine-actioncanon variant has the highest model-call proxy: `3.76` calls per case versus no-defense `2.8333`, a relative increase of `32.71%`.

The task-token proxy also increases for all defense variants. Quarantine-actioncanon increases from `416.3483` to `502.5767` proxy tokens per case, or `+20.71%`. Rewrite-only has the highest task-token proxy at `536.47`, or `+28.85%`.

Quarantine variants reduce retrieved-observation character exposure. Quarantine-actioncanon has mean observation character delta `-248.24` per case, and quarantine-only has `-247.87`; rewrite-only has `-145.40`.

## Interpretation

The current evidence supports a bounded-cost containment framing, not a faster-or-cheaper framing. FlowFence-Lite quarantine-actioncanon reaches zero exposed poisoned retrieval and zero attack manifestation in the main result table, but it pays a same-axis proxy cost of roughly one extra model call per case and about twenty percent more current-task trace-token proxy.

This is useful for the paper because it turns runtime feasibility from an unmeasured claim into a bounded caveat. A strict runtime-feasibility claim still needs new instrumentation that records per-call wall-clock latency and provider token usage.

## Paper-Ready Wording

Supported: "From existing same-axis traces, FlowFence-Lite containment adds moderate execution overhead proxies: the selected quarantine-actioncanon variant increases recorded model calls per case by `32.71%` and current-task trace-token proxy by `20.71%` relative to no defense."

Not supported: "FlowFence-Lite lowers latency or uses fewer tokens."

Not supported yet: "FlowFence-Lite has measured latency overhead below 25% or measured token overhead below 30%."
