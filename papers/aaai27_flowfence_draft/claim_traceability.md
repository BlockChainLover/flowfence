# Claim Traceability - Polished Draft

This file maps the major claims in the AAAI draft to committed evidence and allowed wording.

| Claim | Evidence | Allowed wording | Forbidden wording |
|---|---|---|---|
| Privacy leakage should be evaluated as propagation across runtime channels, not only final outputs. | Problem formulation; deterministic and MiniMax coverage tables | "event-level propagation across messages, memory, workspace, tools, and outputs" | "complete real-world agent safety" |
| FlowFence-Lite enforces a policy-preserving safe-view invariant under complete mediation and sound rewriting. | Proposition 1 in Method; implementation/evaluator assumptions | "formal invariant under stated assumptions" | "mathematical proof of production security" |
| Shared-artifact fanout can amplify contaminated reads. | Proposition 2; topology results | "fanout motivates topology-aware risk scoring" | "all blackboard systems are always unsafe" |
| P0 adapted AgentPoison comparator supports retrieval-memory containment. | Table 1; P0 summaries | "adapted comparator evidence" | "official AgentPoison reproduction" |
| MiniMax 252-run coverage supports FlowFence clean subset. | Table 3; coverage summaries | "MiniMax-backed synthetic-runtime coverage" | "real-world deployment evidence" |
| FlowFence improves or ties baselines on configured raw/external leakage comparisons. | Table 3 | "configured comparison groups" | "universally dominates all defenses" |
| Topology effects are observed in the synthetic-runtime benchmark. | Table 3 and seed/topology summaries | "observed in the synthetic-runtime benchmark" | "validated in real-world deployments" |
| Non-oracle held-out validation mitigates the oracle-label concern. | Table 7; non-oracle summaries | "substantially mitigates under configured held-out matrices" | "arbitrary attack robustness" |
| No-semantic-pattern ablation suggests semantic patterns contribute to raw-leakage containment. | Table 8 | "partial mechanism evidence" | "semantic detection is unnecessary" |
| Non-MiniMax generalization is unsupported. | Limitations and evidence boundaries | "not evaluated" | any positive claim |
