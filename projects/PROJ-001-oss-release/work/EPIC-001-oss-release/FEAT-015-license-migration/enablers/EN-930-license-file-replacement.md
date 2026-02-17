# EN-930: License File Replacement

<!--
TEMPLATE: Enabler
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.9
CREATED: 2026-02-17 (Claude)
PURPOSE: Replace MIT LICENSE with Apache License 2.0
-->

> **Type:** enabler
> **Status:** pending
> **Priority:** high
> **Impact:** high
> **Enabler Type:** compliance
> **Created:** 2026-02-17
> **Due:** ---
> **Completed:** ---
> **Parent:** FEAT-015
> **Owner:** Claude
> **Effort:** 1

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | What this enabler delivers |
| [Problem Statement](#problem-statement) | Why this is needed |
| [Technical Approach](#technical-approach) | How to implement |
| [Acceptance Criteria](#acceptance-criteria) | Definition of done |
| [History](#history) | Status changes |

---

## Summary

Replace the current MIT License file at the repository root with the full Apache License Version 2.0 text. Update the copyright year and holder.

---

## Problem Statement

The repository currently uses MIT License. Apache 2.0 is required for OSS release to provide explicit patent grants and contribution terms.

---

## Technical Approach

1. Replace `LICENSE` file content with Apache License 2.0 full text
2. Set copyright to `2026 Adam Nowak`
3. Verify the file matches the canonical Apache 2.0 text from apache.org

---

## Acceptance Criteria

- [ ] `LICENSE` file contains complete Apache License 2.0 text
- [ ] Copyright line reads `Copyright 2026 Adam Nowak`
- [ ] File passes automated license detection (e.g., GitHub recognizes it as Apache-2.0)

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-02-17 | Created | Initial creation |
