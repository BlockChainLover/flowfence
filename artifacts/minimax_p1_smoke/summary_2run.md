# MiniMax P1 MAS Smoke Summary (2run)

Small MiniMax smoke only; not a full real-model experiment and not evidence for non-MiniMax generalization.

## Run Status

- Expected runs: `2`
- Completed runs: `2`
- Failed runs: `0`
- Provider: `minimax`
- Provider calls enabled: `True`
- Agent backend: `minimax_final_writer`

## Matrix

- Topologies: `chain_4`
- Attacks: `none`
- Defenses: `none, prompt_filter`
- Seeds: `1`

## Aggregate Metrics

- Task success rate: `0.5`
- Unauthorized raw leakage mean: `0.0`
- External leakage mean: `0.0`
- Cascade size mean: `0.0`
- Privilege reach mean: `0.0`
- Topology effect observed: `False`

## FlowFence Comparisons

- FlowFence vs no-defense raw leakage counts: `{'improves': 0, 'ties': 0, 'underperforms': 0, 'unavailable': 0}`
- FlowFence vs no-defense external leakage counts: `{'improves': 0, 'ties': 0, 'underperforms': 0, 'unavailable': 0}`
- FlowFence vs prompt-filter raw leakage counts: `{'improves': 0, 'ties': 0, 'underperforms': 0, 'unavailable': 0}`
- FlowFence vs prompt-filter external leakage counts: `{'improves': 0, 'ties': 0, 'underperforms': 0, 'unavailable': 0}`

## Caveats

- Raw traces, prompts, provider responses, event JSONL files, and per-run metrics are intentionally not committed.
- This evidence is a smoke check for the MiniMax final-writer path only.
- Do not use it to claim broad real-model robustness or non-MiniMax generalization.
