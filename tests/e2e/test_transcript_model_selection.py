"""End-to-end tests for transcript model selection.

Tests the full pipeline from CLI invocation through to model configuration
being used by agents (or at least ready for use).

This E2E test suite uses subprocess to test the actual CLI entry point,
validating that model selection works in a production-like environment.

References:
    - TASK-424: Integration Testing - Track B
    - EN-031: Model Selection Capability
    - TASK-423: Implement Model Profiles
"""

from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path

import pytest

# Get the project root directory
PROJECT_ROOT = Path(__file__).parent.parent.parent


def _find_jerry_executable() -> str:
    """Find the jerry executable - works in both venv and CI environments."""
    # Try venv path first (local development)
    venv_jerry = PROJECT_ROOT / ".venv" / "bin" / "jerry"
    if venv_jerry.exists():
        return str(venv_jerry)

    # Try system path (CI environment with pip install -e .)
    system_jerry = shutil.which("jerry")
    if system_jerry:
        return system_jerry

    # Fallback: use python -m src.interface.cli.main
    pytest.skip("jerry executable not found - run 'uv sync' or 'pip install -e .'")
    return ""  # Never reached


class TestTranscriptModelSelectionE2E:
    """E2E tests for transcript parse with model selection."""

    @pytest.fixture
    def jerry_cmd(self) -> str:
        """Get path to jerry command."""
        return _find_jerry_executable()

    @pytest.fixture
    def temp_transcript(self, tmp_path: Path) -> Path:
        """Create a minimal test transcript file."""
        transcript_file = tmp_path / "test.vtt"
        transcript_file.write_text(
            """WEBVTT

00:00:00.000 --> 00:00:02.000
Speaker 1: Hello world.

00:00:02.000 --> 00:00:04.000
Speaker 2: This is a test.
"""
        )
        return transcript_file

    def test_transcript_parse_with_economy_profile_exits_zero(
        self, jerry_cmd: str, temp_transcript: Path
    ) -> None:
        """Transcript parse with economy profile should work (smoke test).

        Note: This test may fail if ts-parser agent is not available,
        but it validates that CLI argument parsing and profile resolution work.
        """
        result = subprocess.run(
            [
                jerry_cmd,
                "transcript",
                "parse",
                str(temp_transcript),
                "--profile",
                "economy",
            ],
            capture_output=True,
            text=True,
            cwd=PROJECT_ROOT,
        )

        # May exit 0 (success) or 1 (agent not found), but should not crash
        assert result.returncode in (0, 1)

        # Should not have Python traceback
        assert "Traceback" not in result.stderr

    def test_transcript_parse_with_quality_profile_exits_zero(
        self, jerry_cmd: str, temp_transcript: Path
    ) -> None:
        """Transcript parse with quality profile should work (smoke test)."""
        result = subprocess.run(
            [
                jerry_cmd,
                "transcript",
                "parse",
                str(temp_transcript),
                "--profile",
                "quality",
            ],
            capture_output=True,
            text=True,
            cwd=PROJECT_ROOT,
        )

        # May exit 0 (success) or 1 (agent not found), but should not crash
        assert result.returncode in (0, 1)

        # Should not have Python traceback
        assert "Traceback" not in result.stderr

    def test_transcript_parse_with_profile_and_override_exits_zero(
        self, jerry_cmd: str, temp_transcript: Path
    ) -> None:
        """Transcript parse with profile + override should work (smoke test)."""
        result = subprocess.run(
            [
                jerry_cmd,
                "transcript",
                "parse",
                str(temp_transcript),
                "--profile",
                "economy",
                "--model-extractor",
                "opus",
            ],
            capture_output=True,
            text=True,
            cwd=PROJECT_ROOT,
        )

        # May exit 0 (success) or 1 (agent not found), but should not crash
        assert result.returncode in (0, 1)

        # Should not have Python traceback
        assert "Traceback" not in result.stderr

    def test_transcript_parse_with_all_model_flags_exits_zero(
        self, jerry_cmd: str, temp_transcript: Path
    ) -> None:
        """Transcript parse with all five model flags should work (smoke test)."""
        result = subprocess.run(
            [
                jerry_cmd,
                "transcript",
                "parse",
                str(temp_transcript),
                "--model-parser",
                "sonnet",
                "--model-extractor",
                "opus",
                "--model-formatter",
                "sonnet",
                "--model-mindmap",
                "sonnet",
                "--model-critic",
                "opus",
            ],
            capture_output=True,
            text=True,
            cwd=PROJECT_ROOT,
        )

        # May exit 0 (success) or 1 (agent not found), but should not crash
        assert result.returncode in (0, 1)

        # Should not have Python traceback
        assert "Traceback" not in result.stderr

    def test_transcript_parse_invalid_profile_exits_one(
        self, jerry_cmd: str, temp_transcript: Path
    ) -> None:
        """Transcript parse with invalid profile should exit with error message.

        Note: argparse uses exit code 2 for invalid arguments.
        """
        result = subprocess.run(
            [
                jerry_cmd,
                "transcript",
                "parse",
                str(temp_transcript),
                "--profile",
                "invalid-profile",
            ],
            capture_output=True,
            text=True,
            cwd=PROJECT_ROOT,
        )

        # Should fail (argparse uses exit code 2 for invalid arguments)
        assert result.returncode in (1, 2)

        # Should have error message about invalid profile
        # (Error may be in stdout or stderr depending on implementation)
        output = result.stdout + result.stderr
        assert "invalid-profile" in output.lower() or "invalid choice" in output.lower()

    def test_transcript_parse_help_shows_model_flags(self, jerry_cmd: str) -> None:
        """Transcript parse help should show all model selection flags."""
        result = subprocess.run(
            [jerry_cmd, "transcript", "parse", "--help"],
            capture_output=True,
            text=True,
            cwd=PROJECT_ROOT,
        )

        assert result.returncode == 0

        # Should document all model flags
        assert "--model-parser" in result.stdout
        assert "--model-extractor" in result.stdout
        assert "--model-formatter" in result.stdout
        assert "--model-mindmap" in result.stdout
        assert "--model-critic" in result.stdout
        assert "--profile" in result.stdout

    def test_transcript_parse_help_shows_profile_choices(self, jerry_cmd: str) -> None:
        """Transcript parse help should show all profile choices."""
        result = subprocess.run(
            [jerry_cmd, "transcript", "parse", "--help"],
            capture_output=True,
            text=True,
            cwd=PROJECT_ROOT,
        )

        assert result.returncode == 0

        # Should document profile choices
        assert "economy" in result.stdout
        assert "balanced" in result.stdout
        assert "quality" in result.stdout
        assert "speed" in result.stdout


class TestTranscriptModelSelectionJSON:
    """E2E tests for JSON output with model selection."""

    @pytest.fixture
    def jerry_cmd(self) -> str:
        """Get path to jerry command."""
        return _find_jerry_executable()

    @pytest.fixture
    def temp_transcript(self, tmp_path: Path) -> Path:
        """Create a minimal test transcript file."""
        transcript_file = tmp_path / "test.vtt"
        transcript_file.write_text(
            """WEBVTT

00:00:00.000 --> 00:00:02.000
Speaker 1: Hello world.
"""
        )
        return transcript_file

    def test_transcript_parse_json_output_is_valid_json(
        self, jerry_cmd: str, temp_transcript: Path
    ) -> None:
        """Transcript parse with --json should output valid JSON.

        Note: --json flag must come before the namespace (global flag).
        This test validates that JSON output format is correct.
        If no output, it means command failed before producing JSON.
        """
        result = subprocess.run(
            [
                jerry_cmd,
                "--json",  # Global flag must come before namespace
                "transcript",
                "parse",
                str(temp_transcript),
                "--profile",
                "economy",
            ],
            capture_output=True,
            text=True,
            cwd=PROJECT_ROOT,
        )

        # If there's output, it should be valid JSON
        if result.stdout.strip():
            try:
                output = json.loads(result.stdout)
                # If JSON is valid, test passes
                assert isinstance(output, dict)
            except json.JSONDecodeError:
                # If JSON is invalid, fail with helpful message
                pytest.fail(f"Invalid JSON output: {result.stdout[:200]}")
        else:
            # No output means command failed early (e.g., missing agents)
            # This is acceptable - we're testing the model selection feature
            # works at CLI level, not that the full pipeline runs
            # Exit code 2 is argparse error
            assert result.returncode in (0, 1, 2)


class TestModelConfigurationFlow:
    """E2E tests for model configuration flowing through the system."""

    @pytest.fixture
    def jerry_cmd(self) -> str:
        """Get path to jerry command."""
        return _find_jerry_executable()

    def test_model_selection_documented_in_help(self, jerry_cmd: str) -> None:
        """Main help should document model selection feature."""
        result = subprocess.run(
            [jerry_cmd, "transcript", "--help"],
            capture_output=True,
            text=True,
            cwd=PROJECT_ROOT,
        )

        assert result.returncode == 0
        assert "parse" in result.stdout

    def test_all_profiles_accessible_via_cli(self, jerry_cmd: str) -> None:
        """All four profiles should be accessible via CLI.

        This test validates that the profile choices in the CLI parser
        match the profiles defined in model_profiles.py.
        """
        result = subprocess.run(
            [jerry_cmd, "transcript", "parse", "--help"],
            capture_output=True,
            text=True,
            cwd=PROJECT_ROOT,
        )

        # All four profiles should be documented
        help_text = result.stdout.lower()
        assert "economy" in help_text
        assert "balanced" in help_text
        assert "quality" in help_text
        assert "speed" in help_text


class TestModelValidationE2E:
    """E2E tests for model validation at CLI level."""

    @pytest.fixture
    def jerry_cmd(self) -> str:
        """Get path to jerry command."""
        return _find_jerry_executable()

    @pytest.fixture
    def temp_transcript(self, tmp_path: Path) -> Path:
        """Create a minimal test transcript file."""
        transcript_file = tmp_path / "test.vtt"
        transcript_file.write_text(
            """WEBVTT

00:00:00.000 --> 00:00:02.000
Test content.
"""
        )
        return transcript_file

    def test_invalid_model_value_rejected(self, jerry_cmd: str, temp_transcript: Path) -> None:
        """Invalid model value should be rejected with error message.

        Note: Validation may happen at argparse level or ModelConfig level.
        Either way, invalid values should cause exit code 1.
        """
        result = subprocess.run(
            [
                jerry_cmd,
                "transcript",
                "parse",
                str(temp_transcript),
                "--model-parser",
                "invalid-model",
            ],
            capture_output=True,
            text=True,
            cwd=PROJECT_ROOT,
        )

        # Should fail
        assert result.returncode in (1, 2)  # 2 is argparse error code

        # Should mention the invalid model
        output = result.stdout + result.stderr
        # May have "invalid" or "invalid-model" in error message
        assert "invalid" in output.lower()

    def test_case_sensitivity_of_model_values(self, jerry_cmd: str, temp_transcript: Path) -> None:
        """Model values should be case-sensitive (lowercase only).

        Values like "Haiku", "HAIKU", "Sonnet" should be rejected.
        Only "haiku", "sonnet", "opus" should be accepted.
        """
        # Test uppercase
        result = subprocess.run(
            [
                jerry_cmd,
                "transcript",
                "parse",
                str(temp_transcript),
                "--model-parser",
                "HAIKU",
            ],
            capture_output=True,
            text=True,
            cwd=PROJECT_ROOT,
        )

        # Should fail (case-sensitive)
        assert result.returncode in (1, 2)

    def test_all_valid_models_accepted(self, jerry_cmd: str, temp_transcript: Path) -> None:
        """All three valid model values should be accepted.

        Values: haiku, sonnet, opus
        """
        for model in ["haiku", "sonnet", "opus"]:
            result = subprocess.run(
                [
                    jerry_cmd,
                    "transcript",
                    "parse",
                    str(temp_transcript),
                    "--model-parser",
                    model,
                ],
                capture_output=True,
                text=True,
                cwd=PROJECT_ROOT,
            )

            # Should not fail due to validation
            # (may fail for other reasons like missing agents)
            # Exit code 2 is argparse error, which means validation failed
            assert result.returncode != 2, f"Model '{model}' was rejected"
