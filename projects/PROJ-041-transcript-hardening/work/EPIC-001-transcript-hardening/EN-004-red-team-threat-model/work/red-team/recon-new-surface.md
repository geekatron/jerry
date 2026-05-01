# Recon Report — Planned New Attack Surface (TASK-177)

> **Engagement:** RT-PROJ041-001
> **Phase:** 1 — Paper engagement (design-intent recon only)
> **Authoring Agent:** red-recon
> **Date:** 2026-04-30
> **Status:** COMPLETE
> **Parent:** EN-004 / TASK-177
> **Methodology:** PTES Intelligence Gathering, ATT&CK TA0043, OWASP A03/A05/A08
> **Note:** All surfaces in this document are PLANNED, not yet implemented. Recon is based solely on design documents in `feat/PROJ-041-transcript-hardening`. No code exists to exploit.

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Engagement Context](#engagement-context) | Authorization and scope reminder |
| [Surface 6 — SubprocessSandbox](#surface-6--subprocesssandbox) | Bash command execution from JSON-supplied patterns |
| [Surface 7 — verify CLI Subcommand](#surface-7--verify-cli-subcommand) | jerry transcript verify entry point |
| [Surface 8 — update-anchors CLI Subcommand](#surface-8--update-anchors-cli-subcommand) | Atomic write and race condition risk |
| [Surface 9 — ts-formatter Post-Render Hook](#surface-9--ts-formatter-post-render-hook) | Process boundary between LLM agent and subprocess |
| [Surface 10 — CI Workflow Secrets Exposure](#surface-10--ci-workflow-secrets-exposure) | GitHub Actions secrets and injection risks |
| [Pre-Implementation Risk Summary](#pre-implementation-risk-summary) | Ranked risk register for eng-team |
| [Design Questions for eng-team](#design-questions-for-eng-team) | Specific questions EN-001 and EN-003 must resolve |
| [ATT&CK Technique Mapping](#attck-technique-mapping) | Technique IDs for anticipated risks |

---

## Engagement Context

This report covers the five PLANNED new attack surfaces from EN-004's Attack Surface Inventory. These surfaces correspond to FEAT-003 (Deterministic Substrate Validation). No implementation code exists for these surfaces in the branch. Recon is based on:

- `projects/PROJ-041-transcript-hardening/work/EPIC-001-transcript-hardening/FEAT-003-deterministic-validation/FEAT-003-deterministic-validation.md`
- `projects/PROJ-041-transcript-hardening/work/EPIC-001-transcript-hardening/FEAT-003-deterministic-validation/EN-001-ddd-scaffolding/EN-001-ddd-scaffolding.md`
- `projects/PROJ-041-transcript-hardening/work/EPIC-001-transcript-hardening/FEAT-003-deterministic-validation/EN-003-subprocess-sandbox/EN-003-subprocess-sandbox.md`
- The author's prototype gist (referenced in FEAT-003 and EN-003; cited by name only per scope; not fetchable in Phase 1)
- Existing CI workflow files at `.github/workflows/`

All paths are repo-relative per Rule P-9 (`architecture-validation-forbidden-patterns`).

---

## Surface 6 — SubprocessSandbox

### Design Intent

EN-003 establishes that the author's prototype runs `subprocess.run(["bash", "-c", pattern], cwd=str(packet_root))` where `pattern` is read from `_anchors.json`'s `audit_breakdown.per_bucket_derivation[bucket].derivation_grep_pattern` field. This is the core validation mechanism: each ADR-007 rule uses a shell command (grep, wc, find) to mechanically verify declared counts against packet content.

FEAT-003 specifies that these patterns will be executed via a `SubprocessSandbox` port and adapter, living at:
- Port: `src/jerry/transcript/validation/application/ports.py` (`SubprocessSandbox` Protocol)
- Adapter: `src/jerry/transcript/validation/infrastructure/subprocess_sandbox.py`

The sandbox design prescribes: command allowlist (grep/wc/find), argument validation against a permissive grammar, `cwd` forced to `packet_root`, path traversal guard via `pathlib.Path.resolve()`, symlink rejection, 5-second default timeout, env var stripping to `PATH=/usr/bin:/bin`, output size limit of 1MB.

### Anticipated Entry Points

| Entry Point | Data Flow |
|-------------|-----------|
| `_anchors.json` `derivation_grep_pattern` field | Attacker-controlled VTT content → ts-formatter → `_anchors.json` → `SubprocessSandboxAdapter.run(pattern)` |
| CLI: `jerry transcript verify <packet>` | User-supplied packet directory path |
| CLI: `jerry transcript update-anchors <packet>` | User-supplied packet directory path |
| ts-formatter post-render hook | ts-formatter agent calls `verify` at exit via process boundary |

The full data flow for the most dangerous path is:
```
Attacker-supplied VTT content
  → ts-parser (Python): attacker controls segment text
  → ts-extractor (LLM): attacker-controlled text becomes entity text
  → ts-formatter (LLM): entity text written to _anchors.json derivation_grep_pattern
  → SubprocessSandboxAdapter: pattern executed as shell command
```

### Trust Boundary Mismatches

1. **`_anchors.json` is written by an LLM (ts-formatter):** ts-formatter is an LLM agent that will produce the `derivation_grep_pattern` fields in `_anchors.json`. LLM agents do not provide formal security guarantees about their output. Even if the sandbox performs argument validation, the validation logic must assume the pattern can be adversarially crafted — because a context-rotted or prompt-injected ts-formatter could write an adversarial pattern field.

2. **Bucket derivation patterns are currently under-specified in the design:** EN-003's sandbox design specifies a command allowlist (`grep`, `wc`, `find`) and prohibits shell metacharacters (`;`, `&&`, `||`, backticks, `$()`, `>`, `<`, `|`). However, the "permissive grammar" for valid pattern arguments is described abstractly ("command + flags from allowlist + literal-string args") without a formal grammar definition. This leaves implementation ambiguity about which flag combinations are safe.

3. **`cwd` enforcement depends on reliable packet root resolution:** The sandbox design enforces `cwd=packet_root`. If the `packet_root` itself is attacker-influenced (e.g., via a symlink at the packet directory level, or via a `--output-dir ..` traversal in a prior stage), the `cwd` enforcement boundary is undermined.

4. **Output size limit set at 1MB but not yet formalized:** EN-003 specifies "reject output > 1MB (defense against `find /` returning gigabytes)." This limit is a design decision but does not yet have a unit test or acceptance criterion confirming it is enforced before memory pressure occurs.

### Pre-Implementation Risks

1. **[CRITICAL] Shell injection via LLM-generated pattern field:** The most severe risk. If `_anchors.json.audit_breakdown.per_bucket_derivation.derivation_grep_pattern` is not exhaustively validated before execution, any LLM-generated string containing shell metacharacters that pass the argument validator could achieve arbitrary command execution in the validator's process environment. EN-003's design acknowledges this as the primary threat.

2. **[HIGH] Allowlist bypass via allowed-command chain:** Even with `grep`, `wc`, and `find` allowlisted, combinations of these commands with unusual flags may achieve unintended effects. For example: `find . -exec sh -c '...' {} \;` uses an allowlisted command (`find`) with `-exec` to spawn a shell. The argument validator must explicitly prohibit `-exec`, `-execdir`, and similar flag forms.

3. **[HIGH] Path traversal via argument normalization:** `pathlib.Path.resolve()` resolves symlinks. If a symlink inside `packet_root` points outside `packet_root`, `is_relative_to(packet_root)` check passes for the symlink itself but not for the resolved target. The design specifies `lstat` first to detect symlinks, but the sequencing of `lstat` → `resolve` → `is_relative_to` must be implemented correctly to avoid TOCTOU.

4. **[MEDIUM] Env var inheritance before stripping:** The design specifies stripping all env vars except `PATH`. If any sensitive env vars are present at validator process startup (e.g., `ANTHROPIC_API_KEY`, `GITHUB_TOKEN`), they must be stripped before `subprocess.Popen()` is called, not after. Python's `os.environ` mutation is process-global; incorrect stripping timing could expose secrets to the subprocess.

5. **[MEDIUM] Timeout kill does not guarantee cleanup:** A `subprocess` with a 5-second timeout that is `SIGTERM`-killed may spawn child processes before dying. The design specifies "hard kill at 60s" but does not address child process cleanup (`os.killpg` vs `process.kill()` distinction on POSIX).

### Design Questions for eng-team

See [Design Questions for eng-team](#design-questions-for-eng-team) below.

---

## Surface 7 — verify CLI Subcommand

### Design Intent

`jerry transcript verify <packet>` (STORY-007) is a CLI subcommand that runs all 17 ADR-007 validation rules against a packet directory. It calls `PacketValidator.run()` from the application layer, which orchestrates rule execution through the `RuleEngine` port. The interface layer lives at `src/jerry/transcript/validation/interface/cli.py`.

The subcommand accepts a `<packet>` positional argument (a filesystem path to a packet directory) and exits with code 0 (all rules pass) or 1 (any rule fails), emitting structured JSON + Markdown report output.

### Anticipated Entry Points

| Entry Point | Data Flow |
|-------------|-----------|
| CLI positional argument `<packet>` | User-supplied filesystem path passed to `PacketValidator` |
| Packet directory contents (all 8 `.md` files + `_anchors.json`) | Read by validators through `FileReader` adapter |
| `_anchors.json` derivation patterns (subset of rules) | Passed to `SubprocessSandbox` (see Surface 6) |

### Trust Boundary Mismatches

1. **No stated path validation on `<packet>` argument:** The design documents do not specify whether the `<packet>` CLI argument is validated (e.g., canonicalized, checked to be a directory, checked to be within a project root). A user could supply `../../etc` or a symlinked directory.

2. **CLI runs with user process credentials:** `jerry transcript verify` runs as the invoking user. No privilege isolation is defined in the design. If the validator is later integrated into CI (STORY-012), it runs with CI runner credentials. If a compromised packet can force the validator to read outside the packet directory, it does so with the CI runner's permissions.

3. **Report output destination not specified:** FEAT-003's acceptance criteria state the validator "emits structured JSON + Markdown report output and exit code 0/1" but do not specify where the report is written. If the output path is derived from the input `<packet>` path without validation, a traversal in `<packet>` could direct the report to an unintended location.

### Pre-Implementation Risks

1. **[HIGH] Path traversal on `<packet>` argument:** Without canonicalization and containment checks on the input path, `jerry transcript verify <path>` is a potential path traversal vector. This is especially relevant in CI where the tool may run on untrusted PR-submitted packet directories.

2. **[MEDIUM] Resource exhaustion via large packet:** A crafted packet with thousands of anchor entries in `_anchors.json` or an extremely large `02-transcript.md` could cause the validator to spend excessive time or memory during rule evaluation. No resource limits are defined for the `verify` subcommand itself (beyond the subprocess timeout inside `SubprocessSandbox`).

3. **[MEDIUM] Rule engine error handling gap:** `PacketValidator.run()` is planned to orchestrate rule execution and return `ValidationResult` objects. The design does not specify what happens when a rule implementation raises an unexpected exception rather than returning a fail result. An unhandled exception in one rule could abort the entire validation run and return a misleading exit code.

---

## Surface 8 — update-anchors CLI Subcommand

### Design Intent

`jerry transcript update-anchors <packet>` (STORY-008) is a CLI subcommand that recomputes all declared counts in `_anchors.json` by walking the actual packet files — replacing the current LLM-maintained statistics with mechanically correct values. FEAT-003 calls this "declared counts are cache-of-walked-truth, never hand-maintained."

The service (`UpdateAnchorsService` in `src/jerry/transcript/validation/application/update_anchors.py`) reads all packet `.md` files, recount entities, and writes back to `_anchors.json` atomically.

### Anticipated Entry Points

| Entry Point | Data Flow |
|-------------|-----------|
| CLI argument `<packet>` | User-supplied packet directory path |
| All 8 packet `.md` files | Read by `UpdateAnchorsService` |
| `_anchors.json` (current state) | Read and overwritten atomically |
| Atomic write target (temp file + rename) | `_anchors.json` replacement mechanism |

### Trust Boundary Mismatches

1. **Atomic write mechanism not yet specified:** FEAT-003's acceptance criteria state that `update-anchors` writes back to `_anchors.json` using an atomic write. The EN-001 scaffolding describes the operation as `UpdateAnchorsService` but does not specify the atomic write pattern (temp file + rename vs. file locking vs. other). Different platforms (macOS, Linux, Windows) have different atomicity guarantees for `os.rename()`. The design gap is: which platform guarantees are relied upon, and is the temp file created in the same directory as `_anchors.json` (required for same-filesystem atomic rename)?

2. **Concurrent `update-anchors` invocations:** If two `update-anchors` processes run concurrently against the same packet (e.g., ts-formatter hook + manual CLI call), both may read the same initial state, recompute, and write — last writer wins with no conflict detection. This is a lost-update race condition.

3. **ts-formatter hook integration creates a TOCTOU window:** STORY-010 wires `update-anchors` into the ts-formatter write pipeline. ts-formatter writes all 8 packet files, then calls `update-anchors`. During the window between the last file write and the `update-anchors` call, a concurrent process could modify a packet file, causing `update-anchors` to produce counts based on partially different files than ts-formatter wrote.

4. **No rollback defined for partial-write failure:** If `update-anchors` fails partway through (e.g., after writing the temp file but before the rename, or after the rename but before fsyncing), the on-disk state may be inconsistent. The design does not specify a rollback or recovery mechanism.

### Pre-Implementation Risks

1. **[HIGH] Race condition between concurrent update-anchors invocations:** The design acknowledges atomic write but does not define mutual exclusion between concurrent invocations. On multi-core systems or in CI parallelism, this is a realistic failure mode.

2. **[HIGH] TOCTOU window in ts-formatter post-render hook:** The sequence `ts-formatter writes files → hook calls update-anchors → update-anchors reads files` is non-atomic at the filesystem level. The TOCTOU window is the gap between ts-formatter completing all writes and `update-anchors` starting to read. On NFS or network filesystems (e.g., GitHub Actions runners on shared storage), this window may be longer than expected.

3. **[MEDIUM] Temp-file residue on crash:** If `update-anchors` crashes after creating a temp file but before renaming, the temp file persists. If temp files accumulate (e.g., repeated crash-retry loops in CI), the packet directory becomes cluttered with partial-write artifacts.

4. **[MEDIUM] `_anchors.json` schema version compatibility:** The `update-anchors` service rewrites `_anchors.json`. If the rewritten JSON omits fields present in the original (e.g., future schema fields not yet known to the service), the result is a schema-downgrade. A schema version field should be preserved or explicitly migrated.

---

## Surface 9 — ts-formatter Post-Render Hook

### Design Intent

STORY-009 wires `jerry transcript verify` into `ts-formatter` as a post-render hook: after ts-formatter writes all 8 packet files, it calls `verify` before reporting completion. This creates a process boundary where the LLM agent (ts-formatter) calls a subprocess (the CLI validator).

### Anticipated Entry Points

| Entry Point | Data Flow |
|-------------|-----------|
| ts-formatter Write-tool output (the 8 packet files) | Written to packet directory before hook runs |
| Hook invocation mechanism | ts-formatter agent calls the verify subprocess via Bash tool or CLI |
| `verify` subprocess stdout/stderr | Returned to ts-formatter agent context |
| Hook exit code | 0 = proceed, 1 = validation failed |

### Trust Boundary Mismatches

1. **Process boundary is unclear from agent definition:** ts-formatter is an LLM agent with allowed tools: `Read`, `Write`, `Glob`. The Bash tool is NOT in ts-formatter's allowed-tools list (`tools: Read, Write, Glob` per `skills/transcript/agents/ts-formatter.md` YAML frontmatter). This means ts-formatter cannot call `jerry transcript verify` via a Bash tool invocation directly. STORY-009's design must resolve: how does ts-formatter invoke the hook?

   Options (each with different trust implications):
   - Add `Bash` to ts-formatter's allowed tools (expands tool surface significantly).
   - Have the orchestrator (ts-parser or SKILL.md MAIN CONTEXT) call `verify` after ts-formatter returns.
   - Use a post-agent hook mechanism in Claude Code.

2. **Validator output fed back into LLM context:** If `verify` stdout is returned to the ts-formatter LLM context (e.g., as Bash tool output), the validation report becomes part of the LLM's context window. A crafted packet whose validation report contains LLM instruction text could attempt to manipulate ts-formatter's subsequent behavior.

3. **Hook failure handling not specified:** If `verify` returns exit code 1 (validation failed), ts-formatter is expected to "report" this. The design does not specify what ts-formatter should do: retry formatting, raise an error to the orchestrator, or simply include the failure in its output state. An ambiguous failure mode could cause silent validation failure if the LLM interprets a failed hook as non-critical.

4. **Privilege context of the hook:** The hook runs in the same process context as ts-formatter (or the orchestrator). If the LLM agent has been given broad tool permissions in a particular invocation (e.g., `permissionMode: bypassPermissions`), the subprocess spawned by the hook inherits that context.

### Pre-Implementation Risks

1. **[CRITICAL] Architecture ambiguity: ts-formatter lacks Bash tool:** ts-formatter's current allowed-tools list excludes `Bash`. If STORY-009 adds `Bash` to ts-formatter to enable hook invocation, it significantly expands the agent's capability surface and creates a general-purpose shell execution path from an LLM agent that was previously read-write-only. This is a high-risk architectural decision that must be resolved explicitly by eng-architect (TASK-051).

2. **[HIGH] Validator stdout as LLM prompt injection vector:** Validation report content returned to the LLM context could contain attacker-controlled text (from the packet's contents). A validation failure message like `FAIL: Anchor seg-001 referenced in 02-transcript.md line 15 does not match _anchors.json. Recommendation: [injected text]` would place attacker content back into the LLM's prompt.

3. **[MEDIUM] Hook invocation ordering with update-anchors:** STORY-009 (`verify` hook) and STORY-010 (`update-anchors` hook) both run post-render. The ordering between them matters: `update-anchors` must run before `verify` (so that `verify` checks the mechanically correct `_anchors.json`, not the stale LLM-generated one). The design does not currently specify this ordering constraint.

---

## Surface 10 — CI Workflow Secrets Exposure

### Design Intent

STORY-012 wires the validator into CI: the GitHub Actions CI workflow runs `jerry transcript verify` against golden packets on every PR. This creates a new code path that runs the validator (including `SubprocessSandbox`) inside GitHub Actions runners.

The existing CI configuration (`.github/workflows/ci.yml`) uses:
- `permissions: contents: read` on the main CI workflow (minimal permissions).
- Pinned action versions by commit hash (e.g., `actions/checkout@de0fac2e4500dabe0009e67214ff5f5447ce83dd`).
- An env-var pattern to prevent PR title injection (`CLCHK-001` comment in changelog-check step).

The PAT monitor workflow (`.github/workflows/pat-monitor.yml`) uses `secrets.VERSION_BUMP_PAT` for authenticated API calls. The version-bump workflow uses `secrets.CODECOV_TOKEN`.

### Anticipated Entry Points

| Entry Point | Data Flow |
|-------------|-----------|
| PR-submitted golden packet files | Committed to branch; `verify` runs against them in CI |
| CI runner environment | `SubprocessSandbox` runs inside CI runner process |
| `secrets.CODECOV_TOKEN` | Used in `test-uv` job for coverage upload |
| `secrets.VERSION_BUMP_PAT` | Used in `version-bump.yml` for tag creation |
| New CI step for validator | Yet-to-be-defined step running `jerry transcript verify` |

### Trust Boundary Mismatches

1. **Attacker-controlled packets run through SubprocessSandbox in CI:** STORY-012 runs the validator against golden packets. On a PR, the golden packets are PR-submitted files. A malicious PR could include a crafted `_anchors.json` with adversarial `derivation_grep_pattern` values. The `SubprocessSandbox` adapter is the only defense. If the sandbox has a bypass, the PR's patterns execute with CI runner permissions.

2. **CI secrets are not scoped to specific jobs:** The existing CI workflow shows `secrets.CODECOV_TOKEN` referenced in the `test-uv` job. If STORY-012 adds a validator job that runs in the same workflow, and the job step has an unintended subprocess execution (via sandbox bypass), the validator subprocess could potentially read secrets from the process environment. The current `permissions: contents: read` setting does not restrict `secrets` access within the job.

3. **No existing `permissions` scoping for a validator job:** The current CI `permissions` block is `contents: read` at the workflow level. A new validator job that calls `SubprocessSandbox` should be reviewed to confirm it does not require elevated permissions and that its step-level permissions are explicitly minimized.

4. **`pat-monitor.yml` uses `issues: write` permission:** The PAT monitor creates GitHub Issues. This is a separate workflow but demonstrates that the repo has workflows with elevated permissions. If the validator CI job is added to a workflow that includes permission escalation paths, the boundary matters.

### Pre-Implementation Risks

1. **[CRITICAL] Sandbox bypass in CI = arbitrary code execution with runner permissions:** A successful `SubprocessSandbox` bypass via an attacker-controlled `derivation_grep_pattern` in a PR-submitted packet would yield code execution on the GitHub Actions runner. The runner has access to `GITHUB_TOKEN` (at minimum) and any repo secrets provisioned to the workflow. This is the top-priority risk for Phase 4 validation.

2. **[HIGH] PR-submitted golden packets as attack vector:** Unlike tests that run against hardcoded test fixtures, running the validator against PR-submitted content creates an adversarial input path in CI. The design of STORY-012 should specify whether `verify` runs against:
   - Hardcoded golden packets only (lower risk — not PR-controlled),
   - PR-submitted packet files (higher risk — attacker-controlled).

3. **[MEDIUM] Workflow-level `permissions` may be insufficient:** The current `permissions: contents: read` is set at the workflow level in ci.yml. GITHUB_TOKEN permissions are additive per job in GitHub Actions. If STORY-012 adds a new workflow or job requiring `contents: write` (e.g., to post validation summaries), the overall permission footprint increases.

4. **[MEDIUM] Runner environment may expose sensitive env vars before SubprocessSandbox strips them:** GitHub Actions automatically injects many env vars into the runner environment (`GITHUB_TOKEN`, `RUNNER_TEMP`, `ACTIONS_RUNTIME_TOKEN`, etc.). The `SubprocessSandbox` design strips env vars to `PATH=/usr/bin:/bin` before executing the subprocess. However, the stripping must occur inside the `subprocess.Popen()` call (via the `env` parameter), not by modifying `os.environ`. If the implementation uses `os.environ.update()` or `del os.environ[...]` instead of passing `env={...}` to `Popen`, the stripping is incomplete.

---

## Pre-Implementation Risk Summary

| Rank | Surface | Risk | Severity | Phase 4 Target |
|------|---------|------|----------|----------------|
| 1 | 6 (SubprocessSandbox) | Shell injection via LLM-generated derivation_grep_pattern | CRITICAL | Yes — bypass class 1 |
| 2 | 9 (ts-formatter hook) | Architecture ambiguity: Bash tool expansion onto LLM agent | CRITICAL | Architectural resolution before Phase 4 |
| 3 | 10 (CI secrets) | Sandbox bypass in CI = runner code execution | CRITICAL | Yes — bypass class 1 in CI context |
| 4 | 6 (SubprocessSandbox) | Allowlist bypass via `-exec` flag or shell flag combinations | HIGH | Yes — bypass class 2 |
| 5 | 6 (SubprocessSandbox) | Path traversal via symlink + TOCTOU in resolve() | HIGH | Yes — bypass class 3 |
| 6 | 7 (verify CLI) | Path traversal on `<packet>` argument | HIGH | Yes — verify surface probe |
| 7 | 8 (update-anchors) | Race condition between concurrent invocations | HIGH | Yes — Phase 4 atomic-write probe |
| 8 | 9 (ts-formatter hook) | Validator stdout as LLM prompt injection vector | HIGH | Yes — prompt injection probe |
| 9 | 6 (SubprocessSandbox) | Env var inheritance before stripping | MEDIUM | Yes — bypass class 4 (env poisoning) |
| 10 | 8 (update-anchors) | TOCTOU window in post-render hook integration | MEDIUM | Yes — Phase 4 race probe |

---

## Design Questions for eng-team

The following questions must be answered by EN-001 (DDD scaffolding) and EN-003 (SubprocessSandbox) before implementation begins. Each question maps to a specific pre-implementation risk.

### For EN-003 (SubprocessSandbox)

**Q1 — Formal grammar for allowed patterns:**
The EN-003 design states argument validation uses "a permissive grammar: command + flags from allowlist + literal-string args." What is the formal grammar? Specifically: which flags are permitted for `grep`, `wc`, and `find`? Is `-exec` explicitly prohibited for `find`? Is `-P` (pipe) prohibited for `grep`? The grammar must be machine-verifiable, not prose.

**Q2 — Symlink handling sequencing:**
The design specifies `lstat` first to detect symlinks, then `resolve()` + `is_relative_to()`. What is the exact sequencing? If `lstat` shows a symlink, is the path rejected immediately, or does it attempt to verify where the symlink resolves to? TOCTOU between `lstat` and subsequent `resolve()` calls must be addressed.

**Q3 — Subprocess env stripping implementation:**
Does `SubprocessSandboxAdapter` pass `env={"PATH": "/usr/bin:/bin"}` directly to `subprocess.Popen()` (correct), or does it modify `os.environ` (incorrect — process-global, incomplete)? This implementation choice must be specified explicitly in the acceptance criteria for TASK-069.

**Q4 — Output size limit enforcement timing:**
The 1MB output size limit: is it enforced by setting `stdout=subprocess.PIPE` with `communicate()` (which buffers all output in memory before checking size), or by streaming with `read(1024*1024+1)` (which stops reading at the limit)? Buffering all output defeats the purpose of the limit for memory exhaustion attacks.

**Q5 — Child process cleanup on timeout:**
When the wall-clock timeout fires and `process.kill()` is called, does the implementation also kill child processes? On POSIX, use `os.killpg(os.getpgid(process.pid), signal.SIGKILL)` if the subprocess may spawn children (e.g., via `find -exec sh`). Specify which kill mechanism is used and why.

### For EN-001 (DDD scaffolding)

**Q6 — ts-formatter post-render hook architecture:**
ts-formatter's current allowed-tools are `Read, Write, Glob` — `Bash` is excluded. STORY-009 requires ts-formatter to invoke `jerry transcript verify` post-render. Three options exist: (A) add `Bash` to ts-formatter (expands tool surface), (B) orchestrator calls `verify` after ts-formatter returns (no tool change but hook is not ts-formatter's responsibility), (C) use a Claude Code lifecycle hook (post-agent event, if available). Which option does EN-001 recommend? This is a security-critical architectural decision that must be captured in DEC-006 or equivalent.

**Q7 — `update-anchors` concurrency model:**
What concurrency model does `UpdateAnchorsService` use to prevent lost-update races? Options include: advisory file locking (`fcntl.flock`), PID files, atomic rename from a uniquely-named temp file, or explicit "no concurrent invocation" constraint documented in CLI help. Each option has different guarantees across macOS/Linux/Windows (the test matrix in ci.yml shows all three OS).

**Q8 — `_anchors.json` schema version preservation:**
When `update-anchors` rewrites `_anchors.json`, does it preserve the `version` field and any fields it does not understand (forward-compatibility)? Specify in the `UpdateAnchorsService` acceptance criteria (TASK-054) what the preservation policy is.

**Q9 — Validator CLI output destination:**
Where does `jerry transcript verify` write its report (JSON + Markdown)? Options: (A) alongside the packet (`<packet>/validation-report.{json,md}`), (B) to stdout/stderr only, (C) to a caller-specified path. If option A, the output path is derived from the input path, creating a traversal risk if `<packet>` is not validated. Specify in STORY-007 acceptance criteria.

**Q10 — Golden packet test fixture control in CI:**
STORY-012 runs the validator in CI. Should `verify` run against only hardcoded committed golden packets (`skills/transcript/test_data/expected_output/`), or against any PR-submitted packet directory? If against PR-submitted files, the CI job becomes a SubprocessSandbox evaluation target for any PR author. Recommend: restrict to committed golden packets only for CI; provide a separate dev-mode flag for arbitrary packet validation.

---

## ATT&CK Technique Mapping

| Surface | Technique ID | Technique Name | Applicability |
|---------|-------------|----------------|---------------|
| 6 (SubprocessSandbox) | T1059.004 | Command and Scripting Interpreter: Unix Shell | Shell injection via derivation_grep_pattern |
| 6 (SubprocessSandbox) | T1083 | File and Directory Discovery | `find` allowlisted command used for information disclosure |
| 7 (verify CLI) | T1083 | File and Directory Discovery | Path traversal on `<packet>` argument |
| 8 (update-anchors) | T1565.001 | Stored Data Manipulation | Lost-update race overwrites _anchors.json |
| 9 (ts-formatter hook) | T1598 | Phishing for Information | Validator stdout as LLM prompt injection vector |
| 10 (CI secrets) | T1552.001 | Credentials In Files | Env var secrets accessible to sandboxed subprocess if stripping fails |
| 10 (CI secrets) | T1195 | Supply Chain Compromise | Malicious PR-submitted packet → sandbox bypass → CI code execution |

---

*Report Version: 1.0.0*
*Engagement: RT-PROJ041-001 Phase 1*
*Authoring Agent: red-recon*
*Constitutional Compliance: P-001 (evidence-based), P-002 (persisted), P-003 (no subagents), P-022 (no deception)*
*Scope Basis: EN-004 Attack Surface Inventory, surfaces 6-10 (New/Planned)*
*Design intent sourced from: FEAT-003, EN-001, EN-003 (this branch only)*
