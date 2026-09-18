# τ² principal binding audit

Date: 2026-09-18. Phase: baseline scouting, authorized R0-τ audit only.
Canonical: `b7ea9074c1cba482b30687fecdb5c8425fd6f619`. Verified: `864350a8971a8f8ee9e7b8472e2edc380a806b0c`.
Route: native text/half-duplex `LLMAgent` + `UserSimulator`, airline/retail/telecom, base split. Ground-truth/solo agents, voice/full-duplex, knowledge/shell domains and custom assistant teams are not substituted for this standard route.

PRINCIPAL_BINDING: VERIFIED

This means **static availability at existing structured component boundaries**, not a claim that the unmodified low-level model API already enforces principal labels. No recipient IDs were added to source, no adapter was implemented, and no runtime parity was executed.

| Call / component | Structured identity available | Explicit or inferred | Shared model dispatcher? | Semantics-preserving adapter binding possible? |
|---|---|---|---|---|
| LLMAgent._generate_next_message / verified LLMAgent.generate_next_message → generate | YES at the orchestrator's assistant object/state slot and typed Role.AGENT routing | Explicit object association assigned by runtime construction; not prompt interpretation | Yes, common generate | YES for this fixed standard route: bind the existing assistant component at construction/call boundary; retain its entire invocation scope. |
| UserSimulator._generate_next_message → generate | YES at user object/state slot and Role.USER routing | Explicit runtime component, even though provider messages are role-flipped | Yes | YES: bind the existing user component, never infer it from provider chat roles. |
| Environment.get_response / toolkits | YES: ToolCall.requestor and orchestrator from_role distinguish assistant and user; ENV is a scheduler role | Structured runtime field; user simulator explicitly rewrites requestor to user, assistant generation constructs calls with assistant default | No model invocation in the inspected core domain tools | YES for actor attribution at generic tool dispatch; this does not prove state-write mediation. |
| NLAssertionsEvaluator.evaluate_nl_assertions → generate | YES as a separate evaluator component invocation outside the episode loop; NO modeled user/assistant recipient | Explicit evaluator invocation provenance, not a fabricated participant | Yes | YES for exclusion from experimental privacy policy by binding the dedicated evaluator entry point. Never use call_name as authority. |
| EnvironmentEvaluator, ActionEvaluator, CommunicateEvaluator | Evaluator invocation scope is separate | Explicit class/function and Task.evaluation_criteria data flow | No model invocation | YES, leave private evaluation outside runtime policy. |
| Low-level generate(model,messages,tools,...) alone | NO modeled receiving-principal parameter | Purpose labels are not authority | Serves assistant, user and judge | NO if intercepted alone; upstream structured binding is necessary and already possible without redesign. |

The canonical call sites are:

- [src/tau2/agent/llm_agent.py:128](https://github.com/sierra-research/tau2-bench/blob/b7ea9074c1cba482b30687fecdb5c8425fd6f619/src/tau2/agent/llm_agent.py#L128)
- [src/tau2/user/user_simulator.py:235](https://github.com/sierra-research/tau2-bench/blob/b7ea9074c1cba482b30687fecdb5c8425fd6f619/src/tau2/user/user_simulator.py#L235)
- [src/tau2/evaluator/evaluator_nl_assertions.py:121](https://github.com/sierra-research/tau2-bench/blob/b7ea9074c1cba482b30687fecdb5c8425fd6f619/src/tau2/evaluator/evaluator_nl_assertions.py#L121)
- [src/tau2/utils/llm_utils.py:355](https://github.com/sierra-research/tau2-bench/blob/b7ea9074c1cba482b30687fecdb5c8425fd6f619/src/tau2/utils/llm_utils.py#L355)
- [src/tau2/orchestrator/orchestrator.py:837](https://github.com/sierra-research/tau2-bench/blob/b7ea9074c1cba482b30687fecdb5c8425fd6f619/src/tau2/orchestrator/orchestrator.py#L837)
- [src/tau2/runner/build.py:128](https://github.com/sierra-research/tau2-bench/blob/b7ea9074c1cba482b30687fecdb5c8425fd6f619/src/tau2/runner/build.py#L128)

The verified call sites are:

- [src/tau2/agent/llm_agent.py:108](https://github.com/amazon-agi/tau2-bench-verified/blob/864350a8971a8f8ee9e7b8472e2edc380a806b0c/src/tau2/agent/llm_agent.py#L108)
- [src/tau2/user/user_simulator.py:158](https://github.com/amazon-agi/tau2-bench-verified/blob/864350a8971a8f8ee9e7b8472e2edc380a806b0c/src/tau2/user/user_simulator.py#L158)
- [src/tau2/evaluator/evaluator_nl_assertions.py:115](https://github.com/amazon-agi/tau2-bench-verified/blob/864350a8971a8f8ee9e7b8472e2edc380a806b0c/src/tau2/evaluator/evaluator_nl_assertions.py#L115)
- [src/tau2/utils/llm_utils.py:180](https://github.com/amazon-agi/tau2-bench-verified/blob/864350a8971a8f8ee9e7b8472e2edc380a806b0c/src/tau2/utils/llm_utils.py#L180)
- [src/tau2/orchestrator/orchestrator.py:464](https://github.com/amazon-agi/tau2-bench-verified/blob/864350a8971a8f8ee9e7b8472e2edc380a806b0c/src/tau2/orchestrator/orchestrator.py#L464)
- [src/tau2/run.py:502](https://github.com/amazon-agi/tau2-bench-verified/blob/864350a8971a8f8ee9e7b8472e2edc380a806b0c/src/tau2/run.py#L502)

A wrapper can associate the already-constructed assistant/user objects with their explicit orchestrator slots and carry that association through a call. This uses neither variable-name heuristics nor role-description parsing: the branch's typed Role and actual component reference select the receiving principal. It does not add extra modeled actors. Standard initialization constructs separate system/history state and supplies the default opening assistant message; the first generated non-solo message is from the user. Reused initial histories are selected by existing typed message/requestor predicates. Solo/GT first-assistant generation exists but is an explicitly different protocol, not silently included.

User state `flip_roles()` maps provider roles for user simulation. It does not change the modeled owner of that invocation. Actor identity for user tool calls is explicitly set during conversion of generated calls. Generic model retries remain under the same component invocation; both pins configure three default retries in their generation utility. Standard base stop hooks do not invoke models. No nested model call was found in airline/retail/telecom tool source. Optional NL judging uses its own evaluator call site, and all gold/assertion material there remains evaluator-private.

This resolves the earlier R0 principal-binding uncertainty at the static architectural level. It is not a proof of a future implementation's propagation of context-local identity through arbitrary custom agents, callbacks, voice workers or knowledge retrieval. Those are outside the fixed native route.
