# Refutation Panel — Materiality Lens

**Target report:** `projects/PROJ-031-cowork-skeleton/orchestration/adversary-protocol-adr-20260707-001/review/iteration-004/s-002-findings.md` (S-002 Devil's Advocate, iteration-004)
**Deliverable under review:** `projects/PROJ-031-cowork-skeleton/decisions/ADR-adversary-tournament-protocol-001-verified-criticals-methodology.md`
**Lens:** Materiality (does the finding, if true, genuinely undermine the ADR — wrong decision, unimplementable spec, or false evidence — vs. a style/edge-case issue?)
**Panel scope note:** Per this ADR's own protocol (Deliverable line 733 remediation-value lens; Context line 229 "panels adjudicate Criticals only"), refutation panels adjudicate **Critical**-severity claims only. This report's single Critical is `DA-001-iter4`; the three Major and one Minor findings (`DA-002-iter4`, `DA-003-iter4`, `DA-004-iter4`, `DA-005-iter4`) are out of this panel's adjudication scope and are not adjudicated below.
**Default rule:** REFUTED on uncertainty.

---

## DA-001-iter4: RSK-1 mitigation #3 contradicted by Figure 3's own corrected recurrence-discriminator scope [CRITICAL]

**Verdict: VERIFIED**

The claim is directly checkable against the deliverable's own diagram source and caption, and it holds. RSK-1 mitigation #3 (deliverable line 903) states the "convergence discriminator (D-4) re-surfaces a genuinely recurring defect in a later round if it is wrongly refuted once," but Figure 3's mermaid source (deliverable lines 616-636) routes the `Q2` recurrence check exclusively under the `PROTO -- "No (old protocol, no panels yet)"` branch (line 620); the `PROTO -- "Yes (verified protocol)"` branch (line 625) only asks `Q1: "Any VERIFIED Criticals this round?"`, with no path that re-examines a REFUTED verdict. The figure's own caption confirms this scope narrowing explicitly: "the recurrence discriminator applies only in the pre-verified (old-protocol) mode... once the verified protocol is running, any VERIFIED Critical routes unconditionally to remediation (FIX)" (lines 638-641) — REFUTED claims are never mentioned as re-entering any check.

This is materially significant, not a style nitpick: refutation (and therefore the possibility of a wrongly-refuted false negative) can only occur once the verified protocol is the operating mode, which is precisely the regime RSK-1 mitigation #3 claims a re-surfacing safety net for and precisely the regime Figure 3 shows has no such path. RSK-1 is the register's own highest-consequence risk (MED/HIGH), and the ADR's central differentiating claim — that residual false-negative risk is honestly bounded by four named counterweights — is measurably weaker than presented if one of the four counterweights does not operate in steady-state verified-protocol mode. This is a genuine internal contradiction between the ADR's own corrected safety-critical figure (explicitly redrawn in iteration-2 per CV-002-20260707 for a related reason, per the deliverable's own Changelog line 1046) and its risk-register prose, which is exactly the "verify before you count" failure mode this ADR argues against in its own PR-template incident narrative (deliverable lines 192-203). I could not construct a plausible alternate reading of Figure 3's source that preserves mitigation #3's claim; the finding's evidence citations are accurate and the contradiction is real and load-bearing for the ADR's honesty-bounding thesis.

---

## Summary

| ID | Severity | Verdict |
|----|----------|---------|
| DA-001-iter4 | Critical | VERIFIED |

**Result:** 1 of 1 adjudicated Critical VERIFIED. No REFUTED verdicts issued for the Critical tier. Majors/Minor (DA-002 through DA-005) are out of this panel's Critical-only adjudication scope per the ADR's own protocol and carry no verdict here.
