# MiniMax 3-Seed Coverage Timeout Debug

This directory documents the one-timeout debug and retry for the 3-seed MiniMax coverage run.

Raw traces, raw MiniMax outputs, prompts, provider logs, event JSONL, policy JSONL, and individual per-run metrics are intentionally not committed.

The retry used MiniMax only. The original failed run was:

- `mas_p1__enterprise_assistant_001__chain_4__summary_poisoning_direct__prompt_filter__seed1`

The failure was a MiniMax read timeout and appears transient. The retry used the same output root without `--force`, so completed runs with `metrics.json` were skipped and only the missing run was executed. The canonical 3-seed coverage artifacts were refreshed to 252/252 completed runs.
