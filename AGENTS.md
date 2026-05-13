# Topic Research Operating Guide

This repository is a single-topic working repo created from the workspace template. The workspace root may contain many topic folders, but this repo should contain exactly one topic, one contract, one evolving result history, and one paper narrative.

If there is tension between speed and auditability, choose auditability.

## First 10 Minutes

Before writing code or running experiments:

1. Read everything in `research/contract/`.
2. Read `research/logs/roadmap.md` and `research/logs/progress.md`.
3. State the current phase in one line:
   - contract setup,
   - baseline scouting,
   - baseline reproduction,
   - proposed method,
   - paper drafting.
4. Identify the single next decision the repo needs.
5. Work on the smallest action that resolves that decision.

If `research/contract/` is empty or vague, do not proceed to experiments. Write the missing contract material first.

## Hard Execution Order

Unless the user explicitly overrides it in writing, follow this order:

1. Contract
2. Baselines
3. Proposed method
4. Ablations
5. Paper-facing synthesis

The proposed method must not become the default first step. Baseline reproduction is the gate.

## Non-Negotiable Gates

### Gate 1: Contract Ready

The contract is ready only if `research/contract/` states:

- problem definition,
- threat model,
- target datasets,
- evaluation metrics,
- required baselines,
- success criterion,
- disallowed shortcuts or constraints.

### Gate 2: Baseline Ready

The baseline stage is ready only if at least one target baseline has:

- a source paper or repo,
- runnable instructions,
- fixed dataset split and metrics,
- a saved result artifact,
- and a note on any mismatch from the original setup.

### Gate 3: Method Comparison Ready

The proposed method can be compared only after:

- baseline settings are fixed,
- metrics are fixed,
- the result path convention under `results/` is decided,
- and the comparison question is written in `experiments/`.

### Gate 4: Paper Claim Ready

A claim is paper-ready only if `papers/claims_checklist.md` points to:

- a concrete result artifact,
- the comparison target,
- the caveats,
- and the current confidence.

## Working Rules

- One topic per repo. Do not mix separate research questions in one cloned topic folder.
- One decision at a time. Every experiment should answer a specific question.
- Prefer a small credible run over a large vague sweep.
- Never change split, metric, or preprocessing silently after comparisons begin.
- Never describe a baseline as reproduced if it only completed a smoke test.
- Never write polished claims before the evidence exists.

## Required File Discipline

Use these locations consistently:

- `research/contract/`: scope, threat model, hypotheses, evaluation, constraints.
- `research/logs/roadmap.md`: current phase, next milestones, blockers, decision gates.
- `research/logs/progress.md`: dated execution log with commands, artifacts, outcomes, next steps.
- `research/notes/`: source summaries, open questions, scratch reasoning worth keeping.
- `baselines/`: baseline-specific notes, wrappers, imported code, reproduction checklists.
- `datasets/`: access notes, licenses, snapshots, preprocessing assumptions, split definitions.
- `experiments/`: experiment plans, config references, run manifests, comparison matrices.
- `results/`: metrics, tables, logs, plots, and per-run outputs.
- `papers/`: outline, claims checklist, figure backlog, draft material.
- `scripts/`: reusable scripts only. Do not treat shell history as the workflow.

## Required Logging For Any Meaningful Work

If you run code, change a plan, or alter a claim, update `research/logs/progress.md` in the same session.

At minimum log:

- date,
- objective,
- action taken,
- commands or files touched,
- artifact paths,
- result or failure,
- next step.

If there is no artifact path, the work is probably not complete enough to support a claim.

## Result Naming

Prefer stable, readable result directories such as:

- `results/smoke_<date>_<short-name>/`
- `results/baseline_<method>_<dataset>_<date>/`
- `results/method_<variant>_<dataset>_<date>/`
- `results/ablation_<question>_<date>/`

Avoid names like `tmp`, `test2`, `final_final`, or unnamed notebook outputs.

## Baseline-First Decision Policy

When deciding what to do next, prefer this priority order:

1. Clarify contract ambiguity.
2. Remove a blocker to baseline reproduction.
3. Reproduce the strongest baseline.
4. Run the smallest experiment that could falsify the proposed method.
5. Expand with ablations only after the core comparison is credible.

## Writing Standard

- Observations and interpretations must be separable.
- Use modest, testable language.
- Mark speculation explicitly.
- If a result is partial, noisy, or mismatched, say so.
- If a baseline underperforms the paper, explain the gap before using it in a headline comparison.

## Handoff Standard

A collaborator should be able to resume work by reading only:

1. `research/contract/`
2. `research/logs/roadmap.md`
3. `research/logs/progress.md`

Write those files accordingly.

## Definition Of Healthy Repo State

This repo is in a healthy state when:

- the contract is specific,
- the roadmap names the current decision and next milestones,
- baseline status is explicit,
- all serious runs have traceable outputs,
- and paper-facing claims are narrower than the evidence, not broader.
