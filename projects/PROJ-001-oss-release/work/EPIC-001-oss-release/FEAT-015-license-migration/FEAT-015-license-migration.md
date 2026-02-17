# FEAT-015: License Migration (MIT to Apache 2.0)

<!--
TEMPLATE: Feature
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.4
CREATED: 2026-02-17 (Claude)
PURPOSE: Migrate Jerry Framework license from MIT to Apache 2.0 for OSS release
-->

> **Type:** feature
> **Status:** pending
> **Priority:** high
> **Impact:** high
> **Created:** 2026-02-17
> **Due:** ---
> **Completed:** ---
> **Parent:** EPIC-001
> **Owner:** Adam Nowak
> **Target Sprint:** ---

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Feature overview and value proposition |
| [Benefit Hypothesis](#benefit-hypothesis) | Expected benefits |
| [Acceptance Criteria](#acceptance-criteria) | Definition of done |
| [Children (Enablers)](#children-enablers) | Enabler inventory |
| [Progress Summary](#progress-summary) | Overall progress |
| [Related Items](#related-items) | Hierarchy and dependencies |
| [History](#history) | Status changes |

---

## Summary

Migrate the Jerry Framework from MIT License to Apache License 2.0. Apache 2.0 provides explicit patent grants, contribution terms, and trademark protections that MIT lacks — critical for an OSS project that may attract external contributors.

**Key Objectives:**
- Replace MIT LICENSE file with Apache 2.0
- Add Apache 2.0 boilerplate header to all Python source files
- Create NOTICE file (Apache 2.0 convention for attribution)
- Update packaging metadata (`pyproject.toml` license classifier)
- Audit all third-party dependencies for Apache 2.0 compatibility
- Add CI validation for license header compliance

---

## Benefit Hypothesis

**We believe that** migrating from MIT to Apache 2.0

**Will result in** stronger IP protection (patent grant), clearer contribution terms, and better alignment with enterprise OSS adoption requirements

**We will know we have succeeded when:**
- All source files carry Apache 2.0 headers
- NOTICE file exists with proper attribution
- All dependencies confirmed compatible with Apache 2.0
- CI enforces license headers on new files

---

## Acceptance Criteria

### Functional Criteria

- [ ] AC-1: `LICENSE` file contains full Apache License 2.0 text
- [ ] AC-2: `NOTICE` file exists with project name, copyright, and attribution
- [ ] AC-3: All `.py` files in `src/` carry Apache 2.0 boilerplate header
- [ ] AC-4: All `.py` files in `scripts/` and `hooks/` carry Apache 2.0 boilerplate header
- [ ] AC-5: `pyproject.toml` `license` field updated to `"Apache-2.0"` (SPDX identifier)
- [ ] AC-6: All direct dependencies are Apache 2.0 compatible (permissive license)
- [ ] AC-7: CI pre-commit hook validates license headers on `.py` files

### Non-Functional Criteria

- [ ] NFC-1: No test regressions introduced
- [ ] NFC-2: License header format follows SPDX standard short-form
- [ ] NFC-3: NOTICE file follows Apache Foundation conventions

---

## Children (Enablers)

| ID | Title | Status | Effort | Owner |
|----|-------|--------|--------|-------|
| [EN-930](./enablers/EN-930-license-file-replacement.md) | License File Replacement | pending | 1 | Claude |
| [EN-931](./enablers/EN-931-notice-file-creation.md) | NOTICE File Creation | pending | 1 | Claude |
| [EN-932](./enablers/EN-932-source-file-headers.md) | Source File Header Notices | pending | 5 | Claude |
| [EN-933](./enablers/EN-933-packaging-metadata-update.md) | Packaging Metadata Update | pending | 1 | Claude |
| [EN-934](./enablers/EN-934-dependency-license-audit.md) | Dependency License Compatibility Audit | pending | 3 | Claude |
| [EN-935](./enablers/EN-935-ci-license-validation.md) | CI License Header Validation | pending | 3 | Claude |

---

## Progress Summary

```
+------------------------------------------------------------------+
|                    FEATURE PROGRESS TRACKER                       |
+------------------------------------------------------------------+
| Enablers:  [....................] 0% (0/6 completed)              |
| Effort:    [....................] 0% (0/14 points)                |
+------------------------------------------------------------------+
| Overall:   [....................] 0%                               |
+------------------------------------------------------------------+
```

### Progress Metrics

| Metric | Value |
|--------|-------|
| **Total Enablers** | 6 |
| **Completed Enablers** | 0 |
| **Total Effort** | 14 points |
| **Completed Effort** | 0 points |

---

## Related Items

### Hierarchy

- **Parent:** [EPIC-001: OSS Release Preparation](../EPIC-001-oss-release.md)

### Dependencies

| Dependency Type | Item | Description |
|----------------|------|-------------|
| Depends On | EN-934 (audit) | Source headers (EN-932) should only be applied after confirming all deps are compatible |

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-02-17 | Claude | pending | Feature created. 6 enablers, 14 effort points. Migrating from MIT to Apache 2.0 for OSS release. |

---

## System Mapping

| System | Mapping |
|--------|---------|
| **Azure DevOps** | Feature |
| **SAFe** | Feature |
| **JIRA** | Story (Epic child) |
