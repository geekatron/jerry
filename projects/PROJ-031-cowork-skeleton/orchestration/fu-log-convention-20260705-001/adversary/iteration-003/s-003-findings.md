# Steelman Report: Feedback & Decision Log Convention (Design + Staged Artifacts)

## Document Sections

| Section | Purpose |
|---------|---------|
| [Steelman Context](#steelman-context) | Deliverable, scope, method |
| [Summary](#summary) | Assessment, improvement count, recommendation |
| [Step 1: Deep Understanding](#step-1-deep-understanding) | Charitable interpretation of core thesis |
| [Step 2: Weakness Classification](#step-2-weakness-classification) | Presentation vs. structural vs. evidence vs. substantive |
| [Steelman Reconstruction (targeted)](#steelman-reconstruction-targeted) | Strongest-form fixes for surviving findings |
| [Step 4: Best Case Scenario](#step-4-best-case-scenario) | Ideal conditions, assumptions, confidence |
| [Improvement Findings Table](#improvement-findings-table) | SM-NNN findings, severity, dimension |
| [Improvement Details](#improvement-details) | Expanded Major findings |
| [Scoring Impact](#scoring-impact) | Dimension-level impact |

---

## Steelman Context

- **Deliverable:** `projects/PROJ-031-cowork-skeleton/design/feedback-decision-log-convention-design.md` (324L) + `design/staging-feedback-logs/{feedback-decision-logs-standards.md, FEEDBACK-LOG.template.md, LLM-DECISION-LOG.template.md, examples-appendix.md, hook-design-note.md}`
- **Deliverable Type:** Design (convention proposal + staged rule/template artifacts)
- **Criticality Level:** C4 (Critical) — touches `.context/rules/` on install, new ADR
- **Strategy:** S-003 (Steelman Technique)
- **SSOT Reference:** `.context/rules/quality-enforcement.md`
- **Steelman By:** adv-executor (iteration 3) | **Date:** 2026-07-06 | **Original Author:** ps-architect (this project)
- **Method:** Charitable-first read against the package's own stated posture (MEDIUM-tier, anti-bloat, descoped-with-disclosure is valid). Findings below are only what **survives** the strongest available interpretation. Blind protocol observed — no prior iteration-003 sibling-strategy output was read.
- **Context read (permitted):** `orchestration/fu-log-convention-20260705-001/{ux/heuristic-evaluation.md, revision-notes.md}`, `research/feedback-decision-log-research.md`, live `FEEDBACK-LOG.md`, live `LLM-DECISION-LOG.md`, `.context/rules/quality-enforcement.md`.

---

## Summary

**Steelman Assessment:** A genuinely disciplined, evidence-heavy MEDIUM-tier convention that has already absorbed two adversary remediation rounds (v3 0.64→v4 0.65, per the design doc's own changelog) sweeping the "overclaim" class of defect (guarantees, byte-exact fidelity, "cannot collide" language) thoroughly and consistently across all five downstream artifacts. Read charitably against its own stated MEDIUM/anti-bloat posture, the design does not need heavier machinery — it needs its **own already-adopted bootstrap files** and **its own adoption-plan prose** brought into agreement with the schema it says they already encode.

**Improvement Count:** 0 Critical, 2 Major, 3 Minor.

**Original Strength:** High. The disclosure discipline (residual risks, escape hatches, PROPOSED-DEFAULT labeling, honest token-budget overage reporting) is the strongest part of the package and is the reason no Critical survives a charitable read — every place a naive critique would call "overclaim," the text already hedges it (transcript-retention dependency, collision-resistant-not-proof, immutable-by-convention, "once captured" scoping).

**Recommendation:** Incorporate improvements (both Major findings are narrow, evidence-only fixes — no new machinery, consistent with the package's own anti-bloat doctrine). Not a fundamental-revision case.

---

## Step 1: Deep Understanding

**Core thesis (charitable):** Two append-only, segment-rotating markdown ledgers, backed by a logger-assigned/operator-alias id scheme and a MEDIUM-tier rule file, are the minimal codification of an emergent, previously-unshipped feedback/decision capture pattern — sized and enforced to fit a HARD-rule-ceiling-constrained, anti-bloat-doctrine framework. The design's central intellectual move is *disclosure over enforcement*: where a mechanism cannot be made technically airtight without violating the MEDIUM-tier/anti-bloat constraint, the design says so explicitly (collision-resistant not collision-proof; immutable-by-convention not filesystem-locked; capture is SHOULD until a hook ships) rather than overclaiming safety it cannot deliver. That posture is exactly right for a MEDIUM-tier convention and is not, on the evidence found in this iteration, undermined anywhere at Critical severity.

**Key claims examined and confirmed sound on charitable read:**
- The HARD-ceiling/MEDIUM-tier framing (design doc L2, `.context/rules/quality-enforcement.md` "Current count: 25 HARD rules... Zero headroom") is accurately cited.
- AE-002/AE-003 auto-C3 install-gate framing matches the SSOT auto-escalation table exactly.
- The turn-reference and automatable-metadata design (composite `{session_id}#{promptId}` anchor, model-per-turn resolution) is carried through faithfully from `research/feedback-decision-log-research.md` §B-turnref/§B-metadata with no drift.
- The transcript-retention/portability hedge ("byte-exact... while the transcript is retained and its pointer resolves on the reading machine") is now propagated identically across the design doc, the rule file, both templates, and the examples appendix — a genuinely swept fix, not a partial patch.

**Strengthening opportunities (not failures) noted for Step 2:** the package's weakest remaining surface is not its argument but its **own artifact fidelity** — places where the design doc asserts a state of the world ("the bootstrap files already encode the schema") that a direct read of those same bootstrap files only partially confirms.

**Decision Point:** Discernible, coherent thesis — proceeding to Step 2 (no exit).

---

## Step 2: Weakness Classification

| Weakness | Type | Magnitude |
|----------|------|-----------|
| Backfill Queue table schema (missing `Added` column) diverges between the two **live, already-adopted** bootstrap files and the two staged templates | Evidence / Structural | Major |
| Adoption-plan "rename `(user label: X)` → `(alias: X)`" step does not disclose that 5/10 FEEDBACK-LOG entries and all 3 LLM-DECISION-LOG entries currently carry **no suffix at all** to rename | Structural (adoption-plan completeness) | Major |
| Inline example in `FEEDBACK-LOG.template.md` renders the alias suffix without the colon (`(alias FU.0)`) while the canonical heading format, the appendix, and the DEC template all use `(alias: FU.0)` | Presentation | Minor |
| Q2 `scope: framework` tag (specified in the rule file and design doc) has no worked example in either template's Context field | Evidence / Completeness | Minor |
| The "by-convention, not filesystem-enforced" integrity caveat is fully stated in the design doc and restated for **segment rotation** in the staged rule file, but not restated for the base **FEEDBACK-LOG append-only/verbatim-wins** claim in that same rule file | Evidence / Structural | Minor |

All five are presentation/structural/evidence weaknesses in an otherwise sound design; none reach the substantive tier (nothing here calls the core two-ledger, logger-assigned-id, capped-segment thesis into question).

**Decision Point:** No Critical/substantive weaknesses found — proceeding to Step 3 (targeted reconstruction), not a caution flag.

---

## Steelman Reconstruction (targeted)

Per the template's own precedent for large deliverables ("key sections shown"), reconstruction is targeted at the two Major findings — narrow, evidence-only fixes consistent with the package's anti-bloat doctrine (no new lint, no new file, no new subsystem).

### [SM-001] Backfill Queue schema — before / after

**Before (live, `FEEDBACK-LOG.md:165`):**
```
| Approx date | Item | Source |
|---|---|---|
```
**Before (live, `LLM-DECISION-LOG.md:76`):**
```
| Approx date | Decision | Where recorded today |
|---|---|---|
```
**After (strongest form — bring the live tables into parity with the template + the design doc's own Q4 mechanics text, which requires an "added-date" per row):**
```
| Approx date | Added | Item | Source |
|---|---|---|---|
| 2026-06-30 | 2026-07-05 | "YAGNI is not a good answer"... | chat, prior session... |
```
```
| Approx date | Added | Decision | Where recorded today |
|---|---|---|---|
| 2026-06-29 | 2026-07-05 | Accept design-phase ceiling (~0.86)... | RESUME-CHECKPOINT.md |
```
*Rationale:* the design doc's own Q4 mechanics (line 269) says "Backfill Queue rows carry an added-date and are re-assessed at the same commit-cadence checkpoint" — a mechanism that needs the `Added` column the live tables do not have. Zero new machinery: this is a column the template and design text already specify; the live files simply have not been brought to parity with their own already-ratified schema.

### [SM-002] Adoption-plan heading-suffix rename — before / after

**Before (design doc, line 230):**
> "heading suffixes are renamed from the bootstrap `(user label: X)` form to the ratified `(alias: X)` form at install time"

**After (strongest form — disclose the asymmetry the current wording hides):**
> "heading suffixes are normalized to the ratified `(alias: X)` form at install time: entries FU.5–FU.9 / any entry already carrying `(user label: X)` are renamed in place; entries FU.0–FU.4 and DEC-LLM-001–003, which currently carry **no suffix**, receive a newly-added `(alias: —)` (they predate the id/alias convention and the operator gave no turn-local label for them at capture time)."

*Rationale:* a direct read of both live files (`FEEDBACK-LOG.md:26,41,55,71,84` and `LLM-DECISION-LOG.md:25,42,58`) shows zero suffix on 8 of the 13 live entries across both logs. The current plan text implies a uniform rename of an existing form; it should instead disclose the split between "rename" and "add fresh" so the install step does not silently improvise on entries the plan did not anticipate.

---

## Step 4: Best Case Scenario

**Ideal conditions under which this design is strongest:** a single operator, continuously mediated by one assistant session, working within the disclosed HARD-ceiling/MEDIUM-tier constraint, who accepts that "don't lose feedback" means "once captured, persists" rather than "captured automatically and losslessly" until the Q3 hook ships. Under those conditions — which match the validated adoption profile the design itself declares (single-writer-per-log, team use explicitly out-of-scope) — the two-ledger design with capped-collection segment rotation is a well-evidenced, appropriately minimal answer to a real, previously un-codified gap.

**Key assumptions that must hold:** (1) the operator will read the rule file's disclosures (or the design doc) rather than assume machinery-level enforcement; (2) background-agent writes are in fact routed through the orchestrator per the P-003 handoff convention (a procedural discipline, not a technically-enforced one — correctly disclosed as "collision-resistant, not collision-proof"); (3) the Q3 hook eventually ships, since until it does the MEDIUM rule has no L2 compensating control (also correctly disclosed).

**Confidence:** HIGH that the core design is sound and internally coherent; MEDIUM-HIGH that it is fully "installed-and-adopted" as claimed, given the two Major findings show the live artifacts trail the design text in two concrete, checkable places.

---

## Improvement Findings Table

| ID | Description | Severity | Original | Strengthened | Dimension |
|----|--------------|----------|----------|---------------|-----------|
| SM-001-20260706iter3 | Backfill Queue table schema (missing `Added` column) diverges between live bootstrap files and staged templates, contradicting the design doc's own Q4 "rows carry an added-date" mechanics and the Adoption plan's claim that the live files "already encode the schema... Backfill Queue" | Major | `FEEDBACK-LOG.md:165` `\| Approx date \| Item \| Source \|`; `LLM-DECISION-LOG.md:76` `\| Approx date \| Decision \| Where recorded today \|` | Add `Added` column to both live tables (matches `FEEDBACK-LOG.template.md:58` / `LLM-DECISION-LOG.template.md:63`) | Internal Consistency |
| SM-002-20260706iter3 | Adoption-plan heading-suffix rename step (design doc L2, adoption step 4) presumes all live entries already carry `(user label: X)`; 8 of 13 live entries across both logs carry no suffix at all | Major | `design/feedback-decision-log-convention-design.md:230` "renamed from the bootstrap `(user label: X)` form" | Disclose the rename/add-fresh split explicitly (see reconstruction above) | Completeness |
| SM-003-20260706iter3 | `FEEDBACK-LOG.template.md` inline example omits the colon in `(alias FU.0)`, inconsistent with the canonical heading format and the appendix's own worked examples | Minor | `FEEDBACK-LOG.template.md:20` "`FU.0 (alias FU.0)`, `FU.1 (alias FU.1)`, `FU.2 (alias FU.0)`" | `FU.0 (alias: FU.0)`, `FU.1 (alias: FU.1)`, `FU.2 (alias: FU.0)` | Internal Consistency |
| SM-004-20260706iter3 | Q2 `scope: framework` tag (design doc Q2; rule file Scoping section) has no worked example in either template's Context field, despite both templates otherwise embedding a full worked example | Minor | `FEEDBACK-LOG.template.md` Context format line (no `scope` mention); `LLM-DECISION-LOG.template.md` same | Add one parenthetical: "append `scope: framework` only when this is framework-level feedback captured inside an active project (Q2, pending ratification)" | Completeness |
| SM-005-20260706iter3 | The "by-convention, not filesystem-enforced" integrity caveat is stated for segment rotation in the staged rule file but not restated for the base FEEDBACK-LOG append-only/verbatim-wins claim in the same file (it is fully stated in the design doc) | Minor | `staging-feedback-logs/feedback-decision-logs-standards.md:38` "Corrections are append-only..." (no enforcement caveat) vs. design doc L1.1 full caveat | One clause: "(convention-only, git-backstopped; not a technical lock — see design doc)" | Traceability |

**Finding ID Format:** `SM-{NNN}-{execution_id}` where `execution_id = 20260706iter3` (iteration-3 adversary tournament run, this session).

---

## Improvement Details

### SM-001 (Major) — Backfill Queue schema drift

- **Affected Dimension:** Internal Consistency
- **Original Content:** Live `FEEDBACK-LOG.md` and `LLM-DECISION-LOG.md` Backfill Queue tables have 3 columns each (no `Added` column); the design doc's Adoption/migration plan (step 4) asserts the live files "already encode the schema... Backfill Queue"; the design doc's Q4 mechanics (line 269) separately specifies "Backfill Queue rows carry an added-date."
- **Strengthened Content:** Add the `Added` column to both live tables (values can be backfilled with the date the row was first noted, or `—` if unknown), bringing them to parity with the already-ratified template schema.
- **Rationale:** This is a narrow, verifiable schema mismatch between what the design doc claims is already true of the live artifacts and what those artifacts actually contain — exactly the class of "claim vs. reality" gap the tournament's overclaim sensitivity is calibrated to catch, though here the blast radius is one table column, not a safety or fidelity guarantee.
- **Best Case Conditions:** Fixed by a one-line edit to each live file; no schema redesign, no new lint, no new rule.

### SM-002 (Major) — Adoption-plan heading-suffix asymmetry

- **Affected Dimension:** Completeness
- **Original Content:** Design doc line 230 describes install-time suffix normalization as a uniform rename from `(user label: X)` to `(alias: X)`.
- **Strengthened Content:** Split the instruction: entries that already carry a `(user label: X)` suffix are renamed; entries with no suffix (FU.0–FU.4, DEC-LLM-001–003) receive a freshly-added `(alias: —)`.
- **Rationale:** A direct read of both live files shows 8 of 13 entries have no suffix to rename. Left as-is, an installer following the plan literally would not know what to do with those 8 entries — a real, checkable completeness gap in an otherwise carefully-sequenced adoption plan.
- **Best Case Conditions:** Fixed by one clarifying sentence in the Adoption/migration plan; no new machinery.

---

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Neutral/Slightly Positive | SM-002/SM-004 close small adoption-plan and template gaps; core design scope already thorough |
| Internal Consistency | 0.20 | Positive | SM-001/SM-003 directly close claim-vs-artifact and cross-artifact notation mismatches |
| Methodological Rigor | 0.20 | Neutral | Already strong (systematic disclosure discipline observed intact); no rigor gap found |
| Evidence Quality | 0.15 | Neutral | Citations throughout the package are accurate and verifiable against SSOT and live files; findings here are artifact-fidelity gaps, not evidence-quality gaps |
| Actionability | 0.15 | Positive | All 5 findings are single-edit, zero-new-machinery fixes — directly incorporable |
| Traceability | 0.10 | Slightly Positive | SM-005 closes a cross-reference gap (design doc has the caveat; rule file's base FEEDBACK-LOG section doesn't echo it) |

---

*Strategy: S-003 (Steelman Technique) | Template: `.context/templates/adversarial/s-003-steelman.md` | Executed: 2026-07-06T00:00:00Z*
