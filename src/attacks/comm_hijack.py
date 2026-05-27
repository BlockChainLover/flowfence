"""Communication hijack attack for synthetic MAS propagation."""

from __future__ import annotations

from src.attacks.base import AttackResult, BaseAttack
from src.attacks.summary_poisoning import POISON_INSTRUCTION


class CommHijackAttack(BaseAttack):
    attack_id = "comm_hijack"

    def apply(self, action_or_text: str, context: dict | None = None) -> AttackResult:
        return AttackResult(
            text=f"External vendor request: {POISON_INSTRUCTION}\nOriginal message: {action_or_text}",
            annotation={"attack_id": self.attack_id, "applied": True, "poison_instruction": POISON_INSTRUCTION},
        )
