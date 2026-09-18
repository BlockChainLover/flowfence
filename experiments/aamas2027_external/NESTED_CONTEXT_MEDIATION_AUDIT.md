# Nested model contexts

NESTED_CONTEXT_MEDIATION: NOT_FEASIBLE with the currently exposed generic context API and outer-scope adapter.

| Producer/context | Actual model entry | Receiving identity issue |
|---|---|---|
| Top-level role task/profile/BaseMemory | BaseAgent.act → model_prompting | act can supply the role ID through an external scope |
| Session memory/chat history | _handle_new_communication_session → model_prompting inside alternating role loop | Initiating self remains unchanged while session_current_agent changes; no receiving-principal parameter is passed |
| Session chat summary | same method's summarizer call | Separate summarizer context is not identified at the shared transport API |
| Planner assignments/current progress | EnginePlanner.assign_tasks → model_prompting | Planner scope can be supplied, but flattened current_progress is not a publication interface |
| Planner decision/summary | decide_next_step/summarize_output → model_prompting | Requires explicit planner identity; actual paths exercised |
| Coding task/config | create_solution_handler → model_prompting | Tool/sub-model authorization must be bound explicitly, not inferred from the initiating agent |
| Coding code/advice | reviewer calls model_prompting twice | Shared file is consumed before outer tool return; positive raw-context fixture under both arms |
| Evaluator task/runtime/reference | Evaluator methods → model_prompting; DB standalone batch → litellm.completion | Trusted gold/reference and runtime-derived context must remain distinct; common flattened messages carry no such metadata |
| Debugger/Research domain helper | source functions call model_prompting | Not reachable from the pinned registered E2 tools; analyst has no model call |

The original decorated model_prompting executes unchanged and reaches a deterministic litellm transport double (real Message objects). The generic candidate gateway receives correct worker scope in one fixture and removes the protected value. In an actual original session, applying only the initiating owner's scope permits the same value in the worker's context: 6/6 environment/arm fixtures reproduce the identity error. No prompt-text identity heuristic or stack-inspection authorization rule is added.

The original coder/reviewer tool-return wrapper cannot mediate context retroactively: in both arms, a pre-existing shared solution fixture containing the protected value reaches reviewer model input before apply_action returns. The workspace-publication probe closes new active file writes, but does not prove that all legacy/backing state reads have trusted ownership.

A single transport entry alone therefore cannot guarantee the requested property. Explicit trusted recipient and evaluator/runtime span metadata must be introduced at their assembly/handoff points. That is an architectural prerequisite, not a recognizer adjustment or a reason to strip all owner-private context (which would remove a capability). No scientific calls and no evaluator/gold rewrite.
