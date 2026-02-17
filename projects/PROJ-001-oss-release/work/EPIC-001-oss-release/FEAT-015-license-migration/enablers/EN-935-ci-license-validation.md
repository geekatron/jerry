# EN-935: CI License Header Validation

<!--
TEMPLATE: Enabler
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.9
CREATED: 2026-02-17 (Claude)
PURPOSE: Add CI/pre-commit check for Apache 2.0 license headers
-->

> **Type:** enabler
> **Status:** pending
> **Priority:** medium
> **Impact:** medium
> **Enabler Type:** infrastructure
> **Created:** 2026-02-17
> **Due:** ---
> **Completed:** ---
> **Parent:** FEAT-015
> **Owner:** Claude
> **Effort:** 3

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | What this enabler delivers |
| [Problem Statement](#problem-statement) | Why this is needed |
| [Technical Approach](#technical-approach) | How to implement |
| [Acceptance Criteria](#acceptance-criteria) | Definition of done |
| [Dependencies](#dependencies) | Must complete after EN-932 |
| [History](#history) | Status changes |

---

## Summary

Add a pre-commit hook and CI check that validates all `.py` files contain the Apache 2.0 SPDX license header. This prevents future files from being committed without headers.

---

## Problem Statement

Without automated enforcement, new Python files will be added without license headers, eroding compliance over time. A CI gate prevents this.

---

## Technical Approach

1. Add a pre-commit hook using `insert-license` or custom script
2. Hook checks for `SPDX-License-Identifier: Apache-2.0` in all `.py` files
3. Add equivalent check to `.github/workflows/ci.yml`
4. Allow exceptions for empty `__init__.py` files (0 bytes)
5. Verify hook works on both new and modified files

---

## Acceptance Criteria

- [ ] Pre-commit hook checks license headers on all `.py` files
- [ ] CI workflow includes license header validation step
- [ ] New `.py` files without headers are rejected by pre-commit
- [ ] Empty `__init__.py` files are excluded from the check
- [ ] All existing files pass the check (EN-932 prerequisite)

---

## Dependencies

| Dependency Type | Item | Description |
|----------------|------|-------------|
| Depends On | EN-932 | All source files must have headers before CI check is enabled |

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-02-17 | Created | Initial creation. Depends on EN-932 (source file headers). |
