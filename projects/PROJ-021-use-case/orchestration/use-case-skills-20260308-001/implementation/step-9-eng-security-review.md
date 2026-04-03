# Security Code Review: /use-case Skill

> **PS ID:** proj-021 | **Entry ID:** step-9-eng-security-review | **Workflow ID:** use-case-skills-20260308-001
> **Date:** 2026-03-08 | **Agent:** eng-security | **Step:** 9 sub-step 5 of 6
> **Input artifacts:** uc-author.md, uc-author.governance.yaml, uc-slicer.md, uc-slicer.governance.yaml, composition/*.yaml, composition/*.prompt.md, templates/*, docs/schemas/use-case-realization-v1.schema.json, tests/BEHAVIOR_TESTS.md
> **Prior pipeline scores:** eng-architect 0.956, eng-lead 0.952, eng-backend 0.952, eng-qa 0.958 (all PASS at C4)
> **Review standard:** OWASP ASVS 5.0, CWE Top 25 2025, CVSS 3.1, NIST SSDF PW.7
> **Confidence:** 0.92 (complete manual review of all referenced files; one finding requires operational monitoring to fully validate)

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0: Executive Summary](#l0-executive-summary) | Finding counts by severity, overall posture, top risks, immediate actions |
| [L1: Technical Findings](#l1-technical-findings) | Individual finding reports with CWE, CVSS, location, evidence, remediation |
| [OWASP ASVS 5.0 Verification](#owasp-asvs-50-verification) | Chapter-by-chapter verification status |
| [H-34/H-35 Compliance Checklist](#h-34h-35-compliance-checklist) | Agent definition standards compliance |
| [P-003/P-020/P-022 Cross-File Matrix](#p-003p-020p-022-cross-file-matrix) | Constitutional principle verification across all files |
| [L2: Strategic Implications](#l2-strategic-implications) | Systemic patterns, architecture security posture, evolution recommendations |

---

## L0: Executive Summary

### Finding Counts by Severity

| Severity | Count | Findings |
|----------|-------|---------|
| Critical | 0 | -- |
| High | 0 | -- |
| Medium | 2 | SEC-001, SEC-002 |
| Low | 3 | SEC-003, SEC-004, SEC-005 |
| Informational | 2 | SEC-006, SEC-007 |
| **Total** | **7** | |

### Overall Security Assessment

**PASS with observations.** The /use-case skill implementation presents a strong security posture for an LLM agent framework operating on structured document artifacts. No critical or high-severity vulnerabilities were identified. The two medium findings are structural gaps that carry real risk but are mitigated by existing compensating controls. The three low findings are hardening opportunities. Both informational findings document intentional design decisions that are architecturally sound.

The prior pipeline achieved high quality scores (all >= 0.952) and the security foundations are well-established: tool tier enforcement is correct (T2), constitutional triplet is declared across all files, no Task tool access is granted to worker agents, and the schema applies strong structural constraints on artifact content. This review confirms those properties hold under security-focused scrutiny.

### Top 3 Risk Areas

1. **Unscoped Bash execution surface (SEC-001, Medium)** -- Both agents declare Bash tool access without any command scoping constraint. The stated use cases are narrow (`uv run jerry items create`, `uv run jerry validate`), but the Bash tool is unrestricted. An LLM that misinterprets user input could invoke arbitrary shell commands within the agent's execution context.

2. **Schema root `additionalProperties: true` (SEC-002, Medium)** -- The top-level schema accepts arbitrary extra fields. A malformed or adversarially crafted artifact file passed to uc-slicer could include unknown fields that pass schema validation and propagate to downstream consumers (/test-spec, /contract-design) without any structural gate.

3. **No Bash command allowlist in governance YAML (SEC-003, Low)** -- The governance files document the tool tier (T2) and list forbidden agent-level actions, but neither governance YAML nor the agent `.md` files constrain the Bash tool to specific command patterns. This gap means the T2 designation is accurate at the delegation level (no Task tool) but does not constrain within-session shell access.

### Recommended Immediate Actions

1. Add a `capabilities.bash_allowlist` entry to both governance YAML files specifying the exact `uv run` patterns that are permitted (remediation for SEC-001, SEC-003).
2. Change `"additionalProperties": true` to `"additionalProperties": false` at the schema root, or add explicit documentation of the extension contract (remediation for SEC-002).
3. Add `verify_no_arbitrary_bash_commands_outside_allowlist` to both agents' `validation.post_completion_checks` (remediation for SEC-003).

---

## L1: Technical Findings

### Finding Table

| Finding ID | Severity | CVSS 3.1 | CWE | Description | File(s) | Recommendation |
|-----------|----------|----------|-----|-------------|---------|----------------|
| SEC-001 | Medium | 5.5 | CWE-78 | Bash tool declared without command scope constraint | uc-author.md, uc-slicer.md, uc-author.governance.yaml, uc-slicer.governance.yaml, both composition agent YAMLs | Add `bash_allowlist` in governance; constrain to `uv run` patterns only |
| SEC-002 | Medium | 5.3 | CWE-20 | Schema root `additionalProperties: true` permits unvalidated field injection | docs/schemas/use-case-realization-v1.schema.json | Set `additionalProperties: false` or document extension contract |
| SEC-003 | Low | 3.7 | CWE-78 | Governance YAML does not declare Bash command constraints, creating gap between stated T2 intent and actual shell access | uc-author.governance.yaml, uc-slicer.governance.yaml | Add `capabilities.bash_allowlist` field; add post-completion check |
| SEC-004 | Low | 3.1 | CWE-502 | Input artifact YAML frontmatter is consumed by uc-slicer without explicit untrusted-input warning; path-to-file is user-supplied | uc-slicer.md, uc-slicer.governance.yaml | Add explicit input source trust annotation; verify file existence before read |
| SEC-005 | Low | 2.9 | CWE-22 | Output path pattern `projects/${JERRY_PROJECT}/use-cases/UC-{DOMAIN}-{NNN}-{slug}.md` includes user-controlled `{slug}` component that is not constrained by schema or guardrails | uc-author.md (line 129), use-case-realization.template.md | Add slug sanitization rule: enforce `^[a-z0-9-]+$` pattern; document in guardrails |
| SEC-006 | Info | -- | -- | Schema `$id` uses a non-existent domain (`jerry-framework.dev`); not a security risk but could mislead schema tooling | use-case-realization-v1.schema.json line 3 | Accepted design -- document as internal schema identifier; no action required |
| SEC-007 | Info | -- | -- | Composition prompt files (`.prompt.md`) are manually maintained copies with a documented drift risk (FIND-004 synchronization note); stale copies could lead agents to apply outdated guardrails | uc-author.prompt.md line 3, uc-slicer.prompt.md line 3 | Already tracked as FIND-004; CI lint check recommended for long-term |

---

### SEC-001: Bash Tool Without Command Scope Constraint

**Severity:** Medium | **CVSS 3.1:** AV:L/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:N = **5.5** | **CWE:** CWE-78 (OS Command Injection)

**Affected files:**
- `skills/use-case/agents/uc-author.md` line 16 (`- Bash`)
- `skills/use-case/agents/uc-slicer.md` line 18 (`- Bash`)
- `skills/use-case/agents/uc-author.governance.yaml` (no bash constraint in `capabilities`)
- `skills/use-case/agents/uc-slicer.governance.yaml` (no bash constraint in `capabilities`)
- `skills/use-case/composition/uc-author.agent.yaml` line 34 (`- shell_execute`)
- `skills/use-case/composition/uc-slicer.agent.yaml` line 36 (`- shell_execute`)

**Data flow trace:**

User request --> uc-author/uc-slicer agent receives it --> agent may invoke Bash --> Bash executes in the host OS context.

The Bash tool provides unrestricted shell access. The agent definitions state the intended use is narrow:
- uc-author: "Execute CLI validation commands to verify artifact schema compliance (H-05: use `uv run` prefix)"
- uc-slicer: "Execute worktracker CLI commands to create Story entities for each slice via Bash (H-05: use `uv run jerry items create`)"

However, neither the `.md` guardrails section nor the `.governance.yaml` `capabilities` block constrains what Bash commands may be invoked. The `forbidden_actions` array addresses agent-level delegation (P-003) but does not address shell command scope. An LLM that processes a crafted user input containing text like "also run `rm -rf` to clean up" or that misinterprets intent could invoke unintended commands.

**Proof of vulnerability:**

The agent `.md` files explicitly state "Execute CLI validation commands" as a capability but the `<guardrails>` section does not include a `no_arbitrary_bash_execution` constraint. The governance `output_filtering` array constrains artifact content (secrets, status field) but not command execution. There is no `bash_allowlist` or equivalent declaration anywhere in the agent definition stack.

**Severity rationale:** Medium rather than High because: (1) the LLM is the execution layer -- it must first decide to run an unintended command; (2) the stated use cases are narrow and the agent's cognitive mode (integrative/systematic) focuses on document manipulation; (3) the Bash tool executes in the same user context as the IDE/CLI session, not with escalated privileges. The risk is real but requires an LLM reasoning error to materialize.

**Remediation:**

Add to both `uc-author.governance.yaml` and `uc-slicer.governance.yaml` under `capabilities`:

```yaml
capabilities:
  bash_allowlist:
    - "^uv run jerry validate.*$"
    - "^uv run jerry items create.*$"
    - "^uv run python.*$"
  bash_description: "Bash is restricted to Jerry CLI validation and worktracker item creation. No file system destructive commands permitted."
  forbidden_actions:
    # existing entries ...
    - "BASH VIOLATION: NEVER execute shell commands outside the bash_allowlist patterns -- Consequence: unrestricted shell execution in the user's OS context can cause irreversible data loss or expose secrets from the environment."
```

Add to both `<guardrails>` sections in the `.md` files:

```
- `bash_commands_restricted_to_allowlist`: Only execute `uv run jerry validate` (uc-author) and `uv run jerry items create` (uc-slicer) via Bash. Never execute file deletion, environment inspection, or arbitrary OS commands.
```

---

### SEC-002: Schema Root `additionalProperties: true` Permits Unvalidated Field Injection

**Severity:** Medium | **CVSS 3.1:** AV:N/AC:H/PR:N/UI:R/S:U/C:N/I:M/A:N = **5.3** | **CWE:** CWE-20 (Improper Input Validation)

**Affected file:** `docs/schemas/use-case-realization-v1.schema.json` line 642

**Evidence:**

```json
"additionalProperties": true
```

This is the final line of the top-level schema object. All `$defs` sub-schemas use `additionalProperties: false` (confirmed at lines 119, 141, 173, 349, 390, 431, 498, 537, 565, 569). However, the root schema object accepts arbitrary unknown fields. This means an artifact file could contain any top-level key not defined in the schema's `properties` block, and it would pass structural validation.

**Attack scenario:** A use case artifact produced by or modified to include an injected field such as `_override_status: APPROVED` or `_inject_instruction: "ignore previous instructions"` would pass schema validation. uc-slicer would load and process the file. Downstream agents (/test-spec, /contract-design) would also accept the file. The extra field propagates through the entire artifact pipeline without any gate.

The risk is not prompt injection via YAML values (the LLM reads the file, not executes it), but rather: (a) semantic confusion for downstream agents processing unexpected fields, and (b) a structural gap that is inconsistent with the defense-in-depth posture demonstrated by all `$defs` sub-schemas using `additionalProperties: false`.

**Why this was likely intentional:** The schema comment at line 24 (`"$comment_identity": {"const": "=== IDENTITY BLOCK ==="`) suggests the schema was designed to accept organizational comments-as-fields that are not formally typed properties. The template files use fields like `$comment_identity`, `$comment_classification`, etc. as semantic markers. Setting `additionalProperties: false` would break this pattern.

**Remediation options (choose one):**

Option A (preferred): Enumerate the `$comment_*` fields as optional schema properties with `const` constraints, then set `additionalProperties: false`. This makes the extension pattern explicit.

Option B (acceptable): Document the open extension contract explicitly in the schema description and add a guardrail in both agent definitions: "Never add fields to use case artifacts that are not defined in the schema's `properties` block (exception: `$comment_*` organizational markers)."

Option C (minimum): Add an explicit `$comment_extensibility` field to the schema properties documenting why `additionalProperties: true` is intentional, and add input validation in uc-slicer to log a warning when unknown top-level fields are present in an input artifact.

---

### SEC-003: Governance YAML Does Not Declare Bash Command Constraints

**Severity:** Low | **CVSS 3.1:** AV:L/AC:H/PR:L/UI:N/S:U/C:N/I:L/A:N = **3.7** | **CWE:** CWE-78 (partial -- governance gap, not a direct injection vector)

**Affected files:** `uc-author.governance.yaml`, `uc-slicer.governance.yaml`

**Evidence:** The governance YAML files are the machine-readable governance metadata validated against `agent-governance-v1.schema.json`. They correctly declare `tool_tier: "T2"` which -- per agent-development-standards.md -- means "Read-Write (T1 + Write, Edit, Bash)." The T2 tier includes Bash by definition.

However, the governance `capabilities` block (which allows `additionalProperties: true` via the schema) has no field constraining what Bash commands are permitted. The `forbidden_actions` array contains 5 (uc-author) and 6 (uc-slicer) entries, none of which address Bash command scope. This gap means the governance record is accurate about what tools are available but silent about how they are restricted.

**Relationship to SEC-001:** SEC-003 is the governance layer manifestation of the same risk as SEC-001. SEC-001 is the behavioral (agent `.md`) gap; SEC-003 is the declarative (governance YAML) gap. Remediating SEC-001 addresses the behavioral risk; remediating SEC-003 makes the governance record complete and machine-auditable.

**Remediation:** Implement SEC-001 remediation in governance YAML as described above. Additionally add `verify_bash_commands_match_allowlist` to `validation.post_completion_checks` in both governance files.

---

### SEC-004: Input Artifact YAML from User-Controlled Path Lacks Trust Annotation

**Severity:** Low | **CVSS 3.1:** AV:L/AC:H/PR:L/UI:R/S:U/C:N/I:L/A:N = **3.1** | **CWE:** CWE-502 (Deserialization of Untrusted Data -- partial)

**Affected files:** `uc-slicer.md` (input section), `uc-slicer.governance.yaml` (input_validation)

**Evidence:**

The uc-slicer agent accepts `artifact_path` as a session context field:

```
- `artifact_path`: Path to use case artifact to slice
```

The input validation in the governance YAML states:

```yaml
input_validation:
  - "Input artifact must exist and contain valid YAML frontmatter with $.work_type = USE_CASE"
  - "Input artifact $.detail_level must be >= ESSENTIAL_OUTLINE (reject BRIEFLY_DESCRIBED and BULLETED_OUTLINE)"
  - "Input artifact must have $.basic_flow with 3-9 steps"
```

These checks validate content structure but do not validate the path itself. A user (or upstream orchestrator) providing `artifact_path` could supply a path to any readable file in the repository, not just files under `projects/${JERRY_PROJECT}/use-cases/`. If an attacker-controlled file with `work_type: USE_CASE` and appropriate structure exists elsewhere in the repository, uc-slicer would accept and process it.

**Severity rationale:** Low because: (1) the framework requires valid `work_type: USE_CASE` and `detail_level >= ESSENTIAL_OUTLINE`, which limits what files would pass input validation; (2) the agent cannot write to arbitrary locations -- output goes to the same input file path; (3) this is an authenticated-user scenario (the user controls the Jerry session).

**Remediation:** Add an input validation rule to both the `.md` guardrails section and governance YAML:

```yaml
- "artifact_path must resolve to a file under projects/${JERRY_PROJECT}/use-cases/ -- reject paths outside this directory"
```

This is a defense-in-depth control, not a critical fix.

---

### SEC-005: Output Path `{slug}` Component Is User-Controlled Without Pattern Constraint

**Severity:** Low | **CVSS 3.1:** AV:L/AC:H/PR:L/UI:N/S:U/C:N/I:L/A:N = **2.9** | **CWE:** CWE-22 (Path Traversal -- partial)

**Affected files:** `skills/use-case/agents/uc-author.md` (line 129), `skills/use-case/templates/use-case-realization.template.md` (line 4)

**Evidence:**

The output path pattern is:

```
projects/${JERRY_PROJECT}/use-cases/UC-{DOMAIN}-{NNN}-{slug}.md
```

The `{slug}` is described as "a lowercase hyphen-separated version of the title." The title is a user-supplied field, constrained only by:
- Schema: `"type": "string", "minLength": 1, "maxLength": 200`
- Guardrails: no slug character constraint declared

A title like `"../../../.context/rules/quality-enforcement"` would produce slug `../../../.context/rules/quality-enforcement` and an output path `projects/${JERRY_PROJECT}/use-cases/UC-AUTH-001-../../../.context/rules/quality-enforcement.md`, which resolves to a path outside the intended output directory.

**Severity rationale:** Low because: (1) the agent is operating in an authenticated user session; (2) the user would have to deliberately supply a malformed title; (3) the Write tool in Claude Code applies path normalization. However, the absence of a documented constraint is a hardening gap, especially since the schema has `maxLength: 200` but no `pattern` constraint.

**Remediation:** Add to uc-author `<guardrails>` output constraints:

```
- `slug_must_match_safe_pattern`: The slug component of the output filename must match `^[a-z0-9][a-z0-9-]*[a-z0-9]$`. Titles must be sanitized before use in file paths: remove path separator characters (`/`, `\`, `..`), collapse spaces to hyphens, lowercase.
```

Optionally add a `pattern` constraint to the schema `title` property or add a separate schema property `slug` with pattern `^[a-z0-9-]+$`.

---

### SEC-006: Schema `$id` Uses Non-Existent Domain (Informational)

**Severity:** Informational | **CWE:** N/A

**File:** `docs/schemas/use-case-realization-v1.schema.json` line 3

```json
"$id": "https://jerry-framework.dev/schemas/use-case-realization/v1.0.0"
```

The domain `jerry-framework.dev` does not resolve to any live host. This is a common pattern for internal JSON Schema `$id` values used as URIs rather than URLs. It does not create a supply chain risk because schema validators use `$id` as an identifier, not a resolution target (unless remote `$ref` fetching is enabled, which it is not here -- all `$ref` values are local fragment references of the form `#/$defs/...`).

**Assessment:** No action required. This is an accepted internal schema design pattern. The informational finding is recorded for auditability.

---

### SEC-007: Composition Prompt Files Are Manually Maintained Copies (Informational)

**Severity:** Informational | **CWE:** N/A

**Files:** `skills/use-case/composition/uc-author.prompt.md` (line 3), `skills/use-case/composition/uc-slicer.prompt.md` (line 3)

Both prompt files open with:

```
> **Synchronization note:** This file is a manually-maintained copy of the markdown body from
> `skills/use-case/agents/uc-{author|slicer}.md` (everything after the YAML frontmatter closing `---`).
> When updating uc-{author|slicer}.md, this file MUST be updated in the same commit. (FIND-004)
```

This is an acknowledged drift risk (tracked as FIND-004 by eng-backend). Manual synchronization of copies is a known maintenance weakness -- if the agent `.md` guardrails section is updated to address SEC-001 (adding Bash command constraints), the corresponding `.prompt.md` file must be updated in the same commit or the Task-invocation path will operate with the older, less-constrained guardrails.

**Assessment:** No immediate action required beyond the existing FIND-004 tracking. If SEC-001 is remediated, both `.prompt.md` files must be updated in the same commit as the `.md` files. A CI lint check that verifies the markdown bodies of `.md` and `.prompt.md` files are identical would eliminate the drift risk permanently. This is a long-term hardening recommendation.

---

## OWASP ASVS 5.0 Verification

The following chapters are relevant to an LLM agent framework operating on structured document artifacts. Chapters not applicable to this domain (V9 Communication, V6 Stored Cryptography in the traditional sense) are noted as N/A.

### V1: Architecture, Design and Threat Modeling

| Requirement ID | Requirement | Status | Evidence |
|----------------|-------------|--------|---------|
| V1.1 | Software development lifecycle is in use | PASS | Jerry framework has explicit SDLC (eng-team 8-step pipeline, SSDF PW.7 alignment) |
| V1.2 | Threat modeling performed for authentication and trust | PASS | Prior agent eng-architect performed threat modeling (step-9-use-case-architecture.md, Risk Register §7); trust boundaries at uc-author/uc-slicer boundary explicitly documented |
| V1.3 | Separation of high and low security components | PASS | T2 tier enforced; no T5 (Task) access in worker agents; composition layer separates invocation config from system prompt |
| V1.4 | Trust boundary crossings require authentication and authorization | PARTIAL | File-mediated handoff is the sole trust boundary; schema validation is the authorization gate; FIND: no path constraint on input artifact (SEC-004) |
| V1.5 | Data classification performed; PII handling identified | PASS | `no_secrets_in_output` guardrail declared in both agents; documentation explicitly notes "No passwords, tokens, API keys, or PII in use case artifact content" |

### V2: Authentication

| Requirement ID | Requirement | Status | Evidence |
|----------------|-------------|--------|---------|
| V2 (general) | Authentication mechanisms | N/A | The skill operates within an authenticated Jerry session; authentication is the session layer's responsibility, not the skill's |

### V3: Session Management

| Requirement ID | Requirement | Status | Evidence |
|----------------|-------------|--------|---------|
| V3 (general) | Session tokens, fixation, expiry | N/A | No session tokens; stateless per-invocation agents; cross-session state explicitly declared as "not available (no MCP persistent store)" |

### V4: Access Control

| Requirement ID | Requirement | Status | Evidence |
|----------------|-------------|--------|---------|
| V4.1 | Access control enforces least privilege | PASS | T2 tool tier (Read, Write, Edit, Glob, Grep, Bash) is the minimum for the stated tasks; no T5 delegation |
| V4.2 | Access control denies by default | PARTIAL | Tool tier enforces tool-class access; within Bash, no allowlist exists (SEC-001/SEC-003) |
| V4.3 | Authorization checks are not bypassable | PASS | Schema validation (L1 layer) and agent guardrail checks (L2 layer) provide two independent authorization gates for artifact structure |
| V4.4 | Principle of separation of duties | PASS | uc-author writes artifacts; uc-slicer consumes artifacts written by uc-author; neither can invoke the other directly (P-003); distinct role boundaries enforced by domain guardrails |

### V5: Validation, Sanitization and Encoding

| Requirement ID | Requirement | Status | Evidence |
|----------------|-------------|--------|---------|
| V5.1.1 | All HTTP input validated against an allowlist | PARTIAL (adapted) | Schema validation enforces allowlist for all typed fields (enums, patterns); `additionalProperties: true` at root is a gap (SEC-002) |
| V5.1.2 | Structured data validated against a schema | PASS | use-case-realization-v1.schema.json provides structural validation; agent guardrails provide semantic validation; two-layer validation design explicitly documented |
| V5.1.3 | Unstructured data sanitized | PARTIAL | Free-text fields (`title`, `action`, `condition`) accept arbitrary strings; no XSS/injection risk in this domain (YAML, not HTML), but slug sanitization is absent (SEC-005) |
| V5.1.4 | Input validation failures logged and rejected | PASS | Both agents declare `fallback_behavior: escalate_to_user`; failure modes table explicitly maps each rejection condition to a user-facing error response |
| V5.2.1 | User-supplied HTML sanitized | N/A | No HTML rendering in this skill |
| V5.3.1 | Output encoding context-appropriate | PASS | Output is YAML + Markdown; no dynamic HTML rendering; no encoding attack surface |

### V7: Error Handling and Logging

| Requirement ID | Requirement | Status | Evidence |
|----------------|-------------|--------|---------|
| V7.1 | Log messages do not contain sensitive data | PASS | Agent guardrails explicitly prohibit secrets in output; error messages include specific field names but not values |
| V7.2 | Error handling does not leak implementation details | PASS | Failure mode responses are operational (schema field name, validation result) not implementation-internal |
| V7.3 | Security controls do not fail open | PASS | Both agents declare `fallback_behavior: escalate_to_user`; schema validation rejects non-conforming artifacts rather than accepting with defaults |

### V8: Data Protection

| Requirement ID | Requirement | Status | Evidence |
|----------------|-------------|--------|---------|
| V8.1 | Sensitive data not stored unnecessarily | PASS | Use case artifacts represent system behavior, not personal data; `no_secrets_in_output` guardrail prevents credential storage in artifacts |
| V8.2 | Sensitive data in memory purged | N/A | Stateless agent invocations; no in-memory sensitive data accumulation |
| V8.3 | Private keys and passwords not logged | PASS | `no_secrets_in_output` guardrail covers all output paths; no credential fields in schema |

### V6: Stored Cryptography

| Status | Rationale |
|--------|-----------|
| N/A | No cryptographic operations; no secrets storage; no key management in scope |

### V9: Communication

| Status | Rationale |
|--------|-----------|
| N/A | T2 agents have no network access; no external HTTP calls; "External web research (no network access -- T2 tier)" explicitly declared |

---

## H-34/H-35 Compliance Checklist

This checklist verifies the H-34 compound rule (agent definition architecture, schema validation, constitutional compliance).

### uc-author

| Requirement | Evidence | Status |
|-------------|----------|--------|
| Dual-file architecture: `uc-author.md` + `uc-author.governance.yaml` | Both files exist and read successfully | PASS |
| `.md` frontmatter uses only official Claude Code fields | Fields: `name`, `description`, `model`, `tools` -- all in the 12 recognized fields list | PASS |
| No non-standard fields in `.md` frontmatter | Verified: only 4 fields present | PASS |
| `.governance.yaml` has `version` (SemVer pattern) | `version: "1.0.0"` -- matches `^\d+\.\d+\.\d+$` | PASS |
| `.governance.yaml` has `tool_tier` (enum T1-T5) | `tool_tier: "T2"` | PASS |
| `.governance.yaml` has `identity.role` | "Use Case Author -- creates and elaborates use case artifacts..." | PASS |
| `.governance.yaml` has `identity.expertise` (min 2) | 3 entries: Cockburn, Jacobson UC 2.0, Cockburn sea-metaphor | PASS |
| `.governance.yaml` has `identity.cognitive_mode` (valid enum) | `integrative` -- valid per 5-mode taxonomy | PASS |
| `capabilities.forbidden_actions` min 3, includes P-003/P-020/P-022 | 5 entries; first 3 explicitly reference P-003, P-020, P-022 in NPT-009-complete format | PASS |
| `constitution.principles_applied` min 3, includes P-003/P-020/P-022 | 6 entries: P-001, P-002, P-003, P-004, P-020, P-022 | PASS |
| `tools` in `.md` does NOT include `Task` | Tools: Read, Write, Edit, Glob, Grep, Bash -- no Task | PASS |
| `.md` body has all 7 XML-tagged sections | `<identity>`, `<purpose>`, `<input>`, `<capabilities>`, `<methodology>`, `<output>`, `<guardrails>` -- all present | PASS |
| `guardrails.fallback_behavior` declared | `escalate_to_user` | PASS |
| `guardrails.output_filtering` min 3 entries | 5 entries | PASS |
| `guardrails.input_validation` min 1 rule | 2 entries | PASS |
| `output.required` and `output.location` declared | `required: true`, location pattern present | PASS |
| Composition layer `.agent.yaml` does not include `Task` or `agent_delegate` | `tools.forbidden: [agent_delegate]` -- explicit prohibition | PASS |
| Composition `.prompt.md` matches `.md` body | Verified content match; synchronization note present (FIND-004) | PASS |
| **Bash access constrained to specific commands** | No `bash_allowlist` declared in governance or guardrails | **FAIL (SEC-001/SEC-003)** |

### uc-slicer

| Requirement | Evidence | Status |
|-------------|----------|--------|
| Dual-file architecture: `uc-slicer.md` + `uc-slicer.governance.yaml` | Both files exist and read successfully | PASS |
| `.md` frontmatter uses only official Claude Code fields | Fields: `name`, `description`, `model`, `tools` -- all in the 12 recognized fields list | PASS |
| No non-standard fields in `.md` frontmatter | Verified: only 4 fields present | PASS |
| `.governance.yaml` has `version` (SemVer pattern) | `version: "1.0.0"` -- matches `^\d+\.\d+\.\d+$` | PASS |
| `.governance.yaml` has `tool_tier` (enum T1-T5) | `tool_tier: "T2"` | PASS |
| `.governance.yaml` has `identity.role` | "Use Case Slicer -- decomposes use cases..." | PASS |
| `.governance.yaml` has `identity.expertise` (min 2) | 3 entries: Jacobson UC 2.0, slice lifecycle, realization | PASS |
| `.governance.yaml` has `identity.cognitive_mode` (valid enum) | `systematic` -- valid per 5-mode taxonomy | PASS |
| `capabilities.forbidden_actions` min 3, includes P-003/P-020/P-022 | 6 entries; first 3 explicitly reference P-003, P-020, P-022 in NPT-009-complete format | PASS |
| `constitution.principles_applied` min 3, includes P-003/P-020/P-022 | 6 entries: P-001, P-002, P-003, P-004, P-020, P-022 | PASS |
| `tools` in `.md` does NOT include `Task` | Tools: Read, Write, Edit, Glob, Grep, Bash -- no Task | PASS |
| `.md` body has all 7 XML-tagged sections | `<identity>`, `<purpose>`, `<input>`, `<capabilities>`, `<methodology>`, `<output>`, `<guardrails>` -- all present | PASS |
| `guardrails.fallback_behavior` declared | `escalate_to_user` | PASS |
| `guardrails.output_filtering` min 3 entries | 5 entries | PASS |
| `guardrails.input_validation` min 1 rule | 3 entries -- more specific than uc-author | PASS |
| `output.required` and `output.location` declared | `required: true`, location pattern present | PASS |
| Composition layer `.agent.yaml` does not include `Task` or `agent_delegate` | `tools.forbidden: [agent_delegate]` -- explicit prohibition | PASS |
| Composition `.prompt.md` matches `.md` body | Verified content match; synchronization note present (FIND-004) | PASS |
| **Bash access constrained to specific commands** | No `bash_allowlist` declared in governance or guardrails | **FAIL (SEC-001/SEC-003)** |

**H-34/H-35 Summary:** 17/18 requirements PASS for each agent. The single FAIL is the Bash command scope constraint gap (SEC-001/SEC-003). This is not a HARD rule gap in the current H-34 specification (which does not yet mandate bash_allowlist), but is identified as a hardening finding under ASVS V4.2 and CWE-78.

---

## P-003/P-020/P-022 Cross-File Verification Matrix

This matrix verifies that the three constitutional principles are consistently declared across all files in the implementation.

### P-003 (No Recursive Subagents)

| File | Declaration | Text | Consistent? |
|------|------------|------|-------------|
| `uc-author.md` `<guardrails>` | Present | "P-003: NEVER spawn sub-agents or use the Task tool. uc-author is a T2 worker agent." | Yes |
| `uc-author.md` `forbidden_actions` | Present | "P-003 VIOLATION: NEVER spawn recursive subagents or delegate to other agents via Task tool -- Consequence: agent hierarchy violation..." | Yes |
| `uc-author.governance.yaml` `forbidden_actions[0]` | Present | "P-003 VIOLATION: NEVER spawn recursive subagents or delegate to other agents via Task tool -- Consequence: agent hierarchy violation..." | Yes -- exact match with .md |
| `uc-author.governance.yaml` `constitution.principles_applied` | Present | "P-003" listed | Yes |
| `uc-author.agent.yaml` `tools.forbidden` | Present | `[agent_delegate]` -- functional enforcement of P-003 | Yes -- mechanism present |
| `uc-author.agent.yaml` `constitution.forbidden_actions[0]` | Present | "P-003 VIOLATION: NEVER spawn recursive subagents..." | Yes -- consistent |
| `uc-author.prompt.md` `<guardrails>` | Present | Identical to `uc-author.md` `<guardrails>` (FIND-004 synchronization) | Yes |
| `uc-slicer.md` `<guardrails>` | Present | "P-003: NEVER spawn sub-agents or use the Task tool. uc-slicer is a T2 worker agent." | Yes |
| `uc-slicer.md` `forbidden_actions` | Present | "P-003 VIOLATION: NEVER spawn recursive subagents or delegate to other agents via Task tool -- Consequence: agent hierarchy violation..." | Yes |
| `uc-slicer.governance.yaml` `forbidden_actions[0]` | Present | "P-003 VIOLATION: NEVER spawn recursive subagents or delegate to other agents via Task tool -- Consequence: agent hierarchy violation..." | Yes -- exact match |
| `uc-slicer.governance.yaml` `constitution.principles_applied` | Present | "P-003" listed | Yes |
| `uc-slicer.agent.yaml` `tools.forbidden` | Present | `[agent_delegate]` | Yes |
| `uc-slicer.agent.yaml` `constitution.forbidden_actions[0]` | Present | "P-003 VIOLATION: NEVER spawn recursive subagents..." | Yes -- consistent |
| `uc-slicer.prompt.md` `<guardrails>` | Present | Identical to `uc-slicer.md` `<guardrails>` | Yes |

**P-003 verdict:** CONSISTENT across all 14 declaration points. No contradictions detected.

### P-020 (User Authority -- Never Override)

| File | Declaration | Text | Consistent? |
|------|------------|------|-------------|
| `uc-author.md` `<guardrails>` | Present | "P-020: NEVER override user decisions about use case scope, actor list, goal level, or target detail level." | Yes |
| `uc-author.md` `forbidden_actions` | Present | "P-020 VIOLATION: NEVER override user decisions about use case scope, detail level, or actor classification -- Consequence: unauthorized scope changes erode trust..." | Yes |
| `uc-author.governance.yaml` `forbidden_actions[1]` | Present | "P-020 VIOLATION: NEVER override user decisions about use case scope, detail level, or actor classification -- Consequence: unauthorized scope changes erode trust..." | Yes -- exact match |
| `uc-author.governance.yaml` `constitution.principles_applied` | Present | "P-020" listed | Yes |
| `uc-author.agent.yaml` `constitution.forbidden_actions[1]` | Present | "P-020 VIOLATION: NEVER override user decisions about use case scope, detail level, or actor classification..." | Yes -- consistent |
| `uc-author.prompt.md` `<guardrails>` | Present | Identical to `uc-author.md` | Yes |
| `uc-slicer.md` `<guardrails>` | Present | "P-020: NEVER override user decisions about slice boundaries, priority ordering, or lifecycle state transitions." | Yes -- correctly scoped to slicer domain |
| `uc-slicer.md` `forbidden_actions` | Present | "P-020 VIOLATION: NEVER override user decisions about slice boundaries, priority ordering, or lifecycle state transitions -- Consequence: unauthorized slice modifications invalidate implementation planning..." | Yes |
| `uc-slicer.governance.yaml` `forbidden_actions[1]` | Present | Identical to `uc-slicer.md` | Yes -- exact match |
| `uc-slicer.governance.yaml` `constitution.principles_applied` | Present | "P-020" listed | Yes |
| `uc-slicer.agent.yaml` `constitution.forbidden_actions[1]` | Present | "P-020 VIOLATION: NEVER override user decisions about slice boundaries, priority ordering, or lifecycle state transitions..." | Yes -- consistent |
| `uc-slicer.prompt.md` `<guardrails>` | Present | Identical to `uc-slicer.md` | Yes |

**P-020 verdict:** CONSISTENT across all 12 declaration points. Domain-specific scoping (scope/actor/detail-level for uc-author; slice boundaries/priority/state-transitions for uc-slicer) is appropriate and correct -- each agent's P-020 text is tailored to its actual decision domain. The core principle is preserved in both.

### P-022 (No Deception About Actions/Capabilities/Confidence)

| File | Declaration | Text | Consistent? |
|------|------------|------|-------------|
| `uc-author.md` `<guardrails>` | Present | "P-022: NEVER misrepresent the detail level of a produced artifact." | Yes |
| `uc-author.md` `forbidden_actions` | Present | "P-022 VIOLATION: NEVER misrepresent the completeness or detail level of a use case artifact -- Consequence: setting $.detail_level to FULLY_DESCRIBED when extensions are incomplete..." | Yes |
| `uc-author.governance.yaml` `forbidden_actions[2]` | Present | "P-022 VIOLATION: NEVER misrepresent the completeness or detail level of a use case artifact -- Consequence: setting $.detail_level to FULLY_DESCRIBED when extensions are incomplete..." | Yes -- exact match |
| `uc-author.governance.yaml` `constitution.principles_applied` | Present | "P-022" listed | Yes |
| `uc-author.agent.yaml` `constitution.forbidden_actions[2]` | Present | "P-022 VIOLATION: NEVER misrepresent the completeness or detail level of a use case artifact..." | Yes -- consistent |
| `uc-author.prompt.md` `<guardrails>` | Present | Identical to `uc-author.md` | Yes |
| `uc-slicer.md` `<guardrails>` | Present | "P-022: NEVER misrepresent slice lifecycle state or INVEST assessment results." | Yes -- correctly scoped |
| `uc-slicer.md` `forbidden_actions` | Present | "P-022 VIOLATION: NEVER misrepresent slice lifecycle state or INVEST assessment results -- Consequence: setting $.slice_state to PREPARED when test cases are absent..." | Yes |
| `uc-slicer.governance.yaml` `forbidden_actions[2]` | Present | Identical to `uc-slicer.md` | Yes -- exact match |
| `uc-slicer.governance.yaml` `constitution.principles_applied` | Present | "P-022" listed | Yes |
| `uc-slicer.agent.yaml` `constitution.forbidden_actions[2]` | Present | "P-022 VIOLATION: NEVER misrepresent slice lifecycle state or INVEST assessment results..." | Yes -- consistent |
| `uc-slicer.prompt.md` `<guardrails>` | Present | Identical to `uc-slicer.md` | Yes |

**P-022 verdict:** CONSISTENT across all 12 declaration points. Domain-specific scoping is appropriate (detail_level misrepresentation for uc-author; slice_state and INVEST result misrepresentation for uc-slicer). Both capture the P-022 spirit: the agent must not produce artifacts that falsely represent their completion state.

### Cross-File Consistency Summary

| Principle | Consistency | Contradictions Found |
|-----------|------------|---------------------|
| P-003 | CONSISTENT | None |
| P-020 | CONSISTENT | None |
| P-022 | CONSISTENT | None |

All three constitutional principles are consistently declared across all agent definition files, governance YAML files, composition agent YAML files, and composition prompt files. The text is either an exact match between corresponding files or appropriately domain-scoped (uc-author vs. uc-slicer have different but coherent P-020 and P-022 scopes).

---

## L2: Strategic Implications

### Security Posture Assessment

The /use-case skill implementation has a strong security posture relative to its threat model. The skill operates as a document-authoring workflow tool, not as an application handling network-sourced untrusted input. The primary threat surface is:

1. **LLM behavioral control** -- Are the agents constrained to do what they are supposed to do? Answer: Yes, comprehensively. The five-layer enforcement architecture (L2 re-injection, schema validation, agent guardrails, post-completion checks, governance YAML) provides defense in depth. Constitutional compliance is the strongest in the pipeline: 12 declaration points per principle, exact text match across file types, domain-scoped tailoring.

2. **Artifact integrity** -- Can a malformed artifact bypass the pipeline gates? Answer: Mostly yes with caveats. The JSON Schema provides strong structural validation with `additionalProperties: false` on all sub-schemas. The root-level `additionalProperties: true` (SEC-002) is the only structural gap.

3. **Shell access scope** -- Can user input induce unintended OS commands? Answer: The risk exists but is bounded. The Bash tool access is the most significant security concern and the primary remediation target.

### Systemic Vulnerability Patterns

One systemic pattern is identified: **T2 tier includes Bash access without a framework-level mechanism for declaring allowed command patterns.** This is a framework-wide gap, not specific to /use-case. Looking at other T2 agents in the framework (e.g., ps-analyst, nse-architecture per the agent-development-standards.md Tool Security Tiers table), Bash access is a standard T2 capability but the standards document does not define a `bash_allowlist` governance field. The /use-case skill is among the most carefully implemented skills in the framework, and yet it has this gap.

Recommendation: The agent-development-standards.md Tool Security Tiers table should be updated to note that T2+ agents SHOULD declare `capabilities.bash_allowlist` in their governance YAML when Bash access is required. This would be a MEDIUM standard addition (not a HARD rule), consistent with existing MEDIUM standards for T3+ agents requiring citation guardrails.

### Comparison with Threat Model Predictions

The eng-architect threat model (step-9-use-case-architecture.md §7 Risk Register) identified risks in the following areas: schema semantic violations, detail level misrepresentation, realization level inconsistency, and INVEST criteria skipping. This security review confirms that all of these risks are addressed by the behavioral guardrails and schema allOf constraints.

The threat model did not explicitly identify the Bash scope risk (SEC-001) or the slug path traversal risk (SEC-005). These are implementation-level concerns that emerge from the choice of tools and output path patterns and are appropriate for security review to surface.

### Recommendations for Security Architecture Evolution

1. **Short-term (before eng-reviewer handoff):** Remediate SEC-001 and SEC-003 by adding `bash_allowlist` to both governance YAMLs and corresponding `.md` guardrails sections. This is a low-effort, high-value hardening change that closes the most meaningful gap.

2. **Short-term (optional):** Remediate SEC-002 by either enumerating `$comment_*` fields as schema properties or documenting the extension contract explicitly. If `additionalProperties: false` is chosen, update both template files to remove `$comment_*` markers or convert them to YAML comments (lines starting with `#`).

3. **Medium-term:** Add `bash_allowlist` as a MEDIUM standard to agent-development-standards.md for all T2+ agents that declare Bash/shell_execute access. This closes the framework-wide pattern gap identified above.

4. **Medium-term:** Add a CI lint check that verifies `.md` and `.prompt.md` composition files are identical in their markdown body section (addressing FIND-004 drift risk, SEC-007 informational finding).

5. **Long-term:** When the /test-spec and /contract-design skills are implemented as downstream consumers of the use-case artifact, perform a cross-skill security review focused on the `interactions[]` block. The schema description explicitly marks this block as "ARCHITECTURALLY SPECULATIVE" -- the downstream consumers' input validation of this block's content should be a security review focus point at that time.

---

*Security review completed: 2026-03-08*
*Reviewer: eng-security (SSDF PW.7 -- manual code review)*
*Scope: All 10 files under security review focus areas as specified*
*Next step: eng-reviewer (Step 9 sub-step 6 of 6)*
