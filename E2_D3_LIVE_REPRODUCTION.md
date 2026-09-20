# E2 V3 D3 authorized development execution

Human authorization on2026-09-20 permits exactly54 frozen E2_DEVELOPMENT_V3_D3 cells, once, in frozen order. Reviewed D1 head dc40ab91d3cc06bcce56841b52044f6847d3826e; selection rule9e142e7a2ff282e986798da096ec525c0b03bb37. This authorization supersedes the D1 design-stage no-live status only for these54cells. V1/D2 closed; confirmatory/formal execution prohibited; no automatic V4.

The additive D3 CLI binds the exact schedule, full cell identities and nine admitted tasks to unmodified V3 runtime, prompts, schemas, MiniMax configuration, original source adapters and evaluators. It excludes78prior IDs and rejects arbitrary IDs/namespaces. Observational wrapper records trusted-stage participation and treatment states; any valid finance handoff without exactly one treatment entry, early/duplicate/wrong-edge treatment, writer before handoff or quarantine continuation is an IMPLEMENTATION_DEFECT hard stop. No runtime repair or rerun. Requests and raw trajectories stay local, ignored, mode700directories/600files; credentials are read in place from the previously authorized local file, never copied/displayed.

Pre-run commands:
```sh
PYTHONPATH=.:/private/tmp/e2_s0_deps python3 scripts/check_e2_d3_admission.py --source-root /private/tmp/e2_s0_sources --schema /private/tmp/e2_s1r_schema.json --output artifacts/aamas2027_e2_v3_d3_live/admission_validation.json
PYTHONPATH=.:/private/tmp/e2_s0_deps python3 scripts/check_e2_d3_environment.py --source-root /private/tmp/e2_s0_sources --schema /private/tmp/e2_s1r_schema.json --output artifacts/aamas2027_e2_v3_d3_live/environment_validation.json
PYTHONPATH=.:/private/tmp/e2_s0_deps python3 scripts/check_e2_v3_runtime.py --output /private/tmp/e2_d3_treatment_tests.json
```
Admission test includes54mockepisodes,27initial pairs,83invalid identities, and saved-evidence audit reconstruction. Environment checks use D3 reference fixtures only, never model calls or prior-task scoring. PostgreSQL14.24 cluster /private/tmp/e2_s1_pg_data must be running, with original read-only broker and original evaluator route.

Run ONCE after committing runner; substitute the actual first runner commit recorded in run/registration.json:
```sh
PYTHONPATH=.:/private/tmp/e2_s0_deps python3 scripts/run_e2_d3_live.py --source-root /private/tmp/e2_s0_sources --schema /private/tmp/e2_s1r_schema.json --provider-env /Users/crazy/Desktop/agent-privacy-defense/FlowFence-Lite/data/secrets/e2_development_20260920/provider.env --private-output /Users/crazy/Desktop/agent-privacy-defense/FlowFence-Lite/data/secrets/e2_development_v3_d3_20260920/raw --output artifacts/aamas2027_e2_v3_d3_live/run --first-runner-commit FIRST_COMMITTED_RUNNER
```
Existing output paths are rejected. Never relaunch to resume. STOP in the run directory prevents new cells. Ordinary failures are retained. Implementation defects stop new cells; no fixes after first outcome. Conditional treatment entry must be100% among valid A/B handoffs. Unconditional handoffs/36 is reported without a numeric readiness threshold. Missing writer after terminal R2 quarantine is expected. Privacy UNKNOWN is never counted as containment.

Read-only saved-evidence audit (no model/evaluator dispatch):
```sh
PYTHONPATH=.:/private/tmp/e2_s0_deps python3 scripts/summarize_e2_d3_live.py --run artifacts/aamas2027_e2_v3_d3_live/run --private /Users/crazy/Desktop/agent-privacy-defense/FlowFence-Lite/data/secrets/e2_development_v3_d3_20260920/raw --output artifacts/aamas2027_e2_v3_d3_live/derived
```
Audit checks saved request reconstruction, original metric vectors, raw privacy and actual treatment publication/consumption. B2 recipient-level records sharing one artifact count as one treatment submission. Provenance descendants are descriptive lineage, not semantic leakage. No significance tests, pooled cross-family utility, confirmatory CIs or ranking.
