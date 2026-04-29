# TASK-133: PR comment posting on failure (validator summary); branch protection update

> **Type:** task
> **Status:** pending
> **Priority:** medium
> **Created:** 2026-04-29T00:00:00Z
> **Parent:** STORY-012
> **Owner:** eng-devsecops

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Task scope and rationale |
| [Acceptance Criteria](#acceptance-criteria) | Verifiable completion criteria |

---

## Summary

PR comment posts validator summary when checks fail. Branch protection requires the check.

---

## Acceptance Criteria

- [ ] PR comment posts validator summary on failure (rules failed + goldens that failed)
- [ ] Branch protection updated to require this check
- [ ] Test PR confirms behavior
