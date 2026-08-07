# Red Team Report: GitHub Issue #358 (issue-358.md)

**Strategy:** S-001 Red Team Analysis (adapted, compact form for a ~300-word communication artifact)
**Deliverable:** `snapshots/final/issue-358.md` — live text of `geekatron/jerry` issue #358
**Criticality:** C4 (tournament)
**Threat Actor:** An external PR #269 contributor (or their AI coding agent) with zero knowledge of Jerry's internal governance, reading only this issue text, who must decide whether to act, ignore, or push back — and who has no reason to trust maintainer claims without being able to verify them from the text alone.

## Summary

The issue's technical claims (registration gaps, routing-priority mechanics, agent-count fix, CI evidence, worktracker path) were independently verified against the remediation register, the commit diff, the live PR-branch worktree, and the public GitHub issue/branch/commit — **all checked out factually accurate, including the routing-algorithm mechanics (compound-trigger override beats numeric priority), which was traced step-by-step and confirmed correct.** No Critical (factually-wrong/misleading) attack vectors were found. The exploitable surface is self-containedness and reference-resolvability for a zero-context reader: three Major findings where the text names things it never lets the reader reach (internal ticket codes, an undefined "disposition" decision point, a non-hyperlinked path). Recommendation: **ACCEPT with minor countermeasures** (Major findings are polish-adjacent, not blocking).

## Findings Table

| ID | Attack Vector | Category | Severity |
|----|---------------|----------|----------|
| S-001-01 | Title carries unexplained internal codes "PROJ-032/BUG-009" | Ambiguity | Major |
| S-001-02 | "PR #269's disposition" referenced with no pointer to where it will surface | Dependency | Major |
| S-001-03 | Register citation is a bare path + branch name, not a clickable link | Boundary | Major |
| S-001-04 | Sibling-issue existence (6 other clusters, same commit) not disclosed | Ambiguity | Minor |
| S-001-05 | "degradation-proof enforcement layer" — mildly inflated/jargon phrasing | Degradation | Minor |
| S-001-06 | "What the fix changed" omits two sub-fixes actually shipped (verified-date bump, MCP note) | Internal Consistency | Minor |

## Finding Details

### S-001-01: Unexplained internal ticket codes in the title [MAJOR]

**Attack Vector:** The title opens with `PROJ-032/BUG-009:` — two internal identifiers never defined anywhere in the body. A zero-context reader (or their agent) has no way to know if these are blocking dependencies, cross-references they must resolve, or decorative noise, and may waste a lookup cycle trying to find out.
**Evidence:** Line 1: `# GitHub issue #358: PROJ-032/BUG-009: nuclear-sop — skill missing from enforcement lists...`
**Countermeasure:** Drop the raw codes from the title or gloss them inline once, e.g. `(maintainer-tracked as BUG-009)`, and let the existing **Tracking** footer carry the full internal reference.
**Acceptance Criteria:** Title contains no bare internal ID without a same-issue gloss.

### S-001-02: "PR #269's disposition" has no resolution path [MAJOR]

**Attack Vector:** The closing sentence — "this issue stays open only until PR #269's disposition is decided" — sets an external expectation (something will be decided) but gives no link, owner, or venue for that decision. A reader cannot verify progress or know when/where to look; the sentence is unfalsifiable from the issue alone.
**Evidence:** Line 14, final clause of the Tracking paragraph.
**Countermeasure:** Add one clause pointing to where disposition will be communicated, e.g. "tracked on PR #269 itself" or a link to the verdict artifact once it is public.
**Acceptance Criteria:** Reader can navigate from this sentence to the actual decision record without asking the maintainer.

### S-001-03: Register reference not resolvable without manual URL construction [MAJOR]

**Attack Vector:** `remediation-register.md` is cited only as a repo-relative path plus a branch name in backticks — no hyperlink. Verified via WebFetch that the branch and file are in fact public and resolvable (`github.com/geekatron/jerry/blob/feat/proj-032-nuclear-sop-review/...`), so this is not a dead reference, but the reader must hand-assemble the URL themselves, and an AI agent parsing the issue as plain text has no machine-actionable link to follow.
**Evidence:** Line 14: `` `projects/PROJ-032-nuclear-sop-review/work/EPIC-001-pr269-review/FEAT-002-remediation-verdict/STORY-004-remediation/` on branch `feat/proj-032-nuclear-sop-review` ``.
**Countermeasure:** Replace the path+branch pair with a direct `github.com/.../blob/feat/proj-032-nuclear-sop-review/.../remediation-register.md#rem-09-registration-enforcement-surfaces` link.
**Acceptance Criteria:** Every file reference in the Tracking line is a clickable URL, not a path fragment.

## Recommendations

- **P1:** S-001-01, S-001-02, S-001-03 — apply the three countermeasures above; each is a single-sentence/link edit, no redesign.
- **P2 (Minor, optional polish):** S-001-04 — one clause noting "6 sibling issues cover the remaining FIX-NOW clusters from the same commit" would pre-empt reader confusion about scope. S-001-05 — replace "degradation-proof" with "per-prompt" (the concrete mechanism, already named in the same sentence, does the explanatory work). S-001-06 — either extend "What the fix changed" to mention the verified-date and MCP-note updates, or accept the current scoping (the three headline items are the ones a contributor would care about).

## Scoring Impact

| Dimension | Impact | Rationale |
|-----------|--------|-----------|
| Completeness | Negative | S-001-02, S-001-03 leave the reader without a path to close the loop the text itself opens |
| Internal Consistency | Negative | S-001-06 minor mismatch between "what was wrong" (3 sub-items) and "what changed" (implies same 3, ships more) |
| Evidence Quality | Positive | Every checkable claim (CI run, commit hash, branch, diff content, agent count, routing mechanics) verified true |
| Actionability | Neutral | Core "nothing to do unless you disagree" instruction is clear and correct |
| Traceability | Negative | S-001-03: traceable in principle, not traceable in one click |

**Overall assessment:** ACCEPT with minor countermeasures — zero Critical/factual findings; three Major findings are all "add a link/gloss" fixes, not redesign.
