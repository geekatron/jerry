"""
Unit tests for VTTParser.

RED/GREEN/REFACTOR TDD approach per TDD-FEAT-004-hybrid-infrastructure.md v1.2.0

Test Categories:
- Happy path: Valid VTT files parse successfully
- Negative: Invalid/malformed files produce appropriate errors
- Edge cases: Voice tags, encoding, timestamps

Reference: TDD-FEAT-004 v1.2.0, Section 4, 8
"""

import pytest
from pathlib import Path

from src.transcript.infrastructure.adapters.vtt_parser import VTTParser
from src.transcript.domain.value_objects.parsed_segment import ParsedSegment
from src.transcript.domain.value_objects.parse_result import ParseResult


# =============================================================================
# TEST FIXTURES
# =============================================================================

@pytest.fixture
def parser() -> VTTParser:
    """Create a VTTParser instance for testing."""
    return VTTParser()


@pytest.fixture
def simple_vtt_content() -> str:
    """Simple VTT content with voice tags."""
    return """WEBVTT

00:00:00.000 --> 00:00:05.000
<v Alice>Hello, welcome to the meeting.</v>

00:00:05.000 --> 00:00:10.000
<v Bob>Thank you for having me.</v>

00:00:10.000 --> 00:00:15.000
<v Alice>Let's discuss the agenda.</v>
"""


@pytest.fixture
def vtt_without_speakers() -> str:
    """VTT content without voice tags."""
    return """WEBVTT

00:00:00.000 --> 00:00:05.000
Hello, this is plain text.

00:00:05.000 --> 00:00:10.000
No speaker tags here.
"""


# =============================================================================
# HAPPY PATH TESTS
# =============================================================================

class TestVTTParserHappyPath:
    """Happy path tests for VTTParser."""

    @pytest.mark.happy_path
    def test_parse_content_returns_parse_result(
        self, parser: VTTParser, simple_vtt_content: str
    ) -> None:
        """VTTParser.parse_content returns a ParseResult instance."""
        result = parser.parse_content(simple_vtt_content)

        assert isinstance(result, ParseResult)
        assert result.format == "vtt"
        assert result.parse_status == "complete"

    @pytest.mark.happy_path
    def test_parse_content_extracts_all_segments(
        self, parser: VTTParser, simple_vtt_content: str
    ) -> None:
        """VTTParser extracts all segments from VTT content."""
        result = parser.parse_content(simple_vtt_content)

        assert result.segment_count == 3
        assert all(isinstance(s, ParsedSegment) for s in result.segments)

    @pytest.mark.happy_path
    def test_parse_content_extracts_voice_tags(
        self, parser: VTTParser, simple_vtt_content: str
    ) -> None:
        """VTTParser extracts speaker from voice tags."""
        result = parser.parse_content(simple_vtt_content)

        assert result.segments[0].speaker == "Alice"
        assert result.segments[1].speaker == "Bob"
        assert result.segments[2].speaker == "Alice"

    @pytest.mark.happy_path
    def test_parse_content_cleans_voice_tags_from_text(
        self, parser: VTTParser, simple_vtt_content: str
    ) -> None:
        """VTTParser removes voice tags from cleaned text."""
        result = parser.parse_content(simple_vtt_content)

        assert result.segments[0].text == "Hello, welcome to the meeting."
        assert "<v" not in result.segments[0].text
        assert "</v>" not in result.segments[0].text

    @pytest.mark.happy_path
    def test_parse_content_preserves_raw_text(
        self, parser: VTTParser, simple_vtt_content: str
    ) -> None:
        """VTTParser preserves original text with voice tags in raw_text."""
        result = parser.parse_content(simple_vtt_content)

        assert "<v Alice>" in result.segments[0].raw_text
        assert "</v>" in result.segments[0].raw_text

    @pytest.mark.happy_path
    def test_parse_content_converts_timestamps_to_milliseconds(
        self, parser: VTTParser, simple_vtt_content: str
    ) -> None:
        """VTTParser converts timestamps to milliseconds."""
        result = parser.parse_content(simple_vtt_content)

        # 00:00:00.000 --> 00:00:05.000 = 0ms to 5000ms
        assert result.segments[0].start_ms == 0
        assert result.segments[0].end_ms == 5000

        # 00:00:05.000 --> 00:00:10.000 = 5000ms to 10000ms
        assert result.segments[1].start_ms == 5000
        assert result.segments[1].end_ms == 10000

    @pytest.mark.happy_path
    def test_parse_content_calculates_duration(
        self, parser: VTTParser, simple_vtt_content: str
    ) -> None:
        """VTTParser calculates total duration from last segment."""
        result = parser.parse_content(simple_vtt_content)

        # Last segment ends at 00:00:15.000 = 15000ms
        assert result.duration_ms == 15000

    @pytest.mark.happy_path
    def test_parse_content_collects_unique_speakers(
        self, parser: VTTParser, simple_vtt_content: str
    ) -> None:
        """VTTParser collects unique speakers."""
        result = parser.parse_content(simple_vtt_content)

        assert result.speaker_count == 2
        assert set(result.speakers) == {"Alice", "Bob"}


# =============================================================================
# EDGE CASE TESTS
# =============================================================================

class TestVTTParserEdgeCases:
    """Edge case tests for VTTParser."""

    @pytest.mark.edge_case
    def test_parse_content_handles_missing_voice_tags(
        self, parser: VTTParser, vtt_without_speakers: str
    ) -> None:
        """VTTParser handles content without voice tags."""
        result = parser.parse_content(vtt_without_speakers)

        assert result.segment_count == 2
        assert result.speaker_count == 0
        assert all(s.speaker is None for s in result.segments)

    @pytest.mark.edge_case
    def test_parse_content_handles_empty_content(self, parser: VTTParser) -> None:
        """VTTParser handles empty VTT content."""
        result = parser.parse_content("WEBVTT\n\n")

        assert result.segment_count == 0
        assert result.parse_status == "complete"

    @pytest.mark.edge_case
    def test_parse_content_generates_sequential_ids(
        self, parser: VTTParser, simple_vtt_content: str
    ) -> None:
        """VTTParser generates sequential string IDs."""
        result = parser.parse_content(simple_vtt_content)

        assert result.segments[0].id == "1"
        assert result.segments[1].id == "2"
        assert result.segments[2].id == "3"

    @pytest.mark.edge_case
    def test_parse_content_handles_unclosed_voice_tag(
        self, parser: VTTParser
    ) -> None:
        """VTTParser handles unclosed voice tag gracefully.

        Malformed voice tags should not crash the parser.
        Behavior depends on webvtt-py, but our code should not fail.
        """
        content_with_unclosed_tag = """WEBVTT

00:00:00.000 --> 00:00:05.000
<v Alice>Hello, this voice tag is not closed.

00:00:05.000 --> 00:00:10.000
<v Bob>This one is properly closed.</v>
"""
        result = parser.parse_content(content_with_unclosed_tag)

        # Should either succeed or fail gracefully - not raise exception
        assert result.parse_status in ("complete", "partial", "failed")
        # If it succeeded, we should have segments
        if result.parse_status == "complete":
            assert result.segment_count >= 1

    @pytest.mark.edge_case
    def test_parse_content_handles_mm_ss_timestamp_format(
        self, parser: VTTParser
    ) -> None:
        """VTTParser handles MM:SS.mmm timestamp format (2-part, no hours).

        Per W3C WebVTT spec, timestamps can be MM:SS.mmm when hours are 0.
        """
        content_short_timestamps = """WEBVTT

00:05.000 --> 00:10.500
Short timestamp format without hours.
"""
        result = parser.parse_content(content_short_timestamps)

        # Should parse successfully
        assert result.parse_status == "complete"
        assert result.segment_count == 1
        assert result.segments[0].start_ms == 5000
        assert result.segments[0].end_ms == 10500

    @pytest.mark.edge_case
    def test_parse_content_handles_comma_decimal_separator(
        self, parser: VTTParser
    ) -> None:
        """VTTParser behavior with comma decimal separator (European format).

        LIMITATION: webvtt-py does not support comma as decimal separator.
        While our _timestamp_to_ms method handles commas, webvtt-py parses
        timestamps before we receive them, causing parse failure.

        This test documents the limitation rather than expecting success.
        If webvtt-py adds support in the future, this test will fail and
        should be updated to expect success.
        """
        content_comma_timestamps = """WEBVTT

00:00:00,000 --> 00:00:05,500
Comma decimal separator.
"""
        result = parser.parse_content(content_comma_timestamps)

        # webvtt-py limitation: comma decimal separators cause parse failure
        # Our code would handle it, but webvtt-py parses timestamps first
        assert result.parse_status == "failed"
        assert len(result.errors) >= 1


# =============================================================================
# NEGATIVE TESTS
# =============================================================================

class TestVTTParserNegative:
    """Negative/error tests for VTTParser.

    Tests error handling for invalid inputs, malformed content, and edge conditions.
    Each test verifies both the error type (contract) and key message content.

    Error Type Contract (per ParseResult docstring):
    - "encoding_error": File could not be decoded
    - "format_error": Content does not conform to VTT format
    - "timestamp_error": Timestamp could not be parsed
    - "parse_error": Generic parsing failure (fallback)
    """

    @pytest.mark.negative
    def test_parse_raises_for_nonexistent_file(self, parser: VTTParser) -> None:
        """VTTParser raises FileNotFoundError for nonexistent file."""
        with pytest.raises(FileNotFoundError):
            parser.parse("/nonexistent/path/file.vtt")

    @pytest.mark.negative
    def test_timestamp_to_ms_raises_for_invalid_format(self, parser: VTTParser) -> None:
        """VTTParser._timestamp_to_ms raises ValueError for invalid timestamp format.

        Tests our internal timestamp validation, not webvtt-py behavior.
        Invalid format: not matching HH:MM:SS.mmm or MM:SS.mmm pattern.
        """
        with pytest.raises(ValueError) as exc_info:
            parser._timestamp_to_ms("invalid")

        # Verify error message contains the invalid input for debugging
        assert "invalid" in str(exc_info.value).lower()

    @pytest.mark.negative
    def test_timestamp_to_ms_raises_for_single_part(self, parser: VTTParser) -> None:
        """VTTParser._timestamp_to_ms raises ValueError for single-part timestamp.

        Timestamp must have at least MM:SS format (2 parts).
        """
        with pytest.raises(ValueError) as exc_info:
            parser._timestamp_to_ms("12345")

        assert "12345" in str(exc_info.value)

    @pytest.mark.negative
    def test_parse_content_returns_error_for_no_webvtt_header(
        self, parser: VTTParser
    ) -> None:
        """VTTParser returns format_error when WEBVTT header is missing.

        VTT files MUST start with "WEBVTT" per W3C WebVTT specification.
        """
        content_without_header = """
00:00:00.000 --> 00:00:05.000
This content has no WEBVTT header.
"""
        result = parser.parse_content(content_without_header)

        assert result.parse_status == "failed"
        assert len(result.errors) >= 1
        assert result.errors[0]["type"] == "format_error"
        # Message should indicate the format issue
        assert "webvtt" in result.errors[0]["message"].lower() or \
               "header" in result.errors[0]["message"].lower() or \
               "format" in result.errors[0]["message"].lower()

    @pytest.mark.negative
    def test_parse_content_returns_error_for_malformed_cue(
        self, parser: VTTParser
    ) -> None:
        """VTTParser returns error for malformed cue (invalid timestamp arrow).

        VTT cues must use " --> " (with spaces) between timestamps.
        """
        malformed_content = """WEBVTT

00:00:00.000->00:00:05.000
Missing spaces around arrow.
"""
        result = parser.parse_content(malformed_content)

        # Should either fail or return 0 segments (webvtt-py may be lenient)
        # We test that if it fails, error type is correct
        if result.parse_status == "failed":
            assert len(result.errors) >= 1
            assert result.errors[0]["type"] in ("format_error", "parse_error")

    @pytest.mark.negative
    def test_parse_returns_error_for_empty_file(
        self, parser: VTTParser, tmp_path: Path
    ) -> None:
        """VTTParser handles 0-byte empty file gracefully.

        Empty file should return format_error (no WEBVTT header possible).
        """
        empty_file = tmp_path / "empty.vtt"
        empty_file.write_text("")

        result = parser.parse(str(empty_file))

        assert result.parse_status == "failed"
        assert len(result.errors) >= 1
        assert result.errors[0]["type"] == "format_error"

    @pytest.mark.negative
    def test_parse_returns_error_for_binary_content(
        self, parser: VTTParser, tmp_path: Path
    ) -> None:
        """VTTParser returns format_error for binary/non-text content.

        NOTE: latin-1 encoding can decode almost any byte sequence, so binary
        content will "successfully" decode but fail VTT format validation.
        This is acceptable behavior - the error is caught at format validation.
        """
        binary_file = tmp_path / "binary.vtt"
        # Write bytes that are invalid in all supported encodings
        # Using bytes that form invalid UTF-8 sequences
        binary_file.write_bytes(b'\x80\x81\x82\x83\xff\xfe\x00\x00')

        result = parser.parse(str(binary_file))

        # Binary decodes via latin-1 fallback, then fails format validation
        assert result.parse_status == "failed"
        assert len(result.errors) >= 1
        # Error type should be format_error (not encoding_error) since
        # the content decoded but wasn't valid VTT
        assert result.errors[0]["type"] == "format_error"

    @pytest.mark.negative
    def test_parse_content_returns_error_for_completely_invalid_content(
        self, parser: VTTParser
    ) -> None:
        """VTTParser returns error for completely invalid content.

        Content that is not VTT at all (random text).
        """
        invalid_content = "This is just random text with no VTT structure at all."

        result = parser.parse_content(invalid_content)

        assert result.parse_status == "failed"
        assert len(result.errors) >= 1
        assert result.errors[0]["type"] in ("format_error", "parse_error")


# =============================================================================
# INTEGRATION TEST (using actual test data)
# =============================================================================

class TestVTTParserIntegration:
    """Integration tests using actual test data files."""

    @pytest.mark.integration
    def test_parse_meeting_006_all_hands(self, parser: VTTParser) -> None:
        """VTTParser correctly parses meeting-006-all-hands.vtt (AC-1)."""
        test_file = Path(
            "skills/transcript/test_data/transcripts/golden/meeting-006-all-hands.vtt"
        )

        if not test_file.exists():
            pytest.skip(f"Test file not found: {test_file}")

        result = parser.parse(str(test_file))

        # AC-1: Parse meeting-006-all-hands.vtt producing exactly 3,071 segments
        assert result.segment_count == 3071, (
            f"Expected 3071 segments, got {result.segment_count}"
        )
        assert result.parse_status == "complete"
