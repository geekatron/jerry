# Pre-Mortem Report: ADR-PROJ031-004 (ADR Identifier Convention) + Companion Rule Draft — Post-Subtraction-Pass Review

**Strategy:** S-004 Pre-Mortem Analysis
**Deliverable:** `projects/PROJ-031-cowork-skeleton/decisions/ADR-PROJ031-004-adr-identifier-convention.md` + `projects/PROJ-031-cowork-skeleton/design/adr-standards-rule-draft.md`
**Criticality:** C4 (engagement gate 0.95)
**Date:** 2026-07-06
**Reviewer:** adv-executor (S-004, iteration 8, blind independent review)
**H-16 Compliance:** No discrete S-003 execution artifact was accessible to this blind reviewer (blind protocol forbids reading `adversary/` except this file). H-16 is treated as satisfied on the basis of the deliverable's own self-disclosure: the ADR states "S-003's influence on this deliverable is embedded... every Option A–F... *leads* with the strongest steelman case its blind advocate made... before any critique" (`ADR-PROJ031-004-adr-identifier-convention.md:67`), with example tags `ST-001`/`ST-002` cited. This is an **inference from in-document evidence, not an independently verified artifact** (P-022 label).
**Failure Scenario:** It is 2027-07-06 (12 months from ratification). The ADR-identifier convention is nominally "ACCEPTED" but has quietly failed to change behavior: the corpus still mints inconsistent IDs, the lint never shipped, the convention's own self-promotion never happened, and a downstream CoWork adopter who tried to follow the guidance had no worked examples to copy. This report enumerates the failure paths that produce that outcome under the SLIMMED (post-subtraction) design specifically — i.e., failures caused by *under*-enforcement now that 13 of 18 lint rules, the waiver ledger, and the two-tier ratification gate are gone — and checks which of these the package already discloses.

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Overall assessment and recommendation |
| [Scope Note](#scope-note) | What this review does and does not re-litigate |
| [Findings Table](#findings-table) | All failure causes with severity/priority |
| [Finding Details](#finding-details) | Full evidence and disclosure-status per finding |
| [Recommendations](#recommendations) | P0/P1/P2 mitigation plan |
| [Scoring Impact](#scoring-impact) | Mapping to S-014 dimensions |

---

## Summary

The package is unusually well-instrumented for its own failure modes: it already carries a Pre-Mortem section (FM-1..FM-5), a 13-entry Risks register (R-1..R-13), and two named "post-ratification monitoring commitments" (PM-009, R-6) with dated escalation thresholds. Against that high bar, this independent pass found **0 Critical, 3 Major, 2 Minor** *new* failure paths — all specific to the post-subtraction (slimmed) enforcement model, none of which argue for restoring deleted machinery. The most consequential gap (PM-001) is that the single highest-severity *already-disclosed* risk (the "nothing lands" compound scenario, FM-5) is the **only** top-tier risk without a dated, quantified escalation trigger analogous to R-6's "≥2 L-3 failures in 90 days" or PM-009's "re-examine after 2–3 more framework-relevant projects" — an asymmetry in the monitoring rigor applied across the disclosure set. Recommendation: **ACCEPT with targeted mitigations** (no re-litigation of the subtraction pass itself; these are additive disclosures/monitoring commitments, not new machinery).

---

## Scope Note

Per task mandate, this review evaluates the package **as slimmed**: deletion of the waiver ledger, two-tier ratification gate, and 13 lint rules is treated as a valid, ratified design posture (MEDIUM-tier vocabulary, `quality-enforcement.md` Tier Vocabulary), not re-argued here. Findings below are failure paths **caused by or exposed by** the reduced enforcement surface, focused on under-enforcement, not "the lint should have stayed bigger."

---

## Findings Table

| ID | Failure Cause | Category | Likelihood | Severity | Priority | Affected Dimension |
|----|---------------|----------|------------|----------|----------|--------------------|
| PM-001-20260706-iter008 | Highest-severity disclosed risk (FM-5, "nothing lands") has no dated escalation threshold, unlike R-6/PM-009 | Process | High | Major | P1 | Actionability |
| PM-002-20260706-iter008 | `scope:` frontmatter field (load-bearing for AE-004 C3/C4 tiering) is validated by none of the 5 retained lint rules | Technical | Medium | Major | P2 | Internal Consistency |
| PM-003-20260706-iter008 | Downstream/plugin "recommended" strip removes the exemplar ADR corpus (`docs/design/`) alongside `projects/*/decisions/`, leaving guidance-only text with zero worked examples for the named CoWork audience | Process/External | Medium | Major | P2 | Completeness |
| PM-004-20260706-iter008 | R-10's stated LOW probability for entity-embedded-ADR out-of-scan likely understates risk; entity-embedded is a first-class, actively-used worktracker placement pattern, not a rare edge case | Technical | Medium (disputed; disclosed as Low) | Minor | P2 | Completeness |
| PM-005-20260706-iter008 | Dialect-corpus numerical dominance (16 dialect vs 3 canonical files at time of writing) creates an imitation-driven under-enforcement vector distinct from R-4's "deliberate hedge abuse" framing | Assumption | Medium | Minor | P2 | Evidence Quality |

**Finding ID Format:** `PM-{NNN}-20260706-iter008`.

---

## Finding Details

### PM-001: No dated escalation trigger for the single highest-severity disclosed risk [MAJOR]

**Failure Cause:** The package's own Pre-Mortem section names FM-5 ("the compound 'nothing lands' scenario") as "the single best-evidenced risk in this package" (`ADR-PROJ031-004-adr-identifier-convention.md:482`), rated HIGH severity, MED–HIGH occurrence. Its stated containment is "Open real M-2 + M-12 Tasks (H-32 parity) as the *first* execution action" — an intent, not a scheduled or monitored commitment. By contrast, the two "Post-ratification monitoring commitments" the package elevates to a named subsection (`:464-467`) — PM-009 (promotion-rate belief) and R-6 (cross-branch slug race) — **both** carry concrete, dated triggers: PM-009 commits to "re-examine the promotion rate after the next 2–3 framework-relevant projects"; R-6 defines "rising" as "≥ 2 distinct L-3 collision failures on `main` within any rolling 90-day window." FM-5 gets no equivalent: no date, no task count, no "if M-2/M-6/M-12 are still untracked by {date}, escalate to {who}" clause.

**Category:** Process
**Likelihood:** High — this is not hypothetical; the Migration Plan's own Claim-Status note (`:511`) already verifies **zero** worktracker Tasks or GitHub Issues exist for any of M-2 through M-14 as of the ratification date. Absent a trigger, "current state persists" is the default outcome, not an edge case.
**Severity:** Major — under-enforcement here defeats the entire convention at its source (M-12, the producing-agent fix, is explicitly marked "the producing agent must emit compliant IDs or the convention is defeated at the source," `:528`), yet nothing forces attention back to it.
**Evidence:** `ADR-PROJ031-004-adr-identifier-convention.md:482` (FM-5 row); `:464-467` (PM-009/R-6 monitoring commitments, dated); `:511` (zero-Task Claim-Status verification); `:513-530` (Migration Plan, all TBD-Task, no target dates).
**Dimension:** Actionability
**Disclosure status:** **Partially disclosed.** FM-5 itself and the zero-Task current state are disclosed honestly (P-022 compliant — no fabricated Task IDs). What is **not** disclosed is the *asymmetry*: two lower-severity residuals (R-6, PM-009) received dated monitoring commitments while the highest-severity one (FM-5) did not. This asymmetry is the actual finding.
**Mitigation:** Add a dated trigger to FM-5's containment, parallel to R-6/PM-009's format — e.g., "if M-2 and M-12 are not opened as tracked Tasks within 30 days of ratification, escalate to the governance owner and record the gap in the next `/adversary` or status review." This is a disclosure/monitoring addition, not new lint machinery — consistent with the subtraction doctrine.
**Acceptance Criteria:** FM-5's row (or a new "Post-ratification monitoring commitments" bullet) states a concrete date/count trigger and a named escalation path, matching the rigor already applied to PM-009 and R-6.

---

### PM-002: `scope:` frontmatter field is load-bearing for AE-004 tiering but validated by none of the 5 retained lint rules [MAJOR]

**Failure Cause:** The AE-004 scoping argument the ADR relies on to keep routine promotions at a C3 floor (rather than C4) hinges entirely on the `scope:` field: "A Path-1 promotion changes only **location** ... and the **`scope` field**... A metadata+location transition... does not trip AE-004's C4" (`ADR-PROJ031-004-adr-identifier-convention.md:559`). Checking the 5 retained lint rules against this claim: L-1 (grammar) validates the *filename* only; L-2 (no-new-bare) validates the *filename* only; L-3 (no-duplicate) extracts IDs from *filenames*; L-4 (ID↔location) checks dialect-prefix-vs-directory, not frontmatter content; L-7 (relationship-target-resolves) checks only that `superseded_by`/`promoted_to`/`promoted_from` targets exist. **None of the five inspects the `scope:` field's presence or correctness.** This is distinct from the already-disclosed FM-104 residual, which covers `origin_project`/`origin_entity` provenance specifically ("no lint in the 5-rule core checks provenance at all," `:427`) — that passage never names `scope` as the field left unchecked, nor connects the gap to AE-004 tiering.
**Category:** Technical / Governance
**Likelihood:** Medium — requires either an author mis-declaring `scope` or a genuine Path-1 promotion quietly carrying bundled content edits; plausible given the producing agent (`ps-architect.md`) is itself currently non-compliant (M-12 unfixed, `:528`) and the field is authored manually with no fallback default check.
**Severity:** Major — if `scope` is wrong or absent, a content change that should trigger AE-004's auto-C4 escalation could instead be nominally processed and reviewed at only C3 rigor, with zero automated detection, for as long as 12 months.
**Evidence:** `ADR-PROJ031-004-adr-identifier-convention.md:559` (AE-004 Path-1/Path-2 split hinges on `scope`); `adr-standards-rule-draft.md:171-178` (the 5-rule table — L-1/L-2/L-3/L-4/L-7 — none references `scope:`); `ADR-PROJ031-004-adr-identifier-convention.md:427` (FM-104, the disclosed-but-adjacent provenance gap, scoped to `origin_project`/`origin_entity`, not `scope`); `ADR-PROJ031-004-adr-identifier-convention.md:565` (CC-002-iter7: the AE-004 C3/C4 split is itself "this ADR's own interpretation... not yet ratified into the SSOT" — a related, but distinct, disclosed residual that compounds this one).
**Dimension:** Internal Consistency — the ADR asserts a specific mechanism (scope-field-driven AE-004 tiering) that its own lint design cannot verify.
**Disclosure status:** **Not disclosed** as its own residual. A closely related field (`origin_project`) is disclosed as lint-unverified (FM-104); the CC-002-iter7 note discloses that the *interpretation* of AE-004 is unratified; neither statement names `scope`-field validation absence or its specific consequence for silent criticality mis-tiering.
**Mitigation:** Add `scope:` to the disclosed-residual list alongside `origin_project`/`origin_entity` (a one-sentence honesty fix, consistent with the subtraction doctrine's "delete/disclose the exposing claim, add nothing" pattern) — no new lint rule required, only an accurate disclosure of what the 5 rules do not check.
**Acceptance Criteria:** A sentence in Consequences/Positive-3 or the Risks register explicitly names `scope` as unchecked and cross-references its AE-004-tiering consequence.

---

### PM-003: Downstream/plugin "recommended" strip removes the exemplar corpus, not just the lint target [MAJOR]

**Failure Cause:** The ADR's Enforcement Scope section discloses that a distributed plugin build strips `projects/` (and, "as a recommended addition," `docs/`), concluding "a plugin install ships *no* ADR files to lint" (`ADR-PROJ031-004-adr-identifier-convention.md:646-649`). Cross-checked against the sibling design (`phase3-skeleton-generation-design.md:168-173`): the "RECOMMENDED additional strips" explicitly include `docs/ (247 files)` — which contains `docs/design/`, the framework-canonical exemplar ADRs (`ADR-agent-design-001`, `ADR-routing-triggers-001`, `ADR-output-path-resolution-001`) referenced throughout this very ADR as the worked proof that Scheme B works. The disclosed consequence is framed only in **lint** terms ("no ADR files to lint"); it is not reframed in **pedagogical** terms: a fresh downstream CoWork adopter — PROJ-031's own named audience — who follows the auto-loaded `.context/rules/adr-standards.md` guidance (which does survive the strip, since `.context/` is not on either the validated or recommended strip list) has **zero locally-shipped worked examples** of a compliant `ADR-{domain-slug}-NNN` file to imitate, at precisely the moment (fresh install, first ADR) a new contributor most needs one.
**Category:** Process / External
**Likelihood:** Medium — depends on whether the "recommended" (not required) `docs/` strip is applied by a given downstream build; the design frames it as SHOULD, so it is plausible but not universal.
**Severity:** Major — this is a real weakening of the guidance-only enforcement model for exactly the audience the ADR's own creator-project (PROJ-031) exists to serve; a text-only rule with no corpus example is a materially weaker behavioral signal than the same rule accompanied by 3 worked files.
**Evidence:** `ADR-PROJ031-004-adr-identifier-convention.md:646-649` (Enforcement Scope disclosure, framed as lint-target absence); `phase3-skeleton-generation-design.md:168-173` (recommended strip list includes `docs/`, 247 files); `ADR-PROJ031-004-adr-identifier-convention.md:88` (`.context/rules/` not named among stripped paths, so the guidance text itself does survive — confirming the gap is specifically "guidance without exemplar," not "no guidance at all").
**Dimension:** Completeness
**Disclosure status:** **Partially disclosed.** The strip fact and the "no files to lint" consequence are disclosed; the "no files to *learn from*" consequence for the CoWork audience specifically is not named.
**Mitigation:** One additional sentence in the Enforcement Scope table's downstream row: note that the recommended `docs/` strip also removes worked examples, and recommend that a minimal exemplar (one canonical-form sample ADR) be retained or documented separately for downstream adopters — a disclosure/documentation fix, not new machinery.
**Acceptance Criteria:** The downstream-adopter row in the Enforcement Scope table names both consequences (no lint corpus, no exemplar corpus) rather than the first alone.

---

### PM-004: R-10's LOW probability rating for a permanently-unlinted, permitted location class may be optimistic [MINOR]

**Failure Cause:** R-10 discloses that the lint's hard-coded scan (`find projects docs/design -path '*/decisions/*'`) misses two location classes entirely: entity-embedded ADRs (`work/.../{ENTITY}/`, no `decisions/` segment) and the repository-based topology's `{RepositoryRoot}/decisions/` home. R-10 rates this **LOW** probability (`ADR-PROJ031-004-adr-identifier-convention.md:459`). But the Canonical Location Model table itself lists "Entity-embedded (permitted)" as an **Active** state, not a deprecated or rare one (`:380`), and Jerry's worktracker SSOT documents entity-scoped decision-adjacent artifacts (`DEC-NNN`) as a routine, first-class pattern. If entity-embedded ADRs continue to be authored at even a modest rate as the corpus grows (the stated concern for R-7/synonymy — "rises at 50+ projects" — applies equally here), an entire permitted location class remains permanently unlinted, with the disclosed remediation ("parameterizing the scan roots... a future MAY tied to the unbuilt M-6") deferred behind an already-unbuilt milestone with no committed date.
**Category:** Technical
**Likelihood:** Medium (this review's assessment) vs. Low (as stated in the ADR) — a documented disagreement, not a claim of non-disclosure.
**Severity:** Minor — the gap and its non-committed remediation path are already honestly disclosed; only the probability calibration is in question.
**Evidence:** `ADR-PROJ031-004-adr-identifier-convention.md:459` (R-10 row, LOW probability); `:380` (Canonical Location Model, entity-embedded = Active/permitted); R-7's own probability escalation logic ("rises at 50+ projects," `:456`) applied by analogy.
**Dimension:** Completeness
**Disclosure status:** **Fully disclosed** as a residual; this finding only disputes the likelihood label, not the existence of the disclosure.
**Mitigation:** Re-rate R-10's probability to MED (or explicitly justify why entity-embedded ADR authorship is expected to stay rare) at the next revision pass — a labeling correction, not new machinery.
**Acceptance Criteria:** R-10's probability column reflects either a MED rating or an explicit rationale for why LOW is the correct calibration given the "Active" classification of the location it concerns.

---

### PM-005: Dialect-corpus numerical dominance creates an imitation vector distinct from R-4's "deliberate abuse" framing [MINOR]

**Failure Cause:** At time of writing, the visible corpus contains 16 dialect-form ADRs (15 pre-existing + this ADR itself, per D-4/`:223`) versus 3 canonical domain-slug-form ADRs. R-4 in the Risks register frames dialect-persistence risk as "Authors abuse the dialect, re-introducing rename churn" — a **deliberate choice** framing, mitigated by "SHOULD-guidance; promotion process surfaces the cost" (`:453`). This does not address a distinct, passive failure mode: a new author (human or agent) scanning the existing corpus for a pattern to copy will, for a considerable transition period, see the dialect form roughly 5x more often than the canonical form — independent of what the SHOULD-guidance prose says. Pattern-imitation from majority examples is a well-documented behavior in both human onboarding and LLM in-context pattern matching, and the ADR's own text acknowledges this dynamic in a different context (PM-005 acknowledges M-9's importance partly because "the flagship self-compliance demonstration is only described, never performed" without it, `:525` — i.e., the document already recognizes that *demonstrated* examples carry independent weight beyond prose, just not framed as an imitation risk for the dialect-majority corpus).
**Category:** Assumption
**Likelihood:** Medium — declines naturally as the canonical-form share of the corpus grows over 12 months, but is highest exactly in the near-term window this pre-mortem is stress-testing.
**Severity:** Minor — self-correcting over time as D-4's grandfather set stays fixed while new canonical ADRs accumulate; not a structural flaw, but an under-examined transitional risk.
**Evidence:** `ADR-PROJ031-004-adr-identifier-convention.md:223` (D-4, 16-file dialect count); `:453` (R-4, framed as deliberate abuse, not passive imitation); `:525` (M-9 rationale implicitly values demonstrated examples over prose-only guidance, in a different context).
**Dimension:** Evidence Quality
**Disclosure status:** **Not disclosed** as a distinct risk; R-4 covers an adjacent but different mechanism (deliberate hedge abuse vs. passive majority-pattern imitation).
**Mitigation:** Note in R-4 or M-5 that the dialect-to-canonical file-count ratio is itself a transitional imitation risk, expected to invert as canonical-form ADRs accumulate; no new lint required — an observability/disclosure addition only.
**Acceptance Criteria:** R-4 (or a new risk row) names the corpus-ratio imitation dynamic as distinct from deliberate dialect abuse.

---

## Recommendations

**P1 (Important — SHOULD mitigate):**
- PM-001-20260706-iter008: Add a dated escalation trigger to FM-5, matching the rigor already given to R-6/PM-009.

**P2 (Monitor — MAY mitigate; acknowledge risk):**
- PM-002-20260706-iter008: Disclose `scope:` as lint-unvalidated alongside the existing `origin_project` disclosure; note the AE-004-tiering consequence.
- PM-003-20260706-iter008: Extend the Enforcement Scope downstream row to name the exemplar-corpus loss, not only the lint-corpus loss.
- PM-004-20260706-iter008: Re-calibrate R-10's probability rating or justify LOW explicitly against the "Active/permitted" classification of entity-embedded ADRs.
- PM-005-20260706-iter008: Add a one-line disclosure distinguishing corpus-ratio imitation risk from R-4's deliberate-abuse framing.

None of these recommendations restores deleted machinery (waiver ledger, two-tier gate, additional lint rules); all are disclosure or monitoring-commitment additions consistent with the subtraction doctrine already applied to this package.

---

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Negative (Minor) | PM-003, PM-004: two disclosed-but-narrowly-framed gaps (exemplar-corpus loss, entity-embedded scan) are not fully connected to their downstream consequences |
| Internal Consistency | 0.20 | Negative (Minor-Major) | PM-002: the AE-004 C3/C4 tiering claim rests on a `scope:` field that no lint rule verifies, an internal gap between claimed mechanism and actual verification |
| Methodological Rigor | 0.20 | Neutral-to-Positive | The package's own pre-mortem/risk-register/monitoring-commitment apparatus is thorough and largely well-calibrated; PM-001 identifies an asymmetry in rigor application, not an absence of rigor |
| Evidence Quality | 0.15 | Negative (Minor) | PM-005: the dialect/canonical file-count ratio is available evidence not yet connected to an imitation-risk framing |
| Actionability | 0.15 | Negative (Major) | PM-001: the single highest-severity disclosed risk lacks a scheduled, checkable trigger — reducing it to good intentions rather than a monitored commitment |
| Traceability | 0.10 | Positive | All findings in this report trace to specific file:line evidence in the deliverable and one cross-referenced design document; the package's own extensive citation discipline made this traceable review possible |

**Overall assessment:** Targeted mitigation recommended (0 Critical, 3 Major, 2 Minor). The package's post-subtraction posture is sound; the gaps found here are refinements to an already-disclosed risk register, not evidence that the subtraction pass under-disclosed systemically.

---

*No subagents spawned (P-003). No files edited outside mandate — this report only (P-020). All findings cite file:line evidence; the H-16 compliance basis and R-10/R-4 disagreements are explicitly labeled as this reviewer's inference, not fact (P-022).*
