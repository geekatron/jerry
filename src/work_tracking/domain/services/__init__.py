"""
Work Tracking Domain Services.

Domain services encapsulate operations that don't naturally belong to
any entity or value object. They are stateless (or minimal state) and
often coordinate multiple aggregates or perform cross-cutting concerns.

Components:
    - IWorkItemIdGenerator: Protocol for ID generation
    - WorkItemIdGenerator: Snowflake-based ID generator
    - IQualityGateValidator: Protocol for quality gate validation
    - QualityGateValidator: Gate validation logic

References:
    - IMPL-009: Domain Services
    - ADR-007: ID Generation Strategy
    - ADR-008: Quality Gate Layer Configuration
    - Cosmic Python: Domain Services chapter
"""
from __future__ import annotations

from .id_generator import IWorkItemIdGenerator, WorkItemIdGenerator
from .quality_validator import (
    IQualityGateValidator,
    QualityGateValidator,
    ValidationResult,
)

__all__ = [
    # ID Generation
    "IWorkItemIdGenerator",
    "WorkItemIdGenerator",
    # Quality Gate Validation
    "IQualityGateValidator",
    "QualityGateValidator",
    "ValidationResult",
]
