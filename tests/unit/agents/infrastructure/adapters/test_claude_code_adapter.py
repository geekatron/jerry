# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""Tests for ClaudeCodeAdapter."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from src.agents.domain.value_objects.body_format import BodyFormat
from src.agents.domain.value_objects.model_tier import ModelTier
from src.agents.domain.value_objects.tool_tier import ToolTier
from src.agents.domain.value_objects.vendor_target import VendorTarget
from src.agents.infrastructure.adapters.claude_code_adapter import ClaudeCodeAdapter

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def make_adapter(tool_mapper: Any, prompt_transformer: Any, skills_dir: Path) -> ClaudeCodeAdapter:
    """Construct a ClaudeCodeAdapter under test."""
    return ClaudeCodeAdapter(
        tool_mapper=tool_mapper,
        prompt_transformer=prompt_transformer,
        skills_dir=skills_dir,
    )


# ---------------------------------------------------------------------------
# generate()
# ---------------------------------------------------------------------------


class TestGenerate:
    """Tests for ClaudeCodeAdapter.generate()."""

    def test_generate_returns_two_artifacts(
        self,
        make_canonical_agent: Any,
        tool_mapper: Any,
        prompt_transformer: Any,
        tmp_path: Path,
    ) -> None:
        # Arrange
        adapter = make_adapter(tool_mapper, prompt_transformer, tmp_path)
        agent = make_canonical_agent(name="test-agent", skill="test-skill")

        # Act
        artifacts = adapter.generate(agent)

        # Assert
        assert len(artifacts) == 2

    def test_generate_first_artifact_is_md(
        self,
        make_canonical_agent: Any,
        tool_mapper: Any,
        prompt_transformer: Any,
        tmp_path: Path,
    ) -> None:
        # Arrange
        adapter = make_adapter(tool_mapper, prompt_transformer, tmp_path)
        agent = make_canonical_agent(name="my-agent", skill="my-skill")

        # Act
        artifacts = adapter.generate(agent)

        # Assert — first artifact is the .md file
        md_artifact = artifacts[0]
        assert md_artifact.filename == "my-agent.md"
        assert md_artifact.artifact_type == "agent_definition"
        assert md_artifact.vendor == VendorTarget.CLAUDE_CODE
        assert md_artifact.source_agent == "my-agent"

    def test_generate_second_artifact_is_governance_yaml(
        self,
        make_canonical_agent: Any,
        tool_mapper: Any,
        prompt_transformer: Any,
        tmp_path: Path,
    ) -> None:
        # Arrange
        adapter = make_adapter(tool_mapper, prompt_transformer, tmp_path)
        agent = make_canonical_agent(name="my-agent", skill="my-skill")

        # Act
        artifacts = adapter.generate(agent)

        # Assert — second artifact is the .governance.yaml file
        gov_artifact = artifacts[1]
        assert gov_artifact.filename == "my-agent.governance.yaml"
        assert gov_artifact.artifact_type == "governance"
        assert gov_artifact.vendor == VendorTarget.CLAUDE_CODE

    def test_generate_paths_are_under_skill_agents_dir(
        self,
        make_canonical_agent: Any,
        tool_mapper: Any,
        prompt_transformer: Any,
        tmp_path: Path,
    ) -> None:
        # Arrange
        adapter = make_adapter(tool_mapper, prompt_transformer, tmp_path)
        agent = make_canonical_agent(name="eng-qa", skill="eng-team")

        # Act
        artifacts = adapter.generate(agent)

        # Assert — paths are relative to skills/{skill}/agents/
        expected_dir = tmp_path / "eng-team" / "agents"
        assert artifacts[0].path == expected_dir / "eng-qa.md"
        assert artifacts[1].path == expected_dir / "eng-qa.governance.yaml"

    def test_generate_md_content_starts_with_yaml_delimiters(
        self,
        make_canonical_agent: Any,
        tool_mapper: Any,
        prompt_transformer: Any,
        tmp_path: Path,
    ) -> None:
        # Arrange
        adapter = make_adapter(tool_mapper, prompt_transformer, tmp_path)
        agent = make_canonical_agent()

        # Act
        artifacts = adapter.generate(agent)

        # Assert — .md content starts with YAML frontmatter
        assert artifacts[0].content.startswith("---\n")
        assert "---\n" in artifacts[0].content[3:]

    def test_generate_governance_content_is_valid_yaml(
        self,
        make_canonical_agent: Any,
        tool_mapper: Any,
        prompt_transformer: Any,
        tmp_path: Path,
    ) -> None:
        # Arrange
        adapter = make_adapter(tool_mapper, prompt_transformer, tmp_path)
        agent = make_canonical_agent()

        # Act
        artifacts = adapter.generate(agent)

        # Assert — governance content is valid YAML
        gov_content = artifacts[1].content
        # Strip header comment lines
        yaml_lines = [line for line in gov_content.splitlines() if not line.startswith("#")]
        parsed = yaml.safe_load("\n".join(yaml_lines))
        assert isinstance(parsed, dict)


# ---------------------------------------------------------------------------
# extract()
# ---------------------------------------------------------------------------


class TestExtract:
    """Tests for ClaudeCodeAdapter.extract()."""

    def _write_md(self, path: Path, frontmatter: dict[str, Any], body: str) -> None:
        """Write a .md file with YAML frontmatter."""
        fm_str = yaml.dump(frontmatter, default_flow_style=False, sort_keys=False)
        path.write_text(f"---\n{fm_str}---\n{body}", encoding="utf-8")

    def _write_gov(self, path: Path, data: dict[str, Any]) -> None:
        """Write a .governance.yaml file."""
        path.write_text(yaml.dump(data, default_flow_style=False), encoding="utf-8")

    def test_extract_parses_name_from_frontmatter(
        self,
        tool_mapper: Any,
        prompt_transformer: Any,
        tmp_path: Path,
    ) -> None:
        # Arrange — build skills/{skill}/agents/{name}.md structure
        agents_dir = tmp_path / "test-skill" / "agents"
        agents_dir.mkdir(parents=True)
        md_path = agents_dir / "test-agent.md"
        self._write_md(
            md_path,
            {"name": "test-agent", "description": "A test agent", "model": "sonnet"},
            "<identity>\nTest role.\n</identity>\n",
        )
        adapter = make_adapter(tool_mapper, prompt_transformer, tmp_path)

        # Act
        agent = adapter.extract(str(md_path))

        # Assert
        assert agent.name == "test-agent"

    def test_extract_detects_skill_from_path(
        self,
        tool_mapper: Any,
        prompt_transformer: Any,
        tmp_path: Path,
    ) -> None:
        # Arrange
        agents_dir = tmp_path / "my-skill" / "agents"
        agents_dir.mkdir(parents=True)
        md_path = agents_dir / "my-agent.md"
        self._write_md(
            md_path,
            {"name": "my-agent", "description": "desc", "model": "sonnet"},
            "Some body content.\n",
        )
        adapter = make_adapter(tool_mapper, prompt_transformer, tmp_path)

        # Act
        agent = adapter.extract(str(md_path))

        # Assert
        assert agent.skill == "my-skill"

    def test_extract_reads_governance_yaml_when_provided(
        self,
        tool_mapper: Any,
        prompt_transformer: Any,
        tmp_path: Path,
    ) -> None:
        # Arrange
        agents_dir = tmp_path / "skill" / "agents"
        agents_dir.mkdir(parents=True)
        md_path = agents_dir / "agent.md"
        gov_path = agents_dir / "agent.governance.yaml"
        self._write_md(
            md_path,
            {"name": "agent", "description": "desc", "model": "opus"},
            "<identity>\nRole.\n</identity>\n",
        )
        self._write_gov(
            gov_path,
            {
                "version": "2.1.0",
                "tool_tier": "T3",
                "identity": {
                    "role": "Expert",
                    "expertise": ["a", "b"],
                    "cognitive_mode": "convergent",
                },
                "constitution": {
                    "principles_applied": [
                        "P-003: No Recursive Subagents (Hard)",
                        "P-020: User Authority (Hard)",
                        "P-022: No Deception (Hard)",
                    ]
                },
            },
        )
        adapter = make_adapter(tool_mapper, prompt_transformer, tmp_path)

        # Act
        agent = adapter.extract(str(md_path), str(gov_path))

        # Assert — version and tool_tier come from governance YAML
        assert agent.version == "2.1.0"
        assert agent.tool_tier == ToolTier.T3

    def test_extract_xml_body_is_detected_as_xml(
        self,
        tool_mapper: Any,
        prompt_transformer: Any,
        tmp_path: Path,
    ) -> None:
        # Arrange
        agents_dir = tmp_path / "skill" / "agents"
        agents_dir.mkdir(parents=True)
        md_path = agents_dir / "agent.md"
        xml_body = "<agent>\n\n<identity>\nRole text.\n</identity>\n\n<purpose>\nPurpose text.\n</purpose>\n\n</agent>\n"
        self._write_md(
            md_path,
            {"name": "agent", "description": "desc", "model": "sonnet"},
            xml_body,
        )
        adapter = make_adapter(tool_mapper, prompt_transformer, tmp_path)

        # Act
        agent = adapter.extract(str(md_path))

        # Assert
        assert agent.body_format == BodyFormat.XML

    def test_extract_markdown_body_is_detected_as_markdown(
        self,
        tool_mapper: Any,
        prompt_transformer: Any,
        tmp_path: Path,
    ) -> None:
        # Arrange
        agents_dir = tmp_path / "skill" / "agents"
        agents_dir.mkdir(parents=True)
        md_path = agents_dir / "agent.md"
        md_body = "## Identity\n\nRole text.\n\n## Purpose\n\nPurpose text.\n\n## Capabilities\n\nCapabilities here.\n"
        self._write_md(
            md_path,
            {"name": "agent", "description": "desc", "model": "sonnet"},
            md_body,
        )
        adapter = make_adapter(tool_mapper, prompt_transformer, tmp_path)

        # Act
        agent = adapter.extract(str(md_path))

        # Assert
        assert agent.body_format == BodyFormat.MARKDOWN

    def test_extract_missing_governance_yaml_uses_defaults(
        self,
        tool_mapper: Any,
        prompt_transformer: Any,
        tmp_path: Path,
    ) -> None:
        # Arrange
        agents_dir = tmp_path / "skill" / "agents"
        agents_dir.mkdir(parents=True)
        md_path = agents_dir / "agent.md"
        self._write_md(
            md_path,
            {"name": "agent", "description": "desc", "model": "sonnet"},
            "Some body.\n",
        )
        adapter = make_adapter(tool_mapper, prompt_transformer, tmp_path)

        # Act — governance path points to non-existent file
        agent = adapter.extract(str(md_path), str(agents_dir / "missing.governance.yaml"))

        # Assert — falls back to defaults
        assert agent.version == "1.0.0"
        assert agent.tool_tier == ToolTier.T1


# ---------------------------------------------------------------------------
# _build_frontmatter()
# ---------------------------------------------------------------------------


class TestBuildFrontmatter:
    """Tests for ClaudeCodeAdapter._build_frontmatter()."""

    def test_frontmatter_includes_name(
        self,
        make_canonical_agent: Any,
        tool_mapper: Any,
        prompt_transformer: Any,
        tmp_path: Path,
    ) -> None:
        # Arrange
        adapter = make_adapter(tool_mapper, prompt_transformer, tmp_path)
        agent = make_canonical_agent(name="my-agent")

        # Act
        fm_str = adapter._build_frontmatter(agent)
        parsed = yaml.safe_load(fm_str)

        # Assert
        assert parsed["name"] == "my-agent"

    def test_frontmatter_maps_model_tier_to_vendor_model(
        self,
        make_canonical_agent: Any,
        tool_mapper: Any,
        prompt_transformer: Any,
        tmp_path: Path,
    ) -> None:
        # Arrange
        adapter = make_adapter(tool_mapper, prompt_transformer, tmp_path)
        agent = make_canonical_agent(model_tier=ModelTier.REASONING_HIGH)

        # Act
        fm_str = adapter._build_frontmatter(agent)
        parsed = yaml.safe_load(fm_str)

        # Assert — reasoning_high maps to "opus" for claude_code
        assert parsed["model"] == "opus"

    def test_frontmatter_maps_abstract_tools_to_vendor_names(
        self,
        make_canonical_agent: Any,
        tool_mapper: Any,
        prompt_transformer: Any,
        tmp_path: Path,
    ) -> None:
        # Arrange
        adapter = make_adapter(tool_mapper, prompt_transformer, tmp_path)
        agent = make_canonical_agent(native_tools=["file_read", "file_write"])

        # Act
        fm_str = adapter._build_frontmatter(agent)
        parsed = yaml.safe_load(fm_str)

        # Assert — abstract names mapped to Claude Code names
        assert "Read" in parsed["tools"]
        assert "Write" in parsed["tools"]

    def test_frontmatter_excludes_agent_delegate_from_tools(
        self,
        make_canonical_agent: Any,
        tool_mapper: Any,
        prompt_transformer: Any,
        tmp_path: Path,
    ) -> None:
        # Arrange — T5 agent with delegation capability
        adapter = make_adapter(tool_mapper, prompt_transformer, tmp_path)
        agent = make_canonical_agent(
            tool_tier=ToolTier.T5,
            native_tools=["file_read", "agent_delegate"],
        )

        # Act
        fm_str = adapter._build_frontmatter(agent)
        parsed = yaml.safe_load(fm_str)

        # Assert — Task (agent_delegate) excluded from tools
        assert "Task" not in parsed.get("tools", "")

    def test_frontmatter_includes_mcp_servers(
        self,
        make_canonical_agent: Any,
        tool_mapper: Any,
        prompt_transformer: Any,
        tmp_path: Path,
    ) -> None:
        # Arrange
        adapter = make_adapter(tool_mapper, prompt_transformer, tmp_path)
        agent = make_canonical_agent(mcp_servers=["context7", "memory-keeper"])

        # Act
        fm_str = adapter._build_frontmatter(agent)
        parsed = yaml.safe_load(fm_str)

        # Assert
        assert "mcpServers" in parsed
        assert parsed["mcpServers"]["context7"] is True
        assert parsed["mcpServers"]["memory-keeper"] is True

    def test_frontmatter_no_tools_key_when_no_native_tools(
        self,
        make_canonical_agent: Any,
        tool_mapper: Any,
        prompt_transformer: Any,
        tmp_path: Path,
    ) -> None:
        # Arrange — agent with no native tools
        adapter = make_adapter(tool_mapper, prompt_transformer, tmp_path)
        agent = make_canonical_agent(native_tools=[])

        # Act
        fm_str = adapter._build_frontmatter(agent)
        parsed = yaml.safe_load(fm_str)

        # Assert — tools key omitted when empty
        assert "tools" not in parsed


# ---------------------------------------------------------------------------
# _build_body()
# ---------------------------------------------------------------------------


class TestBuildBody:
    """Tests for ClaudeCodeAdapter._build_body()."""

    def test_xml_format_body_is_wrapped_in_agent_tags(
        self,
        make_canonical_agent: Any,
        tool_mapper: Any,
        prompt_transformer: Any,
        tmp_path: Path,
    ) -> None:
        # Arrange
        adapter = make_adapter(tool_mapper, prompt_transformer, tmp_path)
        agent = make_canonical_agent(
            body_format=BodyFormat.XML,
            prompt_body="## Identity\n\nTest role.\n",
        )

        # Act
        body = adapter._build_body(agent)

        # Assert
        assert body.startswith("<agent>")
        assert "</agent>" in body

    def test_markdown_format_body_is_not_wrapped(
        self,
        make_canonical_agent: Any,
        tool_mapper: Any,
        prompt_transformer: Any,
        tmp_path: Path,
    ) -> None:
        # Arrange
        adapter = make_adapter(tool_mapper, prompt_transformer, tmp_path)
        agent = make_canonical_agent(
            body_format=BodyFormat.MARKDOWN,
            prompt_body="## Identity\n\nTest role.\n",
        )

        # Act
        body = adapter._build_body(agent)

        # Assert — no <agent> wrapper for markdown format
        assert not body.startswith("<agent>")
        assert "</agent>" not in body

    def test_abstract_tool_names_substituted_with_vendor_names(
        self,
        make_canonical_agent: Any,
        tool_mapper: Any,
        prompt_transformer: Any,
        tmp_path: Path,
    ) -> None:
        # Arrange
        adapter = make_adapter(tool_mapper, prompt_transformer, tmp_path)
        agent = make_canonical_agent(
            body_format=BodyFormat.MARKDOWN,
            prompt_body="Use file_read to search files and file_write to save output.\n",
        )

        # Act
        body = adapter._build_body(agent)

        # Assert — abstract names replaced with Claude Code names
        assert "Read" in body
        assert "Write" in body


# ---------------------------------------------------------------------------
# _build_governance_yaml()
# ---------------------------------------------------------------------------


class TestBuildGovernanceYaml:
    """Tests for ClaudeCodeAdapter._build_governance_yaml()."""

    def _parse_gov(self, content: str) -> dict[str, Any]:
        """Parse governance YAML, skipping comment lines."""
        yaml_lines = [line for line in content.splitlines() if not line.startswith("#")]
        result: dict[str, Any] = yaml.safe_load("\n".join(yaml_lines)) or {}
        return result

    def test_governance_includes_version(
        self,
        make_canonical_agent: Any,
        tool_mapper: Any,
        prompt_transformer: Any,
        tmp_path: Path,
    ) -> None:
        # Arrange
        adapter = make_adapter(tool_mapper, prompt_transformer, tmp_path)
        agent = make_canonical_agent(version="2.3.1")

        # Act
        content = adapter._build_governance_yaml(agent)
        parsed = self._parse_gov(content)

        # Assert
        assert parsed["version"] == "2.3.1"

    def test_governance_includes_tool_tier(
        self,
        make_canonical_agent: Any,
        tool_mapper: Any,
        prompt_transformer: Any,
        tmp_path: Path,
    ) -> None:
        # Arrange
        adapter = make_adapter(tool_mapper, prompt_transformer, tmp_path)
        agent = make_canonical_agent(tool_tier=ToolTier.T3)

        # Act
        content = adapter._build_governance_yaml(agent)
        parsed = self._parse_gov(content)

        # Assert
        assert parsed["tool_tier"] == "T3"

    def test_governance_moves_forbidden_actions_to_capabilities(
        self,
        make_canonical_agent: Any,
        tool_mapper: Any,
        prompt_transformer: Any,
        tmp_path: Path,
        sample_constitution: dict[str, Any],
    ) -> None:
        # Arrange
        adapter = make_adapter(tool_mapper, prompt_transformer, tmp_path)
        agent = make_canonical_agent(constitution=sample_constitution)

        # Act
        content = adapter._build_governance_yaml(agent)
        parsed = self._parse_gov(content)

        # Assert — forbidden_actions appears in capabilities, not constitution
        assert "forbidden_actions" in parsed.get("capabilities", {})
        # Constitution itself should not contain forbidden_actions
        constitution_block = parsed.get("constitution", {})
        assert "forbidden_actions" not in constitution_block

    def test_governance_header_contains_agent_name(
        self,
        make_canonical_agent: Any,
        tool_mapper: Any,
        prompt_transformer: Any,
        tmp_path: Path,
    ) -> None:
        # Arrange
        adapter = make_adapter(tool_mapper, prompt_transformer, tmp_path)
        agent = make_canonical_agent(name="special-agent")

        # Act
        content = adapter._build_governance_yaml(agent)

        # Assert — header comment references the agent name
        assert "special-agent" in content.splitlines()[0]

    def test_governance_omits_empty_optional_sections(
        self,
        make_canonical_agent: Any,
        tool_mapper: Any,
        prompt_transformer: Any,
        tmp_path: Path,
    ) -> None:
        # Arrange — agent with no persona, output, validation, etc.
        adapter = make_adapter(tool_mapper, prompt_transformer, tmp_path)
        agent = make_canonical_agent(
            persona={},
            output={},
            validation={},
            prior_art=[],
            enforcement={},
            session_context={},
        )

        # Act
        content = adapter._build_governance_yaml(agent)
        parsed = self._parse_gov(content)

        # Assert — optional empty sections not emitted
        assert "persona" not in parsed
        assert "validation" not in parsed
        assert "prior_art" not in parsed
        assert "enforcement" not in parsed
        assert "session_context" not in parsed


# ---------------------------------------------------------------------------
# _parse_md()
# ---------------------------------------------------------------------------


class TestParseMd:
    """Tests for ClaudeCodeAdapter._parse_md()."""

    def test_parses_frontmatter_and_body(
        self,
        tool_mapper: Any,
        prompt_transformer: Any,
        tmp_path: Path,
    ) -> None:
        # Arrange
        adapter = make_adapter(tool_mapper, prompt_transformer, tmp_path)
        content = "---\nname: my-agent\nmodel: sonnet\n---\nBody content here.\n"

        # Act
        fm, body = adapter._parse_md(content)

        # Assert
        assert fm["name"] == "my-agent"
        assert fm["model"] == "sonnet"
        assert "Body content here." in body

    def test_no_frontmatter_returns_empty_dict(
        self,
        tool_mapper: Any,
        prompt_transformer: Any,
        tmp_path: Path,
    ) -> None:
        # Arrange
        adapter = make_adapter(tool_mapper, prompt_transformer, tmp_path)
        content = "Just plain body content with no YAML.\n"

        # Act
        fm, body = adapter._parse_md(content)

        # Assert
        assert fm == {}
        assert "Just plain body content" in body

    def test_malformed_yaml_frontmatter_returns_empty_dict(
        self,
        tool_mapper: Any,
        prompt_transformer: Any,
        tmp_path: Path,
    ) -> None:
        # Arrange
        adapter = make_adapter(tool_mapper, prompt_transformer, tmp_path)
        content = "---\n: invalid: yaml: [unclosed\n---\nBody.\n"

        # Act
        fm, _ = adapter._parse_md(content)

        # Assert — malformed YAML treated as empty, body preserved
        assert fm == {}

    def test_unclosed_frontmatter_returns_empty_dict(
        self,
        tool_mapper: Any,
        prompt_transformer: Any,
        tmp_path: Path,
    ) -> None:
        # Arrange
        adapter = make_adapter(tool_mapper, prompt_transformer, tmp_path)
        content = "---\nname: agent\nmodel: sonnet\n"  # No closing ---

        # Act
        fm, _ = adapter._parse_md(content)

        # Assert
        assert fm == {}


# ---------------------------------------------------------------------------
# _parse_tools_from_frontmatter()
# ---------------------------------------------------------------------------


class TestParseToolsFromFrontmatter:
    """Tests for ClaudeCodeAdapter._parse_tools_from_frontmatter()."""

    def test_string_tools_are_split_by_comma(
        self,
        tool_mapper: Any,
        prompt_transformer: Any,
        tmp_path: Path,
    ) -> None:
        # Arrange
        adapter = make_adapter(tool_mapper, prompt_transformer, tmp_path)
        fm = {"tools": "Read, Write, Edit"}

        # Act
        tools = adapter._parse_tools_from_frontmatter(fm)

        # Assert
        assert tools == ["Read", "Write", "Edit"]

    def test_list_tools_returned_as_is(
        self,
        tool_mapper: Any,
        prompt_transformer: Any,
        tmp_path: Path,
    ) -> None:
        # Arrange
        adapter = make_adapter(tool_mapper, prompt_transformer, tmp_path)
        fm = {"tools": ["Read", "Grep", "Glob"]}

        # Act
        tools = adapter._parse_tools_from_frontmatter(fm)

        # Assert
        assert tools == ["Read", "Grep", "Glob"]

    def test_missing_tools_key_returns_empty_list(
        self,
        tool_mapper: Any,
        prompt_transformer: Any,
        tmp_path: Path,
    ) -> None:
        # Arrange
        adapter = make_adapter(tool_mapper, prompt_transformer, tmp_path)
        fm: dict[str, Any] = {}

        # Act
        tools = adapter._parse_tools_from_frontmatter(fm)

        # Assert
        assert tools == []

    def test_empty_string_tools_returns_empty_list(
        self,
        tool_mapper: Any,
        prompt_transformer: Any,
        tmp_path: Path,
    ) -> None:
        # Arrange
        adapter = make_adapter(tool_mapper, prompt_transformer, tmp_path)
        fm = {"tools": ""}

        # Act
        tools = adapter._parse_tools_from_frontmatter(fm)

        # Assert
        assert tools == []


# ---------------------------------------------------------------------------
# _ensure_constitutional_triplet()
# ---------------------------------------------------------------------------


class TestEnsureConstitutionalTriplet:
    """Tests for ClaudeCodeAdapter._ensure_constitutional_triplet()."""

    def test_adds_missing_principle(
        self,
        tool_mapper: Any,
        prompt_transformer: Any,
        tmp_path: Path,
    ) -> None:
        # Arrange
        adapter = make_adapter(tool_mapper, prompt_transformer, tmp_path)
        constitution: dict[str, Any] = {
            "principles_applied": [
                "P-020: User Authority (Hard)",
                "P-022: No Deception (Hard)",
            ],
            "forbidden_actions": [
                "Override user decisions (P-020)",
                "Misrepresent capabilities or confidence (P-022)",
            ],
        }

        # Act
        result = adapter._ensure_constitutional_triplet(constitution)

        # Assert — P-003 was added
        principles_text = " ".join(result["principles_applied"])
        assert "P-003" in principles_text

    def test_adds_missing_forbidden_action(
        self,
        tool_mapper: Any,
        prompt_transformer: Any,
        tmp_path: Path,
    ) -> None:
        # Arrange
        adapter = make_adapter(tool_mapper, prompt_transformer, tmp_path)
        constitution: dict[str, Any] = {
            "principles_applied": [
                "P-003: No Recursive Subagents (Hard)",
                "P-020: User Authority (Hard)",
                "P-022: No Deception (Hard)",
            ],
            "forbidden_actions": [
                "Spawn recursive subagents (P-003)",
                "Override user decisions (P-020)",
                # P-022 missing
            ],
        }

        # Act
        result = adapter._ensure_constitutional_triplet(constitution)

        # Assert — P-022 forbidden action added
        actions_text = " ".join(result["forbidden_actions"])
        assert "P-022" in actions_text

    def test_idempotent_when_complete(
        self,
        tool_mapper: Any,
        prompt_transformer: Any,
        tmp_path: Path,
        sample_constitution: dict[str, Any],
    ) -> None:
        # Arrange — full constitution with all three principles
        adapter = make_adapter(tool_mapper, prompt_transformer, tmp_path)
        original_principles = list(sample_constitution["principles_applied"])
        original_actions = list(sample_constitution["forbidden_actions"])

        # Act
        result = adapter._ensure_constitutional_triplet(dict(sample_constitution))

        # Assert — no entries were added (count unchanged)
        assert len(result["principles_applied"]) == len(original_principles)
        assert len(result["forbidden_actions"]) == len(original_actions)

    def test_empty_constitution_gets_all_three(
        self,
        tool_mapper: Any,
        prompt_transformer: Any,
        tmp_path: Path,
    ) -> None:
        # Arrange
        adapter = make_adapter(tool_mapper, prompt_transformer, tmp_path)
        constitution: dict[str, Any] = {}

        # Act
        result = adapter._ensure_constitutional_triplet(constitution)

        # Assert
        principles_text = " ".join(result["principles_applied"])
        actions_text = " ".join(result["forbidden_actions"])
        for code in ("P-003", "P-020", "P-022"):
            assert code in principles_text
            assert code in actions_text


# ---------------------------------------------------------------------------
# _strip_agent_wrapper()
# ---------------------------------------------------------------------------


class TestStripAgentWrapper:
    """Tests for ClaudeCodeAdapter._strip_agent_wrapper()."""

    def test_strips_proper_agent_tags(
        self,
        tool_mapper: Any,
        prompt_transformer: Any,
        tmp_path: Path,
    ) -> None:
        # Arrange
        adapter = make_adapter(tool_mapper, prompt_transformer, tmp_path)
        body = "<agent>\n\n<identity>\nContent.\n</identity>\n\n</agent>\n"

        # Act
        result = adapter._strip_agent_wrapper(body)

        # Assert — agent tags removed, inner content preserved
        assert "<agent>" not in result
        assert "</agent>" not in result
        assert "<identity>" in result

    def test_strips_corrupted_agent_prefix(
        self,
        tool_mapper: Any,
        prompt_transformer: Any,
        tmp_path: Path,
    ) -> None:
        # Arrange — "agent>" variant (missing <) from PR #87 transform bug
        adapter = make_adapter(tool_mapper, prompt_transformer, tmp_path)
        body = "agent>\n\n<identity>\nContent.\n</identity>\n\n</agent>\n"

        # Act
        result = adapter._strip_agent_wrapper(body)

        # Assert — corrupted prefix stripped
        assert not result.startswith("agent>")
        assert "</agent>" not in result

    def test_no_wrapper_returns_content_unchanged(
        self,
        tool_mapper: Any,
        prompt_transformer: Any,
        tmp_path: Path,
    ) -> None:
        # Arrange — body without any wrapper
        adapter = make_adapter(tool_mapper, prompt_transformer, tmp_path)
        body = "<identity>\nContent.\n</identity>\n"

        # Act
        result = adapter._strip_agent_wrapper(body)

        # Assert — content preserved as-is (aside from trailing newline)
        assert "<identity>" in result
        assert "Content." in result

    def test_result_ends_with_newline(
        self,
        tool_mapper: Any,
        prompt_transformer: Any,
        tmp_path: Path,
    ) -> None:
        # Arrange
        adapter = make_adapter(tool_mapper, prompt_transformer, tmp_path)
        body = "<agent>\n\n<identity>\nContent.\n</identity>\n\n</agent>"

        # Act
        result = adapter._strip_agent_wrapper(body)

        # Assert
        assert result.endswith("\n")


# ---------------------------------------------------------------------------
# _detect_body_format()
# ---------------------------------------------------------------------------


class TestDetectBodyFormat:
    """Tests for ClaudeCodeAdapter._detect_body_format()."""

    def test_xml_heavy_body_detected_as_xml(
        self,
        tool_mapper: Any,
        prompt_transformer: Any,
        tmp_path: Path,
    ) -> None:
        # Arrange — more XML tags than ## headings
        adapter = make_adapter(tool_mapper, prompt_transformer, tmp_path)
        body = "<identity>\nRole.\n</identity>\n\n<purpose>\nPurpose.\n</purpose>\n\n<capabilities>\nCaps.\n</capabilities>\n"

        # Act
        result = adapter._detect_body_format(body)

        # Assert
        assert result == BodyFormat.XML

    def test_markdown_heavy_body_detected_as_markdown(
        self,
        tool_mapper: Any,
        prompt_transformer: Any,
        tmp_path: Path,
    ) -> None:
        # Arrange — more ## headings than XML tags
        adapter = make_adapter(tool_mapper, prompt_transformer, tmp_path)
        body = "## Identity\n\nRole.\n\n## Purpose\n\nPurpose.\n\n## Capabilities\n\nCaps.\n\n## Methodology\n\nMethod.\n"

        # Act
        result = adapter._detect_body_format(body)

        # Assert
        assert result == BodyFormat.MARKDOWN

    def test_no_tags_no_headings_defaults_to_markdown(
        self,
        tool_mapper: Any,
        prompt_transformer: Any,
        tmp_path: Path,
    ) -> None:
        # Arrange — plain prose body
        adapter = make_adapter(tool_mapper, prompt_transformer, tmp_path)
        body = "This is a plain text body with no headings or XML tags.\n"

        # Act
        result = adapter._detect_body_format(body)

        # Assert — tie goes to MARKDOWN (xml_count == md_count == 0, not >)
        assert result == BodyFormat.MARKDOWN

    def test_vendor_property_returns_claude_code(
        self,
        tool_mapper: Any,
        prompt_transformer: Any,
        tmp_path: Path,
    ) -> None:
        # Arrange
        adapter = make_adapter(tool_mapper, prompt_transformer, tmp_path)

        # Act / Assert
        assert adapter.vendor == VendorTarget.CLAUDE_CODE
