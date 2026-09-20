# E2 development pilot execution request — 2026-09-20

**NOT_READY — pre-dispatch configuration hard stop.**

DEVELOPMENT_ONLY — NOT CONFIRMATORY EVIDENCE

## Summary and concrete blocker

The user authorized54development cells under immutable P1 commit `9290f71b9a3f8dd02334f88f7f331eb61751bd03`, with an explicit instruction to stop before provider dispatch if implementing the runner exposes any scientific/configuration ambiguity not resolved by P1. No provider request or episode was started. No live runner commit exists.

The required episode-level task-success classification is not uniquely defined for HotpotQA. In `experiments/e2_pilot_config_p1/FAMILY_PROFILES.json`, `hotpot.success_metric` lists original answer EM/F1, supporting-fact EM/F1 and joint EM/F1; it does not select one boolean success criterion. `LIVE_FAILURE_POLICY.json` sets SUCCESSFUL_FINAL.task_success to ORIGINAL_EVALUATOR_RESULT, but this source returns multiple metrics. The current user request additionally requires episode-level task success/failure counts. These are not interchangeable: a hypothetical correct answer with incorrect supporting facts passes answer EM and fails joint EM. This example uses no benchmark question, gold or generated output.

Choosing answer EM, joint EM or an invented conjunction/threshold would resolve a scientific measurement choice not explicitly frozen by P1. Retaining the full original metric vector is already required and unambiguous, but does not itself define that additional boolean. The current instruction forbids filling this gap by inference, so execution stopped. The earlier P1 entrypoint/import validation missed this semantic gap; its PASS remains a historical configuration/dry-render result, not proof of complete executable specification.

**Human decision needed:** designate the existing original Hotpot metric for the episode-level success boolean, or explicitly require vector-only Hotpot reporting with no single task-success boolean. Preserve all original metrics and every selected task/defense/policy. This report changes none of them. A written decision can supersede the ambiguous reporting field without rewriting the original preregistration commit; no amendment has been made here.

## Integrity and runtime evidence

The previously temporary worktree was absent and marked prunable. It was restored from the existing authorized branch at the exact P1 commit; no history was rewritten. The unrelated original checkout and its uncommitted files were preserved.

The read-only audit verified58P1 manifest entries,41S1-F frozen entries and45R3 blobs in their separate historical Git lineage. The live manifest itself matches its bytes at the authoritative commit. The commit is reachable, development/confirmatory counts remain9/60 and IDs are disjoint. Recognizer SHA256 remains `6bb7cba43724c10213ee4d81cdf2f82877fa6f5b831ca71c0698495866307d62`. Prompts, schemas, scheduling, budgets, aliases, R2 and EXACT_IFC code, selections and policies are unchanged.

Principal binding is statically preserved. Live scheduler fidelity, capability parity, mediation and evaluator integration are NOT_EXERCISED. Prior deterministic certifications are not presented as new live evidence. Original source/dependency/PostgreSQL caches under /private/tmp were also absent; pinned source/evaluator hash records are unchanged, but physical files were not re-fetched after the mandatory configuration stop. Cache loss is an operational restoration item, not an attempted episode failure.

## Counts and reachability

Expected54; attempted0; valid0; completed finals0; unattempted54. All model/provider/infrastructure/tool/evaluator/timeout/budget/policy episode-failure counts are0. This denotes absence of execution, not success or operational readiness. No live implementation defect was observed; the blocker is pre-execution configuration ambiguity. No fixes after outcomes, retries, replacements or outcome-based design changes occurred.

Each contamination condition has18scheduled cells,0attempted,0observed reached,0observed not reached and18unattempted. Unattempted cells must NOT be counted as CONDITION_SURFACE_NOT_REACHED. The reachability audit includes each frozen family/defense/task cell. Construct validity is NOT_ASSESSED because no trajectory exists.

No privacy or utility observations exist. There is no defense ranking, significance test, confidence interval or effectiveness claim. DEVELOPMENT_MODEL_RUNS_EXECUTED=0; FORMAL_MODEL_RUNS_EXECUTED=0; CONFIRMATORY_TASKS_EXECUTED=0.

## Evidence index and reproduction

Safe records are under `artifacts/aamas2027_e2_development_pilot/execution_20260920/`:

- `integrity_and_blocker.json`: byte checks, Git ancestry and exact blocking fields.
- `summary.json` and `episodes.json`: machine summary and empty episode collection.
- `failure_audit.json`: zero episode failures plus the separately classified pre-execution blocker.
- `contamination_reachability.json`: scheduled/unattempted status for all36contaminated cells.
- `run_artifact_index.json`: raw/safe index; raw-artifact list is empty because no request was constructed or dispatched this session.

Reproduce static integrity with Python hashlib over every path in LIVE_PREREG_MANIFEST.json and S1-F frozen_manifest.json; compare the live manifest itself to `git show 9290f71:LIVE_PREREG_MANIFEST.json`. Hash each R3_PRESERVATION.json path using git show at its recorded historical commit. Check `git merge-base --is-ancestor 9290f71 HEAD`, source/config diff against9290f71, `git diff --check`, and `git status --short`. These checks need no source cache, provider credentials, network call or model output.

After the human resolves the success-reporting field, implement the live runner under all other unchanged P1 requirements; restore source/DB caches from the accepted pinned recipes; run all required mock/dry checks; commit FIRST_LIVE_RUNNER_COMMIT before dispatch. Retain PRE_RUN_PREREG_COMMIT as9290f71. No confirmation or formal execution follows automatically.
