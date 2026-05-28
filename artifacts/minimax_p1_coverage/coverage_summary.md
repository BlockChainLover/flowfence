# MiniMax P1 MAS Coverage Summary

- Expected runs: `84`
- Completed runs: `84`
- Failed runs: `0`
- Provider: `minimax`
- Provider calls enabled: `true`
- Agent backend: `minimax_final_writer`
- Task success rate: `0.952381`
- Unauthorized raw leakage mean: `2.988095`
- External leakage mean: `0.380952`
- Cascade size mean: `4.178571`
- Privilege reach mean: `2.678571`
- Topology effect observed: `True`
- FlowFence clean runs: `21/21`

## FlowFence Comparisons

- Versus no defense: `{'unauthorized_raw_leakage': {'improves': 15, 'ties': 6, 'underperforms': 0, 'unavailable': 0}, 'external_leakage': {'improves': 12, 'ties': 9, 'underperforms': 0, 'unavailable': 0}, 'task_success': {'improves': 2, 'ties': 19, 'underperforms': 0, 'unavailable': 0}}`
- Versus static ACL: `{'unauthorized_raw_leakage': {'improves': 14, 'ties': 7, 'underperforms': 0, 'unavailable': 0}, 'external_leakage': {'improves': 10, 'ties': 11, 'underperforms': 0, 'unavailable': 0}, 'task_success': {'improves': 0, 'ties': 21, 'underperforms': 0, 'unavailable': 0}}`
- Versus prompt filter: `{'unauthorized_raw_leakage': {'improves': 6, 'ties': 15, 'underperforms': 0, 'unavailable': 0}, 'external_leakage': {'improves': 4, 'ties': 17, 'underperforms': 0, 'unavailable': 0}, 'task_success': {'improves': 2, 'ties': 19, 'underperforms': 0, 'unavailable': 0}}`

## Caveats

- MiniMax-only; no non-MiniMax generalization.
- One seed; not multi-seed robustness.
- Raw traces and provider outputs are intentionally not committed.
