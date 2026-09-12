# AAMAS 2027 supplemental experiments

Primary decision: does PAPC outperform a complete-mediation IFC-SafeView comparator with identical policy, protected-value detector, safe-view generator and validator?

The user explicitly requested E0–E3 and conditional E4/E5, pre-run config hashes and fixed task selection. No unrelated gate or frozen contract is introduced. WINE paper and archives remain read-only.

E0: one historical task × three topologies × ten attack settings × three seeds × three defenses = 270 episodes, 90 PAPC/IFC pairs. No Defense is a sanity/reference arm. Reuse the historical inputs and attack generators, but correct partial event interception, pre-mediation/truncated measurement, and defense-dependent final candidate generation in a shared additive adapter. Both arms receive the same complete mediation and common validator. PAPC means flowfence_lite_nonoracle; oracle labels are never supplied. This is an adapted corrected comparison, not exact historical replay.

Use only delivered content downstream. At quarantine, the raw source is hidden and only a validated generated safe view is made available through the same mediated route. No thresholds are retuned. Exact secret/event exposure, external exposed events and unique secret-recipient pairs are distinct metrics. Cascade counts delivered events carrying detected instructions or unauthorized raw values (explicitly differs from historical unconditional ancestral contamination). E0 utility retains the old rule checker and is weak; E1 adds config-grounded task state verification.

E1: preselected workspace_poisoning_indirect from saved no-defense deterministic raw exposure; existing one enterprise scenario is parameterized into 12 saved public task-state instances. 4-task pilot is separate. Formal 12 × 2 topologies × 2 conditions × 3 defenses × 1 seed. Report parametric template scope, not 12 independent domains.

E2: 3 mediator modes × 1K/10K/100K events × five repetitions; serialized audit bytes and mediation-only timer.

E3: fixed representation probes, no new detector, same-recipient history reconstruction. Ten task variants retain one underlying secret policy; no ten-secret-domain claim.

E4 only if an already configured different-family API is usable; E5 only on an E1 topology interaction. Do not rerun/tune after observing unfavorable outcomes.

Inference: E0 seed groups are descriptive repeated measurements of one task; task-cluster sign test cannot support population significance at n=1. E1 clusters parameterized instances, averages repeated conditions within each task; no seed pseudoreplication. All failures retained and no exclusions.

Outputs: artifacts/aamas2027. Every summary rebuilds from saved episode/audit JSONL, latency trial histograms or metric CSVs derived from them. Full credential files and private trajectories never enter Git or bundle.
