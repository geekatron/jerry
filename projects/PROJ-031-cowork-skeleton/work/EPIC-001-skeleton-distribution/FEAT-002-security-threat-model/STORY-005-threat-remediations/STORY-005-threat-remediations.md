# STORY-005: Threat Remediations and Branch-Protection Strategy

<!--
TEMPLATE: Story
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.5
PURPOSE: eng-team remediations for STRIDE findings plus the cowork-skeleton branch-protection strategy
-->

> **Type:** story
> **Status:** pending
> **Priority:** high
> **Impact:** high
> **Created:** 2026-06-26T12:00:00Z
> **Due:**
> **Completed:**
> **Parent:** FEAT-002
> **Owner:** adam.nowak
> **Effort:** 5

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [User Story](#user-story) | As a / I want / So that |
| [Summary](#summary) | Scope and approach |
| [Acceptance Criteria](#acceptance-criteria) | Verification checklist |
| [Progress Summary](#progress-summary) | Overall progress |
| [Related Items](#related-items) | Links, dependencies, GitHub parity |
| [History](#history) | Status changes |

---

## User Story

**As a** Jerry maintainer

**I want** concrete remediations for the STRIDE findings and a branch-protection strategy

**So that** the distribution pipeline ships with no unmitigated critical or high-severity risk

---

## Summary

Apply eng-team (`/eng-team`) remediations to the threats identified in STORY-004 and define the branch-protection strategy for `cowork-skeleton`. Each critical or high finding gets a remediation or an explicit accepted-risk decision; the branch-protection posture must coexist with the automated force-push from EN-001.

**Scope:**
- Remediation per critical/high STRIDE finding (or accepted-risk decision)
- Branch-protection strategy for the force-pushed `cowork-skeleton` branch
- Verification that remediations close the rated threats

---

## Acceptance Criteria

### Acceptance Checklist

- [ ] Every critical and high finding has a remediation or a documented accepted-risk decision
- [ ] Branch-protection strategy for `cowork-skeleton` is defined and compatible with automated force-push
- [ ] Token and secrets handling remediations are specified for the workflow
- [ ] Supply-chain remediations are specified for the regeneration pipeline
- [ ] Residual risk after remediation is documented

---

## Progress Summary

```
+------------------------------------------------------------------+
|                    STORY PROGRESS TRACKER                         |
+------------------------------------------------------------------+
| Tasks:     [....................] 0% (0/0 defined)                |
+------------------------------------------------------------------+
| Overall:   [....................] 0%                              |
+------------------------------------------------------------------+
```

---

## Related Items

### Hierarchy

- **Parent Feature:** [FEAT-002: Security and Threat Model](../FEAT-002-security-threat-model.md)

### Dependencies

| Dependency Type | Item | Description |
|----------------|------|-------------|
| Depends On | STORY-004 | Consumes the rated threat list |
| Related | TASK-003 | Aligns with the EN-001 token and branch-protection strategy |

### GitHub Issue Parity (H-32)

- **GitHub Issue:** Pending — per H-32, GitHub Issue parity is required. Child issues to be created after the approval gate; tracked under parent Epic [#305](https://github.com/geekatron/jerry/issues/305).

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-06-26 | adam.nowak | pending | Story created |
