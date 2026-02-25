# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
Extended schema definitions for all Jerry markdown file types.

Provides schema constants for the 9 new file-type schemas (WI-014, WI-015)
and constructs the frozen default ``SchemaRegistry`` containing all 15 schemas
(6 existing worktracker + 9 new file types).

The default registry is constructed at module load time and frozen immediately
to prevent runtime schema poisoning (T-SV-05).

References:
    - ADR-PROJ005-003 Design Decision 4 (Schema Extension Architecture)
    - WI-014: Agent definition and skill definition schemas
    - WI-015: Remaining file-type schemas
    - Threat Model: T-SV-04 (collision detection), T-SV-05 (freeze)
    - H-07: Domain layer constraint (no external infra/interface imports)

Exports:
    AGENT_DEFINITION_SCHEMA: Schema for agent definition files.
    SKILL_DEFINITION_SCHEMA: Schema for SKILL.md files.
    RULE_FILE_SCHEMA: Schema for rule files.
    ADR_SCHEMA: Schema for ADR documents.
    STRATEGY_TEMPLATE_SCHEMA: Schema for strategy template files.
    FRAMEWORK_CONFIG_SCHEMA: Schema for framework config files.
    ORCHESTRATION_SCHEMA: Schema for orchestration artifacts.
    PATTERN_SCHEMA: Schema for pattern documents.
    KNOWLEDGE_SCHEMA: Schema for knowledge documents.
    DEFAULT_REGISTRY: The frozen default SchemaRegistry with all 15 schemas.
"""

from __future__ import annotations

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
)
from src.domain.markdown_ast.schema_registry import SchemaRegistry

# ---------------------------------------------------------------------------
# New file-type schemas (WI-014: agent_definition, skill_definition)
# ---------------------------------------------------------------------------

AGENT_DEFINITION_SCHEMA: EntitySchema = EntitySchema(
    entity_type="agent_definition",
    field_rules=(
        FieldRule(key="name", required=True, value_pattern=r"^[a-z]+-[a-z]+(-[a-z]+)*$"),
        FieldRule(key="version", required=True, value_pattern=r"^\d+\.\d+\.\d+$"),
        FieldRule(key="description", required=True),
        FieldRule(
            key="model",
            required=True,
            allowed_values=("opus", "sonnet", "haiku"),
        ),
    ),
    section_rules=(),
    require_nav_table=False,
)

SKILL_DEFINITION_SCHEMA: EntitySchema = EntitySchema(
    entity_type="skill_definition",
    field_rules=(
        FieldRule(key="name", required=True),
        FieldRule(key="version", required=True, value_pattern=r"^\d+\.\d+\.\d+$"),
        FieldRule(key="description", required=True),
    ),
    section_rules=(
        SectionRule(heading="Agents", required=False),
        SectionRule(heading="When to Use", required=False),
    ),
    require_nav_table=False,
)

# ---------------------------------------------------------------------------
# New file-type schemas (WI-015: remaining types)
# ---------------------------------------------------------------------------

RULE_FILE_SCHEMA: EntitySchema = EntitySchema(
    entity_type="rule_file",
    field_rules=(),
    section_rules=(
        SectionRule(heading="HARD Rules", required=False),
        SectionRule(heading="Document Sections", required=False),
    ),
    require_nav_table=False,
)

ADR_SCHEMA: EntitySchema = EntitySchema(
    entity_type="adr",
    field_rules=(),
    section_rules=(
        SectionRule(heading="Status", required=True),
        SectionRule(heading="Context", required=True),
        SectionRule(heading="Decision", required=True),
        SectionRule(heading="Consequences", required=True),
    ),
    require_nav_table=True,
)

STRATEGY_TEMPLATE_SCHEMA: EntitySchema = EntitySchema(
    entity_type="strategy_template",
    field_rules=(
        FieldRule(key="Strategy", required=True),
        FieldRule(key="ID", required=True, value_pattern=r"^S-\d{3}$"),
        FieldRule(key="Family", required=True),
    ),
    section_rules=(
        SectionRule(heading="Prompt Template", required=True),
        SectionRule(heading="Rubric", required=True),
    ),
    require_nav_table=False,
)

FRAMEWORK_CONFIG_SCHEMA: EntitySchema = EntitySchema(
    entity_type="framework_config",
    field_rules=(),
    section_rules=(SectionRule(heading="Document Sections", required=False),),
    require_nav_table=False,
)

ORCHESTRATION_SCHEMA: EntitySchema = EntitySchema(
    entity_type="orchestration_artifact",
    field_rules=(),
    section_rules=(),
    require_nav_table=False,
)

PATTERN_SCHEMA: EntitySchema = EntitySchema(
    entity_type="pattern_document",
    field_rules=(),
    section_rules=(),
    require_nav_table=False,
)

KNOWLEDGE_SCHEMA: EntitySchema = EntitySchema(
    entity_type="knowledge_document",
    field_rules=(),
    section_rules=(SectionRule(heading="Document Sections", required=False),),
    require_nav_table=False,
)

# ---------------------------------------------------------------------------
# New file-type schemas (EN-002: Document Type Ontology Hardening)
# ---------------------------------------------------------------------------

SKILL_RESOURCE_SCHEMA: EntitySchema = EntitySchema(
    entity_type="skill_resource",
    field_rules=(),
    section_rules=(),
    require_nav_table=False,
)

TEMPLATE_SCHEMA: EntitySchema = EntitySchema(
    entity_type="template",
    field_rules=(),
    section_rules=(),
    require_nav_table=False,
)


# ---------------------------------------------------------------------------
# Default registry: register all schemas and freeze (V-06 remediation)
# ---------------------------------------------------------------------------

DEFAULT_REGISTRY = SchemaRegistry()

# Register existing worktracker entity schemas
DEFAULT_REGISTRY.register(EPIC_SCHEMA)
DEFAULT_REGISTRY.register(FEATURE_SCHEMA)
DEFAULT_REGISTRY.register(STORY_SCHEMA)
DEFAULT_REGISTRY.register(ENABLER_SCHEMA)
DEFAULT_REGISTRY.register(TASK_SCHEMA)
DEFAULT_REGISTRY.register(BUG_SCHEMA)

# Register new file-type schemas (WI-014, WI-015)
DEFAULT_REGISTRY.register(AGENT_DEFINITION_SCHEMA)
DEFAULT_REGISTRY.register(SKILL_DEFINITION_SCHEMA)
DEFAULT_REGISTRY.register(RULE_FILE_SCHEMA)
DEFAULT_REGISTRY.register(ADR_SCHEMA)
DEFAULT_REGISTRY.register(STRATEGY_TEMPLATE_SCHEMA)
DEFAULT_REGISTRY.register(FRAMEWORK_CONFIG_SCHEMA)
DEFAULT_REGISTRY.register(ORCHESTRATION_SCHEMA)
DEFAULT_REGISTRY.register(PATTERN_SCHEMA)
DEFAULT_REGISTRY.register(KNOWLEDGE_SCHEMA)

# Register EN-002 schemas (skill_resource, template)
DEFAULT_REGISTRY.register(SKILL_RESOURCE_SCHEMA)
DEFAULT_REGISTRY.register(TEMPLATE_SCHEMA)

# Freeze after module-level registration (T-SV-05: runtime poisoning prevention)
DEFAULT_REGISTRY.freeze()
