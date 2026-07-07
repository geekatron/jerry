# Remediation-Value Refutation Panel: S-011 Chain-of-Verification Findings (Iteration 1)

**Lens:** Remediation-value ("would fixing it change observable behavior, and can it be fixed without
adding machinery?" — per ADR L1 item 2, `projects/PROJ-031-cowork-skeleton/decisions/ADR-adversary-tournament-protocol-001-verified-criticals-methodology.md:598-599`)
**Target findings:** Critical findings CV-001-20260707-i1, CV-002-20260707-i1 from
`projects/PROJ-031-cowork-skeleton/orchestration/adversary-protocol-adr-20260707-001/review/iteration-001/s-011-findings.md`
**Finder deliverable under review:** `projects/PROJ-031-cowork-skeleton/decisions/ADR-adversary-tournament-protocol-001-verified-criticals-methodology.md`
**Panel discipline:** Independent, blind to other lenses/panels. Default = REFUTED on uncertainty.
**Task framing:** REMEDIATION-VALUE = would the fix materially improve the decision quality, or is it
churn/machinery-adding? Factual accuracy of the underlying claim is assumed (not re-litigated here);
this panel judges only whether correcting it is worth doing.

---

## Verdicts

| Finding | Verdict | Dimension |
|---|---|---|
| CV-001-20260707-i1 (false "18 verification-panel files" citation) | **VERIFIED** | Evidence Quality |
| CV-002-20260707-i1 (invocation-contract granularity contradiction) | **VERIFIED** | Methodological Rigor / Actionability |

---

## CV-001-20260707-i1: "18 verification-panel files" -> should be "12"

**Verdict: VERIFIED (real remediation value, not churn).**

The fix is a same-sentence numeric substitution in three locations — D-6 rationale
(`ADR-adversary-tournament-protocol-001-verified-criticals-methodology.md:362-369`, "18 verification-panel
files"), the Cost model paragraph (lines 624-626, "~15–18 verifier files per C4 round"), and constraint
c-004's source column (line 206, "iter-8 FU: 18 files") — plus one derived range ("~15–18" -> "~12–15").
This is not machinery: no new section, rule, agent, or template is added; it is a same-line text edit at
three call sites the ADR itself already cites as its evidentiary backing for the cost-proportionality
argument (D-1's chosen Option C is justified partly by "cost gated by criticality," Alignment table,
line 405). Because the ADR's own Force 6 and L2 "Independence as architecture" section (lines 636-641)
stake the whole design on the premise that verification must not be self-attested and must be checkable
against primary evidence, leaving a self-contradicting citation (the source's own line 36 breakdown
computes to 12, not 18, per s-011-findings.md:106) uncorrected directly undermines the credibility of
the exact evidentiary-rigor claim the ADR is built to institutionalize. The correction is cheap,
localized, and materially restores the internal honesty of the record this ADR is asking the team to
trust — it is a substantive accuracy fix, not cosmetic churn.

---

## CV-002-20260707-i1: invocation-contract granularity contradiction (per-report vs. per-Critical)

**Verdict: VERIFIED (real remediation value, not churn).**

This is not a wording nit; the ambiguity sits directly on the change surface that WI-1 will be built
from. L1 item 1 (`ADR-adversary-tournament-protocol-001-verified-criticals-methodology.md:584-587`)
states the invocation is "per lens per Critical-bearing report" but then defines the Input as "the single
claimed Critical" — two different units of work in the same bullet. The Cost model (lines 624-626,
"cost ≈ 3 × (number of claimed Criticals)") and Fig. 4's PANELS lane label ("3 lenses per Critical",
line 555) both encode the per-Critical unit, which — per the finder's own arithmetic — does not match
the empirically observed file counts (iteration-9: 10 claimed Criticals -> 15 files, not 30; FU-log
iteration-8: 7 claimed Criticals -> 12 files, not 21). Left unresolved, an implementer building WI-1
from the literal L1 text would construct a per-claim invocation loop and a `{finding-id}-{lens}.md`
output-naming convention that both contradict the report-scoped pattern the empirical `verify/`
directories actually exhibit, and the Cost model figure used to justify choosing Option C over Option B
in D-1 (Alignment table, "Implementation Effort: M," line 407) would be computed on the wrong unit
(over-stating true cost by roughly the average Criticals-per-report ratio). The fix proposed by the
finder (make L1, Cost model, Fig. 4, and the output-path convention consistent on the report-level unit,
per the correction at s-011-findings.md:135) is a same-scope editorial reconciliation across four
existing locations — no new decision, agent, or mechanism is introduced. This is exactly the kind of
correction that changes observable behavior (a correctly-scoped, correctly-costed WI-1 implementation)
without adding machinery, so it clears the remediation-value bar with clear margin, not by default.

---

## Summary

Both Critical findings from the S-011 Chain-of-Verification pass are VERIFIED under the
remediation-value lens: each correction is a targeted, low-cost textual reconciliation (not new
machinery) that materially improves either the evidentiary integrity of the ADR's own justificatory
citations (CV-001) or the direct implementability and cost-accuracy of the proposed WI-1 change surface
(CV-002). Neither is process churn or gratuitous rigor; both fixes are narrowly scoped to the exact
sentences the finder identified and would leave the ADR's D-1 through D-6 decisions themselves entirely
unchanged, correcting only the supporting evidence and specification text around them.
