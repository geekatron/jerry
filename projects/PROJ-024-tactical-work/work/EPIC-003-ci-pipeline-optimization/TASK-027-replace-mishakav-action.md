# TASK-027: Evaluate Replacing MishaKav Coverage Comment Action

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

`MishaKav/pytest-coverage-comment` is a single-maintainer action processing attacker-generated coverage XML with `pull-requests: write` permission. SHA-pinned (frozen) but represents the weakest third-party trust link. Evaluate replacing with `actions/github-script` to post coverage comments directly, eliminating the third-party dependency.

**Finding:** eng-devsecops Finding 4 (MEDIUM) + red-recon FINDING-001, `ci.yml:371`

---

## Acceptance Criteria

- [ ] Alternatives evaluated (github-script, native GitHub coverage, inline script)
- [ ] Decision documented: replace or keep with documented rationale
- [ ] If replaced: PR coverage comments still appear with equivalent information
- [ ] If kept: added to quarterly third-party action review checklist
