# MiniMax P1 MAS Smoke Debug Summary

This directory contains high-level, redacted debug summaries only. Raw traces, prompts, provider outputs, event JSONL files, policy-decision JSONL files, and individual per-run metrics are intentionally not committed.

## Diagnosis

Main issue: final-writer prompt shape plus utility evaluator strictness. The original evaluator required near-exact wording, while MiniMax can produce safe vendor-facing updates with different wording. The debug run shows no missing final outputs, no empty final outputs, no raw synthetic secrets in final-output previews, and safe update terms in every final output.

## Fixes Applied

- Updated the final-writer prompt to require `Vendor-safe update:` and to preserve safe status while withholding internal-only details.
- Updated the utility evaluator to accept reasonable safe vendor-facing update wording while still rejecting raw synthetic secrets and attack-like instructions.

## Two-run Debug

- Completed runs: `2`
- Failed runs: `0`
- Task success rate: `1.0`
- Unauthorized raw leakage mean: `0.0`
- External leakage mean: `0.0`
- Failure categories: `{'none': 2}`

## Eighteen-run Debug

- Completed runs: `18`
- Failed runs: `0`
- Task success rate: `1.0`
- Unauthorized raw leakage mean: `3.333333`
- External leakage mean: `0.222222`
- Cascade size mean: `3.333333`
- Privilege reach mean: `2.222222`
- Failure categories: `{'none': 18}`

## Caveats

- This is a small MiniMax debug smoke, not a full real-model experiment.
- Utility success is final-output utility; internal/external leakage metrics remain separate.
- Do not claim non-MiniMax generalization or broad real-model robustness.
