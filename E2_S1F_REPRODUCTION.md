# S1-F reproduction and artifact guide

Accepted parent: 406440eb82e588bf0810d631e65a1fd0dbf46974.
Rule checkpoint: 93313c8be90a3f77768d39efd507215ea57d8fa2.

From repository root, with the already pinned S0 source cache and Python3/pyarrow25.0.1:

```bash
PYTHONPATH=.:/private/tmp/e2_s0_deps python3 scripts/select_e2_s1f.py --help
PYTHONPATH=.:/private/tmp/e2_s0_deps python3 scripts/select_e2_s1f.py --source-root /private/tmp/e2_s0_sources --rule-commit 93313c8be90a3f77768d39efd507215ea57d8fa2 --output /private/tmp/e2_s1f_replay_20260918
PYTHONPATH=. python3 scripts/validate_e2_s1f.py --help
PYTHONPATH=. python3 scripts/validate_e2_s1f.py --replay-dir /private/tmp/e2_s1f_replay_20260918 --verify-manifest
git diff --check
git status --short
```

Source retrieval/pins remain documented in E2_SOURCE_SCREENING_S0_REPORT.md and E2_S1R_REPRODUCTION.md; data/evaluator file hashes are in the inherited source manifest. Replay needs these publicly sourced files, inherited committed eligibility/cluster metadata and the rule, not a database server, credentials, model client or scientific output. Source files are hash-checked; only id/type columns of the Hotpot parquet are decoded for selection. No questions, SQL, gold answers or model/defense scores are used. Python implementation can be replayed without the historical temporary path by changing --source-root and installing the recorded pyarrow version. Development tasks remain permanently reserved.

artifacts/aamas2027_e2_source_s1f/ contains:
- preselection_capacity.json: aggregate-only capacity proof committed before selection;
- development.json / confirmatory.json: 9/60 public task IDs, clusters, assignments, principals, surfaces, source pins and evaluators;
- policy_skeletons.json: 69 task-bound templates; no instantiated raw values;
- selection_provenance.json: rule SHA and exact metadata/config inputs;
- allocation_certificate.json: constructive allocation witness, counts and dependence disclosures;
- validation.json: independent graph traversal, policy/annotation checks, replay equality and unchanged implementation;
- frozen_manifest.json: SHA256 for frozen rule/configuration/selection/policy/evidence artifacts and inherited inputs, excluding itself. It is not a signature and does not replace Git chronology.

All new files are small review artifacts; source dumps, source corpora, raw trajectories and secrets are excluded. Original S1/S1-R artifacts remain unmodified. The manifest includes inherited certifications to carry their exact evidence forward without rerunning expensive certification. Git commit ordering establishes that the rule preceded the first materialized split. The validator itself was added after selection and cannot change the precommitted selector.
