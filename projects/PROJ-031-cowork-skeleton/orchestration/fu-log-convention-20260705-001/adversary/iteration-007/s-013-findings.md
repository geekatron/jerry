# Inversion Report: Feedback & Decision Log Convention (FEEDBACK-LOG + LLM-DECISION-LOG)

**Strategy:** S-013 Inversion Technique
**Deliverable:** `projects/PROJ-031-cowork-skeleton/design/feedback-decision-log-convention-design.md` + `projects/PROJ-031-cowork-skeleton/design/staging-feedback-logs/{feedback-decision-logs-standards.md, FEEDBACK-LOG.template.md, LLM-DECISION-LOG.template.md, examples-appendix.md, hook-design-note.md}`
**Criticality:** C4 (engagement gate 0.95)
**Date:** 2026-07-06
**Reviewer:** adv-executor (S-013, iteration-007, blind protocol, VERIFIED-CRITICALS variant — Criticals subject to a 3-lens refutation panel: factual / materiality / remediation-value)
**H-16 Compliance:** S-003 Steelman is required earlier in the C3+/C4 sequence per H-16/quality-enforcement.md; not independently re-verifiable from this blind execution (iteration-001..006 findings were readable as disposition history; the live tournament artifacts for iteration-007/008 were off-limits per blind protocol except `restore-notes.md`). Assumed satisfied at the tournament level (all 6 prior rounds ran S-003 first).
**Goals Analyzed:** 6 | **Assumptions Mapped:** 9 | **Vulnerable Assumptions:** 3 (0 Critical, 1 Major, 2 Minor)

## Document Navigation

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Overall verdict |
| [Goal Inventory](#goal-inventory-step-1) | What the package must guarantee |
| [Anti-Goals](#anti-goals-step-2) | What would guarantee failure of each goal |
| [Assumption Map](#assumption-map-step-3) | Explicit/implicit assumptions, confidence |
| [Findings Table](#findings-table) | IN-NNN summary |
| [Finding Details](#finding-details) | Major/Minor findings expanded |
| [Refuted Critical Candidates](#refuted-critical-candidates-3-lens-panel) | Candidates considered and self-refuted before filing |
| [Loss-Guarantee & Null-Alternative Analysis](#loss-guarantee--null-alternative-analysis-directly-asked) | Answers the two questions the task poses directly |
| [Recommendations](#recommendations) | Prioritized mitigations |
| [Scoring Impact](#scoring-impact) | Mapping to S-014 dimensions |

---

## Summary

This is iteration-007 of the S-013 strategy against the **post-Restore (v9)** package state: iteration-006's 6 Criticals are confirmed closed in current text (verified independently below, not merely trusted from `restore-notes.md`), and two new Mermaid diagrams (FU.10) were added since the last adversarial pass and had **not yet been examined by any strategy**. Running a fresh Inversion pass (goal → anti-goal → assumption → stress-test) against the current text surfaces **one Major** finding: the design doc's newly-worded (v8/iter-006) "Segment-Index-overflow is exempt because lint 2 already detects/recovers it" claim (line 264) misattributes lint 2's actual detection scope (id uniqueness/contiguity/orphan-segment detection) to a materially different failure mode (the Segment Index *table itself* growing past its own stated ~100-line overhead threshold) — the identical bug *class* as the already-fixed IN-001/AE-006e finding from iteration-006, reintroduced in a different location during the very remediation that fixed the original. Two **Minor** wording-precision items are also noted (a diagram/prose semantic gap on "standing" DONE entries, and a lint-1 scope drift between the design doc and the shipped rule file). **No finding invalidates the package's core approach, and none of the three reaches Critical** under the 3-lens panel applied below — plausibility and consequence ceilings are bounded for all three (see [Refuted Critical Candidates](#refuted-critical-candidates-3-lens-panel) for candidates considered and rejected before filing, including one — the alias-normalization-count claim — that a first pass looked wrong but a second, verified pass against the live bootstrap log showed was in fact accurate).

**Recommendation:** ACCEPT with one targeted Major fix (wording-only, no new machinery, consistent with the package's own anti-bloat doctrine) and two optional Minor polish items. The core question this execution was asked to answer — does the package beat the null alternative and does anything guarantee loss — is addressed in its own section below; the answer has not changed materially from iteration-006's honest, already-disclosed assessment.

---

## Goal Inventory (Step 1)

| # | Goal (as stated or inferred) | Measurable form |
|---|---|---|
| G1 | Feedback-worthy user input, once given, is captured into the log | An entry exists for every turn matching a capture trigger (LOG-M-001) |
| G2 | Captured entries survive session boundaries, compaction, and model swaps | Bytes on disk in a committed, pushed git ref |
| G3 | Captured entries are discoverable/consulted in a *later* session | A new session's orientation step actually reads the log before acting |
| G4 | Entry ids and content remain intact under rotation and single-writer discipline | Contiguous, non-duplicated ids across all segments (L5 lint 2) |
| G5 | The convention actually gets installed so its protections apply | Ratification → `.context/rules/` + `mandatory-skill-usage.md` + `project-workflow.md` wiring |
| G6 | The Segment Index (the growth-navigation mechanism itself, FU.5) stays accurate *and* legible as the log scales | Index rows resolve id→file; index/queue overhead does not itself become an unreadable wall inside ACTIVE |

G6 is new relative to iteration-006's inventory — it is the goal the new finding below actually stress-tests (the *meta*-navigability of the navigation mechanism), distinct from G4 (id/content integrity, which lint 2 genuinely covers).

---

## Anti-Goals (Step 2)

- **AG-G1/G2/G3/G5:** unchanged from iteration-006 — all already disclosed exhaustively (Q5 no-detector residual; "once appended AND committed" durability scope; the read-side gap; the install-stall trigger). Not re-graded here; re-verified as still present in current text (see [Refuted Critical Candidates](#refuted-critical-candidates-3-lens-panel) for the specific re-verification of iteration-006's closures).
- **AG-G4:** A rotation is interrupted and the parity re-check never runs → **now has a persisted, session-start trigger** (`feedback-decision-logs-standards.md:67`, "before the *first* append of any session, if the Segment Index's last row does not match the ACTIVE file's actual last heading..."). Confirmed closed (was IN-003 in iteration-006).
- **AG-G6 (new):** A compensating-control citation for a disclosed residual turns out, on inspection, not to cover the risk it is invoked to cover — the exact anti-goal that produced iteration-006's Critical (AE-006e vs. compaction) — reappears **for a different named risk** (Segment-Index-overflow vs. lint 2's actual scope) → **IN-001-20260706-iter007 (Major)**.
- **AG-diagram-fidelity (new, FU.10-specific):** A diagram added to visually explain a mechanism silently narrows or contradicts the mechanism's own documented/demonstrated behavior, and — being new — has not yet been checked by any strategy → **IN-002-20260706-iter007 (Minor)**.
- **AG-artifact-drift (new):** The design doc and the shipping rule file describe "the same" lint check with different scope, so an installer reading only one artifact implements a narrower or broader check than intended → **IN-003-20260706-iter007 (Minor)**.

---

## Assumption Map (Step 3)

| ID | Assumption | Type | Confidence | Validation status |
|---|---|---|---|---|
| A1 | "Five safety functions... all fire at the same commit-cadence checkpoint" is consistent with the same sentence's claim that one of those five is "exempt... because lint 2... detects it" | Explicit wording (Internal Consistency) | Low | **Falsified** — see IN-001 |
| A2 | Lint check 2 ("id integrity: uniqueness + monotonicity + contiguity... orphan-segment cross-check") also covers Segment-Index *table-size* overhead | Implicit (Methodological) | Low | **Falsified against the lint's own stated scope** — see IN-001 |
| A3 | The entry-lifecycle diagram (`DONE --> [*]`) is a faithful abstraction of how "DONE" is actually used in this convention's own worked examples | Implicit (Technical/Process) | Medium | Contradicted by the template's own "DONE (standing — applies continuously)" worked example — see IN-002 |
| A4 | The design doc and the shipped rule file specify identical scope for lint check 1 (nav table presence) | Explicit wording (cross-artifact) | Medium | Design doc scopes to the two ACTIVE filenames only; rule file scopes to ACTIVE + sealed `*.NNN.md` — see IN-003 |
| A5 | The "8 live entries carry no suffix (FU.0–FU.4, DEC-LLM-001..003)" adoption-plan claim is still accurate against the current live bootstrap log | Explicit wording (verifiable against a live artifact) | Medium (pre-check) | **Verified TRUE** on direct inspection of the live `FEEDBACK-LOG.md`/`LLM-DECISION-LOG.md` — the newer entries FU.5–FU.11 all already carry `(user label: X)` suffixes handled by the separate "renamed in place" rule; the "8 with no suffix" enumeration is still exactly correct. **Refuted as a finding** — see [Refuted Critical Candidates](#refuted-critical-candidates-3-lens-panel) |
| A6 | AE-006e (compaction) is no longer cited anywhere as a cumulative-size backstop | Implicit (regression check on iteration-006's Critical) | High | **Verified TRUE** — `feedback-decision-logs-standards.md:28` and design doc L1.4 both now explicitly state AE-006e does *not* cover cap-crossing |
| A7 | The redaction/transcript-retention compounding risk (iteration-006 IN-002) is still disclosed in the current text | Implicit (regression check) | High | **Verified TRUE** — `feedback-decision-logs-standards.md:24` carries the hedge |
| A8 | The package (6 files) contains no employer-internal tokens or absolute host paths | Explicit (hygiene) | High | **Verified TRUE** by direct `grep` of all 6 target files (zero matches for `[home]/`, `[employer]`/`[employer]`); restore-notes.md's genericization claim corroborated independently |
| A9 | Rule-file token-budget overage is a live, accepted [USER-DECISION], not a silent scope-creep | Implicit (governance) | High | **Verified TRUE** — design doc L2 and rule-file header both still carry the disclosure; no new machinery added since iteration-006 |

---

## Findings Table

| ID | Assumption / Anti-Goal | Type | Confidence | Severity | Evidence | Affected Dimension |
|----|------------------------|------|------------|----------|----------|--------------------|
| IN-001-20260706-iter007 | Segment-Index-overflow "exempt... because lint 2 detects it" | Assumption (A1/A2) | Low | **Major** | design doc lines 199, 264; rule file `feedback-decision-logs-standards.md:82` | Internal Consistency, Methodological Rigor |
| IN-002-20260706-iter007 | Entry-lifecycle diagram models DONE as inert-terminal, contradicting the "standing" worked example | Assumption (A3) | Medium | **Minor** | rule file lines 36–48; `FEEDBACK-LOG.template.md:49` | Internal Consistency |
| IN-003-20260706-iter007 | Lint-1 scope drift: design doc vs. shipped rule file | Anti-Goal (cross-artifact wording) | N/A | **Minor** | design doc line 235; rule file `feedback-decision-logs-standards.md:81` | Traceability |

**Finding ID Format:** `IN-{NNN}-20260706-iter007`.

---

## Finding Details

### IN-001: Segment-Index-Overflow Exemption Misattributes Lint 2's Detection Scope [MAJOR]

**Type:** Assumption (compensating-control citation, same bug class as the already-closed iteration-006 IN-001/AE-006e finding, reintroduced for a different rule)
**Original Assumption:** Design doc, `feedback-decision-log-convention-design.md:264` ("One shared dependency" section): "**Five** safety functions — staleness review, graduation proposal, Backfill-Queue review, this install-stall re-assessment, **and the Segment-Index-overflow re-assessment (L1.4)** — all fire at the **same** commit-cadence checkpoint... The Segment-Index-overflow trigger is **explicitly exempt** from the Q3-style dated-worktracker forcing function (DA-001): unlike capture, its failure is detected by lint 2's contiguity/orphan check and is fully recoverable by re-reading segment headings, so it needs no owned review date."
**Inversion:** What the Segment-Index-overflow trigger actually names is defined earlier in the same document, `feedback-decision-log-convention-design.md:199` (L1.4 "Segment index" row): "if one ACTIVE segment's index+queue overhead ever exceeds ~100 lines, revisit at the same commit-cadence checkpoint... the fallback is to move the Segment Index to its own `*-INDEX.md` sidecar (deferred... not built now)." This is a **table-size/overhead** concern — the small `segment · file · canonical-id-range` table inside ACTIVE growing to the point of being a readability burden. Lint check 2, as defined in the shipping rule file (`feedback-decision-logs-standards.md:82`), is: "ids unique, strictly increasing, **and contiguous** across all segments... the same pass also `ls *-LOG.*.md` and flags any on-disk segment **absent from the Segment Index** (a silently-orphaned segment)." That check verifies (a) id contiguity and (b) that every on-disk segment file *appears* in the index — it says nothing about how many *rows* the index itself has grown to, or whether that row count has crossed the ~100-line overhead threshold. A perfectly contiguous, zero-orphan index with 200 rows (a 10,000-entry log, a scale the design doc itself cites elsewhere, line 199, "a 10k-entry log yields ~200 rows (~200 lines)") **passes lint 2 with zero complaint** while being exactly the overhead-overflow scenario the L1.4 row says needs re-assessment. Invert the claim directly: "what would guarantee the Segment-Index-overflow re-assessment never happens, and never gets caught?" — precisely the scenario the exemption text asserts is already covered: the checkpoint is skipped (per the same paragraph's own admission that all five functions can "miss together"), and lint 2 — which does not check row count — never fires, because there is nothing to fire on. This is the identical mismatch pattern that produced iteration-006's Critical (AE-006e cited as covering a risk — cumulative line growth — that its own SSOT trigger, compaction, does not cover): a named compensating control is cited by ID without verifying its actual detection scope against the specific risk it is invoked to close.
**Plausibility:** Low-to-Medium as an actual occurrence (requires the log to reach roughly 5,000–10,000+ entries, a scale far beyond this project's current usage — 12 FEEDBACK-LOG entries after multiple sessions), but the *logical* defect (an incorrect justification for an accepted exemption) is present today regardless of scale, and is High-confidence on inspection.
**Consequence:** Bounded, unlike the AE-006e case. Lint 2's actual job (id integrity, orphan-segment detection) is unaffected — no entry is lost, no id collides, no segment goes missing. The only thing that silently doesn't happen is the operator revisiting whether to split the Segment Index into its own `*-INDEX.md` sidecar once it becomes unwieldy — a readability/navigability degradation of one small table within ACTIVE, not a loss of any feedback or decision content. This is why the finding is Major, not Critical: it fails the "invalidates the deliverable's core approach" bar (Step 4 severity criteria) because the core loss-prevention/id-integrity machinery is untouched; it does meet the "significantly degrades deliverable value... requires mitigation" bar because it is a factual misstatement of what a named, cited control does, in the same document that elsewhere holds itself to a strict standard of only citing a control when its actual trigger matches the claimed risk (the whole reason iteration-006's AE-006e fix exists).
**Evidence:** `projects/PROJ-031-cowork-skeleton/design/feedback-decision-log-convention-design.md:199` (defines the actual overhead-based re-assessment trigger); `projects/PROJ-031-cowork-skeleton/design/feedback-decision-log-convention-design.md:264` (the exemption claim under review); `projects/PROJ-031-cowork-skeleton/design/staging-feedback-logs/feedback-decision-logs-standards.md:82` (lint 2's actual, textually-scoped detection criteria — id uniqueness/contiguity/orphan-segment only).
**Dimension:** Internal Consistency (a sentence names something as both one of "Five... all fire at the same checkpoint" and, in the next clause, exempt from needing any trigger at all, on a justification that does not match the cited mechanism's stated scope); Methodological Rigor (a specific lint check was cited as covering a risk without checking that lint's own defined scope against the claimed risk — the same verification gap iteration-006 closed for AE-006e, recurring here for lint 2).
**Mitigation:** Wording-only, no new machinery, consistent with the package's own anti-bloat/disclosure doctrine (the same style used to fix AE-006e in iteration-006): replace "its failure is detected by lint 2's contiguity/orphan check... so it needs no owned review date" with an honest statement of the actual, bounded residual — e.g., "no lint currently checks Segment-Index row-count/overhead (lint 2 checks id contiguity and orphan segments, not index size); the re-assessment is exempt from the Q3-style dated-worktracker forcing function not because it is automatically caught, but because the consequence of missing it is bounded to index-table readability (no data at risk, and the sidecar fallback remains available at any later checkpoint)." This keeps the (reasonable) decision to exempt this item from forced dated tracking, but grounds it in the actual, low-stakes consequence rather than a false claim of automatic lint coverage.
**Acceptance Criteria:** The design doc no longer claims lint 2 (or any named lint) detects Segment-Index row-count/overhead growth; the exemption from a dated forcing function is justified by the bounded consequence (readability only, no data loss, sidecar fallback available), not by a misattributed control.

### IN-002: Entry-Lifecycle Diagram Models "DONE" as Inert-Terminal, Understating the Convention's Own "Standing" Pattern [MINOR]

**Type:** Assumption (new content, unreviewed prior to this pass — added in the v9 Restore, FU.10)
**Original Assumption:** The `stateDiagram-v2` added to the shipped rule file (`feedback-decision-logs-standards.md:36-48`) models `DONE --> [*]` and `WONTFIX --> [*]` as absorbing terminal states, implying a `DONE` entry is closed/inert.
**Inversion:** The convention's own worked example in `FEEDBACK-LOG.template.md:49` demonstrates the opposite pattern for the majority of real `DONE` entries: `**Disposition:** **DONE (standing — applies continuously).**` — a standing directive is not dormant; it is a continuously-enforced rule that the assistant is expected to keep re-applying every session (the same pattern used for 3 of the 4 `DONE` entries in the project's own live bootstrap `FEEDBACK-LOG.md`, e.g. the commit-cadence and no-internal-refs directives). A diagram reader (human or, per the design's own hook-design-note precedent of using diagrams/state as a basis for tooling, a future automated consumer) could reasonably conclude `DONE` entries need no further attention, when the convention's own recommended usage pattern is that a `DONE (standing...)` entry is precisely the kind that must keep being honored.
**Plausibility:** Medium — the diagram is new (this pass is the first strategy to examine it) and diagrams are inherently lossy abstractions; the gap is real but the accompanying prose immediately below the diagram (`feedback-decision-logs-standards.md:50`) still correctly describes the evidence-link requirement, so a careful reader is not actually misled — only a reader who trusts the diagram in isolation.
**Consequence:** Minor — no data loss, no incorrect lint behavior (lint 3 checks only presence of evidence/reason on any terminal disposition, `DONE (standing...)` included, and would pass either way); purely a precision/fidelity gap in a brand-new visual aid.
**Evidence:** `projects/PROJ-031-cowork-skeleton/design/staging-feedback-logs/feedback-decision-logs-standards.md:36-48` (diagram); `projects/PROJ-031-cowork-skeleton/design/staging-feedback-logs/FEEDBACK-LOG.template.md:49` (the convention's own "standing" worked example, the majority pattern in real use).
**Dimension:** Internal Consistency (diagram vs. the convention's own demonstrated/recommended usage).
**Mitigation:** Optional (MAY, anti-bloat-compliant, no new machinery): add a one-line note under the diagram — "a `DONE (standing...)` entry is not dormant; it represents a continuously-applied directive and remains subject to the same evidence-link requirement" — or add a `DONE --> DONE : re-applied (standing)` self-loop to the diagram itself.
**Acceptance Criteria:** Either the diagram or its adjoining prose distinguishes "DONE (one-time, closed)" from "DONE (standing, continuously re-applied)" so a diagram-only reader is not misled.

### IN-003: Lint-1 Scope Drift Between Design Doc and Shipped Rule File [MINOR]

**Type:** Anti-Goal (cross-artifact wording precision)
**Original Assumption:** The design doc and the rule file describe "the same" lint 1 check identically.
**Inversion:** Design doc, `feedback-decision-log-convention-design.md:235`: "1. **Nav table present + cap not exceeded** — if `FEEDBACK-LOG.md` / `LLM-DECISION-LOG.md` exists and is > 30 lines it MUST have a nav table (already H-23, **scoped to the log filenames**)..." — this names only the two ACTIVE filenames. The shipped rule file, `feedback-decision-logs-standards.md:81`: "1. **Nav table + cap** — a `*-LOG.md` / **`*-LOG.NNN.md`** over 30 lines has a nav table (H-23)..." — this glob explicitly includes sealed numbered segments (`FEEDBACK-LOG.001.md`, etc.), which the design doc's version does not mention. An installer implementing lint 1 strictly from the design doc's wording would not apply the nav-table check to sealed segments; one implementing strictly from the rule file would. Since the rule file, not the design doc, is the artifact slated for `.context/rules/` installation (per the Adoption plan), the rule file's broader (and arguably more correct, since sealed segments are also markdown files subject to H-23) scope would govern in practice — but the two source-of-truth artifacts disagree on paper.
**Plausibility:** High that the drift exists (directly quoted); Low materiality (both readings satisfy H-23 for the primary files; only sealed-segment nav-table coverage is affected, and only after the first rotation, which has not yet occurred in this project).
**Consequence:** Minor — no loss of feedback/decision content; at most a sealed segment lacks a nav table until someone reconciles the wording, which is itself an H-23 cosmetic gap, not a data-integrity one.
**Evidence:** `projects/PROJ-031-cowork-skeleton/design/feedback-decision-log-convention-design.md:235`; `projects/PROJ-031-cowork-skeleton/design/staging-feedback-logs/feedback-decision-logs-standards.md:81`.
**Dimension:** Traceability (the two artifacts that are supposed to describe the same enforcement mechanism do not literally match).
**Mitigation:** Align the design doc's lint-1 bullet to the rule file's broader `*-LOG.md` / `*-LOG.NNN.md` scope (the rule file is the shipping artifact and the more defensible scope) — a one-clause wording fix, no new machinery.
**Acceptance Criteria:** Both artifacts name the same file-glob scope for lint 1.

---

## Refuted Critical Candidates (3-Lens Panel)

Per the VERIFIED-CRITICALS protocol, every candidate that looked Critical-caliber on first read was run through three lenses (factual / materiality / remediation-value) before filing. Two candidates were considered and **not filed**; documenting them satisfies P-022 (no deception by omission of the reasoning) and demonstrates the panel was actually applied, not skipped because nothing survived it.

| Candidate | Lens 1 (Factual) | Lens 2 (Materiality) | Lens 3 (Remediation-value) | Disposition |
|---|---|---|---|---|
| IN-001 (Segment-Index-overflow, above) considered at Critical | Pass — quote-verified | **Fail at Critical bar** — lint 2's actual job (id integrity, no lost/duplicated entries) is untouched; only a small table's own readability is at risk, at a scale (~10k entries) far beyond current usage | Pass — one-clause wording fix | **Filed as Major**, not Critical |
| "8 live entries carry no suffix" adoption-plan claim (design doc, Adoption step 4) — looked stale against the now-12-entry live `FEEDBACK-LOG.md` (FU.0–FU.11) on first read | **Fails at Lens 1** — direct inspection of the live log shows FU.5–FU.11 (7 entries) all already carry `(user label: X)` suffixes, handled by the document's separate "entries already carrying a `(user label: X)` suffix are renamed in place" clause; the "8 with no suffix" figure remains exactly correct for the FU.0–FU.4 + DEC-LLM-001..003 subset it describes | N/A (disqualified at Lens 1) | N/A (disqualified at Lens 1) | **Not filed** — self-refuted; initial read was wrong |
| Iteration-006's 6 Criticals (RT-001, DA-001/FM-006, PM-001/IN-001, PM-002, FM-001, FM-003) re-examined for regression | All 6 re-verified present/closed in current text (see Assumption Map A6/A7 and the direct quotes in [Summary](#summary)) | N/A | N/A | **Not filed** — confirmed closed, consistent with `restore-notes.md` |

No candidate in this pass reached Critical. This is consistent with, not contradictory to, the 6-round history: every prior Critical was closed and stayed closed (zero regressions, matching FU.11's own disposition note), and the package's substance has been independently affirmed sound by all 7 strategies across 6 rounds per the design doc's own changelog.

---

## Loss-Guarantee & Null-Alternative Analysis (directly asked)

**"What guarantees feedback gets lost — and does the package do it?"** Nothing in the current (v9, post-Restore) text of the 6 reviewed files unconditionally guarantees loss of a *captured and committed* entry. The package is honest that three distinct things are **not** guaranteed and remain MEDIUM-tier disciplines rather than mechanically enforced: (1) that a feedback-worthy turn is captured at all (Q5, no detector until the Q3 hook ships); (2) that a captured entry is committed before an uncommitted-loss event (`git checkout`/`reset`/`clean`) — the standing commit-cadence directive is the sole mitigation; (3) that a later session actually reads the logs (the read-side gap, install-action-gated). None of these three is new to this pass — all were found and disclosed across iterations 001–005 and remain accurately stated in current text (re-verified above). This pass's contribution is narrower and more surgical: one place (IN-001) where an *already-accepted, already-disclosed* residual (Segment-Index growing large) is given an inaccurate justification for why it is safe to leave unowned — the actual residual was already correctly identified as low-stakes in L1.4 (line 199, "the fallback is to move the Segment Index to its own sidecar... not built now"); only the *exemption's justification* at line 264 is wrong, not the underlying risk acceptance itself. Fixing IN-001 does not change what data can be lost; it corrects a citation.

**"Does it beat the null alternative (memory + transcripts)?"** The answer is unchanged from iteration-006's own honest assessment, independently re-verified here rather than merely copied forward: **partially, and the package says so itself.** Structure, disposition tracking, and the DEC/ADR boundary are a clear improvement over raw `MEMORY.md` + transcript-only capture. Session-start rediscoverability is **not yet** won — `project-workflow.md`'s "Before" orientation row (visible in this very session's loaded context) still lists only `PLAN.md`, `WORKTRACKER.md`, and `docs/knowledge/`, with no FEEDBACK-LOG/LLM-DECISION-LOG mention, exactly as the design doc's own Null-alternative note (line ~285) discloses ("planned-but-ratification-gated," not yet executed). Uncommitted-loss durability is honestly disclosed as *slightly worse* than `MEMORY.md` (which persists regardless of git state). Both gaps are named by the deliverable itself, not concealed — which is the correct posture for a MEDIUM-tier, install-gated convention, and is not itself a finding.

---

## Recommendations

**SHOULD mitigate (Major):**
- **IN-001-20260706-iter007:** Correct the Segment-Index-overflow exemption justification in `feedback-decision-log-convention-design.md:264` to state the actual (bounded) reason for exemption rather than an inaccurate lint-2-coverage claim. Acceptance: no remaining claim that lint 2 (or any named lint) detects Segment-Index row-count/overhead growth.

**MAY mitigate (Minor):**
- **IN-002-20260706-iter007:** Add a one-line clarifying note (or a self-loop) distinguishing "DONE (standing)" from "DONE (one-time)" adjacent to the new entry-lifecycle diagram.
- **IN-003-20260706-iter007:** Align the design doc's lint-1 file-glob scope (`FEEDBACK-LOG.md`/`LLM-DECISION-LOG.md` only) to the rule file's broader, shipping scope (`*-LOG.md`/`*-LOG.NNN.md`).

All three mitigations are wording-only; none requires new lint, files, fields, or subsystems, consistent with the package's own anti-bloat doctrine.

---

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Neutral | No goal or assumption category was left unstress-tested; the 6-round history already covers the dominant loss vectors exhaustively. |
| Internal Consistency | 0.20 | Negative (minor-scale) | IN-001: an exemption's stated justification does not match the cited control's actual scope. IN-002: a new diagram narrows a pattern the templates themselves demonstrate. |
| Methodological Rigor | 0.20 | Negative (minor-scale) | IN-001 repeats, in a new location, the exact verification gap (cite a control without checking its scope against the claimed risk) that iteration-006 closed elsewhere. |
| Evidence Quality | 0.15 | Neutral | All findings are precision/consistency gaps backed by direct quotes; no fabrication risk identified. |
| Actionability | 0.15 | Positive | All three findings have concrete, wording-only mitigations, and two Critical-looking candidates were explicitly tested and refuted with documented reasoning (not silently dropped). |
| Traceability | 0.10 | Negative (minor-scale) | IN-003: the design doc and the shipping rule file specify different scope for "the same" lint check. |

---

*Strategy Execution Statistics*
- **Total Findings:** 3
- **Critical:** 0
- **Major:** 1 (IN-001)
- **Minor:** 2 (IN-002, IN-003)
- **Refuted Critical Candidates:** 2 (documented above, not silently omitted)
- **Protocol Steps Completed:** 6 of 6 (goals stated, anti-goals inverted, assumptions mapped, stress-tested, mitigations developed, scoring impact synthesized)
- **Blind protocol:** No files under `orchestration/fu-log-convention-20260705-001/adversary/iteration-007/` or `iteration-008/` were read except this output file and `iteration-007/restore-notes.md` (explicitly permitted). Iteration-001 through iteration-006 `s-013-findings.md` disposition history was read. Permitted context read: design doc, all 5 staged artifacts, both live bootstrap logs (`FEEDBACK-LOG.md`, `LLM-DECISION-LOG.md`) for regression/verification evidence only (not treated as in-scope deliverables), `.context/rules/quality-enforcement.md` and `.context/rules/project-workflow.md` (already loaded in this session's context), and the S-013 strategy template.
- **Hygiene:** All 6 target deliverable files independently `grep`-verified clean of absolute host paths and employer-internal tokens (zero matches); this findings file uses repo-relative paths only.
