# Iteration-007 RESTORE Pass Notes — FU/DEC Log Convention

> ps-architect (creator/owner) · 2026-07-06 · RESTORE pass before the verified-criticals round.
> **Trigger:** workflow `wf_89445d40-a95` died mid-iteration-007 (API errors); per the ratified oscillation default, the verified-criticals endgame fired (live `FEEDBACK-LOG.md` FU.11). This pass does the three-part Restore work: (1) confirm the 6 iteration-006 Criticals are closed by TEXT/DISCLOSURE, (2) add the FU.10 visual layer (2 Mermaid diagrams that replace prose), (3) hygiene.
> **Doctrine:** simplify or disclose; never add machinery. Package must stay lean (~788 lines / 6 files). Diagrams REPLACE equivalent prose — net line count must not grow materially.
> **Constitutional:** P-003 no subagents · P-020 draft-only (no writes to `.context/`, `docs/`, `hooks/`; all edits under `projects/PROJ-031-cowork-skeleton/`) · P-022 cite file+line, label inference. Hygiene: repo-relative paths only, no employer-internal tokens.

## Navigation

| Section | Purpose |
|---------|---------|
| [Step 1 — Critical Closure Confirmation](#step-1--critical-closure-confirmation) | The 6 iteration-006 Criticals, verified in current text |
| [Step 2 — Visual Layer](#step-2--visual-layer-fu10) | 2 Mermaid diagrams, prose replaced |
| [Step 3 — Hygiene](#step-3--hygiene) | /Users paths + employer-internal tokens |
| [Line Accounting](#line-accounting) | Before/after line counts (net-neutral target) |
| [Residuals Disclosed](#residuals-disclosed) | Criticals closed by disclosure, not machinery |

## Step 1 — Critical Closure Confirmation

The iteration-006 owner-first remediation (v8) already closed the 6 Criticals by text/disclosure. This pass re-verified each against the CURRENT deliverable text (not the finding as stated). All 6 remain closed; no machinery was added to close any.

| # | Finding | Root cause | Closed where (current text) | Mechanism |
|---|---------|-----------|------------------------------|-----------|
| 1 | RT-001 | Redaction carve-out could launder tampering as hygiene (no size/category discipline, no "presence not veracity" disclosure) | rule `feedback-decision-logs-standards.md` LOG-M-002; design L1.1 | TEXT: redaction note names category + approximate size; a disproportionate redaction is a named review-scrutiny signal ("presence, not veracity") — the same honesty discipline every other trust-sensitive check carries |
| 2 | DA-001/FM-006 | "Four safety functions" undercounts the fifth (segment-index-overflow) sharing the commit-cadence checkpoint | design L2 "One shared dependency" | TEXT: "Four" → "Five"; segment-index-overflow named + explicitly exempted from the Q3-style forcing function (lint 2 detects/recovers it) |
| 3 | PM-001/IN-001 | AE-006e cited as cap-crossing backstop; its SSOT trigger is *compaction*, orthogonal to cumulative file growth | rule LOG-M-006; design L1.4 + L2 | DISCLOSURE (delete + narrow): false AE-006e-as-cap-backstop claim removed; the residual ("no automated cumulative-size backstop until the lint is wired/hook ships") is disclosed, not papered over |
| 4 | PM-002 | Install-stall trigger used unfilled placeholder `~N sessions` | design L2 Install-stall paragraph | TEXT: `~N sessions` → `~3 sessions or 30 days since this review round, or the next milestone checkpoint` (reuses the Q3 concrete-bound pattern) |
| 5 | FM-001 | No dedup for repeated inline-doc marker harvest | rule FEEDBACK-LOG inline-marker bullet; both templates; appendix | TEXT: check-before-mint against an existing entry with the same `source: inline-doc` `path:line/anchor`, reusing the existing sub-field (no new field/lint/doc-mutation) |
| 6 | FM-003 | "verbatim and full" contradicted by live split-entry practice (FU.5–FU.9) | rule LOG-M-002; design entry schema | TEXT: a multi-item message MAY split into per-item entries; each Verbatim is that item's own text; note the split in Summary (matches the live practice) |

## Step 2 — Visual Layer (FU.10)

User feedback FU.10 (2026-07-06, verbatim): *"Is there a reason why we don't have any diagrams to help visualize for yourself and the human operator what the process is supposed to be? This is massive walls of text..."*

Two compact `mermaid` diagrams added, each REPLACING equivalent prose so net line count does not grow materially:

- **(a) Segment-rotation linked-list** (`flowchart LR`) — placed in **design doc L1.4**. Visualizes: sealed segments `.001`/`.002` with prev/next links, the stable ACTIVE tail (`next: —`), the Segment Index living in ACTIVE, and cross-log navigation by canonical id (`Related: <id>`, no paths). Replaces the verbose linked-list / segment-index / cross-log-navigation prose in the L1.4 table rows.
- **(b) Entry lifecycle / disposition state machine** (`stateDiagram-v2`) — placed in **standards file FEEDBACK-LOG section** (the shipped rule the runtime LLM consults — "for yourself"). Visualizes: capture (chat OR `FU:`/`DEC:` inline-doc marker) → logged (mint canonical `FU.N` + record `(alias:)`) → `OPEN` → `IN-PROGRESS` → `DONE`/`WONTFIX` (evidence on terminal), with the inline-doc dedup (FM-001) and append-only reopen path. Replaces the disposition-enumeration prose.

Both diagrams are presentations of existing rules — zero new lint/file/field/subsystem (anti-bloat compliant; a diagram is not machinery). Mermaid node labels are terse, so word count does not grow.

## Step 3 — Hygiene

- Absolute home-directory paths in the 6 deliverable files: **none** (scan clean, before and after).
- Employer-internal token set (employer / internal-KB names, internal codenames, work-item ids): **2 hits found** — one leftover un-genericized internal-artifact-name token, appearing twice (design L0 scoping sentence + Improvement Ledger row 5). Both genericized → "single-artifact-only binding" / "Single-artifact-bound only".
- The English word "delineates" (a legitimate false-positive for the token scan): not present, so nothing to preserve.
- Re-scan after the v9 changelog was added caught two *meta-mentions* of the token pattern inside the changelog prose itself (describing the fix); reworded to describe the token class without quoting it, so the automated scan stays clean.
- This notes file uses repo-relative paths only and does not quote the raw employer tokens.

## Line Accounting

| Stage | Package lines (6 files) | Rule file words |
|-------|-------------------------|-----------------|
| Pre-pass (v8, iteration-6 close) | 788 | 2,240 |
| After 2 diagrams (raw) | 816 | 2,319 |
| After prose compression + row/bullet merges | **813** | **2,281** |

**Net: +25 lines (~3%)**, entirely the two user-requested Mermaid diagrams (~25 source lines) partially offset by prose compression (interpretation-flag, rotation-procedure, discovery-cost paragraphs; merged Linked-list + Cross-log-nav table row in L1.4; merged nav bullets in the rule file; folded `source` sub-field into the rule intro). **Zero new machinery** (no new lint/file/field/subsystem) — a diagram is a presentation of existing rules. Per-file: design doc 351 → 362; rule file 76 → 90 (+41 words = the lifecycle `stateDiagram-v2`). The ~1,500-token rule-file soft-target overage is unchanged as a standing [USER-DECISION]; word-count citations in the design doc (L0, L2, Staged Artifacts) refreshed to 2,281 so no stale count remains.

## Residuals Disclosed

Under the doctrine "simplify or disclose; never add machinery," 5 of the 6 Criticals close by **wording** and 1 closes by **disclosure of an accepted residual**:

| Critical | Closure branch | Residual disclosed? |
|----------|----------------|---------------------|
| RT-001 | wording (adds category+size scrutiny discipline) | — (the git-diff-backstop residual was already disclosed in prior rounds) |
| DA-001 | wording ("Four"→"Five" + explicit exemption) | — |
| **PM-001/IN-001** | **disclosure** (delete AE-006e overclaim; disclose the gap) | **Yes — 1: "no automated cumulative-size backstop until the L5 lint is wired or the Q3 hook ships; AE-006e fires on compaction, not on cross-session file growth"** |
| PM-002 | wording (concrete `~3 sessions / 30 days / next milestone` bound) | — |
| FM-001 | wording (check-before-mint dedup on existing sub-field) | — |
| FM-003 | wording (permit per-item split; note in Summary) | — |

**`residuals_disclosed` = 1** (PM-001/IN-001). The other five Criticals required no accepted-residual disclosure — they were fixable by wording within the anti-bloat posture.
