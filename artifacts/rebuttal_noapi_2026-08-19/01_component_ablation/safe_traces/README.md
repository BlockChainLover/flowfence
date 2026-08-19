# Component Ablation Safe Traces

These files contain only redacted deterministic event previews plus metrics and source raw-trace paths.

- `case_01_no_safe_view.json`: The current deterministic task shows equal privacy and task-success outcomes; this is a neutral utility ablation.
- `case_02_semantic_summary.json`: Semantic patterns change containment for this attack family.
- `case_03_semantic_workspace.json`: Held-out surface wording exposes the semantic-pattern dependency.
- `case_04_topology_fanout.json`: Outcome metrics are neutral; the trace records whether the fanout-only risk signal changed the decision.
- `case_05_propagation_right.json`: Outcome metrics are neutral because lease narrowing is metadata-only in this runtime.
