"""TranslationLanguage enumeration for MR-005 Language Round-Trip.

Extracted to a separate file per H-10 (one class per file).

Domain isolation: MUST NOT import DeepEval, promptfoo, or any adapter (H-07).
"""

from __future__ import annotations

from enum import Enum


class TranslationLanguage(str, Enum):
    """Supported round-trip translation languages.

    Priority order from behavioral-contracts.md Section C.5.
    """

    FRENCH = "fr"
    GERMAN = "de"
    SPANISH = "es"
