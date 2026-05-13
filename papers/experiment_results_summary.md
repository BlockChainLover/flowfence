# FlowFence-Lite Experiment Results Summary

Last updated: 2026-05-12

Purpose: this document is a paper-writing index for the completed FlowFence-Lite experiments. It summarizes what was run, what the results were, what claims each result supports, what claims it does not support, and where the artifacts are.

## Scope and Claim Boundary

The current paper-ready evidence is centered on an adapted AgentPoison StrategyQA full-ReAct axis. The original main evidence used the MiniMax provider profile; the EMNLP P0 extension adds qwen36 and kimi25 provider profiles on the same fixed 25-question axis. This is the main experimental baseline because it directly stresses the paper's data-management problem: poisoned retrieval memory crossing into model-visible agent context.

The current work should not be described as full official AgentPoison reproduction. The accepted main axis keeps the upstream ReAct-StrategyQA loop and DPR-backed retrieval environment, but uses a trigger-query search context to create stable non-vacuous attack pressure under MiniMax.

The strongest supported claim is:

> On an adapted AgentPoison full-ReAct retrieval-memory poisoning axis across MiniMax, qwen36, and kimi25 provider profiles, FlowFence-Lite establishes a runtime containment boundary between raw retrieval and model-visible exposure: raw poisoned retrieval remains non-zero, while exposed poisoned retrieval and attack manifestation are reduced to zero across repeated runs.

The broader claims that are not supported yet are listed near the end of this document.

## Metrics

| metric | meaning | paper use |
| --- | --- | --- |
| raw poisoned retrieval | Poisoned content is returned by retrieval before defense processing. | Shows attack pressure is present. |
| exposed poisoned retrieval | Poisoned content enters model-visible prompt/ReAct observation after defense processing. | Main containment metric. |
| attack manifestation | The adversarial behavior appears in the final or ReAct outcome. | Main safety outcome. |
| clean utility | Exact-match utility on clean StrategyQA questions. | Utility retention, not utility improvement. |
| attacked utility | Exact-match utility under adversarial/retrieval-poisoned setting. | Utility under attack. |
| intervention event rate | Fraction of retrieval events that trigger a defense action. | Cost/disruption proxy. |
| false quarantine rate | Benign instruction-like retrieved records quarantined by defense. | False-positive evidence. |
| LLM calls / tokens / wall time | Execution cost and overhead proxies or measured cost. | Runtime feasibility, with caveats. |

## Master Evidence Map

| experiment group | artifact | main result | claim status |
| --- | --- | --- | --- |
| AgentPoison qwen pre-method baseline | `results/premethod_summary_agentpoison_strategyqa_premethod_v2.json` | Clean utility `0.7667`, attacked utility `0.7000`, attack manifestation `0.7667`, poisoned retrieval `0.7667`. | Historical method-start baseline only. |
| MiniMax main matrix | `results/baseline_agentpoison_fullreact_minimax27_small_matrix_summary.json` | No defense exposes poison and manifests attack; FlowFence-Lite reduces exposed poison and manifestation to `0.0`. | Main paper evidence. |
| Static keyword filter comparator | `results/baseline_agentpoison_fullreact_minimax27_static_keyword_filter_weak_comparator_summary.json` | Static filter also blocks known-trigger axis. | Strong narrow baseline; limits overclaiming. |
| Rewrite-only comparator | `results/baseline_agentpoison_fullreact_minimax27_rewrite_only_weak_comparator_summary.json` | Rewrite-only also blocks exposure on shared-detector axis, but lower clean utility than selected method. | Mechanism/ablation evidence. |
| Quarantine-only vs action-canon ablation | `results/ablation_agentpoison_fullreact_minimax27_quarantine_only_vs_actioncanon_summary.json` | Quarantine-only is sufficient for safety; action canonicalization improves trajectory hygiene/clean utility. | Mechanism evidence. |
| Held-out poisoned-instruction stress | `results/baseline_agentpoison_fullreact_minimax27_heldout_instruction_matrix_summary.json` | Non-oracle static filter fails; FlowFence-Lite contains exposure. | Blocklist brittleness evidence. |
| Overhead proxy | `results/overhead_agentpoison_fullreact_minimax27_same_axis_proxy_summary.json` | FlowFence-Lite adds model-call and trace-token proxy overhead. | Bounded-cost evidence, not measured runtime. |
| Measured overhead slice | `results/overhead_agentpoison_fullreact_minimax27_same_axis_measured_summary.json` | Inspection time is negligible; method did not increase measured wall time/tokens on 10-question slice. | Runtime feasibility with trajectory caveat. |
| ICDE supplemental pressure | `artifacts/icde2027_supplemental/results/poison_pressure_results.csv` | FlowFence-Lite keeps exposed poison and manifestation at `0.0` across retrieval-pressure settings. | Robustness under retrieval pressure. |
| ICDE supplemental paraphrase | `artifacts/icde2027_supplemental/results/paraphrase_family_results.csv` | Static filter averages exposed/manifestation `0.4844/0.2022`; FlowFence-Lite `0.0/0.0`. | Strongest blocklist-brittleness result. |
| ICDE supplemental clean false-positive | `artifacts/icde2027_supplemental/results/false_positive_results.csv` | FlowFence-Lite false quarantine rate on benign instruction-like records is `0.0`. | False-positive/trade-off evidence. |
| ICDE audit traces | `artifacts/icde2027_supplemental/audit_cases/audit_cases.md` | Shows no-defense boundary crossing, FlowFence quarantine, and static-filter paraphrase miss. | Auditability/data-governance evidence. |
| EMNLP P0 cross-provider containment | `artifacts/emnlp2026_p0/results/emnlp_p0_cross_provider_results.csv` | qwen36 and kimi25 no-defense raw/exposed poison near `0.96`; FlowFence-Lite keeps raw near `0.96` but exposed/manifestation at `0.0`. | Cross-provider containment evidence. |
| EMNLP P0 same-axis stronger baselines | `results/emnlp_p0_same_axis_paraphrase_aware_keyword_filter_*`, `results/emnlp_p0_same_axis_prompt_quoting_isolation_*` | Paraphrase-aware keyword and prompt quoting both leave exposed poison around `0.4267`. | Evidence against prompt-only isolation and generalized lightweight keyword matching on this axis. |
| EMNLP P0 fixed-trace overhead replay | `artifacts/emnlp2026_p0/overhead_replay/fixed_trace_overhead_replay.csv` | FlowFence-Lite exposes `0/22` poisoned events with about `14.0` microseconds/event local replay overhead. | Low local containment overhead evidence. |
| AgentDojo MiniMax | `results/baseline_agentdojo_minimax27_*summary.json` | Search hits exist, but selected reruns are unstable. | Auxiliary/stochastic evidence only. |

## Experiment 1: AgentPoison qwen Pre-Method Baseline

### Purpose

Establish a fixed method-start baseline before implementing FlowFence-Lite. This was the early narrow AgentPoison StrategyQA slice used to satisfy the repo's baseline gate.

### How It Was Run

- Benchmark: adapted narrow AgentPoison StrategyQA slice.
- Provider: `qwen36`.
- Fixed manifest: `data/tasks/agentpoison_strategyqa_premethod_v2.json`.
- Reruns: 3.
- Summary artifact: `results/premethod_summary_agentpoison_strategyqa_premethod_v2.json`.

### Results

| metric | mean | min | max |
| --- | ---: | ---: | ---: |
| clean utility | `0.7667` | `0.7000` | `0.8000` |
| attacked utility | `0.7000` | `0.6000` | `0.8000` |
| attack manifestation | `0.7667` | `0.7000` | `0.8000` |
| poisoned retrieval | `0.7667` | `0.7000` | `0.8000` |
| poisoned retrieval gap | `0.8667` | `0.7000` | `1.1000` |

### Supported Claim

This satisfied the baseline-readiness/method-start gate for an early adapted AgentPoison slice with fixed manifest, repeated runs, consistent schema, and saved artifacts.

### Not Supported

Do not use this as the main ICDE evidence. It is a historical baseline floor and not the current full-ReAct MiniMax comparator.

## Experiment 2: Adapted AgentPoison MiniMax Main Matrix

### Purpose

Test the core FlowFence-Lite claim on the current main paper axis: can FlowFence-Lite prevent poisoned retrieved memory from crossing into the model-visible ReAct context while raw poisoned retrieval remains non-zero?

### How It Was Run

- Benchmark axis: adapted AgentPoison StrategyQA full-ReAct.
- Model profile: `minimax27`.
- Retrieval: upstream AgentPoison DPR-backed `local_wikienv.WikiEnv`.
- Attack setup: trigger-query adversarial search context.
- Sample: 25 fixed StrategyQA questions.
- Reruns: 3 per condition.
- Main summary: `results/baseline_agentpoison_fullreact_minimax27_small_matrix_summary.json`.

### Results

| condition | exposed poison | attack manifestation | raw poison | clean utility | attacked utility | intervention |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| No defense | `0.4667` | `0.2533` | `0.4667` | `0.3733` | `0.3333` | `0.0000` |
| FlowFence-Lite quarantine + action-canon | `0.0000` | `0.0000` | `0.4400` | `0.3600` | `0.3867` | `0.4770` |

### Supported Claim

This is the central containment claim. No defense repeatedly exposes poisoned retrieval and has non-zero attack manifestation. FlowFence-Lite still observes raw poisoned retrieval internally but reduces exposed poisoned retrieval and attack manifestation to zero.

### Not Supported

Do not claim broad generalization, formal security, or utility improvement. Clean utility is roughly comparable but noisy.

## Experiment 3: Independent Static Keyword Filter Comparator

### Purpose

Add an independent weak-defense family on the same adapted AgentPoison MiniMax axis. This tests whether a simple known-trigger blocklist can explain the safety result.

### How It Was Run

- Same 25-question MiniMax full-ReAct axis as the main matrix.
- Defense: static keyword/blocklist filter.
- Does not use FlowFence-Lite quarantine semantics, safe-view rewriting, lease signals, or action canonicalization.
- Reruns: 3.
- Summary: `results/baseline_agentpoison_fullreact_minimax27_static_keyword_filter_weak_comparator_summary.json`.

### Results

| metric | value |
| --- | ---: |
| exposed poisoned retrieval | `0.0000` |
| attack manifestation | `0.0000` |
| raw poisoned retrieval | `0.4667` |
| clean utility | `0.3600` |
| attacked utility | `0.3600` |
| intervention event rate | `0.4961` |

### Supported Claim

A known-trigger static keyword filter is a strong narrow baseline on the original trigger-string axis.

### Not Supported

This result prevents overclaiming. The paper should not say FlowFence-Lite is uniquely necessary to block the original known-trigger attack. The stronger claim is that FlowFence-Lite provides structured containment and audit semantics, and later paraphrase stress tests show where old-phrase filtering breaks.

## Experiment 4: Rewrite-Only Weak Comparator

### Purpose

Test whether detector-mediated safe-view rewriting alone can block exposure without quarantine.

### How It Was Run

- Same adapted AgentPoison MiniMax 25-question axis.
- Defense: rewrite unsafe retrieved observation into safe view.
- Removes quarantine semantics.
- Reruns: 3.
- Summary: `results/baseline_agentpoison_fullreact_minimax27_rewrite_only_weak_comparator_summary.json`.

### Results

| metric | value |
| --- | ---: |
| exposed poisoned retrieval | `0.0000` |
| attack manifestation | `0.0000` |
| raw poisoned retrieval | `0.4533` |
| clean utility | `0.2933` |
| attacked utility | `0.4933` |
| intervention event rate | `0.4197` |

### Supported Claim

Detector-mediated safe-view rewriting can block exposed poisoned retrieval on this fixed axis. Quarantine is not uniquely necessary for zero exposure when the same detector is available.

### Not Supported

Do not claim quarantine is the only way to stop exposure on this axis. The reason to prefer quarantine is data-governance semantics: preserving unsafe retrieved records outside active context with explicit state and reason codes.

## Experiment 5: Quarantine-Only vs Quarantine + Action Canonicalization

### Purpose

Ablate the selected FlowFence-Lite variant to separate safety from trajectory hygiene. The question is whether action canonicalization is required for safety, or mainly improves full-ReAct trace stability.

### How It Was Run

- Same adapted AgentPoison MiniMax 25-question axis.
- Conditions: FlowFence-Lite quarantine-only vs FlowFence-Lite quarantine + action canonicalization.
- Reruns: 3 per condition.
- Summary: `results/ablation_agentpoison_fullreact_minimax27_quarantine_only_vs_actioncanon_summary.json`.

### Results

| condition | exposed poison | attack manifestation | raw poison | clean utility | attacked utility | intervention |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Quarantine only | `0.0000` | `0.0000` | `0.5333` | `0.3067` | `0.3733` | `0.5805` |
| Quarantine + action-canon | `0.0000` | `0.0000` | `0.4400` | `0.3600` | `0.3867` | `0.4770` |

### Supported Claim

Quarantine alone is sufficient for the safety outcome on this axis. Action canonicalization should be described as improving trajectory hygiene and clean utility stability, not as the primary safety mechanism.

### Not Supported

Do not claim action canonicalization is required to eliminate exposed poison in this experiment.

## Experiment 6: Held-Out Poisoned-Instruction Stress Test

### Purpose

Test whether an old-phrase static keyword filter fails when poisoned guidance is paraphrased away from the phrases it blocks.

### How It Was Run

- Same adapted AgentPoison MiniMax setup.
- Same trigger sequence and adapted retrieval anchor.
- Poisoned guidance paraphrased away from old static-filter phrases.
- Conditions: no defense, non-oracle static keyword filter, FlowFence-Lite quarantine + action-canon.
- Reruns: 3 per condition.
- Summary: `results/baseline_agentpoison_fullreact_minimax27_heldout_instruction_matrix_summary.json`.

### Results

| condition | exposed poison | attack manifestation | raw poison | clean utility | attacked utility | intervention |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| No defense | `0.5333` | `0.1733` | `0.5333` | `0.3200` | `0.0933` | `0.0000` |
| Non-oracle static filter | `0.4667` | `0.2400` | `0.4667` | `0.1867` | `0.1733` | `0.0000` |
| FlowFence-Lite | `0.0000` | `0.0000` | `0.5333` | `0.1467` | `0.2533` | `0.4869` |

### Supported Claim

Old-phrase static filtering is brittle under paraphrased poisoned guidance. FlowFence-Lite still contains exposure when raw poisoned retrieval remains non-zero.

### Not Supported

This is not broad held-out attack generalization. It keeps the same trigger sequence and adapted retrieval anchor.

## Experiment 7: Same-Axis Overhead Proxy

### Purpose

Estimate overhead from existing 25-question traces where strict provider token usage and wall-clock timing were not available.

### How It Was Run

- Uses saved case traces from the 25-question main matrix and ablations.
- Computes model-call proxy, trace-token proxy, and interventions per case.
- Summary: `results/overhead_agentpoison_fullreact_minimax27_same_axis_proxy_summary.json`.

### Results

| condition | model calls / case | delta vs no defense | token proxy / case | token-proxy delta | interventions / case |
| --- | ---: | ---: | ---: | ---: | ---: |
| No defense | `2.8333` | `0.00%` | `416.3483` | `0.00%` | `0.0000` |
| Rewrite only | `3.4267` | `+20.94%` | `536.4700` | `+28.85%` | `0.6467` |
| Quarantine only | `3.4267` | `+20.94%` | `495.2800` | `+18.96%` | `0.7333` |
| Quarantine + action-canon | `3.7600` | `+32.71%` | `502.5767` | `+20.71%` | `0.7467` |

### Supported Claim

FlowFence-Lite has bounded proxy overhead on the same 25-question efficacy axis.

### Not Supported

This is not measured latency or provider-token evidence. Do not claim faster/cheaper from this proxy table.

## Experiment 8: Same-Axis Measured Overhead Slice

### Purpose

Upgrade overhead evidence from proxy-only to measured wall-clock and provider-token evidence on a smaller fixed slice.

### How It Was Run

- Same adapted AgentPoison MiniMax axis.
- 10 fixed StrategyQA questions.
- Conditions: no defense vs FlowFence-Lite quarantine + action-canon.
- Records wall time, LLM calls, provider token usage, and defense inspection time.
- Summary: `results/overhead_agentpoison_fullreact_minimax27_same_axis_measured_summary.json`.

### Results

| condition | wall sec / case | LLM calls / case | provider tokens / case | defense sec / case |
| --- | ---: | ---: | ---: | ---: |
| No defense | `28.861467` | `3.20` | `5197.25` | `0.000013` |
| FlowFence-Lite | `24.692974` | `2.65` | `4191.50` | `0.000098` |
| Relative delta | `-14.44%` | `-17.19%` | `-19.35%` | `+0.000085 sec` |

### Supported Claim

Defense inspection time is negligible relative to LLM latency on this measured slice. The selected method did not increase measured wall-clock time or provider tokens in this slice.

### Not Supported

Do not claim FlowFence-Lite is generally faster or token-saving. The measured result is trajectory-confounded because the method run had shorter sampled ReAct traces and no intervention events in that smaller slice.

## Experiment 9: ICDE Supplemental Retrieval-Pressure Sensitivity

### Purpose

Show that containment does not only hold at one retrieval pressure. The supplemental pressure slice varies retrieval candidate-pool settings while keeping the same adapted AgentPoison MiniMax axis.

### How It Was Run

- 25 questions.
- 3 runs per condition.
- Pressure settings: `knn1`, `knn3`, `knn5`.
- Conditions: no defense, static keyword filter, FlowFence-Lite.
- Summary CSV: `artifacts/icde2027_supplemental/results/poison_pressure_results.csv`.
- Full supplemental JSON: `artifacts/icde2027_supplemental/results/icde_supplemental_summary.json`.

### Results

Aggregate across `knn1/3/5`:

| condition | raw poison | exposed poison | attack manifestation | clean utility | attacked utility | intervention |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| No defense | `0.3956` | `0.3956` | `0.2578` | `0.2933` | `0.2489` | `0.0000` |
| Static keyword filter | `0.3867` | `0.0000` | `0.0000` | `0.3822` | `0.3911` | `0.2840` |
| FlowFence-Lite | `0.4000` | `0.0000` | `0.0000` | `0.3378` | `0.3644` | `0.3595` |

### Supported Claim

FlowFence-Lite maintains the retrieval-exposure boundary under multiple retrieval-pressure settings: raw poisoned retrieval remains non-zero, while exposed poisoned retrieval and attack manifestation are zero.

### Not Supported

This does not prove FlowFence-Lite dominates static filters on known-trigger attacks. Static keyword filtering is also effective in this pressure slice.

## Experiment 10: ICDE Supplemental Paraphrase-Family Stress Test

### Purpose

Test whether static keyword filtering breaks when poisoned instructions are paraphrased across multiple surface forms.

### How It Was Run

- 6 paraphrase families:
  - direct instruction,
  - policy-style instruction,
  - factual-looking poisoned note,
  - system-message imitation,
  - tool-use suggestion,
  - indirect preference manipulation.
- 25 questions.
- 3 runs per condition per family.
- Conditions: no defense, static keyword filter, FlowFence-Lite.
- Summary CSV: `artifacts/icde2027_supplemental/results/paraphrase_family_results.csv`.

### Results

Average across six families:

| condition | exposed poison | attack manifestation | clean utility | attacked utility | intervention |
| --- | ---: | ---: | ---: | ---: | ---: |
| No defense | `0.4800` | `0.0000` | `0.2778` | `0.1800` | `0.0000` |
| Static keyword filter | `0.4844` | `0.2022` | `0.2444` | `0.1667` | `0.0000` |
| FlowFence-Lite | `0.0000` | `0.0000` | `0.2311` | `0.2267` | `0.4601` |

Per-family static filter vs FlowFence-Lite exposed/manifestation:

| family | static filter | FlowFence-Lite |
| --- | ---: | ---: |
| direct instruction | `0.4667 / 0.2133` | `0.0000 / 0.0000` |
| policy style | `0.4000 / 0.1867` | `0.0000 / 0.0000` |
| factual note | `0.4533 / 0.1867` | `0.0000 / 0.0000` |
| system imitation | `0.5200 / 0.2400` | `0.0000 / 0.0000` |
| tool suggestion | `0.5333 / 0.2667` | `0.0000 / 0.0000` |
| indirect preference | `0.5333 / 0.1200` | `0.0000 / 0.0000` |

### Supported Claim

This is the strongest evidence that old-phrase static filtering is brittle under paraphrased poisoned memory. FlowFence-Lite prevents model-visible exposure and manifestation across all tested paraphrase families.

### Caveat

The raw poisoned retrieval field is not informative for this paraphrase-family stress test because the paraphrase injection path does not increment the raw poisoned-label counter. Use exposed poisoned retrieval and attack manifestation for this stress result. Use the main matrix and pressure slice for raw-poison containment evidence.

### Not Supported

Do not claim universal detection. The result is bounded to the six tested paraphrase families on the same adapted AgentPoison MiniMax axis.

## Experiment 11: ICDE Supplemental Clean False-Positive / Benign Instruction-Like Records

### Purpose

Test whether FlowFence-Lite over-quarantines benign instruction-like memory records.

### How It Was Run

- Clean memory evaluation.
- Benign instruction-like records inserted into retrievable memory.
- 25 clean questions.
- 3 runs per condition.
- Conditions: no defense, FlowFence-Lite.
- Summary CSV: `artifacts/icde2027_supplemental/results/false_positive_results.csv`.

### Results

| condition | clean utility | attacked utility | benign retrieved cases | benign quarantined cases | false quarantine rate |
| --- | ---: | ---: | ---: | ---: | ---: |
| No defense | `0.2800` | `0.2400` | `14.0` | `0.0` | `0.0000` |
| FlowFence-Lite | `0.2533` | `0.1600` | `16.0` | `0.0` | `0.0000` |

### Supported Claim

FlowFence-Lite does not trivially quarantine all instruction-like retrieved memory in this clean benign-instruction slice. False quarantine rate is measurable and currently zero for the tested benign templates.

### Not Supported

Do not claim utility improvement. Clean and attacked utility are lower under FlowFence-Lite in this slice. This should be written as false-positive/trade-off evidence.

## Experiment 12: ICDE Supplemental Audit Trace Case Study

### Purpose

Show the ICDE data-engineering value of FlowFence-Lite: the system can answer which poisoned record was retrieved, whether it crossed the retrieval-exposure boundary, what defense decision was made, and whether the attack manifested.

### How It Was Run

- Exported representative cases from completed runs.
- Output files:
  - `artifacts/icde2027_supplemental/audit_cases/audit_cases.jsonl`
  - `artifacts/icde2027_supplemental/audit_cases/audit_cases.json`
  - `artifacts/icde2027_supplemental/audit_cases/audit_cases.md`

### Cases

| case | raw poison retrieved | boundary crossed | attack manifestation | interpretation |
| --- | ---: | ---: | ---: | --- |
| no-defense attack | true | true | true | Poisoned record enters model-visible context and attack succeeds. |
| FlowFence containment | true | false | false | Poisoned record is retrieved but quarantined before exposure. |
| static-filter paraphrase miss | true | true | true | Static filter fails to block paraphrased poisoned instruction. |

### Supported Claim

FlowFence-Lite is not just deleting text. It preserves audit state for raw retrieval, quarantine decision, reason codes, model-visible context, and final outcome.

### Not Supported

This is a case study, not aggregate statistical evidence. Use it to illustrate auditability and provenance semantics.

## Experiment 13: ICDE Supplemental Batch Completion / Reproducibility Packaging

### Purpose

Ensure the supplemental experiments are complete and locally available for paper writing.

### How It Was Run

- Remote monitor supervised the ICDE supplemental batch.
- Expected runs: 87.
- Final monitor status: `artifacts/icde2027_supplemental/monitor/final_status.json`.
- Summary outputs:
  - `artifacts/icde2027_supplemental/results/icde_supplemental_summary.json`
  - `artifacts/icde2027_supplemental/results/poison_pressure_results.csv`
  - `artifacts/icde2027_supplemental/results/paraphrase_family_results.csv`
  - `artifacts/icde2027_supplemental/results/false_positive_results.csv`

### Results

| expected | success | failed or missing | completed at |
| ---: | ---: | ---: | --- |
| `87` | `87` | `0` | `2026-05-08T18:05:30` |

### Supported Claim

The supplemental result tables used in the ICDE draft are complete and traceable to synced artifacts.

## Experiment 14: AgentDojo MiniMax Auxiliary Studies

### Purpose

Explore whether AgentDojo can serve as a stable additional baseline for before/after defense evaluation under MiniMax.

### How It Was Run

Several AgentDojo axes were searched or selected-rerun tested:

- Banking selected native defenses:
  - `results/baseline_agentdojo_minimax27_banking_selected_native_defenses_summary.json`
- Banking stable-pair search:
  - `results/baseline_agentdojo_minimax27_banking_stable_pair_search_summary.json`
- Axis-switch attempt:
  - `results/baseline_agentdojo_minimax27_axis_switch_attempt_summary.json`

### Results

| study | search signal | selected rerun outcome |
| --- | --- | --- |
| Banking fixed pair | One selected dual-success hit found. | No-defense dual success `0/3` in selected reruns. |
| Native defenses | Same fixed pair with AgentDojo defenses. | Spotlighting injected goal `0/3`, utility `2/3`, but no stable no-defense anchor. |
| Banking stability search | Best candidate had selected dual success `2/3`. | Still not stable enough for robust baseline. |
| Axis switch | Slack partial search found five dual-success candidates. | Selected reruns of four candidates had security false / injected goal not reproduced. |

### Supported Claim

AgentDojo is useful as auxiliary evidence and supports a methodological point: search hits under MiniMax can be stochastic, so selected reruns are necessary before claiming defense effectiveness.

### Not Supported

Do not use AgentDojo as the main stable before/after baseline. Do not claim FlowFence-Lite or native defenses beat AgentDojo baselines from these runs.

## Experiment 15: ASB / Other Baseline Scouting

### Purpose

Early baseline scouting tested whether ASB or other benchmark paths should be on the critical path.

### Result

ASB smoke progressed into live agent execution but remained failing/blocked. It is frozen as a non-critical smoke artifact and not used for the current ICDE paper claims.

### Supported Claim

None for the paper's main results. It only explains why ASB is not part of the current evidence chain.

## Experiment 16: EMNLP P0 Cross-Provider, Same-Axis Baselines, and Fixed-Trace Overhead

### Purpose

Strengthen the EMNLP submission evidence with the smallest high-value additions: cross-provider containment on the same adapted AgentPoison axis, stronger same-axis lightweight baselines, and an overhead measurement that isolates local containment work from provider trajectory variance.

### How It Was Run

- Benchmark axis: adapted AgentPoison StrategyQA full-ReAct with fixed 25-question subset.
- Provider profiles for formal cross-provider matrix: `minimax27`, `qwen36`, `kimi25`.
- Conditions for each provider: no defense, static keyword filter, FlowFence-Lite quarantine + action canonicalization.
- Reruns: 3 per provider-condition group.
- Same-axis stronger baselines: MiniMax paraphrase-aware keyword filter and prompt quoting/isolation, 3 reruns each.
- Fixed-trace overhead replay: offline replay over 466 retrieved-observation events from existing no-defense traces, including 22 poisoned retrieval events.
- Completion status: formal `18/18` successful runs, same-axis `6/6` successful runs, final failed or missing runs `0`.
- Summary artifacts:
  - `artifacts/emnlp2026_p0/results/emnlp_p0_cross_provider_results.csv`
  - `artifacts/emnlp2026_p0/results/emnlp_p0_cross_provider_runs.csv`
  - `artifacts/emnlp2026_p0/results/emnlp_p0_cross_provider_summary.json`
  - `artifacts/emnlp2026_p0/overhead_replay/fixed_trace_overhead_replay.csv`
  - `artifacts/emnlp2026_p0/overhead_replay/fixed_trace_overhead_replay_summary.json`

### Cross-Provider Results

| provider | condition | clean utility | attacked utility | raw poison | exposed poison | manifestation | intervention | false-block proxy |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| MiniMax | no defense | `0.373` | `0.333` | `0.467` | `0.467` | `0.253` | `0.000` | `0.000` |
| MiniMax | static keyword | `0.360` | `0.360` | `0.467` | `0.000` | `0.000` | `0.496` | `0.000` |
| MiniMax | FlowFence-Lite | `0.360` | `0.387` | `0.440` | `0.000` | `0.000` | `0.477` | `0.027` |
| qwen36 | no defense | `0.853` | `0.267` | `0.960` | `0.960` | `0.693` | `0.000` | `0.000` |
| qwen36 | static keyword | `0.893` | `0.720` | `0.960` | `0.000` | `0.000` | `0.382` | `0.040` |
| qwen36 | FlowFence-Lite | `0.867` | `0.653` | `0.960` | `0.000` | `0.000` | `0.397` | `0.040` |
| kimi25 | no defense | `0.440` | `0.027` | `0.960` | `0.960` | `0.893` | `0.000` | `0.000` |
| kimi25 | static keyword | `0.493` | `0.600` | `0.960` | `0.000` | `0.000` | `0.359` | `0.040` |
| kimi25 | FlowFence-Lite | `0.427` | `0.600` | `0.960` | `0.000` | `0.000` | `0.399` | `0.040` |

The full CSV includes case-level descriptive bootstrap intervals over the fixed question subset and repeats. These intervals should be described as descriptive intervals, not as sampling guarantees over a new dataset.

### Same-Axis Stronger Baseline Results

| condition | clean utility | attacked utility | raw poison | exposed poison | manifestation | intervention | false-block proxy |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Paraphrase-aware keyword filter | `0.240` | `0.133` | `0.427` | `0.427` | `0.253` | `0.011` | `0.013` |
| Prompt quoting / isolation | `0.413` | `0.280` | `0.427` | `0.427` | `0.227` | `1.030` | `0.493` |

These results are important because they refine the baseline story. A static keyword filter can block a known trigger, but a lightweight generalized keyword baseline and prompt-level quoting/isolation do not establish a retrieval-to-exposure containment boundary on this same axis.

### Fixed-Trace Overhead Replay

| defense mode | events | poisoned events | poisoned exposed | interventions | local replay time | microseconds/event | token proxy delta |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| No defense | `466` | `22` | `22` | `0` | `0.000449s` | `0.9633` | `0.00` |
| Static keyword filter | `466` | `22` | `0` | `22` | `0.001278s` | `2.7433` | `-2352.75` |
| FlowFence-Lite MVP | `466` | `22` | `0` | `22` | `0.006533s` | `14.0188` | `-2380.25` |
| Prompt quoting / isolation | `466` | `22` | `22` | `466` | `0.000589s` | `1.2630` | `15960.50` |

### Supported Claim

This experiment strengthens the main claim from a MiniMax-only result to a three-provider containment result on the same adapted AgentPoison axis. FlowFence-Lite does not remove attack pressure: raw poisoned retrieval remains high, especially on qwen36 and kimi25. It prevents the poisoned retrieval from crossing the retrieval-to-exposure boundary and prevents attack manifestation in all formal provider profiles.

It also supports a focused overhead claim: local FlowFence-Lite containment inspection and serialization are small in absolute terms on fixed traces. Prompt quoting has low local computation cost but preserves poisoned content in model-visible context and greatly increases token proxy size.

### Not Supported

Do not claim FlowFence-Lite universally outperforms static keyword filtering. On known-trigger settings, static keyword filtering also reaches zero exposed poison and zero attack manifestation.

Do not claim strict utility improvement. Utility is provider-dependent: qwen36 static filtering has higher attacked utility than FlowFence-Lite, while kimi25 has equal attacked utility for both. The correct claim is utility retention under containment, with provider-specific trade-offs.

Do not claim full provider generalization beyond these three provider profiles or official AgentPoison reproduction. The axis is still the adapted trigger-query full-ReAct setting.

## Claim Matrix for Paper Writing

| claim | support level | evidence |
| --- | --- | --- |
| Raw poisoned retrieval remains non-zero while FlowFence-Lite blocks exposed poison. | Strong on adapted AgentPoison axis across MiniMax, qwen36, and kimi25. | Main matrix + pressure slice + EMNLP P0 cross-provider table. |
| FlowFence-Lite prevents attack manifestation on the main axis. | Strong on adapted AgentPoison axis across MiniMax, qwen36, and kimi25. | Main matrix, ablation, pressure, paraphrase, EMNLP P0 cross-provider table. |
| Static keyword filtering is brittle under paraphrase. | Strong within tested paraphrase families. | Held-out stress + 6-family supplemental paraphrase. |
| FlowFence-Lite is better than static filtering in all settings. | Not supported. | Static filter also wins on known-trigger pressure/main axis. |
| FlowFence-Lite provides auditability beyond filtering. | Supported by design + audit case study. | Audit trace exports. |
| Prompt quoting alone establishes containment. | Not supported on EMNLP P0 same-axis baseline. | Prompt quoting leaves exposed poison at `0.4267` and manifestation at `0.2267`. |
| FlowFence-Lite preserves utility. | Conservative support only. | Main matrix roughly comparable; EMNLP P0 utility is provider-dependent. |
| FlowFence-Lite has low local containment overhead. | Stronger support after fixed-trace replay. | Fixed-trace replay reports about `14.0` microseconds/event and `0/22` poisoned events exposed. |
| FlowFence-Lite is generally faster or cheaper. | Not supported. | Measured lower cost is trajectory-confounded. |
| FlowFence-Lite generalizes across model providers on this axis. | Moderate support. | EMNLP P0 covers MiniMax, qwen36, and kimi25 on the same adapted axis. |
| FlowFence-Lite generalizes across attacks/topologies/domains. | Not supported. | No topology or cross-domain matrix yet. |
| AgentDojo provides a stable main baseline. | Not supported. | Selected reruns unstable. |
| Full official AgentPoison reproduction succeeded. | Not supported. | Current main axis is adapted. |

## Recommended Paper Use

### Main Evaluation Table

For the EMNLP draft, use the EMNLP P0 cross-provider table as the main evaluation table:

- providers: MiniMax, qwen36, kimi25,
- conditions: no defense, static keyword filter, FlowFence-Lite,
- metrics: clean utility, attacked utility, raw poison, exposed poison, attack manifestation, intervention rate.

This establishes that the containment pattern is not MiniMax-only on the adapted axis.

For mechanism detail, use the same-axis MiniMax matrix:

- No defense,
- static keyword filter,
- rewrite-only,
- quarantine-only,
- quarantine + action-canon.

This establishes the core containment and mechanism story.

### Robustness Table

Use the supplemental pressure table:

- no defense,
- static keyword filter,
- FlowFence-Lite,
- aggregate over `knn1/3/5`.

This shows raw attack pressure persists while FlowFence-Lite blocks exposure.

### Stress Table

Use the supplemental paraphrase-family table:

- six families,
- static filter vs FlowFence-Lite exposed/manifestation.

This is the strongest evidence against relying only on old-phrase filtering.

### False-Positive / Audit Table

Use a compact combined table:

- clean benign-instruction false quarantine,
- audit case boundary crossing.

This supports the ICDE data-governance angle.

### Overhead Table

For the EMNLP draft, use the fixed-trace overhead replay as the cleanest overhead table:

- no defense,
- static keyword filter,
- FlowFence-Lite MVP,
- prompt quoting/isolation.

This isolates local containment overhead from provider trajectory changes.

For historical ICDE notes, keep the older proxy/measured overhead artifacts as secondary evidence:

- 25-question proxy overhead,
- 10-question measured overhead.

Keep the caveat: measured lower token/time cost is not a general speed claim.

## Claims to Avoid

- FlowFence-Lite is secure.
- FlowFence-Lite is a universal poison detector.
- FlowFence-Lite fully reproduces and beats official AgentPoison.
- FlowFence-Lite broadly generalizes across all agent frameworks.
- FlowFence-Lite broadly generalizes across all model providers.
- FlowFence-Lite outperforms every simple defense.
- FlowFence-Lite improves utility.
- FlowFence-Lite is generally faster or cheaper.
- AgentDojo is a stable main before/after baseline under MiniMax.

## Artifact Index

### Main Paper Draft

- `papers/icde2027_flowfence/main.tex`
- `papers/emnlp2026_flowfence/main.tex`

### Paper-Facing Summaries

- `papers/result_table_agentpoison_minimax.md`
- `papers/experiment_narrative_agentpoison_minimax.md`
- `papers/claims_checklist.md`
- `papers/overhead_agentpoison_minimax.md`
- `papers/overhead_agentpoison_minimax_measured.md`

### Main Result Artifacts

- `results/baseline_agentpoison_fullreact_minimax27_small_matrix_summary.json`
- `results/baseline_agentpoison_fullreact_minimax27_static_keyword_filter_weak_comparator_summary.json`
- `results/baseline_agentpoison_fullreact_minimax27_rewrite_only_weak_comparator_summary.json`
- `results/ablation_agentpoison_fullreact_minimax27_quarantine_only_vs_actioncanon_summary.json`
- `results/baseline_agentpoison_fullreact_minimax27_heldout_instruction_matrix_summary.json`
- `results/overhead_agentpoison_fullreact_minimax27_same_axis_proxy_summary.json`
- `results/overhead_agentpoison_fullreact_minimax27_same_axis_measured_summary.json`

### Supplemental ICDE Artifacts

- `artifacts/icde2027_supplemental/monitor/final_status.json`
- `artifacts/icde2027_supplemental/results/icde_supplemental_summary.json`
- `artifacts/icde2027_supplemental/results/poison_pressure_results.csv`
- `artifacts/icde2027_supplemental/results/paraphrase_family_results.csv`
- `artifacts/icde2027_supplemental/results/false_positive_results.csv`
- `artifacts/icde2027_supplemental/audit_cases/audit_cases.md`
- `artifacts/icde2027_supplemental/audit_cases/audit_cases.jsonl`

### EMNLP P0 Artifacts

- `artifacts/emnlp2026_p0/monitor/formal_final_status.json`
- `artifacts/emnlp2026_p0/monitor/same_axis_final_status.json`
- `artifacts/emnlp2026_p0/results/emnlp_p0_cross_provider_results.csv`
- `artifacts/emnlp2026_p0/results/emnlp_p0_cross_provider_runs.csv`
- `artifacts/emnlp2026_p0/results/emnlp_p0_cross_provider_summary.json`
- `artifacts/emnlp2026_p0/overhead_replay/fixed_trace_overhead_replay.csv`
- `artifacts/emnlp2026_p0/overhead_replay/fixed_trace_overhead_replay_summary.json`
- `results/emnlp_p0_same_axis_paraphrase_aware_keyword_filter_v1`
- `results/emnlp_p0_same_axis_paraphrase_aware_keyword_filter_repeat1`
- `results/emnlp_p0_same_axis_paraphrase_aware_keyword_filter_repeat2`
- `results/emnlp_p0_same_axis_prompt_quoting_isolation_v1`
- `results/emnlp_p0_same_axis_prompt_quoting_isolation_repeat1`
- `results/emnlp_p0_same_axis_prompt_quoting_isolation_repeat2`

### AgentDojo Auxiliary Artifacts

- `results/baseline_agentdojo_minimax27_banking_selected_native_defenses_summary.json`
- `results/baseline_agentdojo_minimax27_banking_stable_pair_search_summary.json`
- `results/baseline_agentdojo_minimax27_axis_switch_attempt_summary.json`
