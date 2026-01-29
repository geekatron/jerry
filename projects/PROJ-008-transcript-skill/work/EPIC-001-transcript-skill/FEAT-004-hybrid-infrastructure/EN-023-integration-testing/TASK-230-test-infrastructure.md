# TASK-230: Integration Test Infrastructure Setup

<!--
TEMPLATE: Task
SOURCE: ONTOLOGY-v1.md Section 3.4.6
VERSION: 1.0.0
CREATED: 2026-01-29 (EN-023 Integration Testing)
PURPOSE: Set up test infrastructure for hybrid architecture testing
-->

---

## Frontmatter

```yaml
# === IDENTITY ===
id: "TASK-230"
work_type: TASK

# === CORE METADATA ===
title: "Integration Test Infrastructure Setup"
description: |
  Set up the test infrastructure for EN-023 Integration Testing including:
  - Directory structure per DEC-012 (tests/{unit,integration,contract,llm}/transcript/)
  - pytest configuration with markers (unit, integration, llm, slow)
  - Shared fixtures in conftest.py files
  - CI configuration to exclude LLM tests

# === CLASSIFICATION ===
classification: ENABLER

# === LIFECYCLE STATE ===
status: DONE
resolution: COMPLETED

# === PRIORITY ===
priority: HIGH

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
  - "infrastructure"
  - "pytest"
  - "CI"

# === DELIVERY ITEM PROPERTIES ===
effort: 2
acceptance_criteria: |
  AC-1: Test directory structure created per DEC-012 D-003
  AC-2: pytest.ini configured with markers (unit, integration, contract, llm, slow)
  AC-3: conftest.py files created with shared fixtures
  AC-4: CI config excludes llm marker tests
due_date: null

# === TASK-SPECIFIC PROPERTIES ===
activity: DEVELOPMENT
original_estimate: 2
remaining_work: 2
time_spent: null
```

---

## State Machine

**Current State:** `DONE`

---

## Description

### Purpose

This task sets up the foundational test infrastructure that all subsequent EN-023 tasks depend on. Per **DEC-012 Hybrid Testing Strategy**, tests are organized into:

1. **Python-Layer Tests** (fast, CI-friendly)
2. **LLM Validation Tests** (slow, on-demand)

### Directory Structure (DEC-012 D-003)

```
tests/
├── unit/
│   └── transcript/
│       ├── conftest.py           # Unit test fixtures
│       ├── test_vtt_parser.py    # VTTParser unit tests
│       └── test_chunker.py       # TranscriptChunker unit tests
├── integration/
│   └── transcript/
│       ├── conftest.py           # Integration fixtures
│       ├── test_parser_chunker.py  # Parser → Chunker
│       └── test_pipeline.py      # Python pipeline
├── contract/
│   └── transcript/
│       ├── conftest.py           # Contract fixtures
│       ├── test_canonical_schema.py
│       ├── test_index_schema.py
│       └── test_chunk_schema.py
└── llm/
    └── transcript/
        ├── conftest.py           # LLM test fixtures
        ├── test_extractor_chunked.py
        ├── test_e2e_pipeline.py
        └── test_quality_gate.py
```

### pytest Configuration

```ini
# pytest.ini additions
[pytest]
markers =
    unit: Unit tests (fast, no I/O)
    integration: Integration tests (filesystem, fast)
    contract: Contract/schema validation tests
    llm: LLM agent tests (slow, expensive)
    slow: Slow tests (> 5 seconds)
```

### CI Configuration

```yaml
# CI should run with:
pytest -m "not llm" --cov=src/transcript
```

---

## Acceptance Criteria

- [x] AC-1: Test directory structure created per DEC-012 D-003
- [x] AC-2: pytest.ini configured with markers (unit, integration, contract, llm, slow)
- [x] AC-3: conftest.py files created with shared fixtures
- [x] AC-4: CI config excludes llm marker tests

---

## Implementation Notes

### Fixtures to Create

**tests/integration/transcript/conftest.py:**
```python
import pytest
from pathlib import Path

@pytest.fixture
def golden_vtt_path() -> Path:
    """Path to meeting-006 golden VTT file."""
    return Path("skills/transcript/test_data/transcripts/golden/meeting-006-all-hands.vtt")

@pytest.fixture
def temp_output_dir(tmp_path: Path) -> Path:
    """Temporary directory for test outputs."""
    output = tmp_path / "transcript_output"
    output.mkdir()
    return output
```

**tests/llm/transcript/conftest.py:**
```python
import pytest

@pytest.fixture(scope="module")
def skip_llm_if_no_api():
    """Skip LLM tests if no API access configured."""
    # Check for API availability
    pass
```

---

## Related Items

- Parent: [EN-023 Integration Testing](./EN-023-integration-testing.md)
- Decision: [DEC-012 Hybrid Testing Strategy](../FEAT-004--DEC-012-hybrid-testing-strategy.md)
- Depends On: None (first task in EN-023)
- Blocks: TASK-231, TASK-232, TASK-233, TASK-234

---

## Time Tracking

| Metric            | Value |
|-------------------|-------|
| Original Estimate | 2 hours |
| Remaining Work    | 0 hours |
| Time Spent        | 1 hour |

---

## Evidence

### Deliverables

| Deliverable | Type | Link |
|-------------|------|------|
| Test directory structure | Directory | `tests/{unit,integration,contract,llm}/transcript/` |
| pytest.ini updates | Configuration | `pytest.ini` |
| conftest.py files | Python | `tests/*/transcript/conftest.py` |

### Verification

- [x] Acceptance criteria verified
- [x] `pytest --collect-only -m "not llm"` works (2231 tests collected)
- [x] `pytest --collect-only -m llm` works (empty, as expected - no llm tests yet)
- [ ] Reviewed by: Human

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-01-29 | BACKLOG | Created per DEC-012 restructuring |
| 2026-01-29 | IN_PROGRESS | Started test infrastructure setup |
| 2026-01-29 | DONE | Completed - all 4 ACs verified |

---

## Implementation Details

### Files Created/Modified

**New Files:**
- `tests/unit/transcript/__init__.py` - Unit test module docstring
- `tests/unit/transcript/conftest.py` - Sample VTT/SRT/TXT content fixtures
- `tests/integration/transcript/__init__.py` - Integration test module docstring
- `tests/integration/transcript/conftest.py` - Golden dataset path and temp dir fixtures
- `tests/contract/transcript/__init__.py` - Contract test module docstring
- `tests/contract/transcript/conftest.py` - JSON schema loading fixtures
- `tests/llm/__init__.py` - LLM test package docstring
- `tests/llm/transcript/__init__.py` - LLM test module docstring with warnings
- `tests/llm/transcript/conftest.py` - LLM test config and chunked input fixtures

**Modified Files:**
- `pytest.ini` - Added `llm` and `slow` markers
- `.github/workflows/ci.yml` - Added `not llm` to pytest marker exclusions

### Verification Evidence

```bash
# Directory structure verified
$ ls tests/{unit,integration,contract,llm}/transcript/
tests/contract/transcript/:
__init__.py  conftest.py  test_chunk_schemas.py

tests/integration/transcript/:
__init__.py  conftest.py

tests/llm/transcript/:
__init__.py  conftest.py

tests/unit/transcript/:
__init__.py  conftest.py  test_chunker.py  test_vtt_parser.py

# pytest markers verified
$ grep -A2 "llm:" pytest.ini
    llm: marks tests that invoke LLM agents (slow, expensive, excluded from CI)
    slow: marks tests that take > 5 seconds (e.g., large file processing)

# CI exclusion verified
$ grep "not llm" .github/workflows/ci.yml
            -m "not subprocess and not llm" \
            -m "not subprocess and not llm" \
            -m "not llm" \
            -m "not llm" \
```
