# Current Evidence Index

## 1. Scope

This is a P0 evidence index for the current FlowFence-Lite AgentPoison retrieval-memory containment axis.

The current saved evidence is about an adapted AgentPoison full-ReAct retrieval-memory containment comparator using StrategyQA-style tasks and the MiniMax provider profile.

The current defense scope is retrieval-memory-only: the indexed evidence concerns whether poisoned retrieved memory is released into model-visible context and whether attack manifestation occurs.

This is not yet a multi-agent propagation benchmark. It does not evaluate cascades across agents, topology effects, shared workspaces, privilege reach, or cross-channel leakage.

## 2. Provider Constraint

Current experiments use the MiniMax provider only.

All future experiments in this phase should remain MiniMax-only unless the human explicitly changes the rule.

There is no current evidence for non-MiniMax provider generalization.

## 3. Supported P0 Claims

### Claim S1: no-defense creates non-vacuous attack pressure on the adapted comparator.

- Evidence artifact path: `results/baseline_agentpoison_fullreact_minimax27_small_matrix_summary.json`
- Comparison target: no defense on the adapted AgentPoison full-ReAct MiniMax comparator.
- Observation: no-defense exposed poisoned retrieval in all three saved runs, with mean exposed poisoned retrieval case rate 0.4667 and mean attack manifestation rate 0.2533.
- Confidence level: high
- Caveat: this is an adapted comparator axis with trigger-question adversarial search context; it must not be described as full official AgentPoison reproduction.

### Claim S2: FlowFence-Lite quarantine plus canonical ReAct action writeback contains exposure and manifestation on the same axis.

- Evidence artifact path: `results/baseline_agentpoison_fullreact_minimax27_small_matrix_summary.json`
- Comparison target: no defense versus FlowFence-Lite quarantine plus canonical ReAct action writeback on the same adapted MiniMax comparator.
- Observation: raw poisoned retrieval remains non-zero under FlowFence-Lite, with mean raw poisoned retrieval case rate 0.44, while exposed poisoned retrieval and attack manifestation are 0.0 in all three saved runs.
- Confidence level: high
- Caveat: this supports retrieval-memory containment on this saved same-axis setting only; it does not establish broader benchmark, topology, or provider generalization.

### Claim S3: quarantine appears sufficient for the safety effect on this retrieval-memory axis.

- Evidence artifact path: `results/ablation_agentpoison_fullreact_minimax27_quarantine_only_vs_actioncanon_summary.json`
- Comparison target: quarantine-only versus quarantine plus canonical ReAct action writeback.
- Observation: both quarantine-only and quarantine-actioncanon reduce exposed poisoned retrieval and attack manifestation to 0.0 across the three saved runs.
- Confidence level: high
- Caveat: action canonicalization should be framed as trajectory hygiene and utility-stability support, not as necessary for the zero-exposure safety result on this axis.

### Claim S4: same-axis measured overhead evidence exists for a saved MiniMax overhead slice.

- Evidence artifact path: `results/overhead_agentpoison_fullreact_minimax27_same_axis_measured_summary.json`
- Comparison target: no defense versus quarantine-actioncanon on an instrumented 20-case overhead slice.
- Observation: the artifact records end-to-end wall time, LLM call wall time, provider request time, provider token usage, token proxy, defense inspection count, and defense wall time. The recorded defense wall time per case is very small relative to LLM wall time on this slice.
- Confidence level: medium
- Caveat: this is a one-run runtime-feasibility slice, not the full 25-question repeated efficacy matrix; it should not be generalized beyond the saved MiniMax slice.

### Claim S5: existing traces also support a same-axis overhead proxy analysis.

- Evidence artifact path: `results/overhead_agentpoison_fullreact_minimax27_same_axis_proxy_summary.json`
- Comparison target: no defense, rewrite-only, quarantine-only, and quarantine-actioncanon using saved case-detail traces.
- Observation: the proxy artifact reports model-call, ReAct-step, trajectory-size, and observation-character proxies across the saved repeated runs.
- Confidence level: medium
- Caveat: this is not measured provider latency or provider token usage; it is trace-derived proxy evidence only.

## 4. Partially Supported Claims

### Claim P1: utility is roughly preserved, not improved.

- Evidence artifact path: `results/baseline_agentpoison_fullreact_minimax27_small_matrix_summary.json`
- Comparison target: no defense versus FlowFence-Lite quarantine-actioncanon.
- Observation: clean utility mean changes from 0.3733 under no defense to 0.36 under FlowFence-Lite; attacked utility changes from 0.3333 to 0.3867.
- Confidence level: medium
- Caveat: MiniMax full-ReAct utility is noisy; the evidence supports conservative wording such as "roughly preserved," not "improved."

### Claim P2: rewrite-only can also block known detector-mediated exposure on this same-axis setting.

- Evidence artifact path: `results/baseline_agentpoison_fullreact_minimax27_rewrite_only_weak_comparator_summary.json`
- Comparison target: rewrite-only weak comparator versus no defense and FlowFence-Lite quarantine-actioncanon.
- Observation: rewrite-only reduces exposed poisoned retrieval and attack manifestation to 0.0 in all three saved runs while raw poisoned retrieval remains non-zero.
- Confidence level: medium
- Caveat: this comparator uses the same detector-mediated unsafe-record identification path; it narrows the claim to structured containment semantics rather than unique necessity of quarantine.

### Claim P3: static keyword filtering is a strong weak baseline on the known-trigger axis.

- Evidence artifact path: `results/baseline_agentpoison_fullreact_minimax27_static_keyword_filter_weak_comparator_summary.json`
- Comparison target: static keyword filter versus no defense and FlowFence-Lite on the same adapted known-trigger axis.
- Observation: the static keyword filter reduces exposed poisoned retrieval and attack manifestation to 0.0 across the saved runs, with mean raw poisoned retrieval 0.4667 and mean intervention rate 0.4961.
- Confidence level: medium
- Caveat: this should be framed as known-trigger same-axis evidence, not as evidence that static filters are robust under paraphrase or adaptive attacks.

### Claim P4: held-out instruction evidence is stress-test evidence only.

- Evidence artifact path: `results/baseline_agentpoison_fullreact_minimax27_heldout_instruction_matrix_summary.json`
- Comparison target: no defense, non-oracle static keyword filter, and FlowFence-Lite quarantine-actioncanon under a paraphrased held-out poisoned instruction.
- Observation: the non-oracle static keyword filter has 0.0 mean intervention rate, non-zero exposed poisoned retrieval, and non-zero attack manifestation; FlowFence-Lite records non-zero raw poisoned retrieval but 0.0 exposed poisoned retrieval and 0.0 attack manifestation.
- Confidence level: medium
- Caveat: this is a stress test on one held-out instruction family, not broad held-out attack generalization.

### Claim P5: AgentDojo MiniMax evidence is auxiliary and stochastic, not a stable main baseline.

- Evidence artifact paths: `results/baseline_agentdojo_minimax27_axis_switch_attempt_summary.json`, `results/baseline_agentdojo_minimax27_banking_stable_pair_search_summary.json`, `results/baseline_agentdojo_minimax27_banking_selected_native_defenses_summary.json`
- Comparison target: AgentDojo MiniMax search axes and selected native-defense reruns.
- Observation: searches produced some non-vacuous candidates, but selected reruns did not stably reproduce no-defense dual success; native-defense observations are therefore auxiliary.
- Confidence level: medium-low
- Caveat: this evidence should not be used as a robust AgentDojo mainline superiority result.

## 5. Unsupported Claims

- Multi-agent propagation containment.
- Topology materially changes privacy risk.
- Cascade-size reduction across topologies.
- Privilege-reach reduction.
- Shared workspace governance.
- Cross-channel privacy leakage containment.
- Broad superiority over independent defense families.
- Official AgentPoison reproduction.
- Robust AgentDojo mainline superiority.
- Non-MiniMax provider generalization.
- Learned graph risk scoring.
- 8/16/32-agent scaling.
- Browser or multimodal experiments.

## 6. Claims That Must Not Be Made

- Do not claim FlowFence-Lite reproduces and beats official AgentPoison.
- Do not claim FlowFence-Lite is broadly better than AgentDojo native defenses.
- Do not claim FlowFence-Lite is uniquely necessary on the known-trigger retrieval axis, because static keyword filtering is a strong weak baseline there.
- Do not claim topology effects before P1 topology experiments.
- Do not claim broad generalization beyond MiniMax.
- Do not claim utility improvement unless a future controlled experiment supports it.

## 7. Evidence Artifacts

| artifact path | inspected status | evidence type | what it supports | limitations |
| --- | --- | --- | --- | --- |
| `papers/claims_checklist.md` | INSPECTED | paper-facing claim checklist | Current claim wording, supported/unsupported claim boundaries, and caveats. | Checklist mirrors existing evidence; it is not itself a raw result. |
| `results/baseline_agentpoison_fullreact_minimax27_small_matrix_summary.json` | INSPECTED | adapted AgentPoison MiniMax main matrix summary | No-defense attack pressure; FlowFence-Lite raw-vs-exposed containment; rough utility preservation. | Adapted same-axis comparator, not official AgentPoison reproduction. |
| `results/ablation_agentpoison_fullreact_minimax27_quarantine_only_vs_actioncanon_summary.json` | INSPECTED | quarantine/action-canonicalization ablation summary | Quarantine sufficiency for safety on this axis; action canonicalization as trajectory hygiene and utility-stability support. | Same-axis ablation only. |
| `results/baseline_agentpoison_fullreact_minimax27_rewrite_only_weak_comparator_summary.json` | INSPECTED | same-axis weak comparator summary | Rewrite-only can also block detector-mediated exposure and manifestation on the same axis. | Uses the same unsafe-record identification path; does not prove broad rewrite robustness. |
| `results/baseline_agentpoison_fullreact_minimax27_static_keyword_filter_weak_comparator_summary.json` | INSPECTED | independent static keyword weak comparator summary | Static keyword filtering is strong on the known-trigger axis. | Known-trigger same-axis result; brittle under paraphrase stress. |
| `results/baseline_agentpoison_fullreact_minimax27_heldout_instruction_matrix_summary.json` | INSPECTED | held-out instruction stress-test summary | Non-oracle static keyword brittleness under paraphrase; FlowFence-Lite containment under this stress test. | One stress-test family; not broad held-out generalization. |
| `results/overhead_agentpoison_fullreact_minimax27_same_axis_measured_summary.json` | INSPECTED | measured overhead slice summary | Wall-clock, provider-token, LLM-call, and defense-inspection evidence on an instrumented MiniMax slice. | One saved slice, not the full repeated efficacy matrix. |
| `results/overhead_agentpoison_fullreact_minimax27_same_axis_proxy_summary.json` | INSPECTED | trace-derived overhead proxy summary | Model-call, ReAct-step, trajectory-size, and observation-size overhead proxies across saved traces. | Proxy evidence only; not measured provider latency or provider token usage. |
| `results/baseline_agentdojo_minimax27_axis_switch_attempt_summary.json` | INSPECTED | AgentDojo auxiliary axis-search summary | AgentDojo MiniMax axis search was stochastic and selected reruns did not provide a stable main baseline. | Partial/interrupted axes are included; not a robust defense comparison. |
| `results/baseline_agentdojo_minimax27_banking_stable_pair_search_summary.json` | INSPECTED | AgentDojo banking stable-pair search summary | No stable no-defense dual-success banking pair was found for a hard before anchor. | Auxiliary evidence only. |
| `results/baseline_agentdojo_minimax27_banking_selected_native_defenses_summary.json` | INSPECTED | AgentDojo selected native-defense summary | Selected native-defense observations exist but no-defense selected reruns failed to reproduce the original anchor. | Not usable as a stable mainline AgentDojo superiority result. |

## 8. Current Method Boundaries

Current implementation is centered on retrieval-memory inspection.

Current metrics observe retrieval-memory exposure and attack manifestation.

Current defense output includes risk score, reason codes, decision, rewritten content, lease signal, and poisoned-content exposure flags.

Current lease signal is not yet a full runtime lease mechanism.

Current evidence is not yet an event-graph, cascade, or privilege-reach evaluation.

## 9. Next Evidence Required

1. P0 eventization adapter.
2. P0 event audit and metric recomputation.
3. P0 failure-case export.
4. P1 synthetic multi-agent propagation runtime.
5. P1 topology matrix using `chain_4`, `star_4`, and `blackboard_4`.
6. P1 cascade evaluator.
7. P1 privilege-reach evaluator.
8. P1 channel-level leakage evaluator.
9. MiniMax-only real-model confirmation after mock MAS runtime works.

## 10. Recommended Next PRs

1. codex/p0-eventization
2. codex/p0-audit-and-recompute
3. codex/p0-failure-case-export
4. codex/p1-mas-synthetic-runtime
5. codex/p1-mas-sweep
