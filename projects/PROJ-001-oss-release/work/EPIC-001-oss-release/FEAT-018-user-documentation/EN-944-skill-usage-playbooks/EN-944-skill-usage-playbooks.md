# EN-944: Create Skill Usage Playbooks

> **Type:** enabler
> **Status:** done
> **Priority:** medium
> **Impact:** high
> **Enabler Type:** compliance
> **Created:** 2026-02-17
> **Due:** ---
> **Completed:** 2026-02-18
> **Parent:** FEAT-018
> **Owner:** ---
> **Effort:** 5

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Brief description and technical scope |
| [Problem Statement](#problem-statement) | Why this enabler is needed |
| [Business Value](#business-value) | How enabler supports feature delivery |
| [Technical Approach](#technical-approach) | High-level technical approach |
| [Acceptance Criteria](#acceptance-criteria) | Definition of done |
| [History](#history) | Status changes and key events |

---

## Summary

Create skill usage playbooks for the major Jerry skills: problem-solving, orchestration, and transcript processing. Each playbook provides strategic guidance with decision trees, examples, and best practices for effective skill use.

**Technical Scope:**
- Problem-solving playbook (when to use, agent selection, workflow patterns)
- Orchestration playbook (pipeline design, barrier patterns, state management)
- Transcript playbook (format selection, domain tuning, quality optimization)
- Common patterns and anti-patterns across skills

---

## Problem Statement

SKILL.md files are comprehensive technical references but poor user guides. Users need strategic playbooks that explain when and how to use each skill effectively, with decision trees for common scenarios.

---

## Business Value

Playbooks unlock the full value of Jerry's skill system by guiding users beyond basic invocation to effective, strategic use of each skill.

### Features Unlocked

- Effective skill utilization (not just basic invocation)
- Reduced skill misuse and wasted iterations
- Self-service advanced feature discovery

---

## Technical Approach

1. Create `docs/user-guides/playbooks/` directory
2. Problem-solving playbook: `playbooks/problem-solving.md`
   - When to use /problem-solving vs direct research
   - Agent selection guide (ps-researcher, ps-analyst, ps-architect, etc.)
   - Common workflow patterns
3. Orchestration playbook: `playbooks/orchestration.md`
   - When to use /orchestration vs sequential agent invocation
   - Pipeline design patterns (cross-pollinated, fan-out, sequential)
   - State management and recovery
4. Transcript playbook: `playbooks/transcript.md`
   - Format selection (VTT preferred, SRT/TXT fallback)
   - Domain selection guide
   - Model selection for cost/quality optimization
5. Include decision trees as ASCII diagrams

---

## Acceptance Criteria

### Definition of Done

- [ ] At least 3 skill playbooks created (problem-solving, orchestration, transcript)
- [ ] Each playbook includes "When to Use" decision tree
- [ ] Each playbook includes worked examples
- [ ] Each playbook includes common anti-patterns
- [ ] All playbooks follow structure defined in EN-942
- [ ] All playbooks follow navigation standards (H-23, H-24)

---

## Dependencies

### Depends On

- [EN-942](../EN-942-runbook-playbook-scope/EN-942-runbook-playbook-scope.md) - Scope defines playbook structure
- [EN-943](../EN-943-getting-started-runbook/EN-943-getting-started-runbook.md) - Getting-started precedes advanced playbooks

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-02-17 | Claude | pending | Created from transcript analysis (ACT-005, TOP-004) |
