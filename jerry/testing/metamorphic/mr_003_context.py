"""MR-003: Irrelevant Context Appendation metamorphic relation.

Definition (behavioral-contracts.md Section C.3):
    Appending text that is irrelevant to the agent's task should not change
    output quality by more than the tolerance (0.03, tighter than MR-001).

Tolerance: 0.03 (max |score_original - score_appended|)
Violation condition: Wilcoxon p < 0.05 AND mean_delta > 0.03 (both required)
Effect size threshold: Cohen's r >= 0.25 (medium-small effect)
Minimum sample size: 20 pairs (ADR-001 FM-002)

The tighter tolerance (0.03 vs MR-001's 0.05) reflects the expectation that
irrelevant context is a weaker perturbation than paraphrasing: if an agent
is sensitive to irrelevant suffix text it indicates a robustness deficiency.

Statistical helper: uses ``_wilcoxon_p_and_effect`` from ``mr_001_paraphrase``;
changes to that function affect this module's evaluate() method.

Domain isolation: MUST NOT import DeepEval, promptfoo, or any adapter (H-07).
One class per file (H-10).
"""

from __future__ import annotations

import random
from collections.abc import Sequence

from jerry.testing.metamorphic.base import (
    MetamorphicRelation,
    MRResult,
    MRViolationSeverity,
)
from jerry.testing.metamorphic.mr_001_paraphrase import _wilcoxon_p_and_effect

# ---------------------------------------------------------------------------
# Irrelevant context corpus
# ---------------------------------------------------------------------------

# A curated pool of topically neutral paragraphs that are clearly unrelated
# to software engineering, AI agents, or Jerry Framework topics.  Each entry
# is marked with a visible delimiter so the agent can unambiguously recognise
# the appended text as non-task content.
#
# Per contracts C.3 example:
#   "According to recent reports, the price of commodities has fluctuated
#    significantly in Q1 2026. [END OF APPENDED CONTEXT - NOT RELATED TO YOUR TASK]"
_IRRELEVANT_CONTEXTS: list[str] = [
    (
        "According to recent reports, the price of commodities has fluctuated "
        "significantly in Q1 2026. Market analysts attribute this to supply chain "
        "disruptions caused by geopolitical tensions in several key regions."
    ),
    (
        "The migratory patterns of Arctic tern populations have shifted by an "
        "average of 200 kilometres northward over the past decade, according to "
        "ornithological research published in the Journal of Avian Biology."
    ),
    (
        "A new study from the University of Cambridge suggests that consuming "
        "dark chocolate in moderate quantities may reduce the risk of cardiovascular "
        "events by up to 11 percent in adults over the age of 45."
    ),
    (
        "The restoration of the Colosseum's outer ring, begun in 2018, is expected "
        "to conclude in late 2027. The project involves specialised limestone masons "
        "sourced from the same quarries used in the original construction."
    ),
    (
        "Global wheat production is forecast to decline by 3.4 percent in the current "
        "growing season, primarily due to drought conditions across the northern "
        "hemisphere. Futures markets have priced in the expected shortfall."
    ),
    (
        "The newly discovered cave system in the Yucatan Peninsula extends more than "
        "380 kilometres and contains previously undocumented species of blind "
        "cavefish adapted to mineral-rich subterranean water flows."
    ),
    (
        "Municipal water treatment facilities in several mid-sized European cities "
        "have begun deploying AI-assisted dosing systems that reduce chemical usage "
        "by an average of 18 percent while maintaining regulatory compliance."
    ),
    (
        "Marathon running has experienced a 34 percent increase in registered "
        "participants over the past five years, with the largest growth segment "
        "being adults aged 35 to 50 entering their first endurance event."
    ),
    (
        "Philatelic auction results for the 1856 British Guiana One-Cent Magenta "
        "stamp reached a record £6.2 million in the spring auction season, "
        "surpassing the previous record set in 2014."
    ),
    (
        "Agricultural drones equipped with multispectral sensors can now identify "
        "nitrogen deficiency in corn crops up to two weeks before visible symptoms "
        "appear, enabling precision fertiliser application that reduces waste."
    ),
]

# Delimiter appended after each irrelevant context block.  The delimiter is
# explicit so that agents with good context-isolation behaviour can filter it.
_DELIMITER = "[END OF APPENDED CONTEXT - NOT RELATED TO YOUR TASK]"

# Default random seed for deterministic context selection when no seed is provided.
_DEFAULT_SEED = 42


class IrrelevantContextAppendation(MetamorphicRelation):
    """MR-003: Irrelevant Context Appendation.

    Tests that appending topically unrelated text to the user message does not
    change output quality by more than the tolerance threshold.

    A violation indicates the agent is distracted by or confused by off-topic
    content -- a robustness deficiency.

    Tolerance values (from behavioral-contracts.md C.3):
        max_delta        = 0.03  (absolute mean score delta; tighter than MR-001)
        p_alpha          = 0.05  (Wilcoxon significance level)
        effect_r_min     = 0.25  (Cohen's r; medium-small threshold)

    Violation condition (both must be true):
        1. Wilcoxon signed-rank p < 0.05
        2. Mean absolute delta > 0.03

    Severity classification (contracts C.3):
        REGRESSION : Score decreases (agent confused by irrelevant content)
        WARNING    : Score increases (agent appears to find irrelevant content useful)
    """

    mr_id: str = "MR-003"
    mr_name: str = "Irrelevant Context Appendation"
    minimum_sample_size: int = 20

    # Contracts C.3 parameters
    TOLERANCE: float = 0.03
    P_ALPHA: float = 0.05
    EFFECT_R_THRESHOLD: float = 0.25

    def __init__(self, seed: int = _DEFAULT_SEED) -> None:
        """Initialise with an optional random seed for context selection.

        Args:
            seed: Random seed ensuring deterministic context selection across
                test runs.  Use the same seed for baseline and regression
                comparisons to ensure comparable transforms.
        """
        self._seed = seed

    def transform(self, input_text: str) -> str:
        """Append a randomly selected irrelevant context paragraph to the input.

        Context is selected deterministically using the configured seed so that
        the same input always receives the same appended context.  The appended
        block is clearly delimited per contracts C.3 example format.

        Args:
            input_text: The original prompt or user message text.

        Returns:
            Input text with an irrelevant context paragraph appended, separated
            by a blank line and terminated with the standard delimiter.

        Raises:
            ValueError: If ``input_text`` is empty.
        """
        if not input_text or not input_text.strip():
            raise ValueError(f"{self.mr_id}: input_text must be non-empty for context appendation.")

        rng = random.Random(self._seed)
        context_paragraph = rng.choice(_IRRELEVANT_CONTEXTS)

        return input_text.rstrip() + "\n\n" + context_paragraph + " " + _DELIMITER

    def evaluate(
        self,
        original_scores: Sequence[float],
        transformed_scores: Sequence[float],
    ) -> MRResult:
        """Evaluate context robustness across paired score sequences.

        Applies the dual-condition violation check from contracts C.3:
        1. Wilcoxon signed-rank p < 0.05
        2. Mean absolute delta > TOLERANCE (0.03)

        Severity distinguishes score decrease (agent confused) from score
        increase (spurious improvement from irrelevant content).

        Args:
            original_scores: Quality scores from N original-prompt runs.
            transformed_scores: Quality scores from N context-appended runs.

        Returns:
            ``MRResult`` with verdict, delta, effect size, p-value, and evidence.

        Raises:
            InsufficientSamplesError: If len(original_scores) < 20.
            ValueError: Mismatched lengths or out-of-range scores.
        """
        self._validate_inputs(original_scores, transformed_scores)

        n = len(original_scores)
        mean_orig = self._mean(original_scores)
        mean_trans = self._mean(transformed_scores)
        mean_delta = abs(mean_orig - mean_trans)

        p_value, effect_r = _wilcoxon_p_and_effect(
            list(original_scores), list(transformed_scores), n
        )

        statistically_significant = p_value < self.P_ALPHA
        practically_significant = mean_delta > self.TOLERANCE
        violated = statistically_significant and practically_significant

        if violated:
            # Determine direction of effect for severity classification
            if mean_trans < mean_orig:
                # Score decreased: agent confused by irrelevant content
                severity = MRViolationSeverity.REGRESSION
                direction = "decreased (agent confused by irrelevant content)"
            else:
                # Score increased: agent finds irrelevant content spuriously useful
                severity = MRViolationSeverity.WARNING
                direction = (
                    "increased (agent appears to find irrelevant content useful; "
                    "possible pattern-matching artefact)"
                )
            passed = False
            evidence = (
                f"MR-003 VIOLATED: quality score {direction}. "
                f"mean_delta={mean_delta:.4f} > tolerance {self.TOLERANCE}. "
                f"Wilcoxon p={p_value:.4f} (alpha {self.P_ALPHA}), "
                f"Cohen's r={effect_r:.3f} (threshold {self.EFFECT_R_THRESHOLD}). "
                f"mean_original={mean_orig:.4f}, mean_appended={mean_trans:.4f}, N={n}."
            )
        else:
            severity = MRViolationSeverity.PASS
            passed = True
            reason_parts: list[str] = []
            if not statistically_significant:
                reason_parts.append(
                    f"Wilcoxon p={p_value:.4f} >= alpha {self.P_ALPHA} (not significant)"
                )
            if not practically_significant:
                reason_parts.append(f"mean_delta={mean_delta:.4f} <= tolerance {self.TOLERANCE}")
            evidence = (
                "MR-003 PASSED: irrelevant context appendation has no significant "
                "effect. " + "; ".join(reason_parts) + ". "
                f"Cohen's r={effect_r:.3f}, N={n}. "
                f"mean_original={mean_orig:.4f}, mean_appended={mean_trans:.4f}."
            )

        return MRResult(
            mr_id=self.mr_id,
            mr_name=self.mr_name,
            passed=passed,
            original_scores=tuple(original_scores),
            transformed_scores=tuple(transformed_scores),
            mean_original=mean_orig,
            mean_transformed=mean_trans,
            mean_delta=mean_delta,
            tolerance=self.TOLERANCE,
            effect_size=effect_r,
            p_value=p_value,
            severity=severity,
            evidence=evidence,
        )
