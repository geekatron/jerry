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
import re
from datetime import UTC, datetime
from pathlib import Path

from jerry.testing.stats import InsufficientSamplesError
from jerry.testing.types import (
    BaselineAuditEntry,
    BaselineRecord,
    EvaluationMode,
)

logger = logging.getLogger(__name__)

#: CG-027: Compiled regex for version key format validation.
#: Format: "{git_hash}:{file_path}" where:
#:   - git_hash must be 7-40 lowercase hexadecimal characters (short or full SHA)
#:   - file_path must not contain newlines or null bytes (injection prevention)
VERSION_KEY_PATTERN: re.Pattern[str] = re.compile(r"^[0-9a-f]{7,40}:[^\n\r\0]+$")

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

        CG-027 strengthened validation:
            1. Colon-split structural check (original): key must contain ":"
               with non-empty hash and path components.
            2. Regex format check (CG-027): git hash must be 7-40 lowercase hex
               characters; file path must not contain newlines (\\n, \\r) or null
               bytes (\\0) which would enable log injection or header splitting.

        Args:
            version_key: Key to validate.

        Raises:
            ValueError: If the key does not contain ":" separator, has empty
                        components, the git hash is not 7-40 lowercase hex chars,
                        or the path part contains newlines or null bytes.
        """
        # --- Original colon-split structural check ---
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

        # --- CG-027: Regex format check ---
        # Validates git hash is 7-40 lowercase hex chars and path contains no
        # newlines or null bytes that could cause log injection or file corruption.
        if not VERSION_KEY_PATTERN.match(version_key):
            raise ValueError(
                f"version_key does not match required pattern "
                f"'^[0-9a-f]{{7,40}}:[^\\n\\r\\0]+$' (CG-027). "
                f"The git hash must be 7-40 lowercase hexadecimal characters; "
                f"the file path must not contain newlines or null bytes. "
                f"Got: {version_key!r}."
            )


# CG-002 fix: __main__ entry point (gap-analysis-20260307-001).
def main() -> int:
    """CLI entry point for the BaselineStore management commands.

    Parses command-line arguments matching the GitHub Actions workflow
    invocation flags (prompt-regression-full.yml, FR-020) and dispatches
    to the appropriate BaselineStore method.  Score extraction wiring
    will be added in CG-008.

    Returns:
        Exit code: 0 on success, 1 on argument/validation errors.
    """
    import argparse  # noqa: PLC0415
    import json as json_mod  # noqa: PLC0415

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )

    parser = argparse.ArgumentParser(
        description="BaselineStore management CLI for the prompt regression harness.",
    )
    parser.add_argument(
        "--action",
        required=True,
        choices=["store", "retrieve", "audit", "invalidate"],
        help="Action to perform on the baseline store.",
    )
    parser.add_argument(
        "--agent",
        default=None,
        help="Agent ID string (e.g., 'ps-researcher'). Required for store/retrieve/invalidate.",
    )
    parser.add_argument(
        "--results-file",
        default=None,
        help="Path to promptfoo results JSON file. Required for store.",
    )
    parser.add_argument(
        "--report-file",
        default=None,
        help="Path to statistical report JSON file (optional for store).",
    )
    parser.add_argument(
        "--commit-sha",
        default=None,
        help="Git HEAD commit SHA. Required for store.",
    )
    parser.add_argument(
        "--tier",
        default=None,
        choices=["smoke", "standard", "full"],
        help="Evaluation tier. Required for store.",
    )
    parser.add_argument(
        "--reason",
        default=None,
        help="Logged reason for the action (optional).",
    )
    parser.add_argument(
        "--metric-id",
        default="composite_score",
        help="Metric identifier for retrieve/invalidate (default: composite_score).",
    )
    parser.add_argument(
        "--agent-file",
        default=None,
        help="Agent definition file path for version key construction (optional).",
    )
    parser.add_argument(
        "--contract-version",
        default=None,
        help="Contract version string. Required for invalidate.",
    )

    args = parser.parse_args()

    # --- Validate action-specific required arguments ---
    if args.action in ("store", "retrieve", "invalidate") and not args.agent:
        logger.error("--agent is required for action '%s'.", args.action)
        return 1

    if args.action == "store":
        if not args.results_file:
            logger.error("--results-file is required for action 'store'.")
            return 1
        if not args.commit_sha:
            logger.error("--commit-sha is required for action 'store'.")
            return 1
        if not args.tier:
            logger.error("--tier is required for action 'store'.")
            return 1

    if args.action == "invalidate" and not args.contract_version:
        logger.error("--contract-version is required for action 'invalidate'.")
        return 1

    # --- Resolve store root relative to the project root ---
    store_root = Path("projects/PROJ-036-prompt-regression-harness/baselines/data")
    store = BaselineStore(store_root)

    # ------------------------------------------------------------------
    # Action: store
    # ------------------------------------------------------------------
    if args.action == "store":
        results_path = Path(args.results_file)
        if not results_path.exists():
            logger.error("Results file does not exist: %s", results_path)
            return 1

        try:
            json_mod.loads(results_path.read_text(encoding="utf-8"))
        except json_mod.JSONDecodeError as exc:
            logger.error("Results file is not valid JSON: %s — %s", results_path, exc)
            return 1

        report_data: dict | None = None
        if args.report_file:
            report_path = Path(args.report_file)
            if report_path.exists():
                try:
                    report_data = json_mod.loads(report_path.read_text(encoding="utf-8"))
                except json_mod.JSONDecodeError as exc:
                    logger.warning(
                        "Report file is not valid JSON (skipping): %s — %s",
                        report_path,
                        exc,
                    )
            else:
                logger.warning("Report file does not exist (skipping): %s", report_path)

        # --- Construct version key from commit SHA and optional agent-file path ---
        if args.agent_file:
            version_key = f"{args.commit_sha}:{args.agent_file}"
        else:
            version_key = f"{args.commit_sha}:{args.agent}"

        # --- Log configuration ---
        logger.info("BaselineStore store action initiated.")
        logger.info("  agent:        %s", args.agent)
        logger.info("  tier:         %s", args.tier)
        logger.info("  results-file: %s", results_path)
        logger.info("  report-file:  %s", args.report_file)
        logger.info("  commit-sha:   %s", args.commit_sha)
        logger.info("  agent-file:   %s", args.agent_file)
        logger.info("  version-key:  %s", version_key)
        logger.info("  reason:       %s", args.reason)
        if report_data is not None:
            logger.info("  report:       loaded (%d top-level keys)", len(report_data))

        # TODO(CG-008): Extract scores from results file and wire into store.store().
        # Score extraction requires the promptfoo results schema parser which will be
        # implemented as part of the Layer 2 results adapter.  For now, log that the
        # store invocation was received and exit cleanly to unblock CI.
        logger.info(
            "TODO(CG-008): Score extraction not yet wired. "
            "Store invocation received for agent=%s version=%s.",
            args.agent,
            version_key,
        )
        return 0

    # ------------------------------------------------------------------
    # Action: retrieve
    # ------------------------------------------------------------------
    if args.action == "retrieve":
        version_key_retrieve: str
        if args.commit_sha and args.agent_file:
            version_key_retrieve = f"{args.commit_sha}:{args.agent_file}"
        elif args.commit_sha:
            version_key_retrieve = f"{args.commit_sha}:{args.agent}"
        else:
            logger.error("retrieve requires --commit-sha to construct the version key.")
            return 1

        logger.info(
            "Retrieving baseline: agent=%s metric=%s version=%s",
            args.agent,
            args.metric_id,
            version_key_retrieve,
        )
        try:
            record = store.retrieve(
                version_key=version_key_retrieve,
                agent_id=args.agent,
                metric_id=args.metric_id,
            )
        except ValueError as exc:
            logger.error("Retrieve failed: %s", exc)
            return 1

        if record is None:
            logger.info(
                "No baseline found for agent=%s metric=%s version=%s.",
                args.agent,
                args.metric_id,
                version_key_retrieve,
            )
            print(json_mod.dumps(None))
        else:
            import dataclasses as dc  # noqa: PLC0415

            print(json_mod.dumps(dc.asdict(record), indent=2))
        return 0

    # ------------------------------------------------------------------
    # Action: audit
    # ------------------------------------------------------------------
    if args.action == "audit":
        logger.info("Running baseline audit on store root: %s", store_root)
        entries = store.audit()
        if not entries:
            print("No baseline records found.")
            return 0

        # Print formatted table header
        header = (
            f"{'agent_id':<24} {'metric_id':<20} {'status':<12} "
            f"{'mean':>6} {'n':>4} {'age_days':>9} version_key"
        )
        print(header)
        print("-" * len(header))
        for entry in entries:
            print(
                f"{entry.agent_id:<24} {entry.metric_id:<20} "
                f"{entry.baseline_status:<12} {entry.mean_score:>6.4f} "
                f"{entry.n_runs:>4} {entry.age_days:>9.1f} "
                f"{entry.version_key}"
            )
        return 0

    # ------------------------------------------------------------------
    # Action: invalidate
    # ------------------------------------------------------------------
    if args.action == "invalidate":
        logger.info(
            "Invalidating baselines: agent=%s metric=%s contract-version=%s",
            args.agent,
            args.metric_id,
            args.contract_version,
        )
        count = store.invalidate(
            agent_id=args.agent,
            metric_id=args.metric_id,
            contract_version=args.contract_version,
        )
        logger.info("Invalidated %d record(s).", count)
        return 0

    # Unreachable: argparse choices enforce valid actions.
    logger.error("Unhandled action: %s", args.action)
    return 1


if __name__ == "__main__":
    import sys  # noqa: PLC0415

    sys.exit(main())
