# E2 Source S1 certification report

**AAMAS_E2_SOURCE_S1: NOT_READY.** This is an unsuccessful certification attempt with saved partial implementation and measurements, not completion of all S1 implementation obligations. No development pilot, Gate B, model generation, study contamination wording or final protected fact values were produced.

The single next decision is human admissibility of original BIRD VES (and treatment of original F1's row-order behavior), followed by completion of S1 runtime certification. EX succeeds for all500 records under the documented serial-query setting. This is not evidence that the entire standardized multi-agent harness is certified.

## Eligibility and naturalness

Predicate/schema and clustering rules were committed **before** S1 final per-task inspection in `0ed9269ff88be8b3656d50c70618adff47c46309`. No predicate was relaxed after measurement. Full per-task evidence is compressed, ordinary JSONL/CSV: `eligibility.jsonl.gz`, `naturalness_and_clusters.csv.gz`, `adapter_reachability.jsonl.gz` under `artifacts/aamas2027_e2_source_s1/`.

| Family | Official | Eligible | Ineligible | Unresolved | Context dependence |
|---|---:|---:|---:|---:|---|
| BIRD PostgreSQL | 500 | 0 | 0 | 500 | 11 source DB identities, combined restored PostgreSQL environment |
| TAT-QA | 1668 | 0 | 0 | 1668 | 278 source table/report contexts |
| HotpotQA distractor | 7405 | 0 | 0 | 7405 | 5918 bridge / 1487 comparison; 7404 distinct title sets |

All9573 records receive a source-family semantic rationale, compatible fact types, authorization/surface policy, clean-independence annotation and tri-state predicate values. Naturalness is a pre-result annotation applying the human-approved sidecar interpretation, not a scorer label or proof of actual attack pressure. BIRD P4 is natural private connection metadata; BIRD P3 remains unassigned pending a more specific request-domain assessment. TAT P1/P3 and Hotpot P2/P3 remain separate request-sidecar information. No sidecar is benchmark answer evidence; no P4 is assigned to Hotpot. These compatibility sets do not imply eligibility.

Every record is UNRESOLVED because complete family capability preservation, structural parity and mediation remain uncertified. BIRD additionally retains original-metric/DB-broker uncertainty. There are no documented semantic contradictions warranting INELIGIBLE. Full reason fields are stored per record; `pool_summary.json` summarizes the common reason distribution.

Hotpot has66581 unique supplied titles,5703 titles shared by multiple tasks,3184 title-overlap connected components, largest2439tasks. Exact-title overlap is not semantic entity resolution. Do not claim independent contexts from question count or title disjointness alone.

**FACT_BALANCE_FEASIBILITY: UNRESOLVED.** No eligible-pool allocation can be certified while every record remains unresolved. This is not a proof that Design A is impossible. No final allocation witness, selection rule, development IDs, confirmatory IDs or final type assignment was emitted. Counts selected:0/0; P1/P2/P3/P4 confirmatory counts all0. Development/confirmatory disjointness is not established for a nonexistent split.

## Adapters and mock orchestration

`src/e2_s1/adapters.py` implements family-wide public allowlists and native output reconstruction. No task-ID/defense/privacy-condition/gold-outcome branch is used. Gold is supplied only as a deterministic scripted **output fixture**, never in task initialization/context. The original evaluator remains outside the runtime; there is no evaluator-private input port on the prototype.

TAT inputs preserve full original table, paragraphs and public question ID/order; answer type, derivation and support labels are excluded. Hotpot inputs preserve all titles/sentences and explicit indices; no fullwiki/web capability. BIRD public fields exclude SQL; schema/description inputs are mapped by the source description files, not inferred from gold. All75 table names resolve in PostgreSQL. **BIRD's full constraint/schema discovery and operational read-only query broker are not certified or complete.** Column serialization alone is not a full allowed-schema/tool proof.

For every record, both frozen arms' deterministic fixtures traverse coordinator→worker1→worker2 messages, detached task state and final publication; native evaluator input is reconstructed from the actual released output. This checks serialization/reachability, not task solving. The generic graph and mock roles are identical across families; no family-specific task DAG or model invocation exists.

Family MAS semantic preservation status is **NOT_VERIFIED for all three families**. TAT/Hotpot input/output equivalence is verified separately, but cannot substitute for complete P0 runtime certification.

## Structural parity and mediation

`src/e2_s1/runtime.py` is explicitly an **interface prototype, not an accepted execution harness**. It implements owner handles, detached copies, integer revisions, queued messages, mediated staged state replacement, private self-access, output port and seven release hooks. The frozen R2 callable is copied byte-for-byte from the accepted prior audit into `src/e2_s1/frozen_r2.py`; the recognizer and existing R3 files are unchanged. The whole-artifact quarantine becomes the common invalid-JSON rejection where it does not satisfy a structured output contract; no task-specific repair is introduced.

Tests verify copy isolation, stale/unauthorized rejection, generic delegation, same configurations, and84 paired release cases (three families × seven boundaries × public/raw-fixture/A/B). Each paired call has identical permitted projection except the frozen arm selector. Raw fixture values are absent from released outputs. Representative A/B omit the sentinel and trigger the exact required recognizer hash `6bb7cba43724c10213ee4d81cdf2f82877fa6f5b831ca71c0698495866307d62`. These are deterministic template fixtures, not final study artifacts.

**STRUCTURAL_PARITY_IMPLEMENTATION: NOT_VERIFIED.** **MEDIATION_ARCHITECTURE_IMPLEMENTATION: NOT_VERIFIED.** `release_variants.json` enumerates all23 P0 transition classes and marks incomplete coverage. Hook reachability is deliberately not presented as coverage of actual query/result publication, typed provenance authority, all state operations, full tool errors/effects, retries, termination variants or source-schema validation after rewrites. In particular, current T15/T16 prototype dispatch does not implement a real query broker; trusted tool-origin authority and P0 typed envelopes need implementation. This prototype must not be used for a live model pilot. External connectors, shell and web are absent; unsupported actual external effects are not certified by a stub.

## Required next work / human review

1. Human decides whether original VES is admissible as a reported metric given saved instability; decide how to treat original F1 row-order sensitivity. Do not silently drop/redefine either.
2. Complete the actual read-only BIRD broker, full source schema metadata, typed P0 provenance/authority envelopes and all23 transition variants; verify seven-boundary domination of actual information paths. Replace prototype-only certification gaps with executable evidence, preserving frozen defenses.
3. Recompute eligibility using the same committed predicate. Resolve any BIRD P3 naturalness needed for balance without forcing assignments. Only after prerequisites pass, verify constrained balance, commit the selection algorithm, then emit the9/60 split.
4. Return for development-pilot review. This report authorizes no development runs or Gate B.
