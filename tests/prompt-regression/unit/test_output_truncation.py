# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Victor Lau

"""Unit tests for DeepEvalAdapter output truncation constant — CG-017.

Verifies that:
  - _MAX_OUTPUT_CHARS is importable from jerry.testing.evaluation.deepeval_adapter.
  - _MAX_OUTPUT_CHARS equals 8000 per the design specification.
  - DeepEvalAdapter is importable (transitively confirming the module loads).

No LLM calls are performed. No network I/O. No filesystem side effects.

References:
    - CG-017: Output truncation constant _MAX_OUTPUT_CHARS = 8000
    - H-20: BDD test-first (90% line coverage target)
"""

from __future__ import annotations

import pytest

from jerry.testing.evaluation import deepeval_adapter as _da_module


class TestMaxOutputCharsConstant:
    """Unit tests for the _MAX_OUTPUT_CHARS module-level constant (CG-017).

    Verifies presence, type, and value of the constant that guards against
    unbounded token consumption in the DeepEval LLM judge.
    """

    @pytest.mark.unit
    def test_max_output_chars_constant_should_exist_on_module(self) -> None:
        """_MAX_OUTPUT_CHARS must be accessible as a module attribute.

        Importability confirms the module loads without error and the constant
        was not accidentally removed or renamed during gap closure.
        """
        assert hasattr(_da_module, "_MAX_OUTPUT_CHARS"), (
            "_MAX_OUTPUT_CHARS not found on jerry.testing.evaluation.deepeval_adapter. "
            "CG-017 requires this constant to guard against unbounded token consumption."
        )

    @pytest.mark.unit
    def test_max_output_chars_should_equal_8000(self) -> None:
        """_MAX_OUTPUT_CHARS must be exactly 8000 per CG-017 specification.

        The value 8000 was chosen to balance evaluation quality (sufficient
        output visible to the LLM judge) against token cost (preventing
        oversized payloads from exhausting the context window budget).
        """
        assert _da_module._MAX_OUTPUT_CHARS == 8000, (  # noqa: SLF001
            f"Expected _MAX_OUTPUT_CHARS == 8000 (CG-017), got {_da_module._MAX_OUTPUT_CHARS!r}"
        )

    @pytest.mark.unit
    def test_max_output_chars_should_be_an_integer(self) -> None:
        """_MAX_OUTPUT_CHARS must be an int, not a float or string.

        String slicing (output_text[:_MAX_OUTPUT_CHARS]) requires an integer
        index. A non-integer constant would cause a TypeError at runtime.
        """
        assert isinstance(_da_module._MAX_OUTPUT_CHARS, int), (  # noqa: SLF001
            f"Expected _MAX_OUTPUT_CHARS to be int, "
            f"got {type(_da_module._MAX_OUTPUT_CHARS).__name__}"
        )

    @pytest.mark.unit
    def test_deepeval_adapter_class_should_be_importable(self) -> None:
        """DeepEvalAdapter class must be importable from the module.

        This test exercises the module's class-level imports without
        constructing an instance (which requires ANTHROPIC_API_KEY).
        """
        from jerry.testing.evaluation.deepeval_adapter import DeepEvalAdapter  # noqa: PLC0415

        assert DeepEvalAdapter is not None
