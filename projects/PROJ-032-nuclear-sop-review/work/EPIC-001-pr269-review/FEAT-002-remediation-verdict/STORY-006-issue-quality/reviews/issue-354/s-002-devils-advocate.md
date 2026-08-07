# Devil's Advocate Report: GitHub Issue #354 (BUG-005 / REM-05, H-36 governance ruling)

**Strategy:** S-002 Devil's Advocate
**Deliverable:** `snapshots/final/issue-354.md` (live text of geekatron/jerry issue #354)
**Criticality:** C4 (tournament)
**Date:** 2026-08-07
**Reviewer:** adv-executor (S-002)
**H-16 Compliance:** S-003 Steelman precedes this execution per tournament group ordering (self-refine -> steelman -> challenge); confirmed by orchestration protocol, not independently re-verified by this agent.

## Summary

3 counter-arguments (0 Critical, 3 Major, 1 Minor). Every specific claim checked against the remediation register, verdict, and commit evidence held up — no invented facts, no wrong severity. The findings are about what the text *omits or leaves unresolved for the reader*: an unresolvable worktracker path, an asserted-but-undisclosed second date, and a one-sided framing of the owner's actual decision. Recommend REVISE (targeted, non-structural fixes).

## Findings Table

| ID | Finding | Severity | Evidence | Affected Dimension |
|----|---------|----------|----------|--------------------|
| S-002-01 | Worktracker path unresolvable without the branch qualifier given to its sibling reference | Major | Issue line 10: `projects/PROJ-032-nuclear-sop-review/work/BUG-005-h36-governance-ruling` vs. same sentence's `remediation-register.md` reference, which explicitly states `on branch feat/proj-032-nuclear-sop-review` | Traceability |
| S-002-02 | "different anchor dates" asserted, never disclosed | Major | Issue text: "use different anchor dates"; register REM-05 G2: actual anchors are "Phase 1 delivery" (undated milestone) vs. "skill registration (2026-06-15)" — issue's own header presents only 2026-06-15 as *the* deadline | Completeness |
| S-002-03 | Eng-team precedent framed as resolving the decision outright, omitting the consequence of the untaken branch | Major | Issue: "adopting that reading... resolves this issue outright"; verdict pr269-verdict.md states the alternative ruling ("revert to 3-hop... eliminate it") removes sop-verifier entirely — that stake is absent from the issue | Internal Consistency / Actionability |
| S-002-04 | Three assignees, but the issue itself says the decision needs "owner authority" — unclear which assignee that is | Minor | Issue header: "Assignees: geekatron victorlau1 malcolm-x-evo"; body: "requires owner authority, not maintainer or contributor alone" | Actionability |

## Finding Details

### S-002-01: Worktracker path unresolvable [MAJOR]

**Claim Challenged:** "Worktracker: `projects/PROJ-032-nuclear-sop-review/work/BUG-005-h36-governance-ruling` (register section REM-05)."
**Counter-Argument:** This path only exists on branch `feat/proj-032-nuclear-sop-review` (confirmed: the file resolves at `.../BUG-005-h36-governance-ruling/BUG-005-h36-governance-ruling.md` on that branch; the PROJ-032 review project is not on `main`). The same sentence's next reference (`remediation-register.md`) is careful to state "on branch `feat/proj-032-nuclear-sop-review`" — but the worktracker path gets no such qualifier, and also drops the filename. An external contributor who clones `main` (the normal path for a PR reviewer) gets a 404 on the worktracker link with no signal why.
**Impact:** Reader loses a reference silently; asymmetric treatment of two adjacent paths in the same sentence looks like an oversight rather than intent.
**Dimension:** Traceability
**Response Required:** Add the branch qualifier and filename to the worktracker path, matching the treatment already given to `remediation-register.md`.
**Acceptance Criteria:** Sentence reads e.g. "Worktracker: `BUG-005-h36-governance-ruling.md` under `projects/PROJ-032-nuclear-sop-review/work/BUG-005-h36-governance-ruling/` on branch `feat/proj-032-nuclear-sop-review`."

### S-002-02: Undisclosed second anchor date [MAJOR]

**Claim Challenged:** "the file's two fallback instructions contradict each other... use different anchor dates" (with the header quoting only one date, 2026-06-15).
**Counter-Argument:** The issue tells the reader a disagreement exists ("different anchor dates") without giving both sides — the only way to learn the second anchor ("Phase 1 delivery," which is not itself a calendar date) is to open the internal rules file, which violates the mission's zero-internal-context premise. This also slightly overclaims: one "anchor" is an undated milestone, not a date, so "different anchor dates" is imprecise.
**Impact:** An external agent asked to "fix" the contradiction cannot even state what the two options are from this text alone; forces a lookup the issue was supposed to make unnecessary.
**Dimension:** Actionability
**Response Required:** Name both anchors explicitly, e.g.: "one fallback resets on an undated 'Phase 1 delivery' milestone, the other on skill registration — 2026-06-15, already passed."
**Acceptance Criteria:** Both anchor conditions are stated in plain language with no unexplained residual plural ("dates") that isn't backed by two actual dates.

### S-002-03: One-sided framing of the owner's decision [MAJOR]

**Claim Challenged:** "adopting that reading (\"predetermined sequences are not routing re-evaluations\") resolves this issue outright and removes the skill's self-scheduled sunset clause."
**Counter-Argument:** This is accurate as far as it goes (verified against pr269-verdict.md), but it states only the consequence of one ruling. The verdict document is explicit that the real decision is binary: keep 4-hop mode with sop-verifier, **or** revert to 3-hop and eliminate sop-verifier (the skill's independent verification agent) entirely. The issue presents the "adopt eng-team's pattern" branch as the path that "resolves this outright" and never mentions that the other branch removes a safety-checking agent from the skill. For a decision explicitly flagged "requires owner authority," omitting what's actually at stake in the untaken branch nudges the reader toward one answer without full information — the opposite of what a governance-ruling issue should do.
**Impact:** Owner could rule based on an incomplete picture of trade-offs; the framing reads as advocacy for a specific outcome rather than a neutral decision brief.
**Dimension:** Internal Consistency (issue claims to present "the decision to make" but presents only one branch's upside)
**Response Required:** Add one clause stating what the other branch costs, e.g.: "the alternative ruling reverts to 3-hop mode and removes sop-verifier from C3+ execution entirely."
**Acceptance Criteria:** Both branches of the ruling and their consequences are stated, even briefly; the "outright resolves" framing is qualified as one option among (at minimum) two.

## Recommendations

**P1 (Major — should resolve):**
- S-002-01: Add branch + filename to the worktracker path. Acceptance: path resolves identically to the register path's citation style.
- S-002-02: Name both fallback anchors explicitly. Acceptance: no unexplained plural claims remain.
- S-002-03: State the consequence of the untaken branch (removal of sop-verifier). Acceptance: both branches and their stakes are visible in-text.

**P2 (Minor — may resolve):**
- S-002-04: Clarify which assignee(s) hold "owner authority" vs. maintainer/contributor roles, or add one clause noting the ruling must come from whichever assignee has repo-owner authority.

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Negative | S-002-02, S-002-03: second date and second branch's consequence both omitted |
| Internal Consistency | 0.20 | Negative | S-002-03: "outright resolves" framing inconsistent with the issue's own "decision to make" framing |
| Methodological Rigor | 0.20 | Neutral | No procedural or structural defect found |
| Evidence Quality | 0.15 | Positive | Every specific factual claim in the issue checked out against register/verdict/commit evidence |
| Actionability | 0.15 | Negative | S-002-01, S-002-02: reader cannot resolve the worktracker link or the anchor-date claim from the text alone |
| Traceability | 0.10 | Negative | S-002-01: asymmetric branch-qualifier treatment between two adjacent references |

**Result:** No factual fabrication found; findings are entirely about self-containedness and neutral framing for an external, zero-context reader. Targeted revision (3 clauses + 1 path fix) closes all Major findings without restructuring the issue.
