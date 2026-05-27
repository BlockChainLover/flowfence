# Codex Task State: p1-benchmark-strengthening

## Goal

Strengthen the deterministic P1 MAS benchmark so it can expose topology-dependent propagation and distinguish FlowFence-Lite from simple `static_acl` and `prompt_filter` baselines without calling any provider.

## Branch

codex/p1-benchmark-strengthening

## Diagnosis

- The previous orchestrator executed the same fixed five-event sequence for `chain_4`, `star_4`, and `blackboard_4`.
- `topology.neighbors`, `can_send`, and blackboard fanout did not affect generated events, causal parents, or artifact reads.
- Blackboard shared workspace did not produce extra fanout reads, so cascade metrics had no topology-dependent input.
- The cascade evaluator could only reflect the fixed trace it received; it was not the main blocker.
- The privilege evaluator counted blocked/quarantined contaminated paths, which could overstate contained privilege reach.
- The old attack payloads used one direct phrase family only.
- The old final-output logic made every defense except `none` automatically safe, causing `static_acl`, `prompt_filter`, and FlowFence to tie.

## Completed

- Added direct and indirect variants for summary poisoning, workspace poisoning, and communication hijack attacks.
- Made the synthetic orchestrator generate topology-dependent propagation paths:
  - `chain_4` uses sequential propagation.
  - `star_4` fans out from `planner_agent`.
  - `blackboard_4` creates shared-artifact reads by multiple agents.
- Made `static_acl` block only external raw-secret movement while allowing internal propagation.
- Made `prompt_filter` block direct prompt-injection phrases but miss indirect sensitive-detail requests.
- Kept FlowFence risk scoring sensitive to cross-principal shared artifacts, high fanout, raw secrets, and indirect sensitive-detail requests.
- Added a strengthened matrix config with direct/indirect attacks.
- Added benchmark-strengthening tests for topology effect, provider guards, leakage reduction, and safe-trace redaction.

## Changed Files

- `src/runtime/orchestrator.py`
- `src/attacks/base.py`
- `src/attacks/summary_poisoning.py`
- `src/attacks/workspace_poisoning.py`
- `src/attacks/comm_hijack.py`
- `src/defenses/mas_flowfence.py`
- `src/evaluators/privilege.py`
- `configs/experiment/mas_p1_strengthened_matrix.yaml`
- `tests/test_mas_benchmark_strengthening.py`
- `artifacts/codex_task_state/codex_p1_benchmark_strengthening.md`

## Validation Commands

- `PYTHONPATH=. python src/runner/sweep_mas.py --help`
- `PYTHONPATH=. python src/runner/summarize_mas_p1.py --help`
- `PYTHONPATH=. python src/runner/sweep_mas.py --config configs/experiment/mas_p1_strengthened_matrix.yaml --output-root /private/tmp/flowfence_mas_p1_strengthened_sweep --force`
- `PYTHONPATH=. python src/runner/summarize_mas_p1.py --runs-root /private/tmp/flowfence_mas_p1_strengthened_sweep --output-dir /private/tmp/flowfence_mas_p1_strengthened_summary --matrix-config configs/experiment/mas_p1_strengthened_matrix.yaml`
- `python -m unittest tests/test_mas_synthetic_runtime.py`
- `python -m unittest tests/test_mas_sweep_and_summary.py`
- `python -m unittest tests/test_mas_benchmark_strengthening.py`
- `python -m compileall scripts src`
- `git diff --check`
- `git status --short`

## Strengthened Sweep Results

- Expected runs: 252.
- Completed runs: 252.
- Failed runs: 0.
- Provider: `minimax`.
- Provider calls enabled: `false`.
- `topology_effect_observed`: `true`.
- No topology sanity warnings were emitted.
- Blackboard cascade size was greater than or equal to chain cascade size for every no-defense attack group.
- FlowFence improved over no-defense on unauthorized raw leakage and external leakage for 18 attack/topology groups, and tied on the 3 no-attack groups.
- FlowFence improved over prompt_filter on all 9 indirect attack/topology groups for unauthorized raw leakage, external leakage, cascade size, and privilege reach.
- FlowFence improved over static_acl on all 9 indirect groups for cascade size and privilege reach, improved on 6 of 9 indirect groups for unauthorized raw leakage, and improved on 4 of 9 indirect groups for external leakage.

## Known Limitations

- This remains deterministic synthetic evidence only.
- It does not call MiniMax or any external provider.
- Generated `/private/tmp` validation outputs are not committed.
- The strengthened benchmark supports topology-sensitive synthetic evidence, not real-model or deployment generalization.
- Static ACL still ties FlowFence on some indirect leakage metrics where both prevent external release but differ on cascade and privilege reach.

## Resume Instructions

Resume on branch `codex/p1-benchmark-strengthening`.

First run:

- `git branch --show-current`
- `git status --short`

Then inspect:

- `src/runtime/orchestrator.py`
- `src/defenses/mas_flowfence.py`
- `configs/experiment/mas_p1_strengthened_matrix.yaml`
- `tests/test_mas_benchmark_strengthening.py`

Do not start the next goal in this branch.
