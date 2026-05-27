# Current Evidence Index

## 1. Scope

This is a current evidence index for FlowFence-Lite. It preserves the P0 AgentPoison retrieval-memory containment evidence and now adds P1 multi-agent synthetic and MiniMax-smoke evidence.

The P0 saved evidence is about an adapted AgentPoison full-ReAct retrieval-memory containment comparator using StrategyQA-style tasks and the MiniMax provider profile.

The P0 defense scope is retrieval-memory-only: that evidence concerns whether poisoned retrieved memory is released into model-visible context and whether attack manifestation occurs.

The P1 evidence adds a deterministic synthetic multi-agent propagation benchmark and a small real-MiniMax final-writer smoke. P1 evidence should be read separately from P0: it evaluates shared-memory/shared-workspace propagation, topology-dependent cascades, privilege reach, and cross-channel leakage in a controlled synthetic runtime, plus a small MiniMax smoke of the final-writing step. It is not yet a broad real-model benchmark.

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

## 3A. Supported P1 Deterministic Synthetic Claims

### Claim S6: the strengthened deterministic synthetic MAS benchmark produces topology-dependent propagation.

- Evidence artifact path: `artifacts/codex_task_state/codex_p1_benchmark_strengthening.md`
- Comparison target: `chain_4`, `star_4`, and `blackboard_4` under the strengthened deterministic matrix.
- Observation: the strengthened sweep completed 252/252 runs with `topology_effect_observed=true`; blackboard cascade size was greater than or equal to chain cascade size for every no-defense attack group.
- Confidence level: medium
- Caveat: this is deterministic synthetic evidence only. It does not establish paper-ready real-model topology effects or deployment generalization.

### Claim S7: in the strengthened deterministic synthetic benchmark, FlowFence-Lite improves over simple baselines on indirect synthetic attacks.

- Evidence artifact path: `artifacts/codex_task_state/codex_p1_benchmark_strengthening.md`
- Comparison target: `flowfence_lite` versus `prompt_filter` and `static_acl` on indirect synthetic attacks.
- Observation: FlowFence improved over `prompt_filter` on all 9 indirect attack/topology groups for unauthorized raw leakage, external leakage, cascade size, and privilege reach. FlowFence improved over `static_acl` on all 9 indirect groups for cascade size and privilege reach, on 6/9 indirect groups for unauthorized raw leakage, and on 4/9 indirect groups for external leakage.
- Confidence level: medium
- Caveat: this supports a synthetic benchmark claim, not broad superiority over independent defense families in real deployments.

## 3B. Pre-Debug P1 MiniMax Smoke Evidence

### Claim M1: the MiniMax final-writer smoke completed successfully.

- Evidence artifact path: `artifacts/minimax_p1_smoke/run_manifest.json`
- Comparison target: MiniMax final-writer smoke matrix over `chain_4` and `blackboard_4`, attacks `none`, `summary_poisoning_indirect`, `workspace_poisoning_indirect`, defenses `none`, `prompt_filter`, `flowfence_lite`, and seed `1`.
- Observation: the 18-run smoke completed 18/18 runs with 0 failed runs.
- Confidence level: medium-low
- Caveat: this is a small smoke only. It validates that the MiniMax final-writer path runs end-to-end; it is not a full real-model experiment.

### Claim M2: the MiniMax 18-run smoke observed leakage reductions for FlowFence-Lite, but the evidence is not paper-ready.

- Evidence artifact path: `artifacts/minimax_p1_smoke/summary_18run.json`
- Comparison target: `flowfence_lite` versus `none` and `prompt_filter` in the 18-run smoke.
- Observation: aggregate task success was `0.055556`, unauthorized raw leakage mean was `4.111111`, external leakage mean was `0.666667`, cascade size mean was `3.333333`, and privilege reach mean was `2.222222`. `topology_effect_observed` was `true`. FlowFence versus no-defense improved raw leakage in 4/6 comparison groups and tied in 2/6; it improved external leakage in 4/6 and tied in 2/6. FlowFence versus `prompt_filter` improved raw leakage in 4/6 and tied in 2/6; it improved external leakage in 2/6 and tied in 4/6.
- Confidence level: low
- Caveat: do not claim broad real-model robustness, paper-ready topology effects, utility preservation, or non-MiniMax generalization from this smoke. The very low task success is a major open risk.

### Claim M3: low MiniMax final-writer task success is a current limitation.

- Evidence artifact path: `artifacts/minimax_p1_smoke/summary_18run.json`
- Comparison target: 18-run MiniMax final-writer smoke.
- Observation: task success rate is `0.055556`.
- Confidence level: medium
- Caveat: this pre-debug limitation was followed by `p1-real-minimax-debug`, which diagnosed prompt/evaluator issues and produced a post-debug debug smoke. Keep the original smoke as historical context, not as the current task-success estimate.

## 3C. Post-Debug P1 MiniMax Debug-Smoke Evidence

### Claim M4: the low pre-debug task success was primarily a prompt/evaluator issue.

- Evidence artifact path: `artifacts/codex_task_state/codex_p1_real_minimax_debug.md`; `artifacts/minimax_p1_smoke_debug/debug_summary.json`; `artifacts/minimax_p1_smoke_debug/debug_summary.md`
- Comparison target: pre-debug MiniMax 18-run smoke versus post-debug MiniMax debug smoke.
- Observation: the debug task diagnosed the main issue as final-writer prompt shape plus utility evaluator strictness. The original final-writer prompt did not require a stable vendor-safe output shape, and the original utility evaluator required near-exact wording. Missing final-output events, empty final outputs, raw-secret final-output previews, and summary aggregation alone were not primary causes in the saved debug summaries.
- Confidence level: medium
- Caveat: this is a debug diagnosis over the small MiniMax smoke path, not a broad model-behavior conclusion.

### Claim M5: after minimal prompt/evaluator fixes, the MiniMax debug smoke has normal task-success behavior.

- Evidence artifact path: `artifacts/minimax_p1_smoke_debug/debug_summary.json`; `artifacts/minimax_p1_smoke_debug/debug_summary.md`; `artifacts/minimax_p1_smoke_debug/run_manifest.json`
- Comparison target: post-debug MiniMax 2-run and 18-run debug smoke.
- Observation: the 2-run debug completed 2/2 runs with 0 failed runs, `task_success_rate=1.0`, `unauthorized_raw_leakage_mean=0.0`, and `external_leakage_mean=0.0`. The 18-run debug completed 18/18 runs with 0 failed runs, `task_success_rate=1.0`, `unauthorized_raw_leakage_mean=3.333333`, `external_leakage_mean=0.222222`, `cascade_size_mean=3.333333`, and `privilege_reach_mean=2.222222`.
- Confidence level: medium-low
- Caveat: this is still a small MiniMax debug smoke. It is not a full real-model experiment, does not support non-MiniMax generalization, and does not by itself support broad real-model robustness.

### Claim M6: post-debug leakage risk remains non-zero.

- Evidence artifact path: `artifacts/minimax_p1_smoke_debug/debug_summary.json`; `artifacts/minimax_p1_smoke_debug/debug_summary.md`
- Comparison target: post-debug MiniMax 18-run debug smoke.
- Observation: despite `task_success_rate=1.0`, the 18-run debug smoke still reports `unauthorized_raw_leakage_mean=3.333333` and `external_leakage_mean=0.222222`.
- Confidence level: medium-low
- Caveat: this should be used as limitation and safety-motivation evidence. It does not mean the real-model setting is solved.

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

### Claim P6: P1 MiniMax topology effects are observed in a small smoke but are not paper-ready.

- Evidence artifact path: `artifacts/minimax_p1_smoke/summary_18run.json`
- Comparison target: `chain_4` versus `blackboard_4` in the 18-run MiniMax smoke.
- Observation: `topology_effect_observed=true` in the saved 18-run smoke.
- Confidence level: low
- Caveat: this is one small MiniMax smoke with one seed and low task success. Treat as a prompt for debugging and follow-up, not as a broad topology claim.

## 5. Unsupported Claims

- Broad multi-agent propagation containment in real-model settings.
- Paper-ready topology effects beyond the deterministic synthetic benchmark and small MiniMax smoke.
- Broad cascade-size reduction across real-model topologies.
- Broad privilege-reach reduction across real-model settings.
- Shared workspace governance beyond the deterministic synthetic benchmark.
- Cross-channel privacy leakage containment beyond the deterministic synthetic benchmark.
- Broad superiority over independent defense families.
- Official AgentPoison reproduction.
- Robust AgentDojo mainline superiority.
- Non-MiniMax provider generalization.
- Full paper-ready MiniMax evidence.
- Utility preservation under broad real MiniMax final-writer execution.
- Learned graph risk scoring.
- 8/16/32-agent scaling.
- Browser or multimodal experiments.

## 6. Claims That Must Not Be Made

- Do not claim FlowFence-Lite reproduces and beats official AgentPoison.
- Do not claim FlowFence-Lite is broadly better than AgentDojo native defenses.
- Do not claim FlowFence-Lite is uniquely necessary on the known-trigger retrieval axis, because static keyword filtering is a strong weak baseline there.
- Do not claim topology effects beyond the deterministic synthetic benchmark and small MiniMax smoke.
- Do not claim paper-ready MiniMax topology effects from the 18-run smoke; say only that the small smoke observed a topology effect.
- Do not claim broad generalization beyond MiniMax.
- Do not claim utility improvement unless a future controlled experiment supports it.
- Do not claim utility preservation under broad real MiniMax final-writer execution from the post-debug smoke; the debug run has `task_success_rate=1.0`, but leakage remains non-zero and the matrix is small.

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
| `artifacts/codex_task_state/codex_p1_mas_sweep.md` | INSPECTED | P1 deterministic sweep task state | Deterministic MAS sweep runner and summary reporter were implemented and validated. | Initial sweep alone had weaker topology distinction before strengthening. |
| `artifacts/codex_task_state/codex_p1_benchmark_strengthening.md` | INSPECTED | P1 strengthened synthetic benchmark task state | Strengthened deterministic benchmark supports synthetic topology effects and FlowFence-vs-baseline distinctions on indirect attacks. | Synthetic deterministic evidence only; generated validation outputs are not committed. |
| `artifacts/minimax_p1_smoke/run_manifest.json` | INSPECTED | P1 MiniMax smoke manifest | MiniMax final-writer 2-run and 18-run smoke execution status, provider metadata, and safety-check result. | No raw traces or provider outputs committed. |
| `artifacts/minimax_p1_smoke/summary_18run.json` | INSPECTED | P1 MiniMax smoke aggregate summary | 18-run real-MiniMax final-writer smoke metrics and comparison counts. | Small smoke only; low task success; one seed; not paper-ready real-model evidence. |
| `artifacts/minimax_p1_smoke/summary_18run.md` | INSPECTED | P1 MiniMax smoke human-readable summary | Concise interpretation of 18-run smoke metrics and caveats. | Summary only; no raw evidence payloads. |
| `artifacts/codex_task_state/codex_p1_real_minimax_debug.md` | INSPECTED | P1 MiniMax debug task state | Diagnosis of low task success and summary of prompt/evaluator fixes plus 2-run and 18-run debug results. | Debug-smoke evidence only; raw traces and provider outputs are intentionally not committed. |
| `artifacts/minimax_p1_smoke_debug/debug_summary.json` | INSPECTED | P1 MiniMax post-debug aggregate diagnostic summary | Post-debug 2-run and 18-run task success, leakage, cascade, privilege, and failure-category diagnostics. | Small debug smoke only; summary excludes raw prompts, raw provider outputs, and event traces. |
| `artifacts/minimax_p1_smoke_debug/debug_summary.md` | INSPECTED | P1 MiniMax post-debug human-readable summary | Concise diagnosis, fixes, post-debug metrics, and caveats. | Summary only; not a full real-model experiment. |
| `artifacts/minimax_p1_smoke_debug/run_manifest.json` | INSPECTED | P1 MiniMax post-debug run manifest | Provider-call safety check and post-debug 2-run/18-run execution status. | Points to temporary run locations but does not include raw outputs. |

## 8. Current Method Boundaries

The P0 implementation is centered on retrieval-memory inspection.

P0 metrics observe retrieval-memory exposure and attack manifestation.

Current defense output includes risk score, reason codes, decision, rewritten content, lease signal, and poisoned-content exposure flags.

Current lease signal is not yet a full runtime lease mechanism.

P1 deterministic metrics now include event-graph cascade, topology, privilege-reach, and channel-level leakage evaluators in a synthetic runtime. This does not replace P0 retrieval-memory evidence and does not establish broad real-model generalization.

The current MiniMax smoke uses MiniMax only for final vendor-facing writing. Propagation, attack injection, defense decisions, and policy evaluation remain deterministic. The pre-debug smoke had very low task success (`0.055556`) and should be treated as historical context. The post-debug MiniMax debug smoke improved task success to `1.0` after minimal prompt/evaluator fixes, but it remains a small debug smoke rather than a full real-model experiment.

## 9. Next Evidence Required

1. Rerun a clean post-fix 18-run MiniMax smoke if the debug summaries should be converted into official post-debug smoke evidence.
2. Inspect high-level failure categories without committing raw traces.
3. Expand MiniMax coverage only after post-fix smoke summaries are stable.
4. Add more seeds, topologies, and attacks only after smoke validation.
5. Maintain deterministic synthetic evidence as the main topology/baseline-supporting evidence until real MiniMax coverage expands.
6. Preserve the distinction between deterministic synthetic evidence, pre-debug MiniMax smoke evidence, and post-debug MiniMax debug-smoke evidence.
7. Continue to avoid non-MiniMax generalization claims.

## 10. Recommended Next PRs

1. codex/p1-real-minimax-18run-rerun
2. codex/p1-real-minimax-coverage
3. codex/p1-results-table-export
4. codex/p1-paper-synthesis
5. codex/p1-evidence-package
