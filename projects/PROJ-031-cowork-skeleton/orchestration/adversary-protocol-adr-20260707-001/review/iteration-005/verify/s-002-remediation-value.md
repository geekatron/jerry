---
id: s-002-remediation-value
type: refutation-panel-output
lens: remediation-value
target_report: s-002-findings.md (S-002 Devil's Advocate, iteration 5)
target_deliverable: projects/PROJ-031-cowork-skeleton/decisions/ADR-adversary-tournament-protocol-001-verified-criticals-methodology.md
scope: Critical-severity findings only (per refutation panel protocol)
---

# Refutation Panel — Remediation-Value Lens — S-002 Findings (iteration 5)

**Lens question:** Would fixing this finding materially improve the decision quality of the ADR, or
would the remediation merely add machinery / bureaucratic churn without improving the decision? Default
REFUTED if uncertain or if the fix is churn.

**Scope note:** Per protocol, this panel adjudicates Critical-severity claims only. The target report
`s-002-findings.md` contains exactly one Critical (`DA-001-iter5`); the four Major and one Minor findings
(`DA-002-iter5` through `DA-006-iter5`) are out of scope for this panel and are not adjudicated here.

---

## DA-001-iter5: Phase-2 escalation trigger is unobservable under the ADR's own design

**Verdict: VERIFIED**

**Evidence check:** All four citations in the finding check out against the deliverable as quoted.
`decisions/ADR-adversary-tournament-protocol-001-verified-criticals-methodology.md:865-867` reads
verbatim: "Trigger: open Phase 2 as a work item if RSK-1/RSK-2 residual exposure (a real Critical
wrongly refuted, or a correlated-error false refutation) is observed in >= 1 of the first 3
post-ratification C3/C4 tournaments." Line 942 (RSK-1 mitigation prose) confirms, in the ADR's own
words, that "once the verified protocol is running a REFUTED claim has no cross-round recurrence path
... such a claim would have to be independently re-raised by a fresh finder pass and re-panelled from
scratch, with no cross-round memory feeding the panel." Lines 251-253 confirm the owner-authored
disposition table's category set is `CLOSED-BY-DELETION / CLOSED-BY-EDIT / CLOSED-BY-DISCLOSURE /
REBUTTED / RESIDUAL-DISCLOSED` — no `PANEL-REFUTED` (or equivalent) category exists there. Line 488
(D-2 decision row) confirms "Refuted claims (at C3/C4) carry zero dimension weight." The finding's
factual substrate is accurate.

**Remediation-value analysis:** The finding offers two remediation paths, and this matters for the
churn test. Path (a) — add a new disposition-table category to persist panel-REFUTED verdicts — would
be machinery-adding and sits in tension with the ADR's own D-3 subtraction-first doctrine
(`ADR-adversary-tournament-protocol-001-verified-criticals-methodology.md:393-411`), which explicitly
treats "each addition became new attack surface" as the failure mode the whole ADR exists to fix. If
that were the only offered fix, this finding would tilt toward churn. But path (b) — reword RSK-1's
mitigation prose to state the residual is currently *unmonitored* and either drop or caveat the specific
"observed in >= 1 of the first 3 ... tournaments" trigger language — is a disclosure-only fix requiring
zero new mechanism. This is exactly the remediation pattern this same ADR has already used successfully
four times in its own changelog (e.g., the "18 verification-panel files" -> "12" correction at
`ADR-adversary-tournament-protocol-001-verified-criticals-methodology.md:195-206`, and the PR-template
attribution correction at `:228-232`, both disclosure-based, not tooling-based). Given that precedent,
option (b) is cheap, in-genre, and directly closes a genuine internal-consistency gap: as written, the
trigger clause implies an observability capability (a persisted, cross-referenceable record of what was
refuted) that the ADR's own architecture explicitly disclaims two sections earlier ("no cross-round
memory feeding the panel"). Leaving this uncorrected lets a governance document whose central thesis is
"verify before you count" make an unfalsifiable claim about how its own flagship residual risk will be
monitored — a rhetorical inconsistency the finding correctly identifies as Internal Consistency, not
mere cosmetic nit-picking. Fixing it via honest reframing materially improves the decision quality of
the risk register (a reader can no longer be misled into thinking RSK-1 has an operative escalation
path when it currently does not), at effectively zero remediation cost.

**Conclusion:** Not churn. The cheapest available remediation path is a wording-level disclosure fix
consistent with the ADR's own established correction pattern, and it closes a real gap between a named
risk's stated escalation mechanism and the architecture's own explicit "no cross-round memory" admission.
VERIFIED under the remediation-value lens.

---

## Summary

| ID | Severity | Verdict | Basis |
|----|----------|---------|-------|
| DA-001-iter5 | Critical | **VERIFIED** | Evidence checks out; remediation is available at zero-machinery cost (disclosure-only, consistent with the ADR's own D-3 doctrine and its own prior correction pattern); fix materially closes an internal-consistency gap rather than adding churn. |

**Panel result:** 1 Critical adjudicated, 1 VERIFIED, 0 REFUTED.
