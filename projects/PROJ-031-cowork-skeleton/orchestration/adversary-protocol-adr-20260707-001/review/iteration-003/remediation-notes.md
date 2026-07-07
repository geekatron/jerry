# Iteration-3 Remediation Notes — ADR-adversary-tournament-protocol-001

> **Disposition record** for the iteration-3 owner remediation pass (ps-architect).
> **Input score:** S-014 0.72 REVISE (VERIFIED-CRITICALS protocol), gate 0.92 (H-13).
> **Doctrine:** subtraction-first (D-3) — close by clarification / scope-narrowing / honest
> disclosure; add machinery only where completing existing backlog parity (H-32) requires it.
> **Constitutional:** P-003 (no subagents); P-020 (writes confined to
> `projects/PROJ-031-cowork-skeleton/`; deliverable is the ADR itself); P-022 (every disposition
> cites the finding's own file+line evidence; inference labeled).

## Navigation

| Section | Purpose |
|---------|---------|
| [Scope of This Pass](#scope-of-this-pass) | What was and was not remediated |
| [Disposition Table](#disposition-table) | Per-finding CLOSED/REBUTTED/RESIDUAL tag |
| [Panel-VERIFIED Criticals](#panel-verified-criticals) | Detailed fix per VERIFIED Critical |
| [High-Value Advisory Majors/Minors](#high-value-advisory-majorsminors) | Detailed fix per advisory item |
| [Not Remediated (Disclosed Residuals)](#not-remediated-disclosed-residuals) | Deferred with rationale |
| [Diagram Consistency](#diagram-consistency) | mmdc-consistency verification |

---

## Scope of This Pass

Remediates the **3 panel-VERIFIED Criticals** (DA-001-i3, DA-002-i3, CV-001-20260707iter3) plus the
**high-value advisory Majors/Minors** the S-014 report priority-ordered (CV-002-iter3, CC-001-iter3,
CC-002-iter3, CC-003-iter3, DA-003-i3, SM-002-iter3, SM-003-iter3, CC-004-iter3, DA-004-i3). All fixes
are text-level clarifications, honest disclosures, or backlog-parity completion — no HARD rule, weight,
threshold, criticality set, chosen decision (D-1..D-6), or Mermaid diagram source is changed. The
25/25 HARD-rule ceiling is untouched.

---

## Disposition Table

| Finding | Source | Severity | Panel | Disposition | Method |
|---|---|---|---|---|---|
| DA-001-i3 | S-002 | Critical | VERIFIED 3-of-3 | CLOSED-BY-CLARIFICATION | Retain unconditional rule as C1–C2 fallback (D-2 + L1 + WI-3 + new Neutral consequence) |
| DA-002-i3 | S-002 | Critical | VERIFIED 3-of-3 | CLOSED-BY-DISCLOSURE | Rewrite RSK-7 mitigation to honestly scope what WI-8 gates; align WI-7/WI-8 text + reversibility exemption |
| CV-001-20260707iter3 | S-011 | Critical | VERIFIED 2-of-3 | CLOSED-BY-DISCLOSURE | Add FU-log iter-7 (0.83) to evidence chain; reconcile 0.83→0.72 decline; correct L0 range to 0.72–0.88 |
| CV-002-20260707iter3 | S-011 | Major | out-of-panel | CLOSED-BY-CLARIFICATION | Qualify "grep confirms all-C4" → operative/scored criticality; disclose 5 C3 hits |
| CC-001-iter3 | S-007 | Major | unrefuted | CLOSED-BY-EDIT | Alignment "Implementation Effort" enumerates all 8 backlog items |
| CC-002-iter3 | S-007 | Major | unrefuted | CLOSED-BY-EDIT | Add draft Issue G for WI-8 (H-32 parity) |
| CC-003-iter3 | S-007 | Major | unrefuted | CLOSED-BY-EDIT | Set `scope: project` (ADR-M-007 descriptive reading); Meta-Note bullet narrates flip-at-promotion |
| DA-003-i3 | S-002 | Major | unrefuted | CLOSED-BY-DISCLOSURE | Add token/context-volume estimate alongside invocation count in Cost model |
| SM-002-iter3 | S-003 | Major (improvement) | advisory | CLOSED-BY-CLARIFICATION | Split remediation-value lens gating criterion (behavior change) from doctrinal annotation |
| SM-003-iter3 | S-003 | Major (improvement) | advisory | CLOSED-BY-EDIT | Add boundary-validation sub-criterion to WI-8 AC |
| CC-004-iter3 | S-007 | Minor | unrefuted | CLOSED-BY-DISCLOSURE | One-line disclosure that Strategy Catalog intentionally excludes S-016 |
| DA-004-i3 | S-002 | Minor | out-of-panel | CLOSED-BY-DISCLOSURE | RSK-7 probability caveat acknowledging the correlated-base tension |

---

## Panel-VERIFIED Criticals

### DA-001-i3 — C1–C2 auto-REVISE gate unreachable (VERIFIED 3-of-3) → CLOSED-BY-CLARIFICATION

The D-1 "no panel at C1–C2" + D-2 "only panel-VERIFIED Criticals auto-REVISE" combination would have
made the hard Critical gate structurally unreachable at C1–C2. Fixed by **scoping** verified-only
gating to *where a panel ran (C3/C4)* and **retaining the pre-existing unconditional
any-Critical→REVISE rule (`adv-scorer.md:166-167`) verbatim as the C1–C2 fallback**. No new machinery
(subtraction-first). Edits: D-2 decision row; D-2 Option-B con cell; D-2 "Why B" rationale (new C1–C2
fallback clause); L1 item 3 (criticality-scope, not blanket-replace); WI-3 AC; Fig. 1 caption (prose
only — diagram source unchanged); new Neutral Consequence #3 (closes the Completeness/self-audit angle).

### DA-002-i3 — RSK-7 generalization "gate" only blocks a doc pointer (VERIFIED 3-of-3) → CLOSED-BY-DISCLOSURE

Only WI-7 (SSOT doc pointer) depended on WI-8; the mechanism (WI-1–WI-5) ships genre-agnostically
(`adv-selector.md:89-107` keys on path/content, not genre). Fixed via honest scope-narrowing (option b,
D-3 doctrine): **rewrote RSK-7's mitigation and WI-7's precondition** to state WI-8 is *post-deployment
validation of the SSOT declaration only*, not a pre-deployment gate on the mechanism; named the genuine
safeguard — the MEDIUM-tier one-line `adv-selector` exemption path for any underperforming genre. The WI
dependency graph and the RSK-7 narrative now describe the same activation behavior (the finding's AC).

### CV-001-20260707iter3 — evidence chain omits iter-7; 0.83→0.72 decline undisclosed (VERIFIED 2-of-3) → CLOSED-BY-DISCLOSURE

Added the **FU-log iteration-007** paragraph (0.83 verified / 0.54 old, REVISE, 4 VERIFIED of 7 raw) to
the "verified protocol converges" chain, plus an **explicit reconciliation** of the 0.83→0.72 movement:
it is a *larger fresh crop* of genuine, panel-confirmed Criticals (6 vs. 4, incl. `DA-002-i8`), not a
recurrence — the D-4/D-5 pattern; the source corpus's own iter-8 report reconciled against iter-6, a gap
this ADR now surfaces rather than inherits. **Corrected the L0** "0.86–0.88 / four later rounds" claim to
the honest, non-monotonic **0.72–0.88 across four named rounds**. Evidence: iter-7 score
`s-014-quality-score.md:21,65-66,73` (0.83/0.54/REVISE).

## High-Value Advisory Majors/Minors

- **CV-002-i3 (Major, ironic overclaim):** qualified "grep confirms all-C4" to *operative/scored*
  criticality; disclosed the 5 `C3` hits from S-010 self-refine mislabeling (FU-log iter-1–5).
- **CC-001-i3 (Major):** Alignment "Implementation Effort" cell now enumerates all **8** backlog items
  (previously 6; omitted WI-6 runner guide + WI-8 validation pass).
- **CC-002-i3 (Major):** added **draft Issue G** for WI-8 (H-32 parity), cross-referencing the WI-7
  precondition; updated Issue F body + PS-Integration reference (A–F → A–G).
- **CC-003-i3 (Major):** set frontmatter **`scope: project`** (ADR-M-007 descriptive reading; flips to
  `framework` at the promotion git-mv per the convention's Promotion Process); added **Meta-Note bullet
  #4** naming the M-007/M-013 tension and its resolution so the first dogfood sets a citable precedent.
- **DA-003-i3 (Major):** added a **token/context-volume cost estimate** (~90–105k input tokens per
  Critical-bearing report for a ~950-line artifact; ~0.4–0.5M/round at C4) alongside the invocation
  count in the Cost model + Negative Consequence #1; WI-8 AC now records observed token volume.
- **SM-002-i3 (improvement):** split the remediation-value lens's **gating** criterion (behavior change)
  from its **doctrinal** annotation (subtraction style), so an expensive-but-real Critical cannot be
  wrongly refuted for needing additive machinery.
- **SM-003-i3 (improvement):** added a **boundary-falsification** sub-criterion to WI-8's AC
  (recurrence-signature check + C1/C2 counterfactual) so the pass can falsify the C3 boundary, not merely
  confirm the mechanism functions.
- **CC-004-i3 (Minor):** one-line disclosure that the Strategy Catalog intentionally excludes S-016
  (an adjudication template, not an 11th finder strategy).
- **DA-004-i3 (Minor):** RSK-7 probability caveat acknowledging the "maximally correlated" base could
  defensibly read HIGH; held at MED because the reversible escape-hatch caps *cost*, not *likelihood*.

## Not Remediated (Disclosed Residuals)

None deferred at Critical severity — all 3 panel-VERIFIED Criticals closed. All priority-1..8 advisory
items from the S-014 report were addressed (Majors and both Minors). No item was rebutted this round.

## Diagram Consistency

**Verified.** No Mermaid diagram source (inline fence or `.mmd`) was modified this pass — all DA-001
edits were prose (D-2/L1/WI-3 text + Fig. 1 *caption*). Fig. 1's `No, or C1-C2 → F` edge remains
accurate: at C1–C2 the scorer applies the retained unconditional rule, which the caption now states
explicitly. `diff` of the inline Figure-1 fence against `diagrams/fig1-pipeline.mmd` = **MATCH**; the
other three figures were untouched and remain byte-consistent with their persisted `.mmd`/`.svg`
sources (mmdc 11.12.0).
