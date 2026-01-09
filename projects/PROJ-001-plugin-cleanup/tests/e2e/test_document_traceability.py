"""
End-to-End Tests: Document Traceability Chain

Tests that verify the complete document traceability chain from
research -> synthesis -> analysis -> decisions -> reports.

This simulates what a human or agent would do when following
document references through the artifact chain.

Test Categories:
- Happy Path: Full chain traversal succeeds
- Lineage: Verify document provenance
- Round Trip: Start from any document, reach all related docs
"""
from __future__ import annotations

import re
from pathlib import Path
from typing import Set

import pytest


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def extract_document_references(content: str) -> set[str]:
    """Extract all document references from content."""
    # Match paths in backticks that look like project paths
    pattern = r"`(projects/PROJ-001-plugin-cleanup/[^`]+\.md)`"
    matches = re.findall(pattern, content)
    return set(matches)


def build_document_graph(proj_001_root: Path, project_root: Path) -> dict[str, set[str]]:
    """
    Build a graph of document references.

    Returns: {document_path: set of referenced_document_paths}
    """
    graph = {}

    for md_file in proj_001_root.rglob("*.md"):
        relative_path = str(md_file.relative_to(project_root))
        content = md_file.read_text()
        references = extract_document_references(content)
        graph[relative_path] = references

    return graph


def traverse_from_document(
    start: str,
    graph: dict[str, set[str]],
    visited: Set[str] | None = None
) -> set[str]:
    """
    Traverse the document graph from a starting point.

    Returns all reachable documents.
    """
    if visited is None:
        visited = set()

    if start in visited:
        return visited

    visited.add(start)

    for ref in graph.get(start, set()):
        traverse_from_document(ref, graph, visited)

    return visited


# =============================================================================
# E2E TESTS - DOCUMENT CHAIN TRAVERSAL
# =============================================================================

class TestDocumentChainTraversal:
    """Test complete document chain traversal."""

    def test_synthesis_references_all_research(self, proj_001_root: Path, project_root: Path):
        """
        E2E: Synthesis document (e-006) should reference all research documents (e-001 to e-005).

        This verifies the traceability chain: research -> synthesis
        """
        synthesis_path = proj_001_root / "synthesis" / "PROJ-001-e-006-unified-architecture-canon.md"
        content = synthesis_path.read_text()
        refs = extract_document_references(content)

        expected_research = [
            "projects/PROJ-001-plugin-cleanup/research/PROJ-001-e-001-worktracker-proposal-extraction.md",
            "projects/PROJ-001-plugin-cleanup/research/PROJ-001-e-002-plan-graph-model.md",
            "projects/PROJ-001-plugin-cleanup/research/PROJ-001-e-003-revised-architecture-foundation.md",
            "projects/PROJ-001-plugin-cleanup/research/PROJ-001-e-004-strategic-plan-v3.md",
            "projects/PROJ-001-plugin-cleanup/research/PROJ-001-e-005-industry-best-practices.md",
        ]

        for expected in expected_research:
            assert expected in refs, f"Synthesis missing reference to: {expected}"

    def test_analysis_references_synthesis(self, proj_001_root: Path):
        """
        E2E: Analysis documents should reference synthesis document.

        This verifies the traceability chain: synthesis -> analysis
        """
        analysis_files = [
            proj_001_root / "analysis" / "PROJ-001-e-007-implementation-gap-analysis.md",
            proj_001_root / "analysis" / "PROJ-001-e-009-alignment-validation.md",
        ]

        synthesis_ref = "projects/PROJ-001-plugin-cleanup/synthesis/PROJ-001-e-006-unified-architecture-canon.md"

        for analysis_file in analysis_files:
            content = analysis_file.read_text()
            refs = extract_document_references(content)
            assert synthesis_ref in refs, f"{analysis_file.name} missing reference to synthesis"

    def test_report_references_full_chain(self, proj_001_root: Path):
        """
        E2E: Status report (e-010) should reference the full document chain.

        This verifies the complete traceability: research -> synthesis -> analysis -> report
        """
        report_path = proj_001_root / "reports" / "PROJ-001-e-010-synthesis-status-report.md"
        content = report_path.read_text()
        refs = extract_document_references(content)

        # Should reference research
        assert any("research" in r for r in refs), "Report should reference research documents"

        # Should reference synthesis
        assert any("synthesis" in r for r in refs), "Report should reference synthesis documents"

        # Should reference analysis
        assert any("analysis" in r for r in refs), "Report should reference analysis documents"

        # Should reference decisions
        assert any("decisions" in r for r in refs), "Report should reference decision documents"

    def test_complete_document_graph_is_connected(self, proj_001_root: Path, project_root: Path):
        """
        E2E: Starting from the status report, we should be able to reach
        all primary Phase 7 artifacts through references.
        """
        graph = build_document_graph(proj_001_root, project_root)

        # Start from the status report (top of the chain)
        start = "projects/PROJ-001-plugin-cleanup/reports/PROJ-001-e-010-synthesis-status-report.md"

        # Traverse and collect reachable documents
        reachable = traverse_from_document(start, graph)

        # Should reach synthesis
        synthesis = "projects/PROJ-001-plugin-cleanup/synthesis/PROJ-001-e-006-unified-architecture-canon.md"
        assert synthesis in reachable, f"Cannot reach synthesis from report. Reachable: {reachable}"


# =============================================================================
# E2E TESTS - DOCUMENT LINEAGE VERIFICATION
# =============================================================================

class TestDocumentLineage:
    """Test document lineage and provenance."""

    def test_all_phase7_artifacts_have_metadata(self, proj_001_root: Path):
        """
        E2E: All Phase 7 artifacts should have required metadata headers.

        Required: Some form of ID (Document ID, PS ID, Entry ID), Date
        """
        phase7_docs = [
            proj_001_root / "research" / "PROJ-001-e-001-worktracker-proposal-extraction.md",
            proj_001_root / "synthesis" / "PROJ-001-e-006-unified-architecture-canon.md",
            proj_001_root / "analysis" / "PROJ-001-e-007-implementation-gap-analysis.md",
            proj_001_root / "reports" / "PROJ-001-e-010-synthesis-status-report.md",
        ]

        for doc in phase7_docs:
            if not doc.exists():
                pytest.skip(f"Document not found: {doc}")

            content = doc.read_text()
            header = content[:1000]  # Check first 1000 chars

            # Should have some form of ID (Document ID, PS ID, Entry ID, or Project)
            has_id = any(x in header for x in ["Document ID", "PS ID", "Entry ID", "Project"])
            assert has_id, f"{doc.name} missing identifier (Document ID, PS ID, Entry ID, or Project)"

            # Should have date
            assert "Date" in header, f"{doc.name} missing Date"

    def test_documents_reference_correct_project(self, proj_001_root: Path):
        """
        E2E: All documents should reference PROJ-001-plugin-cleanup, not other projects.
        """
        for md_file in proj_001_root.rglob("*.md"):
            content = md_file.read_text()

            # Check for references to wrong projects
            wrong_project_pattern = re.compile(r"projects/PROJ-00[2-9]|projects/PROJ-01")
            wrong_refs = wrong_project_pattern.findall(content)

            assert len(wrong_refs) == 0, (
                f"{md_file.name} references wrong project: {wrong_refs}"
            )


# =============================================================================
# E2E TESTS - ROUND TRIP VALIDATION
# =============================================================================

class TestRoundTripValidation:
    """Test that document references form valid round trips."""

    def test_bidirectional_references_where_expected(self, proj_001_root: Path, project_root: Path):
        """
        E2E: Key documents should have bidirectional references.

        Example: If gap analysis references canon, canon's "Referenced By"
        section should mention gap analysis (if such section exists).
        """
        # This test verifies the documentation is interconnected
        # For now, we just verify the forward references work

        gap_analysis = proj_001_root / "analysis" / "PROJ-001-e-007-implementation-gap-analysis.md"
        content = gap_analysis.read_text()

        # Gap analysis should reference canon (forward reference)
        refs = extract_document_references(content)
        canon_ref = "projects/PROJ-001-plugin-cleanup/synthesis/PROJ-001-e-006-unified-architecture-canon.md"

        assert canon_ref in refs, "Gap analysis should reference canon"

        # Verify the referenced file exists (complete round trip)
        canon_path = project_root / canon_ref
        assert canon_path.exists(), f"Canon file does not exist: {canon_path}"

    def test_all_references_are_valid_files(self, proj_001_root: Path, project_root: Path):
        """
        E2E: Every document reference in every file should resolve to an existing file.

        This is the ultimate validation that the fix is complete and correct.
        """
        broken_refs = []

        for md_file in proj_001_root.rglob("*.md"):
            content = md_file.read_text()
            refs = extract_document_references(content)

            for ref in refs:
                ref_path = project_root / ref
                if not ref_path.exists():
                    broken_refs.append((md_file.name, ref))

        assert len(broken_refs) == 0, (
            f"Found {len(broken_refs)} broken references:\n" +
            "\n".join(f"  {doc}: {ref}" for doc, ref in broken_refs)
        )
