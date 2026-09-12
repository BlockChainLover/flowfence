# AAMAS paper integration



Use only the completed rows below. All rates are proportions; exposure/intervention columns are episode means unless stated otherwise.



## Table A — Equal-capability deterministic benchmark



| Defense | n | Task | Safe task | Raw | External | Pairs | Interventions | Blocks |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| PAPC | 90 | 1 | 1 | 0 | 0 | 0 | 1.2 | 0.3 |
| IFC-SafeView | 90 | 1 | 1 | 0 | 0 | 0 | 0.9 | 0 |
| No Defense | 90 | 0.1 | 0.1 | 13.2 | 2.4 | 6 | 0 | 0 |



| Paired metric | Matched | PAPC better | Tie | PAPC worse | Unavailable | Task-cluster sign p |
| --- | --- | --- | --- | --- | --- | --- |
| success | 90 | 0 | 90 | 0 | 0 | 1 |
| privacy_safe_success | 90 | 0 | 90 | 0 | 0 | 1 |
| raw_exposure | 90 | 0 | 90 | 0 | 0 | 1 |
| external_exposure | 90 | 0 | 90 | 0 | 0 | 1 |
| exposure_recipient_pairs | 90 | 0 | 90 | 0 | 0 | 1 |
| intervention_count | 90 | 0 | 66 | 24 | 0 | 1 |
| blocks | 90 | 0 | 63 | 27 | 0 | 1 |



Conclusion: PAPC and IFC-SafeView tie on measured task success and privacy in every matched deterministic group; this experiment does not establish an advantage from PAPC-specific mechanisms. PAPC minus IFC mean intervention count is +0.3 per episode.

Cannot claim: PAPC superiority or task-population significance; the 90 groups reuse one task and the sign test has at most one independent task cluster.



## Table B — LLM-driven agents



| Topology | Condition | Defense | n | Measured n | Failed | Task | Safe task | Raw | External | Interventions | Blocks |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| blackboard_4 | attack | PAPC | 12 | 12 | 0 | 1 | 1 | 0 | 0 | 1 | 0 |
| blackboard_4 | attack | IFC-SafeView | 12 | 12 | 0 | 1 | 1 | 0 | 0 | 1 | 0 |
| blackboard_4 | attack | No Defense | 12 | 11 | 1 | 0.916667 | 0 | 17.0909 | 1.09091 | 0 | 0 |
| blackboard_4 | clean | PAPC | 12 | 12 | 0 | 1 | 1 | 0 | 0 | 0 | 0 |
| blackboard_4 | clean | IFC-SafeView | 12 | 12 | 0 | 1 | 1 | 0 | 0 | 0 | 0 |
| blackboard_4 | clean | No Defense | 12 | 12 | 0 | 1 | 1 | 0 | 0 | 0 | 0 |
| chain_4 | attack | PAPC | 12 | 12 | 0 | 1 | 1 | 0 | 0 | 1 | 0 |
| chain_4 | attack | IFC-SafeView | 12 | 12 | 0 | 1 | 1 | 0 | 0 | 1 | 0 |
| chain_4 | attack | No Defense | 12 | 10 | 2 | 0.75 | 0 | 8 | 0 | 0 | 0 |
| chain_4 | clean | PAPC | 12 | 12 | 0 | 1 | 1 | 0 | 0 | 0 | 0 |
| chain_4 | clean | IFC-SafeView | 12 | 12 | 0 | 1 | 1 | 0 | 0 | 0 | 0 |
| chain_4 | clean | No Defense | 12 | 12 | 0 | 1 | 1 | 0 | 0 | 0 | 0 |



Source versus model-generated exposure (episode means):



| Topology | Condition | Defense | Source raw | Generated raw | Source external | Generated external |
| --- | --- | --- | --- | --- | --- | --- |
| blackboard_4 | attack | PAPC | 0 | 0 | 0 | 0 |
| blackboard_4 | attack | IFC-SafeView | 0 | 0 | 0 | 0 |
| blackboard_4 | attack | No Defense | 16 | 1.09091 | 1 | 0.0909091 |
| blackboard_4 | clean | PAPC | 0 | 0 | 0 | 0 |
| blackboard_4 | clean | IFC-SafeView | 0 | 0 | 0 | 0 |
| blackboard_4 | clean | No Defense | 0 | 0 | 0 | 0 |
| chain_4 | attack | PAPC | 0 | 0 | 0 | 0 |
| chain_4 | attack | IFC-SafeView | 0 | 0 | 0 | 0 |
| chain_4 | attack | No Defense | 8 | 0 | 0 | 0 |
| chain_4 | clean | PAPC | 0 | 0 | 0 | 0 |
| chain_4 | clean | IFC-SafeView | 0 | 0 | 0 | 0 |
| chain_4 | clean | No Defense | 0 | 0 | 0 | 0 |



Matched PAPC vs IFC-SafeView, by topology/condition and overall:



| Topology | Condition | Metric | n | Better | Tie | Worse | Unavailable |
| --- | --- | --- | --- | --- | --- | --- | --- |
| chain_4 | clean | success | 12 | 0 | 12 | 0 | 0 |
| chain_4 | clean | privacy_safe_success | 12 | 0 | 12 | 0 | 0 |
| chain_4 | clean | raw_exposure | 12 | 0 | 12 | 0 | 0 |
| chain_4 | clean | intervention_count | 12 | 0 | 12 | 0 | 0 |
| chain_4 | attack | success | 12 | 0 | 12 | 0 | 0 |
| chain_4 | attack | privacy_safe_success | 12 | 0 | 12 | 0 | 0 |
| chain_4 | attack | raw_exposure | 12 | 0 | 12 | 0 | 0 |
| chain_4 | attack | intervention_count | 12 | 0 | 12 | 0 | 0 |
| blackboard_4 | clean | success | 12 | 0 | 12 | 0 | 0 |
| blackboard_4 | clean | privacy_safe_success | 12 | 0 | 12 | 0 | 0 |
| blackboard_4 | clean | raw_exposure | 12 | 0 | 12 | 0 | 0 |
| blackboard_4 | clean | intervention_count | 12 | 0 | 12 | 0 | 0 |
| blackboard_4 | attack | success | 12 | 0 | 12 | 0 | 0 |
| blackboard_4 | attack | privacy_safe_success | 12 | 0 | 12 | 0 | 0 |
| blackboard_4 | attack | raw_exposure | 12 | 0 | 12 | 0 | 0 |
| blackboard_4 | attack | intervention_count | 12 | 0 | 12 | 0 | 0 |
| overall | overall | success | 48 | 0 | 48 | 0 | 0 |
| overall | overall | privacy_safe_success | 48 | 0 | 48 | 0 | 0 |
| overall | overall | raw_exposure | 48 | 0 | 48 | 0 | 0 |
| overall | overall | intervention_count | 48 | 0 | 48 | 0 | 0 |



Conclusion: PAPC and IFC-SafeView tie in all 48 matched groups on task success, privacy-safe success, raw/external exposure, unique exposure pairs, interventions and blocks. The live three-agent slice provides no measured PAPC advantage over equal-capability IFC-SafeView.

Overall first-attempt task outcome counts:



| Defense | Episodes | Task successes | Privacy-safe successes |
| --- | --- | --- | --- |
| PAPC | 48 | 48 | 48 |
| IFC-SafeView | 48 | 48 | 48 |
| No Defense | 48 | 44 | 24 |



Observed source/generated exposure totals (all recorded attempts, including partial observations): {"flowfence_lite_nonoracle": {"generated_external_exposure": 0, "generated_raw_exposure": 0, "source_external_exposure": 0, "source_raw_exposure": 0}, "ifc_safeview": {"generated_external_exposure": 0, "generated_raw_exposure": 0, "source_external_exposure": 0, "source_raw_exposure": 0}, "none": {"generated_external_exposure": 1, "generated_raw_exposure": 12, "source_external_exposure": 12, "source_raw_exposure": 284}}. Generated exposures are actual measured model-action disclosures, distinct from injected-source leakage.

Cannot claim: independence across domains, production multi-agent robustness, or LLM-caused leakage from source injection counts. The private cap is nonbinding among the twelve selected tasks' cheapest deadline-eligible quotes. Formal primary rows use first attempts; pilot and wiring fixtures are separate.



Actual E1 serialized safe-audit storage (episodes, events, and call attempts):



| Defense | Attempts | Total bytes | KiB/episode |
| --- | --- | --- | --- |
| PAPC | 48 | 628679 | 12.7905 |
| IFC-SafeView | 48 | 613993 | 12.4917 |
| No Defense | 48 | 595978 | 12.1252 |



This includes real stored call-start and call-completion records and excludes private full prompts/responses; it is separate from the E2 standard-schema projection.



## Table C — Mediation latency and serialized storage



| Mode | Events/trial | Trials | p50 µs | p95 µs | p99 µs | Mean µs | Events/s | Bytes/event | KiB/24 events |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| PAPC | 1000 | 5 | 7.833 | 9.166 | 11.1254 | 6.20776 | 161089 | 2366.78 | 55.4715 |
| PAPC | 10000 | 5 | 7.791 | 9.125 | 12.125 | 6.22284 | 160698 | 2368.67 | 55.5156 |
| PAPC | 100000 | 5 | 7.833 | 9.25 | 12.458 | 6.29431 | 158874 | 2370.54 | 55.5596 |
| IFC-SafeView | 1000 | 5 | 1.084 | 6 | 7.00041 | 2.7415 | 364764 | 1522.71 | 35.6886 |
| IFC-SafeView | 10000 | 5 | 1.125 | 6.041 | 7 | 2.75727 | 362677 | 1524.1 | 35.721 |
| IFC-SafeView | 100000 | 5 | 1.125 | 6.041 | 6.792 | 2.76987 | 361028 | 1525.47 | 35.7533 |
| No Defense | 1000 | 5 | 0.417 | 0.542 | 0.584 | 0.455214 | 2.19677e+06 | 1075.75 | 25.213 |
| No Defense | 10000 | 5 | 0.458 | 0.541 | 0.625 | 0.457412 | 2.18621e+06 | 1076.76 | 25.2366 |
| No Defense | 100000 | 5 | 0.458 | 0.5 | 0.584 | 0.466748 | 2.14249e+06 | 1077.76 | 25.2601 |



Conclusion: The measured Python mediator has microsecond-scale per-event cost on this host and event mix; actual audit serialization grows approximately linearly over the measured sizes.

Cannot claim: production throughput, provider latency improvements, or measured E1 storage. Timing includes dispatch/timer overhead, excludes model calls, and storage reflects redacted audit schemas with policy records for interventions.



## Table D — Tested representation transformations



| Transformation | Defense | Probes | Reconstruction leaks | Leak rate | Exact-string hits | Interventions |
| --- | --- | --- | --- | --- | --- | --- |
| T1_formatting | PAPC | 10 | 10 | 1 | 0 | 0 |
| T2_split_history | PAPC | 10 | 10 | 1 | 0 | 0 |
| T3_public_threshold | PAPC | 10 | 10 | 1 | 0 | 0 |
| T1_formatting | IFC-SafeView | 10 | 10 | 1 | 0 | 0 |
| T2_split_history | IFC-SafeView | 10 | 10 | 1 | 0 | 0 |
| T3_public_threshold | IFC-SafeView | 10 | 10 | 1 | 0 | 0 |
| T1_formatting | No Defense | 10 | 10 | 1 | 0 | 0 |
| T2_split_history | No Defense | 10 | 10 | 1 | 0 | 0 |
| T3_public_threshold | No Defense | 10 | 10 | 1 | 0 | 0 |



Conclusion: Recipient-history reconstruction detects disclosure in 90/90 probes while canonical exact matching records 0 exposure events; the evaluated defense does not protect these tested representations.

Cannot claim: semantic confidentiality or ten independent private-value domains. These ten scenario labels share one underlying secret; no task utility or model attack-generation success was measured.



## Table E — Second-model confirmation attempts



| Model | Defense | Attempts | Failed | Measured n | Task incl. failure | Safe task incl. failure | Raw | External |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| kimi-k2.6 | PAPC | 10 | 10 | 0 | 0 | 0 | N/A | N/A |
| kimi-k2.6 | IFC-SafeView | 10 | 10 | 0 | 0 | 0 | N/A | N/A |

Conclusion: The second-model API execution is blocked; failed attempts supply no model confirmation or measured privacy outcome.

Cannot claim: model-family generalization, equivalent privacy, or a successful confirmation from unavailable model outputs.



## Topology interpretation



Topology retained as environmental risk factor rather than independently validated algorithmic contribution.



## Proposed main claim



Equal-capability runtime mediation contains measured exact-value disclosure in the evaluated scripted and LLM-driven enterprise workflows; PAPC shows no measured advantage over IFC-SafeView in either comparison, and neither defense contains the tested reconstructable transformations.
