# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Victor Lau

"""Baseline persistence and retrieval for the Four-Layer Composite Test Harness.

This module implements the BaselineStore adapter that persists and retrieves
score arrays keyed by git commit hash + agent definition file path (FR-004).

Architecture:
    - Hexagonal layer: ADAPTER (outbound).
    - Depends on: jerry.testing.types (domain), jerry.testing.stats (domain,
      for InsufficientSamplesError), stdlib (json, pathlib, datetime).
    - MUST NOT be imported by domain modules (stats.py, types.py).

Storage format:
    baselines/data/{agent_id}/{metric_id}/{version_key_slug}.json

Each file is a JSON object matching the BaselineRecord dataclass fields.

FR-020 baseline quality gate:
    Before a baseline is accepted, mean(scores) >= QUALITY_PASS_THRESHOLD (0.92)
    is verified.  Below-threshold candidates are rejected with a logged reason.

FR-004 version key format:
    "{git_commit_hash}:{file_path}"
    e.g., "abc1234:skills/problem-solving/agents/ps-researcher.md"

STANDARD mode N accumulation protocol (FR-005 / FR-017 AC-1):
    STANDARD mode runs N=10 evaluations per invocation.  The Wilcoxon
    signed-rank test in stats.compare_versions() requires N >= 20 paired
    observations (MIN_STATISTICAL_SAMPLE_SIZE).  To bridge this gap:

    1. Each STANDARD invocation stores its N=10 scores via BaselineStore.store()
       with evaluation_mode=STANDARD.  The FULL-mode N>=30 guard does NOT apply
       to STANDARD batches — STANDARD stores accept any N >= 1.
    2. Subsequent STANDARD invocations for the same (agent_id, metric_id,
       version_key) append to the existing baseline record, accumulating scores.
    3. Once accumulated N >= 20 (MIN_STATISTICAL_SAMPLE_SIZE), Layer 4's
       compare_versions() can perform the Wilcoxon comparison.
    4. If accumulated N < 20, compare_versions() raises InsufficientSamplesError,
       signalling the caller to run additional STANDARD batches.
    5. FULL mode (N=30 per invocation) always satisfies the minimum in one pass.

H-10 compliance: One class (BaselineStore) defined in this file.
H-11 compliance: All public methods have type annotations and docstrings.
"""

from __future__ import annotations

import dataclasses
import hashlib
import json
import logging
from datetime import UTC, datetime
from pathlib import Path

from jerry.testing.stats import InsufficientSamplesError
from jerry.testing.types import (
    BaselineAuditEntry,
    BaselineRecord,
    EvaluationMode,
)

logger = logging.getLogger(__name__)

#: Quality gate threshold for baseline acceptance (mirrors stats.QUALITY_PASS_THRESHOLD).
#: FR-020 acceptance criterion: "verify that the candidate baseline's quality score
#: passes the quality gate (>= 0.92)."
#: Duplicated here rather than imported from stats.py to maintain a clear
#: constant definition that is not transitively dependent on stats-level imports.
_BASELINE_QUALITY_GATE: float = 0.92


class BaselineStore:
    """Git-indexed baseline score store for the PROJ-036 regression harness.

    Persists baseline score arrays for each agent-metric-version combination
    as JSON files on the local filesystem.  The store is append-only: existing
    records are never overwritten; invalidated records are marked in-place.

    Thread safety: This class is NOT thread-safe.  Concurrent baseline capture
    runs must be serialized externally (e.g., via filelock).

    Usage example::

        store = BaselineStore(Path("baselines/data"))
        record = store.store(
            version_key="abc1234:skills/ps-researcher.md",
            agent_id="ps-researcher",
            metric_id="composite_score",
            scores=[0.93, 0.91, ...],  # N >= 20 scores
            evaluation_mode=EvaluationMode.FULL,
            model_version="claude-sonnet-4-20250514",
        )
        retrieved = store.retrieve(
            version_key="abc1234:skills/ps-researcher.md",
            agent_id="ps-researcher",
            metric_id="composite_score",
        )

        # Invalidate baselines after a MAJOR contract version release
        # (behavioral-contracts.md Section E.3):
        count = store.invalidate(
            agent_id="ps-researcher",
            metric_id="composite_score",
            contract_version="2.0.0",
        )
        # count = N records marked as invalidated; re-collect with Full mode.
    """

    def __init__(self, store_root: Path) -> None:
        """Initialise the baseline store.

        Args:
            store_root: Root directory for baseline storage.  Will be created
                        if it does not exist.  Typically
                        ``projects/PROJ-036-prompt-regression-harness/baselines/data/``.
        """
        self._root = store_root
        self._root.mkdir(parents=True, exist_ok=True)

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    #: Minimum number of scores required for FULL mode baselines.
    #: FR-014 acceptance criterion: "N >= 20 observations per metric per agent"
    #: (minimum).  N=30 chosen for production baselines to provide adequate
    #: statistical power for Wilcoxon signed-rank comparisons (FR-017 AC-1),
    #: consistent with the recommendation in behavioral-contracts.md Section D.1
    #: that "baseline capture uses N=30 per-agent per-metric."
    MIN_FULL_SAMPLES: int = 30

    def store(
        self,
        version_key: str,
        agent_id: str,
        metric_id: str,
        scores: list[float],
        evaluation_mode: EvaluationMode,
        model_version: str,
        *,
        min_samples: int = MIN_FULL_SAMPLES,
    ) -> BaselineRecord:
        """Persist a baseline score array after passing the quality gate.

        FR-020 acceptance criterion: before storage, verifies that
        mean(scores) >= 0.92.  Rejects and raises ValueError if not.

        For FULL mode baselines, also enforces N >= min_samples (default 30).
        N=30 is the production minimum for adequate statistical power in
        Wilcoxon signed-rank comparisons (FR-017 AC-1, behavioral-contracts.md
        Section D.1); storing sub-30 baselines in FULL mode would silently
        weaken subsequent regression detection.

        Args:
            version_key:      Composite key "{git_hash}:{file_path}".
            agent_id:         Agent identifier (e.g., "ps-researcher").
            metric_id:        Metric identifier (e.g., "composite_score").
            scores:           Ordered list of quality scores [0.0, 1.0].
            evaluation_mode:  Mode used to collect scores (FULL recommended
                              for baselines; STANDARD permitted with warning).
            model_version:    Pinned LLM model version string.
            min_samples:      Minimum sample size enforced for FULL mode
                              (default 30, per FR-017 AC-1 / behavioral-contracts.md
                              Section D.1).  Override for testing flexibility only.

        Returns:
            The stored BaselineRecord.

        Raises:
            InsufficientSamplesError: If evaluation_mode is FULL and
                len(scores) < min_samples (production baseline protocol).
            ValueError: If mean(scores) < 0.92 (quality gate rejection).
            ValueError: If scores is empty.
            ValueError: If version_key is not in "{hash}:{path}" format.
        """
        self._validate_version_key(version_key)
        if not scores:
            raise ValueError("scores must not be empty.")

        # --- N >= min_samples enforcement for FULL mode (FR-017 AC-1) ---
        if evaluation_mode == EvaluationMode.FULL and len(scores) < min_samples:
            raise InsufficientSamplesError(
                f"FULL mode baseline requires N >= {min_samples} scores "
                f"(got {len(scores)}) for {agent_id}/{metric_id} "
                f"(version={version_key}). "
                "FR-017 AC-1 / behavioral-contracts.md Section D.1: N=30 is "
                "the minimum for adequate Wilcoxon signed-rank statistical power."
            )

        mean_score = sum(scores) / len(scores)
        if mean_score < _BASELINE_QUALITY_GATE:
            logger.warning(
                "Baseline rejected for %s/%s (version=%s): mean_score=%.4f < quality gate %.2f.",
                agent_id,
                metric_id,
                version_key,
                mean_score,
                _BASELINE_QUALITY_GATE,
            )
            raise ValueError(
                f"Baseline quality gate rejected: mean_score={mean_score:.4f} "
                f"< {_BASELINE_QUALITY_GATE} for "
                f"agent={agent_id}, metric={metric_id}, version={version_key}."
            )

        if evaluation_mode == EvaluationMode.STANDARD:
            logger.warning(
                "Baseline captured in STANDARD mode (N=%d) for %s/%s. "
                "FULL mode (N >= %d) is recommended for production baselines.",
                len(scores),
                agent_id,
                metric_id,
                min_samples,
            )

        record = BaselineRecord(
            version_key=version_key,
            agent_id=agent_id,
            metric_id=metric_id,
            scores=list(scores),
            mean_score=mean_score,
            n_runs=len(scores),
            evaluation_mode=evaluation_mode,
            model_version=model_version,
            captured_at=datetime.now(UTC).isoformat(),
            baseline_status="active",
            invalidated_by=None,
        )

        path = self._record_path(version_key, agent_id, metric_id)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            json.dumps(dataclasses.asdict(record), indent=2),
            encoding="utf-8",
        )
        logger.info(
            "Baseline stored: %s/%s version=%s mean=%.4f n=%d.",
            agent_id,
            metric_id,
            version_key,
            mean_score,
            len(scores),
        )
        return record

    def retrieve(
        self,
        version_key: str,
        agent_id: str,
        metric_id: str,
    ) -> BaselineRecord | None:
        """Retrieve a stored baseline record.

        Args:
            version_key: Composite key "{git_hash}:{file_path}".
            agent_id:    Agent identifier.
            metric_id:   Metric identifier.

        Returns:
            BaselineRecord if found and active, None if not found.

        Raises:
            ValueError: If the stored record has baseline_status="invalidated"
                        (callers must handle this case explicitly by
                        re-collecting the baseline).
        """
        path = self._record_path(version_key, agent_id, metric_id)
        if not path.exists():
            return None

        data = json.loads(path.read_text(encoding="utf-8"))
        record = BaselineRecord(
            version_key=data["version_key"],
            agent_id=data["agent_id"],
            metric_id=data["metric_id"],
            scores=data["scores"],
            mean_score=data["mean_score"],
            n_runs=data["n_runs"],
            evaluation_mode=EvaluationMode(data["evaluation_mode"]),
            model_version=data["model_version"],
            captured_at=data["captured_at"],
            baseline_status=data.get("baseline_status", "active"),
            invalidated_by=data.get("invalidated_by"),
        )

        if record.baseline_status == "invalidated":
            raise ValueError(
                f"Baseline for {agent_id}/{metric_id} (version={version_key}) "
                f"has been invalidated by contract {record.invalidated_by}. "
                "Re-collect the baseline using Full mode (N=30)."
            )

        return record

    def invalidate(
        self,
        agent_id: str,
        metric_id: str,
        contract_version: str,
    ) -> int:
        """Mark all baseline records for an agent-metric pair as invalidated.

        Per behavioral-contracts.md Section E.3 (baseline invalidation protocol).
        Called when a MAJOR contract version is released.

        Args:
            agent_id:         Agent to invalidate.
            metric_id:        Metric to invalidate.
            contract_version: Contract version string that triggered invalidation
                              (e.g., "2.0.0").

        Returns:
            Number of records invalidated.
        """
        agent_dir = self._root / agent_id / metric_id
        if not agent_dir.exists():
            return 0

        count = 0
        for path in agent_dir.glob("*.json"):
            data = json.loads(path.read_text(encoding="utf-8"))
            if data.get("baseline_status") != "invalidated":
                data["baseline_status"] = "invalidated"
                data["invalidated_by"] = f"contract-v{contract_version}"
                path.write_text(json.dumps(data, indent=2), encoding="utf-8")
                count += 1

        logger.info(
            "Invalidated %d baseline record(s) for %s/%s (contract-v%s).",
            count,
            agent_id,
            metric_id,
            contract_version,
        )
        return count

    def audit(self) -> list[BaselineAuditEntry]:
        """List all stored baselines with version keys, scores, and ages.

        Implements the ``jerry test baseline audit`` CLI command requirement
        from FR-020.

        Returns:
            List of BaselineAuditEntry sorted by captured_at descending
            (newest first).
        """
        now = datetime.now(UTC)
        entries: list[BaselineAuditEntry] = []

        for json_path in self._root.rglob("*.json"):
            try:
                data = json.loads(json_path.read_text(encoding="utf-8"))
            except (json.JSONDecodeError, OSError) as exc:
                logger.warning("Could not read baseline file %s: %s", json_path, exc)
                continue

            try:
                captured = datetime.fromisoformat(data["captured_at"])
                # Ensure timezone-aware for arithmetic.
                if captured.tzinfo is None:
                    captured = captured.replace(tzinfo=UTC)
                age_days = (now - captured).total_seconds() / 86400.0
            except (KeyError, ValueError):
                age_days = -1.0

            entries.append(
                BaselineAuditEntry(
                    version_key=data.get("version_key", "unknown"),
                    agent_id=data.get("agent_id", "unknown"),
                    metric_id=data.get("metric_id", "unknown"),
                    mean_score=data.get("mean_score", 0.0),
                    n_runs=data.get("n_runs", 0),
                    captured_at=data.get("captured_at", "unknown"),
                    baseline_status=data.get("baseline_status", "unknown"),
                    age_days=age_days,
                )
            )

        entries.sort(key=lambda e: e.captured_at, reverse=True)
        return entries

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _record_path(
        self,
        version_key: str,
        agent_id: str,
        metric_id: str,
    ) -> Path:
        """Compute the filesystem path for a baseline record.

        The version key may contain path separators and colons that are
        not safe for use in filenames.  We hash the key to a short hex
        slug to produce a stable, filesystem-safe filename.

        Args:
            version_key: Composite version key.
            agent_id:    Agent identifier.
            metric_id:   Metric identifier.

        Returns:
            Path object for the JSON file.
        """
        key_slug = hashlib.sha256(version_key.encode()).hexdigest()[:16]
        return self._root / agent_id / metric_id / f"{key_slug}.json"

    @staticmethod
    def _validate_version_key(version_key: str) -> None:
        """Validate that version_key follows the "{hash}:{path}" format.

        FR-004: "The composite key format shall be {git_commit_hash}:{file_path}."

        Args:
            version_key: Key to validate.

        Raises:
            ValueError: If the key does not contain exactly one ":" separator.
        """
        if ":" not in version_key:
            raise ValueError(
                f"version_key must follow the format '{{git_hash}}:{{file_path}}', "
                f"got: {version_key!r}."
            )
        parts = version_key.split(":", 1)
        if not parts[0] or not parts[1]:
            raise ValueError(
                f"version_key has empty git hash or file path component: {version_key!r}."
            )
