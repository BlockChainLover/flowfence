# RQ2 Topology Table Candidate

## Goal

Provide an auditable small table for RQ2 ("Does runtime topology affect propagation?") using the fixed deterministic P1 benchmark.

## Provenance

- Matrix config: `configs/experiment/mas_p1_strengthened_matrix.yaml`
- Rerun date: `2026-06-22`
- Sweep output root: `/private/tmp/flowfence_rq2_topology_strengthened`
- Summary output dir: `/private/tmp/flowfence_rq2_topology_strengthened_summary`
- Summary file: `/private/tmp/flowfence_rq2_topology_strengthened_summary/summary.json`
- Topology sanity file: `/private/tmp/flowfence_rq2_topology_strengthened_summary/topology_sanity.json`
- Provider metadata: `minimax`
- Provider calls enabled: `false`

This is deterministic synthetic-runtime evidence only. It is suitable for the current RQ2 framing but not for non-MiniMax or real-environment generalization claims.

## Recommended Main-Text Table

Condition:

- defense = `none`
- attacks averaged over the six attack-positive settings:
  - `summary_poisoning_direct`
  - `summary_poisoning_indirect`
  - `workspace_poisoning_direct`
  - `workspace_poisoning_indirect`
  - `comm_hijack_direct`
  - `comm_hijack_indirect`
- seeds = `1, 2, 3`
- run count per topology = `18`

| topology | raw leak | external leak | cascade size | cascade depth | privilege reach |
| --- | ---: | ---: | ---: | ---: | ---: |
| `chain_4` | 10.333333 | 2.000000 | 5.000000 | 5.000000 | 5.000000 |
| `star_4` | 13.166667 | 2.833333 | 6.000000 | 4.000000 | 5.000000 |
| `blackboard_4` | 15.833333 | 2.833333 | 7.000000 | 4.000000 | 5.000000 |

Interpretation:

- `chain_4` is the narrowest but deepest propagation path.
- `star_4` increases breadth relative to `chain_4`.
- `blackboard_4` is the broadest and has the highest raw leakage.
- `privilege_reach` saturates at `5.0` in all three topologies for this no-defense attack-positive slice, so this slice does not separate privilege reach.

## Alternate Single-Attack Slice

Condition:

- defense = `none`
- attack = `workspace_poisoning_indirect`
- seeds = `1, 2, 3`
- run count per topology = `3`

| topology | raw leak | external leak | cascade size | cascade depth | privilege reach |
| --- | ---: | ---: | ---: | ---: | ---: |
| `chain_4` | 13.000000 | 2.000000 | 5.000000 | 5.000000 | 5.000000 |
| `star_4` | 17.000000 | 3.000000 | 6.000000 | 4.000000 | 5.000000 |
| `blackboard_4` | 24.000000 | 3.000000 | 7.000000 | 4.000000 | 5.000000 |

This slice is closer to the current blackboard case-study narrative, but it is narrower than the recommended attack-positive aggregate.

## Not Recommended For Main Text

The full 252-run by-topology aggregate mixes four defenses and seven attacks:

| topology | raw leak | external leak | cascade size | cascade depth | privilege reach |
| --- | ---: | ---: | ---: | ---: | ---: |
| `chain_4` | 3.821429 | 0.642857 | 3.642857 | 3.642857 | 2.678571 |
| `star_4` | 5.321429 | 1.071429 | 4.178571 | 3.107143 | 2.678571 |
| `blackboard_4` | 6.750000 | 1.071429 | 4.714286 | 3.107143 | 2.678571 |

These numbers are useful as a sanity check, but they are less suitable for RQ2 because they mix topology effects with defense effects and dilute attack pressure with `attack=none` rows.
