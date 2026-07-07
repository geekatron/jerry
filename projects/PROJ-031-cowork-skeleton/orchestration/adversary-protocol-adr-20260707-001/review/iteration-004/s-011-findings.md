# Chain-of-Verification Report: ADR-adversary-tournament-protocol-001 (iteration 4)

## Navigation

| Section | Purpose |
|---------|---------|
| [Header](#header) | Execution metadata |
| [Summary](#summary) | Overall assessment |
| [Findings Table](#findings-table) | All CV-NNN findings |
| [Finding Details](#finding-details) | Expanded evidence for Critical/Major findings |
| [Verification Log (Clean)](#verification-log-clean) | Claims independently re-checked and confirmed accurate |
| [Recommendations](#recommendations) | Corrections by severity |
| [Scoring Impact](#scoring-impact) | Dimension-level impact mapping |
| [Execution Statistics](#execution-statistics) | Counts |

---

## Header

**Strategy:** S-011 Chain-of-Verification
**Deliverable:** `projects/PROJ-031-cowork-skeleton/decisions/ADR-adversary-tournament-protocol-001-verified-criticals-methodology.md`
**Criticality:** C3 (per commission)
**Date:** 2026-07-07
**Reviewer:** adv-executor (S-011, iteration 4, blind — no sibling iteration-004 files read)
**H-16 Compliance:** S-003 Steelman status not visible to this blind executor (prior-iteration outputs under `review/iteration-004/` excluded per protocol, and the ADR's own H-16-embedded steelman structure — Options Considered leading with a steelman of the rejected option — was read directly in the deliverable). S-011's H-16 compliance is indirect per its template; proceeding without independent confirmation of a discrete S-003 artifact for this iteration.
**Claims Extracted:** 22 | **Verified:** 20 | **Discrepancies:** 2 (1 Major, 1 Minor)

---

## Summary

Independent re-verification against the primary tournament-evidence corpus (`adr-convention-20260702-001/`, `fu-log-convention-20260705-001/`) found this ADR to be **exceptionally well-supported by evidence**. Every checked numeric claim (composite scores, verified/refuted Critical counts, panel file counts, delta figures, disposition tallies) matched the cited source files exactly, including several deliberately-precise figures (the "12" vs "18" panel-file disclosed correction, the 0.66→0.68→0.72→0.83→0.86→0.88 score chain, the "5 C3 hits" grep claim, the −0.04 and +0.01 delta figures). Two independent adversary-thread tournaments (10 ADR-convention rounds + 8 FU-log rounds = 18) were cross-checked and the ADR's arithmetic and quoted language trace cleanly to file+line sources.

One **Major** discrepancy was found: the ADR's fabricated-verification-incident narrative overstates how many tournament rounds *actively re-confirmed* the false "no PR template exists" claim. The ADR states it was "reaffirmed across iterations 6, 7, 8, and 9," but the evidence corpus shows independent re-verification only occurred in iterations 6 and 7 — iteration 8 merely cites the deferred item in passing (no fresh check performed), and iteration 9 contains zero mentions of the claim at all. The ADR's own primary source (`post-ceiling-fix-notes.md:57`) is more precise than the ADR itself on this exact point, distinguishing "reaffirmed at iter-6, iter-7" from "carried unchallenged through iter-8/9" — a distinction the ADR's Context section and RSK-2 collapse.

One **Minor** citation-precision issue was found in a line-range citation.

**Recommendation:** REVISE (targeted correction of the fabricated-claim reaffirmation count; does not affect the ADR's core decision, HARD-rule compliance, or overall evidentiary integrity, which is otherwise very strong).

---

## Findings Table

| ID | Claim | Source | Discrepancy | Severity | Affected Dimension |
|----|-------|--------|-------------|----------|--------------------|
| CV-001-20260707iter4 | "The false negative...was reaffirmed across iterations 6, 7, 8, and 9" (Context, fabricated-verification incident) | `post-ceiling-fix-notes.md:57` (ADR-convention, iteration-010); direct corpus search of iteration-008 and iteration-009 report sets | Only iterations 6 and 7 show independent re-verification of the absence claim (S-012 iter-6 FM-010; S-004 + S-011 iter-7). Iteration 8 has one passing citation with no fresh check; iteration 9 has zero mentions. | Major | Evidence Quality |
| CV-002-20260707iter4 | "the unconditional rule at lines 166–167" quoting "Any Critical finding from adv-executor reports → automatic REVISE regardless of score" | `skills/adversary/agents/adv-scorer.md:166` | The quoted single-line rule is at line 166 only; line 167 is a distinct special case ("Score >= 0.92 but with unresolved Critical findings → REVISE"). Citing a 2-line range for a 1-line quote is imprecise, not wrong. | Minor | Traceability |

---

## Finding Details

### CV-001-20260707iter4: Fabricated-claim "reaffirmed" count overstates independent re-verification in iterations 8–9 [MAJOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Major |
| **Section** | Context → "Evidence chain — the fabricated-verification incident" (deliverable lines ~217–238); also echoed in Positive Consequence #2 ("survived four blind rounds") and RSK-2 ("recurring across four context-isolated rounds") |
| **Strategy Step** | Step 3 (Independent Verification) + Step 4 (Consistency Check) |

**Claim (from deliverable):** "The false negative came from an exact-uppercase-case search and was **reaffirmed across iterations 6, 7, and 8, and 9**." (paraphrase-exact: "reaffirmed across iterations 6, 7, 8, and 9"). Related language elsewhere in the same ADR: "a false 'verified' assertion survived four blind rounds and was exposed only incidentally" (Decision Rationale) and "the fabricated PR-template claim **recurring across four context-isolated rounds** is direct evidence of this residual" (RSK-2).

**Independent Verification (source-by-source):**
- **Iteration 6** (`adr-convention-20260702-001/adversary/iteration-006/s-012-findings.md`, FM-010): independently re-verified — this strategy performed and reported its own Glob check ("Glob-verified absent"). Counts as a genuine independent reaffirmation.
- **Iteration 7**: TWO independent reaffirmations exist — `adversary/iteration-007/s-004-findings.md:55` (PM-001-iter007) explicitly states `Glob(".github/PULL_REQUEST_TEMPLATE.md") returns no match`, and `adversary/iteration-007/s-011-findings.md` (VQ-019, cited by the ADR itself) independently confirms "absent." Both are genuine, independent re-verifications.
- **Iteration 8**: searched the complete `iteration-008/` report set (all 9 finder reports + the score report) for any mention of "PULL_REQUEST_TEMPLATE," "pull_request_template," "FM-010," or "VQ-019." The only hit is `adversary/iteration-008/s-013-findings.md:59` (IN-003-20260706), which merely *cites* "M-10, FM-010 'not yet instrumented' PR-template" as background context for a different finding (whether the R-B citation-sweep residual will actually be executed) — it performs **no independent Glob/filesystem check** of the PR-template's existence. This is not a reaffirmation of the absence claim; it is a passing reference to the already-recorded (false) disposition.
- **Iteration 9**: searched the complete `iteration-009/` report set (all finder reports, score report, and all 15 verify-panel files) for the same terms. **Zero matches.** No strategy or panel in iteration 9 mentions the PR-template claim in any form.
- **Corroborating source:** the ADR's own primary evidence file, `adr-convention-20260702-001/adversary/iteration-010/post-ceiling-fix-notes.md:57`, states this precisely and more conservatively than the ADR itself: *"The same 'Glob-verified absent' claim was **reaffirmed** at iter-6 (FM-010), iter-7 (VQ-019), and **carried unchallenged through iter-8/9**."* This source explicitly distinguishes active reaffirmation (6, 7) from mere unchallenged persistence in the text (8, 9) — a distinction the ADR's own Context section and RSK-2 do not preserve.

**Discrepancy:** The ADR states the false claim was "reaffirmed across iterations 6, 7, 8, and 9" and, elsewhere, that it "recurred across four context-isolated rounds" / "survived four blind rounds" — phrasing that implies active, repeated independent re-confirmation in all four rounds. The evidence supports active reaffirmation in only 2 of the 4 named rounds (6 and 7, with iteration 7 itself containing two independent instances). Iterations 8 and 9 show the claim merely remaining unedited in the deliverable text, not being independently re-checked and re-confirmed.

**Severity:** Major — this does not invalidate the ADR's core decision (the underlying lesson that blind-independence catches self-attestation failures is still true and evidenced by the two genuine reaffirmations plus the iteration-10 catch). However, it materially overstates the evidentiary support for RSK-2's "correlated error" framing (which explicitly leans on "recurring across four context-isolated rounds" as "direct evidence" of a residual risk) and for the general severity framing of the incident. Because this ADR's central thesis is that unverified claims should not be propagated at face value, an unverified overstatement of its own evidentiary record is a notable internal-consistency and evidence-quality gap — the exact failure mode the ADR argues against, recurring at one level removed.

**Correction:** Replace "reaffirmed across iterations 6, 7, and 8, and 9" with an accurate framing, e.g.: "reaffirmed by independent checks in iterations 6 and 7 (three total independent re-verifications: FM-010 iter-6, PM-001-iter007 and VQ-019 iter-7), and left uncorrected — though not independently re-checked — through iterations 8 and 9." Apply the same correction to RSK-2 ("recurring across four context-isolated rounds" → "recurring across two independently-checked rounds and persisting unchecked through two more") and to the Decision Rationale's "survived four blind rounds" (defensible as-is if read as "the false text persisted through four rounds," but should be disambiguated from "reaffirmed," which the ADR uses interchangeably in the same passage).

---

### CV-002-20260707iter4: Line-range citation broader than the quoted text [MINOR]

| Attribute | Value |
|-----------|-------|
| **Severity** | Minor |
| **Section** | Context → "The problem being solved" (deliverable, citation "`skills/adversary/agents/adv-scorer.md:166-167`") |
| **Strategy Step** | Step 3 (Independent Verification) |

**Claim (from deliverable):** "The current acceptance rule is unconditional: *'Any Critical finding from adv-executor reports → automatic REVISE regardless of score'* (`skills/adversary/agents/adv-scorer.md:166-167`)."

**Independent Verification:** Read `skills/adversary/agents/adv-scorer.md` lines 155–168. Line 166 reads exactly: "Any Critical finding from adv-executor reports → automatic REVISE regardless of score". Line 167 is a distinct rule: "Score >= 0.92 but with unresolved Critical findings → REVISE (annotate in L0 summary...)".

**Discrepancy:** The quoted sentence is entirely contained on line 166; the citation range "166-167" additionally spans a different (related but separate) special-case rule. Not a factual error — both lines are part of the same "Special cases" bullet list the ADR is characterizing — but a reader checking the exact quote against the exact line range would find the quote only at 166, not spanning to 167.

**Severity:** Minor — no correction changes any argument or figure in the ADR; this is a citation-precision nit.

**Correction:** Cite `adv-scorer.md:166` for the exact quote, or if the intent is to reference the whole "Special cases" list as context, note that explicitly (e.g., "adv-scorer.md:166, first of three special cases at 166-168").

---

## Verification Log (Clean)

The following claims were independently re-checked against the primary evidence corpus and found **accurate** — listed to document verification scope, not as findings:

| Claim | Source Checked | Result |
|---|---|---|
| Iteration 5 (ADR-convention): score 0.66 REVISE, "10 unresolved Criticals" from "four independent blind reviewers" | `iteration-005/s-014-quality-score.md:20,22,36-47,186-205` | Exact match — Score 0.66, 10 Criticals from S-001/S-004/S-012/S-013 (4 strategies) |
| "each addition became new attack surface — the reviewers then attacked the additions" | `subtraction-pass-notes.md:28` | Verbatim match at line 28 |
| Iteration 8 (ADR-convention): score 0.62 REVISE; "10 of 10 prior Criticals verified closed (8 CLOSED-BY-DELETION, 2 CLOSED-BY-EDIT); 0 recurred"; 7 new Criticals | `iteration-008/s-014-quality-score.md:23,50,58,195-208` | Exact match |
| "scored independently from current-iteration evidence, then compared" | `iteration-008/s-014-quality-score.md:214` | Verbatim match |
| −0.04 composite move explained as "not remediation regressing" | `iteration-008/s-014-quality-score.md:222` | Verbatim match (0.66→0.62 = −0.04) |
| Iteration 9 (ADR-convention): verified 0.86 vs old-protocol 0.68; 10 claimed, 5 VERIFIED / 5 REFUTED | `iteration-009/s-014-quality-score.md:4,36-37,45-46` | Exact match |
| "The ~0.18-point difference between the two protocols is the quantified value of the VERIFIED-CRITICALS refutation panel" | `iteration-009/s-014-quality-score.md:135` | Verbatim match (0.86−0.68=0.18) |
| Iteration 10 (ADR-convention): verified 0.88, 0 VERIFIED / 6 REFUTED, RT-M-010 C4 ceiling (10th round) | `iteration-010/s-014-quality-score.md:22,45,58,66-71` | Exact match |
| Iteration 10: 4 strategies re-derived grandfather seam (002-001, 012-004, 013-001, CV-001-i010); 3 VERIFIED at factual layer, 013-001 REFUTED even at factual lens | `iteration-010/s-014-quality-score.md:49-56`; `iteration-010/verify/s-013 inversion technique-refutation-factual.md` | Exact match — 013-001 factual verdict is explicitly REFUTED, not merely non-material |
| Disclosed correction: "18 verification-panel files" → corrected to "12" (3 lenses × 4 reports, FU-log iteration 8) | Direct `Glob` of `fu-log-convention-20260705-001/adversary/iteration-008/verify/` | Exactly 12 files found (s-001, s-002, s-004, s-012 × 3 lenses). Confirms the ADR's disclosed correction is accurate — the source score report's own footer ("18...3×4+2 extra") is itself arithmetically inconsistent (3×4+2=14≠18) and is correctly *not* re-propagated |
| Iteration 9 (ADR-convention): 15 panel files = 3 lenses × 5 reports | Direct `Glob` of `adr-convention-20260702-001/adversary/iteration-009/verify/` | Exactly 15 files (s-001, s-002, s-004, s-011, s-012 × 3 lenses) |
| Iteration 7 (FU-log): verified 0.83 vs old-protocol 0.54; VERIFIED 4 / REFUTED 3; most material finding FM-001-i7fmea (git-history secret-retention gap) | `fu-log-convention-20260705-001/adversary/iteration-007/s-014-quality-score.md:20,43-56,65-76` | Exact match |
| Iteration 8 (FU-log): verified 0.72 vs old 0.51; DA-002-i8 VERIFIED 3-of-3 (regression introduced by iteration-6's own FM-001-i6 dedup fix); PM-001-iter8 REFUTED 0-of-3 as restatement of iteration-3's FM-006 | `fu-log-convention-20260705-001/adversary/iteration-008/s-014-quality-score.md:45-55,169-174`; `iteration-008/s-002-findings.md:50,83-99` | Exact match; DA-002-i8 confirmed as a defect in the mechanism iteration-6's FM-001-i6 fix introduced |
| Iteration 6 (FU-log): score 0.460 ESCALATE, prior 0.468, six consecutive rounds; L0's "ticked up ~0.01 once then declined" | `fu-log-convention-20260705-001/adversary/iteration-00{1..6}/s-014-quality-score.md` composite figures: 0.64, 0.65, 0.59, 0.53, 0.468, 0.460 | Exact match — iter1→2 delta is +0.01 (the single "tick up"), all subsequent deltas negative |
| Fabricated Glob incident: exact-case `.github/PULL_REQUEST_TEMPLATE.md` absent; lowercase `.github/pull_request_template.md` exists; existed since 2026-02-18 | Direct `Glob` (both casings, this session); `iteration-010/post-ceiling-fix-notes.md:37-43` (`git log --diff-filter=A`) | Confirmed — uppercase form absent, lowercase form exists; first-commit date independently git-verified by the source's own owner pass |
| "a grep across every Criticality Level declaration in both packages returns five C3 hits, all from S-010 self-refine's own report in FU-log iterations 1-5" | Direct `Grep` of `Criticality` across all `s-010*.md` files in both threads | Confirmed — FU-log iterations 1–5 each declare "C3"; ADR-convention's own S-010 reports declare C4 in every iteration except iteration-6 ("C3+", a distinct hybrid label, defensibly excluded from a strict "=C3" match) |
| D-6 rationale: iteration-9 panel files are per-report (not per-finding) — one file adjudicates multiple claimed Criticals (e.g. RT-001/RT-002-iter009 in one factual pass) | `iteration-009/verify/s-001-refutation-factual.md` | Confirmed |
| Figure 3 redraw: under the verified protocol, any VERIFIED Critical routes unconditionally to FIX (no bypass to the ceiling check) | Deliverable Figure 3 mermaid source (lines ~616–636) | Diagram matches caption and prose exactly — the `PROTO -- "Yes" --> Q1` branch's only two exits are FIX or PASS/BAND, never directly to the ceiling check |
| adv-scorer.md verdict-band table (>=0.92 PASS, 0.85-0.91 REVISE, 0.70-0.84 REVISE, 0.50-0.69 REVISE, <0.50 ESCALATE) | `skills/adversary/agents/adv-scorer.md:157-163` | Exact match to the operational bands the cited score reports apply |

---

## Recommendations

**Major (SHOULD correct before acceptance):**
- CV-001-20260707iter4: Correct the "reaffirmed across iterations 6, 7, 8, and 9" claim (Context section) and its echoes in Positive Consequence #2 and RSK-2 to accurately distinguish the 2–3 genuine independent reaffirmations (iter-6 FM-010; iter-7 PM-001-iter007 and VQ-019) from the 2 rounds (8, 9) where the claim simply went unchallenged/unchecked. Source for the corrected framing: `post-ceiling-fix-notes.md:57`, which already states this distinction precisely.

**Minor (MAY correct):**
- CV-002-20260707iter4: Narrow the `adv-scorer.md:166-167` citation to `:166` for the exact quote, or clarify the range is intentionally inclusive of the adjacent special case.

---

## Scoring Impact

Map to S-014 scoring dimensions (Completeness 0.20, Internal Consistency 0.20, Methodological Rigor 0.20, Evidence Quality 0.15, Actionability 0.15, Traceability 0.10):

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Neutral | No claims found incomplete; the 18-round evidence chain is thoroughly covered. |
| Internal Consistency | 0.20 | Negative (minor) | CV-001: the "reaffirmed...6,7,8,9" framing is inconsistent with the ADR's own cited source (`post-ceiling-fix-notes.md:57`), which states the more precise 6/7-vs-8/9 distinction. |
| Methodological Rigor | 0.20 | Neutral | The verification-methodology narrative (independence, 2-of-3 majority, DEFAULT-REFUTED) is accurately and rigorously described everywhere else checked. |
| Evidence Quality | 0.15 | Negative | CV-001: an evidentiary overstatement in a document whose central thesis is "verify before propagating a claim." CV-002: trivial citation-range imprecision. |
| Actionability | 0.15 | Positive | Both findings have exact, mechanical corrections (reword one sentence; narrow one citation range) requiring no further research. |
| Traceability | 0.10 | Negative (minor) | CV-002: citation range slightly broader than the quoted text. |

---

## Execution Statistics

- **Total Findings:** 2
- **Critical:** 0
- **Major:** 1
- **Minor:** 1
- **Protocol Steps Completed:** 5 of 5 (Extract Claims; Generate Verification Questions; Independent Verification; Consistency Check; Synthesize and Score Impact)
- **Claims independently re-verified against primary sources:** 22 (20 clean / 2 discrepant)
