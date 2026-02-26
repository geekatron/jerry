# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
AgentConfigResolver - Agent definition discovery, composition, and validation.

Encapsulates the full agent configuration pipeline:
1. Discover agent .md files under skills/*/agents/
2. Extract YAML frontmatter via YamlFrontmatter
3. Deep merge with base defaults
4. Substitute ${jerry.*} config variables via LayeredConfigAdapter
5. Validate against JSON Schema

This adapter lives within the existing configuration bounded context.
No new bounded contexts are created.

References:
    - PROJ-012: Agent Configuration Extraction & Schema Enforcement
    - H-05: Uses uv run for all Python execution
    - H-07: Infrastructure adapter (may import domain + external libs)
"""

from __future__ import annotations

import copy
import json
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml
from jsonschema import Draft202012Validator

from src.infrastructure.adapters.configuration.layered_config_adapter import (
    LayeredConfigAdapter,
)

# Pattern for ${jerry.*} config variable references
_CONFIG_VAR_RE = re.compile(r"\$\{(jerry\.[a-zA-Z0-9_.]+)\}")


@dataclass(frozen=True)
class AgentInfo:
    """Summary information about a discovered agent.

    Attributes:
        name: Agent name from frontmatter.
        skill: Parent skill directory name.
        file_path: Absolute path to the agent .md file.
        model: Model tier (opus/sonnet/haiku).
        cognitive_mode: Agent cognitive mode.
        version: Agent version string.
    """

    name: str
    skill: str
    file_path: str
    model: str
    cognitive_mode: str
    version: str


@dataclass(frozen=True)
class ComposeResult:
    """Result of composing one agent to a file.

    Attributes:
        agent_name: Name of the composed agent.
        source_path: Path to the original agent definition.
        output_path: Path to the written output file.
        success: Whether composition succeeded.
        error: Error message if composition failed.
    """

    agent_name: str
    source_path: str
    output_path: str
    success: bool
    error: str | None = None


@dataclass
class ValidationResult:
    """Result of schema validation for one agent.

    Attributes:
        agent_name: Name of the validated agent.
        file_path: Path to the agent file.
        is_valid: Whether the agent passed validation.
        errors: List of validation error messages.
        yaml_error: YAML parse error message, if any.
    """

    agent_name: str
    file_path: str
    is_valid: bool
    errors: list[str] = field(default_factory=list)
    yaml_error: str | None = None


class AgentConfigResolver:
    """Resolves, composes, and validates agent configurations.

    Follows the existing LayeredConfigAdapter precedence chain.
    Agent frontmatter overrides base defaults. Config variables
    are substituted from the LayeredConfigAdapter.

    Attributes:
        _config: LayeredConfigAdapter for ${jerry.*} variable resolution.
    """

    def __init__(self, config: LayeredConfigAdapter | None = None) -> None:
        """Initialize the resolver.

        Args:
            config: LayeredConfigAdapter for config variable substitution.
                If None, config variables are not substituted.
        """
        self._config = config

    def discover_agents(self, skills_dir: str) -> list[AgentInfo]:
        """Discover all agent definition files.

        Scans skills/*/agents/*.md, excluding templates, READMEs, and extensions.

        Args:
            skills_dir: Path to the skills directory.

        Returns:
            Sorted list of AgentInfo objects.
        """
        skills_path = Path(skills_dir)
        if not skills_path.is_dir():
            return []

        agents: list[AgentInfo] = []
        for agent_file in sorted(skills_path.glob("*/agents/*.md")):
            if agent_file.name in ("README.md", "AGENTS.md"):
                continue
            if "TEMPLATE" in agent_file.name or "EXTENSION" in agent_file.name:
                continue

            frontmatter = self._extract_frontmatter(agent_file)
            if frontmatter is None:
                continue

            skill = agent_file.parent.parent.name
            agents.append(
                AgentInfo(
                    name=frontmatter.get("name", agent_file.stem),
                    skill=skill,
                    file_path=str(agent_file),
                    model=frontmatter.get("model", "unknown"),
                    cognitive_mode=frontmatter.get("identity", {}).get("cognitive_mode", "unknown"),
                    version=frontmatter.get("version", "0.0.0"),
                )
            )

        return agents

    def compose_agent_config(
        self,
        agent_file: Path,
        defaults: dict[str, Any],
    ) -> dict[str, Any]:
        """Compose a full agent config by merging defaults + frontmatter + config vars.

        Args:
            agent_file: Path to the agent .md file.
            defaults: Base defaults dictionary.

        Returns:
            Fully composed configuration dictionary.

        Raises:
            ValueError: If the agent file has no valid YAML frontmatter.
        """
        frontmatter = self._extract_frontmatter(agent_file)
        if frontmatter is None:
            msg = f"No valid YAML frontmatter in {agent_file}"
            raise ValueError(msg)

        # Deep merge: defaults + agent overrides
        composed = self._deep_merge(copy.deepcopy(defaults), frontmatter)

        # Substitute config variables
        if self._config is not None:
            composed = self._substitute_config_vars(composed)

        return composed

    def validate_agent(
        self,
        agent_file: Path,
        defaults: dict[str, Any],
        validator: Draft202012Validator,
    ) -> ValidationResult:
        """Validate a single agent's composed config against the schema.

        Args:
            agent_file: Path to the agent .md file.
            defaults: Base defaults dictionary.
            validator: JSON Schema validator instance.

        Returns:
            ValidationResult with errors if any.
        """
        agent_name = agent_file.stem
        file_path = str(agent_file)

        # Extract frontmatter
        frontmatter = self._extract_frontmatter(agent_file)
        if frontmatter is None:
            return ValidationResult(
                agent_name=agent_name,
                file_path=file_path,
                is_valid=False,
                yaml_error="No valid YAML frontmatter found",
            )

        # Compose
        composed = self._deep_merge(copy.deepcopy(defaults), frontmatter)
        if self._config is not None:
            composed = self._substitute_config_vars(composed)

        # Validate
        errors = [
            f"{'.'.join(str(p) for p in e.absolute_path) or '(root)'}: {e.message}"
            for e in validator.iter_errors(composed)
        ]

        return ValidationResult(
            agent_name=composed.get("name", agent_name),
            file_path=file_path,
            is_valid=len(errors) == 0,
            errors=errors,
        )

    def validate_all(
        self,
        skills_dir: str,
        schema_path: str,
        defaults_path: str,
    ) -> list[ValidationResult]:
        """Validate all agents against the schema.

        Args:
            skills_dir: Path to the skills directory.
            schema_path: Path to the JSON Schema file.
            defaults_path: Path to the base defaults YAML.

        Returns:
            List of ValidationResult for each agent.
        """
        schema = self._load_json(schema_path)
        defaults = self._load_yaml(defaults_path)
        validator = Draft202012Validator(schema)

        results: list[ValidationResult] = []
        skills_path = Path(skills_dir)
        for agent_file in sorted(skills_path.glob("*/agents/*.md")):
            if agent_file.name in ("README.md", "AGENTS.md"):
                continue
            if "TEMPLATE" in agent_file.name or "EXTENSION" in agent_file.name:
                continue
            if not self._has_frontmatter(agent_file):
                continue

            results.append(self.validate_agent(agent_file, defaults, validator))

        return results

    def validate_single(
        self,
        skills_dir: str,
        agent_name: str,
        schema_path: str,
        defaults_path: str,
    ) -> list[ValidationResult]:
        """Validate a single agent by name.

        Args:
            skills_dir: Path to the skills directory.
            agent_name: Agent name to validate.
            schema_path: Path to the JSON Schema file.
            defaults_path: Path to the base defaults YAML.

        Returns:
            List with one ValidationResult, or a not-found result.
        """
        agent_file = self.find_agent_file(skills_dir, agent_name)
        if agent_file is None:
            return [
                ValidationResult(
                    agent_name=agent_name,
                    file_path="(not found)",
                    is_valid=False,
                    errors=[f"Agent '{agent_name}' not found"],
                )
            ]
        schema = self._load_json(schema_path)
        defaults = self._load_yaml(defaults_path)
        validator = Draft202012Validator(schema)
        return [self.validate_agent(agent_file, defaults, validator)]

    def load_defaults(self, defaults_path: str) -> dict[str, Any]:
        """Load base defaults YAML.

        Args:
            defaults_path: Path to the defaults YAML file.

        Returns:
            Parsed defaults dict.
        """
        return self._load_yaml(defaults_path)

    def find_agent_file(self, skills_dir: str, agent_name: str) -> Path | None:
        """Find an agent file by name.

        Args:
            skills_dir: Path to the skills directory.
            agent_name: Agent name to find.

        Returns:
            Path to the agent file, or None if not found.
        """
        skills_path = Path(skills_dir)
        for agent_file in skills_path.glob("*/agents/*.md"):
            if agent_file.stem == agent_name:
                return agent_file
        return None

    def _extract_frontmatter_and_body(self, agent_file: Path) -> tuple[dict[str, Any], str] | None:
        """Extract YAML frontmatter and markdown body from an agent file.

        Args:
            agent_file: Path to the agent .md file.

        Returns:
            Tuple of (frontmatter_dict, body_string), or None if no frontmatter.
        """
        try:
            content = agent_file.read_text(encoding="utf-8")
        except OSError:
            return None

        if not content.startswith("---"):
            return None

        try:
            end_idx = content.index("---", 3)
        except ValueError:
            return None

        yaml_str = content[3:end_idx]
        try:
            data = yaml.safe_load(yaml_str)
        except yaml.YAMLError:
            return None

        if not isinstance(data, dict):
            return None

        # Body is everything after the closing ---
        body = content[end_idx + 3 :].lstrip("\n")
        return data, body

    def compose_agent_to_file(
        self,
        agent_file: Path,
        defaults: dict[str, Any],
        output_dir: Path,
    ) -> ComposeResult:
        """Compose a single agent and write to output directory.

        Merges defaults with agent frontmatter, then writes a new .md file
        with the composed YAML frontmatter and the original markdown body.

        Args:
            agent_file: Path to the source agent .md file.
            defaults: Base defaults dictionary.
            output_dir: Directory to write the composed file.

        Returns:
            ComposeResult indicating success or failure.
        """
        agent_name = agent_file.stem
        output_path = output_dir / f"{agent_name}.md"

        try:
            result = self._extract_frontmatter_and_body(agent_file)
            if result is None:
                return ComposeResult(
                    agent_name=agent_name,
                    source_path=str(agent_file),
                    output_path=str(output_path),
                    success=False,
                    error="No valid YAML frontmatter found",
                )

            frontmatter, body = result

            # Deep merge: defaults + agent overrides
            composed = self._deep_merge(copy.deepcopy(defaults), frontmatter)

            # Substitute config variables
            if self._config is not None:
                composed = self._substitute_config_vars(composed)

            # Write composed file: ---\n{yaml}\n---\n{body}
            yaml_str = yaml.dump(composed, default_flow_style=False, sort_keys=False)
            content = f"---\n{yaml_str}---\n{body}"
            output_path.write_text(content, encoding="utf-8")

            return ComposeResult(
                agent_name=composed.get("name", agent_name),
                source_path=str(agent_file),
                output_path=str(output_path),
                success=True,
            )

        except Exception as e:
            return ComposeResult(
                agent_name=agent_name,
                source_path=str(agent_file),
                output_path=str(output_path),
                success=False,
                error=str(e),
            )

    def compose_all_to_dir(
        self,
        skills_dir: str,
        defaults_path: str,
        output_dir: str,
        clean: bool = False,
        agent_name: str | None = None,
    ) -> list[ComposeResult]:
        """Compose agents and write to output directory.

        Args:
            skills_dir: Path to the skills directory.
            defaults_path: Path to the base defaults YAML file.
            output_dir: Directory to write composed files.
            clean: If True, remove existing .md files before writing.
            agent_name: If specified, compose only this agent.

        Returns:
            List of ComposeResult for each agent processed.
        """
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        # Clean: remove existing .md files (preserve non-md files)
        if clean:
            for f in output_path.glob("*.md"):
                f.unlink()

        defaults = self._load_yaml(defaults_path)

        # Single agent mode
        if agent_name is not None:
            agent_file = self.find_agent_file(skills_dir, agent_name)
            if agent_file is None:
                return [
                    ComposeResult(
                        agent_name=agent_name,
                        source_path="(not found)",
                        output_path=str(output_path / f"{agent_name}.md"),
                        success=False,
                        error=f"Agent '{agent_name}' not found",
                    )
                ]
            return [self.compose_agent_to_file(agent_file, defaults, output_path)]

        # All agents mode
        skills_path = Path(skills_dir)
        results: list[ComposeResult] = []
        for agent_file in sorted(skills_path.glob("*/agents/*.md")):
            if agent_file.name in ("README.md", "AGENTS.md"):
                continue
            if "TEMPLATE" in agent_file.name or "EXTENSION" in agent_file.name:
                continue
            if not self._has_frontmatter(agent_file):
                continue

            results.append(self.compose_agent_to_file(agent_file, defaults, output_path))

        return results

    def _extract_frontmatter(self, agent_file: Path) -> dict[str, Any] | None:
        """Extract YAML frontmatter from an agent file.

        Args:
            agent_file: Path to the agent .md file.

        Returns:
            Parsed YAML dict, or None if no frontmatter.
        """
        try:
            content = agent_file.read_text(encoding="utf-8")
        except OSError:
            return None

        if not content.startswith("---"):
            return None

        try:
            end_idx = content.index("---", 3)
        except ValueError:
            return None

        yaml_str = content[3:end_idx]
        try:
            data = yaml.safe_load(yaml_str)
        except yaml.YAMLError:
            return None

        if not isinstance(data, dict):
            return None

        return data

    def _has_frontmatter(self, agent_file: Path) -> bool:
        """Check if an agent file has YAML frontmatter.

        Args:
            agent_file: Path to the agent .md file.

        Returns:
            True if the file starts with ---.
        """
        try:
            content = agent_file.read_text(encoding="utf-8")
            return content.startswith("---")
        except OSError:
            return False

    @staticmethod
    def _deep_merge(base: dict[str, Any], override: dict[str, Any]) -> dict[str, Any]:
        """Deep merge two dicts. Override wins for scalars. Arrays replace entirely.

        Args:
            base: Base dictionary (modified in place).
            override: Override dictionary.

        Returns:
            Merged dictionary (same reference as base).
        """
        for key, value in override.items():
            if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                AgentConfigResolver._deep_merge(base[key], value)
            else:
                base[key] = value
        return base

    def _substitute_config_vars(self, data: Any) -> Any:
        """Recursively substitute ${jerry.*} config variables.

        Args:
            data: Data structure to process.

        Returns:
            Data with config variables substituted.
        """
        if isinstance(data, str):
            return self._replace_vars_in_string(data)
        if isinstance(data, dict):
            return {k: self._substitute_config_vars(v) for k, v in data.items()}
        if isinstance(data, list):
            return [self._substitute_config_vars(item) for item in data]
        return data

    def _replace_vars_in_string(self, value: str) -> str:
        """Replace ${jerry.*} tokens in a string with config values.

        Args:
            value: String potentially containing ${jerry.*} tokens.

        Returns:
            String with tokens replaced. Unresolved tokens are left as-is.
        """
        config = self._config
        if config is None:
            return value

        def replacer(match: re.Match[str]) -> str:
            config_key = match.group(1)
            resolved = config.get(config_key)
            if resolved is not None:
                return str(resolved)
            return match.group(0)

        return _CONFIG_VAR_RE.sub(replacer, value)

    @staticmethod
    def _load_json(path: str) -> dict[str, Any]:
        """Load a JSON file.

        Args:
            path: Path to the JSON file.

        Returns:
            Parsed JSON dict.
        """
        with open(path, encoding="utf-8") as f:
            return json.load(f)

    @staticmethod
    def _load_yaml(path: str) -> dict[str, Any]:
        """Load a YAML file.

        Args:
            path: Path to the YAML file.

        Returns:
            Parsed YAML dict, or empty dict if file doesn't exist.
        """
        try:
            with open(path, encoding="utf-8") as f:
                data = yaml.safe_load(f)
                return data if isinstance(data, dict) else {}
        except (OSError, yaml.YAMLError):
            return {}
