# BIRD lossless context candidate — C0 offline contract

Status: offline candidate only, **not a certified context-limit fix** and not connected to a live runner. Explicitly requested by the human C0 audit; no additional execution gate or frozen experiment contract is introduced.

## Input and representation

Input is one already-mediated V3 BIRD stage snapshot. The generic function applies identically to every task and arm and has no task-ID, gold, schema-pruning or row-selection branch.

`BIRD_RELEASED_CONTEXT_SINGLE_COPY_V1` retains a deep copy of every snapshot field except `values` and `history` in `header`. It interns only byte-identical canonical values from those two lists into a per-invocation `released_value_pool`. Ordered `values_pool_indices` and `history_pool_indices` preserve every original occurrence. Equal bytes may share storage, but their original artifact and provenance references remain separate in the unchanged invocation header. No cross-request pool, filesystem/runtime lookup, state cache, or new model tool exists.

Every referenced value is embedded in the same packet and was already released to that invocation's recipient. Expansion reconstructs the exact original snapshot. The semantic test independently compares sorted unique canonical released-value sets. No summary, truncation, type conversion, SQL result deletion, schema deletion, budget reduction or benchmark-capability change is permitted. Nested equal CSV descriptions are measured but conservatively retained; this candidate targets the dominant exact history/scratch duplicate.

## Provenance and mediation

Packing occurs conceptually **after** the existing runtime context/history releases. The offline helper never calls a runtime, reads an artifact by ID or changes a decision. Existing producer/recipient, authorization, lineage, mediation decisions and released value identities remain in their original trusted records. Original invocation artifact/provenance references remain in the packet header; ordered occurrences preserve their association. The packet is not a new authority source and must never be accepted as permission to read runtime state.

Expansion accepts only this representation's exact top-level fields, rejects header collisions and rejects negative, boolean, or out-of-range indices. It returns detached copies. Caller mutation of packet or expanded values cannot change the original snapshot/runtime; modifying an expanded value cannot change the packet. Only embedded released values can be returned. Private finance data stays in finance's authorized input; writer access to the private key remains rejected. Evaluator inputs are absent from these public-task fixtures and are not accessed by either helper.

## Certification evidence

`root_cause.json`: all six real failures reproduce saved accepted requests and last released views; exact expansion and semantic sets verified. Saved input/content is never inferred.

`static_context.json`: 29 selected public inputs × 2 arms × 2 deterministic profiles; 1,508 finance snapshots and 116 planner snapshots. Tests verify exact expansion, unique semantic-item equality, unchanged invocation references, unchanged release events, detached values, malformed reference rejection, private writer denial and planner private-data absence. 754 paired finance snapshots are byte-identical after packing across arms. Both arms retain frozen tools, budgets, stage routing, evaluator and failure policies: no live code/config is edited. Static fixtures call no model or evaluator and do not establish model interpretation equivalence.

- BIRD_CONTEXT_SEMANTIC_EQUIVALENCE: **VERIFIED** for offline representation and expansion.
- BIRD_CONTEXT_PARITY: **VERIFIED** for offline candidate; frozen live settings unchanged.
- BIRD_CONTEXT_MEDIATION: **VERIFIED** for the existing in-process capability boundary and offline helper; no claim about OS/reflection attacks.

These certifications do not imply guard closure or authorization to deploy this representation.

## Size and failure policy

The existing 160,000 UTF-8-byte messages guard remains unchanged. Size calculation uses the frozen original prompt/schema and the candidate packet; a new explanatory prompt would add bytes. Even this optimistic measurement leaves all six observed failures above the guard, maximum 817,657 bytes. The single 706,360-byte SQL result remains present. Removing schema duplication cannot resolve that result alone.

The frozen SQL capability has no finite result-size bound; twelve actions cannot establish a finite byte bound. A fixed fixture maximum is never labeled the absolute worst case. Candidate failure means **LOSSLESS_FIX_NOT_FEASIBLE**, no live binding, no guard adjustment, no new task selection, and a return to human decision. This does not prove impossibility for every mathematical compression scheme, nor certify compressed binary text as equivalent model-readable context.

## Prospective validation

Only a separately certified feasible fix could trigger the requested precommitted selection rule, selection of three disjoint fresh BIRD tasks and human review of the future 18-cell matrix. C0 creates none of those artifacts or IDs. There is no authorization for those cells, confirmatory models or formal models.
