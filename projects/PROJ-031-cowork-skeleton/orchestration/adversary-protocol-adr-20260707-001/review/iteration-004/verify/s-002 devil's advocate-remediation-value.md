# Refutation Panel — Remediation-Value Lens
## S-002 Devil's Advocate, iteration-004

**Target:** `projects/PROJ-031-cowork-skeleton/orchestration/adversary-protocol-adr-20260707-001/review/iteration-004/s-002-findings.md`
**ADR under review:** `projects/PROJ-031-cowork-skeleton/decisions/ADR-adversary-tournament-protocol-001-verified-criticals-methodology.md`
**Lens:** Remediation-value (would the fix materially improve the decision quality, or is it churn/machinery-adding? Default REFUTED if uncertain.)
**Panel member:** blind, isolated from other lenses' verdicts.

---

## Criticals Adjudicated

Only one Critical was raised by this finder: **DA-001-iter4**.

### DA-001-iter4: RSK-1 mitigation #3 does not exist once the verified protocol is running

**Finder's claim challenged:** RSK-1's mitigation #3 ("the convergence discriminator (D-4) re-surfaces
a genuinely recurring defect in a later round if it is wrongly refuted once", ADR line 903) is
contradicted by Figure 3, which routes the recurrence check (`Q2`) only through the
`PROTO -- "No (old protocol, no panels yet)"` branch (ADR lines 616-623), while the
`PROTO -- "Yes (verified protocol)"` branch (line 625) goes straight to `Q1: "Any VERIFIED Criticals
this round?"` with no recurrence check for REFUTED claims (lines 625-628). The Figure's own caption
(lines 638-641) confirms: "the recurrence discriminator applies only in the pre-verified (old-protocol)
mode... once the verified protocol is running, any VERIFIED Critical routes unconditionally to
remediation (FIX)" — REFUTED claims are absent from that sentence.

**Verdict: VERIFIED**

**Rationale (remediation-value lens):**

1. **The underlying inconsistency is real and independently confirmed.** I read Figure 3's mermaid
   source directly (ADR-adversary-tournament-protocol-001, lines 616-636): the `Q2` recurrence-check
   node only exists inside the `PROTO -- "No..."` branch; the `PROTO -- "Yes (verified protocol)"`
   branch (line 625) has exactly two downstream questions (`Q1` and the composite-vs-gate split, lines
   625-628), neither of which re-examines a REFUTED verdict's recurrence. The caption at lines 638-641
   explicitly restricts the recurrence discriminator to "pre-verified (old-protocol) mode." RSK-1's
   mitigation #3 at line 903, by contrast, asserts this exact mechanism operates as an ongoing
   safety net ("re-surfaces a genuinely recurring defect in a later round if it is wrongly refuted
   once") without that scope restriction. This is a genuine, citable contradiction between two parts
   of the same document — not a misreading by the finder.

2. **The fix is low-cost and non-additive, not churn.** The finder's own "Response Required" section
   offers option (a): "explicitly narrow RSK-1 mitigation #3 to state that it applies only during the
   pre-verified-protocol transition window... and honestly re-price the residual risk without that
   counterweight." This is a textual reconciliation between RSK-1's prose and Figure 3's own caption
   (which the ADR authors already produced in a prior correction pass, CV-002-20260707, per line 66 of
   the S-002 report and lines 638-642 of the ADR). It requires no new agent, no new template, no new
   process step — it is strictly a documentation-accuracy fix, the opposite of "machinery-adding."
   Option (b) (a genuine cross-round recurrence check for REFUTED Criticals) would add machinery, but
   the finder explicitly offers (a) as a standalone sufficient remedy, so the Critical does not force a
   machinery-adding fix.

3. **The fix is materially load-bearing, not cosmetic.** RSK-1 is the register's own
   highest-consequence entry (MED probability / HIGH impact), and the ADR's central differentiator
   claim (per its own L0 and Rationale sections, lines 61-95 and 485-501) is that residual risk is
   *honestly bounded*, not merely disclosed. One of RSK-1's four named counterweights describing that
   bound does not operate in the regime where the risk it purports to mitigate can occur (REFUTED
   claims exist only under the verified protocol, and the cited mechanism is scoped out of that
   protocol per the ADR's own Figure 3 caption). A reader (or ratifying user) relying on RSK-1's
   mitigation list to gauge the framework's actual false-negative exposure is materially misled by
   1-of-4 counterweights that do not function as stated. Correcting this is not polish; it changes the
   accuracy of the residual-risk claim a ratification decision would rely on.

4. **Scope check:** the finding does not challenge D-1 through D-6 (the finder concedes this in its own
   Summary), and I concur that is the correct scope — this is a risk-register accuracy defect, not a
   decision-reversal argument. That narrower scope does not make it churn; an ADR's Risks section is
   itself a load-bearing part of the "decision quality" a ratifying reader consumes, and an inaccurate
   mitigation claim for the register's top risk is a genuine defect in that section regardless of
   whether it touches D-1..D-6.

**Conclusion:** This Critical passes the remediation-value lens. The fix is cheap (a documentation
reconciliation the ADR authors have already demonstrated they can perform, per the Figure 3 caption
correction history), non-additive under the finder's own primary remedy, and materially corrects an
overstated safety claim on the register's highest-consequence risk — precisely the property (honest
risk bounding) the ADR claims as its reason for existing.

---

## Summary Table

| ID | Severity | Verdict | Basis |
|----|----------|---------|-------|
| DA-001-iter4 | Critical | VERIFIED | Genuine, citable contradiction (ADR lines 616-641 vs. line 903); fix is low-cost/non-additive per finder's own option (a); materially corrects an overstated mitigation claim on the register's top risk — not churn. |

**Verified:** DA-001-iter4
**Refuted:** (none — only one Critical was raised by this finder)
