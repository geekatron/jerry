# EPIC-001: Jerry OSS Release

<!--
TEMPLATE: Epic
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.2
CREATED: 2026-01-31
PURPOSE: Prepare Jerry Framework for open-source release
-->

> **Type:** epic
> **Status:** pending
> **Priority:** high
> **Impact:** high
> **Created:** 2026-01-31T16:00:00Z
> **Due:** TBD
> **Completed:** -
> **Parent:** PROJ-009-oss-release
> **Owner:** Adam Nowak / Claude
> **Target Quarter:** FY26-Q1

---

## Summary

Prepare the Jerry Framework for public open-source release under MIT license. This epic encompasses all work required to transform Jerry from an internal development tool to a polished, well-documented open-source project that serves users across multiple expertise levels.

**Key Objectives:**
- Complete deep research on Claude Code plugin, skill, and CLAUDE.md best practices
- Optimize CLAUDE.md and all skills using decomposition/imports patterns
- Complete the work tracker skill (extract from CLAUDE.md)
- Create multi-persona documentation (L0 ELI5, L1 Engineer, L2 Architect)
- Plan repository migration (jerry → source-repository, create new public jerry)

---

## Business Outcome Hypothesis

**We believe that** releasing Jerry as a well-documented open-source project with rigorous quality standards

**Will result in** increased adoption by developers seeking to improve their Claude Code experience, and community contributions that enhance the framework

**We will know we have succeeded when:**
- Documentation serves users from beginner to expert (L0/L1/L2)
- Repository is cleanly structured with best practices applied
- Work tracker skill is complete and extracted from CLAUDE.md
- Migration to public repository is planned and ready for execution

---

## Lean Business Case

| Aspect | Description |
|--------|-------------|
| **Problem** | Jerry is currently an internal development tool with documentation scattered across CLAUDE.md, lacking best practices, and not suitable for public release |
| **Solution** | Systematic research, optimization, and documentation following industry best practices and multi-persona accessibility |
| **Cost** | Development time for research, optimization, and documentation |
| **Benefit** | Open-source community adoption, contributions, and ecosystem growth |
| **Risk** | Scope creep during research phase; quality issues if rushed |

---

## Children (Features)

### Feature Inventory

| ID | Title | Status | Priority | Progress |
|----|-------|--------|----------|----------|
| [FEAT-001](./FEAT-001-research-and-preparation/FEAT-001-research-and-preparation.md) | Research and Preparation | pending | high | 0% |

### Planned Features (Future)

| ID | Title | Status | Priority |
|----|-------|--------|----------|
| FEAT-002 | Optimization | pending | high |
| FEAT-003 | Documentation | pending | high |
| FEAT-004 | Migration Planning | pending | high |

---

## Progress Summary

### Status Overview

```
+------------------------------------------------------------------+
|                     EPIC PROGRESS TRACKER                         |
+------------------------------------------------------------------+
| Features:  [....................] 0% (0/1 completed)             |
| Enablers:  [....................] 0% (0/6 planned)               |
| Tasks:     [....................] 0% (0/1 completed)             |
+------------------------------------------------------------------+
| Overall:   [....................] 0%                             |
+------------------------------------------------------------------+
```

### Progress Metrics

| Metric | Value |
|--------|-------|
| **Total Features** | 1 |
| **Completed Features** | 0 |
| **In Progress Features** | 0 |
| **Pending Features** | 1 |
| **Feature Completion %** | 0% |

### Milestone Tracking

| Milestone | Target Date | Status | Notes |
|-----------|-------------|--------|-------|
| Research Phase Complete | TBD | pending | Blocking for all other phases |
| Optimization Complete | TBD | pending | Depends on research |
| Documentation Complete | TBD | pending | Depends on optimization |
| Migration Plan Ready | TBD | pending | Final deliverable |

---

## Related Items

### Hierarchy

- **Parent:** [PROJ-009-oss-release](../../PLAN.md)

### Source Material

- **Transcript:** [001-oss-release](../../../../transcripts/001-oss-release/packet/) - Original action items
- **Adversarial Protocol:** [DISC-002](../../../PROJ-008-transcript-skill/work/EPIC-001-transcript-skill/FEAT-003-future-enhancements/FEAT-003--DISC-002-adversarial-prompting-protocol.md)

### Dependencies

| Dependency Type | Item | Description |
|----------------|------|-------------|
| Informs | PROJ-008 | Transcript skill learnings inform this work |
| References | EN-020 | Adversarial critic patterns for quality gates |

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-01-31 | Claude | pending | Epic created based on transcript analysis |

---

*Epic Version: 1.0.0*
*Created: 2026-01-31*
