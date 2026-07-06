# Refutation Panel — S-011 (Chain-of-Verification) — Remediation-Value Lens

**Iteration:** 9
**Lens:** remediation-value — would fixing this materially change real adoption outcomes, or is it churn? Findings whose fix is optional polish, already scheduled elsewhere, or would ADD machinery against the ratified subtraction doctrine are REFUTED. Default to REFUTED if uncertain.
**Target report:** `projects/PROJ-031-cowork-skeleton/orchestration/adr-convention-20260702-001/adversary/iteration-009/s-011-findings.md`
**Scope:** Only Critical-severity findings are adjudicated. The report contains exactly **one** Critical finding (`011-001` / `CV-001`); `011-002` / `CV-002` is Minor and out of scope for this panel.

---

## Critical Findings Adjudicated

### 011-001 (CV-001): Consequences "near-zero forced churn" claim misciting D-4 for this ADR's own Path-2 exception

**Finder's claim (s-011-findings.md:65-89):** ADR line 438 (Consequences → Positive, item 4) states *"the 15 pre-existing project/entity dialect ADRs (16 incl. this ADR) are grandfathered ... Net near-zero forced churn (D-4)."* The finder argues this contradicts D-4 itself (ADR:223, *"This ADR is the one disclosed exception to 'in place'... it is itself scheduled for Path-2 self-promotion... so it does not remain in place"*) and the Migration Plan table (ADR:511, this ADR's own row costed **"Low"**, not "Zero" — recalibrated from "Trivial" per FM-006-iter7 specifically because the Path-2 self-promotion is "multi-part").

**Verdict: REFUTED.**

**Reasoning:**

1. **The parenthetical is a count cross-reference to D-4's own established terminology, not an independent contradicting assertion.** ADR:226 (the D-4 grandfather-count reconciliation, ~200 lines earlier in the same document) defines "16" verbatim as *"the whole dialect corpus... including this ADR and including the out-of-scan entity-embedded `ADR-STORY015-001`"*. Consequences-Positive-4's "(16 incl. this ADR)" reuses that exact defined figure for a count clarification — it does not introduce a new, competing claim about this ADR's migration cost. Read grammatically, "the 15 pre-existing... ADRs (16 incl. this ADR) are grandfathered" most naturally attaches "are grandfathered" to the 15 (the subject noun phrase), with the parenthetical supplying an alternate total count for readers reconciling the two "15"s D-4 itself flags as "numerically equal by coincidence while counting different sets" (ADR:231).

2. **"Near-zero forced churn" is not "zero forced churn," and the document's own numbers support the weaker aggregate claim regardless of which parse is used.** Even under the finder's less charitable reading (that the predicate extends to all 16), the aggregate migration cost across a 16-18-ADR corpus where 15 are "Zero" cost (ADR:509), 3 are already compliant, and exactly one (this ADR) is costed "Low" (ADR:511) is honestly characterizable as "near-zero" in the corpus-wide sense the bullet is making (a contrast against a hypothetical big-bang renumber of the whole corpus, per the bullet's own opening clause "No big-bang migration"). The word choice already hedges for the one non-zero case; the finder's argument requires reading "near-zero" as if it asserted "zero for all 16," which the text does not literally claim.

3. **No adoption-relevant document is misled by this phrasing.** The operative instrument for executing the migration is the Migration Plan table (ADR:502-544), which correctly and separately rows this ADR's own Path-2 cost as "Low," cites FM-006-iter7's multi-part rationale, and gates M-9 for AE-004 auto-C4 escalation (ADR:539, 573-577) — all accurate, undisputed, and unaffected by the Consequences bullet's wording. A reader executing the migration works from the Migration Plan table and Promotion Process, not from the Consequences summary list; nobody would skip or mis-scope this ADR's own M-9 promotion because of this one bullet. The finder's own "Correction" (s-011-findings.md:89) is a single-sentence prose edit with zero effect on the lint, the migration plan, the gating logic, or any enforcement mechanism — it is definitionally polish.

4. **This is exactly the class of iteration-9 churn the remediation-value lens exists to filter.** The underlying facts (this ADR is the disclosed Path-2 exception; its own migration is "Low," not "Zero"; M-9 is AE-004-gated) are already stated with full honesty and in more authoritative form at D-4 (ADR:223-231) and the Migration Plan row (ADR:511) — both of which the finder's own verification confirms are internally accurate. What remains is a stylistic ambiguity in a *summary restatement* three sections later, in a C4 document that has already been through four disciplined subtraction/remediation passes (subtraction-pass-notes.md, iterations 5-8) explicitly to stop the "additive-remediation spiral" of chasing every residual prose imprecision. Fixing this changes no adoption behavior, no lint rule, no migration cost, and no gating decision — it is optional editorial tightening of an already-adequately-hedged sentence, not a defect that misleads an adopter or an implementer.

**Disposition:** REFUTED under the remediation-value lens. Per the default-to-refuted instruction and the explicit exclusion of "optional polish" findings, this Critical does not survive: the claim is a defensible (if slightly loose) cross-reference to D-4's own established count, the word "near-zero" already accommodates the one non-zero case, and the proposed fix has no bearing on real adoption/execution outcomes since the operative Migration Plan and Promotion Process sections are already accurate and unaffected.

---

## Summary

| Finding ID | Severity | Verdict |
|---|---|---|
| 011-001 (CV-001) | Critical | REFUTED |

**Note:** 011-002 (CV-002) is Minor and out of scope for this Critical-only refutation panel; no verdict is rendered on it.

*No subagents spawned (P-003). No files edited outside mandate (P-020). All claims cite file+line; the "grammatical parse" reasoning in point 1 above is this reviewer's inference, labeled as such (P-022).*
