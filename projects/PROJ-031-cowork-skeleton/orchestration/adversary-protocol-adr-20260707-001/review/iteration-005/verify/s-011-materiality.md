# Materiality Refutation Panel — S-011 Findings (iteration-005)

**Lens:** Materiality (does the finding genuinely undermine the ADR — wrong decision, unimplementable spec, false evidence? Style/edge-cases REFUTED even if true.)
**Panel scope:** Critical-severity findings only (per protocol; S-011 iteration-005 has exactly one Critical: CV-001-20260707iter5).
**Default:** REFUTED IF UNCERTAIN.

---

## CV-001-20260707iter5 — Fabricated third verification-event in the ADR's own "fabricated-verification incident" case study

**Verdict: VERIFIED**

The claim rests on three independently checkable facts, all confirmed by direct inspection:

1. `orchestration/adr-convention-20260702-001/adversary/iteration-010/post-ceiling-fix-notes.md:57` reads: *"The same 'Glob-verified absent' claim was reaffirmed at iter-6 (FM-010), iter-7 (VQ-019), and carried unchallenged through iter-8/9."* Two named events, no `PM-001-iter007`.
2. `orchestration/adr-convention-20260702-001/adversary/iteration-007/s-004-findings.md:39,49-63` shows the actual content of finding `PM-001-iter007`: a Completeness-dimension gap about the ADR's own Pre-Mortem/Failure-Modes table omitting a compound "nothing lands" scenario (M-2/M-6/M-12 untracked). It has no relationship to `.github/PULL_REQUEST_TEMPLATE.md` or the M-9 atomicity claim.
3. `orchestration/adr-convention-20260702-001/adversary/iteration-010/s-001-findings.md:37` (the primary incident source, quoted in the ADR's own Summary) states: *"survived 9 prior tournament rounds and two independent prior 'Glob-verified absent' checks (S-012 iteration-6 FM-010, S-011 iteration-7 VQ-019)."*

Critically, the ADR's own text is internally inconsistent on this exact fact within the same document under review: RSK-2 (target ADR line 943) reads *"independently re-derived in two context-isolated rounds (iter-6, iter-7) and then persisting unchecked through two more (iter-8, iter-9)"* and Positive Consequence #2 (line 887) reads *"independently re-checked in only two of them, iter-6/iter-7, per CV-001-20260707iter4."* The Changelog itself (v0.5 / iteration-4 remediation entry, target ADR line 1087) explicitly records that `CV-001-iter4` was supposed to have corrected *"reaffirmed across iterations 6, 7, 8, and 9"* to *"2 genuine re-verifications (iter-6/7) + 2 unchecked rounds (iter-8/9)... at the Context incident, RSK-2, and Positive Consequence #2."* The live Context-section text (target ADR lines 225-227, verified by direct read) still reads *"three checks in total: FM-010 at iter-6; PM-001-iter007 and VQ-019 at iter-7"* — meaning the documented remediation was not actually applied at one of its three named sites, and the document now contradicts itself on a load-bearing evidentiary fact.

**Materiality analysis:** This is not a stylistic nit or an edge case. The "fabricated-verification incident" is explicitly named in the ADR's own Decision Rationale as one of the two headline pieces of empirical evidence for the entire methodology's central thesis (independence over self-attestation; the other headline piece is `DA-002-i8`). An ADR whose central argument is "a self-attested 'verified' claim is unreliable; only independent re-checking should be trusted" contains, in the exact paragraph making that argument, a citation to a specific finding ID (`PM-001-iter007`) that does not support the claim attributed to it, and an inflated count (three vs. the two established everywhere else in the same document, including its own changelog's disposition record of a prior fix). This directly damages Evidence Quality and Internal Consistency — two of the six weighted S-014 scoring dimensions — for the artifact's own flagship supporting narrative. It does not change which of the six D-1..D-6 decisions is chosen, but it does constitute false evidence in the document under review, which is one of the three explicit materiality triggers in this panel's charge ("false evidence"). VERIFIED.

---

## Summary

| ID | Severity (finder) | Verdict |
|----|--------------------|---------|
| CV-001-20260707iter5 | Critical | VERIFIED |

**Note on scope:** CV-002-20260707iter5 (citation-line imprecision, Minor severity) is outside this panel's Critical-only adjudication scope per protocol and was not adjudicated here.
