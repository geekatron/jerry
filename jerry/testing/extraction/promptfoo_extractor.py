# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Victor Lau

# CG-008

"""Adapter: extract per-metric score arrays from a promptfoo results JSON file.

This module reads the JSON output produced by ``promptfoo eval`` and converts
it into paired ``(head_scores, base_scores)`` score arrays per metric, suitable
for direct consumption by the Layer 4 statistical engine
(``jerry.testing.stats.compare_versions``).

Architecture (H-07 compliance):
    - ADAPTER layer (inbound): translates promptfoo's external JSON format into
      the domain ``ScoreArray`` type.  Depends only on stdlib + domain types.
    - MUST NOT be imported by domain modules (stats.py, types.py).
    - Domain modules NEVER import from this adapter.

H-10 compliance:
    One primary public function defined in this file: ``extract_score_arrays``.
    No classes are defined here; all logic is procedural (parsing adapter).

H-11 compliance:
    All public symbols carry type annotations and docstrings.

Promptfoo results JSON structure (as consumed by this extractor)::

    {
      "results": {
        "results": [
          {
            "vars": {"prompt": "...", "__version__": "head"},
            "response": {"output": "..."},
            "gradingResults": [
              {
                "pass": true,
                "score": 0.85,
                "reason": "...",
                "assertion": {"type": "llm-rubric", "metric": "composite_score"},
                "componentResults": [...]
              }
            ]
          }
        ]
      }
    }

Version discrimination:
    Each test result entry is classified as a "head" (candidate) or "base"
    (baseline) run via the ``__version__`` variable in ``vars``.  Accepted
    values for head: ``"head"``, ``"candidate"`` (case-insensitive).  All
    other values are treated as base.  Entries missing ``__version__`` are
    treated as base and a debug-level log is emitted.

Metric name resolution (precedence order):
    1. ``gradingResult["assertion"]["metric"]`` — explicit metric label.
    2. ``gradingResult["assertion"]["type"]``   — assertion type as fallback.
    3. Literal ``"unnamed"``                    — last-resort placeholder.

Entry skipping:
    Entries with malformed ``gradingResults`` (not a list, missing ``score``
    key, ``score`` not numeric, or ``score`` outside [0.0, 1.0]) are skipped
    with a ``WARNING``-level log.  Structural errors that indicate a completely
    invalid file raise ``ValueError`` immediately.
"""

from __future__ import annotations

import json
import logging
from collections import defaultdict
from pathlib import Path

from jerry.testing.types import ScoreArray

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Module-level constants
# ---------------------------------------------------------------------------

#: Variable key used by promptfoo to tag which prompt version a result belongs to.
_VERSION_VAR_KEY: str = "__version__"

#: Values (case-normalised) that indicate the "head" (candidate) version.
_HEAD_VERSION_VALUES: frozenset[str] = frozenset({"head", "candidate"})


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def extract_score_arrays(
    promptfoo_json_path: Path,
) -> dict[str, tuple[ScoreArray, ScoreArray]]:
    """Parse a promptfoo results JSON file and extract per-metric score arrays.

    Reads the JSON file at ``promptfoo_json_path``, iterates over every test
    result entry, and groups numeric scores by metric name into two parallel
    lists: one for "head" (candidate) runs and one for "base" (baseline) runs.

    Version discrimination is performed via the ``__version__`` variable in
    each result's ``vars`` dictionary.  Entries tagged ``"head"`` or
    ``"candidate"`` (case-insensitive) populate the first array; all others
    populate the second array.

    Args:
        promptfoo_json_path: Absolute or relative path to the promptfoo results
            JSON file produced by ``promptfoo eval --output results.json``.
            The file must be readable and contain valid JSON with the expected
            ``results.results`` list structure.

    Returns:
        A dictionary mapping metric name to a 2-tuple
        ``(head_scores, base_scores)`` where:

        - ``head_scores`` (``ScoreArray``) — list of float scores from runs
          tagged as "head" / "candidate".
        - ``base_scores`` (``ScoreArray``) — list of float scores from all
          other runs (baseline / control).

        Both arrays may be empty if no results for that version were found.
        The dictionary contains one entry per unique metric name encountered
        in the file.  Returns an empty dict if the ``results.results`` list is
        empty (but still structurally valid).

    Raises:
        FileNotFoundError: If ``promptfoo_json_path`` does not exist or is not
            a regular file.
        ValueError: If the file contains invalid JSON, or if the top-level
            structure is missing the required ``results.results`` list (i.e.,
            the file does not look like a promptfoo output file).
        OSError: If the file cannot be read due to a permissions error or
            similar I/O problem.

    Example::

        from pathlib import Path
        from jerry.testing.extraction import extract_score_arrays

        arrays = extract_score_arrays(Path("promptfoo-results.json"))
        head, base = arrays["composite_score"]
        # head and base are ScoreArray (list[float])

    Notes:
        - Entries with ``gradingResults`` that are not a list, or individual
          grading results that are missing a numeric ``score`` in [0.0, 1.0],
          are skipped with a WARNING log rather than raising an exception.
          This tolerates minor promptfoo schema variations between versions.
        - Score values are clamped to [0.0, 1.0]; out-of-range values are
          skipped with a WARNING log (not silently clamped, to surface data
          quality issues early).
        - The function is intentionally stateless (no caching, no side effects
          beyond logging).  Call it once per file per pipeline invocation.
    """
    # ------------------------------------------------------------------
    # I/O: read and parse the JSON file
    # ------------------------------------------------------------------
    if not promptfoo_json_path.exists():
        raise FileNotFoundError(f"Promptfoo results file not found: {promptfoo_json_path}")

    raw_text = promptfoo_json_path.read_text(encoding="utf-8")

    try:
        data = json.loads(raw_text)
    except json.JSONDecodeError as exc:
        raise ValueError(
            f"Promptfoo results file contains invalid JSON ({promptfoo_json_path}): {exc}"
        ) from exc

    # ------------------------------------------------------------------
    # Structural validation: require results.results list
    # ------------------------------------------------------------------
    top_results = data.get("results")
    if not isinstance(top_results, dict):
        raise ValueError(
            f"Promptfoo results file is missing the top-level 'results' object. "
            f'Expected structure: {{"results": {{"results": [...]}}}}. '
            f"Got type {type(top_results).__name__!r} at key 'results'. "
            f"File: {promptfoo_json_path}"
        )

    result_list = top_results.get("results")
    if not isinstance(result_list, list):
        raise ValueError(
            f"Promptfoo results file is missing the 'results.results' list. "
            f'Expected structure: {{"results": {{"results": [...]}}}}. '
            f"Got type {type(result_list).__name__!r} at key 'results.results'. "
            f"File: {promptfoo_json_path}"
        )

    if not result_list:
        logger.warning(
            "extract_score_arrays: zero result entries in %s — file may be empty or stale.",
            promptfoo_json_path.name,
        )

    # ------------------------------------------------------------------
    # Accumulate scores: metric_name -> (head_list, base_list)
    # ------------------------------------------------------------------
    head_buckets: dict[str, list[float]] = defaultdict(list)
    base_buckets: dict[str, list[float]] = defaultdict(list)

    for entry_idx, entry in enumerate(result_list):
        if not isinstance(entry, dict):
            logger.warning(
                "Skipping entry at index %d: expected a dict, got %s.",
                entry_idx,
                type(entry).__name__,
            )
            continue

        # --- Determine head vs. base version ---
        vars_dict = entry.get("vars", {})
        version_tag = ""
        if isinstance(vars_dict, dict):
            raw_tag = vars_dict.get(_VERSION_VAR_KEY, "")
            version_tag = str(raw_tag).strip().lower() if raw_tag else ""
        else:
            logger.debug(
                "Entry %d: 'vars' is not a dict (type=%s); treating as base.",
                entry_idx,
                type(vars_dict).__name__,
            )

        if not version_tag:
            logger.debug(
                "Entry %d: missing '%s' in vars; treating as base.",
                entry_idx,
                _VERSION_VAR_KEY,
            )

        is_head = version_tag in _HEAD_VERSION_VALUES

        # --- Parse gradingResults ---
        grading_results = entry.get("gradingResults")
        if not isinstance(grading_results, list):
            logger.warning(
                "Skipping entry %d: 'gradingResults' is not a list (type=%s, version=%r).",
                entry_idx,
                type(grading_results).__name__,
                version_tag or "base",
            )
            continue

        for gr_idx, gr in enumerate(grading_results):
            if not isinstance(gr, dict):
                logger.warning(
                    "Skipping gradingResult %d in entry %d: expected dict, got %s.",
                    gr_idx,
                    entry_idx,
                    type(gr).__name__,
                )
                continue

            # --- Extract metric name ---
            metric_name = _resolve_metric_name(gr, entry_idx, gr_idx)

            # --- Extract and validate score ---
            raw_score = gr.get("score")
            if raw_score is None:
                logger.warning(
                    "Skipping gradingResult %d in entry %d (metric=%r): missing 'score' key.",
                    gr_idx,
                    entry_idx,
                    metric_name,
                )
                continue

            # bool is a subclass of int in Python, so isinstance(True, (int, float))
            # returns True.  A JSON boolean is not a valid numeric score; reject it
            # explicitly before the numeric type check below.
            if isinstance(raw_score, bool):
                logger.warning(
                    "extract_score_arrays: boolean score in gradingResult %d "
                    "of entry %d (metric=%r) — skipping (expected numeric 0.0–1.0).",
                    gr_idx,
                    entry_idx,
                    metric_name,
                )
                continue

            if not isinstance(raw_score, int | float):
                logger.warning(
                    "Skipping gradingResult %d in entry %d (metric=%r): "
                    "'score' is not numeric (type=%s, value=%r).",
                    gr_idx,
                    entry_idx,
                    metric_name,
                    type(raw_score).__name__,
                    raw_score,
                )
                continue

            score = float(raw_score)
            if not (0.0 <= score <= 1.0):
                logger.warning(
                    "Skipping gradingResult %d in entry %d (metric=%r): "
                    "score %.4f is outside [0.0, 1.0].",
                    gr_idx,
                    entry_idx,
                    metric_name,
                    score,
                )
                continue

            # --- Route to appropriate bucket ---
            if is_head:
                head_buckets[metric_name].append(score)
            else:
                base_buckets[metric_name].append(score)

    # ------------------------------------------------------------------
    # Build output: union of metric names from both buckets
    # ------------------------------------------------------------------
    all_metric_names: set[str] = set(head_buckets.keys()) | set(base_buckets.keys())

    result: dict[str, tuple[ScoreArray, ScoreArray]] = {}
    for metric_name in sorted(all_metric_names):
        head_scores: ScoreArray = list(head_buckets.get(metric_name, []))
        base_scores: ScoreArray = list(base_buckets.get(metric_name, []))
        result[metric_name] = (head_scores, base_scores)

    logger.info(
        "extract_score_arrays: parsed %d result entries from %s. Metrics extracted: %d (%s).",
        len(result_list),
        promptfoo_json_path.name,
        len(result),
        ", ".join(sorted(result)) if result else "none",
    )

    return result


# ---------------------------------------------------------------------------
# Private helpers
# ---------------------------------------------------------------------------


def _resolve_metric_name(grading_result: dict, entry_idx: int, gr_idx: int) -> str:
    """Resolve the metric name from a single grading result dict.

    Resolution priority:
        1. ``assertion["metric"]``  — explicit metric label set by the promptfoo
           YAML configuration (most specific).
        2. ``assertion["type"]``    — assertion type as a fallback label
           (e.g., ``"llm-rubric"``, ``"python"``).
        3. Literal ``"unnamed"``    — last resort when no assertion data is present.

    Args:
        grading_result: A single element from the ``gradingResults`` list.
        entry_idx:      Index of the parent result entry (for log messages).
        gr_idx:         Index of this grading result within its parent (for logs).

    Returns:
        A non-empty metric name string.
    """
    assertion = grading_result.get("assertion")
    if isinstance(assertion, dict):
        metric = assertion.get("metric")
        if metric and isinstance(metric, str):
            return metric.strip() or "unnamed"

        assertion_type = assertion.get("type")
        if assertion_type and isinstance(assertion_type, str):
            logger.debug(
                "Entry %d, gradingResult %d: using assertion 'type' (%r) as metric name "
                "(no 'metric' key in assertion).",
                entry_idx,
                gr_idx,
                assertion_type,
            )
            return assertion_type.strip() or "unnamed"

    logger.debug(
        "Entry %d, gradingResult %d: no assertion data found; using 'unnamed'.",
        entry_idx,
        gr_idx,
    )
    return "unnamed"
