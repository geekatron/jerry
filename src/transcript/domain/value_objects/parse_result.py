"""
ParseResult Value Object.

Result from transcript parsing operations.
Reference: TDD-FEAT-004-hybrid-infrastructure.md v1.2.0, Section 4

Location: src/transcript/domain/value_objects/parse_result.py
"""

from dataclasses import dataclass, field
from typing import List, Optional

from src.transcript.domain.value_objects.parsed_segment import ParsedSegment


@dataclass(frozen=True)
class ParseResult:
    """Result from VTT/SRT parsing operation.

    Attributes:
        segments: List of parsed transcript segments.
        format: Source format identifier. Valid values: "vtt", "srt", "txt".
        encoding: Detected/used encoding (e.g., "utf-8", "utf-8-sig", "windows-1252").
        duration_ms: Total transcript duration in milliseconds. None if no segments.
        warnings: List of non-fatal issues. Each warning is a dict with "type" and "message".
        errors: List of fatal errors. Each error is a dict with "type" and "message".
            See Error Types below for valid type values.
        parse_status: Status indicator. Valid values:
            - "complete": All content parsed successfully
            - "partial": Some content parsed, but errors occurred
            - "failed": No content could be parsed

    Error Types:
        Each error dict has the structure: {"type": <string>, "message": <string>}

        Valid error type values:
        - "encoding_error": File could not be decoded with any supported encoding.
            Supported encodings: utf-8-sig, utf-8, windows-1252, iso-8859-1, latin-1.
            Example: Binary file, corrupted content, unsupported encoding.

        - "format_error": Content does not conform to expected transcript format.
            Example: Missing WEBVTT header, invalid VTT structure, empty file.

        - "timestamp_error": Timestamp in transcript could not be parsed.
            Expected formats: "HH:MM:SS.mmm" or "MM:SS.mmm".
            Example: "invalid:timestamp", "25:61:00.000" (invalid values).

        - "parse_error": Generic parsing failure not covered by specific types.
            Used as fallback for unexpected errors from underlying parser.

    Example - Successful parse:
        >>> result.parse_status
        "complete"
        >>> result.errors
        []
        >>> result.segment_count
        3071

    Example - Failed parse:
        >>> result.parse_status
        "failed"
        >>> result.errors
        [{"type": "format_error", "message": "Missing WEBVTT header"}]
        >>> result.segment_count
        0

    Reference: TDD-FEAT-004 v1.2.0, Section 4
    """

    segments: List[ParsedSegment] = field(default_factory=list)
    format: str = "vtt"
    encoding: str = "utf-8"
    duration_ms: Optional[int] = None
    warnings: List[dict] = field(default_factory=list)
    errors: List[dict] = field(default_factory=list)
    parse_status: str = "complete"

    @property
    def segment_count(self) -> int:
        """Return the number of segments."""
        return len(self.segments)

    @property
    def speaker_count(self) -> int:
        """Return the number of unique speakers."""
        speakers = {
            s.speaker for s in self.segments if s.speaker is not None
        }
        return len(speakers)

    @property
    def speakers(self) -> List[str]:
        """Return sorted list of unique speakers."""
        speakers = {
            s.speaker for s in self.segments if s.speaker is not None
        }
        return sorted(speakers)

    @property
    def is_successful(self) -> bool:
        """Check if parsing completed without fatal errors."""
        return self.parse_status in ("complete", "partial")

    @property
    def has_warnings(self) -> bool:
        """Check if there are any warnings."""
        return len(self.warnings) > 0
