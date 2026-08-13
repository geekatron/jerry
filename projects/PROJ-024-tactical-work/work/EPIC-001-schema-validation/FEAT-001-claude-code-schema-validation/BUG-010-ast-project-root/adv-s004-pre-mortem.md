# Pre-Mortem Report: BUG-010 `jerry ast` Path-Containment Widening (PR #341)

**Strategy:** S-004 Pre-Mortem Analysis
**Deliverable:** `src/interface/cli/project_root.py`, `src/interface/cli/ast_commands.py` (+ `parser.py`/`main.py` wiring), branch `fix/BUG-010-ast-project-root`, PR #341
**Criticality:** C4 (tournament) — Group C, blind executor
**Date:** 2026-08-07
**Reviewer:** adv-executor (agent), S-004 strategy
**H-16 Compliance:** ASSUMED per tournament group ordering (steelman group precedes challenge group per the orchestrator's documented 6-group sequence: self-refine → steelman → challenge → verify → decompose → score). This blind executor was not given a direct file path to a prior S-003 Steelman artifact and did not independently verify one exists. Per P-022, this is disclosed rather than silently assumed satisfied; if S-003 has not in fact run, this finding set should be treated as provisional pending steelman strengthening.
**Failure Scenario:** It is February 2027 (6 months post-merge). `jerry ast` has shipped as part of both the Claude Code plugin and — per the owner's stated roadmap — an extracted standalone `pip`-installable CLI invoked from CI pipelines, cron jobs, and third-party automation outside any Claude Code session. An incident review is underway after `jerry ast modify` silently operated far outside a user's intended project during an unattended CI job, and separately, a shared CI runner's `/tmp` was found to have been read by a `jerry ast` invocation belonging to a different pipeline/tenant despite the H-01 ownership-gate remediation already having shipped.

---

## Summary

Nine failure causes were identified across all 5 category lenses (Technical, Process, Assumption, External, Resource), extending beyond the two findings the prior red-vuln (RED-BUG010) pass already confirmed and remediated (H-01 ownership gate, H-02 broad-root warning). **2 Critical (P0)**, **1 Major (P1)**, and **6 Major/Minor (P2)** causes were found. The dominant risk pattern is not a new vulnerability class but **incomplete generalization of the already-shipped mitigations**: the broad-root warning and the ownership gate were both scoped narrowly (to `--root` only, and to temp-default-root matches only, respectively) in ways that leave the *default, no-flag* invocation path — the path a standalone pip package will hit hardest — silently unprotected in exactly the scenarios the owner's roadmap explicitly names. **Recommendation: REVISE before the standalone-package extraction proceeds** — the two P0 findings (PM-001, PM-002) directly undermine the H-01/H-02 remediations' stated intent under conditions the code review evidence shows are already reachable today, not merely hypothetical.

---

## Findings Table

| ID | Failure Cause | Category | Likelihood | Severity | Priority | Affected Dimension |
|----|---------------|----------|------------|----------|----------|--------------------|
| PM-001-20260807T1400 | Default project root (`CLAUDE_PROJECT_DIR`/cwd) is never broadness-checked; R-4 transparency note is explicitly suppressed for project-root matches | Technical | High | Critical | P0 | Internal Consistency |
| PM-002-20260807T1400 | H-01 ownership gate fails open on `stat()` `OSError`, most likely exactly on the shared/networked storage it was built to protect | Technical | Medium | Critical | P0 | Methodological Rigor |
| PM-003-20260807T1400 | `ast_modify` write-time TOCTOU recheck omits the ownership gate present at read time | Technical | Medium | Major | P2 | Internal Consistency |
| PM-004-20260807T1400 | R-3/R-4 stderr transparency notes assume a human reads stderr; silently discarded in headless CI/cron automation | Assumption | High | Major | P1 | Completeness |
| PM-005-20260807T1400 | Ownership gate assumes UID uniquely identifies a tenant; breaks when multiple containers/pods share a host `/tmp` and all run as root (uid 0) | Assumption | Medium | Major | P2 | Methodological Rigor |
| PM-006-20260807T1400 | `tempfile.gettempdir()` can raise in minimal/distroless containers; called unconditionally, crashing every `jerry ast` invocation, not just temp-adjacent ones | External | Low | Major | P2 | Completeness |
| PM-007-20260807T1400 | No enforced parity mechanism between read-time and write-time containment logic as the pattern is asked to scale to new CLI surfaces | Process | Medium | Major | P2 | Actionability |
| PM-008-20260807T1400 | `Path.home()` resolution failure in minimal/rootless containers silently degrades the ancestor-of-home broadness check to exact-root-only | Technical | Low | Minor | P2 | Evidence Quality |
| PM-009-20260807T1400 | Pattern-consolidation work (eng-lead's own recommendation) explicitly deferred as "premature," with no trigger tied to the standalone-package extraction milestone that would exercise it | Resource | Medium | Major | P2 | Traceability |

**Finding ID Format:** `PM-{NNN}-{execution_id}`, `execution_id = 20260807T1400` (this blind-executor session).

---

## Finding Details

### PM-001: Default containment root has zero broadness protection [CRITICAL]

**Failure Cause:** `get_containment_roots()` only calls `_is_broad_containment_root()` on the `explicit_root` (`--root`) branch. The default branch — `[get_project_root().resolve(), Path(tempfile.gettempdir()).resolve(), ...]` — never checks whether the resolved project root itself is unusually broad. Compounding this, `_is_temp_default_root_match()` treats any match against `allowed_roots[0]` (the project root) as *not* a temp-default match, which suppresses the R-4 transparency note precisely for project-root matches — the one case where, if the project root itself is anomalously broad, the user most needs a signal.

**Category:** Technical
**Likelihood:** High — justified because the owner has stated the CLI will be extracted into a standalone `pip` package invoked "in unforeseen contexts." Outside Claude Code, `CLAUDE_PROJECT_DIR` is not set by any host process, so `get_project_root()` falls through to `Path.cwd()`. `cwd` in cron jobs, systemd units, minimal container `ENTRYPOINT`s, and CI steps that fail to `cd` into the checkout is a well-known source of accidental `/`, `$HOME`, or container-root working directories — the exact class of value `_is_broad_containment_root` already exists to catch, just not on this code path.
**Severity:** Critical — in the worst case (cwd or `CLAUDE_PROJECT_DIR` resolves to `/` or `$HOME`), containment for both `jerry ast <cmd>` reads and the `ast_modify` write path becomes functionally equivalent to `--root /` — but *without* even the WARNING that explicit `--root /` receives. This is a strictly worse outcome than the already-accepted "user discretion" `--root` policy, because there is no discretion exercised and no signal given.
**Evidence:** `src/interface/cli/project_root.py:159-177` (`get_containment_roots`, default branch, lines 171-177) never invokes `_is_broad_containment_root`; contrast with lines 159-169 (`explicit_root` branch) which does. `_is_temp_default_root_match()` (`ast_commands.py:181-209`) returns `False` for a project-root match, which is exactly the input that suppresses `_warn_if_temp_root_match` (`ast_commands.py:212-241`).
**Dimension:** Internal Consistency — the codebase applies broadness protection asymmetrically to two structurally identical "resolve a directory and trust it as a containment root" code paths.
**Mitigation:** Apply `_is_broad_containment_root()` to `get_project_root().resolve()` in the default branch of `get_containment_roots()` with the same stderr WARNING behavior as the `--root` case, regardless of which allowed root a given file ultimately matches. Do not gate this on `_is_temp_default_root_match` — the project root itself being broad is orthogonal to whether a *specific file* matched via the project root or a temp root.
**Acceptance Criteria:** A new test sets `CLAUDE_PROJECT_DIR` (or, with `monkeypatch.chdir`, cwd) to `/`, `Path.home()`, or an ancestor of `Path.home()`, and asserts `get_containment_roots()` prints the same stderr WARNING format used for broad `--root` values — with no `--root` flag supplied.

---

### PM-002: Ownership gate fails open on `stat()` `OSError`, most likely on the storage class it protects [CRITICAL]

**Failure Cause:** `_check_temp_root_ownership()` catches `OSError` from `resolved.stat()` and returns `None` (treated as "ownership verified" / no error) — a deliberate fail-open documented in the code comment ("Fail open on stat error"). `stat()` failures (permission-denied on exotic mounts, NFS stale-handle errors, network filesystem timeouts, FUSE/9p translation errors) are disproportionately likely on precisely the shared/networked, multi-tenant storage that motivated the H-01 remediation in the first place — CI fleets increasingly back ephemeral storage (including `/tmp`) with network-attached or overlay filesystems.
**Category:** Technical
**Likelihood:** Medium — requires a shared/CI host with a storage backend prone to transient `stat()` errors; this is a common but not universal CI architecture (self-hosted runners with NFS-backed workspaces, some Kubernetes `emptyDir`/`hostPath` configurations under load).
**Severity:** Critical — a fail-open security control that is statistically more likely to fail open exactly where the threat model is realized (a hostile co-tenant's file, potentially on flakier storage) provides materially less protection than its passing test suite suggests. This directly undermines the confidence red-vuln's report placed in H-01 as "the highest-leverage, lowest-cost fix."
**Evidence:** `src/interface/cli/ast_commands.py:282-287` (`_check_temp_root_ownership`), the `except OSError: pass` block.
**Dimension:** Methodological Rigor — the remediation was validated (per red-vuln's report and the existing test suite) against the happy path and the "different owner" path, but not against the "ownership cannot be determined" path under the deployment model where that path is most probable.
**Mitigation:** For temp-default-root matches specifically (never the project root or an explicit `--root`, preserving existing policy), either (a) fail closed on `OSError` — treat "cannot verify ownership" as "reject," or (b) if fail-open is retained for availability reasons, emit a stderr warning so the silent-degradation is at minimum observable, mirroring R-4's transparency philosophy.
**Acceptance Criteria:** A test that monkeypatches `Path.stat` to raise `OSError` for a temp-root-matched path and asserts either rejection or a stderr warning — not silent, unconditional success.

---

## Recommendations

### P0 (MUST mitigate before acceptance)

- **PM-001-20260807T1400:** Extend `_is_broad_containment_root()` broadness checking and stderr WARNING to the default (non-`--root`) project-root resolution path. Acceptance: test proves the warning fires for a broad `CLAUDE_PROJECT_DIR`/cwd with no `--root` supplied.
- **PM-002-20260807T1400:** Change the ownership-check fail-open behavior on `OSError` for temp-default-root matches to either fail closed or emit an observable warning. Acceptance: test proves `stat()` `OSError` no longer silently degrades to unconditional allow.

### P1 (SHOULD mitigate)

- **PM-004-20260807T1400:** Add a machine-readable signal (JSON field or `--strict` fail-closed flag) for the broad-root/temp-match conditions, since stderr text is not a reliable channel in headless automation — the deployment context the standalone-pip-package roadmap explicitly targets. Acceptance: documented in README/CHANGELOG at minimum; `--strict` flag is the stronger acceptance bar.

### P2 (MAY mitigate; acknowledge risk)

- **PM-003-20260807T1400:** Extract the ownership-gate call into a helper shared by both the read-time check and the `ast_modify` write-time TOCTOU recheck, closing the asymmetry before a future refactor of the write path silently relies on containment-only re-verification.
- **PM-005-20260807T1400:** Document the UID-convergence limitation explicitly (root-in-container tenants sharing a host temp mount are indistinguishable to `st_uid`); track as a follow-up if containerized-CI becomes a material deployment target.
- **PM-006-20260807T1400:** Wrap `tempfile.gettempdir()` in `get_containment_roots()` in a try/except, degrading to project-root-only rather than crashing every `jerry ast` invocation when no writable temp candidate exists.
- **PM-007-20260807T1400 / PM-009-20260807T1400:** Convert eng-lead's own "future house pattern" recommendation (`get_containment_roots` as the reusable template for future filesystem-touching CLI surfaces) from an aside into an explicit, tracked precondition of the standalone-pip-package extraction milestone, with a contract/architecture test preventing new surfaces from reimplementing containment ad hoc.
- **PM-008-20260807T1400:** Add a well-known-paths fallback (`/`, `/root`, `/home`, `/Users`) for the case where `Path.home()` itself cannot be resolved, so minimal/rootless containers do not silently lose the ancestor-of-home broadness check entirely.

---

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Negative | PM-001, PM-004, PM-006: the current Acceptance Criteria checklist in BUG-010 does not cover default-root broadness, automation-context signaling, or `tempfile.gettempdir()` failure handling. |
| Internal Consistency | 0.20 | Negative | PM-001, PM-003: broadness checking and the ownership gate are each applied to only one of two structurally parallel code paths (default vs. `--root`; read-time vs. write-time). |
| Methodological Rigor | 0.20 | Negative | PM-002, PM-005: the ownership-gate validation did not stress-test the "verification itself fails" and "UID convergence under containerization" cases, despite CI already running a multi-OS matrix that could exercise adjacent conditions. |
| Evidence Quality | 0.15 | Positive | This pre-mortem builds directly on red-vuln's already-strong, code-executed evidence base (H-01/H-02); every new finding here cites the exact function/line generalizing or extending that prior work, not speculation. |
| Actionability | 0.15 | Positive | Every P0/P1 finding has a concrete code-level fix and a specific, testable acceptance criterion. |
| Traceability | 0.10 | Positive | All 9 findings trace to specific lines in `project_root.py`/`ast_commands.py` and explicitly cross-reference the prior eng-lead plan and red-vuln report they extend. |

---

## Ranked Failure Scenarios (Likelihood x Impact)

1. **PM-001 (P0, Critical/High):** Default project-root broadness blind spot — the single most likely incident given the explicit standalone-pip-package/"unforeseen contexts" roadmap; worse than the already-accepted `--root` policy because it gives zero signal.
2. **PM-002 (P0, Critical/Medium):** Ownership gate fails open on `stat()` `OSError`, disproportionately on the shared/networked storage it exists to protect.
3. **PM-004 (P1, Major/High):** stderr-only transparency notes are invisible in headless CI/cron automation — the primary invocation mode of a standalone pip package.
4. **PM-003 (P2, Major/Medium):** Write-time TOCTOU recheck omits the ownership gate present at read time.
5. **PM-005 (P2, Major/Medium):** UID-based ownership check collapses under container-root-uid convergence on shared hostPath/bind-mounted temp storage.
6. **PM-009 (P2, Major/Medium):** Pattern-consolidation deferred with no trigger tied to the exact milestone (standalone extraction) that would need it.
7. **PM-007 (P2, Major/Medium):** No enforced parity mechanism as the containment pattern is asked to cover new CLI surfaces.
8. **PM-006 (P2, Major/Low):** `tempfile.gettempdir()` failure in minimal/distroless containers crashes the entire `ast` namespace, not just temp-adjacent calls.
9. **PM-008 (P2, Minor/Low):** `Path.home()` resolution failure silently narrows the ancestor-of-home broadness check in rootless/minimal containers.

---

## Execution Statistics

- **Total Findings:** 9
- **Critical:** 2 (PM-001, PM-002)
- **Major:** 6 (PM-003, PM-004, PM-005, PM-006, PM-007, PM-009)
- **Minor:** 1 (PM-008)
- **Protocol Steps Completed:** 6 of 6 (Set the Stage, Declare Failure, Generate Failure Causes, Prioritize, Develop Mitigations, Synthesize and Score)

---

*S-004 Pre-Mortem execution — adv-executor, Group C blind reviewer, C4 tournament.*
*Deliverable reviewed: `fix/BUG-010-ast-project-root` (PR #341) — `src/interface/cli/project_root.py`, `src/interface/cli/ast_commands.py`, `parser.py`, `main.py` wiring.*
*Cross-referenced: `eng-lead-implementation-plan.md`, `red-vuln-findings.md` (RED-BUG010), `BUG-010-ast-project-root.md`.*
