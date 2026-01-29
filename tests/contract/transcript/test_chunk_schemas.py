"""
Contract tests for TranscriptChunker output schema compliance.

These tests verify that generated index.json and chunk-NNN.json files
conform to the formal JSON Schema specifications.

Contract Reference:
    - skills/transcript/test_data/schemas/index.schema.json
    - skills/transcript/test_data/schemas/chunk.schema.json
    - TDD-FEAT-004 Section 5

Test Distribution per testing-standards.md:
    - Contract tests: 5% of total coverage
    - Focus: External interface/schema compliance

References:
    - TASK-215: Schema Validation Tests
    - EN-021: Chunking Strategy
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

from src.transcript.application.services.chunker import TranscriptChunker
from src.transcript.domain.value_objects.parsed_segment import ParsedSegment

# Try to import jsonschema for validation
try:
    import jsonschema
    from jsonschema import Draft202012Validator

    JSONSCHEMA_AVAILABLE = True
except ImportError:
    JSONSCHEMA_AVAILABLE = False


# Mark as contract tests
pytestmark = [
    pytest.mark.contract,
]


# =============================================================================
# Fixtures
# =============================================================================


@pytest.fixture
def project_root() -> Path:
    """Get the project root directory."""
    return Path(__file__).parent.parent.parent.parent


@pytest.fixture
def index_schema(project_root: Path) -> dict[str, Any]:
    """Load the index.json schema."""
    schema_path = project_root / "skills/transcript/test_data/schemas/index.schema.json"
    return json.loads(schema_path.read_text())


@pytest.fixture
def chunk_schema(project_root: Path) -> dict[str, Any]:
    """Load the chunk.json schema."""
    schema_path = project_root / "skills/transcript/test_data/schemas/chunk.schema.json"
    return json.loads(schema_path.read_text())


@pytest.fixture
def sample_segments() -> list[ParsedSegment]:
    """Create sample segments for testing."""
    segments = []
    for i in range(1, 21):  # 20 segments
        segments.append(
            ParsedSegment(
                id=str(i),
                start_ms=(i - 1) * 5000,
                end_ms=i * 5000,
                speaker=f"Speaker {(i % 3) + 1}",
                text=f"This is segment {i} content.",
                raw_text=f"<v Speaker {(i % 3) + 1}>This is segment {i} content.</v>",
            )
        )
    return segments


@pytest.fixture
def chunked_output(sample_segments: list[ParsedSegment], tmp_path: Path) -> Path:
    """Generate chunked output for validation."""
    chunker = TranscriptChunker(chunk_size=5)
    chunker.chunk(sample_segments, str(tmp_path))
    return tmp_path


# =============================================================================
# Index Schema Contract Tests
# =============================================================================


class TestIndexSchemaValidation:
    """Contract tests for index.json schema compliance."""

    @pytest.mark.skipif(not JSONSCHEMA_AVAILABLE, reason="jsonschema not installed")
    def test_index_validates_against_schema(
        self, chunked_output: Path, index_schema: dict[str, Any]
    ) -> None:
        """Index.json validates against index.schema.json.

        Contract: Generated index.json MUST conform to the formal schema.
        """
        # Load generated index
        index_path = chunked_output / "index.json"
        index_data = json.loads(index_path.read_text())

        # Validate against schema
        validator = Draft202012Validator(index_schema)
        errors = list(validator.iter_errors(index_data))

        assert len(errors) == 0, (
            f"Index.json schema validation failed with {len(errors)} errors:\n"
            + "\n".join(f"  - {e.message} at {e.json_path}" for e in errors)
        )

    def test_index_has_required_fields(self, chunked_output: Path) -> None:
        """Index.json contains all required fields.

        Contract: Per TDD-FEAT-004 Section 5, index.json MUST have:
        schema_version, total_segments, total_chunks, chunk_size, chunks
        """
        index_path = chunked_output / "index.json"
        index_data = json.loads(index_path.read_text())

        required_fields = [
            "schema_version",
            "total_segments",
            "total_chunks",
            "chunk_size",
            "chunks",
        ]

        for field in required_fields:
            assert field in index_data, f"Missing required field: {field}"

    def test_index_schema_version_is_1_0(self, chunked_output: Path) -> None:
        """Index.json schema_version is '1.0'.

        Contract: schema_version MUST be '1.0' for compatibility.
        """
        index_path = chunked_output / "index.json"
        index_data = json.loads(index_path.read_text())

        assert index_data["schema_version"] == "1.0", (
            f"schema_version must be '1.0', got: {index_data.get('schema_version')}"
        )

    def test_index_chunks_array_not_empty(self, chunked_output: Path) -> None:
        """Index.json chunks array has at least one entry.

        Contract: A valid index MUST have at least one chunk.
        """
        index_path = chunked_output / "index.json"
        index_data = json.loads(index_path.read_text())

        assert len(index_data["chunks"]) >= 1, "chunks array must not be empty"

    def test_index_chunk_pointers_have_required_fields(
        self, chunked_output: Path
    ) -> None:
        """Each chunk pointer has required fields.

        Contract: Per index.schema.json, each chunk pointer needs:
        chunk_id, segment_range, file
        """
        index_path = chunked_output / "index.json"
        index_data = json.loads(index_path.read_text())

        for chunk_ptr in index_data["chunks"]:
            assert "chunk_id" in chunk_ptr, "chunk pointer missing chunk_id"
            assert "segment_range" in chunk_ptr, "chunk pointer missing segment_range"
            assert "file" in chunk_ptr, "chunk pointer missing file"


# =============================================================================
# Chunk Schema Contract Tests
# =============================================================================


class TestChunkSchemaValidation:
    """Contract tests for chunk-NNN.json schema compliance."""

    @pytest.mark.skipif(not JSONSCHEMA_AVAILABLE, reason="jsonschema not installed")
    def test_all_chunks_validate_against_schema(
        self, chunked_output: Path, chunk_schema: dict[str, Any]
    ) -> None:
        """All chunk files validate against chunk.schema.json.

        Contract: Every generated chunk-NNN.json MUST conform to the schema.
        """
        chunks_dir = chunked_output / "chunks"
        validator = Draft202012Validator(chunk_schema)

        for chunk_file in sorted(chunks_dir.glob("chunk-*.json")):
            chunk_data = json.loads(chunk_file.read_text())
            errors = list(validator.iter_errors(chunk_data))

            assert len(errors) == 0, (
                f"{chunk_file.name} schema validation failed:\n"
                + "\n".join(f"  - {e.message}" for e in errors)
            )

    def test_chunk_has_required_fields(self, chunked_output: Path) -> None:
        """Chunk files contain all required fields.

        Contract: Per chunk.schema.json, each chunk MUST have:
        chunk_id, schema_version, segment_range, segments, navigation
        """
        chunks_dir = chunked_output / "chunks"
        required_fields = [
            "chunk_id",
            "schema_version",
            "segment_range",
            "segments",
            "navigation",
        ]

        for chunk_file in chunks_dir.glob("chunk-*.json"):
            chunk_data = json.loads(chunk_file.read_text())
            for field in required_fields:
                assert field in chunk_data, (
                    f"{chunk_file.name} missing required field: {field}"
                )

    def test_chunk_id_format_valid(self, chunked_output: Path) -> None:
        """Chunk IDs follow the pattern 'chunk-NNN'.

        Contract: chunk_id MUST match pattern ^chunk-\\d{3}$
        """
        import re

        chunks_dir = chunked_output / "chunks"
        pattern = re.compile(r"^chunk-\d{3}$")

        for chunk_file in chunks_dir.glob("chunk-*.json"):
            chunk_data = json.loads(chunk_file.read_text())
            chunk_id = chunk_data.get("chunk_id", "")

            assert pattern.match(chunk_id), (
                f"Invalid chunk_id format: {chunk_id} (expected chunk-NNN)"
            )

    def test_chunk_segment_range_valid(self, chunked_output: Path) -> None:
        """Segment range has valid start <= end.

        Contract: segment_range[0] MUST be <= segment_range[1]
        """
        chunks_dir = chunked_output / "chunks"

        for chunk_file in chunks_dir.glob("chunk-*.json"):
            chunk_data = json.loads(chunk_file.read_text())
            seg_range = chunk_data.get("segment_range", [0, 0])

            assert len(seg_range) == 2, f"{chunk_file.name}: segment_range needs 2 values"
            assert seg_range[0] <= seg_range[1], (
                f"{chunk_file.name}: segment_range start > end: {seg_range}"
            )

    def test_chunk_segments_not_empty(self, chunked_output: Path) -> None:
        """Chunk segments array is not empty.

        Contract: Each chunk MUST have at least one segment.
        """
        chunks_dir = chunked_output / "chunks"

        for chunk_file in chunks_dir.glob("chunk-*.json"):
            chunk_data = json.loads(chunk_file.read_text())
            segments = chunk_data.get("segments", [])

            assert len(segments) >= 1, f"{chunk_file.name} has no segments"


# =============================================================================
# Navigation Link Contract Tests
# =============================================================================


class TestNavigationLinksValidation:
    """Contract tests for chunk navigation links."""

    def test_navigation_has_index_link(self, chunked_output: Path) -> None:
        """All chunks have navigation.index link.

        Contract: Every chunk MUST link back to index.json.
        """
        chunks_dir = chunked_output / "chunks"

        for chunk_file in chunks_dir.glob("chunk-*.json"):
            chunk_data = json.loads(chunk_file.read_text())
            navigation = chunk_data.get("navigation", {})

            assert "index" in navigation, f"{chunk_file.name} missing navigation.index"
            assert navigation["index"] is not None, (
                f"{chunk_file.name} navigation.index is null"
            )

    def test_first_chunk_has_no_previous(self, chunked_output: Path) -> None:
        """First chunk has navigation.previous = null.

        Contract: chunk-001 MUST have previous: null.
        """
        chunk_file = chunked_output / "chunks" / "chunk-001.json"
        chunk_data = json.loads(chunk_file.read_text())
        navigation = chunk_data.get("navigation", {})

        assert navigation.get("previous") is None, (
            f"First chunk should have previous: null, got: {navigation.get('previous')}"
        )

    def test_last_chunk_has_no_next(self, chunked_output: Path) -> None:
        """Last chunk has navigation.next = null.

        Contract: Final chunk MUST have next: null.
        """
        chunks_dir = chunked_output / "chunks"
        chunk_files = sorted(chunks_dir.glob("chunk-*.json"))
        last_chunk = chunk_files[-1]

        chunk_data = json.loads(last_chunk.read_text())
        navigation = chunk_data.get("navigation", {})

        assert navigation.get("next") is None, (
            f"Last chunk should have next: null, got: {navigation.get('next')}"
        )


# =============================================================================
# Negative Contract Tests (Invalid JSON Detection)
# =============================================================================


class TestInvalidJsonDetection:
    """Contract tests for invalid JSON detection."""

    @pytest.mark.skipif(not JSONSCHEMA_AVAILABLE, reason="jsonschema not installed")
    def test_missing_required_field_detected(
        self, index_schema: dict[str, Any]
    ) -> None:
        """Missing required field produces validation error.

        Contract: Index without schema_version MUST fail validation.
        """
        invalid_index = {
            # Missing schema_version
            "total_segments": 10,
            "total_chunks": 1,
            "chunk_size": 500,
            "chunks": [{"chunk_id": "chunk-001", "segment_range": [1, 10], "file": "chunks/chunk-001.json"}],
        }

        validator = Draft202012Validator(index_schema)
        errors = list(validator.iter_errors(invalid_index))

        assert len(errors) > 0, "Expected validation error for missing schema_version"

    @pytest.mark.skipif(not JSONSCHEMA_AVAILABLE, reason="jsonschema not installed")
    def test_invalid_schema_version_detected(
        self, index_schema: dict[str, Any]
    ) -> None:
        """Invalid schema_version produces validation error.

        Contract: schema_version other than '1.0' MUST fail validation.
        """
        invalid_index = {
            "schema_version": "2.0",  # Invalid version
            "total_segments": 10,
            "total_chunks": 1,
            "chunk_size": 500,
            "chunks": [{"chunk_id": "chunk-001", "segment_range": [1, 10], "file": "chunks/chunk-001.json"}],
        }

        validator = Draft202012Validator(index_schema)
        errors = list(validator.iter_errors(invalid_index))

        assert len(errors) > 0, "Expected validation error for invalid schema_version"

    @pytest.mark.skipif(not JSONSCHEMA_AVAILABLE, reason="jsonschema not installed")
    def test_invalid_chunk_id_format_detected(
        self, chunk_schema: dict[str, Any]
    ) -> None:
        """Invalid chunk_id format produces validation error.

        Contract: chunk_id not matching ^chunk-\\d{3}$ MUST fail.
        """
        invalid_chunk = {
            "chunk_id": "chunk-1",  # Invalid format (should be chunk-001)
            "schema_version": "1.0",
            "segment_range": [1, 10],
            "segments": [{"id": "1", "text": "test"}],
            "navigation": {"index": "../index.json"},
        }

        validator = Draft202012Validator(chunk_schema)
        errors = list(validator.iter_errors(invalid_chunk))

        assert len(errors) > 0, "Expected validation error for invalid chunk_id format"


# =============================================================================
# Integration Test with Golden Dataset
# =============================================================================


class TestMeeting006Integration:
    """Integration test with meeting-006-all-hands.vtt."""

    @pytest.mark.skipif(not JSONSCHEMA_AVAILABLE, reason="jsonschema not installed")
    def test_meeting_006_produces_valid_output(
        self,
        project_root: Path,
        index_schema: dict[str, Any],
        chunk_schema: dict[str, Any],
        tmp_path: Path,
    ) -> None:
        """meeting-006-all-hands.vtt produces schema-compliant output.

        Contract: Real golden dataset MUST produce valid chunked output.
        """
        # Import parser to get segments
        from src.transcript.infrastructure.adapters.vtt_parser import VTTParser

        # Parse meeting-006
        vtt_path = (
            project_root
            / "skills/transcript/test_data/transcripts/golden/meeting-006-all-hands.vtt"
        )

        if not vtt_path.exists():
            pytest.skip(f"Golden dataset not found: {vtt_path}")

        parser = VTTParser()
        result = parser.parse(str(vtt_path))

        # Chunk the result
        chunker = TranscriptChunker(chunk_size=500)
        chunker.chunk(result.segments, str(tmp_path))

        # Validate index
        index_path = tmp_path / "index.json"
        index_data = json.loads(index_path.read_text())

        index_validator = Draft202012Validator(index_schema)
        index_errors = list(index_validator.iter_errors(index_data))
        assert len(index_errors) == 0, (
            f"Index validation failed: {[e.message for e in index_errors]}"
        )

        # Validate all chunks
        chunk_validator = Draft202012Validator(chunk_schema)
        chunks_dir = tmp_path / "chunks"

        for chunk_file in chunks_dir.glob("chunk-*.json"):
            chunk_data = json.loads(chunk_file.read_text())
            errors = list(chunk_validator.iter_errors(chunk_data))
            assert len(errors) == 0, (
                f"{chunk_file.name} validation failed: {[e.message for e in errors]}"
            )

        # Verify expected chunk count
        # 3071 segments / 500 = 7 chunks (6 full + 1 remainder)
        expected_chunks = (len(result.segments) + 499) // 500  # ceiling division
        assert index_data["total_chunks"] == expected_chunks


# =============================================================================
# Cross-Reference Contract Tests (TASK-232 AC-3)
# =============================================================================


class TestIndexChunkCrossReferences:
    """Contract tests for cross-reference integrity between index and chunks.

    TASK-232 AC-3: Cross-references between index and chunks are consistent.
    """

    def test_index_chunk_cross_references(self, chunked_output: Path) -> None:
        """Verify index chunk references match actual chunk files.

        Contract: Every chunk pointer in index MUST reference an existing file.
        """
        index_path = chunked_output / "index.json"
        index_data = json.loads(index_path.read_text())

        chunks_dir = chunked_output / "chunks"
        actual_chunks = set(p.name for p in chunks_dir.glob("chunk-*.json"))
        index_chunks = set(
            Path(c["file"]).name for c in index_data["chunks"]
        )

        assert actual_chunks == index_chunks, (
            f"Index and filesystem chunks mismatch:\n"
            f"  In index but not filesystem: {index_chunks - actual_chunks}\n"
            f"  In filesystem but not index: {actual_chunks - index_chunks}"
        )

    def test_chunk_count_matches_index(self, chunked_output: Path) -> None:
        """Verify total_chunks matches actual chunk file count.

        Contract: index.total_chunks MUST equal number of chunk files.
        """
        index_path = chunked_output / "index.json"
        index_data = json.loads(index_path.read_text())

        chunks_dir = chunked_output / "chunks"
        actual_count = len(list(chunks_dir.glob("chunk-*.json")))

        assert index_data["total_chunks"] == actual_count, (
            f"total_chunks ({index_data['total_chunks']}) != "
            f"actual file count ({actual_count})"
        )


# =============================================================================
# Segment Range Contract Tests (TASK-232 AC-4)
# =============================================================================


class TestSegmentRangeIntegrity:
    """Contract tests for segment range integrity across chunks.

    TASK-232 AC-4: Segment ID ranges are non-overlapping and complete.
    """

    def test_segment_ranges_non_overlapping(self, chunked_output: Path) -> None:
        """Verify segment ID ranges don't overlap between chunks.

        Contract: No segment ID should appear in multiple chunks.
        """
        index_path = chunked_output / "index.json"
        index_data = json.loads(index_path.read_text())

        all_ranges = []
        for chunk_meta in index_data["chunks"]:
            seg_range = chunk_meta["segment_range"]
            all_ranges.append((seg_range[0], seg_range[1], chunk_meta["chunk_id"]))

        # Sort by start and check no overlaps
        all_ranges.sort()
        for i in range(len(all_ranges) - 1):
            current_end = all_ranges[i][1]
            next_start = all_ranges[i + 1][0]
            current_id = all_ranges[i][2]
            next_id = all_ranges[i + 1][2]

            assert next_start > current_end, (
                f"Overlapping ranges: {current_id} ends at {current_end}, "
                f"{next_id} starts at {next_start}"
            )

    def test_segment_ranges_complete_coverage(self, chunked_output: Path) -> None:
        """Verify segment ranges cover all segments without gaps.

        Contract: Segment IDs 1..total_segments MUST all be covered.
        """
        index_path = chunked_output / "index.json"
        index_data = json.loads(index_path.read_text())

        total_segments = index_data["total_segments"]

        # Verify first chunk starts at 1
        first_range = index_data["chunks"][0]["segment_range"]
        assert first_range[0] == 1, (
            f"First chunk should start at segment 1, got: {first_range[0]}"
        )

        # Verify last chunk ends at total_segments
        last_range = index_data["chunks"][-1]["segment_range"]
        assert last_range[1] == total_segments, (
            f"Last chunk should end at segment {total_segments}, "
            f"got: {last_range[1]}"
        )

        # Verify no gaps between consecutive chunks
        all_ranges = sorted(c["segment_range"] for c in index_data["chunks"])
        for i in range(len(all_ranges) - 1):
            current_end = all_ranges[i][1]
            next_start = all_ranges[i + 1][0]
            assert next_start == current_end + 1, (
                f"Gap in segment coverage: chunk ending at {current_end}, "
                f"next starts at {next_start}"
            )

    def test_segment_count_matches_range(self, chunked_output: Path) -> None:
        """Verify segment_count matches segment_range span in each chunk.

        Contract: For each chunk, segment_count == end - start + 1.
        """
        chunks_dir = chunked_output / "chunks"

        for chunk_file in chunks_dir.glob("chunk-*.json"):
            chunk_data = json.loads(chunk_file.read_text())
            seg_range = chunk_data["segment_range"]
            actual_count = len(chunk_data["segments"])
            expected_count = seg_range[1] - seg_range[0] + 1

            assert actual_count == expected_count, (
                f"{chunk_file.name}: segment count ({actual_count}) != "
                f"range span ({expected_count}) for range {seg_range}"
            )
