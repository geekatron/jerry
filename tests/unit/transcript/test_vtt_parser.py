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


# =============================================================================
# NEGATIVE TESTS
# =============================================================================

class TestVTTParserNegative:
    """Negative/error tests for VTTParser."""

    @pytest.mark.negative
    def test_parse_raises_for_nonexistent_file(self, parser: VTTParser) -> None:
        """VTTParser raises FileNotFoundError for nonexistent file."""
        with pytest.raises(FileNotFoundError):
            parser.parse("/nonexistent/path/file.vtt")


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
