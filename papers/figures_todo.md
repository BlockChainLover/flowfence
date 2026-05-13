# Figures And Tables Todo

Track only assets that answer a concrete research or paper decision.

## Current Draft Target

- active draft: `papers/icde2027_flowfence/main.tex`
- current target: ICDE 2027 paper strengthening around adapted AgentPoison MiniMax retrieval-memory containment as runtime data governance for agentic retrieval pipelines
- weak comparator status: same-axis rewrite-only comparator completed and summarized

| asset | message | source data path | type | status |
| --- | --- | --- | --- | --- |
| AgentPoison MiniMax result table | Does retrieval-memory interception contain poisoned retrieval on the adapted full-ReAct MiniMax axis, and what do static filtering, rewrite-only, quarantine, and action-canon add? | `papers/result_table_agentpoison_minimax.md`; `results/baseline_agentpoison_fullreact_minimax27_small_matrix_summary.json`; `results/baseline_agentpoison_fullreact_minimax27_static_keyword_filter_weak_comparator_summary.json`; `results/baseline_agentpoison_fullreact_minimax27_rewrite_only_weak_comparator_summary.json`; `results/ablation_agentpoison_fullreact_minimax27_quarantine_only_vs_actioncanon_summary.json` | table | drafted |
| Held-out instruction stress-test table | Does an old-phrase non-oracle static keyword filter fail when the poisoned guidance is paraphrased, and does FlowFence-Lite still contain exposure? | `results/baseline_agentpoison_fullreact_minimax27_heldout_instruction_matrix_summary.json`; `papers/result_table_agentpoison_minimax.md` | table | drafted, 3-run same-trigger stress-test caveat |
| AgentPoison MiniMax overhead proxy table | What execution-cost proxies are visible from existing same-axis traces? | `papers/overhead_agentpoison_minimax.md`; `results/overhead_agentpoison_fullreact_minimax27_same_axis_proxy_summary.json` | table | drafted |
| AgentPoison MiniMax measured overhead slice | What measured wall-clock and provider-token overhead appears on a fixed same-axis slice? | `papers/overhead_agentpoison_minimax_measured.md`; `results/overhead_agentpoison_fullreact_minimax27_same_axis_measured_summary.json` | table | drafted |
| Claims/evidence checklist | Which claims are paper-ready and what caveats must be attached? | `papers/claims_checklist.md` | table | drafted |
| AgentDojo auxiliary evidence table | Why is AgentDojo reported as stochastic/blocked rather than a stable main baseline? | `results/baseline_agentdojo_minimax27_axis_switch_attempt_summary.json`; `results/baseline_agentdojo_minimax27_banking_stable_pair_search_summary.json`; `results/baseline_agentdojo_minimax27_banking_selected_native_defenses_summary.json` | appendix table | ready to draft if needed |
| System boundary and containment diagram | Where does FlowFence-Lite intervene between poisoned retrieval and model-visible ReAct context? | `papers/icde2027_flowfence/main.tex`; `papers/icde2027_flowfence/figures/flowfence_architecture.png`; `papers/experiment_narrative_agentpoison_minimax.md` | figure | inserted as current placeholder; needs publication-quality redraw |
| Main result bar chart | Are leakage reductions bought at acceptable utility cost on the adapted AgentPoison axis? | `results/baseline_agentpoison_fullreact_minimax27_small_matrix_summary.json`; `results/baseline_agentpoison_fullreact_minimax27_rewrite_only_weak_comparator_summary.json`; `results/ablation_agentpoison_fullreact_minimax27_quarantine_only_vs_actioncanon_summary.json` | plot | optional but high value |
| Topology sensitivity plot | Does topology change cascade size or privilege reach? | `TODO` | plot | blocked on multi-topology runs |
| Error analysis table | Which channels and policies still fail? | `TODO` | table | blocked on manual case inspection |

## Figure 1 Requirements

- show retrieval backend / poisoned memory
- show raw retrieved items before defense processing
- show FlowFence-Lite quarantine decision
- show model-visible ReAct context after defense processing
- show final answer/action
- emphasize the measured distinction between `raw poisoned retrieval` and `exposed poisoned retrieval`

## Full-Paper Optional Experiment

- experiment: proceed to paper polish, unless choosing a broader attack/topology generalization experiment
- reason: rewrite-only comparator is complete, independent static keyword filter comparator is complete, same-axis overhead proxy is complete, strict measured overhead exists for a fixed 10-question slice, and a 3-run held-out poisoned-instruction stress test now shows non-oracle static-filter brittleness
- keep fixed: task manifest `data/tasks/agentpoison_strategyqa_fullreact_v1.json`
- keep fixed: provider `minimax27`
- keep fixed: attack setting `trigger_question_only`
- keep fixed: three-run reporting policy
- completed proxy: `results/overhead_agentpoison_fullreact_minimax27_same_axis_proxy_summary.json`
- completed measured slice: `results/overhead_agentpoison_fullreact_minimax27_same_axis_measured_summary.json`
- completed independent weak comparator: `results/baseline_agentpoison_fullreact_minimax27_static_keyword_filter_weak_comparator_summary.json`
- completed held-out stress test: `results/baseline_agentpoison_fullreact_minimax27_heldout_instruction_matrix_summary.json`
- current full-paper draft: `papers/icde2027_flowfence/main.tex`
- remaining caveat: the measured overhead slice is smaller than the main 25-question matrix and is trajectory-confounded
- remaining caveat: the held-out instruction stress test is now three runs per condition, but still keeps the same trigger sequence and adapted retrieval anchor, so it is not broad generalization evidence
