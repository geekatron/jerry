# Steelman Report: ADR-adversary-tournament-protocol-001 (Verified-Criticals Tournament Methodology)

## Document Sections

| Section | Purpose |
|---------|---------|
| [Steelman Context](#steelman-context) | Deliverable, criticality, strategy |
| [Summary](#summary) | Assessment and improvement count |
| [Charitable Interpretation](#charitable-interpretation-step-1) | Core thesis, most-charitable reading |
| [Weakness Classification](#weakness-classification-step-2) | Presentation vs. structural vs. substantive |
| [Best Case Scenario](#best-case-scenario-step-4) | Conditions under which the ADR is strongest |
| [Improvement Findings Table](#improvement-findings-table) | SM-NNN findings, severity, dimension |
| [Improvement Details](#improvement-details) | Before/after for each Major finding |
| [Scoring Impact](#scoring-impact) | Effect on the 6 SSOT dimensions |

---

## Steelman Context

- **Deliverable:** `projects/PROJ-031-cowork-skeleton/decisions/ADR-adversary-tournament-protocol-001-verified-criticals-methodology.md`
- **Deliverable Type:** ADR (Nygard format, L0/L1/L2)
- **Criticality Level:** C3 (gate 0.92 SSOT; per invoking task)
- **Strategy:** S-003 (Steelman Technique)
- **SSOT Reference:** `.context/rules/quality-enforcement.md`
- **Steelman By:** adv-executor (blind, iteration 1) | **Date:** 2026-07-07 | **Original Author:** ps-architect

---

## Summary

**Steelman Assessment:** A genuinely strong, unusually well-evidenced C4-derived ADR. Every spot-checked
citation against the 18-round evidence corpus (score reports, subtraction-pass notes, fix-notes) resolved
exactly as stated — a rare degree of evidentiary discipline for a document this size. The surviving gaps
are narrow, self-contained, and fixable by text edit alone; none require re-litigating D-1 through D-6.

**Improvement Count:** 0 Critical, 2 Major, 2 Minor

**Original Strength:** HIGH. The core thesis (independent 3-lens verification restores tournament
convergence) is directly supported by reproduced, verifiable numbers (0.68→0.86/0.88, 5/5 and 0/6
verified/refuted splits, the DA-002-i8 fix-introduced regression, the PR-template fabrication) — all
independently re-verified against source files during this review and found accurate.

**Recommendation:** Incorporate the 2 Major fixes (both are precision/consistency corrections, not
substantive re-decisions) before this ADR proceeds to critique strategies (S-002/S-004/S-001) per H-16.

---

## Charitable Interpretation (Step 1)

**Core thesis:** A blind adversarial tournament without independent verification does not converge — it
manufactures a roughly constant stream of Critical-severity claims per round regardless of the
document's true defect count, and can canonize a fabricated claim for multiple rounds. Inserting an
independent, criticality-gated, 2-of-3-majority 3-lens refutation panel between "claimed" and "counted"
fixes this, at a bounded, criticality-proportional cost.

**Key claims, most-charitable reading:**
1. The additive-remediation spiral (iter-5→iter-8 ADR-convention thread, 10 closed / 7 new) and the
   declining-score spiral (iter-5→iter-6 FU-log thread, 0.468→0.460 across six zero-regression rounds)
   are real, independently reproducible patterns — **verified**: both score reports match the ADR's
   citations exactly, including exact composite figures and Critical counts.
2. The verified-protocol delta (0.68→0.86 at ADR-convention iter-9; 0.68→0.88 at iter-10; 0.51→0.72 at
   FU-log iter-8) is the single strongest piece of evidence for D-1/D-2 — **verified**: all four
   composite pairs reproduce exactly from the cited score reports.
3. The fabricated-verification incident (a false "Glob-verified absent" PR-template claim surviving
   iterations 6-9) is the strongest argument for *independence* specifically (Force 6, D-1 rejection of
   option D) — **verified**: `post-ceiling-fix-notes.md` confirms the false claim, the exact survival
   window (4 iterations), and the git-log-dated correction.
4. DA-002-i8 (a dedup mechanism that itself silently drops edited feedback) is offered as proof the
   panel preserves *genuine*, fix-introduced regressions, not just discards noise — **verified**:
   `post-tournament-fix-notes.md:37` states verbatim "a regression introduced by the very fix that
   closed the prior over-capture finding," matching the ADR's framing precisely.

Given this density of independently-reproducible evidence, the ADR's central decision (D-1: build an
independent, criticality-gated panel) does not need defending against fabrication or cherry-picking
concerns — the record is real and the citations resolve. The task per S-003 Step 2 is therefore to find
where the *expression* — not the *substance* — of D-1 through D-6 has small, fixable gaps.

---

## Weakness Classification (Step 2)

| Weakness | Type | Magnitude |
|----------|------|-----------|
| Verify-stage invocation granularity (per-report vs. per-claimed-Critical) is stated two incompatible ways in the same document, and the two ways yield materially different cost/file-count predictions | Structural / Evidence | Major (SM-001) |
| RSK-1's stated mitigation mechanism reads as logically inverted relative to the risk it mitigates | Presentation (a wording/reasoning defect, not a defect in the underlying design — the *other* three cited mitigations for RSK-1 remain valid) | Major (SM-002) |
| D-1's Options-table wording ("C4 full panels") is never operationalized or reconciled with the Decision table's "C4 all Criticals" (identical in practice to C3's "Criticals only") | Presentation | Minor (SM-003) |
| RSK-6's "sunset once the team is calibrated" has no concrete trigger, unlike every other stop/switch condition in the ADR (RT-M-010 ceiling, plateau delta < 0.01×3, 2-of-3 majority) | Structural | Minor (SM-004) |

All four are presentation/structural/evidence gaps in the ADR's own text, not substantive objections to
D-1 through D-6 — the underlying decisions (build `adv-verifier`, gate by criticality, verified-only
gating, subtraction-first, convergence discriminator, mandatory delta-reconciliation) are left intact for
downstream critique strategies to test on their merits.

---

## Best Case Scenario (Step 4)

This ADR is strongest when read as a **faithful formalization of an already-executed, already-verified
process** rather than a green-field proposal. Under that reading, its evidentiary burden is unusually
low-risk (it is describing something that already ran 18 times, not merely arguing something should
work) — and that is exactly the frame in which the two Major gaps below matter most: SM-001 shows the
formalization's own invocation spec would *not* reproduce the very process it claims to formalize, and
SM-002 shows one risk-mitigation clause is not internally coherent. Filling both gaps costs a few
sentences and strengthens, rather than changes, the ADR's central claim. Confidence in the underlying
thesis: **HIGH** — contingent only on these two textual corrections landing before implementation
(WI-1/WI-3) locks in the wrong granularity or an unexamined risk rating.

---

## Improvement Findings Table

| ID | Improvement | Severity | Affected Dimension |
|----|-------------|----------|---------------------|
| SM-001-20260707T0001 | Reconcile per-report vs. per-claimed-Critical invocation/cost-model contradiction; correct the FU-log iter-8 file-count citation (12, not 18) | Major | Internal Consistency / Evidence Quality / Actionability |
| SM-002-20260707T0001 | Correct RSK-1's inverted mitigation clause (DEFAULT-REFUTED biases toward discarding, not "keeping," claims) | Major | Internal Consistency / Methodological Rigor |
| SM-003-20260707T0001 | Reconcile "C4 full panels" (Options table) with "C4 all Criticals" / "Criticals only" (Decision table, WI-4) — clarify whether C4 ever panels Majors | Minor | Internal Consistency |
| SM-004-20260707T0001 | Give RSK-6's dual-protocol sunset a concrete trigger, consistent with the ADR's own precision elsewhere (RT-M-010, plateau delta) | Minor | Actionability |

---

## Improvement Details

### SM-001 (Major) — Verify-stage invocation granularity contradiction

**Affected Dimension:** Internal Consistency (primary), Evidence Quality, Actionability

**Original Content:**
- Constraints table, `c-004` (ADR line 206): *"panels ≈ 3 agent runs per **Critical-bearing report**"* —
  cites *"iter-9: 15 files = 3 lenses × 5; iter-8 FU: 18 files."*
- D-6 rationale (ADR line 364): *"18 verification-panel files"* for FU-log iteration 8.
- L1 Technical Implementation, item 1 (ADR lines 585-586): *"Invocation contract: one call **per lens
  per Critical-bearing report**. Input = **the single claimed Critical** (id, severity, evidence,
  affected dimension) ..."* and (line 589) persisted to
  `.../verify/{finding-id}-{lens}.md`.
- L1 Cost model (ADR lines 624-626): *"cost ≈ 3 × (**number of claimed Criticals**) at C4, 3 ×
  (Criticals) at C3 ... Empirically ~15-18 verifier files per C4 round."*
- Consequences, Negative-1 (ADR line 680): *"~3 extra agent runs per **claimed Critical** (c-004)."*

**Problem (independently verified against the filesystem, not merely re-stated):**
1. `projects/PROJ-031-cowork-skeleton/orchestration/adr-convention-20260702-001/adversary/iteration-009/verify/`
   contains exactly **15** files — but they are grouped **per finder-strategy report** (`s-001-*`,
   `s-002-*`, `s-004 pre-mortem analysis-*`, `s-011-*`, `s-012 (fmea)...-*` — 5 reports × 3 lenses = 15),
   not per individual claimed Critical. Iteration 9 claimed **10** distinct Criticals across those same
   5 reports (2 from S-001, 2 from S-002, 2 from S-004, 1 from S-011, 3 from S-012 — see
   `iteration-009/s-014-quality-score.md:23-34`), so a genuinely per-Critical invocation (as the Cost
   model and Negative-1 state, and as the proposed filename `{finding-id}-{lens}.md` implies) would
   require **30** files, not 15.
2. `projects/PROJ-031-cowork-skeleton/orchestration/fu-log-convention-20260705-001/adversary/iteration-008/verify/`
   contains exactly **12** files (`s-001 red team analysis-*`, `s-002-*`, `s-004 pre-mortem analysis
   (iteration 8...)-*`, `s-012 (fmea...)-*` — 4 reports × 3 lenses = 12), **not 18** as both ADR line
   206 and line 364 state. (The "18" figure appears to be inherited, unverified, from the source score
   report's own Inputs-Read line, which itself is arithmetically inconsistent — it states "4
   Critical-bearing reports" in the same sentence as "18 verification-panel files," when 4 × 3 = 12.)
   Iteration 8 claimed **7** distinct Criticals (`iteration-008/s-014-quality-score.md:54,63-71`) across
   those 4 reports, so per-Critical invocation would require **21** files, not 12 or 18.
3. The proposed persistence pattern `{finding-id}-{lens}.md` (singular finding-id) is therefore
   inconsistent with the empirical file-naming pattern actually used across all cited evidence
   (`{strategy-report-name}-refutation-{lens}.md`, which bundles every Critical from that report into
   one file per lens) — and inconsistent with the Constraints-table framing on the same page
   (`c-004`: "per Critical-bearing **report**").

**Why this matters:** WI-1 (`adv-verifier` agent + 3-lens contract) and WI-2 (`s-016-refutation-panel.md`
template) are specified directly from this L1 section. As written, an implementer following the literal
invocation contract ("Input = the single claimed Critical," filename `{finding-id}-{lens}.md`) would
build a **different**, more expensive process (per-Critical) than the one this ADR's own evidence base
actually ran (per-report) — the exact kind of unverified-claim-survives-multiple-rounds failure mode this
ADR's own Context section holds up as the central cautionary tale (the fabricated PR-template claim).
This is a fixable, text-only correction fully consistent with the ADR's own subtraction/precision
doctrine — it does not touch D-1's choice of a criticality-gated panel or D-6's choice of a dedicated
agent.

**Strengthened Content (proposed edit, illustrative):**
> *"Invocation contract: one call per lens per Critical-bearing **report** (not per individual claimed
> Critical). Input = **all claimed Criticals in that report** (each with id, severity, evidence, affected
> dimension) + the deliverable path + the lens name; a single lens-file verdict MAY differ per
> claimed Critical within the same report (see `iteration-009` RT-001 VERIFIED vs. RT-002 VERIFIED-2/3,
> same report, same lens-file). Output persisted to
> `.../verify/{report-slug}-refutation-{lens}.md`. Cost model: ≈ 3 × (number of Critical-bearing
> **reports**, not individual claims) — empirically 15 files (5 reports) at ADR-convention iter-9 and
> **12** files (4 reports) at FU-log iter-8, both filesystem-verified 2026-07-07."*

**Rationale:** Preserves D-1/D-6's substance; corrects the one place the ADR's own formalization would
silently double implementation cost and diverge from its cited evidence. Confidence: HIGH — verified
independently via `Glob` against both cited directories, not merely re-derived from the ADR's own
arithmetic.

---

### SM-002 (Major) — RSK-1 mitigation clause reads as logically inverted

**Affected Dimension:** Internal Consistency (primary), Methodological Rigor

**Original Content (ADR line 707, Risks table):**
> | RSK-1 | **Verifier leniency false-negative** — a real Critical is refuted and slips the gate. | MED
> | HIGH | 2-of-3 majority + **DEFAULT-REFUTED biases toward *keeping* claims**; factual lens is
> evidence-anchored (file+line); anti-leniency mandate inherited from `adv-scorer.md:68-91`; convergence
> discriminator re-surfaces a genuinely recurring defect in a later round. |

**Problem:** RSK-1 is the risk that a *genuine* Critical is wrongly **refuted** (a false negative).
DEFAULT-REFUTED, by the ADR's own definition (D-1 Decision row, line 381: *"2-of-3 majority,
**DEFAULT-REFUTED**, blind to each other"*), means any tie or insufficient lens agreement resolves
**toward refuting** the claim — i.e., toward *discarding*, not "keeping," a claim under uncertainty. As
written, the mitigation clause cites the very mechanism that would *increase* the probability of the
named risk (a real Critical failing to reach 2-of-3 and being discarded) as if it reduced that
probability. This is a self-contained logical inversion, checkable from the ADR's own text alone (no
external corpus needed): DEFAULT-REFUTED is the correct anti-*inflation* mechanism (it mitigates the
opposite risk — a false Critical being wrongly *verified*), but it is misapplied here as a mitigation for
false *negatives*.

**Why this matters:** RSK-1 is explicitly named "Primary risk" in the Decision section's Alignment table
(*"Risk Level | MED | Primary risk is verifier leniency/collusion; mitigated by blindness +
default-REFUTED + 2-of-3"*), so the "MED" risk rating assigned to adopting this whole methodology rests
partly on a mitigation clause that does not hold up under its own stated definitions. The other two cited
mitigations for RSK-1 (the evidence-anchored factual lens; the convergence discriminator re-surfacing a
recurring defect in a later round) remain valid and load-bearing on their own — this is why the finding
is Major, not Critical: correcting one clause does not change the Alignment table's bottom line, but the
clause as written currently argues the opposite of what it should.

**Strengthened Content (proposed edit, illustrative):**
> *"Blind independence + the evidence-anchored factual lens (not DEFAULT-REFUTED, which is an
> anti-inflation default and, if anything, mildly **raises** false-negative exposure under genuine
> lens disagreement) reduce single-point failure; the convergence discriminator (D-4) re-surfaces a
> genuinely recurring real defect in a later round even if refuted once; anti-leniency mandate inherited
> from `adv-scorer.md:68-91`. Residual exposure: a real Critical refuted in the **final** round before
> the RT-M-010 ceiling has no later round to re-surface in — disclosed, not eliminated."*

**Rationale:** This correction also surfaces a related, previously-undisclosed residual (a real Critical
refuted in the last round before the ceiling has no later round to catch it) — itself a small,
worthwhile addition to the ADR's own honest-limits discipline, consistent with the subtraction/disclosure
doctrine D-3 champions elsewhere. Confidence: HIGH — derivable from the ADR's own D-1 definition of
DEFAULT-REFUTED without consulting the evidence corpus.

---

### SM-003 (Minor) — "C4 full panels" vs. "C4 all Criticals" terminology drift

**Original Content:** D-1 Options table (line 247): *"C. Criticality-proportional verify (**C4 full
panels**; C3 panels on Criticals only; C1-C2 none)"* vs. the chosen-option Decision table (line 381):
*"C4 **all Criticals**; C3 Criticals only"* and WI-4 (line 730): *"C4 = all Criticals, C3 = Criticals
only."*

**Problem:** "Full panels" (Options table) reads as though C4 might panel more than Criticals alone
(e.g., Majors too), but every other mention of the C4 panel scope — the Decision table, WI-4's
acceptance criteria, and all 18 rounds of cited evidence (Majors are consistently "advisory only, no
refutation panel runs against Majors" — e.g., `iteration-010/s-014-quality-score.md:144-146`) — treats C3
and C4 identically: panel Criticals only, never Majors. The distinction the Options-table wording implies
is never operationalized anywhere downstream.

**Strengthened Content (proposed edit):** Replace "C4 full panels" with "C4 panels on Criticals (same
scope as C3; both exclude Majors)" in the Options table, removing the only place in the document that
implies a C3/C4 scope difference that does not otherwise exist.

**Rationale:** Zero-cost wording fix; removes a dangling implication with no downstream consequence
otherwise. Confidence: HIGH.

---

### SM-004 (Minor) — RSK-6 sunset condition has no concrete trigger

**Original Content:** RSK-6 (Risks table): *"Dual-protocol confusion during transition. MED | LOW |
Operative verdict always labeled; **sunset the old-protocol composite once the team is calibrated**."*

**Problem:** Every other stop/switch condition in this ADR is given a concrete, checkable trigger
(RT-M-010's numeric ceilings; the plateau rule's "delta < 0.01 for 3 consecutive iterations"; the 2-of-3
majority itself). "Once the team is calibrated" is the one exception — no round count, score-stability
window, or user sign-off event is named.

**Strengthened Content (proposed edit, illustrative):** *"Sunset the old-protocol composite after 3
consecutive rounds where the verified and old-protocol composites are both reported and no stakeholder
requests the old-protocol figure — mirroring the plateau rule's 3-round window."*

**Rationale:** Small, consistent with the ADR's own precision standard elsewhere; does not change D-2's
substance. Confidence: MEDIUM (the specific numeric analogy to the plateau rule is this reviewer's
proposal, not independently evidenced — labeled as inference, P-022).

---

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Neutral | Findings do not identify missing sections; the ADR's 8-section-equivalent Nygard structure is already complete. |
| Internal Consistency | 0.20 | Positive | SM-001 and SM-002 each resolve a genuine self-contradiction (invocation granularity; RSK-1 mitigation logic) discoverable from the ADR's own text. SM-003 removes a dangling implication. |
| Methodological Rigor | 0.20 | Positive | SM-002's correction strengthens the risk-assessment discipline the ADR otherwise models well (e.g., its own P-022 correction of the fabricated PR-template claim in the evidence corpus). |
| Evidence Quality | 0.15 | Positive | SM-001 corrects a propagated, verifiably-wrong quantitative citation (18 vs. actual 12 files) — the same failure class (unverified "Glob-verified"-style claims surviving multiple rounds) this ADR's own Context section names as the central cautionary tale. |
| Actionability | 0.15 | Positive | SM-001 prevents WI-1/WI-2 from being built to an ambiguous or contradictory spec; SM-004 gives RSK-6 a checkable trigger. |
| Traceability | 0.10 | Neutral | Citation discipline is otherwise exceptional — every other spot-checked citation (composites, panel splits, DA-002-i8, the PR-template incident, adv-scorer.md:166-167, adv-selector.md:112-128, SKILL.md:111-133, TEMPLATE-FORMAT.md:50/85-89/328) reproduced exactly against source files during this review. |

---

*Steelman execution by adv-executor (S-003, blind, iteration 1). No subagents invoked (P-003). No edits
made to the deliverable (P-020) — all proposed text is illustrative for the Improvement Findings only.
All findings cite repo-relative file paths and line numbers independently re-verified against source
files (P-022); the SM-004 numeric analogy is explicitly labeled as this reviewer's inference, not
evidenced fact.*
