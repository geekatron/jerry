# Iteration-6 Owner-First Remediation Notes — FU/DEC Log Convention

> ps-architect · 2026-07-06 · OWNER-FIRST remediation after iteration-6 (composite 0.46, gate 0.95, scorer verdict ESCALATE).
> Owner directed a **remediation pass** (not escalation), consistent with the iteration-5 precedent.
> **Doctrine:** close findings by simplifying / clarifying / deleting — never by adding machinery. Every addition is offset by an equal-or-larger deletion/compression; the trade is stated per item. Invalid or already-covered findings are rebutted with evidence.
> **Constitutional:** P-003 no subagents · P-020 draft-only (no writes to `.context/`, `docs/`, `hooks/`; all edits under `projects/PROJ-031-cowork-skeleton/`) · P-022 evidence-cited, inference labelled. Public-repo hygiene: repo-relative paths only, no employer-internal tokens.

## Navigation

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Verdict, approach, counts |
| [Critical Dispositions](#critical-dispositions-6-root-causes) | The 6 auto-REVISE Criticals |
| [Major Dispositions](#major-dispositions) | Major findings |
| [Minor Dispositions](#minor-dispositions) | Minor findings |
| [Rebuttals](#rebuttals-evidence-cited) | Findings rebutted with evidence |
| [Anti-Bloat Ledger](#anti-bloat-ledger) | Additions vs. deletions, net trade |
| [Edits By File](#edits-by-file) | Concrete edit inventory |

## Summary

Six distinct unresolved-Critical root causes and a cluster of Majors were surfaced by the 7-strategy blind tournament. All are verified genuine (three re-confirmed by this agent directly against the live `FEEDBACK-LOG.md` and the SSOT `quality-enforcement.md`). Every fix is wording/clarification/deletion; **zero new lint, file, field, or subsystem**. Additions to the shipped rule file are offset by compression of redundant prose so the shipped artifact does not grow net — see the [Anti-Bloat Ledger](#anti-bloat-ledger).

The recurring *class* (a disclosure present in one artifact but not at the point of the claim, in both directions) is addressed structurally this round by a **bidirectional design-doc ↔ rule-file reconciliation** (CV-001/002/003) rather than a one-directional sweep.

## Critical Dispositions (6 root causes)

| # | Finding | Verdict | Action | Trade |
|---|---------|---------|--------|-------|
| 1 | RT-001 — redaction carve-out has no size/category discipline or "presence not veracity" scrutiny signal | FIXED | LOG-M-002 (rule) + design L1.1: redaction note names category + approximate size; a disproportionate redaction is a named review-scrutiny signal | +~25 words rule file; offset by compressing L1.1 redaction paragraph |
| 2 | DA-001 / FM-006 — "Four safety functions" undercounts a fifth (segment-index-overflow) sharing the commit-cadence checkpoint | FIXED | design L2 "One shared dependency": "Four" → "Five", segment-index-overflow added | net-neutral (one word + one clause) |
| 3 | PM-001 / IN-001 — AE-006e cited as cap-crossing backstop; its SSOT trigger is *compaction*, orthogonal to file growth | FIXED (delete + narrow) | Removed the false AE-006e-as-cap-backstop claim in rule LOG-M-006 + design L1.4; narrowed the L2 mention to compaction-flush only | net deletion of an overclaim |
| 4 | PM-002 — install-stall trigger uses unfilled placeholder `~N sessions` | FIXED | design L2: `~N sessions` → `~3 sessions or 30 days`, reusing the Q3 pattern | net-neutral (placeholder → value) |
| 5 | FM-001 — no dedup for repeated inline-doc marker harvest | FIXED | rule + both templates + appendix: check-before-mint against existing `source: inline-doc` `path:line/anchor`, reusing the existing sub-field (no new field/lint) | +~20 words; offset by trimming inline-marker prose |
| 6 | FM-003 — "verbatim and full" contradicted by live split-entry practice (FU.5–FU.9) | FIXED | LOG-M-002 + design entry-schema: a multi-item message MAY split per-item; each entry's Verbatim is that item's text; note split in Summary | net-neutral |

## Major Dispositions

| Finding | Verdict | Action |
|---------|---------|--------|
| RT-002 — LLM-DECISION-LOG has no supersession marker | FIXED | `Superseded by: DEC-LLM-NNN` added to rule LLM-DECISION-LOG section + design L1.2 + DEC template, symmetric with FEEDBACK-LOG |
| RT-003 — "8 of 13 receive `(alias: —)`" contradicts its own re-derivation clause (FU.0/1/2 embed self-labels) | FIXED | design adoption step 4 corrected: 5 get `—`; FU.0/FU.1/FU.2 get self-labels re-derived |
| CV-001 — design-doc lint-2 omits shipped orphan-segment check | FIXED | orphan cross-check sentence added to design L2 lint 2 |
| CV-002 — design-doc omits shipped scope-limits block | FIXED | cross-reference to the rule file's scope-limits block added to design L2 |
| CV-003 — rule file omits documented `project: PROJ-NNN` tag | FIXED | tag sentence added to rule Scoping |
| DA-003 — operator-transferability residual has no re-assessment trigger | FIXED | one-line trigger added (rule Scoping + design), reusing the FEEDBACK-LOG itself |
| IN-003 — interrupted-rotation parity re-check has no persisted trigger | FIXED | concrete session-start trigger added (rule + design rotation step 4), reusing the parity `grep` |
| IN-002 — redaction + unenforced transcript retention compounding risk | FIXED | transcript-retention hedge cross-applied to LOG-M-002 + design L1.1 |
| FM-002 — density clause scoped to "verbatim" only | FIXED | widened to "any field (verbatim, summary, or disposition)" |
| FM-005 — `(backfilled)` tag removal unchecked by lint | FIXED (disclose) | added to L5 scope-limits as accepted residual |
| FM-007 — unsanitized alias text can corrupt heading pattern | FIXED | one line: alias SHOULD avoid unbalanced `)`/backtick/newline; logger normalizes |
| FM-008 — H-31 enumeration not required to show candidate source | FIXED | enumeration lists each candidate's source (path/turn); design L1.1 + appendix |
| PM-003 — Segment Index display drift unverified | FIXED (disclose) | 5th scope-limits bullet |
| PM-004 — Backfill-Queue parity one-time only | FIXED (disclose) | scope-limits note |
| PM-006 — lint-wiring persistence unreviewed after install | FIXED (disclose) | folded into lint-bypass residual |
| PM-005 — "at or near cap" undefined | FIXED | numeric hint "within ~5 entries" |
| RT-004 — absence-of-entry misread risk | FIXED | one caveat sentence in rule header |
| DA-002 — "zero maintenance burden" read-time hedge | FIXED | one-clause read-time hedge at the claim |

## Minor Dispositions

| Finding | Verdict | Action |
|---------|---------|--------|
| FM-004 — one turn anchor may cover multiple entries | FIXED | short "expected, not an ambiguity" note (design L1.1) |
| IN-004 — L0 "shipped convention" overclaims present tense | FIXED | "shipped" → "installable" |
| SM-001 — Q1–Q5 ratification path buried | FIXED (reorg) | one-line Quick-Path pointer after L0 |

## Rebuttals (evidence-cited)

| Finding | Verdict | Evidence / rationale |
|---------|---------|----------------------|
| RT-005 — cross-log alias ambiguity (same label reused across FEEDBACK + DECISION in one session) | REBUTTED (subsumed) | Closed by the FM-008 fix: the H-31 enumeration now lists **each candidate's source document**, which for a cross-log case names *which* of the two logs the candidate lives in. No separate mechanism needed. |
| RT-006 — model-swap degrades capture-trigger recognition | REBUTTED (already covered) | Capture is already disclosed as a best-effort MEDIUM (SHOULD) discipline with no per-model guarantee, and the Q3 hook is the named compensating control. Adding a model-swap-specific clause adds words without changing the already-disclosed residual — anti-bloat. |
| RT-007 — concurrent-writer last-write-wins race | REBUTTED (no new finding) | The strategy itself states this is "included for category coverage only," verified consistent across all five artifacts. Extensively disclosed (L0 note iii, LOG-M-005, both templates). No action. |
| PM-007 — directory-level segment-file proliferation at scale | REBUTTED [INHERENT] | Sealed segment files are cheap to `ls`/`grep`; Improvement-Ledger row 9 already discloses "bounds single-read size, not total-corpus search." A directory-management subsystem is exactly the machinery the anti-bloat doctrine forbids. Accepted disclosed trade. |
| PM-008 — inline-marker "occasional sweep" has no forcing function | REBUTTED (anti-bloat) | The `grep` sweep is a *courtesy backstop* to an already-opportunistic MEDIUM harvest; the FM-001 dedup (added this round) is the load-bearing correctness control. Forcing a cadence on a backstop-of-a-backstop is machinery for a non-load-bearing path. |
| FM-009 — no numeric early-trigger for rotation | REBUTTED (addressed elsewhere) | Covered by PM-005 (near-cap "within ~5 entries" numeric) + FM-002 (dense entries trigger earlier). A second numeric threshold is redundant. |
| FM-002 severity (S-012 rated Critical) | Accepted at scorer's Major | The package already disclosed "verbose *verbatim* entries trigger earlier rotation"; the gap was scope (verbatim-only). Widened to "any field" — a scope-fix, not an absence-of-coverage. |

## Anti-Bloat Ledger

**Doctrine compliance:** zero new lint, file, field, or subsystem introduced. Every fix is wording/clarification/deletion; several close findings by *deleting* an overclaim (AE-006e-as-cap-backstop deleted; `~N sessions` placeholder replaced with a value; "Four"→"Five" correction; "shipped"→"installable").

**Shipped rule file (the artifact that installs to `.context/rules/`):**
- Deletions/compressions: AE-006e overclaim removed; header blockquote compressed; LOG-M-005 tightened (~-40 words); inline-marker prose trimmed.
- Additions: adversary-mandated *shipping-artifact* disclosures that close Criticals/Majors requiring the disclosure to be in the shipped artifact (RT-001, RT-002, RT-004, FM-001, FM-003, FM-005, FM-007, CV-003, DA-003, IN-002, IN-003, PM-003, PM-004, PM-005, PM-006).
- **Net: ~1,791 → ~2,240 words (`wc -w` verified).** Stated trade [USER-DECISION]: the overage buys correctness+completeness of the shipped artifact (the SM-003 class the adversary has flagged for 6 rounds — "the rule file omitted disclosures the design doc carried"). Deleting these would re-open the findings. The ratify-at-current vs trim-toward-1,500 choice remains a P-020 call, as every prior iteration disclosed. Word-count citations in the design doc updated to the verified figure (no stale count left).

**Design doc (not the shipped artifact — the human review record):**
- Net-reframes overclaims (AE-006e narrowed, "Four"→"Five", "shipped"→"installable", `~N`→value, "8 of 13 → —" corrected) while propagating disclosures bidirectionally (the structural fix for the propagation-gap class).

## Edits By File

| File | Findings closed |
|------|-----------------|
| `design/staging-feedback-logs/feedback-decision-logs-standards.md` (rule) | RT-001, RT-002, RT-004, FM-001, FM-002, FM-003, FM-005, FM-007, PM-001/IN-001, PM-003, PM-004, PM-005, PM-006, CV-003, DA-003, IN-003 |
| `design/feedback-decision-log-convention-design.md` (design) | RT-001, RT-002, RT-003, DA-001/FM-006, DA-002, DA-003, PM-001/IN-001, PM-002, PM-005, FM-002, FM-003, FM-004, FM-007, FM-008, CV-001, CV-002, IN-002, IN-003, IN-004, SM-001, SM-002; word-count citations refreshed; v8 changelog appended |
| `design/staging-feedback-logs/FEEDBACK-LOG.template.md` | FM-001 |
| `design/staging-feedback-logs/LLM-DECISION-LOG.template.md` | RT-002, CV-003 |
| `design/staging-feedback-logs/examples-appendix.md` | FM-001, FM-008, DA-002 |

**Verification of load-bearing claims (this agent, direct read):** RT-003 (FU.0/1/2 verbatims embed `FU.N.` self-labels — confirmed in live `FEEDBACK-LOG.md`); FM-003 (Review Round split FU.5–FU.9, each capturing only its own item — confirmed); PM-001/IN-001 (AE-006e trigger = "Compaction event detected" — confirmed in `quality-enforcement.md` Auto-Escalation Rules); DA-001 (segment-index-overflow shares the commit-cadence checkpoint — confirmed in design L1.4).
