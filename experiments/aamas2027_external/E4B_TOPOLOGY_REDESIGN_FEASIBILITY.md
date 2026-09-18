# E4-B permission-only topology feasibility

E4B_ORIGINAL_DESIGN: ORIGINAL_DESIGN_NOT_FEASIBLE (unchanged).
E4B_REDESIGN_FEASIBILITY: UNRESOLVED for the required public-benchmark study.

A narrow direct-message intervention is feasible: keep MARBLE coordinate_mode=star in BOTH conditions and install the same CommunicationEdges wrapper on original send_message/receive_message. Only its allowed edge set differs. STAR permits coordinator↔worker; GRAPH permits the preregistered directed off-diagonal adjacency matrix. No custom GRAPH evaluator, native graph scheduler or changed planner is used. Direct receive is checked too; rejection raises the same PermissionError through original handling.

Actual original agents with deterministic responses, one task per environment: Research and Database have five agents, STAR permits 8/20 attempted directed deliveries vs GRAPH 20/20; Coding has three agents, 4/6 vs 6/6. Direct receive cannot evade denied edges. Captured initial model-call arguments/messages/tools and actual adapter capabilities are equal across conditions. All ordered agent pairs were attempted; these are transport fixtures, not generated scientific trajectories.

| Held fixed | Evidence/status |
|---|---|
| Task instance, agent definitions, role/system prompts | Same Config input and captured act prompts |
| Model configuration, tools and represented tool permissions | Same captured model arguments and schemas; see limitation below |
| Evaluator, stopping, planner/delegation logic | Same original STAR classes/methods and config; no condition-specific method replacement |
| State representation and defense | Same stores/classes and same adapter; only realized message state may diverge |
| Contamination and protected fact/policy | Same sidecar function/record in both; no condition branch modifies it; contaminated full trajectories not exercised |
| Communication-edge permission | Only intentional differing parameter; actual send and direct receive tests |

Why overall UNRESOLVED: direct API reachability alone is insufficient. In all 100 Research and 100 Database records, relationship triples populate directed agent.relationships; worker→coordinator initiation is absent from new_communication_session's target enum, even though available-agent descriptions inspect both directions. Coding's 100 records are bidirectional. The current fixture can call send_message directly, but that does not establish that mocked tool-driven agents can implement the intended routing with the original advertised capabilities. Coordinator-initiated sessions may allow replies; their full relay path remains untested. Changing enum/tool permissions or role prompts in one condition would invalidate the design. We do not silently do so, nor conclude impossibility from an untested session route.

Additionally, shared workspace/memory interfaces stay fixed and permit indirect propagation; this intervention would measure direct message-edge permissions only, not the topology of all information flow. Full mediated protected-data trajectories and a certified public pool are absent.

No replacement preregistration is activated and no 18 tasks selected. If routing and certification are later validated without non-edge differences, preserve exactly 18 unique semantic tasks × contamination A/B × EXACT_IFC/FLOWFENCE_R2 × STAR/GRAPH × 2 repetitions = 288 episodes. No scale reduction, native STAR/GRAPH comparison, custom evaluator, or scientific model execution is authorized here. E3's existing nine mock trajectories/three families are untouched.

Evidence: recovery/INTEGRATION_AUDIT.json topology_checks and TOPOLOGY_TOOL_PERMISSIONS.json. The edge wrapper is a feasibility prototype, not an approved formal runner.
