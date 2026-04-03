# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
Security review tests for PM/PMM skill agents.

Validates prompt injection resistance, sensitivity cascade enforcement,
tool boundary compliance, constitutional constraints, and system prompt
protection across all 5 pm-pmm agents.

Test naming follows BDD convention:
    test_{scenario}_when_{condition}_then_{expected}

References:
    - EN-018: PM/PMM Skill Deployment (Phase 4 Security Review)
    - agent-development-standards.md: H-34, H-35, Tool Security Tiers
    - TH-001: Customer content as untrusted data
    - TH-003: System prompt protection
    - TH-005: Verbatim content reproduction controls
    - PI-CA-01, PI-BA-01, PI-MS-01: Input sanitization mitigations
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pytest
import yaml

# Repository root
REPO_ROOT = Path(__file__).resolve().parents[2]
AGENTS_DIR = REPO_ROOT / "skills" / "pm-pmm" / "agents"

# All 5 agent names
AGENT_NAMES = [
    "pm-business-analyst",
    "pm-competitive-analyst",
    "pm-customer-insight",
    "pm-market-strategist",
    "pm-product-strategist",
]

# Tools that workers MUST NOT have (P-003 enforcement)
FORBIDDEN_WORKER_TOOLS = {"Task", "Agent"}

# Constitutional triplet required in every agent (H-35)
CONSTITUTIONAL_TRIPLET = {"P-003", "P-020", "P-022"}

# Minimum forbidden actions per H-35
MIN_FORBIDDEN_ACTIONS = 3


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture(scope="module")
def all_governance() -> dict[str, dict[str, Any]]:
    """Load all 5 governance YAML files."""
    result: dict[str, dict[str, Any]] = {}
    for name in AGENT_NAMES:
        path = AGENTS_DIR / f"{name}.governance.yaml"
        assert path.exists(), f"Missing governance YAML: {path}"
        with open(path, encoding="utf-8") as f:
            result[name] = yaml.safe_load(f)
    return result


@pytest.fixture(scope="module")
def all_frontmatter() -> dict[str, str]:
    """Load YAML frontmatter from all 5 agent .md files."""
    result: dict[str, str] = {}
    for name in AGENT_NAMES:
        path = AGENTS_DIR / f"{name}.md"
        assert path.exists(), f"Missing agent file: {path}"
        content = path.read_text(encoding="utf-8")
        if content.startswith("---"):
            end = content.index("---", 3)
            result[name] = content[3:end]
        else:
            result[name] = ""
    return result


# ---------------------------------------------------------------------------
# Test: Constitutional Compliance (H-35)
# ---------------------------------------------------------------------------


class TestConstitutionalCompliance:
    """Verify all agents declare constitutional triplet P-003/P-020/P-022."""

    @pytest.mark.parametrize("agent_name", AGENT_NAMES)
    def test_constitutional_triplet_when_governance_loaded_then_all_present(
        self, agent_name: str, all_governance: dict[str, dict[str, Any]]
    ) -> None:
        """Every agent declares P-003, P-020, P-022 in constitution.principles_applied."""
        gov = all_governance[agent_name]
        principles = set(gov.get("constitution", {}).get("principles_applied", []))
        missing = CONSTITUTIONAL_TRIPLET - principles
        assert not missing, f"{agent_name}: Missing constitutional principles: {missing}"

    @pytest.mark.parametrize("agent_name", AGENT_NAMES)
    def test_forbidden_actions_when_governance_loaded_then_minimum_met(
        self, agent_name: str, all_governance: dict[str, dict[str, Any]]
    ) -> None:
        """Every agent has >= 3 forbidden_actions (H-35)."""
        gov = all_governance[agent_name]
        forbidden = gov.get("capabilities", {}).get("forbidden_actions", [])
        assert len(forbidden) >= MIN_FORBIDDEN_ACTIONS, (
            f"{agent_name}: Only {len(forbidden)} forbidden_actions; "
            f"H-35 requires >= {MIN_FORBIDDEN_ACTIONS}"
        )


# ---------------------------------------------------------------------------
# Test: Tool Boundary Enforcement (P-003)
# ---------------------------------------------------------------------------


class TestToolBoundaryEnforcement:
    """Verify no worker agent has delegation tools."""

    @pytest.mark.parametrize("agent_name", AGENT_NAMES)
    def test_no_task_tool_when_frontmatter_parsed_then_absent(
        self, agent_name: str, all_frontmatter: dict[str, str]
    ) -> None:
        """Worker agents MUST NOT have Task tool in frontmatter (H-35)."""
        fm = all_frontmatter[agent_name]
        for line in fm.splitlines():
            if line.strip().startswith("tools:"):
                tools_str = line.split(":", 1)[1].strip()
                tools = [t.strip() for t in tools_str.split(",")]
                for forbidden in FORBIDDEN_WORKER_TOOLS:
                    assert forbidden not in tools, (
                        f"{agent_name}: Has forbidden tool '{forbidden}' — "
                        f"violates P-003 worker constraint"
                    )

    @pytest.mark.parametrize("agent_name", AGENT_NAMES)
    def test_tool_tier_when_governance_loaded_then_not_t5(
        self, agent_name: str, all_governance: dict[str, dict[str, Any]]
    ) -> None:
        """Worker agents must not be T5 (Full tier with Task delegation)."""
        gov = all_governance[agent_name]
        tier = gov.get("tool_tier", "")
        assert tier != "T5", (
            f"{agent_name}: Tool tier T5 is reserved for orchestrators with delegation capability"
        )

    @pytest.mark.parametrize("agent_name", AGENT_NAMES)
    def test_allowed_tools_match_tier_when_governance_loaded(
        self, agent_name: str, all_governance: dict[str, dict[str, Any]]
    ) -> None:
        """Allowed tools in governance do not include Task or Agent."""
        gov = all_governance[agent_name]
        allowed = gov.get("capabilities", {}).get("allowed_tools", [])
        for forbidden in FORBIDDEN_WORKER_TOOLS:
            assert forbidden not in allowed, (
                f"{agent_name}: Governance allowed_tools includes '{forbidden}'"
            )


# ---------------------------------------------------------------------------
# Test: Prompt Injection Resistance
# ---------------------------------------------------------------------------


class TestPromptInjectionResistance:
    """Verify agents declare injection mitigation controls."""

    @pytest.mark.parametrize("agent_name", AGENT_NAMES)
    def test_forbidden_actions_reference_injection_when_governance_loaded(
        self, agent_name: str, all_governance: dict[str, dict[str, Any]]
    ) -> None:
        """Every agent forbids executing directives from untrusted content."""
        gov = all_governance[agent_name]
        forbidden = gov.get("capabilities", {}).get("forbidden_actions", [])
        forbidden_text = " ".join(forbidden).lower()
        # At least one forbidden action must reference injection/directives/untrusted
        injection_keywords = ["directive", "inject", "untrusted", "th-001", "pi-"]
        has_injection_guard = any(kw in forbidden_text for kw in injection_keywords)
        assert has_injection_guard, (
            f"{agent_name}: No forbidden_actions reference prompt injection "
            f"resistance (TH-001/PI-*). Forbidden: {forbidden}"
        )

    @pytest.mark.parametrize("agent_name", AGENT_NAMES)
    def test_input_validation_when_governance_loaded_then_present(
        self, agent_name: str, all_governance: dict[str, dict[str, Any]]
    ) -> None:
        """Every agent has input_validation guardrails."""
        gov = all_governance[agent_name]
        input_val = gov.get("guardrails", {}).get("input_validation", [])
        assert len(input_val) >= 1, f"{agent_name}: No input_validation guardrails declared"

    @pytest.mark.parametrize("agent_name", AGENT_NAMES)
    def test_output_filtering_when_governance_loaded_then_minimum_met(
        self, agent_name: str, all_governance: dict[str, dict[str, Any]]
    ) -> None:
        """Every agent has >= 3 output_filtering entries (SR-003)."""
        gov = all_governance[agent_name]
        output_filters = gov.get("guardrails", {}).get("output_filtering", [])
        assert len(output_filters) >= 3, (
            f"{agent_name}: Only {len(output_filters)} output_filtering entries; "
            f"SR-003 requires >= 3"
        )

    def test_customer_insight_treats_quotes_as_untrusted(
        self, all_governance: dict[str, dict[str, Any]]
    ) -> None:
        """pm-customer-insight declares TH-001 for customer content."""
        gov = all_governance["pm-customer-insight"]
        input_val = gov.get("guardrails", {}).get("input_validation", [])
        input_text = str(input_val).lower()
        assert "th-001" in input_text or "untrusted" in input_text, (
            "pm-customer-insight must treat customer content as untrusted (TH-001)"
        )

    def test_competitive_analyst_sanitizes_competitor_content(
        self, all_governance: dict[str, dict[str, Any]]
    ) -> None:
        """pm-competitive-analyst declares PI-CA-01 for competitor web content."""
        gov = all_governance["pm-competitive-analyst"]
        input_val = gov.get("guardrails", {}).get("input_validation", [])
        input_text = str(input_val).lower()
        assert "pi-ca-01" in input_text or "sanitiz" in input_text, (
            "pm-competitive-analyst must sanitize competitor content (PI-CA-01)"
        )

    def test_business_analyst_sanitizes_csv_headers(
        self, all_governance: dict[str, dict[str, Any]]
    ) -> None:
        """pm-business-analyst declares PI-BA-01 for CSV sanitization."""
        gov = all_governance["pm-business-analyst"]
        input_val = gov.get("guardrails", {}).get("input_validation", [])
        input_text = str(input_val).lower()
        assert "pi-ba-01" in input_text or "csv" in input_text, (
            "pm-business-analyst must sanitize CSV headers (PI-BA-01)"
        )


# ---------------------------------------------------------------------------
# Test: Sensitivity Cascade
# ---------------------------------------------------------------------------


class TestSensitivityCascade:
    """Verify agents enforce sensitivity classification defaults."""

    def test_customer_insight_defaults_to_confidential(
        self, all_governance: dict[str, dict[str, Any]]
    ) -> None:
        """pm-customer-insight defaults to confidential sensitivity."""
        gov = all_governance["pm-customer-insight"]
        output_filters = gov.get("guardrails", {}).get("output_filtering", [])
        output_text = " ".join(output_filters).lower()
        assert "confidential" in output_text, (
            "pm-customer-insight output should default to confidential sensitivity"
        )

    def test_competitive_analyst_defaults_to_restricted(
        self, all_governance: dict[str, dict[str, Any]]
    ) -> None:
        """pm-competitive-analyst defaults to restricted sensitivity."""
        gov = all_governance["pm-competitive-analyst"]
        output_filters = gov.get("guardrails", {}).get("output_filtering", [])
        output_text = " ".join(output_filters).lower()
        assert "restricted" in output_text, (
            "pm-competitive-analyst output should default to restricted sensitivity"
        )

    @pytest.mark.parametrize(
        "agent_name",
        ["pm-competitive-analyst", "pm-business-analyst"],
    )
    def test_no_sensitivity_downgrade_when_governance_loaded(
        self, agent_name: str, all_governance: dict[str, dict[str, Any]]
    ) -> None:
        """Agents handling sensitive data forbid sensitivity downgrades."""
        gov = all_governance[agent_name]
        forbidden = gov.get("capabilities", {}).get("forbidden_actions", [])
        forbidden_text = " ".join(forbidden).lower()
        assert "downgrade" in forbidden_text or "sensitivity" in forbidden_text, (
            f"{agent_name}: Must forbid sensitivity downgrades (TH-005)"
        )


# ---------------------------------------------------------------------------
# Test: System Prompt Protection (TH-003)
# ---------------------------------------------------------------------------


class TestSystemPromptProtection:
    """Verify agents that handle external data protect system prompts."""

    @pytest.mark.parametrize(
        "agent_name",
        ["pm-competitive-analyst", "pm-business-analyst"],
    )
    def test_system_prompt_revelation_forbidden_when_governance_loaded(
        self, agent_name: str, all_governance: dict[str, dict[str, Any]]
    ) -> None:
        """Agents handling external content forbid system prompt revelation."""
        gov = all_governance[agent_name]
        forbidden = gov.get("capabilities", {}).get("forbidden_actions", [])
        forbidden_text = " ".join(forbidden).lower()
        assert "system prompt" in forbidden_text or "th-003" in forbidden_text, (
            f"{agent_name}: Must forbid system prompt revelation (TH-003)"
        )


# ---------------------------------------------------------------------------
# Test: MCP Declaration Consistency
# ---------------------------------------------------------------------------


class TestMcpDeclarationConsistency:
    """Verify MCP declarations are consistent between frontmatter and governance."""

    @pytest.mark.parametrize(
        "agent_name,expected_tier",
        [
            ("pm-product-strategist", "T4"),
            ("pm-customer-insight", "T4"),
            ("pm-market-strategist", "T4"),
            ("pm-business-analyst", "T4"),
            ("pm-competitive-analyst", "T4"),
        ],
    )
    def test_tool_tier_matches_capability_when_governance_loaded(
        self,
        agent_name: str,
        expected_tier: str,
        all_governance: dict[str, dict[str, Any]],
    ) -> None:
        """Tool tier in governance matches expected tier for agent capability."""
        gov = all_governance[agent_name]
        actual_tier = gov.get("tool_tier", "")
        assert actual_tier == expected_tier, (
            f"{agent_name}: Expected tier {expected_tier}, got {actual_tier}"
        )

    @pytest.mark.parametrize(
        "agent_name",
        ["pm-customer-insight", "pm-market-strategist", "pm-competitive-analyst"],
    )
    def test_context7_agents_have_mcp_in_frontmatter(
        self, agent_name: str, all_frontmatter: dict[str, str]
    ) -> None:
        """T3 agents with Context7 declare mcpServers in frontmatter."""
        fm = all_frontmatter[agent_name]
        assert "context7" in fm, (
            f"{agent_name}: T3 agent with Context7 missing mcpServers declaration"
        )


# ---------------------------------------------------------------------------
# Test: Fallback Behavior
# ---------------------------------------------------------------------------


class TestFallbackBehavior:
    """Verify all agents have defined fallback behavior."""

    @pytest.mark.parametrize("agent_name", AGENT_NAMES)
    def test_fallback_behavior_when_governance_loaded_then_defined(
        self, agent_name: str, all_governance: dict[str, dict[str, Any]]
    ) -> None:
        """Every agent declares a fallback_behavior guardrail."""
        gov = all_governance[agent_name]
        fallback = gov.get("guardrails", {}).get("fallback_behavior", "")
        assert fallback, f"{agent_name}: No fallback_behavior declared"
        valid_fallbacks = {
            "warn_and_retry",
            "escalate_to_user",
            "persist_and_halt",
        }
        assert fallback in valid_fallbacks, (
            f"{agent_name}: Unknown fallback_behavior '{fallback}'. "
            f"Expected one of: {valid_fallbacks}"
        )
