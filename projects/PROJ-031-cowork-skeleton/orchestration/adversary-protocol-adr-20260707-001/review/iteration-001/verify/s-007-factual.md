# Refutation Panel — Factual-Accuracy Lens

> **Target report:** `projects/PROJ-031-cowork-skeleton/orchestration/adversary-protocol-adr-20260707-001/review/iteration-001/s-007-findings.md` (S-007 Constitutional AI Critique)
> **Deliverable under review:** `projects/PROJ-031-cowork-skeleton/decisions/ADR-adversary-tournament-protocol-001-verified-criticals-methodology.md`
> **Lens:** Factual accuracy — does the claimed defect actually exist at the cited lines? Misreads, stale references, or restatements of disclosed limitations are REFUTED.
> **Method:** Direct line-by-line re-read of every cited ADR location; independent filesystem re-derivation of every empirical file-count claim via Glob + Read (not trusted from the finder's or the ADR's own prose).

---

## CC-001-20260707-iter1 [CRITICAL] — RSK-1 mitigation is the logical inverse of DEFAULT-REFUTED

**Verdict: VERIFIED**

Direct re-read of ADR line 707 confirms the exact quote: "2-of-3 majority + DEFAULT-REFUTED biases toward *keeping* claims; factual lens is evidence-anchored (file+line); anti-leniency mandate inherited from `adv-scorer.md:68-91`; convergence discriminator re-surfaces a genuinely recurring defect in a later round." This is textually present, verbatim, at the RSK-1 row. Cross-checking the ADR's own three other definitions of the same mechanism confirms the contradiction is real, not a finder misread: line 74 ("a claim only counts if two of the three agree (default is: does not count)"), line 381 (D-1 decision row: "2-of-3 majority, **DEFAULT-REFUTED**, blind to each other"), and line 590 ("Default rule: **REFUTED on uncertainty** (the anti-inflation default)"). All three independently define DEFAULT-REFUTED as a discard-biased (anti-inflation) default, directly contradicting line 707's claim that the same mechanism "biases toward *keeping* claims." This is a genuine, self-contained textual inconsistency verifiable without any external file access.

---

## CC-002-20260707-iter1 [CRITICAL] — Verification invocation granularity is self-contradictory and empirically falsified

**Verdict: VERIFIED**

All three cited passages are present as quoted: lines 585-587 ("Invocation contract: one call per lens per Critical-bearing report. Input = the single claimed Critical (id, severity, evidence, affected dimension)..."), lines 624-626 (Cost model: "cost ≈ 3 × (number of claimed Criticals) at C4"), and lines 362-364 (D-6 rationale: "15 refutation-panel files" = 3 lenses × 5 Criticals"). Independent re-derivation (Glob, this review) of `orchestration/adr-convention-20260702-001/adversary/iteration-009/verify/` confirms exactly **15 files** grouped by 5 report-prefixes (`s-001`, `s-002`, `s-004 pre-mortem analysis`, `s-011`, `s-012`) × 3 lens suffixes — matching the finder's count. Reading `s-012-refutation-factual.md` directly confirms one file adjudicates all three of that report's Criticals (012-001, 012-002, 012-003) in a single verdict document, and `iteration-009/s-014-quality-score.md:21` independently states "Ten Critical findings were claimed across the iteration-9 strategy reports (S-001, S-002, S-004, S-011, S-012)" — 10 Criticals across 5 reports, not 5 Criticals. This confirms the finder's core claim: the "15 = 3 lenses × 5 Criticals" label in the ADR's own D-6 rationale is arithmetically wrong (it is 3 lenses × 5 *reports*, holding 10 Criticals), the "Input = the single claimed Critical" (singular) clause contradicts the empirical batched-per-report reality, and the Cost Model formula ("3 × number of claimed Criticals") would require 30 files for 10 Criticals, not the 15 that exist. The three-way contradiction and its empirical falsification both hold up under independent re-verification.

---

## CC-003-20260707-iter1 [MAJOR, verified incidentally] — "18 verification-panel files" for FU-log iteration-008 is false

**Verdict: VERIFIED** (not a Critical per this ADR's own protocol scope, but independently confirmed as part of adjudicating CC-002's supporting evidence)

Independent Glob of `orchestration/fu-log-convention-20260705-001/adversary/iteration-008/verify/` returns exactly **12 files** (4 report-prefixed groups — `s-001 red team analysis`, `s-002`, `s-004 pre-mortem analysis (iteration 8, verified-criticals protocol)`, `s-012 (fmea - failure mode and effects analysis)` — × 3 lenses each). Direct read of `iteration-008/s-014-quality-score.md:36` confirms the source of the "18" error: "18 verification-panel files under `adversary/iteration-008/verify/` (factual / materiality / remediation-value lenses × 4 Critical-bearing reports: S-001, S-002, S-004, S-012)" — 3 × 4 = 12, not 18, an arithmetic error at the cited source that the ADR (line 364) repeats without independent verification. The defect exists exactly as the finder describes.

---

## Summary

| Finder ID | Verdict | Basis |
|---|---|---|
| CC-001-20260707-iter1 | VERIFIED | Line 707 quote confirmed exact; contradicts 3 independently-confirmed other ADR definitions of DEFAULT-REFUTED (lines 74, 381, 590) |
| CC-002-20260707-iter1 | VERIFIED | All 3 cited passages confirmed exact; independent Glob/Read re-derivation confirms 15 files = 5 reports × 3 lenses (not 5 Criticals), confirms per-report batching in `s-012-refutation-factual.md`, confirms 10 Criticals across 5 reports per `s-014-quality-score.md:21` |
| CC-003-20260707-iter1 | VERIFIED (incidental, Major severity) | Independent Glob confirms 12 files; `s-014-quality-score.md:36` confirmed as the arithmetic-error source (3×4=12, not 18) |

**Scope note:** Per this ADR's own D-1 protocol (panels adjudicate Critical-severity claims only), this lens focused primary effort on the two Critical findings (CC-001, CC-002). CC-003 (Major) was independently confirmed as a byproduct of verifying CC-002's supporting evidence and is reported for completeness; CC-004/CC-005 (Minor, naming/traceability) were not adjudicated by this factual lens as they fall outside the Critical-only panel gate.
