# Refutation Panel — Factual Lens (Iteration 4, S-002 Devil's Advocate)

## Navigation

| Section | Purpose |
|---------|---------|
| [Scope](#scope) | What was reviewed and how |
| [Verdicts](#verdicts) | Per-Critical VERIFIED/REFUTED with evidence |
| [Summary](#summary) | Panel result |

---

## Scope

**Target report:** `orchestration/adversary-protocol-adr-20260707-001/review/iteration-004/s-002-findings.md` (S-002 Devil's Advocate, iteration 4)
**Target deliverable:** `decisions/ADR-adversary-tournament-protocol-001-verified-criticals-methodology.md`
**Lens:** Factual accuracy only — does the alleged defect exist at the cited lines? Materiality and remediation-value are out of scope for this lens.
**Default:** REFUTED if uncertain.
**Criticals adjudicated:** 1 (DA-001-iter4). Majors/Minors are not panelled per protocol (panels adjudicate Criticals only).

---

## Verdicts

### DA-001-iter4 — VERIFIED

**Claim:** RSK-1 mitigation #3 ("the convergence discriminator (D-4) re-surfaces a genuinely recurring defect in a later round if it is wrongly refuted once") is contradicted by Figure 3's own scoping, which confines the recurrence check to the pre-verified/old-protocol branch only.

**Factual check:** The RSK-1 quote is verbatim at `decisions/ADR-adversary-tournament-protocol-001-verified-criticals-methodology.md:903`. Figure 3's mermaid source (lines 616-636) confirms the structure exactly as described: the `Q2{"Do claimed Criticals RECUR across independent rounds?"}` node exists only under the `PROTO -- "No (old protocol, no panels yet)"` branch (line 620); the `PROTO -- "Yes (verified protocol)"` branch (line 625) routes only through `Q1{"Any VERIFIED Criticals this round?"}`, with no path back to a recurrence check for a REFUTED verdict. The caption at lines 638-641 states this scoping explicitly and in the ADR's own words: "The recurrence discriminator applies only in the pre-verified (old-protocol) mode... once the verified protocol is running, any VERIFIED Critical routes unconditionally to remediation (FIX)" — REFUTED claims are not mentioned as having any downstream path.

Tracing the diagram further sharpens the point: under verified-protocol mode, if no Critical is VERIFIED this round (e.g., because a real one was wrongly REFUTED) and the composite is at or above gate, the flow reaches `PASS` (line 627) and the tournament terminates — structurally precluding any "later round" in which recurrence could even be checked. This is a genuine, verifiable textual/diagrammatic inconsistency between RSK-1's mitigation-#3 language and the ADR's own Figure 3 (source + caption), not a misread, a stale reference, or a restatement of an already-disclosed limitation — RSK-1's text does not itself disclose this scoping restriction, and the finding's line citations (903 for the claim; 616-636 and 638-641 for the diagram) all resolve to the quoted content exactly as characterized.

**Verdict: VERIFIED.**

---

## Summary

| ID | Verdict |
|----|---------|
| DA-001-iter4 | VERIFIED |

1 of 1 claimed Critical VERIFIED under the factual-accuracy lens. No misreads, stale references, or restatements-of-disclosed-limits were found; the cited lines resolve exactly as the finding describes, and the internal contradiction between RSK-1's mitigation-#3 claim and Figure 3's own scoped decision tree is real and independently confirmable from the deliverable text alone.
