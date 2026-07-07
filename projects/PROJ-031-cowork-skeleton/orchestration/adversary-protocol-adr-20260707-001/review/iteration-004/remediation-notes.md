# Iteration-4 Remediation Notes — ADR-adversary-tournament-protocol-001

> Owner remediation pass responding to the iteration-4 S-014 quality score (0.75, gate 0.92).
> Doctrine: subtraction-first (close by reconciliation/wording/disclosure; add no machinery).
> Scope guard (P-020): edits confined to `projects/PROJ-031-cowork-skeleton/`; no `.context/`,
> `skills/`, or `docs/` file touched. No HARD rule, weight, threshold, criticality set, chosen
> decision (D-1..D-6), or Mermaid diagram source changed; 25/25 ceiling untouched.

## Navigation

| Section | Purpose |
|---------|---------|
| [Target](#target) | What the score flagged |
| [Disposition Table](#disposition-table) | Per-finding action, tag, evidence |
| [Detail](#detail) | Before/after rationale per fixed finding |
| [Non-Propagation / Diagram Note](#non-propagation--diagram-note) | Why no diagram source changed |

---

## Target

- **Prior score:** 0.75 (iteration 4), gate >= 0.92 (H-13).
- **Panel outcome:** 1 of 2 claimed Criticals VERIFIED — `DA-001-iter4` (3-of-3). `CC-001-iter4`
  REFUTED 0-of-3 (unanimous) → zero weight, no edit.
- **This pass:** fix the panel-VERIFIED Critical (`DA-001-iter4`) plus the high-value unrefuted
  advisory Majors, subtraction-first; sweep the cheap Minors that ride along for free.

---

## Disposition Table

| Finding | Sev | Panel | Tag | Action |
|---------|-----|-------|-----|--------|
| DA-001-iter4 | Critical | VERIFIED 3-of-3 | CLOSED-BY-EDIT | Narrow RSK-1 mitigation #3 to the pre-verified transition window; re-price residual honestly against the already-correct Figure 3 (no diagram change). |
| CC-001-iter4 | Critical | REFUTED 0-of-3 | REBUTTED | No edit — panel traced the Tier Vocabulary SSOT's registration scope; zero weight. |
| DA-002-iter4 | Major | advisory | CLOSED-BY-EDIT | Cross-reference RSK-1 mitigation #1 to RSK-2's correlated-error caveat. |
| SM-003-iter4 | Major | advisory | CLOSED-BY-EDIT | Scope blindness-ordering structural-guarantee language to the true-parallelism branch; name the ordering-barrier branch procedural. |
| DA-003-iter4 | Major | advisory | CLOSED-BY-DISCLOSURE | Disclose the cost worked-example as a deliverable-term-only lower bound; note cited-evidence term is additive and can dominate. |
| CV-001-iter4 | Major | advisory | CLOSED-BY-EDIT | Correct "reaffirmed across iterations 6, 7, 8, and 9" to 2 genuine reaffirmations (iter-6/7) + 2 unchecked rounds (8/9); fix RSK-2 + Positive Consequence #2 echoes. |
| SM-001-iter4 | Major | advisory | CLOSED-BY-DISCLOSURE | Add one-line order-of-magnitude derivation for "~250 agent runs" at L0 + footer. |
| CC-002-iter4 | Major | advisory | CLOSED-BY-DISCLOSURE | Relabel `adv-verifier` tier honestly (nominal T2 Read-Write category, tools restricted to `Read, Glob, Grep, Write`, no `Edit`/`Bash`) so an H-34 audit reads an intentional restriction, not a mislabel. |
| DA-004-iter4 | Major | advisory | CLOSED-BY-EDIT | Soften RSK-7 "genuine safeguard" to bound *cost* of failure, not *likelihood*, consistent with its own probability caveat. |
| DA-005-iter4 | Minor | advisory | CLOSED-BY-EDIT | Clarify D-1 decision row + Fig.1 caption: C3/C4 panel every claimed Critical identically (shorthand denotes strategy-set/ceiling, not a panelling-rate gradient). |
| CC-003-iter4 | Minor | advisory | CLOSED-BY-EDIT | Resolve compound `forensic/convergent` cognitive mode to single enum `forensic`. |
| CC-004-iter4 / CV-002-iter4 | Minor | advisory | CLOSED-BY-EDIT | Narrow `adv-scorer.md:166-167` citations to `:166`; correct RSK-4 "~9–10 reports" to "at most 9". |
| SM-002-iter4 | Minor | advisory | CLOSED-BY-EDIT | Re-true "~950-line" cost self-reference to current length (~1,055 lines); folded into DA-003 cost-model edit. |
| SM-004-iter4 | Minor | advisory | CLOSED-BY-EDIT | Add split-permitted note to WI-8 sizing (three-axis AC). |

---

## Detail

**DA-001-iter4 (VERIFIED 3-of-3) — RSK-1 mitigation #3 vs. Figure 3 scope.** The contradiction is
between the RSK-1 prose and the (already-correct, iteration-2-redrawn) Figure 3. Fix option (a):
narrowed mitigation #3 to state it applies *only during the pre-verified-protocol transition window*
(the recurrence check `Q2` lives solely in Figure 3's old-protocol branch), and added an explicit
**honest re-pricing** — in steady-state verified-protocol operation the residual is bounded by
counterweights (1),(2),(4) only. No machinery added; no diagram changed. Also qualified mitigation #1
(DA-002-iter4) with a forward reference to RSK-2's correlated-error caveat.

**SM-003-iter4 — blindness-ordering structural vs. procedural.** Scoped the "structural guarantee"
language to the true-parallelism branch (the only branch that makes blindness architectural, per the
ADR's own L2 doctrine); named the ordering-barrier fallback a procedural/behavioral control to be
documented in the WI-6 runner guide.

**DA-003-iter4 / SM-002-iter4 — cost worked-example.** Disclosed the worked figure as a
deliverable-term-only lower bound; noted the cited-evidence term is additive and can push true cost
2–5× higher; re-trued the stale "~950-line / ~90–105k" figures to "~1,090-line / ~100–115k" and
reframed the estimate as order-of-magnitude so it needs no re-truing per pass. Applied at the Cost
model and Negative Consequence #1.

**CV-001-iter4 — fabricated-claim reaffirmation count.** Corrected "reaffirmed across iterations 6, 7,
8, and 9" to two genuine independent re-verifications (iter-6/iter-7) plus two rounds where the claim
was merely carried unchecked (iter-8/iter-9), per the ADR's own cited `post-ceiling-fix-notes.md:57`.
Applied at the Context incident, its "survived four blind rounds" sentence, RSK-2, and Positive
Consequence #2.

**SM-001-iter4 — "~250 agent runs" derivation.** Added a one-line order-of-magnitude accounting
(~230–270) at L0 and the footer.

**CC-002-iter4 — `adv-verifier` tier label.** Relabelled honestly: `tool_tier: T2` (nominal Read-Write
risk category) with `tools` deliberately restricted to `Read, Glob, Grep, Write` (no `Edit`/`Bash`),
flagged so an H-34 audit reads an intentional documented restriction rather than a mislabel — no
amendment to the canonical tier table (which this ADR does not touch). Applied at L1 item 1 and both
D-6 table cells.

**DA-004-iter4 — RSK-7 "genuine safeguard."** Softened to state the MEDIUM-tier reversibility bounds
the *cost* of a transfer failure, not its *likelihood*, consistent with RSK-7's own probability caveat.

**Minors.** DA-005 (D-1 row + Fig.1 caption gloss: C3/C4 panel identically); CC-003 (single-enum
`forensic`); CC-004/CV-002 (`adv-scorer.md:166` quote citations; RSK-4 "at most 9" reports); SM-004
(WI-8 split-permitted sizing note).

---

## Non-Propagation / Diagram Note

- **DA-001-iter4** is closed by reconciling the RSK-1 prose *to* Figure 3, which the iteration-2
  redraw already made correct (recurrence check confined to the old-protocol branch). No `.mmd`
  source and no rendered `.svg` is changed by this pass; all four diagrams remain mmdc-consistent.
- **DA-005-iter4** is closed in prose only (D-1 decision row + Fig.1 *caption*, which is prose, not
  Mermaid). The Figure 1 `.mmd` edge label "C4 all / C3 Criticals-only" is retained as valid
  shorthand and now glossed by the caption, so no re-render is required.
