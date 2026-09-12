# AAMAS 2027 experiment extension

## Goal
Complete the equal-capability comparator, real intermediate-agent slice, overhead measurements, representation stress, and conditional follow-ups in one session. Preserve all WINE evidence and package the new artifacts.

## Branch
`codex/aamas2027-experiment-extension`. Start HEAD: `28b2ab2b8c6cd14e018d6e5c95474a9880be768f`. The final source commit is recorded in the local MANIFEST.json and delivery bundle. No remote push.

## Completed work
- E0: 270 episodes, 90 matched pairs; PAPC and IFC tie on privacy and task success. PAPC has more interventions.
- E1: 144 registered attempts, 141 completed and 3 parser failures. Both guards have 48/48 task and privacy-safe successes; all 48 matched comparisons tie. No Defense has 44/48 task successes. The eight pilot episodes remain separate.
- E2: 45 timing trials and 1,665,000 timed events, with serialized audit storage measurements.
- E3: all 90 probes disclose the protected amount under the specified reconstruction evaluator. These are confidentiality failures, not execution failures.
- E4: 20 HTTP 403 failures; BLOCKED_BY_API. No second-family confirmation.
- E5: NOT_TRIGGERED; no topology interaction.
- Total: 470 API request attempts including pilot/E4, 23 formal execution failures, zero excluded episodes.

## Changed files
`.gitignore`, `src/defenses/mas_flowfence.py`, four additive `src/experiments/aamas_*` modules, five AAMAS scripts, the AAMAS JSON configs, four test files, the experiment README, roadmap/progress, this task state, and compact AAMAS audit/table/test artifacts. Large or detailed generated records, final reports, manifest and ZIP are local delivery artifacts excluded from Git. Pre-existing WINE changes remain separate.

## Validation commands
`PYTHONPATH=. /Users/crazy/anaconda3/bin/python -m pytest -q tests/test_aamas_equal.py tests/test_aamas_llm_agents.py tests/test_aamas_stress.py tests/test_aamas_package.py`: 64 passed.

`PYTHONPATH=. /Users/crazy/anaconda3/bin/python -m pytest -q tests`: 132 passed, one pre-existing failure, zero skipped/xfail. The unchanged legacy exporter test requires `papers/claims_checklist.md`, which is absent at the start SHA.

`PYTHONPATH=. python3 scripts/package_aamas2027.py --bundle`: create the delivery bundle. An independent extracted replay reproduced all E0/E3 nonlatency fields and completed E1 dry-run with zero API calls. Exact commands and reports are in the manifest and logs.

## Known limitations
One historical scenario and twelve new public parameter variants; no case where the private budget cap changes the correct public choice. The exact-string detector fails the tested transformations. The new common adapter corrects old mediation, template and truncation issues, so E0 is an adapted comparison rather than exact historical reproduction. E1 uses a fixed role order with actual generated decisions and deterministic tools; no adaptive scheduling or iterative recovery. The API does not receive a provider RNG seed. A returned model name is not an immutable weight revision. Full private prompts/responses remain under `/tmp/flowfence_aamas2027_20260912_private/` on the existing server with files mode 0600; they are excluded from Git and the bundle.

## Resume instructions
Read `artifacts/aamas2027/EXPERIMENT_SUMMARY.md`, `PAPER_INTEGRATION.md`, `MANIFEST.json`, and `PRIOR_EVIDENCE_AUDIT.md`. Rebuild tables with `scripts/package_aamas2027.py --reports-only`; no API is needed. Do not overwrite WINE or replace successful formal episodes. If E4 permission is repaired, preserve and link the original failed attempts and report the resumed attempts separately.

## Recommended next goal
Integrate the saved tables into a separate AAMAS draft. Frame the contribution as unified runtime mediation; drop claims of PAPC-specific superiority, independently validated topology necessity, and semantic confidentiality.
