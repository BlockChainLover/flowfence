# E2 V2 D2 development pilot

**AAMAS_E2_DEVELOPMENT_V2_D2: READY_FOR_CONFIRMATORY_REVIEW**

**DEVELOPMENT_ONLY — NOT CONFIRMATORY EVIDENCE**

All54 frozen D2 cells were attempted once in the registered order. All54 observations, including ordinary failures, are retained. No implementation defect, hard stop, retry, replacement, outcome-based design change or live-code fix occurred. No V1 cell or confirmatory task was executed. The process stopped after cell54; the dedicated temporary PostgreSQL cluster was then shut down.

Readiness here means the authorized engineering checks passed and results are ready for human review. It does not authorize confirmatory execution or establish effectiveness. **D2_CONSTRUCT_VALIDITY_CONCERN: YES**:20/36 contaminated cells terminated before treatment entry. Human review must consider this limited treatment coverage; no scientific design was changed in response.

## Chronology and preserved definitions

- Reviewed D1 head:6c56e87bc7111e38502dd83f6f5ca1b094b6af9a.
- D2 selection rule commit:2acf2059c6b572f85188461cd50e1ad06627334d, before D2 IDs materialization.
- D2 first live runner commit:3944314f4730990119de3158ecf5b153943844fb, committed before first dispatch and pushed.
- Original P1 preregistration:9290f71b9a3f8dd02334f88f7f331eb61751bd03.
- Hotpot prospective amendment:1d67d65cc1974d18430b797c82658833a14937f7; original joint_em==1.0, all12 source metrics retained.
- BIRD success:ORIGINAL_EX_ONLY. TAT-QA success:original EM==1.0. Source evaluators are unchanged.

All58 P1 pins,45 historical R3 blobs,10 source/evaluator pins and42 D1-preserved files were reverified. V2 code/prompts/scheduler, MiniMax configuration/budgets, policy templates, A/B, recognizer, R2 and EXACT_IFC remain unchanged. The D2 runner bytes match its predispatch commit. Recognizer SHA256 remains6bb7cba43724c10213ee4d81cdf2f82877fa6f5b831ca71c0698495866307d62. V1 remains CLOSED_CONSTRUCT_VALIDITY_FAILURE; its28 observations and26 human-stopped cells were not reinterpreted or rerun. Confirmatory60 IDs/facts/policies/repetitions remain untouched.

## Execution and principal participation

The nine fresh D2 tasks each retain six registered cells: CLEAN/A/B × EXACT_IFC/FLOWFENCE_R2, one repetition. There were121 live request attempts: planner58, finance46, writer17. All17 scaffold-complete episodes include at least one invocation of each principal;16 released finals reached original evaluators. One episode failed after completing the scaffold. Other episodes are not described as complete live three-agent executions.

Recorded actor sequences match the frozen staged eligible-FIFO rule. Every one of27 paired defense initial requests is identical. Model-proposed task work remains unscripted. Premature finalize remains PROTOCOL_FAILURE without conversion/repair. All seven mediation boundaries were observed somewhere in live D2; per-episode boundary coverage is retained and no absent per-episode boundary is claimed as exercised. Boundary event totals are B1=337,B2=133,B3=393,B4=14,B5=11,B6=300,B7=48; these are mediation events, not counts of unique tool calls or leaks.

MiniMax-M2.7 was requested on all121calls and returned on116responses. Five failed calls have no returned model/usage metadata. The alias does not pin immutable weights. Reported usage across116responses:652573prompt tokens +62843completion tokens =715416total. Usage for five transport failures is unknown; monetary cost is not reported.

## Failure audit

| Termination | Cells |
|---|---:|
| SUCCESSFUL_FINAL |16|
| PROTOCOL_FAILURE |16|
| POLICY_REJECTION |15|
| PROVIDER_FAILURE |5|
| TOOL_FAILURE |1|
| CONTEXT_LIMIT |1|
| EXPLICIT_STOP / MODEL_LENGTH / BUDGET_EXHAUSTED / EVALUATOR_FAILURE / EPISODE_TIMEOUT / IMPLEMENTATION_DEFECT |0|

Provider and infrastructure counts both equal5 and refer to the same observations. There were zero timeouts, budget-exhausted episodes and evaluator failures. All ordinary failed episodes remain valid retained observations, not missing/replaced tasks. No hard-stop-unattempted cells remain.

The five transport failures retained actual diagnostics: three URLError with underlying SSLEOFError; two RemoteDisconnected. All were non-timeout. No HTTP status, provider request ID or provider error code was available, so those fields remain null. No error cause was invented, arbitrary body/header text copied, or failed request retried. This verifies the generic diagnostic repair on observed failures, not every possible provider error class. Historical V1 cell16 remains unchanged and incompletely diagnosed.

## Treatment entry, delivery and early failure

| Condition | Scheduled / attempted | Entered mediation | Released | Delivered | Quarantined | Early failure before entry | Unattempted |
|---|---:|---:|---:|---:|---:|---:|---:|
| A |18 /18|12|6|6|6|6|0|
| B |18 /18|4|1|1|3|14|0|

All16 A/B episodes with a model-proposed finance→writer handoff submitted exactly one frozen artifact to B2:16/16 conditional treatment entry. CLEAN never injected. R2's nine treatment quarantines count as surface reached and treatment instantiated, with no release/delivery and ordinary POLICY_REJECTION termination. Seven IFC treatments were released and delivered. These observations are not privacy/task-success claims.

Across the36 attempted contaminated cells,20 terminated earlier: BIRD8/12, TAT-QA6/12, HotpotQA6/12. This repeated pre-treatment failure is the reported construct-validity concern, not evidence of containment. Family/defense/task-level counts and each prior termination are in the reachability audit. No significance tests, defense ranking, treatment redefinition or prompt tuning was performed.

Later propagation is recorded as runtime provenance-descendant artifact/boundary activity, separately from raw-value releases. Provenance lineage does not mean semantic copying, leakage or successful task completion. Attempted boundary views, accepted candidate views, committed publication and recipient consumption remain distinct.

## Descriptive task and raw-value privacy observations

| Family | Attempted | Scored finals | Original task successes | Task failures including pre-final termination | Privacy TRUE / FALSE / UNKNOWN |
|---|---:|---:|---:|---:|---|
| BIRD PostgreSQL |18|3|2|16|0 /3 /15|
| TAT-QA |18|7|2|16|0 /7 /11|
| HotpotQA |18|6|1|17|0 /6 /12|

BIRD uses original EX; TAT uses original EM==1.0; Hotpot uses original joint_em==1.0. Full original evaluator outputs are retained, including all12 Hotpot metrics. Five of16 scored finals meet their family-specific success criterion; this is a descriptive count, not a pooled numeric cross-family utility score. All49 remaining episode outcomes are task failures under the frozen accounting.

Privacy totals:0TRUE /16FALSE /38UNKNOWN under exact raw-value release semantics. No unauthorized raw release was observed. FALSE describes completed negative observations only; incomplete episodes remain UNKNOWN. Neither zero IFC leaks nor R2 quarantine proves general confidentiality. No semantic/paraphrase/reconstruction detector was introduced.

## Artifacts and reproduction

Safe root:artifacts/aamas2027_e2_v2_d2_live/. The run directory preserves registration,54attempts,54episode records, status and completion. derived/ contains summary, episode_summary, failure_audit, contamination_reachability, principal_participation, runtime_audit, evaluator_summary, release_audit and artifact_index. The private-file index records paths, sizes and digests, never credentials or payloads.

Private full audit is local and Git-ignored at /Users/crazy/Desktop/agent-privacy-defense/FlowFence-Lite/data/secrets/e2_development_v2_d2_20260920/raw. Directories/files are700/600. It retains requests/responses, private reasoning, typed traces, exact messages, tool inputs/results, final outputs and evaluator input/output. Credentials were read in place from the existing ignored local file, never printed/copied/committed.

E2_D2_LIVE_REPRODUCTION.md gives the exact command and predispatch commit. Do not relaunch it: existing outputs are deliberately non-resumable and no rerun is authorized. scripts/summarize_e2_d2_live.py reads saved artifacts only. It verifies54trajectory digests, frozen requests, staged actor ordering,27initial request pairs, exact raw disclosures, treatment release/delivery, original evaluator output equality and metric definitions. Postrun integrity and safe-artifact/permission checks are saved separately. Reporting additions do not change execution semantics.

## Required human decision

Review the20pre-treatment failures and limited coverage alongside the intact conditional trigger, principal participation and evaluator integration. The completed D2 pilot is READY_FOR_CONFIRMATORY_REVIEW under the authorized criteria; it is not confirmatory evidence or permission to run formal tasks. V1 remains closed. D2 reruns0; outcome-based design changesNO; implementation fixes after first D2 outcomeNONE. CONFIRMATORY_TASKS_EXECUTED=0 and FORMAL_MODEL_RUNS_EXECUTED=0.
