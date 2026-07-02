# Security Review: Output Base Path Resolution Feature (GitHub Issue #192)

<!-- VERSION: 1.0.0 | DATE: 2026-03-18 | AGENT: eng-security | SOURCE: GitHub Issue #192 -->

> STRIDE threat analysis and manual secure code review for the configurable output base path feature.
> Scope: `OutputBasePath` value object, `OutputResolver` service, `get_project_data_path()`, CLI config commands, and 6 governance YAML files.

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0 Executive Summary](#l0-executive-summary) | Finding counts, top risks, immediate actions |
| [L1 Technical Findings](#l1-technical-findings) | Individual finding reports with CWE, CVSS, evidence, remediation |
| [L2 Strategic Implications](#l2-strategic-implications) | Security posture, systemic patterns, threat model correlation |
| [ASVS Verification Status](#asvs-verification-status) | OWASP ASVS 5.0 chapter verification results |
| [STRIDE Threat Matrix](#stride-threat-matrix) | Full STRIDE category analysis |
| [Review Methodology](#review-methodology) | Scope, approach, and evidence sources |

---

## L0 Executive Summary

### Finding Counts by Severity

| Severity | Count | CWE |
|----------|-------|-----|
| HIGH | 2 | CWE-22, CWE-73 |
| MEDIUM | 3 | CWE-20, CWE-532, CWE-778 |
| LOW | 2 | CWE-20, CWE-116 |
| INFO | 1 | Design observation |
| **TOTAL** | **8** | |

### Overall Security Assessment

**CONDITIONAL PASS with REQUIRED remediations.** The feature's core architecture is sound: the single-validation-point (OutputBasePath value object), deterministic fallback chain, and pure path resolution (no directory creation) all reduce attack surface. However, the validation scope is dangerously narrow. Null-byte rejection alone is insufficient to prevent path traversal (CWE-22), and the absence of any audit logging for path configuration changes means that malicious or accidental output redirection is undetectable (CWE-778). Two findings are HIGH severity and require remediation before this feature ships to users who operate in multi-user or shared-filesystem environments.

### Top 3 Risk Areas

1. **Path Traversal via unvalidated `../` sequences** (FIND-001, HIGH) -- An attacker who can set `JERRY_OUTPUT__BASE_PATH` or write to any TOML config file can redirect output to any filesystem location the process user can write to. The value object only checks for null bytes; `../../etc/cron.d/` is accepted without error.

2. **Symlink-based path escape** (FIND-002, HIGH) -- The resolver returns a path string and callers (e.g., `FileSystemEventStore`) open files at that path without verifying the resolved path is within the intended directory. A symlink at the configured path can redirect all writes to an attacker-controlled location.

3. **Silent output redirection with no audit trail** (FIND-005, MEDIUM) -- There is no logging of what path was resolved, what source provided it, or when it changed. A compromised config file or environment variable silently redirects output; the user cannot detect this after the fact.

### Recommended Immediate Actions

1. Add `../` and absolute-path-outside-project validation to `OutputBasePath.__post_init__` or `OutputResolver.resolve()` before writes occur.
2. Add a `realpath`-based boundary check in `get_project_data_path()` that asserts the resolved path is under `project_root`.
3. Emit a structured audit log entry from `get_project_data_path()` that records the resolved path and its source (env, project config, root config, fallback).

---

## L1 Technical Findings

---

### FIND-001: Path Traversal via `../` in Configured Output Path

| Field | Value |
|-------|-------|
| **CWE** | CWE-22 (Improper Limitation of a Pathname to a Restricted Directory) |
| **CVSS 3.1 Score** | 7.1 (High) |
| **CVSS Vector** | AV:L/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:L |
| **Affected Location** | `src/configuration/domain/value_objects/output_base_path.py:47-52` |
| **ASVS Requirement** | V5.1.1 (Input validation for all untrusted data) |

**Data Flow Trace:**

```
[Attacker] sets JERRY_OUTPUT__BASE_PATH=../../etc/cron.d/
    |
    v
EnvConfigAdapter._parse_value()        [env_config_adapter.py:98-149]
    -> returns raw string "../../etc/cron.d/"
    |
    v
LayeredConfigAdapter.get("output.base_path")  [layered_config_adapter.py:197-199]
    -> env value wins, returns "../../etc/cron.d/"
    |
    v
OutputResolver.resolve()               [output_resolver.py:79-82]
    -> value = "../../etc/cron.d/"
    -> OutputBasePath("../../etc/cron.d/")
          __post_init__: checks for "\x00" only -- PASSES
    -> returns "../../etc/cron.d/"
    |
    v
get_project_data_path()               [bootstrap.py:197-205]
    -> resolved = "../../etc/cron.d/"
    -> returns project_root / "../../etc/cron.d/"
          = Path("/workspace/jerry/../../etc/cron.d/")
          = Path("/etc/cron.d/")   [after normalization]
    |
    v
FileSystemEventStore(project_path)    [filesystem_event_store.py:98-101]
    -> self._events_dir = /etc/cron.d/.jerry/data/events/
    -> appends events to files under /etc/
```

**Evidence:**

```python
# output_base_path.py lines 47-52: the ONLY validation
def __post_init__(self) -> None:
    if "\x00" in self.value:
        raise ValueError(
            f"Output base path must not contain null bytes: {self.value!r}"
        )
# "../" sequences are explicitly permitted -- docstring says
# "Relative and absolute paths are both accepted"
```

```python
# output_resolver.py lines 79-82: no sanitization before use
value = self._config.get(_CONFIG_KEY)
if value is not None and str(value) != "":
    path = OutputBasePath(str(value))
    return self._ensure_trailing_slash(path.value)  # returns raw ../../../ path
```

```python
# bootstrap.py lines 197-205: Path() does NOT prevent traversal
return project_root / resolved
# Path("/workspace/jerry") / "../../etc/cron.d/" == Path("/etc/cron.d/")
```

**Reproduction Steps:**

```bash
export JERRY_OUTPUT__BASE_PATH="../../etc/cron.d/"
export JERRY_PROJECT="PROJ-001"
uv run jerry session start  # writes events to /etc/cron.d/.jerry/data/events/
```

**Remediation:**

Option A (preferred -- boundary check in bootstrap): After resolving, assert the resolved absolute path is under `project_root`:

```python
# bootstrap.py -- add after resolved = resolver.resolve()
resolved_abs = (project_root / resolved).resolve()
try:
    resolved_abs.relative_to(project_root.resolve())
except ValueError:
    raise ValueError(
        f"Resolved output path '{resolved_abs}' escapes project root "
        f"'{project_root}'. Check output.base_path configuration."
    )
return resolved_abs
```

Option B (defense-in-depth -- validation in value object):

```python
# output_base_path.py -- add to __post_init__
import os
normalized = os.path.normpath(self.value)
if normalized.startswith(".."):
    raise ValueError(
        f"Output base path must not traverse above the project root: {self.value!r}"
    )
if os.path.isabs(normalized):
    raise ValueError(
        f"Output base path must be relative to the project root: {self.value!r}. "
        "Use output.base_path in project config for relative paths only."
    )
```

Note: Option B alone is insufficient because `os.path.isabs` does not prevent symlink-based traversal (see FIND-002). Both options should be applied.

---

### FIND-002: Symlink Escape -- Resolved Path Not Verified Against `realpath`

| Field | Value |
|-------|-------|
| **CWE** | CWE-73 (External Control of File Name or Path) |
| **CVSS 3.1 Score** | 6.3 (High) |
| **CVSS Vector** | AV:L/AC:H/PR:L/UI:N/S:U/C:L/I:H/A:N |
| **Affected Location** | `src/bootstrap.py:197-205` |
| **ASVS Requirement** | V5.1.2 (Symlink validation before file operations) |

**Data Flow Trace:**

```
[Attacker] creates symlink: /workspace/jerry/projects/PROJ-001/.jerry -> /etc/
    |
    v
get_project_data_path()               [bootstrap.py:179-205]
    -> project_root = Path("/workspace/jerry")
    -> resolved = "projects/PROJ-001/"    [JERRY_PROJECT fallback]
    -> returns project_root / "projects/PROJ-001/"
          = Path("/workspace/jerry/projects/PROJ-001/")
    |
    v
FileSystemEventStore._events_dir:
    = /workspace/jerry/projects/PROJ-001/.jerry/data/events/
    |
    v
    .jerry -> /etc/  (symlink, attacker-planted)
    |
    v
actual write target: /etc/data/events/  [arbitrary write under /etc/]
```

**Evidence:** `get_project_data_path()` at line 205 returns `project_root / resolved` without calling `Path.resolve()` or any check that the physical path is still under `project_root`. Python's `Path.__truediv__` and `Path.joinpath` do not follow symlinks.

**Remediation:**

```python
# bootstrap.py -- replace return statement
candidate = project_root / resolved
real = candidate.resolve()
root_real = project_root.resolve()
try:
    real.relative_to(root_real)
except ValueError:
    raise ValueError(
        f"Resolved output path '{real}' is outside the project root "
        f"'{root_real}' (possible symlink attack)."
    )
return real
```

---

### FIND-003: Arbitrary Config Key Write via `cmd_config_set` Without Key Allowlist

| Field | Value |
|-------|-------|
| **CWE** | CWE-20 (Improper Input Validation) |
| **CVSS 3.1 Score** | 4.4 (Medium) |
| **CVSS Vector** | AV:L/AC:L/PR:L/UI:N/S:U/C:N/I:L/A:N |
| **Affected Location** | `src/interface/cli/adapter.py:1202-1222` |
| **ASVS Requirement** | V5.1.4 (Allowlist validation for structured inputs) |

**Data Flow Trace:**

```
[User] jerry config set output.base_path "../../etc/" --scope root
    |
    v
cmd_config_set(key="output.base_path", value="../../etc/", scope="root")
    -> parts = ["output", "base_path"]
    -> writes to .jerry/config.toml WITHOUT calling OutputBasePath validation
    -> TOML file now contains: base_path = "../../etc/"
    |
    v
Next invocation of get_project_data_path()
    -> reads from TOML, passes to OutputResolver
    -> OutputResolver creates OutputBasePath("../../etc/")
    -> null byte check only: PASSES
    -> returns "../../etc/"
    -> path traversal achieved (see FIND-001)
```

**Evidence:** `cmd_config_set` at lines 1202-1222 accepts any dot-separated key and any string value. There is no call to `OutputBasePath(value)` before writing to TOML. The validation that does exist (`OutputBasePath.__post_init__`) is only invoked at read time by `OutputResolver`, not at write time. This means an invalid but traversal-capable value can be persisted to disk and take effect on the next process invocation.

**Remediation:**

Add a key-specific validator in `cmd_config_set` that applies domain validation at write time:

```python
# adapter.py -- add before current[parts[-1]] = coerced_value
from src.configuration.domain.value_objects.output_base_path import OutputBasePath
_KEY_VALIDATORS = {
    "output.base_path": lambda v: OutputBasePath(str(v)),
}
if key in _KEY_VALIDATORS:
    _KEY_VALIDATORS[key](coerced_value)  # raises ValueError if invalid
```

---

### FIND-004: `CLAUDE_PROJECT_DIR` Environment Variable Accepted Without Validation

| Field | Value |
|-------|-------|
| **CWE** | CWE-20 (Improper Input Validation) |
| **CVSS 3.1 Score** | 4.4 (Medium) |
| **CVSS Vector** | AV:L/AC:L/PR:L/UI:N/S:U/C:N/I:L/A:N |
| **Affected Location** | `src/bootstrap.py:179-180` |
| **ASVS Requirement** | V5.1.1 (Input validation for untrusted environment data) |

**Data Flow Trace:**

```
[Attacker] sets CLAUDE_PROJECT_DIR=/tmp/attacker_dir
    |
    v
get_project_data_path()               [bootstrap.py:179-180]
    -> project_root_env = os.environ.get("CLAUDE_PROJECT_DIR")
    -> project_root = Path("/tmp/attacker_dir")   [no validation]
    |
    v
All downstream paths anchored at /tmp/attacker_dir:
    -> config read from /tmp/attacker_dir/.jerry/config.toml  (attacker-controlled)
    -> config.toml can set output.base_path to anything
    -> events written to /tmp/attacker_dir/...
```

**Evidence:**

```python
# bootstrap.py lines 179-180
project_root_env = os.environ.get("CLAUDE_PROJECT_DIR")
project_root = Path(project_root_env) if project_root_env else Path.cwd()
# No existence check, no realpath normalization, no allowlist
```

**Note on context:** `CLAUDE_PROJECT_DIR` is set by Claude Code itself and is not intended to be user-controllable in that sense. However, in developer environments, test scripts, or CI, this variable could be set by an adversary or misconfiguration. The risk is medium because exploitation requires the ability to set environment variables, which typically implies local access.

**Remediation:**

```python
if project_root_env:
    project_root = Path(project_root_env).resolve()
    if not project_root.exists():
        raise ValueError(f"CLAUDE_PROJECT_DIR does not exist: {project_root}")
else:
    project_root = Path.cwd().resolve()
```

---

### FIND-005: No Audit Logging for Output Path Resolution or Changes

| Field | Value |
|-------|-------|
| **CWE** | CWE-778 (Insufficient Logging) |
| **CVSS 3.1 Score** | 4.0 (Medium) |
| **CVSS Vector** | AV:L/AC:L/PR:L/UI:N/S:U/C:N/I:N/A:N / supplemental: non-repudiation impact |
| **Affected Location** | `src/configuration/application/services/output_resolver.py:63-90`, `src/bootstrap.py:153-205` |
| **ASVS Requirement** | V7.1.1 (Log security events including path/config changes) |

**Observation:** Neither `OutputResolver.resolve()` nor `get_project_data_path()` emits any log entry recording:

- The resolved path value
- The configuration source that determined the path (env, project config, root config, fallback)
- Whether the path was overridden from default
- Who (which process, which invocation) resolved the path

An attacker who successfully redirects output via a compromised config file or environment variable leaves no forensic trace in application logs. There is no way to determine after the fact that output was being written to a non-standard location.

**Remediation:**

```python
# output_resolver.py -- add structured logging to resolve()
import logging
_log = logging.getLogger(__name__)

def resolve(self) -> str:
    value = self._config.get(_CONFIG_KEY)
    if value is not None and str(value) != "":
        path = OutputBasePath(str(value))
        result = self._ensure_trailing_slash(path.value)
        _log.info(
            "output_path_resolved",
            extra={"path": result, "source": "config", "config_key": _CONFIG_KEY}
        )
        return result
    project_id = os.environ.get("JERRY_PROJECT", "")
    if project_id:
        result = self._ensure_trailing_slash(f"projects/{project_id}")
        _log.info(
            "output_path_resolved",
            extra={"path": result, "source": "jerry_project_fallback", "project": project_id}
        )
        return result
    _log.debug("output_path_resolved", extra={"path": _TERMINAL_FALLBACK, "source": "terminal_fallback"})
    return _TERMINAL_FALLBACK
```

---

### FIND-006: Config Value Displayed Without Sanitization in CLI Output

| Field | Value |
|-------|-------|
| **CWE** | CWE-532 (Insertion of Sensitive Information into Log File) / CWE-116 (Improper Encoding of Output) |
| **CVSS 3.1 Score** | 2.9 (Low) |
| **CVSS Vector** | AV:L/AC:H/PR:L/UI:R/S:U/C:L/I:N/A:N |
| **Affected Location** | `src/interface/cli/adapter.py:1127-1129`, `1270-1272` |
| **ASVS Requirement** | V5.3.1 (Output encoding for terminal context) |

**Observation:** `cmd_config_get` prints the raw config value to stdout without any encoding or sanitization (line 1129: `print(value)`). `cmd_config_set` echoes the raw value back (line 1270: `print(f"Set {key} = {coerced_value}")`). If a path value contains ANSI escape sequences (e.g., `\x1b[31m`), they will be rendered by the terminal. This is a low-severity injection concern in the terminal context.

**Example:** A path value such as `work/\x1b[2J\x1b[H` (which passes null byte validation) would clear the terminal when displayed.

**Remediation:**

```python
# Sanitize for terminal output -- strip or replace non-printable characters
import unicodedata
def _safe_display(value: str) -> str:
    return "".join(c if unicodedata.category(c)[0] != "C" else "?" for c in str(value))

print(_safe_display(value))
```

---

### FIND-007: `${JERRY_OUTPUT_BASE}` Token in Governance YAMLs -- Expansion Not Validated

| Field | Value |
|-------|-------|
| **CWE** | CWE-20 (Improper Input Validation) |
| **CVSS 3.1 Score** | 2.1 (Low) |
| **CVSS Vector** | AV:L/AC:H/PR:L/UI:R/S:U/C:N/I:L/A:N |
| **Affected Location** | 6 governance YAML files: `skills/*/agents/*.governance.yaml` |
| **ASVS Requirement** | V5.1.1 |

**Observation:** Six governance YAML files contain `${JERRY_OUTPUT_BASE}` as a path prefix token in their `output.location` fields:

- `skills/contract-design/agents/cd-validator.governance.yaml:62`
- `skills/contract-design/agents/cd-generator.governance.yaml:75`
- `skills/test-spec/agents/tspec-generator.governance.yaml:61`
- `skills/test-spec/agents/tspec-analyst.governance.yaml:64`
- `skills/use-case/agents/uc-author.governance.yaml:51`
- `skills/use-case/agents/uc-slicer.governance.yaml:52`

These tokens are expanded at runtime when agents construct their output paths. If the `${JERRY_OUTPUT_BASE}` value itself contains `../` (as enabled by the weak validation in FIND-001), the expanded path `${JERRY_OUTPUT_BASE}contracts/UC-...` will silently produce a traversal path. The governance YAMLs themselves are not the vulnerability -- the expansion logic consuming them is. This finding flags the downstream impact surface.

**Remediation:** After FIND-001 is resolved, the expansion logic for `${JERRY_OUTPUT_BASE}` must also call the same boundary check. The fix to `get_project_data_path()` in FIND-001 Option A covers this if the expansion always routes through `OutputResolver`, but this should be verified against the agent output path construction code path.

---

### FIND-008 (INFO): Empty String Treated as "Not Set" -- Distinguish Intentional Empty From Absent

| Field | Value |
|-------|-------|
| **CWE** | N/A (Design Observation) |
| **CVSS Score** | N/A |
| **Affected Location** | `src/configuration/application/services/output_resolver.py:80` |

**Observation:**

```python
if value is not None and str(value) != "":
```

The resolver treats an explicit empty string (`""`) identically to the key being absent (`None`). This means `jerry config set output.base_path ""` does not produce an error but silently falls through to the JERRY_PROJECT or terminal fallback. A user who intends to clear a previously set path by writing an empty string may be surprised that the behavior is "use fallback" rather than an explicit confirmation. This is a design edge case, not a security vulnerability by itself, but it could mask configuration mistakes.

**Recommendation:** Either explicitly document this behavior in the CLI help text for `output.base_path`, or reject empty strings with a clear error: "Use `jerry config unset output.base_path` to revert to the default."

---

## ASVS Verification Status

OWASP ASVS 5.0 chapters relevant to this feature scope:

| ASVS Chapter | Requirement ID | Requirement Summary | Status | Notes |
|---|---|---|---|---|
| V5 -- Validation | V5.1.1 | Input validation for all untrusted data | FAIL | Null byte only; path traversal not blocked |
| V5 -- Validation | V5.1.2 | Reject path traversal attempts | FAIL | No `../` or absolute path rejection |
| V5 -- Validation | V5.1.4 | Allowlist for structured inputs | PARTIAL | No allowlist on config keys in `cmd_config_set` |
| V7 -- Logging | V7.1.1 | Log security events | FAIL | No path resolution events logged |
| V7 -- Logging | V7.1.2 | Log authentication and authorization failures | N/A | Not applicable to this feature |
| V8 -- Data Protection | V8.1.1 | Sensitive data not stored unnecessarily | PASS | Path values are not credentials |
| V8 -- Data Protection | V8.3.1 | Prevent path escapes from intended directories | FAIL | No realpath boundary check (FIND-002) |
| V9 -- Communication | V9.x | Communication security | N/A | Local filesystem only |

**Summary:** 3 FAIL, 1 PARTIAL, 1 PASS, 3 N/A.

---

## STRIDE Threat Matrix

### S -- Spoofing

**Threat:** An attacker spoofs legitimate application output by controlling where the application writes. If `JERRY_OUTPUT__BASE_PATH` can be set to a legitimate-looking path (e.g., `projects/PROJ-OFFICIAL/`), output from the attacker's session will appear in a trusted project's directory.

**Affected Components:** `EnvConfigAdapter._load_from_env()`, `OutputResolver.resolve()` step 1.

**Risk:** MEDIUM. Requires the ability to set environment variables for the process.

**Current Controls:** None specific to this threat. The layered config system does not restrict who can set `JERRY_OUTPUT__BASE_PATH`.

**Residual Risk After FIND-001 Remediation:** LOW. The boundary check limits writes to paths under `project_root`.

---

### T -- Tampering

**Threat 1 (FIND-001, HIGH):** An attacker who can write to any config TOML file (`.jerry/config.toml` or `projects/*/jerry/config.toml`) can set `output.base_path` to a traversal path, causing the application to write to attacker-designated filesystem locations.

**Threat 2 (FIND-002, HIGH):** An attacker who can create symlinks anywhere on the filesystem can plant a symlink inside the resolved output directory that redirects writes to an attacker-controlled location.

**Threat 3 (FIND-003, MEDIUM):** The `jerry config set` CLI command accepts path values without applying domain validation at write time. A malformed value is written to TOML and only validated at the next read.

**Current Controls:** TOML files are protected by OS file permissions. `AtomicFileAdapter` provides write atomicity. `OutputBasePath` rejects null bytes.

**Exploitability:** Requires local write access to config files or ability to create symlinks -- realistic in shared development environments.

---

### R -- Repudiation

**Threat (FIND-005, MEDIUM):** There is no logging of what output path was resolved or what configuration source determined it. An attacker who redirects output can deny the action because no forensic evidence is produced.

**Current Controls:** None. No audit log. No per-invocation record of resolved paths.

**Gap:** This directly maps to ASVS V7.1.1. The absence of logging makes incident investigation impossible after the fact.

---

### I -- Information Disclosure

**Threat 1:** The resolved path is exposed in `cmd_config_get` and `cmd_config_set` terminal output. If the path contains any sensitive naming (e.g., usernames, internal project names, IP addresses in a network path), this information is printed to stdout without filtering.

**Threat 2 (FIND-004, MEDIUM):** If `CLAUDE_PROJECT_DIR` is set to a path that does not exist but whose config TOML is attacker-controlled, `LayeredConfigAdapter._load_toml` silently returns an empty dict on `TOMLDecodeError` (line 148-150). This means malformed TOML silently falls through to lower-precedence sources without any indication that the intended config was not applied. The user does not know their project-specific config was silently ignored.

**Current Controls:** None specific. TOML parse errors are silently swallowed.

**Recommendation for Threat 2:** Log a warning when TOML parsing fails:
```python
except tomllib.TOMLDecodeError as e:
    import logging
    logging.getLogger(__name__).warning(
        "config_toml_parse_error", extra={"path": str(path), "error": str(e)}
    )
    return {}
```

---

### D -- Denial of Service

**Threat 1:** An attacker sets `JERRY_OUTPUT__BASE_PATH` to a path on a network filesystem that is unavailable or very slow. All subsequent `FileSystemEventStore` write operations will hang or fail. This requires no special privileges beyond setting an environment variable.

**Threat 2:** An attacker sets `output.base_path` to a path on a full or read-only filesystem. All write operations will fail. Combined with the silent config behavior, this may cause confusing application failures.

**Assessment:** LOW. Both threats require local access. The application already has fallback to InMemoryEventStore when `get_project_data_path()` returns `None`, but this fallback is only triggered when both the config AND `JERRY_PROJECT` are unset. A configured-but-unavailable path does not trigger the fallback.

**Remediation:** Consider adding a path accessibility pre-check in `FileSystemEventStore.__init__` that raises a descriptive error rather than failing silently on the first write.

---

### E -- Elevation of Privilege

**Primary Threat (FIND-001 + FIND-002, combined HIGH):** The path traversal and symlink findings combine into an Elevation of Privilege pathway. If an unprivileged user can redirect output to:

- System cron directories (`/etc/cron.d/`, `/etc/cron.hourly/`)
- Authorized keys files (`~/.ssh/authorized_keys`)
- Sudoers drop-ins (`/etc/sudoers.d/`)
- Systemd unit directories (`/etc/systemd/system/`)

...then writing crafted event content to those locations achieves privilege escalation. The risk is realized only if: (1) FIND-001 or FIND-002 is exploitable, AND (2) the process user has write access to privileged directories. In typical developer environments, this risk is moderate.

**Current Controls:** OS-level file permissions provide the primary barrier. The null-byte check in `OutputBasePath` does not address this.

**Residual Risk After Both FIND-001 and FIND-002 Remediated:** LOW, bounded by OS filesystem permissions.

---

## L2 Strategic Implications

### Security Posture Assessment

The output base path feature introduces a new attack surface that did not exist before: a user-configurable, process-honored path that determines where the application writes persistent data. The pre-existing codebase had hardcoded paths, which are simpler to reason about from a security standpoint. The architectural decision to make this path fully configurable via environment variables, TOML files, and CLI commands expands the attack surface at three independent entry points.

The design decision documented in the ADR -- "OutputBasePath rejects null bytes only" -- is the root cause of the HIGH findings. This decision reflects a minimalist domain modeling philosophy (the value object should be lightweight), but it transfers validation responsibility to callers. The problem is that callers in this codebase do not exercise that responsibility consistently.

### Systemic Vulnerability Patterns

**Pattern 1: Write-time vs. Read-time Validation Asymmetry.** The application validates config values at read time (when `OutputResolver` creates an `OutputBasePath`) but not at write time (when `cmd_config_set` persists a value to TOML). This asymmetry means invalid values can persist in configuration files and take effect after the process that wrote them has exited. This is a recurring pattern in the codebase that should be addressed architecturally: the `cmd_config_set` command should always apply the same validators used by the domain model.

**Pattern 2: Trust Inheritance from Environment Variables.** The env-wins precedence in `LayeredConfigAdapter` means that any environment variable named `JERRY_OUTPUT__BASE_PATH` immediately overrides all other configuration, including admin-set project configs. This is architecturally intentional (12-Factor App pattern) but creates a configuration injection surface. In CI/CD environments where environment variables are set by pipeline scripts, this means pipeline compromise can redirect output paths.

**Pattern 3: No Boundary Validation After Path Composition.** The composition `project_root / resolved` in `get_project_data_path()` relies on the caller (the PathLib `__truediv__` operator) to silently handle relative traversal. Python's `Path` does not raise an error on `Path("/workspace") / "../../etc/"`. This pattern -- composing a root with an untrusted suffix without a subsequent `realpath` boundary check -- should be treated as a code smell and flagged in code review checklists.

### Threat Model Correlation

These findings align with the threat model's expected concern that user-configurable paths are CWE-22 candidates. The design decision to support both relative and absolute paths accepts more threat surface than a relative-only design would. If the ADR's rationale for accepting absolute paths is revisited, restricting `output.base_path` to relative paths only would eliminate FIND-001 Option B partially and reduce the Elevation of Privilege risk to near-zero for typical filesystem permission models.

### Recommendations for Security Architecture Evolution

1. **Introduce a `PathSandbox` domain concept.** Add a domain service `PathSandbox(root: Path)` with a single method `resolve(relative: str) -> Path` that encapsulates the `realpath` boundary check. All callers that compose `project_root / user_supplied` should use this service instead. This eliminates the pattern at the class level.

2. **Enforce write-time validation in `cmd_config_set`.** Create a registry of per-key validators that mirrors the domain model's validation. `cmd_config_set` should consult this registry before writing. This eliminates the write-time/read-time asymmetry systemically.

3. **Add a structured audit log for security-relevant config changes.** At minimum, log path resolution source and value on each invocation. Consider persisting this to a separate, append-only audit log file that is distinct from the event store (which is itself subject to path redirection).

4. **Document the accepted threat model for `JERRY_OUTPUT__BASE_PATH` in the ADR.** The current ADR (ADR-PROJ021-001) should explicitly acknowledge that env var control of output paths is an accepted risk in trusted developer environments, and document the boundary check as a required mitigating control.

---

## Review Methodology

### Scope

| Component | File | Lines Reviewed |
|-----------|------|----------------|
| `OutputBasePath` value object | `src/configuration/domain/value_objects/output_base_path.py` | All (57 lines) |
| `OutputResolver` service | `src/configuration/application/services/output_resolver.py` | All (105 lines) |
| `get_project_data_path()` | `src/bootstrap.py` | 153-205 |
| CLI config set/get | `src/interface/cli/adapter.py` | 1097-1285 |
| `LayeredConfigAdapter` | `src/infrastructure/adapters/configuration/layered_config_adapter.py` | All (383 lines) |
| `EnvConfigAdapter` | `src/infrastructure/adapters/configuration/env_config_adapter.py` | All (258 lines) |
| `FileSystemEventStore` | `src/work_tracking/infrastructure/persistence/filesystem_event_store.py` | Write paths only |
| 6 governance YAMLs | `skills/*/agents/*.governance.yaml` | `output.location` fields |

### Review Approach

1. Full source read of all files in scope.
2. Data flow tracing from all external input points (env vars, TOML files, CLI arguments) through the path resolution chain to the write endpoint.
3. CWE Top 25 2025 checklist applied: CWE-22 (path traversal), CWE-73 (external path control), CWE-20 (input validation), CWE-778 (insufficient logging), CWE-116 (output encoding).
4. ASVS 5.0 V5 and V7 chapters verified against implementation.
5. STRIDE threat analysis conducted against all six threat categories.

### Evidence Quality

All findings are evidence-based with line-number citations and code excerpts. CVSS scores reflect the local access requirement (AV:L) consistent with Jerry's design as a developer CLI tool. Scores would be elevated (AV:N) if Jerry were deployed as a server-side service.

---

*Review Date: 2026-03-18*
*Reviewer Agent: eng-security*
*SSDF Practice: PW.7 (Manual Code Review)*
*GitHub Issue: #192*
*CWE Top 25 2025 Applied: CWE-22, CWE-73, CWE-20, CWE-778, CWE-532, CWE-116*
