# Non-Oracle Held-Out Deterministic Evidence

This directory contains high-level committed summaries for the deterministic non-oracle held-out FlowFence validation.

- Matrix: 3 topologies x 10 attacks x 6 defenses x 3 seeds = 540 expected runs.
- Completed: 540; failed: 0.
- Provider metadata: MiniMax only, with provider calls disabled.
- Agent backend: scripted_deterministic.
- Non-oracle defenses: `flowfence_lite_nonoracle` and `flowfence_lite_nonoracle_no_semantic_patterns`.
- Held-out paraphrase attacks: summary, workspace, and communication hijack paraphrases.

Raw traces, raw prompts, event JSONL, policy JSONL, individual metrics, provider logs, secrets, and generated run directories are intentionally not committed.

## Main high-level result

`flowfence_lite_nonoracle` recorded task_success_rate=1.0, unauthorized_raw_leakage_mean=0.0, external_leakage_mean=0.0, and oracle annotation use count 0.

This is deterministic synthetic-runtime evidence, not production safety or non-MiniMax generalization.
