# EN-005: Add .gitattributes for Cross-Platform Line Ending Normalization (GH #116)

> **Type:** enabler
> **Status:** completed
> **Priority:** medium
> **Impact:** medium
> **Enabler Type:** infrastructure
> **Created:** 2026-02-26T00:00:00Z
> **Due:**
> **Completed:** 2026-03-30T14:00:00Z
> **Parent:** FEAT-001
> **Owner:** adam.nowak
> **Effort:** 1
> **GitHub Issue:** [#116](https://github.com/geekatron/jerry/issues/116)

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | What and why |
| [Technical Approach](#technical-approach) | How it was implemented |
| [Acceptance Criteria](#acceptance-criteria) | Verification checklist |
| [Related Items](#related-items) | Hierarchy and links |
| [History](#history) | Change log |

---

## Summary

Repository lacked `.gitattributes` for line ending normalization. Shell scripts with CRLF fail silently (`/bin/bash\r: bad interpreter`). Adopted comprehensive red-team-reviewed `.gitattributes` from prior branch `feat/116-gitattributes-cross-platform` covering all tracked file types, semantic diff drivers, and defense-in-depth binary markers.

---

## Technical Approach

Adopted the comprehensive `.gitattributes` from prior branch `feat/116-gitattributes-cross-platform` (red-team reviewed, 136 lines). File uses `* text=auto eol=lf` baseline with explicit overrides for all tracked file types, semantic diff drivers (`diff=python`, `diff=markdown`), Windows CRLF proactive coverage, and defense-in-depth binary markers. Post-creation step: `git add --renormalize .` (no-op on macOS, already LF).

---

## Acceptance Criteria

- [x] `.gitattributes` file added to repository root (136 lines)
- [x] Python, shell, and config files enforced LF
- [x] Windows scripts (`.bat`, `.cmd`, `.ps1`) proactively set to CRLF
- [x] Binary files (PDF, images, fonts, archives) marked as binary
- [x] Existing files normalized via `git add --renormalize .` (no-op on macOS)
- [ ] CI `git diff --check` step — deferred (OAuth scope issue per prior branch)

---

## Related Items

### Hierarchy

- **Parent:** [FEAT-001](../FEAT-001-claude-code-schema-validation.md)

### Related Items

- **Fix Commit:** `96c4ca19`
- **Prior Branch:** `feat/116-gitattributes-cross-platform` (adopted verbatim)
- **Source:** PORT-001 Portability Analysis (2026-02-26)

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-02-26 | adam.nowak | pending | PORT-001 identified gap. GH #116 created. |
| 2026-03-01 | adam.nowak | in_progress | Work on feat/116-gitattributes-cross-platform. Deferred due to CI OAuth scope. |
| 2026-03-30 | adam.nowak | completed | Adopted prior branch .gitattributes verbatim. Commit `96c4ca19`. GH #116 closed. |
