# FMEA Report: GitHub Issue #354 (PROJ-032/BUG-005 — H-36 governance ruling)

**Strategy:** S-012 FMEA (adapted for a ~300-word communication artifact)
**Deliverable:** `snapshots/final/issue-354.md` (live text of geekatron/jerry issue #354)
**Criticality:** C4 (tournament)
**Date:** 2026-08-07
**H-16 Compliance:** N/A for this executor invocation — S-012 applied directly to text; no prior strategy output consumed in this context.
**Elements Analyzed:** 6 | **Failure Modes Identified:** 4 | **Total RPN:** 576

## Summary

Decomposed the issue into 6 elements (title, assignees, "what this is about," "decision to make," tracking/severity line, worktracker+analysis-path+branch line). Cross-checked every factual claim (deadline, contradictory fallbacks, missing work-item, eng-team precedent: 8-step/10-agent, owner-authority framing) against `remediation-register.md` REM-05, `pr269-verdict.md`, and the live `nuclear-sop-behavior-rules.md`/`SKILL.md`/`skills/eng-team/SKILL.md` in the PR worktree — all substantive claims verified accurate. No Critical findings. Two Major findings concern precision of the "contradiction" framing and unverified resolvability of the cited branch reference. **Recommendation: ACCEPT with minor corrections** (targeted wording fixes only; no factual retraction needed).

## Findings Table

| ID | Element | Failure Mode | S | O | D | RPN | Severity | Affected Dimension |
|----|---------|-------------|---|---|---|-----|----------|---------------------|
| S-012-01 | "What this is about" paragraph | Incorrect: attributes a two-file contradiction to one file | 6 | 5 | 6 | 180 | Major | Evidence Quality |
| S-012-02 | Tracking footer (analysis path + branch) | Insufficient: branch reference unverified as remote-resolvable, not pinned to a commit | 8 | 4 | 6 | 192 | Major | Actionability |
| S-012-03 | "What this is about" paragraph | Insufficient: missing work-item ID not named | 4 | 4 | 3 | 48 | Minor | Completeness |
| S-012-04 | Title + tracking footer | Ambiguous/redundant: "(PR #269)" stated twice with no added information | 3 | 4 | 3 | 36 | Minor | Traceability |

## Finding Details

### S-012-01: Two-file contradiction described as one file's internal inconsistency

**Element:** "the file's two fallback instructions contradict each other (one says keep the current mode, the other says revert)"
**Failure Mode:** Incorrect — implies a self-contradiction within a single rule file.
**Effect:** Ground truth (`nuclear-sop-behavior-rules.md` NS-H-08, verified in the PR worktree) contains exactly **one** fallback instruction ("NS-H-08 remains as written" = keep 4-hop). The **contradicting** instruction ("default behavior is 3-hop mode... sop-verifier is eliminated") lives in `SKILL.md`'s "Governance Ruling Pending" section — a different file. A reader who opens only the rules file to find "two... instructions" will find one and may conclude the issue text is wrong, or waste time searching the wrong file.
**S/O/D rationale:** S=6 (confuses verification, doesn't invalidate the ask); O=5 (plausible a technical reader checks the cited file first); D=6 (not obvious without diffing both files).
**Corrective Action:** Reword to: "the skill's rule file and its top-level SKILL.md give contradicting fallback instructions (one says keep 4-hop mode, the other says revert to 3-hop)."
**Acceptance Criteria:** Text names both files (or says "across the skill's files") rather than "the file."
**Post-Correction RPN estimate:** ~40.

### S-012-02: Cited branch not confirmed resolvable / not pinned

**Element:** "Full analysis with candidate designs: `remediation-register.md`... on branch `feat/proj-032-nuclear-sop-review`."
**Failure Mode:** Insufficient — the reference depends on a live, mutable branch rather than a permalink, and there is no confirmation in the reviewed artifacts that this branch is pushed to the public remote the external contributor can fetch (as opposed to being a local/worktree-only branch used for this internal review).
**Effect:** If the branch is not pushed, or is later deleted/rebased/merged, the external contributor's only pointer to "full analysis with candidate designs" breaks with no fallback (no commit SHA given). This degrades actionability for the one paragraph the issue explicitly says has "candidate architectures."
**S/O/D rationale:** S=8 (the issue's single deep-dive pointer becomes dead with no recovery path); O=4 (plausible given the branch is described in this task's own context as a worktree branch); D=6 (contributor won't know until they try to fetch it).
**Corrective Action:** Either (a) confirm the branch is pushed and link `github.com/geekatron/jerry/blob/<branch>/.../remediation-register.md#rem-05...`, or (b) cite a specific commit SHA instead of a branch name so the reference survives branch deletion/rebase.
**Acceptance Criteria:** Reference resolves via a clickable GitHub URL or is pinned to a commit SHA.
**Post-Correction RPN estimate:** ~48.

## Recommendations

1. **S-012-01 (Major):** Fix the "one file" framing — name both files (rules file + SKILL.md) or generalize to "the skill's files."
2. **S-012-02 (Major):** Convert the branch reference to a clickable GitHub blob URL or commit SHA; confirm push status before relying on it as the primary "candidate designs" pointer.
3. **S-012-03 (Minor):** Optionally name the missing work-item ID (e.g., "cites `TASK-0039-H36-RULING`, which does not exist") for a self-verifying claim.
4. **S-012-04 (Minor):** Consider dropping the redundant "(PR #269)" from either the title or the closing line; concision opportunity only, no correctness issue.

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Neutral | Core narrative (deadline, contradiction, decision, blocking status) all present |
| Internal Consistency | 0.20 | Negative | S-012-01: framing implies a within-file contradiction that is actually cross-file |
| Methodological Rigor | 0.20 | Neutral | Owner-vs-contributor authority framing and precedent (eng-team 8-step/10-agent) independently verified accurate |
| Evidence Quality | 0.15 | Negative | S-012-01 evidence misattribution |
| Actionability | 0.15 | Negative | S-012-02: sole deep-dive pointer not confirmed durable/resolvable |
| Traceability | 0.10 | Negative | S-012-04 minor redundancy; S-012-03 unnamed work-item ID |

---
*S-012 execution by adv-executor (worker; no subagents invoked). Findings verified against remediation-register.md REM-05, pr269-verdict.md, and live repository files in the PR worktree.*
