# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Victor Lau

# CG-008

"""Extraction adapters for external test-runner result formats.

This package provides adapters that read output files produced by external
CI/CD test runners (promptfoo, deepeval, etc.) and convert them into the
internal ``ScoreArray`` type used by the Four-Layer Composite Test Harness
statistical engine (Layer 4).

Architecture (H-07 compliance):
    - ADAPTER layer (inbound): translates external JSON formats into domain
      types (``ScoreArray``).
    - MUST NOT be imported by domain modules (``stats.py``, ``types.py``).

H-10 compliance (one class/primary function per file):
    promptfoo_extractor.py -- ``extract_score_arrays()``

Public API:
    from jerry.testing.extraction import extract_score_arrays
"""

from jerry.testing.extraction.promptfoo_extractor import extract_score_arrays

__all__ = ["extract_score_arrays"]
