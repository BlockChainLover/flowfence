# Results Draft v1

## Scope and evidence sources

This Results draft separates three evidence layers. First, the P0 evidence evaluates adapted AgentPoison full-ReAct retrieval-memory containment under MiniMax. This is a retrieval-memory comparator, not an official AgentPoison reproduction. Second, the P1 deterministic evidence evaluates a synthetic deterministic MAS runtime with provider calls disabled. Third, the P1 MiniMax evidence evaluates a MiniMax-backed multi-agent synthetic-runtime coverage experiment, where MiniMax is used through the `minimax_final_writer` path while the runtime remains the synthetic deterministic MAS benchmark.

MiniMax is the only real provider used in the evidence summarized here. The results do not support non-MiniMax generalization, production safety, or real browser, desktop, or computer-use deployment claims. Raw traces and provider outputs are intentionally outside the paper-facing evidence package.

## RQ1: Does FlowFence-Lite contain retrieval-memory poisoning in the adapted AgentPoison setting?

Table 1 shows that the no-defense adapted AgentPoison comparator creates non-vacuous attack pressure: across three saved no-defense runs, exposed poisoned retrieval has mean `0.4667`, raw poisoned retrieval has mean `0.4667`, and attack manifestation has mean `0.2533`. Under FlowFence-Lite quarantine plus canonical ReAct action writeback, raw poisoned retrieval remains visible internally with mean `0.44`, but exposed poisoned retrieval and attack manifestation are both reduced to `0.0` on the saved P0 axis.

The P0 result supports a retrieval-memory containment claim for this adapted comparator. It does not establish official AgentPoison reproduction. The table also shows that utility should be phrased conservatively: clean utility changes from `0.3733` under no defense to `0.36` under FlowFence-Lite, while attacked utility changes from `0.3333` to `0.3867`. This is noisy, roughly preserved utility evidence, not a utility-improvement result.

The weak-comparator rows narrow the interpretation. Rewrite-only also blocks exposed poisoned retrieval and attack manifestation on the same detector-mediated axis, and a static keyword filter blocks the known-trigger setting. Therefore, the P0 evidence should not claim that quarantine is uniquely necessary for this trigger-string setup or that FlowFence-Lite dominates all independent defenses. The stronger P0 interpretation is that structured containment prevents poisoned retrieval from being exposed on the adapted retrieval-memory axis, while simple same-axis filters can also be effective when the trigger is known.

## RQ2: Does propagation-aware containment help in deterministic multi-agent synthetic settings?

Table 2 reports two deterministic synthetic MAS stages. The initial deterministic sweep produced meaningful leakage pressure and showed FlowFence improvements over no-defense on raw and external leakage, but it did not support a topology-effect claim. The strengthened deterministic benchmark completed 252/252 deterministic runs and records `topology_effect_observed=true`.

The strengthened deterministic benchmark also supports the mechanism story in the synthetic runtime. FlowFence-Lite improves over `prompt_filter` on all 9 indirect attack/topology groups for unauthorized raw leakage, external leakage, cascade size, and privilege reach. Against `static_acl`, FlowFence improves on all 9 indirect groups for cascade size and privilege reach, on 6/9 groups for unauthorized raw leakage, and on 4/9 groups for external leakage.

These results support deterministic synthetic benchmark claims: topology changes propagation behavior, and propagation-aware containment improves over simple prompt-filter and static-ACL baselines on indirect synthetic attacks. They are not real-provider evidence and should not be described as deployment behavior.

## RQ3: Does MiniMax-backed MAS coverage support the same containment trend?

Table 3 is the canonical MiniMax table. The MiniMax-only P1 MAS coverage over the synthetic deterministic runtime completed 252/252 configured runs after retrying one transient MiniMax read timeout. The matrix covers 3 topologies, 7 attacks, 4 defenses, and seeds `1`, `2`, and `3`. The aggregate coverage metrics are `task_success_rate=0.964286`, `unauthorized_raw_leakage_mean=2.829365`, `external_leakage_mean=0.325397`, `cascade_size_mean=4.178571`, and `privilege_reach_mean=2.678571`.

The FlowFence subset is the main containment result in the MiniMax-backed coverage. Across all 63 configured FlowFence runs, the clean subset is 63/63, with `task_success_rate=1.0`, `unauthorized_raw_leakage_mean=0.0`, and `external_leakage_mean=0.0`. Table 6 shows the same pattern by seed: for seeds 1, 2, and 3, FlowFence has task success 1.0 and zero raw/external leakage, with 21/21 clean FlowFence runs per seed.

The configured comparison counts in Table 3 support an improvement-or-tie claim against simple baselines. Against no-defense, FlowFence improves raw leakage in 42 groups and ties in 21, improves external leakage in 32 and ties in 31, and improves task success in 7 and ties in 56. Against static ACL, FlowFence improves raw leakage in 42 groups and ties in 21, improves external leakage in 30 and ties in 33, and ties task success in all 63 groups. Against prompt-filter, FlowFence improves raw leakage in 18 groups and ties in 45, improves external leakage in 13 and ties in 50, and improves task success in 2 and ties in 61.

This supports the same containment trend in a MiniMax-backed multi-agent synthetic-runtime coverage experiment. It does not support a production-safety claim, a non-MiniMax claim, or a real computer-use deployment claim.

## RQ4: What do topology and attack channel changes reveal?

Both the deterministic strengthened benchmark and the MiniMax-backed 252-run coverage observe topology effects. Table 2 records `topology_effect_observed=true` for the strengthened deterministic benchmark. Table 3 records `topology_effect_observed=true` for the 252-run MiniMax coverage across `chain_4`, `star_4`, and `blackboard_4`.

This supports the paper's narrower topology claim: within the synthetic-runtime benchmark, privacy propagation is topology-sensitive. The result is consistent with the design intuition that shared-workspace and blackboard-style interaction patterns create more propagation pathways than a narrow chain. However, the evidence remains benchmark-scoped. It should not be written as evidence that FlowFence-Lite has been evaluated in real-world multi-agent deployments or real desktop/browser environments.

Attack-channel changes also matter. In the deterministic strengthened benchmark, indirect attacks are the clearest setting where FlowFence separates from prompt-filter. In the MiniMax-backed coverage, no-defense exposes expected unprotected risk, static ACL retains policy gaps, and prompt-filter remains weaker on indirect channels than FlowFence across the configured comparison counts.

## RQ5: How does FlowFence-Lite compare to static_acl and prompt_filter?

No-defense rows in Table 3 show expected unprotected risk, with `unauthorized_raw_leakage_mean=4.603175` and `external_leakage_mean=0.571429` across 63 no-defense runs. Static ACL has perfect task success in this coverage slice but still has `unauthorized_raw_leakage_mean=4.380952` and `external_leakage_mean=0.47619`, which is consistent with fixed-policy gaps in the benchmark. Prompt-filter has lower leakage than static ACL in aggregate, but it is still not clean: its subset records `task_success_rate=0.968254`, `unauthorized_raw_leakage_mean=2.333333`, and `external_leakage_mean=0.253968`.

FlowFence-Lite should be described as improving or tying these baselines on configured raw/external leakage comparisons, not as universally dominating all baselines. The strongest supported statement is that, in the 252-run MiniMax-backed synthetic-runtime coverage, FlowFence is clean across all configured FlowFence runs and improves or ties no-defense, static ACL, and prompt-filter on the recorded raw/external leakage comparison groups.

## Summary of supported findings

- P0 retrieval containment is supported on the adapted AgentPoison full-ReAct retrieval-memory comparator: FlowFence-Lite reduces exposed poisoned retrieval and attack manifestation to zero on the saved P0 axis.
- P0 utility should be described as noisy or roughly preserved, not improved.
- Static keyword filtering is a strong same-axis weak baseline on known-trigger settings, which limits uniqueness claims.
- P1 deterministic topology effects are supported in the strengthened synthetic runtime.
- In the deterministic synthetic setting, FlowFence improves over prompt-filter on indirect attacks.
- The MiniMax-backed 252-run synthetic-runtime coverage supports a FlowFence clean-subset claim: 63/63 clean, task success 1.0, raw leakage 0.0, and external leakage 0.0.
- The MiniMax-backed coverage supports improvement-or-tie comparisons against no-defense, static ACL, and prompt-filter on configured raw/external leakage groups.
- Prompt-filter indirect attack vulnerability is supported in the configured coverage, but only within the benchmark scope.

## Limitations and non-claims

- The real-provider evidence is MiniMax-only.
- The P1 runtime is a synthetic deterministic MAS runtime with MiniMax final-writer calls, not a full autonomous real computer-use stack.
- The evidence does not support non-MiniMax provider generalization.
- The evidence does not support production safety.
- The evidence does not support real browser or desktop agent deployment claims.
- The P0 AgentPoison evidence is an adapted comparator, not a full official AgentPoison reproduction.
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
