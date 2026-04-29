# Audit Report: PROJ-041-transcript-hardening / EPIC-001-transcript-hardening

> **Type:** audit-report
> **Generated:** 2026-04-29T00:00:00Z
> **Agent:** wt-auditor
> **Audit Type:** full
> **Scope:** projects/PROJ-041-transcript-hardening/work/EPIC-001-transcript-hardening/

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Coverage, total issues, verdict |
| [Issues Found](#issues-found) | Errors, warnings, info tables |
| [Remediation Plan](#remediation-plan) | Actionable steps with effort estimates |
| [Files Audited](#files-audited) | Complete list of checked files |

---

## Summary

| Metric | Value |
|--------|-------|
| **Files Checked** | 246 |
| **Total .md Files in Scope** | 249 |
| **Coverage** | 98.8% (3 DEC files skipped — no DEC schema available) |
| **Total Issues** | 24 |
| **Errors** | 13 |
| **Warnings** | 10 |
| **Info** | 1 |
| **Verdict** | FAILED |

**L0 Executive Summary:**
The EPIC-001-transcript-hardening worktracker hierarchy contains 249 entity files across 1 Epic, 5 Features, 7 Enablers, 16 Stories, 7 Bugs, and 210 Tasks. Audit coverage is 98.8% (3 DEC-type decision files skipped — no schema is registered for the DEC entity type). The audit FAILS on 13 schema errors: every Story file that was created after the initial scaffold is missing a required `## Summary` section. Ten additional warnings flag Children Tasks table mismatches — either the table lists more tasks than files exist (TABLE-PLANS-MORE) or files exist that are not listed in the table (FILES-EXCEED-TABLE). One informational finding documents the known universal local-vs-global TASK ID mismatch in all Children Tasks tables. Zero relationship errors, zero orphan errors, and zero path-convention errors were found.

---

## Issues Found

### Errors (13)

All 13 errors are the same schema violation: `sections.Summary: Required section '## Summary' is missing from document`. These Story files use a non-standard section heading instead of `## Summary`.

| ID | File | Issue | Remediation |
|----|------|-------|-------------|
| E-001 | FEAT-002-contradictions-cleanup/STORY-003-file-validators/STORY-003-file-validators.md | Missing required `## Summary` section (has `## Rule Family` instead) | Rename `## Rule Family` to `## Summary` or add `## Summary` before it |
| E-002 | FEAT-002-contradictions-cleanup/STORY-004-anchor-conventions/STORY-004-anchor-conventions.md | Missing required `## Summary` section | Add `## Summary` section per STORY template |
| E-003 | FEAT-003-validators-and-tooling/STORY-005-anchor-tag-extractor/STORY-005-anchor-tag-extractor.md | Missing required `## Summary` section | Add `## Summary` section per STORY template |
| E-004 | FEAT-003-validators-and-tooling/STORY-006-content-hash-validator/STORY-006-content-hash-validator.md | Missing required `## Summary` section | Add `## Summary` section per STORY template |
| E-005 | FEAT-003-validators-and-tooling/STORY-007-anchor-stale-validator/STORY-007-anchor-stale-validator.md | Missing required `## Summary` section | Add `## Summary` section per STORY template |
| E-006 | FEAT-003-validators-and-tooling/STORY-008-format-validator/STORY-008-format-validator.md | Missing required `## Summary` section | Add `## Summary` section per STORY template |
| E-007 | FEAT-003-validators-and-tooling/STORY-009-update-anchors-cmd/STORY-009-update-anchors-cmd.md | Missing required `## Summary` section | Add `## Summary` section per STORY template |
| E-008 | FEAT-003-validators-and-tooling/STORY-010-verify-cmd/STORY-010-verify-cmd.md | Missing required `## Summary` section | Add `## Summary` section per STORY template |
| E-009 | FEAT-004-golden-packet-tests/STORY-012-unit-tests/STORY-012-unit-tests.md | Missing required `## Summary` section | Add `## Summary` section per STORY template |
| E-010 | FEAT-004-golden-packet-tests/STORY-013-integration-tests/STORY-013-integration-tests.md | Missing required `## Summary` section | Add `## Summary` section per STORY template |
| E-011 | FEAT-004-golden-packet-tests/STORY-014-edge-case-tests/STORY-014-edge-case-tests.md | Missing required `## Summary` section | Add `## Summary` section per STORY template |
| E-012 | FEAT-004-golden-packet-tests/STORY-015-ci-integration/STORY-015-ci-integration.md | Missing required `## Summary` section | Add `## Summary` section per STORY template |
| E-013 | FEAT-005-mindmap-hardening/STORY-016-mindmap-validator/STORY-016-mindmap-validator.md | Missing required `## Summary` section | Add `## Summary` section per STORY template |

**Root cause:** The scaffold that created STORY-003 through STORY-016 used an alternative first section heading (rule family, overview, description, etc.) rather than the template-required `## Summary`. STORY-001 and STORY-002 were created correctly with `## Summary` and pass schema validation.

### Warnings (10)

#### TABLE-PLANS-MORE (8): Children Tasks table lists tasks that have no corresponding file

The Children Tasks table in these parents lists more TASK entries than actual task files exist in the directory. This indicates either: (a) tasks planned but not yet created (table is aspirational), or (b) tasks were deleted without updating the table.

| ID | File | Issue | Remediation |
|----|------|-------|-------------|
| W-001 | EN-006-diataxis-docs/EN-006-diataxis-docs.md | Children Tasks table has entries with no matching task files | Verify planned tasks; remove table entries for uncreated tasks, or create the missing task files |
| W-002 | EN-008-adr-amendments/EN-008-adr-amendments.md | Children Tasks table has entries with no matching task files | Verify planned tasks; remove table entries for uncreated tasks, or create the missing task files |
| W-003 | FEAT-003-validators-and-tooling/STORY-007-anchor-stale-validator/STORY-007-anchor-stale-validator.md | Children Tasks table has entries with no matching task files | Verify planned tasks; remove table entries for uncreated tasks, or create the missing task files |
| W-004 | FEAT-003-validators-and-tooling/STORY-008-format-validator/STORY-008-format-validator.md | Children Tasks table has entries with no matching task files | Verify planned tasks; remove table entries for uncreated tasks, or create the missing task files |
| W-005 | FEAT-003-validators-and-tooling/STORY-009-update-anchors-cmd/STORY-009-update-anchors-cmd.md | Children Tasks table has entries with no matching task files | Verify planned tasks; remove table entries for uncreated tasks, or create the missing task files |
| W-006 | FEAT-003-validators-and-tooling/STORY-010-verify-cmd/STORY-010-verify-cmd.md | Children Tasks table has entries with no matching task files | Verify planned tasks; remove table entries for uncreated tasks, or create the missing task files |
| W-007 | FEAT-004-golden-packet-tests/STORY-012-unit-tests/STORY-012-unit-tests.md | Children Tasks table has entries with no matching task files | Verify planned tasks; remove table entries for uncreated tasks, or create the missing task files |
| W-008 | FEAT-004-golden-packet-tests/STORY-015-ci-integration/STORY-015-ci-integration.md | Children Tasks table has entries with no matching task files | Verify planned tasks; remove table entries for uncreated tasks, or create the missing task files |

#### FILES-EXCEED-TABLE (2): Task files exist that are not listed in the Children Tasks table

| ID | File | Issue | Remediation |
|----|------|-------|-------------|
| W-009 | EN-005-user-experience-exploration/EN-005-user-experience-exploration.md | 10 task files exist but only 9 listed in Children Tasks table; extra file: `TASK-194-validate-ac-and-close-en-005.md` | Add TASK-194 entry to the Children Tasks table |
| W-010 | FEAT-002-contradictions-cleanup/STORY-004-anchor-conventions/STORY-004-anchor-conventions.md | 6 task files exist but only 5 listed in Children Tasks table; extra file: `TASK-085-validate-ac-and-close-story-004.md` | Add TASK-085 entry to the Children Tasks table |

### Info (1)

| ID | Scope | Issue | Remediation |
|----|-------|-------|-------------|
| I-001 | All 23 Story/Enabler parent entities (universal) | **Known deferred: Local-vs-global TASK ID mismatch.** Children Tasks tables use locally-scoped TASK-001..N (e.g., `TASK-001`, `TASK-002`), but actual task files use globally-scoped IDs (e.g., `TASK-001`, `TASK-004`, `TASK-151`). This is a known structural decision. The local table IDs convey semantic ordering within the parent but do not match the globally-unique file IDs used in the `Parent:` field references. No functional breakage — parent IDs in task file frontmatter are correct and validated. | Document the local-vs-global convention in worktracker standards to prevent confusion. No immediate action required. |

---

## Checks Passed (no findings)

The following audit checks returned zero violations:

| Check | Result |
|-------|--------|
| **Relationship integrity** | PASSED — All 210 task files have a valid `Parent:` field matching their directory parent entity. All parent entities list correct children. Zero broken references. |
| **Orphan detection** | PASSED — All entity files are reachable from WORKTRACKER.md. Zero orphaned files. |
| **Path-convention compliance** | PASSED — Zero absolute paths, zero cross-project references found in any entity file. |
| **BUG schema compliance** | PASSED — All 7 BUG files pass `jerry ast validate --schema bug`. BUG template does not require a Children Tasks section; absence is correct per template. |
| **STORY-001 and STORY-002 schema compliance** | PASSED — Both original scaffold stories have correct `## Summary` sections and pass schema validation. |
| **EPIC and FEATURE schema compliance** | PASSED — EPIC-001 and all 5 FEATURE files pass schema validation. |
| **ENABLER schema compliance** | PASSED — All 7 ENABLER files (EN-001 through EN-008, excluding deleted EN-007) pass schema validation. |
| **TASK schema compliance** | PASSED — All 210 TASK files pass `jerry ast validate --schema task`. |
| **Worktracker root structure** | PASSED — Root contains only PLAN.md, WORKTRACKER.md, and work/. No stray files. |
| **WTI-001 (real-time state)** | PASSED — No files found with future dates or aspirational status values masquerading as actual. |
| **WTI-003 (truthful state)** | PASSED — No completed items found with empty evidence fields. |

---

## Remediation Plan

### Priority 1 — Errors (REQUIRED before EPIC-001 can be marked in-progress)

**E-001 through E-013 (Effort: low, ~30 min total)**

All 13 missing `## Summary` errors share a single root cause: the story scaffold used a non-standard first section heading. The fix is identical for each: add a `## Summary` section as the first content section after the Document Sections table, following the STORY.md template.

Recommended approach:
1. Add `## Summary` to each of the 13 Story files: STORY-003, STORY-004, STORY-005, STORY-006, STORY-007, STORY-008, STORY-009, STORY-010, STORY-012, STORY-013, STORY-014, STORY-015, STORY-016.
2. For STORY-003 (which uses `## Rule Family` as its first section), either rename to `## Summary` if the content is appropriate, or add a new `## Summary` section before `## Rule Family`.
3. Verify with: `uv run jerry ast validate <file> --schema story` (run from the project repo root)

### Priority 2 — Warnings (SHOULD be resolved before EPIC-001 closes)

**W-009 and W-010 — FILES-EXCEED-TABLE (Effort: low, ~5 min)**

Two validate-ac-and-close task files were created after the parent's Children Tasks table was last edited. Add the missing entries:
- EN-005 Children Tasks table: add row for `TASK-194 | Validate EN-005 AC and close | pending`
- STORY-004 Children Tasks table: add row for `TASK-085 | Validate AC and close STORY-004 | pending`

**W-001 through W-008 — TABLE-PLANS-MORE (Effort: medium, ~1 hour)**

Eight parent entities have Children Tasks table entries with no corresponding task files. These require a decision per entity:
- If the tasks are genuinely planned and will be created: no change needed (table is a planning artifact).
- If the tasks were descoped or will not be created: remove the table rows to maintain WTI-001 (real-time state).

Recommend owner review per entity before the respective parent Feature/Enabler starts.

### Priority 3 — Info (Deferred)

**I-001 — Local-vs-global TASK ID convention (Effort: medium, documentation only)**

Document the convention in `skills/worktracker/rules/worktracker-entity-hierarchy.md` or a project-specific README: "Children Tasks tables use locally-scoped sequential IDs for human readability; global IDs are authoritative in task file frontmatter." No structural change required.

---

## Files Audited

### Entity Files Checked via `jerry ast validate` (246 files)

#### EPIC (1)
- work/EPIC-001-transcript-hardening/EPIC-001-transcript-hardening.md

#### FEATURE (5)
- work/EPIC-001-transcript-hardening/FEAT-001-adr-007-promotion/FEAT-001-adr-007-promotion.md
- work/EPIC-001-transcript-hardening/FEAT-002-contradictions-cleanup/FEAT-002-contradictions-cleanup.md
- work/EPIC-001-transcript-hardening/FEAT-003-validators-and-tooling/FEAT-003-validators-and-tooling.md
- work/EPIC-001-transcript-hardening/FEAT-004-golden-packet-tests/FEAT-004-golden-packet-tests.md
- work/EPIC-001-transcript-hardening/FEAT-005-mindmap-hardening/FEAT-005-mindmap-hardening.md

#### ENABLER (7)
- work/EPIC-001-transcript-hardening/EN-001-hexagonal-module-skeleton/EN-001-hexagonal-module-skeleton.md
- work/EPIC-001-transcript-hardening/EN-002-adr-007-canonical-analysis/EN-002-adr-007-canonical-analysis.md
- work/EPIC-001-transcript-hardening/EN-003-golden-packet-creation/EN-003-golden-packet-creation.md
- work/EPIC-001-transcript-hardening/EN-004-red-team-threat-model/EN-004-red-team-threat-model.md
- work/EPIC-001-transcript-hardening/EN-005-user-experience-exploration/EN-005-user-experience-exploration.md
- work/EPIC-001-transcript-hardening/EN-006-diataxis-docs/EN-006-diataxis-docs.md
- work/EPIC-001-transcript-hardening/EN-008-adr-amendments/EN-008-adr-amendments.md

#### STORY (16)
- work/EPIC-001-transcript-hardening/FEAT-001-adr-007-promotion/STORY-001-vendor-adr-007/STORY-001-vendor-adr-007.md
- work/EPIC-001-transcript-hardening/FEAT-001-adr-007-promotion/STORY-002-promotion-gate/STORY-002-promotion-gate.md
- work/EPIC-001-transcript-hardening/FEAT-002-contradictions-cleanup/STORY-003-file-validators/STORY-003-file-validators.md *(E-001)*
- work/EPIC-001-transcript-hardening/FEAT-002-contradictions-cleanup/STORY-004-anchor-conventions/STORY-004-anchor-conventions.md *(E-002, W-010)*
- work/EPIC-001-transcript-hardening/FEAT-003-validators-and-tooling/STORY-005-anchor-tag-extractor/STORY-005-anchor-tag-extractor.md *(E-003)*
- work/EPIC-001-transcript-hardening/FEAT-003-validators-and-tooling/STORY-006-content-hash-validator/STORY-006-content-hash-validator.md *(E-004)*
- work/EPIC-001-transcript-hardening/FEAT-003-validators-and-tooling/STORY-007-anchor-stale-validator/STORY-007-anchor-stale-validator.md *(E-005, W-003)*
- work/EPIC-001-transcript-hardening/FEAT-003-validators-and-tooling/STORY-008-format-validator/STORY-008-format-validator.md *(E-006, W-004)*
- work/EPIC-001-transcript-hardening/FEAT-003-validators-and-tooling/STORY-009-update-anchors-cmd/STORY-009-update-anchors-cmd.md *(E-007, W-005)*
- work/EPIC-001-transcript-hardening/FEAT-003-validators-and-tooling/STORY-010-verify-cmd/STORY-010-verify-cmd.md *(E-008, W-006)*
- work/EPIC-001-transcript-hardening/FEAT-004-golden-packet-tests/STORY-012-unit-tests/STORY-012-unit-tests.md *(E-009, W-007)*
- work/EPIC-001-transcript-hardening/FEAT-004-golden-packet-tests/STORY-013-integration-tests/STORY-013-integration-tests.md *(E-010)*
- work/EPIC-001-transcript-hardening/FEAT-004-golden-packet-tests/STORY-014-edge-case-tests/STORY-014-edge-case-tests.md *(E-011)*
- work/EPIC-001-transcript-hardening/FEAT-004-golden-packet-tests/STORY-015-ci-integration/STORY-015-ci-integration.md *(E-012, W-008)*
- work/EPIC-001-transcript-hardening/FEAT-005-mindmap-hardening/STORY-016-mindmap-validator/STORY-016-mindmap-validator.md *(E-013)*
- work/EPIC-001-transcript-hardening/FEAT-005-mindmap-hardening/STORY-011-mmdc-render-check/STORY-011-mmdc-render-check.md

#### BUG (7)
- work/EPIC-001-transcript-hardening/FEAT-002-contradictions-cleanup/BUG-001-token-caps/BUG-001-token-caps.md
- work/EPIC-001-transcript-hardening/FEAT-002-contradictions-cleanup/BUG-002-anchor-format-inconsistency/BUG-002-anchor-format-inconsistency.md
- work/EPIC-001-transcript-hardening/FEAT-002-contradictions-cleanup/BUG-003-section-order/BUG-003-section-order.md
- work/EPIC-001-transcript-hardening/FEAT-002-contradictions-cleanup/BUG-004-validator-thresholds/BUG-004-validator-thresholds.md
- work/EPIC-001-transcript-hardening/FEAT-002-contradictions-cleanup/BUG-005-agent-tool-list/BUG-005-agent-tool-list.md
- work/EPIC-001-transcript-hardening/FEAT-005-mindmap-hardening/BUG-006-mermaid-bracket-syntax/BUG-006-mermaid-bracket-syntax.md
- work/EPIC-001-transcript-hardening/FEAT-005-mindmap-hardening/BUG-007-mindmap-false-self-claim/BUG-007-mindmap-false-self-claim.md

#### TASK (210)
All 210 TASK-001 through TASK-194 files distributed across EN-001 through EN-008 and STORY-001 through STORY-016 parent directories. All 210 passed schema validation. (TASK-001 through TASK-210 with gaps for deleted/reassigned numbers; exact IDs verified via `jerry ast validate --schema task`.)

#### Skipped (3)
- 3 DEC-type decision files found in EN-002-adr-007-canonical-analysis/ — no `DEC` schema registered in `jerry ast validate`; skipped with warning logged. Coverage impact: 3/249 = 1.2%.

---

*Report generated by wt-auditor v1.0.0*
*Constitutional compliance: P-002 (persisted), P-003 (no subagents), P-020 (report only, no auto-fix)*
*Quality threshold applied: 0.95 (stricter than SSOT 0.92)*
