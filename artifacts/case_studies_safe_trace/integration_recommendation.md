# Integration Recommendation

## Should We Integrate Into the Main Paper Now?

Yes, if the integration is concise and explicitly framed as redacted safe-trace illustration rather than new experimental evidence.

## Main-Text Cases

- Case 1 and Case 3 should be integrated as a paired failure/prevention vignette.
- Case 4 should be integrated in the non-oracle validation discussion.

## Appendix Cases

- Case 2 is useful as a prompt-filter paraphrase failure example, but it is less central than the paired FlowFence comparison and non-oracle case.

## Candidate Paragraph

In a redacted blackboard workspace example, the no-defense run writes contaminated shared-state content that is read by multiple agents and reaches an external-facing channel. In the paired FlowFence run, the same workspace-poisoning family triggers quarantine and safe-view rewriting before the external path, preserving task success while keeping raw and external leakage at zero. A targeted MiniMax-backed synthetic-runtime validation of the non-oracle variant shows the same containment pattern with oracle_annotation_used=false, supporting that the result does not depend on attack-label access in the configured held-out matrix.

## What Not To Claim

- Do not claim production safety.
- Do not claim real browser/desktop computer-use evidence.
- Do not claim arbitrary attack robustness.
- Do not claim non-MiniMax generalization.
- Do not claim that safe traces are raw transcripts.
