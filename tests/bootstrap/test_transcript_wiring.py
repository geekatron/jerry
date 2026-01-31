"""Unit tests for transcript command wiring in bootstrap.py.

Test Categories:
    - Section 11.4: Bootstrap wiring for ParseTranscriptCommand

References:
    - TDD-FEAT-004 Section 11.4: Bootstrap Wiring
    - TASK-251: Implement CLI Transcript Namespace
"""

from __future__ import annotations

import pytest

from src.application.dispatchers.command_dispatcher import CommandDispatcher
from src.bootstrap import create_command_dispatcher
from src.transcript.application.commands import ParseTranscriptCommand

# =============================================================================
# Section 11.4: Bootstrap Transcript Wiring Tests
# =============================================================================


class TestTranscriptBootstrapWiring:
    """Tests for transcript command wiring in bootstrap.py.

    TDD RED Phase: These tests should FAIL until bootstrap wiring
    is implemented for transcript commands.

    References:
        - TDD-FEAT-004 Section 11.4: Bootstrap Wiring
        - TASK-251: Implement CLI Transcript Namespace
    """

    def test_create_command_dispatcher_returns_dispatcher(self) -> None:
        """create_command_dispatcher should return a CommandDispatcher."""
        dispatcher = create_command_dispatcher()

        assert isinstance(dispatcher, CommandDispatcher)

    def test_dispatcher_handles_parse_transcript_command(self) -> None:
        """Dispatcher should have handler registered for ParseTranscriptCommand."""
        dispatcher = create_command_dispatcher()

        # Check that the command type is registered
        assert dispatcher.has_handler(ParseTranscriptCommand)

    def test_parse_transcript_command_dispatch_invokes_handler(
        self, tmp_path: pytest.TempPathFactory
    ) -> None:
        """Dispatch of ParseTranscriptCommand should invoke handler and return result."""
        dispatcher = create_command_dispatcher()

        # Create a minimal VTT file
        vtt_file = tmp_path / "test.vtt"
        vtt_file.write_text("WEBVTT\n\n00:00:00.000 --> 00:00:05.000\nHello world\n")
        output_dir = tmp_path / "output"
        output_dir.mkdir()

        command = ParseTranscriptCommand(
            path=str(vtt_file),
            format="vtt",
            output_dir=str(output_dir),
            chunk_size=500,
            generate_chunks=True,
        )

        result = dispatcher.dispatch(command)

        # Result should have expected attributes from ParseTranscriptResult
        assert result is not None
        assert hasattr(result, "success")
        assert hasattr(result, "segment_count")

    def test_parse_transcript_returns_success_on_valid_vtt(
        self, tmp_path: pytest.TempPathFactory
    ) -> None:
        """Parsing a valid VTT file should return success=True."""
        dispatcher = create_command_dispatcher()

        vtt_file = tmp_path / "meeting.vtt"
        vtt_file.write_text(
            "WEBVTT\n\n"
            "00:00:00.000 --> 00:00:05.000\n"
            "<v Alice>Hello everyone\n\n"
            "00:00:05.000 --> 00:00:10.000\n"
            "<v Bob>Hi Alice\n"
        )
        output_dir = tmp_path / "output"
        output_dir.mkdir()

        command = ParseTranscriptCommand(
            path=str(vtt_file),
            format="vtt",
            output_dir=str(output_dir),
            chunk_size=500,
            generate_chunks=True,
        )

        result = dispatcher.dispatch(command)

        assert result.success is True
        assert result.segment_count == 2
        assert result.detected_format == "vtt"

    def test_parse_transcript_returns_failure_on_invalid_file(
        self, tmp_path: pytest.TempPathFactory
    ) -> None:
        """Parsing a non-existent file should return success=False."""
        dispatcher = create_command_dispatcher()

        command = ParseTranscriptCommand(
            path=str(tmp_path / "nonexistent.vtt"),
            format="vtt",
            output_dir=str(tmp_path),
            chunk_size=500,
            generate_chunks=True,
        )

        result = dispatcher.dispatch(command)

        assert result.success is False
        assert result.error is not None

    def test_parse_transcript_generates_index_when_chunking_enabled(
        self, tmp_path: pytest.TempPathFactory
    ) -> None:
        """When generate_chunks=True, should create index.json."""
        dispatcher = create_command_dispatcher()

        vtt_file = tmp_path / "meeting.vtt"
        vtt_file.write_text("WEBVTT\n\n00:00:00.000 --> 00:00:05.000\nHello\n")
        output_dir = tmp_path / "output"
        output_dir.mkdir()

        command = ParseTranscriptCommand(
            path=str(vtt_file),
            format="vtt",
            output_dir=str(output_dir),
            chunk_size=500,
            generate_chunks=True,
        )

        result = dispatcher.dispatch(command)

        assert result.success is True
        assert result.index_path is not None
        # Verify file was actually created
        from pathlib import Path

        assert Path(result.index_path).exists()

    def test_parse_transcript_skips_chunking_when_disabled(
        self, tmp_path: pytest.TempPathFactory
    ) -> None:
        """When generate_chunks=False, should not create chunk files."""
        dispatcher = create_command_dispatcher()

        vtt_file = tmp_path / "meeting.vtt"
        vtt_file.write_text("WEBVTT\n\n00:00:00.000 --> 00:00:05.000\nHello\n")
        output_dir = tmp_path / "output"
        output_dir.mkdir()

        command = ParseTranscriptCommand(
            path=str(vtt_file),
            format="vtt",
            output_dir=str(output_dir),
            chunk_size=500,
            generate_chunks=False,
        )

        result = dispatcher.dispatch(command)

        assert result.success is True
        assert result.chunk_count == 0
        assert result.index_path is None

    # =========================================================================
    # NEGATIVE CASE (AC-8 Test Coverage Remediation)
    # =========================================================================

    def test_parse_transcript_returns_failure_on_unsupported_format(
        self, tmp_path: pytest.TempPathFactory
    ) -> None:
        """Parsing with unsupported format should return failure.

        NEGATIVE CASE: SRT and TXT formats not yet implemented.
        Added for AC-8 test coverage ratio compliance (target 30% negative).
        """
        dispatcher = create_command_dispatcher()

        # Create an SRT file
        srt_file = tmp_path / "meeting.srt"
        srt_file.write_text("1\n00:00:00,000 --> 00:00:05,000\nHello world\n")
        output_dir = tmp_path / "output"
        output_dir.mkdir()

        command = ParseTranscriptCommand(
            path=str(srt_file),
            format="srt",  # SRT format - not yet implemented
            output_dir=str(output_dir),
            chunk_size=500,
            generate_chunks=True,
        )

        result = dispatcher.dispatch(command)

        assert result.success is False
        assert result.error is not None
        assert "UNSUPPORTED_FORMAT" in result.error.get("code", "")

    # =========================================================================
    # EDGE CASES (AC-8 Test Coverage Remediation)
    # =========================================================================

    def test_parse_transcript_empty_vtt_file(self, tmp_path: pytest.TempPathFactory) -> None:
        """Parsing a VTT file with only header (no segments) should succeed.

        EDGE CASE: Empty file with valid header should not error.
        Added for AC-8 test coverage ratio compliance (target 10% edge).
        """
        dispatcher = create_command_dispatcher()

        # VTT file with only header, no segments
        vtt_file = tmp_path / "empty.vtt"
        vtt_file.write_text("WEBVTT\n\n")
        output_dir = tmp_path / "output"
        output_dir.mkdir()

        command = ParseTranscriptCommand(
            path=str(vtt_file),
            format="vtt",
            output_dir=str(output_dir),
            chunk_size=500,
            generate_chunks=True,
        )

        result = dispatcher.dispatch(command)

        assert result.success is True
        assert result.segment_count == 0

    def test_parse_transcript_path_with_spaces(self, tmp_path: pytest.TempPathFactory) -> None:
        """Parsing a file at path with spaces should work correctly.

        EDGE CASE: Filesystem paths with spaces must be handled.
        Added for AC-8 test coverage ratio compliance (target 10% edge).
        """
        dispatcher = create_command_dispatcher()

        # Create directory and file with spaces
        spaced_dir = tmp_path / "my meeting files"
        spaced_dir.mkdir()
        vtt_file = spaced_dir / "team meeting 2026.vtt"
        vtt_file.write_text("WEBVTT\n\n00:00:00.000 --> 00:00:05.000\nHello everyone\n")
        output_dir = tmp_path / "output dir"
        output_dir.mkdir()

        command = ParseTranscriptCommand(
            path=str(vtt_file),
            format="vtt",
            output_dir=str(output_dir),
            chunk_size=500,
            generate_chunks=True,
        )

        result = dispatcher.dispatch(command)

        assert result.success is True
        assert result.segment_count == 1
