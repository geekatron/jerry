# EN-003: SubprocessSandbox port + adapter (security boundary)

> **Type:** enabler
> **Enabler Type:** architecture
> **Status:** pending
> **Priority:** high
> **Impact:** critical
> **Created:** 2026-04-28T00:00:00Z
> **Parent:** FEAT-003
> **Owner:** adam.nowak
> **Effort:** 8

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | What this Enabler delivers |
| [Technical Approach](#technical-approach) | Sandbox design overview |
| [Threat Model Summary](#threat-model-summary) | Why this is a security-critical Enabler |
| [Sandbox Design](#sandbox-design) | Defenses applied |
| [Agent Assignment](#agent-assignment) | Specific skill+agent mappings |
| [Acceptance Criteria](#acceptance-criteria) | Verification checklist |
| [Children Tasks](#children-tasks) | Task breakdown |
| [Related Items](#related-items) | Links and dependencies |
| [History](#history) | Change log |

---

## Summary

The author's gist runs `subprocess.run(["bash", "-c", pattern], cwd=str(packet_root))` where `pattern` is read from `_anchors.json.audit_breakdown.per_bucket_derivation[bucket].derivation_grep_pattern`. **Anyone who writes that JSON file gets shell execution** in the validator's environment. This is a direct shell injection vector if the pattern field isn't strictly validated and sandboxed.

This Enabler builds the security boundary as a port + adapter pair. The port (`SubprocessSandbox`) is the contract; the adapter is the hardened implementation. Validators always go through the port — they never call `subprocess.run` directly.

Per AE-005, this is auto-C3 minimum (security-relevant code). Per user direction (`/red-team` scope = full surface), this Enabler is gated by `/red-team` exit criteria.

---

## Technical Approach

Build the security boundary as a port + adapter pair (hexagonal architecture, H-07). The port (`SubprocessSandbox` Protocol) is the contract; the adapter is the hardened implementation. Validators always go through the port — they never call `subprocess.run` directly. Bandit + Semgrep rules enforce this in CI. The Threat Model Summary and Sandbox Design subsections specify the concrete defenses.

---

## Threat Model Summary

(Full threat model lives in EN-004. This section captures the sandbox-specific findings.)

| Threat | STRIDE | Mitigation |
|--------|--------|-----------|
| Arbitrary command injection via JSON-supplied `pattern` | Tampering, Elevation | Command allowlist (only `grep`, `wc`, `find` with restricted flags); reject patterns containing shell metacharacters outside literal strings |
| Path traversal via `pattern` referencing files outside packet root | Tampering, Information Disclosure | Force `cwd` to packet root; reject patterns with `..`, absolute paths, or symlinks resolving outside packet root |
| Resource exhaustion via runaway grep on giant transcript | Denial of Service | Wall-clock timeout (default 5s); CPU/memory limits via subprocess controls |
| Privilege gain via setuid binaries | Elevation | Reject patterns invoking setuid-capable binaries; document allowlist |
| Information disclosure via reading sensitive env vars | Information Disclosure | Subprocess inherits minimal sanitized env (only PATH and explicit allowlist) |

---

## Sandbox Design

| Aspect | Decision |
|--------|----------|
| Command allowlist | `grep`, `wc`, `find` (read-only enumeration). Future expansion requires explicit ADR. |
| Argument validation | Each pattern parsed against a permissive grammar: command + flags from allowlist + literal-string args. Reject patterns containing `;`, `&&`, `\|\|`, backticks, `$()`, `>`, `<`, `\|` outside known-safe positions. |
| `cwd` enforcement | Always `packet_root`; sandbox refuses to execute if requested cwd resolves outside packet_root. |
| Path traversal guard | Resolve all path arguments via `pathlib.Path.resolve()`; reject if `not is_relative_to(packet_root)`. |
| Symlink handling | `lstat` first; refuse if symlink leads outside packet_root. |
| Timeout | Default 5s wall-clock; configurable per call up to 30s; hard kill at 60s. |
| Env var policy | Strip all env vars except `PATH` (set to `/usr/bin:/bin`) and allowlist. |
| Output handling | Capture stdout/stderr to memory; reject output > 1MB (defense against `find /` returning gigabytes). |
| Failure mode | Always raise typed exception; never return ambiguous tuple. |

---

## Agent Assignment

| Step | Skill | Agent | Purpose |
|------|-------|-------|---------|
| 1 | `/red-team` | `red-vuln` | STRIDE threat model + attack-path analysis on planned subprocess execution surface (consumed by EN-004 Phase 1; informs sandbox design here) |
| 2 | `/eng-team` | `eng-architect` | Security boundary architecture: SubprocessSandbox port shape; hexagonal H-07 isolation |
| 3 | `/eng-team` | `eng-infra` | Implement `SubprocessSandboxAdapter`: command allowlist, arg validation, path-traversal guard, timeout, env sanitization, output size limits |
| 4 | `/eng-team` | `eng-qa` | Hypothesis property-based tests; 10K+ generated inputs; coverage ≥95% on adapter |
| 5 | `/eng-team` | `eng-security` | Manual secure code review on adapter implementation |
| 6 | `/red-team` | `red-exploit` | Exploit attempts against sandbox: ≥5 bypass classes (command injection, path traversal, env poisoning, symlink escape, resource exhaustion); document in EN-004 Phase 4 deliverables |
| 7 | `/eng-team` | `eng-devsecops` | Add Bandit + Semgrep rules forbidding direct `subprocess.run` outside this adapter |
| 8 | `/adversary` | `adv-executor` + `adv-scorer` | C4 ≥0.95 review on adapter design + tests + red-team validation |
| 9 | `/worktracker` | `wt-verifier` | Validate AC; close |

---

## Acceptance Criteria

- [ ] `SubprocessSandbox` Protocol class declared in `src/jerry/transcript/validation/application/ports.py`.
- [ ] `SubprocessSandboxAdapter` implementation at `src/jerry/transcript/validation/infrastructure/subprocess_sandbox.py`.
- [ ] Adapter rejects all 5 threat categories above with typed exceptions; each rejection has a unit test.
- [ ] Property-based tests using Hypothesis explore the input space for the pattern parser; no parser bypass found in 10K+ generated inputs.
- [ ] `/eng-team` `eng-security` manual code review pass on the adapter.
- [ ] `/red-team` `red-exploit` exploit attempts against the adapter — at least 5 attempted bypass classes (command injection, path traversal, env var poisoning, symlink escape, resource exhaustion). All blocked with evidence in the threat model report (EN-004).
- [ ] `/eng-team` `eng-devsecops` adds Bandit + Semgrep rules for any future direct `subprocess.run` calls in `validation/` (forces use of the port).
- [ ] Test coverage on the adapter ≥95% (security-critical code).
- [ ] `/adversary` C4 ≥0.95 review on the adapter's design + tests.

---

## Children Tasks

| ID | Title | Status |
|----|-------|--------|
| TASK-001 | Declare SubprocessSandbox Protocol in application/ports.py | pending |
| TASK-002 | Implement SubprocessSandboxAdapter (command allowlist + arg validation) | pending |
| TASK-003 | Implement path traversal guard | pending |
| TASK-004 | Implement timeout + resource limits | pending |
| TASK-005 | Implement env var sanitization | pending |
| TASK-006 | Author Hypothesis property-based tests | pending |
| TASK-007 | Run /eng-team eng-security manual code review | pending |
| TASK-008 | Run /red-team red-exploit bypass attempts | pending |
| TASK-009 | Add Bandit + Semgrep rules to forbid direct subprocess.run | pending |
| TASK-010 | Run /adversary C4 review | pending |

---

## Related Items

### Hierarchy

- **Parent Feature:** [FEAT-003](../FEAT-003-deterministic-validation.md)

### Dependencies

| Type | Item | Description |
|------|------|-------------|
| Blocked By | EN-001 | Module skeleton must exist for port and adapter to live in |
| Blocked By | EN-004 | Threat model informs sandbox design |
| Blocks | STORY-003..STORY-006 | All rule implementations route through this sandbox for any subprocess execution |
| Blocks | STORY-007, STORY-008 | CLI subcommands depend on sandbox for `verify` and `update-anchors` |

### Source

- [#273 comment 1](https://github.com/geekatron/jerry/issues/273#issuecomment-4339264545) — author's gist `walk_pattern` function
- User direction: "red-team scope on everything we do, including the author's gist as well as the existing paths"

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-04-28 | adam.nowak (via Claude scaffold) | pending | Enabler created. Security boundary captured. |
