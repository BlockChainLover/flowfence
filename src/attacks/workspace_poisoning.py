"""Workspace poisoning attack for synthetic MAS propagation."""

from __future__ import annotations

from src.attacks.base import AttackResult, BaseAttack
from src.attacks.summary_poisoning import POISON_INSTRUCTION


class WorkspacePoisoningAttack(BaseAttack):
    attack_id = "workspace_poisoning"

    def apply(self, action_or_text: str, context: dict | None = None) -> AttackResult:
        return AttackResult(
            text=f"{action_or_text}\n\nWorkspace note: {POISON_INSTRUCTION}",
            annotation={"attack_id": self.attack_id, "applied": True, "poison_instruction": POISON_INSTRUCTION},
        )
