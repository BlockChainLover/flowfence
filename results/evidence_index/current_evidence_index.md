# Current Evidence Index

## 1. Scope

This is a current evidence index for FlowFence-Lite. It preserves the P0 AgentPoison retrieval-memory containment evidence and now adds P1 multi-agent synthetic and MiniMax-smoke evidence.

The P0 saved evidence is about an adapted AgentPoison full-ReAct retrieval-memory containment comparator using StrategyQA-style tasks and the MiniMax provider profile.

The P0 defense scope is retrieval-memory-only: that evidence concerns whether poisoned retrieved memory is released into model-visible context and whether attack manifestation occurs.

The P1 evidence adds deterministic synthetic multi-agent propagation benchmarks, MiniMax final-writer smoke/debug runs, and MiniMax-only P1 MAS coverage over the synthetic deterministic runtime. P1 evidence should be read separately from P0: it evaluates shared-memory/shared-workspace propagation, topology-dependent cascades, privilege reach, and cross-channel leakage in a controlled synthetic runtime with MiniMax final-writer calls. It is not non-MiniMax generalization, production safety evidence, or real browser/desktop/computer-use agent evidence.

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

## 3D. Clean Post-Fix P1 MiniMax Smoke and Audit Evidence

### Claim M7: the clean post-fix MiniMax 18-run smoke completed and observed a topology effect, but remains a small smoke.

- Evidence artifact path: `artifacts/minimax_p1_smoke_postfix/summary_18run.json`; `artifacts/minimax_p1_smoke_postfix/summary_18run.md`; `artifacts/minimax_p1_smoke_postfix/run_manifest.json`
- Comparison target: clean post-fix MiniMax final-writer smoke over `chain_4` and `blackboard_4`, attacks `none`, `summary_poisoning_indirect`, `workspace_poisoning_indirect`, defenses `none`, `prompt_filter`, `flowfence_lite`, and seed `1`.
- Observation: the run completed 18/18 runs with 0 failed runs. Aggregate `task_success_rate=0.888889`, `unauthorized_raw_leakage_mean=4.111111`, `external_leakage_mean=0.444444`, `cascade_size_mean=3.333333`, `privilege_reach_mean=2.222222`, and `topology_effect_observed=true`.
- Confidence level: medium-low
- Caveat: this is a small MiniMax-only one-seed smoke, not broad real-model robustness, full paper-ready MiniMax evidence, or non-MiniMax generalization.

### Claim M8: FlowFence-Lite was clean across all six clean post-fix MiniMax smoke runs.

- Evidence artifact path: `artifacts/minimax_p1_smoke_postfix_audit/audit_summary.json`; `artifacts/minimax_p1_smoke_postfix_audit/audit_summary.md`
- Comparison target: `flowfence_lite` subset in the clean post-fix MiniMax 18-run smoke.
- Observation: the audit records FlowFence-Lite as clean across 6/6 runs, with `task_success_rate=1.0`, `unauthorized_raw_leakage_mean=0.0`, and `external_leakage_mean=0.0`.
- Confidence level: medium-low
- Caveat: this supports a small MiniMax smoke subset claim only; it is not broad real-model robustness evidence.

### Claim M9: the aggregate clean post-fix task-success gap is baseline-driven, not FlowFence-driven.

- Evidence artifact path: `artifacts/minimax_p1_smoke_postfix_audit/audit_summary.json`; `artifacts/minimax_p1_smoke_postfix_audit/audit_summary.md`; `artifacts/minimax_p1_smoke_postfix_audit/failure_breakdown.jsonl`
- Comparison target: `flowfence_lite`, `none`, and `prompt_filter` subsets in the clean post-fix MiniMax 18-run smoke.
- Observation: FlowFence-Lite has `task_success_rate=1.0`, `unauthorized_raw_leakage_mean=0.0`, and `external_leakage_mean=0.0`. No-defense has `task_success_rate=1.0`, `unauthorized_raw_leakage_mean=5.0`, and `external_leakage_mean=0.333333`. Prompt-filter has `task_success_rate=0.666667`, `unauthorized_raw_leakage_mean=7.333333`, and `external_leakage_mean=1.0`.
- Observation: the two prompt-filter task failures are `chain_4 / workspace_poisoning_indirect / prompt_filter / seed=1` and `blackboard_4 / workspace_poisoning_indirect / prompt_filter / seed=1`.
- Observation: both failures include non-zero raw and external leakage, so the audit classifies them as expected baseline failures rather than evaluator strictness or runtime bugs. No implementation code was changed in the audit.
- Confidence level: medium-low
- Caveat: the audit uses committed high-level summaries plus per-run metrics from the temporary post-fix run; raw traces and provider outputs remain uncommitted.

### Claim M10: prompt-filter remains vulnerable to indirect workspace poisoning in this MiniMax smoke.

- Evidence artifact path: `artifacts/minimax_p1_smoke_postfix_audit/audit_summary.json`; `artifacts/minimax_p1_smoke_postfix_audit/failure_breakdown.jsonl`
- Comparison target: `prompt_filter` under `workspace_poisoning_indirect` in the clean post-fix MiniMax 18-run smoke.
- Observation: the prompt-filter subset has `unauthorized_raw_leakage_mean=7.333333` and `external_leakage_mean=1.0`, with workspace-poisoning failures in both `chain_4` and `blackboard_4`.
- Confidence level: medium-low
- Caveat: this is small-smoke evidence only; it is not a comprehensive prompt-filter evaluation.

## 3E. MiniMax P1 MAS Coverage Evidence

This section supersedes the 18-run smoke and 84-run one-seed coverage as the current MiniMax coverage evidence, while preserving those earlier artifacts as historical smoke/debug context. It should be described as a MiniMax-backed multi-agent synthetic-runtime coverage experiment or MiniMax-only P1 MAS coverage over the synthetic deterministic runtime.

### Claim M11: the MiniMax-only 3-seed P1 MAS coverage completed 252/252 configured runs after retrying one transient timeout.

- Evidence artifact path: `artifacts/minimax_p1_coverage_3seed/run_manifest.json`; `artifacts/minimax_p1_coverage_3seed/coverage_summary.json`; `artifacts/minimax_p1_coverage_3seed_debug/retry_manifest.json`; `artifacts/codex_task_state/codex_p1_real_minimax_coverage_3seed_debug.md`
- Comparison target: configured MiniMax-only coverage matrix over `chain_4`, `star_4`, `blackboard_4`; attacks `none`, `summary_poisoning_direct`, `summary_poisoning_indirect`, `workspace_poisoning_direct`, `workspace_poisoning_indirect`, `comm_hijack_direct`, `comm_hijack_indirect`; defenses `none`, `static_acl`, `prompt_filter`, `flowfence_lite`; seeds `1`, `2`, `3`.
- Observation: the refreshed canonical artifacts record `expected_run_count=252`, `completed_run_count=252`, `failed_run_count=0`, `provider=minimax`, `provider_calls_enabled=true`, and `agent_backend=minimax_final_writer`.
- Observation: the original 3-seed run had 251/252 completed because of a MiniMax read timeout at `chain_4 / summary_poisoning_direct / prompt_filter / seed=1`. The debug/retry goal reran the same sweep without `--force`, skipped 251 completed `metrics.json` runs, executed only the missing run, and refreshed canonical artifacts to 252/252 completed.
- Confidence level: medium
- Caveat: this is MiniMax-only synthetic deterministic MAS runtime coverage. It is not non-MiniMax generalization, production safety, or real browser/desktop/computer-use agent evidence.

### Claim M12: the 252-run MiniMax coverage reports aggregate task, leakage, cascade, privilege, and topology metrics.

- Evidence artifact path: `artifacts/minimax_p1_coverage_3seed/coverage_summary.json`; `artifacts/minimax_p1_coverage_3seed/coverage_summary.md`
- Comparison target: aggregate 252-run MiniMax-only coverage matrix.
- Observation: aggregate `task_success_rate=0.964286`, `unauthorized_raw_leakage_mean=2.829365`, `external_leakage_mean=0.325397`, `cascade_size_mean=4.178571`, `privilege_reach_mean=2.678571`, and `topology_effect_observed=true`.
- Confidence level: medium
- Caveat: these are aggregate coverage metrics across defenses, attacks, topologies, and seeds in the synthetic runtime. They should not be presented as production safety or broad real-world robustness.

### Claim M13: FlowFence-Lite is clean across all configured FlowFence runs in the 252-run MiniMax coverage.

- Evidence artifact path: `artifacts/minimax_p1_coverage_3seed/coverage_summary.json`; `artifacts/minimax_p1_coverage_3seed/flowfence_clean_matrix.csv`; `artifacts/minimax_p1_coverage_3seed/flowfence_clean_matrix.md`
- Comparison target: `flowfence_lite` subset across 3 topologies, 7 attacks, and seeds `1`, `2`, `3`.
- Observation: FlowFence clean subset is 63/63 clean, with `task_success_rate=1.0`, `unauthorized_raw_leakage_mean=0.0`, and `external_leakage_mean=0.0`. Seed-level summaries record FlowFence task success 1.0 and raw/external leakage 0.0 for seeds `1`, `2`, and `3`.
- Confidence level: medium
- Caveat: this supports a configured MiniMax synthetic-runtime clean-subset claim, not a non-MiniMax or real-world deployment claim.

### Claim M14: FlowFence-Lite improves or ties simple baselines on raw/external leakage across configured comparison groups.

- Evidence artifact path: `artifacts/minimax_p1_coverage_3seed/coverage_summary.json`; `artifacts/minimax_p1_coverage_3seed/coverage_by_attack_defense.csv`; `artifacts/minimax_p1_coverage_3seed/coverage_by_defense.csv`
- Comparison target: `flowfence_lite` versus `none`, `static_acl`, and `prompt_filter` over topology x attack x seed comparison groups.
- Observation: versus no-defense, FlowFence improves raw leakage in 42 groups and ties in 21; improves external leakage in 32 and ties in 31; improves task success in 7 and ties in 56.
- Observation: versus static ACL, FlowFence improves raw leakage in 42 groups and ties in 21; improves external leakage in 30 and ties in 33; ties task success in all 63 groups.
- Observation: versus prompt-filter, FlowFence improves raw leakage in 18 groups and ties in 45; improves external leakage in 13 and ties in 50; improves task success in 2 and ties in 61.
- Confidence level: medium
- Caveat: this is a configured MiniMax synthetic-runtime comparison against simple baselines, not broad superiority over all defense families.

### Claim M15: the 252-run MiniMax coverage observes topology effects.

- Evidence artifact path: `artifacts/minimax_p1_coverage_3seed/coverage_summary.json`; `artifacts/minimax_p1_coverage_3seed/coverage_by_topology.csv`; `artifacts/minimax_p1_coverage_3seed/coverage_by_topology.md`
- Comparison target: `chain_4`, `star_4`, and `blackboard_4` within the MiniMax synthetic-runtime coverage.
- Observation: `topology_effect_observed=true` in the refreshed 252-run coverage summary.
- Confidence level: medium-low to medium
- Caveat: topology effects are observed in the MiniMax synthetic-runtime benchmark; they are not real-world agent deployment evidence.

### Claim M16: remaining 252-run failure categories are baseline and benchmark-risk signals, not FlowFence leaks.

- Evidence artifact path: `artifacts/minimax_p1_coverage_3seed/coverage_summary.json`; `artifacts/minimax_p1_coverage_3seed/failure_breakdown.jsonl`
- Comparison target: high-level failure categories in the refreshed 252-run coverage.
- Observation: committed summaries record `expected_no_defense_leakage=42`, `static_acl_policy_gap=42`, `prompt_filter_indirect_failure=18`, `task_success_failure_without_leakage=1`, and `unknown=32`.
- Confidence level: medium-low
- Caveat: failure categories are high-level audit labels; raw traces and provider outputs remain intentionally uncommitted.

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
- Full paper-ready MiniMax evidence beyond the configured MiniMax synthetic-runtime coverage.
- Utility preservation under broad real MiniMax final-writer execution.
- Broad multi-provider real-model robustness.
- Larger-than-252 MiniMax coverage unless later run.
- Production safety claim.
- Real browser/desktop/computer-use agent evidence.
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
- Do not describe the 252-run MiniMax coverage as a real-world agent deployment, real computer-use experiment, or production agent experiment.
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
| `artifacts/minimax_p1_smoke_postfix/run_manifest.json` | INSPECTED | clean post-fix MiniMax smoke manifest | Clean post-fix provider-call safety check and 2-run/18-run execution status. | No raw traces, prompts, provider outputs, or per-run metrics committed. |
| `artifacts/minimax_p1_smoke_postfix/summary_18run.json` | INSPECTED | clean post-fix MiniMax 18-run aggregate summary | Completed-run count, aggregate metrics, topology sanity, defense slices, and FlowFence comparisons. | Small one-seed MiniMax smoke only. |
| `artifacts/minimax_p1_smoke_postfix/summary_18run.md` | INSPECTED | clean post-fix MiniMax 18-run human-readable summary | Concise small-smoke metrics and defense slice interpretation. | Summary only; not a full real-model experiment. |
| `artifacts/minimax_p1_smoke_postfix_audit/audit_summary.json` | INSPECTED | post-fix MiniMax smoke audit summary | Explains aggregate task-success gap as baseline-driven and records FlowFence/no-defense/prompt-filter subgroup status. | Audit excludes raw traces, prompts, provider outputs, and event JSONL. |
| `artifacts/minimax_p1_smoke_postfix_audit/audit_summary.md` | INSPECTED | post-fix MiniMax smoke audit human-readable summary | FlowFence clean subset, prompt-filter failure groups, and baseline-driven interpretation. | Small-smoke audit only. |
| `artifacts/minimax_p1_smoke_postfix_audit/failure_breakdown.jsonl` | INSPECTED | post-fix MiniMax smoke failure breakdown | Exact prompt-filter workspace-poisoning failure groups and high-level leakage metrics. | No raw outputs or raw traces included. |
| `artifacts/minimax_p1_coverage/run_manifest.json` | INSPECTED | P1 MiniMax 84-run coverage manifest | One-seed broader MiniMax coverage execution status and provider metadata. | Superseded by 252-run 3-seed coverage for current MiniMax coverage claims. |
| `artifacts/minimax_p1_coverage/coverage_summary.json` | INSPECTED | P1 MiniMax 84-run coverage summary | Broader-than-smoke one-seed MiniMax synthetic-runtime coverage metrics. | One seed only; superseded by 252-run 3-seed coverage. |
| `artifacts/minimax_p1_coverage_3seed/run_manifest.json` | INSPECTED | P1 MiniMax 252-run coverage manifest | 252/252 completion, provider metadata, and retry-refreshed canonical status. | MiniMax-only synthetic-runtime evidence. |
| `artifacts/minimax_p1_coverage_3seed/coverage_summary.json` | INSPECTED | P1 MiniMax 252-run coverage summary | Aggregate metrics, FlowFence 63/63 clean subset, comparison counts, topology effect, and failure categories. | No raw traces or provider outputs; not non-MiniMax or production evidence. |
| `artifacts/minimax_p1_coverage_3seed/coverage_by_defense.csv` | INSPECTED | P1 MiniMax 252-run coverage defense table | Defense-level task success and leakage summaries. | Aggregate table only. |
| `artifacts/minimax_p1_coverage_3seed/coverage_by_topology.csv` | INSPECTED | P1 MiniMax 252-run coverage topology table | Topology-level coverage metrics. | Synthetic runtime topology evidence only. |
| `artifacts/minimax_p1_coverage_3seed/coverage_by_attack.csv` | INSPECTED | P1 MiniMax 252-run coverage attack table | Attack-level coverage metrics. | Aggregate table only. |
| `artifacts/minimax_p1_coverage_3seed/coverage_by_attack_defense.csv` | INSPECTED | P1 MiniMax 252-run coverage attack-defense table | Defense behavior by attack family. | Aggregate table only. |
| `artifacts/minimax_p1_coverage_3seed/coverage_by_seed.csv` | INSPECTED | P1 MiniMax 252-run coverage seed table | Seed-level stability and FlowFence clean metrics across seeds 1/2/3. | Three seeds only. |
| `artifacts/minimax_p1_coverage_3seed/flowfence_clean_matrix.csv` | INSPECTED | P1 MiniMax 252-run FlowFence clean matrix | Exact configured FlowFence groups and clean status. | FlowFence subset only. |
| `artifacts/minimax_p1_coverage_3seed/failure_breakdown.jsonl` | INSPECTED | P1 MiniMax 252-run failure breakdown | High-level failure categories without raw outputs. | Does not include raw traces or provider outputs. |
| `artifacts/minimax_p1_coverage_3seed_debug/retry_manifest.json` | INSPECTED | P1 MiniMax 252-run timeout retry manifest | Identifies the transient timeout run and records safe retry from 251/252 to 252/252. | Retry evidence only; no raw outputs. |

## 8. Current Method Boundaries

The P0 implementation is centered on retrieval-memory inspection.

P0 metrics observe retrieval-memory exposure and attack manifestation.

Current defense output includes risk score, reason codes, decision, rewritten content, lease signal, and poisoned-content exposure flags.

Current lease signal is not yet a full runtime lease mechanism.

P1 deterministic metrics now include event-graph cascade, topology, privilege-reach, and channel-level leakage evaluators in a synthetic runtime. This does not replace P0 retrieval-memory evidence and does not establish broad real-model generalization.

The current MiniMax evidence uses MiniMax only for final vendor-facing writing. Propagation, attack injection, defense decisions, and policy evaluation remain deterministic. The pre-debug smoke had very low task success (`0.055556`) and should be treated as historical context. The post-debug MiniMax debug smoke improved task success to `1.0` after minimal prompt/evaluator fixes, but it remains a small debug smoke rather than a full real-model experiment. The clean post-fix 18-run smoke remains useful as a small smoke artifact; its audit attributes the aggregate `task_success_rate=0.888889` gap to prompt-filter baseline failures, while the FlowFence subset is clean across all 6 runs.

The 84-run one-seed MiniMax coverage broadened the smoke, but it is now superseded for current MiniMax coverage claims by the 252-run 3-seed coverage. The 252-run MiniMax-backed multi-agent synthetic-runtime coverage completed 252/252 configured runs after retrying one transient MiniMax read timeout. It supports a stronger MiniMax-only synthetic-runtime claim that FlowFence-Lite is clean across all 63 configured FlowFence runs and improves or ties simple baselines on configured leakage comparisons. It still does not establish non-MiniMax generalization, production safety, real browser/desktop/computer-use agent evidence, or broad real-world robustness.

## 9. Next Evidence Required

1. Refresh paper-facing result tables from P0, deterministic P1, strengthened synthetic P1, MiniMax smoke, 84-run coverage, and 252-run coverage summaries.
2. Decide whether another real-model expansion is necessary after the 252-run tables are regenerated and reviewed.
3. Consider drafting the results section after refreshed tables and claims are reviewed.
4. Keep raw traces, raw provider outputs, event JSONL, policy JSONL, and per-run metrics uncommitted.
5. Keep non-MiniMax provider and real-world computer-use evidence explicitly out of scope unless a later contract change adds them.
6. Preserve the distinction between deterministic synthetic evidence, pre-debug MiniMax smoke evidence, post-debug debug-smoke evidence, clean post-fix MiniMax smoke evidence, 84-run MiniMax coverage, and 252-run MiniMax coverage.
7. Continue to avoid non-MiniMax generalization and production-safety claims.

## 10. Recommended Next PRs

1. codex/p1-paper-tables-refresh-2
2. codex/p1-paper-results-section-draft
3. codex/p1-evidence-package
