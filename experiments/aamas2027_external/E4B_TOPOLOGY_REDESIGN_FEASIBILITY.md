# E4-B final direct-message feasibility decision

E4B_ORIGINAL_DESIGN: ORIGINAL_DESIGN_NOT_FEASIBLE.
E4B_REDESIGN_FEASIBILITY: NOT_FEASIBLE with the pinned original advertised communication APIs.
E4B_CLAIM_SCOPE: DIRECT_AGENT_TO_AGENT_COMMUNICATION_EDGE_TOPOLOGY_ONLY.

Both conditions retain native STAR execution and the same agents, prompts, tools, target enums, evaluator, planner, stopping and shared state. Only send/receive edge permission sets differ. No native GRAPH mode or new GRAPH-only tool is used. No preregistration is activated and no task pool is selected.

This audit invokes original BaseAgent.act with deterministic tool-call responses, not just send_message directly. Across all three environments and both edge policies it tests coordinator initiation, a worker reply/information return, coordinator relay containing the returned public marker, peer initiation and worker initiation. GRAPH agent2→agent3 initiation is advertised and allowed; STAR rejects that peer edge. Research/DB worker→coordinator *new initiation* is not in the initial target enum, but a coordinator-initiated reply is a separate API and was tested rather than assumed impossible.

The decisive failure is in that original reply API: BaseAgent._handle_new_communication_session constructs communicate_to parameters with properties={message}, required=[target_agent_id,message], additionalProperties=false. There is NO schema-valid argument object: omitting target_agent_id violates required, including it violates additionalProperties. Actual original runtime accepts a message-only mock reply and routes/relays it, but that violates the advertised API. Permissive synthetic success cannot certify an unchanged provider-facing tool capability. All exercised reply calls expose the same contradiction.

Fixing this requires changing a tool schema beyond the allowed edge-policy parameter. No such repair is applied here, even symmetrically. The failure is not misreported as a planner/evaluator change, and no scientific generation is used to probe provider tolerance.

Shared workspace/memory is held fixed across conditions. Even a later repaired design would test robustness to DIRECT COMMUNICATION-EDGE TOPOLOGY, not topology of all information flow. Approved scale remains 18 unique tasks × A/B × EXACT_IFC/FLOWFENCE_R2 × STAR/GRAPH × 2 repetitions = 288 episodes. No automatic redesign, task substitution, scale reduction or Gate A-F.

Evidence: AUDIT.json topology entries, source agent/base_agent.py:429-453 and frozen tool-schema checks. The narrower transport-only positive result from A-D remains historical evidence; it is not promoted to final feasibility.
