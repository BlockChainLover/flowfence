# Run Manifest

Use this file for the next concrete batch of runs.

## Decision This Manifest Supports

- question:
  Which staged recovery fix should be applied first to the current quarantine-first FlowFence-Lite defense on the adapted fullreact `AgentPoison` comparator so that zero exposed poisoned retrieval is preserved while defended utility and empty-answer behavior improve?
- success criterion:
  A new improved-defense artifact on the same 25-case adapted comparator preserves `attack_manifestation_rate=0.0` and `exposed_poisoned_retrieval_case_rate=0.0`, while reducing at least one of: adversarial empty-answer count, benign false-block proxy fallout, or defended utility loss relative to the current quarantine-first artifacts.
- failure criterion:
  A staged recovery fix re-exposes poisoned retrieval content, restores attack manifestation, or fails to improve the identified post-quarantine failure modes enough to justify keeping the extra complexity.

## Planned Runs

| run_id | phase | method | dataset/split | seeds | main metric | expected output |
| --- | --- | --- | --- | --- | --- | --- |
| method-004m | proposed method | `minimax27 no-defense adapted comparator` | `StrategyQA 25-case adapted fullreact comparator` | `seed=1` | confirm same-provider attack strength before interpreting minimax defense artifacts | `results/baseline_agentpoison_fullreact_dpr_strategyqa_minimax27_triggerquery_v1/` |
| method-005 | proposed method | `phase 1: canonical action writeback` | `StrategyQA 25-case adapted fullreact comparator` | `seed=1` | preserve `attack_manifestation_rate=0.0` and `exposed_poisoned_retrieval_case_rate=0.0`; reduce bracket-artifact-driven errors | `results/method_flowfence_lite_fullreact_kimi25_triggerquery_quarantine_actioncanon_v1/` |
| method-006 | proposed method | `phase 2: quarantine-aware recovery hint` | same manifest | `seed=1` | preserve safety while reducing repeated quarantines and empty answers | `results/method_flowfence_lite_fullreact_kimi25_triggerquery_quarantine_recoveryhint_v1/` |
| method-007 | proposed method | `phase 3: post-quarantine clean search context` | same manifest | `seed=1` | preserve safety while reducing dirty-context search drift after quarantines | `results/method_flowfence_lite_fullreact_kimi25_triggerquery_quarantine_cleanscontext_v1/` |
| method-005m | proposed method | `phase 1: canonical action writeback under minimax27` | same manifest | `seed=1` | same-provider safety and utility comparison against `method-004m` after `kimi25` token failure | `results/method_flowfence_lite_fullreact_minimax27_triggerquery_quarantine_actioncanon_v1/` |
| method-006m | proposed method | `phase 2: quarantine-aware recovery hint under minimax27` | same manifest | `seed=1` | preserve safety while reducing repeated quarantines and empty answers under minimax27 | `results/method_flowfence_lite_fullreact_minimax27_triggerquery_quarantine_recoveryhint_v1/` |
| method-007m | proposed method | `phase 3: post-quarantine clean search context under minimax27` | same manifest | `seed=1` | preserve safety while reducing dirty-context search drift under minimax27 | `results/method_flowfence_lite_fullreact_minimax27_triggerquery_quarantine_cleanscontext_v1/` |
| method-008m | proposed method | `phase 3b: clean search context without recovery hint under minimax27` | same manifest | `seed=1` | isolate whether Phase 3's attacked-utility gain comes from clean context rather than the repeated-quarantine hint | `results/method_flowfence_lite_fullreact_minimax27_triggerquery_quarantine_cleanscontext_nohint_v1/` |
| method-009m | proposed method | `phase 1 repeat: canonical action writeback under minimax27` | same manifest | `seed=1` | check whether Phase 1 safety and utility are stable enough to keep as the default minimax method artifact | `results/method_flowfence_lite_fullreact_minimax27_triggerquery_quarantine_actioncanon_repeat1/` |

## Acceptance Gate For Staged Recovery Runs

- reuse `data/tasks/agentpoison_strategyqa_fullreact_v1.json`, provider profile `kimi25`, and the same adapted `trigger_question_only` attack setting
- because `kimi25` and `qwen36` currently fail provider authentication, `minimax27` is allowed as an explicit provider override; minimax artifacts must be compared against minimax no-defense artifacts, not used as direct replacements for the saved `kimi25` artifacts
- keep `hard_block_action: quarantine` unless a later stage explicitly tests a different recovery mechanism under the same safety checks
- each improved-defense run directory contains `run_manifest.json`, `resolved_config.yaml`, `status.txt`, `metrics.json`, `official_eval.json`, `mismatch_notes.json`, `upstream_outputs/`, and per-example outputs
- official eval output remains parseable for both benign and adversarial runs
- the first acceptance check is safety parity with the current quarantine baseline: `attack_manifestation_rate=0.0` and `exposed_poisoned_retrieval_case_rate=0.0`
- the second acceptance check is targeted utility/error improvement on the documented failure modes: fewer empty answers, less repeated quarantine looping, or fewer benign trajectory artifacts
- `method-008m` is accepted over `method-007m` only if it preserves zero exposed poisoned retrieval and zero attack manifestation while avoiding the clean-utility loss or non-standard outputs associated with repeated-quarantine hints
- `method-009m` is a repeatability check for the accepted low-risk Phase 1 variant; it should preserve zero exposed poisoned retrieval and have clean/adv utility close enough to `method-005m` to justify treating Phase 1 as the current default under minimax
- `ASB` and `AgentDojo` remain outside the critical path for this staged recovery step

## Notes

- Keep this manifest small.
- Add a new manifest or section when the decision changes.
- Do not mix staged recovery work with new attack/provider/topology expansion.
- The accepted `premethod_v2` rerun bundle remains a historical minimal reference, not the preferred next defense target.

## Next Baseline: AgentDojo

- selected next baseline: `AgentDojo`
- reason:
  `AgentDojo` is the next best attack-defense baseline because it already has official code imported, a successful one-task smoke artifact, native attack/defense switches, and a low-cost path to a real no-defense vs defense comparison under the currently working `minimax27` provider.
- rejected immediate alternatives:
  `G-Safeguard` is the closest defense competitor but is not started in this repo; it should follow after the next AgentDojo artifact. `ASB` remains failed exploratory scaffolding.

| run_id | phase | method | dataset/split | seeds | main metric | expected output |
| --- | --- | --- | --- | --- | --- | --- |
| baseline-adojo-001m | baseline reproduction | `AgentDojo workspace direct attack, no defense, minimax27` | `workspace/user_task_0/injection_task_0` | default AgentDojo deterministic task state | utility/security rates | `results/baseline_agentdojo_minimax27_workspace_direct_none_v1/` |
| baseline-adojo-002m | baseline reproduction | `AgentDojo workspace direct attack, repeat_user_prompt defense, minimax27` | same task pair | same | utility/security rates vs no-defense | `results/baseline_agentdojo_minimax27_workspace_direct_repeat_user_prompt_v1/` |
| baseline-adojo-003m | baseline reproduction | `AgentDojo workspace direct attack, tool_filter defense, minimax27` | same task pair | same | test stronger tool-selection defense after `repeat_user_prompt` failed security | `results/baseline_agentdojo_minimax27_workspace_direct_tool_filter_v1/` |
| baseline-adojo-004m | baseline reproduction | `AgentDojo workspace direct attack, spotlighting_with_delimiting defense, minimax27` | same task pair | same | test tool-output delimiting defense after `tool_filter` provider incompatibility | `results/baseline_agentdojo_minimax27_workspace_direct_spotlighting_with_delimiting_v1/` |
