# EN-936: Update README with OSX-Primary Platform Notice

> **Type:** enabler
> **Status:** pending
> **Priority:** high
> **Impact:** high
> **Enabler Type:** compliance
> **Created:** 2026-02-17
> **Due:** ---
> **Completed:** ---
> **Parent:** FEAT-016
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

Update the project README to indicate that Jerry was primarily built for OSX and that platform portability support (namely Windows) is actively being worked on. Include guidance encouraging Windows users to file platform-specific issues.

**Technical Scope:**
- Add "Platform Support" section to README.md
- Include OSX-primary designation with Windows portability status
- Add link to issue filing guidance for Windows users

---

## Problem Statement

The README does not currently indicate the project's platform support posture. Users on Windows may encounter unexpected issues without understanding that the project is OSX-primary. This creates a poor first impression and missed opportunity to collect Windows-specific bug reports.

---

## Business Value

Sets accurate user expectations and channels Windows users toward productive issue reporting rather than silent abandonment.

### Features Unlocked

- Transparent platform support communication
- Targeted Windows issue collection pipeline

---

## Technical Approach

1. Add a "Platform Support" section to README.md (after installation, before usage)
2. Include clear OSX-primary designation
3. State that Windows portability support is in progress
4. Link to GitHub Issues with a "windows" label template

---

## Acceptance Criteria

### Definition of Done

- [ ] README.md contains "Platform Support" section
- [ ] Section clearly states OSX-primary status
- [ ] Section mentions Windows portability as in-progress
- [ ] Section encourages Windows issue filing

**Transcript Citation:**
> "one of the tasks that we need to deal with is the fact that we need to update the README to indicate that this project was primarily built for OSX and we are working on platform portability support, namely Windows."
> — SPEAKER_00, seg-002

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-02-17 | Claude | pending | Created from transcript ACT-001 (confidence 0.95) |
