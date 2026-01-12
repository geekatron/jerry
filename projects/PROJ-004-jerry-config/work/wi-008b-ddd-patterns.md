# WI-008b: Research DDD Hierarchical Patterns

| Field | Value |
|-------|-------|
| **ID** | WI-008b |
| **Title** | Research DDD patterns for hierarchical configuration |
| **Type** | Research |
| **Status** | PENDING |
| **Priority** | HIGH |
| **Phase** | PHASE-02 |
| **Parent** | WI-008 |
| **Agent** | ps-researcher |
| **Assignee** | WT-Main |
| **Created** | 2026-01-12 |
| **Completed** | - |

---

## Description

Research Domain-Driven Design patterns applicable to hierarchical configuration systems:
- Aggregate relationships (parent-child aggregates)
- Bounded context patterns for multi-level systems
- Configuration as value objects vs entities
- Context/session patterns in DDD

This research provides theoretical foundation for the domain model design.

---

## Agent Invocation

### ps-researcher Prompt

```
You are the ps-researcher agent (v2.0.0).

## PS CONTEXT (REQUIRED)
- **PS ID:** PROJ-004
- **Entry ID:** e-006
- **Topic:** DDD Hierarchical Configuration Patterns

## MANDATORY PERSISTENCE (P-002)
Create file at: projects/PROJ-004-jerry-config/research/PROJ-004-e-006-ddd-hierarchical-patterns.md

## RESEARCH TASK

Research DDD patterns for hierarchical configuration systems:

### 1. Aggregate Relationships
- How do parent-child aggregates communicate?
- Should child aggregates reference parent or use IDs?
- What are patterns for aggregate hierarchies?
- When is a child a separate aggregate vs part of parent?

### 2. Configuration in DDD
- Should configuration be an aggregate or value object?
- How to model layered/cascading configuration?
- Patterns for environment-specific overrides
- Configuration as a domain concern vs infrastructure

### 3. Context/Session Patterns
- How to model runtime context in DDD?
- Patterns for request-scoped vs application-scoped context
- Unit of Work patterns for session state
- How do frameworks like ASP.NET Core handle this?

### 4. Bounded Context Patterns
- How to structure multi-level bounded contexts?
- Shared Kernel patterns for common entities
- Context mapping for framework → project → skill
- Anti-corruption layers between contexts

### 5. Industry Examples
- How does Django/Rails handle multi-tenant config?
- How does Terraform model workspaces?
- How does Git model repo → worktree → index?

## SOURCES TO CONSULT
- "Domain-Driven Design" by Eric Evans
- "Implementing Domain-Driven Design" by Vaughn Vernon
- Martin Fowler's DDD articles
- Microsoft's DDD guidance for .NET
- Python DDD examples (eventsourcing library)

## OUTPUT FORMAT
Use L0/L1/L2 explanation levels with diagrams and code patterns.
Include trade-off analysis for each pattern.
```

---

## Acceptance Criteria

- [ ] AC-008b.1: Aggregate relationship patterns documented
- [ ] AC-008b.2: Configuration modeling patterns identified
- [ ] AC-008b.3: Context/session patterns researched
- [ ] AC-008b.4: Bounded context patterns analyzed
- [ ] AC-008b.5: Industry examples studied
- [ ] AC-008b.6: Research artifact created at specified path

---

## Evidence

| Criterion | Evidence | Source |
|-----------|----------|--------|
| AC-008b.1 | - | - |
| AC-008b.2 | - | - |
| AC-008b.3 | - | - |
| AC-008b.4 | - | - |
| AC-008b.5 | - | - |
| AC-008b.6 | - | - |

---

## Key Questions

| Question | Importance |
|----------|------------|
| Should JerryProject hold reference to JerryFramework or just ID? | HIGH - Affects navigation |
| Is configuration an aggregate or value object? | HIGH - Affects persistence |
| How to model "active project" context? | CRITICAL - Core use case |
| Should skills be independent or project-scoped? | MEDIUM - Affects skill invocation |

---

## Progress Log

| Timestamp | Update | Actor |
|-----------|--------|-------|
| 2026-01-12T12:00:00Z | Work item created | Claude |

---

## Dependencies

| Type | Work Item | Relationship |
|------|-----------|--------------|
| Part Of | WI-008 | Parent work item |
| Parallel With | WI-008a, WI-008c | Can run simultaneously |
| Blocks | WI-008d, WI-008e, WI-008f, WI-008g | Design needs research |

---

## Related Artifacts

- **Output**: `research/PROJ-004-e-006-ddd-hierarchical-patterns.md`
- **References**: Eric Evans DDD, Vaughn Vernon IDDD
