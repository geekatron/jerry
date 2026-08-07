# FMEA Report: GitHub Issue #356 (BUG-007 — executor command gating)

**Strategy:** S-012 FMEA | **Deliverable:** `snapshots/final/issue-356.md` | **Criticality:** C4
**H-16 Compliance:** N/A for this blind single-strategy pass (tournament-level S-003 assumed upstream)
**Elements Analyzed:** 6 | **Failure Modes Identified:** 5 | **Total RPN:** 630

## Summary

Decomposed the ~300-word issue into 6 elements (title, assignees, block-list problem statement, injection-screening problem statement, design question, tracking line). Core factual claims about the substring denylist (S-012-04 area) check out against `remediation-register.md` REM-07. Two findings matter most: the injection-screening problem statement silently imports scope from two *other* blockers (BUG-003, BUG-006), risking duplicated or dropped work by whoever picks this issue up (S-012-01), and the fix pointer to "the existing deterministic enforcement engine" never names it, forcing a codebase search (S-012-02). Recommendation: REVISE (targeted text fixes, not a rewrite).

## Findings Table

| ID | Element | Failure Mode | S | O | D | RPN | Severity | Corrective Action |
|----|---------|-------------|---|---|---|-----|----------|-------------------|
| S-012-01 | Injection-screening problem statement | Inconsistent — scope creep from adjacent bugs | 6 | 6 | 6 | 216 | Critical | Rewrite parenthetical to name the actual missed fields |
| S-012-02 | Design question (engine delegation) | Insufficient — engine unnamed, unlocated | 5 | 6 | 5 | 150 | Major | Name engine + file path |
| S-012-03 | Tracking line (Worktracker path) | Ambiguous — branch qualifier not attached | 3 | 5 | 5 | 75 | Minor | Repeat/consolidate branch note |
| S-012-04 | Assignees line | Missing — formatting/typo | 2 | 6 | 8 | 96 | Minor | Add comma, trim trailing space |
| S-012-05 | Title | Insufficient — half the scope omitted | 4 | 5 | 5 | 100 | Minor | Broaden title to cover both sub-questions |

## Finding Details

### S-012-01: Injection-screening problem statement conflates three separate blockers' scopes

**Element:** "the skill's prompt-injection screening likewise covers only one of the several attacker-influenceable inputs (workflow definitions, state files, lessons-learned entries, hold-point logs)..."

**Effect:** Ground truth (Phase 2 STRIDE table, `phase-2-eng-review.md`) does list exactly these five attacker-influenceable inputs (workflow definition, executor-reported paths, OE corpus/"lessons-learned", state file, hold logs) — so the parenthetical is not invented. But REM-07's *actual* remediation scope (register REM-07 G2 and its own "Redesign question for the contributor") is narrower and different in kind: the missed screening surface is **fields inside the workflow definition** (Action, Target, Expected Result, Sign-off Criterion, Hold Reason, Section 2/3/9 prose) — not separate artifact types. State-file tamper protection is BUG-003's scope (issue #352); the lessons-learned/OE corpus injection channel is BUG-006's scope (issue #355). A contributor picking up #356 could reasonably conclude they must also harden state-file and OE-corpus screening here — duplicating BUG-003/BUG-006 — or conversely assume those are already covered by this issue and skip them there.

**S/O/D rationale:** S=6 (creates real duplicate-work / dropped-work risk across three tracked issues, though not deliverable-invalidating on its own); O=6 (this sentence is the first thing a reader/agent parses before reaching the correctly-scoped design question); D=6 (only detectable by cross-reading REM-03/REM-06/REM-07 side by side — not visible from this issue alone).

**Corrective Action:** Replace the parenthetical with the REM-07-scoped description: "...covers only the WARNING/CAUTION annotation field, while Action, Target, Expected Result, Sign-off Criterion, Hold Reason, and other prose fields inside the same workflow definition are equally attacker-controlled and drive tool calls just as directly." If the broader four-artifact framing is intentional context, add one clause: "(state-file and lessons-learned-corpus injection are tracked separately as BUG-003 and BUG-006)."

**Acceptance Criteria:** Text names only fields/artifacts within REM-07's actual scope, or explicitly disclaims the adjacent-issue overlap. **Post-Correction RPN estimate:** ~48 (S=4, O=4, D=3).

### S-012-02: "Existing deterministic enforcement engine" is unnamed and unlocated

**Element:** "Meanwhile the repository already has a deterministic security enforcement engine this duplicates, weaker, at the prompt level" and "...delegation to the existing deterministic enforcement engine."

**Effect:** Verified against the PR worktree: the engine exists at `src/infrastructure/internal/enforcement/security_enforcement_engine.py` (class `SecurityEnforcementEngine`, with a companion test suite). The issue never names it. An external contributor tasked with "delegate to the existing engine" has no starting point and must grep the entire codebase to find it — the exact "forces a lookup" failure mode the mission statement flags.

**S/O/D rationale:** S=5 (blocks the most concrete of the three redesign options from being started without extra research); O=6 (every reader attempting this option hits it); D=5 (findable but only via a codebase search the issue should have done for them).

**Corrective Action:** Add the class/path: "...delegation to the existing deterministic enforcement engine (`SecurityEnforcementEngine`, `src/infrastructure/internal/enforcement/security_enforcement_engine.py`)."

**Acceptance Criteria:** Engine name and resolvable path present in the issue text. **Post-Correction RPN estimate:** ~30.

### S-012-03: Worktracker path lacks its own branch qualifier

**Element:** "Worktracker: `projects/PROJ-032-nuclear-sop-review/work/BUG-007-executor-command-gating` (register section REM-07)." — no branch note, whereas the very next sentence about `remediation-register.md` does carry "on branch `feat/proj-032-nuclear-sop-review`."

**Effect:** Both paths are branch-scoped artifacts (confirmed: neither exists on `main`). A reader who stops after the Worktracker path, or checks it out on `main`, gets a 404 with no warning that a branch switch is needed. Verified against `remediation-register.md`'s own path, which matches the issue's second path exactly.

**S/O/D rationale:** S=3 (recoverable — the next sentence's branch note is one line away); O=5 (plausible a reader checks the first path first and stops); D=5.

**Corrective Action:** Move the branch qualifier earlier so it covers both paths in one clause, e.g., "...(register section REM-07); both on branch `feat/proj-032-nuclear-sop-review`. Full analysis with candidate designs: `remediation-register.md` in the same directory."

**Acceptance Criteria:** One branch qualifier unambiguously scopes both paths. **Post-Correction RPN estimate:** 20.

## Recommendations (priority order)

1. **S-012-01 (Critical, RPN 216):** Rescope the injection-screening sentence to REM-07's actual field-level gap; disclaim or cross-reference BUG-003/BUG-006 overlap.
2. **S-012-02 (Major, RPN 150):** Name `SecurityEnforcementEngine` and its file path in the design question.
3. **S-012-05 (Minor, RPN 100):** Broaden the title to reflect both the gating-model question and the injection-screening-scope question (currently only the former is titled).
4. **S-012-04 (Minor, RPN 96):** `Assignees: victorlau1, malcolm-x-evo` — add comma, trim trailing whitespace.
5. **S-012-03 (Minor, RPN 75):** Consolidate the branch qualifier to cover both cited paths.

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Internal Consistency | 0.20 | Negative | S-012-01: problem statement scope contradicts the correctly-narrower design question two paragraphs later |
| Actionability | 0.15 | Negative | S-012-02: named redesign option has no locatable starting point |
| Traceability | 0.10 | Negative | S-012-03: one of two cited paths is branch-ambiguous |
| Completeness | 0.20 | Neutral | Core facts (denylist bypasses, log-echo, duplicated weaker control) are all present and accurate |
| Methodological Rigor | 0.20 | Neutral | No rigor defect found beyond S-012-01 |
| Evidence Quality | 0.15 | Positive | Denylist bypass examples and severity/disposition both verified verbatim against the register |

---
*Elements with no finding (title's factual content, block-list problem statement, tracking severity/disposition/blocks-merge claims) were checked against `remediation-register.md` REM-07 and `pr269-verdict.md` and found accurate — no entry fabricated to pad the count.*
