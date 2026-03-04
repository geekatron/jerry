# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
ComposeSkillsCommandHandler - Composes SKILL.md files with governance sections.

Reads canonical source triplet (skill.jerry.yaml + skill.jerry.prompt.md +
skill.claude-code.yaml), builds governance sections from
SkillGovernanceSectionBuilder, injects them into the body, validates with
SkillComposeValidator, and writes the composed SKILL.md.

Pipeline (no circular dependency — canonical sources are inputs, SKILL.md is output):
  1. Read skill.jerry.yaml → CanonicalSkill entity (with description)
  2. Read skill.jerry.prompt.md → prompt_body (or SKILL.md fallback)
  3. Read skill.claude-code.yaml → vendor_overrides (allowed-tools, etc.)
  4. Build frontmatter from canonical sources (name, description + vendor overrides)
  5. Build governance sections from CanonicalSkill
  6. Inject governance sections into body (before footer)
  7. Validate composed output (SCV-001 through SCV-009)
  8. Reassemble: --- + clean frontmatter + --- + body
  9. Write composed SKILL.md

References:
    - PROJ-012: Skill Composition Pipeline
"""

from __future__ import annotations

import re
from typing import TYPE_CHECKING, Any

import yaml

from src.agents.application.commands.compose_skills_command import (
    ComposeSkillsCommand,
)
from src.agents.application.handlers.commands.compose_skill_result import (
    ComposeSkillResult,
)
from src.agents.domain.services.prompt_transformer import PromptTransformer
from src.agents.domain.services.skill_compose_validator import (
    SkillComposeValidator,
)
from src.agents.domain.services.skill_governance_builder import (
    SkillGovernanceSectionBuilder,
)
from src.agents.domain.value_objects.body_format import BodyFormat

if TYPE_CHECKING:
    from pathlib import Path

    from src.agents.application.ports.skill_repository import ISkillRepository
    from src.agents.domain.entities.canonical_skill import CanonicalSkill

# FM-07: Footer pattern broadened to handle bold/alternative formats
# Handles: *Skill Version:*, **Skill Version:**, Skill Version:
_FOOTER_RE = re.compile(r"^\*{0,2}Skill Version:.*$", re.MULTILINE)


class ComposeSkillsCommandHandler:
    """Handler for ComposeSkillsCommand.

    Reads canonical skills, builds governance sections, injects them
    into the prompt body, validates, and writes composed SKILL.md files.

    Attributes:
        _repository: Repository for reading canonical skill source.
        _governance_builder: Builds governance ## heading sections.
        _prompt_transformer: Transforms governance from canonical headings to XML.
        _validator: Post-composition validator for SCV checks.
    """

    def __init__(
        self,
        repository: ISkillRepository,
        governance_builder: SkillGovernanceSectionBuilder,
        prompt_transformer: PromptTransformer | None = None,
        validator: SkillComposeValidator | None = None,
    ) -> None:
        """Initialize with dependencies.

        Args:
            repository: Repository for reading canonical skills.
            governance_builder: Builds governance sections from CanonicalSkill.
            prompt_transformer: Transforms governance headings to XML format.
                If None, governance sections are injected as-is (markdown headings).
            validator: Post-composition validator (None = skip validation).
        """
        self._repository = repository
        self._governance_builder = governance_builder
        self._prompt_transformer = prompt_transformer
        self._validator = validator

    def handle(self, command: ComposeSkillsCommand) -> ComposeSkillResult:
        """Handle the ComposeSkillsCommand.

        Args:
            command: Compose command with optional skill filter.

        Returns:
            ComposeSkillResult with counts and output paths.
        """
        parse_errors: list[str] = []
        if command.skill_name:
            skill = self._repository.get(command.skill_name)
            if skill is None:
                return ComposeSkillResult(
                    errors=[f"Skill not found: {command.skill_name}"],
                    failed=1,
                    dry_run=command.dry_run,
                )
            skills = [skill]
        else:
            skills, parse_errors = self._repository.list_all_with_diagnostics()

        result = ComposeSkillResult(dry_run=command.dry_run)

        # Surface parse errors from list_all (FM-02)
        for parse_error in parse_errors:
            result.warnings.append(f"Parse error: {parse_error}")

        for skill in skills:
            try:
                composed_content, output_path = self._compose_skill(skill)

                # Post-composition validation (SCV-001 through SCV-009)
                if self._validator is not None:
                    folder_name = output_path.parent.name
                    governance_source = self._build_governance_dict(skill)
                    agent_body_formats = self._repository.get_agent_body_formats(skill.name)
                    validation = self._validator.validate(
                        composed_content,
                        skill_name=skill.name,
                        folder_name=folder_name,
                        governance_source=governance_source,
                        canonical_name=skill.name,
                        agent_body_formats=agent_body_formats,
                        canonical_description=skill.description,
                    )
                    if validation.errors:
                        for finding in validation.errors:
                            result.errors.append(
                                f"{skill.name}: [{finding.check_id}] {finding.message}"
                            )
                        result.failed += 1
                        continue
                    for finding in validation.warnings:
                        result.warnings.append(
                            f"{skill.name}: [{finding.check_id}] {finding.message}"
                        )

                if not command.dry_run:
                    output_path.parent.mkdir(parents=True, exist_ok=True)
                    output_path.write_text(composed_content, encoding="utf-8")

                result.output_paths.append(str(output_path))
                result.composed += 1
            except (yaml.YAMLError, OSError, KeyError, TypeError, ValueError) as e:
                result.errors.append(f"{skill.name}: {e}")
                result.failed += 1

        return result

    def _compose_skill(self, skill: CanonicalSkill) -> tuple[str, Path]:
        """Compose a single skill: build frontmatter and governance from canonical sources.

        Args:
            skill: Canonical skill entity.

        Returns:
            Tuple of (composed SKILL.md content, output Path).
        """
        output_path = self._repository.get_skill_md_path(skill.name)

        # Build frontmatter from canonical sources (no circular read)
        frontmatter = self._build_frontmatter(skill)

        # Use body from canonical prompt source
        body = skill.prompt_body

        # Strip existing governance sections so they get regenerated fresh.
        # Without this, the builder's dedup logic sees old ## Heading sections
        # and skips generation, preventing XML transformation on re-compose.
        body = self._strip_governance_sections(body)

        # Build governance sections (canonical ## Heading format)
        governance_sections = self._governance_builder.build(skill, body)

        # Transform governance sections to XML if transformer is available
        if governance_sections and self._prompt_transformer is not None:
            governance_sections = self._prompt_transformer.to_format(
                governance_sections, BodyFormat.XML
            )

        # Inject governance sections before footer
        if governance_sections:
            body = self._inject_before_footer(body, governance_sections)

        # Reassemble with clean frontmatter
        yaml_str = yaml.dump(
            frontmatter,
            default_flow_style=False,
            sort_keys=False,
            allow_unicode=True,
            width=float("inf"),
        )
        composed = f"---\n{yaml_str}---\n{body}"

        return composed, output_path

    @staticmethod
    def _build_frontmatter(skill: CanonicalSkill) -> dict[str, Any]:
        """Build SKILL.md frontmatter from canonical sources.

        Merge order:
          1. skill.jerry.yaml identity fields (name, description)
          2. skill.claude-code.yaml vendor overrides (allowed-tools, etc.)

        The ``name`` field always comes from skill.jerry.yaml and cannot
        be overridden by vendor overrides.

        Args:
            skill: Canonical skill entity.

        Returns:
            Dict suitable for YAML frontmatter serialization.
        """
        fm: dict[str, Any] = {}

        # Layer 1: Identity from skill.jerry.yaml
        fm["name"] = skill.name
        if skill.description:
            fm["description"] = skill.description

        # Layer 2: Vendor overrides from skill.claude-code.yaml
        for key, value in skill.vendor_overrides.items():
            if key != "name":  # name always from jerry.yaml
                fm[key] = value

        return fm

    @staticmethod
    def _inject_before_footer(body: str, governance_sections: str) -> str:
        """Inject governance sections before the footer line.

        The footer is identified by the pattern *Skill Version:*.
        If no footer, append at end.

        Args:
            body: Existing SKILL.md body.
            governance_sections: Governance sections to inject.

        Returns:
            Body with governance sections injected.
        """
        match = _FOOTER_RE.search(body)
        if match:
            insert_pos = match.start()
            # Ensure clean separation
            before = body[:insert_pos].rstrip("\n")
            after = body[insert_pos:]
            return f"{before}\n\n{governance_sections}\n{after}"

        # No footer found — append at end
        return f"{body.rstrip()}\n\n{governance_sections}\n"

    # Governance section headings and XML tags to strip on re-compose
    _GOVERNANCE_HEADINGS = {
        "Skill Version",
        "Activation Keywords",
        "Agent Registry",
        "Context Injection",
    }
    _GOVERNANCE_XML_TAGS = {
        "skill_version",
        "activation_keywords",
        "agent_registry",
        "context_injection",
    }

    @classmethod
    def _strip_governance_sections(cls, body: str) -> str:
        """Strip existing governance sections from body for fresh regeneration.

        Removes both ## Heading format and <xml_tag> format governance sections
        so the builder can regenerate them in the correct format.

        Args:
            body: SKILL.md body text.

        Returns:
            Body with governance sections removed.
        """
        lines = body.split("\n")
        result_lines: list[str] = []
        in_governance_heading = False
        in_governance_xml = False
        in_code_block = False

        for line in lines:
            stripped = line.strip()

            # Track code blocks to avoid stripping inside them
            if stripped.startswith("```"):
                in_code_block = not in_code_block
                if not in_governance_heading and not in_governance_xml:
                    result_lines.append(line)
                continue

            if in_code_block:
                if not in_governance_heading and not in_governance_xml:
                    result_lines.append(line)
                continue

            # Check for ## heading (any heading ends a governance heading section)
            heading_match = re.match(r"^##\s+(.+?)(?:\s*<!--.*-->)?\s*$", line)
            if heading_match:
                heading_text = heading_match.group(1).strip()
                if heading_text in cls._GOVERNANCE_HEADINGS:
                    in_governance_heading = True
                    continue
                else:
                    in_governance_heading = False
                    result_lines.append(line)
                    continue

            # Check for XML governance opening tags
            is_xml_open = False
            for tag in cls._GOVERNANCE_XML_TAGS:
                if stripped == f"<{tag}>" or re.match(rf"<{tag}\s", stripped):
                    is_xml_open = True
                    break
            if is_xml_open:
                in_governance_xml = True
                continue

            # Check for XML governance closing tags
            is_xml_close = False
            for tag in cls._GOVERNANCE_XML_TAGS:
                if stripped == f"</{tag}>":
                    is_xml_close = True
                    break
            if is_xml_close:
                in_governance_xml = False
                continue

            # Footer pattern terminates governance heading section
            if in_governance_heading and _FOOTER_RE.match(stripped):
                in_governance_heading = False

            # Skip content inside governance heading sections
            if in_governance_heading:
                continue

            # Skip content inside governance XML tags
            if in_governance_xml:
                continue

            result_lines.append(line)

        return "\n".join(result_lines)

    @staticmethod
    def _build_governance_dict(skill: CanonicalSkill) -> dict[str, Any]:
        """Build a dict matching canonical source keys for validation.

        Args:
            skill: Canonical skill entity.

        Returns:
            Dict with canonical source field names for SCV-003 cross-reference.
        """
        result: dict[str, Any] = {}
        if skill.version:
            result["version"] = skill.version
        if skill.activation_keywords:
            result["activation-keywords"] = list(skill.activation_keywords)
        if skill.agents:
            result["agents"] = list(skill.agents)
        if skill.context_injection:
            result["context_injection"] = skill.context_injection
        return result
