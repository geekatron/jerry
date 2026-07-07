# Refutation Panel: Remediation-Value Lens — S-002 Devil's Advocate Findings

**Panel:** Remediation-Value (would the fix materially improve decision quality, or is it
churn/machinery-adding?)
**Target report:** `projects/PROJ-031-cowork-skeleton/orchestration/adversary-protocol-adr-20260707-001/review/iteration-001/s-002-findings.md`
**Deliverable under review:** `projects/PROJ-031-cowork-skeleton/decisions/ADR-adversary-tournament-protocol-001-verified-criticals-methodology.md`
**Iteration:** 1
**Scope:** All four Critical findings in the target report (DA-001, DA-002, DA-003, DA-004).
**Policy:** DEFAULT REFUTED IF UNCERTAIN. This panel is blind to the factual-accuracy and
materiality panel outputs for this same report.

---

## DA-001-20260707-i1 — ADR's own cost-evidence citation is factually false

**Claim:** ADR context (line 133) and constraint c-004 (line 206) both cite "18 verification-panel
files" / "iter-8 FU: 18 files" for `fu-log-convention-20260705-001/adversary/iteration-008/verify/`,
but the actual directory contains 12 files.

**Verdict: VERIFIED**

Independently re-globbed `projects/PROJ-031-cowork-skeleton/orchestration/fu-log-convention-20260705-001/adversary/iteration-008/verify/*`
and counted exactly 12 files (s-001, s-002, s-004, s-012 x 3 lenses each), matching the finder's
count and contradicting the ADR's own "18" citation at ADR-adversary-tournament-protocol-001-verified-criticals-methodology.md:133,206.
The fix is a one-line numeric correction plus a disclosure note — it adds zero machinery and is the
cheapest possible remediation on the list. It has direct, material value: the corrected count is
itself an input to c-004's cost-proportionality constraint and the Cost model paragraph (lines
624-626), so an uncorrected false count propagates into the ADR's own quantitative self-support. In
a document whose subject matter is "verify a claim before counting it," leaving a citably-false count
uncorrected is not a stylistic nit; the fix directly raises Evidence Quality. Not churn.

---

## DA-002-20260707-i1 — Cost-model formula contradicts c-004 and WI-1's invocation contract

**Claim:** c-004 (line 206) states the unit of verification cost is "per Critical-bearing report,"
the Cost model paragraph (lines 624-626) states the unit is "per claimed Critical" (a ~2x-different
formula), and the L1 invocation contract (lines 585-589) states both units in adjacent sentences,
leaving WI-1's implementer without an unambiguous specification.

**Verdict: VERIFIED**

Re-read ADR-adversary-tournament-protocol-001-verified-criticals-methodology.md:204-206 (c-004:
"panels ≈ 3 agent runs per Critical-bearing report"), :624-626 (Cost model: "cost ≈ 3 × (number of
claimed Criticals)"), and :585-589 (invocation contract: "one call per lens per Critical-bearing
report" immediately followed by "Input = the single claimed Critical"). All three passages are
present as cited and the unit mismatch is real and textually verifiable without needing the
underlying file counts to resolve it. The fix required is a wording correction picking one unit
consistently across three existing passages (c-004, the Cost model paragraph, WI-1's acceptance
criteria) — no new agent, template, or process step is added, so this is not machinery-adding
churn. The remediation value is concrete and forward-looking: WI-1 (`adv-verifier`) is a proposed,
not-yet-built work item, and an implementer following the literal text today could build either a
2x-cheaper or 2x-more-expensive verifier with no way to tell which the ADR intended. Fixing the
wording before WI-1 is built prevents a real, material implementation defect rather than papering
over a merely cosmetic inconsistency.

---

## DA-003-20260707-i1 — D-1's criticality-gating boundary is evidenced by zero C1/C2/C3 rounds

**Claim:** D-1's rationale (line 264) asserts "C1-C2 work... neither exhibited [the spiral]," but
all 18 cited tournament rounds are self-declared C4, so the C1-C2 exemption and C3-vs-C4 split are
extrapolated rather than observed, undercutting the "evidence-led" framing (c-005).

**Verdict: VERIFIED (narrow scope)**

The underlying premise is independently checkable and holds: every cited round in both
`adr-convention-20260702-001` and `fu-log-convention-20260705-001` is declared C4 in this ADR's own
Context section (lines 109-166), and the ADR nowhere cites a C1, C2, or C3 round. The finder's own
proposed cheapest fix (option a: relabel the C1-C2/C3-vs-C4 cut point as a reasoned default rather
than an evidence-led finding) is pure wording — it adds no new machinery, agent, or process step, so
it is not churn. It has genuine, if narrower, remediation value: the ADR explicitly claims (c-005)
that "the decision must be evidence-led," and D-1's own rationale paragraph blurs "verification helps
at C4" (measured) with "this generalizes to a C1-C2 exemption and a C3 cut" (asserted) under one
"evidence-led" banner. Distinguishing these in the text costs nothing and directly serves the ADR's
own disclosure doctrine (P-022, D-3 subtraction/disclosure). The finder's alternative, heavier fix
(option b: run C1-C3 tournament rounds before treating the boundary as settled) would be
disproportionate scope-creep relative to the actual defect (a labeling-precision gap, not a wrong
design choice — the finder itself concedes "this does not mean the extrapolation is wrong");
remediation value here rests on the cheap wording fix, not the heavier validation-round option.

---

## DA-004-20260707-i1 — RSK-1's mitigation misdescribes DEFAULT-REFUTED's own effect

**Claim:** RSK-1's mitigation (line 707) states "DEFAULT-REFUTED biases toward *keeping* claims,"
which is the opposite of the ADR's own D-1/D-2 definitions (lines 381-382: DEFAULT-REFUTED means an
uncertain lens votes REFUTE, and D-2: "Refuted claims carry zero dimension weight") — a
discard-biased default, not a keep-biased one.

**Verdict: VERIFIED**

Directly re-read ADR-adversary-tournament-protocol-001-verified-criticals-methodology.md:381 ("2-of-3
majority, DEFAULT-REFUTED, blind to each other"), :382 ("Refuted claims carry zero dimension
weight"), and :707 ("2-of-3 majority + DEFAULT-REFUTED biases toward *keeping* claims"). The
contradiction is a direct textual comparison, not an inference: a rule whose own name and D-2's
consequence both describe discarding claims under uncertainty cannot, in the same document, be cited
as biasing toward keeping them. The fix is a rewrite of one risk-register cell's mitigation text to
state the true trade-off (discard-bias trades false-positive suppression for residual false-negative
exposure) — no new mechanism, agent, or gate is proposed; the finder's own remediation guidance is
explicitly wording-only ("rewrite RSK-1's mitigation to state the true trade-off honestly"). This is
the highest-value fix among the four Criticals: RSK-1 is the sole MED/HIGH cell in the entire risk
register, it is the specific risk this review's invoking task was instructed to probe, and an
uncorrected self-contradictory mitigation leaves the ADR's single highest-priority risk assessed by a
description that inverts its own mechanism's direction. Not churn — this is a correctness fix to the
document's own risk-honesty claim, materially affecting whether a reader can trust the risk register.

---

## Summary

| Finding | Verdict | Rationale (one line) |
|---|---|---|
| DA-001-20260707-i1 | VERIFIED | Independently reconfirmed false count (12 actual vs. 18 cited); one-line fix, zero machinery, direct Evidence Quality gain. |
| DA-002-20260707-i1 | VERIFIED | Textually-confirmed 2x unit mismatch across three passages; wording-only fix prevents a real future implementation defect in not-yet-built WI-1. |
| DA-003-20260707-i1 | VERIFIED (narrow) | Confirmed zero C1/C2/C3 rounds in the cited record; cheap relabeling fix serves the ADR's own disclosure doctrine — heavier "run validation rounds" option not required for remediation value. |
| DA-004-20260707-i1 | VERIFIED | Direct textual contradiction (line 707 vs. 381-382) on the sole MED/HIGH risk cell, which is the exact risk this review was asked to probe; wording-only fix, highest priority among the four. |

All four Critical findings from S-002 pass the remediation-value lens: each proposes a fix that is
either a pure factual correction or a pure wording/labeling correction (no new agent, tool, template,
or gate), and each directly improves either Evidence Quality, Actionability (WI-1 specification),
Methodological Rigor (evidence-scope honesty), or Internal Consistency (risk-register accuracy) in a
document whose own subject matter is verification rigor. None of the four is machinery-adding churn.

---

*Constitutional compliance: P-003 (no subagents invoked); P-020 (writes confined to
`projects/PROJ-031-cowork-skeleton/`); P-022 (all verdicts cite file+line from the ADR and
independently-reproduced directory listings; DA-003's verdict is explicitly scoped narrower than the
finder's full claim). All paths in this report are repo-relative; no absolute filesystem paths or
employer-internal tokens are present.*
