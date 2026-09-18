# Benchmark replacement R0 task state

- Goal: architecture-first public candidate audit for unchanged 60-task/1080-episode E2 objective, without runtime redesign or model execution.
- Branch: `codex/aamas2027-benchmark-replacement-r0`; base `2a179d3`; worktree `/private/tmp/flowfence_r0_20260918`.
- Completed work: four pinned source audits; source evidence index; candidate matrix; UNRESOLVED report, empty passing shortlist. Global default rule confirmed already present.
- Changed files: `BENCHMARK_REPLACEMENT_R0_REPORT.md`, `BENCHMARK_CANDIDATES.json`, `artifacts/aamas2027_benchmark_replacement_r0/SOURCE_EVIDENCE.json`, `artifacts/aamas2027_benchmark_replacement_r0/VALIDATION.json`, `research/logs/roadmap.md`, `research/logs/progress.md`, this file.
- Validation commands: standard-library JSON validation and source-anchor check (checks described in VALIDATION.json); `git diff --check`; `git -C <candidate> status --porcelain`; `git -C /private/tmp/flowfence_gate_a_worktree_20260918 status --porcelain`; final `git status --short`.
- Known limitations: no architecture passing candidate; tau2 structured binding/synchronization/evaluator proof incomplete; no eligible task counts, new-task recognizer/sidecar certification, parity execution, provider compatibility or scientific results. Four designs do not exhaust the public landscape.
- Resume instructions: read root report and JSON, then SOURCE_EVIDENCE.json. Use recorded revisions to inspect existing source. MARBLE Gate A is closed and read-only at `9615ca34d166c8c9f75c0c037626956512b0c251`; do not merge its branch. Do not modify R3, candidate sources, frozen recognizer, gold or evaluators. Do not select tasks or call models. Any next work remains static R0 until explicit human authorization changes scope.
- Formal model runs: 0. Development model runs: 0.
- Commit: see branch HEAD after audit commit; no push/merge performed.
