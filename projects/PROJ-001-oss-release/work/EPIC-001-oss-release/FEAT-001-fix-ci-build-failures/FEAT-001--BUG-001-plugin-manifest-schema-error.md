# BUG-001: Marketplace manifest schema error — `keywords` not allowed

> **Type:** bug
> **Status:** in_progress
> **Priority:** high
> **Impact:** high
> **Severity:** major
> **Created:** 2026-02-10
> **Due:** —
> **Completed:** —
> **Parent:** FEAT-001
> **Owner:** —
> **Found In:** PR #6
> **Fix Version:** —

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Brief description and key details |
| [Reproduction Steps](#reproduction-steps) | Steps to reproduce the issue |
| [Environment](#environment) | Environment where bug occurs |
| [Root Cause Analysis](#root-cause-analysis) | Investigation and root cause |
| [Acceptance Criteria](#acceptance-criteria) | Conditions for bug to be fixed |
| [Related Items](#related-items) | Hierarchy and related items |
| [History](#history) | Status changes |

---

## Summary

The Plugin Validation CI check fails with schema validation error: `Additional properties are not allowed ('keywords' was unexpected)`. The **marketplace manifest** (`.claude-plugin/marketplace.json`) contains a `keywords` field in a plugin item that is not defined in the marketplace plugin item schema.

**Key Details:**
- **Symptom:** Plugin Validation CI check fails with schema error on `marketplace.json`
- **Frequency:** Every CI run (100%)
- **Workaround:** None — blocks CI
- **Note:** `plugin.json` passes validation (it has `keywords` defined in its schema). Only `marketplace.json` fails.

---

## Reproduction Steps

### Steps to Reproduce

1. Push any commit to PR #6
2. CI triggers Plugin Validation job
3. Plugin validation runs schema check on manifest

### Expected Result

Plugin validation passes.

### Actual Result

```
Error: Schema validation failed: Additional properties are not allowed ('keywords' was unexpected)
Some validations failed.
```

---

## Environment

| Attribute | Value |
|-----------|-------|
| **Operating System** | Ubuntu 24.04 (GitHub Actions) |
| **Runtime** | Python 3.14 / uv 0.10.2 |
| **CI Job** | Plugin Validation |

---

## Root Cause Analysis

### Investigation Summary

**CORRECTED (2026-02-10):** Initial investigation incorrectly identified a JSON Schema draft mismatch as the root cause. Local verification disproved this:

1. `plugin.json` passes validation with BOTH default and Draft202012 validators — **no issue**
2. `marketplace.json` fails with BOTH default and Draft202012 validators — the `keywords` property is **genuinely missing from the schema**
3. `schemas/marketplace.schema.json` plugin item properties (line 52-93): `name`, `description`, `source`, `version`, `category`, `author` — **no `keywords`**
4. `.claude-plugin/marketplace.json` plugin item (line 16): `"keywords": [...]` — **present in data, absent from schema**
5. With `"additionalProperties": false` (line 95), `keywords` is correctly rejected

**Verification commands run:**
```bash
# Both produce FAIL for marketplace.json
uv run python scripts/validate_plugin_manifests.py
uv run python -c "import json, jsonschema; ..."  # tested with explicit Draft202012Validator
```

### Root Cause

**Missing property in marketplace schema.** The `schemas/marketplace.schema.json` does not define `keywords` in the plugin item properties (lines 52-93), but `.claude-plugin/marketplace.json` includes `keywords` in a plugin item (line 16). With `"additionalProperties": false`, the validator correctly rejects it.

The Draft 2020-12 mismatch identified in the initial analysis was a **red herring** — `properties` and `additionalProperties` behave identically in Draft 4/7 and Draft 2020-12 for basic use cases.

### Contributing Factors

- Schema was authored without `keywords` in the plugin item definition
- `plugin.schema.json` correctly includes `keywords` but `marketplace.schema.json` does not (inconsistency)
- Initial investigation mistakenly attributed the failure to a JSON Schema draft mismatch

### Previous Incorrect Analysis (Superseded)

The original analysis concluded the issue was a JSON Schema draft mismatch requiring `cls=jsonschema.Draft202012Validator`. This was disproved by local testing showing the same failure with both the default validator and the explicit Draft202012Validator. DEC-001 remains valid as a best practice but is not the root cause fix.

---

## Children (Tasks)

| ID | Title | Status | Priority |
|----|-------|--------|----------|
| [TASK-001](./BUG-001--TASK-001-add-keywords-to-marketplace-schema.md) | Add `keywords` property to marketplace plugin item schema | BACKLOG | HIGH |
| [TASK-002](./BUG-001--TASK-002-add-validation-tests.md) | Add tests for plugin manifest validation | BACKLOG | HIGH |
| [TASK-003](./BUG-001--TASK-003-specify-validator-class.md) | Specify Draft202012Validator in validation script (best practice) | BACKLOG | MEDIUM |

---

## Acceptance Criteria

### Fix Verification

- [ ] `keywords` property added to marketplace plugin item schema (TASK-001)
- [ ] Tests verify `keywords` is accepted and unknown properties rejected (TASK-002)
- [ ] `jsonschema.validate()` calls specify `cls=jsonschema.Draft202012Validator` as best practice (TASK-003)
- [ ] `uv run python scripts/validate_plugin_manifests.py` passes locally (all 3 manifests)
- [ ] Plugin Validation CI check passes
- [ ] No regression in plugin functionality

---

## Related Items

### Hierarchy

- **Parent:** [FEAT-001: Fix CI Build Failures](./FEAT-001-fix-ci-build-failures.md)

### Decision

- [FEAT-001:DEC-001: JSON Schema Validator Class Selection](./FEAT-001--DEC-001-json-schema-validator-class.md) — Decided to use explicit `Draft202012Validator` (Option B)

### CI Reference

- **CI Run:** [GitHub Actions #21845050753](https://github.com/geekatron/jerry/actions/runs/21845050753/job/63161832093)

### Files Involved

| File | Role | Change Needed |
|------|------|---------------|
| `schemas/marketplace.schema.json` | Marketplace schema | **Fix: add `keywords` to plugin item properties** |
| `scripts/validate_plugin_manifests.py` | Validation script | Best practice: add `cls=jsonschema.Draft202012Validator` |
| `.claude-plugin/marketplace.json` | Marketplace manifest | No change (correct — has `keywords`) |
| `schemas/plugin.schema.json` | Plugin schema | No change (already has `keywords`) |
| `.claude-plugin/plugin.json` | Plugin manifest | No change (passes validation) |

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-02-10 | Claude | pending | Bug triaged from PR #6 CI failure |
| 2026-02-10 | Claude | pending | Root cause analysis: initially identified as JSON Schema draft mismatch |
| 2026-02-10 | Claude | in_progress | **CORRECTED**: Root cause is missing `keywords` in marketplace schema, not draft mismatch. Local verification confirmed plugin.json passes, marketplace.json fails with both default and Draft202012 validators. Tasks reorganized. |
