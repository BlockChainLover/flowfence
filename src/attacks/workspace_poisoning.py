"""Workspace poisoning attack for synthetic MAS propagation."""

from __future__ import annotations

from src.attacks.base import AttackResult, BaseAttack
from src.attacks.summary_poisoning import DIRECT_POISON_INSTRUCTION, INDIRECT_POISON_INSTRUCTION


class WorkspacePoisoningAttack(BaseAttack):
    def __init__(self, mode: str = "direct") -> None:
        self.mode = mode
        self.attack_id = f"workspace_poisoning_{mode}"

    def apply(self, action_or_text: str, context: dict | None = None) -> AttackResult:
        poison_instruction = DIRECT_POISON_INSTRUCTION if self.mode == "direct" else INDIRECT_POISON_INSTRUCTION
        return AttackResult(
            text=f"{action_or_text}\n\nWorkspace note: {poison_instruction}",
            annotation={
                "attack_id": self.attack_id,
                "attack_family": "workspace_poisoning",
                "attack_mode": self.mode,
                "applied": True,
                "poison_instruction": poison_instruction,
            },
        )
