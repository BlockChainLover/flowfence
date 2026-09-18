# E1, E2 and E3 validity separation

Status: **P0 design proposal, not an implemented or certified runtime**. Date: 2026-09-18.
Native benchmark-runtime search is CLOSED. No dataset search/selection, development-task selection, benchmark integration, model generation, Gate B, R3 change or frozen-recognizer change is authorized here.

E2_E3_VALIDITY_SEPARATION: EXPLICIT

| Experiment | What is externally constrained or controlled | Evidence it can add | Limit |
|---|---|---|---|
| E1 | Controlled mechanism cases and matched release decisions | Isolate the claimed mechanism under controlled inputs | Does not establish transfer to independent task objectives. |
| E2 | Externally authored public tasks and original external evaluator; one experimental MAS template | Transfer of utility/privacy behavior to independent semantic objectives and scoring under the declared harness | Does not validate original benchmark runtime or native assistant-team orchestration. |
| E3 | Purpose-built enterprise workflows with designed privacy-relevant dynamic delegation/tool use | Controlled stress of multi-hop delegation, tool opportunities and privacy-relevant state transitions | Workflows and scoring are authored for the study; cannot substitute for independent public-task evidence. |
| E4-A | Predeclared cross-model comparison | Model robustness on approved task overlap | Does not establish all-provider generalization. No new provider configured in P0. |
| E4-B | Direct communication-edge graph only | STAR/GRAPH direct-edge robustness in the standardized runtime | Does not isolate all information-flow topology. |

Sharing a runtime, tools API and frozen defenses across E2/E3 is desirable control, not duplicate evidence. Their task provenance and evaluator provenance differ. E2 must use source-native objectives/gold and original evaluation; it must not turn public task descriptions into bespoke enterprise tasks. E3 remains explicitly purpose-built and cannot be counted as public benchmark transfer. Report results in separate strata; never pool them as identically distributed tasks just because the event schema matches.

E2 dynamic coordination is solver behavior over independent objectives. E3 deliberately ensures specific privacy-relevant delegation/tool stresses are present. E2 need not be post-hoc filtered to retain only trajectories with rich propagation; absence of such opportunities must be reported as coverage/validity limitations. No task is removed because a defense looks uninteresting or two arms tie.

Preserved targets: E2 60 semantic tasks and 1080 episodes; E3 18 workflows and 324 episodes; E4-A 288 episodes; E4-B 288 episodes. Three conditions, two defenses and repetitions are repeated measurements of tasks, not new semantic instances. Maintain a later cross-experiment task identity table to account for overlap; approximately 84 unique semantic tasks is a target requiring human-approved accounting, not a sum inferred from matrix dimensions.
