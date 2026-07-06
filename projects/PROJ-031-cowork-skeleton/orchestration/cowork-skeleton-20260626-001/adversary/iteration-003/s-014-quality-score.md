# Quality Score Report: PROJ-031 CoWork Skeleton — Phase 1 Deliverables (Iteration 3)

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0 Executive Summary](#l0-executive-summary) | Score, verdict, top action item |
| [Scoring Context](#scoring-context) | Deliverables, criticality, strategy |
| [Score Summary](#score-summary) | Composite and threshold |
| [Dimension Scores](#dimension-scores) | Weighted table with evidence |
| [Iteration Trajectory](#iteration-trajectory) | IT1→IT2→IT3 per-dimension trend |
| [Detailed Dimension Analysis](#detailed-dimension-analysis) | Evidence, gaps, improvement path per dimension |
| [Issue Classification](#issue-classification) | (A) Phase-1-fixable vs (B) Phase-2-deferred |
| [Projected Post-(A) Score](#projected-post-a-score) | Composite after Phase-1 fixes |
| [Improvement Recommendations](#improvement-recommendations) | Priority-ordered action list |
| [Leniency Bias Check](#leniency-bias-check) | Anti-leniency protocol |

---

## L0 Executive Summary

**Score:** 0.824/1.00 | **Verdict:** REVISE | **Weakest Dimension:** Completeness (0.80) tied with Evidence Quality (0.80)

**One-line assessment:** Iteration 3 substantially closed the ADR→requirements gap (adding REQ-035/036/037/034d/NFR-006 dual-check), but the new publish-then-assert architecture introduced a convergent critical flaw found independently by 5 of 8 strategies: GitHub Release notes share the same `contents: write` permission as the branch they are supposed to independently verify, collapsing the "protected surface" integrity anchor; 23 additional Phase-1-addressable issues span permissions omissions, wrong reference resolution in acceptance criteria, and a circular Phase-5 gate dependency — fixing all Phase-1 issues projects to 0.872, with the gap to 0.92 dominated by Phase-2 STRIDE architectural work.

---

## Scoring Context

| Field | Value |
|-------|-------|
| **Deliverable: Requirements** | `projects/PROJ-031-cowork-skeleton/requirements/phase1-requirements.md` |
| **Deliverable: ADR-001** | `projects/PROJ-031-cowork-skeleton/decisions/ADR-001-skeleton-derived-branch-strategy.md` |
| **Deliverable: ADR-002** | `projects/PROJ-031-cowork-skeleton/decisions/ADR-002-ci-token-push-strategy.md` |
| **Deliverable Type** | Requirements + ADR (Design) |
| **Criticality Level** | C4 |
| **Scoring Strategy** | S-014 (LLM-as-Judge) |
| **SSOT Reference** | `.context/rules/quality-enforcement.md` |
| **Quality Gate** | ≥ 0.92 (H-13) |
| **Project Target** | ≥ 0.95 |
| **Prior Scores** | Iteration 1: 0.781 | Iteration 2: 0.801 |
| **H-14 Status** | SATISFIED — iteration 3 meets minimum 3-cycle requirement |
| **Scored** | 2026-06-26 |

**Strategy findings incorporated:** Yes — all 8 iteration-3 adversary strategies read:
- S-001 Red Team: 2 Critical, 3 Major, 3 Minor
- S-002 Devil's Advocate: 1 Critical, 4 Major, 2 Minor
- S-003 Steelman: 0 Critical, 3 Major, 5 Minor
- S-004 Pre-Mortem: 2 Critical, 5 Major, 1 Minor
- S-007 Constitutional AI: 0 Critical, 1 Major, 3 Minor
- S-011 Chain-of-Verification: 0 Critical, 4 Major, 2 Minor
- S-012 FMEA: 1 Critical, 10 Major, 5 Minor
- S-013 Inversion: 0 Critical, 5 Major, 2 Minor

**Total across all strategies:** 6 Critical, 35 Major, 23 Minor

---

## Score Summary

| Metric | Value |
|--------|-------|
| **Weighted Composite** | **0.824** |
| **Threshold** | 0.92 (H-13) |
| **Project Target** | 0.95 |
| **Gap to Gate** | −0.096 |
| **Gap to Project Target** | −0.126 |
| **Verdict** | **REVISE** |
| **Band** | 0.70–0.84 (significant gaps, focused revision needed) |
| **Critical Findings Count** | 6 (cluster into 3 root causes — see Issue Classification) |
| **Strategy Findings Incorporated** | Yes — 8 strategies |

---

## Dimension Scores

| Dimension | Weight | Score | Weighted | Evidence Summary |
|-----------|--------|-------|----------|-----------------|
| Completeness | 0.20 | 0.80 | 0.160 | IT3 REQ additions large; undercut by CV-002 missing `contents: read` (monitoring non-functional as specified), FM-06 (meta-monitoring absent), FM-11 (no post-publish verification), PM-007 (build-status precondition has no CC/REQ) |
| Internal Consistency | 0.20 | 0.82 | 0.164 | CC-to-REQ table added in ADR-002 closes major IT2 gap; new inconsistencies: CV-003 (dimension-d circular dependency), FM-09 (REQ-022 AC checks wrong git ref), IN-002 (dual-SSOT for retention surface), CC-002 (duplicate allocation matrix rows) |
| Methodological Rigor | 0.20 | 0.84 | 0.168 | Four-dimensional gate, loop-safety triple-guarantee, and dual-check NFR-006 are genuinely rigorous; held back by FM-04 (threshold calibration at 10 Mbps not 5 Mbps), FM-02 (24h SLA too long for executable-hook blast radius), and FM-09 (diff gate compares wrong refs at runtime) |
| Evidence Quality | 0.15 | 0.80 | 0.120 | Empirical ruleset inventory, GitHub API command outputs, CC-to-REQ table all strong; critically undercut by convergent finding across 5 strategies: "protected surface" claim for Release notes is unsupported — same `contents: write` permission enables branch push AND release edit; growth-rate (~2 MB/release) asserted without empirical derivation |
| Actionability | 0.15 | 0.83 | 0.125 | REQ-035/036/037 have specific, testable ACs; CC-to-REQ table makes Phase-6 implementation path clear; degraded by CC-001/CV-001 (CC-6 mapped to wrong REQ — implementers routed to REQ-037 for a pre-deploy check that lives in REQ-021), FM-09 (wrong git ref in REQ-022 AC means the gate silently tests nothing), IN-003 (Windows workaround documented but inapplicable in CoWork-managed clone) |
| Traceability | 0.10 | 0.87 | 0.087 | Biggest IT3 gain: ADR-002 CC-1 through CC-8 all gained backing SHALL requirements; remaining gaps: CC-001/CV-001 (CC-6 traces to wrong REQ), CV-006 (REQ-014 AC cites ADR-001 for an argument that appears only in ADR-002), CC-004 (Phase-2 deferred items lack worktracker entity IDs) |
| **TOTAL** | **1.00** | | **0.824** | |

---

## Iteration Trajectory

> IT1 and IT2 per-dimension breakdowns are estimated from composite data (IT1: 0.781, IT2: 0.801) and the structural changes documented in the IT3 remediation log (IT3-001 through IT3-007). Per-dimension scores for prior iterations are estimates; they are not loaded from prior score reports.

| Dimension | IT1 (est.) | IT2 (est.) | IT3 (scored) | Δ IT2→IT3 | Trend |
|-----------|-----------|-----------|-------------|-----------|-------|
| Completeness (0.20) | 0.72 | 0.74 | 0.80 | +0.06 | ↑ |
| Internal Consistency (0.20) | 0.78 | 0.80 | 0.82 | +0.02 | ↑ |
| Methodological Rigor (0.20) | 0.82 | 0.83 | 0.84 | +0.01 | ↑ |
| Evidence Quality (0.15) | 0.80 | 0.81 | 0.80 | −0.01 | ↓ |
| Actionability (0.15) | 0.80 | 0.81 | 0.83 | +0.02 | ↑ |
| Traceability (0.10) | 0.75 | 0.79 | 0.87 | +0.08 | ↑↑ |
| **Composite** | **0.781** | **0.801** | **0.824** | **+0.023** | ↑ |

**Trajectory notes:**

- **Completeness +0.06 (biggest positive):** REQ-035, REQ-036, REQ-037, REQ-034d, and NFR-006 dual-check directly close the "architecture specified in ADR but not in requirements" gap from IT1/IT2. CV-002 (missing `contents: read`) is a new gap introduced by the new architecture.
- **Evidence Quality −0.01 (only regression):** The publish-then-assert architecture introduced in IT3 brought the "protected surface" framing, which 5 strategies independently found is unsupported by GitHub's permission model. IT3 created more architecture to critique than IT2 had, and that architecture contained a trust-model gap. Net is a slight regression on this dimension.
- **Traceability +0.08 (largest dimension gain):** The CC-to-REQ table in ADR-002 resolves the primary IT2 gap (controls without backing requirements). This dimension had the highest room for improvement and took the most benefit from IT3 remediation.
- **Overall composite velocity:** +0.040 from IT1→IT2 (smaller step), +0.023 from IT2→IT3. The slowdown reflects both that easy gains were already captured and that the new architecture introduced new critique surface.

---

## Detailed Dimension Analysis

### Completeness (0.80/1.00)

**Rubric level:** 0.7–0.89 (most requirements addressed, minor gaps). At the lower end of this band — "minor" overstates the CV-002 impact.

**Evidence (what is complete):**

WS-1 through WS-5 are fully populated with requirements, acceptance criteria, V-methods, and stakeholder traces. The IT3 additions are substantive: REQ-035 (async monitor architecture with 5-point AC), REQ-036 (event-discriminated tag resolution with allow-list validation), REQ-037 (push-failure `if:failure()` step), REQ-034d (per-release clone-weight emit with hard-fail), NFR-006 revised to dual-check (staleness via Source-Commit trailer, tamper-detection via non-forgeable tip SHA). The Phase-2 Deferred Items table explicitly names auto-revert, tag-on-main provenance, detection→prevention escalation, and R-007b re-rating — all four are correctly scoped as Phase-2.

**Gaps:**

1. **CV-002 (Major):** REQ-035 and NFR-006 mandate `issues: write` only. The Releases API (`gh release view` / `gh release list`) requires `contents: read`. A strictly-compliant implementation declaring only `issues: write` sets all other permissions to `none` by GitHub's explicit rule, causing the SHA-lookup step to fail with HTTP 403. The tamper-detection logic is unreachable as currently specified. This is functional rather than stylistic.
2. **FM-06 (Major):** No meta-monitoring requirement exists for the NFR-006 monitor itself. GitHub Actions documents that scheduled workflows may be delayed or silently skipped under high load. A monitor that fails to run produces no alert, making the SLA effectively unbounded on monitor failure.
3. **FM-11 (Major):** REQ-035 specifies the publish step (`gh release edit … --notes-append`) but no post-publish verification step. If the API call fails silently, the reference anchor is absent; the next monitor run compares live SHA against a stale prior release SHA.
4. **PM-007 (Major, via S-004):** ADR-002 build-status precondition (require successful validation before SHA published) has no backing CC number and no SHALL requirement in the requirements document. The self-certifying checklist at ADR-002 line 437 states all CCs have backing requirements — this is incorrect.
5. **IN-004 (Major):** REQ-024 and REQ-027 document `uv` in Tutorial prerequisites and How-To failure modes, but no requirement mandates that `hooks/session-start.py` detect `uv` absence at execution time. Without a hook-level check, a CoWork user who installed the plugin without reading the Tutorial receives a cryptic OS error (`uv: command not found`) with no in-session guidance.
6. **IN-003 (Major):** REQ-027 documents a `git config core.symlinks true` workaround for Windows. In a CoWork-managed clone, the user cannot set this config before CoWork executes the clone; the workaround is inapplicable. REQ-009 AC explicitly limits the symlink test to "CI Linux environment." Windows CoWork installs silently produce broken sessions with no error.

**Improvement path:** Add `contents: read` to REQ-035/NFR-006 permissions block. Add meta-monitoring requirement to NFR-006 (monitor asserts its own last-success timestamp). Add post-publish verification AC to REQ-035. Add CC entry for build-status precondition. Add `uv`-detection AC to STORY-002 scope. Update REQ-027 to formally state Windows CoWork symlink install is unsupported pending Phase-5 generation-script fix.

---

### Internal Consistency (0.82/1.00)

**Rubric level:** 0.7–0.89 (minor inconsistencies). At the higher end — most claims are aligned; the inconsistencies found are concrete and fixable.

**Evidence (what is consistent):**

The ADR→requirements alignment is substantially improved in IT3. The CC-to-REQ table in ADR-002 (CC-1 through CC-8 with backing requirements) resolves the primary IT2 consistency gap. Loop-safety triple-guarantee is coherent across both ADRs. NFR-006 dual-check correctly scopes the two legs (Source-Commit trailer for staleness, tip SHA for tamper-detection). The Option A default / Option B flip procedure is coherent between REQ-034d and ADR-001.

**Gaps (inconsistencies found):**

1. **CV-003 (Major):** REQ-034 dimension (d) states "Phase 5 is blocked until [dimension d] is completed." Dimension (d) requires installing `geekatron/jerry@cowork-skeleton`, which is the branch created by Phase 5. The gate cannot be enforced without the output of the phase it claims to block. No resolution clause (e.g., locally generated dry-run branch) is documented.
2. **FM-09 (Major):** REQ-022 AC specifies `git diff v{N}..cowork-skeleton -- ':!projects/'`. In the generation workflow, `cowork-skeleton` resolves to the remote tracking ref (the previous release's skeleton), not to the locally generated `HEAD`. The gate compares source tag against old remote, not against freshly generated content — a tampered locally-generated tree passes the gate silently.
3. **IN-002 (Major):** ADR-001 §Canonical Plugin-Retention Surface declares itself the SSOT with REQ-005 "mirroring it verbatim." Both documents embed the list as independent text. This already drifted once in iteration 1. Two documents claiming to be SSOT for the same list is architecturally inconsistent.
4. **CC-002 (Minor):** The Allocation Matrix contains duplicate rows for REQ-034d (two entries with slightly different content) and REQ-035 (two entries), artifacts of the IT3 remediation editing pass.
5. **CV-005 (Minor):** Tag discovery glob `v[0-9]*.[0-9]*.[0-9]*` requires exactly 3 version components; allow-list `^v[0-9]+\.[0-9]+(\.[0-9]+)?$` permits 2. A two-component tag passes validation but is not returned by the discovery command.

**Improvement path:** Add resolution clause to REQ-034 dimension (d) specifying a locally-generated dry-run branch as the test object. Fix REQ-022 AC to use `git diff ${TAG}..HEAD`. Add CI lint requirement to ADR-002/REQ-005 asserting both lists are identical (or collapse to single data source). Merge duplicate Allocation Matrix rows. Align tag discovery glob with allow-list.

---

### Methodological Rigor (0.84/1.00)

**Rubric level:** 0.7–0.89 (sound methodology, minor gaps). At the high end of this band — the methodology is genuinely sophisticated.

**Evidence (what is rigorous):**

The three-guarantee loop-safety proof (trigger shape, listener shape, credential shape) is structured as a conjunction where all three must hold for loop-safety — a logically complete argument. The four-dimensional R-001 verification gate covers file count, pack size, clone time, and CoWork install — each dimension tests a distinct failure mode. The NFR-006 dual-check correctly distinguishes forgeable (Source-Commit trailer) from non-forgeable (tip SHA) comparators and assigns each to the right detection objective. The event-discriminated tag resolution (3-branch conditional with explicit WARNING comment against the naive one-liner) demonstrates awareness of the subtle platform behavior difference.

**Gaps:**

1. **FM-04 (Major):** The 250 MB hard-fail and 150 MB early-warning thresholds reference 10 Mbps (≈ 30th-percentile global broadband) as the calibration point. At 5 Mbps (≈ 20th-percentile, covering VPN and mobile users), 250 MB requires approximately 400 seconds — more than 3× the 120-second timeout. The threshold that actually triggers the 120-second timeout at 5 Mbps is approximately 75 MB. The methodology correctly identifies calibration as important but uses the wrong reference point.
2. **FM-02 (Major):** The 24-hour tamper-detection SLA is acknowledged in ADR-002 as set specifically because "the skeleton ships executable hooks to user workstations." The methodology correctly identifies the concern but then sets a SLA that allows 24 hours of tampered hook distribution. The event-driven leg is "best-effort" only. The methodological basis for accepting 24 hours given executable-hook blast radius is not documented.
3. **FM-09 (double-counted, already in Internal Consistency):** REQ-022 accepts a test that cannot actually detect the failure it is designed to catch — a methodological gap beyond just inconsistency.
4. **CC-003 (Minor):** REQ-004 AC embeds a cross-workstream functional flow test (H-04 `<project-required>` prompt) that depends on REQ-024a Tutorial content existing. This creates an implicit verification ordering dependency that makes REQ-004 unverifiable in isolation.

**Improvement path:** Recalibrate clone-weight thresholds to 5 Mbps reference bandwidth; document the reference bandwidth and calculation in REQ-034 and REQ-034d. Reduce scheduled tamper-detection cadence to ≤ hourly in NFR-006 and REQ-035; document formal risk-acceptance for the residual window. Remove cross-workstream AC from REQ-004.

---

### Evidence Quality (0.80/1.00)

**Rubric level:** 0.7–0.89 (most claims supported). At the lower end — the unsupported "protected surface" claim is systemic and identified by 5 strategies.

**Evidence (what is well-supported):**

The empirical ruleset inventory (`gh ruleset list` run 2026-06-26: only "Don't fuck with main" targeting `~DEFAULT_BRANCH`, cowork-skeleton unprotected) is concrete and dated. The GitHub Actions non-retrigger property is cited as "vendor-documented" (ADR-002 Loop-Safety Argument). The CC-to-REQ table provides explicit backing for each compensating control. The R-001 four-dimensional gate documents uncertainty explicitly (CoWork file-count limit stated as "per project settled facts, empirical confirmation still warranted").

**Gaps:**

1. **Convergent Critical (DA-001/RT-001/FM-01/CV-004/IN-001 — 5 strategies):** ADR-002 §Continuous Integrity Monitoring and ADR-001 §Tamper-Evidence characterize GitHub Release notes as "a durable, off-branch, **protected** surface (Releases are governed by `main`/release permissions, not by the unprotected branch)." This claim is not supported by GitHub's permission model. Repository collaborators with `write` access can execute both `git push` to unprotected branches AND `gh release edit` to update release notes under the same permission tier. The "protected surface" framing implies a separation of access that does not exist. An RT-01 actor who can push to `cowork-skeleton` can also update the Release notes SHA to match the tampered commit in two API calls. Five strategies identified this independently; it is the highest-confidence finding of the entire tournament.
2. **RT-002/DA-005 (Critical):** ADR-001 characterizes integrity monitoring as "the compensating detective control for a wrong-but-well-formed tag" pushed by an attacker. This is false for the CI-triggered attack path: an attacker pushes a well-formed `v9.9.9` tag at a malicious commit, CI processes the `push:tags` event, generates a tampered skeleton, and publishes its SHA to Release notes — all within CI. The GITHUB_TOKEN non-retrigger property means the event-driven monitor does NOT fire (CI push to `cowork-skeleton`). The scheduled monitor compares live tip SHA against the just-published SHA: MATCH. Zero detection for this vector. The claim in ADR-001 is directly incorrect.
3. **IN-006 (Minor):** The ~2 MB/release growth rate estimate (from which the "1–3 years to flip trigger" calculation derives) is asserted in ADR-001 without a data source or calculation. REQ-034 dimension (b) measures current pack size but does not derive a per-release rate.
4. **DA-004 (Minor):** The GITHUB_TOKEN non-retrigger property — on which loop-safety guarantee (3) depends — is cited as "vendor-documented" without a GitHub Docs URL or access date. Future GitHub policy changes would invalidate the guarantee silently.

**Improvement path:** In ADR-002 §Continuous Integrity Monitoring and ADR-001 §Tamper-Evidence: remove "protected surface" framing; replace with explicit scope statement: "This detection model covers out-of-band direct pushes by RT-01 actors; it does NOT detect CI-compromise attacks (where both branch and Release notes are updated by the same job) — that attack path is an accepted residual risk, with the Phase-2 STRIDE analysis determining whether prevention controls are warranted." Correct ADR-001 claim about monitoring effectiveness against well-formed rogue tags. Extend REQ-034 dimension (b) to derive per-release growth rate. Add GitHub Docs URL + access date to the non-retrigger documentation in ADR-002 §Loop-Safety Argument.

---

### Actionability (0.83/1.00)

**Rubric level:** 0.7–0.89 (actions present, some vague). At the higher end — most requirements have specific testable ACs; the gaps are in precision of specific ACs rather than absence of actions.

**Evidence (what is actionable):**

REQ-035 AC has 5 enumerated testable outcomes. REQ-036 AC covers push-trigger path, workflow_dispatch explicit path, blank-input fallback, allow-list rejection, and env-binding. REQ-037 AC specifies exact GITHUB_STEP_SUMMARY content. The ADR-002 CC-to-REQ table gives Phase-6 implementers an explicit requirements map. AG-01 through AG-10 approval gates are specific and named.

**Gaps:**

1. **CC-001/CV-001 (Major):** ADR-002 CC-6 backing requirement is listed as "REQ-037 (or sibling)." REQ-037 is the post-push `if:failure()` runtime detection step (CC-5, not CC-6). CC-6 is the pre-deploy ruleset-coverage check, which is backed by REQ-021. A Phase-6 implementer following CC-6 to REQ-037 will find post-push error handling language, not the pre-deploy `gh api orgs/geekatron/rulesets` check. The "(or sibling)" hedge signals awareness but leaves the correct reference unnamed. This directly degrades Phase-6 actionability.
2. **FM-09 (Major):** REQ-022 AC specifies `git diff v{N}..cowork-skeleton` as the pre-push gate. A Phase-6 implementer implementing this exactly will create a gate that silently validates against the old remote skeleton rather than the locally generated content. The correct command is `git diff ${TAG}..HEAD`. The AC as written creates a broken gate that would pass even with a corrupted local tree.
3. **IN-003 (Major):** REQ-027 documents a `git config core.symlinks true` Windows workaround. This workaround requires the user to configure git before CoWork's automated clone — which they cannot do. Documenting an inapplicable workaround is worse than documenting "unsupported" because it implies a resolution path that does not exist, and implementers may waste time attempting it.
4. **FM-13 (Major):** REQ-034d early-warning at 150 MB opens a GitHub issue but is non-blocking with no documented assignee or response SLA. There is no escalation between the non-blocking warning and the hard 250 MB failure — which at 5 Mbps reference bandwidth already causes user-facing install timeouts.

**Improvement path:** Fix CC-6 backing requirement in ADR-002 CC table from REQ-037 to REQ-021. Fix REQ-022 AC to use `git diff ${TAG}..HEAD`. Update REQ-027 to state Windows CoWork install is currently unsupported (not "workaround available"). Add assignee and 30-day response SLA to early-warning GitHub issue, or convert 200 MB to a blocking threshold.

---

### Traceability (0.87/1.00)

**Rubric level:** 0.7–0.89 (most items traceable). At the top of this band — the IT3 CC-to-REQ table is the primary traceability gain.

**Evidence (what is traceable):**

All STK-001 through STK-005 stakeholders have upward traces to requirements. REQ-001 through REQ-037 all have explicit V-Method assignments and acceptance criteria. The ADR-002 CC-1 through CC-8 table now maps each compensating control to a backing SHALL requirement (IT3-001 closure). ADR-001 and ADR-002 footers contain S-010 self-refine notes with IT3-001 through IT3-007 item-by-item remediation record. REQ-014 traces the loop-safety three-guarantee conjunction.

**Gaps:**

1. **CC-001/CV-001 (Major):** The CC-to-REQ trace for CC-6 points to REQ-037 — an incorrect trace. An incorrect trace is a traceability failure (P-040): a Phase-6 implementer following the trace from CC-6 arrives at the wrong requirement.
2. **CV-006 (Minor):** REQ-014 AC references "three independent guarantees documented in ADR-001/ADR-002." The three guarantees are documented only in ADR-002 §Loop-Safety Argument; ADR-001 does not enumerate them. The joint reference overstates ADR-001's traceability contribution and makes the AC non-navigable for a reviewer reading ADR-001 only.
3. **CC-004 (Minor):** Phase-2 Deferred Items table provides ADR section pointers as Phase-2 entry points but omits STORY/TASK worktracker entity IDs. P-040 requires downward traceability from requirements to tracking artifacts. This gap closes naturally when Phase-2 stories are created, but it is currently incomplete.
4. **IN-007/RT-002 (Minor):** The tag-on-main provenance assertion is noted in ADR-001 §Tag-name sanitization prose as a Phase-2 STRIDE item, but the ORCHESTRATION_PLAN.md Phase-2 scope section has not been confirmed to explicitly reference RT-003 / "tag-on-main provenance assertion" as a named Phase-2 deliverable.

**Improvement path:** Fix CC-6 trace in ADR-002 CC table to REQ-021. Revise REQ-014 AC to reference "ADR-002 §Loop-Safety Argument" only. Add Worktracker column to Phase-2 Deferred Items table once entities are created. Confirm ORCHESTRATION_PLAN Phase-2 scope explicitly names tag-on-main provenance assertion (RT-003).

---

## Issue Classification

### Classification Logic

- **(A) Phase-1-fixable:** Can be resolved by editing the three existing Phase-1 deliverables (requirements doc, ADR-001, ADR-002) or the ORCHESTRATION_PLAN. Does not require Phase-2 STRIDE analysis, new credentials, or architectural decisions outside current ADR scope.
- **(B) Phase-2/STRIDE-deferred:** Requires Phase-2 STRIDE threat modeling, a new credential decision (GitHub App), a new ADR, or implementation work that depends on Phase-5/6 artifacts.

### (A) Phase-1-Fixable Issues

These 23 items are addressable by revising the current Phase-1 documents:

| # | Finding IDs | Fix Description | Primary Dimension Impact |
|---|-------------|-----------------|-------------------------|
| A-01 | DA-001, RT-001, FM-01, CV-004, IN-001 | Remove "protected surface" / "governed by main/release permissions" framing from ADR-002 §CIM and ADR-001 §Tamper-Evidence; replace with explicit scope statement: detection covers out-of-band direct pushes; CI-compromise and coordinated branch+notes forgery are accepted residual risks pending Phase-2 STRIDE | Evidence Quality, Internal Consistency |
| A-02 | RT-002, DA-005 | Correct ADR-001 claim that integrity monitoring is "the compensating detective control for a wrong-but-well-formed tag" — state explicitly that CI-triggered generation from an attacker-created `v*` tag produces a MATCH result in the monitor (both SHA values written by same CI run); this attack vector is the Phase-2 tag-provenance scope | Evidence Quality, Internal Consistency |
| A-03 | CV-002 (S-011), FM-07 (S-012) | Add `contents: read` to REQ-035 and NFR-006 required permissions block; update REQ-035 AC(e) to verify both `contents: read` and `issues: write` are declared | Completeness |
| A-04 | FM-11 | Add post-publish verification step to REQ-035: after `gh release edit`, retrieve release notes via `gh release view --json body` and assert `cowork-skeleton-sha:` field is present and matches the pushed SHA; add to REQ-035 AC | Completeness |
| A-05 | FM-06, PM-006, RT-005 | Add meta-monitoring requirement to NFR-006: a separate daily job asserts the NFR-006 monitor produced a successful run within the prior 25 hours; failure opens a GitHub issue | Completeness, Methodological Rigor |
| A-06 | CC-001, CV-001 | Fix ADR-002 CC table, CC-6 row: change backing requirement from "REQ-037 (or sibling)" to "REQ-021 (pre-deploy org-ruleset check)"; add note distinguishing CC-5 (REQ-037, post-push runtime) from CC-6 (REQ-021, pre-deploy assertion) | Actionability, Traceability |
| A-07 | FM-09 | Fix REQ-022 AC: change `git diff v{N}..cowork-skeleton` to `git diff ${TAG}..HEAD -- ':!projects/'`; update Demonstration AC to confirm local-tree injection triggers exit non-zero | Internal Consistency, Actionability |
| A-08 | CV-003, FM-03, IN-005, PM-002 | Add to REQ-034 dimension (d): "Dimension (d) SHALL be performed using a manually-generated `cowork-skeleton` branch produced by running the Phase-5 generation script locally (dry-run) against a `v*` tag, prior to merging the CI workflow file to main"; add dimension-d PASS as an explicit named condition in the ORCHESTRATION_PLAN approval gate before Phase-5 authorization | Completeness, Traceability |
| A-09 | PM-007 | Add CC-N to ADR-002 CC table: "Build-status precondition — SHA publication occurs only after successful validation; implemented by [existing workflow step ordering — add SHALL in REQ-035 AC requiring publish step to be gated on prior steps exiting zero]" | Completeness, Traceability |
| A-10 | PM-001, FM-02 | Reduce scheduled tamper-detection cadence from ≤ daily to ≤ hourly in NFR-006 and REQ-035; document formal risk-acceptance statement for the residual ≤ 1-hour window given the executable-hook blast radius | Methodological Rigor |
| A-11 | FM-04 | Recalibrate clone-weight thresholds using 5 Mbps (≈ 20th-percentile) reference bandwidth; document reference bandwidth and calculation in REQ-034d and REQ-034; set early-warning at 50 MB and hard-fail at 75 MB (or document the deliberate choice to accept higher thresholds at stated bandwidth for current user base); update R-001 §Verification Approach to record dimension (c) at both 10 Mbps and 5 Mbps | Evidence Quality, Methodological Rigor |
| A-12 | IN-003 | Update REQ-027 to state Windows CoWork plugin install is currently unsupported (not "workaround available") due to CoWork-managed clone not accepting `git config core.symlinks` pre-configuration; escalate to Phase-5 generation script scope to copy symlink targets rather than preserve symlinks | Completeness, Actionability |
| A-13 | IN-004 | Add AC to STORY-002 (hooks/session-start.py): script MUST detect `uv` absence before `uv run` invocation and emit a user-visible message with install command and Tutorial link; update REQ-027 How-To AC to reference this in-hook detection | Completeness |
| A-14 | PM-003 | Add note to ADR-002 §Continuous Integrity Monitoring: "The event-driven leg does not fire on `delete`+`create` branch sequence (only `push` events); the scheduled backstop covers this gap within the cadence window" | Internal Consistency |
| A-15 | DA-004, FM-17 | Add GitHub Docs URL and access date to ADR-002 §Loop-Safety Argument for the GITHUB_TOKEN non-retrigger guarantee; document that future GitHub policy changes to this behavior would invalidate guarantee (3) and trigger AE-005 re-assessment | Evidence Quality |
| A-16 | IN-006 | Extend REQ-034 dimension (b) to derive per-release growth rate: calculate (current_size − oldest_tag_size) / release_count; record in `verification/R001-clean-clone-count.md` with "N releases to 75 MB trigger" calculation | Evidence Quality |
| A-17 | CC-002 | Merge duplicate Allocation Matrix rows for REQ-034d and REQ-035 (two rows each from IT3 editing pass); use the more complete version of each | Internal Consistency |
| A-18 | CC-003 | Remove cross-workstream H-04 functional flow AC from REQ-004 acceptance criteria; REQ-024a already owns and tests that scenario; document as integration test if needed | Methodological Rigor |
| A-19 | CV-006 | Fix REQ-014 AC: change "three independent guarantees documented in ADR-001/ADR-002" to "three independent guarantees documented in ADR-002 §Loop-Safety Argument" | Traceability |
| A-20 | CV-005 | Align blank-input tag discovery glob `v[0-9]*.[0-9]*.[0-9]*` with allow-list by adding `(\.[0-9]*)?` to permit 2-component tags, or document the intentional discrepancy as a project convention comment in ADR-001 pseudocode | Internal Consistency |
| A-21 | FM-13 | Add assignee and 30-day response SLA to the 150 MB early-warning GitHub issue; or convert 200 MB to a blocking threshold, leaving 150 MB as first non-blocking notice | Actionability |
| A-22 | SM-001 | Front-load decisive framing in ADR-001: move the "CoWork uses clean-clone working tree — Option C is eliminated outright" conclusion before the option comparison table, not buried mid-analysis | Actionability |
| A-23 | SM-002, SM-003 | Name GITHUB_TOKEN "double duty" (loop-safety + tamper-detection enabler) as explicit architectural economy in ADR-002 Decision rationale; reframe R-001 as a "falsification protocol" not a checklist (the four dimensions are chosen to cover distinct plausible failure modes, not just due diligence steps) | Actionability |

### (B) Phase-2/STRIDE-Deferred Items

These items are correctly scoped to Phase-2 and cannot be resolved in Phase-1 deliverables:

| # | Finding IDs | Deferral Rationale |
|---|-------------|--------------------|
| B-01 | DA-001/RT-001/FM-01 (architectural layer) | Establishing a genuinely independent reference surface (immutable, CI-write-only) requires either a GitHub App token for a protected branch or alternative artifact storage (SLSA provenance); both require Phase-2 STRIDE and a new credential ADR |
| B-02 | RT-002/DA-005 (architectural layer) | Tag-on-main provenance assertion (`git merge-base --is-ancestor <commit> main`) is explicitly Phase-2 STRIDE (STORY-004); requires validation that the check is not itself bypassable |
| B-03 | Auto-revert automation | Requires PAT or GitHub App with write-to-main scope — a new credential decision that inverts ADR-002's explicit PAT rejection; Phase-2 STRIDE must validate the revert trigger is not itself exploitable |
| B-04 | Detection→prevention escalation (branch protection rulesets) | Requires adopting ADR-002 Option C (GitHub App token); ADR-002 explicitly documents this as the upgrade path from the Phase-1 detection model |
| B-05 | R-007b STRIDE consequence re-rating (C=4→C=5) | Requires Phase-2 threat modeling data on executable-hook blast radius for user-workstation impact; current deferral is constitutionally sound per S-007 analysis |
| B-06 | Phase-2 Deferred Items worktracker IDs (CC-004) | Inherently Phase-2 tracking work — STORY/TASK IDs cannot be created until Phase-2 planning; the Deferred Items table should be updated when entities are created |
| B-07 | IN-007: ORCHESTRATION_PLAN Phase-2 scope confirmation for RT-003 tag-on-main | Requires reviewing and potentially editing ORCHESTRATION_PLAN.md (out of Phase-1 deliverable scope for this scoring pass) |

---

## Projected Post-(A) Score

After applying all 23 (A) Phase-1-fixable items:

| Dimension | IT3 Score | Post-(A) Estimate | Delta |
|-----------|-----------|-------------------|-------|
| Completeness | 0.80 | 0.86 | +0.06 |
| Internal Consistency | 0.82 | 0.87 | +0.05 |
| Methodological Rigor | 0.84 | 0.88 | +0.04 |
| Evidence Quality | 0.80 | 0.86 | +0.06 |
| Actionability | 0.83 | 0.88 | +0.05 |
| Traceability | 0.87 | 0.91 | +0.04 |
| **Composite** | **0.824** | **0.872** | **+0.048** |

**Computation:**
```
Post-(A) composite =
  (0.86 × 0.20) + (0.87 × 0.20) + (0.88 × 0.20)
+ (0.86 × 0.15) + (0.88 × 0.15) + (0.91 × 0.10)
= 0.172 + 0.174 + 0.176 + 0.129 + 0.132 + 0.091
= 0.874
```

*(Rounding: 0.872–0.874 depending on rounding order)*

**Projected post-(A) verdict:** REVISE — 0.874 is below the 0.92 gate and below the 0.95 project target.

**Is the remaining gap dominated by (B) Phase-2 items?** Yes.

The primary ceiling after (A) fixes is the publisher-independence architectural gap (B-01): even with the "protected surface" framing corrected to an honest scope statement, the underlying architecture remains one where the integrity monitor's reference value is written by the same CI job with the same credentials that creates the artifact being monitored. This is an accepted architectural limitation of the Phase-1 design that requires Phase-2 STRIDE to resolve (either via a genuinely independent reference surface or via formal risk-acceptance with documented bounds). This single architectural gap holds Evidence Quality and Methodological Rigor below 0.90 after (A) fixes.

The path to 0.95 requires:
1. Phase-2 STRIDE: establish genuinely independent reference surface for the integrity anchor (B-01)
2. Phase-2 STRIDE: tag-on-main provenance assertion (B-02)
3. Phase-2 STRIDE: R-007b consequence re-rating with evidence (B-05)
4. Phase-4: Completion of REQ-034 dimension (d) CoWork smoke test with a live CoWork runtime
5. Phase-5/6: CI implementation artifacts (monitoring workflows, generation script)

---

## Improvement Recommendations

Priority ordered by dimension weight × finding severity:

| Priority | Finding | Dimension(s) | Current | Target | Recommendation |
|----------|---------|-------------|---------|--------|----------------|
| 1 | A-01: Correct "protected surface" framing | Evidence Quality, Internal Consistency | 0.80, 0.82 | 0.86, 0.87 | Remove "governed by main/release permissions" claim; replace with explicit detection-scope statement in both ADRs |
| 2 | A-03: Add `contents: read` to monitor permissions | Completeness | 0.80 | 0.86 | Add `contents: read` to REQ-035 and NFR-006 permissions spec; without it the monitoring architecture is non-functional as written |
| 3 | A-02: Correct ADR-001 claim re rogue-tag detection | Evidence Quality | 0.80 | 0.86 | State that CI-triggered generation from attacker `v*` tag produces MATCH in monitor — monitoring does not cover this attack vector in Phase 1 |
| 4 | A-07: Fix REQ-022 AC wrong git ref | Internal Consistency, Actionability | 0.82, 0.83 | 0.87, 0.88 | Change `cowork-skeleton` to `HEAD` in the pre-push diff command; the gate as written silently validates against the old remote branch |
| 5 | A-06: Fix CC-6 backing requirement | Actionability, Traceability | 0.83, 0.87 | 0.88, 0.91 | Change ADR-002 CC-6 from REQ-037 to REQ-021; incorrect trace misdirects Phase-6 implementers |
| 6 | A-08: Add dimension-d gate resolution | Completeness, Traceability | 0.80, 0.87 | 0.86, 0.91 | Add resolution clause to REQ-034 (locally-generated dry-run branch); add to ORCHESTRATION_PLAN approval gate |
| 7 | A-04: Add post-publish verification | Completeness | 0.80 | 0.86 | Add post-publish verification step to REQ-035 AC; silent publish failure leaves monitor anchor absent |
| 8 | A-05: Add meta-monitoring requirement | Completeness | 0.80 | 0.86 | Add NFR-006 meta-monitoring requirement; monitor self-failure makes SLA unbounded |
| 9 | A-10: Reduce cadence to hourly | Methodological Rigor | 0.84 | 0.88 | Change NFR-006/REQ-035 scheduled cadence to ≤ hourly for tamper-detection; 24h is too long for executable-hook blast radius |
| 10 | A-09: Add CC for build-status precondition | Completeness, Traceability | 0.80, 0.87 | 0.86, 0.91 | Add CC entry to ADR-002 table; PM-007 noted the self-certifying checklist incorrectly claims all CCs have requirements |
| 11 | A-11: Recalibrate thresholds to 5 Mbps | Evidence Quality, Methodological Rigor | 0.80, 0.84 | 0.86, 0.88 | At 5 Mbps, 250 MB hard-fail is 3.3× the timeout-trigger size; recalibrate and document reference bandwidth |
| 12 | A-12/A-13: Windows and uv gaps | Completeness, Actionability | 0.80, 0.83 | 0.86, 0.88 | State Windows CoWork as unsupported; add uv-detection hook requirement to STORY-002 |
| 13–23 | A-14 through A-23 | Various | — | — | Minor precision fixes (PM-003, DA-004, IN-006, CC-002, CC-003, CV-006, CV-005, FM-13, SM-001/002/003) |

---

## Leniency Bias Check

- [x] Each dimension scored independently before computing composite
- [x] Evidence documented for each score with specific finding IDs
- [x] Uncertain scores resolved downward (Evidence Quality: chose 0.80 not 0.82 given 5-strategy convergence on the "protected surface" claim; Completeness: chose 0.80 not 0.82 given CV-002 makes the core monitoring architecture non-functional as written)
- [x] Third-iteration calibration: 0.824 for a C4 third-iteration deliverable with 6 Critical findings and 35 Major findings across 8 strategies is consistent with "good work with clear improvement areas (0.70)" to "strong work with minor refinements (0.85)"; 0.824 sits at the appropriate point given the architecture is genuinely sophisticated but the new IT3 content introduced multiple concrete gaps
- [x] No dimension scored above 0.95 (highest is Traceability at 0.87, justified by the CC-to-REQ table being the primary IT3 gain)
- [x] The 6 Critical findings are properly weighted in Evidence Quality and Internal Consistency rather than averaged into the overall score
- [x] Composite verified: 0.80(0.20)+0.82(0.20)+0.84(0.20)+0.80(0.15)+0.83(0.15)+0.87(0.10) = 0.160+0.164+0.168+0.120+0.125+0.087 = **0.824** ✓

---

## Session Context Handoff

```yaml
verdict: REVISE
composite_score: 0.824
threshold: 0.92
project_target: 0.95
weakest_dimension: completeness
weakest_score: 0.80
critical_findings_count: 6
critical_root_causes: 3
  # (1) Publisher-independence: Release notes share write permission with branch (DA-001/RT-001/FM-01/CV-004/IN-001)
  # (2) CI-triggered rogue-tag attack: monitoring cannot detect well-formed attacker v* tag CI run (RT-002/DA-005)
  # (3) Detection SLA + executable hooks: 24h worst-case window for hook distribution (PM-001/FM-02)
phase_1_fixable_issues: 23
phase_2_deferred_items: 7
projected_post_a_score: 0.874
projected_post_a_verdict: REVISE
gap_to_gate_after_a_fixes: -0.046
gap_dominated_by_phase2: true
iteration: 3
h14_minimum_satisfied: true
improvement_recommendations:
  - "Remove 'protected surface' framing from ADR-002/ADR-001; add detection-scope statement"
  - "Add contents:read to REQ-035/NFR-006 monitor permissions (monitoring non-functional without it)"
  - "Correct ADR-001 rogue-tag detection claim"
  - "Fix REQ-022 AC: use HEAD not cowork-skeleton in pre-push diff"
  - "Fix ADR-002 CC-6 backing requirement from REQ-037 to REQ-021"
  - "Add REQ-034 dimension-d resolution clause and ORCHESTRATION_PLAN approval gate"
  - "Add post-publish verification step to REQ-035"
  - "Add meta-monitoring requirement to NFR-006"
  - "Reduce scheduled tamper-detection cadence to hourly"
  - "Add CC for build-status precondition (PM-007)"
```

---

*Generated by: jerry:adv-scorer (adv-scorer)*
*Strategy: S-014 LLM-as-Judge*
*SSOT: `.context/rules/quality-enforcement.md`*
*Project: PROJ-031-cowork-skeleton*
*Workflow: cowork-skeleton-20260626-001 / Phase 1 / QG-1 Iteration 3*
*All 8 strategy findings read before scoring (S-001, S-002, S-003, S-004, S-007, S-011, S-012, S-013)*
*Date: 2026-06-26*
*H-15 self-review applied before persistence*
