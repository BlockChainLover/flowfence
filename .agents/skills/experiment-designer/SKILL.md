# Experiment Designer

Use this skill when the next task is to turn a research question into a small run matrix with decision value.

## Goal

Write a concrete experiment plan that can be executed without guessing parameters and that preserves the baseline-first workflow.

## Read First

1. `research/contract/`
2. `research/logs/roadmap.md`
3. `research/logs/progress.md`
4. `baselines/`

## Preconditions

- The contract states the main evaluation setup.
- Baseline targets have been selected.

If baseline status is unclear, resolve that first. Do not silently plan proposed-method runs as if baselines were done.

## Required Output

Create or update a plan in `experiments/README.md` or `experiments/run_manifest.md` that includes:

- experiment name,
- exact question being answered,
- comparison set,
- datasets and splits,
- metrics,
- seeds,
- output path convention,
- stop condition,
- and the next command or script to run.

Also update `research/logs/roadmap.md` with the next concrete milestones.

## Workflow

1. Write the single decision this experiment should resolve.
2. Classify the experiment:
   - smoke,
   - baseline reproduction,
   - proposed method,
   - ablation.
3. Write the minimum run set needed to resolve that decision.
4. For each run, define:
   - run id,
   - method or variant,
   - dataset and split,
   - seed count,
   - key hyperparameters that must be fixed,
   - expected runtime or cost,
   - expected result directory.
5. Add a stop rule for every phase:
   - smoke stops when the pipeline runs end to end,
   - baseline reproduction stops when numbers are within an acceptable gap or the mismatch is documented,
   - proposed method stops when it clearly helps, clearly fails, or needs redesign,
   - ablation stops when the main claim is already explained.
6. Ensure comparability:
   - same split,
   - same metric definition,
   - same evaluation code where possible.
7. Put any blocked assumptions into roadmap blockers instead of hiding them inside the plan.

## Design Rules

- One experiment plan should answer one main question.
- Prefer two or three decisive runs over a giant sweep.
- Lock evaluation details before launching comparison runs.
- Expensive runs need a cheap smoke version first.

## Avoid

- “explore everything” plans,
- ablations before the main comparison exists,
- and plans that cannot name where outputs will be saved.

## Done Condition

This skill is done when a collaborator can launch the next runs directly from the written plan and know how to judge success or failure.
