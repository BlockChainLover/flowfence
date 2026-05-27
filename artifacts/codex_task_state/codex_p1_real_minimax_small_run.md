# Codex Task State: p1-real-minimax-small-run

## Goal

Run the MiniMax-only P1 MAS smoke on `wentian-server` using the implemented `minimax_final_writer` path, committing only small high-level evidence summaries and task state without raw traces or provider outputs.

## Branch

codex/p1-real-minimax-small-run

## Credential Availability Check

- Local `MINIMAX_API_KEY`: absent.
- Remote `.secrets/providers.env`: present.
- Remote `MINIMAX_API_KEY`: present.
- Remote `MINIMAX_BASE_URL`: present.
- Remote `MODEL_MINIMAX27`: present.
- Remote `MINIMAX_GROUP_ID`: not checked; optional for this smoke path.
- No credential values were printed, copied, or committed.

## Provider-call Safety Check

- Command: `PYTHONPATH=. python3 src/runner/sweep_mas.py --config configs/experiment/mas_p1_minimax_smoke.yaml --output-root /tmp/flowfence_mas_p1_minimax_smoke_safety --max-runs 1`
- Expected result: fail before any MiniMax request because `--allow-provider-calls` is not set.
- Observed result: failed as expected.

## Two-run Smoke Result

- Executed: yes.
- Output root: `/tmp/flowfence_mas_p1_minimax_smoke_2run`.
- Summary root: `/tmp/flowfence_mas_p1_minimax_smoke_2run_summary`.
- Completed runs: 2.
- Failed runs: 0.
- Scope: `chain_4`, attack `none`, defenses `none` and `prompt_filter`, seed `1`.
- Aggregate metrics: task success rate `0.5`, unauthorized raw leakage mean `0.0`, external leakage mean `0.0`, cascade size mean `0.0`, privilege reach mean `0.0`.

## Eighteen-run Smoke Result

- Executed: yes.
- Output root: `/tmp/flowfence_mas_p1_minimax_smoke_18run`.
- Summary root: `/tmp/flowfence_mas_p1_minimax_smoke_18run_summary`.
- Completed runs: 18.
- Failed runs: 0.
- Scope: topologies `chain_4` and `blackboard_4`; attacks `none`, `summary_poisoning_indirect`, and `workspace_poisoning_indirect`; defenses `none`, `prompt_filter`, and `flowfence_lite`; seed `1`.
- Aggregate metrics: task success rate `0.055556`, unauthorized raw leakage mean `4.111111`, external leakage mean `0.666667`, cascade size mean `3.333333`, privilege reach mean `2.222222`.
- Topology effect observed: true.
- FlowFence vs no-defense: improves on unauthorized raw leakage in 4 groups, ties in 2 no-attack groups; improves on external leakage in 4 groups, ties in 2 no-attack groups.
- FlowFence vs prompt-filter: improves on unauthorized raw leakage in 4 groups, ties in 2 no-attack groups; improves on external leakage in 2 groups, ties in 4 groups.

## Committed Evidence Files

- `artifacts/minimax_p1_smoke/README.md`
- `artifacts/minimax_p1_smoke/summary_2run.json`
- `artifacts/minimax_p1_smoke/summary_2run.md`
- `artifacts/minimax_p1_smoke/summary_18run.json`
- `artifacts/minimax_p1_smoke/summary_18run.md`
- `artifacts/minimax_p1_smoke/run_manifest.json`
- `artifacts/codex_task_state/codex_p1_real_minimax_small_run.md`

## Validation Commands

- `PYTHONPATH=. python src/runner/sweep_mas.py --help`
- `PYTHONPATH=. python src/runner/summarize_mas_p1.py --help`
- `python -m unittest tests/test_mas_minimax_smoke_config.py`
- `python -m compileall scripts src`
- Remote safety check listed above.
- Remote two-run MiniMax smoke.
- Remote eighteen-run MiniMax smoke.
- `git diff --check`
- `git status --short`

## Known Limitations

- This is a small MiniMax smoke, not a full real-model experiment.
- Raw traces, prompts, provider outputs, event JSONL files, policy-decision JSONL files, and per-run metrics are intentionally not committed.
- The remote Linux host used `/tmp` rather than `/private/tmp`.
- The 2-run subset is only a connectivity/smoke gate and does not include FlowFence.
- The 18-run smoke uses only two topologies, two attack families plus the no-attack control, three defenses, and one seed.
- No non-MiniMax provider generalization is supported.

## Resume Instructions

Resume from branch `codex/p1-real-minimax-small-run`.

First run:

- `git branch --show-current`
- `git status --short`

Then inspect:

- `artifacts/minimax_p1_smoke/run_manifest.json`
- `artifacts/minimax_p1_smoke/summary_18run.json`
- `artifacts/minimax_p1_smoke/summary_18run.md`

Do not commit raw run directories from `/tmp` or any provider output.
