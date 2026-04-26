---
template: e2e-governance-config.md
version: 1.0.0
operationalizes_principles: [P-E2E-05, P-E2E-08, P-E2E-10]
produced_by: eng-qa (Phase 4 Step B); consumed by adopters of the skill when configuring their e2e-testing deployment
consumed_by: all agents at invocation (YAML parsed and passed to every agent prompt at run start)
inputs:
  - user-supplied overrides or defaults at invocation time
outputs:
  - "output/{testrun-id}/governance-config.yaml"
---

# Template: E2E Governance Configuration

## Document Sections

| Section | Purpose |
|---------|---------|
| [Purpose](#purpose) | What this template produces |
| [When to Use](#when-to-use) | When to generate or modify governance config |
| [Input Parameters](#input-parameters) | All configurable fields with types and defaults |
| [Template Body](#template-body) | The YAML governance block with populated placeholders |
| [Expected Output](#expected-output) | Output format and validation |
| [Validation Rules](#validation-rules) | Field-level validation rules applied at load time |
| [Example](#example) | Two complete worked examples (default and security-hardened) |
| [Source](#source) | Principle and architecture traceability |

---

## Purpose

Generate a validated per-run governance YAML block that controls every parameter of a `/e2e-testing` execution. This is the R-011-equivalent configuration interface for the skill: it declares execution mode (P-E2E-05), WSTG mandatory categories (P-E2E-08), autonomy tier (P-E2E-10), quality thresholds (RT-004), SPA wait strategy, and Playwright MCP version pin. Every agent reads this config at invocation start. Any field absent from governance config is a blocking error -- agents do not use implicit defaults except where this template explicitly marks a field as optional with a documented default.

This template is also the artifact adopters of the skill customise when deploying `/e2e-testing` for their project. Walk an adopter through completing this config before running the first test.

---

## When to Use

Invoke this template to:
- Generate a `governance-config.yaml` at the start of a new test run (testrun-id assignment step)
- Override any default for a specific engagement (e.g., add webkit browser, change autonomy tier to SUPERVISED, enable ISO 29119 artifacts)
- Audit an existing governance config for compliance with current field validation rules
- Onboard a new project to `/e2e-testing` (walk through each field with the adopter)

---

## Input Parameters

| Parameter | Type | Required | Description | Default |
|-----------|------|----------|-------------|---------|
| `TESTRUN_ID` | string | YES | Run identifier matching `^E2E-\d{4}$` | none -- must be supplied |
| `EXECUTION_MODE` | enum | YES | `codegen` or `explorer` | `codegen` (P-E2E-05: codegen is default for C2+ flows) |
| `AUTONOMY_TIER` | enum | YES | `AUTONOMOUS`, `SUPERVISED`, or `MANAGED-EQUIVALENT` | none -- must be explicitly supplied; no silent default (P-E2E-10 / P-022) |
| `BROWSERS` | array | NO | Subset of `[chromium, firefox, webkit]` | `[chromium, firefox]` |
| `VIEWPORTS` | array | NO | Array of `{width, height}` objects | `[{width: 1280, height: 720}]` |
| `RETRY_COUNT` | integer | NO | Browser-level retries in codegen mode (0 = no retry for determinism) | `0` |
| `SCREENSHOT_ON_FAILURE` | boolean | NO | Capture screenshot at failure point | `true` |
| `TRACE_ON_FAILURE` | boolean | NO | Capture Playwright trace at failure point | `true` |
| `VISUAL_DIFF_THRESHOLD` | float or null | NO | Pixel-diff ratio threshold; null disables visual diff | `0.02` |
| `JOURNEY_TIMEOUT_SECONDS` | integer | NO | Per-journey timeout | `30` |
| `QUALITY_THRESHOLD` | float | NO | Internal S-014 gate threshold (must be >= 0.92 SSOT floor) | `0.94` (RT-004 triangulation) |
| `ISO29119_ARTIFACTS` | boolean | NO | Generate ISO 29119-3 compatible test case specifications | `false` |
| `WSTG_MANDATORY_CATEGORIES` | array | NO | WSTG categories required in test suite; must include the six default minimums | `[ATHN, ATHZ, SESS, INPV, BUSL, APIT]` |
| `SPA_WAIT_STRATEGY` | enum | NO | Wait strategy for SPA applications: `networkidle`, `domcontentloaded`, or `custom` | `networkidle` |
| `PLAYWRIGHT_MCP_VERSION` | string | NO | Pinned version of `@playwright/mcp`; see PLAYBOOK.md for current pin | see PLAYBOOK.md (Risk 1 mitigation) |
| `SUT_ENTRY_URL` | string | NO | Base URL of the system under test | none -- required per-run by e2e-author |

---

## Template Body

```
You are generating a governance configuration for a /e2e-testing run.

Complete the following YAML block with the values provided. For any field marked
[REQUIRED], the user MUST supply a value before this config is valid. Do NOT
invent values for REQUIRED fields.

After completing the block, validate it against the field validation rules below.
If any validation fails, report the failure and ask for a corrected value.
Persist the validated block to: skills/e2e-testing/output/{{TESTRUN_ID}}/governance-config.yaml

---
# E2E Testing Governance Configuration
# Generated by: /e2e-testing (e2e-governance-config.md template)
# Testrun: {{TESTRUN_ID}}
# Source principles: P-E2E-05 (execution_mode), P-E2E-08 (wstg_mandatory_categories), P-E2E-10 (autonomy_tier)

e2e_governance:
  version: "1.0"

  # Execution identity
  testrun_id: "{{TESTRUN_ID}}"                    # [REQUIRED] Format: ^E2E-\d{4}$
  testrun_id_format: "^E2E-\\d{4}$"

  # Browser configuration
  browsers:
    - chromium
    - firefox
  # Override with: browsers: [chromium] or [chromium, firefox, webkit]

  viewports:
    - width: 1280
      height: 720
  # Override with additional viewport objects for responsive testing

  # Execution mode (P-E2E-05 HARD)
  execution_mode: "{{EXECUTION_MODE}}"            # [REQUIRED] codegen | explorer
  # codegen: produces committed .spec.ts; CI runs without LLM. Default for C2+.
  # explorer: LLM stays in loop; for self-healing and exploratory runs.

  # Reliability settings
  retry_count: 0                                  # 0 = no retry for codegen determinism
  screenshot_on_failure: true
  trace_on_failure: true
  visual_diff_threshold: 0.02                     # null to disable visual diff
  journey_timeout_seconds: 30

  # Quality gate (RT-004 triangulation; not empirically optimal -- P-022 disclosure)
  quality_threshold: 0.94                         # Must be >= 0.92 (SSOT H-13 floor)
  # Override with justification if raising above 0.94 for security-critical engagements.

  # ISO 29119 opt-in (RT-001 resolution)
  iso29119_artifacts: false                       # Set to true for regulated/enterprise contexts

  # WSTG mandatory security categories (P-E2E-08 HARD)
  # Minimum six categories required. Additional categories may be added.
  wstg_mandatory_categories:
    - ATHN   # Authentication
    - ATHZ   # Authorization
    - SESS   # Session Management
    - INPV   # Input Validation
    - BUSL   # Business Logic
    - APIT   # API Testing

  # Autonomy tier declaration (P-E2E-10 HARD / P-022 enforcement)
  autonomy_tier: "{{AUTONOMY_TIER}}"              # [REQUIRED] AUTONOMOUS | SUPERVISED | MANAGED-EQUIVALENT
  # AUTONOMOUS: agent acts without human review of individual steps; quality gate is the only backstop.
  # SUPERVISED: human reviews each generated test before execution begins.
  # MANAGED-EQUIVALENT: human engineers review and backstop AI failures post-run.
  # WARNING: If absent, ALL agents will block invocation and emit a P-022 enforcement halt.

  # SPA hardening (OQ-E2E-002 resolution from PLAYBOOK.md)
  spa_wait_strategy: networkidle
  # For SPAs: apply networkidle + waitForSelector('[data-testid=app-ready]') before DOM snapshot.
  # For Angular SPAs: also await window.getAllAngularRootElements() to resolve.
  # Override with 'domcontentloaded' for server-rendered applications.
  # Override with 'custom' and document the wait chain in the engagement notes.

  # Playwright MCP version pin (Risk 1 mitigation -- v0.0.x instability)
  playwright_mcp_version: "see PLAYBOOK.md"
  # IMPORTANT: DO NOT use 'latest'. Pin to the exact version documented in PLAYBOOK.md.
  # To upgrade: follow the upgrade SOP in PLAYBOOK.md before updating this pin.

  # Output configuration
  output_path_template: "skills/e2e-testing/output/{testrun_id}/"
  # All agent artifacts persist to this directory. Add to .gitignore for production/staging runs.

  # Secret and credential handling
  # screenshots and DOM snapshots may contain credentials or PII.
  # Review output/{testrun_id}/ before committing for runs against production systems.
  secret_scan_on_output: true

---

FIELD VALIDATION (apply before writing governance-config.yaml):

1. testrun_id: must match regex ^E2E-\d{4}$ -- reject if not
2. execution_mode: must be exactly "codegen" or "explorer" -- reject if neither
3. autonomy_tier: must be exactly "AUTONOMOUS", "SUPERVISED", or "MANAGED-EQUIVALENT" -- reject if absent or other value
4. quality_threshold: must be >= 0.92 and <= 0.99 -- reject if outside this range
5. wstg_mandatory_categories: must include at minimum all six default categories (ATHN, ATHZ, SESS, INPV, BUSL, APIT) -- warn if any default is removed (removal requires P-E2E-08 exception documented in engagement notes)
6. playwright_mcp_version: must not be "latest" or empty -- warn if set to "latest"; enforce explicit pin

If all validations pass, write the config and emit:
"governance-config.yaml VALIDATED AND PERSISTED: skills/e2e-testing/output/{{TESTRUN_ID}}/governance-config.yaml"

If any validation fails, report the failure, ask for corrected value, and re-validate before writing.
```

---

## Expected Output

**`governance-config.yaml`** at `skills/e2e-testing/output/{testrun_id}/governance-config.yaml`:
- All mandatory fields populated with validated values
- No absent REQUIRED fields
- Autonomy tier declared (P-E2E-10 enforcement)
- Playwright MCP version pinned to explicit version (not "latest")
- WSTG mandatory categories include all six defaults

---

## Validation Rules

| Rule | Principle | Check |
|------|-----------|-------|
| `testrun_id` matches `^E2E-\d{4}$` | implementation-plan Section 4 | Regex reject |
| `execution_mode` is `codegen` or `explorer` | P-E2E-05 | Enum reject |
| `autonomy_tier` is one of three valid values | P-E2E-10 / P-022 | Reject if absent or invalid; blocking |
| `quality_threshold` >= 0.92 | H-13 (SSOT floor) | Reject if below floor |
| `quality_threshold` <= 0.99 | sanity check | Warn if above 0.99 (likely config error) |
| `wstg_mandatory_categories` includes all six defaults | P-E2E-08 | Warn if any default removed |
| `playwright_mcp_version` is not "latest" or empty | Risk 1 mitigation | Warn and require explicit pin |

---

## Example

### Example 1: Default Configuration (new project onboarding)

```yaml
e2e_governance:
  version: "1.0"
  testrun_id: "E2E-0001"
  testrun_id_format: "^E2E-\\d{4}$"
  browsers: [chromium, firefox]
  viewports:
    - {width: 1280, height: 720}
  execution_mode: "codegen"
  retry_count: 0
  screenshot_on_failure: true
  trace_on_failure: true
  visual_diff_threshold: 0.02
  journey_timeout_seconds: 30
  quality_threshold: 0.94
  iso29119_artifacts: false
  wstg_mandatory_categories: [ATHN, ATHZ, SESS, INPV, BUSL, APIT]
  autonomy_tier: "SUPERVISED"
  spa_wait_strategy: networkidle
  playwright_mcp_version: "0.0.70"
  output_path_template: "skills/e2e-testing/output/{testrun_id}/"
  secret_scan_on_output: true
```

Validation result: PASS on all 7 rules.
Persisted to: `skills/e2e-testing/output/E2E-0001/governance-config.yaml`

### Example 2: Security-Hardened Configuration (regulated enterprise context)

```yaml
e2e_governance:
  version: "1.0"
  testrun_id: "E2E-0015"
  testrun_id_format: "^E2E-\\d{4}$"
  browsers: [chromium, firefox, webkit]
  viewports:
    - {width: 1280, height: 720}
    - {width: 375, height: 812}
  execution_mode: "codegen"
  retry_count: 0
  screenshot_on_failure: true
  trace_on_failure: true
  visual_diff_threshold: 0.01
  journey_timeout_seconds: 60
  quality_threshold: 0.94
  iso29119_artifacts: true
  wstg_mandatory_categories: [ATHN, ATHZ, SESS, INPV, BUSL, APIT, CRYP, CLNT]
  autonomy_tier: "MANAGED-EQUIVALENT"
  spa_wait_strategy: networkidle
  playwright_mcp_version: "0.0.70"
  output_path_template: "skills/e2e-testing/output/{testrun_id}/"
  secret_scan_on_output: true
```

Key differences from default:
- Added webkit for cross-browser coverage
- Added mobile viewport 375x812
- Tighter visual diff threshold (0.01)
- Extended timeout for complex regulated flows (60s)
- ISO 29119 artifacts enabled (regulated context)
- Extended WSTG categories: CRYP and CLNT added beyond the six mandatory defaults
- Autonomy tier MANAGED-EQUIVALENT: human engineers review and backstop post-run

Validation result: PASS on all 7 rules. wstg_mandatory_categories extends beyond defaults (PASS; additions are additive, not removals).

---

## Source

| Item | Source |
|------|--------|
| Execution mode field and defaults | P-E2E-05 (HARD); implementation-plan Section 3 governance default block |
| WSTG mandatory categories field | P-E2E-08 (HARD); requirements §2 P-E2E-08; implementation-plan Section 3 |
| Autonomy tier field as P-022 enforcement | P-E2E-10 (HARD); requirements §2 P-E2E-10; skill-architecture Section 8 |
| Quality threshold 0.94 | RT-004 triangulation; requirements §3 RT-004; implementation-plan Section 4 quality field |
| ISO 29119 opt-in flag | RT-001 resolution; requirements §3 RT-001 |
| SPA wait strategy `networkidle` default | OQ-E2E-002 resolution; implementation-plan Section 1 PLAYBOOK.md rationale |
| Playwright MCP version pin | Risk 1 (Playwright MCP version instability); implementation-plan Section 8 Risk 1 |
| Section skeleton | skill-architecture Section 3.5 |
| Field validation rules | skill-architecture Section 3.5 validation rules |
| AGPL-3.0 guardrail (no_skyvern_source_code) | implementation-plan Section 8 Risk 2; requirements §8 Skyvern MIRROR posture |
