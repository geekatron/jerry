# EN-939: Remove/Deprecate Archive-Based Installation Instructions

> **Type:** enabler
> **Status:** done
> **Priority:** high
> **Impact:** high
> **Enabler Type:** compliance
> **Created:** 2026-02-17
> **Due:** ---
> **Completed:** 2026-02-18
> **Parent:** FEAT-017
> **Owner:** ---
> **Effort:** 2

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Brief description and technical scope |
| [Problem Statement](#problem-statement) | Why this enabler is needed |
| [Business Value](#business-value) | How enabler supports feature delivery |
| [Technical Approach](#technical-approach) | High-level technical approach |
| [Acceptance Criteria](#acceptance-criteria) | Definition of done |
| [History](#history) | Status changes and key events |

---

## Summary

Remove or deprecate the existing installation instructions that reference shipping a private archive of the Jerry repository. These instructions no longer reflect the current distribution model and will confuse new users.

**Technical Scope:**
- Audit current INSTALLATION.md for archive-based references
- Remove or mark as deprecated all archive distribution instructions
- Ensure no dead links or broken references remain

---

## Problem Statement

The current installation instructions are "very targeted regarding shipping an archive of the private Jerry repository." This model is no longer the primary distribution method, creating confusion for users following outdated instructions.

---

## Business Value

Removes misleading instructions that cause failed installations and support requests.

### Features Unlocked

- Clean slate for modern installation instructions (EN-940, EN-941)

---

## Technical Approach

1. Audit INSTALLATION.md and README.md for archive-based references
2. Remove archive distribution sections
3. Add deprecation notice if any references must remain for backward compatibility
4. Verify no orphaned links or cross-references

---

## Acceptance Criteria

### Definition of Done

- [ ] No active archive-based installation instructions in INSTALLATION.md
- [ ] No archive-based references in README.md installation section
- [ ] All cross-references updated or removed
- [ ] No broken links introduced

**Transcript Citation:**
> "Currently they're very targeted regarding shipping an archive of the private Jerry repository."
> — SPEAKER_00, seg-008

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-02-17 | Claude | pending | Created from transcript analysis (seg-007, seg-008) |
