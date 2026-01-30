"""
VTTParser - WebVTT Format Parser.

Implements deterministic VTT transcript parsing using webvtt-py.
Reference: TDD-FEAT-004-hybrid-infrastructure.md v1.2.0, Section 4

Location: src/transcript/infrastructure/adapters/vtt_parser.py
Dependencies: webvtt-py, charset-normalizer (optional-dependency: transcript)
"""

import re
from io import StringIO
from pathlib import Path

from src.transcript.domain.value_objects.parse_result import ParseResult
from src.transcript.domain.value_objects.parsed_segment import ParsedSegment


class VTTParser:
    """WebVTT format parser using webvtt-py.

    Parses VTT transcript files and extracts:
    - Timestamped segments
    - Speaker identification from voice tags
    - Clean text with voice tags removed
    - Duration and metadata

    Reference: TDD-FEAT-004 v1.2.0, Section 4
    """

    # Pre-compiled regex pattern for voice tag extraction (fallback)
    VOICE_TAG_PATTERN = re.compile(r"<v\s+([^>]+)>")

    # Encoding fallback chain per TDD-FEAT-004
    ENCODING_FALLBACK = ["utf-8-sig", "utf-8", "windows-1252", "iso-8859-1", "latin-1"]

    def parse(self, file_path: str) -> ParseResult:
        """Parse a VTT file to canonical format.

        Args:
            file_path: Path to the VTT transcript file

        Returns:
            ParseResult containing segments and metadata

        Raises:
            FileNotFoundError: If file does not exist
            PermissionError: If file cannot be read
            ValueError: If file format is invalid
        """
        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(f"VTT file not found: {file_path}")

        # Read file with encoding detection
        content, encoding = self._read_file_with_encoding(path)

        result = self.parse_content(content)

        # Update encoding in result (create new immutable object)
        return ParseResult(
            segments=result.segments,
            format=result.format,
            encoding=encoding,
            duration_ms=result.duration_ms,
            warnings=result.warnings,
            errors=result.errors,
            parse_status=result.parse_status,
        )

    def parse_content(self, content: str) -> ParseResult:
        """Parse VTT content from string.

        Args:
            content: Raw VTT content as string

        Returns:
            ParseResult containing segments and metadata

        Raises:
            ValueError: If content format is invalid
        """
        try:
            import webvtt
        except ImportError as e:
            raise ImportError(
                "webvtt-py is required for VTT parsing. Install with: pip install webvtt-py"
            ) from e

        segments: list[ParsedSegment] = []
        warnings: list[dict] = []

        try:
            # webvtt.from_buffer parses VTT content
            captions = webvtt.from_buffer(StringIO(content))

            for i, caption in enumerate(captions, start=1):  # type: ignore[arg-type]
                # webvtt-py provides voice attribute and raw_text
                raw_text = caption.raw_text
                speaker = getattr(caption, "voice", None) or self._extract_speaker(raw_text)
                text = caption.text  # Already cleaned by webvtt-py

                segments.append(
                    ParsedSegment(
                        id=str(i),
                        start_ms=self._timestamp_to_ms(caption.start),
                        end_ms=self._timestamp_to_ms(caption.end),
                        speaker=speaker,
                        text=text,
                        raw_text=raw_text,
                    )
                )

        except Exception as e:
            # Classify error type based on exception message and content
            error_type = self._classify_error(e, content)

            # Return partial result with error
            return ParseResult(
                segments=segments,
                format="vtt",
                warnings=warnings,
                errors=[{"type": error_type, "message": str(e)}],
                parse_status="failed" if not segments else "partial",
            )

        # Calculate duration from last segment
        duration_ms = segments[-1].end_ms if segments else None

        return ParseResult(
            segments=segments,
            format="vtt",
            duration_ms=duration_ms,
            warnings=warnings,
            parse_status="complete",
        )

    def _classify_error(self, error: Exception, content: str) -> str:
        """Classify error type based on exception and content.

        Error Types (per ParseResult docstring contract):
        - "format_error": Missing WEBVTT header, invalid VTT structure, empty file
        - "timestamp_error": Invalid timestamp format
        - "encoding_error": Decoding failures (handled in _read_file_with_encoding)
        - "parse_error": Generic fallback for unexpected errors

        Args:
            error: The exception that occurred during parsing
            content: The content that was being parsed

        Returns:
            Error type string matching ParseResult error type contract
        """
        error_msg = str(error).lower()

        # Check for format errors (missing WEBVTT header, invalid structure)
        format_indicators = [
            "webvtt",
            "header",
            "malformed",
            "invalid",
            "expected",
            "file",
        ]
        if any(indicator in error_msg for indicator in format_indicators):
            return "format_error"

        # Check for empty content (format error)
        if not content or not content.strip():
            return "format_error"

        # Check if content lacks WEBVTT header (format error)
        if not content.strip().startswith("WEBVTT"):
            return "format_error"

        # Check for timestamp errors
        timestamp_indicators = ["timestamp", "time", "-->"]
        if any(indicator in error_msg for indicator in timestamp_indicators):
            return "timestamp_error"

        # Default to generic parse_error
        return "parse_error"

    def _extract_speaker(self, text: str) -> str | None:
        """Extract speaker from VTT voice tag.

        Handles format: <v Speaker Name>text</v>
        Uses pre-compiled VOICE_TAG_PATTERN for performance.

        Note: This is a fallback for when webvtt-py's voice attribute
        is not available. webvtt-py handles most voice tag extraction.

        Args:
            text: Raw caption text potentially containing voice tags

        Returns:
            Speaker name if found, None otherwise
        """
        match = self.VOICE_TAG_PATTERN.match(text)
        return match.group(1).strip() if match else None

    def _timestamp_to_ms(self, timestamp: str) -> int:
        """Convert VTT timestamp to milliseconds.

        Args:
            timestamp: VTT timestamp format (HH:MM:SS.mmm or MM:SS.mmm)

        Returns:
            Time in milliseconds
        """
        # Handle both HH:MM:SS.mmm and MM:SS.mmm formats
        parts = timestamp.replace(",", ".").split(":")

        if len(parts) == 3:
            hours = int(parts[0])
            minutes = int(parts[1])
            sec_parts = parts[2].split(".")
        elif len(parts) == 2:
            hours = 0
            minutes = int(parts[0])
            sec_parts = parts[1].split(".")
        else:
            raise ValueError(f"Invalid timestamp format: {timestamp}")

        seconds = int(sec_parts[0])
        milliseconds = int(sec_parts[1]) if len(sec_parts) > 1 else 0

        return (hours * 3600 + minutes * 60 + seconds) * 1000 + milliseconds

    def _read_file_with_encoding(self, path: Path) -> tuple[str, str]:
        """Read file with encoding detection fallback.

        Args:
            path: Path to the file

        Returns:
            Tuple of (content, encoding_used)

        Raises:
            ValueError: If file cannot be decoded with any encoding
        """
        for encoding in self.ENCODING_FALLBACK:
            try:
                content = path.read_text(encoding=encoding)
                return content, encoding
            except UnicodeDecodeError:
                continue

        raise ValueError(f"Unable to decode file with any encoding: {self.ENCODING_FALLBACK}")
