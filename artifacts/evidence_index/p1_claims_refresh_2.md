# P1 Claims Refresh 2

## Inputs inspected

- `results/evidence_index/current_evidence_index.md`
- `papers/claims_checklist.md`
- `artifacts/evidence_index/p1_claims_refresh.md`
- `artifacts/codex_task_state/codex_p1_claims_refresh.md`
- `artifacts/codex_task_state/codex_p1_real_minimax_debug.md`
- `artifacts/minimax_p1_smoke/README.md`
- `artifacts/minimax_p1_smoke/run_manifest.json`
- `artifacts/minimax_p1_smoke/summary_18run.json`
- `artifacts/minimax_p1_smoke/summary_18run.md`
- `artifacts/minimax_p1_smoke_debug/README.md`
- `artifacts/minimax_p1_smoke_debug/run_manifest.json`
- `artifacts/minimax_p1_smoke_debug/debug_summary.json`
- `artifacts/minimax_p1_smoke_debug/debug_summary.md`

## What changed since p1-claims-refresh

- The pre-debug MiniMax smoke remains recorded as a small smoke with low task success (`0.055556`).
- The post-debug MiniMax debug smoke is now recorded separately.
- The debug diagnosis is now evidence-bound: low task success was primarily caused by final-writer prompt shape plus overly strict utility evaluation.
- The post-debug debug smoke improved task success to `1.0` on the saved 18-run debug matrix.
- Remaining leakage risk is still explicit: post-debug unauthorized raw leakage mean is `3.333333`, and external leakage mean is `0.222222`.

## Post-debug MiniMax evidence

- Evidence paths: `artifacts/minimax_p1_smoke_debug/debug_summary.json`, `artifacts/minimax_p1_smoke_debug/debug_summary.md`, `artifacts/minimax_p1_smoke_debug/run_manifest.json`.
- 2-run debug: completed `2`, failed `0`, `task_success_rate=1.0`, `unauthorized_raw_leakage_mean=0.0`, `external_leakage_mean=0.0`.
- 18-run debug: completed `18`, failed `0`, `task_success_rate=1.0`, `unauthorized_raw_leakage_mean=3.333333`, `external_leakage_mean=0.222222`, `cascade_size_mean=3.333333`, `privilege_reach_mean=2.222222`.
- Scope: MiniMax-only final-writer debug smoke. Propagation, attack injection, policy decisions, and evaluation remain deterministic.
- Boundary: not a full real-model experiment and not evidence for non-MiniMax generalization.

## Claims now supported

- The initial low MiniMax task success was primarily a prompt/evaluator issue, not missing or empty final outputs.
- After minimal prompt/evaluator fixes, the MiniMax 18-run debug smoke completed with `task_success_rate=1.0`.
- The current post-debug summaries are safe high-level artifacts; raw traces and provider outputs remain intentionally uncommitted.

## Claims partially supported

- MiniMax final-writer task success is plausible after the debug fix, but only within the small 18-run debug smoke.
- MiniMax leakage reduction remains smoke-level evidence only.
- MiniMax topology observations remain smoke-level evidence only.

## Claims still unsupported

- Broad real-model robustness.
- Non-MiniMax provider generalization.
- Full paper-ready MiniMax MAS evidence.
- Broad superiority over all baselines.
- Utility preservation under broad real-model settings.
- Official AgentPoison reproduction.
- Real-model multi-seed robustness.
- Full 252-run real MiniMax matrix.

## Current risk interpretation

The post-debug run removes the immediate task-success blocker for the MiniMax final-writer path, but it does not solve the real-model evidence problem. Leakage remains non-zero in the post-debug 18-run debug smoke, and the evidence is still small, one-seed, and MiniMax-only.

## Recommended next goal

`p1-real-minimax-18run-rerun`

Reason: the debug run improved task success, but it is better to run a clean post-fix 18-run smoke and summarize it as the official post-debug MiniMax smoke evidence before expanding coverage.
