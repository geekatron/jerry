"""
ParsedSegment Value Object.

Canonical segment representation for transcript parsing.
Reference: TDD-FEAT-004-hybrid-infrastructure.md v1.2.0, Section 4

Location: src/transcript/domain/value_objects/parsed_segment.py
"""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ParsedSegment:
    """Canonical segment representation (Value Object).

    Attributes:
        id: String ID for cross-reference compatibility
        start_ms: Start time in milliseconds
        end_ms: End time in milliseconds
        speaker: Speaker name from voice tag (if present)
        text: Cleaned text content (voice tags removed)
        raw_text: Original text with voice tags preserved

    Invariants:
        - id must not be empty
        - start_ms must be >= 0
        - end_ms must be >= start_ms
        - text must not be None (use empty string for empty segments)

    Reference: TDD-FEAT-004 v1.2.0, Section 4
    """

    id: str
    start_ms: int
    end_ms: int
    speaker: str | None
    text: str
    raw_text: str

    def __post_init__(self) -> None:
        """Validate invariants after initialization."""
        if not self.id:
            raise ValueError("Segment id must not be empty")
        if self.start_ms < 0:
            raise ValueError(f"start_ms must be >= 0, got {self.start_ms}")
        if self.end_ms < self.start_ms:
            raise ValueError(f"end_ms ({self.end_ms}) must be >= start_ms ({self.start_ms})")

    @property
    def duration_ms(self) -> int:
        """Calculate segment duration in milliseconds."""
        return self.end_ms - self.start_ms

    @property
    def has_speaker(self) -> bool:
        """Check if segment has an identified speaker."""
        return self.speaker is not None and len(self.speaker.strip()) > 0
