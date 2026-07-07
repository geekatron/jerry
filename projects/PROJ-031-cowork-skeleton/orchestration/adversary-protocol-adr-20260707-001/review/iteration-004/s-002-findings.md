# Devil's Advocate Report: ADR-adversary-tournament-protocol-001 (Verified-Criticals Tournament Methodology)

## Navigation

| Section | Purpose |
|---------|---------|
| [Header](#header) | Strategy metadata and H-16 compliance note |
| [Summary](#summary) | Overall assessment |
| [Assumption Inventory](#assumption-inventory-step-2) | Explicit/implicit assumptions challenged |
| [Findings Table](#findings-table) | All counter-arguments with severity |
| [Finding Details](#finding-details) | Expanded Critical/Major findings |
| [Recommendations](#recommendations) | P0/P1/P2 prioritized actions |
| [Scoring Impact](#scoring-impact) | Dimension-level impact assessment |

---

## Header

**Strategy:** S-002 Devil's Advocate
**Deliverable:** `projects/PROJ-031-cowork-skeleton/decisions/ADR-adversary-tournament-protocol-001-verified-criticals-methodology.md` (iteration-004 candidate, v0.4 baseline per its own Changelog)
**Criticality:** C3 (auto-escalated per c-007 / AE-002 / AE-003)
**Date:** 2026-07-07
**Reviewer:** adv-executor (S-002, blind lane, iteration-004)
**H-16 Compliance:** **Cannot be independently confirmed by this agent.** The launching instructions BLIND this execution from every file under `.../review/iteration-004/` except this report, so this agent cannot read a sibling `s-003-*.md` steelman output to verify H-16 ordering directly. Per the tournament's own Group ordering (Group B — Strengthen, S-003 — precedes Group C — Challenge, S-002 — in `skills/adversary/agents/adv-selector.md`, consistent with the pipeline this very ADR documents at deliverable line 530: `B["Group B - Strengthen<br/>S-003 (H-16)"]` before `C["Group C - Challenge<br/>S-002 / S-004 / S-001"]`), H-16 sequencing is presumed satisfied by orchestration design. **This is an inference (P-022), not a direct verification**, and is flagged here rather than silently assumed.

---

## Summary

4 counter-arguments identified (1 Critical, 3 Major) plus 1 Minor wording note. The ADR's core decision (add an independent, criticality-gated refutation panel) is evidence-grounded and its four prior remediation iterations have already closed most of the obvious gaps in cost, C1-C2 gating, and external-validity disclosure. This pass finds a genuine, previously-unaddressed **internal contradiction between the ADR's own Figure 3 and its RSK-1 risk mitigation #3** (the claimed "recurrence re-surfaces a wrongly-refuted defect" safety net does not exist once the verified protocol is actually running, per the ADR's own corrected diagram) — this is the flagship finding and directly undermines the ADR's honest-bounding claim on false-negative risk. Three further Major findings show (a) RSK-1's "independent lenses" mitigation is in tension with RSK-2's own correlated-error admission, (b) the token-cost formula's worked example silently drops two of its own three declared cost terms, and (c) the WI-8 anti-overfitting safeguard is a single-sample, reactive, post-deployment check being described with more confidence than a single data point can bear. Recommend **REVISE**: none of these findings challenge the D-1..D-6 decisions themselves, but they weaken the ADR's central selling point — that residual risk is *honestly bounded*, not merely disclosed.

---

## Assumption Inventory (Step 2)

| # | Assumption (explicit/implicit) | Challenge |
|---|---------------------------------|-----------|
| A-1 | Explicit: "two of three independent lenses must both fail" (RSK-1 mitigation #1) bounds false-negative risk statistically. | Independence is exactly what RSK-2 disclaims two rows later ("context isolation ... not reasoning independence ... correlated errors"). See DA-002. |
| A-2 | Explicit: "the convergence discriminator (D-4) re-surfaces a genuinely recurring defect in a later round if it is wrongly refuted once" (RSK-1 mitigation #3). | Figure 3's own corrected decision tree shows the recurrence check applies **only in pre-verified/old-protocol mode**; under the running verified protocol there is no recurrence path for REFUTED claims. See DA-001. |
| A-3 | Implicit: the cost-model worked example (~90-105k tokens/report) faithfully instantiates the stated 3-term formula (deliverable + cited-evidence + rubric). | The arithmetic (3 × ~32k) only ever prices the deliverable's own token count; cited-evidence and rubric terms are silently zeroed for a document that itself cites 18 evidence files. See DA-003. |
| A-4 | Implicit: a single non-ADR-genre validation deliverable (WI-8) plus a reactive one-line exemption is adequate protection against the disclosed n=2, "maximally correlated" evidence base (RSK-7). | One additional, un-replicated genre sample does not materially change statistical confidence, and the safeguard only fires *after* the mechanism has already gone live framework-wide. See DA-004. |
| A-5 | Explicit: "C4 all Criticals; C3 Criticals only" (D-1 decision row) implies the two tiers panel differently. | Every other description of the same gate (L1 item 4) states both tiers panel *every claimed Critical*; the only real binary is C1-C2 (no panel) vs. C3/C4 (panel). See DA-005 (Minor). |

---

## Findings Table

| ID | Finding | Severity | Evidence | Affected Dimension |
|----|---------|----------|----------|--------------------|
| DA-001-iter4 | RSK-1 mitigation #3 is contradicted by Figure 3's own corrected recurrence-discriminator scope | Critical | Deliverable lines 616-636 (Fig. 3 source) + line 638 caption vs. line 903 (RSK-1 row) | Internal Consistency / Methodological Rigor |
| DA-002-iter4 | RSK-1 mitigation #1 ("independent lenses") is in tension with RSK-2's own correlated-error admission | Major | Deliverable line 903 (RSK-1) vs. line 904 (RSK-2) | Internal Consistency / Evidence Quality |
| DA-003-iter4 | Token-cost formula's worked example drops 2 of its own 3 declared cost terms | Major | Deliverable lines 791-797 (Cost model paragraph) | Evidence Quality / Actionability |
| DA-004-iter4 | WI-8's single-sample, reactive safeguard is overclaimed as sufficient for the disclosed n=2 "maximally correlated" overfitting risk | Major | Deliverable line 909 (RSK-7) + lines 930-931 (WI-7/WI-8) | Methodological Rigor / Traceability |
| DA-005-iter4 | "C4 all Criticals; C3 Criticals only" implies a proportional gradient that does not exist in the described implementation | Minor | Deliverable line 478 (D-1 decision row) vs. line 751 (L1 item 4) | Traceability / Completeness |

**Finding ID Format:** `DA-{NNN}-iter4` (execution_id = `iter4`, iteration-004 of the ADR-adversary-tournament-protocol-001 tournament).

---

## Finding Details

### DA-001-iter4: RSK-1's "convergence discriminator re-surfaces wrongly-refuted defects" mitigation does not exist once the verified protocol is running [CRITICAL]

**Claim Challenged:** RSK-1 (Verifier leniency false-negative) lists four partial counterweights to a refuted-but-real Critical slipping the gate, the third of which reads: *"the convergence discriminator (D-4) re-surfaces a genuinely recurring defect in a later round if it is wrongly refuted once"* (deliverable line 903).

**Counter-Argument:** The ADR's own Figure 3 — explicitly redrawn in the iteration-2 remediation specifically to fix this exact seam (CV-002-20260707, deliverable line 642: "closing the branch that let a VERIFIED Critical bypass remediation") — shows the recurrence check (`Q2: "Do claimed Criticals RECUR across independent rounds?"`) living **only inside the `PROTO -- "No (old protocol, no panels yet)"` branch** (deliverable lines 616-623). Once `PROTO -- "Yes (verified protocol)"` (line 625), the only downstream questions are `Q1: "Any VERIFIED Criticals this round?"` (line 625) → FIX, or composite-vs-gate (lines 627-628). There is no path in this diagram that re-examines a REFUTED claim's recurrence once the verified protocol is the operating mode. The Figure's own caption states this explicitly: *"the recurrence discriminator applies only in the pre-verified (old-protocol) mode, where it decides whether to switch to the verified protocol; once the verified protocol is running, any VERIFIED Critical routes unconditionally to remediation (FIX)"* (deliverable lines 638-641) — REFUTED claims are conspicuously absent from that sentence, because there is nothing downstream that revisits them.

But the verified protocol is **precisely the only mode in which a REFUTED claim (and therefore a possible false negative) can exist at all** — refutation panels do not run under the old protocol. So the one mitigation RSK-1 cites that is supposed to catch a wrongly-refuted claim describes a mechanism that, per the ADR's own corrected diagram, is switched off in exactly the operating regime where the risk it is meant to mitigate can occur. This is not a hypothetical edge case; it is a structural gap in the ADR's own most safety-critical figure, in the one figure the ADR itself flags as having been fixed for a related reason in iteration 2.

**Impact:** RSK-1 is the highest-consequence risk in the register (MED probability / HIGH impact) and the ADR's central honesty claim is that this residual is "mitigated, not eliminated" by four named counterweights. One of those four (25% of the stated mitigation) does not actually apply during steady-state verified-protocol operation. The honest bound on false-negative risk is therefore weaker than presented: a Critical refuted once under the verified protocol has no described mechanism to be re-caught by recurrence in a later round — it would need to be independently re-raised by a fresh finder pass and re-panelled from scratch, with no cross-round memory feeding the panel's own adjudication.

**Dimension:** Internal Consistency (primary), Methodological Rigor (secondary — the risk register's own citation of D-4 as a mitigation for RSK-1 is not methodologically supported by D-4's actual scope).

**Response Required:** Either (a) explicitly narrow RSK-1 mitigation #3 to state that it applies only during the pre-verified-protocol transition window, not as an ongoing safety net once panels are running, and honestly re-price the residual risk without that counterweight; or (b) add a genuine cross-round recurrence check for REFUTED Criticals under the verified protocol (e.g., persisting refuted-claim fingerprints and flagging a claim refuted 2+ times across independent rounds for mandatory escalation), and reflect that addition in Figure 3.

**Acceptance Criteria:** RSK-1's mitigation list and Figure 3 (source + caption) describe the same, actually-implemented behavior; if a genuine recurrence check for refuted Criticals is added, it appears both in the mermaid source and in L1 Technical Implementation with a concrete mechanism (not merely restated prose).

---

### DA-002-iter4: RSK-1's "independent lenses" claim is undercut by RSK-2's own correlated-error disclosure [MAJOR]

**Claim Challenged:** RSK-1 mitigation #1: *"the 2-of-3 majority means a single lenient lens cannot refute a real Critical — two of three **independent** lenses must both fail"* (deliverable line 903, emphasis added).

**Counter-Argument:** Two rows later, RSK-2 states the opposite property for the identical panel: *"context isolation delivers context independence, not reasoning independence — the lenses run on the same model class, so a systematic model bias can produce correlated errors that blindness alone cannot rule out. The fabricated PR-template claim recurring across four context-isolated rounds is direct evidence of this residual"* (deliverable line 904). RSK-1's statistical argument ("two of three independent lenses must both fail") is only as strong as the independence assumption it rests on; RSK-2 is the ADR's own admission that this assumption does not hold for the failure mode that matters most (shared model bias). Neither risk entry cross-references the other, so a reader who reads RSK-1 in isolation walks away with a stronger confidence in the 2-of-3 rule's protective value than the ADR's own RSK-2 supports two lines down.

**Impact:** This does not invalidate the 2-of-3 majority design (it is still strictly better than a single self-attesting reviewer, and the empirical record shows it worked on the cases observed), but it means RSK-1's own stated mitigation strength is inconsistent with RSK-2's disclosed limitation on the same mechanism, within the same risk register, without acknowledgment.

**Dimension:** Internal Consistency (primary), Evidence Quality (the word "independent" is used as a load-bearing statistical claim without the qualifier RSK-2 supplies elsewhere).

**Response Required:** Qualify RSK-1 mitigation #1 with a forward reference to RSK-2 (e.g., "...though see RSK-2: this independence is architectural/context-based, not a guarantee against correlated model reasoning errors").

**Acceptance Criteria:** RSK-1 and RSK-2 cross-reference each other wherever "independent lenses" is used as a mitigation claim; no unqualified use of "independent" remains in the risk register where correlated-error risk is disclosed elsewhere for the same mechanism.

---

### DA-003-iter4: The token-cost formula's worked example silently drops two of its own three declared terms [MAJOR]

**Claim Challenged:** *"the panel cost ≈ `3 lenses × (deliverable size + cited-evidence size + rubric)` in input tokens. For a ~950-line ADR like this one (~30–35k tokens), that is roughly **90–105k input tokens per Critical-bearing report** (3 × ~32k), before output"* (deliverable lines 794-797).

**Counter-Argument:** The formula names three additive cost components. The worked example collapses to a single number, ~32k tokens per lens, that maps only to "deliverable size" (the ADR's own ~30-35k token count) — there is no separate arithmetic contribution visible for "cited-evidence size" or "rubric." For the factual-accuracy lens specifically, whose entire mandate is "does the claim's cited evidence resolve as stated?" (deliverable line 726), verifying a citation requires opening the cited file — and this ADR alone cites 18 evidence files across two packages (author-notes.md, Evidence Corpus Read table), several of which (e.g., `subtraction-pass-notes.md`, multi-round `s-014-quality-score.md` reports) are substantial documents in their own right. Treating "cited-evidence size" as zero for exactly the genre of artifact (evidence-heavy governance ADR) this cost estimate is anchored to is not a conservative simplification — it is very plausibly the dominant, not negligible, term the formula itself declares.

**Impact:** If cited-evidence reload is anywhere close to the same order of magnitude as the deliverable itself (plausible for a document this citation-dense), true per-lens cost could be 2-5x the stated 90-105k figure, i.e., the "0.4-0.5M input tokens for the Verify stage alone" figure (line 797) is likely a substantial underestimate for exactly the evidence-heavy genre this ADR represents. This affects the Alignment table's "Implementation Effort: M–L aggregate" (line 509) and RSK-4's cost-blowup risk assessment, both of which are downstream consumers of this same cost model.

**Dimension:** Evidence Quality (primary — the numeric claim does not match its own stated formula), Actionability (secondary — WI-8's AC asks to "reconcile the invocation-count and token-cost units" from observed data, which is a good mitigation, but does not fix the pre-existing internal arithmetic gap being carried forward as the ADR's stated estimate in the meantime).

**Response Required:** Either supply a separate, explicit estimate for the cited-evidence term (even order-of-magnitude), or explicitly disclose that the ~90-105k figure is a lower bound that excludes cited-evidence reload, rather than presenting it as the total.

**Acceptance Criteria:** The Cost model section's worked numeric example accounts for, or explicitly and separately discloses the omission of, the cited-evidence and rubric terms it itself declares as part of the formula.

---

### DA-004-iter4: WI-8's single-sample, reactive safeguard is presented with more confidence than one data point supports [MAJOR]

**Claim Challenged:** RSK-7 names the evidence base as "n=2 governance/ADR-genre packages, same author role, same reviewer roster, same project, days apart (maximally correlated, not merely small-n)" and states *"the genuine safeguard against premature over-generalization is the MEDIUM-tier reversibility: any genre where WI-8 (or early field use) shows the protocol underperforms can be exempted by a one-line adv-selector gate edit"* (deliverable line 909); WI-7 (line 930) is gated on WI-8 (line 931), whose AC requires *"at least one validation deliverable MUST be a non-ADR genre."*

**Counter-Argument:** The ADR itself discloses, correctly, that the mechanism (WI-1 through WI-5) "is genre-agnostic and goes live for every C3/C4 tournament of any genre the moment WI-1–WI-5 ship" (RSK-7 text) — i.e., before WI-8 runs. The stated safeguard against the n=2, maximally-correlated evidence base is therefore: (a) reactive (detects underperformance after it has already occurred in production tournaments of unknown genre), and (b) grounded in exactly **one** additional, un-replicated non-ADR sample. Swapping "n=2, maximally correlated" for "n=2 correlated + 1 additional single sample of a different genre" does not materially change the statistical confidence that D-1 through D-6's specific parameter choices (2-of-3 majority, three named lenses, DEFAULT-REFUTED) generalize — a single sample cannot distinguish "this genre behaves like the ADR-genre evidence" from "this genre happened to behave well on this one artifact by chance." Calling this combination "the genuine safeguard" somewhat overclaims what a reactive, one-sample check plus a one-line exemption edit can actually deliver, especially given RSK-7's own probability rating is held at MED only "because the reversible escape-hatch below caps the *cost* of a transfer failure, not its *likelihood*" (line 909) — i.e., the ADR already concedes the safeguard bounds cost, not the probability the DA attack specifically asks about (overfitting risk itself).

**Impact:** This does not argue against shipping the mechanism (the ADR's own disclosure that the escape hatch is cheap and reversible is a legitimate risk-acceptance argument), but the rhetorical framing of WI-8 + exemption as a "genuine safeguard" risks understating, to a reader who does not chase the RSK-7 caveat to its own qualifying clause, how thin the anti-overfitting evidence actually is at the moment of framework-wide rollout.

**Dimension:** Methodological Rigor (the WI-8 validation design does not include a pre-registered falsification criterion beyond "≥1 correctly refuted / ≥1 correctly verified" — a bar a lenient or a strict panel could both clear by chance on a single artifact), Traceability (WI-7/WI-8 dependency is correctly modeled, but the qualitative confidence claimed for a 1-sample gate is not).

**Response Required:** Either commit WI-8 to more than one non-ADR-genre deliverable (even two, from different genres, meaningfully increases the base beyond n=1), or soften "genuine safeguard" language to explicitly state it bounds cost of failure, not likelihood of failure, consistent with the ADR's own RSK-7 probability-rating caveat.

**Acceptance Criteria:** WI-8's AC and RSK-7's mitigation text use consistent, non-overclaiming language about what a single (or the currently-scoped) non-ADR validation sample can and cannot establish.

---

## Recommendations

**P0 (Critical — MUST resolve before acceptance):**
- DA-001-iter4: Reconcile RSK-1 mitigation #3 with Figure 3's actual scope (either narrow the risk-register claim or add a real cross-round recurrence check for refuted Criticals under the verified protocol). Acceptance criteria per [Finding Details](#da-001-iter4-rsk-1s-convergence-discriminator-re-surfaces-wrongly-refuted-defects-mitigation-does-not-exist-once-the-verified-protocol-is-running-critical).

**P1 (Major — SHOULD resolve; require justification if not):**
- DA-002-iter4: Add explicit RSK-1↔RSK-2 cross-reference qualifying "independent lenses."
- DA-003-iter4: Reconcile the cost-model worked example with its own 3-term formula, or explicitly disclose the omission.
- DA-004-iter4: Either strengthen WI-8's non-ADR sample size or soften "genuine safeguard" language to match RSK-7's own cost-vs-likelihood caveat.

**P2 (Minor — MAY resolve; acknowledgment sufficient):**
- DA-005-iter4: Clarify that "C4 all Criticals; C3 Criticals only" describes the same per-Critical panelling rule at both tiers (the real gate is C1-C2 vs. C3/C4), or state explicitly what (if anything) differs between the two tiers' panel scope.

---

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Neutral | No missing sections identified; the ADR's structure is complete against TEMPLATE-FORMAT/Nygard requirements. |
| Internal Consistency | 0.20 | Negative | DA-001, DA-002: two distinct contradictions between the risk register and the ADR's own Figure 3 / RSK-2 disclosure. |
| Methodological Rigor | 0.20 | Negative | DA-001 (mitigation cited does not match diagram), DA-004 (single-sample validation design lacks a pre-registered falsification bar). |
| Evidence Quality | 0.15 | Negative | DA-002 (unqualified independence claim), DA-003 (cost worked-example drops declared terms). |
| Actionability | 0.15 | Negative | DA-003, DA-004: downstream consumers (Alignment table, RSK-4, WI-7 gate) inherit an understated cost figure and an overclaimed validation bar. |
| Traceability | 0.10 | Negative | DA-004 (WI-7/WI-8 dependency correctly modeled but confidence language inconsistent with RSK-7's own caveat); DA-005 (Minor labeling ambiguity between D-1 decision row and L1 item 4). |

**Result:** 1 Critical, 3 Major, 1 Minor. The chosen decisions (D-1 through D-6) are not challenged at the option-selection level — all five findings are internal-consistency and evidence-honesty gaps in how the ADR *bounds and communicates* residual risk and cost, which is precisely the property this ADR claims as its differentiator from the status-quo tournament. Recommend **REVISE**, prioritizing DA-001-iter4 (P0) before re-scoring.
