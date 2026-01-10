"""
Work Tracking Value Objects.

Immutable objects defined by their attributes, not identity.

Components:
    - WorkItemId: Hybrid identity (Snowflake + display ID)
    - TestCoverage: Test coverage percentage
    - TestRatio: Test type distribution (positive/negative/edge)
    - WorkItemStatus: Work item lifecycle state machine
    - QualityLevel: Quality gate levels (L0/L1/L2)

References:
    - PAT-005-e006: Quality Gate Value Objects
    - PAT-004-e006: Status State Machine
"""
from __future__ import annotations

from .test_coverage import TestCoverage
from .test_ratio import QualityLevel, TestRatio
from .work_item_id import WorkItemId
from .work_item_status import InvalidStateTransitionError, WorkItemStatus

__all__ = [
    # Identity
    "WorkItemId",
    # Quality
    "TestCoverage",
    "TestRatio",
    "QualityLevel",
    # Status
    "WorkItemStatus",
    "InvalidStateTransitionError",
]
