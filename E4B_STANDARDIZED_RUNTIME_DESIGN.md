# E4-B standardized runtime conceptual design

Status: **P0 design proposal, not an implemented or certified runtime**. Date: 2026-09-18.
Native benchmark-runtime search is CLOSED. No dataset search/selection, development-task selection, benchmark integration, model generation, Gate B, R3 change or frozen-recognizer change is authorized here.

E4B_STANDARDIZED_RUNTIME_FEASIBILITY: FEASIBLE (conceptual only)
E4B_CLAIM_SCOPE: DIRECT_COMMUNICATION_EDGE_TOPOLOGY_ROBUSTNESS

Use the same coordinator and two workers, model profiles, role prompts, initial data, privacy policies, tools/permissions, shared/private state APIs, graph validation algorithm, scheduler, budgets, failure handling, evaluator and stopping criteria. STAR permits worker↔coordinator direct messages only. GRAPH adds a preregistered pair of directed worker1↔worker2 edges; other direct edges are identical. All endpoints remain explicit principal IDs.

The declared direct-edge table is the only changed exogenous runtime configuration. The model may choose among permitted edges using the same prompt template and structured routing metadata; no graph-specific coaching or added tasks/tools. The destination list necessarily reflects the graph treatment, but identities, privileges and ordinary role instructions do not change. Invalid routing follows the same typed failure behavior. Do not force a matched realized message sequence, because direct-edge availability may naturally change worker choice, delegation, hops, coordination and termination.

Shared-state channels and tool-mediated information paths remain identical and may carry information between workers even under STAR. Thus STAR does not imply information-flow isolation or a general star-shaped propagation graph. Keep side-effect permissions and all indirect channels fixed; measure/label direct-message edges separately from shared-state/tool paths. Do not remove shared state to make the topology contrast look cleaner.

Preserve target 18 tasks × 2 contaminations × 2 defenses × 2 topologies × 2 repetitions = 288 episodes. This is a conceptual feasibility statement for a future human-approved design, not E4-B implementation, task selection or execution authorization. It does not reopen the MARBLE reply-schema redesign.
