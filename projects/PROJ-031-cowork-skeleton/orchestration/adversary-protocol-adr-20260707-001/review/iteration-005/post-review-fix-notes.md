# Iteration-5 Post-Review Fix Notes — ADR-adversary-tournament-protocol-001

> Post-review remediation pass on the two iteration-5 panel-VERIFIED Criticals. **No re-score is
> claimed**: iteration-5 scored S-014 **0.74 REVISE** (2 of 2 claimed Criticals VERIFIED); these two
> fixes close both VERIFIED Criticals. Owner: ps-architect (creator/owner of the ADR). Version:
> **0.5 → 0.6**.

## Navigation

| Section | Purpose |
|---------|---------|
| [Scope](#scope) | What this pass covers |
| [CV-001-20260707iter5 (VERIFIED 3-of-3)](#cv-001-20260707iter5-verified-3-of-3) | Fabricated-verification-incident miscount |
| [DA-001-iter5 (VERIFIED 2-of-3)](#da-001-iter5-verified-2-of-3) | Phase-2 escalation-trigger observability |
| [Disposition Table](#disposition-table) | Finding → action mapping |
| [Invariants Held](#invariants-held) | What was deliberately not changed |

---

## Scope

Two panel-VERIFIED Criticals from `review/iteration-005/s-014-quality-score.md`:

- **CV-001-20260707iter5** (S-011 Chain-of-Verification, unanimous 3-of-3) — Evidence Quality /
  Internal Consistency.
- **DA-001-iter5** (S-002 Devil's Advocate, 2-of-3: factual VERIFIED, materiality REFUTED,
  remediation-value VERIFIED) — Internal Consistency.

Advisory Majors/Minors (DA-002..DA-006-iter5, CC-001..CC-003-iter5, CV-002-20260707iter5, SM-001..
SM-006-iter5) are **out of scope** for this pass (panels adjudicate Criticals only; advisory items are
non-gating per D-2) and are not addressed here.

---

## CV-001-20260707iter5 (VERIFIED 3-of-3)

**Defect:** The flagship "fabricated-verification incident" narrative (Context section) self-contradicted
on the re-verification count: it read **"three checks in total: FM-010 at iter-6; PM-001-iter007 and
VQ-019 at iter-7,"** while RSK-2 and Positive Consequence #2 said **"two,"** and the cited
`PM-001-iter007` does not examine the PR-template claim.

**Primary-source verification (not by picking one of the two internal claims):**

| Primary source | States |
|----------------|--------|
| `.../iteration-010/post-ceiling-fix-notes.md:57` | "reaffirmed at iter-6 (FM-010), iter-7 (VQ-019)" → **two** events; `PM-001-iter007` not mentioned |
| `.../iteration-010/s-001-findings.md:37` (RT-001-iter010, the primary incident source) | "**two** independent prior 'Glob-verified absent' checks (S-012 iteration-6 FM-010, S-011 iteration-7 VQ-019)" |
| `.../iteration-007/s-004-findings.md:39,49` (actual `PM-001-iter007` content) | A Pre-Mortem-table-completeness finding ("Compound 'nothing lands' scenario … not modeled as its own row in the ADR's own Pre-Mortem/Failure-Modes table") — **never examines** the PR-template claim |

**Authoritative true count: TWO checks — FM-010 (S-012) at iter-6; VQ-019 (S-011) at iter-7.**
`PM-001-iter007` is a spurious third with no bearing on the PR-template question.

**Fix:** Stated the count **once authoritatively** in the Context incident ("exactly two checks — FM-010
(S-012) at iter-6 and VQ-019 (S-011) at iter-7"), with both primary-source citations and an explicit
note that `PM-001-iter007` is unrelated (so a future editor cannot re-introduce it). RSK-2 and Positive
Consequence #2 (and the second in-section count reference) re-pointed to that authoritative statement;
correction marker updated iter4 → **iter5**.

---

## DA-001-iter5 (VERIFIED 2-of-3)

**Defect:** The Phase-2 escalation trigger for RSK-1/RSK-2 ("open Phase 2 … if residual exposure … is
observed in ≥1 of the first 3 post-ratification C3/C4 tournaments") presupposed a persistent
panel-REFUTED record that the D-3 disposition-table taxonomy (CLOSED-BY-DELETION / CLOSED-BY-EDIT /
CLOSED-BY-DISCLOSURE / REBUTTED / RESIDUAL-DISCLOSED, `:251-253`) does not define.

**Two candidate fixes (per the finding's own acceptance criteria):**

1. Add a `PANEL-REFUTED` column/field to the disposition-table spec (text, not machinery).
2. Re-word the trigger to use records the taxonomy/artifacts already provide.

**Chosen: option 2 (re-word).** Justification:

- The REFUTED verdicts **already persist** in the per-round `verify/{report-id}-{lens}.md` files and in
  each score report's panel-reconciliation table. RSK-2 already states verdicts are "persisted as
  separate files for audit," and the finding's **own materiality lens** (`verify/s-002-materiality.md`)
  REFUTED it precisely because "no persistent record anywhere" overstates the gap — the `verify/`
  directories are the persistent record.
- Adding a `PANEL-REFUTED` taxonomy field is **additive attack surface** (violates D-3 subtraction-first)
  that would not make an *un-re-raised* false negative any more detectable, and risks re-introducing the
  cross-round memory the panel is deliberately blind to (RSK-1, "no cross-round memory feeding the
  panel").

**Fix:** Re-worded the trigger to honestly scope observability: a false *refutation* is not
auto-detectable; it is observable only **opportunistically** — when a later blind finder rotation
independently re-raises the substance of a previously-REFUTED Critical and the panel VERIFIES it, at
which point the owner's mandatory **D-5 delta-reconciliation** cross-references the persisted prior-round
REFUTED verdict in the `verify/` files. Absent such re-raising, the residual is disclosed as currently
**unmonitored**, not merely "mitigated." RSK-1's mitigation prose updated to match.

---

## Disposition Table

| Finding | Panel verdict | Dimension | Action | Site(s) |
|---------|---------------|-----------|--------|---------|
| CV-001-20260707iter5 | VERIFIED 3-of-3 | Evidence Quality / Internal Consistency | CLOSED-BY-EDIT (authoritative single statement + primary-source citations) | Context incident; RSK-2; Positive Consequence #2; in-section back-reference |
| DA-001-iter5 | VERIFIED 2-of-3 | Internal Consistency | CLOSED-BY-EDIT (trigger re-worded to existing artifacts; residual honestly disclosed as unmonitored) | L2 Evolution-path trigger; RSK-1 mitigation |

---

## Invariants Held

- No HARD rule, weight, threshold, criticality set, or chosen decision (D-1..D-6) changed.
- 25/25 HARD-rule ceiling untouched.
- 4 Mermaid diagram sources unchanged; captions unchanged.
- 18-section navigation table intact (H-23); no section headers added/removed.
- Zero hardcoded absolute home-directory paths; zero employer-internal tokens; repo-relative citations only.
- Changelog appended honestly: v0.6, "no re-score claimed."
