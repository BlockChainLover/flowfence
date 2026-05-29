# Open Risks Before Paper Integration v2

## 1. Experimental risks

- MiniMax remains the only real provider represented.
- P1 MiniMax coverage uses a synthetic deterministic MAS runtime with MiniMax final-writer calls, not a real browser, desktop, or computer-use environment.
- The 252-run coverage and 72-run targeted non-oracle validation cover configured benchmark matrices, not arbitrary tasks or arbitrary attacks.
- P0 AgentPoison evidence is an adapted comparator and must not be called a full official AgentPoison reproduction.
- Module ablation is partial: the no-semantic-pattern ablation tests one mechanism slice, not every FlowFence component.

## 2. Wording risks

- Use "MiniMax-backed multi-agent synthetic-runtime coverage experiment" or "MiniMax-only P1 MAS coverage over the synthetic deterministic runtime" for the 252-run coverage.
- Use "targeted MiniMax-backed synthetic-runtime validation" or "MiniMax-only non-oracle held-out validation over the synthetic deterministic MAS runtime" for the 72-run non-oracle validation.
- Do not write "real-world deployment", "real computer-use experiment", "production safety validation", or "arbitrary attack robustness".
- Do not claim non-MiniMax generalization.
- Do not claim production safety.
- Do not claim real browser/desktop/computer-use agent evidence.
- Do not claim FlowFence-Lite universally dominates all baselines.
- Do not claim semantic detection is unnecessary.

## 3. Reviewer risks

- Reviewers may ask why P0 is adapted rather than official AgentPoison. The answer should be explicit: this is an adapted full-ReAct retrieval-memory comparator with saved mismatch caveats.
- Reviewers may ask why static keyword filtering is strong in the P0 known-trigger setting. The paper should use this as a caveat, not hide it.
- Reviewers may ask why MiniMax is the only real provider. The limitation should be stated directly.
- Reviewers may ask whether synthetic-runtime coverage transfers to real computer-use agents. The current evidence does not support that transfer.
- Reviewers may ask whether prior FlowFence evidence depended on oracle attack annotations. The current answer is that the default-path risk was diagnosed and substantially mitigated by non-oracle held-out validation.
- Reviewers may ask whether the phrase detector is the entire mechanism. Table 8 supports a narrower answer: semantic patterns contribute to raw-leakage containment, while policy/fanout/safe-view mechanisms still matter.

## 4. Missing baselines

- Non-MiniMax providers are not evaluated.
- Production or browser/desktop agents are not evaluated.
- Learned graph risk scorer is not implemented or evaluated.
- Broader defense families beyond `none`, `static_acl`, and `prompt_filter` are not part of the MiniMax coverage.
- Deeper module-level ablations beyond no-semantic-pattern ablation are not yet evaluated.
- The official AgentPoison reproduction remains unsupported.

## 5. Missing environments

- No real browser environment.
- No desktop computer-use environment.
- No production deployment.
- No human-user study.
- No multimodal environment.

## 6. Resolved risks

- The oracle-annotation concern is addressed or substantially mitigated for the configured held-out matrices by `flowfence_lite_nonoracle`, which records zero oracle annotation use in both deterministic and targeted MiniMax summaries.
- The phrase-overfitting concern is partially mitigated by held-out paraphrased attacks in the deterministic and targeted MiniMax non-oracle validations.
- The no-semantic-pattern ablation shows semantic patterns matter for raw leakage; it also indicates that policy/fanout/safe-view mechanisms retain value because external leakage and task success did not collapse.

## 7. Remaining next experiment candidates

- Deeper module-level ablation if reviewers require finer mechanism isolation.
- Redacted qualitative case studies to make failure modes and containment behavior easier to interpret without raw traces.
- Non-MiniMax provider coverage only if the provider rule is explicitly changed.
- Browser/desktop environment experiments as a separate scoped goal with new safety and raw-output handling rules.
- Learned graph scorer development and evaluation if the paper needs a predictive risk-scoring contribution.
