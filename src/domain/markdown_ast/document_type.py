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
    SKILL_RESOURCE = "skill_resource"
    RULE_FILE = "rule_file"
    ADR = "adr"
    STRATEGY_TEMPLATE = "strategy_template"
    WORKTRACKER_ENTITY = "worktracker_entity"
    FRAMEWORK_CONFIG = "framework_config"
    ORCHESTRATION_ARTIFACT = "orchestration_artifact"
    TEMPLATE = "template"
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
    # Security: path-first detection prevents content-based type spoofing
    # (T-DT-01 CWE-843). Pattern ordering is security-critical -- more
    # specific patterns MUST precede catch-alls to prevent type confusion.
    PATH_PATTERNS: list[tuple[str, DocumentType]] = [
        # --- Tier 1: Most specific patterns ---
        ("skills/*/agents/*.md", DocumentType.AGENT_DEFINITION),
        ("skills/*/SKILL.md", DocumentType.SKILL_DEFINITION),
        (".context/rules/*.md", DocumentType.RULE_FILE),
        (".claude/rules/*.md", DocumentType.RULE_FILE),
        ("docs/design/*.md", DocumentType.ADR),
        ("docs/adrs/*.md", DocumentType.ADR),
        (".context/templates/adversarial/*.md", DocumentType.STRATEGY_TEMPLATE),
        # --- Tier 2: Skill resources (before broad skill/* catch-all) ---
        ("skills/*/PLAYBOOK.md", DocumentType.SKILL_RESOURCE),
        ("skills/*/rules/*.md", DocumentType.RULE_FILE),
        ("skills/*/tests/*.md", DocumentType.SKILL_RESOURCE),
        ("skills/*/composition/*.md", DocumentType.SKILL_RESOURCE),
        ("skills/*/reference/*.md", DocumentType.SKILL_RESOURCE),
        ("skills/*/references/*.md", DocumentType.SKILL_RESOURCE),
        ("skills/*/templates/*.md", DocumentType.TEMPLATE),
        ("skills/*/docs/*.md", DocumentType.SKILL_RESOURCE),
        ("skills/*/validation/*.md", DocumentType.SKILL_RESOURCE),
        ("skills/*/knowledge/**/*.md", DocumentType.KNOWLEDGE_DOCUMENT),
        ("skills/shared/*.md", DocumentType.SKILL_RESOURCE),
        ("skills/*/test_data/**/*.md", DocumentType.SKILL_RESOURCE),
        ("skills/*/*.md", DocumentType.SKILL_RESOURCE),
        # --- Tier 3: Worktracker entities ---
        ("projects/*/WORKTRACKER.md", DocumentType.WORKTRACKER_ENTITY),
        ("projects/*/work/**/*.md", DocumentType.WORKTRACKER_ENTITY),
        ("projects/*/PLAN.md", DocumentType.FRAMEWORK_CONFIG),
        ("projects/*/ORCHESTRATION_PLAN.md", DocumentType.FRAMEWORK_CONFIG),
        ("projects/*/ORCHESTRATION_WORKTRACKER.md", DocumentType.WORKTRACKER_ENTITY),
        ("projects/*/decisions/*.md", DocumentType.ADR),
        ("projects/*/analysis/*.md", DocumentType.KNOWLEDGE_DOCUMENT),
        ("projects/*/research/*.md", DocumentType.KNOWLEDGE_DOCUMENT),
        ("projects/*/synthesis/*.md", DocumentType.KNOWLEDGE_DOCUMENT),
        ("projects/*/critiques/*.md", DocumentType.KNOWLEDGE_DOCUMENT),
        ("projects/*/README.md", DocumentType.FRAMEWORK_CONFIG),
        ("projects/README.md", DocumentType.FRAMEWORK_CONFIG),
        # --- Tier 4: Framework config (root-level files) ---
        ("CLAUDE.md", DocumentType.FRAMEWORK_CONFIG),
        ("AGENTS.md", DocumentType.FRAMEWORK_CONFIG),
        ("README.md", DocumentType.FRAMEWORK_CONFIG),
        ("CONTRIBUTING.md", DocumentType.FRAMEWORK_CONFIG),
        ("CODE_OF_CONDUCT.md", DocumentType.FRAMEWORK_CONFIG),
        ("SECURITY.md", DocumentType.FRAMEWORK_CONFIG),
        ("GOVERNANCE.md", DocumentType.FRAMEWORK_CONFIG),
        # --- Tier 5: Broader patterns (catch-alls last) ---
        ("projects/*/orchestration/**/*.md", DocumentType.ORCHESTRATION_ARTIFACT),
        ("work/**/*.md", DocumentType.WORKTRACKER_ENTITY),
        (".context/templates/worktracker/*.md", DocumentType.TEMPLATE),
        (".context/templates/design/*.md", DocumentType.TEMPLATE),
        (".context/templates/**/*.md", DocumentType.TEMPLATE),
        (".context/patterns/**/*.md", DocumentType.PATTERN_DOCUMENT),
        (".context/guides/*.md", DocumentType.PATTERN_DOCUMENT),
        ("docs/knowledge/**/*.md", DocumentType.KNOWLEDGE_DOCUMENT),
        ("docs/governance/*.md", DocumentType.KNOWLEDGE_DOCUMENT),
        ("docs/research/**/*.md", DocumentType.KNOWLEDGE_DOCUMENT),
        ("docs/playbooks/*.md", DocumentType.KNOWLEDGE_DOCUMENT),
        ("docs/synthesis/**/*.md", DocumentType.KNOWLEDGE_DOCUMENT),
        ("docs/schemas/*.md", DocumentType.KNOWLEDGE_DOCUMENT),
        ("docs/specifications/*.md", DocumentType.KNOWLEDGE_DOCUMENT),
        ("docs/security/*.md", DocumentType.KNOWLEDGE_DOCUMENT),
        ("docs/analysis/*.md", DocumentType.KNOWLEDGE_DOCUMENT),
        ("docs/scores/**/*.md", DocumentType.KNOWLEDGE_DOCUMENT),
        ("docs/reviews/**/*.md", DocumentType.KNOWLEDGE_DOCUMENT),
        ("docs/rewrites/**/*.md", DocumentType.KNOWLEDGE_DOCUMENT),
        ("docs/runbooks/*.md", DocumentType.KNOWLEDGE_DOCUMENT),
        ("docs/blog/**/*.md", DocumentType.KNOWLEDGE_DOCUMENT),
        ("docs/templates/*.md", DocumentType.TEMPLATE),
        ("docs/*.md", DocumentType.KNOWLEDGE_DOCUMENT),
        ("runbooks/*.md", DocumentType.KNOWLEDGE_DOCUMENT),
        ("commands/*.md", DocumentType.FRAMEWORK_CONFIG),
        (".github/*.md", DocumentType.FRAMEWORK_CONFIG),
    ]

    # Structural cue priority order for conflicting signals.
    # Higher index = lower priority. First match in the ordered list wins.
    # EN-002: Removed overly broad cues ("---" matched ALL files, "<!--"
    # matched most files). Each cue must be specific to its document type.
    # With comprehensive PATH_PATTERNS (63 entries), structural cues are
    # a fallback that should rarely activate.
    #
    # Cues evaluated and rejected (eng-security F-002):
    #   - "<purpose>": Also present in non-agent markdown files; too broad.
    #   - "## Status": Common in ADRs but also in worktracker entities,
    #     changelogs, and other files. Path patterns cover all ADR locations.
    STRUCTURAL_CUE_PRIORITY: list[tuple[str, DocumentType]] = [
        # Agent definitions use XML-tagged sections (agent-development-standards.md)
        ("<identity>", DocumentType.AGENT_DEFINITION),
        ("<methodology>", DocumentType.AGENT_DEFINITION),
        # Worktracker entities use specific blockquote frontmatter
        ("> **Type:**", DocumentType.WORKTRACKER_ENTITY),
        # Rule files use L2-REINJECT markers
        ("<!-- L2-REINJECT", DocumentType.RULE_FILE),
        # Strategy templates use specific frontmatter
        ("> **Strategy:**", DocumentType.STRATEGY_TEMPLATE),
        # Skill definitions use version frontmatter
        ("> **Version:**", DocumentType.SKILL_DEFINITION),
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

        Security precondition (CWE-843):
            For the path-first security property to hold, ``file_path``
            should be a repo-relative path or a verified filesystem path.
            Adversarial absolute paths containing embedded directory markers
            (e.g., ``/tmp/evil/skills/hack/agents/payload.md``) may bypass
            the ``already_relative`` guard in ``_normalize_path`` and receive
            an incorrect type classification. The CLI layer
            (``ast_commands.py``) validates paths before calling this
            function; direct API callers must ensure path provenance.

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

    # Handle absolute paths: try to find repo-relative portion.
    # Look for known root markers. If the path already starts with a
    # known marker (idx=0), it's already repo-relative -- skip extraction
    # to prevent embedded markers from causing false matches (F-001 CWE-22).
    root_markers = [
        "skills/",
        ".context/",
        ".claude/",
        "docs/",
        "projects/",
        "src/",
        "work/",
        "runbooks/",
        "commands/",
        ".github/",
    ]
    already_relative = any(path.startswith(m) for m in root_markers)
    if not already_relative:
        for marker in root_markers:
            idx = path.find(marker)
            if idx > 0:
                path = path[idx:]
                break

    # Handle root-level files that have no directory prefix in patterns.
    # For absolute paths where no root marker was found, reduce to basename
    # if the filename matches a known root-level file.
    _ROOT_FILES = frozenset(
        {
            "CLAUDE.md",
            "AGENTS.md",
            "README.md",
            "CONTRIBUTING.md",
            "CODE_OF_CONDUCT.md",
            "SECURITY.md",
            "GOVERNANCE.md",
            "SOUNDTRACK.md",
        }
    )
    basename = path.rsplit("/", 1)[-1] if "/" in path else path
    if basename in _ROOT_FILES and "/" in path:
        # Only reduce to basename if the path has directory components
        # that weren't resolved by root markers above
        is_under_known_root = any(path.startswith(m) for m in root_markers)
        if not is_under_known_root:
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
        for ps, pp in zip(path_segments, prefix_segments, strict=False):
            if not fnmatch.fnmatch(ps, pp):
                return False
        remaining_segments = path_segments[len(prefix_segments) :]
    else:
        remaining_segments = path_segments

    if suffix_pattern:
        suffix_segments = suffix_pattern.split("/")
        if len(remaining_segments) < len(suffix_segments):
            return False
        for rs, sp in zip(reversed(remaining_segments), reversed(suffix_segments), strict=False):
            if not fnmatch.fnmatch(rs, sp):
                return False
        return True

    return True
