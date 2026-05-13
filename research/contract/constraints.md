# Constraints

- compute budget:
  Use one model backend only for the pre-method stage: the existing provider-backed `qwen36` path. The locked slice is now a 10-question `StrategyQA` subset with exactly 3 reruns before any broader matrix.
- time budget:
  Prioritize one minimal baseline-ready `AgentPoison` slice plus its 3-rerun aggregate summary, then the first method check on that same slice. Do not spend pre-method time debugging `ASB`, integrating the full DPR/REALM retriever stack, or broadening to new comparators unless the locked slice fails to answer the method question.
- licensing or access limits:
  Prefer open code and locally replayable tools. The chosen backend for the pre-method stage is the existing OpenAI-compatible provider path configured through `.secrets/providers.env`; access assumptions remain documented in config files rather than new external dataset notes.
- implementation boundaries:
  The runtime is simulated and instrumented. Every meaningful action must be wrappable and loggable. The proposed method itself should not be implemented in this session.
- unacceptable shortcuts:
  No silent split or metric changes after comparisons begin, no calling a smoke test a reproduced baseline, no unsupported paper claims, no using unsupported facts from literature or benchmark details not present in the contract.
- mismatch policy for the first comparator:
  The pre-method `AgentPoison` slice is an adapted narrow baseline using official `ReAct-StrategyQA` assets plus simplified retrieval. It is baseline-ready for method comparison, but it must not be described as full official reproduction.
- rerun policy note:
  The current wrapper uses temperature 0, but provider/runtime nondeterminism may still change outputs across reruns. The pre-method gate therefore uses aggregate reporting across 3 reruns, not single-run stability.
