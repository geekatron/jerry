# Security Remediation Summary -- W12-PHASE2

## tool_exec Bounded Context: Four High/Medium Security Findings

**Agent:** eng-backend
**Engagement ID:** W12-PHASE2
**Criticality:** C3
**Remediation Date:** 2026-03-17
**Input:** `skills/eng-team/output/W12-PHASE2/eng-security-phase2-review.md`
**OWASP Alignment:** A01 (Broken Access Control), A02 (Cryptographic Failures), A03 (Injection), A08 (Data Integrity Failures)
**SSDF Practice:** PW.5 (Secure coding), PW.6 (Secure defaults)

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0 Executive Summary](#l0-executive-summary) | Status, findings fixed, test results |
| [L1 Technical Detail](#l1-technical-detail) | Per-finding implementation description, files changed |
| [L2 Strategic Implications](#l2-strategic-implications) | Security posture impact, residual risk |
| [OWASP Self-Verification](#owasp-self-verification) | Post-remediation OWASP Top 10 checklist |

---

## L0 Executive Summary

All four mandated findings from the eng-security Phase 2 review are remediated. The full test suite (211 tests) passes with zero regressions.

| Finding | Severity | CWE | Status | Tests Added |
|---------|----------|-----|--------|-------------|
| FINDING-001: --evidence-dir path traversal | High | CWE-22 | FIXED | 9 |
| FINDING-002: Engagement ID validation gap | Medium | CWE-22 | FIXED | 10 |
| FINDING-003: resolver_class name unconstrained | Medium | CWE-94 | FIXED | 14 |
| FINDING-004: Credential filter skips stderr | Medium | CWE-200 | FIXED | 10 |

**Total new security tests:** 43 (across 4 test classes in 4 files + 1 new file).

**Test run result:** 211 passed, 0 failed, 0 errors.

### Key Security Controls Applied

- **CWE-22 (Path Traversal):** Two independent path containment controls implemented. `_validate_evidence_dir()` applies `.resolve()` + `relative_to()` containment at the CLI layer; `_validate_id()` is now enforced at every trust boundary in `EngagementInitializer`.
- **CWE-94 (Code Injection via getattr):** `_CLASS_NAME_PATTERN` regex (`^[A-Z][a-zA-Z0-9]{1,63}$`) constrains resolver class attribute access before `getattr()` is called. Dunder attributes, lowercase module imports, and dotted paths are all excluded.
- **CWE-200 (Information Exposure via stderr):** Credential filter now applied to both `stdout` and `stderr`. If either stream triggers detection, both streams are quarantined and exit code 4 is returned.

---

## L1 Technical Detail

### FINDING-001: --evidence-dir Path Traversal (High, CWE-22)

**Root cause:** `_persist_evidence()` accepted the `--evidence-dir` CLI argument as a raw `Path` string and called `Path(evidence_dir_override).mkdir(parents=True, exist_ok=True)` without canonicalization or containment check. `parents=True` created the full traversed path including any `../` segments.

**Fix:**

1. Added `_validate_evidence_dir(evidence_dir_override: str, project_root: Path) -> Path` to `src/interface/cli/tool_exec_commands.py`. This function:
   - Calls `Path(evidence_dir_override).resolve()` to canonicalize symlinks and relative segments.
   - Calls `resolved.relative_to(project_root.resolve())` to assert project-root containment.
   - Raises `ValueError` with a message naming both the rejected path and the project root boundary if containment fails.

2. Added `project_root: Path | None = None` parameter to `_persist_evidence()`. When `evidence_dir_override` is supplied, `_validate_evidence_dir()` is called before `mkdir()`. The `project_root` is passed in from `handle_tool_exec()` (which already had `project_root` in scope).

3. The `_persist_evidence()` call in `handle_tool_exec()` is wrapped in a `try/except ValueError` block that returns `ExitCode.ENGAGEMENT_NOT_INIT` on rejection, consistent with the existing engagement error path.

**Files changed:**
- `src/interface/cli/tool_exec_commands.py`: `_validate_evidence_dir()` added (new function), `_persist_evidence()` signature updated, call site updated with `project_root=` kwarg and error handling.

**Tests added:** `tests/unit/tool_exec/test_tool_exec_commands_security.py` -- `TestValidateEvidenceDirFinding001` (9 tests covering in-tree acceptance, out-of-tree rejection by relative traversal, absolute out-of-tree path, sibling, parent, dotdot-in-tree, error message content, resolved return type).

---

### FINDING-002: Engagement ID Validation Gap (Medium, CWE-22)

**Root cause:** `EngagementInitializer._validate_id()` (M-05 allowlist) was called only from `initialize()`. The `is_initialized()`, `evidence_dir()`, and `quarantine_dir()` methods composed filesystem paths directly from the raw `engagement_id` string parameter. A caller passing `"../../etc"` to `is_initialized()` would silently traverse the filesystem, and passing it to `evidence_dir()` or `quarantine_dir()` would return a traversed path used for writes.

**Fix:** Added `self._validate_id(engagement_id)` as the first statement in each of the three unprotected methods:

```python
def is_initialized(self, engagement_id: str) -> bool:
    self._validate_id(engagement_id)  # FINDING-002 fix
    engagement_dir = self._base_dir / engagement_id
    ...

def evidence_dir(self, engagement_id: str) -> Path:
    self._validate_id(engagement_id)  # FINDING-002 fix
    return self._base_dir / engagement_id / self.EVIDENCE_DIR

def quarantine_dir(self, engagement_id: str) -> Path:
    self._validate_id(engagement_id)  # FINDING-002 fix
    return self._base_dir / engagement_id / self.QUARANTINE_DIR
```

Each method's docstring is updated to document the `ValueError` raise condition.

**Files changed:**
- `src/tool_exec/domain/services/engagement_initializer.py`: Three methods updated.

**Tests added:** `tests/unit/tool_exec/test_engagement_initializer.py` -- `TestEngagementInitializerFinding002` (10 tests: path-traversal and empty-ID rejection for all three methods; valid-ID acceptance regression guards for all three methods).

---

### FINDING-003: resolver_class Name Unconstrained (Medium, CWE-94)

**Root cause:** `FamilyRegistryLoader._load_resolver()` called `self._validate_module_path()` (M-01 allowlist) on the module path before `importlib.import_module()`, but passed `family_info.resolver_class` directly to `getattr(module, ...)` without any validation. Any string value from `tool_families.yaml` could be used as an attribute name, including `__builtins__`, `subprocess`, `os`, or any other module-level attribute on the allowed module.

**Fix:**

1. Added `import re` to the module imports.

2. Added `_CLASS_NAME_PATTERN: re.Pattern[str] = re.compile(r"^[A-Z][a-zA-Z0-9]{1,63}$")` as a module-level constant. This pattern:
   - Requires the first character to be an uppercase ASCII letter (excludes dunder names, lowercase module imports, digits).
   - Allows 1-63 additional alphanumeric characters (total 2-64 chars).
   - Excludes underscores, dots, spaces, and all non-alphanumeric characters.

3. Added `_validate_class_name(self, class_name: str) -> None` method that matches against `_CLASS_NAME_PATTERN` and raises `ValueError` on mismatch.

4. Called `self._validate_class_name(family_info.resolver_class)` in `_load_resolver()` after `_validate_module_path()` and BEFORE `importlib.import_module()`. The class name is validated before the module is even imported, so no attribute access can occur with an invalid name.

**Files changed:**
- `src/tool_exec/infrastructure/registry/family_registry_loader.py`: `import re` added; `_CLASS_NAME_PATTERN` constant added; `_validate_class_name()` method added; `_load_resolver()` updated with validation call.

**Tests added:** `tests/unit/tool_exec/test_family_registry_loader.py` -- `TestFamilyRegistryLoaderClassNameValidation` (14 tests: valid CamelCase acceptance, minimum/maximum length boundaries, dunder rejection, lowercase rejection, module-import rejection, dotted name rejection, empty/single-char rejection, 65-char rejection, underscore rejection, constant verification, and two end-to-end `load()` rejection tests).

---

### FINDING-004: Credential Filter Skips stderr (Medium, CWE-200)

**Root cause:** Both `LocalExecutor.execute()` and `ContainerExecutor.execute()` called `self._credential_filter.filter_output(raw_stdout)` and returned the raw, unfiltered `result.stderr` in the `ExecutionResult`/`ContainerExecutionResult`. Security tools in the exploit and post-exploitation domain (Metasploit, Impacket, pwntools) routinely write credentials, session tokens, NTLM hashes, and key material to stderr. This allowed credential-bearing stderr to bypass the L1 regex filter, the quarantine pipeline, and the `CREDENTIAL_DETECTED` exit code 4 signal.

**Fix:**

Both executors now:
1. Capture `raw_stderr = result.stderr` alongside `raw_stdout`.
2. Apply the filter to both streams: `stdout_filter_result` and `stderr_filter_result`.
3. Compute `detected = stdout_filter_result.detected or stderr_filter_result.detected`.
4. Return the filtered output for both streams.
5. Set exit code 4 if detection triggers on either stream.

Both `ExecutionResult` and `ContainerExecutionResult` dataclasses gain a `raw_stderr: str = ""` field, mirroring the existing `raw_stdout` field. This field carries the original unfiltered stderr content for downstream quarantine use.

Error path returns (FileNotFoundError, TimeoutExpired) are also updated to set `raw_stderr=""` explicitly.

The `filter_result` field retains the stdout filter result (for line-number reporting in quarantine metadata). A future improvement would track stderr match info separately.

**Files changed:**
- `src/tool_exec/infrastructure/adapters/local_executor.py`: `ExecutionResult` dataclass updated (`raw_stderr` added); `execute()` method updated (dual-stream filtering).
- `src/tool_exec/infrastructure/adapters/container_executor.py`: `ContainerExecutionResult` dataclass updated (`raw_stderr` added); `execute()` method updated (dual-stream filtering, error paths updated).

**Tests added:**
- `tests/unit/tool_exec/test_local_executor.py` -- `TestLocalExecutorFinding004` (6 tests).
- `tests/unit/tool_exec/test_container_executor.py` -- `TestContainerExecutorFinding004` (4 tests).

Coverage: credential-in-stderr detection, stderr redaction, stdout detection regression guard, clean stderr passthrough, `raw_stderr` preservation, `--no-filter` bypass of stderr filtering.

---

## L2 Strategic Implications

### Security Posture Impact

The four remediations close the "partial propagation of validation invariants" pattern identified in the eng-security review's L2 analysis. Before this work:
- One method in `EngagementInitializer` enforced the engagement ID allowlist; three did not.
- One dimension of the M-01 allowlist (module path) was enforced; the other (class name) was not.
- One output stream (stdout) was credential-filtered; stderr was not.
- One code path (normal engagement directory) validated the evidence dir; the CLI override did not.

After this work, each of these validation controls is uniformly applied at every trust boundary where the corresponding input can arrive.

### Alignment with eng-architect Recommendation

The eng-security review's strategic recommendation was to move validation into value object construction (`__post_init__()` of frozen dataclasses). This sprint implements the defence-in-depth variant: validation enforced at every service method boundary. The value object approach (an `EngagementId` type that validates at construction) remains the preferred long-term architecture but requires a larger refactor touching all callers. The service-method approach applied here provides equivalent protection with minimal blast radius.

### Residual Risk (Not in Scope for This Sprint)

The following findings from eng-security are informational or Low severity and were not in scope for this remediation sprint:

| Finding | Severity | Note |
|---------|----------|------|
| FINDING-005: JERRY_STRICT_MODE truthy value handling | Low | "1", "yes" bypass strict mode; "true" is the documented value. Informational hardening. |
| FINDING-006: YAML config_path not validated | Low | Read-only operation; `yaml.safe_load` parse failure on invalid content is the current backstop. |
| FINDING-007: tool_args in plaintext meta files | Informational | Argument redaction would require pattern extension. No secrets transport in default workflows. |
| FINDING-008: No output size limit before filter scan | Informational | Memory exhaustion vector for very large tool outputs; no ReDoS patterns identified in current patterns. |

### Dependency Risk Observation

No new dependencies were introduced. All fixes use the Python standard library (`re`, `pathlib.Path.resolve()`). The `_CLASS_NAME_PATTERN` regex uses only anchors and character classes -- no catastrophic backtracking risk.

---

## OWASP Self-Verification

Post-remediation OWASP Top 10 verification for the four changed files:

| OWASP Category | Finding Addressed | Post-Fix Status |
|----------------|-------------------|-----------------|
| A01:2021 Broken Access Control | FINDING-001 (evidence dir redirect) | PASS -- project-root containment enforced |
| A02:2021 Cryptographic Failures | -- | PASS -- no changes to crypto paths |
| A03:2021 Injection | FINDING-002 (engagement ID path composition), FINDING-003 (getattr attribute injection) | PASS -- allowlist enforced at all trust boundaries |
| A04:2021 Insecure Design | -- | PASS -- changes align with engagement isolation model |
| A05:2021 Security Misconfiguration | -- | PASS -- no configuration changes |
| A06:2021 Vulnerable Components | -- | PASS -- no new dependencies |
| A07:2021 Auth Failures | -- | PASS -- strict mode gate (M-03) unchanged |
| A08:2021 Data Integrity Failures | FINDING-003 (resolver_class getattr constraint) | PASS -- class name validated before dynamic attribute access |
| A09:2021 Logging Failures | FINDING-004 (credential-bearing stderr logged to terminal) | PASS -- stderr now filtered before return to caller |
| A10:2021 SSRF | -- | PASS -- no network communication in this bounded context |
