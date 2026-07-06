# Inversion Report: ADR-PROJ031-004 + Companion Rule Draft (Iteration 6, Post-Subtraction)

**Strategy:** S-013 Inversion Technique
**Deliverable:** `projects/PROJ-031-cowork-skeleton/decisions/ADR-PROJ031-004-adr-identifier-convention.md` + `projects/PROJ-031-cowork-skeleton/design/adr-standards-rule-draft.md`
**Criticality:** C4 (engagement gate 0.95)
**Date:** 2026-07-05
**Reviewer:** adv-executor (blind, independent iteration-6 reviewer)
**H-16 Compliance:** S-003 Steelman applied per the deliverable's own self-report (embedded steelmans in Options A-F, ADR:65-68); not independently re-verified -- blind protocol precludes reading `adversary/` except this file.
**Goals Analyzed:** 7 | **Assumptions Mapped:** 6 | **Vulnerable Assumptions:** 4 (1 Critical, 2 Major, 1 Minor)

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Overall assessment and recommendation |
| [Goal Inventory](#goal-inventory) | Explicit and implicit goals stated in measurable terms |
| [Anti-Goal Analysis](#anti-goal-analysis) | "What would guarantee failure?" -- checked against the package as-is |
| [Assumption Map](#assumption-map) | Explicit/implicit assumptions, confidence, validation status |
| [Findings Table](#findings-table) | Classified findings |
| [Finding Details](#finding-details) | Expanded findings with evidence and mitigations |
| [Null-Alternative Check](#null-alternative-check) | Direct answer to "does it still beat doing nothing?" |
| [Recommendations](#recommendations) | Prioritized mitigations |
| [Scoring Impact](#scoring-impact) | Mapping to S-014 dimensions |

---

## Summary

Applying Inversion to the post-subtraction package (iteration 6): the *design decision itself* (Scheme B, subject-encoded identity, MEDIUM-tier, grandfathered legacy) survives inversion cleanly -- the anti-goals for the naming/promotion mechanics are already addressed, and the subtraction pass's honest residual disclosures (R-A/R-B/R-C, Claim-Status "designed-not-built") pre-empt most of what an inversion pass would otherwise surface. This reviewer independently corroborates one of those residuals with a filesystem check (`.context/rules/adr-standards.md` does not exist -- confirmed by Glob) and finds it under-disclosed at the point where it matters most: the **Status** section's present-tense claim that the convention "is now in force... and delivers value with zero tooling." That claim is the load-bearing premise of the entire post-subtraction enforcement story (guidance-first, lint-second), and it is not yet true in the one sense a reader would check first -- the guidance is not yet living where any session would see it, and there is no tracked forcing function (Task, GH Issue, deadline) that guarantees it ever will be. This is the one new, non-redundant, evidence-backed Critical finding this iteration surfaces (IN-001); the remaining findings (IN-002 through IN-004) are lower-severity corollaries and a genuine H-32 compliance gap in the Migration Plan not previously disclosed. **Recommendation: REVISE (targeted, single-section fix) -- not REJECT.** The scheme still beats the null alternative once this gap is closed to an honest "not yet realized" disclosure; it does not yet beat the null alternative in the narrow, literal, present-tense sense the Status section currently implies.

---

## Goal Inventory

| # | Goal (as stated/inferred) | Measurable form |
|---|---|---|
| G1 | Promotion (project -> framework) does not break citations | Path-1 `git mv` preserves ID with zero ID-string churn for canonical ADRs |
| G2 | Stay MEDIUM-tier; no new HARD rule | Zero new entries in the 25/25 HARD Rule Index; enforcement via override-with-justification |
| G3 | No big-bang renumbering of legacy ADRs | 16-file dialect corpus grandfathered in place (c-003) |
| G4 | Deliver real guidance value *immediately*, before the lint is built | Guidance auto-loads via the `.claude/rules -> ../.context/rules` symlink and is actually followed by ADR-authoring humans/agents |
| G5 | Beat the "do nothing / index-and-search" null alternative | Demonstrate net present value over no convention, not just eventual value |
| G6 | Model self-compliance | This ADR itself executes its own Path-2 self-promotion (M-9) |
| G7 | Governance parity in the Jerry repo | Migration Plan work items comply with H-32 GitHub Issue parity |

---

## Anti-Goal Analysis

*"What would guarantee this fails?"* -- checked against the package as it now stands.

| Anti-goal (guaranteed-failure condition) | Present in the package? | Evidence |
|---|---|---|
| Sneak "non-bypassable"/HARD-tier language into a MEDIUM standard | **No** -- explicitly removed | ADR:619 "there is **no** waiver ledger, no CODEOWNERS gate, and no 'non-bypassable' rule"; rule-draft:165 same |
| Silently renumber grandfathered legacy ADRs | **No** | ADR D-4 (:223), Migration Plan (:485) "Grandfather in place... Zero" cost |
| Overclaim the lint as built/fail-closed today | **No** -- honestly labeled | ADR:621 Claim-Status block; rule-draft:163 same |
| **Publish present-tense "in force / delivers value" language while the guidance file has not actually been moved to where it takes effect, and no tracked task forces the move** | **YES -- present** | See [IN-001](#in-001-status-claims-present-tense-in-force-value-that-is-not-yet-structurally-true-critical) |
| Apply a HARD constitutional rule (H-32) inconsistently across a work-item plan in the very repo it governs | **YES -- present** | See [IN-003](#in-003-h-32-github-issue-parity-applied-inconsistently-across-the-migration-plan-major) |
| Leave a load-bearing empirical belief (promotion-frequency, n=3) to informally "revisit itself" with no tracked trigger | **YES -- present, but explicitly disclosed as an open residual (PM-009), not hidden** | See [IN-004](#in-004-pm-009-re-examination-commitment-has-no-tracked-trigger-minor) |

---

## Assumption Map

| ID | Assumption | Type | Confidence | Validation status | Consequence if wrong |
|----|---|---|---|---|---|
| AS-1 | On the M-2 file move, the rule content auto-loads via the `.claude/rules -> ../.context/rules` directory symlink | Technical (explicit, rule-draft:1-4) | High (mechanism is structurally verified elsewhere in the repo) | **Not yet exercised** -- Glob-verified `.context/rules/adr-standards.md` does not exist | Guidance remains invisible to every session except one that manually opens this project's `design/` folder |
| AS-2 | M-2 (guidance publication), M-9 (self-promotion), M-12 (producer-agent fix) will happen in a timely manner because they are marked "Gating: Yes" | Process (implicit) | Low | **Contradicted** -- ADR's own Claim-Status (:497) discloses zero worktracker Tasks and zero GH Issues exist for *any* Migration-Plan row; independently confirmed by Glob over `projects/PROJ-031-cowork-skeleton/work/` (no ADR-convention-related entities present) | Convention stays permanently in "ratified-on-paper" limbo; no forcing function exists |
| AS-3 | H-32 GitHub Issue parity is correctly scoped as applying only to 3 of the 14 Migration-Plan rows (the ones explicitly tagged) | Process/Governance (implicit) | Low | Not reconciled against H-32's stated scope (applies to "jerry repo work items" generally, no stated carve-out) | Task entities created for the other 11 rows would be created non-compliant with a HARD rule on day one |
| AS-4 | The current (pre-M-2/M-6/M-12) state of the package already delivers materially more real value than the null alternative, matching the Status section's present-tense framing | Environmental (implicit) | Medium | Partially true (design/intent) but overstated for *present* state | Reader over-trusts "ratified = operative" and treats the convention as already governing sessions it does not yet reach |
| AS-5 | A solo maintainer (single CODEOWNERS, per the subtraction pass's own removed-machinery rationale) has bandwidth to execute all 14 untracked TBD-Task migration items without formal prioritization | Resource (implicit) | Low | Not validated; same single-maintainer bandwidth caveat is explicitly conceded elsewhere for M-5b | Untracked items compete invisibly with all other backlog items and may never surface |
| AS-6 | The PM-009 promotion-rate re-examination ("after the next 2-3 framework-relevant projects") will actually be revisited without an explicit owner or deadline | Temporal (implicit) | Low | Honestly disclosed as an open residual, but has no tracked trigger | The load-bearing belief ages past its own falsification window unnoticed |

---

## Findings Table

| ID | Assumption / Anti-Goal | Type | Confidence | Severity | Evidence | Affected Dimension |
|----|---|---|---|---|---|---|
| IN-001-20260705-i6 | AS-1 + AS-2: guidance is "in force" and auto-loaded | Assumption | Low | **Critical** | ADR:89; rule-draft:1-4; Glob (`.context/rules/adr-standards.md` absent) | Internal Consistency |
| IN-002-20260705-i6 | AS-4: current state beats the null alternative | Assumption | Medium | **Major** | ADR:260-266 (Null-Alternative section) vs. current unpublished state | Evidence Quality |
| IN-003-20260705-i6 | AS-3: H-32 scoped to only 3 of 14 rows | Anti-Goal | N/A | **Major** | ADR Migration Plan rows M-2..M-14 (:502-516); `.context/rules/quality-enforcement.md` H-32; `.context/rules/project-workflow.md` GitHub Issue Parity | Completeness / Methodological Rigor |
| IN-004-20260705-i6 | AS-6: PM-009 revisit has no tracked trigger | Assumption | Low | **Minor** | ADR:456 (PM-009 commitment prose, no owner/deadline field) | Traceability |

**Finding ID format:** `IN-{NNN}-20260705-i6` (execution_id = date + iteration marker, to avoid collision with prior iterations' IN-NNN tags already embedded in the deliverable).

---

## Finding Details

### IN-001: Status claims present-tense "in force / value" that is not yet structurally true [CRITICAL]

**Type:** Assumption (AS-1 + AS-2)
**Original Assumption:** "The convention is now in force as MEDIUM-tier guidance: authors SHOULD follow it, and it delivers value with zero tooling." (ADR-PROJ031-004:89, Status section, part of the v1.7 subtraction-pass rewrite)
**Inversion:** What if the guidance is *not* actually reachable by any session yet? Then "in force... delivers value" is not a description of present fact but of intended future fact.
**Plausibility:** Confirmed, not merely plausible. Two independent checks:
1. The companion rule draft's own wrapper states: *"On the M-2 move this content -- minus this wrapper -- becomes `.context/rules/adr-standards.md` and auto-loads via the `.claude/rules -> ../.context/rules` directory symlink."* (`adr-standards-rule-draft.md:3`) -- phrased as a future action ("on the M-2 move"), i.e., not yet done.
2. Independently Glob-verified in this review: `.context/rules/adr-standards.md` **does not exist** in the repository as of 2026-07-05. The only artifact is the project-scoped draft at `projects/PROJ-031-cowork-skeleton/design/adr-standards-rule-draft.md`, which no Claude Code session auto-loads (per `CLAUDE.md` Navigation, only `.context/rules/` content marked `(A)` auto-loads).
3. The ADR's own Claim-Status disclosure (:497) states plainly that **zero worktracker Task entities and zero GitHub Issues exist for any Migration-Plan row**, and this review independently confirms via Glob over `projects/PROJ-031-cowork-skeleton/work/` that no ADR-convention-related Task/Enabler/Story exists there (the only work items present are unrelated EPIC-001 skeleton-distribution entities). M-2 (publish guidance) and M-12 (fix the producing agent, disclosed by the ADR itself as the step "the convention is defeated at the source" without) are both marked "Gating: Yes" -- signaling the owner *knows* these are prerequisites -- yet neither has any tracked mechanism compelling execution.
**Consequence:** The single sentence in Status most likely to be read in isolation (by a future promoter, a governance reviewer, or another agent deciding whether to treat this as "settled") asserts a present-tense operative fact that is not yet true. This is precisely the "guaranteed failure" condition Inversion exists to surface: a convention that is ratified in prose, never propagated into either the auto-loaded rule corpus or the ADR-producing agent, and for which no tracked forcing function exists, is functionally indistinguishable from an unratified draft -- indefinitely. Nothing in the current package prevents this from persisting past PROJ-031's active window; once attention moves on, the "TBD-Task" cells (:497) have no mechanism to ever become real tasks.
**Dimension:** Internal Consistency (Status section vs. Migration Plan / Enforcement Design sections of the *same* document already disclose the gap this claim glosses over) and, secondarily, Completeness (no forcing function specified for M-2/M-9/M-12).
**Mitigation:** Add one explicit sentence to the Status section, at the point of the "delivers value with zero tooling" claim, disclosing the actual current state: *"As of ratification, this guidance has not yet been published to `.context/rules/adr-standards.md` (M-2, pending, untracked) and the producing agent has not yet been fixed (M-12, pending, untracked); until both land, the convention is a ratified intention, not yet an operative one for any session."* This costs one paragraph and closes the gap between the document's own internal disclosures (Migration Plan, Claim-Status) and its headline claim -- a subtraction-pass-consistent fix (disclose, don't add machinery).
**Acceptance Criteria:** The Status section states, in the same breath as any "in force" or "delivers value" language, the concrete current-vs-not-yet state of M-2/M-9/M-12, OR the M-2 move is actually executed (verifiable via Glob for `.context/rules/adr-standards.md`) before the next review cycle.

---

### IN-002: "Beats the null alternative" is demonstrated for the intended end-state, not the current state [MAJOR]

**Type:** Assumption (AS-4)
**Original Assumption:** The "zero-governance null alternative" section (ADR:260-266) argues Scheme B strictly beats doing-nothing on citation-integrity and collision-safety grounds, concluding "B is therefore strictly better than the null... The benchmark confirms a convention is warranted; it does not favour doing nothing."
**Inversion:** What if the comparison is evaluated at the *current*, actually-existing state of the package rather than its designed steady state?
**Plausibility:** High. The null-alternative argument's strongest claim -- "a subject-encoded ID is self-describing at zero maintenance cost, so `grep`-by-subject is free and always current" -- depends on new ADRs actually being minted with domain-slug identity. Today, new ADRs are minted by the producing agent (`ps-architect.md`), which the ADR's own Migration Plan (M-12) discloses still hardcodes a non-canonical filename grammar and is unfixed. Until M-12 lands, an ADR authored via that agent tomorrow is exactly as non-compliant as it would be under the null alternative -- the discovery-substrate advantage claimed for B has not yet materialized for agent-authored ADRs.
**Consequence:** The null-alternative section is directionally correct as a design-merit argument (it correctly identifies that a good convention beats no convention once operative), but as currently worded it reads as a claim about *already-realized* value ("B is therefore strictly better than the null" -- present tense, unqualified), which overstates what the current, unpublished, unfixed-producer state actually delivers.
**Dimension:** Evidence Quality (the claimed advantage is not yet evidenced by any executed instance -- consistent with the ADR's own honest DA-003 disclosure elsewhere that "zero Path-1 promotions have actually occurred yet").
**Mitigation:** Add a one-clause qualifier to the null-alternative conclusion: "...once M-2 (guidance publication) and M-12 (producer-agent fix) land" -- mirroring the Claim-Status pattern already used elsewhere in the same document (e.g., the lint Claim-Status block at :621). This is a wording fix, not new machinery, consistent with the subtraction doctrine.
**Acceptance Criteria:** The null-alternative conclusion carries the same "designed, not yet demonstrated" qualifier already applied consistently elsewhere in the ADR (Claim-Status convention).

---

### IN-003: H-32 GitHub Issue parity applied inconsistently across the Migration Plan [MAJOR]

**Type:** Anti-Goal (governance-compliance gap)
**Original Assumption (implicit):** It is acceptable for only 3 of the 14 Migration-Plan action rows (M-6, M-12, M-13) to carry "TBD-Task + GH Issue (H-32)" while the remaining 11 rows (M-2, M-2b, M-3, M-4, M-5, M-5b, M-8, M-9, M-10, M-11, M-14) carry only "TBD-Task" with no GitHub Issue reference.
**Inversion:** What would guarantee this Migration Plan generates work items that violate governance on day one? Answer: apply a HARD constitutional rule to a subset of the planned work items without a stated rationale for the subset boundary.
**Plausibility:** Confirmed by direct comparison. `.context/rules/quality-enforcement.md` HARD Rule Index lists `H-32 | GitHub Issue parity for jerry repo work items | project-workflow` with no stated exception for planning-stage or non-code work items. `.context/rules/project-workflow.md` ("GitHub Issue Parity" section) states the rule applies whenever "the active repository is `geekatron/jerry`" and requires GH issue parity for "all worktracker bugs, stories, enablers, and tasks" -- with no carve-out for governance/documentation Tasks (M-2, M-3, M-4, M-5, M-11, M-14 are exactly this kind of Task). The ADR's own Migration Plan (:502-516) shows the asymmetry directly: M-6/M-12/M-13 explicitly cite "(H-32)"; the other Task rows do not, with no stated reason for the distinction (e.g., "these are governance-only, not code-affecting" is not argued anywhere in the document).
**Consequence:** If/when these Task entities are actually created (a separate, currently-untracked step -- see IN-001), 11 of 14 would be created without a matching GitHub Issue, an out-of-the-box HARD-rule violation in the very repository this convention is designed to govern -- an ironic outcome for a document whose central thesis is preventing governance-integrity gaps.
**Dimension:** Completeness (the Migration Plan's own governance-compliance column is incomplete) and Methodological Rigor (a HARD rule applied selectively without justification).
**Mitigation:** Either (a) append "(H-32)" uniformly to all 14 "TBD-Task" cells with a one-line note that all will receive matching GH Issues per H-32 when created, or (b) if some rows are genuinely intended as non-worktracker informal follow-ups (not formal Task entities), say so explicitly to justify the omission. Either is a wording-only fix.
**Acceptance Criteria:** Every Migration-Plan cell that will produce a worktracker Task entity in the `geekatron/jerry` repo states its H-32 GitHub Issue obligation consistently, or explicitly states why it is exempt.

---

### IN-004: PM-009 re-examination commitment has no tracked trigger [MINOR]

**Type:** Assumption (AS-6)
**Original Assumption:** "Re-examine the promotion rate after the next 2-3 framework-relevant projects produce ADRs; if forward promotion stays approximately 0%... Scheme C should be reconsidered via a superseding ADR." (ADR:456, PM-009)
**Inversion:** What if nobody actually re-examines it, because there is no owner, deadline, or tracked worktracker item attached to the commitment?
**Plausibility:** Medium -- this is the same "no forcing function" pattern as IN-001/IN-003, applied to the single most load-bearing empirical belief in the whole decision (confidence explicitly capped at 0.70-0.75, n=3). The ADR is already honest that this is an open residual, not a closed one ("Neither residual is presented as fixed; both have a named detection signal and a named escalation path" -- :459), which meaningfully reduces (but does not eliminate) the risk of silent staleness.
**Consequence:** If the promotion rate regresses to the adverse regime described at :294-297 and nobody notices because no one is watching for it, the decision persists past the point its own stated conditions call for reconsideration.
**Dimension:** Traceability (the commitment names a detection signal in prose but not a tracked mechanism).
**Mitigation:** Note PM-009 as a worktracker-trackable recurring check (e.g., a lightweight reminder tied to "next 2-3 framework-relevant project closures") rather than leaving it purely as prose. Low priority given the honest framing already present.
**Acceptance Criteria:** MAY be addressed opportunistically; not a blocker.

---

## Null-Alternative Check

Direct answer to the assignment's explicit question: **does the slimmed package still beat the null alternative (no convention)?**

**Yes, on design merit -- with one caveat.** The ADR's own null-alternative section (:260-266) correctly identifies that the null option has no collision story (it is exactly today's already-collided state) and no citation-integrity fix, whereas Scheme B's filename grammar is a free, self-describing discovery substrate once operative. That reasoning holds. **The caveat, surfaced by this inversion pass:** "once operative" is doing real work in that sentence. As of this review (2026-07-05), the guidance is not yet published to where any session would see it (`.context/rules/adr-standards.md` absent, Glob-confirmed), the producing agent that mints new ADRs is not yet fixed (M-12 pending, untracked), and the lint that would catch new violations does not exist (already honestly disclosed by the owner). In this narrow, literal, present-tense sense, a new ADR authored today by the standard producing agent is exactly as non-compliant under Scheme B as it would be under the null alternative -- the advantage is real but not yet realized. This does not sink the decision; it means the Status section's present-tense framing should be brought into line with what the rest of the same document already discloses (see IN-001, IN-002).

---

## Recommendations

**Critical (MUST mitigate):**
- IN-001-20260705-i6: Add an explicit "not yet operative" disclosure to the Status section's "in force / delivers value" claim, naming M-2/M-9/M-12 as pending and untracked. One paragraph; no new machinery (consistent with subtraction doctrine).

**Major (SHOULD mitigate):**
- IN-002-20260705-i6: Qualify the null-alternative conclusion with the same Claim-Status pattern used elsewhere in the document ("once M-2/M-12 land").
- IN-003-20260705-i6: Reconcile H-32 citation coverage across all 14 Migration-Plan rows -- either apply uniformly or state the exemption rationale.

**Minor (MAY mitigate):**
- IN-004-20260705-i6: Optionally attach a lightweight tracked trigger to the PM-009 re-examination commitment.

---

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Negative | IN-003: Migration Plan's own governance-compliance coverage (H-32) is incomplete/inconsistent |
| Internal Consistency | 0.20 | Negative | IN-001: Status section's present-tense claim contradicts the same document's own Migration Plan / Claim-Status disclosures |
| Methodological Rigor | 0.20 | Negative | IN-003: a HARD rule applied selectively without stated rationale |
| Evidence Quality | 0.15 | Negative | IN-002: null-alternative "beats it" claim not yet evidenced by any executed instance |
| Actionability | 0.15 | Neutral | All four findings have concrete, one-paragraph, no-new-machinery mitigations consistent with subtraction doctrine |
| Traceability | 0.10 | Negative | IN-004: PM-009 commitment lacks a tracked trigger |

**Result:** 1 Critical and 2 Major assumption vulnerabilities identified via systematic inversion, plus 1 Minor. All four are wording/disclosure-level fixes (no new machinery required, consistent with the user-authorized subtraction doctrine) -- none invalidates Scheme B itself. The design decision (Options A-F evaluation, Scheme B selection, sensitivity analysis, grandfathering, MEDIUM-tier posture) holds up cleanly under inversion; the gap this pass surfaces is specifically in how the *current, actually-existing state* of the package is described relative to its *intended future state*, which is exactly the kind of gap Inversion (as distinct from Pre-Mortem's temporal framing) is designed to catch by stress-testing assumptions directly rather than narrating a hypothetical failure story.

---

*Generated by adv-executor (S-013 Inversion Technique, iteration 6). No subagents spawned (P-003). No deliverable files edited (P-020 -- owner-only edit per blind protocol mandate). All findings cite file+line or independently-run Glob checks; inference is labeled where used (P-022).*
