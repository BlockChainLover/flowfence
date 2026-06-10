# Open Review Risks - Polished Draft

## High-priority reviewer risks

1. **Synthetic-runtime scope.** The strongest evidence uses a synthetic deterministic multi-agent runtime with MiniMax final-writer calls. The paper must not imply a real browser/desktop or production deployment.

2. **MiniMax-only provider evidence.** The real-provider evidence is MiniMax-only. This is acceptable for a scoped paper but must be explicit in title-adjacent prose, abstract, experiments, and limitations.

3. **Rule-based method concern.** FlowFence-Lite is a practical runtime method with deterministic risk features. The paper now includes a risk formula, safe-view invariant, fanout proposition, and no-semantic-pattern ablation, but reviewers may still ask for deeper module ablations or learned risk scoring.

4. **Official baseline concern.** P0 is an adapted AgentPoison comparator, not an official reproduction. The paper should frame it as a retrieval-memory sanity check rather than a main benchmark victory.

5. **Raw trace availability.** Raw traces and provider outputs are not committed for privacy reasons. The artifact should emphasize reproducible high-level summaries and safe traces.

## Risks mitigated in the current draft

- Method wording now presents the paper-facing defense as non-oracle and runtime-observable, with the oracle-annotation path framed as an engineering risk that was diagnosed and tested.
- Results wording now explains that ties often occur in no-attack or low-pressure settings, and that non-zero cascade size can be compatible with successful quarantine/safe-view containment.
- The oracle-annotation concern is substantially mitigated by `flowfence_lite_nonoracle` and held-out paraphrased attacks.
- Phrase-overfitting concern is partially mitigated by the held-out paraphrase validation.
- Utility-overblocking concern is mitigated by task success 1.0 in the FlowFence subset and non-oracle validations.
- Interpretability risk is reduced by concise redacted safe-trace illustrations that connect aggregate metrics to event paths.
- The safe-trace examples are explicitly framed as redacted qualitative examples, not raw traces, raw transcripts, provider outputs, production logs, or additional experiments.
- Dense tables have been shortened, but a LaTeX-capable pass is still needed to confirm page count and overfull-box status.

## Remaining experiment candidates

- Deeper module ablations beyond no-semantic-pattern.
- Non-MiniMax provider replication.
- Real browser/desktop/computer-use runtime.
- Learned graph risk scorer.

## Remaining qualitative-evidence caveat

The redacted safe-trace illustrations improve readability and reviewer auditability, but they do not broaden the evidence boundary. Lack of raw trace release remains a privacy-driven limitation, and the paper must keep production, real computer-use, arbitrary-attack, and non-MiniMax claims out of scope.
