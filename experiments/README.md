# Experiments

This folder contains only decision-oriented experiment plans. Each plan should answer one concrete question and point to a result directory convention in `results/`.

## Workstreams

### 1. Baseline reproduction

Purpose: make the unprotected runtime and narrow baselines runnable and auditable.

Required outputs:

- smoke run artifacts,
- baseline result artifacts,
- mismatch notes versus source papers or repos,
- fixed task split and metric definitions.
- pre-method comparison-ready artifact for the chosen critical-path baseline.

### 2. Method implementation

Purpose: reserved for after the baseline gate is passed.

Current status:

- blocked until the fixed `AgentPoison` pre-method subset is stable across reruns and comparable through the shared aggregation path.
- do not schedule FlowFence-Lite implementation runs until that gate is passed.

### 3. Ablations

Purpose: isolate which method components matter after the method exists.

Planned ablations:

- remove safe-view rewriting,
- remove quarantine,
- remove lease downgrade/revocation,
- remove topology-aware scoring features.

### 4. Robustness and error analysis

Purpose: test whether the defense generalizes and where it fails.

Planned analyses:

- leave-one-attack-out,
- leave-one-topology-out,
- failure-case review by channel,
- false-block and benign-quarantine analysis.

### 5. Paper assets

Purpose: map finished experiments to tables, figures, and checklist claims.

Required outputs:

- benchmark setup table,
- main comparison table,
- topology sensitivity figure,
- privacy-utility tradeoff plot,
- error analysis table.

## Minimum Standard For Any Experiment Plan

- clear name,
- decision question,
- fixed task/domain and split,
- metrics,
- seeds,
- expected output directory,
- stopping rule,
- log entry in `research/logs/progress.md`.
