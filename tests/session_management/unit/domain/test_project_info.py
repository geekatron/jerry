"""Unit tests for ProjectInfo entity.

Test Categories:
    - Protocol Compliance: IAuditable and IVersioned (not EntityBase - see DISC-002)
    - Entity Properties: Status, has_plan, has_tracker, path
    - Factory Methods: create() with flexible input types
    - Audit Metadata: IAuditable compliance
    - Version Tracking: IVersioned compliance
    - Immutability: Frozen dataclass behavior

References:
    - ENFORCE-008d: Domain Refactoring
    - DISC-002: ProjectInfo EntityBase Design Tension
    - Canon PAT-007: EntityBase Class (NOT extended - see DISC-002)
    - ADR-013: Shared Kernel Module

Note: ProjectInfo does NOT extend EntityBase because it is an immutable snapshot
(frozen=True) while EntityBase is designed for mutable entities. ProjectInfo
implements IAuditable and IVersioned protocols directly via property accessors.
"""

from __future__ import annotations

from datetime import UTC, datetime

import pytest

from src.session_management.domain.entities.project_info import ProjectInfo
from src.session_management.domain.value_objects.project_id import ProjectId
from src.session_management.domain.value_objects.project_status import ProjectStatus
from src.shared_kernel.auditable import IAuditable
from src.shared_kernel.versioned import IVersioned

# =============================================================================
# Protocol Compliance Tests (I-008d.2.1) - REVISED per DISC-002
# =============================================================================


class TestProjectInfoProtocolCompliance:
    """Tests for protocol compliance (IAuditable, IVersioned).

    Note: ProjectInfo does NOT extend EntityBase (see DISC-002).
    It remains frozen/immutable but implements the protocols directly.
    """

    def test_project_info_is_frozen_dataclass(self) -> None:
        """ProjectInfo should be immutable (frozen dataclass)."""
        project_id = ProjectId.parse("PROJ-001-test")
        project_info = ProjectInfo.create(project_id)
        with pytest.raises(Exception):  # FrozenInstanceError
            project_info.status = ProjectStatus.COMPLETED

    def test_project_info_has_id_property(self) -> None:
        """ProjectInfo should have id property."""
        project_id = ProjectId.parse("PROJ-001-test")
        project_info = ProjectInfo.create(project_id)
        assert hasattr(project_info, "id")
        assert project_info.id == project_id

    def test_project_info_implements_iauditable(self) -> None:
        """ProjectInfo should implement IAuditable protocol."""
        project_id = ProjectId.parse("PROJ-001-test")
        project_info = ProjectInfo.create(project_id)
        assert isinstance(project_info, IAuditable)

    def test_project_info_implements_iversioned(self) -> None:
        """ProjectInfo should implement IVersioned protocol."""
        project_id = ProjectId.parse("PROJ-001-test")
        project_info = ProjectInfo.create(project_id)
        assert isinstance(project_info, IVersioned)

    def test_project_info_has_version_property(self) -> None:
        """ProjectInfo should have version property."""
        project_id = ProjectId.parse("PROJ-001-test")
        project_info = ProjectInfo.create(project_id)
        assert hasattr(project_info, "version")
        assert project_info.version >= 0


# =============================================================================
# Audit Metadata Tests (I-008d.2.2)
# =============================================================================


class TestProjectInfoAuditMetadata:
    """Tests for audit metadata (IAuditable compliance)."""

    def test_has_created_by_property(self) -> None:
        """ProjectInfo should have created_by property."""
        project_id = ProjectId.parse("PROJ-001-test")
        project_info = ProjectInfo.create(project_id, created_by="Claude")
        assert hasattr(project_info, "created_by")
        assert project_info.created_by == "Claude"

    def test_has_created_at_property(self) -> None:
        """ProjectInfo should have created_at property."""
        before = datetime.now(UTC)
        project_id = ProjectId.parse("PROJ-001-test")
        project_info = ProjectInfo.create(project_id)
        after = datetime.now(UTC)

        assert hasattr(project_info, "created_at")
        assert before <= project_info.created_at <= after

    def test_has_updated_by_property(self) -> None:
        """ProjectInfo should have updated_by property."""
        project_id = ProjectId.parse("PROJ-001-test")
        project_info = ProjectInfo.create(project_id, created_by="Claude")
        assert hasattr(project_info, "updated_by")
        # Initially should match created_by
        assert project_info.updated_by == "Claude"

    def test_has_updated_at_property(self) -> None:
        """ProjectInfo should have updated_at property."""
        project_id = ProjectId.parse("PROJ-001-test")
        project_info = ProjectInfo.create(project_id)
        assert hasattr(project_info, "updated_at")
        # Initially should equal created_at
        assert project_info.updated_at >= project_info.created_at

    def test_default_created_by_is_system(self) -> None:
        """Default created_by should be 'System'."""
        project_id = ProjectId.parse("PROJ-001-test")
        project_info = ProjectInfo.create(project_id)
        assert project_info.created_by == "System"


# =============================================================================
# Entity Properties Tests
# =============================================================================


class TestProjectInfoProperties:
    """Tests for entity properties."""

    def test_status_property(self) -> None:
        """ProjectInfo should have status property."""
        project_id = ProjectId.parse("PROJ-001-test")
        project_info = ProjectInfo.create(project_id, status=ProjectStatus.IN_PROGRESS)
        assert project_info.status == ProjectStatus.IN_PROGRESS

    def test_default_status_is_unknown(self) -> None:
        """Default status should be UNKNOWN."""
        project_id = ProjectId.parse("PROJ-001-test")
        project_info = ProjectInfo.create(project_id)
        assert project_info.status == ProjectStatus.UNKNOWN

    def test_has_plan_property(self) -> None:
        """ProjectInfo should have has_plan property."""
        project_id = ProjectId.parse("PROJ-001-test")
        project_info = ProjectInfo.create(project_id, has_plan=True)
        assert project_info.has_plan is True

    def test_default_has_plan_is_false(self) -> None:
        """Default has_plan should be False."""
        project_id = ProjectId.parse("PROJ-001-test")
        project_info = ProjectInfo.create(project_id)
        assert project_info.has_plan is False

    def test_has_tracker_property(self) -> None:
        """ProjectInfo should have has_tracker property."""
        project_id = ProjectId.parse("PROJ-001-test")
        project_info = ProjectInfo.create(project_id, has_tracker=True)
        assert project_info.has_tracker is True

    def test_default_has_tracker_is_false(self) -> None:
        """Default has_tracker should be False."""
        project_id = ProjectId.parse("PROJ-001-test")
        project_info = ProjectInfo.create(project_id)
        assert project_info.has_tracker is False

    def test_path_property(self) -> None:
        """ProjectInfo should have path property."""
        project_id = ProjectId.parse("PROJ-001-test")
        project_info = ProjectInfo.create(project_id, path="/some/path")
        assert project_info.path == "/some/path"

    def test_default_path_is_none(self) -> None:
        """Default path should be None."""
        project_id = ProjectId.parse("PROJ-001-test")
        project_info = ProjectInfo.create(project_id)
        assert project_info.path is None


# =============================================================================
# Factory Method Tests
# =============================================================================


class TestProjectInfoFactoryMethods:
    """Tests for factory methods."""

    def test_create_with_project_id_instance(self) -> None:
        """create() should accept ProjectId instance."""
        project_id = ProjectId.parse("PROJ-001-test")
        project_info = ProjectInfo.create(project_id)
        assert project_info.id == project_id

    def test_create_with_project_id_string(self) -> None:
        """create() should accept project ID string."""
        project_info = ProjectInfo.create("PROJ-001-test")
        assert project_info.id.value == "PROJ-001-test"

    def test_create_with_status_enum(self) -> None:
        """create() should accept ProjectStatus enum."""
        project_id = ProjectId.parse("PROJ-001-test")
        project_info = ProjectInfo.create(project_id, status=ProjectStatus.COMPLETED)
        assert project_info.status == ProjectStatus.COMPLETED

    def test_create_with_status_string(self) -> None:
        """create() should accept status string."""
        project_id = ProjectId.parse("PROJ-001-test")
        project_info = ProjectInfo.create(project_id, status="in_progress")
        assert project_info.status == ProjectStatus.IN_PROGRESS

    def test_create_with_all_parameters(self) -> None:
        """create() should accept all parameters."""
        project_id = ProjectId.parse("PROJ-001-test")
        project_info = ProjectInfo.create(
            project_id,
            status=ProjectStatus.IN_PROGRESS,
            has_plan=True,
            has_tracker=True,
            path="/projects/test",
            created_by="Claude",
        )
        assert project_info.id == project_id
        assert project_info.status == ProjectStatus.IN_PROGRESS
        assert project_info.has_plan is True
        assert project_info.has_tracker is True
        assert project_info.path == "/projects/test"
        assert project_info.created_by == "Claude"


# =============================================================================
# Computed Properties Tests
# =============================================================================


class TestProjectInfoComputedProperties:
    """Tests for computed properties."""

    def test_is_complete_true_when_both_files_exist(self) -> None:
        """is_complete should be True when both plan and tracker exist."""
        project_id = ProjectId.parse("PROJ-001-test")
        project_info = ProjectInfo.create(project_id, has_plan=True, has_tracker=True)
        assert project_info.is_complete is True

    def test_is_complete_false_when_missing_plan(self) -> None:
        """is_complete should be False when plan missing."""
        project_id = ProjectId.parse("PROJ-001-test")
        project_info = ProjectInfo.create(project_id, has_plan=False, has_tracker=True)
        assert project_info.is_complete is False

    def test_is_complete_false_when_missing_tracker(self) -> None:
        """is_complete should be False when tracker missing."""
        project_id = ProjectId.parse("PROJ-001-test")
        project_info = ProjectInfo.create(project_id, has_plan=True, has_tracker=False)
        assert project_info.is_complete is False

    def test_is_active_true_for_in_progress(self) -> None:
        """is_active should be True for IN_PROGRESS status."""
        project_id = ProjectId.parse("PROJ-001-test")
        project_info = ProjectInfo.create(project_id, status=ProjectStatus.IN_PROGRESS)
        assert project_info.is_active is True

    def test_is_active_false_for_archived(self) -> None:
        """is_active should be False for ARCHIVED status."""
        project_id = ProjectId.parse("PROJ-001-test")
        project_info = ProjectInfo.create(project_id, status=ProjectStatus.ARCHIVED)
        assert project_info.is_active is False

    def test_is_active_false_for_completed(self) -> None:
        """is_active should be False for COMPLETED status."""
        project_id = ProjectId.parse("PROJ-001-test")
        project_info = ProjectInfo.create(project_id, status=ProjectStatus.COMPLETED)
        assert project_info.is_active is False

    def test_warnings_includes_missing_plan(self) -> None:
        """warnings should include missing plan message."""
        project_id = ProjectId.parse("PROJ-001-test")
        project_info = ProjectInfo.create(project_id, has_plan=False)
        assert "Missing PLAN.md" in project_info.warnings

    def test_warnings_includes_missing_tracker(self) -> None:
        """warnings should include missing tracker message."""
        project_id = ProjectId.parse("PROJ-001-test")
        project_info = ProjectInfo.create(project_id, has_tracker=False)
        assert "Missing WORKTRACKER.md" in project_info.warnings

    def test_warnings_empty_when_complete(self) -> None:
        """warnings should be empty when complete."""
        project_id = ProjectId.parse("PROJ-001-test")
        project_info = ProjectInfo.create(project_id, has_plan=True, has_tracker=True)
        assert project_info.warnings == []


# =============================================================================
# String Representation Tests
# =============================================================================


class TestProjectInfoStringRepresentation:
    """Tests for string representation."""

    def test_str_includes_id(self) -> None:
        """__str__ should include project ID."""
        project_id = ProjectId.parse("PROJ-001-test")
        project_info = ProjectInfo.create(project_id)
        assert "PROJ-001-test" in str(project_info)

    def test_str_includes_status(self) -> None:
        """__str__ should include status."""
        project_id = ProjectId.parse("PROJ-001-test")
        project_info = ProjectInfo.create(project_id, status=ProjectStatus.IN_PROGRESS)
        assert "In Progress" in str(project_info)

    def test_repr_includes_details(self) -> None:
        """__repr__ should include detailed representation."""
        project_id = ProjectId.parse("PROJ-001-test")
        project_info = ProjectInfo.create(project_id)
        repr_str = repr(project_info)
        assert "ProjectInfo" in repr_str
        assert "PROJ-001-test" in repr_str


# =============================================================================
# Session ID Reference Tests (I-008d.3.3)
# =============================================================================


class TestProjectInfoSessionIdReference:
    """Tests for session_id reference on ProjectInfo.

    This links ProjectInfo to the active Session working on it.
    """

    def test_has_session_id_property(self) -> None:
        """ProjectInfo should have session_id property."""
        project_id = ProjectId.parse("PROJ-001-test")
        project_info = ProjectInfo.create(project_id)
        assert hasattr(project_info, "session_id")

    def test_session_id_defaults_to_none(self) -> None:
        """session_id should default to None."""
        project_id = ProjectId.parse("PROJ-001-test")
        project_info = ProjectInfo.create(project_id)
        assert project_info.session_id is None

    def test_create_with_session_id(self) -> None:
        """create() should accept optional session_id."""
        from src.session_management.domain.value_objects.session_id import SessionId

        project_id = ProjectId.parse("PROJ-001-test")
        session_id = SessionId.generate()
        project_info = ProjectInfo.create(project_id, session_id=session_id)
        assert project_info.session_id == session_id.value

    def test_create_with_session_id_string(self) -> None:
        """create() should accept session_id as string."""
        project_id = ProjectId.parse("PROJ-001-test")
        project_info = ProjectInfo.create(project_id, session_id="SESS-a1b2c3d4")
        assert project_info.session_id == "SESS-a1b2c3d4"

    def test_session_id_is_immutable(self) -> None:
        """session_id should be immutable on frozen dataclass."""
        from src.session_management.domain.value_objects.session_id import SessionId

        project_id = ProjectId.parse("PROJ-001-test")
        session_id = SessionId.generate()
        project_info = ProjectInfo.create(project_id, session_id=session_id)
        with pytest.raises(Exception):  # FrozenInstanceError
            project_info.session_id = "different"

    def test_session_id_in_repr(self) -> None:
        """session_id should appear in repr when set."""
        from src.session_management.domain.value_objects.session_id import SessionId

        project_id = ProjectId.parse("PROJ-001-test")
        session_id = SessionId.generate()
        project_info = ProjectInfo.create(project_id, session_id=session_id)
        repr_str = repr(project_info)
        assert "session_id=" in repr_str or session_id.value in repr_str
