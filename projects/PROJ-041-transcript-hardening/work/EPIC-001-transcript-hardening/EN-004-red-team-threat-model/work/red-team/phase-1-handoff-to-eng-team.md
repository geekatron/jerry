# Phase 1 Handoff to `/eng-team` — RT-PROJ041-001

> **Engagement:** RT-PROJ041-001
> **Phase:** 1 (Threat Model) — handoff deliverable
> **Authoring Agent:** red-reporter
> **Date:** 2026-04-30
> **Status:** COMPLETE
> **Parent:** EN-004 / TASK-179
> **Audience:** `/eng-team` (eng-architect, eng-backend, eng-devsecops, eng-security, eng-reviewer); EN-001 and EN-003 owners; STORY-009 and STORY-012 owners
> **Methodology:** PTES Reporting; STRIDE; MITRE ATT&CK; OWASP A03/A05/A08

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Engagement Metadata](#engagement-metadata) | Engagement ID, window, agents, source documents |
| [Executive Summary](#executive-summary) | 5-minute read: what the threat model says + the ask |
| [Top Findings (CRITICAL and HIGH)](#top-findings-critical-and-high) | Forwarded findings with mitigations and downstream owners |
| [Design Constraints for `/eng-team`](#design-constraints-for-eng-team) | REQUIREMENTS grouped by destination entity |
| [Open Design Questions for `/eng-team`](#open-design-questions-for-eng-team) | The 10 design questions; blocker mapping |
| [Phase 4 Anticipation](#phase-4-anticipation) | Verification probes /eng-team must build TO |
| [Acceptance Signal](#acceptance-signal) | Phase 1 closure declaration |

---

## Engagement Metadata

| Field | Value |
|-------|-------|
| Engagement ID | RT-PROJ041-001 |
| Engagement Type | Code-and-design red-team (paper engagement; NOT a live-network pentest) |
| Phase | 1 of 2 (Phase 4 explicitly deferred) |
| Phase 1 Window — Start | 2026-04-30 |
| Phase 1 Window — End | This handoff document delivered to `/eng-team` |
| Parent Enabler | EN-004 |
| Parent Epic | EPIC-001 (transcript hardening) |
| Branch | `feat/PROJ-041-transcript-hardening` |
| Authoring Agents (Phase 1) | red-lead (scope), red-recon (recon existing + new), red-vuln (STRIDE + attack paths), red-reporter (this handoff) |
| Methodology | PTES Pre-Engagement + Intelligence Gathering + Reporting; STRIDE per Microsoft SDL; MITRE ATT&CK technique mapping |

### Source Documents (inputs to this handoff)

| Document | Path |
|----------|------|
| Engagement scope (RoE) | `projects/PROJ-041-transcript-hardening/work/EPIC-001-transcript-hardening/EN-004-red-team-threat-model/work/red-team/scope-document.md` |
| Recon — existing surface (Surfaces 1-5) | `projects/PROJ-041-transcript-hardening/work/EPIC-001-transcript-hardening/EN-004-red-team-threat-model/work/red-team/recon-existing-surface.md` |
| Recon — new surface (Surfaces 6-10 + 10 design questions) | `projects/PROJ-041-transcript-hardening/work/EPIC-001-transcript-hardening/EN-004-red-team-threat-model/work/red-team/recon-new-surface.md` |
| STRIDE threat model (60 cells, 10 surfaces) | `projects/PROJ-041-transcript-hardening/work/EPIC-001-transcript-hardening/EN-004-red-team-threat-model/work/red-team/stride-threat-model.md` |
| Attack paths (5 chains, 10-rank mitigation list, 8 Phase 4 bypass classes) | `projects/PROJ-041-transcript-hardening/work/EPIC-001-transcript-hardening/EN-004-red-team-threat-model/work/red-team/attack-paths.md` |
| Parent Enabler (acceptance criteria) | `projects/PROJ-041-transcript-hardening/work/EPIC-001-transcript-hardening/EN-004-red-team-threat-model/EN-004-red-team-threat-model.md` |

---

## Executive Summary

The `/transcript` skill is a four-zone pipeline (filesystem -> parsed JSON -> LLM-extracted JSON -> rendered Markdown) that, in its planned FEAT-003 form, terminates in `subprocess.run(["bash", "-c", pattern])` where `pattern` is an LLM-authored field inside `_anchors.json`. The threat model identifies that **attacker-controlled VTT/SRT content propagates verbatim through every stage** and that **no structural integrity check exists between stages**. The most consequential outcome of this is that a single Tier-1 attacker (someone who supplies a transcript file) can chain through the pipeline to reach `SubprocessSandbox` with adversarial pattern strings — and in CI, that chain ends inside a GitHub Actions runner with `GITHUB_TOKEN` in scope.

The three highest-priority findings: (1) `SubprocessSandbox` is the only line of defense between LLM output and shell execution and must be built with a **formally defined, code-enforced grammar** (not prose); (2) the `STORY-009` post-render hook must NOT add the `Bash` tool to ts-formatter — that single architectural decision deletes an entire critical-severity attack chain; (3) `STORY-012` CI must run the validator against **only committed golden packets**, never PR-submitted files, or every fork PR becomes a sandbox evaluation target with runner credentials in scope.

**The bottom-line ask of `/eng-team`:** treat the design constraints in §[Design Constraints for `/eng-team`](#design-constraints-for-eng-team) as REQUIREMENTS (not suggestions), resolve the 10 open design questions in §[Open Design Questions for `/eng-team`](#open-design-questions-for-eng-team) before the relevant story acceptance, and build EN-003 + STORY-009 + STORY-012 such that the Phase 4 verification probes in §[Phase 4 Anticipation](#phase-4-anticipation) cleanly fail.

---

## Top Findings (CRITICAL and HIGH)

> Severity rubric: CRITICAL = Risk Score 7-9 in STRIDE matrix AND member of an end-to-end attack chain; HIGH = Risk Score 5-6 OR enables a CRITICAL chain. MEDIUM and LOW findings are intentionally NOT forwarded here — refer to the source STRIDE document for those.
>
> Each finding states the exact mitigation that breaks the most chains (cross-referenced to the Mitigation Priority List in `attack-paths.md`).

### CRITICAL Findings

#### F-CRIT-1 — Shell injection via LLM-authored `derivation_grep_pattern`

| Field | Value |
|-------|-------|
| Surface | 6 — `SubprocessSandbox` (planned) |
| ATT&CK | T1059.004 (Command and Scripting Interpreter: Unix Shell) |
| Risk Score | 9 (Critical) — Spoofing, Tampering, Elevation of Privilege all rated 9 in STRIDE matrix |
| Source | `stride-threat-model.md` Surface 6; `attack-paths.md` Chain 1 Step 4, Chain 2 Step 3 |

`_anchors.json` is authored by ts-formatter (an LLM agent). Its `audit_breakdown.per_bucket_derivation[].derivation_grep_pattern` field is the input to `subprocess.run(["bash", "-c", pattern])`. There is no code today between the LLM and the shell. EN-003's design names a command allowlist (`grep`, `wc`, `find`) and prohibits shell metacharacters — but specifies the validator's grammar in prose, not as code. Because LLMs offer no formal security guarantees, the validator is the only barrier between attacker-supplied transcript content and arbitrary command execution.

**Mitigation that breaks the most chains (Mitigation #1 in `attack-paths.md`):** Build `SubprocessSandbox` with a formally defined, code-enforced grammar. The grammar MUST be a callable validator (regex+state machine or equivalent), MUST explicitly enumerate the permitted flags for `grep`, `wc`, `find`, MUST explicitly prohibit `-exec`, `-execdir`, `-P`, MUST prohibit ALL shell metacharacters (`;`, `&&`, `||`, `|`, `>`, `<`, backtick, `$()`), and MUST be exercised by unit tests for each Phase 4 bypass class (BC-1 through BC-5).

**Downstream owners:** EN-003 (sandbox port + adapter); EN-001 (DDD scaffolding must place validator in the application layer where the port lives, not at the adapter where the subprocess call lives).

---

#### F-CRIT-2 — Hook architecture: `Bash` tool MUST NOT be added to ts-formatter

| Field | Value |
|-------|-------|
| Surface | 9 — ts-formatter post-render hook (planned) |
| ATT&CK | T1059.004 + T1598.003 (prompt injection chained to shell execution) |
| Risk Score | 9 (Critical) — both Spoofing and Tampering rated 9 in STRIDE matrix |
| Source | `recon-new-surface.md` Q6; `stride-threat-model.md` Surface 9; `attack-paths.md` Chain 3 |

`STORY-009` requires ts-formatter to invoke `jerry transcript verify` after writing the 8 packet files. ts-formatter's current `tools` list is `Read, Write, Glob` — it does not include `Bash`. The recon surfaced three architectural options for the hook (Q6): (A) add `Bash` to ts-formatter, (B) orchestrator calls `verify` after ts-formatter returns, (C) Claude Code lifecycle hook. **Option A is critical-severity and MUST be rejected.** Adding `Bash` to ts-formatter creates a direct path from prompt injection (Surface 5) to shell execution: an attacker with only Tier-1 capability (a crafted SRT file) can cause an LLM agent with a Bash tool to invoke arbitrary commands.

**Mitigation that breaks the most chains (Mitigation #3 in `attack-paths.md`):** Resolve Q6 as **Option B** — the orchestrator (MAIN CONTEXT or `ts-parser` SKILL.md driver) calls `jerry transcript verify` after ts-formatter returns. ts-formatter's `tools` list is unchanged. The validator's stdout MUST NOT be fed back into ts-formatter's LLM context (this also closes the Step 4 second-stage injection in Chain 3).

**Downstream owners:** EN-001 (architecture decision — record as DEC-006 or equivalent); STORY-009 (acceptance criteria must specify Option B); STORY-010 (`update-anchors` hook ordering — see F-CRIT-5).

---

#### F-CRIT-3 — CI runs SubprocessSandbox against PR-submitted attacker content

| Field | Value |
|-------|-------|
| Surface | 10 — CI workflow (`STORY-012`) |
| ATT&CK | T1195 (Supply Chain Compromise) + T1552.001 (Credentials in Files) |
| Risk Score | 9 (Critical) — Surface 10 Spoofing and Tampering both rated 9 in STRIDE matrix |
| Source | `recon-new-surface.md` Q10; `stride-threat-model.md` Surface 10; `attack-paths.md` Chain 2 |

If `STORY-012`'s CI job runs `jerry transcript verify` against any packet directory present in a pull request branch (rather than only against committed golden packets), a malicious PR can ship a crafted `_anchors.json` whose `derivation_grep_pattern` triggers a sandbox bypass. The bypass executes inside the GitHub Actions runner with `GITHUB_TOKEN` in scope — and depending on workflow configuration, also `CODECOV_TOKEN` and `VERSION_BUMP_PAT`. This converts every fork PR into a live sandbox evaluation against the project's CI credentials.

**Mitigation that breaks the chain at Step 1 (Mitigation #5 in `attack-paths.md`):** Resolve Q10 as **hardcoded-fixture-only** — `STORY-012`'s CI job MUST validate only committed golden packets under `skills/transcript/test_data/expected_output/`. PR-submitted packet directories MUST NOT be passed to `verify` in the standard CI job. If a developer needs to validate an arbitrary packet, that runs locally — not in CI.

**Downstream owners:** STORY-012 (CI workflow definition); EN-003 (sandbox env-stripping correctness — see F-CRIT-4); eng-devsecops (workflow `permissions:` review).

---

#### F-CRIT-4 — Cross-stage integrity gap: `extraction-report.json` and `_anchors.json` are not verified

| Field | Value |
|-------|-------|
| Surface | 3 — JSON sidecar parsing |
| ATT&CK | T1565.001 (Stored Data Manipulation) chaining to T1059.004 |
| Risk Score | 9 (Critical) — Surface 3 Tampering rated 9 in STRIDE matrix |
| Source | `recon-existing-surface.md` Cross-Surface Observations; `stride-threat-model.md` Surface 3; `attack-paths.md` Chain 2 Step 1 |

The pipeline is a trust chain (VTT -> chunks -> extraction-report -> _anchors -> packet) with NO integrity check between stages. A Tier-2 attacker (local filesystem write access) or Tier-3 attacker (PR author committing to test data) can modify `extraction-report.json` or `_anchors.json` between stages. Because no schema validation gate, no checksum, and no signature exists between stages, the next stage consumes the modified file as authoritative pipeline output. This is what enables Chain 2 (sidecar tampering -> sandbox bypass -> CI secret exfiltration) to bypass Chain 1's prompt-injection complexity entirely.

**Mitigations (defense in depth):**
- (Mitigation #2 in `attack-paths.md`) Validate `derivation_grep_pattern` fields against the same allowlist grammar as `SubprocessSandbox` BEFORE ts-formatter writes them to `_anchors.json`. This is a code gate, not a behavioral instruction.
- (Mitigation #10 in `attack-paths.md`) Add cross-stage integrity verification: at minimum, a hash sidecar written by each stage and verified by the next.

**Downstream owners:** EN-001 (architecture must accommodate a write-time validation port for `_anchors.json` and a hash-sidecar mechanism); EN-003 (sandbox grammar is reused for the pre-write validator).

---

#### F-CRIT-5 — Hook ordering gap: verify-before-update-anchors -> infinite retry

| Field | Value |
|-------|-------|
| Surface | 9 — ts-formatter post-render hook (planned) |
| ATT&CK | T1499.004 (Application or System Exploitation) |
| Risk Score | 9 (Critical) — Surface 9 Denial of Service rated 9 in STRIDE matrix |
| Source | `recon-new-surface.md` STORY-009/STORY-010 ordering observation; `stride-threat-model.md` Surface 9 (D row) |

`STORY-009` (verify hook) and `STORY-010` (update-anchors hook) both run post-render. The ordering between them is unspecified. If `verify` runs FIRST (against the LLM-generated, mechanically-stale `_anchors.json`), the verifier rejects on every invocation, causing ts-formatter to retry indefinitely. This is a Critical-severity availability issue that becomes a permanent pipeline stall on first deployment.

**Mitigation:** Specify the ordering as `update-anchors` -> `verify` in BOTH STORY-009 and STORY-010 acceptance criteria. The orchestrator (per F-CRIT-2 Option B) MUST call them in order and MUST NOT call `verify` until `update-anchors` has succeeded.

**Downstream owners:** STORY-009 and STORY-010 (acceptance criteria); EN-001 (orchestrator behavior contract).

---

### HIGH Findings

#### F-HIGH-1 — Path traversal on `<packet>` CLI argument (`verify` and `update-anchors`)

| Field | Value |
|-------|-------|
| Surface | 7 (verify CLI) and 8 (update-anchors CLI) |
| ATT&CK | T1083 (File and Directory Discovery) + T1005 (Data from Local System) + T1222.002 (arbitrary write via update-anchors) |
| Risk Score | 9 (Surface 7 Tampering) and 6 (Surface 8 Elevation of Privilege) |
| Source | `recon-new-surface.md` Q9 + Surface 7/8 risks; `attack-paths.md` Chain 4 |

The `<packet>` positional argument to both `jerry transcript verify` and `jerry transcript update-anchors` is passed to the application layer with no documented canonicalization or scope-check. A user (or CI job) supplying `../../etc` causes the validator to read outside the packet directory; supplying a target like `../../skills/transcript/test_data/expected_output/transcript-meeting-001` to `update-anchors` causes an arbitrary write of `_anchors.json` outside the intended packet — which then chains back into Chain 2 by overwriting committed golden test data.

**Mitigation (Mitigation #4 in `attack-paths.md`):** Add path canonicalization + scope enforcement to BOTH CLI subcommands. The implementation: `pathlib.Path(packet_arg).resolve()` -> verify it is a directory -> verify `is_relative_to()` against an allowed root (e.g., `Path.cwd()` subtree or an explicitly configured project root) -> reject with a clear error message otherwise.

**Downstream owners:** STORY-007 (verify acceptance criteria); STORY-008 (update-anchors acceptance criteria); EN-001 (interface-layer placement of canonicalization, before the application service is called).

---

#### F-HIGH-2 — VTT speaker-name and segment text propagated verbatim into LLM prompts

| Field | Value |
|-------|-------|
| Surface | 1 (VTT/SRT) feeding Surface 5 (LLM injection) |
| ATT&CK | T1565.001 + T1598.003 |
| Risk Score | 9 (Surface 1 Tampering) and 6 (Surface 5 Elevation of Privilege) |
| Source | `recon-existing-surface.md` Surface 1 #2 (no speaker name validation); `stride-threat-model.md` Surface 1 (T row) and Surface 5; `attack-paths.md` Chain 1 Step 1, Chain 5 Step 1 |

`VTTParser` extracts speaker names with the regex `<v\s+([^>]+)>` and stores them verbatim in `ParsedSegment.speaker`; `raw_text` is preserved un-sanitized; both flow through `chunks/chunk-NNN.json` into ts-extractor's LLM context. ts-extractor and ts-formatter agent definitions have no structural delimiter (no `<transcript_data>...</transcript_data>` fence) separating attacker-controlled content from system instructions. This is the foundation enabling Chain 1 (full pipeline injection) and Chain 5 (silent SRT corruption).

**Mitigations (defense in depth):**
- (Mitigation #9 in `attack-paths.md`) Speaker-name validation in `vtt_parser.py`: allowlist or sanitize `ParsedSegment.speaker`; reject Jinja-like templates, YAML special characters, instruction-resembling prefixes.
- (Mitigation #6 in `attack-paths.md`) Structural prompt delimiters in ts-extractor and ts-formatter agent definitions (defense in depth — does not provide guarantees, but degrades injection effectiveness).

**Downstream owners:** EN-001 (the parsing port and adapter must surface a sanitization point); the ts-extractor and ts-formatter agent definitions are out of `/eng-team` direct authorship but the agent-definition changes are tracked via SKILL.md updates in this branch.

---

#### F-HIGH-3 — `find -exec` allowlist bypass class

| Field | Value |
|-------|-------|
| Surface | 6 — `SubprocessSandbox` |
| ATT&CK | T1059.004 + T1548 (Abuse Elevation Control Mechanism) |
| Risk Score | 9 (Surface 6 Elevation of Privilege) |
| Source | `recon-new-surface.md` Surface 6 risk #2; `stride-threat-model.md` Surface 6 (E row); `attack-paths.md` Phase 4 Bypass Class BC-2 |

`find` is on the planned allowlist. `find` supports `-exec` and `-execdir`, which spawn a shell subprocess with arbitrary commands. A pattern like `find . -name "*.md" -exec sh -c '...' {} \;` uses an allowlisted command with a flag that bypasses the entire allowlist. EN-003's prose grammar does not yet explicitly prohibit `-exec`/`-execdir`. This is the canonical class-of-bypass for command-allowlist sandboxes.

**Mitigation:** Subsumed by F-CRIT-1 — the formally defined grammar MUST explicitly prohibit `-exec`, `-execdir`, and any flag that takes a sub-command argument. The unit tests for the validator MUST include a `find -exec` bypass attempt (Phase 4 BC-2).

**Downstream owners:** EN-003 (grammar definition + unit tests).

---

#### F-HIGH-4 — Symlink TOCTOU in `cwd` enforcement

| Field | Value |
|-------|-------|
| Surface | 6 — `SubprocessSandbox` |
| ATT&CK | T1083 (information disclosure path) + T1059.004 (path-relative execution path) |
| Risk Score | 6 (HIGH per recon Pre-Implementation Risk Summary) |
| Source | `recon-new-surface.md` Surface 6 risk #3 + Q2; `attack-paths.md` Phase 4 Bypass Class BC-3 |

The sandbox enforces `cwd=packet_root`. The design uses `pathlib.Path.resolve()` + `is_relative_to()` for path traversal defense and `lstat` for symlink detection, but the sequencing is not yet specified. A symlink inside `packet_root` pointing outside it can pass `is_relative_to()` for the link itself while resolving to a target outside the packet. TOCTOU between `lstat` and `resolve()` enables an attacker who can write inside `packet_root` to swap a regular file for a symlink during the validation window.

**Mitigation:** Specify the sequencing in EN-003 (Q2). Recommended: `lstat` + reject if symlink (do not attempt to resolve and re-check); operate on file descriptors after a successful directory open via `O_NOFOLLOW` semantics where available.

**Downstream owners:** EN-003 (adapter implementation + tests covering BC-3).

---

#### F-HIGH-5 — Atomic-write race / TOCTOU in `update-anchors`

| Field | Value |
|-------|-------|
| Surface | 8 — `update-anchors` CLI |
| ATT&CK | T1565.001 (race-condition stored data manipulation) |
| Risk Score | 6 (Surface 8 Tampering with TOCTOU) |
| Source | `recon-new-surface.md` Surface 8 risks #1-3 + Q7; `stride-threat-model.md` Surface 8 (S, T rows); `attack-paths.md` Phase 4 Bypass Class BC-7 |

Two concurrent `update-anchors` invocations both read the same initial state and produce a last-writer-wins overwrite. The ts-formatter -> update-anchors sequence has a TOCTOU window (file writes complete -> update-anchors begins reading). On NFS or shared CI storage the window is observably long. There is no documented mutual-exclusion mechanism. Partial-write recovery is undefined.

**Mitigation:** Resolve Q7 — specify a concurrency model. Recommended: atomic rename (`os.replace`) from a uniquely-named temp file in the same directory as `_anchors.json`, plus advisory file locking (`fcntl.flock` on POSIX; equivalent on Windows) on a sentinel file in the packet directory. Document explicit "no concurrent invocation" semantics in CLI help.

**Downstream owners:** EN-001 (`UpdateAnchorsService` application service contract); STORY-008 (acceptance criteria including atomic rename + lock); STORY-010 (hook ordering with F-CRIT-5).

---

#### F-HIGH-6 — Validator stdout as LLM prompt-injection vector

| Field | Value |
|-------|-------|
| Surface | 9 — ts-formatter post-render hook |
| ATT&CK | T1598.003 (prompt injection via verification feedback) |
| Risk Score | 6 (HIGH per recon Pre-Implementation Risk Summary; Surface 9 Tampering rated 9 in STRIDE) |
| Source | `recon-new-surface.md` Surface 9 risk #2; `attack-paths.md` Chain 3 Step 4, Phase 4 Bypass Class BC-8 |

If the orchestrator (or any caller) feeds the `verify` subprocess stdout back into ts-formatter's LLM context, attacker-controlled packet content reaches the LLM as "validation report" text. Failure messages echo anchor IDs, file paths, and content excerpts — all of which are attacker-controlled if the upstream pipeline was injected.

**Mitigation:** The orchestrator (per F-CRIT-2 Option B) MUST consume only the `verify` exit code and a structured machine-readable summary; it MUST NOT pass full stdout back to the ts-formatter LLM. If diagnostic output is required for debugging, it goes to logs, not to LLM context.

**Downstream owners:** EN-001 (orchestrator behavior contract); STORY-009 (acceptance criteria).

---

#### F-HIGH-7 — `--output-dir` path traversal in ts-formatter packet writing

| Field | Value |
|-------|-------|
| Surface | 4 — Markdown packet writing |
| ATT&CK | T1222.002 (analogue: arbitrary write) |
| Risk Score | 6 (Surface 4 Elevation of Privilege) |
| Source | `recon-existing-surface.md` Cross-Surface Observations (Output Directory is Caller-Specified); `stride-threat-model.md` Surface 4 (E row) |

`uv run jerry transcript parse "<FILE_PATH>" --output-dir "<OUTPUT_DIR>"` accepts the output directory verbatim. A `..`-prefixed path writes packet files outside the intended location, including potentially overwriting skill configuration or CI workflow files in the same checkout.

**Mitigation:** Apply the same canonicalization + scope-check pattern as F-HIGH-1 to the `--output-dir` argument at the CLI interface layer. Resolved path MUST be inside an allowed root.

**Downstream owners:** EN-001 (CLI interface layer of the parse subcommand); the existing `parse` CLI surface lives outside FEAT-003 today but the same architectural placement applies.

---

## Design Constraints for `/eng-team`

> These are stated as REQUIREMENTS, not suggestions. Each constraint has a finding ID showing which CRITICAL/HIGH finding it satisfies. Where a constraint references a Phase 4 verification probe, that probe is enumerated in §[Phase 4 Anticipation](#phase-4-anticipation).

### For EN-001 (DDD scaffolding)

| ID | Constraint | Source Finding |
|----|------------|----------------|
| C-EN001-1 | The hexagonal layout MUST place a `SubprocessSandbox` Protocol/port in `src/jerry/transcript/validation/application/ports.py` with the adapter at `src/jerry/transcript/validation/infrastructure/subprocess_sandbox.py`. The application layer MUST consume the sandbox via the port only — domain code MUST NOT reference subprocess primitives. This isolation is required so the sandbox can be replaced with a no-op in tests and so the validator grammar lives in application code, not adapter code. | F-CRIT-1 |
| C-EN001-2 | A pre-write validation port for `_anchors.json` (`AnchorWriter` or equivalent) MUST exist. The port's contract MUST require the same allowlist-grammar validation as `SubprocessSandbox` is applied to every `derivation_grep_pattern` field BEFORE the file is persisted. ts-formatter's write path goes through this port. | F-CRIT-4 |
| C-EN001-3 | The post-render hook architecture MUST be **Option B** (orchestrator calls `verify` after ts-formatter returns). ts-formatter's `tools` list MUST remain `Read, Write, Glob` — `Bash` MUST NOT be added. The decision MUST be recorded in DEC-006 or equivalent. | F-CRIT-2 |
| C-EN001-4 | The orchestrator's hook contract MUST call `update-anchors` BEFORE `verify`. The contract MUST specify: (a) `update-anchors` exit code 0 is a precondition for invoking `verify`, (b) `verify` is NOT called if `update-anchors` failed, (c) the verifier's stdout MUST NOT be passed back into any LLM agent's context. | F-CRIT-5, F-HIGH-6 |
| C-EN001-5 | Path canonicalization for the `<packet>` CLI argument (and the `--output-dir` argument of `parse`) MUST occur in the interface layer, BEFORE the application service is called. Implementation pattern: `Path.resolve()` -> `is_dir()` -> `is_relative_to(allowed_root)` -> reject otherwise. | F-HIGH-1, F-HIGH-7 |
| C-EN001-6 | The `UpdateAnchorsService` application service contract MUST specify a concurrency model (atomic rename + advisory lock recommended; alternative MUST be justified). Forward-compatible field preservation MUST be specified (Q8). | F-HIGH-5 |
| C-EN001-7 | The validator report destination MUST be specified explicitly in STORY-007's acceptance criteria. The destination MUST NOT be derived from the `<packet>` argument without canonicalization (combining F-HIGH-1 with information disclosure risk on Surface 7). | F-HIGH-1 |

### For EN-003 (`SubprocessSandbox`)

| ID | Constraint | Source Finding |
|----|------------|----------------|
| C-EN003-1 | The argument validator MUST be a formally defined, code-enforced grammar. Allowlisted commands: `grep`, `wc`, `find` only. The validator MUST be expressed as code (regex+state machine, parser combinator, or equivalent) — NOT as prose in agent definitions or comments. | F-CRIT-1 |
| C-EN003-2 | The grammar MUST explicitly enumerate permitted flags per command. For `find`: `-exec`, `-execdir`, and any flag taking a sub-command argument MUST be explicitly prohibited. For `grep`: `-P` (PCRE) MUST be prohibited (catastrophic-backtracking DoS vector). The flag list per command MUST be a closed allowlist. | F-CRIT-1, F-HIGH-3 |
| C-EN003-3 | ALL shell metacharacters MUST be prohibited at the validator level: `;`, `&&`, `||`, `|`, `>`, `<`, backtick, `$()`, `$(...)`, redirection of any form. The validator MUST reject patterns containing these BEFORE invoking `subprocess`. | F-CRIT-1 |
| C-EN003-4 | Path arguments inside patterns MUST be canonicalized via `pathlib.Path.resolve()` and `is_relative_to(packet_root)` MUST hold. `lstat` MUST be called first; if the path is a symlink, it MUST be rejected immediately (do NOT attempt to resolve and re-check — this opens a TOCTOU window). | F-HIGH-4 |
| C-EN003-5 | Environment stripping MUST be implemented by passing `env={"PATH": "/usr/bin:/bin"}` directly to `subprocess.Popen()`. Implementations MUST NOT mutate `os.environ` (process-global, leaks back into other code paths). This is non-negotiable — the Q3 answer is "via the `env=` parameter to Popen." | F-CRIT-3 (CI secret protection) |
| C-EN003-6 | Output size limit MUST be enforced via streaming reads with a hard cap, NOT via `communicate()` buffering all output before checking. Recommended: `process.stdout.read(MAX_BYTES + 1)`; if `len > MAX_BYTES` -> kill subprocess + reject. The limit is 1 MiB; the implementation MUST NOT permit a multi-GB grep output to be buffered before the limit check. | F-CRIT-1 (DoS via resource exhaustion) |
| C-EN003-7 | Timeout enforcement MUST kill the subprocess AND its descendants. On POSIX: spawn the subprocess in its own process group (`start_new_session=True` or `preexec_fn=os.setsid`) and on timeout `os.killpg(pgid, signal.SIGKILL)`. The implementation MUST NOT rely on `process.kill()` alone — `find -exec sh ...` may have spawned children. | F-CRIT-1 (cleanup), F-HIGH-3 |
| C-EN003-8 | The validator MUST have unit tests for each Phase 4 bypass class enumerated in §[Phase 4 Anticipation](#phase-4-anticipation) BC-1 through BC-5. Tests MUST be present on the first commit of EN-003 — not added retroactively. | F-CRIT-1 |

### For STORY-009 (post-render hook)

| ID | Constraint | Source Finding |
|----|------------|----------------|
| C-STORY009-1 | Hook architecture MUST be Option B per C-EN001-3. ts-formatter MUST NOT be granted the `Bash` tool. The orchestrator (MAIN CONTEXT or ts-parser SKILL.md driver) MUST be the caller of `jerry transcript verify`. | F-CRIT-2 |
| C-STORY009-2 | The orchestrator MUST call `update-anchors` BEFORE `verify`. STORY-009 acceptance criteria MUST cite the ordering constraint AND a corresponding test that confirms `verify` is not called when `update-anchors` fails. | F-CRIT-5 |
| C-STORY009-3 | The orchestrator MUST NOT pass the verifier's stdout back into any LLM agent's context. The orchestrator may pass the exit code and a structured machine-readable summary (counts, failed rule IDs) — but NOT the full report content. | F-HIGH-6 |
| C-STORY009-4 | Failure handling MUST be specified explicitly: `verify` exit code 1 MUST surface as a hard error to the orchestrator and MUST NOT be silently interpreted by the LLM as a soft warning. | F-CRIT-5 (related: ambiguous failure mode) |

### For STORY-012 (CI workflow)

| ID | Constraint | Source Finding |
|----|------------|----------------|
| C-STORY012-1 | The validator CI job MUST run `verify` against ONLY committed golden packets under `skills/transcript/test_data/expected_output/`. The job MUST NOT be configured to validate PR-submitted packet directories. This resolves Q10 as fixture-only. | F-CRIT-3 |
| C-STORY012-2 | The validator CI job MUST set `permissions:` to the minimum required (`contents: read` at minimum; explicitly NOT `contents: write`, NOT `issues: write`, NOT `pull-requests: write`). | F-CRIT-3 |
| C-STORY012-3 | The validator CI job MUST NOT run in the same workflow as any job that has access to `VERSION_BUMP_PAT` or any other elevated PAT. Workflow isolation: the validator runs in its own workflow file or a dedicated job whose `permissions:` block is at the job level (not inherited from the workflow level). | F-CRIT-3 |
| C-STORY012-4 | The CI job MUST have a total wall-clock timeout (e.g., 10 minutes) to bound resource exhaustion via large `_anchors.json` (Surface 7 D row). | F-HIGH-1 (DoS via large packet) |

### Cross-Cutting Constraints (apply across multiple entities)

| ID | Constraint | Source Finding |
|----|------------|----------------|
| C-XCUT-1 | **Pipeline integrity verification between stages.** A code-enforced gate MUST exist between every pipeline stage where attacker-controlled content crosses a trust boundary. Specifically: (a) `derivation_grep_pattern` validation BEFORE write to `_anchors.json` (C-EN001-2); (b) JSON schema validation of `extraction-report.json` BEFORE ts-formatter consumes it; (c) JSON schema validation of `_anchors.json` BEFORE `SubprocessSandbox` consumes any of its fields. Behavioral instructions in agent definitions DO NOT satisfy this constraint — code does. | F-CRIT-4 |
| C-XCUT-2 | **No reliance on LLM behavioral guardrails for security-critical decisions.** Every "Mitigation: behavioral instruction" entry in the STRIDE matrix is effectively "Mitigation: None." Security-critical guarantees (allowlists, validators, scope checks, integrity verification) MUST be code, not prose in agent .md files. | Systemic finding (`stride-threat-model.md` Cross-Surface Aggregate Findings: "Behavioral vs. Structural Guardrail Gap") |
| C-XCUT-3 | **Repo-relative paths only in all errors and reports.** No deliverable, log, error message, or report produced by FEAT-003 entities may contain absolute machine paths (POSIX home directories, Windows drive letters). This aligns with scope-document P-9 and is enforceable via CI architecture-validation tests. | scope-document P-9 |
| C-XCUT-4 | **Speaker name and segment text sanitization at parse boundary.** `vtt_parser.py` MUST sanitize `ParsedSegment.speaker` and reject or escape Jinja-like templates, YAML control characters, and instruction-resembling prefixes BEFORE the field reaches `chunks/chunk-NNN.json`. This is the earliest break point for Chains 1 and 5. | F-HIGH-2 |

---

## Open Design Questions for `/eng-team`

> The 10 design questions enumerated in `recon-new-surface.md` are reproduced verbatim below. Each question is annotated with: (a) which downstream entity owns the resolution, (b) which acceptance gates the question blocks, and (c) the recommended answer where one was identified during Phase 1.

### Q1 — Formal grammar for allowed patterns (EN-003)

The EN-003 design states argument validation uses "a permissive grammar: command + flags from allowlist + literal-string args." What is the formal grammar? Specifically: which flags are permitted for `grep`, `wc`, and `find`? Is `-exec` explicitly prohibited for `find`? Is `-P` (pipe) prohibited for `grep`? The grammar must be machine-verifiable, not prose.

- **Owner:** EN-003.
- **Blocks acceptance of:** EN-003, all stories that consume `SubprocessSandbox` (STORY-007, STORY-012).
- **Recommended answer:** Per C-EN003-1, C-EN003-2, C-EN003-3 — formally defined, code-enforced grammar with explicit flag allowlists per command and explicit prohibition of `-exec`, `-execdir`, `-P`, and all shell metacharacters.

### Q2 — Symlink handling sequencing (EN-003)

The design specifies `lstat` first to detect symlinks, then `resolve()` + `is_relative_to()`. What is the exact sequencing? If `lstat` shows a symlink, is the path rejected immediately, or does it attempt to verify where the symlink resolves to? TOCTOU between `lstat` and subsequent `resolve()` calls must be addressed.

- **Owner:** EN-003.
- **Blocks acceptance of:** EN-003.
- **Recommended answer:** Per C-EN003-4 — `lstat` first, reject immediately on symlink (do not attempt resolve-and-recheck).

### Q3 — Subprocess env stripping implementation (EN-003)

Does `SubprocessSandboxAdapter` pass `env={"PATH": "/usr/bin:/bin"}` directly to `subprocess.Popen()` (correct), or does it modify `os.environ` (incorrect — process-global, incomplete)? This implementation choice must be specified explicitly in the acceptance criteria for TASK-069.

- **Owner:** EN-003 (TASK-069).
- **Blocks acceptance of:** EN-003, STORY-012 (CI secret protection depends on correct implementation).
- **Recommended answer:** Per C-EN003-5 — `env={...}` parameter to `Popen()` only. Mutating `os.environ` is prohibited.

### Q4 — Output size limit enforcement timing (EN-003)

The 1MB output size limit: is it enforced by setting `stdout=subprocess.PIPE` with `communicate()` (which buffers all output in memory before checking size), or by streaming with `read(1024*1024+1)` (which stops reading at the limit)? Buffering all output defeats the purpose of the limit for memory exhaustion attacks.

- **Owner:** EN-003.
- **Blocks acceptance of:** EN-003.
- **Recommended answer:** Per C-EN003-6 — streaming reads with a hard cap. Buffering via `communicate()` is prohibited.

### Q5 — Child process cleanup on timeout (EN-003)

When the wall-clock timeout fires and `process.kill()` is called, does the implementation also kill child processes? On POSIX, use `os.killpg(os.getpgid(process.pid), signal.SIGKILL)` if the subprocess may spawn children (e.g., via `find -exec sh`). Specify which kill mechanism is used and why.

- **Owner:** EN-003.
- **Blocks acceptance of:** EN-003.
- **Recommended answer:** Per C-EN003-7 — process group with `os.killpg()` on POSIX.

### Q6 — ts-formatter post-render hook architecture (EN-001)

ts-formatter's current allowed-tools are `Read, Write, Glob` — `Bash` is excluded. STORY-009 requires ts-formatter to invoke `jerry transcript verify` post-render. Three options exist: (A) add `Bash` to ts-formatter (expands tool surface), (B) orchestrator calls `verify` after ts-formatter returns (no tool change but hook is not ts-formatter's responsibility), (C) use a Claude Code lifecycle hook (post-agent event, if available). Which option does EN-001 recommend? This is a security-critical architectural decision that must be captured in DEC-006 or equivalent.

- **Owner:** EN-001.
- **Blocks acceptance of:** EN-001, STORY-009.
- **Recommended answer:** Per C-EN001-3 and F-CRIT-2 — **Option B** (orchestrator calls verify). Option A is critical-severity and MUST be rejected.

### Q7 — `update-anchors` concurrency model (EN-001)

What concurrency model does `UpdateAnchorsService` use to prevent lost-update races? Options include: advisory file locking (`fcntl.flock`), PID files, atomic rename from a uniquely-named temp file, or explicit "no concurrent invocation" constraint documented in CLI help. Each option has different guarantees across macOS/Linux/Windows (the test matrix in ci.yml shows all three OS).

- **Owner:** EN-001 (`UpdateAnchorsService` contract); STORY-008 (acceptance criteria).
- **Blocks acceptance of:** STORY-008, STORY-010.
- **Recommended answer:** Per F-HIGH-5 mitigation — atomic rename (`os.replace`) from a uniquely-named temp file in the same directory + advisory file locking on a sentinel file. Document explicit "no concurrent invocation" semantics in CLI help.

### Q8 — `_anchors.json` schema version preservation (EN-001)

When `update-anchors` rewrites `_anchors.json`, does it preserve the `version` field and any fields it does not understand (forward-compatibility)? Specify in the `UpdateAnchorsService` acceptance criteria (TASK-054) what the preservation policy is.

- **Owner:** EN-001 (TASK-054).
- **Blocks acceptance of:** STORY-008.
- **Recommended answer:** Preserve unknown fields; preserve and propagate `version` field; if the service does not understand the schema version, fail explicitly rather than rewriting.

### Q9 — Validator CLI output destination (EN-001)

Where does `jerry transcript verify` write its report (JSON + Markdown)? Options: (A) alongside the packet (`<packet>/validation-report.{json,md}`), (B) to stdout/stderr only, (C) to a caller-specified path. If option A, the output path is derived from the input path, creating a traversal risk if `<packet>` is not validated. Specify in STORY-007 acceptance criteria.

- **Owner:** STORY-007 acceptance criteria.
- **Blocks acceptance of:** STORY-007.
- **Recommended answer:** Per F-HIGH-1 mitigation — Option C (caller-specified path) with the same canonicalization + scope check as the `<packet>` argument. Default to stdout (Option B) when `--report` is not specified.

### Q10 — Golden packet test fixture control in CI (STORY-012)

STORY-012 runs the validator in CI. Should `verify` run against only hardcoded committed golden packets (`skills/transcript/test_data/expected_output/`), or against any PR-submitted packet directory? If against PR-submitted files, the CI job becomes a SubprocessSandbox evaluation target for any PR author. Recommend: restrict to committed golden packets only for CI; provide a separate dev-mode flag for arbitrary packet validation.

- **Owner:** STORY-012.
- **Blocks acceptance of:** STORY-012.
- **Recommended answer:** Per C-STORY012-1 and F-CRIT-3 — **fixture-only**. CI validates only committed golden packets. Arbitrary packet validation runs locally, not in CI.

### Blocker Summary

| Question | Blocks | Severity if Unanswered |
|----------|--------|------------------------|
| Q1, Q2, Q3, Q4, Q5 | EN-003 acceptance | CRITICAL — sandbox cannot ship without these |
| Q6 | EN-001 architecture decision; STORY-009 | CRITICAL — F-CRIT-2 |
| Q7 | STORY-008, STORY-010 | HIGH — F-HIGH-5 |
| Q8 | STORY-008 | MEDIUM — forward-compatibility hygiene |
| Q9 | STORY-007 | HIGH — F-HIGH-1 information-disclosure path |
| Q10 | STORY-012 | CRITICAL — F-CRIT-3 |

---

## Phase 4 Anticipation

> Phase 4 is explicitly NOT authorized by the current scope (RT-PROJ041-001 covers only Phase 1). When FEAT-003 implementations land, a new scope authorization (suggested ID: `RT-PROJ041-002`) MUST be authored by red-lead and re-signed by the user before any Phase 4 agent operates.
>
> The probes below tell `/eng-team` what Phase 4 will attempt. Build TO these probes — i.e., expect that Phase 4 will run the listed bypass classes, atomic-write race, and prompt-injection probe against the built artifacts. The probes are derived verbatim from the 8 Phase 4 bypass classes in `attack-paths.md`.

| Probe | Surface | Description | Prerequisite Artifact |
|-------|---------|-------------|----------------------|
| **BC-1** — Shell metacharacter injection | 6 | Probe `_anchors.json.derivation_grep_pattern` containing `;`, `&&`, backticks, `$()`, redirection. Sandbox MUST reject before invoking subprocess. | EN-003 complete |
| **BC-2** — `find -exec` allowlist bypass | 6 | Probe `find . -name "*.md" -exec sh -c '...' {} \;` (allowlisted command + prohibited flag). Sandbox MUST reject. | EN-003 complete; formal grammar must explicitly prohibit `-exec`/`-execdir` (F-HIGH-3) |
| **BC-3** — Symlink escape via `cwd` enforcement | 6 | Create a symlink inside `packet_root` pointing outside it. Sandbox MUST detect and reject before subprocess invocation. Verify `lstat` precedes `resolve()` and rejection is immediate. | EN-003 complete |
| **BC-4** — Env var inheritance | 6, 10 | Verify `subprocess.Popen(env={...})` is used; attempt to read `GITHUB_TOKEN` from subprocess environment via an allowlisted command (`env` is not allowlisted, but `find` -exec sh could; covered by BC-2 prohibition). The probe also verifies that `os.environ` is unchanged in the parent process after the subprocess runs. | EN-003 complete + STORY-012 CI job defined |
| **BC-5** — Resource exhaustion | 6 | Probe with `find` against deep tree, `grep` on binary file, patterns generating multi-MB output. Verify output size limit (1 MiB) and timeout (5s default; 60s hard kill) are both enforced before memory pressure. Verify streaming reads (not `communicate()` buffering). | EN-003 complete |
| **BC-6** — Path traversal on `<packet>` | 7, 8 | Probe `jerry transcript verify ../../etc` and `jerry transcript update-anchors ../../skills/transcript`. Both subcommands MUST reject with a clear error and MUST NOT read or write outside the resolved scope. | STORY-007 + STORY-008 complete |
| **BC-7** — Atomic write race | 8 | Run two concurrent `update-anchors` invocations against the same packet. Verify either (a) mutual exclusion blocks the second invocation, or (b) both invocations produce a consistent end state (last-writer-wins detectable, no corruption, no half-written `_anchors.json`). Verify on macOS, Linux, and Windows (the project's CI matrix). | STORY-008 complete |
| **BC-8** — Validator stdout injection | 9 | Craft packet content that produces validation failure messages containing LLM instruction syntax. Confirm that the orchestrator does NOT feed full `verify` stdout back into ts-formatter's LLM context (per C-STORY009-3). The probe measures whether ts-formatter's behavior changes when the validator emits adversarial-looking failure text. | STORY-009 complete (Option B hook architecture) |

### Additional Phase 4 Targets Implied by Findings

| Probe | Source Finding | Notes |
|-------|----------------|-------|
| Pipeline injection chain end-to-end | F-CRIT-1 + F-HIGH-2 + F-CRIT-4 (Chain 1 in `attack-paths.md`) | Construct adversarial VTT/SRT, run full pipeline, verify SubprocessSandbox blocks the resulting `_anchors.json` payload. |
| Sidecar tampering chain end-to-end | F-CRIT-3 + F-CRIT-4 (Chain 2) | Direct modify of `extraction-report.json`/`_anchors.json` in a Tier-2 scenario; verify the pre-write validation gate (C-EN001-2) catches it. |
| Hook ordering | F-CRIT-5 | Run a packet that triggers `update-anchors` to fail; verify `verify` is NOT invoked by the orchestrator. |
| `--output-dir` traversal | F-HIGH-7 | Probe `jerry transcript parse --output-dir ../..`. Parse subcommand MUST reject. |

The constraints in §[Design Constraints for `/eng-team`](#design-constraints-for-eng-team) are written such that, if all constraints are satisfied, every probe in this section will fail to achieve its adversarial objective. Conversely, any probe that succeeds in Phase 4 indicates a constraint that was violated — the constraints and probes are dual.

---

## Acceptance Signal

This handoff completes Phase 1 of EN-004 per the parent enabler's acceptance criterion: "Phase 1 handoff document delivered to `/eng-team` before EN-001 design starts."

The Phase 1 deliverable set is now complete:

| Deliverable | Path | Status |
|-------------|------|--------|
| Engagement scope (RoE) | `projects/PROJ-041-transcript-hardening/work/EPIC-001-transcript-hardening/EN-004-red-team-threat-model/work/red-team/scope-document.md` | Complete |
| Recon (existing surface) | `projects/PROJ-041-transcript-hardening/work/EPIC-001-transcript-hardening/EN-004-red-team-threat-model/work/red-team/recon-existing-surface.md` | Complete |
| Recon (new surface) | `projects/PROJ-041-transcript-hardening/work/EPIC-001-transcript-hardening/EN-004-red-team-threat-model/work/red-team/recon-new-surface.md` | Complete |
| STRIDE threat model (60 cells, 10 surfaces) | `projects/PROJ-041-transcript-hardening/work/EPIC-001-transcript-hardening/EN-004-red-team-threat-model/work/red-team/stride-threat-model.md` | Complete |
| Attack paths (5 chains, 10-rank mitigation list, 8 Phase 4 bypass classes) | `projects/PROJ-041-transcript-hardening/work/EPIC-001-transcript-hardening/EN-004-red-team-threat-model/work/red-team/attack-paths.md` | Complete |
| Phase 1 handoff to `/eng-team` (this document) | `projects/PROJ-041-transcript-hardening/work/EPIC-001-transcript-hardening/EN-004-red-team-threat-model/work/red-team/phase-1-handoff-to-eng-team.md` | This deliverable |

**Phase 1 closure is subject to:**
1. `/adversary` C4 review on the threat model + remediation set per the parent enabler acceptance criterion (target score >= 0.95).
2. `/eng-team` acknowledgment of this handoff (consumer signal).

**Phase 4 deferral (explicit):**
Phase 4 (live exploit attempts against built artifacts: SubprocessSandbox bypasses, atomic-write race probe, prompt-injection probe per `scope-document.md` §Phase 4 Deferral Notice) is EXPLICITLY DEFERRED until FEAT-003 implementations land. A new scope authorization (suggested ID: `RT-PROJ041-002`) MUST be authored by red-lead and re-signed by the user before any Phase 4 agent operates. This handoff document does NOT authorize Phase 4 activity.

---

*Document Version: 1.0.0*
*Engagement: RT-PROJ041-001 Phase 1*
*Authoring Agent: red-reporter*
*Constitutional Compliance: P-001 (evidence-based; all findings cite source documents), P-002 (persisted to disk), P-003 (no subagents), P-020 (user authority — recommendations, not directives outside scope), P-022 (no deception; severity scoring honest and consistent with STRIDE matrix; Phase 4 deferral stated explicitly)*
*Source Inputs: scope-document.md, recon-existing-surface.md, recon-new-surface.md, stride-threat-model.md, attack-paths.md, EN-004-red-team-threat-model.md*
