# P1 MiniMax MAS Coverage

This directory contains committed high-level summaries for the P1 MiniMax-only MAS coverage experiment.

Raw traces, raw MiniMax outputs, prompts, provider logs, event JSONL, policy JSONL, and individual per-run metrics are intentionally not committed.

## Scope

- Provider: MiniMax only
- Agent backend: `minimax_final_writer`
- Provider calls enabled: true
- Matrix: 3 topologies x 7 attacks x 4 defenses x seed 1
- Expected runs: 84
- Topologies: `chain_4`, `star_4`, `blackboard_4`
- Attacks: `none`, `summary_poisoning_direct`, `summary_poisoning_indirect`, `workspace_poisoning_direct`, `workspace_poisoning_indirect`, `comm_hijack_direct`, `comm_hijack_indirect`
- Defenses: `none`, `static_acl`, `prompt_filter`, `flowfence_lite`

This coverage is broader than the prior 18-run smoke, but it remains one-seed evidence. It does not support non-MiniMax generalization, production safety, or broad real-model robustness.

The optional 252-run three-seed config exists for a later explicit goal and was not run here.
