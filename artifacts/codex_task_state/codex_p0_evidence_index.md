# Codex Task State: p0-evidence-index

## Goal

Create the P0 evidence index for the current FlowFence-Lite AgentPoison retrieval-memory containment axis.

## Branch

codex/p0-evidence-index

## Completed

- Read and followed `AGENTS.md`.
- Created `results/evidence_index/current_evidence_index.md`.
- Indexed only existing checklist and summary artifacts.
- Separated supported, partially supported, unsupported, and forbidden claims.
- Kept the evidence scope MiniMax-only and P0 retrieval-memory-only.
- Did not run experiments, edit implementation code, edit results, edit paper drafts, or modify research logs.

## Changed Files

- `results/evidence_index/current_evidence_index.md`
- `artifacts/codex_task_state/codex_p0_evidence_index.md`

## Evidence Inspected

- `papers/claims_checklist.md`
- `results/baseline_agentpoison_fullreact_minimax27_small_matrix_summary.json`
- `results/ablation_agentpoison_fullreact_minimax27_quarantine_only_vs_actioncanon_summary.json`
- `results/baseline_agentpoison_fullreact_minimax27_rewrite_only_weak_comparator_summary.json`
- `results/baseline_agentpoison_fullreact_minimax27_static_keyword_filter_weak_comparator_summary.json`
- `results/baseline_agentpoison_fullreact_minimax27_heldout_instruction_matrix_summary.json`
- `results/overhead_agentpoison_fullreact_minimax27_same_axis_measured_summary.json`
- `results/overhead_agentpoison_fullreact_minimax27_same_axis_proxy_summary.json`
- `results/baseline_agentdojo_minimax27_axis_switch_attempt_summary.json`
- `results/baseline_agentdojo_minimax27_banking_stable_pair_search_summary.json`
- `results/baseline_agentdojo_minimax27_banking_selected_native_defenses_summary.json`

## Validation Commands

- `git diff --check`
- `python -m compileall src scripts || true`
- `git status --short`

## Known Limitations

- This task is documentation/evidence-indexing only.
- It does not create P0 eventization adapters.
- It does not recompute metrics from event traces.
- It does not export failure cases.
- It does not validate raw logs or raw trajectories.
- It does not create P1 multi-agent propagation runtime evidence.

## Resume Instructions

Resume on branch `codex/p0-evidence-index`.

First run:

- `git branch --show-current`
- `git status --short`

Then inspect:

- `results/evidence_index/current_evidence_index.md`
- `artifacts/codex_task_state/codex_p0_evidence_index.md`

Do not start eventization in this branch.
