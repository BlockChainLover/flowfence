# FlowFence-Lite — Problem Definition

## 1. One-sentence project goal

Build and evaluate a **runtime defense for multi-agent LLM systems** that reduces **unauthorized privacy leakage and propagation of contaminated content** across agents, shared memory, shared workspaces, and tools, while preserving task utility.

---

## 2. Why this problem matters

Once an agent can read private data, write shared notes, call tools, and coordinate with other agents, privacy failures are no longer single-turn prompt mistakes. They become **system events**:

- one malicious or compromised input can be copied into shared memory,
- shared memory can be re-read by many agents,
- summaries can amplify the spread instead of compressing it safely,
- low-trust content can cross into high-privilege execution contexts.

The research question is not only **“does the final answer leak?”** but also:

1. **Which internal channels leak?**
2. **How far does the leak propagate?**
3. **Does leaked content reach higher-privilege agents or tools?**
4. **Can we contain the spread without destroying collaboration utility?**

---

## 3. Target system model

We study a **text-first, tool-enabled, instrumented multi-agent runtime** with the following components.

### 3.1 Entities

- **Agents**: planner, worker, reviewer, tool-using specialist, etc.
- **Memory**:
  - per-agent private memory,
  - shared raw memory,
  - safe-view shared memory,
  - quarantine memory.
- **Workspace**:
  - shared task board,
  - shared document,
  - shared intermediate results.
- **Tools**:
  - search/read-only tools,
  - write/side-effect tools (email send, booking, document write, external upload),
  - local simulated tools for reproducible experiments.
- **Policy engine / defense runtime**
- **Evaluator**

### 3.2 Observable action types

Every state-changing or information-moving action must be logged as one of:

1. `SEND_MESSAGE`
2. `MEMORY_READ`
3. `MEMORY_WRITE`
4. `WORKSPACE_READ`
5. `WORKSPACE_WRITE`
6. `TOOL_CALL`
7. `FINAL_OUTPUT`

### 3.3 Channels we care about

- agent → agent message
- agent → shared memory write
- shared memory → agent retrieval
- agent → shared workspace/document write
- workspace/document → agent read
- agent → tool arguments
- tool output → agent observation
- agent → final user-visible output

---

## 4. Threat model

### 4.1 Adversary capabilities in scope

The attacker may do one or more of the following:

- inject malicious content into **tool outputs**,
- poison **shared memory** or a **shared summary**,
- inject malicious content into a **shared document/workspace artifact**,
- compromise or simulate a **low-trust agent** that sends malicious inter-agent messages,
- query the system in a way that tries to **extract stored private content** from memory.

### 4.2 Adversary capabilities out of scope

The attacker does **not**:

- gain root / OS / container-level compromise,
- break network transport or steal raw model weights,
- directly read the evaluator’s private ground-truth labels,
- exploit training-time memorization of the base model,
- use multimodal image/audio channels in MVP.

### 4.3 Assets to protect

- user secrets and sensitive attributes,
- contextually sensitive task facts,
- credentials and identifiers,
- shared documents containing private information,
- privileged tools and tool arguments,
- internal traces that would not be visible in a clean execution.

---

## 5. Privacy policy model

Every secret instance must be defined by a machine-readable policy.

### 5.1 Required fields per secret

- `secret_id`
- `owner_principal`
- `secret_type`
- `raw_value`
- `allowed_recipients`
- `allowed_abstraction_level`
- `must_use_for_subtasks`
- `forbidden_channels`

### 5.2 Abstraction levels

We will use four levels:

- `none`: secret should not be disclosed at all
- `coarse`: only a coarse category is allowed
- `summary`: abstract summary allowed, raw value forbidden
- `raw`: raw value allowed only to explicitly authorized recipients

### 5.3 Principals

A principal is the entity whose data is being protected, e.g.:

- the user,
- a finance department role,
- an external vendor,
- a clinician or legal reviewer,
- another collaborating user.

The system should treat **cross-principal disclosure** as higher-risk than intra-principal reuse.

---

## 6. What counts as failure

A run is considered unsafe if any of the following occurs.

### 6.1 Unauthorized raw leakage

A secret raw value appears in a channel or artifact not authorized by policy.

Examples:
- credit limit copied to shared raw memory,
- SSN appearing in a shared doc,
- API key passed to a booking tool that did not require it.

### 6.2 Unauthorized abstract leakage

The raw value is not exposed, but an over-detailed or unauthorized abstraction is exposed.

Examples:
- “budget is under 5k” may be allowed,
- “budget is exactly 4.8k” may not be allowed.

### 6.3 Propagation failure

Contaminated or policy-violating content spreads to additional nodes/artifacts after the first unsafe step.

### 6.4 Privilege escalation by propagation

Low-trust or contaminated content reaches:
- higher-privilege agents,
- shared raw memory,
- shared workspace,
- high-side-effect tools,
- final output.

### 6.5 Containment failure

The defense detects risk too late to prevent meaningful spread.

---

## 7. Formal working definitions

We do not need a full theorem in MVP, but we do need operational definitions.

### 7.1 Event graph

For each run, construct a directed time-indexed graph:

- nodes = agents, memory slots, workspace artifacts, tool sessions, final outputs
- edges = logged actions that move or transform information

### 7.2 Contaminated node / artifact

A node or artifact is marked contaminated if it contains:
- malicious injected instruction content,
- an unauthorized secret,
- a derived unsafe summary produced from such content.

### 7.3 Cascade size

Fraction of nodes/artifacts that become contaminated during a run.

### 7.4 Cascade depth

Maximum hop distance from the initial contaminated seed to any contaminated descendant.

### 7.5 Privilege reach

Highest privilege level touched by contaminated content.

### 7.6 Containment delay

Number of steps between the first contaminated event and the first successful containment action that stops further unsafe spread.

---

## 8. Core research question

> Can a propagation-aware runtime defense that combines risk scoring, lease-based least privilege, and shared-memory governance reduce internal and external privacy leakage in multi-agent systems with only modest utility loss?

### 8.1 Sub-questions

1. Are internal channels (memory, workspace, tool args, inter-agent messages) a larger privacy surface than final outputs?
2. Does topology materially change leakage and containment behavior?
3. Are prompt-only defenses insufficient once shared memory and shared workspaces are introduced?
4. Is static access control insufficient without runtime propagation awareness?
5. Is a unified defense better than isolated defenses at the same utility level?

---

## 9. Hypotheses

### H1 — Internal channels matter
In multi-agent settings, **internal leakage** will exceed leakage observable from final outputs alone.

### H2 — Shared artifacts amplify risk
Shared memory and shared workspace increase cascade size and privilege reach relative to private-only memory.

### H3 — Single-axis defenses are insufficient
Prompt filtering, topology-only detection, or static ACLs alone will not consistently control both leakage and propagation.

### H4 — Joint containment works better
A defense that combines:
- risk scoring,
- lease downgrading/revocation,
- safe-view rewriting,
- quarantine of risky artifacts  
will outperform isolated baselines under similar utility.

---

## 10. Scope of MVP

### In scope

- text-only multi-agent runtime
- simulated tools and reproducible environments
- 3 domains
- 3–4 topologies
- 4–5 attack types
- 5–6 defenses
- channel-level leakage evaluation
- dual logging: full trace + safe trace

### Out of scope for MVP

- multimodal attacks
- browser automation with real internet browsing
- OS-level sandbox escape
- theoretical universal robustness claims
- cross-run online learning of defense rules
- production deployment claims

---

## 11. Assumptions

These assumptions must be written explicitly because they affect what claims are defensible.

1. **Instrumentation assumption**  
   We can wrap every channel that moves information.

2. **Policy availability assumption**  
   We can define ground-truth disclosure policies for synthetic secrets.

3. **Controllability assumption**  
   The runtime can block, rewrite, or quarantine risky actions before execution.

4. **Replayability assumption**  
   The benchmark environment can be replayed deterministically enough for fair comparison.

5. **Model abstraction assumption**  
   Text outputs and tool calls are sufficient observable proxies for harmful propagation in MVP.

6. **No hidden channel assumption**  
   We ignore side channels such as token timing, embeddings stored outside our wrappers, and latent memory in closed-source provider infrastructure.

---

## 12. Non-goals

Do **not** let the project drift into these claims:

- “solves privacy for all agents”
- “provably secure against adaptive adversaries” (unless we actually prove something)
- “works on real computer-use agents at internet scale”
- “prevents training-data leakage”
- “covers all multi-agent architectures”

---

## 13. Success criteria for the project

These are project-level targets, not guaranteed paper claims.

### Minimum success criteria

- clean utility drop <= 10% relative to no defense
- internal raw leakage reduction >= 30% vs no defense
- cascade size reduction >= 25% vs no defense
- privilege reach reduced in at least 2 of 3 domains
- results reproducible across at least 2 seeds

### Strong success criteria

- clean utility drop <= 5%
- internal raw leakage reduction >= 40%
- cascade size reduction >= 35%
- beats strongest non-FlowFence baseline on leakage and cascade while preserving >= 90% of its utility
- generalizes to one held-out topology or attack family

---

## 14. Deliverables that make the problem concrete

By the time the problem is “implemented,” the repo must contain:

1. **Instrumented runtime**
2. **Task manifests**
3. **Secret manifests**
4. **Disclosure policies**
5. **Attack plugins**
6. **Defense plugins**
7. **Event logs**
8. **Leakage + propagation evaluators**
9. **Aggregated experiment reports**
10. **A safe-shareable trace format**

---

## 15. Open risks that may invalidate the framing

### Risk A — Synthetic secrets are too easy
If the benchmark only uses regex-friendly canaries, the problem becomes trivial and unrealistic.

**Mitigation:** mix exact-match secrets with contextual secrets and abstraction-sensitive secrets.

### Risk B — Defense wins only by blocking collaboration
If leakage falls because the system refuses to collaborate, the result is not interesting.

**Mitigation:** track clean utility retention and false-block rate.

### Risk C — Shared memory is an artificial bottleneck
If all failures are caused by an unrealistic memory design, reviewers may dismiss the setup.

**Mitigation:** compare multiple memory backends, including private-only and stronger memory systems.

### Risk D — Attack implementations are weak
If baselines are poorly reproduced, defense gains will not be credible.

**Mitigation:** use official code where available; clearly label reimplemented attacks.

### Risk E — We measure only final outputs
This would miss the central claim.

**Mitigation:** require channel-level evaluation in every run.

---

## 16. Final problem statement

The concrete problem is:

> Given a multi-agent LLM runtime with shared memory, shared workspace, and tools, design and evaluate a defense that observes runtime information flows and prevents low-trust or privacy-sensitive content from being copied, transformed, or escalated across the system beyond policy-allowed recipients and abstraction levels, while preserving the system’s task-solving ability.

That is the exact problem FlowFence-Lite should solve in MVP.
