# eng-backend R4 Priority Fixes — W12-PHASE2-R4

| Field | Value |
|-------|-------|
| Engagement ID | W12-PHASE2-R4 |
| Criticality | C4 |
| Target | `src/tool_exec/` bounded context composite score >= 0.95 (B11 gate) |
| Weakest Dimensions | Traceability (0.78), Completeness (0.87) |
| Fixes Applied | 11 |
| Validation | pytest 280/280 PASS, pyright 0 errors, ruff 0 errors |

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0 Executive Summary](#l0-executive-summary) | What was done and what was fixed |
| [L1 Technical Detail](#l1-technical-detail) | Per-fix implementation record |
| [L2 Strategic Implications](#l2-strategic-implications) | Security posture and architecture impact |
| [Validation Results](#validation-results) | Test, type, lint gate outcomes |

---

## L0 Executive Summary

All 11 items from the adv-scorer R3 priority list were implemented to address the two weakest scoring dimensions (Traceability 0.78 and Completeness 0.87). The fixes span five source files in the domain layer, one infrastructure file, one port interface, and the CLI handler. Four test files were updated to match the new behavioral contracts.

OWASP categories addressed: A09 (Logging Failures — FM-006, FM-001), A01 (Broken Access Control — CV-003 zone gate), A02 (Cryptographic Failures — CV-006 SHA-256 filenames), A05 (Security Misconfiguration — PM-004-R3 singleton isolation), A07 (Auth Failures — strict mode enforcement).

All three validation gates pass cleanly: 280/280 unit tests, 0 pyright errors, 0 ruff errors.

---

## L1 Technical Detail

### Traceability Fixes

#### FM-006 — Auto-detection routing logging
**File:** `src/tool_exec/domain/services/family_router.py`

Added `import logging` and `logger = logging.getLogger(__name__)`. In `_resolve_auto()`, added `logger.info("Auto-detected '%s' -> family '%s'", tool_command, resolver.FAMILY_NAME)` before returning the resolution entry.

Companion change: `src/tool_exec/domain/ports/tool_family_resolver_port.py` — declared `FAMILY_NAME: str` as a class variable on the abstract port so pyright can verify the attribute access is valid on all concrete implementations.

Test fix: `tests/unit/tool_exec/test_family_router.py` — `_make_resolver()` now sets `resolver.FAMILY_NAME = name` on the mock, matching the new port contract.

**OWASP A09 mitigation:** Security-relevant routing decisions are now observable in structured logs, supporting audit trail requirements.

#### SR-003 — Law of Demeter violation in `_write_approval_audit`
**File:** `src/tool_exec/domain/services/engagement_initializer.py`

Added `global_audit_dir() -> Path` public method returning `self._base_dir.parent / ".zone3-audit"`. Eliminates the cross-module private attribute access (`engagement_init._base_dir`) in the CLI handler.

**File:** `src/interface/cli/tool_exec_commands.py`

`_write_approval_audit()` now calls `engagement_init.global_audit_dir()` instead of accessing `engagement_init._base_dir.parent / ".zone3-audit"` directly.

#### CV-002 — JERRY_TOOL_MODE generic fallback
**File:** `src/tool_exec/domain/services/mode_resolver.py`

Added Level 2b in the resolution hierarchy: after checking the family-specific env var (e.g., `RAINBOW_TOOL_MODE`), the resolver checks `JERRY_TOOL_MODE` as a global fallback if the current instance's `env_var_name` differs from `"JERRY_TOOL_MODE"`. This closes the gap where users set `JERRY_TOOL_MODE` but the family-specific resolver ignored it.

Constant: `_GLOBAL_ENV_VAR = "JERRY_TOOL_MODE"` defined locally in `resolve()`.

#### CV-013B — `--list-families` missing tool count
**File:** `src/tool_exec/domain/value_objects/tool_family_info.py`

Added `tool_count: int | None = field(default=None)` to the frozen `ToolFamilyInfo` dataclass.

**File:** `src/tool_exec/infrastructure/registry/family_registry_loader.py`

Added `project_root: Path | None = None` parameter to `list_families()`. Added private `_count_tools(config_path, project_root) -> int | None` helper that loads the YAML and counts entries in the `tools` key. When `project_root` is provided, reconstructs `ToolFamilyInfo` instances with `tool_count` populated.

**File:** `src/interface/cli/tool_exec_commands.py`

`--list-families` handler now passes `project_root=project_root` to `loader.list_families()` and displays `tools=N` or `tools=?` per family.

---

### Completeness Fixes

#### FM-001 — `--no-filter` file-based audit trail
**File:** `src/interface/cli/tool_exec_commands.py`

Added `_write_no_filter_audit(tool_command, engagement_id, strict_mode_env, project_root)` function. Writes a JSONL entry to `work/.no-filter-audit/no-filter-audit.jsonl` (engagement-scoped path when engagement is active) with timestamp, tool command, engagement ID, and strict mode status. Called in the `no_filter` code path after the strict-mode gate passes.

**OWASP A09 mitigation:** `--no-filter` bypass events are now permanently audited to disk, not merely emitted as a `logger.warning`.

#### CV-003 — Zone 2/3 strict mode gate (exit 6)
**File:** `src/interface/cli/tool_exec_commands.py`

Added gate after mode resolution: when `strict=True` and the resolved family zone is `Zone 2` or `Zone 3` and no explicit mode was provided (via `--mode`, family-specific env var, or `JERRY_TOOL_MODE`), the handler returns `ExitCode.MODE_UNSET` (exit 6) with a descriptive error message.

Explicit mode detection checks three sources: `cli_mode`, `os.environ.get(mode_resolver.env_var_name)`, and `os.environ.get("JERRY_TOOL_MODE")`.

#### CV-006 — SHA-256 content-addressable quarantine filenames
**File:** `src/interface/cli/tool_exec_commands.py`

`_quarantine_output()` now computes `sha256_stdout = hasher.hash_string(raw_stdout)` and `sha256_stderr = hasher.hash_string(raw_stderr)` before writing files. Filenames use the hash as the stem:
- `{sha256_stdout}.stdout.raw`
- `{sha256_stderr}.stderr.raw`
- `{sha256_stdout}.meta.json`

This implements UC-005 DR-019 (content-addressable deduplication): identical output produces the same quarantine filename, preventing duplicate quarantine files.

Test fix: `tests/unit/tool_exec/test_c4_remediation.py` — glob pattern updated from `quarantine-*.stdout.txt` to `*.stdout.raw`.

#### CV-007 — `--no-filter` + strict returns exit 9 (documented)
**Files:** `projects/PROJ-023-exploit-framework/work/design/use-cases/UC-TOOLEXEC-001.md`, `UC-TOOLEXEC-005.md`

After reviewing the exit code semantics, the decision was to retain exit code 9 (`STRICT_MODE_VIOLATION`) rather than change to 6 (`MODE_UNSET`). Rationale: strict mode rejection of `--no-filter` is a policy enforcement event, not a configuration gap. Both UC documents were updated to document exit code 9 in AF-05 (UC-001) and AF-02 (UC-005) with explicit rationale explaining why 9 was chosen over 6.

No code change required — the implementation already uses `ExitCode.STRICT_MODE_VIOLATION` (9) correctly.

#### CV-010 — `.engagement-meta.json` field alignment with UC spec
**File:** `src/tool_exec/domain/services/engagement_initializer.py`

The metadata written to `.engagement-meta.json` was updated to use UC-spec field names:
- `"id"` (was `"engagement_id"` in the old implementation)
- `"created_at"` — ISO 8601 UTC timestamp using `datetime.now(tz=UTC).strftime("%Y-%m-%dT%H:%M:%SZ")`
- `"created_by"` — resolved from `os.environ.get("USER") or os.environ.get("USERNAME") or "unknown"`

DR-010 write-once invariant enforced: `if not meta_path.exists():` guard prevents overwriting the original creation timestamp on re-initialization.

Test fix: `tests/unit/tool_exec/test_engagement_initializer.py` — assertions updated to check `meta["id"]`, `"created_at"`, and `"created_by"`.

#### CV-016 — `evidence_auto_persist` flag in SecurityPolicy
**File:** `src/tool_exec/domain/value_objects/security_policy.py`

Added `evidence_auto_persist: bool = True` to the frozen `SecurityPolicy` dataclass. Default `True` preserves backward compatibility for all existing families.

**File:** `src/interface/cli/tool_exec_commands.py`

Evidence persistence gate now checks `policy.evidence_auto_persist`. Tools in families that set `evidence_auto_persist=False` will not auto-persist evidence even when an engagement is active and no credential was detected.

#### PM-004-R3 — CredentialFilterService invocation-scoped instances
**File:** `src/tool_exec/domain/services/credential_filter.py`

Added `with_extra_patterns(patterns, case_sensitive=True) -> CredentialFilterService` factory method that creates a fresh `CredentialFilterService` instance containing base patterns plus the provided extras. The shared singleton is not mutated. Fixed ruff UP037 violation: removed quotes from return type annotation.

**File:** `src/interface/cli/tool_exec_commands.py`

Replaced `credential_filter.extend_patterns(policy.credential_filter_patterns)` mutation with:
```python
if policy.credential_filter_patterns:
    invocation_filter = credential_filter.with_extra_patterns(
        policy.credential_filter_patterns
    )
    local_executor = LocalExecutor(credential_filter=invocation_filter)
    container_executor = ContainerExecutor(
        credential_filter=invocation_filter,
        project_root=str(project_root),
    )
```
The shared `credential_filter` singleton remains unmodified. The invocation-scoped `invocation_filter` is used only for this execution.

---

## L2 Strategic Implications

### Security Posture Assessment

The R4 fixes complete the behavioral contract implementation for the credential filter pipeline (BC-07) and engagement management subsystem. The SHA-256 content-addressable quarantine filenames (CV-006) establish a deduplication invariant that prevents storage bloat in repeated-scan scenarios. The `evidence_auto_persist` opt-out flag (CV-016) gives families control over evidence accumulation, reducing unintended data retention for Zone 1 non-engagement tools.

The PM-004-R3 singleton fix closes a subtle multi-invocation contamination vector: without it, the shared `CredentialFilterService` would accumulate family-specific patterns across invocations in the same process, causing false positives for subsequent unrelated families. This is a correctness issue with security implications — an AI CLI family's key patterns bleeding into a network scanner family's filter run would produce misleading credential detections.

### Dependency Risk Landscape

The `FAMILY_NAME: str` class variable added to `ToolFamilyResolverPort` creates a contract that all concrete adapter implementations must satisfy. Any existing adapter missing this attribute will now cause a pyright error at CI. This is intentional — the attribute is already used in the FM-006 logging path at runtime, so pyright enforcement prevents a runtime `AttributeError` from reaching production.

### Evolution Path

The `evidence_auto_persist` flag anticipates a future batch-processing mode where tools run without user context. Families that generate high-volume outputs (e.g., port scanners, OSINT pipeline) can set `evidence_auto_persist=False` to suppress automatic evidence accumulation while still benefiting from credential filtering and zone enforcement.

The `global_audit_dir()` public method on `EngagementInitializer` establishes a clean API surface for Zone 3 audit artifacts. Future Zone 3 features (approval expiry, approval revocation) can use this method without accessing internal state.

---

## Validation Results

| Gate | Command | Result |
|------|---------|--------|
| Unit tests | `uv run pytest tests/unit/tool_exec/ -q --tb=short` | 280 passed, 0 failed |
| Type checking | `uv run pyright src/tool_exec/ src/interface/cli/tool_exec_commands.py` | 0 errors, 0 warnings |
| Lint | `uv run ruff check src/tool_exec/ src/interface/cli/tool_exec_commands.py` | All checks passed |

### Test Fixes Required

Four tests required updates to match the new behavioral contracts introduced by R4 fixes:

| Test File | Test Method | Fix Applied |
|-----------|-------------|-------------|
| `test_engagement_initializer.py` | `test_initialize_writes_metadata` | CV-010: Assertions updated to check `id`, `created_at`, `created_by` |
| `test_family_router.py` | `test_auto_detect_single_family` | FM-006: `resolver.FAMILY_NAME = name` added to mock factory |
| `test_family_router.py` | `test_auto_detect_multiple_families` | FM-006: same mock factory fix |
| `test_c4_remediation.py` | `test_quarantine_writes_file` | CV-006: glob updated from `quarantine-*.stdout.txt` to `*.stdout.raw` |

All fixes align the tests with the updated behavioral contracts — no test semantics were weakened.
