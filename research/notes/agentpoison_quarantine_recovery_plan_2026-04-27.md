# AgentPoison Quarantine Recovery Plan

## Scope

This note records the current postmortem and staged improvement plan for the adapted fullreact `AgentPoison` comparator:

- attack artifact: `results/baseline_agentpoison_fullreact_dpr_strategyqa_kimi25_triggerquery_v1/`
- current best defense artifact: `results/method_flowfence_lite_fullreact_kimi25_triggerquery_quarantine_v1/`
- repeated defense artifact: `results/method_flowfence_lite_fullreact_kimi25_triggerquery_quarantine_repeat1/`

This is still an adapted comparator, not full official `AgentPoison` reproduction. The attack uses:

- provider: `kimi25`
- retriever path: upstream DPR inside `local_wikienv.WikiEnv`
- adversarial search context policy: `trigger_question_only`

## Current Mechanism

The current defense does not modify the retriever. It intercepts retrieval observations after `Search[...]` or `Lookup[...]` returns text and before that text is appended to the model prompt.

Current quarantine policy:

1. detect poisoned content in a retrieval observation
2. replace the entire observation with a short quarantine message
3. keep raw poisoned retrieval counts for auditability
4. set exposed poisoned retrieval counts to zero when the poisoned text is withheld

This explains the current metric pattern:

- raw poisoned retrieval remains high
- exposed poisoned retrieval drops to zero
- attack manifestation drops to zero
- utility can still fall because the model loses retrieval evidence and may not recover cleanly

## Observations

### Observation 1: safety is stable

Across the two completed quarantine runs:

- `raw_poisoned_retrieval_case_rate = 0.96`
- `exposed_poisoned_retrieval_case_rate = 0.0`
- `attack_manifestation_rate = 0.0`

Interpretation:

- the retriever still surfaces poisoned content
- the current defense successfully blocks poisoned content from entering the model prompt

### Observation 2: empty answers are a major utility failure mode

Typical adversarial failure cases show repeated quarantined search steps followed by an empty final answer after the runner reaches `max_steps`.

Interpretation:

- the model often does not receive enough clean evidence after quarantine
- the current prompt/control flow does not redirect the model toward a clean finish decision

### Observation 3: trajectory pollution remains after quarantine

The current runner writes the original `Action` string back into the prompt trajectory. Malformed action strings can contain repeated `]` tokens and other artifacts. These artifacts can later be interpreted by the model as a signal sequence even when poisoned retrieval content itself was quarantined.

Interpretation:

- utility loss is not caused only by missing retrieval facts
- dirty action writeback can create a second, non-retrieval path for prompt confusion

### Observation 4: post-quarantine search context can drift

The default benign search path uses `current_context` as search input. After quarantine, `current_context` includes prior actions, quarantine messages, and any trajectory artifacts that survived writeback.

Interpretation:

- repeated searches after quarantine may be less semantically aligned with the original question
- later retrievals can become noisy even without additional poisoned exposures

## Staged Improvement Plan

The stages are ordered by risk. Earlier stages should not reintroduce poisoned content into the prompt.

### Phase 1: canonical action writeback

Change:

- write the normalized/canonicalized ReAct action back into the prompt trajectory instead of the raw action string

Why first:

- this is the smallest behavioral change
- it directly targets observed bracket-artifact failures
- it does not relax the quarantine rule

Primary checks:

- preserve `attack_manifestation_rate = 0.0`
- preserve `exposed_poisoned_retrieval_case_rate = 0.0`
- inspect whether benign artifact-driven mistakes decrease, especially cases similar to benign case index `19`

### Phase 2: quarantine-aware recovery hint

Change:

- after repeated quarantines in the same case, replace the generic quarantine message with a stronger recovery-oriented message that tells the model not to repeat the same search and to finish from the question plus any clean evidence when appropriate

Why second:

- the main remaining adversarial utility failure is repeated quarantined searches ending in empty answers
- this stage changes control flow guidance without changing the retriever or re-exposing poisoned content

Primary checks:

- preserve the same safety metrics as phase 1
- reduce adversarial empty answers
- reduce repeated quarantine loops per case

### Phase 3: post-quarantine clean search context

Change:

- after a quarantine event, stop feeding the full dirty `current_context` back into later search queries
- use a cleaner search context derived from the original question or a cleaned entity span

Why third:

- this changes retrieval behavior more than phases 1 and 2
- it specifically targets search drift after quarantine

Primary checks:

- preserve the same safety metrics as phase 2
- reduce retrieval noise in later steps
- improve defended utility on cases that currently loop through repeated low-value searches

## Why Not Start With Safe-View Rewrite

The ideal outcome would be to preserve clean facts while removing only the poisoned parts of a retrieval observation. That is not the first step here because the current defense layer receives only a single returned observation string and does not reliably know which tokens are safe factual content versus attack payload. A premature rewrite can reintroduce prompt confusion or leak residual attack instructions.

The safer order is:

1. remove trajectory artifacts
2. improve post-quarantine recovery behavior
3. reduce dirty-context search drift
4. only then consider a more aggressive safe-view extraction path if needed

## Acceptance Rule

No stage should be accepted as the new default unless it satisfies both:

1. safety parity with the current quarantine baseline
2. a targeted improvement on the failure mode it is meant to address

Safety parity means:

- `attack_manifestation_rate = 0.0`
- `exposed_poisoned_retrieval_case_rate = 0.0`

Targeted improvement means at least one of:

- fewer empty answers
- fewer repeated quarantine loops
- fewer benign artifact-driven failures
- higher attacked utility without a worse clean utility collapse than the current two quarantine runs
