# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Victor Lau

"""Hexagonal port interfaces for regression report output.

Defines the ``ReportOutputPort`` Protocol that the domain core depends on.
Concrete adapters (e.g., ``ReportGenerator``) implement this protocol so
the Layer 4 pipeline can depend on the abstraction rather than a specific
report-rendering implementation.

Architecture:
    - Hexagonal layer: DOMAIN (port definition).
    - Imports ONLY from stdlib and jerry.testing.types.
    - MUST NOT import from adapter modules (generator.py, store.py,
      layer4_stats.py).

H-07 compliance: Domain-layer module — stdlib-only imports.
H-10 compliance: One Protocol class defined in this file.
H-11 compliance: All public methods have type annotations and docstrings.
"""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from jerry.testing.types import (
    ComparisonReport,
    EvaluationMode,
    MultiMetricResult,
    RegressionResult,
)


@runtime_checkable
class ReportOutputPort(Protocol):
    """Port contract for regression report generation and serialisation.

    Defines the interface the Layer 4 pipeline depends on for building
    and serialising ``ComparisonReport`` objects.  Concrete implementations
    (e.g., ``ReportGenerator``) satisfy this protocol structurally — no
    explicit inheritance required.

    Any object that implements all of the following methods with matching
    signatures satisfies ``isinstance(obj, ReportOutputPort)`` checks
    (enabled by ``@runtime_checkable``).

    Usage::

        from jerry.testing.reports.ports import ReportOutputPort
        from jerry.testing.reports.generator import ReportGenerator

        gen: ReportOutputPort = ReportGenerator()
        # Type checkers and runtime checks both accept this assignment.
    """

    def from_single_metric(
        self,
        result: RegressionResult,
        *,
        structural_violations: list[str] | None = None,
    ) -> ComparisonReport:
        """Build a ``ComparisonReport`` from a single-metric ``RegressionResult``.

        Args:
            result:                The ``RegressionResult`` from ``compare_versions()``.
            structural_violations: Structural invariant violation descriptions
                                   (Section A invariants), if any.

        Returns:
            ``ComparisonReport`` with all required fields populated.
        """
        ...

    def from_multi_metric(
        self,
        multi_result: MultiMetricResult,
        agent_id: str,
        version_key_a: str,
        version_key_b: str,
        evaluation_mode: EvaluationMode,
        *,
        structural_violations: list[str] | None = None,
    ) -> ComparisonReport:
        """Build a ``ComparisonReport`` from a multi-metric Bonferroni-corrected result.

        Args:
            multi_result:          The ``MultiMetricResult`` from ``compare_multiple_metrics()``.
            agent_id:              Target agent identifier.
            version_key_a:         Baseline version key.
            version_key_b:         Candidate version key.
            evaluation_mode:       Evaluation mode used.
            structural_violations: Structural invariant violation descriptions.

        Returns:
            ``ComparisonReport`` with Bonferroni disclosure in narrative.
        """
        ...

    def smoke_mode_report(
        self,
        agent_id: str,
        version_key: str,
        structural_violations: list[str],
    ) -> ComparisonReport:
        """Build a structural-only ``ComparisonReport`` for Smoke mode evaluations.

        Smoke mode does not perform statistical comparison.  The report is
        labelled as "STRUCTURAL ONLY — not statistically valid" per FR-005.

        Args:
            agent_id:               Target agent identifier.
            version_key:            Version key of the evaluated prompt.
            structural_violations:  Structural invariant failures, if any.

        Returns:
            ``ComparisonReport`` with ``classification="STRUCTURAL_FAIL"`` or
            ``"STRUCTURAL_PASS"``.
        """
        ...

    def to_markdown(self, report: ComparisonReport) -> str:
        """Render a ``ComparisonReport`` as Markdown for GitHub PR comments.

        Includes verdict, per-metric Wilcoxon results, Wilson confidence
        intervals, and Bonferroni correction disclosure (FR-018).

        Args:
            report: The ``ComparisonReport`` to render.

        Returns:
            Markdown-formatted string suitable for a GitHub PR comment.
        """
        ...

    def to_json(self, report: ComparisonReport) -> str:
        """Serialise a ``ComparisonReport`` to JSON matching the D.6 schema.

        Args:
            report: The ``ComparisonReport`` to serialise.

        Returns:
            Pretty-printed JSON string compatible with behavioral-contracts.md
            Section D.6 report schema.
        """
        ...
