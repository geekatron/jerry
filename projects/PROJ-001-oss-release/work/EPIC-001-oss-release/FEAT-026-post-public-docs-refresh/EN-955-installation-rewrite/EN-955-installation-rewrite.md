# EN-955: Installation Guide Public-Repo Rewrite

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
> **Effort:** 5

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

Rewrite `docs/INSTALLATION.md` to remove all private-repository collaborator sections and make the public HTTPS clone the primary installation path. The current document was written for the private-repo era and contains ~200 lines of SSH key setup, collaborator invitation workflows, PAT configuration, and "Future: Public Repository" placeholder sections that are now the current reality.

**Technical Scope:**
- Remove "Collaborator Installation (Private Repository)" section (lines 47-218)
- Remove or reframe PAT Alternative section (lines 224-274)
- Promote "Future: Public Repository Installation" content into the main flow
- Remove collaborator cross-reference callouts (lines 319, 408)
- Update/remove private-repo troubleshooting entries (lines 680-714)
- Update Table of Contents to reflect new structure
- Retain SSH as an optional advanced clone method (not mandatory)

---

## Problem Statement

Users arriving at `docs/INSTALLATION.md` (via docs site or README) encounter instructions telling them Jerry is a "private repository" requiring collaborator invitations and SSH key setup. This is factually wrong since FEAT-025 flipped the repo to public. The document creates confusion and friction for new users who can simply `git clone` via HTTPS.

---

## Tasks

| ID | Title | Status | Effort |
|----|-------|--------|--------|
| TASK-001 | Remove "Collaborator Installation" section (lines 47-218) | done | 1 |
| TASK-002 | Remove/reframe PAT Alternative section (lines 224-274) | done | 1 |
| TASK-003 | Merge "Future: Public Repository" into main installation flow | done | 1 |
| TASK-004 | Remove collaborator callouts and cross-references | done | 1 |
| TASK-005 | Update troubleshooting section (remove private-repo entries, keep useful SSH/general entries) | done | 1 |

---

## Acceptance Criteria

| ID | Criterion | Status |
|----|-----------|--------|
| AC-1 | No occurrences of "private repository", "collaborator invitation", or "distributed to collaborators only" in `docs/INSTALLATION.md` | PASS |
| AC-2 | HTTPS clone (`git clone https://github.com/geekatron/jerry.git`) is the primary method | PASS |
| AC-3 | SSH clone is documented as optional/advanced, not mandatory | PASS |
| AC-4 | "Future: Public Repository" section is removed (content merged into main flow) | PASS |
| AC-5 | PAT section removed or reframed as optional for rate-limit avoidance, not required for clone | PASS |
| AC-6 | Table of Contents reflects the new document structure | PASS |
| AC-7 | All internal anchor links are valid (no broken cross-references) | PASS |

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-02-19 | Claude | pending | Enabler created. 5 tasks, 5 effort pts. Rewrite INSTALLATION.md for public repo. |
| 2026-02-19 | Claude | done | INSTALLATION.md fully rewritten for public repo. Removed ~360 lines of private-repo content (collaborator sections, PAT setup, SSH-as-mandatory). HTTPS public clone is primary path. SSH retained as optional advanced method. C2 quality gate PASS (0.9195): S-003 Steelman (4 Major applied), S-007 Constitutional (1 Major fixed), S-002 Devil's Advocate (5 Major applied), S-014 scored 0.8925 REVISE → 0.9195 PASS after targeted fixes. All 7 ACs verified. |
