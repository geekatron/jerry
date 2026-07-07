# Refutation Panel — Factual Lens — S-002 (Devil's Advocate) Criticals — Iteration 2

**Panel:** Factual accuracy lens (Lens 1 of 3, per D-1 refutation-panel design)
**Target:** `projects/PROJ-031-cowork-skeleton/orchestration/adversary-protocol-adr-20260707-001/review/iteration-002/s-002-findings.md`
**Deliverable under review:** `projects/PROJ-031-cowork-skeleton/decisions/ADR-adversary-tournament-protocol-001-verified-criticals-methodology.md` (v0.2)
**Rule applied:** DEFAULT-REFUTED on uncertainty. Misreads, stale references, or restatements of a limit the ADR already discloses are REFUTED. A defect that factually exists at the cited lines (accurate quote, accurate line reference, real — not imagined — mismatch) is VERIFIED.
**Scope:** Critical-severity findings only (DA-001-i2, DA-002-i2, DA-003-i2), consistent with the ADR's own D-1 panel-gating rule (panels adjudicate claimed Criticals; Majors/Minors are advisory).

---

## DA-001-i2 — Cost-model empirical basis does not reconcile with the ADR's own narrated Critical counts

**Verdict: VERIFIED**

Citations check out verbatim. Lines 146-147 state, for iteration 9: *"Of 10 claimed Criticals, 5 were VERIFIED and 5 REFUTED"* — a total of 10. c-004 (line 217) and the D-6 rationale (lines 385-386) both label the identical multiplier "5" as "Criticals" in "iter-9: 15 files = 3 lenses × 5 Criticals," and the Cost model (lines 659-660) repeats "iter-9 = 3 × 5 = 15." If the invocation contract is truly "3 lens-invocations per claimed Critical" (stated at lines 608-611 and required by WI-1's acceptance criteria at line 762), 10 claimed Criticals implies an expected 30 files, not 15 — a 2x gap that the ADR nowhere reconciles. The unit ambiguity is compounded by the disclosed-correction footnote at line 166, which labels the *same* iteration-8 FU-log "4" figure as "Critical-bearing **reports**," while lines 217 and 385-386 label the identical "4" as "**Criticals**" — two different units used interchangeably for one number. This is a genuine, newly-surfaced residual: the v0.2 changelog (line 858, "D2") records that the prior iteration's remediation *standardized the wording* of the unit ("3 x claimed Criticals," gated at report level) across all citation sites, but that pass did not verify the underlying claimed-Critical counts against the multipliers actually used — so the wording is now consistent while the arithmetic underneath it is not. Not a misread or a restatement of an already-disclosed limit.

---

## DA-002-i2 — Positive Consequence #4 asserts as fact what D-1 explicitly disclaims

**Verdict: VERIFIED**

Both quotes are accurate at the cited lines. Lines 705-706 read, verbatim: *"**Cost proportionality.** C1–C2 work pays nothing; the panel budget concentrates on C3/C4 governance where the spiral actually occurs."* Lines 282-284 read, verbatim: *"...the **C1–C2 exemption is a cost-proportionality default**... **not** a finding that C1–C2 'did not spiral.'"* — and the surrounding D-1 text (lines 276-279) additionally discloses that the entire 18-round record is 100% C4 with **zero C3 rounds**, making the C3 half of "the spiral actually occurs [at] C3/C4" an extrapolation the ADR's own D-1 section calls "provisional" (line 285), not an observed fact. Positive Consequence #4 states the C3/C4-scoped spiral as settled empirical fact with no hedge, directly contradicting D-1's own careful qualification of the identical claim two sections earlier in the same document. This is not a stale reference: the v0.2 changelog's "D4" entry (line 858) shows the prior remediation pass added the "reasoned default, not a finding" hedge specifically to D-1's text, but did not propagate the same hedge to the Positive Consequences bullet — leaving exactly the contradiction the finder identifies.

---

## DA-003-i2 — RSK-7's mitigation is not enforced by the work-item dependency graph

**Verdict: VERIFIED**

The Work-Item Decomposition table is confirmed as cited. WI-7's row (line 768) lists "Depends on" = **"WI-2, WI-3"** only. WI-8's row (line 769) lists "Depends on" = **"WI-1..WI-5"** only. Neither row references the other, so nothing in the machine-readable dependency graph prevents WI-7 (the `quality-enforcement.md` Implementation-section pointer, i.e., the SSOT artifact that operationalizes framework-general adoption) from completing before WI-8 (the non-ADR-genre validation pass) runs. This is a real, verifiable gap against RSK-7's own mitigation text at line 747, which states in prose: *"**WI-8's validation pass is required to include at least one non-ADR-genre C3/C4 deliverable**... before the protocol is treated as framework-general."* The v0.2 changelog confirms RSK-7 and the non-ADR-genre requirement in WI-8 were themselves *added* during the prior remediation pass (line 858, "DA-005" advisory item) — but that pass added the prose mitigation without also adding the corresponding dependency edge, so the enforcement gap the finder identifies is a genuine, unaddressed residual of that same fix, not a misread of an already-disclosed limitation.

---

## Summary

| ID | Verdict | Lines checked | Basis |
|----|---------|---------------|-------|
| DA-001-i2 | VERIFIED | 146-147, 154-161, 166, 217, 385-386, 608-611, 659-660, 762 | Claimed-Critical counts (10; ≥7) do not reconcile with the "5"/"4" multipliers used in the cost model; unit conflated between "Criticals" and "reports" at line 166 vs. 217/385-386. |
| DA-002-i2 | VERIFIED | 226-228, 276-288, 705-706 | Positive Consequence #4 states the C3/C4-scoped spiral as settled fact; D-1's own text (same document) explicitly disclaims this exact framing and discloses zero C3 rounds exist in the record. |
| DA-003-i2 | VERIFIED | 747 (RSK-7), 762, 768-769 (WI-7/WI-8 "Depends on") | WI-7's dependency list ("WI-2, WI-3") does not include WI-8; WI-8's dependency list ("WI-1..WI-5") does not reference WI-7 either — RSK-7's prose mitigation is unenforced by the dependency graph. |

**All three Critical findings from S-002 iteration 2 are VERIFIED under the factual lens.** No misreads, stale references, or restatements of already-disclosed limits were found; each finding's cited evidence resolves exactly as the finder states, and each identifies a defect that survived (or was introduced as a residual of) the iteration-1 remediation pass recorded in the ADR's own Changelog.
