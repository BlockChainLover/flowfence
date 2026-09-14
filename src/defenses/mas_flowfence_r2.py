"""Post-observation PAPC repair: contaminated artifacts release no residual text."""
from src.defenses.mas_flowfence import DefenseResult, contains_poison_instruction, inspect_mas_event
from src.runtime.events import redact_preview, sha256_text

R2_MODE = 'flowfence_lite_nonoracle_r2'
QUARANTINE_MARKER = '[artifact quarantined]'
PROPAGATION_SURFACES = frozenset({'shared_raw', 'shared_doc', 'safe_view', 'internal_message',
                                 'external_message', 'vendor_send_tool', 'final_output'})


def inspect_r2_event(**kwargs):
    """Preserve all legacy modes. R2 changes release semantics, not recognition.

    No task/gold/evaluator input is accepted. Ordinary raw-secret handling is
    delegated unchanged. An existing hard block remains a hard block.
    """
    if kwargs['defense_mode'] != R2_MODE:
        return inspect_mas_event(**kwargs)
    legacy = dict(kwargs, defense_mode='flowfence_lite_nonoracle', attack_annotation=None)
    result = inspect_mas_event(**legacy)
    decision = dict(result.decision)
    policy = dict(result.policy_decision, defense_mode=R2_MODE)
    content = result.content
    if (result.decision['decision'] != 'block'
            and (kwargs['channel'] in PROPAGATION_SURFACES or kwargs['target_zone'] in PROPAGATION_SURFACES)
            and contains_poison_instruction(kwargs['content'])):
        content = QUARANTINE_MARKER
        decision.update(decision='quarantine', lease_signal='downgrade_shared_artifact',
                        hard_blocker=True, defense_fired=True,
                        rewritten_content_sha256=sha256_text(content),
                        rewritten_content_preview_redacted=redact_preview(content, kwargs['secret_policies']))
        policy.update(decision='quarantine', lease_signal='downgrade_shared_artifact', actions=['quarantine'])
    return DefenseResult(content=content, decision=decision, policy_decision=policy)
