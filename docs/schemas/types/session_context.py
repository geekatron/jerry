"""
Session Context Types for Jerry Framework

Generated from: docs/schemas/session_context.json
Schema Version: 1.0.0
Generated: 2026-01-10

These types define the agent-to-agent handoff contract.
Uses Python 3.11+ features (dataclasses, type hints).
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any


# ============================================================================
# Enums
# ============================================================================


class AgentFamily(str, Enum):
    """Agent family for cross-skill handoff detection."""

    PS = "ps"
    NSE = "nse"
    ORCH = "orch"


class CognitiveMode(str, Enum):
    """Agent's cognitive mode (affects output expectations)."""

    CONVERGENT = "convergent"
    DIVERGENT = "divergent"
    MIXED = "mixed"


class ModelType(str, Enum):
    """LLM model used by the agent."""

    OPUS = "opus"
    SONNET = "sonnet"
    HAIKU = "haiku"
    AUTO = "auto"


class Severity(str, Enum):
    """Severity level for prioritization."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class FindingCategory(str, Enum):
    """Finding category for filtering."""

    INSIGHT = "insight"
    RISK = "risk"
    REQUIREMENT = "requirement"
    DECISION = "decision"
    GAP = "gap"
    RECOMMENDATION = "recommendation"


class ArtifactType(str, Enum):
    """Artifact type for consumer."""

    REQUIREMENT = "requirement"
    RISK = "risk"
    ARCHITECTURE = "architecture"
    VERIFICATION = "verification"
    REVIEW = "review"
    INTEGRATION = "integration"
    CONFIGURATION = "configuration"
    REPORT = "report"
    ANALYSIS = "analysis"
    SYNTHESIS = "synthesis"


class ArtifactFormat(str, Enum):
    """File format."""

    MARKDOWN = "markdown"
    YAML = "yaml"
    JSON = "json"
    TEXT = "text"


# ============================================================================
# Data Classes
# ============================================================================


@dataclass(frozen=True)
class AgentReference:
    """Reference to an agent in the handoff."""

    id: str
    family: AgentFamily
    cognitive_mode: CognitiveMode | None = None
    model: ModelType | None = None

    def __post_init__(self) -> None:
        """Validate agent ID pattern."""
        if not is_valid_agent_id(self.id):
            raise ValueError(f"Invalid agent ID: {self.id}")


@dataclass
class Finding:
    """A key finding from the source agent."""

    id: str
    summary: str
    category: FindingCategory | None = None
    severity: Severity | None = None
    evidence: list[str] = field(default_factory=list)
    traceability: list[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        """Validate finding ID pattern."""
        if not is_valid_finding_id(self.id):
            raise ValueError(f"Invalid finding ID: {self.id}")
        if len(self.summary) > 500:
            raise ValueError("Finding summary exceeds 500 characters")


@dataclass
class Question:
    """An unresolved question for the target agent."""

    id: str
    question: str
    priority: Severity = Severity.MEDIUM
    suggested_approach: str | None = None

    def __post_init__(self) -> None:
        """Validate question ID pattern."""
        if not is_valid_question_id(self.id):
            raise ValueError(f"Invalid question ID: {self.id}")


@dataclass
class Blocker:
    """An issue blocking completion."""

    id: str
    description: str
    severity: Severity
    workaround: str | None = None
    blocked_actions: list[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        """Validate blocker ID pattern."""
        if not is_valid_blocker_id(self.id):
            raise ValueError(f"Invalid blocker ID: {self.id}")


@dataclass
class ConfidenceScore:
    """Confidence score with optional breakdown."""

    overall: float
    reasoning: str | None = None
    breakdown: dict[str, float] = field(default_factory=dict)

    def __post_init__(self) -> None:
        """Validate confidence range."""
        if not 0.0 <= self.overall <= 1.0:
            raise ValueError(f"Confidence must be 0.0-1.0, got {self.overall}")
        for key, value in self.breakdown.items():
            if not 0.0 <= value <= 1.0:
                raise ValueError(f"Breakdown '{key}' must be 0.0-1.0, got {value}")


@dataclass
class ArtifactReference:
    """Reference to an artifact file."""

    path: str
    type: ArtifactType
    format: ArtifactFormat = ArtifactFormat.MARKDOWN
    size_bytes: int | None = None

    def __post_init__(self) -> None:
        """Validate path is repository-relative."""
        if self.path.startswith("/"):
            raise ValueError(f"Path must be repository-relative: {self.path}")


@dataclass
class HandoffPayload:
    """The actual handoff content."""

    key_findings: list[Finding]
    confidence: ConfidenceScore
    open_questions: list[Question] = field(default_factory=list)
    blockers: list[Blocker] = field(default_factory=list)
    artifacts: list[ArtifactReference] = field(default_factory=list)
    context: dict[str, Any] = field(default_factory=dict)
    recommendations: list[str] = field(default_factory=list)


@dataclass
class TraceContext:
    """Distributed tracing context for debugging."""

    trace_id: str | None = None
    span_id: str | None = None
    parent_span_id: str | None = None
    depth: int = 0

    def __post_init__(self) -> None:
        """Validate P-003 compliance."""
        if self.depth > 1:
            raise ValueError(f"P-003 violation: depth {self.depth} > 1")


@dataclass
class SessionContext:
    """Root session context for agent-to-agent handoff."""

    schema_version: str
    session_id: str
    source_agent: AgentReference
    target_agent: AgentReference
    timestamp: str
    payload: HandoffPayload
    workflow_id: str | None = None
    trace: TraceContext | None = None

    def __post_init__(self) -> None:
        """Validate schema version format."""
        if not re.match(r"^\d+\.\d+\.\d+$", self.schema_version):
            raise ValueError(f"Invalid schema version: {self.schema_version}")

    @property
    def is_cross_skill_handoff(self) -> bool:
        """Check if this is a cross-skill handoff."""
        return self.source_agent.family != self.target_agent.family


# ============================================================================
# Validation Functions
# ============================================================================


def is_valid_agent_id(id: str) -> bool:
    """Validate agent ID pattern."""
    return bool(re.match(r"^(ps|nse|orch)-[a-z]+((-[a-z]+)*)$", id))


def is_valid_finding_id(id: str) -> bool:
    """Validate finding ID pattern."""
    return bool(re.match(r"^F-[0-9]{3}$", id))


def is_valid_question_id(id: str) -> bool:
    """Validate question ID pattern."""
    return bool(re.match(r"^Q-[0-9]{3}$", id))


def is_valid_blocker_id(id: str) -> bool:
    """Validate blocker ID pattern."""
    return bool(re.match(r"^BLK-[0-9]{3}$", id))


def is_valid_traceability_ref(ref: str) -> bool:
    """Validate traceability reference pattern."""
    return bool(re.match(r"^(REQ|RISK|TSR|ICD)-[A-Z0-9-]+$", ref))


# ============================================================================
# Factory Functions
# ============================================================================


def create_session_context(
    session_id: str,
    source_agent: AgentReference,
    target_agent: AgentReference,
    payload: HandoffPayload,
    workflow_id: str | None = None,
) -> SessionContext:
    """Create a new SessionContext with current timestamp."""
    return SessionContext(
        schema_version="1.0.0",
        session_id=session_id,
        source_agent=source_agent,
        target_agent=target_agent,
        timestamp=datetime.now(tz=timezone.utc).isoformat().replace("+00:00", "Z"),
        payload=payload,
        workflow_id=workflow_id,
    )


def create_empty_payload() -> HandoffPayload:
    """Create an empty payload with default confidence."""
    return HandoffPayload(
        key_findings=[],
        confidence=ConfidenceScore(
            overall=0.5,
            reasoning="Default confidence - needs validation",
        ),
    )


# ============================================================================
# Serialization (to/from dict)
# ============================================================================


def finding_to_dict(finding: Finding) -> dict[str, Any]:
    """Convert Finding to dictionary."""
    return {
        "id": finding.id,
        "summary": finding.summary,
        "category": finding.category.value if finding.category else None,
        "severity": finding.severity.value if finding.severity else None,
        "evidence": finding.evidence,
        "traceability": finding.traceability,
    }


def agent_ref_to_dict(agent: AgentReference) -> dict[str, Any]:
    """Convert AgentReference to dictionary."""
    return {
        "id": agent.id,
        "family": agent.family.value,
        "cognitive_mode": agent.cognitive_mode.value if agent.cognitive_mode else None,
        "model": agent.model.value if agent.model else None,
    }


def session_context_to_dict(ctx: SessionContext) -> dict[str, Any]:
    """Convert SessionContext to dictionary for JSON serialization."""
    result: dict[str, Any] = {
        "schema_version": ctx.schema_version,
        "session_id": ctx.session_id,
        "source_agent": agent_ref_to_dict(ctx.source_agent),
        "target_agent": agent_ref_to_dict(ctx.target_agent),
        "timestamp": ctx.timestamp,
        "payload": {
            "key_findings": [finding_to_dict(f) for f in ctx.payload.key_findings],
            "open_questions": [
                {
                    "id": q.id,
                    "question": q.question,
                    "priority": q.priority.value,
                    "suggested_approach": q.suggested_approach,
                }
                for q in ctx.payload.open_questions
            ],
            "blockers": [
                {
                    "id": b.id,
                    "description": b.description,
                    "severity": b.severity.value,
                    "workaround": b.workaround,
                    "blocked_actions": b.blocked_actions,
                }
                for b in ctx.payload.blockers
            ],
            "confidence": {
                "overall": ctx.payload.confidence.overall,
                "reasoning": ctx.payload.confidence.reasoning,
                "breakdown": ctx.payload.confidence.breakdown,
            },
            "artifacts": [
                {
                    "path": a.path,
                    "type": a.type.value,
                    "format": a.format.value,
                    "size_bytes": a.size_bytes,
                }
                for a in ctx.payload.artifacts
            ],
            "context": ctx.payload.context,
            "recommendations": ctx.payload.recommendations,
        },
    }

    if ctx.workflow_id:
        result["workflow_id"] = ctx.workflow_id

    if ctx.trace:
        result["trace"] = {
            "trace_id": ctx.trace.trace_id,
            "span_id": ctx.trace.span_id,
            "parent_span_id": ctx.trace.parent_span_id,
            "depth": ctx.trace.depth,
        }

    return result
