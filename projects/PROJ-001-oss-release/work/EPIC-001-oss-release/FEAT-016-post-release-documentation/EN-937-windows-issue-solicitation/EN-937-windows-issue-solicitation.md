# EN-937: Add Windows Issue Solicitation Guidance

> **Type:** enabler
> **Status:** pending
> **Priority:** medium
> **Impact:** medium
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

Create guidance and infrastructure for actively soliciting Windows-specific issue reports from users. This includes a GitHub issue template for Windows issues and documentation pointing users to it.

**Technical Scope:**
- Create GitHub issue template for Windows-specific issues
- Add CONTRIBUTING.md section on Windows issue reporting
- Reference issue template from README platform notice (EN-936)

---

## Problem Statement

Without active solicitation, Windows users who encounter issues may abandon the project silently rather than filing reports. The team needs structured issue collection to identify and prioritize Windows compatibility fixes.

---

## Business Value

Converts silent churn into actionable bug reports, enabling data-driven prioritization of Windows portability work.

### Features Unlocked

- Windows issue triage pipeline
- Data-driven platform portability roadmap

---

## Technical Approach

1. Create `.github/ISSUE_TEMPLATE/windows-compatibility.yml` issue template
2. Add "Windows Compatibility" section to CONTRIBUTING.md (or create if not exists)
3. Include fields: OS version, PowerShell version, steps to reproduce, expected vs actual behavior
4. Add "windows" label to repository

---

## Acceptance Criteria

### Definition of Done

- [ ] GitHub issue template for Windows issues exists
- [ ] CONTRIBUTING.md includes Windows issue reporting section
- [ ] "windows" label exists in GitHub repository
- [ ] README platform notice (EN-936) links to issue template

**Transcript Citation:**
> "We are actively looking for issues to be filed by Windows users so that we can try and mitigate and resolve any Windows specific issues."
> — SPEAKER_00, seg-003

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-02-17 | Claude | pending | Created from transcript ACT-002 (confidence 0.85) |
