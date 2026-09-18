# S0 source audit evidence

This directory contains ID inventories, source provenance and original-evaluator sanity outputs only. **All enumerated IDs are unselected.** No row is a development/confirmatory assignment. No protected facts, contamination payloads, decrypted BrowseComp text, gold content, provider credentials or full trajectories are committed.

Read ../../E2_SOURCE_SCREENING_S0_REPORT.md, ../../PUBLIC_SOURCE_CANDIDATES.json and ../../CANDIDATE_COMBINATIONS.md. Fourteen profiles were audited; five pass source-level feasibility, seven fail current requirements and two remain unresolved. Two three-family combinations are for human selection; no final design selected.

## Reproduction

Exact source commits, HF revisions and source paths are in source_provenance.json. `current_database_archive_inventory.json` records public package member names/sizes only. The Google Drive package was range-inspected, not fully downloaded or restored. The original SQLite database used for fixtures was extracted from the source's documented legacy package; its object metadata is retained. Source docs permit original SQLite DBs. Exact package-vs-HF task ID alignment was checked: one gold SQL differs, question_id879 in each dialect; use canonical HF gold. No new hash/freeze mechanism is introduced.

From the repository root:

```sh
PYTHONPATH=. python3 scripts/fetch_e2_source_s0.py --help
PYTHONPATH=. python3 scripts/fetch_e2_source_s0.py --source-root /private/tmp/e2_s0_replay_sources
python3 -m pip install --target /private/tmp/e2_s0_replay_deps numpy==2.5.3 pandas==3.0.6 scipy==1.18.1 sympy==1.14.0 pyarrow==25.0.1 func_timeout==4.3.5 psycopg2-binary==2.9.13 pymysql==1.2.3 tqdm==4.70.1 ujson==6.0.0
PYTHONPATH=. python3 scripts/audit_e2_source_s0.py --help
PYTHONPATH=. python3 scripts/audit_e2_source_s0.py --source-root /private/tmp/e2_s0_replay_sources --dependency-path /private/tmp/e2_s0_replay_deps --output /private/tmp/e2_s0_replay_report
```

The actual session used /private/tmp/e2_s0_sources and /private/tmp/e2_s0_deps. Initial acquisition used parallel canonical clones/HF downloads and bounded ZIP reads; the reusable fetch helper was subsequently checked with --help and syntax compilation, **not replayed end-to-end**. The audit helper itself was executed successfully against the downloaded sources. It writes no source code and does not invoke any solver/model. The first audit attempt stopped at HotpotQA's missing ujson import; after installing the original dependency, the complete audit succeeded. This environment uses current Python/scientific libraries, not the original baseline training stacks; no complete source reproduction is claimed.

An additional original TAT-QA `tatqa_eval.evaluate_prediction_file` entrypoint check completed on all1668 dev gold answers in legal answer-list format; see tatqa_entrypoint_sanity.json. The reusable audit covers its underlying original metric class. All twelve Hotpot metrics were preserved, including gold-normalization edge behavior. FinQA includes execution and symbolic-program scores. SQLite companion fixtures include original EX and Soft-F1, not R-VES timing or PostgreSQL restore. BrowseComp executes only the unmodified original grade method/comparison with a fixed fake grader string and synthetic placeholders, never a provider request or encrypted dataset decryption.

Counts in TASK_SCALE_AUDIT.csv are provisional source-level pools. The complete official ID inventory includes audited failed/unresolved sources for provenance, not a selected experimental sample. BIRD dialects are duplicate semantic pools; repetitions and shared source contexts are not independent tasks.

No full runtime, benchmark adapter or FlowFence/EXACT_IFC integration exists in this change. R3 and frozen recognizer files are unchanged. Next step is a human source-design decision only; do not enter task selection, implementation, development pilot or Gate B on the authority of this artifact.
