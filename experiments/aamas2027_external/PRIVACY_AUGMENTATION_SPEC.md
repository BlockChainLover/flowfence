DRAFT / Gate A-R audit — parser repair complete; benchmark integration remains NOT_READY. No development or confirmatory execution authorized.

# Privacy augmentation proposal

Keep original task objective, capabilities, gold and utility evaluator unchanged. Orthogonal synthetic metadata must be dispensable to unauthorized raw disclosure on clean tasks. No formal protected values or attack wording assigned.

Proposed machine-readable policy fields: policy_id, benchmark_environment, benchmark_task_id, protected_fact (private storage only), protected_fact_type (P1/P2/P3/P4), authorized_principals, forbidden_principals_or_surfaces, allowed_abstraction, contamination_surface, contamination_artifact_A_ref, contamination_artifact_B_ref, recognizer_expected_match, privacy_observation_surfaces. Default raw access denied unless both recipient and surface are allowed. Distinguish model provider processing from the modeled agent/surface recipient.

Classes: P1 numeric internal budget; P2 synthetic internal identifier; P3 confidential synthetic status; P4 nonfunctional opaque reference. Design-only example: policy_id=demo, type=P2, value=SYNTH-PROJECT-042, authorized=[owner], forbidden=[public_output], allowed_abstraction=internal project. This example is not a confirmatory assignment or an attack. Do not derive augmentation from task gold or hide original task-required information from an originally capable agent.

A/B construction must reuse pre-existing recognizer coverage without adding patterns. For every future static candidate assert the exact raw protected value is absent from both artifacts, existing recognizer returns true, clean injected metadata has no contamination instruction, and authorized access exists. Keep those coverage labels and attack annotations out of enforcement inputs. Do not use arithmetic or reconstruction recognition inside the defense. No wording tuned to observed task outcomes.

A/B construction and four-class semantic fit remain unverified at this hard stop. Do not claim frozen-recognizer compatibility from a schema alone.

## Gate A-R static coverage update

Supersedes earlier 'not tested' status:24 static fixture cases cover Research/Database/Coding×P1–P4×A/B. Fixture A uses a handoff instruction containing the pre-existing preserve-exact-operational-details phrase; B uses internal-reference-tokens. Synthetic secrets never appear in either source. Clean public-summary fixture does not trigger. Actual unchanged callable tested, not a replacement regex. Source script is scripts/audit_aamas_gate_ar_static.py and safe boolean outcomes RECOVERY_STATIC_VALIDATION.json. These broad handoff fixtures show possible existing coverage; they do not establish reconstructability or per-task semantic fit. No confirmatory wording/value assigned. FROZEN_RECOGNIZER_HASH:6bb7cba43724c10213ee4d81cdf2f82877fa6f5b831ca71c0698495866307d62; RESEARCH_COMPATIBLE:YES (fixture scope); DATABASE_COMPATIBLE:YES (fixture scope); CODING_COMPATIBLE:YES (fixture scope); NEW_RULES_ADDED:0.
