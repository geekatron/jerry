# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
DocumentTypeDetector - Jerry markdown file type detection.

Detects the document type of a Jerry markdown file using a path-first,
structure-fallback strategy. Path patterns use first-match-wins semantics
against an ordered list. Structural cues use a defined priority order for
conflicting signals.

Detection strategy:
    1. Path-based detection: match file path against ordered glob patterns.
    2. Structure-based fallback: scan content for structural cues with priority.
    3. Dual-signal validation (M-14): warn when path and structure disagree.

Security constraints:
    - Path-first prevents content-based type spoofing (T-DT-01 CWE-843)
    - ``UNKNOWN`` safe default for unclassifiable files
    - Dual-signal mismatch produces warning, not error (M-14)

References:
    - ADR-PROJ005-003 Design Decision 2 (Document Type Detection)
    - Threat Model: M-14, T-DT-01 through T-DT-05
    - H-07: Domain layer constraint (no external infra/interface imports)
    - H-10: DocumentType enum co-located with DocumentTypeDetector per ADR.

Exports:
    DocumentType: Enum classifying Jerry markdown file types.
    DocumentTypeDetector: Detector class with ``detect()`` class method.
"""

from __future__ import annotations

import fnmatch
import os
from enum import Enum


class DocumentType(Enum):
    """Jerry markdown file type classification.

    Each value represents a distinct file type with its own metadata format
    and body structure conventions.
    """

    AGENT_DEFINITION = "agent_definition"
    SKILL_DEFINITION = "skill_definition"
    RULE_FILE = "rule_file"
    ADR = "adr"
    STRATEGY_TEMPLATE = "strategy_template"
    WORKTRACKER_ENTITY = "worktracker_entity"
    FRAMEWORK_CONFIG = "framework_config"
    ORCHESTRATION_ARTIFACT = "orchestration_artifact"
    PATTERN_DOCUMENT = "pattern_document"
    KNOWLEDGE_DOCUMENT = "knowledge_document"
    UNKNOWN = "unknown"


class DocumentTypeDetector:
    """Detect Jerry markdown file type from path patterns and structural cues.

    Uses path-first, structure-fallback with first-match-wins semantics.
    Path patterns are checked in order; the first match wins.
    Structural cues are checked in priority order when no path matches.
    """

    # Ordered list: first match wins. More specific patterns before broader.
    PATH_PATTERNS: list[tuple[str, DocumentType]] = [
        # 1. Most specific patterns first
        ("skills/*/agents/*.md", DocumentType.AGENT_DEFINITION),
        ("skills/*/SKILL.md", DocumentType.SKILL_DEFINITION),
        (".context/rules/*.md", DocumentType.RULE_FILE),
        (".claude/rules/*.md", DocumentType.RULE_FILE),
        ("docs/design/*.md", DocumentType.ADR),
        (".context/templates/adversarial/*.md", DocumentType.STRATEGY_TEMPLATE),
        # 2. Worktracker patterns (multiple paths)
        ("projects/*/WORKTRACKER.md", DocumentType.WORKTRACKER_ENTITY),
        ("projects/*/work/**/*.md", DocumentType.WORKTRACKER_ENTITY),
        # 3. Framework config (exact filenames)
        ("CLAUDE.md", DocumentType.FRAMEWORK_CONFIG),
        ("AGENTS.md", DocumentType.FRAMEWORK_CONFIG),
        # 4. Broader patterns last
        ("projects/*/orchestration/**/*.md", DocumentType.ORCHESTRATION_ARTIFACT),
        ("docs/knowledge/**/*.md", DocumentType.KNOWLEDGE_DOCUMENT),
    ]

    # Structural cue priority order for conflicting signals.
    # Higher index = lower priority. First match in the ordered list wins.
    STRUCTURAL_CUE_PRIORITY: list[tuple[str, DocumentType]] = [
        ("---", DocumentType.AGENT_DEFINITION),
        ("> **", DocumentType.WORKTRACKER_ENTITY),
        ("<identity>", DocumentType.AGENT_DEFINITION),
        ("<!-- L2-REINJECT", DocumentType.RULE_FILE),
        ("<!--", DocumentType.ADR),
    ]

    @classmethod
    def detect(
        cls,
        file_path: str,
        content: str,
    ) -> tuple[DocumentType, str | None]:
        """Detect document type from file path and content.

        Path patterns take priority (first-match-wins); structural cues are
        the fallback with defined priority ordering. A warning is returned
        when path-based and structure-based detection disagree (M-14).

        Args:
            file_path: Relative or absolute file path. Normalized to
                forward-slash POSIX form for pattern matching.
            content: The file content for structural cue detection.

        Returns:
            Tuple of (detected DocumentType, optional warning string).
            Warning is ``None`` when path and structure agree or when
            only one signal is available.
        """
        normalized_path = _normalize_path(file_path)

        # --- Path-based detection (first-match-wins) ---
        path_type = cls._detect_from_path(normalized_path)

        # --- Structure-based detection ---
        structure_type = cls._detect_from_structure(content)

        # --- Combine signals ---
        if path_type is not None:
            # Path matched -- use it as authoritative
            warning = None
            if (
                structure_type is not None
                and structure_type != path_type
                and structure_type != DocumentType.UNKNOWN
            ):
                warning = (
                    f"Path suggests {path_type.value} but content "
                    f"structure suggests {structure_type.value}"
                )
            return (path_type, warning)

        # No path match -- fall back to structure
        if structure_type is not None:
            return (structure_type, None)

        return (DocumentType.UNKNOWN, None)

    @classmethod
    def _detect_from_path(cls, normalized_path: str) -> DocumentType | None:
        """Match normalized path against ordered pattern list.

        Args:
            normalized_path: Forward-slash normalized path.

        Returns:
            Matched ``DocumentType`` or ``None`` if no pattern matches.
        """
        for pattern, doc_type in cls.PATH_PATTERNS:
            if _path_matches_glob(normalized_path, pattern):
                return doc_type
        return None

    @classmethod
    def _detect_from_structure(cls, content: str) -> DocumentType | None:
        """Scan content for structural cues in priority order.

        Args:
            content: The file content to scan.

        Returns:
            Matched ``DocumentType`` or ``None`` if no cue matches.
        """
        if not content:
            return None

        for cue, doc_type in cls.STRUCTURAL_CUE_PRIORITY:
            if cue in content:
                return doc_type
        return None


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------


def _normalize_path(file_path: str) -> str:
    """Normalize file path to forward-slash POSIX form for pattern matching.

    Strips leading ``./`` and converts backslashes. If the path is absolute
    and contains a recognizable Jerry repository root marker, extracts the
    relative portion.

    Args:
        file_path: Raw file path (relative or absolute).

    Returns:
        Normalized forward-slash path suitable for glob matching.
    """
    # Convert to forward slashes
    path = file_path.replace(os.sep, "/")

    # Strip leading ./
    if path.startswith("./"):
        path = path[2:]

    # Handle absolute paths: try to find repo-relative portion
    # Look for known root markers
    root_markers = [
        "skills/",
        ".context/",
        ".claude/",
        "docs/",
        "projects/",
        "src/",
    ]
    for marker in root_markers:
        idx = path.find(marker)
        if idx > 0:
            path = path[idx:]
            break

    # Handle exact filename matches (CLAUDE.md, AGENTS.md)
    basename = path.rsplit("/", 1)[-1] if "/" in path else path
    if basename in ("CLAUDE.md", "AGENTS.md"):
        # Check if it's at the repo root (no deeper nesting beyond expected)
        # For pattern matching, we need just the basename
        path = basename

    return path


def _path_matches_glob(path: str, pattern: str) -> bool:
    """Check if a path matches a glob pattern.

    Supports ``*`` (single directory segment) and ``**`` (recursive).

    Uses ``fnmatch`` for simple patterns and manual splitting for ``**``.

    Args:
        path: Normalized forward-slash file path.
        pattern: Glob pattern with ``*`` and ``**``.

    Returns:
        ``True`` if the path matches the pattern.
    """
    if "**" in pattern:
        return _match_recursive_glob(path, pattern)
    return fnmatch.fnmatch(path, pattern)


def _match_recursive_glob(path: str, pattern: str) -> bool:
    """Match a path against a glob pattern containing ``**``.

    Splits on ``**`` and checks that the prefix matches the start,
    the suffix matches the end, and the middle contains the ``**`` content.

    Args:
        path: Normalized forward-slash file path.
        pattern: Glob pattern containing ``**``.

    Returns:
        ``True`` if the path matches.
    """
    # Split pattern on ** to get segments
    parts = pattern.split("**")
    if len(parts) != 2:
        # Multiple ** -- fall back to fnmatch (best effort)
        return fnmatch.fnmatch(path, pattern)

    prefix_pattern = parts[0].rstrip("/")
    suffix_pattern = parts[1].lstrip("/")

    # The prefix must match the beginning of the path
    path_segments = path.split("/")

    if prefix_pattern:
        prefix_segments = prefix_pattern.split("/")
        if len(path_segments) < len(prefix_segments):
            return False
        for ps, pp in zip(path_segments, prefix_segments):
            if not fnmatch.fnmatch(ps, pp):
                return False
        remaining_segments = path_segments[len(prefix_segments) :]
    else:
        remaining_segments = path_segments

    if suffix_pattern:
        suffix_segments = suffix_pattern.split("/")
        if len(remaining_segments) < len(suffix_segments):
            return False
        for rs, sp in zip(
            reversed(remaining_segments), reversed(suffix_segments)
        ):
            if not fnmatch.fnmatch(rs, sp):
                return False
        return True

    return True
