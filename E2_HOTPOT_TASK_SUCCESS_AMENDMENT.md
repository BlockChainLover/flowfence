# E2 HotpotQA episode-success amendment — 2026-09-20

HOT_POT_METRIC_FREEZE_TIMING: AFTER_TASK_SELECTION_AND_P1_BEFORE_ANY_MODEL_OUTCOME
HOTPOTQA_CONFIRMATORY_SUCCESS_METRIC: ORIGINAL_JOINT_EM
HOTPOTQA_EPISODE_SUCCESS_RULE: joint_em == 1.0
HOTPOTQA_FULL_METRIC_VECTOR_RETAINED: YES

The human resolves the pre-dispatch ambiguity prospectively. Use the unchanged original HotpotQA evaluator. For each scored episode retain every original returned metric: answer EM/F1/precision/recall, supporting-fact EM/F1/precision/recall, and joint EM/F1/precision/recall. Only original joint_em == 1.0 supplies the episode task-success boolean. Required answer and supporting facts must both be correct; no new metric, normalization, threshold or scorer modification is introduced. Later paper/supplement reporting must distinguish primary original joint EM from the full descriptive source-metric vector and retain this chronology.

The ambiguity was discovered before the first live model call. At amendment time development attempted/valid/model runs=0, formal/confirmatory runs=0, and no E2 privacy or model task-success outcome exists. No development/confirmatory ID, prompt, policy, fact type, A/B template, defense, recognizer or evaluator changed. P1 commit9290f71b9a3f8dd02334f88f7f331eb61751bd03 remains immutable. This amendment, not P1, is the authority for the new explicit Hotpot accounting rule.

TAT-QA sanity: P1 FAMILY_PROFILES.json already designates Original EM as success_metric; original F1 and scale metrics are retained separately. TATQA_EPISODE_SUCCESS_RULE: original per-episode EM == 1.0. Unlike the prior Hotpot list of candidate success metrics, this identifies one binary exact-match metric. Do not add an F1 threshold or scale-correctness conjunction. BIRD remains ORIGINAL_EX_ONLY; F1/VES diagnostic only.

This containing commit is HOT_POT_METRIC_FREEZE_COMMIT, reported externally to avoid self-reference. Push it before live runner implementation. Then resume the previously authorized54development cells after deterministic validation and FIRST_LIVE_RUNNER_COMMIT; no additional authorization is needed for the resolved Hotpot issue. All prior no-retry/no-repair/no-replacement/no-post-outcome-fix constraints remain. No confirmatory execution.
