> Gate A-C supersedes this earlier checklist: see MEDIATION_COVERAGE_AUDIT.md.

# Mediation coverage at effective benchmark variant

No production mediation adapter was installed in Gate A-R. Consequently no runtime row is called MEDIATED merely because a hook is feasible. All paths below are source-observable; coverage must be demonstrated before READY. This matrix concerns modeled application recipients, not unrestricted OS or provider internals.

| Transition | Code site | Research | Database | Coding | Required pre-release interception |
|---|---|---|---|---|---|
| agent → agent | BaseAgent.send_message/receive_message | OBSERVABLE_BUT_NOT_MEDIATED | OBSERVABLE_BUT_NOT_MEDIATED | OBSERVABLE_BUT_NOT_MEDIATED | Before recipient.msg_box mutation, including communication-session helpers |
| agent → shared state | Engine result/summary and planner.update_progress | OBSERVABLE_BUT_NOT_MEDIATED | OBSERVABLE_BUT_NOT_MEDIATED | OBSERVABLE_BUT_NOT_MEDIATED | Before aggregation reaches planner or summary readers |
| shared state → agent | BaseMemory.get_memory_str, planner/agent task construction | OBSERVABLE_BUT_NOT_MEDIATED | OBSERVABLE_BUT_NOT_MEDIATED | OBSERVABLE_BUT_NOT_MEDIATED | Recipient-specific prompt context after authorized read |
| agent → tool | BaseAgent.act → BaseEnvironment.apply_action | OBSERVABLE_BUT_NOT_MEDIATED | OBSERVABLE_BUT_NOT_MEDIATED | OBSERVABLE_BUT_NOT_MEDIATED | Typed arguments before handler or side effect |
| tool → agent | act result_from_function, memory.update | OBSERVABLE_BUT_NOT_MEDIATED | OBSERVABLE_BUT_NOT_MEDIATED | OBSERVABLE_BUT_NOT_MEDIATED | Before memory write and act return, including error strings |
| intermediate document | tool/output artifacts | NOT_APPLICABLE to native shared solution file; retrieved papers still tools | OBSERVABLE_BUT_NOT_MEDIATED (DB logs/SQL state) | OBSERVABLE_BUT_NOT_MEDIATED (solution.py, advice logs) | Coding handler writes before returning; outer return wrapper is too late |
| final output | Engine._write_to_jsonl, summary output | OBSERVABLE_BUT_NOT_MEDIATED | OBSERVABLE_BUT_NOT_MEDIATED | OBSERVABLE_BUT_NOT_MEDIATED | Before public output; private audit separately authorized |
| external action | research HTTP / DB SQL / nested coding model | OBSERVABLE_BUT_NOT_MEDIATED | OBSERVABLE_BUT_NOT_MEDIATED | OBSERVABLE_BUT_NOT_MEDIATED | Before URL/query, SQL execution, or nested model request |
| delegation | planner.assign_tasks, agent.plan_task, communication target | OBSERVABLE_BUT_NOT_MEDIATED | OBSERVABLE_BUT_NOT_MEDIATED | OBSERVABLE_BUT_NOT_MEDIATED | Before task delivery, retain generated target/ordering |
| debug logging | logger.info full prompts/results | OBSERVABLE_BUT_NOT_MEDIATED | OBSERVABLE_BUT_NOT_MEDIATED | OBSERVABLE_BUT_NOT_MEDIATED | Private sink or safe annotations before shared log release |

BaseAgent allocates its own BaseMemory and a new SharedMemory even if passed shared_memory; Engine separately owns planner memory. Do not claim a common agent blackboard from the class name. Native per-agent memory is private-by-object, not an authorization-enforced store. Coding agents share actual workspace files.

Research HTTP queries may disclose before results return. DB query handler executes model-provided SQL and logs; infrastructure init includes sudo docker compose down -v and public service bindings, so construction was NOT executed. Coding create_solution/reviewer invokes nested model_prompting and writes files before BaseAgent sees the result. These paths need internal hooks; filtering only BaseAgent.act return leaves bypasses. No NOT_OBSERVABLE path is proven unavoidable, but zero end-to-end mediated surfaces are currently verified.

MEDIATION_COVERAGE: NOT_VERIFIED
