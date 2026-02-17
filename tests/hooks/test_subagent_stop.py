"""Tests for subagent_stop.py hook.

Comprehensive test suite covering:
1. Handoff signal parsing (parse_agent_output)
2. HANDOFF_RULES matching and mismatch warnings (determine_handoff)
3. Log handoff behavior (log_handoff)
4. Hook output schema compliance (SubagentStop schema)
5. Exit code semantics

References:
    - DA-001: Missing test suite for subagent_stop.py handoff signal parsing
    - CC-002: H-21 test coverage for subagent_stop.py unverified
    - PM-001: HANDOFF_RULES mismatch warning
    - FM-001: FMEA high-RPN failure modes
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from typing import Any

# Path to the hook script
HOOK_SCRIPT = Path(__file__).resolve().parents[2] / "scripts" / "subagent_stop.py"


# ---------------------------------------------------------------------------
# Subprocess helper
# ---------------------------------------------------------------------------


def run_hook(
    agent_name: str = "unknown",
    agent_output: str = "",
    extra_fields: dict[str, Any] | None = None,
) -> tuple[int, dict[str, Any] | None, str]:
    """Run the subagent_stop hook as a subprocess.

    Args:
        agent_name: Name of the agent that is stopping.
        agent_output: The agent's output text (may contain handoff signals).
        extra_fields: Additional fields to include in the input JSON.

    Returns:
        Tuple of (exit_code, parsed_stdout_json_or_None, stderr_text).
    """
    input_data: dict[str, Any] = {
        "agent_name": agent_name,
        "output": agent_output,
    }
    if extra_fields:
        input_data.update(extra_fields)

    result = subprocess.run(
        [sys.executable, str(HOOK_SCRIPT)],
        input=json.dumps(input_data),
        capture_output=True,
        text=True,
        timeout=10,
    )

    stdout_json = None
    if result.stdout.strip():
        try:
            stdout_json = json.loads(result.stdout.strip())
        except json.JSONDecodeError:
            pass

    return result.returncode, stdout_json, result.stderr


# ---------------------------------------------------------------------------
# Import hook module functions for unit testing
# ---------------------------------------------------------------------------

sys.path.insert(0, str(HOOK_SCRIPT.parent))
from subagent_stop import (  # noqa: E402
    HANDOFF_RULES,
    determine_handoff,
    parse_agent_output,
)

# =============================================================================
# Test: parse_agent_output
# =============================================================================


class TestParseAgentOutput:
    """Tests for handoff signal parsing from agent output text."""

    def test_parse_handoff_signal(self) -> None:
        """Parse ##HANDOFF:condition## signal."""
        output = "Some work done\n##HANDOFF:implementation_complete##\nDone."
        signals = parse_agent_output(output)

        assert signals["handoff_condition"] == "implementation_complete"

    def test_parse_workitem_signal(self) -> None:
        """Parse ##WORKITEM:ID## signal."""
        output = "##WORKITEM:WORK-123##\nCompleted task."
        signals = parse_agent_output(output)

        assert "WORK-123" in signals["work_items"]

    def test_parse_multiple_workitems(self) -> None:
        """Parse multiple ##WORKITEM:## signals."""
        output = "##WORKITEM:WORK-100##\n##WORKITEM:WORK-200##\nDone."
        signals = parse_agent_output(output)

        assert len(signals["work_items"]) == 2
        assert "WORK-100" in signals["work_items"]
        assert "WORK-200" in signals["work_items"]

    def test_parse_status_signal(self) -> None:
        """Parse ##STATUS:status## signal."""
        output = "##STATUS:IN_REVIEW##\nReady for review."
        signals = parse_agent_output(output)

        assert signals["status_update"] == "IN_REVIEW"

    def test_parse_all_signals_combined(self) -> None:
        """Parse output containing all signal types."""
        output = (
            "Summary of work\n"
            "##HANDOFF:tests_passing##\n"
            "##WORKITEM:WORK-456##\n"
            "##STATUS:TESTING_COMPLETE##\n"
            "All tests pass."
        )
        signals = parse_agent_output(output)

        assert signals["handoff_condition"] == "tests_passing"
        assert "WORK-456" in signals["work_items"]
        assert signals["status_update"] == "TESTING_COMPLETE"
        assert "Summary of work" in signals["summary"]
        assert "All tests pass." in signals["summary"]

    def test_parse_no_signals(self) -> None:
        """Output with no signals returns empty signal dict."""
        output = "Just a normal agent output with no special signals."
        signals = parse_agent_output(output)

        assert signals["handoff_condition"] is None
        assert signals["work_items"] == []
        assert signals["status_update"] is None
        assert "normal agent output" in signals["summary"]

    def test_parse_empty_output(self) -> None:
        """Empty output is handled gracefully."""
        signals = parse_agent_output("")

        assert signals["handoff_condition"] is None
        assert signals["work_items"] == []
        assert signals["status_update"] is None

    def test_summary_excludes_signal_lines(self) -> None:
        """Summary should not contain signal lines."""
        output = "Line 1\n##HANDOFF:test##\nLine 2\n##WORKITEM:W-1##\nLine 3"
        signals = parse_agent_output(output)

        assert "Line 1" in signals["summary"]
        assert "Line 2" in signals["summary"]
        assert "Line 3" in signals["summary"]
        assert "##HANDOFF" not in signals["summary"]
        assert "##WORKITEM" not in signals["summary"]


# =============================================================================
# Test: determine_handoff
# =============================================================================


class TestDetermineHandoff:
    """Tests for HANDOFF_RULES matching logic."""

    def test_orchestrator_implementation_complete(self) -> None:
        """Orchestrator with implementation_complete triggers handoff to qa-engineer."""
        signals = {"handoff_condition": "implementation_complete"}
        to_agent, context = determine_handoff("orchestrator", signals)

        assert to_agent == "qa-engineer"
        assert context is not None
        assert len(context) > 0

    def test_qa_security_concern(self) -> None:
        """QA with security_concern triggers handoff to security-auditor."""
        signals = {"handoff_condition": "security_concern"}
        to_agent, context = determine_handoff("qa-engineer", signals)

        assert to_agent == "security-auditor"

    def test_qa_tests_passing(self) -> None:
        """QA with tests_passing triggers handoff back to orchestrator."""
        signals = {"handoff_condition": "tests_passing"}
        to_agent, context = determine_handoff("qa-engineer", signals)

        assert to_agent == "orchestrator"

    def test_security_review_complete(self) -> None:
        """Security auditor with review_complete triggers handoff to orchestrator."""
        signals = {"handoff_condition": "review_complete"}
        to_agent, context = determine_handoff("security-auditor", signals)

        assert to_agent == "orchestrator"

    def test_no_condition_returns_none(self) -> None:
        """No handoff condition returns (None, None)."""
        signals = {"handoff_condition": None}
        to_agent, context = determine_handoff("orchestrator", signals)

        assert to_agent is None
        assert context is None

    def test_unknown_agent_returns_none_with_warning(self, capsys) -> None:
        """Unknown agent with a handoff condition returns None and logs warning."""
        signals = {"handoff_condition": "some_condition"}
        to_agent, context = determine_handoff("unknown-agent", signals)

        assert to_agent is None
        assert context is None
        # Warning should be on stderr
        captured = capsys.readouterr()
        assert "unknown-agent" in captured.err
        assert "not found in HANDOFF_RULES" in captured.err

    def test_known_agent_unknown_condition_warns(self, capsys) -> None:
        """Known agent with unknown condition returns None and logs warning."""
        signals = {"handoff_condition": "nonexistent_condition"}
        to_agent, context = determine_handoff("orchestrator", signals)

        assert to_agent is None
        assert context is None
        captured = capsys.readouterr()
        assert "nonexistent_condition" in captured.err
        assert "no matching rule" in captured.err

    def test_all_handoff_rules_keys_are_strings(self) -> None:
        """All HANDOFF_RULES keys should be strings (agent names)."""
        for key in HANDOFF_RULES:
            assert isinstance(key, str)

    def test_all_handoff_rules_values_are_tuples(self) -> None:
        """All HANDOFF_RULES values should be lists of 3-tuples."""
        for agent_name, rules in HANDOFF_RULES.items():
            assert isinstance(rules, list), f"Rules for {agent_name} should be a list"
            for rule in rules:
                assert len(rule) == 3, f"Rule for {agent_name} should be a 3-tuple"
                condition, to_agent, context = rule
                assert isinstance(condition, str)
                assert isinstance(to_agent, str)
                assert isinstance(context, str)


# =============================================================================
# Test: log_handoff
# =============================================================================


class TestLogHandoff:
    """Tests for handoff logging behavior."""

    def test_log_creates_file(self, tmp_path: Path, monkeypatch) -> None:
        """log_handoff should create a handoff log file."""
        import subagent_stop as sas

        # Point __file__ to a fake location under tmp_path so log_dir resolves there
        fake_script = tmp_path / "scripts" / "subagent_stop.py"
        fake_script.parent.mkdir(parents=True, exist_ok=True)
        monkeypatch.setattr(sas, "__file__", str(fake_script))

        signals = {
            "handoff_condition": "test_condition",
            "work_items": ["WORK-001"],
            "summary": "Test summary",
        }

        sas.log_handoff("from-agent", "to-agent", signals, "Test context")

        # log_dir resolves to: dirname(dirname(__file__))/../docs/experience
        # = tmp_path/../docs/experience
        log_dir = tmp_path.parent / "docs" / "experience"
        log_files = list(log_dir.glob("handoff_*.md"))
        assert len(log_files) == 1

        # Clean up outside tmp_path
        log_files[0].unlink()
        log_dir.rmdir()
        log_dir.parent.rmdir()

    def test_log_content_format(self, tmp_path: Path, monkeypatch) -> None:
        """Verify log_handoff writes expected content structure."""
        import subagent_stop as sas

        fake_script = tmp_path / "scripts" / "subagent_stop.py"
        fake_script.parent.mkdir(parents=True, exist_ok=True)
        monkeypatch.setattr(sas, "__file__", str(fake_script))

        signals = {
            "handoff_condition": "implementation_complete",
            "work_items": ["WORK-001", "WORK-002"],
            "summary": "Implementation completed successfully",
        }

        sas.log_handoff("test-agent", "qa-engineer", signals, "Test context")

        log_dir = tmp_path.parent / "docs" / "experience"
        log_files = list(log_dir.glob("handoff_*.md"))
        assert len(log_files) == 1

        content = log_files[0].read_text()
        assert "test-agent" in content
        assert "qa-engineer" in content
        assert "implementation_complete" in content
        assert "WORK-001" in content
        assert "Implementation completed successfully" in content

        # Clean up outside tmp_path
        log_files[0].unlink()
        log_dir.rmdir()
        log_dir.parent.rmdir()


# =============================================================================
# Test: Hook Output - Subprocess (Schema Compliance)
# =============================================================================


class TestHookOutputAllow:
    """Tests for allow (no handoff) output via subprocess."""

    def test_no_handoff_returns_empty_dict(self) -> None:
        """Agent with no handoff signals should produce empty dict output."""
        exit_code, output, stderr = run_hook(
            agent_name="some-agent",
            agent_output="Just finished my work, nothing special.",
        )

        assert exit_code == 0
        assert output == {}

    def test_unknown_agent_no_signals_returns_empty(self) -> None:
        """Unknown agent with no signals returns empty dict (allow)."""
        exit_code, output, stderr = run_hook(
            agent_name="brand-new-agent",
            agent_output="Work done.",
        )

        assert exit_code == 0
        assert output == {}

    def test_empty_output_returns_empty(self) -> None:
        """Agent with empty output returns empty dict (allow)."""
        exit_code, output, stderr = run_hook(
            agent_name="orchestrator",
            agent_output="",
        )

        assert exit_code == 0
        assert output == {}


class TestHookOutputBlock:
    """Tests for block (handoff triggered) output via subprocess."""

    def test_orchestrator_handoff_returns_block(self) -> None:
        """Orchestrator with implementation_complete signal returns block."""
        exit_code, output, stderr = run_hook(
            agent_name="orchestrator",
            agent_output="Done implementing.\n##HANDOFF:implementation_complete##\nAll good.",
        )

        assert exit_code == 0
        assert output is not None
        assert output.get("decision") == "block"
        assert "reason" in output
        assert "qa-engineer" in output["reason"]

    def test_qa_security_concern_returns_block(self) -> None:
        """QA engineer with security_concern returns block."""
        exit_code, output, stderr = run_hook(
            agent_name="qa-engineer",
            agent_output="Found issues.\n##HANDOFF:security_concern##\nNeeds review.",
        )

        assert exit_code == 0
        assert output is not None
        assert output.get("decision") == "block"
        assert "security-auditor" in output["reason"]

    def test_block_output_includes_system_message(self) -> None:
        """Block output should include systemMessage field."""
        exit_code, output, stderr = run_hook(
            agent_name="orchestrator",
            agent_output="##HANDOFF:implementation_complete##",
        )

        assert exit_code == 0
        assert output is not None
        assert "systemMessage" in output

    def test_block_output_has_no_hookspecificoutput(self) -> None:
        """SubagentStop MUST NOT use hookSpecificOutput."""
        exit_code, output, stderr = run_hook(
            agent_name="orchestrator",
            agent_output="##HANDOFF:implementation_complete##",
        )

        assert exit_code == 0
        assert output is not None
        assert "hookSpecificOutput" not in output


# =============================================================================
# Test: Error Handling
# =============================================================================


class TestErrorHandling:
    """Tests for hook error handling."""

    def test_invalid_json_returns_exit_2(self) -> None:
        """Invalid JSON input should return exit code 2."""
        result = subprocess.run(
            [sys.executable, str(HOOK_SCRIPT)],
            input="not valid json",
            capture_output=True,
            text=True,
            timeout=10,
        )

        assert result.returncode == 2
        assert result.stderr.strip()  # Error details on stderr

    def test_empty_input_returns_exit_2(self) -> None:
        """Empty stdin should return exit code 2."""
        result = subprocess.run(
            [sys.executable, str(HOOK_SCRIPT)],
            input="",
            capture_output=True,
            text=True,
            timeout=10,
        )

        assert result.returncode == 2

    def test_missing_agent_name_defaults_gracefully(self) -> None:
        """Missing agent_name field should not crash (defaults to 'unknown')."""
        result = subprocess.run(
            [sys.executable, str(HOOK_SCRIPT)],
            input=json.dumps({"output": "test"}),
            capture_output=True,
            text=True,
            timeout=10,
        )

        assert result.returncode == 0

    def test_missing_output_field_defaults_gracefully(self) -> None:
        """Missing output field should not crash (defaults to empty string)."""
        result = subprocess.run(
            [sys.executable, str(HOOK_SCRIPT)],
            input=json.dumps({"agent_name": "test"}),
            capture_output=True,
            text=True,
            timeout=10,
        )

        assert result.returncode == 0


# =============================================================================
# Test: HANDOFF_RULES Mismatch Warnings (PM-001, FM-001)
# =============================================================================


class TestHandoffRulesWarnings:
    """Tests for HANDOFF_RULES mismatch warning system."""

    def test_unknown_agent_with_signal_warns_on_stderr(self) -> None:
        """Unknown agent with handoff signal should produce stderr warning."""
        exit_code, output, stderr = run_hook(
            agent_name="renamed-agent-v2",
            agent_output="##HANDOFF:implementation_complete##",
        )

        assert exit_code == 0
        assert output == {}  # Allow (no matching rule)
        assert "renamed-agent-v2" in stderr
        assert "not found in HANDOFF_RULES" in stderr

    def test_known_agent_unknown_condition_warns(self) -> None:
        """Known agent with unrecognized condition should warn."""
        exit_code, output, stderr = run_hook(
            agent_name="orchestrator",
            agent_output="##HANDOFF:brand_new_condition##",
        )

        assert exit_code == 0
        assert output == {}  # Allow (no matching rule)
        assert "brand_new_condition" in stderr
        assert "no matching rule" in stderr
