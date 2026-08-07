# Inversion Report: GitHub Issue #354 (BUG-005 / REM-05, H-36 governance ruling)

**Strategy:** S-013 Inversion Technique | **Deliverable:** `snapshots/final/issue-354.md` (~230 words)
**Criticality:** C4 (tournament) | **Date:** 2026-08-07 | **Reviewer:** adv-executor (S-013)
**H-16 Compliance:** N/A for this blind lane (executed as an independent strategy lane per orchestrator instruction, not a sequential C3+ workflow)
**Goals Analyzed:** 4 | **Assumptions Mapped:** 6 | **Vulnerable Assumptions:** 1 (Major)

## Summary

Goal: an external contributor/agent, with zero Jerry-governance context, must be able to understand the H-36 hop-counting question, verify the claims, and locate supporting artifacts from this text alone. Inversion of that goal ("what would guarantee the reader gets lost or acts wrongly?") surfaced one real vulnerability — an inconsistent, branch-qualifier omission on the worktracker path that sits right next to a path that *does* carry a branch qualifier — plus two low-impact jargon/clarity gaps. All substantive factual claims (deadline date, contradiction, missing tracking artifact, eng-team precedent, severity, blocking status) verified against the remediation register, remediation log, verdict, and the live PR worktree. Recommendation: ACCEPT with one Major fix.

## Findings Table

| ID | Assumption / Anti-Goal | Type | Confidence | Severity | Evidence | Dimension |
|----|------------------------|------|------------|----------|----------|-----------|
| S-013-01 | Reader can resolve the worktracker path without a stated branch | Assumption | Medium | Major | Tracking line: `Worktracker: projects/PROJ-032-nuclear-sop-review/work/BUG-005-h36-governance-ruling` (no branch) vs. the next sentence's `remediation-register.md ... on branch \`feat/proj-032-nuclear-sop-review\`` (branch stated) | Actionability |
| S-013-02 | "register section REM-05" is self-explanatory to a zero-context reader | Assumption | Low | Minor | `(register section REM-05)` — "register" and "REM-05" are undefined internal shorthand | Completeness |
| S-013-03 | Reader does not need the hop-counting arithmetic to evaluate the ruling | Assumption | Medium | Minor | "internal four-agent sequence" vs. "three agent-to-agent handoffs" — actual model (verified in `nuclear-sop-behavior-rules.md` lines 278-281) is 4 direct main-context-to-agent hops, not a 4-agent chain producing 3 handoffs; the arithmetic isn't spelled out | Evidence Quality |

## Finding Detail (Major)

### S-013-01: Worktracker path lacks the branch qualifier its sibling path has [MAJOR]

**Type:** Assumption (self-containedness / resolvable references)
**Original assumption:** The reader will find `projects/PROJ-032-nuclear-sop-review/work/BUG-005-h36-governance-ruling` without being told which branch it lives on.
**Inversion:** An external contributor/agent, working from PR #269's branch (`proj-0039-nuclear-engineer`) or `main`, looks for this path there, doesn't find it (it only exists on `feat/proj-032-nuclear-sop-review`, confirmed present at `BUG-005-h36-governance-ruling.md`), and either gives up on the worktracker reference or wastes a round-trip asking where it is — while the *very next* file reference in the same sentence group is careful to state its branch explicitly, so the omission reads as an oversight rather than an implied "same as above."
**Plausibility:** High — this is exactly the failure mode the mission's "paths carry branches" criterion targets, and the text visibly demonstrates it knows the rule (it applies it to the second path) but not the first.
**Consequence:** Actionability gap — one of the two supporting-evidence pointers in the issue may not resolve for the target audience.
**Dimension:** Actionability
**Mitigation:** Merge the two references under one branch statement, e.g.: "Both on branch `feat/proj-032-nuclear-sop-review`: worktracker `projects/PROJ-032-nuclear-sop-review/work/BUG-005-h36-governance-ruling`; full analysis `remediation-register.md` in `.../STORY-004-remediation/`."
**Acceptance Criteria:** Every repo-relative path in the Tracking line is either preceded/followed by an explicit branch name, or one sentence states the branch once and both paths are visibly grouped under it.

## Recommendations

- **Major (SHOULD fix):** S-013-01 — state the branch once, covering both the worktracker and register paths (see mitigation above).
- **Minor (MAY fix):** S-013-02 — replace "(register section REM-05)" with "(see the linked remediation register, finding REM-05)" or drop the ID if not load-bearing.
- **Minor (MAY fix):** S-013-03 — one clause on hop-counting (e.g., "each of the four agents is invoked directly by the main context, so a C3+ run makes four such handoffs") would let the owner evaluate the technical premise, not just the precedent, without leaving this file.

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Negative (minor) | S-013-02: undefined "register"/"REM-05" shorthand |
| Internal Consistency | 0.20 | Negative | S-013-01: one of two adjacent paths states its branch, the other doesn't |
| Methodological Rigor | 0.20 | Neutral | Core ruling question and precedent are stated with method (predetermined-sequence framing) |
| Evidence Quality | 0.15 | Negative (minor) | S-013-03: hop-count claim asserted without the underlying arithmetic |
| Actionability | 0.15 | Negative | S-013-01 blocks one of two evidence trails for the actual target audience |
| Traceability | 0.10 | Positive | Deadline date, contradiction, missing tracking ID, and eng-team precedent all independently verified against register/verdict/live rules file |

**Result:** No Critical or fact-inverting findings — every substantive claim in the issue text checked out against ground truth (2026-06-15 deadline in NS-H-08 itself; the "remains as written" vs. automatic-3-hop-reversion contradiction, confirmed within the same rules file and repeated in SKILL.md/PLAYBOOK.md; `TASK-0039-H36-RULING` confirmed absent from the live worktree; the `/eng-team` precedent matches the verdict's Phase 2 citation). One Major actionability gap (inconsistent branch qualifier) and two Minor clarity gaps.
