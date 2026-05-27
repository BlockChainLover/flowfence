# MiniMax P1 MAS Smoke Summary (18run)

Small MiniMax smoke only; not a full real-model experiment and not evidence for non-MiniMax generalization.

## Run Status

- Expected runs: `18`
- Completed runs: `18`
- Failed runs: `0`
- Provider: `minimax`
- Provider calls enabled: `True`
- Agent backend: `minimax_final_writer`

## Matrix

- Topologies: `blackboard_4, chain_4`
- Attacks: `none, summary_poisoning_indirect, workspace_poisoning_indirect`
- Defenses: `flowfence_lite, none, prompt_filter`
- Seeds: `1`

## Aggregate Metrics

- Task success rate: `0.055556`
- Unauthorized raw leakage mean: `4.111111`
- External leakage mean: `0.666667`
- Cascade size mean: `3.333333`
- Privilege reach mean: `2.222222`
- Topology effect observed: `True`

## FlowFence Comparisons

- FlowFence vs no-defense raw leakage counts: `{'improves': 4, 'ties': 2, 'underperforms': 0, 'unavailable': 0}`
- FlowFence vs no-defense external leakage counts: `{'improves': 4, 'ties': 2, 'underperforms': 0, 'unavailable': 0}`
- FlowFence vs prompt-filter raw leakage counts: `{'improves': 4, 'ties': 2, 'underperforms': 0, 'unavailable': 0}`
- FlowFence vs prompt-filter external leakage counts: `{'improves': 2, 'ties': 4, 'underperforms': 0, 'unavailable': 0}`

## Caveats

- Raw traces, prompts, provider responses, event JSONL files, and per-run metrics are intentionally not committed.
- This evidence is a smoke check for the MiniMax final-writer path only.
- Do not use it to claim broad real-model robustness or non-MiniMax generalization.
