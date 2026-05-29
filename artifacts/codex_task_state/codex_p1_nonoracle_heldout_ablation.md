# Codex Task State: p1-nonoracle-heldout-ablation

## Goal

Run a non-oracle held-out attack and ablation experiment for FlowFence-Lite to test whether containment holds without oracle attack annotations and under paraphrased attacks.

## Branch

`codex/p1-nonoracle-heldout-ablation`

## Oracle Signal Diagnosis

Default `flowfence_lite` used `attack_annotation.applied` inside `src/defenses/mas_flowfence.py` by OR-ing it into the poison signal. The runtime passed attack annotations from `src/runtime/orchestrator.py` during seed defense and final send defense. This is an internal-validity risk because those labels are ground-truth attack metadata.

The new `flowfence_lite_nonoracle` and `flowfence_lite_nonoracle_no_semantic_patterns` modes ignore `attack_annotation.applied`, `attack_id`, `attack_mode`, and attack ground-truth labels. Their decision metadata records `oracle_annotation_used=false`; the no-semantic ablation also records `semantic_patterns_enabled=false`.

## Implementation Changes

- Added `flowfence_lite_nonoracle` and `flowfence_lite_nonoracle_no_semantic_patterns`.
- Added held-out paraphrase attacks for summary poisoning, workspace poisoning, and communication hijack.
- Added non-oracle deterministic and targeted MiniMax configs.
- Added `scripts/audit_nonoracle_heldout.py`.
- Added tests for non-oracle defense behavior, held-out attacks, configs, and audit outputs.

## Deterministic Run Result

- Expected/completed/failed: 540/540/0.
- Provider calls enabled: false.
- `flowfence_lite_nonoracle`: task_success_rate=1.0, unauthorized_raw_leakage_mean=0.0, external_leakage_mean=0.0.
- Oracle annotation violation count for nonoracle modes: {'flowfence_lite_nonoracle_no_semantic_patterns_oracle_annotation_used_true_count': 0, 'flowfence_lite_nonoracle_oracle_annotation_used_true_count': 0}.
- Interpretation: nonoracle_holds.

## MiniMax Targeted Run Result

- Pilot 6-run executed and completed 6/6.
- Targeted expected/completed/failed: 72/72/0.
- Provider calls enabled: true, MiniMax only.
- `flowfence_lite_nonoracle`: task_success_rate=1.0, unauthorized_raw_leakage_mean=0.0, external_leakage_mean=0.0.
- Oracle annotation violation count for nonoracle mode: 0.
- Interpretation: nonoracle_holds.

## Committed Evidence Files

- `artifacts/nonoracle_heldout_deterministic/`
- `artifacts/minimax_nonoracle_heldout_targeted/`

## Validation Commands

See final response for the full validation command list.

## Known Limitations

- MiniMax is the only real provider represented.
- The deterministic matrix is synthetic-runtime only.
- The targeted MiniMax run uses MiniMax final-writer in the synthetic runtime, not a production browser/desktop/computer-use agent.
- Raw traces, raw provider outputs, prompts, event JSONL, policy JSONL, and individual metrics are not committed.

## Resume Instructions

If continuing, refresh claims and paper tables only after reviewing the committed high-level summaries. Do not use raw traces or provider outputs in claims.
