# EN-932: Source File Header Notices

<!--
TEMPLATE: Enabler
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.9
CREATED: 2026-02-17 (Claude)
PURPOSE: Add Apache 2.0 boilerplate header to all Python source files
-->

> **Type:** enabler
> **Status:** done
> **Priority:** high
> **Impact:** high
> **Enabler Type:** compliance
> **Created:** 2026-02-17
> **Due:** ---
> **Completed:** 2026-02-17
> **Parent:** FEAT-015
> **Owner:** Claude
> **Effort:** 5

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | What this enabler delivers |
| [Problem Statement](#problem-statement) | Why this is needed |
| [Technical Approach](#technical-approach) | How to implement |
| [Acceptance Criteria](#acceptance-criteria) | Definition of done |
| [Risks and Mitigations](#risks-and-mitigations) | Known risks |
| [History](#history) | Status changes |

---

## Summary

Add the Apache 2.0 SPDX short-form boilerplate header to all Python source files across `src/`, `scripts/`, `hooks/`, and `tests/`. This is required by Apache 2.0 Section 4(b) to include a prominent notice in each modified file.

---

## Problem Statement

Apache 2.0 requires license notices in source files. No Python files currently have license headers. This must be applied consistently across the entire codebase.

---

## Technical Approach

1. Define the standard SPDX short-form header:
   ```python
   # Copyright 2026 Adam Nowak
   # SPDX-License-Identifier: Apache-2.0
   ```
2. Create a script to add headers to all `.py` files that don't already have them
3. Apply to: `src/**/*.py`, `scripts/**/*.py`, `hooks/**/*.py`, `tests/**/*.py`
4. Skip `__init__.py` files that are empty (0 bytes)
5. Verify no files are missed

---

## Acceptance Criteria

- [x] All `.py` files in `src/` have Apache 2.0 SPDX header (191 files)
- [x] All `.py` files in `scripts/` have Apache 2.0 SPDX header (19 files)
- [x] All `.py` files in `hooks/` have Apache 2.0 SPDX header (1 file)
- [x] All `.py` files in `tests/` have Apache 2.0 SPDX header (192 files)
- [x] Header uses SPDX short-form identifier (`Apache-2.0`)
- [x] No test regressions from header addition (3196 passed, 0 failed)

---

## Risks and Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Header breaks shebang lines | Medium | High | Insert header after shebang, not before |
| Large number of files to modify | High | Low | Script-based approach for consistency |

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-02-17 | Created | Initial creation. Highest effort enabler (5 pts) due to file count. |
| 2026-02-17 | done | Applied SPDX headers to 403 .py files via scripts/apply_spdx_headers.py. 17 shebang files handled correctly. Independent verification (header-verifier) confirmed 403/403 pass all 5 criteria. Test suite: 3196 passed, 0 failed. |
