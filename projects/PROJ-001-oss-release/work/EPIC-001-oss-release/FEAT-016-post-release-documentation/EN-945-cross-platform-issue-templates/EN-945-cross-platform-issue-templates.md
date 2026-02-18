# EN-945: Create Cross-Platform Issue Templates (macOS & Linux)

> **Type:** enabler
> **Status:** done
> **Priority:** high
> **Impact:** high
> **Enabler Type:** compliance
> **Created:** 2026-02-18
> **Due:** ---
> **Completed:** 2026-02-18
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
| [Dependencies](#dependencies) | Dependencies and items enabled |
| [History](#history) | Status changes and key events |

---

## Summary

Expand the platform-specific issue template infrastructure to cover macOS and Linux in addition to the existing Windows template (EN-937). Each platform gets a dedicated issue template with OS-appropriate diagnostic fields, making it as easy as possible for users to file actionable compatibility reports.

**Technical Scope:**
- Create macOS compatibility issue template with macOS version, Apple Silicon/Intel chip, and Homebrew version fields
- Create Linux compatibility issue template with distro, kernel version, and package manager fields
- Update README Platform Support section to link all three templates
- Ensure consistent structure across all three platform templates

---

## Problem Statement

EN-937 created a Windows-specific issue template, but macOS and Linux users encountering platform-specific issues have no structured reporting path. Since Jerry is OSX-primary, macOS issues may surface as the project evolves. Linux users need a template tailored to their environment (distro, kernel, package manager) rather than a generic bug report.

---

## Business Value

Structured issue templates for all three platforms ensure that every compatibility report arrives with the diagnostic information needed for triage. This eliminates back-and-forth "what OS/version/shell?" exchanges and accelerates resolution.

### Features Unlocked

- Complete cross-platform issue triage pipeline
- Diagnostic data collection tailored per platform
- Lower barrier to filing issues for all users

---

## Technical Approach

1. Create `.github/ISSUE_TEMPLATE/macos-compatibility.yml` with fields: macOS version, chip (Apple Silicon/Intel), Homebrew version, shell, steps to reproduce
2. Create `.github/ISSUE_TEMPLATE/linux-compatibility.yml` with fields: distribution, kernel version, package manager, shell, steps to reproduce
3. Update README.md Platform Support section to link all three issue templates
4. Maintain consistent template structure across all three platforms (description, steps, expected/actual, additional context)

---

## Acceptance Criteria

### Definition of Done

- [x] `.github/ISSUE_TEMPLATE/macos-compatibility.yml` exists with macOS-specific fields
- [x] `.github/ISSUE_TEMPLATE/linux-compatibility.yml` exists with Linux-specific fields
- [x] README Platform Support section links to all three platform issue templates
- [x] All three templates share consistent structure (description, steps, expected, actual, additional)
- [x] Templates use appropriate GitHub issue form YAML schema

---

## Dependencies

### Depends On

- [EN-937](../EN-937-windows-issue-solicitation/EN-937-windows-issue-solicitation.md) - Windows template establishes the pattern

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-02-18 | Claude | pending | Created to expand platform issue template coverage beyond Windows (EN-937) to macOS and Linux |
| 2026-02-18 | Claude | done | Created macos-compatibility.yml (macOS version, chip, Homebrew, shell) and linux-compatibility.yml (distro, kernel, package manager, shell). README Platform Support updated to link all 3 templates. Consistent structure across all templates. |
