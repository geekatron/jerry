# Factual-Accuracy Refutation Panel: S-011 Chain-of-Verification Findings (Iteration 5)

**Lens:** Factual accuracy (does the defect exist at the cited lines? misreads/stale refs/restatements of disclosed limits are REFUTED)
**Target Report:** `projects/PROJ-031-cowork-skeleton/orchestration/adversary-protocol-adr-20260707-001/review/iteration-005/s-011-findings.md`
**Deliverable:** `projects/PROJ-031-cowork-skeleton/decisions/ADR-adversary-tournament-protocol-001-verified-criticals-methodology.md`
**Panel scope note:** per the ADR's own D-1/c-004 methodology ("panels adjudicate Criticals only"; panels are gated at the report level and only Critical-bearing reports are panelled), this lens's mandatory scope is the report's single Critical, CV-001-20260707iter5. CV-002-20260707iter5 is a Minor finding and outside panel-adjudication scope by the ADR's own design, but is assessed below for completeness since it was reported in the same file.

---

## CV-001-20260707iter5 [CRITICAL] — VERIFIED

**Claim under test:** the ADR's Context section ("fabricated-verification incident" subsection) states "independently re-verified in iterations 6 and 7 (three checks in total: FM-010 at iter-6; PM-001-iter007 and VQ-019 at iter-7)" — and that this "three checks... PM-001-iter007" framing is wrong, since PM-001-iter007 never examines the PR-template claim, and every other source in the corpus (including two the ADR cites for this same fact, and two of the ADR's own other passages) says "two" checks.

**Direct inspection of the deliverable:** Confirmed. `ADR-adversary-tournament-protocol-001-verified-criticals-methodology.md:226` reads exactly: "iterations 6 and 7 (three checks in total: FM-010 at iter-6; PM-001-iter007 and VQ-019 at iter-7)," matching the finder's quote verbatim.

**Direct inspection of cited sources:**
1. `adr-convention-20260702-001/adversary/iteration-010/post-ceiling-fix-notes.md:57` reads: "The same 'Glob-verified absent' claim was reaffirmed at iter-6 (FM-010), iter-7 (VQ-019), and carried unchallenged through iter-8/9." — two events named (FM-010, VQ-019), no mention of PM-001-iter007. Confirmed as cited.
2. `adr-convention-20260702-001/adversary/iteration-007/s-004-findings.md:39,49` (`PM-001-iter007`'s actual content) is titled "Compound non-adoption scenario absent from the ADR's own Pre-Mortem table" and concerns a Completeness gap in the ADR's own 4-row Pre-Mortem/Failure-Modes table (M-2/M-6/M-12 untracked). It has no textual relationship to `.github/PULL_REQUEST_TEMPLATE.md` or the PR-template existence claim. Confirmed unrelated.
3. `adr-convention-20260702-001/adversary/iteration-010/s-001-findings.md:37` (the primary incident source) reads: "survived 9 prior tournament rounds and two independent prior 'Glob-verified absent' checks (S-012 iteration-6 FM-010, S-011 iteration-7 VQ-019)" — two checks, same pair (FM-010, VQ-019). Confirmed as cited.
4. The ADR's own RSK-2 row (`ADR-adversary-tournament-protocol-001-verified-criticals-methodology.md:943`) reads: "independently re-derived in two *context-isolated* rounds (iter-6, iter-7)." The Positive Consequence #2 passage (line 887) reads: "independently re-checked in only two of them, iter-6/iter-7." Both confirm "two," directly contradicting the Context section's "three checks... PM-001-iter007" framing within the same document.

**Determination:** The defect exists exactly as described at the cited line. This is not a misread or a restatement of an already-disclosed limit — it is a genuine internal inconsistency: the same ADR states "two" (RSK-2, Positive Consequence #2, and every external source cited for the fact) and "three... PM-001-iter007" (Context section) for the identical underlying event, and the third named ID does not support the claim attributed to it. **VERIFIED.**

---

## CV-002-20260707iter5 [MINOR] — VERIFIED (out of mandatory panel scope; assessed for completeness)

**Claim under test:** the ADR cites `.../iteration-008/s-014-quality-score.md:68, 75` for "PM-001-iter8... restatement of iteration-3's already-closed FM-006," but the string "FM-006" does not appear at either cited line; it appears at lines 55/174/233 instead.

**Direct inspection:** `fu-log-convention-20260705-001/adversary/iteration-008/s-014-quality-score.md:68` is a Verification-Roll-Up table row for `PM-001-iter8` (disposition REFUTED, 0-of-3) that does not contain the string "FM-006." Line 75 discusses the same tension narratively ("restates a tension... raised, closed, and re-verified as closed in iterations 3, 7, and 8") but likewise does not use the string "FM-006." Line 55 does contain the exact phrase: "PM-001-iter8 (0-of-3 panel lenses; independently re-identified as a restatement of iteration-003's already-closed FM-006)" — confirming the finder's alternate citation (55/174/233) as the correct location.

**Determination:** The underlying fact is true and present in the source document, but not at the cited lines — a genuine citation-locator imprecision, not a misread of substance. **VERIFIED** as an accurate (Minor) finding, though outside this lens's mandatory Critical-only scope.

---

## Summary

| ID | Severity | Verdict |
|----|----------|---------|
| CV-001-20260707iter5 | Critical | VERIFIED |
| CV-002-20260707iter5 | Minor | VERIFIED (out of mandatory scope) |
