# S-012 Refutation Panel — Materiality Lens (Iteration 10)

## Navigation

| Section | Purpose |
|---------|---------|
| [Scope](#scope) | What this panel reviewed |
| [Verdicts](#verdicts) | Per-Critical verdict + reasoning |
| [Summary](#summary) | Tally |

---

## Scope

Target report: `projects/PROJ-031-cowork-skeleton/orchestration/adr-convention-20260702-001/adversary/iteration-010/s-012-findings.md` (S-012 FMEA, iteration 10).

Only Critical-severity findings are in scope for this refutation panel per mandate. The S-012 report names exactly **one** Critical: **012-004**. (012-005 and 012-006 are Major and out of scope for this panel.)

Lens: **Materiality** — does the finding genuinely block the standard's purpose (collision-free identity, honest promotion, adoptable convention)? Default to REFUTED if uncertain; edge cases with negligible probability x impact are REFUTED even if factually true.

---

## Verdicts

### 012-004: Grandfather-baseline enumeration excludes PROJ-014's bare drafts, which L-2's unscoped wording would otherwise catch

**Verdict: REFUTED**

**Reasoning:**

1. **The entire mechanism is not-yet-built and may never ship.** `scripts/lint_adr_convention.py` does not exist (ADR line 659: "Claim-Status: the lint is DESIGNED, NOT BUILT... nothing today prevents a non-compliant ADR from merging"). The document's own pre-mortem rates "nothing lands" (M-6 never ships) as "the single best-evidenced risk in this package" (ADR line 501, FM-5). The finding's own corrective-action framing concedes this is a "specification-level reading, not an observed CI failure" (finding 012-004 Analysis, bracketed P-022 note). A defect in an unbuilt, possibly-never-built artifact's spec text is not a live blocker of the standard's purpose today.

2. **Even if M-6 is built exactly to the letter of the current spec, the consequence is bounded and trivially overridable.** The lint is explicitly MEDIUM-tier: "a FAIL is overridable with a documented justification in the PR description... no waiver ledger, no CODEOWNERS gate" (rule draft line 167; ADR line 657). The worst-case outcome the finding describes — a future git-modify (e.g., a typo fix) of one of exactly 4 already-named legacy files triggering an L-2 advisory flag — costs one PR-comment justification, not a collision, not a broken citation, and not a defeated promotion. This is precisely the class of "negligible probability x impact" edge case the materiality lens instructs to refute.

3. **The scenario requires a specific, narrow conjunction of future events**: (a) M-6 gets built: contingent per FM-5; (b) it is built with the baseline enumerated exactly as "18 + STORY015 = 19" with no accommodation for PROJ-014 (plausible but not certain — an implementer reading the Migration Plan row at ADR line 517, which already flags these 4 files by name and disposition, would very plausibly fold them in); AND (c) someone specifically git-modifies one of those 4 named, already-flagged-as-low-priority-transient files before that promotion/rename happens. Occurrence is not "6/10" (as rated in the finding) under this reading — it requires all three conditions to co-occur against a corpus the Migration Plan already tags "Low priority" (ADR line 517).

4. **L-2's "anywhere" scope is plausibly a deliberate design choice, not an inconsistency.** Unlike L-1 (a per-file grammar check reasonably scoped to canonical homes), L-2 exists specifically to catch *new bare-ID creation* wherever it might occur — an intentionally broader net than L-1's grammar check. The finding treats the absence of an explicit scope qualifier on L-2 as an "Inconsistent" defect (Strategy Step: Inconsistent lens), but a rule with a deliberately wider catch-scope than a sibling rule is a design decision, not automatically a contradiction — especially given D-5's dedicated "Topology-scope of the lint's collision-safety" disclosure (ADR line 235) already discusses L-1/L-3/L-4/L-7 scope explicitly, and its silence on L-2 is at least as consistent with "L-2 is meant to be unscoped" as with "L-2's scope was overlooked."

5. **The underlying fact pattern is already disclosed, just not by the specific "L-2 false-positive" framing.** The Migration Plan row for PROJ-014 (ADR line 517) already states these 4 files are "Transient, colliding with docs/adrs/" with an explicit remediation path ("rename... only if promoted"), and the rule draft's Frozen-and-Grandfathered-Legacy section (line 94) already separately calls out these exact 4 files as "not a recognized dialect" — distinguishing them from the true grandfathered-dialect corpus. A reader is put on notice that these 4 files sit outside the normal dialect/canonical taxonomy; the residual the finding surfaces is an implementation nuance of that already-disclosed special status, not a new collision-integrity gap threatening the standard's core purpose (collision-free identity, honest promotion, adoptability).

**Conclusion:** 012-004 identifies a real textual gap in an as-yet-unbuilt CI-lint specification affecting exactly 4 named legacy files, with a worst-case consequence of one overridable PR-comment-level CI advisory — not a collision, not a broken promotion, not an adoption blocker. Under the materiality lens this is refuted.

---

## Summary

| Finding ID | Severity (as reported) | Verdict |
|---|---|---|
| 012-004 | Critical | **REFUTED** |

**Verified Criticals: 0. Refuted Criticals: 1 (012-004).**

No other Critical findings exist in the target report to adjudicate (012-005 and 012-006 are Major, out of scope for this Critical-only panel).
