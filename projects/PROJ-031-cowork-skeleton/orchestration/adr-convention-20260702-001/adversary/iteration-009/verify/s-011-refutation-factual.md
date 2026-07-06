# Refutation Panel — S-011 Findings, Factual-Accuracy Lens (Iteration 9)

**Target report:** `projects/PROJ-031-cowork-skeleton/orchestration/adr-convention-20260702-001/adversary/iteration-009/s-011-findings.md`
**Lens:** Factual accuracy — does the cited defect actually exist in the current deliverables at the cited locations?
**Scope:** Critical findings only (this panel does not adjudicate Minor findings). The report contains exactly one Critical finding: **011-001 (CV-001)**.
**Method:** Re-read every cited line in the current `ADR-PROJ031-004-adr-identifier-convention.md` and cross-checked against `subtraction-pass-notes.md`'s residual register (R-1..R-17) and disposition tables. No other refuters'/panels' output read (blind protocol).

---

## 011-001 (CV-001): "near-zero forced churn (D-4)" vs. D-4's own carve-out for this ADR

**Verdict: REFUTED**

**Citation accuracy check (all confirmed exact, no misreading of the quotes themselves):**
- ADR:438 reads exactly as quoted: *"the 15 pre-existing project/entity dialect ADRs (16 incl. this ADR) are grandfathered; PROJ-031's set already migrated. Net near-zero forced churn (D-4)."* (confirmed verbatim, Consequences → Positive, item 4).
- D-4 (ADR:223) reads exactly as quoted: *"This ADR is the one disclosed exception to 'in place': its current filename is a valid dialect, but it is itself scheduled for Path-2 self-promotion out of the dialect (M-9…), so it does not remain in place."* (confirmed verbatim).
- Migration Plan (ADR:511) reads exactly as quoted: this ADR's own row Cost = **"Low"** (recalibrated from "Trivial" per FM-006-iter7, multi-part rename+tombstone+reciprocal-link-repair), distinct from the "Project-scoped families" row (ADR:509) Cost = **"Zero."**

So every individual quotation the finder extracted is real and correctly transcribed. The refutation is not on transcription grounds — it is on the *inferential leap* from those quotes to "internal citation mismatch."

**Why the inference does not hold as a genuine, previously-undisclosed contradiction:**

1. **The operative word is "near," not "zero."** ADR:438 never claims this ADR (or the framework ADRs) incur *zero* churn — it claims *net near-zero*. The finder's argument requires reading "near-zero" as if it asserted exact-zero for all 16 items, then treating the one disclosed non-zero item as a violation of that (unstated) exact-zero claim. But "near" is precisely the hedge that accommodates a small number of non-zero-but-Low items inside an otherwise-zero-cost set.
2. **The same bundled sentence already contains a second "Low, not Zero" item that the finder does not flag** — the Migration Plan row for "3 framework ADRs" (ADR:508) is also Cost **"Low"** (optional YAML/`origin_project` retrofit, M-11), not "Zero," even though ADR:438's first clause says "the 3 framework ADRs already comply." If "near-zero" were meant literally as "zero" per named item, it would already be inaccurate for the framework-ADR clause independent of this ADR — which is strong evidence the author's chosen wording ("near-zero," not "zero") is deliberate aggregate hedging across *two* known Low-cost exceptions (framework retrofit + this ADR's Path-2 promotion), not an oversight confined to this ADR alone.
3. **The alleged contradiction is not hidden — it is repeated at high density in the same document, immediately adjacent to the very D-4 text the finder quotes.** D-4 itself (the cited source) discusses this ADR's own carve-out in the same paragraph the finder quotes from (ADR:223-231). The Migration Plan (ADR:511) restates the Low/multi-part cost. An entire dedicated section, **Meta-Note: This ADR's Own Identity and Remap Path** (ADR:711-721), re-discloses the same fact a third time, including the AE-004/C4 gating and the "worked example of its own Path-2 promotion" framing the finder cites as evidence of the document's "flagship pedagogical claim." A reader of this ADR encounters this exact fact (this-ADR's-cost-is-Low-not-Zero) three separate times before or immediately after Consequences-Positive-4 — this is the opposite of an "incomplete propagation of a fix" silently missed by an editor; it is a fact the document goes out of its way to repeat.
4. **"Grandfathered" and "does not remain in place" are not contradictory claims about the same point in time.** "Grandfathered" in this document's usage (D-3/D-4) consistently means "the existing dialect filename is valid *today*, without requiring an immediate forced rename to comply with the new convention." D-4's own text supports exactly that for this ADR ("its current filename is a valid dialect"). The *separate* fact that this ADR additionally plans a **voluntary, self-initiated** Path-2 promotion (M-9, framed as a pedagogical demonstration, not a compliance requirement — see Meta-Note:717, "This makes the ADR a worked example… the discouraged rename it exists to help future authors avoid") is a forward-looking, author-elected action, not evidence that "grandfathered" was misapplied to describe today's filename validity.

**Conclusion:** The citations are factually accurate, but the "internal citation mismatch" reading requires ignoring (a) the qualifying word "near," (b) a second Low-cost item bundled in the same sentence that the finder's own theory would also indict, and (c) the fact that this exact tension is disclosed three times in the same document, including in a section titled specifically to address it. This is not a genuine previously-undetected defect at the cited lines; it is a strained reading of already-abundant, already-cross-referenced disclosure. Per the factual-accuracy lens's default-to-refute-when-uncertain instruction, and given the "near" qualifier plus triple redundant disclosure make the "uncontradicted-zero" reading the less plausible one, **011-001/CV-001 is REFUTED.**

---

## Summary

| Finding ID | Severity (as reported) | Verdict |
|---|---|---|
| 011-001 (CV-001) | Critical | **REFUTED** |

011-002 (CV-002) is reported as Minor and is out of scope for this Critical-only refutation panel.

**Refuted:** 011-001
**Verified:** (none — the sole Critical finding was refuted)

*No subagents spawned (P-003). No files edited outside mandate (P-020). All verdicts cite file+line from the current deliverables; inferential reasoning is labeled as such (P-022).*
