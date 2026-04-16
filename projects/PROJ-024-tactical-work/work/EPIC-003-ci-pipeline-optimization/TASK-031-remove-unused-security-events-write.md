# TASK-031: Remove Unused security-events:write Permission

> **Type:** task
> **Status:** completed
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

- [x] `security-events: write` removed from security-scan.yml permissions
- [x] If SARIF upload is planned, document the intent in a comment instead — no SARIF upload exists; permission was unused
- [x] Security scan still functions correctly after permission removal

## Evidence

| Verification | Agent | Result |
|-------------|-------|--------|
| No step requires security-events:write | eng-devsecops | PASS — GITHUB_STEP_SUMMARY/OUTPUT use runner file descriptors, not API |
| Blast radius eliminated | red-recon | CLOSED — compromised workflow can no longer write to Security tab |
| Reference doc updated | diataxis-reference | Permissions table added to Scheduled Security Scan section |
