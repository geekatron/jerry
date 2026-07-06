# Iteration-008 Post-Tournament Fix Notes — FU/DEC Log Convention

> ps-architect (creator/owner) · 2026-07-06 · Post-tournament fix pass on the **6 panel-VERIFIED Criticals** from the iteration-008 VERIFIED-CRITICALS round.
> **Disposition-record choice (stated per task):** a NEW file `adversary/iteration-008/post-tournament-fix-notes.md` (this file), leaving `adversary/iteration-007/restore-notes.md` intact as the iteration-007 RESTORE record. This keeps each round's disposition history self-contained.
> **Trigger:** iteration-008 scored **0.72** (REVISE; gate 0.95) with 6 Criticals that each cleared a 3-lens refutation panel (factual / materiality / remediation-value) at 2-of-3 majority (DA-002-i8 at 3-of-3). The iteration-008 scorer states all 6 are wording-only, zero new machinery. **No re-score is claimed here** — this is an owner fix pass; next steps are the user's call.
> **Doctrine:** fix the panel-VERIFIED findings only; the 1 refuted Critical and the advisory Majors/Minors are settled. Simplify or disclose; never add machinery. Package stays ~there (~813 lines).
> **Constitutional:** P-003 no subagents · P-020 draft-only (edits under `projects/PROJ-031-cowork-skeleton/` only; no writes to `.context/`, `docs/`, `hooks/`) · P-022 each fix cites its panel disposition + file+line; honest line/word counts. Hygiene: repo-relative paths only, no employer-internal tokens.

## Navigation

| Section | Purpose |
|---------|---------|
| [Verified-Criticals Disposition](#verified-criticals-disposition) | The 6 VERIFIED Criticals: panel verdict + fix + landing sites |
| [DA-002-i8 in Detail](#da-002-i8-in-detail-priority-1) | The unanimous, highest-materiality fix |
| [Refuted / Advisory (Settled)](#refuted--advisory-settled) | What was deliberately NOT touched, and why |
| [Line & Word Accounting](#line--word-accounting) | Before/after counts (P-022) |
| [Hygiene](#hygiene) | /Users paths + employer-internal token scan |
| [Diagram & Nav Consistency](#diagram--nav-consistency) | Mermaid + H-23 checks |

## Verified-Criticals Disposition

Panel verdicts are quoted from `iteration-008/s-014-quality-score.md` Verification Roll-Up and the per-lens files under `iteration-008/verify/`. Each row: the finding, its 2-of-3 (or 3-of-3) panel result, the fix landed, and the exact artifacts touched.

| # | Finding | Panel (Factual / Materiality / Remediation) | Dimension | Fix (wording-only, zero machinery) | Landing sites |
|---|---------|----------------------------------------------|-----------|-------------------------------------|----------------|
| 1 | **DA-002-i8** | VERIFIED / **VERIFIED** / VERIFIED = **3-of-3** | Completeness | Content-aware dedup: key on `path#anchor` **and** marker text (vs. the entry's existing Verbatim); skip only a true unchanged re-read; a changed marker = a **new** append-only entry (`Related: <old id>`), never a silent skip. | rule inline bullet (`feedback-decision-logs-standards.md`); `FEEDBACK-LOG.template.md`; `examples-appendix.md` Common cases |
| 2 | **FM-001-i008fmea** | VERIFIED / REFUTED / VERIFIED = 2-of-3 | Internal Consistency | Delete the false "detected by lint 2's contiguity/orphan check" clause; rest the Q3-forcing-function exemption on the **no-data-loss** property; state explicitly that no lint detects Segment-Index overflow (matches rule Scope-limits (e)). Also closes advisory CV-001-i8 (same defect, 2nd strategy). | design doc L2 "One shared dependency" (`:264`) |
| 3 | **RT-001-20260706-iter8** | VERIFIED / REFUTED / VERIFIED = 2-of-3 | Internal Consistency | Require the P-003 background-agent candidate to carry the operator's words **unaltered** as a distinct sub-field; the orchestrator appends *that* as the Verbatim, never a worker paraphrase. | design L1.1 candidate bullet (`:78`); rule LOG-M-005 (`:27`); `FEEDBACK-LOG.template.md`; `LLM-DECISION-LOG.template.md` |
| 4 | **DA-001-i8** | VERIFIED / REFUTED / VERIFIED = 2-of-3 | Internal Consistency | Disclosed-residual clause at the "ids never reset" invariant: worktree-merge renumbering cannot repair **inbound** external citations (ADR `Reflected in:`, DECISION `Source:`, another log's `Related:`); prefer the graduated id as the surviving side; else operator `grep`s + repairs by hand. | design L1.1 Scope-boundary bullet (`:79`); rule LOG-M-005 (`:27`) |
| 5 | **PM-002-iter8** | VERIFIED / REFUTED / VERIFIED = 2-of-3 | Completeness | Restate the numeric cap (~50 entries / ~800 lines) directly in the artifacts a session actually appends to. | `FEEDBACK-LOG.template.md` + `LLM-DECISION-LOG.template.md` Segment Index sections; **live** `FEEDBACK-LOG.md` + `LLM-DECISION-LOG.md` bootstrap-conventions sections |
| 6 | **FM-002-i008fmea** | VERIFIED / REFUTED / VERIFIED = 2-of-3 | Evidence Quality | Canonicalize the inline-doc dedup key to `path#heading-anchor` (edit-stable; raw `:line` a drift-prone fallback) at all 3 specification sites; add one concrete worked Context-line example. | design entry-schema Context row (`:61`); rule inline bullet; `FEEDBACK-LOG.template.md`; worked example in `examples-appendix.md` |

**All 6 corrective actions were confirmed by every remediation-value panel as adding no machinery** (`iteration-008/verify/*-refutation-remediation-value.md`): DA-002-i8 reuses the existing Verbatim field; FM-001/CV-001 is a delete-and-reword; RT-001 and DA-001-i8 are one-clause disclosures; PM-002 restates an existing number; FM-002 fixes a key form + adds one example. Zero new lint / file / field / subsystem, consistent with the package's 8-round anti-bloat doctrine.

## DA-002-i8 in Detail (Priority 1)

**Why it mattered most (materiality panel, 3-of-3):** the iteration-007 RESTORE FM-001 fix (check-before-mint dedup) keyed **only** on `source: inline-doc` `path:line/anchor` location. A re-encountered marker whose *text changed in place* at the same line matched the location key and was skipped — so **edited feedback was silently lost**. This is a mechanism-level drop (no memory dependency), and it directly falsified the package's own "over-capture, never lost" claim (`feedback-decision-log-convention-design.md:91`). It was a regression introduced by the very fix that closed the prior over-capture finding — a fresh interaction the RESTORE pass (which re-verified only the original 6 iteration-006 Criticals) did not examine.

**Fix chosen (and why):** dedup applies **only to UNCHANGED markers** (location AND text identical). A **changed** marker is treated as **new feedback → a new append-only entry**, linked to the prior capture via `Related: <old FU.N>`. Rationale, stated in the artifacts:

- **Operator burden stays zero.** The content comparison is performed by the assistant during harvest (it already reads the marker and the existing entry's Verbatim); the operator does nothing new.
- **A new entry, not an in-place update.** Rewriting the old entry's Verbatim in place was rejected because it would breach the package's own "exactly two sanctioned edits to a sealed entry" rule (status pointer + hygiene redaction; L1.4). Minting a new entry is the internally-consistent, append-only choice and loses nothing.

This wording is identical across the three artifacts that state the dedup rule (rule file, FEEDBACK template, appendix), preventing the propagation-gap class that drove prior rounds.

## Refuted / Advisory (Settled)

Per the verified-criticals protocol, these were **not** touched:

- **PM-001-iter8** — REFUTED 0-of-3. The factual-lens panel found it restates a CP-01-vs-P-003-exception tension raised, closed, and re-verified as closed in iterations 3, 7, and 8. Settled; no action.
- **Advisory Majors** (CC-001-i8, IN-005-i8, PM-004-i8, DA-003-i8, DA-004-i8, FM-003-i008fmea, FM-004-i008fmea, CV-001-i8) — advisory-only, no scoring weight per protocol. **Exception:** CV-001-i8 (design doc misattributes Segment-Index-overflow detection to lint 2) is the *same defect* as VERIFIED FM-001-i008fmea and was closed by that fix at no extra cost. The remaining advisories were left as disclosed/monitored per the scorer's own priority list (items 7-9, advisory).
- **Advisory Minors** (DA-005-i8, etc.) — no action.

## Line & Word Accounting

| Stage | Package lines (6 files) | Rule-file words |
|-------|-------------------------|-----------------|
| Pre-pass (v9, iter-7 RESTORE close) | 813 | 2,281 |
| Post-pass (v10, this pass) | **818** | **2,671** |

**Net: +5 lines (~0.6%)** — the PM-002 cap restatement (a 2-line note × 2 templates = +4) plus the v10 changelog row itself (+1); the other five fixes landed **within existing lines** (table cells, bullets, paragraphs), so they add words but no lines. **Per-file lines:** design doc 362 → 363 (+1, the v10 changelog row; the four within-doc content edits are within-line); rule file 90 → 90 (within table cells / bullet); FEEDBACK template 64 → 66 (+2, PM-002 cap); DEC template 68 → 70 (+2, PM-002 cap); appendix 173 → 173 (within-bullet); hook note 56 → 56 (untouched).

**Rule-file words 2,281 → 2,671 (+390):** the six iteration-008 verified-Critical disclosures landed in the shipping artifact (where the adversary said such disclosures belong). This is the standing `[USER-DECISION]` overage vs the ~1,500-token soft target — unchanged in kind from prior rounds, larger in degree; the design doc's word-count citations (L0, L2, Staged Artifacts) were refreshed to 2,671 so no stale count remains (P-022). Token estimate ≈ 3,470–4,010 (1.3–1.5 tokens/word); re-count at ratification.

**Two live bootstrap files also edited (PM-002 acceptance):** `projects/PROJ-031-cowork-skeleton/FEEDBACK-LOG.md` and `LLM-DECISION-LOG.md` each gained a one-line cap statement in their bootstrap-conventions section. These are the project's operational logs (not part of the 6-file package); the edit closes PM-002's "the shipped/live artifact is missing the cap" gap, which was explicitly about the file's present state.

## Hygiene

Scanned all 6 deliverable files after edits:

- **Absolute home-directory (`[home]/`) paths:** none introduced (all new text uses repo-relative paths or no path). Verified clean.
- **Employer-internal tokens** (employer names, internal-KB names, codenames, internal work-item ids): none introduced. New text uses only generic terms (`ADR`, `DECISION`, `Reflected in:`, `Source:`, `PROJ-NNN`, placeholder anchors like `research/pricing-options.md#tam-sam-som`). Verified clean.
- The two illustrative anchors added (`#pricing-section`, `#tam-sam-som`, `research/pricing-options.md`) are generic examples, not real internal artifacts.

## Diagram & Nav Consistency

- **Mermaid diagram (a)** — segment-rotation `flowchart` (design L1.4): shows `FU.0–FU.49` per segment, consistent with the ~50-entry cap the PM-002 fix restates. No change needed; remains accurate.
- **Mermaid diagram (b)** — entry-lifecycle `stateDiagram-v2` (rule file FEEDBACK-LOG section): does not depict the dedup gate, so the DA-002-i8 content-aware-dedup change introduces no inconsistency with it. (Adding the dedup gate to the diagram was advisory FM-003-i008fmea, refuted-for-weight and out of this pass's scope; not touched, per anti-bloat + scope discipline.) Remains accurate.
- **H-23 navigation tables:** untouched in every file; all edits were inside existing sections. No new `##` sections were added, so no nav-table row is missing. Verified intact.
