# TASK-033: Evaluate docs.yml deploy-pages Migration

> **Type:** task
> **Status:** pending
> **Priority:** low
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

`docs.yml` uses `contents: write` to push to gh-pages via `mkdocs gh-deploy --force`. This is broader than needed — `contents: write` also grants ability to push to main or create tags. Evaluate migrating to `actions/deploy-pages` which uses the more targeted `pages: write` + `id-token: write` permissions.

**Finding:** eng-devsecops Finding 10 (LOW), `docs.yml:21-22`

---

## Acceptance Criteria

- [ ] Migration feasibility evaluated (MkDocs compatibility with deploy-pages action)
- [ ] Decision documented: migrate or keep with rationale
- [ ] If migrated: docs deploy still works, permissions reduced to pages:write
