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
        segments: List of parsed transcript segments
        format: Source format identifier (vtt, srt, txt)
        encoding: Detected/used encoding
        duration_ms: Total transcript duration in milliseconds
        warnings: List of non-fatal issues encountered
        errors: List of fatal errors (parse_status will be 'failed')
        parse_status: Status indicator (complete, partial, failed)

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
