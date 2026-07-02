---
DISCLAIMER: This guidance is AI-generated based on NASA Systems Engineering
standards. It is advisory only and does not constitute official NASA guidance.
All SE decisions require human review and professional engineering judgment.
Not for use in mission-critical decisions without SME validation.
---

# Verification and Validation Plan: Configurable Output Base Path

> **Project:** PROJ-021-output-base-path
> **Entry:** nse-2
> **Date:** 2026-03-18
> **Status:** Draft
> **Source Issue:** GitHub #192 — Configurable output base path for skill agents
> **Workflow:** output-basepath-20260318-001
> **Criticality:** C3 (Significant) — quality threshold >= 0.93
> **Input Artifacts:**
> - Requirements: `nse/phase-nse-1/requirements.md`
> - ADR: `et/phase-et-1/ADR-PROJ021-001-output-path-resolution.md`
> - BARRIER-1 Handoff: `cross-pollination/barrier-1/et-to-nse/handoff.md`
> - Orchestration Plan v1.2: `ORCHESTRATION_PLAN.md`

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0: Executive Summary](#l0-executive-summary) | Verification status overview for stakeholders |
| [L1: VCRM — Verification Cross-Reference Matrix](#l1-vcrm--verification-cross-reference-matrix) | REQ-to-method mapping, procedure refs, status |
| [BDD Scenario Stubs](#bdd-scenario-stubs) | Gherkin Given/When/Then for all oracle sets |
| [Edge Case Test Assignments](#edge-case-test-assignments) | EC-001 through EC-025 mapped to test scenarios |
| [Traceability Matrix](#traceability-matrix) | AC → REQ → Test → Evidence Gate |
| [AC-3 Known Gap Documentation](#ac-3-known-gap-documentation) | Formal gap record: runtime interpolation NOT verified |
| [L2: Coverage Analysis](#l2-coverage-analysis) | Metrics, gaps, review readiness |
| [Evidence Gate Reference](#evidence-gate-reference) | Gates 1-6 from orchestration plan v1.2 |
| [References](#references) | Source document traceability |

---

## L0: Executive Summary

This V&V plan governs verification of GitHub Issue #192 (Configurable Output Base Path) for PROJ-021. Eight requirements (REQ-OBP-001 through REQ-OBP-008) with 26 sub-requirements are mapped to verification activities. Of 34 total requirement entries, 30 are verified by Test (T), 8 by Inspection (I), and 0 by Analysis only. All Must-priority requirements have verification procedures defined. One known gap exists: AC-3c (runtime interpolation of `${JERRY_OUTPUT_BASE}` in governance YAML at agent invocation time) is explicitly out of scope for this release. Every other acceptance criterion is fully verifiable through the six evidence gates defined in ORCHESTRATION_PLAN.md v1.2. Coverage risk is Low — BDD test-first (H-20) ensures procedures exist before implementation begins. The AC-3 partial satisfaction is a documented, intentional scope decision, not a verification gap.

---

## L1: VCRM — Verification Cross-Reference Matrix

### Verification Method Key

| Code | Method | Description | Evidence Type |
|------|--------|-------------|---------------|
| A | Analysis | Mathematical/logical proof or static reasoning | Analysis Report |
| D | Demonstration | Observed operation against defined criteria | Demo Record |
| I | Inspection | Visual/automated examination of artifact content | Inspection Report |
| T | Test | Execution with measurement against pass/fail oracle | Test Report (pytest output) |

### Verification Level Key

| Level | Scope |
|-------|-------|
| Unit | Single class or function in isolation |
| Integration | Multiple components exercised together |
| System | Full CLI + config stack end-to-end |

---

### REQ-OBP-001 — Config Set Persistence (AC-1)

| Req ID | Requirement (abbreviated) | V-Method | V-Level | Procedure | Status | Evidence Gate | Notes |
|--------|---------------------------|----------|---------|-----------|--------|---------------|-------|
| REQ-OBP-001 | `jerry config set output.base_path` persists to TOML | T | System | TS-001 | Not Started | Gate 3 | CLI round-trip |
| REQ-OBP-001a | Root scope writes to `.jerry/config.toml [output]` | T | System | TS-001-a | Not Started | Gate 3 | Inspect TOML after set |
| REQ-OBP-001b | Project scope writes to project config file | T | System | TS-001-b | Not Started | Gate 3 | JERRY_PROJECT required |
| REQ-OBP-001c | Exit 0 on success; prints key, coerced value, scope, file | T | System | TS-001-c | Not Started | Gate 3 | OR-001, OR-006 |
| REQ-OBP-001d | Root scope works without JERRY_PROJECT | T | System | TS-001-d | Not Started | Gate 3 | OR-001 unset env |
| REQ-OBP-001e | Project scope fails gracefully without JERRY_PROJECT | T | System | TS-001-e | Not Started | Gate 3 | OR-005; exit code 1 |

### REQ-OBP-002 — Config Get Retrieval (AC-2)

| Req ID | Requirement (abbreviated) | V-Method | V-Level | Procedure | Status | Evidence Gate | Notes |
|--------|---------------------------|----------|---------|-----------|--------|---------------|-------|
| REQ-OBP-002 | `jerry config get output.base_path` retrieves with correct precedence | T | System | TS-002 | Not Started | Gate 3 | |
| REQ-OBP-002a | Prints value exactly as stored | T | System | TS-002-a | Not Started | Gate 3 | OR-002, OR-004 |
| REQ-OBP-002b | Honors env > project > root > defaults precedence | T | System | TS-002-b | Not Started | Gate 3 | OR-107 pattern |
| REQ-OBP-002c | Prints absence message and exits code 1 when key absent | T | System | TS-002-c | Not Started | Gate 3 | OR-003 |
| REQ-OBP-002d | `--json` flag outputs key/value/source JSON | T | System | TS-002-d | Not Started | Gate 3 | Should-priority |

### REQ-OBP-003 — OutputResolver Application Service (AC-3 implementable scope)

| Req ID | Requirement (abbreviated) | V-Method | V-Level | Procedure | Status | Evidence Gate | Notes |
|--------|---------------------------|----------|---------|-----------|--------|---------------|-------|
| REQ-OBP-003 | OutputResolver with 4-step fallback chain | T | Unit + Integration | TU-003 | Not Started | Gates 4, 5 | |
| REQ-OBP-003a | `resolve()` always returns string ending with `/` | T | Unit | TU-003-a | Not Started | Gate 4 | OR-101 through OR-106 |
| REQ-OBP-003b | Resides in application layer; no infra imports | I | — | IP-003-b | Not Started | Gate 4 | Import graph inspection |
| REQ-OBP-003c | OutputBasePath VO rejects null bytes; permits empty | T | Unit | TU-003-c | Not Started | Gate 4 | OR-301 through OR-304 |
| REQ-OBP-003d | Explicit config takes highest priority (non-empty first) | T | Unit | TU-003-d | Not Started | Gate 4 | OR-101, OR-102 |
| REQ-OBP-003e | JERRY_PROJECT fallback returns `projects/{id}/` | T | Unit | TU-003-e | Not Started | Gate 4 | OR-103 |
| REQ-OBP-003f | Terminal fallback returns `work/` | T | Unit | TU-003-f | Not Started | Gate 4 | OR-105, OR-106 |
| REQ-OBP-003g | `output.base_path` default is `None` in LayeredConfigAdapter | T | Unit | TU-003-g | Not Started | Gate 4 | |
| REQ-OBP-003h | Resolver propagates ValueError; no silent fallback on invalid | T | Unit | TU-003-h | Not Started | Gate 4 | OR-303; null byte propagation |

### REQ-OBP-004 — Governance YAML Token Placement (AC-3 YAML scope)

| Req ID | Requirement (abbreviated) | V-Method | V-Level | Procedure | Status | Evidence Gate | Notes |
|--------|---------------------------|----------|---------|-----------|--------|---------------|-------|
| REQ-OBP-004 | All 6 governance YAMLs use `${JERRY_OUTPUT_BASE}` token | I | — | IP-004 | Not Started | Gate 2 (audit) + Gate 5 | OR-201 through OR-205 |
| REQ-OBP-004a | All 6 YAML files have `output.location` updated to token pattern | I | — | IP-004-a | Not Started | Gate 5 | OR-201 through OR-204 |
| REQ-OBP-004b | Token has no trailing slash in YAML; slash owned by resolver | I | — | IP-004-b | Not Started | Gate 5 | YAML diff inspection |
| REQ-OBP-004c | `fallback_location` field absent from all 6 YAML files | I | — | IP-004-c | Not Started | Gate 2 + Gate 5 | OR-202; grep audit |
| REQ-OBP-004d | All 6 YAML files pass schema validation after edit | T | System | TS-004-d | Not Started | Gate 5 | Schema: agent-governance-v1.schema.json |
| REQ-OBP-004e | No other YAML fields modified | I | — | IP-004-e | Not Started | Gate 5 | Diff review |

### REQ-OBP-005 — Project-Based Fallback (AC-4)

| Req ID | Requirement (abbreviated) | V-Method | V-Level | Procedure | Status | Evidence Gate | Notes |
|--------|---------------------------|----------|---------|-----------|--------|---------------|-------|
| REQ-OBP-005 | Resolver returns `projects/{JERRY_PROJECT}/` when no config | T | Unit | TU-005 | Not Started | Gate 4 | OR-103 |
| REQ-OBP-005a | Directory existence not validated by resolver | T | Unit | TU-005-a | Not Started | Gate 4 | Non-existent project ID |
| REQ-OBP-005b | `get_project_data_path()` delegates to resolver | T | Integration | TI-005-b | Not Started | Gate 5 | Bootstrap integration test |

### REQ-OBP-006 — Terminal Fallback to work/ (AC-5)

| Req ID | Requirement (abbreviated) | V-Method | V-Level | Procedure | Status | Evidence Gate | Notes |
|--------|---------------------------|----------|---------|-----------|--------|---------------|-------|
| REQ-OBP-006 | Resolver returns `work/` when nothing configured | T | Unit | TU-006 | Not Started | Gate 4 | OR-105 |
| REQ-OBP-006a | Returns exactly `"work/"` | T | Unit | TU-006-a | Not Started | Gate 4 | OR-106 exact string |
| REQ-OBP-006b | Empty-string JERRY_PROJECT treated as absent | T | Unit | TU-006-b | Not Started | Gate 4 | OR-106 |

### REQ-OBP-007 — Bootstrap Integration

| Req ID | Requirement (abbreviated) | V-Method | V-Level | Procedure | Status | Evidence Gate | Notes |
|--------|---------------------------|----------|---------|-----------|--------|---------------|-------|
| REQ-OBP-007 | Bootstrap wires LayeredConfigAdapter into OutputResolver | T + I | Integration | TI-007 | Not Started | Gate 5 | Wiring inspection + integration test |

### REQ-OBP-008 — Test Coverage Requirement

| Req ID | Requirement (abbreviated) | V-Method | V-Level | Procedure | Status | Evidence Gate | Notes |
|--------|---------------------------|----------|---------|-----------|--------|---------------|-------|
| REQ-OBP-008 | >= 90% line coverage on `output_base_path.py` and `output_resolver.py` | T | Unit | TC-008 | Not Started | Gate 6 | `pytest --cov` report |

---

## BDD Scenario Stubs

All scenarios are written in RED phase (test-first, H-20). Implementation in et-2 must turn these RED before going GREEN.

### Suite TS-001: CLI Config Set (Oracle Set 1, AC-1)

```gherkin
Feature: jerry config set output.base_path persists to TOML
  As a framework user
  I want to set an output base path that persists across sessions
  So that all skill agents write to my preferred directory without manual correction

  # OR-001
  Scenario: TS-001-a Root scope writes to .jerry/config.toml under [output] section
    Given no output.base_path is configured in any config source
    And JERRY_PROJECT is not set in the environment
    When I run "jerry config set output.base_path work/ --scope root"
    Then the command exits with code 0
    And .jerry/config.toml contains the [output] section
    And .jerry/config.toml [output] base_path equals "work/"
    And stdout contains "output.base_path"
    And stdout contains "work/"
    And stdout contains "root"
    And stdout contains ".jerry/config.toml"

  # OR-006
  Scenario: TS-001-b Project scope writes to projects/{project}/.jerry/config.toml
    Given JERRY_PROJECT is set to "PROJ-021"
    When I run "jerry config set output.base_path custom/ --scope project"
    Then the command exits with code 0
    And "projects/PROJ-021/.jerry/config.toml" contains [output] base_path = "custom/"
    And stdout contains "projects/PROJ-021/.jerry/config.toml"

  # OR-001 + REQ-OBP-001c
  Scenario: TS-001-c Successful set prints key, coerced value, scope, and target file
    Given no prior output.base_path configuration
    When I run "jerry config set output.base_path work/ --scope root"
    Then the command exits with code 0
    And stdout contains the key "output.base_path"
    And stdout contains the coerced value "work/"
    And stdout contains the scope "root"
    And stdout contains the config file path

  # OR-001 unset env + REQ-OBP-001d
  Scenario: TS-001-d Root scope succeeds without JERRY_PROJECT
    Given JERRY_PROJECT is not set in the environment
    When I run "jerry config set output.base_path work/ --scope root"
    Then the command exits with code 0

  # OR-005 + REQ-OBP-001e
  Scenario: TS-001-e Project scope fails gracefully without JERRY_PROJECT
    Given JERRY_PROJECT is not set in the environment
    When I run "jerry config set output.base_path custom/ --scope project"
    Then the command exits with code 1
    And stdout or stderr contains "No active project"
```

### Suite TS-002: CLI Config Get (Oracle Set 1, AC-2)

```gherkin
Feature: jerry config get output.base_path retrieves correct value

  # OR-002
  Scenario: TS-002-a Prints value exactly as stored after set
    Given output.base_path is set to "work/" via "jerry config set --scope root"
    When I run "jerry config get output.base_path"
    Then the command exits with code 0
    And stdout is exactly "work/"

  # OR-004
  Scenario: TS-002-a2 Round-trip with project-based path
    Given output.base_path is set to "projects/PROJ-021/" via "jerry config set --scope root"
    When I run "jerry config get output.base_path"
    Then the command exits with code 0
    And stdout is exactly "projects/PROJ-021/"

  # REQ-OBP-002b + OR-107 pattern
  Scenario: TS-002-b Environment variable JERRY_OUTPUT__BASE_PATH overrides file config
    Given output.base_path is set to "file-value/" in root config
    And the environment variable JERRY_OUTPUT__BASE_PATH is set to "/env/override/"
    When I run "jerry config get output.base_path"
    Then the command exits with code 0
    And stdout is exactly "/env/override/"

  # OR-003 + REQ-OBP-002c
  Scenario: TS-002-c Key absent prints message and exits code 1
    Given no output.base_path is configured in any source
    And JERRY_OUTPUT__BASE_PATH is not set
    When I run "jerry config get output.base_path"
    Then the command exits with code 1
    And stdout contains "Key 'output.base_path' not found."

  # REQ-OBP-002d (Should-priority)
  Scenario: TS-002-d JSON flag outputs structured object
    Given output.base_path is set to "work/" in root config
    When I run "jerry config get output.base_path --json"
    Then the command exits with code 0
    And stdout is valid JSON
    And the JSON object contains field "key" with value "output.base_path"
    And the JSON object contains field "value" with value "work/"
    And the JSON object contains field "source"
```

### Suite TU-003: OutputResolver Unit Tests (Oracle Set 2, AC-3/4/5)

```gherkin
Feature: OutputResolver resolves output base path via 4-step fallback chain

  # OR-101 + REQ-OBP-003d
  Scenario: TU-003-d Explicit config with trailing slash takes highest priority
    Given the config provider returns "custom/output/" for key "output.base_path"
    And JERRY_PROJECT is set to "PROJ-001"
    When OutputResolver.resolve() is called
    Then the result is "custom/output/"

  # OR-102 + REQ-OBP-003a
  Scenario: TU-003-a Explicit config without trailing slash gets slash appended
    Given the config provider returns "custom/output" (no trailing slash) for key "output.base_path"
    When OutputResolver.resolve() is called
    Then the result is "custom/output/"

  # OR-103 + REQ-OBP-003e
  Scenario: TU-003-e JERRY_PROJECT fallback when no config set
    Given the config provider returns None for key "output.base_path"
    And JERRY_PROJECT is set to "PROJ-021"
    When OutputResolver.resolve() is called
    Then the result is "projects/PROJ-021/"

  # OR-104 + REQ-OBP-003d
  Scenario: TU-003-d2 Empty string config treated as not configured
    Given the config provider returns "" (empty string) for key "output.base_path"
    And JERRY_PROJECT is set to "PROJ-021"
    When OutputResolver.resolve() is called
    Then the result is "projects/PROJ-021/"

  # OR-105 + REQ-OBP-003f
  Scenario: TU-003-f Terminal work/ fallback when neither config nor JERRY_PROJECT set
    Given the config provider returns None for key "output.base_path"
    And JERRY_PROJECT is not set in the environment
    When OutputResolver.resolve() is called
    Then the result is "work/"

  # OR-106 + REQ-OBP-006b
  Scenario: TU-003-f2 Empty string JERRY_PROJECT treated as absent
    Given the config provider returns None for key "output.base_path"
    And JERRY_PROJECT is set to ""
    When OutputResolver.resolve() is called
    Then the result is "work/"

  # OR-107 + REQ-OBP-002b
  Scenario: TU-003-d3 Env var override reaches resolver through config provider
    Given JERRY_OUTPUT__BASE_PATH is set to "/env/path/"
    And the config provider reflects env layer (env > project > root > defaults)
    When OutputResolver.resolve() is called
    Then the result is "/env/path/"

  # REQ-OBP-003g
  Scenario: TU-003-g output.base_path default is None in LayeredConfigAdapter
    Given LayeredConfigAdapter is initialized with standard defaults
    And "output.base_path" has not been set in any config file or env var
    When config_adapter.get("output.base_path") is called
    Then the result is None (not KeyError, not empty string)

  # REQ-OBP-003h + OR-303
  Scenario: TU-003-h Resolver propagates ValueError from OutputBasePath on null byte
    Given the config provider returns a string containing "\x00" for key "output.base_path"
    When OutputResolver.resolve() is called
    Then a ValueError is raised
    And the resolver does NOT fall back to the next chain step

  # REQ-OBP-003b
  Scenario: TU-003-b OutputResolver imports only from domain and port (no infra)
    When the import graph of output_resolver.py is inspected
    Then it contains imports from "configuration.domain.value_objects.output_base_path"
    And it contains an import of "IConfigurationProvider" (Protocol)
    And it does NOT contain any import from "infrastructure.adapters"
    And it does NOT contain any import from "LayeredConfigAdapter" directly
```

### Suite TU-003-c: OutputBasePath Value Object (Oracle Set 4, REQ-OBP-003c)

```gherkin
Feature: OutputBasePath value object validates and normalizes paths

  # OR-301
  Scenario: TU-003-c1 Valid relative path with trailing slash constructs without error
    When OutputBasePath("work/") is constructed
    Then no exception is raised
    And the .value attribute equals "work/"

  # OR-302
  Scenario: TU-003-c2 Empty string constructs without error (triggers resolver fallback)
    When OutputBasePath("") is constructed
    Then no exception is raised
    And the .value attribute equals ""

  # OR-303 + REQ-OBP-003c
  Scenario: TU-003-c3 Null byte in path raises ValueError
    When OutputBasePath("path\x00with-null") is constructed
    Then a ValueError is raised

  # OR-304
  Scenario: TU-003-c4 Absolute path constructs without error
    When OutputBasePath("/absolute/path/") is constructed
    Then no exception is raised
    And the .value attribute equals "/absolute/path/"

  # REQ-OBP-003a
  Scenario: TU-003-c5 Path without trailing slash gets normalized to include slash
    When OutputBasePath.from_string("work") is called
    Then the resulting .value ends with "/"
    And the resulting .value equals "work/"

  # INV-4
  Scenario: TU-003-c6 Path already ending with slash is not double-slashed
    When OutputBasePath.from_string("work/") is called
    Then the resulting .value equals "work/"
    And the resulting .value does not equal "work//"
```

### Suite IP-004: Governance YAML Inspection (Oracle Set 3, AC-3 specification)

```gherkin
Feature: Governance YAML files contain correct output.location token

  # OR-201
  Scenario: IP-004-a1 uc-author.governance.yaml output.location contains ${JERRY_OUTPUT_BASE}
    Given the file "skills/use-case/agents/uc-author.governance.yaml" is loaded
    When the "output.location" field is read
    Then the value contains "${JERRY_OUTPUT_BASE}"
    And the value does NOT contain "${JERRY_PROJECT}"
    And the value does NOT contain "projects/"

  # OR-202
  Scenario: IP-004-c1 uc-author.governance.yaml has no fallback_location field
    Given the file "skills/use-case/agents/uc-author.governance.yaml" is loaded as a dict
    When the "fallback_location" key is looked up
    Then a KeyError is raised (field is absent)

  # OR-203
  Scenario: IP-004-a2 tspec-generator.governance.yaml output.location contains correct subpath
    Given the file "skills/test-spec/agents/tspec-generator.governance.yaml" is loaded
    When the "output.location" field is read
    Then the value contains "${JERRY_OUTPUT_BASE}test-specs/"

  # OR-204
  Scenario: IP-004-a3 cd-generator.governance.yaml output.location contains correct subpath
    Given the file "skills/contract-design/agents/cd-generator.governance.yaml" is loaded
    When the "output.location" field is read
    Then the value contains "${JERRY_OUTPUT_BASE}contracts/"

  # OR-205 + REQ-OBP-004d
  Scenario: IP-004-d All six governance YAML files pass schema validation
    Given the schema file "docs/schemas/agent-governance-v1.schema.json"
    When each of the six governance YAML files is validated against the schema:
      | skills/use-case/agents/uc-author.governance.yaml |
      | skills/use-case/agents/uc-slicer.governance.yaml |
      | skills/test-spec/agents/tspec-generator.governance.yaml |
      | skills/test-spec/agents/tspec-analyst.governance.yaml |
      | skills/contract-design/agents/cd-generator.governance.yaml |
      | skills/contract-design/agents/cd-validator.governance.yaml |
    Then all six files pass schema validation with no errors

  # REQ-OBP-004b
  Scenario: IP-004-b Token has no trailing slash in YAML value
    Given each of the six governance YAML files is loaded
    When the "output.location" field is read from each file
    Then "${JERRY_OUTPUT_BASE}" appears without an immediately following "/"
    And each "output.location" value matches the pattern "${JERRY_OUTPUT_BASE}{subdirectory}/..."
    Where subdirectory does not start with "/"

  # REQ-OBP-004e
  Scenario: IP-004-e No other YAML fields were modified
    Given the git diff for each of the six governance YAML files
    When the diff is inspected
    Then the only modified field is "output.location"
    And the only removed field is "fallback_location"
    And all other fields are unchanged

  # REQ-OBP-004a (uc-slicer.governance.yaml)
  Scenario: IP-004-a4 uc-slicer.governance.yaml output.location contains ${JERRY_OUTPUT_BASE}
    Given the file "skills/use-case/agents/uc-slicer.governance.yaml" is loaded
    When the "output.location" field is read
    Then the value contains "${JERRY_OUTPUT_BASE}"
    And the value does NOT contain "${JERRY_PROJECT}"

  # REQ-OBP-004a (tspec-analyst.governance.yaml)
  Scenario: IP-004-a5 tspec-analyst.governance.yaml output.location contains ${JERRY_OUTPUT_BASE}
    Given the file "skills/test-spec/agents/tspec-analyst.governance.yaml" is loaded
    When the "output.location" field is read
    Then the value contains "${JERRY_OUTPUT_BASE}test-specs/"

  # REQ-OBP-004a (cd-validator.governance.yaml)
  Scenario: IP-004-a6 cd-validator.governance.yaml output.location contains ${JERRY_OUTPUT_BASE}
    Given the file "skills/contract-design/agents/cd-validator.governance.yaml" is loaded
    When the "output.location" field is read
    Then the value contains "${JERRY_OUTPUT_BASE}contracts/"
```

### Suite TI-005: Bootstrap Integration (AC-4, REQ-OBP-005b)

```gherkin
Feature: Bootstrap wires OutputResolver and get_project_data_path delegates to it

  # REQ-OBP-005b + REQ-OBP-007
  Scenario: TI-005-b get_project_data_path delegates to OutputResolver
    Given JERRY_PROJECT is set to "PROJ-021"
    And no output.base_path is configured
    When get_project_data_path() is called from src/bootstrap.py
    Then the return value begins with "projects/PROJ-021/"
    And OutputResolver.resolve() was called internally

  # REQ-OBP-007
  Scenario: TI-007 Bootstrap wires LayeredConfigAdapter into OutputResolver
    Given a real LayeredConfigAdapter reading from the active config files
    And output.base_path is set to "my/output/" in root config
    When OutputResolver(config=LayeredConfigAdapter(...)).resolve() is called
    Then the result is "my/output/"

  # AC-3 known gap — must document in evidence/test-results-e2e.txt
  Scenario: TI-E2E-AC3a Resolver returns correct path for explicit config case
    Given output.base_path is set to "/custom/output/" via real LayeredConfigAdapter
    When OutputResolver.resolve() is called
    Then the result is "/custom/output/"
    And this test does NOT assert that agents interpolate ${JERRY_OUTPUT_BASE} at runtime

  Scenario: TI-E2E-AC3b Resolver returns correct path for JERRY_PROJECT fallback case
    Given no output.base_path is configured
    And JERRY_PROJECT is set to "PROJ-021"
    When OutputResolver.resolve() is called with real LayeredConfigAdapter
    Then the result is "projects/PROJ-021/"

  Scenario: TI-E2E-AC3c Resolver returns correct path for work/ terminal fallback case
    Given no output.base_path is configured in any source
    And JERRY_PROJECT is not set
    When OutputResolver.resolve() is called with real LayeredConfigAdapter
    Then the result is "work/"

  # REQ-OBP-005a
  Scenario: TU-005-a Resolver does not validate directory existence
    Given no output.base_path is configured
    And JERRY_PROJECT is set to "PROJ-999" (a project directory that does not exist)
    When OutputResolver.resolve() is called
    Then the result is "projects/PROJ-999/"
    And no exception is raised due to directory absence
```

### Suite TC-008: Coverage Gate (REQ-OBP-008)

```gherkin
Feature: New modules achieve >= 90% line coverage

  # REQ-OBP-008
  Scenario: TC-008 output_base_path.py achieves >= 90% line coverage
    Given all BDD scenarios in TU-003-c are implemented and passing
    When "uv run pytest tests/unit/configuration/domain/value_objects/test_output_base_path.py --cov=src/configuration/domain/value_objects/output_base_path --cov-report=term-missing" is executed
    Then the coverage report shows >= 90% line coverage for output_base_path.py

  Scenario: TC-008-b output_resolver.py achieves >= 90% line coverage
    Given all BDD scenarios in TU-003 are implemented and passing
    When "uv run pytest tests/unit/configuration/application/services/test_output_resolver.py --cov=src/configuration/application/services/output_resolver --cov-report=term-missing" is executed
    Then the coverage report shows >= 90% line coverage for output_resolver.py
```

---

## Edge Case Test Assignments

All 25 edge cases from the requirements Edge Case Catalog are assigned to specific test scenarios. Each EC entry maps to the scenario that exercises it and the evidence gate that captures the result.

### AC-1/AC-2 Config Set and Get Edge Cases

| EC ID | Edge Case Summary | Assigned Test | BDD Scenario | Evidence Gate |
|-------|-------------------|---------------|--------------|---------------|
| EC-001 | Relative path stored and retrieved exactly | TS-001-a + TS-002-a | TU-003-d (config returns relative path) | Gate 3 |
| EC-002 | Absolute path stored and retrieved exactly | TS-002-a + TU-003-d3 | TU-003-d (absolute path input) | Gate 3 + Gate 4 |
| EC-003 | Path with spaces stored as quoted TOML; retrieved with spaces | TS-002-a (space path variant) | New variant: `config set "my output/" --scope root` | Gate 3 |
| EC-004 | Path without trailing slash; resolver adds slash | TU-003-a | OR-102 scenario TU-003-a | Gate 4 |
| EC-005 | Empty string stored; resolver treats as not configured | TU-003-d2 | OR-104 scenario TU-003-d2 | Gate 4 |
| EC-006 | Second write overwrites first; get returns second value | TS-002-a (sequential set) | Two-step: set "A/", then set "B/"; get returns "B/" | Gate 3 |
| EC-007 | Project scope without JERRY_PROJECT exits code 1 | TS-001-e | OR-005 | Gate 3 |
| EC-008 | Null byte in path; ValueError propagated, not swallowed | TU-003-h | OR-303 + TU-003-h | Gate 4 |
| EC-009 | Very long path (>256 chars) stored; OS rejects at write | TU-003-c additional variant | `OutputBasePath(300-char-path)` constructs OK | Gate 4 |
| EC-010 | Path with `..` segments; VO does not normalize; security review required | TU-003-c additional variant + et-3 security | `OutputBasePath("../../etc/")` behavior documented | Gate 4 + security review |
| EC-011 | Malformed TOML; LayeredConfigAdapter returns empty dict; get returns "Key not found" | TS-002-c (malformed TOML variant) | Inject bad TOML; run config get; assert exit 1 + message | Gate 3 |
| EC-012 | Config file does not exist; get returns "Key not found" | TS-002-c | Fresh env; no .jerry/config.toml; config get exits 1 | Gate 3 |

### AC-3 OutputResolver Edge Cases

| EC ID | Edge Case Summary | Assigned Test | BDD Scenario | Evidence Gate |
|-------|-------------------|---------------|--------------|---------------|
| EC-013 | Config returns empty string; resolver proceeds to JERRY_PROJECT check | TU-003-d2 | OR-104 variant with empty string | Gate 4 |
| EC-014 | Config returns None; resolver proceeds to JERRY_PROJECT check | TU-003-e | OR-103 | Gate 4 |
| EC-015 | Path missing trailing slash; resolver appends one | TU-003-a | OR-102 | Gate 4 |
| EC-016 | Path already has trailing slash; not double-appended | TU-003-c6 | OR-101 | Gate 4 |
| EC-017 | JERRY_PROJECT set to non-existent project ID; resolver returns path without checking dir | TU-005-a | `PROJ-999` scenario | Gate 4 |
| EC-018 | JERRY_PROJECT set to empty string; terminal fallback applies | TU-003-f2 | OR-106 | Gate 4 |
| EC-019 | Env var overrides config file | TU-003-d3 + TS-002-b | OR-107 at unit level; CLI-level also | Gate 3 + Gate 4 |
| EC-020 | Project config overrides root config | TS-002-b (project vs. root) | Set root config; set project config; get returns project value | Gate 3 |
| EC-021 | Null byte in env var; ValueError propagated | TU-003-h (env var variant) | Set `JERRY_OUTPUT__BASE_PATH` to `\x00`-containing value | Gate 4 |

### AC-4/AC-5 Fallback Edge Cases

| EC ID | Edge Case Summary | Assigned Test | BDD Scenario | Evidence Gate |
|-------|-------------------|---------------|--------------|---------------|
| EC-022 | Both config and JERRY_PROJECT set; config wins | TU-003-d | OR-101 with JERRY_PROJECT also set | Gate 4 |
| EC-023 | Neither config nor JERRY_PROJECT; work/ returned | TU-003-f + TI-E2E-AC3c | OR-105 + E2E terminal fallback | Gate 4 + Gate 5 |
| EC-024 | JERRY_PROJECT with unusual characters; passed through without validation | TU-005-a (unusual chars variant) | `JERRY_PROJECT=PROJ_TEST-99`; result is `projects/PROJ_TEST-99/` | Gate 4 |
| EC-025 | Whitespace-only path value stored; resolver uses as-is (no strip); returns `"   /"` | TU-003 additional variant | `config.get()` returns `"   "`; resolver appends `/`; result is `"   /"` | Gate 4 |

---

## Traceability Matrix

This matrix traces from Acceptance Criteria (AC) through Requirements (REQ) to Test Scenarios (procedure) to Evidence Gates. Every requirement has at least one test; every AC has at least one evidence gate. Missing cells indicate scope exclusions (documented).

### AC-1: Persistent Storage

| AC | Requirement | Test Scenario | Evidence Gate | Pass Criterion |
|----|-------------|---------------|---------------|----------------|
| AC-1 | REQ-OBP-001 | TS-001 (all variants) | Gate 3 | `jerry config set` exits 0; TOML contains correct value |
| AC-1 | REQ-OBP-001a | TS-001-a | Gate 3 | `.jerry/config.toml` has `[output] base_path = "work/"` |
| AC-1 | REQ-OBP-001b | TS-001-b | Gate 3 | Project TOML has `[output] base_path = "custom/"` |
| AC-1 | REQ-OBP-001c | TS-001-c | Gate 3 | Stdout contains all 4 diagnostic fields |
| AC-1 | REQ-OBP-001d | TS-001-d | Gate 3 | Exit 0 without JERRY_PROJECT |
| AC-1 | REQ-OBP-001e | TS-001-e | Gate 3 | Exit 1 with "No active project" |

### AC-2: Config Get Retrieval

| AC | Requirement | Test Scenario | Evidence Gate | Pass Criterion |
|----|-------------|---------------|---------------|----------------|
| AC-2 | REQ-OBP-002 | TS-002 (all variants) | Gate 3 | `jerry config get` retrieves correct value with correct precedence |
| AC-2 | REQ-OBP-002a | TS-002-a | Gate 3 | Stdout equals stored value exactly |
| AC-2 | REQ-OBP-002b | TS-002-b | Gate 3 | Env var beats file config |
| AC-2 | REQ-OBP-002c | TS-002-c | Gate 3 | Exit 1, message "Key 'output.base_path' not found." |
| AC-2 | REQ-OBP-002d | TS-002-d | Gate 3 | Valid JSON with key/value/source (Should-priority) |

### AC-3: Variable Resolution (Partially Satisfied — see AC-3 Known Gap section)

| AC Sub | Requirement | Test Scenario | Evidence Gate | Pass Criterion |
|--------|-------------|---------------|---------------|----------------|
| AC-3a | REQ-OBP-003 | TU-003 (all variants) | Gate 4 | All unit tests GREEN |
| AC-3a | REQ-OBP-003a | TU-003-a | Gate 4 | `resolve()` returns string ending with `/` |
| AC-3a | REQ-OBP-003b | TU-003-b (import inspection) | Gate 4 | No infra imports in output_resolver.py |
| AC-3a | REQ-OBP-003c | TU-003-c1 through TU-003-c6 | Gate 4 | OR-301 to OR-304 exact match |
| AC-3a | REQ-OBP-003d | TU-003-d, TU-003-d2, TU-003-d3 | Gate 4 | Config value takes priority over env/project/default |
| AC-3a | REQ-OBP-003e | TU-003-e | Gate 4 | Returns `"projects/PROJ-021/"` when JERRY_PROJECT set |
| AC-3a | REQ-OBP-003f | TU-003-f, TU-003-f2 | Gate 4 | Returns `"work/"` when nothing configured |
| AC-3a | REQ-OBP-003g | TU-003-g | Gate 4 | `config.get("output.base_path")` returns None (not KeyError) |
| AC-3a | REQ-OBP-003h | TU-003-h | Gate 4 | ValueError raised; no silent fallback |
| AC-3b | REQ-OBP-004 | IP-004 (all variants) | Gate 2 + Gate 5 | YAML inspection passes; schema validates |
| AC-3b | REQ-OBP-004a | IP-004-a1 to IP-004-a6 | Gate 5 | All 6 files contain `${JERRY_OUTPUT_BASE}` in output.location |
| AC-3b | REQ-OBP-004b | IP-004-b | Gate 5 | Token has no trailing slash in YAML |
| AC-3b | REQ-OBP-004c | IP-004-c1 | Gate 2 + Gate 5 | fallback_location absent from all 6 files |
| AC-3b | REQ-OBP-004d | IP-004-d | Gate 5 | All 6 YAML files pass schema validation |
| AC-3b | REQ-OBP-004e | IP-004-e | Gate 5 | Only output.location modified; only fallback_location removed |
| AC-3c | [DEFERRED] Runtime interpolation | None (out of scope) | None | NOT VERIFIED — see AC-3 Known Gap |

### AC-4: Project-Based Fallback

| AC | Requirement | Test Scenario | Evidence Gate | Pass Criterion |
|----|-------------|---------------|---------------|----------------|
| AC-4 | REQ-OBP-005 | TU-005 + TI-E2E-AC3b | Gate 4 + Gate 5 | `resolve()` returns `projects/PROJ-021/` |
| AC-4 | REQ-OBP-005a | TU-005-a | Gate 4 | Non-existent project ID passes through |
| AC-4 | REQ-OBP-005b | TI-005-b | Gate 5 | `get_project_data_path()` calls resolver |

### AC-5: Terminal Fallback to work/

| AC | Requirement | Test Scenario | Evidence Gate | Pass Criterion |
|----|-------------|---------------|---------------|----------------|
| AC-5 | REQ-OBP-006 | TU-006 + TI-E2E-AC3c | Gate 4 + Gate 5 | `resolve()` returns `"work/"` |
| AC-5 | REQ-OBP-006a | TU-006-a | Gate 4 | Exact string `"work/"` |
| AC-5 | REQ-OBP-006b | TU-006-b | Gate 4 | Empty string JERRY_PROJECT triggers `work/` |

### Cross-Cutting Requirements

| Requirement | Test Scenario | Evidence Gate | Pass Criterion |
|-------------|---------------|---------------|----------------|
| REQ-OBP-007 (Bootstrap wiring) | TI-007 + TI-005-b | Gate 5 | Integration test passes with real adapter |
| REQ-OBP-008 (>= 90% coverage) | TC-008 + TC-008-b | Gate 6 | `pytest --cov` report >= 90% on both modules |

---

## AC-3 Known Gap Documentation

> **Gap ID:** GAP-AC3c
> **Severity:** Documented — known scope exclusion, not a defect
> **Source:** ORCHESTRATION_PLAN.md v1.2, Gate 5; BARRIER-1 handoff; requirements.md AC-3 Boundary Analysis

### Formal Gap Statement

AC-3 as stated in GitHub Issue #192 reads: "Agent `output.location` fields resolve `${JERRY_OUTPUT_BASE}` at invocation time."

This release provides a PARTIAL satisfaction of AC-3, split into three sub-concerns per the requirements specification:

| Sub-AC | Description | Status in This Release |
|--------|-------------|------------------------|
| AC-3a | `OutputResolver.resolve()` correctly computes the effective base path | SATISFIED — verified by TU-003, Gates 4 and 5 |
| AC-3b | Governance YAML `output.location` fields contain the `${JERRY_OUTPUT_BASE}` token | SATISFIED — verified by IP-004, Gates 2 and 5 |
| AC-3c | Agent invocation framework reads governance YAML and interpolates `${JERRY_OUTPUT_BASE}` at runtime | NOT VERIFIED — out of scope for this release |

### Why AC-3c Is Not Verified

The mechanism for AC-3c would require the agent invocation framework to:
1. Load the agent's `.governance.yaml` file
2. Read `output.location`
3. Call `OutputResolver.resolve()`
4. Substitute the `${JERRY_OUTPUT_BASE}` token in the string

No such agent invocation framework currently exists in the codebase. The governance YAML `output.location` field is a behavioral specification (documentation-level), not a runtime-enforced contract. Implementing AC-3c is a separate architectural component. Attempting to verify AC-3c in this release would be a P-022 violation (claiming a pass without evidence).

### Mandatory Documentation Actions

Per the orchestration plan, the following documentation is required:

1. **In `evidence/test-results-e2e.txt`** (Gate 5): The integration test output must include an explicit comment: "AC-3c (runtime interpolation) is NOT verified by this test. The governance YAML contains `${JERRY_OUTPUT_BASE}` (AC-3b) and the resolver produces the correct path (AC-3a), but the token substitution at agent invocation time is a follow-up work item."

2. **In the PR description**: The PR must state that AC-3 is partially satisfied and link to the follow-up GitHub Issue.

3. **In the nse-3 SRR gate doc**: The technical review must record AC-3c as an open item with a follow-up issue reference, not as a failure.

### Constraint on Test Scenarios

No test scenario in this V&V plan claims to verify AC-3c. Scenarios TI-E2E-AC3a through TI-E2E-AC3c verify AC-3a only (resolver returns correct path). They explicitly note they do NOT assert that agents perform token substitution at invocation time.

---

## L2: Coverage Analysis

### Summary Metrics

| Metric | Value | Target | Status |
|--------|-------|--------|--------|
| Total requirement entries (REQ + sub-REQ) | 34 | — | — |
| Must-priority requirements | 33 | 100% verified | On Track |
| Should-priority requirements | 1 (REQ-OBP-002d) | Best-effort | On Track |
| With Test procedure assigned | 30 | 100% | On Track |
| With Inspection procedure assigned | 8 | 100% | On Track |
| Verified by Evidence Gate | 34 | 100% | On Track |
| Deferred (AC-3c) | 1 sub-AC | Documented | Documented |
| Failed | 0 | 0 | OK |

### Coverage by Verification Method

| Method | Requirement Count | % of Total | Notes |
|--------|-------------------|------------|-------|
| Test (T) | 30 | 88% | Includes unit, integration, system-level |
| Inspection (I) | 8 | 24% | REQ-OBP-003b, REQ-OBP-004 family, REQ-OBP-005b (call graph) |
| Analysis (A) | 0 | 0% | Not required for this feature |
| Demonstration (D) | 0 | 0% | Not required for this feature |

Note: REQ-OBP-005b and REQ-OBP-007 use both Test and Inspection; hence total exceeds 100%.

### Coverage by Evidence Gate

| Gate | Purpose | Requirements Verified |
|------|---------|----------------------|
| Gate 1 | Baseline regression check (pre-implementation) | Confirms no pre-existing failures; establishes comparison baseline |
| Gate 2 | `fallback_location` audit | REQ-OBP-004c (pre-condition: no Python reads field) |
| Gate 3 | CLI round-trip | REQ-OBP-001 family (001, 001a-001e), REQ-OBP-002 family (002, 002a-002d) |
| Gate 4 | Unit tests GREEN | REQ-OBP-003 family (003, 003a-003h), REQ-OBP-005, REQ-OBP-005a, REQ-OBP-006, REQ-OBP-006a-006b |
| Gate 5 | Integration + YAML inspection | REQ-OBP-004 family (004, 004a-004e), REQ-OBP-005b, REQ-OBP-007; AC-3 gap documented |
| Gate 6 | Final full run + regression | REQ-OBP-008 (coverage >= 90%); regression confirmation for all previous gates |

### Gap Analysis

| Gap | Description | Risk | Mitigation |
|-----|-------------|------|------------|
| AC-3c | Runtime governance YAML interpolation not implemented | RPN 4 (L:Medium x C:Medium per requirements risk table) | Documented as explicit scope exclusion; follow-up GitHub Issue required before merge; nse-3 SRR must confirm follow-up exists |
| EC-010 (`..` segments in path) | VO does not normalize; security review required | RPN 3 (security concern) | Assigned to et-3 eng-security; STRIDE analysis covers T-1 (path traversal); INV-5 in ADR mitigates absolute path traversal |
| EC-025 (whitespace-only path) | Resolver uses as-is; OS rejects at write time | RPN 2 (low impact; unusual config) | Documented in TU-003 additional variant; acceptable behavior documented in EC-025 |

### Review Readiness

| Review | Required Coverage | Current | Gap | Ready |
|--------|-------------------|---------|-----|-------|
| BARRIER-1 (reqs → arch sync) | V&V plan drafted | 100% procedures defined | None | Yes (this document satisfies nse-2) |
| BARRIER-2 (impl + V&V handoff) | BDD stubs ready for implementation | 100% stubs written | None | Yes |
| BARRIER-3 (joint final review) | All evidence gates captured | Gates 1-6 defined; captured in et-2/et-3 | Pending execution | After et-2/et-3 complete |
| CDR equivalent (READY_FOR_MERGE) | 100% pass or documented waiver | AC-3c documented as scope exclusion | Requires follow-up issue | Conditional |

---

## Evidence Gate Reference

Summary of the six evidence gates from ORCHESTRATION_PLAN.md v1.2. These gates are defined by the orchestration plan; this V&V plan maps requirements to gates for traceability.

| Gate # | Artifact | Phase | Command (abbreviated) | V&V Relevance |
|--------|----------|-------|----------------------|---------------|
| 1 | `evidence/test-results-baseline.txt` | Pre-et-2 | `uv run pytest tests/ --cov=src --cov-report=term-missing --tb=short` | Establishes regression baseline; confirms no pre-existing failures before new code is added |
| 2 | `evidence/fallback-location-audit.txt` | et-2 (before YAML edits) | `grep -r "fallback_location" src/ skills/ tests/ --include="*.py"` | Pre-condition for REQ-OBP-004c: confirms no Python code reads `fallback_location` before field is removed |
| 3 | `evidence/test-results-cli.txt` | et-2 (after implementation) | CLI set/get round-trip commands | Primary evidence for REQ-OBP-001 family and REQ-OBP-002 family (AC-1, AC-2) |
| 4 | `evidence/test-results-unit.txt` | et-2 (after implementation) | `uv run pytest tests/unit/ -v --tb=short` | Primary evidence for REQ-OBP-003 family (AC-3a), REQ-OBP-005, REQ-OBP-006 |
| 5 | `evidence/test-results-e2e.txt` | et-2 (after YAML edits) | `uv run pytest tests/integration/test_bootstrap_output_resolver.py -v --tb=short` | Evidence for AC-3a E2E (resolver works), AC-3b (YAML inspection), REQ-OBP-005b, REQ-OBP-007; AC-3c gap explicitly documented here |
| 6 | `evidence/test-results-final.txt` | et-3 (eng-reviewer final action) | `uv run pytest tests/ --cov=src --cov-report=term-missing --tb=short` | REQ-OBP-008 (>= 90% coverage on new modules); regression check vs. Gate 1; final quality signal |

All evidence files are raw terminal output (`.txt`), not summaries. Gate failure is a hard blocker on the phase quality gate (`/adversary` score >= 0.93).

---

## References

- NPR 7123.1D, Process 7 (Product Verification) — Evidence-based verification methodology
- NPR 7123.1D, Process 8 (Product Validation) — Stakeholder need satisfaction
- NASA SWEHB 7.9 — Entrance/Exit Criteria
- NASA-HDBK-1009A — V&V Work Products; quality criteria
- GitHub Issue #192 — Source acceptance criteria (AC-1 through AC-5)
- `nse/phase-nse-1/requirements.md` — REQ-OBP-001 through REQ-OBP-008; Edge Case Catalog; Test Oracle Reference
- `et/phase-et-1/ADR-PROJ021-001-output-path-resolution.md` — Architecture decisions D-1 through D-5; INV-1 through INV-5; STRIDE threat model
- `cross-pollination/barrier-1/et-to-nse/handoff.md` — V&V testability notes; AC-3 known gap constraint; ADR testability summary
- `ORCHESTRATION_PLAN.md` v1.2 — Evidence Artifact Registry (Gates 1-6); AC-3 known gap; criticality assessment (C3)
- `.context/rules/quality-enforcement.md` — H-13 (>= 0.93 threshold), H-14 (creator-critic cycle), H-20 (BDD test-first, 90% coverage), P-022 (no deception about pass without evidence)
- `docs/schemas/agent-governance-v1.schema.json` — Schema for governance YAML validation (REQ-OBP-004d)

---

*Generated by nse-verification agent v2.2.0*
*Workflow: output-basepath-20260318-001 | Phase: nse-2 | Date: 2026-03-18*
