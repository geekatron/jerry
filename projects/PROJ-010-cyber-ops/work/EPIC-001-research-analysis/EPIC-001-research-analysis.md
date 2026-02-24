# EPIC-001: Research & Analysis

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

Comprehensive research and analysis across 6 streams to establish the evidence base for PROJ-010 Cyber Ops. Covers offensive security methodology (MITRE ATT&CK, PTES, OSSTMM), defensive engineering practices (OWASP, NIST, CIS, SANS), role completeness analysis against industry teams, tool integration landscape, prior art survey, and LLM agent team patterns.

**Key Objectives:**
- Validate and refine agent rosters for /eng-team and /red-team through gap analysis against industry team structures
- Map offensive and defensive tooling integration points (Metasploit, Burp Suite, Semgrep, etc.)
- Research LLM portability patterns across providers (OpenAI, Anthropic, Google, open-source)
- Survey prior art (PentestGPT, HackerGPT, XBOW, Microsoft Copilot for Security) and establish differentiation
- Produce evidence-cited research artifacts for all Phase 2 architectural decisions (R-006)
- Persist all findings to `work/research/` per R-007

---

## Business Outcome Hypothesis

**We believe that** comprehensive, evidence-driven research across offensive security, defensive engineering, tool integration, portability, and prior art domains

**Will result in** architecturally sound decisions for /eng-team and /red-team that are grounded in industry reality rather than assumptions

**We will know we have succeeded when** all Phase 2 ADRs cite specific research findings, role gap analysis produces zero uncovered MITRE ATT&CK tactics, and the research compendium passes C4 /adversary review at >= 0.95

---

## Children Features/Capabilities

### Feature Inventory

| ID | Title | Status | Priority | Progress |
|----|-------|--------|----------|----------|
| FEAT-001 | Offensive Security Research | pending | critical | 0% |
| FEAT-002 | Defensive Engineering Research | pending | critical | 0% |
| FEAT-003 | Role Completeness Analysis | pending | critical | 0% |
| FEAT-004 | Tool Integration Landscape Research | pending | high | 0% |
| FEAT-005 | Prior Art & Industry Standards | pending | high | 0% |
| FEAT-006 | LLM Agent Team Patterns Research | pending | high | 0% |

### Feature Links

- [FEAT-001: Offensive Security Research](./FEAT-001-offensive-security-research/FEAT-001-offensive-security-research.md)
- [FEAT-002: Defensive Engineering Research](./FEAT-002-defensive-engineering-research/FEAT-002-defensive-engineering-research.md)
- [FEAT-003: Role Completeness Analysis](./FEAT-003-role-completeness-analysis/FEAT-003-role-completeness-analysis.md)
- [FEAT-004: Tool Integration Landscape Research](./FEAT-004-tool-integration-landscape/FEAT-004-tool-integration-landscape.md)
- [FEAT-005: Prior Art & Industry Standards](./FEAT-005-prior-art-industry-standards/FEAT-005-prior-art-industry-standards.md)
- [FEAT-006: LLM Agent Team Patterns Research](./FEAT-006-llm-agent-team-patterns/FEAT-006-llm-agent-team-patterns.md)

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
| Blocks | EPIC-002 | Architecture decisions depend on research findings |

### Research Output

All research artifacts persisted to `work/research/`:
- `stream-a-role-completeness/` (4 files)
- `stream-b-methodology/` (4 files)
- `stream-c-tool-integration/` (3 files)
- `stream-d-prior-art/` (3 files)
- `stream-e-llm-portability/` (3 files)
- `stream-f-secure-sdlc/` (3 files)
- `synthesis/` (3 files)
- `quality/` (barrier scores)

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-02-22 | Claude | pending | Epic created with 6 features, 25 enablers |
