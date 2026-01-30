"""
Unit tests for TranscriptChunker.

RED/GREEN/REFACTOR TDD approach per TDD-FEAT-004-hybrid-infrastructure.md v1.2.0

Test Categories (EN-021 target: 60% unit, 30% contract, 10% integration):
- Happy path: Valid segments chunk successfully
- Negative: Invalid inputs produce appropriate errors
- Edge cases: Boundary conditions, small inputs

Reference: TDD-FEAT-004 v1.2.0, Section 5, 8
"""

import json
import pytest
from pathlib import Path
from typing import List

from src.transcript.domain.value_objects.parsed_segment import ParsedSegment


# =============================================================================
# TEST FIXTURES
# =============================================================================

@pytest.fixture
def sample_segments() -> List[ParsedSegment]:
    """Create a list of sample segments for testing."""
    segments = []
    for i in range(1, 11):  # 10 segments
        segments.append(ParsedSegment(
            id=str(i),
            start_ms=(i - 1) * 5000,
            end_ms=i * 5000,
            speaker=f"Speaker {(i % 3) + 1}",
            text=f"This is segment {i} content.",
            raw_text=f"<v Speaker {(i % 3) + 1}>This is segment {i} content.</v>",
        ))
    return segments


@pytest.fixture
def large_segment_list() -> List[ParsedSegment]:
    """Create 1500 segments to test multi-chunk scenario."""
    segments = []
    for i in range(1, 1501):  # 1500 segments = 3 chunks with 500/chunk
        segments.append(ParsedSegment(
            id=str(i),
            start_ms=(i - 1) * 1000,
            end_ms=i * 1000,
            speaker=f"Speaker {(i % 10) + 1}",
            text=f"Content for segment {i}.",
            raw_text=f"<v Speaker {(i % 10) + 1}>Content for segment {i}.</v>",
        ))
    return segments


@pytest.fixture
def tmp_output_dir(tmp_path: Path) -> Path:
    """Create a temporary directory for chunk output."""
    return tmp_path / "chunks_output"


# =============================================================================
# HAPPY PATH TESTS
# =============================================================================

class TestChunkerHappyPath:
    """Happy path tests for TranscriptChunker."""

    @pytest.mark.happy_path
    def test_chunker_creates_index_and_chunks_directory(
        self, sample_segments: List[ParsedSegment], tmp_output_dir: Path
    ) -> None:
        """TranscriptChunker creates index.json and chunks/ directory."""
        from src.transcript.application.services.chunker import TranscriptChunker

        chunker = TranscriptChunker(chunk_size=5)
        result = chunker.chunk(sample_segments, str(tmp_output_dir))

        assert (tmp_output_dir / "index.json").exists()
        assert (tmp_output_dir / "chunks").is_dir()

    @pytest.mark.happy_path
    def test_chunker_produces_correct_number_of_chunks(
        self, large_segment_list: List[ParsedSegment], tmp_output_dir: Path
    ) -> None:
        """TranscriptChunker produces correct number of chunks (1500 / 500 = 3)."""
        from src.transcript.application.services.chunker import TranscriptChunker

        chunker = TranscriptChunker(chunk_size=500)
        result = chunker.chunk(large_segment_list, str(tmp_output_dir))

        # Check index.json reports correct chunk count
        with open(tmp_output_dir / "index.json") as f:
            index = json.load(f)

        assert index["total_chunks"] == 3
        assert len(index["chunks"]) == 3

    @pytest.mark.happy_path
    def test_chunker_index_contains_required_fields(
        self, sample_segments: List[ParsedSegment], tmp_output_dir: Path
    ) -> None:
        """Index.json contains all required fields per schema."""
        from src.transcript.application.services.chunker import TranscriptChunker

        chunker = TranscriptChunker(chunk_size=5)
        chunker.chunk(sample_segments, str(tmp_output_dir))

        with open(tmp_output_dir / "index.json") as f:
            index = json.load(f)

        # Required fields per index.schema.json
        assert "schema_version" in index
        assert index["schema_version"] == "1.0"
        assert "total_segments" in index
        assert "total_chunks" in index
        assert "chunk_size" in index
        assert "chunks" in index

    @pytest.mark.happy_path
    def test_chunker_chunk_files_contain_required_fields(
        self, sample_segments: List[ParsedSegment], tmp_output_dir: Path
    ) -> None:
        """Chunk files contain all required fields per schema."""
        from src.transcript.application.services.chunker import TranscriptChunker

        chunker = TranscriptChunker(chunk_size=5)
        chunker.chunk(sample_segments, str(tmp_output_dir))

        chunk_file = tmp_output_dir / "chunks" / "chunk-001.json"
        with open(chunk_file) as f:
            chunk = json.load(f)

        # Required fields per chunk.schema.json
        assert "chunk_id" in chunk
        assert "schema_version" in chunk
        assert "segment_range" in chunk
        assert "segments" in chunk
        assert "navigation" in chunk

    @pytest.mark.happy_path
    def test_chunker_segments_preserved_across_chunks(
        self, large_segment_list: List[ParsedSegment], tmp_output_dir: Path
    ) -> None:
        """Total segments across all chunks equals input segment count."""
        from src.transcript.application.services.chunker import TranscriptChunker

        chunker = TranscriptChunker(chunk_size=500)
        chunker.chunk(large_segment_list, str(tmp_output_dir))

        # Count segments in all chunks
        total_segments = 0
        chunks_dir = tmp_output_dir / "chunks"
        for chunk_file in sorted(chunks_dir.glob("chunk-*.json")):
            with open(chunk_file) as f:
                chunk = json.load(f)
            total_segments += len(chunk["segments"])

        assert total_segments == len(large_segment_list)

    @pytest.mark.happy_path
    def test_chunker_collects_unique_speakers(
        self, sample_segments: List[ParsedSegment], tmp_output_dir: Path
    ) -> None:
        """Index.json contains speaker metadata."""
        from src.transcript.application.services.chunker import TranscriptChunker

        chunker = TranscriptChunker(chunk_size=5)
        chunker.chunk(sample_segments, str(tmp_output_dir))

        with open(tmp_output_dir / "index.json") as f:
            index = json.load(f)

        assert "speakers" in index
        assert index["speakers"]["count"] == 3  # Speaker 1, 2, 3

    @pytest.mark.happy_path
    def test_chunker_calculates_duration(
        self, sample_segments: List[ParsedSegment], tmp_output_dir: Path
    ) -> None:
        """Index.json contains calculated duration."""
        from src.transcript.application.services.chunker import TranscriptChunker

        chunker = TranscriptChunker(chunk_size=5)
        chunker.chunk(sample_segments, str(tmp_output_dir))

        with open(tmp_output_dir / "index.json") as f:
            index = json.load(f)

        # 10 segments * 5000ms each = 50000ms total
        assert index["duration_ms"] == 50000

    @pytest.mark.happy_path
    def test_chunker_returns_index_path(
        self, sample_segments: List[ParsedSegment], tmp_output_dir: Path
    ) -> None:
        """TranscriptChunker.chunk() returns path to index.json."""
        from src.transcript.application.services.chunker import TranscriptChunker

        chunker = TranscriptChunker(chunk_size=5)
        result = chunker.chunk(sample_segments, str(tmp_output_dir))

        assert result == str(tmp_output_dir / "index.json")


# =============================================================================
# EDGE CASE TESTS
# =============================================================================

class TestChunkerEdgeCases:
    """Edge case tests for TranscriptChunker."""

    @pytest.mark.edge_case
    def test_chunker_single_segment(
        self, tmp_output_dir: Path
    ) -> None:
        """TranscriptChunker handles single segment (1 chunk)."""
        from src.transcript.application.services.chunker import TranscriptChunker

        single_segment = [ParsedSegment(
            id="1",
            start_ms=0,
            end_ms=5000,
            speaker="Alice",
            text="Single segment.",
            raw_text="<v Alice>Single segment.</v>",
        )]

        chunker = TranscriptChunker(chunk_size=500)
        chunker.chunk(single_segment, str(tmp_output_dir))

        with open(tmp_output_dir / "index.json") as f:
            index = json.load(f)

        assert index["total_segments"] == 1
        assert index["total_chunks"] == 1

    @pytest.mark.edge_case
    def test_chunker_exactly_chunk_size_segments(
        self, tmp_output_dir: Path
    ) -> None:
        """Exactly chunk_size segments produces 1 chunk."""
        from src.transcript.application.services.chunker import TranscriptChunker

        segments = [
            ParsedSegment(
                id=str(i),
                start_ms=(i - 1) * 1000,
                end_ms=i * 1000,
                speaker="Speaker",
                text=f"Segment {i}",
                raw_text=f"Segment {i}",
            )
            for i in range(1, 501)  # Exactly 500
        ]

        chunker = TranscriptChunker(chunk_size=500)
        chunker.chunk(segments, str(tmp_output_dir))

        with open(tmp_output_dir / "index.json") as f:
            index = json.load(f)

        assert index["total_chunks"] == 1

    @pytest.mark.edge_case
    def test_chunker_chunk_size_plus_one_segments(
        self, tmp_output_dir: Path
    ) -> None:
        """chunk_size + 1 segments produces 2 chunks."""
        from src.transcript.application.services.chunker import TranscriptChunker

        segments = [
            ParsedSegment(
                id=str(i),
                start_ms=(i - 1) * 1000,
                end_ms=i * 1000,
                speaker="Speaker",
                text=f"Segment {i}",
                raw_text=f"Segment {i}",
            )
            for i in range(1, 502)  # 501 segments
        ]

        chunker = TranscriptChunker(chunk_size=500)
        chunker.chunk(segments, str(tmp_output_dir))

        with open(tmp_output_dir / "index.json") as f:
            index = json.load(f)

        assert index["total_chunks"] == 2

        # Last chunk should have 1 segment
        chunk_2 = tmp_output_dir / "chunks" / "chunk-002.json"
        with open(chunk_2) as f:
            chunk = json.load(f)
        assert len(chunk["segments"]) == 1

    @pytest.mark.edge_case
    def test_chunker_custom_chunk_size(
        self, sample_segments: List[ParsedSegment], tmp_output_dir: Path
    ) -> None:
        """TranscriptChunker respects custom chunk_size."""
        from src.transcript.application.services.chunker import TranscriptChunker

        chunker = TranscriptChunker(chunk_size=3)  # 10 segments / 3 = 4 chunks
        chunker.chunk(sample_segments, str(tmp_output_dir))

        with open(tmp_output_dir / "index.json") as f:
            index = json.load(f)

        assert index["chunk_size"] == 3
        assert index["total_chunks"] == 4  # 3+3+3+1

    @pytest.mark.edge_case
    def test_chunker_no_speakers(
        self, tmp_output_dir: Path
    ) -> None:
        """TranscriptChunker handles segments with no speakers."""
        from src.transcript.application.services.chunker import TranscriptChunker

        segments = [
            ParsedSegment(
                id=str(i),
                start_ms=(i - 1) * 1000,
                end_ms=i * 1000,
                speaker=None,  # No speaker
                text=f"Segment {i}",
                raw_text=f"Segment {i}",
            )
            for i in range(1, 6)
        ]

        chunker = TranscriptChunker(chunk_size=500)
        chunker.chunk(segments, str(tmp_output_dir))

        with open(tmp_output_dir / "index.json") as f:
            index = json.load(f)

        assert index["speakers"]["count"] == 0


# =============================================================================
# NEGATIVE TESTS
# =============================================================================

class TestChunkerNegative:
    """Negative/error tests for TranscriptChunker."""

    @pytest.mark.negative
    def test_chunker_raises_for_empty_segments(
        self, tmp_output_dir: Path
    ) -> None:
        """TranscriptChunker raises ValueError for empty segments list."""
        from src.transcript.application.services.chunker import TranscriptChunker

        chunker = TranscriptChunker(chunk_size=500)

        with pytest.raises(ValueError) as exc_info:
            chunker.chunk([], str(tmp_output_dir))

        assert "empty" in str(exc_info.value).lower()

    @pytest.mark.negative
    def test_chunker_raises_for_zero_chunk_size(self) -> None:
        """TranscriptChunker raises ValueError for chunk_size=0."""
        from src.transcript.application.services.chunker import TranscriptChunker

        with pytest.raises(ValueError) as exc_info:
            TranscriptChunker(chunk_size=0)

        assert "chunk_size" in str(exc_info.value).lower()

    @pytest.mark.negative
    def test_chunker_raises_for_negative_chunk_size(self) -> None:
        """TranscriptChunker raises ValueError for negative chunk_size."""
        from src.transcript.application.services.chunker import TranscriptChunker

        with pytest.raises(ValueError) as exc_info:
            TranscriptChunker(chunk_size=-1)

        assert "chunk_size" in str(exc_info.value).lower()


# =============================================================================
# NAVIGATION TESTS
# =============================================================================

class TestChunkerNavigation:
    """Tests for chunk navigation links (TASK-213)."""

    @pytest.mark.happy_path
    def test_chunker_first_chunk_has_no_previous(
        self, large_segment_list: List[ParsedSegment], tmp_output_dir: Path
    ) -> None:
        """First chunk has previous: null."""
        from src.transcript.application.services.chunker import TranscriptChunker

        chunker = TranscriptChunker(chunk_size=500)
        chunker.chunk(large_segment_list, str(tmp_output_dir))

        chunk_1 = tmp_output_dir / "chunks" / "chunk-001.json"
        with open(chunk_1) as f:
            chunk = json.load(f)

        assert chunk["navigation"]["previous"] is None

    @pytest.mark.happy_path
    def test_chunker_last_chunk_has_no_next(
        self, large_segment_list: List[ParsedSegment], tmp_output_dir: Path
    ) -> None:
        """Last chunk has next: null."""
        from src.transcript.application.services.chunker import TranscriptChunker

        chunker = TranscriptChunker(chunk_size=500)
        chunker.chunk(large_segment_list, str(tmp_output_dir))

        chunk_3 = tmp_output_dir / "chunks" / "chunk-003.json"
        with open(chunk_3) as f:
            chunk = json.load(f)

        assert chunk["navigation"]["next"] is None

    @pytest.mark.happy_path
    def test_chunker_middle_chunk_has_both_links(
        self, large_segment_list: List[ParsedSegment], tmp_output_dir: Path
    ) -> None:
        """Middle chunk has both previous and next links."""
        from src.transcript.application.services.chunker import TranscriptChunker

        chunker = TranscriptChunker(chunk_size=500)
        chunker.chunk(large_segment_list, str(tmp_output_dir))

        chunk_2 = tmp_output_dir / "chunks" / "chunk-002.json"
        with open(chunk_2) as f:
            chunk = json.load(f)

        assert chunk["navigation"]["previous"] is not None
        assert chunk["navigation"]["next"] is not None
        assert "chunk-001" in chunk["navigation"]["previous"]
        assert "chunk-003" in chunk["navigation"]["next"]

    @pytest.mark.happy_path
    def test_chunker_all_chunks_have_index_link(
        self, large_segment_list: List[ParsedSegment], tmp_output_dir: Path
    ) -> None:
        """All chunks have link back to index.json."""
        from src.transcript.application.services.chunker import TranscriptChunker

        chunker = TranscriptChunker(chunk_size=500)
        chunker.chunk(large_segment_list, str(tmp_output_dir))

        chunks_dir = tmp_output_dir / "chunks"
        for chunk_file in chunks_dir.glob("chunk-*.json"):
            with open(chunk_file) as f:
                chunk = json.load(f)
            assert "index" in chunk["navigation"]
            assert chunk["navigation"]["index"] is not None


# =============================================================================
# TOKEN-BASED CHUNKING TESTS (EN-026, TASK-262)
# =============================================================================

class TestChunkerTokenBased:
    """Token-based chunking tests per EN-026 (BUG-001 fix).

    TDD RED Phase: These tests written BEFORE implementation.
    Reference: TASK-262, DEC-001 (D-005, D-006, D-007)
    """

    @pytest.mark.happy_path
    def test_chunker_accepts_target_tokens_parameter(
        self, sample_segments: List[ParsedSegment], tmp_output_dir: Path
    ) -> None:
        """TranscriptChunker accepts target_tokens parameter."""
        from src.transcript.application.services.chunker import TranscriptChunker

        # Should not raise an error
        chunker = TranscriptChunker(target_tokens=18000)
        result = chunker.chunk(sample_segments, str(tmp_output_dir))

        assert (tmp_output_dir / "index.json").exists()

    @pytest.mark.happy_path
    def test_chunker_default_target_tokens_is_18000(self) -> None:
        """Default target_tokens value is 18000 when specified."""
        from src.transcript.application.services.chunker import TranscriptChunker

        # When target_tokens is explicitly set to use default
        chunker = TranscriptChunker(target_tokens=18000)
        assert chunker.target_tokens == 18000

    @pytest.mark.happy_path
    def test_chunker_target_tokens_takes_precedence(
        self, sample_segments: List[ParsedSegment], tmp_output_dir: Path
    ) -> None:
        """target_tokens takes precedence over chunk_size when both provided."""
        from src.transcript.application.services.chunker import TranscriptChunker

        # Both parameters provided - target_tokens should win
        chunker = TranscriptChunker(chunk_size=2, target_tokens=18000)

        # If chunk_size were used, we'd get 5 chunks (10 segments / 2)
        # With token-based, we'll get fewer chunks since 18000 tokens is generous
        chunker.chunk(sample_segments, str(tmp_output_dir))

        with open(tmp_output_dir / "index.json") as f:
            index = json.load(f)

        # With 18000 tokens target, 10 small segments should fit in 1 chunk
        assert index["total_chunks"] < 5  # Less than segment-based would produce

    @pytest.mark.happy_path
    def test_chunker_accepts_token_counter_injection(
        self, sample_segments: List[ParsedSegment], tmp_output_dir: Path
    ) -> None:
        """TranscriptChunker accepts TokenCounter via constructor injection."""
        from src.transcript.application.services.chunker import TranscriptChunker
        from src.transcript.application.services.token_counter import TokenCounter

        # Create a TokenCounter instance
        token_counter = TokenCounter()

        # Inject into chunker
        chunker = TranscriptChunker(target_tokens=18000, token_counter=token_counter)
        result = chunker.chunk(sample_segments, str(tmp_output_dir))

        assert (tmp_output_dir / "index.json").exists()

    @pytest.mark.happy_path
    def test_chunker_token_based_respects_limit(
        self, large_segment_list: List[ParsedSegment], tmp_output_dir: Path
    ) -> None:
        """Token-based chunks don't exceed target_tokens limit."""
        from src.transcript.application.services.chunker import TranscriptChunker
        from src.transcript.application.services.token_counter import TokenCounter

        target = 5000  # Small target to force multiple chunks
        token_counter = TokenCounter()
        chunker = TranscriptChunker(target_tokens=target, token_counter=token_counter)
        chunker.chunk(large_segment_list, str(tmp_output_dir))

        # Verify each chunk is under the target
        chunks_dir = tmp_output_dir / "chunks"
        for chunk_file in sorted(chunks_dir.glob("chunk-*.json")):
            with open(chunk_file) as f:
                chunk = json.load(f)

            # Count tokens in this chunk
            chunk_text = json.dumps(chunk["segments"])
            chunk_tokens = token_counter.count_tokens(chunk_text)

            # Should be under target (with some margin for JSON overhead)
            assert chunk_tokens <= target * 1.1  # 10% margin for overhead

    @pytest.mark.happy_path
    def test_chunker_token_based_index_contains_target_tokens(
        self, sample_segments: List[ParsedSegment], tmp_output_dir: Path
    ) -> None:
        """Index.json contains target_tokens field when token-based chunking used."""
        from src.transcript.application.services.chunker import TranscriptChunker

        chunker = TranscriptChunker(target_tokens=18000)
        chunker.chunk(sample_segments, str(tmp_output_dir))

        with open(tmp_output_dir / "index.json") as f:
            index = json.load(f)

        assert "target_tokens" in index
        assert index["target_tokens"] == 18000

    @pytest.mark.happy_path
    def test_chunker_creates_token_counter_internally_if_not_injected(
        self, sample_segments: List[ParsedSegment], tmp_output_dir: Path
    ) -> None:
        """TokenCounter is created internally if not injected."""
        from src.transcript.application.services.chunker import TranscriptChunker

        # No token_counter injected - should create one internally
        chunker = TranscriptChunker(target_tokens=18000)
        result = chunker.chunk(sample_segments, str(tmp_output_dir))

        assert (tmp_output_dir / "index.json").exists()

    @pytest.mark.edge_case
    def test_chunker_token_based_single_segment_under_limit(
        self, tmp_output_dir: Path
    ) -> None:
        """Single segment under target_tokens produces 1 chunk."""
        from src.transcript.application.services.chunker import TranscriptChunker

        single_segment = [ParsedSegment(
            id="1",
            start_ms=0,
            end_ms=5000,
            speaker="Alice",
            text="Short content.",
            raw_text="<v Alice>Short content.</v>",
        )]

        chunker = TranscriptChunker(target_tokens=18000)
        chunker.chunk(single_segment, str(tmp_output_dir))

        with open(tmp_output_dir / "index.json") as f:
            index = json.load(f)

        assert index["total_chunks"] == 1

    @pytest.mark.edge_case
    def test_chunker_token_based_forces_split_on_large_content(
        self, tmp_output_dir: Path
    ) -> None:
        """Large content segments are split into multiple chunks."""
        from src.transcript.application.services.chunker import TranscriptChunker

        # Create segments with substantial content
        segments = []
        for i in range(20):
            long_text = f"This is segment {i} with substantial content. " * 100
            segments.append(ParsedSegment(
                id=str(i),
                start_ms=i * 5000,
                end_ms=(i + 1) * 5000,
                speaker="Speaker",
                text=long_text,
                raw_text=f"<v Speaker>{long_text}</v>",
            ))

        # Use a smaller target to force splitting
        chunker = TranscriptChunker(target_tokens=2000)
        chunker.chunk(segments, str(tmp_output_dir))

        with open(tmp_output_dir / "index.json") as f:
            index = json.load(f)

        # Should produce multiple chunks due to token limit
        assert index["total_chunks"] > 1


class TestChunkerDeprecation:
    """Deprecation warning tests per DEC-001 D-007."""

    @pytest.mark.happy_path
    def test_chunk_size_alone_logs_deprecation_warning(
        self, sample_segments: List[ParsedSegment], tmp_output_dir: Path, caplog
    ) -> None:
        """Using chunk_size without target_tokens logs deprecation warning."""
        import logging
        from src.transcript.application.services.chunker import TranscriptChunker

        with caplog.at_level(logging.WARNING):
            chunker = TranscriptChunker(chunk_size=500)  # No target_tokens
            chunker.chunk(sample_segments, str(tmp_output_dir))

        # Should log deprecation warning
        assert any("deprecat" in record.message.lower() for record in caplog.records)

    @pytest.mark.happy_path
    def test_target_tokens_does_not_log_deprecation(
        self, sample_segments: List[ParsedSegment], tmp_output_dir: Path, caplog
    ) -> None:
        """Using target_tokens does not log deprecation warning."""
        import logging
        from src.transcript.application.services.chunker import TranscriptChunker

        with caplog.at_level(logging.WARNING):
            chunker = TranscriptChunker(target_tokens=18000)
            chunker.chunk(sample_segments, str(tmp_output_dir))

        # Should NOT log deprecation warning
        assert not any("deprecat" in record.message.lower() for record in caplog.records)


class TestChunkerBackwardCompatibility:
    """Backward compatibility tests - existing behavior must not break."""

    @pytest.mark.happy_path
    def test_backward_compat_chunk_size_only_still_works(
        self, sample_segments: List[ParsedSegment], tmp_output_dir: Path
    ) -> None:
        """TranscriptChunker(chunk_size=X) still works as before."""
        from src.transcript.application.services.chunker import TranscriptChunker

        # Old usage pattern - should still work
        chunker = TranscriptChunker(chunk_size=3)
        result = chunker.chunk(sample_segments, str(tmp_output_dir))

        with open(tmp_output_dir / "index.json") as f:
            index = json.load(f)

        # 10 segments / 3 per chunk = 4 chunks (segment-based behavior)
        assert index["total_chunks"] == 4
        assert index["chunk_size"] == 3

    @pytest.mark.happy_path
    def test_backward_compat_default_constructor_works(
        self, large_segment_list: List[ParsedSegment], tmp_output_dir: Path
    ) -> None:
        """TranscriptChunker() with no args still works (uses default chunk_size=500)."""
        from src.transcript.application.services.chunker import TranscriptChunker

        # Default constructor - should use segment-based with chunk_size=500
        chunker = TranscriptChunker()
        result = chunker.chunk(large_segment_list, str(tmp_output_dir))

        with open(tmp_output_dir / "index.json") as f:
            index = json.load(f)

        # 1500 segments / 500 per chunk = 3 chunks
        assert index["total_chunks"] == 3
        assert index["chunk_size"] == 500
