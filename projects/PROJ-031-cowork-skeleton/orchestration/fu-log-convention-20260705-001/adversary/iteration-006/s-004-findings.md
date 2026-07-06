# Pre-Mortem Report: FEEDBACK-LOG + LLM-DECISION-LOG Convention (Iteration 6)

**Strategy:** S-004 Pre-Mortem Analysis
**Deliverable:** `projects/PROJ-031-cowork-skeleton/design/feedback-decision-log-convention-design.md` + `projects/PROJ-031-cowork-skeleton/design/staging-feedback-logs/{feedback-decision-logs-standards.md, FEEDBACK-LOG.template.md, LLM-DECISION-LOG.template.md, examples-appendix.md, hook-design-note.md}`
**Criticality:** C4 (engagement gate 0.95, user-set)
**Date:** 2026-07-06
**Reviewer:** adv-executor (blind, iteration 6)
**H-16 Compliance:** `[INFERENCE]` — S-003 Steelman presumed executed in the prior tournament group per the documented 6-group blind order (self-refine -> steelman -> challenge -> verify -> decompose -> score). The blind protocol for this execution forbids reading any file under `adversary/` other than this output, so direct confirmation of the S-003 artifact was not performed; this is an orchestration-level assumption, not a verified fact.
**Failure Scenario:** It is 2027-07-06. The FEEDBACK-LOG/LLM-DECISION-LOG convention has quietly failed. PROJ-031's `FEEDBACK-LOG.md` is 2,400 lines long and was never rotated. Three feedback items from a session six months ago were never captured. The ratified design was never installed into `.context/rules/` — it stalled after this review round and nobody flagged it as stalled. The two bootstrap logs are still running the informal, pre-convention, unrotated scheme they started with on day one.

## Navigation

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Overall assessment and recommendation |
| [Findings Table](#findings-table) | All PM-NNN findings, severity, priority |
| [Finding Details](#finding-details) | Expanded Critical/Major findings with evidence |
| [Recommendations](#recommendations) | P0/P1/P2 mitigation plan (wording-only, no new machinery) |
| [Scoring Impact](#scoring-impact) | Mapping to S-014 dimensions |
| [What The Package Already Prevents](#what-the-package-already-prevents-credit-where-due) | Failure paths already closed, for balance |

---

## Summary

Six failure causes were newly identified via prospective hindsight after reading the full package (design doc + all 5 staged files) and the two live bootstrap logs; two are Critical (both are *overclaimed-coverage* defects — a stated backstop that does not actually cover the failure mode it is cited for), four are Major, two are Minor. The dominant 12-months-out failure path is **not** a missing disclosure (this package already discloses more residual risk per line than any other artifact in this project) but two places where an existing disclosure *names a mitigation that does not structurally work*: the AE-006e compaction checkpoint is cited as the rotation-cap backstop but fires on a different, uncorrelated signal (this session's own context fill, not the log's cumulative size across all sessions), and the install-stall re-assessment trigger uses an unfilled placeholder (`~N sessions`) so the single safeguard against "this never gets installed, so none of the protections ever apply to the real logs" has no operational value. All proposed fixes below are wording/disclosure-only, consistent with every prior remediation round in this package's history (v3-v7: zero new machinery each time) — no new lint, hook, or file is proposed. **Recommendation: REVISE** — the substance is sound and the fixes are small, but two Critical overclaims must be corrected before acceptance per the explicit "overclaimed coverage IS Critical" instruction for this review.

---

## Findings Table

| ID | Failure Cause | Category | Likelihood | Severity | Priority | Affected Dimension |
|----|---------------|----------|------------|----------|----------|--------------------|
| PM-001-20260706-I6 | AE-006e cited as the rotation-cap backstop, but its trigger (this session's context-fill/compaction) does not correlate with the actual failure surface (cumulative log size across many sessions) | Process | Medium | Critical | P0 | Internal Consistency |
| PM-002-20260706-I6 | Install-stall re-assessment trigger uses an unfilled placeholder (`~N sessions`), leaving the sole safeguard against indefinite non-adoption without an operational value | Process | Medium-High | Critical | P0 | Completeness |
| PM-003-20260706-I6 | Segment Index display (id-range per row) is never verified against the segment's true first/last heading; only overall contiguity is lint-checked | Technical | High | Major | P1 | Completeness |
| PM-004-20260706-I6 | Backfill-Queue row-count parity is checked once, at rotation time only; no ongoing lint re-verifies it, so a skipped/interrupted rotation can silently and permanently drop Backfill rows | Technical | Medium | Major | P1 | Completeness |
| PM-005-20260706-I6 | "At or near cap" (the trigger for switching id-minting from an LLM Read to a deterministic `grep -c` count) has no numeric definition | Assumption | Low-Medium | Major | P2 | Methodological Rigor |
| PM-006-20260706-I6 | No periodic re-verification that the ≤3 L5 lint checks remain wired + branch-protected after install; CI/pipeline drift over a 12-month horizon is undetected by any named owner or cadence | Process | Medium | Major | P1 | Completeness |
| PM-007-20260706-I6 | Directory-level segment-file proliferation (dozens of sealed segments/year at observed velocity) is not acknowledged anywhere | Resource | High | Minor | P2 | Actionability |
| PM-008-20260706-I6 | The inline-doc-marker "occasional project-open sweep" backstop has no forcing function or cadence, unlike every sibling residual in this design (Q3 hook, install-stall, graduation, Backfill review all got a named checkpoint) | Process | Medium | Minor | P2 | Actionability |

---

## Finding Details

### PM-001: AE-006e mis-cited as the rotation-cap backstop [CRITICAL]

**Failure Cause:** The design instructs that, until the (unshipped) Q3 provenance/reminder hook exists, the assistant self-counts entries/lines to catch the ~50-entry/~800-line segment cap, and that "the framework's existing AE-006e mandatory compaction checkpoint is the interim backstop if the count is forgotten."

**Category:** Process
**Likelihood:** Medium — self-count discipline forgetting across many short sessions over 12 months is plausible; the project's own history already shows a related enforcement gap being exercised (a `--no-verify` commit, `FEEDBACK-LOG.md:78`).
**Severity:** Critical — an unrotated, oversized FEEDBACK-LOG directly recreates "the exact context-rot Jerry exists to solve" (design doc's own framing, line 174), which is the deliverable's entire reason for existing.
**Evidence:**
- `projects/PROJ-031-cowork-skeleton/design/staging-feedback-logs/feedback-decision-logs-standards.md:28` — "This self-count is a temporary exception to the governing principle (design doc L1.4; AE-006e is the interim backstop)."
- `projects/PROJ-031-cowork-skeleton/design/feedback-decision-log-convention-design.md:180` — "...the framework's existing **AE-006e** mandatory compaction checkpoint is the interim backstop if the count is forgotten (RT-004/FM-001)."
- Per `.context/rules/quality-enforcement.md` Auto-Escalation Rules table: AE-006e fires on "Compaction event detected" — a property of the *current session's own context window*, not of the FEEDBACK-LOG file's cumulative size. A short, low-context session that appends two entries to an already-750-line file never approaches compaction and never triggers AE-006e, yet the file can cross the cap mid-append with zero automated signal. Across many such sessions (the realistic profile for a MEDIUM-tier convention with no dedicated skill invocation), the cap can be exceeded indefinitely without AE-006e ever firing.
**Dimension:** Internal Consistency — the claim ("AE-006e … is the interim backstop") is presented as functioning coverage, but is inconsistent with AE-006e's actual trigger semantics as defined in the same rules corpus this design cites.
**Mitigation:** Delete or replace the AE-006e citation in both locations with an honest statement that no automated, cumulative-size-aware backstop currently exists for cap-crossing besides the (currently unwired, `--no-verify`-bypassable) L5 lint check at commit time. No new mechanism proposed — wording only.
**Acceptance Criteria:** Neither the staged rule file nor the design doc asserts AE-006e as a functioning rotation-cap backstop; the gap is instead named as an accepted residual, consistent with the rest of the package's disclosure style.

### PM-002: Install-stall trigger has an unfilled placeholder [CRITICAL]

**Failure Cause:** The one safeguard against "this design never gets ratified/installed, so none of its protections (id scheme, rotation, lint) ever apply to the real, live PROJ-031 logs" is gated on a literal template placeholder that was never filled in.

**Category:** Process
**Likelihood:** Medium-High — the design doc itself cites a directly analogous, already-realized precedent in this same project (the sibling ADR-convention effort's multi-iteration stall), so "indefinite delay" is not hypothetical here.
**Severity:** Critical — if install never happens, the bootstrap logs keep running "the informal FU.2-only convention" indefinitely (design doc's own words), i.e. exactly today's un-rotated, non-monotonic-id, unlint-checked state, for the entire 12-month horizon — the precise "logs abandoned / ids drifted / rotation never happened" outcome named in this pre-mortem's brief.
**Evidence:**
- `projects/PROJ-031-cowork-skeleton/design/feedback-decision-log-convention-design.md:244` — "If the design is not ratified within a bounded window (**e.g. ~N sessions** or the next milestone checkpoint), the bootstrap logs keep operating under the informal FU.2-only convention and the owner flags the stall at the next commit-cadence checkpoint rather than letting it lapse silently."
- Contrast with the Q3 hook's trigger, same document, line 241, which *does* carry a concrete bound: "**or ~3 months of wall-clock time**". The install-stall trigger — arguably the more consequential of the two, since it gates whether *any* of this design's protections ever activate on the real logs — was never given the equivalent concrete figure.
- "next milestone checkpoint" is likewise unscheduled: for a stalled/deprioritized initiative there may be no future milestone to check against, so both halves of the OR-condition are soft.
**Dimension:** Completeness — the mitigation clause is present in prose but missing its one load-bearing parameter.
**Mitigation:** Replace `~N sessions` with a concrete bound, reusing the pattern already established elsewhere in this same document (the ~3-month bound used for the Q3 hook, graduation, and Backfill review triggers), e.g. "~3 sessions or 30 days since this review round, whichever comes first." No new machinery — a single-variable substitution.
**Acceptance Criteria:** The install-stall trigger names a concrete, checkable value; it does not rely on an unfilled template variable.

---

### PM-003: Segment Index display drift is unverified [MAJOR]

**Category:** Technical. **Likelihood:** High (a hand/LLM-maintained table over many rotations across 12 months is a plausible drift surface). **Severity:** Major (bounded/recoverable — a `grep` of headings always resolves the true state — but it degrades exactly the "easy forward/backward navigation" outcome FU.5 asked for).

**Evidence:** `projects/PROJ-031-cowork-skeleton/design/staging-feedback-logs/feedback-decision-logs-standards.md:66` (lint 2 description) and `:69` (the "Scope limits" disclosure block, items a-d) never mention that the Segment Index's *displayed* `canonical-id-range` column is not itself checked against the segment file's actual first/last heading — lint 2 derives true contiguity from the headings directly (design doc `:184`: "the id-ranges are read from each segment's first/last headings, not from filenames"), so a stale or mistyped index row can sit undetected indefinitely; nothing in the existing four-item scope-limits list covers this fifth gap.

**Mitigation:** Add a fifth bullet to the existing Scope-limits block naming this exact gap (the block already lists four; this is consistent with the established disclosure pattern, not new machinery).

### PM-004: Backfill-Queue parity is a one-time check, not an ongoing invariant [MAJOR]

**Category:** Technical/Process. **Likelihood:** Medium (a session crash mid-rotation is an explicitly named, already-observed project reality — `projects/PROJ-031-cowork-skeleton/FEEDBACK-LOG.md:49`, "interrupted by a session crash, resumed from cache," albeit in a different workflow). **Severity:** Major (silent, permanent data loss of Backfill candidates with zero future detection).

**Evidence:** `.../feedback-decision-log-convention-design.md:193` (rotation procedure step 3) requires the parity check "confirm... the Backfill-Queue rows carried forward equal the pre-seal row count" — but this check runs *only during* rotation. None of the ≤3 ongoing L5 lint checks (`.../feedback-decision-logs-standards.md:65-67`) re-verify Backfill-Queue integrity on any subsequent commit. A rotation whose parity step is skipped, or an interruption resumed without re-running it (the design's own resume guidance at `:194` depends on someone electing to re-run it), can silently drop Backfill rows forever with no lint ever flagging it.

**Mitigation:** Add one sentence to the Scope-limits disclosure block (or the rotation-procedure text) naming that Backfill-Queue integrity is verified only at rotation time, not continuously. Disclosure only, no new lint (which would breach the stated ≤3 ceiling).

### PM-006: No periodic re-verification that the L5 lint stays wired [MAJOR]

**Category:** Process. **Likelihood:** Medium (CI/pipeline refactors are routine over a year; these are low-visibility checks for an obscure log convention, unlike core build/test gates that get noticed immediately if they break). **Severity:** Major (once wiring silently lapses, every downstream guarantee this package attributes to "the lint" — id integrity, cap detection, terminal evidence — reverts to purely advisory).

**Evidence:** `.../feedback-decision-log-convention-design.md:238` assigns wiring as a one-time install acceptance criterion ("owner: the session/engineer executing this install step"); `.../feedback-decision-logs-standards.md:64` discloses the bypass risk ("a `--no-verify` commit skips them") but nowhere is there a recurring check (analogous to the Q3-hook's dated re-assessment or the commit-cadence-anchored graduation/Backfill/install-stall reviews) that the wiring and branch-protection *remain* intact after the initial install. `FEEDBACK-LOG.md:78` (FU.3) already documents a real `--no-verify` bypass in this exact project, evidencing that enforcement erosion is an observed behavior, not a hypothetical.

**Mitigation:** Fold one sentence into the existing "Lint-bypass residual" disclosure naming that wiring persistence is unreviewed after install. No new cadence invented — a disclosure only, consistent with the anti-bloat posture.

---

## Recommendations

**P0 (Critical — MUST fix before acceptance, wording-only, no new machinery):**
- **PM-001-20260706-I6:** Remove/replace the AE-006e "interim backstop" claim in both `feedback-decision-logs-standards.md:28` and the design doc `:180` with an honest statement that no automated cumulative-size backstop exists pre-lint-wiring. Acceptance: no shipped artifact asserts AE-006e covers cap-crossing detection.
- **PM-002-20260706-I6:** Replace `~N sessions` at design doc `:244` with a concrete bound (e.g. "~3 sessions or 30 days"), matching the pattern already used for the Q3 hook. Acceptance: the install-stall trigger is a checkable value, not a placeholder.

**P1 (Major — SHOULD fix, single-sentence disclosures):**
- **PM-003-20260706-I6:** Add a 5th Scope-limits bullet on Segment Index display accuracy (`feedback-decision-logs-standards.md:69`).
- **PM-004-20260706-I6:** Disclose that Backfill-Queue parity is checked only at rotation time, not on an ongoing basis.
- **PM-006-20260706-I6:** Disclose that lint-wiring/branch-protection persistence is unreviewed after install, alongside the existing lint-bypass residual.

**P2 (Minor — MAY fix; acknowledge and monitor):**
- **PM-005-20260706-I6:** Give "at or near cap" a numeric hint (e.g. "within the last ~5 entries").
- **PM-007-20260706-I6:** Directory-level segment-file proliferation at scale — acknowledge as an accepted anti-bloat trade in L1.4 or the Adoption section; no directory-management machinery proposed.
- **PM-008-20260706-I6:** Anchor the "occasional" inline-marker grep-sweep backstop to the same commit-cadence checkpoint every sibling residual already uses.

---

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Negative | PM-002, PM-003, PM-004, PM-006 — an unparameterized trigger and three unreviewed ongoing-integrity gaps (Segment Index display, Backfill-Queue parity, lint-wiring persistence) |
| Internal Consistency | 0.20 | Negative | PM-001 — AE-006e cited as coverage it does not structurally provide |
| Methodological Rigor | 0.20 | Negative | PM-005 — the id-minting mode-switch trigger ("at or near cap") is undefined |
| Evidence Quality | 0.15 | Neutral | Findings concern coverage gaps, not the evidentiary quality of what the package does assert; existing claims are unusually well-cited to real project incidents |
| Actionability | 0.15 | Negative | PM-007, PM-008 — no operational guidance for segment-file scale; no cadence for the inline-marker sweep backstop |
| Traceability | 0.10 | Neutral | Every finding traces to a specific file:line in the shipped artifacts; no traceability defect identified |

**Result:** 2 Critical and 4 Major failure causes identified via prospective hindsight, all closeable by wording/disclosure edits consistent with this package's established zero-new-machinery remediation pattern. **Overall assessment: targeted mitigation required (REVISE)** — the two Criticals are genuine overclaims of coverage (AE-006e, the unbound install-stall trigger) that should not ship as-is; the Majors and Minors are honest-disclosure gaps of the same style already used extensively elsewhere in the package.

---

## What The Package Already Prevents (credit where due)

For balance, per the brief's instruction to check "which [failure paths] the package prevents or honestly discloses": the following 12-months-out failure paths raised during this review were found to be **already adequately prevented or disclosed**, and are not re-raised as findings:
- Concurrent-writer id collisions (single-writer/orchestrator-only-append discipline, disclosed as collision-resistant not collision-proof).
- Silent non-capture with no detector (Q5, explicit PROPOSED-DEFAULT with P-020 visibility).
- Assistant-verbatim transcript-retention dependency (Q1, `[INFERENCE]` disclosed, C3+ escape hatch).
- Secrets/PII persisting in a public-repo log (LOG-M-002 redaction carve-out, modeled on this project's own real `FU.4` precedent).
- Read-side session-start rediscoverability gap (named, with a concrete install-step remedy).
- Cross-log/cross-segment id citation surviving rotation (id-as-join-key design; verified sound).
- Grandfathering of existing un-suffixed bootstrap entries at install (explicit, disclosed procedure).
