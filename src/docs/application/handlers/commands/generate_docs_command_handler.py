# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""GenerateDocsCommandHandler — Orchestrates README documentation generation.

Coordinates SkillExtractor, ITemplateRenderer, and IFrontmatterReader to
extract skill/agent metadata, render template sections, and optionally
check or write updated content to README.md.

Location: src/docs/application/handlers/commands/generate_docs_command_handler.py
Reference: doc-module-spec.md Section: Handler Orchestration
           M-3: Atomic write pattern
           M-5: Schema validation (delegated to SkillExtractor)
"""

from __future__ import annotations

import logging
import os
import tempfile
from pathlib import Path
from typing import TYPE_CHECKING, Any

import yaml

from src.docs.application.commands.generate_docs_command import GenerateDocsCommand
from src.docs.application.results.generate_docs_result import GenerateDocsResult

if TYPE_CHECKING:
    from src.docs.application.services.skill_extractor import SkillExtractor
    from src.docs.domain.ports.frontmatter_reader import IFrontmatterReader
    from src.docs.domain.ports.template_renderer import ITemplateRenderer

logger = logging.getLogger(__name__)

_SKILLS_TABLE_TEMPLATE = "skills-table.md.jinja2"
_FEATURES_TEMPLATE = "features-section.md.jinja2"
_SKILL_EXAMPLES_FILE = "skill-examples.yaml"
_FEATURES_FILE = "features.yaml"
_SKILLS_TABLE_SECTION = "SKILLS_TABLE"
_FEATURES_SECTION = "FEATURES"
_DEFAULT_TEMPLATE_SUBDIR = Path(".context") / "templates" / "docs"
_DEFAULT_SKILLS_SUBDIR = Path("skills")


class GenerateDocsCommandHandler:
    """Handler for GenerateDocsCommand.

    Orchestrates the extraction of skill metadata, rendering of template
    sections, and optional drift detection or atomic README update.

    Error codes returned via GenerateDocsResult.error["code"]:
        - ``PATH_TRAVERSAL``: readme_path is outside the repository root.
        - ``INVALID_MODE``: command.mode is not 'check', 'write', or None.
        - ``GENERATION_ERROR``: unexpected error during extraction or rendering.

    Attributes:
        _extractor: Application service for extracting skill/agent metadata.
        _renderer: Domain port for rendering Jinja2 templates.
        _reader: Domain port for reading YAML frontmatter (unused directly,
            but available for future extension).
        _repo_root: Absolute path to the repository root, used to resolve
            skills_dir and template data paths independent of CWD (BUG-002).
    """

    def __init__(
        self,
        extractor: SkillExtractor,
        renderer: ITemplateRenderer,
        reader: IFrontmatterReader,
        repo_root: Path | None = None,
    ) -> None:
        """Initialize with injected dependencies.

        Args:
            extractor: SkillExtractor application service.
            renderer: ITemplateRenderer implementation (e.g., Jinja2Renderer).
            reader: IFrontmatterReader implementation (e.g., AstFrontmatterReader).
            repo_root: Absolute path to the repository root.  When provided,
                skills_dir and template data paths are resolved relative to
                this directory instead of CWD (BUG-002 fix).  Defaults to
                ``Path.cwd()`` when None, preserving the original behaviour
                for callers that do not supply a root.
        """
        self._extractor = extractor
        self._renderer = renderer
        self._reader = reader
        if repo_root is None:
            import logging

            logging.getLogger(__name__).warning(
                "repo_root not supplied; falling back to CWD. "
                "Pass an explicit repo_root for reliable path resolution (BUG-002)."
            )
        self._repo_root: Path = (repo_root or Path.cwd()).resolve()

    def handle(self, command: GenerateDocsCommand) -> GenerateDocsResult:
        """Execute the docs generation command.

        Args:
            command: The generation command with mode and readme path.

        Returns:
            GenerateDocsResult with rendered sections, statistics,
            and drift detection or write status.

        Note:
            The path traversal guard uses ``self._repo_root`` (resolved at
            construction time via the composition root) rather than CWD,
            ensuring consistency with all other path resolution in this
            handler (BUG-002).
        """
        # M-3/path safety: Validate readme_path is within the repository root
        # to prevent path traversal attacks (e.g., --readme ../../etc/passwd).
        # Uses self._repo_root (not CWD) for consistency with all other path
        # resolution in this handler (BUG-002).
        try:
            readme_abs = Path(command.readme_path).resolve()
            readme_abs.relative_to(self._repo_root)
        except ValueError:
            return GenerateDocsResult(
                success=False,
                error={
                    "code": "PATH_TRAVERSAL",
                    "message": "README path must be within the repository root",
                },
            )

        # Validate mode before proceeding
        valid_modes = {"check", "write", None}
        if command.mode not in valid_modes:
            return GenerateDocsResult(
                success=False,
                error={
                    "code": "INVALID_MODE",
                    "message": (
                        f"Unrecognized mode: {command.mode!r}. "
                        f"Valid modes are 'check', 'write', or None (stdout)."
                    ),
                },
            )

        warnings: list[str] = []

        try:
            # Step 1: Extract skill metadata
            # Resolve skills_dir against repo_root so the path is absolute and
            # CWD-independent (BUG-002).
            skills_dir = str(self._repo_root / _DEFAULT_SKILLS_SUBDIR)
            skills = self._extractor.extract_all(skills_dir=skills_dir)

            # Step 2: Load static data files
            # Resolve template data files against repo_root (BUG-002).
            template_data_dir = self._repo_root / _DEFAULT_TEMPLATE_SUBDIR
            examples = self._load_yaml(str(template_data_dir / _SKILL_EXAMPLES_FILE))
            features = self._load_yaml(str(template_data_dir / _FEATURES_FILE))

            # Step 3: Build template context
            total_agents = sum(s.agent_count for s in skills)
            skills_with_examples = []
            for skill in skills:
                example = examples.get(skill.name, "")
                skills_with_examples.append(
                    {
                        "name": skill.name,
                        "description": skill.description,
                        "version": skill.version,
                        "agent_count": skill.agent_count,
                        "example": example,
                    }
                )

            context: dict[str, Any] = {
                "skills": skills_with_examples,
                "total_agents": total_agents,
                "total_skills": len(skills),
                "features": features if isinstance(features, list) else [],
            }

            # Step 4: Render sections
            skills_table = self._renderer.render_section(_SKILLS_TABLE_TEMPLATE, context)
            features_section = self._renderer.render_section(_FEATURES_TEMPLATE, context)

            sections = {
                _SKILLS_TABLE_SECTION: skills_table,
                _FEATURES_SECTION: features_section,
            }

            # Step 5: Mode-specific behavior
            # - "check" mode: detect drift, set drift_detected to True/False
            # - "write" mode: write updated README, set drift_detected to False
            # - default (stdout): render only, drift_detected stays None (not applicable)
            drift_detected = None

            if command.mode == "check":
                drift_detected = self._check_drift(command.readme_path, sections, warnings)
            elif command.mode == "write":
                self._write_readme(command.readme_path, sections, warnings)
                drift_detected = False

            return GenerateDocsResult(
                success=True,
                sections=sections,
                drift_detected=drift_detected,
                skills_count=len(skills),
                agents_count=total_agents,
                warnings=warnings,
            )

        except Exception as e:
            logger.exception("Docs generation failed")
            return GenerateDocsResult(
                success=False,
                warnings=warnings,
                error={"code": "GENERATION_ERROR", "message": str(e)},
            )

    def _check_drift(
        self,
        readme_path: str,
        sections: dict[str, str],
        warnings: list[str],
    ) -> bool:
        """Check if the README content differs from generated output.

        Args:
            readme_path: Path to the README.md file.
            sections: Mapping of section names to generated content.
            warnings: Mutable list to append warnings to.

        Returns:
            True if drift is detected, False if content matches.
        """
        try:
            readme_content = Path(readme_path).read_text(encoding="utf-8")
        except FileNotFoundError:
            warnings.append(f"README not found at {readme_path}")
            return True

        for section_name, generated in sections.items():
            begin_marker = f"<!-- BEGIN:GENERATED:{section_name} -->"
            end_marker = f"<!-- END:GENERATED:{section_name} -->"

            if begin_marker not in readme_content or end_marker not in readme_content:
                warnings.append(f"Markers not found for section {section_name}")
                return True

            begin_idx = readme_content.index(begin_marker) + len(begin_marker)
            end_idx = readme_content.index(end_marker)

            if begin_idx > end_idx:
                warnings.append(f"Inverted markers for section {section_name}")
                return True

            current = readme_content[begin_idx:end_idx].strip()

            if current != generated.strip():
                return True

        return False

    def _write_readme(
        self,
        readme_path: str,
        sections: dict[str, str],
        warnings: list[str],
    ) -> None:
        """Atomically write updated sections to the README file (M-3).

        Uses ``tempfile.NamedTemporaryFile`` + ``os.replace()`` for
        atomic write to prevent corruption on interrupted writes.

        Args:
            readme_path: Path to the README.md file.
            sections: Mapping of section names to generated content.
            warnings: Mutable list to append warnings to.
        """
        readme = Path(readme_path)
        try:
            content = readme.read_text(encoding="utf-8")
        except FileNotFoundError:
            warnings.append(f"README not found at {readme_path}; cannot write")
            return

        for section_name, generated in sections.items():
            content = self._renderer.inject_between_markers(content, section_name, generated)

        # M-3: Atomic write pattern
        dir_name = str(readme.parent) if readme.parent != Path() else "."
        temp_fd = None
        temp_path = None
        try:
            temp_fd = tempfile.NamedTemporaryFile(
                mode="w",
                dir=dir_name,
                delete=False,
                suffix=".tmp",
                encoding="utf-8",
            )
            temp_path = temp_fd.name
            temp_fd.write(content)
            temp_fd.close()
            os.replace(temp_path, str(readme))
        except Exception:
            # Clean up temp file on failure
            if temp_path and Path(temp_path).exists():
                try:
                    os.unlink(temp_path)
                except OSError:
                    pass
            raise

    @staticmethod
    def _load_yaml(file_path: str) -> Any:
        """Load a YAML data file.

        Args:
            file_path: Path to the YAML file.

        Returns:
            Parsed YAML content (dict or list).

        Raises:
            FileNotFoundError: If the file does not exist.
            ValueError: If the YAML content is malformed.
        """
        try:
            content = Path(file_path).read_text(encoding="utf-8")
        except FileNotFoundError:
            raise
        try:
            return yaml.safe_load(content)
        except yaml.YAMLError as e:
            raise ValueError(f"Malformed YAML in {file_path}: {e}") from e
