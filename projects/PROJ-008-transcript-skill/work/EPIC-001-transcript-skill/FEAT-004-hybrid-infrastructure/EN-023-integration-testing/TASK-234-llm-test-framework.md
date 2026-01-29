# TASK-234: LLM Integration Test Framework

<!--
TEMPLATE: Task
SOURCE: ONTOLOGY-v1.md Section 3.4.6
VERSION: 1.0.0
CREATED: 2026-01-29 (EN-023 Integration Testing)
PURPOSE: Set up framework for LLM validation tests
-->

---

## Frontmatter

```yaml
# === IDENTITY ===
id: "TASK-234"
work_type: TASK

# === CORE METADATA ===
title: "LLM Integration Test Framework"
description: |
  Set up the test framework for LLM validation tests:
  - fixtures for LLM agent invocation
  - test utilities for comparing LLM output
  - timeout and retry handling
  - cost tracking for test runs

# === CLASSIFICATION ===
classification: ENABLER

# === LIFECYCLE STATE ===
status: BACKLOG
resolution: null

# === PRIORITY ===
priority: MEDIUM

# === PEOPLE ===
assignee: "Claude"
created_by: "Claude"

# === TIMESTAMPS ===
created_at: "2026-01-29T21:30:00Z"
updated_at: "2026-01-29T21:30:00Z"

# === HIERARCHY ===
parent_id: "EN-023"

# === TAGS ===
tags:
  - "testing"
  - "llm"
  - "framework"
  - "validation"

# === DELIVERY ITEM PROPERTIES ===
effort: 3
acceptance_criteria: |
  AC-1: LLM test fixtures created in tests/llm/transcript/conftest.py
  AC-2: Utility functions for agent invocation via Task tool
  AC-3: Output comparison utilities for extraction reports
  AC-4: Timeout handling with configurable limits
  AC-5: pytest -m llm marker correctly identifies LLM tests
due_date: null

# === TASK-SPECIFIC PROPERTIES ===
activity: DEVELOPMENT
original_estimate: 3
remaining_work: 3
time_spent: null
```

---

## State Machine

**Current State:** `BACKLOG`

---

## Description

### Purpose

This task creates the foundational framework for LLM validation tests. These tests are expensive and slow, so the framework must:
1. Make tests easy to write
2. Handle timeouts and retries
3. Track costs (token usage)
4. Provide utilities for comparing outputs

### Framework Components

**tests/llm/transcript/conftest.py:**
```python
import pytest
from pathlib import Path
from typing import Generator

@pytest.fixture(scope="module")
def llm_test_config() -> dict:
    """Configuration for LLM tests."""
    return {
        "timeout_seconds": 300,  # 5 minutes
        "max_retries": 1,
        "model": "sonnet",  # Default model
    }

@pytest.fixture
def chunked_input_path(temp_output_dir) -> Path:
    """Generate chunked input from meeting-006 for LLM tests."""
    from src.transcript.infrastructure.adapters.vtt_parser import VTTParser
    from src.transcript.application.services.chunker import TranscriptChunker

    vtt_path = Path("skills/transcript/test_data/transcripts/golden/meeting-006-all-hands.vtt")
    parser = VTTParser()
    chunker = TranscriptChunker()

    canonical = parser.parse(vtt_path)
    index_path = chunker.chunk(canonical, temp_output_dir)

    return index_path

@pytest.fixture
def extraction_report_schema() -> dict:
    """Load extraction report schema for validation."""
    import json
    schema_path = Path("skills/transcript/test_data/schemas/extraction-report.json")
    with open(schema_path) as f:
        return json.load(f)
```

**tests/llm/transcript/utils.py:**
```python
"""Utilities for LLM integration tests."""

import subprocess
import json
from pathlib import Path
from dataclasses import dataclass
from typing import Any

@dataclass
class LLMTestResult:
    """Result from an LLM test invocation."""
    success: bool
    output: dict | None
    error: str | None
    tokens_used: int
    elapsed_seconds: float

def invoke_ts_extractor(
    index_path: Path,
    output_dir: Path,
    timeout_seconds: int = 300,
) -> LLMTestResult:
    """Invoke ts-extractor agent via skill."""
    # Implementation would use subprocess or direct API
    pass

def compare_extraction_reports(
    actual: dict,
    expected: dict,
    tolerance: float = 0.10,
) -> list[str]:
    """Compare two extraction reports, returning list of differences."""
    differences = []

    # Compare counts with tolerance
    for key in ["action_items", "decisions", "questions"]:
        actual_count = actual.get("extraction_stats", {}).get(key, 0)
        expected_count = expected.get("extraction_stats", {}).get(key, 0)

        if expected_count > 0:
            ratio = abs(actual_count - expected_count) / expected_count
            if ratio > tolerance:
                differences.append(
                    f"{key}: expected ~{expected_count}, got {actual_count}"
                )

    return differences

def validate_citations(report: dict) -> list[str]:
    """Validate all citations in extraction report."""
    errors = []

    for entity_type in ["action_items", "decisions", "questions"]:
        for entity in report.get(entity_type, []):
            citation = entity.get("citation", {})
            segment_id = citation.get("segment_id")

            if not segment_id:
                errors.append(f"{entity_type}/{entity['id']}: missing segment_id")

            # Validate format
            if segment_id and not segment_id.startswith("seg-"):
                errors.append(f"{entity_type}/{entity['id']}: invalid segment_id format")

    return errors
```

---

## Acceptance Criteria

- [ ] AC-1: LLM test fixtures created in tests/llm/transcript/conftest.py
- [ ] AC-2: Utility functions for agent invocation via Task tool
- [ ] AC-3: Output comparison utilities for extraction reports
- [ ] AC-4: Timeout handling with configurable limits
- [ ] AC-5: pytest -m llm marker correctly identifies LLM tests

---

## Related Items

- Parent: [EN-023 Integration Testing](./EN-023-integration-testing.md)
- Depends On: TASK-230 (test infrastructure)
- Blocks: TASK-235, TASK-236, TASK-237
- Related: EN-022 (extraction report schema)

---

## Time Tracking

| Metric | Value |
|--------|-------|
| Original Estimate | 3 hours |
| Remaining Work | 3 hours |
| Time Spent | - |

---

## Evidence

### Deliverables

| Deliverable | Type | Link |
|-------------|------|------|
| LLM test fixtures | Python | `tests/llm/transcript/conftest.py` |
| Test utilities | Python | `tests/llm/transcript/utils.py` |

### Verification

- [ ] Acceptance criteria verified
- [ ] `pytest --collect-only -m llm` finds LLM tests
- [ ] Reviewed by: Human

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-01-29 | BACKLOG | Created per DEC-012 restructuring |
