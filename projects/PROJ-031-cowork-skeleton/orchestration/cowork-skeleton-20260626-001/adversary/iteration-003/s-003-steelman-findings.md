# Strategy Execution Report: S-003 Steelman Technique — Iteration 3

## Document Sections

| Section | Purpose |
|---------|---------|
| [Execution Context](#execution-context) | Strategy, template, deliverables, timestamp |
| [Core Thesis Summary](#core-thesis-summary) | Brief characterization of what the deliverables argue |
| [Steelman Reconstruction](#steelman-reconstruction) | The strongest, most charitable form of the design argument |
| [Best Case Scenario](#best-case-scenario) | Conditions under which the argument is most compelling |
| [Findings Summary](#findings-summary) | SM-NNN findings table (severity, target, one-line description) |
| [Detailed Findings](#detailed-findings) | Evidence, analysis, and recommendations per finding |
| [Execution Statistics](#execution-statistics) | Counts and protocol completion |

---

## Execution Context

| Field | Value |
|-------|-------|
| **Strategy** | S-003 — Steelman Technique |
| **Template** | `.context/templates/adversarial/s-003-steelman.md` v1.0.0 |
| **Finding Prefix** | SM-NNN (per template Identity section) |
| **Deliverable 1** | `projects/PROJ-031-cowork-skeleton/requirements/phase1-requirements.md` |
| **Deliverable 2** | `projects/PROJ-031-cowork-skeleton/decisions/ADR-001-skeleton-derived-branch-strategy.md` |
| **Deliverable 3** | `projects/PROJ-031-cowork-skeleton/decisions/ADR-002-ci-token-push-strategy.md` |
| **Grounding** | `projects/PROJ-031-cowork-skeleton/research/phase1-skeleton-ci-research.md` (not read — blind) |
| **Executed** | 2026-06-26 |
| **Iteration** | QG-1 Iteration 3 — Group B (Strengthen) |
| **Blindness** | Prior iteration adversary directories NOT read (contamination prevention) |

---

## Core Thesis Summary

The deliverables jointly argue: Jerry cannot install as a Claude CoWork plugin because the repository's ~6,344 tracked files exceed CoWork's ~5,000-file ceiling. The right fix is a CI-regenerated `cowork-skeleton` branch equal to `main` minus `projects/` plus a minimal sentinel stub. The generation is deterministic (same release in → bit-identical commit out), the push credential is `GITHUB_TOKEN` with `contents: write` only, loop-safety is overdetermined by three independent guarantees, and tamper-evidence is provided not by commit signing but by the mathematical property that the deterministic tip SHA is independently recomputable on a non-forgeable value. Security is detection-bounded rather than prevention-based, with a stated ≤ daily SLA, event-driven fast-path, and a documented upgrade to prevention (branch-protection ruleset with Actions bypass actor) for future STRIDE re-assessment.

---

## Steelman Reconstruction

The strongest form of this design argument is as follows.

**The decisive framing eliminates an entire option family with a single empirical observation.** A Claude Code plugin install materializes the *tip working tree* of a branch into a local cache; git history is never checked out. Therefore, whether `projects/` exists in any historical commit is completely irrelevant to the installed file count. This single, code-grounded fact (confirmed in `FilesystemProjectAdapter.scan_projects` line behavior) does not merely prefer Option A over Option C — it removes the entire premise on which history-rewriting approaches (git-filter-repo, subtree split) rest. Option C is not just suboptimal; it solves a problem that does not exist for this use case, and does so slowly, non-idempotently, and with external tooling. The design is cleanest when this is stated as an eliminative argument, not a preference.

**The GITHUB_TOKEN non-retrigger property does double duty, and this is an architectural economy.** A single design choice — using `GITHUB_TOKEN` as the push credential — simultaneously: (a) shrinks the blast radius (repo-scoped, job-expiring), (b) provides the third and strongest leg of the loop-safety conjunction (pushes cannot re-trigger any workflow), and (c) makes the event-driven tamper-detection monitor possible without a false-positive problem. The monitor fires on `on: push: branches: [cowork-skeleton]`; because CI uses `GITHUB_TOKEN` to regenerate the branch, that push does NOT fire the monitor — meaning the monitor's events are exclusively non-CI direct pushes (the exact tamper surface). A PAT or App token would re-trigger the monitor on every CI regeneration, creating a false-positive loop. The `GITHUB_TOKEN` choice is therefore not merely a security preference but the enabling primitive for a near-real-time tamper-detection architecture. No alternative credential enables this combination.

**Determinism yields non-forgeable integrity evidence without requiring commit signing.** The design deliberately omits GPG signing (which would vary per run and break the bit-identical SHA). Instead, tamper-evidence rests on the mathematical property that `regenerate(T)` is a pure function of the release tag `T`: any attacker who modifies the published branch changes the tip SHA, and anyone can independently recompute the expected SHA by re-running the generator against the same tag. To make a tampered tree present the expected SHA requires a SHA-256 preimage collision — computationally infeasible. This is provably stronger than a signed statement from a single actor, because it does not depend on key management, key custody, or signature verification infrastructure. The binary distinction between the *forgeable* `Source-Commit:` trailer (free-form text) and the *non-forgeable* tip SHA is a clean cryptographic principle applied at the operational level.

**The three-guarantee loop-safety conjunction is mathematically overdetermined.** (1) Trigger shape: the workflow listens on `v*` tags; its output is a branch name. (2) Listener shape: no existing workflow listens on `cowork-skeleton` branches. (3) Credential shape: `GITHUB_TOKEN` pushes cannot re-trigger workflows. Each guarantee independently prevents a loop. A single misconfiguration of any one guarantee would still be blocked by the other two. For a C4 irreversibility review, this overdetermination is the correct design: it provides defense-in-depth against configuration drift without requiring all three to hold simultaneously for the constraint to remain satisfied.

**The R-001 verification protocol is a falsification framework, not just a checklist.** The four-dimensional gate (file count, pack size, clone time, CoWork smoke test) is structured to cover every plausible interpretation of what "the ~5,000-file limit" means: if the limit is file-count-based, dimension (a) detects it; if size-based, dimension (b); if time-based, dimension (c); if expressed in the actual CoWork runtime, dimension (d). The design is honest that the limit is undocumented and that any single proxy measurement could falsely pass while a different mechanism is the real constraint. This is scientific methodology applied to an underdocumented external dependency.

**The Option B orphan flip is pre-designed and integrity-neutral post-IT3-004.** A common objection to choosing Option A (full provenance, growing clone weight) over Option B (O(1) orphan, no parent chain) is that switching later is complex or security-regressive. Both objections are false. The implementation change is a single-line substitution (`git checkout --orphan` instead of branch-from-tag). And after IT3-004, integrity does not depend on the parent chain — it rests on the deterministic tip SHA, which an orphan commit also has. The flip is therefore a pure performance optimization with no security regression, pre-designed as an early-warning-band-triggered mechanism.

**The design reuses an existing operational pattern, shrinking reviewer surface.** `cowork-skeleton` is the third CI-owned derived branch in the repository alongside `gh-pages` (force-pushed by `docs.yml`) and the tag-driven release artifact flow. The same bot identity, force-push semantics, `GITHUB_TOKEN` credential, `concurrency` guard, and `if: always()` job-summary pattern are already in production. A C4 reviewer's incremental risk surface is small: the only genuinely new element is the deterministic-commit metadata pinning — and this is explicitly documented with a pseudocode proof and failure modes listed.

---

## Best Case Scenario

This design is most compelling when:

1. The ~5,000-file limit is confirmed to apply to the tracked-file count of a clean clone (R-001 dimension a passes), rendering the ~1,744-file skeleton straightforwardly installable.
2. The current pack size baseline is well under 150 MB, giving 15–40+ releases of headroom before the early-warning band activates.
3. Phase-2 STRIDE analysis confirms that the ≤ daily tamper-detection SLA is acceptable given the hook-blast-radius consequence rating (R-007b C=4; upgrade to prevention deferred).
4. The CoWork plugin-install smoke test (R-001 dimension d) succeeds and validates the decisive framing empirically in a live CoWork client.

Under these conditions, the design is auditable, minimal in tooling, operationally proven (via `gh-pages` precedent), and mathematically tamper-evident — a complete C4-quality supply-chain architecture for a plugin distribution derived branch.

---

## Findings Summary

| ID | Severity | Finding | Section |
|----|----------|---------|---------|
| SM-001 | Major | "Decisive framing" argument is the backbone of the design but is buried mid-context rather than front-loaded as the eliminating premise for Option C | ADR-001 §Options Considered / §Decisive Framing |
| SM-002 | Major | GITHUB_TOKEN "double duty" (loop-safety + tamper-detection enabler) is mentioned but not named as an explicit architectural economy in the decision rationale | ADR-002 §Decision / §Loop-Safety |
| SM-003 | Major | R-001 four-dimensional verification is a falsification protocol but is framed only as a verification checklist; the falsification framing is a stronger C4 argument | Requirements §Stated Assumption R-001 / REQ-034 |
| SM-004 | Minor | Option B orphan flip's one-line implementation cost and integrity-neutrality post-IT3-004 are understated in the Consequences and Clone-Weight Decision sections | ADR-001 §Clone-Weight Decision / §Consequences |
| SM-005 | Minor | Forgeable-vs-non-forgeable binary is introduced but not stated as a generalizable principle for integrity comparator selection | ADR-001 §Tamper-Evidence; ADR-002 §Continuous Integrity Monitoring |
| SM-006 | Minor | ADR-001 c-003 SSOT ownership pattern (one authoritative list → one mirror) is not articulated as a forward-looking maintainability architecture principle | ADR-001 §Canonical Plugin-Retention Surface |
| SM-007 | Minor | Phase-2 deferred items are labeled "deferred to Phase 2" without foregrounding that the gate is STRIDE-driven, making deferrals appear time-based rather than risk-informed | Requirements §Phase 2 Deferred Items; ADR-002 §Compensating Controls |
| SM-008 | Minor | `gh-pages` precedent reuse is framed as operational familiarity; stronger framing is a security argument about reviewer cognitive burden, incremental risk surface, and production track record | ADR-001 §L2 / ADR-002 §L2 |

---

## Detailed Findings

### SM-001: "Decisive Framing" Argument Buried Mid-Context

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Section** | ADR-001 §Context — Decisive Framing; §Options Considered |
| **Strategy Step** | Step 2 (Identify Weaknesses in Presentation) — Structural |

**Evidence:**

ADR-001 places the "Decisive Framing" in the Context section, after the executive summary. The executive summary says "We reject the history-rewriting alternatives" and names the reason inline, but the formal eliminative argument appears mid-document:

> "A Claude Code plugin install **clones the branch and materializes its working tree at the tip commit**, then copies that tree to a cache [...] Therefore the only thing that affects the installed file count is **the tree at the branch tip** — not whether `projects/` ever existed in history [...] This single fact removes any reason to rewrite history and is the spine of the decision below."

Option C is then presented, steelmanned, and rejected — but a reader must work through the Options Considered table before encountering the Options Comparison table which lists "Non-idempotent" as Option C's disqualifier. The structure presents elimination of Option C as a *consequence* of criteria scoring rather than as a logical *premise* that makes Option C's evaluation unnecessary.

**Analysis:**

The decisive framing is the strongest claim in the document: it converts the decision from "which option scores best" to "which options are even applicable." This is categorically different reasoning. When the decisive framing is treated as context rather than as a deductive premise, it can be read as one data point among many rather than as the argument that makes Option C's analysis a foregone conclusion. For C4 review, the logical structure matters: the reviewer should see that Option C is not merely disfavored but is the wrong tool for a problem that does not exist — and this conclusion should be available in the first paragraph that mentions Option C.

**Recommendation:**

Add a one-paragraph "Eliminating Premise" sub-section immediately before the Options Considered section (or at the start of Options Considered), stating explicitly: "The decisive framing establishes that CoWork materializes only the tip working tree. This is an *eliminating* premise for Option C: history rewriting addresses a problem (projects/ in historical commits affecting installed count) that does not exist for this installation model. Option C is presented below for completeness but is logically eliminated before scoring begins." This restructuring is a presentation change, not a content change.

---

### SM-002: GITHUB_TOKEN "Double Duty" Not Named as Architectural Economy

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Section** | ADR-002 §Decision; §Loop-Safety Argument; §L2 Architectural Implications |
| **Strategy Step** | Step 2 (Identify Weaknesses in Presentation) — Structural |

**Evidence:**

ADR-002 §L2 item 6 does note: "The architecture deliberately exploits the `GITHUB_TOKEN` non-retrigger property twice — once for loop-safety, once to make a direct-push tamper trip a near-real-time monitor that CI's own pushes do not." However, this appears in L2 (Architectural Implications) rather than in the Decision or Rationale sections. The Decision section names loop-safety as a benefit of Option A but does not connect it to tamper-detection. The Loop-Safety Argument section establishes the three-guarantee conjunction but does not discuss the monitor. A reader scanning the Decision and Rationale sections sees "free loop-safety" and "Option A dominates" without the additional payoff that the same property enables the monitor architecture.

**Analysis:**

The non-retrigger property doing double duty is an unusually economical design choice: one property (GITHUB_TOKEN pushes cannot re-trigger workflows) simultaneously delivers (a) loop-safety guarantee #3 and (b) the false-positive-free event-driven monitor. No alternative credential supports both. A PAT or App token would enable downstream triggering — which means the event-driven monitor (`on: push: branches: [cowork-skeleton]`) would fire on every CI regeneration, producing a false-positive loop. The `GITHUB_TOKEN` choice is therefore not just "cheapest safe credential" but the *only* standard credential that enables the complete monitoring architecture described in ADR-002. This reframing significantly strengthens the rationale for rejecting the PAT: Option B (PAT) doesn't just add maintenance cost — it makes the near-real-time tamper-detection architecture non-viable.

**Recommendation:**

In ADR-002 §Rationale (or as a bolded callout within §Decision), add: "The `GITHUB_TOKEN` non-retrigger property does architectural double duty: it is simultaneously the third leg of the loop-safety conjunction and the enabling primitive for the event-driven tamper-detection monitor. A PAT or App token would re-trigger the monitor on every CI regeneration push, creating a false-positive loop. The credential choice and the monitoring architecture are therefore not independent decisions — `GITHUB_TOKEN` is the only standard credential that supports both requirements simultaneously." This directly strengthens the PAT rejection argument.

---

### SM-003: R-001 Verification Is a Falsification Protocol, Framed as Checklist

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Section** | Requirements §Stated Assumption R-001; REQ-034 |
| **Strategy Step** | Step 2 (Identify Weaknesses in Presentation) — Evidence |

**Evidence:**

The R-001 assumption section and REQ-034 present a four-dimensional verification:
- (a) tracked file count on a clean clone
- (b) compressed pack size in MB
- (c) estimated clone time in seconds
- (d) direct CoWork plugin-install smoke test

The rationale for each dimension is provided, and the section notes that "the limit could be size- or time-based rather than file-count-based." However, the framing is "verify that the strategy works" — a multi-dimensional checklist. What is not explicitly stated is that the four dimensions are structurally designed to cover all plausible interpretations of what "the ~5,000-file CoWork limit" could mean, such that if the real limit mechanism is any one of these, the test will catch it.

**Analysis:**

This is actually a falsification protocol in the Popperian sense: the design identifies four distinct causal mechanisms by which the underdocumented limit could operate, constructs one test per mechanism, and requires all four tests to pass before Phase 5. A design reviewer who understands this framing recognizes that the protocol is not conservative over-testing but a minimum necessary coverage of an epistemically uncertain constraint. The current framing leaves open the reading that the dimensions are "just to be thorough." The falsification framing closes this gap: each dimension is logically necessary because the others do not cover it. For example, a repository with 1,500 files but a 500 MB pack size would pass dimension (a) and fail dimension (b); the file count alone cannot certify the strategy.

**Recommendation:**

Add a sentence to the R-001 §Verification Approach (and to REQ-034 rationale) stating: "The four dimensions are not redundant belt-and-suspenders; they are structurally independent tests for mutually exclusive limit mechanisms. A file-count-only test cannot detect a size-based or time-based limit. A pack-size test cannot detect a file-count-based limit. Dimension (d) is the only falsification test for the decisive framing itself: it empirically validates that CoWork materializes the tip working tree rather than counting some other artifact. All four must pass because each is the only test for its hypothesis." This framing also strengthens the argument that dimension (d) deferred-to-Phase-4 is acceptable: the other three are proxy falsifications; dimension (d) is the direct test.

---

### SM-004: Option B Orphan Flip's Cheapness and Integrity-Neutrality Are Understated

| Attribute | Value |
|-----------|-------|
| **Severity** | Minor |
| **Section** | ADR-001 §Clone-Weight Decision; §Consequences Negative #1 |
| **Strategy Step** | Step 2 (Identify Weaknesses in Presentation) — Evidence |

**Evidence:**

ADR-001 §Clone-Weight Decision says: "switch to Option B is a one-line change (`git checkout --orphan` instead of branch-from-tag); integrity-neutral post-IT3-004." The Consequences Negative #1 says: "Mitigation [...] Flip to Option B [...] constant-weight orphan becomes the new default." The Options B row in the comparison table shows Idempotency "(pinned)" and notes it requires the same pinning discipline.

**Analysis:**

The document correctly states that the orphan flip is one-line and integrity-neutral. However, these facts appear embedded in the mitigation discussion for a negative consequence, which frames Option B as a fallback for a risk. The stronger framing for S-003 purposes is: the design's positive attribute is that it does not require a *redesign* when the clone-weight warning band is breached — it requires a *configuration change*. This is architecturally significant: the entire Consequences Negative section for clone weight is actually a well-controlled risk because the escape hatch is cheap, pre-designed, and non-regressive. The deliverables could foreground this in the Positive Consequences as well, stating explicitly: "The Option B flip is a pre-designed, one-line, integrity-neutral escape hatch — not a future redesign — making the Option A choice low-commitment."

**Recommendation:**

Add to ADR-001 §Consequences Positive, or §Decision, a sentence explicitly naming the low-commitment nature of Option A: "The Option A choice is low-commitment: the pre-designed Option B flip requires exactly one implementation change (`git checkout --orphan` instead of branch-from-tag), carries no integrity regression (tamper-evidence rests on the recomputable SHA, not the parent chain), and is triggered by a quantitative threshold (150 MB early-warning band, 250 MB hard trigger) rather than a judgment call. The cost of being wrong about Option A is exactly one line of bash."

---

### SM-005: Forgeable-vs-Non-Forgeable Binary Not Stated as a Generalizable Principle

| Attribute | Value |
|-----------|-------|
| **Severity** | Minor |
| **Section** | ADR-001 §Tamper-Evidence; ADR-002 §Continuous Integrity Monitoring |
| **Strategy Step** | Step 2 (Identify Weaknesses in Presentation) — Structural |

**Evidence:**

ADR-001 §Tamper-Evidence and ADR-002 §Continuous Integrity Monitoring both introduce the distinction between the forgeable `Source-Commit:` trailer and the non-forgeable tip SHA:

> "The assert MUST NOT use the `Source-Commit:` trailer: that is free-form commit-message text any push actor can set to the correct value while shipping a different tree (forgeable). [...] Every assert compares `git rev-parse cowork-skeleton` (the live tip SHA; equivalently the tip tree hash) against the independently-recomputed/published expected SHA. The tip SHA is non-forgeable..."

**Analysis:**

This is a correct and important insight. However, it is stated as an observation specific to this design. The underlying principle generalizes: when designing integrity monitors, the comparator must be non-forgeable — i.e., a value that the attacker cannot reproduce independently of the actual content they ship. Commit message fields (trailers, subjects, author names) are always forgeable by any push actor. Cryptographic hashes of actual content (tip SHA, tree SHA) are non-forgeable without a preimage collision. Stating this as a *principle* applied to this design, rather than as an observation about two specific fields, would (a) better justify why this is the right choice, (b) help reviewers identify if future monitoring designs accidentally use forgeable comparators, and (c) provide a quotable standard for the Phase-2 STRIDE review.

**Recommendation:**

Add a one-sentence principle statement in ADR-001 §Tamper-Evidence or ADR-002 §Continuous Integrity Monitoring: "**Integrity comparator selection principle:** any value a push actor can compute or set independently of the actual content they ship is forgeable and MUST NOT be the sole integrity comparator. Only values that are derived from the committed content by a cryptographic function the attacker cannot invert (such as the tip SHA, the tree hash) qualify as non-forgeable comparators." Then state that the design applies this principle by choosing `git rev-parse cowork-skeleton` over the `Source-Commit:` trailer.

---

### SM-006: c-003 SSOT Ownership Pattern Not Articulated as a Maintainability Architecture Principle

| Attribute | Value |
|-----------|-------|
| **Severity** | Minor |
| **Section** | ADR-001 §Canonical Plugin-Retention Surface |
| **Strategy Step** | Step 2 (Identify Weaknesses in Presentation) — Structural |

**Evidence:**

ADR-001 §Canonical Plugin-Retention Surface opens:

> "*(Authoritative list for c-003. REM-008 reconciliation — this ADR OWNS the list; the requirements' REQ-005 mirrors it verbatim.)*"

And the requirements' REQ-005 states: "REQ-005 defers to ADR-001 c-003 [...] REQ-005 and ADR-001 c-003 must be kept in sync; changes to the surface list require updating both documents."

**Analysis:**

The design correctly identifies a single source of truth (ADR-001 c-003) with a single downstream mirror (REQ-005). This resolves the iteration-1 inconsistency (different directory lists in the two documents). However, the value of this pattern is understated: when new plugin functionality is added requiring a new directory in the retention surface, a developer knows exactly where to update (ADR-001 c-003) and exactly where the mirror lives (REQ-005 text). There is no list-of-lists to track down. This is a forward-looking maintainability architecture decision, not just a consistency fix. Articulating it as such would help future maintainers understand why the SSOT pattern exists and prevent them from adding a third list elsewhere.

**Recommendation:**

Add a note to ADR-001 §Canonical Plugin-Retention Surface: "**Maintainability pattern:** this document (ADR-001) owns the canonical retention surface list; all other documents (REQ-005, generation script assertions, CI validation) MUST mirror it, not define their own list. Any future addition to the retention surface (e.g., a new top-level directory required by a new plugin capability) MUST update ADR-001 c-003 first; downstream documents update in consequence. This single-SSOT pattern prevents the divergence found in iteration-1 from recurring."

---

### SM-007: Phase-2 Deferred Items Framed as Time-Based Rather Than STRIDE-Gated

| Attribute | Value |
|-----------|-------|
| **Severity** | Minor |
| **Section** | Requirements §Phase 2 Deferred Items; ADR-002 §Compensating Controls |
| **Strategy Step** | Step 2 (Identify Weaknesses in Presentation) — Structural |

**Evidence:**

Requirements §Phase 2 Deferred Items lists four items (auto-revert automation, tag-on-main provenance assertion, detection-to-prevention escalation, R-007b consequence re-rating) with "Rationale for Deferral" citing either "requires STRIDE threat model" or "architectural decision needed before implementing write-to-main automation." ADR-002 §Compensating Controls table marks the same items "deferred to Phase 2 (STRIDE / STORY-004/005, P-042/AE-005)."

**Analysis:**

The rationale mentions STRIDE in parentheses or in dependent clauses. But the operative framing in the table header ("Rationale for Deferral") does not lead with "STRIDE-gated." A C4 reviewer could read the deferred items as "things we didn't have time for in Phase 1." The stronger and accurate framing is that these items are *gated by a preceding analysis* (STRIDE threat model) whose outputs are required inputs to the deferred decisions. You cannot safely design auto-revert without knowing the threat actors and trust boundary assumptions that STRIDE will surface. This is governance-informed scope control, not time-boxing — and saying so explicitly defends the deferral against the critique that Phase 1 left security gaps.

**Recommendation:**

Add a preamble sentence to Requirements §Phase 2 Deferred Items: "The items below are not deferred because of resource constraints. Each item requires the output of the Phase-2 STRIDE threat model as a prerequisite input before a safe design decision can be made. Implementing any of these items before STRIDE completion would require security assumptions to be made implicitly that the threat model is designed to make explicit." Similarly, update the ADR-002 §Compensating Controls Phase-2 placeholder row to say "STRIDE-gated (requires threat model output as design input)" rather than just "deferred to Phase 2."

---

### SM-008: gh-pages Precedent Reuse Framed as Familiarity, Not as a Security Argument

| Attribute | Value |
|-----------|-------|
| **Severity** | Minor |
| **Section** | ADR-001 §L2 Architectural Implications item 1; ADR-002 §L2 item 5 |
| **Strategy Step** | Step 2 (Identify Weaknesses in Presentation) — Evidence |

**Evidence:**

ADR-001 §L2 item 1: "The skeleton joins an established operational pattern, minimizing novel risk. `gh-pages` and the `release.yml` artifact flow already exercise force-pushed / tag-driven derived outputs. Adopting the same conventions [...] keeps the C4 reviewer surface small and reuses battle-tested behavior."

ADR-002 §L2 item 5: "Posture parity with `gh-pages` minimizes novel risk. Treating `cowork-skeleton` as another unprotected, CI-owned derivative reuses an operational model already trusted in the repo, shrinking reviewer surface."

**Analysis:**

The deliverables note "minimizing novel risk" and "small reviewer surface." This is the right conclusion, but the argument leading to it is weak: "reuses battle-tested behavior" describes familiarity, not a formal security property. The stronger argument is: (1) any security flaw in the `cowork-skeleton` CI mechanism would also need to exist in the `gh-pages` CI mechanism, since they are structurally identical — the incremental security risk of adding `cowork-skeleton` is therefore bounded by the incremental difference from `gh-pages`, which is only the deterministic-commit metadata; (2) the `gh-pages` pattern has an operational track record in this repository with no known security incidents; (3) a C4 reviewer evaluating `cowork-skeleton` security does not need to assess the entire pattern from first principles — only the delta, which is small and explicitly documented. This is a formal incremental risk argument, not just "we've done this before."

**Recommendation:**

Strengthen the `gh-pages` precedent argument in ADR-001 §L2 and ADR-002 §L2: "**Security argument for pattern reuse:** the only novel element in `cowork-skeleton` relative to the `gh-pages` mechanism is the deterministic-commit metadata pinning (pinned dates, parent, 40-char SHA) and the SHA-publish step. Every other element — `GITHUB_TOKEN` credential, `permissions: contents: write`, force-push semantics, `github-actions[bot]` identity, `concurrency` guard — is already operating in production via `docs.yml` without a known security incident. A C4 reviewer's incremental risk surface is therefore exactly the two novel elements, both of which are explicitly documented and formally analyzed in this ADR. Pattern reuse is a security argument about bounded incremental risk, not merely an ergonomics choice."

---

## Execution Statistics

| Metric | Value |
|--------|-------|
| **Total Findings** | 8 |
| **Critical** | 0 |
| **Major** | 3 (SM-001, SM-002, SM-003) |
| **Minor** | 5 (SM-004 through SM-008) |
| **Protocol Steps Completed** | 6 of 6 |
| **H-15 Self-Review Applied** | Yes |

### Self-Review Checklist (H-15)

- [x] All findings have specific evidence quoted from the deliverable
- [x] No Critical findings — justified: all core arguments are sound; the three Major findings are presentation/structural gaps, not substantive flaws
- [x] Severity classifications meet the template's definitions (Major = materially improves quality; Minor = polish)
- [x] Finding identifiers follow the SM-NNN prefix format from the template
- [x] Summary table matches the 8 detailed findings
- [x] No findings omitted or minimized (P-022)
- [x] No deliverable files were read from prior adversary iteration directories (blindness maintained)

---

*Executed by:* jerry:adv-executor
*Strategy:* S-003 Steelman Technique (template v1.0.0)
*Iteration:* QG-1 Iteration 3 — Group B (Strengthen)
*Date:* 2026-06-26
*Constitutional compliance:* P-001 (evidence-based), P-002 (persisted), P-003 (no subagents), P-004 (provenance), P-011 (evidence per finding), P-022 (honest severity)
