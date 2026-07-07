# Materiality Refutation Panel — S-002 Devil's Advocate Findings (iteration 2)

## Navigation

| Section | Purpose |
|---------|---------|
| [Scope](#scope) | Panel context and method |
| [Verdicts](#verdicts) | Per-finding VERIFIED/REFUTED with evidence |
| [Summary](#summary) | Structured output summary |

---

## Scope

**Lens:** Materiality (does the finding genuinely undermine the ADR — wrong decision, unimplementable
spec, or false evidence — vs. a style/edge-case nit?). Default REFUTED if uncertain.

**Target:** `projects/PROJ-031-cowork-skeleton/orchestration/adversary-protocol-adr-20260707-001/review/iteration-002/s-002-findings.md`
(S-002 Devil's Advocate, iteration 2)

**Deliverable under review:** `projects/PROJ-031-cowork-skeleton/decisions/ADR-adversary-tournament-protocol-001-verified-criticals-methodology.md` (v0.2)

**Only Critical-severity findings are in scope for verification** (per the refutation-panel protocol):
DA-001-i2, DA-002-i2, DA-003-i2. This panel is blind to any other lens's output (factual-accuracy,
remediation-value) or any other panel's verdicts.

---

## Verdicts

### DA-001-i2: Cost-model empirical basis does not reconcile — **VERIFIED**

The ADR's own text contains a real, checkable quantitative mismatch. At line 217 (c-004) and lines
385-386 (D-6 rationale), the cost-model anchor is stated as "iter-9: 15 files = 3 lenses × 5
Criticals." But the Context section's own narration of the same iteration-9 round (lines 146-148,
citing `.../iteration-009/s-014-quality-score.md:36-37, 128-135`) states "Of 10 claimed Criticals, 5
were VERIFIED and 5 REFUTED" — i.e., the panel adjudicated **10** claimed Criticals that round, not
5. Under the ADR's own stated invocation contract ("3 × k" where k = claimed Criticals, lines 608-611,
662-661, and WI-1's acceptance criteria at line 762), 10 claimed Criticals should have produced 30
files, not the cited 15. Compounding this, the disclosed-correction footnote at line 166 labels the
identical "4" multiplier for the parallel iter-8 FU-log case as "4 **Critical-bearing reports**" —
a different unit than "Criticals," which lines 217 and 385-386 use for the same figure. This is a
genuine, file+line-verifiable internal inconsistency between the empirical anchor (which appears to
be per-report) and the going-forward specified unit (per-claimed-Critical, per WI-1 and L1's
invocation contract). It is material, not stylistic: it undermines the "false evidence" prong directly
— the ADR presents "~12–15 files empirically confirmed" (line 659-660) as validating the exact
per-claimed-Critical costing contract that WI-1 will implement, when the cited data does not actually
reconcile with that unit. If the true empirical grain was per-report, the going-forward per-Critical
model is untested and future per-round cost could be understated by roughly 2x, directly affecting the
Alignment table's "Implementation Effort: M" rating and RSK-4's mitigation credibility.

**Evidence:** ADR lines 146-148, 154-161, 166, 217, 385-386, 608-611, 659-660, 762 (cross-checked
against the DA-001-i2 citations; all resolve to the quoted content).

---

### DA-002-i2: Positive Consequence #4 contradicts D-1's own disclaimer — **VERIFIED**

Positive Consequence #4 (lines 705-706) states: "the panel budget concentrates on C3/C4 governance
where **the spiral actually occurs**." D-1's own rationale (lines 282-284) explicitly cautions: "the
C1–C2 exemption is a cost-proportionality default... **not** a finding that C1–C2 'did not spiral.'"
These are in real tension: one passage frames spiral-occurrence as an established fact scoped to
C3/C4; the other explicitly disclaims drawing that inference. The contradiction is sharper than a
wording nit because the ADR's own D-1 section discloses, prominently and specifically, that **100% of
the 18 cited tournament rounds ran at C4 — zero C1, C2, or C3 rounds exist in the record** (lines
276-278). Positive Consequence #4's phrase "C3/C4 governance where the spiral actually occurs" thus
implies observed C3 evidence that the ADR itself, elsewhere, explicitly says does not exist. This is
material because it touches the ADR's central selling point — evidence-honest scoping (c-005,
"evidence-led... disclosed residuals are valid posture") — and a reader who encounters only the
Consequences section (a natural high-level summary a reviewer might quote) would draw an incorrect,
more confident conclusion than the ADR's own careful analysis supports. This is a substantive Internal
Consistency defect, not a style nit, because it misstates evidentiary scope for the exact criticality
boundary (C3) that WI-8 is designed to validate as still-provisional.

**Evidence:** ADR lines 226-228, 276-284, 705-706 (cross-checked; all resolve to the quoted content).

---

### DA-003-i2: RSK-7's mitigation is not enforced by the work-item dependency graph — **VERIFIED**

RSK-7's mitigation text (line 747) states: "WI-8's validation pass is required to include at least one
non-ADR-genre C3/C4 deliverable... before the protocol is treated as framework-general." Direct
inspection of the Proposed backlog table (lines 762-769) confirms: WI-7 ("`quality-enforcement.md`
Implementation-section pointer" — the artifact that operationalizes framework-general adoption) lists
"Depends on: WI-2, WI-3" only; WI-8 is not listed. WI-8 itself lists "Depends on: WI-1..WI-5" — it does
not appear as an upstream gate on WI-7, and WI-7's row makes no reference to WI-8. As specified, a team
executing this backlog literally could complete WI-7 (adding the SSOT pointer that treats the protocol
as framework-general) without WI-8 ever having run, silently defeating the one stated safeguard against
the n=2, maximally-correlated evidence base that RSK-7 itself names as a MED/MED risk. This is material
under the "wrong decision" / "unimplementable-as-promised spec" prong: the mitigation is asserted in
prose but the executable artifact (the dependency table that actually gates other work items, e.g.,
WI-3→WI-1, WI-4→WI-2) does not encode it, so the safeguard is not real as written.

**Evidence:** ADR lines 747 (RSK-7), 762-769 (Proposed backlog table, "Depends on" column)
(cross-checked; all resolve to the quoted content).

---

## Summary

All three Critical findings (DA-001-i2, DA-002-i2, DA-003-i2) are **VERIFIED** under the materiality
lens. Each is grounded in precise, file+line-checkable citations to the ADR's own text, each
identifies a genuine tension or gap between two passages of the same document (not an external or
speculative claim), and each affects a load-bearing property of the ADR: the empirical cost-model
justification (DA-001-i2), the evidence-honesty framing the ADR claims for itself (DA-002-i2), and the
enforceability of the ADR's own stated risk mitigation for its most significant evidentiary limitation
(DA-003-i2). None were refuted; none were judged to be style/edge-case nits.

**Verdict counts:** 3 VERIFIED, 0 REFUTED.
