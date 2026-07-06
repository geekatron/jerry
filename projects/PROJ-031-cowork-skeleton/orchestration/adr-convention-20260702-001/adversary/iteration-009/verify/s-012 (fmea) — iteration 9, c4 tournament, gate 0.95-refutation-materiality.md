# Adversarial Refutation Panel — Iteration 9, Materiality Lens

> **Target report:** `projects/PROJ-031-cowork-skeleton/orchestration/adr-convention-20260702-001/adversary/iteration-009/s-012-findings.md` (S-012 FMEA, iteration 9, C4 tournament, gate 0.95)
> **Lens:** Materiality — does the finding genuinely block the standard's purpose (collision-free identity, honest promotion, adoptable convention)? Edge cases, cosmetic wording, and style preferences are REFUTED even if factually true. Default to REFUTED when uncertain.
> **Scope:** All three Critical findings in the target report (012-001, 012-002, 012-003). Majors/Minors (012-004, 012-005) are out of scope per the panel mandate ("attempt to REFUTE every Critical finding").
> **Blind protocol:** Sibling refuter outputs and other panels' outputs NOT read. Read: target S-012 report, both current deliverables (ADR-PROJ031-004 v1.10, adr-standards-rule-draft.md), and `subtraction-pass-notes.md` (disposition record + R-1..R-17 register).

---

## Navigation

| Section | Purpose |
|---------|---------|
| [012-001](#012-001-plugin-distribution-zero-tooling-guidance-overclaim) | Verdict + reasoning |
| [012-002](#012-002-no-general-schema-field-or-lint-check-for-the-adrcompanion-rule-file-relationship) | Verdict + reasoning |
| [012-003](#012-003-grandfather-baseline-temporal-anchor-creates-an-unbounded-post-ratification-amnesty-window) | Verdict + reasoning |
| [Summary](#summary) | Final verdict table |

---

## 012-001: Plugin-Distribution "Zero-Tooling Guidance" Overclaim

**Verdict: REFUTED**

**Reasoning:** The cited sentence at `ADR-PROJ031-004:675` ("What carries value downstream on day one is the *guidance*, which needs no tooling") sits inside a paragraph whose own preceding sentences already discharge the P-022 honesty burden for the *enforcement/lint* half of the claim ("no committed timeline is attached — it is adopter-dependent"), and the document elsewhere already discloses, in detail and more than once, that the guidance has *not* yet been relocated: Status section (`:89`) states plainly "'in force' today means *for a reader of this ADR or its companion rule draft* — the guidance has **not yet been relocated** to the auto-loaded `.context/rules/adr-standards.md` (Migration-Plan M-2, Glob-verified absent)"; Migration-Plan M-2 is flagged `TBD-Task` with an explicit unresolved Claim-Status block (`:525`). The finding's own proposed fix — one more sentence connecting two already-disclosed facts (M-2 pending; `projects/` is stripped) — is a clarity polish on top of extensive existing disclosure, not a new material gap.

More decisively on materiality: the audience the finding claims could be misled (a downstream plugin/CoWork recipient) cannot actually encounter the overclaiming sentence in the first place — the ADR document itself lives at `projects/PROJ-031-cowork-skeleton/decisions/ADR-PROJ031-004-adr-identifier-convention.md`, which is inside the same `projects/` tree stripped by `phase3-skeleton-generation-design.md:159` ("`git rm -r projects/ tests/ skills/.graveyard .github`"). Only a *source-repo* reader (who already has full access to the Migration-Plan TBD-Task disclosures, the Status section's "not yet relocated" caveat, and the Enforcement-Scope table) would ever read line 675 — and that reader already has the context to interpret "day one" as describing the intended post-M-2 state, not a claim about the present moment. The practical harm of the alleged overclaim is therefore negligible: the one audience that could be misled never sees the sentence; the audience that sees the sentence already has the disclosures needed to read it correctly. This is exactly the kind of low-probability × low-impact edge case the materiality lens instructs to refute even where technically true.

---

## 012-002: No General Schema Field or Lint Check for the ADR↔Companion-Rule-File Relationship

**Verdict: REFUTED**

**Reasoning:** This finding identifies a genuine completeness gap (no `companion_rule_file:`-style frontmatter field, no L-7-equivalent check for the ADR↔rule-file pairing pattern) but it does not bear on any of the three stated purposes — collision-free identity, honest promotion, or adoptable convention. It is a traceability nicety for a narrow, low-occurrence pattern: only a handful of instances exist corpus-wide (`ADR-agent-design-001`↔`agent-development-standards.md`, `ADR-routing-triggers-001`↔`agent-routing-standards.md`, `ADR-EPIC002-001/002`↔`quality-enforcement.md`, and this ADR↔its own rule draft — four cases, per the finding's own evidence at `ADR-PROJ031-004:732-734`). The package's own governing doctrine (`subtraction-pass-notes.md:26`, "subtract, don't compensate") explicitly counsels against adding new schema/lint surface for narrow, low-frequency concerns; the finding's own corrective action offers "or, if declining new schema per the subtraction doctrine, add an explicit disclosed residual" as an equally acceptable closure — i.e., even the finder does not treat new machinery as required. A missing cross-reference field for a rare authoring pattern, recoverable today via the same manual `grep`/cross-link-repair the package already performs for M-2/M-9, is a low-probability × low-impact completeness gap — cosmetic relative to the standard's core purpose, not a blocker to adoption.

---

## 012-003: Grandfather-Baseline Temporal Anchor Creates an Unbounded Post-Ratification Amnesty Window

**Verdict: VERIFIED**

**Reasoning:** This is a genuine, non-redundant enforcement-design flaw that directly touches the "collision-free identity" purpose. Per `ADR-PROJ031-004:688` and `adr-standards-rule-draft.md:183`, the grandfather baseline is captured as "the enumerable set of ADR files that exist **when the lint first ships**" rather than at ratification (2026-07-05). Because M-6 (lint implementation) has no committed date and FM-5 (`ADR-PROJ031-004:496`) independently rates "nothing lands" as the single best-evidenced risk in the whole package, any non-compliant ADR file (e.g., a bare `ADR-NNN` — the exact pattern that produced Jerry's three historical collisions) created during the ratification-to-lint-ship gap and still present on the day the lint's baseline snapshot is taken would be folded into the permanently-exempted baseline, never subsequently flagged by L-1/L-2 even after the lint ships. This is not a re-derivation of the already-disclosed R-1 ("the lint may never be built") — R-1 addresses non-existence of the lint; this finding addresses a distinct temporal-anchoring defect in *how* the baseline is computed *if and when* the lint does ship. It also compounds directly with an already-disclosed, currently-active failure mode: R-A (`subtraction-pass-notes.md:127`) discloses that the ADR-producing agent (`ps-architect.md`) "still hardcodes a non-canonical filename grammar" and emits non-compliant IDs until M-12 lands — meaning the exact class of file this finding worries about is actively being produced today, with no fixed date for either M-6 (lint) or M-12 (producer fix). The corrective action is a one-sentence disclosure or a baseline-anchoring fix (the ratification-date file counts, 16/15/3/18, are already reconciled and available), fully consistent with the package's own subtraction/disclosure doctrine — but the underlying gap is real, plausible (not a negligible-probability edge case), and bears directly on whether the convention's collision-prevention guarantee actually holds once enforcement eventually activates.

---

## Summary

| ID | Severity (per report) | Verdict |
|----|------------------------|---------|
| 012-001 | Critical (RPN 512) | **REFUTED** |
| 012-002 | Critical (RPN 245) | **REFUTED** |
| 012-003 | Critical (RPN 252) | **VERIFIED** |
