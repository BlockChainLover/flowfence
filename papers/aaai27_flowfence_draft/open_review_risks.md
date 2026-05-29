# Open Review Risks

This document records likely reviewer concerns for the AAAI-27 v0 draft, current answers from committed evidence, residual risk, and whether another experiment is likely needed.

| Reviewer concern | Current answer | Residual risk | Extra experiment needed? |
|---|---|---|---|
| The original FlowFence path may have used oracle attack labels. | The risk was diagnosed; `flowfence_lite_nonoracle` ignores oracle attack annotations and records zero oracle-annotation violations in deterministic and targeted MiniMax validation. | The default engineering path still exists for backward compatibility; the paper method should emphasize the non-oracle variant. | Not blocking for draft; deeper audit could help. |
| Phrase matching may explain the result. | Held-out paraphrases and a no-semantic-pattern ablation were added. The ablation had higher raw leakage, suggesting semantic patterns matter, while policy/fanout/safe-view still matter. | The ablation is partial and does not isolate every module. | Optional module-level ablation if reviewers ask. |
| Evidence is MiniMax-only. | The draft states MiniMax is the only real provider and does not claim non-MiniMax generalization. | Provider-specific behavior may not transfer. | Yes, if the target claim becomes multi-provider. |
| The runtime is synthetic rather than a real computer-use stack. | The draft explicitly scopes P1 evidence to synthetic deterministic MAS runtime and MiniMax final-writer calls. | Real browser/desktop workflows may introduce new channels and failures. | Yes, if claiming deployment relevance. |
| P0 is not an official AgentPoison reproduction. | The draft calls it an adapted AgentPoison retrieval-memory comparator. | Some readers may want an official reproduction. | Optional, depending on paper positioning. |
| Raw traces and provider outputs are not committed. | Paper-facing artifacts use high-level summaries to avoid raw private data and provider output exposure. | Qualitative debugging examples are limited. | Optional redacted case studies could help. |
| Static ACL and prompt filter baselines may be simplistic. | The draft presents them as deterministic benchmark baselines, not exhaustive production baselines. | Reviewers may request stronger baselines. | Optional targeted baseline expansion. |
| Learned graph risk scoring is absent. | The draft describes FlowFence-Lite as a lightweight runtime, not a learned scorer. | Learned scoring may improve generalization. | Future work, not needed for current claims. |
