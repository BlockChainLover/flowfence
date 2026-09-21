# E2-A prospective reporting-only correction

Human approval received2026-09-21: cells001–053 are valid formal observations; the known defect is aggregation-only and affected no runtime/treatment/privacy/evaluator/defense/model/source semantics. Preserve original artifacts and never rerun those cells. Only054–720may execute in a new instance after this correction is committed and pushed.

Original preregistration: `2a8e3910a133862a0df9f53a47131d798da047c1`. Immutable original evidence commit: `f5f6fa8849df45c67de351dc719abab9e070e83b`. Record actual `E2A_REPORTING_FIX_COMMIT` in continuation registration before dispatch; no history rewrite.

## Correction

The auditor now accounts for a retained episode before trying to inspect its trajectory. For minimal IMPLEMENTATION_DEFECT records, missing stage/trajectory observations stay explicitly null/UNAVAILABLE. Observed-success totals count only explicit true values, with unavailable-stage counts separately reported. Termination and validity are preserved. Absent privacy/task outcomes contribute UNKNOWN; existing values are retained without inference. A missing handoff observation is not a pre-handoff failure, a successful handoff, a treatment entry, or privacy success. The input episode records are emitted unchanged in the derived episode summary.

The existing original53records all have full evidence. Regression compares every existing field in all original derived JSON outputs and the complete release audit: no original outcome or interpretation changes. Original22safe files and439private files remain byte-identical.

## Authorized continuation adapter

New scripts/run_e2a_continuation.py admits exactly schedule[53:] (orders054–720), in existing order, keeping scientific namespace E2A_FORMAL_CONFIRMATORY and distinct run instance E2A_FORMAL_CONTINUATION_054_720_001. It uses the unchanged FormalEpisode/V3/provider/evaluator implementation. The original runner and stopped directory remain unchanged, including original STOP. CLI registration is tested with nonexistent credential/source paths to establish zero access/calls in registration-only mode. Remote fix commit, frozen configuration and original artifacts are checked before dispatch. Any new implementation defect hard-stops; no automatic patch or resume.

New scripts/summarize_e2a_combined.py creates temporary derived input and private symlink views of the two runs, then invokes the corrected auditor. It writes a combined provenance index and maps file references back to real originals. It never edits source runs or invokes a provider/evaluator. The report renderer accepts this derived combined registration and reports the historical correction separately.

## Validation

```sh
PYTHONPATH=.:/private/tmp/e2_s0_deps /opt/homebrew/bin/python3 scripts/check_e2a_reporting_fix.py --output artifacts/aamas2027_e2a_continuation/reporting_fix_validation.json
```

Checks: exact original zero-call fixture; contaminated missing-stage fixture; original53summary-field/release-audit invariance; all667suffix admissions;103invalid admission denials (001–053, BIRD, development, E2-B namespace and arbitrary IDs); actual CLI registration; empty-continuation combined prefix; combined original53plus minimal054failure and report rendering. No live model or original evaluator calls. All new/changed CLI --help/compile checks and frozen-file preservation are required before dispatch.

No runtime/scientific configuration change; no V4, retries, task replacements, evaluator edits, privacy judge, new fact rules, recognizer/IFC/R2 changes. R3 and original manifests stay unchanged. E2-B DEFERRED_NOT_SELECTED.40semantic tasks remain the intended sample;720episodes are repeated observations.
