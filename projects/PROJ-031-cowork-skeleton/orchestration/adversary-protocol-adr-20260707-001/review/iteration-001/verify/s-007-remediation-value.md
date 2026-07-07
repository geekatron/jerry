# Refutation Panel — Remediation-Value Lens (Iteration 1, S-007)

**Target:** `orchestration/adversary-protocol-adr-20260707-001/review/iteration-001/s-007-findings.md`
**Cited ADR:** `decisions/ADR-adversary-tournament-protocol-001-verified-criticals-methodology.md`
**Lens:** remediation-value — would the proposed fix materially improve the decision quality, or is it churn/machinery-adding? Default REFUTED if uncertain or if the fix is cosmetic/non-load-bearing.
**Panel isolation:** blind to factual-accuracy and materiality lane outputs for this iteration.

---

## CC-001-20260707-iter1 [Critical] — RSK-1 mitigation is the logical inverse of DEFAULT-REFUTED

**Verdict: VERIFIED**

The cited text at ADR line 707 reads verbatim: "2-of-3 majority + DEFAULT-REFUTED biases toward *keeping* claims..." as the stated mitigation for RSK-1 ("a real Critical is refuted and slips the gate" — a false-negative/over-discard risk, MED/HIGH). The ADR itself defines DEFAULT-REFUTED as the discard-biased, anti-inflation default in three other places (line 74: "default is: does not count"; line 381: "DEFAULT-REFUTED"; line 590: "REFUTED on uncertainty (the anti-inflation default)"). A discard-biased default cannot be the named reason a false-negative/over-discard risk is mitigated — as literally written it argues the mechanism protects against the very failure mode it structurally leans toward. This is the risk register entry for the single highest-impact-rated risk in the table (HIGH impact) in a document whose entire thesis is "don't trust an unverified claim," so the misdescription is not a stray adjective — a P-020 ratifying reader is given false reassurance about the ADR's own riskiest failure mode. The remediation is a single-sentence correction (either drop the DEFAULT-REFUTED clause from RSK-1's mitigation and rely on the three other named controls, or reframe the argument without invoking a mechanism that argues the opposite direction) — no new machinery, no re-opening of D-1..D-6, and it directly improves the accuracy of the risk assessment the ratification decision depends on. This clears the remediation-value bar: cheap fix, real payoff on a load-bearing document section.

---

## CC-002-20260707-iter1 [Critical] — Verification invocation granularity self-contradictory / cost model unsupported

**Verdict: VERIFIED**

Three ADR passages state incompatible units of work for the same mechanism: line 585-587 ("one call per lens per Critical-bearing report... Input = the single claimed Critical" — singular, self-contradicting "per report" if a report has >1 Critical), line 624-626 ("cost ≈ 3 × (number of claimed Criticals)" — an explicit per-Critical formula), and line 362-364 ("15 refutation-panel files = 3 lenses × 5 Criticals" for iteration-009, which the ADR's own Context section states had **10** claimed Criticals that round, line 144-146: "Of 10 claimed Criticals, 5 were VERIFIED and 5 REFUTED" — so "3×5" cannot be 3 lenses × 5 Criticals against the ADR's own stated Critical count). This is not cosmetic: WI-1 (the concrete Story whose acceptance criteria is drawn near-verbatim from the L1 Technical Implementation section) inherits "one-invocation-per-lens contract" directly from this ambiguous text, and the Cost Model claim underpins both a stated Force/constraint (c-004, cost proportional to criticality) and a named risk mitigation (RSK-4, "cost blow-up"), plus Negative Consequence #1 ("~3 extra agent runs per claimed Critical... materially more expensive than status quo"). If the true empirical unit is per-report (which the finding's own Glob-based file-count check supports: 15 files for iteration-009 matches 5 reports × 3 lenses, not 5 Criticals × 3 lenses against a stated 10-Critical round), then the Cost Model formula the ADR asserts materially overstates cost by up to 2x for that data point, and the Alignment table's "Implementation Effort: M" / Consequences' cost claims rest on an internally unsupported number. Fixing this — picking one granularity, aligning the three passages, and correcting the formula — is a textual reconciliation of an existing (already-specified) contract and cost claim; it does not add new machinery or reopen the D-1..D-6 decisions, and it directly firms up an implementation contract (WI-1 AC) and a cost/risk claim the ADR uses to argue for its own reversibility/effort profile. This clears the remediation-value bar.

---

## Summary Table

| ID | Severity (finder) | Remediation-Value Verdict | Basis |
|----|--------------------|-----------------------------|-------|
| CC-001-20260707-iter1 | Critical | VERIFIED | One-sentence, no-new-machinery fix that corrects a materially misleading risk-mitigation description for the ADR's single HIGH-impact risk; directly affects ratification-relevant risk assessment. |
| CC-002-20260707-iter1 | Critical | VERIFIED | Text-only reconciliation (no new machinery) of a 3-way contradictory contract spec that WI-1's acceptance criteria inherits verbatim, and a cost-model correction that underpins a stated constraint (c-004), a risk mitigation (RSK-4), and a Consequences-section cost claim. |
