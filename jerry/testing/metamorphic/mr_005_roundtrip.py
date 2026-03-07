"""MR-005: Language Round-Trip metamorphic relation.

Definition (behavioral-contracts.md Section C.5):
    Translating the prompt to a second language and back to English (round-trip
    translation) should not change output quality by more than the tolerance
    (0.06).  This tests semantic robustness to surface-level wording variation.

Important constraint (contracts C.5):
    This MR applies only to the USER MESSAGE, not the system prompt.  The
    system prompt remains in English.

Tolerance: 0.06 (highest across all MRs; accommodates translation noise)
Violation condition: Wilcoxon p < 0.05 AND mean_delta > 0.06 (both required)
Effect size threshold: Cohen's r >= 0.35 (slightly higher; translation noise
    increases expected baseline effect size)
Minimum sample size: 20 pairs (ADR-001 FM-002)

Translation languages (priority order per contracts C.5):
    1. French (FR)
    2. German (DE)
    3. Spanish (ES)

Statistical helper: uses ``_wilcoxon_p_and_effect`` from ``mr_001_paraphrase``;
changes to that function affect this module's evaluate() method.

Domain isolation: MUST NOT import DeepEval, promptfoo, or any adapter (H-07).
One class per file (H-10): TranslationLanguage enum is in translation_language.py;
this file contains only LanguageRoundTrip.
"""

from __future__ import annotations

import re
from collections.abc import Callable, Sequence

from jerry.testing.metamorphic.base import (
    MetamorphicRelation,
    MRResult,
    MRViolationSeverity,
)
from jerry.testing.metamorphic.mr_001_paraphrase import _wilcoxon_p_and_effect
from jerry.testing.metamorphic.translation_language import TranslationLanguage

# ---------------------------------------------------------------------------
# Built-in vocabulary substitution tables for offline round-trip simulation
# ---------------------------------------------------------------------------
# Full LLM-backed translation would require external service calls and network
# access, violating the domain isolation requirement (H-07) and making tests
# non-deterministic and rate-limited.
#
# This implementation provides a vocabulary-substitution approximation that:
# 1. Is deterministic (same input -> same output, always)
# 2. Has no external dependencies
# 3. Introduces realistic synonym substitution that mirrors the wording drift
#    produced by genuine round-trip translation
# 4. Can be replaced by a real translation adapter at the adapter layer
#    without changing the domain class interface
#
# When a real translation adapter is provided via the `translator` constructor
# argument, it will be used instead of the vocabulary tables.

# French -> English back-translation substitution table
# These simulate typical round-trip translation drift for French.
_FR_ROUNDTRIP_SUBSTITUTIONS: list[tuple[str, str]] = [
    ("analyze", "analyse"),
    ("organization", "organisation"),
    ("recognize", "recognise"),
    ("behavior", "behaviour"),
    ("color", "colour"),
    ("favor", "favour"),
    ("labor", "labour"),
    ("utilize", "utilise"),
    ("criticize", "criticise"),
    ("summarize", "summarise"),
    ("emphasize", "emphasise"),
    ("goal", "objective"),
    ("important", "significant"),
    ("used", "employed"),
    ("shows", "demonstrates"),
    ("clear", "evident"),
    ("need", "require"),
    ("improve", "enhance"),
    ("make sure", "ensure"),
    ("check", "verify"),
    ("get", "obtain"),
    ("use", "utilise"),
    ("find out", "determine"),
    ("look at", "examine"),
    ("talk about", "discuss"),
    ("show", "illustrate"),
    ("help", "assist"),
    ("based on", "on the basis of"),
    ("about", "regarding"),
    ("because", "due to the fact that"),
    ("so", "therefore"),
    ("also", "furthermore"),
    ("but", "however"),
    ("and", "as well as"),
]

# German -> English back-translation substitution table
_DE_ROUNDTRIP_SUBSTITUTIONS: list[tuple[str, str]] = [
    ("show", "present"),
    ("create", "generate"),
    ("use", "apply"),
    ("start", "commence"),
    ("end", "conclude"),
    ("important", "significant"),
    ("different", "various"),
    ("new", "novel"),
    ("good", "adequate"),
    ("big", "substantial"),
    ("small", "minor"),
    ("need", "necessitate"),
    ("give", "provide"),
    ("take", "undertake"),
    ("many", "numerous"),
    ("often", "frequently"),
    ("always", "invariably"),
    ("must", "is required to"),
    ("can", "is able to"),
    ("should", "ought to"),
    ("may", "is permitted to"),
    ("get", "receive"),
    ("look", "observe"),
    ("think", "consider"),
    ("become", "develop into"),
    ("make", "produce"),
    ("put", "place"),
    ("set", "establish"),
    ("come", "arrive"),
    ("go", "proceed"),
]

# Spanish -> English back-translation substitution table
_ES_ROUNDTRIP_SUBSTITUTIONS: list[tuple[str, str]] = [
    ("use", "employ"),
    ("do", "perform"),
    ("have", "possess"),
    ("make", "construct"),
    ("see", "observe"),
    ("know", "be aware of"),
    ("give", "provide"),
    ("take", "undertake"),
    ("look for", "seek"),
    ("find", "locate"),
    ("think", "believe"),
    ("come", "arrive"),
    ("go", "proceed"),
    ("want", "desire"),
    ("need", "require"),
    ("good", "satisfactory"),
    ("bad", "unsatisfactory"),
    ("big", "large"),
    ("small", "reduced"),
    ("new", "recent"),
    ("old", "prior"),
    ("high", "elevated"),
    ("low", "reduced"),
    ("always", "at all times"),
    ("never", "under no circumstances"),
    ("now", "currently"),
    ("also", "additionally"),
    ("but", "nevertheless"),
    ("because", "given that"),
    ("so", "consequently"),
]

_SUBSTITUTIONS_BY_LANGUAGE: dict[TranslationLanguage, list[tuple[str, str]]] = {
    TranslationLanguage.FRENCH: _FR_ROUNDTRIP_SUBSTITUTIONS,
    TranslationLanguage.GERMAN: _DE_ROUNDTRIP_SUBSTITUTIONS,
    TranslationLanguage.SPANISH: _ES_ROUNDTRIP_SUBSTITUTIONS,
}


class LanguageRoundTrip(MetamorphicRelation):
    """MR-005: Language Round-Trip.

    Tests that round-trip translation of the user message does not change
    output quality beyond the translation-noise tolerance.

    A violation indicates the agent's output quality is brittle to minor
    semantic wording variations -- a generalisation deficiency.

    System prompt isolation:
        The transform() method applies only to the user message portion of the
        input.  Callers MUST pass only the user message to transform(), not the
        full agent definition system prompt.  This matches contracts C.5.

    Tolerance values (from behavioral-contracts.md C.5):
        max_delta        = 0.06  (highest across all MRs; translation noise)
        p_alpha          = 0.05  (Wilcoxon significance level)
        effect_r_min     = 0.35  (slightly higher; translation noise inflates baseline)

    Violation condition (both must be true):
        1. Wilcoxon signed-rank p < 0.05
        2. Mean absolute delta > 0.06
    """

    mr_id: str = "MR-005"
    mr_name: str = "Language Round-Trip"
    minimum_sample_size: int = 20

    # Contracts C.5 parameters
    TOLERANCE: float = 0.06
    P_ALPHA: float = 0.05
    EFFECT_R_THRESHOLD: float = 0.35

    def __init__(
        self,
        language: TranslationLanguage = TranslationLanguage.FRENCH,
        translator: Callable[[str, str], str] | None = None,
    ) -> None:
        """Initialise with a translation language and optional real translator.

        Args:
            language: The intermediate language for the round-trip translation.
                Defaults to ``FRENCH`` (highest translation quality, minimal
                semantic drift per contracts C.5).
            translator: Optional callable with signature ``(text, lang_code) -> str``
                that performs actual round-trip translation via an external
                service.  If ``None``, the built-in vocabulary substitution
                approximation is used.  The callable should return the
                English back-translation of ``text`` after routing through
                the language indicated by ``lang_code`` (e.g. "fr").
        """
        self._language = language
        self._translator = translator

    @property
    def language(self) -> TranslationLanguage:
        """The active intermediate translation language."""
        return self._language

    def transform(self, input_text: str) -> str:
        """Apply a round-trip language translation to the user message text.

        If a real translator callable was provided at construction, it is used.
        Otherwise, applies the built-in vocabulary substitution table for the
        configured language, which produces realistic wording drift without
        requiring external services.

        IMPORTANT: Pass only the user message to this method, not the full
        system prompt.  The system prompt must remain in English per contracts
        C.5.

        Args:
            input_text: The user message text to round-trip through translation.

        Returns:
            Round-trip translated variant of the input text.

        Raises:
            ValueError: If ``input_text`` is empty.
        """
        if not input_text or not input_text.strip():
            raise ValueError(
                f"{self.mr_id}: input_text must be non-empty for round-trip transform."
            )

        if self._translator is not None:
            return self._translator(input_text, self._language.value)

        return _apply_vocabulary_substitution(input_text, self._language)

    def evaluate(
        self,
        original_scores: Sequence[float],
        transformed_scores: Sequence[float],
    ) -> MRResult:
        """Evaluate round-trip translation robustness across paired score sequences.

        Applies the dual-condition violation check from contracts C.5:
        1. Wilcoxon signed-rank p < 0.05
        2. Mean absolute delta > TOLERANCE (0.06)

        The higher tolerance (0.06) relative to MR-001 (0.05) reflects the
        additional semantic drift introduced by translation.

        Args:
            original_scores: Quality scores from N original user-message runs.
            transformed_scores: Quality scores from N round-trip translated runs.

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

        lang_name = self._language.name.capitalize()

        if violated:
            severity = MRViolationSeverity.REGRESSION
            passed = False
            evidence = (
                f"MR-005 VIOLATED: {lang_name} round-trip translation changed "
                f"quality by {mean_delta:.4f} (tolerance {self.TOLERANCE}). "
                f"Agent output quality is brittle to minor wording variations. "
                f"Wilcoxon p={p_value:.4f} (alpha {self.P_ALPHA}), "
                f"Cohen's r={effect_r:.3f} (threshold {self.EFFECT_R_THRESHOLD}). "
                f"mean_original={mean_orig:.4f}, mean_roundtrip={mean_trans:.4f}, N={n}."
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
                f"MR-005 PASSED: {lang_name} round-trip translation has no "
                "significant quality impact. " + "; ".join(reason_parts) + ". "
                f"Cohen's r={effect_r:.3f}, N={n}. "
                f"mean_original={mean_orig:.4f}, mean_roundtrip={mean_trans:.4f}."
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


# ---------------------------------------------------------------------------
# Vocabulary substitution (module-private)
# ---------------------------------------------------------------------------


def _apply_vocabulary_substitution(text: str, language: TranslationLanguage) -> str:
    """Apply vocabulary substitutions simulating round-trip translation drift.

    Substitutions target whole words only (using word boundary matching) to
    avoid partial word corruption.  The substitutions are applied sequentially;
    once a token has been substituted it is not re-substituted by a later rule.

    Args:
        text: Original English user message.
        language: The intermediate language determining which substitution
            table is applied.

    Returns:
        Text with vocabulary substitutions applied (simulating back-translation
        wording drift from the specified language).
    """
    substitutions = _SUBSTITUTIONS_BY_LANGUAGE.get(language, [])
    result = text

    for original, replacement in substitutions:
        # Word-boundary match to avoid partial substitution
        pattern = r"\b" + re.escape(original) + r"\b"
        result = re.sub(pattern, replacement, result, flags=re.IGNORECASE)

    return result
