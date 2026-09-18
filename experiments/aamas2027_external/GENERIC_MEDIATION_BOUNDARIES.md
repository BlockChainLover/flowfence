# Generic runtime mediation architecture

GENERIC_MEDIATION_BOUNDARY_COUNT: 7 conceptual boundaries. This is NOT a claim of seven fully certified installed boundaries.
GENERIC_MEDIATION_ARCHITECTURE: NOT_FEASIBLE_WITH_CURRENT_CONTEXT_AND_STATE_INTERFACES.

| Boundary | Actual runtime APIs | Finding |
|---|---|---|
| 1. Model context ingress | model_prompting → litellm.completion, common to top-level agents, sessions, planner, coder, reviewer and evaluator | Genuine common dispatch exists, but no trusted receiving-principal/private-span metadata. Explicit correct scope filters the fixture. Initiator-only scope wrongly authorizes worker context in an actual session. NOT_FEASIBLE as a context-complete wrapper over current API. |
| 2. Inter-agent publication | BaseAgent.send_message/receive_message, called by _handle_communicate_to; planner assignment/act handoff | Same existing wrappers in both arms; complete normal send/receive path observed. Mutable mailbox storage belongs to boundary 3. |
| 3. State publication/access | BaseMemory.update/get_memory_str/__str__/retrieve_all/storage; SharedMemory.update/retrieve/retrieve_all/storage; planner.current_progress; environment.state/get_state; engine memory | No common pre-publication operation governs all exposed objects. Direct backing mutations and direct reads bypass current hooks. A context gateway after the fact is not a shared-publication boundary. NOT_FEASIBLE with existing state API; ownership-aware stores/attributes would be a new runtime design. |
| 4. Tool arguments | BaseEnvironment.apply_action before _action_handlers dispatch | One mechanism, all ten registered tool names across environments. Same tool schemas/permissions. No task-ID branch, gold or new recognizer. |
| 5. Tool results/errors | apply_action return and last_action_result | One mechanism in both arms. Covers returned values, not earlier nested consumers or publications. |
| 6. Shared/external effects | argument boundary for registered Research/DB data-dependent requests; builtins.open namespace publication for active Coding text writes/json.dump | No per-coder/reviewer file hook list needed. Scoped synchronous workspace probe closes the active writers using one actual runtime file interface. Clean new-file and JSON chunk behavior preserved. No arbitrary-code execution tool is registered in this pin. |
| 7. Final publication | Engine._write_to_jsonl, final-output value | Same final release mechanism. Evaluator-private metrics and local diagnostics retain their distinct classifications. |

The two new pieces of code are feasibility probes only: ContextBoundaryProbe and workspace_publication_probe. Neither is an approved formal runner. The file probe selects a workspace namespace, not a handler name; it preserves the pinned synchronous w-mode publication pattern and leaves trusted diagnostic files outside that shared namespace. It is not an OS sandbox or a guarantee for unregistered/concurrent future tools.

Convergence: Research, Database and Coding all fail the present context/state architecture, despite tractable registered side effects. Formal completion would need explicit principal handoff and private/runtime span metadata at model invocation, plus ownership-aware state publication/access. Guessing principals from prompt strings, stack locals or variable names is rejected. These are cross-cutting runtime changes, not one outstanding engineering check or another handler patch. This gate does not implement that redesign or create Gate A-F. This is not a theorem that no future generic architecture can support MARBLE.

Both defense arms retain identical interfaces; their only defense branch is the existing frozen inspect_r2_event dispatch. No new semantic detector, task/gold branch or capability removal. Failing these integration probes is not evidence that the public tasks themselves are scientifically unsuitable.
