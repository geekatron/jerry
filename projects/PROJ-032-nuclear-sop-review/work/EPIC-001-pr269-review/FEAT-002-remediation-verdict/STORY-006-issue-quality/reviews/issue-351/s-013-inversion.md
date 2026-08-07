# Inversion Report: GitHub Issue #351 (PROJ-032/BUG-002)

**Strategy:** S-013 Inversion Technique
**Deliverable:** `snapshots/final/issue-351.md` (live text of geekatron/jerry issue #351)
**Criticality:** C4 (tournament)
**Date:** 2026-08-07
**Reviewer:** adv-executor
**Goals Analyzed:** 2 (external contributor understands defect; contributor/agent can locate full analysis and act) | **Assumptions Mapped:** 6 | **Vulnerable Assumptions:** 2

## Summary

Core factual claims (AskUserQuestion ungranted by any of 89 agents, unpinned runtime model, non-terminating self-check rule, Critical/not-maintainer-fixable/blocks-merge framing) check out exactly against the remediation register and are independently confirmed live on GitHub. Inversion found the vulnerability elsewhere: the text assumes its bare-path references will resolve the same way regardless of which branch a reader is on, and assumes prose severity is enough for triage — both assumptions fail under a plausible reader action. Recommendation: ACCEPT with two targeted mitigations (S-013-02, S-013-03).

## Findings Table

| ID | Assumption / Anti-Goal | Type | Confidence | Severity | Evidence | Affected Dimension |
|----|------------------------|------|------------|----------|----------|--------------------|
| S-013-01 | "self-check before every file write" covers the whole non-terminating rule | Assumption | Medium | Minor | Ground truth: NS-H-01/STAR applies to Write, Edit, **and Bash** (`nuclear-sop-behavior-rules.md` line 30, 149) | Evidence Quality |
| S-013-02 | Prose "severity critical... Blocks merge" is sufficient for triage without a label | Anti-Goal | High | Major | Confirmed live: issue #351 has **Labels: None** | Actionability |
| S-013-03 | The bare `Worktracker:` path resolves regardless of branch | Assumption | High | Major | Confirmed: same path 404s on `main`; branch is stated only once, attached to the *other* path in the same sentence group | Traceability |
| S-013-04 | A code-formatted bare path is as usable as a clickable link | Assumption | Medium | Minor | GitHub does not auto-link code-span paths; reader must manually construct the blob URL | Actionability |
| S-013-05 | Reader does not need the affected agent/file names to start acting | Assumption | Medium | Minor | Register lists 4 agents + `SKILL.md` + rules + templates as affected; issue names none of them | Completeness |

**Finding ID Format:** `S-013-NN` per task instructions (execution_id omitted; single-issue review).

## Finding Details

### S-013-02: No label reflects the asserted Critical/blocking severity [MAJOR]

**Type:** Anti-Goal
**Original Assumption:** Stating "severity critical" and "Blocks merge of PR #269" in the issue body is sufficient to keep this defect visible during triage.
**Inversion:** A maintainer or bot sorting/filtering issues by label (the mechanism GitHub actually offers for this) sees an unlabeled issue and treats it as routine backlog — increasing the chance PR #269 gets merged before this is resolved, which is the exact outcome the issue exists to prevent.
**Plausibility:** High — verified live; the issue currently has zero labels.
**Consequence:** Undermines the "honest severity/status framing" the text otherwise gets right; the prose claim is not backed by the repo's actual triage signal.
**Evidence:** Live GitHub fetch of issue #351: `Labels: None`.
**Dimension:** Actionability
**Mitigation:** Apply a `critical` (or repo-equivalent) label and, if available, a `blocks-merge` label; cross-link the issue from PR #269's description.
**Acceptance Criteria:** Issue #351 carries a severity label machine-readable by triage tooling, not only prose.

### S-013-03: Branch anchor is ambiguous for the Worktracker path [MAJOR]

**Type:** Assumption
**Original Assumption:** "Worktracker: `projects/PROJ-032-nuclear-sop-review/work/BUG-002-user-hold-runtime-model`" will resolve the same way the adjacent, explicitly branch-qualified `remediation-register.md` reference does.
**Inversion:** A reader who clicks/navigates the Worktracker path on GitHub's default view (branch `main`) gets a 404 — verified live — because the entire PROJ-032 review project exists only on `feat/proj-032-nuclear-sop-review`. The branch qualifier in the text is grammatically attached to the *next* sentence's path only.
**Plausibility:** High — this is the default navigation behavior on GitHub for a bare path with no branch/link.
**Consequence:** Reader concludes the reference is broken or stale, loses confidence in the rest of the issue, and re-derives the branch by trial and error instead of acting.
**Evidence:** `https://github.com/geekatron/jerry/tree/main/projects/PROJ-032-nuclear-sop-review/work/BUG-002-user-hold-runtime-model` → HTTP 404 (confirmed live); path exists at that same relative location on `feat/proj-032-nuclear-sop-review`.
**Dimension:** Traceability
**Mitigation:** State the branch once, covering both paths (e.g., "Both paths below are on branch `feat/proj-032-nuclear-sop-review`:"), or give each path as a full `.../tree/feat/proj-032-nuclear-sop-review/...` URL.
**Acceptance Criteria:** Every repo-relative path in the issue is either a full URL or explicitly and unambiguously scoped to its correct branch.

## Recommendations

**Major (SHOULD mitigate):** S-013-02 (add severity label), S-013-03 (fix branch ambiguity on Worktracker path).
**Minor (MAY mitigate):** S-013-01 (say "state-modifying action" not "file write"), S-013-04 (use full blob URLs instead of bare code-span paths), S-013-05 (name the 4 agents / list affected files inline, e.g., "sop-executor, sop-brief, and SKILL.md").

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Negative (minor) | S-013-05: affected agents/files omitted, forcing a lookup |
| Internal Consistency | 0.20 | Neutral | No contradictions found in the text itself |
| Methodological Rigor | 0.20 | Neutral | Not applicable to a communication artifact |
| Evidence Quality | 0.15 | Negative (minor) | S-013-01: rule scope slightly overstated as "file write" |
| Actionability | 0.15 | Negative | S-013-02, S-013-04: severity not machine-visible; paths not clickable |
| Traceability | 0.10 | Negative | S-013-03: branch-ambiguous path 404s on default branch |

**Result:** 0 Critical, 2 Major, 3 Minor. All factual claims verified accurate against the remediation register, remediation log, and live GitHub state; vulnerabilities are in reference resolvability and triage-signal durability, not content correctness.
