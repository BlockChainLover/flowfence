# P1 Claims Refresh 4

## Inputs inspected

- `results/evidence_index/current_evidence_index.md`
- `papers/claims_checklist.md`
- `artifacts/evidence_index/p1_claims_refresh_3.md`
- `artifacts/codex_task_state/codex_p1_real_minimax_coverage_3seed.md`
- `artifacts/codex_task_state/codex_p1_real_minimax_coverage_3seed_debug.md`
- `artifacts/minimax_p1_coverage_3seed/README.md`
- `artifacts/minimax_p1_coverage_3seed/run_manifest.json`
- `artifacts/minimax_p1_coverage_3seed/coverage_summary.json`
- `artifacts/minimax_p1_coverage_3seed/coverage_summary.md`
- `artifacts/minimax_p1_coverage_3seed/coverage_by_defense.csv`
- `artifacts/minimax_p1_coverage_3seed/coverage_by_topology.csv`
- `artifacts/minimax_p1_coverage_3seed/coverage_by_attack.csv`
- `artifacts/minimax_p1_coverage_3seed/coverage_by_attack_defense.csv`
- `artifacts/minimax_p1_coverage_3seed/coverage_by_seed.csv`
- `artifacts/minimax_p1_coverage_3seed/flowfence_clean_matrix.csv`
- `artifacts/minimax_p1_coverage_3seed/failure_breakdown.jsonl`
- `artifacts/minimax_p1_coverage_3seed_debug/README.md`
- `artifacts/minimax_p1_coverage_3seed_debug/debug_summary.json`
- `artifacts/minimax_p1_coverage_3seed_debug/debug_summary.md`
- `artifacts/minimax_p1_coverage_3seed_debug/failed_run_diagnosis.json`
- `artifacts/minimax_p1_coverage_3seed_debug/retry_manifest.json`

## What changed since p1-claims-refresh-3

The prior claims refresh centered on the clean post-fix 18-run MiniMax smoke and audit. Since then, the project added MiniMax-only P1 MAS coverage over the synthetic deterministic runtime:

- 84-run one-seed coverage, now superseded for current MiniMax coverage claims.
- 252-run 3-seed coverage, initially 251/252 because of one MiniMax read timeout.
- Timeout debug/retry, which identified `chain_4 / summary_poisoning_direct / prompt_filter / seed=1` as the transient timeout run and refreshed canonical artifacts to 252/252 completed.

## 252-run MiniMax 3-seed coverage evidence

- Expected runs: 252
- Completed runs: 252
- Failed runs: 0 after retry
- Provider: MiniMax
- Provider calls enabled: true
- Agent backend: `minimax_final_writer`
- Topologies: `chain_4`, `star_4`, `blackboard_4`
- Attacks: `none`, `summary_poisoning_direct`, `summary_poisoning_indirect`, `workspace_poisoning_direct`, `workspace_poisoning_indirect`, `comm_hijack_direct`, `comm_hijack_indirect`
- Defenses: `none`, `static_acl`, `prompt_filter`, `flowfence_lite`
- Seeds: `1`, `2`, `3`

Aggregate metrics from `artifacts/minimax_p1_coverage_3seed/coverage_summary.json`:

- `task_success_rate=0.964286`
- `unauthorized_raw_leakage_mean=2.829365`
- `external_leakage_mean=0.325397`
- `cascade_size_mean=4.178571`
- `privilege_reach_mean=2.678571`
- `topology_effect_observed=true`

FlowFence subset:

- 63/63 FlowFence runs clean
- `task_success_rate=1.0`
- `unauthorized_raw_leakage_mean=0.0`
- `external_leakage_mean=0.0`
- Clean across seeds `1`, `2`, and `3`

Comparison counts:

- FlowFence vs no-defense: raw improves 42/ties 21; external improves 32/ties 31; task success improves 7/ties 56.
- FlowFence vs static ACL: raw improves 42/ties 21; external improves 30/ties 33; task success ties 63.
- FlowFence vs prompt-filter: raw improves 18/ties 45; external improves 13/ties 50; task success improves 2/ties 61.

## Timeout retry result

The original 3-seed coverage attempt completed 251/252 runs and failed one run with a MiniMax read timeout:

- Run name: `mas_p1__enterprise_assistant_001__chain_4__summary_poisoning_direct__prompt_filter__seed1`
- Topology: `chain_4`
- Attack: `summary_poisoning_direct`
- Defense: `prompt_filter`
- Seed: `1`
- Failure type: `minimax_read_timeout`

The retry used the same sweep without `--force`, skipped 251 completed runs with `metrics.json`, executed only the missing run, and refreshed canonical coverage artifacts to 252/252 completed.

## Claims now supported

- The MiniMax-only 3-seed P1 MAS coverage completed 252/252 configured runs after retrying one transient MiniMax timeout.
- In the 252-run MiniMax coverage, FlowFence-Lite was clean across all 63 configured FlowFence runs.
- In the 252-run MiniMax coverage, FlowFence-Lite improves or ties no-defense, static ACL, and prompt-filter on raw/external leakage across configured comparison groups.
- Topology effects are observed in the 252-run MiniMax synthetic-runtime benchmark.

## Claims partially supported

- MiniMax-only multi-seed synthetic-runtime robustness is supported for this configured 252-run matrix, but not beyond it.
- Simple-baseline comparison claims are supported for `none`, `static_acl`, and `prompt_filter` in this benchmark, but not for all possible defense families.
- Task-success preservation is supported for the FlowFence subset in this matrix, but not for broad real-world deployments.

## Claims still unsupported

- Non-MiniMax generalization.
- Production safety.
- Real browser, desktop, or computer-use agent evidence.
- Full official AgentPoison reproduction.
- Broad real-world robustness.
- Learned graph risk scorer evidence.
- MiniMax coverage larger than the completed 252-run matrix.
- Multi-provider real-model robustness.

## Current risk interpretation

The 252-run coverage is stronger than the earlier 18-run smoke and 84-run one-seed coverage. It supports paper-facing MiniMax synthetic-runtime claims with conservative caveats. It still must not be described as a real-world deployment, real computer-use experiment, or production agent experiment.

Raw traces, prompts, provider outputs, event JSONL, policy JSONL, and per-run metrics remain intentionally uncommitted.

## Recommended next goal

`p1-paper-tables-refresh-2`

Reason: the 252-run coverage supersedes the 18-run smoke and 84-run one-seed coverage for paper-facing MiniMax tables. The result tables should be regenerated and reviewed before drafting the results section.
