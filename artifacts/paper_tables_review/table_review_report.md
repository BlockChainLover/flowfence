# Paper Table Review Report

- Status: `pass`
- ERROR count: `0`
- WARN count: `6`
- INFO count: `5`
- Table values inconsistent with source evidence: `False`
- Unsupported claim overmarked: `False`
- Raw secret appeared: `False`

## Tables reviewed
- `table_1_p0_agentpoison`
- `table_2_p1_synthetic`
- `table_3_minimax_postfix_smoke`
- `table_4_claims_matrix`
- `table_5_evidence_boundaries`

## Issues
| severity | table | row | check | message |
| --- | --- | --- | --- | --- |
| INFO | table_1_p0_agentpoison | table | review_complete | Reviewed P0 AgentPoison table. |
| INFO | table_2_p1_synthetic | table | review_complete | Reviewed P1 synthetic table. |
| WARN | table_3_minimax_postfix_smoke | aggregate | minimax_smoke_caveat | MiniMax row caveat could more explicitly mention not broad real-model robustness. |
| WARN | table_3_minimax_postfix_smoke | flowfence_lite_subset | minimax_smoke_caveat | MiniMax row caveat could more explicitly mention not broad real-model robustness. |
| WARN | table_3_minimax_postfix_smoke | none_subset | minimax_smoke_caveat | MiniMax row caveat could more explicitly mention not broad real-model robustness. |
| WARN | table_3_minimax_postfix_smoke | prompt_filter_subset | minimax_smoke_caveat | MiniMax row caveat could more explicitly mention not broad real-model robustness. |
| WARN | table_3_minimax_postfix_smoke | blackboard_4 / workspace_poisoning_indirect / prompt_filter / seed=1 | minimax_smoke_caveat | MiniMax row caveat could more explicitly mention not broad real-model robustness. |
| WARN | table_3_minimax_postfix_smoke | chain_4 / workspace_poisoning_indirect / prompt_filter / seed=1 | minimax_smoke_caveat | MiniMax row caveat could more explicitly mention not broad real-model robustness. |
| INFO | table_3_minimax_postfix_smoke | table | review_complete | Reviewed MiniMax post-fix smoke table. |
| INFO | table_4_claims_matrix | table | review_complete | Reviewed claims matrix. |
| INFO | table_5_evidence_boundaries | table | review_complete | Reviewed evidence boundaries. |

## Interpretation

The generated paper-facing tables are consistent with committed high-level evidence unless ERROR issues are listed above. Raw traces and provider outputs are intentionally not included. MiniMax is the only real provider represented.
