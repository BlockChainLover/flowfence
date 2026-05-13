# FLOWFENCE EMNLP 2026 Data Package

This package contains result data supporting the paper "FLOWFENCE: Runtime Containment for Retrieval-Memory Poisoning in LLM Agents".

Scope:
- Data only: aggregate CSV/JSON files and run-level case summaries.
- No source code, no provider API credentials, no run scripts, no raw provider configuration files.
- The package supports paper claims about retrieval-to-exposure containment, inspector-swap replay, adaptive-pilot exposure containment, benign false-quarantine replay, and local fixed-trace overhead.

Important caveats:
- The experiments are adapted AgentPoison StrategyQA full-ReAct runs, not an official full AgentPoison reproduction.
- Inspector-swap LLM judge results are capped replay/dry-run results, not downstream full-ReAct detector-swap experiments.
- Adaptive poisoning results are a Kimi pilot over three same-axis families and should be read primarily as exposure-containment evidence.
- Fixed-trace overhead is local replay overhead; it is not end-to-end provider runtime.

Top-level directories:
- `aggregate/`: CSV/JSON artifacts used to build paper tables.
- `run_level/`: selected per-run `metrics.json`, `case_results.jsonl`, `mismatch_notes.json`, and `status.txt` files for EMNLP P0/P1 runs.
- `source_manifest.csv`: destination file, original source path, and reason for inclusion.
- `excluded_files.csv`: intentionally excluded logs/configs/raw outputs/caches.
- `checksums_sha256.txt`: SHA-256 checksums for all packaged files.
- `validation_report.json`: basic packaging checks.

Generated: 2026-05-13T11:58:47

Additional run-level directory:
- `run_level/minimax_mechanism_and_stress/`: selected MiniMax run summaries supporting the mechanism matrix, known-trigger comparator, rewrite/quarantine ablations, and held-out paraphrase stress slice.
