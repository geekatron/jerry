# Implementation Plan: STORY-W12-001 Jerry CLI Tool Exec Command

> **Engagement:** W12-PHASE2
> **Criticality:** C3 (Significant -- >10 files, API surface change, security-sensitive)
> **Methodology:** MS SDL Requirements Phase, NIST SSDF PO.1/PO.3/PS.1/PS.2, OWASP SAMM
> **Date:** 2026-03-17
> **Agent:** eng-lead (convergent mode)
> **Source Artifacts:**
>   - `skills/eng-team/output/W12-PHASE2/eng-architect-threat-model.md`
>   - `projects/PROJ-023-exploit-framework/work/FEAT-W12-tool-exec-cli/WORKTRACKER.md`
>   - `projects/PROJ-023-exploit-framework/work/design/jerry-tool-exec-cli-design-v2.md`
>   - `projects/PROJ-023-exploit-framework/work/design/use-cases/UC-TOOLEXEC-001.md`
>   - `src/tool_exec/` scaffold (all files read and assessed)
>   - `src/interface/cli/tool_exec_commands.py` (CLI handler, complete)
>   - `tests/unit/tool_exec/` (all 12 test files assessed)

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0: Executive Summary](#l0-executive-summary) | Timeline, key decisions, risk summary, team readiness |
| [L0: Scaffold Assessment](#l0-scaffold-assessment) | What exists, what needs revision, what is missing |
| [L1: Per-Task Implementation Guidance](#l1-per-task-implementation-guidance) | 13-task breakdown with security standards mapping |
| [L1: Top-3 Threat Mitigation Integration](#l1-top-3-threat-mitigation-integration) | T-01/T-03/T-06 mapped to tasks with implementation detail |
| [L1: Coding Standards Checklist](#l1-coding-standards-checklist) | H-07/H-10/H-11/H-20 enforcement rules per task category |
| [L1: Testing Strategy](#l1-testing-strategy) | Unit tests, integration tests, BDD feature file plan |
| [L1: Dependency Governance](#l1-dependency-governance) | Runtime dependencies, dev dependencies, banned APIs |
| [L2: SAMM Maturity Assessment](#l2-samm-maturity-assessment) | Current vs target maturity across SAMM practices |
| [L2: PR Review Criteria](#l2-pr-review-criteria) | Security checkpoints for every PR in STORY-W12-001 |
| [L2: Standards Mapping](#l2-standards-mapping) | Implementation tasks cross-referenced to MS SDL, SSDF, ASVS |

---

## L0: Executive Summary

### Implementation Timeline

STORY-W12-001 contains 13 tasks totaling 24.5 estimated hours across three waves:

| Wave | Tasks | Hours | Parallelism | Gate |
|------|-------|-------|-------------|------|
| Wave 1 (Foundation) | TASK-001C, TASK-001B, TASK-001D, TASK-001 | 4.5 hrs | TASK-001C and TASK-001B in parallel | Value objects + port + loader + CLI skeleton complete |
| Wave 2 (Core Services) | TASK-002, TASK-003, TASK-006, TASK-007 | 9 hrs | TASK-003 and TASK-007 in parallel after TASK-002 | Security services complete; top-3 mitigations integrated |
| Wave 3 (Executors + Close-out) | TASK-004, TASK-005, TASK-008, TASK-009, TASK-010 | 11 hrs | TASK-004 and TASK-005 in parallel after TASK-006 | Full pipeline wired; 90% coverage verified |

**Estimated total:** 24.5 hours (matches WORKTRACKER.md estimate of 17 story points across 13 tasks).

### Key Standards Decisions

1. **Module allowlist is a Wave 1 blocker.** Mitigation M-01 (T-01: importlib allowlist) must be integrated into TASK-001D before the loader ships. No loader that performs unrestricted `importlib.import_module()` may be merged.

2. **Credential filter expansion is a Wave 2 deliverable.** Mitigation M-02 (T-03: pattern expansion) is owned by TASK-006. The task estimate has been assessed as sufficient for adding 7 new patterns plus corresponding test canaries.

3. **Strict mode enforcement is a Wave 2 deliverable.** Mitigation M-03 (T-06: `--no-filter` gating) is owned by TASK-001 (CLI argument parsing) and the CLI handler in `tool_exec_commands.py`. The CLI handler already exists but lacks the `JERRY_STRICT_MODE` check.

4. **The existing CLI handler (`tool_exec_commands.py`) has structural issues** that must be addressed before TASK-010 (unit tests) can achieve 90% coverage. See the scaffold assessment below.

### Dependency Risk Summary

| Dependency | Version | Risk | Action |
|-----------|---------|------|--------|
| `pyyaml` | `^6.0.2` | LOW -- `yaml.safe_load()` used consistently | No change; verify safe_load usage in all new code |
| `subprocess` | stdlib | LOW -- `shell=False` enforced | Monitor: no new code may pass `shell=True` |
| `importlib` | stdlib | HIGH -- dynamic module loading | M-01 allowlist restricts to `src.tool_exec.infrastructure.adapters.*` |
| `argparse` | stdlib | LOW | Supplement with domain-layer input validation for engagement ID and evidence path |
| `hashlib` | stdlib | LOW -- SHA-256 only | No change required |
| `re` | stdlib | MEDIUM -- ReDoS risk on new patterns | Review each new pattern for catastrophic backtracking before merge |

### Team Readiness Assessment (OWASP SAMM)

| SAMM Practice | Current Level | Target (W12) | Gap |
|--------------|--------------|--------------|-----|
| Security Requirements | 1 | 2 | Threat model exists but requirements not yet codified in implementation acceptance criteria |
| Threat Assessment | 2 | 2 | STRIDE+DREAD complete; attack trees produced |
| Implementation Review | 1 | 2 | Tests exist for existing scaffold; no systematic checklist enforced |
| Defect Management | 1 | 2 | Threats identified; tracking not yet linked to GitHub Issues |

---

## L0: Scaffold Assessment

The `src/tool_exec/` scaffold was assessed against the 13 tasks. Status:

### Exists and is CORRECT -- no revision required

| File | Task | Assessment |
|------|------|-----------|
| `domain/value_objects/security_policy.py` | TASK-001C | Correct frozen dataclass; H-10 compliant; H-11 compliant |
| `domain/value_objects/tool_family_info.py` | TASK-001C | Correct frozen dataclass; all fields present |
| `domain/value_objects/exit_codes.py` | TASK-009 | `ExitCode(IntEnum)` complete for values 0-6; missing `FAMILY_NOT_FOUND=7` and `FAMILY_CONFIG_ERROR=8` per v2 design |
| `domain/ports/tool_family_resolver_port.py` | TASK-001B | Correct ABC with 4 abstract methods; H-10 compliant; H-11 compliant |
| `domain/services/evidence_hasher.py` | TASK-007 | Correct; `hash_string`, `hash_bytes`, `hash_file` all present with type hints and docstrings |
| `domain/services/mode_resolver.py` | TASK-003 | Present but uses `RAINBOW_TOOL_MODE` env var name -- must update to check both `JERRY_TOOL_MODE` (primary) and `RAINBOW_TOOL_MODE` (backward-compat) |
| `infrastructure/adapters/rainbow_tool_resolver.py` | TASK-002 | Complete; longest-prefix matching correct |
| `infrastructure/adapters/container_executor.py` | TASK-005 | Present; missing: stderr credential filtering (T-18), compose file path validation (M-11) |
| `tests/unit/tool_exec/` | TASK-010 | 12 test files exist; assessed as skeleton-level (partial coverage); full test suite needed |

### Exists but requires REVISION

| File | Task | Required Change | Threat |
|------|------|-----------------|--------|
| `infrastructure/registry/family_registry_loader.py` | TASK-001D | Add `_ALLOWED_MODULE_PREFIXES` allowlist check before `importlib.import_module()` call (line 147) | T-01 / M-01 |
| `domain/services/engagement_initializer.py` | TASK-008 | Replace blocklist validation (`..`, `/`, `\`) with allowlist regex `^[a-zA-Z0-9][a-zA-Z0-9_-]*$`; add `os.chmod(0o700)` on quarantine directory | T-08/M-05, T-21/M-10 |
| `domain/services/credential_filter.py` | TASK-006 | Add 7 new patterns (M-02): GitHub PAT, JWT, AI provider keys, Stripe, Slack; extend stderr coverage | T-03 / M-02 |
| `domain/value_objects/exit_codes.py` | TASK-009 | Add `FAMILY_NOT_FOUND=7`, `FAMILY_CONFIG_ERROR=8`, `STRICT_MODE_VIOLATION=6` (rename `MODE_UNSET`) | UC-TOOLEXEC-001 exit contract |
| `infrastructure/adapters/local_executor.py` | TASK-004 | Add `shutil.which()` check before subprocess call; filter stderr alongside stdout | T-02/M-07, T-18/M-08 |
| `domain/services/mode_resolver.py` | TASK-003 | Check `JERRY_TOOL_MODE` first, then `RAINBOW_TOOL_MODE` (backward compat); update `ENV_VAR_NAME` to a list | T-22; v2 design DR-005 |
| `src/interface/cli/tool_exec_commands.py` | TASK-001 | Add `JERRY_STRICT_MODE` check to block `--no-filter`; add evidence path sandboxing; fix hardcoded rainbow config path | T-06/M-03, T-07/M-06 |

### Does NOT yet exist -- must be created new

| File | Task | Purpose |
|------|------|---------|
| `domain/services/family_router.py` | TASK-002 | Already exists; router service is complete |
| Tests for top-3 mitigations | TASK-010 | Canary fixtures for new credential patterns; allowlist rejection tests; strict mode enforcement tests |
| BDD feature file implementation | TASK-010 | `skills/rainbow/tests/bdd/test_tool_exec.feature` exists but steps not implemented |

---

## L1: Per-Task Implementation Guidance

Tasks are presented in dependency order as specified in WORKTRACKER.md. Each task entry includes: current state assessment, specific implementation requirements, security standards mapping, and acceptance criteria.

---

### TASK-001C: SecurityPolicy and ToolFamilyInfo Value Objects

**Dependency:** None (Wave 1, start immediately)
**Estimate:** 0.5 hrs
**Current state:** COMPLETE -- both files exist, are H-10 and H-11 compliant, frozen dataclasses with `__post_init__` validation.

**Required changes:** None.

**Security standards mapping:**
- OWASP ASVS V5.1 (Input Validation): `__post_init__` validates `network_access` enum values -- correct pattern.
- CWE-20 (Improper Input Validation): Addressed by frozen dataclass + post-init validation.

**Acceptance criteria:**
- `security_policy.py` contains exactly one class (`SecurityPolicy`) per H-10.
- `tool_family_info.py` contains exactly one class (`ToolFamilyInfo`) per H-10.
- All public attributes have type annotations per H-11.
- Module-level docstring present on both files.

---

### TASK-001B: ToolFamilyResolverPort Interface Design

**Dependency:** TASK-001C (can run in parallel with 001C if ABCs are written before value objects are needed)
**Estimate:** 0.5 hrs
**Current state:** COMPLETE -- correct ABC with 4 abstract methods: `can_resolve`, `resolve`, `security_policy`, `load_config`. `TYPE_CHECKING` guard used correctly for forward references.

**Required changes:** None.

**Security standards mapping:**
- OWASP ASVS V1.1 (Secure Software Development Lifecycle): Port contract enforces that every resolver exposes `security_policy()` -- policy cannot be omitted.
- MS SDL Requirements Phase: The port encodes the security requirements (security policy retrieval) as a compile-time contract, not a runtime convention.

**Acceptance criteria:**
- `tool_family_resolver_port.py` contains exactly one class per H-10.
- All 4 abstract methods have type hints and docstrings per H-11.
- `ABC` import from `abc` is the only domain-layer dependency.

---

### TASK-001D: Family Registry Loader (with M-01 Allowlist)

**Dependency:** TASK-001C, TASK-001B
**Estimate:** 1 hr (includes M-01 implementation)
**Current state:** EXISTS but REQUIRES REVISION -- `_load_resolver()` calls `importlib.import_module(family_info.resolver_module)` without any prefix validation. This is T-01 CRITICAL threat, DREAD 38.

**Required changes -- M-01 implementation (MUST before merge):**

Add a class-level constant to `FamilyRegistryLoader`:

```python
_ALLOWED_MODULE_PREFIXES: tuple[str, ...] = (
    "src.tool_exec.infrastructure.adapters.",
)
```

In `_load_resolver()`, add this check BEFORE `importlib.import_module()`:

```python
if not family_info.resolver_module.startswith(self._ALLOWED_MODULE_PREFIXES):
    msg = (
        f"Resolver module '{family_info.resolver_module}' is outside the "
        f"allowed prefix set. Permitted prefixes: "
        f"{', '.join(self._ALLOWED_MODULE_PREFIXES)}"
    )
    raise ValueError(msg)
```

The check must execute before the import call on line 147 of the current scaffold. The `issubclass` check after import is a secondary defense and must be retained.

**Security standards mapping:**
- T-01 mitigation M-01 (MUST implement)
- OWASP ASVS V14.2.1 (Dependency Verification): Restrict dynamic loading to known-good module namespaces.
- CWE-502 (Deserialization of Untrusted Data): Dynamic import from external config is analogous -- allowlist is the correct mitigation.
- NIST SSDF PO.1.1: Security requirements must be codified in the implementation.
- MS SDL Threat Modeling: T-01 is classified CRITICAL (DREAD 38); mitigation must be present before deployment.

**Acceptance criteria:**
- `_ALLOWED_MODULE_PREFIXES` constant is present and not empty.
- `_load_resolver()` raises `ValueError` for any module path not starting with a permitted prefix.
- `ValueError` is raised BEFORE `importlib.import_module()` is called.
- Unit tests cover: (a) valid module prefix accepted, (b) module outside allowlist rejected with ValueError, (c) empty module path rejected.
- Error message does NOT include the malicious module path verbatim (information disclosure risk T-12).

---

### TASK-001: CLI Skeleton with --family Flag (with M-03 Strict Mode)

**Dependency:** TASK-001D
**Estimate:** 2.5 hrs (includes M-03 implementation)
**Current state:** `src/interface/cli/tool_exec_commands.py` EXISTS and is substantially complete. The `handle_tool_exec()` function implements the full pipeline. However, three security defects must be remediated.

**Required changes:**

**Defect 1 -- M-03 (MUST implement): Add `JERRY_STRICT_MODE` check for `--no-filter`.**

In `handle_tool_exec()`, after the `no_filter = getattr(args, "no_filter", False)` assignment (line 82), add:

```python
import os

if no_filter and os.environ.get("JERRY_STRICT_MODE") == "true":
    print(
        "Error: --no-filter is FORBIDDEN in strict mode (JERRY_STRICT_MODE=true). "
        "Credential protection cannot be disabled when strict mode is active.",
        file=sys.stderr,
    )
    return ExitCode.STRICT_MODE_VIOLATION
if no_filter:
    import logging
    logging.getLogger(__name__).warning(
        "WARNING: --no-filter is active. Credential filter bypassed for: %s",
        tool_command,
    )
```

**Defect 2 -- M-06 (SHOULD implement): Evidence directory path sandboxing.**

In `_persist_evidence()`, the `evidence_dir_override` path is used without validation. Add:

```python
if evidence_dir_override:
    project_root = _find_project_root()
    resolved = Path(evidence_dir_override).resolve()
    if not str(resolved).startswith(str(project_root.resolve())):
        raise ValueError(
            f"Evidence directory '{evidence_dir_override}' is outside the "
            f"project root. Sandboxed to: {project_root}"
        )
    evidence_dir = resolved
    evidence_dir.mkdir(parents=True, exist_ok=True)
```

**Defect 3 -- hardcoded config path (correctness).**

Line 125 hardcodes `skills/rainbow/config/tool-exec.yaml`. This path should come from the `ToolResolutionEntry.family` field plus the registry loader's `config_path`. The resolver already has its config loaded at instantiation time -- the config lookup in `handle_tool_exec()` should use the resolver's own config, not re-read a hardcoded path. Refactor to call `resolver.load_config(family_info.config_path)` where `family_info` comes from the registry, or simplify by making `ModeResolverService.resolve()` accept a direct `config_mode` value that each resolver exposes via a `default_mode` property.

**Note on argparse vs Click:** The current implementation uses `argparse`. The design document references "Click command skeleton" in TASK-001's title but the design text uses argparse. The scaffold uses argparse. Do NOT migrate to Click -- the inconsistency is in the task title only. Argparse is the correct implementation choice given the existing codebase.

**Security standards mapping:**
- T-06 mitigation M-03 (MUST implement -- DREAD 34)
- T-07 mitigation M-06 (SHOULD implement -- DREAD 28)
- OWASP ASVS V4.3.1 (Access Control): Strict mode prevents credential filter bypass by AI agents.
- OWASP ASVS V12.3.1 (File Execution): Evidence path must be sandboxed to project root.
- CWE-22 (Path Traversal): The evidence directory override is an unvalidated path write.
- NIST SSDF PS.1: Protect code from unauthorized access -- same principle applies to evidence file paths.

**Acceptance criteria:**
- `JERRY_STRICT_MODE=true` with `--no-filter` returns `ExitCode.STRICT_MODE_VIOLATION`.
- `JERRY_STRICT_MODE` unset with `--no-filter` logs a warning and continues.
- Evidence directory outside project root raises `ValueError` and does not create files.
- `ExitCode.STRICT_MODE_VIOLATION` must be defined (see TASK-009).
- Hardcoded `skills/rainbow/config/tool-exec.yaml` path removed.

---

### TASK-002: Tool Resolution (Port + Adapter + Router)

**Dependency:** TASK-001
**Estimate:** 3.5 hrs
**Current state:** Both `family_router.py` and `rainbow_tool_resolver.py` EXIST and are CORRECT. The router correctly implements explicit and auto-detect dispatch. The rainbow resolver correctly implements longest-prefix matching with wildcard support.

**Required changes:**

**T-04 awareness (logging):** `FamilyRouterService._resolve_auto()` silently uses the first match. Add logging to make auto-detection observable:

```python
import logging
logger = logging.getLogger(__name__)

# In _resolve_auto(), before return:
logger.info(
    "Auto-detected family '%s' for tool '%s'",
    resolver.__class__.__name__,
    tool_command,
)
```

This operationalizes mitigation M-04 (CI collision check is a separate CI concern; this covers the runtime observability requirement).

**T-11 information disclosure:** The `NotFoundError` raised in `_resolve_auto()` currently includes `searched families: {families}`. This is acceptable for a security tool framework where the family list is not sensitive; retain as-is but document the accepted risk.

**Security standards mapping:**
- T-04 partially mitigated (M-04 logging component)
- OWASP ASVS V7.2.1 (Log Content): Auto-detection decisions must be logged for audit.
- CWE-94 (Code Injection): `can_resolve()` probes a YAML-loaded resolver; allowlist from TASK-001D provides the outer defense.

**Acceptance criteria:**
- `FamilyRouterService` has exactly one class per H-10.
- `RainbowToolResolver` has exactly one class per H-10.
- Auto-detection logs which family claimed the tool at INFO level.
- `resolve()` with explicit family raises `NotFoundError` for unregistered families.
- `resolve()` in auto-detect mode raises `NotFoundError` when no family matches.
- Both classes have complete type hints and docstrings per H-11.

---

### TASK-003: Mode Resolver (with JERRY_TOOL_MODE)

**Dependency:** TASK-002
**Estimate:** 1 hr
**Current state:** EXISTS but REQUIRES REVISION -- `ModeResolverService.ENV_VAR_NAME = "RAINBOW_TOOL_MODE"` is hardcoded to the rainbow-family env var. The v2 design specifies a generic `JERRY_TOOL_MODE` as the primary env var with `RAINBOW_TOOL_MODE` as a backward-compatible fallback.

**Required changes:**

Replace the single `ENV_VAR_NAME` constant with an ordered tuple:

```python
_ENV_VAR_PRECEDENCE: tuple[str, ...] = (
    "JERRY_TOOL_MODE",       # Generic (highest precedence among env vars)
    "RAINBOW_TOOL_MODE",     # Rainbow backward-compat
)
```

In `resolve()`, replace the single env var check with iteration:

```python
# Level 2: Environment variables (in precedence order)
for env_var in self._ENV_VAR_PRECEDENCE:
    env_mode = os.environ.get(env_var)
    if env_mode is not None:
        return self._validate(env_mode, source=f"env var {env_var}")
```

**T-22 documentation:** The env var override of container isolation mode is BY DESIGN for user-controlled environments. Add a comment to `resolve()` explicitly acknowledging this: "Note: env var override is intentional per ADR-PROJ023-001 DR-005. AI agent invocation contexts should set JERRY_STRICT_MODE=true to prevent inadvertent local-mode override."

**Security standards mapping:**
- T-22 (BY DESIGN, documented risk)
- OWASP ASVS V14.5.1 (HTTP Method): Analogous principle -- explicit precedence ordering prevents unintended override.
- NIST CSF PR.AC-1: Mode selection is an access control decision; precedence must be deterministic.

**Acceptance criteria:**
- `JERRY_TOOL_MODE` takes precedence over `RAINBOW_TOOL_MODE` when both are set.
- `RAINBOW_TOOL_MODE` still works when `JERRY_TOOL_MODE` is not set (backward compat).
- Invalid mode values raise `ValueError` from either env var.
- T-22 risk comment present in source.

---

### TASK-006: Credential Filter with SecurityPolicy Extension (with M-02 Pattern Expansion)

**Dependency:** TASK-003
**Estimate:** 3.5 hrs (includes M-02 implementation and canary fixtures)
**Current state:** EXISTS but REQUIRES REVISION -- current implementation has 8 base patterns (4 CS + 4 CI). The threat model identifies T-03 (DREAD 36, HIGH) as having significant pattern gaps for modern token formats that are directly relevant to the AI CLI family.

**Required changes -- M-02 (MUST implement):**

Add the following patterns to `_BASE_CS_PATTERNS` (case-sensitive):

```python
# GitHub fine-grained personal access token (since 2022)
r"github_pat_[A-Za-z0-9_]{82}",
# JWT token header (base64-encoded {"alg":...} always starts with eyJ)
r"eyJ[A-Za-z0-9_\-]+\.[A-Za-z0-9_\-]+\.[A-Za-z0-9_\-]+",
# OpenAI project API key
r"sk-proj-[A-Za-z0-9_\-]{48,}",
# Anthropic API key
r"sk-ant-[A-Za-z0-9_\-]{48,}",
# Stripe live secret key
r"sk_live_[A-Za-z0-9]{24,}",
# Stripe live restricted key
r"rk_live_[A-Za-z0-9]{24,}",
# Slack bot token
r"xoxb-[0-9]{11}-[0-9]{11}-[A-Za-z0-9]{24}",
# Google AI API key (AIzaSy prefix)
r"AIzaSy[A-Za-z0-9_\-]{33}",
```

**Pattern count:** The test `test_base_pattern_count` in `test_credential_filter.py` asserts `pattern_count() == 8`. This test must be updated to assert `>= 8` or to the new exact count after M-02 additions.

**ReDoS review (T-16):** Before merging, each new pattern must be reviewed for catastrophic backtracking. The patterns above are designed with fixed-width suffixes and anchored prefixes to avoid ReDoS. Specifically:
- Avoid `[A-Za-z0-9]{20,}` without a prefix anchor on long quantifiers.
- The JWT pattern uses `+` quantifiers on character classes without alternation -- acceptable.
- Validate each pattern against a ReDoS checker (e.g., `safe-regex` pattern analysis) before merge.

**extend_patterns() validation (T-17):** Add pattern complexity validation to `extend_patterns()` to reject patterns with nested quantifiers. A simple safeguard:

```python
def _validate_pattern_complexity(self, pattern_str: str) -> None:
    """Reject patterns with nested quantifiers that risk ReDoS.

    Args:
        pattern_str: Pattern to validate.

    Raises:
        ValueError: If pattern contains nested quantifier constructs.
    """
    # Detect common ReDoS constructs: (a+)+ or (a*)* or similar
    if re.search(r"\([^)]+[*+]\)[*+]", pattern_str):
        msg = f"Pattern '{pattern_str[:50]}...' contains nested quantifiers (ReDoS risk)"
        raise ValueError(msg)
```

Call this in `extend_patterns()` before `re.compile()`.

**Security standards mapping:**
- T-03 mitigation M-02 (MUST implement -- DREAD 36)
- T-16 partial mitigation (ReDoS review)
- T-17 partial mitigation (nested quantifier check)
- OWASP ASVS V2.10.4 (Credential Protection): Credential redaction must cover modern API key formats.
- CWE-200 (Exposure of Sensitive Information): Filter must cover all known high-value secret formats.
- CWE-400 (Uncontrolled Resource Consumption): ReDoS prevention for regex patterns.

**Acceptance criteria:**
- `pattern_count()` returns 16 or more (8 original + 8 new minimum).
- Each of the 8 new patterns has at least one unit test in `test_credential_filter.py` using the canary fixture pattern (dynamically constructed strings to avoid hook detection).
- `extend_patterns()` raises `ValueError` for patterns containing nested quantifiers.
- All new patterns pass ReDoS review (no catastrophic backtracking on adversarial input).
- `test_cs_github_pat`, `test_cs_jwt_token`, `test_cs_openai_key`, `test_cs_anthropic_key`, `test_cs_stripe_live`, `test_cs_slack_bot`, `test_cs_google_ai` tests exist.

---

### TASK-007: Evidence Hasher

**Dependency:** TASK-003 (parallel with TASK-006)
**Estimate:** 1 hr
**Current state:** COMPLETE -- `EvidenceHasher` with `hash_string`, `hash_bytes`, `hash_file` is correct, H-10 and H-11 compliant, uses `hashlib.sha256` exclusively.

**Required changes:** None to the implementation.

**T-23 acceptance (hash-only integrity):** The threat model identifies T-23 (hash-only integrity without signatures, DREAD 23, LOW) and accepts it. Document this in the class docstring: "Note (T-23): SHA-256 hashes provide integrity detection only, not tamper evidence -- an attacker with filesystem write access can modify both file and hash. HMAC-based signatures are planned for a future enhancement (Phase 2 post-W12)."

**Security standards mapping:**
- OWASP ASVS V12.1.1 (File Upload): Evidence integrity via hash -- correct baseline.
- NIST SSDF PS.2: Provide a mechanism for verifying software release integrity -- SHA-256 satisfies this at Level 1.
- T-23 accepted risk, documented.

**Acceptance criteria:**
- T-23 risk comment added to class docstring.
- `hash_string()` correctly handles empty string (returns known SHA-256 of empty bytes).
- `hash_file()` raises `FileNotFoundError` for nonexistent path.
- All methods have type hints and docstrings per H-11.

---

### TASK-004: Local Executor (with M-07 and M-08)

**Dependency:** TASK-006
**Estimate:** 2 hrs (includes M-07 and M-08 implementation)
**Current state:** EXISTS but REQUIRES REVISION -- missing binary resolution validation (M-07) and stderr credential filtering (M-08).

**Required changes:**

**M-07 (SHOULD implement): Add `shutil.which()` check.**

In `execute()`, before the `subprocess.run()` call:

```python
import shutil
import logging
logger = logging.getLogger(__name__)

resolved_path = shutil.which(tool_command)
if resolved_path is not None:
    logger.info("Tool binary resolved: %s -> %s", tool_command, resolved_path)
else:
    logger.warning(
        "Tool binary not found via PATH: %s. "
        "Proceeding with subprocess execution attempt.",
        tool_command,
    )
```

The `shutil.which()` check is advisory: it logs the resolved path for audit but does not block execution when the binary is not on PATH (some tools use absolute paths). This makes T-02 (PATH manipulation) observable without breaking legitimate use cases.

**M-08 (SHOULD implement): Apply credential filter to stderr.**

In `execute()`, extend the filter application to cover stderr:

```python
if self._credential_filter is not None and not no_filter:
    stdout_result = self._credential_filter.filter_output(raw_stdout)
    stderr_result = self._credential_filter.filter_output(result.stderr)
    detected = stdout_result.detected or stderr_result.detected
    return ExecutionResult(
        exit_code=4 if detected else result.returncode,
        stdout=stdout_result.filtered_output,
        stderr=stderr_result.filtered_output,
        raw_stdout=raw_stdout,
        raw_stderr=result.stderr,   # Add raw_stderr field to ExecutionResult
        credential_detected=detected,
        filter_result=stdout_result if stdout_result.detected else stderr_result,
    )
```

**Note:** Adding `raw_stderr` to `ExecutionResult` is a breaking change to the dataclass. Update `ContainerExecutionResult` in TASK-005 symmetrically. Update `tool_exec_commands.py` accordingly.

**Security standards mapping:**
- T-02 mitigation M-07 (SHOULD implement -- DREAD 27)
- T-18 mitigation M-08 (SHOULD implement -- DREAD 25)
- OWASP ASVS V5.3.1 (Output Encoding): Credentials must not be returned to calling context regardless of output channel.
- CWE-532 (Insertion of Sensitive Information into Log File): stderr credential scanning prevents credential leakage via error channel.
- NIST CSF ID.AM-2: Log resolved binary paths as an asset management record.

**Acceptance criteria:**
- `shutil.which()` is called before `subprocess.run()`.
- Resolved binary path is logged at INFO level when found.
- Credential filter is applied to both stdout AND stderr.
- `ExecutionResult` has `raw_stderr` field.
- `FileNotFoundError` handling returns `ExitCode.UNKNOWN_TOOL`.

---

### TASK-005: Container Executor (with M-11)

**Dependency:** TASK-004 (parallel with TASK-004 after TASK-006)
**Estimate:** 2 hrs (includes M-11 compose path validation)
**Current state:** EXISTS but REQUIRES REVISION -- missing compose file path validation (M-11) and stderr filtering.

**Required changes:**

**M-11 (SHOULD implement): Validate compose file path.**

In `_build_command()` or in `execute()`, add a compose file path validation:

```python
if compose_file:
    compose_path = Path(compose_file).resolve()
    if self._project_root:
        project_root = Path(self._project_root).resolve()
        if not str(compose_path).startswith(str(project_root)):
            raise ValueError(
                f"Compose file '{compose_file}' is outside the project root. "
                f"Sandboxed to: {project_root}"
            )
```

**Stderr filtering:** Apply the same `raw_stderr` + filter pattern as TASK-004 for consistency. Both executors must filter both channels.

**T-20 accepted risk (exec_flags):** The `exec_flags` parameter that defaults to `["-T"]` is not exposed to CLI users. Add a docstring note: "Note (T-20): exec_flags is an internal API. Do NOT expose to user input; privileged flags like --privileged would enable container escape."

**Security standards mapping:**
- T-19 mitigation M-11 (SHOULD implement -- DREAD 25)
- T-20 accepted risk, documented
- OWASP ASVS V12.3.1 (File Execution): Compose file must be within repository boundaries.
- CWE-22 (Path Traversal): Compose file path injection via YAML is the specific risk.

**Acceptance criteria:**
- Compose file outside project root raises `ValueError`.
- T-20 risk comment present in `execute()` docstring.
- Stderr filtered alongside stdout.
- `ContainerExecutionResult` has `raw_stderr` field (symmetric with TASK-004).

---

### TASK-008: Engagement Initializer (with M-05 and M-10)

**Dependency:** TASK-004, TASK-005 (can start as soon as TASK-006 is done)
**Estimate:** 1 hr (includes M-05 and M-10 implementation)
**Current state:** EXISTS but REQUIRES REVISION -- `_validate_id()` uses a blocklist (`..`, `/`, `\`) instead of a character-class allowlist. Quarantine directory has default umask permissions.

**Required changes:**

**M-05 (SHOULD implement): Replace blocklist with allowlist in `_validate_id()`.**

Replace the current body of `_validate_id()`:

```python
def _validate_id(self, engagement_id: str) -> None:
    """Validate the engagement ID format against an allowlist.

    Permits only alphanumeric characters, hyphens, and underscores,
    starting with an alphanumeric character. This is a character-class
    allowlist (safer than a blocklist of specific bad characters).

    Args:
        engagement_id: The ID to validate.

    Raises:
        ValueError: If the ID is empty, blank, or contains disallowed characters.
    """
    import re as _re
    if not engagement_id or not engagement_id.strip():
        msg = "Engagement ID must not be empty"
        raise ValueError(msg)
    if not _re.match(r'^[a-zA-Z0-9][a-zA-Z0-9_-]*$', engagement_id):
        msg = (
            f"Engagement ID '{engagement_id}' contains disallowed characters. "
            f"Only alphanumeric characters, hyphens, and underscores are permitted, "
            f"starting with an alphanumeric character."
        )
        raise ValueError(msg)
```

**M-10 (SHOULD implement): Restrict quarantine directory permissions.**

In `initialize()`, after `quarantine_dir.mkdir(parents=True, exist_ok=True)`:

```python
import os
os.chmod(str(quarantine_dir), 0o700)
```

This restricts the quarantine directory to owner-only access, preventing other users on shared systems from reading quarantined credential-bearing output.

**Security standards mapping:**
- T-08 mitigation M-05 (SHOULD implement -- DREAD 28)
- T-21 mitigation M-10 (SHOULD implement -- DREAD 24)
- OWASP ASVS V5.1.3 (Input Validation): Allowlist is preferred over blocklist for input validation.
- OWASP ASVS V12.1.3 (File Storage): Quarantine directory must have appropriate permissions.
- CWE-22 (Path Traversal): Allowlist prevents shell metacharacter injection in directory names.
- CWE-732 (Incorrect Permission Assignment): Default umask may expose quarantine content.

**Acceptance criteria:**
- `_validate_id()` uses `re.match(r'^[a-zA-Z0-9][a-zA-Z0-9_-]*$', ...)` allowlist.
- IDs like `$(whoami)`, `` `id` ``, `..test`, `test/subdir` are all rejected.
- IDs like `eng-001`, `PROJ_2026_Q1`, `test123` are all accepted.
- Quarantine directory is created with `0o700` permissions.
- `os.chmod()` is called after `mkdir()`.

---

### TASK-009: Exit Code Handler

**Dependency:** TASK-008
**Estimate:** 1 hr
**Current state:** EXISTS but REQUIRES REVISION -- missing `FAMILY_NOT_FOUND=7`, `FAMILY_CONFIG_ERROR=8`, and `STRICT_MODE_VIOLATION` (currently named `MODE_UNSET=6`).

**Required changes:**

Update `ExitCode` enum to match the v2 design's full exit code contract:

```python
class ExitCode(IntEnum):
    SUCCESS = 0
    UNKNOWN_TOOL = 1
    TOOL_ERROR = 2
    CONTAINER_NOT_RUNNING = 3
    CREDENTIAL_DETECTED = 4
    ENGAGEMENT_NOT_INIT = 5
    STRICT_MODE_VIOLATION = 6   # Renamed from MODE_UNSET; covers: mode unset AND --no-filter in strict mode
    FAMILY_NOT_FOUND = 7         # NEW: explicit --family name not in registry
    FAMILY_CONFIG_ERROR = 8      # NEW: family config file invalid or missing
    # 10+ reserved for family-specific extensions
```

**Backward compatibility note:** `MODE_UNSET` (value 6) is renamed to `STRICT_MODE_VIOLATION`. The integer value is unchanged; only the symbolic name changes. Update all usages in `tool_exec_commands.py` to use `STRICT_MODE_VIOLATION`.

**UC-TOOLEXEC-001 alignment:** The use case specifies exit codes 0-8. All 9 values must be present in the enum.

**Security standards mapping:**
- OWASP ASVS V7.3.1 (Log Content): Exit codes must distinguish security failures (4, 5, 6) from tool errors (2) and configuration errors (7, 8).
- ADR-PROJ023-001 Behavioral Contract BC-01 through BC-09: Exit codes must align with the documented contract.

**Acceptance criteria:**
- All 9 exit code values (0-8) present in `ExitCode` enum.
- `STRICT_MODE_VIOLATION = 6` (renamed from `MODE_UNSET`).
- `FAMILY_NOT_FOUND = 7` present.
- `FAMILY_CONFIG_ERROR = 8` present.
- `test_exit_codes.py` updated to assert all 9 values.
- No duplicate integer values.

---

### TASK-010: Unit Tests and Port Contract Tests

**Dependency:** All preceding tasks (Wave 3 close-out)
**Estimate:** 4.5 hrs
**Current state:** 12 test files exist as SKELETONS with partial coverage. All scaffolded tests cover happy-path behavior. Security-specific tests (M-01, M-02, M-03 enforcement) are missing. Port contract tests are in `test_port_contract.py` but may not fully exercise the ABC contract.

**Test scope for Wave 3 additions (tests that do not yet exist):**

| Test File | New Test Cases Required |
|-----------|------------------------|
| `test_family_registry_loader.py` | M-01: module outside allowlist raises ValueError; allowlist check fires BEFORE import; empty module path rejected |
| `test_credential_filter.py` | M-02: all 8 new patterns detected; `extend_patterns()` rejects nested quantifiers; pattern count updated |
| `test_engagement_initializer.py` | M-05: `$(whoami)` rejected; `..test` rejected; `/subpath` rejected; `eng-001` accepted; M-10: quarantine dir has 0o700 permissions |
| `test_local_executor.py` | M-07: `shutil.which()` called; M-08: credential in stderr triggers detection |
| `test_container_executor.py` | M-11: compose file outside project root raises ValueError; T-20 flag is not exposed |
| `test_tool_exec_commands.py` | NEW FILE: M-03: `JERRY_STRICT_MODE=true` + `--no-filter` returns exit code 6; M-06: evidence dir outside project root raises ValueError |
| `test_exit_codes.py` | Updated: all 9 values present; FAMILY_NOT_FOUND=7; FAMILY_CONFIG_ERROR=8 |
| `test_mode_resolver.py` | JERRY_TOOL_MODE takes precedence over RAINBOW_TOOL_MODE; RAINBOW_TOOL_MODE still works alone |

**Coverage requirement (H-20):** 90% line coverage across `src/tool_exec/`. The existing scaffold tests provide a foundation; the new security-focused tests are required to close the coverage gap on error paths and validation branches.

**Port contract tests:** `test_port_contract.py` must verify that `RainbowToolResolver` satisfies all 4 abstract methods of `ToolFamilyResolverPort` and that passing a non-conforming object to `FamilyRegistryLoader` raises `ValueError`. This validates the interface contract at the type-system level.

**BDD feature file implementation:** `skills/rainbow/tests/bdd/test_tool_exec.feature` exists. The following scenarios must be implemented as step definitions:

| Scenario | BDD Scenario Name | Implements |
|----------|-------------------|-----------|
| Auto-detection with rainbow tool | "Given no family flag, tool is auto-detected from rainbow family" | UC-TOOLEXEC-001 Basic Flow steps 3-4 |
| Unknown tool returns exit 1 | "Given unknown tool command, exit code is 1" | Extension 3a |
| Engagement required for Zone 2 | "Given Zone 2 tool without engagement, exit code is 5" | Extension 7a |
| Strict mode blocks --no-filter | "Given JERRY_STRICT_MODE=true and --no-filter, exit code is 6" | AF-05 |
| Credential detected returns exit 4 | "Given tool output contains AWS key, exit code is 4" | Extension 9a |

**Security standards mapping:**
- H-20: 90% line coverage REQUIRED.
- NIST SSDF PO.3: Implement supporting toolchains (pytest-cov for coverage enforcement).
- OWASP ASVS V1.6 (Cryptographic Architecture): Tests must verify credential detection patterns.
- MS SDL Verification Phase: Security test cases must cover all identified threats.

**Acceptance criteria:**
- `uv run pytest tests/unit/tool_exec/ --cov=src/tool_exec --cov-fail-under=90` passes.
- All M-01, M-02, M-03, M-05, M-06, M-07, M-08, M-10, M-11 test cases present.
- Port contract tests exercise all 4 ABC methods.
- BDD step definitions implemented for all 5 scenarios listed above.
- No test uses a real credential value (all test strings are constructed via helper functions per the `_build_test_string()` pattern already in `test_credential_filter.py`).

---

## L1: Top-3 Threat Mitigation Integration

This section provides the cross-task view of the three MUST-implement mitigations from the threat model.

### M-01: importlib Allowlist (T-01, DREAD 38 -- CRITICAL)

| Task | Integration Point | Change Type |
|------|-------------------|-------------|
| TASK-001D | `FamilyRegistryLoader._load_resolver()` -- add allowlist check before `importlib.import_module()` | Implementation |
| TASK-010 | `test_family_registry_loader.py` -- add 3 tests: valid prefix accepted, invalid prefix rejected, invalid check fires before import | Testing |

**Implementation detail:**

The allowlist must use `str.startswith(tuple)` for efficient prefix checking. The current constant is:

```
_ALLOWED_MODULE_PREFIXES = ("src.tool_exec.infrastructure.adapters.",)
```

When a new family adapter is added in a future sprint, the maintainer must explicitly add its module prefix to this constant. This is an intentional friction point -- it prevents supply-chain injection via YAML without requiring code review of the YAML file itself.

**Verification:** The CI pipeline (`proj023-ci.yml`) must include a grep check that `importlib.import_module` is only called in `family_registry_loader.py` and that the allowlist check immediately precedes it.

---

### M-02: Credential Pattern Expansion (T-03, DREAD 36 -- HIGH)

| Task | Integration Point | Change Type |
|------|-------------------|-------------|
| TASK-006 | `CredentialFilterService._BASE_CS_PATTERNS` -- add 8 new patterns | Implementation |
| TASK-006 | `extend_patterns()` -- add nested quantifier validation | Implementation |
| TASK-010 | `test_credential_filter.py` -- add 8 new detection tests + `extend_patterns()` validation | Testing |
| TASK-010 | `tests/credential-fixtures/` -- add canary fixture strings for the 8 new patterns | Testing infrastructure |

**Pattern priority guidance:**

The three most relevant patterns for the immediate AI CLI family extension are:
1. `sk-ant-[A-Za-z0-9_\-]{48,}` -- Anthropic API keys (direct risk: jerry framework uses Claude Code)
2. `sk-proj-[A-Za-z0-9_\-]{48,}` -- OpenAI project API keys
3. `AIzaSy[A-Za-z0-9_\-]{33}` -- Google AI API keys

These three must be present before the AI CLI family is enabled. The remaining 5 (GitHub PAT, JWT, Stripe, Slack) must be present before any family config declares those platforms in its `credential_filter_patterns`.

---

### M-03: Strict Mode Enforcement (T-06, DREAD 34 -- HIGH)

| Task | Integration Point | Change Type |
|------|-------------------|-------------|
| TASK-001 | `tool_exec_commands.py` -- add `JERRY_STRICT_MODE` check after `no_filter` assignment | Implementation |
| TASK-001 | `tool_exec_commands.py` -- add `logging.warning()` for `--no-filter` when NOT in strict mode | Implementation |
| TASK-009 | `exit_codes.py` -- `STRICT_MODE_VIOLATION = 6` must be present | Implementation |
| TASK-010 | `test_tool_exec_commands.py` -- add tests: strict mode blocks `--no-filter`, permissive mode warns but continues | Testing |

**Environment variable name:** `JERRY_STRICT_MODE`. Value must be exactly the string `"true"` (case-sensitive). This is a convention inherited from the existing `RAINBOW_STRICT_MODE` approach. Document in comments: "Strict mode is activated by setting `JERRY_STRICT_MODE=true` in the environment. This is the standard pattern for CI/CD and AI agent invocation contexts where credential protection must be unconditional."

---

## L1: Coding Standards Checklist

The following checklist applies to ALL code written for TASK-001 through TASK-010. Reviewers must verify compliance during PR review.

### H-07: Architecture Layer Isolation

| Rule | Enforcement |
|------|-------------|
| Domain layer (`src/tool_exec/domain/`) MUST NOT import from `src/tool_exec/infrastructure/` | CI: `import linter` grep check for cross-layer imports |
| Domain layer MUST NOT import `subprocess`, `yaml`, `importlib`, or any I/O library | Manual PR review |
| Infrastructure adapters MAY import domain ports and value objects | Permitted direction |
| `tool_exec_commands.py` (interface layer) MAY import from all layers | Composition root |
| `TYPE_CHECKING` guards for forward references are permitted in domain layer | Use `if TYPE_CHECKING:` pattern as in existing code |

**Violations to watch for in this sprint:**
- `credential_filter.py` is domain layer -- it must not import from infrastructure.
- `engagement_initializer.py` is domain layer -- the `os.chmod()` call for M-10 is acceptable as `os` is a stdlib primitive, not an infrastructure dependency.
- Adding `shutil` to `local_executor.py` (M-07) is acceptable -- `local_executor.py` is infrastructure layer.

### H-10: One Class Per File

| Rule | Current Compliance | Sprint Compliance |
|------|-------------------|------------------|
| Each `.py` file in `src/tool_exec/` contains exactly one class | PASS (all scaffold files are compliant) | Maintain for all new files |
| `ExecutionResult` dataclass and `LocalExecutor` class in `local_executor.py` | EXCEPTION: dataclass helper co-located with its producing class is permitted per team convention | Document exception in PR |
| `CredentialMatch` and `FilterResult` dataclasses in `credential_filter.py` | EXCEPTION: same as above | Document exception in PR |

**Note on dataclass helpers:** The current pattern of co-locating result dataclasses with their producing service class (e.g., `ExecutionResult` in `local_executor.py`) is a documented exception to H-10. This is pragmatic for result types that have no consumers outside their producing class. However, `FilterResult` is consumed by both `LocalExecutor` and `ContainerExecutor`. If the filter result dataclass needs to move to its own file to satisfy strict H-10, a separate `src/tool_exec/domain/value_objects/filter_result.py` should be created.

### H-11: Type Hints and Docstrings

All public functions and methods MUST have:
1. Full type annotations on all parameters and return types.
2. A docstring with at minimum an Args section (for functions with parameters) and a Returns or Raises section.

| Specific enforcement for M-01 through M-11 code | Example |
|--------------------------------------------------|---------|
| `_validate_pattern_complexity()` in TASK-006 must have type hints | `def _validate_pattern_complexity(self, pattern_str: str) -> None:` |
| The M-03 strict mode check added inline in `handle_tool_exec()` is within an existing function -- inline comments suffice; no new function signature required | `# T-06 M-03: Strict mode enforcement -- reject --no-filter when JERRY_STRICT_MODE=true` |
| New `test_*` functions in TASK-010 must have docstrings | `"""Verifies that module path outside allowlist raises ValueError before import."""` |

### H-20: 90% Line Coverage

| Module | Current Est. Coverage | Target | Key Uncovered Paths |
|--------|-----------------------|--------|---------------------|
| `credential_filter.py` | ~85% | 90% | `extend_patterns()` with invalid pattern, multi-line output with credential |
| `family_registry_loader.py` | ~70% | 90% | Allowlist rejection (new code), malformed YAML paths |
| `engagement_initializer.py` | ~75% | 90% | Allowlist rejection (new regex), chmod failure path |
| `local_executor.py` | ~80% | 90% | `shutil.which()` not-found path, stderr credential detection |
| `container_executor.py` | ~75% | 90% | Compose file path validation (new code), stderr detection |
| `tool_exec_commands.py` | ~60% | 90% | Strict mode check (new code), evidence sandboxing (new code), all extension/alternative flows |

**Coverage enforcement:** Add to `pyproject.toml` under `[tool.pytest.ini_options]`:

```toml
addopts = "--cov=src/tool_exec --cov-fail-under=90 --cov-branch"
```

This enforces both line and branch coverage at 90%.

---

## L1: Testing Strategy

### Unit Tests (TASK-010)

Unit tests must use the existing test file structure in `tests/unit/tool_exec/`. One test class per test file, per H-10 convention for test files.

| Test File | Test Class | Coverage Focus |
|-----------|-----------|----------------|
| `test_security_policy.py` | `TestSecurityPolicy` | Validation, frozen dataclass, invalid network_access |
| `test_tool_family_info.py` | `TestToolFamilyInfo` | Frozen dataclass, all fields |
| `test_tool_resolution_entry.py` | `TestToolResolutionEntry` | Validation, zone enum values, invalid default_mode |
| `test_exit_codes.py` | `TestExitCodes` | All 9 values present, no duplicates, integer values correct |
| `test_family_registry_loader.py` | `TestFamilyRegistryLoader` | Parsing, allowlist (M-01), disabled families, malformed YAML |
| `test_family_router.py` | `TestFamilyRouterService` | Explicit dispatch, auto-detect, NotFoundError, logging |
| `test_mode_resolver.py` | `TestModeResolverService` | 4-level precedence, JERRY_TOOL_MODE, RAINBOW_TOOL_MODE, invalid mode |
| `test_credential_filter.py` | `TestCredentialFilterBasePatterns`, `TestCredentialFilterExtension` | 8 original + 8 new patterns, extend_patterns validation (M-02) |
| `test_evidence_hasher.py` | `TestEvidenceHasher` | All 3 hash methods, empty string, binary data |
| `test_engagement_initializer.py` | `TestEngagementInitializer` | Allowlist (M-05), directory creation, permissions (M-10), is_initialized |
| `test_local_executor.py` | `TestLocalExecutor` | shutil.which (M-07), stderr filter (M-08), FileNotFoundError, timeout |
| `test_container_executor.py` | `TestContainerExecutor` | Compose path validation (M-11), health_check, command construction |
| `test_port_contract.py` | `TestToolFamilyResolverPort` | RainbowToolResolver satisfies ABC, non-conforming resolver raises ValueError |
| `test_rainbow_tool_resolver.py` | `TestRainbowToolResolver` | Prefix matching, wildcard, can_resolve, security_policy zones |
| `test_tool_exec_commands.py` | `TestHandleToolExec` | NEW FILE: strict mode (M-03), evidence sandboxing (M-06), init engagement, health check |

### Integration Tests

Integration tests are NOT in scope for TASK-010. The following integration tests are recommended for a future sprint (STORY-W12-002 or a dedicated integration story):

| Scenario | Integration Surface | Why Deferred |
|----------|--------------------|--------------|
| Full pipeline with mock resolver | `handle_tool_exec()` + all domain services | Requires argparse namespace construction; out of scope for unit test budget |
| Container executor with real docker | `ContainerExecutor.health_check()` | Requires Docker daemon; CI-environment dependent |
| Registry loading real `tool_families.yaml` | `FamilyRegistryLoader.load()` against live file | Requires project root navigation; acceptable as a pytest fixture in a future integration suite |

### BDD Feature File Implementation

`skills/rainbow/tests/bdd/test_tool_exec.feature` must have step definitions implemented. The step implementation file should be created at `skills/rainbow/tests/bdd/steps/test_tool_exec_steps.py`.

**Required scenario implementations (5 scenarios):**

```gherkin
Feature: Jerry tool exec CLI -- auto-family detection

  Scenario: Auto-detection routes rainbow tool to rainbow family
    Given the family registry contains the rainbow family
    When the user runs "jerry tool exec nuclei"
    Then the rainbow resolver is called with "nuclei"
    And the exit code is 0

  Scenario: Unknown tool returns exit code 1
    Given no family can resolve the tool command
    When the user runs "jerry tool exec unknown-tool-xyz"
    Then the exit code is 1
    And the error message contains "Unknown tool"

  Scenario: Zone 2 tool without engagement returns exit code 5
    Given the rainbow family resolves "nmap" as Zone 2
    When the user runs "jerry tool exec nmap" without --engagement-id
    Then the exit code is 5
    And the error message contains "engagement"

  Scenario: --no-filter is blocked in strict mode
    Given JERRY_STRICT_MODE is set to "true"
    When the user runs "jerry tool exec nuclei --no-filter"
    Then the exit code is 6
    And the error message contains "FORBIDDEN in strict mode"

  Scenario: Credential in tool output triggers quarantine
    Given the local executor returns output containing an AWS access key
    When the credential filter processes the output
    Then the exit code is 4
    And the output contains "[CREDENTIAL-REDACTED]"
    And the raw output is written to the quarantine directory
```

**BDD test framework:** Use `pytest-bdd`. The step file at `skills/rainbow/tests/bdd/steps/test_tool_exec_steps.py` should use `@given`, `@when`, `@then` decorators and inject mock resolvers via pytest fixtures to avoid real subprocess calls.

---

## L1: Dependency Governance

### Runtime Dependencies

| Package | Current Version | Use in STORY-W12-001 | CVE Check | Decision |
|---------|-----------------|---------------------|-----------|----------|
| `pyyaml` | `^6.0.2` | `yaml.safe_load()` in registry loader and rainbow resolver | No known CVEs in 6.0.x for safe_load | APPROVED -- `safe_load` is the only permitted YAML loading function; `yaml.load()` without Loader is BANNED |
| stdlib: `subprocess` | Python 3.12+ | `subprocess.run()` with `shell=False` | N/A | APPROVED -- `shell=True` is BANNED |
| stdlib: `importlib` | Python 3.12+ | Dynamic module loading in `FamilyRegistryLoader` | N/A | CONDITIONALLY APPROVED -- allowlist (M-01) must be in place |
| stdlib: `re` | Python 3.12+ | Credential filter patterns | N/A | APPROVED -- new patterns must pass ReDoS review |
| stdlib: `shutil` | Python 3.12+ | `shutil.which()` in LocalExecutor (M-07) | N/A | APPROVED |
| stdlib: `hashlib` | Python 3.12+ | SHA-256 in EvidenceHasher | N/A | APPROVED |
| stdlib: `os` | Python 3.12+ | `os.chmod()` in EngagementInitializer (M-10), env var reads | N/A | APPROVED |

### Development Dependencies

| Package | Use | Risk |
|---------|-----|------|
| `pytest` | Test runner | LOW |
| `pytest-cov` | Coverage enforcement (H-20) | LOW |
| `pytest-bdd` | BDD step definitions | LOW |
| `unittest.mock` | Mocking subprocess, env vars in tests | LOW |

### Banned APIs

The following APIs are explicitly forbidden in all STORY-W12-001 code:

| API | Reason | Alternative |
|-----|--------|-------------|
| `subprocess.run(..., shell=True)` | Shell injection (CWE-78) | Always use list-based command construction |
| `yaml.load()` without explicit Loader | YAML deserialization attack (CWE-502) | Use `yaml.safe_load()` exclusively |
| `importlib.import_module()` without allowlist check | Arbitrary code execution (T-01) | Always precede with `_ALLOWED_MODULE_PREFIXES` check |
| `os.system()` | Shell injection | Use `subprocess.run()` with list |
| `eval()` | Arbitrary code execution | Forbidden without exception |
| `exec()` | Arbitrary code execution | Forbidden without exception |
| `open(..., 'w')` on user-supplied path without `Path.resolve()` check | Path traversal (CWE-22) | Always resolve and validate against project root |

---

## L2: SAMM Maturity Assessment

Assessment against OWASP SAMM v2.0, scoped to STORY-W12-001 work.

### Security Requirements (Governance)

| Activity | Current Level | Evidence | Target Level | Gap Action |
|----------|--------------|---------|--------------|-----------|
| SR-A (Software Requirements) | 1 | Threat model exists; behavioral contracts in ADR-PROJ023-001 | 2 | Convert top-5 threats to acceptance criteria in each task (done in this plan) |
| SR-B (Supplier Security) | 1 | `pyyaml` selected with CVE check; no formal SCA pipeline | 2 | Add `uv audit` to CI pipeline (`proj023-ci.yml`) |

### Threat Assessment (Design)

| Activity | Current Level | Evidence | Target Level | Gap Action |
|----------|--------------|---------|--------------|-----------|
| TA-A (Architecture Analysis) | 2 | Trust boundary diagram, 22-threat STRIDE model, attack trees for Tier 1 | 2 | Maintain; no gap |
| TA-B (Threat Modeling) | 2 | DREAD scoring, prioritized threat matrix, residual risk assessment | 2 | Maintain; no gap |

### Secure Build (Implementation)

| Activity | Current Level | Evidence | Target Level | Gap Action |
|----------|--------------|---------|--------------|-----------|
| SB-A (Build Process) | 1 | CI pipeline exists; no SAST configured | 2 | Add `ruff` with security rules to CI |
| SB-B (Software Dependencies) | 1 | `uv` used; no formal SCA or SBOM | 2 | Add `uv audit` + SBOM generation to CI |

### Security Testing (Verification)

| Activity | Current Level | Evidence | Target Level | Gap Action |
|----------|--------------|---------|--------------|-----------|
| ST-A (Scalable Baseline) | 1 | 12 unit test files scaffolded; coverage not enforced | 2 | Enforce 90% coverage in CI; TASK-010 delivers this |
| ST-B (Deep Understanding) | 1 | No security-specific test cases for T-01/T-03/T-06 | 2 | TASK-010 adds security test cases for all 3 mitigations |

**SAMM target trajectory:** The W12 sprint moves the Implementation and Verification practices from Level 1 to Level 2. Governance and Design are already at Level 2 due to the threat model and ADRs.

---

## L2: PR Review Criteria

Every PR for STORY-W12-001 tasks must pass the following checklist before merge. The reviewer is responsible for verifying each checkpoint.

### Standard Quality Checkpoints

| ID | Checkpoint | HARD Rule |
|----|-----------|-----------|
| PR-S-01 | All changed Python files have type hints on all public function signatures | H-11 |
| PR-S-02 | All changed Python files have docstrings on all public functions and methods | H-11 |
| PR-S-03 | No file contains more than one class (dataclass helpers co-located with their producer are documented exceptions) | H-10 |
| PR-S-04 | No domain layer file imports from infrastructure layer | H-07 |
| PR-S-05 | `uv run pytest tests/unit/tool_exec/ --cov=src/tool_exec --cov-fail-under=90` passes | H-20 |
| PR-S-06 | All new test functions have docstrings | H-11 |

### Security-Specific Checkpoints

| ID | Checkpoint | Threat | Task |
|----|-----------|--------|------|
| PR-SEC-01 | `importlib.import_module()` is preceded by allowlist check against `_ALLOWED_MODULE_PREFIXES` | T-01 M-01 | TASK-001D |
| PR-SEC-02 | No new call to `subprocess.run()` uses `shell=True` | T-02 | TASK-004, TASK-005 |
| PR-SEC-03 | New credential filter patterns have corresponding unit tests using constructed strings (no real secrets) | T-03 M-02 | TASK-006 |
| PR-SEC-04 | `JERRY_STRICT_MODE=true` test case exists and blocks `--no-filter` | T-06 M-03 | TASK-001 |
| PR-SEC-05 | `_validate_id()` uses allowlist regex, not blocklist | T-08 M-05 | TASK-008 |
| PR-SEC-06 | Evidence dir override is validated against project root using `Path.resolve()` | T-07 M-06 | TASK-001 |
| PR-SEC-07 | `shutil.which()` is called before `subprocess.run()` in LocalExecutor | T-02 M-07 | TASK-004 |
| PR-SEC-08 | Credential filter applied to stderr as well as stdout | T-18 M-08 | TASK-004, TASK-005 |
| PR-SEC-09 | Quarantine directory created with `os.chmod(0o700)` | T-21 M-10 | TASK-008 |
| PR-SEC-10 | No new call to `yaml.load()` -- only `yaml.safe_load()` permitted | T-01 related | All |
| PR-SEC-11 | New regex patterns reviewed for catastrophic backtracking before merge | T-16 | TASK-006 |

---

## L2: Standards Mapping

Cross-reference of implementation tasks to security standards frameworks.

### MS SDL Requirements Phase Mapping

| Task | MS SDL Practice | Mapping |
|------|-----------------|---------|
| TASK-001D (M-01 allowlist) | Threat Modeling -- Mitigation Implementation | T-01 identified in threat model, implemented in loader |
| TASK-006 (M-02 patterns) | Privacy + Security Architecture | Credential protection requirements from ADR-PROJ023-001 BC-07 |
| TASK-001 (M-03 strict mode) | Defense-in-Depth | Enforcement layer for credential filter bypass prevention |
| TASK-008 (M-05 allowlist) | Input Validation Requirements | Allowlist validation requirement per SDL guidance |
| TASK-010 (security tests) | Security Testing | Verification that threat mitigations function as specified |

### NIST SSDF Practice Mapping

| Task | SSDF Practice | Activity |
|------|---------------|---------|
| TASK-001D | PO.1.1 | Security requirements codified in loader implementation |
| TASK-006 | PO.1.2 | Credential protection requirements maintained as patterns |
| TASK-010 | PO.3.1 | pytest + pytest-cov as security testing toolchain |
| All tasks | PS.1.1 | Code protected via git branch + PR review workflow |
| TASK-007 + TASK-010 | PS.2.1 | SHA-256 integrity verification for evidence files |

### OWASP ASVS Cross-Reference

| Task | ASVS Control | Category |
|------|-------------|---------|
| TASK-001D (M-01) | V14.2.1 -- Dependency Verification | Allow only verified components via import allowlist |
| TASK-006 (M-02) | V2.10.4 -- Service Authentication | Protect API keys and service credentials in output |
| TASK-001 (M-03) | V4.3.1 -- Other Access Control | Administrative functions require appropriate protection |
| TASK-008 (M-05) | V5.1.3 -- Input Validation | Allowlist input validation for engagement IDs |
| TASK-001 (M-06) | V12.3.1 -- File Execution | Prevent path traversal in evidence directory writes |
| TASK-004 (M-07) | V2.2.5 -- General Authenticator | Log resolved binary paths as part of audit trail |
| TASK-004/005 (M-08) | V5.3.1 -- Output Encoding | Credential filtering applies to all output channels |
| TASK-008 (M-10) | V12.1.3 -- File Storage | Quarantine directory restricted to owner-only access |
| TASK-005 (M-11) | V12.3.1 -- File Execution | Compose file path must be within project boundaries |

### CWE Coverage Summary

| CWE | Description | Mitigated By |
|-----|-------------|-------------|
| CWE-20 | Improper Input Validation | TASK-001C (`__post_init__`), TASK-008 (M-05 allowlist) |
| CWE-22 | Path Traversal | TASK-001 (M-06), TASK-005 (M-11), TASK-008 (M-05) |
| CWE-78 | OS Command Injection | `shell=False` (existing), no new violations |
| CWE-200 | Exposure of Sensitive Information | TASK-006 (M-02 patterns), TASK-004/005 (M-08 stderr) |
| CWE-400 | Uncontrolled Resource Consumption | TASK-006 (M-16 ReDoS review) |
| CWE-502 | Deserialization of Untrusted Data | TASK-001D (M-01 allowlist) |
| CWE-532 | Insertion of Sensitive Information into Log | TASK-004/005 (M-08 stderr filter) |
| CWE-732 | Incorrect Permission Assignment | TASK-008 (M-10 chmod 0o700) |

---

*Implementation Plan Version: 1.0.0*
*Constitutional Compliance: P-001 (evidence-based -- all findings traced to source code line reads and threat model), P-002 (persisted to file), P-022 (scaffold assessment reflects actual file reads; no unverified claims)*
*Created: 2026-03-17*
*Agent: eng-lead (convergent mode, MS SDL Requirements Phase, NIST SSDF PO.1/PO.3/PS.1/PS.2)*
*SSDF Mapping: PO.1.1, PO.1.2, PO.3.1, PS.1.1, PS.2.1*
*SAMM Assessment: Governance SR-1→2, Implementation SB-1→2, Verification ST-1→2*
