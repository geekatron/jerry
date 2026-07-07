# Refutation Panel — Remediation-Value Lens

## Navigation

| Section | Purpose |
|---------|---------|
| [Header](#header) | Execution metadata |
| [Verdicts](#verdicts) | Per-finding VERIFIED/REFUTED with evidence |
| [Scope Note](#scope-note) | Why only the Critical finding is adjudicated |
| [Summary](#summary) | Structured output preview |

---

## Header

**Strategy lens:** Remediation-Value (3rd of 3 refutation-panel lenses)
**Target report:** `projects/PROJ-031-cowork-skeleton/orchestration/adversary-protocol-adr-20260707-001/review/iteration-003/s-011-findings.md` (S-011 Chain-of-Verification, iteration 3)
**Deliverable under review:** `projects/PROJ-031-cowork-skeleton/decisions/ADR-adversary-tournament-protocol-001-verified-criticals-methodology.md`
**Question this lens answers:** If the finding's proposed correction were applied, would it materially improve the decision record's quality — or is it churn / machinery-adding that would not change how a reader should trust or act on the document?
**Default rule:** REFUTED if uncertain.
**Blind execution:** No access to sibling factual-accuracy or materiality panel outputs for this iteration.

---

## Verdicts

### CV-001-20260707iter3 — VERIFIED

**Claim under review:** The ADR's L0 ("moved scores from a misleading 0.68 up to an honest 0.86–0.88... proven across four later rounds") and its Context "evidence chain — the verified protocol converges" subsection omit FU-log iteration-007 (composite 0.83, VERIFIED-CRITICALS protocol vs. 0.54 old-protocol), the fourth round the "four later rounds" language implicitly requires, and never reconcile the 0.83 → 0.72 decline into iteration-008 under the identical protocol.

**Independent re-check:** `orchestration/fu-log-convention-20260705-001/adversary/iteration-007/s-014-quality-score.md:20-21` confirms `Score: 0.83/1.00 (VERIFIED-CRITICALS protocol) | Verdict: REVISE` and `Composite (naive, old-protocol...): 0.54` (line 66). A full-text grep of the ADR (`decisions/ADR-adversary-tournament-protocol-001-verified-criticals-methodology.md`) for `iteration-007`, `iter-7`, `iter7`, and `0.83` returns zero hits — the round is genuinely absent from the document, not merely under-cited. Iteration-008's own reconciliation (`.../iteration-008/s-014-quality-score.md:51-52, 205-217`) reconciles explicitly against iteration-006 (0.460), never against iteration-007 (0.83), despite iteration-008 listing `iteration-007/restore-notes.md` as a read input — so the 0.83→0.72 movement is genuinely never explained anywhere in the corpus, not just in the ADR's summary of it.

**Remediation-value assessment:** This is not narrative polish. The ADR's central, self-declared thesis is that unreconciled round-over-round score movement is exactly the failure mode the new protocol (specifically D-5, mandatory delta-reconciliation) exists to eliminate going forward — and this ADR's own headline evidentiary claim ("0.86–0.88... four later rounds") is falsified by one of its own four constituent data points (0.83, outside the cited range) sitting next to an unexplained same-protocol decline (0.83→0.72) that the document neither names nor reconciles. A reader ratifying a C3+ governance ADR on the strength of "the fix was proven across four later rounds, converging to 0.86–0.88" is being given a range that is both numerically wrong and silent about the one data point most in tension with the "converges" framing. The prescribed fix (cite iteration-007, and either explain the decline or widen the claimed range to the true 0.72–0.88 dispersion) is a single paragraph — low implementation cost — but it closes a genuine evidence-integrity gap in a document whose entire subject is trustworthy evidence chains. This is squarely the kind of fix that changes what a reader takes away from the L0/Context, not cosmetic churn.

**File+line evidence:** `orchestration/fu-log-convention-20260705-001/adversary/iteration-007/s-014-quality-score.md:20-21,66`; `orchestration/fu-log-convention-20260705-001/adversary/iteration-008/s-014-quality-score.md:36,51-52,205-217`; ADR full-text grep (`iteration-007`, `0.83`) = 0 hits.

---

## Scope Note

Per the ADR's own D-1/D-6 design (`decisions/ADR-adversary-tournament-protocol-001-verified-criticals-methodology.md`, "Options Considered" D-1 and "L1 Technical Implementation" invocation contract), refutation panels adjudicate **Critical-severity claims only**; Majors are advisory and are not gated into a panel. CV-002-20260707iter3 in the target report is explicitly classified **Major** (Findings Table, Scoring Impact table). It is therefore out of this lens's adjudication scope and receives no VERIFIED/REFUTED verdict here, consistent with the protocol the target ADR itself specifies. (Advisory note only, not a verdict: the same full-text grep confirms the FU-log `Criticality Level` lines cited by CV-002 do contain the literal string `C3` in 5 files, so the underlying factual observation is not in dispute — this note does not adjudicate its remediation value.)

---

## Summary

- **Verified (remediation value confirmed, correction is worth making):** CV-001-20260707iter3
- **Refuted:** none
- **Out of scope (Major, not panel-gated per ADR's own protocol):** CV-002-20260707iter3

---

*Report persisted per P-002. Constitutional compliance: P-003 (no subagents invoked); P-020 (all output confined to `projects/PROJ-031-cowork-skeleton/`, deliverable and target report not edited); P-022 (every verdict cites file+line evidence independently re-derived from primary tournament-corpus sources and the ADR's own full text; no sibling refutation-panel outputs were read for this blind execution). Hygiene: all paths reported repo-relative; no absolute host paths or employer-internal tokens included.*
