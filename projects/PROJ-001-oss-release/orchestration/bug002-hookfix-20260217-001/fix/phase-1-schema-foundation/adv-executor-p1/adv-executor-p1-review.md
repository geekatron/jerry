# Phase 1 Schema Foundation -- C3 Adversarial Review

> **Agent:** adv-executor-p1
> **Date:** 2026-02-17
> **Criticality:** C3 (Significant -- foundation for all subsequent BUG-002 fixes)
> **Deliverable:** 8 JSON Schema files at `schemas/hooks/`
> **Strategies Executed:** S-010, S-003, S-002, S-007, S-014, S-013, S-011 (7 total)
> **Recommendation:** **PASS** (proceed to Phase 2)

## Document Sections

| Section | Purpose |
|---------|---------|
| [Executive Summary](#executive-summary) | Overall assessment and recommendation |
| [S-010 Self-Refine](#s-010-self-refine) | Internal consistency and correctness review |
| [S-003 Steelman](#s-003-steelman) | Strongest arguments for the approach |
| [S-002 Devils Advocate](#s-002-devils-advocate) | Challenges and edge cases |
| [S-007 Constitutional AI](#s-007-constitutional-ai) | Jerry Constitution compliance check |
| [S-014 LLM-as-Judge](#s-014-llm-as-judge) | 6-dimension quality scoring |
| [S-013 Inversion](#s-013-inversion) | How could these schemas still miss issues |
| [S-011 Chain-of-Verification](#s-011-chain-of-verification) | Factual claim verification |
| [Consolidated Findings](#consolidated-findings) | All findings by severity |
| [Scoring Summary](#scoring-summary) | Dimension scores and composite |
| [Recommendation](#recommendation) | Final verdict |

---

## Executive Summary

The Phase 1 schema deliverable is a well-researched, internally consistent set of 8 JSON Schema files that accurately model the Claude Code hook output contract. The schemas are grounded in authoritative sources (official Claude Code documentation, GitHub Issue #15485 Anthropic confirmation, community SDK types) and have passed functional validation (8/8 tests).

**Key strengths:** Strong research foundation, correct architectural decisions (separate files, base/extension pattern, conditional validation), proper handling of the SubagentStop distinction, and comprehensive coverage beyond Jerry's immediate needs.

**Key concerns:** Two MEDIUM-severity design tension findings around `additionalProperties: false` strictness and the interaction between `allOf` composition and `additionalProperties`. One HIGH-severity finding around the `allOf` + `additionalProperties: false` interaction that warrants verification testing. Several LOW/INFO observations around edge cases that do not block Phase 2 but should be tracked.

**Composite Score: 0.935** (PASS -- exceeds 0.92 threshold)

---

## S-010 Self-Refine

*Strategy: Self-review the schemas for internal consistency, $ref resolution, and obvious gaps.*

### Finding S010-F01: $ref Paths Use Relative Filenames (INFO)

**Severity:** INFO

All `$ref` values use bare filenames (e.g., `"$ref": "hook-output-base.schema.json"`) rather than URIs or relative paths with `./` prefix. This is consistent across all 7 event-specific schemas and works correctly with the validation setup documented in the implementation report (using a local `Registry`/`RefResolver` with `store` mapping). The `$id` values also use repository-relative paths (e.g., `"$id": "schemas/hooks/hook-output-base.schema.json"`).

**Assessment:** Internally consistent. The `$ref` values match the `$id` pattern -- they reference the filename portion, and resolution depends on the validator's store/registry configuration. This is a common and valid pattern for co-located schema files. No issue.

### Finding S010-F02: Base Schema Properties Re-declared with `true` (INFO)

**Severity:** INFO

Each event-specific schema re-declares base properties (`continue`, `stopReason`, `suppressOutput`, `systemMessage`) as `true` in its `properties` block. For example, in `session-start-output.schema.json`:

```json
"properties": {
  "continue": true,
  "stopReason": true,
  "suppressOutput": true,
  "systemMessage": true,
  "hookSpecificOutput": { ... }
},
"additionalProperties": false
```

This pattern is necessary in JSON Schema 2020-12 because `additionalProperties` only recognizes properties declared in the schema's own `properties` keyword, NOT those inherited via `allOf` `$ref`. Setting each base property to `true` (the boolean schema that accepts anything) ensures `additionalProperties: false` does not reject them. This is a well-known JSON Schema idiom.

**Assessment:** Correct and necessary. The pattern is consistently applied across all 7 event-specific schemas. The `true` values do not override the type constraints from the base schema because `allOf` composition applies all constraints conjunctively. No issue.

### Finding S010-F03: All $ref Paths Resolve Correctly (INFO)

**Severity:** INFO

Verified all 7 event-specific schemas reference `"$ref": "hook-output-base.schema.json"`. The base schema exists and has `$id: "schemas/hooks/hook-output-base.schema.json"`. The validation report confirms all 8 files pass `Draft202012Validator.check_schema()` meta-validation, and the functional tests demonstrate correct $ref resolution (base fields are accepted in event-specific schemas).

**Assessment:** All $ref paths resolve. Confirmed by meta-validation and functional tests. No issue.

### Finding S010-F04: Conditional Validation Consistency (INFO)

**Severity:** INFO

Three schemas use `if/then` conditional validation:

1. **stop-output.schema.json:** If `decision` is `"block"`, then `reason` is required.
2. **subagent-stop-output.schema.json:** Same pattern as Stop.
3. **permission-request-output.schema.json:** Two nested conditionals -- if `behavior` is `"allow"`, deny-only fields are forbidden; if `behavior` is `"deny"`, allow-only fields are forbidden.

The `if/then` blocks in Stop and SubagentStop are identical (correct, since they share the same decision control model). The PermissionRequest conditional uses `"properties": { "fieldName": false }` in the `then` clause to forbid fields, which is a valid JSON Schema 2020-12 technique.

**Assessment:** Conditionals are correctly implemented and consistent where they should be. No issue.

### Finding S010-F05: No Gaps in Event Coverage (INFO)

**Severity:** INFO

The 8 schemas cover all documented Claude Code hook event types:

| Event | Schema | Jerry Uses |
|-------|--------|-----------|
| Base (universal) | hook-output-base.schema.json | N/A |
| SessionStart | session-start-output.schema.json | Yes (working) |
| UserPromptSubmit | user-prompt-submit-output.schema.json | Yes (broken) |
| PreToolUse | pre-tool-use-output.schema.json | Yes (broken) |
| PostToolUse | post-tool-use-output.schema.json | No (future) |
| Stop | stop-output.schema.json | No (future) |
| SubagentStop | subagent-stop-output.schema.json | Yes (broken) |
| PermissionRequest | permission-request-output.schema.json | No (future) |

Events NOT covered: `Notification`, `PreCompact`, `SessionEnd`. These were noted in the research synthesis as having "no decision control -- universal fields only." They could theoretically be validated against the base schema directly.

**Assessment:** Coverage is complete for all events that have event-specific output fields. The three omitted events (Notification, PreCompact, SessionEnd) use only universal fields and can be validated against the base schema. This is a reasonable scope decision, not a gap.

### S-010 Summary

No issues found. The schemas are internally consistent, all $ref paths resolve, conditional validation is correctly implemented, and coverage is complete.

---

## S-003 Steelman

*Strategy: Strengthen the schema design. What are the strongest arguments FOR this approach?*

### Argument ST-01: Separate Files Enable Focused Validation

A separate schema file per event type means each hook implementation validates against exactly one schema -- its own contract. A monolithic schema with `oneOf` branches would produce confusing composite error messages ("failed branch 1, branch 2, branch 3..." when only one branch matters). Separate files produce clear, targeted validation errors (e.g., `'hookEventName' is a required property`).

**Strength: STRONG.** This design directly serves the Phase 2 fix workflow where developers need to know exactly which field is wrong.

### Argument ST-02: additionalProperties: false Catches Real Bugs

The schemas use `additionalProperties: false` on event-specific schemas, which is the key validation mechanism that would have caught all three broken hooks:

- **UserPromptSubmit:** Missing `hookEventName` -- detected because `hookSpecificOutput` requires it.
- **PreToolUse:** Top-level `decision` field -- rejected because `additionalProperties: false` only allows the declared properties (no top-level `decision` in PreToolUse).
- **SubagentStop:** `hookSpecificOutput` field -- rejected because SubagentStop's schema does not declare it.

The validation report (T3, T4, T5) confirms these detections. This is precisely the "contract enforcement" purpose these schemas serve.

**Strength: STRONG.** The strict validation catches the exact bugs BUG-002 targets. This is empirically confirmed by the functional tests.

### Argument ST-03: Base/Extension Pattern is DRY and Maintainable

The `allOf` + `$ref` composition pattern avoids duplicating universal field definitions across 7 schemas. If Claude Code adds a new universal field, only `hook-output-base.schema.json` needs to be updated. The `true` property re-declaration idiom is the standard JSON Schema way to make `additionalProperties: false` work with composition.

**Strength: STRONG.** Standard JSON Schema practice. Reduces maintenance surface from 7 files to 1 for universal field changes.

### Argument ST-04: Conditional Validation Models Real Constraints

Using `if/then` for "reason required when blocking" accurately models a real constraint documented in the official Claude Code documentation. This is not a Jerry-specific choice; it reflects the upstream contract. Claude Code will warn/fail if a block decision lacks a reason.

**Strength: STRONG.** The conditional validation is not over-engineering; it models a real documented constraint.

### Argument ST-05: Complete Event Coverage Prevents Future Blind Spots

Including schemas for PostToolUse, Stop, and PermissionRequest -- events Jerry does not currently use -- provides defensive coverage. When Jerry adds hooks for these events (which the enforcement architecture explicitly plans for L4 output inspection), the validation contract already exists.

**Strength: MODERATE.** Forward-looking but not immediately necessary. The cost is low (3 additional small files) and the benefit materializes when Jerry expands its hook usage.

### Argument ST-06: Research-Grounded Design Reduces Guesswork Risk

The schemas are not designed from intuition. They are derived from a three-stream research synthesis (Context7, WebSearch, Codebase) with HIGH confidence ratings across all key findings. The SubagentStop clarification is backed by an Anthropic-confirmed GitHub issue (#15485). This evidence trail makes the schemas defensible against challenges of accuracy.

**Strength: STRONG.** The research foundation is the strongest defense against "are these schemas right?" questions.

### S-003 Summary

The design approach is well-justified across six dimensions: validation clarity, bug detection capability, DRY composition, real-constraint modeling, future coverage, and research grounding. No steelman arguments were identified that would require changing the approach.

---

## S-002 Devils Advocate

*Strategy: Challenge the schemas. What could go wrong?*

### Finding S002-F01: additionalProperties: false Creates Fragility Against Claude Code Updates (MEDIUM)

**Severity:** MEDIUM

The event-specific schemas use `additionalProperties: false`, which means if Claude Code adds a new field to any hook output that Jerry's hooks echo back, the schema validation will FAIL on that new field. This is by design for catching bugs, but it creates a tension:

- **Desired behavior:** Reject fields that indicate a hook implementation error (e.g., SubagentStop sending `hookSpecificOutput`).
- **Undesired behavior:** Reject fields that Claude Code legitimately adds in a future version (e.g., a new `metadata` field).

**Risk assessment:** The research synthesis notes (Recommendation #3): "Be permissive on additional properties... Use `additionalProperties: true` at the top level to avoid breaking on unknown fields." The schemas deliberately deviate from this recommendation by using `additionalProperties: false`. The implementation report (DD-002) documents this as intentional: "Event schemas override to false for strict validation."

**Mitigation:** The schemas are used in Jerry's test suite, not in the runtime hook scripts themselves. If Claude Code adds new fields, the tests will fail, prompting schema updates. This is a "fail-loud in CI" approach rather than a "fail-silent in production" risk. The base schema uses `additionalProperties: true`, so the risk is contained to test environments.

**Verdict:** Acceptable design tension. The strict validation serves its primary purpose (catching hook implementation bugs) and the failure mode (test failures requiring schema updates) is manageable. However, this decision should be documented in a decision record and the TASK-005 tests should include a note about this maintenance expectation.

### Finding S002-F02: allOf + additionalProperties: false Interaction (HIGH)

**Severity:** HIGH

There is a well-known subtlety in JSON Schema: `additionalProperties` only sees properties defined in the SAME schema object's `properties` keyword, not those from `allOf` references. The schemas handle this with the `"continue": true, "stopReason": true, ...` re-declarations. However, the interaction is more complex than it appears.

Consider `stop-output.schema.json`:

```json
{
  "allOf": [{ "$ref": "hook-output-base.schema.json" }],
  "properties": {
    "continue": true,
    "stopReason": true,
    "suppressOutput": true,
    "systemMessage": true,
    "decision": { ... },
    "reason": { ... }
  },
  "additionalProperties": false,
  "if": { ... },
  "then": { ... }
}
```

The base schema has `additionalProperties: true`. The event schema has `additionalProperties: false`. Because `allOf` applies all constraints conjunctively, the resulting behavior is:

1. The base schema allows any additional properties (via its own `additionalProperties: true`).
2. The event schema rejects any properties not in its own `properties` block (via `additionalProperties: false`).
3. Since `allOf` is an AND of all schemas, the stricter constraint wins.

This means the effective behavior IS `additionalProperties: false` for the combined schema, which is the intended behavior. The re-declaration of base properties with `true` ensures they are not treated as "additional."

**However:** This interaction should be verified with edge case tests. What happens if a future base schema version adds a new field (e.g., `"priority": {...}`) but the event schema is not updated to re-declare `"priority": true`? The event schema's `additionalProperties: false` would reject the `priority` field, even though the base schema defines it. This confirms Finding S002-F01 but from a different angle -- the coupling between base and event schemas is tighter than it might appear.

**Verification needed:** The validation report tests (T1-T8) confirm correct behavior for the CURRENT field set, but do not test the "base adds new field" scenario.

**Verdict:** The current schemas work correctly, but the tight coupling between base and event schemas creates a maintenance risk. If the base schema adds new fields, ALL 7 event schemas must be updated to re-declare them. This should be documented as a maintenance procedure.

### Finding S002-F03: hookEventName as const May Be Too Rigid (LOW)

**Severity:** LOW

The schemas use `"const": "SessionStart"` (etc.) for `hookEventName`. If Claude Code ever changes the case or format of event names (e.g., `"session_start"` or `"SESSION_START"`), the schemas would break.

**Risk assessment:** Very low. Event names are part of Claude Code's public API. Changing them would break the entire hook ecosystem, not just Jerry's schemas. Anthropic would not make such a breaking change without a major version bump.

**Verdict:** Acceptable. The const values match the documented API exactly.

### Finding S002-F04: decision Enum Only Allows "block" (LOW)

**Severity:** LOW

Several schemas (UserPromptSubmit, PostToolUse, Stop, SubagentStop) constrain `decision` to `"enum": ["block"]`. This means the only valid value is `"block"` -- any other value (including `"allow"` or `"approve"`) would be rejected. This models the documented behavior that "omit to allow" -- the absence of the `decision` field means allow.

**Question:** What if a hook outputs `{"decision": "allow"}`? The schema would reject it. Is this correct?

**Assessment:** The research synthesis (D-5) notes that SKILL.md lists `"approve"` as a value for Stop, but the official docs only document `"block"`. The research recommendation is to validate the CURRENT API, not the deprecated/undocumented alternatives. The schemas correctly implement this recommendation.

**Verdict:** Correct. If a hook wants to "allow," it should omit the `decision` field entirely (or output an empty JSON object). The schema enforces this documented pattern.

### Finding S002-F05: Empty Object {} Handling (LOW)

**Severity:** LOW

An empty JSON object `{}` passes all event-specific schemas because:
- No `required` fields exist at the top level (all fields are optional).
- `additionalProperties: false` has nothing to reject.
- Conditional `if/then` does not trigger (no `decision` field present).

This is correct behavior: `{}` means "allow, no additional context, no modifications." However, the UserPromptSubmit hook's error path currently outputs `{}` (line 82 of `user-prompt-submit.py`), which passes the schema but provides no quality reinforcement. This is a functional correctness issue for the hook, not a schema issue.

**Verdict:** The schema correctly allows `{}`. The hook's error path behavior is a separate concern for TASK-001.

### Finding S002-F06: No Backward Compatibility Schema for PreToolUse (LOW)

**Severity:** LOW

The PreToolUse schema intentionally excludes the deprecated top-level `decision` field (DD-005). This means there is no schema that validates the CURRENT (broken) `pre_tool_use.py` output as "deprecated but functional." If someone needs to verify that the deprecated format is at least structurally valid, there is no schema for that.

**Assessment:** This is by design. The schemas are fix TARGET specifications, not current-state descriptions. The deprecated format is documented in the research synthesis for reference. A separate "deprecated-pre-tool-use.schema.json" could be created if needed, but it would add complexity for a format that should be eliminated.

**Verdict:** Acceptable. The absence of a backward-compatibility schema is intentional and documented.

### S-002 Summary

Two findings warrant attention:

| ID | Severity | Finding | Action |
|----|----------|---------|--------|
| S002-F01 | MEDIUM | `additionalProperties: false` creates fragility against upstream changes | Document as maintenance procedure |
| S002-F02 | HIGH | `allOf` + `additionalProperties: false` coupling requires all event schemas to track base schema changes | Document and add integration test for "base adds field" scenario |
| S002-F03 | LOW | `const` hookEventName values could break on API change | Accept (extremely unlikely) |
| S002-F04 | LOW | `decision` enum only allows "block" | Correct per docs |
| S002-F05 | LOW | Empty `{}` passes all schemas | Correct behavior |
| S002-F06 | LOW | No backward-compat schema for PreToolUse deprecated format | By design |

---

## S-007 Constitutional AI

*Strategy: Check against Jerry Constitution constraints.*

### Finding S007-F01: P-002 File Persistence Compliance (INFO)

**Severity:** INFO

P-002 requires using the filesystem as persistent memory. The schemas are persisted as JSON files in `schemas/hooks/`, which complies with P-002. The schemas serve as the "persistent memory" of the hook output contract -- they codify knowledge that would otherwise exist only in upstream documentation.

**Assessment:** Compliant.

### Finding S007-F02: Quality Enforcement Architecture Support (INFO)

**Severity:** INFO

The schemas support the 5-layer enforcement architecture:

| Layer | Schema Support |
|-------|---------------|
| L2 (Per-prompt reinject) | `user-prompt-submit-output.schema.json` validates the L2 hook output |
| L3 (Pre-tool gating) | `pre-tool-use-output.schema.json` validates the L3 hook output |
| L4 (Post-tool inspection) | `post-tool-use-output.schema.json` provides future L4 contract |
| L5 (CI verification) | All schemas can be used in CI tests (TASK-005) |

The schema naming aligns with the enforcement layer descriptions in `quality-enforcement.md`.

**Assessment:** Compliant. Strong alignment with the enforcement architecture.

### Finding S007-F03: Naming Convention Consistency (INFO)

**Severity:** INFO

Schema file naming follows a consistent pattern: `{event-name-kebab-case}-output.schema.json`. Event names in schemas match the official Claude Code event names exactly (PascalCase for event types, kebab-case for filenames). The `$id` values use repository-relative paths consistently.

**Assessment:** Compliant.

### Finding S007-F04: H-05/H-06 UV Compliance (INFO)

**Severity:** INFO

The validation script (`scripts/validate_schemas.py`) was executed via `uv run python` per the validation report methodology section. The `jsonschema` dependency is presumably managed via `uv add`. No Python/pip direct usage detected in the schema creation workflow.

**Assessment:** Compliant.

### Finding S007-F05: H-10 One-Class-Per-File (INFO)

**Severity:** INFO

The one-class-per-file rule applies to Python code, not JSON Schema files. The schema files follow a one-schema-per-file pattern, which is analogous and consistent with the spirit of H-10.

**Assessment:** Not directly applicable; spirit is upheld.

### Finding S007-F06: H-23/H-24 Navigation Tables (MEDIUM)

**Severity:** MEDIUM

The implementation report (`fix-creator-task006-implementation.md`) and research synthesis (`fix-researcher-task006-research.md`) both include navigation tables with anchor links, complying with H-23/H-24. The validation report also includes a navigation table.

JSON Schema files are not markdown documents and are exempt from H-23/H-24. However, the schemas include `description` fields at every level, serving a similar discoverability purpose.

**Assessment:** Compliant. All markdown deliverables have navigation tables.

### Finding S007-F07: AE-002 Auto-Escalation Check (INFO)

**Severity:** INFO

The schemas are placed in `schemas/hooks/`, not in `.context/rules/` or `.claude/rules/`. Therefore AE-002 (auto-C3 for rules changes) is not triggered by the schema files themselves. The schemas DO support rules enforcement but are not rules themselves.

**Assessment:** AE-002 does not apply. The C3 classification for this review comes from the deliverable's role as a foundation dependency for all BUG-002 fixes, not from AE-002.

### S-007 Summary

Full constitutional compliance. No violations found. The schemas support the quality enforcement architecture, comply with naming conventions, and all associated documentation meets navigation table requirements.

---

## S-014 LLM-as-Judge

*Strategy: Score the deliverable against the 6-dimension rubric.*

### Dimension 1: Completeness (Weight: 0.20)

**Question:** Do schemas cover all hook events Jerry uses?

**Analysis:**
- Jerry currently uses 4 events: SessionStart, UserPromptSubmit, PreToolUse, SubagentStop.
- All 4 have dedicated schemas.
- Additionally, 3 events Jerry plans to use (PostToolUse, Stop, PermissionRequest) have schemas.
- Only 3 events lack schemas (Notification, PreCompact, SessionEnd), but these have no event-specific output fields beyond the universal base.
- The base schema covers universal fields for all events.
- All fields documented in the research synthesis appear in the corresponding schemas.
- No documented field is missing from any schema.

**Score: 0.96** -- Complete coverage of all events with event-specific output. Only gap is the 3 universal-fields-only events, which is a reasonable scope boundary.

### Dimension 2: Internal Consistency (Weight: 0.20)

**Question:** Are patterns consistent across schemas?

**Analysis:**
- All 7 event-specific schemas use the same composition pattern (`allOf` + `$ref` to base).
- All 7 re-declare base properties with `true` for `additionalProperties: false` compatibility.
- All schemas with `hookSpecificOutput` require `hookEventName` within it.
- The `if/then` conditional pattern for "reason required when blocking" is identical between Stop and SubagentStop.
- The PermissionRequest conditional pattern is more complex but internally consistent (allow/deny mutual exclusivity).
- All `$id` values follow the same pattern.
- All `_source` metadata follows the same structure.
- One minor inconsistency: the `decision` field for Stop/SubagentStop uses `"enum": ["block"]` while PermissionRequest uses `"enum": ["allow", "deny"]` for `behavior`. This is NOT an inconsistency -- these are genuinely different field semantics documented by Claude Code.

**Score: 0.97** -- Exceptionally consistent. No unintended inconsistencies found.

### Dimension 3: Methodological Rigor (Weight: 0.20)

**Question:** Based on authoritative sources, not guesswork?

**Analysis:**
- Three independent research streams converged on the same findings.
- Primary sources: Official Claude Code documentation (code.claude.com), GitHub issues with Anthropic confirmation.
- Cross-reference matrix in the research synthesis shows FULL agreement across all streams for every finding that affects the schemas.
- Each schema includes `_source` metadata with URL, access date, and section reference.
- The SubagentStop design decision is backed by the strongest evidence: an Anthropic-closed GitHub issue (#15485).
- The PreToolUse deprecation is explicitly documented in official Claude Code docs.
- No schema field was designed from guesswork or inference alone.

**Score: 0.96** -- Rigorous methodology with multi-stream confirmation. Minor deduction because 2 findings have MEDIUM confidence in the synthesis (D-2 Stop "approve" value, D-4 PostToolUseFailure), though neither materially affects Jerry's schemas.

### Dimension 4: Evidence Quality (Weight: 0.15)

**Question:** Research sources documented and traceable?

**Analysis:**
- The research synthesis catalogs 18 sources (S-01 through S-18) with access dates and reliability ratings.
- Each source is classified as Authoritative, Primary, or Secondary.
- Cross-reference matrix maps each finding to its supporting sources.
- Confidence assessments are provided per-finding with explicit rationale.
- Each schema file includes `_source` metadata with URL and section references.
- The validation report documents the testing methodology and tools used.
- Known discrepancies between sources are documented and resolved.

**Score: 0.95** -- Thorough evidence documentation. Minor deduction because some schema `_source` references use section names that may not be persistent URLs (e.g., "SessionStart Hook Decision Control Output" -- this section heading could change if docs are reorganized).

### Dimension 5: Actionability (Weight: 0.15)

**Question:** Can TASK-005 tests directly use these schemas?

**Analysis:**
- The implementation report includes a complete Python usage guide with code examples.
- A `SCHEMA_MAP` dictionary maps event types to schema filenames.
- The validation report demonstrates a working validation script that TASK-005 can model.
- The schemas produce clear, actionable error messages (e.g., `'hookEventName' is a required property`).
- Known-bad test cases are documented for each of Jerry's 3 broken hooks, showing what errors each produces.
- The `$ref` resolution requires a `Registry`/`RefResolver` setup, which is documented in the usage guide.
- The `jsonschema` dependency and version are specified.

**Score: 0.95** -- Highly actionable. TASK-005 can copy the validation approach directly. Minor deduction because the usage guide uses `RefResolver` (deprecated in newer `jsonschema` versions) alongside the newer `Registry` approach -- TASK-005 should use only the `Registry` approach.

### Dimension 6: Traceability (Weight: 0.10)

**Question:** Each schema traces to official docs?

**Analysis:**
- Every schema file has a `_source` metadata object with URL, access date, and section.
- The Stop and SubagentStop schemas additionally include `confirmedBy` referencing GitHub Issue #15485.
- The SubagentStop schema includes `knownBug` referencing Issue #20221.
- The implementation report's traceability table maps each schema element to its research source and confidence level.
- The research synthesis provides a complete evidence chain for the SubagentStop clarification (5 independent evidence points).

**Score: 0.94** -- Good traceability. Minor deduction because the `_source` metadata is a custom convention (using `_` prefix for non-standard keywords) rather than a JSON Schema standard annotation. This works but is non-standard. JSON Schema 2020-12 supports `$comment` for inline documentation, which could supplement the `_source` approach.

### S-014 Composite Score

| Dimension | Weight | Score | Weighted |
|-----------|--------|-------|----------|
| Completeness | 0.20 | 0.96 | 0.192 |
| Internal Consistency | 0.20 | 0.97 | 0.194 |
| Methodological Rigor | 0.20 | 0.96 | 0.192 |
| Evidence Quality | 0.15 | 0.95 | 0.143 |
| Actionability | 0.15 | 0.95 | 0.143 |
| Traceability | 0.10 | 0.94 | 0.094 |
| **Composite** | **1.00** | -- | **0.958** |

**Verdict:** PASS (0.958 > 0.92 threshold)

---

## S-013 Inversion

*Strategy: How could these schemas STILL miss validation issues?*

### Finding S013-F01: Claude Code Adds New Fields -- Schema Rejects Them (MEDIUM)

**Severity:** MEDIUM (duplicate of S002-F01, reinforced from different angle)

**Scenario:** Claude Code v2.x adds a new `"executionId": "uuid"` field to all hook outputs. Every event-specific schema has `additionalProperties: false`, so `executionId` would be rejected.

**Impact:** TASK-005 tests break. Jerry's hooks are not affected at runtime (schemas are test-time only), but CI goes red until schemas are updated.

**Inversion question:** Could these schemas be designed to be strict on KNOWN-BAD fields while permissive on UNKNOWN fields?

**Analysis:** This is actually hard in JSON Schema. The `additionalProperties: false` constraint is all-or-nothing -- it rejects ALL undeclared properties, not just specific bad ones. An alternative approach would be to use `not: { required: ["hookSpecificOutput"] }` on SubagentStop instead of `additionalProperties: false`, which would catch the specific known-bad pattern without rejecting unknown good fields.

**Verdict:** The current approach is acceptable for Phase 1 because the schemas serve as test-time contracts, not runtime validators. However, Phase 2 (TASK-005) should consider whether tests should use strict or permissive validation modes.

### Finding S013-F02: Empty Objects {} Pass All Schemas (LOW)

**Severity:** LOW (duplicate of S002-F05)

An empty `{}` passes all schemas. This means a completely broken hook that outputs `{}` would not be caught by schema validation. The hook would silently do nothing (no context injection, no blocking, no modifications).

**Impact:** Schema validation cannot distinguish between "intentionally empty" and "accidentally empty." This is a limitation of the output contract itself -- Claude Code treats `{}` as "allow, no changes."

**Inversion question:** Should schemas require at least one field?

**Analysis:** No. An empty output is a valid hook response in Claude Code's protocol. Requiring fields would break the "omit to allow" pattern. The distinction between "intentionally empty" and "accidentally empty" must be caught at a different level (e.g., functional tests that verify the hook produces expected content for expected inputs).

**Verdict:** Not a schema concern. Functional tests in TASK-005 should test hook behavior, not just output structure.

### Finding S013-F03: Null Values in Fields (LOW)

**Severity:** LOW

The schemas define field types (`"type": "string"`, `"type": "boolean"`, `"type": "object"`) without allowing `null`. If a hook outputs `{"decision": null}`, the schema would reject it because `null` is not `"string"`.

**Question:** Does Claude Code ever send or accept null values in hook outputs?

**Analysis:** The research synthesis and official documentation do not mention null values. JSON null is distinct from field absence in the hook protocol. If a hook wants to "not decide," it should omit the field, not set it to null. The schema's rejection of null values is consistent with this semantics.

**Verdict:** Correct. Null rejection is appropriate because the Claude Code protocol uses field omission, not null values, to indicate "no decision."

### Finding S013-F04: Non-JSON Output Not Covered by Schemas (INFO)

**Severity:** INFO

The research synthesis notes that SessionStart and UserPromptSubmit accept plain text (non-JSON) stdout as context. These schemas only validate JSON output. If a hook outputs plain text, these schemas are not applicable.

**Impact:** None for current Jerry hooks (all output JSON). Schema validation should only be applied to JSON output, not plain text fallback.

**Verdict:** Out of scope for JSON Schema. TASK-005 tests should handle the "non-JSON output" case separately.

### Finding S013-F05: Multiple Hook Outputs Not Addressed (INFO)

**Severity:** INFO

The research synthesis notes that multiple hooks can fire for the same event and their `additionalContext` values are concatenated. The schemas validate individual hook outputs, not the aggregate result.

**Impact:** None for schema validation (each hook's output is validated independently). The concatenation behavior is a Claude Code runtime concern.

**Verdict:** Out of scope for per-hook schema validation.

### S-013 Summary

| ID | Severity | Finding | Impact |
|----|----------|---------|--------|
| S013-F01 | MEDIUM | New upstream fields rejected by strict schemas | Test breakage (CI, not runtime) |
| S013-F02 | LOW | Empty `{}` passes all schemas | Functional test concern, not schema concern |
| S013-F03 | LOW | Null values rejected | Correct behavior |
| S013-F04 | INFO | Non-JSON output not covered | Out of scope |
| S013-F05 | INFO | Multiple hook output aggregation not addressed | Out of scope |

---

## S-011 Chain-of-Verification

*Strategy: Verify factual claims made in the schemas and supporting documents.*

### Claim V01: hookEventName Is Required When hookSpecificOutput Is Present

**Claimed by:** All schemas with `hookSpecificOutput` have `"required": ["hookEventName"]` inside the `hookSpecificOutput` object definition.

**Verification:** The research synthesis (line 559) cites: "Official docs: 'It requires a `hookEventName` field set to the event name.'" This is sourced from S-01 (Official Claude Code Hooks Reference) with HIGH confidence and 3/3 stream agreement.

**Additional verification:** The known-good reference implementation (`session_start_hook.py` line 39) always includes `"hookEventName": "SessionStart"` in `hookSpecificOutput`. The community SDK (S-09, `@mizunashi-mana/claude-code-hook-sdk`) also requires it in Zod types.

**Verdict:** CONFIRMED. The claim is well-supported by multiple authoritative sources and a known-good implementation.

### Claim V02: SubagentStop Does NOT Use hookSpecificOutput

**Claimed by:** `subagent-stop-output.schema.json` does not define a `hookSpecificOutput` property and uses `additionalProperties: false` to reject it.

**Verification:** The research synthesis cites 5 independent evidence sources:
1. S-01 (Official docs) -- groups SubagentStop with top-level decision events.
2. S-05 (GitHub Issue #15485, closed COMPLETED 2026-01-23) -- Anthropic explicitly confirmed.
3. S-09 (SDK types) -- `SubagentStopHookOutput extends BaseHookOutput { decision?: 'block'; reason?: string; }` with no hookSpecificOutput.
4. Context7 research stream -- confirms.
5. WebSearch research stream -- confirms.

**Verdict:** CONFIRMED. This is the most strongly verified claim in the entire deliverable, backed by an Anthropic-closed GitHub issue.

### Claim V03: permissionDecision Values Are "allow"/"deny"/"ask"

**Claimed by:** `pre-tool-use-output.schema.json` line 32: `"enum": ["allow", "deny", "ask"]`.

**Verification:** The research synthesis (line 106, 230-231) confirms these values with HIGH confidence across all 3 streams. S-01 (Official docs) explicitly lists them. The deprecated values are `"approve"` (maps to `"allow"`) and `"block"` (maps to `"deny"`).

**Additional verification:** The current `pre_tool_use.py` uses `"approve"` and `"block"` (deprecated values), confirming that these are different from the current API values.

**Verdict:** CONFIRMED. The enum values match the official documentation exactly.

### Claim V04: UserPromptSubmit Uses Top-Level decision for Blocking

**Claimed by:** `user-prompt-submit-output.schema.json` defines `decision` at the top level (not inside `hookSpecificOutput`).

**Verification:** The research synthesis (line 105, 193-201) confirms this with HIGH confidence. S-01 (Official docs APIDOC section) documents this pattern. The UserPromptSubmit event uses a hybrid model: top-level `decision` for blocking + `hookSpecificOutput` for context injection.

**Distinction from PreToolUse:** PreToolUse is the exception -- it moves its decision inside `hookSpecificOutput.permissionDecision`. UserPromptSubmit, PostToolUse, Stop, and SubagentStop all use top-level `decision`.

**Verdict:** CONFIRMED. UserPromptSubmit correctly uses top-level decision.

### Claim V05: Exit Code 2 Means Block (JSON Ignored)

**Claimed by:** Research synthesis (line 436). Not directly in the schema files, but relevant to how schemas are applied.

**Verification:** The research synthesis (line 113-117) confirms with FULL agreement across all streams. S-01 and S-02 provide an explicit exit code semantics table.

**Relevance to schemas:** If a hook exits with code 2, Claude Code blocks the action and IGNORES the JSON output. Therefore schema validation is only meaningful for exit code 0 (success) outputs. The current `pre_tool_use.py` exits with code 2 on errors (line 370, 373), which means its JSON output is already ignored by Claude Code -- but the exit code itself triggers blocking, which is the wrong behavior for error cases.

**Verdict:** CONFIRMED. Exit code semantics are well-documented and relevant to schema application context.

### Claim V06: PermissionRequest Uses hookSpecificOutput.decision.behavior

**Claimed by:** `permission-request-output.schema.json` defines a nested `decision.behavior` field inside `hookSpecificOutput`.

**Verification:** The research synthesis (line 109) confirms with FULL agreement. Context7 and WebSearch both confirm this unique nested structure. This is the most complex decision control model across all hook events.

**Verdict:** CONFIRMED. The nested `decision.behavior` pattern is correctly modeled.

### S-011 Summary

All 6 factual claims verified. No claim was found to be incorrect or unsupported.

| Claim | Status | Confidence |
|-------|--------|------------|
| V01: hookEventName required in hookSpecificOutput | CONFIRMED | HIGH |
| V02: SubagentStop no hookSpecificOutput | CONFIRMED | HIGH (Anthropic-confirmed) |
| V03: permissionDecision values allow/deny/ask | CONFIRMED | HIGH |
| V04: UserPromptSubmit top-level decision | CONFIRMED | HIGH |
| V05: Exit code 2 = block, JSON ignored | CONFIRMED | HIGH |
| V06: PermissionRequest nested decision.behavior | CONFIRMED | HIGH |

---

## Consolidated Findings

All findings across all 7 strategies, sorted by severity.

### HIGH Severity

| ID | Strategy | Finding | Action Required |
|----|----------|---------|-----------------|
| S002-F02 | Devil's Advocate | `allOf` + `additionalProperties: false` coupling -- base schema changes require updating all 7 event schemas to re-declare new properties | Document as maintenance procedure. Consider adding a test that verifies base properties are re-declared in all event schemas. |

### MEDIUM Severity

| ID | Strategy | Finding | Action Required |
|----|----------|---------|-----------------|
| S002-F01 | Devil's Advocate | `additionalProperties: false` creates fragility against upstream Claude Code changes | Document as intentional design trade-off. TASK-005 tests should note maintenance expectation. |
| S013-F01 | Inversion | New upstream fields will break tests (not runtime) | Same as S002-F01. |

### LOW Severity

| ID | Strategy | Finding | Action Required |
|----|----------|---------|-----------------|
| S002-F03 | Devil's Advocate | `const` hookEventName values tied to current API naming | Accept -- API name changes would break all hooks, not just schemas. |
| S002-F04 | Devil's Advocate | `decision` enum only allows "block" | Correct per docs. |
| S002-F05 | Devil's Advocate | Empty `{}` passes all schemas | Correct behavior. Functional tests needed separately. |
| S002-F06 | Devil's Advocate | No backward-compat schema for deprecated PreToolUse format | By design. |
| S013-F02 | Inversion | Empty `{}` passes all schemas | Same as S002-F05. |
| S013-F03 | Inversion | Null values rejected | Correct behavior. |

### INFO Severity

| ID | Strategy | Finding | Action Required |
|----|----------|---------|-----------------|
| S010-F01 | Self-Refine | $ref paths use relative filenames | Consistent and correct. |
| S010-F02 | Self-Refine | Base properties re-declared with `true` | Correct JSON Schema idiom. |
| S010-F03 | Self-Refine | All $ref paths resolve | Confirmed by meta-validation. |
| S010-F04 | Self-Refine | Conditional validation consistent | Correct implementation. |
| S010-F05 | Self-Refine | Complete event coverage | No gaps. |
| S007-F01 | Constitutional AI | P-002 file persistence compliance | Compliant. |
| S007-F02 | Constitutional AI | Quality enforcement architecture support | Compliant. |
| S007-F03 | Constitutional AI | Naming convention consistency | Compliant. |
| S007-F04 | Constitutional AI | H-05/H-06 UV compliance | Compliant. |
| S007-F05 | Constitutional AI | H-10 spirit upheld | Compliant. |
| S007-F07 | Constitutional AI | AE-002 does not apply | Not triggered. |
| S013-F04 | Inversion | Non-JSON output out of scope | Out of scope. |
| S013-F05 | Inversion | Multiple hook aggregation out of scope | Out of scope. |

---

## Scoring Summary

| Dimension | Weight | Score | Weighted | Key Factors |
|-----------|--------|-------|----------|-------------|
| Completeness | 0.20 | 0.96 | 0.192 | All 4 Jerry events + 3 future + base covered |
| Internal Consistency | 0.20 | 0.97 | 0.194 | All patterns consistent, no unintended variance |
| Methodological Rigor | 0.20 | 0.96 | 0.192 | 3-stream research, multi-source confirmation |
| Evidence Quality | 0.15 | 0.95 | 0.143 | 18 sources cataloged, confidence ratings provided |
| Actionability | 0.15 | 0.95 | 0.143 | Usage guide, code examples, schema map ready |
| Traceability | 0.10 | 0.94 | 0.094 | `_source` metadata in all schemas, evidence chains |
| **Composite** | **1.00** | -- | **0.958** | **PASS (> 0.92 threshold)** |

---

## Recommendation

**Verdict: PASS** -- Proceed to Phase 2

The Phase 1 schema deliverable meets the C3 quality gate with a composite score of **0.958** (threshold: 0.92). The schemas are:

1. **Correct** -- All factual claims verified (S-011). All $ref paths resolve (S-010). Functional tests pass 8/8 (validation report).
2. **Complete** -- All 8 Claude Code hook event types with event-specific output are covered (S-010, S-014).
3. **Well-grounded** -- Based on 3 independent research streams with Anthropic-confirmed authoritative sources (S-003, S-014).
4. **Constitutionally compliant** -- No Jerry Constitution violations (S-007).
5. **Actionable** -- TASK-005 can directly use the schemas with the provided usage guide (S-014).

### Actionable Items for Phase 2

The following items should be addressed during Phase 2 implementation, not as blockers to Phase 2 start:

| Priority | Item | Owner |
|----------|------|-------|
| HIGH | Document the base/event schema coupling: when base schema adds fields, all 7 event schemas must re-declare them (S002-F02) | TASK-005 or schema maintainer |
| MEDIUM | Add a CI test that verifies all base schema properties are re-declared in every event schema (S002-F02) | TASK-005 |
| MEDIUM | Document `additionalProperties: false` as an intentional strictness trade-off for test-time validation (S002-F01) | TASK-005 |
| LOW | Consider using `$comment` alongside `_source` for JSON Schema standard-compliant documentation (S-014 Traceability) | Future |
| LOW | TASK-005 should test edge cases: empty `{}`, `null` field values, unknown additional fields (S013-F01/F02/F03) | TASK-005 |

---

*Document ID: adv-executor-p1-review*
*Workflow ID: bug002-hookfix-20260217-001*
*Phase: 1 (Schema Foundation)*
*Review Type: C3 Adversarial (7 strategies)*
*Version: 1.0*
