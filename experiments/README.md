# Experiments

This folder is now organized for rebuttal lookup. Each paper has one evidence map that links paper tables and claims to the exact summary artifacts, raw result roots, metric definitions, and caveats.

## Paper Evidence Maps

- `experiments/emnlp2026_flowfence/README.md`: EMNLP retrieval-memory containment paper.
- `experiments/wine2026_flowfence/README.md`: WINE privacy-propagation externalities paper.

## Minimum Standard For New Experiment Plans

- State the paper and research question it supports.
- State the fixed task/domain, split, provider constraint, metrics, seeds, expected output directory, and stopping rule.
- Point to the intended paper table or claim before running.
- Update `research/logs/progress.md` in the same session.
- Do not add non-MiniMax experiment configs or claims in the current phase unless the human explicitly changes the provider constraint.
