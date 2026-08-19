# Experiment A - Mechanism Component Ablation

FULL is `flowfence_lite_nonoracle`. NO_SEMANTIC_PATTERNS disables all configured semantic request patterns. NO_SAFE_VIEW converts would-be safe-view rewrites to block and uses a quarantine marker rather than raw allow. NO_TOPOLOGY_FANOUT zeros only shared-workspace/shared-memory fanout risk features without threshold changes. NO_PROPAGATION_RIGHT_NARROWING keeps content decisions but removes lease revoke/downgrade signals; the low-risk downgrade-only branch becomes allow. Lease signals are metadata-only in this runtime.

New runs: 270/270; failures: 0. Reference schema-refresh runs: 180.
