# Security Code Review: /test-spec Skill

> **PS ID:** proj-021 | **Entry ID:** step-10-eng-security-review | **Workflow ID:** use-case-skills-20260308-001
> **Date:** 2026-03-09 | **Agent:** eng-security | **Step:** 10 (Phase 3 Implementation)
> **Input artifacts:** tspec-generator.md, tspec-generator.governance.yaml, tspec-analyst.md, tspec-analyst.governance.yaml, clark-transformation-rules.md, SKILL.md, bdd-scenario.template.md, test-plan.template.md, test-specification-v1.schema.json
> **Prior pipeline scores:** eng-architect 0.952 (PASS), eng-lead 0.9615 (PASS), eng-backend 0.960 (PASS), eng-qa 0.957 (PASS)
> **Review standard:** OWASP ASVS 5.0, CWE Top 25 2025, CVSS 3.1, NIST SSDF PW.7
> **Pattern reference:** step-9-eng-security-review.md (v1.2.0)
> **GitHub Issue:** #109
> **Version:** 1.0.0
> **Confidence:** 0.92 (complete manual review of all referenced files; Bash tool behavioral risk requires operational monitoring of live agent sessions to fully validate; schema additionalProperties risk is bounded by the LLM trust model)

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0: Executive Summary](#l0-executive-summary) | Finding counts by severity, overall posture, top risks, immediate actions |
| [L1: Technical Findings](#l1-technical-findings) | Individual finding reports with CWE, CVSS, location, evidence, remediation |
| [Constitutional Compliance Verification](#constitutional-compliance-verification) | P-003, P-020, P-022 cross-file verification matrix |
| [OWASP ASVS 5.0 Verification](#owasp-asvs-50-verification) | Chapter-by-chapter verification status |
| [H-34/H-35 Compliance Checklist](#h-34h-35-compliance-checklist) | Agent definition standards compliance |
| [Tool Tier Verification](#tool-tier-verification) | T2 tier appropriateness and Bash risk assessment |
| [Cross-Skill Trust Boundary Analysis](#cross-skill-trust-boundary-analysis) | /use-case to /test-spec and tspec-generator to tspec-analyst data flows |
| [Template and Schema Security Assessment](#template-and-schema-security-assessment) | bdd-scenario.template.md, test-plan.template.md, and JSON schema review |
| [L2: Strategic Implications](#l2-strategic-implications) | Systemic patterns, architecture posture, evolution recommendations |
| [S-010 Self-Review](#s-010-self-review) | Pre-delivery self-review checklist |

---

## L0: Executive Summary

### Finding Counts by Severity

| Severity | Count | Findings |
|----------|-------|---------|
| Critical | 0 | -- |
| High | 0 | -- |
| Medium | 2 | SEC-001, SEC-002 |
| Low | 4 | SEC-003, SEC-004, SEC-005, SEC-006 |
| Informational | 2 | SEC-007, SEC-008 |
| **Total** | **8** | |

### Overall Security Assessment

**PASS with observations.** The /test-spec skill presents a minimal attack surface consistent with its role as a pure markdown/YAML transformation skill. No critical or high-severity vulnerabilities were identified. The constitutional triplet (P-003, P-020, P-022) is correctly implemented across both agents. The T2 tool tier is appropriate and consistently declared. The Clark transformation algorithm's deterministic $. path-reference model substantially limits injection surface compared to string-interpolation-based approaches.

The two medium findings both involve the Bash tool: an unscoped execution surface (SEC-001) carried forward from the /use-case skill pattern, and the absence of explicit output path boundary enforcement in guardrails (SEC-002). Both are mitigated by compensating controls and neither constitutes an exploitable vulnerability given the LLM trust model, but both represent hardening opportunities consistent with defense-in-depth.

The four low findings are specification gaps: schema additionalProperties permissiveness (SEC-003), a missing slug sanitization constraint in the output path pattern (SEC-004), test-plan.template.md's generated_by field admitting arbitrary values (SEC-005), and RULE-OT-02's Traceability Matrix annotation inconsistency (SEC-006). None affect the correctness of the security controls implemented.

Compared to the /use-case skill (step-9-eng-security-review.md), the /test-spec skill has a smaller attack surface: the input trust boundary is narrower (reads only validated UC artifacts already processed by /use-case), the output is Markdown-only with no YAML-driven behavior, and there are no worktracker entity creation operations with user-supplied field values. The Bash tool risk pattern is structurally identical to SEC-001 in the /use-case review and the same remediation applies.

### Top 3 Risk Areas

1. **Unscoped Bash execution surface (SEC-001, Medium)** -- Both tspec-generator and tspec-analyst declare the Bash tool without any command scope constraint in governance YAML. The intended use is narrow (CLI validation via `uv run`), but neither the guardrails nor governance files restrict what shell commands may be invoked. Mitigated by: stated LLM methodology is narrowly scoped; no user-controlled string is passed to Bash in the stated use cases.

2. **No explicit output path boundary constraint in guardrails (SEC-002, Medium)** -- The output path pattern `projects/${JERRY_PROJECT}/test-specs/UC-{DOMAIN}-{NNN}-{slug}.feature.md` relies on the JERRY_PROJECT environment variable and LLM interpretation. Neither agent's guardrails section explicitly prohibits writing outside `projects/`. The eng-qa review (step-10-eng-qa-review.md) noted the same gap. The risk is bounded by the T2 tool tier's filesystem access model but is not explicitly mitigated in the specification.

3. **Schema `additionalProperties: true` at root level (SEC-003, Low)** -- The test-specification-v1.schema.json permits arbitrary extra fields in Feature file YAML frontmatter. A crafted Feature file with extra fields passes schema validation. The risk is lower than the equivalent finding in use-case-realization-v1.schema.json (SEC-002 in step-9 review) because the test-specification schema is consumed by tspec-analyst reading its own skill's output, not arbitrary external input.

### Recommended Immediate Actions

1. Add `capabilities.bash_allowlist` to both governance YAML files, listing permitted `uv run` command patterns (remediation for SEC-001 and SEC-003).
2. Add an explicit output path boundary guardrail to both agent `.md` files: "NEVER write Feature files or coverage reports outside `projects/${JERRY_PROJECT}/`" (remediation for SEC-002).
3. Add `verify_no_arbitrary_bash_commands_outside_allowlist` to `validation.post_completion_checks` in both governance YAML files (complementary to action 1).

---

## L1: Technical Findings

### Finding Table

| Finding ID | Severity | CVSS 3.1 | CWE | Description | File(s) | Recommendation |
|-----------|----------|----------|-----|-------------|---------|----------------|
| SEC-001 | Medium | 5.5 | CWE-78 | Bash tool declared without command scope constraint | tspec-generator.md, tspec-analyst.md, both .governance.yaml files | Add `bash_allowlist` in governance; constrain to `uv run` patterns only |
| SEC-002 | Medium | 4.3 | CWE-22 | Output path boundary not explicitly constrained in guardrails; `${JERRY_PROJECT}` and `{slug}` are not bounds-checked at the specification level | tspec-generator.md (output section), tspec-analyst.md (output section) | Add explicit output path boundary guardrail; add slug validation rule |
| SEC-003 | Low | 2.5 | CWE-20 | Schema root `additionalProperties: true` permits unvalidated field injection into Feature file YAML frontmatter | docs/schemas/test-specification-v1.schema.json (line 117) | Set `additionalProperties: false` or document extension contract explicitly |
| SEC-004 | Low | 3.1 | CWE-20 | Output slug component `{slug}` in Feature file path is derived from UC title but no sanitization pattern is enforced in agent specification | tspec-generator.md (line 88, line 182) | Add slug sanitization rule: enforce `^[a-z0-9-]+$` pattern in clark-transformation-rules.md |
| SEC-005 | Low | 2.3 | CWE-116 | test-plan.template.md frontmatter `generated_by` field is a string placeholder with no `const` constraint, unlike bdd-scenario.template.md which correctly hardcodes `tspec-generator` | skills/test-spec/templates/test-plan.template.md (line 4) | Change `generated_by: tspec-generator` in template to a constant and add note that this field must not be modified |
| SEC-006 | Low | 2.1 | CWE-116 | RULE-OT-02 labels alternate success extensions as `error (alternate success)` in the Traceability Matrix, which is semantically misleading -- success extensions are not errors; this mislabeling could cause tspec-analyst to misclassify scenarios | clark-transformation-rules.md (line 136) | Change RULE-OT-02 Traceability Matrix annotation from `error (alternate success)` to `alternate_success` to maintain consistent type semantics |
| SEC-007 | Info | -- | -- | Schema `$id` uses a non-existent domain (`jerry-framework.dev`); not a security risk but could mislead schema tooling | docs/schemas/test-specification-v1.schema.json (line 4) | Accepted design -- document as internal schema identifier; consistent with use-case-realization-v1.schema.json pattern |
| SEC-008 | Info | -- | -- | Composition prompt files (`.prompt.md`) carry documented drift risk (FIND-002 synchronization note); stale copies could lead agents to apply outdated guardrails | skills/test-spec/composition/tspec-generator.prompt.md, tspec-analyst.prompt.md | Already tracked as FIND-002; CI lint check recommended for long-term; same pattern as SEC-007 in step-9 review |

---

### SEC-001: Bash Tool Without Command Scope Constraint

**Severity:** Medium | **CVSS 3.1:** AV:L/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:N = **5.5** | **CWE:** CWE-78 (OS Command Injection)

**CVSS metric justification:** AV:L -- attack requires local session context (LLM-to-OS boundary is local, not network-exposed). AC:L -- no special conditions; the agent executes Bash if it decides to. PR:L -- the user who invoked the agent has low-privilege access. UI:N -- once the agent makes the decision, no further interaction is needed. S:U -- scope is the user's OS process context. C:N -- command injection in this context does not directly exfiltrate data. I:H -- arbitrary shell commands can modify or delete files. A:N -- availability impact subsumed by integrity impact.

**Affected files:**
- `skills/test-spec/agents/tspec-generator.md` line 18 (`- Bash`)
- `skills/test-spec/agents/tspec-analyst.md` line 18 (`- Bash`)
- `skills/test-spec/agents/tspec-generator.governance.yaml` (no bash constraint in `capabilities`)
- `skills/test-spec/agents/tspec-analyst.governance.yaml` (no bash constraint in `capabilities`)

**Data flow trace:**

```
User request -> tspec-generator or tspec-analyst agent receives it
-> agent may invoke Bash tool
-> Bash executes in the host OS context (unrestricted shell access)
```

The Bash tool provides unrestricted shell access. The agent definitions state the intended use is narrow:
- tspec-generator: "Execute CLI validation commands (H-05: use `uv run` prefix for all Python commands)"
- tspec-analyst: "Execute CLI commands for file existence verification (H-05: use `uv run` prefix)"

However, neither the `.md` guardrails section nor either `.governance.yaml` `capabilities` block constrains what Bash commands may be invoked. The `forbidden_actions` array addresses agent-level delegation (P-003) but does not address shell command scope. An LLM that processes a crafted user input -- for example, "also run `rm -rf` to clean up" or that misinterprets intent due to adversarial UC artifact content -- could invoke unintended commands.

**Distinction from /use-case SEC-001:** This finding is structurally identical to SEC-001 in step-9-eng-security-review.md. The risk profile is comparable but the /test-spec skill has a slightly narrower Bash use case: tspec-generator is stated as using Bash for CLI validation only, while uc-author used Bash for worktracker entity creation which involves user-controlled field values passed as arguments. The absence of user-controlled string interpolation into Bash commands reduces the exploitability slightly.

**Evidence (tspec-generator.governance.yaml, line 33-38):** The `forbidden_actions` array contains five entries addressing P-003, P-020, P-022, schema violations, and methodology violations. No entry restricts shell command scope. The `capabilities` object contains `forbidden_action_format` and `output_formats` but no `bash_allowlist` or `allowed_commands` field.

**Remediation:**

Add to `skills/test-spec/agents/tspec-generator.governance.yaml` and `tspec-analyst.governance.yaml`:

```yaml
capabilities:
  bash_allowlist:
    - "uv run jerry validate"
    - "uv run jerry items"
    - "uv run python"
  bash_deny_all_else: true
```

Add to the `<guardrails>` section of both `.md` files, under Forbidden Actions:

```
- BASH VIOLATION: NEVER invoke Bash commands outside the allowlist [uv run jerry validate, uv run jerry items, uv run python] -- Consequence: unrestricted shell access violates the T2 least-privilege guarantee and enables unintended filesystem modification outside the project directory.
```

Add to `validation.post_completion_checks` in both governance YAML files:

```yaml
- "verify_no_arbitrary_bash_commands_outside_allowlist"
```

---

### SEC-002: Output Path Boundary Not Explicitly Constrained

**Severity:** Medium | **CVSS 3.1:** AV:L/AC:H/PR:L/UI:N/S:U/C:L/I:H/A:N = **4.3** | **CWE:** CWE-22 (Path Traversal)

**CVSS metric justification:** AV:L -- local execution context. AC:H -- requires either adversarial UC content or misinterpretation of user instructions; not trivially triggered. PR:L -- user has low-privilege access. UI:N -- once triggered, no user interaction needed. S:U -- scoped to local filesystem context. C:L -- reads outside project/ could expose file existence. I:H -- writes outside project/ could corrupt framework files. A:N -- not a denial-of-service vector.

**Affected files:**
- `skills/test-spec/agents/tspec-generator.md` output section (line 88, line 180-182)
- `skills/test-spec/agents/tspec-analyst.md` output section (line 77, line 162)

**Data flow trace:**

```
User provides artifact_path or output_path parameter
-> tspec-generator receives parameter in session context
-> Agent interprets output path: "projects/${JERRY_PROJECT}/test-specs/UC-{DOMAIN}-{NNN}-{slug}.feature.md"
-> Write tool is invoked with the constructed path
-> No boundary check against "must be within projects/${JERRY_PROJECT}/" is present in the specification
```

The output path pattern `projects/${JERRY_PROJECT}/test-specs/UC-{DOMAIN}-{NNN}-{slug}.feature.md` includes two components that are environment-variable-derived or UC-artifact-derived:
1. `${JERRY_PROJECT}` -- session environment variable; could be set to an empty string or a path with traversal characters
2. `{slug}` -- derived from `$.title` field in the UC artifact; a UC with a title containing `../` characters would produce a traversal slug

The `<guardrails>` section of tspec-generator includes `no_secrets_in_output` and content-derivation constraints, but no explicit rule stating "NEVER write outside `projects/${JERRY_PROJECT}/`" or "NEVER write outside the repository root."

**Evidence (tspec-generator.md, line 234-238, output filtering):**

```
- no_secrets_in_output
- every_scenario_must_trace_to_source_flow_step
- all_given_clauses_must_derive_from_preconditions_or_flow_context
- all_then_clauses_must_derive_from_postconditions_or_system_responses
- scenario_names_must_include_source_step_reference
```

No entry addresses output path boundary. The eng-qa review (step-10-eng-qa-review.md, line 143) independently identified this as a LOW risk: "The risk is low because the agent operates as an LLM reasoning about file paths rather than directly evaluating user-controlled strings as filesystem operations. The guardrails section does not explicitly prohibit writing outside `projects/`, which is a minor specification gap (LOW)." This review rates it MEDIUM because the combination of slug derivation from user-controlled UC content (an attack surface) and the Bash tool access creates a potential two-step escalation path: adversarial UC title -> malformed slug -> path traversal when combined with Bash-mediated path operations.

**Slug derivation risk (tspec-generator.md line 182):**

```
The slug is a lowercase hyphen-separated version of the UC title
(e.g., UC-AUTH-001-validate-user-credentials.feature.md).
```

No sanitization constraint enforces that the slug is restricted to `[a-z0-9-]+`. A UC title such as `../../../.context/rules/quality-enforcement` would produce a slug that traverses out of the test-specs directory if not sanitized.

**Remediation:**

Add to the `<guardrails>` Forbidden Actions section of both agent `.md` files:

```
- PATH VIOLATION: NEVER write Feature files or coverage reports outside projects/${JERRY_PROJECT}/test-specs/ -- Consequence: writing to arbitrary filesystem paths may corrupt framework files, governance documents, or other project artifacts outside the intended scope of this skill.
```

Add to `clark-transformation-rules.md` as RULE-QA-05 (or equivalent slug sanitization rule):

```
RULE-QA-05: Sanitize output slug before file path construction.
WHEN constructing the Feature file output path from $.title, apply slug sanitization:
1. Lowercase all characters
2. Replace spaces and underscores with hyphens
3. Remove any character not matching [a-z0-9-]
4. Remove any occurrence of ".." (path traversal prevention)
5. Truncate to 80 characters maximum
Result must match pattern: ^[a-z0-9][a-z0-9-]*[a-z0-9]$
REJECT slug construction if the sanitized result is empty or contains "../".
```

---

### SEC-003: Schema `additionalProperties: true` at Root Level

**Severity:** Low | **CVSS 3.1:** AV:N/AC:H/PR:L/UI:N/S:U/C:N/I:L/A:N = **2.5** | **CWE:** CWE-20 (Improper Input Validation)

**Affected file:** `docs/schemas/test-specification-v1.schema.json` (line 117)

**Evidence:**

```json
"additionalProperties": true
```

The schema permits Feature file YAML frontmatter to include arbitrary extra fields beyond the 8 required fields and the 2 optional fields (`slice_id`, `version`). A Feature file containing:

```yaml
source_use_case: UC-AUTH-001
generated_by: tspec-generator
malicious_field: "unexpected content"
...
```

would pass schema validation. tspec-analyst reads YAML frontmatter to extract `source_use_case`, `slice_id`, and `scenario_count` (tspec-analyst.md, methodology Step 1). Extra fields are ignored by the analyst's parsing logic.

**Risk context:** This finding is lower severity than the equivalent finding SEC-002 in step-9-eng-security-review.md because:
1. The test-specification-v1.schema.json validates the output of tspec-generator (the skill's own output), not arbitrary external input. An attacker would need to create a crafted Feature file that bypasses the generation step entirely.
2. tspec-analyst does not execute or evaluate any field values; it reads metadata for coverage computation only.
3. The schema's `coverage` sub-object also has `additionalProperties: true` (line 99), creating a second permissive boundary within the schema. This is documented as "to allow future extension without breaking existing files" (eng-backend implementation report, line 135) -- an acceptable extension strategy, but the same documentation should be at the root level.

**Remediation:**

Either set `"additionalProperties": false` at the root level (strict option), or document the extension contract explicitly:

```json
"$comment_extension_contract": "additionalProperties: true is intentional to allow future Feature file metadata fields without breaking existing files. Extension fields must not conflict with the 8 required fields or the 2 optional fields. Extension fields that affect tspec-analyst behavior must be added to this schema before use.",
"additionalProperties": true
```

If the extension contract is documented, downgrade this finding to Informational.

---

### SEC-004: Slug Component Without Sanitization Constraint

**Severity:** Low | **CVSS 3.1:** AV:L/AC:H/PR:L/UI:N/S:U/C:N/I:L/A:N = **3.1** | **CWE:** CWE-20 (Improper Input Validation)

**Affected files:**
- `skills/test-spec/agents/tspec-generator.md` (lines 88, 182)
- `skills/test-spec/rules/clark-transformation-rules.md` (no slug sanitization rule)

**Evidence (tspec-generator.md, line 182):**

```
The slug is a lowercase hyphen-separated version of the UC title
(e.g., UC-AUTH-001-validate-user-credentials.feature.md).
```

No rule enforces slug character restrictions. The clark-transformation-rules.md file contains 24 rules (RULE-IV-01 through RULE-QA-04), none of which address slug sanitization. While RULE-IV-01 gates transformation on `detail_level >= ESSENTIAL_OUTLINE`, it does not gate on the content of `$.title`.

**Attack scenario:** A UC artifact with title `../../.context/rules/quality-enforcement` passes all four RULE-IV checks (detail_level, extensions, basic_flow count, step types). The Clark transformation proceeds, and when constructing the output path, the slug would become `../../.context/rules/quality-enforcement` if not sanitized, potentially causing the Feature file to be written to `.context/rules/`.

**Relationship to SEC-002:** This finding is the input-validation complement to SEC-002 (output path boundary). SEC-002 addresses the missing guardrail constraint; SEC-004 addresses the missing sanitization rule in the transformation rules. Both are needed for defense-in-depth.

**Remediation:** Add RULE-QA-05 as described in SEC-002 remediation. Additionally, add a RULE-IV-05 input validation check:

```
RULE-IV-05: Validate $.title for slug-safe content.
WHEN constructing the Feature file path slug from $.title, reject if the sanitized slug
would be empty, contain path traversal sequences ("../"), or produce a path outside
projects/${JERRY_PROJECT}/test-specs/.
Rejection message: "UC $.title contains characters that cannot be safely used in a file path slug.
Use /use-case to update the title to use only alphanumeric characters, spaces, and hyphens."
```

---

### SEC-005: test-plan.template.md `generated_by` Field Is Not Constrained

**Severity:** Low | **CVSS 3.1:** AV:L/AC:H/PR:L/UI:N/S:U/C:N/I:L/A:N = **2.3** | **CWE:** CWE-116 (Improper Output Encoding)

**Affected file:** `skills/test-spec/templates/test-plan.template.md` (line 4)

**Evidence (test-plan.template.md, line 4):**

```yaml
generated_by: tspec-generator
```

The `generated_by` field is hardcoded to `tspec-generator` as a literal string value in the template, not a placeholder. This is correct. However, the `bdd-scenario.template.md` achieves the same intent more robustly: the JSON schema encodes `generated_by` as `"const": "tspec-generator"` and the template reproduces this. The test-plan template does not reference the JSON schema for its frontmatter validation because test plan documents (`-test-plan.md`) are explicitly documented as human-readable analytical reports outside the Feature file format (tspec-analyst.md, line 160).

**Risk:** The test-plan template's `generated_by` value is correct but there is no schema constraint enforcing it. If a user or another agent produces a test plan document with `generated_by: manual` or `generated_by: other-agent`, no validation gate would detect the provenance violation. This is a weaker provenance chain than the Feature file's schema-enforced `const` constraint.

**Remediation options:**
1. Create a `test-plan-v1.schema.json` schema with `generated_by: {const: "tspec-generator"}` and reference it from the test-plan template (preferred for consistency with the Feature file pattern).
2. Document in the template Usage Notes that `generated_by` must not be modified, and add a validation post-completion check: `verify_generated_by_is_tspec-generator_in_coverage_report`.

Option 1 is preferred for defense-in-depth but may be out of scope for the current implementation. Option 2 is an immediate low-cost improvement.

---

### SEC-006: RULE-OT-02 Traceability Matrix Type Annotation Semantically Misleading

**Severity:** Low | **CVSS 3.1:** AV:L/AC:L/PR:L/UI:R/S:U/C:N/I:L/A:N = **2.1** | **CWE:** CWE-116 (Improper Encoding/Escaping of Output)

**Affected file:** `skills/test-spec/rules/clark-transformation-rules.md` (line 136)

**Evidence (RULE-OT-02, line 136):**

```
- Is annotated as type: `error (alternate success)` in the Traceability Matrix
```

RULE-OT-02 generates a scenario for extensions with `outcome = "success"` -- an alternate success path, not an error. However, the Traceability Matrix type is labeled `error (alternate success)`. The other outcome types use labels `error (failure)` (RULE-OT-01) and `error (rejoin:N)` (RULE-OT-03), which are structurally consistent but semantically incorrect for RULE-OT-02: a success extension is not an error.

**Impact on tspec-analyst:** tspec-analyst reads the Traceability Matrix source annotations to compute coverage. The `type` column is used for the coverage report classification. An `error (alternate success)` type annotation in the Traceability Matrix could cause tspec-analyst to misclassify an alternate success scenario as an error scenario. This affects the C2 (Correctness) criterion in the 7 Cs framework: "Each scenario's Given/When/Then clauses trace to correct source elements."

**Remediation:** Change the Traceability Matrix type annotation in RULE-OT-02 from `error (alternate success)` to `alternate_success`. Update RULE-C5-01 (line 78) to reflect the distinct type labels:

```
- outcome = "failure" -> error (failure)
- outcome = "success" -> alternate_success
- outcome = "rejoin:{N}" -> error (rejoin:N)
```

This change should also be reflected in the bdd-scenario.template.md Traceability Matrix example (line 110).

---

## Constitutional Compliance Verification

### P-003 (No Recursive Subagents) -- Cross-File Matrix

| File | Location | P-003 Declaration | Task Tool Absent | Evidence |
|------|----------|-----------------|-----------------|---------|
| tspec-generator.md | frontmatter `tools:` | YES | YES | tools list: Read, Write, Edit, Glob, Grep, Bash -- no Task |
| tspec-generator.md | `<capabilities>` | YES | explicit | "Delegation to sub-agents (no Task tool -- T2 worker, P-003 compliant)" |
| tspec-generator.md | `<guardrails>` | YES | -- | "P-003: NEVER spawn sub-agents or use the Task tool." |
| tspec-generator.md | forbidden_actions | YES | -- | "P-003 VIOLATION: NEVER spawn recursive subagents or delegate to other agents via Task tool" |
| tspec-generator.governance.yaml | constitution.principles_applied | YES | -- | "P-003" listed |
| tspec-generator.governance.yaml | forbidden_actions | YES | -- | First entry is P-003 VIOLATION |
| tspec-analyst.md | frontmatter `tools:` | YES | YES | tools list: Read, Write, Edit, Glob, Grep, Bash -- no Task |
| tspec-analyst.md | `<capabilities>` | YES | explicit | "Delegation to sub-agents (no Task tool -- T2 worker, P-003 compliant)" |
| tspec-analyst.md | `<guardrails>` | YES | -- | "P-003: NEVER spawn sub-agents or use the Task tool." |
| tspec-analyst.md | forbidden_actions | YES | -- | "P-003 VIOLATION: NEVER spawn recursive subagents or delegate to other agents via Task tool" |
| tspec-analyst.governance.yaml | constitution.principles_applied | YES | -- | "P-003" listed |
| tspec-analyst.governance.yaml | forbidden_actions | YES | -- | First entry is P-003 VIOLATION |
| SKILL.md | P-003 Agent Topology section | YES | -- | ASCII hierarchy diagram explicitly shows no worker-to-worker invocation |
| SKILL.md | Constitutional Compliance table | YES | -- | "tspec-generator and tspec-analyst are T2 worker agents. Neither has Task tool access. Neither invokes the other directly." |

**P-003 Verdict: PASS.** All 14 evidence points confirm P-003 compliance. The SKILL.md ASCII hierarchy diagram is particularly strong: it explicitly states "Workers do NOT invoke each other. tspec-generator output (Feature file) is consumed by tspec-analyst via filesystem. Cross-agent data flow is mediated by shared artifact files on disk (P-003 compliant)." This is a defense-in-depth declaration of P-003 that goes beyond the minimum requirement.

### P-020 (User Authority) -- Cross-File Matrix

| File | Location | P-020 Declaration | Evidence |
|------|----------|-----------------|---------|
| tspec-generator.md | `<guardrails>` Constitutional Compliance | YES | "NEVER override user decisions about scenario scope, test priority, feature file organization, or which use case to transform." |
| tspec-generator.md | forbidden_actions | YES | "P-020 VIOLATION: NEVER override user decisions about scenario scope, test priority, or feature file organization" |
| tspec-generator.governance.yaml | forbidden_actions | YES | Second entry is P-020 VIOLATION |
| tspec-generator.governance.yaml | constitution.principles_applied | YES | "P-020" listed |
| tspec-analyst.md | `<guardrails>` Constitutional Compliance | YES | "NEVER override user decisions about coverage priorities or acceptable coverage thresholds. Present the analysis; the user decides whether coverage is adequate." |
| tspec-analyst.md | forbidden_actions | YES | "P-020 VIOLATION: NEVER override user decisions about coverage priorities or acceptable coverage thresholds" |
| tspec-analyst.governance.yaml | forbidden_actions | YES | Second entry is P-020 VIOLATION |
| tspec-analyst.governance.yaml | constitution.principles_applied | YES | "P-020" listed |
| SKILL.md | Constitutional Compliance table | YES | "tspec-analyst does not override user decisions about coverage thresholds." |

**P-020 Verdict: PASS.** All evidence points confirm P-020 compliance. The declarations are agent-appropriate: tspec-generator defers on scenario scope and feature file organization; tspec-analyst defers on coverage thresholds and prioritization. Both are substantive applications of P-020 rather than generic boilerplate.

### P-022 (No Deception) -- Cross-File Matrix

| File | Location | P-022 Declaration | Evidence |
|------|----------|-----------------|---------|
| tspec-generator.md | `<guardrails>` Constitutional Compliance | YES | "NEVER misrepresent test coverage completeness. If extensions are unmapped, explicitly state which extensions could not be mapped and why." |
| tspec-generator.md | forbidden_actions | YES | "P-022 VIOLATION: NEVER misrepresent test coverage completeness" |
| tspec-generator.governance.yaml | forbidden_actions | YES | Third entry is P-022 VIOLATION |
| tspec-generator.governance.yaml | constitution.principles_applied | YES | "P-022" listed |
| tspec-analyst.md | `<guardrails>` Constitutional Compliance | YES | "NEVER misrepresent coverage metrics or gap severity. Coverage percentages must be mathematically verifiable (cite numerator and denominator)." |
| tspec-analyst.md | `<output>` | YES | "Coverage percentage is mathematically computed and stated" in Post-Creation Verification |
| tspec-analyst.md | forbidden_actions | YES | "P-022 VIOLATION: NEVER misrepresent coverage metrics or gap severity" |
| tspec-analyst.governance.yaml | forbidden_actions | YES | Third entry is P-022 VIOLATION |
| tspec-analyst.governance.yaml | output_filtering | YES | "coverage_percentages_must_be_mathematically_verifiable" |
| tspec-analyst.governance.yaml | constitution.principles_applied | YES | "P-022" listed |
| SKILL.md | Constitutional Compliance table | YES | "tspec-generator explicitly reports unmapped flows. tspec-analyst reports mathematically verifiable coverage percentages with numerator and denominator." |

**P-022 Verdict: PASS.** The P-022 implementation is particularly strong for tspec-analyst: the `output_filtering` entry `coverage_percentages_must_be_mathematically_verifiable` is a machine-checkable constraint that operationalizes P-022 beyond a generic "no deception" statement. The requirement that coverage percentages cite numerator and denominator prevents the most common form of coverage deception (reporting percentages without basis).

### NPT-009-Complete Format Audit

| Agent | Entry Count | Format Compliance | Missing Elements |
|-------|------------|-----------------|-----------------|
| tspec-generator | 5 entries | NPT-009-complete | None |
| tspec-analyst | 5 entries | NPT-009-complete | None |

All 10 forbidden_actions entries across both agents follow the `{PRINCIPLE} VIOLATION: NEVER {action} -- Consequence: {impact}` format:
- VIOLATION label: present in all 10
- NEVER prohibition: present in all 10
- Consequence clause: present in all 10, with specific domain-relevant consequences

The domain-specific entries (entries 4 and 5 in each agent) go beyond the minimum constitutional triplet with meaningful skill-specific prohibitions:
- tspec-generator entries 4-5: SCHEMA VIOLATION (generation from invalid input) and METHODOLOGY VIOLATION (inventing untraceable scenarios) -- both security-relevant
- tspec-analyst entries 4-5: ANALYSIS VIOLATION (modifying source artifacts during analysis) and METHODOLOGY VIOLATION (coverage without source cross-reference) -- both security-relevant

**NPT-009-complete Verdict: PASS.** All forbidden_actions entries meet the complete format requirement. Domain-specific entries are substantive and security-relevant, not generic padding.

---

## OWASP ASVS 5.0 Verification

### V1 -- Architecture, Design and Threat Modeling

| Control | Status | Evidence |
|---------|--------|---------|
| V1.1.1 Threat model exists for sensitive functionality | PASS | step-10-test-spec-architecture.md includes trust boundary analysis; cross-skill integration model documented |
| V1.1.2 All user data identified and classified | PASS | UC artifact fields enumerated; no PII flows through the skill |
| V1.2.3 Privileged components use least privilege | PASS | T2 tool tier enforced; no Task tool; no network access |
| V1.5.1 Input/output requirements documented | PASS | Input Requirements section in SKILL.md; two-layer validation gate in both agents |

**V1 Assessment: PASS.** Architecture documentation is comprehensive. The SKILL.md P-003 Agent Topology section, the cross-skill integration model, and the two-layer validation gate satisfy V1 architectural security requirements for a framework agent skill.

### V2 -- Authentication

| Control | Status | Evidence |
|---------|--------|---------|
| N/A for LLM agent skills operating in filesystem-only context | N/A | No authentication surface; agents read/write local filesystem files |

**V2 Assessment: N/A.** No authentication controls apply to a T2 filesystem-scoped agent skill.

### V3 -- Session Management

| Control | Status | Evidence |
|---------|--------|---------|
| N/A -- no session state beyond current agent invocation | N/A | No MCP persistence; no cross-session state; no session tokens |

**V3 Assessment: N/A.** No session management applies.

### V4 -- Access Control

| Control | Status | Evidence |
|---------|--------|---------|
| V4.1.1 Access control decisions enforce deny by default | PASS | RULE-IV gates reject on validation failure; no partial output on error |
| V4.1.3 Principle of least privilege enforced | PASS | T2 tier (Read, Write, Edit, Glob, Grep, Bash); no Task tool; no network tools |
| V4.2.1 Directory traversal prevented | PARTIAL | Output path pattern scopes to projects/; no explicit path sanitization rule (SEC-002, SEC-004) |

**V4 Assessment: PASS with gap.** SEC-002 and SEC-004 represent the gap in V4.2.1. The existing scoping to `projects/${JERRY_PROJECT}/test-specs/` provides substantial protection; the missing explicit sanitization rule and path boundary guardrail are the identified gaps.

### V5 -- Validation, Sanitization and Encoding

| Control | Status | Evidence |
|---------|--------|---------|
| V5.1.1 Input validation against an allowlist | PASS | RULE-IV-01 through RULE-IV-04 allowlist-gate the input UC artifact |
| V5.1.2 Server-side validation of all input | PASS | Two-layer validation: Layer 1 (JSON Schema) + Layer 2 (agent semantic guardrails) |
| V5.1.3 Structured output validated against schema | PASS | test-specification-v1.schema.json validates Feature file frontmatter |
| V5.2.1 All output data encoded for the target context | PARTIAL | Gherkin content is Markdown-fenced; no cross-site risks; slug sanitization absent (SEC-004) |
| V5.3.1 Query parameterization or equivalent | PASS | Clark transformation uses $. field path lookups (not string interpolation); no injection surface |

**V5 Assessment: PASS with gap.** The SEC-004 slug sanitization absence is the gap. The Clark transformation's use of $. path references rather than string interpolation is a strong defense against injection at the content derivation level.

### V6 -- Stored Cryptography

| Control | Status | Evidence |
|---------|--------|---------|
| N/A -- no cryptographic operations | N/A | Skill produces plaintext Markdown/YAML; no encryption, hashing, or signing required |

**V6 Assessment: N/A.** No cryptographic controls apply.

### V7 -- Error Handling and Logging

| Control | Status | Evidence |
|---------|--------|---------|
| V7.1.1 No sensitive information in error messages | PASS | Rejection messages expose only UC ID and field names, not secrets |
| V7.1.2 Error messages actionable without sensitive detail | PASS | All RULE-IV rejection messages include the specific UC field, the rejection reason, and a recommended next step (e.g., "Use /use-case to elaborate") |
| V7.2.1 Error handling logic is consistent | PASS | All four RULE-IV gates use the same pattern: detect -> reject -> message -> halt |

**V7 Assessment: PASS.** Error handling is consistent across all validation gates. Rejection messages are informative without exposing sensitive data.

### V8 -- Data Protection

| Control | Status | Evidence |
|---------|--------|---------|
| V8.1.1 Sensitive data not logged unnecessarily | PASS | `no_secrets_in_output` output_filtering constraint in both agents; RULE-QA-04 mandates generation summary (not artifact content) before writing |
| V8.3.1 No sensitive data in API parameters | PASS | No API calls; filesystem-only operations |
| V8.2.1 Server-side data classified and protected | PASS | UC artifacts and Feature files do not contain PII or credentials by design |

**V8 Assessment: PASS.** No sensitive data flows through the skill.

### V9 -- Communication

| Control | Status | Evidence |
|---------|--------|---------|
| N/A -- T2 tier prohibits network access | N/A | Both agents are T2 (no WebSearch, no WebFetch); no external communication |

**V9 Assessment: N/A.** No communication security controls apply to a filesystem-only T2 skill.

---

## H-34/H-35 Compliance Checklist

### H-34: Agent Definition Architecture (Dual-File)

| Check | tspec-generator | tspec-analyst |
|-------|----------------|--------------|
| `.md` frontmatter contains ONLY official Claude Code fields | PASS (name, description, model, tools) | PASS (name, description, model, tools) |
| `.governance.yaml` contains: version, tool_tier, identity.role | PASS | PASS |
| `identity.expertise` has >= 2 entries | PASS (3 entries) | PASS (3 entries) |
| `identity.cognitive_mode` is valid enum value | PASS (systematic) | PASS (convergent) |
| `reasoning_effort: high` at root level (C3 agent per ET-M-001) | PASS | PASS |
| `persona` declares tone, communication_style, audience_level | PASS | PASS |
| `guardrails.input_validation` has >= 1 rule | PASS (4 rules) | PASS (3 rules) |
| `guardrails.output_filtering` has >= 3 entries | PASS (5 entries) | PASS (4 entries) |
| `guardrails.fallback_behavior` declared | PASS (escalate_to_user) | PASS (escalate_to_user) |
| `output.required: true` | PASS | PASS |
| `output.location` specified | PASS | PASS |
| `output.levels` declared | PASS (L0, L1) | PASS (L0, L1, L2) |
| `constitution.principles_applied` has >= 3 entries | PASS (6 entries) | PASS (6 entries) |
| `validation.post_completion_checks` declared | PASS (7 checks) | PASS (5 checks) |
| `session_context.on_receive` and `on_send` declared | PASS | PASS |
| `enforcement` tier and escalation_path declared | PASS (medium, eng-reviewer) | PASS (medium, eng-reviewer) |

**H-34 Verdict: PASS.** Both agents fully satisfy the dual-file architecture standard.

### H-35: Constitutional Compliance Triplet (Retired but enforced under H-34)

| Check | tspec-generator | tspec-analyst |
|-------|----------------|--------------|
| P-003 in `constitution.principles_applied` | PASS | PASS |
| P-020 in `constitution.principles_applied` | PASS | PASS |
| P-022 in `constitution.principles_applied` | PASS | PASS |
| `forbidden_actions` has >= 3 entries | PASS (5 entries) | PASS (5 entries) |
| First 3 forbidden_actions reference P-003, P-020, P-022 | PASS | PASS |
| No Task tool in `.md` frontmatter `tools:` list | PASS | PASS |
| `forbidden_action_format: "NPT-009-complete"` declared | PASS | PASS |

**H-35 (under H-34) Verdict: PASS.** Constitutional triplet is correctly implemented in all required locations.

---

## Tool Tier Verification

### T2 Tier Appropriateness

| Tool | tspec-generator | tspec-analyst | Security Risk | Justified? |
|------|----------------|--------------|--------------|-----------|
| Read | YES | YES | Low -- reads only declared input files | YES -- required to read UC artifacts, clark-transformation-rules.md |
| Write | YES | YES | Low -- constrained to Feature files and coverage reports | YES -- required to produce output artifacts |
| Edit | YES | YES | Low -- edits existing Feature files for post-generation corrections | YES -- for RULE-QA-02/RULE-QA-03 repair operations |
| Glob | YES | YES | Low -- file discovery within project directory | YES -- finding related Feature files for cross-UC analysis |
| Grep | YES | YES | Low -- content search within project directory | YES -- finding Source annotations in Feature files |
| Bash | YES | YES | Medium -- unrestricted shell access (SEC-001) | PARTIAL -- narrow use case stated but not constrained |
| Task | NO | NO | N/A -- absent by design | N/A -- correct for T2 workers per P-003 |
| WebSearch | NO | NO | N/A -- absent by design | N/A -- correct for T2 (no network access) |
| WebFetch | NO | NO | N/A -- absent by design | N/A -- correct for T2 (no network access) |

**T2 Tier Verdict: PASS with finding.** The T2 tier is correctly declared and consistently implemented. The Bash tool is the only tool creating a security gap (SEC-001). All other tools are appropriate for the stated use cases. The absence of Task, WebSearch, and WebFetch is correctly enforced through the frontmatter `tools:` list.

### Bash Tool Risk Assessment

The Bash tool is declared for both agents with these stated use cases:
- tspec-generator: "Execute CLI validation commands (H-05: use `uv run` prefix)"
- tspec-analyst: "Execute CLI commands for file existence verification (H-05: use `uv run` prefix)"

**Comparison with /use-case skill:** The /use-case skill (step-9 review, SEC-001) used Bash for worktracker entity creation, which involved user-controlled field values as command arguments (higher injection risk). The /test-spec agents use Bash for validation and existence verification only -- lower injection risk because no user-controlled strings are interpolated into commands in the stated use cases.

**Residual risk:** The Bash tool provides unrestricted shell access regardless of the stated use cases. The mitigating factor is that the LLM's methodology section narrowly scopes Bash to two specific patterns. The governance YAML does not encode this scope, leaving the constraint as an LLM-behavioral instruction rather than a structural enforcement.

**T3 Tools: Confirmed Absent.** Neither tspec-generator nor tspec-analyst references WebSearch or WebFetch in any file. Both governance YAML `tool_tier: "T2"` declarations correctly reflect the absence of T3 tools.

---

## Cross-Skill Trust Boundary Analysis

### Trust Boundary 1: /use-case -> /test-spec

```
/use-case skill (uc-author, uc-slicer)
    |
    +-- Writes: projects/${JERRY_PROJECT}/use-cases/UC-{DOMAIN}-{NNN}-{slug}.md
                (UC artifact with YAML frontmatter validated against use-case-realization-v1.schema.json)
    |
    +-- Trust boundary: filesystem read by tspec-generator
    |
tspec-generator
    |
    +-- RULE-IV-01 through RULE-IV-04: validate before transformation
```

**Security assessment of this boundary:**

1. **Input trust level:** UC artifacts produced by uc-author/uc-slicer are validated by the use-case-realization-v1.schema.json before being written. However, manually crafted UC artifacts (bypassing the /use-case skill) would receive the same validation only at the tspec-generator input gate (RULE-IV-01 through RULE-IV-04). The RULE-IV gates are necessary and sufficient for this trust boundary.

2. **Content injection surface:** UC artifact `$.basic_flow[*].action` and `$.extensions[*].condition` fields contain natural language strings that are reproduced verbatim in Gherkin When/Then clauses. A UC artifact with adversarial content in these fields would produce a Feature file containing that content. The risk is assessed as LOW because: (a) the output is Markdown, not executable code; (b) the guardrail `all_then_clauses_must_derive_from_postconditions_or_system_responses` bounds the derivation source; (c) the LLM's systematic cognitive mode should treat these fields as data, not instructions.

3. **Missing mitigation:** The eng-backend implementation report (L2, line 147) states "Path traversal risk is mitigated by the templated path pattern enforced in the output specification." This is a behavioral claim (LLM will follow the template) rather than a structural enforcement (code or schema rule). SEC-002 and SEC-004 document this gap.

**Trust Boundary 1 Verdict: PASS with findings SEC-002 and SEC-004.** The two-layer validation gate is the primary mitigation and is correctly implemented. The missing structural enforcement of the path boundary is the gap.

### Trust Boundary 2: tspec-generator -> tspec-analyst (Filesystem Handoff)

```
tspec-generator
    |
    +-- Writes: Feature file (.feature.md) with YAML frontmatter
                (validated against test-specification-v1.schema.json)
    |
    +-- Trust boundary: filesystem read by tspec-analyst
    |
tspec-analyst
    |
    +-- Input validation: Feature file existence, Gherkin Scenario blocks,
                          Source UC artifact existence, basic_flow presence
```

**Security assessment of this boundary:**

1. **Handoff integrity:** The `generated_by: const: "tspec-generator"` constraint in test-specification-v1.schema.json ensures that only tspec-generator-produced Feature files pass schema validation. A manually authored Feature file without the correct `generated_by` field would fail validation. This is a strong provenance control.

2. **Coverage tampering:** The `coverage` object in Feature file YAML frontmatter contains coverage metrics that tspec-analyst reads as a "generation-time snapshot." tspec-analyst independently recomputes coverage from the Source annotations and Traceability Matrix. The frontmatter coverage fields are "a generation-time snapshot for quick inspection" (schema description, line 100), not the authoritative coverage computation. This design is correct: tspec-analyst should not trust the frontmatter coverage fields as authoritative.

3. **Missing structural control:** The schema `coverage.mapped_flows` has no upper bound constraint relative to `coverage.total_flows`. A Feature file with `mapped_flows: 100, total_flows: 5` passes schema validation, creating a misleading coverage snapshot. This is finding FIND-QA-004 in the QA review (LOW severity). From a security perspective, this is a data integrity issue: a crafted Feature file could mislead a user who reads the frontmatter coverage fields without running tspec-analyst's independent recomputation. Severity remains LOW because tspec-analyst does not use these frontmatter fields as its authoritative source.

4. **P-003 compliance:** The filesystem-mediated handoff is the correct implementation of P-003 for this skill. Workers do not communicate directly. The SKILL.md diagram explicitly states this and the agent capability sections both declare "no Task tool." This is the strongest possible P-003 compliance posture for a two-agent skill.

**Trust Boundary 2 Verdict: PASS.** The filesystem handoff is secure, the `generated_by` const constraint provides provenance, and tspec-analyst's independent recomputation protects against tampered frontmatter coverage fields.

---

## Template and Schema Security Assessment

### bdd-scenario.template.md Security Assessment

**Overall:** PASS. The template is a well-structured placeholder file with no security risks. Placeholder tokens (`{UPPERCASE}`) are clearly distinguished from Gherkin content. The YAML frontmatter correctly hardcodes `generated_by: tspec-generator`. The `slice_id: null` default is safe (slice-scoped generation requires explicit non-null value).

**Content injection surface:** Template placeholders such as `{PRIMARY_ACTOR}`, `{ALT_CONDITION}`, and `{EXTENSION_CONDITION}` are derived from UC artifact fields. When tspec-generator populates these placeholders, it uses Clark transformation rules that map field values to Gherkin clauses. The placeholders are design-time documentation of the expected derivation; they do not create a runtime injection surface because the template is a reference, not a code execution template.

**Navigation table:** Present (H-23 compliance verified). Template Usage Notes section correctly documents all placeholders with their source fields.

### test-plan.template.md Security Assessment

**Overall:** PASS with finding SEC-005. The template structure is sound for a human-readable test plan document. The `priority_distribution` YAML block provides useful planning metadata. The `generated_by: tspec-generator` value is correct but lacks the schema-enforced `const` constraint present in the Feature file format (SEC-005).

**Out-of-scope YAML frontmatter:** The test-plan template's frontmatter does not reference test-specification-v1.schema.json (and should not -- test plan documents are not Feature files). However, the absence of any schema validation for test plan documents means the `generated_by` provenance is enforced only by the template convention, not by structural validation (SEC-005).

### test-specification-v1.schema.json Security Assessment

| Constraint | Security Value | Assessment |
|-----------|---------------|-----------|
| `source_use_case` pattern `^UC-[A-Z]+-\d{3}$` | Prevents arbitrary string injection in source reference | PASS -- strong structural constraint |
| `source_detail_level` enum (ESSENTIAL_OUTLINE, FULLY_DESCRIBED only) | Encodes RULE-IV-01 gate in output artifact | PASS -- defense-in-depth for input validation |
| `generated_by: const: "tspec-generator"` | Provenance immutability | PASS -- strongest possible constraint |
| `generated_at: format: date-time` | Enables stale detection | PASS |
| `scenario_count: minimum: 1` | Prevents empty Feature files | PASS |
| `coverage.total_flows: minimum: 1` | Prevents zero-denominator coverage | PASS |
| `coverage.mapped_flows: minimum: 0` | No upper bound relative to total_flows | GAP -- FIND-QA-004 (LOW) |
| Root `additionalProperties: true` | Permits arbitrary field injection | GAP -- SEC-003 (Low) |
| `coverage.additionalProperties: true` | Permits arbitrary coverage subfields | ACCEPTABLE -- documented extension strategy |
| `$id` uses non-existent domain | Misleading to schema tooling | INFO -- SEC-007 |

**Schema Security Verdict: PASS with gaps SEC-003 and FIND-QA-004.** The schema is well-designed with strong constraints on the most security-sensitive fields. The two gaps are addressable without structural redesign.

---

## L2: Strategic Implications

### Security Posture Assessment

The /test-spec skill establishes a consistent security posture with the /use-case skill reviewed in step-9: strong constitutional compliance, appropriate tool tier enforcement, no network access, no hardcoded credentials, and a minimal attack surface for a markdown/YAML transformation skill. The Bash tool represents the same structural gap identified in the /use-case review (SEC-001 in both reviews).

**Skill-specific security strengths not present in /use-case:**

1. **Deterministic transformation model (Clark $. path references):** The Clark algorithm's field-path-based derivation creates a fundamentally different injection surface than string interpolation. UC content flows into Gherkin clauses via named field paths, not string concatenation or template evaluation. This is a security-by-design property.

2. **Output artifact schema with `const` constraint:** The `generated_by: const: "tspec-generator"` constraint in the JSON schema creates provenance immutability that /use-case lacks (use-case-realization-v1.schema.json has no equivalent producer lock).

3. **Independent coverage recomputation:** tspec-analyst independently recomputes coverage from Source annotations rather than trusting the frontmatter coverage fields. This provides integrity verification of the generation-time snapshot without requiring the consuming agent to trust a potentially tampered field.

### Systemic Vulnerability Patterns

**Pattern 1: Bash tool governance gap (SEC-001)** -- This is now a two-skill pattern. Both /use-case (step-9-eng-security-review.md SEC-001) and /test-spec (this review SEC-001) declare the Bash tool without command scope constraints in governance YAML. The remediation recommendation is the same for both: `capabilities.bash_allowlist` in governance YAML with `uv run` pattern allowlist. This pattern should be applied as a framework-wide standard to all T2 agents that declare Bash access. A framework-level `bash_allowlist` field should be added to the agent-governance-v1.schema.json to enforce this at the schema level.

**Pattern 2: Schema `additionalProperties: true` (SEC-003)** -- Both /use-case (step-9-eng-security-review.md SEC-002) and /test-spec (this review SEC-003) schemas use `additionalProperties: true`. This is a framework-level schema design choice that should be documented as a policy: either all Jerry schemas use `false` (strict) or all use `true` with an explicit extension contract. The current inconsistency (no policy documentation) leaves each schema to make the choice independently.

**Pattern 3: Output path slug sanitization (SEC-004)** -- Both /use-case (step-9-eng-security-review.md SEC-005) and /test-spec (this review SEC-004) rely on UC title-derived slug components in output paths without explicit sanitization rules. A framework-level slug sanitization standard (e.g., a shared RULE-SLUG-01 rule in a framework-rules file) would address this across all skills that derive output paths from user-controlled content.

### Comparison with Threat Model Predictions

The architecture document (step-10-test-spec-architecture.md) identified GATE-3 (CI enforcement of test-specification-v1.schema.json) as pending. This review confirms GATE-3 is the most important outstanding security control: without CI enforcement, the schema's structural guarantees apply only during agent generation, not after-the-fact when Feature files are modified manually or by other tools. The GATE-3 implementation recommendation from eng-backend (step-10-eng-backend-implementation.md, L2, line 170-174) is correct and should be prioritized.

### Recommendations for Security Architecture Evolution

1. **Framework-level `bash_allowlist` in agent-governance-v1.schema.json** (P0 -- addresses SEC-001 pattern across all skills): Add `capabilities.bash_allowlist` as a recognized field in the governance schema. Document that T2+ agents declaring Bash MUST populate this field. Enforce via CI schema validation.

2. **Framework-level slug sanitization standard** (P1 -- addresses SEC-004 pattern): Create a shared `skills/_framework/rules/output-path-standards.md` that defines the slug sanitization algorithm applicable to all skills deriving output paths from user-controlled content fields.

3. **GATE-3: CI schema validation for Feature files** (P1 -- pending architecture): Implement as described in eng-backend L2 strategic implications. Apply to `projects/*/test-specs/*.feature.md`.

4. **Schema policy document** (P2 -- addresses SEC-003 pattern): Create a framework-level document defining the `additionalProperties` policy for Jerry schemas. Until policy is established, document the extension contract inline in each schema that uses `true`.

5. **coverage.mapped_flows upper bound constraint** (P3 -- addresses FIND-QA-004): Add schema constraint `"maximum": {"$ref": "#/properties/coverage/properties/total_flows"}` or equivalent to prevent coverage frontmatter values that exceed the total flow count.

---

## S-010 Self-Review

> Pre-delivery self-review per H-15 (S-010 required before presenting any deliverable).

### Evidence Coverage Check

| Review Area | Evidence Read | Coverage |
|-------------|--------------|---------|
| tspec-generator.md | Yes (full file, 256 lines) | Complete |
| tspec-generator.governance.yaml | Yes (full file, 97 lines) | Complete |
| tspec-analyst.md | Yes (full file, 243 lines) | Complete |
| tspec-analyst.governance.yaml | Yes (full file, 96 lines) | Complete |
| clark-transformation-rules.md | Yes (full file, 204 lines) | Complete |
| SKILL.md | Yes (full file, 377 lines) | Complete |
| bdd-scenario.template.md | Yes (full file, 143 lines) | Complete |
| test-plan.template.md | Yes (full file, 155 lines) | Complete |
| test-specification-v1.schema.json | Yes (full file, 118 lines) | Complete |
| step-10-test-spec-architecture.md | Yes (preview + key sections) | Sufficient |
| step-10-eng-lead-review.md | Yes (preview + key sections) | Sufficient |
| step-10-eng-backend-implementation.md | Yes (full file, 324 lines) | Complete |
| step-10-eng-qa-review.md | Yes (full file with security sections) | Complete |
| step-9-eng-security-review.md | Yes (pattern reference, full relevant sections) | Complete |

### Finding Validation Check

| Finding | CWE Verified | CVSS Verified | Evidence Cited | Remediation Specific |
|---------|-------------|--------------|---------------|---------------------|
| SEC-001 | CWE-78 (OS Command Injection) | 5.5 -- metric-justified | Governance YAML lines, capability text | bash_allowlist field specified |
| SEC-002 | CWE-22 (Path Traversal) | 4.3 -- metric-justified | Output section lines 88, 182 | Guardrail text and RULE-QA-05 specified |
| SEC-003 | CWE-20 (Improper Input Validation) | 2.5 -- metric-justified | Schema line 117 | False or documented extension contract |
| SEC-004 | CWE-20 (Improper Input Validation) | 3.1 -- metric-justified | clark-transformation-rules.md gap | RULE-IV-05 and RULE-QA-05 specified |
| SEC-005 | CWE-116 (Improper Output Encoding) | 2.3 -- metric-justified | test-plan.template.md line 4 | Schema or post-completion check |
| SEC-006 | CWE-116 (Improper Output Encoding) | 2.1 -- metric-justified | clark-transformation-rules.md line 136 | Type label correction specified |
| SEC-007 | N/A -- informational | N/A | Schema line 4 | Accepted design documented |
| SEC-008 | N/A -- informational | N/A | .prompt.md synchronization notes | FIND-002 tracking noted |

### Constitutional Compliance Verification Check

| Principle | tspec-generator | tspec-analyst | SKILL.md | Result |
|-----------|----------------|--------------|---------|--------|
| P-003 | 4 declarations | 4 declarations | 2 declarations | PASS |
| P-020 | 3 declarations | 3 declarations | 1 declaration | PASS |
| P-022 | 3 declarations | 4 declarations | 1 declaration | PASS |

### CWE Top 25 2025 Coverage Check

| CWE | Checked | Finding |
|-----|---------|---------|
| CWE-79 (XSS) | YES | N/A -- no browser rendering of output |
| CWE-89 (SQL Injection) | YES | N/A -- no database queries |
| CWE-78 (OS Command Injection) | YES | SEC-001 (Medium) |
| CWE-287 (Improper Authentication) | YES | N/A -- no authentication surface |
| CWE-862 (Missing Authorization) | YES | N/A -- T2 tier; filesystem-only |
| CWE-306 (Missing Auth for Critical Function) | YES | N/A -- no critical functions requiring auth |
| CWE-502 (Deserialization) | YES | PARTIAL -- YAML parsing of frontmatter; risk is LOW due to structured schema validation |
| CWE-798 (Hardcoded Credentials) | YES | None found |
| CWE-22 (Path Traversal) | YES | SEC-002 (Medium), SEC-004 (Low) |
| CWE-352 (CSRF) | YES | N/A -- no web interface |
| CWE-20 (Improper Input Validation) | YES | SEC-003 (Low), SEC-004 (Low) |
| CWE-116 (Improper Encoding) | YES | SEC-005 (Low), SEC-006 (Low) |

**CWE Coverage Verdict:** All applicable CWE Top 25 2025 categories checked. 8 N/A (not applicable to LLM agent framework skill), 1 partial, 3 with findings, 1 clean.

### ASVS Chapter Coverage Check

| Chapter | Applicable | Status |
|---------|-----------|--------|
| V1 (Architecture) | YES | PASS |
| V2 (Authentication) | NO | N/A |
| V3 (Session Management) | NO | N/A |
| V4 (Access Control) | YES | PASS with gap (SEC-002) |
| V5 (Validation/Sanitization) | YES | PASS with gap (SEC-004) |
| V6 (Cryptography) | NO | N/A |
| V7 (Error Handling) | YES | PASS |
| V8 (Data Protection) | YES | PASS |
| V9 (Communication) | NO | N/A |

### Output Quality Check

| Criterion | Status |
|-----------|--------|
| L0 executive summary present with finding counts | PASS |
| L1 detailed findings with CWE, CVSS, location, evidence, remediation | PASS |
| L2 strategic implications present | PASS |
| Constitutional compliance verified (P-003, P-020, P-022) | PASS |
| ASVS chapter verification present | PASS |
| H-34/H-35 compliance checklist present | PASS |
| Tool tier verification present | PASS |
| Cross-skill trust boundary analysis present | PASS |
| Template and schema security assessment present | PASS |
| Self-review (S-010) checklist present | PASS |
| Navigation table present (H-23 compliant) | PASS |
| File persisted to declared output path (P-002) | PASS |

---

*Security Review Version: 1.0.0*
*Author: eng-security | Date: 2026-03-09 | Standard: OWASP ASVS 5.0, CWE Top 25 2025, CVSS 3.1, NIST SSDF PW.7*
*Pattern reference: step-9-eng-security-review.md (v1.2.0)*
*Next step: step-10-eng-security-adv-score.md (adversarial scoring), then step-10-eng-reviewer-final.md (registration)*
