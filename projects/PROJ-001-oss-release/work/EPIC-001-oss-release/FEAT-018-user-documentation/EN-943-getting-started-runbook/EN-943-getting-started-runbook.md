# EN-943: Create Getting-Started Runbook

> **Type:** enabler
> **Status:** pending
> **Priority:** high
> **Impact:** high
> **Enabler Type:** compliance
> **Created:** 2026-02-17
> **Due:** ---
> **Completed:** ---
> **Parent:** FEAT-018
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

Create a comprehensive getting-started runbook that guides new users from installation through first successful skill invocation. This is the primary onboarding document for Jerry users.

**Technical Scope:**
- Prerequisites and installation reference
- First session setup (project creation, JERRY_PROJECT configuration)
- First skill invocation walkthrough
- Common first-time issues and solutions

---

## Problem Statement

New users currently must piece together information from CLAUDE.md, INSTALLATION.md, and individual SKILL.md files to understand how to use Jerry. A unified getting-started guide reduces time-to-first-success dramatically.

---

## Business Value

The getting-started runbook is the single most impactful user document — it determines whether users succeed or abandon Jerry in their first session.

### Features Unlocked

- Sub-10-minute time-to-first-success for new users
- Reduced onboarding support burden

---

## Technical Approach

1. Create `docs/user-guides/getting-started.md`
2. Structure: Prerequisites → Install → Configure → First Project → First Skill → Next Steps
3. Include copy-pasteable commands for each step
4. Include "What you should see" screenshots/outputs for verification
5. End with pointers to skill playbooks (EN-944)

---

## Acceptance Criteria

### Definition of Done

- [ ] `docs/user-guides/getting-started.md` created
- [ ] Covers installation through first skill invocation
- [ ] Includes prerequisite checklist
- [ ] All commands are copy-pasteable
- [ ] Includes verification steps ("you should see...")
- [ ] Points to next resources (skill playbooks)

**Transcript Citation:**
> "For users to know how to use Jerry."
> — SPEAKER_00, seg-013

---

## Dependencies

### Depends On

- [EN-942](../EN-942-runbook-playbook-scope/EN-942-runbook-playbook-scope.md) - Scope defines document structure
- [FEAT-017](../../FEAT-017-installation-instructions/FEAT-017-installation-instructions.md) - Installation instructions must be current

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-02-17 | Claude | pending | Created from transcript analysis (ACT-005, seg-012, seg-013) |
