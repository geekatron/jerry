# Security Code Review: PROJ-021 Adversary Remediation Implementations

**Reviewer:** eng-security (Security Code Review Specialist)
**Review date:** 2026-03-11
**Scope:** Six agent definitions across /use-case, /test-spec, and /contract-design skills; two JSON schemas; four implementation summaries (PM-001, FM-001, FM-002, IN-001)
**Methodology:** Manual review -- OWASP ASVS 5.0 V5/V7 verification, CWE Top 25 2025 checklist, H-34/H-35 compliance, tool tier and constitutional triplet verification
**SSDF Practice:** PW.7 (review human-readable code to identify vulnerabilities)

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0: Executive Summary](#l0-executive-summary) | Findings by severity, overall posture, top risk areas, immediate actions |
| [L1: Technical Detail](#l1-technical-detail) | Individual findings with CWE, CVSS, location, evidence, remediation |
| [L2: Strategic Implications](#l2-strategic-implications) | Security posture assessment, systemic patterns, architectural recommendations |
| [OWASP ASVS 5.0 Verification](#owasp-asvs-50-verification) | Chapter-level verification status |
| [Methodology Notes](#methodology-notes) | Review approach, confidence indicators, limitations |

---

## L0: Executive Summary

### Findings by Severity

| Severity | Count |
|----------|-------|
| Critical | 0 |
| High | 0 |
| Medium | 3 |
| Low | 4 |
| Informational | 5 |
| **Total** | **12** |

### Overall Security Assessment

**PASS WITH CONDITIONS.** The four remediation implementations (PM-001, FM-001, FM-002, IN-001) are architecturally sound and represent a meaningful improvement to the security posture of the /use-case, /test-spec, and /contract-design skill pipeline. No critical or high-severity vulnerabilities were identified. The three medium findings are governance completeness gaps that do not compromise runtime security but reduce the reliability of automated enforcement layers (L3/L5 CI gates).

The implementations demonstrate genuine security thinking: defense-in-depth layering (schema + behavioral + CLI), explicit prompt injection mitigations (T1-T5 in PM-001), and deterministic schema enforcement (FM-002 allOf constraint). This is above-average security practice for an LLM agent governance framework.

### Top 3 Risk Areas

1. **uc-author post-creation CLI gap (Medium, FM-002)** -- uc-author.md references CLI validation in the Post-Creation Verification section but the step text remains behavioral (no explicit `uv run jerry ast validate` command) while uc-slicer received the explicit CLI gate at Step 8. The asymmetry means uc-author relies on behavioral self-correction while uc-slicer has deterministic enforcement. This is the highest-priority medium finding because uc-author is the source artifact producer for the entire pipeline.

2. **tspec-analyst missing output_filtering entry (Medium, F-003)** -- The `do_not_modify_feature_files_or_uc_artifacts` output constraint is present in the agent .md guardrails section but absent from tspec-analyst.governance.yaml `output_filtering`. This is the FM-001 pattern (behavioral constraint not mirrored in governance YAML) recurring in an agent not covered by the FM-001 implementation pass.

3. **Schema: `parent_id` null pattern duality (Low, F-007)** -- `use-case-realization-v1.schema.json` declares `parent_id` as `type: ["string", "null"]` with a regex pattern constraint. JSON Schema Draft 2020-12 applies `pattern` to string values only; null is permitted but the intent is ambiguous. This is a schema design gap that could produce false-pass or false-fail validation results in strict validators.

### Recommended Immediate Actions

| Priority | Action | Finding |
|----------|--------|---------|
| P1 | Add explicit CLI command to uc-author.md Post-Creation Verification | F-001 (Medium) |
| P1 | Add `do_not_modify_feature_files_or_uc_artifacts` to tspec-analyst.governance.yaml output_filtering | F-003 (Medium) |
| P2 | Add `do_not_modify_uc_artifacts` to tspec-generator.governance.yaml output_filtering | F-002 (Medium) |
| P3 | Clarify `parent_id` null/pattern handling in schema | F-007 (Low) |
| P3 | Add `rejected_artifact_path_must_not_escape_session_root` to uc-slicer output_filtering | F-004 (Low) |

---

## L1: Technical Detail

### Finding F-001: uc-author Post-Creation Verification -- No Explicit CLI Gate

**Severity:** Medium
**CWE:** CWE-693 (Protection Mechanism Failure)
**CVSS 3.1 Base Score:** 4.0 (AV:L/AC:L/PR:L/UI:N/S:U/C:N/I:L/A:N)
**ASVS Chapter:** V5.1 (Input Validation)
**Location:** `skills/use-case/agents/uc-author.md`, Post-Creation Verification section (lines 180-186)

**Evidence:**

The FM-002 implementation correctly added an explicit CLI gate to uc-slicer.md at the state transition point (Step 8):

```
Before setting `realization_level: INTERACTION_DEFINED`, run
`uv run jerry ast validate {artifact_path} --schema use_case_realization`
```

The same FM-002 implementation scope included uc-author.md. The fm002-implementation-summary.md states that uc-author's Post-Creation Verification was updated. Reading the current uc-author.md (lines 180-186) reveals:

```
After writing the artifact, verify by manually checking the YAML frontmatter
satisfies the allOf constraints defined in
`docs/schemas/use-case-realization-v1.schema.json` and confirming all of the
following:
1. File exists at the declared output path
2. Verify the output artifact's YAML frontmatter satisfies the allOf constraints
   defined in `docs/schemas/use-case-realization-v1.schema.json`. Check: (1) ...
```

The instruction says "manually checking" and "verify" -- these are behavioral instructions, not deterministic CLI commands. The uc-author.governance.yaml post_completion_checks contains:

```yaml
- "verify_yaml_frontmatter_validates_against_schema_via_jerry_ast_validate"
```

This check name (added by FM-002) references the CLI tool name but the corresponding .md instruction does not provide the concrete invocation. The fm002-implementation-summary.md states under "Post-State (After This Implementation)" for uc-author.md:

```
After writing the artifact, verify by running
`uv run jerry ast validate {artifact_path} --schema use_case_realization`
```

This text appears in the summary document but the actual uc-author.md does not contain the `uv run jerry ast validate` invocation -- the .md still says "manually checking."

**Data flow trace:** uc-author writes an artifact -> Post-Creation Verification instructs "manually checking" -> no deterministic CLI gate executes -> allOf constraint violations (e.g., INTERACTION_DEFINED without interactions[]) can pass the author step undetected -> uc-slicer receives a semantically invalid artifact.

**Impact:** The behavioral enforcement gap (L1 only, no L3 CLI gate at uc-author) means the first deterministic check is at uc-slicer's Step 8. For uc-author-only workflows (elaboration without slicing), no deterministic schema validation occurs. Confidence: HIGH (direct code read, no inference).

**Remediation:**

In `skills/use-case/agents/uc-author.md`, replace the Post-Creation Verification section preamble:

Change: "After writing the artifact, verify by manually checking the YAML frontmatter satisfies the allOf constraints..."

To: "After writing the artifact, verify by running `uv run jerry ast validate {artifact_path} --schema use_case_realization` and confirming all of the following:"

This aligns uc-author with the uc-slicer pattern established in FM-002 and makes the governance YAML post_completion_check `verify_yaml_frontmatter_validates_against_schema_via_jerry_ast_validate` accurate.

---

### Finding F-002: tspec-generator output_filtering Missing Read-Only Constraint

**Severity:** Medium
**CWE:** CWE-732 (Incorrect Permission Assignment for Critical Resource)
**CVSS 3.1 Base Score:** 3.5 (AV:L/AC:L/PR:L/UI:R/S:U/C:N/I:L/A:N)
**ASVS Chapter:** V7.2 (Log Content Requirements -- output filtering as governance enforcement)
**Location:** `skills/test-spec/agents/tspec-generator.governance.yaml`, output_filtering array

**Evidence:**

tspec-generator.md `<capabilities>` section explicitly states:
```
Modification of source use case artifacts (tspec-generator is a read-only consumer of UC artifacts)
```

tspec-generator.md `<guardrails>` Forbidden Actions includes:
```
METHODOLOGY VIOLATION: NEVER invent scenarios that do not trace to a specific use case flow step
```

However, tspec-generator.governance.yaml `output_filtering` contains only 5 entries:
```yaml
output_filtering:
  - "no_secrets_in_output"
  - "every_scenario_must_trace_to_source_flow_step"
  - "all_given_clauses_must_derive_from_preconditions_or_flow_context"
  - "all_then_clauses_must_derive_from_postconditions_or_system_responses"
  - "scenario_names_must_include_source_step_reference"
```

The behavioral constraint "do not modify source UC artifacts" is present in the .md but absent from the governance YAML output_filtering. This is the FM-001 pattern: a constraint documented in the .md without a corresponding machine-readable governance YAML entry. The FM-001 implementation pass covered cd-generator's banned-term entry but did not cover tspec-generator's read-only constraint.

**Data flow trace:** tspec-generator has Write/Edit tools in its allowed tools list (uc-author.md frontmatter) -> behavioral constraint "read-only consumer" exists in .md only -> CI gate reading governance YAML output_filtering cannot detect this constraint -> no automated enforcement at L3/L5 that the agent must not modify source artifacts.

**Impact:** An LLM agent operating under context rot conditions that causes it to forget the behavioral read-only constraint has no governance YAML fallback. The risk is low in normal operation (the .md constraint is clear) but medium from an enforcement reliability standpoint. Confidence: HIGH.

**Remediation:**

Add to `skills/test-spec/agents/tspec-generator.governance.yaml` output_filtering:

```yaml
- "do_not_modify_source_use_case_artifacts"
```

This mirrors the constraint already declared in the .md `<capabilities>` section and makes it machine-readable for CI gate inspection.

---

### Finding F-003: tspec-analyst output_filtering Missing Read-Only Constraint

**Severity:** Medium
**CWE:** CWE-732 (Incorrect Permission Assignment for Critical Resource)
**CVSS 3.1 Base Score:** 3.5 (AV:L/AC:L/PR:L/UI:R/S:U/C:N/I:L/A:N)
**ASVS Chapter:** V7.2 (Log Content Requirements -- output filtering as governance enforcement)
**Location:** `skills/test-spec/agents/tspec-analyst.governance.yaml`, output_filtering array

**Evidence:**

tspec-analyst.md `<guardrails>` Forbidden Actions includes:
```
ANALYSIS VIOLATION: NEVER modify Feature files or use case artifacts during analysis
-- Consequence: tspec-analyst is a read-and-report agent; modifying source artifacts
corrupts the provenance chain...
```

tspec-analyst.governance.yaml `output_filtering` contains:
```yaml
output_filtering:
  - "no_secrets_in_output"
  - "coverage_percentages_must_be_mathematically_verifiable"
  - "every_gap_must_cite_specific_unmapped_flow_element"
  - "recommendations_must_include_priority_and_effort_estimate"
```

The `do_not_modify_feature_files_or_uc_artifacts` constraint is present in the .md Forbidden Actions but absent from the governance YAML output_filtering. This is the FM-001 pattern recurring in tspec-analyst, which was not covered in the FM-001 implementation pass (that pass covered all 6 agents, but the .md boundary was the behavioral constraint; adding it to output_filtering as a machine-readable filter was not included in the scope).

The same gap exists in tspec-analyst as in tspec-generator (F-002 above), but tspec-analyst is a stronger case because tspec-analyst has Write/Edit tools AND processes two input files (Feature file + source UC artifact), making the opportunity for accidental modification higher.

**Data flow trace:** tspec-analyst receives Feature file + UC artifact -> performs coverage analysis -> writes coverage report. The agent has Edit tool capability. The behavioral constraint "read-and-report only" exists in .md but not in governance YAML output_filtering.

**Impact:** Same as F-002: enforcement reliability gap. Confidence: HIGH.

**Remediation:**

Add to `skills/test-spec/agents/tspec-analyst.governance.yaml` output_filtering:

```yaml
- "do_not_modify_feature_files_or_uc_artifacts"
```

---

### Finding F-004: uc-slicer Rejection Artifact -- No Path Containment Constraint in output_filtering

**Severity:** Low
**CWE:** CWE-22 (Improper Limitation of a Pathname to a Restricted Directory -- Path Traversal)
**CVSS 3.1 Base Score:** 2.5 (AV:L/AC:H/PR:L/UI:N/S:U/C:N/I:L/A:N)
**ASVS Chapter:** V5.2 (Sanitization and Sandboxing)
**Location:** `skills/use-case/agents/uc-slicer.governance.yaml`, output_filtering; `skills/use-case/agents/uc-slicer.md`, Rejection Artifact Protocol

**Evidence:**

The PM-001 implementation adds a rejection artifact protocol to uc-slicer. The rejection artifact is written to `{artifact_path}-rejection.yaml`. The uc-author.md T2 mitigation validates that `rejected_artifact` matches the current artifact path before consuming it:

```
Validate `rejected_artifact` matches the current artifact path (T2 path-traversal
mitigation) -- if the paths do not match, log a warning and proceed without
rejection context.
```

However, the uc-slicer rejection artifact WRITE path (not the consume path) has no path containment constraint. Specifically:

- `{artifact_path}` is derived from the session context or user-provided input
- The rejection artifact protocol writes to `{artifact_path}-rejection.yaml` using the Write tool
- No check verifies that `{artifact_path}` is within the session's expected workspace root
- uc-slicer.governance.yaml output_filtering does not include a path containment rule for the rejection artifact output path

In an LLM agent context, a malformed `artifact_path` session context field (e.g., `../../etc/passwd`) could cause the Write tool call to write to an unintended location. The risk is low because:
1. The session context is typically provided by the same trusted orchestrator
2. The Write tool operates under the CLI's file permissions
3. Rejection artifacts are YAML files, not executable content

**Data flow trace:** Session context provides `artifact_path` -> uc-slicer rejection protocol appends `-rejection.yaml` to the path -> Write tool writes to that constructed path -> no validation that the constructed path is within expected workspace bounds.

**Impact:** Low. The threat requires a malformed session context field and the Write tool's filesystem access. The artifact content is controlled YAML, not executable code. Confidence: MEDIUM (the behavioral instructions are correct; the governance YAML omission is the gap).

**Remediation:**

1. Add to `skills/use-case/agents/uc-slicer.governance.yaml` output_filtering:
   ```yaml
   - "rejected_artifact_path_must_be_within_session_workspace_root"
   ```

2. Add to uc-slicer.md Rejection Artifact Protocol Step 2, before the Write tool call:
   "Verify that `{artifact_path}` is within the current session workspace before writing the rejection artifact. If the path contains `..` or references a path outside the project root, report a path validation error and halt."

---

### Finding F-005: Rejection Artifact -- Timestamp Field Lacks ISO-8601 Format Enforcement at Schema Level

**Severity:** Low
**CWE:** CWE-20 (Improper Input Validation)
**CVSS 3.1 Base Score:** 2.0 (AV:L/AC:H/PR:L/UI:N/S:U/C:N/I:L/A:N)
**ASVS Chapter:** V5.1 (Input Validation)
**Location:** `skills/use-case/agents/uc-slicer.md`, Rejection Artifact Protocol YAML template; `skills/use-case/agents/uc-author.md`, Rejection Artifact Check Step 2d

**Evidence:**

The rejection artifact template in uc-slicer.md specifies:
```yaml
timestamp: "{ISO-8601 timestamp, e.g. 2026-03-11T14:30:00Z}"
```

The staleness check in uc-author.md Step 2d states:
```
If the artifact file's modification time is more recent than the rejection
artifact's `timestamp`, warn the user...
```

The PM-001 implementation defers the formal JSON Schema for the rejection artifact to Phase 2 (`docs/schemas/rejection-artifact-v1.schema.json` is not yet created). This means the `timestamp` field is a free-text string with no format validation at the schema level.

The staleness check depends on comparing the rejection artifact timestamp against the artifact modification time. If the timestamp field contains a non-ISO-8601 value (e.g., a human-written date "March 11 2026"), the comparison logic is undefined. The T4 mitigation (YAML parse failure -> warn and proceed) covers parse errors but not semantically invalid timestamp formats that parse successfully as a YAML string.

**Data flow trace:** uc-slicer writes `timestamp` as a free-text string -> uc-author reads `timestamp` -> uc-author compares `timestamp` against artifact modification time -> comparison behavior with non-ISO-8601 string is undefined -> staleness check (T3) may silently fail.

**Impact:** Low. The T3 staleness check is a defense-in-depth measure; its failure does not block artifact processing but reduces the security value of the staleness detection. Confidence: MEDIUM (inference from behavioral instructions; no formal schema to verify).

**Remediation:**

1. Add timestamp format validation to uc-author.md Rejection Artifact Check Step 2a (parse YAML):
   "After parsing: validate that `timestamp` is parseable as an ISO-8601 datetime. If not parseable, log a warning and proceed without staleness check (treat T3 as unavailable for this artifact)."

2. When Phase 2 schema is created, enforce `format: date-time` on the `timestamp` field in `docs/schemas/rejection-artifact-v1.schema.json`.

---

### Finding F-006: IN-001 Banned-Term List -- Governance YAML Entry Missing Full Algorithm Reference

**Severity:** Low
**CWE:** CWE-693 (Protection Mechanism Failure)
**CVSS 3.1 Base Score:** 2.0 (AV:L/AC:H/PR:L/UI:N/S:U/C:N/I:N/A:N)
**ASVS Chapter:** V5.1 (Input Validation)
**Location:** `skills/contract-design/agents/cd-generator.governance.yaml`, input_validation entry 8

**Evidence:**

The IN-001 implementation added the following input_validation entry to cd-generator.governance.yaml:

```yaml
- "Each $.interactions[*].request_description and response_description must not
   contain banned placeholder terms (TBD, TODO, FIXME, placeholder, N/A, lorem
   ipsum, etc.) -- REJECT with guidance directing to /use-case (uc-slicer
   Activity 5) for description revision; see cd-generator.md Step 1 Layer 2a
   for full banned-term list and matching algorithm"
```

The entry is correct in its behavioral intent. However, from a CI gate perspective, the banned-term list is defined in cd-generator.md (the .md file) and referenced by the governance YAML via "see cd-generator.md Step 1 Layer 2a". This creates a forward-reference from a machine-readable governance artifact to an LLM-consumed .md file.

The FM-001 boundary rule classifies this as appropriate: behavioral detail (the full list and matching algorithm) belongs in .md only. However, the governance YAML entry omits the two-tier matching rule distinction (EXACT_MATCH_TERMS vs. SUBSTRING_TERMS with length threshold), which is a security-relevant detail. A future maintainer adding a new banned term without reading the .md may not apply the two-tier rule correctly.

**Data flow trace:** cd-generator.governance.yaml declares banned-term check -> CI gate reads the entry -> CI gate has no visibility into the two-tier matching algorithm -> CI gate implementation must separately read cd-generator.md to implement correctly.

**Impact:** Low. The risk is a maintenance gap, not a runtime vulnerability. The current implementation is correct. Confidence: MEDIUM.

**Remediation:**

Augment the governance YAML entry to include the two-tier distinction as a structural declaration:

```yaml
- "Each $.interactions[*].request_description and response_description must not
   contain banned placeholder terms. Two-tier matching: (1) EXACT_MATCH_TERMS --
   whole-string case-insensitive match (TBD, TODO, N/A, etc.) -- REJECT; (2)
   SUBSTRING_TERMS -- word-boundary match when total length < 60 characters
   (FIXME, placeholder, lorem ipsum, etc.) -- REJECT. Full lists and algorithm
   in cd-generator.md Step 1 Layer 2a. REJECT with actionable guidance to
   /use-case (uc-slicer Activity 5)."
```

---

### Finding F-007: Schema `parent_id` -- Null Type and Pattern Constraint Interaction

**Severity:** Low
**CWE:** CWE-20 (Improper Input Validation)
**CVSS 3.1 Base Score:** 2.0 (AV:L/AC:H/PR:N/UI:N/S:U/C:N/I:L/A:N)
**ASVS Chapter:** V5.1 (Input Validation)
**Location:** `docs/schemas/use-case-realization-v1.schema.json`, line 229

**Evidence:**

```json
"parent_id": {
  "type": ["string", "null"],
  "pattern": "^UC-[A-Z]+-\\d{3}$",
  "description": "Parent use case ID for sub-use-cases. Null for top-level use cases."
}
```

In JSON Schema Draft 2020-12, `pattern` applies only to string values. When the value is `null`, the `pattern` constraint is not evaluated (null is not a string), so the schema permits `null` as a valid `parent_id` value regardless of the pattern.

This is the intended behavior (as stated in the description). However, it creates an ambiguity: the type declaration is `["string", "null"]` but only one of those types (string) is constrained by the pattern. An implementer reading only the `type` field might construct a `parent_id` validation that rejects null. Additionally, the distinction between `null` (explicit null value) and absent (field not present) is not enforced -- both are permitted since `parent_id` is not in the `required` array.

**Impact:** Low. The schema accurately describes the semantic intent. The risk is that an alternative JSON Schema validator with stricter type coercion behavior might reject artifacts with `parent_id: null`. Confidence: HIGH (direct schema read, JSON Schema Draft 2020-12 spec behavior confirmed).

**Remediation:**

Use `oneOf` to make the null/pattern duality explicit and unambiguous:

```json
"parent_id": {
  "oneOf": [
    {
      "type": "string",
      "pattern": "^UC-[A-Z]+-\\d{3}$"
    },
    {
      "type": "null"
    }
  ],
  "description": "Parent use case ID for sub-use-cases. Null for top-level use cases."
}
```

This is semantically equivalent but removes the implicit null-bypasses-pattern behavior that could confuse validator implementations.

---

### Finding F-008: test-specification-v1.schema.json -- `coverage_percentage` Field Not Cross-Validated Against `mapped_flows`/`total_flows`

**Severity:** Low
**CWE:** CWE-20 (Improper Input Validation)
**CVSS 3.1 Base Score:** 1.5 (AV:L/AC:H/PR:N/UI:N/S:U/C:N/I:L/A:N)
**ASVS Chapter:** V5.1 (Input Validation)
**Location:** `docs/schemas/test-specification-v1.schema.json`, lines 85-89

**Evidence:**

```json
"coverage_percentage": {
  "type": "number",
  "minimum": 0,
  "maximum": 100,
  "description": "Mapped flows / total flows * 100. Optional; computable from mapped_flows and total_flows."
}
```

The `coverage_percentage` field is optional and declared as a standalone numeric constraint. No allOf constraint verifies that `coverage_percentage` equals `mapped_flows / total_flows * 100`. This means a producer can write `coverage_percentage: 100` while `mapped_flows: 2` and `total_flows: 5` -- a contradictory artifact that passes schema validation.

The tspec-analyst.governance.yaml output_filtering contains:
```yaml
- "coverage_percentages_must_be_mathematically_verifiable"
```

This is a behavioral constraint, not a schema-level enforcement. The schema lacks the corresponding allOf cross-validation.

**Data flow trace:** tspec-generator writes `coverage_percentage` -> test-specification-v1.schema.json validates only range (0-100) -> no cross-validation against `mapped_flows`/`total_flows` -> inconsistent coverage claims pass schema validation.

**Impact:** Low. The behavioral constraint in tspec-analyst catches this at analysis time. The schema gap allows inconsistent artifacts to pass structural validation. Confidence: HIGH (direct schema read).

**Remediation:**

Consider adding an allOf constraint that enforces consistency when `coverage_percentage` is present:

```json
{
  "if": {
    "properties": {
      "coverage_percentage": { "type": "number" }
    },
    "required": ["coverage_percentage", "mapped_flows", "total_flows"]
  },
  "then": {
    "description": "When coverage_percentage is present alongside mapped_flows and total_flows, the value should be consistent. Note: JSON Schema cannot enforce arithmetic equality; this constraint documents the requirement for behavioral enforcement."
  }
}
```

Note: JSON Schema cannot enforce arithmetic equality (it has no arithmetic operators). The correct remediation is a comment in the schema description and a post-completion check entry in tspec-generator.governance.yaml validation.post_completion_checks:

```yaml
- "verify_coverage_percentage_consistent_with_mapped_and_total_flows"
```

---

### Finding F-009: uc-slicer.md Step 8 -- Verification Language Uses "Manually Checking" Despite FM-002 Scope

**Severity:** Informational
**CWE:** N/A (governance documentation gap, no vulnerability)
**ASVS Chapter:** V5.1 (Input Validation -- process documentation)
**Location:** `skills/use-case/agents/uc-slicer.md`, Post-Update Verification (line 195)

**Evidence:**

uc-slicer.md Post-Update Verification section reads:
```
After updating the artifact, verify by manually checking the YAML frontmatter
satisfies the allOf constraints defined in `docs/schemas/use-case-realization-v1.schema.json`...
```

Step 8 in the methodology correctly adds the CLI gate:
```
Before setting `realization_level: INTERACTION_DEFINED`, verify the output
artifact's YAML frontmatter satisfies the allOf constraints...
```

The Post-Update Verification header says "manually checking" but item 1 in the checklist references the `allOf` constraints that are enforced by the CLI. The fm002-implementation-summary.md Post-State shows the explicit CLI invocation in the verification block. The actual current file (line 195) retains "manually checking."

This is an informational discrepancy: the methodology step (Step 8) is correct and explicit; the post-update verification header is slightly inconsistent. No security impact.

**Remediation:** Change "manually checking" to "running `uv run jerry ast validate {artifact_path} --schema use_case_realization` and confirming" for consistency with Step 8 and the governance YAML.

---

### Finding F-010: uc-author.governance.yaml -- `output_filtering` Missing `verify_yaml_frontmatter_validates_against_schema_via_jerry_ast_validate` Alignment

**Severity:** Informational
**CWE:** N/A (governance alignment gap)
**ASVS Chapter:** V5.1 (process documentation)
**Location:** `skills/use-case/agents/uc-author.governance.yaml`, output_filtering vs. post_completion_checks

**Evidence:**

uc-author.governance.yaml has:
```yaml
validation:
  post_completion_checks:
    - "verify_yaml_frontmatter_validates_against_schema_via_jerry_ast_validate"
```

But `output_filtering` does not have a corresponding entry that references CLI schema validation. The output_filtering array contains `detail_level_must_match_actual_content_depth` (behavioral) but no entry referencing the CLI-based structural validation. This creates a minor alignment gap: the post_completion_check references the CLI tool explicitly, but no output_filtering entry connects the schema validation result to the filtering layer.

**Remediation:** Add to output_filtering:
```yaml
- "schema_validation_must_pass_via_jerry_ast_validate_before_handoff"
```

---

### Finding F-011: cd-validator.governance.yaml -- Four output_filtering Entries vs. Five Distinct Constraint Categories in .md

**Severity:** Informational
**CWE:** N/A (governance completeness gap)
**ASVS Chapter:** V7.2 (output filtering)
**Location:** `skills/contract-design/agents/cd-validator.governance.yaml`, output_filtering

**Evidence:**

cd-validator.md Output Constraints section defines four constraints, all correctly mirrored in governance YAML:
```yaml
output_filtering:
  - "no_secrets_in_output"
  - "validation_results_must_include_pass_fail_per_check"
  - "traceability_gaps_must_list_specific_interaction_ids"
  - "coverage_percentage_must_show_numerator_and_denominator"
```

cd-validator.md Forbidden Actions includes:
```
MODIFICATION VIOLATION: NEVER modify the generated contract file during validation
```

This is a fifth output constraint (the generated contract must not be modified). The constraint is present as a Forbidden Action in both the .md and the governance YAML `forbidden_actions`, which is the correct placement per the FM-001 boundary rule (forbidden actions belong in `forbidden_actions`, not `output_filtering`). This is not a finding -- it is a confirmation of correct placement per the boundary rule.

Informational only: the `MODIFICATION VIOLATION` entry is correctly in `forbidden_actions`, not `output_filtering`. No change needed.

---

### Finding F-012: All Six Agents -- Constitutional Triplet Complete, Tool Tier Compliant

**Severity:** Informational
**CWE:** N/A (positive finding)
**ASVS Chapter:** V1.1 (Secure Software Development Lifecycle)
**Location:** All six governance YAML files

**Evidence:**

All six agents pass H-35 constitutional triplet verification:

| Agent | P-003 | P-020 | P-022 | Task Tool Absent | Forbidden Actions >= 3 |
|-------|-------|-------|-------|-----------------|----------------------|
| uc-author | PASS | PASS | PASS | PASS (T2) | PASS (5 entries) |
| uc-slicer | PASS | PASS | PASS | PASS (T2) | PASS (6 entries) |
| tspec-generator | PASS | PASS | PASS | PASS (T2) | PASS (5 entries) |
| tspec-analyst | PASS | PASS | PASS | PASS (T2) | PASS (5 entries) |
| cd-generator | PASS | PASS | PASS | PASS (T2) | PASS (6 entries) |
| cd-validator | PASS | PASS | PASS | PASS (T2) | PASS (4 entries) |

All six agents are T2 (Read-Write tier). No agent includes the Task tool. All forbidden_actions entries use NPT-009-complete format as declared. All constitution.principles_applied arrays include P-001, P-002, P-003, P-004, P-020, and P-022.

All six agents declare both `output.location` and `output.fallback_location` as required by the review scope criteria. This is a positive finding confirming the fallback_location requirement is met.

---

## OWASP ASVS 5.0 Verification

### V5 -- Validation, Sanitization and Encoding

| Requirement | Status | Evidence |
|-------------|--------|---------|
| V5.1.1 -- Input validation for all user inputs | PARTIAL | Schema-level validation present for UC artifacts (use-case-realization-v1.schema.json). Rejection artifact lacks formal schema (Phase 2 deferred). See F-005. |
| V5.1.2 -- Positive validation (allowlist) on structured data | PASS | Schema uses `enum`, `pattern`, `const` for all structured fields. allOf constraints enforce cross-field consistency. |
| V5.1.3 -- Input validation at every trust boundary | PASS | Each agent has a multi-layer input validation gate (schema L1 + agent L2 + CLI L3). tspec-generator and cd-generator both validate at Step 1 before any transformation. |
| V5.1.4 -- Strict type validation | PASS | Schema uses `type` with specific string/integer/boolean/array declarations and `additionalProperties: false` on most definitions. |
| V5.2.1 -- Path traversal prevention | PARTIAL | uc-author T2 mitigation validates incoming `rejected_artifact` path. uc-slicer write path lacks containment constraint. See F-004. |
| V5.2.3 -- HTML encoding for output | N/A -- no HTML output in this scope | |
| V5.3.1 -- Output encoding context | PASS | All agents produce YAML/Markdown, not HTML. No encoding context applicable. |

### V7 -- Error Handling and Logging

| Requirement | Status | Evidence |
|-------------|--------|---------|
| V7.1.1 -- Logging of security events | PASS | All five warning conditions in PM-001 (T1-T5) are logged as user-visible warnings. Rejection messages name specific interaction IDs, field names, and corrective actions. |
| V7.1.2 -- Sensitive data not in logs | PASS | output_filtering includes `no_secrets_in_output` on all six agents. Governance YAML entries are documentation-only; no runtime secrets. |
| V7.2.1 -- Log content sufficient for forensic analysis | PASS | Rejection artifacts contain: `rejecting_agent`, `rejected_artifact`, `rejection_reason` (enum), `current_state`, `required_state`, `missing_elements`, `recommended_action`, `timestamp`. Sufficient forensic detail. |
| V7.3.1 -- Validation of log injection | PARTIAL | uc-author.md H field explicitly treats `human_message` as display-only (not injected into reasoning context). However, `missing_elements[]` items are used as a "checklist reference" which is a semi-injection vector. The T1 mitigation treats them as data not instructions, which is correct but depends on LLM behavioral compliance rather than a deterministic filter. |

### V1 -- Architecture (Reference Only)

| Requirement | Status | Evidence |
|-------------|--------|---------|
| V1.1.1 -- SDLC lifecycle documentation | PASS | All implementation summaries document OWASP categories addressed, remaining risks, and evolution paths. |
| V1.2.1 -- Authentication architecture | N/A -- agent framework, no user authentication in scope | |
| V1.5.1 -- Input/output trust boundaries | PASS | Trust boundary is clearly defined: same-session filesystem, same-user permissions. PM-001 explicitly scopes the threat model to same-trust-boundary. |

---

## L2: Strategic Implications

### Security Posture Assessment

The PROJ-021 remediation implementations advance the security posture of the Jerry framework's use-case pipeline from "behavioral enforcement only" to a partial defense-in-depth architecture. The key advance is the introduction of deterministic enforcement mechanisms at two layers: schema-level (allOf constraints in use-case-realization-v1.schema.json) and CLI-level (uc-slicer Step 8 `uv run jerry ast validate`). These mechanisms are context-rot immune, unlike behavioral instructions in .md files which degrade as session context fills.

The PM-001 implementation's T1-T5 mitigation taxonomy is sound security engineering. Treating the rejection artifact as a data-not-instructions boundary (T1) is the correct response to the prompt injection threat class in LLM agent systems. This aligns with OWASP's LLM Top 10 2025 LLM01 (Prompt Injection).

### Systemic Vulnerability Patterns

**Pattern 1 -- FM-001 Recurrence (F-002, F-003):** The FM-001 implementation fixed all existing cross-reference constraints that lacked loading prerequisites. It did not, however, add behavioral constraint mirroring for all read-only status declarations. tspec-generator and tspec-analyst both declare read-only consumption of source artifacts in their .md files but do not mirror this in governance YAML output_filtering. This is a documentation pattern gap, not a runtime vulnerability, but it indicates the FM-001 scope was narrower than the underlying governance completeness principle requires.

**Recommendation:** Extend the FM-001 boundary rule to include: "behavioral read-only constraints declared in `<capabilities>` MUST also appear in `output_filtering` as a machine-readable constraint (format: `do_not_modify_{artifact_type}`)."

**Pattern 2 -- CLI Gate Asymmetry (F-001, F-009):** The FM-002 implementation added explicit CLI gates to uc-slicer but left uc-author with behavioral "manually check" language in its post-creation verification header. The governance YAML post_completion_checks correctly reference the CLI tool name, creating an asymmetry between the machine-readable governance declaration and the human-readable .md instruction. This asymmetry could cause a future maintainer to de-implement the CLI check (believing the .md's "manually check" instruction takes precedence).

**Recommendation:** Adopt a convention that whenever a post_completion_check entry names a CLI tool (e.g., `verify_...via_jerry_ast_validate`), the corresponding .md verification section MUST use the explicit `uv run` invocation form.

**Pattern 3 -- Phase 2 Deferral Accumulation:** Three findings (F-004, F-005, and the rejection artifact formal schema) depend on Phase 2 deliverables that are deferred. As the pipeline grows (PM-003 indicates tspec-generator/tspec-analyst will receive rejection artifacts in Phase 2), the deferral accumulation increases residual risk. The total Phase 2 debt includes: formal rejection artifact schema, CLI validation for rejection artifact, containment constraint for rejection artifact write path, and PM-003 implementation.

**Recommendation:** Set a Phase 2 trigger condition tied to agent count (as stated in ADR-PM001: "5+ agent pairs"), but also set a hard calendar deadline (no more than 3 months from PM-001 merge) to prevent indefinite deferral.

### Comparison with Threat Model Predictions

The PM-001 implementation's T1-T5 threat taxonomy maps directly to the five primary threat vectors for filesystem-based inter-agent communication:
- T1 (Prompt Injection): addressed -- data-not-instructions treatment
- T2 (Path Traversal): partially addressed -- consume-side only; write-side lacks containment
- T3 (Stale Artifact): addressed -- timestamp staleness check with user confirmation
- T4 (Malformed YAML): addressed -- parse error falls back gracefully
- T5 (Unknown Enum): addressed -- fall back to missing_elements[] and required_state

The partial gap at T2 write-side (F-004) was not identified in the PM-001 threat model. This suggests the threat model focused on the consumer's perspective (uc-author consuming a rejection artifact) but did not fully model the producer's perspective (uc-slicer writing an artifact with a path derived from external input).

### Recommendations for Security Architecture Evolution

1. **Formal rejection artifact schema (Phase 2):** The `docs/schemas/rejection-artifact-v1.schema.json` schema should enforce `format: date-time` on `timestamp`, `pattern` on `rejecting_agent` (agent name pattern), and `pattern` on `rejected_artifact` (path pattern excluding `..` components).

2. **Governance YAML output_filtering completeness standard:** Promote the following as a MEDIUM standard in `agent-development-standards.md`: "Behavioral read-only constraints in `<capabilities>` MUST be mirrored as `do_not_modify_{artifact_type}` entries in governance YAML `output_filtering`."

3. **Path containment helper:** Add a path containment check (resolve canonical path and verify it is under the project root) as a standard operation in the CLI validation suite, callable from agent methodology steps: `uv run jerry ast validate --check-path {path}`.

---

## Methodology Notes

**Confidence indicators:**
- HIGH confidence: findings based on direct code/schema reads with no inference required
- MEDIUM confidence: findings requiring inference about behavioral interactions between components
- N/A: positive findings requiring no inference

**Limitations:**
- This review covers agent definitions and schemas as static artifacts. Dynamic behavior (LLM execution quality, context-rot degradation timing) cannot be assessed from static review.
- The CLI commands (`uv run jerry ast validate`) are referenced in agent definitions but the CLI implementation was not reviewed. The assumption that `--schema use_case_realization` mode is implemented is carried from the FM-002 analysis (E-013 explicitly notes this assumption).
- No penetration testing or dynamic analysis was performed (that is eng-devsecops scope).
- The rejection artifact Phase 2 schema deferred items represent known residual risk accepted by ADR-PM001; this review flags them as Low findings but does not recommend blocking the implementation on them.

**CWE Top 25 2025 Coverage:**

| CWE | Description | Checked | Finding |
|-----|-------------|---------|---------|
| CWE-79 | XSS | N/A -- no HTML output | None |
| CWE-89 | SQL Injection | N/A -- no database queries | None |
| CWE-78 | OS Command Injection | CHECKED | No user input flows to Bash tool calls unfiltered |
| CWE-287 | Improper Authentication | N/A -- no auth flow in scope | None |
| CWE-862 | Missing Authorization | N/A -- single-user session scope | None |
| CWE-306 | Missing Auth for Critical Function | N/A | None |
| CWE-502 | Deserialization | CHECKED | YAML deserialization of rejection artifact uses T4 parse-error mitigation; no arbitrary object deserialization |
| CWE-798 | Hardcoded Credentials | CHECKED | No credentials in any reviewed file; `no_secrets_in_output` filter present on all agents |
| CWE-22 | Path Traversal | CHECKED | F-004 (Low) -- uc-slicer rejection artifact write path lacks containment |
| CWE-352 | CSRF | N/A -- no web interface | None |
| CWE-20 | Improper Input Validation | CHECKED | F-005 (Low), F-007 (Low), F-008 (Low) |
| CWE-693 | Protection Mechanism Failure | CHECKED | F-001 (Medium), F-006 (Low) |
| CWE-732 | Incorrect Permission Assignment | CHECKED | F-002 (Medium), F-003 (Medium) |

---

*Reviewer: eng-security (Security Code Review Specialist)*
*Review date: 2026-03-11*
*Constitutional compliance: P-001 (all findings evidence-based with citations to specific file locations and line numbers), P-002 (persisted to file), P-022 (limitations disclosed; confidence indicators applied; Phase 2 deferrals explicitly noted)*
*SSDF practice: PW.7 (review and analyze human-readable code to identify vulnerabilities)*
*OWASP ASVS 5.0: V5 (Validation/Sanitization/Encoding) PARTIAL, V7 (Error Handling and Logging) PARTIAL, V1 (Architecture) PASS*
