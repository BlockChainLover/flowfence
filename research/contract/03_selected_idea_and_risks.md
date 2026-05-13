# FlowFence-Lite — Selected Idea and Risks

## 1. Selected idea

We will build **FlowFence-Lite**, a **runtime privacy containment layer** for multi-agent LLM systems.

### Core design choice
Do **not** start with a learned graph model or a theory-heavy method.  
Start with a **strong systems baseline** that is implementable, testable, and ablatable:

1. **Propagation-aware risk scoring**
2. **Lease-based least privilege**
3. **Shared-memory / shared-workspace governance**
4. **Dual trace logging for internal leakage evaluation**

This is the most practical route to a paper because it gives us:
- a clear engineering artifact,
- a direct comparison against narrow baselines,
- a clean path to later upgrade the risk scorer into a learned model.

---

## 2. Why this idea was selected

We considered several possible angles.

### Option A — pure benchmark paper
**Rejected as primary plan.**  
Benchmark-only work is useful, but it is harder to pitch as a strong main-track method paper unless the benchmark is unusually large or uniquely realistic.

### Option B — pure topology detector (G-Safeguard-style extension)
**Rejected as primary plan.**  
This would likely be seen as too close to G-Safeguard unless we add something genuinely new. The real gap is not only anomaly detection over messages.

### Option C — pure privacy prompt defense (AgentDAM-style extension)
**Rejected as primary plan.**  
Prompting alone is too narrow once shared memory and shared workspaces exist.

### Option D — unified runtime containment system
**Selected.**  
It directly addresses the gap left between:
- prompt-defense work,
- topology-defense work,
- privacy benchmarking,
- memory attack papers.

---

## 3. Design summary

FlowFence-Lite is a **middleware layer** around a multi-agent runtime.

### Inputs
- candidate agent actions,
- current topology / graph snapshot,
- artifact metadata,
- secret/policy metadata,
- current lease/privilege state.

### Outputs
- a risk score,
- an allow/block/rewrite/quarantine decision,
- lease updates,
- structured event logs.

### Main claim target
A joint runtime defense can reduce:
- unauthorized leakage,
- cascade size,
- privilege reach  
with smaller utility loss than isolated baselines.

---

## 4. System architecture

## 4.1 Component view

### A. Event graph builder
Every runtime action becomes an event edge in a time-indexed graph.

**Purpose:** make privacy failures observable as propagation, not just wrong outputs.

### B. Risk scorer
Scores each candidate action using:
- semantic features,
- provenance,
- executability,
- topology context,
- privilege context,
- artifact destination.

### C. Lease controller
Each agent receives a **temporary lease** for:
- readable memory scopes,
- writable destinations,
- callable tools.

Leases can be downgraded or revoked at runtime.

### D. Safe-view generator
Instead of exposing raw memory or raw workspace content broadly, generate a **safe view**:
- redacted,
- abstracted,
- policy-aware,
- narrower than the original content.

### E. Quarantine manager
High-risk artifacts are diverted into a quarantine zone instead of entering shared raw memory or shared workspace.

### F. Policy engine
Combines all module signals into a final decision.

### G. Dual logger
Produces:
- `full trace`: for private evaluation and replay,
- `safe trace`: for artifact sharing and reproducibility.

---

## 5. Operational design

## 5.1 Runtime objects

### Agents
Each agent has:
- `agent_id`
- `role`
- `principal`
- `trust_level`
- `current_lease`

### Artifacts
Each artifact has:
- `artifact_id`
- `artifact_kind`
- `owner_principal`
- `zone`
- `sensitivity_tags`
- `contains_secret`
- `secret_ids`

### Leases
Each lease defines:
- readable scopes,
- writable scopes,
- tool scopes,
- TTL in steps,
- revocation rules.

### Policies
Each secret policy defines:
- authorized recipients,
- allowed abstraction level,
- forbidden channels,
- must-use subtask exceptions.

---

## 5.2 Risk scoring features

The MVP scorer should be **hybrid**, not fully learned.

### Semantic features
- instruction-like phrasing
- explicit request to share/broadcast/save
- presence of sensitive entities
- extraction intent
- summary-to-raw mismatch
- tool-use intent

### Structural features
- channel type
- destination zone (`shared_raw`, `safe_view`, `workspace`, `tool_arg`)
- cross-principal movement
- current node fan-out
- node centrality proxy
- whether destination is globally readable
- whether content would reach a side-effect tool

### Policy features
- whether content contains protected secret
- whether abstraction level violates policy
- whether destination is forbidden by policy
- whether action exceeds current lease

### Suggested initial output
Use a scalar `risk_score in [0,1]` plus reason codes.

---

## 5.3 Decision policy

Use threshold-based decisions first.

### Suggested thresholds
- `risk < tau_redact`: allow
- `tau_redact <= risk < tau_quarantine`: rewrite / safe-view downgrade
- `risk >= tau_quarantine`: quarantine + lease downgrade / revoke

### Hard blockers
Regardless of score, the following should cause hard intervention:

- write to a forbidden channel,
- raw secret to unauthorized recipient,
- unauthorized high-side-effect tool call,
- cross-principal raw disclosure to shared raw memory.

---

## 5.4 Decision pipeline

```text
candidate_action
  -> optional attack mutation
  -> static policy checks
  -> risk scorer
  -> lease controller
  -> safe-view generator
  -> quarantine manager
  -> final policy decision
  -> execute or block
  -> log event + policy decision
```

### Why this order
- cheap hard blockers run first,
- dynamic risk then determines whether stronger containment is needed,
- content rewriting happens before final execution,
- every stage remains ablatable.

---

## 6. Minimal interface boundaries

These interfaces are required for the project to stay modular.

## 6.1 Attack interface
Each attack plugin must:

- declare supported action types/channels,
- mutate only the candidate action,
- never execute actions directly,
- emit a machine-readable attack annotation.

## 6.2 Defense module interface
Each defense module must:

- inspect the action and context,
- output a score / reason codes / suggested actions,
- remain stateless or explicitly stateful,
- be composable with other defense modules.

## 6.3 Policy engine interface
The policy engine must:

- merge module signals,
- produce one final verdict,
- attach lease changes,
- explain the decision via reason codes.

## 6.4 Logger interface
The logger must:

- record blocked and executed actions,
- support full + safe traces,
- store causal parent links,
- support deterministic replay as much as possible.

---

## 7. What is in MVP, and what is deferred

## 7.1 In MVP

- text-only runtime
- hybrid risk scoring
- threshold policy engine
- leases for memory/workspace/tool access
- safe-view memory + quarantine
- 3 domains
- 3–4 topologies
- channel-level leakage metrics

## 7.2 Deferred until after first end-to-end result

- learned graph model / GNN risk scorer
- multimodal propagation
- real browser agent integration
- distributed runtime across machines
- online adaptation of thresholds
- formal guarantees beyond simple threshold logic

This is important: **MVP must prove the systems idea before adding model complexity.**

---

## 8. Concrete novelty hypothesis

FlowFence-Lite is novel **only if** it clearly combines things that prior work treats separately.

The selected novelty statement is:

> a multi-agent runtime defense that uses propagation-aware scoring and lease-based privilege control to govern shared memory and workspace writes under explicit privacy policies.

That statement is stronger than:
- “we detect attacks,”
- “we add privacy prompting,”
- “we study topology,”
- “we benchmark privacy.”

It is also narrower and safer than:
- “we solve privacy in agent systems.”

---

## 9. Major risks and mitigations

| Risk | Why it matters | Mitigation |
|---|---|---|
| Utility collapse | Defense may “win” by blocking too much collaboration. | Track clean utility retention and false-block rate from day one. |
| Safe-view leakage | The summarizer/redactor may still leak too much. | Evaluate raw leakage and abstract leakage separately. |
| Scope explosion | Browser agents + many frameworks will slow us down. | Keep MVP text-first and tool-simulated. |
| Weak baseline reproduction | Reviewers will not trust gains if baselines are weak. | Use official code where available; label reimplementations clearly. |
| Logging itself leaks secrets | Full traces may contain the very data we want to protect. | Produce safe traces and keep full traces private/local. |
| Graph features add little value | If topology features do not help, “propagation-aware” becomes weak. | Keep static ACL + prompt filter + topology-only baseline for honest comparison. |
| Memory backend confound | Gains may come only from changing memory, not from the defense. | Compare multiple memory backends and isolate safe-view/quarantine effects. |
| Novelty risk | A reviewer may say this is “just policy + filtering.” | Emphasize joint runtime containment and internal-channel metrics. |
| Reimplementation burden for MEXTRA/AiTM | Could delay results. | Treat them as stretch baselines; do not block MVP on them. |

---

## 10. Assumptions that could break the method

### Assumption A — policies are available
If we cannot define good disclosure policies, leakage evaluation becomes fuzzy.

### Assumption B — risky actions are interceptable
If the runtime cannot intercept memory writes, workspace writes, or tool args, FlowFence-Lite loses its control points.

### Assumption C — safe views preserve enough task information
If safe views remove too much information, the defense will appear useless.

### Assumption D — topology features are observable cheaply
If graph reconstruction becomes too expensive, runtime overhead may dominate.

---

## 11. How we fail fast

We should declare in advance what outcomes count as an early warning that the idea is not working.

### Fail-fast signal 1
FlowFence-Lite does not beat **static ACL + prompt filter** on leakage in the first full MVP run.

### Fail-fast signal 2
Clean utility drop is > 15% and no ablation shows a recoverable cause.

### Fail-fast signal 3
Most leakage comes from channels we do not instrument.

### Fail-fast signal 4
The only gains come from blocking raw shared memory entirely.

If any of the above happens, the project may need to pivot from:
- a method paper  
to either:
- a benchmark/measurement paper, or
- a narrower memory-governance paper.

---

## 12. Continuation criteria after first complete MVP run

Continue with the current plan only if all of the following are true:

- internal leakage is measurable and non-trivial,
- at least one shared-artifact channel contributes materially to leakage,
- FlowFence-Lite improves leakage or cascade metrics over no defense,
- utility is not catastrophically degraded,
- ablations show at least one module matters.

If these conditions are met, the project is worth scaling up.

---

## 13. What we will not claim unless proven

Do not claim the following unless experiments explicitly support them:

- “generalizes to all agent frameworks”
- “provable containment guarantees”
- “secure in real-world deployment”
- “defeats adaptive attackers”
- “more private than human workflows”
- “works for multimodal or browser agents”

---

## 14. Selected idea in one paragraph

FlowFence-Lite will be a runtime containment system for multi-agent LLM workflows. It will score each information-moving action using semantic, policy, and graph-context features; enforce temporary least-privilege leases over reads, writes, and tool calls; rewrite shared artifacts into safe views when possible; and quarantine high-risk content when needed. The MVP intentionally avoids a heavy learned model and instead aims to prove that a unified runtime design can reduce privacy leakage and propagation better than prompt-only, topology-only, or static-access baselines without collapsing utility.
