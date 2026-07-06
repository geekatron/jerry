# Red Team Report: Feedback/Decision Log Convention Design (Iteration 4)

## Navigation

| Section | Purpose |
|---------|---------|
| [Execution Context](#execution-context) | Header metadata |
| [Summary](#summary) | Overall verdict |
| [Findings Table](#findings-table) | All 8 attack vectors at a glance |
| [Finding Details](#finding-details) | Full write-up for the 1 Critical + 5 Major findings |
| [Recommendations](#recommendations) | P0/P1/P2 countermeasure plan |
| [Scoring Impact](#scoring-impact) | Mapping to the 6 S-014 dimensions |

## Execution Context

**Strategy:** S-001 Red Team Analysis
**Deliverable:** `projects/PROJ-031-cowork-skeleton/design/feedback-decision-log-convention-design.md` + `projects/PROJ-031-cowork-skeleton/design/staging-feedback-logs/{feedback-decision-logs-standards.md, FEEDBACK-LOG.template.md, LLM-DECISION-LOG.template.md, examples-appendix.md, hook-design-note.md}`
**Criticality:** C4 (engagement gate 0.95, user-set)
**Date:** 2026-07-06
**Reviewer:** adv-executor (blind, iteration 4)
**H-16 Compliance:** Not independently verifiable from this blind seat -- the tournament blind protocol restricts this execution from reading `.../adversary/` except its own output file. `[INFERENCE]`: the deliverable's own Revision Changelog (design doc, References to iteration-001/002/003 `remediation-notes.md`) shows RT-/DA-/PM-/CC-/SM-/IN-/CV-/FM-prefixed findings already remediated across 3 prior rounds, so S-003/S-001/etc. have plausibly run before against this package; this executor cannot confirm S-003 ran specifically on the *current* (iteration-4) text state.
**Threat Actor:** A time-pressured or bad-faith LLM operator/session that wants to (a) skip the friction of same-turn logging with zero risk of detection, (b) fabricate or backdate provenance to build a false paper trail, or (c) exploit the single-writer/append-only conventions' lack of *technical* enforcement to bypass them quietly -- while using the design's own MEDIUM-tier, anti-bloat, "descoped-with-disclosure" posture as cover to decline any compensating control, however cheap.

---

## Summary

The package is unusually mature -- three prior adversary rounds have already closed 30+ Critical/Major findings, and nearly every attack surface an ordinary Red Team pass would find (concurrent writers, tampering-vs-append-only, transcript-pointer fragility) is *already* disclosed, often in more than one of the 6 files. That maturity is itself the finding surface for this iteration: this pass hunts for (1) places where a disclosure is *worded* more strongly than its actual technical backing (overclaim-by-wording, not overclaim-by-omission), (2) safety-relevant functions that all quietly resolve to the same undefined "checkpoint," and (3) the one named attack vector (**a hostile/careless session that never logs**) whose only defense is that it is honestly disclosed -- disclosure is not detection, and this residual was resolved unilaterally rather than elevated to the same explicit per-item user ratification (P-020) that Q1-Q4 received. 8 attack vectors identified (1 Critical, 5 Major, 2 Minor) across all 5 MITRE-adapted categories. **Recommendation: REVISE.** Every countermeasure below is wording-only or ratification-elevation-only -- consistent with the package's own anti-bloat doctrine; none require new lint, new hooks, or new files.

---

## Findings Table

| ID | Attack Vector | Category | Exploitability | Severity | Priority | Defense | Affected Dimension |
|----|---------------|----------|----------------|----------|----------|---------|--------------------|
| RT-001-20260706-i004 | "Operational" single-writer discipline has zero technical enforcement | Rule Circumvention | Medium | Major | P1 | Missing | Internal Consistency |
| RT-002-20260706-i004 | Backfill dates are self-attested; the only anti-fabrication signal is voluntary and self-reported by the possible fabricator | Rule Circumvention | Medium | Major | P2 | Partial | Evidence Quality |
| RT-003-20260706-i004 | Undefined "commit-cadence checkpoint" is the sole review mechanism for 4 distinct safety functions | Ambiguity Exploitation | Medium | Major | P1 | Missing | Traceability |
| RT-004-20260706-i004 | Self-proposed graduation lets a session indefinitely avoid H-32/H-33 formal accountability | Boundary Violation | Medium | Major | P1 | Missing | Completeness |
| RT-005-20260706-i004 | Silent non-capture: zero detection anywhere in the package; not elevated to a user-ratified default like Q1-Q4 | Degradation Path | High | **Critical** | **P0** | Missing | Methodological Rigor |
| RT-006-20260706-i004 | Self-declared HARD-vocabulary/ceiling exemption in `hook-design-note.md` sets an unreviewed precedent | Rule Circumvention | Low | Major | P1 | Missing | Internal Consistency |
| RT-007-20260706-i004 | Transcript-pointer scheme depends on Claude Code's own file-naming/retention format staying stable, with no version tag | Dependency Attack | Low | Minor | P2 | Missing | Completeness |
| RT-008-20260706-i004 | Iteration score trajectory (0.64 -> 0.65 -> **0.59**, a regression) mirrors the sibling ADR-convention package's already-diagnosed "non-convergent finding stream," undisclosed here | Degradation Path | Low | Minor | P2 | Missing | Actionability |

---

## Finding Details

### RT-001: "Operational" single-writer discipline has zero technical enforcement [MAJOR]

**Attack Vector:** The design's own words claim the concurrent-writer mitigation has been made real: *"Making it operational (no new machinery): appends happen only in the orchestrating/main context; worker and background agents return feedback/decision candidates via the existing P-003 orchestrator-worker handoff, and the orchestrator serializes the append."* No lint check, tool-permission restriction, or pre-tool gate actually verifies that a worker/background agent refrained from writing to `FEEDBACK-LOG.md` / `LLM-DECISION-LOG.md` directly. Per `agent-development-standards.md` Tool Security Tiers, T2+ worker agents routinely hold `Write`. Nothing in this package (or cross-referenced elsewhere) strips that access for the two log files specifically. A misconfigured, buggy, or simply non-compliant worker agent can append directly, and -- critically -- this bypass produces **no observable symptom** when it happens in isolation (no race, no duplicate id, no lint failure): it looks identical to a compliant orchestrator-mediated append.
**Category:** Rule Circumvention
**Exploitability:** Medium -- requires only that some agent in the pipeline hold Write access and not follow the convention; no adversarial skill needed, just non-compliance (deliberate or accidental).
**Severity:** Major -- the "load-bearing safeguard" (the design's own words) for the entire concurrent-writer risk section is asserted to be "operational" while remaining purely conventional; the immediately following sentence in the same document contradicts the word "operational" ("This discipline -- not lint 2 -- prevents lost writes"), producing an internal-consistency gap between the section label and its own content.
**Existing Defense:** Missing. Lint check 2 (id integrity) explicitly does not catch this class ("does not catch a last-write-wins overwrite"), and no other check inspects *which* actor performed an append.
**Evidence:** `design/feedback-decision-log-convention-design.md` L1.1, "Concurrent-writer residual risk" paragraph (the sentence beginning "Making it operational (no new machinery)"); same claim echoed without the word "operational" in `design/staging-feedback-logs/feedback-decision-logs-standards.md` LOG-M-005 ("This discipline -- not lint 2 -- prevents lost writes").
**Dimension:** Internal Consistency
**Countermeasure:** Wording-only, zero new machinery: replace "Making it operational" with "Making it procedural" (or "Making it a stated convention") and add a 4-6 word clause noting no lint or tool-permission check verifies compliance -- consistent with how the very next sentence already hedges ("not the lint"). No new lint, no new tool restriction requested.
**Acceptance Criteria:** The word "operational" (or any synonym implying enforcement) does not appear attached to the single-writer discipline anywhere across the 6 files unless a corresponding lint/tool-permission check is cited by name.

---

### RT-002: Backfill dates are self-attested with a self-reported anti-fabrication signal [MAJOR]

**Attack Vector:** The Backfill mechanism allows an entry to be "appended at the current tail with the next available canonical id" while recording an arbitrary historical `datetime` in the body -- explicitly exempt from the "no gaps" lint by design. The only safeguard against a fabricated or antedated backfill is: *"a backfilled row SHOULD cite at least one independent reference... absent one, flag it (backfilled, unverified)."* This is voluntary and self-administered by the exact party who might have a motive to fabricate a convenient decision timeline (e.g., to make a governance decision look pre-existing rather than retroactively justified). A hostile/careless session simply omits the flag; nothing else checks it.
**Category:** Rule Circumvention
**Exploitability:** Medium -- no technical skill required, only intent, and the record is designed to look ordinary (an unflagged backfill entry is indistinguishable from a corroborated one).
**Severity:** Major -- this directly undermines the provenance integrity the entire LLM-DECISION-LOG exists to provide (per L1.2, hardened decisions graduate into worktracker DECISIONs and ADRs; a fabricated backfilled decision could seed a downstream formal artifact with a false timeline).
**Existing Defense:** Partial -- the SHOULD-flag exists as a norm, but is unverified, self-administered, and carries no consequence for omission.
**Evidence:** `design/feedback-decision-log-convention-design.md`, "Proposed Defaults" section, Backfill mechanics item (e): "a backfilled row SHOULD cite at least one independent reference... absent one, flag it `(backfilled, unverified)`... presence, not veracity — mirrors lint 3."
**Dimension:** Evidence Quality
**Countermeasure:** Wording-only, zero new machinery: invert the default polarity -- every backfilled entry is tagged `(backfilled)` by default in the heading (not only when unverified), and is only dropped once a reference is actually present and named. This makes "no corroboration" the visible default state instead of something the operator must remember to disclose against their own interest.
**Acceptance Criteria:** Template/appendix worked examples show the `(backfilled)` tag applied unconditionally to every backfill-originated entry, removing the self-administered opt-in step.

---

### RT-003: Undefined "commit-cadence checkpoint" is the sole review mechanism for 4 distinct safety functions [MAJOR]

**Attack Vector:** "Commit-cadence checkpoint" is invoked as the trigger point for: (1) staleness review of OPEN/IN-PROGRESS entries, (2) graduation-review of hardened decisions (LOG-M-004), (3) Backfill Queue review/authorization, and (4) install-stall re-assessment -- four functionally different, safety-relevant review actions, all anchored to one undefined term. The design itself concedes: *"a nudge, not a mechanism."* No file in the package names who performs this review, what they check, or what "reviewed" means operationally; it appears to derive informally from FU.3 (a directive about git commit/push cadence for *rollback capability*, not content review), yet is repeatedly repurposed as a content-integrity checkpoint. Because the checkpoint has no defined owner or action, an operator can satisfy the letter of every cross-reference to it ("reviewed at the commit-cadence checkpoint") while performing no actual review of anything.
**Category:** Ambiguity Exploitation
**Exploitability:** Medium -- requires no adversarial effort at all; the ambiguity is self-triggering under ordinary use, since nothing forces a concrete review action to occur.
**Severity:** Major -- 4 distinct safety properties (staleness, graduation, backfill authorization, install-stall) all silently degrade to "whenever someone happens to commit," with no independent verification step, compounded by the single-operator adoption scope (no second reviewer exists to catch a self-certifying operator).
**Existing Defense:** Missing -- explicitly conceded as "a nudge, not a mechanism" in the source text itself.
**Evidence:** `design/feedback-decision-log-convention-design.md` L1.1 ("reviewed for staleness at the existing commit-cadence checkpoint — a nudge, not a mechanism"); L1.2 graduation cadence ("SHOULD be proposed for graduation at the next commit-cadence checkpoint"); Q4 Backfill mechanics ("re-assessed at the same commit-cadence checkpoint as OPEN entries"); Adoption plan step 7 install-stall ("the owner flags the stall at the next commit-cadence checkpoint").
**Dimension:** Traceability
**Countermeasure:** Wording-only, zero new machinery: add one clause naming the owner -- e.g., "the operator, at the same moment they execute the standing commit/push directive (FEEDBACK-LOG FU.3)" -- reusing the existing FU.3 anchor rather than inventing a new mechanism.
**Acceptance Criteria:** Every use of "commit-cadence checkpoint" in the package resolves to a named actor and a concrete action (even if that action is simply "re-read the OPEN/IN-PROGRESS list before running `git commit`").

---

### RT-004: Self-proposed graduation lets a session indefinitely avoid formal accountability [MAJOR]

**Attack Vector:** LOG-M-004's graduation trigger is: "the assistant proposes graduation... the user authorizes." The assistant that made (or helped make) a decision is also the party deciding *whether to propose* that decision for the higher-ceremony worktracker DECISION / H-32 GitHub-parity / H-33 AST-validated lifecycle. The only compensating control is a self-authored `Graduation: deferred — {reason}` note with no maximum deferral bound (unlike the Q3 hook re-assessment trigger, which explicitly carries a "~3 months" calendar bound). A session with reason to avoid formal scrutiny of a decision (e.g., one that would look worse under H-33 AST validation or public H-32 issue visibility) can defer indefinitely, each time writing a plausible-sounding `reason`, with no external forcing function ever tripping.
**Category:** Boundary Violation (crossing between the low-ceremony log and the high-ceremony worktracker/H-32/H-33 boundary can be delayed unilaterally by the same party who benefits from the delay)
**Exploitability:** Medium -- simply not proposing graduation, or citing a vague `reason`, requires no special access.
**Severity:** Major -- this is precisely the boundary the design elsewhere calls load-bearing ("a hardened, work-item-attached decision graduates... so none silently bypasses the H-32/H-33 lifecycle"), yet the only enforcement of "none silently bypasses" is the same undefined checkpoint flagged in RT-003 plus an unbounded deferral note.
**Existing Defense:** Missing -- no calendar bound, no escalation path, no independent trigger comparable to the Q3 hook's 3-month/rotation/incidental-discovery re-assessment triggers.
**Evidence:** `design/feedback-decision-log-convention-design.md` L1.2 ("Graduation-review cadence... a hardened-but-not-yet-graduated item stays visible in the log with a `Reflected in:` placeholder... one left pending across several checkpoints carries a `Graduation: deferred — {reason}` note"); contrast with the explicit calendar bound given to the Q3 hook re-assessment ("~3 months of wall-clock time... whichever comes first").
**Dimension:** Completeness
**Countermeasure:** Wording-only, zero new machinery: apply the same "whichever comes first" calendar-bound pattern already used for the Q3 hook to graduation deferral (e.g., "deferred past ~3 months or 2 checkpoints escalates the `Graduation: deferred` note into a visible OPEN item in its own right"). Reuses existing pattern; no new file, lint, or hook.
**Acceptance Criteria:** LOG-M-004 names a maximum deferral bound after which a pending graduation is surfaced as its own trackable item rather than remaining an inline note of indefinite duration.

---

### RT-005: Silent non-capture -- zero detection anywhere, and not elevated to explicit ratification [CRITICAL]

**Attack Vector:** This is the task's named vector: *does the design detect or honestly disclose a hostile/careless session that never logs?* It honestly discloses it (L0 scope note (i): "capture stays a MEDIUM (SHOULD) discipline until the fail-open hook... ships"; changelog: "IN-007/RT-008... silent non-capture... INHERENT/monitor (no action)"). But every other integrity mechanism in the package (the 3 lint checks, segment rotation parity check, id-integrity check) operates **only on entries that already exist** in the log. None of them -- and nothing else in the package -- can detect the case where a turn that *should* have produced an entry (per the LOG-M-001 capture triggers) produced none at all. The Q3 hook (`Stop`-based reminder) is the one mechanism designed to catch this, and it is explicitly deferred to a separate, not-yet-approved gate. Until it ships (an open-ended timeline: "Ship the hook inside the v1 install" was explicitly the rejected alternative), a hostile or careless session bypasses **100% of the deliverable's stated purpose** ("so that we don't lose feedback") with **zero observable trace** -- not a lint failure, not a diff anomaly, not a session-start signal (the install-step 3 fix wires *reading* existing entries at session start; it does nothing for entries that were never written). Compounding this: Q1-Q4 are each individually elevated to an explicit user-ratified PROPOSED-DEFAULT under P-020 ("Only questions that change the design are listed... each still requires explicit user ratification"), yet this residual -- arguably more consequential than at least Q2 (the `scope: framework` tag) -- was resolved unilaterally by the adversary-remediation process as "INHERENT... no action," never surfaced to the user as a Q5 for the same explicit, per-item sign-off the other four received.
**Category:** Degradation Path (per the template's own definition -- "conditions under which the deliverable's protections erode over time... knowledge loss" -- this is the purest instance of that category: the protection erodes to zero the moment attention lapses, with no compensating signal)
**Exploitability:** High -- the "attack" is doing nothing; no adversarial skill, no timing, no technical access required. It is also the single most likely real-world failure mode given the package's own admission that the LOG-M-001..006 rules receive "no L2 per-prompt re-injection... more context-rot-vulnerable than a HARD rule."
**Severity:** Critical -- per the S-001 severity definition ("would invalidate the deliverable or allow complete bypass of its protections"), this is a complete, undetectable bypass of the deliverable's entire stated purpose, not a partial weakening.
**Existing Defense:** Missing (honestly disclosed as missing, which is creditable, but disclosure is not detection, and disclosure alone does not change the severity classification per the Red Team template's severity criteria, which key off exploitability/impact, not off whether the gap is confessed).
**Evidence:** L0 scope note (i), `design/feedback-decision-log-convention-design.md` line ~30; "no L2 per-prompt re-injection" disclosure, `design/staging-feedback-logs/feedback-decision-logs-standards.md` L5-lint section preamble; Q1-Q4 individual-ratification framing, design doc "Proposed Defaults (Pending Ratification)" section header; Revision Changelog v5 entry listing "IN-007 (silent non-capture)" under "INHERENT/monitor (no action)".
**Dimension:** Methodological Rigor
**Countermeasure:** Two wording/process-only changes, zero new machinery: (1) Elevate this residual to an explicit **Q5 PROPOSED-DEFAULT** in the "Proposed Defaults (Pending Ratification)" table, worded as plainly as Q1-Q4 (e.g., "Q5: Accept that, until the Q3 hook ships, no mechanism detects a turn that should have been logged but wasn't -- capture is entirely self-policed"), so the user ratifies (or rejects) this specific residual with the same visibility as the other four, rather than it being resolved silently inside an adversary-remediation changelog line. (2) State the gap with the same directness as the "verbatim wins" rule in the L0 executive summary itself, not only in a changelog entry three rounds deep.
**Acceptance Criteria:** A Q5 row exists in the Proposed Defaults table naming this exact residual, and the L0 executive summary states in one direct sentence (not an inference from a scope-note aside) that no detection mechanism exists for missed captures pre-Q3.

---

### RT-006: Self-declared HARD-vocabulary/ceiling exemption sets an unreviewed precedent [MAJOR]

**Attack Vector:** `hook-design-note.md` opens with: *"the MUST / MUST NOT below specify code-implementation contracts for the (separately gated) hook script — not Jerry HARD-rule-tier governance. They are exempt from the MEDIUM-tier vocabulary discipline the rest of this package observes, and do not count against the 25/25 HARD-rule ceiling."* Per `.context/rules/quality-enforcement.md` Tier Vocabulary table, "MUST, SHALL, NEVER, FORBIDDEN, REQUIRED, CRITICAL" are, by definition, HARD-tier vocabulary; the ceiling mechanism, exception process, and 3-family derivation in that same SSOT do not carve out a "code-implementation contract" exemption class anywhere this executor can find cross-referenced. This document invents and self-grants that exemption in a footnote, for itself, with no citation to an SSOT provision that authorizes it. The current instance is low-risk in isolation (the hook is design-only, not shipped, gated separately) -- but the *pattern* is the risk: it is a working example any future design note can copy verbatim to justify sprinkling HARD-tier language for its own "internal contracts" while declaring itself out of ceiling scope, which is exactly the kind of governance loophole that would quietly erode the 25/25 ceiling's stated purpose (bounding cognitive load and L2 token budget) without ever tripping the ceiling-exception ADR process defined for that purpose.
**Category:** Rule Circumvention
**Exploitability:** Low today (requires someone to author a follow-on design note copying the pattern), but the barrier to copying it is trivial -- it is one paragraph, already written, ready to paste.
**Severity:** Major -- this is the one place in an otherwise carefully MEDIUM-tier-disciplined 6-file package (LOG-M-001..006 are consistently "SHOULD") where HARD-tier words appear, justified by a self-authored rather than SSOT-cited exemption -- an internal-consistency gap in a package that elsewhere holds itself to unusually strict tier discipline.
**Existing Defense:** Missing -- no SSOT citation, no C4 ADR, no ceiling-exception tracking entry for this usage.
**Evidence:** `design/staging-feedback-logs/hook-design-note.md` lines 1-4 (the "Vocabulary note" blockquote); contrast with `.context/rules/quality-enforcement.md` "Tier Vocabulary" and "HARD Rule Ceiling Exception Mechanism" sections, neither of which defines a code-contract exemption class.
**Dimension:** Internal Consistency
**Countermeasure:** Wording-only, zero new machinery: replace the capitalized "MUST / MUST NOT" in the hook-note's guardrail bullets with non-normative phrasing ("is required to" / "is not permitted to", or lowercase "must" as plain English rather than a governance keyword), which removes the need for any exemption claim at all -- the simplest anti-bloat-consistent fix. Alternatively, if a genuine SSOT basis for a code-contract exemption exists, cite the specific clause instead of asserting it unsupported.
**Acceptance Criteria:** Either the capitalized HARD-tier keywords no longer appear in `hook-design-note.md`, or the exemption claim cites a specific quality-enforcement.md provision by name.

---

## Recommendations

**P0 (Immediate -- MUST mitigate before acceptance):**
- **RT-005** -- Add an explicit Q5 PROPOSED-DEFAULT for the silent-non-capture residual (same per-item P-020 ratification treatment as Q1-Q4); state the gap directly in the L0 executive summary. Zero new machinery.

**P1 (Important -- SHOULD mitigate):**
- **RT-001** -- Replace "operational" with "procedural" (or equivalent) for the single-writer discipline claim; note the absence of a lint/tool-permission backstop in the same sentence.
- **RT-003** -- Name an owner and concrete action for "commit-cadence checkpoint" (reuse the existing FU.3 anchor).
- **RT-004** -- Apply the existing Q3-hook-style calendar bound ("~3 months / N checkpoints, whichever comes first") to graduation deferral.
- **RT-006** -- Remove capitalized HARD-tier vocabulary from `hook-design-note.md`, or cite the specific SSOT clause authorizing the claimed exemption.

**P2 (Monitor -- MAY mitigate):**
- **RT-002** -- Flip the backfill "(backfilled, unverified)" flag to default-on (`(backfilled)` applied unconditionally, dropped only once corroborated) rather than a self-administered opt-in.
- **RT-007** -- Add one sentence distinguishing the transcript-pointer scheme's dependency on Claude Code's file-naming/retention *format* staying stable from the already-disclosed retention-*duration* risk (IN-006).
- **RT-008** -- Add a one-line cross-reference in the Revision Changelog acknowledging the FU.1-documented "non-convergent finding stream" risk (from the sibling ADR-convention package, same project) as a known, applicable process risk for this tournament too.

---

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Negative | RT-004, RT-007: graduation deferral and transcript-pointer format dependency leave governance/dependency surfaces open-ended |
| Internal Consistency | 0.20 | Negative | RT-001, RT-006: "operational" contradicts the sentence beside it; HARD-tier vocabulary appears in an otherwise strictly MEDIUM-tier-disciplined package |
| Methodological Rigor | 0.20 | Negative | RT-005: the one mechanism (Q3 hook) that would detect the package's single most consequential failure mode is deferred, and the residual was resolved without the same rigor (explicit per-item ratification) applied to Q1-Q4 |
| Evidence Quality | 0.15 | Negative | RT-002: backfill provenance integrity rests on a self-administered, unverified flag |
| Actionability | 0.15 | Neutral-to-Negative | RT-008: countermeasures above are concrete and immediately actionable (positive), but the package's growing hedge-density (evidence: 3 prior remediation rounds, each adding disclosure text) is itself trending toward reduced maintainability |
| Traceability | 0.10 | Negative | RT-003: 4 distinct safety functions trace to one undefined "checkpoint" with no named owner |

**Overall assessment:** Targeted remediation required (not major rework). All 8 findings close via wording, ratification-elevation, or default-polarity changes -- no new lint, hook, file, or subsystem is requested, consistent with the package's own anti-bloat doctrine. RT-005 (Critical) is the one finding this reviewer weighs as blocking: not because silent non-capture is undisclosed (it is disclosed, credibly and repeatedly), but because a C4/0.95-gated deliverable whose entire purpose is "so we don't lose feedback" should put its one total-bypass residual in front of the user for the same explicit, individually-ratified decision that Q1-Q4 already receive, rather than resolving it internally as an accepted trade.

---

*Strategy Version: S-001 v1.0.0 template*
*Blind protocol: adversary/ directory not read except this file; ux/, revision-notes.md, research file, and both live bootstrap logs read as permitted corroborating context.*
*Reviewer: adv-executor*
