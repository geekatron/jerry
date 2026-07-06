# Inversion Report: Feedback & Decision Log Convention (FEEDBACK-LOG + LLM-DECISION-LOG) — Iteration 8

**Strategy:** S-013 Inversion Technique
**Deliverable:** `projects/PROJ-031-cowork-skeleton/design/feedback-decision-log-convention-design.md` + `projects/PROJ-031-cowork-skeleton/design/staging-feedback-logs/{feedback-decision-logs-standards.md, FEEDBACK-LOG.template.md, LLM-DECISION-LOG.template.md, examples-appendix.md, hook-design-note.md}`
**Criticality:** C4 (engagement gate 0.95, user-set)
**Date:** 2026-07-06
**Reviewer:** adv-executor (S-013, iteration-008, blind protocol, VERIFIED-CRITICALS)
**H-16 Compliance:** S-003 Steelman is required earlier in the C3+/C4 sequence per H-16/quality-enforcement.md; not independently re-verifiable from this blind execution (iteration artifacts under `adversary/` were off-limits except `iteration-007/restore-notes.md`, explicitly permitted as the owner's public disposition record). Assumed satisfied at the tournament level.
**Goals Analyzed:** 6 | **Assumptions Mapped:** 9 | **Vulnerable Assumptions (new this round):** 2 (0 Critical, 1 Major, 1 Minor)

## Document Navigation

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Overall verdict, direct answers to the two questions asked |
| [Regression Check](#regression-check-iteration-006-criticals-in-current-text) | Re-verification of the 6 prior Criticals against current text (zero regressions) |
| [Goal Inventory](#goal-inventory-step-1) | What the package must guarantee |
| [Anti-Goals](#anti-goals-step-2) | What would guarantee failure of each goal |
| [Assumption Map](#assumption-map-step-3) | Explicit/implicit assumptions relevant to this round, confidence |
| [Findings Table](#findings-table) | IN-NNN summary (this iteration only) |
| [Finding Details](#finding-details) | Expanded Major + Minor findings |
| [Null-Alternative Comparison](#null-alternative-comparison-directly-asked) | Does it beat memory-files + transcripts only? |
| [Recommendations](#recommendations) | Prioritized mitigations |
| [Scoring Impact](#scoring-impact) | Mapping to S-014 dimensions |

---

## Summary

This is iteration 8 of a package that has already absorbed 7 rounds of adversarial remediation and one owner-directed RESTORE pass (`iteration-007/restore-notes.md`). All 6 Criticals from iteration 006 (RT-001, DA-001/FM-006, PM-001/IN-001, PM-002, FM-001, FM-003) were re-verified against the **current** text of the design doc and rule file in this execution and remain closed — see [Regression Check](#regression-check-iteration-006-criticals-in-current-text). No regression was found on any of them. The two prior Majors this strategy raised in iteration 006 (IN-002 redaction/transcript-retention compounding, IN-003 interrupted-rotation trigger) were also both addressed by text (confirmed below).

Stress-testing the assumptions **underneath the new v9/iteration-7 RESTORE-pass text itself** (the two diagrams and the "Five safety functions" reconciliation are new since iteration 006 and had not yet been inversion-tested) surfaced **one new Major finding**: the IN-003 fix's own claim that its session-start Segment-Index-vs-tail check "does not depend on the model remembering" is an overclaim — the check itself is an unenforced, un-hooked, un-linted SHOULD-tier habit, i.e. exactly the same class of residual the package's own Q5 disclosure already admits for capture ("no detector for a turn that should have been logged but was not"), just relocated to a different mechanism (rotation-recovery) and not cross-referenced to that admission. This does not reopen the original IN-003 gap to a worse state than iteration 006 assessed it (still Major, not Critical) — it means the claimed closure is less complete than the text asserts. One **Minor** internal-consistency nit is also noted (the "Five safety functions ... all miss together" claim in the L2 "One shared dependency" section is directly undercut by the next sentence's own exemption for the fifth). Neither finding invalidates the package's core approach; both are wording-only fixes consistent with the package's own anti-bloat doctrine.

**Direct answer — does the package guarantee feedback gets lost?** No single mechanism in the current text *guarantees* loss. What the package does *not yet fully close* (all disclosed, none new this round except the nuance in IN-005-20260706-iter008 below): (1) capture depends on the model remembering to log a turn (Q5, MEDIUM/SHOULD, no detector, mitigated only by the not-yet-shipped Q3 hook); (2) an uncommitted append is lost on `git checkout`/`reset`/`clean` (disclosed, commit-cadence is the sole mitigation); (3) a fresh session does not yet automatically consult the logs (disclosed read-side gap, fix is a named-but-not-yet-executed install action); (4) the segment-rotation interruption-recovery check added to close the old IN-003 gap is itself a SHOULD-tier habit with no forcing function (this round's finding). None of these are new surprises; (1)-(3) are honestly disclosed at the point of the claim. (4) is the one instance this round where a "closed" claim slightly overstates what was actually closed.

**Direct answer — does it beat the null alternative (`MEMORY.md` + raw transcripts only)?** Unchanged from iteration 006's assessment, re-verified against the current text: **yes on structure/disposition/DEC-ADR-boundary/portability-once-committed; not yet on session-start rediscoverability** (`MEMORY.md` is force-loaded — this very system context demonstrates that — while `FEEDBACK-LOG.md`/`LLM-DECISION-LOG.md` still have no entry in `.context/rules/project-workflow.md`'s session-start orientation row, confirmed by direct inspection of the currently-loaded rule file); **slightly worse on uncommitted-loss durability** (`MEMORY.md` persists regardless of git state; these logs require an explicit commit). The design states this honestly (L0 scope note, Improvement Ledger "Null-alternative note") and does not overclaim it — this is a disclosed residual, not a finding.

**Recommendation:** REVISE (targeted, cosmetic-adjacent). Reword the IN-003 fix's "does not depend on the model remembering" claim in both the design doc and the rule file to accurately describe what changed (a specific historical fact replaced by a generic per-session habit — still SHOULD-tier, still unenforced pre-Q3). Optionally correct the "Five ... all miss together" internal inconsistency. Both fixes are wording-only; no new machinery required, consistent with the deliverable's own anti-bloat doctrine.

---

## Regression Check (iteration-006 Criticals in current text)

Re-verified directly against the current deliverable text (not against the finding as originally stated), independent of `iteration-007/restore-notes.md`'s own claims (cross-checked, not merely trusted):

| # | Finding | Current text | Status |
|---|---------|---------------|--------|
| 1 | RT-001 (redaction laundering) | `feedback-decision-logs-standards.md:24` — redaction note names category + approximate size; "presence, not veracity" scrutiny discipline present | CLOSED, no regression |
| 2 | DA-001/FM-006 ("Four" undercounts fifth) | `feedback-decision-log-convention-design.md:264` — reads "**Five** safety functions", segment-index-overflow named + exempted | CLOSED, no regression (see [Minor finding](#in-006-20260706-iter008-five-safety-functions-all-miss-together-is-contradicted-by-the-next-sentence-minor) below for a new, narrower issue in the *same* sentence) |
| 3 | PM-001/IN-001 (AE-006e wrong backstop) | `feedback-decision-log-convention-design.md:195,241`; `feedback-decision-logs-standards.md:28` — AE-006e claim narrowed to "compaction... flushing pending entries," cap-crossing explicitly disclosed as having no automated backstop | CLOSED, no regression |
| 4 | PM-002 (unfilled `~N sessions` placeholder) | `feedback-decision-log-convention-design.md:260` — reads "~3 sessions or 30 days since this review round, or the next milestone checkpoint" | CLOSED, no regression |
| 5 | FM-001 (no inline-marker dedup) | `feedback-decision-logs-standards.md:51` — "Before minting, check for an existing entry carrying the same `source: inline-doc` `path:line/anchor`" | CLOSED, no regression |
| 6 | FM-003 ("verbatim and full" vs. live split-entry practice) | `feedback-decision-log-convention-design.md:58`; `feedback-decision-logs-standards.md:24` — multi-item message MAY split into per-item entries, each Verbatim its own item's text | CLOSED, no regression |

**Prior S-013-specific Majors (iteration 006), re-verified:**

| Finding | Current text | Status |
|---------|---------------|--------|
| IN-002-20260706-iter006 (redaction + transcript-retention compounding) | `feedback-decision-log-convention-design.md:65` — "Redaction is irreversible in the repo, and that transcript carries the same unenforced-retention / cross-machine-portability dependency already disclosed for Q1"; `feedback-decision-logs-standards.md:24` mirrors it | CLOSED, no regression |
| IN-003-20260706-iter006 (interrupted-rotation no persisted trigger) | `feedback-decision-log-convention-design.md:208`; `feedback-decision-logs-standards.md:67` — a session-start Segment-Index-vs-tail check now exists | **Text present, but the fix's own framing is itself the subject of this round's new finding** — see [IN-005-20260706-iter008](#in-005-20260706-iter008-the-in-003-fix-overclaims-that-it-removes-the-model-memory-dependency-major) |

---

## Goal Inventory (Step 1)

| # | Goal (as stated or inferred) | Measurable form |
|---|---|---|
| G1 | Feedback-worthy user input, once given, is captured into the log | An entry exists for every turn matching a capture trigger (LOG-M-001) |
| G2 | Captured entries survive session boundaries, compaction, and model swaps | Bytes on disk in a committed, pushed git ref |
| G3 | Captured entries are discoverable/consulted in a *later* session | A new session's orientation step actually reads the log before acting |
| G4 | Entry ids and content remain intact under rotation and single-writer discipline, **including recovery from an interrupted rotation** | Contiguous, non-duplicated ids across all segments (L5 lint 2), and any interrupted rotation is actually reconciled before further appends |
| G5 | The convention actually gets installed so its protections apply | Ratification → `.context/rules/` + `mandatory-skill-usage.md` + `project-workflow.md` wiring |
| G6 | Sensitive content is redacted without destroying the only recoverable copy of the underlying information | Redaction marker + recoverable original via an independent channel |

---

## Anti-Goals (Step 2)

- **AG-G4 (rotation-recovery sub-case, re-examined this round):** A rotation crashes mid-procedure; the session-start check added to detect this (IN-003 fix) is itself never run because nothing forces it to run (no hook pre-Q3, no lint pre-append) — the exact "depends on the model remembering" failure the fix's own prose claims to have eliminated → **IN-005-20260706-iter008 (Major)**.
- **AG-consistency (new self-referential case):** The L2 "One shared dependency" claim that all five named safety functions "miss together" if the shared checkpoint is skipped is falsified, in the very next sentence, for one of the five it lists → **IN-006-20260706-iter008 (Minor)**.
- All other anti-goals examined in iteration 006 (AG-G1 no-hook-ships, AG-G2 uncommitted-loss, AG-G3 read-side gap, AG-G6 redaction+transcript-retention) remain addressed by disclosure with no regression (see [Regression Check](#regression-check-iteration-006-criticals-in-current-text)); not re-graded here per the instruction that already-disclosed residuals are not findings.

---

## Assumption Map (Step 3, this round's incremental assumptions — full historical map in `iteration-006/s-013-findings.md`)

| ID | Assumption | Type | Confidence | Validation status |
|---|---|---|---|---|
| A9 | The session-start Segment-Index-vs-tail check "does not depend on the model remembering" (as literally claimed) | Explicit wording | Low | **Falsified** — the check itself is a SHOULD-tier, unenforced, un-hooked, un-linted habit; see IN-005 |
| A10 | The Segment Index row the session-start check compares against is itself accurate | Implicit (Enforcement) | Low | Already disclosed elsewhere as unverified (`feedback-decision-logs-standards.md:85`, scope-limit (e)); not independently re-verified by the new check — compounds A9's risk |
| A11 | "Five safety functions ... all fire at / miss together at the same checkpoint" accurately describes all five listed items | Explicit wording | N/A | **Contradicted** by the same paragraph's own exemption of the fifth item (lint-detected, checkpoint-independent); see IN-006 |

---

## Findings Table

| ID | Assumption / Anti-Goal | Type | Confidence | Severity | Evidence | Affected Dimension |
|----|------------------------|------|------------|----------|----------|--------------------|
| IN-005-20260706-iter008 | Session-start rotation-recovery check "does not depend on the model remembering" | Assumption (A9, compounded by A10) | Low | **Major** | design doc line 208; rule file line 67; rule file line 85 (Segment-Index staleness scope-limit) | Evidence Quality, Internal Consistency |
| IN-006-20260706-iter008 | "Five safety functions... all miss together" | Anti-Goal (wording, A11) | N/A | **Minor** | design doc line 264 | Internal Consistency |

**Finding ID Format:** `IN-{NNN}-20260706-iter008`.

---

## Finding Details

### IN-005-20260706-iter008: The IN-003 Fix Overclaims That It Removes the Model-Memory Dependency [MAJOR]

**Type:** Assumption (self-referential overclaim about the design's own fix)
**Original Assumption:** "**Persisted trigger (IN-003, so recovery does not depend on the model remembering a mid-flight rotation):** before the *first* append of any session, if the Segment Index's last row does not match the ACTIVE file's actual last heading, treat it as a possible interrupted rotation and run the parity check before proceeding — reusing the same `grep`, no new marker file." (`projects/PROJ-031-cowork-skeleton/design/feedback-decision-log-convention-design.md:208`). The rule file mirrors this: "**Trigger (so recovery does not depend on memory):** before the *first* append of any session, if the Segment Index's last row does not match the ACTIVE file's actual last heading, treat it as a possible interrupted rotation and run the parity check before proceeding (IN-003, reuses the same `grep`)." (`projects/PROJ-031-cowork-skeleton/design/staging-feedback-logs/feedback-decision-logs-standards.md:67`).
**Inversion:** Invert the claim: "what would guarantee this check never actually runs?" — the check is not stamped by any hook (Q3 is designed, not shipped, per `hook-design-note.md`), it is not enforced by any L5 lint (the three lint checks all run at commit time, per `feedback-decision-logs-standards.md:78-83`, not at session start before the first append), and there is no L2 per-prompt re-injection for this MEDIUM-tier convention (`feedback-decision-log-convention-design.md:241`, "no L2 per-prompt re-injection"). The obligation to "run this check before the first append of any session" is therefore itself a SHOULD-tier habit that must be performed by the model from memory, every session, forever, until Q3 ships — which is *exactly* the failure mode the same document's own governing principle names: "what depends on the model remembering will eventually be forgotten" (design doc line 38). The fix has not removed the memory-dependency; it has relocated it from "remembering a specific historical fact (was a rotation interrupted?)" to "remembering to perform a specific generic habit (check the tail vs. the index) at the start of every session" — a real but much narrower improvement than "does not depend on the model remembering" asserts. This is the same recurring failure class the whole tournament has repeatedly found (a claim about a compensating control that doesn't fully hold under its own definition), applied here to the design's own newest fix rather than to an external framework citation. **Compounding factor (A10):** even when the check *is* run, it depends on the Segment Index's displayed id-range being accurate — which the rule file's own L5-lint scope-limits list names as unverified: "(e) Segment Index display accuracy — the displayed `id-range` per row is not checked against the segment's true first/last heading... so a stale index row can sit undetected" (`feedback-decision-logs-standards.md:85`). If the Index row is stale, the tail-vs-index comparison can silently miss a genuinely interrupted rotation even when the model does remember to run the check.
**Plausibility:** Medium-High. The scenario is not exotic: this is a MEDIUM-tier convention with no L2 reinjection, by the document's own admission (line 241), and the document's own Q5 disclosure already concedes the parallel case for capture ("no detector for a turn that should have been logged but was not"). There is no structural reason a session-start habit would be more reliably remembered than a same-turn capture habit; if anything, a session-start check is easier to skip because it has no proximate trigger (unlike LOG-M-001, which is cued by the user's own words in the same turn).
**Consequence:** If the check is skipped and a rotation actually was interrupted, the exact original IN-003 vulnerability recurs (an unreconciled split — entries possibly double-counted or dropped) — but now under text that tells a ratifying reviewer this residual is closed ("does not depend on the model remembering"), which could cause the residual to be under-weighted at ratification. This does not make the underlying risk worse than iteration 006 assessed it (still bounded, still Medium plausibility, still recoverable once the wired L5 lint eventually runs) — it means the claimed closure overstates what changed.
**Evidence:** `projects/PROJ-031-cowork-skeleton/design/feedback-decision-log-convention-design.md:208` (design doc claim); `projects/PROJ-031-cowork-skeleton/design/feedback-decision-log-convention-design.md:38` (the document's own governing principle, directly contradicted); `projects/PROJ-031-cowork-skeleton/design/feedback-decision-log-convention-design.md:241` ("no L2 per-prompt re-injection" disclosure, confirming the check is unenforced); `projects/PROJ-031-cowork-skeleton/design/staging-feedback-logs/feedback-decision-logs-standards.md:67` (rule-file mirror of the claim); `projects/PROJ-031-cowork-skeleton/design/staging-feedback-logs/feedback-decision-logs-standards.md:78-83` (the three L5 lint checks, all commit-time, none session-start); `projects/PROJ-031-cowork-skeleton/design/staging-feedback-logs/feedback-decision-logs-standards.md:85` (Segment-Index display-accuracy scope-limit, the compounding factor).
**Dimension:** Evidence Quality (a claim about the fix's own properties is not accurate as stated), Internal Consistency (the claim contradicts the document's own governing principle stated 170 lines earlier in the same file).
**Mitigation:** Reword both instances to something like: "this replaces the need to recall a *specific* historical fact (was a rotation interrupted in a prior session?) with a *generic*, cheap, deterministic per-session habit (check the tail vs. the index) — the habit itself remains a SHOULD-tier, Q3-unenforced action with the same class of risk Q5 already discloses for capture; treat it the same way." Optionally cross-reference the Segment-Index display-accuracy scope-limit (`feedback-decision-logs-standards.md:85`) at the point of this claim, so the compounding dependency is visible where the claim is made (matching the propagation-sweep discipline the package already applies to its other disclosures).
**Acceptance Criteria:** Neither the design doc nor the rule file claims this check "does not depend on the model remembering" without qualification; the residual (habit still unenforced pre-Q3, Index accuracy still unverified) is named at the point of the claim, not only elsewhere in the document.

### IN-006-20260706-iter008: "Five Safety Functions ... All Miss Together" Is Contradicted by the Next Sentence [MINOR]

**Type:** Anti-Goal (internal-consistency wording)
**Original Assumption:** "**Five** safety functions -- staleness review, graduation proposal, Backfill-Queue review, this install-stall re-assessment, **and the Segment-Index-overflow re-assessment (L1.4)** -- all fire at the **same** commit-cadence checkpoint... If that checkpoint is skipped, all five miss *together*, not independently" (`projects/PROJ-031-cowork-skeleton/design/feedback-decision-log-convention-design.md:264`).
**Inversion:** The very next sentence in the same paragraph states: "The Segment-Index-overflow trigger is **explicitly exempt** from the Q3-style dated-worktracker forcing function (DA-001): unlike capture, its failure is detected by lint 2's contiguity/orphan check and is fully recoverable by re-reading segment headings, so it needs no owned review date." If the fifth item's failure is independently detected by an automated lint regardless of whether the human checkpoint ever fires, then it does *not* "miss together" with the other four when the checkpoint is skipped — the two claims describe mutually exclusive outcomes for the same item in the same breath. This is the same recurrence class (DA-001/FM-006) that this exact paragraph was itself remediating in the prior round ("Four" → "Five"), reintroduced in the wording chosen to close it.
**Plausibility:** High as a reading — it is a direct textual contradiction, not a speculative inversion.
**Consequence:** Minor and reassuring, not risk-increasing: the true state of affairs is that the correlated-checkpoint risk covers *four* items, not five (the fifth has an independent backstop), so the paragraph *overstates* the correlated risk rather than understating it. This does not threaten the package's purpose; it is a precision gap in a risk-disclosure paragraph.
**Evidence:** `projects/PROJ-031-cowork-skeleton/design/feedback-decision-log-convention-design.md:264`.
**Dimension:** Internal Consistency.
**Mitigation:** Reword to "Four of five safety functions ... depend on the shared checkpoint; the fifth (Segment-Index-overflow) is independently covered by lint 2 and is named here for completeness, not because it shares the same correlated-failure risk."
**Acceptance Criteria:** The paragraph no longer claims all five items "miss together" while also claiming one of the five has an independent, checkpoint-agnostic detection mechanism.

---

## Null-Alternative Comparison (directly asked)

**Question:** Does the package beat the null alternative (`MEMORY.md` + raw transcripts only)?

Re-verified directly against the current text (unchanged conclusion from iteration 006, confirmed not stale):

- **Structure/disposition/DEC-ADR boundary/portability-once-committed:** Yes — clearly better than raw transcripts, which in this environment live outside the project's git working tree in a machine-local directory (not portable, not part of the repo's branch/backup history).
- **Session-start rediscoverability:** **Not yet.** `MEMORY.md` is force-loaded into every session (directly demonstrated by this conversation's own system-injected memory content). `FEEDBACK-LOG.md`/`LLM-DECISION-LOG.md` still have no entry in `.context/rules/project-workflow.md`'s session-start "Before" orientation row (verified directly against the currently-loaded rule file, which lists only `PLAN.md`, `WORKTRACKER.md`, `docs/knowledge/`, `/worktracker`). The design's own Adoption plan (step 3) names the fix as a not-yet-executed install action — honestly disclosed, not a regression.
- **Uncommitted-loss durability:** Slightly worse than `MEMORY.md` by the design's own admission — these logs require an explicit commit; `MEMORY.md` does not.
- **Net:** Unchanged from iteration 006. A real, disclosed, partial win — not yet a full win on the read-side axis. IN-005 above (this round's finding) means one of the mechanisms that would make the "captured entries are actually intact" half of the story fully solid is itself less airtight than its own text currently claims — worth fixing before ratification, but it is a wording gap in an already-Major (not newly Critical) residual, not a new hole in the floor.

---

## Recommendations

**SHOULD mitigate (Major):**
- **IN-005-20260706-iter008:** Reword the "does not depend on the model remembering" claim in both `feedback-decision-log-convention-design.md:208` and `feedback-decision-logs-standards.md:67` to accurately scope what changed (a specific historical fact replaced by a generic per-session habit, still SHOULD-tier and Q3-unenforced); optionally cross-reference the Segment-Index display-accuracy scope-limit at the point of the claim.

**MAY mitigate (Minor):**
- **IN-006-20260706-iter008:** Reword `feedback-decision-log-convention-design.md:264` to state that four of five safety functions share the correlated-checkpoint risk, with the fifth named for completeness but independently lint-covered.

---

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Neutral | No new gap in coverage; both findings are about the framing of already-covered mechanisms. |
| Internal Consistency | 0.20 | Negative | IN-006: a risk-correlation claim is directly contradicted by the sentence that immediately follows it. |
| Methodological Rigor | 0.20 | Negative | IN-005: a claimed property of a compensating check ("removes the memory dependency") does not hold under the document's own governing principle and enforcement-layer disclosures. |
| Evidence Quality | 0.15 | Negative | IN-005: the specific claim about what the fix accomplishes is not accurate as literally stated. |
| Actionability | 0.15 | Neutral-Positive | Both findings have concrete, wording-only mitigations consistent with the package's own anti-bloat doctrine — no new machinery required. |
| Traceability | 0.10 | Neutral | Both findings cite specific lines and are self-contained; no traceability gap introduced. |

---

*Strategy Execution Statistics*
- **Total Findings (this iteration):** 2
- **Critical:** 0
- **Major:** 1 (IN-005-20260706-iter008)
- **Minor:** 1 (IN-006-20260706-iter008)
- **Regressions found on iteration-006's 6 Criticals + 2 prior S-013 Majors:** 0 (all 8 re-verified closed against current text)
- **Protocol Steps Completed:** 6 of 6 (goals stated, anti-goals inverted, assumptions mapped, stress-tested, mitigations developed, scoring impact synthesized)
- **Blind protocol:** No files under `orchestration/fu-log-convention-20260705-001/adversary/iteration-007/` or `iteration-008/` were read except this output file and `iteration-007/restore-notes.md` (explicitly permitted as the owner's public disposition record). Iterations 001-006 findings were read as disposition history. Permitted context otherwise: design doc, all 5 staged artifacts, both live bootstrap logs (already resident in this session's environment context), `.context/rules/quality-enforcement.md` and `.context/rules/project-workflow.md` (already loaded in this session's context).
