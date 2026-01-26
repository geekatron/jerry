# EN-004: Architecture Decision Records

<!--
TEMPLATE: Enabler
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.5
-->

> **Type:** enabler
> **Status:** pending
> **Priority:** high
> **Impact:** high
> **Created:** 2026-01-26T00:00:00Z
> **Due:** TBD
> **Completed:**
> **Parent:** FEAT-001
> **Owner:** Claude
> **Target Sprint:** Sprint 1
> **Effort Points:** 8
> **Gate:** GATE-3 (Architecture Review)

---

## Summary

Create formal Architecture Decision Records (ADRs) documenting key technical decisions for the Transcript Skill. Each ADR captures the context, decision, and consequences to provide traceability and enable future maintainers to understand why decisions were made.

**Technical Justification:**
- ADRs provide decision traceability
- Future maintainers understand "why" not just "what"
- Prevents re-litigating past decisions
- Documents trade-offs considered

---

## Benefit Hypothesis

**We believe that** documenting architecture decisions as formal ADRs

**Will result in** clear implementation guidance and long-term maintainability

**We will know we have succeeded when:**
- All major technical decisions have ADRs
- Each ADR has context, decision, and consequences
- ADRs reference supporting research
- Human approval received at GATE-3

---

## Acceptance Criteria

### Definition of Done

- [ ] ADR-001: Agent Architecture created
- [ ] ADR-002: Artifact Structure & Token Management created
- [ ] ADR-003: Bidirectional Deep Linking created
- [ ] ADR-004: File Splitting Strategy created
- [ ] ADR-005: Prompt-based vs Python-based Agents created
- [ ] All ADRs follow standard template
- [ ] ps-critic review passed
- [ ] Human approval at GATE-3

### Technical Criteria

| # | Criterion | Verified |
|---|-----------|----------|
| AC-1 | Each ADR has Context section with problem statement | [ ] |
| AC-2 | Each ADR has Decision section with clear choice | [ ] |
| AC-3 | Each ADR has Consequences section (pros/cons) | [ ] |
| AC-4 | Each ADR references supporting research | [ ] |
| AC-5 | ADRs are numbered and dated | [ ] |
| AC-6 | Alternative options documented | [ ] |

---

## Children (Tasks)

### Task Inventory

| ID | Title | Status | Owner | Effort | Blocked By |
|----|-------|--------|-------|--------|------------|
| TASK-016 | Create ADR-001: Agent Architecture | pending | ps-architect | 2 | EN-003 |
| TASK-017 | Create ADR-002: Artifact Structure | pending | ps-architect | 2 | EN-003 |
| TASK-018 | Create ADR-003: Bidirectional Linking | pending | ps-architect | 1 | EN-003 |
| TASK-019 | Create ADR-004: File Splitting Strategy | pending | ps-architect | 1 | EN-003 |
| TASK-020 | Create ADR-005: Agent Implementation Approach | pending | ps-architect | 1 | EN-003 |
| TASK-021 | ps-critic ADR Review | pending | ps-critic | 1 | TASK-016..020 |

---

## ADR Template

Each ADR will follow this structure:

```markdown
# ADR-{NNN}: {Title}

> **Status:** PROPOSED | ACCEPTED | DEPRECATED | SUPERSEDED
> **Date:** YYYY-MM-DD
> **Deciders:** {Who made this decision}
> **Technical Area:** {agents | artifacts | linking | parsing | etc.}

## Context

{What is the issue that we're seeing that is motivating this decision?}

## Decision

{What is the decision that was made?}

## Consequences

### Positive
- {Pro 1}
- {Pro 2}

### Negative
- {Con 1}
- {Con 2}

### Neutral
- {Observation 1}

## Alternatives Considered

### Alternative 1: {Name}
- Description: {What was this alternative?}
- Pros: {Benefits}
- Cons: {Drawbacks}
- Why rejected: {Reason}

## References

- {Link to research document}
- {Link to requirements}
- {External reference with citation}
```

---

## Planned ADRs

### ADR-001: Agent Architecture

**Scope:** Define the architecture for transcript processing agents
- Custom agents vs existing Jerry agents
- Agent responsibilities and boundaries
- Inter-agent communication

### ADR-002: Artifact Structure & Token Management

**Scope:** Define output artifact structure
- Directory layout for transcript packets
- Token budget per artifact (35K limit)
- Naming conventions

### ADR-003: Bidirectional Deep Linking

**Scope:** Define linking strategy between artifacts
- Link format specification
- Backlinks section structure
- Anchor generation rules

### ADR-004: File Splitting Strategy

**Scope:** Define how large artifacts are split
- Split trigger criteria
- Naming for split files
- Cross-reference handling

### ADR-005: Agent Implementation Approach

**Scope:** Define phased implementation strategy
- Phase 1: Prompt-based (YAML/MD)
- Phase 2: Python-based (if needed)
- Migration path between phases

---

## Related Items

### Hierarchy

- **Parent Feature:** [FEAT-001: Analysis & Design](../FEAT-001-analysis-design.md)

### Dependencies

| Dependency Type | Item | Description |
|----------------|------|-------------|
| Depends On | EN-003 | Requirements inform architecture |
| Blocks | EN-005 | Design needs architecture decisions |
| Blocks | FEAT-002 | Implementation needs ADRs |

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-01-26 | Claude | pending | Enabler created |

---

## System Mapping

| System | Mapping |
|--------|---------|
| **Azure DevOps** | Product Backlog Item (tagged Architecture) |
| **SAFe** | Enabler Story |
| **JIRA** | Task |
