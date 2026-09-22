# QRecovery formal report

Status: INCOMPLETE_OR_STOPPED. Preregistration 677f32ab81fa08f2d5541bbb2f9c1f9dc87884a2; implementation e9847b72da1db61d2e3d62837897259298614f98.

Scheduled280; attempted10; finished10; clean10; contaminated0; implementation defects0. Every ordinary failure stays in attempted denominators. Historical720unchanged and never rerun.

## Table A — containment and continuation (contaminated)

| defense | attempted | treatment_reaching | original_artifact_released | original_artifact_reaches_writer | quarantined | recovery_attempted | writer_invoked_after_quarantine | schema_valid_finals |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EXACT_IFC | 240 | 215 | 215 | 215 | 0 | 0 | 0 | 205 |
| FLOWFENCE_R2 | 240 | 215 | 0 | 0 | 215 | 0 | 0 | 0 |
| FLOWFENCE_RECOVERY | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |

## Table B — native utility (separate benchmarks)

| family | defense | condition | attempted | scored | native_success | success_over_attempted | success_over_scored |
| --- | --- | --- | --- | --- | --- | --- | --- |
| hotpot | EXACT_IFC | CLEAN | 60 | 55 | 4 | 0.06666666666666667 | 0.07272727272727272 |
| hotpot | FLOWFENCE_R2 | CLEAN | 60 | 54 | 3 | 0.05 | 0.05555555555555555 |
| hotpot | FLOWFENCE_RECOVERY | CLEAN | 5 | 4 | 0 | 0.0 | 0.0 |
| hotpot | EXACT_IFC | CONTAMINATION_A | 60 | 54 | 6 | 0.1 | 0.1111111111111111 |
| hotpot | FLOWFENCE_R2 | CONTAMINATION_A | 60 | 0 | 0 | 0.0 | None |
| hotpot | EXACT_IFC | CONTAMINATION_B | 60 | 49 | 3 | 0.05 | 0.061224489795918366 |
| hotpot | FLOWFENCE_R2 | CONTAMINATION_B | 60 | 0 | 0 | 0.0 | None |
| tatqa | EXACT_IFC | CLEAN | 60 | 53 | 29 | 0.48333333333333334 | 0.5471698113207547 |
| tatqa | FLOWFENCE_R2 | CLEAN | 60 | 53 | 27 | 0.45 | 0.5094339622641509 |
| tatqa | FLOWFENCE_RECOVERY | CLEAN | 5 | 4 | 2 | 0.4 | 0.5 |
| tatqa | EXACT_IFC | CONTAMINATION_A | 60 | 51 | 24 | 0.4 | 0.47058823529411764 |
| tatqa | FLOWFENCE_R2 | CONTAMINATION_A | 60 | 0 | 0 | 0.0 | None |
| tatqa | EXACT_IFC | CONTAMINATION_B | 60 | 50 | 21 | 0.35 | 0.42 |
| tatqa | FLOWFENCE_R2 | CONTAMINATION_B | 60 | 0 | 0 | 0.0 | None |

## Table C — raw-value privacy

| family | defense | condition | TRUE | FALSE | UNKNOWN |
| --- | --- | --- | --- | --- | --- |
| hotpot | EXACT_IFC | CLEAN | 0 | 55 | 5 |
| hotpot | FLOWFENCE_R2 | CLEAN | 0 | 54 | 6 |
| hotpot | FLOWFENCE_RECOVERY | CLEAN | 0 | 4 | 1 |
| hotpot | EXACT_IFC | CONTAMINATION_A | 0 | 54 | 6 |
| hotpot | FLOWFENCE_R2 | CONTAMINATION_A | 0 | 0 | 60 |
| hotpot | EXACT_IFC | CONTAMINATION_B | 0 | 49 | 11 |
| hotpot | FLOWFENCE_R2 | CONTAMINATION_B | 0 | 0 | 60 |
| tatqa | EXACT_IFC | CLEAN | 0 | 54 | 6 |
| tatqa | FLOWFENCE_R2 | CLEAN | 0 | 53 | 7 |
| tatqa | FLOWFENCE_RECOVERY | CLEAN | 0 | 4 | 1 |
| tatqa | EXACT_IFC | CONTAMINATION_A | 0 | 52 | 8 |
| tatqa | FLOWFENCE_R2 | CONTAMINATION_A | 0 | 0 | 60 |
| tatqa | EXACT_IFC | CONTAMINATION_B | 0 | 50 | 10 |
| tatqa | FLOWFENCE_R2 | CONTAMINATION_B | 0 | 0 | 60 |

## Table D — recovery integrity

| treatment_reaching | quarantine_committed | recovery_attempted | original_artifact_released | artifact_writer_exposure | artifact_reentry | valid_provenance | writer_invoked | final_produced |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |

## Task-level descriptive comparisons

| family | condition | baseline | paired_tasks | equal_weight_success_difference | equal_weight_final_difference |
| --- | --- | --- | --- | --- | --- |
| tatqa | CONTAMINATION_A | EXACT_IFC | 0 | None | None |
| tatqa | CONTAMINATION_A | FLOWFENCE_R2 | 0 | None | None |
| hotpot | CONTAMINATION_A | EXACT_IFC | 0 | None | None |
| hotpot | CONTAMINATION_A | FLOWFENCE_R2 | 0 | None | None |
| tatqa | CONTAMINATION_B | EXACT_IFC | 0 | None | None |
| tatqa | CONTAMINATION_B | FLOWFENCE_R2 | 0 | None | None |
| hotpot | CONTAMINATION_B | EXACT_IFC | 0 | None | None |
| hotpot | CONTAMINATION_B | FLOWFENCE_R2 | 0 | None | None |

Task-level rows, equal-weight means and original evaluator metric vectors are retained in derived/. Repetitions are not independent semantic samples. No new significance method or pooled cross-benchmark utility is introduced. Exact IFC comparisons are descriptive; neither superiority nor equivalence is established. Historical versus new runs may differ in provider time/cohort. CLEAN one-repetition results are only a regression check.

Recognized-artifact writer exposure: 0; reentry: 0. Terminal R2 has zero writer exposure and zero treatment-reaching contaminated finals. Recovery produced 0 finals after 0 recovery attempts. These counts must be read with pre-handoff failures and provenance availability, not interpreted as general confidentiality.

This implementation reconstructs from public task/evidence only; it has no independent structured finance result. Zero reentry plus nonzero continuation would support only the bounded claim that terminal rejection is not architecturally necessary under this separation. Low or zero utility is retained without tuning. TRUE/FALSE/UNKNOWN use the frozen observation rule; no exposure is not automatically FALSE. No paper claim is promoted and no anonymous manuscript is edited.

Termination accounting: {"SUCCESSFUL_FINAL": 8, "PROVIDER_FAILURE": 1, "PROTOCOL_FAILURE": 1}

STOP for human scientific review. No further experiment, retry, merge or paper revision is authorized by this report.
