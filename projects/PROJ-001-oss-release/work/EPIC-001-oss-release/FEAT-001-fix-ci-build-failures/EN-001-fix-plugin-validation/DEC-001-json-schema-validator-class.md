# EN-001:DEC-001: JSON Schema Validator Class Selection

> **Type:** decision
> **Status:** ACCEPTED
> **Priority:** HIGH
> **Created:** 2026-02-10
> **Parent:** EN-001
> **Owner:** Adam Nowak
> **Related:** BUG-001

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Brief description of decision |
| [Decision Context](#decision-context) | Background and constraints |
| [Decisions](#decisions) | Structured decision entries |
| [Decision Summary](#decision-summary) | Quick reference table |
| [Related Artifacts](#related-artifacts) | Traceability |
| [Document History](#document-history) | Changes |

---

## Summary

Decision on how to fix BUG-001 (Plugin manifest schema validation error where `keywords` is rejected as unexpected despite being defined in the schema).

**Decisions Captured:** 1

**Key Outcomes:**
- Use explicit `Draft202012Validator` class instead of downgrading the schema
- Fix lives in the validation call site, not the schema definition

---

## Decision Context

### Background

The plugin manifest validation CI step fails with: `Additional properties are not allowed ('keywords' was unexpected)`. Investigation revealed:

1. The schema (`schemas/plugin.schema.json`) correctly defines `keywords` as a valid property
2. The schema uses JSON Schema Draft 2020-12 (`"$schema": "https://json-schema.org/draft/2020-12/schema"`)
3. The Python `jsonschema` library defaults to Draft 4 or Draft 7 when no validator class is specified
4. The validation call (`jsonschema.validate(manifest, schema)`) does not specify a validator class
5. The draft mismatch causes the library to ignore the `properties` definitions, treating all properties as additional

### Constraints

- Must not break existing schema definitions
- Must support JSON Schema Draft 2020-12 features if needed in the future
- Fix must be minimal and targeted

---

## Decisions

### D-001: Use explicit Draft202012Validator instead of downgrading schema

**Date:** 2026-02-10
**Participants:** Adam Nowak, Claude

#### Question/Context

The `jsonschema.validate()` call in `validate_plugin_manifests.py` doesn't specify which JSON Schema draft to use. Two options were proposed:
1. Downgrade the schema from Draft 2020-12 to Draft 7
2. Specify `cls=jsonschema.Draft202012Validator` at the call site

Claude initially recommended Option 1 (downgrade) as "simpler and more portable." Adam challenged this recommendation, asking Claude to critique its own answer.

#### Options Considered

| Option | Description | Pros | Cons |
|--------|-------------|------|------|
| **A: Downgrade schema to Draft 7** | Change `$schema` to Draft 7 in all schema files | Works with default validator | Modifies correct artifact to fix incorrect consumer; loses Draft 2020-12 features; signals wrong intent |
| **B: Specify validator class explicitly** | Add `cls=jsonschema.Draft202012Validator` to `jsonschema.validate()` calls | Fixes bug where it lives; preserves schema intent; forward-compatible | Requires knowing the validator class name |

#### Decision

**We decided:** Option B — Specify `cls=jsonschema.Draft202012Validator` explicitly at all three `jsonschema.validate()` call sites in `scripts/validate_plugin_manifests.py`.

#### Rationale

1. **The schema is correct** — it properly defines `keywords` as a valid property. The bug is in the validation consumer, not the schema definition.
2. **Option A fixes the wrong thing** — modifying a correct artifact to work around an incorrect consumer is a workaround, not a fix.
3. **Equally simple** — both options are one-line changes; there is no meaningful complexity difference.
4. **Forward-compatible** — preserves access to Draft 2020-12 features (e.g., `prefixItems`, `$dynamicRef`) if needed in the future.
5. **Signals correct intent** — tells future contributors that the project uses modern JSON Schema, not that it can't support it.

#### Implications

- **Positive:** Correct fix at the right layer; forward-compatible; maintains schema author's intent
- **Negative:** None identified
- **Follow-up required:** Verify `jsonschema` package version supports Draft 2020-12 (requires >= 4.0)

---

## Decision Summary

| ID | Decision | Date | Status |
|----|----------|------|--------|
| D-001 | Use explicit `Draft202012Validator` class instead of downgrading schema | 2026-02-10 | ACCEPTED |

---

## Related Artifacts

| Type | Path | Description |
|------|------|-------------|
| Parent | [EN-001](./EN-001-fix-plugin-validation.md) | Fix Plugin Validation |
| Feature | [FEAT-001](../FEAT-001-fix-ci-build-failures.md) | Fix CI Build Failures |
| Bug | [BUG-001](./BUG-001-marketplace-manifest-schema-error.md) | Marketplace manifest schema error |
| File | `scripts/validate_plugin_manifests.py` | Validation script to fix |
| File | `schemas/plugin.schema.json` | Schema (correct, no changes needed) |
| File | `.claude-plugin/plugin.json` | Manifest (correct, no changes needed) |

---

## Addendum (2026-02-10)

**Root Cause Correction:** Subsequent local verification revealed that the actual CI failure is in `marketplace.json`, not `plugin.json`, and the root cause is a **missing `keywords` property** in the marketplace plugin item schema — not a JSON Schema draft mismatch. Both default and `Draft202012Validator` produce the same failure for `marketplace.json`.

**DEC-001 Status:** This decision remains **ACCEPTED** as a best practice improvement (TASK-003), but it is **not the root cause fix**. The actual fix is TASK-001: adding `keywords` to the marketplace schema.

---

## Document History

| Date | Author | Change |
|------|--------|--------|
| 2026-02-10 | Claude | Created decision document |
| 2026-02-10 | Claude | Added addendum: DEC-001 is best practice, not root cause fix. Root cause is missing `keywords` in marketplace schema. |

---

## Metadata

```yaml
id: "EN-001:DEC-001"
parent_id: "EN-001"
work_type: DECISION
title: "JSON Schema Validator Class Selection"
status: ACCEPTED
priority: HIGH
created_by: "Claude"
created_at: "2026-02-10"
updated_at: "2026-02-10"
decided_at: "2026-02-10"
participants: ["Adam Nowak", "Claude"]
tags: ["json-schema", "validation", "bug-fix"]
decision_count: 1
superseded_by: null
supersedes: null
```
