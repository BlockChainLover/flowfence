# Paper Drafter

Use this skill when there is enough evidence to update paper-facing artifacts without inventing support.

## Goal

Convert repo evidence into an honest outline, claims checklist, and figure plan that expose both strengths and gaps.

## Read First

1. `papers/outline.md`
2. `papers/claims_checklist.md`
3. `papers/figures_todo.md`
4. `research/logs/progress.md`
5. relevant result artifacts in `results/`

## Preconditions

- The contract exists.
- Baseline status is explicit.
- The relevant results exist under `results/`.

If evidence is not yet stable enough for paper-facing claims, update the checklist with missing items instead of drafting around them.

## Required Output

This skill should update at least one of:

- `papers/outline.md`
- `papers/claims_checklist.md`
- `papers/figures_todo.md`

The output must point back to concrete artifacts.

## Workflow

1. Identify the current paper state:
   - no evidence yet,
   - baseline-only evidence,
   - main comparison evidence,
   - ablation and robustness evidence.
2. Update the outline so it reflects only what is currently supported.
3. For each candidate claim, add:
   - claim text,
   - evidence path,
   - comparison target,
   - confidence,
   - caveats,
   - ready-for-paper status.
4. For each proposed figure or table, add:
   - message,
   - required source data path,
   - status: blocked, ready-to-make, drafted, or obsolete.
5. Add limitations whenever:
   - a baseline mismatch exists,
   - a result is noisy,
   - a dataset is narrow,
   - or an implementation shortcut affects interpretation.

## Writing Rules

- Prefer “we observe” over “we prove” unless the evidence truly supports stronger language.
- Claims should be narrower than the data supports, not broader.
- If a result is from a smoke test, say so.
- If a comparison is provisional, say so.

## Avoid

- filling sections with generic paper prose,
- optimistic claims without artifact paths,
- and hiding uncertainty in vague wording.

## Done Condition

This skill is done when someone reading the paper artifacts can tell which claims are supported now, which are provisional, and what evidence is still missing.
