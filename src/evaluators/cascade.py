"""Cascade metrics for synthetic MAS event traces."""

from __future__ import annotations

from typing import Any


def compute_cascade_metrics(events: list[dict[str, Any]]) -> dict[str, Any]:
    contaminated_ids: set[str] = set()
    depth: dict[str, int] = {}
    first_contaminated_step: int | None = None
    first_containment_step: int | None = None
    for event in events:
        event_id = str(event.get("event_id"))
        parents = [str(parent) for parent in event.get("causal_parents", [])]
        parent_depth = max((depth.get(parent, 0) for parent in parents), default=0)
        metadata = event.get("metadata") if isinstance(event.get("metadata"), dict) else {}
        contaminated = bool(event.get("contains_poison")) or bool(metadata.get("contaminated"))
        if contaminated or any(parent in contaminated_ids for parent in parents):
            contaminated_ids.add(event_id)
            depth[event_id] = parent_depth + 1
            step = int(event.get("step_idx") or 0)
            if first_contaminated_step is None:
                first_contaminated_step = step
        else:
            depth[event_id] = parent_depth
        defense = event.get("defense") if isinstance(event.get("defense"), dict) else {}
        if first_containment_step is None and defense.get("decision") in {"quarantine", "block"}:
            first_containment_step = int(event.get("step_idx") or 0)
    containment_delay = None
    if first_contaminated_step is not None and first_containment_step is not None:
        containment_delay = max(0, first_containment_step - first_contaminated_step)
    return {
        "cascade_size": len(contaminated_ids),
        "cascade_depth": max((depth[event_id] for event_id in contaminated_ids), default=0),
        "containment_delay": containment_delay,
    }
