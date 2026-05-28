# Paper Table Review Report

- Status: `pass`
- ERROR count: `0`
- WARN count: `0`
- INFO count: `7`
- Table values inconsistent with source evidence: `False`
- Unsupported claim overmarked: `False`
- Raw secret appeared: `False`

## Tables reviewed
- `table_1_p0_agentpoison`
- `table_2_p1_synthetic`
- `table_3_minimax_postfix_smoke`
- `table_3_minimax_3seed_coverage`
- `table_4_claims_matrix`
- `table_5_evidence_boundaries`
- `table_6_minimax_3seed_seed_stability`

## Issues
| severity | table | row | check | message |
| --- | --- | --- | --- | --- |
| INFO | table_1_p0_agentpoison | table | review_complete | Reviewed P0 AgentPoison table. |
| INFO | table_2_p1_synthetic | table | review_complete | Reviewed P1 synthetic table. |
| INFO | table_3_minimax_postfix_smoke | table | review_complete | Reviewed MiniMax post-fix smoke table. |
| INFO | table_3_minimax_3seed_coverage | table | review_complete | Reviewed MiniMax 3-seed coverage table. |
| INFO | table_4_claims_matrix | table | review_complete | Reviewed claims matrix. |
| INFO | table_5_evidence_boundaries | table | review_complete | Reviewed evidence boundaries. |
| INFO | table_6_minimax_3seed_seed_stability | table | review_complete | Reviewed MiniMax 3-seed seed stability table. |

## Interpretation

The generated paper-facing tables are consistent with committed high-level evidence unless ERROR issues are listed above. Raw traces and provider outputs are intentionally not included. MiniMax is the only real provider represented.
