# Factual-Lens Refutation Panel: S-011 Chain-of-Verification Findings

**Target:** `projects/PROJ-031-cowork-skeleton/orchestration/adversary-protocol-adr-20260707-001/review/iteration-001/s-011-findings.md`
**Panel Lens:** Factual accuracy (does the cited defect exist at the cited lines? misreads/stale refs/restatements of disclosed limits = REFUTED)
**Default rule:** REFUTED IF UNCERTAIN
**Scope:** Critical-severity findings only (CV-001-20260707-i1, CV-002-20260707-i1)

---

## CV-001-20260707-i1: False "18 verification-panel files" citation

**Verdict: VERIFIED**

Independent `Glob` of `projects/PROJ-031-cowork-skeleton/orchestration/fu-log-convention-20260705-001/adversary/iteration-008/verify/` returns exactly **12 files** (4 Critical-bearing reports x 3 lenses: S-001, S-002, S-004, S-012), not 18. The cited primary source `.../fu-log-convention-20260705-001/adversary/iteration-008/s-014-quality-score.md:36` was read directly and confirms the finder's quote verbatim: "18 verification-panel files under `adversary/iteration-008/verify/` (factual / materiality / remediation-value lenses x 4 Critical-bearing reports: S-001, S-002, S-004, S-012)" — 3 x 4 = 12, arithmetically contradicting its own headline "18" in the same sentence. The ADR text was read directly at the three cited locations (D-6 rationale ~line 362-364, Cost model ~line 624-626, Constraint c-004 ~line 206) and each does propagate "18" (or "~15-18" range) verbatim, exactly as the finder quotes. This is not a misread or a restatement of a disclosed limit; it is a reproducible, tool-verifiable arithmetic error that the finder correctly traced to source and confirmed against the filesystem.

## CV-002-20260707-i1: Invocation-contract granularity contradiction (per-report vs. per-Critical)

**Verdict: VERIFIED**

ADR text read directly confirms all three cited artifacts contain the described language: L1 item 1 states "one call per lens per Critical-bearing report. Input = the single claimed Critical..." (internally juxtaposing report-level cardinality with claim-level singular input); the Cost model paragraph states "cost ≈ 3 x (number of claimed Criticals)" (claim-level formula); and `diagrams/fig4-iteration.mmd:16` (read directly, confirmed byte-for-byte) labels the PANELS lane "3 lenses per Critical<br/>2-of-3, DEFAULT-REFUTED" (claim-level label). Independent `Glob` of both cited empirical panel directories confirms report-level cardinality in practice, not claim-level: FU-log iteration-8 has 7 claimed Criticals (per `s-014-quality-score.md:54-55`: 6 verified + 1 refuted) across 4 reports, yielding 12 files (4x3), not 21 (7x3); ADR-convention iteration-9 has 10 claimed Criticals (per `s-014-quality-score.md:19-37` Panel-Outcome-Reconciliation table, independently counted: 10 rows) across 5 reports (S-001 x2, S-002 x2, S-004 x2, S-011 x1, S-012 x3), yielding 15 files (5x3, confirmed by direct Glob), not 30 (10x3). The claim-level Cost-model formula and Fig. 4 label are therefore falsified by the same empirical evidence the ADR itself cites, while the L1 text's "per report" clause is undermined by its own next clause ("the single claimed Critical," singular). This is a genuine, reproducible internal contradiction, not a misread.

---

## Summary

Both Critical findings under review (CV-001-20260707-i1, CV-002-20260707-i1) hold up under independent factual re-verification: cited line numbers resolve to the quoted text, and independent tool calls (Glob file counts, direct reads of the ADR and both score reports) corroborate the finder's arithmetic and cross-reference claims exactly. Neither finding is a stale reference, a misread, or a restatement of an already-disclosed limitation.
