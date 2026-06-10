# Claims and Results Coverage Audit

This audit summarizes the current experiment results, maps paper-facing claims to supporting evidence, and records whether the AAAI draft includes each claim. It uses committed high-level artifacts only. It does not use raw traces, raw prompts, raw provider outputs, event JSONL, policy JSONL, or individual per-run metrics.

## Current Experiment Results

| Evidence layer | Current result | Evidence artifacts | Draft coverage |
|---|---|---|---|
| P0 adapted AgentPoison retrieval-memory comparator | No defense has exposed poisoned retrieval mean 0.4667 and attack manifestation mean 0.2533; FlowFence reduces exposed poisoned retrieval and manifestation to 0.0 while raw poisoned retrieval remains internal. | `results/baseline_agentpoison_fullreact_minimax27_small_matrix_summary.json`; Table 1 | Included in Results RQ1 and Table 1. |
| P0 weak/static comparator caveat | Static keyword filtering blocks the known-trigger same-axis attack, so FlowFence should be framed as structured containment rather than uniquely necessary for that trigger-string setting. | `results/baseline_agentpoison_fullreact_minimax27_static_keyword_filter_weak_comparator_summary.json`; Table 1 | Included in Results RQ1 and Table 1. |
| P0 held-out instruction stress | Under a held-out instruction stress test on the same retrieval anchor, the non-oracle static keyword filter has non-zero attack manifestation while FlowFence remains at 0.0. | `results/baseline_agentpoison_fullreact_minimax27_heldout_instruction_matrix_summary.json`; Table 1 | Added to Results RQ1 and Table 1 as a caveated blocklist-brittleness finding. |
| P0 overhead evidence | Same-axis measured and proxy overhead artifacts exist, but they support bounded runtime-feasibility/proxy claims rather than a headline speed claim. | `results/overhead_agentpoison_fullreact_minimax27_same_axis_measured_summary.json`; `results/overhead_agentpoison_fullreact_minimax27_same_axis_proxy_summary.json` | Mentioned as tracked but not headline in Results RQ1; not emphasized in main tables. |
| P1 deterministic synthetic MAS | Strengthened deterministic benchmark completed 252/252 and supports topology-dependent propagation plus FlowFence improvements over prompt-filter on indirect synthetic attacks. | `artifacts/codex_task_state/codex_p1_benchmark_strengthening.md`; Table 2 | Included in Results RQ2 and evidence-boundary table. |
| MiniMax 252-run coverage | MiniMax-backed multi-agent synthetic-runtime coverage completed 252/252 after retrying one transient timeout; aggregate task success 0.964286, raw leakage mean 2.829365, external leakage mean 0.325397, cascade mean 4.178571, privilege reach mean 2.678571, topology effect observed. | `artifacts/minimax_p1_coverage_3seed/coverage_summary.json`; Table 3 | Included in abstract, benchmark, Results RQ3/RQ4, Table 3, and evidence-boundary table. |
| FlowFence 63/63 clean subset | FlowFence subset is 63/63 clean, task success 1.0, raw leakage 0.0, external leakage 0.0, clean across seeds 1/2/3. | `artifacts/minimax_p1_coverage_3seed/flowfence_clean_matrix.csv`; Table 3; Table 6 | Included in abstract, introduction, Results RQ3/RQ4, Table 3, and Table 6. |
| FlowFence vs baselines in 252-run coverage | FlowFence improves or ties no defense, static ACL, and prompt filter on configured raw/external leakage comparisons with no underperformance in recorded comparison groups. | `artifacts/minimax_p1_coverage_3seed/coverage_summary.json`; Table 3 | Included in Results RQ3/RQ5 and Table 3. |
| Non-oracle deterministic held-out validation | `flowfence_lite_nonoracle` completes 540/540 deterministic runs with task success 1.0, raw leakage 0.0, external leakage 0.0, and zero oracle-annotation violations. | `artifacts/nonoracle_heldout_deterministic/summary.json`; Table 7 | Included in abstract, introduction, Results RQ6, and Table 7. |
| Targeted MiniMax non-oracle validation | Targeted MiniMax-backed synthetic-runtime validation completes 72/72 runs with task success 1.0, raw leakage 0.0, external leakage 0.0, and zero oracle-annotation violations. | `artifacts/minimax_nonoracle_heldout_targeted/summary.json`; Table 7 | Included in abstract, introduction, Results RQ6, and Table 7. |
| No-semantic-pattern ablation | No-semantic-pattern ablation has higher deterministic raw leakage than full non-oracle FlowFence while tying external leakage and task success, suggesting semantic patterns contribute to raw-leakage containment but are not the only mechanism. | `artifacts/nonoracle_heldout_deterministic/ablation_summary.csv`; Table 8 | Included in Results RQ7 and Table 7/8-derived text. |
| Redacted safe-trace case studies | Case 1/3 illustrate no-defense blackboard propagation versus FlowFence quarantine/safe-view containment; Case 4 illustrates non-oracle containment; Case 2 illustrates prompt-filter paraphrase weakness. | `artifacts/case_studies_safe_trace/*`; Table case studies | Included in Analysis and Table case studies. |

## Claim Support Map

| Claim | Supported status | Evidence | AAAI draft status |
|---|---|---|---|
| Privacy leakage in multi-agent systems should be evaluated as event-level propagation, not only final output leakage. | Supported for the synthetic runtime and adapted comparator framing. | Problem definition, deterministic MAS evidence, MiniMax topology/cascade metrics. | Included in abstract, Introduction, Problem, Method, Results, and Conclusion. |
| FlowFence-Lite provides runtime containment through safe views, quarantine, policy, fanout, and privilege signals. | Supported as a method description and by configured experiments. | Method implementation snapshots, Tables 1/3/7/8. | Included in Method, Results, and Analysis. |
| P0 adapted AgentPoison evidence supports retrieval-memory containment. | Supported with caveat. | Table 1, P0 summaries. | Included in Results RQ1. |
| P0 is not official AgentPoison reproduction. | Supported as limitation. | Claims checklist and evidence index. | Included in Results RQ1 and Limitations. |
| Static keyword filtering is strong on known-trigger P0 but brittle under the held-out stress setting. | Supported as caveated P0 interpretation. | P0 static keyword and held-out instruction summaries. | Added to Results RQ1 and Table 1. |
| Deterministic synthetic MAS supports topology-dependent propagation and FlowFence-vs-prompt-filter improvements on indirect attacks. | Supported for deterministic synthetic runtime. | Table 2 and benchmark-strengthening task state. | Included in Results RQ2 and evidence-boundary table. |
| MiniMax 252-run coverage completed 252/252 and is the canonical provider-backed coverage result. | Supported. | Table 3, coverage summary, retry manifest. | Included in abstract, benchmark, Results RQ3, and Table 3. |
| FlowFence is clean across 63/63 configured FlowFence runs in MiniMax 252-run coverage. | Supported. | Table 3, Table 6, clean matrix. | Included in abstract, Introduction, Results RQ3/RQ4, Table 3, and Table 6. |
| FlowFence improves or ties no defense, static ACL, and prompt filter on configured raw/external leakage comparisons. | Supported for configured comparison groups. | Table 3 and coverage summary. | Included in Results RQ3/RQ5. |
| Topology effects are observed in the MiniMax-backed synthetic-runtime benchmark. | Supported with caveat. | Table 3, Table 6, coverage by topology. | Included in Results RQ4 and Analysis. |
| Default FlowFence had an oracle-annotation internal-validity risk. | Supported as addressed limitation. | Non-oracle task state, code snapshots, Table 8. | Included in Introduction, Method, Results RQ6, Analysis, and traceability. |
| Non-oracle FlowFence ignores oracle labels and remains clean on configured held-out matrices. | Supported for deterministic and targeted MiniMax validations. | Table 7, non-oracle summaries. | Included in abstract, Introduction, Results RQ6, and Table 7. |
| No-semantic-pattern ablation suggests semantic patterns contribute to raw-leakage containment. | Partially supported. | Table 8, ablation summary. | Included in Results RQ7 and Analysis. |
| Redacted safe traces illustrate representative event paths. | Supported as qualitative illustration only. | Safe-trace case-study artifacts. | Included in Analysis and Table case studies. |
| Non-MiniMax generalization, production safety, real browser/desktop deployment, arbitrary attack robustness, official AgentPoison reproduction, and learned graph-risk scoring are unsupported. | Unsupported claims are explicitly excluded. | Claims checklist, evidence boundaries, limitations. | Included in abstract limitations sentence, Introduction scope paragraph, Limitations, and evidence-boundary table. |

## Coverage Gaps and Decisions

- The AAAI main draft now includes the main supported claims and core experimental results.
- P0 overhead evidence is intentionally not a headline table because the paper's main claim is containment, not latency or cost. It remains traceable in the claims checklist.
- Historical 18-run smoke and 84-run coverage are not headline AAAI results because they are superseded by the 252-run MiniMax coverage.
- The evidence-boundary table is now included in the Limitations section so unsupported claims are visible in the paper body.
- The draft still needs a LaTeX-capable layout pass to verify page count, bibliography, references, and table overfull warnings.
