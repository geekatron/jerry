# Steelman Report: ADR Identifier, Location, and Promotion Convention

## Document Sections

| Section | Purpose |
|---------|---------|
| [Steelman Context](#steelman-context) | Deliverable identification and scope |
| [Summary](#summary) | Assessment, improvement count, recommendation |
| [Blind-Protocol Note](#blind-protocol-note) | What was and was not read |
| [Steelman Reconstruction](#steelman-reconstruction) | Strongest-form restatement + annotated excerpts |
| [Best Case Scenario](#best-case-scenario) | Conditions under which the convention is strongest |
| [Improvement Findings Table](#improvement-findings-table) | SM-NNN findings, severity, dimension |
| [Improvement Details](#improvement-details) | Full before/after for each finding |
| [Explicitly Excluded (Already-Disclosed Residuals)](#explicitly-excluded-already-disclosed-residuals) | What I deliberately did NOT re-report |
| [Scoring Impact](#scoring-impact) | Effect on the 6 quality dimensions |
| [Step 6 Sign-Off](#step-6-sign-off) | H-15 self-review and readiness for downstream critique |

---

## Steelman Context

- **Deliverable 1:** `projects/PROJ-031-cowork-skeleton/decisions/ADR-PROJ031-004-adr-identifier-convention.md` (v1.11, ~797 lines)
- **Deliverable 2:** `projects/PROJ-031-cowork-skeleton/design/adr-standards-rule-draft.md` (v1.11, ~253 lines)
- **Deliverable Type:** ADR + companion MEDIUM-tier rule draft (framework governance convention)
- **Criticality Level:** C4
- **Strategy:** S-003 (Steelman Technique) — iteration 10 of a 10-round tournament
- **SSOT Reference:** `.context/rules/quality-enforcement.md`
- **Steelman By:** adv-executor (Strategy Executor agent) | **Date:** 2026-07-06 | **Original Author:** ps-architect (creator/owner)
- **Execution ID:** `iter010-20260706`

---

## Summary

**Steelman Assessment:** This is an exceptionally mature, self-critical C4 governance ADR — 11 changelog versions across 9 prior adversarial rounds, an explicit residual register (R-1…R-17), and a disciplined subtraction doctrine (delete the exposing claim rather than add compensating machinery). The core decision (subject-encoded ADR identity, origin in frontmatter, promotion as a pure file move) is sound, well-evidenced, and honestly hedged. At this maturity, the highest-value Steelman contribution is no longer substantive gap-filling — nearly every substantive gap already has a named residual (R-1…R-17) and an owner — it is **strengthening the deliverable's actual adoptability**, since "adoptable MEDIUM-tier convention" is one of the three purposes this review is scoped against.

**Improvement Count:** 0 Critical, 1 Major, 1 Minor.

**Original Strength:** Very high. Both files pass H-15/H-16 discipline visibly (self-refine changelog rows, steelman-before-critique tag glossary, VERIFIED-CRITICALS panel discipline in v1.11). No fundamental flaw in the decision itself was found.

**Recommendation:** Incorporate the 2 improvements below (both are cheap, presentation-only, add zero new machinery, and are consistent with the subtraction doctrine already governing this package) before M-2 executes. The package is otherwise ready to proceed directly to downstream critique strategies without requiring author revision first.

---

## Blind-Protocol Note

Per the invoking task's BLIND PROTOCOL, I did not read anything under `adversary/iteration-009/` or `adversary/iteration-010/` except this output file. I did read (as authorized, since both are part of the package's own disposition record): the full ADR (`ADR-PROJ031-004-adr-identifier-convention.md`, all ~797 lines), the full companion rule draft (`adr-standards-rule-draft.md`, all 253 lines), and `orchestration/adr-convention-20260702-001/subtraction-pass-notes.md` (all 239 lines, covering the disposition of every iteration-5 through iteration-9 Critical, R-1…R-17). I loaded the S-003 template's Identity and Execution Protocol sections (`.context/templates/adversarial/s-003-steelman.md`) per lazy-loading discipline.

---

## Steelman Reconstruction

> Per CR-002 (S-003's legitimate output adaptation), this section is the actionable recommendation — presented as (a) a strongest-form distillation of the existing argument (verifying it is already close to its ceiling), and (b) two concrete, annotated excerpts showing exactly where the two SM-NNN improvements insert.

### (a) Strongest-form restatement (verification, not a rewrite)

The core argument, at its strongest and most compact: *An identifier should be invariant across an artifact's lifecycle. Jerry's scope-prefixed ontology (PROJ/EPIC/FEAT/STORY, and the parent-scoped `DEC-NNN`) is correct for those entities precisely because their governing scope never changes — encoding a permanent property into a permanent identifier is free and correct. The ADR is the one Jerry artifact explicitly built to migrate scope (project → framework), so it is the one artifact for which the ontology's usual rule is a category error: encoding the artifact's one **mutable** property (current scope) into its one property that must **never** change (its identifier). Two things about a well-scoped ADR are genuinely immutable — its origin (birth project) and its subject (what it decided) — and only subject is also the axis every future reader queries by. Subject therefore wins the identifier; origin is preserved in frontmatter (satisfying provenance, P-004) without being load-bearing for identity; and promotion — the framework's own accrual thesis in action — becomes a `git mv`, not a rename. This is not asserted as a proof (subject-relabeling in hindsight is a real, disclosed edge case, DA-008) — only as materially more stable than scope, which is demonstrably true because scope changes by design on every promotion.* (`ADR-PROJ031-004-adr-identifier-convention.md:258`, `:73-78`.)

This restatement matches the original's own [Rationale](projects/PROJ-031-cowork-skeleton/decisions/ADR-PROJ031-004-adr-identifier-convention.md#rationale--answering-the-crux-head-on) essentially verbatim in substance — confirming the argument is already at, or very near, its strongest form. I found no missing evidence, no unsupported claim, and no logical gap in the core decision (D-1 through D-5) that Step 3 (Reconstruct the Argument) would need to fill. The two findings below are the only strengthening opportunities identified; both are about the **delivery form** of the guidance, not its substance.

### (b) Annotated excerpt 1 — where [SM-001] applies

**Original** (`projects/PROJ-031-cowork-skeleton/design/adr-standards-rule-draft.md:1-3`):
```
# DRAFT — Proposed `.context/rules/adr-standards.md`

> **REVIEW DRAFT of a ratified convention.** Proposed content of `.context/rules/adr-standards.md`,
> companion to `ADR-PROJ031-004` (canonical `ADR-adr-convention-001`). ... On the M-2 move this
> content — minus this wrapper — becomes `.context/rules/adr-standards.md` and auto-loads via the
> `.claude/rules -> ../.context/rules` directory symlink. ...
```

**Strengthened [SM-001]:**
```
# DRAFT — Proposed `.context/rules/adr-standards.md`

> **REVIEW DRAFT of a ratified convention.** ... On the M-2 move this content — minus this wrapper
> AND minus every inline tournament-provenance annotation (patterns like `(RT-002-iter8)`,
> `(iter-6)`, `(FM-003-iter8)`, `(DA-002-i9)`) — becomes `.context/rules/adr-standards.md` and
> auto-loads via the `.claude/rules -> ../.context/rules` directory symlink. Tournament provenance
> for each clause is retained permanently in this draft file and in
> `subtraction-pass-notes.md`, not inline in the shipped rule.
```

### (c) Annotated excerpt 2 — where [SM-002] applies

**Original** (`projects/PROJ-031-cowork-skeleton/design/adr-standards-rule-draft.md:42-46`, MEDIUM Standards table opening):
```
## MEDIUM Standards

| ID | Standard |
|----|----------|
| **ADR-M-001** | New ADRs SHOULD use **subject-encoded identity** `ADR-{domain-slug}-NNN`,
  `{domain-slug}` naming the subject in kebab-case, `NNN` a 3-digit per-slug sequence, never
  reused. Origin is a birth fact, not an identity. The frontmatter `id:` value **SHOULD exactly
  equal this filename-derived identity string** (RT-002-iter8); no lint in the 5-rule core checks
  the two agree or that `id:` is corpus-unique — a disclosed residual (**R-15** in the parent ADR's
  Risks register). |
```

**Strengthened [SM-002]** (a preceding TL;DR box; the table row itself is unchanged, since editing the row would re-litigate already-dispositioned content):
```
## Quick Reference (read this first)

New ADR? → `ADR-{domain-slug}-NNN-{title-slug}.md` (e.g. `ADR-plugin-distribution-001-foo.md`).
Purely local, will never promote? → `ADR-{PROJ|EPIC|FEAT|STORY}NNN-NNN` is permitted (SOFT `MAY`).
Never use bare `ADR-NNN`. Origin goes in frontmatter, never the filename. Everything below is the
full normative detail and its provenance; this box is the 30-second version.

## MEDIUM Standards
...
```

---

## Best Case Scenario

Per Step 4: this convention is strongest under exactly the conditions the ADR itself already names — (1) framework-mandate projects continue producing promoted ADRs at a rate materially above the tactical ≈0% baseline (`ADR-PROJ031-004-adr-identifier-convention.md:292`); (2) domain-slug collisions stay rare relative to the taxonomy's size, so the lint's `sort | uniq -d` remains a sufficient backstop; (3) the two remaining execution items this Steelman pass identifies (M-2's tag-stripping, and a quick-reference entry point) land before or during M-2, so the auto-loaded `.context/rules/adr-standards.md` is consumable by an author who has never seen the tournament history. Confidence in the reconstruction: **HIGH** — the two findings below are additive-clarity items, not challenges to the decision's substance, and both are already consistent with the subtraction doctrine the package has applied for 5 consecutive passes (delete/clarify, do not add machinery).

---

## Improvement Findings Table

| SM-ID | Package-style ID | Description | Severity | Dimension |
|-------|-------------------|-------------|----------|-----------|
| SM-001-iter010-20260706 | 003-001 | Rule-draft's inline tournament-provenance tags (`RT-002-iter8`, `FM-003-iter8`, etc.) have no glossary in the rule-draft itself (unlike the ADR, which has one at line 65), and Migration Plan step M-2 does not specify whether they are stripped before the file becomes the auto-loaded `.context/rules/adr-standards.md` | Major | Actionability |
| SM-002-iter010-20260706 | 003-002 | No "quick reference" / TL;DR exists for a first-time author; the MEDIUM Standards table (the primary actionable content) embeds tournament caveats inside normative sentences, reducing scanability relative to every other file in `.context/rules/` | Minor | Actionability |

---

## Improvement Details

### SM-001-iter010-20260706 (Major) — Rule-draft ships with unexplained tournament tags; M-2 doesn't say to strip them

**Affected Dimension:** Actionability (secondary: Completeness — the Migration Plan action item is under-specified for what should be a simple, checkable close-condition).

**Original Content:**
- Rule-draft wrapper (`adr-standards-rule-draft.md:1-3`): "On the M-2 move this content — minus this wrapper — becomes `.context/rules/adr-standards.md`..." — only the review-draft banner is named for removal.
- Migration Plan row M-2 (`ADR-PROJ031-004-adr-identifier-convention.md:535`): "Author `.context/rules/adr-standards.md` from Deliverable 2 (this ADR's companion draft). **Cross-link repair (DA-002):** ..." — the row specifies link repair in detail but says nothing about the ~15+ inline tags scattered through the draft's normative prose (e.g. `adr-standards-rule-draft.md:46,66,175,179,183,206` carry parenthetical tags like `RT-002-iter8`, `DA-002`, `IN-001-iter8`, `FM-002-iter8`, `012-003-iter9`).
- The ADR itself *does* carry an explicit glossary for these tags — "Reading note — prior-review tag glossary (SM-001)" at `ADR-PROJ031-004-adr-identifier-convention.md:65-67` — but this glossary lives only in the ADR, a file the rule-draft does not carry forward and will not exist alongside the shipped rule once it lives at `.context/rules/adr-standards.md` (which is loaded standalone by agents/authors, per CLAUDE.md's Navigation table).

**Strengthened Content:** See annotated excerpt (b) above — M-2's row and the wrapper note should explicitly name tag-stripping (or relocation to a footnote/appendix) as part of the M-2 close-condition, mirroring the atomicity discipline the ADR already applies to the M-2/M-9 reciprocal link repair (`ADR-PROJ031-004-adr-identifier-convention.md:544`, "M-9 cannot be marked closed until M-2's reciprocal edit is verified present in the same PR diff").

**Rationale:** The task framing for this review explicitly names "adoptable MEDIUM-tier convention" as one of three purposes the standard must serve. A rule file that ships to every future ADR author with unexplained strings like `(RT-002-iter8)`, `(FM-003-iter8)`, `(012-003-iter9)` embedded inside its normative sentences is measurably harder to adopt than the framework's own established norm: I directly observed, from the full text of `.context/rules/quality-enforcement.md` and `.context/rules/agent-development-standards.md` provided in this session's project context, that neither file carries any inline adversarial-review finding-ID annotation inside its normative prose — both confine review/version history to a trailing Changelog table. Shipping `adr-standards.md` with tournament jargon inline would be a stylistic regression relative to every sibling rule file, and — because the tags are meaningless without the ADR's own glossary, which does not travel with the rule file — a genuinely confusing reading experience for the target audience (authors deciding how to name a new ADR), not merely an aesthetic quibble. This is **not** an already-disclosed residual: the subtraction-pass-notes.md Residuals table (R-A, R-B, R-C) and the ADR's own R-1…R-17 register do not mention this gap; it concerns the **shipped rule file's** form, which none of the prior 9 iterations' Criticals addressed (they are, by their own IDs, about the ADR/rule-draft's content, not about M-2's execution completeness).

**Best Case Conditions:** Fully closed by adding one clause to M-2 (e.g., "and strip/relocate inline tournament-provenance tags to a footnote") — zero new machinery, consistent with the subtraction doctrine already governing 5 consecutive remediation passes.

---

### SM-002-iter010-20260706 (Minor) — No quick-reference entry point for a first-time reader

**Affected Dimension:** Actionability (secondary: Completeness).

**Original Content:** The rule-draft's first actionable content is the "MEDIUM Standards" table at `adr-standards-rule-draft.md:42-59` — 13 rows, several of which embed a parenthetical review-tag citation and a residual-register cross-reference inside the normative sentence itself (e.g. ADR-M-001 at line 46 embeds `(RT-002-iter8)` and `a disclosed residual (**R-15**...)` inside the single sentence stating the core rule).

**Strengthened Content:** See annotated excerpt (c) above — a 4-line "Quick Reference" box before the MEDIUM Standards table, giving the actionable rule with zero caveats, positions the detailed table as the reference tier rather than the entry point.

**Rationale:** This is genuinely Minor (not Major) because the MEDIUM Standards table already IS a reasonably compact, scannable list relative to the rest of the package (13 rows vs. ~800 combined lines elsewhere), and every other rule file in `.context/rules/` uses an analogous "index table first" pattern (e.g., quality-enforcement.md's HARD Rule Index) without a separate TL;DR layer — so this is a polish opportunity, not a deviation from established framework convention. I did not find this in the Residuals or Risk register.

**Best Case Conditions:** A 4-line addition; no other changes required.

---

## Explicitly Excluded (Already-Disclosed Residuals)

Per the invoking task's instruction that "already-disclosed residuals are NOT findings," I deliberately did **not** re-report the following, all of which I verified are already named with an owner and detection signal in `subtraction-pass-notes.md` and/or the ADR's own Risks register (R-1…R-17): the lint being designed-not-built (R-1/R-5); slug-uniqueness as discipline-not-guarantee (Negative-1); taxonomy synonymy drift (R-3); dialect abuse (R-4); cross-branch same-slug race (R-6); slug reuse for an unrelated subject (R-7); YAML/blockquote frontmatter drift (R-8); case-fold look-alikes (R-9); out-of-scan location classes (R-10); L-7's 3-of-6 relationship-field asymmetry (R-11); solo-maintainer self-approvable override (R-12); L-3's title-slug-tail extraction false-negative (R-13); frozen-dir new-file collision (R-14); frontmatter `id:` never deduplicated (R-15); L-7's zero real YAML targets in the live PROJ031 chain (R-16); cross-branch concurrent-supersession race (R-17); the citation-staleness residual for full-path/GitHub-Issue citations (R-B); in-place amendment mutation (R-C); the producer-agent non-compliance until M-12 lands (R-A); and the plugin/downstream "no trace of this convention until M-2+build" caveat (012-001, already folded into the Enforcement Scope section). None of these needed re-verification for me to conclude they are already honestly disclosed with an owner; I spot-checked several (R-15, R-A, R-B, R-9) directly against the cited line numbers and confirmed the disclosure text is present as claimed.

---

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Neutral | The decision's substantive content is already complete; the 2 findings are about delivery form (M-2 execution + a missing entry point), not missing analysis |
| Internal Consistency | 0.20 | Neutral | No inconsistency found between the ADR and rule-draft on any point checked |
| Methodological Rigor | 0.20 | Neutral | Charitable interpretation applied throughout; the package's own subtraction discipline is itself methodologically rigorous and was preserved, not weakened, by these findings |
| Evidence Quality | 0.15 | Neutral | No claim found lacking evidence; both findings are about presentation, not evidentiary support |
| Actionability | 0.15 | Positive | SM-001 closes a genuine gap in M-2's action-item completeness (what "minus this wrapper" covers); SM-002 gives first-time authors a lower-friction entry point |
| Traceability | 0.10 | Neutral | Both findings preserve, and in SM-001's case strengthen, the existing traceability model (tags retained in the draft/notes file, just not inline in the shipped rule) |

---

## Step 6 Sign-Off

H-15 self-review applied: both findings cite exact file+line evidence (`adr-standards-rule-draft.md:1-3,42-46`; `ADR-PROJ031-004-adr-identifier-convention.md:65-67,535,544`); severity classifications match the template's Step 5 definitions (Major = "would score notably lower without it," not "transforms the deliverable"); no Critical is claimed, so the VERIFIED-CRITICALS 3-lens refutation panel has nothing to adjudicate from this strategy's output. The reconstruction confirms the original is close to its strongest form (mostly Minor/Major polish, not structural rework) — ready to proceed directly to downstream critique strategies (S-002/S-004/S-001/S-014) per H-16 without requiring author revision first, though incorporating SM-001 before M-2 executes is recommended.

---

*No subagents spawned (P-003). No files edited outside this output (P-020). All findings cite file+line; the "strongest-form restatement" and "best case conditions" framings are this reviewer's characterization, not a verified external fact, and are labeled as such (P-022).*
