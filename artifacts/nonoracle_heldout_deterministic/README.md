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

## Claim Use

- This artifact supports a deterministic non-oracle held-out validation claim for the configured 540-run synthetic matrix.
- `flowfence_lite_nonoracle` did not use oracle attack annotations: the committed summary records oracle annotation use count 0.
- The held-out paraphrase attacks are included for summary poisoning, workspace poisoning, and communication hijack.
- `flowfence_lite_nonoracle` was clean in the high-level deterministic summary: task success 1.0, raw leakage 0.0, and external leakage 0.0.
- This artifact does not support MiniMax provider behavior, non-MiniMax generalization, arbitrary attack robustness, production safety, or real browser/desktop/computer-use deployment.
