# MiniMax P1 Post-Fix 2-Run Safety Smoke

This is a 2-run safety smoke only. It confirms that the post-fix MiniMax path can execute before running the full 18-run smoke.

## Scope

- Provider: MiniMax
- Provider calls enabled: `true`
- Agent backend: `minimax_final_writer`
- Topology: `chain_4`
- Attack: `none`
- Defenses covered by the 2-run prefix: `none`, `prompt_filter`
- Seed: `1`

## Results

- Completed runs: `2`
- Failed runs: `0`
- Task success rate: `1.0`
- Unauthorized raw leakage mean: `0.0`
- External leakage mean: `0.0`
- Cascade size mean: `0.0`
- Privilege reach mean: `0.0`
- Topology effect observed: `false`

## Caveats

The 2-run prefix does not include `flowfence_lite`, so no FlowFence-vs-no-defense comparison is available from this subset. Raw traces, prompts, provider outputs, event JSONL files, policy JSONL files, and per-run metrics are intentionally not committed.
