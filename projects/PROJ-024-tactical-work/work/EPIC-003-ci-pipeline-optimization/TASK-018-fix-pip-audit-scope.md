# TASK-018: Fix Pip-Audit to Scan Full Dependency Tree

> **Type:** task
> **Status:** pending
> **Priority:** high
> **Created:** 2026-04-13
> **Parent:** EPIC-003
> **GitHub Issue:** [#252](https://github.com/geekatron/jerry/issues/252)

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Task scope and rationale |
| [Acceptance Criteria](#acceptance-criteria) | Verifiable completion criteria |

---

## Summary

The security job audits 3 hand-picked packages instead of the full project dependency graph. CVEs in pytest, mkdocs-material, or any transitive dependency are invisible. This task closes a supply chain gap by scanning the complete dependency tree.

---

## Acceptance Criteria

- [ ] `pip-audit` runs against `uv export --frozen --format requirements-txt --all-extras`
- [ ] All direct and transitive deps are covered
- [ ] Hand-picked package list removed
