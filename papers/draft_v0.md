# FlowFence-Lite: Retrieval-Memory Containment for Tool-Using LLM Agents

Draft status: v0, evidence-bound draft.

This draft intentionally scopes the empirical claim to the current saved artifacts. It should not be read as claiming full official AgentPoison reproduction, broad AgentDojo defense effectiveness, or full multi-agent topology coverage.

## Abstract

Tool-using LLM agents increasingly rely on retrieved memory, shared context, and iterative reasoning loops. These capabilities create a security and privacy problem that is not fully captured by final-output evaluation: contaminated or unauthorized content may be retrieved, propagated through intermediate reasoning, written into shared artifacts, or used to steer later actions before it appears in a final answer. We study this problem through FlowFence-Lite, a runtime containment layer that intercepts retrieved memory before it enters the agent reasoning context. The current implementation focuses on quarantine-based retrieval containment and canonical ReAct action writeback.

We evaluate FlowFence-Lite on an adapted AgentPoison StrategyQA full-ReAct comparator under the MiniMax provider profile. The no-defense condition establishes a non-vacuous attack: across three runs, exposed poisoned retrieval has mean 0.4667 and attack manifestation has mean 0.2533. FlowFence-Lite with quarantine plus canonical action writeback reduces both exposed poisoned retrieval and attack manifestation to 0.0 across three repeated runs, while raw poisoned retrieval remains non-zero. This indicates containment at the retrieval-memory boundary rather than disappearance of the attack input. An ablation shows that quarantine alone is sufficient for the safety effect on this axis, while canonical ReAct action writeback improves trajectory hygiene and clean utility stability. We report AgentDojo MiniMax experiments as auxiliary evidence: selected-pair reruns were too stochastic to support a stable before/after defense claim.

## 1. Introduction

LLM agents are no longer single-turn text generators. They retrieve memory, call tools, write intermediate notes, and execute multi-step reasoning policies such as ReAct. In these systems, a malicious or contaminated input can influence the agent through internal channels before any final answer is produced. Memory poisoning is a particularly direct instance of this problem: the agent retrieves adversarial content from an external or semi-trusted knowledge source, then treats it as useful context during reasoning.

Existing agent security work has shown that prompt injection and memory poisoning can alter agent behavior. However, a practical runtime defense needs to answer a narrower systems question: when unsafe retrieved content exists, can the agent runtime prevent that content from entering the actionable reasoning context while preserving enough utility to complete the task? This paper studies that question through FlowFence-Lite.

FlowFence-Lite is designed as a runtime containment layer. In the broader project, the intended system includes propagation-aware risk scoring, lease-based privilege control, shared-memory/workspace governance, and dual trace logging. The current paper draft reports the strongest completed empirical slice: retrieval-memory containment on an adapted AgentPoison full-ReAct StrategyQA setup under MiniMax. We focus on this slice because it provides a stable before/after attack anchor, while other attempted axes, especially AgentDojo under MiniMax, did not yield stable selected-pair reruns.

The contribution of this draft is therefore deliberately scoped:

- We frame retrieval-memory poisoning as a runtime containment problem over internal agent context, not only a final-answer problem.
- We implement a FlowFence-Lite variant that quarantines unsafe retrieved memory before it reaches the model prompt and optionally canonicalizes ReAct action writeback.
- We evaluate the method on a fixed adapted AgentPoison MiniMax axis with three repeated runs per condition.
- We provide an ablation showing that quarantine is the core safety mechanism and canonical action writeback primarily improves trajectory hygiene.
- We document negative or blocked AgentDojo evidence rather than using unstable search hits as a headline baseline.

This is not yet a full multi-domain, multi-topology privacy propagation paper. Claims about topology, cascade size, runtime overhead, and superiority over multiple independent defense families remain future work unless additional experiments are added.

## 2. Problem Setting

### 2.1 Agent Runtime

We consider a text-first, tool-using LLM agent that operates through iterative reasoning steps. At each step, the agent can read retrieved memory, produce reasoning text, choose an action, and observe tool or environment outputs. In a full multi-agent runtime, similar channels would include inter-agent messages, shared memory, shared workspace writes, and tool arguments. The current empirical slice focuses on the retrieval-memory channel inside a full-ReAct loop.

### 2.2 Threat Model

The attacker can poison retrievable memory or knowledge-base content. When the agent searches memory, the poisoned content may be returned alongside benign content. If the poisoned content enters the model prompt unmodified, it may influence the agent's answer or action choice.

The attacker does not compromise the operating system, steal model weights, alter evaluator labels, or directly modify the defense code. The defense is allowed to inspect retrieved memory before it is exposed to the model prompt and to rewrite, quarantine, or block unsafe retrieved content.

### 2.3 Safety Objective

The immediate objective is retrieval-memory containment: poisoned content may be retrieved by the underlying memory system, but it should not be exposed to the model context in a way that can steer the agent. We therefore distinguish raw poisoned retrieval from exposed poisoned retrieval.

- Raw poisoned retrieval measures whether poisoned content was retrieved before defense processing.
- Exposed poisoned retrieval measures whether poisoned retrieved content reached the model prompt after defense processing.
- Attack manifestation measures whether the adversarial behavior targeted by the poisoning attack appears in the agent output.
- Clean utility measures task accuracy in the clean setting.
- Attacked utility measures task accuracy under attack.

This distinction is central. A defense should not receive credit merely because the attack input disappeared from the environment. The stronger evidence is that raw poisoned retrieval remains present, but the exposed poisoned retrieval and attack manifestation rates fall.

## 3. FlowFence-Lite

FlowFence-Lite is a runtime containment layer placed between agent actions and the information sources they consume or update. The broader design has four components: propagation-aware risk scoring, lease-based least privilege, shared-artifact governance, and structured tracing. The current evaluated implementation uses the subset needed for retrieval-memory containment.

### 3.1 Retrieval Quarantine

The quarantine mechanism inspects retrieved memory items before they are written into the agent's prompt context. Retrieved content judged unsafe is diverted into a quarantine zone. The agent can continue its reasoning loop, but the unsafe raw content is not exposed as normal contextual evidence.

In this draft, quarantine is the main safety mechanism. It directly targets the retrieval-memory boundary: poisoned content can still be returned by the retrieval backend, but the defense prevents it from becoming part of the model-visible ReAct context.

### 3.2 Canonical ReAct Action Writeback

Full-ReAct agents can become unstable when observations or previous actions drift from the expected format. The selected FlowFence-Lite variant therefore adds canonical action writeback. This does not replace quarantine. Instead, it normalizes the action representation that is written back into the ReAct trajectory after defense processing.

The hypothesis is that canonical action writeback improves trajectory hygiene and reduces repeated or drifted retrieval behavior. The ablation results support this as a utility-stability mechanism rather than as the source of the zero-exposure safety effect.

### 3.3 Scope of the Current Implementation

The current implementation should be viewed as a retrieval-memory containment instance of the broader FlowFence-Lite design. It does not yet evaluate lease revocation, topology-aware propagation scoring, workspace governance, or broad privacy policy enforcement over multiple internal channels. Those components remain part of the project direction but are not claimed as completed empirical contributions in this draft.

## 4. Experimental Setup

### 4.1 Main Axis: Adapted AgentPoison StrategyQA Full-ReAct

The main experiment uses an adapted AgentPoison StrategyQA full-ReAct comparator under the MiniMax provider profile.

Source artifacts:

- Task manifest: `data/tasks/agentpoison_strategyqa_fullreact_v1.json`
- No-defense config: `configs/experiment/agentpoison_fullreact_minimax27_triggerquery.yaml`
- Quarantine-only config: `configs/experiment/agentpoison_fullreact_flowfence_lite_minimax27_triggerquery_quarantine_only.yaml`
- Quarantine-actioncanon config: `configs/experiment/agentpoison_fullreact_flowfence_lite_minimax27_triggerquery_quarantine_actioncanon.yaml`
- Main result summary: `results/baseline_agentpoison_fullreact_minimax27_small_matrix_summary.json`
- Ablation summary: `results/ablation_agentpoison_fullreact_minimax27_quarantine_only_vs_actioncanon_summary.json`

The setup keeps the upstream AgentPoison ReAct-StrategyQA loop and DPR retrieval path via `local_wikienv.WikiEnv`. It uses the MiniMax provider profile `minimax27`.

### 4.2 Adaptation Note

This experiment is an adapted comparator, not a full official AgentPoison reproduction. Earlier full-context attempts under MiniMax completed but did not produce a trustworthy attack anchor: poisoned retrieval and attack manifestation were both effectively absent. The current comparator uses `trigger_question_only` adversarial search context to avoid that diagnosed trigger dilution and to establish a non-vacuous no-defense attack condition.

This adaptation is acceptable for a controlled containment test, but it must be stated explicitly. The result should be described as evidence on an adapted AgentPoison MiniMax axis, not as evidence that FlowFence-Lite reproduces and defeats official AgentPoison.

### 4.3 Conditions

We compare three conditions:

1. No defense.
2. FlowFence-Lite with quarantine only.
3. FlowFence-Lite with quarantine plus canonical ReAct action writeback.

Each condition has three completed runs. All reported values are means across the three runs, with min/max ranges shown where useful.

### 4.4 Metrics

The main metrics are:

- Exposed poisoned retrieval: case rate where poisoned retrieved content reaches the model prompt after defense processing.
- Raw poisoned retrieval: case rate where poisoned content is retrieved before defense processing.
- Attack manifestation: case rate where the adversarial answer manifests the poisoning attack rule.
- Clean utility: benign StrategyQA exact-match accuracy on the adapted subset.
- Attacked utility: adversarial StrategyQA exact-match accuracy on the adapted subset.
- Intervention event rate: fraction of retrieval events that triggered a defense intervention.

## 5. Results

### 5.1 Main Result

Table 1 reports the current paper-facing main result and ablation.

| condition | exposed poisoned retrieval | attack manifestation | raw poisoned retrieval | clean utility | attacked utility | intervention event rate |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| No defense | 0.4667 (0.36-0.52) | 0.2533 (0.16-0.36) | 0.4667 (0.36-0.52) | 0.3733 (0.28-0.44) | 0.3333 (0.32-0.36) | 0.0000 |
| FlowFence-Lite, quarantine only | 0.0000 (0.00-0.00) | 0.0000 (0.00-0.00) | 0.5333 (0.40-0.60) | 0.3067 (0.24-0.36) | 0.3733 (0.32-0.48) | 0.5805 (0.4894-0.6271) |
| FlowFence-Lite, quarantine + action-canon | 0.0000 (0.00-0.00) | 0.0000 (0.00-0.00) | 0.4400 (0.32-0.56) | 0.3600 (0.28-0.40) | 0.3867 (0.28-0.48) | 0.4770 (0.4267-0.5758) |

The no-defense condition establishes that the attack is non-vacuous on this axis. Exposed poisoned retrieval is non-zero in all three no-defense runs, with mean 0.4667. Attack manifestation is also non-zero in all three no-defense runs, with mean 0.2533.

FlowFence-Lite with quarantine plus action-canon reduces exposed poisoned retrieval to 0.0 in all three runs and reduces attack manifestation to 0.0 in all three runs. Raw poisoned retrieval remains non-zero, with mean 0.4400. This is the key containment pattern: the poisoned content still exists and is still retrieved by the underlying system, but it is not exposed to the model prompt after defense processing and the attack no longer manifests.

Utility should be interpreted conservatively. Clean utility is close but slightly lower for quarantine-actioncanon than no defense, changing from 0.3733 to 0.3600. Attacked utility is higher for quarantine-actioncanon than no defense, changing from 0.3333 to 0.3867. Because MiniMax full-ReAct execution is noisy, the appropriate claim is roughly preserved utility, not utility improvement.

### 5.2 Ablation: Quarantine Only vs. Quarantine + Action-Canon

The quarantine-only variant also reduces exposed poisoned retrieval and attack manifestation to 0.0 in all three runs. This shows that quarantine is sufficient for the safety effect on the adapted AgentPoison MiniMax axis. Canonical action writeback is therefore not necessary to achieve zero exposed poisoned retrieval in this setting.

However, quarantine-actioncanon has better trajectory indicators than quarantine-only. Clean utility improves from 0.3067 to 0.3600, and intervention event rate drops from 0.5805 to 0.4770. This suggests that canonical action writeback reduces repeated or drifted retrieval behavior and stabilizes the full-ReAct trajectory. The evidence is suggestive rather than definitive because utility variance remains high.

The mechanism conclusion is therefore:

- Quarantine is the core safety mechanism for retrieval-memory containment on this axis.
- Canonical action writeback improves trajectory hygiene and clean utility stability.
- The selected method should include both, but the zero-exposure safety claim should be attributed primarily to quarantine.

### 5.3 AgentDojo Auxiliary Evidence

AgentDojo was investigated as a possible same-provider before/after defense baseline under MiniMax. The resulting evidence should not be used as a main defense-effect claim.

Relevant artifacts:

- `results/baseline_agentdojo_minimax27_banking_selected_native_defenses_summary.json`
- `results/baseline_agentdojo_minimax27_banking_stable_pair_search_summary.json`
- `results/baseline_agentdojo_minimax27_axis_switch_attempt_summary.json`

The high-level observation is that MiniMax AgentDojo searches produced non-vacuous search hits, but selected-pair reruns repeatedly failed to reproduce stable dual success. For example, a banking pair produced `utility=true/security=true` in search, but selected no-defense reruns failed to reproduce that result. Axis-switch attempts found additional search hits, but selected reruns again failed to provide a stable no-defense anchor.

This supports a limitation rather than a headline result: under the tested MiniMax settings, AgentDojo selected-pair evaluation was stochastic enough that it could not support a robust before/after defense claim. We therefore keep AgentDojo as auxiliary stochastic/blocked evidence and base the main empirical claim on the adapted AgentPoison axis.

## 6. Discussion

### 6.1 Why Raw vs. Exposed Retrieval Matters

A common failure mode in evaluating containment defenses is to report lower attack success without showing whether the attack input was still present. If the attack input is absent, the defense may not have contained anything. The raw/exposed distinction avoids this ambiguity.

In the current results, raw poisoned retrieval remains non-zero under FlowFence-Lite. This means the attack pressure is still present at the retrieval layer. The zero exposed poisoned retrieval result therefore indicates an active containment effect at the boundary between retrieval and model-visible context.

### 6.2 What This Result Supports

The current evidence supports a narrow but meaningful claim:

On an adapted AgentPoison full-ReAct comparator under MiniMax, FlowFence-Lite retrieval quarantine prevents poisoned retrieved content from reaching the model prompt and eliminates attack manifestation across three repeated runs, while roughly preserving task utility.

The ablation strengthens the mechanism story: quarantine alone explains the safety effect, while canonical ReAct action writeback improves trajectory hygiene and clean utility stability.

### 6.3 What This Result Does Not Support

The current evidence does not support broad claims that FlowFence-Lite is generally better than all prompt-injection defenses or that it solves multi-agent privacy propagation. In particular, the following claims are not ready:

- FlowFence-Lite outperforms multiple independent defense families such as prompt filters, static ACLs, topology guards, and data minimizers.
- FlowFence-Lite generalizes across topologies, domains, attacks, or providers.
- FlowFence-Lite is runtime-feasible under measured latency and token overhead constraints.
- AgentDojo provides a stable main before/after defense baseline under MiniMax.
- The current AgentPoison result is a full official AgentPoison reproduction.

These gaps should be handled as limitations or as a future experimental plan.

## 7. Related Work

Agent security benchmarks such as AgentDojo and ASB show that tool-using agents are vulnerable to prompt injection and related attacks. Their main relevance here is methodological: they demonstrate the importance of dynamic, tool-in-the-loop evaluation rather than static prompt-only tests.

AgentPoison directly motivates the retrieval-memory poisoning setting. It shows that memory and knowledge-base content can become an attack surface for LLM agents. Our current experiment uses an adapted AgentPoison StrategyQA full-ReAct setup as the main empirical axis, with the important caveat that this is not a full official reproduction.

Prior work on multi-agent propagation and topology, including Agent Smith and G-Safeguard, motivates the broader FlowFence-Lite project. These works suggest that security failures can spread across agent graphs and that topology matters. The current draft does not yet evaluate topology sensitivity, but the broader FlowFence-Lite design is intended to support that evaluation.

Privacy-focused agent evaluation, including AgentDAM and memory-extraction work such as MEXTRA, motivates policy-aware privacy metrics and internal-channel leakage measurement. The current draft uses this literature as motivation, while the completed empirical result remains focused on retrieval-memory poisoning containment rather than full privacy-policy enforcement.

## 8. Limitations

The main limitation is scope. The completed evidence is one adapted AgentPoison MiniMax axis plus one same-axis ablation. It is useful because the no-defense attack is non-vacuous and repeated, but it is not broad enough to support a full systems-security claim.

The AgentPoison setup is adapted. The use of `trigger_question_only` adversarial search context is documented and necessary for the current MiniMax attack anchor, but it means the result should not be described as official AgentPoison reproduction.

The model axis is MiniMax only. No claim is made about robustness across model providers.

Utility is noisy under full-ReAct execution. The current result supports roughly preserved utility, not a strong utility improvement claim.

AgentDojo under MiniMax is unstable as a selected-pair before/after baseline. Its current role is an auxiliary negative or stochastic result, not a main comparison.

Runtime overhead, token overhead, false block rate, topology sensitivity, cascade size, privilege reach, and held-out generalization remain unevaluated in the current artifact set.

## 9. Future Work

The next experimental step depends on the paper target.

For a narrow workshop or short-paper target, the immediate next step is to polish the current AgentPoison MiniMax result, add a concise system diagram, and write a reproducibility appendix around the saved configs and summaries.

For a fuller systems paper, the next experiments should be prioritized as follows:

1. Add one same-axis weak defense comparator, such as rewrite-only or safe-view rewrite, to reduce the concern that the paper only compares no defense against the proposed method.
2. Measure runtime overhead, token overhead, and false block proxies on the current same-axis setup.
3. Add a small topology or shared-artifact experiment only after the retrieval-memory result is stable and the metric definitions are fixed.
4. Revisit AgentDojo only if a timeout-bounded selected-stability harness is built; otherwise keep it as blocked auxiliary evidence.

## 10. Conclusion

This draft reports a narrow but concrete retrieval-memory containment result. On an adapted AgentPoison full-ReAct comparator under MiniMax, no defense repeatedly exposes poisoned retrieved content and produces non-zero attack manifestation. FlowFence-Lite reduces exposed poisoned retrieval and attack manifestation to zero across three repeated runs while raw poisoned retrieval remains non-zero. This supports the claim that runtime quarantine can contain poisoned retrieval before it reaches model-visible reasoning context.

The ablation shows that quarantine is the core safety mechanism on this axis, while canonical ReAct action writeback improves trajectory hygiene and clean utility stability. The evidence is promising but deliberately scoped: broader claims about multi-agent privacy propagation, topology, runtime feasibility, and superiority over multiple independent defense families require additional experiments.

## Appendix A. Paper-Ready Claim Wording

Supported wording:

> On an adapted AgentPoison full-ReAct comparator under MiniMax, FlowFence-Lite reduces exposed poisoned retrieval and attack manifestation to zero across three repeated runs.

Supported wording:

> Quarantine is sufficient for the safety effect on this axis; canonical ReAct action writeback improves trajectory hygiene and clean utility stability.

Avoid:

> FlowFence-Lite reproduces and beats official AgentPoison.

Avoid:

> FlowFence-Lite is broadly better than AgentDojo native defenses.

Avoid:

> FlowFence-Lite significantly improves utility.

## Appendix B. Reproducibility Pointers

Main artifacts:

- `results/baseline_agentpoison_fullreact_minimax27_small_matrix_summary.json`
- `results/ablation_agentpoison_fullreact_minimax27_quarantine_only_vs_actioncanon_summary.json`

Main configs:

- `configs/experiment/agentpoison_fullreact_minimax27_triggerquery.yaml`
- `configs/experiment/agentpoison_fullreact_flowfence_lite_minimax27_triggerquery_quarantine_only.yaml`
- `configs/experiment/agentpoison_fullreact_flowfence_lite_minimax27_triggerquery_quarantine_actioncanon.yaml`

Task manifest:

- `data/tasks/agentpoison_strategyqa_fullreact_v1.json`

Auxiliary AgentDojo artifacts:

- `results/baseline_agentdojo_minimax27_banking_selected_native_defenses_summary.json`
- `results/baseline_agentdojo_minimax27_banking_stable_pair_search_summary.json`
- `results/baseline_agentdojo_minimax27_axis_switch_attempt_summary.json`
