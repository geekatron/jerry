# EN-001: Fix Plugin Validation

> **Type:** enabler
> **Status:** pending
> **Priority:** high
> **Impact:** high
> **Enabler Type:** infrastructure
> **Created:** 2026-02-10
> **Due:** —
> **Completed:** —
> **Parent:** FEAT-001
> **Owner:** —
> **Effort:** —

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Brief description and technical scope |
| [Problem Statement](#problem-statement) | Why this enabler is needed |
| [Business Value](#business-value) | How enabler supports feature delivery |
| [Technical Approach](#technical-approach) | High-level technical approach |
| [Tasks](#tasks) | Task inventory (children of BUG-001) |
| [Bugs](#bugs) | Bugs addressed by this enabler |
| [Decisions](#decisions) | Decisions made in this enabler |
| [Progress Summary](#progress-summary) | Overall enabler progress |
| [Acceptance Criteria](#acceptance-criteria) | Definition of done |
| [Related Items](#related-items) | Hierarchy and related work |
| [History](#history) | Status changes and key events |

---

## Summary

Fix the Plugin Validation CI check which fails because `marketplace.schema.json` is missing the `keywords` property in plugin item definitions. Also apply the Draft202012Validator best practice to all validation call sites.

**Technical Scope:**
- Add `keywords` property to marketplace plugin item schema
- Add validation tests for plugin manifests
- Apply Draft202012Validator as best practice

---

## Problem Statement

The Plugin Validation CI job fails on every push with: `Additional properties are not allowed ('keywords' was unexpected)` for `marketplace.json`. The marketplace schema does not define `keywords` in plugin item properties, but the manifest correctly includes it. This blocks PR #6 from merging.

---

## Business Value

Unblocks the Plugin Validation CI check, which is one of the 5 failing CI categories preventing PR #6 merge to main.

### Features Unlocked

- PR #6 merge to main (contributes to FEAT-001 completion)
- Clean CI baseline for OSS release

---

## Technical Approach

1. **TASK-001 (root cause fix):** Add `keywords` to `schemas/marketplace.schema.json` plugin item properties, matching the existing `keywords` definition in `schemas/plugin.schema.json`
2. **TASK-002 (tests):** Add tests verifying keywords accepted, unknown properties rejected, all manifests pass
3. **TASK-003 (best practice):** Specify `cls=jsonschema.Draft202012Validator` at all 3 `jsonschema.validate()` call sites

---

## Tasks

> Tasks are children of [BUG-001](./BUG-001-marketplace-manifest-schema-error.md) and listed here for enabler-level visibility.

| ID | Title | Status | Priority | Parent | Owner |
|----|-------|--------|----------|--------|-------|
| [TASK-001](./TASK-001-add-keywords-to-marketplace-schema.md) | Add `keywords` property to marketplace plugin item schema | BACKLOG | HIGH | BUG-001 | — |
| [TASK-002](./TASK-002-add-validation-tests.md) | Add tests for plugin manifest validation | BACKLOG | HIGH | BUG-001 | — |
| [TASK-003](./TASK-003-specify-validator-class.md) | Specify Draft202012Validator in validation script | BACKLOG | MEDIUM | BUG-001 | — |

---

## Bugs

| ID | Title | Status | Priority |
|----|-------|--------|----------|
| [BUG-001](./BUG-001-marketplace-manifest-schema-error.md) | Marketplace manifest schema error: `keywords` not allowed | in_progress | high |

---

## Decisions

| ID | Title | Status |
|----|-------|--------|
| [DEC-001](./DEC-001-json-schema-validator-class.md) | JSON Schema Validator Class Selection | ACCEPTED |

---

## Progress Summary

### Status Overview

```
+------------------------------------------------------------------+
|                   ENABLER PROGRESS TRACKER                        |
+------------------------------------------------------------------+
| Tasks:     [....................] 0% (0/3 completed)              |
+------------------------------------------------------------------+
| Overall:   [....................] 0%                               |
+------------------------------------------------------------------+
```

### Progress Metrics

| Metric | Value |
|--------|-------|
| **Total Tasks** | 3 |
| **Completed Tasks** | 0 |
| **Completion %** | 0% |

---

## Acceptance Criteria

### Definition of Done

- [ ] `keywords` property added to marketplace plugin item schema (TASK-001)
- [ ] Validation tests pass (TASK-002)
- [ ] Draft202012Validator specified at all call sites (TASK-003)
- [ ] `uv run python scripts/validate_plugin_manifests.py` passes locally (all 3 manifests)
- [ ] Plugin Validation CI check passes

---

## Evidence

### Deliverables

| Deliverable | Type | Link |
|-------------|------|------|
| Updated marketplace schema | Code | `schemas/marketplace.schema.json` (TASK-001) |
| Validation tests | Code | TBD (TASK-002) |
| Updated validation script | Code | `scripts/validate_plugin_manifests.py` (TASK-003) |

### Verification

- [ ] `uv run python scripts/validate_plugin_manifests.py` passes all 3 manifests
- [ ] Plugin Validation CI check passes
- [ ] `uv run pytest` includes new validation tests

---

## Related Items

### Hierarchy

- **Parent:** [FEAT-001: Fix CI Build Failures](../FEAT-001-fix-ci-build-failures.md)

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-02-10 | Claude | in_progress | Enabler created from FEAT-001 restructure. Groups BUG-001, 3 tasks, and DEC-001. |
| 2026-02-10 | Claude | pending | Status corrected: no task work started yet. Tasks clarified as BUG-001 children (EN-001 references for visibility). Evidence section added. |
