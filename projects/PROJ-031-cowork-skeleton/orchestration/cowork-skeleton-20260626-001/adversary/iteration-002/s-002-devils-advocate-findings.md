# Devil's Advocate Report: PROJ-031 CoWork Skeleton — Phase 1 Deliverables (Iteration 2)

**Strategy:** S-002 Devil's Advocate
**Deliverables:**
- `projects/PROJ-031-cowork-skeleton/requirements/phase1-requirements.md` (iteration 2)
- `projects/PROJ-031-cowork-skeleton/decisions/ADR-001-skeleton-derived-branch-strategy.md` (iteration 2)
- `projects/PROJ-031-cowork-skeleton/decisions/ADR-002-ci-token-push-strategy.md` (iteration 2)
**Criticality:** C4
**Date:** 2026-06-26
**Reviewer:** jerry:adv-executor (Group C — Challenge; blind, independent)
**H-16 Compliance:** S-003 Steelman applied in QG-1 iteration-1 tournament. Steelmanned alternatives are embedded in ADR-001 §Options Considered (Option B orphan, Option C filter-repo) and ADR-002 §Options Considered (Option B PAT, Option C GitHub App token). Current deliverables incorporate strengthened arguments from that prior steelmanning. H-16 constraint satisfied by QG-1 sequencing.

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Overall assessment and verdict |
| [Findings Table](#findings-table) | All seven findings with severity and dimension mapping |
| [Detailed Findings](#detailed-findings) | Evidence and counter-arguments for Critical and Major findings |
| [Response Requirements](#response-requirements) | P0/P1/P2 prioritized action items |
| [Scoring Impact](#scoring-impact) | Per-dimension impact assessment |
| [Execution Statistics](#execution-statistics) | Protocol completion record |

---

## Summary

Seven counter-arguments identified across the three deliverables: 0 Critical, 4 Major, 3 Minor. The core design — derived branch via tag checkout + `git rm` + deterministic commit + GITHUB_TOKEN force-push — is architecturally sound and the iteration-2 revisions have substantially hardened the requirement set. However, four significant gaps remain that the prior steelmanning did not fully neutralize.

The most important: the pre-publication integrity gate (ADR-001/ADR-002's primary compensating control for the unprotected branch) is logically inconsistent as described — a git branch becomes installable the moment it is pushed, so "asserting the SHA before the branch is advertised as installable" either runs before the push (checking stale state) or after (too late for malicious direct-push content already live to CoWork users). Additionally, R-001's three-dimensional verification gate tests synthetic observables (file count, pack size, estimated clone time) but never requires an actual CoWork installation attempt; the Phase-2 gate could pass all three dimensions while CoWork still rejects the plugin. Two further Major findings target gaps in H-04 verification and the executable-content risk profile of the unprotected branch.

Verdict: **REVISE** — the four Major findings require substantive response before proceeding to S-014 scoring. None individually invalidates the core approach, but collectively they leave the C4 quality gate's compensating-control chain with logical gaps.

---

## Findings Table

| ID | Finding | Severity | Evidence | Affected Dimension |
|----|---------|----------|----------|--------------------|
| DA-001-iter2 | R-001 three-dimensional gate tests synthetic observables without requiring an actual CoWork installation attempt | Major | REQ-034 AC specifies only CLI commands (`git ls-files \| wc -l`, `git count-objects -vH`, estimated clone time); no integration test against CoWork runtime | Methodological Rigor |
| DA-002-iter2 | Pre-publication integrity gate is logically inconsistent — a branch is immediately installable upon push, so the gate cannot execute "before" the content is accessible | Major | ADR-001 §Tamper-Evidence; ADR-002 §Branch-Protection Posture: "before `cowork-skeleton` is advertised/consumed as installable, assert `git rev-parse cowork-skeleton == <expected SHA>`" | Internal Consistency |
| DA-003-iter2 | Detection-not-prevention posture for a branch containing executable hooks and CLI source significantly underweights attack window risk versus the `gh-pages` documentation analogy | Major | ADR-002 §Branch-Protection Posture; Risk R-007b (L=3, C=4, score=12, YELLOW); mitigation is REQ-021 designation + REQ-022 CI-only gate + REQ-028 documentation warning | Evidence Quality |
| DA-004-iter2 | REQ-004 acceptance criterion uses `uv run jerry projects list` but does not verify H-04 in CoWork's actual hook execution context where `uv` availability is not guaranteed | Major | REQ-004 AC: "`uv run jerry projects list` exits 0 and prints 'No projects found'"; STK-003 states "must function from the first session" | Completeness |
| DA-005-iter2 | Deterministic-commit idempotency proof treats the CI runner environment as a constant; it is not tested across runner image upgrades | Minor | ADR-001 §Regeneration Commit Determinism: "the preimage... is a pure function of T"; REQ-003 AC tests only "separate `workflow_dispatch` runs at different wall-clock times" not across runner image versions | Methodological Rigor |
| DA-006-iter2 | GITHUB_TOKEN loop-safety guarantee #3 is treated as a permanent platform invariant rather than a documented GitHub behavior that could change in a breaking update | Minor | ADR-002 §Loop-Safety Argument: "GITHUB_TOKEN pushes cannot re-trigger any workflow"; this is GitHub's current design, not a contractual guarantee | Internal Consistency |
| DA-007-iter2 | `v*` tag trigger fires on any `v`-prefixed tag before the allow-list sanitization validation runs, enabling resource exhaustion through repeated malformed-tag pushes by any repo collaborator | Minor | REQ-011: "trigger on `push: tags: ['v*']`"; ADR-001 §Tag-name sanitization: validation runs within the workflow step, after the trigger fires | Actionability |

---

## Detailed Findings

### DA-001-iter2: R-001 Three-Dimensional Gate Does Not Include a CoWork Integration Test [MAJOR]

**Claim Challenged:** REQ-034 states: "Before Phase 2 begins, a `verification/R001-clean-clone-count.md` artifact SHALL be created and committed to the project directory, recording a three-dimensional R-001 verification: (a) tracked file count on a clean clone of `main`... (b) total compressed pack size... (c) estimated clone time... All three dimensions must be within acceptable bounds before any Phase 5 implementation script may execute."

**Counter-Argument:** The three dimensions test observable proxies for the hypothesis "CoWork will accept the skeleton branch," but none of them constitutes an actual CoWork installation attempt. The R-001 statement itself acknowledges that "Anthropic's public plugin docs do not document any ~5,000-file limit — that limit is a CoWork/Claude-Desktop runtime constraint per the project's settled facts." If the actual enforcement mechanism is file-count-based, dimension (a) is the relevant test. If it is size-based, dimension (b) is relevant. If it is time-based, dimension (c) is relevant. But CoWork could also enforce the limit by scanning the post-checkout working directory for all filesystem entries (including CoWork-injected cache files), by counting git objects, or by an internal timeout unrelated to network clone time. All three proxy measurements can PASS while CoWork still rejects the install.

**Evidence:** REQ-034 acceptance criterion (WS-5): "(a) `git ls-files | wc -l` output on a clean clone of `main`; (b) `git count-objects -vH` output showing `size-pack:` in MB; (c) recorded clone time in seconds." None of the three criteria test "run `claude plugin marketplace add geekatron/jerry@cowork-skeleton` and observe success." The gap between measuring proxies and testing the actual integration is not acknowledged in REQ-034 or in the R-001 §Verification Approach.

**Impact:** If all three proxy dimensions pass but CoWork still fails to install the skeleton (different enforcement mechanism), the project discovers the failure at Phase 5 after C4-approved design artifacts have been committed. The Phase-2 gate that was intended to block Phase 5 will have been judged PASS on incorrect evidence.

**Dimension:** Methodological Rigor — the verification method (proxy measurement) is not rigorous enough to confirm the hypothesis it is testing.

**Response Required:** Add a fourth verification dimension to REQ-034: an actual CoWork installation attempt of a test skeleton on a machine with CoWork installed. This need not be part of the machine-checkable artifact at Phase 2 if CoWork is not available; it may be documented as a Phase-3 or pre-Phase-5 requirement. But the three-dimensional gate should explicitly acknowledge that it does not substitute for an actual integration test, and the plan should identify when that integration test will be executed.

**Acceptance Criteria:** REQ-034 is revised to either (a) include a CoWork installation test as a mandatory fourth dimension, or (b) explicitly acknowledge the proxy nature of the three dimensions and add a separate requirement (REQ-035 or similar) for a CoWork installation integration test at a specified phase before Phase 5.

---

### DA-002-iter2: Pre-Publication Integrity Gate Cannot Execute Before Malicious Content Reaches CoWork Users [MAJOR]

**Claim Challenged:** ADR-001 §Tamper-Evidence: "Publish the expected SHA for each release (e.g., in the GitHub Release notes, alongside the `Source-Commit` trailer) and add a **pre-publication integrity gate** that asserts `git rev-parse cowork-skeleton == <expected SHA>` before the branch is advertised as installable."

ADR-002 §Branch-Protection Posture: "Before `cowork-skeleton` is advertised/consumed as installable, assert `git rev-parse cowork-skeleton == <expected deterministic SHA>` for the release tag."

**Counter-Argument:** A git branch becomes installable the instant it exists with a push ref. CoWork users can run `claude plugin marketplace add geekatron/jerry@cowork-skeleton` at any time — before, during, or after any integrity check. The phrase "before the branch is advertised as installable" does not map to any implementable gate because no mechanism can delay a git ref's availability to clients.

For CI-originated pushes, the integrity gate CAN run within the CI job itself: generate the commit locally, compute its SHA, assert it matches the expected deterministic SHA, then push only if the assertion passes. This would be a pre-push integrity gate (not a post-push check against `git rev-parse cowork-skeleton`). This variant is useful and should be the specified implementation.

For the direct-push threat (RT-01 / R-007b): a repository collaborator can push malicious content to `cowork-skeleton` without CI involvement. The integrity gate does not run for direct pushes. The malicious content is immediately installable by CoWork users. The "detection" only fires at the next CI run (when the CI job would force-push the correct SHA, overwriting the malicious content). The detection window is hours to days.

**Evidence:** ADR-002 §Branch-Protection Posture states: "a repository collaborator could in principle push a malicious commit directly to `cowork-skeleton` without CI involvement, injecting unauthorized or erroneous content that persists until the next CI regeneration." This directly acknowledges the window but the mitigation table lists: "pre-publication integrity gate asserts the live tip SHA equals ADR-001's recomputable deterministic SHA; a mismatch blocks publication." This statement is circular: the gate blocks CI publication but does not block a direct push, which bypasses the gate.

**Impact:** The integrity gate, as the primary compensating control for the unprotected branch, does not provide the protection claimed for the direct-push attack surface. CoWork users can install malicious content during the window between a direct push and the next CI regeneration.

**Dimension:** Internal Consistency — the ADR's compensating-control chain contains a logical gap between the claimed protection property and what the gate can actually enforce.

**Response Required:** Clarify the two distinct scenarios and revise the language accordingly:

1. **CI-path integrity (achievable):** Within `cowork-skeleton.yml`, before the force-push step, assert that the locally-generated commit SHA matches the independently-computed expected SHA for the tag. This prevents a corrupted CI run from publishing an incorrect commit. Specify this as a pre-push step in the workflow.

2. **Direct-push attack (detection-only, with acknowledged window):** Explicitly acknowledge that the integrity gate does not prevent a direct push from being immediately installable. Provide a documented detection SLA (e.g., "detected within 24 hours via NFR-006 staleness check") and clarify whether this detection latency is acceptable for a C4 public plugin.

**Acceptance Criteria:** ADR-001 §Tamper-Evidence and ADR-002 §Branch-Protection Posture are revised to distinguish CI-path integrity (preventable) from direct-push attack (detection-only with explicit SLA). The pre-push CI assertion is specified as a concrete workflow step, not a post-push check.

---

### DA-003-iter2: Detection-Not-Prevention for Executable Content Underweights the Direct-Push Attack Window [MAJOR]

**Claim Challenged:** ADR-002 §Decision: "Keep `cowork-skeleton` UNPROTECTED (gh-pages parity), because: Nothing to guard. The branch is a disposable, CI-regenerated derivative..." and §Branch-Protection Posture: "The integrity risk is handled by detection, not prevention."

**Counter-Argument:** The `gh-pages` analogy does not hold for `cowork-skeleton`. The `gh-pages` branch contains static HTML and Markdown documentation files. A malicious commit to `gh-pages` would serve modified documentation to website visitors who can observe the modification immediately (it is human-readable HTML). `cowork-skeleton`, by contrast, contains:
- `hooks/session-start.py` and other hook files: executable Python code that runs in every Claude Code session
- `src/`: the Jerry CLI with hexagonal Python architecture
- `.claude/settings.json`: configuration affecting Claude Code's system behavior
- `.context/rules/`: behavioral rule files that modify how Claude Code operates

A malicious commit to `cowork-skeleton` does not produce visible HTML — it executes silently in CoWork sessions. A collaborator who inserts malicious code into `hooks/session-start.py` would have that code execute in every CoWork user's session without their knowledge. This is a fundamentally different risk profile from `gh-pages`.

Risk R-007b is scored L=3 (Possible), C=4 (Major), score=12, YELLOW. For a branch containing executable session hooks in a public Claude Code plugin, L=3 (Possible that a collaborator pushes malicious code) seems understated. C=4 seems understated: malicious hook execution in a user's Claude Code session could read files, exfiltrate environment variables, or make unauthorized API calls — a C=5 (Critical) consequence.

**Evidence:** ADR-002 §Consequences, Negative: "Cannot force-push a *protected* `cowork-skeleton`" is listed as the primary negative consequence of the unprotected posture. The executable-content risk is not identified as a distinguishing factor from `gh-pages`. Risk R-007b in phase1-requirements.md §Risk Implications: "mitigation: REQ-021 designates CI-owned unprotected posture with org-ruleset pre-check; REQ-022 pre-push diff gate prevents CI from publishing divergent content; REQ-028 warns users branch is CI-owned." REQ-022's pre-push diff gate and REQ-021's pre-check run only in CI, providing no protection against a direct push by a collaborator.

**Impact:** The documented mitigations (REQ-021, REQ-022, REQ-028) do not protect against direct-push injection of malicious executable content. For a C4 deliverable authorizing a public plugin with executable hooks, accepting a YELLOW direct-push risk with documentation-only mitigation requires explicit justification beyond "gh-pages parity."

**Dimension:** Evidence Quality — the `gh-pages` analogy is presented as an equivalence but the risk profiles of static documentation versus executable hooks are materially different.

**Response Required:** Either (a) demonstrate why the `cowork-skeleton` executable-content risk profile is equivalent to `gh-pages` (documentation only), or (b) add a ruleset bypass actor for `github-actions[bot]` that restricts direct-push capability to CI (Option A from the upgrade table in ADR-002), or (c) explicitly re-evaluate R-007b at C=5 consequence and document the decision to accept a 15 (RED) risk with documented justification at C4.

**Acceptance Criteria:** ADR-002 either (a) justifies the `gh-pages` analogy explicitly addressing the executable-content difference, (b) documents a concrete architectural change that prevents direct push (ruleset bypass actor), or (c) re-scores R-007b to C=5 and documents an explicit risk-acceptance decision with user authorization at C4.

---

### DA-004-iter2: REQ-004 Acceptance Criterion Does Not Verify H-04 in CoWork's Hook Execution Context [MAJOR]

**Claim Challenged:** REQ-004: "The `cowork-skeleton` branch SHALL contain a tracked `projects/README.md` sentinel file inside a `projects/` directory." Acceptance criterion: "On a clean clone of `cowork-skeleton`: `git ls-files projects/README.md` returns non-empty; `uv run jerry projects list` exits 0 and prints 'No projects found.'" STK-003: "A fresh install of the plugin must be immediately usable: H-04 bootstrap (active-project requirement) and SessionStart hook must function from the first session."

**Counter-Argument:** The acceptance criterion for REQ-004 tests `uv run jerry projects list` — explicitly using `uv` as the runtime. In a CoWork plugin session, the workflow is different:
1. CoWork installs the plugin by cloning `cowork-skeleton` to `~/.claude/plugins/cache/geekatron-jerry/`
2. CoWork registers and runs hook files specified in `.claude/hooks.json` (or equivalent)
3. The hook file `hooks/session-start.py` executes via CoWork's process execution mechanism — likely `python3 hooks/session-start.py` or equivalent, NOT `uv run`
4. If `session-start.py` calls `uv run jerry session status` or similar internally, it requires `uv` to be on PATH in the CoWork environment

Users who install Jerry via CoWork are general Claude Code users, not developers with `uv` configured. CoWork's documentation does not specify that `uv` must be installed. If `uv` is not available in the CoWork user's environment, any hook or CLI invocation that uses `uv run` will fail with a `command not found` error.

The research §Q4 (code-grounded) confirms that `FilesystemProjectAdapter.scan_projects` raises `RepositoryError` when `projects/` is absent — this verifies the sentinel's structural necessity. But it does not verify that the H-04 flow executes correctly in a CoWork runtime context where `uv` may be absent.

**Evidence:** REQ-004 AC: "`uv run jerry projects list` exits 0." This acceptance criterion explicitly requires `uv`. REQ-024a: "Tutorial SHALL include a dedicated step covering the H-04 first-run experience" — but REQ-024a only requires documentation, not verification that the actual CoWork hook execution works. The research citation is "Research Q4, code-grounded in `FilesystemProjectAdapter.scan_projects`" — this verifies Python logic, not CoWork integration.

**Impact:** If `uv` is required but not available in CoWork users' environments, STK-003 ("must function from the first session") fails for the majority of non-developer CoWork users, making the plugin immediately unusable after installation.

**Dimension:** Completeness — REQ-004's acceptance criterion verifies H-04 in a developer environment (where `uv` is available) but not in the CoWork plugin execution environment.

**Response Required:** Add a requirement or acceptance criterion that explicitly verifies how Jerry hook invocations work within CoWork's process execution model. Specifically: (a) document whether `hooks/session-start.py` uses `uv run` or can run with the system Python; (b) if `uv run` is required, add a requirement that the plugin installation documentation or setup script installs `uv` as a prerequisite; (c) if the hook can run with system Python, revise the REQ-004 AC to test without `uv` (e.g., `python hooks/session-start.py` or the equivalent CoWork invocation).

**Acceptance Criteria:** REQ-004 (or a new REQ-004b) includes an acceptance criterion that verifies H-04 behavior using the same invocation mechanism that CoWork uses to run the hook, documented in the STK-003 context. Alternatively, STK-003 explicitly declares `uv` as a prerequisite dependency with a REQ requiring the Tutorial to instruct users to install it.

---

## Response Requirements

### P0 — Critical (MUST resolve before acceptance)

None. No Critical findings.

### P1 — Major (SHOULD resolve; require justification if not addressed)

| ID | Action | Acceptance Criteria |
|----|--------|-------------------|
| DA-001-iter2 | Add to REQ-034 (or as REQ-035) a requirement for an actual CoWork installation integration test, or explicitly acknowledge that the three-dimensional gate is proxy-based and specify when the integration test will be executed | REQ-034 or a successor requirement names a CoWork installation attempt as a verification step and identifies the phase at which it will occur |
| DA-002-iter2 | Revise ADR-001 §Tamper-Evidence and ADR-002 §Branch-Protection Posture to distinguish CI-path integrity (pre-push assertion within workflow) from direct-push attack (detection-only); specify the pre-push assertion as a concrete workflow step | Both ADR sections use precise language distinguishing the two scenarios; the CI-path gate is described as a pre-push step, not a post-push check against the live ref |
| DA-003-iter2 | Address the `gh-pages` analogy gap for executable content: either justify the equivalence, add a ruleset bypass actor for CI, or re-evaluate R-007b consequence to C=5 with documented risk acceptance | One of the three alternatives is documented with sufficient rationale for a C4 reviewer; if risk acceptance, the user's explicit acknowledgment is recorded |
| DA-004-iter2 | Verify or specify the CoWork hook execution context and `uv` dependency; revise REQ-004 AC to test H-04 via the CoWork invocation mechanism | REQ-004 AC tests H-04 using the invocation mechanism CoWork uses (documented in research or a new STK-003 verification step); `uv` dependency is explicit if required |

### P2 — Minor (MAY resolve; acknowledgment sufficient)

| ID | Action |
|----|--------|
| DA-005-iter2 | Acknowledge in ADR-001 §Regeneration Commit Determinism that the idempotency proof assumes a stable CI runner environment; note that runner image changes should trigger a re-run of the idempotency acceptance test |
| DA-006-iter2 | Acknowledge in ADR-002 §Loop-Safety Argument that guarantee #3 is based on GitHub's documented behavior rather than a contractual invariant; note that a GitHub platform change would require re-evaluation |
| DA-007-iter2 | Document in the workflow design (TASK-001) that `v*`-prefixed tags failing the allow-list validation consume CI minutes; consider adding a concurrency-group note or a workflow timeout |

---

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Negative | DA-004: REQ-004's acceptance criterion is incomplete — it verifies H-04 in a developer context but not in CoWork's hook execution context; STK-003 traces to this requirement and the gap leaves an unverified use case |
| Internal Consistency | 0.20 | Negative | DA-002: The pre-publication integrity gate is described as asserting the SHA "before the branch is advertised as installable," but a git branch is installable immediately upon push — the gate cannot execute before the content is accessible to CoWork users; DA-006: loop-safety guarantee #3 is positioned as a design invariant but is an observed platform behavior |
| Methodological Rigor | 0.20 | Negative | DA-001: The R-001 three-dimensional verification gate is well-designed but incomplete — proxy measurements (file count, pack size, clone time) do not substitute for an actual CoWork installation test; the gate could pass while CoWork rejects the plugin on an unmeasured dimension |
| Evidence Quality | 0.15 | Negative | DA-003: The `gh-pages` analogy is cited as evidence that unprotected posture is acceptable for `cowork-skeleton`, but the analogy is not supported — `gh-pages` contains static HTML; `cowork-skeleton` contains executable session hooks and CLI code with a materially different risk profile |
| Actionability | 0.15 | Neutral | P0/P1 findings all have specific response requirements and acceptance criteria; the four Major findings are addressable without redesign; the design remains sound |
| Traceability | 0.10 | Neutral | All findings trace to specific deliverable claims with direct quotation; dimension mapping is complete; H-16 compliance is documented |

**Overall Assessment:** The four Major findings collectively reduce the methodological rigor, internal consistency, completeness, and evidence quality dimensions. None individually invalidates the core design (derived branch + deterministic commit + GITHUB_TOKEN + unprotected posture), but the pre-publication integrity gate gap (DA-002) and the executable-content analogy gap (DA-003) together leave the compensating-control chain for the unprotected branch with logical holes that a C4 review should require resolved.

---

## Execution Statistics

- **Total Findings:** 7
- **Critical:** 0
- **Major:** 4
- **Minor:** 3
- **Protocol Steps Completed:** 5 of 5
- **Deliverables Reviewed:** 3 (phase1-requirements.md, ADR-001, ADR-002)
- **Strategy:** S-002 Devil's Advocate
- **Template:** `.context/templates/adversarial/s-002-devils-advocate.md` v1.0.0
- **Finding Prefix Used:** DA-NNN-iter2
- **H-16 Compliance:** Verified (S-003 Steelman embedded in ADR Options Considered sections; deliverables are iteration-2 revisions incorporating prior steelmanning)

---

*Generated by: jerry:adv-executor*
*Strategy: S-002 Devil's Advocate*
*Project: PROJ-031-cowork-skeleton*
*Workflow: cowork-skeleton-20260626-001 / QG-1 / Iteration 2 / Group C*
*Date: 2026-06-26*
