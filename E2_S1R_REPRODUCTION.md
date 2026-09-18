# S1-R deterministic reproduction commands

Run from repository root. No provider credentials or live model client are needed.

Sources: `/private/tmp/e2_s0_sources`; original DB files: `/private/tmp/e2_s1_private`; restored cluster: `/private/tmp/e2_s1_pg_data`. PostgreSQL14.24 binaries are under `/opt/homebrew/opt/postgresql@14/bin`. At handoff the temporary server is stopped; verify localhost5432is unused before restarting this specific cluster. Never reuse an unrelated database. If recreation is necessary, first verify S1's exact archive/dump/extracted hashes and follow `E2_S1_EVALUATOR_REPRODUCTION.md`; do not update source data.

Temporary dependencies: `/private/tmp/e2_s0_deps` (original S1 manifest), `/private/tmp/e2_pivot_schema_deps` (jsonschema), `/private/tmp/e2_s1r_deps` (pglast8.4). Source schema JSON is private local operational metadata, not evaluator-private gold; regenerate it from the actual restored DB and original descriptions.

```bash
export PYTHONPATH=.:/private/tmp/e2_s0_deps:/private/tmp/e2_s1r_deps:/private/tmp/e2_pivot_schema_deps
export PGOPTIONS='-c max_parallel_workers_per_gather=0'
/opt/homebrew/opt/postgresql@14/bin/pg_ctl -D /private/tmp/e2_s1_pg_data -l /private/tmp/e2_s1_pg_server.log -o '-h 127.0.0.1 -p 5432 -k /private/tmp/e2_s1_pg_socket' start
python3 scripts/prepare_e2_s1r_broker.py --dependency-path /private/tmp/e2_s0_deps --private-root /private/tmp/e2_s1_private --output /private/tmp/e2_s1r_schema.json
python3 scripts/certify_e2_s1r_runtime.py --schema /private/tmp/e2_s1r_schema.json --source-root /private/tmp/e2_s0_sources --output artifacts/aamas2027_e2_source_s1r/runtime_certification.json
python3 scripts/check_e2_s1r_edge_cases.py --schema /private/tmp/e2_s1r_schema.json --output artifacts/aamas2027_e2_source_s1r/edge_cases.json
python3 scripts/audit_e2_s1r_sources.py --schema /private/tmp/e2_s1r_schema.json --source-root /private/tmp/e2_s0_sources --output artifacts/aamas2027_e2_source_s1r
python3 scripts/recalculate_e2_s1r_eligibility.py --s1 artifacts/aamas2027_e2_source_s1 --certification artifacts/aamas2027_e2_source_s1r
python3 scripts/validate_e2_s1r_evidence.py --artifacts artifacts/aamas2027_e2_source_s1r --source-root /private/tmp/e2_s0_sources
/opt/homebrew/opt/postgresql@14/bin/pg_ctl -D /private/tmp/e2_s1_pg_data stop -m fast
git diff --check
git status --short
```

The runtime test includes two actual30sSQL timeout checks; it does not replace the original EX timeout behavior or use shorter timeout evidence. Do not run original F1/VES again to search for favorable timings or redefine either metric. Their unchanged S1 diagnostic evidence is sufficient and preserved.
