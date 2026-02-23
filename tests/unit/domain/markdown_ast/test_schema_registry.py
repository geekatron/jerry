# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""Unit tests for SchemaRegistry (WI-003) and schema definitions (WI-014/WI-015/WI-016).

Tests cover:
    - SchemaRegistry register(), freeze(), get(), list_types(), schemas property
    - Collision detection (T-SV-04)
    - Freeze enforcement (T-SV-05)
    - MappingProxyType read-only view
    - DEFAULT_REGISTRY with all 15 schemas
    - New file-type schemas (WI-014, WI-015)
    - Backward compatibility of get_entity_schema()

References:
    - H-20: BDD test-first
"""

from __future__ import annotations

from types import MappingProxyType

import pytest

from src.domain.markdown_ast.schema import (
    BUG_SCHEMA,
    ENABLER_SCHEMA,
    EPIC_SCHEMA,
    FEATURE_SCHEMA,
    STORY_SCHEMA,
    TASK_SCHEMA,
    EntitySchema,
    FieldRule,
    SectionRule,
    get_entity_schema,
)
from src.domain.markdown_ast.schema_definitions import (
    ADR_SCHEMA,
    AGENT_DEFINITION_SCHEMA,
    DEFAULT_REGISTRY,
    FRAMEWORK_CONFIG_SCHEMA,
    KNOWLEDGE_SCHEMA,
    ORCHESTRATION_SCHEMA,
    PATTERN_SCHEMA,
    RULE_FILE_SCHEMA,
    SKILL_DEFINITION_SCHEMA,
    STRATEGY_TEMPLATE_SCHEMA,
)
from src.domain.markdown_ast.schema_registry import SchemaRegistry


# =============================================================================
# SchemaRegistry Core Tests (WI-003)
# =============================================================================


class TestSchemaRegistryRegister:
    """Tests for SchemaRegistry.register()."""

    @pytest.mark.happy_path
    def test_register_succeeds_before_freeze(self) -> None:
        """Registering a schema before freeze succeeds."""
        registry = SchemaRegistry()
        schema = EntitySchema(
            entity_type="test_type",
            field_rules=(),
            section_rules=(),
            require_nav_table=False,
        )
        registry.register(schema)
        assert registry.get("test_type") is schema

    @pytest.mark.negative
    def test_register_after_freeze_raises_runtime_error(self) -> None:
        """Registering after freeze raises RuntimeError (T-SV-05)."""
        registry = SchemaRegistry()
        registry.freeze()
        schema = EntitySchema(
            entity_type="test_type",
            field_rules=(),
            section_rules=(),
            require_nav_table=False,
        )
        with pytest.raises(RuntimeError, match="registry is frozen"):
            registry.register(schema)

    @pytest.mark.negative
    def test_register_duplicate_raises_value_error(self) -> None:
        """Registering duplicate entity_type raises ValueError (T-SV-04)."""
        registry = SchemaRegistry()
        schema = EntitySchema(
            entity_type="test_type",
            field_rules=(),
            section_rules=(),
            require_nav_table=False,
        )
        registry.register(schema)
        with pytest.raises(ValueError, match="already registered"):
            registry.register(schema)


class TestSchemaRegistryFreeze:
    """Tests for SchemaRegistry.freeze()."""

    @pytest.mark.happy_path
    def test_freeze_sets_frozen_property(self) -> None:
        """Freeze sets the frozen property to True."""
        registry = SchemaRegistry()
        assert registry.frozen is False
        registry.freeze()
        assert registry.frozen is True

    @pytest.mark.edge_case
    def test_freeze_is_idempotent(self) -> None:
        """Calling freeze() multiple times does not raise."""
        registry = SchemaRegistry()
        registry.freeze()
        registry.freeze()  # Should not raise
        assert registry.frozen is True


class TestSchemaRegistryGet:
    """Tests for SchemaRegistry.get()."""

    @pytest.mark.happy_path
    def test_get_returns_registered_schema(self) -> None:
        """get() returns the correct schema for a registered type."""
        registry = SchemaRegistry()
        schema = EntitySchema(
            entity_type="test_type",
            field_rules=(),
            section_rules=(),
            require_nav_table=False,
        )
        registry.register(schema)
        assert registry.get("test_type") is schema

    @pytest.mark.negative
    def test_get_unknown_type_raises_value_error(self) -> None:
        """get() raises ValueError for an unknown entity type."""
        registry = SchemaRegistry()
        with pytest.raises(ValueError, match="Unknown entity type"):
            registry.get("nonexistent")


class TestSchemaRegistryListTypes:
    """Tests for SchemaRegistry.list_types()."""

    @pytest.mark.happy_path
    def test_list_types_returns_sorted_names(self) -> None:
        """list_types() returns sorted entity type names."""
        registry = SchemaRegistry()
        for name in ["charlie", "alpha", "bravo"]:
            registry.register(
                EntitySchema(
                    entity_type=name,
                    field_rules=(),
                    section_rules=(),
                    require_nav_table=False,
                )
            )
        assert registry.list_types() == ["alpha", "bravo", "charlie"]


class TestSchemaRegistrySchemas:
    """Tests for SchemaRegistry.schemas property."""

    @pytest.mark.happy_path
    def test_schemas_returns_mapping_proxy(self) -> None:
        """schemas property returns MappingProxyType."""
        registry = SchemaRegistry()
        assert isinstance(registry.schemas, MappingProxyType)

    @pytest.mark.negative
    def test_schemas_proxy_is_read_only(self) -> None:
        """Mutations via schemas proxy raise TypeError."""
        registry = SchemaRegistry()
        with pytest.raises(TypeError):
            registry.schemas["new"] = None  # type: ignore[index]


# =============================================================================
# DEFAULT_REGISTRY Tests (WI-003, WI-014, WI-015, WI-016)
# =============================================================================


class TestDefaultRegistry:
    """Tests for the module-level DEFAULT_REGISTRY."""

    @pytest.mark.happy_path
    def test_default_registry_is_frozen(self) -> None:
        """DEFAULT_REGISTRY is frozen at module load time."""
        assert DEFAULT_REGISTRY.frozen is True

    @pytest.mark.happy_path
    def test_default_registry_has_15_schemas(self) -> None:
        """DEFAULT_REGISTRY contains all 15 schemas (6 existing + 9 new)."""
        assert len(DEFAULT_REGISTRY.schemas) == 15

    @pytest.mark.happy_path
    def test_default_registry_contains_existing_worktracker_schemas(self) -> None:
        """All 6 existing worktracker schemas are registered."""
        for entity_type in ["epic", "feature", "story", "enabler", "task", "bug"]:
            assert entity_type in DEFAULT_REGISTRY.schemas

    @pytest.mark.happy_path
    def test_default_registry_contains_new_schemas(self) -> None:
        """All 9 new file-type schemas are registered."""
        new_types = [
            "agent_definition",
            "skill_definition",
            "rule_file",
            "adr",
            "strategy_template",
            "framework_config",
            "orchestration_artifact",
            "pattern_document",
            "knowledge_document",
        ]
        for entity_type in new_types:
            assert entity_type in DEFAULT_REGISTRY.schemas

    @pytest.mark.negative
    def test_default_registry_rejects_registration(self) -> None:
        """DEFAULT_REGISTRY is frozen and rejects new registrations."""
        schema = EntitySchema(
            entity_type="test_type",
            field_rules=(),
            section_rules=(),
            require_nav_table=False,
        )
        with pytest.raises(RuntimeError, match="registry is frozen"):
            DEFAULT_REGISTRY.register(schema)


# =============================================================================
# New Schema Definition Tests (WI-014, WI-015)
# =============================================================================


class TestAgentDefinitionSchema:
    """Tests for AGENT_DEFINITION_SCHEMA (WI-014)."""

    @pytest.mark.happy_path
    def test_entity_type(self) -> None:
        assert AGENT_DEFINITION_SCHEMA.entity_type == "agent_definition"

    @pytest.mark.happy_path
    def test_has_required_fields(self) -> None:
        required_keys = {r.key for r in AGENT_DEFINITION_SCHEMA.field_rules if r.required}
        assert "name" in required_keys
        assert "version" in required_keys
        assert "description" in required_keys
        assert "model" in required_keys

    @pytest.mark.happy_path
    def test_model_allowed_values(self) -> None:
        model_rule = next(r for r in AGENT_DEFINITION_SCHEMA.field_rules if r.key == "model")
        assert model_rule.allowed_values == ("opus", "sonnet", "haiku")


class TestSkillDefinitionSchema:
    """Tests for SKILL_DEFINITION_SCHEMA (WI-014)."""

    @pytest.mark.happy_path
    def test_entity_type(self) -> None:
        assert SKILL_DEFINITION_SCHEMA.entity_type == "skill_definition"

    @pytest.mark.happy_path
    def test_has_required_fields(self) -> None:
        required_keys = {r.key for r in SKILL_DEFINITION_SCHEMA.field_rules if r.required}
        assert "name" in required_keys
        assert "version" in required_keys
        assert "description" in required_keys


class TestAdrSchema:
    """Tests for ADR_SCHEMA (WI-015)."""

    @pytest.mark.happy_path
    def test_entity_type(self) -> None:
        assert ADR_SCHEMA.entity_type == "adr"

    @pytest.mark.happy_path
    def test_required_sections(self) -> None:
        required_sections = {s.heading for s in ADR_SCHEMA.section_rules if s.required}
        assert "Status" in required_sections
        assert "Context" in required_sections
        assert "Decision" in required_sections
        assert "Consequences" in required_sections

    @pytest.mark.happy_path
    def test_requires_nav_table(self) -> None:
        assert ADR_SCHEMA.require_nav_table is True


class TestStrategyTemplateSchema:
    """Tests for STRATEGY_TEMPLATE_SCHEMA (WI-015)."""

    @pytest.mark.happy_path
    def test_entity_type(self) -> None:
        assert STRATEGY_TEMPLATE_SCHEMA.entity_type == "strategy_template"

    @pytest.mark.happy_path
    def test_has_id_pattern(self) -> None:
        id_rule = next(r for r in STRATEGY_TEMPLATE_SCHEMA.field_rules if r.key == "ID")
        assert id_rule.value_pattern is not None


class TestRemainingSchemas:
    """Tests for remaining schemas (WI-015)."""

    @pytest.mark.happy_path
    def test_rule_file_schema(self) -> None:
        assert RULE_FILE_SCHEMA.entity_type == "rule_file"
        assert RULE_FILE_SCHEMA.require_nav_table is False

    @pytest.mark.happy_path
    def test_framework_config_schema(self) -> None:
        assert FRAMEWORK_CONFIG_SCHEMA.entity_type == "framework_config"

    @pytest.mark.happy_path
    def test_orchestration_schema(self) -> None:
        assert ORCHESTRATION_SCHEMA.entity_type == "orchestration_artifact"

    @pytest.mark.happy_path
    def test_pattern_schema(self) -> None:
        assert PATTERN_SCHEMA.entity_type == "pattern_document"

    @pytest.mark.happy_path
    def test_knowledge_schema(self) -> None:
        assert KNOWLEDGE_SCHEMA.entity_type == "knowledge_document"


# =============================================================================
# Backward Compatibility (WI-003)
# =============================================================================


class TestGetEntitySchemaBackwardCompat:
    """Verify get_entity_schema() delegates to DEFAULT_REGISTRY."""

    @pytest.mark.happy_path
    def test_get_entity_schema_returns_epic(self) -> None:
        schema = get_entity_schema("epic")
        assert schema.entity_type == "epic"

    @pytest.mark.happy_path
    def test_get_entity_schema_returns_new_type(self) -> None:
        schema = get_entity_schema("agent_definition")
        assert schema.entity_type == "agent_definition"

    @pytest.mark.negative
    def test_get_entity_schema_unknown_raises(self) -> None:
        with pytest.raises(ValueError, match="Unknown entity type"):
            get_entity_schema("nonexistent_type")
