# EN-956: Docs Site Disclaimers & Notices

> **Type:** enabler
> **Status:** done
> **Priority:** high
> **Impact:** high
> **Enabler Type:** compliance
> **Created:** 2026-02-19
> **Due:** ---
> **Completed:** 2026-02-19
> **Parent:** FEAT-026
> **Owner:** Claude
> **Effort:** 3

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Brief description and technical scope |
| [Problem Statement](#problem-statement) | Why this enabler is needed |
| [Tasks](#tasks) | Work breakdown |
| [Acceptance Criteria](#acceptance-criteria) | Definition of done |
| [History](#history) | Status changes and key events |

---

## Summary

Add platform support, known limitations, and framework maturity disclaimers to the MkDocs documentation site (`jerry.geekatron.org`). The `README.md` already contains a Platform Support table and Known Limitations section, but these were never ported to the docs site. New users arriving via the docs site get no warning about platform compatibility or skill optimization status.

**Technical Scope:**
- Add platform support table to `docs/index.md` (macOS primary, Linux community-supported, Windows experimental)
- Add known limitations notice to `docs/index.md` (skill optimization, Windows portability)
- Add framework maturity/early-access notice to `docs/index.md`
- Add platform compatibility note to `docs/INSTALLATION.md` header (before installation steps)

**Source content:** `README.md` lines 80-102 (Platform Support table, Known Limitations)

---

## Problem Statement

The public-facing docs site at `jerry.geekatron.org` has no platform compatibility warnings, no skill optimization disclaimers, and no framework maturity indicators. Users on Linux or Windows get no upfront notice that their platform is not the primary development target before beginning installation. The README has this information but the docs site does not.

---

## Tasks

| ID | Title | Status | Effort |
|----|-------|--------|--------|
| TASK-001 | Add platform support table and known limitations to `docs/index.md` | done | 1 |
| TASK-002 | Add framework maturity/early-access notice to `docs/index.md` | done | 1 |
| TASK-003 | Add platform compatibility note to `docs/INSTALLATION.md` header | done | 1 |

---

## Acceptance Criteria

| ID | Criterion | Status |
|----|-----------|--------|
| AC-1 | `docs/index.md` contains platform support table with macOS/Linux/Windows status | PASS |
| AC-2 | `docs/index.md` contains known limitations section (skill optimization, Windows portability) | PASS |
| AC-3 | `docs/index.md` contains framework maturity notice | PASS |
| AC-4 | `docs/INSTALLATION.md` has platform compatibility note before first installation step | PASS |
| AC-5 | Content is consistent with `README.md` platform support and known limitations sections | PASS |

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-02-19 | Claude | pending | Enabler created. 3 tasks, 3 effort pts. Port README disclaimers to docs site. |
| 2026-02-19 | Claude | done | All disclaimers and notices added to docs/index.md: Platform Support table (macOS primary, Linux CI-tested, Windows in-progress), Known Limitations section, Early Access Notice with release tag pinning guidance. Platform Note added to docs/INSTALLATION.md header. Content aligned with README.md. C2 quality gate applied jointly with EN-955 — PASS (0.9195). All 5 ACs verified. |
