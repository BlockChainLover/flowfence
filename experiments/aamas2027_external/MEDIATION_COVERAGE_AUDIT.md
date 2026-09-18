# Gate A-D mediation coverage

MEDIATION_COVERAGE: NOT_VERIFIED. None of the three environments has complete propagation coverage. Recovery and one Coding hook do not erase the remaining bypasses.

Each installed release records actor, recipient, channel, decision and post-release exact raw-disclosure boolean. Private fixture text and evaluator gold are not saved in safe evidence. Exact matching is the frozen observation scope, not a semantic confidentiality guarantee.

| Producer → consumer | Storage/transport | Hook / observation | Bypass assessment |
|---|---|---|---|
| Planner → agent | assigned task / act argument | assign_tasks return and act input; release observer | actual clean fixture passes; other context fields not fully covered |
| Agent → peer | send/receive msg_box | both instance methods; release observer | actual send/receive exercised; all generated multi-turn session paths not certified |
| Agent → self context | BaseMemory update/get_memory_str | two wrappers; release observer | `str(memory)` and retrieve_all/direct storage bypass these wrappers; session builds context using str(memory) |
| Agent → shared memory | per-agent SharedMemory | absent | separate stores created by BaseAgent; public interfaces unwrapped |
| Agent → planner | act return / results | return release observer | raw result logged inside act first |
| Planner → shared progress/context | planner summaries, engine memory | partial summary/progress/update wrappers | original dynamic planner branches and direct retrieval not fully covered |
| Agent → tool | apply_action args | whole argument artifact; release observer | actual Coding invocation tested; other tool internals remain uncovered |
| Tool → agent | returned value / last_action_result | apply_action return; release observer | side effects can occur before this hook |
| Research tools → agent | queries / HTTP papers | outer arguments/results | real external dependencies mocked; intermediate source implementations not exhaustively exercised |
| Database tools → database/process/alerts | SQL, files, Docker, HTTP | outer arguments/results | database triggers, logs, subprocess side effects unmediated/unverified; live infrastructure not certified |
| Coding create_solution → shared file | solution.py | new scoped workspace write release; observer | 200 protected real-handler fixtures intercepted; clean 200 unchanged |
| Coding reviewer/debugger/analyst → shared file | revisions/advice/docs/error files | absent inside handlers | source confirms alternate writes, including same solution.py; not closed by coder-only hook |
| Coding generated code → filesystem/process | pytest/Popen/temp files | no process mediation | positive source path; cannot claim complete mediation or remove capability |
| Workspace → nested Coding models/evaluator | file reads / assembled prompts | no general nested-context wrapper | tool return mediation occurs too late for nested consumers |
| Engine → final artifact | _write_to_jsonl | final release observer | exercised; other output/debug channels remain |
| Agent/tool/planner → logs/console | logger, print, reviewer advice_log | absent | source directly prints/logs generated content; must stay private; not safe artifacts |

Protected data can reach these paths via the private sidecar and generated copying. No absence of data in a clean mock is used to certify a path. Uncovered source paths are recorded as unresolved certification, not proof that public tasks are semantically unsuitable. No whole-system coverage claim; hard stop conditions 3–5 and 9 prevent Gate B.
