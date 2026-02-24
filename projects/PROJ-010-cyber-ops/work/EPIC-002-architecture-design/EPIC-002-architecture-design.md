# EPIC-002: Architecture & Design

> **Type:** epic
> **Status:** pending
> **Priority:** critical
> **Impact:** critical
> **Created:** 2026-02-22
> **Due:** ---
> **Completed:** ---
> **Parent:** —
> **Owner:** Adam Nowak
> **Target Quarter:** FY26-Q1

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Brief description and key objectives |
| [Business Outcome Hypothesis](#business-outcome-hypothesis) | Expected business outcomes |
| [Children Features/Capabilities](#children-featurescapabilities) | Feature inventory and tracking |
| [Progress Summary](#progress-summary) | Overall epic progress |
| [Related Items](#related-items) | Dependencies and related epics |
| [History](#history) | Status changes and key events |

---

## Summary

Design the architectural foundation for both skills. Produces 6 ADRs covering agent team architecture, skill routing, LLM portability, configurable rule sets, tool integration adapters, and authorization/scope control. Every ADR cites Phase 1 research evidence.

**Key Objectives:**
- Produce 6 ADRs with explicit evidence citations from EPIC-001 research artifacts
- Apply hexagonal/ports-and-adapters patterns per R-002
- Design provider abstraction layer for LLM portability per R-010
- Define pluggable adapter interfaces for tool integration per R-012
- Design override/merge rule set architecture per R-011
- Architect authorization verification system preventing unauthorized testing per R-020

---

## Business Outcome Hypothesis

**We believe that** evidence-grounded architecture decisions across agent teams, skill routing, portability, rule sets, tool adapters, and authorization

**Will result in** skills that are portable across LLM providers, testable in isolation, and extensible without framework modification

**We will know we have succeeded when** all 6 ADRs pass C4 /adversary review at >= 0.95, zero provider-specific coupling exists in the design, and the authorization architecture provably prevents unauthorized testing

---

## Children Features/Capabilities

### Feature Inventory

| ID | Title | Status | Priority | Progress |
|----|-------|--------|----------|----------|
| FEAT-010 | Agent Team Architecture | pending | critical | 0% |
| FEAT-011 | Skill Routing & Invocation Architecture | pending | critical | 0% |
| FEAT-012 | LLM Portability Architecture | pending | critical | 0% |
| FEAT-013 | Configurable Rule Set Architecture | pending | high | 0% |
| FEAT-014 | Tool Integration Adapter Architecture | pending | high | 0% |
| FEAT-015 | Authorization & Scope Control Architecture | pending | critical | 0% |

### Feature Links

- [FEAT-010: Agent Team Architecture](./FEAT-010-agent-team-architecture/FEAT-010-agent-team-architecture.md)
- [FEAT-011: Skill Routing & Invocation Architecture](./FEAT-011-skill-routing-architecture/FEAT-011-skill-routing-architecture.md)
- [FEAT-012: LLM Portability Architecture](./FEAT-012-llm-portability-architecture/FEAT-012-llm-portability-architecture.md)
- [FEAT-013: Configurable Rule Set Architecture](./FEAT-013-configurable-rule-set-architecture/FEAT-013-configurable-rule-set-architecture.md)
- [FEAT-014: Tool Integration Adapter Architecture](./FEAT-014-tool-integration-adapter-architecture/FEAT-014-tool-integration-adapter-architecture.md)
- [FEAT-015: Authorization & Scope Control Architecture](./FEAT-015-authorization-scope-control-architecture/FEAT-015-authorization-scope-control-architecture.md)

---

## Progress Summary

### Status Overview

```
+------------------------------------------------------------------+
|                     EPIC PROGRESS TRACKER                         |
+------------------------------------------------------------------+
| Features:  [....................] 0% (0/6 completed)              |
| Enablers:  [....................] 0% (0/26 completed)             |
+------------------------------------------------------------------+
| Overall:   [....................] 0%                               |
+------------------------------------------------------------------+
```

### Progress Metrics

| Metric | Value |
|--------|-------|
| **Total Features** | 6 |
| **Completed Features** | 0 |
| **In Progress Features** | 0 |
| **Pending Features** | 6 |
| **Feature Completion %** | 0% |

---

## Related Items

### Dependencies

| Dependency Type | Item | Description |
|----------------|------|-------------|
| Depends On | EPIC-001 | All ADRs cite Phase 1 research findings as evidence |
| Blocks | EPIC-003 | /eng-team build requires architectural decisions |
| Blocks | EPIC-004 | /red-team build requires architectural decisions |

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-02-22 | Claude | pending | Epic created with 6 features, 26 enablers |
