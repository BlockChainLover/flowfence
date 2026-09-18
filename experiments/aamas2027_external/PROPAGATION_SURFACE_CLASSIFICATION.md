# Propagation surface classification — Gate A-E

Scope: pinned Research/Database/Coding, original STAR scheduler and actual registered tools. Each surface has exactly one of the five requested classes. JSON is authoritative for producer, consumer, visibility, later-model reachability, task semantics, observation, hook and bypass evidence. Reachability is a separate field: unregistered source functions are inventoried without pretending agents have those capabilities.

Corrections to Gate A-D: Coding registers only create_solution and give_advice_and_revise. Tester/debugger/analyst registration is commented out; analyst has no model call. DB registers only query_db. Local Python logs/console/advice_log are trusted diagnostic instrumentation, not privacy releases under the five explicitly checked conditions. This does not exempt advices.json (shared state) or PostgreSQL query statistics (readable via the registered SQL tool).

All C-class entries satisfy: no benchmark-agent/model consumer, no external recipient, no shared benchmark-artifact role, no final-output inclusion, trusted local instrumentation only. Source search and runtime fixtures support these conditions. Raw local diagnostics never enter committed safe evidence. If a later runner exports or re-ingests these logs, classification must change; this is a scope condition, not a silent deletion of a propagation surface.

Evaluator gold/reference fields are D. Runtime text entering judge prompts is separately A, even when both appear in one flattened prompt. No detector sees gold; no evaluator prompt or metric changes. A trusted-private evaluator is not a blanket exemption for unlabelled runtime data or arbitrary service transmission.

| Surface | Class | Reachable | Mediation required | Boundary / evidence |
|---|---|---|---|---|
| task_and_role_context | MODEL_VISIBLE_PROPAGATION | True | REQUIRED | act argument wrapper only; role/system/state assembly not completely bound to an authorized recipient |
| owner_private_memory | MODEL_VISIBLE_PROPAGATION | True | REQUIRED | update/get_memory_str wrappers; direct storage insertion and str/retrieve_all remain reachable; authorization depends on actual context recipient |
| agent_shared_memory | EXTERNAL_OR_SHARED_SIDE_EFFECT | True | REQUIRED | none on per-agent SharedMemory; direct update and backing dictionary reads expose value without release event |
| engine_memory | EXTERNAL_OR_SHARED_SIDE_EFFECT | True | REQUIRED | update wrapper; direct append/retrieve_all bypass publication |
| planner_progress | EXTERNAL_OR_SHARED_SIDE_EFFECT | True | REQUIRED | update_progress wrapper; direct attribute assignment appears in create_prompt without release |
| environment_state | EXTERNAL_OR_SHARED_SIDE_EFFECT | True | REQUIRED | apply_action last-result overwrite only; direct backing assignment observed via get_state without release |
| agent_task_history | MODEL_VISIBLE_PROPAGATION | True | REQUIRED | act argument release; backing list is not a publication API; common context identity is required |
| messages_and_mailbox | MODEL_VISIBLE_PROPAGATION | True | REQUIRED | both send_message and receive_message; normal dispatch intercepted; direct mutable mailbox is outside a closed state boundary |
| session_model_context | MODEL_VISIBLE_PROPAGATION | True | REQUIRED | no trusted recipient at common model API; actual worker context inherits outer owner scope; raw passes generic gateway in both arms |
| session_summary | MODEL_VISIBLE_PROPAGATION | True | REQUIRED | result later reaches memory.update; summary model is invoked before that return; current generic context API has no receiving-principal argument |
| agent_results | MODEL_VISIBLE_PROPAGATION | True | REQUIRED | act return wrapper; covered after return; does not cover nested consumers before return |
| planner_assignment_context | MODEL_VISIBLE_PROPAGATION | True | REQUIRED | assignment output wrapper; input current_progress can bypass publication; explicit planner recipient works only when supplied externally |
| planner_decision_summary | MODEL_VISIBLE_PROPAGATION | True | REQUIRED | partial summary wrapper; common provider gateway exists but lacks trusted role binding |
| tool_arguments | EXTERNAL_OR_SHARED_SIDE_EFFECT | True | REQUIRED | generic whole-argument release; protected fixture mediated before HTTP/SQL dispatch; clean tool schemas unchanged |
| tool_results_errors | MODEL_VISIBLE_PROPAGATION | True | REQUIRED | generic tool-result release; post-return hook cannot stop earlier nested calls or file publication |
| research_outbound | EXTERNAL_OR_SHARED_SIDE_EFFECT | True | REQUIRED | generic apply_action input dominates modeled private-runtime inputs; registered tools do not read agent/private stores or call a reachable generative helper; fresh protected query mediated before dispatch |
| research_returned_papers | MODEL_VISIBLE_PROPAGATION | True | REQUIRED | tool-result release; intermediate HTTP responses remain inside tool until returned; no shared file publication in these registered tools |
| research_domain_helper | MODEL_VISIBLE_PROPAGATION | False | NOT_REQUIRED_IN_PINNED_E2_ROUTE | common API if invoked; helper exists but no call from registered E2 research actions |
| db_runtime_sql | EXTERNAL_OR_SHARED_SIDE_EFFECT | True | REQUIRED | generic tool-argument release before query_db; only registered runtime DB action; protected SQL mediated before cursor dispatch; no per-SQL operation patch |
| db_initialization_sql | EXTERNAL_OR_SHARED_SIDE_EFFECT | True | NOT_REQUIRED_IN_PINNED_E2_ROUTE | trusted initialization before sidecar injection; no generated/protected runtime value is available during initialization; not a suppressed runtime tool |
| db_docker_process | EXTERNAL_OR_SHARED_SIDE_EFFECT | True | NOT_REQUIRED_IN_PINNED_E2_ROUTE | trusted lifecycle (external double in audit); no generated command parameter at registered runtime interfaces; originals preserved |
| db_alerts_http | MODEL_VISIBLE_PROPAGATION | True | NOT_REQUIRED_IN_PINNED_E2_ROUTE | initialization service doubles; alert/log/metric tools are commented out in register_actions; no runtime generated args reach them |
| coding_generate_context | MODEL_VISIBLE_PROPAGATION | True | REQUIRED | common completion API only; outer caller wrapper insufficient; recipient needs a trusted sub-model/tool binding; no principal field in upstream API |
| coding_reviewer_context | MODEL_VISIBLE_PROPAGATION | True | REQUIRED | none before original nested calls; actual raw shared solution reaches reviewer before outer return under both arms |
| coding_solution_publication | EXTERNAL_OR_SHARED_SIDE_EFFECT | True | REQUIRED | generic workspace namespace open publication probe; one probe intercepts both active writers; no module/handler dispatch list; does not resolve model identity/state |
| coding_advice_publication | EXTERNAL_OR_SHARED_SIDE_EFFECT | True | REQUIRED | same generic workspace publication probe; real chunked json.dump mediated at publication; file distinct from diagnostic advice_log |
| coding_debugger | EXTERNAL_OR_SHARED_SIDE_EFFECT | False | NOT_REQUIRED_IN_PINNED_E2_ROUTE | not installed; unregistered in pinned CodingEnvironment; do not remove tools or add them for this audit |
| coding_tester_execution | EXTERNAL_OR_SHARED_SIDE_EFFECT | False | NOT_REQUIRED_IN_PINNED_E2_ROUTE | not installed; tester import/registration commented out; generated solution is read by an LLM evaluator, not executed by current tool registry |
| coding_analyst | EXTERNAL_OR_SHARED_SIDE_EFFECT | False | NOT_REQUIRED_IN_PINNED_E2_ROUTE | not installed; analyst has no model invocation; module functions not registered in pinned E2 |
| benchmark_logger | TRUSTED_LOCAL_DIAGNOSTIC | True | NOT_REQUIRED_IN_PINNED_E2_ROUTE | local private capture; no benchmark read path, service export or final inclusion; any future log export invalidates this classification |
| benchmark_console | TRUSTED_LOCAL_DIAGNOSTIC | True | NOT_REQUIRED_IN_PINNED_E2_ROUTE | local private capture; not subprocess tool stdout: these Python diagnostic prints are not returned to agents or published in evidence |
| reviewer_diagnostic | TRUSTED_LOCAL_DIAGNOSTIC | True | NOT_REQUIRED_IN_PINNED_E2_ROUTE | local private instrumentation; source search finds write only, no reads; fixture intentionally retains raw locally while shared files remove it |
| judge_gold_reference | BENCHMARK_EVALUATOR_PRIVATE | True | NOT_REQUIRED_IN_PINNED_E2_ROUTE | unchanged original evaluator; no label input to defense; do not redact/rewrite gold or classify all mixed evaluator messages as diagnostics; runtime segment separately below |
| judge_runtime_artifact | MODEL_VISIBLE_PROPAGATION | True | REQUIRED | upstream runtime release, then original evaluator context; common flattened completion API does not label runtime vs evaluator-private spans; cannot skip all judge input as private |
| private_evaluator_metrics | BENCHMARK_EVALUATOR_PRIVATE | True | NOT_REQUIRED_IN_PINNED_E2_ROUTE | private audit artifacts; only booleans/counters released in Gate A-E; no fabricated utility scores used for eligibility |
| final_answer_publication | EXTERNAL_OR_SHARED_SIDE_EFFECT | True | REQUIRED | generic final artifact release; actual original serializer executed in both arms; diagnostic data are not implicitly final answers |

Machine evidence: artifacts/aamas2027_gate_ae/PROPAGATION_SURFACE_CLASSIFICATION.json and AUDIT.json. Privacy observations concern modeled recipients/publications, not arbitrary OS syscalls or the mere existence of a diagnostic string.
