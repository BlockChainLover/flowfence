# Finite transition-class capability parity

EXACT_IFC_PARITY: VERIFIED for the pinned E2 STAR/naive/BaseMemory route and the current common adapters.
TRANSITION_CLASSES_TOTAL: 23
TRANSITION_CLASSES_VERIFIED: 23
Paired environment/class fixtures: 59.

This replaces the earlier demand for arbitrary trajectory enumeration with finite reachable transition types. It does not certify completeness of mediation or the capability equivalence of an as-yet unimplemented architecture redesign.

The original Config/Engine/agent/planner/evaluator and decorated model_prompting code execute; only transport/services/time/UUID are deterministic doubles. Planner assignment and next-step methods are no longer replaced by constant method mocks. Captured actual model kwargs, available tool schemas, routes, failure shape, clean results and outbound requests match for each pair. Identical non-model fixture arguments are supplied by the same function in the two defense iterations. Both planner-decided termination and budget termination execute. Model failure executes the original retry wrapper identically. No scientific task quality is used.

agent_model_invocation | agent_result_to_planner | agent_send | coding_nested_review | coding_workspace_read_after_write | database_offline_judge | database_sql_error | final_serialization | model_error_retry | planner_assignment | planner_next_step | planner_progress_update | research_network_tools | session_initiation | session_reply_receive | shared_state_read | shared_state_write | task_initialization | termination | termination_budget | tool_error | tool_invocation | tool_result

Common types include all requested initialization, assignment, next-step, invocation, send, session initiation/reply, state read/write, tool input/result/error, result-to-planner, progress, termination and final serialization. Additional types cover original model retry, budget stop, Research network tools, DB SQL error, nested Coding review and workspace read-after-write. Registered tool coverage is seven Research, one DB and two Coding actions; inactive source functions are not falsely treated as available capabilities. Other native coordination/planning/memory modes are outside the fixed E2 route.

Important separation: identical invalid reply schemas are a shared benchmark defect, not an IFC capability disadvantage. Actual permissive runtime session paths and their symmetric failure/permission cases are exercised. E4-B separately requires lawful advertised communication APIs and fails that test. Equality of two broken schemas is not a claim that they are valid or that scientific runs can proceed.

Evidence: artifacts/aamas2027_gate_ae/AUDIT.json transition_pairs/runtime_inventory; tests/test_aamas_gate_ae.py validates every comparison. The only defense-specific operation is unchanged inspect_r2_event dispatch; post-defense outputs may differ by design.

The original standalone Database batch evaluator also runs under both arms on an isolated public fixture, with identical captured completion kwargs and score/output/error handling. Token trimming and transport are offline doubles. Its upstream hard-coded `gpt-4o-mini` selector is observed, never dispatched; no non-MiniMax configuration is added. This proves bounded parity only; an unchanged live MiniMax-only judge path is not certified.
