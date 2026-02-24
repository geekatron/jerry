# EPIC-006: Documentation & Guides

> **Type:** epic
> **Status:** pending
> **Priority:** high
> **Impact:** high
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

Complete documentation for both skills including user guides, rule set customization guide, tool integration guide, and framework registration (AGENTS.md, CLAUDE.md, mandatory-skill-usage.md). Documentation quality must meet industry leader standard per R-017.

**Key Objectives:**
- Produce /eng-team user documentation covering all 8 agents, routing, and workflows
- Produce /red-team user documentation covering all 9 agents, methodology, and authorization
- Write rule set customization guide enabling override/merge configuration per R-011
- Write tool integration guide for adding new adapters per R-012
- Complete framework registration in AGENTS.md, CLAUDE.md, and mandatory-skill-usage.md per R-022

---

## Business Outcome Hypothesis

**We believe that** comprehensive documentation covering user guides, customization, tool integration, and framework registration

**Will result in** adoption and customization of both skills without requiring deep framework expertise

**We will know we have succeeded when** all documentation passes C4 /adversary review at >= 0.95, framework registration is complete in all three files, and the customization guide enables rule set override without code changes

---

## Children Features/Capabilities

### Feature Inventory

| ID | Title | Status | Priority | Progress |
|----|-------|--------|----------|----------|
| FEAT-050 | /eng-team User Documentation | pending | high | 0% |
| FEAT-051 | /red-team User Documentation | pending | high | 0% |
| FEAT-052 | Rule Set Customization Guide | pending | high | 0% |
| FEAT-053 | Tool Integration Guide | pending | high | 0% |
| FEAT-054 | Framework Registration | pending | critical | 0% |

### Feature Links

- [FEAT-050: /eng-team User Documentation](./FEAT-050-eng-team-documentation/FEAT-050-eng-team-documentation.md)
- [FEAT-051: /red-team User Documentation](./FEAT-051-red-team-documentation/FEAT-051-red-team-documentation.md)
- [FEAT-052: Rule Set Customization Guide](./FEAT-052-rule-set-customization-guide/FEAT-052-rule-set-customization-guide.md)
- [FEAT-053: Tool Integration Guide](./FEAT-053-tool-integration-guide/FEAT-053-tool-integration-guide.md)
- [FEAT-054: Framework Registration](./FEAT-054-framework-registration/FEAT-054-framework-registration.md)

---

## Progress Summary

### Status Overview

```
+------------------------------------------------------------------+
|                     EPIC PROGRESS TRACKER                         |
+------------------------------------------------------------------+
| Features:  [....................] 0% (0/5 completed)              |
| Enablers:  [....................] 0% (0/18 completed)             |
+------------------------------------------------------------------+
| Overall:   [....................] 0%                               |
+------------------------------------------------------------------+
```

### Progress Metrics

| Metric | Value |
|--------|-------|
| **Total Features** | 5 |
| **Completed Features** | 0 |
| **In Progress Features** | 0 |
| **Pending Features** | 5 |
| **Feature Completion %** | 0% |

---

## Related Items

### Dependencies

| Dependency Type | Item | Description |
|----------------|------|-------------|
| Depends On | EPIC-003 | /eng-team documentation requires completed skill |
| Depends On | EPIC-004 | /red-team documentation requires completed skill |
| Depends On | EPIC-005 | Documentation reflects hardened, validated skills |

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-02-22 | Claude | pending | Epic created with 5 features, 18 enablers |
