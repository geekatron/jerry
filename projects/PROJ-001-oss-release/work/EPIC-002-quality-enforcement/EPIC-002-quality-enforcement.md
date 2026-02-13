# EPIC-002: Quality Framework Enforcement & Course Correction

<!--
TEMPLATE: Epic
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.2
CREATED: 2026-02-12 (Claude)
PURPOSE: Enforce quality framework compliance and retroactively validate EPIC-001 deliverables
-->

> **Type:** epic
> **Status:** in_progress
> **Priority:** critical
> **Impact:** critical
> **Created:** 2026-02-12
> **Due:** —
> **Completed:** —
> **Parent:** —
> **Owner:** Adam Nowak
> **Target Quarter:** FY26-Q1

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Epic overview and key objectives |
| [Business Outcome Hypothesis](#business-outcome-hypothesis) | Expected outcomes from enforcement |
| [Lean Business Case](#lean-business-case) | Why this investment is necessary |
| [Children (Features/Capabilities)](#children-featurescapabilities) | Feature inventory and tracking |
| [Progress Summary](#progress-summary) | Overall epic progress |
| [Related Items](#related-items) | Dependencies on EPIC-001 |
| [History](#history) | Status changes and key events |

---

## Summary

Establish enforceable quality mechanisms within the Jerry Framework that ensure Claude follows all quality constraints including adversarial feedback loops, quality scoring (>=0.92), creator-critic-revision cycles, and multi-platform testing. Additionally, retroactively validate ALL EPIC-001 deliverables that were closed without quality gates.

**Key Objectives:**
- Research and implement enforcement mechanisms that force compliance with Jerry's quality framework (hooks, rules, prompts, session context)
- Research 15 adversarial critic/review strategies, select best 10, define situational applicability, and enhance /problem-solving, /nasa-se, AND /orchestration skills
- Retroactively review ALL EPIC-001 deliverables through creator→critic→adversarial feedback loops with >=0.92 quality score
- Ensure platform portability across macOS, Windows, and Linux
- Create orchestration plans at Epic/Feature/Enabler level with quality gates baked into acceptance criteria
- All decisions must be evidence-driven with citations from authoritative industry sources

---

## Business Outcome Hypothesis

**We believe that** establishing enforceable quality mechanisms with adversarial feedback loops and retroactively validating EPIC-001 deliverables

**Will result in** a framework that produces mission-critical quality outputs with verifiable evidence, measurable quality scores, and enforced process compliance

**We will know we have succeeded when:**
- All enforcement mechanisms are operational and prevent quality bypasses
- 10 adversarial strategies are documented, integrated, and tested
- All EPIC-001 deliverables pass retroactive quality review (>=0.92)
- /problem-solving, /nasa-se, and /orchestration skills are enhanced with adversarial capabilities
- Advanced adversarial capabilities (automated selection, metrics, A/B testing) researched and implemented
- Platform portability is verified on macOS, Windows, and Linux

---

## Lean Business Case

| Aspect | Description |
|--------|-------------|
| **Problem** | Claude repeatedly bypasses Jerry's quality framework (skills, adversarial loops, quality gates) despite rules being loaded into context. This produces unvalidated deliverables with zero trust and zero visibility. |
| **Solution** | Multi-vector enforcement (hooks, rules, prompts, session context) + adversarial strategy research + retroactive quality review + skill enhancement |
| **Cost** | Significant token investment for deep research, adversarial cycles, and retroactive review |
| **Benefit** | Mission-critical quality assurance, verifiable evidence trail, enforced process compliance, restored trust |
| **Risk** | Enforcement mechanisms may add overhead to simple tasks (mitigate: tiered enforcement based on task complexity) |

---

## Children (Features/Capabilities)

### Feature Inventory

| ID | Title | Status | Priority | Enablers | Effort | Progress |
|----|-------|--------|----------|----------|--------|----------|
| FEAT-004 | Adversarial Strategy Research & Skill Enhancement | in_progress | critical | 7 (EN-301–307) | 57 | 5% |
| FEAT-005 | Quality Framework Enforcement Mechanisms | in_progress | critical | 6 (EN-401–406) | 49 | 5% |
| FEAT-006 | EPIC-001 Retroactive Quality Review | pending | high | 5 (EN-501–505) | 42 | 0% |
| FEAT-007 | Advanced Adversarial Capabilities | pending | high | 5 (EN-601–605) | 51 | 0% |

### Feature Links

- [FEAT-004: Adversarial Strategy Research & Skill Enhancement](./FEAT-004-adversarial-strategy-research/FEAT-004-adversarial-strategy-research.md)
- [FEAT-005: Quality Framework Enforcement Mechanisms](./FEAT-005-enforcement-mechanisms/FEAT-005-enforcement-mechanisms.md)
- [FEAT-006: EPIC-001 Retroactive Quality Review](./FEAT-006-epic001-retroactive-review/FEAT-006-epic001-retroactive-review.md)
- [FEAT-007: Advanced Adversarial Capabilities](./FEAT-007-advanced-adversarial-capabilities/FEAT-007-advanced-adversarial-capabilities.md)

---

## Progress Summary

### Status Overview

```
+------------------------------------------------------------------+
|                     EPIC PROGRESS TRACKER                         |
+------------------------------------------------------------------+
| Features:  [....................] 0% (0/4 completed)              |
| Enablers:  [....................] 0% (0/23 completed)             |
| Tasks:     [....................] 0% (0/? completed)              |
+------------------------------------------------------------------+
| Overall:   [....................] 0%                               |
+------------------------------------------------------------------+
```

### Progress Metrics

| Metric | Value |
|--------|-------|
| **Total Features** | 4 |
| **Completed Features** | 0 |
| **In Progress Features** | 2 |
| **Pending Features** | 2 |
| **Total Enablers** | 23 |
| **Total Effort (points)** | 199 |
| **Feature Completion %** | 0% |

---

## Related Items

### Hierarchy

- **Parent:** None (top-level epic under PROJ-001-oss-release)

### Related Epics

- [EPIC-001: OSS Release Preparation](../EPIC-001-oss-release/EPIC-001-oss-release.md) - EPIC-002 remediates quality gaps from EPIC-001

### Dependencies

| Dependency Type | Item | Description |
|----------------|------|-------------|
| Depends On | EPIC-001 | FEAT-006 reviews EPIC-001 deliverables |
| Blocks | EPIC-001 closure | EPIC-001 cannot be re-closed until FEAT-006 validates all deliverables |

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-02-12 | Claude | pending | Epic created. EPIC-001 deliverables bypassed all quality gates (no adversarial feedback, no quality scoring, no creator→critic cycles, no multi-platform testing). This epic addresses enforcement and retroactive quality review. |
| 2026-02-12 | Claude | in_progress | Execution started. Orchestration plans dispatched for FEAT-004 and FEAT-005. Research agents launched: EN-301 (15 adversarial strategies) and EN-401 (enforcement vectors) running in parallel. |
| 2026-02-12 | Claude | in_progress | Course correction: Updated FEAT-004 ACs (18 functional + 8 NFC) and FEAT-005 ACs (19 functional + 8 NFC) to require full 22-agent utilization, DEC/DISC tracking, detailed enabler/task files. Added EN-307 (/orchestration skill enhancement). Created all 13 enabler entity files (EN-301–307, EN-401–406). Created FEAT-007 (Advanced Adversarial Capabilities) from FEAT-004 Out of Scope items with 5 enablers (EN-601–605). Total: 4 features, 23 enablers, 199 story points. |

---

## System Mapping

| System | Mapping |
|--------|---------|
| **Azure DevOps** | Epic |
| **SAFe** | Epic (Portfolio Backlog) |
| **JIRA** | Epic |
