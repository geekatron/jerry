# FEAT-002:DISC-001: Enabler Alignment Analysis - EN-005/EN-006 to FEAT-002 Restructuring

<!--
TEMPLATE: Discovery
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.9
CREATED: 2026-01-26
PURPOSE: Document alignment gaps between FEAT-001 design outputs and FEAT-002 enabler structure
-->

> **Type:** discovery
> **Status:** DOCUMENTED
> **Priority:** CRITICAL
> **Impact:** HIGH
> **Created:** 2026-01-26
> **Completed:** 2026-01-26
> **Parent:** FEAT-002
> **Owner:** Claude
> **Source:** FEAT-002 Inspection during EN-006 Phase 5 (Implementation Alignment)

---

## Frontmatter

```yaml
id: "FEAT-002:DISC-001"
work_type: DISCOVERY
title: "Enabler Alignment Analysis - EN-005/EN-006 to FEAT-002 Restructuring"
classification: TECHNICAL
status: DOCUMENTED
resolution: null
priority: CRITICAL
impact: HIGH
assignee: "Claude"
created_by: "Claude"
created_at: "2026-01-26T15:30:00Z"
updated_at: "2026-01-26T15:30:00Z"
completed_at: "2026-01-26T15:30:00Z"
parent_id: "FEAT-002"
tags:
  - "alignment"
  - "restructuring"
  - "en-005"
  - "en-006"
  - "task-id-conflict"
  - "implementation-planning"
finding_type: GAP
confidence_level: HIGH
source: "FEAT-002 Inspection during EN-006 Phase 5"
research_method: "Design artifact comparison and gap analysis"
validated: true
validation_date: "2026-01-26T15:30:00Z"
validated_by: "Claude (systematic inspection)"
```

---

## Summary

During inspection of FEAT-002 structure in preparation for implementation, significant alignment gaps were discovered between the design outputs from FEAT-001 (EN-005, EN-006) and the placeholder enablers in FEAT-002.

**Key Findings:**

| Finding | Severity | Impact |
|---------|----------|--------|
| Task ID Conflicts | CRITICAL | EN-006 and FEAT-002 enablers use overlapping TASK IDs |
| Architectural Misalignment | HIGH | EN-008 proposes 6 agents vs design's 1 ts-extractor |
| Missing Enablers | HIGH | No enablers for domain contexts, transcript validation |
| Python Code References | MEDIUM | EN-013 references Python, design specifies YAML-only |
| Missing Design References | MEDIUM | Enablers don't reference EN-005 TDDs |

**Recommendation:** Full restructuring of FEAT-002 enablers required before implementation.

---

## Context

### Background

FEAT-001 Analysis & Design produced two major enablers:
- **EN-005**: Design Documentation (TDDs, SKILL.md, agents, PLAYBOOK, RUNBOOK)
- **EN-006**: Context Injection Design (SPEC, domain contexts, FMEA, 8D reports)

FEAT-002 Implementation has 7 placeholder enablers (EN-007 through EN-013) that were created before EN-005 and EN-006 were completed. These placeholders need revision to align with the actual design outputs.

### Research Question

What alignment gaps exist between FEAT-001 design outputs and FEAT-002 enabler structure, and how should FEAT-002 be restructured to properly implement the design?

### Investigation Approach

1. Read FEAT-002 main file and all 7 enabler files
2. Read skills/transcript implementation artifacts (SKILL.md, agents)
3. Compare against EN-005 and EN-006 design deliverables
4. Document gaps and propose restructuring

---

## Finding 1: Task ID Conflicts (CRITICAL)

### Current State

| Location | Task IDs Used |
|----------|---------------|
| **EN-006 (FEAT-001)** | TASK-031 through TASK-042 |
| **EN-007 (FEAT-002)** | TASK-034 through TASK-038 |
| **EN-008 (FEAT-002)** | TASK-039 through TASK-045 |
| **EN-013 (FEAT-002)** | TASK-063 through TASK-066 |

### Conflicts Identified

```
EN-006 (Design)               EN-007/008 (Implementation)
================              =========================
TASK-034: TDD Creation        TASK-034: VTT Parser Prompt   <-- CONFLICT!
TASK-035: SPEC Creation       TASK-035: Speaker ID Logic    <-- CONFLICT!
TASK-036: Orchestration       TASK-036: Timestamp Normal.   <-- CONFLICT!
TASK-037: FMEA Analysis       TASK-037: Chunking Strategy   <-- CONFLICT!
TASK-038: Domain Contexts     TASK-038: Unit Tests          <-- CONFLICT!
TASK-039: Quality Review      TASK-039: Speaker Profiler    <-- CONFLICT!
TASK-040: Final Synthesis     TASK-040: Topic Extractor     <-- CONFLICT!
TASK-041: REM-001 8D          TASK-041: Question Detector   <-- CONFLICT!
TASK-042: REM-002 DISC        TASK-042: Action Extractor    <-- CONFLICT!
```

### Resolution Required

All FEAT-002 enabler tasks MUST be renumbered to avoid conflicts:
- **New range:** TASK-101 through TASK-199 reserved for FEAT-002
- **Rationale:** FEAT-001 can use TASK-001 to TASK-099, FEAT-002 uses TASK-101+

---

## Finding 2: Architectural Misalignment (HIGH)

### Designed Architecture (EN-005)

From `skills/transcript/SKILL.md`:

```
TRANSCRIPT SKILL PIPELINE
=========================

ts-parser (haiku) → ts-extractor (sonnet) → ts-formatter (sonnet) → ps-critic (sonnet)
     │                    │                        │                      │
     ▼                    ▼                        ▼                      ▼
Canonical JSON    Extraction Report        Packet Files          Quality Report
```

**4 agents total:** ts-parser, ts-extractor, ts-formatter, ps-critic (shared)

### FEAT-002 Enabler Structure (Current)

| Enabler | Purpose | Agents Proposed |
|---------|---------|-----------------|
| EN-007 | VTT Parser | 1 agent |
| EN-008 | Entity Extraction | **6 separate agents** (Speaker, Topic, Question, Action, Idea, Decision) |
| EN-009 | Mind Map Generator | 1 agent |
| EN-010 | Artifact Packaging | 1 agent |

### Gap Analysis

```
Designed (EN-005)              Current (FEAT-002)              Status
=================              ==================              ======
ts-parser agent                EN-007 VTT Parser               ✓ ALIGNED
ts-extractor agent (1)         EN-008: 6 separate agents       ✗ MISALIGNED
ts-formatter agent             EN-009 + EN-010 combined        ✗ SPLIT WRONG
```

**Critical Issue:** EN-008 proposes 6 parallel extraction agents, but the design specifies ONE ts-extractor with tiered extraction (Rule → ML → LLM) as described in TDD-ts-extractor.md.

### Resolution Required

1. **EN-008** must be revised to implement ts-extractor (single agent) per TDD-ts-extractor.md
2. **EN-009** (Mind Map) should be MERGED into EN-010 or REMOVED - ts-formatter handles all output per ADR-002
3. **EN-010** must be revised to implement ts-formatter per TDD-ts-formatter.md

---

## Finding 3: Missing Enablers (HIGH)

### Required by EN-006 DISC-001

EN-006 produced [DISC-001 FEAT-002 Implementation Scope](../FEAT-001-analysis-design/EN-006-context-injection-design/EN-006--DISC-001-feat002-implementation-scope.md) which identified required implementation tasks:

| Required Task | FEAT-002 Coverage | Status |
|---------------|-------------------|--------|
| contexts/software-engineering.yaml | None | **MISSING** |
| contexts/software-architecture.yaml | None | **MISSING** |
| contexts/product-management.yaml | None | **MISSING** |
| contexts/user-experience.yaml | None | **MISSING** |
| contexts/cloud-engineering.yaml | None | **MISSING** |
| contexts/security-engineering.yaml | None | **MISSING** |
| Test Transcript Provision | None | **MISSING** |
| Transcript Validation Workflow | None | **MISSING** |

### Resolution Required

New enablers must be created:
- **EN-014**: Domain Context Files (6 contexts/*.yaml files from EN-006 specs)
- **EN-015**: Transcript Validation (test transcripts and validation workflow)

---

## Finding 4: Implementation Language Misalignment (MEDIUM)

### EN-013 Current Content

EN-013 contains Python pseudocode:

```python
class ContextLoader:
    def load(self, context_injection_config: dict) -> InjectedContext:
        ...

class PromptMerger:
    def merge(self, base_prompt: str, override_template: str, variables: dict) -> str:
        ...
```

### Design Decision (EN-006 DEC-002)

From [DEC-002 Implementation Approach](../FEAT-001-analysis-design/EN-006-context-injection-design/EN-006--DEC-002-implementation-approach.md):

> **All FEAT-002 implementation tasks produce YAML configuration files only**
> (`contexts/*.yaml`, SKILL.md, AGENT.md). No Python or executable code is created.

### Resolution Required

EN-013 must be rewritten to align with YAML-only implementation per:
- [SPEC-context-injection.md Section 3](../FEAT-001-analysis-design/EN-006-context-injection-design/docs/specs/SPEC-context-injection.md#3-claude-code-skills-mapping)
- Claude Code Skills pattern: SKILL.md `context_injection` section configuration

---

## Finding 5: Missing Design References (MEDIUM)

### Current State

Enablers do not reference the EN-005 and EN-006 deliverables they should implement:

| Enabler | Should Reference | Currently References |
|---------|------------------|---------------------|
| EN-007 | TDD-ts-parser.md | None |
| EN-008 | TDD-ts-extractor.md | None |
| EN-009/10 | TDD-ts-formatter.md | None |
| EN-013 | SPEC-context-injection.md | EN-006 (generic) |

### Resolution Required

All enablers must be updated with explicit references to:
- Technical Design Documents (TDD-*.md)
- Architecture Decision Records (ADR-001 through ADR-005)
- Specification documents (SPEC-*.md)

---

## Restructuring Proposal

### Revised Enabler Structure

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                      FEAT-002 REVISED ENABLER STRUCTURE                      │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  GATE-5: Core Parsing & Extraction                                          │
│  ┌───────────────────────────────────────────────────────────────────────┐ │
│  │                                                                        │ │
│  │  EN-007: ts-parser Implementation                                     │ │
│  │  ├── Implements: TDD-ts-parser.md                                     │ │
│  │  ├── Output: agents/ts-parser.md (exists, verify alignment)           │ │
│  │  └── Tasks: TASK-101 through TASK-105                                 │ │
│  │                                                                        │ │
│  │  EN-008: ts-extractor Implementation (REVISED)                        │ │
│  │  ├── Implements: TDD-ts-extractor.md                                  │ │
│  │  ├── Output: agents/ts-extractor.md (exists, verify alignment)        │ │
│  │  ├── Pattern: PAT-001 Tiered Extraction, PAT-003 Speaker ID           │ │
│  │  └── Tasks: TASK-106 through TASK-112                                 │ │
│  │                                                                        │ │
│  └───────────────────────────────────────────────────────────────────────┘ │
│                                                                             │
│  GATE-6: Output & Integration                                               │
│  ┌───────────────────────────────────────────────────────────────────────┐ │
│  │                                                                        │ │
│  │  EN-009: ts-formatter Implementation (REVISED - was Mind Map)         │ │
│  │  ├── Implements: TDD-ts-formatter.md                                  │ │
│  │  ├── Absorbs: EN-010 Artifact Packaging                               │ │
│  │  ├── Output: agents/ts-formatter.md (exists, verify alignment)        │ │
│  │  └── Tasks: TASK-113 through TASK-118                                 │ │
│  │                                                                        │ │
│  │  EN-010: DEPRECATED - Merged into EN-009                              │ │
│  │                                                                        │ │
│  │  EN-011: Worktracker Integration                                      │ │
│  │  ├── Implements: Jerry worktracker skill integration                  │ │
│  │  ├── Output: 08-workitems/ packet section                             │ │
│  │  └── Tasks: TASK-119 through TASK-122                                 │ │
│  │                                                                        │ │
│  │  EN-013: Context Injection Implementation (REVISED)                   │ │
│  │  ├── Implements: SPEC-context-injection.md Section 3                  │ │
│  │  ├── Output: YAML configuration, NO Python code                       │ │
│  │  └── Tasks: TASK-123 through TASK-128                                 │ │
│  │                                                                        │ │
│  │  EN-014: Domain Context Files (NEW)                                   │ │
│  │  ├── Implements: EN-006 DISC-001 domain contexts                      │ │
│  │  ├── Output: contexts/*.yaml (6 files)                                │ │
│  │  └── Tasks: TASK-129 through TASK-135                                 │ │
│  │                                                                        │ │
│  │  EN-015: Transcript Validation (NEW)                                  │ │
│  │  ├── Implements: User-requested validation workflow                   │ │
│  │  ├── Input: Test transcripts (user provides)                          │ │
│  │  └── Tasks: TASK-136 through TASK-140                                 │ │
│  │                                                                        │ │
│  └───────────────────────────────────────────────────────────────────────┘ │
│                                                                             │
│  GATE-7: CLI (Above and Beyond - LAST)                                      │
│  ┌───────────────────────────────────────────────────────────────────────┐ │
│  │  EN-012: Skill CLI Interface (Unchanged)                              │ │
│  │  └── Tasks: TASK-141 through TASK-145                                 │ │
│  └───────────────────────────────────────────────────────────────────────┘ │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Task Renumbering Scheme

| Enabler | Old Task Range | New Task Range |
|---------|----------------|----------------|
| EN-007 | TASK-034-038 | TASK-101-105 |
| EN-008 | TASK-039-045 | TASK-106-112 |
| EN-009 (revised) | N/A | TASK-113-118 |
| EN-010 | N/A | DEPRECATED |
| EN-011 | N/A | TASK-119-122 |
| EN-012 | N/A | TASK-141-145 |
| EN-013 | TASK-063-066 | TASK-123-128 |
| EN-014 (new) | N/A | TASK-129-135 |
| EN-015 (new) | N/A | TASK-136-140 |

---

## Implementation Actions Required

### Phase 1: Structure Revision (EN-007 through EN-009)

1. **EN-007**: Update to reference TDD-ts-parser.md, renumber tasks to TASK-101+
2. **EN-008**: Major rewrite - single ts-extractor per design, renumber to TASK-106+
3. **EN-009**: Rename to "ts-formatter Implementation", absorb EN-010, reference TDD-ts-formatter.md
4. **EN-010**: Mark as DEPRECATED with redirect to EN-009

### Phase 2: Integration Enablers (EN-011, EN-013)

5. **EN-011**: Enhance with Jerry worktracker skill integration details
6. **EN-013**: Complete rewrite for YAML-only implementation per SPEC Section 3

### Phase 3: New Enablers (EN-014, EN-015)

7. **EN-014**: Create new enabler for domain context files
8. **EN-015**: Create new enabler for transcript validation workflow

### Phase 4: Orchestration

9. Create ORCHESTRATION_PLAN.md for FEAT-002
10. Create ORCHESTRATION.yaml with state tracking

---

## Evidence

### Source Documentation

| Evidence ID | Type | Description | Source |
|-------------|------|-------------|--------|
| E-001 | Design Doc | skills/transcript/SKILL.md | EN-005 deliverable |
| E-002 | Design Doc | skills/transcript/agents/ts-*.md | EN-005 deliverables |
| E-003 | Design Doc | TDD-ts-*.md (4 files) | EN-005 deliverables |
| E-004 | Specification | SPEC-context-injection.md | EN-006 deliverable |
| E-005 | Discovery | DISC-001 FEAT-002 Implementation Scope | EN-006 discovery |
| E-006 | Decision | DEC-002 Implementation Approach | EN-006 decision |

---

## Relationships

### Creates

| Work Item | Description |
|-----------|-------------|
| EN-014 | Domain Context Files (new enabler) |
| EN-015 | Transcript Validation (new enabler) |
| TASK-101 through TASK-145 | Renumbered implementation tasks |

### Informs

- [FEAT-002-implementation.md](./FEAT-002-implementation.md) - Requires restructuring
- All EN-007 through EN-013 enablers - Require revision

### Related Artifacts

| Type | Path | Description |
|------|------|-------------|
| Design | [TDD-transcript-skill.md](../FEAT-001-analysis-design/EN-005-design-documentation/docs/TDD-transcript-skill.md) | Main TDD |
| Design | [TDD-ts-parser.md](../FEAT-001-analysis-design/EN-005-design-documentation/docs/TDD-ts-parser.md) | Parser TDD |
| Design | [TDD-ts-extractor.md](../FEAT-001-analysis-design/EN-005-design-documentation/docs/TDD-ts-extractor.md) | Extractor TDD |
| Design | [TDD-ts-formatter.md](../FEAT-001-analysis-design/EN-005-design-documentation/docs/TDD-ts-formatter.md) | Formatter TDD |
| Spec | [SPEC-context-injection.md](../FEAT-001-analysis-design/EN-006-context-injection-design/docs/specs/SPEC-context-injection.md) | Context injection spec |
| Discovery | [DISC-001](../FEAT-001-analysis-design/EN-006-context-injection-design/EN-006--DISC-001-feat002-implementation-scope.md) | EN-006 implementation scope |

---

## Document History

| Date | Author | Change |
|------|--------|--------|
| 2026-01-26 | Claude | Created discovery during FEAT-002 inspection |
