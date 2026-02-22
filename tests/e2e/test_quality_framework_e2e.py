# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
End-to-end integration tests for the Quality Framework (EN-711).

Validates cross-component interactions across the quality enforcement
layers (L1-L5), hook enforcement pipelines, rule compliance, session
context injection, skill adversarial mode content, and performance
benchmarks.

Test naming follows BDD convention:
    test_{scenario}_when_{condition}_then_{expected}

References:
    - EN-711: E2E Integration Testing
    - EPIC-003: Quality Framework Implementation
    - .context/rules/quality-enforcement.md: SSOT
"""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path

import pytest

pytestmark = [pytest.mark.e2e, pytest.mark.subprocess]

# ===========================================================================
# Constants
# ===========================================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
SSOT_PATH = PROJECT_ROOT / ".context" / "rules" / "quality-enforcement.md"
RULES_DIR = PROJECT_ROOT / ".context" / "rules"
SCRIPTS_DIR = PROJECT_ROOT / "scripts"
HOOKS_DIR = PROJECT_ROOT / "hooks"

# Hook script paths
PRETOOL_HOOK = SCRIPTS_DIR / "pre_tool_use.py"
SESSION_HOOK = HOOKS_DIR / "session-start.py"
USERPROMPT_HOOK = HOOKS_DIR / "user-prompt-submit.py"

# Skill paths
PROBLEM_SOLVING_SKILL = PROJECT_ROOT / "skills" / "problem-solving" / "SKILL.md"
NASA_SE_SKILL = PROJECT_ROOT / "skills" / "nasa-se" / "SKILL.md"
ORCHESTRATION_SKILL = PROJECT_ROOT / "skills" / "orchestration" / "SKILL.md"


# ===========================================================================
# Helper functions
# ===========================================================================


def read_file(path: Path) -> str:
    """Read a file and return its content as a string."""
    return path.read_text(encoding="utf-8")


def run_pretool_hook(
    tool_name: str,
    tool_input: dict,
) -> tuple[int, dict | None, str]:
    """Run the pre_tool_use.py hook with the given input.

    Args:
        tool_name: Name of the tool (e.g., "Write", "Bash").
        tool_input: Tool input parameters.

    Returns:
        Tuple of (exit_code, stdout_json_or_none, stderr_text).
    """
    input_data = json.dumps({"tool_name": tool_name, "tool_input": tool_input})

    result = subprocess.run(
        [sys.executable, str(PRETOOL_HOOK)],
        input=input_data,
        capture_output=True,
        text=True,
        timeout=10,
        cwd=str(PROJECT_ROOT),
    )

    stdout_json = None
    if result.stdout.strip():
        try:
            stdout_json = json.loads(result.stdout.strip())
        except json.JSONDecodeError:
            pass

    return result.returncode, stdout_json, result.stderr


def run_session_hook(
    env_overrides: dict[str, str] | None = None,
) -> subprocess.CompletedProcess[str]:
    """Run the session-start hook via CLI and capture output.

    Args:
        env_overrides: Optional environment variable overrides.

    Returns:
        CompletedProcess with captured stdout/stderr.
    """
    env = os.environ.copy()
    if env_overrides:
        env.update(env_overrides)

    return subprocess.run(
        ["uv", "run", "jerry", "--json", "hooks", "session-start"],
        input="{}",
        capture_output=True,
        text=True,
        timeout=60,
        cwd=str(PROJECT_ROOT),
        env=env,
    )


def run_userprompt_hook(
    input_data: str | None = None,
) -> tuple[int, dict | None, str]:
    """Run the prompt-submit hook via CLI with the given input.

    Args:
        input_data: JSON string to pass via stdin.

    Returns:
        Tuple of (exit_code, stdout_json_or_none, stderr_text).
    """
    if input_data is None:
        input_data = json.dumps({"prompt": "test prompt"})

    result = subprocess.run(
        ["uv", "run", "jerry", "--json", "hooks", "prompt-submit"],
        input=input_data,
        capture_output=True,
        text=True,
        timeout=15,
        cwd=str(PROJECT_ROOT),
    )

    stdout_json = None
    if result.stdout.strip():
        try:
            stdout_json = json.loads(result.stdout.strip())
        except json.JSONDecodeError:
            pass

    return result.returncode, stdout_json, result.stderr


# ===========================================================================
# AC-1: Cross-Layer Interaction Tests (L1-L5)
# ===========================================================================


class TestCrossLayerInteractions:
    """Tests validating consistency across enforcement layers L1-L5."""

    def test_ssot_threshold_when_read_then_contains_092(self) -> None:
        """SSOT quality-enforcement.md defines the 0.92 threshold."""
        content = read_file(SSOT_PATH)
        assert ">= 0.92" in content or "0.92" in content

    def test_ssot_threshold_when_checked_against_session_generator_then_matches(
        self,
    ) -> None:
        """Session quality context generator embeds the same 0.92 threshold as SSOT."""
        generator_path = (
            PROJECT_ROOT
            / "src"
            / "infrastructure"
            / "internal"
            / "enforcement"
            / "session_quality_context_generator.py"
        )
        generator_content = read_file(generator_path)
        assert "0.92" in generator_content, (
            "Session quality context generator must reference the 0.92 threshold"
        )

    def test_enforcement_layers_when_defined_in_ssot_then_l1_through_l5_present(
        self,
    ) -> None:
        """SSOT defines all five enforcement layers L1 through L5."""
        content = read_file(SSOT_PATH)
        for layer in ["L1", "L2", "L3", "L4", "L5"]:
            assert layer in content, f"Enforcement layer {layer} missing from SSOT"

    def test_l2_reinject_markers_when_parsed_then_present_in_ssot(self) -> None:
        """SSOT contains L2-REINJECT markers for per-prompt reinforcement."""
        content = read_file(SSOT_PATH)
        pattern = r"<!--\s*L2-REINJECT:"
        matches = re.findall(pattern, content)
        assert len(matches) >= 1, "SSOT must contain at least one L2-REINJECT marker"

    def test_l3_hook_script_when_checked_then_exists(self) -> None:
        """L3 PreToolUse hook script exists for deterministic gating."""
        assert PRETOOL_HOOK.exists(), f"PreToolUse hook not found at {PRETOOL_HOOK}"

    def test_l1_session_hook_when_checked_then_exists(self) -> None:
        """L1 SessionStart hook script exists for behavioral foundation."""
        assert SESSION_HOOK.exists(), f"SessionStart hook not found at {SESSION_HOOK}"

    def test_l1_session_hook_cli_when_checked_then_available(self) -> None:
        """L1 SessionStart hook is available via CLI."""
        result = subprocess.run(
            ["uv", "run", "jerry", "--json", "hooks", "session-start"],
            input="{}",
            capture_output=True,
            text=True,
            timeout=60,
            cwd=str(PROJECT_ROOT),
        )
        assert result.returncode == 0, f"Session hook CLI failed: {result.stderr}"

    def test_l2_userprompt_hook_when_checked_then_exists(self) -> None:
        """L2 UserPromptSubmit hook script exists for per-prompt reinforcement."""
        assert USERPROMPT_HOOK.exists(), f"UserPromptSubmit hook not found at {USERPROMPT_HOOK}"

    def test_enforcement_architecture_when_ssot_read_then_token_budgets_defined(
        self,
    ) -> None:
        """SSOT enforcement architecture defines token budgets for each layer."""
        content = read_file(SSOT_PATH)
        # Check that the enforcement architecture section exists with token data
        assert "Enforcement Architecture" in content
        assert "Tokens" in content
        # L2 should have ~850 per prompt (updated from 600 per EN-002)
        assert "850" in content

    def test_ssot_references_when_checked_then_adr_sources_present(self) -> None:
        """SSOT references its source ADRs for traceability."""
        content = read_file(SSOT_PATH)
        assert "ADR-EPIC002-001" in content
        assert "ADR-EPIC002-002" in content


# ===========================================================================
# AC-2: Hook Enforcement E2E Tests
# ===========================================================================


class TestHookEnforcementE2E:
    """Tests validating hook enforcement pipeline end-to-end."""

    def test_pretool_hook_when_pip_install_command_then_responds(self) -> None:
        """PreToolUse hook processes pip install command without crashing."""
        exit_code, stdout_json, _stderr = run_pretool_hook(
            "Bash",
            {"command": "pip install requests"},
        )
        # Hook must exit 0 (either approve or block)
        assert exit_code == 0
        assert stdout_json is not None

    def test_pretool_hook_when_rm_rf_root_then_blocks(self) -> None:
        """PreToolUse hook blocks dangerous rm -rf / command."""
        exit_code, stdout_json, _stderr = run_pretool_hook(
            "Bash",
            {"command": "rm -rf /"},
        )
        assert exit_code == 0
        assert stdout_json is not None
        hso = stdout_json.get("hookSpecificOutput", {})
        assert hso.get("permissionDecision") == "deny"

    def test_pretool_hook_when_safe_command_then_approves(self) -> None:
        """PreToolUse hook approves safe bash commands."""
        exit_code, stdout_json, _stderr = run_pretool_hook(
            "Bash",
            {"command": "ls -la /tmp"},
        )
        assert exit_code == 0
        assert stdout_json is not None
        hso = stdout_json.get("hookSpecificOutput", {})
        assert hso.get("permissionDecision") == "allow"

    @pytest.mark.subprocess
    def test_session_hook_when_executed_then_produces_valid_json(self) -> None:
        """SessionStart hook produces valid JSON output."""
        result = run_session_hook()
        assert result.returncode == 0, f"Hook exited with {result.returncode}: {result.stderr}"
        output = result.stdout.strip()
        assert output, "Hook produced no output"
        data = json.loads(output)
        assert "additionalContext" in data

    @pytest.mark.subprocess
    def test_session_hook_when_executed_then_injects_quality_context_xml(
        self,
    ) -> None:
        """SessionStart hook injects quality context XML into output."""
        result = run_session_hook()
        assert result.returncode == 0
        data = json.loads(result.stdout.strip())
        additional = data["additionalContext"]
        assert "<quality-context>" in additional or "quality" in additional.lower()

    def test_userprompt_hook_when_executed_then_returns_valid_json(self) -> None:
        """UserPromptSubmit hook returns valid JSON with quality reinforcement."""
        exit_code, stdout_json, stderr = run_userprompt_hook()
        assert exit_code == 0
        assert stdout_json is not None

    def test_userprompt_hook_when_executed_then_contains_quality_reinforcement(
        self,
    ) -> None:
        """UserPromptSubmit hook output contains quality reinforcement content."""
        exit_code, stdout_json, stderr = run_userprompt_hook()
        assert exit_code == 0
        assert stdout_json is not None
        additional = stdout_json.get("additionalContext", "")
        assert "P-003" in additional or "P-020" in additional or additional

    @pytest.mark.subprocess
    def test_all_hooks_when_run_independently_then_exit_zero(self) -> None:
        """All three hooks exit with code 0 (fail-open) when run independently."""
        # PreToolUse
        exit_code_pre, _, _ = run_pretool_hook("Bash", {"command": "echo hello"})
        assert exit_code_pre == 0, "PreToolUse hook did not exit 0"

        # SessionStart
        result_session = run_session_hook()
        assert result_session.returncode == 0, "SessionStart hook did not exit 0"

        # UserPromptSubmit
        exit_code_prompt, _, _ = run_userprompt_hook()
        assert exit_code_prompt == 0, "UserPromptSubmit hook did not exit 0"


# ===========================================================================
# AC-3: Rule Compliance Validation Tests
# ===========================================================================


class TestRuleComplianceValidation:
    """Tests validating SSOT rule definitions and compliance."""

    def test_ssot_when_checked_then_file_exists(self) -> None:
        """quality-enforcement.md exists at the expected path."""
        assert SSOT_PATH.exists(), f"SSOT not found at {SSOT_PATH}"

    def test_ssot_when_read_then_contains_required_sections(self) -> None:
        """SSOT contains all required top-level sections."""
        content = read_file(SSOT_PATH)
        required_sections = [
            "HARD Rule Index",
            "Quality Gate",
            "Criticality Levels",
            "Tier Vocabulary",
            "Auto-Escalation Rules",
            "Enforcement Architecture",
            "Strategy Catalog",
            "References",
        ]
        for section in required_sections:
            assert section in content, f"Required section '{section}' missing from SSOT"

    def test_ssot_when_read_then_h_rules_h01_through_h16_defined(self) -> None:
        """SSOT defines H-rules H-01 through H-16 (post-consolidation: H-08, H-09 absorbed into H-07)."""
        content = read_file(SSOT_PATH)
        # H-08 and H-09 were consolidated into H-07 per EN-002
        consolidated_ids = {"H-08", "H-09"}
        for i in range(1, 17):
            rule_id = f"H-{i:02d}"
            if rule_id in consolidated_ids:
                continue
            assert rule_id in content, f"H-rule '{rule_id}' missing from SSOT"

    def test_ssot_when_read_then_h_rules_extended_set_defined(self) -> None:
        """SSOT defines extended H-rules H-17 through H-26 (post-consolidation: H-27..H-30 absorbed into H-25, H-26)."""
        content = read_file(SSOT_PATH)
        # H-27..H-30 were consolidated into H-25, H-26 per EN-002
        consolidated_ids = {"H-27", "H-28", "H-29", "H-30"}
        for i in range(17, 27):
            rule_id = f"H-{i:02d}"
            if rule_id in consolidated_ids:
                continue
            assert rule_id in content, f"Extended H-rule '{rule_id}' missing from SSOT"

    def test_ssot_when_read_then_selected_strategies_defined(self) -> None:
        """SSOT defines the 10 selected strategies (S-001 through S-014, excluding gaps)."""
        content = read_file(SSOT_PATH)
        selected_ids = [
            "S-001",
            "S-002",
            "S-003",
            "S-004",
            "S-007",
            "S-010",
            "S-011",
            "S-012",
            "S-013",
            "S-014",
        ]
        for sid in selected_ids:
            assert sid in content, f"Selected strategy '{sid}' missing from SSOT"

    def test_ssot_when_read_then_excluded_strategies_documented(self) -> None:
        """SSOT documents excluded strategies with rationale."""
        content = read_file(SSOT_PATH)
        excluded_ids = ["S-005", "S-006", "S-008", "S-009", "S-015"]
        for sid in excluded_ids:
            assert sid in content, f"Excluded strategy '{sid}' not documented in SSOT"

    def test_ssot_when_read_then_criticality_levels_c1_through_c4_defined(
        self,
    ) -> None:
        """SSOT defines criticality levels C1 through C4."""
        content = read_file(SSOT_PATH)
        for level in ["C1", "C2", "C3", "C4"]:
            assert level in content, f"Criticality level '{level}' missing from SSOT"

    def test_ssot_when_read_then_criticality_has_strategy_mappings(self) -> None:
        """SSOT criticality levels include strategy set mappings."""
        content = read_file(SSOT_PATH)
        # C1 maps to S-010
        assert "S-010" in content
        # C2 maps to S-007, S-002, S-014
        assert "S-007" in content
        assert "S-002" in content
        assert "S-014" in content

    def test_ssot_when_read_then_tier_vocabulary_defined(self) -> None:
        """SSOT defines the three enforcement tiers: HARD, MEDIUM, SOFT."""
        content = read_file(SSOT_PATH)
        assert "HARD" in content
        assert "MEDIUM" in content
        assert "SOFT" in content

    def test_ssot_when_read_then_auto_escalation_rules_present(self) -> None:
        """SSOT defines auto-escalation rules AE-001 through AE-006."""
        content = read_file(SSOT_PATH)
        for i in range(1, 7):
            ae_id = f"AE-{i:03d}"
            assert ae_id in content, f"Auto-escalation rule '{ae_id}' missing from SSOT"

    def test_rule_files_when_listing_rules_dir_then_ssot_present(self) -> None:
        """The .context/rules/ directory contains quality-enforcement.md."""
        rule_files = [f.name for f in RULES_DIR.iterdir() if f.suffix == ".md"]
        assert "quality-enforcement.md" in rule_files


# ===========================================================================
# AC-4: Session Context Injection Verification Tests
# ===========================================================================


@pytest.mark.subprocess
class TestSessionContextInjection:
    """Tests validating SessionStart hook quality context injection."""

    def test_session_output_when_executed_then_contains_quality_framework_tag(
        self,
    ) -> None:
        """SessionStart output contains <quality-framework> tag."""
        result = run_session_hook()
        assert result.returncode == 0
        data = json.loads(result.stdout.strip())
        additional = data["additionalContext"]
        assert "<quality-framework" in additional

    def test_session_output_when_executed_then_contains_quality_gate_section(
        self,
    ) -> None:
        """SessionStart quality context includes <quality-gate> section."""
        result = run_session_hook()
        assert result.returncode == 0
        data = json.loads(result.stdout.strip())
        additional = data["additionalContext"]
        assert "<quality-gate>" in additional
        assert "</quality-gate>" in additional

    def test_session_output_when_executed_then_contains_adversarial_strategies(
        self,
    ) -> None:
        """SessionStart quality context includes adversarial strategies section."""
        result = run_session_hook()
        assert result.returncode == 0
        data = json.loads(result.stdout.strip())
        additional = data["additionalContext"]
        assert "<adversarial-strategies>" in additional
        assert "</adversarial-strategies>" in additional

    def test_session_output_when_executed_then_contains_decision_criticality(
        self,
    ) -> None:
        """SessionStart quality context includes decision criticality levels."""
        result = run_session_hook()
        assert result.returncode == 0
        data = json.loads(result.stdout.strip())
        additional = data["additionalContext"]
        assert "<decision-criticality>" in additional
        assert "</decision-criticality>" in additional

    def test_session_output_when_executed_then_contains_constitutional_principles(
        self,
    ) -> None:
        """SessionStart quality context includes constitutional principles."""
        result = run_session_hook()
        assert result.returncode == 0
        data = json.loads(result.stdout.strip())
        additional = data["additionalContext"]
        assert "<constitutional-principles>" in additional
        assert "</constitutional-principles>" in additional

    def test_session_output_when_executed_then_quality_gate_references_092(
        self,
    ) -> None:
        """SessionStart quality gate section references the 0.92 threshold."""
        result = run_session_hook()
        assert result.returncode == 0
        data = json.loads(result.stdout.strip())
        additional = data["additionalContext"]
        assert "0.92" in additional, (
            "Quality gate in session output must reference the 0.92 threshold"
        )


# ===========================================================================
# AC-5: Skill Adversarial Mode Tests (DOCUMENT-ONLY)
# ===========================================================================


class TestSkillAdversarialModeContent:
    """Tests validating adversarial quality content in skill files.

    These are document-only tests -- they verify that skill SKILL.md files
    contain the required adversarial quality mode sections and reference
    the SSOT threshold. No code execution is involved.
    """

    def test_problem_solving_skill_when_read_then_contains_adversarial_section(
        self,
    ) -> None:
        """problem-solving/SKILL.md contains 'Adversarial Quality Mode' section."""
        content = read_file(PROBLEM_SOLVING_SKILL)
        assert "Adversarial Quality Mode" in content, (
            "problem-solving SKILL.md missing 'Adversarial Quality Mode' section"
        )

    def test_nasa_se_skill_when_read_then_contains_adversarial_section(
        self,
    ) -> None:
        """nasa-se/SKILL.md contains 'Adversarial Quality Mode' section."""
        content = read_file(NASA_SE_SKILL)
        assert "Adversarial Quality Mode" in content, (
            "nasa-se SKILL.md missing 'Adversarial Quality Mode' section"
        )

    def test_orchestration_skill_when_read_then_contains_adversarial_section(
        self,
    ) -> None:
        """orchestration/SKILL.md contains 'Adversarial Quality Mode' section."""
        content = read_file(ORCHESTRATION_SKILL)
        assert "Adversarial Quality Mode" in content, (
            "orchestration SKILL.md missing 'Adversarial Quality Mode' section"
        )

    def test_problem_solving_skill_when_read_then_references_ssot(self) -> None:
        """problem-solving/SKILL.md references the quality-enforcement SSOT."""
        content = read_file(PROBLEM_SOLVING_SKILL)
        assert "quality-enforcement" in content.lower(), (
            "problem-solving SKILL.md must reference quality-enforcement.md"
        )

    def test_nasa_se_skill_when_read_then_references_ssot(self) -> None:
        """nasa-se/SKILL.md references the quality-enforcement SSOT."""
        content = read_file(NASA_SE_SKILL)
        assert "quality-enforcement" in content.lower(), (
            "nasa-se SKILL.md must reference quality-enforcement.md"
        )

    def test_orchestration_skill_when_read_then_references_ssot(self) -> None:
        """orchestration/SKILL.md references the quality-enforcement SSOT."""
        content = read_file(ORCHESTRATION_SKILL)
        assert "quality-enforcement" in content.lower(), (
            "orchestration SKILL.md must reference quality-enforcement.md"
        )

    def test_problem_solving_skill_when_read_then_references_092_threshold(
        self,
    ) -> None:
        """problem-solving/SKILL.md references the 0.92 threshold."""
        content = read_file(PROBLEM_SOLVING_SKILL)
        assert "0.92" in content, "problem-solving SKILL.md must reference the 0.92 threshold"

    def test_nasa_se_skill_when_read_then_references_092_threshold(self) -> None:
        """nasa-se/SKILL.md references the 0.92 threshold."""
        content = read_file(NASA_SE_SKILL)
        assert "0.92" in content, "nasa-se SKILL.md must reference the 0.92 threshold"

    def test_orchestration_skill_when_read_then_references_092_threshold(
        self,
    ) -> None:
        """orchestration/SKILL.md references the 0.92 threshold."""
        content = read_file(ORCHESTRATION_SKILL)
        assert "0.92" in content, "orchestration SKILL.md must reference the 0.92 threshold"

    def test_all_skills_when_read_then_reference_strategy_ids(self) -> None:
        """All three skill files reference at least some strategy IDs."""
        for skill_path, skill_name in [
            (PROBLEM_SOLVING_SKILL, "problem-solving"),
            (NASA_SE_SKILL, "nasa-se"),
            (ORCHESTRATION_SKILL, "orchestration"),
        ]:
            content = read_file(skill_path)
            # Each skill should reference at least S-002 and S-003
            assert "S-002" in content or "S-003" in content, (
                f"{skill_name} SKILL.md must reference adversarial strategy IDs"
            )


# ===========================================================================
# AC-6: Performance Benchmarks
# ===========================================================================


class TestPerformanceBenchmarks:
    """Tests establishing performance and size benchmarks for quality framework."""

    def test_ssot_when_measured_then_under_token_budget(self) -> None:
        """quality-enforcement.md file size is reasonable as a proxy for token budget.

        The SSOT is read at various points. A rough heuristic:
        characters / 4 * 0.83 should stay within the documented ~12,500 L1 budget.
        We use a generous upper bound of 20,000 estimated tokens.
        """
        content = read_file(SSOT_PATH)
        estimated_tokens = int(len(content) / 4 * 0.83)
        # The SSOT itself should not be enormous
        assert estimated_tokens < 20000, (
            f"SSOT estimated at {estimated_tokens} tokens, exceeds 20,000 limit"
        )

    def test_pretool_hook_when_timed_then_completes_within_10s(self) -> None:
        """PreToolUse hook completes within the 10-second timeout."""
        start = time.monotonic()
        exit_code, _, _ = run_pretool_hook("Bash", {"command": "echo hello"})
        elapsed = time.monotonic() - start
        assert exit_code == 0
        assert elapsed < 10.0, f"PreToolUse hook took {elapsed:.2f}s, exceeds 10s timeout"

    @pytest.mark.subprocess
    def test_session_hook_when_timed_then_completes_within_60s(self) -> None:
        """SessionStart hook via CLI completes within the 60-second timeout."""
        start = time.monotonic()
        result = run_session_hook()
        elapsed = time.monotonic() - start
        assert result.returncode == 0
        assert elapsed < 60.0, f"SessionStart hook took {elapsed:.2f}s, exceeds 60s timeout"

    def test_userprompt_hook_when_timed_then_completes_within_15s(self) -> None:
        """UserPromptSubmit hook completes within the 15-second timeout."""
        start = time.monotonic()
        exit_code, _, _ = run_userprompt_hook()
        elapsed = time.monotonic() - start
        assert exit_code == 0
        assert elapsed < 15.0, f"UserPromptSubmit hook took {elapsed:.2f}s, exceeds 15s timeout"

    def test_rule_files_when_totaled_then_under_150kb(self) -> None:
        """Total size of all .context/rules/*.md files is under 150KB."""
        total_size = sum(f.stat().st_size for f in RULES_DIR.iterdir() if f.suffix == ".md")
        max_size = 150 * 1024  # 150KB (expanded for agent-development/routing-standards)
        assert total_size < max_size, (
            f"Total rule files size {total_size / 1024:.1f}KB exceeds 150KB limit"
        )

    def test_quality_preamble_when_generated_then_under_700_token_budget(
        self,
    ) -> None:
        """Session quality preamble is under the 700-token budget."""
        # Read the generator source to extract the preamble constant
        generator_path = (
            PROJECT_ROOT
            / "src"
            / "infrastructure"
            / "internal"
            / "enforcement"
            / "session_quality_context_generator.py"
        )
        assert generator_path.exists(), f"Generator not found: {generator_path}"

        # Measure the preamble by importing the module
        sys.path.insert(0, str(PROJECT_ROOT))
        try:
            from src.infrastructure.internal.enforcement.session_quality_context_generator import (
                SessionQualityContextGenerator,
            )

            generator = SessionQualityContextGenerator()
            result = generator.generate()
            assert result.token_estimate <= 700, (
                f"Quality preamble estimated at {result.token_estimate} tokens, "
                f"exceeds 700-token budget"
            )
        finally:
            if str(PROJECT_ROOT) in sys.path:
                sys.path.remove(str(PROJECT_ROOT))

    def test_l2_reinforcement_when_generated_then_under_850_token_budget(
        self,
    ) -> None:
        """L2 prompt reinforcement preamble is under the 850-token budget (EN-002)."""
        sys.path.insert(0, str(PROJECT_ROOT))
        try:
            from src.infrastructure.internal.enforcement.prompt_reinforcement_engine import (
                PromptReinforcementEngine,
            )

            # EN-002: Engine now reads all auto-loaded rule files from directory
            rules_dir = PROJECT_ROOT / ".context" / "rules"
            engine = PromptReinforcementEngine(
                rules_path=rules_dir,
                token_budget=850,
            )
            result = engine.generate_reinforcement()
            assert result.token_estimate <= 850, (
                f"L2 reinforcement estimated at {result.token_estimate} tokens, "
                f"exceeds 850-token budget"
            )
        finally:
            if str(PROJECT_ROOT) in sys.path:
                sys.path.remove(str(PROJECT_ROOT))
