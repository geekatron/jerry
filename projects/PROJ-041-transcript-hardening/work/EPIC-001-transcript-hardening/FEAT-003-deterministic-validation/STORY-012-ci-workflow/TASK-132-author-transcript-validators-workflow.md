# TASK-132: Author .github/workflows/transcript-validators.yml; hash-pin actions; coverage gates

> **Type:** task
> **Status:** pending
> **Priority:** high
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

CI gate runs validators on PR. Configure ≥90% module / ≥95% subprocess sandbox coverage gates. Hash-pin all action versions per supply-chain hardening.

---

## Acceptance Criteria

- [ ] Workflow file exists with `pull_request` trigger and path filters
- [ ] All action versions hash-pinned (no float tags)
- [ ] Coverage gates configured per spec
