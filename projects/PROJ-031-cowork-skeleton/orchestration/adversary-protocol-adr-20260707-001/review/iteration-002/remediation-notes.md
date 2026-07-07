# Iteration-2 Remediation Notes — ADR-adversary-tournament-protocol-001

> Owner remediation pass after S-014 iteration-2 score **0.65** (gate 0.92, verdict REVISE).
> Disposition table for the 6 panel-VERIFIED Criticals + high-value advisory Majors.
> Subtraction-first (D-3): correct claims / remove machinery; add only where a gate is missing.

## Navigation

| Section | Purpose |
|---------|---------|
| [Disposition Table](#disposition-table) | Per-finding CLOSED-BY tag + edit sites |
| [Cost-Model Reconciliation](#cost-model-reconciliation-da-001--sm-001) | The per-report vs per-Critical fix, worked |
| [Figure 3 Redraw](#figure-3-redraw-cv-002) | Stop-condition flowchart correction |
| [Residual Register](#residual-register) | What remains disclosed, not closed |

---

## Disposition Table

| Finding | Sev | Panel | Disposition | Edit sites |
|---------|-----|-------|-------------|-----------|
| DA-001-i2 | Critical | VERIFIED 3/3 | CLOSED-BY-EDIT — cost-model unit relabeled "per Critical-bearing report" | c-004; D-6 rationale; L1 item 1; Cost model; Fig. 4 label; WI-1 AC; Issue A; Neg-Consequence #1; RSK-4 |
| DA-002-i2 | Critical | VERIFIED 3/3 | CLOSED-BY-EDIT — Positive Consequence #4 hedged to match D-1 | Positive Consequence #4 |
| DA-003-i2 | Critical | VERIFIED 3/3 | CLOSED-BY-EDIT — WI-8 added as WI-7 dependency + AC clause | WI-7 row; WI-7 AC |
| CC-001-iter2 | Critical | VERIFIED 3/3 | CLOSED-BY-EDIT — tool tier corrected to read+write-new-files, Edit/Bash/Agent forbidden | L1 item 1; WI-1 AC; Issue A |
| CV-001-20260707 | Critical | VERIFIED 3/3 | CLOSED-BY-EDIT — PR-template catch re-attributed to S-001 Red Team (RT-001-iter010); DA-002-i8 named as the panel-caught example | Context incident section; L1 item 2; Decision Rationale |
| CV-002-20260707 | Critical | VERIFIED 3/3 | CLOSED-BY-EDIT — Figure 3 redrawn: recurrence discriminator reserved for pre-verified mode; VERIFIED Critical routes unconditionally to FIX | Fig. 3 mermaid block + fig3-stopcondition.mmd + re-render SVG |
| DA-004-i2 | Major (advisory) | — | CLOSED-BY-EDIT — "structural closure" softened; Phase 2 given a trigger condition | L2 Evolution path; RSK-1; RSK-2 |
| DA-005-i2 | Major (advisory) | — | CLOSED-BY-EDIT — RSK-4 given a per-report ceiling + escalate rule | RSK-4 |
| CV-003-20260707 | Major (advisory) | — | CLOSED-BY-EDIT — grandfather-seam unanimity claim corrected (3 of 4) | Context iteration-10 paragraph |
| SM-002 | Major (advisory) | not panelled | CLOSED-BY-EDIT — WI-8 AC gets invocation-count reconciliation clause | WI-8 AC |
| SM-003 | Minor (advisory) | not panelled | CLOSED-BY-DISCLOSURE — footnote notes source-footer residual | disclosed-correction footnote |
| CC-002/003/004-iter2 | Major/Minor | REFUTED (materiality lens) | REBUTTED — zero weight, no edit | — |
| DA-006-i2 | Minor (advisory) | — | CLOSED-BY-EDIT — D-1 numeric-score footnote clarifies relative-preference semantics | D-1 options intro |

---

## Cost-Model Reconciliation (DA-001 / SM-001)

**Root cause:** iteration-1 remediation kept the correct file counts (15, 12) but relabeled the
multiplicand "5"/"4" as *claimed Criticals* when the primary `verify/` artifacts show they are
*Critical-bearing reports*. One lens file adjudicates every claimed Critical in its target report
(e.g. `iteration-009/verify/s-001-refutation-factual.md` renders both RT-001-iter009 VERIFIED and
RT-002-iter009 REFUTED in one pass).

**Verified units (independent Glob/Read, per S-011 VQ-16 and S-003 SM-001):**

| Round | Critical-bearing reports | verify/ files | Claimed Criticals adjudicated |
|-------|--------------------------|---------------|-------------------------------|
| iter-9 (adr-convention) | 5 (S-001,S-002,S-004,S-011,S-012) | 15 = 3×5 | 10 |
| iter-8 (fu-log) | 4 (S-001,S-002,S-004,S-012) | 12 = 3×4 | 7 |
| iteration-002 (this review) | 3 (S-002,S-007,S-011) | 9 = 3×3 | 6 |

**Going-forward unit:** cost = **3 × (number of Critical-bearing reports)**, each lens invocation
returning one VERIFIED/REFUTED verdict per claimed Critical in that report. File count tracks report
count, not claimed-Critical count.

---

## Figure 3 Redraw (CV-002)

**Defect:** old Fig. 3 mixed the D-4 recurrence discriminator (a *pre-verified* heuristic for whether
to SWITCH protocols) with post-panel gating, producing a branch (fresh stream + already-verified →
Q4) that let a VERIFIED Critical bypass FIX — contradicting D-2 and Figure 2's unconditional gating.

**Fix:** split on protocol mode first. Under the OLD protocol the recurrence discriminator decides
SWITCH-vs-remediate. Under the VERIFIED protocol, any VERIFIED Critical routes **unconditionally** to
FIX. Re-rendered with mmdc 11.12.0; SVG persisted alongside source.

---

## Residual Register

| ID | Status | Note |
|----|--------|------|
| RSK-1/RSK-2 residual | DISCLOSED, not closed | DEFAULT-REFUTED false-negative + model-correlation exposure; Phase-2 deterministic factual lens is now trigger-gated, not asserted as closed |
| SM-001 batch-vs-split granularity | RESOLVED to per-report | WI-8 now reconciles built invocation count against the formula |
| all-C4 evidence base (RSK-7) | DISCLOSED | C3 boundary provisional; WI-8 gates WI-7 |
