# τ²-Bench multi-agent scientific-scope audit

Date: 2026-09-18. Phase: baseline scouting, authorized R0-τ audit only.
Canonical: `b7ea9074c1cba482b30687fecdb5c8425fd6f619`. Verified: `864350a8971a8f8ee9e7b8472e2edc380a806b0c`.
Route: native text/half-duplex `LLMAgent` + `UserSimulator`, airline/retail/telecom, base split. Ground-truth/solo agents, voice/full-duplex, knowledge/shell domains and custom assistant teams are not substituted for this standard route.

MULTI_AGENT_SCOPE_FIT: PARTIAL
TAU2_SCIENTIFIC_CLAIM_SCOPE: PUBLIC_MULTI_PRINCIPAL_AGENTIC_BENCHMARK_EXTERNAL_VALIDITY
TAU2_E2_ROLE: AGENTIC_EXTERNAL_VALIDITY_ONLY

These are scientific-role classifications, independent of the architecture failure documented in the architecture report. They do not authorize even a multi-principal experiment under the current constraints.

| Required question | Standard protocol finding |
|---|---|
| Evaluated autonomous assistant agents per task | One. The orchestrator holds one evaluated assistant object. |
| Simulated user | Yes, a separate UserSimulator object and state. |
| Model-driven user | Yes, it invokes the model generation utility independently. It is not a second evaluated assistant. |
| Can user use tools / mutate state? | Yes in telecom, using the provided user tool kit and device/surroundings DB; airline and retail constructors provide no user tool kit. |
| Multiple collaborating assistant agents | No in the standard inspected execution. |
| Planner/worker delegation | None in the standard route. |
| Agent-to-agent communication | Assistant↔user messages exist between autonomous modeled actors. No assistant↔assistant delegation/message graph exists. |
| Shared state among multiple assistants | No; one assistant. Telecom couples service-provider state with user device/environment state. |
| Standard multi-agent orchestration | A two-actor assistant/user turn scheduler exists. A collaborative assistant team is not prescribed by the benchmark protocol. |
| Adding multiple assistants | A custom agent implementation/submission would add that architecture. It may fit the benchmark's agent extension interface, but the teamwork would be an experimental system addition, not native benchmark workflow evidence. |

**Multi-model** describes model invocations or backend choices; assistant and user can even use the same model. **Multi-principal** describes distinct modeled recipients and private histories. **Dual-control** additionally lets both sides act on the environment, especially telecom. **Collaborative multi-agent workflow**, as originally intended for E2, entails multiple assistant/worker principals coordinating the benchmark task. These are different scientific properties.

The authors explicitly model telecom as a Dec-POMDP with agent/user coordination and tool use. That supports dual-control terminology, not a claim that the standard implementation contains a planner-worker team. Source: [original τ² paper](https://arxiv.org/abs/2506.07982).

Runtime evidence: canonical [src/tau2/orchestrator/orchestrator.py:119](https://github.com/sierra-research/tau2-bench/blob/b7ea9074c1cba482b30687fecdb5c8425fd6f619/src/tau2/orchestrator/orchestrator.py#L119), [src/tau2/orchestrator/orchestrator.py:837](https://github.com/sierra-research/tau2-bench/blob/b7ea9074c1cba482b30687fecdb5c8425fd6f619/src/tau2/orchestrator/orchestrator.py#L837), [src/tau2/agent/llm_agent.py:128](https://github.com/sierra-research/tau2-bench/blob/b7ea9074c1cba482b30687fecdb5c8425fd6f619/src/tau2/agent/llm_agent.py#L128), [src/tau2/user/user_simulator.py:235](https://github.com/sierra-research/tau2-bench/blob/b7ea9074c1cba482b30687fecdb5c8425fd6f619/src/tau2/user/user_simulator.py#L235), [src/tau2/runner/build.py:128](https://github.com/sierra-research/tau2-bench/blob/b7ea9074c1cba482b30687fecdb5c8425fd6f619/src/tau2/runner/build.py#L128); verified [src/tau2/orchestrator/orchestrator.py:115](https://github.com/amazon-agi/tau2-bench-verified/blob/864350a8971a8f8ee9e7b8472e2edc380a806b0c/src/tau2/orchestrator/orchestrator.py#L115), [src/tau2/orchestrator/orchestrator.py:464](https://github.com/amazon-agi/tau2-bench-verified/blob/864350a8971a8f8ee9e7b8472e2edc380a806b0c/src/tau2/orchestrator/orchestrator.py#L464), [src/tau2/run.py:502](https://github.com/amazon-agi/tau2-bench-verified/blob/864350a8971a8f8ee9e7b8472e2edc380a806b0c/src/tau2/run.py#L502).

Category 2 is the strongest accurate candidate claim: **public multi-principal agentic benchmark external validity**. Category 3 is also accurate but narrower. Category 1, **public multi-agent benchmark external validity in the original collaborative-workflow sense**, is not defensible from these standard runs alone. τ² cannot be a silent one-for-one replacement for MARBLE's approved E2 role. Any reframing requires a human scientific-design decision, without silently reducing the 60-task/1080-episode target.

The three domains differ in flight reservations/refunds, product orders/exchanges, and telecom diagnosis/device-service coordination. They are three customer-service domains, not automatically three distinct collaborative multi-agent workflow families. Verified retains the same one-assistant/one-user protocol and does not solve this scope mismatch.
