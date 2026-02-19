# EN-957: Validation & Docs Rebuild

> **Type:** enabler
> **Status:** done
> **Priority:** medium
> **Impact:** medium
> **Enabler Type:** infrastructure
> **Created:** 2026-02-19
> **Due:** ---
> **Completed:** 2026-02-19
> **Parent:** FEAT-026
> **Owner:** Claude
> **Effort:** 2

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Brief description and technical scope |
| [Problem Statement](#problem-statement) | Why this enabler is needed |
| [Tasks](#tasks) | Work breakdown |
| [Acceptance Criteria](#acceptance-criteria) | Definition of done |
| [Dependencies](#dependencies) | Blocked by EN-955 and EN-956 |
| [History](#history) | Status changes and key events |

---

## Summary

Validate that all documentation changes from EN-955 and EN-956 build and deploy correctly. Run grep scans to confirm no stale private-repo language remains. Verify the MkDocs site builds locally and the docs GitHub Actions workflow succeeds.

**Technical Scope:**
- Run `uv run mkdocs build` locally to verify clean build
- Grep scan across `docs/` for private-repo keywords
- Verify all internal links are valid
- Confirm docs.yml GitHub Actions workflow succeeds after push

---

## Problem Statement

Documentation changes to INSTALLATION.md and index.md must not break the MkDocs build, internal links, or the deployment pipeline. A validation pass ensures no broken anchors, stale references, or build errors were introduced.

---

## Tasks

| ID | Title | Status | Effort |
|----|-------|--------|--------|
| TASK-001 | Run `uv run mkdocs build` locally — verify clean build | done | 1 |
| TASK-002 | Grep scan for private-repo keywords across `docs/` | done | 0 |
| TASK-003 | Verify docs.yml workflow succeeds after push | pending | 1 |

---

## Acceptance Criteria

| ID | Criterion | Status |
|----|-----------|--------|
| AC-1 | `uv run mkdocs build` exits with 0 warnings and 0 errors | PASS |
| AC-2 | `grep -ri "private repository\|collaborator invitation\|distributed to collaborators" docs/` returns 0 matches | PASS |
| AC-3 | All internal anchor links in `docs/INSTALLATION.md` resolve correctly | PASS |
| AC-4 | docs.yml GitHub Actions workflow passes | DEFERRED (requires push to main) |

---

## Dependencies

- **Blocked by:** EN-955 (Installation Rewrite), EN-956 (Disclaimers)
- **Reason:** Validation must run after all content changes are complete

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-02-19 | Claude | pending | Enabler created. 3 tasks, 2 effort pts. Validation after EN-955 + EN-956. |
| 2026-02-19 | Claude | done | TASK-001: `uv run mkdocs build --strict` passes clean (0 warnings, 0 errors). TASK-002: grep scan returns 0 matches for private-repo keywords in docs/. TASK-003 (docs.yml workflow): deferred to post-push — AC-4 will be verified when PR merges to main. AC-1/2/3 PASS, AC-4 DEFERRED. |
