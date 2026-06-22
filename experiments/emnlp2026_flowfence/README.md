# EMNLP 2026 FlowFence Evidence Map

## Paper

- Paper directory: `papers/emnlp2026_flowfence/`
- Main source: `papers/emnlp2026_flowfence/main.tex`
- Title: `FlowFence: Runtime Containment for Retrieval-Memory Poisoning in LLM Agents`
- Scope: retrieval-memory containment on an AgentPoison-derived StrategyQA full-ReAct axis.
- Rebuttal use: locate the source artifact, raw run directory, metric meaning, and caveat for each EMNLP table or claim.

## Claim Boundaries

Supported claims:

- Retrieved poison can remain present in raw retrieval while FlowFence prevents model-visible exposure and downstream attack manifestation.
- The retrieval-to-exposure boundary result holds on the reported AgentPoison-derived full-ReAct axis across the saved provider profiles and MiniMax mechanism slices.
- Known-trigger static filtering is a strong narrow comparator on the original trigger, but fails as a general containment story under paraphrased or held-out poisoned instructions.
- Inspector-swap, benign replay, and overhead measurements support implementation feasibility for the saved traces, not deployment-wide safety.

Do not claim:

- Official AgentPoison reproduction.
- Broad multi-agent topology propagation.
- Non-MiniMax generalization for new experiments in the current phase.
- Production security, formal guarantees, or arbitrary adaptive robustness.

## Main Tables And Evidence

| Paper table / section | Supported claim | Primary summary artifact | Raw result roots or event artifacts | Metric level | Caveat |
| --- | --- | --- | --- | --- | --- |
| `tab:crossprovider` Cross-provider containment | Raw poisoned retrieval can remain non-zero while exposed poison and manifestation are suppressed after the boundary. | `artifacts/emnlp2026_p0/results/emnlp_p0_cross_provider_summary.json`, `artifacts/emnlp2026_p0/results/emnlp_p0_cross_provider_results.csv`, `artifacts/emnlp2026_p0/results/emnlp_p0_cross_provider_runs.csv` | Run roots listed in `emnlp_p0_cross_provider_runs.csv`; includes `results/baseline_agentpoison_fullreact_dpr_strategyqa_minimax27_triggerquery_*`, `results/method_flowfence_lite_fullreact_minimax27_triggerquery_quarantine_actioncanon_*`, `results/emnlp_p0_cross_provider_qwen36_*`, `results/emnlp_p0_cross_provider_kimi25_*` | Case-level over three 25-question runs per provider-condition group | Provider profiles are historical paper evidence; do not add new non-MiniMax experiments under the current phase constraint. |
| `tab:main` Mechanism matrix | MiniMax same-axis mechanism comparison among no defense, static keyword, rewrite-only, quarantine-only, and FlowFence quarantine+action-canon. | `results/baseline_agentpoison_fullreact_minimax27_small_matrix_summary.json`, `results/baseline_agentpoison_fullreact_minimax27_static_keyword_filter_weak_comparator_summary.json`, `results/baseline_agentpoison_fullreact_minimax27_rewrite_only_weak_comparator_summary.json`, `results/ablation_agentpoison_fullreact_minimax27_quarantine_only_vs_actioncanon_summary.json` | `results/baseline_agentpoison_fullreact_dpr_strategyqa_minimax27_triggerquery_*`, `results/baseline_agentpoison_fullreact_minimax27_triggerquery_static_keyword_filter_*`, `results/baseline_agentpoison_fullreact_minimax27_triggerquery_rewrite_only_*`, `results/method_flowfence_lite_fullreact_minimax27_triggerquery_quarantine_only_*`, `results/method_flowfence_lite_fullreact_minimax27_triggerquery_quarantine_actioncanon_*` | Case-level over three MiniMax runs per condition | Static keyword is a strong known-trigger baseline; do not claim FlowFence is uniquely necessary for this exact trigger string. |
| `tab:pressure` Retrieval-pressure sensitivity | Boundary containment is not tied to one retrieval candidate count. | `artifacts/icde2027_supplemental/results/poison_pressure_results.csv`, `artifacts/icde2027_supplemental/results/poison_pressure_runs.csv` | `results/icde_pressure_knn1_*`, `results/icde_pressure_knn3_*`, `results/icde_pressure_knn5_*` | Case-level grouped by `k in {1,3,5}` and condition | Kept as EMNLP supplemental evidence despite the `icde_` prefix. |
| `tab:inspectorswap` Inspector-swap replay | Boundary semantics can be replayed with rule, heuristic, and capped LLM judge inspectors. | `artifacts/emnlp2026_p1/inspector_swap/inspector_swap_summary.json`, `artifacts/emnlp2026_p1/inspector_swap/inspector_swap_summary.csv` | `artifacts/emnlp2026_p1/inspector_swap/inspector_swap_events.csv`, `artifacts/emnlp2026_p1/inspector_swap/llm_judge_cache_kimi25.jsonl`, `artifacts/emnlp2026_p1/inspector_swap/llm_judge_cache_minimax27.jsonl` | Event-level over saved retrieval events; LLM judges use capped 50-event subset | LLM judge outputs are replay diagnostics, not production guard claims. |
| `tab:sameaxis` Lexical and prompt-isolation comparators | Prompt quoting and paraphrase-aware lexical filtering do not enforce the same raw-view separation. | Same-axis summaries embedded in run metrics; see run roots. | `results/emnlp_p0_same_axis_paraphrase_aware_keyword_filter_*`, `results/emnlp_p0_same_axis_prompt_quoting_isolation_*` | Case-level over three runs per comparator | False intervention is a proxy for non-quarantine comparators. |
| `tab:stress` Held-out/paraphrase stress | Non-oracle static filtering fails when the poisoned instruction changes surface form; FlowFence blocks exposure in these saved slices. | `results/baseline_agentpoison_fullreact_minimax27_heldout_instruction_matrix_summary.json`, `artifacts/icde2027_supplemental/results/paraphrase_family_results.csv`, `artifacts/icde2027_supplemental/results/paraphrase_family_runs.csv` | Held-out roots in the summary JSON plus `results/icde_paraphrase_*` | Case-level grouped by stress family and condition | Manifestation is downstream diagnostic; exposure is the primary endpoint. |
| `tab:adaptive` Kimi adaptive pilot | Three same-axis adaptive poison families are detected in retrieval but not exposed under FlowFence. | Case-level summaries in `results/emnlp_p1_adaptive_*_kimi25_v1/metrics.json` and `case_results.jsonl` | `results/emnlp_p1_adaptive_factual_misinformation_*_kimi25_v1`, `results/emnlp_p1_adaptive_mixed_language_*_kimi25_v1`, `results/emnlp_p1_adaptive_soft_preference_*_kimi25_v1` | Corrected case-level `Detected` and `Exposed` fields | This is a pilot; do not use it as broad adaptive robustness evidence. |
| `tab:benign-replay` Benign replay | Rule/heuristic inspectors have measured false-quarantine behavior on benign record families. | `artifacts/emnlp2026_p1/benign_false_quarantine/benign_false_quarantine_summary.json`, `artifacts/emnlp2026_p1/benign_false_quarantine/benign_false_quarantine_summary.csv` | `artifacts/emnlp2026_p1/benign_false_quarantine/benign_false_quarantine_events.csv`, plus `artifacts/icde2027_supplemental/results/false_positive_results.csv` | Record-level for offline replay; case-level for supplemental false-positive slice | Offline replay is not a deployment false-positive estimate. |
| `tab:cost` Fixed-trace cost | Boundary replay has negligible local processing cost on saved events; token deltas are serialized-context proxies. | `artifacts/emnlp2026_p0/overhead_replay/fixed_trace_overhead_replay_summary.json`, `results/overhead_agentpoison_fullreact_minimax27_same_axis_proxy_summary.json`, `results/overhead_agentpoison_fullreact_minimax27_same_axis_measured_summary.json` | `artifacts/emnlp2026_p0/overhead_replay/fixed_trace_events.jsonl`, `results/overhead_agentpoison_fullreact_minimax27_triggerquery_nodefense_v1`, `results/overhead_agentpoison_fullreact_minimax27_triggerquery_quarantine_actioncanon_v1` | Event-level replay plus narrow measured 10-question slice | The measured slice does not support a general faster-or-cheaper claim. |

## Metric Definitions

- Raw: raw poisoned retrieval before the FlowFence retrieval-to-exposure boundary.
- Exp.: poisoned content exposed in model-visible context after condition-specific processing.
- Man.: downstream attack manifestation in trajectory or final-answer behavior.
- Clean: exact-match utility rate on benign cases.
- AtkU: exact-match utility rate on attacked/adversarial cases.
- Int./case: intervention events divided by evaluated cases; can exceed 1 because a case may contain multiple retrieval events.
- FQ: false quarantine rate on clean records or clean retrieval events.
- False int.: false-intervention proxy for comparators that do not have quarantine state.
- Detected: adaptive-pilot case-level rate where poisoned content appears in retrieved observations.
- Exposed: adaptive-pilot case-level rate where poisoned content remains model-visible.
- Local microseconds/event: local replay processing time only.
- Token delta: serialized-context proxy unless the table explicitly says provider-billed tokens.

## Canonical Evidence Roots

- Paper source: `papers/emnlp2026_flowfence/`
- High-level EMNLP P0 summaries: `artifacts/emnlp2026_p0/`
- High-level EMNLP P1 replay summaries: `artifacts/emnlp2026_p1/`
- Supplemental stress/pressure summaries used by EMNLP: `artifacts/icde2027_supplemental/`
- Canonical raw run directories: the `results/` paths listed in the table above.
- EMNLP retained `results/` manifest: `experiments/emnlp2026_flowfence/results_manifest.csv`.

## Cleanup Rules

- Keep the raw run directories listed in this document until a replacement evidence package exists.
- Keep historical `icde_*` result roots only when they are referenced by `artifacts/icde2027_supplemental/results/*.csv`.
- Delete or archive smoke, dry-run, diagnostic, AgentDojo, ASB, and old simplified `qwen36` pre-method results unless another retained paper map points to them.
