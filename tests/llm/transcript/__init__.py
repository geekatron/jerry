"""LLM validation tests for transcript skill.

Tests in this module:
- ts-extractor chunked input validation
- Full pipeline E2E tests
- ps-critic quality gate tests

WARNING: These tests invoke LLM agents and are:
- SLOW (minutes per test)
- EXPENSIVE (token costs)
- EXCLUDED FROM CI (use pytest -m llm to run)

Run manually with: pytest -m llm tests/llm/transcript/
"""
