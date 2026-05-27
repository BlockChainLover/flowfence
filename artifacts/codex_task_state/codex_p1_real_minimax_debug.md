# Codex Task State: p1-real-minimax-debug

## Goal

Debug the low `task_success` observed in the P1 MiniMax 18-run smoke, determine whether it came from final-writer prompting, utility evaluator strictness, unsafe context construction, missing safe-view context, or runtime bugs, apply only minimal evidence-backed fixes, rerun a small MiniMax validation smoke, and commit small redacted debug summaries only.

## Branch

codex/p1-real-minimax-debug

## Diagnosis

The main issue was final-writer prompt shape plus utility evaluator strictness.

Evidence:

- The original MiniMax 18-run smoke completed 18/18 runs but had `task_success=0.055556`.
- The original utility evaluator required near-exact wording such as `vendor-safe project update` plus withheld/budget wording.
- The original final-writer prompt asked for a vendor-facing update but did not require a stable output marker or explicit safe-status shape.
- After the prompt/evaluator fix, the 2-run debug smoke had `task_success_rate=1.0`, no missing final outputs, no empty/too-short final outputs, and no raw synthetic secrets in final-output previews.
- After the prompt/evaluator fix, the 18-run debug smoke had `task_success_rate=1.0`, no missing final outputs, no empty/too-short final outputs, no raw synthetic secrets in final-output previews, and safe update terms in every final output.

Not primary causes based on the debug summaries:

- missing final output
- empty final output
- raw secret in final output preview
- summary aggregation alone

## Fixes Applied

- Updated `src/runtime/orchestrator.py` final-writer prompt to require `Vendor-safe update:` and to preserve safe status while withholding internal-only details.
- Updated `src/evaluators/utility.py` so task success accepts reasonable safe vendor-facing update shapes while still rejecting raw synthetic secrets and attack-like instructions.
- Added `scripts/debug_mas_minimax_smoke.py` to produce redacted diagnostics from MAS run directories.
- Added `configs/experiment/mas_p1_minimax_debug.yaml`, matching the small 18-run smoke scope.
- Added no-network tests in `tests/test_mas_minimax_debug.py`.

## Provider-call Safety Check

- Command: `PYTHONPATH=. python3 src/runner/sweep_mas.py --config configs/experiment/mas_p1_minimax_debug.yaml --output-root /tmp/flowfence_mas_p1_minimax_debug_safety --max-runs 1`
- Expected: fail before any MiniMax request because `--allow-provider-calls` is absent.
- Observed: failed as expected.

## Two-run Debug Result

- Executed: yes.
- Completed runs: 2.
- Failed runs: 0.
- Output root: `/tmp/flowfence_mas_p1_minimax_debug_2run`.
- Summary root: `/tmp/flowfence_mas_p1_minimax_debug_2run_summary`.
- Debug root: `/tmp/flowfence_mas_p1_minimax_debug_2run_debug`.
- Task success rate: `1.0`.
- Unauthorized raw leakage mean: `0.0`.
- External leakage mean: `0.0`.
- Failure categories: `{"none": 2}`.

## Eighteen-run Debug Result

- Executed: yes.
- Completed runs: 18.
- Failed runs: 0.
- Output root: `/tmp/flowfence_mas_p1_minimax_debug_18run`.
- Summary root: `/tmp/flowfence_mas_p1_minimax_debug_18run_summary`.
- Debug root: `/tmp/flowfence_mas_p1_minimax_debug_18run_debug`.
- Task success rate: `1.0`.
- Unauthorized raw leakage mean: `3.333333`.
- External leakage mean: `0.222222`.
- Cascade size mean: `3.333333`.
- Privilege reach mean: `2.222222`.
- Failure categories: `{"none": 18}`.

## Committed Evidence Files

- `artifacts/minimax_p1_smoke_debug/README.md`
- `artifacts/minimax_p1_smoke_debug/debug_summary.json`
- `artifacts/minimax_p1_smoke_debug/debug_summary.md`
- `artifacts/minimax_p1_smoke_debug/run_manifest.json`
- `artifacts/codex_task_state/codex_p1_real_minimax_debug.md`

## Validation Commands

- `PYTHONPATH=. python src/runner/sweep_mas.py --help`
- `PYTHONPATH=. python src/runner/summarize_mas_p1.py --help`
- `python scripts/debug_mas_minimax_smoke.py --help`
- `python -m unittest tests/test_mas_minimax_debug.py`
- `python -m unittest tests/test_mas_minimax_smoke_config.py`
- `python -m unittest tests/test_mas_synthetic_runtime.py`
- `python -m unittest tests/test_mas_sweep_and_summary.py`
- `python -m unittest tests/test_mas_benchmark_strengthening.py`
- `python -m compileall scripts src`
- `git diff --check`
- `git status --short`

## Known Limitations

- This is a small MiniMax-only debug smoke, not a full real-model experiment.
- Raw traces, prompts, provider outputs, event JSONL files, policy-decision JSONL files, and individual per-run metrics are intentionally not committed.
- Utility success is final-output utility; internal/external leakage metrics remain separate.
- No non-MiniMax generalization is supported.

## Resume Instructions

Resume from branch `codex/p1-real-minimax-debug`.

First run:

- `git branch --show-current`
- `git status --short`

Then inspect:

- `artifacts/minimax_p1_smoke_debug/debug_summary.json`
- `scripts/debug_mas_minimax_smoke.py`
- `src/evaluators/utility.py`
- `src/runtime/orchestrator.py`

Do not commit raw run directories from `/tmp` or any provider output.
