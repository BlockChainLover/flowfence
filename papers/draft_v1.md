# FlowFence-Lite: Runtime Containment for Retrieval-Memory Poisoning in Tool-Using LLM Agents

Draft status: v1, submission-shaped but still evidence-bound.

Scope note: this draft reports a narrow, completed empirical slice. It does not claim full official AgentPoison reproduction, broad AgentDojo defense effectiveness, multi-domain generalization, or topology sensitivity. It reports both 25-question overhead proxies from saved traces and a smaller 10-question measured-overhead slice with wall-clock and provider-token usage. It also includes a three-run held-out poisoned-instruction stress test; that result should be described as same-trigger stress-test evidence, not broad held-out attack or topology generalization.

## Abstract

Tool-using LLM agents increasingly rely on retrieved memory and iterative reasoning loops. This creates a containment problem: contaminated memory can enter the model-visible context and steer actions before any final answer is produced. We present FlowFence-Lite, a runtime containment layer that intercepts retrieved memory before it reaches the agent reasoning context. The evaluated variant combines retrieval quarantine with canonical ReAct action writeback.

We evaluate FlowFence-Lite on an adapted AgentPoison StrategyQA full-ReAct comparator under the MiniMax provider profile. The no-defense condition provides a repeated non-vacuous attack anchor: across three runs, exposed poisoned retrieval has mean 0.4667 and attack manifestation has mean 0.2533. FlowFence-Lite with quarantine plus canonical action writeback reduces both exposed poisoned retrieval and attack manifestation to 0.0 across three repeated runs, while raw poisoned retrieval remains non-zero. A same-axis safe-view rewrite-only weak defense also reaches zero exposed retrieval and zero attack manifestation, but has lower clean utility than the selected quarantine-actioncanon variant. An independent static keyword filter also reaches zero exposed retrieval and zero attack manifestation on this known-trigger axis, with clean utility comparable to quarantine-actioncanon. This strengthens baseline coverage while narrowing the claim: FlowFence-Lite should be positioned as structured retrieval-memory containment, not as uniquely necessary for blocking this specific trigger-string attack. To test that limitation, we add a three-run held-out poisoned-instruction stress test. In that setting, a non-oracle static keyword filter trained on old phrases does not intervene and leaves exposed poisoned retrieval at mean 0.4667 with attack manifestation mean 0.2400, while FlowFence-Lite sees raw poisoned retrieval mean 0.5333 but reduces exposed retrieval and attack manifestation to 0.0. This supports a blocklist-brittleness interpretation, with the caveat that it is same-trigger stress-test evidence rather than broad held-out generalization. From saved 25-question traces, quarantine-actioncanon adds overhead proxies of +32.71% recorded model calls per case and +20.71% current-task trace-token proxy relative to no defense. On a separate 10-question measured-overhead slice, quarantine-actioncanon does not increase wall-clock time or provider-reported token usage, and defense inspection itself is microsecond-scale relative to LLM latency; this result is trajectory-confounded and should be read as runtime-feasibility evidence, not as a general faster-or-cheaper claim. We also report AgentDojo MiniMax experiments as auxiliary negative evidence: selected-pair reruns were too stochastic to support a stable before/after defense claim.

## 1. Introduction

LLM agents now retrieve memory, call tools, and execute multi-step policies such as ReAct. In this setting, security and privacy failures are not only final-output events. Unsafe content can enter the intermediate reasoning context, affect tool choices, or be written into later artifacts before a final response is emitted.

Prior benchmarks and attacks establish different parts of this risk landscape. AgentDojo and ASB show that tool-using agents are vulnerable to prompt injection and related attacks [AgentDojo; ASB]. AgentPoison shows that memory and knowledge bases can be poisoned to steer agents [AgentPoison]. Agent Smith and G-Safeguard motivate propagation and topology-aware views of multi-agent risk [AgentSmith; GSafeguard]. AgentDAM and MEXTRA motivate privacy-aware evaluation and memory leakage threats [AgentDAM; MEXTRA]. These works motivate a runtime question: if unsafe retrieved content exists, can the agent system prevent it from becoming actionable model context?

This draft studies that question through FlowFence-Lite. The broader FlowFence-Lite project targets runtime privacy containment across messages, memory, workspaces, tools, and shared artifacts. The completed empirical contribution in this draft is narrower: retrieval-memory containment on an adapted AgentPoison full-ReAct StrategyQA axis under MiniMax.

The contributions are:

- We formulate retrieval-memory poisoning as a runtime containment problem, separating raw poisoned retrieval from model-exposed poisoned retrieval.
- We implement a FlowFence-Lite variant that quarantines unsafe retrieved memory before it enters the ReAct context.
- We evaluate no defense, an independent static keyword filter, a safe-view rewrite-only weak defense, quarantine-only, and quarantine plus canonical ReAct action writeback on the same adapted AgentPoison MiniMax axis with three repeated runs per condition.
- We show that FlowFence-Lite reduces exposed poisoned retrieval and attack manifestation to zero on this axis while raw poisoned retrieval remains non-zero.
- We add a three-run held-out poisoned-instruction stress test showing that an old-phrase non-oracle static keyword filter is brittle while FlowFence-Lite still contains the retrieved poison.
- We report same-axis overhead proxies from existing traces and a strict measured-overhead slice with wall-clock and provider-token usage.
- We document AgentDojo MiniMax instability as auxiliary evidence rather than overclaiming a stable defense baseline.

## 2. Problem Setting

### 2.1 Runtime Model

We consider a text-first, tool-using LLM agent running an iterative reasoning loop. At each step, the agent can query a retrieval environment, receive observations, produce reasoning text, and choose an action. The empirical setting is a full-ReAct StrategyQA loop with retrieved memory.

The broader project model includes additional internal channels such as inter-agent messages, shared memory, shared workspaces, and tool arguments. Those channels motivate the system design, but the completed experiment in this draft focuses on the retrieval-memory boundary.

### 2.2 Threat Model

The attacker can poison retrievable memory or knowledge-base content. If the agent retrieves that content and it enters the model prompt, the content can steer the agent's answer or action choice.

Out of scope are operating-system compromise, evaluator-label compromise, network compromise, model-weight theft, and multimodal channels. The defense is allowed to inspect retrieved content before it reaches the model-visible context and to rewrite, quarantine, or block unsafe content.

### 2.3 Containment Objective

The goal is not to make poisoned content disappear from the underlying environment. Instead, the goal is to prevent retrieved poisoned content from becoming actionable model context.

We therefore distinguish:

- Raw poisoned retrieval: poisoned content is returned by the retrieval layer before defense processing.
- Exposed poisoned retrieval: poisoned content reaches the model prompt after defense processing.
- Attack manifestation: the adversarial behavior targeted by the poisoned memory appears in the agent's output.
- Clean utility: exact-match accuracy in the clean task setting.
- Attacked utility: exact-match accuracy under attack.

This distinction is important because a defense should receive credit only if it contains an existing attack pressure. The strongest pattern is raw poisoned retrieval remaining non-zero while exposed poisoned retrieval and attack manifestation fall.

## 3. FlowFence-Lite

FlowFence-Lite is a runtime layer between an agent and the information channels it consumes or updates. The broader design includes propagation-aware risk scoring, lease-based least privilege, shared-artifact governance, and structured trace logging. The current evaluated implementation focuses on retrieval quarantine and ReAct trajectory hygiene.

### 3.1 Retrieval Quarantine

Retrieval quarantine intercepts memory items after retrieval and before prompt construction. Items judged unsafe are diverted into quarantine and are not exposed as ordinary model-visible evidence. The agent can continue the reasoning loop, but the poisoned text is kept out of the actionable prompt context.

This component is the main safety mechanism evaluated in the current paper slice.

### 3.2 Canonical ReAct Action Writeback

Full-ReAct trajectories can become brittle when actions, observations, or rewritten context drift away from the expected format. Canonical action writeback normalizes the post-defense action representation written back into the trajectory.

This component is not expected to be the primary safety mechanism. Its role is trajectory hygiene: reducing repeated retrieval drift and stabilizing task utility after quarantine interventions.

### 3.3 Current Implementation Boundary

The evaluated implementation does not yet measure lease revocation, topology-aware scoring, workspace governance, broad privacy policy enforcement, or broader runtime behavior across topologies and domains. Those are planned system components but are not part of the completed empirical claim. The current draft reports trace-derived overhead proxies for the full saved matrix and strict measured overhead for a smaller fixed slice.

## 4. Experimental Setup

### 4.1 Main Comparator

The main experiment uses an adapted AgentPoison StrategyQA full-ReAct comparator under MiniMax.

Artifacts and configs:

- Task manifest: `data/tasks/agentpoison_strategyqa_fullreact_v1.json`
- No-defense config: `configs/experiment/agentpoison_fullreact_minimax27_triggerquery.yaml`
- Static keyword filter config: `configs/experiment/agentpoison_fullreact_static_keyword_filter_minimax27_triggerquery.yaml`
- Quarantine-only config: `configs/experiment/agentpoison_fullreact_flowfence_lite_minimax27_triggerquery_quarantine_only.yaml`
- Quarantine-actioncanon config: `configs/experiment/agentpoison_fullreact_flowfence_lite_minimax27_triggerquery_quarantine_actioncanon.yaml`
- Rewrite-only weak comparator config: `configs/experiment/agentpoison_fullreact_flowfence_lite_minimax27_triggerquery_rewrite_only.yaml`
- Main summary: `results/baseline_agentpoison_fullreact_minimax27_small_matrix_summary.json`
- Ablation summary: `results/ablation_agentpoison_fullreact_minimax27_quarantine_only_vs_actioncanon_summary.json`
- Independent weak comparator summary: `results/baseline_agentpoison_fullreact_minimax27_static_keyword_filter_weak_comparator_summary.json`
- Weak comparator summary: `results/baseline_agentpoison_fullreact_minimax27_rewrite_only_weak_comparator_summary.json`
- Overhead proxy summary: `results/overhead_agentpoison_fullreact_minimax27_same_axis_proxy_summary.json`
- Measured overhead summary: `results/overhead_agentpoison_fullreact_minimax27_same_axis_measured_summary.json`
- Held-out instruction stress-test summary: `results/baseline_agentpoison_fullreact_minimax27_heldout_instruction_matrix_summary.json`

The setup keeps the upstream AgentPoison ReAct-StrategyQA loop and DPR retrieval path through `local_wikienv.WikiEnv`. It uses provider profile `minimax27`.

### 4.2 Adaptation From Official AgentPoison

This is an adapted comparator, not full official AgentPoison reproduction. Earlier full-context MiniMax attempts completed but did not provide a trustworthy attack anchor: poisoned retrieval and attack manifestation were both absent. The current comparator uses `trigger_question_only` adversarial search context to avoid trigger dilution and establish a non-vacuous no-defense condition.

The correct interpretation is controlled containment evidence on an adapted AgentPoison axis.

### 4.3 Conditions and Repeats

We compare five conditions:

- No defense.
- Independent static keyword filter.
- Safe-view rewrite-only weak defense.
- FlowFence-Lite, quarantine only.
- FlowFence-Lite, quarantine plus canonical ReAct action writeback.

Each condition has three completed runs on the same fixed axis.

We also run a three-run held-out poisoned-instruction stress test. It keeps the same trigger sequence and retrieval anchor, but paraphrases the poisoned guidance away from the old static-filter phrases. The static filter in this stress test is intentionally non-oracle: it does not match the trigger sequence and only blocks old-axis phrases.

### 4.4 Metrics

We report exposed poisoned retrieval, raw poisoned retrieval, attack manifestation, clean utility, attacked utility, and intervention event rate. We also report same-axis overhead proxies derived from saved traces: recorded model calls per case, current-task ReAct steps, current-task trace-token proxy, and observation character deltas. Separately, we report a strict measured-overhead slice with per-case wall-clock time, provider request time, provider-reported token usage, and defense-inspection timing.

## 5. Results

### 5.1 Main Result and Ablation

All values are means over three runs. Parentheses show min-max ranges.

| condition | exposed poisoned retrieval | attack manifestation | raw poisoned retrieval | clean utility | attacked utility | intervention event rate |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| No defense | 0.4667 (0.36-0.52) | 0.2533 (0.16-0.36) | 0.4667 (0.36-0.52) | 0.3733 (0.28-0.44) | 0.3333 (0.32-0.36) | 0.0000 |
| Static keyword filter | 0.0000 (0.00-0.00) | 0.0000 (0.00-0.00) | 0.4667 (0.28-0.64) | 0.3600 (0.28-0.48) | 0.3600 (0.24-0.52) | 0.4961 (0.3077-0.6164) |
| Safe-view rewrite only | 0.0000 (0.00-0.00) | 0.0000 (0.00-0.00) | 0.4533 (0.28-0.68) | 0.2933 (0.16-0.44) | 0.4933 (0.40-0.64) | 0.4197 (0.3143-0.5521) |
| FlowFence-Lite, quarantine only | 0.0000 (0.00-0.00) | 0.0000 (0.00-0.00) | 0.5333 (0.40-0.60) | 0.3067 (0.24-0.36) | 0.3733 (0.32-0.48) | 0.5805 (0.4894-0.6271) |
| FlowFence-Lite, quarantine + action-canon | 0.0000 (0.00-0.00) | 0.0000 (0.00-0.00) | 0.4400 (0.32-0.56) | 0.3600 (0.28-0.40) | 0.3867 (0.28-0.48) | 0.4770 (0.4267-0.5758) |

The no-defense condition is non-vacuous. Exposed poisoned retrieval and attack manifestation are non-zero in all three no-defense runs. This establishes that the adapted MiniMax axis creates repeated attack pressure.

The independent static keyword filter also reduces exposed poisoned retrieval and attack manifestation to 0.0 in all three runs, with raw poisoned retrieval mean 0.4667. This is an important baseline result because it uses a fixed blocklist rather than FlowFence-Lite risk scoring or lease semantics. It also shows the limitation of the current attack axis: a known-trigger filter can block it.

The safe-view rewrite-only weak defense reduces exposed poisoned retrieval and attack manifestation to 0.0 in all three runs, with raw poisoned retrieval mean 0.4533. FlowFence-Lite with quarantine plus action-canon reduces exposed poisoned retrieval and attack manifestation to 0.0 in all three runs. Raw poisoned retrieval remains non-zero, with mean 0.4400. This is the key containment evidence: the attack input is still retrieved internally, but it does not reach the model-visible context and the attack no longer manifests.

Utility should be described conservatively. Clean utility changes from 0.3733 under no defense to 0.3600 under quarantine-actioncanon, 0.3600 under static filtering, and 0.2933 under rewrite-only. Attacked utility changes from 0.3333 under no defense to 0.3867 under quarantine-actioncanon, 0.3600 under static filtering, and 0.4933 under rewrite-only. Given MiniMax full-ReAct variance, the supported claim is roughly preserved utility for quarantine-actioncanon and static filtering, with noisy utility behavior overall, not significant utility improvement.

### 5.2 Mechanism: What the Ablation Shows

Quarantine-only also reduces exposed poisoned retrieval and attack manifestation to 0.0 across all three runs. This shows that quarantine is sufficient for the safety effect on this axis.

Canonical action writeback improves the process indicators: clean utility is higher than quarantine-only and rewrite-only. The supported interpretation is that canonical action writeback improves ReAct trajectory hygiene and clean utility stability. The static keyword filter and rewrite-only weak comparator both narrow the mechanism claim. Quarantine is not uniquely necessary for zero exposure on this trigger-string axis. The stronger claim is that retrieval-memory interception is the effective boundary. FlowFence-Lite remains the selected method because quarantine gives structured containment semantics for untrusted memory, while static filtering is brittle to unseen triggers and rewrite-only keeps a sanitized observation in the active trajectory.

### 5.3 Held-Out Instruction Stress Test

The same-axis static keyword result raises a direct concern: maybe a simple filter is enough. We therefore added a held-out poisoned-instruction stress test that keeps the same adapted AgentPoison MiniMax retrieval setup but paraphrases the poisoned guidance away from the old known phrases. The static filter condition is non-oracle and does not match the trigger sequence.

| condition | exposed poisoned retrieval | attack manifestation | raw poisoned retrieval | clean utility | attacked utility | intervention event rate |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| No defense, held-out instruction | 0.5333 | 0.1733 | 0.5333 | 0.3200 | 0.0933 | 0.0000 |
| Non-oracle static keyword filter, held-out instruction | 0.4667 | 0.2400 | 0.4667 | 0.1867 | 0.1733 | 0.0000 |
| FlowFence-Lite, held-out instruction | 0.0000 | 0.0000 | 0.5333 | 0.1467 | 0.2533 | 0.4869 |

Observation: the held-out instruction still creates attack pressure under no defense. The non-oracle static filter does not intervene and continues to expose poisoned retrieval. FlowFence-Lite sees raw poisoned retrieval but quarantines it before exposure.

Interpretation: this stress test supports the claim that old-phrase blocklists are brittle to poisoned-guidance paraphrases, while structured retrieval-memory containment can remain effective. The caveat is important: this is three runs per condition, but it keeps the same trigger sequence and adapted `trigger_question_only` retrieval anchor, so it should be reported as same-trigger stress-test evidence, not broad held-out attack generalization.

### 5.4 Overhead Proxies

The 25-question saved matrix does not contain per-call wall-clock timestamps or provider token-usage fields. We therefore report overhead proxies for that matrix and keep them separate from the smaller measured slice.

| condition | model calls / case | delta vs no defense | current-task token proxy / case | token-proxy delta | interventions / case |
| --- | ---: | ---: | ---: | ---: | ---: |
| No defense | 2.8333 | 0.00% | 416.3483 | 0.00% | 0.0000 |
| Safe-view rewrite only | 3.4267 | +20.94% | 536.4700 | +28.85% | 0.6467 |
| FlowFence-Lite, quarantine only | 3.4267 | +20.94% | 495.2800 | +18.96% | 0.7333 |
| FlowFence-Lite, quarantine + action-canon | 3.7600 | +32.71% | 502.5767 | +20.71% | 0.7467 |

All detector-mediated defenses add overhead proxies relative to no defense. The selected quarantine-actioncanon variant has the largest model-call proxy increase but a lower current-task token proxy than rewrite-only. This supports a bounded-cost containment framing, not a faster-or-cheaper framing.

For strict runtime feasibility, we added an instrumented 10-question slice on the same adapted AgentPoison MiniMax axis. MiniMax returned provider token usage for all 40 case executions. On this slice, no defense averaged 28.861467 seconds and 5197.25 provider tokens per case, while quarantine-actioncanon averaged 24.692974 seconds and 4191.50 provider tokens per case. The defense-inspection time was 0.000098 seconds per case for quarantine-actioncanon. Because the method run had shorter sampled ReAct trajectories and no quarantine/intervention events in this slice, the lower wall-clock and token use should not be generalized into a claim that FlowFence-Lite is intrinsically faster. The supported claim is narrower: measured overhead on this fixed slice did not show additional latency or token burden, and the inspection code itself is negligible relative to LLM calls.

### 5.5 AgentDojo MiniMax Auxiliary Result

AgentDojo was tested as a possible same-provider before/after defense axis. It should not be used as the main defense-effect result in the current paper.

Relevant artifacts:

- `results/baseline_agentdojo_minimax27_banking_selected_native_defenses_summary.json`
- `results/baseline_agentdojo_minimax27_banking_stable_pair_search_summary.json`
- `results/baseline_agentdojo_minimax27_axis_switch_attempt_summary.json`

Observation: AgentDojo MiniMax search runs produced non-vacuous hits, but selected-pair reruns repeatedly failed to reproduce stable dual success. This makes the axis useful as a stochastic or blocked-evaluation note, not as a robust before/after defense baseline.

## 6. Discussion

### 6.1 Why This Evidence Is Strong Enough for a Narrow Claim

The main result has three properties that make it credible despite its narrow scope.

First, no defense has repeated non-zero exposed poisoned retrieval and attack manifestation. Second, FlowFence-Lite eliminates the exposed/manifested attack outcomes across repeated runs. Third, raw poisoned retrieval remains non-zero under FlowFence-Lite, so the observed safety effect is containment rather than absence of attack input.

### 6.2 Why This Evidence Is Not Enough for a Broad Claim

The current experiment includes one independent weak defense family and a repeated held-out-instruction stress test, but it does not include multiple topologies, multiple domains, or broad held-out attack generalization. It also uses an adapted AgentPoison comparator. Therefore, the paper should not claim that FlowFence-Lite broadly outperforms prompt filters, static ACLs, topology guards, or data minimizers.

### 6.3 What the Weak Comparators Add

The weak comparators resolve one important full-paper weakness: the main table no longer compares only no defense against FlowFence-Lite variants. The static keyword filter adds an independent blocklist-style defense family, while rewrite-only adds a non-quarantine same-axis defense using the same detector and the same MiniMax AgentPoison setup.

The result is informative but also constraining. Static filtering and rewrite-only both block exposed poisoned retrieval on the known-trigger axis, so the paper should not claim that quarantine is uniquely necessary or that FlowFence-Lite outperforms all independent weak defenses. The held-out stress test adds the missing nuance: when the static filter is not allowed to oracle-match the trigger and the poisoned guidance is paraphrased away from old phrases, it fails to intervene. The stronger and more defensible claim is that retrieval-memory interception is the effective boundary, and that quarantine-actioncanon is the selected method because it has structured containment semantics, similar clean utility to static filtering on the known-trigger axis, better clean utility than rewrite-only, and a clearer path beyond old-phrase blocklists.

### 6.4 What the Overhead Proxy Adds

The overhead artifacts resolve a smaller paper weakness: runtime cost is no longer completely unmeasured on the main axis. The 25-question proxy artifact shows that containment is not free: quarantine-actioncanon adds about one recorded model call per case and about 20.71% current-task trace-token proxy compared with no defense.

The separate 10-question measured slice supports a strict but narrow runtime-feasibility statement: measured wall-clock time and provider token usage did not increase for quarantine-actioncanon versus no defense on that slice, and defense-inspection time was negligible in absolute terms. This should not be framed as a general faster-or-cheaper claim because the measured slice is smaller than the main efficacy matrix and trajectory-confounded.

## 7. Related Work

AgentDojo provides a dynamic benchmark for prompt injection attacks and defenses in tool-using agents [AgentDojo]. ASB broadens the benchmark framing across agent attacks and defenses [ASB]. These works motivate dynamic agent evaluation rather than static prompt-only tests.

AgentPoison is the closest empirical attack baseline for this draft because it targets poisoned memory and knowledge bases [AgentPoison]. Our experiment uses an adapted AgentPoison StrategyQA full-ReAct axis, but we explicitly avoid claiming official reproduction.

Agent Smith motivates the propagation view of multi-agent compromise [AgentSmith]. G-Safeguard shows that topology can affect multi-agent security behavior [GSafeguard]. These works support the broader FlowFence-Lite framing, although the current draft does not yet evaluate topology.

AgentDAM motivates privacy-utility evaluation for agentic systems [AgentDAM]. MEXTRA motivates memory extraction as a privacy threat [MEXTRA]. These works inform the broader project goal of internal-channel privacy evaluation, while the current experiment remains focused on retrieval-memory poisoning containment.

A-MEM motivates treating memory as a first-class system component for agent utility [AMEM]. In this project it is a future memory-backend comparator rather than a completed baseline.

## 8. Limitations

The result is narrow. It covers one adapted AgentPoison full-ReAct axis, one provider profile, and three repeated runs per condition.

The AgentPoison comparator is adapted with `trigger_question_only` adversarial search context. This should be reported as a controlled adaptation, not official reproduction.

AgentDojo under MiniMax did not provide a stable selected-pair before/after anchor. It should remain an appendix or limitation.

The current evidence does not measure topology sensitivity, cascade size, privilege reach, false block rate, or broad held-out attack generalization. The held-out instruction stress test is three runs per condition, but keeps the same trigger sequence and adapted retrieval anchor. Measured overhead exists only for a 10-question same-axis slice.

Utility is noisy. The appropriate utility claim is roughly preserved utility for quarantine-actioncanon, not improvement. Rewrite-only has high attacked utility in the three runs but lower clean utility, so it should not be framed as a utility-dominant baseline.

## 9. Conclusion

FlowFence-Lite provides a narrow but concrete retrieval-memory containment result. On an adapted AgentPoison full-ReAct comparator under MiniMax, no defense repeatedly exposes poisoned retrieval and produces non-zero attack manifestation. Safe-view rewrite-only and FlowFence-Lite quarantine-actioncanon both reduce exposed poisoned retrieval and attack manifestation to zero across three repeated runs while raw poisoned retrieval remains non-zero.

The ablation, weak comparators, held-out stress test, and overhead artifacts refine the mechanism story. The effective boundary is retrieval-memory interception before poisoned memory reaches model-visible context. Quarantine-actioncanon remains the selected method because it provides clearer untrusted-memory containment, similar clean utility to static filtering on the known-trigger axis, better clean utility than rewrite-only in the main matrix, and repeated same-trigger stress-test evidence against an old-phrase blocklist. The result is promising enough for a scoped full-paper direction, but broader systems claims still require topology experiments, broader held-out attacks, and broader independent defense coverage.

## Appendix A. Evidence-Bound Claim List

Supported:

- On an adapted AgentPoison full-ReAct comparator under MiniMax, FlowFence-Lite reduces exposed poisoned retrieval and attack manifestation to zero across three repeated runs.
- An independent static keyword filter also reduces exposed poisoned retrieval and attack manifestation to zero across three repeated runs on this known-trigger axis; this supports broader baseline coverage but limits uniqueness claims.
- In a three-run held-out poisoned-instruction stress test, an old-phrase non-oracle static keyword filter fails to intervene while FlowFence-Lite reduces exposed poisoned retrieval and attack manifestation to zero.
- A same-axis safe-view rewrite-only weak defense also reduces exposed poisoned retrieval and attack manifestation to zero across three repeated runs.
- Quarantine is sufficient for the safety effect on this axis, but not uniquely necessary when the shared detector can rewrite unsafe retrieved content.
- Canonical ReAct action writeback improves trajectory hygiene and clean utility stability relative to quarantine-only.
- Same-axis saved traces show bounded overhead proxies for quarantine-actioncanon: +32.71% recorded model calls per case and +20.71% current-task trace-token proxy versus no defense.
- A 10-question measured-overhead slice shows no wall-clock or provider-token increase for quarantine-actioncanon versus no defense, with defense-inspection time around 0.000098 seconds per case; this is trajectory-confounded and should be used only as runtime-feasibility evidence.
- AgentDojo MiniMax should be reported as stochastic/blocked auxiliary evidence, not as a stable main baseline.

Not supported:

- FlowFence-Lite reproduces and beats official AgentPoison.
- FlowFence-Lite broadly outperforms AgentDojo native defenses.
- FlowFence-Lite significantly improves utility.
- FlowFence-Lite generally lowers latency or always uses fewer tokens.
- FlowFence-Lite outperforms multiple independent defense families.
- FlowFence-Lite is uniquely necessary to block this known-trigger AgentPoison variant.
- FlowFence-Lite generalizes across topologies or providers.
- FlowFence-Lite has broad held-out attack or topology generalization evidence.

## Appendix B. References To Resolve Into BibTeX

- [AgentDojo] AgentDojo: A Dynamic Environment to Evaluate Prompt Injection Attacks and Defenses for LLM Agents. NeurIPS 2024 Datasets and Benchmarks. https://openreview.net/forum?id=m1YYAQjO3w
- [ASB] Agent Security Bench: Formalizing and Benchmarking Attacks and Defenses in LLM-based Agents. ICLR 2025. https://openreview.net/forum?id=V4y0CpX4hK
- [AgentPoison] AgentPoison: Red-teaming LLM Agents via Poisoning Memory or Knowledge Bases. NeurIPS 2024. https://openreview.net/forum?id=Y841BRW9rY
- [AgentSmith] Agent Smith: A Single Image Can Jailbreak One Million Multimodal LLM Agents Exponentially Fast. ICML 2024. https://proceedings.mlr.press/v235/gu24e.html
- [GSafeguard] G-Safeguard: A Topology-Guided Security Lens and Treatment on LLM-based Multi-agent Systems. ACL 2025. https://aclanthology.org/2025.acl-long.359/
- [AgentDAM] AgentDAM: Privacy Leakage Evaluation for Autonomous Web Agents. NeurIPS 2025 Datasets and Benchmarks. https://openreview.net/forum?id=qaxf7q41aK
- [MEXTRA] Unveiling Privacy Risks in LLM Agent Memory. ACL 2025. https://aclanthology.org/2025.acl-long.1227/
- [AMEM] A-MEM: Agentic Memory for LLM Agents. NeurIPS 2025. https://openreview.net/forum?id=FiM0M8gcct
