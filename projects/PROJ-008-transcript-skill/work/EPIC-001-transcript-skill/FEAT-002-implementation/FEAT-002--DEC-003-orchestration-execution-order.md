# FEAT-002:DEC-003: Orchestration Execution Order Correction

<!--
TEMPLATE: Decision
VERSION: 1.0.0
SOURCE: worktracker.md (Decision File), ADR/MADR best practices
CREATED: 2026-01-28 (EN-008 GATE-5 Review)
PURPOSE: Document orchestration execution order corrections and missing artifacts
EXTENDS: KnowledgeItem -> WorkItem (worktracker-specific, not in ONTOLOGY)
-->

> **Type:** decision
> **Status:** DOCUMENTED
> **Priority:** HIGH
> **Created:** 2026-01-28T08:30:00Z
> **Parent:** FEAT-002
> **Owner:** Claude
> **Related:** EN-008, EN-009, EN-013, EN-014, EN-015, EN-016, ORCHESTRATION.yaml

---

## Frontmatter

```yaml
# =============================================================================
# DECISION WORK ITEM
# Source: worktracker.md (Decision File), ADR/MADR best practices
# Purpose: Document decisions made during work with Q&A context
# =============================================================================

# Identity (inherited from WorkItem)
id: "FEAT-002:DEC-003"
work_type: DECISION
title: "Orchestration Execution Order Correction"

# State (see State Machine below)
status: DOCUMENTED

# Priority
priority: HIGH

# People
created_by: "Claude"
participants:
  - "Claude"
  - "User (Adam Nowak)"

# Timestamps (auto-managed)
created_at: "2026-01-28T08:30:00Z"
updated_at: "2026-01-28T08:30:00Z"
decided_at: "2026-01-28T08:30:00Z"

# Hierarchy
parent_id: "FEAT-002"

# Tags
tags: ["orchestration", "execution-order", "dependency-analysis", "gap-analysis"]

# =============================================================================
# DECISION-SPECIFIC PROPERTIES
# =============================================================================

# Supersession (for ADR pattern)
superseded_by: null
supersedes: null

# Decision Count
decision_count: 5
```

---

## Summary

This decision document captures critical findings during EN-008 GATE-5 review regarding orchestration execution order and missing artifacts. Analysis of ORCHESTRATION.yaml revealed a dependency conflict and missing task files that must be corrected before proceeding.

**Decisions Captured:** 5

**Key Outcomes:**
- EN-009 cannot be parallel with EN-016 due to dependency relationship
- TASK-046 through TASK-049 files were never created (gap identified)
- Corrected execution order for Group 2 enablers documented
- EN-008 minor findings tracked for EN-015 (TASK-138)
- EN-014 position in orchestration clarified (Group 3, after EN-013)

---

## Decision Context

### Background

During the GATE-5 review of EN-008 (Entity Extraction Core), the user requested clarification on enabler execution order. Upon analysis of ORCHESTRATION.yaml, a dependency conflict was discovered:

1. **ORCHESTRATION.yaml Group 2** lists EN-009, EN-013, EN-016 as **PARALLEL**
2. **However**, EN-009 has a dependency on EN-016 in its `dependencies:` field
3. **Furthermore**, EN-009's referenced task files (TASK-046 through TASK-049) do not exist

This violates the user's principle: *"We should execute enablers in parallel that are not dependant on one another. If there are dependencies then that means we should run sequentially."*

### Evidence (Citations from ORCHESTRATION.yaml)

```yaml
# From ORCHESTRATION.yaml - Group 2 Configuration
groups:
  group_2:
    phase: "parallel"
    enablers:
      - EN-009  # Mindmap Generator
      - EN-013  # Output Formatter
      - EN-016  # Parser-Extractor Contract

# From ORCHESTRATION.yaml - EN-009 Dependencies
enablers:
  EN-009:
    id: EN-009
    name: "Mindmap Generator"
    dependencies:
      - EN-016  # <-- CONFLICT: Cannot be parallel if depends on EN-016
    tasks:
      - TASK-046
      - TASK-047
      - TASK-048
      - TASK-049
```

### Constraints

- Enablers with dependencies MUST execute sequentially after their dependencies
- Task files MUST exist before enabler work can begin
- Orchestration state MUST be corrected to reflect accurate execution order
- Context MUST be persisted to prevent loss during session compaction

### Stakeholders

| Stakeholder | Role | Interest |
|-------------|------|----------|
| User (Adam Nowak) | Project Owner | Correct execution order, no lost context |
| Claude | Agent | Truthful, evidence-based orchestration |
| Future Agents | Executors | Accurate task files to work from |

---

## Decisions

### D-001: EN-009 Task Files Gap Identified

**Date:** 2026-01-28
**Participants:** Claude, User (Adam Nowak)

#### Question/Context

User observed: *"For EN-009, I don't see associated tasks for the enabler."*

Investigation via glob search confirmed:
```bash
# Search performed
Glob pattern: **/EN-009-mindmap-generator/TASK-*.md
Result: No files found
```

#### Options Considered

| Option | Description | Pros | Cons |
|--------|-------------|------|------|
| **A** | Create task files now before proceeding | Complete artifacts, ready for execution | Delays GATE-5 approval |
| **B** | Document gap and defer creation to EN-009 start | Minimal disruption to current flow | Gap persists until addressed |
| **C** | Assume enabler file is sufficient | Fastest path forward | Violates artifact completeness standards |

#### Decision

**We decided:** Document the gap (Option B) and ensure TASK-046 through TASK-049 are created when EN-009 becomes active. The enabler file (EN-009-mindmap-generator.md) contains task definitions that must be converted to individual task files.

#### Rationale

1. Creating task files now would interrupt the current GATE-5 approval flow
2. EN-009 cannot start until EN-016 completes (see D-002), so time exists
3. Documenting the gap ensures it won't be forgotten
4. Task definitions exist in EN-009 enabler file - just need file creation

#### Implications

- **Positive:** Gap identified and documented before it causes execution failure
- **Negative:** Additional work required before EN-009 can start
- **Follow-up required:** Create TASK-046, TASK-047, TASK-048, TASK-049 before EN-009 activation

**Task Definitions (from EN-009-mindmap-generator.md):**

| ID | Title | Status | Owner | Effort | Blocked By |
|----|-------|--------|-------|--------|------------|
| TASK-046 | Create Mermaid Generator Agent | pending | Claude | 3 | EN-008 |
| TASK-047 | Create ASCII Generator Agent | pending | Claude | 2 | EN-008 |
| TASK-048 | Implement Deep Link Embedding | pending | Claude | 2 | TASK-046 |
| TASK-049 | Create Unit Tests | pending | Claude | 1 | TASK-046..048 |

---

### D-002: Orchestration Dependency Conflict Correction

**Date:** 2026-01-28
**Participants:** Claude, User (Adam Nowak)

#### Question/Context

User asked: *"We should execute enablers in parallel that are not dependant on one another. If there are dependencies then that means we should run sequentially."*

Analysis revealed ORCHESTRATION.yaml Group 2 contains a conflict:
- EN-009, EN-013, EN-016 listed as **PARALLEL**
- EN-009.dependencies includes EN-016
- This is logically inconsistent

#### Options Considered

| Option | Description | Pros | Cons |
|--------|-------------|------|------|
| **A** | Keep EN-009 in Group 2, remove EN-016 dependency | Preserves current grouping | May not reflect true dependency |
| **B** | Move EN-009 to Group 3 (sequential after Group 2) | Correct execution order | Delays EN-009 start |
| **C** | Split Group 2 into subgroups | Fine-grained control | Adds complexity |

#### Decision

**We decided:** Option B - EN-009 must execute AFTER EN-016 completes, not in parallel with it. Group 2 should contain only EN-013 and EN-016 as parallel. EN-009 should be in a subsequent sequential phase after EN-016.

#### Rationale

1. Dependencies define execution order - this is non-negotiable
2. EN-016 (Parser-Extractor Contract) must complete before EN-009 (Mindmap Generator) can use its outputs
3. EN-013 (Output Formatter) has no dependency on EN-016, so it CAN be parallel with EN-016
4. The user's principle is clear: "dependencies = sequential"

#### Implications

- **Positive:** Correct execution order ensures EN-009 has required inputs
- **Negative:** EN-009 starts later than originally planned
- **Follow-up required:** Update ORCHESTRATION.yaml to reflect corrected grouping

---

### D-003: Corrected Execution Order for Group 2

**Date:** 2026-01-28
**Participants:** Claude, User (Adam Nowak)

#### Question/Context

What is the correct execution order for the enablers currently in Group 2?

#### Analysis

**Current Group 2 (INCORRECT):**
```
EN-009 ─┐
EN-013 ─┼─ PARALLEL (Group 2)
EN-016 ─┘
```

**Dependency Analysis:**
- EN-013 depends on EN-006 (COMPLETE from FEAT-001) ✓
- EN-016 depends on EN-008 (COMPLETE - just passed GATE-5) ✓
- EN-009 depends on EN-016 (NOT COMPLETE - must wait)

**Corrected Execution Order:**
```
                    ┌──────────┐
                    │  EN-008  │ ← COMPLETE (GATE-5)
                    └────┬─────┘
                         │
         ┌───────────────┼───────────────┐
         │               │               │
         v               v               │
    ┌────────┐      ┌────────┐           │
    │ EN-013 │      │ EN-016 │           │
    └────┬───┘      └────┬───┘           │
         │               │               │
         │     PARALLEL  │               │
         │               │               │
         │               v               │
         │          ┌────────┐           │
         │          │ EN-009 │ ← Sequential AFTER EN-016
         │          └────────┘           │
         │                               │
         └───────────────────────────────┘
```

#### Decision

**We decided:**
- **Group 2A (PARALLEL):** EN-013 + EN-016 (no mutual dependency)
- **Group 2B (SEQUENTIAL):** EN-009 (after EN-016 completes)

#### Rationale

This structure:
1. Honors all declared dependencies
2. Maximizes parallelism where safe (EN-013 || EN-016)
3. Ensures EN-009 has EN-016's outputs before starting

---

### D-004: EN-014 Position in Orchestration

**Date:** 2026-01-28
**Participants:** Claude, User (Adam Nowak)

#### Question/Context

User asked: *"Where does EN-14 fit in this orchestration plan? Will EN-14 be happening after EN-016, EN-009 and EN-013?"*

#### Analysis

From ORCHESTRATION.yaml:
```yaml
EN-014:
  id: EN-014
  name: "Integration Testing"
  dependencies:
    - EN-013  # Depends on Output Formatter
```

EN-014 is currently in Group 3 with EN-011 and EN-015.

**Dependency Chain:**
```
EN-013 (Group 2A) → EN-014 (Group 3)
```

EN-014 does NOT depend on EN-009 or EN-016 directly.

#### Decision

**We decided:** EN-014 can start as soon as EN-013 completes. It does not need to wait for EN-009 or EN-016.

**Execution Timeline:**
1. Group 2A: EN-013 || EN-016 (parallel)
2. After EN-013: EN-014 can start
3. After EN-016: EN-009 can start
4. EN-011 and EN-015 have their own dependency chains

#### Rationale

1. EN-014 only depends on EN-013 (Output Formatter)
2. Once EN-013 completes, EN-014's dependency is satisfied
3. EN-014 does not require EN-009's mindmap generation outputs

#### Implications

- **Positive:** EN-014 can start earlier than if it waited for all of Group 2
- **Negative:** None identified
- **Follow-up required:** Verify EN-014 task definitions are ready

---

### D-005: EN-008 Minor Findings Tracking

**Date:** 2026-01-28
**Participants:** Claude, User (Adam Nowak)

#### Question/Context

User stated: *"We need to ensure that the minor findings are moved to the correct future enabler - we don't want to loose them."*

#### Minor Findings from EN-008 GATE-5 Review

| Finding ID | Description | Severity | Category |
|------------|-------------|----------|----------|
| F-001 / QA-CM-001 | Version mismatch: ts-extractor.md shows 1.2.0, agent def shows 1.1.0 | Minor | Configuration |
| F-004 | Plain text format not in INT-006 cross-format integration test | Minor | Testing |
| F-005 | No negative test cases (malformed input, missing timestamps) | Minor | Testing |
| QA-TD-001 | Performance target "~500 tokens/batch" not in agent definition | Minor | Documentation |
| QA-TD-002 | Token budget "1200 tokens" not in agent definition | Minor | Documentation |

#### Options Considered

| Option | Description | Pros | Cons |
|--------|-------------|------|------|
| **A** | Create tasks in EN-015 (Transcript Validation) | Logical home for test enhancements | May not cover doc updates |
| **B** | Create tasks in EN-014 (Integration Testing) | Test-focused enabler | F-001 is config, not test |
| **C** | Distribute across multiple enablers | Each finding goes to best fit | Complex tracking |

#### Decision

**We decided:** Option A - Create TASK-138 in EN-015 to capture all EN-008 minor findings as deferred test enhancements and documentation updates.

#### Rationale

1. EN-015 (Transcript Validation) focuses on validation and testing - natural home for F-004, F-005
2. QA-TD-001 and QA-TD-002 are documentation items that can be bundled
3. F-001 (version mismatch) is a quick fix that can be done immediately
4. Single task simplifies tracking of related deferred items

#### Implications

- **Positive:** Minor findings won't be lost; clear ownership established
- **Negative:** F-001 could be fixed now rather than deferred
- **Follow-up required:**
  - Fix F-001 immediately (ts-extractor.md version)
  - Create TASK-138 in EN-015 for remaining items

---

## Decision Summary

| ID | Decision | Date | Status |
|----|----------|------|--------|
| D-001 | EN-009 task files (TASK-046-049) missing - create when enabler activates | 2026-01-28 | Accepted |
| D-002 | EN-009 cannot be parallel with EN-016 - must be sequential | 2026-01-28 | Accepted |
| D-003 | Group 2 split: EN-013+EN-016 parallel, EN-009 sequential after | 2026-01-28 | Accepted |
| D-004 | EN-014 can start after EN-013 (doesn't need EN-009/EN-016) | 2026-01-28 | Accepted |
| D-005 | EN-008 minor findings go to TASK-138 in EN-015 | 2026-01-28 | Accepted |

---

## Action Items

| ID | Action | Owner | Due | Status |
|----|--------|-------|-----|--------|
| AI-001 | Fix F-001 (ts-extractor.md version mismatch) | Claude | Now | Pending |
| AI-002 | Create TASK-138 in EN-015 for deferred minor findings | Claude | Now | Pending |
| AI-003 | Update ORCHESTRATION.yaml with corrected groups | Claude | Before Group 2 start | Pending |
| AI-004 | Create TASK-046, 047, 048, 049 files for EN-009 | Claude | Before EN-009 start | Pending |

---

## Related Artifacts

| Type | Path | Description |
|------|------|-------------|
| Parent | [FEAT-002](./FEAT-002-implementation.md) | Parent feature |
| Orchestration | [ORCHESTRATION.yaml](./ORCHESTRATION.yaml) | Execution state SSOT |
| Enabler | [EN-008](./EN-008-entity-extraction/EN-008-entity-extraction.md) | Source of minor findings |
| Enabler | [EN-009](./EN-009-mindmap-generator/EN-009-mindmap-generator.md) | Missing task files |
| Enabler | [EN-015](./EN-015-transcript-validation/EN-015-transcript-validation.md) | Target for TASK-138 |
| Discovery | [DISC-003](./FEAT-002--DISC-003-quality-artifact-folder-structure.md) | Related quality issues |
| Discovery | [DISC-004](./FEAT-002--DISC-004-agent-instruction-compliance-failure.md) | Related compliance issues |

---

## Document History

| Date | Author | Change |
|------|--------|--------|
| 2026-01-28 | Claude | Created decision document capturing orchestration corrections |

---

## Metadata

```yaml
id: "FEAT-002:DEC-003"
parent_id: "FEAT-002"
work_type: DECISION
title: "Orchestration Execution Order Correction"
status: DOCUMENTED
priority: HIGH
created_by: "Claude"
created_at: "2026-01-28T08:30:00Z"
updated_at: "2026-01-28T08:30:00Z"
decided_at: "2026-01-28T08:30:00Z"
participants: ["Claude", "User (Adam Nowak)"]
tags: ["orchestration", "execution-order", "dependency-analysis", "gap-analysis"]
decision_count: 5
superseded_by: null
supersedes: null
```
