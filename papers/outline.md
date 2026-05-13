# Paper Outline

## Working Title

FlowFence-Lite: Runtime Privacy Containment for Multi-Agent LLM Systems

## Core Problem

- Multi-agent privacy leakage is not only a final-output problem; it propagates through internal channels such as messages, memory, shared workspaces, and tool arguments.
- Shared artifacts and cross-agent coordination create failure modes that narrow prompt-only or static permission defenses do not fully address.

## Main Hypothesis

- A unified runtime containment layer can reduce unauthorized leakage and propagation better than strong narrow baselines with modest utility loss.

## Method Summary

- Current selected method variant for the paper-facing adapted AgentPoison axis:
  FlowFence-Lite retrieval-memory quarantine plus canonical ReAct action writeback.
- Mechanism supported by ablation:
  quarantine is the core safety mechanism; canonical action writeback improves full-ReAct trajectory hygiene and clean utility stability.
- Current writing rule:
  keep method claims scoped to the adapted AgentPoison MiniMax full-ReAct comparator unless new independent baselines are added.

## Experimental Setup

- Current main empirical axis:
  adapted AgentPoison StrategyQA full-ReAct comparator under MiniMax.
- Task manifest:
  `data/tasks/agentpoison_strategyqa_fullreact_v1.json`.
- Provider:
  `minimax27`.
- Attack setting:
  `trigger_question_only` adversarial search context.
- Primary paper-facing metrics on this axis:
  exposed poisoned retrieval, raw poisoned retrieval, attack manifestation, clean utility, attacked utility, intervention event rate.
- Main comparison:
  no defense vs FlowFence-Lite quarantine-only vs FlowFence-Lite quarantine + action-canon.
- Auxiliary evidence:
  AgentDojo under MiniMax is reported as stochastic/blocked because selected reruns did not provide a stable before/after anchor.

## Main Results

- Table 1: adapted AgentPoison MiniMax main result and ablation, sourced from `papers/result_table_agentpoison_minimax.md`.
- Table 2: claim/evidence/caveat mapping, sourced from `papers/claims_checklist.md`.
- Figure 1: system overview and channel instrumentation.
- Figure 2: optional privacy-utility bar chart from `results/baseline_agentpoison_fullreact_minimax27_small_matrix_summary.json` and `results/ablation_agentpoison_fullreact_minimax27_quarantine_only_vs_actioncanon_summary.json`.
- Appendix table: AgentDojo MiniMax stochastic/blocked evidence.
- Deferred: topology sensitivity, cascade comparison, and broad benchmark matrix.

## Limitations

- MVP is text-first and simulated.
- Multimodal attacks and OS-level compromise are out of scope.
- Current main result uses an adapted AgentPoison comparator, not full official AgentPoison reproduction.
- The main result is one provider/model axis: `minimax27`.
- AgentDojo results cannot support robust defense-effect claims because selected-pair reruns were unstable.
- Utility is noisy under MiniMax full-ReAct execution; claim roughly preserved utility, not utility improvement.
- Claims must remain narrower than the evidence from saved artifacts.

## Next Missing Pieces

- Optional weak defense comparator on the same adapted AgentPoison axis, such as rewrite-only or safe-view rewrite.
- Concrete runtime overhead measurements.
- Held-out robustness across attacks, providers, or topologies.
- Broader baseline families if the paper target requires stronger external comparison.
