# Devil's Advocate Report: PROJ-031-cowork-skeleton Phase 1 Deliverables — Iteration 3

**Strategy:** S-002 Devil's Advocate
**Deliverables:** phase1-requirements.md (iter 3), ADR-001-skeleton-derived-branch-strategy.md (iter 3), ADR-002-ci-token-push-strategy.md (iter 3)
**Criticality:** C4
**Date:** 2026-06-26
**Reviewer:** adv-executor (Group C — Challenge, Blind Independent)
**H-16 Compliance:** S-003 Steelman applied in iteration-003 (confirmed — s-003-steelman-findings.md present in same iteration directory)

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Overall assessment and recommendation |
| [Findings Table](#findings-table) | All findings with severity and affected dimension |
| [Detailed Findings](#detailed-findings) | Evidence, counter-argument, and response requirements for each finding |
| [Recommendations](#recommendations) | Prioritized action list (P0/P1/P2) |
| [Scoring Impact](#scoring-impact) | Devil's Advocate findings mapped to S-014 dimensions |
| [Execution Statistics](#execution-statistics) | Protocol step completion and finding counts |

---

## Summary

Seven counter-arguments identified (1 Critical, 4 Major, 2 Minor) across the three iteration-3 deliverables. The iteration-3 fixes made genuine progress: the async publish-then-assert architecture correctly identifies the tautology problem of in-CI gates, REQ-035/036/037 close the ADR-prose-vs-requirements gap from iteration 2, and the four-dimensional R-001 gate is a meaningful improvement. However, the most significant remaining gap is that the "protected surface" claim for GitHub Release notes — the integrity architecture's reference-value anchor — is factually unsupported against Write-level collaborators (the primary R-007b threat actors), because Release note editing requires the identical `contents: write` permission as direct branch push. A coordinated tamper (branch + Release notes) defeats the entire monitoring architecture. The async monitoring genuinely narrows the detection window for uncoordinated single-actor tampering, but the "protection" framing is stronger than the underlying access control warrants. Recommendation: **REVISE** to address the 1 Critical finding and 4 Major findings before proceeding to QG-1 final scoring.

---

## Findings Table

| ID | Finding | Severity | Evidence Location | Affected Dimension |
|----|---------|----------|-------------------|--------------------|
| DA-001-20260626I3 | GitHub Release notes are NOT more protected than the unprotected branch against Write-level collaborators — coordinated tamper (branch + Release notes) defeats the integrity monitor | Critical | ADR-002 §Continuous Integrity Monitoring; REQ-035 AC | Methodological Rigor |
| DA-002-20260626I3 | Async monitoring bounds the detection window but does NOT prevent executable-hook distribution during that window — the ≤ 24 h SLA is the exposure window, not a mitigation of it | Major | ADR-002 §Continuous Integrity Monitoring; R-007b row in Risk Implications | Evidence Quality |
| DA-003-20260626I3 | Dimension (d) smoke test has an undocumented circular dependency: the branch it must install does not exist until Phase 5, which it must gate | Major | REQ-034 §Verification Approach, REQ-034 AC (d); ORCHESTRATION_PLAN phase sequence | Completeness |
| DA-004-20260626I3 | The event-driven monitor's loop-safety and detection depend entirely on the GITHUB_TOKEN non-retrigger property — the failure mode of this property is not analyzed | Major | ADR-002 §Loop-Safety Argument guarantee (3); §Continuous Integrity Monitoring event-driven leg | Methodological Rigor |
| DA-005-20260626I3 | The allow-list validates tag syntax only; a malicious but syntactically valid tag triggers legitimate CI generation of a tampered branch — and the integrity monitor then validates it as PASS | Major | ADR-001 §Tag-name sanitization RT-004 "Scope boundary"; REQ-036 | Evidence Quality |
| DA-006-20260626I3 | The lazy-staleness check (Source-Commit trailer) is defeated by any deliberate direct push that writes the correct trailer — its utility is narrower than the "two complementary checks" framing implies | Minor | NFR-006 check (1); ADR-002 §Non-forgeable comparator paragraph | Internal Consistency |
| DA-007-20260626I3 | After a mismatch alert (GitHub issue creation), the mandatory Phase-1 floor specifies no remediation owner, timeline, or steps — creating an undocumented gap between detection and restoration | Minor | NFR-006 AC; ADR-002 §Automation mode "Mandatory floor: detect-and-alert" | Actionability |

---

## Detailed Findings

### DA-001-20260626I3: Release Notes Are NOT a Protected Surface Against the Primary Threat Actor [CRITICAL]

| Attribute | Value |
|-----------|-------|
| **Severity** | Critical |
| **Section** | ADR-002 §Continuous Integrity Monitoring (publish step); REQ-035 |
| **Strategy Step** | Step 3 — Construct Counter-Arguments (lens: Unstated Assumptions) |

**Claim Challenged:**
> "CI publishes the expected deterministic SHA for the release to a **durable, off-branch, protected surface** — the GitHub **Release notes** for the `v*` tag (Releases are governed by `main`/release permissions, not by the unprotected branch)." — ADR-002 §Continuous Integrity Monitoring

**Counter-Argument:**
GitHub Release notes are NOT more access-controlled than the `cowork-skeleton` branch against Write-level repository collaborators — the primary R-007b threat actors. GitHub's permission model grants the `contents: write` scope access to BOTH branch push operations AND release create/edit operations. This is demonstrated by REQ-035's own acceptance criterion: `gh release edit v{TAG} --notes-append "cowork-skeleton-sha: <40-char-sha>"` — the `gh release edit` command operates under the same `contents: write` scope declared in REQ-020/NFR-004 for the GITHUB_TOKEN. Any Write-level collaborator who can push directly to the unprotected `cowork-skeleton` branch (the R-007b actor) can ALSO edit the Release notes.

The consequence is that a coordinated attack — (1) push a tampered commit to `cowork-skeleton`, (2) compute the new tip SHA, (3) update the Release notes to show THAT SHA — causes EVERY integrity monitor assertion to PASS against a compromised branch. The event-driven leg compares `git rev-parse cowork-skeleton` against the Release notes SHA: both reflect the tampered content → PASS. The scheduled backstop does the same comparison: PASS. The "non-forgeable tip SHA" is non-forgeable in the sense that git derives it from the actual published tree — but the REFERENCE VALUE stored in Release notes is equally accessible to the threat actor.

The entire continuous integrity monitoring architecture rests on the Release notes being "protected" relative to the branch. This characterization holds only against unauthenticated public users — not against the Write-level collaborators the deliverables identify as the primary R-007b threat.

**Impact:**
If this counter-argument is valid, the integrity monitoring architecture does not detect coordinated tamper by Write-level collaborators — exactly the adversarial scenario the architecture is designed to bound. The "guaranteed ≤ daily detection SLA" is not guaranteed against this actor class.

**Dimension:** Methodological Rigor — the integrity architecture's soundness depends on a permission model claim that is not established.

**Response Required:**
The creator must either (a) establish that GitHub Release notes require a higher permission level than `contents: write` for the repo's Write-role collaborators, citing a specific GitHub permission model reference; OR (b) acknowledge that the "protected surface" characterization is limited to public/unauthenticated actors, revise the framing to remove the "protected" claim for the R-007b threat model, and document the residual: coordinated Write-collaborator tamper is not detectable by the current monitoring architecture (it remains detectable only if the attacker omits step 3 above — i.e., lazy attackers only). Option (b) should then specify whether Phase-2 STRIDE should evaluate branch-protection escalation specifically for this residual.

**Acceptance Criteria:**
Either (a) a cited GitHub documentation reference showing Release editing requires a stricter role than Write — and confirmation that the GITHUB_TOKEN with `contents: write` is NOT sufficient to edit Releases (falsified by REQ-035's `gh release edit` AC); OR (b) revised ADR-002 and REQ-035 language that: removes "protected" from the Release notes description, explicitly scopes the monitor's detection guarantee to "single-actor uncoordinated direct push (i.e., attacker does not also edit Release notes)," and adds a Risk Implications row for coordinated tamper at appropriate L×C score.

---

### DA-002-20260626I3: Async Monitoring Bounds the Exposure Window — It Does Not Prevent Hook Distribution During That Window [MAJOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Section** | ADR-002 §Continuous Integrity Monitoring; R-007b row, Risk Implications (phase1-requirements.md) |
| **Strategy Step** | Step 3 — Construct Counter-Arguments (lens: Unaddressed Risks) |

**Claim Challenged:**
> "It **does** bound that window and, with auto-revert, automatically heal it; and it makes any tamper **provable** via the non-forgeable SHA." — ADR-002 §Branch-Protection Posture

**Counter-Argument:**
The deliverables frame the async monitoring as "genuinely defending" the unprotected branch and providing "verifiable-integrity posture." The more precise characterization is: it bounds the DETECTION window. During the detection window (best-effort minutes via event-driven leg; guaranteed ≤ 24 hours via scheduled leg), a tampered `cowork-skeleton` containing malicious executable hooks IS installable by CoWork users. Detection + the mandatory detect-and-alert floor then: creates a GitHub issue → a maintainer notices → the maintainer manually reverts (Phase 1 only; auto-revert is Phase 2). The tamper is only healed AFTER this human chain completes — likely hours beyond the detection event itself.

Users who installed during the tamper window have already received the malicious hooks. The hooks execute at session start (`hooks/session-start.py`). The R-007b risk row already notes "C=4 (Major); pending Phase-2 STRIDE re-analysis for potential C=5 upgrade" and explicitly flags the "executable hooks on user workstations (R-007b, IT3-007)" concern. If C is re-rated to 5 (Critical) in Phase-2 STRIDE, the current "bounded detection window" framing will need to be revisited: a 24-hour guaranteed-worst-case exposure window for critical malicious code distribution on user workstations is a risk acceptance that Phase-1 should not preempt.

The "what the monitoring actually defends" section in ADR-002 is commendably honest: "This is a **detection** control, not **prevention**." The issue is that iteration-3 remediations may have created an impression that the async monitoring "closes" the R-007b gap, when it bounds it to a stated SLA that may be re-evaluated as inadequate in Phase-2 STRIDE.

**Impact:**
Phase-2 STRIDE may determine that the ≤ 24 h detection SLA + manual revert is insufficient for the hook blast radius — requiring escalation to branch protection (prevention). If Phase-1 requirements establish the detection SLA as an accepted control without establishing a Phase-2 re-evaluation criterion, Phase-2 may be insufficiently scoped.

**Dimension:** Evidence Quality — the monitoring's efficacy framing is asserted but not evaluated against the consequence severity it is claimed to bound.

**Response Required:**
Add to the R-007b Risk Implications row an explicit Phase-2 STRIDE trigger condition: if STRIDE analysis confirms C=5 (Critical — malicious hooks on user workstations), the detection-SLA posture SHALL be evaluated against that consequence and the branch-protection prevention upgrade SHALL be assessed as a Phase-2 mandatory control rather than an optional escalation path. The current framing implies Phase-2 makes the determination; the requirement should specify what Phase-2 must deliver in the STRIDE output for this risk.

**Acceptance Criteria:**
R-007b row or a supporting note explicitly states: "Phase-2 STRIDE shall determine whether C=5 re-rating requires branch-protection as a mandatory control; if C=5 is confirmed, the ≤ daily detection SLA is insufficient as the sole control and detection-to-prevention escalation SHALL be a Phase-2 deliverable, not an optional upgrade." Or equivalently: the Phase-2 STRIDE scope (STORY-004) explicitly lists the R-007b consequence re-rating and detection-vs-prevention decision as required outputs.

---

### DA-003-20260626I3: Dimension (d) Smoke Test Has an Undocumented Circular Dependency With Phase 5 [MAJOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Section** | REQ-034, REQ-034 AC (d); WS-5; Stated Assumption R-001 §Verification Approach |
| **Strategy Step** | Step 3 — Construct Counter-Arguments (lens: Unstated Assumptions) |

**Claim Challenged:**
> "dimension (d) MAY be deferred to Phase 4 completion if a CoWork runtime is unavailable before Phase 2; the artifact SHALL record 'DEFERRED — required before Phase 5'" — REQ-034 Rationale

**Counter-Argument:**
Dimension (d) requires installing `geekatron/jerry@cowork-skeleton` in a running CoWork-compatible client. This presupposes that the `cowork-skeleton` branch exists and contains the expected skeleton content. The `cowork-skeleton` branch is created by Phase 5's CI workflow implementation (specifically STORY-001 + TASK-002). REQ-034 blocks Phase 5 until all four dimensions show PASS (or dimension d shows DEFERRED). This creates a circular dependency:

- Dimension (d) requires the `cowork-skeleton` branch → branch requires Phase 5 → Phase 5 requires dimension (d) PASS or DEFERRED status

The DEFERRED path breaks the loop (Phase 5 can proceed with DEFERRED), but the PASS path requires the branch to exist before Phase 5. The deliverables do not document how dimension (d) achieves PASS status independently of Phase 5. A pragmatic resolution — manually creating the branch using local git operations as a pre-Phase-5 verification step — is not described anywhere in the requirements, ADRs, or risk implications.

The result: implementers reading REQ-034 may conclude that dimension (d) can only achieve PASS if they manually execute the Phase-5 generation script locally on a development machine before the CI workflow exists. This is a valid approach, but it is undocumented, unvalidated (the locally-generated branch is not produced by the CI workflow REQ-018 tests), and potentially inconsistent with the bit-identical idempotency guarantee (REQ-003/NFR-001) — which applies to the CI-run generator, not a manually-run local instance.

**Impact:**
Implementers may either (a) treat dimension (d) as always-DEFERRED (weakening R-001 verification) or (b) need to reverse-engineer an unspecified manual branch creation step, creating a verification artifact that tests a different execution context than the actual CI pipeline.

**Dimension:** Completeness — the four-dimensional gate has an unspecified execution path for its most critical dimension.

**Response Required:**
REQ-034 must document the execution path for achieving dimension (d) PASS before Phase 5: either (a) explicitly state that dimension (d) requires manually executing the generation script locally against the intended release tag and installing the resulting branch via a local git push to the repo before Phase 5; OR (b) formally accept that dimension (d) is always-DEFERRED to Phase 4 (with a note that Phase 4 documentation work can co-occur with a freshly-CI-generated branch after Phase 5's first CI run on a non-blocking test tag) and add this constraint to the Phase sequencing ORCHESTRATION_PLAN. The acceptance criterion for dimension (d) should specify whether the tested branch is CI-generated or manually generated.

**Acceptance Criteria:**
REQ-034 or its cross-referenced R-001 §Verification Approach contains an explicit statement of one of: (a) the manual pre-Phase-5 execution path for dimension (d), including how the manually-generated branch relates to the CI-generated branch; or (b) a formal statement that dimension (d) is always-DEFERRED with its Phase-4 execution window defined in terms of a CI-generated branch (implying Phase 5 must run first in a non-blocking capacity before Phase 4 documentation).

---

### DA-004-20260626I3: GITHUB_TOKEN Non-Retrigger Property Is an Unanalyzed Single Point of Structural Failure in the Event-Driven Monitor [MAJOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Section** | ADR-002 §Loop-Safety Argument (guarantee 3); §Continuous Integrity Monitoring (event-driven fast path) |
| **Strategy Step** | Step 3 — Construct Counter-Arguments (lens: Unaddressed Risks) |

**Claim Challenged:**
> "The very `GITHUB_TOKEN` property chosen here both prevents the regenerate loop **and** makes near-real-time tamper detection possible without a downstream-trigger credential." — ADR-002 §Loop-Safety Argument

**Counter-Argument:**
The entire event-driven monitoring architecture exploits a single behavioral property of `GITHUB_TOKEN`: that pushes made with it do not trigger `on: push` workflows. This property is used twice: (1) for loop-safety in the generation workflow, and (2) to ensure the event-driven monitor fires on direct pushes but NOT on CI's regeneration pushes. Both uses depend on the same GitHub runtime behavior.

The deliverables cite GitHub documentation for this property (reference [3] in ADR-002: "events triggered by the `GITHUB_TOKEN`... will not create a new workflow run"). However, the failure mode of this property is not analyzed:

- **Scenario A (property degrades):** If GitHub changes this behavior (e.g., for `push` events to branches, in a GitHub Enterprise environment, or via a future platform update), CI's own regeneration push begins firing the event-driven monitor. The monitor runs, compares the correct SHA (CI just pushed it) to the Release notes SHA (CI just published it), and passes. This is a false PASS (the monitor fired when it shouldn't have), but it appears normal. The monitor's alert credibility remains intact for this case.

- **Scenario B (property partially degrades):** More concerning — if the property only partially degrades (fires sometimes but not always), the monitor produces intermittent alerts. Maintainers treating intermittent alerts as CI noise may disable the event-driven leg, removing the near-real-time detection entirely and leaving only the ≤ daily scheduled backstop.

- **Scenario C (undetected dependency inversion):** A future GitHub Actions update might introduce a `no-retrigger` attribute on `GITHUB_TOKEN` that can be disabled at org level. If this is set to disabled (by an org admin or via a GitHub Enterprise configuration), the loop-safety guarantee (3) silently fails without any workflow-level indication.

The deliverables treat guarantee (3) as a reliable architectural invariant, but cite only external documentation and provide no monitoring, no CI assertion, and no fallback behavior if the property fails. For a C4 quality gate, a structural invariant with no failure-mode analysis weakens the overall security argument's rigor.

**Impact:**
If the GITHUB_TOKEN non-retrigger property degrades, the event-driven monitor's loop-safety fails. The downstream effect ranges from noisy false-positive alerts (benign) to the monitor being disabled (losing near-real-time detection, leaving only the ≤ daily backstop).

**Dimension:** Methodological Rigor — a load-bearing property supporting loop-safety and tamper detection has no failure-mode documentation or compensating control.

**Response Required:**
ADR-002 should add a "Failure Mode Analysis — Guarantee (3)" note that: (a) identifies what would happen if `GITHUB_TOKEN` pushes began triggering `push:branches` events; (b) specifies whether the concurrency group on the generation workflow (`cancel-in-progress: false`, REQ-015) provides any protection; and (c) documents the compensating control (the ≤ daily scheduled backstop remains functional regardless of the non-retrigger property, so the worst-case detection fallback is the scheduled leg).

**Acceptance Criteria:**
ADR-002 §Loop-Safety Argument or §Continuous Integrity Monitoring contains a note identifying the GITHUB_TOKEN non-retrigger property as a platform-behavioral assumption and stating: "If this property fails, the event-driven leg may fire on CI's own pushes (false positives) or fail to suppress — the scheduled backstop (≤ daily, not dependent on this property) provides the guaranteed detection floor independent of this behavioral guarantee."

---

### DA-005-20260626I3: Allow-List Validates Syntax — A Malicious CI Invocation Produces a Correctly-Monitored But Tampered Branch [MAJOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Section** | ADR-001 §Tag-name sanitization "Scope boundary — syntax vs. provenance (RT-003)"; REQ-036 |
| **Strategy Step** | Step 3 — Construct Counter-Arguments (lens: Unaddressed Risks) |

**Claim Challenged:**
> "The allow-list validates the tag's **syntax** only; it does **not** establish the tag's **provenance**... asserting that the resolved tag points at a commit reachable from `main`... is a **provenance** control... delegated to the Phase-2 STRIDE threat model." — ADR-001 §Tag-name sanitization

**Counter-Argument:**
The deliverables correctly identify and disclose the provenance gap. The Devil's Advocate challenge is whether the disclosure is adequately surfaced and whether the Phase-1 compensating control (deterministic-SHA integrity monitoring) actually covers this attack path.

The attack: a Write-level collaborator with `workflow_dispatch` permission invokes `cowork-skeleton.yml` with `inputs.target_tag` = `v9.9.9` where `v9.9.9` is a well-formed tag the attacker has pushed to the repo pointing at a malicious commit. The workflow:
1. Resolves `TAG = v9.9.9` (passes the allow-list)
2. Generates the skeleton from the malicious commit
3. Force-pushes the tampered `cowork-skeleton` branch via GITHUB_TOKEN
4. Publishes the deterministic SHA of the malicious-content branch to the Release notes (`gh release edit v9.9.9`)
5. The integrity monitor compares `git rev-parse cowork-skeleton` to the Release-notes SHA: MATCH → PASS

The integrity monitoring provides ZERO detection for this attack because CI legitimately created the tampered branch. The "compensating detective control" cited in the "Scope boundary" note detects only OUT-OF-CI direct pushes. A `workflow_dispatch`-based malicious generation is an IN-CI attack that produces a correctly-SHA'd, correctly-monitored, legitimately-published tampered artifact.

The risk is heightened because:
- `workflow_dispatch` permission is available to any repository collaborator (GitHub's model: anyone with Write access can trigger `workflow_dispatch`)
- ADR-001 explicitly states `inputs.target_tag` "is *exactly* as untrusted as `GITHUB_REF_NAME`"
- The Phase-1 period (before Phase-2 STRIDE) leaves this attack window open

The Risk Implications table does not contain a risk entry for this attack vector. It is mentioned only in the "Scope boundary" note in ADR-001, which is not in a risk-register format and does not specify the Phase-1 open window. A C4 reviewer expects risk entries for open, exploitable attack paths.

**Impact:**
A well-formed malicious tag + `workflow_dispatch` invocation can produce and legitimately publish a tampered `cowork-skeleton` branch that passes all monitoring. The Risk Implications table has no entry for this scenario.

**Dimension:** Evidence Quality — the risk is acknowledged in an ADR prose note but not elevated to the Risk Implications table with appropriate L×C scoring.

**Response Required:**
Add a risk entry to the Risk Implications table for "In-CI malicious tag invocation via `workflow_dispatch`" covering the vector: well-formed tag pointing at non-`main` commit + collaborator with `workflow_dispatch` permission. The entry should: (a) assign L×C score; (b) identify Phase-1 compensating controls (there are none beyond the allow-list syntax check); (c) explicitly state the Phase-2 STRIDE deliverable required to close this (tag-on-main provenance assertion or equivalent). Additionally, the Phase-2 deferred items table should include this vector by name, not just the generic "Tag-on-main provenance assertion" entry it currently has.

**Acceptance Criteria:**
Risk Implications table contains an entry for the `workflow_dispatch` + malicious-but-valid-tag attack vector with L×C score, explicit "Phase-1 partial coverage: none beyond syntax allow-list" notation, and a Phase-2 STRIDE entry by name. The Phase-2 Deferred Items table's "Tag-on-main provenance assertion" entry references this specific attack scenario.

---

### DA-006-20260626I3: The Lazy-Staleness Check's Utility Is Limited to Accidental CI Failures — Overstated as "Complementary" [MINOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Minor |
| **Section** | NFR-006 check (1); ADR-002 §Non-forgeable comparator paragraph |
| **Strategy Step** | Step 3 — Construct Counter-Arguments (lens: Alternative Interpretations) |

**Claim Challenged:**
> "The dual-check resolves both failure modes: trailer for staleness, non-forgeable tip SHA for tampering." — requirements NFR-006 rationale. And: "two independent, complementary checks" — NFR-006 AC preamble.

**Counter-Argument:**
The deliverables explicitly identify the Source-Commit trailer as forgeable ("free-form commit-message text any push actor can set to the correct value while shipping a different tree") and route it to lazy-staleness only. The counter-argument is that the "two complementary checks" framing overstates their combined coverage:

- A deliberate direct-push that includes the correct Source-Commit trailer value (trivially achievable) causes the lazy-staleness check to PASS (trailer matches latest tag SHA) while the tamper-detection check catches it (tip SHA ≠ Release-notes SHA). The checks are NOT independently detecting different attacks — the staleness check is defeated by ANY targeted attacker (who writes the correct trailer), and only the tamper-detection check catches it.

- The practical utility of the lazy-staleness check is therefore: detect ACCIDENTAL CI failures where the generator either did not run or produced an incorrect Source-Commit trailer. Against any deliberate actor, it provides no additional detection coverage beyond the tamper-detection check.

- The NFR-006 AC (test 2: "demonstrate that check (1) passes (trailer matches) but check (2) detects the tip-SHA mismatch") correctly captures this interaction. But the framing in NFR-006's rationale ("dual-check resolves BOTH failure modes") implies the lazy-staleness check provides coverage it does not provide against targeted actors.

**Impact:**
Framing issue only — no security gap beyond what is already documented. The tamper-detection check (tip SHA vs. Release notes SHA) correctly catches all tampering. The lazy-staleness check catches accidental CI failures. This is well-designed; the framing should reflect it more precisely.

**Response Required:**
NFR-006 rationale may optionally clarify: "The lazy-staleness check provides coverage for ACCIDENTAL CI failures only; a deliberate attacker who writes the correct Source-Commit trailer defeats the staleness check but not the tamper-detection check." Acknowledgment without revision is acceptable.

**Acceptance Criteria:**
Creator acknowledges the observation. Optional: NFR-006 rationale adds a parenthetical clarifying the staleness check's scope; or the language "two complementary checks" is softened to "two checks with distinct failure modes (accidental staleness vs. deliberate tamper)."

---

### DA-007-20260626I3: Post-Detection Remediation Path Is Not Specified — Gap Between Alert and Restoration [MINOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Minor |
| **Section** | NFR-006 AC; ADR-002 §Automation mode; R-007b row (Risk Implications) |
| **Strategy Step** | Step 4 — Require Substantive Responses (lens: Actionability) |

**Claim Challenged:**
> "Mandatory floor: **detect-and-alert** — on mismatch, open a GitHub issue and fail the run loudly (requires `issues: write`, IN-003)." — ADR-002 §Automation mode

**Counter-Argument:**
The Phase-1 mandatory detect-and-alert floor creates a GitHub issue on tamper detection. Neither the requirements nor the ADRs specify: who is responsible for acting on the issue, in what time window, what actions to take, or what the issue body should contain to enable rapid remediation. The Phase-2 auto-revert (STORY-004/005) will eventually close this gap, but in the Phase-1 state that AG-03 authorizes, a maintainer receiving the GitHub issue must independently determine the recovery steps (invoke `workflow_dispatch` for the affected tag, verify regenerated SHA, monitor re-run). During this unspecified manual recovery period, the tampered branch continues to be installable by CoWork users — the detection-to-restoration window is unbounded in Phase 1.

The `if: failure()` step in REQ-037 emits a structured diagnostic to `$GITHUB_STEP_SUMMARY` for push failures. An equivalent structured remediation guide in the GitHub issue created by NFR-006/REQ-035 mismatch detection would reduce response time substantially.

**Impact:**
Minor operational gap. The detection is sound; the restoration path is implicit rather than documented. No requirement blocks acceptance on this finding alone.

**Response Required:**
Optionally, specify in REQ-035 AC or NFR-006 AC that the GitHub issue body SHALL contain: (a) the affected tag, (b) the expected SHA (from Release notes), (c) the observed tip SHA, and (d) a remediation action: "Re-run `cowork-skeleton.yml` via `workflow_dispatch` with `inputs.target_tag`=`{affected tag}` to restore the correct tip SHA." Acknowledgment without revision is acceptable for a Minor finding.

**Acceptance Criteria:**
Creator acknowledges the observation. Optional improvement: REQ-035 or NFR-006 specifies that the GitHub issue body includes the affected tag, expected SHA, observed SHA, and remediation action pointer.

---

## Recommendations

### P0 — Critical: MUST resolve before acceptance

**DA-001-20260626I3 (Critical — Release notes protection claim)**

Either establish that GitHub Release note editing requires stricter permissions than `contents: write` for Write-level collaborators (with citation), or revise ADR-002 to:
1. Remove "protected" from the description of GitHub Release notes
2. Explicitly scope the monitor's detection guarantee to "single-actor uncoordinated direct push (attacker does not also edit Release notes)"
3. Add a Risk Implications row for "Coordinated tamper: branch + Release notes simultaneously updated by Write-level collaborator" with L×C score
4. Note that coordinated tamper is detectable only via out-of-band auditing (e.g., Release notes edit history), not by the current monitoring architecture

### P1 — Major: SHOULD resolve before proceeding to S-014 scoring

**DA-002-20260626I3 (Major — Hook blast radius vs. detection SLA)**

Add to R-007b row: explicit Phase-2 STRIDE trigger criterion specifying that if STRIDE confirms C=5, detection-to-prevention escalation becomes a mandatory Phase-2 deliverable. Clarify that the ≤ 24 h SLA is the exposure window, not a closure of R-007b.

**DA-003-20260626I3 (Major — Dimension (d) circular dependency)**

Document in REQ-034 the execution path for achieving dimension (d) PASS status independently of Phase 5: either the manual pre-Phase-5 branch creation path (with constraints on how the manually-generated branch relates to REQ-003/NFR-001), or a formal declaration that dimension (d) is always-DEFERRED with Phase-4 timing defined in terms of a CI-generated branch.

**DA-004-20260626I3 (Major — GITHUB_TOKEN non-retrigger failure mode)**

Add to ADR-002 §Loop-Safety Argument or §Continuous Integrity Monitoring a note identifying the GITHUB_TOKEN non-retrigger property as a platform-behavioral assumption and documenting the fallback: the ≤ daily scheduled backstop does not depend on this property and remains the guaranteed detection floor if the event-driven leg degrades.

**DA-005-20260626I3 (Major — Allow-list provenance gap not in Risk Implications)**

Add a Risk Implications table entry for "`workflow_dispatch` + malicious-but-valid-tag attack via `inputs.target_tag`" with L×C score and explicit Phase-1 compensating control (none beyond syntax check). Update Phase-2 Deferred Items table to reference this specific vector by name.

### P2 — Minor: MAY resolve; acknowledgment sufficient

**DA-006-20260626I3 (Minor):** Clarify that the lazy-staleness check (Source-Commit trailer) detects accidental CI failures only; any deliberate attacker who writes the correct trailer defeats it. The tamper-detection check handles all adversarial scenarios.

**DA-007-20260626I3 (Minor):** Specify in REQ-035 or NFR-006 that the GitHub issue body includes affected tag, expected SHA, observed SHA, and a remediation action pointer.

---

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Negative | DA-003: Dimension (d) execution path is unspecified, creating a silent gap in the four-dimensional gate implementation. DA-005: Attack vector (workflow_dispatch + malicious tag) absent from Risk Implications table. |
| Internal Consistency | 0.20 | Negative | DA-001: "Protected surface" characterization of Release notes is inconsistent with the permission model evidence (REQ-035 AC uses `gh release edit` with the same `contents: write` scope). DA-006: "Two complementary checks" framing is mildly inconsistent with the staleness check's explicitly forgeable comparator. |
| Methodological Rigor | 0.20 | Negative | DA-001 (Critical): Integrity architecture's core premise (Release notes are a more-protected surface) is unsupported. DA-004: A load-bearing behavioral assumption (GITHUB_TOKEN non-retrigger) has no failure-mode documentation. |
| Evidence Quality | 0.15 | Negative | DA-002: The claim that async monitoring "genuinely defends" the branch against executable-hook distribution is not supported by evidence that the detection window is acceptable for C=4/5 consequences. DA-005: The provenance gap's risk is disclosed in ADR prose but not substantiated in the Risk Implications evidence base. |
| Actionability | 0.15 | Slightly Negative | DA-007: Post-detection remediation path unspecified. Otherwise, P0/P1 findings each have clear response requirements. Overall actionability of the deliverables is good; this is a minor gap. |
| Traceability | 0.10 | Neutral | Traceability is strong across the three deliverables (STK→REQ→ADR CC traces closed in iteration 3). DA-005 adds a gap in the risk register but does not break existing traces. |

**Overall assessment:** Major revision targeted at the Critical finding (DA-001) is required before S-014 scoring; addressing DA-003 and DA-005 (Major findings) would additionally close evidence and completeness gaps. The iteration-3 deliverables are substantially improved from iteration 2, with the async publish-then-assert architecture, REQ-035/036/037, and four-dimensional R-001 gate representing genuine progress. The Critical DA-001 finding challenges the architecture's load-bearing premise, not its overall design direction.

---

## Execution Statistics

- **Total Findings:** 7
- **Critical:** 1 (DA-001)
- **Major:** 4 (DA-002, DA-003, DA-004, DA-005)
- **Minor:** 2 (DA-006, DA-007)
- **Protocol Steps Completed:** 5 of 5
- **H-16 Compliance:** Confirmed (S-003 Steelman findings present in iteration-003 directory)
- **Deliverables Reviewed:** 3 (phase1-requirements.md iter-3, ADR-001 iter-3, ADR-002 iter-3)

---

*Strategy: S-002 Devil's Advocate*
*Execution ID: 20260626I3*
*Template: .context/templates/adversarial/s-002-devils-advocate.md (v1.0.0)*
*Agent: adv-executor (Group C — Challenge, Blind Independent)*
*Date: 2026-06-26*
*Project: PROJ-031-cowork-skeleton / QG-1 Iteration 3*
