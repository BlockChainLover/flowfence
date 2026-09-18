# E2 Source S1 evaluator reproduction

Status: **NOT_READY** for development-pilot review. Baseline reproduction only; scientific/development model generations **0 / 0**. Accepted source Design A is unchanged. The authorized claim remains `PUBLIC_BENCHMARK_TASK_AND_EVALUATOR_EXTERNAL_VALIDITY_UNDER_A_STANDARDIZED_MULTI_AGENT_EXECUTION_HARNESS`; original benchmark runtime external validity is not claimed.

## Exact sources and environment

`artifacts/aamas2027_e2_source_s1/source_manifest.json` records the accepted code/data pins, exact inspected file SHA256 values, Python version and evaluator dependencies. Code: BIRD `abd11b6db92a1c9f809b32f7564c7c71b34d67f0`; TAT-QA `870accc41953dcde885aabeb963d94aabdc0fbc3`; Hotpot `3635853403a8735609ee997664e1528f4480762a`. Data: BIRD HF `f65faf4ae3b638c1fa6df1d3370c8d92c8366301`; Hotpot mirror `1908d6afbbead072334abe2965f91bd2709910ab`. No source update or evaluator edit was made. The previously identified archive/HF discrepancy remains resolved in favor of the accepted canonical HF fields; question 879 was not repaired or substituted.

BIRD archive: 799,944,582 bytes; SHA256 `aeb211c0e39010bbdae3838bb5e8bd27dc446ed77495b1709f85ccc9bf67f2be`. Original PostgreSQL dump: 1,001,882,533 bytes; SHA256 `31b1da211849d24a57c9af7636da46a5b82fc8a3ca1542bb3ebd8775e9a31cec`. Every extracted description file is indexed in `database_source.json`. The original dump combines 75 tables into database `bird`, public schema; the original PostgreSQL connector uses this combined database. Source DB identities remain task metadata, not 11 independently restored server databases.

Actual engine: PostgreSQL 14.24 (Homebrew), arm64 macOS; UTF8, `lc_collate=C`, `lc_ctype=C`, timezone Asia/Shanghai. Source dump header reports PostgreSQL 14.12. Homebrew installed postgresql@14 and dependencies and initialized its default cluster as a package side effect; that service was not started. Only a separate temporary cluster was used. Restore initially failed because source owner role `xiaolongli` was absent. Creating that role with NOLOGIN and recreating only the temporary `bird` database allowed the unchanged dump to restore with `ON_ERROR_STOP=1`. Local dump/DB/logs remain uncommitted.

EX/F1: original `execute_model`, 30-second timeout, four caller threads, original PostgreSQL connection path. VES: original implementation, one caller, 100 timing iterations, three repeats on the first five source records, fixed before measuring; no timing-record selection. The source's timeout mechanism is unchanged. Serial-engine diagnostic sets `PGOPTIONS='-c max_parallel_workers_per_gather=0'`; the initial default-engine run remains saved separately. No SQLite result is used for S1 PostgreSQL certification.

## Original scorer observations

| Source | Deterministic evidence | Interpretation |
|---|---|---|
| BIRD EX, default engine | 498/500 native and serialized gold self-comparisons pass; invalid SQL scores 0 | Two failures are real source-evaluator self-comparison failures, not adapter serialization mismatches. |
| BIRD EX, serial query engine | 500/500 native and serialized gold self-comparisons pass | EX reproduction succeeds under the documented serial setting. |
| BIRD original F1 | Default: 483/500 self-comparisons score 1; serial: 493/500 score 1 | Original implementation compares deduplicated rows by list position despite its set-oriented docstring. Unordered query results can lower self-F1; no sorting/repair added. Its reported-metric admissibility remains unresolved. |
| BIRD original VES | Default and serial repeats both change reward for identical SQL | Not reproducible as a fixed reported metric in this measured setup. Source code preserved; human decision required before retaining/omitting VES. |
| TAT-QA | 1668 questions / 278 contexts; list-gold and adapter EM/F1/scale = 1; missing = 0 | Original full file entrypoint also reports 100/100/100. Family-wide output is `uid -> [answer-list, scale]`, including wrapping scalar zero as `[0]`. |
| TAT-QA scalar diagnostic | EM/F1/scale = 0.9970023980815348 | Known falsey scalar-zero behavior preserved. Operation metric = 0 because that API supplies no predicted operations. |
| HotpotQA | All 7405 records losslessly roundtrip; all 12 metrics rerun | Gold answer EM, support metrics and joint EM = 1; answer/joint F1, precision, recall = 0.999729912221472. Source normalization edge behavior retained. Wrong-answer/empty-support fixture gives all 12 metrics = 0. |

For BIRD 1473 and 1482, direct SQL execution succeeds but successive floating-point aggregate results fail exact equality under the initial environment. Three further original-EX repeats per record remain 0. Disabling query parallelism produces EX=1 for every record, supporting execution-order sensitivity; no epsilon comparator or gold change was introduced. This is an engineering diagnostic, not a model outcome used for task selection.

Example VES rewards, default engine: 1471 `[0.75,0.75,1]`, 1476 `[1,0.75,0.75]`, 1479 `[1,1,0.75]`. Serial engine: 1471 `[0.75,1,1]`, 1479 `[0.75,1,1]`. Identical SQL timing is close to the original reward threshold; changing the definition, rounding, averaging across new seeds, or silently dropping the metric would exceed this certification result. This report makes no admissibility decision.

Hotpot's canonical CMU host was unavailable in S0; the accepted versioned mirror is retained. No byte equality against an unavailable canonical download is claimed. IDs, question, titles, ordered sentences, sentence indices, answer, supporting pairs, type, level and context cardinality roundtrip exactly. 7345 records have ten paragraphs; 60 have two through nine. No padding/filtering was applied.

## Reproduction commands

Run from repository root with Python and temporary dependencies described in the manifest:

```bash
PYTHONPATH=. python3 scripts/prepare_e2_s1_postgres.py --private-root /private/tmp/e2_s1_private --output artifacts/aamas2027_e2_source_s1/database_source.json
# Initialize a dedicated PostgreSQL 14 cluster with UTF8/C locale, user postgres,
# localhost:5432. Do not target an existing user database.
# Create source owner xiaolongli NOLOGIN, create bird, and restore the original dump
# with psql -X -v ON_ERROR_STOP=1. The dump is never changed.
PYTHONPATH=. python3 scripts/audit_e2_s1_evaluators.py --source-root /private/tmp/e2_s0_sources --dependency-path /private/tmp/e2_s0_deps --output artifacts/aamas2027_e2_source_s1 --phase qa
PYTHONPATH=. python3 scripts/audit_e2_s1_evaluators.py --source-root /private/tmp/e2_s0_sources --dependency-path /private/tmp/e2_s0_deps --output artifacts/aamas2027_e2_source_s1 --phase pg
PGOPTIONS='-c max_parallel_workers_per_gather=0' PYTHONPATH=. python3 scripts/audit_e2_s1_evaluators.py --source-root /private/tmp/e2_s0_sources --dependency-path /private/tmp/e2_s0_deps --output artifacts/aamas2027_e2_source_s1/serial_engine --phase pg
```

The archive source is an unversioned public download URL captured by explicit archive/dump hashes. Re-fetching must verify these exact hashes; matching only file size is not sufficient provenance verification.
