# MiniMax Coverage Timeout Debug Summary

- Status: `retry_succeeded`
- Expected runs: `252`
- Completed before retry: `251`
- Failed before retry: `1`
- Completed after retry: `252`
- Failed after retry: `0`
- Failed run: `mas_p1__enterprise_assistant_001__chain_4__summary_poisoning_direct__prompt_filter__seed1`
- Failure type: `minimax_read_timeout`
- Appears transient: `true`

## Failed Configuration

- topology: `chain_4`
- attack: `summary_poisoning_direct`
- defense: `prompt_filter`
- seed: `1`

## Retry Result

- Strategy: same sweep without `--force`; completed runs with `metrics.json` were skipped.
- Retry completed runs: `1`
- Retry skipped runs: `251`
- Retry failed runs: `0`
- Canonical 3-seed coverage artifacts refreshed: `true`

## Privacy Boundary

Raw traces, raw provider outputs, prompts, policy JSONL, event JSONL, and individual metrics are not written by this script.
