# EN-954: Visibility Flip & Post-Public Verification

> **Type:** enabler
> **Status:** pending
> **Priority:** critical
> **Impact:** high
> **Enabler Type:** infrastructure
> **Created:** 2026-02-18
> **Due:** ---
> **Completed:** ---
> **Parent:** FEAT-025
> **Owner:** ---
> **Effort:** 1

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Brief description and technical scope |
| [Acceptance Criteria](#acceptance-criteria) | Definition of done |
| [History](#history) | Status changes and key events |

---

## Summary

Flip the repository from private to public and verify everything works post-flip. This is the final step — all other enablers must be complete first.

**Steps:**
1. `gh api -X PATCH repos/geekatron/jerry -f visibility=public` (REQUIRES USER CONFIRMATION)
2. Verify anonymous clone
3. Verify docs site still serves
4. Check community profile score

---

## Acceptance Criteria

| ID | Criterion | Status |
|----|-----------|--------|
| AC-1 | Repository visibility is `public` | pending |
| AC-2 | Anonymous clone succeeds | pending |
| AC-3 | Docs site accessible | pending |
| AC-4 | Community profile shows all health files present | pending |

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-02-18 | Claude | pending | Enabler created. Blocked by EN-951, EN-952, EN-953. |
