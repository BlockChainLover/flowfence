# E2 Source S1 durable task state

Goal: certify accepted Design A using original evaluators, deterministic family adapters and full-pool eligibility; select9/60only if all prerequisites pass.
Branch: codex/aamas2027-e2-source-s1; isolated worktree /private/tmp/flowfence_e2_source_s1_20260918; base S0 3dec10223ef4ce40c3aa52dbefa94503ef94c5c7; pre-result predicate commit0ed9269ff88be8b3656d50c70618adff47c46309.

Completed work: exact source provenance/DB archive hashes; PostgreSQL14.24 actual restoration; original EX/F1/VES measurements under two documented engine settings; TAT/Hotpot original scorer reproduction; public serialization adapters; deterministic interface prototype/basic ownership and84paired release tests;9573-record conservative eligibility/naturalness/clustering audit; report NOT_READY. No final study IDs, facts, A/B content or models.

Changed files: E2_TASK_ELIGIBILITY_SPEC.md; E2_TASK_CLUSTERING_SPEC.md; E2_S1_EVALUATOR_REPRODUCTION.md; E2_S1_CERTIFICATION_REPORT.md; experiments/e2_source_s1/eligibility_schema.json; src/e2_s1/; scripts/prepare_e2_s1_postgres.py, audit_e2_s1_evaluators.py, audit_e2_s1_pool.py, check_e2_s1_interfaces.py, check_e2_s1_release_variants.py, validate_e2_s1_evidence.py; artifacts/aamas2027_e2_source_s1/; research/logs/roadmap.md and progress.md; this file.

Validation commands:
- PYTHONPATH=. /opt/homebrew/bin/python3 scripts/audit_e2_s1_evaluators.py --source-root /private/tmp/e2_s0_sources --dependency-path /private/tmp/e2_s0_deps --output artifacts/aamas2027_e2_source_s1 --phase qa (also --phase pg).
- PGOPTIONS='-c max_parallel_workers_per_gather=0' with same pg command, output artifacts/aamas2027_e2_source_s1/serial_engine.
- PYTHONPATH=. /opt/homebrew/bin/python3 scripts/audit_e2_s1_pool.py --source-root /private/tmp/e2_s0_sources --dependency-path /private/tmp/e2_s0_deps --private-root /private/tmp/e2_s1_private --output artifacts/aamas2027_e2_source_s1.
- PYTHONPATH=. /opt/homebrew/bin/python3 scripts/check_e2_s1_interfaces.py --output artifacts/aamas2027_e2_source_s1/interfaces.json.
- PYTHONPATH=. /opt/homebrew/bin/python3 scripts/check_e2_s1_release_variants.py --output artifacts/aamas2027_e2_source_s1/release_variants.json.
- PYTHONPATH=. /opt/homebrew/bin/python3 scripts/validate_e2_s1_evidence.py --artifacts artifacts/aamas2027_e2_source_s1 --dependency-path /private/tmp/e2_pivot_schema_deps.
- All six new scripts --help; compileall; git diff --check; byte comparison of copied frozen R2 and unchanged recognizer SHA256.

Known limitations: VES unstable, reported-metric decision pending human; original F1 row-order behavior unresolved. Full source DB broker/constraint metadata, typed P0 authority/provenance and all23transition variants are incomplete. Seven tested hooks are not complete mediation. All9573eligibility records unresolved; balance unresolved; no selection. Hotpot canonical host unavailable; accepted pinned mirror retained. No original-runtime external validity claim.

Resume instructions: read contract, newest roadmap/progress and S1 reports. Preserve pre-result predicate and frozen R3/recognizer. Resolve metric admissibility with human, complete already-authorized deterministic runtime implementation, rerun full eligibility before balance/selection. Source fixtures /private/tmp/e2_s0_sources; dependencies /private/tmp/e2_s0_deps and /private/tmp/e2_pivot_schema_deps; original database files /private/tmp/e2_s1_private. Temporary PostgreSQL cluster /private/tmp/e2_s1_pg_data, socket /private/tmp/e2_s1_pg_socket; it is stopped at handoff. Port5432must be free before restarting; never reuse an unrelated DB/service. No model/pilot/Gate B authorization. Final Git HEAD/remote verified in delivered response; original user checkout retains its preexisting dirty files.
