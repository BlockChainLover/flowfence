# Finite transition inventory (design only)

23 proposed classes, seven generic mediation boundaries. Class count is a taxonomy choice, not a security result or inheritance of MARBLE certification. Runtime implementation must dispatch all actions through these classes; unknown actions fail closed with the same typed failure in both arms. A newly required semantic transition needs explicit design review rather than silent omission.

| ID | Class | Boundary/ownership obligation |
|---|---|---|
| T01 | task_initialization | B1 B3 |
| T02 | trusted_private_installation | trusted initialization; export B2–B7 |
| T03 | model_context_assembly | B1 |
| T04 | model_invocation | B1 |
| T05 | delegation_assignment | B2 B1 |
| T06 | next_step_decision | B2 B3 B4 |
| T07 | planner_progress_summary | B2 B3 B1 |
| T08 | interagent_publication | B2 |
| T09 | message_delivery_session_reply | B2 B1 |
| T10 | worker_result_propagation | B2 B3 B1 |
| T11 | private_memory_access | owner check; export B2 B3; context B1 |
| T12 | shared_state_artifact_read | B3 B1 |
| T13 | shared_state_publication_write | B3 |
| T14 | artifact_export | B3 B7 |
| T15 | tool_argument_invocation | B3 B4 |
| T16 | tool_result | B5 B3 B1 |
| T17 | tool_error | B5 B1 |
| T18 | side_effect_preparation | B4 B6 |
| T19 | side_effect_commit | B6 B3 |
| T20 | model_error_retry | B1; shared error B2 B3 |
| T21 | termination | B7; private control only otherwise |
| T22 | final_serialization_publication | B7 |
| T23 | evaluator_invocation_replay | trusted evaluator port; no runtime publication |

Variants must be enumerated in later implementation fixtures: coordinator/each worker, allowed/denied/rewrite, shared read/write, set/delete, private self-access/export, tool read-only/internal/external, synchronous error and unknown external commit, normal/budget/error/protocol termination. T11 includes read and write; T21 includes all termination causes. Combined transitions traverse every listed applicable boundary, not just one convenient check.

For every class, later same-input tests must compare capabilities, recipients, provenance, original values supplied to the frozen decision, resulting typed release/deny behavior and emitted state/actions. Equal defense outputs are not required. Declassification must remain the existing frozen policy behavior. Test post-release model ingress, state alias prevention, stale revisions, unauthorized references, metadata payloads and all effect paths. None of those behavioral tests is claimed performed in P0.

## Mapping from the earlier 23-class MARBLE audit

This reuses its finite enumeration and paired comparison method, not its implementation or pass status. The prior source was TRANSITION_CLASS_PARITY_AUDIT.md on branch codex/aamas2027-gate-a at 9615ca34d166c8c9f75c0c037626956512b0c251. The native-runtime search remains closed.

| Earlier class | Proposed coverage |
|---|---|
| agent_model_invocation | T03 T04 |
| agent_result_to_planner | T10 |
| agent_send | T08 T09 |
| coding_nested_review | T05 T04 T08 T10 |
| coding_workspace_read_after_write | T13 T12 |
| database_offline_judge | T23 |
| database_sql_error | T17 |
| final_serialization | T22 |
| model_error_retry | T20 |
| planner_assignment | T05 |
| planner_next_step | T06 |
| planner_progress_update | T07 |
| research_network_tools | T15 T18 T19 T16 |
| session_initiation | T08 T09 |
| session_reply_receive | T09 |
| shared_state_read | T12 |
| shared_state_write | T13 |
| task_initialization | T01 T02 |
| termination | T21 |
| termination_budget | T21 |
| tool_error | T17 |
| tool_invocation | T15 |
| tool_result | T16 |

New explicit classes expose context assembly, private memory, artifact export and preparation/commit separately. Tool callbacks, hidden I/O, live mutable aliases and evaluator-to-worker backchannels are forbidden capabilities, not unlisted permitted transitions. An accepted adapter must demonstrate it has none. Trusted diagnostics and evaluator scoring remain outside experimental release; promoting either to a modeled audience is an explicit mediated publication.
