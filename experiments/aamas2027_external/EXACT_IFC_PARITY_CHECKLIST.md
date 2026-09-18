> Gate A-C supersedes this earlier checklist: see EXACT_IFC_PARITY_AUDIT.md.

# EXACT_IFC parity audit

Direct callable parity is feasible and tested; integrated benchmark parity is not yet verified.

| Required capability | Same input path | Evidence / limit |
|---|---|---|
| protected-value registry | secret_policies | Same SecretPolicy list passed to both frozen callables in24 static fixtures |
| authorization policy | same SecretPolicy object | allowed_recipients and forbidden_channels identical |
| actor / recipient | actor_id / recipient_id | Same values passed; no role renaming to legacy enterprise IDs |
| surface | channel / target_zone | Same shared_doc mapping in fixtures; remaining release mapping pending |
| raw artifact | content | Exact same text before either call |
| abstraction | allowed_abstraction_level | Same 'none' value in fixtures; arbitrary new coarse abstraction strings unsupported by existing hardcoded coarse_safe_view mapping |
| topology metadata | topology | Same Topology instance, explicit edges; no dynamic privilege registry invented |
| evaluator/annotations | no access | attack_annotation=None; no benchmark gold passed |

Existing inspect_mas_event returns early for ifc_safeview; inspect_r2_event delegates legacy non-oracle decision and applies its frozen propagation override. We do not replace that legacy behavior with a new invented exact-then-recognizer implementation. Its existing risk/privilege behavior remains part of frozen R2. Direct-call fixtures establish matching available inputs, not universal equivalence of decisions.

Blocked: no MARBLE mediator covers every planner/message/tool/workspace release yet. Topology IDs and privilege_level use historical registries; unknown official roles receive the existing default level0, not an inferred task-specific privilege. New private policy registries can hold official IDs, but their mapping needs an adapter proof. Changing the frozen privilege registry or coarse safe-view semantics is forbidden.

EXACT_IFC_PARITY: NOT_VERIFIED
