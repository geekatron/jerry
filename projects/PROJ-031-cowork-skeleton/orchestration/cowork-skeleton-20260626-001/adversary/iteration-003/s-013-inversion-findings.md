# Inversion Report: PROJ-031-cowork-skeleton Phase-1 Deliverables (Iteration 3)

**Strategy:** S-013 Inversion Technique
**Deliverable:** phase1-requirements.md + ADR-001-skeleton-derived-branch-strategy.md + ADR-002-ci-token-push-strategy.md
**Criticality:** C4
**Date:** 2026-06-26
**Reviewer:** adv-executor (Group E — Decompose) — BLIND INDEPENDENT
**H-16 Compliance:** S-003 Steelman applied in prior strategy sequence (confirmed via iteration context)
**Goals Analyzed:** 8 | **Assumptions Mapped:** 15 | **Vulnerable Assumptions:** 7

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Overall inversion assessment |
| [Goals Inventory](#goals-inventory) | Eight stated and implicit goals with specific, measurable restatements |
| [Anti-Goals Inventory](#anti-goals-inventory) | Inverted failure conditions per goal cluster |
| [Assumption Map](#assumption-map) | Explicit and implicit assumptions across five categories |
| [Findings Table](#findings-table) | IN-001 through IN-007 stress-test results |
| [Detailed Findings](#detailed-findings) | Expanded Major findings IN-001 through IN-005 |
| [Recommendations](#recommendations) | Prioritized mitigations with acceptance criteria |
| [Scoring Impact](#scoring-impact) | Dimensional assessment against S-014 rubric |

---

## Summary

The iteration-3 design is substantially sound: the core determinism / idempotency chain (pinned dates, fixed-length SHA, static stub), the loop-safety triple-guarantee, and the event-discriminated tag sanitization all hold under inversion. However, systematic inversion across the five inverted failure clusters (stale, bloated, broken install, silently compromised, unmaintainable) exposes **five Major and two Minor gaps** that the new iteration-3 controls only partially close. The most significant is structural: the publish-then-assert integrity model colocates the publisher and the reference-value store in the same CI job with the same `contents: write` credentials, so a supply-chain compromise of the workflow can falsify both simultaneously — defeating the non-forgeable comparator. A separate but operationally serious gap is that the Windows symlink workaround documented in REQ-027 is inapplicable in CoWork's automated-clone scenario. Recommendation: **REVISE** — five targeted mitigations before Phase 2 proceeds.

---

## Goals Inventory

| ID | Goal (specific, measurable restatement) |
|----|----------------------------------------|
| G-1 | `cowork-skeleton` tracked file count < 5,000 on a clean clone; CoWork plugin installs within 120 s on a 10 Mbps reference link |
| G-2 | `cowork-skeleton` regenerated within one CI workflow run of every `v*` tag push; never more than one release stale |
| G-3 | Same `v*` tag SHA always yields a bit-identical `cowork-skeleton` tip SHA; re-runs produce no diff |
| G-4 | CoWork user on a fresh install reaches a working first session: H-04 bootstrap (`<project-required>`) fires, `jerry projects list` exits 0, SessionStart hook executes without error |
| G-5 | Any tamper of the published `cowork-skeleton` branch is detected within ≤ 24 h; no silent substitution reaches users for more than one SLA interval |
| G-6 | The CI regeneration push triggers zero downstream workflows; no infinite loop is possible |
| G-7 | The CI push credential is repo-scoped and auto-expires; no long-lived secret is required or stored |
| G-8 | The generation script uses four plain git commands; no new tooling dependency; new maintainers can understand and re-run the pipeline without specialist knowledge |

---

## Anti-Goals Inventory

For each failure cluster requested in the task, the design conditions that would guarantee it — and whether iteration-3 avoids each:

### (a) Guarantee the skeleton ends up STALE
| Condition | Iteration-3 status |
|-----------|-------------------|
| CI fails silently; no detection | Addressed: REQ-016 `if: failure()` step; REQ-037 push-rejection structured diagnostic |
| CI runs but clone-weight exceeds 120 s timeout; future releases blocked | Addressed in design (REQ-034d hard-fail, early-warning): **Phase-6 implementation required** |
| `workflow_dispatch` blank-input resolves to wrong ref (e.g. "main") | Addressed: event-discriminated logic in ADR-001 pseudocode and REQ-036 |
| NFR-006 staleness check runs but fires false negative | Residual: NFR-006 dual-check is a Phase-6 deliverable |

### (b) Guarantee the skeleton becomes BLOATED / over-clone-limit
| Condition | Iteration-3 status |
|-----------|-------------------|
| Growth rate faster than ~2 MB/release, threshold reached sooner than estimated | Partially addressed: REQ-034d per-release emit catches it, but the 2 MB/release estimate is unverified (IN-006) |
| Early-warning band (150 MB) GitHub issue opened but no one acts | Residual: issue is non-blocking; human response required |
| Option B flip deferred until timeout actually occurs in production | Addressed in design: early-warning band and pre-designed flip; MINOR residual |

### (c) Guarantee it BREAKS on a fresh CoWork install
| Condition | Iteration-3 status |
|-----------|-------------------|
| `uv` not installed; SessionStart hook fails at first session with opaque error | Partially addressed: REQ-024/REQ-027 document prerequisite; no in-hook detection (IN-004) |
| Windows: CoWork-managed clone doesn't set `core.symlinks=true`; symlinks arrive as text files | Partially addressed: REQ-027 documents workaround; workaround inapplicable in managed-clone scenario (IN-003) |
| R-001 limit is size/time-based, not file-count-based; branch-stripping fails to resolve the limit | Addressed: REQ-034 four-dimensional gate; dimension (d) deferred with procedural Phase-5 block (IN-005) |
| `projects/README.md` sentinel generated with a timestamp; stub non-static | Addressed: REQ-004a + ADR-001 Stub Determinism Constraint; STORY-002 constrained by ADR |

### (d) Guarantee it is SILENTLY COMPROMISED
| Condition | Iteration-3 status |
|-----------|-------------------|
| CI job compromised; tampered tree pushed AND Release-notes SHA updated to match | NOT FULLY CLOSED: same CI job with same `contents: write` writes both (IN-001) |
| Direct push by collaborator; monitor event leg not yet deployed | Partially addressed in design; Phase-6 implementation required |
| `Source-Commit` trailer used as tamper-detection comparator | Addressed: NFR-006 explicitly uses non-forgeable tip SHA; trailer relegated to staleness only |
| Well-formed rogue tag processed (e.g. attacker pushes `v9.9.9` at malicious commit) | Partially addressed: REQ-036 validates syntax; tag-on-main provenance deferred to Phase-2 (IN-007) |

### (e) Guarantee it is UNMAINTAINABLE
| Condition | Iteration-3 status |
|-----------|-------------------|
| ADR-001 c-003 surface list evolves; REQ-005 not updated | Partially addressed: manual synchronization requirement documented; automated check absent (IN-002) |
| Option B flip is "one-line" in prose but requires correlated monitor-state update | Reviewed: flip is genuinely integrity-neutral post-IT3-004; minor operational coordination needed |
| Generation script isn't version-controlled separately; inline pseudocode drifts from implementation | Residual: pseudocode in ADR-001 is a specification, not the implementation; STORY-001 will implement |

---

## Assumption Map

### Explicit Assumptions

| ID | Assumption | Category | Confidence | Validation Status |
|----|------------|----------|------------|-------------------|
| A-01 | CoWork file limit applies to tracked file count on a clean clone (not local working directory with `.venv/`) | Technical | Medium | Unverified (R-001 open risk) |
| A-02 | GitHub guarantees `GITHUB_TOKEN` pushes cannot re-trigger any workflow | Technical | High | Vendor-documented |
| A-03 | `cowork-skeleton` branch remains unprotected (only "Don't fuck with main" ruleset active) | Environmental | High | Empirically verified 2026-06-26; future-dependent |
| A-04 | Clone weight grows at approximately 2 MB/release; 250 MB trigger is 1–3 years away | Technical | Medium | Asserted, not measured from data |
| A-05 | Event-driven monitor (`on: push: branches: [cowork-skeleton]`) fires reliably on all non-GITHUB_TOKEN direct pushes | Technical | High | Logically derived from GitHub's non-retrigger invariant |

### Implicit Assumptions

| ID | Assumption | Category | Confidence | Validation Status |
|----|------------|----------|------------|-------------------|
| A-06 | REQ-034 dimension (d) (CoWork smoke test) will be completed before Phase 5; the procedural "blocked" declaration will be enforced | Process | Medium | No automated gate; human discipline required |
| A-07 | Phase-6 monitoring implementation (REQ-035, NFR-006, REQ-034d) will be delivered before the skeleton is at operational risk | Process | Medium | Scheduling dependency; Phase-6 is future work |
| A-08 | CoWork plugin users have `uv` installed prior to first session | Resource | Low | Not enforced at install time; required only by hook execution |
| A-09 | `Source-Commit:` trailer is adequate for lazy-staleness detection (not tamper-detection) | Technical | High | Explicitly scoped by NFR-006/ADR-002 |
| A-10 | Option B orphan flip is integrity-neutral after IT3-004 (monitor compares new release SHA, not prior Option A SHA) | Technical | High | Architecturally sound per ADR-002 analysis |
| A-11 | Release tags are treated as immutable; no maintainer force-moves a `v*` tag | Process | Medium | Convention only; no GitHub enforcement on non-protected tags |
| A-12 | ADR-001 c-003 and REQ-005 remain synchronized as documents evolve post-approval | Process | Medium | Has already drifted once (iteration-1 finding); manual discipline required |
| A-13 | The Release notes SHA (published by `cowork-skeleton.yml`) is a trustworthy, independent reference value — i.e., the publisher is separate from or more trusted than the entity being monitored | Technical | Low | FALSE: same CI job with `contents: write` writes both the branch and Release notes |
| A-14 | Blank-input `workflow_dispatch` `git tag -l` fallback always resolves to a valid, already-released tag | Technical | High | Logic sound; edge case: repo with no `v*` tags exits non-zero (correct behavior) |
| A-15 | Symlinks (`.claude/rules`, `.claude/patterns`) resolve correctly in the CoWork client's runtime clone environment | Technical | Medium | REQ-009 tested only in Linux CI; Windows CoWork-managed clone behavior unverified |

---

## Findings Table

| ID | Assumption / Anti-Goal | Type | Confidence | Severity | Evidence | Affected Dimension |
|----|------------------------|------|------------|----------|----------|--------------------|
| IN-001-20260626 | Publisher-assertion independence violated: CI job writes both branch and Release notes SHA | Assumption (A-13) | Low | **Major** | ADR-002 §Continuous Integrity Monitoring; `permissions: contents: write` allows `gh release edit` | Methodological Rigor |
| IN-002-20260626 | Dual-SSOT plugin-retention surface (ADR-001 c-003 and REQ-005 both claim ownership) | Assumption (A-12) | Medium | **Major** | ADR-001 c-003 "REQ-005 mirrors it verbatim"; has already drifted in iteration 1 | Internal Consistency |
| IN-003-20260626 | Windows symlink workaround (`git config core.symlinks true`) inapplicable to CoWork-managed clones | Assumption (A-15) | Medium | **Major** | REQ-027 AC "git config core.symlinks true workaround"; REQ-009 AC "CI Linux environment" | Actionability |
| IN-004-20260626 | `uv` absence produces opaque hook failure at first session; no in-hook detection or user-visible guidance at failure point | Assumption (A-08) | Low | **Major** | REQ-024 "Tutorial Prerequisites"; REQ-027 "`uv`: command not found" failure mode; no hook-level check | Completeness |
| IN-005-20260626 | REQ-034 dimension (d) Phase-5 gate has no automated enforcement; "DEFERRED" artifact records blocking intent procedurally only | Assumption (A-06) | Medium | **Major** | REQ-034 "MAY be deferred to Phase 4"; REQ-034 AC "Any Phase 5 script execution is blocked until all four dimensions show PASS" | Traceability |
| IN-006-20260626 | Clone-weight growth rate (~2 MB/release) asserted but not empirically derived; "1–3 years" estimate could be materially wrong | Assumption (A-04) | Medium | **Minor** | ADR-001 Decision "at ~2 MB/release…1–3 years away"; REQ-034 dimension (b) measures current pack size only | Evidence Quality |
| IN-007-20260626 | Tag-on-main provenance not verified; well-formed rogue tag (e.g. `v9.9.9` pointing at attacker commit) passes REQ-036 allow-list | Anti-Goal (d) | High | **Minor** | ADR-001 §Regeneration Commit Determinism "Scope boundary — syntax vs. provenance (RT-003)"; Phase-2 deferred | Evidence Quality |

---

## Detailed Findings

### IN-001-20260626: Publisher-Assertion Independence Violated [MAJOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Type** | Assumption failure (A-13) |
| **Section** | ADR-002 §Continuous Integrity Monitoring; REQ-035 |
| **Strategy Step** | Step 4 (stress-test A-13) |

**Original Assumption:** The GitHub Release notes serve as a "durable, off-branch, protected surface" for the expected deterministic SHA — a reference value independent of the branch being monitored.

**Inversion:** The `cowork-skeleton.yml` job that force-pushes the branch also runs `gh release edit v{TAG} --notes-append "cowork-skeleton-sha: <SHA>"`. The job's declared `permissions: contents: write` is sufficient for both operations. A supply-chain compromise of the workflow (e.g., via a compromised pinned Action SHA despite REQ-017, or via a malicious workflow step injected through a prior step's output) can simultaneously push a tampered tree and publish the tampered tree's SHA to Release notes. The integrity monitor then compares live-tip-SHA (tampered) against published-SHA (also tampered to match) and returns PASS. The non-forgeable comparator (IT3-004) is mathematically sound, but the independence of the publisher is not established.

**Plausibility:** Low-to-Medium for a highly targeted attack; but the architectural gap exists regardless of attack probability. The ADR's "protected surface" framing is misleading as stated.

**Consequence:** The detect-and-alert model silently fails for the class of attacks where the CI workflow is compromised, which is also the highest-blast-radius supply-chain attack scenario (REQ-017's SHA-pinning mitigates but does not eliminate this). The model correctly detects out-of-band direct pushes (RT-01); it does not detect compromised-CI pushes.

**Evidence:** ADR-002 §Continuous Integrity Monitoring: *"(1) Publish…CI publishes the expected deterministic tip SHA for the release to a durable, off-branch, protected surface — the GitHub Release notes…Releases are governed by main/release permissions."* The `permissions: contents: write` declaration at ADR-002 §Decision permits `gh release edit` from the same job.

**Mitigation:** Publish the expected SHA to a surface the generating job cannot write to under `contents: write`. Options in ascending implementation complexity:
- (a) Publish the expected SHA to a protected branch or tag annotation (requires a separate job with different permission scope, or writing to `main` via a dedicated step that requires pull-request approval — Phase-2 STRIDE scope).
- (b) Have a separate monitoring workflow that independently recomputes the expected SHA by re-running the deterministic algorithm against the source tag, rather than comparing against a CI-published value. This eliminates the dependency on the published value entirely.
- Minimum Phase-1 action: add a disclosure note to ADR-002 §Continuous Integrity Monitoring acknowledging that CI-compromise attacks on the "protected surface" are not detected; document this as an accepted residual risk or a Phase-2 remediation item.

**Acceptance Criteria:** ADR-002 §Continuous Integrity Monitoring explicitly states the trust model boundary: detection covers out-of-band (direct-push) tampering; CI-compromise tampering is a Phase-2 threat-model scope item. OR: a separate recomputation mechanism is specified that does not rely on the generating job's published SHA.

---

### IN-002-20260626: Dual-SSOT Plugin-Retention Surface [MAJOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Type** | Assumption failure (A-12) |
| **Section** | ADR-001 §Canonical Plugin-Retention Surface; REQ-005 |
| **Strategy Step** | Step 4 (stress-test A-12) |

**Original Assumption:** ADR-001 c-003 is the single source of truth for the plugin-retention surface; REQ-005 "mirrors it verbatim." Manual synchronization discipline keeps them aligned.

**Inversion:** As the project progresses through approval gates and implementation phases, ADR-001 may be revised (STORY-001 may surface additional directories; Phase-2 STRIDE may add entries) without a corresponding REQ-005 update, or vice versa. The iteration-1 review already found them out of sync.

**Plausibility:** High — the documents are in separate files, maintained by different agents in different phases. The stated solution ("changes to the surface list require updating both documents") is a governance instruction with no automated enforcement.

**Consequence:** The generation script (STORY-001) and the acceptance test (STORY-003 / REQ-005 AC) verify against REQ-005's list; the actual plugin surface is ADR-001 c-003. A drift means the acceptance test either passes for a skeleton that strips a required directory, or requires a directory that the ADR no longer mandates. Both produce silent functional regressions.

**Evidence:** ADR-001 §Canonical Plugin-Retention Surface: *"REQ-005 mirrors it verbatim… changes to the surface list require updating both documents."* Iteration-1 finding: ADR-001 c-003 and REQ-005 enumerated different directory sets (`commands/`, `src/`, `schemas/`, `marketplace.json` absent from one or the other).

**Mitigation:** Add a CI lint step (Phase-6 scope) that parses both ADR-001 c-003 table and REQ-005 table entries and asserts they are identical. Alternatively, collapse to a single data source: define the surface list in a separate YAML/JSON file (`retention-surface.yml`) imported by both the generation script and the acceptance test; ADR-001 and REQ-005 reference this file rather than embedding the list.

**Acceptance Criteria:** Either (a) a CI check exists that fails if ADR-001 c-003 and REQ-005 enumerated surfaces diverge, or (b) the list is defined exactly once in a machine-readable artifact and both documents reference it with no inline copy.

---

### IN-003-20260626: Windows Symlink Workaround Inapplicable in CoWork-Managed Clone [MAJOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Type** | Assumption failure (A-15) |
| **Section** | REQ-027; REQ-009 |
| **Strategy Step** | Step 4 (stress-test A-15) |

**Original Assumption:** REQ-027's documented `git config core.symlinks true` workaround is actionable for Windows CoWork plugin users.

**Inversion:** CoWork's plugin installation clones `geekatron/jerry@cowork-skeleton` using its own internal git operation. The user does not control this clone; they cannot set `core.symlinks=true` prior to CoWork's automated clone. On Windows, where the git default is `core.symlinks=false`, the clone produces `.claude/rules` and `.claude/patterns` as plain text files containing the symlink path string — not as actual symlinks. The Jerry auto-loading mechanism (H-22, L1 rule injection) silently fails for all Windows CoWork users.

**Plausibility:** High for Windows users of Claude Desktop / CoWork — `core.symlinks=false` is the Windows default unless the user has specifically enabled symlink support in git configuration globally.

**Consequence:** Goal G-4 (working first session) is not met for Windows users. The failure is silent: the `skills/*.md` and `.context/rules/*.md` framework rules do not auto-load. Jerry responds as if no rules exist. The user receives no error message — they simply get a non-Jerry-configured Claude session.

**Evidence:** REQ-027 AC: *"How-To troubleshooting doc contains…a Windows symlinks note."* REQ-009 AC: *"In `cowork-skeleton`: `readlink -f .claude/rules`…both resolve to non-empty, existing paths (CI Linux environment)."* The AC explicitly scopes the verification to CI Linux; no Windows CoWork verification is specified.

**Mitigation:** (a) Evaluate whether CoWork's plugin git clone can be configured for symlinks — if Anthropic exposes a git config surface in CoWork plugin settings, document it. (b) If not configurable: replace the symlinks (`.claude/rules`, `.claude/patterns`) with actual directory copies in the `cowork-skeleton` branch, or generate non-symlink equivalents during skeleton generation. The skeleton generation script can resolve and copy the symlink targets rather than preserving symlinks. (c) Minimum Phase-1 action: update REQ-027 and REQ-009 to state this as an open known-broken failure mode for Windows CoWork users (not just a "workaround exists" — the workaround is inapplicable). Escalate to a requirements gap for Phase-4 documentation or Phase-5 skeleton generation.

**Acceptance Criteria:** Either (a) skeleton generation resolves symlinks to actual directories on the generated branch (verified: `git ls-files .claude/rules` returns files, not a symlink entry), or (b) REQ-009 acceptance criterion includes a Windows clone test, or (c) the Windows case is formally accepted as out-of-scope with a clear statement in REQ-027 that CoWork Windows install is unsupported pending a fix.

---

### IN-004-20260626: Silent `uv` Failure at First Session [MAJOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Type** | Assumption failure (A-08) |
| **Section** | REQ-024; REQ-027; STK-003 |
| **Strategy Step** | Step 4 (stress-test A-08) |

**Original Assumption:** CoWork plugin users have `uv` installed, or will install it after reading the Tutorial Prerequisites section.

**Inversion:** A user installs `geekatron/jerry@cowork-skeleton` via CoWork (install succeeds), opens a new CoWork session, and the SessionStart hook fires `hooks/session-start.py`. That script calls `uv run jerry session …`. With `uv` absent, the OS produces: `bash: uv: command not found` (or equivalent). The CoWork client may display this as a hook failure or silently swallow it. Either way, the user has no contextual guidance within the session — they must already know to search the Tutorial documentation.

**Plausibility:** High. `uv` is not a standard system package on any major OS. CoWork users who installed the plugin from the marketplace may never have visited the Tutorial; the marketplace listing does not surface prerequisites. The install succeeds without `uv`, so the user has no reason to expect a hook failure.

**Consequence:** Goal G-4 (working first session, STK-003 "immediately usable") fails. The iteration-3 remediation added `uv` documentation to REQ-024 and REQ-027, but documentation is a partial mitigation: it requires the user to read the Tutorial before encountering the failure.

**Evidence:** REQ-024: *"Tutorial SHALL include a 'Prerequisites' step…documenting `uv` (≥ 0.5)…"* REQ-027: *"How-To…SHALL document '`uv`: command not found' as a named hook-execution failure mode with recovery path."* No requirement addresses `hooks/session-start.py` detecting `uv` absence and emitting a user-visible diagnostic.

**Mitigation:** Add a `uv` presence check to `hooks/session-start.py` (STORY-002 or a new STORY) that runs before the `uv run jerry` invocation and emits a structured, user-visible error message containing: the exact failure reason, the install command (`curl -LsSf https://astral.sh/uv/install.sh | sh`), and a reference to the Tutorial. This converts a cryptic OS error into an actionable in-session guidance prompt. The check is a one-line `which uv || echo "…"` gate before the `uv run` call.

**Acceptance Criteria:** In a test session where `uv` is not in `$PATH`, the SessionStart hook emits a human-readable message identifying `uv` as missing and providing the install command. The hook exits non-zero. This behavior is demonstrated by the STORY that implements `hooks/session-start.py`.

---

### IN-005-20260626: REQ-034 Dimension (d) Phase-5 Gate Has No Automated Enforcement [MAJOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Type** | Anti-goal (c) — design gap for guarantee-stale/broken |
| **Section** | REQ-034; R-001 §Verification Approach |
| **Strategy Step** | Step 2 (anti-goal for G-1) and Step 4 (stress-test A-06) |

**Original Assumption:** The procedural declaration ("Phase 5 is blocked until all four dimensions show PASS") is sufficient to prevent Phase 5 from proceeding without a completed REQ-034 dimension (d).

**Inversion:** Dimension (d) — installing `geekatron/jerry@cowork-skeleton` in a live CoWork runtime — is the only direct falsification of the project's central premise (ADR-001's "decisive framing": CoWork materializes the tip working tree). It is the only test that can actually break the strategy. It is also the most deferred test (MAY be deferred to Phase 4 completion). The "DEFERRED — required before Phase 5" artifact entry is a prose statement, not a machine-checkable gate. If the CoWork runtime remains unavailable, there is no automated mechanism that prevents Phase-5 implementation scripts from being prepared and submitted for AG approval.

**Plausibility:** Medium. The orchestration relies on human governance (AG-02 through AG-10 approval gates) to enforce phase sequencing. But the approval gate questions (AG-01 through AG-10) may not explicitly reference the dimension (d) PASS/FAIL status, and an operator under schedule pressure may proceed without it.

**Consequence:** Phase 5 implementation scripts execute, CI workflow is committed, `cowork-skeleton` is published — and only after public availability does a user discover that CoWork does not, in fact, resolve the file-count limit (or times out, or has a size-based limit). This is the highest-consequence failure mode in the entire project.

**Evidence:** REQ-034: *"dimension (d) MAY be deferred to Phase 4 completion if a CoWork runtime is unavailable before Phase 2; the artifact SHALL record 'DEFERRED — required before Phase 5' and Phase 5 is blocked until completed."* There is no REQ, gate-item, or approval criterion that explicitly verifies dimension (d) PASS before any AG-0x approval for Phase 5 actions.

**Mitigation:** Add dimension (d) status as an explicit approval gate item. Either: (a) add `AG-N: Confirm REQ-034 dimension (d) shows PASS (not DEFERRED)` to the approval gate list before Phase 5 actions, or (b) add a Phase-4 completion criterion that requires the `verification/R001-clean-clone-count.md` file to show PASS on all four dimensions (not DEFERRED) before Phase 4 is marked complete. Escalation: if dimension (d) cannot be completed before Phase 5, this is a required scope-pivot decision (user authority per H-02/P-020) — not a silent deferral.

**Acceptance Criteria:** The Phase-5 approval gate (whichever AG item covers implementation authorization) includes an explicit check of `verification/R001-clean-clone-count.md` dimension (d) status = PASS. The ORCHESTRATION_PLAN.md approval gate table is updated to reflect this dependency.

---

### IN-006-20260626: Clone-Weight Growth Rate Unverified [MINOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Minor |
| **Type** | Assumption failure (A-04) |
| **Section** | ADR-001 §Clone-Weight Decision; REQ-034 dimension (b); REQ-034d |
| **Strategy Step** | Step 4 (stress-test A-04) |

**Original Assumption:** Clone weight grows at approximately 2 MB/release, placing the 250 MB flip trigger "dozens of releases (1–3 years)" away.

**Inversion:** The ~2 MB/release figure is described as "empirically" observed but no measurement source is cited in ADR-001. REQ-034 dimension (b) establishes a current baseline `size-pack:` measurement at Phase 2. It does not require calculating the per-release growth rate. Without a measured rate, the 1–3 year estimate is unverifiable; if the rate is 5 MB/release (e.g., due to binary skill test-data files growing), the 250 MB trigger is 50 releases away — potentially within 2 years at current release cadence — and the early-warning at 150 MB arrives at release 30.

**Evidence:** ADR-001 Decision: *"at ~2 MB/release the 250 MB trigger is dozens of releases (1–3 years) away, not imminent."* No citation or calculation. REQ-034 dimension (b) AC: *"`git count-objects -vH` output showing `size-pack:` in MB with PASS/FAIL determination."* No AC for per-release growth rate.

**Mitigation:** Extend REQ-034 dimension (b) to calculate the per-release growth rate: subtract the oldest-tag pack size from the current pack size and divide by the number of releases. Alternatively, compute `git log --format="%H" v* | wc -l` as the release count and derive a rough rate. Document the measured rate in `verification/R001-clean-clone-count.md` alongside the "N releases to flip trigger" calculation.

**Acceptance Criteria:** `verification/R001-clean-clone-count.md` contains an estimated per-release growth rate (MB/release) derived from at least two data points, and a derived "estimated releases to 250 MB trigger" calculation.

---

### IN-007-20260626: Tag Provenance Gap Enables Well-Formed Rogue Tags [MINOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Minor |
| **Type** | Anti-goal (d) — silently compromised |
| **Section** | ADR-001 §Regeneration Commit Determinism RT-003; REQ-036 |
| **Strategy Step** | Step 2 (anti-goal for G-5) |

**Original Assumption:** The REQ-036 allow-list (`^v[0-9]+\.[0-9]+(\.[0-9]+)?$`) is the primary gate for the tag input; Phase-2 STRIDE will add provenance verification.

**Inversion:** A repository collaborator pushes `v9.9.9` pointing at a commit that introduces a backdoor in the skeleton, then triggers `workflow_dispatch` with `inputs.target_tag=v9.9.9`. The tag passes the allow-list. CI generates a legitimate-looking skeleton from a malicious source commit, publishes it as `cowork-skeleton`, and records the SHA in Release notes. The integrity monitor checks the SHA and passes (the SHA is deterministically correct for the malicious tree). Detection depends on the Phase-2 STRIDE control ("tag-on-main provenance assertion"), which is explicitly deferred.

**Plausibility:** Low — requires a repository collaborator with tag-push and `workflow_dispatch` permission. The Phase-2 deferral is acknowledged and justified. The integrity monitor is the compensating control for what it can detect.

**Evidence:** ADR-001 §Tag-name sanitization: *"A well-formed but illegitimate tag…passes the allow-list. Asserting that the resolved tag points at a commit reachable from `main`…is a provenance control…delegated to the Phase-2 STRIDE threat model (STORY-004)."*

**Mitigation:** Acceptable as a Phase-2 deferred item provided the Phase-2 STRIDE explicitly includes tag-on-main provenance assertion as a required control (not optional). Minimum Phase-1 action: confirm that the Phase-2 STRIDE entry point in ORCHESTRATION_PLAN.md explicitly references RT-003 / "tag-on-main provenance assertion" as a Phase-2 entry item — not merely mentioned in ADR-001 prose.

**Acceptance Criteria:** ORCHESTRATION_PLAN.md Phase-2 (STRIDE / STORY-004) scope explicitly includes: "Assert that the resolved tag's commit is reachable from `main` (git merge-base --is-ancestor <commit> main)." This is tracked as a Phase-2 deliverable, not left as an ADR footnote.

---

## Recommendations

### MUST Mitigate (Major findings)

| ID | Finding | Action | Acceptance Criterion |
|----|---------|--------|---------------------|
| IN-001-20260626 | Publisher-assertion independence violated | Add explicit trust-model disclosure to ADR-002 §CIM: state that CI-compromise attacks are outside the detect-and-alert model scope; OR specify an independent SHA-recomputation path (Phase-2 STRIDE scope) | ADR-002 states the detection boundary; "protected surface" framing removed or qualified |
| IN-002-20260626 | Dual-SSOT plugin-retention surface | Add Phase-6 CI lint step asserting ADR-001 c-003 and REQ-005 lists are identical; OR consolidate to one machine-readable data source | No two documents contain the surface list as independent text |
| IN-003-20260626 | Windows symlink workaround inapplicable in CoWork | Update REQ-027 to state Windows CoWork install is currently broken (not "workaround available"); escalate to Phase-5 generation script to copy symlink targets rather than preserve symlinks | REQ-009 either includes a Windows CoWork clone test, or symlinks are resolved in the generated branch tree |
| IN-004-20260626 | Silent `uv` failure at first session | Add `uv` presence check to `hooks/session-start.py` with user-visible error and install command | Hook emits actionable message when `uv` absent; demonstrated in STORY acceptance test |
| IN-005-20260626 | REQ-034 dimension (d) gate has no automated enforcement | Add explicit dimension-d PASS requirement as an approval gate criterion before Phase-5 authorization | AG gate or Phase-4 completion criterion verifies dimension (d) = PASS before Phase-5 work begins |

### SHOULD Mitigate (Minor findings)

| ID | Finding | Action | Acceptance Criterion |
|----|---------|--------|---------------------|
| IN-006-20260626 | Clone-weight growth rate unverified | Extend REQ-034 dimension (b) to derive per-release growth rate and "N releases to trigger" estimate | `verification/R001-clean-clone-count.md` contains derived growth rate with data-point basis |
| IN-007-20260626 | Tag provenance gap | Confirm ORCHESTRATION_PLAN.md Phase-2 scope includes RT-003 tag-on-main assertion as a named deliverable | Phase-2 scope entry references RT-003 explicitly |

---

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Negative | IN-004 (silent `uv` failure closes G-4 partially), IN-005 (dimension-d deferral leaves G-1 verification incomplete), IN-003 (Windows path breaks G-4 for a significant user segment) |
| Internal Consistency | 0.20 | Negative | IN-002 (dual-SSOT plugin surface is architecturally inconsistent: two documents claim ownership of the same list with no automated arbiter); minor inconsistency between ADR-002's "protected surface" claim and the actual permission boundary |
| Methodological Rigor | 0.20 | Negative | IN-001 (the publish-then-assert model's independence property is asserted but not established; the rigorous model requires independent publisher and assertor); IN-006 (growth rate asserted without empirical basis) |
| Evidence Quality | 0.15 | Neutral | The iteration-3 additions (REQ-035/036/037, NFR-006 dual-check, four-dimensional gate) are well-evidenced. Deductions for A-04 growth rate estimate and A-13 independence assumption, but these are partially offset by the genuine care in the broader evidence base |
| Actionability | 0.15 | Negative | IN-003 (documented workaround is inapplicable — a documented-but-unactionable mitigation is worse than acknowledged absence); IN-004 (REQ-024/REQ-027 address the documentation but not the failure itself) |
| Traceability | 0.10 | Neutral | Overall traceability is strong; every ADR-002 CC traces to a SHALL requirement (IT3-001 closed). Minor gap: IN-007 provenance deferral exists in ADR prose but Phase-2 STRIDE scope entry is not confirmed |

**Overall assessment:** Five Major findings, two Minor. The design is structurally sound but has five targeted gaps in the new iteration-3 controls. All five Major findings have concrete, implementable mitigations that do not require design rethinking. Recommended disposition: REVISE (targeted mitigations deliverable within Phase 1 or at Phase 2 entry) before the composite QG-1 score is recorded.

---

## Execution Statistics

- **Total Findings:** 7
- **Critical:** 0
- **Major:** 5
- **Minor:** 2
- **Goals Analyzed:** 8
- **Assumptions Mapped:** 15 (5 explicit, 10 implicit)
- **Vulnerable Assumptions:** 7
- **Protocol Steps Completed:** 6 of 6

---

*Strategy: S-013 Inversion Technique*
*Template: .context/templates/adversarial/s-013-inversion.md (v1.0.0)*
*Deliverable: PROJ-031-cowork-skeleton Phase-1 iteration-3 (phase1-requirements.md, ADR-001, ADR-002)*
*Executed: 2026-06-26T00:00:00Z*
*Reviewer: adv-executor (Group E — Decompose, BLIND INDEPENDENT)*
*Finding Prefix: IN-NNN-20260626*
