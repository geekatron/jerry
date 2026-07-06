# STORY-004: STRIDE Threat Model of Derived-Branch CI

<!--
TEMPLATE: Story
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.5
PURPOSE: Red-team STRIDE threat model of the regeneration/force-push CI pipeline
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

**As a** Jerry maintainer responsible for the distribution pipeline

**I want** a STRIDE threat model of the derived-branch CI

**So that** force-push, token/secrets, and supply-chain threats are identified and rated before the automation ships

---

## Summary

Produce a red-team STRIDE threat model (via `/red-team`) of the regeneration/force-push automation. Enumerate threats across the force-push surface (history rewrite, branch hijack), the token and secrets surface (credential theft, over-scoped tokens, log leakage), and the supply-chain surface (dependency tampering, malicious workflow edits), and assign a severity rating to each.

**Scope:**
- Force-push abuse and history-rewrite threats on `cowork-skeleton`
- Token and secrets exposure threats in the workflow
- Supply-chain tampering threats in the regeneration pipeline
- Severity rating per threat (handoff to STORY-005)

---

## Acceptance Criteria

### Acceptance Checklist

- [ ] Threat model enumerates force-push and history-rewrite threats with severity ratings
- [ ] Threat model enumerates token and secrets exposure threats with severity ratings
- [ ] Threat model enumerates supply-chain tampering threats with severity ratings
- [ ] Each threat is mapped to a STRIDE category and a trust boundary
- [ ] Threat model output is structured for remediation handoff to STORY-005

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
| Depends On | EN-001 | The CI workflow is the system under analysis |
| Blocks | STORY-005 | Remediations consume the rated threat list |

### GitHub Issue Parity (H-32)

- **GitHub Issue:** Pending — per H-32, GitHub Issue parity is required. Child issues to be created after the approval gate; tracked under parent Epic [#305](https://github.com/geekatron/jerry/issues/305).

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-06-26 | adam.nowak | pending | Story created |
