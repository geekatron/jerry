# Pre-Mortem Report: Feedback & Decision Log Convention (PROJ-031, iteration-3)

**Strategy:** S-004 Pre-Mortem Analysis
**Deliverable:** `design/feedback-decision-log-convention-design.md` + `design/staging-feedback-logs/{feedback-decision-logs-standards.md, FEEDBACK-LOG.template.md, LLM-DECISION-LOG.template.md, examples-appendix.md, hook-design-note.md}`
**Criticality:** C4 (engagement gate 0.95, user-set)
**Date:** 2026-07-06
**Reviewer:** adv-executor (S-004, iteration-3, blind protocol — did not read other adversary/ findings)
**H-16 Compliance:** CONFIRMED structurally — `adversary/iteration-003/s-003-findings.md` exists in the iteration-3 directory (path observed via directory listing only; content NOT read per this task's blind protocol, which forbids reading any file under `adversary/` except this agent's own output).
**Failure Scenario:** It is 2027-07-06 (12 months out). The FEEDBACK-LOG/LLM-DECISION-LOG convention was ratified and installed, but by month 6 nobody was reliably maintaining it: the two bootstrap logs still show unreviewed Backfill Queue rows from the 2026-07 launch window, at least one segment sits well past its rotation cap because the flag was never acted on, a duplicate/gap in the canonical id sequence went unnoticed for weeks, and three "IN-PROGRESS" feedback items from the original design review were never graduated or closed. The convention exists on disk but has quietly stopped doing the one job it was built for: guaranteeing that captured feedback and decisions survive.

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Overall assessment and recommendation |
| [Findings Table](#findings-table) | All PM-NNN findings at a glance |
| [Finding Details](#finding-details) | Expanded Critical/Major findings with evidence |
| [What the Package Already Prevents/Discloses](#what-the-package-already-preventsdiscloses) | Honest accounting per P-022 |
| [Recommendations](#recommendations) | P0/P1/P2 mitigation plan |
| [Scoring Impact](#scoring-impact) | Dimension-level impact mapping |

---

## Summary

Pre-Mortem generated **6 failure causes** (1 Critical, 4 Major, 1 Minor) across the Process, Technical, Assumption, and External/Resource lenses. The headline finding (PM-001) is not speculative: it is a **live, dated, currently-observable instance** of the "logs abandoned" failure path already beginning inside the very bootstrap artifacts this package ships — the two Backfill Queues (8 rows total, oldest dated 2026-06-29) remain fully unreviewed across at least one already-executed "commit-cadence checkpoint" (the 2026-07-05 FU.3/FU.4 commit+push), directly contradicting the design's own claim that these rows are handled "rather than sitting indefinitely." The remaining findings (PM-002 through PM-005) form a coherent cluster: the package's *only* automated backstops (the ≤3 L5 lint checks) are not yet wired into any enforcement surface in this repository, and this project has **already** demonstrated, in its own commit history narrative, a bypass-and-defer pattern (`--no-verify` + "debt tracked for fix before next commit") that would silently defeat exactly those lint checks once implemented. Three of the four named 12-month failure modes (ids drifted, rotation never happened, logs abandoned) trace to this single point of failure; the fourth (entries missing) is, by contrast, honestly and thoroughly disclosed already (see [What the Package Already Prevents/Discloses](#what-the-package-already-preventsdiscloses)) and generates no new finding here. **Recommendation: REVISE (targeted).** No new machinery is required — per the anti-bloat doctrine already governing this package, PM-001 through PM-005 are addressable by (a) tightening one sentence that overclaims backfill-queue handling, and (b) disclosing — not building — the lint-bypass residual the same way concurrent-writer and transcript-retention residuals are already disclosed elsewhere in this package.

---

## Findings Table

| ID | Failure Cause | Category | Likelihood | Severity | Priority | Affected Dimension |
|----|---------------|----------|------------|----------|----------|--------------------|
| PM-001 | "Commit-cadence checkpoint" review cadence for Backfill Queue is overclaimed — already empirically not occurring | Process | High (observed) | Critical | P0 | Internal Consistency |
| PM-002 | Sole automated backstop (≤3 L5 lint checks) unimplemented + this project has an already-demonstrated bypass-and-defer precedent | Technical/Process | Medium-High | Major | P1 | Methodological Rigor |
| PM-003 | Single-writer discipline is convention-only (no technical lock); a human hand-edit outside the orchestrator path silently reintroduces last-write-wins loss | Assumption | Medium | Major | P1 | Internal Consistency |
| PM-004 | Rotation is 100% manual, triggered only by a lint "flag" that can be suppressed by the same bypass path (PM-002) — no forcing function | Process | Medium | Major | P1 | Completeness |
| PM-005 | Compensating control (Q3 provenance/reminder hook) is unshipped with no committed date; this project's own sibling effort demonstrates Jerry-framework install work here already stalls across multi-iteration passes | External/Resource | Medium | Major | P1 | Actionability |
| PM-006 | Checkpoint-based reviews leave no negative record — "reviewed, nothing to do" is indistinguishable from "never reviewed" after the fact | Process | Medium | Minor | P2 | Traceability |

**Finding ID Format:** `PM-{NNN}` (single execution; no collision risk within this iteration's output file).

---

## Finding Details

### PM-001: Backfill-queue "rather than sitting indefinitely" claim is already contradicted by observable state [CRITICAL]

**Failure Cause:** The design doc states, of the two bootstrap logs' Backfill Queues: *"The 8 rows currently live across the two bootstrap queues are flagged for a one-time authorization decision at the next checkpoint rather than sitting indefinitely."* (`design/feedback-decision-log-convention-design.md:269`, Q4 backfill mechanics, part (c)). The same "commit-cadence checkpoint" is reused as the sole review/escalation trigger for FEEDBACK-LOG staleness nudges (`design/feedback-decision-log-convention-design.md:58`), LOG-M-004 graduation cadence (`design/feedback-decision-log-convention-design.md:137`), and whole-convention install-stall detection (`design/feedback-decision-log-convention-design.md:235`) — four distinct lifecycle-hygiene mechanisms, all keyed to a term that is **never operationally defined** anywhere in the package (no lint checks it, no hook stamps it, no artifact records that a "checkpoint" occurred).

**Category:** Process failure (compounded by an internal-consistency overclaim).

**Likelihood:** High — this is not a projection to 12 months out; it is already true today. Evidence below.

**Severity:** Critical — per this engagement's explicit instruction, overclaimed coverage is Critical, and this is a directly falsifiable, dated claim contradicted by the artifacts the design itself ships alongside.

**Evidence:**
- `FEEDBACK-LOG.md:161-170` — Backfill Queue, 4 rows, dated 2026-06-30, 2026-07-02 (×2), 2026-07-05. All rows remain in raw candidate form; none has been promoted or explicitly declined.
- `LLM-DECISION-LOG.md:72-81` — Backfill Queue, 4 rows, dated 2026-06-29, 2026-06-30, 2026-07-02 (×2). Same state.
- `FEEDBACK-LOG.md:71-81` (FU.3, Disposition) — a "commit-cadence checkpoint" event **did already occur**: "First execution 2026-07-05: commits `518c6556` (178-file PROJ-031 corpus) + `8ea94fc6` (dependency vulnerability fixes) pushed to `origin/feat/proj-030-skeleton-branch`." This is the standing directive's own first execution — i.e., a concrete instance of "the next checkpoint" that the Q4 language promises will carry a backfill authorization decision.
- Today's system date is 2026-07-06 (one day, and at least one further round of adversary work, after that checkpoint) — the 8 rows are unchanged, per the read of both files performed for this report.

**Dimension:** Internal Consistency (0.20) — primary; Evidence Quality (0.15) — secondary, since the claim is presented as settled design rather than as an open, unverified aspiration.

**Mitigation:** Reword the Q4 sentence to disclose rather than claim: e.g., *"...are candidates for a one-time authorization decision at a future checkpoint; as of this writing [{date}], no checkpoint has yet actioned them — this is disclosed, not silently assumed away."* Alternatively/additionally, stop overloading one undefined term for four distinct mechanisms: give each lifecycle-hygiene trigger (staleness, graduation, backfill, install-stall) an explicit, checkable definition of what a "checkpoint" is (e.g., "the FU.3 commit-push directive" specifically, with an explicit note that occurrence of a commit does **not** by itself guarantee the review step was performed — the review is a separate, currently-unenforced human action).

**Acceptance Criteria:** The design doc no longer asserts that backfill/staleness/graduation reviews are occurring at checkpoints without also disclosing that (a) "checkpoint" has no operational definition and (b) the demonstrated first checkpoint did not perform the promised review. This can be closed by wording changes alone (anti-bloat compliant — no new machinery required).

### PM-002: Sole automated backstop is unimplemented, and this project already has a bypass-and-defer precedent [MAJOR]

**Failure Cause:** The ≤3 L5 lint checks (nav-table+cap, id-integrity, terminal-evidence — `design/staging-feedback-logs/feedback-decision-logs-standards.md:62-67`) are the package's *only* automated defense against two of the four named 12-month failure modes ("ids drifted" via check 2; "rotation never happened" via check 1's cap-crossing flag). The Adoption plan commits to "implement and wire the ≤3 L5 lint checks into the existing CI/lint pipeline... acceptance: all three checks run pre-commit and in CI" (`design/feedback-decision-log-convention-design.md:229`) — this is a **future, unimplemented promise**, not a shipped control. Separately, and concretely, this exact project has already exercised a bypass-and-defer pattern against its existing convention checks: *"Execution surfaced and fixed two real gates: 10 pip-audit vulnerabilities... and 24 doc-convention test failures on the new corpus... committed `--no-verify` once, disclosed in the commit message; debt tracked for fix before next commit"* (`FEEDBACK-LOG.md:78`, FU.3 Disposition). Whether that debt was actually cleared "before next commit" is not verifiable from the artifacts available to this review.

**Category:** Technical failure (unimplemented control) compounding a Process failure (demonstrated bypass precedent).

**Likelihood:** Medium-High — the bypass mechanism (`git commit --no-verify`) is a standard, always-available escape hatch; this project has used it at least once already for a comparable "doc-convention" check class.

**Severity:** Major — this does not invalidate the design (a genuinely stronger design still cannot force humans to run lint), but it means the design's implicit claim of an automated backstop is weaker in practice than the "≤3 lint checks" framing suggests, and this repo's CI configuration (`.github/workflows/ci.yml`) currently has no wired-in markdown/nav-table/doc-convention job — the pytest-based check that produced "24 doc-convention test failures" was, per the same FU.3 note, bypassable at the commit layer regardless of whether CI later re-runs it.

**Evidence:** `design/feedback-decision-log-convention-design.md:229` (future promise, not yet built); `FEEDBACK-LOG.md:78` (demonstrated bypass, this project); `.github/workflows/ci.yml` (repo-wide grep for `doc-convention`/`markdown-navigation`/`nav.table`/`H-23` returned zero matches — `[INFERENCE]`: no CI job currently enforces this class of check in a way independent of local hooks; the design's own install step has not landed yet).

**Dimension:** Methodological Rigor (0.20) — primary; Traceability (0.10) — secondary (the "debt tracked for fix before next commit" claim is itself unverified from the artifacts in scope).

**Mitigation:** Add one disclosure sentence to the lint section (`feedback-decision-logs-standards.md` L5 Lint) analogous to the existing concurrent-writer/last-write-wins disclosure: the lint is a backstop, not a guarantee, and is only as strong as its CI wiring — a locally-bypassed commit is only caught if CI is both wired to run these specific checks **and** required (branch-protected) before merge; neither is confirmed at install time. No new machinery — wording only.

**Acceptance Criteria:** Lint section explicitly states the bypass residual (mirrors the existing "not a guarantee" framing already used for LOG-M-005's concurrent-writer risk), and the install work item's acceptance criteria (`design/feedback-decision-log-convention-design.md:229`) additionally requires confirming branch-protection/required-status-check wiring, not just "checks run... in CI."

### PM-003: Single-writer discipline has no technical lock; a direct human hand-edit silently reintroduces the disclosed "rare" loss case [MAJOR]

**Failure Cause:** LOG-M-005 states the single-writer-per-log discipline is what prevents last-write-wins loss, "not the lint" (`design/staging-feedback-logs/feedback-decision-logs-standards.md:27`), and the design's L1.1 concurrent-writer analysis frames the residual as scoped to *"parallel/background agents"* racing (`design/feedback-decision-log-convention-design.md:74`). But the actual mechanism enforcing single-writer status is "appends happen only in the orchestrating/main context" — a **behavioral convention**, not a file lock, permission gate, or CI check. Nothing in the package prevents a human operator (or, on a public repo, a future contributor) from opening `FEEDBACK-LOG.md` in an editor and appending or editing directly, entirely outside any orchestrator/agent path. This is not a hypothetical for this exact package: the bootstrap logs already show direct evidence of ad hoc edits made outside the described append-only workflow (e.g., the "user label" → "alias" heading-rename adoption action explicitly planned for install time, `design/feedback-decision-log-convention-design.md:230`, is itself a bulk rewrite of existing entries).

**Category:** Assumption failure — the design's residual-risk scoping (background agents only) is narrower than the actual attack surface (any direct file edit).

**Likelihood:** Medium — direct hand-edits of a markdown log are a low-friction, high-plausibility action, especially for a public open-source repository whose adoption profile is explicitly out-of-scope for multi-writer teams (`feedback-decision-logs-standards.md:59`) yet whose repository itself has no technical barrier to a second human editing the file.

**Severity:** Major — the loss mode this reintroduces (silent last-write-wins) is explicitly the one the id-integrity lint *cannot* catch (`feedback-decision-logs-standards.md:66`), so this is not a redundant risk — it is the single named gap in the lint's coverage, reachable by a path the design did not scope for.

**Evidence:** `design/staging-feedback-logs/feedback-decision-logs-standards.md:27` ("this, not lint check 2... is what prevents lost writes"); `design/feedback-decision-log-convention-design.md:74` (residual scoped to "parallel/background agents"); `design/feedback-decision-log-convention-design.md:230` (planned bulk heading-rewrite at install, itself a non-orchestrator edit path, evidencing that direct file edits to these logs are already an anticipated/normal operation, not an edge case).

**Dimension:** Internal Consistency (0.20).

**Mitigation:** Widen the disclosed scope of the concurrent-writer residual from "background/worker agents" to "any writer bypassing the orchestrator append path, human or agent" — this is a one-clause wording change, not new machinery, and is consistent with the anti-bloat doctrine already applied elsewhere in this package.

**Acceptance Criteria:** L1.1's concurrent-writer disclosure and LOG-M-005 both name direct human hand-edits (not only background agents) as within the same disclosed residual.

### PM-004: Rotation has no forcing function beyond a lint flag that shares PM-002's bypass path [MAJOR]

**Failure Cause:** Segment rotation is explicitly "operator/assistant-driven" (`design/feedback-decision-log-convention-design.md:190`) and triggered only by lint check 1 flagging the ACTIVE file once it crosses ~800 lines / ~50 entries (`feedback-decision-logs-standards.md:65`). There is no independent mechanism (e.g., a hard file-size guard, a second reminder path not gated on the same lint run) forcing rotation once flagged. If the same commit that crosses the cap is committed with `--no-verify` (PM-002's demonstrated precedent), the flag never surfaces, and the ACTIVE file continues growing past the threshold the entire FU.5 mechanism exists to prevent — silently re-creating the ~25k-token truncation failure this package's own PM-001 (design doc's internal citation, not this report's PM-001) was written to solve.

**Category:** Process failure, directly downstream of PM-002.

**Likelihood:** Medium — requires the cap-crossing commit specifically to be the one where lint is bypassed; plausible but not certain.

**Severity:** Major — if it occurs, it defeats the single most load-bearing mechanism in the entire package (segment rotation exists specifically because an unbounded log "would re-create the context-rot Jerry exists to solve," `design/feedback-decision-log-convention-design.md:170`).

**Evidence:** `design/feedback-decision-log-convention-design.md:190` ("sealing stays operator/assistant-driven because it is a git-visible content operation"); `feedback-decision-logs-standards.md:65` (lint 1 is the only cap-crossing detector).

**Dimension:** Completeness (0.20).

**Mitigation:** Disclosure-only fix: note in L1.4 that cap-crossing detection depends entirely on the lint actually running, and that a bypassed commit at the exact crossing point defeats it — this mirrors the honesty already applied to the last-write-wins gap in LOG-M-005. No new hook or lint is required to close this as a disclosed (not silent) residual.

**Acceptance Criteria:** L1.4 or the L5 Lint section names this dependency explicitly.

### PM-005: Compensating control (Q3 hook) has no committed ship date, and this project has direct precedent for install stalls [MAJOR]

**Failure Cause:** The Q3 provenance/reminder hook — repeatedly cited as the intended remedy for the package's MEDIUM-tier (no L2 reinjection) enforcement weakness (`design/feedback-decision-log-convention-design.md:219`) — is "designed in v1... but shipped as a separate gated change" (`design/feedback-decision-log-convention-design.md:266`) with no committed date, only a disjunctive re-assessment trigger ("first segment rotation, OR... fixed cadence checkpoint..., OR the first time a missed capture is discovered incidentally," `design/feedback-decision-log-convention-design.md:232`) that itself depends on the same undefined "checkpoint" concept flagged in PM-001. This project's own text supplies direct precedent that install/remediation work here can stall for extended, multi-iteration periods: the sibling ADR-convention effort "needed a multi-iteration subtraction pass" (`design/feedback-decision-log-convention-design.md:235`, install-stall paragraph, citing its own precedent) and required 8 total tournament rounds before the design doc's own changelog was written.

**Category:** External/Resource failure (dependent on future prioritization, staffing/attention, and a precedent-evidenced stall pattern in this codebase).

**Likelihood:** Medium.

**Severity:** Major — while explicitly disclosed as a risk in principle, the *compounding* effect (PM-001's undefined checkpoint governs when the hook decision is even revisited) means the stated "re-assessment trigger" is weaker than it reads at first pass.

**Evidence:** `design/feedback-decision-log-convention-design.md:219, 232, 235, 266`.

**Dimension:** Actionability (0.15); Traceability (0.10).

**Mitigation:** Add a concrete, calendar-bound fallback to the disjunctive re-assessment trigger (e.g., "or N months of wall-clock time, whichever comes first") so the hook decision cannot be deferred purely by the absence of a rotation/discovery/checkpoint event. Wording-only change; no new machinery.

**Acceptance Criteria:** Q3's re-assessment trigger includes at least one time-bound (not only event-bound) condition.

### PM-006: Checkpoint reviews leave no negative record [MINOR]

**Failure Cause:** Because "reviewed, nothing to do" and "never reviewed" both look identical (no entry, no log line) after the fact, a future auditor 12 months out cannot distinguish diligence from neglect for any of the checkpoint-gated mechanisms (staleness, graduation, backfill, install-stall).

**Category:** Process failure (audit-trail gap).

**Likelihood:** Medium. **Severity:** Minor — quality-of-life/auditability gap, not a data-loss path.

**Dimension:** Traceability (0.10).

**Mitigation (P2, monitor only — no action required to accept this release):** if the recurrence of PM-001-class issues becomes evident in practice, consider a one-line "Last reviewed: {date}" stamp in the Segment Index or Backfill Queue header — deliberately not proposed as a required fix now, consistent with the anti-bloat doctrine (this is a MAY, not a SHOULD).

---

## What the Package Already Prevents/Discloses

Per P-022, an honest pre-mortem must credit what already works, not just what fails. Of the four failure paths named for this review:

- **"Entries missing"** — thoroughly and honestly disclosed already: opportunistic inline-doc harvest with a named CB-05 partial-read blind spot, a documented `grep` sweep backstop, and an explicit statement that the keyword-heuristic Stop reminder is "a reminder trigger, not a classifier" that "cannot catch every phrasing" (`hook-design-note.md:35`). No new finding generated — this is a model instance of descoped-with-disclosure, not an omission.
- **"Ids drifted" (pure numbering, not the loss-of-writes case)** — the logger-assigned canonical-id scheme plus lint check 2 is a sound, minimal design for the common case (duplicate/gap detection); the one gap (last-write-wins) is honestly named as out of the lint's coverage already (`feedback-decision-logs-standards.md:66`). PM-002/PM-003 above extend this disclosure rather than contradict it.
- **"Rotation never happened" (mechanism design, as opposed to enforcement)** — the cap math (2.5x Read-window headroom, 2-3x under the truncation point), stable-ACTIVE-name design, and required parity check are genuinely well-reasoned and evidence-based; PM-004 is narrowly about the *enforcement* gap, not the mechanism's design quality.
- **"Logs abandoned" (MEDIUM-tier/no-L2-reinjection)** — already disclosed at the framework level (`design/feedback-decision-log-convention-design.md:219`); PM-001 is a *sharper, dated, and already-observable* instance of this same disclosed category, not a new category of risk.

---

## Recommendations

**P0 (MUST mitigate before acceptance):**
- PM-001: Reword the Q4 backfill-queue claim to disclose current unreviewed state rather than assert non-indefinite handling; either define "commit-cadence checkpoint" operationally or stop presenting it as a review mechanism for four distinct lifecycle events without evidence any of the four is occurring.

**P1 (SHOULD mitigate):**
- PM-002: Add a lint-bypass disclosure sentence (mirrors existing last-write-wins disclosure style) + tie the install acceptance criteria to confirming CI is both wired AND required (branch-protected).
- PM-003: Widen the concurrent-writer disclosure to cover direct human hand-edits, not only background/worker agents.
- PM-004: Disclose that cap-crossing detection depends entirely on lint execution, sharing PM-002's bypass exposure.
- PM-005: Add a calendar-bound fallback condition to the Q3 hook re-assessment trigger.

**P2 (MAY mitigate; acknowledge risk):**
- PM-006: Optional "Last reviewed" stamp — defer unless PM-001-class drift recurs in practice.

All six mitigations are **wording/disclosure changes**. None requires new lint, new hooks, new files, or new subsystems — consistent with the anti-bloat doctrine this package already applies successfully to its prior four review rounds.

---

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Negative | PM-004: rotation enforcement gap is an unaddressed completeness hole in an otherwise well-specified mechanism. |
| Internal Consistency | 0.20 | Negative | PM-001 (overclaim directly contradicted by observable state), PM-003 (residual scope narrower than actual attack surface). |
| Methodological Rigor | 0.20 | Negative | PM-002: the described enforcement backstop is not yet real, and a bypass precedent already exists in this project. |
| Evidence Quality | 0.15 | Negative | PM-001: the specific claim cited is falsified by the same corpus the design doc treats as supporting evidence elsewhere. |
| Actionability | 0.15 | Neutral-to-Negative | PM-005: mitigation exists (calendar fallback) but is not yet specified; PM-006 has an explicit MAY-only mitigation (no action forced). |
| Traceability | 0.10 | Negative | PM-002, PM-006: unverifiable claims ("debt tracked," "reviewed at checkpoint") with no artifact confirming resolution. |

**Result:** 1 Critical and 4 Major failure causes identified via prospective hindsight, all closable by wording/disclosure changes with zero new machinery. The Critical finding (PM-001) is unusual among pre-mortems in that it required no imagination — the failure path is already partially visible in the dated state of the bootstrap artifacts as of this review (2026-07-06). Recommend REVISE (targeted, low-cost) rather than REJECT: the underlying design remains sound and minimal; the gap is entirely in a small number of overclaiming or under-disclosing sentences layered on top of it.

---

*Strategy: S-004 Pre-Mortem Analysis · Template: `.context/templates/adversarial/s-004-pre-mortem.md` · Iteration: 3*
