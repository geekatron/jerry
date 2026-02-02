"""
ITranscriptParser Port Interface.

Domain port for transcript parsing operations.
Reference: TDD-FEAT-004-hybrid-infrastructure.md v1.2.0, Section 4

Location: src/transcript/domain/ports/transcript_parser.py
"""

from typing import Protocol

from src.transcript.domain.value_objects.parse_result import ParseResult


class ITranscriptParser(Protocol):
    """Port interface for transcript parsing.

    Implementations:
        - VTTParser: WebVTT format (src/transcript/infrastructure/adapters/vtt_parser.py)
        - SRTParser: SubRip format (Phase 2, DEC-011 D-002)
        - PlainTextParser: Plain text (Phase 3)

    Reference: TDD-FEAT-004 v1.2.0, Section 4
    """

    def parse(self, file_path: str) -> ParseResult:
        """Parse a transcript file to canonical format.

        Args:
            file_path: Path to the transcript file

        Returns:
            ParseResult containing segments and metadata

        Raises:
            FileNotFoundError: If file does not exist
            PermissionError: If file cannot be read
            ValueError: If file format is invalid
        """
        ...

    def parse_content(self, content: str) -> ParseResult:
        """Parse transcript content from string.

        Args:
            content: Raw transcript content as string

        Returns:
            ParseResult containing segments and metadata

        Raises:
            ValueError: If content format is invalid
        """
        ...
