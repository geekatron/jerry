# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
ValidateFrontmatterCommandHandler -- Handler for frontmatter validation.

Validates YAML frontmatter in skills/*/agents/*.md and skills/*/SKILL.md files
against the official Claude Code JSON schemas. Performs structural schema
validation plus semantic checks (name-matches-filename, unrecognized fields,
P-003 Agent tool restriction, security checks).

References:
    - PROJ-024: CLI frontmatter validation command
    - STORY-025: Port P-003 validation from standalone script
    - STORY-022: P-003 Agent tool restriction (original implementation)
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from src.agents.application.commands.frontmatter_file_result import (
    FrontmatterFileResult,
)
from src.agents.application.commands.validate_frontmatter_command import (
    ValidateFrontmatterCommand,
)
from src.agents.application.commands.validate_frontmatter_result import (
    ValidateFrontmatterResult,
)

# ---------------------------------------------------------------------------
# Constants: known official Claude Code fields
# ---------------------------------------------------------------------------

#: Official Claude Code agent frontmatter fields (March 2026).
_AGENT_KNOWN_FIELDS: frozenset[str] = frozenset(
    {
        "name",
        "description",
        "model",
        "tools",
        "disallowedTools",
        "mcpServers",
        "permissionMode",
        "maxTurns",
        "skills",
        "hooks",
        "memory",
        "background",
        "isolation",
        "color",
        "effort",
        "initialPrompt",
    }
)

#: Official Claude Code SKILL.md frontmatter fields (March 2026).
_SKILL_KNOWN_FIELDS: frozenset[str] = frozenset(
    {
        "name",
        "description",
        "argument-hint",
        "disable-model-invocation",
        "user-invocable",
        "allowed-tools",
        "model",
        "context",
        "agent",
        "hooks",
        "paths",
        "shell",
        "mode",
        "license",
        "compatibility",
        "metadata",
        "effort",
    }
)

_MULTILINE_INDICATOR_RE: re.Pattern[str] = re.compile(r"^description:\s*[>|]", re.MULTILINE)
_XML_TAG_RE: re.Pattern[str] = re.compile(r"<[^>]+>")


class ValidateFrontmatterCommandHandler:
    """Handler for ValidateFrontmatterCommand.

    Loads JSON schemas, discovers .md files, extracts YAML frontmatter from
    each, validates against the appropriate schema, and applies semantic checks
    including P-003 Agent tool restriction enforcement.

    Attributes:
        _repo_root: Absolute path to the repository root.
        _agent_schema_path: Path to the agent frontmatter JSON schema.
        _skill_schema_path: Path to the skill frontmatter JSON schema.
    """

    def __init__(
        self,
        repo_root: Path,
        agent_schema_path: Path,
        skill_schema_path: Path,
    ) -> None:
        """Initialize the handler with schema paths.

        Args:
            repo_root: Absolute path to repository root.
            agent_schema_path: Path to claude-code-frontmatter-v1.schema.json.
            skill_schema_path: Path to claude-code-skill-frontmatter-v1.schema.json.

        Raises:
            FileNotFoundError: If either schema file does not exist.
        """
        if not agent_schema_path.exists():
            raise FileNotFoundError(f"Agent schema not found: {agent_schema_path}")
        if not skill_schema_path.exists():
            raise FileNotFoundError(f"Skill schema not found: {skill_schema_path}")

        self._repo_root = repo_root
        self._agent_schema: dict[str, Any] = json.loads(
            agent_schema_path.read_text(encoding="utf-8")
        )
        self._skill_schema: dict[str, Any] = json.loads(
            skill_schema_path.read_text(encoding="utf-8")
        )

    def handle(self, command: ValidateFrontmatterCommand) -> ValidateFrontmatterResult:
        """Execute the frontmatter validation command.

        Args:
            command: Command specifying optional agent/skill filters and repo root.

        Returns:
            ValidateFrontmatterResult with per-file outcomes.
        """
        repo_root = command.repo_root if command.repo_root is not None else self._repo_root

        if command.agent_filter is not None:
            agent_files = self._discover_agent_files(repo_root, command.agent_filter)
            skill_files: list[Path] = []
        elif command.skill_filter is not None:
            agent_files: list[Path] = []
            skill_files = self._discover_skill_files(repo_root, command.skill_filter)
        else:
            agent_files = self._discover_agent_files(repo_root, None)
            skill_files = self._discover_skill_files(repo_root, None)

        agent_results = [self._validate_agent_file(fp, repo_root) for fp in agent_files]
        skill_results = [self._validate_skill_file(fp, repo_root) for fp in skill_files]

        return ValidateFrontmatterResult(
            agent_results=agent_results,
            skill_results=skill_results,
        )

    # ------------------------------------------------------------------
    # File discovery
    # ------------------------------------------------------------------

    def _discover_agent_files(
        self,
        repo_root: Path,
        agent_filter: str | None,
    ) -> list[Path]:
        """Discover agent .md files under skills/*/agents/*.md.

        Args:
            repo_root: Repository root to search from.
            agent_filter: Optional stem name to match.

        Returns:
            Sorted list of matching agent .md paths.
        """
        found: list[Path] = []
        for fp in sorted((repo_root / "skills").rglob("agents/*.md")):
            if ".graveyard" in fp.parts:
                continue
            if agent_filter is not None and fp.stem != agent_filter:
                continue
            found.append(fp)
        return found

    def _discover_skill_files(
        self,
        repo_root: Path,
        skill_filter: str | None,
    ) -> list[Path]:
        """Discover SKILL.md files under skills/*/SKILL.md.

        Args:
            repo_root: Repository root to search from.
            skill_filter: Optional parent directory name.

        Returns:
            Sorted list of matching SKILL.md paths.
        """
        found: list[Path] = []
        for fp in sorted((repo_root / "skills").rglob("SKILL.md")):
            if ".graveyard" in fp.parts:
                continue
            if skill_filter is not None and fp.parent.name != skill_filter:
                continue
            found.append(fp)
        return found

    # ------------------------------------------------------------------
    # Frontmatter extraction
    # ------------------------------------------------------------------

    def _extract_frontmatter(
        self,
        file_path: Path,
    ) -> tuple[str | None, dict[str, Any] | None, str | None]:
        """Extract raw YAML frontmatter text and parsed dict from a file.

        Args:
            file_path: Path to the .md file.

        Returns:
            Tuple of (raw_text, parsed_dict, error_message).
        """
        try:
            import yaml
        except ImportError as exc:
            return None, None, f"PyYAML not installed: {exc}"

        try:
            text = file_path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError) as exc:
            return None, None, f"Could not read file: {exc}"

        match = re.match(r"^---\s*\n(.*?)\n---", text, re.DOTALL)
        if not match:
            match = re.match(r"^---\n(.*?)\n---", text, re.DOTALL)
        if not match:
            return None, None, None

        raw_text = match.group(1)
        if not raw_text.strip():
            return raw_text, {}, None

        try:
            parsed = yaml.safe_load(raw_text)
        except yaml.YAMLError as exc:
            return raw_text, None, f"YAML parse error: {exc}"

        if not isinstance(parsed, dict):
            return (
                raw_text,
                None,
                (f"Frontmatter parsed to {type(parsed).__name__}, expected mapping"),
            )

        return raw_text, parsed, None

    # ------------------------------------------------------------------
    # Schema validation
    # ------------------------------------------------------------------

    def _schema_errors(
        self,
        frontmatter: dict[str, Any],
        schema: dict[str, Any],
    ) -> list[tuple[str, str, str]]:
        """Run JSON Schema validation against frontmatter.

        Args:
            frontmatter: Parsed YAML frontmatter dict.
            schema: JSON Schema dict to validate against.

        Returns:
            List of (field_path, constraint, current_value) tuples.
        """
        from jsonschema import Draft202012Validator

        results: list[tuple[str, str, str]] = []
        validator = Draft202012Validator(schema)
        for error in sorted(validator.iter_errors(frontmatter), key=lambda e: list(e.path)):
            field_path = ".".join(str(p) for p in error.absolute_path) or "(root)"
            schema_path_parts = list(error.absolute_schema_path)
            constraint = str(schema_path_parts[-1]) if schema_path_parts else "unknown"
            try:
                current_val = repr(error.instance)
                if len(current_val) > 120:
                    current_val = current_val[:117] + "..."
            except Exception:
                current_val = "(unable to represent)"
            results.append((field_path, constraint, current_val))
        return results

    # ------------------------------------------------------------------
    # Per-file validation
    # ------------------------------------------------------------------

    def _validate_agent_file(self, fp: Path, repo_root: Path) -> FrontmatterFileResult:
        """Validate a single agent .md file.

        Applies JSON Schema validation and semantic checks:
        - name must match filename stem
        - unrecognized fields produce a warning
        - MCP tools in the 'tools' field produce a warning
        - P-003: Agent/Task tool restricted to T5 orchestrators only (STORY-022/025)

        Args:
            fp: Path to the agent .md file.
            repo_root: Repository root for computing relative path.

        Returns:
            FrontmatterFileResult with full validation outcome.
        """
        result = FrontmatterFileResult(
            path=fp,
            file_type="agent",
            relative_path=str(fp.relative_to(repo_root)),
        )
        raw_text, fm, error = self._extract_frontmatter(fp)

        if error is not None:
            result.status = "parse_error"
            result.errors.append(("(file)", "parse_error", error))
            return result

        if raw_text is None or fm is None:
            result.status = "no_frontmatter"
            return result

        result.frontmatter = fm

        # JSON Schema validation
        for field_path, constraint, val in self._schema_errors(fm, self._agent_schema):
            result.errors.append((field_path, constraint, val))

        # Semantic: name must match filename stem
        expected_name = fp.stem
        actual_name = fm.get("name", "")
        if actual_name != expected_name:
            result.errors.append(
                (
                    "name",
                    "name_matches_filename",
                    f"'{actual_name}' (expected '{expected_name}')",
                )
            )

        # Semantic: unrecognized fields -> warning
        unknown = set(fm.keys()) - _AGENT_KNOWN_FIELDS
        if unknown:
            result.warnings.append(
                (
                    "(root)",
                    "unrecognized_fields",
                    f"Jerry-specific fields not recognized by Claude Code: {sorted(unknown)}",
                )
            )

        # Semantic: MCP tools in tools field -> warning
        tools = fm.get("tools")
        if isinstance(tools, str):
            tools_list = [t.strip() for t in tools.split(",")]
        elif isinstance(tools, list):
            tools_list = [str(t) for t in tools]
        else:
            tools_list = []
        mcp_in_tools = [t for t in tools_list if t.startswith("mcp__")]
        if mcp_in_tools:
            result.warnings.append(
                (
                    "tools",
                    "mcp_tools_in_tools_field",
                    f"MCP tools should go in mcpServers, not tools: {mcp_in_tools}",
                )
            )

        # P-003: Agent/Task tool restricted to T5 orchestrators (STORY-022/025)
        delegation_tools = [t for t in tools_list if t in ("Agent", "Task")]
        if delegation_tools:
            gov_path = fp.with_suffix(".governance.yaml")
            is_t5 = False
            if gov_path.exists():
                try:
                    import yaml

                    gov = yaml.safe_load(gov_path.read_text(encoding="utf-8"))
                    if isinstance(gov, dict):
                        tier = gov.get("tool_tier")
                        is_t5 = isinstance(tier, str) and tier == "T5"
                except Exception as exc:
                    result.warnings.append(
                        (
                            "tools",
                            "governance_read_error",
                            f"Could not read {gov_path.name}: {exc} -- assuming non-T5",
                        )
                    )
            if not is_t5:
                result.errors.append(
                    (
                        "tools",
                        "p003_agent_tool_restriction",
                        f"Contains {delegation_tools} -- only T5 orchestrator agents "
                        f"may have Agent/Task tool access (P-003 violation). "
                        f"Fix: remove {delegation_tools} from tools list, or set "
                        f"tool_tier: T5 in {gov_path.name} with documented justification.",
                    )
                )

        if result.errors:
            result.status = "fail"
        elif result.warnings:
            result.status = "pass_with_warnings"
        else:
            result.status = "pass"

        return result

    def _validate_skill_file(self, fp: Path, repo_root: Path) -> FrontmatterFileResult:
        """Validate a single SKILL.md file.

        Args:
            fp: Path to the SKILL.md file.
            repo_root: Repository root for computing relative path.

        Returns:
            FrontmatterFileResult with full validation outcome.
        """
        result = FrontmatterFileResult(
            path=fp,
            file_type="skill",
            relative_path=str(fp.relative_to(repo_root)),
        )
        raw_text, fm, error = self._extract_frontmatter(fp)

        if error is not None:
            result.status = "parse_error"
            result.errors.append(("(file)", "parse_error", error))
            return result

        if raw_text is None or fm is None:
            result.status = "no_frontmatter"
            return result

        result.frontmatter = fm

        # JSON Schema validation
        for field_path, constraint, val in self._schema_errors(fm, self._skill_schema):
            result.errors.append((field_path, constraint, val))

        # Semantic: name must match parent directory name
        expected_name = fp.parent.name
        actual_name = fm.get("name", expected_name)
        if actual_name.lower() != expected_name:
            result.errors.append(
                (
                    "name",
                    "name_matches_directory",
                    f"'{actual_name}' (expected '{expected_name}')",
                )
            )

        # Semantic: 'tools' used instead of 'allowed-tools'
        if "tools" in fm and "allowed-tools" not in fm:
            result.errors.append(
                (
                    "tools",
                    "wrong_field_name",
                    f"Skills use 'allowed-tools', not 'tools'. Current value: '{fm['tools']}'",
                )
            )

        # Semantic: multiline description indicator
        if raw_text and _MULTILINE_INDICATOR_RE.search(raw_text):
            result.errors.append(
                (
                    "description",
                    "multiline_indicator",
                    "Uses YAML multiline indicator (> or |) -- Claude Code skill indexer may misparse",
                )
            )

        # Semantic: XML angle brackets in description
        desc = fm.get("description", "")
        if isinstance(desc, str) and _XML_TAG_RE.search(desc):
            result.errors.append(
                (
                    "description",
                    "xml_angle_brackets",
                    "Contains XML angle brackets -- potential prompt injection risk",
                )
            )

        # Semantic: description maxLength for skills (1024 chars)
        if isinstance(desc, str) and len(desc) > 1024:
            result.errors.append(
                (
                    "description",
                    "maxLength",
                    f"Length {len(desc)} exceeds 1024 char limit",
                )
            )

        # Semantic: unrecognized fields -> warning
        unknown = set(fm.keys()) - _SKILL_KNOWN_FIELDS
        if unknown:
            result.warnings.append(
                (
                    "(root)",
                    "unrecognized_fields",
                    f"Jerry-specific fields not recognized by Claude Code: {sorted(unknown)}",
                )
            )

        if result.errors:
            result.status = "fail"
        elif result.warnings:
            result.status = "pass_with_warnings"
        else:
            result.status = "pass"

        return result
