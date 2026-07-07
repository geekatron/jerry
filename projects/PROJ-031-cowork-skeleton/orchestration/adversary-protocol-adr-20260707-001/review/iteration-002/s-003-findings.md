# Steelman Report: ADR-adversary-tournament-protocol-001 (Verified-Criticals Tournament Methodology)

## Document Sections

| Section | Purpose |
|---------|---------|
| [Steelman Context](#steelman-context) | Deliverable, criticality, strategy metadata |
| [Summary](#summary) | Assessment, improvement count, recommendation |
| [Charitable Interpretation](#charitable-interpretation-step-1) | Core thesis and strongest reading (Step 1) |
| [Weakness Classification](#weakness-classification-step-2) | Presentation vs. structural vs. evidence vs. substantive (Step 2) |
| [Steelman Reconstruction](#steelman-reconstruction-step-3) | Targeted before/after reconstruction of the affected passages |
| [Best Case Scenario](#best-case-scenario-step-4) | Conditions under which the ADR is strongest |
| [Improvement Findings Table](#improvement-findings-table-step-5) | SM-NNN findings with severity |
| [Improvement Details](#improvement-details) | Expanded Critical/Major findings |
| [Scoring Impact](#scoring-impact) | Dimension-level impact of improvements |

---

## Steelman Context

- **Deliverable:** `projects/PROJ-031-cowork-skeleton/decisions/ADR-adversary-tournament-protocol-001-verified-criticals-methodology.md`
- **Deliverable Type:** ADR (Architecture Decision Record), Nygard format, PROPOSED status
- **Criticality Level:** C3 (per task instruction; auto-escalated — new ADR touching `.context/`/`skills/` on implementation, per its own c-007)
- **Strategy:** S-003 (Steelman Technique)
- **SSOT Reference:** `.context/rules/quality-enforcement.md`
- **Steelman By:** adv-executor (S-003) | **Date:** 2026-07-07 | **Original Author:** ps-architect
- **Review round:** Iteration 2 (post iteration-1 remediation: 0.66 → target ≥0.92, per the ADR's own Changelog v0.2 entry)

---

## Summary

**Steelman Assessment:** A genuinely mature, evidence-dense C4/C3 decision record that dogfoods the exact discipline (18-round empirical record, disclosed corrections, subtraction-first doctrine) it proposes to formalize — but its own iteration-1 "standardization" of the verifier cost model introduced a self-contradictory unit-of-work claim that is directly falsifiable against the evidence corpus it cites, and that inconsistency now sits inside the load-bearing implementation spec (D-6, L1, WI-1) rather than in prose color.

**Improvement Count:** 1 Critical, 1 Major, 1 Minor

**Original Strength:** Very high. The Context section's 18-round evidence chain is independently verifiable (spot-checked against `iteration-009/s-014-quality-score.md`, `fu-log .../iteration-008/s-014-quality-score.md`, `iteration-010/post-ceiling-fix-notes.md`, and `subtraction-pass-notes.md`) and every spot-checked claim — the 0.86/0.68 and 0.72/0.51 dual-protocol scores, the 5-VERIFIED/5-REFUTED and 6-VERIFIED/1-REFUTED tallies, the fabricated-PR-template incident, the grandfather-seam recurrence across 4 strategies, and the corrected "12" (not "18") verification-file count for the FU-log iteration-8 round — checks out exactly against the primary-source score reports and panel files. The disclosed-correction footnote in Context and the Changelog v0.2 entry are themselves an instance of the honesty discipline the ADR argues for.

**Recommendation:** Incorporate the SM-001 (Critical) fix before this ADR is exposed to S-002/S-004/S-001 critique — it is exactly the class of defect (a load-bearing quantitative claim, repeated across multiple sections, that contradicts the one artifact that would falsify it) that this very ADR's Context section (RT-001-iter009, FM-001-i8) identifies as the recurring failure mode the verification panel exists to catch. Leaving it in place would let a downstream Devil's Advocate or FMEA pass "discover" a residual of exactly the kind the ADR spent 18 rounds learning to distrust unverified counts about.

---

## Charitable Interpretation (Step 1)

**Core thesis:** A blind adversarial tournament without an independent verification gate does not converge — it manufactures a roughly-constant stream of claimed Critical findings per round regardless of the document's true defect count, can canonize a fabricated claim, and drives scores flat-or-down even under zero regressions. Inserting a criticality-gated, 3-lens, 2-of-3-majority, default-REFUTED refutation panel between the finder groups and the scorer is the single intervention the 18-round record shows reverses this, and five supporting decisions (severity gating, subtraction-first remediation, a convergence discriminator, mandatory delta-reconciliation, and a dedicated blind verifier agent) are the minimum scaffolding that makes the gate coherent.

This thesis is well-supported. Every headline number I independently re-derived from primary sources (not just the ADR's restatement of them) matched: iteration-9's 0.86-vs-0.68 dual-protocol split and 5/5 VERIFIED/REFUTED split (`adr-convention .../iteration-009/s-014-quality-score.md:36-37,45-51`); iteration-8 FU-log's 0.72-vs-0.51 split and 6/1 VERIFIED/REFUTED split, including `DA-002-i8`'s 3-of-3 unanimous verification (`fu-log .../iteration-008/s-014-quality-score.md:45-55,65-71`); the fabricated PR-template claim's four-round survival and iteration-10 factual-lens catch (`.../iteration-010/post-ceiling-fix-notes.md:41-65`); and the four-strategy grandfather-seam recurrence (`.../iteration-010/post-ceiling-fix-notes.md:71-75`, matching the ADR's own citation at line 176). The Context section's "what this ADR is NOT" and the RSK-7 external-validity disclosure (all-C4 evidence base, n=2 correlated packages) are the strongest kind of steelmanning already performed by the author — an evaluator does not need to supply this charity independently because the document already supplies it against itself.

**Strengthening opportunities identified:** the one place the charitable reading strains is the L1/D-6/Cost-model description of *how* the verification panels were actually run empirically, versus how the new `adv-verifier` agent is specified to run. See [Weakness Classification](#weakness-classification-step-2) and [SM-001](#sm-001-invocation-contract-contradicts-its-own-cited-evidence).

---

## Weakness Classification (Step 2)

| Weakness | Type | Magnitude |
|----------|------|-----------|
| L1 item 1 / c-004 / Cost model / D-6 rationale / Fig. 4 label / WI-1 all assert a "3 invocations per lens **per claimed Critical**" unit of work, but the cited empirical file counts (12, 15) and the actual verify-panel files are evidenced at "3 invocations per lens **per Critical-bearing report**" — a different, and in both cited rounds smaller, quantity | Evidence (claim contradicts the very artifact cited to support it) | **Critical** |
| WI-8's acceptance criteria do not require confirming which invocation granularity (per-report vs. per-claimed-Critical) the built `adv-verifier` actually uses, so the SM-001 ambiguity could ship unresolved into the first real implementation | Structural (validation gap for a not-yet-disambiguated design parameter) | Major |
| The Context section's disclosed-correction footnote (lines 163-170) states the "18" figure was corrected to "12" via "direct filesystem enumeration," but does not note that the same source score report's own footer (`fu-log .../iteration-008/s-014-quality-score.md:251`) still carries an uncorrected, differently-wrong "18" arithmetic ("3 lenses × 4 Critical-bearing reports + 2 extra... files" = 14, not 18, and not 12 either) — a minor completeness gap in an otherwise exemplary correction | Evidence (citation hygiene of the corrected source, not the ADR's own claim) | Minor |

All three weaknesses are in **presentation of a factual/quantitative claim**, not in the underlying idea (verification panels are a sound, evidence-supported mechanism). None require rejecting D-1 through D-6; SM-001 requires correcting *how* the chosen implementation is specified to work.

---

## Steelman Reconstruction (Step 3)

> **Scoping note:** given the deliverable is an 866-line ADR and the identified gaps are localized to six specific sites, this reconstruction presents targeted before/after passages (per the Evidence Requirements in Section 5 of the S-003 template) rather than a full-document rewrite. All six sites are listed so the disposition is auditable as a set, exactly the discipline the ADR's own `subtraction-pass-notes.md` disposition tables model.

### Site 1 — Constraint c-004 (line 217)

**Original:**
> "The token cost of verification MUST be proportionate to criticality (panels ≈ 3 agent runs — one per lens — per claimed Critical; panels are *gated* at the report level, i.e., only Critical-bearing reports are panelled)."

**Strengthened [SM-001]:**
> "The token cost of verification MUST be proportionate to criticality (panels ≈ 3 agent runs — one per lens — per Critical-bearing *report*, with every claimed Critical in that report adjudicated individually within the same 3 invocations; panels are *gated and costed* at the report level — this matches the empirical practice in every cited tournament round, see Cost model)."

### Site 2 — D-6 rationale (lines 384-388)

**Original:**
> "the empirical panels are *separate blind files per lens* (`.../iteration-009/`: 15 refutation-panel files = 3 lenses × 5 Criticals; `.../fu-log .../iteration-008/`: 12 verification-panel files = 3 lenses × 4 Criticals)."

**Strengthened [SM-001]:**
> "the empirical panels are *separate blind files per lens, one set per Critical-bearing report* (`.../iteration-009/`: 15 refutation-panel files = 3 lenses × 5 Critical-bearing reports, adjudicating 10 individual claimed Criticals across those reports; `.../fu-log .../iteration-008/`: 12 verification-panel files = 3 lenses × 4 Critical-bearing reports, adjudicating 7 individual claimed Criticals). Each per-report, per-lens file renders an independent VERIFIED/REFUTED verdict for every claimed Critical the target report raised (see e.g. `iteration-009/verify/s-001-refutation-factual.md`, which adjudicates both RT-001-iter009 and RT-002-iter009 in one factual-accuracy pass)."

### Site 3 — L1 Technical Implementation, item 1 (lines 608-613)

**Original:**
> "Invocation contract: the **unit of verification work is one claimed Critical**, adjudicated by **one invocation per lens** — i.e., **3 lens-invocations per claimed Critical** (a report with *k* claimed Criticals produces 3 × *k* verifier runs). Panels are *gated* at the report level (only Critical-bearing reports are panelled), but *costed* per claimed Critical."

**Strengthened [SM-001]:**
> "Invocation contract: the **unit of verification work is one Critical-bearing report**, adjudicated by **one invocation per lens** — i.e., **3 lens-invocations per report**, with each invocation individually adjudicating every claimed Critical that report raised (a report with *k* claimed Criticals still produces 3 verifier runs, each returning *k* verdicts). Panels are *gated and costed* at the report level — this is the invocation contract every cited empirical round actually used, confirmed against the primary verify/ artifacts, not merely their score-report descriptions."

### Site 4 — Cost model paragraph (lines 655-660)

**Original:**
> "panels are *gated* at the report level (only Critical-bearing reports are panelled) and *costed* per claimed Critical. Per round, cost ≈ **3 × (number of claimed Criticals)** at C4, **3 × (number of claimed Criticals)** at C3, **0** at C1–C2 — one invocation per lens per claimed Critical, matching the L1 invocation contract, Fig. 4's "3 lenses per Critical" label, and the `{finding-id}-{lens}.md` output-file naming. Empirically ~**12–15** verifier files per C4 round (iter-8 FU = 3 × 4 = 12; iter-9 = 3 × 5 = 15)."

**Strengthened [SM-001]:**
> "panels are *gated and costed* at the report level (only Critical-bearing reports are panelled). Per round, cost ≈ **3 × (number of Critical-bearing reports)** at C4, same at C3, **0** at C1–C2 — one invocation per lens per report, each invocation adjudicating every claimed Critical in that report and returning one verdict per Critical. Empirically ~**12–15** verifier files per C4 round (iter-8 FU = 3 lenses × 4 reports = 12 files, adjudicating 7 claimed Criticals; iter-9 = 3 lenses × 5 reports = 15 files, adjudicating 10 claimed Criticals) — the file count tracks report count, not claimed-Critical count; a round with the same claimed-Critical total spread across fewer reports costs less, not more."

### Site 5 — Figure 4 label (line 577)

**Original:** `PN["3 lenses per Critical<br/>2-of-3, DEFAULT-REFUTED"]`

**Strengthened [SM-001]:** `PN["3 lenses per Critical-bearing report<br/>(all claimed Criticals in-report), 2-of-3 per finding, DEFAULT-REFUTED"]`

### Site 6 — WI-1 acceptance criteria (line 762)

**Original:**
> "...T1 tools only; H-34 (incl. sub-item b, ex-H-35) schema-valid; **one-invocation-per-lens-per-claimed-Critical contract**; DEFAULT-REFUTED; per-lens verdict files persisted; P-003 self-check present."

**Strengthened [SM-001]:**
> "...T1 tools only; H-34 (incl. sub-item b, ex-H-35) schema-valid; **one-invocation-per-lens-per-Critical-bearing-report contract, adjudicating every claimed Critical in that report to its own verdict**; DEFAULT-REFUTED; per-lens-per-report verdict files persisted with per-finding verdict sections; P-003 self-check present."

---

## Best Case Scenario (Step 4)

**Ideal conditions:** This ADR is strongest when read as what it actually is — a mid-implementation-detail correction to an already-sound architectural decision, not a challenge to the decision itself. The six-decision structure (D-1..D-6) does not depend on invocation granularity; independence, criticality-gating, verified-only severity, subtraction-first remediation, the convergence discriminator, and a dedicated blind agent are all intact regardless of whether the new `adv-verifier` batches all of a report's Criticals into one lens-invocation or splits them one-per-invocation.

**Key assumptions that must hold:** (1) the empirical 12-15 file counts genuinely came from report-level batching (confirmed directly against `iteration-009/verify/s-001-refutation-factual.md` and `fu-log .../iteration-008/verify/s-002-refutation-factual.md`, both of which render two independent per-finding verdicts inside one lens file); (2) no cited empirical round actually used one-invocation-per-claimed-Critical (none of the 27 verify/ files across the two spot-checked rounds is named or scoped to a single finding-id — all are named by report/strategy); (3) the WI-1/WI-2 implementers have not already built a per-claimed-Critical `adv-verifier` from a reading of the current L1 text that would make this correction retroactive rework rather than a pre-implementation fix.

**Confidence:** HIGH that the inconsistency is real and independently verifiable (confirmed by direct Glob + Read of both cited verify/ directories, not by re-reading the ADR's own description of them). MEDIUM-HIGH that the report-level design (my proposed fix) is the correct resolution versus deliberately upgrading to per-claimed-Critical with a disclosed cost increase — this is a legitimate design choice for the ADR's author to make, not one S-003 should force; either resolution closes the finding as long as the chosen granularity is stated once, consistently, and honestly costed.

---

## Improvement Findings Table (Step 5)

| ID | Description | Severity | Original | Strengthened | Dimension |
|----|-------------|----------|----------|---------------|-----------|
| SM-001-20260707T-iter002 | Invocation-contract/cost-model unit-of-work ("per claimed Critical") contradicts the empirical file counts and primary verify/ artifacts cited to support it ("per Critical-bearing report") at 6 sites: c-004, D-6 rationale, L1 item 1, Cost model, Fig. 4 label, WI-1 AC | **Critical** | "3 × (number of claimed Criticals)"; "3 lenses per Critical"; "{finding-id}-{lens}.md" | "3 × (number of Critical-bearing reports)"; "3 lenses per Critical-bearing report"; per-report file with per-finding verdict sections | Internal Consistency, Evidence Quality |
| SM-002-20260707T-iter002 | WI-8 validation-pass acceptance criteria do not require confirming/fixing the invocation granularity before treating the cost model as settled | Major | WI-8 AC: "confirm ≥1 claimed Critical is correctly refuted and ≥1 correctly verified" | Add: "confirm the built `adv-verifier`'s invocation count for the validation round matches the ADR's stated cost formula, and reconcile any mismatch before sign-off" | Actionability, Traceability |
| SM-003-20260707T-iter002 | Context disclosed-correction footnote (18→12) does not flag that its cited source's own footer line still carries a second, differently-inconsistent "18" arithmetic | Minor | Footnote cites only the body-line correction | Footnote could note the footer discrepancy is a source-artifact residual, not re-propagated into this ADR | Traceability |

**Finding ID Format:** `SM-{NNN}-{execution_id}` per template; `execution_id` = `20260707T-iter002` (iteration-2 review pass, 2026-07-07).

---

## Improvement Details

### SM-001: Invocation-contract contradicts its own cited evidence

| Attribute | Value |
|-----------|-------|
| **Severity** | Critical |
| **Affected Dimension** | Internal Consistency (0.20), Evidence Quality (0.15) |
| **Sites** | c-004 (line 217); D-6 rationale (lines 384-388); L1 item 1 (lines 608-613); Cost model (lines 655-660); Fig. 4 label (line 577); WI-1 AC (line 762); Changelog D2 entry (line 858) |

**Original Content:** Six sites in the ADR each assert, in near-identical wording, that the verification unit of work is "one invocation per lens **per claimed Critical**" — i.e., cost = 3 × (number of claimed Criticals) — and cite "iter-8 FU = 3 × 4 = 12" and "iter-9 = 3 × 5 = 15" as the empirical support.

**Strengthened Content:** The same six sites corrected to state the unit of work as "one invocation per lens **per Critical-bearing report**" — cost = 3 × (number of reports) — with the same 12/15 figures now correctly explained by the "4" and "5" being report counts, not claimed-Critical counts.

**Rationale:** I independently verified both cited rounds against primary sources, not the ADR's restatement of them:
- **iteration-9 (adr-convention):** `adr-convention .../iteration-009/s-014-quality-score.md:21` states "**Ten** Critical findings were claimed across the iteration-9 strategy reports (S-001, S-002, S-004, S-011, S-012)" — 10 claimed Criticals, 5 reports. `Glob adr-convention .../iteration-009/verify/*` returns exactly 15 files, one factual/materiality/remediation-value triplet per report (`s-001-*`, `s-002-*`, `s-004 pre-mortem analysis-*`, `s-011-*`, `s-012-*`). Reading `s-001-refutation-factual.md` directly (not the score report's summary of it) shows **one file** renders **two independent verdicts** — `## RT-001-iter009 — VERIFIED` and `## RT-002-iter009 — REFUTED` — both S-001's claimed Criticals in a single factual-accuracy invocation. If the ADR's own "3 × claimed Criticals" formula were what was actually run, iteration-9 would have needed 3 × 10 = 30 files, not 15.
- **iteration-8 (fu-log):** `fu-log .../iteration-008/s-014-quality-score.md` Score Summary lists **7** claimed Criticals (RT-001-20260706-iter8, DA-001-i8, DA-002-i8, PM-001-iter8, PM-002-iter8, FM-001-i008fmea, FM-002-i008fmea) across 4 reports (S-001, S-002, S-004, S-012). `Glob fu-log .../iteration-008/verify/*` returns exactly 12 files (one triplet per report). Reading `s-002-refutation-factual.md` directly shows **one file** adjudicating **both** DA-001-i8 and DA-002-i8. The ADR's own "3 × claimed Criticals" formula would require 3 × 7 = 21 files for this round, not 12.
- The ADR's own Changelog (line 858, entry D2) states this exact figure was a deliberate **iteration-1 remediation**: "standardized the verification unit on one invocation per lens per claimed Critical (3 × claimed Criticals), gated at report level, and made L1 item 1, c-004, the Cost model, Fig. 4's label, and the `{finding-id}-{lens}` file-naming all state it identically." This means the inconsistency was introduced (or entrenched) by the very remediation pass intended to fix a different, adjacent issue (the "18 files" miscount) — the corrected "12"/"15" figures were kept, but the *formula* used to explain them was changed to one the figures do not actually satisfy.

This is precisely the failure class the ADR's own evidence chain warns against (RT-001-iter009: "a load-bearing quantitative claim... repeated as authoritative across 3 locations, was never verified against the one artifact... that would have falsified it" — `iteration-009/s-014-quality-score.md:95`) — now recurring, once, inside the ADR proposing the fix for it.

**Best Case Conditions:** The fix is text-only (six sentence-level edits, no new machinery, no change to D-1 through D-6's chosen options) and is fully consistent with the ADR's own subtraction-first doctrine (D-3) — correct the claim to match the artifact, do not build new machinery to reconcile it.

### SM-002: WI-8 does not gate on resolving the invocation-granularity question

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Affected Dimension** | Actionability (0.15), Traceability (0.10) |
| **Site** | WI-8 row, Work-Item Decomposition table (line 769) |

**Original Content:** WI-8's acceptance criteria require confirming "≥1 claimed Critical is correctly refuted and ≥1 correctly verified" but say nothing about confirming the actual per-round invocation count matches whichever cost formula the ADR ultimately states.

**Strengthened Content:** Add an acceptance-criterion clause: "confirm the built `adv-verifier`'s per-round invocation count matches the ADR's stated cost formula (Cost model); reconcile any mismatch in the ADR or the agent definition before treating WI-8 as passed."

**Rationale:** Without this, WI-1 could be implemented literally per the (currently incorrect) L1 spec — one invocation per lens per claimed Critical — and WI-8's validation pass would still "pass" (it only checks verdict correctness, not invocation count), silently doubling the token cost c-004 was meant to bound, with no acceptance gate positioned to catch it.

**Best Case Conditions:** This is a one-clause addition to an already-PROPOSED work item; it does not add a new work item or change WI-8's sizing.

---

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Neutral | Not affected by SM-001/SM-002; the six-decision structure remains complete either way. |
| Internal Consistency | 0.20 | **Positive** | SM-001 directly closes a 6-site self-contradiction between the stated cost formula and its own cited worked examples. |
| Methodological Rigor | 0.20 | Positive | SM-002 closes a validation-gate gap so WI-8 actually tests the parameter the ADR is least certain about. |
| Evidence Quality | 0.15 | **Positive** | SM-001 makes the "12"/"15" citations actually support the claim they are attached to, rather than supporting a different (report-level) claim by coincidence. |
| Actionability | 0.15 | Positive | SM-002 gives WI-1/WI-8 implementers an unambiguous, checkable invocation contract instead of one contradicted by the ADR's own evidence. |
| Traceability | 0.10 | Neutral/Positive | SM-003 is a minor, non-blocking hygiene note on the corrected source citation. |

---

*Strategy: S-003 (Steelman Technique) | Template: `.context/templates/adversarial/s-003-steelman.md` | H-16: this output is intended to precede any S-002/S-004/S-001 pass in this iteration's tournament sequence.*
*Constitutional: P-003 no subagents invoked. P-020: all writes confined to `projects/PROJ-031-cowork-skeleton/`. P-022: every SM-NNN finding cites file+line or independently-reproduced Glob/Read evidence; inference is labeled where used (e.g., "confidence: MEDIUM-HIGH" on the recommended resolution direction).*
*Hygiene: zero absolute home-directory paths; zero employer-internal tokens; all paths repo-relative.*
