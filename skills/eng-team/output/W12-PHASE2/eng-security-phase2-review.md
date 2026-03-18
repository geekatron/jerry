# Security Code Review -- W12-PHASE2
## tool_exec Bounded Context: Manual Vulnerability Review

**Agent:** eng-security
**Engagement ID:** W12-PHASE2
**Criticality:** C3
**Review Date:** 2026-03-17
**Methodology:** Manual source code review, data flow tracing, CWE Top 25 2025, OWASP ASVS 5.0
**SSDF Practice:** PW.7

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0 Executive Summary](#l0-executive-summary) | Finding counts, top risks, immediate actions |
| [L1 Technical Findings](#l1-technical-findings) | Full CWE/CVSS detail per finding with code evidence |
| [L2 Strategic Implications](#l2-strategic-implications) | Patterns, posture, architectural observations |
| [Mitigation Verification](#mitigation-verification) | M-01, M-02, M-03 implementation assessment |
| [ASVS Chapter Verification](#asvs-chapter-verification) | Chapter-level pass/fail/partial status |
| [Scope and Methodology](#scope-and-methodology) | Files reviewed, approach |

---

## L0 Executive Summary

### Finding Counts by Severity

| Severity | Count |
|----------|-------|
| Critical | 0 |
| High | 1 |
| Medium | 3 |
| Low | 2 |
| Informational | 2 |
| **Total** | **8** |

### Overall Security Assessment

The `tool_exec` bounded context demonstrates a well-structured security posture for a framework of this scope. The three mandated mitigations (M-01, M-02, M-03) are correctly implemented. The most significant risk is an unvalidated path injection in `--evidence-dir` (FINDING-001, High), which allows an attacker-controlled CLI argument to redirect quarantined credential-bearing output to an arbitrary filesystem location, bypassing engagement isolation guarantees. No hardcoded credentials were found. No `shell=True` subprocess calls were found. YAML loading is exclusively `yaml.safe_load`.

### Top 3 Risk Areas

1. **Path Traversal via --evidence-dir override** (FINDING-001, CWE-22, High): The `--evidence-dir` CLI parameter is accepted as a raw `Path` string without allowlist or canonicalization validation. An operator could specify `../../` paths that redirect evidence writes outside the engagement directory.
2. **Engagement ID validation gap in is_initialized() and helper methods** (FINDING-002, CWE-22, Medium): The `_validate_id()` allowlist is only called from `initialize()`. The `is_initialized()`, `evidence_dir()`, and `quarantine_dir()` methods accept raw engagement ID strings without validation, creating a path-composition risk if called with unvalidated input from non-CLI entry points.
3. **resolver_class name not constrained by allowlist** (FINDING-003, CWE-94, Medium): While the module path allowlist (M-01) prevents loading arbitrary modules, the `resolver_class` string from `tool_families.yaml` is passed directly to `getattr()` without validation. A tampered YAML can use `resolver_class` to access any attribute of an allowed module, including module-level callables that are not ToolFamilyResolverPort implementations.

### Recommended Immediate Actions

1. Add path canonicalization and project-root containment check to `_persist_evidence()` for the `evidence_dir_override` parameter. (FINDING-001)
2. Add `_validate_id()` calls to `is_initialized()`, `evidence_dir()`, and `quarantine_dir()` in `EngagementInitializer`. (FINDING-002)
3. Add an explicit class name allowlist or regex pattern constraint to `_validate_module_path()` scope in `FamilyRegistryLoader`, extended to cover `resolver_class`. (FINDING-003)

---

## L1 Technical Findings

---

### FINDING-001: Unvalidated Path in --evidence-dir Override

| Field | Value |
|-------|-------|
| **ID** | FINDING-001 |
| **Severity** | High |
| **CWE** | CWE-22: Improper Limitation of a Pathname to a Restricted Directory (Path Traversal) |
| **CVSS 3.1 Vector** | AV:L/AC:L/PR:L/UI:N/S:C/C:L/I:H/A:N |
| **CVSS 3.1 Score** | 6.8 |
| **Affected File** | `src/interface/cli/tool_exec_commands.py` lines 409-411 |
| **ASVS Reference** | V5.1.2 (Input validation, file paths) |

**Description**

The `--evidence-dir` CLI argument is accepted as a raw string and converted directly to a `Path` object without any validation, canonicalization, or containment check. This value is user-supplied and lands in `_persist_evidence()` where it is used as the directory for writing evidence files that may contain filtered tool output.

**Data Flow Trace**

```
CLI argument: --evidence-dir ../../tmp/exfil
  -> argparse stores as args.evidence_dir (parser.py:1049-1053)
  -> getattr(args, "evidence_dir", None)  (tool_exec_commands.py:84)
  -> _persist_evidence(evidence_dir_override=evidence_dir_override)  (line 218)
  -> evidence_dir = Path(evidence_dir_override)  (line 410)
  -> evidence_dir.mkdir(parents=True, exist_ok=True)  (line 411)
  -> evidence_file.write_text(filtered_output, ...)  (line 419)
```

No validation occurs between argument intake and `Path()` construction. `parents=True` will create the full path including traversed parent directories.

**Code Evidence**

```python
# tool_exec_commands.py lines 409-411
if evidence_dir_override:
    evidence_dir = Path(evidence_dir_override)
    evidence_dir.mkdir(parents=True, exist_ok=True)
```

The engagement isolation model guarantees that evidence lands in `work/engagements/{id}/evidence/`. The `--evidence-dir` override bypasses this entirely.

**Impact**

A user invoking `jerry tool exec --evidence-dir /tmp/captured nuclei ...` redirects evidence files (containing raw tool output, SHA-256 metadata, and engagement context) to an attacker-controlled location. If tool output contains credentials that evade the L1 regex filter (e.g., encoded or novel formats), raw_stdout is written to the evidence file. Crucially, the `_persist_evidence` function also writes `raw_output` to its evidence file, not just `filtered_output`. Redirecting evidence to a world-readable path exposes this data.

Note: the meta.json written alongside contains `tool_command` and `tool_args` in plaintext (line 425-426) -- these may contain target hostname or scope data that should remain within engagement isolation.

**Proof of Vulnerability**

```bash
# Redirect evidence outside engagement boundary to world-readable path
jerry tool exec --engagement-id eng-001 \
  --evidence-dir /tmp/world-readable-path \
  nuclei -target example.com
# Evidence file is written to /tmp/world-readable-path/
# Bypasses quarantine directory 0o700 permission protections
```

**Remediation**

```python
def _validate_evidence_dir(evidence_dir_override: str, project_root: Path) -> Path:
    """Validate and canonicalize the evidence directory override.

    Raises ValueError if the resolved path escapes the project root.
    """
    resolved = Path(evidence_dir_override).resolve()
    try:
        resolved.relative_to(project_root.resolve())
    except ValueError:
        msg = (
            f"--evidence-dir '{evidence_dir_override}' resolves outside "
            f"project root. Use a path under: {project_root}"
        )
        raise ValueError(msg)
    return resolved
```

Call `_validate_evidence_dir(evidence_dir_override, project_root)` before `evidence_dir.mkdir()`. This applies `.resolve()` to canonicalize symlinks and relative segments, then asserts containment within the project root.

---

### FINDING-002: Missing Engagement ID Validation in Non-initialize Paths

| Field | Value |
|-------|-------|
| **ID** | FINDING-002 |
| **Severity** | Medium |
| **CWE** | CWE-22: Improper Limitation of a Pathname to a Restricted Directory (Path Traversal) |
| **CVSS 3.1 Vector** | AV:L/AC:H/PR:L/UI:N/S:C/C:L/I:M/A:N |
| **CVSS 3.1 Score** | 5.0 |
| **Affected File** | `src/tool_exec/domain/services/engagement_initializer.py` lines 105-141 |
| **ASVS Reference** | V5.1.2 (Input validation, file paths) |

**Description**

`_validate_id()` with the M-05 character-class allowlist is only invoked by `initialize()`. Three other public methods -- `is_initialized()`, `evidence_dir()`, and `quarantine_dir()` -- compose filesystem paths using the raw `engagement_id` string without calling `_validate_id()` first.

**Data Flow Trace**

```
engagement_id = "../../etc"  # hypothetical attacker-controlled value
  -> EngagementInitializer.is_initialized("../../etc")  (line 105)
  -> engagement_dir = self._base_dir / "../../etc"      (line 114)
  -> (engagement_dir / "evidence").is_dir()             (line 116)
  # Path resolves to /base_dir/../../etc/evidence -- traversal succeeds
  # is_initialized() returns False (directory unlikely to exist)
  # BUT if it does exist, could cause false True return
```

For `evidence_dir()` and `quarantine_dir()`, the traversed path is returned to the caller and used for file writes.

**Code Evidence**

```python
# engagement_initializer.py -- is_initialized() calls NO validation
def is_initialized(self, engagement_id: str) -> bool:
    engagement_dir = self._base_dir / engagement_id  # raw composition
    return (
        (engagement_dir / self.EVIDENCE_DIR).is_dir()
        ...
    )

# evidence_dir() -- no validation before path construction
def evidence_dir(self, engagement_id: str) -> Path:
    return self._base_dir / engagement_id / self.EVIDENCE_DIR  # raw composition
```

**Current Exposure Context**

In the CLI handler (`tool_exec_commands.py`), `engagement_id` flows from argparse through `handle_tool_exec()` to `engagement_init.is_initialized(engagement_id)` on line 178. The CLI path validates `engagement_id` indirectly through `_handle_init_engagement` only when `--init-engagement` is passed -- but `--engagement-id` accepts any string value without prior validation before the `is_initialized()` call.

**Severity Rationale**

Rated Medium (not High) because: the current CLI path does not call `evidence_dir()` or `quarantine_dir()` with unvalidated IDs in practice -- `is_initialized()` acts as a gate. However, this is a defense-in-depth gap: the allowlist protection is localized to one code path, and any future caller of these methods who does not pre-validate will silently introduce path traversal.

**Remediation**

Add `self._validate_id(engagement_id)` as the first statement in `is_initialized()`, `evidence_dir()`, and `quarantine_dir()`. The `_validate_id()` method already exists and raises `ValueError` on invalid input -- this is a three-line fix with zero logic change.

```python
def is_initialized(self, engagement_id: str) -> bool:
    self._validate_id(engagement_id)  # ADD THIS
    engagement_dir = self._base_dir / engagement_id
    ...
```

---

### FINDING-003: Unvalidated resolver_class Name in Registry Loader

| Field | Value |
|-------|-------|
| **ID** | FINDING-003 |
| **Severity** | Medium |
| **CWE** | CWE-94: Improper Control of Generation of Code (Code Injection) |
| **CVSS 3.1 Vector** | AV:L/AC:H/PR:H/UI:N/S:U/C:L/I:L/A:L |
| **CVSS 3.1 Score** | 4.2 |
| **Affected File** | `src/tool_exec/infrastructure/registry/family_registry_loader.py` lines 192-200 |
| **ASVS Reference** | V5.1.1 (Input validation, trust boundaries) |

**Description**

M-01 correctly constrains the `resolver_module` dotted path via `_ALLOWED_MODULE_PREFIXES`. However, the `resolver_class` string is taken directly from `tool_families.yaml` and passed to `getattr(module, family_info.resolver_class)` without any validation. Any attribute on the allowed module -- including functions, constants, or nested callables -- can be retrieved this way. The `issubclass()` check on the retrieved attribute provides a secondary gate, but only catches instances that are not subclasses of `ToolFamilyResolverPort`; it does not prevent retrieval and attempted-call of arbitrary module-level objects.

**Data Flow Trace**

```
tool_families.yaml: resolver_class: "os.system"   # tampered value
  -> ToolFamilyInfo(resolver_class="os.system")  (family_registry_loader.py:136)
  -> getattr(module, "os.system")                (line 192)
  # AttributeError raised (os.system not in adapter module)
  # BUT: resolver_class: "__builtins__" would return the builtins dict/module
  # resolver_class: "open" on a module that re-exports open would return builtin open
```

More concretely: if a future adapter module imports `subprocess` at module level (which `local_executor.py` and `container_executor.py` both do), then `resolver_class: "subprocess"` would cause `getattr(module, "subprocess")` to return the subprocess module. The `issubclass(subprocess, ToolFamilyResolverPort)` call would raise `TypeError` (not `ValueError`), which is caught by the bare `except Exception` in `load()` (line 88) and reraised -- but the getattr execution itself has already occurred.

**Severity Rationale**

Rated Medium because: (a) `tool_families.yaml` requires local file modification (elevated access), (b) the module path allowlist substantially limits the attack surface, and (c) the `issubclass` check and exception handling provide a secondary barrier. The residual risk is from the gap between M-01's module-path protection and the unconstrained class attribute access.

**Remediation**

Add a `resolver_class` name validation function:

```python
_CLASS_NAME_PATTERN: re.Pattern[str] = re.compile(r"^[A-Z][a-zA-Z0-9]{1,63}$")

def _validate_class_name(self, class_name: str) -> None:
    """Validate resolver class name: CamelCase identifier, 2-64 chars."""
    if not _CLASS_NAME_PATTERN.match(class_name):
        msg = (
            f"Resolver class name '{class_name}' is invalid. "
            "Must be a CamelCase Python identifier (2-64 characters)."
        )
        raise ValueError(msg)
```

Call `self._validate_class_name(family_info.resolver_class)` in `_load_resolver()` before the `getattr()` call, after `_validate_module_path()`.

---

### FINDING-004: Credential Filter Only Scans stdout; stderr Passes Unfiltered

| Field | Value |
|-------|-------|
| **ID** | FINDING-004 |
| **Severity** | Medium |
| **CWE** | CWE-200: Exposure of Sensitive Information to an Unauthorized Actor |
| **CVSS 3.1 Vector** | AV:N/AC:H/PR:N/UI:R/S:U/C:L/I:N/A:N |
| **CVSS 3.1 Score** | 3.1 |
| **Affected Files** | `src/tool_exec/infrastructure/adapters/local_executor.py` lines 111-130; `container_executor.py` lines 132-163 |
| **ASVS Reference** | V8.2.2 (Client-side data protection, sensitive data not logged) |

**Description**

Both `LocalExecutor.execute()` and `ContainerExecutor.execute()` apply the credential filter only to `stdout`. The `stderr` stream is captured (`capture_output=True`) and passed through to the caller entirely unfiltered. Security tools frequently write credentials, key material, session tokens, and connection strings to stderr. For example, Metasploit's `msfconsole` writes session token output to stderr; `impacket-secretsdump` may write discovered NTLM hashes to stderr.

**Code Evidence**

```python
# local_executor.py lines 113-123
if self._credential_filter is not None and not no_filter:
    filter_result = self._credential_filter.filter_output(raw_stdout)  # stdout only
    return ExecutionResult(
        exit_code=4 if filter_result.detected else result.returncode,
        stdout=filter_result.filtered_output,
        stderr=result.stderr,   # <-- unfiltered stderr returned to caller
        ...
    )
```

The same pattern appears in `container_executor.py` lines 145-155.

**Impact**

Tool credentials output on stderr bypass the L1 regex filter, the quarantine pipeline, and the `CREDENTIAL_DETECTED` (exit code 4) signal. They are printed to the terminal (line 235 in `tool_exec_commands.py`) and may be captured by shell pipelines, log aggregators, or CI/CD systems that record process stderr.

**Remediation**

Apply the credential filter to both `result.stderr` and `result.stdout`. If a credential is detected in either stream, trigger the quarantine pipeline. Update `ExecutionResult.stderr` to hold the filtered value and introduce `raw_stderr` analogous to `raw_stdout`.

```python
raw_stdout = result.stdout
raw_stderr = result.stderr
if self._credential_filter is not None and not no_filter:
    stdout_result = self._credential_filter.filter_output(raw_stdout)
    stderr_result = self._credential_filter.filter_output(raw_stderr)
    detected = stdout_result.detected or stderr_result.detected
    return ExecutionResult(
        exit_code=4 if detected else result.returncode,
        stdout=stdout_result.filtered_output,
        stderr=stderr_result.filtered_output,
        raw_stdout=raw_stdout,
        raw_stderr=raw_stderr,
        credential_detected=detected,
        ...
    )
```

---

### FINDING-005: Strict Mode Default is Env-var Controlled and Case-Sensitive

| Field | Value |
|-------|-------|
| **ID** | FINDING-005 |
| **Severity** | Low |
| **CWE** | CWE-304: Missing Critical Step in Authentication (logic flaw in policy gate) |
| **CVSS 3.1 Score** | 2.9 (AV:L/AC:H/PR:L/UI:N/S:U/C:L/I:N/A:N) |
| **Affected File** | `src/interface/cli/tool_exec_commands.py` lines 97-98 |
| **ASVS Reference** | V5.1.1 (Input validation) |

**Description**

The M-03 strict mode gate reads `JERRY_STRICT_MODE` from the environment with a default of `"true"` (string, not bool), then compares via `.lower() == "true"`. The comparison is case-normalised correctly. However, the gate logic has two subtle weaknesses:

1. **Any value other than "true" bypasses the gate.** The check `if strict_mode == "true"` means `JERRY_STRICT_MODE=1`, `JERRY_STRICT_MODE=yes`, `JERRY_STRICT_MODE=True` (before `.lower()`), and `JERRY_STRICT_MODE=TRUE` would all bypass the block (`.lower()` handles the last two, but `1` and `yes` do not). An AI agent generating shell config might emit `JERRY_STRICT_MODE=1` believing it is enabling strict mode.

2. **The warning log for non-strict mode may not be visible to the operator.** The `logger.warning()` call on line 107 uses the Python logger, which outputs to stderr by default. In container environments or when stderr is suppressed, this warning is silently dropped.

**Code Evidence**

```python
strict_mode = os.environ.get("JERRY_STRICT_MODE", "true").lower()
if strict_mode == "true":
    # block --no-filter
    ...
# else: warning logged, execution proceeds
```

**Remediation**

Replace the string comparison with a strict boolean parser:

```python
_STRICT_MODE_TRUE_VALUES = frozenset({"true", "1", "yes", "on"})
_STRICT_MODE_FALSE_VALUES = frozenset({"false", "0", "no", "off"})

def _is_strict_mode_enabled() -> bool:
    raw = os.environ.get("JERRY_STRICT_MODE", "true").lower().strip()
    if raw in _STRICT_MODE_TRUE_VALUES:
        return True
    if raw in _STRICT_MODE_FALSE_VALUES:
        return False
    # Unknown value -- fail closed (treat as strict)
    logger.warning("Unrecognised JERRY_STRICT_MODE value '%s'; treating as true.", raw)
    return True
```

---

### FINDING-006: YAML config_path from tool_families.yaml is Not Validated

| Field | Value |
|-------|-------|
| **ID** | FINDING-006 |
| **Severity** | Low |
| **CWE** | CWE-22: Path Traversal |
| **CVSS 3.1 Score** | 2.9 (AV:L/AC:H/PR:H/UI:N/S:U/C:L/I:N/A:N) |
| **Affected File** | `src/tool_exec/infrastructure/registry/family_registry_loader.py` lines 130-140 |
| **ASVS Reference** | V5.1.2 (Input validation, file paths) |

**Description**

The `config_path` field from `tool_families.yaml` is stored in `ToolFamilyInfo.config_path` and later passed to the resolver's `load_config()`. No path validation, canonicalization, or project-root containment check is performed. A tampered `tool_families.yaml` entry with `config_path: ../../../../etc/passwd` would cause the `RainbowToolResolver.load_config()` to attempt to read that path.

**Code Evidence**

```python
# family_registry_loader.py line 137
config_path=entry["config_path"],  # raw string from YAML, no validation

# Called in _load_resolver line 202
return resolver_cls(config_path=family_info.config_path)
```

**Severity Rationale**

Rated Low rather than Medium because: (a) `load_config()` opens the file in read-only text mode, and YAML parsing of a binary file (e.g., `/etc/shadow`) would fail cleanly with a `ValueError`; (b) the file requires local access to modify; (c) `yaml.safe_load` is used, preventing deserialization exploit via the config itself.

**Remediation**

Add a config path validation function in `FamilyRegistryLoader._parse_registry()`:

```python
def _validate_config_path(self, config_path: str, project_root: Path) -> None:
    resolved = (project_root / config_path).resolve()
    if not resolved.is_relative_to(project_root.resolve()):
        msg = f"config_path '{config_path}' resolves outside project root"
        raise ValueError(msg)
```

---

### FINDING-007: Evidence Meta Files Include tool_args in Plaintext

| Field | Value |
|-------|-------|
| **ID** | FINDING-007 |
| **Severity** | Informational |
| **CWE** | CWE-312: Cleartext Storage of Sensitive Information |
| **CVSS 3.1 Score** | N/A (Informational) |
| **Affected File** | `src/interface/cli/tool_exec_commands.py` lines 421-430 |
| **ASVS Reference** | V8.1.1 (Data protection in transit/at rest) |

**Description**

The `.meta.json` evidence file writes `tool_args` as a plaintext JSON array (line 425-426). Tool arguments for security tools frequently include `--password`, `--api-key`, target credentials, or authorization tokens. These would appear in the meta file verbatim.

**Code Evidence**

```python
meta = {
    ...
    "tool_command": tool_command,
    "tool_args": tool_args,   # plaintext list of all args
    ...
}
```

**Note**

The `SecurityPolicy.redacted_env_vars` field exists for environment variable redaction. No equivalent mechanism exists for argument redaction.

**Recommendation**

Apply the same credential filter patterns to each element of `tool_args` before persisting to the meta file. Mark detected sensitive arguments as `[REDACTED]`. This is consistent with the existing L1 regex layer approach and does not require new infrastructure.

---

### FINDING-008: No Upper Bound on tool Output Size Before Filter Scan

| Field | Value |
|-------|-------|
| **ID** | FINDING-008 |
| **Severity** | Informational |
| **CWE** | CWE-400: Uncontrolled Resource Consumption |
| **CVSS 3.1 Score** | N/A (Informational) |
| **Affected File** | `src/tool_exec/domain/services/credential_filter.py` lines 183-214 |

**Description**

`CredentialFilterService.filter_output()` splits the raw output on newlines and applies regex patterns to each line. There is no upper bound on the size of `raw_output`. A tool producing multi-gigabyte output (e.g., `nuclei` against a large target, or a network dump) would be held entirely in memory before filtering. Combined with the 15 compiled regex patterns applied per line, this creates a potential memory exhaustion vector for large outputs.

The regex patterns themselves were reviewed for ReDoS characteristics. No catastrophic backtracking patterns were identified in the 15 base patterns. The patterns use bounded quantifiers (`{16}`, `{86}`, `{33}`) or anchored groups that terminate early on non-match. The case-insensitive patterns with `\s*[=:]\s*` are not vulnerable to ReDoS because the match space is well-bounded by the surrounding literal strings.

**Recommendation**

Add a streaming mode to `filter_output()` that processes lines incrementally and short-circuits to quarantine on first match without loading the entire output. Set a maximum line length threshold (e.g., 64 KB) above which the line is truncated before pattern matching. This is a hardening measure, not a required fix at current operational scope.

---

## Mitigation Verification

### M-01: Module Path Allowlist (importlib CWE-94)

| Aspect | Status | Evidence |
|--------|--------|---------|
| Allowlist constant defined | PASS | `_ALLOWED_MODULE_PREFIXES = ("src.tool_exec.infrastructure.adapters.",)` |
| Validation executes BEFORE import_module | PASS | `_validate_module_path()` called on line 190, `import_module()` on line 191 |
| ValueError raised for non-allowed paths | PASS | Explicit message with allowed prefixes in error |
| issubclass check as secondary gate | PASS | Line 194-200 |
| resolver_class also constrained | FAIL | See FINDING-003 -- class name not validated |

**Verdict:** M-01 is correctly implemented for the module path dimension. The class name dimension was not within the original M-01 scope but represents a residual gap (FINDING-003).

---

### M-02: Cloud AI API Key Patterns (Credential Filter CWE-200)

| Pattern Category | Status | Pattern Evidence |
|-----------------|--------|-----------------|
| Anthropic `sk-ant-api` | PASS | `r"sk-ant-api[0-9]{2}-[A-Za-z0-9_-]{86}"` |
| OpenAI `sk-proj-` | PASS | `r"sk-proj-[A-Za-z0-9_-]{20,}"` |
| Google AI `AIzaSy` | PASS | `r"AIzaSy[A-Za-z0-9_-]{33}"` |
| GitHub fine-grained PAT | PASS | `r"github_pat_[A-Za-z0-9_]{22,}"` |
| Stripe `sk_live_`/`rk_live_` | PASS | `r"(sk_live_|rk_live_)[A-Za-z0-9]{24,}"` |
| Slack `xoxb-`/`xoxp-`/`xoxa-` | PASS | `r"xox[bpa]-[0-9]{10,}-[0-9]{10,}-[A-Za-z0-9]{24,}"` |
| JWT `eyJ...eyJ...` | PASS | `r"eyJ[A-Za-z0-9_-]{10,}\.eyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}"` |
| Base 15 patterns ported from bash | PASS | 8 CS + 7 CI patterns, matches original implementation |
| Stderr filtered | FAIL | See FINDING-004 -- stderr bypasses filter entirely |

**Verdict:** M-02 base patterns are correctly implemented. The significant gap is that stderr is unfiltered (FINDING-004), which can allow credential-bearing output to bypass M-02 entirely.

**Pattern coverage observation:** The patterns do not cover Azure SAS tokens (`sig=`), GCP service account JSON keys (`"private_key"`), or HashiCorp Vault tokens (`hvs.`). These are additional coverage gaps but were not part of the M-02 scope as defined.

---

### M-03: --no-filter Strict Mode Gate (CWE-284)

| Aspect | Status | Evidence |
|--------|--------|---------|
| JERRY_STRICT_MODE read from environment | PASS | `os.environ.get("JERRY_STRICT_MODE", "true")` |
| Default is strict (true) | PASS | Default value `"true"` is the secure default |
| Gate fires before any tool execution | PASS | Check at lines 96-112, before `_handle_init_engagement`, loader calls, and execution |
| ExitCode.STRICT_MODE_VIOLATION returned | PASS | Exit code 7 returned on violation |
| Warning logged in non-strict mode | PASS | `logger.warning()` with SECURITY-WARN tag |
| Truthy value handling | PARTIAL | Only `"true"` (after `.lower()`) triggers block; `"1"`, `"yes"` bypass -- see FINDING-005 |

**Verdict:** M-03 is correctly implemented for its primary use case. The partial finding (FINDING-005) is a defence-in-depth improvement, not a bypass of the core protection.

---

## ASVS Chapter Verification

**Note:** OWASP ASVS 5.0 chapters reviewed against the scope of the tool_exec bounded context. Chapters outside the scope of this bounded context (V2 Authentication, V3 Session Management) are marked N/A.

| ASVS Chapter | Status | Key Observations |
|-------------|--------|-----------------|
| V1: Architecture | PASS | Hexagonal architecture cleanly separates domain/infra. No infrastructure imports in domain layer. |
| V4: Access Control | PARTIAL | Strict mode gate (M-03) correctly implemented. Zone-based policy enforcement via SecurityPolicy. No per-user access control (not in scope for a CLI tool). |
| V5: Validation, Sanitization, Encoding | PARTIAL | Strong: engagement ID allowlist (M-05), mode validation, network_access enum validation. Gaps: evidence_dir_override (FINDING-001), is_initialized path (FINDING-002), resolver_class (FINDING-003), config_path (FINDING-006). |
| V6: Stored Cryptography | PASS | SHA-256 via hashlib for evidence integrity. No custom crypto. No weak hash algorithms (MD5, SHA-1) used. |
| V7: Error Handling and Logging | PARTIAL | Exceptions are caught and re-raised with informative messages. Security warnings logged with SECURITY-WARN tag. Gap: logger.warning for strict mode bypass may be silently dropped (FINDING-005). |
| V8: Data Protection | PARTIAL | Quarantine directory 0o700 chmod applied (M-10). Credential filter protects stdout. Gaps: stderr unfiltered (FINDING-004), tool_args in plaintext meta (FINDING-007). |
| V9: Communication | N/A | No network communication in this bounded context. Container execution delegates to docker compose. |
| V5.2: Sanitization | PASS | No HTML/JS rendering. No SQL queries. `yaml.safe_load` used exclusively -- unsafe YAML deserialization absent. |
| V5.3: Output Encoding | PASS | No template rendering or HTML output paths identified. |

---

## L2 Strategic Implications

### Security Posture Assessment

The tool_exec bounded context has a fundamentally sound security architecture. The threat model has been operationalized into concrete mitigations (M-01 through M-03, M-05, M-10) with clear traceability to DREAD scores and CWE IDs in the source. This is evidence of an intentional security-first implementation process, not security added after the fact.

The three mandated mitigations are implemented correctly. The findings in this report represent residual gaps that follow a consistent pattern: the primary trust boundary (CLI invocation by an authorized operator) is well-guarded, but secondary paths created by the same input processing logic do not uniformly inherit the same guards.

### Systemic Vulnerability Pattern

**Pattern: Partial Propagation of Validation Invariants**

FINDING-001, FINDING-002, and FINDING-006 share a root cause: a validation control is implemented in one code path (the most-travelled path) but not systematically propagated to all paths that process the same class of input. Specifically:

- Engagement ID allowlist validates in `initialize()` but not in `is_initialized()`, `evidence_dir()`, `quarantine_dir()`
- Module path allowlist validates `resolver_module` but not `resolver_class`
- Evidence dir validated as engagement sub-path for normal flow but not for `--evidence-dir` override

This pattern suggests the validation strategy is correct but the enforcement scope is narrower than the input attack surface. The recommended architectural fix is to move validation into the value objects themselves (at construction time) rather than at service method entry points. If `ToolFamilyInfo.resolver_class` were validated by `ToolFamilyInfo.__post_init__()`, the gap in FINDING-003 would not exist.

**Pattern: Unilateral stdout Filter Assumption**

FINDING-004 and FINDING-007 both follow from an implicit assumption that credentials appear only in stdout. Security tools in the exploit/post-exploitation domain (Impacket, Metasploit, pwntools) routinely write sensitive material to stderr. The credential filter architecture is correct; its application scope is incomplete.

### Comparison with Threat Model Predictions

The engagement document references DREAD-scored threats (T-01 DREAD 38, T-03 DREAD 36, T-06 DREAD 34, T-08 DREAD 28). The highest-DREAD threats (T-01, T-03, T-06) each have implemented mitigations that were verified as correct in this review. The residual findings cluster around lower-DREAD scenarios:

- FINDING-001 (CWE-22, evidence_dir) was not explicitly threat-modelled as a separate threat from T-08 (engagement ID path traversal). It shares the same CWE but is a distinct data flow.
- FINDING-004 (stderr unfiltered) was not in the T-03 threat scope, which targeted stdout credential exposure.

This indicates the threat model covered the highest-priority risks accurately and that the residual findings are incremental security hardening opportunities consistent with the engagement's security posture goals.

### Recommendations for Security Architecture Evolution

1. **Enforce validation at value object construction.** Move all input validation into `__post_init__()` of frozen dataclasses (`ToolFamilyInfo`, `ToolResolutionEntry`). This removes the partial-propagation pattern entirely -- objects cannot be constructed with invalid data.

2. **Introduce an `EngagementId` value object.** Replace `engagement_id: str` parameters with a typed value object that enforces the allowlist at construction. All three instances of unvalidated engagement ID use (FINDING-002) would be eliminated structurally.

3. **Extend credential filter to a dual-stream pipeline.** Redesign `ExecutionResult` and `ContainerExecutionResult` to process both streams through the filter. The filter architecture (FINDING-004) is not a fundamental limitation -- it is a scope gap.

4. **Harden `tool_families.yaml` as a trust boundary.** The YAML file is the primary attack surface for M-01. Consider adding file integrity verification (SHA-256 of the file checked against a stored value) as a startup gate, so that unauthorized modification of `tool_families.yaml` is detected before any dynamic import occurs.

---

## Scope and Methodology

### Files Reviewed

| File | Lines | Primary Review Focus |
|------|-------|----------------------|
| `src/tool_exec/domain/ports/tool_family_resolver_port.py` | 110 | Interface contract, type safety |
| `src/tool_exec/domain/services/family_router.py` | 136 | Dispatch logic, error message info exposure |
| `src/tool_exec/domain/services/mode_resolver.py` | 90 | Mode validation, env var handling |
| `src/tool_exec/domain/services/credential_filter.py` | 248 | Pattern completeness, filter scope, ReDoS |
| `src/tool_exec/domain/services/evidence_hasher.py` | 76 | Cryptographic soundness |
| `src/tool_exec/domain/services/engagement_initializer.py` | 173 | CWE-22, ID validation, directory permissions |
| `src/tool_exec/domain/value_objects/security_policy.py` | 59 | Invariant validation, network_access enum |
| `src/tool_exec/domain/value_objects/exit_codes.py` | 53 | Exit code semantics |
| `src/tool_exec/infrastructure/adapters/rainbow_tool_resolver.py` | 243 | YAML loading, zone policy, CWE-502 |
| `src/tool_exec/infrastructure/adapters/local_executor.py` | 131 | CWE-78, subprocess.run safety |
| `src/tool_exec/infrastructure/adapters/container_executor.py` | 227 | CWE-78, docker compose injection, filter scope |
| `src/tool_exec/infrastructure/registry/family_registry_loader.py` | 203 | CWE-94, importlib, M-01 |
| `src/interface/cli/tool_exec_commands.py` | 477 | Full pipeline wiring, M-03, CWE-22 |
| `tool_families.yaml` | 30 | Registry content, trust boundary |
| `src/tool_exec/domain/value_objects/tool_resolution_entry.py` | 64 | Validation coverage |
| `src/tool_exec/domain/value_objects/tool_family_info.py` | 44 | Field types, validation absence |

### CWE Checklist Results

| CWE | Check | Result |
|-----|-------|--------|
| CWE-78: OS Command Injection | `subprocess.run` called with `shell=False` (default), cmd always a list, no string concatenation | PASS -- no shell injection |
| CWE-22: Path Traversal | Engagement ID allowlist (M-05), evidence_dir override | PARTIAL -- see FINDING-001, FINDING-002, FINDING-006 |
| CWE-502: Deserialization | All YAML loading uses `yaml.safe_load` exclusively | PASS |
| CWE-94: Code Injection | Module path allowlist (M-01), resolver_class unvalidated | PARTIAL -- see FINDING-003 |
| CWE-200: Information Exposure | Stderr unfiltered, tool_args in plaintext meta | PARTIAL -- see FINDING-004, FINDING-007 |
| CWE-798: Hardcoded Credentials | Full codebase search via Grep | PASS -- no hardcoded credentials found |
| CWE-400: Resource Consumption | No output size limit before filter scan | LOW -- see FINDING-008 |
| CWE-352: CSRF | Not applicable (CLI tool, no web surface) | N/A |
| CWE-287: Authentication | Strict mode gate (M-03) for policy enforcement | PASS |
| CWE-862: Missing Authorization | Zone-based policy checked before execution | PASS |

### Methodology Notes

- Data flow tracing performed from CLI argument intake through to subprocess invocation and filesystem writes for all user-controlled inputs.
- `grep -r 'shell=True'` and `grep -r 'yaml.load\b'` confirmed zero occurrences across the entire `src/` tree.
- No hardcoded credential strings, API keys, or passwords were identified in source code (search terms: `sk-`, `password`, `api_key`, `secret`, `token` as literals).
- ReDoS analysis performed on all 15 regex patterns in `credential_filter.py`; no catastrophic backtracking patterns identified.
- `resolver_class` validation gap (FINDING-003) identified through forward data flow trace from `tool_families.yaml` -> `_parse_registry()` -> `_load_resolver()` -> `getattr()`.
- Stderr filter gap (FINDING-004) identified through backward trace from `print(result["stderr"], file=sys.stderr)` line 235 to its unfiltered origin.
