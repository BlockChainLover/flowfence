# QRecovery formal report

Status: FORMAL_COMPLETED_AFTER_AUTHORIZED_REPORTING_CORRECTION. Preregistration 677f32ab81fa08f2d5541bbb2f9c1f9dc87884a2; implementation e9847b72da1db61d2e3d62837897259298614f98.

Scheduled280; attempted280; finished280; clean40; contaminated240; implementation defects0. Every ordinary failure stays in attempted denominators. Historical720unchanged and never rerun.

## Table A — containment and continuation (contaminated)

| defense | attempted | treatment_reaching | original_artifact_released | original_artifact_reaches_writer | quarantined | recovery_attempted | writer_invoked_after_quarantine | schema_valid_finals |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EXACT_IFC | 240 | 215 | 215 | 215 | 0 | 0 | 0 | 205 |
| FLOWFENCE_R2 | 240 | 215 | 0 | 0 | 215 | 0 | 0 | 0 |
| FLOWFENCE_RECOVERY | 240 | 223 | 0 | 0 | 223 | 223 | 223 | 222 |

## Table B — native utility (separate benchmarks)

| family | defense | condition | attempted | scored | native_success | success_over_attempted | success_over_scored |
| --- | --- | --- | --- | --- | --- | --- | --- |
| hotpot | EXACT_IFC | CLEAN | 60 | 55 | 4 | 0.06666666666666667 | 0.07272727272727272 |
| hotpot | FLOWFENCE_R2 | CLEAN | 60 | 54 | 3 | 0.05 | 0.05555555555555555 |
| hotpot | FLOWFENCE_RECOVERY | CLEAN | 20 | 17 | 3 | 0.15 | 0.17647058823529413 |
| hotpot | EXACT_IFC | CONTAMINATION_A | 60 | 54 | 6 | 0.1 | 0.1111111111111111 |
| hotpot | FLOWFENCE_R2 | CONTAMINATION_A | 60 | 0 | 0 | 0.0 | None |
| hotpot | FLOWFENCE_RECOVERY | CONTAMINATION_A | 60 | 57 | 5 | 0.08333333333333333 | 0.08771929824561403 |
| hotpot | EXACT_IFC | CONTAMINATION_B | 60 | 49 | 3 | 0.05 | 0.061224489795918366 |
| hotpot | FLOWFENCE_R2 | CONTAMINATION_B | 60 | 0 | 0 | 0.0 | None |
| hotpot | FLOWFENCE_RECOVERY | CONTAMINATION_B | 60 | 53 | 9 | 0.15 | 0.16981132075471697 |
| tatqa | EXACT_IFC | CLEAN | 60 | 53 | 29 | 0.48333333333333334 | 0.5471698113207547 |
| tatqa | FLOWFENCE_R2 | CLEAN | 60 | 53 | 27 | 0.45 | 0.5094339622641509 |
| tatqa | FLOWFENCE_RECOVERY | CLEAN | 20 | 19 | 8 | 0.4 | 0.42105263157894735 |
| tatqa | EXACT_IFC | CONTAMINATION_A | 60 | 51 | 24 | 0.4 | 0.47058823529411764 |
| tatqa | FLOWFENCE_R2 | CONTAMINATION_A | 60 | 0 | 0 | 0.0 | None |
| tatqa | FLOWFENCE_RECOVERY | CONTAMINATION_A | 60 | 55 | 28 | 0.4666666666666667 | 0.509090909090909 |
| tatqa | EXACT_IFC | CONTAMINATION_B | 60 | 50 | 21 | 0.35 | 0.42 |
| tatqa | FLOWFENCE_R2 | CONTAMINATION_B | 60 | 0 | 0 | 0.0 | None |
| tatqa | FLOWFENCE_RECOVERY | CONTAMINATION_B | 60 | 57 | 28 | 0.4666666666666667 | 0.49122807017543857 |

## Table C — raw-value privacy

| family | defense | condition | TRUE | FALSE | UNKNOWN |
| --- | --- | --- | --- | --- | --- |
| hotpot | EXACT_IFC | CLEAN | 0 | 55 | 5 |
| hotpot | FLOWFENCE_R2 | CLEAN | 0 | 54 | 6 |
| hotpot | FLOWFENCE_RECOVERY | CLEAN | 0 | 17 | 3 |
| hotpot | EXACT_IFC | CONTAMINATION_A | 0 | 54 | 6 |
| hotpot | FLOWFENCE_R2 | CONTAMINATION_A | 0 | 0 | 60 |
| hotpot | FLOWFENCE_RECOVERY | CONTAMINATION_A | 0 | 57 | 3 |
| hotpot | EXACT_IFC | CONTAMINATION_B | 0 | 49 | 11 |
| hotpot | FLOWFENCE_R2 | CONTAMINATION_B | 0 | 0 | 60 |
| hotpot | FLOWFENCE_RECOVERY | CONTAMINATION_B | 0 | 53 | 7 |
| tatqa | EXACT_IFC | CLEAN | 0 | 54 | 6 |
| tatqa | FLOWFENCE_R2 | CLEAN | 0 | 53 | 7 |
| tatqa | FLOWFENCE_RECOVERY | CLEAN | 0 | 19 | 1 |
| tatqa | EXACT_IFC | CONTAMINATION_A | 0 | 52 | 8 |
| tatqa | FLOWFENCE_R2 | CONTAMINATION_A | 0 | 0 | 60 |
| tatqa | FLOWFENCE_RECOVERY | CONTAMINATION_A | 0 | 55 | 5 |
| tatqa | EXACT_IFC | CONTAMINATION_B | 0 | 50 | 10 |
| tatqa | FLOWFENCE_R2 | CONTAMINATION_B | 0 | 0 | 60 |
| tatqa | FLOWFENCE_RECOVERY | CONTAMINATION_B | 0 | 57 | 3 |

## Table D — recovery integrity

| treatment_reaching | quarantine_committed | recovery_attempted | original_artifact_released | artifact_writer_exposure | artifact_reentry | valid_provenance | writer_invoked | final_produced |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 223 | 223 | 223 | 0 | 0 | 0 | 223 | 223 | 222 |

## Task-level descriptive comparisons

| family | condition | baseline | paired_tasks | equal_weight_success_difference | equal_weight_final_difference |
| --- | --- | --- | --- | --- | --- |
| tatqa | CONTAMINATION_A | EXACT_IFC | 20 | 0.06666666666666668 | 0.05 |
| tatqa | CONTAMINATION_A | FLOWFENCE_R2 | 20 | 0.4666666666666667 | 0.9166666666666666 |
| hotpot | CONTAMINATION_A | EXACT_IFC | 20 | -0.01666666666666666 | 0.05 |
| hotpot | CONTAMINATION_A | FLOWFENCE_R2 | 20 | 0.08333333333333333 | 0.95 |
| tatqa | CONTAMINATION_B | EXACT_IFC | 20 | 0.11666666666666667 | 0.11666666666666667 |
| tatqa | CONTAMINATION_B | FLOWFENCE_R2 | 20 | 0.4666666666666667 | 0.95 |
| hotpot | CONTAMINATION_B | EXACT_IFC | 20 | 0.1 | 0.06666666666666668 |
| hotpot | CONTAMINATION_B | FLOWFENCE_R2 | 20 | 0.15 | 0.8833333333333334 |

Task-level rows, equal-weight means and original evaluator metric vectors are retained in derived/. Repetitions are not independent semantic samples. No new significance method or pooled cross-benchmark utility is introduced. Exact IFC comparisons are descriptive; neither superiority nor equivalence is established. Historical versus new runs may differ in provider time/cohort. CLEAN one-repetition results are only a regression check.

Recognized-artifact writer exposure: 0; reentry: 0. Terminal R2 has zero writer exposure and zero treatment-reaching contaminated finals. Recovery produced 222 finals after 223 recovery attempts. These counts must be read with pre-handoff failures and provenance availability, not interpreted as general confidentiality.

This implementation reconstructs from public task/evidence only; it has no independent structured finance result. Zero reentry plus nonzero continuation would support only the bounded claim that terminal rejection is not architecturally necessary under this separation. Low or zero utility is retained without tuning. TRUE/FALSE/UNKNOWN use the frozen observation rule; no exposure is not automatically FALSE. No paper claim is promoted and no anonymous manuscript is edited.

Termination accounting: {"SUCCESSFUL_FINAL": 258, "PROVIDER_FAILURE": 4, "PROTOCOL_FAILURE": 18}

STOP for human scientific review. No further experiment, retry, merge or paper revision is authorized by this report.

## Authorized reporting interruption and continuation

The formal run stopped after10CLEANobservations because in-flight IDs overlapped unattempted IDs. Human review classified this as reporting-only and retained all10observations without rerun. The reporting correction and partition validation preceded every contaminated recovery execution. The original STOP and defective snapshots remain immutable. Remaining270identities are dispatched once by attempted-ID membership. Scientific recovery implementation remains e9847b72da1db61d2e3d62837897259298614f98.

HARD_STOP_SHA: 7ae4b5986ba7655f1f0b7f4be2a4dfd6ecdf99ad; AMENDMENT_SHA: e55b1ed805e7104ccf2f535d168750d2ccd75337; REPORTING_FIX_SHA: 2a627c2e8d99c1b636ff28a21f94498f8b371ec0.

Accounting: scheduled=280, attempted=280, finished=280, in_flight=0, unattempted=0. Historical reporting defects corrected:1. New episode implementation defects:0.

## Final endpoint interpretation and explicit denominators

Observed security preservation: original recognized-artifact writer exposure0/223under recovery, compared descriptively with0/215under historical terminal R2. All223reconstructions have source-object provenance with artifact_sources=[]; quarantined artifact re-entry0/223. These are observed counts under the fixed recognizer/templates, not a guarantee against unrecognized or semantic attacks.

Observed availability recovery:222/223treatment-reaching contaminated finals (99.55%), compared with0/215under terminal R2. Unconditionally, recovery produces222/240contaminated finals (92.50%), compared with0/240terminal R2. The17pre-treatment failures remain in attempted denominators and are not recovery successes. One additional TAT-QA protocol failure occurred after recovery invoked the writer; it has UNKNOWN privacy, not a successful final. All223recovery attempts invoked writer.

Native utility in the contaminated main experiment:

| Benchmark | Defense | Attempted | Scored | Native success | Success/attempted | Success/scored |
| --- | --- | --- | --- | --- | --- | --- |
| TAT-QA | FLOWFENCE_RECOVERY | 120 | 112 | 56 | 46.67% | 50.00% |
| TAT-QA | EXACT_IFC (historical) | 120 | 101 | 45 | 37.50% | 44.55% |
| TAT-QA | FLOWFENCE_R2 (historical) | 120 | 0 | 0 | 0.00% | undefined |
| HotpotQA | FLOWFENCE_RECOVERY | 120 | 110 | 14 | 11.67% | 12.73% |
| HotpotQA | EXACT_IFC (historical) | 120 | 103 | 9 | 7.50% | 8.74% |
| HotpotQA | FLOWFENCE_R2 (historical) | 120 | 0 | 0 | 0.00% | undefined |

Within treatment-reaching recovery only, TAT-QA native success is56/113reached and56/112scored; HotpotQA14/110reached and14/110scored. These conditional denominators supplement, never replace, attempted denominators. Original EM/F1/scale/operation and Hotpot answer/support/joint metric means and per-episode vectors are retained under combined/derived. No utility is pooled across benchmarks. Task-level equal-weight and paired summaries use20tasks per benchmark, with3repetitions per condition; no significance or superiority/equivalence claim is made.

CLEAN regression:40attempted,36finals/scored,2provider failures and2protocol failures; recovery triggered0, implementation defects0. TAT-QA8/20attempted and8/19scored; HotpotQA3/20and3/17. This single-repetition regression is not a main statistical estimate.

Overall280observations:258SUCCESSFUL_FINAL,4PROVIDER_FAILURE,18PROTOCOL_FAILURE; no evaluator failure, new implementation defect, retry or rerun. Overall raw-value privacy TRUE0/FALSE258/UNKNOWN22. Contaminated-only TRUE0/FALSE222/UNKNOWN18; treatment-reaching TRUE0/FALSE222/UNKNOWN1. Unknown remains unknown and no-exposure alone is not FALSE. Total804provider request attempts, all built by the unchanged original request builder; no model calls were made for summarization.

The bounded systems observation is zero quarantined-artifact causal re-entry together with nonzero workflow continuation from immutable task/evidence. Utility is incomplete, especially HotpotQA joint EM, and no independent structured finance computation was retained. This is task-state reconstruction, not recovery of finance reasoning. Historical comparisons have cohort/time confounding and do not establish superiority. Human scientific review must decide the paper interpretation; no manuscript was modified.

## Evidence integrity and handoff

Postrun PASS: historical720identities and5648historical private files unchanged; original10CLEANobservations,26safe evidence files,86private files, original STOP and all defect evidence unchanged. Scientific recovery source, recognizer, attacks, task subset/order, prompts/schema, model/provider/evaluator and reporting-fix source remain unchanged. All280identities occur exactly once in the original order;270new identities have no overlap with the retained10. Private3104files have600permissions and directories700.

Preregistration677f32ab81fa08f2d5541bbb2f9c1f9dc87884a2; scientific implementatione9847b72da1db61d2e3d62837897259298614f98; hard-stop7ae4b5986ba7655f1f0b7f4be2a4dfd6ecdf99ad; amendmente55b1ed805e7104ccf2f535d168750d2ccd75337; reporting fix2a627c2e8d99c1b636ff28a21f94498f8b371ec0. These SHAs have distinct meanings. Final/remote evidence HEAD is the commit delivering this report, reported in the human handoff; it is not a scientific implementation revision.

Continuation session22399exited0 at2026-09-22T10:23:51.423630Z. No further formal calls are authorized. The original report remains byte-preserved at artifacts/aamas2027_qrecovery/combined/historical_hard_stop_report.md and in hard-stop commit7ae4b59. Machine evidence: combined/derived/{execution_summary,treatment_reachability,recovery_provenance_summary,privacy_summary,evaluator_summary,failure_audit,task_level_summary,endpoint_denominators,saved_evidence_audit}.json; combined/postrun_integrity.json; continuation/run; reporting amendment/test artifacts.

**QRECOVERY_FORMAL_FINISHED — STOP for human scientific review.** Do not merge, tune, rerun or edit the AAMAS manuscript automatically.
