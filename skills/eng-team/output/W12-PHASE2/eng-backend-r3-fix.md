# eng-backend R3 Fix Summary

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0 Executive Summary](#l0-executive-summary) | What was fixed, security controls applied |
| [L1 Technical Detail](#l1-technical-detail) | Per-finding implementation detail |
| [L2 Strategic Implications](#l2-strategic-implications) | Security posture assessment |

---

## L0 Executive Summary

**Engagement ID:** W12-PHASE2-R3-FIX
**Criticality:** C4
**Outcome:** 3 Critical/Major consensus findings from the R3 tournament resolved. 280 tests pass (264 pre-existing + 16 new). Zero regressions.

### Fixes Applied

| Finding ID | Severity | Description | Status |
|------------|----------|-------------|--------|
| FIX-R3-1 (PM-001-R3) | Critical | `strict_mode` not threaded to executors -- executor always used hard-coded `True` default | FIXED |
| FIX-R3-2 (PM-002-R3/RT-001/IN-021) | Critical | `_write_approval_audit()` swallowed failures silently -- Zone 3 could execute without audit record | FIXED |
| FIX-R3-3 (SR-002/CC-005/DA-R3-001/IN-022/PM-005) | Major consensus | `_handle_health_check()` and `_handle_init_engagement()` bypassed factory; unused `mode_resolver` in factory | FIXED |

### OWASP Categories Addressed

| Category | Finding Addressed |
|----------|------------------|
| A01:2021 Broken Access Control | FIX-R3-2: Zone 3 execution without audit record |
| A02:2021 Cryptographic Failures | FIX-R3-1: Credential filter strict_mode inconsistency |
| A05:2021 Security Misconfiguration | FIX-R3-3: Inline construction bypassing factory wiring |
| A09:2021 Logging Failures | FIX-R3-2: Audit write failure swallowed |

---

## L1 Technical Detail

### FIX-R3-1: strict_mode not threaded to executors

**Root cause:** `handle_tool_exec()` resolved `strict_mode` from `JERRY_STRICT_MODE` only inside `if no_filter:` and stored it in a local `strict` variable. The executors were called without it, so `LocalExecutor.execute()` and `ContainerExecutor.execute()` always called `filter_output(strict_mode=True)` using the hard-coded default. When `JERRY_STRICT_MODE=false` and `--no-filter` were used together, the CLI guard would pass (because it saw `strict=False`) but the executor would still raise `RuntimeError` at the `filter_output` call.

**Files changed:**

- `src/interface/cli/tool_exec_commands.py` -- moved `strict_mode_env` and `strict` resolution outside `if no_filter:` (lines 237-238); added `strict_mode=strict` to `_execute_local()` and `_execute_container()` call sites; added `strict_mode: bool = True` parameter to both helper signatures with docstring annotation.
- `src/tool_exec/infrastructure/adapters/local_executor.py` -- added `strict_mode: bool = True` to `execute()` signature; threaded to `filter_output(strict_mode=strict_mode)` for both stdout and stderr filter calls.
- `src/tool_exec/infrastructure/adapters/container_executor.py` -- same change as local_executor.

**Security invariant preserved:** `strict_mode` defaults to `True` in both executor signatures. Callers that bypass the CLI and invoke executors directly (e.g., unit tests) remain protected by the safe default. Only the CLI handler can legitimately pass `strict_mode=False` (after validating `JERRY_STRICT_MODE`).

### FIX-R3-2: Audit write failure silently swallowed

**Root cause:** `_write_approval_audit()` returned `None` and the `except Exception:` block only called `logger.exception(...)`. If the audit file could not be written (permissions error, full disk), Zone 3 execution would proceed with no tamper-evident record, violating OWASP A09:2021 Security Logging Failures.

**Files changed:**

- `src/interface/cli/tool_exec_commands.py`:
  - Changed `_write_approval_audit()` return type from `None` to `bool` (`True` = success, `False` = failure).
  - Added `print(..., file=sys.stderr)` in the `except` block so failures are always visible in the operator console even when log output is suppressed.
  - In `_prompt_zone3_approval()`, captured the return value of `_write_approval_audit()` into `audit_ok`. Added guard: `if approved and not audit_ok: return False` with a descriptive stderr warning.
  - Denial events remain best-effort: a failed audit write on a denial does not block the denial (denying is already safe).

**Security invariant:** Zone 3 execution requires BOTH operator approval AND a successfully written audit record. Approval without an audit record is treated equivalently to a denial.

### FIX-R3-3: Health check and init-engagement bypass factory

**Root cause (three sub-issues):**

1. `_handle_health_check()` constructed its own `ContainerExecutor(credential_filter=CredentialFilterService(), ...)` inline, bypassing the factory-wired instance. This violates H-07(c) (composition root exclusivity) and means any family-extended credential filter patterns would not be present during health checks.

2. `_handle_init_engagement()` constructed its own `EngagementInitializer(base_dir=...)` inline, bypassing the factory. Same violation.

3. `create_tool_exec_handler()` returned a `mode_resolver` key with a default-prefix `ModeResolverService()`. `handle_tool_exec()` constructed its own with a family-specific prefix immediately after. The factory instance was never used and its presence invited callers to use the wrong prefix. (DA-R3-002)

**Files changed:**

- `src/interface/cli/tool_exec_commands.py`:
  - Moved `services = create_tool_exec_handler(project_root)` above the `if init_engagement:` branch so factory services are available to all sub-handlers.
  - Changed `_handle_init_engagement(engagement_id, project_root)` signature to `_handle_init_engagement(engagement_id, engagement_init)`. Removed inline `EngagementInitializer` construction.
  - Changed `_handle_health_check(resolution, project_root)` signature to `_handle_health_check(resolution, container_executor, project_root)`. Removed inline `ContainerExecutor` and `CredentialFilterService` construction. Added `project_root` to build the absolute compose path (health_check passes it to `docker compose -f`).
  - Removed `mode_resolver` key from `create_tool_exec_handler()` return dict and updated docstring. (DA-R3-002)
  - Updated `test_c4_remediation.py::TestFix9CompositionRoot::test_factory_returns_all_services` to assert `"mode_resolver" not in services`.

### New tests: `tests/unit/tool_exec/test_r3_fixes.py`

16 new tests covering all three findings:

| Class | Tests | Finding |
|-------|-------|---------|
| `TestR3Fix1StrictModeThreaded` | 5 | FIX-R3-1 |
| `TestR3Fix2AuditWriteFailure` | 5 | FIX-R3-2 |
| `TestR3Fix3FactoryCompliance` | 6 | FIX-R3-3 |

**Test run result:** 280 passed, 0 failed, 0 errors.

---

## L2 Strategic Implications

### Backend Security Posture

All three R3 findings were defence-in-depth failures -- the outer CLI guard was present but the inner domain/infrastructure layer did not honour the same constraint. This is the classic "defence-in-depth gap": security decisions made at one layer must propagate through all downstream layers that act on the same trust boundary.

**FIX-R3-1** closes the gap between the CLI-layer strict_mode resolution and the domain-layer `filter_output()` enforcement. The fix pattern (resolve once at composition root, inject as a parameter, never re-read env in domain layer) is the correct hexagonal architecture approach and aligns with PM-004-R2 and H-07.

**FIX-R3-2** converts an advisory audit into a mandatory pre-condition for Zone 3 execution. This is a security regression prevention measure: if a future change weakens the audit directory permissions or introduces a race condition, execution is blocked rather than proceeding silently. OWASP A09:2021 Security Logging Failures is fully addressed.

**FIX-R3-3** enforces the single composition root invariant (H-07(c)) for all sub-handlers. Any future family-specific credential filter extension applied by the main pipeline will now also apply during health checks. The removal of `mode_resolver` from the factory eliminates a latent confusion source that could cause operators to use the wrong env var prefix for mode resolution.

### Scalability Considerations

The `strict_mode` parameter threading pattern is O(1) for each new executor type added. Any future executor (e.g., SSH executor, API executor) that wraps `filter_output()` must follow the same pattern: accept `strict_mode` as a constructor or method parameter and thread it to the filter call. This should be codified in `eng-backend` implementation standards for future executor implementations.

### Remaining Risk

- The `_write_approval_audit()` fallback path (global `.zone3-audit/` dir) still has a race condition when multiple concurrent Zone 3 approval attempts write to the same timestamp-based filename. This is a pre-existing condition not introduced by these fixes; it is outside the scope of R3 findings but should be tracked for a future R4 finding.
- The audit directory is created with `os.chmod(dir, 0o700)` after `mkdir`, but on systems with restrictive umasks the `mkdir` itself may fail before chmod runs. This edge case also pre-exists and is outside R3 scope.

---

*Agent: eng-backend*
*Engagement: W12-PHASE2-R3-FIX*
*Date: 2026-03-18*
*Tests: 280 passed / 0 failed*
*ASVS 5.0 chapters: V1.9 (Communications), V2.1 (Authentication), V7.4 (Logging), V14.1 (Build)*
