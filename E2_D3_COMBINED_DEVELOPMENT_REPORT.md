# E2 V3 D3 combined development result

Status: READY_FOR_CONFIRMATORY_REVIEW. This is a readiness result for human review, not authorization to run confirmatory E2 and not an effectiveness conclusion. All observations remain DEVELOPMENT_ONLY — NOT CONFIRMATORY EVIDENCE. V3 remains FINAL_V3_CANDIDATE; no automaticV4.

## Provenance and metadata correction

The combined dataset has54unique cells in the original frozen order: original immutable cell001 plus continuation002–054. Cell001 remains VALID_DEVELOPMENT_OBSERVATION_WITH_REGISTRATION_METADATA_DEFECT, PROTOCOL_FAILURE, privacyUNKNOWN, no scored final, rerunNO. Its original registration E2_DEVELOPMENT_V2_D3 is retained unchanged. The human accepted this as a metadata-only defect without altered scientific execution.

Prospective fix cdf4a26558ecad62c3799f91e243c69ae8a16c80 was committed and pushed before cell002. The actual continuation CLI registration passes its invariant: scientific namespace E2_DEVELOPMENT_V3_D3, distinct run instance E2_DEVELOPMENT_V3_D3_CONTINUATION_001, exact53-cell suffix. CLI regression covers original001rejection,78prior-task exclusions and old/confirmatory namespaces. D3_CONTINUATION_PREFLIGHT=PASS. D1 head dc40ab91d3cc06bcce56841b52044f6847d3826e, selection rule9e142e7a2ff282e986798da096ec525c0b03bb37 and first runner792620bb7cea6ac1e697aaae5f2fe721a1ba37b5 remain in history.

Original22safe artifact files and every originally indexed raw file match their pre-fix evidence. No original run directory was resumed or edited. Combined_index.json references both real run roots and records registration_metadata_defect=true only for001, false for002–054. The original run had no run_instance_id field; its derived value remains null rather than inventing historical metadata.

## Observations

Continuation53/53 attempted once; combined54/54attempted,54valid scientific observations,27completed/scored finals,0unattempted. Terminations:27SUCCESSFUL_FINAL,15POLICY_REJECTION,5PROTOCOL_FAILURE,6CONTEXT_LIMIT,1PROVIDER_FAILURE. Tool failures, evaluator failures, model-length failures, timeouts and budget exhaustion are zero. Provider/infrastructure counts both describe the same one failure, not two independent failures.

151model requests: planner54, finance70, writer27. Planner-stage success52; finance entered52; valid finance handoffs42. Missing writer invocation after the15R2 treatment quarantines is expected terminal behavior, not a stage-order failure. Maximum observed per-episode usage:7model invocations,5tool calls,27runtime service actions and3messages; frozen limits remain unchanged.

| Condition | Scheduled/attempted | Valid finance handoffs | Treatment entry | Quarantined | Released | Delivered | Pre-handoff failures |
|---|---:|---:|---:|---:|---:|---:|---:|
| A |18/18|14|14|7|7|7|4|
| B |18/18|15|15|8|7|7|3|

Conditional treatment entry is29/29=100%; every valid contaminated handoff produced exactly one wrapper submission. Unconditional valid handoff coverage is29/36≈80.56%. All15quarantines obeyed terminal POLICY_REJECTION with no semantic finance handoff and no writer. All14released wrappers were delivered; release is not equated with raw leakage. CLEAN had no A/B treatment.

Seven contaminated episodes failed before valid handoff: BIRD6/12treated cells and TAT-QA1/12; Hotpot0/12. BIRD failures comprise four context limits, one provider failure and one protocol failure. TAT-QA's one is protocol failure. These are ordinary observations, not containment or privacy success. This concentration is a construct-validity concern for human review. No unconditional readiness threshold was selected or changed after outcomes.

| Family | Attempted | Scored finals | Original task successes among scored finals | Success rule |
|---|---:|---:|---:|---|
| BIRD |18|5|3/5|Original EX only|
| TAT-QA |18|11|7/11|Original EM=1|
| HotpotQA |18|11|3/11|Original joint_em=1|

All other original metric vectors remain in evaluator_summary.json. Incomplete episodes retain the frozen task-failure convention; their absence of a scored final is not an original metric score. No pooled cross-family numeric utility, significance test, confirmatory CI or defense ranking is produced.

Raw-value privacy outcomes: TRUE0/FALSE27/UNKNOWN27. No unauthorized raw disclosure was observed in saved publication views; the27UNKNOWN episodes are not privacy successes and do not establish general confidentiality. Provenance descendant counts track lineage only, not semantic copying or reconstruction.

## Integrity and readiness

Saved-evidence audit reconstructs all151requests from frozen stage builders, verifies27paired initial requests, trusted principal order, actual mediated release/consumption, unique treatment artifact identity, original metric vectors and raw-value criteria. B1–B7 were all exercised in this live study; per-episode boundary coverage remains explicit. Offline certification remains separate from these observed live paths.

Postrun verification passes58P1 files,45historicalR3 blobs,67D1 files,10source/evaluator pins, restored schema, original evidence and unchanged live execution code since the fix. Recognizer SHA256 remains6bb7cba43724c10213ee4d81cdf2f82877fa6f5b831ca71c0698495866307d62. Runtime, stage schemas/prompts, BIRD loop, treatment wording/trigger, terminal quarantine, MiniMax sampling, budgets, retries, timeouts, R2/IFC and privacy/evaluator rules are unchanged.

150responses identify MiniMax-M2.7; the single transport failure has no returned model or usage. Its allowlisted diagnostics retain URLError/SSLEOFError, timeout=false; unavailable HTTP status/request ID/provider code remain null. No inferred metadata or retry.

Historical implementation defect count1, resolved prospectively with human acceptance of001; new/unresolved defects0. IMPLEMENTATION_FIXES_AFTER_FIRST_D3_OUTCOME=REGISTRATION_METADATA_FIX_ONLY. No further live-code modification, duplicate, rerun, replacement, outcome-based design change or prior-study reinterpretation. V1/D2 reruns0; confirmatory tasks0; formal model runs0. The60confirmatory IDs/assignments/quotas/policies remain unchanged.

Readiness follows the human's preregistered execution/integrity criteria. The seven pre-handoff failures, especially BIRD6/12, remain visible for the separate human scientific-scope decision. Low utility does not itself change readiness, and ready-for-review is not confirmatory approval.

## Evidence and next decision

- Original evidence: artifacts/aamas2027_e2_v3_d3_live/run/registration.json (unchanged defective namespace).
- Prospective fix: D3_REGISTRATION_FIX_AUDIT.md; artifacts/aamas2027_e2_v3_d3_continuation/registration_tests.json.
- Continuation: artifacts/aamas2027_e2_v3_d3_continuation/run/{registration,preflight,completion}.json.
- Combined: artifacts/aamas2027_e2_v3_d3_combined/{combined_index,summary,episode_summary,stage_treatment_reachability,principal_participation,failure_audit,evaluator_summary,runtime_audit,postrun_integrity}.json.
- Safe release/provenance evidence: combined release_audit.jsonl and artifact_index.json. Full requests/responses/trajectories stay only in ignored local private directories with700/600modes.
- Reproduction: E2_D3_CONTINUATION_REPRODUCTION.md. Its combined audit reads saved evidence only, never dispatches a model or reruns an evaluator. Do not relaunch either live command.

The dedicated PostgreSQL cluster was stopped after completion. Recommend human review of the BIRD pre-handoff failure concentration and development results before any confirmatory authorization. NEXT_GATE=HUMAN_CONFIRMATORY_REVIEW_NO_EXECUTION. No automaticV4 or merge.
