# PAPC-R2 method change — post-observation quarantine repair

R1/R1.1 pilot was used to identify the residual-instruction flaw. R2 is a method revision informed by that development evidence, not preregistered confirmation of an unchanged method.

Variant: `flowfence_lite_nonoracle_r2`. Implementation: `src/defenses/mas_flowfence_r2.py`. All old modes and `src/defenses/mas_flowfence.py` remain byte-identical. IFC is delegated to that identical old inspector.

R2 first obtains the legacy non-oracle decision using attack_annotation=None. If a hard block already applies, it remains a block. Otherwise, when the existing observable poison/sensitive-request signal matches content on a shared or propagation surface, R2 quarantines the whole contaminated artifact and releases only the constant `[artifact quarantined]`. No substring of the artifact is used to construct that marker. Recognized surfaces are shared_raw, shared_doc, safe_view, internal_message, external_message, vendor_send_tool and final_output. Trusted private memory/tool surfaces retain the old behavior; pre-existing external-to-internal hard blocking remains stronger than marker release.

Ordinary exact raw-secret policy violations without recognized semantic/poison contamination still use exactly the original safe-view primitive and validator. Unrecognized paraphrases and representations do not gain a new detector. No new regex, arithmetic/threshold recognizer, task-specific branch, task gold, evaluator, second registry or attack annotation enters the defense. Existing risk scores/signals are inherited. The legacy safe-view may be computed privately before the R2 override, but its residual text is never released by the contamination branch.

The R2 episode adapter inherits tasks, prompts, workflows, generation/parsing, tools, event evaluators and parsed-action diagnostics. Its mediation route is an AST-identical copy of the old _mediate method, bound only to the versioned inspector. This additive adapter avoids changing R1/R1.1 runtime sources. Extra marker metadata and separate safe_view_rewrites counts are evaluator/reporting-only. Both R2 and IFC use the same adapter, registry, interception locations, role tool schemas, MiniMax profile and public/private inputs.

Method claim scope: configured semantic-request recognition plus correct artifact quarantine enforcement. R2 does not claim general semantic confidentiality and does not intercept otherwise unrecognized transformed values. The E3 negative evidence remains valid and unchanged.
