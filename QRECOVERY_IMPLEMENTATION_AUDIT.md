# QRecovery implementation audit

Preregistration SHA: 677f32a (full SHA in run/registration.json). Implementation SHA: the first commit adding src/e2_live/qrecovery.py and scripts/run_qrecovery.py; resolved full SHA is required by the runner and saved before dispatch. Baseline342599f8e6884bafb333fa0bf99b0543352d88ed.

Added TrustedStateRecoveryPolicy, RecoveryEpisode subclass and one-shot CLI. Frozen V3 executes all original stages, transport, privacy definition, finalization, budgets and evaluator. No global ARMS mutation: construction selects existing R2, then restores the new reporting label. Only the existing B2 finance-to-writer quarantine rejection can trigger reconstruction. The quarantined payload and the pending finance handoff are discarded. All other rejections retain frozen termination behavior.

Source-object provenance: canonical detached task serialization occurs before provider generation; no planner/finance/private-note fields are trusted. Policy accepts serialized public task, empty extra state, and typed metadata containing artifact ID/reason code only. No payload/attack/template/oracle argument. Every task field is copied from that initial task object with path and source ID. Runtime B1 supplies TASK_STATE again and must equal reconstruction. Actual writer snapshot has task-only context and empty history. Runtime artifact-parent graph is checked for the quarantined ID; payload similarity is not the proof. Full source objects and writer snapshot are private auditable files, safe logs contain field provenance only.

Static original protocol and runtime authorization metadata are configuration, not recovered semantic fields. Recovery uses the original writer prompt/schema without extra instructions. As no independent structured finance fields exist, this is task-only recovery; neither preservation of intermediate computation nor utility success is assumed.

Synthetic preflight: scripts/check_qrecovery.py; both benchmarks A/B quarantine-and-continue, source invariant, three payload mutations per A/B case with exact actual-request equality, clean exact request/termination/budget parity to V3, early/model/protocol failure accounting and UNKNOWN privacy, rejection of nonempty extra state, corrupted-provenance stop before writer. Fixtures have SYNTHETIC identities and no formal input tasks. Zero network/provider calls.

Integrity preflight: scripts/run_qrecovery.py --preflight-only; reused original source/runtime checks (58 prereg files,45 R3files,67D1files), all720historical identities,5648private historical file digests,407protected tracked source/evidence paths. Checks PASS. Existing hashes are necessary for untracked local raw evidence and external source provenance not covered by Git. No new generic gate/contract framework.

No-oracle guarantee is scoped to this trusted implementation, not hostile Python reflection or OS compromise. Gold answers enter only the original evaluator after finalization. Recovery never reads evaluator objects or policy/attack templates. The surrounding original treatment generator still reads its frozen templates to instantiate the attack.

All ordinary failures remain attempted observations. Invalid provenance is a hard-stop implementation defect; no automatic patch/resume after formal start. A failed writer retains its original termination plus RECOVERY_WRITER_FAILURE. No clean task selection or outcome tuning. Source-only old evidence is byte protected and never dispatched again.

Resolved preregistration SHA: 677f32ab81fa08f2d5541bbb2f9c1f9dc87884a2.
Resolved implementation SHA: e9847b72da1db61d2e3d62837897259298614f98.

Post-dispatch reporting defect: scripts/summarize_qrecovery.py was added for saved-evidence analysis after the frozen runtime commit. Its live in-flight/unattempted overlap triggered a mandatory stop; source remains unpatched. See implementation_defect.json, synthetic reproduction, and formal report hard-stop supplement. Runtime remains frozen and all10retained observations are CLEAN; no formal recovery endpoint is observed.
