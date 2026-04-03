# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""Schema validation test suite for Claude Code frontmatter schemas (EN-003).

Validates both agent and skill YAML frontmatter schemas against:
  - Positive fixtures extracted from production agent/skill files
  - Negative fixtures covering each schema constraint

Schemas under test:
  - docs/schemas/claude-code-frontmatter-v1.schema.json   (agent schema)
  - docs/schemas/claude-code-skill-frontmatter-v1.schema.json  (skill schema)

References:
    - EN-003: Schema validation CI gate for frontmatter
    - H-20: BDD test-first (Red phase)
    - agent-development-standards.md H-34: agent definition standards
    - docs/schemas/claude-code-frontmatter-v1.schema.json
    - docs/schemas/claude-code-skill-frontmatter-v1.schema.json
"""

from __future__ import annotations

import json
import re
from pathlib import Path

import pytest
import yaml
from jsonschema import ValidationError, validate

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

REPO_ROOT = Path(__file__).parents[2]
SCHEMAS_DIR = REPO_ROOT / "docs" / "schemas"

AGENT_SCHEMA_PATH = SCHEMAS_DIR / "claude-code-frontmatter-v1.schema.json"
SKILL_SCHEMA_PATH = SCHEMAS_DIR / "claude-code-skill-frontmatter-v1.schema.json"

SKILLS_DIR = REPO_ROOT / "skills"

# ---------------------------------------------------------------------------
# Schema loading
# ---------------------------------------------------------------------------


def _load_schema(path: Path) -> dict:
    """Load a JSON Schema file from disk.

    Args:
        path: Absolute path to the .schema.json file.

    Returns:
        Parsed JSON Schema as a Python dict.

    Raises:
        FileNotFoundError: If the schema file does not exist.
        json.JSONDecodeError: If the schema is not valid JSON.
    """
    return json.loads(path.read_text(encoding="utf-8"))


AGENT_SCHEMA: dict = _load_schema(AGENT_SCHEMA_PATH)
SKILL_SCHEMA: dict = _load_schema(SKILL_SCHEMA_PATH)


# ---------------------------------------------------------------------------
# Frontmatter extraction helper
# ---------------------------------------------------------------------------

_FRONTMATTER_RE = re.compile(r"^---\r?\n(.*?)\r?\n---", re.DOTALL)


def _extract_frontmatter(md_path: Path) -> dict:
    """Extract and parse YAML frontmatter from a Markdown file.

    Uses a regex to locate the opening ``---`` / closing ``---`` delimiters
    and parses the interior with ``yaml.safe_load``.

    Args:
        md_path: Absolute path to the ``.md`` file.

    Returns:
        Parsed frontmatter as a Python dict.  Returns an empty dict when no
        frontmatter block is found.

    Raises:
        yaml.YAMLError: If the frontmatter YAML is malformed.
    """
    text = md_path.read_text(encoding="utf-8")
    match = _FRONTMATTER_RE.match(text)
    if not match:
        return {}
    return yaml.safe_load(match.group(1)) or {}


# ---------------------------------------------------------------------------
# Positive fixtures — extracted from production agent files
# ---------------------------------------------------------------------------

# skills/problem-solving/agents/ps-researcher.md
# Has: mcpServers as object (legacy format), model alias 'opus', tools as string
_PS_RESEARCHER_FRONTMATTER: dict = {
    "name": "ps-researcher",
    "description": (
        "Deep research agent with MANDATORY artifact persistence, PS integration, "
        "Context7 MCP, adversarial quality strategies, and L0/L1/L2 output levels"
    ),
    "model": "opus",
    "tools": "Read, Write, Edit, Glob, Grep, WebSearch, WebFetch, Bash",
    "mcpServers": {"context7": True},
}

# skills/adversary/agents/adv-scorer.md
# Has: minimal T1-tier agent, tools as string, model alias 'sonnet'
_ADV_SCORER_FRONTMATTER: dict = {
    "name": "adv-scorer",
    "description": (
        "Quality Scorer agent — implements S-014 LLM-as-Judge rubric scoring with "
        "the SSOT 6-dimension weighted composite, producing per-dimension scores, "
        "weighted composite, and PASS/REVISE/ESCALATE verdict"
    ),
    "model": "sonnet",
    "tools": "Read, Write, Edit, Glob, Grep",
}

# skills/eng-team/agents/eng-architect.md
# Has: mcpServers as object, model alias 'opus', tools as string
_ENG_ARCHITECT_FRONTMATTER: dict = {
    "name": "eng-architect",
    "description": (
        "Solution architect and threat modeler for the /eng-team skill. Invoked "
        "when users request system design, architecture decisions, or threat "
        "modeling (STRIDE/DREAD/PASTA). Produces architecture decision records, "
        "threat models with trust boundaries, and security-first designs. Routes "
        "from Step 1 of the /eng-team 8-step workflow. Integrates NIST CSF 2.0 "
        "governance and threat intelligence from /red-team cross-skill integration."
    ),
    "model": "opus",
    "tools": "Read, Write, Edit, Glob, Grep, Bash, WebSearch, WebFetch",
    "mcpServers": {"context7": True},
}

_AGENT_POSITIVE_FIXTURES = [
    pytest.param(_PS_RESEARCHER_FRONTMATTER, id="ps-researcher"),
    pytest.param(_ADV_SCORER_FRONTMATTER, id="adv-scorer"),
    pytest.param(_ENG_ARCHITECT_FRONTMATTER, id="eng-architect"),
]

# ---------------------------------------------------------------------------
# Positive fixtures — extracted from production SKILL.md files
# ---------------------------------------------------------------------------

# skills/problem-solving/SKILL.md
# Has: version (Jerry extension), activation-keywords (Jerry extension), allowed-tools
_PS_SKILL_FRONTMATTER: dict = {
    "name": "problem-solving",
    "description": (
        "Structured problem-solving framework with specialized agents for research, "
        "analysis, architecture decisions, validation, synthesis, reviews, "
        "investigations, and reporting. Use when tackling complex problems that need "
        "systematic exploration, evidence-based decisions, and persistent artifacts."
    ),
    "version": "2.2.0",
    "allowed-tools": (
        "Read, Write, Edit, Glob, Grep, Bash, Task, WebSearch, WebFetch, "
        "mcp__context7__resolve-library-id, mcp__context7__query-docs, "
        "mcp__memory-keeper__context_save, mcp__memory-keeper__context_get, "
        "mcp__memory-keeper__context_search"
    ),
    "activation-keywords": [
        "research",
        "analyze",
        "investigate",
        "review",
        "synthesize",
        "validate",
        "architecture decision",
        "ADR",
        "root cause",
        "trade-off analysis",
        "5 whys",
        "problem solving",
        "critique",
        "quality score",
        "iterative refinement",
        "evaluate quality",
        "improvement feedback",
    ],
}

# skills/adversary/SKILL.md
# Has: version (Jerry extension), activation-keywords (Jerry extension), allowed-tools
_ADV_SKILL_FRONTMATTER: dict = {
    "name": "adversary",
    "description": (
        "On-demand adversarial quality reviews using strategy templates. Selects "
        "strategies by criticality level, executes adversarial templates against "
        "deliverables, and scores quality using LLM-as-Judge rubric. Integrates "
        "with quality-enforcement.md SSOT."
    ),
    "version": "1.0.0",
    "allowed-tools": "Read, Write, Edit, Glob, Grep, Bash",
    "activation-keywords": [
        "adversarial review",
        "adversary",
        "adversarial quality review",
        "strategy review",
        "adversarial critique",
        "rigorous critique",
        "formal critique",
        "run adversarial",
        "quality scoring",
        "LLM-as-Judge",
        "strategy selection",
        "tournament review",
        "red team",
        "devil's advocate",
        "steelman",
        "pre-mortem",
        "C2 review",
        "C3 review",
        "C4 review",
        "tournament mode",
        "quality gate",
    ],
}

_SKILL_POSITIVE_FIXTURES = [
    pytest.param(_PS_SKILL_FRONTMATTER, id="problem-solving-skill"),
    pytest.param(_ADV_SKILL_FRONTMATTER, id="adversary-skill"),
]

# ---------------------------------------------------------------------------
# Negative fixtures — agent schema (must FAIL validation)
# ---------------------------------------------------------------------------

_AGENT_NEGATIVE_FIXTURES = [
    pytest.param(
        {"description": "A valid description for an agent with no name field."},
        "required field 'name' is missing",
        id="agent-missing-name",
    ),
    pytest.param(
        {"name": "valid-agent"},
        "required field 'description' is missing",
        id="agent-missing-description",
    ),
    pytest.param(
        {"name": "My-Agent", "description": "Agent with uppercase in name."},
        "'name' pattern rejects uppercase letters",
        id="agent-name-uppercase",
    ),
    pytest.param(
        {"name": "my--agent", "description": "Agent with consecutive hyphens in name."},
        "'name' pattern rejects consecutive hyphens",
        id="agent-name-consecutive-hyphens",
    ),
    pytest.param(
        {
            "name": "valid-agent",
            "description": "Agent with an invalid model identifier using underscore.",
            "model": "claude_3_sonnet",
        },
        "'model' pattern rejects underscores — only hyphens permitted after 'claude-'",
        id="agent-model-invalid-underscore",
    ),
    pytest.param(
        {
            "name": "valid-agent",
            "description": "Agent with a typo in the model alias.",
            "model": "opuis",
        },
        "'model' pattern rejects unknown alias 'opuis'",
        id="agent-model-typo",
    ),
    pytest.param(
        {
            "name": "valid-agent",
            "description": "Agent with an invalid permissionMode value.",
            "permissionMode": "admin",
        },
        "'permissionMode' enum rejects 'admin'",
        id="agent-permission-mode-invalid",
    ),
    pytest.param(
        {
            "name": "valid-agent",
            "description": "Agent with an invalid effort value.",
            "effort": "extreme",
        },
        "'effort' enum rejects 'extreme'",
        id="agent-effort-invalid",
    ),
    pytest.param(
        {
            "name": "valid-agent",
            "description": "Agent with maxTurns as a string instead of integer.",
            "maxTurns": "10",
        },
        "'maxTurns' must be integer, not string",
        id="agent-max-turns-string",
    ),
    pytest.param(
        {"name": "valid-agent", "description": "Too short"},
        "'description' minLength=10 rejects strings under 10 characters",
        id="agent-description-too-short",
    ),
    pytest.param(
        {"name": "claude", "description": "Agent using reserved word 'claude' as name."},
        "'name' allOf/not rejects reserved word 'claude'",
        id="agent-name-reserved-claude",
    ),
    pytest.param(
        {
            "name": "anthropic-service",
            "description": "Agent using reserved word 'anthropic' in name.",
        },
        "'name' allOf/not rejects names containing 'anthropic'",
        id="agent-name-reserved-anthropic",
    ),
]

# ---------------------------------------------------------------------------
# Negative fixtures — skill schema (must FAIL validation)
# ---------------------------------------------------------------------------

_SKILL_NEGATIVE_FIXTURES = [
    pytest.param(
        {"name": "a" * 65, "description": "A skill with a name that is over 64 characters long."},
        "'name' maxLength=64 rejects names over 64 characters",
        id="skill-name-too-long",
    ),
    pytest.param(
        {
            "name": "MySkill",
            "description": "A skill with uppercase letters in the name field.",
        },
        "'name' pattern rejects uppercase letters",
        id="skill-name-uppercase",
    ),
    pytest.param(
        {
            "name": "valid-skill",
            "description": "A skill with an invalid effort value.",
            "effort": "extreme",
        },
        "'effort' enum rejects 'extreme'",
        id="skill-effort-invalid",
    ),
    pytest.param(
        {
            "name": "valid-skill",
            "description": "A skill with an invalid shell value.",
            "shell": "zsh",
        },
        "'shell' enum rejects 'zsh' (only bash and powershell are valid)",
        id="skill-shell-invalid",
    ),
    pytest.param(
        {
            "name": "valid-skill",
            "description": "A skill with an invalid context value.",
            "context": "split",
        },
        "'context' enum rejects 'split' (only 'fork' is valid)",
        id="skill-context-invalid",
    ),
    pytest.param(
        {
            "name": "valid-skill",
            "description": "x" * 1025,
        },
        "'description' maxLength=1024 rejects strings over 1024 characters",
        id="skill-description-too-long",
    ),
    pytest.param(
        {
            "name": "valid-skill",
            "description": "A skill with a typo in the model alias.",
            "model": "sonnett",
        },
        "'model' pattern rejects 'sonnett' (typo — double t)",
        id="skill-model-typo",
    ),
    pytest.param(
        {"name": "claude-helper", "description": "Skill using reserved word 'claude' in name."},
        "'name' allOf/not rejects names containing 'claude'",
        id="skill-name-reserved-claude",
    ),
    pytest.param(
        {
            "name": "my-anthropic-tool",
            "description": "Skill using reserved word 'anthropic' in name.",
        },
        "'name' allOf/not rejects names containing 'anthropic'",
        id="skill-name-reserved-anthropic",
    ),
]


# ---------------------------------------------------------------------------
# Tests — agent schema: positive (must PASS)
# ---------------------------------------------------------------------------


class TestAgentSchemaPositive:
    """Positive validation tests: production agent frontmatter must pass the schema."""

    @pytest.mark.parametrize("frontmatter", _AGENT_POSITIVE_FIXTURES)
    def test_valid_agent_frontmatter_passes(self, frontmatter: dict) -> None:
        """Production agent frontmatter extracted from live files validates without error.

        Args:
            frontmatter: Parsed agent frontmatter dict from a production agent .md file.
        """
        validate(instance=frontmatter, schema=AGENT_SCHEMA)


# ---------------------------------------------------------------------------
# Tests — agent schema: negative (must FAIL)
# ---------------------------------------------------------------------------


class TestAgentSchemaNegative:
    """Negative validation tests: each invalid definition must raise ValidationError."""

    @pytest.mark.parametrize("frontmatter,expected_reason", _AGENT_NEGATIVE_FIXTURES)
    def test_invalid_agent_frontmatter_fails(self, frontmatter: dict, expected_reason: str) -> None:
        """Invalid agent frontmatter must raise ValidationError.

        Args:
            frontmatter: Frontmatter dict containing a deliberate schema violation.
            expected_reason: Human-readable description of the expected constraint
                that should be violated.
        """
        with pytest.raises(ValidationError):
            validate(instance=frontmatter, schema=AGENT_SCHEMA)


# ---------------------------------------------------------------------------
# Tests — skill schema: positive (must PASS)
# ---------------------------------------------------------------------------


class TestSkillSchemaPositive:
    """Positive validation tests: production SKILL.md frontmatter must pass the schema."""

    @pytest.mark.parametrize("frontmatter", _SKILL_POSITIVE_FIXTURES)
    def test_valid_skill_frontmatter_passes(self, frontmatter: dict) -> None:
        """Production skill frontmatter extracted from live SKILL.md files validates without error.

        Args:
            frontmatter: Parsed skill frontmatter dict from a production SKILL.md file.
        """
        validate(instance=frontmatter, schema=SKILL_SCHEMA)


# ---------------------------------------------------------------------------
# Tests — skill schema: negative (must FAIL)
# ---------------------------------------------------------------------------


class TestSkillSchemaNegative:
    """Negative validation tests: each invalid skill definition must raise ValidationError."""

    @pytest.mark.parametrize("frontmatter,expected_reason", _SKILL_NEGATIVE_FIXTURES)
    def test_invalid_skill_frontmatter_fails(self, frontmatter: dict, expected_reason: str) -> None:
        """Invalid skill frontmatter must raise ValidationError.

        Args:
            frontmatter: Frontmatter dict containing a deliberate schema violation.
            expected_reason: Human-readable description of the expected constraint
                that should be violated.
        """
        with pytest.raises(ValidationError):
            validate(instance=frontmatter, schema=SKILL_SCHEMA)


# ---------------------------------------------------------------------------
# Tests — live file round-trip (parse then validate)
# ---------------------------------------------------------------------------


class TestLiveFileFrontmatterRoundTrip:
    """Round-trip tests: parse frontmatter from disk and validate against schema.

    These tests catch drift between the hard-coded positive fixtures and the
    actual files on disk.  If a production file changes its frontmatter, these
    tests will fail before the static fixtures can mask the regression.
    """

    @pytest.mark.parametrize(
        "rel_path",
        [
            "skills/problem-solving/agents/ps-researcher.md",
            "skills/adversary/agents/adv-scorer.md",
            "skills/eng-team/agents/eng-architect.md",
        ],
    )
    def test_agent_file_frontmatter_is_valid(self, rel_path: str) -> None:
        """Frontmatter extracted from a live agent .md file passes agent schema.

        Args:
            rel_path: Repository-relative path to the agent .md file.
        """
        path = REPO_ROOT / rel_path
        frontmatter = _extract_frontmatter(path)
        assert frontmatter, f"No frontmatter found in {rel_path}"
        validate(instance=frontmatter, schema=AGENT_SCHEMA)

    @pytest.mark.parametrize(
        "rel_path",
        [
            "skills/problem-solving/SKILL.md",
            "skills/adversary/SKILL.md",
        ],
    )
    def test_skill_file_frontmatter_is_valid(self, rel_path: str) -> None:
        """Frontmatter extracted from a live SKILL.md file passes skill schema.

        Args:
            rel_path: Repository-relative path to the SKILL.md file.
        """
        path = REPO_ROOT / rel_path
        frontmatter = _extract_frontmatter(path)
        assert frontmatter, f"No frontmatter found in {rel_path}"
        validate(instance=frontmatter, schema=SKILL_SCHEMA)


# ---------------------------------------------------------------------------
# Tests — schema file integrity
# ---------------------------------------------------------------------------


class TestSchemaFileIntegrity:
    """Sanity checks that the schema files themselves are well-formed."""

    def test_agent_schema_is_valid_json(self) -> None:
        """Agent schema file must be parseable as JSON without error."""
        raw = AGENT_SCHEMA_PATH.read_text(encoding="utf-8")
        parsed = json.loads(raw)
        assert isinstance(parsed, dict)

    def test_skill_schema_is_valid_json(self) -> None:
        """Skill schema file must be parseable as JSON without error."""
        raw = SKILL_SCHEMA_PATH.read_text(encoding="utf-8")
        parsed = json.loads(raw)
        assert isinstance(parsed, dict)

    def test_agent_schema_requires_name_and_description(self) -> None:
        """Agent schema must declare 'name' and 'description' as required fields."""
        required = AGENT_SCHEMA.get("required", [])
        assert "name" in required, "Agent schema must require 'name'"
        assert "description" in required, "Agent schema must require 'description'"

    def test_skill_schema_has_name_with_max_length(self) -> None:
        """Skill schema must constrain 'name' with a maxLength of 64."""
        name_schema = SKILL_SCHEMA.get("properties", {}).get("name", {})
        assert name_schema.get("maxLength") == 64, (
            "Skill schema 'name' property must have maxLength=64"
        )

    def test_agent_schema_has_effort_enum(self) -> None:
        """Agent schema must enumerate valid 'effort' values."""
        effort_schema = AGENT_SCHEMA.get("properties", {}).get("effort", {})
        enum_values = effort_schema.get("enum", [])
        assert set(enum_values) == {"low", "medium", "high", "max"}, (
            "Agent schema 'effort' enum must be exactly {low, medium, high, max}"
        )

    def test_skill_schema_has_shell_enum(self) -> None:
        """Skill schema must enumerate valid 'shell' values."""
        shell_schema = SKILL_SCHEMA.get("properties", {}).get("shell", {})
        enum_values = shell_schema.get("enum", [])
        assert set(enum_values) == {"bash", "powershell"}, (
            "Skill schema 'shell' enum must be exactly {bash, powershell}"
        )

    def test_agent_schema_has_permission_mode_enum(self) -> None:
        """Agent schema must enumerate valid 'permissionMode' values."""
        pm_schema = AGENT_SCHEMA.get("properties", {}).get("permissionMode", {})
        enum_values = pm_schema.get("enum", [])
        assert set(enum_values) == {
            "default",
            "acceptEdits",
            "dontAsk",
            "bypassPermissions",
            "plan",
        }, "Agent schema 'permissionMode' enum must include all 5 documented values"


# ---------------------------------------------------------------------------
# Tests — CLI integration (jerry agents validate-frontmatter)
# ---------------------------------------------------------------------------


class TestCLIValidateFrontmatter:
    """Integration tests for the `jerry agents validate-frontmatter` CLI command."""

    def test_cli_validate_all_exits_zero(self) -> None:
        """Full corpus validation via CLI handler returns zero failures."""
        from src.agents.application.commands.validate_frontmatter_command import (
            ValidateFrontmatterCommand,
        )
        from src.agents.application.commands.validate_frontmatter_command_handler import (
            ValidateFrontmatterCommandHandler,
        )

        handler = ValidateFrontmatterCommandHandler(
            repo_root=REPO_ROOT,
            agent_schema_path=AGENT_SCHEMA_PATH,
            skill_schema_path=SKILL_SCHEMA_PATH,
        )
        command = ValidateFrontmatterCommand(repo_root=REPO_ROOT)
        result = handler.handle(command)
        assert result.failed == 0, f"Expected 0 failures, got {result.failed}: " + ", ".join(
            r.relative_path for r in result.all_results if r.status == "fail"
        )

    def test_cli_validate_single_agent_filter(self) -> None:
        """Single agent filter returns exactly one agent result."""
        from src.agents.application.commands.validate_frontmatter_command import (
            ValidateFrontmatterCommand,
        )
        from src.agents.application.commands.validate_frontmatter_command_handler import (
            ValidateFrontmatterCommandHandler,
        )

        handler = ValidateFrontmatterCommandHandler(
            repo_root=REPO_ROOT,
            agent_schema_path=AGENT_SCHEMA_PATH,
            skill_schema_path=SKILL_SCHEMA_PATH,
        )
        command = ValidateFrontmatterCommand(repo_root=REPO_ROOT, agent_filter="ps-researcher")
        result = handler.handle(command)
        assert len(result.agent_results) == 1
        assert result.agent_results[0].relative_path.endswith("ps-researcher.md")

    def test_cli_json_output_is_valid_json(self) -> None:
        """JSON output mode produces parseable JSON with expected keys."""
        import json as json_mod
        import subprocess

        proc = subprocess.run(
            [
                "uv",
                "run",
                "jerry",
                "--json",
                "agents",
                "validate-frontmatter",
                "--agent",
                "ps-researcher",
            ],
            capture_output=True,
            text=True,
            cwd=str(REPO_ROOT),
            timeout=30,
        )
        assert proc.returncode == 0, f"CLI failed: {proc.stderr}"
        data = json_mod.loads(proc.stdout)
        assert "total" in data or "passed" in data, f"Unexpected JSON keys: {list(data.keys())}"
        assert data.get("failed", data.get("fail_count", 0)) == 0
