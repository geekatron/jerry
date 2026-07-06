# Iteration-4 Remediation Notes — FU-Log / DEC-LLM Convention Package

> **Agent:** ps-architect (convergent, opus) · **Mode:** OWNER-FIRST remediation after iteration-4 (S-014 composite 0.53, gate 0.95).
> **Doctrine:** ANTI-BLOAT — close findings by simplifying / clarifying / deleting, never by adding machinery. Any addition must be offset by a larger deletion; the trade is stated per item.
> **Constitutional:** P-003 no subagents. P-020 draft-only — all edits under `projects/PROJ-031-cowork-skeleton/`; no framework path touched. P-022 — evidence cited, inference labelled.
> **Public-repo hygiene:** repo-relative paths and placeholders only.

## Navigation

| Section | Purpose |
|---------|---------|
| [Strategy](#strategy) | Root-cause read and remediation philosophy |
| [Critical Dispositions](#critical-dispositions) | The 4 auto-REVISE Criticals + disclosed-residual |
| [Major Dispositions](#major-dispositions) | Fix / rebut per Major finding |
| [Rebuttals (evidence)](#rebuttals-evidence) | Findings declined with proof |
| [Additions/Deletions Ledger](#additionsdeletions-ledger) | Anti-bloat trade accounting |

## Strategy

The scorer's own root-cause read (iteration-4 s-014, line 215) is decisive: the composite is declining **not** because prior fixes regressed (self-refine + CoVe confirm zero regression) but because **each round adds hedges that create new attack surface**, and because **claims outrun the minimal mechanism**. The scorer's leniency check confirms "minimal by design, honestly disclosed" is *not* penalized; only "claims outrunning the mechanism" is.

Therefore the highest-value anti-bloat move is **subtraction**: where a claim outruns the mechanism, **delete or soften the claim to match the mechanism** rather than bolt on another hedge. This fixes findings, reduces surface, and honours the doctrine simultaneously. This pass nets toward deletion.

## Critical Dispositions

| ID | Strategy | Root cause | Action | Anti-bloat trade |
|----|----------|------------|--------|-------------------|
| FM-001 | S-012 | Single-line `FU:`/`DEC:` marker cannot carry the "verbatim and full" text LOG-M-002 requires | **FIX (clarify)** — "verbatim and full" is channel-relative: capture the operator's complete text *as given in that channel*; the inline marker is a single-line annotation by design; substantive/multi-paragraph feedback belongs in chat | +~2 clauses, offset by RT-006 deletion |
| SM-001 / IN-002 | S-003 + S-013 | Rule-file header omits the "AND committed" durability qualifier the design doc carries | **FIX** — add "and committed" + one-clause exposure to rule-file header; compress the redundant MEDIUM/auto-close clause to offset | net ~0 |
| IN-001 | S-013 | Null-alternative note claims both weaknesses "addressed" when one is gated-future, one mere disclosure | **FIX (rewrite)** — distinguish "planned-but-gated" (rediscoverability) from "disclosed-not-mechanically-fixed" (durability); delete "addressed" | net ~0 (rewrite) |
| DA-001 | S-002 | "generalizes cleanly to any other single operator" — unhedged, unvalidated universal claim | **FIX (delete)** — remove the unsupported clause entirely; the sentence's load-bearing point (team = out-of-scope) stands without it | net deletion |
| RT-005 | S-001 | Silent non-capture has no detector | **FIX (elevate visibility)** — already disclosed (L0 note (i)); add a compact Q5 PROPOSED-DEFAULT so the residual gets the same per-item P-020 visibility as Q1–Q4 | +1 table row + 1 L0 clause, offset by DA-001 + RT-006 deletions |

## Major Dispositions

| ID | Strategy | Action | Note / trade |
|----|----------|--------|--------------|
| RT-001 | S-001 | **FIX (word)** | "operational" → "procedural" (2 sites) |
| RT-006 | S-001 | **FIX (delete)** | Delete the hook-note "Vocabulary note" self-exemption blockquote; lowercase the code-contract imperatives so no HARD-tier signal is emitted. Net deletion. |
| DA-003 | S-002 | **FIX (word)** | "bounded" → "rate-bounded (not size-bounded)" |
| PM-001 | S-004 | **FIX (word)** | "is the remedy" → "is the intended remedy (Q3, designed, not yet shipped)" |
| RT-002 | S-001 | **FIX (word)** | Flip backfill flag default-on: `(backfilled)` unconditional, drop only once a reference is named |
| CC-001 / SM-002 | S-007 + S-003 | **FIX (re-measure)** | Rule file re-measured at end of pass: **~1,425 words** (`wc -w`) ≈ ~1,850–2,150 tokens. The genuinely stale datum was iteration-2's "~1,120 words" claim, not the token estimate; the file grew ~150 words this pass as Critical fixes landed in the shipped artifact. All three design-doc figures updated + "re-count at ratification" flag added |
| RT-004 | S-001 | **FIX (small)** | Add calendar cap to graduation deferral: "next milestone or ~3 months, whichever first" |
| FM-002 | S-012 | **FIX (small x2)** | Add forward-nav fallback footnote to each template's Segment Index so it travels with the artifact |
| FM-006 | S-012 | **FIX (small)** | Add same calendar bound to Backfill staleness trigger |
| RT-003 / PM-002 | S-001 + S-004 | **FIX (small)** | Name the commit-cadence checkpoint's correlated-SPOF + owner (reuse FU.3 directive) in one sentence |
| FM-007 / IN-004 | S-012 + S-013 | **FIX (small)** | Add rotation-interruption resume rule (parity check is the resume detector) + halt-and-escalate on mismatch |
| PM-003 | S-004 | **FIX (small)** | Extend the required rotation parity check to Backfill Queue row counts |
| FM-003 | S-012 | **FIX (word)** | Note batch-harvest overshoot is bounded by "one batch," not "one entry" |
| DA-004 | S-002 | **FIX (small)** | Flag the FU.5 "cross-log linked traversal" reading as the interpretation taken (per-log linked-list + id citation) |
| IN-003 | S-013 | **FIX (word)** | Make the same-turn append obligation explicit for handoff-carried candidates in LOG-M-005 |
| FM-005 | S-012 | **FIX (small)** | Real drift in live data — add cross-log citation normalization (`Related: <id>`) to Adoption step 4 |
| DA-002 | S-002 | **REBUT** | See below — factually unfounded |
| FM-004 | S-012 | **REBUT** | See below — existing `Superseded by:` pattern covers it; a formal dedup check is machinery |

## Rebuttals (evidence)

- **DA-002 (S-002, Major) — REBUTTED.** The finding asserts "a real collision already exists in the live bootstrap log … canonical `FU.1` vs. alias `FU.1` at entry `FU.9`, both `IN-PROGRESS`." Evidence (`grep -nE '^## FU\.' FEEDBACK-LOG.md`, 2026-07-06): the live log contains exactly **five** entries, **FU.0–FU.4**, **none carrying any `(alias: …)` suffix** (they predate the id/alias convention), and **there is no entry FU.9**. There is therefore no live alias collision to demonstrate against. The appendix already discloses, honestly, that the mechanism is "exercised here synthetically, not against already-collided data." A synthetic example is appropriate: the canonical/alias separation is identical whether the repeated alias is synthetic or live, so live data would add no design information. Declined per anti-bloat. *(Note: the same FU.0–FU.9 miscount recurs across the s-014 report; the live-log reality is FU.0–FU.4.)*

- **FM-004 (S-012, Major) — REBUTTED (with an existing-pattern pointer, no new machinery).** The finding wants a cross-channel de-duplication check. Under the single-writer-per-log discipline (LOG-M-005) the appending context has the recent turn in view, so a chat/inline-doc duplicate is a judgment the writer already exercises. When a duplicate *is* noticed, the **existing** `Superseded by: FU.N` status-pointer (appendix → Common cases) links the two at zero new mechanism. A mandatory scan-before-mint step is exactly the machinery the anti-bloat doctrine forbids for a MEDIUM-tier log. Declined; the existing pointer pattern is the sanctioned resolution.

- **Content-hash / immutability lint — REBUTTED (carried, re-confirmed).** Re-raised implicitly by integrity findings; git already provides the tamper-evidence a hash field would duplicate, at added maintenance cost. Declined, consistent with iterations 2–3.

## Additions/Deletions Ledger

Anti-bloat accounting (approximate, clause-level):

| Deletions (surface removed) | Additions (offset) |
|------------------------------|--------------------|
| DA-001 "generalizes cleanly …" clause (design L1.1) | FM-001 channel-relative clarification (rule + design + template) |
| RT-006 hook-note vocabulary-note blockquote (~3 lines) | SM-001 "and committed" header clause (rule file) |
| SM-001 offset: compressed redundant MEDIUM/auto-close clause | RT-005 compact Q5 row + 1 L0 clause |
| IN-001 rewrite (removes "addressed" overclaim, ~net 0) | FM-002 template footnotes (x2, one line each) |
| CC-001 removed stale "~2,150" over-count | Small Major clarifications (RT-004, FM-006, FM-007, PM-003, etc.) |

**Net (honest, P-022):** the **design doc** net-deletes overclaims (DA-001 clause, hook-note self-exemption). The **shipped rule file grew ~150 words (1,273 → 1,425)** because the Critical fixes ("and committed", channel-relative verbatim, rotation parity/recovery, cross-log `Related:`) belong in the artifact that actually governs behavior — exactly where the adversary (SM-001, SM-003) said they belong. **No new machinery** in the anti-bloat sense: zero new lint, zero new file, zero new subsystem; every added clause is prose that matches an existing mechanism. LOG-M-005 was compressed to partially offset.
