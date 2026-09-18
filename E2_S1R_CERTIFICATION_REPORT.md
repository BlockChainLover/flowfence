# E2 Source S1-R — runtime closure and eligibility recalculation

**AAMAS_E2_SOURCE_S1: NOT_READY.** Runtime closure, source adapters, original task-success evaluators and all9573eligibility records are now verified. The remaining blocker is a mathematically infeasible fact-type allocation under the unchanged S1 naturalness annotations. No development/confirmatory IDs or selection algorithm were created. Scientific/development model runs remain0/0.

## Human metric decision and source preservation

`E2_S1R_METRIC_DECISION.md` was committed as188ceb7 before final certification or any model outcomes:

- BIRD_CONFIRMATORY_SUCCESS_METRIC: ORIGINAL_EX_ONLY.
- BIRD_F1_STATUS: PRESERVED_DIAGNOSTIC_NOT_CONFIRMATORY.
- BIRD_VES_STATUS: PRESERVED_DIAGNOSTIC_NOT_CONFIRMATORY.

Original F1/VES implementations, default/serial S1 measurements and their caveats remain unchanged. No complete BIRD leaderboard-suite reproduction is claimed. There was no new source screening or source-family change.

`source_verification.json` and `validation.json` verify the inherited exact code/data pins and hashes, full archive and76extracted files, plus the unchanged recognizer. The same S1-restored PostgreSQL14.24 cluster was restarted; no database recreation or source-data mutation occurred. Only read-only role grants/schema access controls were added. Final EX uses UTF8/C locale, max_parallel_workers_per_gather=0 and the original30-second EX timeout behavior. New parser dependency: pglast8.4 in a temporary directory.

## Source/evaluator and adapter results

| Family | Official records | Original scoring / mapping evidence | Adapter status |
|---|---:|---|---|
| BIRD PostgreSQL | 500 | Original EX500/500; original invalid-SQL fixture0; actual broker/source result equality for every reference-query fixture; source index/db_id retained | VERIFIED |
| TAT-QA dev | 1668 | Original EM/F1/scale1.0; original full file entrypoint succeeds; operation remains0 because the source API supplies no predicted operation | VERIFIED |
| Hotpot distractor dev | 7405 | All12original metrics reproduced; every mirror field roundtrips; original non-perfect answer-F1 normalization behavior retained | VERIFIED |

BIRD_SCHEMA_CAPABILITY_PRESERVATION: VERIFIED. All11source database profiles /75tables include full source column metadata, descriptions and source-visible restored constraints/relationships. Metadata is obtained without gold SQL. Non-UTF8 descriptions now decode losslessly rather than using replacement characters. The actual broker's SELECT-only grants match each source profile exactly, and none has table-write privileges. Original query result order is preserved; engineering equality checks use source EX set semantics without modifying original scorer data/comparators.

BIRD output is the actual released SQL plus source db_id and recorded source ordering; TAT output is the actual released answer-list/scale; Hotpot output is the actual released answer/support pairs. Golden outputs are explicitly deterministic reproduction fixtures, not solved-task/model performance. No gold/reference **input** or hidden TAT answer-type/derivation/support field enters runtime context. The original evaluator receives outputs only through a trusted outgoing port, with P0 EvaluatorJob private references outside Runtime.

## Runtime certification

See `E2_S1R_RUNTIME_CLOSURE.md` for implementation, scope and the coverage argument; see `mediation_paths.json` for each family/path's producer, consumer, API, boundary, trusted provenance and bypass test.

- STRUCTURAL_PARITY_IMPLEMENTATION: VERIFIED.
- TRANSITION_CLASSES_TOTAL / VERIFIED:23/23.
- PAIRED_RUNTIME_FIXTURES:51 (45core scenarios +6focused edge scenarios), failures0.
- MEDIATION_ARCHITECTURE_IMPLEMENTATION: VERIFIED.
- MODELED_BYPASSES_REMAINING:0 under the declared trusted-service/actor-capability scope.

Fixtures use actual state/message/tool/final/evaluator interfaces, not direct release-hook calls. BIRD has real SELECT/WITH, empty rows, SQL error, read-only denial,30s server timeout, safe result publication, tool-recipient authorization and source-result equivalence. TAT and Hotpot use complete document/evidence state; they have no SQL/web/fullwiki capability. All23classes are covered across the fixed runtime and applicable family paths; successful source-tool classes are not invented for tool-free families.

No OS-wide security, malicious trusted Python, reflection sandbox, covert-channel protection or future live provider integration is certified. The original recognizer's limitations remain. Runtime mediation coverage is distinct from universal attack detection.

## Task-level recognizer and eligibility

Required recognizer SHA256 remains:
`6bb7cba43724c10213ee4d81cdf2f82877fa6f5b831ca71c0698495866307d62`.

All9573records instantiate the approved A/B template structure on their actual planned internal_message handoff, with a distinct synthetic placeholder used only for absence checks. Both artifacts omit the placeholder, match the unchanged recognizer and use no task-specific detector. The surface is exercised through actual send/receive interfaces. These are certification fixtures; no final study protected values or scientific/model-generated A/B wording exists.

The original S1 predicate, schema and clustering specification are unchanged. Only the previously UNKNOWN evaluator/capability/adapter/parity/mediation fields were resolved from completed certification. Naturalness, compatible types and rationale remain byte-value equal to each prior S1 row.

| Family | Eligible | Ineligible | Unresolved | Exclusion reasons |
|---|---:|---:|---:|---|
| BIRD PostgreSQL | 500 | 0 | 0 | none |
| TAT-QA | 1668 | 0 | 0 | none |
| HotpotQA | 7405 | 0 | 0 | none |

Eligibility requires at least one natural compatible type; it does not imply that a globally balanced subset exists. TAT still has278source contexts. Hotpot retains5918bridge/1487comparison records and original variable context cardinality. S1 overlap metadata and clustering limits remain authoritative; no independence claim is inferred from9573questions.

## Machine-checkable balance failure

**FACT_BALANCE_FEASIBILITY: FAILED.** `balance_infeasibility.json` and `recalculate_e2_s1r_eligibility.py` provide the certificate:

1. Every one of the500eligible BIRD records retains exactly `compatible_types=[P4]`.
2. Selecting exactly20BIRD records therefore forces at least20P4assignments.
3. The required global P4count is exactly15.
4. Thus20≤15would be necessary, a contradiction. Adding clustering/development-disjointness constraints cannot make this infeasible set feasible.

No positive allocation witness exists under these recorded compatibility sets. This does **not** prove that every conceivable independent semantic justification for BIRD P3 is impossible. It does prove that the current retained annotations cannot satisfy the requested allocation. No P3label was added to make balance work, and no task/fact quota was reduced.

Selection prerequisites fail, so no selection algorithm was written/committed and no selected IDs were materialized. Development0; confirmatory0; assigned P1/P2/P3/P4counts0each. Split disjointness is not applicable.

## Required human decision / next gate

Return this fixed-annotation fact-balance contradiction for **human design review**. Do not relabel tasks, reduce20per family or change source families automatically. Any independently justified change to the permitted naturalness/design constraints requires a separate human decision before recalculation. The next gate is fact-balance/design review, not the development pilot. Pilot review remains conditional on a valid allocation and frozen9/60split.
