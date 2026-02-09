#!/usr/bin/env python3
"""
VTT Compliance Validator - Validates VTT files against W3C WebVTT specification.

Source: FEAT-002:DISC-007 VTT Generation Validation Gap
Reference: W3C WebVTT Specification (https://www.w3.org/TR/webvtt1/)

Usage:
    python validate_vtt.py <file.vtt>
    python validate_vtt.py --dir <directory>
    python validate_vtt.py --all  # Validate all golden VTT files

Exit Codes:
    0 - All files valid
    1 - Validation errors found
    2 - Invalid arguments
"""

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path


@dataclass
class ValidationIssue:
    """A validation issue found in a VTT file."""

    line_num: int
    code: str
    message: str
    severity: str = "error"  # error, warning


@dataclass
class ValidationResult:
    """Result of validating a VTT file."""

    file_path: Path
    valid: bool
    issues: list[ValidationIssue]
    cue_count: int
    duration_str: str


def parse_timestamp_to_ms(ts: str) -> int | None:
    """Parse VTT timestamp to milliseconds. Returns None if invalid."""
    # Format: [HH:]MM:SS.mmm
    patterns = [
        r"^(\d{2,}):(\d{2}):(\d{2})\.(\d{3})$",  # HH:MM:SS.mmm
        r"^(\d{2}):(\d{2})\.(\d{3})$",  # MM:SS.mmm (hours optional)
    ]

    for pattern in patterns:
        match = re.match(pattern, ts)
        if match:
            groups = match.groups()
            if len(groups) == 4:
                h, m, s, ms = map(int, groups)
            else:
                h = 0
                m, s, ms = map(int, groups)
            return (h * 3600 + m * 60 + s) * 1000 + ms

    return None


def validate_vtt(file_path: Path) -> ValidationResult:
    """Validate a VTT file against W3C WebVTT specification."""
    issues: list[ValidationIssue] = []
    cue_count = 0
    last_start_ms = -1
    last_timestamp_str = ""

    try:
        content = file_path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        # Try with fallback encoding
        try:
            content = file_path.read_text(encoding="windows-1252")
            issues.append(
                ValidationIssue(
                    line_num=0,
                    code="WARN-001",
                    message="File uses Windows-1252 encoding, not UTF-8",
                    severity="warning",
                )
            )
        except Exception as e:
            return ValidationResult(
                file_path=file_path,
                valid=False,
                issues=[
                    ValidationIssue(
                        line_num=0,
                        code="ERR-001",
                        message=f"Cannot read file: {e}",
                    )
                ],
                cue_count=0,
                duration_str="N/A",
            )

    lines = content.splitlines()

    # Check 1: WEBVTT header
    if not lines or not lines[0].startswith("WEBVTT"):
        issues.append(
            ValidationIssue(
                line_num=1,
                code="ERR-002",
                message="File must start with 'WEBVTT'",
            )
        )

    # Timestamp line pattern
    timestamp_line_pattern = re.compile(
        r"^(\d{2,}:\d{2}:\d{2}\.\d{3})\s+-->\s+(\d{2,}:\d{2}:\d{2}\.\d{3})(.*)$"
    )

    for i, line in enumerate(lines, start=1):
        stripped = line.strip()

        # Check for timestamp lines
        match = timestamp_line_pattern.match(stripped)
        if match:
            cue_count += 1
            start_ts, end_ts, _settings = match.groups()

            # Get seconds from the SS.mmm part
            start_secs_val = int(start_ts.split(":")[-1].split(".")[0])
            end_secs_val = int(end_ts.split(":")[-1].split(".")[0])

            if start_secs_val >= 60:
                issues.append(
                    ValidationIssue(
                        line_num=i,
                        code="ERR-003",
                        message=f"Start timestamp seconds >= 60: {start_ts}",
                    )
                )

            if end_secs_val >= 60:
                issues.append(
                    ValidationIssue(
                        line_num=i,
                        code="ERR-004",
                        message=f"End timestamp seconds >= 60: {end_ts}",
                    )
                )

            # Parse timestamps
            start_ms = parse_timestamp_to_ms(start_ts)
            end_ms = parse_timestamp_to_ms(end_ts)

            if start_ms is None:
                issues.append(
                    ValidationIssue(
                        line_num=i,
                        code="ERR-005",
                        message=f"Invalid start timestamp format: {start_ts}",
                    )
                )
            elif end_ms is None:
                issues.append(
                    ValidationIssue(
                        line_num=i,
                        code="ERR-006",
                        message=f"Invalid end timestamp format: {end_ts}",
                    )
                )
            else:
                # Check 3: End > Start
                if end_ms <= start_ms:
                    issues.append(
                        ValidationIssue(
                            line_num=i,
                            code="ERR-007",
                            message=f"End timestamp not after start: {start_ts} --> {end_ts}",
                        )
                    )

                # Check 4: Monotonic ordering
                if start_ms < last_start_ms:
                    issues.append(
                        ValidationIssue(
                            line_num=i,
                            code="ERR-008",
                            message=f"Non-monotonic: {start_ts} < previous cue {last_timestamp_str}",
                        )
                    )

                last_start_ms = start_ms
                last_timestamp_str = start_ts

    # Determine duration
    if last_timestamp_str:
        duration_str = last_timestamp_str
    else:
        duration_str = "N/A"

    # Filter for errors only (warnings don't invalidate)
    errors = [issue for issue in issues if issue.severity == "error"]
    valid = len(errors) == 0

    return ValidationResult(
        file_path=file_path,
        valid=valid,
        issues=issues,
        cue_count=cue_count,
        duration_str=duration_str,
    )


def print_result(result: ValidationResult, verbose: bool = True) -> None:
    """Print validation result."""
    status_symbol = "\u2713" if result.valid else "\u2717"

    print(
        f"{status_symbol} {result.file_path.name}: {result.cue_count} cues, duration ~{result.duration_str}"
    )

    if result.issues:
        errors = [i for i in result.issues if i.severity == "error"]
        warnings = [i for i in result.issues if i.severity == "warning"]

        if errors:
            print(f"  Errors: {len(errors)}")
            if verbose:
                for issue in errors[:10]:
                    print(f"    Line {issue.line_num}: [{issue.code}] {issue.message}")
                if len(errors) > 10:
                    print(f"    ... and {len(errors) - 10} more errors")

        if warnings:
            print(f"  Warnings: {len(warnings)}")
            if verbose:
                for issue in warnings[:5]:
                    print(f"    Line {issue.line_num}: [{issue.code}] {issue.message}")


def main() -> int:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Validate VTT files against W3C WebVTT specification"
    )
    parser.add_argument("file", nargs="?", help="VTT file to validate")
    parser.add_argument("--dir", help="Directory containing VTT files")
    parser.add_argument(
        "--all",
        action="store_true",
        help="Validate all golden VTT files",
    )
    parser.add_argument("-q", "--quiet", action="store_true", help="Only show failures")

    args = parser.parse_args()

    # Determine files to validate
    files: list[Path] = []

    if args.all:
        # Find golden VTT files relative to script location
        script_dir = Path(__file__).parent
        golden_dir = script_dir.parent / "test_data" / "transcripts" / "golden"
        if golden_dir.exists():
            files = list(golden_dir.glob("*.vtt"))
        else:
            # Try from current directory
            golden_dir = Path("skills/transcript/test_data/transcripts/golden")
            if golden_dir.exists():
                files = list(golden_dir.glob("*.vtt"))

    elif args.dir:
        dir_path = Path(args.dir)
        if not dir_path.is_dir():
            print(f"Error: {args.dir} is not a directory", file=sys.stderr)
            return 2
        files = list(dir_path.glob("*.vtt"))

    elif args.file:
        file_path = Path(args.file)
        if not file_path.exists():
            print(f"Error: {args.file} not found", file=sys.stderr)
            return 2
        files = [file_path]

    else:
        parser.print_help()
        return 2

    if not files:
        print("No VTT files found to validate")
        return 2

    # Validate files
    all_valid = True
    results: list[ValidationResult] = []

    for file_path in sorted(files):
        result = validate_vtt(file_path)
        results.append(result)
        if not result.valid:
            all_valid = False

    # Print results
    print("\nVTT Compliance Validation")
    print("=" * 50)
    print(f"Files: {len(files)}")
    print()

    for result in results:
        if not args.quiet or not result.valid:
            print_result(result, verbose=not args.quiet)

    # Summary
    print()
    passed = sum(1 for r in results if r.valid)
    failed = len(results) - passed
    print(f"Summary: {passed}/{len(results)} passed, {failed} failed")

    return 0 if all_valid else 1


if __name__ == "__main__":
    sys.exit(main())
