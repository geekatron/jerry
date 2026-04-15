# TASK-031: Remove Unused security-events:write Permission

> **Type:** task
> **Status:** pending
> **Priority:** medium
> **Created:** 2026-04-15
> **Parent:** EN-006
> **GitHub Issue:** [#252](https://github.com/geekatron/jerry/issues/252)

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Task scope and rationale |
| [Acceptance Criteria](#acceptance-criteria) | Verifiable completion criteria |

---

## Summary

`security-scan.yml` declares `security-events: write` but no step uploads SARIF or writes security events. This is an over-scoped permission violating least privilege.

**Finding:** eng-devsecops Finding 8 (MEDIUM), `security-scan.yml:37`

---

## Acceptance Criteria

- [ ] `security-events: write` removed from security-scan.yml permissions
- [ ] If SARIF upload is planned, document the intent in a comment instead
- [ ] Security scan still functions correctly after permission removal
