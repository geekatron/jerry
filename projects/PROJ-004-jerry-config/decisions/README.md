# Architecture Decision Records - PROJ-004-jerry-config

> This directory contains Architecture Decision Records (ADRs) for the Jerry Configuration System project.

---

## ADR Index

| ID | Title | Status | Work Item | Date |
|----|-------|--------|-----------|------|
| [ADR-PROJ004-001](ADR-PROJ004-001-jerry-framework-aggregate.md) | JerryFramework Aggregate | ACCEPTED | WI-008d | 2026-01-12 |
| [ADR-PROJ004-002](ADR-PROJ004-002-jerry-project-aggregate.md) | JerryProject Aggregate | ACCEPTED | WI-008e | 2026-01-12 |
| [ADR-PROJ004-003](ADR-PROJ004-003-jerry-skill-aggregate.md) | JerrySkill Aggregate | ACCEPTED | WI-008f | 2026-01-12 |
| [ADR-PROJ004-004](ADR-PROJ004-004-jerry-session-context.md) | JerrySession Context | ACCEPTED | WI-008g | 2026-01-12 |

---

## Status Legend

| Status | Meaning |
|--------|---------|
| PROPOSED | Under consideration |
| ACCEPTED | Approved and implemented |
| SUPERSEDED | Replaced by another ADR |
| DEPRECATED | No longer applicable |

---

## ADR Format

Each ADR follows the L0/L1/L2 structure from the Jerry Design Canon:

- **L0: Executive Summary** - One-sentence decision
- **L1: Technical Design** - Detailed implementation with code
- **L2: Strategic Implications** - Rationale, invariants, trade-offs

### Required Sections

1. Context (with Research Inputs)
2. Decision (L0, L1, L2)
3. Consequences (Positive, Negative, Neutral)
4. Related (links to other ADRs/work items)

---

## Aggregate Relationship Diagram

```
JerryFramework (ADR-001)
├── JerryProject (ADR-002) - child aggregate
├── JerrySkill (ADR-003) - child aggregate
└── used by JerrySession (ADR-004) - runtime context
```

---

## Cross-Reference Matrix

| ADR | References |
|-----|------------|
| ADR-001 | ADR-002, ADR-003, ADR-004 |
| ADR-002 | ADR-001, ADR-004 |
| ADR-003 | ADR-001, ADR-004 |
| ADR-004 | ADR-001, ADR-002, ADR-003 |

---

## Reviewed

- **Date:** 2026-01-12
- **Reviewer:** Claude (WI-020)
- **Status:** All 4 ADRs verified complete and accurately reflect implementation
