# Benchmark Replacement R0 — Architecture-First Public Benchmark Candidate Audit

Date: 2026-09-18. Phase: **baseline scouting**. Decision: **UNRESOLVED**.

Four public candidate designs were inspected at recorded Git revisions. None is certified ARCHITECTURE_PASS; three fail the requested architecture requirements and one remains unresolved. The preferred shortlist is empty. This is not evidence that no viable public replacement exists, nor a scientific rejection of the candidate tasks. No candidate was run, imported, patched, selected for confirmatory use, or scored.

## Authority and preserved scientific objective

The human closes MARBLE Gate A, rejects MARBLE-native and permission-only E4-B, and authorizes this static replacement audit. No Gate A-F, Gate B, MARBLE redesign, reply-schema repair, or development execution follows from this report. E4-B topology support is **not** an E2 replacement requirement.

Keep **60 confirmatory semantic tasks**, preferably **20 + 20 + 20**, with disjoint development tasks. Each intended 20-task family must plausibly have at least 23 pre-result eligible tasks: 3 development plus at least 20 confirmatory. Keep CLEAN / CONTAMINATION_A / CONTAMINATION_B, EXACT_IFC / FLOWFENCE_R2, and 3 repetitions: **60 × 3 × 2 × 3 = 1080 formal episodes**. Keep P1 numeric / P2 identifier / P3 sensitive categorical / P4 opaque token at **15 each**. No allocation, task, protected value, contamination wording or split was selected here. No reduction of the target is proposed.

MiniMax remains the only authorized experiment provider. Upstream code mentions other providers; this audit neither configures them nor proposes using them. No paid endpoint, scientific generation, development generation, LLM evaluator, mock agent initialization, or benchmark entry point was called.

## Evidence and interpretation policy

Pinned source is the evidence; judgments below are static inferences, not measured compatibility. Source links include Git revisions and line anchors. `artifacts/aamas2027_benchmark_replacement_r0/SOURCE_EVIDENCE.json` records each inspected anchor and observation. Git revisions identify existing sources; no new content hashes, security gates, frozen contracts or baseline implementations were introduced.

An API is useful only if it dominates the relevant normal-execution paths. Public mutability alone is not treated as proof of a bypass, and wrapping the final string is not assumed to mediate earlier side effects. An explicit recipient at an upstream object boundary may support an adapter, but a prompt role, purpose label or function name is not itself principal identity. No architecture PASS is inferred from task counts.

## Candidate disposition

| Candidate design | Status | Decisive finding |
|---|---|---|
| tau2-bench native text, airline/retail/telecom | UNRESOLVED | Structured routing/tools exist; complete principal binding, telecom state mediation and evaluator replay preservation remain unproven. |
| AgentVerse native SDE team | ARCHITECTURE_FAIL | Active path directly accesses shared rule dictionaries and executes generated Python with unmediated effects. |
| ChatArena native Player/Arena language games | ARCHITECTURE_FAIL | Message interfaces exist, but no native generic tool invocation/result/error interface on this path, required as HARD by this request. |
| AWS collaboration scenarios, standalone release | ARCHITECTURE_FAIL | Data and evaluator are public; the executing multi-agent runtime is not supplied by this release. |

Counts are by **scoped design**, not claims about every configuration in a repository. ARCHITECTURE_PASS=0, ARCHITECTURE_FAIL=3, UNRESOLVED=1, INSUFFICIENT_TASKS=0.

## tau2-bench native text half-duplex, airline/retail/telecom

Status: **UNRESOLVED**. Repository: [https://github.com/sierra-research/tau2-bench](https://github.com/sierra-research/tau2-bench). Revision: `b7ea9074c1cba482b30687fecdb5c8425fd6f619`. License: MIT. Public families in scope: airline, retail, telecom.

Relevant eligible task counts: **not established**. Deep task-count, split, infrastructure and representative augmentation audits were not entered because the architecture did not pass.

- **recipient_identity**: PARTIAL: Orchestrator.from_role/to_role are trusted structured Role fields; agent/user have separate object/state slots. generate() has no modeled-recipient field; initialization, flipped user history, tool errors and all nested calls need a complete binding argument. call_name alone is not treated as identity.
- **context_provenance**: PARTIAL: system_messages/messages, ToolMessage.requestor and task.evaluation_criteria are structurally separate. Reused histories and evaluator replay need a complete provenance map.
- **communication_boundary**: PRESENT: Orchestrator.step passes structured messages between agent, user and environment.
- **shared_state_boundary**: UNRESOLVED: Environment.get_response/make_tool_call cover normal tool dispatch; TelecomEnvironment.sync_tools directly transfers data across publicly reachable DB objects and calls toolkit helpers. sync_tools is a finite existing hook, so this is not yet a proven impossibility. Its sufficiency for pre-publication mediation, including constructor/init/replay calls, has not been established.
- **tool_boundary**: PRESENT: get_response -> make_tool_call -> use_tool, structured ToolCall requestor/arguments and ToolMessage result/error.
- **side_effect_boundary**: UNRESOLVED: core domains model effects locally; telecom synchronization must be included rather than treating all effects as tool arguments. No OS sandbox is proposed.
- **final_output_boundary**: PRESENT: trajectory/get_messages/_finalize/SimulationRun. Final messages must be mediated before delivery, not just filtered in the final report.
- **evaluator_preservation**: PARTIAL: original evaluator has separate predicted/gold environments. Strict replay checks mutating-tool outputs; need proof that delivered safe views and unchanged native grading can coexist without mutating gold, disabling strict replay, or feeding unreleased content as delivered content.
- **capability_parity_feasibility**: UNKNOWN: same native config and orchestration can serve both arms; no complete boundary or error/stop parity proof yet.
- **privacy_augmentation_feasibility**: UNKNOWN: architecture has not passed; no representative task sidecar or A/B fixture was certified.
- **transition_class_parity_feasibility**: UNKNOWN
- **at_least_23_tasks_per_candidate_family_plausibility**: UNKNOWN: pre-result eligibility and disjoint development/confirmatory pools have not been established.

Concrete blockers:

- Complete structured recipient binding across initialization and user role-flipping, without interpreting prompt text or call-name strings.
- Show that existing sync_tools/state APIs dominate every modeled cross-principal publication, or reject the telecom design. No field-specific handler patches.
- Show unchanged evaluator replay semantics with mediated tool results and isolated gold/private evaluator context.
- User-simulator participation is native dual-control interaction, not evidence of a team of multiple assistant workers. Human scientific scope acceptance remains necessary.
- MiniMax-only agent, user and any required evaluator model compatibility is untested; no provider configured or called.

Pinned source observations:

- [src/tau2/orchestrator/orchestrator.py:771](https://github.com/sierra-research/tau2-bench/blob/b7ea9074c1cba482b30687fecdb5c8425fd6f619/src/tau2/orchestrator/orchestrator.py#L771): The orchestrator routes using a structured Role, not prompt-role guessing.
- [src/tau2/agent/llm_agent.py:44](https://github.com/sierra-research/tau2-bench/blob/b7ea9074c1cba482b30687fecdb5c8425fd6f619/src/tau2/agent/llm_agent.py#L44): Trusted system messages and accumulated interaction messages are separate state fields.
- [src/tau2/user/user_simulator.py:232](https://github.com/sierra-research/tau2-bench/blob/b7ea9074c1cba482b30687fecdb5c8425fd6f619/src/tau2/user/user_simulator.py#L232): User-side model roles are flipped; API chat role is not modeled receiving identity.
- [src/tau2/utils/llm_utils.py:355](https://github.com/sierra-research/tau2-bench/blob/b7ea9074c1cba482b30687fecdb5c8425fd6f619/src/tau2/utils/llm_utils.py#L355): Common generation API has purpose call_name, not an explicit modeled-principal parameter.
- [src/tau2/environment/environment.py:465](https://github.com/sierra-research/tau2-bench/blob/b7ea9074c1cba482b30687fecdb5c8425fd6f619/src/tau2/environment/environment.py#L465): Structured tool dispatch/result/error API exists and invokes sync_tools.
- [src/tau2/environment/environment.py:293](https://github.com/sierra-research/tau2-bench/blob/b7ea9074c1cba482b30687fecdb5c8425fd6f619/src/tau2/environment/environment.py#L293): Initialization/replay separately accesses and shares DB objects; must distinguish evaluator replay from experimental state access.
- [src/tau2/domains/telecom/environment.py:39](https://github.com/sierra-research/tau2-bench/blob/b7ea9074c1cba482b30687fecdb5c8425fd6f619/src/tau2/domains/telecom/environment.py#L39): Telecom synchronization directly reads/writes agent and user DBs and calls helpers outside the generic tool dispatcher.
- [src/tau2/environment/toolkit.py:138](https://github.com/sierra-research/tau2-bench/blob/b7ea9074c1cba482b30687fecdb5c8425fd6f619/src/tau2/environment/toolkit.py#L138): Tool dispatch is generic, but backing db remains publicly reachable.
- [src/tau2/evaluator/evaluator_env.py:89](https://github.com/sierra-research/tau2-bench/blob/b7ea9074c1cba482b30687fecdb5c8425fd6f619/src/tau2/evaluator/evaluator_env.py#L89): Native evaluator reconstructs predicted state and gold state separately.
- [src/tau2/environment/environment.py:399](https://github.com/sierra-research/tau2-bench/blob/b7ea9074c1cba482b30687fecdb5c8425fd6f619/src/tau2/environment/environment.py#L399): Strict replay compares recorded mutating-tool results with replayed results; sanitized-view handling requires a preservation argument.
- [src/tau2/orchestrator/orchestrator.py:210](https://github.com/sierra-research/tau2-bench/blob/b7ea9074c1cba482b30687fecdb5c8425fd6f619/src/tau2/orchestrator/orchestrator.py#L210): Common final simulation publication exists.
- [src/tau2/runner/build.py:357](https://github.com/sierra-research/tau2-bench/blob/b7ea9074c1cba482b30687fecdb5c8425fd6f619/src/tau2/runner/build.py#L357): Native text mode is an existing selectable execution path, not a new benchmark redesign.
- [src/tau2/evaluator/evaluator.py:24](https://github.com/sierra-research/tau2-bench/blob/b7ea9074c1cba482b30687fecdb5c8425fd6f619/src/tau2/evaluator/evaluator.py#L24): Evaluator includes optional LLM assertion grading; no evaluator was called in R0.

## AgentVerse native SDE code-team design

Status: **ARCHITECTURE_FAIL**. Repository: [https://github.com/OpenBMB/AgentVerse](https://github.com/OpenBMB/AgentVerse). Revision: `f90c4bd9680fdd3bcff8c52c9170911a59b23478`. License: Apache-2.0. Public families in scope: SDE team / code generation and tests.

Relevant eligible task counts: **not established**. Deep task-count, split, infrastructure and representative augmentation audits were not entered because the architecture did not pass.

- **recipient_identity**: PARTIAL: BaseAgent.name exists, but optional nested summary calls do not carry an explicit principal.
- **context_provenance**: PARTIAL: Message and per-agent memory exist; SDE selector merges code, tests and feedback through direct shared state.
- **communication_boundary**: PRESENT BUT INCOMPLETE: message selector/updater and add_message_to_memory do not dominate rule_params access.
- **shared_state_boundary**: FAIL: active SDE selector directly reads/writes environment.rule_params code/unit_tests/feedback/end_flag; no existing generic per-publication/access API dominates these accesses.
- **tool_boundary**: PARTIAL: executor rules exist, but SDE selector calls execute_unit_tests directly.
- **side_effect_boundary**: FAIL: in-process exec of generated Python permits effects not mediated by a finite modeled tool bus; removing execution or adding an OS sandbox is forbidden.
- **final_output_boundary**: PARTIAL: environment step/results exist; filtering these is too late for code side effects.
- **evaluator_preservation**: NOT ESTABLISHED: original tests/feedback remain untouched; wrapping all results cannot repair pre-output side effects.
- **capability_parity_feasibility**: NOT_FEASIBLE for audited SDE design under no-redesign constraint.
- **privacy_augmentation_feasibility**: UNKNOWN: architecture has not passed; no representative task sidecar or A/B fixture was certified.
- **transition_class_parity_feasibility**: NOT_FEASIBLE
- **at_least_23_tasks_per_candidate_family_plausibility**: UNKNOWN: pre-result eligibility and disjoint development/confirmatory pools have not been established.

Concrete blockers:

- Direct shared dictionary access in active configured SDE path.
- Generated code side effects are outside the allowed generic mediation model.
- Other AgentVerse designs were not exhaustively audited; this verdict must not be generalized to every configuration.

Pinned source observations:

- [agentverse/agents/base.py:17](https://github.com/OpenBMB/AgentVerse/blob/f90c4bd9680fdd3bcff8c52c9170911a59b23478/agentverse/agents/base.py#L17): Agent objects expose structured name, role and memory fields; absence of any identity is not the rejection reason.
- [agentverse/environments/simulation_env/rules/selector/sde_team.py:52](https://github.com/OpenBMB/AgentVerse/blob/f90c4bd9680fdd3bcff8c52c9170911a59b23478/agentverse/environments/simulation_env/rules/selector/sde_team.py#L52): Normal SDE execution writes code directly into a shared backing dictionary.
- [agentverse/environments/simulation_env/rules/selector/sde_team.py:55](https://github.com/OpenBMB/AgentVerse/blob/f90c4bd9680fdd3bcff8c52c9170911a59b23478/agentverse/environments/simulation_env/rules/selector/sde_team.py#L55): Shared code/test state is read directly to execute code, outside message-memory mediation.
- [agentverse/environments/simulation_env/rules/selector/code_api.py:38](https://github.com/OpenBMB/AgentVerse/blob/f90c4bd9680fdd3bcff8c52c9170911a59b23478/agentverse/environments/simulation_env/rules/selector/code_api.py#L38): Generated Python executes in-process with ordinary builtins; a code-string wrapper is not complete mediation of its runtime side effects.
- [agentverse/memory/chat_history.py:202](https://github.com/OpenBMB/AgentVerse/blob/f90c4bd9680fdd3bcff8c52c9170911a59b23478/agentverse/memory/chat_history.py#L202): Optional memory summarization uses a separate model path without receiving-principal parameter; reachability depends on configuration.
- [agentverse/tasks/simulation/sde_team/sde_team_3players/config.yaml:202](https://github.com/OpenBMB/AgentVerse/blob/f90c4bd9680fdd3bcff8c52c9170911a59b23478/agentverse/tasks/simulation/sde_team/sde_team_3players/config.yaml#L202): The rejected SDE path is connected to an existing public configuration, not merely dead helper code.

## ChatArena native Player/Arena language-game design

Status: **ARCHITECTURE_FAIL**. Repository: [https://github.com/Farama-Foundation/chatarena](https://github.com/Farama-Foundation/chatarena). Revision: `a15802dd89c0d69165bb0b07e70c2bac5a7c4e36`. License: Apache-2.0. Public families in scope: Chameleon, conversation / moderated conversation, board-game environment examples.

Relevant eligible task counts: **not established**. Deep task-count, split, infrastructure and representative augmentation audits were not entered because the architecture did not pass.

- **recipient_identity**: PRESENT: Player.name is passed explicitly as backend.query(agent_name=...).
- **context_provenance**: PARTIAL: role_desc/global_prompt/history_messages and Message.visible_to are structured. Original game secret/gold must remain benchmark-private/trusted where originally supplied.
- **communication_boundary**: PRESENT: MessagePool.append_message and get_visible_messages, scheduled by Arena.
- **shared_state_boundary**: PARTIAL: message API exists; get_all_messages returns backing references. No normal-execution bypass is claimed merely from public mutability.
- **tool_boundary**: ABSENT for audited native Player/Arena design: textual action -> Environment.step is not an existing tool invocation/result/error interface. User explicitly lists tool mediation as HARD.
- **side_effect_boundary**: PARTIAL: language-game state transitions go through step; external tool workflows are not provided by this design.
- **final_output_boundary**: PRESENT: TimeStep observation/reward/terminal and message publication; game-specific scoring remains separate.
- **evaluator_preservation**: PLAUSIBLE for native game scoring but does not supply missing tool capability. Do not reclassify the game secret as a privacy sidecar or change the win condition.
- **capability_parity_feasibility**: NOT_FEASIBLE for the full requested hard interface set; message-only parity would be a narrower claim.
- **privacy_augmentation_feasibility**: UNKNOWN: architecture has not passed; no representative task sidecar or A/B fixture was certified.
- **transition_class_parity_feasibility**: NOT_FEASIBLE
- **at_least_23_tasks_per_candidate_family_plausibility**: UNKNOWN: pre-result eligibility and disjoint development/confirmatory pools have not been established.

Concrete blockers:

- No native generic tool-call/result/error interface on the inspected execution path. Adding tools changes the candidate capability set.
- Rejection interprets the explicitly HARD tool requirement literally. If human permits absent-channel N/A, this design needs re-audit, not automatic acceptance.
- No claim that prompt templates, topic words, game seeds or permutations are independent public semantic tasks.

Pinned source observations:

- [chatarena/agent.py:112](https://github.com/Farama-Foundation/chatarena/blob/a15802dd89c0d69165bb0b07e70c2bac5a7c4e36/chatarena/agent.py#L112): Backend receives a structured runtime player name.
- [chatarena/message.py:78](https://github.com/Farama-Foundation/chatarena/blob/a15802dd89c0d69165bb0b07e70c2bac5a7c4e36/chatarena/message.py#L78): Existing message publication API.
- [chatarena/message.py:127](https://github.com/Farama-Foundation/chatarena/blob/a15802dd89c0d69165bb0b07e70c2bac5a7c4e36/chatarena/message.py#L127): Existing recipient-specific message access API.
- [chatarena/message.py:103](https://github.com/Farama-Foundation/chatarena/blob/a15802dd89c0d69165bb0b07e70c2bac5a7c4e36/chatarena/message.py#L103): All-message access exposes a mutable alias; this alone is not proof of a normal-execution bypass.
- [chatarena/arena.py:50](https://github.com/Farama-Foundation/chatarena/blob/a15802dd89c0d69165bb0b07e70c2bac5a7c4e36/chatarena/arena.py#L50): Native loop is observation -> textual player action -> environment step, with invalid-action retries.
- [chatarena/environments/base.py:125](https://github.com/Farama-Foundation/chatarena/blob/a15802dd89c0d69165bb0b07e70c2bac5a7c4e36/chatarena/environments/base.py#L125): Base environment exposes an action step, not a generic tool-call/result/error interface.
- [chatarena/environments/chameleon.py:97](https://github.com/Farama-Foundation/chatarena/blob/a15802dd89c0d69165bb0b07e70c2bac5a7c4e36/chatarena/environments/chameleon.py#L97): Chameleon game gold is initialized in the environment and must not be relabeled as a synthetic privacy fact.
- [chatarena/environments/chameleon.py:158](https://github.com/Farama-Foundation/chatarena/blob/a15802dd89c0d69165bb0b07e70c2bac5a7c4e36/chatarena/environments/chameleon.py#L158): Original game scoring is task-specific deterministic logic.

## AWS Multi-agent Collaboration Scenario Benchmark standalone release

Status: **ARCHITECTURE_FAIL**. Repository: [https://github.com/aws-samples/multiagent-collab-scenario-benchmark](https://github.com/aws-samples/multiagent-collab-scenario-benchmark). Revision: `cb82575c0846bb147423bebacc8597bc24196142`. License: MIT-0 source; CC-BY-4.0 dataset. Public families in scope: travel planning, mortgage financing, software development.

Relevant eligible task counts: **not established**. The README advertises 30 scenarios per domain (90 total); this is not a verified eligible-task count. Deep task-count, split, infrastructure and representative augmentation audits were not entered because the architecture did not pass.

- **recipient_identity**: NOT PROVIDED: source/destination fields in saved input trajectories are not trusted runtime recipient binding.
- **context_provenance**: NOT PROVIDED for execution: scenario/assertions and evaluation input are present, but runtime provenance cannot be established.
- **communication_boundary**: NOT PROVIDED: input trajectory schema is not a message bus.
- **shared_state_boundary**: NOT PROVIDED: tool schemas and sample conversations do not implement a state access API.
- **tool_boundary**: NOT PROVIDED: agents.json describes tools; runnable implementations and generic runtime invocation are absent from this release.
- **side_effect_boundary**: NOT PROVIDED: benchmark runner consumes already-generated conversations.
- **final_output_boundary**: EVALUATOR OUTPUT ONLY: save_results publishes scores, not agent final delivery.
- **evaluator_preservation**: Evaluator source available and separately callable; LLM judge compatibility with MiniMax is untested. Does not make the absent runtime architecture eligible.
- **capability_parity_feasibility**: NOT_FEASIBLE as a standalone runtime candidate; would require supplying a separately audited existing runtime or implementing one.
- **privacy_augmentation_feasibility**: UNKNOWN: architecture has not passed; no representative task sidecar or A/B fixture was certified.
- **transition_class_parity_feasibility**: NOT_FEASIBLE
- **at_least_23_tasks_per_candidate_family_plausibility**: UNKNOWN: pre-result eligibility and disjoint development/confirmatory pools have not been established.

Concrete blockers:

- Release provides data and evaluator, not the original multi-agent execution runtime.
- A custom FlowFence runtime around these tasks is disallowed; a public existing runtime pairing would be a different candidate design requiring its own audit.
- Do not infer original proprietary runtime mediation properties from sample trace fields.

Pinned source observations:

- [README.md:20](https://github.com/aws-samples/multiagent-collab-scenario-benchmark/blob/cb82575c0846bb147423bebacc8597bc24196142/README.md#L20): Repository expects externally prepared trajectories; it does not supply their multi-agent execution runtime.
- [README.md:7](https://github.com/aws-samples/multiagent-collab-scenario-benchmark/blob/cb82575c0846bb147423bebacc8597bc24196142/README.md#L7): README advertises 30 scenarios in each of three domains; no eligibility count is inferred.
- [src/benchmark.py:20](https://github.com/aws-samples/multiagent-collab-scenario-benchmark/blob/cb82575c0846bb147423bebacc8597bc24196142/src/benchmark.py#L20): Available execution path evaluates supplied conversations using an LLM judge.
- [src/benchmark.py:73](https://github.com/aws-samples/multiagent-collab-scenario-benchmark/blob/cb82575c0846bb147423bebacc8597bc24196142/src/benchmark.py#L73): Evaluator helper depends on module-scope loop index; recorded as a defect, not repaired.
- [README.md:75](https://github.com/aws-samples/multiagent-collab-scenario-benchmark/blob/cb82575c0846bb147423bebacc8597bc24196142/README.md#L75): Dataset license is CC-BY-4.0; source is MIT-0.

## What remains unresolved in tau2-bench

This is the only inspected design retained for further architecture investigation, **not a preferred architecture-passing candidate**. The source already has `Role.AGENT`, `Role.USER`, `ToolCall.requestor`, separate agent/user states and a native text runner. It is therefore wrong to reject it merely because the last provider function has no principal argument. An adapter might carry trusted identity from an existing runtime boundary. It must also cover first-turn generation, initialization/reused history, user-side role flipping and tool errors; this audit does not certify that coverage.

Likewise, `sync_tools()` is an existing finite hook, so its use of mutable DB objects does not by itself establish that a redesign is necessary. However, it transfers information in both directions using domain helpers and direct field writes. A complete static argument must demonstrate mediation **before** cross-principal state publication, including synchronization during construction, initialization and tool dispatch. Treating only tool arguments/results as mediated leaves this path unexplained. Replacing DB objects, adding ownership-aware state infrastructure, or patching individual fields/handlers would violate R0 constraints.

Native environment evaluation reconstructs predicted and gold environments and verifies replayed mutating-tool responses. A candidate design must distinguish the original execution record from delivered model-visible views without lying about what a recipient saw, disabling strict checks, changing gold, or applying privacy policy to evaluator-private data. A potential raw-versus-delivered-view split is a question for audit, not an approved adapter design or a demonstrated evaluator failure.

Resolving these three questions requires a source-level boundary map or a concrete counterexample. No scientific outcome can resolve them. If any requires runtime redesign, reject the scoped design; do not continue repairing it. Airline/retail alone must not silently replace the preferred three-family plan or reduce the 60-task target.

## Transition-class methodology retained

No architecture-passing design exists in this audit, so no complete transition-class parity certificate is asserted. For the unresolved tau2 native text design, the finite classes visible in source are:

| Transition type | Existing source boundary | Static parity estimate / unresolved issue |
|---|---|---|
| Construction and initialization | build_text_orchestrator, get_init_state, Environment.set_state | UNKNOWN: bind both principals before any first call or sync. |
| Planner / delegation | Native text customer-service path has no separate planner-worker graph | N/A for this native design, not a capability removed from it. |
| Model invocation | agent/user generate_next_message and generate | UNKNOWN: preserve recipient/provenance across all calls and role conversion. |
| Communication | Orchestrator.step, from_role/to_role | FEASIBLE locally: same scheduler and opportunities; not a whole-runtime PASS. |
| State read/write and synchronization | get_response, make_tool_call, sync_tools, set_state | UNKNOWN: generic pre-publication domination remains unresolved. |
| Tool input/result/error | ToolCall, get_response, ToolMessage | FEASIBLE locally: same tools, permissions, exceptions; must include state effects. |
| Result propagation | trajectory append/extend and per-agent state update | UNKNOWN: raw execution record versus delivered view and mutable aliases. |
| Termination | is_stop, communication/error limits, timeout and _finalize | UNKNOWN: wrappers must retain original failure/stop order and limits. |
| Final publication | get_messages/get_trajectory, SimulationRun | FEASIBLE locally: requires mediation at delivery as well as export. |
| Evaluator invocation/replay | run_simulation, evaluate_simulation, predicted/gold set_state | UNKNOWN: unchanged strict replay and evaluator-private context. |

Both defenses must receive identical model, pre-defense context, roles, tools, permissions, scheduler, communication opportunities, state access, failure handling, evaluator and stopping semantics. No arm may win by a reduced capability set. No EXACT_IFC weakening, recognizer edit or FlowFence-specific handler is proposed. The other designs are NOT_FEASIBLE for the scoped hard requirements, as recorded in JSON.

## Task counts and privacy augmentation

Architecture-first short-circuiting is intentional: none passed, therefore no confirmatory or development task identifiers were chosen, no deep count/eligibility audit was performed, and no repository's advertised size is used to satisfy the 23-per-family requirement. UNKNOWN is different from INSUFFICIENT_TASKS: a lack of eligible-task certification is not proof of numerical insufficiency. Game seeds, role permutations and topic substitutions are not automatically independent semantic tasks.

The existing PrivacyInstance proposal was read from the completed Gate A worktree's `PRIVACY_AUGMENTATION_SPEC.md`. It supports synthetic protected fact, type P1–P4, authorized principals, forbidden recipients/surfaces, contamination surface and private A/B references, with original gold/evaluator unchanged. The prior frozen-recognizer fixture success is retained as **prior fixture evidence only**. It does not certify any new benchmark task.

For a future architecture-passing candidate, representative-only static screening must establish semantic plausibility, an authorized owner and forbidden recipient/surface, no clean requirement for unauthorized raw disclosure, raw-value-free A/B artifacts, actual compatibility with the unchanged recognizer, and unchanged original gold/evaluation. These are all unverified for the candidates here. Do not substitute ChatArena's game secret or tau2 task-required customer facts for orthogonal synthetic facts: withholding existing task-required data changes the task.

## Prior evidence and repository isolation

The completed MARBLE Gate A evidence at `/private/tmp/flowfence_gate_a_worktree_20260918` was read only (HEAD `9615ca34d166c8c9f75c0c037626956512b0c251`). Its conclusion is preserved: tasks are not scientifically rejected; the pinned runtime fails the required generic receiving-principal and shared-state mediation architecture; both native and permission-only E4-B are rejected, including the contradictory reply schema. Frozen recognizer audit, transition-class parity, pre-result eligibility, evaluator preservation and generic mediation boundary auditing remain the successful methodology.

This audit uses a new branch `codex/aamas2027-benchmark-replacement-r0` in `/private/tmp/flowfence_r0_20260918`, based on existing checkout HEAD `2a179d3`. It does not merge or cherry-pick the MARBLE branch. R3 and Gate A artifacts are therefore referenced externally, not copied into or rewritten in this older base. Existing dirty changes in the user's original worktree were preserved. The requested global default rule is already present in `/Users/crazy/.codex/AGENTS.md`; it was not duplicated.

## Validation and limits

Validation is static source-anchor existence, candidate JSON field/status/count checks, unchanged candidate Git worktrees, unchanged Gate A worktree, scoped file diff and whitespace checks. Results, check descriptions and Git commands are saved in `artifacts/aamas2027_benchmark_replacement_r0/VALIDATION.json`. No candidate dependencies were installed, no candidate code was imported, and no model credentials were accessed. Reading Python source and parsing report JSON are not benchmark execution.

This is a four-design bounded survey, not exhaustive public-benchmark coverage. No reproduction, model compatibility, clean utility, contamination effectiveness, scientific superiority or cross-provider generalization is claimed. The source checkouts remain local in `/private/tmp/benchmark_r0_sources/`; pinned public links permit reinspection if temporary directories are removed.

## Human decision and next step

**Do not select an E2 benchmark yet.** Retain the full target and the closed MARBLE decision. The next useful work is a focused **R0 static-only** resolution of tau2 principal/state/evaluator boundaries, or auditing another existing public runtime design under the same hard requirements. There is no selected runtime combination and no preferred passing shortlist. No new gate is opened, and no development or formal execution is authorized.

FORMAL_MODEL_RUNS_EXECUTED: 0
DEVELOPMENT_MODEL_RUNS_EXECUTED: 0
R3_MUTATED: NO
MARBLE_MUTATED_AFTER_GATE_A: NO
