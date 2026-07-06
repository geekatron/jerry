# Refutation Panel — Materiality Lens (Iteration 10, S-013 Inversion Technique)

> **Target report:** `projects/PROJ-031-cowork-skeleton/orchestration/adr-convention-20260702-001/adversary/iteration-010/s-013-findings.md`
> **Lens:** MATERIALITY — does the finding genuinely block the standard's purpose (collision-free identity, honest promotion, adoptable convention)? Cosmetic wording and negligible-probability-x-impact edge cases are REFUTED even if factually true. DEFAULT TO REFUTED IF UNCERTAIN.
> **Scope:** Critical findings only, using the finder's own IDs.
> **Criticals in target report:** 013-001 (only Critical; 013-002 is Major and out of scope for this panel).

---

## 013-001: "L-1 grammar rule and the grandfather regression test directly contradict each other on `ADR-150-001`" [claimed CRITICAL]

**Verdict: REFUTED**

**Reasoning:**

1. **The textual tension is real but the resolution is documented immediately adjacent, not absent.** The finding is correct that ADR:686 ("the canonical slug begins with a letter, so `ADR-150-001` (numeric-leading) is rejected") and ADR:691 ("18 files... pass L-1") read as contradictory in isolation. But the very next paragraph in the same section — ADR:693, under the identical heading `## Enforcement Design (L5 CI Lint)` — is titled exactly "How 'pre-adoption grandfathered' is operationalized on a subsequent edit" and states in plain terms: "A git-modified file that is already on that baseline is treated as **grandfathered-exempt from L-1/L-2**, not as a newly-minted ID." The mirror passage exists in `adr-standards-rule-draft.md:183`, in the same relative position (immediately after the 5-rule table and the grandfather-regression-test paragraph). An implementer who reads the section — not one isolated sentence — has an unambiguous, adjacent, cross-referenced instruction for exactly this case.

2. **This is not "previously-undisclosed."** The finding's own evidence trail names the mechanism as "the IN-001-iter8 spec clarification" (ADR:693, rule-draft:183) — i.e., this exact tension (does L-1's row wording, read alone, contradict the grandfather claim?) was already raised as a Critical by a prior S-013 Inversion pass (iteration 8) and disposed by adding precisely this exemption paragraph. See `subtraction-pass-notes.md:194`: *"IN-001 | S-013 | CLOSED-BY-EDIT | ... L-1 spec gained the grandfather-baseline clause so a later-edited legacy file (`ADR-150-001`) is exempt rather than new-bare, closing the deleted-L-12 gap by wording."* 013-001 is a re-litigation of the same seam, now demanding the fix be re-expressed as a literal three-way disjunction inside the table cell itself rather than in the adjoining paragraph — a stricter drafting preference, not a newly discovered defect.

3. **Materiality: no implementation failure is actually guaranteed.** The finding's central claim — "the mandatory pre-ship regression test cannot go green without an undocumented ad-hoc fix invented at build time" — is not supported once the adjoining paragraph is read as part of the same specification unit. A solo maintainer implementing M-6 from this document would build: (a) L-1's grammar regex, and (b) a ratification-time baseline exemption list, because the document tells them to do exactly that two sentences later, in the same section, under the same rule's discussion. The "fix" the finding recommends (fold the exemption into L-1's own row as a literal 3-way disjunction) is a valid drafting tightening, but its absence does not create a genuine build-time ambiguity — it is a stylistic/organizational preference about which paragraph carries which clause, not a gap in the substantive design. This is exactly the class of issue the materiality mandate directs to REFUTE: "cosmetic wording... REFUTED even if factually true."

4. **No risk to the standard's actual purposes.** Collision-free identity, honest promotion, and adoptability are not threatened by where within the document the grandfather-exemption sentence sits. The regression-test claim ("18 files pass L-1") is durable and correctly engineered once the whole section is read; the residual is a drafting-polish opportunity (best captured as Minor), not a Critical that blocks the package's core purpose.

**Disposition:** REFUTED under the materiality lens. (Note, non-binding: the underlying textual observation is accurate and a one-line edit folding the exemption into L-1's row would improve precision — but this does not rise to Critical materiality given the adjoining, cross-referenced, already-once-remediated resolution.)

---

## Summary

| ID | Claimed Severity | Verdict | Basis |
|---|---|---|---|
| 013-001 | Critical | **REFUTED** | Resolution is documented in the immediately adjacent paragraph (ADR:693 / rule-draft:183) under the same heading; the same seam was already raised and closed as IN-001-iter8; no genuine build-time ambiguity or purpose-blocking risk — cosmetic drafting preference, not a Critical defect. |

**013-002 (Major) is out of scope for this Critical-only refutation panel and is not adjudicated here.**
