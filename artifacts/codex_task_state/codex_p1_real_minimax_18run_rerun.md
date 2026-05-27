# Codex Task State: p1-real-minimax-18run-rerun

## Goal

Run a clean post-debug MiniMax 18-run smoke after the final-writer prompt and utility-evaluator fixes, then commit only high-level redacted summaries and a run manifest.

## Branch

codex/p1-real-minimax-18run-rerun

## Credential Availability Check

- Local `MINIMAX_API_KEY`: absent.
- Local `MINIMAX_BASE_URL`: absent.
- Local `MODEL_MINIMAX27`: absent.
- Local `MINIMAX_MODEL`: absent.
- Local `MINIMAX_GROUP_ID`: absent.
- Remote `MINIMAX_API_KEY`: present.
- Remote `MINIMAX_BASE_URL`: present.
- Remote `MODEL_MINIMAX27`: present.
- Remote `MINIMAX_MODEL`: absent.
- Remote `MINIMAX_GROUP_ID`: absent.

Credential values were not printed or copied.

## Config Check

- Config path: `configs/experiment/mas_p1_minimax_smoke.yaml`
- Expected run count: `18`
- Topologies: `chain_4`, `blackboard_4`
- Attacks: `none`, `summary_poisoning_indirect`, `workspace_poisoning_indirect`
- Defenses: `none`, `prompt_filter`, `flowfence_lite`
- Seeds: `1`
- Provider: `minimax`
- Provider calls enabled: `true`
- Agent backend: `minimax_final_writer`

## Provider-call Safety Check

- Command: `PYTHONPATH=. python src/runner/sweep_mas.py --config configs/experiment/mas_p1_minimax_smoke.yaml --output-root /tmp/flowfence_mas_p1_postfix_safety --max-runs 1`
- Expected: fail before any MiniMax request because `--allow-provider-calls` is absent.
- Observed: failed as expected with `provider_calls_enabled=true requires --allow-provider-calls before any MiniMax request`.

## Two-run Post-fix Smoke Result

- Executed: yes.
- Output root: `/tmp/flowfence_mas_p1_postfix_2run`
- Summary root: `/tmp/flowfence_mas_p1_postfix_2run_summary`
- Completed runs: `2`
- Failed runs: `0`
- Task success rate: `1.0`
- Unauthorized raw leakage mean: `0.0`
- External leakage mean: `0.0`
- Cascade size mean: `0.0`
- Privilege reach mean: `0.0`

## Eighteen-run Post-fix Smoke Result

- Executed: yes.
- Output root: `/tmp/flowfence_mas_p1_postfix_18run`
- Summary root: `/tmp/flowfence_mas_p1_postfix_18run_summary`
- Completed runs: `18`
- Failed runs: `0`
- Task success rate: `0.888889`
- Unauthorized raw leakage mean: `4.111111`
- External leakage mean: `0.444444`
- Cascade size mean: `3.333333`
- Privilege reach mean: `2.222222`
- Topology effect observed: `true`
- FlowFence-Lite defense slice: `task_success_rate=1.0`, `unauthorized_raw_leakage_mean=0.0`, `external_leakage_mean=0.0`.
- Prompt-filter defense slice: `task_success_rate=0.666667`, `unauthorized_raw_leakage_mean=7.333333`, `external_leakage_mean=1.0`.

## Committed Evidence Files

- `artifacts/minimax_p1_smoke_postfix/README.md`
- `artifacts/minimax_p1_smoke_postfix/run_manifest.json`
- `artifacts/minimax_p1_smoke_postfix/summary_2run.json`
- `artifacts/minimax_p1_smoke_postfix/summary_2run.md`
- `artifacts/minimax_p1_smoke_postfix/summary_18run.json`
- `artifacts/minimax_p1_smoke_postfix/summary_18run.md`
- `artifacts/codex_task_state/codex_p1_real_minimax_18run_rerun.md`

## Validation Commands

- `PYTHONPATH=. python src/runner/sweep_mas.py --help`
- `PYTHONPATH=. python src/runner/summarize_mas_p1.py --help`
- `python -m unittest tests/test_mas_minimax_smoke_config.py`
- `python -m unittest tests/test_mas_minimax_debug.py`
- `python -m compileall scripts src`
- `git diff --check`
- `git status --short`

## Known Limitations

- This is still a small MiniMax-only smoke, not a full real-model experiment.
- The overall post-fix task success rate is `0.888889`, so the prior debug-smoke `1.0` result did not fully reproduce at aggregate level.
- The FlowFence-Lite subset is clean on task success and leakage in this smoke, but broad real-model robustness is not supported.
- Raw traces, prompts, provider outputs, provider logs, event JSONL files, policy JSONL files, individual metrics, credentials, and secrets were not committed.

## Resume Instructions

Resume from branch `codex/p1-real-minimax-18run-rerun`.

First run:

- `git branch --show-current`
- `git status --short`

Then inspect:

- `artifacts/minimax_p1_smoke_postfix/summary_18run.json`
- `artifacts/minimax_p1_smoke_postfix/summary_18run.md`
- `artifacts/minimax_p1_smoke_postfix/run_manifest.json`

Recommended next goal: `p1-real-minimax-debug-2` if investigating the aggregate task-success regression, or `p1-claims-refresh-3` if only updating evidence docs.
