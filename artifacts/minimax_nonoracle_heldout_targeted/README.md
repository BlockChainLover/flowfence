# MiniMax Non-Oracle Held-Out Targeted Evidence

This directory contains high-level committed summaries for the targeted MiniMax-only non-oracle held-out validation.

- Matrix: 2 topologies x 3 paraphrase attacks x 4 defenses x 3 seeds = 72 expected runs.
- Completed: 72; failed: 0.
- Provider: MiniMax only.
- Provider calls enabled: true.
- Agent backend: minimax_final_writer.
- FlowFence defense in the targeted matrix: `flowfence_lite_nonoracle`.

Raw traces, raw MiniMax outputs, raw prompts, event JSONL, policy JSONL, individual metrics, provider logs, secrets, and generated run directories are intentionally not committed.

## Main high-level result

`flowfence_lite_nonoracle` recorded task_success_rate=1.0, unauthorized_raw_leakage_mean=0.0, external_leakage_mean=0.0, and oracle annotation use count 0.

This is MiniMax-backed synthetic-runtime targeted validation, not non-MiniMax generalization, production safety, or real browser/desktop/computer-use evidence.
