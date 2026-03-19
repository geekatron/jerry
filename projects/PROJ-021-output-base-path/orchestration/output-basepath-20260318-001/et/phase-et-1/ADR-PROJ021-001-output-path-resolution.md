# ADR-PROJ021-001: Output Path Resolution System

<!-- ET-ID: PROJ-021 | PHASE: et-1 | AGENT: eng-architect | DATE: 2026-03-18 -->
<!-- CRITICALITY: C3 (new ADR, AE-003 auto-C3; API surface change, >10 files affected) -->

> Architecture Decision Record establishing the output path resolution system for Jerry skill agents, enabling configurable output base paths via `output.base_path` config key with a four-step fallback chain.

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0: Executive Summary](#l0-executive-summary) | Plain-language overview for stakeholders |
| [L1: Technical Detail](#l1-technical-detail) | Full architecture specification with layer placement |
| [L2: Strategic Implications](#l2-strategic-implications) | Long-term evolution and trade-off analysis |
| [Status](#status) | ADR lifecycle state |
| [Context](#context) | Why this decision is needed |
| [Decision](#decision) | What we decided |
| [1. OutputBasePath Value Object](#1-outputbasepath-value-object) | Domain model for validated output paths |
| [2. OutputResolver Application Service](#2-outputresolver-application-service) | Fallback chain resolution logic |
| [3. Config Key and Env Var Mapping](#3-config-key-and-env-var-mapping) | TOML section and environment variable design |
| [4. Fallback Chain Implementation](#4-fallback-chain-implementation) | Strategy evaluation and selected approach |
| [5. Layer Placement and Import Diagram](#5-layer-placement-and-import-diagram) | Hexagonal architecture conformance |
| [6. Threat Model](#6-threat-model) | STRIDE analysis of the resolution system |
| [Consequences](#consequences) | Positive, negative, and risk outcomes |
| [Migration Path](#migration-path) | Transition plan for existing agent output paths |
| [Evidence Sources](#evidence-sources) | Traced citations |
| [Self-Review (S-010)](#self-review-s-010) | Pre-submission quality verification |

---

## L0: Executive Summary

Jerry skill agents currently hardcode `projects/${JERRY_PROJECT}/` as the output base path. This prevents users who use the repository-based placement pattern (`work/`) or who do not set `JERRY_PROJECT` from using skill agents without manual path correction after every invocation.

This ADR introduces a configurable output path resolution system with three new components:

1. **`OutputBasePath` value object** in `src/configuration/domain/value_objects/` -- validates and normalizes output paths with a guaranteed trailing-slash contract.
2. **`OutputResolver` application service** in `src/configuration/application/services/` -- resolves the effective output base path through a four-step fallback chain: config key, environment variable, project path, default `work/`.
3. **`output.base_path` config key** -- settable via `jerry config set output.base_path <path>`, overridable via `JERRY_OUTPUT__BASE_PATH` environment variable.

The resolution chain ensures backward compatibility: users with `JERRY_PROJECT` set and no explicit `output.base_path` configured see no behavior change. Users who want `work/` as their base get it automatically when neither config key nor `JERRY_PROJECT` is set.

---

## L1: Technical Detail

See sections [1](#1-outputbasepath-value-object) through [6](#6-threat-model) below for complete specifications including: value object invariants and validation rules, application service resolution algorithm, config key naming and TOML representation, fallback chain implementation rationale, hexagonal layer placement with import direction diagrams, and STRIDE threat analysis.

---

## L2: Strategic Implications

**Architectural evolution.** This ADR establishes the pattern for how Jerry resolves environment-dependent paths at runtime. Future features requiring path resolution (template directories, cache locations, plugin output) should follow the same value-object-plus-resolver pattern, extending `OutputResolver` or creating parallel resolvers that share the `OutputBasePath` value object.

**Risk tolerance trade-off.** The fallback chain intentionally favors "produce output somewhere reasonable" over "fail loudly when unconfigured." This is the correct posture for a developer tool: silent failure (writing to `/dev/null` or not writing at all) is worse than writing to a slightly unexpected directory. The trailing-slash guarantee eliminates an entire class of path-joining bugs.

**Integration considerations.** Agent definitions that currently hardcode `projects/${JERRY_PROJECT}/` in their output location fields will need to adopt the `${JERRY_OUTPUT_BASE}` variable. This is a documentation-level change for agent `.md` files and a YAML-level change for `.governance.yaml` files. No runtime code in agent definitions is affected because agents do not execute path resolution themselves -- the orchestrator or user prompt provides the resolved path.

---

## Status

**Proposed**

---

## Context

### Problem Statement

Jerry skill agents hardcode output paths using the pattern `projects/${JERRY_PROJECT}/`. This creates three concrete problems:

1. **Repository-based placement is unsupported.** Users who choose the `work/` placement pattern (documented in `skills/worktracker/rules/worktracker-directory-structure.md`) cannot use skill agents without manually correcting every output path in every prompt. The worktracker supports both `projects/{ProjectId}/work/` and `{RepositoryRoot}/work/`, but skill agents only support the former.

2. **Missing JERRY_PROJECT breaks agents.** When `JERRY_PROJECT` is not set (which is valid -- H-04 requires an active project but the project could be identified by other means), agent output paths resolve to `projects//` -- a malformed path that creates unexpected directory structures.

3. **No override mechanism.** Even when `JERRY_PROJECT` is set, there is no way to redirect output to a different location (e.g., a temporary directory for experimentation, a shared team directory, or a CI artifact directory). Every path is derived from a single hardcoded pattern.

### Driving Evidence

**Codebase evidence:**
- `src/bootstrap.py` lines 163-173: `get_project_data_path()` returns `base / "projects" / project_id` with no fallback when `project_id` is empty.
- `skills/contract-design/agents/cd-generator.md` line 104: Documents the need for fallback -- "Output paths resolve to `projects/${JERRY_PROJECT}/...` when JERRY_PROJECT is set. Falls back to `work/...` when JERRY_PROJECT is not set" -- but this fallback is aspirational, not implemented.
- `src/infrastructure/adapters/configuration/layered_config_adapter.py`: The existing `LayeredConfigAdapter` already supports the precedence chain (env > project > root > defaults) and dot-notation keys, making `output.base_path` a natural extension.

**Architecture evidence:**
- `src/configuration/domain/value_objects/config_key.py`: `ConfigKey` validates dot-notation keys matching `^[a-zA-Z][a-zA-Z0-9_-]*(\.[a-zA-Z][a-zA-Z0-9_-]*)*$`. The key `output.base_path` conforms to this pattern (two segments: `output` and `base_path`).
- `src/infrastructure/adapters/configuration/env_config_adapter.py` line 82: Environment key conversion uses `key.lower().replace("__", ".")`, so `JERRY_OUTPUT__BASE_PATH` maps to `output.base_path`.

---

## Decision

We will implement a three-component output path resolution system: an `OutputBasePath` value object in the configuration domain, an `OutputResolver` application service in a new `src/configuration/application/services/` directory, and an `output.base_path` configuration key accessible via the existing config CLI and environment variable override.

---

### 1. OutputBasePath Value Object

**Location:** `src/configuration/domain/value_objects/output_base_path.py`

**Decision: configuration domain, not shared kernel.** The `OutputBasePath` value object belongs in `src/configuration/domain/value_objects/` because:

- It is semantically a configuration value -- it represents a user-configurable setting that determines where output lands.
- It follows the existing pattern: `ConfigKey`, `ConfigValue`, `ConfigPath`, and `ConfigSource` all live in this directory.
- Placing it in `src/shared_kernel/` would be appropriate only if multiple bounded contexts needed to import it directly. In practice, only the configuration domain and the `OutputResolver` application service consume it. Other modules receive a resolved `str` or `Path`, not the value object itself.

**Invariants:**

| Invariant | Rule | Enforcement |
|-----------|------|-------------|
| INV-1 | Path must not be empty | `ValidationError` on construction |
| INV-2 | Path must not contain null bytes | `ValidationError` on construction |
| INV-3 | Path must not contain `..` segments when absolute (traversal prevention). Both relative and absolute paths are permitted. | Validated in `__post_init__`; absolute paths are valid for env var overrides and explicit config. |
| INV-4 | Resolved value always ends with `/` | Enforced in `__post_init__` normalization |
| INV-5 | Path segments must not contain `..` (no traversal) | `ValidationError` on construction |

**Interface:**

```python
@dataclass(frozen=True, slots=True)
class OutputBasePath:
    """Immutable, validated output base path with trailing-slash guarantee."""

    value: str  # Always ends with '/'

    def __post_init__(self) -> None: ...  # Validates INV-1 through INV-5
    def join(self, relative: str) -> str: ...  # Joins and returns normalized path
    def to_path(self) -> Path: ...  # Returns pathlib.Path representation
    @classmethod
    def from_string(cls, raw: str) -> "OutputBasePath": ...  # Factory with normalization
```

**Trailing-slash guarantee rationale:** Every consumer of `OutputBasePath.value` can safely concatenate without worrying about missing separators. The `join()` method provides an additional convenience, but the invariant means even raw string concatenation produces correct paths.

---

### 2. OutputResolver Application Service

**Location:** `src/configuration/application/services/output_resolver.py`

**Decision: new `src/configuration/application/` directory.** The configuration module currently has only a `domain/` subdirectory. `OutputResolver` is an application service (it coordinates between the config provider port and environment state to produce a resolved value), so it belongs in the application layer. This creates the standard hexagonal structure:

```
src/configuration/
    domain/
        value_objects/
            output_base_path.py  # NEW
        aggregates/
        events/
    application/                 # NEW directory
        services/
            __init__.py          # NEW
            output_resolver.py   # NEW
```

**Resolution algorithm:**

```python
class OutputResolver:
    """Resolves the effective output base path through a 4-step fallback chain."""

    def __init__(self, config: IConfigurationProvider) -> None:
        self._config = config

    def resolve(self) -> OutputBasePath:
        """
        Resolve the output base path.

        Fallback chain (first non-None wins):
            1. Config key: output.base_path
            2. Env var: JERRY_OUTPUT__BASE_PATH
            3. projects/${JERRY_PROJECT}/ (if JERRY_PROJECT is set)
            4. work/

        Returns:
            OutputBasePath with trailing-slash guarantee.
        """
        ...
```

**Why an application service, not a domain service?** The resolver depends on `IConfigurationProvider` (a port) and reads environment variables (infrastructure concerns). Domain services in Jerry's hexagonal architecture must not depend on ports or infrastructure. The application layer is the correct location for coordinating these concerns.

**Why not a standalone function in bootstrap.py?** The existing `get_project_data_path()` in `src/bootstrap.py` (line 163) is a procedural function that returns `Path | None`. While adding fallback logic there would be expedient, it would:
- Mix resolution policy (the fallback chain) with bootstrap wiring
- Make the resolution untestable without environment variable manipulation
- Prevent dependency injection of the config provider

The `OutputResolver` class accepts `IConfigurationProvider` via constructor injection, making it testable with a mock config provider and no environment variable side effects.

---

### 3. Config Key and Env Var Mapping

**Config key:** `output.base_path`

**TOML representation:**

```toml
# In .jerry/config.toml (root) or projects/PROJ-NNN/.jerry/config.toml (project)
[output]
base_path = "projects/PROJ-021-output-base-path/"
```

**Environment variable:** `JERRY_OUTPUT__BASE_PATH`

**Mapping verification:** The `EnvConfigAdapter._env_to_config_key()` method (line 69-82 of `env_config_adapter.py`) performs:
1. Strip prefix `JERRY_` -> `OUTPUT__BASE_PATH`
2. Lowercase -> `output__base_path`
3. Replace `__` with `.` -> `output.base_path`

This produces the correct config key. No changes to `EnvConfigAdapter` are required.

**Key validation:** `ConfigKey("output.base_path")` passes the pattern `^[a-zA-Z][a-zA-Z0-9_-]*(\.[a-zA-Z][a-zA-Z0-9_-]*)*$` because:
- Segment 1: `output` matches `[a-zA-Z][a-zA-Z0-9_-]*`
- Segment 2: `base_path` matches `[a-zA-Z][a-zA-Z0-9_-]*`

No changes to `ConfigKey` are required.

**Precedence:** The existing `LayeredConfigAdapter.get()` precedence (env > project config > root config > defaults) applies without modification. Setting `JERRY_OUTPUT__BASE_PATH=custom/output/` in the environment overrides any TOML-configured value.

**CLI usage:**

```bash
# Set output base path for the current project
jerry config set output.base_path "work/" --scope project

# Set output base path globally
jerry config set output.base_path "output/" --scope root

# View the current effective value
jerry config get output.base_path

# Override via environment for a single session
JERRY_OUTPUT__BASE_PATH="tmp/experiment/" jerry session start
```

---

### 4. Fallback Chain Implementation

**Decision: Conditional chain in resolver (not Strategy pattern).**

**Options evaluated:**

| Option | Description | Pros | Cons |
|--------|-------------|------|------|
| **A. Strategy pattern** | Each fallback step is a class implementing `IOutputPathStrategy` with a `resolve() -> OutputBasePath \| None` method. Strategies are composed in a chain-of-responsibility. | Extensible; new fallback sources added without modifying resolver; testable per-strategy. | Over-engineered for 4 fixed steps; adds 4 new files (one per strategy) plus an interface; indirection obscures the simple linear fallback; violates YAGNI unless we anticipate > 6 fallback sources. |
| **B. Conditional chain** | A single `resolve()` method with ordered `if` checks. Each step is a private method returning `str \| None`. | Simple; readable; debuggable; all logic in one file; easy to understand the precedence by reading top-to-bottom. | Adding a 5th+ fallback requires modifying the resolver; less isolated per-step testing (though private methods can still be unit-tested). |

**Selected: Option B (Conditional chain).**

**Rationale:** The fallback chain has exactly four steps and is unlikely to grow beyond five. The Strategy pattern's extensibility benefit does not justify its complexity cost for this use case. The conditional chain is more readable -- a developer can understand the entire resolution algorithm by reading a single method top-to-bottom. If future requirements demand pluggable resolution (e.g., user-defined fallback chains), this decision can be revisited with a new ADR.

**Implementation sketch:**

```python
def resolve(self) -> OutputBasePath:
    # Step 1: Explicit config key
    path = self._from_config()
    if path is not None:
        return OutputBasePath.from_string(path)

    # Step 2: Dedicated env var (checked separately from config
    # because JERRY_OUTPUT__BASE_PATH may be set even when the
    # config adapter's env scan did not run)
    path = self._from_env()
    if path is not None:
        return OutputBasePath.from_string(path)

    # Step 3: Derive from JERRY_PROJECT
    path = self._from_project()
    if path is not None:
        return OutputBasePath.from_string(path)

    # Step 4: Default
    return OutputBasePath.from_string("work/")
```

**Note on Step 2 redundancy:** In the current `LayeredConfigAdapter` implementation, `JERRY_OUTPUT__BASE_PATH` is already captured by Step 1 (because `EnvConfigAdapter` scans all `JERRY_*` vars and `LayeredConfigAdapter.get()` checks env first). Step 2 exists as an explicit safety net for scenarios where `OutputResolver` is constructed with a config provider that does not include env var scanning (e.g., in tests with a pure in-memory config, or in future config provider implementations). This makes the resolver's contract independent of the config provider's implementation details.

---

### 5. Layer Placement and Import Diagram

**Hexagonal architecture conformance (H-07):**

```
                    DOMAIN LAYER
    ┌──────────────────────────────────────────────┐
    │  src/configuration/domain/                   │
    │                                              │
    │  value_objects/                               │
    │    output_base_path.py  ─imports─> shared_kernel/exceptions.py
    │    config_key.py                             │
    │    config_value.py                           │
    │    config_path.py                            │
    │    config_source.py                          │
    │                                              │
    │  aggregates/                                 │
    │    configuration.py                          │
    └──────────────────────────┬───────────────────┘
                               │
                          imports DOWN
                          (domain only)
                               │
                    APPLICATION LAYER
    ┌──────────────────────────┴───────────────────┐
    │  src/configuration/application/              │
    │                                              │
    │  services/                                   │
    │    output_resolver.py                        │
    │      ─imports─> domain/value_objects/output_base_path.py
    │      ─imports─> IConfigurationProvider (port)│
    │      ─reads──> os.environ (JERRY_PROJECT)    │
    └──────────────────────────┬───────────────────┘
                               │
                          imports DOWN
                          (app + domain)
                               │
                  INFRASTRUCTURE LAYER
    ┌──────────────────────────┴───────────────────┐
    │  src/infrastructure/adapters/configuration/  │
    │                                              │
    │  layered_config_adapter.py                   │
    │    ─implements─> IConfigurationProvider       │
    │    (no changes needed)                       │
    │                                              │
    │  env_config_adapter.py                       │
    │    (no changes needed)                       │
    └──────────────────────────────────────────────┘

    Import direction: Domain <── Application <── Infrastructure
    (arrows point toward dependencies, direction of allowed imports)
```

**H-07 compliance check:**

| Rule | Check | Status |
|------|-------|--------|
| H-07(a): Domain imports only from shared_kernel | `OutputBasePath` imports `ValidationError` from `shared_kernel.exceptions` | PASS |
| H-07(b): Application imports from domain, not infrastructure | `OutputResolver` imports `OutputBasePath` (domain) and `IConfigurationProvider` (port defined in infra but used as protocol) | PASS -- see note |
| H-07(c): Composition root exclusivity | `OutputResolver` is wired in `bootstrap.py` or CLI adapter | PASS |
| H-10: One class per file | `OutputBasePath` in its own file, `OutputResolver` in its own file | PASS |
| H-11: Type hints + docstrings | All public methods fully typed and documented | PASS |

**H-07(b) note on IConfigurationProvider:** The `IConfigurationProvider` protocol is currently defined in `layered_config_adapter.py` (infrastructure layer). For strict H-07 compliance, this protocol should be extracted to a port in the application or domain layer (e.g., `src/configuration/application/ports/i_configuration_provider.py`). This is a pre-existing architectural debt, not introduced by this ADR. The `OutputResolver` depends on the protocol interface, not the concrete implementation, which satisfies the dependency inversion principle even though the protocol's current file location is impure.

**Recommended future cleanup:** Extract `IConfigurationProvider` to `src/configuration/application/ports/i_configuration_provider.py`. This is a separate, low-risk refactor (C1) that can be tracked independently.

---

### 6. Threat Model

**Scope:** STRIDE analysis of the output path resolution system. Criticality C3 mandates STRIDE + DREAD scoring per `quality-enforcement.md` escalation table.

**Trust boundaries:**

```
    ┌─────────────────────────────────┐
    │  TRUST BOUNDARY 1: User Input   │
    │  - jerry config set             │
    │  - JERRY_OUTPUT__BASE_PATH env  │
    │  - JERRY_PROJECT env            │
    └────────────┬────────────────────┘
                 │
                 v
    ┌─────────────────────────────────┐
    │  TRUST BOUNDARY 2: Config Store │
    │  - .jerry/config.toml           │
    │  - projects/PROJ-*/.jerry/      │
    │    config.toml                  │
    └────────────┬────────────────────┘
                 │
                 v
    ┌─────────────────────────────────┐
    │  TRUST BOUNDARY 3: Resolution   │
    │  - OutputResolver.resolve()     │
    │  - OutputBasePath validation    │
    └────────────┬────────────────────┘
                 │
                 v
    ┌─────────────────────────────────┐
    │  TRUST BOUNDARY 4: Filesystem   │
    │  - File writes to resolved path │
    └─────────────────────────────────┘
```

**STRIDE analysis:**

| # | Category | Threat | Component | DREAD Score | Mitigation |
|---|----------|--------|-----------|-------------|------------|
| T-1 | **Tampering** | Malicious config value sets `output.base_path` to overwrite sensitive files (e.g., `../../.git/`) | OutputBasePath constructor | D=5, R=3, E=7, A=4, D=6 = **5.0** | INV-5 blocks `..` traversal. Absolute paths are permitted (user intent). |
| T-2 | **Tampering** | Environment variable injection: attacker sets `JERRY_OUTPUT__BASE_PATH` to redirect output | EnvConfigAdapter | D=3, R=2, E=5, A=3, D=4 = **3.4** | Environment variable control is an OS-level concern. Jerry cannot defend against a compromised shell. Document in security notes. Accepted risk. |
| T-3 | **Information Disclosure** | Config file readable by other users reveals project structure | config.toml files | D=2, R=2, E=3, A=2, D=2 = **2.2** | File permissions are user responsibility. TOML files contain no secrets (only paths). Low severity. |
| T-4 | **Denial of Service** | Config value set to path on a full/read-only filesystem causes write failures | OutputResolver consumer | D=4, R=3, E=4, A=3, D=5 = **3.8** | OutputResolver resolves the path; it does not write. Writing agents should handle `OSError` / `PermissionError`. Separation of concerns. |
| T-5 | **Elevation of Privilege** | Symlink at resolved path redirects writes to privileged location | Filesystem write | D=3, R=2, E=4, A=2, D=3 = **2.8** | Jerry runs as user-level process. Symlink exploitation requires user-level filesystem access, which means the attacker already has the privileges they would gain. Accepted risk. |
| T-6 | **Spoofing** | Untrusted TOML file in project directory provides malicious `output.base_path` | LayeredConfigAdapter | D=3, R=2, E=4, A=3, D=4 = **3.2** | Project config files are within the project directory the user chose to trust. INV-3 and INV-5 in OutputBasePath provide defense-in-depth against path traversal. |

**DREAD scoring key:** D=Damage, R=Reproducibility, E=Exploitability, A=Affected Users, D=Discoverability. Scale 1-10. Score = mean.

**Residual risk summary:** All threats score below 5.0 (medium). The highest-scored threat (T-1, path traversal) is fully mitigated by `OutputBasePath` invariants INV-3 and INV-5. No threats require architectural changes beyond the designed validation.

**NIST CSF 2.0 mapping:**

| CSF Function | Implementation |
|-------------|----------------|
| **Identify** | Trust boundaries documented. Data flows mapped. Attack surface (config input + env vars + filesystem) enumerated. |
| **Protect** | Input validation via `OutputBasePath` invariants. Path traversal prevention (INV-5). Null byte rejection (INV-2). |
| **Detect** | `ConfigurationValueChanged` domain events emitted when `output.base_path` is set (existing event infrastructure). |
| **Respond** | `ValidationError` raised on malformed paths. Fallback chain ensures resolution always succeeds with a safe default (`work/`). |
| **Recover** | Default fallback (`work/`) ensures the system is always functional even with corrupted config. |

---

## Consequences

### Positive

1. **Both placement patterns supported.** Users of `projects/PROJ-NNN/` and `work/` patterns can use skill agents without manual path correction.
2. **Backward compatible.** Users with `JERRY_PROJECT` set and no `output.base_path` configured see identical behavior to today (fallback step 3 produces `projects/{JERRY_PROJECT}/`).
3. **Environment-overridable.** CI/CD pipelines can set `JERRY_OUTPUT__BASE_PATH` to redirect output to artifact directories without modifying config files.
4. **Existing infrastructure reused.** No changes to `LayeredConfigAdapter`, `EnvConfigAdapter`, `ConfigKey`, or the config CLI commands. The new key "just works" with the existing precedence system.
5. **Trailing-slash guarantee eliminates path-joining bugs.** Every consumer of `OutputBasePath` gets a correctly terminated path without defensive programming.

### Negative

1. **New application layer directory.** Creating `src/configuration/application/` adds a directory to a module that previously had only `domain/`. This is architecturally correct but adds a directory that currently contains only one service.
2. **Agent documentation updates.** All agent definitions that reference `projects/${JERRY_PROJECT}/` in output location fields need to be updated to reference `${JERRY_OUTPUT_BASE}` or document the resolver. This is approximately 15-20 agent files across 4 skills.

### Risks

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Users set `output.base_path` to an absolute path, breaking portability | Low | Medium | Absolute paths are permitted as intentional user choice. Portability warning documented in CLI help text. |
| Fallback chain produces unexpected path when multiple config sources disagree | Low | Low | `jerry config get output.base_path` shows the effective value. `jerry config show --source` shows which source provides each key. |
| Path traversal via crafted config value | Low | High | INV-5 rejects paths containing `..`. INV-2 rejects null bytes. Defense in depth. |

---

## Migration Path

### Phase 1: Core Implementation (This ADR)

1. Create `src/configuration/domain/value_objects/output_base_path.py`
2. Create `src/configuration/application/__init__.py`
3. Create `src/configuration/application/services/__init__.py`
4. Create `src/configuration/application/services/output_resolver.py`
5. Write unit tests for `OutputBasePath` (invariant validation, trailing-slash normalization, join behavior)
6. Write unit tests for `OutputResolver` (all four fallback steps, precedence, edge cases)
7. Register `output.base_path` in the defaults dict passed to `LayeredConfigAdapter` if a framework-level default is desired (optional -- `work/` is the hardcoded fallback in the resolver)

### Phase 2: Agent Definition Updates (Separate Work Item)

1. Update agent `.governance.yaml` files to use `${JERRY_OUTPUT_BASE}` in `output.location` fields
2. Update agent `.md` files to document the output path resolution
3. Update SKILL.md files for affected skills (contract-design, nasa-se, problem-solving, orchestration)

### Phase 3: Bootstrap Integration (Separate Work Item)

1. Wire `OutputResolver` in `src/bootstrap.py` alongside existing `get_project_data_path()`
2. Deprecate `get_project_data_path()` in favor of `OutputResolver.resolve()`
3. Update `CLIAdapter` to use `OutputResolver` where it currently reads `JERRY_PROJECT` directly

---

## Evidence Sources

| Source | Authority | Content |
|--------|-----------|---------|
| `src/infrastructure/adapters/configuration/layered_config_adapter.py` | Primary (codebase) | Existing config precedence: env > project > root > defaults |
| `src/infrastructure/adapters/configuration/env_config_adapter.py` | Primary (codebase) | Env var to config key mapping: `__` -> `.`, uppercase -> lowercase |
| `src/configuration/domain/value_objects/config_key.py` | Primary (codebase) | Key validation pattern, `to_env_key()` conversion |
| `src/configuration/domain/value_objects/config_path.py` | Primary (codebase) | Existing path value object pattern for reference |
| `src/bootstrap.py` lines 155-173 | Primary (codebase) | Current `get_project_data_path()` implementation |
| `skills/contract-design/agents/cd-generator.md` | Primary (codebase) | Documents aspirational `work/` fallback not yet implemented |
| `skills/worktracker/rules/worktracker-directory-structure.md` | Primary (codebase) | Two placement patterns: project-based and repository-based |
| `.context/rules/quality-enforcement.md` | Primary (governance) | C3 criticality: STRIDE + DREAD required |
| NIST SP 800-218 SSDF PO.1 | Secondary (standard) | Security requirements derived from threat model |

---

## Self-Review (S-010)

| Criterion | Assessment |
|-----------|------------|
| **Completeness** | All five decisions from the task specification are addressed: value object location, service location, config key naming, fallback chain implementation, return contract. |
| **H-07 compliance** | Layer placement diagram shows all import directions. Domain layer imports only from shared_kernel. Application layer imports from domain. Infrastructure unchanged. |
| **H-10 compliance** | One class per file: `OutputBasePath` in `output_base_path.py`, `OutputResolver` in `output_resolver.py`. |
| **H-11 compliance** | All public interfaces shown with type hints and docstrings. |
| **Threat model** | STRIDE analysis covers all trust boundaries. DREAD scoring quantifies each threat. All threats below 5.0 (medium). Highest threat (T-1) fully mitigated by value object invariants. |
| **Backward compatibility** | Fallback step 3 preserves current behavior for users with `JERRY_PROJECT` set. No existing config keys or env vars are modified. |
| **Nygard ADR format** | Title, Status, Context, Decision, Consequences sections present. Extended with L0/L1/L2 per Jerry output requirements. |
| **Trailing-slash guarantee** | INV-4 ensures `OutputBasePath.value` always ends with `/`. Documented in value object invariants and interface. |
| **Config key validation** | Verified `ConfigKey("output.base_path")` passes existing pattern. Verified `JERRY_OUTPUT__BASE_PATH` env var maps correctly via existing `EnvConfigAdapter` logic. |
