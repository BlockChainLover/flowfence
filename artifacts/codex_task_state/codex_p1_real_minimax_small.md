# Codex Task State: p1-real-minimax-small

## Goal

Add a minimal MiniMax-only real-model smoke path for the strengthened P1 MAS benchmark, using MiniMax only for the final vendor-facing writing step while preserving event traces, safe traces, policy decisions, and metrics.

## Branch

codex/p1-real-minimax-small

## Existing MiniMax Integration Notes

- Existing repo conventions use MiniMax provider profiles such as `minimax25` and `minimax27`.
- Existing safe config examples reference `MINIMAX_API_KEY`, `MINIMAX_BASE_URL`, `MODEL_MINIMAX25`, and `MODEL_MINIMAX27`.
- Previous provider smoke notes indicate `minimax27` maps to `MiniMax-M2.7` through an OpenAI-compatible chat-completions endpoint.
- No credentials were read from `.env` files and no credential values were printed.

## Completed

- Added a minimal MiniMax-only client wrapper that reads credentials from environment variables and returns hashed prompt/response metadata.
- Added `minimax_final_writer` runtime support for final vendor-facing writing while keeping deterministic propagation, attack, defense, and evaluation steps.
- Added explicit sweep safety: MiniMax provider calls require `provider_calls_enabled: true`, `provider: minimax`, `agent_backend: minimax_final_writer`, and the `--allow-provider-calls` CLI flag.
- Added a small 18-run MiniMax smoke matrix config.
- Updated the P1 summary reporter to distinguish deterministic synthetic evidence from MiniMax smoke evidence.
- Added no-network tests with a fake MiniMax client and safety checks for provider-call gating.

## Changed Files

- `src/runtime/minimax_client.py`
- `src/runtime/orchestrator.py`
- `src/runner/run_mas_synthetic.py`
- `src/runner/sweep_mas.py`
- `src/runner/summarize_mas_p1.py`
- `configs/experiment/mas_p1_minimax_smoke.yaml`
- `tests/test_mas_minimax_smoke_config.py`
- `artifacts/codex_task_state/codex_p1_real_minimax_small.md`

## Validation Commands

- `PYTHONPATH=. python src/runner/sweep_mas.py --help`
- `PYTHONPATH=. python src/runner/summarize_mas_p1.py --help`
- `python -m unittest tests/test_mas_minimax_smoke_config.py`
- `python -m unittest tests/test_mas_synthetic_runtime.py`
- `python -m unittest tests/test_mas_sweep_and_summary.py`
- `python -m unittest tests/test_mas_benchmark_strengthening.py`
- `python -m compileall scripts src`
- `git diff --check`
- `git status --short`
- `PYTHONPATH=. python src/runner/sweep_mas.py --config configs/experiment/mas_p1_minimax_smoke.yaml --output-root /private/tmp/flowfence_mas_p1_minimax_smoke_safety --max-runs 1`

## MiniMax Smoke Results

- Provider-call safety check passed: the sweep without `--allow-provider-calls` failed before any MiniMax request.
- Real MiniMax smoke was not executed because the local environment did not provide `MINIMAX_API_KEY`.
- Fake-client runtime test exercised the `minimax_final_writer` path and verified safe traces did not contain synthetic raw secret values.

## Known Limitations

- This is a smoke-path implementation only, not a paper-ready real-model experiment.
- The real 2-run MiniMax smoke still needs to be run in an environment with MiniMax credentials.
- MiniMax is used only for the final writer step; all propagation and defense decisions remain deterministic.
- No non-MiniMax provider generalization is supported or claimed.

## Resume Instructions

Resume from branch `codex/p1-real-minimax-small`.

First run:

- `git branch --show-current`
- `git status --short`

Then inspect:

- `configs/experiment/mas_p1_minimax_smoke.yaml`
- `src/runtime/minimax_client.py`
- `tests/test_mas_minimax_smoke_config.py`

If MiniMax credentials are available, run:

- `PYTHONPATH=. python src/runner/sweep_mas.py --config configs/experiment/mas_p1_minimax_smoke.yaml --output-root /private/tmp/flowfence_mas_p1_minimax_smoke --allow-provider-calls --max-runs 2 --force`
- `PYTHONPATH=. python src/runner/summarize_mas_p1.py --runs-root /private/tmp/flowfence_mas_p1_minimax_smoke --output-dir /private/tmp/flowfence_mas_p1_minimax_smoke_summary --matrix-config configs/experiment/mas_p1_minimax_smoke.yaml`
