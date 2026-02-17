# EN-934: Dependency License Compatibility Audit

<!--
TEMPLATE: Enabler
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.9
CREATED: 2026-02-17 (Claude)
PURPOSE: Audit all dependencies for Apache 2.0 compatibility
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
> **Effort:** 3

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

Audit all direct and transitive Python dependencies to confirm their licenses are compatible with Apache 2.0 distribution. Produce a compatibility matrix documenting each dependency's license.

---

## Problem Statement

Distributing under Apache 2.0 requires that all bundled/required dependencies use compatible licenses (Apache 2.0, MIT, BSD, ISC, etc.). GPL dependencies are incompatible and would require removal or replacement.

---

## Technical Approach

1. Extract all direct dependencies from `pyproject.toml`
2. Use `pip-licenses` or `uv run pip-audit` to enumerate dependency licenses
3. Classify each license as: Compatible (Apache/MIT/BSD/ISC/PSF), Incompatible (GPL/AGPL/LGPL), or Review Needed
4. Document results in a compatibility matrix
5. Flag any incompatible dependencies for replacement

---

## Acceptance Criteria

- [ ] All direct dependencies audited with license identified
- [ ] All transitive dependencies audited
- [ ] Compatibility matrix produced and stored in FEAT-015 directory
- [ ] Zero incompatible (copyleft) dependencies found, OR replacement plan documented
- [ ] `pip-audit` security scan still passes

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-02-17 | Created | Initial creation. Should be completed BEFORE EN-932 (source headers). |
