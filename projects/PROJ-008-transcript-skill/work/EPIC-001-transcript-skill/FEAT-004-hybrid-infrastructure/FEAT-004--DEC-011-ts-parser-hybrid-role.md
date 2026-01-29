# FEAT-004:DEC-011: ts-parser.md Hybrid Architecture Role

<!--
TEMPLATE: Decision
VERSION: 1.0.0
SOURCE: worktracker.md (Decision File), ADR/MADR best practices
CREATED: 2026-01-29 (FEAT-004 TDD Planning)
PURPOSE: Document ts-parser.md role in hybrid architecture
-->

> **Type:** decision
> **Status:** ACCEPTED
> **Priority:** HIGH
> **Created:** 2026-01-29T20:00:00Z
> **Parent:** FEAT-004
> **Owner:** User
> **Related:** DISC-009, DISC-011, ADR-001-amendment-001

---

## Frontmatter

```yaml
id: "FEAT-004:DEC-011"
work_type: DECISION
title: "ts-parser.md Hybrid Architecture Role"

status: ACCEPTED
priority: HIGH

created_by: "Claude"
participants:
  - "User"
  - "Claude"

created_at: "2026-01-29T20:00:00Z"
updated_at: "2026-01-29T20:00:00Z"
decided_at: "2026-01-29T20:00:00Z"

parent_id: "FEAT-004"

tags:
  - "architecture"
  - "ts-parser"
  - "hybrid"
  - "strategy-pattern"

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

This decision document captures the user's architectural decisions about how ts-parser.md should function within the hybrid architecture established by DISC-009 and ADR-001-amendment-001.

**Decisions Captured:** 3

**Key Outcomes:**
- ts-parser.md becomes an **orchestrator** using Strategy Pattern, not removed
- Python handles deterministic formats (VTT first, then SRT, etc.) incrementally
- LLM fallback preserved for unsupported formats
- Backward compatibility maintained throughout transition

---

## Decision Context

### Background

During TDD-FEAT-004 planning, Claude initially misunderstood the hybrid architecture scope, proposing to **remove** ts-parser.md entirely and replace it with Python scripts. The user corrected this misunderstanding, clarifying that:

1. The hybrid architecture means Python handles what it's good at (deterministic parsing)
2. LLM agents handle what they're good at (semantic work, complex patterns)
3. ts-parser.md should **evolve**, not be eliminated

### Constraints

- **Backward Compatibility**: Existing formats (VTT, SRT, plain text) must continue working
- **Incremental Adoption**: Cannot switch all formats to Python at once
- **Quality Assurance**: Python output needs validation
- **Single Entry Point**: Downstream agents (ts-extractor) should not need to know about the internal routing

### Stakeholders

| Stakeholder | Role | Interest |
|-------------|------|----------|
| User | Product Owner | Backward compatibility, quality |
| Claude | Implementer | Clear architectural guidance |
| Future Developers | Maintainers | Understandable, extensible design |

---

## Decisions

### D-001: ts-parser.md Role in Hybrid Architecture

**Date:** 2026-01-29
**Participants:** User, Claude

#### Question/Context

Claude proposed removing ts-parser.md entirely and replacing it with Python scripts. User asked:

> "No claude, no-where did it say we get rid of the ts-parser.md agent.... I thought we were using a hybrid solution? Are you proposing we use the VTT parser for everything? How does that work for other formats that we currently support?"

#### Options Considered

| Option | Description | Pros | Cons |
|--------|-------------|------|------|
| **A** | Remove ts-parser.md, Python handles all | Simpler architecture | Breaks unsupported formats, no fallback |
| **B** | Python handles VTT only, ts-parser handles rest | Safe, minimal change | Inconsistent routing logic |
| **C** | ts-parser.md becomes orchestrator | Clean separation, extensible | More complex, requires redesign |
| **D (Chosen)** | ts-parser.md as orchestrator/delegator/fallback/validator | All benefits of C + validation | Most work, but highest quality |

#### Decision

**We decided:** ts-parser.md becomes an **orchestrator** that:
1. **Delegates** to Python for deterministic formats (VTT first, then incrementally add SRT, etc.)
2. **Falls back** to LLM-based parsing for formats without Python support
3. **Validates** Python output for quality assurance

This follows the **Strategy Pattern** where:
- Python scripts are the "preferred strategy" for supported formats
- LLM parsing is the "fallback strategy" for unsupported formats
- ts-parser.md selects the appropriate strategy based on format detection

#### Rationale

1. **Backward Compatible**: Formats without Python support continue to work via LLM fallback
2. **Incremental Adoption**: Add Python handlers one format at a time without breaking changes
3. **Quality Assured**: Validation layer catches Python parsing issues
4. **Single Entry Point**: ts-parser.md remains the interface for downstream agents
5. **Extensible**: New formats can be added by implementing new Python handlers

#### Implications

- **Positive:** Clean architecture, backward compatible, extensible
- **Negative:** More complex than simple replacement, requires ts-parser.md redesign
- **Follow-up required:** TDD-FEAT-004 must specify the orchestration logic, interface contracts, and validation rules

---

### D-002: Format Support Scope for Python

**Date:** 2026-01-29
**Participants:** User, Claude

#### Question/Context

Claude asked: "For the hybrid architecture, which formats should Python handle?"

| Option | Description |
|--------|-------------|
| A | Python handles VTT only |
| B | Python handles VTT and SRT |
| C | Python handles ALL formats |
| D | Python handles formats incrementally as scripts are developed |

#### Decision

**We decided:** Option D - Python handles formats incrementally as deterministic scripts are developed. VTT is first priority (webvtt-py library exists). SRT and plain text will be added as Python handlers are implemented.

#### Rationale

1. **Risk Mitigation**: Don't try to Python-ify all formats at once
2. **Evidence-Based**: webvtt-py is proven (MIT license, active maintenance)
3. **Prioritized**: VTT is the format that caused the 99.8% data loss in DISC-009
4. **Fallback Safety**: Formats without Python support still work via LLM

---

### D-003: Testing Strategy for TDD-FEAT-004

**Date:** 2026-01-29
**Participants:** User, Claude

#### Question/Context

Claude asked: "For RED/GREEN/REFACTOR TDD - should this cover unit tests, contract tests, integration tests, or all of the above?"

#### Decision

**We decided:** All of the above - but the TDD should provide **concrete instructions** for work item creation, not the actual test code. The TDD should enable the next agent to build out required entities in the work tracker.

#### Rationale

1. **Actionable**: TDD creates work items, work items drive implementation
2. **Separation of Concerns**: TDD specifies WHAT, implementation tasks do HOW
3. **Traceability**: Clear link from TDD requirements to work items to code

---

## Decision Summary

| ID | Decision | Date | Status |
|----|----------|------|--------|
| D-001 | ts-parser.md as orchestrator/delegator/fallback/validator (Strategy Pattern) | 2026-01-29 | ACCEPTED |
| D-002 | Python format support added incrementally (VTT first) | 2026-01-29 | ACCEPTED |
| D-003 | TDD provides instructions for work items, not test code | 2026-01-29 | ACCEPTED |

---

## Related Artifacts

| Type | Path | Description |
|------|------|-------------|
| Parent | [FEAT-004-hybrid-infrastructure.md](./FEAT-004-hybrid-infrastructure.md) | Parent feature |
| Discovery | [FEAT-002--DISC-009](../FEAT-002-implementation/FEAT-002--DISC-009-agent-only-architecture-limitation.md) | Original architecture limitation |
| Discovery | [FEAT-002--DISC-011](../FEAT-002-implementation/FEAT-002--DISC-011-disc009-operational-findings-gap.md) | Operational findings gap |
| ADR | [ADR-001-amendment-001](../../../../docs/adrs/ADR-001-amendment-001-python-preprocessing.md) | Python preprocessing layer |
| Enabler | [EN-020-python-parser](./EN-020-python-parser/EN-020-python-parser.md) | Python parser implementation |
| Enabler | [EN-021-chunking-strategy](./EN-021-chunking-strategy/EN-021-chunking-strategy.md) | Chunking strategy |
| Enabler | [EN-022-extractor-adaptation](./EN-022-extractor-adaptation/EN-022-extractor-adaptation.md) | Extractor adaptation |

---

## Document History

| Date | Author | Change |
|------|--------|--------|
| 2026-01-29T20:00:00Z | Claude | Created decision document from user feedback |

---

## Metadata

```yaml
id: "FEAT-004:DEC-011"
parent_id: "FEAT-004"
work_type: DECISION
title: "ts-parser.md Hybrid Architecture Role"
status: ACCEPTED
priority: HIGH
created_by: "Claude"
created_at: "2026-01-29T20:00:00Z"
updated_at: "2026-01-29T20:00:00Z"
decided_at: "2026-01-29T20:00:00Z"
participants: ["User", "Claude"]
tags: ["architecture", "ts-parser", "hybrid", "strategy-pattern"]
decision_count: 3
superseded_by: null
supersedes: null
```
