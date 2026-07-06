# Pre-Mortem Report: FEEDBACK-LOG + LLM-DECISION-LOG Convention (Iteration 8, VERIFIED-CRITICALS Protocol)

**Strategy:** S-004 Pre-Mortem Analysis
**Deliverable:** `projects/PROJ-031-cowork-skeleton/design/feedback-decision-log-convention-design.md` + 5 files under `projects/PROJ-031-cowork-skeleton/design/staging-feedback-logs/` (`feedback-decision-logs-standards.md`, `FEEDBACK-LOG.template.md`, `LLM-DECISION-LOG.template.md`, `examples-appendix.md`, `hook-design-note.md`)
**Criticality:** C4 (gate 0.95)
**Date:** 2026-07-06
**Reviewer:** adv-executor (blind, iteration 8)
**H-16 Compliance:** S-003 Steelman output confirmed present for this iteration (`orchestration/fu-log-convention-20260705-001/adversary/iteration-008/s-003-findings.md` exists per directory listing; content not read per this iteration's BLIND PROTOCOL, consistent with the standard tournament sequence S-010→S-003→S-007→S-002→S-004 already exercised in iterations 001-007).
**Failure Scenario:** It is 2027-07-06 (12 months out). The convention has been running unattended across many independent sessions and at least one model swap. An operator asks "what's the status of the framework-feedback item I raised eight months ago?" and the answer cannot be produced with confidence: a background-agent-sourced item never made it into the log, the ACTIVE segment silently grew past its intended cap because no session in the chain knew the threshold, an inline-doc citation resolves to a file that no longer exists at that path, and the convention itself never finished ratification -- it is still "informal," un-installed, and un-enforced by any auto-loaded rule.

## Navigation

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Overall assessment and recommendation |
| [Findings Table](#findings-table) | All findings at a glance |
| [Finding Details](#finding-details) | Expanded Critical/Major findings with evidence |
| [Recommendations](#recommendations) | P0/P1/P2 mitigation plan |
| [Scoring Impact](#scoring-impact) | Mapping to S-014 dimensions |
| [Findings Deliberately Not Raised](#findings-deliberately-not-raised) | Candidate paths considered and excluded as already-disclosed residuals |

---

## Summary

This package is unusually self-aware: across 6 prior tournament rounds plus a Restore pass, it has accumulated an extremely dense set of named, accepted residuals (RT/DA/PM/CC/CV/FM/IN tags) covering nearly every failure path a first-pass pre-mortem would surface (silent non-capture, concurrent-writer races, uncommitted-loss, lint bypass, squash-merge, backfill staleness, segment-index growth). Consistent with the VERIFIED-CRITICALS instruction, this pass reports only paths that are **neither prevented nor already disclosed** anywhere in the package. Four such paths survive scrutiny: two Critical (a cross-document SSOT gap that can cause literal entry loss from background agents, and a missing in-artifact cap threshold that can silently re-create the exact truncation failure the whole design exists to prevent) and two Major (inline-doc provenance staleness, and an escalation asymmetry in the install-stall trigger). None of the four requires new machinery to close; all four are wording/propagation fixes consistent with this package's own anti-bloat doctrine. **Recommendation: REVISE (targeted) -- close PM-001 and PM-002 before acceptance; PM-003/PM-004 SHOULD be closed in the same pass given how cheap the fix is.**

---

## Findings Table

| ID | Failure Cause | Category | Likelihood | Severity | Priority | Affected Dimension |
|----|---------------|----------|------------|----------|----------|--------------------|
| PM-001-iter8 | CP-01 (handoff "file paths only, NEVER inline content") has no documented exception in its own SSOT; a background/worker agent built to the real rule has no basis to inline a feedback candidate | Process | High | Critical | P0 | Internal Consistency |
| PM-002-iter8 | Segment-rotation cap (~50 entries / ~800 lines) exists only in the rule file and design doc -- never in the log template or the live bootstrap log itself | Technical | High | Critical | P0 | Completeness |
| PM-003-iter8 | Inline-doc provenance (`source: inline-doc {path}:{line/anchor}`) has no staleness check; a moved/renamed/deleted source file silently breaks the citation | Technical | Medium | Major | P2 | Traceability |
| PM-004-iter8 | Whole-convention install-stall trigger lacks the "second consecutive deferral flagged explicitly" forcing function that the graduation and Backfill Queue triggers already have | Process | High | Major | P1 | Methodological Rigor |

---

## Finding Details

### PM-001-iter8: CP-01 exception exists only inside this design's own text, not in the SSOT it depends on [CRITICAL]

**Failure Cause:** The convention's core anti-loss mechanism -- "only the orchestrating context appends; workers/background agents return short candidates inline via the handoff" (LOG-M-005) -- is explicitly described, twice, as *"a stated exception to CP-01's file-paths-only preference"* (design doc) and *"a stated exception to CP-01"* (rule file). But CP-01 as actually defined for every agent in the framework carries no such exception:

> `| CP-01 | File paths only in handoffs, NEVER inline content | MEDIUM | Prevents context duplication; receiving agent loads content via Read |`
> -- `.context/rules/agent-development-standards.md:382`

Compare the design's own framing of the exception:
> "(A candidate is a short judgment-bearing text payload returned inline in the handoff's `key_findings`/summary -- a stated exception to CP-01's file-paths-only preference, justified because a 1-3-line candidate does not warrant a separate file plus round-trip; the orchestrator appends it verbatim.)"
> -- `projects/PROJ-031-cowork-skeleton/design/feedback-decision-log-convention-design.md:78`

and the rule file's version:
> "workers (incl. background handoffs) return short candidates inline via the P-003 handoff, appended the same turn (a stated exception to CP-01)."
> -- `projects/PROJ-031-cowork-skeleton/design/staging-feedback-logs/feedback-decision-logs-standards.md:27`

The exception is "stated" only inside this project's own staging documents -- documents that govern nobody's behavior until installed, and even after install do not touch `agent-development-standards.md`. Any worker or background agent implemented against the actual SSOT (the only place CP-01 has authority) sees a flat "NEVER inline content" with no carve-out. Over a 12-month horizon in which the framework's agent roster keeps growing (this very session's context shows dozens of skills/agents authored against exactly this file), the first time a worker/background agent is asked to surface a feedback/decision candidate under this convention, one of two things happens: (a) it inlines the candidate, silently violating the framework's real CP-01 with no textual authorization to point to outside a project-local design doc, or (b) it correctly follows the real CP-01 and does **not** inline the candidate -- and since writing a separate file "does not warrant a separate file plus round-trip" per the design's own reasoning, the candidate has nowhere sanctioned to go and is dropped. Path (b) is a genuine, silent, structural loss of exactly the item this convention exists to capture -- not a hypothetical edge case but the direct consequence of the SSOT never being updated.

**Category:** Process (missing propagation step)
**Likelihood:** High -- justified by (1) FU.2's own stated goal of "leverage background agents so we don't burn through the main context window," meaning this path is not a corner case but a design driver, and (2) `agent-development-standards.md` is the single SSOT for every agent in the framework, so nothing project-local can silently override it for one convention.
**Severity:** Critical -- directly produces the "entries lost" failure this pre-mortem was commissioned to find, and additionally creates a framework-wide precedent problem (a convention that assumes an unratified exception to a global MEDIUM rule).
**Evidence:** `.context/rules/agent-development-standards.md:382` (CP-01, no exception); `design/feedback-decision-log-convention-design.md:78`; `design/staging-feedback-logs/feedback-decision-logs-standards.md:27`.
**Dimension:** Internal Consistency (the two documents make contradictory claims about what CP-01 permits).
**Mitigation:** Add an explicit adoption-plan step (alongside the existing 7 steps in `design/feedback-decision-log-convention-design.md` L2 "Adoption / migration plan") to update `agent-development-standards.md`'s CP-01 row (or add an adjacent footnote/sub-bullet) naming the short-candidate-inline exception for single-writer log-append patterns, cross-referenced from LOG-M-005. This is a one-line SSOT edit, not new machinery.
**Acceptance Criteria:** `agent-development-standards.md` CP-01 entry (or an explicitly linked exception clause in the same table) names the log-candidate-handoff exception; the Adoption plan lists this as an install-time action with an owner, the same way it already tracks the project-workflow.md session-start wiring (Adoption step 3).

---

### PM-002-iter8: The segment-rotation cap threshold is absent from every artifact a session actually reads while appending [CRITICAL]

**Failure Cause:** The entire segment-rotation mechanism (FU.5) exists to prevent the log from silently exceeding the ~2,000-line Read window / ~25k-token truncation point. The specific numeric trigger for that mechanism -- "~50 entries or ~800 lines" -- is defined in exactly two places, both of which are the *design-time* artifacts, not the *runtime* artifact:

> "At the segment cap (~50 entries or ~800 lines) seal the ACTIVE log..." -- `design/staging-feedback-logs/feedback-decision-logs-standards.md:28` (LOG-M-006)
> "**Cap** | Seal the ACTIVE file when it first reaches **~50 entries or ~800 lines**..." -- `design/feedback-decision-log-convention-design.md:195`

The artifact an assistant actually reads and appends to turn after turn -- `FEEDBACK-LOG.template.md` (and, confirmed by direct read, the live bootstrap `projects/PROJ-031-cowork-skeleton/FEEDBACK-LOG.md` itself) -- contains **no cap number anywhere**. `FEEDBACK-LOG.template.md`'s "Log Conventions" section (lines 16-26) and "Segment Index" section (lines 28-36) explain the id/alias mechanism and forward/backward navigation in detail but never state when to rotate. The live bootstrap file's "Log Conventions (bootstrap)" section (`projects/PROJ-031-cowork-skeleton/FEEDBACK-LOG.md:18-22`) likewise carries no cap figure. This is not a 12-months-out hypothetical -- it is the file's state **today**. The rule file that carries the only copy of the number is still staged (not yet installed to `.context/rules/`, per the design's own pending-ratification status), and even after install, this package's own Revision Changelog documents the rule file growing every single round (1,584 -> 1,690 -> 2,150 -> 2,281 words) while staying flagged as a standing over-budget `[USER-DECISION]` -- i.e., it is the kind of artifact a future rule-corpus consolidation pass would target for trimming (this session's own rule corpus shows exactly that pattern already executed repeatedly: H-06, H-08, H-09, H-12, H-21, H-24, H-27-H-30, H-35, H-37 were all retired/folded during EN-001/EN-002 consolidation). If the rule file is ever trimmed, deprioritized, or simply not in a session's context when the log is being appended -- which is the file's literal present state, pre-install -- there is no textual anchor anywhere in the artifact being read that tells the assistant or a human operator that ~50/~800 is the number. The log can grow unbounded, silently re-creating the exact FU.5 truncation failure this whole design was built to solve, with zero in-file warning.

**Category:** Technical (single point of knowledge failure for a load-bearing numeric parameter)
**Likelihood:** High -- confirmed as the *current* state of both the template and the live bootstrap file (not a projection); the rule file's own disclosed over-budget trend increases exposure further over 12 months.
**Severity:** Critical -- directly re-creates the specific failure (context-rot-inducing unbounded growth) that this design exists to prevent, with no fallback signal in the file itself.
**Evidence:** `design/staging-feedback-logs/FEEDBACK-LOG.template.md:16-36` (no cap stated); `projects/PROJ-031-cowork-skeleton/FEEDBACK-LOG.md:18-22` (live file, no cap stated, confirmed by direct read); cap defined only at `feedback-decision-logs-standards.md:28` and `feedback-decision-log-convention-design.md:195`.
**Dimension:** Completeness (the shipped/live artifact is missing a parameter necessary for its own core safety mechanism to function without external context).
**Mitigation:** Add a one-line statement of the numeric cap directly to `FEEDBACK-LOG.template.md` and `LLM-DECISION-LOG.template.md`'s "Segment Index" section (e.g., "Seal this file and start a new segment at ~50 entries or ~800 lines, whichever first -- see rotation walkthrough in `examples-appendix.md`."), and apply the same one-line addition to the live bootstrap `FEEDBACK-LOG.md` / `LLM-DECISION-LOG.md` at the next commit-cadence touch. Zero new machinery -- restating an existing number in a second location.
**Acceptance Criteria:** Both templates and both live bootstrap files state the numeric cap in their own text, independent of whether the rule file is installed, loaded, or later trimmed.

---

## Recommendations

**P0 (Critical -- MUST mitigate before acceptance):**
- **PM-001-iter8:** Add an adoption-plan action to propagate the CP-01 exception into `agent-development-standards.md`'s CP-01 entry (or an adjacent linked clause) before or at install. Acceptance: SSOT text names the exception; a worker/background agent reading only the SSOT can act correctly.
- **PM-002-iter8:** Restate the numeric segment cap (~50 entries / ~800 lines) directly in both templates and both live bootstrap log files. Acceptance: the cap is legible from the log file alone, with no dependency on the rule file being loaded.

**P1 (Important -- SHOULD mitigate):**
- **PM-004-iter8:** Add a "second consecutive deferral flagged explicitly" clause to the whole-convention install-stall trigger in `design/feedback-decision-log-convention-design.md` L2 Adoption section, mirroring the pattern already used for graduation (RT-005, v8 changelog) and the Backfill Queue. Acceptance: the install-stall paragraph names an explicit escalation on the second stall, not only "flag and continue."

**P2 (Monitor -- MAY mitigate; acknowledge risk):**
- **PM-003-iter8:** Add inline-doc path staleness as an explicit 8th item to the already-published L5-Lint "Scope limits" list in `feedback-decision-logs-standards.md` (which currently enumerates seven other non-covered classes, (a)-(g)) so a stale `source: inline-doc` citation is a disclosed, named residual rather than a silent one. A one-sentence addition; no new lint required, consistent with the ≤3-lint ceiling already in force.

---

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Negative | PM-002-iter8: the shipped/live log artifacts are missing the numeric parameter their own core safety mechanism depends on. |
| Internal Consistency | 0.20 | Negative | PM-001-iter8: the design's and rule file's own text asserts an exception to CP-01 that CP-01's actual definition does not carry -- an unresolved cross-document contradiction. |
| Methodological Rigor | 0.20 | Negative | PM-004-iter8: the same document applies a "second-deferral escalation" pattern inconsistently -- present for graduation and Backfill, absent for the install-stall trigger it most needs to guard. |
| Evidence Quality | 0.15 | Negative | PM-003-iter8: inline-doc provenance citations have no mechanism to detect or flag staleness, degrading the evidentiary trail this package otherwise polices tightly (e.g., lint 3's terminal-evidence requirement). |
| Actionability | 0.15 | Negative | PM-001/PM-002: the Adoption/migration plan (7 numbered steps) does not currently include either fix, so the plan as written is not sufficient to close either Critical. |
| Traceability | 0.10 | Negative | PM-001-iter8: the "stated exception to CP-01" claim does not trace to any change in CP-01's own SSOT entry. |

---

## Findings Deliberately Not Raised

Per the VERIFIED-CRITICALS instruction, the following candidate paths were investigated and excluded because they duplicate an already-disclosed residual or an already-closed prior finding (confirmed against `iteration-007/restore-notes.md`, which is the owner's public disposition record, and against targeted searches of the readable iterations 001-006 findings):

- Silent non-capture with no proactive detector -- already an explicit ratified default (Q5).
- Concurrent-writer / worktree-branch merge races -- already disclosed with a "never discard, renumber on collision" merge rule (L1.1).
- Uncommitted-append loss on `git checkout`/`reset` -- already disclosed in the L0 scope note (ii).
- Backfill Queue / graduation review stalling at the shared commit-cadence checkpoint -- already named as an accepted correlated risk ("One shared dependency," L2) with calendar-bound backstops.
- Rule-file token budget over its ~1,500 soft target -- already a standing, explicitly re-ratified `[USER-DECISION]` each round.
- "Operational" single-writer discipline having no technical enforcement -- already raised and closed to "procedural" framing in iteration-004 (RT-001) / propagated in iteration-005 (PM-004/FM-002).
- Read-side gap (a new session not consulting the logs) pre-install -- already disclosed and tied to Adoption step 3.

---

## Execution Statistics
- **Total Findings:** 4
- **Critical:** 2
- **Major:** 2
- **Minor:** 0
- **Protocol Steps Completed:** 6 of 6
