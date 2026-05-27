"""Shared event primitives for deterministic FlowFence runtime traces."""

from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any


EVENT_SCHEMA_VERSION = "flowfence_event_v1"
POLICY_SCHEMA_VERSION = "flowfence_policy_decision_v1"


@dataclass(frozen=True)
class AgentRef:
    agent_id: str
    principal: str
    privilege_level: int


@dataclass(frozen=True)
class SecretPolicy:
    secret_id: str
    owner_principal: str
    raw_value: str
    secret_type: str
    allowed_recipients: list[str]
    allowed_abstraction_level: str
    forbidden_channels: list[str]
    required_for_subtasks: list[str] = field(default_factory=list)


@dataclass
class LeaseState:
    scope: str = "default"
    signal: str = "keep"
    active: bool = True


@dataclass(frozen=True)
class RunMetadata:
    run_id: str
    task_id: str
    topology: str
    attack: str
    defense: str
    agent_backend: str
    provider: str
    provider_calls_enabled: bool
    seed: int


@dataclass
class ArtifactRecord:
    artifact_id: str
    zone: str
    owner_principal: str
    created_by_event: str
    content_hash: str
    content_preview_redacted: str
    contains_secret: bool
    contains_poison: bool
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class EventRecord:
    schema_version: str
    event_id: str
    run_id: str
    case_id: str
    task_type: str
    step_idx: int
    event_type: str
    channel: str
    actor_id: str
    object_id: str
    causal_parents: list[str]
    payload_sha256: str | None
    payload_preview_redacted: str | None
    contains_poison: bool
    defense: dict[str, Any]
    exposure: dict[str, Any]
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class PolicyDecisionRecord:
    schema_version: str
    decision_id: str
    event_id: str
    run_id: str
    case_id: str
    task_type: str
    step_idx: int
    defense_mode: str
    decision: str
    risk_score: float
    reason_codes: list[str]
    lease_signal: str
    actions: list[str]
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def make_event_id(index: int) -> str:
    return f"evt_{index:06d}"


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def redact_preview(text: str, secrets: list[SecretPolicy], max_chars: int = 240) -> str:
    redacted = text
    for secret in secrets:
        redacted = redacted.replace(secret.raw_value, f"[SECRET:{secret.secret_id}]")
    return redacted.replace("\r", " ").replace("\n", "\\n")[:max_chars]


def write_jsonl(path: str | Path, records: list[Any]) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        for record in records:
            if hasattr(record, "to_dict"):
                payload = record.to_dict()
            elif hasattr(record, "__dataclass_fields__"):
                payload = asdict(record)
            else:
                payload = record
            handle.write(json.dumps(payload, ensure_ascii=False, sort_keys=True) + "\n")


def read_jsonl(path: str | Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with Path(path).open("r", encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def empty_defense() -> dict[str, Any]:
    return {
        "decision": "allow",
        "risk_score": 0.0,
        "reason_codes": [],
        "lease_signal": "keep",
        "defense_fired": False,
        "rewritten_content_sha256": None,
        "rewritten_content_preview_redacted": None,
        "hard_blocker": False,
    }


def empty_exposure() -> dict[str, Any]:
    return {
        "poisoned_content_detected": False,
        "poisoned_content_exposed": False,
        "raw_poisoned_retrieval": False,
        "attack_manifested": False,
        "safe_trace_redacted": False,
    }
