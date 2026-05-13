# Results

Store every serious run in a stable, readable directory so a collaborator can audit the claim without guessing what produced it.

## Naming Convention

- `results/smoke_<date>_<short-name>/`
- `results/baseline_<method>_<dataset>_<date>/`
- `results/method_<variant>_<dataset>_<date>/`
- `results/ablation_<question>_<date>/`

Do not use names like `tmp`, `test2`, or `final_final`.

## Minimum Contents Per Run Directory

- `manifest.json` and `run_manifest.json` describing the run purpose and fixed task manifest
- config snapshot
- command or runner reference
- metrics summary
- per-example outputs needed for audit
- failure notes if the run is partial

## Canonical Pre-Method Artifact Set

For the fixed `AgentPoison` pre-method slice, each serious run should contain:

- `run_manifest.json`
- `resolved_config.yaml`
- `status.txt`
- `metrics.json`
- `baseline_summary.json`
- `case_results.jsonl`
- `case_details/`
- `stdout.log`
- `stderr.log`

## Early Required Result Artifacts

1. Three fixed pre-method `AgentPoison` rerun artifacts on the same manifest.
2. One rerun aggregate summary artifact with mean/min/max for the frozen pre-method metrics.
3. Optional pairwise comparison artifacts for ad hoc inspection.

## Audit Rule

Every artifact here must be referenced from `research/logs/progress.md`. If there is no artifact path in the log, the result is not ready to support a claim.
