# Refutation Panel: Materiality Lens — S-011 Findings (iteration-003)

## Navigation

| Section | Purpose |
|---------|---------|
| [Scope](#scope) | What is adjudicated in this pass |
| [Verdicts](#verdicts) | Per-Critical VERIFIED/REFUTED determination |
| [Summary](#summary) | Roll-up |

---

## Scope

Per the ADR's own protocol (`decisions/ADR-adversary-tournament-protocol-001-verified-criticals-methodology.md`, D-1/D-2/c-004: panels adjudicate Critical-severity claims only), this materiality-lens pass adjudicates the **one Critical** finding in `s-011-findings.md`: CV-001-20260707iter3. CV-002-20260707iter3 is Major-severity and is out of scope for panel adjudication (advisory only, no panel weight per the same protocol).

---

## Verdicts

### CV-001-20260707iter3 — Evidence chain omits FU-log iteration-007; "0.86–0.88... four later rounds" claim

**Verdict: REFUTED**

The underlying facts are independently confirmed accurate: FU-log iteration-007 scored 0.83 (VERIFIED-CRITICALS) vs. 0.54 (old-protocol) (`orchestration/fu-log-convention-20260705-001/adversary/iteration-007/s-014-quality-score.md:20,65-66`), it is never named in the ADR (confirmed via grep — zero hits for "iteration-007"/"iter-7" in the ADR body), and iteration-008's own delta reconciliation is explicitly against iteration-006, not iteration-007 (`.../iteration-008/s-014-quality-score.md:51-52,205-217`). The finding is factually sound. However, on materiality it does not clear the bar: the finding's own text repeatedly concedes it "does not overturn the chosen decision (D-1..D-6)" and that "the VERIFIED-CRITICALS protocol still clearly outperforms naive counting in the omitted round too (0.83 vs. naive 0.54)" — i.e., restoring the missing data point strengthens, not weakens, the case for adopting the methodology (every one of the four rounds beats its own naive-protocol counterpart: 0.83>0.54, 0.72>0.51, 0.86>0.68, 0.88>0.68). This is an L0/Context narrative-precision and evidence-completeness gap (the exact range "0.86–0.88" undercounts one data point; "four later rounds" is numerically defensible but not fully narrated), not a wrong decision, an unimplementable spec, or fabricated evidence — the D-1 through D-6 decisions, the `adv-verifier` design, and the six coordinated changes are unaffected by adding this one paragraph. Per the materiality lens's explicit instruction ("style/edge-cases REFUTED even if true" / "default REFUTED if uncertain"), this is refuted as immaterial to the ADR's decision, even though the underlying textual gap is real and worth a low-cost editorial fix (as the finder's own "Correction" section proposes).

---

## Summary

| ID | Verdict |
|----|---------|
| CV-001-20260707iter3 | REFUTED (materiality) |

CV-002-20260707iter3 (Major) is out of scope for this panel per the ADR's own "panels adjudicate Criticals only" rule and carries no panel verdict.

---

*Constitutional compliance: P-003 (no subagents invoked); P-020 (output confined to `projects/PROJ-031-cowork-skeleton/`, deliverable and s-011-findings.md not edited); P-022 (verdict cites file+line evidence independently re-derived from primary source files for this execution; no reliance on sibling review-panel outputs). Hygiene: all paths repo-relative; no absolute host paths or employer-internal tokens.*
