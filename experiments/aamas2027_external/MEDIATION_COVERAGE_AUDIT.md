# Gate A-C mediation coverage

MEDIATION_COVERAGE: NOT_VERIFIED

Actual instance wrappers are in src/experiments/aamas_gate_ac.py. The privacy observer records post-release exact raw disclosure using the same policy; it does not perform semantic reconstruction. Safe audit output contains booleans/IDs, never fixture secret text or benchmark gold. Private raw model/tool text is not a safe trace.

| Surface | Protected data reachable | Adapter interception / observer | Bypass status |
|---|---|---|---|
| Agent input task | Yes | act wrapper before task argument enters original act; observed | Complete context includes other fields; full coverage unresolved |
| Agent private memory | Yes, authorized owner | update and get_memory_str wrapped; observed | retrieve_all/direct storage access not wrapped; stores are Python objects, not isolated processes |
| Agent→agent | Yes | send_message and receive_message wrapped, including direct receive; observed | Script exercises actual methods; complete session-turn coverage not proven |
| Agent result→planner | Yes | act return wrapped before planner gets tuple; observed | Internal logger sees original result before return |
| Planner shared progress | Yes | update_progress, summarize_output and assign_tasks returns wrapped; observed | Other direct planner state accesses require full-path validation |
| Engine shared memory | Yes | configured BaseMemory.update wrapped; observed | retrieve_all/direct storage not wrapped |
| Per-agent SharedMemory | Potential | No wrapper on these separate objects | Existing BaseAgent ignores passed shared memory and allocates its own; no false common-blackboard claim |
| Tool arguments | Yes | apply_action serializes whole argument artifact before original handler; observed | No malformed rewritten JSON forwarded; both arms use same blocked-tool interface |
| Tool returned result | Yes | apply_action return and last_action_result mediated; observed | Internal side effects precede this hook |
| Research query/retrieved paper | Yes | outer tool arguments/return covered with HTTP doubles | Network tool implementations and intermediate derived data not fully exercised; unresolved |
| Database SQL/storage | Yes | outer argument/return covered; SQL connection/process mocked | Actual DB writes, logs, triggers and alerts unverified; no live DB isolation claim |
| Coding solution/document | Yes | outer arguments/returned content covered | CONFIRMED BYPASS: create_solution writes shared solution.py before return wrapper |
| Nested coding model input/output | Yes | Not fully hooked by production adapter | Only deterministic response double installed in audit; a mock is not mediation |
| Final JSON output | Yes | _write_to_jsonl receives mediated artifact; observed | Other logging/output paths not redirected by adapter |
| Logger/console | Yes | No privacy-safe logger implementation | Original prompts/results logged internally; must remain private, not released as safe logs |

The Coding bypass is tested using the ORIGINAL create_solution handler, staged original task config, real temporary file writes, and a static model response containing the synthetic protected value. Under each defense, for each100 Coding tasks, that value is present in solution.py before the outer adapter returns.200 positive bypass fixtures are saved as booleans, not scientific leakage episodes. No real generation was made. An outer tool wrapper cannot truthfully certify whole-artifact write mediation.

No safety result is inferred from a quiet mock. Research and DB coverage remains unresolved; Coding coverage fails for the current adapter. Closing internal-handler writes requires additional integration work, not detector changes. No new evaluator, detector or reconstruction oracle was introduced.
