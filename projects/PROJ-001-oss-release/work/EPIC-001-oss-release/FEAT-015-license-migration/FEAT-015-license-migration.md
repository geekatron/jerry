# FEAT-015: License Migration (MIT to Apache 2.0)

<!--
TEMPLATE: Feature
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.4
CREATED: 2026-02-17 (Claude)
PURPOSE: Migrate Jerry Framework license from MIT to Apache 2.0 for OSS release
-->

> **Type:** feature
> **Status:** done
> **Priority:** high
> **Impact:** high
> **Created:** 2026-02-17
> **Due:** ---
> **Completed:** 2026-02-17
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
| [EN-930](./enablers/EN-930-license-file-replacement.md) | License File Replacement | done | 1 | Claude |
| [EN-931](./enablers/EN-931-notice-file-creation.md) | NOTICE File Creation | done | 1 | Claude |
| [EN-932](./enablers/EN-932-source-file-headers.md) | Source File Header Notices | done | 5 | Claude |
| [EN-933](./enablers/EN-933-packaging-metadata-update.md) | Packaging Metadata Update | done | 1 | Claude |
| [EN-934](./enablers/EN-934-dependency-license-audit.md) | Dependency License Compatibility Audit | done | 3 | Claude |
| [EN-935](./enablers/EN-935-ci-license-validation.md) | CI License Header Validation | done | 3 | Claude |

---

## Progress Summary

```
+------------------------------------------------------------------+
|                    FEATURE PROGRESS TRACKER                       |
+------------------------------------------------------------------+
| Enablers:  [####################] 100% (6/6 completed)            |
| Effort:    [####################] 100% (14/14 points)             |
+------------------------------------------------------------------+
| Overall:   [####################] 100%                             |
+------------------------------------------------------------------+
```

### Progress Metrics

| Metric | Value |
|--------|-------|
| **Total Enablers** | 6 |
| **Completed Enablers** | 6 |
| **Total Effort** | 14 points |
| **Completed Effort** | 14 points |

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
| 2026-02-17 | Claude | in_progress | Orchestration plan created (feat015-licmig-20260217-001). Phase 1 (EN-934 audit) execution started. |
| 2026-02-17 | Claude | in_progress | Phase 1 COMPLETE. EN-934 done (QG-1 PASS 0.941). Phase 2 started: EN-930, EN-931, EN-933 in parallel. |
| 2026-02-17 | Claude | in_progress | Phase 2 COMPLETE. EN-930, EN-931, EN-933 all done. QG-2 PASS (0.9505, 2 iterations). Phase 3 unblocked. |
| 2026-02-17 | Claude | in_progress | Phase 3 COMPLETE. EN-932 done: 403 .py files have SPDX headers (17 shebangs handled). Independent verification PASS. Tests: 3196 passed. QG-3 pending. |
| 2026-02-17 | Claude | in_progress | QG-3 PASS (0.935, 2 iterations). Iteration 1 REVISE (0.873): shebang roster mismatch, missing version metadata, no criteria cross-ref. Remediated all P1 findings. Iteration 2 PASS: S-014=0.935, S-007=0.96, S-002=ACCEPT. Phase 4 unblocked. |
| 2026-02-17 | Claude | in_progress | Phase 4 COMPLETE. EN-935 done: scripts/check_spdx_headers.py, pre-commit hook (spdx-license-headers), CI job (license-headers). 5/5 tests pass, 404 files validated. QG-Final pending. |
| 2026-02-17 | Claude | in_progress | QG-Final PASS (0.9335, 2 iterations). Iter 1 REVISE: MIT refs in README/INSTALLATION, file count gap, thin Phase 2 evidence. Remediated all 5 items. Iter 2 PASS: S-014=0.9335, S-007=0.94, S-002=MARGINAL PASS. |
| 2026-02-17 | Claude | done | FEAT-015 COMPLETE. All 6 enablers done. All 4 quality gates passed. Workflow feat015-licmig-20260217-001 closed. |

---

## System Mapping

| System | Mapping |
|--------|---------|
| **Azure DevOps** | Feature |
| **SAFe** | Feature |
| **JIRA** | Story (Epic child) |
