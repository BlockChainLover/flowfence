# MiniMax P1 MAS Post-Fix Smoke Evidence

This directory contains small committed summaries for the clean post-debug P1 MiniMax 18-run smoke.

Raw traces, provider outputs, prompts, provider logs, event JSONL files, policy-decision JSONL files, individual per-run `metrics.json` files, credentials, and secrets are intentionally not committed.

The real provider is MiniMax only. This is a clean post-fix smoke after final-writer prompt and utility-evaluator debugging. It is not a full real-model experiment and should not be used to claim broad real-model robustness or non-MiniMax generalization.

Matrix scope:

- Topologies: `chain_4`, `blackboard_4`
- Attacks: `none`, `summary_poisoning_indirect`, `workspace_poisoning_indirect`
- Defenses: `none`, `prompt_filter`, `flowfence_lite`
- Seed: `1`
- Expected runs: `18`

The clean 18-run rerun completed all runs, but aggregate task success was `0.888889`, lower than the prior debug run. FlowFence-Lite itself had `task_success_rate=1.0` in its six-run subset, while `prompt_filter` had `task_success_rate=0.666667`. Treat this as official small post-fix smoke evidence plus a reason to inspect prompt-filter/no-defense task failures before broader coverage.
