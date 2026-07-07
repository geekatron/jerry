# Materiality Refutation Panel — S-002 Devil's Advocate (iteration 5)

**Lens:** Materiality
**Target report:** `review/iteration-005/s-002-findings.md`
**Target ADR:** `decisions/ADR-adversary-tournament-protocol-001-verified-criticals-methodology.md`
**Question:** Does the Critical genuinely undermine the ADR (wrong decision, unimplementable spec,
false evidence)? Style/edge-case issues are REFUTED even if factually true. Default is REFUTED if
uncertain.

**Scope note:** Only one Critical was raised by this report (DA-001-iter5). DA-002 through DA-006
are Major/Minor and are out of scope for this lens's Critical-only mandate.

---

## DA-001-iter5: Phase-2 escalation trigger is unobservable under the ADR's own design

**Verdict: REFUTED**

The finding's central premise — that "a panel-REFUTED Critical leaves no persistent record anywhere
in the tournament's own artifacts" (s-002-findings.md:94) — is directly contradicted by the ADR's own
text. RSK-2's mitigation column states verdicts are "persisted as separate files for audit"
(`ADR-adversary-tournament-protocol-001-verified-criticals-methodology.md:943`), and the document
elsewhere references real per-lens verdict files that adjudicate individual claimed Criticals
(e.g. `.../iteration-009/verify/s-001-refutation-factual.md` at line 469, `.../iteration-010/verify/s-013
inversion technique-refutation-factual.md` at line 216-217). The finding conflates "no entry in the
disposition table's taxonomy" (true — CLOSED-BY-DELETION/CLOSED-BY-EDIT/CLOSED-BY-DISCLOSURE/REBUTTED/
RESIDUAL-DISCLOSED per lines 251-253 indeed has no PANEL-REFUTED category) with "no persistent record
anywhere," which overstates the gap: a manual cross-round review of the persisted `verify/` directories
across the first 3 post-ratification tournaments could, in principle, check whether any REFUTED claim's
substance later recurs and gets VERIFIED — laborious and unindexed, but not architecturally impossible
as the finding asserts.

Further weakening materiality: RSK-1's own mitigation text already discloses the Phase-2 trigger as
non-committal — "it is trigger-gated (opened only if this residual is actually observed...), so it must
not be read as a committed near-term bound" (`...md:942`). The ADR does not claim an active, working
observability mechanism for this trigger; it already flags the closure as aspirational and unscheduled,
and separately names future cross-round automation as an open gap ("precondition for ... future L4/L5
instrumentation," `...md:858-861`). Since the ADR already discloses the soft/unscheduled nature of this
specific trigger rather than asserting it is actively monitored, DA-001-iter5 does not expose a false
claim, does not invalidate the chosen D-1 through D-6 decisions (this trigger clause is explicitly
"future ... out of scope for *this* ADR," `...md:862`), and does not render any WI acceptance criterion
unimplementable (no WI's acceptance criteria depend on this trigger firing). This is a legitimate
specificity/tooling-improvement suggestion for a forward-looking evolution clause, not a defect that
undermines the ADR's decision, implementability, or evidentiary honesty. Per the materiality mandate
(and default-refute-if-uncertain), REFUTED.

---

## Summary

| ID | Verdict |
|----|---------|
| DA-001-iter5 | REFUTED |

**Materiality rationale:** The one Critical raised concerns a forward-looking, explicitly-non-committal
Phase-2 escalation trigger that the ADR itself already discloses as unscheduled. The finding's strongest
claim ("no persistent record anywhere") is contradicted by the ADR's own stated persistence of per-lens
verdict files. Nothing in this finding, if left unaddressed, changes the D-1 through D-6 decision, makes
any Work Item unimplementable, or exposes false evidence in the deliverable's core claims.
