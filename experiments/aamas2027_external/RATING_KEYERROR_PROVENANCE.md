# Exact rating failure provenance

Diagnosis completed before repair on 2026-09-18. Original failure is not evidence of semantic task unsuitability.

- Source expression: `marble/evaluator/evaluator.py:108`, `Evaluator.evaluate_planning`, `planning_prompt_template.format(summary=summary, agent_profiles=agent_profiles, agent_tasks=agent_tasks, results=results)`.
- Template: `marble/evaluator/evaluator_prompts.json:9`, JSON path `Graph.Planning.prompt`. Three literal JSON examples contain unescaped braces. The same defect exists at line 5 (`Graph.Communication.prompt`), consumed by `Evaluator.evaluate_communication`, evaluator.py:78.
- Each `{"rating": X}` in the original template is interpreted by `str.format` as a replacement field with lookup key `"rating"` and format specifier ` X`. No such keyword is provided. The first example raises before any judge invocation.
- Initialization path: `Config(data)` → `Engine.__init__` → real Research/DB/Coding environment, agents, planner and Evaluator constructors (all pass; DB uses explicit service doubles) → `Engine.start:1043` → `Engine.star_coordinate:575` → `Evaluator.evaluate_planning:108`. Successful constructor frames cannot appear in a subsequent exception traceback. Their outcomes are separately saved in diagnosis/INTEGRATION_AUDIT.json (600 successful constructions).
- Canonical base: PRESENT. Already-backported 40ddb54 state: PRESENT; that commit's template bytes equal base exactly. `git blame` attributes the current bad lines to merged official PR #171, `03f4f30be6ec1ce376c253e02cbd8df4e642b418`; earlier branch `88c4177` also contains rating examples.
- Python string formatting: YES. Literal object braces parsed as placeholders: YES.
- Python-version dependency: NO supported-version-specific cause; this is built-in `str.format` syntax. Reproduced with Python 3.10.9 and the additional local interpreter recorded in PYTHON_FORMAT_CHECK.txt. This does not claim testing every Python release.
- Third-party-version dependency: NO for this exception. The minimal reproducer uses only built-ins. Importing the full benchmark has separate package requirements already recorded in Gate A-C.

Minimal reproducer (raises the exact KeyError without dependencies):

```python
'{"rating": X}'.format(summary='S', agent_profiles='P', agent_tasks='T', results='R')
```

Full deterministic STAR traceback (representative Research EXACT_IFC; all six environment/arm traces retained under diagnosis):

```text
Traceback (most recent call last):
  File "/private/tmp/flowfence_gate_a_worktree_20260918/scripts/certify_aamas_gate_ac.py", line 164, in main
    try:en.start();scheduler_modes.append('completed')
  File "/private/tmp/flowfence_gate_a_marble_20260918/marble/engine/engine.py", line 1043, in start
    self.star_coordinate()
  File "/private/tmp/flowfence_gate_a_marble_20260918/marble/engine/engine.py", line 575, in star_coordinate
    self.evaluator.evaluate_planning(
  File "/private/tmp/flowfence_gate_a_marble_20260918/marble/evaluator/evaluator.py", line 108, in evaluate_planning
    prompt = planning_prompt_template.format(
KeyError: '"rating"'
```

Reproduce the original template failure and independent rendered-text equivalence check with `PYTHONPATH=. /tmp/flowfence_gate_ac_env/bin/python scripts/audit_aamas_rating.py --benchmark /tmp/flowfence_gate_a_marble_20260918 --output /tmp/gate-ad-rating-replay`. This reads the original Git blob even when the checkout is repaired. `--apply-approved` is the explicit mutation option, used only after the human approval saved in the manifest.

No official exact fix found after canonical branch/tag/PR/history search. 262 fetched refs, 210 PR metadata records (63 merged), no tags. The earlier valid templates differ semantically and are rejected as backports. Candidate C changes only six brace pairs in two template values; exact diff retained. The approved patch was applied only after diagnosis and classification. It does not fix the failure by supplying a fictitious rating field, skipping evaluation, or replacing judge criteria.
