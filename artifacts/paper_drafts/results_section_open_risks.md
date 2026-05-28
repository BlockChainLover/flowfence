# Open Risks Before Paper Integration

## 1. Experimental risks

- The real-provider evidence is MiniMax-only.
- The P1 MiniMax coverage uses a synthetic deterministic MAS runtime with MiniMax final-writer calls, not a real browser, desktop, or computer-use environment.
- The 252-run coverage is stronger than the prior 18-run smoke and 84-run one-seed coverage, but it still covers one task family and a configured synthetic benchmark.
- Table 2 uses task-state summaries rather than a structured deterministic summary JSON artifact. The text should avoid excessive precision beyond the table entries.
- P0 AgentPoison evidence is an adapted comparator and must not be called full official AgentPoison reproduction.

## 2. Wording risks

- Do not write "real-world agent deployment", "real computer-use experiment", or "production agent experiment" for the 252-run MiniMax coverage.
- Use "MiniMax-backed multi-agent synthetic-runtime coverage experiment" or "MiniMax-only P1 MAS coverage over the synthetic deterministic runtime".
- Do not claim non-MiniMax generalization.
- Do not claim production safety.
- Do not claim real-world browser/desktop/computer-use agent evidence.
- Do not claim utility improvement from P0; use noisy or roughly preserved.
- Do not claim FlowFence-Lite universally dominates all baselines; use improves or ties on configured comparison groups.

## 3. Reviewer risks

- Reviewers may ask why the strongest P0 baseline is adapted rather than official AgentPoison. The answer should be explicit: this is an adapted full-ReAct retrieval-memory comparator with saved mismatch caveats.
- Reviewers may ask why static keyword filtering is strong in the P0 known-trigger setting. The paper should use this as a caveat, not hide it.
- Reviewers may ask why MiniMax is the only real provider. The limitation should be stated directly and tied to the current evidence boundary.
- Reviewers may ask whether synthetic-runtime coverage transfers to real computer-use agents. The current answer is no; this remains future work.
- Reviewers may ask whether FlowFence differs mechanistically from prompt-filter/static-ACL baselines. The results section can point to propagation-aware containment, but a fuller mechanism/ablation argument may need a separate section.

## 4. Missing baselines

- Non-MiniMax providers are not evaluated.
- Production or browser/desktop agents are not evaluated.
- Learned graph risk scorer is not implemented or evaluated.
- Broader defense families beyond `none`, `static_acl`, and `prompt_filter` are not part of the 252-run MiniMax coverage.
- The official AgentPoison reproduction remains unsupported.

## 5. Missing environments

- No real browser environment.
- No desktop computer-use environment.
- No production deployment.
- No human-user study.
- No multimodal environment.

## 6. Next experiment candidates

- `p1-experiment-gap-analysis` to decide whether more experiments are needed before integrating prose into the main paper.
- A targeted ablation or mechanism study if reviewers ask why FlowFence differs from static ACL and prompt-filter.
- A non-MiniMax provider expansion only if the provider rule is explicitly changed.
- A real browser/desktop agent experiment only as a separate scoped goal with new safety and raw-output handling rules.
