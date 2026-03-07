"""FR-011: MR Tolerance Calibration utility.

FR-011 (MR Tolerance Calibration from Real Output Pairs, "Must" priority)
requires a calibration utility that accepts 100+ output pairs and computes
empirical tolerance values for each metamorphic relation.

Requirement traceability:
    FR-011 -- MR Tolerance Calibration utility
    ADR-001 FM-009 -- MR violation ambiguous (RPN=125): mitigated by calibrating
                      tolerances against Phase A baseline data after initial
                      deployment.
    behavioral-contracts.md Section C.0 -- "MR tolerances should be calibrated
                      against baseline data" (principle 4).

FR-011 output path:
    Calibrated tolerances are persisted to
    ``tests/prompt-regression/mr-config.yaml`` as specified in the FR-011
    acceptance criteria.  The YAML file maps MR identifier strings (e.g.
    "MR-001") to their calibrated float tolerance values and serves as the
    persistent configuration source for MR tolerance overrides.

Current status:
    STUB -- Interface defined; implementation deferred until Phase A baseline
    data collection is complete.  The hardcoded tolerance values in MR-001
    through MR-005 are analytically derived initial values per contracts C.1
    through C.5.  After Phase A, run CalibrationRunner.calibrate_tolerances()
    with the collected output pairs to produce empirically calibrated values,
    then call apply_calibrated_tolerances() to inject them into MR instances.

Domain isolation: MUST NOT import DeepEval, promptfoo, or any adapter (H-07).
One class per file (H-10).
"""

from __future__ import annotations

import warnings

from jerry.testing.metamorphic.base import MetamorphicRelation

ScoreArray = list[float]


class CalibrationRunner:
    """FR-011 MR Tolerance Calibration runner.

    Accepts baseline output pairs (original vs. transformed score sequences)
    and computes empirically calibrated tolerance values for each metamorphic
    relation.

    Calibration should be run after Phase A baseline data collection (N >= 100
    output pairs per MR) to replace the analytically derived tolerances in
    MR-001 through MR-005 with values grounded in real agent output variance.

    Calibrated tolerances are persisted to
    ``tests/prompt-regression/mr-config.yaml`` (FR-011 AC output path).
    Use ``apply_calibrated_tolerances()`` to inject the returned values into
    live MR instances without modifying source code.

    Per behavioral-contracts.md Section C.0 principle 4:
        "MR tolerances should be calibrated against baseline data.  Initial
        tolerances are analytically derived.  After Phase A baseline
        collection, tolerances should be updated against empirical calibration
        data per FM-009 mitigation."

    Usage (after Phase A data collection)::

        runner = CalibrationRunner()
        baseline_pairs = load_phase_a_pairs()   # list of (original, transformed) arrays
        tolerances = runner.calibrate_tolerances(baseline_pairs)
        # tolerances = {"MR-001": 0.047, "MR-002": 0.052, ...}
        # Persist to tests/prompt-regression/mr-config.yaml, then inject:
        relations = all_relations()
        apply_calibrated_tolerances(tolerances, relations)
    """

    def calibrate_tolerances(
        self,
        baseline_pairs: list[tuple[ScoreArray, ScoreArray]],
    ) -> dict[str, float]:
        """Compute empirically calibrated tolerance values from baseline pairs.

        Processes N >= 100 original/transformed score pair sequences (one pair
        per MR application on a known-good baseline prompt) and computes the
        95th percentile absolute delta.  The 95th percentile is the standard
        statistical threshold for outlier exclusion in tolerance calibration
        (consistent with LLMORPH calibration practice; chosen over the mean to
        be robust against outlier score pairs while remaining sensitive to
        systematic variance).  This provides a statistically robust tolerance
        value that reflects actual agent output variance rather than the
        analytically estimated initial values.

        Calibrated values are intended for persistence to
        ``tests/prompt-regression/mr-config.yaml`` (FR-011 AC output path).

        Args:
            baseline_pairs: List of (original_scores, transformed_scores) tuples
                collected during Phase A baseline evaluation.  Each tuple is one
                MR application result on a known-good prompt version.  Fewer
                than 100 pairs emits a UserWarning but execution continues;
                results will be less reliable.

        Returns:
            Dictionary mapping MR identifier strings (e.g. "MR-001") to their
            calibrated tolerance values (floats).  Return values replace the
            hardcoded TOLERANCE constants in MR-001 through MR-005 after
            validation and persistence to mr-config.yaml.

        Raises:
            NotImplementedError: FR-011 calibration utility -- implement after
                Phase A baseline data collection is complete.
        """
        if len(baseline_pairs) < 100:
            warnings.warn(
                f"FR-011: Only {len(baseline_pairs)} pairs provided "
                f"(recommended >= 100 for reliable calibration). "
                f"Collect additional Phase A baseline data for more robust results.",
                UserWarning,
                stacklevel=2,
            )
        raise NotImplementedError(
            "FR-011 calibration utility -- implement after Phase A baseline "
            "data collection is complete.  See behavioral-contracts.md C.0 "
            "principle 4 and ADR-001 FM-009 for calibration requirements.  "
            "Calibrated tolerances persist to tests/prompt-regression/mr-config.yaml."
        )


def apply_calibrated_tolerances(
    tolerances: dict[str, float],
    relations: list[MetamorphicRelation],
) -> None:
    """Tolerance injection interface for the FR-011 calibration workflow.

    Updates each MR instance's ``TOLERANCE`` attribute with the value from the
    calibrated tolerances dictionary produced by
    ``CalibrationRunner.calibrate_tolerances()``.  This allows calibrated
    values from ``tests/prompt-regression/mr-config.yaml`` to be applied at
    runtime without modifying source code constants.

    Only relations whose MR identifier is present in the ``tolerances`` dict
    are updated; unmatched relations retain their compile-time defaults.

    Args:
        tolerances: Dictionary mapping MR identifier strings to calibrated
            float tolerance values.  Keys must match
            ``MetamorphicRelation.mr_id`` exactly (e.g. ``"MR-001"``,
            ``"MR-003"``).  Values must be in the open interval ``(0.0, 1.0)``.
            Typically returned by
            ``CalibrationRunner.calibrate_tolerances()`` and persisted to
            ``tests/prompt-regression/mr-config.yaml``.
        relations: List of ``MetamorphicRelation`` instances to update in
            place.  Typically produced by ``all_relations()``.

    Raises:
        ValueError: If any tolerance value is not in the range ``(0.0, 1.0)``.

    Example::

        tolerances = {"MR-001": 0.047, "MR-003": 0.028}
        relations = all_relations()
        apply_calibrated_tolerances(tolerances, relations)
        # MR-001.TOLERANCE is now 0.047; MR-003.TOLERANCE is now 0.028
        # MR-002, MR-004, MR-005 retain their compile-time defaults
    """
    for relation in relations:
        if relation.mr_id in tolerances:
            new_tolerance = tolerances[relation.mr_id]
            if not 0.0 < new_tolerance < 1.0:
                raise ValueError(
                    f"Calibrated tolerance for {relation.mr_id} must be in "
                    f"(0.0, 1.0); got {new_tolerance}"
                )
            relation.TOLERANCE = new_tolerance
