# Inversion Report: GitHub Issue #355 (BUG-006 / REM-06 — OE feedback-loop design)

**Strategy:** S-013 Inversion Technique | **Deliverable:** `snapshots/final/issue-355.md`
**Criticality:** C4 (tournament) | **Date:** 2026-08-07 | **Reviewer:** adv-executor
**Goals Analyzed:** 3 | **Assumptions Mapped:** 6 | **Vulnerable Assumptions:** 2

## Summary

Goal-inverted the issue text against "what would guarantee an external contributor/agent cannot act on this correctly." The technical description of the OE (operating-experience) feedback-loop defect is factually faithful to REM-06/BUG-006 (schema gap, ownership contradiction, threshold ratchet, injection channel, provenance false-fire) and its severity/disposition framing ("major; not maintainer-fixable") is honest. The stress-test surfaces one unaddressed reference-resolution assumption (Major) that could send a zero-context reader down a dead-end lookup, plus minor concision/framing nits. No factual (Critical) defects found. Recommendation: ACCEPT with one targeted fix.

## Findings Table

| ID | Assumption / Anti-Goal | Type | Confidence | Severity | Evidence |
|----|------------------------|------|------------|----------|----------|
| S-013-01 | Reader will infer the Worktracker path lives on the same branch as the adjacent remediation-register path | Assumption | Low | Major | Line 10: register path states "on branch `feat/proj-032-nuclear-sop-review`"; the Worktracker path in the same sentence carries no branch qualifier |
| S-013-02 | A bare repo-relative path (no host/URL/branch ref) is sufficient for an external agent to resolve a file that is NOT on the PR's own branch | Assumption | Low | Major | Both paths in line 10 are plain code spans, not links; PR branch is `proj-0039-nuclear-engineer` (per BUG-006 "Found In"), a different branch/location than the cited paths |
| S-013-03 | Prefixing the title with internal identifiers ("PROJ-032/BUG-006") does not need a gloss | Anti-Goal (self-containedness) | N/A | Minor | Line 1 title: `PROJ-032/BUG-006:` precedes the plain-language description with no inline explanation of what this project/bug tag is |
| S-013-04 | Named assignees are self-explanatory to a zero-context reader | Anti-Goal (self-containedness) | N/A | Minor | Line 3: `Assignees: victorlau1 malcolm-x-evo` — no role/affiliation context (maintainer vs. bot vs. reviewer) |

## Finding Details

### S-013-01: Worktracker path is missing its branch, unlike the adjacent register path [MAJOR]

**Type:** Assumption | **Original Assumption:** "Same-sentence context (the register path's branch note) transfers to the Worktracker path."
**Inversion:** The reader/agent treats the Worktracker path as resolvable on the PR's own checkout (branch `proj-0039-nuclear-engineer`), searches there, finds nothing, and either wastes a round-trip or concludes the reference is fabricated.
**Plausibility:** High — the PR's own branch does not contain `projects/PROJ-032-nuclear-sop-review/`; this project tree lives only on `feat/proj-032-nuclear-sop-review` (verified: `projects/PROJ-032-nuclear-sop-review/work/BUG-006-oe-feedback-loop-design/BUG-006-oe-feedback-loop-design.md` exists there, not on the PR branch).
**Consequence:** Wasted lookup, or a false conclusion that the issue cites a nonexistent artifact — directly harms the "resolvable references" criterion.
**Evidence:** Issue line 10 gives two paths in one sentence; only the first ("Full analysis...") is qualified "on branch `feat/proj-032-nuclear-sop-review`". The Worktracker path that follows has no such qualifier.
**Dimension:** Traceability
**Mitigation:** Append the same branch qualifier to the Worktracker path, e.g.: "Worktracker: `projects/PROJ-032-nuclear-sop-review/work/BUG-006-oe-feedback-loop-design` (also on branch `feat/proj-032-nuclear-sop-review`; register section REM-06)."
**Acceptance Criteria:** Every non-PR-branch path in the issue carries an explicit branch qualifier, no shared-context inference required.

### S-013-02: Cross-repo/branch references given as bare paths, not resolvable links [MAJOR]

**Type:** Assumption | **Original Assumption:** "A plain repo-relative path string is enough for a reader to open the file."
**Inversion:** The reader has no host, no branch-aware URL, and no instruction to `git checkout`/`fetch` a different branch than the one their PR lives on; both citations require out-of-band knowledge of the reviewing repository's layout.
**Plausibility:** High — this is the only access path offered for either citation.
**Consequence:** Actionability degrades from "click and read" to "reverse-engineer the review repo's branch structure," which the mission explicitly requires this text to avoid.
**Evidence:** Line 10, both citations are inline code spans with no URL.
**Dimension:** Actionability
**Mitigation:** Replace at least one citation with a resolvable GitHub URL, e.g. `https://github.com/geekatron/jerry/blob/feat/proj-032-nuclear-sop-review/projects/PROJ-032-nuclear-sop-review/work/EPIC-001-pr269-review/FEAT-002-remediation-verdict/STORY-004-remediation/remediation-register.md#rem-06-oe-feedback-loop-design`, and likewise for the Worktracker path.
**Acceptance Criteria:** At least one clickable, branch-qualified URL per citation; zero bare paths for cross-branch references.

## Recommendations

- **MUST:** S-013-01 — add the branch qualifier to the Worktracker path so both citations in that sentence carry identical resolution context.
- **SHOULD:** S-013-02 — convert citations to clickable branch-qualified GitHub URLs.
- **MAY:** S-013-03/04 — gloss the `PROJ-032/BUG-006` title prefix (e.g., "internal tracking ID") and/or drop or annotate assignees if they are not the PR author's contacts.

## Scoring Impact

| Dimension | Impact | Rationale |
|-----------|--------|-----------|
| Traceability | Negative | S-013-01: inconsistent branch-qualification between two adjacent citations |
| Actionability | Negative | S-013-02: no resolvable links for cross-branch artifacts |
| Completeness | Neutral | Technical defect description (schema gap, ownership conflict, threshold ratchet, injection channel, provenance false-fire) verified accurate and complete against REM-06/BUG-006 |
| Evidence Quality | Positive | Severity/disposition ("major", "not maintainer-fixable") verified honest against source register and BUG-006 |
| Internal Consistency | Neutral | No contradictions found within the issue text itself |
| Methodological Rigor | N/A | Not applicable to a communication artifact |

**Fact-check note:** All substantive technical claims in the issue body were verified against `remediation-register.md` REM-06 and `BUG-006-oe-feedback-loop-design.md` and found accurate; no fabricated or misstated facts identified.
