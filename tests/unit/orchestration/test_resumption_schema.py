# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
Unit tests for the ORCHESTRATION.yaml v2.0 resumption schema.

Tests cover:
  - All 7 sub-sections present and valid (BDD scenario 1)
  - Backward compatibility with existing 5 fields (BDD scenario 2)
  - ISO 8601 timestamp format for updated_at (BDD scenario 3)
  - Schema validation against JSON schema

Test naming follows BDD convention:
    test_{scenario}_when_{condition}_then_{expected}

References:
    - ST-001: Enhanced Resumption Schema + Update Protocol
    - SPIKE-001 Phase 4: Resumption Completeness Assessment
"""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path

import jsonschema
import pytest
import yaml

from tests.unit.orchestration.resumption_schema import (
    ORIGINAL_V1_FIELDS,
    RESUMPTION_SCHEMA,
)


# =============================================================================
# Test Fixtures
# =============================================================================

@pytest.fixture
def valid_resumption_v2() -> dict:
    """A complete, valid v2.0 resumption section with all 7 sub-sections."""
    return {
        "recovery_state": {
            "last_checkpoint": "CP-002",
            "current_phase": 3,
            "current_phase_name": "Source File SPDX Header Notices",
            "workflow_status": "ACTIVE",
            "current_activity": "phase-3-agent-execution",
            "next_step": "Execute header-applicator agent for EN-932",
            "context_fill_at_update": 0.642,
            "updated_at": "2026-02-17T12:34:56Z",
            "cross_session_portable": True,
            "ephemeral_references": False,
        },
        "files_to_read": [
            {
                "path": "projects/PROJ-001-oss-release/ORCHESTRATION.yaml",
                "priority": 1,
                "purpose": "Machine-readable workflow state. Read resumption section first.",
                "sections": ["resumption", "quality_gates", "next_actions"],
            },
            {
                "path": "projects/PROJ-001-oss-release/ORCHESTRATION_PLAN.md",
                "priority": 2,
                "purpose": "Strategic context. Agent definitions, phase descriptions.",
                "sections": ["agent-registry", "phase-3"],
            },
            {
                "path": "projects/PROJ-001-oss-release/WORKTRACKER.md",
                "priority": 3,
                "purpose": "Tactical documentation. Feature status, blockers.",
            },
        ],
        "quality_trajectory": {
            "gates_completed": ["qg-1", "qg-2"],
            "gates_remaining": ["qg-3", "qg-final"],
            "current_gate": None,
            "current_gate_iteration": None,
            "score_history": {
                "qg-1": [0.825, 0.916, 0.941],
                "qg-2": [0.960, 0.951],
            },
            "lowest_dimension": "evidence_quality",
            "total_iterations_used": 5,
        },
        "defect_summary": {
            "total_defects_found": 14,
            "total_defects_resolved": 14,
            "unresolved_defects": [],
            "recurring_patterns": [
                {
                    "pattern": "Evidence quality gaps (missing URLs, unattached artifacts)",
                    "gates_affected": ["qg-1", "qg-2"],
                    "resolution": "Added source URLs and attached raw data artifacts",
                },
            ],
            "last_gate_primary_defect": None,
        },
        "decision_log": [
            {
                "id": "RD-001",
                "gate": "qg-2",
                "iteration": 1,
                "decision": "Align copyright holder to 'Adam Nowak' across NOTICE, header_template",
                "rationale": "DA-001 found inconsistency. NOTICE is authoritative source.",
                "affects_phases": [3],
                "applied": True,
            },
        ],
        "agent_summaries": {
            "audit-executor": "PASS. All 25 deps Apache-2.0 compatible.",
            "license-replacer": "DONE. LICENSE file replaced with canonical Apache 2.0 text.",
        },
        "compaction_events": {
            "count": 0,
            "events": [],
        },
    }


@pytest.fixture
def valid_resumption_v1() -> dict:
    """A valid v1.0 resumption section (original 5 fields)."""
    return {
        "last_checkpoint": "CP-003",
        "current_state": (
            "WORKFLOW COMPLETE. All 4 phases done. "
            "QG-1: 0.941, QG-2: 0.9505, QG-3: 0.935."
        ),
        "next_step": "Close FEAT-015 feature entity.",
        "files_to_read": [
            "ORCHESTRATION_PLAN.md",
            "ORCHESTRATION.yaml",
            "WORKTRACKER.md",
        ],
        "cross_session_portable": True,
        "ephemeral_references": False,
    }


@pytest.fixture
def minimal_resumption_v2() -> dict:
    """A minimal valid v2.0 resumption section (required fields only, initial state)."""
    return {
        "recovery_state": {
            "last_checkpoint": None,
            "current_phase": 0,
            "current_phase_name": "Not started",
            "workflow_status": "ACTIVE",
            "current_activity": "idle",
            "next_step": "Execute Phase 1 agents",
            "context_fill_at_update": None,
            "updated_at": "2026-02-20T00:00:00Z",
        },
        "files_to_read": [
            {
                "path": "ORCHESTRATION.yaml",
                "priority": 1,
                "purpose": "Machine-readable workflow state",
            },
        ],
        "quality_trajectory": {
            "gates_completed": [],
            "gates_remaining": ["qg-1"],
            "current_gate": None,
            "current_gate_iteration": None,
            "score_history": {},
            "lowest_dimension": None,
            "total_iterations_used": 0,
        },
        "defect_summary": {
            "total_defects_found": 0,
            "total_defects_resolved": 0,
            "unresolved_defects": [],
            "recurring_patterns": [],
            "last_gate_primary_defect": None,
        },
        "decision_log": [],
        "agent_summaries": {},
        "compaction_events": {
            "count": 0,
            "events": [],
        },
    }


# =============================================================================
# BDD Scenario 1: Template contains all 7 resumption sub-sections
# =============================================================================

class TestTemplateContainsAll7SubSections:
    """Feature: ORCHESTRATION.yaml v2.0 resumption schema

    Scenario: Template contains all 7 resumption sub-sections
    """

    EXPECTED_SUB_SECTIONS = [
        "recovery_state",
        "files_to_read",
        "quality_trajectory",
        "defect_summary",
        "decision_log",
        "agent_summaries",
        "compaction_events",
    ]

    def test_schema_requires_all_7_sub_sections(self) -> None:
        """Given the resumption schema, all 7 sub-sections should be required."""
        assert RESUMPTION_SCHEMA["required"] == self.EXPECTED_SUB_SECTIONS

    def test_valid_v2_validates_when_all_sub_sections_present(
        self, valid_resumption_v2: dict
    ) -> None:
        """Given a valid v2.0 resumption section, it should validate without errors."""
        jsonschema.validate(instance=valid_resumption_v2, schema=RESUMPTION_SCHEMA)

    def test_minimal_v2_validates_when_required_fields_only(
        self, minimal_resumption_v2: dict
    ) -> None:
        """Given a minimal v2.0 resumption section, it should validate without errors."""
        jsonschema.validate(instance=minimal_resumption_v2, schema=RESUMPTION_SCHEMA)

    @pytest.mark.parametrize("missing_section", EXPECTED_SUB_SECTIONS)
    def test_validation_fails_when_sub_section_missing(
        self, valid_resumption_v2: dict, missing_section: str
    ) -> None:
        """Given a resumption section missing a sub-section, validation should fail."""
        incomplete = deepcopy(valid_resumption_v2)
        del incomplete[missing_section]
        with pytest.raises(jsonschema.ValidationError, match=missing_section):
            jsonschema.validate(instance=incomplete, schema=RESUMPTION_SCHEMA)

    def test_template_file_contains_all_sub_sections(self) -> None:
        """Given the ORCHESTRATION.template.yaml file,
        when I parse the resumption section,
        then it should contain all 7 sub-sections.
        """
        template_path = Path(
            "skills/orchestration/templates/ORCHESTRATION.template.yaml"
        )
        # Use project root for path resolution
        project_root = Path(__file__).resolve().parents[3]
        full_path = project_root / template_path

        assert full_path.exists(), f"Template not found at {full_path}"

        with open(full_path) as f:
            template = yaml.safe_load(f)

        assert "resumption" in template, "Template missing 'resumption' top-level key"
        resumption = template["resumption"]

        for section in self.EXPECTED_SUB_SECTIONS:
            assert section in resumption, (
                f"Template resumption section missing sub-section: {section}"
            )

    def test_template_field_names_match_schema(self) -> None:
        """Given the ORCHESTRATION.template.yaml file,
        when I compare its resumption field names to the JSON schema,
        then all required field names should match the schema definition
        and no unexpected fields should be present.
        """
        template_path = Path(
            "skills/orchestration/templates/ORCHESTRATION.template.yaml"
        )
        project_root = Path(__file__).resolve().parents[3]
        full_path = project_root / template_path

        with open(full_path) as f:
            template = yaml.safe_load(f)

        resumption = template["resumption"]
        schema_props = RESUMPTION_SCHEMA["properties"]

        for section_name, section_schema in schema_props.items():
            if section_schema.get("type") != "object":
                continue
            if "properties" not in section_schema:
                continue

            section_data = resumption.get(section_name)
            if not isinstance(section_data, dict):
                continue

            expected_keys = set(section_schema["properties"].keys())
            actual_keys = set(section_data.keys())

            # All required keys must be present in the template
            required = set(section_schema.get("required", []))
            missing_required = required - actual_keys
            assert not missing_required, (
                f"Template resumption.{section_name} missing required keys: "
                f"{missing_required}"
            )

            # No unexpected keys (additionalProperties: false)
            if section_schema.get("additionalProperties") is False:
                extra_keys = actual_keys - expected_keys
                assert not extra_keys, (
                    f"Template resumption.{section_name} has unexpected keys: "
                    f"{extra_keys}. Schema does not allow additional properties."
                )


# =============================================================================
# BDD Scenario 2: Backward compatible with existing 5 fields
# =============================================================================

class TestBackwardCompatibility:
    """Feature: ORCHESTRATION.yaml v2.0 resumption schema

    Scenario: Backward compatible with existing 5 fields
    """

    def test_original_fields_preserved_in_v2_schema(self) -> None:
        """Given an ORCHESTRATION.yaml with old 5-field resumption section,
        when the v2.0 schema is applied,
        then the 5 original fields should be preserved within recovery_state.
        """
        v2_recovery_props = RESUMPTION_SCHEMA["properties"]["recovery_state"]["properties"]
        v2_top_level_props = RESUMPTION_SCHEMA["properties"]

        # last_checkpoint -> recovery_state.last_checkpoint
        assert "last_checkpoint" in v2_recovery_props

        # current_state -> decomposed into structured fields
        # (current_phase, workflow_status, current_activity replace the prose string)
        assert "current_phase" in v2_recovery_props
        assert "workflow_status" in v2_recovery_props
        assert "current_activity" in v2_recovery_props

        # next_step -> recovery_state.next_step
        assert "next_step" in v2_recovery_props

        # files_to_read -> top-level files_to_read (now structured)
        assert "files_to_read" in v2_top_level_props

        # cross_session_portable -> recovery_state.cross_session_portable
        assert "cross_session_portable" in v2_recovery_props

    def test_files_to_read_accepts_simple_string_paths(self) -> None:
        """Given v1.0 files_to_read with simple string paths,
        the v2.0 schema should accept them for backward compatibility.
        """
        data = {
            "recovery_state": {
                "last_checkpoint": None,
                "current_phase": 0,
                "current_phase_name": "Not started",
                "workflow_status": "ACTIVE",
                "current_activity": "idle",
                "next_step": "Begin",
                "context_fill_at_update": None,
                "updated_at": "2026-02-20T00:00:00Z",
            },
            "files_to_read": [
                "ORCHESTRATION_PLAN.md",
                "ORCHESTRATION.yaml",
                "WORKTRACKER.md",
            ],
            "quality_trajectory": {
                "gates_completed": [],
                "gates_remaining": [],
                "current_gate": None,
                "current_gate_iteration": None,
                "score_history": {},
                "lowest_dimension": None,
                "total_iterations_used": 0,
            },
            "defect_summary": {
                "total_defects_found": 0,
                "total_defects_resolved": 0,
                "unresolved_defects": [],
                "recurring_patterns": [],
                "last_gate_primary_defect": None,
            },
            "decision_log": [],
            "agent_summaries": {},
            "compaction_events": {"count": 0, "events": []},
        }
        # Should not raise
        jsonschema.validate(instance=data, schema=RESUMPTION_SCHEMA)

    def test_files_to_read_accepts_mixed_format(self) -> None:
        """Given files_to_read with a mix of simple strings and structured objects,
        the v2.0 schema should accept both formats.
        """
        data = {
            "recovery_state": {
                "last_checkpoint": None,
                "current_phase": 0,
                "current_phase_name": "Not started",
                "workflow_status": "ACTIVE",
                "current_activity": "idle",
                "next_step": "Begin",
                "context_fill_at_update": None,
                "updated_at": "2026-02-20T00:00:00Z",
            },
            "files_to_read": [
                {
                    "path": "ORCHESTRATION.yaml",
                    "priority": 1,
                    "purpose": "Workflow state",
                },
                "WORKTRACKER.md",
            ],
            "quality_trajectory": {
                "gates_completed": [],
                "gates_remaining": [],
                "current_gate": None,
                "current_gate_iteration": None,
                "score_history": {},
                "lowest_dimension": None,
                "total_iterations_used": 0,
            },
            "defect_summary": {
                "total_defects_found": 0,
                "total_defects_resolved": 0,
                "unresolved_defects": [],
                "recurring_patterns": [],
                "last_gate_primary_defect": None,
            },
            "decision_log": [],
            "agent_summaries": {},
            "compaction_events": {"count": 0, "events": []},
        }
        jsonschema.validate(instance=data, schema=RESUMPTION_SCHEMA)

    def test_v1_field_mapping_is_documented(self) -> None:
        """The original 5 v1.0 fields should be listed in the backward compat mapping."""
        assert len(ORIGINAL_V1_FIELDS) == 5
        assert "last_checkpoint" in ORIGINAL_V1_FIELDS
        assert "current_state" in ORIGINAL_V1_FIELDS
        assert "next_step" in ORIGINAL_V1_FIELDS
        assert "files_to_read" in ORIGINAL_V1_FIELDS
        assert "cross_session_portable" in ORIGINAL_V1_FIELDS


# =============================================================================
# BDD Scenario 3: updated_at timestamp present in ISO 8601 format
# =============================================================================

class TestUpdatedAtTimestamp:
    """Feature: ORCHESTRATION.yaml v2.0 resumption schema

    Scenario: updated_at timestamp present
    """

    def test_updated_at_required_in_recovery_state(self) -> None:
        """Given an ORCHESTRATION.yaml with v2.0 resumption section,
        the resumption section should contain an updated_at field.
        """
        required = RESUMPTION_SCHEMA["properties"]["recovery_state"]["required"]
        assert "updated_at" in required

    @pytest.mark.parametrize(
        "valid_timestamp",
        [
            "2026-02-17T12:34:56Z",
            "2026-02-20T00:00:00Z",
            "2026-01-10T09:30:15+00:00",
            "2026-06-15T23:59:59-05:00",
        ],
    )
    def test_valid_iso8601_timestamps_accepted(
        self, minimal_resumption_v2: dict, valid_timestamp: str
    ) -> None:
        """Given a valid ISO 8601 timestamp, validation should pass."""
        data = deepcopy(minimal_resumption_v2)
        data["recovery_state"]["updated_at"] = valid_timestamp
        jsonschema.validate(instance=data, schema=RESUMPTION_SCHEMA)

    @pytest.mark.parametrize(
        "invalid_timestamp",
        [
            "2026-02-17",
            "2026-02-17 12:34:56",
            "17/02/2026T12:34:56Z",
            "not-a-timestamp",
            "",
            "2026-02-17T12:34:56",  # Missing timezone
        ],
    )
    def test_invalid_timestamps_rejected(
        self, minimal_resumption_v2: dict, invalid_timestamp: str
    ) -> None:
        """Given an invalid timestamp format, validation should fail."""
        data = deepcopy(minimal_resumption_v2)
        data["recovery_state"]["updated_at"] = invalid_timestamp
        with pytest.raises(jsonschema.ValidationError):
            jsonschema.validate(instance=data, schema=RESUMPTION_SCHEMA)


# =============================================================================
# Additional Schema Validation Tests
# =============================================================================

class TestRecoveryStateValidation:
    """Tests for the recovery_state sub-section constraints."""

    def test_workflow_status_enum_enforced(
        self, minimal_resumption_v2: dict
    ) -> None:
        """Given an invalid workflow_status value, validation should fail."""
        data = deepcopy(minimal_resumption_v2)
        data["recovery_state"]["workflow_status"] = "INVALID_STATUS"
        with pytest.raises(jsonschema.ValidationError):
            jsonschema.validate(instance=data, schema=RESUMPTION_SCHEMA)

    def test_context_fill_range_enforced(
        self, minimal_resumption_v2: dict
    ) -> None:
        """Given context_fill_at_update > 1.0, validation should fail."""
        data = deepcopy(minimal_resumption_v2)
        data["recovery_state"]["context_fill_at_update"] = 1.5
        with pytest.raises(jsonschema.ValidationError):
            jsonschema.validate(instance=data, schema=RESUMPTION_SCHEMA)

    def test_current_phase_negative_rejected(
        self, minimal_resumption_v2: dict
    ) -> None:
        """Given a negative current_phase, validation should fail."""
        data = deepcopy(minimal_resumption_v2)
        data["recovery_state"]["current_phase"] = -1
        with pytest.raises(jsonschema.ValidationError):
            jsonschema.validate(instance=data, schema=RESUMPTION_SCHEMA)


class TestQualityTrajectoryValidation:
    """Tests for the quality_trajectory sub-section constraints."""

    def test_score_values_bounded(
        self, valid_resumption_v2: dict
    ) -> None:
        """Given score values outside 0.0-1.0 range, validation should fail."""
        data = deepcopy(valid_resumption_v2)
        data["quality_trajectory"]["score_history"]["qg-1"] = [1.5]
        with pytest.raises(jsonschema.ValidationError):
            jsonschema.validate(instance=data, schema=RESUMPTION_SCHEMA)


class TestCompactionEventsValidation:
    """Tests for the compaction_events sub-section constraints."""

    def test_valid_compaction_event_accepted(
        self, minimal_resumption_v2: dict
    ) -> None:
        """Given a valid compaction event entry, validation should pass."""
        data = deepcopy(minimal_resumption_v2)
        data["compaction_events"] = {
            "count": 1,
            "events": [
                {
                    "id": "CX-001",
                    "timestamp": "2026-02-17T11:45:00Z",
                    "trigger": "auto",
                    "estimated_fill_before": 0.886,
                    "active_phase": 2,
                    "active_gate": "qg-2",
                    "active_gate_iteration": 1,
                    "checkpoint_file": ".jerry/checkpoints/cx-001-checkpoint.json",
                    "acknowledged": False,
                },
            ],
        }
        jsonschema.validate(instance=data, schema=RESUMPTION_SCHEMA)

    def test_compaction_trigger_enum_enforced(
        self, minimal_resumption_v2: dict
    ) -> None:
        """Given an invalid trigger value, validation should fail."""
        data = deepcopy(minimal_resumption_v2)
        data["compaction_events"] = {
            "count": 1,
            "events": [
                {
                    "id": "CX-001",
                    "timestamp": "2026-02-17T11:45:00Z",
                    "trigger": "invalid",
                    "estimated_fill_before": 0.5,
                },
            ],
        }
        with pytest.raises(jsonschema.ValidationError):
            jsonschema.validate(instance=data, schema=RESUMPTION_SCHEMA)


class TestDecisionLogValidation:
    """Tests for the decision_log sub-section constraints."""

    def test_valid_decision_entry_accepted(
        self, minimal_resumption_v2: dict
    ) -> None:
        """Given a valid decision log entry, validation should pass."""
        data = deepcopy(minimal_resumption_v2)
        data["decision_log"] = [
            {
                "id": "RD-001",
                "gate": "qg-2",
                "iteration": 1,
                "decision": "Align copyright holder across all files",
                "rationale": "DA-001 found inconsistency",
                "affects_phases": [3],
                "applied": True,
            },
        ]
        jsonschema.validate(instance=data, schema=RESUMPTION_SCHEMA)

    def test_decision_missing_required_fields_rejected(
        self, minimal_resumption_v2: dict
    ) -> None:
        """Given a decision entry missing required fields, validation should fail."""
        data = deepcopy(minimal_resumption_v2)
        data["decision_log"] = [
            {
                "id": "RD-001",
                # Missing 'decision' and 'rationale'
            },
        ]
        with pytest.raises(jsonschema.ValidationError):
            jsonschema.validate(instance=data, schema=RESUMPTION_SCHEMA)


class TestFilesToReadValidation:
    """Tests for the files_to_read sub-section constraints."""

    def test_empty_files_to_read_rejected(
        self, minimal_resumption_v2: dict
    ) -> None:
        """Given an empty files_to_read array, validation should fail (minItems: 1)."""
        data = deepcopy(minimal_resumption_v2)
        data["files_to_read"] = []
        with pytest.raises(jsonschema.ValidationError):
            jsonschema.validate(instance=data, schema=RESUMPTION_SCHEMA)

    def test_structured_entry_requires_path_priority_purpose(
        self, minimal_resumption_v2: dict
    ) -> None:
        """Given a structured file entry missing required fields, validation should fail."""
        data = deepcopy(minimal_resumption_v2)
        data["files_to_read"] = [
            {
                "path": "ORCHESTRATION.yaml",
                # Missing 'priority' and 'purpose'
            },
        ]
        with pytest.raises(jsonschema.ValidationError):
            jsonschema.validate(instance=data, schema=RESUMPTION_SCHEMA)
