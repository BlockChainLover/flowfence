# MiniMax P1 Post-Fix Smoke Audit

This directory contains high-level audit outputs explaining the aggregate task-success gap in the clean post-fix MiniMax 18-run smoke.

Raw traces, raw MiniMax outputs, raw prompts, provider logs, event JSONL files, policy JSONL files, individual per-run `metrics.json` files, credentials, and secrets are intentionally not committed.

The evidence is MiniMax-only. This is still a small 18-run smoke, not a full real-model experiment.

Audit conclusion: the aggregate `task_success_rate=0.888889` gap is baseline-driven. The two task failures are both `prompt_filter` runs under `workspace_poisoning_indirect`, one on `chain_4` and one on `blackboard_4`. FlowFence-Lite remains clean across its six runs with `task_success_rate=1.0`, `unauthorized_raw_leakage_mean=0.0`, and `external_leakage_mean=0.0`.
