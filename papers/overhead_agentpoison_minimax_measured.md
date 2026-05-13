# AgentPoison MiniMax Measured Overhead Slice

This note summarizes the strict measured-overhead slice added on 2026-05-06.

## Scope

- Axis: adapted AgentPoison full-ReAct StrategyQA under `minimax27`.
- Manifest: `data/tasks/agentpoison_strategyqa_fullreact_overhead_v1.json`.
- Conditions: `no_defense` vs `quarantine_actioncanon`.
- Slice size: 10 questions, executed in both benign and adversarial modes, for 20 case executions per condition.
- Purpose: runtime-feasibility evidence only; this does not replace the 25-question efficacy matrix.

## Artifacts

- Summary: `results/overhead_agentpoison_fullreact_minimax27_same_axis_measured_summary.json`
- No defense run: `results/overhead_agentpoison_fullreact_minimax27_triggerquery_nodefense_v1/`
- Quarantine-actioncanon run: `results/overhead_agentpoison_fullreact_minimax27_triggerquery_quarantine_actioncanon_v1/`
- Instrumented runner: `src/runner/run_agentpoison_fullreact.py`
- Summarizer: `src/runner/summarize_agentpoison_measured_overhead.py`

## Main Numbers

| condition | wall sec / case | LLM calls / case | provider tokens / case | token proxy / case | defense sec / case |
| --- | ---: | ---: | ---: | ---: | ---: |
| no defense | 28.861467 | 3.20 | 5197.25 | 5804.0125 | 0.000013 |
| quarantine-actioncanon | 24.692974 | 2.65 | 4191.50 | 4602.5000 | 0.000098 |
| relative delta | -14.44% | -17.19% | -19.35% | -20.70% | +0.000085 sec |

## Interpretation

Observation: On this 10-question measured slice, the selected quarantine-actioncanon condition used fewer LLM calls, lower wall-clock time, and fewer provider-reported tokens than no defense.

Observation: Provider token usage was available for all 40 case executions, so this artifact is stronger than the prior proxy-only artifact for this slice.

Observation: FlowFence-Lite inspection time was negligible in absolute terms: about `0.000098` seconds per case for quarantine-actioncanon.

Interpretation: The result supports a narrow runtime-feasibility claim: measured overhead on this same-axis slice did not show additional latency or token burden, and the defense inspection itself is microsecond-scale relative to LLM latency.

Caveat: Do not claim that FlowFence-Lite is generally faster or uses fewer tokens. The method run had shorter ReAct trajectories and no quarantine/intervention events on this 10-question slice, so lower latency/token is trajectory-confounded rather than a universal property of the defense.

Caveat: The main safety/effectiveness claim should still use the 25-question 3-rerun matrix. This measured-overhead slice is an auxiliary feasibility result.
