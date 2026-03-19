---
DISCLAIMER: This guidance is AI-generated based on NASA Systems Engineering
standards. It is advisory only and does not constitute official NASA guidance.
All SE decisions require human review and professional engineering judgment.
Not for use in mission-critical decisions without SME validation.
---

# Requirements Specification: Configurable Output Base Path

> **Project:** PROJ-021-output-base-path
> **Entry:** nse-1
> **Date:** 2026-03-18
> **Status:** Draft
> **Source Issue:** GitHub #192 - Configurable output base path for skill agents
> **Workflow:** output-basepath-20260318-001
> **Criticality:** C3 (Significant)

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0: Executive Summary](#l0-executive-summary) | Plain-language description for stakeholders |
| [L1: Technical Requirements](#l1-technical-requirements) | Formal SHALL statements, MoSCoW classification, verification criteria |
| [L2: Systems Perspective](#l2-systems-perspective) | Allocation, risk implications, traceability strategy |
| [AC-3 Boundary Analysis](#ac-3-boundary-analysis) | Implementable now vs. future work, known gap documentation |
| [Edge Case Catalog](#edge-case-catalog) | Exhaustive edge cases for all five acceptance criteria |
| [Test Oracle Reference](#test-oracle-reference) | Input/output pairs for deterministic verification |
| [Requirements Quality Checklist](#requirements-quality-checklist) | Self-assessment against NASA-HDBK-1009A criteria |
| [References](#references) | Source document traceability |

---

## L0: Executive Summary

Jerry skill agents currently hardcode their output paths to `projects/${JERRY_PROJECT}/`, which breaks for users who organize their workspace without setting `JERRY_PROJECT` or who prefer a `work/` directory layout. This feature introduces a configurable `output.base_path` key that users can set once via `jerry config set` to redirect all agent output to a custom location. When no configuration is set, the system falls back gracefully: first to the project-based path (when `JERRY_PROJECT` is active), then to `work/`. Agents that currently carry an explicit `fallback_location` field in their governance YAML will have that field removed, as the fallback chain is now owned by a dedicated `OutputResolver` service in the application layer.

---

## L1: Technical Requirements

### Stakeholder Needs (NPR 7123.1D Process 1)

| ID | Stakeholder | Need | Priority | Source |
|----|-------------|------|----------|--------|
| STK-001 | Framework users (repo-based layout) | Configure where agents write output without editing individual agent definitions | H | GH #192 - users report path friction with work/ layout |
| STK-002 | Framework users (no active project) | Agents produce usable output even when JERRY_PROJECT is not set | H | GH #192 AC-5 - new users lack project context |
| STK-003 | Framework users (project-based layout) | Existing project-based path behavior is preserved as a default | H | GH #192 AC-4 - backward compatibility |
| STK-004 | Contributors and reviewers | Agent behavioral specification (output.location) reflects the configured base path | M | GH #192 AC-3 - governance YAML as source of truth |
| STK-005 | CI and automation users | Configuration persists across CLI invocations without re-setting | H | GH #192 AC-1 - persistent storage |

### Technical Requirements (NPR 7123.1D Process 2)

#### REQ-OBP-001 — Config Set Persistence (AC-1)

| Field | Value |
|-------|-------|
| **ID** | REQ-OBP-001 |
| **Requirement** | The `jerry config set output.base_path <path>` command SHALL write the value to the TOML configuration file at the scope specified by `--scope` (root or project), such that the value persists across subsequent CLI invocations in the same environment. |
| **Rationale** | Persistence is the defining property that distinguishes a configuration store from a transient variable. Without TOML persistence, users must re-set the path on every session, negating the benefit of the feature (STK-001, STK-005). The existing `cmd_config_set` infrastructure (implemented in `src/interface/cli/adapter.py:1139` via `cmd_config_set()`) already writes to `.jerry/config.toml` using `AtomicFileAdapter` (in `src/infrastructure/adapters/persistence/atomic_file_adapter.py`); this requirement specifies that `output.base_path` is a recognized key within that system. |
| **Parent** | STK-001, STK-005 |
| **V-Method** | Test (T) - execute CLI round-trip, inspect TOML file for written value |
| **Priority** | Must |
| **Status** | Draft |

**Sub-requirements:**

| ID | Requirement | Rationale | Parent | V-Method | Priority |
|----|-------------|-----------|--------|----------|----------|
| REQ-OBP-001a | The `jerry config set output.base_path <path> --scope root` command SHALL write the value to `.jerry/config.toml` under the `[output]` TOML section with key `base_path`. | Root scope is the primary mechanism for repo-wide configuration without requiring an active project (STK-002). The `[output]` section groups output-related keys. | REQ-OBP-001 | Test | Must |
| REQ-OBP-001b | The `jerry config set output.base_path <path> --scope project` command SHALL write the value to `projects/${JERRY_PROJECT}/.jerry/config.toml` under the `[output]` TOML section with key `base_path`. | Project scope enables per-project output path overrides, consistent with the existing layered config precedence (project overrides root). | REQ-OBP-001 | Test | Must |
| REQ-OBP-001c | The `jerry config set output.base_path <path>` command SHALL exit with code 0 on success and SHALL print the key, coerced value, scope, and target config file path to stdout. The "coerced value" is the value after type coercion applied by the config system (e.g., `"true"` → `true` for booleans, `"42"` → `42` for integers); for `output.base_path`, the coerced value is always a string identical to the input since no type coercion applies. | Exit code and output allow callers (scripts, CI) to confirm the write was accepted without inspecting the file directly. The coerced-value definition disambiguates what callers should expect when the config system applies type inference. | REQ-OBP-001 | Test | Must |
| REQ-OBP-001d | The `jerry config set output.base_path <path>` command SHALL NOT require JERRY_PROJECT to be set when `--scope root` is used. | Root scope must be usable before any project is active (STK-002). Requiring JERRY_PROJECT for root scope would block the primary new-user workflow. | REQ-OBP-001 | Test | Must |
| REQ-OBP-001e | The `jerry config set output.base_path <path> --scope project` command SHALL return exit code 1 with an error message when JERRY_PROJECT is not set. | Project scope writes require a project directory to exist; writing to an indeterminate path is undefined behavior. | REQ-OBP-001 | Test | Must |

---

#### REQ-OBP-002 — Config Get Retrieval (AC-2)

| Field | Value |
|-------|-------|
| **ID** | REQ-OBP-002 |
| **Requirement** | The `jerry config get output.base_path` command SHALL retrieve and print the currently configured value of `output.base_path` following the existing layered precedence order (env > project > root > defaults), and SHALL exit with code 0 when the key is present or code 1 when it is absent. |
| **Rationale** | Retrieval completes the read-write contract (STK-005). The layered precedence is already implemented in `LayeredConfigAdapter.get()`; this requirement specifies that `output.base_path` participates in that precedence chain without special-casing. An explicit exit code for absence (code 1) is required so callers can distinguish "not configured" from "empty string". |
| **Parent** | STK-001, STK-005 |
| **V-Method** | Test (T) - CLI round-trip with known stored value; inspect stdout and exit code |
| **Priority** | Must |
| **Status** | Draft |

**Sub-requirements:**

| ID | Requirement | Rationale | Parent | V-Method | Priority |
|----|-------------|-----------|--------|----------|----------|
| REQ-OBP-002a | The `jerry config get output.base_path` command SHALL print the value to stdout exactly as stored when the key is present in any configuration source. | Exact reproduction is required so callers can use the output programmatically. Whitespace-trimmed but otherwise unmodified. | REQ-OBP-002 | Test | Must |
| REQ-OBP-002b | The `jerry config get output.base_path` command SHALL honor the env > project > root > defaults precedence: an environment variable `JERRY_OUTPUT__BASE_PATH` SHALL override any file-based configuration. | Env override is the highest-priority precedence in `LayeredConfigAdapter`; env var mapping for dot notation uses double-underscore per the existing `EnvConfigAdapter._env_to_config_key()` contract (`output.base_path` -> `JERRY_OUTPUT__BASE_PATH`). | REQ-OBP-002 | Test | Must |
| REQ-OBP-002c | The `jerry config get output.base_path` command SHALL print `Key 'output.base_path' not found.` to stdout and exit with code 1 when the key is absent from all configuration sources and no default is registered. | Code 1 for absence is required per the existing `cmd_config_get` contract. A clear message prevents user confusion about whether the key was misspelled. | REQ-OBP-002 | Test | Must |
| REQ-OBP-002d | When `--json` flag is used, `jerry config get output.base_path` SHOULD output a JSON object containing `key`, `value`, and `source` fields. | JSON output is recommended for scripted consumers; `source` enables debugging of precedence resolution. Consistent with existing `cmd_config_get --json` behavior. | REQ-OBP-002 | Test | Should |

---

#### REQ-OBP-003 — OutputResolver Application Service (AC-3, implementable scope)

| Field | Value |
|-------|-------|
| **ID** | REQ-OBP-003 |
| **Requirement** | The system SHALL provide an `OutputResolver` application service with a `resolve() -> str` method that returns the effective output base path for the current invocation context, following the four-step fallback chain: (1) `output.base_path` from `LayeredConfigAdapter`, (2) `JERRY_OUTPUT__BASE_PATH` environment variable (covered by step 1 via env adapter), (3) `projects/{JERRY_PROJECT}/` when `JERRY_PROJECT` is set, (4) `work/` as the terminal fallback. |
| **Rationale** | A dedicated application service encapsulates the fallback logic and keeps it out of the domain layer and bootstrap, consistent with H-07 hexagonal layer isolation. Every agent output path decision routes through this single service, ensuring consistent behavior (STK-001, STK-002, STK-003). See [AC-3 Boundary Analysis](#ac-3-boundary-analysis) for the known gap between this resolver and runtime governance YAML interpolation. |
| **Parent** | STK-001, STK-002, STK-003 |
| **V-Method** | Test (T) - unit tests for each fallback case with mocked config adapter; integration test with real LayeredConfigAdapter |
| **Priority** | Must |
| **Status** | Draft |

**Sub-requirements:**

| ID | Requirement | Rationale | Parent | V-Method | Priority |
|----|-------------|-----------|--------|----------|----------|
| REQ-OBP-003a | The `OutputResolver.resolve()` method SHALL return a string that ends with exactly one forward slash character `/`. | A guaranteed trailing slash ensures callers can safely concatenate subdirectory paths without checking (e.g., `resolver.resolve() + "use-cases/"` works regardless of whether the base path was configured as `work` or `work/`). | REQ-OBP-003 | Test | Must |
| REQ-OBP-003b | The `OutputResolver` class SHALL reside in `src/configuration/application/services/output_resolver.py` and SHALL import only from the configuration domain layer and the `IConfigurationProvider` port (defined as a `Protocol` at `src/infrastructure/adapters/configuration/layered_config_adapter.py:40`; note: the port is collocated with the adapter as architectural debt — see ADR-PROJ021-001 Section 5 H-07(b) note). `OutputResolver` SHALL NOT import from `LayeredConfigAdapter` directly. | H-07 compliance: application layer services may depend on domain and ports, not on infrastructure adapters. The bootstrap composition root wires the concrete adapter. | REQ-OBP-003 | Inspection (I) - import analysis | Must |
| REQ-OBP-003c | The `OutputBasePath` value object SHALL reside in `src/configuration/domain/value_objects/output_base_path.py`, SHALL wrap a single string path value, and SHALL reject null bytes (`\x00`) in the path string by raising `ValueError`. | Domain value objects enforce invariants. Null bytes are a path-traversal attack vector and an invalid filesystem character on all target platforms. Empty string is explicitly permitted (triggers fallback in resolver). | REQ-OBP-003 | Test | Must |
| REQ-OBP-003d | The `OutputResolver.resolve()` method SHALL check the `IConfigurationProvider.get("output.base_path")` port first; if that returns a non-empty string, it SHALL use that value as the base path regardless of environment variables or JERRY_PROJECT. | This enforces the highest-priority slot in the fallback chain, ensuring explicit configuration is always honored. Non-empty check prevents an empty-string stored value from masking the fallback chain. The port abstraction (`IConfigurationProvider`) is used per REQ-OBP-003b — the concrete adapter is wired at the composition root. | REQ-OBP-003 | Test | Must |
| REQ-OBP-003e | The `OutputResolver.resolve()` method SHALL return `projects/{JERRY_PROJECT}/` (with trailing slash) when no `output.base_path` is configured and the `JERRY_PROJECT` environment variable is set to a non-empty value. | Backward compatibility with the existing project-based path convention (STK-003). `JERRY_PROJECT` is already available via the env adapter as `jerry_project` config key, or directly via `os.environ`. | REQ-OBP-003 | Test | Must |
| REQ-OBP-003f | The `OutputResolver.resolve()` method SHALL return `work/` (with trailing slash) when neither `output.base_path` is configured nor `JERRY_PROJECT` is set. | Terminal fallback ensures the service never raises an exception or returns an empty string; a caller can always write to `work/` (STK-002). | REQ-OBP-003 | Test | Must |
| REQ-OBP-003g | The `LayeredConfigAdapter` SHALL include `output.base_path` in its `defaults` dict with value `None` (Python None, not string "None"). | A `None` default causes `LayeredConfigAdapter.get("output.base_path")` to return `None` rather than raising `KeyError`, and distinguishes "not set" from "empty string". The `IConfigurationProvider.get()` port (signature: `def get(self, key: str) -> Any | None` at `layered_config_adapter.py:48`) returns `None` for absent-but-defaulted keys, which is the contract the resolver depends on. The resolver's non-empty check (`if value is not None and value != ""`) handles both cases uniformly. | REQ-OBP-003 | Test | Must |
| REQ-OBP-003h | The `OutputResolver.resolve()` method SHALL propagate any `ValueError` raised by the `OutputBasePath` value object (REQ-OBP-003c) without catching it. The resolver SHALL NOT fall back to the next chain step when the configured value is structurally invalid (contains null bytes). | Silently falling back on invalid input would mask security-relevant errors (null byte injection). The caller (bootstrap or CLI) is responsible for catching `ValueError` and presenting an appropriate error message. This is consistent with the fail-fast principle: validation errors at the domain boundary must surface, not be silently absorbed. | REQ-OBP-003 | Test | Must |

---

#### REQ-OBP-004 — Governance YAML Token Placement (AC-3, YAML scope)

| Field | Value |
|-------|-------|
| **ID** | REQ-OBP-004 |
| **Requirement** | The `output.location` field in each of the six affected agent governance YAML files SHALL contain the `${JERRY_OUTPUT_BASE}` token in place of the hardcoded `projects/${JERRY_PROJECT}/` prefix, and the `fallback_location` field SHALL be removed from all six files. |
| **Rationale** | The governance YAML `output.location` field is the behavioral specification that documents where an agent writes its output. Updating these fields to use `${JERRY_OUTPUT_BASE}` makes the specification accurate and consistent with the new resolver behavior (STK-004). Removing `fallback_location` eliminates a redundant field whose semantics are now fully owned by `OutputResolver`. See [AC-3 Boundary Analysis](#ac-3-boundary-analysis) for the known gap: the token placement is a specification-level change; runtime interpolation by the agent invocation framework is a separate follow-up. |
| **Parent** | STK-004 |
| **V-Method** | Inspection (I) - YAML field value inspection; Test (T) - schema validation |
| **Priority** | Must |
| **Status** | Draft |

**Sub-requirements:**

| ID | Requirement | Rationale | Parent | V-Method | Priority |
|----|-------------|-----------|--------|----------|----------|
| REQ-OBP-004a | Each of the six governance YAML files SHALL have `output.location` updated to the pattern `${JERRY_OUTPUT_BASE}{subdirectory}/{filename-pattern}` where `{subdirectory}` matches the current path segment after `projects/${JERRY_PROJECT}/`. The six files are: (1) `skills/use-case/agents/uc-author.governance.yaml`, (2) `skills/use-case/agents/uc-slicer.governance.yaml`, (3) `skills/test-spec/agents/tspec-generator.governance.yaml`, (4) `skills/test-spec/agents/tspec-analyst.governance.yaml`, (5) `skills/contract-design/agents/cd-generator.governance.yaml`, (6) `skills/contract-design/agents/cd-validator.governance.yaml`. | The token replaces only the configurable base prefix; the subdirectory structure (`use-cases/`, `test-specs/`, `contracts/`) is intrinsic to each skill and must be preserved. Full paths listed for traceability and audit clarity. | REQ-OBP-004 | Inspection (I) | Must |
| REQ-OBP-004b | The `${JERRY_OUTPUT_BASE}` token SHALL appear without a trailing slash in the YAML value; the responsibility for ensuring a trailing slash before concatenation rests with `OutputResolver.resolve()`. | Placing the slash responsibility in the resolver (a single code location) rather than in N YAML files (N data locations) reduces the risk of inconsistency across files. | REQ-OBP-004 | Inspection (I) | Must |
| REQ-OBP-004c | The `fallback_location` field SHALL be absent from all six governance YAML files after the edit. Pre-condition verified: `fallback_location` is currently present in all 6 files (`uc-author.governance.yaml:52`, `uc-slicer.governance.yaml:53`, `tspec-generator.governance.yaml:62`, `tspec-analyst.governance.yaml:65`, `cd-generator.governance.yaml:76`, `cd-validator.governance.yaml:63`). | The fallback chain is now owned by `OutputResolver`; a `fallback_location` field in the YAML would be dead specification that could mislead contributors about how fallback works. Evidence: `grep -r "fallback_location" skills/ --include="*.governance.yaml"` confirms all 6 files currently contain this field. | REQ-OBP-004 | Inspection (I) | Must |
| REQ-OBP-004d | All six governance YAML files SHALL continue to pass JSON Schema validation against `docs/schemas/agent-governance-v1.schema.json` after the edit. | Schema compliance is required by H-34; the schema must accept `output.location` values containing the `${JERRY_OUTPUT_BASE}` token and must declare `fallback_location` as optional (not required) to permit its removal. | REQ-OBP-004 | Test (T) - schema validation | Must |
| REQ-OBP-004e | No other fields in the six governance YAML files SHALL be modified as part of this change. | Minimizes diff scope for reviewer clarity and prevents accidental behavioral changes to unrelated agent settings. | REQ-OBP-004 | Inspection (I) - diff review | Must |

---

#### REQ-OBP-005 — Project-Based Fallback (AC-4)

| Field | Value |
|-------|-------|
| **ID** | REQ-OBP-005 |
| **Requirement** | When `output.base_path` is not configured in any configuration source, the `OutputResolver.resolve()` method SHALL return `projects/{JERRY_PROJECT}/` (with trailing slash) as the effective output base path, where `{JERRY_PROJECT}` is the value of the `JERRY_PROJECT` environment variable. |
| **Rationale** | This fallback preserves the existing behavior that all current users depend on (STK-003). Users who have not configured `output.base_path` must experience no change in agent output locations. The fallback is the second step in the resolver's chain, taking effect only when no explicit configuration exists. |
| **Parent** | STK-003 |
| **V-Method** | Test (T) - invoke resolver with empty config and JERRY_PROJECT set; assert return value |
| **Priority** | Must |
| **Status** | Draft |

**Sub-requirements:**

| ID | Requirement | Rationale | Parent | V-Method | Priority |
|----|-------------|-----------|--------|----------|----------|
| REQ-OBP-005a | The `OutputResolver.resolve()` method SHALL treat JERRY_PROJECT values of any non-empty string as valid project IDs for path construction, without validating that the directory exists. | Directory existence is a filesystem concern, not a resolver concern (domain layer does not perform I/O). An agent that receives a path to a non-existent directory should create it at write time; the resolver must not block on directory absence. | REQ-OBP-005 | Test | Must |
| REQ-OBP-005b | The `get_project_data_path()` function in `src/bootstrap.py` SHALL call `OutputResolver.resolve()` instead of constructing `base / "projects" / project_id` directly, maintaining the same `Path | None` return type contract for existing callers. | All existing callers of `get_project_data_path()` must continue to work without modification. The resolver integration happens at the bootstrap composition root, consistent with H-07. | REQ-OBP-005 | Test (T) - integration test for bootstrap; Inspection (I) - call graph | Must |

---

#### REQ-OBP-006 — Terminal Fallback to work/ (AC-5)

| Field | Value |
|-------|-------|
| **ID** | REQ-OBP-006 |
| **Requirement** | When neither `output.base_path` is configured in any configuration source nor `JERRY_PROJECT` is set to a non-empty value, the `OutputResolver.resolve()` method SHALL return `work/` as the effective output base path. |
| **Rationale** | New users who have not set up a project or configured an output path must still receive usable output (STK-002). `work/` is the existing repository-based placement pattern documented in `worktracker-directory-structure.md`. This fallback must be unconditional so `resolve()` never raises an exception or returns an empty string. |
| **Parent** | STK-002 |
| **V-Method** | Test (T) - invoke resolver with empty config and JERRY_PROJECT unset; assert return value equals "work/" |
| **Priority** | Must |
| **Status** | Draft |

**Sub-requirements:**

| ID | Requirement | Rationale | Parent | V-Method | Priority |
|----|-------------|-----------|--------|----------|----------|
| REQ-OBP-006a | The `OutputResolver.resolve()` method SHALL return the string `"work/"` (exactly, with trailing slash) as the terminal fallback. | Exact string match is required so callers can predict and test the fallback without parsing. The trailing slash is guaranteed by REQ-OBP-003a. | REQ-OBP-006 | Test | Must |
| REQ-OBP-006b | The terminal fallback SHALL apply when `JERRY_PROJECT` is set to an empty string `""` as well as when it is absent from the environment. | An empty-string `JERRY_PROJECT` is semantically equivalent to "not set" for path construction purposes; producing `projects//` would be invalid. | REQ-OBP-006 | Test | Must |

---

#### REQ-OBP-007 — Bootstrap Integration

| Field | Value |
|-------|-------|
| **ID** | REQ-OBP-007 |
| **Requirement** | The composition root (`src/bootstrap.py`) SHALL wire a `LayeredConfigAdapter` instance into `OutputResolver` such that `OutputResolver.resolve()` reads from the active configuration files (root `.jerry/config.toml` and, when `JERRY_PROJECT` is set, `projects/{JERRY_PROJECT}/.jerry/config.toml`). |
| **Rationale** | The bootstrap is the sole owner of dependency wiring per the composition root pattern. `OutputResolver` must not construct its own adapter (that would violate dependency inversion); the adapter must be injected (H-07). |
| **Parent** | STK-001 |
| **V-Method** | Test (T) - integration test with real config files; Inspection (I) - bootstrap wiring |
| **Priority** | Must |
| **Status** | Draft |

---

#### REQ-OBP-008 — Test Coverage Requirement

| ID | Requirement | Rationale | Parent | V-Method | Priority |
|----|-------------|-----------|--------|----------|----------|
| REQ-OBP-008 | All new Python modules introduced for this feature (`output_base_path.py`, `output_resolver.py`) SHALL achieve >= 90% line coverage as measured by `pytest --cov`. | H-20 (BDD test-first, 90% line coverage) is a HARD rule. Coverage below 90% is a blocking defect. | REQ-OBP-001 through REQ-OBP-007 | Test (T) - coverage report | Must |

---

### MoSCoW Summary

| ID | Requirement (abbreviated) | MoSCoW |
|----|---------------------------|--------|
| REQ-OBP-001 | `jerry config set output.base_path` persists to TOML | Must |
| REQ-OBP-001a | Root scope writes to `.jerry/config.toml [output]` | Must |
| REQ-OBP-001b | Project scope writes to project config file | Must |
| REQ-OBP-001c | Exit 0 on success with diagnostic output | Must |
| REQ-OBP-001d | Root scope works without JERRY_PROJECT | Must |
| REQ-OBP-001e | Project scope fails gracefully without JERRY_PROJECT | Must |
| REQ-OBP-002 | `jerry config get output.base_path` retrieves current value | Must |
| REQ-OBP-002a | Prints value exactly as stored | Must |
| REQ-OBP-002b | Honors env > project > root > defaults precedence | Must |
| REQ-OBP-002c | Exit 1 with message when key is absent | Must |
| REQ-OBP-002d | `--json` output with key/value/source | Should |
| REQ-OBP-003 | `OutputResolver` application service with 4-step fallback | Must |
| REQ-OBP-003a | `resolve()` always returns string with trailing slash | Must |
| REQ-OBP-003b | Resides in application layer; no infra imports | Must |
| REQ-OBP-003c | `OutputBasePath` VO rejects null bytes; permits empty | Must |
| REQ-OBP-003d | Explicit config takes highest priority | Must |
| REQ-OBP-003e | JERRY_PROJECT fallback returns `projects/{id}/` | Must |
| REQ-OBP-003f | Terminal fallback returns `work/` | Must |
| REQ-OBP-003g | `output.base_path` default is `None` in LayeredConfigAdapter | Must |
| REQ-OBP-003h | Resolver propagates `ValueError` from VO; no silent fallback on invalid input | Must |
| REQ-OBP-004 | Governance YAML token placement (`${JERRY_OUTPUT_BASE}`) | Must |
| REQ-OBP-004a | All 6 YAML files updated to use token | Must |
| REQ-OBP-004b | Token has no trailing slash in YAML; slash in resolver | Must |
| REQ-OBP-004c | `fallback_location` removed from all 6 files | Must |
| REQ-OBP-004d | All 6 files pass schema validation after edit | Must |
| REQ-OBP-004e | No other YAML fields modified | Must |
| REQ-OBP-005 | Project-based fallback when JERRY_PROJECT is set | Must |
| REQ-OBP-005a | Directory existence not validated by resolver | Must |
| REQ-OBP-005b | `get_project_data_path()` delegates to resolver | Must |
| REQ-OBP-006 | Terminal fallback to `work/` | Must |
| REQ-OBP-006a | Returns exactly `"work/"` | Must |
| REQ-OBP-006b | Empty-string JERRY_PROJECT treated as absent | Must |
| REQ-OBP-007 | Bootstrap wires adapter into resolver | Must |
| REQ-OBP-008 | >= 90% line coverage on new modules | Must |
| Runtime interpolation of `${JERRY_OUTPUT_BASE}` in governance YAML at agent invocation | Agent invocation framework reads and substitutes token | Won't (this release; see AC-3 Known Gap) |

---

## L2: Systems Perspective

### Allocation Matrix

| Requirement | Allocated To | Layer | File |
|-------------|--------------|-------|------|
| REQ-OBP-001 | CLI adapter | Interface | `src/interface/cli/adapter.py` (existing `cmd_config_set`) |
| REQ-OBP-002 | CLI adapter | Interface | `src/interface/cli/adapter.py` (existing `cmd_config_get`) |
| REQ-OBP-003 | OutputResolver service | Application | `src/configuration/application/services/output_resolver.py` (new) |
| REQ-OBP-003c | OutputBasePath value object | Domain | `src/configuration/domain/value_objects/output_base_path.py` (new) |
| REQ-OBP-003g | LayeredConfigAdapter defaults | Infrastructure | `src/infrastructure/adapters/configuration/layered_config_adapter.py` (modify defaults) |
| REQ-OBP-004 | Agent governance YAMLs | Skills | 6 `.governance.yaml` files (modify) |
| REQ-OBP-005b | `get_project_data_path()` delegation | Bootstrap | `src/bootstrap.py` (modify `get_project_data_path()` to call `OutputResolver.resolve()`) |
| REQ-OBP-007 | Bootstrap dependency wiring | Bootstrap | `src/bootstrap.py` (wire `LayeredConfigAdapter` into `OutputResolver` constructor at composition root) |
| REQ-OBP-008 | BDD test suite | Tests | `tests/unit/configuration/`, `tests/integration/` (new) |

### Interface Implications

| Interface | Type | Impact |
|-----------|------|--------|
| `IConfigurationProvider.get("output.base_path")` | Port (read) | New key recognized; no new port methods required |
| `OutputResolver.resolve() -> str` | Application service | New public interface; callers: bootstrap, future agent invocation framework |
| `get_project_data_path() -> Path | None` | Bootstrap function | Return type unchanged; internal implementation delegates to resolver |
| `cmd_config_set` / `cmd_config_get` | CLI commands | No new commands; `output.base_path` is a recognized key in the existing system |
| `output.location` in governance YAMLs | Specification | Token value changes from `projects/${JERRY_PROJECT}/...` to `${JERRY_OUTPUT_BASE}...`; format change only |

### Risk Implications (NPR 8000.4C)

**RPN Scale:** Likelihood and Consequence are each rated Low (1), Medium (2), or High (3). RPN = Likelihood × Consequence (range 1-9). Risk priority: RPN 1-2 = acceptable, RPN 3-4 = monitor, RPN 6-9 = mitigate actively.

| Requirement | Risk | Likelihood x Consequence | Mitigation |
|-------------|------|--------------------------|------------|
| REQ-OBP-003b (layer isolation) | OutputResolver accidentally imports LayeredConfigAdapter directly | L:Low x C:Medium = RPN 2 | H-07 import check in eng-reviewer phase; pre-tool AST enforcement |
| REQ-OBP-004c (fallback_location removal) | Python code somewhere reads `fallback_location` field at runtime | L:Low x C:High = RPN 3 | Evidence Gate 2 (`grep -r "fallback_location" src/ --include="*.py"`) must pass before any YAML edits |
| REQ-OBP-005b (get_project_data_path delegation) | Existing callers of `get_project_data_path()` receive different path due to config side-effect | L:Low x C:High = RPN 3 | Integration test that confirms behavior with no config matches prior behavior; baseline test run required (Evidence Gate 1) |
| REQ-OBP-003c (null byte rejection) | Path traversal via `\x00` in configured base path | L:Low x C:High = RPN 3 | STRIDE path traversal check in eng-security phase; unit test for null byte rejection |
| REQ-OBP-004 (AC-3 known gap) | Stakeholders interpret governance YAML update as full runtime resolution | L:Medium x C:Medium = RPN 4 | Explicit gap documentation in Evidence Gate 5; follow-up issue logged; partial AC-3 status published |
| REQ-OBP-008 (coverage) | New modules fail to reach 90% line coverage | L:Medium x C:Medium = RPN 4 | BDD test-first per H-20; eng-qa review of test strategy before GREEN phase |

### Traceability Summary

```
GH Issue #192 (5 Acceptance Criteria)
    |
    +-- AC-1 (config set)
    |       └── REQ-OBP-001 (+ 001a-001e)
    |               └── CLIAdapter.cmd_config_set()
    |                       └── Evidence Gate 3 (CLI round-trip)
    |
    +-- AC-2 (config get)
    |       └── REQ-OBP-002 (+ 002a-002d)
    |               └── CLIAdapter.cmd_config_get()
    |                       └── Evidence Gate 3 (CLI round-trip)
    |
    +-- AC-3 (variable resolution -- partially satisfied)
    |       +-- REQ-OBP-003 (OutputResolver) -- implementable now
    |       |       └── Evidence Gate 4 (unit tests) + Gate 5 (integration)
    |       +-- REQ-OBP-004 (YAML token placement) -- implementable now
    |       |       └── Evidence Gate 2 (audit) + Gate 5 (schema validation)
    |       +-- [DEFERRED] Runtime interpolation at agent invocation -- WON'T (this release)
    |               └── Follow-up GitHub Issue required
    |
    +-- AC-4 (project fallback)
    |       └── REQ-OBP-005 (+ 005a-005b)
    |               └── OutputResolver.resolve() case 2
    |                       └── Evidence Gate 4 (unit test: case 2)
    |
    +-- AC-5 (work/ fallback)
            └── REQ-OBP-006 (+ 006a-006b)
                    └── OutputResolver.resolve() case 3
                            └── Evidence Gate 4 (unit test: case 3)

Cross-cutting:
    REQ-OBP-007 (bootstrap wiring) -- traces to AC-3, AC-4, AC-5
    REQ-OBP-008 (coverage) -- traces to all REQ-OBP-003 through 006
```

---

## AC-3 Boundary Analysis

AC-3 states: "Agent output.location fields resolve `${JERRY_OUTPUT_BASE}` at invocation time."

This acceptance criterion contains two separable concerns:

### Concern A: Resolver infrastructure + YAML token (implementable in this release)

| Deliverable | Status | Requirement |
|-------------|--------|-------------|
| `OutputResolver.resolve()` returns correct base path | Implementable | REQ-OBP-003 |
| `${JERRY_OUTPUT_BASE}` token appears in all 6 governance YAMLs | Implementable | REQ-OBP-004 |
| Bootstrap wires resolver | Implementable | REQ-OBP-007 |

The resolver correctly computes the effective base path for all three cases (explicit config, JERRY_PROJECT fallback, work/ fallback). The governance YAML `output.location` field is updated to contain `${JERRY_OUTPUT_BASE}use-cases/...` instead of `projects/${JERRY_PROJECT}/use-cases/...`. This is a specification-level change: the YAML correctly documents what the resolved path will be.

### Concern B: Runtime interpolation at agent invocation (deferred -- WON'T this release)

The mechanism by which a running agent reads its `output.location` field from its governance YAML and substitutes `${JERRY_OUTPUT_BASE}` with the resolved value at invocation time is NOT implemented by this issue. That substitution would require the agent invocation framework to:

1. Load the agent's `.governance.yaml` file
2. Read `output.location`
3. Call `OutputResolver.resolve()`
4. Substitute the token in the string

This mechanism is part of the agent invocation framework, which is a separate architectural component not touched by this issue. No such framework currently exists.

**Consequence for verification:** AC-3 is considered partially satisfied by this release. Evidence Gate 5 must document this gap explicitly. The test in `tests/integration/test_bootstrap_output_resolver.py` SHALL demonstrate that:
- `OutputResolver.resolve()` returns the correct path for all three cases
- The governance YAML `output.location` field contains `${JERRY_OUTPUT_BASE}` (YAML inspection)
- The test does NOT claim that agents perform token substitution at invocation time

**Follow-up item:** A separate GitHub Issue SHALL be logged before merge to track implementation of the agent invocation interpolation mechanism. The PR description for this issue must reference that follow-up and explain the partial satisfaction of AC-3.

### Formal AC-3 Requirement Split

| Sub-AC | Description | Status | Requirement |
|--------|-------------|--------|-------------|
| AC-3a | OutputResolver correctly resolves `${JERRY_OUTPUT_BASE}` to the effective base path | Satisfied by this release | REQ-OBP-003 |
| AC-3b | Governance YAML `output.location` fields contain `${JERRY_OUTPUT_BASE}` token | Satisfied by this release | REQ-OBP-004 |
| AC-3c | Agent invocation framework reads governance YAML and interpolates `${JERRY_OUTPUT_BASE}` at runtime | Deferred -- WON'T this release | [Future issue] |

---

## Edge Case Catalog

### AC-1 / AC-2: Config Set and Get Edge Cases

| ID | Edge Case | Input | Expected Behavior | Requirement |
|----|-----------|-------|-------------------|-------------|
| EC-001 | Relative path (no leading slash) | `output.base_path = "work/"` | Stored and retrieved exactly as given; resolver uses as-is | REQ-OBP-001, REQ-OBP-002 |
| EC-002 | Absolute path | `output.base_path = "/custom/output/"` | Stored and retrieved exactly as given; resolver uses as-is | REQ-OBP-001, REQ-OBP-002 |
| EC-003 | Path with spaces | `output.base_path = "my output/"` | Stored in TOML as quoted string; retrieved with spaces intact | REQ-OBP-001a |
| EC-004 | Path without trailing slash | `output.base_path = "work"` | Stored and retrieved without slash; `resolve()` adds trailing slash | REQ-OBP-003a |
| EC-005 | Empty string value | `output.base_path = ""` | Stored as empty string; resolver treats as "not configured" and proceeds to next fallback step | REQ-OBP-003d |
| EC-006 | Setting same key twice | Two sequential `jerry config set` calls | Second write overwrites first; `config get` returns second value | REQ-OBP-001 |
| EC-007 | Project scope without JERRY_PROJECT | `--scope project` with JERRY_PROJECT unset | Exit code 1, error message "No active project. Set JERRY_PROJECT first." | REQ-OBP-001e |
| EC-008 | Key with null byte in path | `output.base_path` set to a string containing `\x00` via config set | `OutputBasePath` value object raises `ValueError`; `OutputResolver.resolve()` propagates the exception to the caller without catching it (per REQ-OBP-003h). Silently falling back to `work/` would mask a potentially malicious input. | REQ-OBP-003c, REQ-OBP-003h |
| EC-009 | Very long path (> 256 chars) | `output.base_path` = 300-character path | Stored and retrieved; domain VO does not impose length limit; OS-level rejection happens at file write | REQ-OBP-003c |
| EC-010 | Path with `..` segments | `output.base_path = "../../etc/"` | Stored and retrieved; `OutputBasePath` VO does NOT normalize paths (normalization is an infra concern); eng-security review required | REQ-OBP-003c, security |
| EC-011 | Config file is malformed TOML | Existing `.jerry/config.toml` contains invalid TOML | `LayeredConfigAdapter._load_toml()` catches `TOMLDecodeError` and returns empty dict; `config get` returns "Key not found"; does not crash | REQ-OBP-002 |
| EC-012 | Config file does not exist | No `.jerry/config.toml` present | `config get output.base_path` returns "Key not found" (exit 1); does not create the file | REQ-OBP-002 |

### AC-3: OutputResolver Edge Cases

| ID | Edge Case | Input | Expected Behavior | Requirement |
|----|-----------|-------|-------------------|-------------|
| EC-013 | Config returns empty string | `config.get("output.base_path")` returns `""` | Resolver treats as "not configured"; proceeds to JERRY_PROJECT check | REQ-OBP-003d |
| EC-014 | Config returns `None` | `config.get("output.base_path")` returns `None` | Resolver treats as "not configured"; proceeds to JERRY_PROJECT check | REQ-OBP-003d |
| EC-015 | Path missing trailing slash | Config returns `"work"` (no slash) | Resolver appends `/`; `resolve()` returns `"work/"` | REQ-OBP-003a |
| EC-016 | Path already has trailing slash | Config returns `"work/"` | Resolver does not double-append; returns `"work/"` | REQ-OBP-003a |
| EC-017 | JERRY_PROJECT set to non-existent project ID | `JERRY_PROJECT=PROJ-999` (directory does not exist) | Resolver returns `"projects/PROJ-999/"` without checking directory existence | REQ-OBP-005a |
| EC-018 | JERRY_PROJECT set to empty string | `JERRY_PROJECT=""` | Resolver treats as "not set"; terminal fallback `"work/"` applies | REQ-OBP-006b |
| EC-019 | Env var overrides config file | `JERRY_OUTPUT__BASE_PATH=/override/` and root config has `output.base_path = "other/"` | `LayeredConfigAdapter` env layer wins; resolver receives `/override/` | REQ-OBP-002b, REQ-OBP-003d |
| EC-020 | Project config overrides root config | Project config has `output.base_path = "proj_out/"`, root config has `output.base_path = "work/"` | Project config wins per layered precedence; resolver receives `"proj_out/"` | REQ-OBP-003d |
| EC-021 | Path with null byte in env var | `JERRY_OUTPUT__BASE_PATH` contains `\x00` | `OutputBasePath` VO raises `ValueError`; `OutputResolver.resolve()` propagates exception per REQ-OBP-003h; calling code (bootstrap/CLI) must handle | REQ-OBP-003c, REQ-OBP-003h |

### AC-4 / AC-5: Fallback Edge Cases

| ID | Edge Case | Input | Expected Behavior | Requirement |
|----|-----------|-------|-------------------|-------------|
| EC-022 | Both config and JERRY_PROJECT set | `output.base_path = "custom/"` and `JERRY_PROJECT = "PROJ-001"` | Config wins; `resolve()` returns `"custom/"` | REQ-OBP-003d |
| EC-023 | Neither config nor JERRY_PROJECT | No config, no env var | Terminal fallback; `resolve()` returns `"work/"` | REQ-OBP-006 |
| EC-024 | JERRY_PROJECT with unusual characters | `JERRY_PROJECT=PROJ_TEST-99` | Resolver passes value through without validation; `resolve()` returns `"projects/PROJ_TEST-99/"` | REQ-OBP-005a |
| EC-025 | Whitespace-only path value | `output.base_path = "   "` | Stored as-is by config system; resolver treats whitespace-only string as "configured" (non-empty after `strip()` check is NOT applied — resolver does NOT strip whitespace, it uses the value as given); `resolve()` returns `"   /"` with trailing slash appended. This is a valid but unusual configuration; the OS will reject the path at file-write time. | REQ-OBP-003a, REQ-OBP-003d |

---

## Test Oracle Reference

These input/output pairs serve as the definitive verification basis for each acceptance criterion. Exact string matching applies unless noted.

### Oracle Set 1: CLI Round-Trip (AC-1, AC-2)

| Oracle ID | Command Sequence | Expected stdout (last command) | Expected exit code |
|-----------|-----------------|-------------------------------|-------------------|
| OR-001 | `jerry config set output.base_path work/ --scope root` | Output contains all 4 diagnostic fields per REQ-OBP-001c: key (`output.base_path`), coerced value (`work/`), scope (`root`), and target config file path (`.jerry/config.toml`) | 0 |
| OR-002 | (after OR-001) `jerry config get output.base_path` | `work/` | 0 |
| OR-003 | `jerry config get output.base_path` (key not set, fresh env) | `Key 'output.base_path' not found.` | 1 |
| OR-004 | `jerry config set output.base_path projects/PROJ-021/ --scope root && jerry config get output.base_path` | `projects/PROJ-021/` | 0 |
| OR-005 | `jerry config set output.base_path work/ --scope project` (JERRY_PROJECT unset) | Contains `No active project` | 1 |
| OR-006 | `JERRY_PROJECT=PROJ-021 jerry config set output.base_path custom/ --scope project` | Output contains key (`output.base_path`), coerced value (`custom/`), scope (`project`), and target config file path (`projects/PROJ-021/.jerry/config.toml`) | 0 |

### Oracle Set 2: OutputResolver.resolve() (AC-3, AC-4, AC-5)

| Oracle ID | Config State | JERRY_PROJECT | Expected resolve() return |
|-----------|-------------|---------------|--------------------------|
| OR-101 | `output.base_path = "custom/output/"` | Any | `"custom/output/"` |
| OR-102 | `output.base_path = "custom/output"` (no slash) | Any | `"custom/output/"` |
| OR-103 | `output.base_path = None` | `"PROJ-021"` | `"projects/PROJ-021/"` |
| OR-104 | `output.base_path = ""` | `"PROJ-021"` | `"projects/PROJ-021/"` |
| OR-105 | `output.base_path = None` | Not set or `""` | `"work/"` |
| OR-106 | `output.base_path = None` | `""` | `"work/"` |
| OR-107 | `JERRY_OUTPUT__BASE_PATH=/env/path/` in env | `"PROJ-021"` | `"/env/path/"` |

### Oracle Set 3: Governance YAML State (AC-3 specification)

| Oracle ID | YAML File | Field | Expected Value (pattern) |
|-----------|-----------|-------|--------------------------|
| OR-201 | `uc-author.governance.yaml` | `output.location` | Contains `${JERRY_OUTPUT_BASE}` and does NOT contain `${JERRY_PROJECT}` |
| OR-202 | `uc-author.governance.yaml` | `fallback_location` | Field absent (KeyError on dict lookup) |
| OR-203 | `tspec-generator.governance.yaml` | `output.location` | Contains `${JERRY_OUTPUT_BASE}test-specs/` |
| OR-204 | `cd-generator.governance.yaml` | `output.location` | Contains `${JERRY_OUTPUT_BASE}contracts/` |
| OR-205 | All 6 files | Schema validation | All pass `docs/schemas/agent-governance-v1.schema.json` |

### Oracle Set 4: OutputBasePath Value Object (REQ-OBP-003c)

| Oracle ID | Input | Expected Behavior |
|-----------|-------|-------------------|
| OR-301 | `OutputBasePath("work/")` | Constructs without error |
| OR-302 | `OutputBasePath("")` | Constructs without error (empty permitted; triggers fallback) |
| OR-303 | `OutputBasePath("path\x00with-null")` | Raises `ValueError` |
| OR-304 | `OutputBasePath("/absolute/path/")` | Constructs without error |

---

## Requirements Quality Checklist

Per NASA-HDBK-1009A quality criteria:

| Criterion | Assessment |
|-----------|-----------|
| Complete | All 5 acceptance criteria from GH #192 are addressed. The AC-3 gap is explicitly bounded and documented. Edge cases catalog is comprehensive. |
| Consistent | No conflicting requirements identified. REQ-OBP-003a (trailing slash guarantee) is consistently referenced by REQ-OBP-005 and REQ-OBP-006 rather than re-stated, preventing contradiction. |
| Verifiable | Each requirement has an assigned ADIT verification method. Test oracles provide exact input/output pairs for deterministic test implementation. REQ-OBP-004d (schema validation) is verifiable by a deterministic CLI command. |
| Traceable | All requirements trace to a stakeholder need (STK-001 through STK-005). All requirements trace forward to an allocated component and at least one verification evidence gate. Orphan check: none. |
| Unambiguous | "Non-empty string" is defined (not None, not ""). "Trailing slash" is defined as exactly one `/` character at the end. The AC-3 boundary is explicitly partitioned into three sub-concerns. |
| Necessary | Each requirement removed would leave a stakeholder need unmet or create an untestable gap. The `WON'T` classification for runtime interpolation explicitly bounds scope without orphaning the need. |
| Implementation-Free | Requirements specify WHAT, not HOW. Exception: REQ-OBP-003b specifies file path and layer for `OutputResolver` — this is a structural constraint derived from H-07, not an implementation choice left to the developer. |

---

## References

- NPR 7123.1D, Process 1 (Stakeholder Expectations Definition) - Stakeholder needs STK-001 through STK-005
- NPR 7123.1D, Process 2 (Technical Requirements Definition) - REQ-OBP-001 through REQ-OBP-008
- NPR 7123.1D, Process 11 (Requirements Management) - Traceability matrix, change log
- NASA-HDBK-1009A - Requirements quality criteria (Complete, Consistent, Verifiable, Traceable, Unambiguous, Necessary)
- GitHub Issue #192 - Source acceptance criteria
- PROJ-021-ORCH-PLAN v1.2 (`projects/PROJ-021-output-base-path/orchestration/output-basepath-20260318-001/ORCHESTRATION_PLAN.md`) - Orchestration plan, AC-3 Known Gap documentation, Evidence Artifact Registry (Gates 1-6)
- `src/infrastructure/adapters/configuration/layered_config_adapter.py` - Existing config system
- `src/infrastructure/adapters/configuration/env_config_adapter.py` - Env var key mapping (`__` -> `.`)
- `src/bootstrap.py` - Composition root, `get_project_data_path()` function
- `src/interface/cli/adapter.py` - Existing `cmd_config_set` / `cmd_config_get` implementation
- `docs/rules/quality-enforcement.md` - H-07 (layer isolation), H-20 (BDD test-first, 90% coverage), H-34 (schema validation)

---

*Generated by nse-requirements agent v2.3.0*
*Phase: nse-1 | Workflow: output-basepath-20260318-001 | Date: 2026-03-18*
