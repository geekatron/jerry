# EN-004: ContextFillEstimator + ResumptionContextGenerator

> **Type:** enabler
> **Status:** pending
> **Priority:** critical
> **Impact:** high
> **Enabler Type:** architecture
> **Created:** 2026-02-19
> **Due:** --
> **Completed:** --
> **Parent:** FEAT-001
> **Owner:** --
> **Effort:** 3-5h

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Technical scope |
| [Acceptance Criteria](#acceptance-criteria) | BDD scenarios and checklist |
| [Dependencies](#dependencies) | What this enables |
| [History](#history) | Status changes |

---

## Summary

Complete the remaining application services and infrastructure adapters for the `context_monitoring` bounded context. Creates `ContextFillEstimator` (fill estimation + XML tag generation), `ResumptionContextGenerator` (checkpoint-to-XML conversion), `ITranscriptReader` port, and `JsonlTranscriptReader` adapter.

**Technical Scope:**
- `application/services/context_fill_estimator.py` — ContextFillEstimator
- `application/services/resumption_context_generator.py` — ResumptionContextGenerator
- `application/ports/transcript_reader.py` — ITranscriptReader Protocol
- `infrastructure/adapters/jsonl_transcript_reader.py` — JsonlTranscriptReader
- Composition root wiring in `bootstrap.py`

**Key behaviors:**
- ContextFillEstimator reads transcript via port, computes FillEstimate, determines ThresholdTier, generates `<context-monitor>` XML (40-200 tokens)
- ResumptionContextGenerator receives CheckpointData, generates `<resumption-context>` XML (~760 token budget)
- JsonlTranscriptReader reads `$TRANSCRIPT_PATH` JSONL, extracts `input_tokens` from latest entry via seek-to-end for O(1)

---

## Acceptance Criteria

### BDD Scenarios (pytest-bdd)

```gherkin
Feature: ContextFillEstimator determines fill level and tier

  Scenario Outline: Correct tier classification
    Given a transcript with <input_tokens> tokens and context window of 200000
    When ContextFillEstimator.estimate() is called
    Then the fill_percentage should be <fill_pct>
    And the threshold_tier should be <tier>

    Examples:
      | input_tokens | fill_pct | tier      |
      | 100000       | 0.50     | NOMINAL   |
      | 115000       | 0.575    | LOW       |
      | 150000       | 0.75     | WARNING   |
      | 170000       | 0.85     | CRITICAL  |
      | 180000       | 0.90     | EMERGENCY |

  Scenario: XML tag generated with tier-appropriate content
    Given a fill estimate at WARNING tier
    When ContextFillEstimator generates the context-monitor tag
    Then the output should be XML containing fill percentage and recommended action
    And the output should be between 40 and 200 tokens

  Scenario: Fail-open on transcript read error
    Given ITranscriptReader raises FileNotFoundError
    When ContextFillEstimator.estimate() is called
    Then it should return a NOMINAL tier estimate
    And no exception should propagate


Feature: ResumptionContextGenerator creates session-start XML

  Scenario: Generate resumption context from checkpoint
    Given a CheckpointData with resumption_state containing recovery info
    When ResumptionContextGenerator.generate() is called
    Then the output should be a <resumption-context> XML string
    And it should be within 760 token budget

  Scenario: No resumption data returns empty string
    Given a CheckpointData with resumption_state = None
    When ResumptionContextGenerator.generate() is called
    Then the output should be an empty string


Feature: JsonlTranscriptReader extracts tokens from JSONL

  Scenario: Read input_tokens from valid JSONL transcript
    Given a JSONL file with entries containing input_tokens fields
    When JsonlTranscriptReader.read_latest_tokens() is called
    Then it should return the input_tokens from the last entry

  Scenario: Missing transcript file raises FileNotFoundError
    Given no file at the transcript path
    When JsonlTranscriptReader.read_latest_tokens() is called
    Then FileNotFoundError should be raised

  Scenario: Empty file raises ValueError
    Given an empty JSONL file
    When JsonlTranscriptReader.read_latest_tokens() is called
    Then ValueError should be raised
```

### Acceptance Checklist

- [ ] `ContextFillEstimator.estimate(transcript_path: str) -> FillEstimate` with type hints and docstring (H-11, H-12)
- [ ] Correct tier boundaries: NOMINAL (<0.55), LOW (0.55-0.70), WARNING (0.70-0.80), CRITICAL (0.80-0.88), EMERGENCY (>0.88)
- [ ] `<context-monitor>` XML tag generated with fill %, tier, recommended action
- [ ] Fail-open: transcript errors return NOMINAL estimate
- [ ] `ResumptionContextGenerator.generate(checkpoint: CheckpointData) -> str` (H-11, H-12)
- [ ] Empty string when `resumption_state` is None
- [ ] `<resumption-context>` XML within ~760 token budget
- [ ] `ITranscriptReader` Protocol defined (H-11, H-12)
- [ ] `JsonlTranscriptReader` reads from tail of JSONL efficiently
- [ ] `bootstrap.py` wires all services and adapters
- [ ] H-07: no external imports in domain layer. H-08: no infrastructure imports in application
- [ ] Unit tests for all 5 tier boundaries, fail-open, XML generation, token budget
- [ ] One class per file (H-10)

---

## Dependencies

**Depends On:**
- EN-003 (domain value objects, CheckpointService, ICheckpointRepository)
- EN-002 (IThresholdConfiguration port)

**Enables:**
- EN-006 (CLI commands use these services)
- ST-002 (AE-006 sub-rules reference context-monitor signals)
- SPIKE-003 (validates JsonlTranscriptReader accuracy)

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-02-19 | Claude | pending | Enabler created from CWI-03 + merged CWI-06. |
