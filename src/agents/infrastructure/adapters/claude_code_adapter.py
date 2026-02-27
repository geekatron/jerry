# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
ClaudeCodeAdapter - Generates Claude Code agent files from canonical source.

Produces a single file per agent:
- {agent}.md: Official Claude Code YAML frontmatter + system prompt body
  (with governance data injected as XML sections in the body)

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
from src.agents.domain.services.governance_section_builder import GovernanceSectionBuilder
from src.agents.domain.services.prompt_transformer import PromptTransformer
from src.agents.domain.services.tool_mapper import ToolMapper
from src.agents.domain.value_objects.body_format import BodyFormat
from src.agents.domain.value_objects.model_tier import ModelTier
from src.agents.domain.value_objects.tool_tier import ToolTier
from src.agents.domain.value_objects.vendor_target import VendorTarget


class ClaudeCodeAdapter(IVendorAdapter):
    """Generates Claude Code native agent files from canonical source.

    Produces a single file per agent:
    - {name}.md — YAML frontmatter (12 official fields) + system prompt body
      (governance data injected as XML sections in the body)

    Attributes:
        _tool_mapper: Maps abstract tool names to Claude Code native names.
        _prompt_transformer: Transforms prompt body between formats.
        _governance_builder: Builds governance markdown sections.
        _skills_dir: Path to the skills/ directory for output.
    """

    def __init__(
        self,
        tool_mapper: ToolMapper,
        prompt_transformer: PromptTransformer,
        skills_dir: Path,
        governance_builder: GovernanceSectionBuilder | None = None,
    ) -> None:
        """Initialize with dependencies.

        Args:
            tool_mapper: Configured tool/model name mapper.
            prompt_transformer: Prompt body format transformer.
            skills_dir: Path to skills/ for output file placement.
            governance_builder: Builder for governance sections (default: new instance).
        """
        self._tool_mapper = tool_mapper
        self._prompt_transformer = prompt_transformer
        self._skills_dir = skills_dir
        self._governance_builder = governance_builder or GovernanceSectionBuilder()

    @property
    def vendor(self) -> VendorTarget:
        """Return the vendor target."""
        return VendorTarget.CLAUDE_CODE

    def generate(self, agent: CanonicalAgent) -> list[GeneratedArtifact]:
        """Generate Claude Code files from a canonical agent.

        Args:
            agent: Parsed canonical agent definition.

        Returns:
            List containing a single GeneratedArtifact (.md file with
            governance data injected into the prompt body).
        """
        agents_dir = self._skills_dir / agent.skill / "agents"

        md_content = self._build_md(agent)
        md_artifact = GeneratedArtifact(
            path=agents_dir / f"{agent.name}.md",
            content=md_content,
            vendor=VendorTarget.CLAUDE_CODE,
            source_agent=agent.name,
            artifact_type="agent_definition",
        )

        return [md_artifact]

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

        # Extract governance from body when no .governance.yaml was found
        if not gov_data:
            gov_data = self._extract_governance_from_body(body, body_format)

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

        Governance sections are appended to the canonical prompt body
        before format transformation, so they become XML tags in the
        final output.

        Args:
            agent: Canonical agent definition.

        Returns:
            Transformed system prompt body string.
        """
        # 1. Start with canonical prompt body (markdown headings)
        canonical_body = agent.prompt_body

        # 2. Append governance sections (also as markdown headings)
        # Governance sections (version, tool_tier, enforcement, portability, prior_art,
        # session_context) are appended AFTER the canonical body content. Rationale:
        # governance metadata is reference data, not behavioral instructions. Keeping it
        # after the primary identity/methodology/guardrails flow preserves the agent's
        # behavioral prompt structure. The GovernanceSectionBuilder only injects fields
        # NOT already present in the body (dedup check), so existing governance prose
        # in the canonical prompt takes precedence over injected metadata.
        # Design decision documented per PROJ-012 adversary review FM-013 (RPN 405).
        governance_sections = self._governance_builder.build(agent, existing_body=canonical_body)
        if governance_sections:
            canonical_body = canonical_body.rstrip("\n") + "\n\n" + governance_sections

        # 3. Transform to target format (e.g., markdown headings -> XML tags)
        body = self._prompt_transformer.to_format(canonical_body, agent.body_format)

        # 4. Substitute abstract tool names with Claude Code names
        body = self._tool_mapper.substitute_tool_names_in_text(body, VendorTarget.CLAUDE_CODE)

        # 5. Wrap XML-format bodies in <agent> tags
        if agent.body_format == BodyFormat.XML:
            body = "<agent>\n\n" + body.rstrip("\n") + "\n\n</agent>\n"

        return body

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

    def _extract_governance_from_body(self, body: str, body_format: BodyFormat) -> dict[str, Any]:
        """Extract governance data from the prompt body when no .governance.yaml exists.

        Parses governance sections that were injected by GovernanceSectionBuilder
        during compose. Supports both XML tag format and markdown heading format.

        Args:
            body: System prompt body content (after agent wrapper stripping).
            body_format: Detected body format (XML or MARKDOWN).

        Returns:
            Dict of governance fields extracted from the body. Empty dict if
            no governance sections are found.
        """
        if body_format == BodyFormat.XML:
            return self._extract_governance_from_xml(body)
        return self._extract_governance_from_markdown(body)

    def _extract_governance_from_xml(self, body: str) -> dict[str, Any]:
        """Extract governance fields from XML-tagged body content.

        Args:
            body: Body with XML tags (e.g., <agent_version>2.3.1</agent_version>).

        Returns:
            Dict of governance fields.
        """
        gov_data: dict[str, Any] = {}

        # Simple string fields
        tag_to_key = {
            "agent_version": "version",
            "tool_tier": "tool_tier",
        }
        for tag, key in tag_to_key.items():
            match = re.search(rf"<{tag}>\s*(.*?)\s*</{tag}>", body, re.DOTALL)
            if match:
                value = match.group(1).strip()
                if not value:
                    continue  # Skip empty tags
                if key == "tool_tier":
                    # Strip label, e.g., "T3 (External)" -> "T3"
                    tier_match = re.match(r"(T\d)", value)
                    if tier_match:
                        value = tier_match.group(1)
                gov_data[key] = value

        # YAML-block fields
        yaml_tags = ["enforcement", "portability", "session_context"]
        for tag in yaml_tags:
            match = re.search(rf"<{tag}>\s*(.*?)\s*</{tag}>", body, re.DOTALL)
            if match:
                content = match.group(1).strip()
                try:
                    parsed = yaml.safe_load(content)
                    if isinstance(parsed, dict):
                        gov_data[tag] = parsed
                except yaml.YAMLError:
                    pass

        # Bullet-list field: prior_art
        match = re.search(r"<prior_art>\s*(.*?)\s*</prior_art>", body, re.DOTALL)
        if match:
            content = match.group(1).strip()
            items = [
                line.lstrip("- ").strip()
                for line in content.split("\n")
                if line.strip().startswith("-")
            ]
            if items:
                gov_data["prior_art"] = items

        return gov_data

    def _extract_governance_from_markdown(self, body: str) -> dict[str, Any]:
        """Extract governance fields from markdown heading body content.

        Args:
            body: Body with ## headings (e.g., ## Agent Version).

        Returns:
            Dict of governance fields.
        """
        gov_data: dict[str, Any] = {}

        # Split body into sections by ## headings
        sections: dict[str, str] = {}
        current_heading: str | None = None
        current_lines: list[str] = []

        for line in body.split("\n"):
            match = re.match(r"^##\s+(.+?)(?:\s*<!--.*-->)?\s*$", line)
            if match:
                if current_heading is not None:
                    sections[current_heading.lower()] = "\n".join(current_lines).strip()
                current_heading = match.group(1).strip()
                current_lines = []
            else:
                current_lines.append(line)

        if current_heading is not None:
            sections[current_heading.lower()] = "\n".join(current_lines).strip()

        # Simple string fields
        heading_to_key = {
            "agent version": "version",
            "tool tier": "tool_tier",
        }
        for heading, key in heading_to_key.items():
            if heading in sections and sections[heading]:
                value = sections[heading].strip()
                if key == "tool_tier":
                    # Strip label, e.g., "T3 (External)" -> "T3"
                    tier_match = re.match(r"(T\d)", value)
                    if tier_match:
                        value = tier_match.group(1)
                gov_data[key] = value

        # YAML-block fields
        yaml_headings = {
            "enforcement": "enforcement",
            "portability": "portability",
            "session context": "session_context",
        }
        for heading, key in yaml_headings.items():
            if heading in sections and sections[heading]:
                try:
                    parsed = yaml.safe_load(sections[heading])
                    if isinstance(parsed, dict):
                        gov_data[key] = parsed
                except yaml.YAMLError:
                    pass

        # Bullet-list field: prior_art
        if "prior art" in sections and sections["prior art"]:
            content = sections["prior art"]
            items = [
                line.lstrip("- ").strip()
                for line in content.split("\n")
                if line.strip().startswith("-")
            ]
            if items:
                gov_data["prior_art"] = items

        return gov_data

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
