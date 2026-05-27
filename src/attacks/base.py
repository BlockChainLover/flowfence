"""Deterministic synthetic attack interface."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class AttackResult:
    text: str
    annotation: dict[str, Any]


class BaseAttack:
    attack_id = "base"

    def apply(self, action_or_text: str, context: dict[str, Any] | None = None) -> AttackResult:
        return AttackResult(text=action_or_text, annotation={"attack_id": self.attack_id, "applied": False})
