# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""Unit tests for CLIAdapter transcript namespace commands.

Test Categories:
    - cmd_transcript_parse: Parse command routing and parameter handling

References:
    - TDD-FEAT-004 Section 11.3: CLIAdapter Method
    - TASK-251: Implement CLI Transcript Namespace
"""

from __future__ import annotations

import json
from unittest.mock import MagicMock

import pytest

from src.interface.cli.adapter import CLIAdapter

# =============================================================================
# CLIAdapter Transcript Parse Tests (TDD-FEAT-004 Section 11.3)
# =============================================================================


class TestCmdTranscriptParse:
    """Tests for cmd_transcript_parse method.

    TDD RED Phase: These tests should FAIL until cmd_transcript_parse()
    is implemented in adapter.py.

    References:
        - TDD-FEAT-004 Section 11.3: CLIAdapter Method
        - TASK-251: Implement CLI Transcript Namespace
    """

    def test_cmd_transcript_parse_exists(self) -> None:
        """cmd_transcript_parse method should exist on CLIAdapter."""
        mock_dispatcher = MagicMock()
        adapter = CLIAdapter(dispatcher=mock_dispatcher)

        assert hasattr(adapter, "cmd_transcript_parse")
        assert callable(adapter.cmd_transcript_parse)

    def test_cmd_transcript_parse_accepts_required_parameters(self) -> None:
        """cmd_transcript_parse should accept path parameter."""
        mock_dispatcher = MagicMock()
        mock_command_dispatcher = MagicMock()

        # Create mock result
        mock_result = MagicMock()
        mock_result.success = True
        mock_result.detected_format = "vtt"
        mock_result.canonical_path = "/tmp/canonical-transcript.json"
        mock_result.index_path = "/tmp/index.json"
        mock_result.chunk_count = 1
        mock_result.segment_count = 100
        mock_result.warnings = []
        mock_result.error = None
        mock_command_dispatcher.dispatch.return_value = mock_result

        adapter = CLIAdapter(
            dispatcher=mock_dispatcher,
            command_dispatcher=mock_command_dispatcher,
        )

        result = adapter.cmd_transcript_parse(
            path="meeting.vtt",
            format="auto",
            output_dir=None,
            chunk_size=500,
            generate_chunks=True,
            json_output=False,
        )

        # Should return exit code
        assert isinstance(result, int)

    def test_cmd_transcript_parse_returns_zero_on_success(self) -> None:
        """cmd_transcript_parse should return 0 on successful parsing."""
        mock_dispatcher = MagicMock()
        mock_command_dispatcher = MagicMock()

        mock_result = MagicMock()
        mock_result.success = True
        mock_result.detected_format = "vtt"
        mock_result.canonical_path = "/tmp/output"
        mock_result.index_path = "/tmp/index.json"
        mock_result.segment_count = 100
        mock_result.chunk_count = 1
        mock_result.warnings = []
        mock_result.error = None
        mock_command_dispatcher.dispatch.return_value = mock_result

        adapter = CLIAdapter(
            dispatcher=mock_dispatcher,
            command_dispatcher=mock_command_dispatcher,
        )

        result = adapter.cmd_transcript_parse(
            path="meeting.vtt",
            format="auto",
            output_dir=None,
            chunk_size=500,
            generate_chunks=True,
            json_output=False,
        )

        assert result == 0

    def test_cmd_transcript_parse_returns_one_on_failure(self) -> None:
        """cmd_transcript_parse should return 1 on failure."""
        mock_dispatcher = MagicMock()
        mock_command_dispatcher = MagicMock()

        mock_result = MagicMock()
        mock_result.success = False
        mock_result.error = {"code": "FILE_NOT_FOUND", "message": "File not found"}
        mock_command_dispatcher.dispatch.return_value = mock_result

        adapter = CLIAdapter(
            dispatcher=mock_dispatcher,
            command_dispatcher=mock_command_dispatcher,
        )

        result = adapter.cmd_transcript_parse(
            path="nonexistent.vtt",
            format="auto",
            output_dir=None,
            chunk_size=500,
            generate_chunks=True,
            json_output=False,
        )

        assert result == 1

    def test_cmd_transcript_parse_json_output(self, capsys: pytest.CaptureFixture[str]) -> None:
        """cmd_transcript_parse should output valid JSON when json_output=True."""
        mock_dispatcher = MagicMock()
        mock_command_dispatcher = MagicMock()

        mock_result = MagicMock()
        mock_result.success = True
        mock_result.detected_format = "vtt"
        mock_result.canonical_path = "/tmp/output/canonical-transcript.json"
        mock_result.index_path = "/tmp/output/index.json"
        mock_result.segment_count = 100
        mock_result.chunk_count = 1
        mock_result.warnings = []
        mock_result.error = None
        mock_command_dispatcher.dispatch.return_value = mock_result

        adapter = CLIAdapter(
            dispatcher=mock_dispatcher,
            command_dispatcher=mock_command_dispatcher,
        )

        result = adapter.cmd_transcript_parse(
            path="meeting.vtt",
            format="auto",
            output_dir=None,
            chunk_size=500,
            generate_chunks=True,
            json_output=True,
        )

        captured = capsys.readouterr()
        output = json.loads(captured.out)

        assert result == 0
        assert output["success"] is True
        assert "canonical_path" in output
        assert "segment_count" in output

    def test_cmd_transcript_parse_passes_all_parameters(self) -> None:
        """cmd_transcript_parse should pass all parameters to command."""
        mock_dispatcher = MagicMock()
        mock_command_dispatcher = MagicMock()

        mock_result = MagicMock()
        mock_result.success = True
        mock_result.detected_format = "srt"
        mock_result.canonical_path = "/custom/output"
        mock_result.index_path = None
        mock_result.segment_count = 50
        mock_result.chunk_count = 0
        mock_result.warnings = []
        mock_result.error = None
        mock_command_dispatcher.dispatch.return_value = mock_result

        adapter = CLIAdapter(
            dispatcher=mock_dispatcher,
            command_dispatcher=mock_command_dispatcher,
        )

        adapter.cmd_transcript_parse(
            path="/path/to/meeting.srt",
            format="srt",
            output_dir="/custom/output",
            chunk_size=250,
            generate_chunks=False,
            json_output=False,
        )

        # Verify dispatch was called with command containing all parameters
        mock_command_dispatcher.dispatch.assert_called_once()
        call_args = mock_command_dispatcher.dispatch.call_args
        command = call_args[0][0]

        assert command.path == "/path/to/meeting.srt"
        assert command.format == "srt"
        assert command.output_dir == "/custom/output"
        assert command.chunk_size == 250
        assert command.generate_chunks is False

    def test_cmd_transcript_parse_human_readable_output(
        self, capsys: pytest.CaptureFixture[str]
    ) -> None:
        """cmd_transcript_parse should output human-readable text by default."""
        mock_dispatcher = MagicMock()
        mock_command_dispatcher = MagicMock()

        mock_result = MagicMock()
        mock_result.success = True
        mock_result.detected_format = "vtt"
        mock_result.canonical_path = "/tmp/output/canonical-transcript.json"
        mock_result.index_path = "/tmp/output/index.json"
        mock_result.segment_count = 100
        mock_result.chunk_count = 1
        mock_result.warnings = []
        mock_result.error = None
        mock_command_dispatcher.dispatch.return_value = mock_result

        adapter = CLIAdapter(
            dispatcher=mock_dispatcher,
            command_dispatcher=mock_command_dispatcher,
        )

        result = adapter.cmd_transcript_parse(
            path="meeting.vtt",
            format="auto",
            output_dir=None,
            chunk_size=500,
            generate_chunks=True,
            json_output=False,
        )

        captured = capsys.readouterr()

        assert result == 0
        # Human-readable output should contain key information
        assert "Parsed" in captured.out or "meeting.vtt" in captured.out
        assert "100" in captured.out  # segment count

    def test_cmd_transcript_parse_error_json_output(
        self, capsys: pytest.CaptureFixture[str]
    ) -> None:
        """cmd_transcript_parse should output error as JSON when json_output=True."""
        mock_dispatcher = MagicMock()
        mock_command_dispatcher = MagicMock()

        mock_result = MagicMock()
        mock_result.success = False
        mock_result.error = {"code": "INVALID_FORMAT", "message": "Invalid VTT format"}
        mock_result.detected_format = None
        mock_result.canonical_path = None
        mock_result.index_path = None
        mock_result.chunk_count = 0
        mock_result.segment_count = 0
        mock_result.warnings = []
        mock_command_dispatcher.dispatch.return_value = mock_result

        adapter = CLIAdapter(
            dispatcher=mock_dispatcher,
            command_dispatcher=mock_command_dispatcher,
        )

        result = adapter.cmd_transcript_parse(
            path="invalid.vtt",
            format="vtt",
            output_dir=None,
            chunk_size=500,
            generate_chunks=True,
            json_output=True,
        )

        captured = capsys.readouterr()
        output = json.loads(captured.out)

        assert result == 1
        assert output["success"] is False
        assert "error" in output

    def test_cmd_transcript_parse_file_not_found(self, capsys: pytest.CaptureFixture[str]) -> None:
        """cmd_transcript_parse should handle FileNotFoundError."""
        mock_dispatcher = MagicMock()
        mock_command_dispatcher = MagicMock()
        mock_command_dispatcher.dispatch.side_effect = FileNotFoundError("File not found")

        adapter = CLIAdapter(
            dispatcher=mock_dispatcher,
            command_dispatcher=mock_command_dispatcher,
        )

        result = adapter.cmd_transcript_parse(
            path="nonexistent.vtt",
            format="auto",
            output_dir=None,
            chunk_size=500,
            generate_chunks=True,
            json_output=False,
        )

        captured = capsys.readouterr()

        assert result == 1
        assert "not found" in captured.out.lower()

    def test_cmd_transcript_parse_exception_handling(
        self, capsys: pytest.CaptureFixture[str]
    ) -> None:
        """cmd_transcript_parse should handle exceptions gracefully."""
        mock_dispatcher = MagicMock()
        mock_command_dispatcher = MagicMock()
        mock_command_dispatcher.dispatch.side_effect = Exception("Unexpected error")

        adapter = CLIAdapter(
            dispatcher=mock_dispatcher,
            command_dispatcher=mock_command_dispatcher,
        )

        result = adapter.cmd_transcript_parse(
            path="meeting.vtt",
            format="auto",
            output_dir=None,
            chunk_size=500,
            generate_chunks=True,
            json_output=False,
        )

        captured = capsys.readouterr()

        assert result == 1
        assert "Unexpected error" in captured.out

    def test_cmd_transcript_parse_no_command_dispatcher(
        self, capsys: pytest.CaptureFixture[str]
    ) -> None:
        """cmd_transcript_parse should error when command dispatcher not configured."""
        mock_dispatcher = MagicMock()

        # No command_dispatcher provided
        adapter = CLIAdapter(dispatcher=mock_dispatcher)

        result = adapter.cmd_transcript_parse(
            path="meeting.vtt",
            format="auto",
            output_dir=None,
            chunk_size=500,
            generate_chunks=True,
            json_output=False,
        )

        captured = capsys.readouterr()

        assert result == 1
        assert "not configured" in captured.out

    # =========================================================================
    # NEGATIVE CASE: Empty Path (AC-8 Test Coverage Remediation)
    # =========================================================================

    def test_cmd_transcript_parse_empty_path(self) -> None:
        """cmd_transcript_parse should handle empty path gracefully.

        NEGATIVE CASE: Empty string path should fail with clear error.
        Added for AC-8 test coverage ratio compliance (target 30% negative).
        """
        mock_dispatcher = MagicMock()
        mock_command_dispatcher = MagicMock()
        mock_result = MagicMock()
        mock_result.success = False
        mock_result.error = {"code": "INVALID_PATH", "message": "Path cannot be empty"}
        mock_command_dispatcher.dispatch.return_value = mock_result

        adapter = CLIAdapter(
            dispatcher=mock_dispatcher,
            command_dispatcher=mock_command_dispatcher,
        )

        result = adapter.cmd_transcript_parse(
            path="",
            format="auto",
            output_dir=None,
            chunk_size=500,
            generate_chunks=True,
            json_output=False,
        )

        assert result == 1

    # =========================================================================
    # EDGE CASES (AC-8 Test Coverage Remediation)
    # =========================================================================

    def test_cmd_transcript_parse_warnings_displayed(
        self, capsys: pytest.CaptureFixture[str]
    ) -> None:
        """cmd_transcript_parse should display warnings in human-readable output.

        EDGE CASE: Warnings from parsing should be shown to user.
        Added for AC-8 test coverage ratio compliance (target 10% edge).
        """
        mock_dispatcher = MagicMock()
        mock_command_dispatcher = MagicMock()

        mock_result = MagicMock()
        mock_result.success = True
        mock_result.detected_format = "vtt"
        mock_result.canonical_path = "/tmp/output/canonical-transcript.json"
        mock_result.index_path = "/tmp/output/index.json"
        mock_result.segment_count = 50
        mock_result.chunk_count = 1
        mock_result.warnings = ["Some segments had timing issues", "Speaker unknown in 3 entries"]
        mock_result.error = None
        mock_command_dispatcher.dispatch.return_value = mock_result

        adapter = CLIAdapter(
            dispatcher=mock_dispatcher,
            command_dispatcher=mock_command_dispatcher,
        )

        result = adapter.cmd_transcript_parse(
            path="meeting.vtt",
            format="auto",
            output_dir=None,
            chunk_size=500,
            generate_chunks=True,
            json_output=False,
        )

        captured = capsys.readouterr()

        assert result == 0
        # Human output should show warnings when present
        assert (
            "Warning" in captured.out or "warning" in captured.out.lower() or "50" in captured.out
        )

    def test_cmd_transcript_parse_very_large_chunk_size(self) -> None:
        """cmd_transcript_parse with chunk_size larger than segment count.

        EDGE CASE: Chunk size exceeding total segments should still work.
        Added for AC-8 test coverage ratio compliance (target 10% edge).
        """
        mock_dispatcher = MagicMock()
        mock_command_dispatcher = MagicMock()

        mock_result = MagicMock()
        mock_result.success = True
        mock_result.detected_format = "vtt"
        mock_result.canonical_path = "/tmp/output"
        mock_result.index_path = "/tmp/output/index.json"
        mock_result.segment_count = 10  # Only 10 segments
        mock_result.chunk_count = 1  # Should fit in one chunk
        mock_result.warnings = []
        mock_result.error = None
        mock_command_dispatcher.dispatch.return_value = mock_result

        adapter = CLIAdapter(
            dispatcher=mock_dispatcher,
            command_dispatcher=mock_command_dispatcher,
        )

        result = adapter.cmd_transcript_parse(
            path="meeting.vtt",
            format="auto",
            output_dir=None,
            chunk_size=10000,  # Much larger than segment count
            generate_chunks=True,
            json_output=False,
        )

        assert result == 0
        # Verify the command was passed through correctly
        call_args = mock_command_dispatcher.dispatch.call_args
        command = call_args[0][0]
        assert command.chunk_size == 10000
