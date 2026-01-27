# EN-007:DISC-002: Test Infrastructure Dependency Gap

<!--
TEMPLATE: Discovery
VERSION: 1.1.0
SOURCE: ONTOLOGY-v1.md Section 3.4.9, worktracker.md (Discovery File)
CREATED: 2026-01-27 (TASK-102 Pre-work Analysis)
-->

> **Type:** discovery
> **Status:** RESOLVED
> **Priority:** HIGH
> **Impact:** HIGH
> **Created:** 2026-01-27T14:00:00Z
> **Completed:** 2026-01-27T14:30:00Z
> **Parent:** EN-007
> **Owner:** Claude
> **Source:** TASK-102 Pre-work Analysis

---

## Frontmatter

```yaml
# =============================================================================
# DISCOVERY WORK ITEM
# Source: ONTOLOGY-v1.md Section 3.4.9 (Discovery Entity Schema)
# Purpose: Document task ordering dependency issue discovered during TASK-102 prep
# =============================================================================

# Identity (inherited from WorkItem)
id: "EN-007:DISC-002"
work_type: DISCOVERY
title: "Test Infrastructure Dependency Gap"

# Classification
classification: PROCESS

# State
status: RESOLVED
resolution: "Created minimal test infrastructure in skills/transcript/test_data/"

# Priority
priority: HIGH

# Impact (REQ-D-004)
impact: HIGH

# People
assignee: "Claude"
created_by: "Claude"

# Timestamps
created_at: "2026-01-27T14:00:00Z"
updated_at: "2026-01-27T14:30:00Z"
completed_at: "2026-01-27T14:30:00Z"

# Hierarchy
parent_id: "EN-007"

# Tags
tags:
  - "task-ordering"
  - "test-infrastructure"
  - "tdd-dependency"
  - "process-gap"

# =============================================================================
# DISCOVERY-SPECIFIC PROPERTIES
# =============================================================================

# Finding Classification
finding_type: DEPENDENCY_GAP
confidence_level: HIGH

# Source Information
source: "TASK-102 Pre-work Analysis"
research_method: "Dependency analysis of EN-007 vs EN-015 task ordering"

# Validation
validated: true
validation_date: "2026-01-27T14:00:00Z"
validated_by: "Human review"
```

---

## State Machine

**Current State:** `RESOLVED`

**State History:**
- 2026-01-27 14:00: DISCOVERED (dependency analysis)
- 2026-01-27 14:30: RESOLVED (minimal test infrastructure created)

---

## Containment Rules

| Rule | Value |
|------|-------|
| **Allowed Children** | None |
| **Allowed Parents** | Epic, Feature, Story, Enabler |
| **Max Depth** | 0 (leaf node) |
| **Co-Location** | MUST be in parent's folder (REQ-D-025) |

---

## Summary

**Task ordering dependency discovered:** EN-007 (Sprint 3) requires test infrastructure defined in EN-015 (Sprint 4), but EN-015 is scheduled AFTER EN-007. This violates TDD principles where tests should exist before verification.

**Key Finding:**
- TASK-102 (Verify VTT Processing) references `parser-tests.yaml`
- `parser-tests.yaml` is created by TASK-134 in EN-015
- EN-015 is Sprint 4, EN-007 is Sprint 3
- This creates a circular dependency that blocks TDD-style verification

**Resolution:** Create minimal test infrastructure in `skills/transcript/test_data/` to unblock EN-007 verification tasks, then expand to full EN-015 scope in Sprint 4.

---

## Context

### Background

During preparation for TASK-102 (Verify VTT Processing), analysis revealed that the task references test artifacts that don't exist yet:

1. **TASK-102 Acceptance Criteria** references `parser-tests.yaml`
2. **parser-tests.yaml** is defined in EN-015 (TASK-134)
3. **EN-015** is scheduled for Sprint 4
4. **EN-007** is scheduled for Sprint 3

This creates an impossible situation for TDD-style development.

### Research Question

How can we verify EN-007 parser implementation without the test infrastructure from EN-015?

### Investigation Approach

1. Analyzed EN-007 task dependencies
2. Analyzed EN-015 task structure
3. Identified minimal test infrastructure needed for EN-007
4. Proposed resolution strategy

---

## Finding

### GAP-001: Sprint Ordering Violates TDD (HIGH)

**Severity:** HIGH
**Impact:** Cannot perform TDD-style verification of EN-007 tasks

**Current Sprint Ordering:**
```
Sprint 3: EN-007 (ts-parser Implementation)
  └── TASK-102: Verify VTT Processing → needs parser-tests.yaml
  └── TASK-103: Verify SRT Processing → needs parser-tests.yaml
  └── TASK-104: Verify Plain Text Processing → needs parser-tests.yaml
  └── TASK-105A: Create Contract Tests → needs test infrastructure

Sprint 4: EN-015 (Transcript Validation)
  └── TASK-131: Create golden dataset
  └── TASK-134: Create parser-tests.yaml ← EN-007 depends on this!
```

**Problem:** EN-007 tasks cannot be completed in TDD style without EN-015 artifacts.

### GAP-002: No Test Data Location Defined

**Severity:** MEDIUM
**Impact:** No clear location for test artifacts within skill structure

**Finding:** EN-015 defines `test_data/` structure but doesn't specify where it lives relative to the skill.

---

## Resolution

### Decision: Create Minimal Test Infrastructure

**Approved by:** Human (via conversation)
**Date:** 2026-01-27

**Resolution Strategy:**

1. **Create test_data structure** in `skills/transcript/test_data/`
2. **Derive expected values** from real VTT file (deterministic for parser)
3. **Create minimal parser-tests.yaml** with first 20 cues
4. **Human reviews** derived expected values before verification
5. **Expand to full EN-015** scope in Sprint 4

### Test Data Location

```
skills/transcript/
├── agents/
│   ├── ts-parser.md
│   ├── ts-extractor.md
│   └── ts-formatter.md
├── test_data/                    ← NEW: Self-contained in skill
│   ├── transcripts/
│   │   ├── real/                 ← Real VTT files (TASK-131A)
│   │   │   └── internal-sample-sample.vtt
│   │   ├── golden/               ← Synthetic golden dataset (TASK-131)
│   │   └── edge_cases/           ← Edge case files (TASK-133)
│   ├── expected/                 ← Expected outputs for test cases
│   │   └── internal-sample-sample.expected.json
│   └── validation/
│       └── parser-tests.yaml     ← Test specifications
└── SKILL.md
```

### Scope of Minimal Infrastructure

| Artifact | Minimum for EN-007 | Full EN-015 Scope |
|----------|-------------------|-------------------|
| Real VTT sample | First 20 cues | Full file |
| Expected JSON | 20 segments | All segments |
| parser-tests.yaml | 5 test cases | Full spec |
| Golden dataset | Skip | 3 meetings |
| Edge cases | Skip | 5+ files |

---

## Implications

### Impact on Project

- **TASK-102, 103, 104** can proceed with minimal test infrastructure
- **EN-015** scope reduced for Sprint 4 (expansion only)
- **TDD principles** preserved through early test creation

### Design Decisions Affected

- **Decision:** Test data lives in `skills/transcript/test_data/` (self-contained)
- **Decision:** Real VTT files used for parser verification (deterministic)
- **Decision:** Human reviews expected values before verification

### Risks Identified

| Risk | Severity | Mitigation |
|------|----------|------------|
| Minimal tests miss edge cases | MEDIUM | Expand in EN-015 (Sprint 4) |
| Expected value derivation errors | LOW | Human review before verification |

---

## Relationships

### Creates

- `skills/transcript/test_data/` directory structure
- `parser-tests.yaml` (minimal)
- Expected output JSON for sample VTT

### Informs

- [TASK-102](./TASK-102-vtt-processing.md) - VTT Processing verification
- [TASK-103](./TASK-103-srt-processing.md) - SRT Processing verification
- [TASK-104](./TASK-104-plain-text-processing.md) - Plain text verification
- [EN-015](../EN-015-transcript-validation/EN-015-transcript-validation.md) - Full test infrastructure

### Related Discoveries

- [DISC-001](./EN-007--DISC-001-vtt-voice-tag-gaps.md) - VTT Voice Tag Parsing Gaps

---

## Evidence

### Source Documentation

| Evidence ID | Type | Description | Date |
|-------------|------|-------------|------|
| E-001 | Analysis | TASK-102 dependency on parser-tests.yaml | 2026-01-27 |
| E-002 | Analysis | EN-015 defines TASK-134 for parser-tests.yaml | 2026-01-27 |
| E-003 | Human Decision | Approved minimal test infrastructure approach | 2026-01-27 |

---

## Document History

| Date | Author | Change |
|------|--------|--------|
| 2026-01-27 | Claude | Created discovery during TASK-102 pre-work analysis |
| 2026-01-27 | Claude | Resolved with minimal test infrastructure approach |

---

## Metadata

```yaml
id: "EN-007:DISC-002"
parent_id: "EN-007"
work_type: DISCOVERY
title: "Test Infrastructure Dependency Gap"
status: RESOLVED
priority: HIGH
impact: HIGH
created_by: "Claude"
created_at: "2026-01-27T14:00:00Z"
updated_at: "2026-01-27T14:30:00Z"
completed_at: "2026-01-27T14:30:00Z"
tags: ["task-ordering", "test-infrastructure", "tdd-dependency", "process-gap"]
source: "TASK-102 Pre-work Analysis"
finding_type: DEPENDENCY_GAP
confidence_level: HIGH
validated: true
```

---

*Discovery ID: EN-007:DISC-002*
*Parent: EN-007 (ts-parser Agent Implementation)*
*Resolution: Minimal test infrastructure in skills/transcript/test_data/*
*Constitutional Compliance: P-002 (persisted), P-004 (provenance), P-011 (evidence-based)*
