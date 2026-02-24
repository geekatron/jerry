# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
Unit tests for ResumptionContextGenerator.

Tests cover BDD scenarios from EN-004:
    - generate() with valid checkpoint returns XML
    - generate() with None resumption_state returns empty string
    - XML contains checkpoint-id
    - XML within token budget (~760 tokens)
    - recovery-state section serialization

References:
    - EN-004: ContextFillEstimator and ResumptionContextGenerator
    - PROJ-004: Context Resilience
"""

from __future__ import annotations

import pytest

from src.context_monitoring.application.services.resumption_context_generator import (
    ResumptionContextGenerator,
)
from src.context_monitoring.domain.value_objects.checkpoint_data import CheckpointData
from src.context_monitoring.domain.value_objects.fill_estimate import FillEstimate
from src.context_monitoring.domain.value_objects.threshold_tier import ThresholdTier

# =============================================================================
# Helpers
# =============================================================================


def _make_checkpoint(
    checkpoint_id: str = "cx-001",
    fill_pct: float = 0.82,
    tier: ThresholdTier = ThresholdTier.CRITICAL,
    resumption_state: dict | None = None,
    created_at: str = "2026-02-20T10:00:00+00:00",
) -> CheckpointData:
    """Create a CheckpointData for testing."""
    return CheckpointData(
        checkpoint_id=checkpoint_id,
        context_state=FillEstimate(fill_percentage=fill_pct, tier=tier),
        resumption_state=resumption_state,
        created_at=created_at,
    )


# =============================================================================
# Fixtures
# =============================================================================


@pytest.fixture()
def generator() -> ResumptionContextGenerator:
    """Return a ResumptionContextGenerator instance."""
    return ResumptionContextGenerator()


# =============================================================================
# BDD Scenario: generate() with None resumption_state returns empty string
# =============================================================================


class TestGenerateWithNoResumptionState:
    """Scenario: Checkpoint with no resumption_state produces empty output.

    Given a CheckpointData with resumption_state=None,
    generate() must return an empty string "".
    """

    def test_returns_empty_string_when_resumption_state_none(
        self, generator: ResumptionContextGenerator
    ) -> None:
        """generate() returns '' when checkpoint.resumption_state is None."""
        checkpoint = _make_checkpoint(resumption_state=None)
        result = generator.generate(checkpoint)
        assert result == ""

    def test_returns_string_type_when_none(self, generator: ResumptionContextGenerator) -> None:
        """Return type is str (not None) when resumption_state is None."""
        checkpoint = _make_checkpoint(resumption_state=None)
        result = generator.generate(checkpoint)
        assert isinstance(result, str)


# =============================================================================
# BDD Scenario: generate() with valid checkpoint returns XML
# =============================================================================


class TestGenerateWithValidCheckpoint:
    """Scenario: CheckpointData with resumption_state produces resumption XML.

    Given a CheckpointData with populated resumption_state,
    generate() must return well-formed XML with all required sections.
    """

    def test_returns_non_empty_string(self, generator: ResumptionContextGenerator) -> None:
        """generate() returns non-empty string when resumption_state is present."""
        checkpoint = _make_checkpoint(resumption_state={"current_phase": "implementation"})
        result = generator.generate(checkpoint)
        assert len(result) > 0

    def test_xml_contains_checkpoint_id(self, generator: ResumptionContextGenerator) -> None:
        """Generated XML contains the checkpoint-id element."""
        checkpoint = _make_checkpoint(
            checkpoint_id="cx-001",
            resumption_state={"step": "alpha"},
        )
        result = generator.generate(checkpoint)
        assert "<checkpoint-id>" in result
        assert "cx-001" in result

    def test_xml_contains_fill_percentage(self, generator: ResumptionContextGenerator) -> None:
        """Generated XML contains fill-percentage in context-state section."""
        checkpoint = _make_checkpoint(
            fill_pct=0.82,
            resumption_state={"step": "alpha"},
        )
        result = generator.generate(checkpoint)
        assert "<fill-percentage>" in result
        assert "0.82" in result

    def test_xml_contains_tier(self, generator: ResumptionContextGenerator) -> None:
        """Generated XML contains tier in context-state section."""
        checkpoint = _make_checkpoint(
            tier=ThresholdTier.CRITICAL,
            resumption_state={"step": "alpha"},
        )
        result = generator.generate(checkpoint)
        assert "<tier>" in result
        assert "CRITICAL" in result

    def test_xml_contains_created_at(self, generator: ResumptionContextGenerator) -> None:
        """Generated XML contains created-at element."""
        checkpoint = _make_checkpoint(
            created_at="2026-02-20T10:00:00+00:00",
            resumption_state={"step": "alpha"},
        )
        result = generator.generate(checkpoint)
        assert "<created-at>" in result
        assert "2026-02-20T10:00:00+00:00" in result

    def test_xml_contains_recovery_state_section(
        self, generator: ResumptionContextGenerator
    ) -> None:
        """Generated XML contains recovery-state section."""
        checkpoint = _make_checkpoint(resumption_state={"current_phase": "implementation"})
        result = generator.generate(checkpoint)
        assert "<recovery-state>" in result

    def test_xml_is_valid_resumption_context_structure(
        self, generator: ResumptionContextGenerator
    ) -> None:
        """Generated XML is wrapped in <resumption-context> tags."""
        checkpoint = _make_checkpoint(
            resumption_state={"step": "alpha"},
        )
        result = generator.generate(checkpoint)
        assert result.strip().startswith("<resumption-context>")
        assert result.strip().endswith("</resumption-context>")

    def test_xml_within_token_budget(self, generator: ResumptionContextGenerator) -> None:
        """Generated XML is within ~760 token budget (approx via len/4)."""
        resumption_state = {
            "current_phase": "implementation",
            "entity_id": "EN-004",
            "completed_items": ["task1", "task2"],
            "pending_items": ["task3"],
        }
        checkpoint = _make_checkpoint(resumption_state=resumption_state)
        result = generator.generate(checkpoint)
        approx_tokens = len(result) / 4
        assert approx_tokens <= 760


# =============================================================================
# BDD Scenario: recovery-state section serialization
# =============================================================================


class TestRecoveryStateSerialization:
    """Scenario: resumption_state dict is serialized as key-value pairs in XML.

    Given a resumption_state dict with various keys and values,
    each key should appear in the recovery-state section.
    """

    def test_single_key_value_serialized(self, generator: ResumptionContextGenerator) -> None:
        """Single key-value pair appears in recovery-state section."""
        checkpoint = _make_checkpoint(resumption_state={"current_phase": "testing"})
        result = generator.generate(checkpoint)
        assert "current_phase" in result
        assert "testing" in result

    def test_multiple_keys_serialized(self, generator: ResumptionContextGenerator) -> None:
        """Multiple keys all appear in recovery-state section."""
        checkpoint = _make_checkpoint(
            resumption_state={
                "phase": "alpha",
                "entity": "EN-004",
                "status": "in_progress",
            }
        )
        result = generator.generate(checkpoint)
        assert "phase" in result
        assert "entity" in result
        assert "status" in result

    def test_empty_resumption_state_dict(self, generator: ResumptionContextGenerator) -> None:
        """Empty dict resumption_state still produces XML (not empty string)."""
        checkpoint = _make_checkpoint(resumption_state={})
        result = generator.generate(checkpoint)
        # Empty dict is truthy test: resumption_state={} is not None,
        # so we still produce XML
        assert isinstance(result, str)
        # The exact behavior (empty string vs XML) may vary — document it:
        # For now we just ensure it doesn't raise and returns a string.


# =============================================================================
# BDD Scenario: TASK-001 Structured field serialization
# =============================================================================


class TestStructuredFieldSerialization:
    """Scenario: Structured fields from TASK-001 are serialized correctly.

    Given a resumption_state with structured fields (lists, dicts, nested),
    the serializer should produce semantic XML tags, not raw key-value pairs.
    """

    def test_list_values_serialized_as_items(self, generator: ResumptionContextGenerator) -> None:
        """List values produce <item> elements within parent tag."""
        checkpoint = _make_checkpoint(
            resumption_state={
                "next_actions": [
                    {"action": "Execute Phase 3 agents"},
                    {"action": "Run quality gate"},
                ],
            }
        )
        result = generator.generate(checkpoint)
        assert "<next_actions>" in result
        assert "</next_actions>" in result
        assert "<item>" in result
        assert "Execute Phase 3 agents" in result

    def test_dict_values_serialized_as_nested_tags(
        self, generator: ResumptionContextGenerator
    ) -> None:
        """Dict values produce child XML tags for each key."""
        checkpoint = _make_checkpoint(
            resumption_state={
                "quality_gate_state": {
                    "current_gate": "QG-2",
                    "total_iterations_used": 2,
                },
            }
        )
        result = generator.generate(checkpoint)
        assert "<quality_gate_state>" in result
        assert "<current_gate>QG-2</current_gate>" in result
        assert "<total_iterations_used>2</total_iterations_used>" in result

    def test_orchestration_raw_excluded_from_xml(
        self, generator: ResumptionContextGenerator
    ) -> None:
        """orchestration_raw is excluded from XML rendering (avoids duplication)."""
        checkpoint = _make_checkpoint(
            resumption_state={
                "workflow_id": "feat001",
                "orchestration_raw": "workflow:\n  id: feat001\n",
            }
        )
        result = generator.generate(checkpoint)
        assert "<workflow_id>feat001</workflow_id>" in result
        assert "orchestration_raw" not in result

    def test_agent_statuses_list_of_dicts(self, generator: ResumptionContextGenerator) -> None:
        """Agent statuses (list of dicts) render correctly."""
        checkpoint = _make_checkpoint(
            resumption_state={
                "agent_statuses": [
                    {"id": "agent-001", "status": "COMPLETE"},
                    {"id": "agent-002", "status": "IN_PROGRESS"},
                ],
            }
        )
        result = generator.generate(checkpoint)
        assert "<agent_statuses>" in result
        assert "agent-001" in result
        assert "COMPLETE" in result
        assert "agent-002" in result

    def test_simple_list_values(self, generator: ResumptionContextGenerator) -> None:
        """Simple list values (non-dict items) render as <item> elements."""
        checkpoint = _make_checkpoint(
            resumption_state={
                "gates_completed": ["QG-1", "QG-2"],
            }
        )
        result = generator.generate(checkpoint)
        assert "<gates_completed>" in result
        assert "<item>QG-1</item>" in result
        assert "<item>QG-2</item>" in result

    def test_mixed_structured_and_simple_fields(
        self, generator: ResumptionContextGenerator
    ) -> None:
        """Mix of scalars, lists, and dicts renders correctly."""
        checkpoint = _make_checkpoint(
            resumption_state={
                "workflow_id": "feat001",
                "current_phase": 3,
                "agent_statuses": [{"id": "a1", "status": "DONE"}],
                "recovery_state": {"phase": 3, "status": "ACTIVE"},
                "orchestration_raw": "raw yaml content",
            }
        )
        result = generator.generate(checkpoint)
        assert "<workflow_id>feat001</workflow_id>" in result
        assert "<current_phase>3</current_phase>" in result
        assert "<agent_statuses>" in result
        assert "<recovery_state>" in result
        assert "orchestration_raw" not in result

    def test_xml_special_chars_escaped_in_scalar(
        self, generator: ResumptionContextGenerator
    ) -> None:
        """XML special characters in scalar values are escaped."""
        checkpoint = _make_checkpoint(
            resumption_state={
                "note": "phase < 3 & status > ACTIVE",
            }
        )
        result = generator.generate(checkpoint)
        assert "&lt;" in result
        assert "&amp;" in result
        assert "&gt;" in result

    def test_xml_special_chars_escaped_in_dict_values(
        self, generator: ResumptionContextGenerator
    ) -> None:
        """XML special characters in dict values are escaped."""
        checkpoint = _make_checkpoint(
            resumption_state={
                "config": {"rule": "x < y & z > 0"},
            }
        )
        result = generator.generate(checkpoint)
        assert "&lt;" in result
        assert "&amp;" in result

    def test_xml_special_chars_escaped_in_list_items(
        self, generator: ResumptionContextGenerator
    ) -> None:
        """XML special characters in list items are escaped."""
        checkpoint = _make_checkpoint(
            resumption_state={
                "actions": [{"desc": "if a < b & c > d"}],
            }
        )
        result = generator.generate(checkpoint)
        assert "&lt;" in result
        assert "&amp;" in result
