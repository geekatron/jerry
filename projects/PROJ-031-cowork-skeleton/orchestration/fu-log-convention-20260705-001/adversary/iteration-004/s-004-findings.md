# Pre-Mortem Report: FEEDBACK-LOG + LLM-DECISION-LOG Convention (Iteration 4)

## Document Sections

| Section | Purpose |
|---------|---------|
| [Header](#header) | Strategy metadata and H-16 compliance |
| [Summary](#summary) | Overall assessment and recommendation |
| [Findings Table](#findings-table) | All PM-NNN findings at a glance |
| [Finding Details](#finding-details) | Full detail for each Major finding |
| [Minor Findings (Compact)](#minor-findings-compact) | Minor findings, compact form |
| [Recommendations](#recommendations) | P0/P1/P2 mitigation plan |
| [Scoring Impact](#scoring-impact) | Dimension-level impact mapping |
| [Coverage Notes](#coverage-notes) | Failure paths checked and found already disclosed/prevented |

---

## Header

**Strategy:** S-004 Pre-Mortem Analysis
**Deliverable:** `projects/PROJ-031-cowork-skeleton/design/feedback-decision-log-convention-design.md` + `design/staging-feedback-logs/{feedback-decision-logs-standards.md, FEEDBACK-LOG.template.md, LLM-DECISION-LOG.template.md, examples-appendix.md, hook-design-note.md}`
**Criticality:** C4 (engagement gate 0.95, user-set)
**Date:** 2026-07-06
**Reviewer:** adv-executor (S-004, blind protocol, iteration 4)
**H-16 Compliance:** Satisfied by evidence internal to the deliverable — the design doc's own Revision Changelog (`design/feedback-decision-log-convention-design.md:317-320`) cites extensive `SM-NNN` (Steelman) findings closed across iterations 1-3 (e.g. `SM-001`, `SM-002`, `SM-003`, `SM-004`, `SM-005`, `SM-006`, `SM-007`), confirming S-003 has already run and strengthened this deliverable multiple times before this S-004 pass. No fresh S-003 output was supplied for iteration 4 specifically, but H-16's intent (steelman before critique, on the strongest version of the artifact) is satisfied by this prior-round record. Proceeding.
**Failure Scenario (declared, per protocol Step 1-2):** It is 2027-07-06. The FEEDBACK-LOG/LLM-DECISION-LOG convention has failed quietly, not loudly: entries slowed to a trickle around month 4 and stopped almost entirely by month 7; the two live bootstrap logs never rotated even after crossing the cap because the model-memory-dependent self-count habit lapsed and the lint was never wired into CI; the Q3 provenance/reminder hook was "revisited" twice at its stated re-assessment triggers and deferred again both times, so every entry in year one still has hand-typed, occasionally-wrong session/model metadata; a Backfill Queue row silently vanished during the one rotation that did occur because nobody checked it was carried forward; and several months of real feedback exist only as vague memories, because the review habit that was supposed to catch staleness, propose graduation, and audit the backfill queue was itself keyed to a commit-cadence ritual that had gone quiet.

---

## Summary

Zero Critical findings. This package has already absorbed three prior remediation rounds (iterations 1-3, referenced in `design/feedback-decision-log-convention-design.md:317-320`) that closed 30 Criticals across recurring overclaim classes (collision-proof language, "byte-exact"/guarantee wording, immutability-without-caveat). By iteration 4 the remaining overclaim surface is thin, and I found none that meet the Critical bar (a claim of protection/coverage that does not actually exist). What remains are seven genuine, evidence-based gaps in the disclosed failure surface — three Major, four Minor — clustered around a single theme: several of the package's own safety nets are themselves dependent on the exact "the model/human will remember" failure mode the design's own governing principle warns against (`design/feedback-decision-log-convention-design.md:38`), and this dependency is not fully traced through to its second-order consequences (a hook with no forcing function, a Backfill Queue carry-forward step with no parity check, and multiple independent-sounding review triggers that collapse to one unenforced ritual). **Recommendation: ACCEPT WITH MITIGATIONS.** None of the findings invalidate the MEDIUM-tier, anti-bloat posture the user has ratified; all seven are addressable by wording/disclosure/small-process fixes consistent with the package's own established remediation pattern (no new lint, no new subsystem required for any of them except optionally PM-003).

---

## Findings Table

| ID | Failure Cause | Category | Likelihood | Severity | Priority | Affected Dimension |
|----|---------------|----------|------------|----------|----------|--------------------|
| PM-001-iter004 | Q3 provenance/reminder hook has no forcing function, owner, or tracked work item — real risk of indefinite deferral mirroring the exact `[internal-kb]` "wish never shipped" anti-pattern this package claims to fix | Process / Resource | High | Major | P1 | Completeness |
| PM-002-iter004 | Multiple independent-sounding safety nets (staleness nudge, graduation-cadence proposal, Backfill Queue review) all collapse to the same single, unenforced "commit-cadence checkpoint" trigger — a correlated single point of failure never named as such | Process | High | Major | P1 | Methodological Rigor |
| PM-003-iter004 | Segment-rotation Backfill Queue carry-forward has no parity/verification check, unlike the main entry sequence which gets a required, explicit check | Technical / Process | Medium | Major | P2 | Methodological Rigor |
| PM-004-iter004 | Installing the ~2,150-token rule file into `.context/rules/` is never reconciled against the SSOT's own "~12,500" L1 session-start token budget (`quality-enforcement.md` Enforcement Architecture table) | Technical | Medium | Minor | P2 | Traceability |
| PM-005-iter004 | The Q3 hook's "~3 months of wall-clock time" re-assessment trigger — the one calendar-bound commitment in the design — has no persistent, force-loaded reminder (e.g. a `MEMORY.md` entry), contrary to the design's own guidance that cross-session standing triggers belong there | Assumption | Medium | Minor | P2 | Actionability |
| PM-006-iter004 | The interim (pre-hook) cap-crossing self-count discipline is itself a model-memory-dependent mechanism, in tension with the design's own governing principle ("what depends on the model remembering will eventually be forgotten") | Technical / Internal Consistency | Low | Minor | P2 | Internal Consistency |
| PM-007-iter004 | Claude Code transcript JSONL schema stability over a 12-month horizon is an unstated external dependency for the (currently unshipped) hook's `message.model` resolution (Seam 1) | External | Low | Minor | P2 | Evidence Quality |

**Finding ID Format:** `PM-{NNN}-iter004` (iteration 4 of this tournament; prior iterations used their own execution ids per the blind protocol).

---

## Finding Details

### PM-001-iter004: Q3 hook has no forcing function, owner, or tracked ticket [MAJOR]

**Failure Cause:** The Q3 provenance/reminder hook is the single mechanism designed to remove hand-typed, drift-prone metadata (`hook-design-note.md:1-57`) — the exact `[internal-kb]` failure class this package claims to fix (Improvement Ledger row 3, `design/feedback-decision-log-convention-design.md:252`). Its shipment is explicitly deferred: "the hook is designed in v1 ... but shipped as a separate gated change" (`hook-design-note.md:57`; PROPOSED-DEFAULT Q3, `design/feedback-decision-log-convention-design.md:273`). The only re-visitation mechanism is a soft "re-assessment trigger," not a shipment commitment: "revisit the deferral at the first segment rotation, or after a fixed cadence checkpoint..., or ~3 months of wall-clock time, or the first time a missed capture is discovered incidentally... whichever comes first" (`design/feedback-decision-log-convention-design.md:237`). Nothing in the Adoption plan (steps 1-7, `design/feedback-decision-log-convention-design.md:232-240`) assigns an owner or a worktracker Enabler/Story to actually build the hook; step 6 reads as optional ("ship the hook now or as a fast follow").
**Category:** Process / Resource
**Likelihood:** High — justified by direct precedent *within this same package's own research*: the `[internal-kb]` "templatize" wish (`[legacy-oi-id]`) "never shipped" despite being flagged (Improvement Ledger row 1, `design/feedback-decision-log-convention-design.md:250`), and the sibling ADR-convention effort in this same project needed a multi-iteration subtraction pass to escape a stall (cited at `design/feedback-decision-log-convention-design.md:240`). A "re-assessment trigger" with no assigned owner and no tracked ticket is exactly the condition under which both of those precedents occurred.
**Severity:** Major — Consequence if this failure occurs: the whole first year (and potentially indefinitely) runs on hand-typed provenance and zero automated capture reminders, i.e. the entire manual-drift risk the hook exists to close persists for the convention's entire practical lifetime, and the design's own text treats the hook as settled ("the hook ... is the remedy," `design/feedback-decision-log-convention-design.md:221`) in a way that reads more confident than its actual (unscheduled, ownerless) status warrants.
**Evidence:** `design/feedback-decision-log-convention-design.md:221,237,240,250,273`; `design/staging-feedback-logs/hook-design-note.md:57`.
**Dimension:** Completeness (the Adoption plan is incomplete without an accountable follow-through mechanism for its own most load-bearing deferred item).
**Mitigation:** No new machinery required — a wording + tracking fix only. (a) Soften "is the remedy" to "is the intended remedy, contingent on a future gated change that is not yet scheduled." (b) Create (or reference, if one already exists outside this reviewer's blind scope) a worktracker Enabler/Story for the Q3 hook with the existing re-assessment triggers as its own acceptance criteria, so the deferral is at least visible in the worktracker rather than only inside this design doc's prose.
**Acceptance Criteria:** Either (a) a worktracker id for the Q3 hook is added to the Adoption plan, or (b) the design doc explicitly and prominently states that no such tracking exists yet and that the re-assessment trigger is honor-system only, so the residual risk is undiluted.

---

### PM-002-iter004: Correlated single point of failure — multiple safety nets keyed to one unenforced "commit-cadence checkpoint" [MAJOR]

**Failure Cause:** At least three distinct review disciplines are all triggered by "the commit-cadence checkpoint": (1) FEEDBACK-LOG staleness review — "Non-terminal (OPEN/IN-PROGRESS) entries are reviewed for staleness at the existing commit-cadence checkpoint — a nudge, not a mechanism" (`design/feedback-decision-log-convention-design.md:58`); (2) LLM-DECISION-LOG graduation proposal — "work-item-attached, review-hardened decisions SHOULD be proposed for graduation at the next commit-cadence checkpoint" (`design/feedback-decision-log-convention-design.md:139`; also `feedback-decision-logs-standards.md:26`); (3) Backfill Queue review for both logs — "reviewed at the same commit-cadence checkpoint as OPEN entries" (`FEEDBACK-LOG.template.md:56`, `LLM-DECISION-LOG.template.md:61`). The commit-cadence directive itself is a MEDIUM "standing directive" (FEEDBACK-LOG FU.3, `FEEDBACK-LOG.md:71-78`), not an enforced mechanism — and this very project's own commit history shows the cadence is already imperfect in practice: FU.3's disposition admits "committed `--no-verify` once" and a 178-file bulk commit (`518c6556`) rather than granular per-change commits (`FEEDBACK-LOG.md:78`).
**Category:** Process
**Likelihood:** High — the correlating trigger has already shown irregularity (bulk commits, one disclosed `--no-verify`) within the very project that authored this design, and nothing about the trigger changes once installed elsewhere.
**Severity:** Major — Consequence: if the commit-cadence habit lapses for an extended period (a plausible, even likely, occurrence over 12 months given competing priorities, session churn, or a long research spree with few commits), staleness review, graduation proposals, AND both Backfill Queues go silent simultaneously — not independently, but as one correlated outage. This is a materially different (and larger) risk than any one of the three disclosures reads in isolation.
**Evidence:** `design/feedback-decision-log-convention-design.md:58,139`; `design/staging-feedback-logs/FEEDBACK-LOG.template.md:56`; `design/staging-feedback-logs/LLM-DECISION-LOG.template.md:61`; `projects/PROJ-031-cowork-skeleton/FEEDBACK-LOG.md:78` (evidence of already-imperfect cadence).
**Dimension:** Methodological Rigor (the design does not appear to have evaluated the aggregate/correlated effect of reusing one trigger for several distinct safety mechanisms, even though each instance is individually disclosed).
**Mitigation:** No new machinery — a one-sentence disclosure fix, consistent with this package's established anti-bloat remediation pattern (wording/deletion only, e.g. iteration 1-3 fixes per the Revision Changelog). Add a single sentence naming the correlation explicitly, e.g.: "Note: staleness review, graduation proposal, and Backfill Queue review all share the same commit-cadence trigger; if that habit lapses, all three lapse together — this is an accepted MEDIUM-tier trade, not three independent safeguards."
**Acceptance Criteria:** The design doc (or the staged rule file) contains an explicit sentence naming this as one correlated risk rather than three separately-scoped ones.

---

### PM-003-iter004: Backfill Queue carry-forward at rotation has no parity check [MAJOR]

**Failure Cause:** The rotation procedure's Step 3 "Parity check (required, not optional)" verifies only the canonical entry sequence: "confirm the sealed segment's entry count plus the new ACTIVE's count equals the pre-seal count — `grep -c '^## FU\.'` (or `'^## DEC-LLM-'`...) on both" (`design/feedback-decision-log-convention-design.md:189`). Step 2 separately instructs "carry forward any unresolved Backfill Queue rows into the new ACTIVE (they live only in ACTIVE and are excluded from the sealed segment, so they must travel with it)" (`design/feedback-decision-log-convention-design.md:188`) — but this carry-forward step has no analogous verification. If the model/operator performing a future rotation (a rare, one-time-per-cap event, likely performed without much practiced muscle memory) forgets this specific sub-step, the required parity check would still PASS (it only counts `## FU.N` headings, not Backfill Queue rows), giving false confidence that "nothing was dropped" while the Backfill Queue's pending candidates are silently and irrecoverably lost inside the now-immutable-by-convention sealed segment.
**Category:** Technical / Process
**Likelihood:** Medium — rotation has not yet occurred in this project (the live bootstrap logs are far from the ~50-entry/~800-line cap), so this is a future, one-time procedural risk whose probability depends on how carefully a future session follows the written 4-step procedure; it is not a certainty, but the specific verification gap is concrete and already present in the written procedure today.
**Severity:** Major — Consequence: a silent loss of exactly the kind of item ("that feedback about X," pre-log candidates) whose disposition-tracking this package otherwise treats with unusual rigor elsewhere (e.g. the required entry-parity check, the id-integrity lint). The asymmetry (rigorous check for entries, no check for Backfill Queue rows) is the actual defect, not the carry-forward instruction itself, which does exist.
**Evidence:** `design/feedback-decision-log-convention-design.md:188-189`; `design/staging-feedback-logs/feedback-decision-logs-standards.md:50` (repeats the same asymmetry in the shipped rule file: "unresolved Backfill rows **carry forward** into the new ACTIVE" with no accompanying check language).
**Dimension:** Methodological Rigor (asymmetric verification applied to two artifacts that live in the same file and rotate together).
**Mitigation:** Extend the existing required parity check's wording to also cover the Backfill Queue row count (pre-seal vs. post-carry-forward), rather than inventing a new check. This is a wording extension to an already-required step, not new machinery.
**Acceptance Criteria:** Rotation procedure Step 3 explicitly states the Backfill Queue row count is also confirmed unchanged across the rotation, alongside the existing entry-count parity check.

---

## Minor Findings (Compact)

### PM-004-iter004: L1 token-budget impact of the new rule file is not reconciled against the SSOT [MINOR]

**Evidence:** `.context/rules/quality-enforcement.md` Enforcement Architecture table states L1 (session start) currently consumes "~12,500" tokens across all auto-loaded `.context/rules/*.md` files (confirmed empirically: this very executor task received all 14 current `.context/rules/*.md` files verbatim as auto-loaded context). The staged rule file measures "~2,150 tokens" (`design/feedback-decision-log-convention-design.md:202`) and is targeted for install into `.context/rules/` (Adoption step 3, `design/feedback-decision-log-convention-design.md:234`) — an addition of roughly 17% to the current L1 budget figure. Nowhere in the package is this aggregate/global L1 impact reconciled against the SSOT's own stated figure, despite the package's otherwise obsessive self-measurement of its own token footprint. **Dimension:** Traceability. **Mitigation (no new machinery):** one sentence noting the L1 budget-aggregate impact and recommending the SSOT figure be updated at install time.

### PM-005-iter004: The Q3 3-month re-assessment trigger is not itself persisted to `MEMORY.md` [MINOR]

**Evidence:** The design explicitly recommends that cross-session standing directives "SHOULD **also** be persisted to `MEMORY.md`... so a standing directive [is] rediscoverable from a later, unrelated project" (`design/feedback-decision-log-convention-design.md:98`). Yet the design's own most concrete deadline — "~3 months of wall-clock time" for revisiting the Q3 hook deferral (`design/feedback-decision-log-convention-design.md:237`) — has no corresponding entry in the user's `MEMORY.md` (checked; no matching entry present as of this review). **Dimension:** Actionability. **Mitigation (no new machinery, self-consistent with the package's own stated best practice):** add one `MEMORY.md` entry for the Q3 re-assessment deadline.

### PM-006-iter004: Interim self-count discipline is itself model-memory-dependent [MINOR]

**Evidence:** The design's stated governing principle is "what depends on the model remembering will eventually be forgotten" (`design/feedback-decision-log-convention-design.md:38`). Yet the interim (pre-hook) safeguard against uncontrolled log growth is: "until the Q3 cap-reminder hook ships the assistant SHOULD self-count entries/lines in the ACTIVE file as it appends and proactively propose rotation on approaching the cap" (`design/feedback-decision-log-convention-design.md:178`; repeated in `feedback-decision-logs-standards.md:28`) — precisely a model-memory-dependent mechanism, for the one safeguard category (log-size control) the package otherwise treats as load-bearing. Tempered because a commit-time lint (once wired) is a real, disclosed backstop (`design/feedback-decision-log-convention-design.md:217`). **Dimension:** Internal Consistency. **Mitigation:** none required beyond acknowledging the tension in one sentence; this is an honest self-consistency note, not a new failure path beyond what the lint-bypass disclosure already covers.

### PM-007-iter004: Transcript JSONL schema drift is an unstated external dependency for hook Seam 1 [MINOR, `[INFERENCE]`]

**Evidence:** Hook Seam 1 resolves `model_of_last_assistant_turn` "by reading the last `assistant` record's `message.model` from the transcript JSONL (`[INFERENCE]`: model is not on hook stdin; it is only in the transcript...)" (`hook-design-note.md:29`). No schema-version pinning, validation, or fallback-on-format-change is described. Low priority because the hook itself is unshipped and separately gated (Q3), so this externality is only live once/if the hook actually ships. **Dimension:** Evidence Quality / Completeness. **Mitigation:** none required now; flag for the hook's own eventual implementation gate.

---

## Recommendations

**P0 (Immediate — MUST mitigate before acceptance):** None.

**P1 (Important — SHOULD mitigate):**
- PM-001-iter004: Soften "is the remedy" framing and/or attach a tracked worktracker id to the Q3 hook so its deferral is visible outside this design doc's prose. Acceptance: wording softened OR tracking id added.
- PM-002-iter004: Add one sentence naming the commit-cadence-checkpoint correlation across staleness/graduation/backfill reviews as a single accepted risk. Acceptance: sentence present in the design doc or staged rule file.

**P2 (Monitor — MAY mitigate; acknowledge risk):**
- PM-003-iter004: Extend the existing required rotation parity check to also cover Backfill Queue row counts.
- PM-004-iter004: Note the aggregate L1 budget impact against the SSOT's "~12,500" figure at install time.
- PM-005-iter004: Add a `MEMORY.md` entry for the Q3 3-month re-assessment deadline.
- PM-006-iter004: Optionally acknowledge the self-count-discipline / governing-principle tension in one sentence.
- PM-007-iter004: No action needed until/unless the Q3 hook is actually scheduled for implementation; flag then.

---

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Negative (minor) | PM-001-iter004: Adoption plan lacks a forcing/ownership mechanism for its most load-bearing deferred item. |
| Internal Consistency | 0.20 | Negative (minor) | PM-006-iter004: interim self-count discipline is in tension with the package's own governing principle; otherwise this package's internal consistency is strong after 3 prior remediation rounds. |
| Methodological Rigor | 0.20 | Negative | PM-002-iter004, PM-003-iter004: correlated single point of failure across review triggers, and asymmetric verification rigor (entries checked at rotation, Backfill Queue not) are both methodological gaps in an otherwise unusually rigorous package. |
| Evidence Quality | 0.15 | Neutral | Findings are evidence-based with file+line citations throughout; PM-007-iter004 is explicitly labeled `[INFERENCE]` per P-022. |
| Actionability | 0.15 | Negative (minor) | PM-005-iter004: the design's own MEMORY.md-persistence advice is not applied to its own most concrete deadline. |
| Traceability | 0.10 | Negative (minor) | PM-004-iter004: new rule file's aggregate L1 budget impact is untraced against the SSOT figure it will affect. |

**Overall assessment:** No Critical failure causes were found. The three Major findings (PM-001, PM-002, PM-003) are all real, previously-unflagged gaps in the disclosed failure surface, but none invalidate the deliverable's deliberately minimal, MEDIUM-tier posture, and all are addressable via wording/disclosure fixes or a small check-extension — consistent with this package's own established remediation pattern across iterations 1-3. **ACCEPT WITH MITIGATIONS.**

---

## Coverage Notes

Failure paths from the prompt's "12 months out" scenario that this pre-mortem checked and found **already honestly disclosed / adequately prevented for a MEDIUM-tier convention** (no new finding raised; anti-bloat posture respected, no new machinery demanded):

- **"ids drifted" via concurrent writers** — thoroughly disclosed as collision-resistant-not-collision-proof, with an explicit out-of-scope boundary for concurrent top-level sessions and direct hand-edits (`design/feedback-decision-log-convention-design.md:74-75`; `feedback-decision-logs-standards.md:27`).
- **"rotation never happened" via lint bypass** — explicitly disclosed, including the concrete precedent that this very project has already used `--no-verify` once (`design/feedback-decision-log-convention-design.md:223`).
- **"entries missing" via team growth / multi-writer adoption** — explicitly scoped out-of-scope with rationale (`design/feedback-decision-log-convention-design.md:97`).
- **"entries missing" via transcript loss (LLM-DECISION-LOG assistant-verbatim recoverability)** — repeatedly and honestly disclosed as an unenforced dependency, with a stated C3+/ADR-graduating full-paste mitigation (`design/feedback-decision-log-convention-design.md:121,123,261`; `examples-appendix.md:116`).
- **"logs abandoned" via read-side gap (new sessions never consult the logs)** — disclosed, with a concrete install-step remedy already planned (`design/feedback-decision-log-convention-design.md:224,234`); confirmed via direct inspection that `.context/rules/project-workflow.md` does not yet reference these logs, consistent with "deferred to install."

None of these required a new finding; they represent the package's own prior remediation rounds (iterations 1-3) working as intended.

---

*Report Version: 1.0*
*Strategy Template: `.context/templates/adversarial/s-004-pre-mortem.md` v1.0.0*
*Blind protocol: no file under `orchestration/fu-log-convention-20260705-001/adversary/` was read except this output file.*
*Constitutional: P-003 (no subagents), P-020 (draft-only, no framework-path writes), P-022 (evidence cited; inference labelled).*
