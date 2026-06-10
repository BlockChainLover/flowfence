# Claim Traceability - Polished Draft

This file maps the major claims in the AAAI draft to committed evidence and allowed wording.

| Claim | Evidence | Allowed wording | Forbidden wording |
|---|---|---|---|
| Privacy leakage should be evaluated as propagation across runtime channels, not only final outputs. | Problem formulation; deterministic and MiniMax coverage tables | "event-level propagation across messages, memory, workspace, tools, and outputs" | "complete real-world agent safety" |
| FlowFence-Lite enforces a policy-preserving safe-view invariant under complete mediation and sound rewriting. | Proposition 1 in Method; implementation/evaluator assumptions | "formal invariant under stated assumptions" | "mathematical proof of production security" |
| Shared-artifact fanout can amplify contaminated reads. | Proposition 2; topology results | "fanout motivates topology-aware risk scoring" | "all blackboard systems are always unsafe" |
| P0 adapted AgentPoison comparator supports retrieval-memory containment. | Table 1; P0 summaries | "adapted comparator evidence" | "official AgentPoison reproduction" |
| Static keyword filtering is strong on the known-trigger P0 setting but brittle under the held-out instruction stress setting. | Table 1; P0 static-keyword and held-out-instruction summaries | "blocklist-brittleness caveat on the adapted retrieval anchor" | "broad held-out attack robustness" |
| P0 overhead artifacts exist but are not a headline AAAI result. | P0 measured-overhead and proxy summaries; claims checklist | "overhead evidence is traceable but secondary" | "FlowFence is generally faster" |
| MiniMax 252-run coverage supports FlowFence clean subset. | Table 3; coverage summaries | "MiniMax-backed synthetic-runtime coverage" | "real-world deployment evidence" |
| FlowFence improves or ties baselines on configured raw/external leakage comparisons. | Table 3 | "configured comparison groups" | "universally dominates all defenses" |
| Topology effects are observed in the synthetic-runtime benchmark. | Table 3 and seed/topology summaries | "observed in the synthetic-runtime benchmark" | "validated in real-world deployments" |
| Non-oracle held-out validation mitigates the oracle-label concern. | Table 7; non-oracle summaries | "substantially mitigates under configured held-out matrices" | "arbitrary attack robustness" |
| No-semantic-pattern ablation suggests semantic patterns contribute to raw-leakage containment. | Table 8 | "partial mechanism evidence" | "semantic detection is unnecessary" |
| The paper-facing FlowFence method is non-oracle and runtime-observable. | Method section; `src/defenses/mas_flowfence.py`; non-oracle task state; Table 7 | "the evaluated non-oracle variant ignores attack labels and uses runtime-observable signals" | "the original engineering default is the final method" |
| Cascade size need not be zero when containment succeeds. | Table 3; cascade evaluator; safe-trace cases | "contaminated content can be observed and quarantined while raw/external leakage stays zero" | "all contaminated events are eliminated" |
| Non-MiniMax generalization is unsupported. | Limitations and evidence boundaries | "not evaluated" | any positive claim |
| Case 1 illustrates no-defense blackboard workspace propagation. | `artifacts/case_studies_safe_trace/case_1_no_defense_workspace_leak_trace.md`; Table~\ref{tab:case_studies} | "redacted safe-trace illustration of a configured no-defense failure; appropriate for main text" | "raw transcript", "production log", "real-world deployment trace" |
| Case 3 illustrates FlowFence safe-view/quarantine containment on the paired workspace attack. | `artifacts/case_studies_safe_trace/case_3_flowfence_safe_view_success_trace.md`; Table~\ref{tab:case_studies} | "redacted safe-trace illustration of quarantine/safe-view routing; appropriate for main text" | "FlowFence universally prevents all leaks", "raw provider output" |
| Case 4 illustrates non-oracle held-out containment with no oracle-label use. | `artifacts/case_studies_safe_trace/case_4_nonoracle_heldout_success_trace.md`; Table~\ref{tab:case_studies} | "targeted MiniMax-backed synthetic-runtime validation trace records oracle_annotation_used=false; appropriate for main text" | "arbitrary attack robustness", "production safety validation" |
| Case 2 illustrates prompt-filter paraphrase weakness. | `artifacts/case_studies_safe_trace/case_2_prompt_filter_paraphrase_failure_trace.md`; Table~\ref{tab:case_studies} | "redacted safe-trace illustration of configured prompt-filter paraphrase failure; appendix-level or brief analysis note" | "all prompt filters fail", "real computer-use trajectory" |
| Table polish improves readability but does not alter evidence. | Edited AAAI table files; source paper tables in `artifacts/paper_tables/` | "table wording was shortened while preserving committed values" | "new experimental evidence" |
