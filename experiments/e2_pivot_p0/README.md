# E2 Pivot P0 design decision — 2026-09-18

AAMAS_E2_PIVOT_P0: READY_FOR_PUBLIC_TASK_SEARCH
E2_PIVOT_ARCHITECTURE: FEASIBLE (design only)

Current phase: contract setup. The next decision is human acceptance of this task/evaluator-under-standardized-harness design, followed by a separately authorized focused public task/evaluator source screen. Native-runtime replacement search stays CLOSED. No search or task selection occurred in P0.

## Review map

| Requirement | Artifact |
|---|---|
| A claim / P scale | ../../E2_PIVOT_CLAIM_BOUNDARY.md |
| B–E identities, provenance, ownership, tools | ../../STANDARDIZED_MAS_RUNTIME_CONTRACT.md; HARNESS_SCHEMA.json |
| F–G evaluator/task preservation | ../../ORIGINAL_EVALUATOR_PRESERVATION_CONTRACT.md |
| H dynamic orchestration / J PrivacyInstance / K–L parity and boundaries | ../../STANDARDIZED_MAS_RUNTIME_CONTRACT.md; TRANSITION_CLASS_DESIGN.md; TRANSITION_CLASSES.json |
| I evidence separation | ../../E2_E3_VALIDITY_SEPARATION.md |
| M acceptance | ../../PUBLIC_TASK_EVALUATOR_ACCEPTANCE_SPEC.md |
| N threats | ../../E2_PIVOT_VALIDITY_THREATS.md |
| O E4-B | ../../E4B_STANDARDIZED_RUNTIME_DESIGN.md |
| Q–S design-only validation | SCHEMA_FIXTURES.json; ../../artifacts/aamas2027_e2_pivot_p0/schema_validation.json |
| T commit/push | Branch codex/aamas2027-e2-pivot-p0; git history / remote verification in final response |

The schema is a transport/interface sketch. Fixture strings are synthetic references, not public tasks, actual grants, selected development instances or protected facts. Ten positive and seven negative shape checks passed. It does not verify provenance authenticity, authorization, source-schema equivalence, side effects, reference consistency, frozen-defense behavior or runtime mediation. The 23 transition classes are a finite proposed inventory; no runtime parity result is claimed.

## Reproduce the bounded validation

From repository root, using a temporary dependency directory:

```sh
python3 -m pip install --target /private/tmp/e2_pivot_schema_deps 'jsonschema==4.26.0'
PYTHONPATH=. python3 scripts/validate_e2_pivot_schema.py --help
PYTHONPATH=. python3 scripts/validate_e2_pivot_schema.py --dependency-path /private/tmp/e2_pivot_schema_deps --output artifacts/aamas2027_e2_pivot_p0/schema_validation.json
git diff --check
```

No dependencies were installed into the repository or a global Python environment. No full runner, source adapter, model generation or public benchmark integration was built. Existing R3 and recognizer files are unchanged. P0 has no design blocker; source availability at the full target scale, actual evaluator compatibility and implementation correctness remain unresolved future obligations. Seven release boundaries rely on trusted services and truthful accepted adapter effect declarations; no arbitrary native-code sandbox or broad information-flow security is claimed.

## Resume

Read the seven root P0 documents, this review map and the transition inventory. Preserve the target 60 E2 tasks / 1080 episodes and the other approved targets. Ask for the human design judgment; do not treat this artifact as execution/search authorization. Once separately authorized, apply the acceptance specification to task/evaluator sources without reopening native-runtime benchmarking or selecting final/development tasks prematurely. Do not merge prior feasibility branches or modify frozen R3/recognizer.
