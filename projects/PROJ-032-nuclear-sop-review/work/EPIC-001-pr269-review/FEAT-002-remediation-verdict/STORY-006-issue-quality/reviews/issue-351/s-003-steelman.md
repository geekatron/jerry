# Steelman Report: GitHub Issue #351 (PROJ-032/BUG-002)

## Steelman Context
- **Deliverable:** `snapshots/final/issue-351.md` (live text of GitHub issue #351, geekatron/jerry)
- **Deliverable Type:** Communication/specification artifact (GitHub issue for external contributor + agent)
- **Criticality Level:** C4
- **Strategy:** S-003 (Steelman Technique)
- **SSOT Reference:** `.context/rules/quality-enforcement.md`
- **Steelman By:** adv-executor | **Date:** 2026-08-07

## Summary

**Steelman Assessment:** The issue text is already strong — every factual claim checked against the remediation register, BUG-002 worktracker entity, and verdict is accurate (severity, disposition "not maintainer-fixable", the "zero agents have AskUserQuestion" claim, the six-gate count, the STAR-non-termination mechanism). It correctly avoids internal jargon (no "NS-H-01", "STAR", "H-02" leakage) while preserving technical precision. The improvements below are genuine strengthening opportunities in resolvability and actionability, not corrections of errors.

**Improvement Count:** 0 Critical, 2 Major, 2 Minor
**Original Strength:** High — factually clean, self-contained, correctly severity-framed.
**Recommendation:** Incorporate SM-001/SM-002 before downstream critique; SM-003/SM-004 are optional polish.

## Improvement Findings Table

| ID | Improvement | Severity | Dimension |
|----|-------------|----------|-----------|
| SM-001 | Attach the branch qualifier to *both* referenced paths, not just the register path; both paths live entirely outside PR #269's own branch | Major | Actionability / Traceability |
| SM-002 | Add a one-clause candidate-direction hint to the design question so the issue is actionable without a mandatory register lookup | Major | Actionability |
| SM-003 | Gloss `AskUserQuestion` as "an interactive prompt tool" for readers unfamiliar with agent tooling | Minor | Completeness |
| SM-004 | Clarify the Worktracker reference resolves to a directory containing one file, not a page/file itself | Minor | Traceability |

## Improvement Details

### SM-001 (Major) — Branch attribution must cover both paths

**Original:**
> Worktracker: `projects/PROJ-032-nuclear-sop-review/work/BUG-002-user-hold-runtime-model` (register section REM-02). Full analysis with candidate designs: `remediation-register.md` in `projects/PROJ-032-nuclear-sop-review/work/EPIC-001-pr269-review/FEAT-002-remediation-verdict/STORY-004-remediation/` on branch `feat/proj-032-nuclear-sop-review`.

**Verified:** The PR #269 checkout (branch `proj-0039-nuclear-engineer`) contains `projects/README.md` only — no `PROJ-032` or `PROJ-0039` tree at all. Both referenced paths resolve exclusively on the separate maintainer review branch `feat/proj-032-nuclear-sop-review` in geekatron/jerry. As written, the branch qualifier grammatically attaches only to the second (register) path; a reader who checks out PR #269 to find the Worktracker path first will not find it there, and nothing on that first sentence warns them to look elsewhere.

**Strengthened:**
> Both paths below are on branch `feat/proj-032-nuclear-sop-review` in this repository (not on PR #269's own branch). Worktracker: `projects/PROJ-032-nuclear-sop-review/work/BUG-002-user-hold-runtime-model`. Full analysis with candidate designs: `remediation-register.md` (section REM-02) in `.../FEAT-002-remediation-verdict/STORY-004-remediation/` on that same branch.

**Rationale:** Removes a forward-reference dependency and states explicitly, once, that neither path is reachable from the PR's own branch — the single most consequential resolvability fact in the issue for an agent that acts by checking out files.

### SM-002 (Major) — Give the design question a starting direction

**Original:** "The design question to answer: what is the pinned runtime execution model, how do USER-HOLD and the briefing agent's six interactive gates actually reach a human under that model, and what is the terminating scope of the self-check rule?"

**Verified:** The verdict and register both already contain a concrete candidate split ("if worker subagents: USER-HOLD becomes a return-to-orchestrator protocol...; if main-context persona: re-justify tool-tier enforcement and verifier isolation") that costs one sentence to surface.

**Strengthened (append):** "One candidate: if the four agents stay background workers, USER-HOLD becomes a return-to-orchestrator step (the orchestrator asks the human, then resumes); if they run as the main session instead, the tool-isolation guarantees elsewhere in the design need re-justifying."

**Rationale:** Actionability — a contributor or their agent can begin evaluating a concrete option immediately instead of treating the register lookup as a hard prerequisite to starting work.

### SM-003 (Minor) — Gloss the tool name

**Original:** "calls a tool (`AskUserQuestion`)"
**Strengthened:** "calls a tool (`AskUserQuestion`, an interactive prompt-the-user tool)"
**Rationale:** Marginal completeness gain for a reader with no agent-tooling background; the mission requires zero assumed internal knowledge.

### SM-004 (Minor) — Directory vs. file clarity

**Original:** "Worktracker: `projects/PROJ-032-nuclear-sop-review/work/BUG-002-user-hold-runtime-model`"
**Strengthened:** "Worktracker: `projects/PROJ-032-nuclear-sop-review/work/BUG-002-user-hold-runtime-model/` (directory; entity file `BUG-002-user-hold-runtime-model.md`)"
**Rationale:** Removes one ambiguity step for an agent doing a direct file read vs. a directory listing.

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Neutral | Core claims already complete; SM-003 is marginal |
| Internal Consistency | 0.20 | Neutral | No inconsistency found |
| Methodological Rigor | 0.20 | Neutral | N/A — this is a communication artifact, not a method |
| Evidence Quality | 0.15 | Neutral | All claims independently verified against register/verdict/worktracker |
| Actionability | 0.15 | Positive | SM-001, SM-002 close two genuine act-without-lookup gaps |
| Traceability | 0.10 | Positive | SM-001, SM-004 remove path-resolution ambiguity |

---
*Steelman execution complete. No Critical findings — issue text is factually accurate and well-scoped for its audience; ready for downstream critique strategies.*
