# P1 Claims Refresh

## Inputs inspected

- `results/evidence_index/current_evidence_index.md`
- `papers/claims_checklist.md`
- `artifacts/codex_task_state/codex_p1_mas_sweep.md`
- `artifacts/codex_task_state/codex_p1_benchmark_strengthening.md`
- `artifacts/codex_task_state/codex_p1_real_minimax_small.md`
- `artifacts/codex_task_state/codex_p1_real_minimax_small_run.md`
- `artifacts/minimax_p1_smoke/README.md`
- `artifacts/minimax_p1_smoke/run_manifest.json`
- `artifacts/minimax_p1_smoke/summary_2run.json`
- `artifacts/minimax_p1_smoke/summary_2run.md`
- `artifacts/minimax_p1_smoke/summary_18run.json`
- `artifacts/minimax_p1_smoke/summary_18run.md`

## What is now supported

- The strengthened deterministic synthetic MAS benchmark supports topology-dependent propagation in the synthetic runtime only.
- In the strengthened deterministic synthetic MAS benchmark, FlowFence-Lite improves over `prompt_filter` on indirect attacks for unauthorized raw leakage, external leakage, cascade size, and privilege reach.
- The MiniMax final-writer smoke path runs end-to-end: the 18-run smoke completed 18/18 runs with 0 failures.

## What is partially supported

- In the MiniMax 18-run smoke, FlowFence-Lite reduces unauthorized raw leakage versus no-defense in 4/6 comparison groups and ties in 2/6.
- In the MiniMax 18-run smoke, FlowFence-Lite reduces external leakage versus no-defense in 4/6 comparison groups and ties in 2/6.
- In the MiniMax 18-run smoke, topology effect was observed.
- These MiniMax observations are smoke evidence only because the matrix is small, uses one seed, and has low task success.

## What remains unsupported

- Broad real-model robustness.
- Non-MiniMax provider generalization.
- Full paper-ready MiniMax MAS evidence.
- Broad superiority over all simple or independent baseline families.
- Topology claims beyond the deterministic synthetic benchmark and the small MiniMax smoke.
- Utility preservation under real MiniMax MAS execution.
- Full official AgentPoison reproduction.

## MiniMax smoke interpretation

The MiniMax 18-run smoke is useful as an engineering and evidence-quality checkpoint. It shows that the `minimax_final_writer` path can run with MiniMax and produce aggregate leakage/cascade/privilege summaries without committing raw traces or provider outputs.

The smoke should not be presented as a full real-model experiment. The scope is limited to `chain_4` and `blackboard_4`, attacks `none`, `summary_poisoning_indirect`, and `workspace_poisoning_indirect`, defenses `none`, `prompt_filter`, and `flowfence_lite`, and seed `1`.

## Low task-success risk

The 18-run MiniMax smoke has task success `0.055556`. This is the main blocker before expanding real MiniMax coverage. The next step should inspect failure cases locally without committing raw traces, then determine whether the issue is the final-writer prompt, the task-success evaluator, or the runtime context.

## Recommended next goal

`p1-real-minimax-debug`

Reason: the 18-run MiniMax smoke completed, but task success is only `0.055556`, so before expanding coverage we need to diagnose whether the final-writer prompt, task-success evaluator, or runtime context is too strict or broken.
