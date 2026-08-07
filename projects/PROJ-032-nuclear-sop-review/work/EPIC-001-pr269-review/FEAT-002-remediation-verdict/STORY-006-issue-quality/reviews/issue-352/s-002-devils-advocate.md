# Devil's Advocate Report: GitHub Issue #352 (BUG-003 trust-boundary/state-tamper)

**Strategy:** S-002 Devil's Advocate
**Deliverable:** `snapshots/final/issue-352.md` (live text of geekatron/jerry issue #352)
**Criticality:** C4
**H-16 Compliance:** Steelman pass assumed prior per tournament ordering; this execution attacks the strengthened text directly.

## Summary

The technical claims (authority inversion, self-declared criticality, inert SHA-256 `state_hash`, hold-bypass-on-resume) all check out against the remediation register and the BUG-003 worktracker entity — no factual defect found there. The critique instead targets the artifact's own resolvability: the Tracking block gives the external reader a Worktracker path with no branch qualifier, on a project that (per repo state) exists only on an unmerged feature branch, while the very next sentence *does* attach the branch qualifier to a different path — inviting the reasonable inference that the first path is on the default branch. Combined with the issue's total absence of concrete affected-file paths, an agent following this issue alone can dead-end. 2 Critical/Major, 2 Minor. Recommend REVISE before further publication.

## Findings Table

| ID | Finding | Severity | Evidence | Affected Dimension |
|----|---------|----------|----------|--------------------|
| S-002-01 | Worktracker path stated without branch qualifier; will 404 on default branch | Critical | "Worktracker: `projects/PROJ-032-nuclear-sop-review/work/BUG-003-trust-boundary-state-tamper` (register section REM-03). Full analysis... on branch `feat/proj-032-nuclear-sop-review`." | Traceability / Actionability |
| S-002-02 | No affected-file paths given in the issue body; all actionability routes through one (branch-ambiguous) link | Major | Issue text names no `skills/nuclear-sop/...` file anywhere, unlike the BUG-003 worktracker entity's "Affected files" line | Actionability |
| S-002-03 | Assignees not corroborated by any provided ground-truth artifact | Minor | "Assignees: victorlau1 malcolm-x-evo" — absent from remediation-register.md, remediation-log.md, verdict.md, and the BUG-003 entity | Evidence Quality |
| S-002-04 | Title leads with unexplained internal codes for an audience stated to have zero governance context | Minor | Title: "PROJ-032/BUG-003: nuclear-sop — verifier takes its criteria..." | Completeness |

## Finding Details

### S-002-01: Branch-qualifier scope ambiguity makes the primary reference path unresolvable [CRITICAL]

**Claim challenged:** "Worktracker: `projects/PROJ-032-nuclear-sop-review/work/BUG-003-trust-boundary-state-tamper` (register section REM-03). Full analysis with candidate designs: `remediation-register.md` in `.../STORY-004-remediation/` on branch `feat/proj-032-nuclear-sop-review`."

**Counter-argument:** The branch qualifier is textually attached only to the second path (`remediation-register.md`). A reader with zero repo context has no signal that the *first* path (the Worktracker BUG-003 directory) also requires that non-default branch. Repo evidence (this session's own git status: default/main branch is `main`; the review project's own most recent commit is "scaffold nuclear-sop review project," on `feat/proj-032-nuclear-sop-review`) indicates `projects/PROJ-032-nuclear-sop-review/` almost certainly does not exist on `main`. An external contributor's AI agent that clones/checks out `main` (the normal default) and looks up the Worktracker path will get a file-not-found and may reasonably (and wrongly) conclude the tracking reference is broken or fabricated — undermining trust in the whole issue.
**Impact:** Primary traceability anchor fails silently for the target audience; agent may abandon verification of the "not maintainer-fixable" claim entirely.
**Dimension:** Traceability / Actionability
**Response Required:** State the branch once, scoped explicitly to both paths (or repeat it after each path).
**Acceptance Criteria:** Text reads, e.g.: "Worktracker: `.../BUG-003-trust-boundary-state-tamper` (register section REM-03) — both this and the register below are on branch `feat/proj-032-nuclear-sop-review` (not yet on `main`)."

### S-002-02: No in-body file paths reduce one-shot actionability [MAJOR]

**Claim challenged:** The entire issue relies on "Full analysis with candidate designs: `remediation-register.md`..." as the sole route to concrete code locations.
**Counter-argument:** The BUG-003 worktracker entity this issue is supposedly a public mirror of *does* list affected files (`sop-verifier.md`, `sop-brief.md`, `sop-executor.md`, `PROCEDURE_STATE.template.yaml`, `docs/reference.md`, `nuclear-sop-behavior-rules.md`). Omitting even the single highest-value file (`skills/nuclear-sop/agents/sop-verifier.md`, where SR-09 states the criteria/paths come from the workflow definition) means the reader must fully resolve S-002-01's link before they can open a single source file — two hops instead of one, and the first hop is broken per S-002-01.
**Impact:** Increases time-to-first-action; compounds the branch-resolution failure into a dead end rather than a detour.
**Dimension:** Actionability
**Response Required:** Add one line naming the primary implicated file(s).
**Acceptance Criteria:** Issue body contains at least: "Primary location: `skills/nuclear-sop/agents/sop-verifier.md` (SR-09)."

## Recommendations

- **P0:** S-002-01 — disambiguate branch scope for the Worktracker path before this issue is relied upon by an external agent.
- **P1:** S-002-02 — add the primary affected-file path inline.
- **P2:** S-002-03 — verify assignees against actual GitHub issue state (`gh issue view 352 --json assignees`) before treating this snapshot as final; drop the line if it is placeholder data.
- **P2:** S-002-04 — drop or relocate the "PROJ-032/BUG-003" prefix out of the human-facing title; it adds no actionable information for the stated audience.

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Negative | S-002-02, S-002-04: no file paths; unexplained title codes |
| Internal Consistency | 0.20 | Negative | S-002-01: branch qualifier applied to one path but not the other, sibling path |
| Methodological Rigor | 0.20 | Neutral | Technical claims (authority inversion, criticality self-declaration, inert hash, resume-past-holds) all verified accurate against ground truth |
| Evidence Quality | 0.15 | Negative | S-002-03: assignees unverifiable against any provided source |
| Actionability | 0.15 | Negative | S-002-01 + S-002-02 compound into a dead-end for the target reader |
| Traceability | 0.10 | Negative | S-002-01 is a traceability-anchor failure |

**Overall assessment:** Targeted revision. The substance is sound and matches ground truth precisely; the defects are entirely in reference resolvability and completeness, both fixable with small, localized edits (no rewrite required).
