# P1 MiniMax MAS 3-Seed Coverage

This directory contains committed high-level summaries for the P1 MiniMax-only 3-seed MAS coverage experiment.

Raw traces, raw MiniMax outputs, prompts, provider logs, event JSONL, policy JSONL, and individual per-run metrics are intentionally not committed.

## Scope

- Provider: MiniMax only
- Agent backend: `minimax_final_writer`
- Provider calls enabled: true
- Matrix: 3 topologies x 7 attacks x 4 defenses x 3 seeds
- Expected runs: 252
- Completed runs: 252
- Failed runs: 0
- Topologies: `chain_4`, `star_4`, `blackboard_4`
- Attacks: `none`, `summary_poisoning_direct`, `summary_poisoning_indirect`, `workspace_poisoning_direct`, `workspace_poisoning_indirect`, `comm_hijack_direct`, `comm_hijack_indirect`
- Defenses: `none`, `static_acl`, `prompt_filter`, `flowfence_lite`
- Seeds: `1`, `2`, `3`

The initial 252-run attempt had one MiniMax read timeout:

- `mas_p1__enterprise_assistant_001__chain_4__summary_poisoning_direct__prompt_filter__seed1`

The timeout was retried safely by rerunning the same sweep without `--force`, which skipped 251 completed runs and executed only the missing run. The canonical artifacts in this directory were refreshed after the retry and now record 252/252 completed runs.

This is stronger than the prior 84-run one-seed coverage, but it is still MiniMax-only evidence. It does not support non-MiniMax generalization, production safety, or broad deployment robustness.

## Interpretation Caveats

- The canonical 3-seed coverage is now 252/252 completed after retrying one transient MiniMax read timeout.
- The FlowFence subset is clean across 63/63 configured FlowFence runs, with task success 1.0 and zero raw/external leakage in the committed high-level summaries.
- The benchmark uses a synthetic deterministic MAS runtime with MiniMax final-writer calls; it is not a real-world browser, desktop, or computer-use agent environment.
- The evidence is MiniMax-only and does not support non-MiniMax provider generalization.
- The evidence is not production safety evidence.
