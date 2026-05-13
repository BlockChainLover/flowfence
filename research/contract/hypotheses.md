# Hypotheses

## Main Hypothesis

- statement:
  A unified runtime containment layer that combines propagation-aware risk scoring, lease-based privilege control, shared-memory/workspace governance, and structured logging can reduce unauthorized privacy leakage and contamination propagation with modest utility loss relative to strong narrow baselines.
- what would support it:
  FlowFence-Lite beats `no defense` on all primary privacy metrics, beats at least 3 of 4 non-trivial defense baselines on unauthorized raw leakage, and does not trail the strongest baseline by more than 5% utility retention.
- what would falsify it:
  A narrow baseline dominates after utility normalization, gains disappear outside one topology/domain, or the defense causes excessive false blocks or runtime overhead.

## Secondary Hypotheses

- statement:
  Internal leakage across messages, memory, workspace, and tool arguments exceeds leakage visible from final outputs alone.
- why it matters:
  This justifies auditing internal channels and not relying on output-only privacy evaluation.
- minimum evidence needed:
  Internal raw leakage is meaningfully higher than final-output raw leakage in at least 2 domains.

- statement:
  Shared artifacts and topology materially change cascade size and privilege reach.
- why it matters:
  This motivates topology-aware evaluation and shared-artifact governance.
- minimum evidence needed:
  Blackboard or star differs meaningfully from chain or tree in at least 2 attack settings.

- statement:
  Shared-memory governance and runtime lease control are both necessary contributors.
- why it matters:
  This supports the system design and keeps the contribution from collapsing into one module.
- minimum evidence needed:
  At least 2 ablations show clear degradation on different axes, with one hurting leakage and one hurting cascade or privilege reach.
