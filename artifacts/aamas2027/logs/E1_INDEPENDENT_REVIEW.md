# Independent E1 implementation review

Reviewed the intermediate-agent runner, its task/formal/pilot configs, existing enterprise scenario, policy, attack generator, utility checker, and targeted tests before formal E1 execution. This review did not modify E1 code or task selection.

Two implementation defects found during concurrent development were reported and corrected by the owning agent before this review finished:

- The explicit provider-settings constructor was temporarily nested after the matrix runner's return. It is now a method of `MiniMaxAgentClient`; construction with `provider_settings=None` succeeds.
- The event privilege metric omitted the vendor tool endpoint. A direct injected disclosure through `vendor_send_tool` now reports its existing privilege level 5.

Validation:

```bash
PYTHONPATH=. /Users/crazy/anaconda3/bin/python -m pytest tests/test_aamas_llm_agents.py -q
```

Observed: 32 passed, 0 failed, 0 skipped. Additional in-memory probes verified provider construction, the privilege value, and source/generated exposure attribution. No provider request was made by this review.

The actual planner action determines whether the deterministic workflow accepts a finance request. Finance selects the actual quote submitted to the deterministic approval tool. The writer receives the mediated finance action and actual approval state, and its generated fields determine the final vendor action. The real client does not receive evaluator gold; only the explicitly labeled dry-run fixture calls the expected-decision helper to emit answers. Policy/config/role prompts are common across defenses. Canonical private-cap access is separately mediated for the authorized finance role. Full model text is separated into private audit output; safe results retain IDs, measurements, decisions, and public catalog choices.

Required interpretation caveats:

1. There is one historical enterprise scenario. The twelve quote/deadline/status instances are new synthetic public-parameter extensions, not twelve independently sourced tasks or domains. The old scenario did not contain the new vendor quote catalog or approval state.
2. For all twelve instances, the cheapest quote meeting the public deadline is already budget-eligible. Comparing that public-only choice to the registered budget-aware gold gives zero changed choices out of twelve. The private cap therefore does not create a binding decision tradeoff in this slice. The verifier tests generated catalog choice/state correctness, not evidence that private-budget reasoning was necessary.
3. Attacked source content includes exogenous protected values before the first model call. In a dry-run blackboard probe, no defense had 16 source exposure events and zero generated exposure events; IFC and PAPC had zero of each. All three completed the task in that wiring probe. An overall privacy-safe-success difference against no defense can therefore arise solely from source mediation. Formal reports must retain source/generated exposure splits and should not infer model-induced leakage from the aggregate alone.
4. E1 measures only existing exact protected strings. A reformatted or reconstructable model output may escape its evaluator; E3 explicitly demonstrates this limitation. Zero E1 measured exposure is not semantic confidentiality.
5. The workflow has three generated role actions/messages in a fixed role order. Generated actions have causal state effects and downstream contexts reflect mediation, but this is not evidence of adaptive scheduling, arbitrary tool planning, or iterative recovery.

No remaining critical blocker was found in the reviewed paths after the two corrections. This review is not a claim that the expensive model matrix succeeded; those outcomes belong to the saved formal episodes.
