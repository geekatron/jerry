# TASK-032: Add CODEOWNERS for Workflow Files

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

No CODEOWNERS file exists. Workflow files (`.github/workflows/`) can be modified in PRs without designated reviewer approval. Adding CODEOWNERS ensures pipeline changes require explicit review from a security-aware maintainer.

**Finding:** red-recon (MEDIUM), no CODEOWNERS file detected

---

## Acceptance Criteria

- [ ] `.github/CODEOWNERS` file created
- [ ] `.github/workflows/` requires review from designated maintainer(s)
- [ ] `.github/dependabot.yml` requires review from designated maintainer(s)
- [ ] Branch protection rules enforce CODEOWNERS review
