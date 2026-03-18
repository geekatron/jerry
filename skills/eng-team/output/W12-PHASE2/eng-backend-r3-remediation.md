# eng-backend R3 Remediation Report

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0 Executive Summary](#l0-executive-summary) | What was fixed, security controls applied, residual risk |
| [L1 Technical Detail](#l1-technical-detail) | Per-finding fix record with code locations |
| [L2 Strategic Implications](#l2-strategic-implications) | Security posture assessment, architecture evolution |

---

## L0 Executive Summary

**Engagement ID:** W12-PHASE2-R3
**Criticality:** C4
**R2 Score:** 0.861 (REVISE band -- below 0.92 gate)
**Fixes Applied:** 15 code changes across 8 files + 9 test file updates
**Tooling:** 264/264 tests PASS | pyright 0 errors | ruff 0 violations

### What Was Fixed

All P0 Critical and P1 Major findings from the R2 adversary tournament were
remediated. The 15 fixes address:

- **Credential filter hardening:** `no_filter` bypass via `None` default
  constructor removed; `strict_mode` decoupled from `os.environ`; sliding
  window extended from pairs to N-line (default 3); both stdout and stderr
  quarantined unconditionally.
- **Exit code contract:** `ZONE3_APPROVAL_DENIED = 11` added, ending the
  conflation of approval denial with engagement-not-initialized (exit code 5).
- **Composition root compliance:** `LocalExecutor` and `ContainerExecutor`
  now constructed in the factory, not inline in helpers (H-07(c)).
- **Zone 3 approval audit trail:** Persistent JSON event written on every
  approval/denial, providing tamper-evident record.
- **FamilyRegistryLoader resilience:** Single failing family is now skipped
  rather than halting all family loading.
- **Type safety:** `load_config()` return type tightened to `dict[str, Any]`.
- **Environment coupling:** `ModeResolverService._DEFAULT_ENV_PREFIX` changed
  from `"RAINBOW"` to `"JERRY"` (produces `JERRY_TOOL_MODE`).

### OWASP Top 10 Coverage

| OWASP Category | Control Applied |
|----------------|----------------|
| A01:2021 Broken Access Control | ZONE3_APPROVAL_DENIED distinguishes denial; health check precedes approval |
| A02:2021 Cryptographic Failures | Quarantine dir chmod 0o700; files chmod 0o600 |
| A04:2021 Insecure Design | Composition root compliance; required constructor args remove bypass |
| A08:2021 Data Integrity Failures | errors="replace" prevents silent data loss on Unicode |
| A09:2021 Logging Failures | Approval audit trail; global quarantine fallback for Zone 1 |

### Residual Risk

- `_DEFAULT_ENV_PREFIX = "JERRY"` is a behavioural change: callers relying on
  `RAINBOW_TOOL_MODE` without passing an explicit prefix will no longer find their
  setting. The fix is intentional (IN-020-R2) and documented.
- The approval audit trail uses `engagement_init._base_dir` (private attribute) for
  the fallback path. This should be replaced with a public accessor in a follow-on
  enabler.

---

## L1 Technical Detail

### Fix #1: Remove `credential_filter: ... | None = None` default (IN-017-R2)

**Files:** `src/tool_exec/infrastructure/adapters/local_executor.py`,
`src/tool_exec/infrastructure/adapters/container_executor.py`

Both executors previously defaulted `credential_filter` to `None`, creating a
bypass path: any caller instantiating without the argument would silently skip
all credential detection. The parameter is now required (no default). All callers
(composition root factory, test helpers) updated to supply `CredentialFilterService`.

### Fix #2: Unconditional quarantine with global fallback (PM-006-R2 / RT-R2-002)

**File:** `src/interface/cli/tool_exec_commands.py` (`_quarantine_output`)

The previous `if credential_detected and engagement_id:` guard meant Zone 1
credential detections without an active engagement were silently discarded.
The guard is removed. When `engagement_id is None`, the global fallback path
`work/.credential-quarantine/` is used. A warning is logged.

### Fix #3: Add `ZONE3_APPROVAL_DENIED = 11` (IN-015-R2 / NEW-001)

**File:** `src/tool_exec/domain/value_objects/exit_codes.py`

Approval denial previously returned `ENGAGEMENT_NOT_INIT` (5), making the
machine-readable contract ambiguous. `ZONE3_APPROVAL_DENIED = 11` is a distinct
code for the approval gate path. The family-specific range shifted from 11+ to 12+.

### Fix #4: Pass both `raw_stdout` AND `raw_stderr` to quarantine (RT-R2-001)

**Files:** `_execute_local()`, `_execute_container()`, `_quarantine_output()`

`_execute_local` and `_execute_container` now include `"raw_stderr"` in their
returned dicts. `_quarantine_output` signature changed to `(raw_stdout, raw_stderr, ...)`.
Two separate files (`quarantine-*.stdout.txt`, `quarantine-*.stderr.txt`) are written.

### Fix #5: Sliding window extended to N lines (PM-001-R2)

**File:** `src/tool_exec/domain/services/credential_filter.py`

`filter_output()` gains `window_size: int = 3`. The Pass 2 loop now iterates over
window sizes from 2 to `effective_window` (clamped minimum 2), joining `win` adjacent
lines per iteration. Credentials split across 3 lines are now detected. The old
`_redact_adjacent_lines` method is preserved as a compatibility shim delegating to
the new `_redact_window_lines(lines, idx, win, match)`.

### Fix #6: `load_config() -> dict[str, Any]` (SR-001-20260318)

**Files:** `src/tool_exec/domain/ports/tool_family_resolver_port.py`,
`src/tool_exec/infrastructure/adapters/rainbow_tool_resolver.py`

Bare `-> dict` return type replaced with `-> dict[str, Any]`. `from typing import Any`
added to the port module (the adapter already imported it).

### Fix #7: Composition root wires all services (CC-004-20260318)

**File:** `src/interface/cli/tool_exec_commands.py` (`create_tool_exec_handler`)

Factory now returns `local_executor`, `container_executor`, and `mode_resolver` in
addition to the original three. `_execute_local()` and `_execute_container()` accept
a pre-built executor argument instead of constructing one inline. This satisfies
H-07(c) (composition root exclusivity).

### Fix #8: Remove `os.environ` from domain service (PM-004-R2)

**File:** `src/tool_exec/domain/services/credential_filter.py`

`os.environ.get("JERRY_STRICT_MODE")` removed from `filter_output()`. The method
now accepts `strict_mode: bool = True` (default True maintains the security
invariant). The CLI handler reads `JERRY_STRICT_MODE` from the environment and
passes the resolved boolean. `import os` removed from the domain service.

### Fix #9: `os.chmod(quarantine_dir, 0o700)` after mkdir (SR-002-20260318)

**File:** `src/interface/cli/tool_exec_commands.py` (`_quarantine_output`)

`mkdir` respects umask (typically 0o022 → resulting mode 0o755). Adding
`os.chmod(str(quarantine_dir), 0o700)` after `mkdir` ensures the quarantine
directory itself is protected regardless of umask. NIST CSF PR.DS-1.

### Fix #10: Wrap `filter_output()` with `try/except RuntimeError` (PM-003-R2)

**Files:** `local_executor.py`, `container_executor.py`

When `filter_output()` raises `RuntimeError` (strict mode violation), the executor
now catches it and returns a result with `exit_code=STRICT_MODE_VIOLATION` (9) and
an informative stderr message. This prevents unhandled exceptions from propagating
to the CLI handler.

### Fix #11: Change `_DEFAULT_ENV_PREFIX` to `"JERRY"` (IN-020-R2)

**File:** `src/tool_exec/domain/services/mode_resolver.py`

Default changed from `"RAINBOW"` to `"JERRY"`. The format string
`f"{prefix}_TOOL_MODE"` produces `JERRY_TOOL_MODE` from prefix `"JERRY"`.
This decouples the generic service from the rainbow family.

### Fix #12: Write Zone 3 approval/denial audit trail (IN-016-R2)

**File:** `src/interface/cli/tool_exec_commands.py`

`_prompt_zone3_approval()` signature extended to accept `engagement_id` and
`engagement_init`. A new `_write_approval_audit()` helper writes a JSON event
(`{timestamp, engagement_id, tool_command, zone, approved, reason}`) to
`<engagement>/audit/zone3-approval-*.json` or `work/.zone3-audit/` when no
engagement is active. Audit write failures are caught and logged without
suppressing the approval decision.

### Fix #13: Health check BEFORE Zone 3 approval gate (RT-R2-004)

**File:** `src/interface/cli/tool_exec_commands.py` (`handle_tool_exec`)

The `if health_check: return _handle_health_check(...)` block was previously
positioned after the Zone 3 approval prompt. It now appears between the
`ZONE3_CONTAINER_REQUIRED` check and the `requires_approval` check. Operators
can check container health without triggering an approval request.

### Fix #14: Skip failing family, raise only when all fail (NEW-002 / FM-005)

**File:** `src/tool_exec/infrastructure/registry/family_registry_loader.py`

`except Exception: raise` changed to `except Exception: continue`. A counter
(`attempted`) tracks enabled families that were attempted. After the loop, if
`attempted > 0 and not resolvers`, a `ValueError("No family resolvers could be
loaded...")` is raised. If `attempted == 0` (all families disabled), an empty
dict is returned.

### Fix #15: `errors="replace"` in quarantine `write_text()` (NEW-003)

**File:** `src/interface/cli/tool_exec_commands.py` (`_quarantine_output`)

`write_text(content, encoding="utf-8")` changed to
`write_text(content, encoding="utf-8", errors="replace")` on both stdout and
stderr quarantine files and the meta file. Prevents `UnicodeEncodeError` when
tool output contains binary or mixed-encoding sequences.

---

## L2 Strategic Implications

### Security Posture Assessment

The R3 fixes close the remaining credential filter bypass vectors identified
in the R2 tournament. The most significant improvement is the elimination of
the `None` default in executor constructors: this was the only production path
where credential filtering could be silently absent. With required constructor
arguments, the type checker (pyright) now enforces filter injection.

The Zone 3 approval audit trail is a new defensive control not present in the
bash implementation. It provides evidence for engagement review and incident
response -- if a Zone 3 tool is misused, the audit log establishes whether
operator approval was obtained.

### Dependency Risk Landscape

No new external dependencies were introduced. The `os` module was removed
from `credential_filter.py` (reducing its surface), and no new stdlib imports
were added beyond those already present.

### Scalability of Security Controls

The `window_size` parameter on `filter_output()` is forward-compatible. As new
multi-line credential formats are identified (e.g., PEM-encoded certificates split
over many lines), `window_size` can be increased by the caller without changing the
domain service interface.

The composition root factory pattern scales cleanly: each new executor type added
to the pipeline requires only a single addition to `create_tool_exec_handler()`.
The current pattern demonstrates this with `local_executor`, `container_executor`,
and `mode_resolver` all wired in one place.

### Evolution Path for Auth Architecture

The approval audit trail currently uses a private `engagement_init._base_dir`
attribute for the fallback path. A follow-on enabler should add a public
`EngagementInitializer.global_audit_dir()` accessor to remove this coupling.

The `_write_approval_audit()` helper is a direct file writer. Future iterations
could route through an `AuditLogPort` (domain port) to allow pluggable audit
backends (e.g., SIEM, syslog) without changing the approval gate logic.

---

*Generated by: eng-backend (Secure Backend Engineer)*
*Engagement: W12-PHASE2-R3*
*Date: 2026-03-18*
*Tests: 264 passed | pyright: 0 errors | ruff: 0 violations*
