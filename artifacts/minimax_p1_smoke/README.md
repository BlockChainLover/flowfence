# MiniMax P1 MAS Smoke Evidence

This directory contains small committed summaries for the P1 MiniMax smoke. Raw traces, prompts, provider outputs, provider logs, event JSONL files, policy-decision JSONL files, and per-run metrics are intentionally not committed.

The real provider is MiniMax only. This is not a full real-model experiment and should not be used to claim broad real-model robustness or non-MiniMax generalization.

The 18-run smoke covers only `chain_4` and `blackboard_4`, attacks `none`, `summary_poisoning_indirect`, and `workspace_poisoning_indirect`, defenses `none`, `prompt_filter`, and `flowfence_lite`, and `seed=1`.

The 18-run smoke had low task success (`0.055556`). Treat it as a MiniMax final-writer smoke and debugging checkpoint, not as a full real-model result. Raw traces and provider outputs remain intentionally uncommitted. The next recommended step is MiniMax smoke debugging, not broad coverage expansion.
