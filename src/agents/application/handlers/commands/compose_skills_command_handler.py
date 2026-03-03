# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
ComposeSkillsCommandHandler - Composes SKILL.md files with governance sections.

Reads skill.jerry.yaml canonical source, builds governance sections from
SkillGovernanceSectionBuilder, injects them into the SKILL.md body,
validates with SkillComposeValidator, and writes the result.

Pipeline (simpler than agents — no 4-layer merge):
  1. Read skill.jerry.yaml → CanonicalSkill entity
  2. Read existing SKILL.md → parse frontmatter + body
  3. Build governance sections from CanonicalSkill
  4. Inject governance sections into body (before footer)
  5. Validate composed output (SCV-001 through SCV-006)
  6. Reassemble: --- + clean frontmatter + --- + body
  7. Write composed SKILL.md

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
from src.agents.domain.services.skill_compose_validator import (
    SkillComposeValidator,
)
from src.agents.domain.services.skill_governance_builder import (
    SkillGovernanceSectionBuilder,
)

if TYPE_CHECKING:
    from pathlib import Path

    from src.agents.application.ports.skill_repository import ISkillRepository
    from src.agents.domain.entities.canonical_skill import CanonicalSkill

# Footer pattern to find injection point
_FOOTER_RE = re.compile(r"^\*Skill Version:.*$", re.MULTILINE)


class ComposeSkillsCommandHandler:
    """Handler for ComposeSkillsCommand.

    Reads canonical skills, builds governance sections, injects them
    into SKILL.md body, validates, and writes composed files.

    Attributes:
        _repository: Repository for reading canonical skill source.
        _governance_builder: Builds governance ## heading sections.
        _validator: Post-composition validator for SCV checks.
    """

    def __init__(
        self,
        repository: ISkillRepository,
        governance_builder: SkillGovernanceSectionBuilder,
        validator: SkillComposeValidator | None = None,
    ) -> None:
        """Initialize with dependencies.

        Args:
            repository: Repository for reading canonical skills.
            governance_builder: Builds governance sections from CanonicalSkill.
            validator: Post-composition validator (None = skip validation).
        """
        self._repository = repository
        self._governance_builder = governance_builder
        self._validator = validator

    def handle(self, command: ComposeSkillsCommand) -> ComposeSkillResult:
        """Handle the ComposeSkillsCommand.

        Args:
            command: Compose command with optional skill filter.

        Returns:
            ComposeSkillResult with counts and output paths.
        """
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
            skills = self._repository.list_all()

        result = ComposeSkillResult(dry_run=command.dry_run)

        for skill in skills:
            try:
                composed_content, output_path = self._compose_skill(skill)

                # Post-composition validation (SCV-001 through SCV-006)
                if self._validator is not None:
                    folder_name = output_path.parent.name
                    governance_source = self._build_governance_dict(skill)
                    validation = self._validator.validate(
                        composed_content,
                        skill_name=skill.name,
                        folder_name=folder_name,
                        governance_source=governance_source,
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
        """Compose a single skill: build governance, inject into body.

        Args:
            skill: Canonical skill entity.

        Returns:
            Tuple of (composed SKILL.md content, output Path).
        """
        output_path = self._repository.get_skill_md_path(skill.name)

        # Parse existing SKILL.md
        existing_content = ""
        if output_path.exists():
            existing_content = output_path.read_text(encoding="utf-8")

        frontmatter, body = self._parse_md(existing_content)

        # Build governance sections
        governance_sections = self._governance_builder.build(skill, body)

        # Inject governance sections before footer
        if governance_sections:
            body = self._inject_before_footer(body, governance_sections)

        # Reassemble with clean frontmatter
        yaml_str = yaml.dump(
            frontmatter,
            default_flow_style=False,
            sort_keys=False,
            allow_unicode=True,
            width=200,
        )
        composed = f"---\n{yaml_str}---\n{body}"

        return composed, output_path

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

    @staticmethod
    def _parse_md(content: str) -> tuple[dict[str, Any], str]:
        """Parse an .md file into frontmatter dict and body string.

        Args:
            content: Full .md file content.

        Returns:
            Tuple of (frontmatter_dict, body_string).
        """
        if not content.startswith("---"):
            return {}, content

        end = content.find("---", 3)
        if end == -1:
            return {}, content

        fm_text = content[3:end].strip()
        body = content[end + 3 :].lstrip("\n")

        try:
            fm_data = yaml.safe_load(fm_text) or {}
        except yaml.YAMLError:
            fm_data = {}

        return fm_data, body

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
