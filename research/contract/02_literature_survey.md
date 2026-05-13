# FlowFence-Lite — Literature Survey

## 1. Inclusion rules

This survey is split into three buckets so that we stay honest about what we can rely on.

### Bucket A — Core references
Use these as **primary evidence and direct baselines**. Inclusion criteria:

- accepted at a top conference or top conference benchmark/datasets track,
- directly relevant to agent security, privacy, memory, or propagation,
- official code available on GitHub or Hugging Face.

### Bucket B — Top-conference paper signal, but no official code located
Use these as **paper evidence only**. Reimplement only if necessary.

### Bucket C — Supporting engineering references
Useful for implementation ideas, but **not** for headline paper claims if they are not top-conference main evidence.

As of **2026-04-18**, the links below were checked for paper and code availability.

---

## 2. Bucket A — Core references with open code

| Paper | Venue | Paper | Code | Why it matters to FlowFence-Lite | How we use it |
|---|---|---|---|---|---|
| AgentDojo: A Dynamic Environment to Evaluate Prompt Injection Attacks and Defenses for LLM Agents | NeurIPS 2024 (Datasets & Benchmarks) | https://openreview.net/forum?id=m1YYAQjO3w | https://github.com/ethz-spylab/agentdojo | Strong dynamic benchmark for tool-calling agents under prompt injection. | Use its task design philosophy, attack/defense API patterns, and dynamic evaluation style. |
| Agent Security Bench (ASB): Formalizing and Benchmarking Attacks and Defenses in LLM-based Agents | ICLR 2025 | https://openreview.net/forum?id=V4y0CpX4hK | https://github.com/agiresearch/ASB | Broad attack/defense coverage across tool use, memory poisoning, and mixed attacks. | Use as the main benchmark baseline for attack families and prompt-based defenses. |
| AgentPoison: Red-teaming LLM Agents via Poisoning Memory or Knowledge Bases | NeurIPS 2024 | https://openreview.net/forum?id=Y841BRW9rY | https://github.com/AI-secure/AgentPoison | Direct evidence that memory poisoning is a real agent attack surface. | Use as the memory-poisoning attack baseline. |
| Agent Smith: A Single Image Can Jailbreak One Million Multimodal LLM Agents Exponentially Fast | ICML 2024 | https://proceedings.mlr.press/v235/gu24e.html | https://github.com/sail-sg/Agent-Smith | Establishes the “infectious” propagation framing in multi-agent systems. | Use as the conceptual motivation for propagation/cascade modeling; keep as post-MVP multimodal stress test. |
| G-Safeguard: A Topology-Guided Security Lens and Treatment on LLM-based Multi-agent Systems | ACL 2025 (Long Paper) | https://aclanthology.org/2025.acl-long.359/ | https://github.com/wslong20/G-safeguard | Strong evidence that topology and message-graph structure affect security outcomes. | Use as the topology-aware defense baseline and as the closest conceptual competitor. |
| AgentDAM: Privacy Leakage Evaluation for Autonomous Web Agents | NeurIPS 2025 (Datasets & Benchmarks) | https://openreview.net/forum?id=qaxf7q41aK | https://github.com/facebookresearch/ai-agent-privacy | Makes “data minimization” measurable end-to-end for agentic systems. | Use for privacy metrics, policy framing, and a prompt-based privacy-defense baseline. |
| A-MEM: Agentic Memory for LLM Agents | NeurIPS 2025 | https://openreview.net/forum?id=FiM0M8gcct | https://github.com/agiresearch/A-mem | Strong memory backend that improves utility; useful to test whether better memory also enlarges privacy attack surface. | Use as a stronger memory backend baseline if integration cost is manageable. |

---

## 3. What each core reference contributes

### 3.1 AgentDojo
**Value:** dynamic attack/defense evaluation with tool usage.  
**What it gives us:** a clean precedent for treating agent security as an extensible environment rather than a static benchmark.

**What it does not solve:**  
It is not designed around **multi-agent shared-memory privacy propagation**. We should borrow its environment style, not its exact problem framing.

### 3.2 ASB
**Value:** broad systematization of attack/defense families.  
**What it gives us:** a large menu of attack types, evaluation logic, and prompt-defense baselines.

**What it does not solve:**  
It does not center on **internal privacy channels**, **shared workspace governance**, or **propagation-aware privilege control**.

### 3.3 AgentPoison
**Value:** clean, credible memory poisoning baseline.  
**What it gives us:** the strongest off-the-shelf evidence that memory is a controllable attack surface.

**What it does not solve:**  
It attacks memory but does not provide a unified defense combining propagation control and least privilege.

### 3.4 Agent Smith
**Value:** strong conceptual anchor for “infection” and cascade thinking.  
**What it gives us:** the framing that one compromised node can create system-wide spread.

**What it does not solve:**  
It is multimodal and not directly about privacy policy, shared workspace, or authorization.

### 3.5 G-Safeguard
**Value:** closest direct defense competitor.  
**What it gives us:** a topology-aware anomaly detection and intervention baseline for multi-agent systems.

**What it does not solve:**  
It reasons mainly over the **utterance graph**. It does not explicitly govern:
- raw vs safe memory views,
- shared document writes,
- cross-principal privacy policy,
- lease-based tool and write privileges.

### 3.6 AgentDAM
**Value:** direct privacy benchmark precedent.  
**What it gives us:** a strong operationalization of **data minimization** and privacy-vs-utility trade-off.

**What it does not solve:**  
It is not a multi-agent propagation paper. It does not model contamination spread over shared artifacts.

### 3.7 A-MEM
**Value:** strong memory system baseline.  
**What it gives us:** a utility-oriented advanced memory backend.

**What it does not solve:**  
It is not a privacy defense. In our project, A-MEM is important precisely because stronger memory may raise the bar for containment.

---

## 4. Bucket B — Top-conference paper signal, but no official code located

| Paper | Venue | Paper | Official code located? | Use in project |
|---|---|---|---|---|
| Unveiling Privacy Risks in LLM Agent Memory (MEXTRA) | ACL 2025 (Long Paper) | https://aclanthology.org/2025.acl-long.1227/ | I did **not** locate an official GitHub/HF repository during this survey. | Use as paper evidence that black-box memory extraction is a serious privacy threat; reimplement a simplified extraction attack only if needed. |

### Why MEXTRA still matters
MEXTRA is important because it turns privacy leakage from “accidental bad reasoning” into a **targeted extraction threat model**. It just should not be the first thing we try to reproduce if we want fast experimental progress.

---

## 5. Bucket C — Supporting engineering references (not primary claim anchors)

| Reference | Status | Link | Why it is useful |
|---|---|---|---|
| Firewalled-Agentic-Networks | Engineering comparator; not a top-conference accepted paper in the sources checked here | https://github.com/microsoft/Firewalled-Agentic-Networks | Useful for comparing against communication-layer rewriting / firewall ideas. |
| AiTM / Red-Teaming LLM Multi-Agent Systems via Communication Attacks | ACL 2025 Findings, not main long paper | https://aclanthology.org/2025.findings-acl.349/ | Useful as a communication-attack reference, but do not make it the core novelty comparator. |

**Rule:** these references may inform experiments, but they should not carry the main novelty claim if a top-conference main-track comparator is available.

---

## 6. Synthesis: what the literature already covers

The literature already provides strong evidence for the following:

1. **Tool-based agent attacks exist**  
   AgentDojo and ASB show that prompt injection and related attacks break real agent behavior.

2. **Memory is attackable**  
   AgentPoison shows poisoning; MEXTRA shows extraction.

3. **Propagation is real in multi-agent systems**  
   Agent Smith makes the cascade framing hard to ignore.

4. **Topology matters**  
   G-Safeguard shows that security is not independent of agent graph structure.

5. **Privacy should be measured against utility**  
   AgentDAM shows that privacy protection cannot be evaluated without task utility.

6. **Memory design matters for utility**  
   A-MEM shows that memory architecture is a first-order variable, not a background implementation detail.

---

## 7. The gap our project targets

No single core paper in the list above combines all four of these elements in one experimental system:

1. **Propagation-aware runtime modeling**
2. **Lease-based least privilege over agents / tools / writes**
3. **Shared-memory and shared-workspace content governance**
4. **Privacy evaluation over internal channels, not only final outputs**

That is the exact gap FlowFence-Lite should occupy.

---

## 8. Practical decisions for our project

### 8.1 Direct baseline set
We should treat the following as the main baseline pool:

- AgentDojo
- ASB
- AgentPoison
- G-Safeguard
- AgentDAM
- A-MEM

### 8.2 Conceptual motivation set
Use these to explain why the problem is important:

- Agent Smith
- MEXTRA

### 8.3 What not to over-promise
Do not say:
- “no one studied agent privacy before” — false
- “no one studied propagation before” — false
- “no one studied topology before” — false

Instead say:
> prior work studies these pieces separately; we unify them into a runtime privacy containment problem with shared-memory governance and privilege control.

---

## 9. Literature-driven design implications

The literature suggests the following concrete design choices.

### Implication A — keep the benchmark dynamic
Borrow this from AgentDojo/ASB.  
**Reason:** static prompts will not support runtime containment claims.

### Implication B — make memory first-class
Borrow this from AgentPoison, MEXTRA, and A-MEM.  
**Reason:** memory is both a capability source and an attack surface.

### Implication C — track internal channels
Borrow the privacy spirit from AgentDAM, but extend it to multi-agent internals.  
**Reason:** output-only evaluation will undercount leaks.

### Implication D — model graph structure
Borrow this from Agent Smith and G-Safeguard.  
**Reason:** propagation is not independent of topology.

### Implication E — compare against strong but narrow baselines
A good paper here must show that:
- prompt filtering alone is not enough,
- topology-only detection is not enough,
- data-minimization prompting is not enough,
- static ACL is not enough.

---

## 10. Survey conclusion

The literature is already strong enough to justify the problem and to supply competitive baselines. The project should therefore **not** be framed as “finding any agent privacy issue.” That part is already established.

The right framing is:

> existing work shows attacks, memory leakage, topology effects, and privacy-utility trade-offs; FlowFence-Lite targets the missing systems question of how to contain privacy propagation across shared memory, shared workspace, and privilege boundaries in a multi-agent runtime.

That framing is both concrete and defensible.
