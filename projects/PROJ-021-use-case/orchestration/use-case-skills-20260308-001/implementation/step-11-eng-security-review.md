# Security Code Review: /contract-design Skill

> **PS ID:** proj-021 | **Entry ID:** step-11-eng-security-review | **Workflow ID:** use-case-skills-20260308-001
> **Date:** 2026-03-09 | **Agent:** eng-security | **Step:** 11 (Phase 3 Implementation)
> **Input artifacts:** 17 files spanning SKILL.md, cd-generator.md/.governance.yaml, cd-validator.md/.governance.yaml, composition files (x4), templates (x4), uc-to-contract-rules.md, CD_SKILL_CONTRACT.yaml, BEHAVIOR_TESTS.md, sample-contract.openapi.yaml
> **Prior pipeline scores:** eng-architect 0.956 (PASS), eng-lead 0.956 (PASS), eng-backend 0.959 (PASS), eng-qa 0.953 (PASS)
> **Review standard:** OWASP ASVS 5.0, CWE Top 25 2025, CVSS 3.1, NIST SSDF PW.7
> **Pattern reference:** step-10-eng-security-review.md (v1.1.0)
> **Version:** 1.0.0
> **Confidence:** 0.91 (complete manual review of all 17 files; LLM trust model bounds residual risk for behavioral guardrails that cannot be statically verified; deferred-template activation risk requires operational monitoring)

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0: Executive Summary](#l0-executive-summary) | Finding counts by severity, overall posture, top risks, immediate actions |
| [L1: Technical Findings](#l1-technical-findings) | Individual finding reports with CWE, CVSS, location, evidence, remediation |
| [SEC-CD-001: Schema Injection via Natural Language Fields](#sec-cd-001-schema-injection-via-natural-language-fields) | CWE-20: Improper Input Validation -- template injection via UC description fields |
| [SEC-CD-002: ErrorResponse Schema Lacks Sensitive-Data Filtering Guarantee](#sec-cd-002-errorresponse-schema-lacks-sensitive-data-filtering-guarantee) | CWE-209: Information Exposure Through Error Messages |
| [SEC-CD-003: Missing Security Schemes in Generated OpenAPI Template](#sec-cd-003-missing-security-schemes-in-generated-openapi-template) | CWE-306: Missing Authentication for Critical Function |
| [SEC-CD-004: Deferred Template Files Lack Runtime Activation Guard](#sec-cd-004-deferred-template-files-lack-runtime-activation-guard) | CWE-284: Improper Access Control (deferred feature activation path) |
| [SEC-CD-005: Slug Sanitization Not Enforced in Output Path Construction](#sec-cd-005-slug-sanitization-not-enforced-in-output-path-construction) | CWE-22: Path Traversal |
| [SEC-CD-006: No Rate or Volume Bound on Interaction Count](#sec-cd-006-no-rate-or-volume-bound-on-interaction-count) | CWE-400: Uncontrolled Resource Consumption |
| [SEC-CD-007: PROTOTYPE Label Bypass via x-prototype Field Overwrite](#sec-cd-007-prototype-label-bypass-via-x-prototype-field-overwrite) | CWE-693: Protection Mechanism Failure |
| [OWASP ASVS 5.0 Verification](#owasp-asvs-50-verification) | Chapter-by-chapter verification status |
| [OWASP Top 10 Mapping](#owasp-top-10-mapping) | Relevance of each OWASP category to this skill |
| [Constitutional Compliance Verification](#constitutional-compliance-verification) | P-003, P-020, P-022 cross-file verification matrix |
| [H-34/H-35 Compliance Checklist](#h-34h-35-compliance-checklist) | Agent definition standards compliance from security perspective |
| [Findings Table](#findings-table) | All findings sorted by severity with CVSS scores and CWE IDs |
| [Recommendations](#recommendations) | Prioritized remediation actions |
| [L2: Strategic Implications](#l2-strategic-implications) | Security posture relative to production deployment |
| [S-010 Self-Review Checklist](#s-010-self-review-checklist) | Pre-delivery quality verification |

---

## L0: Executive Summary

### Overall Security Assessment

The `/contract-design` skill presents a **sound security posture** for a documentation-generation tool within a trusted framework. The skill does not execute arbitrary code, does not make network calls, operates on internally-authored UC artifacts, and correctly applies the most critical control -- the mandatory PROTOTYPE label -- which prevents premature production use of generated contracts. The architecture's threat model (Section 8 of step-11-contract-design-architecture.md) is methodologically complete and the STRIDE analysis is accurate for the primary risks.

Seven security findings are raised. None are CRITICAL. Two are HIGH severity. Three are MEDIUM. Two are LOW. All are addressable without architectural change and without modifying the existing HARD rule set.

### Finding Counts by Severity

| Severity | Count | Actionable Before Production? |
|----------|-------|-------------------------------|
| CRITICAL | 0 | N/A |
| HIGH | 2 | Yes -- SEC-CD-003, SEC-CD-005 |
| MEDIUM | 3 | Yes -- SEC-CD-001, SEC-CD-004, SEC-CD-007 |
| LOW | 2 | Yes -- SEC-CD-002, SEC-CD-006 |
| **Total** | **7** | |

### Top 3 Risk Areas

1. **Missing security scheme generation in contracts (SEC-CD-003 -- HIGH).** The OpenAPI template (`openapi-template.yaml`) and the generation algorithm (uc-to-contract-rules.md) have no mechanism for producing `securitySchemes` or `security` blocks in generated contracts. The UC artifact schema has no field for authentication requirements. Downstream implementers who consume PROTOTYPE-removed contracts will build APIs with no authentication model. This is the most impactful finding because it affects every contract produced by the skill.

2. **Path traversal risk in slug-based output path construction (SEC-CD-005 -- HIGH).** The output path pattern `projects/${JERRY_PROJECT}/contracts/UC-{DOMAIN}-{NNN}-{slug}.openapi.yaml` derives the `{slug}` component from the UC title. If a UC title contains `..`, `/`, or other traversal characters and the slug sanitization is not enforced at the guardrail level (FIND-QA-006 from eng-qa confirms this gap), an adversarially-crafted UC artifact could cause the contract to be written outside the intended `contracts/` directory.

3. **Deferred template files lack a hard runtime activation guard (SEC-CD-004 -- MEDIUM).** Both `asyncapi-template.yaml` and `cloudevents-template.yaml` are marked `x-deferred: true` in their file content and the SCOPE VIOLATION forbidden action in `cd-generator` explicitly prohibits AsyncAPI/CloudEvents generation. However, the prohibition is a behavioral LLM guardrail, not a structural read-time gate. A future model update or context-pressure failure could cause the guardrail to be ignored, activating untested template logic.

### Recommended Immediate Actions

| Priority | Action | Finding |
|----------|--------|---------|
| P1 | Add `security_requirements` field to UC artifact schema and `securitySchemes` generation to cd-generator rules | SEC-CD-003 |
| P1 | Enforce slug sanitization via explicit guardrail constraint and output_filtering entry | SEC-CD-005 |
| P2 | Add deferred-template file access check to cd-generator input validation gate | SEC-CD-004 |
| P2 | Clarify PROTOTYPE label bypass scenario handling in cd-validator mandatory FAIL flow | SEC-CD-007 |
| P3 | Add `sensitive_data_warning_if_error_message_contains_entity_identifier` to output_filtering | SEC-CD-002 |
| P3 | Document interaction count upper bound in input validation gate | SEC-CD-006 |
| P3 | Remove `source_extension` from the public `ErrorResponse` schema or restrict it to non-public variants | SEC-CD-001 |

---

## L1: Technical Findings

---

### SEC-CD-001: Schema Injection via Natural Language Fields

**Severity:** MEDIUM
**CWE:** CWE-20 (Improper Input Validation) / CWE-116 (Improper Encoding or Escaping of Output)
**CVSS 3.1 Score:** 4.3 (Medium)
**CVSS Vector:** AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:L/A:N

**Affected Files:**
- `skills/contract-design/rules/uc-to-contract-rules.md` (RULE-SD-01, RULE-SD-02)
- `skills/contract-design/agents/cd-generator.md` (Step 5, Step 6 methodology)
- `skills/contract-design/templates/openapi-template.yaml` (description fields)

**Location:**
The `verbatim precondition text` and `verbatim postcondition text` outputs described in RULE-SD-01 and RULE-SD-02 are written directly into OpenAPI schema `description` fields without sanitization.

**Evidence:**
RULE-SD-01 specifies:
> "Property description: **verbatim precondition text**"

RULE-SD-02 specifies:
> "Property description: **verbatim postcondition text**"

The sample contract at line 72 confirms verbatim emission:
```yaml
member_card_id:
  type: string
  description: "Valid, active library card identifier (precondition: 'Member holds a valid, active library card')"
```

If a UC artifact author (or a compromised /use-case output) places YAML control characters, Markdown injection sequences (e.g., `](javascript:evil())`), or HTML injection strings (`<script>`) in precondition/postcondition text, those characters are emitted verbatim into the generated OpenAPI YAML `description` field. OpenAPI rendering tools (Swagger UI, Redocly) render `description` fields as Markdown/HTML. This creates a stored XSS vector for contract consumers using browser-based API documentation tools.

**OWASP Top 10 Mapping:** A03:2021 -- Injection (stored XSS in rendered OpenAPI documentation)

**Reproduction Steps:**
1. Author a UC artifact with precondition text: `"Valid token <script>alert('xss')</script>"`
2. Invoke cd-generator on the artifact
3. Open the generated OpenAPI contract in Swagger UI or Redocly
4. Observe XSS execution in the rendered documentation interface

**Remediation:**
Add an output_filtering constraint to `cd-generator.governance.yaml`:
```yaml
- "description_fields_must_strip_html_tags_and_escape_yaml_special_characters"
```

Add to uc-to-contract-rules.md RULE-SD-01 and RULE-SD-02:
> **Sanitization requirement:** Before emitting precondition/postcondition text into YAML description fields, strip HTML tags, escape YAML special characters (`{`, `}`, `[`, `]`, `|`, `>`), and encode Markdown link syntax. This is not a limitation on the content -- the semantic meaning is preserved; only structural injection characters are removed.

The risk is bounded somewhat by the fact that UC artifacts are internally authored (not from untrusted external users), but as the skill is consumed by more teams, the provenance assumption weakens.

---

### SEC-CD-002: ErrorResponse Schema Lacks Sensitive-Data Filtering Guarantee

**Severity:** LOW
**CWE:** CWE-209 (Generation of Error Message Containing Sensitive Information)
**CVSS 3.1 Score:** 3.1 (Low)
**CVSS Vector:** AV:N/AC:H/PR:N/UI:R/S:U/C:L/I:N/A:N

**Affected Files:**
- `skills/contract-design/templates/openapi-template.yaml` (ErrorResponse schema)
- `skills/contract-design/templates/json-schema-template.json` (ErrorResponse schema)
- `skills/contract-design/samples/sample-contract.openapi.yaml` (ErrorResponse in use)

**Location:**
The `ErrorResponse` schema in both templates defines a `source_extension` field:
```yaml
ErrorResponse:
  type: object
  properties:
    error:
      type: string
    code:
      type: string
    source_extension:
      type: string
      description: "Extension ID that generated this error response"
```

**Evidence:**
The `source_extension` field (populated with values like `EXT-2a`) exposes the internal use case artifact's extension ID namespace to external API consumers. This is a form of implementation detail leakage. While `EXT-2a` by itself is low-sensitivity, the pattern of exposing internal traceability identifiers (designed for developer use) in a public API error response schema creates a disclosure surface for the internal UC artifact structure.

More significantly, the `no_secrets_in_output` output_filtering constraint in `cd-generator.governance.yaml` focuses on API keys, passwords, and PII -- it does not explicitly address internal identifier disclosure via the ErrorResponse schema. An implementer who populates the `source_extension` field verbatim in runtime API responses leaks internal structure to external callers.

**OWASP Top 10 Mapping:** A05:2021 -- Security Misconfiguration (implementation details in error responses)

**Remediation:**
Add a note to the ErrorResponse schema template warning that `source_extension` is for internal tooling/development use and SHOULD NOT be returned in runtime API responses:
```yaml
source_extension:
  type: string
  description: "Extension ID that generated this error response. FOR INTERNAL TOOLING USE ONLY -- do not return this field in runtime API responses to external callers."
  x-internal-only: true
```

Add to output_filtering in `cd-generator.governance.yaml`:
```yaml
- "error_response_source_extension_must_be_marked_internal_only"
```

---

### SEC-CD-003: Missing Security Schemes in Generated OpenAPI Template

**Severity:** HIGH
**CWE:** CWE-306 (Missing Authentication for Critical Function)
**CVSS 3.1 Score:** 7.5 (High)
**CVSS Vector:** AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N

**Affected Files:**
- `skills/contract-design/templates/openapi-template.yaml` (no `securitySchemes` section)
- `skills/contract-design/rules/uc-to-contract-rules.md` (no security derivation rule)
- `skills/contract-design/agents/cd-generator.md` (methodology Steps 1-9 have no security step)
- `skills/contract-design/contracts/CD_SKILL_CONTRACT.yaml` (GeneratorInput schema has no security_requirements field)

**Location:**
The OpenAPI template (`openapi-template.yaml`) contains no `securitySchemes` block and no `security` declarations on operations. The 9-step transformation algorithm in `uc-to-contract-rules.md` covers resource identification (RI), operation mapping (OM), HTTP method inference (HM), schema derivation (SD), error responses (ER), actor roles (AR), and traceability (TR) -- but has no security rule category (e.g., RULE-SEC-01).

**Evidence:**
`openapi-template.yaml` lines 1-89 contain no `securitySchemes` section in `components`. No `security:` key appears anywhere in the template. The UC artifact input schema (`CD_SKILL_CONTRACT.yaml` GeneratorInput) has no field for authentication type, authorization model, or security requirements.

The sample contract (`sample-contract.openapi.yaml`) at `POST /loans` has no security declaration -- a library member can call the loan creation endpoint without any authentication model specified in the contract.

**Security impact:**
When a human reviewer removes the `x-prototype: true` label and approves the contract for production use, the contract has no `securitySchemes` or operation-level `security` declarations. Code generators consuming the contract (e.g., OpenAPI Generator) will generate API stubs with no authentication middleware. API gateway configurations derived from the contract will have no security policy baseline. This is the most impactful finding because it creates a systemic omission across all generated contracts.

**OWASP Top 10 Mapping:** A07:2021 -- Identification and Authentication Failures; A01:2021 -- Broken Access Control

**ASVS Mapping:** V2.1 (Authentication), V4.1 (Access Control Design)

**Remediation:**

**Option A (Minimal -- documentation only):** Add a `securitySchemes` placeholder section to `openapi-template.yaml` with a `# TODO: Replace with actual security scheme before removing x-prototype` comment:
```yaml
components:
  securitySchemes:
    # PLACEHOLDER: Specify the authentication scheme for this API before removing x-prototype: true
    # Common options: bearerAuth (JWT), apiKey, oauth2, openIdConnect
    # Reference: OpenAPI 3.1 Section 4.8.26 (Security Scheme Object)
    bearerAuth:
      type: http
      scheme: bearer
      x-placeholder: true
      x-note: "Replace with actual authentication scheme. This placeholder prevents code generators from producing unauthenticated stubs."
```

Add a RULE-SEC-01 to `uc-to-contract-rules.md`:
> RULE-SEC-01: Generate a placeholder `securitySchemes` section in every contract with `x-placeholder: true` annotation. Apply the placeholder scheme to all consumer-facing operations. Annotate the contract with `x-security-review-required: true` to flag that security scheme selection requires human decision.

**Option B (Preferred -- schema extension):** Add an optional `security_requirements` field to the UC artifact schema's `interactions` block for actor-authenticated interactions:
```yaml
actor_authentication:
  type: string
  enum: [bearer_jwt, api_key, oauth2, none, tbd]
  description: "Authentication scheme required by the primary actor"
```

Then derive `securitySchemes` from this field via a new RULE-SEC-01 in the transformation algorithm.

**Short-term action (P1):** Implement Option A to ensure all generated contracts have a security placeholder. Option B requires schema versioning work.

---

### SEC-CD-004: Deferred Template Files Lack Runtime Activation Guard

**Severity:** MEDIUM
**CWE:** CWE-284 (Improper Access Control) / CWE-1035 (OWASP Top 10 2021 Category A05 -- Security Misconfiguration)
**CVSS 3.1 Score:** 4.4 (Medium)
**CVSS Vector:** AV:L/AC:H/PR:L/UI:N/S:U/C:L/I:L/A:N

**Affected Files:**
- `skills/contract-design/templates/asyncapi-template.yaml` (x-deferred: true)
- `skills/contract-design/templates/cloudevents-template.yaml` (x-deferred: true)
- `skills/contract-design/agents/cd-generator.md` (SCOPE VIOLATION forbidden action)
- `skills/contract-design/agents/cd-generator.governance.yaml` (SCOPE VIOLATION forbidden action)

**Location:**
The deferred templates exist at:
- `skills/contract-design/templates/asyncapi-template.yaml`
- `skills/contract-design/templates/cloudevents-template.yaml`

Both carry `x-deferred: true` metadata. The cd-generator agent has a behavioral guardrail:
> "SCOPE VIOLATION: NEVER generate AsyncAPI or CloudEvents contracts in v1.0.0"

**Evidence:**
The prohibition is an LLM behavioral instruction. It relies on the model interpreting and following the forbidden action at runtime. No structural check prevents cd-generator from loading and populating the deferred templates:
- The `capabilities` section does not exclude reading `asyncapi-template.yaml` or `cloudevents-template.yaml` from the allowed file list
- No input validation gate checks that the requested output format is OpenAPI-only
- The composition files (`cd-generator.agent.yaml`) do not restrict the file write target to `.openapi.yaml` extensions only

Under context pressure (large UC artifact, high token consumption), or following a model update that changes instruction-following behavior, the behavioral guardrail could fail silently. An implementer who explicitly asks "generate an AsyncAPI contract" could receive output from the deferred templates without the G-02 unresolved design gaps being respected.

**OWASP Top 10 Mapping:** A05:2021 -- Security Misconfiguration (disabled-by-design feature bypass)

**Remediation:**
Add an explicit check to the cd-generator input validation gate (Step 1 guardrail):
```
If the requested output format or output_path does not end in .openapi.yaml:
  REJECT: "cd-generator v1.0.0 generates OpenAPI 3.1 contracts only. AsyncAPI and CloudEvents generation are deferred pending G-02 resolution. Requested format: {format}."
```

Add to `guardrails.input_validation` in `cd-generator.governance.yaml`:
```yaml
- "output_path must end in .openapi.yaml (rejects requests for .asyncapi.yaml or .cloudevents.yaml output)"
```

Add to `output_filtering`:
```yaml
- "generated_yaml_must_contain_openapi_version_key_not_asyncapi_or_cloudevents_key"
```

This converts the deferred-format restriction from a behavioral LLM instruction to a structural output-validation check that cd-validator can also verify.

---

### SEC-CD-005: Slug Sanitization Not Enforced in Output Path Construction

**Severity:** HIGH
**CWE:** CWE-22 (Improper Limitation of a Pathname to a Restricted Directory -- Path Traversal)
**CVSS 3.1 Score:** 6.5 (Medium-High, adjusted because the attacker must author a UC artifact and the framework has no shell execution of the path -- file writes only)
**CVSS Vector:** AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:H/A:N

**Affected Files:**
- `skills/contract-design/agents/cd-generator.md` (output location patterns, Step 9 methodology)
- `skills/contract-design/agents/cd-generator.governance.yaml` (output_filtering)
- `skills/contract-design/SKILL.md` (output artifacts section)
- `skills/contract-design/composition/cd-generator.agent.yaml` (output location)

**Location:**
The output path pattern defined consistently across all files:
```
projects/${JERRY_PROJECT}/contracts/UC-{DOMAIN}-{NNN}-{slug}.openapi.yaml
```

The `{slug}` is defined in `cd-generator.md`:
> "The slug is a lowercase hyphen-separated version of the UC title (e.g., UC-LIB-001-borrow-a-book.openapi.yaml)."

**Evidence:**
This finding was also identified by eng-qa as FIND-QA-006: "Slug sanitization not present in agent output_filtering guardrail lists." The eng-qa review recommended adding slug sanitization but classified it as LOW. This security review upgrades the severity to HIGH because the specific attack surface is a path traversal vector, not merely a naming inconsistency.

The `output_filtering` entries in `cd-generator.governance.yaml` do not include any constraint on the slug content. The agent methodology Step 9 ("The slug is a lowercase hyphen-separated version of the UC title") describes the target format but does not specify a sanitization step that enforces the restriction.

**Attack scenario:**
1. Author a UC artifact with `title: "Exploit ../../.claude/settings.local.json target"`
2. The slug derivation produces: `exploit-../../.claude/settings-local-json-target` (if the LLM does not sanitize the `..` sequences)
3. The output path becomes: `projects/${JERRY_PROJECT}/contracts/UC-{DOMAIN}-{NNN}-exploit-../../.claude/settings-local-json-target.openapi.yaml`
4. This resolves to writing the "contract" file outside the intended `contracts/` directory

The risk is bounded by:
- UC artifacts are internally authored (not from arbitrary external input)
- File writes via the `Write` tool do not execute the written content
- The `JERRY_PROJECT` prefix anchors part of the path

However, within the framework's threat model, the attack surface is real: a team member could inadvertently or maliciously author a UC artifact with a title that causes output path escape. The lack of a deterministic sanitization guardrail means the protection relies entirely on author intent.

**OWASP Top 10 Mapping:** A01:2021 -- Broken Access Control (file write path traversal)

**ASVS Mapping:** V5.2.5 (Path Traversal), V5.3.4 (Output Encoding for File Operations)

**Remediation:**
Add to `guardrails.output_filtering` in `cd-generator.governance.yaml`:
```yaml
- "slug_must_contain_only_lowercase_letters_digits_and_hyphens_no_path_separators"
- "output_path_must_start_with_projects/{JERRY_PROJECT}/contracts/ prefix_verification"
```

Add a sanitization step to the slug derivation in `cd-generator.md` methodology Step 9:
> Before using the slug in the output path, sanitize it: strip all characters except `[a-z0-9-]`. Replace spaces with hyphens. Remove any `.`, `/`, `\`, or `..` sequences. The sanitized slug must match `^[a-z0-9][a-z0-9-]*[a-z0-9]$`. If the sanitized slug is empty or shorter than 3 characters, substitute `unnamed-contract`.

Add to `uc-to-contract-rules.md` as RULE-RI-04 (safety rule):
> **RULE-RI-04:** Sanitize the output path slug before writing any file. The slug is derived from UC title but must be restricted to `[a-z0-9-]+`. No path traversal characters (`.`, `/`, `\`) are permitted. This rule has no UC schema input -- it is a safety gate applied unconditionally.

---

### SEC-CD-006: No Rate or Volume Bound on Interaction Count

**Severity:** LOW
**CWE:** CWE-400 (Uncontrolled Resource Consumption)
**CVSS 3.1 Score:** 3.1 (Low)
**CVSS Vector:** AV:L/AC:L/PR:L/UI:N/S:U/C:N/I:N/A:L

**Affected Files:**
- `skills/contract-design/agents/cd-generator.md` (input validation gate, Step 1)
- `skills/contract-design/agents/cd-generator.governance.yaml` (input_validation)
- `skills/contract-design/contracts/CD_SKILL_CONTRACT.yaml` (UCInteraction pattern constraint)

**Location:**
The input validation gate at Step 1 checks that `$.interactions` is non-empty (at least 1 interaction). It does not check for an upper bound on interaction count.

**Evidence:**
`cd-generator.governance.yaml` input_validation:
```yaml
- "Input artifact must have $.interactions array with at least 1 entry (reject with actionable error directing to /use-case uc-slicer)"
```

No upper bound is specified. The `CD_SKILL_CONTRACT.yaml` GeneratorInput schema has `interaction_count: { minimum: 1 }` but no `maximum`.

A UC artifact with 500 interactions would cause cd-generator to apply the full 9-step transformation to every interaction, consuming proportional context window and token budget. At sufficient scale (e.g., 200+ interactions), this could exhaust the cd-generator context window mid-generation and produce a truncated, malformed OpenAPI contract.

**OWASP Top 10 Mapping:** A05:2021 -- Security Misconfiguration (resource bound omission)

**Remediation:**
Add to `cd-generator.governance.yaml` input_validation:
```yaml
- "$.interactions array must not exceed 50 entries per generation session (split large UCs into focused sub-use-cases if the interaction count exceeds this limit)"
```

Add to `CD_SKILL_CONTRACT.yaml` GeneratorInput:
```yaml
interaction_count:
  type: integer
  minimum: 1
  maximum: 50
  description: "Count of interactions in the UC artifact. Maximum 50 per generation session to prevent context window exhaustion."
```

Add to `uc-to-contract-rules.md` Overview:
> **Scope constraint:** The UC-to-contract transformation is designed for use case realizations with 1-50 interaction entries. Use cases with more than 50 interactions should be decomposed into focused sub-use-cases (each covering a coherent user goal) before generating contracts. This is a context window management constraint, not a methodology limitation.

The 50-interaction ceiling is provisional; calibrate against observed context window consumption during Phase 3 prototype validation (R-01 per architecture risk register).

---

### SEC-CD-007: PROTOTYPE Label Bypass via x-prototype Field Overwrite

**Severity:** MEDIUM
**CWE:** CWE-693 (Protection Mechanism Failure)
**CVSS 3.1 Score:** 5.3 (Medium)
**CVSS Vector:** AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:L/A:N

**Affected Files:**
- `skills/contract-design/agents/cd-generator.md` (RULE-TR-02, output constraints)
- `skills/contract-design/agents/cd-validator.md` (Step 7 mandatory FAIL)
- `skills/contract-design/rules/uc-to-contract-rules.md` (RULE-TR-02)

**Location:**
The PROTOTYPE label is enforced by:
1. cd-generator: output constraint `generated_contracts_must_carry_x_prototype_true`
2. cd-validator Step 7: mandatory FAIL if `info.x-prototype: true` is absent
3. RULE-TR-02: "Include x-prototype: true in the info section of every generated contract"

**Evidence:**
The current implementation protects against *absence* of the label (`x-prototype: true` missing triggers FAIL). However, the following scenarios are not covered by the current validation:

**Scenario A -- x-prototype: false bypass:** A contract where `info.x-prototype: false` is present would pass the current cd-validator Step 7 check. Step 7 verifies "Verify that `info.x-prototype: true` is present" -- it checks for the value `true`, but if the field is present with value `false`, the behavior of the check depends on interpretation. The validator specification says "Verify that `info.x-prototype: true` is present" -- if `x-prototype: false` is in the info section, the check could be read as FAIL (the field is there but not `true`) or ambiguous.

**Scenario B -- Validator inconsistency handling:** `cd-validator.md` Failure Modes table includes:
> "All 9 steps PASS but contract has x-prototype: false -- This is a contradiction (Step 7 would have caught it). Flag as an internal error; escalate to user."

This scenario is documented as a failure mode to handle, confirming that the ambiguity is recognized but the resolution path ("flag as internal error") does not specify whether the overall verdict is PASS or FAIL in this edge case. If the verdict defaults to PASS despite `x-prototype: false`, the protection mechanism fails.

**Attack scenario:**
A UC artifact processed through cd-generator produces a contract with `x-prototype: true`. An implementer edits the contract to replace `x-prototype: true` with `x-prototype: false` (intending to mark it as production-ready without proper review). They then run cd-validator. If the validator's Step 7 check does not explicitly test for `x-prototype: false` as a distinct FAIL case, the contract receives a PASS verdict despite having an invalid prototype label state.

**OWASP Top 10 Mapping:** A05:2021 -- Security Misconfiguration (protection bypass through field value substitution)

**Remediation:**
Update cd-validator Step 7 to check for both conditions:
```markdown
### Step 7: PROTOTYPE Label Verification

Verify BOTH conditions:
1. `info.x-prototype` field is present in the contract's `info` section
2. `info.x-prototype` value is exactly `true` (boolean true, not the string "true" or false)

Failure action for condition 1 (field absent): FAIL -- "Contract is missing info.x-prototype: true..."
Failure action for condition 2 (field present but value is not true): FAIL -- "Contract has info.x-prototype set to {value}, not true. This indicates the PROTOTYPE label may have been manually altered before human review was complete. Restore x-prototype: true and complete the review process before removing the label."
```

Add to `cd-validator.governance.yaml` output_filtering:
```yaml
- "step_7_must_fail_when_x_prototype_absent_or_not_true"
```

Add to `uc-to-contract-rules.md` RULE-TR-02:
> **Bypass prevention:** The PROTOTYPE label value must be the boolean `true`. Contracts carrying `x-prototype: false` or `x-prototype: "true"` (string) are considered mislabeled. cd-validator Step 7 MUST fail for any value other than the boolean `true`.

---

## OWASP ASVS 5.0 Verification

This skill is a documentation/specification generator, not a web application. The most relevant ASVS chapters are those governing input validation, output encoding, data protection, and error handling. API security chapters apply indirectly because the skill *produces* API specifications that will define web APIs.

| ASVS Chapter | Application | Status | Evidence |
|-------------|-------------|--------|---------|
| V1 Architecture, Design and Threat Modeling | Threat model exists in architecture Section 8 with STRIDE analysis and DREAD scoring | PASS | step-11-contract-design-architecture.md Section 8: 7 STRIDE threats mapped, 3 DREAD-scored |
| V2 Authentication | Not directly applicable (skill is a documentation generator, not an authentication system). Indirectly: generated contracts lack authentication model (SEC-CD-003) | PARTIAL | Missing `securitySchemes` in template -- see SEC-CD-003 |
| V3 Session Management | Not applicable -- stateless document transformation | N/A | Both agents are T2, no cross-session state |
| V4 Access Control | File access is bounded by T2 tool tier. No output to paths outside `projects/` is intended. Path traversal risk identified (SEC-CD-005) | PARTIAL | Slug sanitization gap identified -- see SEC-CD-005 |
| V5 Validation, Sanitization and Encoding | Input validation gate (two-layer) is present. Output encoding for YAML description fields lacks explicit HTML/YAML injection sanitization (SEC-CD-001) | PARTIAL | RULE-SD-01 "verbatim" description emission without sanitization |
| V6 Stored Cryptography | Not applicable -- no credential storage | N/A | T2 tier; no secrets stored by the skill |
| V7 Error Handling and Logging | REJECT messages are specific and actionable. Failure modes are documented. ErrorResponse schema leaks internal identifiers (SEC-CD-002) | PARTIAL | `source_extension` field in ErrorResponse schema |
| V8 Data Protection | `no_secrets_in_output` constraint present. No PII fields in generated contracts by design (derived from UC descriptions, not live data) | PASS | output_filtering constraint verified in governance YAML |
| V9 Communication | Not applicable -- skill produces file artifacts, no network communication | N/A | T2 tier has no WebSearch/WebFetch tools |

**ASVS Overall Assessment:** PARTIAL PASS. The skill correctly addresses the most critical chapters (V1, V8) and has N/A status for network-dependent chapters. The gaps in V4 (path traversal), V5 (output encoding), and the indirect V2 concern (no security scheme generation) are the primary areas requiring remediation.

---

## OWASP Top 10 Mapping

This section maps OWASP Top 10 2021 categories to their relevance for a contract-generation skill that produces OpenAPI specifications.

| OWASP Category | Relevance to /contract-design | Finding |
|----------------|-------------------------------|---------|
| A01:2021 Broken Access Control | Path traversal risk in output path construction. Generated contracts lack access control model. | SEC-CD-005, SEC-CD-003 |
| A02:2021 Cryptographic Failures | Not directly applicable -- skill does not handle cryptographic material. Generated contracts should specify TLS requirements but currently do not. | SEC-CD-003 (indirect) |
| A03:2021 Injection | Verbatim emission of UC description text into YAML/OpenAPI fields creates stored XSS risk in rendered API documentation tools. | SEC-CD-001 |
| A04:2021 Insecure Design | Missing security scheme generation represents an insecure design default -- contracts pass review without authentication model. | SEC-CD-003 |
| A05:2021 Security Misconfiguration | Deferred templates lack hard activation guard. No interaction count bound. PROTOTYPE bypass scenario. | SEC-CD-004, SEC-CD-006, SEC-CD-007 |
| A06:2021 Vulnerable and Outdated Components | Not applicable -- skill uses no runtime dependencies. | N/A |
| A07:2021 Identification and Authentication Failures | Generated contracts have no authentication scheme by default, leaving this design choice entirely to human reviewers. | SEC-CD-003 |
| A08:2021 Software and Data Integrity Failures | PROTOTYPE label protection mechanism has a bypass scenario (x-prototype: false not explicitly caught). | SEC-CD-007 |
| A09:2021 Security Logging and Monitoring Failures | Rejection messages are actionable. Mapping document provides traceability. No logging specification exists for operational contract generation monitoring. | Minor gap only -- operational monitoring is out of scope for a documentation generator |
| A10:2021 Server-Side Request Forgery | Not applicable -- both agents are T2 with no network access. | N/A |

**Key insight:** The most impactful OWASP categories for /contract-design are A01 (broken access control -- because generated contracts define the access surface of future APIs), A03 (injection -- because description fields are verbatim-populated), and A05 (security misconfiguration -- because deferred features and missing security scheme generation represent configuration gaps). The skill's greatest security responsibility is to produce contracts that guide secure API implementation, which means SEC-CD-003 (missing security scheme) is the highest-priority finding despite not being a traditional "injection" or "authentication" vulnerability in the skill itself.

---

## Constitutional Compliance Verification

| Principle | cd-generator.md | cd-generator.governance.yaml | cd-validator.md | cd-validator.governance.yaml | SKILL.md | Status |
|-----------|----------------|------------------------------|-----------------|------------------------------|----------|--------|
| **P-003 (No recursive subagents)** | NEVER spawn sub-agents or use the Task tool | Forbidden actions entry 1 (NPT-009-complete) | NEVER spawn sub-agents or use the Task tool | Forbidden actions entry 1 (NPT-009-complete) | P-003 Agent Topology diagram with explicit "Workers do NOT invoke each other" | **PASS** |
| **P-020 (User authority)** | NEVER override user decisions about contract scope, operation granularity, resource naming | Forbidden actions entry 2 (NPT-009-complete). PROTOTYPE removal is user decision. | NEVER override user decisions about validation scope, acceptance criteria | Forbidden actions entry 2 (NPT-009-complete) | PROTOTYPE label removal is user decision (Output Quality Gate section) | **PASS** |
| **P-022 (No deception)** | NEVER misrepresent contract completeness or traceability. Confidence annotations on HTTP method inference. Unmapped interactions explicitly reported. | Forbidden actions entry 3 (NPT-009-complete) | NEVER misrepresent validation results. Report every gap with specific evidence. No softening of FAIL verdicts. | Forbidden actions entry 3 (NPT-009-complete) | G-01 (no prior art) acknowledged. Confidence annotations documented. | **PASS** |
| **P-001 (Truth/Accuracy)** | Every mapping traces to UC schema field or RFC 9110. No invented operations. | principles_applied: P-001 | FAIL verdicts cite specific evidence | principles_applied: P-001 | Traceability algorithm documented | **PASS** |
| **P-002 (File Persistence)** | All outputs to files; no inline-only responses | principles_applied: P-002 | Validation report to file | principles_applied: P-002 | Output Artifacts section specifies file paths | **PASS** |

**Constitutional triplet verification result: ALL PASS.** Both agents carry the complete P-003/P-020/P-022 triplet in their forbidden_actions (NPT-009-complete format) and constitution.principles_applied arrays. The SKILL.md reinforces constitutional compliance through the P-003 topology diagram and user-authority language in the PROTOTYPE removal workflow.

**Additional constitutional integrity observation:** The cd-generator composition file (`cd-generator.agent.yaml`) includes `forbidden: [agent_delegate]` in the tools section, providing a structural enforcement layer for P-003 beyond the behavioral guardrail. This is consistent with the H-34 intent.

---

## H-34/H-35 Compliance Checklist

| Requirement | cd-generator | cd-validator | Evidence | Status |
|-------------|-------------|-------------|---------|--------|
| Dual-file (.md + .governance.yaml) | cd-generator.md + cd-generator.governance.yaml | cd-validator.md + cd-validator.governance.yaml | Both pairs exist at correct paths | PASS |
| Official .md frontmatter only | name, description, model, tools | name, description, model, tools | No non-standard fields in .md frontmatter | PASS |
| version (SemVer) in governance.yaml | "1.0.0" | "1.0.0" | Pattern `^\d+\.\d+\.\d+$` satisfied | PASS |
| tool_tier in governance.yaml | "T2" | "T2" | Both correct: Write tool required | PASS |
| identity.role (unique) | "API Contract Generator..." | "API Contract Validator..." | Distinct and non-empty | PASS |
| identity.expertise (min 2) | 3 entries | 3 entries | All specific | PASS |
| identity.cognitive_mode | "convergent" | "systematic" | Both valid enum values | PASS |
| forbidden_actions (min 3, P-003/P-020/P-022) | 6 entries | 4 entries | First 3 reference constitutional triplet in NPT-009-complete format | PASS |
| forbidden_action_format | "NPT-009-complete" | "NPT-009-complete" | Both declared | PASS |
| constitution.principles_applied (P-003/P-020/P-022) | P-001, P-002, P-003, P-004, P-020, P-022 | P-001, P-002, P-003, P-020, P-022 | All three required principles present | PASS |
| Task tool absent from .md tools list | [Read, Write, Edit, Glob, Grep, Bash] | [Read, Write, Edit, Glob, Grep, Bash] | Task absent from both | PASS |
| XML-tagged markdown body sections | All 7 sections present | All 7 sections present | identity, purpose, input, capabilities, methodology, output, guardrails | PASS |
| reasoning_effort declared | max (C4) | high (C3) | ET-M-001 compliant | PASS |
| guardrails.output_filtering (min 3) | 6 entries | 4 entries | Both exceed minimum | PASS |
| guardrails.fallback_behavior | "escalate_to_user" | "escalate_to_user" | Standard value per agent-development-standards | PASS |

**H-34/H-35 Overall: PASS (15/15 checks).** No blocking defects from a security enforcement perspective.

---

## Findings Table

| ID | Severity | CWE | CVSS | Title | File(s) | Prior Review? |
|----|----------|-----|------|-------|---------|---------------|
| SEC-CD-001 | MEDIUM | CWE-20, CWE-116 | 4.3 | Schema injection via verbatim natural language fields | uc-to-contract-rules.md, cd-generator.md | Partially raised as FIND-QA-006 (slug only) |
| SEC-CD-002 | LOW | CWE-209 | 3.1 | ErrorResponse source_extension field leaks internal identifiers | openapi-template.yaml, json-schema-template.json | Not previously raised |
| SEC-CD-003 | HIGH | CWE-306 | 7.5 | Missing security scheme generation in OpenAPI template | openapi-template.yaml, uc-to-contract-rules.md, cd-generator.md | Not previously raised |
| SEC-CD-004 | MEDIUM | CWE-284 | 4.4 | Deferred templates lack runtime activation guard | asyncapi-template.yaml, cloudevents-template.yaml, cd-generator.md | Not previously raised |
| SEC-CD-005 | HIGH | CWE-22 | 6.5 | Slug sanitization not enforced in output path construction | cd-generator.md, cd-generator.governance.yaml | FIND-QA-006 (LOW -- this review upgrades to HIGH) |
| SEC-CD-006 | LOW | CWE-400 | 3.1 | No volume bound on interaction count | cd-generator.md, cd-generator.governance.yaml | Not previously raised |
| SEC-CD-007 | MEDIUM | CWE-693 | 5.3 | PROTOTYPE label bypass via x-prototype: false not caught | cd-validator.md, uc-to-contract-rules.md | Not previously raised |

### Severity Justification Notes

**SEC-CD-003 (HIGH):** Elevated from what might otherwise be a MEDIUM documentation gap because the absence of security scheme generation creates a systematic omission across every contract produced by the skill. The downstream effect -- API implementations built without authentication models -- has HIGH confidentiality impact when such implementations reach production.

**SEC-CD-005 (HIGH from QA's LOW):** The eng-qa review identified the slug sanitization gap as a LOW naming issue. This review elevates to HIGH because the specific failure mode is path traversal (CWE-22), which can escape the intended output directory. The attack is bounded (internal UC authors, file writes only), which prevents elevation to CRITICAL.

**SEC-CD-007 (MEDIUM):** The PROTOTYPE bypass scenario is a protection mechanism failure, but requires an attacker who already has write access to the generated contract file. The impact is bounded to preventing false validation outcomes rather than enabling direct data exfiltration.

---

## Recommendations

### Priority 1 (Before Production Deployment -- Blocking)

| Rec | Finding | Action | Effort |
|-----|---------|--------|--------|
| R-SEC-01 | SEC-CD-003 | Add `securitySchemes` placeholder to `openapi-template.yaml` and add RULE-SEC-01 to `uc-to-contract-rules.md` | Low (template edit + rule addition) |
| R-SEC-02 | SEC-CD-005 | Add slug sanitization constraint to `cd-generator.governance.yaml` output_filtering and sanitization logic to methodology Step 9 | Low (governance edit + methodology note) |

### Priority 2 (Before End-to-End Pipeline Validation)

| Rec | Finding | Action | Effort |
|-----|---------|--------|--------|
| R-SEC-03 | SEC-CD-004 | Add output format check to cd-generator input validation gate (reject non-.openapi.yaml output paths) | Low (guardrail addition) |
| R-SEC-04 | SEC-CD-007 | Update cd-validator Step 7 to explicitly fail on `x-prototype: false` (not just `x-prototype` absent) | Low (methodology wording update) |

### Priority 3 (Before Broad Skill Distribution)

| Rec | Finding | Action | Effort |
|-----|---------|--------|--------|
| R-SEC-05 | SEC-CD-001 | Add HTML/YAML sanitization requirement to RULE-SD-01 and RULE-SD-02 description field emission | Low (rule wording addition) |
| R-SEC-06 | SEC-CD-002 | Mark `source_extension` as internal-only in ErrorResponse schema templates | Low (template annotation) |
| R-SEC-07 | SEC-CD-006 | Add 50-interaction upper bound to input_validation and CD_SKILL_CONTRACT.yaml GeneratorInput schema | Low (schema field update) |

### Note on FIND-QA-003 Carryforward

The eng-qa review identified FIND-QA-003: "Layer 2 guardrail uses `detail_level` field name instead of `realization_level`." This is a correctness defect, not a security finding. However, it affects input validation gate effectiveness: if the guardrail checks the wrong field name, the validation fails silently and a UC artifact at an incorrect realization level may pass the Layer 2 gate. This indirectly affects security by weakening the input validation boundary (SEC-CD-001 and SEC-CD-005 become more exploitable when the input validation gate has a field name error). Remediation of FIND-QA-003 from eng-qa is prerequisite to the security input validation gate functioning as designed.

---

## L2: Strategic Implications

### Security Posture Relative to Production Deployment

The `/contract-design` skill is **not production-ready for unreviewed contract consumption**, which is the correct and intentional design. The PROTOTYPE labeling system (RULE-TR-02, cd-validator Step 7) is the most important security control in the skill and it functions correctly. The skill is appropriately designed for internal use within a trusted framework where UC artifact authors are team members.

The security findings raised in this review represent the gap between the skill's current state and production readiness for broader team distribution:

1. **SEC-CD-003 (missing security scheme)** is the most consequential for production deployment. When contracts are eventually used to guide API implementation, the lack of an authentication model template means security architecture decisions are deferred entirely to human reviewers who may lack the OpenAPI schema knowledge to add securitySchemes correctly. Adding a placeholder scheme is low-cost and shifts this from "security decision deferred" to "security decision guided."

2. **SEC-CD-005 (path traversal)** is the most acute risk if the skill is used in a multi-tenant or CI/CD context where UC artifacts could be supplied by less-trusted sources. In the current single-team context, the risk is bounded but the remediation is sufficiently low-effort that it should not be deferred.

3. **SEC-CD-004 (deferred template bypass)** represents technical debt that will grow in risk as the framework matures. The deferred AsyncAPI/CloudEvents generation represents design work (G-02) that is unresolved, not capability that is ready but disabled. Converting the behavioral guardrail to a structural gate prevents future model updates from accidentally activating untested transformation logic.

### Systemic Pattern Observations

This review identifies a pattern consistent with the prior security review of `/test-spec` (step-10-eng-security-review.md): **description-field verbatim emission** is a recurring risk class across skills that transform natural language UC artifacts into machine-readable specifications. The RULE-SD-01/RULE-SD-02 verbatim emission pattern (SEC-CD-001) is analogous to the verbatim step text emission found in the test-spec skill. A framework-level policy prohibiting verbatim emission without sanitization would address this pattern across all current and future transformation skills.

### PROTOTYPE Label as Defense-in-Depth

The PROTOTYPE labeling system, while not a traditional "security control," functions as an effective defense-in-depth mechanism against the most significant risk (R-01 from the risk register: novel algorithm producing incorrect contracts). The mandatory label + mandatory human review before removal creates a human-in-the-loop checkpoint that compensates for the inherent uncertainty of the novel UC-to-contract transformation algorithm. This architectural decision deserves recognition as a security design pattern that Jerry Framework should codify for all skills producing artifacts that will feed downstream automation (code generators, API gateways, test runners).

### Comparison with Threat Model

The architecture's threat model (Section 8) identified three primary threats:

1. **UC artifact with crafted interaction descriptions (DREAD 9/25)** -- This review maps to SEC-CD-001 and SEC-CD-005. The architecture identified the risk correctly but assessed it as Medium. The path traversal dimension (SEC-CD-005) warrants HIGH severity.

2. **External consumers treating PROTOTYPE as production-ready (DREAD 14/25)** -- The architecture's mitigation is correct. This review adds SEC-CD-007 as a refinement: the bypass scenario via `x-prototype: false` is a subtlety the architecture did not explicitly address.

3. **Generated contract omits error responses (DREAD 10/25)** -- This risk is well-mitigated by the existing extension-to-error-response mapping algorithm and cd-validator Step 5. No new security finding in this area.

This review adds two high-severity findings the architecture's threat model did not cover: SEC-CD-003 (missing security scheme -- an omission rather than an attack) and SEC-CD-005 (path traversal via slug -- identified in eng-qa but severity underweighted).

---

## S-010 Self-Review Checklist

| Check | Criterion | Status |
|-------|-----------|--------|
| All 17 files reviewed | Each file read and analyzed for security-relevant content | PASS -- all 17 files read directly |
| No findings duplicate prior reviews | Each finding checked against eng-lead and eng-qa findings tables | PASS -- SEC-CD-005 escalation from FIND-QA-006 documented; all others are new |
| CWE IDs verified | Each finding mapped to a CWE Top 25 2025 or related CWE | PASS |
| CVSS scores calibrated | Each score reflects the bounded attack surface (internal tooling, T2 agents, LLM trust model) | PASS |
| Constitutional triplet verified across all files | P-003, P-020, P-022 checked in both .md and .governance.yaml for both agents | PASS |
| OWASP ASVS 5.0 chapters addressed | All 9 chapters assessed for applicability | PASS |
| OWASP Top 10 2021 mapped | All 10 categories assessed for relevance | PASS |
| Remediation actions are specific and actionable | Each recommendation specifies exact file, field, and content to change | PASS |
| Severity justifications documented | HIGH/MEDIUM findings include rationale for severity level | PASS -- SEC-CD-003 and SEC-CD-005 elevations documented |
| Prior review pattern followed | Structure matches step-10-eng-security-review.md pattern | PASS |
| L0/L1/L2 three-level output structure | All three levels present | PASS |
| H-23 navigation table | Navigation table present with anchor links | PASS |
| P-002 file persistence | Output written to specified path | PASS (this file) |
| No secrets in output | No passwords, tokens, PII, or credentials in this document | PASS |
| Confidence indicator present | 0.91 declared in document header with rationale | PASS |
