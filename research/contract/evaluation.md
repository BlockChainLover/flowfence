# Evaluation

- target datasets:
  Synthetic but realistic task suites in three MVP domains remain the broader MVP target, but the locked pre-method slice is `StrategyQA` from the official `AgentPoison` `ReAct-StrategyQA` assets with the fixed manifest at `data/tasks/agentpoison_strategyqa_premethod_v2.json`.
- split definition:
  For the first defense check, use the fixed `train` split subset defined in `data/tasks/agentpoison_strategyqa_premethod_v2.json` with question indices `[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]`, provider profile `qwen36`, and the frozen comparison seed list `[1, 2]`. Do not change this subset or metric set silently once method runs begin.
- primary metrics:
  Unauthorized raw leakage, unauthorized abstract leakage, cascade size, privilege reach, utility retention.
- secondary metrics:
  Containment delay, latency overhead, token overhead, false block rate, benign quarantine rate.
- pre-method comparison metrics:
  `baseline_faithfulness.benign_exact_match_rate`, `baseline_faithfulness.adv_exact_match_rate`, `baseline_faithfulness.attack_manifested_rate`, `future_defense_metrics.clean_utility_rate`, `future_defense_metrics.attacked_utility_rate`, `future_defense_metrics.attack_manifestation_rate`, and `future_defense_metrics.poisoned_retrieval_case_rate`.
- pre-method rerun policy:
  Use exactly 3 reruns on the same fixed manifest. The method-start reference artifact is the rerun aggregate summary, which must report mean/min/max for `clean_utility_rate`, `attacked_utility_rate`, `attack_manifestation_rate`, `poisoned_retrieval_case_rate`, and `poisoned_retrieval_gap_mean`.
- required baselines:
  Attack baselines: prompt injection, memory poisoning, summary poisoning, workspace poisoning.
  Defense baselines: no defense, prompt filter, static ACL, topology guard, data minimizer.
  Runtime baselines: flat shared scratchpad, per-agent private memory, shared retrieval memory.
- minimum comparison standard:
  At least one baseline must have a source paper or repo, runnable instructions, fixed split/metrics, a saved result artifact under `results/`, and an explicit mismatch note if reproduction diverges from the original setup.
- locked pre-method comparator:
  The first method-facing baseline is the adapted narrow `AgentPoison` slice defined above. `ASB` remains exploratory scaffolding and is not required before the first proposed-defense check.
