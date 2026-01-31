# Acceptance Criteria: Software Engineering Domain

<!--
DOCUMENT: acceptance-criteria.md
VERSION: 1.0.0
DOMAIN: software-engineering
TASK: TASK-038 (Phase 3)
STATUS: DESIGN COMPLETE

DISCLAIMER: This guidance is AI-generated based on NASA Systems Engineering
standards. It is advisory only and does not constitute official NASA guidance.
-->

---

## Acceptance Criteria Matrix

| ID | Criterion | Verification Method | Status |
|----|-----------|---------------------|--------|
| **SE-AC-001** | Entity definitions cover: commitment, blocker, decision, action_item, risk | Schema validation | ✅ Pass |
| **SE-AC-002** | Each entity has ≥3 meaningful attributes | Manual review | ✅ Pass |
| **SE-AC-003** | Extraction rules include ≥4 patterns per entity type | Pattern count | ✅ Pass |
| **SE-AC-004** | Patterns cover common standup/planning terminology | Domain expert review | ✅ Pass |
| **SE-AC-005** | Prompt template includes all {{$variable}} placeholders | Template validation | ✅ Pass |
| **SE-AC-006** | Prompt template provides clear extraction instructions | Manual review | ✅ Pass |
| **SE-AC-007** | Output format aligns with SPEC-context-injection.md schema | Schema validation | ✅ Pass |
| **SE-AC-008** | Validation criteria defined for transcript testing | Checklist review | ✅ Pass |

---

## Detailed Verification

### SE-AC-001: Entity Coverage

**Criterion:** Entity definitions cover: commitment, blocker, decision, action_item, risk

**Evidence:**
```yaml
entities:
  commitment: ✓ Defined with 5 attributes
  blocker: ✓ Defined with 5 attributes
  decision: ✓ Defined with 5 attributes
  action_item: ✓ Defined with 5 attributes
  risk: ✓ Defined with 5 attributes
```

**Result:** ✅ Pass (5/5 entities defined)

---

### SE-AC-002: Attribute Completeness

**Criterion:** Each entity has ≥3 meaningful attributes

**Evidence:**

| Entity | Attribute Count | Attributes |
|--------|-----------------|------------|
| commitment | 5 | assignee, work_item, sprint, confidence, story_points |
| blocker | 5 | reporter, description, dependency, severity, status |
| decision | 5 | topic, outcome, rationale, participants, scope |
| action_item | 5 | owner, task, due_date, context, priority |
| risk | 5 | description, likelihood, impact, mitigation, owner |

**Result:** ✅ Pass (all entities have ≥3 attributes)

---

### SE-AC-003: Pattern Coverage

**Criterion:** Extraction rules include ≥4 patterns per entity type

**Evidence:**

| Entity Type | Pattern Count |
|-------------|---------------|
| commitment_patterns | 6 |
| blocker_patterns | 6 |
| decision_patterns | 6 |
| action_item_patterns | 6 |
| risk_patterns | 6 |

**Result:** ✅ Pass (all have ≥4 patterns)

---

### SE-AC-004: Terminology Coverage

**Criterion:** Patterns cover common standup/planning terminology

**Evidence:**

| Meeting Type | Key Terms Covered |
|--------------|-------------------|
| Standup | "I will", "blocked on", "waiting for" |
| Planning | "committing to", "risk is", "dependency" |
| Retro | "we decided", "action item", "concern about" |
| Code Review | "let's go with", "TODO", "need to" |

**Result:** ✅ Pass (common terminology covered)

---

### SE-AC-005: Template Variables

**Criterion:** Prompt template includes all {{$variable}} placeholders

**Evidence:**

| Variable | Present | Usage |
|----------|---------|-------|
| `{{$transcript_type}}` | ✓ | Context header |
| `{{$team_name}}` | ✓ | Context section |
| `{{$sprint_number}}` | ✓ | Context section |
| `{{$meeting_date}}` | ✓ | Context section |
| `{{$participants}}` | ✓ | Context section |
| `{{$output_schema}}` | ✓ | Output format |

**Result:** ✅ Pass (all variables present)

---

### SE-AC-006: Extraction Instructions

**Criterion:** Prompt template provides clear extraction instructions

**Evidence:**

| Entity | Instructions Include |
|--------|---------------------|
| commitment | ✓ Fields to extract, example phrases |
| blocker | ✓ Fields to extract, example phrases |
| decision | ✓ Fields to extract, example phrases |
| action_item | ✓ Fields to extract, example phrases |
| risk | ✓ Fields to extract, example phrases |

**Result:** ✅ Pass (clear instructions for all entities)

---

### SE-AC-007: Schema Alignment

**Criterion:** Output format aligns with SPEC-context-injection.md schema

**Evidence:**

| Schema Element | SPEC Requirement | Implementation |
|----------------|------------------|----------------|
| metadata section | ✓ Required | ✓ Included |
| entities section | ✓ Required | ✓ Included |
| source_quote field | ✓ Required | ✓ Per entity |
| confidence levels | ✓ high/medium/low | ✓ Matches |
| summary section | ✓ Optional | ✓ Included |

**Result:** ✅ Pass (aligns with SPEC schema)

---

### SE-AC-008: Validation Criteria

**Criterion:** Validation criteria defined for transcript testing

**Evidence:**

This document defines:
1. ✓ Acceptance criteria with IDs
2. ✓ Verification methods per criterion
3. ✓ Evidence requirements
4. ✓ Pass/fail status tracking

**Result:** ✅ Pass (validation criteria defined)

---

## Transcript Testing Criteria (FEAT-002)

The following criteria will be validated with real transcripts in FEAT-002:

| Test ID | Test Description | Expected Result |
|---------|------------------|-----------------|
| TT-SE-001 | Extract commitments from standup | ≥80% recall |
| TT-SE-002 | Extract blockers from standup | ≥85% recall |
| TT-SE-003 | Extract decisions from planning | ≥75% recall |
| TT-SE-004 | Extract action items | ≥80% recall |
| TT-SE-005 | Correct attribution to speakers | ≥90% accuracy |
| TT-SE-006 | False positive rate | ≤10% |

---

## Summary

| Category | Criteria | Passed | Failed |
|----------|----------|--------|--------|
| Design Criteria | 8 | 8 | 0 |
| Testing Criteria | 6 | Deferred | Deferred |

**Overall Status:** ✅ Design Complete (8/8 criteria passed)

---

*Document ID: VAL-SE-001*
*Domain: software-engineering*
*Task: TASK-038*
*Status: DESIGN COMPLETE*
