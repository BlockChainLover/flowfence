"""Simple workspace artifact store for synthetic MAS traces."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from src.runtime.events import ArtifactRecord, SecretPolicy, redact_preview, sha256_text


WORKSPACE_ZONES = {"shared_doc", "quarantine"}


@dataclass
class WorkspaceStore:
    artifacts: dict[str, ArtifactRecord] = field(default_factory=dict)
    _counter: int = 0

    def write(
        self,
        *,
        zone: str,
        owner_principal: str,
        created_by_event: str,
        content: str,
        secrets: list[SecretPolicy],
        contains_poison: bool,
        metadata: dict[str, Any] | None = None,
    ) -> str:
        if zone not in WORKSPACE_ZONES:
            raise ValueError(f"Unsupported workspace zone: {zone}")
        self._counter += 1
        artifact_id = f"ws_{self._counter:04d}"
        contains_secret = any(secret.raw_value in content for secret in secrets)
        self.artifacts[artifact_id] = ArtifactRecord(
            artifact_id=artifact_id,
            zone=zone,
            owner_principal=owner_principal,
            created_by_event=created_by_event,
            content_hash=sha256_text(content),
            content_preview_redacted=redact_preview(content, secrets),
            contains_secret=contains_secret,
            contains_poison=contains_poison,
            metadata=metadata or {},
        )
        return artifact_id

    def read(self, artifact_id: str) -> ArtifactRecord:
        return self.artifacts[artifact_id]
