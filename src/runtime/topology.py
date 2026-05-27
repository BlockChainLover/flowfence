"""Deterministic four-agent topology definitions."""

from __future__ import annotations

from dataclasses import dataclass


AGENTS = ("planner_agent", "finance_agent", "doc_writer_agent", "external_vendor_agent")


@dataclass(frozen=True)
class Topology:
    name: str
    edges: dict[str, set[str]]
    blackboard_enabled: bool = False

    def neighbors(self, agent_id: str) -> list[str]:
        return sorted(self.edges.get(agent_id, set()))

    def can_send(self, src_agent_id: str, dst_agent_id: str) -> bool:
        if self.blackboard_enabled and src_agent_id in AGENTS and dst_agent_id in AGENTS:
            return True
        return dst_agent_id in self.edges.get(src_agent_id, set())

    def fanout(self, agent_id: str) -> int:
        if self.blackboard_enabled and agent_id in AGENTS:
            return len(AGENTS) - 1
        return len(self.edges.get(agent_id, set()))

    @property
    def is_blackboard_enabled(self) -> bool:
        return self.blackboard_enabled


def get_topology(name: str) -> Topology:
    if name == "chain_4":
        return Topology(
            name=name,
            edges={
                "planner_agent": {"finance_agent"},
                "finance_agent": {"doc_writer_agent"},
                "doc_writer_agent": {"external_vendor_agent"},
                "external_vendor_agent": set(),
            },
        )
    if name == "star_4":
        return Topology(
            name=name,
            edges={
                "planner_agent": {"finance_agent", "doc_writer_agent", "external_vendor_agent"},
                "finance_agent": {"planner_agent"},
                "doc_writer_agent": {"planner_agent"},
                "external_vendor_agent": {"planner_agent"},
            },
        )
    if name == "blackboard_4":
        return Topology(name=name, edges={agent: set(AGENTS) - {agent} for agent in AGENTS}, blackboard_enabled=True)
    raise ValueError(f"Unsupported topology: {name}")
