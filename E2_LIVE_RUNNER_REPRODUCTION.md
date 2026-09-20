# E2 live runner implementation and reproduction

Authoritative configuration: P1 commit9290f71b9a3f8dd02334f88f7f331eb61751bd03, followed by E2_HOTPOT_TASK_SUCCESS_AMENDMENT.md at its separate pre-outcome commit. No frozen config/defense/evaluator file is modified. All output is DEVELOPMENT_ONLY — NOT CONFIRMATORY EVIDENCE.

Implementation: src/e2_live/pilot.py; development-only launcher scripts/run_e2_development_pilot.py. The trusted runtime subclass observes the unchanged release callable exactly once and records attempted/candidate views. It does not alter the defense return. Committed publications are tracked separately from intermediate candidates, so a staged/rejected publication is not classified as released raw disclosure. Raw events, prompts, responses including reasoning, SQL, reference inputs and scorer outputs remain in a private directory (700; files600). Safe metadata carries hashes, numeric outcomes, IDs and decision categories only. No API key is written to audit artifacts.

Serial FIFO scheduler and action parser reuse the frozen P1 reference functions. Runtime context/history/receipts use only Session methods. Provider, SQL and scorer operations run in supervised child processes with bounded deadlines; timeout cancels and joins the child, no retry. Provider redirects are disabled to prevent hidden alternate requests. Original BIRD EX is invoked unchanged in a read-only, serial PostgreSQL session; runtime queries use the existing readonly broker. Original TAT and Hotpot scorers consume actual released native outputs. Hotpot stores the full12-metric vector and uses joint_em==1.0; TAT uses original EM==1.0. Source evaluator gold never enters Runtime or provider contexts.

The launcher admits only byte-frozen schedule cells whose family/task IDs are in the development input map. There is no arbitrary task, model, prompt or endpoint override. It refuses existing output directories (no implicit resume/rerun), records attempts before execution and stops on IMPLEMENTATION_DEFECT. Ordinary failures remain valid development observations. A queued condition whose edge is not proposed is not considered containment success.

## Pre-run validation

With restored pinned dependencies/source/DB as in E2_S1R_REPRODUCTION.md:

```bash
PYTHONPATH=.:/private/tmp/e2_s0_deps python3 scripts/check_e2_live_runner.py --source-root /private/tmp/e2_s0_sources --schema /private/tmp/e2_s1r_schema.json --output artifacts/aamas2027_e2_development_live/runner_mock_validation.json
PYTHONPATH=.:/private/tmp/e2_s0_deps python3 scripts/check_e2_live_environment.py --source-root /private/tmp/e2_s0_sources --schema /private/tmp/e2_s1r_schema.json --output artifacts/aamas2027_e2_development_live/environment_validation.json
python3 -m py_compile src/e2_live/pilot.py scripts/run_e2_development_pilot.py scripts/check_e2_live_runner.py scripts/check_e2_live_environment.py
```

The first script cannot open sockets:54complete mocked cells plus FIFO, quarantine, strict parser, transport-failure,24call-budget and confirmatory-rejection scenarios. The second uses one fixed development source reference per family solely as a deterministic scorer output fixture, plus real broker SELECT/write rejection and supervised cancellation. These are not model outcomes or pilot episodes. All58P1 and45historicalR3hashes and10source/evaluatorfiles are verified. Original restored schema SHA matches P1. --help is available on every new script.

Before executing, commit this implementation and supply its full SHA as --first-runner-commit. Keep the separate Hotpot amendment SHA. Copyable launch shape (credentials and raw path are local-only):

```bash
PYTHONPATH=.:/private/tmp/e2_s0_deps python3 scripts/run_e2_development_pilot.py --source-root /private/tmp/e2_s0_sources --schema /private/tmp/e2_s1r_schema.json --provider-env /Users/crazy/Desktop/agent-privacy-defense/FlowFence-Lite/data/secrets/e2_development_20260920/provider.env --private-output /Users/crazy/Desktop/agent-privacy-defense/FlowFence-Lite/data/secrets/e2_development_20260920/raw --output artifacts/aamas2027_e2_development_live/run --first-runner-commit FULL_RUNNER_SHA --hotpot-amendment-commit FULL_AMENDMENT_SHA
```

Never rerun this command against an existing output or invent a replacement directory after any live attempt. The original user authorized exactly one54cell pass, no post-outcome implementation fix/rerun. No confirmatory execution follows completion. Metadata registration and final report record actual SHAs and commands.
