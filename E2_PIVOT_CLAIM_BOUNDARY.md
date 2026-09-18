# E2 pivot claim boundary

Status: **P0 design proposal, not an implemented or certified runtime**. Date: 2026-09-18.
Native benchmark-runtime search is CLOSED. No dataset search/selection, development-task selection, benchmark integration, model generation, Gate B, R3 change or frozen-recognizer change is authorized here.

E2_CLAIM_SCOPE: PUBLIC_BENCHMARK_TASK_AND_EVALUATOR_EXTERNAL_VALIDITY_UNDER_A_STANDARDIZED_MULTI_AGENT_EXECUTION_HARNESS

Three objects must remain distinct:

1. **Public task semantics:** the externally authored objective, input, permitted knowledge/actions, output requirements and success condition.
2. **Original public evaluator semantics:** the source evaluator code/prompt, gold, reference state, thresholds, weights, judge configuration and failure semantics.
3. **Standardized experimental runtime:** our declared coordinator/worker orchestration, typed state and release boundaries. This is a new experimental execution system, not the benchmark's original agent architecture.

If future accepted families, adapters and executions meet the contracts, E2 can test whether the frozen defense comparison transfers to externally authored task objectives and original external scoring under the declared MAS harness. It can report public-task utility and measured privacy propagation within that harness, with task-level uncertainty and augmentation caveats. P0 itself supplies no utility, safety, effectiveness, parity-execution or generalization result.

It cannot support original benchmark-runtime external validity, native benchmark MAS evaluation, reproduction of the original agent architecture, native-runtime leaderboard equivalence, universal confidentiality, broad recognizer robustness, all-tool mediation or topology-independent safety. Multiple workers are supplied by the experiment; public datasets must not be described as natively multi-agent because of that decomposition.

The task/evaluator source is externally fixed; roles, prompts, budgets, routing affordances and adapters are experimental choices disclosed with the eventual results. Preserving task semantics does not imply preserving the original solver's difficulty or score distribution.

The human closure of MARBLE, the three other audited designs and τ² as a direct replacement remains effective. This pivot does not reopen those native runtimes or select their task data. Prior audit branches remain separate; no feasibility branch is merged into P0.

Targets remain E2 60×3×2×3=1080; E3 18×3×2×3=324; E4-A 24×3×2×2=288; E4-B 18×2×2×2×2=288. E2 prefers three predeclared task families at 20 confirmatory tasks each plus at least three disjoint development tasks per family. Preserve protected-fact balance P1/P2/P3/P4=15 each. Approximately 84 unique semantic tasks remains the primary semantic-scale target, subject to later human-approved cross-experiment overlap/replacement accounting. The episode counts sum to 1980; they are not 1980 independent semantic samples, and family totals across E1–E4 cannot be added to infer unique-task count.
