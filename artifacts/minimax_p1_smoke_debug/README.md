# MiniMax P1 MAS Smoke Debug Evidence

This directory contains small committed summaries for the MiniMax final-writer task-success debug run. Raw traces, prompts, provider outputs, provider logs, event JSONL files, policy-decision JSONL files, and individual per-run metrics are intentionally not committed.

The debug evidence indicates that the original low task success was primarily caused by final-writer prompt shape and utility evaluator strictness. The fix preserves privacy checks: raw synthetic secrets and attack-like instructions still fail utility.

This remains a small MiniMax-only debug smoke, not a full real-model experiment.
