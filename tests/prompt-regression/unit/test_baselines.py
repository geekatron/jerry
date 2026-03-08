# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Victor Lau

"""Unit tests for jerry.testing.baselines.store — BaselineStore.

Tests all public methods of BaselineStore:
    - store(): round-trip persistence with quality gate enforcement
    - retrieve(): record retrieval and invalidated-record rejection
    - audit(): listing of stored baselines (FR-020)
    - invalidate(): marking records as invalidated

All tests use a temporary directory (tmp_path fixture) for isolation.
No LLM calls are performed.

FR-020 traceability: The audit() method directly satisfies FR-020 acceptance
criterion "The system shall provide a `jerry test baseline audit` CLI command
that lists all stored baselines with their version keys, mean scores, and ages."
Tests in TestBaselineStoreAudit cover: empty store, single-entry listing,
multi-agent listing, age_days field presence, and entry type validation.

References:
    - CG-002: BaselineStore persistence and quality gate requirements
    - CG-027: VERSION_KEY_PATTERN regex for version key format validation
    - FR-004: Version key format {commit_hash}:{file_path}
    - FR-020: Baseline quality gate (mean >= 0.92) and audit CLI command
    - FR-014: N >= 30 for FULL mode baselines (MIN_FULL_SAMPLES)
    - H-20: 90% line coverage target
"""

from __future__ import annotations

from pathlib import Path

import pytest

from jerry.testing.baselines.store import BaselineStore
from jerry.testing.evaluation.debiasing import DebiasingStrategy
from jerry.testing.evaluation.deepeval_adapter import DeepEvalAdapter
from jerry.testing.evaluation.exceptions import EvaluationConfigError
from jerry.testing.stats import InsufficientSamplesError
from jerry.testing.types import (
    BaselineAuditEntry,
    BaselineRecord,
    EvaluationMode,
)

pytestmark = [pytest.mark.unit]

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def store(tmp_path: Path) -> BaselineStore:
    """Return a BaselineStore backed by a temporary directory."""
    return BaselineStore(tmp_path / "baselines")


# ---------------------------------------------------------------------------
# Helper constants
# ---------------------------------------------------------------------------

# CG-027: VERSION_KEY_PATTERN requires 7+ lowercase hex chars before the colon.
# BaselineStore uses this relaxed format (any 7+ hex chars) for storage keys.
_VALID_VERSION_KEY = "abc1234:skills/ps-researcher.md"
# FR-004 full format: {7+ hex commit hash}:{repo-relative file path}
# VersionKey (test_version_keys.py) enforces a stricter 40-char SHA-1;
# BaselineStore uses CG-027 relaxed format (7+ hex chars), not FR-004 full SHA-1.
_FULL_VALID_VERSION_KEY = "a1b2c3d4e5f6789:skills/ps-researcher.md"

# A full set of 30 high-quality scores for FULL mode baselines
_FULL_GOOD_SCORES: list[float] = [0.93 if i % 2 == 0 else 0.95 for i in range(30)]

# A full set of 30 low-quality scores (below the 0.92 gate)
_FULL_BAD_SCORES: list[float] = [0.85 if i % 2 == 0 else 0.88 for i in range(30)]


# ---------------------------------------------------------------------------
# store() — primary persistence method
# ---------------------------------------------------------------------------


class TestBaselineStoreStore:
    """Tests for BaselineStore.store() — covers CG-002 persistence requirements."""

    def test_store_and_retrieve_should_round_trip(self, store: BaselineStore) -> None:
        """Storing and retrieving a record should return equivalent data."""
        store.store(
            version_key=_VALID_VERSION_KEY,
            agent_id="ps-researcher",
            metric_id="composite_score",
            scores=_FULL_GOOD_SCORES,
            evaluation_mode=EvaluationMode.FULL,
            model_version="claude-sonnet-4",
        )
        retrieved = store.retrieve(
            version_key=_VALID_VERSION_KEY,
            agent_id="ps-researcher",
            metric_id="composite_score",
        )
        assert retrieved is not None
        assert retrieved.version_key == _VALID_VERSION_KEY
        assert retrieved.agent_id == "ps-researcher"
        assert retrieved.metric_id == "composite_score"
        assert retrieved.scores == _FULL_GOOD_SCORES
        assert retrieved.n_runs == 30

    def test_store_should_return_baseline_record(self, store: BaselineStore) -> None:
        """store() should return a BaselineRecord object."""
        record = store.store(
            version_key=_VALID_VERSION_KEY,
            agent_id="ps-researcher",
            metric_id="composite_score",
            scores=_FULL_GOOD_SCORES,
            evaluation_mode=EvaluationMode.FULL,
            model_version="claude-sonnet-4",
        )
        assert isinstance(record, BaselineRecord)

    def test_store_full_mode_min_samples_should_reject_insufficient_count(
        self, store: BaselineStore
    ) -> None:
        """FULL mode baseline with N < 30 should raise InsufficientSamplesError."""
        too_few = [0.93] * 10  # Only 10 scores, FULL needs >= 30
        with pytest.raises(InsufficientSamplesError) as exc_info:
            store.store(
                version_key=_VALID_VERSION_KEY,
                agent_id="ps-researcher",
                metric_id="composite_score",
                scores=too_few,
                evaluation_mode=EvaluationMode.FULL,
                model_version="claude-sonnet-4",
            )
        assert "FULL" in str(exc_info.value) or "30" in str(exc_info.value)

    def test_store_should_reject_scores_below_quality_gate(self, store: BaselineStore) -> None:
        """Baseline with mean score < 0.92 should raise ValueError."""
        with pytest.raises(ValueError) as exc_info:
            store.store(
                version_key=_VALID_VERSION_KEY,
                agent_id="ps-researcher",
                metric_id="composite_score",
                scores=_FULL_BAD_SCORES,
                evaluation_mode=EvaluationMode.FULL,
                model_version="claude-sonnet-4",
            )
        assert "quality gate" in str(exc_info.value).lower() or "0.92" in str(exc_info.value)

    def test_store_should_reject_version_key_without_colon(self, store: BaselineStore) -> None:
        """Version key without colon separator should raise ValueError."""
        with pytest.raises(ValueError):
            store.store(
                version_key="no-colon-here",
                agent_id="ps-researcher",
                metric_id="composite_score",
                scores=_FULL_GOOD_SCORES,
                evaluation_mode=EvaluationMode.FULL,
                model_version="claude-sonnet-4",
            )

    def test_store_should_reject_version_key_with_empty_parts(self, store: BaselineStore) -> None:
        """Version key with empty hash or path should raise ValueError."""
        with pytest.raises(ValueError):
            store.store(
                version_key=":skills/ps-researcher.md",
                agent_id="ps-researcher",
                metric_id="composite_score",
                scores=_FULL_GOOD_SCORES,
                evaluation_mode=EvaluationMode.FULL,
                model_version="claude-sonnet-4",
            )

    def test_store_should_reject_empty_scores(self, store: BaselineStore) -> None:
        """Empty scores list should raise ValueError."""
        with pytest.raises(ValueError):
            store.store(
                version_key=_VALID_VERSION_KEY,
                agent_id="ps-researcher",
                metric_id="composite_score",
                scores=[],
                evaluation_mode=EvaluationMode.FULL,
                model_version="claude-sonnet-4",
            )

    def test_store_standard_mode_should_not_enforce_min_samples(self, store: BaselineStore) -> None:
        """STANDARD mode should not enforce N >= 30 (but still enforces quality gate)."""
        standard_scores = [0.93 if i % 2 == 0 else 0.94 for i in range(10)]
        record = store.store(
            version_key=_VALID_VERSION_KEY,
            agent_id="ps-researcher",
            metric_id="composite_score",
            scores=standard_scores,
            evaluation_mode=EvaluationMode.STANDARD,
            model_version="claude-sonnet-4",
        )
        assert record is not None
        assert record.n_runs == 10

    def test_store_should_create_directory_structure(
        self, store: BaselineStore, tmp_path: Path
    ) -> None:
        """store() should create the directory structure for the agent/metric."""
        store.store(
            version_key=_VALID_VERSION_KEY,
            agent_id="ps-analyst",
            metric_id="completeness",
            scores=_FULL_GOOD_SCORES,
            evaluation_mode=EvaluationMode.FULL,
            model_version="claude-sonnet-4",
        )
        expected_dir = tmp_path / "baselines" / "ps-analyst" / "completeness"
        assert expected_dir.exists()
        json_files = list(expected_dir.glob("*.json"))
        assert len(json_files) == 1


# ---------------------------------------------------------------------------
# retrieve() — record retrieval
# ---------------------------------------------------------------------------


class TestBaselineStoreRetrieve:
    """Tests for BaselineStore.retrieve() — covers CG-002 retrieval requirements."""

    def test_retrieve_should_return_none_when_not_found(self, store: BaselineStore) -> None:
        """Retrieving a non-existent baseline should return None."""
        result = store.retrieve(
            version_key="a1b2c3d:key",
            agent_id="unknown-agent",
            metric_id="composite_score",
        )
        assert result is None

    def test_retrieve_should_raise_for_invalidated_record(self, store: BaselineStore) -> None:
        """Retrieving an invalidated record should raise ValueError."""
        # First store a valid baseline
        store.store(
            version_key=_VALID_VERSION_KEY,
            agent_id="ps-researcher",
            metric_id="composite_score",
            scores=_FULL_GOOD_SCORES,
            evaluation_mode=EvaluationMode.FULL,
            model_version="claude-sonnet-4",
        )
        # Then invalidate it
        store.invalidate("ps-researcher", "composite_score", "2.0.0")
        # Now retrieve should raise
        with pytest.raises(ValueError) as exc_info:
            store.retrieve(
                version_key=_VALID_VERSION_KEY,
                agent_id="ps-researcher",
                metric_id="composite_score",
            )
        assert "invalidated" in str(exc_info.value).lower()

    def test_retrieve_should_preserve_evaluation_mode(self, store: BaselineStore) -> None:
        """Retrieved record should preserve the evaluation_mode used when stored."""
        store.store(
            version_key=_VALID_VERSION_KEY,
            agent_id="ps-researcher",
            metric_id="composite_score",
            scores=_FULL_GOOD_SCORES,
            evaluation_mode=EvaluationMode.FULL,
            model_version="claude-sonnet-4",
        )
        retrieved = store.retrieve(
            version_key=_VALID_VERSION_KEY,
            agent_id="ps-researcher",
            metric_id="composite_score",
        )
        assert retrieved is not None
        assert retrieved.evaluation_mode == EvaluationMode.FULL


# ---------------------------------------------------------------------------
# audit() — listing
# ---------------------------------------------------------------------------


class TestBaselineStoreAudit:
    """Tests for BaselineStore.audit() — covers CG-002 audit requirements (FR-020)."""

    def test_audit_should_return_empty_list_for_empty_store(self, store: BaselineStore) -> None:
        """Auditing an empty store should return an empty list."""
        entries = store.audit()
        assert entries == []

    def test_audit_should_return_entries_for_stored_baselines(self, store: BaselineStore) -> None:
        """Audit should return one entry per stored baseline."""
        store.store(
            version_key=_VALID_VERSION_KEY,
            agent_id="ps-researcher",
            metric_id="composite_score",
            scores=_FULL_GOOD_SCORES,
            evaluation_mode=EvaluationMode.FULL,
            model_version="claude-sonnet-4",
        )
        entries = store.audit()
        assert len(entries) == 1
        assert entries[0].agent_id == "ps-researcher"
        assert entries[0].metric_id == "composite_score"

    def test_audit_should_return_baseline_audit_entry_type(self, store: BaselineStore) -> None:
        """Audit entries should be BaselineAuditEntry instances."""
        store.store(
            version_key=_VALID_VERSION_KEY,
            agent_id="ps-analyst",
            metric_id="completeness",
            scores=_FULL_GOOD_SCORES,
            evaluation_mode=EvaluationMode.FULL,
            model_version="claude-sonnet-4",
        )
        entries = store.audit()
        assert all(isinstance(e, BaselineAuditEntry) for e in entries)

    def test_audit_should_list_all_baselines_across_agents(self, store: BaselineStore) -> None:
        """Audit should list all stored baselines across multiple agents."""
        store.store(
            version_key="a1b2c3d:path1",
            agent_id="ps-researcher",
            metric_id="composite_score",
            scores=_FULL_GOOD_SCORES,
            evaluation_mode=EvaluationMode.FULL,
            model_version="claude-sonnet-4",
        )
        store.store(
            version_key="e4f5a6b:path2",
            agent_id="ps-analyst",
            metric_id="completeness",
            scores=_FULL_GOOD_SCORES,
            evaluation_mode=EvaluationMode.FULL,
            model_version="claude-sonnet-4",
        )
        entries = store.audit()
        assert len(entries) == 2
        agent_ids = {e.agent_id for e in entries}
        assert "ps-researcher" in agent_ids
        assert "ps-analyst" in agent_ids

    def test_audit_should_include_age_days_float(self, store: BaselineStore) -> None:
        """Audit entries should include an age_days float."""
        store.store(
            version_key=_VALID_VERSION_KEY,
            agent_id="ps-researcher",
            metric_id="composite_score",
            scores=_FULL_GOOD_SCORES,
            evaluation_mode=EvaluationMode.FULL,
            model_version="claude-sonnet-4",
        )
        entries = store.audit()
        assert isinstance(entries[0].age_days, float)


# ---------------------------------------------------------------------------
# invalidate() — marking records as invalidated
# ---------------------------------------------------------------------------


class TestBaselineStoreInvalidate:
    """Tests for BaselineStore.invalidate() — covers CG-002 invalidation requirements."""

    def test_invalidate_should_remove_baseline_from_active_access(
        self, store: BaselineStore
    ) -> None:
        """Invalidated record should not be retrievable without ValueError."""
        store.store(
            version_key=_VALID_VERSION_KEY,
            agent_id="ps-researcher",
            metric_id="composite_score",
            scores=_FULL_GOOD_SCORES,
            evaluation_mode=EvaluationMode.FULL,
            model_version="claude-sonnet-4",
        )
        count = store.invalidate("ps-researcher", "composite_score", "2.0.0")
        assert count == 1
        with pytest.raises(ValueError):
            store.retrieve(
                version_key=_VALID_VERSION_KEY,
                agent_id="ps-researcher",
                metric_id="composite_score",
            )

    def test_invalidate_should_return_count_of_marked_records(self, store: BaselineStore) -> None:
        """invalidate() should return the number of records marked."""
        store.store(
            version_key="a1b2c3d:p1",
            agent_id="ps-analyst",
            metric_id="completeness",
            scores=_FULL_GOOD_SCORES,
            evaluation_mode=EvaluationMode.FULL,
            model_version="claude-sonnet-4",
        )
        store.store(
            version_key="e4f5a6b:p2",
            agent_id="ps-analyst",
            metric_id="completeness",
            scores=_FULL_GOOD_SCORES,
            evaluation_mode=EvaluationMode.FULL,
            model_version="claude-sonnet-4",
        )
        count = store.invalidate("ps-analyst", "completeness", "2.0.0")
        assert count == 2

    def test_invalidate_should_return_zero_for_nonexistent_agent(
        self, store: BaselineStore
    ) -> None:
        """Invalidating an agent/metric that doesn't exist should return 0."""
        count = store.invalidate("nonexistent-agent", "nonexistent-metric", "1.0.0")
        assert count == 0

    def test_invalidate_should_not_double_count_already_invalidated_records(
        self, store: BaselineStore
    ) -> None:
        """Calling invalidate twice should only count records once."""
        store.store(
            version_key=_VALID_VERSION_KEY,
            agent_id="ps-researcher",
            metric_id="composite_score",
            scores=_FULL_GOOD_SCORES,
            evaluation_mode=EvaluationMode.FULL,
            model_version="claude-sonnet-4",
        )
        count_first = store.invalidate("ps-researcher", "composite_score", "2.0.0")
        count_second = store.invalidate("ps-researcher", "composite_score", "2.0.0")
        assert count_first == 1
        assert count_second == 0  # already invalidated, not counted again


# ---------------------------------------------------------------------------
# Evaluator fixture contract — EvaluationConfigError on missing API key
# ---------------------------------------------------------------------------


class TestEvaluatorFixtureContract:
    """Evaluator construction contract: EvaluationConfigError on missing ANTHROPIC_API_KEY.

    Verifies the fail-fast principle (CG-005, OWASP AUTHN): the DeepEvalAdapter
    must raise EvaluationConfigError during __post_init__ when ANTHROPIC_API_KEY
    is absent for a Claude model, not defer the failure to the first LLM call.

    References:
        - CG-005: Typed exception hierarchy + pre-batch health check
        - FR-006: DeepEval pytest plugin integration (evaluator fixture)
        - OWASP AUTHN: Authentication configuration validation at initialization
    """

    def test_evaluator_fixture_should_raise_on_missing_api_key(
        self, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        """DeepEvalAdapter with a Claude model should raise EvaluationConfigError
        when ANTHROPIC_API_KEY is not set.

        Removes ANTHROPIC_API_KEY from the environment via monkeypatch to
        simulate a misconfigured CI environment, then verifies that adapter
        construction fails with EvaluationConfigError during __post_init__
        rather than silently deferring the failure to the first LLM call.

        OWASP AUTHN: Authentication configuration errors must be surfaced at
        construction time to prevent misleading downstream failures (e.g.,
        silent 0.0 score arrays in the evaluation batch).

        References:
            - CG-005: Typed exception hierarchy + pre-batch health check
            - FR-006: DeepEval pytest plugin integration (evaluator fixture)
        """
        monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)

        with pytest.raises(EvaluationConfigError) as exc_info:
            DeepEvalAdapter(
                model_name="claude-sonnet-4-20250514",
                debiasing_strategy=DebiasingStrategy(),
            )

        raised = exc_info.value
        assert "ANTHROPIC_API_KEY" in str(raised), (
            "EvaluationConfigError message must mention ANTHROPIC_API_KEY "
            f"to guide the user toward remediation; got: {raised!r}"
        )
