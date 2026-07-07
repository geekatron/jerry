# Chain-of-Verification Report: ADR-adversary-tournament-protocol-001 (Verified-Criticals Tournament Methodology)

**Strategy:** S-011 Chain-of-Verification
**Deliverable:** `projects/PROJ-031-cowork-skeleton/decisions/ADR-adversary-tournament-protocol-001-verified-criticals-methodology.md`
**Criticality:** C3
**Date:** 2026-07-07
**Reviewer:** adv-executor (S-011 blind execution, iteration-005)
**H-16 Compliance:** BLIND execution scope restricts reading prior review-iteration artifacts under this review's own `review/iteration-005/` sibling files; S-003 Steelman status against this specific CoVe pass is therefore not independently observable. Proceeding per S-011's indirect-H-16 rule (verification-oriented, not critique-oriented).
**Claims Extracted:** 21 | **Verified:** 19 | **Discrepancies:** 2 (1 Critical, 1 Minor)

## Navigation

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Overall verification assessment |
| [Claim Inventory](#claim-inventory) | All CL-NNN claims extracted and their verification method |
| [Findings Table](#findings-table) | CV-NNN findings |
| [Finding Details](#finding-details) | Expanded evidence per finding |
| [Recommendations](#recommendations) | Corrections by severity |
| [Scoring Impact](#scoring-impact) | S-014 dimension mapping |

---

## Summary

Independent re-verification of 21 testable empirical claims against the primary tournament artifacts (score reports, panel-verdict files, agent/selector source, and live directory listings) confirms 19 claims exactly as stated, including every headline number in the ADR's evidence chain: the 0.66→0.62 ADR-convention spiral, the 0.64→0.65→0.59→0.53→0.468→0.460 FU-log decline (the "ticked up ~0.01 then declined" framing is accurate), the 0.86/0.68, 0.83/0.54, 0.72/0.51, and 0.88/0.68 verified-vs-old-protocol pairs, the exact 5/5, 4/3, 6/1, and 0/6 VERIFIED/REFUTED splits, the 12/15/15/15 panel-file counts (independently confirmed by directory listing, not just quoted score-report text), the DA-002-i8 3-of-3 fix-introduced-regression story, and the `adv-scorer.md:166` / `adv-selector.md:112-128` source citations. All four Mermaid diagrams are internally consistent with their own prose captions and with each other, and all four have persisted `.mmd` + rendered `.svg` pairs as claimed. One **Critical** discrepancy was found: the ADR's own flagship "fabricated-verification incident" narrative — the case study it uses to argue that self-attested verification is unreliable — itself miscounts the independent re-verification events it describes, attributing a check to a finding ID (`PM-001-iter007`) that never examined the claim in question, inflating "two checks" into "three checks" in a way that is internally inconsistent with the ADR's own (already-remediated) RSK-2 and Positive-Consequence-#2 passages. One **Minor** discrepancy (an imprecise line citation, correct substance at different lines in the same file) is also reported. Recommendation: **REVISE** — correct CV-001 before acceptance; CV-002 may be corrected at the author's discretion.

---

## Claim Inventory

| CL-ID | Claim (deliverable text, paraphrased) | Deliverable location | Source Document | Result |
|-------|----------------------------------------|------------------------|------------------|--------|
| CL-001 | Iteration 5 (ADR-convention): score 0.66, REVISE, 10 unresolved Criticals | Context, para 2 | `adr-convention-20260702-001/adversary/iteration-005/s-014-quality-score.md:20,55,47` | VERIFIED |
| CL-002 | Iteration 8 (ADR-convention): score 0.62, REVISE, 10/10 prior Criticals verified closed (8 deletion/2 edit/0 recurred), 7 brand-new Criticals | Context, para 3 | `.../iteration-008/s-014-quality-score.md:23,25,50,195-208` | VERIFIED |
| CL-003 | FU-log iteration 6: score 0.46/0.460, ESCALATE, six consecutive rounds zero regressions, composite drifting 0.468→0.460 | Context, para 4; L0 | `fu-log-convention-20260705-001/adversary/iteration-006/s-014-quality-score.md:19-20,43-45,56` | VERIFIED |
| CL-004 | FU-log 6-round trajectory: "ticked up by about 0.01 in one round before declining across the rest" | L0 | iterations 1-6 `s-014-quality-score.md` headers: 0.64→0.65→0.59→0.53→0.468→0.460 | VERIFIED (0.64→0.65 is the +0.01 tick; monotonic decline thereafter) |
| CL-005 | Iteration 9 (ADR-convention): verified 0.86 vs old-protocol 0.68, 5 VERIFIED / 5 REFUTED of 10 claimed Criticals | Context "verified protocol converges" | `.../iteration-009/s-014-quality-score.md:4,25-37` | VERIFIED |
| CL-006 | Quote: "The ~0.18-point difference between the two protocols is the quantified value of the VERIFIED-CRITICALS refutation panel" | Context, quoted | `.../iteration-009/s-014-quality-score.md:135` | VERIFIED (exact match) |
| CL-007 | FU-log iteration 7: verified 0.83 vs old 0.54, REVISE, 4 VERIFIED of 7 claimed, most material = undisclosed git-history secret-retention gap, after RESTORE closed all 6 iter-6 Criticals w/ zero regression | Context "Reconciling..." | `.../iteration-007/s-014-quality-score.md:20-21,51,65-66,73-77` | VERIFIED |
| CL-008 | FU-log iteration 8: verified 0.72 vs old 0.51, 6 VERIFIED / 1 REFUTED, `DA-002-i8` VERIFIED 3-of-3 (dedup regression), `PM-001-iter8` REFUTED 0-of-3 | Context "Iteration 8 (FU-log)" | `.../iteration-008/s-014-quality-score.md:24,45-46,54-55,66-68,73-75` + `post-tournament-fix-notes.md:37` | VERIFIED |
| CL-009 | Iteration-8 FU-log's own delta table compares against iteration-6 (0.46), silently skipping iteration-7 (0.83) | Context "Reconciling the 0.83→0.72" | `.../iteration-008/s-014-quality-score.md:51,81-89` (Delta Reconciliation section header + rows all read "Prior (iter-6)"; no iteration-7 column/reference anywhere in the report) | VERIFIED — confirmed by direct inspection: the report's own Delta-Reconciliation table and Score-Summary both cite only "Prior Iteration (iteration-006) Composite: 0.460" |
| CL-010 | Iteration 10 (ADR-convention): verified 0.88 vs old 0.68, 0 VERIFIED / 6 REFUTED, RT-M-010 ceiling reached | Context "Iteration 10" | `.../iteration-010/s-014-quality-score.md:22,45,58` | VERIFIED |
| CL-011 | 4 independent strategies re-derive the same grandfather-exemption seam; 3-of-4 factual lenses confirm the tension is real (immaterial); `013-001`'s own factual lens found the tension "is resolved in the same section" | Context "Iteration 10", para 2 | `.../iteration-010/s-014-quality-score.md:47-56` + `.../iteration-010/verify/s-013 inversion technique-refutation-factual.md:26,39` | VERIFIED (exact quote match: "the apparent tension is resolved in the same section") |
| CL-012 | Quote: "Any Critical finding from adv-executor reports → automatic REVISE regardless of score" | Context, quoted | `skills/adversary/agents/adv-scorer.md:166` | VERIFIED (exact match) |
| CL-013 | H-16 ordering + "Group F always last" preserved in adv-selector | c-006 | `skills/adversary/agents/adv-selector.md:112-113 (H-16), :127 (Group F)` | VERIFIED |
| CL-014 | Panel-file counts: iter-9 = 15 files (3×5 reports); FU iter-8 = 12 files (3×4 reports); iter-10 = 15 files; FU iter-7 = 15 files | c-004, D-6 rationale, Cost model | Direct `Glob` of `.../iteration-009/verify/`, `.../fu-log.../iteration-008/verify/`, `.../iteration-010/verify/`, `.../fu-log.../iteration-007/verify/` | VERIFIED — all four counts match directory enumeration exactly (12 and 15 as claimed) |
| CL-015 | Fabricated PR-template claim: `.github/pull_request_template.md` existed since 2026-02-18 (lowercase), falsely claimed absent via an exact-uppercase-case Glob search, exposed in iteration 10 by an ordinary S-001 Red Team pass (`RT-001-iter010`), not the refutation panel | Context "fabricated-verification incident" | `.../iteration-010/post-ceiling-fix-notes.md:41-44,55-61` + `.../iteration-010/s-001-findings.md:20,29,37` | VERIFIED |
| CL-016 | "independently re-verified in iterations 6 and 7 (**three checks in total**: FM-010 at iter-6; **PM-001-iter007** and VQ-019 at iter-7)" | Context "fabricated-verification incident", 2nd paragraph | `.../iteration-010/post-ceiling-fix-notes.md:57`; `.../iteration-007/s-004-findings.md:39,49` (PM-001-iter007's actual content); `.../iteration-010/s-001-findings.md:37` (primary incident source) | **MATERIAL DISCREPANCY — see CV-001** |
| CL-017 | "The same panel REFUTED `PM-001-iter8` 0-of-3 as a restatement of iteration-3's already-closed `FM-006`" cited at `.../iteration-008/s-014-quality-score.md:68, 75` | Context "Iteration 8 (FU-log)", last sentence; also D-2 rationale | `.../fu-log-convention-20260705-001/adversary/iteration-008/s-014-quality-score.md` (fact is true, but at lines 55, 174, 233 — not 68 or 75) | **MINOR DISCREPANCY — see CV-002** |
| CL-018 | All 4 figures rendered/validated with `mmdc` 11.12.0; SVGs persisted alongside sources at `.../adversary-protocol-adr-20260707-001/diagrams/` | Design Diagrams intro | Direct `Glob` of the diagrams directory | VERIFIED — 4 `.mmd` + 4 `.svg` pairs present (fig1-pipeline, fig2-lifecycle, fig3-stopcondition, fig4-iteration) |
| CL-019 | grep across both packages returns 5 `C3` hits, all from S-010 self-refine's own report, FU-log iterations 1-5 | Options D-1, "Why C is chosen" | Spot-checked `fu-log-convention-20260705-001/adversary/iteration-001/s-010-self-refine-findings.md:6,29` (`Criticality: C3`) | VERIFIED (spot-check on iter-1 confirms the pattern; iter-1 iteration-001 `s-014` report independently corroborates: "s-010/self-refine labels C3 — noted as a minor internal labeling inconsistency") |
| CL-020 | RSK-4: "at most 9" finder reports at C4 (Group A-E finder strategies) | RSK-4 mitigation | `skills/adversary/agents/adv-selector.md:118-127` (Groups A-E: 1+1+3+2+2 = 9 strategies) | VERIFIED |
| CL-021 | H-13 (≥0.92), H-14 (min 3 iterations), H-16, RT-M-010 (C1=3/C2=5/C3=7/C4=10) "retained verbatim"; 25/25 HARD-rule ceiling untouched | "What this ADR is NOT" | `.context/rules/quality-enforcement.md` (Quality Gate, HARD Rule Ceiling Derivation sections) | VERIFIED |

**Diagram-vs-prose cross-check (all 4 figures):** Figure 1's `CLAIMS -- "No, or C1-C2" --> F` edge is consistent with its own caption's C1-C2-fallback explanation and with D-2's decision row. Figure 2's `Claimed --> PanelAdjudication: severity == Critical` / `Claimed --> AdvisoryMajorMinor: severity == Major or Minor` states match D-1/D-2. Figure 3's `Q1 -- "Yes: ALWAYS remediate" --> FIX` and the caption's "no VERIFIED Critical can reach the ceiling check without first passing through FIX" are mutually consistent, and match the changelog's own claim (v0.3, CV-002-20260707) that Figure 3 was redrawn to fix exactly this branch. Figure 4's "Finders (adv-executor x9, blind)" is consistent with CL-020 (9 Group A-E strategies). No diagram-prose contradictions found.

---

## Findings Table

| ID | Claim | Source | Discrepancy | Severity | Affected Dimension |
|----|-------|--------|-------------|----------|--------------------|
| CV-001-20260707iter5 | "three checks in total: FM-010 at iter-6; PM-001-iter007 and VQ-019 at iter-7" (Context section, fabricated-verification incident) | `.../iteration-010/post-ceiling-fix-notes.md:57`; `.../iteration-007/s-004-findings.md:39,49`; `.../iteration-010/s-001-findings.md:37` | The ADR asserts a third independent re-verification event (`PM-001-iter007`) of the PR-template-absence claim. That finding ID exists but adjudicates an unrelated Pre-Mortem defect ("compound non-adoption scenario… not present as a unified scenario in the Pre-Mortem/Failure-Modes table") — it never touches the PR-template question. Both proximate sources cited elsewhere in the very same ADR for this incident state **two** checks, not three: `post-ceiling-fix-notes.md:57` itself ("reaffirmed at iter-6 (FM-010), iter-7 (VQ-019)") and the primary incident source `RT-001-iter010` ("two independent prior 'Glob-verified absent' checks (S-012 iteration-6 FM-010, S-011 iteration-7 VQ-019)"). The ADR's own RSK-2 and Positive-Consequence-#2 passages (already touched by the iteration-4 remediation, CV-001-iter4) correctly say "two" (rounds/re-checks) — so the Context-section "three checks... PM-001-iter007" framing is internally inconsistent with the rest of the same document. | Critical | Evidence Quality / Internal Consistency |
| CV-002-20260707iter5 | "The same panel REFUTED `PM-001-iter8` 0-of-3 as a restatement of iteration-3's already-closed `FM-006`" cited at `.../iteration-008/s-014-quality-score.md:68, 75` | `.../fu-log-convention-20260705-001/adversary/iteration-008/s-014-quality-score.md` | The underlying fact is true and appears in the cited file — but at lines 55, 174, and 233, not at the cited lines 68 or 75. Line 68 in the source is an unrelated Verification-Roll-Up table row (`FM-002-i008fmea`); line 75 discusses the same tension narratively but without naming "FM-006" (that exact attribution appears only at lines 55/174/233). | Minor | Evidence Quality |

---

## Finding Details

### CV-001-20260707iter5: Fabricated third verification-event in the ADR's own headline "fabricated-verification incident" case study [CRITICAL]

**Claim (from deliverable):** "The false negative came from an exact-uppercase-case search and was **independently re-verified in iterations 6 and 7 (three checks in total: FM-010 at iter-6; PM-001-iter007 and VQ-019 at iter-7)**, then carried unchallenged — but *not* independently re-checked — through iterations 8 and 9 (`.../iteration-010/post-ceiling-fix-notes.md:57` states exactly this distinction; corrected per CV-001-20260707iter4...)."

**Source Document:** `projects/PROJ-031-cowork-skeleton/orchestration/adr-convention-20260702-001/adversary/iteration-010/post-ceiling-fix-notes.md:57` and `projects/PROJ-031-cowork-skeleton/orchestration/adr-convention-20260702-001/adversary/iteration-007/s-004-findings.md:39,49`.

**Independent Verification:**
1. `post-ceiling-fix-notes.md:57` (the ADR's own cited source for "exactly this distinction") reads: *"The same 'Glob-verified absent' claim was reaffirmed at iter-6 (FM-010), iter-7 (VQ-019), and carried unchallenged through iter-8/9."* This names **two** reaffirmation events (FM-010, VQ-019) — not three, and does not mention `PM-001-iter007` at all.
2. `iteration-007/s-004-findings.md` (the report that actually contains a finding ID `PM-001-iter007`) shows that finding's full text: *"Compound 'nothing lands' scenario (M-2 relocation, M-6 lint, M-12 producer fix all remain untracked/unbuilt) is not modeled as its own row in the ADR's own Pre-Mortem/Failure-Modes table…"* — a Completeness-dimension gap about the Pre-Mortem table's own scenario coverage. It has no relationship whatsoever to `.github/PULL_REQUEST_TEMPLATE.md` or the M-9 atomicity-checklist claim.
3. `iteration-010/s-001-findings.md:37` — the primary source for the entire incident, quoted in the ADR's own Summary — states: *"this execution found one Major, evidence-backed overclaim that survived 9 prior tournament rounds and **two** independent prior 'Glob-verified absent' checks (S-012 iteration-6 FM-010, S-011 iteration-7 VQ-019)."* This is the report that discovered the false claim, and it explicitly counts two prior checks, naming the same two (FM-010, VQ-019) as `post-ceiling-fix-notes.md`.
4. The ADR's own RSK-2 row states: *"The fabricated PR-template claim — independently re-derived in **two** context-isolated rounds (iter-6, iter-7)…"* and Positive Consequence #2 states: *"a false 'verified' assertion persisted through four blind rounds (independently re-checked in only **two** of them, iter-6/iter-7…)."* Both of these passages were explicitly touched by the iteration-4 remediation (per the v0.5 changelog entry, "CV-001-iter4… corrected 'reaffirmed across iterations 6, 7, 8, and 9' to 2 genuine re-verifications (iter-6/7) + 2 unchecked rounds (iter-8/9)… at the Context incident, RSK-2, and Positive Consequence #2"), yet the Context-section passage under review here still reads "three checks... PM-001-iter007" — meaning the iteration-4 fix was applied inconsistently within the very passage it claims to have corrected.

**Discrepancy:** The deliverable's Context section asserts a specific, named third verification event (`PM-001-iter007`) that, on direct inspection of its actual content, never examined the PR-template claim. Every other source in the corpus — including two the ADR itself cites for this exact fact, and two passages within the ADR's own text that this same remediation pass claims to have fixed — states there were **two** independent checks (FM-010 at iter-6; VQ-019 at iter-7), not three.

**Severity:** Critical — this is not a peripheral detail. The "fabricated-verification incident" is one of the ADR's two headline pieces of empirical evidence (alongside `DA-002-i8`) for the entire methodology's central thesis: that self-attested "verified" claims are unreliable and must be independently checked. An ADR whose argument is "verify before you count" contains, in the load-bearing paragraph making that argument, an uncounted/miscounted verification event — the exact failure mode it warns against. It also creates an internal contradiction: the same document says "two" in RSK-2 and Positive Consequence #2, and "three" (with a specific, wrong ID) in the Context section, for the identical underlying fact.

**Dimension:** Evidence Quality (a citation names a specific finding ID that does not support the claim attributed to it) / Internal Consistency (the document contradicts itself on the same fact in three different sections).

**Correction:** In the Context section's "fabricated-verification incident" subsection, change *"independently re-verified in iterations 6 and 7 (three checks in total: FM-010 at iter-6; PM-001-iter007 and VQ-019 at iter-7)"* to *"independently re-verified in iterations 6 and 7 (two checks: FM-010 at iter-6; VQ-019 at iter-7)"* — matching the wording already used correctly in RSK-2 and Positive Consequence #2, and matching both `post-ceiling-fix-notes.md:57` and the primary `RT-001-iter010` source.

---

### CV-002-20260707iter5: Citation-line imprecision for the PM-001-iter8/FM-006 restatement fact [MINOR]

**Claim (from deliverable):** "The same panel **REFUTED `PM-001-iter8` 0-of-3** as a restatement of iteration-3's already-closed `FM-006` (`.../iteration-008/s-014-quality-score.md:68, 75`)." (Context section, and the identical citation recurs at D-2 Rationale.)

**Source Document:** `projects/PROJ-031-cowork-skeleton/orchestration/fu-log-convention-20260705-001/adversary/iteration-008/s-014-quality-score.md`.

**Independent Verification:** The fact itself is true and present in the source file — but not at the cited lines. Line 68 of that file is the Verification-Roll-Up table row for a different finding (`FM-002-i008fmea`). Line 75 discusses the `PM-001-iter8` tension narratively ("restates a tension (CP-01 vs. the P-003 candidate-handoff exception) that was raised, closed, and re-verified as closed in iterations 3, 7, and 8") but does not use the string "FM-006" there. The exact fact as stated in the ADR — "restatement of iteration-3's already-closed FM-006" — appears verbatim at **lines 55, 174, and 233** of the same file (e.g., line 55: "PM-001-iter8 (0-of-3 panel lenses; independently re-identified as a restatement of iteration-003's already-closed FM-006)").

**Discrepancy:** Citation-locator imprecision only; the underlying claim is fully supported by the same source document, just at different line numbers than cited.

**Severity:** Minor — no substantive inaccuracy, only an imprecise pinpoint citation within an otherwise-correct source reference.

**Dimension:** Evidence Quality.

**Correction:** Update the citation from `.../iteration-008/s-014-quality-score.md:68, 75` to `.../iteration-008/s-014-quality-score.md:55` (or `:174` / `:233`) at both occurrences (Context section and D-2 Rationale).

---

## Recommendations

**Critical (MUST correct before acceptance):**
- CV-001-20260707iter5: Correct the "three checks... PM-001-iter007 and VQ-019" framing in the Context section's fabricated-verification-incident paragraph to "two checks: FM-010 at iter-6; VQ-019 at iter-7," aligning it with the ADR's own RSK-2 and Positive Consequence #2 passages and with both cited primary sources.

**Minor (MAY correct):**
- CV-002-20260707iter5: Update the two `s-014-quality-score.md:68, 75` citations (Context section and D-2 Rationale) to the correct line numbers (55/174/233) where the "restatement of iteration-3's already-closed FM-006" fact actually appears.

---

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Neutral | No claims found incomplete; both discrepancies are accuracy/precision issues, not coverage gaps. |
| Internal Consistency | 0.20 | Negative | CV-001-20260707iter5: the Context section's "three checks... PM-001-iter007" directly contradicts the ADR's own RSK-2 ("two context-isolated rounds") and Positive Consequence #2 ("re-checked in only two of them") for the identical fact, within a single document. |
| Methodological Rigor | 0.20 | Neutral | The verification methodology (2-of-3 panels, DEFAULT-REFUTED, blind lenses) is itself well-specified and consistently applied across all cited rounds; the defect is in a narrative citation, not the methodology's design. |
| Evidence Quality | 0.15 | Negative | CV-001-20260707iter5 (a cited finding ID does not support the claim attributed to it, in the ADR's flagship evidence case study) and CV-002-20260707iter5 (imprecise line citation) both reduce confidence in citation accuracy, though 19 of 21 sampled claims verified exactly. |
| Actionability | 0.15 | Positive | Both findings include exact replacement text and precise correction locations; correctable without re-research. |
| Traceability | 0.10 | Negative | CV-001-20260707iter5 breaks the claim→source chain for one of the ADR's two headline evidentiary narratives; the correct chain (FM-010, VQ-019) is fully traceable and well-cited elsewhere in the same document. |

---

## Execution Statistics

- **Total Findings:** 2
- **Critical:** 1
- **Major:** 0
- **Minor:** 1
- **Claims Verified Clean:** 19 of 21 (90.5%)
- **Protocol Steps Completed:** 5 of 5 (Extract Claims, Generate Verification Questions, Independent Verification, Consistency Check, Synthesize and Score Impact)
