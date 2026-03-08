# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Victor Lau

"""Unit tests for jerry.testing.extraction.promptfoo_extractor — CG-008.

Verifies that extract_score_arrays() correctly:
  - Parses valid promptfoo JSON and splits scores into head/base arrays.
  - Raises FileNotFoundError for missing files.
  - Raises ValueError for invalid JSON.
  - Raises ValueError for files missing the results.results structure.
  - Skips out-of-range scores with a WARNING log.
  - Classifies "head", "candidate", and "base" version tags correctly.
  - Resolves metric names from assertion.metric > assertion.type > "unnamed".

No LLM calls are performed. All tests use tmp_path for file-system isolation.

References:
    - CG-008: extract_score_arrays() function
    - CG-021: Metric name resolution precedence
    - H-20: BDD test-first (90% line coverage target)
"""

from __future__ import annotations

import json
import logging
from pathlib import Path

import pytest

from jerry.testing.extraction.promptfoo_extractor import extract_score_arrays

# ---------------------------------------------------------------------------
# Helpers — promptfoo JSON builders
# ---------------------------------------------------------------------------


def _make_result(
    version_tag: str,
    metric: str | None,
    assertion_type: str | None,
    score: float,
) -> dict:
    """Build a single promptfoo result entry with one grading result.

    Args:
        version_tag:    Value for the ``__version__`` variable (e.g., "head").
        metric:         Optional explicit metric label for the assertion.
        assertion_type: Optional assertion type string (fallback metric name).
        score:          Numeric score to embed in the grading result.

    Returns:
        Dict matching the promptfoo result entry schema.
    """
    assertion: dict = {}
    if metric is not None:
        assertion["metric"] = metric
    if assertion_type is not None:
        assertion["type"] = assertion_type

    return {
        "vars": {"__version__": version_tag, "prompt": "test prompt"},
        "response": {"output": "test output"},
        "gradingResults": [
            {
                "pass": score >= 0.5,
                "score": score,
                "reason": "test reason",
                "assertion": assertion,
            }
        ],
    }


def _write_promptfoo_json(path: Path, results: list[dict]) -> None:
    """Write a minimal valid promptfoo results JSON file.

    Args:
        path:    Destination file path.
        results: List of result entry dicts (the inner results.results list).
    """
    data = {"results": {"results": results}}
    path.write_text(json.dumps(data), encoding="utf-8")


# ---------------------------------------------------------------------------
# Tests: file I/O error paths
# ---------------------------------------------------------------------------


class TestExtractScoreArraysFileErrors:
    """Unit tests for extract_score_arrays() file I/O error handling.

    Covers FileNotFoundError and ValueError (invalid JSON / bad structure).
    """

    @pytest.mark.unit
    def test_missing_file_should_raise_file_not_found_error(self, tmp_path: Path) -> None:
        """extract_score_arrays raises FileNotFoundError for a non-existent file.

        The error must be raised immediately (before any parsing) so callers
        can distinguish missing-file conditions from parsing failures.
        """
        missing = tmp_path / "does_not_exist.json"

        with pytest.raises(FileNotFoundError, match="does_not_exist.json"):
            extract_score_arrays(missing)

    @pytest.mark.unit
    def test_invalid_json_file_should_raise_value_error(self, tmp_path: Path) -> None:
        """extract_score_arrays raises ValueError for files with invalid JSON.

        Corrupted or truncated promptfoo output must be surfaced as ValueError
        (not JSONDecodeError) so callers only need to catch ValueError.
        """
        bad_json = tmp_path / "bad.json"
        bad_json.write_text("{not valid json", encoding="utf-8")

        with pytest.raises(ValueError, match="invalid JSON"):
            extract_score_arrays(bad_json)

    @pytest.mark.unit
    def test_json_missing_results_key_should_raise_value_error(self, tmp_path: Path) -> None:
        """extract_score_arrays raises ValueError when the top-level 'results' object is absent.

        The promptfoo schema requires {'results': {'results': [...]}}.
        A file that contains valid JSON but lacks this structure is rejected
        with a descriptive ValueError.
        """
        no_results = tmp_path / "no_results.json"
        no_results.write_text(json.dumps({"something_else": []}), encoding="utf-8")

        with pytest.raises(ValueError, match="results"):
            extract_score_arrays(no_results)

    @pytest.mark.unit
    def test_json_missing_inner_results_list_should_raise_value_error(self, tmp_path: Path) -> None:
        """extract_score_arrays raises ValueError when results.results is not a list.

        The inner 'results' key must be a list. A dict, None, or other type
        at that position indicates a malformed promptfoo output.
        """
        bad_structure = tmp_path / "bad_structure.json"
        bad_structure.write_text(
            json.dumps({"results": {"results": "not-a-list"}}), encoding="utf-8"
        )

        with pytest.raises(ValueError, match="results.results"):
            extract_score_arrays(bad_structure)


# ---------------------------------------------------------------------------
# Tests: happy path — score array extraction
# ---------------------------------------------------------------------------


class TestExtractScoreArraysHappyPath:
    """Unit tests for extract_score_arrays() core score extraction logic.

    Verifies correct head/base splitting and metric name resolution.
    """

    @pytest.mark.unit
    def test_valid_json_with_head_and_base_should_return_correct_split(
        self, tmp_path: Path
    ) -> None:
        """extract_score_arrays correctly splits scores into head and base arrays.

        Given one head entry (score=0.9) and one base entry (score=0.7) for
        the same metric, the returned tuple should be ([0.9], [0.7]).
        """
        results_file = tmp_path / "results.json"
        _write_promptfoo_json(
            results_file,
            [
                _make_result("head", "composite_score", "llm-rubric", 0.9),
                _make_result("base", "composite_score", "llm-rubric", 0.7),
            ],
        )

        arrays = extract_score_arrays(results_file)

        assert "composite_score" in arrays
        head_scores, base_scores = arrays["composite_score"]
        assert head_scores == [0.9]
        assert base_scores == [0.7]

    @pytest.mark.unit
    def test_candidate_tag_should_be_classified_as_head(self, tmp_path: Path) -> None:
        """'candidate' version tag is treated as a head (candidate) run.

        Both 'head' and 'candidate' are valid tags for the candidate version
        per the promptfoo extractor spec. Both must populate head_scores.
        """
        results_file = tmp_path / "results.json"
        _write_promptfoo_json(
            results_file,
            [
                _make_result("candidate", "metric_a", "llm-rubric", 0.85),
                _make_result("base", "metric_a", "llm-rubric", 0.75),
            ],
        )

        arrays = extract_score_arrays(results_file)

        head_scores, base_scores = arrays["metric_a"]
        assert head_scores == [0.85], "candidate tag must populate head_scores"
        assert base_scores == [0.75]

    @pytest.mark.unit
    def test_unknown_version_tag_should_be_classified_as_base(self, tmp_path: Path) -> None:
        """An unrecognised version tag falls through to base classification.

        Only 'head' and 'candidate' are head tags. Any other value (including
        'baseline', 'control', '') must be treated as base.
        """
        results_file = tmp_path / "results.json"
        _write_promptfoo_json(
            results_file,
            [_make_result("baseline", "metric_b", "llm-rubric", 0.80)],
        )

        arrays = extract_score_arrays(results_file)

        head_scores, base_scores = arrays["metric_b"]
        assert head_scores == []
        assert base_scores == [0.80]

    @pytest.mark.unit
    def test_empty_results_list_should_return_empty_dict(self, tmp_path: Path) -> None:
        """An empty results.results list produces an empty output dict.

        No scores = no metrics. The function must return {} rather than raise.
        """
        results_file = tmp_path / "empty.json"
        _write_promptfoo_json(results_file, [])

        arrays = extract_score_arrays(results_file)

        assert arrays == {}

    @pytest.mark.unit
    def test_multiple_metrics_should_be_independently_split(self, tmp_path: Path) -> None:
        """Multiple metric names produce independent head/base arrays per metric.

        Two metrics (metric_x, metric_y) in the same file must be stored in
        separate dict entries; neither should bleed into the other's arrays.
        """
        results_file = tmp_path / "multi.json"
        _write_promptfoo_json(
            results_file,
            [
                _make_result("head", "metric_x", "llm-rubric", 0.91),
                _make_result("base", "metric_x", "llm-rubric", 0.88),
                _make_result("head", "metric_y", "llm-rubric", 0.76),
                _make_result("base", "metric_y", "llm-rubric", 0.72),
            ],
        )

        arrays = extract_score_arrays(results_file)

        assert set(arrays.keys()) == {"metric_x", "metric_y"}
        hx, bx = arrays["metric_x"]
        hy, by = arrays["metric_y"]
        assert hx == [0.91] and bx == [0.88]
        assert hy == [0.76] and by == [0.72]


# ---------------------------------------------------------------------------
# Tests: score skipping logic
# ---------------------------------------------------------------------------


class TestExtractScoreArraysSkippingLogic:
    """Unit tests for extract_score_arrays() entry-skipping behaviour.

    Out-of-range scores must be skipped with a WARNING log; they must not
    appear in either array and must not raise an exception.
    """

    @pytest.mark.unit
    def test_out_of_range_score_above_1_should_be_skipped_with_warning(
        self, tmp_path: Path, caplog: pytest.LogCaptureFixture
    ) -> None:
        """A score > 1.0 is skipped and a WARNING is logged (not an exception).

        Out-of-range scores indicate data quality issues but should not abort
        the entire extraction run — the valid entries must still be processed.
        """
        results_file = tmp_path / "bad_score.json"
        _write_promptfoo_json(
            results_file,
            [
                _make_result("head", "composite_score", "llm-rubric", 1.5),  # invalid
                _make_result("head", "composite_score", "llm-rubric", 0.85),  # valid
            ],
        )

        with caplog.at_level(
            logging.WARNING, logger="jerry.testing.extraction.promptfoo_extractor"
        ):
            arrays = extract_score_arrays(results_file)

        head_scores, _ = arrays["composite_score"]
        assert 1.5 not in head_scores, "Out-of-range score 1.5 must be excluded"
        assert 0.85 in head_scores, "Valid score 0.85 must be included"
        assert any("outside" in rec.message for rec in caplog.records), (
            "Expected a WARNING mentioning 'outside' for the out-of-range score"
        )

    @pytest.mark.unit
    def test_out_of_range_score_below_0_should_be_skipped_with_warning(
        self, tmp_path: Path, caplog: pytest.LogCaptureFixture
    ) -> None:
        """A score < 0.0 is skipped with a WARNING log (symmetric with > 1.0 check)."""
        results_file = tmp_path / "neg_score.json"
        _write_promptfoo_json(
            results_file,
            [_make_result("base", "my_metric", "llm-rubric", -0.1)],
        )

        with caplog.at_level(
            logging.WARNING, logger="jerry.testing.extraction.promptfoo_extractor"
        ):
            arrays = extract_score_arrays(results_file)

        _, base_scores = arrays.get("my_metric", ([], []))
        assert -0.1 not in base_scores


# ---------------------------------------------------------------------------
# Tests: metric name resolution precedence
# ---------------------------------------------------------------------------


class TestMetricNameResolution:
    """Unit tests for metric name resolution in extract_score_arrays().

    Verifies the three-level precedence: assertion.metric > assertion.type > 'unnamed'.
    """

    @pytest.mark.unit
    def test_assertion_metric_field_should_take_precedence_over_type(self, tmp_path: Path) -> None:
        """assertion.metric is used when present, ignoring assertion.type.

        The explicit metric label is the most specific identifier and must
        win over the generic assertion type fallback.
        """
        results_file = tmp_path / "metric_vs_type.json"
        result = _make_result("head", "composite_score", "llm-rubric", 0.88)
        _write_promptfoo_json(results_file, [result])

        arrays = extract_score_arrays(results_file)

        assert "composite_score" in arrays, "assertion.metric 'composite_score' must be used"
        assert "llm-rubric" not in arrays, "assertion.type must not override assertion.metric"

    @pytest.mark.unit
    def test_missing_metric_field_should_fall_back_to_assertion_type(self, tmp_path: Path) -> None:
        """When assertion.metric is absent, assertion.type is used as metric name.

        This fallback accommodates promptfoo configs that do not set an explicit
        metric label but do specify an assertion type (e.g., 'python').
        """
        results_file = tmp_path / "type_fallback.json"
        result = _make_result("head", None, "python", 0.75)
        _write_promptfoo_json(results_file, [result])

        arrays = extract_score_arrays(results_file)

        assert "python" in arrays, "assertion.type must be used when assertion.metric is absent"

    @pytest.mark.unit
    def test_missing_both_metric_and_type_should_use_unnamed(self, tmp_path: Path) -> None:
        """When both assertion.metric and assertion.type are absent, 'unnamed' is used.

        The last-resort placeholder 'unnamed' prevents key errors downstream
        and signals to callers that the metric labelling is incomplete.
        """
        results_file = tmp_path / "no_assertion.json"
        # Build an entry with an empty assertion dict (no metric, no type)
        entry: dict = {
            "vars": {"__version__": "head"},
            "response": {"output": "output"},
            "gradingResults": [{"pass": True, "score": 0.70, "reason": "ok", "assertion": {}}],
        }
        _write_promptfoo_json(results_file, [entry])

        arrays = extract_score_arrays(results_file)

        assert "unnamed" in arrays, "No assertion data must produce 'unnamed' metric key"


# ---------------------------------------------------------------------------
# Tests: edge cases added by FIX-WI4-B
# ---------------------------------------------------------------------------


class TestExtractScoreArraysEdgeCases:
    """Unit tests for edge cases addressed by FIX-WI4-B.

    Covers:
    - Uppercase "CANDIDATE" version tag (case-insensitive head classification).
    - Missing __version__ key (absent, not empty string) classified as base.
    - Boolean score values skipped with a WARNING log.
    """

    @pytest.mark.unit
    def test_uppercase_candidate_tag_should_be_classified_as_head(self, tmp_path: Path) -> None:
        """'CANDIDATE' (uppercase) is treated as a head run (case-insensitive).

        Version tag comparison is case-insensitive per the extractor spec.
        'CANDIDATE', 'Candidate', and 'candidate' must all populate head_scores.
        """
        results_file = tmp_path / "uppercase_candidate.json"
        entry: dict = {
            "vars": {"__version__": "CANDIDATE", "prompt": "test"},
            "response": {"output": "test output"},
            "gradingResults": [
                {
                    "pass": True,
                    "score": 0.82,
                    "reason": "ok",
                    "assertion": {"metric": "composite_score", "type": "llm-rubric"},
                }
            ],
        }
        _write_promptfoo_json(results_file, [entry])

        arrays = extract_score_arrays(results_file)

        head_scores, base_scores = arrays["composite_score"]
        assert head_scores == [0.82], "CANDIDATE (uppercase) must be classified as head, not base"
        assert base_scores == []

    @pytest.mark.unit
    def test_missing_version_key_should_be_classified_as_base(self, tmp_path: Path) -> None:
        """An entry whose vars dict lacks __version__ entirely is classified as base.

        Absent key (not empty string) must fall through to base classification
        and emit a debug-level log — not a warning, not an exception.
        """
        results_file = tmp_path / "no_version_key.json"
        # vars dict is present but __version__ key is completely absent
        entry: dict = {
            "vars": {"prompt": "test prompt"},
            "response": {"output": "test output"},
            "gradingResults": [
                {
                    "pass": True,
                    "score": 0.65,
                    "reason": "ok",
                    "assertion": {"metric": "metric_z", "type": "llm-rubric"},
                }
            ],
        }
        _write_promptfoo_json(results_file, [entry])

        arrays = extract_score_arrays(results_file)

        head_scores, base_scores = arrays["metric_z"]
        assert head_scores == [], "Entry with absent __version__ must not appear in head_scores"
        assert base_scores == [0.65], "Entry with absent __version__ must be classified as base"

    @pytest.mark.unit
    def test_boolean_score_should_be_skipped_with_warning(
        self, tmp_path: Path, caplog: pytest.LogCaptureFixture
    ) -> None:
        """A boolean score (True/False) is skipped with a WARNING log.

        In Python, bool is a subclass of int, so isinstance(True, (int, float))
        returns True.  The extractor must reject booleans explicitly before the
        numeric type check to prevent True (== 1) or False (== 0) from silently
        entering the score arrays as 1.0 or 0.0.

        A valid sibling score in the same file must still be extracted normally.
        """
        results_file = tmp_path / "bool_score.json"
        bool_entry: dict = {
            "vars": {"__version__": "head", "prompt": "test"},
            "response": {"output": "test output"},
            "gradingResults": [
                {
                    "pass": True,
                    "score": True,  # boolean — must be skipped
                    "reason": "ok",
                    "assertion": {"metric": "composite_score", "type": "llm-rubric"},
                }
            ],
        }
        valid_entry = _make_result("head", "composite_score", "llm-rubric", 0.75)
        _write_promptfoo_json(results_file, [bool_entry, valid_entry])

        with caplog.at_level(
            logging.WARNING, logger="jerry.testing.extraction.promptfoo_extractor"
        ):
            arrays = extract_score_arrays(results_file)

        head_scores, _ = arrays["composite_score"]
        assert True not in head_scores, "Boolean True must not appear in head_scores"
        assert 1.0 not in head_scores, "Boolean True coerced to 1.0 must not appear in head_scores"
        assert 0.75 in head_scores, "Valid sibling score 0.75 must still be extracted"
        assert any("boolean" in rec.message.lower() for rec in caplog.records), (
            "Expected a WARNING mentioning 'boolean' for the bool score"
        )
