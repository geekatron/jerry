# SPDX-License-Identifier: Apache-2.0
"""Hexagonal port interfaces for baseline persistence.

Defines the ``BaselinePersistencePort`` Protocol that the domain core
depends on.  Concrete adapters (e.g., ``BaselineStore``) implement this
protocol so the Layer 4 pipeline can depend on the abstraction rather
than the filesystem-backed implementation.

Architecture:
    - Hexagonal layer: DOMAIN (port definition).
    - Imports ONLY from stdlib and jerry.testing.types.
    - MUST NOT import from adapter modules (store.py, generator.py,
      layer4_stats.py).

H-07 compliance: Domain-layer module — stdlib-only imports.
H-10 compliance: One Protocol class defined in this file.
H-11 compliance: All public methods have type annotations and docstrings.
"""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from jerry.testing.types import (
    BaselineAuditEntry,
    BaselineRecord,
    EvaluationMode,
)


@runtime_checkable
class BaselinePersistencePort(Protocol):
    """Port contract for baseline score persistence and retrieval.

    Defines the interface the Layer 4 pipeline and CLI commands depend on.
    Concrete implementations (e.g., ``BaselineStore``) satisfy this protocol
    structurally — no explicit inheritance required.

    Any object that implements all of the following methods with matching
    signatures satisfies ``isinstance(obj, BaselinePersistencePort)``
    checks (enabled by ``@runtime_checkable``).

    Usage::

        from jerry.testing.baselines.ports import BaselinePersistencePort
        from jerry.testing.baselines.store import BaselineStore

        store: BaselinePersistencePort = BaselineStore(Path("baselines/data"))
        # Type checkers and runtime checks both accept this assignment.
    """

    def store(
        self,
        version_key: str,
        agent_id: str,
        metric_id: str,
        scores: list[float],
        evaluation_mode: EvaluationMode,
        model_version: str,
        *,
        min_samples: int = 30,
    ) -> BaselineRecord:
        """Persist a baseline score array after passing all quality gates.

        Args:
            version_key:      Composite key "{git_hash}:{file_path}" (FR-004).
            agent_id:         Agent identifier (e.g., "ps-researcher").
            metric_id:        Metric identifier (e.g., "composite_score").
            scores:           Ordered list of quality scores [0.0, 1.0].
            evaluation_mode:  Mode used to collect scores.
            model_version:    Pinned LLM model version string.
            min_samples:      Minimum sample size for FULL mode (default 30).

        Returns:
            The stored ``BaselineRecord``.

        Raises:
            InsufficientSamplesError: If FULL mode and len(scores) < min_samples.
            ValueError:               If mean(scores) < quality gate threshold,
                                      scores is empty, or version_key is malformed.
        """
        ...

    def retrieve(
        self,
        version_key: str,
        agent_id: str,
        metric_id: str,
    ) -> BaselineRecord | None:
        """Retrieve a stored baseline record by key.

        Args:
            version_key: Composite key "{git_hash}:{file_path}".
            agent_id:    Agent identifier.
            metric_id:   Metric identifier.

        Returns:
            ``BaselineRecord`` if found and active, ``None`` if not found.

        Raises:
            ValueError: If the stored record has ``baseline_status="invalidated"``.
        """
        ...

    def invalidate(
        self,
        agent_id: str,
        metric_id: str,
        contract_version: str,
    ) -> int:
        """Mark all baseline records for an agent-metric pair as invalidated.

        Called when a MAJOR contract version is released, per
        behavioral-contracts.md Section E.3 (baseline invalidation protocol).

        Args:
            agent_id:         Agent to invalidate.
            metric_id:        Metric to invalidate.
            contract_version: Contract version string (e.g., "2.0.0").

        Returns:
            Number of records invalidated.
        """
        ...

    def audit(self) -> list[BaselineAuditEntry]:
        """List all stored baselines with version keys, scores, and ages.

        Implements the ``jerry test baseline audit`` CLI requirement (FR-020).

        Returns:
            List of ``BaselineAuditEntry`` sorted by ``captured_at`` descending
            (newest first).
        """
        ...
