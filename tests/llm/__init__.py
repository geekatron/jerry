"""LLM integration tests (slow, expensive).

This test package contains tests that invoke LLM agents:
- transcript/ - Transcript skill LLM validation tests

WARNING: These tests are:
- SLOW (minutes per test)
- EXPENSIVE (token costs)
- EXCLUDED FROM CI

Run manually: pytest -m llm tests/llm/
"""
