# Devil's Advocate Report: GitHub Issue #350 (BUG-001, PR #269)

**Strategy:** S-002 Devil's Advocate
**Deliverable:** `projects/PROJ-032-nuclear-sop-review/.../STORY-006-issue-quality/snapshots/final/issue-350.md`
**Criticality:** C4 (tournament execution)
**Date:** 2026-08-07
**Reviewer:** adv-executor (blind execution)
**H-16 Compliance:** Per orchestrator-enforced tournament group order (self-refine -> steelman -> challenge), S-003 Steelman is executed in a prior group before this challenge-group execution. This agent does not have file-level visibility into the S-003 output (blind per task scope) and proceeds on that basis.

## Summary

5 counter-arguments identified (1 Critical, 2 Major, 2 Minor). The text's core factual claims about `sop-executor` (the first-person QG-HOLD invocation, the "cannot invoke any other agent" line, the missing return-to-orchestrator step, and the ~7-hop composed pattern vs. the 3-hop ceiling) are verified accurate against the live PR-branch files and the remediation register. The most serious weakness is not a factual error but a resolvability gap: the one pointer to "full analysis" sends an outside contributor to a file+branch they likely cannot reach, and the issue itself names zero files to edit. Recommend REVISE.

## Findings Table

| ID | Finding | Severity | Evidence | Affected Dimension |
|----|---------|----------|----------|--------------------|
| S-002-01 | "Full analysis" pointer is not resolvable by the stated audience | Critical | Tracking line names a file+branch with no GitHub link | Actionability |
| S-002-02 | Worktracker path given without the branch qualifier the sibling reference carries | Major | Same Tracking line, first vs. second path | Internal Consistency |
| S-002-03 | Two distinct defects (mid-procedure agent calls; ~7-hop composed pattern) collapsed into one sentence, zero files named anywhere | Major | Body paragraph, sentence 2 | Completeness |
| S-002-04 | Title leads with unexplained internal identifiers before any gloss | Minor | Title: "PROJ-032/BUG-001: nuclear-sop..." | Traceability |
| S-002-05 | "Acceptable descope" omits that naming and hop-budget corrections still apply under descope | Minor | Body paragraph, "Acceptable descope" | Completeness |

## Finding Details

### S-002-01: "Full analysis" pointer is not resolvable by the stated audience [CRITICAL]

**Claim Challenged:** "Full analysis with candidate designs: `remediation-register.md` in `.../STORY-004-remediation/` on branch `feat/proj-032-nuclear-sop-review`."

**Counter-Argument:** The mission requires the text to be actionable by PR #269's external author/agent with zero internal-governance context. `feat/proj-032-nuclear-sop-review` is the *reviewer's* internal working branch for a separate review project — not PR #269's branch, not `main`, and not linked anywhere in the issue as a GitHub URL. An external contributor who is not a repo maintainer has no obvious way to know this branch exists, whether it is pushed to the public remote, or how to fetch it. Giving a bare local-style path plus a branch name, with no `https://github.com/.../blob/<branch>/<path>` link, is the single most consequential resolvability gap in the issue: it is the only place the "candidate architectures" (the concrete options a) return-to-main-context, b) orchestrator-executes-the-step, c) drop mid-procedure composition) actually live. Without it, the contributor sees only the one-line design question and has to reverse-engineer the same candidate list from scratch.

**Impact:** Contributor/agent cannot retrieve the referenced analysis at all, or wastes time trying to locate a branch that may not be publicly fetchable — directly undermining the "resolvable references" and "actionability" criteria this review is scored against.

**Dimension:** Actionability

**Response Required:** Replace the bare path+branch reference with a resolvable link: either a GitHub blob/permalink (`https://github.com/geekatron/jerry/blob/<pushed-branch-or-commit-sha>/projects/PROJ-032-nuclear-sop-review/.../remediation-register.md#rem-01-...`), or inline the three candidate architectures (a/b/c) and the four "must also" requirements directly in the issue body so no cross-branch lookup is needed.

**Acceptance Criteria:** The reference resolves via a single click/fetch from the contributor's default checkout of the public repo, OR the issue is self-contained (candidate designs stated inline) and the register is cited only as supplementary provenance.

### S-002-02: Worktracker path missing branch qualifier [MAJOR]

**Claim Challenged:** "Worktracker: `projects/PROJ-032-nuclear-sop-review/work/BUG-001-qg-hold-delegation-topology` (register section REM-01). Full analysis ... on branch `feat/proj-032-nuclear-sop-review`."

**Counter-Argument:** The branch qualifier is attached only to the second path (remediation-register.md), not the first (the worktracker item). Both paths live under the same `projects/PROJ-032-nuclear-sop-review/` tree and are, in fact, on the same non-default branch. A reader who checks out their own PR branch or `main` and successfully understands "I need branch X" from the second sentence may still reasonably (and incorrectly) assume the first path is available on whatever branch they're already on, since it's stated with no qualifier at all.

**Evidence:** Verified — `projects/PROJ-032-nuclear-sop-review/work/BUG-001-qg-hold-delegation-topology/BUG-001-qg-hold-delegation-topology.md` exists only on `feat/proj-032-nuclear-sop-review`; it is not part of PR #269's branch tree.

**Impact:** Minor confusion escalates the same resolvability problem as S-002-01 across a second reference.

**Dimension:** Internal Consistency

**Response Required:** State the branch once, up front, covering both references (e.g., "Both paths below are on branch `feat/proj-032-nuclear-sop-review` of this repo").

**Acceptance Criteria:** A single unambiguous branch statement governs every repo-relative path in the Tracking line.

### S-002-03: Conflated defects, zero files named [MAJOR]

**Claim Challenged:** "The flagship example workflow additionally requires outside agents mid-procedure with no way to suspend and resume the executor's step-tracking around them, and the composed sequence exceeds the framework's three-handoff routing ceiling."

**Counter-Argument:** Per the remediation register, these are two separate defects in two separate files: the flagship example (`examples/c3-adr-workflow-definition.md`) requires mid-procedure external-agent calls with no suspend/resume protocol (register group G2); the ~7-hop composed pattern that exceeds the 3-hop ceiling is attributed to a *different* document, the how-to guide (register group G4), whose own deferred citation ("skill-integration-analysis.md") isn't even shipped. The issue sentence reads as if one artifact ("the flagship example workflow ... and the composed sequence") is the source of both problems. Combined with the fact that the issue names no files at all, a contributor could reasonably conclude that fixing the flagship example alone resolves the hop-ceiling finding too, when the register treats them as distinct defects in distinct files.

**Evidence:** remediation-register.md REM-01 groups G2 and G4; issue body sentence 2 (as quoted above) does not distinguish the two source documents.

**Impact:** Could misdirect scoping of the fix, or cause the hop-ceiling defect to be left unaddressed if the contributor treats the sentence as describing one artifact.

**Dimension:** Completeness

**Response Required:** Split the sentence into two, each naming its source artifact (e.g., "...the worked example (`examples/c3-adr-workflow-definition.md`) calls outside agents mid-procedure with no suspend/resume mechanism. Separately, the composed pattern shown in the how-to guide chains roughly seven agent hops against the framework's three-hop ceiling.").

**Acceptance Criteria:** Each named defect in the issue traces to a distinguishable source location, even without a full file list.

### S-002-04: Title leads with unexplained internal identifiers [MINOR]

**Counter-Argument:** "PROJ-032/BUG-001" prefixes the title before the plain-language gloss "(delegation redesign, PR #269)" appears at the end. A reader's first five words are two internal codes with no definition until the Tracking section, three paragraphs later.

**Response Required:** Lead with the plain-language question; move the internal ID to a trailing tag or the Tracking line only, e.g. "nuclear-sop: who may invoke agents mid-procedure? (delegation redesign, PR #269) — internal ref BUG-001".

### S-002-05: Descope option omits its own remaining requirements [MINOR]

**Counter-Argument:** The register states that even the "drop mid-procedure composition" descope still requires naming the correct quality-scoring mechanism consistently and publishing a hop-count budget for whatever remains composed. The issue's one-line descope note doesn't flag that trailing obligation, so a contributor who picks the descope path might consider the finding fully closed once composition is removed.

**Response Required:** Append: "Note: choosing this descope still requires correcting the quality-gate mechanism name and stating the hop budget for the remaining composed steps (see full analysis)."

## Recommendations

**P0 (MUST resolve):**
- S-002-01: Make the "full analysis" reference resolvable to the stated audience (link, or inline the candidate designs).

**P1 (SHOULD resolve):**
- S-002-02: Unify branch qualification across both repo-relative paths.
- S-002-03: Attribute the two defects to their two distinct source artifacts.

**P2 (MAY resolve):**
- S-002-04: Lead the title with plain language, not internal IDs.
- S-002-05: Note the residual requirement under the descope option.

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Negative | S-002-03: defect attribution incomplete; no file named for either sub-defect |
| Internal Consistency | 0.20 | Negative | S-002-02: branch qualifier applied inconsistently across sibling paths |
| Methodological Rigor | 0.20 | Neutral | Core technical claims (QG-HOLD, "invoke any other agent", missing return step) verified accurate against source files |
| Evidence Quality | 0.15 | Positive | Claims independently confirmed against `sop-executor.md` lines 77, 230, 247 |
| Actionability | 0.15 | Negative | S-002-01: the one path to concrete candidate designs is unreachable by the target audience |
| Traceability | 0.10 | Negative | S-002-04: leads with unexplained codes before plain-language framing |

**Result:** 1 Critical, 2 Major, 2 Minor. The design question itself is sound and factually grounded; the defect is entirely in reference resolvability and defect attribution, not in the accuracy of the core claim.
