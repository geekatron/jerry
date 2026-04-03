# BUG-007: Fix Broken mkdocs Anchor Links (GH #213)

> **Type:** bug
> **Status:** completed
> **Priority:** high
> **Impact:** high
> **Severity:** major
> **Created:** 2026-03-21T00:00:00Z
> **Due:**
> **Completed:** 2026-03-30T14:00:00Z
> **Parent:** FEAT-001
> **Owner:** adam.nowak
> **Found In:** 0.29.1
> **GitHub Issue:** [#213](https://github.com/geekatron/jerry/issues/213)

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | What's broken |
| [Steps to Reproduce](#steps-to-reproduce) | How to observe the bug |
| [Acceptance Criteria](#acceptance-criteria) | Verification checklist |
| [Fix Description](#fix-description) | What was changed |
| [Related Items](#related-items) | Hierarchy and links |
| [History](#history) | Change log |

---

## Steps to Reproduce

1. Run `uv run python -m mkdocs build --strict`
2. Observe 8 "does not contain an anchor" errors in output
3. Pre-commit pytest hook fails because `tests/e2e/test_mkdocs_research_validation.py` builds the site with `--strict`

---

## Summary

`mkdocs build --strict` reported 8 broken anchor links across 7 documentation files. Broken anchors caused by heading renames in INSTALLATION.md without updating cross-references, and by adv-scorer generating Document Sections tables with truncated anchor slugs that don't match actual heading text.

---

## Acceptance Criteria

- [x] All 8 broken anchor links resolved
- [x] `mkdocs build --strict` exits 0 with zero anchor errors
- [x] `pytest tests/e2e/test_mkdocs_research_validation.py` passes (3 tests)
- [x] Pre-commit hooks pass

---

## Fix Description

### Changes Made

| # | File | Fix |
|---|------|-----|
| 1 | `docs/index.md` | `#alternative-local-clone-install` -> `#local-clone` |
| 2 | `docs/index.md` | `#enable-hooks-recommended` -> `#enable-hooks-early-access` |
| 3 | `docs/howto/update-sha-pinned-action.md` | `#5-update-the-reference-document` -> `#5-update-the-sha-to-version-mapping-table` |
| 4 | `docs/scores/adversary/en-001-s014-rescore.md` | Added `## References` section + nav table entry |
| 5-8 | 4 voice score files | `#improvement-recommendations` -> `#improvement-recommendations-priority-ordered` |

---

## Related Items

### Hierarchy

- **Parent:** [FEAT-001](../FEAT-001-claude-code-schema-validation.md)

### Related Items

- **Fix Commit:** `5ffce5e7`
- **Dependency fix:** `1597e224` (pymdown-extensions 10.21.2 upgrade fixed mkdocs build crash)

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-03-21 | adam.nowak | pending | Discovered during PROJ-023 CLM commit. GH #213 created. |
| 2026-03-30 | adam.nowak | completed | Commit `5ffce5e7`. Fixed 8 anchors (7 from issue + 1 found via ps-analyst). GH #213 closed. |
