"""
Contract Tests: Document Schema Compliance

Tests that verify documents conform to expected schema and format.
These tests validate the "contract" between document producers (ps-* agents)
and consumers (humans, other agents).

Test Categories:
- Happy Path: Documents conform to schema
- Required Fields: Mandatory metadata present
- Path Format: References use correct format
"""
from __future__ import annotations

import re
from pathlib import Path

import pytest


# =============================================================================
# SCHEMA DEFINITIONS
# =============================================================================

REQUIRED_HEADER_FIELDS = {
    # Research uses "Entry ID" or "Document ID"
    "research": ["PS ID", "Date"],
    "synthesis": ["PS ID", "Date", "Synthesizer", "Sources"],
    "analysis": ["PS ID", "Date"],
    "reports": ["Date", "Project", "Phase"],
    "decisions": ["Status", "Date"],
}

PATH_FORMAT_PATTERN = re.compile(
    r"projects/PROJ-\d{3}-[a-z0-9-]+/(research|synthesis|analysis|decisions|reports)/"
)

DOCUMENT_ID_PATTERN = re.compile(r"PROJ-\d{3}-e-\d{3}")


# =============================================================================
# CONTRACT TESTS - HEADER SCHEMA
# =============================================================================

class TestDocumentHeaderSchema:
    """Test that documents have required header fields."""

    def test_research_documents_have_required_headers(self, proj_001_root: Path):
        """Research documents should have required header fields."""
        research_dir = proj_001_root / "research"
        required = REQUIRED_HEADER_FIELDS["research"]

        for doc in research_dir.glob("PROJ-001-*.md"):
            content = doc.read_text()
            header = content[:500]

            for field in required:
                assert field in header, f"{doc.name} missing required field: {field}"

    def test_synthesis_documents_have_required_headers(self, proj_001_root: Path):
        """Synthesis documents should have required header fields."""
        synthesis_dir = proj_001_root / "synthesis"
        required = REQUIRED_HEADER_FIELDS["synthesis"]

        for doc in synthesis_dir.glob("PROJ-001-*.md"):
            content = doc.read_text()
            header = content[:800]

            for field in required:
                assert field in header, f"{doc.name} missing required field: {field}"

    def test_analysis_documents_have_required_headers(self, proj_001_root: Path):
        """Analysis documents should have required header fields."""
        analysis_dir = proj_001_root / "analysis"
        required = REQUIRED_HEADER_FIELDS["analysis"]

        for doc in analysis_dir.glob("PROJ-001-e-*.md"):
            content = doc.read_text()
            header = content[:500]

            for field in required:
                assert field in header, f"{doc.name} missing required field: {field}"

    def test_report_documents_have_required_headers(self, proj_001_root: Path):
        """Report documents should have required header fields."""
        reports_dir = proj_001_root / "reports"
        required = REQUIRED_HEADER_FIELDS["reports"]

        for doc in reports_dir.glob("PROJ-001-*.md"):
            content = doc.read_text()
            header = content[:500]

            for field in required:
                assert field in header, f"{doc.name} missing required field: {field}"


# =============================================================================
# CONTRACT TESTS - PATH FORMAT
# =============================================================================

class TestPathFormatContract:
    """Test that path references conform to expected format."""

    def test_all_project_paths_match_format(self, proj_001_root: Path):
        """
        CONTRACT: All project path references in PHASE 7 artifacts must match the expected format.

        Format: projects/PROJ-{NNN}-{slug}/{category}/...
        Exceptions: archive paths, template paths, design paths, PLAN/WORKTRACKER paths
        """
        violations = []

        # Only check Phase 7 synthesis artifacts
        phase7_artifacts = [
            proj_001_root / "synthesis" / "PROJ-001-e-006-unified-architecture-canon.md",
            proj_001_root / "analysis" / "PROJ-001-e-007-implementation-gap-analysis.md",
            proj_001_root / "analysis" / "PROJ-001-e-009-alignment-validation.md",
            proj_001_root / "reports" / "PROJ-001-e-010-synthesis-status-report.md",
        ]

        for md_file in phase7_artifacts:
            if not md_file.exists():
                continue

            content = md_file.read_text()

            # Find all paths that look like PROJ-001 project references
            all_paths = re.findall(r"`(projects/PROJ-001-plugin-cleanup/[^`]+)`", content)

            for path in all_paths:
                # Only validate paths to artifact categories (research, synthesis, etc.)
                if any(cat in path for cat in ["/research/", "/synthesis/", "/analysis/", "/decisions/", "/reports/"]):
                    if not PATH_FORMAT_PATTERN.match(path):
                        violations.append((md_file.name, path))

        assert len(violations) == 0, (
            f"Found {len(violations)} path format violations:\n" +
            "\n".join(f"  {doc}: {path}" for doc, path in violations)
        )

    def test_no_docs_prefix_paths(self, proj_001_root: Path):
        """
        CONTRACT: No path references should use deprecated docs/ prefix in Phase 7 artifacts.

        Specifically checks e-006, e-007, e-009, e-010 (BUG-001 affected files).
        """
        violations = []
        deprecated_pattern = re.compile(r"`docs/(research|synthesis|analysis|decisions)/PROJ-001")

        # Only check Phase 7 synthesis artifacts (the BUG-001 affected files)
        phase7_artifacts = [
            proj_001_root / "synthesis" / "PROJ-001-e-006-unified-architecture-canon.md",
            proj_001_root / "analysis" / "PROJ-001-e-007-implementation-gap-analysis.md",
            proj_001_root / "analysis" / "PROJ-001-e-009-alignment-validation.md",
            proj_001_root / "reports" / "PROJ-001-e-010-synthesis-status-report.md",
        ]

        for md_file in phase7_artifacts:
            if not md_file.exists():
                continue

            content = md_file.read_text()
            matches = deprecated_pattern.findall(content)

            if matches:
                violations.append((md_file.name, matches))

        assert len(violations) == 0, (
            f"Found {len(violations)} deprecated docs/ paths in Phase 7 artifacts:\n" +
            "\n".join(f"  {doc}: {paths}" for doc, paths in violations)
        )


# =============================================================================
# CONTRACT TESTS - DOCUMENT ID FORMAT
# =============================================================================

class TestDocumentIdContract:
    """Test that document IDs follow expected format."""

    def test_research_docs_have_valid_ids(self, proj_001_root: Path):
        """Research documents should have valid document IDs.

        Research docs may use either:
        - Combined format: PROJ-NNN-e-NNN
        - Separate format: PS ID: PROJ-NNN + Entry ID: e-NNN
        """
        research_dir = proj_001_root / "research"

        # Patterns for separate ID format used by ps-researcher agent
        ps_id_pattern = re.compile(r"PS ID[:\s*]+PROJ-\d{3}")
        entry_id_pattern = re.compile(r"Entry ID[:\s*]+e-\d{3}")

        for doc in research_dir.glob("PROJ-001-e-*.md"):
            content = doc.read_text()
            header = content[:500]

            # Check for either combined or separate format
            has_combined = DOCUMENT_ID_PATTERN.search(header) is not None
            has_separate = (ps_id_pattern.search(header) is not None and
                           entry_id_pattern.search(header) is not None)

            assert has_combined or has_separate, (
                f"{doc.name} has invalid or missing document ID. "
                f"Expected either 'PROJ-NNN-e-NNN' or 'PS ID: PROJ-NNN' + 'Entry ID: e-NNN'"
            )

    def test_synthesis_docs_have_valid_ids(self, proj_001_root: Path):
        """Synthesis documents should have valid document IDs."""
        synthesis_dir = proj_001_root / "synthesis"

        for doc in synthesis_dir.glob("PROJ-001-e-*.md"):
            content = doc.read_text()
            header = content[:300]

            match = DOCUMENT_ID_PATTERN.search(header)
            assert match is not None, f"{doc.name} has invalid or missing document ID"

    def test_analysis_docs_have_valid_ids(self, proj_001_root: Path):
        """Analysis documents should have valid document IDs."""
        analysis_dir = proj_001_root / "analysis"

        for doc in analysis_dir.glob("PROJ-001-e-*.md"):
            content = doc.read_text()
            header = content[:300]

            match = DOCUMENT_ID_PATTERN.search(header)
            assert match is not None, f"{doc.name} has invalid or missing document ID"


# =============================================================================
# CONTRACT TESTS - REFERENCE CONSISTENCY
# =============================================================================

class TestReferenceConsistencyContract:
    """Test that references are consistent across documents."""

    def test_synthesis_source_count_matches_references(self, proj_001_root: Path):
        """
        CONTRACT: Synthesis document should reference exactly 5 research sources.
        """
        synthesis_path = proj_001_root / "synthesis" / "PROJ-001-e-006-unified-architecture-canon.md"
        content = synthesis_path.read_text()

        # Count research references
        research_refs = re.findall(
            r"projects/PROJ-001-plugin-cleanup/research/PROJ-001-e-\d{3}",
            content
        )
        unique_refs = set(research_refs)

        # Should reference e-001 through e-005
        expected_count = 5
        assert len(unique_refs) == expected_count, (
            f"Synthesis should reference {expected_count} research docs, found {len(unique_refs)}: {unique_refs}"
        )

    def test_report_mentions_all_artifact_categories(self, proj_001_root: Path):
        """
        CONTRACT: Status report should mention all artifact categories.
        """
        report_path = proj_001_root / "reports" / "PROJ-001-e-010-synthesis-status-report.md"
        content = report_path.read_text()

        required_categories = ["research", "synthesis", "analysis", "decisions"]

        for category in required_categories:
            assert category.lower() in content.lower(), (
                f"Status report should mention '{category}' artifacts"
            )
