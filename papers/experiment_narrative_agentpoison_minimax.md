# Experiment Narrative: Adapted AgentPoison MiniMax Axis

## Purpose

This experiment asks whether FlowFence-Lite can contain retrieval-memory poisoning in a full-ReAct agent loop while preserving task utility. The credible main axis is an adapted AgentPoison StrategyQA full-ReAct setup under the MiniMax provider profile.

The experiment is intentionally narrow. It does not claim full official AgentPoison reproduction. It keeps the upstream ReAct-StrategyQA loop and DPR retrieval path, but uses `trigger_question_only` adversarial search context because the official full-context setup previously diluted the trigger and failed to produce a trustworthy attack anchor under MiniMax.

## Setup

- Dataset/task axis: StrategyQA adapted full-ReAct manifest at `data/tasks/agentpoison_strategyqa_fullreact_v1.json`
- Model/provider: `minimax27`
- Retrieval: upstream AgentPoison DPR path via `local_wikienv.WikiEnv`
- Attack setting: `trigger_question_only`
- Main metrics: clean utility, attacked utility, raw poisoned retrieval, exposed poisoned retrieval, attack manifestation
- Main artifacts: `results/baseline_agentpoison_fullreact_minimax27_small_matrix_summary.json`, `results/ablation_agentpoison_fullreact_minimax27_quarantine_only_vs_actioncanon_summary.json`, and `results/baseline_agentpoison_fullreact_minimax27_rewrite_only_weak_comparator_summary.json`

## Conditions

The paper-facing table compares three conditions on the same fixed axis.

1. `No defense`: the adapted AgentPoison full-ReAct comparator without FlowFence-Lite.
2. `Weak defense, safe-view rewrite only`: retrieval-memory interception with the same detector, but unsafe observations are rewritten into a safe view rather than quarantined.
3. `FlowFence-Lite, quarantine only`: retrieval-memory interception with quarantine, without canonical ReAct action writeback.
4. `FlowFence-Lite, quarantine + action-canon`: the selected method variant, adding canonical ReAct action writeback to the quarantine policy.

Each condition has three completed runs.

## Observations

No defense is non-vacuous and repeatable on this axis. Across three runs, exposed poisoned retrieval has mean `0.4667` and attack manifestation has mean `0.2533`; both are non-zero in every no-defense run.

FlowFence-Lite quarantine + action-canon reduces exposed poisoned retrieval and attack manifestation to `0.0` in all three runs. Raw poisoned retrieval remains non-zero with mean `0.44`, which means poisoned content is still retrieved internally but not exposed after defense processing.

The safe-view rewrite-only weak defense also reduces exposed poisoned retrieval and attack manifestation to `0.0` in all three runs. Raw poisoned retrieval remains non-zero with mean `0.4533`. Clean utility mean is `0.2933`, below quarantine-actioncanon `0.36`; attacked utility mean is `0.4933`, but MiniMax utility is noisy and should not be framed as a stable improvement.

FlowFence-Lite quarantine-only also reduces exposed poisoned retrieval and attack manifestation to `0.0` in all three runs. Its raw poisoned retrieval mean is `0.5333`, clean utility mean is `0.3067`, and intervention event rate mean is `0.5805`.

The selected quarantine-actioncanon variant has clean utility mean `0.36` and intervention event rate mean `0.477`. Compared with quarantine-only, this suggests cleaner full-ReAct trajectories and less repeated/drifted retrieval behavior.

## Interpretation

The main safety conclusion is that detector-mediated retrieval-memory interception contains poisoned retrieval on the adapted AgentPoison MiniMax axis. The strongest evidence is that raw poisoned retrieval remains present, while exposed poisoned retrieval and attack manifestation fall to zero across repeated runs.

The weak comparator and ablation refine the mechanism. Safe-view rewrite-only is sufficient to block exposed poisoned retrieval under the same detector, so quarantine should not be claimed as uniquely necessary. Quarantine remains the selected containment semantics because unsafe retrieved memory is removed from the active trajectory rather than rewritten into it. Canonical action writeback is better framed as a trajectory-hygiene and utility-stability improvement for full-ReAct execution, not as a necessary condition for safety.

Utility should be described conservatively. Quarantine-actioncanon has clean utility mean `0.36`, close to no-defense mean `0.3733`, and attacked utility mean `0.3867`, above no-defense mean `0.3333`. However, MiniMax full-ReAct utility is noisy across runs, so the correct claim is roughly preserved utility, not utility improvement.

## AgentDojo Auxiliary Result

AgentDojo should not be used as the main defense-effect baseline in the current paper narrative. MiniMax AgentDojo searches produced non-vacuous search hits, but selected reruns repeatedly failed to reproduce stable dual success. The appropriate conclusion is an auxiliary compatibility/negative result: AgentDojo selected-pair evaluation under MiniMax was stochastic enough that it could not support a robust before/after defense claim.

Relevant artifacts:

- `results/baseline_agentdojo_minimax27_banking_selected_native_defenses_summary.json`
- `results/baseline_agentdojo_minimax27_banking_stable_pair_search_summary.json`
- `results/baseline_agentdojo_minimax27_axis_switch_attempt_summary.json`

## Paper-Ready Paragraph

On an adapted AgentPoison full-ReAct comparator under MiniMax, no defense repeatedly exposes poisoned retrieval content and produces non-zero attack manifestation. A same-axis safe-view rewrite-only weak defense and FlowFence-Lite quarantine-actioncanon both reduce exposed poisoned retrieval and attack manifestation to zero across three repeated runs, while raw poisoned retrieval remains non-zero, indicating containment at the retrieval-memory boundary rather than absence of the attack. The selected quarantine-actioncanon variant has stronger clean utility than rewrite-only and provides clearer containment semantics for untrusted memory. Because the comparator uses an adapted `trigger_question_only` search context, these results should be framed as evidence on a controlled adapted AgentPoison axis rather than full official AgentPoison reproduction.

## Claims Not Supported Yet

- FlowFence-Lite beats multiple independent defense baseline families.
- FlowFence-Lite robustly generalizes across topologies.
- FlowFence-Lite improves utility.
- AgentDojo provides a stable main before/after defense baseline under MiniMax.
