# Pre-Mortem Report: GitHub Issue #356 (BUG-007 / REM-07)

**Strategy:** S-004 Pre-Mortem Analysis (adapted for a communication artifact)
**Deliverable:** `projects/PROJ-032-nuclear-sop-review/.../STORY-006-issue-quality/snapshots/final/issue-356.md` (live text of GitHub issue #356)
**Criticality:** C4 tournament
**Date:** 2026-08-07
**Failure Scenario:** Six months from now, the contributor (or their coding agent) ships a "fix" for BUG-007 that the maintainer rejects on re-review, because the issue text sent them after the wrong target: they build cross-document injection screening (state files, OE entries, hold logs) instead of the intra-document field coverage the redesign question actually asks for, they never learn the name of the deterministic engine they're meant to consider delegating to, and they close out only 2 of the 6 items the register's own redesign question requires — so the PR bounces a second time on the same issue number, burning the contributor's goodwill.

## Summary

6 failure causes found (1 Critical, 4 Major, 1 Minor). The text is directionally accurate on its two headline claims (denylist evasion, Major severity, DEFER-REWORK) but contains one internally-contradictory scope description that could misdirect implementation effort, omits a resolvable name/path for a control it tells the reader to consider, under-specifies the full fix scope relative to the linked worktracker item, and exposes internal tracking codenames in the title despite the project's own stated intent to keep issues self-contained for a governance-blind audience. **Recommendation: REVISE** — fixable within the existing ~300-word budget.

## Findings Table

| ID | Failure Cause | Category | Likelihood | Severity | Priority |
|----|---------------|----------|------------|----------|----------|
| S-004-01 | Screening-scope sentence conflates cross-document threat inputs with the actual (intra-document) finding | Technical/Assumption | Medium | Critical | P0 |
| S-004-02 | Deterministic engine referenced but not named or pathed | Actionability | High | Major | P1 |
| S-004-03 | Design question captures 2 of 6 required fix elements | Completeness | Medium | Major | P1 |
| S-004-04 | Title embeds unexplained internal codenames for a governance-blind audience | Process | Medium | Major | P1 |
| S-004-05 | Worktracker path omits the branch qualifier the very next path gets | Actionability | Medium | Major | P1 |
| S-004-06 | Available low-risk interim mitigation (narrow Bash grants) not surfaced | Completeness | Low | Minor | P2 |

## Finding Details

### S-004-01: Screening-scope description conflates two different findings [CRITICAL]

**Failure Cause:** "the skill's prompt-injection screening likewise covers only one of the several attacker-influenceable inputs (workflow definitions, state files, lessons-learned entries, hold-point logs)" describes a *cross-document* coverage gap. The actual REM-07 source finding (P2-027) is that SEC-001 screens only WARNING/CAUTION-annotated text *inside the workflow definition*, while other fields in that *same* document (Action, Target, Expected Result, Sign-off Criterion, Hold Reason, prose sections) are equally attacker-controlled and unscreened. State files, OE/"lessons-learned" entries, and hold-point logs are separate trust concerns already tracked as distinct blockers (issues #352 and #355). The issue's own design question later correctly scopes the ask as "*all definition-sourced fields*" — contradicting the "What this is about" framing two sentences earlier.
**Likelihood:** Medium — a careful reader may notice the internal contradiction and self-correct by reading the linked register; a less careful reader (or an agent skimming for the ask) takes the first framing at face value.
**Severity:** Critical — sends implementation effort at the wrong surface (cross-document screening) and risks duplicating work already scoped under #352/#355.
**Evidence:** Compare issue-356.md line 5 ("covers only one of the several attacker-influenceable inputs...") against register REM-07 G2 ("SEC-001 screens only WARNING/CAUTION annotation content while Action, Target, Expected Result, Sign-off Criterion, Hold Reason, and Sections 2/3/9 prose are equally attacker-controlled") and against the issue's own line 7 ("injection-screening scope across *all* definition-sourced fields").
**Mitigation:** Replace the sentence with: "...injection screening covers only WARNING/CAUTION-annotated text; other fields in the *same* workflow-definition document that equally drive tool calls (Action, Target, Expected Result, Sign-off Criterion, Hold Reason, free-form prose) are unscreened." Drop the "workflow definitions, state files, lessons-learned entries, hold-point logs" list — that cross-document surface belongs to issues #352 and #355, not this one.
**Acceptance Criteria:** Revised sentence names only intra-document fields; no contradiction remains between "What this is about" and "The design question."

### S-004-02: Deterministic control referenced without name or path [MAJOR]

**Failure Cause:** "the repository already has a deterministic security enforcement engine this duplicates, weaker, at the prompt level" — no name, no path. Ground truth confirms a concrete, resolvable target: `SecurityEnforcementEngine` (82 tests) at `src/infrastructure/internal/enforcement/security_enforcement_engine.py`.
**Likelihood:** High — any contributor evaluating "delegate to the existing engine" as an option must first find it, and the issue text alone does not let them.
**Severity:** Major — forces an off-issue lookup before the reader can even evaluate one of the three named design options.
**Evidence:** Confirmed present at `src/infrastructure/internal/enforcement/security_enforcement_engine.py` in the PR worktree; register REM-07 G3 names it as "SecurityEnforcementEngine, 82 tests" but the issue text drops the name.
**Mitigation:** "...duplicates, weaker, the repo's `SecurityEnforcementEngine` (`src/infrastructure/internal/enforcement/security_enforcement_engine.py`, 82 tests)."
**Acceptance Criteria:** Engine name and file path both appear in the issue body.

### S-004-03: Design question omits 4 of 6 required fix elements [MAJOR]

**Failure Cause:** The design question asks for (a) a gating model and (b) injection-screening scope only. BUG-007's own acceptance criteria (and the register's redesign question) also require: neutralizing verbatim payload echo into logs, surfacing H-05 (uv-only Python) in executor constraints, narrowing/dropping sop-brief's and sop-capture's over-broad Bash grants, and correcting PLAYBOOK.md's claim that SEC-001/002 are "the primary mitigations" (SR-06 human review is). A contributor who satisfies only (a) and (b) leaves the linked worktracker item's acceptance criteria unmet.
**Likelihood:** Medium — the issue does link to the full register, which mitigates this, but a design question is normally read as the complete ask.
**Severity:** Major — incomplete fix risks a second review round-trip on the same issue.
**Evidence:** BUG-007 acceptance criteria (worktracker) list all 6 elements; issue-356.md's design question states only the first 2.
**Mitigation:** Append: "...and (c) neutralize verbatim payload echo into logs, (d) surface the uv-only Python rule in executor constraints, (e) narrow sop-brief/sop-capture's Bash grants to their actual needs, and (f) correct PLAYBOOK.md's mitigation-hierarchy claim (human review, not SEC-001/002, is primary)." If space-constrained, at minimum add "(full acceptance criteria in the linked worktracker item)."
**Acceptance Criteria:** All 6 elements are either stated or explicitly pointed to from the issue body.

### S-004-04: Title embeds unexplained internal codenames [MAJOR]

**Failure Cause:** Title reads "PROJ-032/BUG-007: nuclear-sop — replace the command block-list...". The project's own verdict document states issues were "rewritten and retitled to be self-contained" because "the PR audience has no Jerry-governance context." "PROJ-032" and "BUG-007" are internal worktracker identifiers with no meaning to an external contributor and introduce a second, unexplained numbering scheme alongside GitHub's own #356.
**Likelihood:** Medium — doesn't block understanding the body, but is the first thing read and signals an internal tracking system the reader cannot resolve.
**Severity:** Major — directly conflicts with the project's own stated self-containedness goal for this exact document.
**Evidence:** pr269-verdict.md, PR Comment section: "Issues #350–#356 were likewise rewritten and retitled to be self-contained... because the PR audience has no Jerry-governance context."
**Mitigation:** Title becomes: "nuclear-sop: replace the command block-list with a principled gating model (PR #269)". The worktracker cross-reference already lives in the Tracking footer, where it is explained.
**Acceptance Criteria:** Title contains no bare internal ID prefix; worktracker/register IDs appear only in the explained Tracking section.

### S-004-05: Worktracker path lacks the branch qualifier its sibling reference gets [MAJOR]

**Failure Cause:** "Worktracker: `projects/PROJ-032-nuclear-sop-review/work/BUG-007-executor-command-gating`" is given with no branch. The very next sentence gives the register path *with* "on branch `feat/proj-032-nuclear-sop-review`". A reader who follows the first path against the repo's default branch (main) will not find it there — only the second, branch-qualified reference is unambiguously resolvable.
**Likelihood:** Medium — proximity to the branch-qualified sentence makes the branch inferable, but nothing states it applies to both paths.
**Severity:** Major — the mission's own resolvability bar ("paths carry branches") is met for one reference and not the other, in the same sentence group.
**Evidence:** issue-356.md Tracking paragraph, sentences 2 and 3.
**Mitigation:** "Worktracker: `projects/PROJ-032-nuclear-sop-review/work/BUG-007-executor-command-gating` (register section REM-07; both on branch `feat/proj-032-nuclear-sop-review`)." — state the branch once, covering both paths.
**Acceptance Criteria:** Every file/directory path in the Tracking section is unambiguously resolvable without inferring branch from a neighboring sentence.

### S-004-06: Available low-risk interim mitigation not mentioned [MINOR]

**Failure Cause:** The register notes a maintainer-safe interim step independent of the full redesign: narrowing sop-brief's/sop-capture's Bash grants, whose declared needs (read-only interrogation, timestamps, file counts) are already covered by other granted tools. The issue omits this, missing a chance to point at low-risk progress available today.
**Likelihood:** Low — omission, not misdirection.
**Severity:** Minor — nice-to-have, not required to act on the core ask.
**Mitigation:** Add one clause: "(Narrowing sop-brief/sop-capture's Bash grants to their actual read-only needs is a low-risk step available now, independent of the redesign.)"

## Recommendations

- **P0:** S-004-01 — rewrite the screening-scope sentence to match the intra-document finding; remove the contradiction with the issue's own design question.
- **P1:** S-004-02 (name + path the engine), S-004-03 (complete the design-question scope or point to full acceptance criteria), S-004-04 (de-codename the title), S-004-05 (state the branch once for both paths).
- **P2:** S-004-06 — one-clause addition noting the available interim mitigation.

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Negative | S-004-03, S-004-06: fix scope under-specified relative to linked worktracker item |
| Internal Consistency | 0.20 | Negative | S-004-01: "What this is about" contradicts the issue's own design question |
| Methodological Rigor | 0.20 | Neutral | Structure (context → design question → tracking) is sound |
| Evidence Quality | 0.15 | Negative | S-004-02: named control lacks resolvable name/path in-text |
| Actionability | 0.15 | Negative | S-004-01, S-004-02, S-004-05: force lookups or misdirect effort |
| Traceability | 0.10 | Negative | S-004-05: one of two adjacent path references is branch-unqualified |

## Execution Statistics

- **Total Findings:** 6
- **Critical:** 1
- **Major:** 4
- **Minor:** 1
- **Protocol Steps Completed:** 6 of 6 (Set Stage, Declare Failure, Generate Causes, Prioritize, Mitigations, Synthesize)
