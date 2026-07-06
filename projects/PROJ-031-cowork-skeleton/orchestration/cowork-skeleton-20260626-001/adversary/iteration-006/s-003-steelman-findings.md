# Steelman Report: PROJ-031 CoWork Skeleton Architecture

## Steelman Context

- **Deliverable:** Five-artifact set: ADR-001, ADR-003, phase1-requirements.md, phase2-stride-threat-model.md, phase2-attack-surface.md (HISTORICAL recon input — not evaluated as current design)
- **Deliverable Type:** ADR + Security + Requirements (multi-artifact C4 design package)
- **Criticality Level:** C4
- **Strategy:** S-003 (Steelman Technique)
- **SSOT Reference:** .context/rules/quality-enforcement.md
- **Steelman By:** adv-executor (blind tournament, iteration-006 Group B) | **Date:** 2026-06-29T00:00:00Z | **Original Authors:** ps-architect, eng-architect, nse-requirements

---

## Summary

**Steelman Assessment:** The PROJ-031 design represents a mature, multi-layer supply-chain security architecture for an executable-instructions artifact distributed at org scale. Its core structural moves — dedicated-repo prevention, CI-only-writable Sigstore attestation, D8 content-safety gate, and an honest Claim-Status Convention — are sound and defensible at C4. The design's strongest intellectual contribution is recognizing that five independent prior adversarial strategies each independently rediscovered the same structural failure (Release notes sharing `contents: write` with the artifact) and then architecturally eliminating that failure class rather than patching around it.

**Improvement Count:** 0 Critical, 3 Major, 3 Minor (6 total)

**Original Strength:** Pre-Steelman quality is high. The documents are remarkably self-aware: they distinguish designed-but-not-validated from achieved, name trust boundaries honestly (RTB-1 through RTB-5), and explicitly refuse to assert "is prevented" where the correct statement is "is designed to prevent." The weaknesses surviving steelman scrutiny are specification completeness gaps, not conceptual flaws.

**Recommendation:** Incorporate improvements before Devil's Advocate and Pre-Mortem strategies proceed. The 3 Major findings target under-specified areas that critique strategies will attack hard: D8 bootstrapping, G-update fallback scope, and D5 interim gap. Addressing them pre-emptively prevents those valid attacks from landing as unfair.

---

## Steelman Reconstruction

The following presents the design's strongest possible argument, with inline SM-NNN annotations marking where improvements strengthen an already-sound case.

### Core Thesis (strongest framing)

The design correctly identifies a class-level structural failure in its predecessor (the Phase-1 model), not merely an instance failure. When five independent adversarial strategies independently converge on the same Critical (Release notes sharing `contents: write` with the artifact branch), the correct response is to eliminate the structural condition that makes the failure possible, not to add more detection around it. The dedicated-repo model achieves exactly this: by moving the artifact to a separate repository, the artifact branch becomes protectable independently of the source repo's write-collaborator surface, and the integrity anchor moves to a surface (immutable release + Sigstore build-provenance attestation) that CI alone can write. No write-level collaborator on `geekatron/jerry` has any access path to `geekatron/jerry-cowork`. This is a genuine architectural improvement, not a cosmetic one.

### Strongest Case FOR the Generation Strategy (ADR-001)

The decisive framing — that CoWork materializes only the tip working tree, not history — correctly eliminates the entire filter-repo/subtree-split option class. This is not a convenience observation; it is a principled argument that the problem being solved (installed file count at the tip) has no relationship to what those techniques solve (historical object count). Option A's idempotency is provably bit-identical under the pinning scheme: since the commit SHA is a deterministic hash of (tree, parent, identity, author_date, committer_date, message), and all six inputs are pinned to values that are invariant for a given release tag, `regenerate(T)` is referentially transparent. This proof has practical consequence: the acceptance test for the file count is not just stable — it is definitionally stable, because any deviation from the expected tip SHA is detectable and attributable.

The clone-weight continuous monitoring decision [SM-001 would say: augment by specifying the "last-good tag" definition for auto-revert] is methodologically superior to a single-shot gate. The early-warning band (150 MB / 40 s at 60% of trigger) ensures the Option B orphan flip is proactive, never reactive. The orphan flip being integrity-neutral (post-IT3-004) means the provenance vs. weight trade-off can be taken purely on weight grounds later, without weakening the supply-chain story.

### Strongest Case FOR the Security Architecture (ADR-003)

The eight-decision structure cleanly separates orthogonal concerns: D1 (where), D2 (protection), D3 (credential), D4 (anchor), D5 (provenance), D6 (runner hardening), D7 (monitor), D8 (content). Each decision is grounded in a specific STRIDE threat or threat cluster. No decision is made without a named threat it closes and a gate that validates it. This is the structure of a C4-quality security architecture.

D8 is the architecture's most important conceptual addition. Every D1–D7 control proves that the published skeleton equals what CI built — integrity. None of them can see whether what CI built contains hostile instructions, because the tree IS exactly what CI built. D8's placement (after the D6 faithful-derivative + secret-scan gates, before attestation and push) guarantees that the attested artifact is the scanned artifact — there is no window in which an unscanned tree could be attested or shipped. The fail-closed requirement (scanner error = block) is the correct posture for a blocking gate on an executable artifact: a gate that can be bypassed by a scanner crash is not a gate.

The Claim-Status Convention is itself a strength. The design explicitly refuses to write "is prevented" when the correct statement is "is designed to prevent (G-x pending)." This epistemic honesty protects against false assurance at the moment these Phase-2 controls matter most: before they are validated, before the infrastructure exists. The three design-only controls that block go-live (D2, D5, D8) are named as blockers, not hedged.

### Strongest Case FOR the Requirements (phase1-requirements.md)

The six-gate Phase-5 Authorization Checklist (G-prevention ∧ G-update ∧ G-provenance ∧ G-content ∧ G-monitor ∧ G-headroom, all AND-pass) converts the "designed-but-not-validated" status into an explicit, testable authorization predicate. Removing the "MAY defer dimension (d)" language for G-headroom (PM-002 closure) is methodologically correct — a file-count-only gate cannot falsify a size/time-based ceiling, so a file-count-only pass is logically insufficient to establish installability. The four-dimensional R-001 verification (tracked file count + pack size + clone time + live CoWork smoke test) is the right verification scope.

The requirements' bi-directional trace (STK→REQ, REQ→verification method, REQ→acceptance criterion) and the explicit Allocation Matrix are evidence of systematic requirements engineering, not bureaucratic overhead. At C4, where an implementation error in a SHALL requirement ships to every org user's session on next install, this traceability is load-bearing.

### Best Case Scenario

This architecture is most compelling under these conditions:
1. GitHub's immutable-release + build-provenance attestation feature works as documented on `geekatron/jerry-cowork` (G-monitor validates this)
2. GitHub's ruleset bypass-actor semantics (Sep 2025 feature) correctly allow the CI App as sole bypass actor (G-prevention validates this)
3. CoWork propagates default-branch updates to already-installed users within a bounded window (G-update validates this)
4. The D5 provenance gate (tag-on-main ancestor assertion + `v*` tag protection) is implemented before any release ships to org users (SC-02 DREAD 7.6 otherwise stays open)
5. The D8 content-safety pattern catalog correctly covers the adversarial template corpus without excessive false positives (G-content validates this)

**Rational evaluator confidence, post-steelman:** HIGH on the structural soundness of the architecture; MEDIUM on operational validation pending the Phase-5 gates; LOW-MEDIUM on D8 effectiveness pending the allow-list bootstrap procedure being specified [SM-001] and on G-update being provable [SM-002].

---

## Improvement Findings Table

| ID | Improvement | Severity | Affected Dimension | Section |
|----|-------------|----------|--------------------|---------|
| SM-001-it006 | Specify D8 allow-list bootstrap procedure for adversarial-template corpus | **Major** | Completeness, Methodological Rigor | ADR-003 §D8 / STRIDE §D8 Detector Spec |
| SM-002-it006 | Design the G-update failure-case recovery path (not just re-scope the claim) | **Major** | Actionability, Completeness | ADR-001 §L2 #6 / Phase-5 Gate Set §G-update |
| SM-003-it006 | Specify interim compensating control for D5 gap (design-to-implementation window) | **Major** | Completeness, Evidence Quality | ADR-003 §D5 / STRIDE §SC-02 |
| SM-004-it006 | Clarify whether R-001 verification preceded Phase 2 start as required | **Minor** | Traceability, Internal Consistency | requirements §Stated Assumption R-001 |
| SM-005-it006 | Add recovery SLA and tested runbook to RTB-3 (org-registration process control) | **Minor** | Actionability | ADR-003 §RTB-3 |
| SM-006-it006 | Justify the 2-hour D7 freshness window and define "last-good tag" for auto-revert | **Minor** | Evidence Quality, Methodological Rigor | ADR-003 §D7 / requirements REQ-049 |

---

## Improvement Details

### SM-001-it006: D8 Allow-List Bootstrap Procedure

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Section** | ADR-003 §D8 Content-Safety Gate — Detector Specification; STRIDE §D8 Detector Specification |
| **Strategy Step** | Step 2 (evidence weakness) / Step 3 (supply missing specification) |

**Evidence:**

ADR-003 §D8 Detector Specification states:

> "a baseline scan of the current `main` retained surface establishes the known-benign set at adoption, so the gate fails only on **net-new** indicators. The allow-list is part of the security-reviewed surface; adding an entry is a reviewed change."

The allow-list mechanism itself is specified: keyed by `{file path + rule id + content hash}`, hash-pinned so an altered line voids the exception.

**Analysis:**

Jerry's retained surface includes `skills/adversary/` (strategy templates for red team, devil's advocate, steelman, FMEA, chain-of-verification), `.context/templates/adversarial/` (all 10 strategy execution templates), and the STRIDE threat model itself. These files contain extensive natural-language discussion of C1–C4 indicator patterns:

- C1 (system override): adversary templates discuss "ignore previous instructions," "act as," role-reversal attacks
- C2 (data exfiltration): STRIDE SC-08 and the D8 spec itself contain imperative verbs co-occurring with URLs in illustrative patterns
- C4 (LLM control tokens): `<\|im_start\|>`, `[INST]`, ChatML markers appear in the detector specification as the patterns to detect

The STRIDE D8 spec notes: "Jerry's own legitimate corpus *discusses* prompt injection (this very threat model, /adversary strategy templates, red-team agent docs)." It names the allow-list as the release valve. What is missing is: **who runs the baseline, on what commit, under what review, and what is the procedure for resolving false-positive blocking findings?**

Without specifying this, two failure modes exist: (a) the baseline is run on a commit that already contains malicious content, making the allow-list silently permissive for that payload; (b) the baseline scan produces hundreds of allow-list entries from legitimate adversary content and the list becomes ungovernable, or the gate is disabled in frustration.

This weakness survives steelman because the allow-list hash-pinning mechanism (which is correctly designed) does not substitute for the bootstrap procedure itself.

**Strengthened version:**

Add to ADR-003 §D8 and to nse-requirements as a new REQ:

> **D8 bootstrap procedure (required once, before first production release):**
> 1. Run the scanner against the current `main` retained surface on a commit verified by ≥2 independent reviewers to contain no injection content.
> 2. Every finding from that scan is a candidate for the allow-list. Each candidate must be reviewed and explicitly accepted by a named security reviewer (not the author of the file containing the pattern).
> 3. The resulting allow-list is code-reviewed as a security artifact and committed to the source repo.
> 4. Subsequent releases: only net-new findings (not present in the allow-list) block the release.
> 5. The initial allow-list commit is tagged with the baseline source-commit SHA so the bootstrap provenance is auditable.

**Recommendation:** ADR-003 §D8 should specify this procedure (ps-architect is the owner for the architectural decision; eng-architect owns the pattern catalog details). nse-requirements should formalize as a REQ. OWNER: ADR → ps-architect; requirements → nse-requirements; pattern catalog → eng-architect.

---

### SM-002-it006: G-update Failure Recovery Path Underdesigned

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Section** | ADR-001 §L2 #6; Phase-5 Validation Gate Set §G-update; requirements §STK-002 |
| **Strategy Step** | Step 2 (structural weakness) / Step 4 (best-case conditions) |

**Evidence:**

ADR-001 §L2 #6:

> "If CoWork caches at install, an alternate update path (or a documented manual-update procedure) is REQUIRED and the 'automatically in sync' claim must be re-scoped."

Phase-5 Validation Gate Set §G-update pass criterion:

> "a force-push to `geekatron/jerry-cowork` reaches an already-installed user's session within a documented window; **OR** a manual update procedure is documented and the 'automatically in sync' claim is re-scoped (PM-001/CV-001)"

The STK-002 stakeholder need is marked:

> "contingent on G-update being verified (REQ-054 / OQ-048); 'automatically in sync' for already-installed users is an UNVERIFIED assumption"

**Analysis:**

The design correctly refuses to assert what it cannot verify (P-022 compliance is good). However, G-update's pass criterion includes an OR branch: "OR a manual update procedure is documented." The design does not pre-specify what that manual procedure would be, who would build it, or how it would be evaluated for adequacy.

At C4, the headline value proposition of the project is STK-002: existing users stay in sync automatically. If G-update fails (CoWork caches at install), the project's core value for the installed user base is absent. The design faces a scope-change decision: pivot to a different distribution mechanism, ship with a manual-update UX, or de-scope to fresh-install-only. None of these is pre-designed.

This survives steelman because: (a) the design correctly acknowledges the uncertainty; but (b) at C4, an undesigned failure path is a gap, not a feature. The orphan-branch fallback (ADR-001) is a good model: it's pre-designed, named, and has a one-line implementation. G-update failure recovery should be similarly pre-designed.

**Strengthened version:**

Add a G-update failure response tree to ADR-001:

> **G-update FAIL response (pre-designed, not improvised at Phase-5):**
> 1. **If CoWork propagates on next launch (not real-time):** re-scope the "automatically in sync" claim to "updates on next CoWork relaunch" — document the lag window; update STK-002 accordingly.
> 2. **If CoWork caches at install with no auto-update:** implement a `jerry update-plugin` CLI command that deletes and reinstalls the plugin from the dedicated repo; document it as the update procedure; re-scope STK-002 to "manually updatable."
> 3. **If neither path is feasible:** escalate to user (H-02/P-020) as a scope change — the project's install-once-update-manually posture changes the project goals.

**Recommendation:** ADR-001 §L2 #6 should add the failure response tree. requirements should convert REQ-054 from a stated assumption to a decision tree with named outcomes. OWNER: ADR → ps-architect; requirements → nse-requirements.

---

### SM-003-it006: No Interim Mitigation for D5 Gap

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Section** | ADR-003 §D5; STRIDE §SC-02; STRIDE Consolidated Threat Register rank 1 |
| **Strategy Step** | Step 2 (structural weakness) / Step 3 (supply missing argument) |

**Evidence:**

STRIDE §SC-02:

> "Status: Designed — operational validation pending [G-provenance]; specified, NOT yet implemented (FM-032) — the rogue-tag path stays OPEN through Phase-5 and **blocks go-live**."

STRIDE Consolidated Threat Register:

> "| 1 | SC-02 | T/R | Rogue-tag CI self-certification | 2×5=10 | Y | **STILL-NEEDED** — provenance (D5 designed-NOT-implemented, FM-032; G-provenance blocks go-live) |"

Attack tree DREAD for AT-1.2: **7.6** (D=9, R=7, E=6, A=9, D=7).

ADR-003 §D5:

> "Both legs (REQ-038 ancestor assertion, REQ-039 v* tag-protection ruleset) are **specified but NOT yet implemented**."

**Analysis:**

D5 (provenance gate) is explicitly designed-but-not-implemented and blocks go-live. DREAD 7.6 is the highest-scored attack path in the register. Between design approval (AG-04) and D5 implementation, every CI run triggered by a push to any `v*` tag (including rogue ones) will faithfully build, faithfully attest (D4 does not distinguish legitimate from rogue tags — it proves the build was faithful, not that the input was legitimate), and ship to all org users.

This is not a theoretical gap. The attack requires only tag-push permission on `geekatron/jerry`, which is a subset of write access. The design does not specify any controls that reduce the rogue-tag risk in the period before D5 is operational.

The orphan-branch fallback in ADR-001 is a useful model: it names the condition that triggers the switch and is pre-designed. D5 needs an equivalent interim posture.

This survives steelman because: D5's designed-but-not-implemented status is correctly disclosed; the honesty is good; but at C4 with DREAD 7.6 and C=5 blast radius (all org users, executable hooks), "we will implement it before Phase-5" is not an interim mitigation. The gap between design approval and D5 operational status is a live risk period.

**Strengthened version:**

Add to ADR-003 §D5:

> **Interim mitigation (D5 pre-operational):** Until G-provenance validates REQ-038 and REQ-039 on the live pipeline, NO automatic `push: tags: v*` trigger is active on `cowork-skeleton.yml`. Skeleton releases are gated behind a `workflow_dispatch` that requires a named approver in a GitHub Actions Environment (`skeleton-push`) restricted to principals who can also authorize the tag. This converts the automated rogue-tag risk from "undetected" to "requires social-engineering a named approver in addition to having tag-push permission." The interim gate is removed once G-provenance passes. Cost: requires one manual approval per release during the implementation window. This is consistent with REQ-045 (GitHub Actions Environment for the push credential).

**Recommendation:** ADR-003 §D5 should specify an interim mitigation binding the `push: tags` automation to a protected environment until D5 is operational. OWNER: ADR → ps-architect; STRIDE → eng-architect (STRIDE mitigation entry for SC-02).

---

### SM-004-it006: R-001 Verification Sequencing Ambiguity

| Attribute | Value |
|-----------|-------|
| **Severity** | Minor |
| **Section** | requirements §Stated Assumption R-001; REQ-034 |
| **Strategy Step** | Step 2 (structural weakness) |

**Evidence:**

requirements §Stated Assumption R-001:

> "A three-dimensional verification (REQ-034) MUST be completed and its machine-checkable artifact committed **BEFORE Phase 2 begins**."

The Phase-2 STRIDE threat model (phase2-stride-threat-model.md) and ADR-003 are both dated 2026-06-28 and reference "~1,417 files" and the `tests/` strip as confirmed. The R-001 verification artifact (`verification/R001-clean-clone-count.md`) is not in scope of this review.

**Analysis:**

The requirements impose a hard sequencing constraint: R-001 verification must precede Phase 2. The Phase-2 artifacts exist and are already incorporating the R-001 assumption (strip = `projects/` and `tests/` → ~1,417 files). It is unclear from the review artifacts whether the R-001 verification was completed and committed before Phase 2 proceeded. If it was not, a Must requirement's precondition was violated.

This is a Minor finding because: (a) the design is honest about R-001 being an assumption; (b) G-headroom (Phase-5 gate) still provides empirical validation before go-live; and (c) it is possible the verification was done but the artifact is simply outside this review's scope. The finding is a traceability gap, not a design flaw.

**Strengthened version:**

The requirements should add a cross-reference: "R-001 verification artifact: `verification/R001-clean-clone-count.md` (status: [CONFIRMED | PENDING])." This makes the sequencing constraint verifiable without reading outside the requirements document.

**Recommendation:** requirements §Stated Assumption R-001 should carry the verification status explicitly. OWNER: requirements → nse-requirements.

---

### SM-005-it006: Org-Registration Recovery SLA Unspecified

| Attribute | Value |
|-----------|-------|
| **Severity** | Minor |
| **Section** | ADR-003 §RTB-3; STRIDE §OR-01 |
| **Strategy Step** | Step 2 (structural weakness) |

**Evidence:**

ADR-003 §RTB-3:

> "REQ-043's 'two-admin approval for any registered-source change' has **no GitHub-native technical enforcement**... the control is **detect-and-respond, not prevent**."
> "an org audit-log webhook (REQ-047) on marketplace-settings changes provides near-real-time drift alerting, paired with a documented ≤ monthly manual verification."

**Analysis:**

RTB-3 is correctly classified as a process control with near-real-time detection (audit-log webhook). The analysis is honest. What is absent is: a recovery SLA (maximum time from detection to remediation) and a tested recovery runbook.

For the D7 tamper path (direct push to dedicated branch), the response is automated (auto-revert via `workflow_dispatch` re-generation of last-good tag, REQ-053). For an org-registration compromise (OR-01), the response is manual: de-register the rogue repo, re-register the canonical one, and notify affected users. While the design acknowledges the process boundary, it does not specify how long users could be exposed to a rogue-registered marketplace between the webhook alert and remediation, nor what the manual steps are.

This is Minor because RTB-3 honestly scopes the limitation. However, for an artifact with executable hooks reaching all org users, a recovery SLA and a documented-and-tested runbook strengthen the architecture's operational completeness.

**Strengthened version:**

Add to ADR-003 §RTB-3 or requirements as a new REQ:

> "A runbook SHALL document: (1) the de-registration and re-registration procedure, (2) a target recovery SLA from webhook alert to remediation (e.g., ≤ 4 h business hours), (3) a procedure for notifying affected org users of the exposure window and required actions (e.g., reinstall or verify plugin source), (4) a ≤ quarterly drill of the runbook to confirm the steps remain accurate."

**Recommendation:** ADR-003 §RTB-3 and STRIDE §OR-01 should reference a named runbook (not just "a runbook should exist"). OWNER: requirements → nse-requirements; STRIDE → eng-architect (OR-01 mitigation note).

---

### SM-006-it006: D7 Freshness Window Unjustified; "Last-Good Tag" Undefined for Auto-Revert

| Attribute | Value |
|-----------|-------|
| **Severity** | Minor |
| **Section** | ADR-003 §D7; requirements REQ-049 / REQ-053 |
| **Strategy Step** | Step 2 (evidence weakness) |

**Evidence:**

ADR-003 §D7:

> "Freshness... the newest source `v*` tag produced a matching dedicated-repo deployment within ≤ **2 h** of its push timestamp."

REQ-053:

> "A D7 monitor integrity/freshness failure SHALL automatically dispatch `workflow_dispatch` re-generation of the **last-good `v*` tag**."

Neither document specifies: (a) the basis for the 2-hour window (vs. 30 min or 4 hours), or (b) how "last-good tag" is determined (latest tag with a passing attestation? latest tag before `vN`? a durably stored value?).

**Analysis:**

The 2-hour freshness window is conservative given that a typical CI run completes in minutes. However, under GitHub Actions queue saturation (documented to occur at popular release times), a legitimate run for `vN` could be queued for >2 hours. In that scenario, the freshness check fires, triggers auto-revert to "last-good" (which is `vN-1`), and `vN-1` gets force-pushed back to the dedicated repo — before `vN`'s legitimate CI run completes. This creates a confused state: the dedicated repo holds `vN-1`, `vN`'s CI eventually completes and force-pushes `vN`, and the auto-revert logic may trigger again.

The "last-good tag" definition matters: if it means "the tag whose attestation the monitor last successfully verified," this value is durably stored where? The monitor needs to persist this across runs. The architecture doesn't specify where this value lives.

These are implementation-level gaps that would be discovered during REQ-049 and REQ-053 implementation, but at C4, discovery during implementation is costly. Specifying them now prevents implementation-time scope creep.

**Strengthened version:**

ADR-003 §D7 should add:

> **Freshness window rationale:** 2 hours accommodates P99 CI queue time observed on GitHub Actions public runners for repositories of Jerry's size (typical run: 5–10 minutes; P99 under saturation: ~60 minutes). 2 hours provides a 2× safety margin. The window SHOULD be revisited after 30 days of operational data.
>
> **"Last-good tag" definition:** the highest semver `v*` tag whose corresponding dedicated-repo deployment has been verified by the monitor within the current monitoring cycle. This value SHALL be persisted as a labeled GitHub release `last-known-good` or in `$GITHUB_STEP_SUMMARY` of the last successful monitor run (the latter is not durable across workflow purge). The source `main` SHALL carry a `last-good-tag` variable in the generation workflow's environment (updated on each successful deployment and pushed as a commit to the source repo if needed, or stored as a GitHub repo variable). nse-requirements SHALL formalize the storage mechanism.
>
> **CI queue saturation false-positive mitigation:** if a freshness check fires while a generation workflow run for the same tag is ACTIVE (in-progress or queued), the monitor SHOULD suppress auto-revert and wait one additional cycle before triggering.

**Recommendation:** ADR-003 §D7 and REQ-049/REQ-053 should specify the window's rationale, the "last-good tag" storage mechanism, and the active-run suppression clause. OWNER: ADR → ps-architect; requirements → nse-requirements.

---

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | **Positive** | SM-001 (D8 bootstrap procedure), SM-002 (G-update failure path), SM-003 (D5 interim mitigation) each fill specification gaps that currently leave implementation teams without guidance at load-bearing decision points |
| Internal Consistency | 0.20 | **Positive** | SM-004 (R-001 sequencing) and SM-006 ("last-good tag" definition) resolve ambiguities where different document sections could be interpreted inconsistently |
| Methodological Rigor | 0.20 | **Positive** | SM-002 and SM-003 strengthen the C4 argument by pre-designing failure paths rather than deferring them to discovery; SM-006 provides a basis for the 2-hour window rather than asserting it without justification |
| Evidence Quality | 0.15 | **Positive** | SM-001 (allow-list bootstrap provenance), SM-006 (window rationale), and SM-004 (R-001 status) each supply specific evidence backing for claims that currently rest on asserted-but-ungrounded values |
| Actionability | 0.15 | **Positive** | SM-002 (G-update failure tree), SM-003 (interim mitigation spec), and SM-005 (recovery SLA) convert ambiguous "a procedure is required" notes into concrete implementable actions |
| Traceability | 0.10 | **Positive** | SM-004 adds explicit cross-reference for the R-001 verification artifact; SM-001 adds a traceability path from the allow-list to the baseline commit |

---

## Execution Statistics

- **Total Findings:** 6
- **Critical:** 0
- **Major:** 3
- **Minor:** 3
- **Protocol Steps Completed:** 6 of 6

---

## Appendix: Steelman — What Makes the Core Thesis Hold

Under the most charitable scrutiny, this design's core thesis holds unconditionally:

1. **The structural cause of the Phase-1 5-strategy Critical is eliminated.** Not patched — eliminated. The architectural separation of the artifact repo from the source repo's write-collaborator surface, with a CI-only-writable attestation, makes the "one key locks two things" failure structurally impossible under the new model.

2. **D8 is the correct response to the payload-semantics gap.** Recognizing that integrity controls cannot see content semantics, and placing a blocking content-safety gate *before* the attestation job (so the attested artifact is exactly the scanned artifact), is architecturally sound. No other approach in the options considered (human review alone, async detection, consumer-side verification) matches D8's combination of blocking posture and correct placement.

3. **The Phase-5 gate set prevents premature go-live on paper designs.** The six-gate AND-pass requirement forces empirical validation of every major security claim before users are exposed. This is the right governance posture for an executable-instructions artifact distributed at org scale.

4. **The Claim-Status Convention is the right epistemic posture at C4.** Refusing to assert achieved what is only designed is not excessive hedging — it is accurate representation of a system that does not yet exist. Under steelman scrutiny, this honesty is a strength, not a weakness.

The 3 Major findings (SM-001, SM-002, SM-003) are specification completeness gaps in well-designed controls. They do not invalidate the controls; they leave the controls' implementation exposed to foreseeable problems at implementation time. Addressing them before the Devil's Advocate and Pre-Mortem strategies engage makes those strategies target residual genuine risks, not easily-fixable specification gaps.

---

*Strategy: S-003 (Steelman Technique)*
*Template: .context/templates/adversarial/s-003-steelman.md*
*Deliverables reviewed: ADR-001, ADR-003, phase1-requirements.md, phase2-stride-threat-model.md, phase2-attack-surface.md (historical recon input, pre-decision)*
*Execution ID: it006*
*H-15 Self-Review: Applied — findings have specific evidence; severity classifications meet SM template Step 5 definitions; identifiers follow SM-NNN-it006 format; summary table matches detailed findings; P-022 complied with (0 Critical findings is honest — the core thesis holds)*
