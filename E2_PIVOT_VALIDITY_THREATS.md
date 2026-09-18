# E2 pivot validity threats

Status: **P0 design proposal, not an implemented or certified runtime**. Date: 2026-09-18.
Native benchmark-runtime search is CLOSED. No dataset search/selection, development-task selection, benchmark integration, model generation, Gate B, R3 change or frozen-recognizer change is authorized here.

| Threat | Planned mitigation | Residual limitation |
|---|---|---|
| 1. Orchestration-induced distribution shift | One preregistered template, shared prompts/budgets/graph; report task provenance and harness details. | Native-runtime performance is not reproduced; solver traces and error distributions change. |
| 2. Decomposition changes difficulty | Preserve aggregate capabilities and information; no hidden gold; same team configuration for both arms; preserve source interaction caps. | Extra reasoning, coordination cost and role assignment may help or hurt. Task-semantic preservation does not prove equal difficulty. |
| 3. Evaluator mismatch | Original evaluator unchanged; deterministic serialization and per-component native/adapted fixture checks, including failed/blocked cases. | Some sources cannot represent mediated execution; scoring APIs can drift; reject/unresolve rather than replace scoring. |
| 4. Tool-capability mismatch | Preserve source tool semantics and availability; require pre-publication effects; use only source-permitted mocks. | Restricts eligible families and cannot cover arbitrary agent code, hidden I/O or uncontrolled side effects. |
| 5. Loss of original-runtime comparability | Use the exact allowed task/evaluator-under-harness claim and label all tables accordingly. | Results are not native benchmark MAS or leaderboard reproductions. |
| 6. Family heterogeneity | Define family adapters, context/tool profiles and budgets before task selection; stratify results and uncertainty by family. | Three families do not represent all domains; different tools/evaluators limit pooled interpretation. |
| 7. Synthetic privacy augmentation | Orthogonal facts, existing principals, independent pre-result semantic eligibility, no task-goal/gold edits, P1–P4 balance. | Artificial fact salience and policies may not match real sensitive data; introducing sidecars can change model behavior despite unchanged success criteria. |
| 8. Contamination recognizer scope | Reuse unchanged recognizer; test A/B raw absence and coverage before results; report fixed-pattern scope and no detector tuning. | Recognition is not general semantic understanding or adaptive/reconstruction protection. Known coverage can overstate natural-world attack representativeness. |
| 9. Repetitions are not semantic samples | Cluster analysis by original semantic task; paired conditions/defenses/repetitions; disclose task overlap across E1–E4. | 1080 E2 episodes remain 60 task clusters; few families and correlated reruns limit inference. |
| 10. Adapter trust / incomplete mediation | Opaque state handles, detached drafts, structured effect proposals, seven service boundaries; later adversarial same-input/type fixtures. | P0 specifies architecture only; implementation bugs or falsely declared effects can invalidate completeness. |
| 11. Outcome-driven task selection | Later eligibility and disjoint selection before outcome observation; retain failed/tied/uninformative tasks and all attempts. | Pre-result architectural filtering itself narrows the population of public tasks. |
| 12. Common harness confounds E2/E3 | Keep external task/evaluator and purpose-built workflow results separate and explain common runtime as a control. | Both still share implementation/model failure modes; evidence is complementary, not independent replications. |
| 13. Graph affects realized schedule | Only the explicit E4-B edge set changes, with same routing algorithm/caps and no forced conversations. | Realized paths/hops can change endogenously; STAR vs GRAPH is not pure information-flow topology. |

No threat is removed by adding a hash, freeze file or blanket gate. Ordinary types, principal ownership, transactions, versioned source references and targeted future execution tests address concrete implementation concerns; the scientific limitations remain reportable limitations. Existing safety measures and frozen evidence are retained.
