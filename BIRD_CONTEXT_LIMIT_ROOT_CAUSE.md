# E2 C0 — BIRD context closure audit

Decision: **NOT_READY / LOSSLESS_FIX_NOT_FEASIBLE**. V3 remains **FINAL_V3_CANDIDATE**. The accepted treatment design and all historical D3 observations remain unchanged. No new orchestration or live representation binding is introduced.

## Evidence and scope

V3 completed history: `49d73d3fac1d0c166beb8c310a4cc9a53c521c10`; original D3 live runner: `792620bb7cea6ac1e697aaae5f2fe721a1ba37b5`; prospective registration correction: `cdf4a26558ecad62c3799f91e243c69ae8a16c80`; D1 specification: `dc40ab91d3cc06bcce56841b52044f6847d3826e`; D2 final: `ca84c2a94935c819fd7a07d6b546a9e743ab17c0`. C0 is a new branch from completed V3; no history is rewritten.

All **six** saved BIRD CONTEXT_LIMIT episodes were inspected: four contaminated and two CLEAN. The human-reviewed contaminated denominator remains **4 context failures among 12 contaminated BIRD cells**, with **6/12 pre-handoff failures** overall (the other two are provider/protocol failures). Conditional treatment entry remains **29/29**, with all 15 R2 quarantines terminal. C0 does not reinterpret early execution failures as containment.

All six context failures concern D3 task 346, finance stage, next model invocation **3**. The two accepted requests in each episode were reconstructed byte-for-structure exactly against saved requests and their saved responses were replayed without dispatch. Recorded SQL arguments and recorded tool draft results were used; no SQL engine or evaluator ran. Original private notes and final saved released context/history were checked for equality. The failed third request was never dispatched: its size is an **offline reconstruction**, not an invented saved provider request.

## Measured failure sizes

Bytes below measure canonical UTF-8 `messages`, including nested JSON escaping, as in the frozen guard. Candidate sizes retain the original prompts; any future representation instruction would add overhead. These are optimistic candidate measurements, still far above the unchanged **160,000-byte** guard.

| Cell | Condition | Arm | Before bytes | Single-copy candidate bytes | Planner JSON bytes |
|---|---|---|---:|---:|---:|
| E2_DEVELOPMENT_V3_D3_003 | CONTAMINATION_A | FLOWFENCE_R2 | 1583203 | 817091 | 231 |
| E2_DEVELOPMENT_V3_D3_004 | CONTAMINATION_A | EXACT_IFC | 1583769 | 817657 | 746 |
| E2_DEVELOPMENT_V3_D3_021 | CONTAMINATION_B | EXACT_IFC | 1583636 | 817524 | 608 |
| E2_DEVELOPMENT_V3_D3_022 | CONTAMINATION_B | FLOWFENCE_R2 | 1583450 | 817338 | 474 |
| E2_DEVELOPMENT_V3_D3_039 | CLEAN | FLOWFENCE_R2 | 1583468 | 817356 | 458 |
| E2_DEVELOPMENT_V3_D3_040 | CLEAN | EXACT_IFC | 1583535 | 817423 | 559 |

Each result has **29,936 rows and two columns**, occupying **706,360 canonical JSON bytes in one copy**. It appears once in SQL history and again as latest-result finance scratch. Removing the duplicate saves **766,112 serialized request bytes** in every failed episode. Maximum before: **1,583,769**; after: **817,657**. All six still fail.

Each task occupies 41,234 JSON bytes: complete source schema 27,163 and descriptions map 13,659 (components overlap conceptually and are not additive after request escaping). Each description CSV is also embedded in the schema; the second CSV values total **13580 JSON bytes**. No duplicate complete schema object was found. The candidate deliberately retains both CSV occurrences; even removing the entire task, prompts, and metadata cannot make the unrepeated 706,360-byte result fit as ordinary released JSON. Complete planner delegation appears once, private sidecar once (175 bytes), and system prompt/stage/tool schema is 2,113 UTF-8 bytes. Invocation/provenance metadata is 1,003 JSON bytes per failure.

SQL query objects are retained in saved ToolCall records, with per-episode lengths in `root_cause.json`; they are **not explicitly embedded in the frozen snapshot**. We do not infer them from results or silently add/remove them. Finance history consists of delegation plus released tool results; it is not a transcript containing every model query. No extra full runtime state snapshot or duplicate receipt wrapper was identified inside these failed requests. Distinct artifact references for scratch and history remain distinct even when their value bytes match.

## Classification

| Component | Classification | Treatment |
|---|---|---|
| Full task, schema, first description occurrence | REQUIRED_CURRENT_SEMANTIC_STATE | Preserve all tables, columns, descriptions, evidence and question |
| Second identical description CSV occurrence | REDUNDANT_SERIALIZATION_OF_ALREADY_PRESENT_STATE | Quantified; retained by this conservative candidate |
| Planner delegation, every SQL result, private finance sidecar, prompt/schema | REQUIRED_CURRENT_SEMANTIC_STATE | Preserve without relevance heuristics |
| Latest-result scratch copy also in history | REDUNDANT_SERIALIZATION_OF_ALREADY_PRESENT_STATE | One value with two ordered occurrence references |
| Artifact references, producer, recipient, authorization, lineage and decisions | REQUIRED_PROVENANCE_METADATA | Preserve original identities and trusted audit trail |
| Saved query/diagnostic records outside the model snapshot | HISTORICAL_DIAGNOSTIC_NOT_REQUIRED_FOR_NEXT_MODEL_DECISION | Classification describes current serialization only; retain audit evidence; semantic usefulness of adding query text is UNRESOLVED and out of scope |
| Repeated state across separate stateless model requests | REQUIRED_CURRENT_SEMANTIC_STATE | No hidden cross-request cache |

**BIRD_CONTEXT_GROWTH_CAUSE: MIXED.** There is substantial removable duplication and substantial required result content. This is an operational failure of the tested single-copy representation under the frozen capability, not an information-theoretic claim that no imaginable compression could encode these bytes. Arbitrary compressed blobs do not by themselves demonstrate equivalent model-accessible semantics; adding a decoder/tool or changing capability requires a separate human decision.

## All selected BIRD tasks: blind static audit

All **29 distinct selected public tasks**: V1 3, D2 3, D3 3, confirmatory 20. Only question ID, question, database ID, evidence, full schema and descriptions are passed to the adapter. No answer/SQL-gold/difficulty fields are accessed, no model output is generated, and no task-specific query is executed. Selection manifests and source bytes are unchanged.

Each task uses both arms and the same two deterministic profiles: twelve identical one-row results, or twelve distinct 256-row results whose text is fixed by action/row ordinal. Every finance prefix from 0 through 12 SQL actions is measured, plus initial planner context: **116 fixture constructions, 1,508 finance snapshots, 754 exact paired-arm comparisons**. Full measurements are in `static_context.json`, including initial size, per-prefix before/after sizes and maximum duplication removed per task/profile/arm.

Across these fixtures, finance maximum before is **369,045**, after **345,675**, and maximum net bytes removed **23,397**. These are maxima over the declared fixtures, **not universal worst-case bounds**. The frozen SQL broker uses `fetchall()` and imposes no result byte/row bound. Twelve actions limit action count, not semantic result size; a finite genuine worst-case size cannot be certified from this capability. No task pruning, output truncation, query restriction or guard increase is introduced.

Confirmatory static check: **20/20 serialization/schema coverage passed; context closure NOT certified**. Confirmatory tasks executed: **0**.

## Decision and next human decision

The candidate preserves semantics and provenance in offline tests but does not eliminate any observed context failure. **LOSSLESS_FIX_NOT_FEASIBLE under the tested contract and unchanged guard**. No live integration was made. No fresh selection rule or fresh IDs were produced because feasibility certification is a prerequisite. The requested future 3 × 3 × 2 = **18-cell** matrix is conditional only, not selected, authorized or executed.

Return for human review of the BIRD context budget/capability conflict before any prospective live validation. Do not raise the guard automatically, change the benchmark capability, start confirmatory execution or create V4. See `BIRD_LOSSLESS_CONTEXT_CONTRACT.md` for the candidate and certification limits.

## Reproduction

Run from this repository root (local saved private trajectories are required for the first command):

```bash
PYTHONPATH=.:/private/tmp/e2_s0_deps /opt/homebrew/bin/python3 scripts/audit_e2_bird_context_failures.py --output artifacts/aamas2027_e2_bird_context_c0/root_cause.json
PYTHONPATH=.:/private/tmp/e2_s0_deps /opt/homebrew/bin/python3 scripts/audit_e2_bird_context_static.py --source-root /private/tmp/e2_s0_sources --schema /private/tmp/e2_s1r_schema.json --output artifacts/aamas2027_e2_bird_context_c0/static_context.json
```

Both scripts prohibit socket operations. Providers/evaluators are replay-only or explicitly forbidden; brokers return saved drafts or deterministic fixtures. No provider credential is loaded. Raw content is kept in process memory or temporary private replay files, removed on completion; committed evidence contains only counts, sizes, classifications and task/cell IDs. Component byte counts are non-additive diagnostics. C0 model runs, confirmatory runs and formal runs: **0 / 0 / 0**.
