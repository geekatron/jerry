# FMEA Report: Feedback/Follow-Up + LLM-Decision-Log Convention Package (iteration 2)

> **Blind execution note:** Per protocol, this analysis was produced without reading any prior adversary iteration output (including this deliverable's own iteration-001 FMEA). Findings below are independently derived from the deliverable package + the explicitly permitted supplementary files (ux/heuristic-evaluation.md, revision-notes.md, research doc, bootstrap logs). Any overlap with iteration-001 findings is coincidental convergence on the same evidence, not copying.

## Document Sections

| Section | Purpose |
|---------|---------|
| [Execution Context](#execution-context) | Strategy, deliverable, scope |
| [Summary](#summary) | Overall assessment |
| [Element Inventory](#element-inventory) | Step 1 decomposition |
| [Findings Summary](#findings-summary) | All FM-NNN findings, RPN-ranked |
| [Finding Details](#finding-details) | Expanded Critical + Major findings |
| [Recommendations](#recommendations) | Prioritized corrective actions |
| [Scoring Impact](#scoring-impact) | Mapping to S-014 dimensions |
| [Execution Statistics](#execution-statistics) | Protocol completion |

---

## Execution Context

- **Strategy:** S-012 FMEA (Failure Mode and Effects Analysis)
- **Template:** `.context/templates/adversarial/s-012-fmea.md`
- **Deliverable:** `projects/PROJ-031-cowork-skeleton/design/feedback-decision-log-convention-design.md` (v3, 2026-07-06) + `design/staging-feedback-logs/{feedback-decision-logs-standards.md, FEEDBACK-LOG.template.md, LLM-DECISION-LOG.template.md, examples-appendix.md, hook-design-note.md}`
- **Criticality:** C4 (engagement gate 0.95, user-set)
- **Date:** 2026-07-06
- **Reviewer:** adv-executor (S-012, blind background execution, iteration 2)
- **H-16 Compliance:** S-003 Steelman is not directly required before S-012 (H-16 names S-002/S-004/S-001); this deliverable's own changelog documents multiple prior adversary iterations at C4 (cowork-skeleton and adr-convention orchestrations show S-003 executed in the group sequence), so the C3+ Steelman-before-critique precondition is satisfied by the tournament's own sequencing.
- **Elements Analyzed:** 10 | **Failure Modes Identified:** 11 | **Total RPN:** 1663

---

## Summary

The package is a deliberately MINIMAL, MEDIUM-tier convention (anti-bloat by design), and that posture is accepted as valid per the engagement brief — descoping is not itself penalized. However, this FMEA finds **3 Critical failure modes**: (1) the design's foundational single-writer-per-log discipline has no enforcement mechanism and is in direct, acknowledged tension with the user's explicit requirement to "leverage background agents" (FEEDBACK-LOG.md FU.2), with no corrective action offered even though the framework's own P-003 orchestrator-worker topology would resolve it structurally; (2) the rule file that actually ships to `.context/rules/` (`feedback-decision-logs-standards.md:3`) makes an unqualified, present-tense survival/hook-assists claim that the design doc itself qualifies more carefully elsewhere — an overclaim in the governing artifact; (3) the manual, content-level segment-rotation procedure has no guard against a concurrent append landing mid-rotation. Six Major and two Minor findings round out the lifecycle coverage (entry creation, backfill, segment linking, cross-log navigation). **Recommendation: REVISE** — all three Criticals are closeable by small, anti-bloat-consistent wording/rule additions (no new machinery required), consistent with this package's own remediation doctrine.

---

## Element Inventory

| # | Element | Deliverable Locus |
|---|---------|--------------------|
| E1 | Entry creation — chat channel (capture triggers) | design.md L74-83; hook-design-note.md Seam 2 |
| E2 | Entry creation — inline-doc channel (harvest) | design.md L79,81; standards.md L36 |
| E3 | Alias/canonical id mapping (FU.6 scheme) | design.md L61-70; standards.md L27; templates |
| E4 | Back-reference disambiguation (bare-alias queries) | design.md L68; examples-appendix.md "Common cases" |
| E5 | Rotation trigger (segment cap detection) | design.md L162-177; standards.md "Segment rotation" |
| E6 | Segment linking (prev/next, immutability) | design.md L172-173; standards.md L51-52 |
| E7 | Segment index + Backfill Queue persistence across rotation | design.md L174,177; templates' Segment Index / Backfill Queue sections |
| E8 | Cross-log navigation (FEEDBACK ⇄ DECISION by canonical id) | design.md L175; standards.md L53 |
| E9 | Backfill (pre-log items) | design.md Q4, adoption step 5; FEEDBACK-LOG.md/LLM-DECISION-LOG.md Backfill Queue |
| E10 | Multi-session / multi-writer concurrency | design.md L70 (LOG-M-005 residual-risk disclosure) |

---

## Findings Summary

| ID | Element | Failure Mode | S | O | D | RPN | Severity | Affected Dimension |
|----|---------|-------------|---|---|---|-----|----------|--------------------|
| FM-001-20260706-i2 | E10 | Single-writer discipline unenforced; conflicts with explicit background-agent requirement | 8 | 6 | 7 | 336 | Critical | Completeness / Internal Consistency |
| FM-002-20260706-i2 | Rule file (governs, not an inventory element) | Unqualified present-tense "survive…/hook assists" claim in the artifact that ships to `.context/rules/` | 8 | 6 | 6 | 288 | Critical | Internal Consistency |
| FM-003-20260706-i2 | E5+E10 | Rotation procedure has no guard against a concurrent append landing mid-rotation | 8 | 4 | 7 | 224 | Critical | Methodological Rigor |
| FM-004-20260706-i2 | E3/E10 | Id-integrity lint cannot distinguish a legitimate crash/retry gap from a real dropped entry | 5 | 4 | 6 | 120 | Major | Methodological Rigor |
| FM-005-20260706-i2 | E2 | Inline-doc harvest blind spot from the framework's own CB-05 partial-Read practice, undisclosed as a distinct cause | 6 | 5 | 6 | 180 | Major | Completeness |
| FM-006-20260706-i2 | E9 | Backfilled entries get tail-appended monotonic ids despite predating existing entries chronologically; no disclaimer | 5 | 5 | 6 | 150 | Major | Completeness |
| FM-007-20260706-i2 | E7 | Rotation procedure silent on what happens to the Backfill Queue section (move / freeze / duplicate) | 4 | 5 | 7 | 140 | Major | Methodological Rigor |
| FM-008-20260706-i2 | E5 | Cap math assumes typical entry size; a single oversized verbatim entry can itself exceed the cap | 6 | 3 | 6 | 108 | Major | Methodological Rigor |
| FM-009-20260706-i2 | E1 | Capture-trigger heuristics (incl. hook Seam 2's broad interrogative cues) have no exclusion guard against over-capture | 3 | 6 | 6 | 108 | Major | Completeness |
| FM-010-20260706-i2 | E8 | No signal when a cited canonical id is later corrected/superseded; stale cross-references can accumulate | 3 | 5 | 5 | 75 | Minor | Traceability |
| FM-011-20260706-i2 | E3/E4 | Bare-alias back-reference disambiguation requires an unbounded cross-segment scan at C4-scale logs | 2 | 4 | 5 | 40 | Minor | Methodological Rigor |

**Finding ID Format:** `FM-{NNN}-20260706-i2` (iteration-2 execution identifier, disambiguates from iteration-001's FM-NNN ids).

---

## Finding Details

### FM-001-20260706-i2: Single-writer discipline is a convention, not a mechanism — and conflicts with the requirement that motivated the whole feature

| Attribute | Value |
|-----------|-------|
| **Severity** | Critical (RPN 336) |
| **Element** | E10 — Multi-session / multi-writer concurrency |
| **Strategy Step** | Step 2 (enumerate) + Step 3 (rate) |

**Evidence:** design.md L70: *"Concurrent writers appending to the *same* log file (e.g. parallel/background agents) are a **disclosed residual risk** — the scheme is **collision-resistant, not collision-proof**; it is backstopped by the id-integrity lint (L5 #2), which *detects* a duplicate/gap rather than *preventing* the race."* Compare the requirement that commissioned this feature, FEEDBACK-LOG.md L63 (FU.2 verbatim): *"I would like you to use the most appropriate jerry (jerry:\*) skills and agents to build this into the Jerry Framework and **leverage background agents** so that we don't burn through the main context window."* LOG-M-005 (standards.md L27) states the append discipline as a **SHOULD**-tier convention with no described serialization mechanism.

**Analysis:** Under the S-012 rubric this is a **Missing** failure mode at the corrective-action level: the design correctly *identifies* the risk (P-022 credit for honest disclosure) but stops at disclosure precisely where the user's own explicit request (background agents) makes the risk **most likely to manifest**, not a theoretical edge case. The obvious structural fix is already native to Jerry's own governance: the orchestrator-worker topology (P-003/H-01, `agent-development-standards.md` Pattern 2) means worker/background agents should never hold direct write access to a shared log file — they return findings via a structured handoff, and only the orchestrating context appends. The design never states this as the enforcement path, leaving "single-writer" as aspirational language with a lint-only (post-hoc, not preventive) backstop. Severity 8 (not 9-10) because normal single-session usage is unaffected; Occurrence 6 because the feature exists *because* background agents were requested; Detection 7 because the lint only catches duplicate/gap ids after the fact, not the underlying lost-write scenario for true concurrent filesystem writes.

**Corrective Action:** Add one clause to LOG-M-005 (or a short new sentence in the Scoping section): "Log appends occur only in the orchestrating/main context (P-003); worker and background agents MUST return feedback/decision candidates via structured handoff for the orchestrator to append, never write the log file directly." Zero new machinery — this reuses the existing handoff protocol (`agent-development-standards.md` Handoff Protocol) that background agents already use.

**Acceptance Criteria:** LOG-M-005 (or an adjacent line) explicitly names the orchestrator-only-append rule; no new lint, no new file.

**Post-Correction RPN estimate:** S=8, O=3 (structural prevention, not just convention), D=7 (lint remains the only detector) → **168** (Major; the residual reflects that this becomes a documented discipline, not a technical lock — an accepted trade for a MEDIUM-tier convention).

---

### FM-002-20260706-i2: The artifact that actually ships to `.context/rules/` overclaims

| Attribute | Value |
|-----------|-------|
| **Severity** | Critical (RPN 288) |
| **Element** | Rule file framing (governs all downstream elements) |
| **Strategy Step** | Step 2 (enumerate) — Incorrect/Inconsistent lens |

**Evidence:** `design/staging-feedback-logs/feedback-decision-logs-standards.md:3`: *"Two append-only, segment-rotating ledgers so user feedback and human/LLM decisions **survive compaction, sessions, and model swaps**. MEDIUM tier (HARD ceiling is full at 25/25). **Fail-open hook assists**; nothing auto-closes."* Compare the more carefully hedged design doc L30: *"(Scope note: the ledgers persist *what is logged*; they do not by themselves guarantee that every turn gets logged. Capture stays a **MEDIUM (SHOULD)** discipline until the fail-open hook of Q3 ships — see L1.3.)"* and Q3's own status (design.md L247, hook-design-note.md L56): the hook is **"designed in v1... but shipped as a separate gated change"** — i.e., not built, not installed, not currently "assisting" anything.

**Analysis:** This is an **Inconsistent** failure mode between two artifacts in the same package, and it lands in the one that matters most operationally: the rule file is the artifact designed (by the package's own anti-bloat doctrine) to be **self-contained** enough to govern behavior without requiring a read of the 300-line design doc. An operator or future agent who reads only `feedback-decision-logs-standards.md` — the intended, lean, standalone consumption path — receives an unqualified survival guarantee and a present-tense claim that a hook "assists" when no hook currently exists. This is precisely the "overclaimed coverage" class the engagement brief flags as Critical regardless of package minimalism: a MEDIUM-tier, deliberately small convention is a legitimate posture; a MEDIUM-tier convention whose canonical rule text reads as a stronger guarantee than the design doc itself claims is not. Severity 8: an operator who relies on the stated guarantee and later discovers capture was skipped (because LOG-M-001 is SHOULD, not enforced) experiences a genuine trust/governance failure, not just a documentation nit. Occurrence 6: the rule file is the file most likely to be read in isolation (that's its designed purpose). Detection 6: a careful reader cross-referencing the design doc would catch it, but the rule file gives no internal signal to prompt that cross-reference.

**Corrective Action:** Amend `feedback-decision-logs-standards.md:3` to carry the same qualifier the design doc already uses, e.g.: *"...so that, once captured, user feedback and decisions survive compaction, sessions, and model swaps. Capture itself is a MEDIUM (SHOULD) discipline; a fail-open hook is designed to assist but is not yet shipped (see hook-design-note.md)."* This is a ~20-token addition, well inside the ratified ~1,690-token budget, and requires no new mechanism — purely a wording fix consistent with the package's own subtraction/anti-bloat remediation pattern (design.md Revision Changelog v3).

**Acceptance Criteria:** Rule-file preamble no longer makes an unqualified survival claim or present-tense hook-assists claim in isolation from the capture-is-MEDIUM caveat.

**Post-Correction RPN estimate:** S=8, O=3 (claim now self-qualifying), D=3 (no cross-reference needed) → **72** (Minor).

---

### FM-003-20260706-i2: Rotation is a manual content operation with no concurrent-write guard

| Attribute | Value |
|-----------|-------|
| **Severity** | Critical (RPN 224) |
| **Element** | E5 (rotation trigger) × E10 (concurrency) |
| **Strategy Step** | Step 2 (enumerate) — Missing lens |

**Evidence:** design.md L177: *"Rotation procedure (documented, not new enforcement): copy the filled ACTIVE content to the next `.{NNN}.md`, mark it SEALED with prev/next, reset the ACTIVE to a fresh segment-N+1 header, and continue canonical ids... **Post-rotation parity check:** confirm the sealed segment's entry count matches the ACTIVE file's pre-seal count before continuing (a 5-second `grep -c '^## FU\.'` on both — nothing dropped or duplicated in the copy)."* hook-design-note.md L50 independently confirms rotation "stays operator/assistant-driven because it is a git-visible content operation" (i.e., no automated locking).

**Analysis:** A **Missing** failure mode: the rotation procedure describes copy-then-reset as if it is atomic, but it is three separate file operations (write sealed copy, mark SEALED, reset ACTIVE) performed by "the operator/assistant." If a second writer (background agent, per FM-001's already-disclosed concurrency risk) appends to the ACTIVE file **during** that window — after the content was copied to the sealed file but before the ACTIVE file is reset — the new entry can be silently lost (present in neither the sealed copy nor surviving the reset) or, depending on implementation order, duplicated. The only stated mitigation, the "post-rotation parity check," is presented as optional guidance ("a 5-second grep"), not a mandatory gate. Severity 8 (direct violation of "don't lose feedback," the design's own stated thesis, design.md L30); Occurrence 4 (rotation is rare — every ~50 entries — narrowing the window, but not zero, especially once FM-001's background-agent scenario is realized); Detection 7 (nothing but a manual, optional grep — no lint currently checks post-rotation parity, and the existing L5 lints run at commit time, potentially long after the race occurred).

**Corrective Action:** Promote the "post-rotation parity check" from a documented suggestion to a **required** step in the rotation procedure (one word change: "SHOULD confirm" → the procedure's step list itself, not just prose praise for doing it), and add one sentence noting that rotation should be treated as a short critical section — the same orchestrator-only-append discipline recommended for FM-001 also closes this gap, since a single writer cannot race itself.

**Acceptance Criteria:** Rotation procedure lists parity-check as a numbered, required step (not a parenthetical aside); FM-001's orchestrator-only-append fix is cross-referenced as the structural mitigation.

**Post-Correction RPN estimate:** S=8, O=3 (single-writer-via-orchestrator narrows this further), D=4 (mandatory check) → **96** (Major).

---

## Recommendations

Prioritized corrective actions (Critical first, then Major). All are wording/rule additions — no new lint, no new subsystem, consistent with the package's own anti-bloat doctrine.

| ID | Corrective Action | Est. RPN Reduction |
|----|--------------------|---------------------|
| FM-001 | Add orchestrator-only-append clause to LOG-M-005, citing P-003 handoff protocol as the enforcement path for background agents | 336 → 168 |
| FM-002 | Add "(once captured)" + hook-not-yet-shipped qualifier to `feedback-decision-logs-standards.md:3` | 288 → 72 |
| FM-003 | Promote post-rotation parity check from suggestion to required step; cross-reference FM-001's fix | 224 → 96 |
| FM-005 | Extend the "opportunistic harvest" disclosure to explicitly name CB-05 partial-Read (offset/limit) as a second cause, not just "never revisited" | 180 → ~120 |
| FM-006 | Add one sentence to the Backfill section: backfilled entries are not date-ordered by canonical id; sort by Context `datetime` for chronology | 150 → ~45 |
| FM-007 | State explicitly that the Backfill Queue section is NOT copied into sealed segments (lives only in ACTIVE, like the Segment Index) | 140 → ~60 |
| FM-004 | Document that a lint-flagged id gap MAY be a legitimate crash/retry artifact requiring a one-line reason note (mirrors terminal-evidence pattern) | 120 → ~100 |
| FM-008 | Add a one-line guard: an oversized single entry seals its segment immediately regardless of overall size | 108 → ~54 |
| FM-009 | Extend Seam 2's disclosed-residual framing to the over-capture direction (false positives), not just missed-capture | 108 → ~54 |
| FM-010 | (Minor, optional) Add `Superseded by: FU.N` convention for corrected entries | 75 → ~40 |
| FM-011 | (Minor, accepted trade at current scale; revisit if C4-scale log volume materializes) | 40 (no action required) |

---

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Negative | FM-001 (no corrective action for the concurrency risk tied to the feature's own motivating requirement), FM-005 (harvest blind spot undisclosed for a second cause), FM-006/FM-009 (unaddressed edge cases) |
| Internal Consistency | 0.20 | Negative | FM-002 (rule file overclaims relative to the design doc's own hedged framing) and FM-001 (single-writer discipline vs. explicit background-agent requirement) are both cross-artifact/cross-requirement contradictions |
| Methodological Rigor | 0.20 | Negative | FM-003, FM-004, FM-007, FM-008, FM-011 — the rotation, id-integrity, and Backfill-Queue-during-rotation procedures are under-specified at the edge cases a systematic FMEA pass surfaces |
| Evidence Quality | 0.15 | Neutral | All findings in this package cite specific file+line evidence with disclosed inference; no unsupported claims found |
| Actionability | 0.15 | Positive | Every Critical/Major finding here has a concrete, low-effort (wording-only) corrective action consistent with the package's own subtraction/anti-bloat remediation pattern |
| Traceability | 0.10 | Negative | FM-010 (no signal for stale cross-references once a cited entry is corrected/superseded) |

---

## Execution Statistics

- **Total Findings:** 11
- **Critical:** 3 (FM-001, FM-002, FM-003)
- **Major:** 6 (FM-004, FM-005, FM-006, FM-007, FM-008, FM-009)
- **Minor:** 2 (FM-010, FM-011)
- **Protocol Steps Completed:** 5 of 5 (Decompose, Enumerate, Rate, Prioritize, Synthesize)

**Overall assessment:** REVISE. None of the 3 Critical findings requires new machinery — each is closeable by a small wording/rule addition consistent with the package's own established anti-bloat, subtraction-first remediation pattern. The MEDIUM-tier, minimal-package posture itself is accepted as valid per the engagement brief; the findings above concern gaps in disclosure/corrective-action completeness and one direct overclaim, not insufficient scope of ambition.
