# S-010 Self-Refine Findings — Iteration 5 (Group A)

| Field | Value |
|-------|-------|
| Strategy | S-010 Self-Refine |
| Deliverable | ADR-PROJ031-004 (canonical `ADR-adr-convention-001`) + companion `adr-standards-rule-draft.md` |
| Criticality | C4 (AE-002/AE-003 set a C3 floor; C4 by tier definition) |
| Date | 2026-07-02 |
| Reviewer | ps-architect (creator/owner — only tournament role with edit rights) |
| Iteration | 5 (S-010 pass) |

## Objectivity Assessment (Step 1)

High-attachment case (multi-iteration owned artifact; prior scores 0.67 / 0.54 / 0.62 / 0.59).
Per the template's conservative fallback, chose the stricter posture and applied leniency-bias
counteraction (target 5+ findings). The declining/oscillating score across iterations is itself
treated as a signal to hunt harder in the *annotation layer*, where the package's density can
hide consistency defects, rather than re-litigate already-settled substance.

## Summary

The package answers the crux ("is `project` the right scope key?") head-on and correctly (subject-vs-scope
= the mutability principle), carries genuine steelmans for all six options, keeps the honest Scheme-C
counter-case alive, and discloses its own residuals honestly. This pass found **one concrete, fixable
internal-consistency defect** — a Changelog row-order inversion, ironic because a prior iteration's
`SM-204` note claims to have fixed exactly that class — plus two minor precision items and four verified
strengths. The Major finding was fixed in place; the two minor items were judged not worth consistency-churn.

---

## Findings Table

| ID | Finding | Severity | Evidence | Affected Dimension | Disposition |
|----|---------|----------|----------|--------------------|-------------|
| SR-501 | Changelog row-order inversion: v1.5 listed *above* v1.4, breaking the ascending 1.0→1.3 table — the same class v1.4's `SM-204` claims to have fixed | **Major** | ADR (pre-fix) lines 807–812: rows read `1.0,1.1,1.2,1.3,1.5,1.4`; v1.4 row text: "**(SM-204)** Corrected this Changelog's own row order" | Internal Consistency | **FIXED** — deterministic line-swap (1.4 now precedes 1.5) + new v1.6 entry |
| SR-502 | Regression-test size described as both "16-file" and "19-file (16 dialect + 3 canonical)" | Minor | ADR:640 & rule-draft:199 say "16-file"; ADR:110 (G-2) says "19-file"; ADR:531 (M-6) says "16-file dialect / 19-file-exercised"; reconciled at ADR:711-728 | Internal Consistency | Noted; **not changed** (explicit reconciliation already present; editing risks new drift) |
| SR-503 | Scheme E lacks the explicit `**Pros:**` line the other 5 options carry (steelman→Cons→Fit) | Minor | ADR:207-212 (E) vs ADR:179-180/187-188/195-196/203-204/217-218 (A/B/C/D/F all have `**Pros:**`) | Methodological Rigor (even-handedness) | Noted; **not changed** (E's merits stated in-prose: Nygard/MADR original, C2=5 — steelman fairness substantively preserved) |
| SR-504 | Crux is answered head-on and robustly | Strength | ADR:267-322 — direct "No", mutability principle, 3 converging arguments (2 promotion-independent), honest Scheme-C counter-case, null-alternative benchmark, full sensitivity + adverse-regime | Completeness / Actionability | Verified — no change |
| SR-505 | MEDIUM rule draft carries zero uppercase HARD-tier keywords | Strength / clean | grep of rule-draft: no MUST/SHALL/NEVER/FORBIDDEN/REQUIRED/CRITICAL; lowercase "must"/"required" at rule-draft:203,205,217,226,229,231 are all lint-mechanism/check descriptions per the register discipline at rule-draft:299 & ADR:596 | Internal Consistency (tier vocabulary) | Verified — no violation |
| SR-506 | Nav tables + all in-page/cross-file anchors resolve (no dangling refs) | Strength / clean | All 25 ADR `##` + 14 rule-draft `##` covered in nav; 34 ADR + 14 rule-draft `](#…)` anchors each map to an existing heading slug (incl. em-dash/paren cases); cross-file links to `#l5-ci-lint-specification`, `#frontmatter-schema`, `#enforcement-design-l5-ci-lint`, `#frozen-and-grandfathered-legacy` all resolve | Traceability | Verified — no dangling refs |

Leniency-counteraction satisfied: 3 substantive findings (1 Major + 2 Minor) beyond the required minimum, plus 3 verifications that actively tested for the failure modes the task flagged.

---

## Finding Details (Critical / Major)

### SR-501 — Changelog row-order inversion (Major, Internal Consistency) — FIXED

- **Severity:** Major (the document's weakest dimension across every prior iteration is Internal
  Consistency, 0.52–0.55; this defect lives in exactly that dimension and is self-referentially ironic).
- **Evidence:** Before the fix, the Changelog table (ADR lines 807–812) read version order
  `1.0, 1.1, 1.2, 1.3, 1.5, 1.4` — v1.5 (iteration-4 full tournament) was placed *above* v1.4
  (iteration-4 S-010 self-refine). The v1.4 row itself contains: *"(SM-204) Corrected this
  Changelog's own row order (1.3 was listed above 1.2)."* So a prior iteration explicitly claimed to
  have fixed changelog ordering, yet a newer inversion shipped — the precise "convention that fails
  to follow its own convention" credibility hit an S-011/S-012 critic would seize on.
- **Impact:** Undermines the package's central selling point (internal rigor / self-compliance) and
  the "prose row is not evidence of completion" discipline it applies elsewhere. Low functional impact,
  high symbolic impact for a C4 governance ADR.
- **Fix applied:** Deterministic line-swap (via `uv run python`, no content mutated — the two rows
  carry Unicode minus/ellipsis/em-dash that manual reproduction would corrupt) so v1.4 now precedes
  v1.5; the table reads `1.0, 1.1, 1.2, 1.3, 1.4, 1.5`. Added a v1.6 entry recording the correction.
  Version numbers remain the authoritative chronology; the two entries' external references
  (rule-draft footer, remediation-notes filenames) are preserved because content did not move between
  version labels — only the physical row order was corrected.

---

## Recommendations

1. **(DONE)** SR-501 fixed in place; v1.6 entry added.
2. **(Optional, deferred)** SR-502: if a future structural pass touches the Enforcement-Design summary,
   harmonize the "16-file" phrasing to "16-file dialect / 19-file-exercised" for one-glance consistency.
   Not done now — the reconciliation already exists (ADR:711-728) and editing a poorly-consistency-scoring
   doc for a non-defect risks introducing new drift.
3. **(Optional, deferred)** SR-503: add a one-line `**Pros:**` to Scheme E for format parity with A/B/C/D/F.
   Not done — E's merits are already stated and the omission does not amount to a steelman-fairness violation.

---

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Positive | Crux, sensitivity, null-alternative, all six options, pre-mortem, migration all present (SR-504) |
| Internal Consistency | 0.20 | Negative → improved | SR-501 (Major) fixed; SR-502 a reconciled minor; tier-vocabulary clean (SR-505) |
| Methodological Rigor | 0.20 | Neutral | SR-503 minor even-handedness blemish; steelman-before-critique honoured across options |
| Evidence Quality | 0.15 | Positive | Claims carry file:line citations; qualitative estimates explicitly labelled as inference |
| Actionability | 0.15 | Positive | Migration plan, lint spec, promotion paths, ratification gates concrete |
| Traceability | 0.10 | Positive | Nav + anchors + cross-file links resolve; no dangling refs (SR-506) |

---

## Decision

**Outcome:** Ready for external review (this S-010 pass is complete; one Major defect fixed, minors documented).

**Rationale:** The package is substantively sound and now internally consistent on the one concrete
defect this pass surfaced. Remaining items are minor and reconciled-or-substantively-fine. The
INHERENT residuals (lint DESIGNED-not-BUILT, n=3 promotion evidence, single-maintainer waiver
self-certification, zero demonstrated Path-1 promotions) are honestly framed, not closable by a
document edit, and correctly left disclosed rather than papered over.

**Next Action:** Return to the tournament orchestrator for the remaining Group-A/B strategies.
No further owner edits required from S-010 beyond the SR-501 fix.
