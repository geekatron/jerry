# TASK-032: Add CODEOWNERS for Workflow Files

> **Type:** task
> **Status:** completed
> **Priority:** medium
> **Created:** 2026-04-15
> **Completed:** 2026-04-16
> **Parent:** EN-006
> **GitHub Issue:** [#252](https://github.com/geekatron/jerry/issues/252)

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Task scope and rationale |
| [Acceptance Criteria](#acceptance-criteria) | Verifiable completion criteria |
| [Evidence](#evidence) | Verification record |

---

## Summary

No CODEOWNERS file exists. Workflow files (`.github/workflows/`) can be modified in PRs without designated reviewer approval. Adding CODEOWNERS ensures pipeline changes require explicit review from a security-aware maintainer.

**Finding:** red-recon (MEDIUM), no CODEOWNERS file detected

---

## Acceptance Criteria

- [x] `.github/CODEOWNERS` file created
- [x] `.github/workflows/` requires review from designated maintainer(s)
- [x] `.github/dependabot.yml` requires review from designated maintainer(s)
- [x] Branch protection rules enforce CODEOWNERS review — ruleset "Don't fuck with main" updated: `require_code_owner_review: true`, `enforcement: active`, `current_user_can_bypass: never`

## Evidence

| Verification | Agent | Result |
|-------------|-------|--------|
| Pattern syntax valid | eng-devsecops | PASS — directory trailing `/`, exact file paths, all correct |
| Attack surface closed | red-recon | CLOSED — ruleset "Don't fuck with main" enforces `require_code_owner_review: true` with `current_user_can_bypass: never` |
| DX impact assessed | ux-heuristic-evaluator | F-001 (Sev 3) fixed: CONTRIBUTING.md updated with Required Reviewers section |
| Reference doc updated | diataxis-reference | CODEOWNERS section added to ci-cd-pipeline-security.md |
