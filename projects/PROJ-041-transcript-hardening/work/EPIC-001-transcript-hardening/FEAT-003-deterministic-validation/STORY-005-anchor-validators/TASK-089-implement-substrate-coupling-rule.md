# TASK-089: Implement substrate-coupling rule (ANCHOR-003) using SubprocessSandbox

> **Type:** task
> **Status:** pending
> **Priority:** critical
> **Created:** 2026-04-29T00:00:00Z
> **Parent:** STORY-005
> **Owner:** eng-backend

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Task scope and rationale |
| [Acceptance Criteria](#acceptance-criteria) | Verifiable completion criteria |

---

## Summary

Walk `_anchors.json.audit_breakdown.per_bucket_derivation` patterns through SubprocessSandbox; assert walked == declared per bucket. **The rule that catches the iter-9 audit drift class.**

---

## Acceptance Criteria

- [ ] Substrate-coupling rule passes tests
- [ ] Routes ALL grep execution through SubprocessSandbox port (no direct subprocess calls)
- [ ] Reproduces audit's iter-9 drift detection (declared 33 vs walked 32)
