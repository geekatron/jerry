# eng-backend R4 Fix — W12-PHASE2-R4-FIX

| Field | Value |
|-------|-------|
| Engagement ID | W12-PHASE2-R4-FIX |
| Criticality | C4 |
| Findings Addressed | 1 Critical + 5 Major |
| Validation | pytest 299/299 PASS |

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0 Executive Summary](#l0-executive-summary) | What was fixed and key security impact |
| [L1 Technical Detail](#l1-technical-detail) | Per-finding implementation record |
| [L2 Strategic Implications](#l2-strategic-implications) | Security posture impact |
| [Validation Results](#validation-results) | Test gate outcomes |
| [OWASP Verification](#owasp-verification) | Self-verification checklist |

---

## L0 Executive Summary

Six findings from the R4 tournament were addressed. One Critical (CC-001-R4) removed an H-07 architectural violation where a domain service directly accessed `os.environ`. Five Majors addressed a path traversal gap (SR-003-R4), a dead --zone flag (FM-033), an exit code documentation discrepancy (CV-007), a factory docstring inaccuracy (DA-R4-001), and a meta filename collision vector (PM-004-R4).

No regressions. 299/299 unit tests pass after changes across three source files and one new test file.

**OWASP categories addressed:**
- A07:2021 Auth Failures — CC-001-R4 domain isolation removes env-read side-effect
- A03:2021 Injection (CWE-22) — SR-003-R4 path traversal gate enforced on audit path
- A01:2021 Broken Access Control — FM-033 zone override now enforced on security policy
- A09:2021 Security Logging Failures — PM-004-R4 compound hash prevents meta file collision

---

## L1 Technical Detail

### CC-001-R4 (CRITICAL) — H-07: domain service reads os.environ

**Finding:** `EngagementInitializer.initialize()` contained `os.environ.get("USER") or os.environ.get("USERNAME") or "unknown"` inside the domain service. Domain services must not access infrastructure concerns (H-07). NIST SSDF PW.5.

**Fix — `src/tool_exec/domain/services/engagement_initializer.py`:**

Added `created_by: str = "unknown"` parameter to `initialize()`. The domain service now stores the explicitly passed value; it no longer reads `os.environ`. Default `"unknown"` preserves backward compatibility for callers that do not need attribution. Removed the inline `os.environ.get(...)` call. Updated all docstring references to document the new parameter contract.

**Fix — `src/interface/cli/tool_exec_commands.py` (`_handle_init_engagement`):**

Added `created_by: str = os.environ.get("USER") or os.environ.get("USERNAME") or "unknown"` at the top of `_handle_init_engagement`. This is the correct boundary for env var access (CLI adapter layer). Passes the resolved string to `engagement_init.initialize(engagement_id, created_by=created_by)`.

**Tests added (`tests/unit/tool_exec/test_r4_fixes.py`):**
- `test_created_by_parameter_written_to_meta` — parameter stored in JSON
- `test_default_created_by_is_unknown` — default with env vars unset
- `test_explicit_created_by_overrides_env` — domain ignores env when param supplied
- `test_cli_handler_passes_env_user_to_initialize` — CLI boundary reads USER correctly

---

### SR-003-R4 (MAJOR) — path traversal in `_write_no_filter_audit`

**Finding:** `_write_no_filter_audit()` built the engagement evidence path manually:
```python
audit_dir = project_root / "work" / "engagements" / engagement_id / "evidence"
```
This bypassed `_validate_id()` inside `EngagementInitializer.evidence_dir()`. A malformed `engagement_id` (e.g., `../escape`) would write the audit file outside the engagement tree (CWE-22).

**Fix — `src/interface/cli/tool_exec_commands.py`:**

1. `_write_no_filter_audit()` now accepts an optional `engagement_init: EngagementInitializer | None = None` parameter.
2. When `engagement_id` is set and `engagement_init` is not None, the audit directory is obtained via `engagement_init.evidence_dir(engagement_id)` — which calls `_validate_id()` and raises `ValueError` for malformed IDs (caught by the best-effort `except Exception` block, preventing any file write at the traversal target).
3. The factory construction was moved before the `no_filter` block so `engagement_init` is available when `_write_no_filter_audit` is called.
4. The call site updated to pass `engagement_init=engagement_init`.
5. Docstring updated with SR-003-R4 rationale and CWE-22 annotation.

**Tests added:**
- `test_audit_written_to_evidence_dir_when_engagement_active` — audit lands in `evidence_dir()`
- `test_audit_fallback_when_no_engagement` — global fallback path unchanged
- `test_audit_path_does_not_bypass_validate_id` — malformed ID: no file escapes to traversal path

---

### FM-033 (MAJOR) — `--zone` flag never consumed

**Finding:** `--zone` was parsed by argparse but `handle_tool_exec()` never called `getattr(args, "zone", None)`. The security zone override had no effect on execution.

**Fix — `src/interface/cli/tool_exec_commands.py`:**

1. Added `zone_override: str | None = getattr(args, "zone", None)` to the args extraction block.
2. Added `import dataclasses` at the top of the file.
3. After `policy = resolver.security_policy(tool_command)`, inserted a zone override block: when `zone_override` is not None, `dataclasses.replace(policy, **_ZONE_OVERRIDE_FIELDS[zone_override])` produces a new frozen `SecurityPolicy` with the zone-appropriate values:
   - Zone 1: `requires_engagement=False, requires_approval=False, container_required=False, network_access="none", family_zone_label="Zone 1"`
   - Zone 2: `requires_engagement=True, requires_approval=False, container_required=False, network_access="restricted", family_zone_label="Zone 2"`
   - Zone 3: `requires_engagement=True, requires_approval=True, container_required=True, network_access="full", family_zone_label="Zone 3"`
4. `credential_filter_enabled` is intentionally not overridden — it is a family-level configuration, not a zone classification.
5. Added `logger.info(...)` trace log when override is applied.

**Tests added:**
- `test_zone_override_zone1_produces_no_engagement_policy`
- `test_zone_override_zone2_requires_engagement`
- `test_zone_override_zone3_full_constraints`
- `test_no_zone_override_leaves_policy_unchanged`

---

### CV-007 (MAJOR) — exit code documentation discrepancy

**Finding:** Tournament cited that `--no-filter` + strict returns exit 9 (`STRICT_MODE_VIOLATION`) but a UC acceptance criterion implied exit 6 (`MODE_UNSET`).

**Resolution:** No code change required. The implementation is correct. `ExitCode.STRICT_MODE_VIOLATION` (9) is semantically accurate for a strict mode policy rejection; `MODE_UNSET` (6) is reserved for the Zone 2/3 explicit-mode gate (UC-001 Extension 7b). UC-TOOLEXEC-001 AF-05 and UC-TOOLEXEC-005 AF-02 already document this decision from a prior R4 pass (eng-backend-r4-priority-fixes.md CV-007 section). The UC documents are already aligned with the implementation.

**Tests added (regression):**
- `test_strict_mode_violation_exit_code_is_9`
- `test_mode_unset_exit_code_is_6`
- `test_strict_mode_violation_and_mode_unset_are_distinct`

---

### DA-R4-001 (MAJOR) — factory docstring claims "single composition root"

**Finding:** `create_tool_exec_handler()` docstring comment claimed "The factory is the single composition root" (from CC-004 annotation), but PM-004-R3 introduced an invocation-scoped filter path where `local_executor` and `container_executor` are rebound to new instances inline. This two-path topology was undocumented, misleading future maintainers.

**Fix — `src/interface/cli/tool_exec_commands.py`:**

Updated the `create_tool_exec_handler()` docstring with a `DA-R4-001 (two-path topology)` section explaining:
- The factory produces base service instances for most invocations (path 1).
- When `SecurityPolicy.credential_filter_patterns` is non-empty (path 2), the CLI handler creates an invocation-scoped `CredentialFilterService` via `with_extra_patterns()` and rebinds the executor local variables to new instances holding this scoped filter.
- The factory's shared instances are NOT mutated.
- The Returns section updated to note the `credential_filter` field "may be superseded by an invocation-scoped instance" with a reference to DA-R4-001.

**Tests added:**
- `test_factory_docstring_mentions_two_path_topology` — docstring contains "DA-R4-001" and "two-path"
- `test_factory_returns_expected_keys` — factory dict structure unchanged

---

### PM-004-R4 (MAJOR) — meta filename uses stdout hash only

**Finding:** `_quarantine_output()` used `sha256(raw_stdout)` as the meta file stem. When a tool writes credentials only to stderr (stdout is empty), every such detection produces `sha256("")` as the stem — a constant. Successive stderr-only detections overwrite each other's meta file.

**Fix — `src/interface/cli/tool_exec_commands.py`:**

1. After computing `sha256_stdout` and `sha256_stderr`, added:
   ```python
   sha256_compound = hasher.hash_string(raw_stdout + raw_stderr)
   ```
2. Changed `meta_file = quarantine_dir / f"{sha256_stdout}.meta.json"` to `f"{sha256_compound}.meta.json"`.
3. Added `"sha256_compound": sha256_compound` to the meta JSON dict for traceability.
4. Updated inline comment to explain PM-004-R4 rationale (sha256(stdout + stderr) is distinct per (stdout, stderr) pair).

The stdout and stderr raw files retain their individual hashes as stems (`{sha256_stdout}.stdout.raw`, `{sha256_stderr}.stderr.raw`) — these are unchanged and still provide per-stream deduplication.

**Tests added:**
- `test_meta_filename_uses_compound_hash` — stem equals sha256(stdout + stderr)
- `test_stderr_only_detections_get_distinct_meta_files` — two stderr-only events produce 2 distinct meta files
- `test_meta_json_contains_sha256_compound_field` — meta JSON has sha256_compound key

---

## L2 Strategic Implications

**H-07 layer isolation (CC-001-R4):** Removing environment variable reads from the domain service hardens the hexagonal architecture boundary. The domain layer is now fully testable without OS environment setup and is portable across execution contexts (CLI, server mode, test harness) without behavioral variance.

**Path traversal defence-in-depth (SR-003-R4):** The `_validate_id()` gate was already enforced on all five public methods of `EngagementInitializer` (initialize, is_initialized, evidence_dir, quarantine_dir, and global_audit_dir). SR-003-R4 closes the remaining gap where the CLI built an engagement path manually. All engagement-scoped filesystem operations now route through the service's validated path methods (CWE-22, OWASP A03:2021).

**Zone override operationality (FM-033):** The `--zone` flag is now functional. This enables operators to downgrade or upgrade the security constraints for a resolved tool when the tool resolution table's zone classification does not match the engagement context (e.g., running a Zone 3 tool under a Zone 2 engagement for a limited-scope test). The override is logged at INFO level for audit purposes.

**Compound hash integrity (PM-004-R4):** Stderr-only credential detections now produce stable, unique meta filenames. This matters most in CI/CD pipelines where a tool streams secrets to stderr (common for environment-variable leaks in build logs). Each detection event now produces a durable, non-colliding forensic record.

---

## Validation Results

| Gate | Result |
|------|--------|
| `uv run pytest tests/unit/tool_exec/ -q` | 299/299 PASS |
| New test file | `tests/unit/tool_exec/test_r4_fixes.py` (33 tests) |
| Regressions | 0 |

---

## OWASP Verification

| OWASP Category | Finding | Mitigation Applied |
|----------------|---------|-------------------|
| A01:2021 Broken Access Control | FM-033 zone flag dead | `--zone` now enforces security policy constraints |
| A03:2021 Injection (CWE-22) | SR-003-R4 manual path build | `evidence_dir()` enforces `_validate_id()` allowlist |
| A05:2021 Security Misconfiguration | CC-001-R4 domain reads env | Domain service isolated from OS environment |
| A07:2021 Authentication Failures | CV-007 exit code | Exit 9 correctly signals strict mode policy violation |
| A09:2021 Logging Failures | PM-004-R4 meta collision | Compound hash prevents overwrite of stderr-only detections |
