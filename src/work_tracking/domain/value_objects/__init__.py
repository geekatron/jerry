"""
Work Tracking Value Objects.

Immutable objects defined by their attributes, not identity.

Components:
    - WorkItemId: Hybrid identity (Snowflake + display ID)
    - TestCoverage: Test coverage percentage
    - TestRatio: Test type distribution (positive/negative/edge)
    - WorkItemStatus: Work item lifecycle state machine
    - QualityLevel: Quality gate levels (L0/L1/L2)
    - Priority: Work item priority (CRITICAL/HIGH/MEDIUM/LOW)
    - WorkType: Work item type classification

References:
    - PAT-005-e006: Quality Gate Value Objects
    - PAT-004-e006: Status State Machine
    - impl-es-e-006-workitem-schema: Priority and WorkType specifications
"""
from __future__ import annotations

from .priority import Priority
from .test_coverage import TestCoverage
from .test_ratio import QualityLevel, TestRatio
from .work_item_id import WorkItemId
from .work_item_status import InvalidStateTransitionError, WorkItemStatus
from .work_type import WorkType

__all__ = [
    # Identity
    "WorkItemId",
    # Classification
    "Priority",
    "WorkType",
    # Quality
    "TestCoverage",
    "TestRatio",
    "QualityLevel",
    # Status
    "WorkItemStatus",
    "InvalidStateTransitionError",
]
