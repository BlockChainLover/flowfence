# Official STAR/GRAPH equivalence investigation

STAR_GRAPH_FEASIBILITY: ORIGINAL_DESIGN_NOT_FEASIBLE

Scope: pinned canonical MARBLE plus documented parser backport, and52 fetched official remote refs (includes HEAD alias), inspected at their recorded SHAs. Full per-ref engine-call survey is artifacts/aamas2027_gate_ac/TOPOLOGY_BRANCH_SURVEY.json. No official branch inspected exposes matching STAR/GRAPH evaluator and planning call signatures; this is a necessary-condition screen, not a proof about every possible future commit or third-party fork.

At base8d60fa17, GRAPH assigns full task to all agents initially then agent.plan_task; STAR planner.assign_tasks generates central allocations. AgentGraph uses supplied relationships for both, so mode STAR does not itself constrain graph edges to a star. Stop decision timing/progress updates and call budgets differ. GRAPH skips planning/communication/KPI judging and records-1; STAR invokes them. GRAPH has no Coding evaluator at base. These cannot be held fixed by merely toggling coordinate_mode.

Important official alternative found: maintainer fix/coding at c5d50755ffd66510bbb61ec1b0ec449f2b7d634a DOES add Coding evaluation to GRAPH and unifies certain paths. feature/env/coding_base_backup also contains a GRAPH Coding evaluator. This corrects the narrower prior impression that no official branch had that path. Neither removes central-vs-self planning or the scoring differences; no signature-matched route was found. We did NOT backport these engine changes or change the benchmark pin. Exact file diff inspected with git diff8d60fa17 origin/fix/coding -- marble/engine/engine.py.

Original design is not feasible under the requirement to hold exact task evaluator, prompts, tools, roles, stopping rules and scoring semantics fixed. A working Coding GRAPH evaluator alone would not isolate topology.

Possible scientific alternatives (not selected or implemented): (1) keep one official coordinator/planner/evaluator route fixed and manipulate only allowed communication edges with the same role/tool set; document that neighbor information necessarily changes with the graph and clarify what 'fixed prompts' means; (2) keep MARBLE E2 intact and run topology intervention only in the independently controlled E3 runtime with a shared scheduler and evaluator. Either changes the approved E4-B design and needs explicit human approval, preserving task/repetition scale unless separately authorized. No silent replacement or matrix reduction.
