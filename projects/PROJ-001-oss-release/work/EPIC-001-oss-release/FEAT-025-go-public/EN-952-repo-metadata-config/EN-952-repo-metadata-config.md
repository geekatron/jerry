# EN-952: Repository Metadata & Configuration

> **Type:** enabler
> **Status:** done
> **Priority:** high
> **Impact:** medium
> **Enabler Type:** infrastructure
> **Created:** 2026-02-18
> **Due:** ---
> **Completed:** 2026-02-18
> **Parent:** FEAT-025
> **Owner:** ---
> **Effort:** 2

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Brief description and technical scope |
| [Acceptance Criteria](#acceptance-criteria) | Definition of done |
| [History](#history) | Status changes and key events |

---

## Summary

Configure GitHub repository metadata via `gh api` to present a polished public face:

1. Set description: "A Claude Code plugin for behavior and workflow guardrails with knowledge accrual"
2. Set homepage: `https://jerry.geekatron.org`
3. Set topics: `claude-code`, `claude`, `ai-agent`, `developer-tools`, `quality-framework`, `plugin`, `python`, `workflow-automation`
4. Disable wiki (redundant with docs site)
5. Fix license detection

---

## Acceptance Criteria

| ID | Criterion | Status |
|----|-----------|--------|
| AC-1 | Description is set and visible on repo page | PASS |
| AC-2 | Homepage points to jerry.geekatron.org | PASS |
| AC-3 | Topics are set (8 tags) | PASS |
| AC-4 | Wiki disabled | PASS |

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-02-18 | Claude | pending | Enabler created. Blocked by EN-953 (security audit). |
| 2026-02-18 | User/Claude | done | All metadata set via gh CLI (geekatron account). Verified: description, homepage, 8 topics, wiki disabled. License detection deferred (expected to auto-resolve on public). |
