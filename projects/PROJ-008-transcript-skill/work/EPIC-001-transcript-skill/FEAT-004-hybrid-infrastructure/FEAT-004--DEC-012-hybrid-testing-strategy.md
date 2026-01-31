# FEAT-004:DEC-012: Hybrid Testing Strategy

<!--
TEMPLATE: Decision
VERSION: 1.0.0
SOURCE: worktracker.md (Decision File), ADR/MADR best practices
CREATED: 2026-01-29 (EN-023 Integration Testing Planning)
PURPOSE: Document testing strategy for hybrid Python+LLM architecture
-->

> **Type:** decision
> **Status:** ACCEPTED
> **Priority:** HIGH
> **Created:** 2026-01-29T21:00:00Z
> **Parent:** FEAT-004
> **Owner:** User
> **Related:** DEC-011, EN-023, EN-020, EN-021, EN-022

---

## Frontmatter

```yaml
id: "FEAT-004:DEC-012"
work_type: DECISION
title: "Hybrid Testing Strategy"

status: ACCEPTED
priority: HIGH

created_by: "Claude"
participants:
  - "User"
  - "Claude"

created_at: "2026-01-29T21:00:00Z"
updated_at: "2026-01-29T21:00:00Z"
decided_at: "2026-01-29T21:00:00Z"

parent_id: "FEAT-004"

tags:
  - "testing"
  - "integration"
  - "hybrid"
  - "CI/CD"
  - "LLM-validation"

superseded_by: null
supersedes: null

decision_count: 3
```

---

## State Machine

**Current State:** `ACCEPTED`

```
PENDING → DOCUMENTED → ACCEPTED
                          ↑
                     (current)
```

---

## Summary

This decision captures the hybrid testing strategy for EN-023 Integration Testing. The strategy separates fast, deterministic Python tests (suitable for CI) from slow, expensive LLM validation tests (run on-demand when making changes to the transcription service).

**Decisions Captured:** 3

**Key Outcomes:**
- Two-tier testing strategy: Fast Python (CI) + Slow LLM (validation)
- EN-023 restructured from 6 tasks to 8 tasks for clearer separation
- Test directory structure defined at `tests/integration/transcript/`
- Specifications-first approach: Design tests before implementation

---

## Decision Context

### Background

During EN-023 Integration Testing planning, the original 6-task structure mixed Python-layer tests with LLM validation tests. This created confusion about:
1. Which tests should run in CI (fast, deterministic)
2. Which tests require LLM invocation (slow, expensive, but real validation)
3. How to structure the test hierarchy

The user clarified that a **hybrid testing solution** is needed:
- Python-layer integration tests that run quickly and can be part of CI
- LLM validation tests that are expensive but provide real end-to-end validation

### Constraints

- **Cost Control**: LLM tests are expensive and should not run on every commit
- **CI Speed**: CI pipeline should complete in reasonable time (< 5 minutes for integration tests)
- **Real Validation**: Need ability to validate full pipeline including LLM agents
- **Clear Separation**: Developers must know which tests to run when

### Stakeholders

| Stakeholder | Role | Interest |
|-------------|------|----------|
| User | Product Owner | Cost control, real validation when needed |
| Claude | Implementer | Clear task separation, testable components |
| CI System | Automation | Fast, deterministic tests only |
| Future Developers | Maintainers | Know which tests to run when |

---

## Decisions

### D-001: Two-Tier Testing Strategy

**Date:** 2026-01-29
**Participants:** User, Claude

#### Question/Context

Claude asked about testing approach for EN-023:

> "Q2. Testing Philosophy - How comprehensive should EN-023 be?"
>
> Options:
> - A) Lightweight integration tests (quick validation)
> - B) Full pipeline tests with LLM invocation (comprehensive but expensive)
> - C) Hybrid with toggles for quick vs comprehensive
> - D) Contract tests only (verify interfaces, not behavior)

User responded:

> "Q2. We need a hybrid solution. We want an integration layer we can run all the time and then we want a way to be able to invoke the LLM agents as part of tests (expensive, slow, but real validation) for when we make changes to the transcription service"

#### Options Considered

| Option | Description | Pros | Cons |
|--------|-------------|------|------|
| **A** | Lightweight only | Fast CI, cheap | No real LLM validation |
| **B** | Full LLM always | Real validation | Expensive, slow CI |
| **C (Chosen)** | Hybrid with clear separation | Best of both worlds | More test organization needed |
| **D** | Contract tests only | Very fast | No behavioral validation |

#### Decision

**We decided:** Two-tier testing strategy with clear separation:

**Tier 1: Python-Layer Tests (Fast, CI)**
- Parser unit tests (VTTParser)
- Chunker service tests (TranscriptChunker)
- Parser → Chunker integration tests
- Contract tests for output schemas
- **Run:** On every commit, in CI pipeline
- **Markers:** `@pytest.mark.unit`, `@pytest.mark.integration`

**Tier 2: LLM Validation Tests (Slow, On-Demand)**
- ts-extractor chunked input validation
- Full pipeline E2E tests
- ps-critic quality gate validation
- **Run:** On-demand, when changing transcription service
- **Markers:** `@pytest.mark.llm`, `@pytest.mark.slow`
- **Invocation:** `pytest -m llm` or dedicated script

#### Rationale

1. **Cost Efficiency**: LLM tests only run when needed, not on every commit
2. **CI Speed**: Python tests complete quickly, keeping CI responsive
3. **Real Validation**: LLM tests provide ground truth when making changes
4. **Developer Experience**: Clear markers indicate test category and run-time

#### Implications

- **Positive:** Fast CI, controlled costs, real validation when needed
- **Negative:** Requires discipline to run LLM tests before PRs affecting transcription
- **Follow-up required:** CI configuration to exclude `llm` marker tests

---

### D-002: EN-023 Task Restructuring (6 → 8 Tasks)

**Date:** 2026-01-29
**Participants:** User, Claude

#### Question/Context

Claude proposed restructuring EN-023 from 6 tasks to 7-8 tasks for clearer separation between Python-layer tests and LLM validation tests:

> "The original 6 tasks mixed Python and LLM tests. Should we:
> - A) Keep 6 tasks (current structure)
> - B) Restructure into 7-8 tasks with clearer separation"

User responded:

> "B) Restructure into 7-8 tasks with clearer separation. Yes capture a decision for this first before building out the tasks."

#### Options Considered

| Option | Description | Pros | Cons |
|--------|-------------|------|------|
| **A** | Keep 6 tasks | Less files to create | Mixed concerns per task |
| **B (Chosen)** | Restructure to 8 tasks | Clear separation, better traceability | More files, more overhead |

#### Decision

**We decided:** Restructure EN-023 into 8 tasks:

**Python-Layer Tasks (TASK-230..233):**
| Task ID | Title | Type | CI |
|---------|-------|------|-----|
| TASK-230 | Integration Test Infrastructure Setup | Setup | - |
| TASK-231 | Parser → Chunker Integration Tests | Python | ✓ |
| TASK-232 | Chunker Output Contract Tests | Python | ✓ |
| TASK-233 | Python-Layer Pipeline Tests | Python | ✓ |

**LLM Validation Tasks (TASK-234..237):**
| Task ID | Title | Type | CI |
|---------|-------|------|-----|
| TASK-234 | LLM Integration Test Framework | Setup | - |
| TASK-235 | ts-extractor Chunked Input Validation | LLM | ✗ |
| TASK-236 | Full Pipeline E2E Test | LLM | ✗ |
| TASK-237 | ps-critic Quality Gate Test | LLM | ✗ |

#### Rationale

1. **Single Responsibility**: Each task has one clear concern
2. **CI Clarity**: TASK-231..233 explicitly marked as CI tests
3. **LLM Isolation**: TASK-235..237 clearly marked as expensive tests
4. **Infrastructure First**: TASK-230 and TASK-234 set up foundations
5. **Traceability**: Clear mapping from tier to task IDs

#### Implications

- **Positive:** Clear separation, easy to understand scope per task
- **Negative:** More task files to create and maintain
- **Follow-up required:** Create all 8 TASK-*.md files following this structure

---

### D-003: Test Directory Structure

**Date:** 2026-01-29
**Participants:** User, Claude

#### Question/Context

Claude asked about test directory organization for the hybrid testing strategy.

#### Decision

**We decided:** Test directory structure at `tests/integration/transcript/`:

```
tests/
├── unit/
│   └── transcript/
│       ├── test_vtt_parser.py          # Parser unit tests
│       └── test_chunker.py             # Chunker unit tests
├── integration/
│   └── transcript/
│       ├── conftest.py                 # Shared fixtures
│       ├── test_parser_chunker.py      # Parser → Chunker integration
│       └── test_pipeline.py            # Python pipeline tests
├── contract/
│   └── transcript/
│       ├── test_canonical_schema.py    # canonical-transcript.json schema
│       ├── test_index_schema.py        # index.json schema
│       └── test_chunk_schema.py        # chunk-NNN.json schema
└── llm/
    └── transcript/
        ├── conftest.py                 # LLM test fixtures
        ├── test_extractor_chunked.py   # ts-extractor validation
        ├── test_e2e_pipeline.py        # Full pipeline E2E
        └── test_quality_gate.py        # ps-critic validation
```

#### Rationale

1. **Pytest Best Practice**: Organize by test type (unit, integration, contract, llm)
2. **Clear Markers**: Directory structure mirrors pytest markers
3. **CI Exclusion**: `llm/` directory easily excluded from CI runs
4. **Shared Fixtures**: conftest.py in each directory for appropriate scope

#### Implications

- **Positive:** Clear organization, easy CI configuration
- **Negative:** Multiple conftest.py files to maintain
- **Follow-up required:** pytest.ini configuration for markers

---

## Decision Summary

| ID | Decision | Date | Status |
|----|----------|------|--------|
| D-001 | Two-tier testing: Fast Python (CI) + Slow LLM (validation) | 2026-01-29 | ACCEPTED |
| D-002 | EN-023 restructured from 6 to 8 tasks for clear separation | 2026-01-29 | ACCEPTED |
| D-003 | Test directory structure at tests/{unit,integration,contract,llm}/transcript/ | 2026-01-29 | ACCEPTED |

---

## Related Artifacts

| Type | Path | Description |
|------|------|-------------|
| Parent | [FEAT-004-hybrid-infrastructure.md](./FEAT-004-hybrid-infrastructure.md) | Parent feature |
| Decision | [DEC-011](./FEAT-004--DEC-011-ts-parser-hybrid-role.md) | ts-parser hybrid role |
| Enabler | [EN-020-python-parser](./EN-020-python-parser/EN-020-python-parser.md) | Python VTT parser |
| Enabler | [EN-021-chunking-strategy](./EN-021-chunking-strategy/EN-021-chunking-strategy.md) | Chunking service |
| Enabler | [EN-022-extractor-adaptation](./EN-022-extractor-adaptation/EN-022-extractor-adaptation.md) | Extractor adaptation |
| Enabler | [EN-023-integration-testing](./EN-023-integration-testing/EN-023-integration-testing.md) | Integration testing (target) |

---

## Document History

| Date | Author | Change |
|------|--------|--------|
| 2026-01-29T21:00:00Z | Claude | Created decision document from user feedback |

---

## Metadata

```yaml
id: "FEAT-004:DEC-012"
parent_id: "FEAT-004"
work_type: DECISION
title: "Hybrid Testing Strategy"
status: ACCEPTED
priority: HIGH
created_by: "Claude"
created_at: "2026-01-29T21:00:00Z"
updated_at: "2026-01-29T21:00:00Z"
decided_at: "2026-01-29T21:00:00Z"
participants: ["User", "Claude"]
tags: ["testing", "integration", "hybrid", "CI/CD", "LLM-validation"]
decision_count: 3
superseded_by: null
supersedes: null
```
