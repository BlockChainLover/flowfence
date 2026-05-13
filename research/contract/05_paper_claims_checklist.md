# FlowFence-Lite — Paper Claims Checklist

## 1. Purpose of this file

This file is a **claim gate**.  
A claim should appear in the paper only if the required evidence box is checked.

Use the following status markers:

- `[ ]` not yet supported
- `[~]` partially supported
- `[x]` supported well enough for a paper claim

---

## 2. Core paper claims

## Claim C1 — Privacy leakage in multi-agent systems is a system-level propagation problem, not only a final-output problem

**Status:** [ ]

### Required evidence
- internal leakage is measured over at least:
  - agent messages,
  - memory writes/reads,
  - workspace writes/reads,
  - tool arguments,
  - final outputs
- internal leakage exceeds final-output leakage in at least **2 domains**
- blackboard or shared-memory topology materially increases leakage or cascade size

### Minimum threshold
- internal raw leakage > final-output raw leakage by a meaningful margin in at least 2 settings

### Disproof conditions
- almost all leakage is already visible in final outputs
- shared artifacts do not materially change exposure

### Paper wording allowed only if passed
> Privacy risk in multi-agent systems is undercounted by output-only evaluation because internal channels introduce substantial additional leakage.

---

## Claim C2 — FlowFence-Lite outperforms narrow baselines on privacy containment

**Status:** [ ]

### Required baselines
- no defense
- prompt filter
- static ACL
- topology guard
- data minimizer

### Required metrics
- unauthorized raw leakage
- unauthorized abstract leakage
- cascade size
- privilege reach
- utility retention

### Minimum threshold
FlowFence-Lite should satisfy **all**:
- better than no defense on all primary privacy metrics
- better than at least **3 of 4** non-trivial baselines on unauthorized raw leakage
- not worse than the strongest baseline by > 5% utility retention

### Strong threshold
- best or tied-best on leakage and cascade metrics,
- utility retention >= 90% of strongest baseline utility,
- advantage visible in at least 2 domains and 2 topologies

### Disproof conditions
- gains disappear after utility normalization
- one narrow baseline dominates FlowFence-Lite across most settings

### Paper wording allowed only if passed
> A unified runtime defense is more effective than prompt-only, topology-only, or static-access alternatives for containing privacy leakage and propagation.

---

## Claim C3 — Shared-memory governance and lease-based privilege control are both necessary

**Status:** [ ]

### Required ablations
- remove safe-view rewriting
- remove quarantine
- remove lease downgrade/revocation
- remove topology-aware scoring features

### Minimum threshold
At least **two** ablations must produce clear degradation on different axes:
- one should hurt leakage,
- one should hurt cascade or privilege reach.

### Disproof conditions
- one component alone explains almost all gains
- lease control adds no measurable benefit
- safe-view rewriting adds no measurable benefit

### Paper wording allowed only if passed
> Both content governance and runtime privilege control are necessary components of effective privacy containment.

---

## Claim C4 — Topology changes the privacy risk profile

**Status:** [ ]

### Required evidence
- same attack + same defense + same task family evaluated on multiple topologies
- measurable change in at least one of:
  - cascade size
  - privilege reach
  - containment delay
  - internal leakage rate

### Minimum threshold
- blackboard or star should be meaningfully different from chain/tree in at least 2 attack settings

### Disproof conditions
- topology has negligible impact once utility is matched
- differences are inconsistent across seeds and domains

### Paper wording allowed only if passed
> Privacy containment behavior depends materially on interaction topology, especially when shared artifacts are globally visible.

---

## Claim C5 — FlowFence-Lite generalizes beyond the attack/topology it was tuned on

**Status:** [ ]

### Required evidence
Run at least one:
- leave-one-attack-out
- leave-one-topology-out

### Minimum threshold
- FlowFence-Lite still beats no defense and at least 2 narrow baselines on the held-out setting

### Disproof conditions
- performance collapses on held-out attack or topology
- tuning clearly overfits to benchmark specifics

### Paper wording allowed only if passed
> The defense shows non-trivial generalization to unseen attacks or topologies.

---

## Claim C6 — The defense is practical enough to use at runtime

**Status:** [ ]

### Required metrics
- latency overhead
- token overhead
- false block rate
- percent of quarantined artifacts later judged harmless

### Minimum threshold
- latency overhead <= 25%
- token overhead <= 30%
- false block rate acceptable relative to utility target

### Disproof conditions
- the defense is too expensive or too disruptive
- utility falls mainly because of frequent false blocks

### Paper wording allowed only if passed
> The method is runtime-feasible in our benchmark setting.

---

## 3. Claims we should avoid unless evidence is unusually strong

Do **not** write any of the following unless there is direct evidence.

### Avoid A
“FlowFence-Lite is secure”  
Use instead: “reduces leakage/propagation in our benchmark.”

### Avoid B
“Provably prevents systemic privacy failures”  
Use instead: “empirically lowers cascade size / privilege reach.”

### Avoid C
“Generalizes across all agent frameworks”  
Use instead: “shows robustness across the tested runtime variants.”

### Avoid D
“Provides strong privacy guarantees”  
Use instead: “enforces explicit policy constraints within the benchmarked runtime.”

### Avoid E
“Solves multi-agent privacy”  
Never write this.

---

## 4. Evidence checklist by figure / table

## Table 1 — Benchmark setup
**Needed for paper:** [ ]
- tasks by domain
- topologies
- attacks
- defenses
- models
- seeds

## Table 2 — Main comparison
**Needed for paper:** [ ]
- leakage metrics
- cascade metrics
- utility metrics
- baselines + FlowFence-Lite

## Figure 1 — System overview
**Needed for paper:** [ ]
- runtime channels
- attack insertion points
- defense interception points

## Figure 2 — Propagation behavior
**Needed for paper:** [ ]
- cascade size or privilege reach vs topology / attack

## Figure 3 — Utility vs privacy trade-off
**Needed for paper:** [ ]
- utility retention vs leakage reduction

## Table 3 — Ablations
**Needed for paper:** [ ]
- remove lease
- remove safe view
- remove quarantine
- remove topology features

## Table 4 — Overhead
**Needed for paper:** [ ]
- latency
- token overhead
- false block rate

---

## 5. Artifact and reproducibility checklist

## Code release
- [ ] configs checked in
- [ ] schemas checked in
- [ ] run scripts checked in
- [ ] aggregation scripts checked in
- [ ] deterministic seed handling documented
- [ ] safe-shareable sample traces included

## Experiment reproducibility
- [ ] every reported metric can be recomputed from logs
- [ ] train/dev/test or tune/eval splits are documented
- [ ] held-out evaluation settings are not used for threshold tuning
- [ ] reimplemented baselines are clearly labeled as reimplemented

## Privacy hygiene
- [ ] safe traces contain no raw secrets
- [ ] private full traces are excluded from public artifact release
- [ ] report generation does not accidentally print secrets

---

## 6. Threats to validity checklist

These need to be written into the paper if relevant.

### Internal validity
- [ ] baseline implementations are faithful
- [ ] the same utility budget / model budget is used across methods
- [ ] thresholds are not tuned on test results

### External validity
- [ ] explain that MVP is text-first and tool-simulated
- [ ] explain that browser/desktop or multimodal agents are not covered
- [ ] explain that real enterprise deployment claims are out of scope

### Measurement validity
- [ ] raw leakage and abstract leakage are separated
- [ ] internal channels are logged
- [ ] safe-view rewriting is evaluated, not assumed safe

---

## 7. Pivot logic if results are mixed

## Pivot P1 — Method claim fails, measurement claim succeeds
If FlowFence-Lite is not clearly stronger than baselines, but internal leakage and propagation measurements are strong:
- pivot to a **benchmark / measurement** paper.

## Pivot P2 — Privacy claim weak, memory governance claim strong
If leakage metrics are noisy but safe-view and shared-memory governance clearly help:
- pivot to a **memory governance systems** paper.

## Pivot P3 — Generalization weak, main comparison strong
If held-out generalization is weak:
- keep the method paper, but narrow the claim and remove broad generalization language.

---

## 8. Submission readiness gates

Do not start paper writing seriously until the following are true.

### Gate G1 — Main result exists
- [ ] one complete main comparison table is stable

### Gate G2 — Ablation exists
- [ ] at least one ablation table is stable

### Gate G3 — Story is coherent
- [ ] evidence supports a single crisp narrative
- [ ] no central claim depends on optional/stretch baselines

### Gate G4 — Novelty is defensible
- [ ] we can explain clearly why this is not just prompt filtering, not just topology detection, and not just privacy prompting

---

## 9. Final claim template (only use if boxes are checked)

If the core boxes are checked, a safe headline claim is:

> We study privacy leakage in multi-agent LLM systems as a propagation problem over internal channels. We introduce FlowFence-Lite, a runtime containment layer that combines propagation-aware scoring, lease-based privilege control, and shared-memory governance. Across multiple domains, topologies, and attacks, it reduces unauthorized leakage and propagation relative to strong narrow baselines while preserving most task utility.

Do not use stronger wording unless the evidence truly supports it.
