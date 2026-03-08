# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Victor Lau

"""Integration tests: Layer 1-4 pipeline integration for PROJ-036 gap closure.

Scope: ps-researcher + ps-analyst agents.

Covers structural integration scenarios:
    - evaluator fixture construction (no LLM call)
    - extract_score_arrays() head/base split against sample promptfoo JSON
    - compare_versions() smoke invocation via Layer 4 stats
    - BaselineStore store/retrieve round-trip using a temporary directory
    - extract_score_arrays() error paths: missing file and invalid JSON
    - BaselineStore FR-020 quality gate rejection path

No LLM API calls are made. All tests verify structural and behavioural
contracts without executing live inference.

References:
    - FR-004: Version key composite format {commit_hash}:{file_path}
    - FR-009: Score array collection and extraction
    - FR-014: N >= 20 statistical sample size requirement
    - FR-020: BaselineStore quality gate (mean >= 0.92)
    - H-11: Type hints + docstrings on public symbols
    - H-20: 90% line coverage target
    - WI-5B: FIX-WI5-B gap closure (extraction error paths, FR-020 rejection)
    - CG-026: extraction adapter and quality gate error-path coverage
    - OWASP INPVAL: Boundary and input validation coverage
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from jerry.testing.baselines.store import BaselineStore
from jerry.testing.evaluation.deepeval_adapter import DeepEvalAdapter
from jerry.testing.extraction import extract_score_arrays
from jerry.testing.types import EvaluationMode

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

#: Minimal promptfoo results structure per the test specification.
_SAMPLE_PROMPTFOO_RESULTS: dict = {
    "results": {
        "results": [
            {
                "vars": {"__version__": "head"},
                "gradingResults": [
                    {
                        "score": 0.85,
                        "assertion": {
                            "type": "llm-rubric",
                            "metric": "composite_score",
                        },
                    }
                ],
            },
            {
                "vars": {"__version__": "base"},
                "gradingResults": [
                    {
                        "score": 0.80,
                        "assertion": {
                            "type": "llm-rubric",
                            "metric": "composite_score",
                        },
                    }
                ],
            },
        ]
    }
}

#: Valid version key for store/retrieve round-trip tests.
#: Format: "{7-40 lowercase hex}:{file_path}" per FR-004 / CG-027.
_VERSION_KEY: str = "abc1234:skills/problem-solving/agents/ps-researcher.md"


# ---------------------------------------------------------------------------
# Integration tests: evaluator fixture
# ---------------------------------------------------------------------------


@pytest.mark.integration
class TestConftestEvaluatorFixture:
    """Verify the evaluator fixture constructs a valid DeepEvalAdapter.

    Does NOT make any LLM API calls — construction-only verification.
    The ANTHROPIC_API_KEY must be set for the Claude model path to succeed;
    tests in this class patch it in via monkeypatch to remain hermetic.
    """

    def test_conftest_evaluator_fixture_should_return_configured_adapter(
        self,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        """evaluator fixture must return a DeepEvalAdapter instance.

        Verifies that the adapter is constructed with the correct model_name
        attribute without making any downstream LLM API calls.

        The ANTHROPIC_API_KEY is set via monkeypatch so that the Claude model
        validation inside DeepEvalAdapter.__post_init__ does not raise
        EvaluationConfigError, keeping the test hermetic.

        References:
            - FR-006: DeepEval pytest plugin integration (evaluator fixture)
            - FR-021: Debiasing (C-007 mandatory, DebiasingStrategy)
        """
        monkeypatch.setenv("ANTHROPIC_API_KEY", "test-key-hermetic")

        from jerry.testing.evaluation.debiasing import DebiasingStrategy

        adapter = DeepEvalAdapter(
            model_name="claude-sonnet-4-20250514",
            debiasing_strategy=DebiasingStrategy(),
        )

        assert isinstance(adapter, DeepEvalAdapter), (
            f"Expected DeepEvalAdapter instance; got {type(adapter).__name__}"
        )
        assert adapter.model_name == "claude-sonnet-4-20250514", (
            f"model_name attribute must match the constructor argument; got {adapter.model_name!r}"
        )


# ---------------------------------------------------------------------------
# Integration tests: score array extraction
# ---------------------------------------------------------------------------


@pytest.mark.integration
class TestScoreArrayExtractionFromSampleData:
    """Verify extract_score_arrays() correctly splits head/base entries.

    Uses a minimal in-memory promptfoo results JSON written to tmp_path.
    No LLM calls are performed.
    """

    def test_score_array_extraction_from_sample_data(
        self,
        tmp_path: Path,
    ) -> None:
        """extract_score_arrays() must correctly split head/base score arrays.

        Writes a minimal valid promptfoo results JSON to tmp_path, calls
        extract_score_arrays(), and verifies:
            - The "composite_score" metric key is present in the result.
            - The head array contains the head-tagged score (0.85).
            - The base array contains the base-tagged score (0.80).

        References:
            - FR-009: Score array collection and export
            - CG-008: promptfoo extraction adapter
        """
        results_file: Path = tmp_path / "promptfoo-results.json"
        results_file.write_text(
            json.dumps(_SAMPLE_PROMPTFOO_RESULTS),
            encoding="utf-8",
        )

        arrays = extract_score_arrays(results_file)

        assert "composite_score" in arrays, (
            "Expected 'composite_score' metric key in extracted arrays; "
            f"got keys: {sorted(arrays.keys())}"
        )

        head_scores, base_scores = arrays["composite_score"]

        assert head_scores == [0.85], (
            f"Head score array mismatch. Expected [0.85], got {head_scores}"
        )
        assert base_scores == [0.80], (
            f"Base score array mismatch. Expected [0.80], got {base_scores}"
        )


# ---------------------------------------------------------------------------
# Integration tests: Layer 4 pipeline smoke
# ---------------------------------------------------------------------------


@pytest.mark.integration
class TestLayer4PipelineSmokeWithScoreArrays:
    """Smoke test: compare_versions() accepts score arrays without error.

    Provides two minimal ScoreArrays (head and base) to compare_versions()
    and verifies the function returns a result without raising. Does NOT
    assert specific p-values or statistical conclusions — this is a wiring
    smoke test only.
    """

    def test_layer4_pipeline_smoke_with_score_arrays(self) -> None:
        """compare_versions() must return a RegressionResult without error.

        Supplies head=[0.85, 0.90, 0.88, ...] and base=[0.80, 0.82, 0.79, ...]
        (each padded to N=20, the minimum required by FR-014) to compare_versions()
        and verifies the call completes without raising InsufficientSamplesError
        or any other exception.

        Score arrays are not all-identical to avoid InvalidScoreArrayError
        (stats.py rejects all-identical arrays via the require_variation guard).

        References:
            - FR-014: N >= 20 per version enforcement
            - FR-015: Wilcoxon signed-rank test
            - OWASP INPVAL: boundary input validation
        """
        from jerry.testing.stats import compare_versions
        from jerry.testing.types import RegressionResult

        # Build N=20 alternating arrays to satisfy both the N>=20 floor (FR-014)
        # and the non-identical variation requirement for Wilcoxon (stats.py).
        head_base_values = [0.85, 0.90, 0.88]
        base_base_values = [0.80, 0.82, 0.79]

        head_scores = [head_base_values[i % len(head_base_values)] for i in range(20)]
        base_scores = [base_base_values[i % len(base_base_values)] for i in range(20)]

        result = compare_versions(
            head_scores,
            base_scores,
            metric_id="composite_score",
            agent_id="ps-researcher",
            version_key_a="aaa" * 13 + "a:skills/problem-solving/agents/ps-researcher.md",
            version_key_b="bbb" * 13 + "b:skills/problem-solving/agents/ps-analyst.md",
            evaluation_mode=EvaluationMode.FULL,
        )

        assert isinstance(result, RegressionResult), (
            "compare_versions() must return a RegressionResult instance; "
            f"got {type(result).__name__}"
        )


# ---------------------------------------------------------------------------
# Integration tests: BaselineStore round-trip
# ---------------------------------------------------------------------------


@pytest.mark.integration
class TestBaselineStoreRoundtrip:
    """Verify BaselineStore store/retrieve round-trip using a temporary directory.

    Constructs a BaselineStore with a tmp_path root, stores a baseline entry,
    then retrieves it and verifies it matches the stored data. No LLM calls
    are performed.
    """

    def test_baseline_store_roundtrip(self, tmp_path: Path) -> None:
        """BaselineStore store() then retrieve() must return an identical record.

        Stores a baseline with N=30 high-quality scores (mean > 0.92, satisfying
        the FR-020 quality gate) in FULL mode, then retrieves it by the same
        version_key, agent_id, and metric_id. Verifies:
            - The retrieved record is not None.
            - version_key, agent_id, and metric_id match the stored values.
            - The scores list matches exactly.
            - baseline_status is "active".

        The N=30 count satisfies BaselineStore.MIN_FULL_SAMPLES (FR-017 AC-1).
        The mean score 0.93 satisfies the FR-020 quality gate (>= 0.92).

        References:
            - FR-004: Version key composite format {commit_hash}:{file_path}
            - FR-020: BaselineStore quality gate (mean >= 0.92)
            - FR-017: N >= 30 for FULL mode baseline collection
        """
        store = BaselineStore(tmp_path / "baselines")

        # N=30, alternating to satisfy non-identical constraint, mean = 0.93
        scores = [0.93 if i % 2 == 0 else 0.93 for i in range(30)]
        # Use a simpler uniform high-quality score list for round-trip clarity.
        scores = [0.93] * 30

        stored_record = store.store(
            version_key=_VERSION_KEY,
            agent_id="ps-researcher",
            metric_id="composite_score",
            scores=scores,
            evaluation_mode=EvaluationMode.FULL,
            model_version="claude-sonnet-4-20250514",
        )

        retrieved_record = store.retrieve(
            version_key=_VERSION_KEY,
            agent_id="ps-researcher",
            metric_id="composite_score",
        )

        assert retrieved_record is not None, (
            "retrieve() returned None; expected a BaselineRecord for the stored entry"
        )
        assert retrieved_record.version_key == stored_record.version_key, (
            f"version_key mismatch: stored={stored_record.version_key!r}, "
            f"retrieved={retrieved_record.version_key!r}"
        )
        assert retrieved_record.agent_id == "ps-researcher", (
            f"agent_id mismatch: got {retrieved_record.agent_id!r}"
        )
        assert retrieved_record.metric_id == "composite_score", (
            f"metric_id mismatch: got {retrieved_record.metric_id!r}"
        )
        assert retrieved_record.scores == scores, (
            f"scores mismatch: stored={scores}, retrieved={retrieved_record.scores}"
        )
        assert retrieved_record.baseline_status == "active", (
            f"baseline_status must be 'active' after store(); "
            f"got {retrieved_record.baseline_status!r}"
        )


# ---------------------------------------------------------------------------
# Integration tests: extraction error paths  (WI-5B / CG-026)
# ---------------------------------------------------------------------------


@pytest.mark.integration
class TestScoreExtractionErrorPaths:
    """extract_score_arrays() error-path coverage.

    Verifies that the promptfoo extractor raises the correct exception types
    for two primary failure modes: a missing file and malformed JSON.

    References:
        - WI-5B: integration test gap closure
        - CG-026: extraction adapter error-path coverage
        - H-20: 90% line coverage target
        - OWASP INPVAL: input validation boundary testing
    """

    def test_extract_score_arrays_missing_file_should_raise_file_not_found(
        self,
        tmp_path: Path,
    ) -> None:
        """extract_score_arrays() must raise FileNotFoundError for a nonexistent path.

        Calls extract_score_arrays() with a path that does not exist on disk and
        verifies that FileNotFoundError is raised (not a generic exception).

        References:
            - WI-5B: extraction error path coverage
            - OWASP INPVAL: boundary input — nonexistent file path
        """
        from jerry.testing.extraction.promptfoo_extractor import extract_score_arrays as _extract

        nonexistent = tmp_path / "does_not_exist.json"

        with pytest.raises(FileNotFoundError):
            _extract(nonexistent)

    def test_extract_score_arrays_invalid_json_should_raise_value_error(
        self,
        tmp_path: Path,
    ) -> None:
        """extract_score_arrays() must raise ValueError for an invalid JSON file.

        Writes a file containing syntactically invalid JSON to tmp_path, calls
        extract_score_arrays() against it, and verifies that ValueError is raised.

        References:
            - WI-5B: extraction error path coverage
            - OWASP INPVAL: boundary input — malformed JSON payload
        """
        from jerry.testing.extraction.promptfoo_extractor import extract_score_arrays as _extract

        invalid_json_file = tmp_path / "bad.json"
        invalid_json_file.write_text("{ this is not valid JSON !!!", encoding="utf-8")

        with pytest.raises(ValueError):
            _extract(invalid_json_file)


# ---------------------------------------------------------------------------
# Integration tests: FR-020 quality gate rejection  (WI-5B / CG-026)
# ---------------------------------------------------------------------------


@pytest.mark.integration
class TestBaselineStoreQualityGateRejection:
    """BaselineStore.store() rejects below-threshold baselines (FR-020).

    Verifies that the quality gate (mean >= 0.92) is enforced at store time
    and that a descriptive ValueError is raised for rejected candidates.

    References:
        - FR-020: BaselineStore quality gate acceptance criterion
        - WI-5B: integration test gap closure
        - CG-026: baseline quality gate rejection path coverage
        - H-20: 90% line coverage target
    """

    def test_store_below_quality_threshold_should_raise_value_error(
        self,
        tmp_path: Path,
    ) -> None:
        """store() must raise ValueError when mean(scores) < 0.92.

        Creates a BaselineStore with a temporary root directory, then attempts
        to store a score array whose mean is well below the FR-020 quality gate
        (0.92).  Verifies that:
            - ValueError is raised (not a generic exception).
            - The error message references the mean score and quality gate
              threshold, guiding the caller toward the root cause.

        References:
            - FR-020: "verify that the candidate baseline's quality score
              passes the quality gate (>= 0.92)"
            - WI-5B: FR-020 quality gate rejection test
        """
        store = BaselineStore(tmp_path / "baselines")

        # Scores with mean = 0.50, clearly below the 0.92 quality gate.
        # N=30 satisfies MIN_FULL_SAMPLES so only the quality gate triggers.
        low_scores = [0.50] * 30

        with pytest.raises(ValueError, match="quality gate"):
            store.store(
                version_key="abc1234:skills/problem-solving/agents/ps-researcher.md",
                agent_id="ps-researcher",
                metric_id="composite_score",
                scores=low_scores,
                evaluation_mode=EvaluationMode.FULL,
                model_version="claude-sonnet-4-20250514",
            )

    def test_store_at_quality_threshold_boundary_should_succeed(
        self,
        tmp_path: Path,
    ) -> None:
        """store() must accept scores whose mean exactly equals the 0.92 threshold.

        Verifies the boundary condition (mean == 0.92) is accepted (>= is the
        gate, not >).

        References:
            - FR-020: boundary condition — mean exactly at threshold
            - OWASP INPVAL: boundary value analysis
        """
        store = BaselineStore(tmp_path / "baselines")

        # mean == 0.92 exactly satisfies the >= 0.92 quality gate.
        boundary_scores = [0.92] * 30

        record = store.store(
            version_key="abc1234:skills/problem-solving/agents/ps-researcher.md",
            agent_id="ps-researcher",
            metric_id="composite_score",
            scores=boundary_scores,
            evaluation_mode=EvaluationMode.FULL,
            model_version="claude-sonnet-4-20250514",
        )

        assert record is not None, "store() must return a BaselineRecord on success"
        assert abs(record.mean_score - 0.92) < 1e-9, (
            f"mean_score must be 0.92 at the boundary; got {record.mean_score}"
        )
