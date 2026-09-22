# QRecovery prospective reporting amendment

Human decision: **AUTHORIZED_PROSPECTIVE_REPORTING_FIX_AND_CONTINUATION**.

- Original preregistration: `677f32ab81fa08f2d5541bbb2f9c1f9dc87884a2`.
- Frozen scientific implementation: `e9847b72da1db61d2e3d62837897259298614f98`.
- Hard-stop commit: `7ae4b5986ba7655f1f0b7f4be2a4dfd6ecdf99ad`.
- Amendment SHA: the commit first adding this document, resolved and recorded in reporting_amendment.json before any reporting code change or continuation.

The live summarizer classified unattempted cells from the set of finished episode IDs rather than attempted/started IDs. An in-flight cell could therefore be counted simultaneously as attempted and unattempted. The defect affects reporting/accounting only and does not alter episode execution, model requests, recovery semantics, provenance, privacy adjudication, evaluator outputs, or retained trajectories.

The 10 retained CLEAN observations remain part of the formal run. They MUST NOT be rerun. The remaining 270 never-attempted schedule identities may be continued exactly once after the reporting-only correction passes synthetic and saved-evidence validation. The retained results are 8 SUCCESSFUL_FINAL, 1 PROVIDER_FAILURE and 1 PROTOCOL_FAILURE; all10terminal, no contaminated attempt. Original720historical observations remain immutable.

Correct reporting takes scheduled IDs from the frozen schedule, attempted IDs from immutable start logs, and finished IDs from terminal episode records. It computes unattempted=scheduled−attempted and in-flight=attempted−finished. Enforce finished⊆attempted⊆scheduled and a disjoint complete finished/in-flight/unattempted partition. Counts are derived together, never independently overwritten. Duplicate start IDs are an integrity error, never additional scientific observations or silently ignored dispatches.

Before continuation validate zero-attempt, in-flight, finished, mixed and duplicate-start synthetic cases, plus the retained10saved trajectories, requests, evaluator outputs, privacy, termination, provenance and logs. Preserve every historical defect file and original STOP unchanged. Record amendment SHA and a separate REPORTING_FIX_SHA; neither replaces the scientific implementation SHA.

Continuation uses schedule membership against already-attempted IDs, not numeric slicing. Preserve the original run directory and private evidence; write remaining270observations into new continuation directories and combine read-only. Remaining30CLEANprecede the unchanged240contaminated cells. No retries, replacements, extra episodes or model/prompt/schema/attack/recognizer/evaluator/privacy/recovery changes. Only reporting/accounting and minimal scheduler plumbing for this authorized suffix may change. A new implementation/provenance/reporting defect stops further dispatch and requires another human decision. Security failures remain evidence; never tune outcomes away.

Final reporting must retain interruption history, distinguish PREREG_SHA, SCIENTIFIC_IMPLEMENTATION_SHA, HARD_STOP_SHA, AMENDMENT_SHA, REPORTING_FIX_SHA and final/remote heads, report native utility by benchmark and task-based comparisons, and retain all ordinary failures. After final delivery update draft PR8 and stop for human scientific review; no manuscript edits, merge or extra experiments.
