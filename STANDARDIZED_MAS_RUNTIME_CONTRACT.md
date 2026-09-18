# Standardized multi-agent harness contract — P0 proposal

Status: **P0 design proposal, not an implemented or certified runtime**. Date: 2026-09-18.
Native benchmark-runtime search is CLOSED. No dataset search/selection, development-task selection, benchmark integration, model generation, Gate B, R3 change or frozen-recognizer change is authorized here.

E2_PIVOT_ARCHITECTURE: FEASIBLE (architecture/design level, conditional on source acceptance and later implementation verification).

## One fixed orchestration template

Use one coordinator and two persistent workers for every E2 task family. They are **modeled principals**, not provider accounts: coordinator/planner, worker 1 and worker 2. A non-generating tool/environment principal owns task-effect staging; each modeled external sink has a registered identity. The original utility evaluator is a separate trusted component, outside the runtime communication graph. It cannot delegate, publish agent context or participate as a worker.

The proposed binding to existing frozen-defense IDs is coordinator→`planner_agent`, worker 1→`finance_agent`, worker 2→`doc_writer_agent`. These legacy strings are opaque registry identifiers, not financial/document personas and not role inference. All tasks use the same generic role prompts. Their existing frozen privilege levels remain unchanged; new family-specific privilege systems are not invented. Internal tool/environment events must declare their actual sink identity and an explicitly reviewed mapping using existing semantics; unknown frozen IDs retain the existing fallback, never silently become privileged. External effects may use the existing external/tool category only when its semantics really match. A family requiring unsupported distinctions is ineligible until a separate human design decision; P0 does not modify a registry or certify that mapping for any family.

A single logical cooperative assistant's public capabilities are shared across these three principals. Default E2 communication is a fixed fully connected coordinator/worker graph, with explicit directed edges. All three can propose allowed source tools through the same broker; a predeclared family profile may bind a tool to a worker if the full original capability remains reachable with no added privilege or hidden information. Prefer identical permissions across roles. No per-task role, privileged expert, extra agent, custom DAG or outcome-driven role assignment is allowed. No alternative template is currently proposed.

Execution policy:

1. The coordinator receives the public objective and structured initial task state through the context builder.
2. It proposes delegation, messages, state operations, tool use or finalization through a fixed action grammar.
3. The dispatcher validates registered target/tool IDs and graph permissions, then applies the appropriate common release boundary.
4. A selected worker receives a task artifact and may reason, use its permitted tools, send messages or return artifacts. The coordinator may issue further delegation or tool requests from the current released state.
5. A source-compatible final answer/state is published and the original evaluator is invoked outside the runtime.

Next worker, delegation order, hop count, tool selection and message sequence are model-generated decisions, constrained by the same graph and budgets. A deterministic FIFO dispatcher processes the resulting proposals; it does not encode a task DAG. Concurrent calls are unnecessary for this design: serial, resumable message turns simplify atomic publication without constraining the generated communication sequence. The exact scheduling algorithm and global caps are preregistered by family before development-task selection, not adjusted to individual task IDs or defense outcomes.

Shared total task-tool budgets preserve any original episode limits across all workers combined, rather than multiplying allowances by agent count. Original permitted capabilities must remain available. For sources with no comparable generation budget, the experimental total token/turn cap is disclosed before task selection; original-runtime score comparability is not claimed. If a cap removes a required source capability or makes its valid task protocol unrepresentable, reject that family profile. Algorithmic decomposition may change difficulty; this is a validity threat, not something P0 can promise to eliminate.

## Explicit model invocation and typed provenance

The runtime, never the model, constructs `ModelInvocation`. It contains `recipient_principal`, nullable `sender_principal`, `authorization_context`, typed context parts, `task_family_id`, `tool_permissions`, and provider/model-profile references. Identity derives from the issued principal handle and dispatcher routing. No prompt inspection, stack inspection, role-string heuristic or task-specific identity rule is allowed.

Context categories:

| Category | Meaning | Who can provide it / how it is consumed |
|---|---|---|
| TRUSTED_PRIVATE | Approved system/role instructions and deliberately installed private initial context | Trusted initialization only; read only by its authorized principal. A model cannot create this classification. |
| RUNTIME_SHARED | Messages, generated summaries, shared artifacts and model-derived private scratch | Provenance follows producer and parents; all cross-principal/publication/access paths mediate it. Private storage does not make content trusted. |
| TASK_STATE | Original public task inputs and current committed source-semantic state | Family adapter identifies fields from source schema; runtime uses registered handles and audience. Hidden gold cannot be relabeled as task state. |
| TOOL_RUNTIME | Tool outputs/errors and state-effect artifacts | Tool broker labels producing tool, call and source-state revisions before release. |
| EVALUATOR_PRIVATE | Gold/reference actions, hidden tests, evaluator assertions/prompts and private grading state | Separate evaluator port/store only; rejected in ModelInvocation, state publication and tool-runtime context schemas. |

`experiments/e2_pivot_p0/HARNESS_SCHEMA.json` separates runtime parts from evaluator-private references. It is a shape prototype. Schema validity cannot prove that a label or principal was issued by a trusted component; dispatcher/store authority checks remain required implementation obligations. Model-authored requests may name permitted actions/targets, but cannot set authorization, provenance, trust labels, policy decisions or raw content references outside their issued scope.

Each artifact has a runtime-generated sequential ID, producer, owner, immutable payload reference, provenance category, parent IDs, family and audience. IDs are not content hashes. Data-bearing titles, paths, keys, tool arguments, errors and metadata must either be fixed registered identifiers or be part of the mediated payload. The logger must not smuggle payloads into IDs. Content copied or summarized from runtime artifacts stays runtime-derived even if the model stores it privately. Legitimate original task material that also appears in gold must be provided through the independently documented public input path, never by exposing the gold record.

Private/trusted self-context is not indiscriminately filtered as an untrusted artifact. PrivacyInstance facts enter only their authorized private context. A later export, use in a tool argument or message still crosses its relevant release boundary. The original utility evaluator and any evaluator model receive their required private material via the evaluator port, not through the experimental policy.

## Ownership-aware state and generic access/publication

Only a state service owns authoritative data. Actors and adapters never obtain mutable backing references. Generic JSON values, byte artifacts and opaque handles represent all families; the runtime does not contain task-specific state classes. An adapter may serialize source-native models at its family edge, but cannot give those objects to workers or retain live aliases into committed state.

Required APIs (proposed interfaces, not implemented):

- `read(actor_handle, object_id, expected_revision, purpose)` returns an immutable per-recipient view plus source lineage after the read-release decision.
- `propose_publish(actor_handle, target, payload_ref, audience, parent_refs)` proposes an artifact/message/history entry; the service owns append and routing.
- `propose_patch(actor_handle, object_id, base_revision, operations, audience)` proposes generic set/delete operations without changing live state.
- `commit(proposal_id, release_receipt, expected_revisions)` atomically installs only the approved typed values and advances ordinary integer revisions.
- `append_history(...)` uses the same publication service; `private_put(...)` remains owner-scoped and cannot create trusted provenance.

The same store handles private memory, shared task state, artifacts, per-principal history and tool state references. Every shared read and publication has a generic interception point; private→shared moves are explicit publications, never assignment of a backing dictionary. Stale revisions fail with a common typed conflict and leave state unchanged. This uses ordinary ownership, revision checks and transactions; no new hash/freeze mechanism is necessary.

Even for trusted tool computations, use a detached private draft or immutable input snapshot, never the formal store's backing object. Draft writes are not yet modeled publication, are not visible to agents/other tools, and cannot perform external I/O. A generic serialized diff may become a StateProposal only if the adapter can demonstrate that all original effects are represented faithfully. A tool that leaks a reference, runs uncontrolled model-produced code, invokes callbacks that publish mid-computation or hides effects cannot be accepted. No OS sandbox is proposed as a workaround.

## Generic tool contract and effect protocol

`ToolCall` includes calling principal, registered tool name, structured arguments, authorization metadata, state read/write declarations, result audience and publication target. `ToolResult` includes a payload reference, structured error, proposed state/effect references and original-call lineage. Original argument/result schemas remain family-owned public interfaces; the harness uses the same invocation envelope for every tool and defense. No FlowFence-only tool behavior exists.

The broker resolves declared state reads through the read API, mediates the full outgoing argument artifact, validates the released value against the original tool schema, and calls the registered tool transition. A tool transition must either be read-only or produce a complete **proposal** for effects and result; it cannot commit formal/shared/external state itself. Both proposed effects and the tool result are released through generic boundaries before becoming observable. The result audience and state audience are separate: checking a result is not checking a DB write.

For an internal effect, commit accepted state patches atomically and then publish a result consistent with the actual commit. If a source tool requires atomic all-or-nothing output/state behavior, its entire declared transaction is accepted or rejected; no partial arbitrary patch subset is applied. If a transformed value violates a source schema or invariant, return the common blocked/invalid-release status with no effect, never task-specific repair. Defensive intervention may cause ordinary task failure; it may not fabricate a success result.

For a modeled external effect, require a complete prepared request/publication object whose semantic effect can be checked **before** sending. A broker-owned connector performs only the approved operation; original source-defined receipts/results re-enter through TOOL_RUNTIME. If an API creates hidden onward content or irreversible effects that cannot be fully mediated from the prepared request, reject that source capability/family. Side-effecting APIs need declared retry/idempotency behavior; an uncertain external commit is recorded as UNKNOWN and not silently repeated. A transactional local stub is allowed only if it is the source's permitted environment, not a convenience replacement for a required real service.

Tool computation errors are typed payload artifacts (code, safe message reference, retry class), mediated before model visibility. Stack traces and payload-bearing exception strings remain private diagnostics. Source-defined exceptions and failure behavior must survive the family serialization adapter; fabricated success, discarded hard calls or removed tools are forbidden.

## Seven generic boundaries and architectural coverage argument

| Boundary | Dominates | Mechanism in this design |
|---|---|---|
| B1 Model context ingress | Every provider request for a modeled runtime principal | Only context builder can invoke provider; handles resolve authorized typed context, runtime parts pass release. |
| B2 Inter-agent publication | Delegation, messages, replies, summaries, worker return | Only message service enqueues immutable released artifacts with explicit destination. |
| B3 State publication/access | Private export, shared memory/state/artifact/history read/write | Only state service reads and commits; no backing-object alias is returned. |
| B4 Tool arguments | Model-generated or delegated tool input | Only tool broker dispatches registered tools after argument release. |
| B5 Tool results/errors | Results before participant history/context | Broker output becomes typed artifacts, never direct callback to an agent. |
| B6 Modeled shared/external effects | Tool/scheduler-mediated state publications and external sends | Proposal→release→typed validation→commit; no tool-owned direct commit. |
| B7 Final output | User-visible answer/state/output file publication | Final publisher consumes released artifacts before serialization/export. |

Proof sketch under explicit assumptions: initialization installs typed objects; each participant can emit only action proposals; every provider/tool/store/message/export capability is held by one trusted service; all service outputs re-enter as typed artifacts or declared effects. Inductively the only new model-visible or shared/external publication is produced by one of B1–B7. Draft storage and evaluator-private stores are not modeled recipients. Thus there is no modeled backing-state bypass in the **specified runner**. This is a design invariant, not evidence that code enforcing it exists.

Assumptions: trusted runtime services and accepted family adapters follow the contract; there is no arbitrary untrusted Python/plugin execution, unsupervised network/filesystem effect, covert/timing side-channel claim or malicious host. Internal trusted diagnostics are not claimed mediated unless promoted to an explicit modeled recipient; any such export must use B7. No broad security claim follows from JSON Schema passing.

## Structural EXACT_IFC / FLOWFENCE_R2 parity

Create one episode configuration and one implementation path. It contains original task input, role template, model profile, common prompts, tool schemas/permissions, graph, dispatcher, state APIs, budgets, failure/retry rules, evaluator descriptor and stopping criteria. The sole arm-dependent input to release is the frozen defense selector; its outputs may naturally change later generated actions/context. Same pre-defense context means identical input at a paired boundary test and identical exogenous setup, not forced identical endogenous trajectories after interventions.

Reuse the existing frozen callables, including EXACT_IFC's actual `ifc_safeview` route and FLOWFENCE_R2's delegated legacy behavior. Do not reimplement them as a cleaner invented exact-then-recognizer algorithm. Do not provide task ID, gold, expected match labels, condition names or attack annotations to defense decisions. Task-family/provenance fields are trusted transport metadata used by the common builder; the defense projection exposes only the existing permitted fields. Both arms receive the same projection, policy registry and full artifact before any release.

Map surfaces before task selection: shared raw state→`shared_raw`, shared document artifacts→`shared_doc`, internal delegation/message→`internal_message`, customer/external message→`external_message`, final→`final_output`; `safe_view` and `vendor_send_tool` only for their existing meanings. Tool argument/result/effect events must declare a faithful existing surface/target-zone profile; do not extend R2's PROPAGATION_SURFACES or suppress an unsupported channel to pass. If a source needs an unrepresentable channel or policy abstraction, reject the family. These are proposed mappings requiring later same-input fixtures, not new recognizer rules.

Generic serialization examines all data-bearing content, including structured keys/metadata; it does not add semantic decoding rules to the recognizer. A frozen whole-artifact quarantine or rewrite must remain a valid output of the source interface or be treated uniformly as a blocked operation. Per-task repair, detector tuning, defense-specific retry, fallback model, extra context, extra tool or evaluator bypass is forbidden. Common hard blocks and failure handling are retained.

## PrivacyInstance attachment

Preserve the fields `protected_fact`, `protected_fact_type`, `authorized_principals`, `forbidden_principals_or_surfaces`, `allowed_abstraction`, `contamination_surface`, `contamination_artifact_A`, `contamination_artifact_B`, `recognizer_expected_match`, `privacy_observation_surfaces`. In the machine-readable transport schema, fact/A/B are private-store references; the existing private materialized instance retains the actual values. This is storage indirection, not deletion or weakening of those fields.

Use synthetic facts unrelated to the source gold/success criterion, installed only in authorized private context by trusted initialization. Workers collectively retain every original required public capability/input. Policy may not hide task-required original facts to manufacture leakage. A clean task inherently requiring unauthorized raw disclosure is ineligible. A/B are untrusted artifacts on a predeclared existing runtime surface, contain no raw protected value and must match the unchanged recognizer in later static fixture checks; CLEAN contains neither contaminated artifact. Match expectations and condition labels stay in the private experiment/audit store, not defense inputs.

No task-specific role invention, task-goal rewrite or bespoke tool is used to make a PrivacyInstance plausible. P0 proves the schema can attach such references; it does not certify semantics, detector coverage or attack pressure for any unselected task. Preserve the 15/15/15/15 E2 target and later inspect all proposed eligible instances before result observation.

The shape prototype includes structured tool arguments/results and immutable payload references. The broker must ensure these represent the same canonical payload and apply the original family tool schema; schema examples alone do not establish that consistency. Arrays of permissions may be empty; actual audience membership and reference access are checked by the issuing runtime service.
