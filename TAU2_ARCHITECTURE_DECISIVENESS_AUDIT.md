# R0-τ architecture, evaluator, data and decision audit

Date: 2026-09-18. Phase: baseline scouting, authorized R0-τ audit only.
Canonical: `b7ea9074c1cba482b30687fecdb5c8425fd6f619`. Verified: `864350a8971a8f8ee9e7b8472e2edc380a806b0c`.
Route: native text/half-duplex `LLMAgent` + `UserSimulator`, airline/retail/telecom, base split. Ground-truth/solo agents, voice/full-duplex, knowledge/shell domains and custom assistant teams are not substituted for this standard route.

AAMAS_BENCHMARK_REPLACEMENT_R0_TAU2: NOT_SUITABLE
TAU2_ARCHITECTURE_STATUS: ARCHITECTURE_FAIL
TAU2_E2_ROLE: AGENTIC_EXTERNAL_VALIDITY_ONLY

Two independent decisions: the standard scientific scope is PARTIAL for original E2; the requested complete state-publication mediation architecture fails without prohibited changes. The scientific label above names the strongest possible role, not permission to execute a failing design. No unresolved bundle remains as the architecture verdict.

## Implementations and provenance

| Item | Sierra canonical/current | Amazon Verified |
|---|---|---|
| Repository | [sierra-research/tau2-bench](https://github.com/sierra-research/tau2-bench) | [amazon-agi/tau2-bench-verified](https://github.com/amazon-agi/tau2-bench-verified) |
| Inspected Git revision | `b7ea9074c1cba482b30687fecdb5c8425fd6f619` | `864350a8971a8f8ee9e7b8472e2edc380a806b0c` |
| Package version | 1.0.1 | 0.2.1-dev |
| Python | >=3.12,<3.14 | >=3.10 |
| Build/runtime | hatchling; LiteLLM >=1.80.15,<1.82.7; local JSON/Pydantic environment | pdm-backend; LiteLLM >=1.65.0; local JSON/Pydantic environment |
| License | MIT | MIT |
| Relationship | Upstream canonical | Public verified derivative of upstream |
| Domains supplied | mock, airline, retail, telecom, banking_knowledge; optional voice | mock, airline, retail, telecom |
| Intended audited route | Native text, three core domains | Native text, three core domains |

Version/runtime/license evidence: [pyproject.toml:7](https://github.com/sierra-research/tau2-bench/blob/b7ea9074c1cba482b30687fecdb5c8425fd6f619/pyproject.toml#L7), [pyproject.toml:10](https://github.com/sierra-research/tau2-bench/blob/b7ea9074c1cba482b30687fecdb5c8425fd6f619/pyproject.toml#L10), [LICENSE:1](https://github.com/sierra-research/tau2-bench/blob/b7ea9074c1cba482b30687fecdb5c8425fd6f619/LICENSE#L1); [pyproject.toml:7](https://github.com/amazon-agi/tau2-bench-verified/blob/864350a8971a8f8ee9e7b8472e2edc380a806b0c/pyproject.toml#L7), [pyproject.toml:10](https://github.com/amazon-agi/tau2-bench-verified/blob/864350a8971a8f8ee9e7b8472e2edc380a806b0c/pyproject.toml#L10), [LICENSE:1](https://github.com/amazon-agi/tau2-bench-verified/blob/864350a8971a8f8ee9e7b8472e2edc380a806b0c/LICENSE#L1). Both public remote HEADs were checked with `git ls-remote` and matched the inspected revisions. These are current commit pins; no claim that a fetched Git release tag points exactly to either HEAD. Verified's package version is a development version, not a discovered stable release tag.

Both core environments and task/evaluator source are public and locally modeled; no proprietary unavailable business backend is required by these core tools. Full dependency installation and complete benchmark reproduction were not attempted. Future model-backed execution still requires provider access. MiniMax compatibility, including required evaluator models, is not demonstrated; no non-MiniMax execution is proposed.

## Architecture verdicts

| Requirement | Verdict | Basis |
|---|---|---|
| PRINCIPAL_BINDING | VERIFIED | Explicit component and typed-role bindings at existing entry points; see dedicated audit. |
| EVALUATOR_PRIVATE_SEPARATION | VERIFIED | Runtime construction receives user scenario/policy; expected actions/assertions live in separate evaluation criteria and evaluator entry points. |
| SHARED_STATE_MEDIATION | NOT_FEASIBLE | No existing generic pre-publication state API for direct tool DB writes and telecom cross-DB sync under the required state-publication interpretation. |
| TOOL_MEDIATION | NOT_FEASIBLE | Arguments/results/errors have common interfaces, but the requested requirement also includes DB mutations that publish modeled state; those are not all mediated by the tool envelope. |
| TRAJECTORY_MEDIATION | VERIFIED | Finite typed send/receive/tool/history/final boundaries are identifiable for interception; no claim that interception preserves grading. |
| EVALUATOR_REPLAY_PRESERVATION | VERIFIED | Existing full execution trajectory is distinct from recipient histories. Preserve actual tool execution records there, mediate recipient views, and record communication/actions faithfully. No extra oracle trace is required. |
| TRANSITION_CLASS_PARITY_FEASIBILITY | NOT_FEASIBLE | Matching wrapper placement alone cannot satisfy complete pre-publication state mediation under these constraints. |

VERIFIED means static boundary/data-flow verification in this scope, not adapter implementation or scientific execution. NOT_FEASIBLE is relative to the required complete mediation and unchanged native protocol; it does not mean the benchmark is defective for its intended use.

## Evaluator-private provenance

The standard LLMAgent receives policy and tool schemas, not gold actions. UserSimulator receives `str(task.user_scenario)` and optional user tools; its private scenario/instructions are intentionally model-visible to the user principal. They are not evaluator-only gold. Each component holds separate system_messages and interaction messages. `Task.evaluation_criteria` supplies expected actions, communication requirements, assertions and reward_basis to scoring after the episode. Initial-state data is a task setup input, not automatically gold merely because evaluator replay also uses it.

EnvironmentEvaluator creates predicted and gold environments separately. Gold initialization and reference actions remain private; an adapter must not filter them. ActionEvaluator matches recorded assistant/user ToolCalls against expected actions. CommunicateEvaluator scans AssistantMessage content for required information. NLAssertionsEvaluator sends conversation text and assertions to a separate judge. Its model must receive evaluator-private material unchanged and must not be mistaken for a runtime user/assistant. Full-duplex conversion is not on this intended path and was not used to resolve its problems.

Canonical evaluator evidence: [src/tau2/evaluator/evaluator_env.py:85](https://github.com/sierra-research/tau2-bench/blob/b7ea9074c1cba482b30687fecdb5c8425fd6f619/src/tau2/evaluator/evaluator_env.py#L85), [src/tau2/evaluator/evaluator_action.py:62](https://github.com/sierra-research/tau2-bench/blob/b7ea9074c1cba482b30687fecdb5c8425fd6f619/src/tau2/evaluator/evaluator_action.py#L62), [src/tau2/evaluator/evaluator_communicate.py:50](https://github.com/sierra-research/tau2-bench/blob/b7ea9074c1cba482b30687fecdb5c8425fd6f619/src/tau2/evaluator/evaluator_communicate.py#L50), [src/tau2/evaluator/evaluator_nl_assertions.py:121](https://github.com/sierra-research/tau2-bench/blob/b7ea9074c1cba482b30687fecdb5c8425fd6f619/src/tau2/evaluator/evaluator_nl_assertions.py#L121), [src/tau2/evaluator/evaluator.py:88](https://github.com/sierra-research/tau2-bench/blob/b7ea9074c1cba482b30687fecdb5c8425fd6f619/src/tau2/evaluator/evaluator.py#L88). Verified: [src/tau2/evaluator/evaluator_env.py:72](https://github.com/amazon-agi/tau2-bench-verified/blob/864350a8971a8f8ee9e7b8472e2edc380a806b0c/src/tau2/evaluator/evaluator_env.py#L72), [src/tau2/evaluator/evaluator_action.py:7](https://github.com/amazon-agi/tau2-bench-verified/blob/864350a8971a8f8ee9e7b8472e2edc380a806b0c/src/tau2/evaluator/evaluator_action.py#L7), [src/tau2/evaluator/evaluator_communicate.py:50](https://github.com/amazon-agi/tau2-bench-verified/blob/864350a8971a8f8ee9e7b8472e2edc380a806b0c/src/tau2/evaluator/evaluator_communicate.py#L50), [src/tau2/evaluator/evaluator_nl_assertions.py:115](https://github.com/amazon-agi/tau2-bench-verified/blob/864350a8971a8f8ee9e7b8472e2edc380a806b0c/src/tau2/evaluator/evaluator_nl_assertions.py#L115), [src/tau2/evaluator/evaluator.py:21](https://github.com/amazon-agi/tau2-bench-verified/blob/864350a8971a8f8ee9e7b8472e2edc380a806b0c/src/tau2/evaluator/evaluator.py#L21).

Evaluator-private state replay after an episode is **not** itself a modeled privacy propagation surface. Its direct DB writes are not used as evidence against runtime mediation. Runtime and evaluator objects can be classified separately at their actual construction/invocation boundaries without changing evaluator code. Native trajectory semantics must be preserved using the existing distinction between execution events and recipient histories, as detailed below. This is independent of the state-publication blocker.

## Runtime state and tool mediation

| State | Ownership / use | Relevant normal access |
|---|---|---|
| Airline FlightDB, RetailDB | Local service environment backing state | Tool methods directly read dictionaries/models and mutate bookings/orders. |
| TelecomDB | Service/provider environment | Agent tools plus telecom synchronization helpers. |
| TelecomUserDB.device/surroundings | User-side modeled device/environment | User tools and sync_tools directly read/write fields; properties expose backing models. |
| LLMAgentState / UserState | Private per-component system/history | Generation adds received messages and own outputs; user role conversion is local presentation. |
| Orchestrator trajectory / pending message | Episode history and next delivery | Same generated message object is appended and assigned for delivery; tool objects likewise stored and routed. |
| Predicted/gold evaluator DBs | Evaluator-private after episode | Fresh reconstruction from task initial state/actions; not runtime publication. |

Environment.get_response provides ToolCall→result/error, dispatching by requestor via make_tool_call/use_tool/use_user_tool. Thus agent arguments, user arguments, model-visible results and serialized exceptions are individually interceptable. The actual domain handlers retain publicly reachable mutable DB references. In telecom, `sync_tools` also bypasses `make_tool_call/use_tool` to call `_get_line_by_phone`, `_get_plan_by_id`, `_set_bill_to_paid`, and copy a service bill's ID/amount into user-side `payment_request`. It runs in construction, task initialization and after tools/steps; it is not an isolated final evaluator operation.

A finite callback named sync_tools is **not** a structured proposed-write/publication API: it mutates both backing objects internally, returns no proposed state transfer, and has no general read/write access layer. A pre-call wrapper sees the old objects, while a post-call wrapper observes publication after mutation. A generic dry-run/copy/commit replacement, ownership-aware DB proxies, or field-specific handling would introduce the state model/redesign expressly disallowed here. Blocking the whole sync would remove native dual-control behavior. Tool input/output mediation alone cannot certify this state-publication requirement. If the human later changes the threat model to *only model-visible tool/message disclosure*, this finding must be re-scoped; it must not be silently treated as the approved stronger state guarantee.

Evidence in both pins: [src/tau2/environment/environment.py:465](https://github.com/sierra-research/tau2-bench/blob/b7ea9074c1cba482b30687fecdb5c8425fd6f619/src/tau2/environment/environment.py#L465), [src/tau2/environment/toolkit.py:138](https://github.com/sierra-research/tau2-bench/blob/b7ea9074c1cba482b30687fecdb5c8425fd6f619/src/tau2/environment/toolkit.py#L138), [src/tau2/domains/telecom/environment.py:39](https://github.com/sierra-research/tau2-bench/blob/b7ea9074c1cba482b30687fecdb5c8425fd6f619/src/tau2/domains/telecom/environment.py#L39), [src/tau2/domains/telecom/user_tools.py:57](https://github.com/sierra-research/tau2-bench/blob/b7ea9074c1cba482b30687fecdb5c8425fd6f619/src/tau2/domains/telecom/user_tools.py#L57); [src/tau2/environment/environment.py:390](https://github.com/amazon-agi/tau2-bench-verified/blob/864350a8971a8f8ee9e7b8472e2edc380a806b0c/src/tau2/environment/environment.py#L390), [src/tau2/environment/toolkit.py:76](https://github.com/amazon-agi/tau2-bench-verified/blob/864350a8971a8f8ee9e7b8472e2edc380a806b0c/src/tau2/environment/toolkit.py#L76), [src/tau2/domains/telecom/environment.py:39](https://github.com/amazon-agi/tau2-bench-verified/blob/864350a8971a8f8ee9e7b8472e2edc380a806b0c/src/tau2/domains/telecom/environment.py#L39), [src/tau2/domains/telecom/user_tools.py:57](https://github.com/amazon-agi/tau2-bench-verified/blob/864350a8971a8f8ee9e7b8472e2edc380a806b0c/src/tau2/domains/telecom/user_tools.py#L57). The telecom environment source is byte-identical at these pins. A method-level fixture executes its unchanged sync body with public in-memory stubs and observes a user-side payment_request even though the stub exposes no generic tool dispatcher. This proves a dispatcher bypass; the broader no-redesign rejection additionally rests on the source's direct state access, not on the fixture alone.

## Trajectory and publication inventory

| Event | Producer → recipient | Model-visible / stored / later use | Existing interception boundary |
|---|---|---|---|
| User text | user → assistant | Received into assistant history; stored in episode trajectory; later evaluator input | UserSimulator return / assistant generate_next_message input, typed Role route |
| Assistant text | assistant → user | Received into user history; stored; later scoring | LLMAgent return / user generate_next_message input |
| Assistant tool call | assistant → ENV | Arguments execute; call is stored in assistant history/trajectory; not forwarded as user speech | Environment.get_response / make_tool_call |
| User tool call | user → ENV | Telecom tool arguments execute; user history and trajectory store it; not assistant speech | Same interface, requestor=user |
| Tool result | ENV → originating assistant/user | ToolMessage/MultiToolMessage enters that principal's history and trajectory | get_response return / receiving generate_next_message input |
| Tool error | ENV → originating principal | Serialized exception and error flag; error counter/stopping still native | get_response exception/result envelope |
| Environment mutation | tool or sync → shared/provider/user state | Indirectly model-visible in later tool observations; not necessarily a distinct trajectory event | Tool dispatcher only partially dominates; direct sync state writes are blocker |
| Initial history | task setup → appropriate principal state | Typed validity predicates choose histories; copied initial trajectory | get_init_state / initialize |
| Termination/final | orchestrator → stop hooks / SimulationRun / scorer | Stored trajectory exported; stop hooks may receive final pending message; standard hooks do not generate | stop / _finalize or run / get_trajectory |

Provider logs, raw_data diagnostics and caches are not an existing benchmark-semantic evaluator-only delivered-message channel. They cannot be promoted into one for grading. Public exposure of diagnostic data would require its own export boundary; nothing here authorizes publishing raw traces.

## Exact evaluator replay preservation finding

EVALUATOR_REPLAY_PRESERVATION: VERIFIED — static feasibility using existing execution-record / recipient-history separation, **not** arbitrary interchangeability of raw and delivered trajectories and not implementation certification.

1. **Fresh replay:** yes. EnvironmentEvaluator reconstructs predicted state from recorded actions/results in a fresh environment, and gold from initial history plus expected actions.
2. **Final DB scoring:** yes. DB equality and/or explicit environment assertions contribute by reward_basis. Action and Communicate evaluators read the same full execution record.
3. **Raw requirement:** native tool execution results and actual executed arguments are required for replay; provider raw_data is not required. A recipient-visible safe view is not a substitute for a tool's execution result.
4. **Existing structural separation:** `Orchestrator.trajectory` contains both principals' events. Agent and user each have separate state/history and existing typed history predicates; user tool results are present in the trajectory but excluded from assistant history, and vice versa. get_trajectory makes an evaluator serialization copy. The full trajectory is therefore already a privileged execution record, not a promise that every item was visible to every principal.
5. **Allowed preservation route:** retain actual native ToolCall/ToolMessage execution events in the existing trajectory. At the existing recipient entry point, provide a separate safe model-visible value/history view. No additional evaluator-only trace or oracle data is needed; the original private execution store is already present. Do not mutate the shared ToolMessage object in place to implement its recipient view. No state wrapper or adapter was implemented here.
6. **Communication/actions must stay truthful:** when an assistant/user message is transformed before publication, its trajectory entry must represent the actually published content. When tool arguments are transformed or a call is blocked, the record must represent actual execution, not the model's unexecuted proposal. These changes belong at existing output/dispatch boundaries and use the same native message schema. Keeping every original proposed message and scoring it as delivered/executed is forbidden.
7. **No new gold channel:** evaluator Task criteria/reference DB remain original and private. Preserving a native execution event already stored by the runtime is distinct from manufacturing a raw gold/evaluator copy to award credit. The latter is neither required nor permitted. Adding arbitrary custom recipient-specific record semantics would need a new audit; this verdict concerns the fixed single-assistant/single-user typed route.

The method-level fixtures deliberately test two **invalid strategies**: substituting a released-view string for a native tool execution result raises ValueError in unchanged set_state; scoring a withheld assistant phrase from an unchanged original communication trace awards false communication credit. They do not prove that every existing-boundary adapter is impossible. Native own-versus-other tool-history predicate fixtures confirm that privileged execution history and modeled recipient history are already structurally different. The correct source-level route above avoids both errors without modifying any evaluator.

Current upstream skips non-mutating/unknown-tool history cases and supports strict=False for regrading; standard live scoring remains strict. Verified replays all tool pairs with no strict option. **Neither strict flag nor gold/action/assertion code needs to be changed** when the existing trajectory records actual tool execution and actual published communication. A future adapter would still need deterministic end-to-end parity validation; none is authorized in this audit.

These findings supersede the earlier provisional interpretation that original/delivered result mismatch alone proves evaluator incompatibility. The single remaining decisive architectural failure is the stronger shared-state pre-publication requirement, not evaluator-private replay after the episode.

## Task inventory and representative privacy plausibility

Counts below are source metadata required for implementation comparison, not task eligibility certification. The hard architecture failure prevents proceeding to the full K eligibility/selection stage.

| Domain | Canonical base | Verified base | Other splits in both | Task file rows |
|---|---:|---:|---|---:|
| Airline | 50 | 50 | train 30, test 20 | 50 |
| Retail | 114 | 114 | train 74, test 40 | 114 |
| Telecom | 114 | 114 | train 74, test 40, small 20, full 2285 | 2285 |

Base is the existing default loader split. IDs are unique and all split references resolve in both pins. The 2285 telecom generator combinations are **not** substituted for 114 base tasks or treated as independent workflow families. Airline test-only has 20, so cannot itself provide 3+20 disjoint examples; base has numerical headroom. No task IDs have been selected for development or confirmation.

Pinned split evidence: [data/tau2/domains/airline/split_tasks.json:56](https://github.com/sierra-research/tau2-bench/blob/b7ea9074c1cba482b30687fecdb5c8425fd6f619/data/tau2/domains/airline/split_tasks.json#L56), [data/tau2/domains/retail/split_tasks.json:120](https://github.com/sierra-research/tau2-bench/blob/b7ea9074c1cba482b30687fecdb5c8425fd6f619/data/tau2/domains/retail/split_tasks.json#L120), [data/tau2/domains/telecom/split_tasks.json:2429](https://github.com/sierra-research/tau2-bench/blob/b7ea9074c1cba482b30687fecdb5c8425fd6f619/data/tau2/domains/telecom/split_tasks.json#L2429); [data/tau2/domains/airline/split_tasks.json:56](https://github.com/amazon-agi/tau2-bench-verified/blob/864350a8971a8f8ee9e7b8472e2edc380a806b0c/data/tau2/domains/airline/split_tasks.json#L56), [data/tau2/domains/retail/split_tasks.json:120](https://github.com/amazon-agi/tau2-bench-verified/blob/864350a8971a8f8ee9e7b8472e2edc380a806b0c/data/tau2/domains/retail/split_tasks.json#L120), [data/tau2/domains/telecom/split_tasks.json:2429](https://github.com/amazon-agi/tau2-bench-verified/blob/864350a8971a8f8ee9e7b8472e2edc380a806b0c/data/tau2/domains/telecom/split_tasks.json#L2429).

One pre-existing first file record per domain was inspected as a representative, not selected: airline task 0 (cancellation/refund refusal), retail task 0 (product-option exchanges), telecom first record (mobile-data roaming diagnosis). Both pins contain those examples, with minor retail wording differences. Reading representatives does not authorize their later inclusion.

| Domain | Privacy plausibility | Authorized / forbidden / plausible synthetic sidecar |
|---|---|---|
| Airline | PLAUSIBLE | Assistant owns internal service-session metadata; customer/user and customer-visible reply are forbidden. Metadata is unrelated to original reservation/refund eligibility. |
| Retail | PLAUSIBLE | Assistant owns internal case/session metadata; customer/user and outward reply are forbidden. The public order, product IDs and exchange criteria remain fully available. |
| Telecom | PLAUSIBLE | Assistant owns internal support-session metadata; user/device-visible output is forbidden. Original phone status, payment facts needed by the task and diagnosis goal remain unchanged. |

For each, four illustrative types are an internal discretionary handling-budget number, internal case reference, internal triage category and nonfunctional service-session token. No actual credential is used. Synthetic facts can live in authorized private assistant context; they are not substituted for original customer IDs, payment details or evaluator gold. The clean task does not require disclosing this added sidecar. An untrusted incoming dialogue artifact can carry pre-existing A/B request phrases without containing the protected value. This uses the existing user→assistant surface and adds no worker principal, task goal or tool handler.

The unchanged frozen recognizer's pattern tuples and three called functions were evaluated directly from the read-only Gate A source on 24 public static examples (3 domains × 4 fact classes × A/B), with raw-value absence and a clean negative control. No new rule or defense implementation was added. This proves fixture recognition only; not runtime attack placement, efficacy, reconstructability or eligible-task balance. Original goal/evaluator data were never changed.

TASK_SCALE_FEASIBILITY: UNRESOLVED. Raw counts numerically permit 3+20 per domain, but **60 eligible semantic tasks with P1/P2/P3/P4=15 each have not been certified**. Full eligibility audit is not continued after architecture failure; representative plausibility cannot prove the 60-task balance. The original preferred 20+20+20 and 1080-episode design remain unchanged.

## Canonical versus Verified compatibility

CANONICAL_VERIFIED_COMPATIBILITY: MATERIALLY_DIFFERENT_BENCHMARK_AT_INSPECTED_PINS

This means different task/evaluation semantics at these two revisions, **within the same benchmark lineage**; it does not mean Verified invented a new assistant-team protocol. It cannot be treated as a data-only interchangeable install of current canonical.

Verified documents policy, DB-reference, impossible-scenario and instruction-ambiguity corrections. Current Sierra already includes later corrections and runtime/evaluator developments. Raw comparisons find the same task-ID sets and identical telecom task records, but 10 airline and 28 retail user_scenario records differ. After accounting for the common default reward_basis, 9 airline and all 114 retail evaluation_criteria records differ. Raw full-record differences (50 airline / 114 retail) are not all independent substantive task corrections; explicit defaults alone explain some differences.

Most importantly, canonical retail includes 112 base tasks whose reward_basis includes NL_ASSERTION (40 have nonempty assertions); canonical ALL triggers the NL path when required. Verified airline/retail omit reward_basis and inherit DB+COMMUNICATE; its ALL does not automatically run NL assertions. Verified has 8 retail records with nonempty NL assertions, which are not part of that default basis. The default judge models also differ and are hardcoded non-MiniMax defaults in config. No judge was called, changed or silently dropped to meet the provider constraint.

Canonical environment replay skips non-mutating/unknown-tool history cases and accepts a strict parameter; Verified replays every tool pair. Canonical has runner/build/simulation modules, expanded message/audio types, user-tool filtering, typed tool metadata and additional evaluator modes; Verified uses run.py and earlier base-agent/user interfaces. The core telecom sync implementation is identical, so Verified does not solve that state boundary.

Reproducibility tradeoffs: canonical has an explicit 1.0.1 package version and a bounded Python/LiteLLM range; Verified has a narrower feature surface and a detailed correction catalog, but advertises 0.2.1-dev and generally looser dependency lower bounds. Both need their own pin, task/evaluator settings and environment record. Neither is demonstrated cleaner end-to-end here because neither was installed/run in full. No winner is selected, and no score or expected privacy outcome informed this comparison.

Correction provenance: [FIXES.md:1](https://github.com/amazon-agi/tau2-bench-verified/blob/864350a8971a8f8ee9e7b8472e2edc380a806b0c/FIXES.md#L1). API/evaluator evidence is linked above and captured in SOURCE_EVIDENCE.json; count/diff results are in STATIC_VALIDATION.json.

## Transition-class inventory (18 classes)

1. Task/component construction and initial state setup.
2. Initial-history reconstruction and recipient-specific history selection.
3. User model invocation and role presentation conversion.
4. Assistant model invocation.
5. User→assistant message delivery/history insertion.
6. Assistant→user message delivery/history insertion.
7. Assistant tool proposal and requestor attribution.
8. User tool proposal and requestor attribution.
9. Generic tool dispatch and tool argument validation.
10. Tool-result delivery, including MultiToolMessage batching.
11. Tool exception/error serialization and error counting.
12. Direct tool database mutation.
13. Cross-database telecom synchronization.
14. Model/provider exception and retry behavior.
15. Natural stop, protocol error, max-step/error limits and timeout where supported.
16. Final pending-message stop hooks and trajectory serialization.
17. Evaluator predicted/gold replay and deterministic action/communication/assertion scoring.
18. Optional/required evaluator LLM invocation and reward combination.

These are transition **types**, not task-specific fixtures or an expanded experiment matrix. Planner/worker delegation is absent in the native protocol and is not added. A later parity audit would need identical models, pre-defense context, roles, tools/permissions, scheduler, communication, state access, failure handling, evaluator and stopping semantics across both defenses. Classes 12–13 expose the state blocker; class 17 must preserve the verified execution-record distinction; this audit implements neither arm. TRANSITION_CLASS_PARITY_FEASIBILITY: NOT_FEASIBLE under the full current requirements.

## Final decision, preservation and reproduction

Do not select either implementation as a direct E2 replacement. Preserve the scientific distinction: it could provide multi-principal/dual-control agentic evidence only after an explicitly approved scientific redesign, and the current stronger state-publication mediation requirement still fails. Do not repair τ² or silently narrow privacy to final outputs, remove user capabilities, introduce a hidden evaluator oracle trace or weaken EXACT_IFC.

Recommended human decision: keep τ² rejected for the current unchanged E2 design; retain the 60-task/1080-episode target; choose whether to seek another native collaborative multi-agent runtime or explicitly reconsider the scientific scope in a separate decision. No next development gate is opened.

No candidate source, R3, MARBLE evidence, evaluator or recognizer was modified. No model credential or paid endpoint was used. `FORMAL_MODEL_RUNS_EXECUTED=0`, `DEVELOPMENT_MODEL_RUNS_EXECUTED=0`, `R3_MUTATED=NO`. The current branch is the user-requested existing R0 branch. Push is authorized; merge is not.

Validation commands (from repository root):

```bash
PYTHONPATH=. python3 scripts/audit_tau2_r0_static.py --help
PYTHONPATH=. python3 scripts/audit_tau2_r0_static.py --canonical /private/tmp/benchmark_r0_sources/tau2 --verified /private/tmp/benchmark_r0_sources/tau2_verified --recognizer /private/tmp/flowfence_gate_a_worktree_20260918/src/defenses/mas_flowfence.py --output artifacts/aamas2027_benchmark_replacement_r0_tau/STATIC_VALIDATION.json
git diff --cached --check
git status --short
```

The script uses only the standard library, parses task data, compiles selected unchanged method bodies with minimal stubs, and optionally evaluates the existing recognizer; it does not import candidate packages or execute model clients. This is a deterministic component fixture audit, not a full evaluator replay of a real task or a benchmark reproduction. Temporary source locations are optional inputs and can be recreated at the recorded public commits. Safe artifacts store fixture booleans/counts and public IDs, not protected fact values or full contaminated trajectories.
