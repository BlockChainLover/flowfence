# Results Draft v2

## Scope and evidence sources

This Results draft separates five evidence layers. First, P0 evaluates adapted AgentPoison full-ReAct retrieval-memory containment under MiniMax. Second, P1 deterministic evidence evaluates a synthetic deterministic MAS runtime with provider calls disabled. Third, the MiniMax-backed multi-agent synthetic-runtime coverage experiment evaluates the same benchmark with MiniMax as the final writer. Fourth, the non-oracle validation tests whether FlowFence-Lite remains effective when the defense cannot use oracle attack annotations. Fifth, the no-semantic-pattern ablation tests whether semantic pattern detection is carrying the entire effect.

MiniMax is the only real provider used in the current evidence. The non-oracle evidence includes a 540-run deterministic validation and a 72-run targeted MiniMax-backed synthetic-runtime validation. These results do not support non-MiniMax generalization, production safety, real browser/desktop/computer-use deployment evidence, or arbitrary attack robustness. Raw traces and provider outputs are intentionally outside the paper-facing evidence package.

## RQ1: Does FlowFence-Lite contain retrieval-memory poisoning in the adapted AgentPoison setting?

Table 1 shows that the no-defense adapted AgentPoison comparator creates non-vacuous attack pressure: exposed poisoned retrieval has mean `0.4667`, raw poisoned retrieval has mean `0.4667`, and attack manifestation has mean `0.2533` across the saved no-defense runs. Under FlowFence-Lite quarantine plus canonical ReAct action writeback, raw poisoned retrieval remains internally present with mean `0.44`, but exposed poisoned retrieval and attack manifestation are both reduced to `0.0` on the saved P0 axis.

This supports retrieval-memory containment on the adapted comparator. It does not establish an official AgentPoison reproduction. Utility should be described conservatively: clean utility changes from `0.3733` under no defense to `0.36` under FlowFence-Lite, while attacked utility changes from `0.3333` to `0.3867`. This is noisy, roughly preserved utility evidence, not a utility-improvement claim.

The weak-comparator rows narrow the interpretation. Rewrite-only also blocks exposed poisoned retrieval and attack manifestation on the same detector-mediated axis, and static keyword filtering blocks the known-trigger setting. The supported P0 statement is therefore structured containment on the adapted retrieval-memory axis, not broad superiority over all simple filters.

## RQ2: Does propagation-aware containment help in deterministic multi-agent synthetic settings?

Table 2 reports deterministic synthetic MAS evidence. The initial deterministic sweep produced meaningful leakage pressure and FlowFence improvements over no-defense on raw and external leakage, but it did not support a topology-effect claim. After benchmark strengthening, the deterministic benchmark completed 252/252 runs and records `topology_effect_observed=true`.

The strengthened deterministic benchmark supports the method mechanism in the synthetic runtime. FlowFence-Lite improves over `prompt_filter` on all 9 indirect attack/topology groups for unauthorized raw leakage, external leakage, cascade size, and privilege reach. Against `static_acl`, FlowFence improves on all 9 indirect groups for cascade size and privilege reach, on 6/9 groups for unauthorized raw leakage, and on 4/9 groups for external leakage.

These are deterministic synthetic benchmark results. They should not be described as real-provider evidence or deployment behavior.

## RQ3: Does MiniMax-backed MAS coverage support the same containment trend?

Table 3 is the canonical MiniMax main-coverage table. The MiniMax-only P1 MAS coverage over the synthetic deterministic runtime completed 252/252 configured runs after retrying one transient MiniMax read timeout. The matrix covers 3 topologies, 7 attacks, 4 defenses, and seeds `1`, `2`, and `3`. Aggregate metrics are `task_success_rate=0.964286`, `unauthorized_raw_leakage_mean=2.829365`, `external_leakage_mean=0.325397`, `cascade_size_mean=4.178571`, and `privilege_reach_mean=2.678571`.

The FlowFence subset is the central containment result. Across all 63 configured FlowFence runs, the clean subset is 63/63, with `task_success_rate=1.0`, `unauthorized_raw_leakage_mean=0.0`, and `external_leakage_mean=0.0`. Table 6 records the same seed-level pattern: seeds 1, 2, and 3 each have 21/21 clean FlowFence runs, task success 1.0, and zero raw/external leakage.

Table 3 supports improvement-or-tie comparisons against simple baselines. Against no-defense, FlowFence improves raw leakage in 42 groups and ties in 21, improves external leakage in 32 and ties in 31, and improves task success in 7 and ties in 56. Against static ACL, FlowFence improves raw leakage in 42 groups and ties in 21, improves external leakage in 30 and ties in 33, and ties task success in all 63 groups. Against prompt-filter, FlowFence improves raw leakage in 18 groups and ties in 45, improves external leakage in 13 and ties in 50, and improves task success in 2 and ties in 61.

This supports the same containment trend in a MiniMax-backed multi-agent synthetic-runtime coverage experiment. It is not production evidence, non-MiniMax evidence, or real computer-use deployment evidence.

## RQ4: What do topology and attack channel changes reveal?

The deterministic strengthened benchmark and the MiniMax-backed 252-run coverage both observe topology effects. Table 2 records `topology_effect_observed=true` after benchmark strengthening. Table 3 records `topology_effect_observed=true` across `chain_4`, `star_4`, and `blackboard_4`.

The narrow supported claim is that privacy propagation is topology-sensitive within the synthetic-runtime benchmark. This is consistent with the design intuition that shared-workspace and blackboard-style interaction patterns create more propagation pathways than a narrow chain, but the evidence remains benchmark-scoped. It should not be written as real-world multi-agent deployment evidence.

Attack-channel changes also matter. Indirect attacks are the clearest deterministic setting where FlowFence separates from prompt-filter. In the MiniMax-backed coverage, no-defense exposes expected unprotected risk, static ACL retains policy gaps, and prompt-filter remains weaker on indirect channels than FlowFence across the configured comparison counts.

## RQ5: How does FlowFence-Lite compare to static_acl and prompt_filter?

No-defense rows in Table 3 show expected unprotected risk, with `unauthorized_raw_leakage_mean=4.603175` and `external_leakage_mean=0.571429` across 63 no-defense runs. Static ACL preserves task success in this coverage slice but still has `unauthorized_raw_leakage_mean=4.380952` and `external_leakage_mean=0.47619`, consistent with policy gaps in the benchmark. Prompt-filter has lower aggregate leakage than static ACL but is not clean: its subset records `task_success_rate=0.968254`, `unauthorized_raw_leakage_mean=2.333333`, and `external_leakage_mean=0.253968`.

FlowFence-Lite should be described as improving or tying these baselines on configured raw/external leakage comparisons, not as universally dominating all baselines. The strongest supported statement is that, in the 252-run MiniMax-backed synthetic-runtime coverage, FlowFence is clean across all configured FlowFence runs and improves or ties no-defense, static ACL, and prompt-filter on the recorded raw/external leakage groups.

## RQ6: Does FlowFence-Lite still work without oracle attack annotations?

Table 7 addresses an internal-validity risk in the earlier default `flowfence_lite` path. The default path used `attack_annotation.applied` as part of the poison signal, and that field is ground-truth attack metadata. The non-oracle variant, `flowfence_lite_nonoracle`, ignores `attack_annotation.applied`, `attack_id`, `attack_mode`, and oracle attack labels; its decision metadata records `oracle_annotation_used=false`.

In deterministic non-oracle held-out validation, the configured matrix completed 540/540 runs with 0 failures. The `flowfence_lite_nonoracle` subset has `task_success_rate=1.0`, `unauthorized_raw_leakage_mean=0.0`, `external_leakage_mean=0.0`, and 0 oracle annotation violations. Against no-defense, non-oracle FlowFence improves raw leakage in 81 groups and ties in 9, and improves external leakage in 81 and ties in 9. Against static ACL, it improves raw leakage in 66 and ties in 24, and improves external leakage in 48 and ties in 42. Against prompt-filter, it improves raw leakage in 54 and ties in 36, and improves external leakage in 54 and ties in 36.

The targeted MiniMax-backed synthetic-runtime validation completed 72/72 runs with 0 failures. The `flowfence_lite_nonoracle` subset again has `task_success_rate=1.0`, `unauthorized_raw_leakage_mean=0.0`, `external_leakage_mean=0.0`, and 0 oracle annotation violations. Against no-defense, non-oracle FlowFence improves raw leakage in 15 groups and ties in 3, and improves external leakage in 10 and ties in 8. Against static ACL, it improves raw leakage in 15 and ties in 3, and improves external leakage in 9 and ties in 9. Against prompt-filter, it improves raw leakage in 16 and ties in 2, and improves external leakage in 10 and ties in 8.

This substantially mitigates the oracle-annotation concern for the configured held-out matrices. It does not prove arbitrary attack robustness.

## RQ7: Which mechanism matters: semantic detection or policy/fanout/safe-view containment?

Table 8 reports the no-semantic-pattern ablation. The ablation disables semantic pattern matching while retaining non-oracle policy, fanout, and safe-view behavior. It ties the full non-oracle variant on external leakage and task success in the deterministic results, but it has higher raw leakage: `unauthorized_raw_leakage_mean=1.5` versus `0.0` for `flowfence_lite_nonoracle`.

This suggests semantic pattern detection contributes to raw-leakage containment. At the same time, the ablation did not collapse external leakage or task success, so policy, fanout, and safe-view mechanisms still matter. The supported interpretation is partial mechanism evidence, not a complete component isolation study. The paper should not claim semantic detection is unnecessary. A deeper module-level ablation can remain future work if reviewers require a finer mechanism analysis.

## Summary of supported findings

- P0 retrieval containment is supported on the adapted AgentPoison full-ReAct retrieval-memory comparator.
- P1 deterministic topology effects are supported in the strengthened synthetic runtime.
- In deterministic synthetic settings, FlowFence improves over prompt-filter on indirect attacks.
- The MiniMax-backed 252-run synthetic-runtime coverage supports a FlowFence clean-subset claim under configured attacks, topologies, defenses, and seeds.
- MiniMax evidence supports improvement-or-tie comparisons against no-defense, static ACL, and prompt-filter on configured raw/external leakage comparisons.
- Non-oracle held-out evidence shows FlowFence remains effective without oracle attack annotations on configured held-out paraphrase attacks.
- The no-semantic-pattern ablation suggests semantic detection contributes to raw-leakage containment.

## Limitations and non-claims

- The real-provider evidence is MiniMax-only.
- The P1 runtime is a synthetic deterministic MAS runtime with MiniMax final-writer calls, not a full autonomous real computer-use stack.
- The evidence does not support non-MiniMax provider generalization.
- The evidence does not support production safety.
- The evidence does not support real browser or desktop agent deployment claims.
- The P0 AgentPoison evidence is an adapted comparator, not a full official AgentPoison reproduction.
- The non-oracle held-out validation covers configured paraphrase attacks only; it does not establish arbitrary attack robustness.
- There is no learned graph risk scorer yet.
- There is no human-user study.
- Raw traces, raw provider outputs, prompts, event JSONL, policy JSONL, and per-run metrics are not committed in the paper-facing evidence package.

## Recommended paper table placement

- Table 1: P0 adapted AgentPoison containment.
- Table 2: deterministic synthetic MAS evidence.
- Table 3: canonical MiniMax 252-run coverage.
- Table 4: claims matrix.
- Table 5: evidence boundaries.
- Table 6: seed stability.
- Table 7: non-oracle held-out validation.
- Table 8: non-oracle mechanism ablation.
