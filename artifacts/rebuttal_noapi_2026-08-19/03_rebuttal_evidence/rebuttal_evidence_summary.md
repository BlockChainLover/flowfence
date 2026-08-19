# WINE 2026 Rebuttal - No-API Supplemental Evidence

## Experiment A: Component Ablation

### Setup

The matched non-oracle deterministic matrix uses 3 topologies, 10 attacks, and 3 seeds. FULL and NO_SEMANTIC_PATTERNS were schema-refreshed because historical raw per-run traces were no longer present remotely; the three new variants account for 270 new runs. Thresholds, attacks, topology definitions, policy, and seeds were unchanged.

### Main results

- FULL: task=1.0, raw=0.0, external=0.0, cascade=2.7/2.7, privilege=0.0
- NO_SEMANTIC_PATTERNS: task=1.0, raw=1.5, external=0.0, cascade=4.5/3.5, privilege=1.8
- NO_SAFE_VIEW: task=1.0, raw=0.0, external=0.0, cascade=2.7/2.7, privilege=0.0
- NO_TOPOLOGY_FANOUT: task=1.0, raw=0.0, external=0.0, cascade=2.7/2.7, privilege=0.0
- NO_PROPAGATION_RIGHT_NARROWING: task=1.0, raw=0.0, external=0.0, cascade=2.7/2.7, privilege=0.0

### What the data support

The table measures each component's association with exact raw leakage, external leakage, deterministic cascade, privilege reach, and rule-based task completion in this synthetic runtime.

### What the data do NOT support

These results do not establish semantic utility, production robustness, provider generalization, or capability enforcement by propagation-right metadata.

## Experiment B: Composite Defense Baseline

### Baseline definition

ACL_CONTENT_RUNTIME combines the existing Static ACL rule with the existing direct prompt-filter surface rule at runtime transitions and final/external transitions. It blocks on a match and uses no provenance, fanout, privilege-risk score, safe-view, quarantine store, lease narrowing, PAPC risk fusion, or evaluator labels.

### Main results

- STATIC_ACL: task=1.0, raw=4.633333, external=0.533333, cascade=5.4/3.9, privilege=4.5
- PROMPT_FILTER: task=0.4, raw=7.866667, external=1.533333, cascade=4.5/3.5, privilege=3.0
- ACL_CONTENT_RUNTIME: task=0.4, raw=2.233333, external=0.166667, cascade=4.5/3.5, privilege=1.8
- FLOWFENCE_NONORACLE: task=1.0, raw=0.0, external=0.0, cascade=2.7/2.7, privilege=0.0

### Matched comparison against FlowFence

- Raw: FlowFence better 39 / tie 51 / worse 0
- External: FlowFence better 15 / tie 75 / worse 0
- Task: FlowFence better 54 / tie 36 / worse 0

### What the data support

The matched counts characterize this explicit defense-in-depth comparator on the same deterministic topology-attack-seed groups.

### What the data do NOT support

The clean-case block rate is only a deterministic blocking proxy. It is not a semantic utility or user-quality judgment.

## Unexpected / Negative Results

- NO_SAFE_VIEW is reported even if task success remains unchanged; the current scripted final writer can preserve the fixed safe template after blocking, so this benchmark may not expose safe-view's utility benefit.
- NO_TOPOLOGY_FANOUT is reported as neutral if exact-policy and semantic signals already dominate the unchanged threshold.
- NO_PROPAGATION_RIGHT_NARROWING is expected to be outcome-neutral because lease signals are metadata-only and do not gate downstream execution in this implementation.
- Any composite wins or ties remain visible in the matched CSV and counts above.

## Candidate numbers for rebuttal

Use only the values in the two main tables and matched counts above, with the deterministic-runtime caveat. Human review is required before citing them; this script does not modify the paper.
