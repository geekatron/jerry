# EN-933: Packaging Metadata Update

<!--
TEMPLATE: Enabler
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.9
CREATED: 2026-02-17 (Claude)
PURPOSE: Update pyproject.toml and packaging metadata for Apache 2.0
-->

> **Type:** enabler
> **Status:** pending
> **Priority:** high
> **Impact:** medium
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

Update `pyproject.toml` license field and any other packaging metadata to reflect Apache 2.0. Ensure PyPI classifiers and SPDX identifiers are correct.

---

## Problem Statement

The `pyproject.toml` currently declares MIT license. This must be updated to Apache-2.0 to match the actual LICENSE file.

---

## Technical Approach

1. Update `pyproject.toml` `license` field to `"Apache-2.0"` (SPDX identifier)
2. Update PyPI classifier to `"License :: OSI Approved :: Apache Software License"`
3. Check for any other files referencing "MIT" license (README, docs)
4. Update any badge URLs if present

---

## Acceptance Criteria

- [ ] `pyproject.toml` license field is `"Apache-2.0"`
- [ ] PyPI classifier updated to Apache Software License
- [ ] No remaining MIT license references in packaging metadata
- [ ] `uv sync` succeeds after changes

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-02-17 | Created | Initial creation |
