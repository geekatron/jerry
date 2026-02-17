# EN-933: Packaging Metadata Update

<!--
TEMPLATE: Enabler
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.9
CREATED: 2026-02-17 (Claude)
PURPOSE: Update pyproject.toml and packaging metadata for Apache 2.0
-->

> **Type:** enabler
> **Status:** done
> **Priority:** high
> **Impact:** medium
> **Enabler Type:** compliance
> **Created:** 2026-02-17
> **Due:** ---
> **Completed:** 2026-02-17
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

- [x] `pyproject.toml` license field is `"Apache-2.0"`
- [x] PyPI classifier updated to Apache Software License
- [x] No remaining MIT license references in packaging metadata
- [x] `uv sync` succeeds after changes

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-02-17 | Created | Initial creation |
| 2026-02-17 | done | pyproject.toml updated (license→Apache-2.0, classifier updated). `uv sync` PASS. MIT refs in README.md/INSTALLATION.md flagged for downstream. Artifact: `orchestration/feat015-licmig-20260217-001/lic/phase-2-core/metadata-updater/metadata-updater-output.md` |
