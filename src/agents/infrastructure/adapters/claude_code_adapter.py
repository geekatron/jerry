# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
ClaudeCodeAdapter - Generates Claude Code agent files from canonical source.

Produces:
- {agent}.md: Official Claude Code YAML frontmatter + system prompt body
- {agent}.governance.yaml: CI validation governance metadata

References:
    - ADR-PROJ010-003: LLM Portability Architecture
    - agent-development-standards.md: H-34 agent definition standards
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

import yaml

from src.agents.application.ports.vendor_adapter import IVendorAdapter
from src.agents.domain.entities.canonical_agent import CanonicalAgent
from src.agents.domain.entities.generated_artifact import GeneratedArtifact
from src.agents.domain.services.prompt_transformer import PromptTransformer
from src.agents.domain.services.tool_mapper import ToolMapper
from src.agents.domain.value_objects.body_format import BodyFormat
from src.agents.domain.value_objects.model_tier import ModelTier
from src.agents.domain.value_objects.tool_tier import ToolTier
from src.agents.domain.value_objects.vendor_target import VendorTarget


class ClaudeCodeAdapter(IVendorAdapter):
    """Generates Claude Code native agent files from canonical source.

    Produces two files per agent:
    1. {name}.md — YAML frontmatter (12 official fields) + system prompt body
    2. {name}.governance.yaml — Machine-readable governance metadata

    Attributes:
        _tool_mapper: Maps abstract tool names to Claude Code native names.
        _prompt_transformer: Transforms prompt body between formats.
        _skills_dir: Path to the skills/ directory for output.
    """

    def __init__(
        self,
        tool_mapper: ToolMapper,
        prompt_transformer: PromptTransformer,
        skills_dir: Path,
    ) -> None:
        """Initialize with dependencies.

        Args:
            tool_mapper: Configured tool/model name mapper.
            prompt_transformer: Prompt body format transformer.
            skills_dir: Path to skills/ for output file placement.
        """
        self._tool_mapper = tool_mapper
        self._prompt_transformer = prompt_transformer
        self._skills_dir = skills_dir

    @property
    def vendor(self) -> VendorTarget:
        """Return the vendor target."""
        return VendorTarget.CLAUDE_CODE

    def generate(self, agent: CanonicalAgent) -> list[GeneratedArtifact]:
        """Generate Claude Code files from a canonical agent.

        Args:
            agent: Parsed canonical agent definition.

        Returns:
            List of two GeneratedArtifact instances (md + governance.yaml).
        """
        agents_dir = self._skills_dir / agent.skill / "agents"

        # 1. Build .md file
        md_content = self._build_md(agent)
        md_artifact = GeneratedArtifact(
            path=agents_dir / f"{agent.name}.md",
            content=md_content,
            vendor=VendorTarget.CLAUDE_CODE,
            source_agent=agent.name,
            artifact_type="agent_definition",
        )

        # 2. Build .governance.yaml file
        gov_content = self._build_governance_yaml(agent)
        gov_artifact = GeneratedArtifact(
            path=agents_dir / f"{agent.name}.governance.yaml",
            content=gov_content,
            vendor=VendorTarget.CLAUDE_CODE,
            source_agent=agent.name,
            artifact_type="governance",
        )

        return [md_artifact, gov_artifact]

    def extract(
        self,
        agent_md_path: str,
        governance_yaml_path: str | None = None,
    ) -> CanonicalAgent:
        """Extract a canonical agent from existing Claude Code files.

        Args:
            agent_md_path: Path to existing .md agent file.
            governance_yaml_path: Path to existing .governance.yaml file.

        Returns:
            Extracted CanonicalAgent entity.
        """
        md_path = Path(agent_md_path)
        md_content = md_path.read_text(encoding="utf-8")

        # Parse frontmatter and body
        frontmatter, body = self._parse_md(md_content)

        # Parse governance YAML if available
        gov_data: dict[str, Any] = {}
        if governance_yaml_path:
            gov_path = Path(governance_yaml_path)
            if gov_path.exists():
                gov_content = gov_path.read_text(encoding="utf-8")
                gov_data = yaml.safe_load(gov_content) or {}

        # Determine skill from file path
        # Expected: skills/{skill}/agents/{name}.md
        skill = md_path.parent.parent.name

        # Strip <agent> wrapper (and corrupted "agent>" variant)
        body = self._strip_agent_wrapper(body)

        # Detect body format (XML or markdown)
        body_format = self._detect_body_format(body)

        # Convert body to canonical markdown headings
        if body_format == BodyFormat.XML:
            canonical_body = self._prompt_transformer.from_xml(body)
        else:
            canonical_body = body

        # Substitute vendor tool names to abstract names
        canonical_body = self._tool_mapper.substitute_tool_names_in_text(
            canonical_body, VendorTarget.CLAUDE_CODE, reverse=True
        )

        # Map vendor model name to abstract tier
        model_name = frontmatter.get("model", "sonnet")
        model_tier = ModelTier.from_vendor_model("claude_code", model_name)

        # Map vendor tool names to abstract names
        vendor_tools = self._parse_tools_from_frontmatter(frontmatter)
        abstract_tools = self._tool_mapper.reverse_map_tools(vendor_tools, VendorTarget.CLAUDE_CODE)

        # Extract MCP servers
        mcp_data = frontmatter.get("mcpServers", {})
        mcp_servers = [k for k, v in mcp_data.items() if v]

        # Determine forbidden tools
        forbidden_tools: list[str] = []
        if gov_data.get("tool_tier", "T1") != "T5":
            forbidden_tools = ["agent_delegate"]

        # Build constitution from governance data
        constitution = gov_data.get("constitution", {})
        capabilities = gov_data.get("capabilities", {})
        if "forbidden_actions" in capabilities and "forbidden_actions" not in constitution:
            constitution["forbidden_actions"] = capabilities["forbidden_actions"]

        # Ensure constitutional triplet (H-35 compliance normalization)
        constitution = self._ensure_constitutional_triplet(constitution)

        return CanonicalAgent(
            name=frontmatter.get("name", md_path.stem),
            version=gov_data.get("version", "1.0.0"),
            description=frontmatter.get("description", ""),
            skill=skill,
            identity=gov_data.get("identity", {}),
            persona=gov_data.get("persona", {}),
            model_tier=model_tier,
            model_preferences=[],
            native_tools=abstract_tools,
            mcp_servers=mcp_servers,
            forbidden_tools=forbidden_tools,
            tool_tier=ToolTier.from_string(gov_data.get("tool_tier", "T1")),
            guardrails=gov_data.get("guardrails", {}),
            output=gov_data.get("output", {}),
            constitution=constitution,
            validation=gov_data.get("validation", {}),
            portability=gov_data.get(
                "portability",
                {
                    "enabled": True,
                    "minimum_context_window": 128000,
                    "reasoning_strategy": "adaptive",
                    "body_format": body_format.value,
                },
            ),
            enforcement=gov_data.get("enforcement", {}),
            session_context=gov_data.get("session_context", {}),
            prior_art=gov_data.get("prior_art", []),
            prompt_body=canonical_body,
            body_format=body_format,
        )

    # -------------------------------------------------------------------------
    # MD file generation
    # -------------------------------------------------------------------------

    def _build_md(self, agent: CanonicalAgent) -> str:
        """Build the .md file content (frontmatter + body).

        Args:
            agent: Canonical agent definition.

        Returns:
            Complete .md file content string.
        """
        frontmatter = self._build_frontmatter(agent)
        body = self._build_body(agent)
        return f"---\n{frontmatter}---\n{body}"

    def _build_frontmatter(self, agent: CanonicalAgent) -> str:
        """Build the YAML frontmatter with only Claude Code official fields.

        Args:
            agent: Canonical agent definition.

        Returns:
            YAML frontmatter string (without --- delimiters).
        """
        fm: dict[str, Any] = {}

        # name (required)
        fm["name"] = agent.name

        # description (required) — single line
        fm["description"] = agent.description

        # model
        model_name = self._tool_mapper.map_model(agent.model_tier, VendorTarget.CLAUDE_CODE)
        if model_name:
            fm["model"] = model_name

        # tools — map abstract names to Claude Code native names
        # Exclude agent_delegate from tools list (workers must not have Task)
        tools_to_map = [t for t in agent.native_tools if t != "agent_delegate"]
        vendor_tools = self._tool_mapper.map_tools(tools_to_map, VendorTarget.CLAUDE_CODE)
        if vendor_tools:
            fm["tools"] = ", ".join(vendor_tools)

        # mcpServers
        if agent.mcp_servers:
            mcp: dict[str, bool] = {}
            for server in agent.mcp_servers:
                mcp[server] = True
            fm["mcpServers"] = mcp

        return yaml.dump(
            fm,
            default_flow_style=False,
            sort_keys=False,
            allow_unicode=True,
            width=200,
        )

    def _build_body(self, agent: CanonicalAgent) -> str:
        """Build the system prompt body with vendor-specific tool names.

        Args:
            agent: Canonical agent definition.

        Returns:
            Transformed system prompt body string.
        """
        # Transform body to target format
        body = self._prompt_transformer.to_format(agent.prompt_body, agent.body_format)

        # Substitute abstract tool names with Claude Code names
        body = self._tool_mapper.substitute_tool_names_in_text(body, VendorTarget.CLAUDE_CODE)

        # Wrap XML-format bodies in <agent> tags
        if agent.body_format == BodyFormat.XML:
            body = "<agent>\n\n" + body.rstrip("\n") + "\n\n</agent>\n"

        return body

    # -------------------------------------------------------------------------
    # Governance YAML generation
    # -------------------------------------------------------------------------

    def _build_governance_yaml(self, agent: CanonicalAgent) -> str:
        """Build the .governance.yaml file content.

        Args:
            agent: Canonical agent definition.

        Returns:
            Complete .governance.yaml file content string.
        """
        gov: dict[str, Any] = {}

        # Header comment
        header = (
            f"# Governance metadata for {agent.name}\n"
            f"# Validated by: docs/schemas/agent-governance-v1.schema.json\n"
            f"# Runtime config: {agent.name}.md\n\n"
        )

        gov["version"] = agent.version
        gov["tool_tier"] = agent.tool_tier.value
        gov["identity"] = agent.identity

        if agent.persona:
            gov["persona"] = agent.persona

        if agent.guardrails:
            gov["guardrails"] = agent.guardrails

        if agent.output:
            # Copy output but omit formats (moved to capabilities)
            output_copy = {k: v for k, v in agent.output.items() if k != "formats"}
            if output_copy:
                gov["output"] = output_copy

        # Constitution without forbidden_actions (moved to capabilities)
        constitution_copy = {
            k: v for k, v in agent.constitution.items() if k != "forbidden_actions"
        }
        if constitution_copy:
            gov["constitution"] = constitution_copy

        if agent.validation:
            gov["validation"] = agent.validation

        if agent.prior_art:
            gov["prior_art"] = agent.prior_art

        if agent.enforcement:
            gov["enforcement"] = agent.enforcement

        if agent.session_context:
            gov["session_context"] = agent.session_context

        # Capabilities with forbidden_actions and output_formats
        capabilities: dict[str, Any] = {}
        if agent.constitution.get("forbidden_actions"):
            capabilities["forbidden_actions"] = agent.constitution["forbidden_actions"]
        if agent.output.get("formats"):
            capabilities["output_formats"] = agent.output["formats"]
        if capabilities:
            gov["capabilities"] = capabilities

        yaml_content = yaml.dump(
            gov,
            default_flow_style=False,
            sort_keys=False,
            allow_unicode=True,
            width=100,
        )

        return header + yaml_content

    # -------------------------------------------------------------------------
    # Parsing helpers (for extract)
    # -------------------------------------------------------------------------

    def _parse_md(self, content: str) -> tuple[dict[str, Any], str]:
        """Parse an .md file into frontmatter dict and body string.

        Args:
            content: Full .md file content.

        Returns:
            Tuple of (frontmatter_dict, body_string).
        """
        if not content.startswith("---"):
            return {}, content

        # Find closing ---
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

    def _parse_tools_from_frontmatter(self, frontmatter: dict[str, Any]) -> list[str]:
        """Extract tool names from Claude Code frontmatter.

        Args:
            frontmatter: Parsed YAML frontmatter dict.

        Returns:
            List of vendor-specific tool names.
        """
        tools = frontmatter.get("tools", "")
        if isinstance(tools, str):
            return [t.strip() for t in tools.split(",") if t.strip()]
        if isinstance(tools, list):
            return tools
        return []

    def _ensure_constitutional_triplet(self, constitution: dict[str, Any]) -> dict[str, Any]:
        """Ensure constitutional triplet (P-003, P-020, P-022) per H-35.

        Adds missing required principles and forbidden actions during
        extract to close pre-existing compliance gaps.

        Args:
            constitution: Constitution dict from governance data.

        Returns:
            Constitution dict with triplet entries guaranteed.
        """
        # Ensure principles_applied has all three
        required_principles = {
            "P-003": "P-003: No Recursive Subagents (Hard)",
            "P-020": "P-020: User Authority (Hard)",
            "P-022": "P-022: No Deception (Hard)",
        }
        principles = constitution.get("principles_applied", [])
        for code, full_text in required_principles.items():
            if not any(code in p for p in principles):
                principles.append(full_text)
        constitution["principles_applied"] = principles

        # Ensure forbidden_actions has all three
        required_actions = {
            "P-003": "Spawn recursive subagents (P-003)",
            "P-020": "Override user decisions (P-020)",
            "P-022": "Misrepresent capabilities or confidence (P-022)",
        }
        actions = constitution.get("forbidden_actions", [])
        for code, full_text in required_actions.items():
            if not any(code in a for a in actions):
                actions.append(full_text)
        constitution["forbidden_actions"] = actions

        return constitution

    def _strip_agent_wrapper(self, body: str) -> str:
        """Strip <agent>...</agent> wrapper from body content.

        Handles both proper <agent> tags and the corrupted "agent>"
        variant (missing < prefix) from PR #87 transform.

        Args:
            body: Raw body content from .md file.

        Returns:
            Body with <agent> wrapper stripped.
        """
        stripped = body.strip()

        # Strip proper <agent> wrapper
        if stripped.startswith("<agent>"):
            stripped = stripped[len("<agent>") :].lstrip("\n")
        # Strip corrupted "agent>" variant (missing <)
        elif stripped.startswith("agent>"):
            stripped = stripped[len("agent>") :].lstrip("\n")

        # Strip closing </agent> tag
        if stripped.rstrip().endswith("</agent>"):
            stripped = stripped.rstrip()
            stripped = stripped[: -len("</agent>")].rstrip("\n")

        return stripped + "\n"

    def _detect_body_format(self, body: str) -> BodyFormat:
        """Detect whether body uses XML tags or markdown headings.

        Args:
            body: System prompt body content.

        Returns:
            Detected BodyFormat.
        """
        # Check for XML-style tags
        xml_pattern = re.compile(r"<[a-z_]+>")
        md_heading_pattern = re.compile(r"^## ", re.MULTILINE)

        xml_count = len(xml_pattern.findall(body))
        md_count = len(md_heading_pattern.findall(body))

        if xml_count > md_count:
            return BodyFormat.XML
        return BodyFormat.MARKDOWN


# =========================================================================
# Factory functions (composition root for agents bounded context)
# =========================================================================


def _get_skills_dir() -> Path:
    """Resolve the skills directory path.

    Returns:
        Path to the skills/ directory.
    """
    import os

    project_root = os.environ.get("CLAUDE_PROJECT_DIR", "")
    if project_root:
        return Path(project_root) / "skills"
    return Path.cwd() / "skills"


def _get_schema_path() -> Path:
    """Resolve the canonical schema path.

    Returns:
        Path to agent-canonical-v1.schema.json.
    """
    import os

    project_root = os.environ.get("CLAUDE_PROJECT_DIR", "")
    if project_root:
        base = Path(project_root)
    else:
        base = Path.cwd()
    return base / "docs" / "schemas" / "agent-canonical-v1.schema.json"


def _create_tool_mapper() -> ToolMapper:
    """Create a ToolMapper from the mappings.yaml file.

    Returns:
        Configured ToolMapper instance.
    """
    mappings_path = Path(__file__).parent.parent / "mappings.yaml"
    mappings_content = mappings_path.read_text(encoding="utf-8")
    mappings = yaml.safe_load(mappings_content)
    return ToolMapper.from_mappings(mappings)


def _create_claude_code_adapter() -> ClaudeCodeAdapter:
    """Create a fully configured ClaudeCodeAdapter.

    Returns:
        ClaudeCodeAdapter with all dependencies.
    """
    tool_mapper = _create_tool_mapper()
    prompt_transformer = PromptTransformer()
    skills_dir = _get_skills_dir()
    return ClaudeCodeAdapter(
        tool_mapper=tool_mapper,
        prompt_transformer=prompt_transformer,
        skills_dir=skills_dir,
    )


def create_agents_build_handler() -> Any:
    """Create a fully configured BuildAgentsCommandHandler.

    Returns:
        BuildAgentsCommandHandler ready for use.
    """
    from src.agents.application.handlers.commands.build_agents_command_handler import (
        BuildAgentsCommandHandler,
    )
    from src.agents.infrastructure.persistence.filesystem_agent_repository import (
        FilesystemAgentRepository,
    )

    skills_dir = _get_skills_dir()
    repository = FilesystemAgentRepository(skills_dir)
    adapter = _create_claude_code_adapter()

    return BuildAgentsCommandHandler(
        repository=repository,
        adapters={"claude_code": adapter},
    )


def create_agents_extract_handler() -> Any:
    """Create a fully configured ExtractCanonicalCommandHandler.

    Returns:
        ExtractCanonicalCommandHandler ready for use.
    """
    from src.agents.application.handlers.commands.extract_canonical_command_handler import (
        ExtractCanonicalCommandHandler,
    )

    skills_dir = _get_skills_dir()
    adapter = _create_claude_code_adapter()

    return ExtractCanonicalCommandHandler(
        adapters={"claude_code": adapter},
        skills_dir=skills_dir,
    )


def create_agents_validate_handler() -> Any:
    """Create a fully configured ValidateAgentsQueryHandler.

    Returns:
        ValidateAgentsQueryHandler ready for use.
    """
    from src.agents.application.handlers.queries.validate_agents_query_handler import (
        ValidateAgentsQueryHandler,
    )
    from src.agents.infrastructure.persistence.filesystem_agent_repository import (
        FilesystemAgentRepository,
    )

    skills_dir = _get_skills_dir()
    repository = FilesystemAgentRepository(skills_dir)
    schema_path = _get_schema_path()

    return ValidateAgentsQueryHandler(
        repository=repository,
        schema_path=schema_path,
    )


def create_agents_list_handler() -> Any:
    """Create a fully configured ListAgentsQueryHandler.

    Returns:
        ListAgentsQueryHandler ready for use.
    """
    from src.agents.application.handlers.queries.list_agents_query_handler import (
        ListAgentsQueryHandler,
    )
    from src.agents.infrastructure.persistence.filesystem_agent_repository import (
        FilesystemAgentRepository,
    )

    skills_dir = _get_skills_dir()
    repository = FilesystemAgentRepository(skills_dir)

    return ListAgentsQueryHandler(repository=repository)
