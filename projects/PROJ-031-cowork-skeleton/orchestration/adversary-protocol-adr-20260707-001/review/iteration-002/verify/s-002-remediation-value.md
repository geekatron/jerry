# Remediation-Value Refutation Panel: S-002 Devil's Advocate (iteration 2)

**Lens:** remediation-value (would the fix materially improve decision quality, or is it churn/machinery-adding?)
**Target:** `projects/PROJ-031-cowork-skeleton/orchestration/adversary-protocol-adr-20260707-001/review/iteration-002/s-002-findings.md`
**Deliverable under review:** `projects/PROJ-031-cowork-skeleton/decisions/ADR-adversary-tournament-protocol-001-verified-criticals-methodology.md`
**Default rule:** DEFAULT-REFUTED if uncertain.

---

## DA-001-i2 — Cost-model empirical basis does not reconcile with the ADR's own narrated Critical counts [CRITICAL]

**Verdict: VERIFIED**

Independently confirmed the underlying numbers in the ADR itself: line 146-147 states "Of 10 claimed Criticals, 5 were VERIFIED and 5 REFUTED" for iteration 9, while c-004 (line 217) and the Cost model (line 659-660) cite "iter-9: 15 files = 3 lenses × 5 Criticals" as the empirical basis for the going-forward per-Critical costing rule. If the L1 invocation contract (line 608-611: "3 × k verifier runs" where k = claimed Criticals) actually held historically, 10 claimed Criticals would produce 30 files, not the cited 15 — meaning the historical data was priced per-report (as the line-166 footnote explicitly labels the parallel iter-8 FU datum, "4 Critical-bearing reports"), not per-Critical as the adopted going-forward model claims. Fixing this is not churn: the reconciled unit directly feeds the Alignment table's "Implementation Effort: M" rating (line 429) and RSK-4's cost-blowup mitigation (line 744), and an unreconciled 2x cost-estimate error is a real planning-relevant defect, not cosmetic precision. The fix (state the actual per-report vs. per-Critical split with citations, and re-derive or caveat the "~12-15" figure) is a correction to existing content, not new process — high remediation value.

---

## DA-002-i2 — Positive Consequence #4 asserts as fact what D-1 explicitly disclaims [CRITICAL]

**Verdict: VERIFIED**

Confirmed the direct textual contradiction: line 705-706 states "the panel budget concentrates on C3/C4 governance where the spiral actually occurs," while D-1 (line 282-284) explicitly disclaims that exact framing — "the C1-C2 exemption is a cost-proportionality default... not a finding that C1-C2 'did not spiral.'" The Forces section (line 226-228) independently corroborates that the finder-incentive mechanism is criticality-agnostic, reinforcing that the Positive Consequence's stronger claim is unsupported. The fix is a one-bullet wording correction (no new machinery), and it is squarely within scope because the ADR's own selling point is evidence-led honesty (c-005) and it already sets precedent for exactly this kind of correction (the RSK-1 DEFAULT-REFUTED reframing recorded in the changelog, line 858). Aligning the Consequences section with the ADR's own careful D-1 hedge materially improves internal consistency and prevents a reader who skims Consequences-only from drawing an unsupported empirical conclusion — real value, not busywork.

---

## DA-003-i2 — RSK-7's mitigation is not enforced by the work-item dependency graph [CRITICAL]

**Verdict: VERIFIED**

Confirmed from the Work-Item Decomposition table: WI-7's "Depends on" column reads "WI-2, WI-3" (line 768) and WI-8's reads "WI-1..WI-5" (line 769) — WI-8 is not listed as a precondition of WI-7, and RSK-7 (line 747) explicitly requires the non-ADR-genre validation ("WI-8's validation pass") to complete "before the protocol is treated as framework-general," which WI-7 (the `quality-enforcement.md` SSOT pointer) operationalizes. The proposed fix — add WI-8 to WI-7's dependency cell or its acceptance criteria — is a single-cell edit consistent with the table's own existing convention (other rows, e.g. WI-3 -> WI-1, WI-4 -> WI-2, already use this column as the operative gate), not new machinery. Because dependency chains are exactly the mechanism most likely to be lost once WI-1..WI-8 fork into separate GitHub issues/worktracker entities (RSK-7's only named mitigation would then live solely in ADR prose, disconnected from the executable plan), this is a low-cost, high-value fix that closes a real enforcement gap for a MED/MED risk rather than adding process overhead.

---

## Summary

All three Critical findings pass the remediation-value bar: each proposed fix is a targeted correction to existing content (reconciling cited figures, aligning contradictory prose, adding one dependency edge) rather than new process, complexity, or machinery, and each closes a gap that would otherwise mislead a reader or silently defeat a stated risk mitigation once the plan moves into execution.
