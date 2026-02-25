# EN-002: Document Type Ontology Hardening

<!--
TEMPLATE: Enabler
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.9
-->

> **Type:** enabler
> **Status:** completed
> **Priority:** high
> **Impact:** high
> **Enabler Type:** infrastructure
> **Created:** 2026-02-24
> **Due:** --
> **Completed:** 2026-02-24
> **Parent:** FEAT-001
> **Owner:** Claude
> **Effort:** 13

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | What this enabler delivers |
| [Problem Statement](#problem-statement) | Why the ontology needs hardening |
| [Business Value](#business-value) | What this enabler unlocks |
| [Technical Approach](#technical-approach) | Implementation strategy reference |
| [Children (Tasks)](#children-tasks) | Task breakdown |
| [Progress Summary](#progress-summary) | Overall progress |
| [Acceptance Criteria](#acceptance-criteria) | Definition of done |
| [Risks and Mitigations](#risks-and-mitigations) | Known risks |
| [Dependencies](#dependencies) | Upstream and downstream |
| [Related Items](#related-items) | Hierarchy and links |
| [History](#history) | Change log |

---

## Summary

Harden the `DocumentTypeDetector` ontology to correctly classify all markdown files in the Jerry repository. The implementation expanded the `DocumentType` enum (11 to 13 values), rewrote `PATH_PATTERNS` (12 to 65 patterns across 5 tiers), replaced the buggy `"---"` structural cue with 6 precise fingerprints, added an explicit `UNKNOWN` fallback with structured diagnostics, and built a full-repo regression test suite (5,528 parametrized tests) that runs in CI on every commit.

For detailed implementation design (path pattern registry, structural cue design, enum additions, regression test sketch), see [evidence/technical-approach.md](evidence/technical-approach.md).

---

## Problem Statement

The `DocumentTypeDetector` was designed for a repo with ~100 markdown files across 6-8 categories. The repo grew to 2,774+ files across 20+ categories, exposing three defects:

1. **Path layer gaps:** `PATH_PATTERNS` covered only ~8 of 20+ file categories, leaving ~1,634 files unmatched
2. **Structure layer defect:** The `"---"` structural cue matched every markdown file using horizontal rules, causing universal misclassification to `agent_definition` (BUG-004)
3. **No fallback strategy:** Files outside the ontology had no explicit `UNKNOWN` classification, making gaps invisible

---

## Business Value

- **Universal `detect` reliability:** Any markdown file returns a correct or intentional `UNKNOWN` classification
- **Auto-schema selection:** `jerry ast validate` can auto-select the correct schema based on detected type
- **Pre-commit hook accuracy:** Schema validation routes files to correct schemas
- **Full-repo CI gate:** Regression test catches ontology regressions on every commit

---

## Technical Approach

See [evidence/technical-approach.md](evidence/technical-approach.md) for full implementation details including file taxonomy audit, path pattern design (65 patterns across 5 tiers), structural cue design (6 precise fingerprints), UNKNOWN fallback design, and regression test sketch.

---

## Children (Tasks)

| ID | Title | Status | Effort | Owner |
|----|-------|--------|--------|-------|
| TASK-003 | Expand `DocumentType` enum with `SKILL_RESOURCE`, `TEMPLATE` values | completed | 1 | Claude |
| TASK-004 | Rewrite `PATH_PATTERNS` to cover all 20+ file categories | completed | 3 | Claude |
| TASK-005 | Replace structural cues and add `UNKNOWN` fallback with diagnostics | completed | 2 | Claude |
| TASK-006 | Build full-repo parametrized regression test (~5,500 files) | completed | 3 | Claude |
| TASK-007 | Audit and refine nav table validation for partial coverage | closed | 2 | Claude |
| TASK-008 | Full-repo validation scan: zero misclassifications, zero false warnings | completed | 2 | Claude |

---

## Progress Summary

| Metric | Value |
|--------|-------|
| **Total Tasks** | 6 |
| **Completed Tasks** | 6 |
| **Total Effort (points)** | 13 |
| **Completed Effort** | 13 |
| **Completion %** | 100% |

---

## Acceptance Criteria

- [x] `DocumentType` enum expanded to cover all file categories (`SKILL_RESOURCE`, `TEMPLATE` added)
- [x] `PATH_PATTERNS` covers all 20+ file categories (65 patterns across 5 tiers); zero misclassifications across full repo
- [x] BUG-004 fixed: `"---"` structural cue removed; no file classified as `agent_definition` via structural fallback
- [x] Full-repo regression test (5,528 parametrized tests) passes in CI on every commit
- [x] UNKNOWN fallback is explicit and intentional (`EXPECTED_UNKNOWN` allowlist: 1 entry)

---

## Risks and Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Regression test is too slow (~5,500 files) | Low | Medium | Test only calls `detect()` (path matching + string search), no full parse. Actual: ~7s. |
| New path patterns conflict with existing patterns | Low | Low | First-match-wins semantics; validated by full-repo test. |
| `EXPECTED_UNKNOWN` allowlist grows uncontrollably | Low | Low | Review in PR reviews. Target: < 20 files. |
| Adding enum values breaks schema_definitions.py | Medium | Medium | Regression test catches missing schemas. |

---

## Dependencies

### Depends On

- [BUG-004: Document type detection misclassification](../BUG-004-document-type-detection-misclassification/BUG-004-document-type-detection-misclassification.md) -- RCA findings drive the fix approach

### Enables

- Reliable `jerry ast detect` for automation across all repo files
- Auto-schema selection in `jerry ast validate`
- Pre-commit hook accuracy improvement
- CI regression gate that catches ontology gaps on new file additions

---

## Related Items

### Hierarchy

- **Parent:** [FEAT-001: AST Strategy](../FEAT-001-ast-strategy.md)
- **Parent Epic:** [EPIC-001: Markdown AST Infrastructure](../../EPIC-001-markdown-ast.md)

### Related Items

- **Related Bug:** [BUG-004: Document type detection misclassification](../BUG-004-document-type-detection-misclassification/BUG-004-document-type-detection-misclassification.md)
- **Design Document:** [evidence/technical-approach.md](evidence/technical-approach.md) -- Path pattern design, structural cue design, regression test sketch
- **Source ADR:** ADR-PROJ005-003 (Document Type Detection design decision)
- **Source File:** `src/domain/markdown_ast/document_type.py`
- **Source File:** `src/domain/markdown_ast/schema_definitions.py`

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-02-24 | Claude | pending | Enabler created from BUG-004 RCA findings. Initial scope: 4 tasks, 8 SP. |
| 2026-02-24 | Claude | pending | Scope expanded after full taxonomy audit: 2,774 files across 20+ categories. 6 tasks, 13 SP. |
| 2026-02-24 | Claude | completed | All 6 tasks completed. C4 quality gate: eng-reviewer 0.950 GO, adv-scorer 0.920 PASS. |
| 2026-02-24 | Claude | completed | Technical content extracted to evidence/technical-approach.md per content standards. AC reduced to 5 bullets. |
