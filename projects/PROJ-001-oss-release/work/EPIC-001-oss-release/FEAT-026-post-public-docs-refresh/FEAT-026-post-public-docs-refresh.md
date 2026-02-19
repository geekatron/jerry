# FEAT-026: Post-Public Documentation Refresh

<!--
TEMPLATE: Feature
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.4
CREATED: 2026-02-19 (Claude)
PURPOSE: Update all documentation to reflect public repository status
-->

> **Type:** feature
> **Status:** done
> **Priority:** high
> **Impact:** high
> **Created:** 2026-02-19
> **Due:** --
> **Completed:** 2026-02-19
> **Parent:** EPIC-001-oss-release
> **Owner:** Claude

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | What this feature delivers |
| [Acceptance Criteria](#acceptance-criteria) | Definition of done |
| [Enablers](#enablers) | Implementation work items |
| [Progress Summary](#progress-summary) | Tracking |
| [History](#history) | Change log |

---

## Summary

Now that the Jerry framework repository has been flipped from private to public (FEAT-025), all user-facing documentation must be updated to reflect the new access model. The installation guide (`docs/INSTALLATION.md`) still contains extensive private-repo collaborator sections (SSH setup, PAT configuration, collaborator invitations) that are now obsolete. The MkDocs docs site (`jerry.geekatron.org`) is missing platform support disclaimers, skill optimization notices, and framework maturity indicators that exist in the README but were never ported to the public-facing documentation.

**Key Objectives:**
- Rewrite `docs/INSTALLATION.md` to remove all private-repo collaborator sections and make HTTPS public clone the primary path
- Add platform support, known limitations, and framework maturity disclaimers to the docs site
- Verify the docs site builds and deploys cleanly after all changes

**Criticality:** C2 (Standard) — Public-facing documentation on live docs site (jerry.geekatron.org), 3-5 files, reversible within 1 day. Requires S-007, S-002, S-014 quality gate after content changes (EN-955 + EN-956) before validation (EN-957).

---

## Acceptance Criteria

| ID | Criterion | Status |
|----|-----------|--------|
| AC-1 | `docs/INSTALLATION.md` contains no references to "private repository", "collaborator invitation", or mandatory SSH/PAT setup for cloning | PASS |
| AC-2 | HTTPS `git clone https://github.com/geekatron/jerry.git` is the primary clone method in installation docs | PASS |
| AC-3 | "Future: Public Repository" section is removed or merged into main flow | PASS |
| AC-4 | `docs/index.md` includes platform support table (macOS primary, Linux community, Windows experimental) | PASS |
| AC-5 | `docs/index.md` includes known limitations notice (skill optimization, Windows portability) | PASS |
| AC-6 | MkDocs site builds successfully locally (`uv run mkdocs build`) | PASS |
| AC-7 | No stale private-repo language found via grep scan across `docs/` | PASS |

---

## Enablers

| ID | Title | Status | Priority | Effort |
|----|-------|--------|----------|--------|
| EN-955 | Installation Guide Public-Repo Rewrite | done | high | 5 |
| EN-956 | Docs Site Disclaimers & Notices | done | high | 3 |
| EN-957 | Validation & Docs Rebuild | done | medium | 2 |

### Enabler Links

- [EN-955: Installation Guide Public-Repo Rewrite](./EN-955-installation-rewrite/EN-955-installation-rewrite.md)
- [EN-956: Docs Site Disclaimers & Notices](./EN-956-docs-site-disclaimers/EN-956-docs-site-disclaimers.md)
- [EN-957: Validation & Docs Rebuild](./EN-957-validation-docs-rebuild/EN-957-validation-docs-rebuild.md)

### Execution Order

```
EN-955 (Installation Rewrite)    <- FIRST: largest change
    |
    +-- EN-956 (Disclaimers)     <- Parallel with EN-955
    |
    +-- EN-957 (Validation)      <- LAST: after EN-955 + EN-956 complete
```

---

## Progress Summary

| Metric | Value |
|--------|-------|
| **Total Enablers** | 3 |
| **Completed Enablers** | 3 |
| **Total Effort** | 10 |
| **Completion %** | 100% |

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-02-19 | Claude | pending | Feature created. 3 enablers (EN-955-957), 10 effort pts. Post-public repo documentation refresh — remove private-repo sections from INSTALLATION.md, add disclaimers to docs site. |
| 2026-02-19 | Claude | done | All 3 enablers complete (EN-955, EN-956, EN-957). C2 quality gate PASS (0.9195): S-003 Steelman, S-007 Constitutional, S-002 Devil's Advocate, S-014 LLM-as-Judge (0.8925 REVISE → 0.9195 PASS). INSTALLATION.md rewritten (~360 lines removed), docs/index.md enriched with platform support/limitations/maturity notices. MkDocs build clean. Grep scan 0 matches. All 7 feature-level ACs PASS. |
