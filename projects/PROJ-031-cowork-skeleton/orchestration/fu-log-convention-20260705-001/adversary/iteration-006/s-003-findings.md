# Steelman Report: FEEDBACK-LOG + LLM-DECISION-LOG Jerry Convention

## Document Sections

| Section | Purpose |
|---------|---------|
| [Steelman Context](#steelman-context) | Deliverable, criticality, strategy metadata |
| [Summary](#summary) | Assessment, improvement count, recommendation |
| [Step 1: Charitable Interpretation](#step-1-charitable-interpretation) | Core thesis, strongest reading |
| [Step 2: Weakness Classification](#step-2-weakness-classification) | Presentation vs. substantive triage |
| [Steelman Reconstruction](#steelman-reconstruction) | Strengthened framing (adapted per CR-002) |
| [Step 4: Best Case Scenario](#step-4-best-case-scenario) | Ideal conditions, assumptions, confidence |
| [Improvement Findings Table](#improvement-findings-table) | SM-NNN findings, severity, dimension |
| [Improvement Details](#improvement-details) | Expanded rationale per Major finding |
| [Verification Notes (P-022)](#verification-notes-p-022) | Spot-checks performed, what held up |
| [Scoring Impact](#scoring-impact) | Dimension-level effect of improvements |
| [Out-of-Scope Observation](#out-of-scope-observation) | Disclosed, non-findings item |

---

## Steelman Context

- **Deliverable:** `projects/PROJ-031-cowork-skeleton/design/feedback-decision-log-convention-design.md` + `projects/PROJ-031-cowork-skeleton/design/staging-feedback-logs/{feedback-decision-logs-standards.md, FEEDBACK-LOG.template.md, LLM-DECISION-LOG.template.md, examples-appendix.md, hook-design-note.md}`
- **Deliverable Type:** Design (Jerry Framework convention proposal + staged rule/template artifacts)
- **Criticality Level:** C4 (Critical) — touches `.context/rules/` post-approval (AE-002/AE-003 auto-C3 minimum), engagement gate 0.95
- **Strategy:** S-003 (Steelman Technique) — Iteration 6
- **SSOT Reference:** `.context/rules/quality-enforcement.md`
- **Steelman By:** adv-executor (blind, no prior-iteration adversary files read per BLIND PROTOCOL) | **Date:** 2026-07-06 | **Original Author:** ps-architect (per package's own attribution)

---

## Summary

**Steelman Assessment:** The design's *substance* — two lightweight, append-only, git-backstopped markdown ledgers with logger-assigned monotonic ids, verbatim operator aliases, capped-segment rotation, ≤3 pure-text L5 lint checks, and five explicitly-ratifiable PROPOSED-DEFAULTs — is sound, well-evidenced against this project's own artifacts, and correctly disciplined against the HARD-rule ceiling and the sibling ADR-convention's over-engineering failure. Under a charitable, evidence-checked reading, **no Critical overclaimed-coverage gap survives** in the reviewed package. The improvement opportunities that do survive are entirely presentational/structural: the package's meta-narrative (round-by-round remediation changelog, opaque cross-strategy finding-code citations) has grown to the point that it competes with, and partially obscures, the ratification-critical content it exists to support — an irony given the package's own anti-bloat doctrine.

**Improvement Count:** 0 Critical, 2 Major, 3 Minor

**Original Strength:** High. Verified against source evidence (see [Verification Notes](#verification-notes-p-022)): the "8 of 13 live entries carry no alias suffix" claim, the Q1 token-math, the 800-line/2,000-line-window ratio, the "Added" column parity claim, and the "not a guarantee" hedging in both templates all check out against the actual files. No `MUST`-tier language leakage was found in the staged artifacts. No absolute paths or employer-internal references were found in the reviewed package.

**Recommendation:** Incorporate the two Major (structural/traceability) improvements below via **reorganization only** (moving/labeling existing content) — consistent with the anti-bloat doctrine the package already applies to itself. Do **not** add further disclosure prose in response to this report; the substantive content is already stable and well-hedged. Proceed to downstream critique strategies (S-002, S-004, S-001) treating the *substance* as a fair target and the *presentation* as the strongest-form gap this Steelman pass identifies.

---

## Step 1: Charitable Interpretation

**Core thesis (most charitable reading):** Jerry currently has an emergent, un-codified, employer-internal pattern (`[internal-kb]`) for capturing user feedback and human↔LLM decisions that (a) was never shipped as a real convention, (b) drifted into an observed id collision (`DJ-NNN` scheme), and (c) has no segment-rotation answer to the fact that append-only logs eventually exceed an LLM's read window. The design commissioned by the user (FU.2, verbatim, `FEEDBACK-LOG.md:57-63`) asks for exactly two things: a Feedback/Follow-Up log and an LLM Decision Log, built via Jerry skills/agents and background agents "so that we don't burn through the main context window." The design responds with the minimum viable codification: one MEDIUM-tier rule file (six rules, `LOG-M-001..006`), two templates with embedded worked examples, one examples appendix, one design-only (not-shipped) hook note, and — critically — it does **not** invent new HARD rules, new enforcement subsystems, or a new lint category beyond three cheap, pure-text checks. This is a textbook-correct MEDIUM-tier response to a HARD-rule ceiling that is documented elsewhere in this same repository as full at 25/25 with zero headroom (`.context/rules/quality-enforcement.md` HARD Rule Ceiling Derivation section).

The design is explicit that it learned this discipline empirically: it cites its own sibling effort (the ADR-identifier-convention orchestration, same project, `PROJ-031`) which spiraled to an ~30k-token rule draft and an 18-rule lint before being subtractively remediated back down — and the feedback-log design repeatedly invokes that precedent as the reason to hold the line at "≤3 lint, one new rule per genuinely new mechanism, examples pushed to an appendix." That is a strong, self-aware piece of engineering judgment, not merely an assertion: the same project actually lived the failure mode being avoided.

**Strengthening opportunities noted for Step 2 (not failures):** the document's honesty about its own residual risks (concurrent-writer races, silent non-capture, uncommitted-loss exposure, discovery-cost at scale) is a strength for engineering trust, but the sheer volume of disclosure prose accumulated defending against five prior adversarial rounds has begun to work against the reader's ability to locate the actually-ratifiable decision points (Q1-Q5). That is a presentation opportunity, addressed below.

---

## Step 2: Weakness Classification

| Weakness | Type | Magnitude | Strongest Intended Reading |
|----------|------|-----------|------------------------------|
| Q1-Q5 ratification table sits ~270 lines into the design doc, after dense L1/L2 mechanism prose | Presentation/Structural | Major | Author intends the user to ratify "each of Q1–Q5 individually" (Adoption step 1); the content is present and correct, just positioned for a linear read rather than a ratification workflow |
| Cross-strategy finding-code citations (`SM-003 class`, `CV-001/003/004`, `PM-005`, etc.) appear inline throughout L1/L2/changelog with no legend and, for a blind reviewer, no resolvable source | Traceability | Major | Author is using these as internal shorthand for a real, evidenced remediation history (verified: `Full trace:` paths are given per changelog round) — the codes are not fabricated, just undocumented as a convention |
| Revision Changelog (v1-v7) is now denser, in raw prose volume, than the L1 design content it documents, and is not visually separated from "current, ratifiable state" | Presentation/Structural | Minor-Major (see SM-003) | This is process transparency (P-022) executed diligently, not padding — the fix is separation, not deletion |
| Rule-file word/token count has been re-measured every round with a differently-derived number (1,120 words -> ~2,150 tokens -> ~1,425 words -> ~1,791 words) narrated across several paragraphs rather than tabulated | Evidence/Presentation | Minor | The underlying honesty (P-022, "re-count at ratification, don't trust this estimate") is exactly right; only the presentation of the trend is diffuse |
| Adoption step 4's precise 8-of-13 alias-normalization instruction is expressed as prose-with-counts rather than an explicit per-id table | Actionability | Minor | The count is independently verified correct (see below) — this is a legibility polish, not a defect |

No **substantive** weakness (an idea the reviewer would refer to S-002/S-004 as a defect in the design's core mechanism) was identified that survives the charitable read and the spot-checks below.

---

## Steelman Reconstruction

> **Adaptation notice (CR-002-style, applied within Section 5's provision for legitimate strategy-specific adaptation):** the reviewed package spans six files and ~340+75+66+67+173+57 lines. Reproducing the entire package "rewritten in strongest form" would itself be a bloat action the package's own anti-bloat doctrine would reject, and none of the identified gaps are substantive (nothing here needs a sentence-level rewrite of the mechanism). The reconstruction below therefore takes the form the improvements themselves require: two concrete, drop-in patches (reorder/label only, zero new claims) that a subtraction-style revision could apply verbatim.

**Patch A — Ratification Quick-Path (closes SM-001).** Insert immediately after the L0 Executive Summary, before "L1: Full Design":

> **Quick-Path to Ratification.** This design proceeds provisionally on five PROPOSED-DEFAULTs (Q1-Q5, full detail and rationale in [Proposed Defaults](#proposed-defaults-pending-ratification)). To ratify, confirm or override each: **Q1** (assistant-verbatim = excerpt+pointer, not full paste), **Q2** (`scope: framework` tag, not always-repo-root), **Q3** (hook designed now, shipped later), **Q4** (backfill supported, execution gated), **Q5** (accept the no-detector residual as disclosed, not built now). Everything else in this document is supporting rationale and process history.

This is a pure pointer/label addition — it repeats no new claim, adds no mechanism, and does not touch the ≤3-lint or LOG-M-00x rule count.

**Patch B — Finding-code legend (closes SM-002).** Insert one line at the top of the Revision Changelog:

> **Finding-code legend:** `SM`=Steelman(S-003) · `DA`=Devil's Advocate(S-002) · `PM`=Pre-Mortem(S-004) · `CC`=Constitutional AI(S-007) · `CV`=Chain-of-Verification(S-011) · `FM`=FMEA(S-012) · `IN`=Inversion(S-013) · `RT`=Red Team(S-001) · `SR`=Self-Refine(S-010). Full reports: `orchestration/fu-log-convention-20260705-001/adversary/iteration-{NNN}/`.

This converts an opaque internal shorthand into a self-contained reference in one line, again zero new substantive claims.

---

## Step 4: Best Case Scenario

**Ideal conditions under which this design is strongest:** a single operator, one continuously-mediating assistant session per project, disciplined milestone-cadence commits, and a willingness to accept MEDIUM-tier (not HARD-tier) enforcement as the correct answer given the documented 25/25 ceiling. Under those conditions — which match this project's own actual operating profile, per the bootstrap `FEEDBACK-LOG.md`/`LLM-DECISION-LOG.md` evidence reviewed — the design closes the specific, real failure the user asked it to close (FU.2: "so that we don't lose feedback or follow up items") without re-creating the sibling ADR-convention's over-engineering failure.

**Key assumptions that must hold:** (1) the operator does not run concurrent sessions/windows against the same log (disclosed, named, accepted); (2) the commit-cadence checkpoint is not skipped indefinitely (disclosed single point of correlated failure, with calendar-capped backstops); (3) the Q3 hook eventually ships, or the MEDIUM/SHOULD discipline is judged sufficient indefinitely.

**Confidence assessment:** HIGH that the mechanism design is correct for the stated scope (single-operator, MEDIUM-tier convention). MODERATE-HIGH that the document, in its *current organizational form*, will read as ratifiable-in-one-pass by the user without the Quick-Path reorganization in Patch A — this is the one place where "strongest form" and "current form" genuinely diverge.

---

## Improvement Findings Table

| ID | Description | Severity | Original | Strengthened | Dimension |
|----|--------------|----------|----------|---------------|-----------|
| SM-001-iter6-20260706 | Q1-Q5 ratification table buried ~270 lines into the doc | Major | Design doc structured as one linear narrative; Proposed Defaults appear after full L1/L2 mechanism detail (`feedback-decision-log-convention-design.md:273-285`) | Add "Quick-Path to Ratification" pointer directly after L0 (Patch A) | Actionability |
| SM-002-iter6-20260706 | Adversarial finding-codes (SM/DA/PM/CC/CV/FM/IN/RT/SR-NNN) used inline with no legend | Major | Codes appear ~60+ times across L1/L2/Changelog with no decode key (e.g. `feedback-decision-log-convention-design.md:206`, `:246`, `:327-331`) | Add one-line legend + path convention at top of Revision Changelog (Patch B) | Traceability |
| SM-003-iter6-20260706 | Process-history prose (Changelog v1-v7) not visually separated from current-state design content | Minor | Both live in one undifferentiated document body (`feedback-decision-log-convention-design.md:321-331`) | Add an explicit `---` + "History (informational, not part of the ratifiable design)" banner above the Changelog | Internal Consistency |
| SM-004-iter6-20260706 | Rule-file token-count trend narrated in prose across 5 rounds rather than tabulated | Minor | Counts appear scattered in L2 prose and in Changelog rows (`:206`, `:326-331`) | Optional 5-row micro-table: round, measured words, measured/estimated tokens, delta rationale | Evidence Quality |
| SM-005-iter6-20260706 | Adoption step 4's verified-correct 8-of-13 alias-normalization instruction is prose-only | Minor | `feedback-decision-log-convention-design.md:239` | Optional per-id table (id, current suffix, target suffix) for the installer | Actionability |

**Finding ID Format:** `SM-{NNN}-{execution_id}` where `execution_id = iter6-20260706` (iteration 6, this session).

---

## Improvement Details

### SM-001-iter6-20260706 — Ratification Quick-Path

- **Affected Dimension:** Actionability
- **Original Content:** The design doc's Navigation table (`feedback-decision-log-convention-design.md:8-24`) lists "Proposed Defaults" as one of eleven linked sections, indistinguishable in prominence from "L1.3 Automation" or "Improvement Ledger." The Adoption plan (line 236) asks the user to ratify "each of Q1-Q5 individually," but nothing in the document's structure signals, before a full read, that this is the single action the user must take.
- **Strengthened Content:** Patch A (above) — a 4-sentence pointer block placed immediately after L0.
- **Rationale:** This is the single highest-leverage, lowest-cost change identifiable: it does not alter a single design decision, add a rule, or touch the rule file/lint/template artifacts that will actually ship. It only changes how a human finds the five decisions they are being asked to make. Consistent with the package's own repeatedly-stated anti-bloat doctrine ("close findings by simplifying, never by adding machinery") applied to the design doc's own structure, not just its rule content.
- **Best Case Conditions:** Maximally valuable if the user ratifies Q1-Q5 in a single sitting without re-reading the full L1/L2 body; degrades gracefully (costs nothing) if they read linearly anyway.

### SM-002-iter6-20260706 — Finding-Code Legend

- **Affected Dimension:** Traceability
- **Original Content:** Citations such as "the driver each round has been the same class of gap... (SM-002/CV-003/FM-008 and this pass)" (`:246`) and "closes DA-001/RT-001/PM-001/FM-001/IN-001" (`:328`) assume the reader already knows the `/adversary` skill's per-strategy prefix convention (documented in `.context/templates/adversarial/s-00N-*.md` Section 1 Identity tables, e.g. `SM-NNN` for S-003, `DA-NNN` for S-002). A reader of only this design package — including, per this iteration's BLIND PROTOCOL, this reviewer — cannot resolve an individual code to its source report without independently knowing that convention.
- **Strengthened Content:** Patch B (above) — one legend line, reusing the "Full trace: `orchestration/.../iteration-00N/remediation-notes.md`" pattern already present per changelog round (a genuinely good existing practice that should be generalized, not replaced).
- **Rationale:** The underlying evidence is real and traceable (verified: each Revision Changelog row already ends with a "Full trace:" path); what's missing is the one-time decode key that makes the whole citation apparatus self-contained for a reader who lands on this file without adversary-skill context (e.g., a future engineer, an auditor, or — as in this iteration — a blind-protocol reviewer).
- **Best Case Conditions:** Strongest when this document outlives the current session/tournament and is read by someone without live access to (or memory of) the five prior iteration folders.

---

## Verification Notes (P-022)

Spot-checks performed against source files (not exhaustive; scoped to plausible overclaim candidates given the "overclaimed coverage is Critical" framing for this pass):

| Claim checked | Verified against | Result |
|---|---|---|
| "8 of 13 live entries... currently carry no suffix" (`design doc:239`) | `FEEDBACK-LOG.md` FU.0-FU.9 + `LLM-DECISION-LOG.md` DEC-LLM-001-003 | **Confirmed exact**: FU.0-FU.4 (5) + DEC-LLM-001-003 (3) = 8 with no suffix; FU.5-FU.9 (5) carry `(user label: ...)` — matches the doc's disclosed plan to rename these at install |
| "the two live Backfill tables now carry the Added column" (`:239`) | `FEEDBACK-LOG.md:165`, `LLM-DECISION-LOG.md:77` | **Confirmed**: both tables have an `Added` column |
| Q1 size math (~0.3M-1.5M tokens full-paste vs ~15k-40k excerpt, 100 decisions) | `design doc:120-125` | **Arithmetic checks out** (100×3k-15k and 100×150-400) |
| 800-line cap vs. 2,000-line Read window / ~25k-token truncation | `design doc:180` | **Ratios check out** (800/2000=40%, 2000/800=2.5×; 25k/8-12k ≈ 2-3×) |
| Templates state capture is "not a guarantee" | `FEEDBACK-LOG.template.md:3`, `LLM-DECISION-LOG.template.md:3` | **Confirmed present** in both |
| No `MUST`-tier language leakage in staged rule/template artifacts | grep across `staging-feedback-logs/` | **Zero matches** — tier discipline holds |
| No absolute home-directory paths or employer-internal tokens in the reviewed package | grep across `design/` scope of this package | **Zero matches** in the design doc + staging files reviewed |
| Read-side gap ("survive sessions" = bytes-persist only, not auto-consulted) | `design doc:228, 238`; cross-checked against `.context/rules/project-workflow.md` Workflow Phases table (no FEEDBACK-LOG/LLM-DECISION-LOG reference yet) | **Confirmed consistent** — the gap is real, disclosed, and its closure is explicitly sequenced as an Adoption-step-3 install action, not silently assumed done |

No claim spot-checked here was found to overclaim coverage beyond what the package actually delivers or explicitly defers.

---

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Neutral | Mechanism coverage already thorough after 5 remediation rounds; no coverage gap found |
| Internal Consistency | 0.20 | Positive | SM-003 separation reduces the risk that process-history prose is mistaken for live design content |
| Methodological Rigor | 0.20 | Neutral | Charitable interpretation applied; presentation/substance distinction maintained throughout |
| Evidence Quality | 0.15 | Positive (Minor) | SM-004 tabulation would make the already-honest token-count trend easier to audit at a glance |
| Actionability | 0.15 | Positive | SM-001 and SM-005 directly reduce ratification/install friction with zero new mechanism |
| Traceability | 0.10 | Positive | SM-002 legend closes the one real traceability gap found |

---

## Out-of-Scope Observation

While confirming public-repo hygiene (no employer-internal references) across the `design/` tree for context, an employer-name token was found in `projects/PROJ-031-cowork-skeleton/design/qg3-review/s-014-quality-score.md`. **This file is not part of the deliverable package assigned to this iteration** (the assigned package is `feedback-decision-log-convention-design.md` + `staging-feedback-logs/*`), so it is disclosed here as an aside per P-022 honesty, not scored as an S-003 finding against this package. Recommend the orchestrator route this to whichever review currently owns the `qg3-review/` artifact set.

---

## Execution Statistics

- **Total Findings:** 5
- **Critical:** 0
- **Major:** 2
- **Minor:** 3
- **Protocol Steps Completed:** 6 of 6

---

*Strategy: S-003 (Steelman Technique) | Template: `.context/templates/adversarial/s-003-steelman.md` v1.0.0*
*Iteration: 006 | Executed: 2026-07-06*
