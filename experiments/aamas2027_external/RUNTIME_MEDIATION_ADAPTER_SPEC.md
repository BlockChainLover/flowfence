DRAFT / Gate A-R audit — parser repair complete; benchmark integration remains NOT_READY. No development or confirmatory execution authorized.

# Runtime adapter design boundary

No implementation added. The exact benchmark call-site map is incomplete because the shared evaluator cannot parse.

Proposed interface: mediate(event, protected_registry, authorization_policy, allowed_abstractions) -> decision + released_artifact. Both defenses receive identical actor/recipient, surfaces, state, raw artifact and registry. Existing exact mediation runs first on both arms. R2 uses its unchanged callable and propagation-surface mapping; only existing recognized contamination can trigger constant whole-artifact quarantine. Preserve original safe-view handling for ordinary exact raw violations and preserve hard blocks. No task ID, gold, attack annotation, evaluator verdict or alternate secret registry can enter the defense.

Required observable boundaries: agent sends and receives; shared memory reads/writes; shared documents and workspace files; private-to-shared scratchpad exports; delegation messages; tool arguments/results; external actions; final output; planner summaries and model-visible tool errors. Intercept before release, including any side effects. Mapping each to an existing R2 channel requires review; a new detector is forbidden. Logging an action after exposure is insufficient mediation.

Event proposal: episode_id, task_id, environment, step, sequence, actor, recipient, surface, artifact_id, parent_artifact_ids, private_content_ref, protected_policy_ids, mediation_decision, recognizer_signal, released_artifact_id, private_released_content_ref, disclosure_exact, timestamp, logical_generation_id, transport_attempt_id, outcome_status. Safe logs contain IDs/counts/booleans, not secret content or payload. Use sequential artifact IDs; no new content hash is needed. Low-entropy secrets must not be exposed through enumerable hashes. Protected text and full trajectories stay in access-restricted local audit storage.

Parity checklist (all pending): same registry; same ACL; same surface mapping; same actors; same state; same pre-release text; same abstractions; same exact decision path; same tools and prompts; same budgets; no gold/annotation access; only R2 quarantine increment. Require static mock fixtures at every release site after resumption, including blocked and marker-only release cases and exception paths.

Failures are separate execution_status (completed/model_failure/infrastructure_failure), evaluator_status and privacy_status (known/unknown). Never treat absent logs or parse errors as safe. Record all attempts and no model regeneration after response; audit nested SDK retries. Preserve original evaluator output alongside parse/failure annotations, without replacing its primary score.

## Gate A-R source audit correction

Parser blocker repaired; use MEDIATION_COVERAGE_MATRIX.md for actual release sites. No adapter installed. Direct same-input tests establish callable feasibility only. Preserve inspect_r2_event exactly, including its delegated legacy result; do not implement the earlier conceptual 'exact first' sentence as a new algorithm. Coarse safe-view mappings and privilege registry are frozen and not generalized. Integration parity remains NOT_VERIFIED. Nested coding model requests/file writes require hooks before side effect, not just returned-text mediation.
