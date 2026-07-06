# Steelman Report: FEEDBACK-LOG + LLM-DECISION-LOG Jerry Convention (Iteration 7, VERIFIED-CRITICALS Protocol)

## Document Sections

| Section | Purpose |
|---------|---------|
| [Steelman Context](#steelman-context) | Deliverable, criticality, strategy metadata |
| [Summary](#summary) | Assessment, improvement count, recommendation |
| [Step 1: Charitable Interpretation](#step-1-charitable-interpretation) | Core thesis, strongest reading of the post-RESTORE package |
| [Step 2: Weakness Classification](#step-2-weakness-classification) | Presentation vs. substantive triage |
| [Steelman Reconstruction](#steelman-reconstruction) | Strengthened framing (adapted per CR-002) |
| [Step 4: Best Case Scenario](#step-4-best-case-scenario) | Ideal conditions, assumptions, confidence |
| [Improvement Findings Table](#improvement-findings-table) | SM-NNN findings, severity, dimension |
| [Improvement Details](#improvement-details) | Expanded rationale for the Major finding |
| [Verification Notes (P-022)](#verification-notes-p-022) | Spot-checks performed, what held up, what did not |
| [Scoring Impact](#scoring-impact) | Dimension-level effect of improvements |
| [Prior-Criticals Re-Verification](#prior-criticals-re-verification) | Independent confirmation of the 6 iteration-006 Criticals as closed |

---

## Steelman Context

- **Deliverable:** `projects/PROJ-031-cowork-skeleton/design/feedback-decision-log-convention-design.md` + `projects/PROJ-031-cowork-skeleton/design/staging-feedback-logs/{feedback-decision-logs-standards.md, FEEDBACK-LOG.template.md, LLM-DECISION-LOG.template.md, examples-appendix.md, hook-design-note.md}`
- **Deliverable Type:** Design (Jerry Framework convention proposal + staged rule/template artifacts)
- **Criticality Level:** C4 (Critical) — touches `.context/rules/` post-approval (AE-002/AE-003 auto-C3 minimum), gate 0.95
- **Strategy:** S-003 (Steelman Technique) — Iteration 7 (post-RESTORE pass, VERIFIED-CRITICALS protocol)
- **SSOT Reference:** `.context/rules/quality-enforcement.md`
- **Steelman By:** adv-executor (blind protocol: no iteration-007/008 adversary files read except `restore-notes.md`, which is the owner's public disposition record) | **Date:** 2026-07-06 | **Original Author:** ps-architect

---

## Summary

**Steelman Assessment:** The package's substance remains sound after six tournament rounds and the iteration-007 RESTORE pass: all 6 iteration-006 Criticals verify as closed in the current text (re-confirmed independently below, not merely trusted from `restore-notes.md`), and the two new FU.10 Mermaid diagrams are a genuine net improvement for a "yourself and the human operator" audience. However, the diagrams are also the **least-reviewed content in the entire package** — they did not exist during iterations 1-6, so no prior strategy pass has exercised them. A careful line-by-line check of the new `stateDiagram-v2` (shipped rule file, FEEDBACK-LOG section) against the rest of the package's own schema turns up one genuine, previously-undisclosed inconsistency: the diagram's entry point conflates the FEEDBACK-LOG disposition lifecycle with the LLM-DECISION-LOG entry lifecycle, which the rest of the package is explicit do **not** share a disposition model. This is a Major finding, not Critical — the surrounding prose text is still correct and the mechanism itself is undamaged; the fix is a diagram-only edit, not a design change. Two Minor presentation items in the new diagrams round out this report.

**Improvement Count:** 0 Critical, 1 Major, 2 Minor

**Original Strength:** High. The 6 iteration-006 Criticals independently re-verify as closed against current text (see [Prior-Criticals Re-Verification](#prior-criticals-re-verification)). No `MUST`-tier language leakage, no absolute home-directory paths, and no employer-internal tokens were found anywhere in the 6-file package (independently grepped, not merely trusted from `restore-notes.md`).

**Recommendation:** Fix SM-001 (diagram scope conflation) before this package proceeds past a VERIFIED-CRITICALS gate that specifically targets fresh/unreviewed content — it is cheap (a label/edge edit, zero new machinery) and closes the one genuine gap this pass found. SM-002/SM-003 are optional polish. No Critical blocks the convention's purpose (feedback/decisions never lost, operator-burden-free capture, navigable growth, honest metadata) in the reviewed package as it currently stands.

---

## Step 1: Charitable Interpretation

**Core thesis (most charitable reading):** the package commissioned by the user (FU.2) asks for two lightweight, append-only ledgers so that feedback and human/LLM decisions survive context compaction and session boundaries, without recreating the sibling ADR-convention's over-engineering failure. Six tournament rounds already converged on this being the correct minimum-viable answer for a MEDIUM-tier convention under a 25/25 HARD-rule ceiling; iteration-006's own S-003 pass (`orchestration/fu-log-convention-20260705-001/adversary/iteration-006/s-003-findings.md`) found **zero** Critical findings and only presentational/structural Majors, which the RESTORE pass then closed (Quick-Path pointer, finding-code legend, changelog separation banner — all independently confirmed present in the current design doc).

The iteration-007 RESTORE pass had a narrow, well-scoped mandate per `restore-notes.md`: (1) re-verify the 6 iteration-006 Criticals are closed, (2) add exactly two Mermaid diagrams that *replace* equivalent prose (user-requested, FU.10), (3) hygiene. This is a disciplined, minimal-surface-area change — precisely the anti-bloat posture the package has maintained throughout. Under a charitable reading, this pass earns the benefit of the doubt that it did not reintroduce old defect classes.

**Strengthening opportunity noted for Step 2:** a diagram is new, unreviewed content by construction — none of iterations 1-6 could have caught a defect in an artifact that did not exist until iteration 7. The correct adversarial posture toward *new* content in an otherwise heavily-converged package is not "trust the pattern of prior clean rounds" but "verify the new artifact against the same rigor the rest of the package received." That verification is what this pass focuses on.

---

## Step 2: Weakness Classification

| Weakness | Type | Magnitude | Strongest Intended Reading |
|----------|------|-----------|------------------------------|
| The new entry-lifecycle `stateDiagram-v2` (rule file FEEDBACK-LOG section) opens with a transition labeled "chat feedback or inline FU/DEC marker" leading into a single OPEN/IN-PROGRESS/DONE/WONTFIX chain, but LLM-DECISION-LOG entries have no Disposition field anywhere in the package (they use `Reflected in` / `Superseded by` instead) | Structural (diagram-schema mismatch) | Major | Author intended the diagram to illustrate FEEDBACK-LOG's lifecycle specifically (it sits directly under the `## FEEDBACK-LOG` heading, right after the FU.N schema description) and reused "FU/DEC marker" loosely to mean "either inline-marker type can trigger a capture," not to claim DEC-LLM entries share this disposition state machine — the omission is a scoping label, not a design substance change |
| Diagram state `IN_PROGRESS` (underscore, no display-label override) renders literally, while every other occurrence of this enum value in the same file (and the design doc, both templates, and the appendix) uses `IN-PROGRESS` (hyphen) | Presentation (Mermaid syntax artifact) | Minor | Mermaid state identifiers cannot contain a bare hyphen without a display-label override (`IN_PROGRESS : IN-PROGRESS`); the author almost certainly intended the hyphenated form and simply omitted the override — a one-line fix |
| The new segment-rotation `flowchart` shows one directional cross-log edge (`FEEDBACK-LOG --Related: DEC-LLM-012--> LLM-DECISION-LOG`), while the package's actual mechanism supports citation in either direction (a DEC-LLM entry's Context line can equally carry `Related: FU.N`, per `LLM-DECISION-LOG.template.md:25`) | Presentation (diagram completeness) | Minor | The single arrow is illustrative of the *mechanism* (id-based resolution, no path needed), not a claim that citation is one-directional; the prose elsewhere is unambiguous that it is symmetric |

No **substantive** weakness (an idea the reviewer would refer to S-002/S-004 as a defect in the design's core mechanism) was identified. All three items above are presentation/structural gaps in freshly-added diagram content, closable without touching the ledger mechanism, the rule count, or the lint count.

---

## Steelman Reconstruction

> **Adaptation notice (CR-002-style, per Section 5's provision for legitimate strategy-specific adaptation):** consistent with iteration-006's precedent, reproducing the full six-file package "rewritten in strongest form" would itself be an anti-bloat violation the package's own doctrine would reject. The reconstruction below is the form the findings actually require: a targeted diagram patch closing the one Major gap, plus two optional Minor polish patches.

**Patch A — Scope the diagram's entry edge (closes SM-001).** In `projects/PROJ-031-cowork-skeleton/design/staging-feedback-logs/feedback-decision-logs-standards.md`, the `stateDiagram-v2` block (rule file lines 36-48):

Change:
```
    [*] --> Captured: chat feedback or inline FU/DEC marker
```
to:
```
    [*] --> Captured: chat feedback or inline FU marker
```
and add one clause to the sentence immediately preceding the diagram (rule file line 34, "Entry lifecycle (capture → logged → disposition):") — e.g. "Entry lifecycle for FEEDBACK-LOG entries (capture → logged → disposition); LLM-DECISION-LOG entries do not carry a Disposition field and instead use `Reflected in` / `Superseded by` (see LLM-DECISION-LOG section below)."

This is a label edit plus one clarifying clause — it repeats no new claim, adds no mechanism, does not touch the ≤3-lint or LOG-M-00x rule count, and does not change which markers (`FU:`/`DEC:`) exist as capture triggers (both remain valid per LOG-M-001's capture-trigger list; the fix only removes the false implication that a `DEC:` marker feeds this specific disposition state machine).

**Patch B — Diagram label override (closes SM-002, optional).** Change the two `IN_PROGRESS` occurrences to carry a display override: `IN_PROGRESS : IN-PROGRESS` (Mermaid syntax for a display label distinct from the state id), or rename the internal state id itself if the rendering pipeline supports hyphens via quoting. Either way, the rendered diagram then reads `IN-PROGRESS`, consistent with every other reference in the package.

**Patch C — Bidirectional cross-log note (closes SM-003, optional).** Add a one-clause note under the flowchart caption (design doc, after line 191): "(citation is symmetric — a DEC-LLM entry may equally carry `Related: FU.N`; one direction is shown for brevity)."

---

## Step 4: Best Case Scenario

**Ideal conditions under which this design (with Patch A applied) is strongest:** the same conditions iteration-006's Steelman already identified — a single operator, one continuously-mediating assistant session per project, disciplined milestone-cadence commits, MEDIUM-tier enforcement accepted as correct given the documented 25/25 ceiling. Patch A additionally requires nothing beyond the existing "diagram is a presentation of existing rules, not machinery" principle already used to justify FU.10 itself — applying the same principle to fix the diagram is fully consistent with how the RESTORE pass justified adding it.

**Key assumptions that must hold:** (1) the diagram is consulted by the assistant/operator as a fast-orientation aid, precisely per its own stated purpose (`restore-notes.md` FU.10 motivation: "massive walls of text") — meaning a reader who trusts the diagram over the surrounding prose is a realistic, not a hypothetical, reader; (2) the fix does not need to wait for a future round, since it requires no new lint/file/field/subsystem and is a strict subset of the RESTORE pass's own "diagram-only, prose-replacing" change class.

**Confidence assessment:** HIGH that the mechanism design (ledgers, ids, rotation, lint) remains correct and Critical-free. MODERATE-HIGH confidence that, absent Patch A, an assistant relying on the diagram in a future session could genuinely attempt to write a `Disposition:` field on an LLM-DECISION-LOG entry or expect one to be present — this is the one place in the reviewed package where the "strongest form" (all six files internally consistent) and the "current form" (one new diagram not yet cross-checked against the rest) diverge.

---

## Improvement Findings Table

| ID | Description | Severity | Original | Strengthened | Dimension |
|----|--------------|----------|----------|---------------|-----------|
| SM-001-iter7-20260706 | FU.10 entry-lifecycle diagram's initial transition names both `FU`/`DEC` markers as triggers into an OPEN/IN-PROGRESS/DONE/WONTFIX chain that only FEEDBACK-LOG entries actually have | Major | `feedback-decision-logs-standards.md:38` ("chat feedback or inline FU/DEC marker") vs. `feedback-decision-logs-standards.md:55-61` (LLM-DECISION-LOG schema: no Disposition field) and `LLM-DECISION-LOG.template.md:17-28` (same) | Patch A: scope the edge to "FU marker" only + one clarifying clause distinguishing the two logs' lifecycle models | Internal Consistency |
| SM-002-iter7-20260706 | Diagram renders `IN_PROGRESS` (underscore); every other occurrence of the value in the package uses `IN-PROGRESS` (hyphen) | Minor | `feedback-decision-logs-standards.md:41,44,45` vs. `feedback-decision-logs-standards.md:50` ("`OPEN / IN-PROGRESS / DONE / WONTFIX`") | Patch B: Mermaid display-label override | Evidence Quality |
| SM-003-iter7-20260706 | New segment-rotation flowchart shows a one-directional cross-log arrow; the mechanism is bidirectional | Minor | `feedback-decision-log-convention-design.md:190` (`A ==>|"Related: DEC-LLM-012..."| D`) vs. `LLM-DECISION-LOG.template.md:25` ("A cross-log citation to the FEEDBACK-LOG renders as a labeled `Related: FU.N`") | Patch C: one-clause symmetry note | Completeness |

**Finding ID Format:** `SM-{NNN}-{execution_id}` where `execution_id = iter7-20260706` (iteration 7, this session).

---

## Improvement Details

### SM-001-iter7-20260706 — Diagram Lifecycle Scope Conflation

- **Affected Dimension:** Internal Consistency
- **Original Content:** `feedback-decision-logs-standards.md` line 34 introduces the diagram as "Entry lifecycle (capture → logged → disposition)" directly under the `## FEEDBACK-LOG` heading (line 30). Line 38 of the diagram reads `[*] --> Captured: chat feedback or inline FU/DEC marker`, and the chain proceeds `Captured --> Logged --> OPEN --> {IN_PROGRESS, DONE, WONTFIX}`. Nothing in the diagram or its two surrounding sentences marks a branch point where a `DEC:`-triggered capture diverges from this chain. Cross-checked against the LLM-DECISION-LOG schema (same file, lines 55-61; also `feedback-decision-log-convention-design.md` L1.2 entry-schema table; also `LLM-DECISION-LOG.template.md:17-28`): the DEC-LLM-NNN entry fields are Decision / User verbatim / Assistant verbatim / Summary-consequences / Context, with lifecycle expressed only via `Reflected in` (graduation) and `Superseded by` (reversal) — no `OPEN`/`IN-PROGRESS`/`DONE`/`WONTFIX` enum exists for this entry type anywhere in the package.
- **Strengthened Content:** Patch A above — narrow the diagram's entry edge to name only the FU marker, and add one clause distinguishing the two logs' lifecycle models in the preceding sentence.
- **Rationale:** This is the single genuinely new (not previously disclosed, not previously reviewable) finding in this pass: the diagram did not exist in iterations 1-6, so no prior strategy execution — including iteration-006's own S-003 pass, which found zero Criticals — could have caught it. The design's own philosophy motivating FU.10 ("for yourself and the human operator," per `restore-notes.md` line 33) makes this a live risk rather than a theoretical one: an assistant orienting itself from the diagram (its explicit purpose) rather than re-deriving the full LLM-DECISION-LOG schema from prose could genuinely attempt to write or expect a Disposition field on a DEC-LLM entry, producing exactly the kind of metadata drift the rest of this heavily-hardened package works hard to prevent. It does not, however, invalidate the ledger mechanism, alter a rule, or require new machinery to fix — hence Major, not Critical.
- **Best Case Conditions:** Maximally valuable before the first live session that consults this rule file post-install; degrades gracefully (costs nothing) for a reader who cross-checks the diagram against the full LLM-DECISION-LOG section anyway.

---

## Verification Notes (P-022)

Spot-checks performed against source files (scoped to plausible fresh-content risk given the RESTORE pass's narrow diagram/hygiene mandate):

| Claim checked | Verified against | Result |
|---|---|---|
| LLM-DECISION-LOG entries have no Disposition field | `feedback-decision-logs-standards.md:55-61`; `feedback-decision-log-convention-design.md` L1.2 entry-schema table; `LLM-DECISION-LOG.template.md:17-28` | **Confirmed absent** in all three independent schema statements — the diagram's implied shared lifecycle does not match any of them |
| `IN_PROGRESS` vs `IN-PROGRESS` spelling | `feedback-decision-logs-standards.md:41,44,45` (diagram) vs. `:50` (prose enum) | **Confirmed mismatch**, verified via direct grep, not just visual read |
| Cross-log citation is bidirectional in the actual mechanism | `LLM-DECISION-LOG.template.md:25` ("A cross-log citation to the FEEDBACK-LOG renders as a labeled `Related: FU.N`") | **Confirmed** — the new flowchart's single-direction example does not itself claim otherwise, but does not show it either |
| No `MUST`-tier language leakage in the 6-file package | Grep for `MUST` across `feedback-decision-log-convention-design.md` + `staging-feedback-logs/*.md` | **Zero matches** — tier discipline holds |
| No absolute home-directory paths in the 6-file package | Grep for `/Users/`, `/home/`, `C:\\` across the same scope | **Zero matches** — independently confirmed, not merely trusted from `restore-notes.md` |
| No employer-internal name tokens (e.g. `[employer]`/`[employer-predecessor-A]`/`[employer-predecessor-B]`) in the 6-file package | Grep across the same scope | **Zero matches** |
| Mermaid syntax validity of both new diagrams | Manual parse of `flowchart LR` (design doc L1.4) and `stateDiagram-v2` (rule file) blocks | **Both syntactically well-formed** — no rendering-breaking errors found beyond the SM-002 label mismatch |
| Segment-cap arithmetic shown in the new flowchart (`FU.0–FU.49` = 50, `FU.50–FU.99` = 50) | `feedback-decision-log-convention-design.md:184-186` vs. the "~50 entries or ~800 lines" cap stated in L1.4/LOG-M-006 | **Consistent** — matches the stated cap |

No claim spot-checked here was found to overclaim coverage beyond what the package actually delivers or explicitly defers, **except** the diagram lifecycle-scope issue documented as SM-001.

---

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Neutral | Mechanism coverage already thorough; SM-003 is a minor diagram-completeness nit, not a coverage gap |
| Internal Consistency | 0.20 | Positive | SM-001 fix removes the one genuine schema/diagram mismatch found in the fresh content |
| Methodological Rigor | 0.20 | Neutral | Charitable interpretation applied; presentation/substance distinction maintained throughout |
| Evidence Quality | 0.15 | Positive (Minor) | SM-002 fix keeps the diagram's rendered text consistent with every other citation of the same enum value |
| Actionability | 0.15 | Positive | All three patches are directly incorporable, zero-mechanism, diagram-only edits |
| Traceability | 0.10 | Neutral | No traceability gap found in this pass (iteration-006's SM-002 legend already closed the prior traceability gap) |

---

## Prior-Criticals Re-Verification

Independent re-confirmation (not merely trusted from `restore-notes.md`) that the 6 iteration-006 Criticals are closed in the current deliverable text:

| # | Iteration-006 Critical | Independently re-checked at | Status |
|---|------------------------|------------------------------|--------|
| 1 | RT-001 (redaction carve-out could launder tampering) | `feedback-decision-logs-standards.md:24` — names category + approximate size, "presence not veracity" scrutiny signal | **Confirmed closed** |
| 2 | DA-001/FM-006 ("Four" safety functions undercounts a fifth) | `feedback-decision-log-convention-design.md:264` — reads "**Five** safety functions," lists all five, names the Segment-Index-overflow exemption | **Confirmed closed** |
| 3 | PM-001/IN-001 (AE-006e false cap-crossing backstop claim) | `feedback-decision-logs-standards.md:28` and `feedback-decision-log-convention-design.md:195` — both state AE-006e fires on compaction only, no cumulative-size backstop exists | **Confirmed closed** |
| 4 | PM-002 (unfilled `~N sessions` placeholder) | `feedback-decision-log-convention-design.md:260` — concrete "~3 sessions or 30 days ... or the next milestone checkpoint" | **Confirmed closed** |
| 5 | FM-001 (no inline-doc harvest dedup) | `feedback-decision-logs-standards.md:51` and `FEEDBACK-LOG.template.md:25` — check-before-mint against existing `source: inline-doc path:line/anchor` | **Confirmed closed** |
| 6 | FM-003 ("verbatim and full" contradicted split-entry practice) | `feedback-decision-logs-standards.md:24` — multi-item message MAY split into per-item entries, split noted in Summary | **Confirmed closed** |

All 6 independently re-verify as closed. No regression found on any of the 6 across this pass's review.

---

## Execution Statistics

- **Total Findings:** 3
- **Critical:** 0
- **Major:** 1
- **Minor:** 2
- **Protocol Steps Completed:** 6 of 6

---

*Strategy: S-003 (Steelman Technique) | Template: `.context/templates/adversarial/s-003-steelman.md` v1.0.0*
*Iteration: 007 (VERIFIED-CRITICALS protocol, post-RESTORE) | Executed: 2026-07-06*
