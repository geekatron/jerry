# EN-940: Document Collaborator-Based Installation (SSH + Marketplace)

> **Type:** enabler
> **Status:** pending
> **Priority:** high
> **Impact:** high
> **Enabler Type:** compliance
> **Created:** 2026-02-17
> **Due:** ---
> **Completed:** ---
> **Parent:** FEAT-017
> **Owner:** ---
> **Effort:** 3

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

Write new installation instructions covering the current collaborator-based access model: users are added as collaborators to the GitHub repository, then install via the Claude Code marketplace by pointing it at the repository with a valid SSH key.

**Technical Scope:**
- Document prerequisite: being added as a collaborator
- Document SSH key setup and verification
- Document Claude Code marketplace installation pointing at GitHub repository
- Include troubleshooting for common SSH/access issues

---

## Problem Statement

There are no instructions for the current primary installation method (collaborator + SSH key + Claude Code marketplace). Users granted collaborator access have no documented path to install Jerry.

---

## Business Value

Provides the primary installation path for current users, reducing onboarding friction and support requests.

### Features Unlocked

- Self-service installation for collaborators
- Reduced onboarding support burden

---

## Technical Approach

1. Create "Current Installation (Collaborator Access)" section in INSTALLATION.md
2. Document prerequisites: GitHub account, collaborator invite accepted, SSH key configured
3. Step-by-step: Add SSH key → Verify access → Claude Code marketplace → Point at repo → Install
4. Include verification steps (how to confirm successful installation)
5. Troubleshooting section for SSH and access issues

---

## Acceptance Criteria

### Definition of Done

- [ ] INSTALLATION.md has "Collaborator Installation" section
- [ ] Prerequisites clearly listed (collaborator access, SSH key)
- [ ] Step-by-step installation guide from SSH setup through marketplace install
- [ ] Verification steps included
- [ ] Troubleshooting section for common issues

**Transcript Citation:**
> "We need to update the installation instructions to reflect the current reality where people can be added as a collaborator to the repository, and then they can just install the marketplace by pointing the marketplace at the GitHub repository, assuming that they have a valid SSH key."
> — SPEAKER_00, seg-009

---

## Dependencies

### Depends On

- [EN-939](../EN-939-remove-archive-instructions/EN-939-remove-archive-instructions.md) - Archive instructions must be removed first

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-02-17 | Claude | pending | Created from transcript ACT-004 (confidence 0.97) |
