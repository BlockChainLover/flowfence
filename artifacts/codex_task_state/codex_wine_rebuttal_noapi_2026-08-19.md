# Goal

Complete WINE 2026 rebuttal Experiment A component ablation and Experiment B strong defense-in-depth baseline without any LLM API/provider call, execute remotely in isolation, pull results locally, and package an auditable ZIP.

# Branch

`codex/wine2026-rebuttal-noapi`

# Completed work

- Audited the deterministic MAS implementation, canonical non-oracle config, evaluators, and remote source availability.
- Added three non-oracle ablation modes and `acl_content_runtime` without changing thresholds or canonical artifacts.
- Added per-run provider/oracle/action counts and a hard `no_llm_api_required` guard.
- Passed local and remote pilot gates, then completed 270 Experiment A and 90 Experiment B new runs with zero failures.
- Generated matched summaries, negative/neutral findings, redacted safe traces, environment metadata, source manifest, code patch, and local evidence package.
- Verified `/Users/crazy/Desktop/agent-privacy-defense/FlowFence-Lite/wine2026_rebuttal_noapi_experiments_2026-08-19.zip`; SHA-256 `8210fc67506323d8f2172f9dfd5d7075059b97389a8de1045885fb2b9e3fee54`.

# Changed files

- `src/defenses/mas_flowfence.py`
- `src/runtime/orchestrator.py`
- `src/runner/sweep_mas.py`
- `configs/experiment/mas_rebuttal_noapi_*.yaml`
- `scripts/audit_wine_rebuttal_pilot.py`
- `scripts/summarize_wine_rebuttal_noapi.py`
- `tests/test_wine_rebuttal_noapi.py`
- `artifacts/rebuttal_noapi_2026-08-19/`
- `research/logs/progress.md`

# Validation commands

- `PYTHONPATH=. python -m unittest tests.test_wine_rebuttal_noapi tests.test_nonoracle_flowfence tests.test_mas_synthetic_runtime tests.test_mas_sweep_and_summary`
- Remote pilot and full `sweep_mas.py` commands recorded in `artifacts/rebuttal_noapi_2026-08-19/README.md`.
- Strict aggregation by `scripts/summarize_wine_rebuttal_noapi.py`.
- `git diff --check`
- `unzip -t wine2026_rebuttal_noapi_experiments_2026-08-19.zip`

# Known limitations

- Historical P1 raw traces were absent from the remote paths recorded by canonical manifests, so FULL/NO_SEMANTIC/Static ACL/Prompt Filter were deterministically schema-refreshed.
- NO_SAFE_VIEW, NO_TOPOLOGY_FANOUT, and NO_PROPAGATION_RIGHT_NARROWING are neutral on the main outcomes in this suite.
- Propagation-right signals are metadata-only in the current runtime and do not gate downstream execution.
- Task success is a deterministic template/rule check, not semantic-quality evaluation.
- The remote repository mapping is not a Git checkout; source identity is the synced local HEAD plus `CODE_CHANGES.patch`.

# Resume instructions

Read `artifacts/rebuttal_noapi_2026-08-19/README.md`, `NO_LLM_API_AUDIT.md`, and `03_rebuttal_evidence/rebuttal_evidence_summary.md`; verify `FILES_SHA256.txt` and the ZIP checksum before citing numbers. Do not write these results into the paper automatically.
