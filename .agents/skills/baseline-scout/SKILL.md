# Baseline Scout

Use this skill when the repo needs a concrete baseline plan, not a broad literature review.

## Goal

Produce a small, defensible baseline set and a runnable reproduction plan that another collaborator can execute immediately.

## Read First

1. `research/contract/`
2. `research/logs/roadmap.md`
3. `research/logs/progress.md`

If the contract does not define task, threat model, datasets, and metrics, stop and fix the contract first.

## Required Output

This skill should leave behind all of the following:

- a named baseline list,
- a short reason each baseline is included,
- a reproduction order,
- a smoke-test command plan,
- a blocker list,
- and a progress-log entry.

Write the durable baseline plan into `baselines/README.md` or a dedicated note such as `baselines/<topic>_plan.md`.

## Workflow

1. Extract from the contract:
   - task,
   - threat model,
   - dataset and split,
   - metric definitions,
   - compute or licensing constraints.
2. Build a candidate list of baselines from prior work already known for this topic.
3. Reduce the list to the minimum credible comparison set:
   - one strongest standard baseline,
   - one closest comparable method family,
   - one simple non-novel baseline if needed for calibration.
4. For each selected baseline, record:
   - source paper or repository,
   - code status: available, partial, or missing,
   - exact dependency on datasets or preprocessing,
   - target metrics and expected ballpark values if known,
   - likely reproduction risks.
5. Decide the reproduction order:
   - cheapest sanity-check baseline first,
   - most important benchmark baseline next,
   - harder or fragile baselines after the pipeline is stable.
6. Define the first smoke test for the top baseline:
   - command or script reference,
   - smallest dataset slice or reduced setting,
   - expected artifact path under `results/`.
7. Update `research/logs/progress.md` with the chosen baselines, why they were chosen, and what will be run next.

## Decision Rules

- Favor baselines that can actually be reproduced in this repo’s constraints.
- Prefer quality of comparison over quantity of citations.
- A missing-code baseline can stay in scope, but must be marked as high risk.
- If metrics or splits differ across papers, record the mismatch instead of pretending they are directly comparable.

## Avoid

- collecting many baselines with no run plan,
- mixing papers from different problem definitions,
- and drifting into proposed-method design.

## Done Condition

This skill is done when the repo has an explicit answer to: “Which baseline do we run first, with what data, by what command, and why?”
