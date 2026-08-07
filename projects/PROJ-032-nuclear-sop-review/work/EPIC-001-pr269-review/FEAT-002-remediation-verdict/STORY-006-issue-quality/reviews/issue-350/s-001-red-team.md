# Red Team Report: GitHub Issue #350 (BUG-001 / REM-01)

**Strategy:** S-001 Red Team Analysis
**Deliverable:** `projects/PROJ-032-nuclear-sop-review/.../STORY-006-issue-quality/snapshots/final/issue-350.md`
**Criticality:** C4
**Threat Actor:** An external PR #269 contributor (or their coding agent) with zero knowledge of this repo's internal governance, reading only the issue text and following its links literally, under time pressure to ship a fix that "closes the issue."
**H-16 Note:** No S-003 Steelman output was supplied in this invocation's context; executing as directed by the orchestrator. Findings below still apply regardless of steelman status.

## Summary

Issue #350 accurately restates the core REM-01 defect (mid-procedure delegation violates the one-level-deep agent rule, no suspend/resume, hop-ceiling exceeded) in plain, self-contained language, and its tracking links resolve to real files on the stated branch. The attack surface is not factual error — it is **incompleteness that narrows the contributor's design space**: the issue surfaces only the "give up" option from the source register while omitting the two constructive redesign candidates and a bundled naming-fix requirement, and its two file references are unclickable bare paths on a branch the contributor does not own. Recommendation: REVISE (not reject) — tighten the "design question" section and convert path references to links.

## Findings

| ID | Finding | Severity | Section |
|----|---------|----------|---------|
| S-001-01 | "Acceptable descope" is the only option surfaced; the two constructive redesign candidates from the register are dropped | Major | Body, "Acceptable descope" |
| S-001-02 | Bundled naming-fix requirement (ps-critic → adv-scorer) is not mentioned as part of this issue's scope | Major | Body, "design question" |
| S-001-03 | Register/worktracker references are bare paths on a non-PR branch, not clickable links | Major | Tracking |
| S-001-04 | Hop-ceiling violation stated qualitatively ("exceeds ... ceiling") without the concrete magnitude (~7 vs. 3) | Minor | Body, para 1 |
| S-001-05 | Title/tracking carry unglossed internal shorthand ("PROJ-032/BUG-001") | Minor | Title, Tracking |

## Finding Details

### S-001-01: Descope-only framing hides the two preferred redesign options [MAJOR]

**Attack Vector:** A contributor (or agent) reading only this issue sees exactly one path forward — delete mid-procedure agent composition and rewrite the flagship example. `remediation-register.md` REM-01 actually offers three candidate architectures: (a) QG-HOLD returns control to the main context (mirrors the existing IV-HOLD pattern), (b) the orchestrator executes any agent-invocation step directly, (c) drop the composition (what the issue shows). Presenting only (c) as "the acceptable" answer steers toward discarding the flagship capability instead of attempting a compliant redesign that preserves it.
**Evidence:** Issue text: "Acceptable descope: drop mid-procedure agent composition entirely..." — no mention of options (a)/(b). Register: "Candidate architectures to choose and specify: (a) ... (b) ... (c) mid-procedure composition is dropped."
**Countermeasure:** Add one line: "Other viable designs (see linked register): (a) return control to the main session at each gate, mirroring the existing hold pattern used elsewhere in this skill, or (b) have the invoking session perform the agent call directly instead of the sub-agent." Keep the descope as a fallback, not the only visible option.

### S-001-02: Naming-fix requirement is not surfaced as in-scope [MAJOR]

**Attack Vector:** The register states that whichever topology is chosen, the fix "must also: name [the actual S-014 implementer] (not [the wrong name]) as the S-014 implementer everywhere" — a ~8-file naming defect subsumed into this same cluster. The issue's design question and descope text say nothing about this; a contributor who fixes only the delegation topology ships an incomplete fix and the naming defect survives.
**Evidence:** Register REM-01 G3 and "Redesign question" closing sentence (naming-fix mandate). Issue body has no equivalent sentence.
**Countermeasure:** Append to the design question: "Whatever design you choose, also correct every place the workflow names the wrong quality-gate implementer as the S-014 scorer — the skill's own worked example already uses the correct name, so treat that as the reference."

### S-001-03: Cross-branch file references are unclickable [MAJOR]

**Attack Vector:** Both the worktracker path and `remediation-register.md` are given as bare relative paths qualified only by branch name (`feat/proj-032-nuclear-sop-review`) — a branch the external contributor's own PR (on a different branch) does not have checked out. A human or agent must know to `git fetch`/checkout a foreign branch by name before the path resolves; nothing in the issue signals that step is needed.
**Evidence:** Confirmed both paths exist as stated on that branch (verified directly), but no `https://github.com/...blob/...` URL or explicit "fetch this branch" instruction is given.
**Countermeasure:** Replace both bare paths with resolvable GitHub blob URLs, e.g. `https://github.com/geekatron/jerry/blob/feat/proj-032-nuclear-sop-review/projects/PROJ-032-nuclear-sop-review/work/EPIC-001-pr269-review/FEAT-002-remediation-verdict/STORY-004-remediation/remediation-register.md`, which resolve directly in a browser or via raw fetch without any local branch operation.

### S-001-04: Hop-ceiling violation lacks the concrete count [MINOR]

**Attack Vector:** "exceeds the framework's three-handoff routing ceiling" is true but unquantified; the source register gives "~7 Task hops vs the HARD 3-hop ceiling," a number useful as an acceptance-criteria target (e.g., "reduce to ≤3 hops or restructure so hop-counting doesn't apply").
**Countermeasure:** Add the number: "...exceeds the framework's three-handoff routing ceiling (the composed sequence needs roughly seven)."

### S-001-05: Unglossed tracking shorthand [MINOR]

**Attack Vector:** "PROJ-032/BUG-001" appears in the title with no inline gloss; a first-time external reader must infer it is an internal cross-reference ID rather than something actionable.
**Countermeasure:** Add a parenthetical on first use, e.g. "PROJ-032/BUG-001 (internal tracking ID for this review; see links below)."

## Recommendations

**P0:** None — no finding invalidates the issue's core factual content.
**P1:** S-001-01 (surface all three candidate designs), S-001-02 (state the bundled naming fix), S-001-03 (convert paths to links).
**P2:** S-001-04 (quantify hop count), S-001-05 (gloss tracking shorthand).

## Scoring Impact

| Dimension | Impact | Rationale |
|-----------|--------|-----------|
| Completeness | Negative | S-001-01, S-001-02: two of three candidate designs and a bundled sub-fix are omitted |
| Actionability | Negative | S-001-03: references don't resolve without out-of-band branch knowledge |
| Evidence Quality | Neutral | Core factual claims (H-01/P-003 quote, severity, paths) verified accurate |
| Traceability | Positive | Worktracker + register cross-references are correct and exist as stated |

---
*S-001 execution complete. 5 findings (0 Critical / 3 Major / 2 Minor). No H-16 blocking issue raised against this deliverable's factual content.*
