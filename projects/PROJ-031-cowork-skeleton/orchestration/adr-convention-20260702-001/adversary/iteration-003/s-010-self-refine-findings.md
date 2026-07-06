# S-010 Self-Refine — Findings Log (Iteration 3)

> **Strategy:** S-010 Self-Refine (Iterative Self-Correction family)
> **Reviewer/Owner:** ps-architect (creator/owner of the reviewed package)
> **Date:** 2026-07-02
> **Iteration:** 3 of the adr-convention tournament
> **Criticality:** C4 (ADR governance convention; AE-002/AE-003 C3 floor, C4 by tier definition)
> **Deliverables under self-review:**
> 1. `projects/PROJ-031-cowork-skeleton/decisions/ADR-PROJ031-004-adr-identifier-convention.md` (687 lines)
> 2. `projects/PROJ-031-cowork-skeleton/design/adr-standards-rule-draft.md` (300 lines)
> **Edit rights:** This role MAY edit BOTH deliverables (sole tournament role with edit rights).

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Header](#header) | Execution metadata |
| [Step 1: Objectivity Assessment](#step-1-objectivity-assessment) | Perspective shift |
| [Step 2: Systematic Self-Critique](#step-2-systematic-self-critique) | Dimension-by-dimension |
| [Findings Table](#findings-table) | All findings, severity-sorted |
| [Finding Details](#finding-details) | Expanded Critical/Major |
| [Edits Applied](#edits-applied) | What was changed in the deliverables |
| [Scoring Impact](#scoring-impact) | Dimension mapping |
| [Decision](#decision) | Ready / revise / escalate |

---

## Header

| Field | Value |
|-------|-------|
| Strategy | S-010 Self-Refine |
| Deliverable | ADR-PROJ031-004 + adr-standards-rule-draft (package) |
| Criticality | C4 |
| Date | 2026-07-02 |
| Reviewer | ps-architect (owner) |
| Iteration | 3 |
| Execution ID | 20260702-i3 |

---

## Step 1: Objectivity Assessment

Objectivity check: **medium attachment** (this is the owner's own package, remediated across two prior iterations; risk of leniency/echo-chamber bias is real). Per the S-010 Conservative Fallback, I choose the higher attachment level and apply the stricter guidance — **aim for 5+ findings, not the 3 minimum** — and I hunt specifically for the categories the invoking task named (internal contradictions, unevidenced claims, steelman-fairness, tier-vocabulary violations in the MEDIUM draft, dangling refs, nav-table compliance, and whether the crux is truly answered). Proceeding with counteraction toward higher finding yield.

---

## Step 2: Systematic Self-Critique

Dimension-by-dimension pass, cross-referenced against the task's named hunt categories. Every factual claim below is grounded in a filesystem/grep probe run during this execution (P-022).

**Completeness (0.20).** The package is thorough: crux answered head-on, all 6 schemes steelmanned, sensitivity analysis present, migration plan + lint spec + promotion paths + status vocab all covered. Gap found: the lint spec's L-1a regex does not exclude all-numeric slugs (SM-101), leaving one corpus file's grammar-status misclassified.

**Internal Consistency (0.20).** Strongest hunt area. Verified:
- **Tier vocabulary (MEDIUM draft):** `grep -E '(MUST|SHALL|REQUIRED|FORBIDDEN|NEVER)'` on the rule draft returns **zero** hits — the MEDIUM draft is clean. PASS. (The ADR itself uses MUST in Constraints/meta-process contexts, which is legitimate for a decision doc, not the MEDIUM rule file.)
- **L-1a vs L-2 contradiction (SM-101, MAJOR):** the L-1a regex `^ADR-[a-z0-9]+...` admits `ADR-150-001` (slug `150`) while L-2 bare-detection `^ADR-\d` rejects it — same file simultaneously "canonical" and "bare"; and the repeated claim that `ADR-150-001` "matches neither grammar" was false. FIXED (leading-letter requirement).
- **DEC-NNN bare-vs-composite:** worktracker SSOT confirms BOTH forms — composite `EPIC-001--DEC-001` (`:65`) at Epic/Feature, bare `DEC-001-cli-hook.md` (`:80`) at Enabler/Story. Both ADR characterizations are individually accurate at different levels; the crux-rebuttal's reliance on the bare form is **verified sound**. Minor: the Relationship table stated only the composite (SM, m3) — reconciled.

**Methodological Rigor (0.20).** Options analysis leads with steelman for all six (H-16). Scores traced to `trade-study.md:228` — **all six weighted totals and ranks verified exact** (A 3.52/4, B 3.58/3, C 3.86/1, D 3.06/5, E 2.10/6, F 3.60/2). Confidence 0.75 sits at (not above) the trade study's declared ceiling (`trade-study.md:341`: headline 0.70, "decline to claim >0.75") — accurately attributed.

**Evidence Quality (0.15).** Load-bearing citations spot-checked and CONFIRMED on disk:
- Stale `ADR-PROJ007-001/002` citations present at `WORKTRACKER.md:106-107`, `ORCHESTRATION.yaml:228,242`, `EN-001.md:48-49,72-73`. ✓
- Dangling `ADR-CI-001` at `.github/workflows/ci.yml:2`; cited project `PROJ-001-plugin-cleanup` is **absent** → citation genuinely dangling. ✓
- Exactly **3** framework ADRs in `docs/design/` (agent-design, output-path-resolution, routing-triggers). ✓
- **15** `ADR-*` files under `projects/*/decisions/` across 5 projects → the "14 project-level ADRs" figure = 14 pre-existing (excludes the in-flight ADR) and excludes entity-embedded STORY015; phrasing clarified (m2).

**Actionability (0.15).** Migration plan M-1..M-14 each owned + gating-flagged; lint spec is implementable. Honest DESIGNED-NOT-BUILT claim-status retained.

**Traceability (0.10).** Every finding tag traces to the glossary (line 46); references table complete; nav tables (both files) verified complete and anchor-correct (H-23/H-24 PASS).

### Nav-table compliance check (H-23/H-24)

- **ADR:** 24 `##` sections ↔ 24 nav rows; every anchor (incl. em-dash cases `#rationale--answering-the-crux-head-on`, `#pre-mortem-and-failure-modes-s-004--s-012`) resolves. PASS.
- **Rule draft:** 14 governed `##` sections ↔ 14 nav rows; anchors resolve. PASS.

### Steelman-fairness check

All six schemes lead with "Strongest case." Winner (B) is separated from its two closest rivals (C at baseline, F fractionally above at baseline) with explicit "what this is NOT" analysis. Rejected A/C kept alive in the Rationale's "honest counter-case" and adverse-regime section. Steelman discipline: PASS.

### Crux answered?

"Is *project* the right scope key?" — answered directly ("No"), with a **promotion-frequency-independent** principle (identifier must be lifecycle-invariant; ADR scope is the one mutable property; encoding it in the immutable ID is the defect), three convergent lines (two of which survive the low-promotion regime), and an explicit statement of the regime in which the decision would be wrong. Verdict: **fully answered** — a genuine strength.

---

## Findings Table

| ID | Finding | Severity | Evidence | Affected Dimension |
|----|---------|----------|----------|--------------------|
| SM-101 | L-1a canonical regex `^ADR-[a-z0-9]+(-[a-z0-9]+)*-\d{3}...` admits all-numeric domain slugs (`ADR-150-001`, slug=`150`), which (a) contradicts L-2 bare-detection `^ADR-\d` (same file both "canonical" and "bare"), and (b) falsifies the repeated claim that `ADR-150-001` "matches neither grammar." | **Major** | Rule draft L-73, L-199, L-211; ADR L-280, L-582. `ADR-150-001` verified on disk at `PROJ-030-bugs/decisions/`. | Internal Consistency |
| SM-102a | Rule-draft onboarding note asserts `decisions/` is "ADR files only" and DEC-Files "live inside their parent entity folder"; contradicted by live `PROJ-002-roadmap-next/decisions/DEC-001-project-creation.md`. | Minor | Rule draft L-272; ADR non-conflation table L-607; disk counterexample verified. | Internal Consistency / Evidence |
| SM-102b | "14 live project-level ADRs ... occupy [decisions/] ... filesystem-verified" undercounts the 15 `ADR-*` files actually in `projects/*/decisions/` by silently excluding the in-flight ADR; inconsistent with the D-4 "15 pre-existing + this = 16" inclusion convention. | Minor | Rule draft L-270; ADR M-14 L-459; `find` returns 15. | Internal Consistency |
| SM-102c | ADR Relationship table characterized DEC identity only as "parent-scoped composite `{ParentId}--DEC-NNN-slug`," omitting the bare `DEC-NNN-slug` Enabler/Story variant the L0/L2 crux-rebuttal depends on. | Minor | ADR L-605 vs worktracker `:80,:88`. | Internal Consistency |
| SM-102d | ADR "regression test asserts all 16 live dialect/canonical files pass" conflates the 16 dialect files with the 3 canonical it also exercises (19 files total). | Minor | ADR L-571; rule draft L-215 (already precise). | Actionability / Clarity |

Considered and **withdrawn** (not findings): (o1) ADR L-492 "MUST NOT be rewritten" for historical records — this is a distinct rule from the amendment-boundary that CC-003's "one register" claim scopes, and is a truth-preservation constraint, not a MEDIUM authoring rule; no contradiction. (o2) pre-flight grep `[a-z0-9-]+` at ADR L-344 is over-inclusive for collision extraction but harmless.

---

## Finding Details

### SM-101 (MAJOR): Numeric-leading slug ambiguity in the L-1a lint

- **Severity:** Major
- **Affected Dimension:** Internal Consistency
- **Evidence:** `ADR-150-001-pre-tool-enforcement-consolidation.md` exists in `projects/PROJ-030-bugs/decisions/`. Under the as-written L-1a `^ADR-[a-z0-9]+(-[a-z0-9]+)*-\d{3}(-[a-z0-9-]+)?\.md$`, the first token `[a-z0-9]+` matches `150`, so the file PASSES L-1a. Under L-2 bare-detection `^ADR-\d`, the digit after `ADR-` makes it FAIL L-2. Two FAIL-class rules therefore return opposite verdicts on the same file. Separately, the rule draft (L-211) and regression-test design (L-215) assert `ADR-150-001` "matches neither canonical nor entity-dialect grammar" — false under the as-written L-1a.
- **Impact:** For a C4 governance ADR whose central enforcement mechanism *is* this lint spec, a self-contradicting FAIL-rule pair is a correctness defect: any future `ADR-{number}-NNN` mint would get contradictory lint verdicts, and the grandfather rationale rests on a false grammar claim.
- **Recommendation / Fix APPLIED:** Tightened the domain-slug first token to require a leading letter: `^ADR-[a-z][a-z0-9]*(-[a-z0-9]+)*-\d{3}...`. Verified safe — all 3 canonical framework ADRs (`agent-design`, `output-path-resolution`, `routing-triggers`) and the canonical self-ID `adr-convention` start with letters and still pass; `ADR-150-001` now correctly fails L-1a (→ grandfather allowlist), removing the L-1a/L-2 contradiction and making the "matches neither grammar" claim true. The RT-003 dialect-look-alike guard is unaffected (`proj031` starts with a letter, still caught by the `^(proj|epic|feat|story)\d+$` guard).

---

## Edits Applied

All edits carry an `SM-101`/`SM-102` iter-3 tag for traceability (glossary line 46: `SM-*` = self-refine).

| # | File | Location | Change |
|---|------|----------|--------|
| E1 | ADR | ID grammar block (`domain-slug`) | Regex `[a-z0-9]+` → `[a-z][a-z0-9]*` + leading-letter rationale note (SM-101) |
| E2 | ADR | L-1a lint table row | Regex tightened + numeric-leading rejection noted (SM-101) |
| E3 | Rule draft | ID Scheme L-1a bullet | Regex tightened + L-1a/L-2 contradiction explained (SM-101) |
| E4 | Rule draft | L5 lint L-1a table row | Regex tightened + numeric-leading note (SM-101) |
| E5 | Rule draft | Grandfather scope note | `ADR-150-001` "matches neither grammar" now *actually* true post-fix (SM-101) |
| E6 | Rule draft | New-Project Onboarding note | "ADR files only" → prefix-based separation + live DEC counterexample (SM-102a) |
| E7 | ADR | Non-conflation table (Location) | DEC "inside parent folder" → "typically" + counterexample (SM-102a) |
| E8 | Rule draft | Onboarding count | "14 live" → "14 pre-existing (15 incl. this ADR)" + derivation (SM-102b) |
| E9 | ADR | M-14 row | Same count clarification + STORY015 derivation (SM-102b) |
| E10 | ADR | Non-conflation table (Identity) | Added bare `DEC-NNN` Enabler/Story variant (SM-102c) |
| E11 | ADR | Two-corrections block | Regression-test file count clarified: 16 dialect + 3 canonical = 19 (SM-102d) |

---

### Post-edit verification (self-refine loop caught a self-inflicted regression)

A second self-review pass over my own edits found that the SM-101 wording (E3/E4) had introduced **two `MUST` tokens into the MEDIUM rule draft** (lines 73, 199) — the exact tier-vocabulary violation this pass was tasked to hunt. Re-verified `grep -E '(MUST|SHALL|REQUIRED|FORBIDDEN|NEVER)'` on the rule draft, caught the 2 hits, and reworded to descriptive phrasing ("the regex constrains ... to begin with a letter"). Final grep on the rule draft: **zero** HARD-tier tokens. The ADR retains one `MUST` in the same grammar note, which is acceptable — the ADR is a decision document that uses `MUST` throughout its Constraints (c-001..c-007); the "no MUST/SHALL" rule applies only to the MEDIUM rule draft. Regex behavior re-checked by bash: 3 canonical + self-ID PASS L-1a; `ADR-150-001` correctly REJECTED.

---

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Neutral→Positive | Lint spec now covers the numeric-slug edge (SM-101) |
| Internal Consistency | 0.20 | Negative→Positive | L-1a/L-2 contradiction removed; DEC + count claims reconciled with disk truth |
| Methodological Rigor | 0.20 | Positive | Steelman intact; scores/confidence verified against source |
| Evidence Quality | 0.15 | Positive | All load-bearing citations confirmed on disk this pass |
| Actionability | 0.15 | Positive | Regression-test scope made precise (SM-102d) |
| Traceability | 0.10 | Positive | Nav tables verified; every edit tagged |

---

## Decision

**Outcome:** Revisions applied; package materially improved and ready for the remaining tournament strategies.

**Rationale:** One Major (SM-101, a genuine lint-spec internal contradiction) and four Minor precision defects were found and fixed in-place. No Critical findings. The core decision (subject-encoded ADR identity) is sound and the crux is fully answered; the fixes tighten enforcement precision and reconcile descriptive claims with the verified corpus. All fixes were checked against the live corpus so none breaks the grandfather regression set.

**Next Action:** Proceed to the remaining Group-A/downstream strategies (steelman, challenge, verify, decompose, score). SM-101's regex change SHOULD be re-checked by the chain-of-verification / FMEA strategies against the 19-file regression corpus.
