# Repro Runner

Use this skill when actually executing a smoke test, baseline reproduction, proposed-method run, or ablation.

## Goal

Run experiments with enough structure that results can be trusted, resumed, and compared later.

## Read First

1. relevant plan in `experiments/`
2. `research/contract/`
3. `research/logs/progress.md`

## Before Launch

Confirm all of the following:

- the run type is known,
- the dataset and split are fixed,
- the metric definition is fixed,
- the output directory under `results/` is chosen,
- and the command or script is explicit.

If any of those are missing, stop and fix the plan before running.

## Required Output

Every run handled with this skill should leave:

- a dated progress entry before launch,
- a stable result directory under `results/`,
- a post-run note with metrics or failure details,
- and, when relevant, a comparison against the intended baseline target.

## Workflow

1. Record a pre-run entry in `research/logs/progress.md`:
   - objective,
   - run id,
   - command or script,
   - expected output path,
   - success criterion.
2. Execute the smallest viable version first if the pipeline is unproven.
3. Save outputs using a stable directory name.
4. After the run, record:
   - completion status,
   - key metrics,
   - config reference,
   - data snapshot or split,
   - notable warnings or mismatches,
   - next decision.
5. For baseline runs:
   - compare against reported or expected values,
   - state the gap,
   - state whether the baseline is credible enough for comparison.
6. For proposed-method runs:
   - compare only against fixed baseline settings,
   - do not change metrics or evaluation code to rescue a weak result.
7. For failed runs:
   - log the failure mode,
   - preserve logs if useful,
   - choose the narrowest next retry.

## Result Conventions

Prefer one directory per run or run group, for example:

- `results/smoke_<date>_<run-id>/`
- `results/baseline_<method>_<dataset>_<date>/`
- `results/method_<variant>_<dataset>_<date>/`

Put summary metrics near the run output rather than only in prose.

## Guardrails

- Do not overwrite previous result directories.
- Do not call a baseline “reproduced” without numbers.
- Do not mix debugging notes with final metrics; label them separately.
- Do not move on from a broken baseline without documenting the gap.

## Done Condition

This skill is done when a third party can inspect `experiments/`, `results/`, and `research/logs/progress.md` and reconstruct exactly what happened.
