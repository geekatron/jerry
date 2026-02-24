# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
ValidateAgentsQueryHandler - Validates canonical agent definitions.

References:
    - ADR-PROJ010-003: LLM Portability Architecture
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import TYPE_CHECKING, Any

from src.agents.application.queries.validate_agents_query import ValidateAgentsQuery

if TYPE_CHECKING:
    from src.agents.application.ports.agent_repository import IAgentRepository


@dataclass
class ValidationIssue:
    """A single validation issue.

    Attributes:
        agent_name: Agent with the issue.
        field: Field path with the issue.
        message: Description of the issue.
        severity: 'error' or 'warning'.
    """

    agent_name: str
    field: str
    message: str
    severity: str = "error"


@dataclass
class ValidateAgentsResult:
    """Result of validate agents query.

    Attributes:
        total: Total agents checked.
        passed: Number that passed validation.
        failed: Number that failed.
        issues: List of validation issues.
    """

    total: int = 0
    passed: int = 0
    failed: int = 0
    issues: list[ValidationIssue] = field(default_factory=list)

    @property
    def is_valid(self) -> bool:
        """Check if all agents passed validation."""
        return self.failed == 0


class ValidateAgentsQueryHandler:
    """Handler for ValidateAgentsQuery.

    Validates canonical agent definitions against the JSON Schema
    and checks domain-level constraints.

    Attributes:
        _repository: Repository for reading canonical agents.
        _schema_path: Path to the canonical agent JSON Schema.
    """

    def __init__(
        self,
        repository: IAgentRepository,
        schema_path: Path,
    ) -> None:
        """Initialize with dependencies.

        Args:
            repository: Repository for reading canonical agents.
            schema_path: Path to agent-canonical-v1.schema.json.
        """
        self._repository = repository
        self._schema_path = schema_path

    def handle(self, query: ValidateAgentsQuery) -> ValidateAgentsResult:
        """Handle the ValidateAgentsQuery.

        Args:
            query: Query with optional agent name filter.

        Returns:
            ValidateAgentsResult with validation outcomes.
        """
        if query.agent_name:
            agent = self._repository.get(query.agent_name)
            agents = [agent] if agent else []
        else:
            agents = self._repository.list_all()

        result = ValidateAgentsResult(total=len(agents))

        for agent in agents:
            issues = self._validate_agent(agent)
            if issues:
                result.failed += 1
                result.issues.extend(issues)
            else:
                result.passed += 1

        return result

    def _validate_agent(self, agent: Any) -> list[ValidationIssue]:
        """Validate a single canonical agent.

        Performs domain-level validation checks beyond JSON Schema.

        Args:
            agent: CanonicalAgent entity.

        Returns:
            List of validation issues (empty = passed).
        """
        issues: list[ValidationIssue] = []

        # Check constitutional triplet (H-35)
        principles = agent.constitution.get("principles_applied", [])
        principles_text = " ".join(principles)
        for required in ("P-003", "P-020", "P-022"):
            if required not in principles_text:
                issues.append(
                    ValidationIssue(
                        agent_name=agent.name,
                        field="constitution.principles_applied",
                        message=f"Missing required principle: {required}",
                    )
                )

        forbidden = agent.constitution.get("forbidden_actions", [])
        forbidden_text = " ".join(forbidden)
        for required in ("P-003", "P-020", "P-022"):
            if required not in forbidden_text:
                issues.append(
                    ValidationIssue(
                        agent_name=agent.name,
                        field="constitution.forbidden_actions",
                        message=f"Missing required forbidden action reference: {required}",
                    )
                )

        # Check worker agents don't have agent_delegate (H-35)
        if agent.tool_tier.value != "T5" and "agent_delegate" in agent.native_tools:
            issues.append(
                ValidationIssue(
                    agent_name=agent.name,
                    field="tools.native",
                    message="Non-T5 agent must not have agent_delegate tool (P-003)",
                )
            )

        # Check expertise minimum (PR-003)
        expertise = agent.identity.get("expertise", [])
        if len(expertise) < 2:
            issues.append(
                ValidationIssue(
                    agent_name=agent.name,
                    field="identity.expertise",
                    message=f"Minimum 2 expertise entries required, found {len(expertise)}",
                )
            )

        return issues
