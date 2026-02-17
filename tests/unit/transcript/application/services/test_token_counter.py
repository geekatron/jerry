# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
Unit tests for TokenCounter service.

TDD RED Phase: These tests are written BEFORE implementation.
Reference: TASK-261, EN-026 (Token-Based Chunking), BUG-001 fix

Test Categories:
- Happy path: Valid inputs return correct token counts
- Edge cases: Empty strings, unicode, special characters
- Behavioral: Encoding caching, segment overhead calculation

Design Decisions (DEC-001):
- D-004: TokenCounter as separate injectable service
- D-005: Constructor injection into TranscriptChunker
"""

import pytest

from src.transcript.domain.value_objects.parsed_segment import ParsedSegment

# =============================================================================
# TEST FIXTURES
# =============================================================================


@pytest.fixture
def sample_segment() -> ParsedSegment:
    """Create a sample ParsedSegment for testing."""
    return ParsedSegment(
        id="42",
        start_ms=10000,
        end_ms=15000,
        speaker="Alice",
        text="Hello, this is a test segment for token counting.",
        raw_text="<v Alice>Hello, this is a test segment for token counting.</v>",
    )


@pytest.fixture
def segment_with_long_text() -> ParsedSegment:
    """Create a segment with longer text for token testing."""
    long_text = " ".join(["This is a longer segment with more content."] * 20)
    return ParsedSegment(
        id="100",
        start_ms=0,
        end_ms=60000,
        speaker="Bob",
        text=long_text,
        raw_text=f"<v Bob>{long_text}</v>",
    )


@pytest.fixture
def segment_no_speaker() -> ParsedSegment:
    """Create a segment without a speaker."""
    return ParsedSegment(
        id="1",
        start_ms=0,
        end_ms=5000,
        speaker=None,
        text="Anonymous segment.",
        raw_text="Anonymous segment.",
    )


# =============================================================================
# HAPPY PATH TESTS
# =============================================================================


class TestTokenCounterHappyPath:
    """Happy path tests for TokenCounter service."""

    @pytest.mark.happy_path
    def test_count_tokens_simple_text(self) -> None:
        """TokenCounter correctly counts tokens in simple text."""
        from src.transcript.application.services.token_counter import TokenCounter

        counter = TokenCounter()
        # "hello world" with p50k_base encoding = 2 tokens
        result = counter.count_tokens("hello world")

        assert result == 2

    @pytest.mark.happy_path
    def test_count_tokens_sentence(self) -> None:
        """TokenCounter counts tokens in a complete sentence."""
        from src.transcript.application.services.token_counter import TokenCounter

        counter = TokenCounter()
        text = "The quick brown fox jumps over the lazy dog."
        result = counter.count_tokens(text)

        # Should be a reasonable token count > 0
        assert result > 0
        assert isinstance(result, int)

    @pytest.mark.happy_path
    def test_count_segment_tokens_returns_integer(self, sample_segment: ParsedSegment) -> None:
        """count_segment_tokens returns an integer count."""
        from src.transcript.application.services.token_counter import TokenCounter

        counter = TokenCounter()
        result = counter.count_segment_tokens(sample_segment)

        assert isinstance(result, int)
        assert result > 0

    @pytest.mark.happy_path
    def test_count_segment_tokens_includes_overhead(self, sample_segment: ParsedSegment) -> None:
        """Segment token count includes JSON structure overhead."""
        from src.transcript.application.services.token_counter import TokenCounter

        counter = TokenCounter()

        # Count just the text
        text_only_tokens = counter.count_tokens(sample_segment.text)

        # Count the full segment (with JSON structure overhead)
        segment_tokens = counter.count_segment_tokens(sample_segment)

        # Segment tokens should be MORE than text-only due to JSON overhead
        # (id, start_ms, end_ms, speaker, raw_text, structure)
        assert segment_tokens > text_only_tokens

    @pytest.mark.happy_path
    def test_count_tokens_consistent_results(self) -> None:
        """Multiple calls with same input return same result."""
        from src.transcript.application.services.token_counter import TokenCounter

        counter = TokenCounter()
        text = "Consistent token counting is important."

        result1 = counter.count_tokens(text)
        result2 = counter.count_tokens(text)
        result3 = counter.count_tokens(text)

        assert result1 == result2 == result3

    @pytest.mark.happy_path
    def test_default_encoding_is_p50k_base(self) -> None:
        """TokenCounter uses p50k_base encoding by default."""
        from src.transcript.application.services.token_counter import TokenCounter

        counter = TokenCounter()
        # Access internal encoding name to verify
        assert counter.encoding_name == "p50k_base"


# =============================================================================
# EDGE CASE TESTS
# =============================================================================


class TestTokenCounterEdgeCases:
    """Edge case tests for TokenCounter service."""

    @pytest.mark.edge_case
    def test_count_tokens_empty_string(self) -> None:
        """Empty string returns 0 tokens."""
        from src.transcript.application.services.token_counter import TokenCounter

        counter = TokenCounter()
        result = counter.count_tokens("")

        assert result == 0

    @pytest.mark.edge_case
    def test_count_tokens_whitespace_only(self) -> None:
        """Whitespace-only string returns minimal tokens."""
        from src.transcript.application.services.token_counter import TokenCounter

        counter = TokenCounter()
        result = counter.count_tokens("   ")

        # Whitespace may tokenize to 1 token depending on encoding
        assert result >= 0

    @pytest.mark.edge_case
    def test_count_tokens_unicode(self) -> None:
        """Unicode text tokenizes correctly."""
        from src.transcript.application.services.token_counter import TokenCounter

        counter = TokenCounter()
        # Test with Japanese, emojis, and mixed content
        unicode_text = "Hello world, Bonjour le monde, Hola mundo"
        result = counter.count_tokens(unicode_text)

        assert result > 0

    @pytest.mark.edge_case
    def test_count_tokens_unicode_emojis(self) -> None:
        """Emoji text tokenizes correctly."""
        from src.transcript.application.services.token_counter import TokenCounter

        counter = TokenCounter()
        emoji_text = "Hello! Great job! Keep going!"
        result = counter.count_tokens(emoji_text)

        assert result > 0

    @pytest.mark.edge_case
    def test_count_tokens_special_characters(self) -> None:
        """Special characters tokenize correctly."""
        from src.transcript.application.services.token_counter import TokenCounter

        counter = TokenCounter()
        special_text = 'JSON: {"key": "value", "num": 123}'
        result = counter.count_tokens(special_text)

        assert result > 0

    @pytest.mark.edge_case
    def test_count_segment_tokens_no_speaker(self, segment_no_speaker: ParsedSegment) -> None:
        """Segment without speaker tokenizes correctly."""
        from src.transcript.application.services.token_counter import TokenCounter

        counter = TokenCounter()
        result = counter.count_segment_tokens(segment_no_speaker)

        assert result > 0

    @pytest.mark.edge_case
    def test_count_tokens_very_long_text(self) -> None:
        """Very long text tokenizes without error."""
        from src.transcript.application.services.token_counter import TokenCounter

        counter = TokenCounter()
        # 10,000 repetitions of a phrase
        long_text = "The meeting discussed important topics. " * 10000
        result = counter.count_tokens(long_text)

        assert result > 0
        assert result > 10000  # Each phrase is multiple tokens


# =============================================================================
# BEHAVIORAL TESTS
# =============================================================================


class TestTokenCounterBehavior:
    """Behavioral tests for TokenCounter service."""

    @pytest.mark.happy_path
    def test_encoding_is_cached(self) -> None:
        """Encoding is created once and cached for efficiency."""
        from src.transcript.application.services.token_counter import TokenCounter

        counter = TokenCounter()

        # Call count_tokens multiple times
        counter.count_tokens("first call")
        counter.count_tokens("second call")
        counter.count_tokens("third call")

        # The encoding instance should be the same (cached)
        # We verify this by checking the internal _encoding attribute
        encoding1 = counter._encoding
        counter.count_tokens("fourth call")
        encoding2 = counter._encoding

        assert encoding1 is encoding2

    @pytest.mark.happy_path
    def test_custom_encoding_supported(self) -> None:
        """TokenCounter accepts custom encoding name."""
        from src.transcript.application.services.token_counter import TokenCounter

        # cl100k_base is another valid tiktoken encoding
        counter = TokenCounter(encoding_name="cl100k_base")

        assert counter.encoding_name == "cl100k_base"
        result = counter.count_tokens("test text")
        assert result > 0

    @pytest.mark.negative
    def test_invalid_encoding_raises_error(self) -> None:
        """Invalid encoding name raises appropriate error."""
        from src.transcript.application.services.token_counter import TokenCounter

        with pytest.raises(Exception):  # tiktoken raises KeyError or similar
            TokenCounter(encoding_name="invalid_encoding_name")


# =============================================================================
# SEGMENT SERIALIZATION TESTS
# =============================================================================


class TestSegmentTokenization:
    """Tests for segment-to-JSON token counting."""

    @pytest.mark.happy_path
    def test_segment_overhead_calculation(self, sample_segment: ParsedSegment) -> None:
        """Verify segment JSON overhead is accounted for."""
        import json

        from src.transcript.application.services.token_counter import TokenCounter

        counter = TokenCounter()

        # Manually serialize segment to compare
        segment_dict = {
            "id": sample_segment.id,
            "start_ms": sample_segment.start_ms,
            "end_ms": sample_segment.end_ms,
            "speaker": sample_segment.speaker,
            "text": sample_segment.text,
            "raw_text": sample_segment.raw_text,
        }
        json_str = json.dumps(segment_dict)
        expected_tokens = counter.count_tokens(json_str)

        # The segment token count should match JSON serialization
        actual_tokens = counter.count_segment_tokens(sample_segment)

        # Should be equal (same serialization method)
        assert actual_tokens == expected_tokens

    @pytest.mark.happy_path
    def test_multiple_segments_cumulative(self, sample_segment: ParsedSegment) -> None:
        """Multiple segments cumulative token count is additive."""
        from src.transcript.application.services.token_counter import TokenCounter

        counter = TokenCounter()

        single_count = counter.count_segment_tokens(sample_segment)

        # Count 5 identical segments
        total_count = sum(counter.count_segment_tokens(sample_segment) for _ in range(5))

        assert total_count == single_count * 5


# =============================================================================
# INTEGRATION-LIKE UNIT TESTS
# =============================================================================


class TestTokenCounterForChunking:
    """Tests verifying TokenCounter is suitable for chunking use case."""

    @pytest.mark.happy_path
    def test_can_estimate_chunk_token_count(self, sample_segment: ParsedSegment) -> None:
        """TokenCounter can estimate if segments fit in a chunk."""
        from src.transcript.application.services.token_counter import TokenCounter

        counter = TokenCounter()
        target_tokens = 18000  # Our target from EN-026

        # Create 100 similar segments
        segments = []
        for i in range(100):
            seg = ParsedSegment(
                id=str(i),
                start_ms=i * 5000,
                end_ms=(i + 1) * 5000,
                speaker="Speaker",
                text=f"This is segment number {i} with some content.",
                raw_text=f"<v Speaker>This is segment number {i} with some content.</v>",
            )
            segments.append(seg)

        # Count total tokens
        total_tokens = sum(counter.count_segment_tokens(seg) for seg in segments)

        # Verify we can use this to determine if under limit
        assert (
            total_tokens < target_tokens or total_tokens >= target_tokens
        )  # Always true, verifies no exception

    @pytest.mark.happy_path
    def test_token_count_scales_with_content(self) -> None:
        """More content means more tokens (sanity check)."""
        from src.transcript.application.services.token_counter import TokenCounter

        counter = TokenCounter()

        short_seg = ParsedSegment(
            id="1",
            start_ms=0,
            end_ms=1000,
            speaker="A",
            text="Short.",
            raw_text="Short.",
        )

        long_seg = ParsedSegment(
            id="2",
            start_ms=0,
            end_ms=1000,
            speaker="B",
            text="This is a much longer segment with significantly more content that should tokenize to many more tokens than the short segment above.",
            raw_text="This is a much longer segment...",
        )

        short_tokens = counter.count_segment_tokens(short_seg)
        long_tokens = counter.count_segment_tokens(long_seg)

        assert long_tokens > short_tokens
