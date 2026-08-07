# Constitutional Compliance Report: GitHub Issue #354 (BUG-005 / REM-05)

**Strategy:** S-007 Constitutional AI Critique (adapted for a ~300-word external communication artifact)
**Deliverable:** `.../STORY-006-issue-quality/snapshots/final/issue-354.md` (live text of GitHub issue #354)
**Criticality:** C4 (tournament)
**Date:** 2026-08-07
**Constitutional lens applied:** P-001 (Truth/Accuracy), P-022 (No Deception, incl. deception-by-omission), and the mission-specific criteria (self-containedness, actionability, resolvable references)

## Summary

PARTIAL compliance: 1 Critical (P-001/P-022 — the "resolves this issue outright" claim omits a documented blocking dependency), 3 Major (missing locator, inconsistent branch qualification, unassigned follow-up responsibility), 2 Minor (directory- vs file-level link, unglossed term). Estimated compliance score: 0.71 (REJECTED band; below 0.85). Recommend targeted revision — the core facts (deadline, contradictory fallbacks, missing tracker) all check out against ground truth; the defects are in framing and reference precision, not fabrication.

## Findings Table

| ID | Principle | Tier | Severity | Evidence | Affected Dimension |
|----|-----------|------|----------|----------|--------------------|
| S-007-01 | P-001/P-022: Truth/no deception (incl. omission) | HARD | Critical | Para 2: "adopting that reading ... resolves this issue outright" | Evidence Quality |
| S-007-02 | Self-containedness / resolvable reference | MEDIUM | Major | Para 2: "the existing eng-team skill runs a predetermined 8-step sequence ... no hop-ceiling machinery" — no path | Actionability |
| S-007-03 | Resolvable reference consistency | MEDIUM | Major | Tracking line: Worktracker path has no branch qualifier; adjacent register path in the same sentence does | Actionability |
| S-007-04 | Actionability / responsibility assignment | MEDIUM | Major | Para 2: "encode it once ... and track it as a real work item" — passive, unassigned | Actionability |
| S-007-05 | Resolvable reference precision | SOFT | Minor | Tracking line: Worktracker path points to a directory, not the entity file | Traceability |
| S-007-06 | Self-containedness (plain language) | SOFT | Minor | Para 2: "a fail-closed default" — ungloss'd term | Completeness |

## Finding Details

### S-007-01: Precedent framed as outright resolution, omitting a documented dependency [CRITICAL]

**Location:** Paragraph 2, "adopting that reading (\"predetermined sequences are not routing re-evaluations\") resolves this issue outright and removes the skill's self-scheduled sunset clause."
**Ground truth:** `BUG-005-h36-governance-ruling.md` (Disposition line) and `remediation-register.md` REM-05 both state the ruling "depends on the hop-model redesign in REM-01" (open blocker BUG-001 / issue #350) — the topology decision that defines what counts as a "hop" for this skill. Whichever answer is chosen now could be invalidated once BUG-001's redesign lands.
**Impact:** An owner acting on this text alone would reasonably conclude the eng-team precedent settles the matter with no caveats, and could issue a ruling that has to be re-litigated after BUG-001 lands — the exact scenario the register itself already warns against. This is a "would send the reader down a wrong path" case, not a polish issue.
**Remediation:** Add an explicit caveat, e.g.: "Note: per the remediation register, this ruling is coupled to the hop-model redesign in issue #350 (BUG-001) — confirm the eng-team precedent still applies once that topology is chosen before finalizing."

### S-007-02: Precedent cited with no locator [MAJOR]

**Location:** Paragraph 2, eng-team comparison.
**Ground truth:** Verified independently — `skills/eng-team/SKILL.md` does describe an 8-step "Orchestration Flow" across a 10-agent roster, so the factual content of the comparison holds. But the sentence gives no path or link.
**Impact:** The owner or their agent must do a repo-wide search to verify or apply the cited precedent — exactly the kind of lookup the mission asks this text to avoid forcing.
**Remediation:** Append `(see skills/eng-team/SKILL.md, "Orchestration Flow")`.

### S-007-03: Branch qualifier applied to one path but not the other [MAJOR]

**Location:** Tracking line: "Worktracker: `projects/PROJ-032-nuclear-sop-review/work/BUG-005-h36-governance-ruling` (register section REM-05). Full analysis ... `remediation-register.md` in `.../STORY-004-remediation/` on branch `feat/proj-032-nuclear-sop-review`."
**Ground truth:** The entire PROJ-032 review project (including the Worktracker `BUG-005-h36-governance-ruling` directory) exists only on branch `feat/proj-032-nuclear-sop-review` — the same branch explicitly named for the second path in the same sentence. It is not part of PR #269's own branch and (per the branch's own commit history, which shows the PROJ-032 scaffold as its most recent, review-only commit) is not established as present on `main`.
**Impact:** A reader who checks out `main` or the PR's branch to find the Worktracker path (reasonable, since no branch is given) will not find it, while the very next clause proves the author knew a branch qualifier was needed for this project's paths.
**Remediation:** State the branch once for both paths, e.g.: "On branch `feat/proj-032-nuclear-sop-review`: Worktracker `projects/PROJ-032-nuclear-sop-review/work/BUG-005-h36-governance-ruling`; full analysis in `.../STORY-004-remediation/remediation-register.md` (section REM-05)."

### S-007-04: Follow-up work is unassigned [MAJOR]

**Location:** Paragraph 2, "Whatever the ruling: encode it once, with one fallback behavior, one anchor date, and a fail-closed default, and track it as a real work item."
**Ground truth:** `BUG-005-h36-governance-ruling.md` Acceptance Criteria assign this encoding and tracker-creation work to the contributor ("Contributor redesign answers the register's REM-05 redesign question ... Encode exactly one fallback semantics ... create the TASK-0039-H36-RULING worktracker entity"), not to the "owner," who the same paragraph names as the sole decision-maker one sentence earlier.
**Impact:** An agent reading only this issue text could reasonably conclude no one but the owner has anything to do here, and stall waiting rather than starting contributor-side encoding work once the ruling lands.
**Remediation:** Split the sentence by actor: "Owner: rule on the question above. Contributor: once ruled, encode it in NS-H-08, SKILL.md, and PLAYBOOK.md, and create the tracking work item."

### S-007-05: Worktracker link resolves to a folder, not the record [MINOR]

**Location:** Tracking line, Worktracker path.
**Ground truth:** The actual file is `.../BUG-005-h36-governance-ruling/BUG-005-h36-governance-ruling.md`.
**Remediation:** Point to the `.md` file directly for one-click access.

### S-007-06: "fail-closed default" unglossed [MINOR]

**Location:** Paragraph 2.
**Remediation:** Add a 4-6 word gloss, e.g., "a fail-closed default (keep the stronger check until ruled otherwise)".

## Remediation Plan

**P0 (Critical):** S-007-01 — add the REM-01/BUG-001 coupling caveat to the precedent sentence.
**P1 (Major):** S-007-02 — add eng-team locator. S-007-03 — unify branch qualification across both paths in the tracking line. S-007-04 — split owner vs. contributor responsibility for the encode/track sentence.
**P2 (Minor):** S-007-05 — link the `.md` file, not the folder. S-007-06 — gloss "fail-closed default."

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Negative | S-007-06 |
| Internal Consistency | 0.20 | Negative | S-007-03 (inconsistent branch qualification within one sentence) |
| Methodological Rigor | 0.20 | Neutral | No findings affect rigor |
| Evidence Quality | 0.15 | Negative | S-007-01 (unsupported "resolves outright" claim) |
| Actionability | 0.15 | Negative | S-007-02, S-007-04 |
| Traceability | 0.10 | Negative | S-007-05 |

**Constitutional Compliance Score:** 0.71 = 1.00 − (1×0.10 + 3×0.05 + 2×0.02) → **REJECTED band** (<0.85); targeted revision recommended, not a rewrite — all core facts checked against `remediation-register.md`, `remediation-log.md`, `pr269-verdict.md`, and `BUG-005-h36-governance-ruling.md` are accurate.

## Execution Statistics
- **Total Findings:** 6
- **Critical:** 1
- **Major:** 3
- **Minor:** 2
- **Protocol Steps Completed:** 5 of 5
