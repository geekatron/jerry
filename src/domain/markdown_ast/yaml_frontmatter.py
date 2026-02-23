# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
YamlFrontmatter - YAML frontmatter extraction from ``---`` delimited blocks.

Extracts YAML frontmatter from markdown files that use the standard ``---``
delimiter pattern (agent definitions, SKILL.md files). Uses ``yaml.safe_load()``
ONLY -- no other YAML loading function is permitted.

Security constraints:
    - MUST use ``yaml.safe_load()`` exclusively (M-01, T-YF-07 CWE-502)
    - Pre-parse block size check (M-07)
    - Post-parse result size verification (M-20, closes temporal gap)
    - Post-parse depth/key validation (M-06, M-16)
    - Duplicate key detection (M-23)
    - First-pair-only extraction (M-24)
    - Sanitized error messages (M-19, T-YF-04 CWE-209)
    - Control character stripping (M-18)
    - Value length enforcement (M-17)

References:
    - ADR-PROJ005-003 Design Decision 1 (Polymorphic Parser Pattern)
    - ADR-PROJ005-003 Design Decision 10 (YAML Type Normalization)
    - Threat Model: M-01, M-04a, M-06, M-07, M-16-M-20, M-23, M-24
    - H-07: Domain layer constraint (no external infra/interface imports)
    - H-10: Supporting frozen dataclasses (YamlFrontmatterField,
      YamlFrontmatterResult) are co-located with primary class per ADR.

Exports:
    YamlFrontmatterField: Frozen dataclass for a single YAML field.
    YamlFrontmatterResult: Frozen dataclass for the extraction result.
    YamlFrontmatter: Extractor class with static ``extract()`` method.
"""

from __future__ import annotations

import json
import re
from collections import Counter
from dataclasses import dataclass

import yaml
from yaml.constructor import ConstructorError
from yaml.parser import ParserError
from yaml.scanner import ScannerError

from src.domain.markdown_ast.input_bounds import InputBounds
from src.domain.markdown_ast.jerry_document import JerryDocument

# ---------------------------------------------------------------------------
# Control character pattern (M-18)
# Strips null bytes and non-printable control characters except \n, \r, \t
# ---------------------------------------------------------------------------
_CONTROL_CHAR_RE = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]")

# ---------------------------------------------------------------------------
# YAML block extraction pattern (M-24: first-pair-only)
# Matches the first --- ... --- pair at the start of the document
# ---------------------------------------------------------------------------
_YAML_BLOCK_RE = re.compile(
    r"\A---[ \t]*\n(?P<yaml>.*?\n)---[ \t]*(?:\n|\Z)",
    re.DOTALL,
)

# ---------------------------------------------------------------------------
# Alias reference pattern for pre-parse counting (M-20)
# ---------------------------------------------------------------------------
_ALIAS_RE = re.compile(r"\*[a-zA-Z_][a-zA-Z0-9_]*")


@dataclass(frozen=True)
class YamlFrontmatterField:
    """Single field from YAML frontmatter.

    Attributes:
        key: The field name.
        value: The original typed value from ``yaml.safe_load()``.
        value_type: String representation of the Python type
            (``"str"``, ``"int"``, ``"float"``, ``"bool"``, ``"list"``,
            ``"dict"``, ``"null"``).
    """

    key: str
    value: str | int | float | bool | list | dict | None  # noqa: UP007
    value_type: str


@dataclass(frozen=True)
class YamlFrontmatterResult:
    """Complete YAML frontmatter extraction result.

    Attributes:
        fields: Extracted fields as a tuple (immutable).
        raw_yaml: The raw YAML text between ``---`` delimiters.
        start_line: Zero-based line of the opening ``---``.
        end_line: Zero-based line of the closing ``---``.
        parse_error: ``None`` if parsing succeeded; error message otherwise.
        parse_warnings: Warnings (e.g., duplicate key detection).
    """

    fields: tuple[YamlFrontmatterField, ...]
    raw_yaml: str
    start_line: int
    end_line: int
    parse_error: str | None
    parse_warnings: tuple[str, ...] = ()


def _normalize_value(value: object) -> tuple[str, str]:
    """Normalize a YAML value to its canonical string representation (DD-10).

    Args:
        value: A value produced by ``yaml.safe_load()``.

    Returns:
        Tuple of (normalized_string, type_string).
    """
    if value is None:
        return ("null", "null")
    if isinstance(value, bool):
        return ("true" if value else "false", "bool")
    if isinstance(value, int):
        return (str(value), "int")
    if isinstance(value, float):
        return (str(value), "float")
    if isinstance(value, list):
        return (", ".join(str(item) for item in value), "list")
    if isinstance(value, dict):
        return (str(value), "dict")
    return (str(value), "str")


def _check_nesting_depth(obj: object, max_depth: int, current: int = 0) -> bool:
    """Check if a parsed YAML structure exceeds the maximum nesting depth.

    Args:
        obj: The parsed YAML object.
        max_depth: Maximum allowed depth.
        current: Current recursion depth.

    Returns:
        ``True`` if the depth is within bounds, ``False`` otherwise.
    """
    if current > max_depth:
        return False
    if isinstance(obj, dict):
        return all(_check_nesting_depth(v, max_depth, current + 1) for v in obj.values())
    if isinstance(obj, list):
        return all(_check_nesting_depth(item, max_depth, current + 1) for item in obj)
    return True


def _detect_duplicate_keys(raw_yaml: str) -> tuple[str, ...]:
    """Detect duplicate top-level keys in raw YAML text (M-23).

    Scans for lines matching ``key:`` pattern and reports duplicates.
    PyYAML silently uses the last value for duplicate keys.

    Args:
        raw_yaml: The raw YAML text between delimiters.

    Returns:
        Tuple of warning messages for each duplicate key found.
    """
    key_pattern = re.compile(r"^([a-zA-Z_][a-zA-Z0-9_.-]*):", re.MULTILINE)
    keys = key_pattern.findall(raw_yaml)
    counts = Counter(keys)
    return tuple(
        f"Duplicate key '{key}' found {count} times; last value used"
        for key, count in counts.items()
        if count > 1
    )


def _strip_control_chars(value: str) -> str:
    """Strip null bytes and non-printable control characters (M-18).

    Preserves ``\\n``, ``\\r``, ``\\t``.

    Args:
        value: The string to sanitize.

    Returns:
        The sanitized string.
    """
    return _CONTROL_CHAR_RE.sub("", value)


class YamlFrontmatter:
    """Extract and validate YAML frontmatter from ``---`` delimited blocks.

    Uses ``yaml.safe_load()`` exclusively. Extracts only the first
    ``---`` ... ``---`` pair (first-pair-only rule, M-24).
    """

    @staticmethod
    def extract(
        doc: JerryDocument,
        bounds: InputBounds | None = None,
    ) -> YamlFrontmatterResult:
        """Extract YAML frontmatter from a JerryDocument.

        Args:
            doc: The parsed markdown document.
            bounds: Resource limits. Defaults to ``InputBounds.DEFAULT``.

        Returns:
            A ``YamlFrontmatterResult`` with extracted fields or error info.
        """
        if bounds is None:
            bounds = InputBounds.DEFAULT

        source = doc.source
        warnings: list[str] = []

        # --- Match first --- ... --- pair (M-24) ---
        match = _YAML_BLOCK_RE.match(source)
        if match is None:
            return YamlFrontmatterResult(
                fields=(),
                raw_yaml="",
                start_line=0,
                end_line=0,
                parse_error=None,
            )

        raw_yaml = match.group("yaml")
        start_line = 0
        end_line = raw_yaml.count("\n") + 1

        # --- Pre-parse size check (M-07) ---
        if len(raw_yaml.encode("utf-8")) > bounds.max_yaml_block_bytes:
            return YamlFrontmatterResult(
                fields=(),
                raw_yaml=raw_yaml,
                start_line=start_line,
                end_line=end_line,
                parse_error=(
                    f"YAML block exceeds maximum size "
                    f"({len(raw_yaml.encode('utf-8'))} bytes > "
                    f"{bounds.max_yaml_block_bytes} bytes)"
                ),
            )

        # --- Pre-parse alias count check (M-20) ---
        alias_count = len(_ALIAS_RE.findall(raw_yaml))
        if alias_count > bounds.max_alias_count:
            return YamlFrontmatterResult(
                fields=(),
                raw_yaml=raw_yaml,
                start_line=start_line,
                end_line=end_line,
                parse_error=(
                    f"YAML alias count exceeds maximum ({alias_count} > {bounds.max_alias_count})"
                ),
            )

        # --- Duplicate key detection (M-23) ---
        dup_warnings = _detect_duplicate_keys(raw_yaml)
        warnings.extend(dup_warnings)

        # --- Parse with yaml.safe_load() ONLY (M-01, T-YF-07) ---
        try:
            result = yaml.safe_load(raw_yaml)
        except ScannerError as e:
            line_info = ""
            if e.problem_mark is not None:
                line_info = f" at line {e.problem_mark.line}"
            return YamlFrontmatterResult(
                fields=(),
                raw_yaml=raw_yaml,
                start_line=start_line,
                end_line=end_line,
                parse_error=f"YAML scan error{line_info}: {e.problem}",
            )
        except ParserError as e:
            line_info = ""
            if e.problem_mark is not None:
                line_info = f" at line {e.problem_mark.line}"
            return YamlFrontmatterResult(
                fields=(),
                raw_yaml=raw_yaml,
                start_line=start_line,
                end_line=end_line,
                parse_error=f"YAML parse error{line_info}: {e.problem}",
            )
        except ConstructorError as e:
            return YamlFrontmatterResult(
                fields=(),
                raw_yaml=raw_yaml,
                start_line=start_line,
                end_line=end_line,
                parse_error=f"YAML construction error: {e.problem}",
            )

        if not isinstance(result, dict):
            return YamlFrontmatterResult(
                fields=(),
                raw_yaml=raw_yaml,
                start_line=start_line,
                end_line=end_line,
                parse_error=(f"YAML frontmatter must be a mapping, got {type(result).__name__}"),
            )

        # --- Post-parse result size verification (M-20) ---
        try:
            result_json = json.dumps(result, default=str)
        except (TypeError, ValueError):
            result_json = str(result)
        if len(result_json.encode("utf-8")) > bounds.max_yaml_result_bytes:
            return YamlFrontmatterResult(
                fields=(),
                raw_yaml=raw_yaml,
                start_line=start_line,
                end_line=end_line,
                parse_error=(
                    f"YAML result exceeds maximum size after expansion "
                    f"({len(result_json.encode('utf-8'))} bytes > "
                    f"{bounds.max_yaml_result_bytes} bytes)"
                ),
            )

        # --- Post-parse key count check (M-16) ---
        if len(result) > bounds.max_frontmatter_keys:
            return YamlFrontmatterResult(
                fields=(),
                raw_yaml=raw_yaml,
                start_line=start_line,
                end_line=end_line,
                parse_error=(
                    f"YAML key count exceeds maximum "
                    f"({len(result)} > {bounds.max_frontmatter_keys})"
                ),
            )

        # --- Post-parse nesting depth check (M-06) ---
        if not _check_nesting_depth(result, bounds.max_nesting_depth):
            return YamlFrontmatterResult(
                fields=(),
                raw_yaml=raw_yaml,
                start_line=start_line,
                end_line=end_line,
                parse_error=(f"YAML nesting depth exceeds maximum ({bounds.max_nesting_depth})"),
            )

        # --- Build field objects with type normalization (DD-10) ---
        fields: list[YamlFrontmatterField] = []
        for key, value in result.items():
            key_str = str(key)

            # Value length check (M-17)
            normalized, value_type = _normalize_value(value)
            if len(normalized) > bounds.max_value_length:
                warnings.append(
                    f"Value for key '{key_str}' truncated "
                    f"({len(normalized)} > {bounds.max_value_length} chars)"
                )

            # Control character stripping (M-18)
            if isinstance(value, str):
                value = _strip_control_chars(value)
            key_str = _strip_control_chars(key_str)

            fields.append(
                YamlFrontmatterField(
                    key=key_str,
                    value=value,
                    value_type=value_type,
                )
            )

        return YamlFrontmatterResult(
            fields=tuple(fields),
            raw_yaml=raw_yaml,
            start_line=start_line,
            end_line=end_line,
            parse_error=None,
            parse_warnings=tuple(warnings),
        )
