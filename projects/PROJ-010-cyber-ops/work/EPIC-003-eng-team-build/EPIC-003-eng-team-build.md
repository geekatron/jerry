# EPIC-003: /eng-team Skill Build

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

Build the /eng-team skill with 8 agents (eng-architect, eng-lead, eng-backend, eng-frontend, eng-infra, eng-qa, eng-security, eng-reviewer). Includes SKILL.md, routing table, agent definitions, templates, playbook, and /adversary integration. Secure by design (R-001), architecturally pure (R-002), no slop (R-003).

**Key Objectives:**
- Define 8 agent definitions following agent-development-standards per R-022
- Create SKILL.md with routing table mapping user intents to agents
- Build templates for secure SDLC workflows (threat modeling, secure code review, security testing)
- Integrate /adversary for C2+ deliverable quality gates per R-024
- Embed threat modeling as a first-class concern in eng-architect per R-001

---

## Business Outcome Hypothesis

**We believe that** a purpose-built engineering team skill with security as a first-class constraint across all 8 agents

**Will result in** more secure software than bolt-on security review, with consistent quality enforcement through /adversary integration

**We will know we have succeeded when** all agents pass C4 /adversary review at >= 0.95, agents are portable across LLM providers per R-010, and purple team validation in Phase 5 confirms security-first design effectiveness

---

## Children Features/Capabilities

### Feature Inventory

| ID | Title | Status | Priority | Progress |
|----|-------|--------|----------|----------|
| FEAT-020 | SKILL.md & Routing | pending | critical | 0% |
| FEAT-021 | Architecture Agents (eng-architect, eng-lead) | pending | critical | 0% |
| FEAT-022 | Implementation Agents (eng-backend, eng-frontend, eng-infra) | pending | critical | 0% |
| FEAT-023 | Quality Agents (eng-qa, eng-security, eng-reviewer) | pending | critical | 0% |
| FEAT-024 | Templates & Playbook | pending | high | 0% |
| FEAT-025 | /adversary Integration | pending | high | 0% |

### Feature Links

- [FEAT-020: SKILL.md & Routing](./FEAT-020-eng-skill-routing/FEAT-020-eng-skill-routing.md)
- [FEAT-021: Architecture Agents](./FEAT-021-architecture-agents/FEAT-021-architecture-agents.md)
- [FEAT-022: Implementation Agents](./FEAT-022-implementation-agents/FEAT-022-implementation-agents.md)
- [FEAT-023: Quality Agents](./FEAT-023-quality-agents/FEAT-023-quality-agents.md)
- [FEAT-024: Templates & Playbook](./FEAT-024-templates-playbook/FEAT-024-templates-playbook.md)
- [FEAT-025: /adversary Integration](./FEAT-025-adversary-integration/FEAT-025-adversary-integration.md)

---

## Progress Summary

### Status Overview

```
+------------------------------------------------------------------+
|                     EPIC PROGRESS TRACKER                         |
+------------------------------------------------------------------+
| Features:  [....................] 0% (0/6 completed)              |
| Enablers:  [....................] 0% (0/25 completed)             |
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
| Depends On | EPIC-002 | Agent definitions and routing require architectural decisions from Phase 2 |
| Blocks | EPIC-005 | Purple team validation requires completed /eng-team skill |

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-02-22 | Claude | pending | Epic created with 6 features, 25 enablers |
