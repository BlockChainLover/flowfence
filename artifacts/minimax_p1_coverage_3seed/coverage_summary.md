# MiniMax P1 MAS Coverage Summary

- Expected runs: `252`
- Completed runs: `252`
- Failed runs: `0`
- Provider: `minimax`
- Provider calls enabled: `true`
- Agent backend: `minimax_final_writer`
- Task success rate: `0.964286`
- Unauthorized raw leakage mean: `2.829365`
- External leakage mean: `0.325397`
- Cascade size mean: `4.178571`
- Privilege reach mean: `2.678571`
- Topology effect observed: `True`
- FlowFence clean runs: `63/63`

## FlowFence Comparisons

- Versus no defense: `{'unauthorized_raw_leakage': {'improves': 42, 'ties': 21, 'underperforms': 0, 'unavailable': 0}, 'external_leakage': {'improves': 32, 'ties': 31, 'underperforms': 0, 'unavailable': 0}, 'task_success': {'improves': 7, 'ties': 56, 'underperforms': 0, 'unavailable': 0}}`
- Versus static ACL: `{'unauthorized_raw_leakage': {'improves': 42, 'ties': 21, 'underperforms': 0, 'unavailable': 0}, 'external_leakage': {'improves': 30, 'ties': 33, 'underperforms': 0, 'unavailable': 0}, 'task_success': {'improves': 0, 'ties': 63, 'underperforms': 0, 'unavailable': 0}}`
- Versus prompt filter: `{'unauthorized_raw_leakage': {'improves': 18, 'ties': 45, 'underperforms': 0, 'unavailable': 0}, 'external_leakage': {'improves': 13, 'ties': 50, 'underperforms': 0, 'unavailable': 0}, 'task_success': {'improves': 2, 'ties': 61, 'underperforms': 0, 'unavailable': 0}}`

## Caveats

- MiniMax-only; no non-MiniMax generalization.
- Scope is limited to the configured seeds and matrix.
- Raw traces and provider outputs are intentionally not committed.
