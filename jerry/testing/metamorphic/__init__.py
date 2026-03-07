"""Metamorphic relation framework for the Four-Layer Composite Test Harness.

Layer 3 of the Four-Layer Composite Test Harness.  This package provides the
five universal metamorphic relations (MR-001 through MR-005) that enable
oracle-safe behavioral consistency assertions without requiring exact expected
outputs.

Background:
    The LLM oracle problem (ADR-001 Force F-1) means that there is no ground-
    truth output to compare against for open-ended generative tasks.  Metamorphic
    relations resolve this by asserting CONSISTENCY PROPERTIES across semantically
    related inputs rather than testing specific output values.  The LLMORPH study
    (ASE 2024, 560,000 tests) validated this approach with an 8.6% false positive
    rate for well-calibrated tolerances.

Public API:
    Base classes and result types::

        MetamorphicRelation   -- Abstract base class for all MR implementations
        MRResult              -- Frozen dataclass carrying the verdict and evidence
        MRViolationSeverity   -- Enumeration of violation severity levels
        InsufficientSamplesError -- Domain exception for under-powered samples

    Five universal MR implementations::

        ParaphraseConsistency    -- MR-001: paraphrase should not change quality
        NegationHandling         -- MR-002: negation should produce detectable change
        IrrelevantContextAppendation -- MR-003: irrelevant context should not change quality
        FormattingPerturbation   -- MR-004: formatting changes should not change quality
        LanguageRoundTrip        -- MR-005: round-trip translation should not change quality

    Supporting enumerations::

        FormattingVariant     -- Variants for MR-004 (from formatting_variant.py)
        TranslationLanguage   -- Language codes for MR-005 (from translation_language.py)

    Calibration::

        CalibrationRunner     -- FR-011 stub: empirical tolerance calibration utility

Requirement traceability (corrected per harness-requirements.md):
    FR-010  -- Five Universal Metamorphic Relations (all five MR implementations:
               MR-001 ParaphraseConsistency, MR-002 NegationHandling,
               MR-003 IrrelevantContextAppendation, MR-004 FormattingPerturbation,
               MR-005 LanguageRoundTrip)
    FR-011  -- MR Tolerance Calibration utility (CalibrationRunner in calibration.py;
               stub pending Phase A baseline data collection)
    FR-012  -- Agent-specific MR mechanism (downstream deliverable; not in this package)
    FR-013  -- MR Coverage Tracking (downstream deliverable; not in this package)
    FR-014  -- N >= 20 per version minimum; enforced in MetamorphicRelation._validate_inputs

Architectural deviation (FR-010 AC vs. domain ABC pattern):
    FR-010 acceptance criteria reference DeepEval BaseMetric inheritance.  This
    package uses a domain ABC (MetamorphicRelation) instead, per H-07 domain
    isolation.  The DeepEval adapter in jerry.testing.evaluation.deepeval_adapter
    wraps these domain classes for framework integration.  See base.py module
    docstring for full rationale and system-design.md Section 1.4 / H-07
    Enforcement Rules.

Domain isolation (H-07):
    All classes in this package are DOMAIN-layer components.  They MUST NOT import
    DeepEval, promptfoo, or any adapter module.  The adapter layer in
    jerry.testing.evaluation.deepeval_adapter wraps these classes for framework
    integration.

Usage::

    from jerry.testing.metamorphic import (
        MetamorphicRelation,
        MRResult,
        MRViolationSeverity,
        InsufficientSamplesError,
        ParaphraseConsistency,
        NegationHandling,
        ContextWindowStability,
        FormatInvariance,
        PromptRoundTrip,
    )

    # Apply a metamorphic relation
    mr = ParaphraseConsistency()
    transformed_prompt = mr.transform(original_prompt)

    # Run the agent N times on each variant (N >= 20 for most MRs)
    original_scores = run_agent(original_prompt, n=30)
    transformed_scores = run_agent(transformed_prompt, n=30)

    # Evaluate the relation
    result: MRResult = mr.evaluate(original_scores, transformed_scores)
    if not result.passed:
        print(result.evidence)

Notes:
    Tolerance values are sourced from behavioral-contracts.md Section C and
    MUST NOT be modified without updating the contracts document and re-running
    calibration per FR-011.  Mismatched tolerances are FMEA failure mode FM-009
    (MR violation ambiguous, RPN=125).

    P-value aggregation across multiple MRs (e.g. combining the Wilcoxon
    p-values from MR-001 through MR-005 into a single composite verdict) is
    specified in behavioral-contracts.md Section C.6 using Fisher's method
    for aggregating MR p-values.  Fisher's aggregation is an adapter-layer
    concern and is NOT implemented in this domain package.  It is applied by
    the evaluation adapter (jerry.testing.evaluation) after collecting
    individual ``MRResult`` instances from each relation.
"""

from jerry.testing.metamorphic.base import (
    InsufficientSamplesError,
    MetamorphicRelation,
    MRResult,
    MRViolationSeverity,
)
from jerry.testing.metamorphic.calibration import CalibrationRunner, apply_calibrated_tolerances
from jerry.testing.metamorphic.formatting_variant import FormattingVariant
from jerry.testing.metamorphic.mr_001_paraphrase import ParaphraseConsistency
from jerry.testing.metamorphic.mr_002_negation import NegationHandling
from jerry.testing.metamorphic.mr_003_context import IrrelevantContextAppendation
from jerry.testing.metamorphic.mr_004_formatting import FormattingPerturbation
from jerry.testing.metamorphic.mr_005_roundtrip import LanguageRoundTrip
from jerry.testing.metamorphic.translation_language import TranslationLanguage

# Public API aliases matching the canonical names in the task specification
# and system-design.md module decomposition section.  Both the canonical
# implementation names and these canonical aliases are valid.
ContextWindowStability = IrrelevantContextAppendation
FormatInvariance = FormattingPerturbation
# PromptRoundTrip is the FR-traceability alias for LanguageRoundTrip.
PromptRoundTrip = LanguageRoundTrip


def all_relations() -> list[MetamorphicRelation]:
    """Return one instance of each of the five universal metamorphic relations.

    Uses the default configuration for each relation:
    - MR-001: ParaphraseConsistency (rule-based vocabulary substitution)
    - MR-002: NegationHandling (first-matching negation pattern)
    - MR-003: IrrelevantContextAppendation (seed=42, deterministic selection)
    - MR-004: FormattingPerturbation (MARKDOWN_TO_PLAIN variant)
    - MR-005: LanguageRoundTrip (FRENCH, vocabulary substitution approximation)

    Returns:
        List of five MetamorphicRelation instances in MR ID order.
    """
    return [
        ParaphraseConsistency(),
        NegationHandling(),
        IrrelevantContextAppendation(),
        FormattingPerturbation(),
        LanguageRoundTrip(),
    ]


__all__ = [
    # Base classes and result types
    "MetamorphicRelation",
    "MRResult",
    "MRViolationSeverity",
    "InsufficientSamplesError",
    # Five universal MR implementations (canonical implementation names)
    "ParaphraseConsistency",
    "NegationHandling",
    "IrrelevantContextAppendation",
    "FormattingPerturbation",
    "LanguageRoundTrip",
    # Enumerations (in dedicated single-class files per H-10)
    "FormattingVariant",
    "TranslationLanguage",
    # FR-011 calibration utility stub and tolerance injection interface
    "CalibrationRunner",
    "apply_calibrated_tolerances",
    # Factory
    "all_relations",
    # Public API aliases matching system-design.md and FR traceability names
    "ContextWindowStability",
    "FormatInvariance",
    "PromptRoundTrip",
]
