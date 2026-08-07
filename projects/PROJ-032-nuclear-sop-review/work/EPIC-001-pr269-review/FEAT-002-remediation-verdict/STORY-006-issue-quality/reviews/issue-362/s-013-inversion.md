# Inversion Report: GitHub Issue #362 (BUG-013 composition-drift)

**Strategy:** S-013 Inversion Technique
**Deliverable:** `snapshots/final/issue-362.md` (live text of GitHub issue geekatron/jerry#362)
**Criticality:** C4 (tournament)
**Goals Analyzed:** 3 | **Assumptions Mapped:** 6 | **Vulnerable Assumptions:** 3 (1 Critical, 2 Major)

## Summary

Goal: PR #269's author must be able to trust the diagnosis and independently re-verify it using only the commands the issue gives them. Inverting that goal ("how would we guarantee they can't verify it, or verify the wrong thing?") surfaces one Critical defect: the issue attributes the "canonical" mislabel to the wrong file, and its own suggested `git diff` command excludes the file that actually changed — so following the issue's own verification instructions will not surface the fact it asserts. A second defect softens what was actually wrong with the maintainer's own reference source. Recommendation: REVISE (targeted text fixes; core diagnosis and fix summary are otherwise accurate).

## Findings Table

| ID | Assumption / Anti-Goal | Confidence | Severity | Evidence |
|----|------------------------|------------|----------|----------|
| S-013-01 | Assumption: "canonical" mislabel lived in SKILL.md | Low | Critical | PLAYBOOK.md diff + composition file self-headers |
| S-013-02 | Assumption: given `git diff` scope covers everything the text asserts | Low | Major | REM-13 affected-files list includes PLAYBOOK.md; verify command omits it |
| S-013-03 | Assumption: agents/sop-executor.md was already "full stop-work" | Medium | Major | evidence-c07033ce.md fix spec item 2 |
| S-013-04 | Anti-goal: dense single paragraph reduces scanability | N/A | Minor | "What was wrong" paragraph, ~140 words, 5 defects |
| S-013-05 | Anti-goal: unexplained internal label "worktracker" | N/A | Minor | Tracking footer |

## Finding Details

### S-013-01: "SKILL.md labeled ... canonical" is the wrong file [CRITICAL]

**Original claim:** "Meanwhile SKILL.md labeled the never-loaded `composition/` copy 'canonical.'"
**Inversion:** What if the reader opens SKILL.md looking for this label and doesn't find it? They wouldn't — per `evidence-c07033ce.md`, the "(canonical format)" label being corrected to "(derived artifacts)" is in **PLAYBOOK.md** (line ~167, and its References table rows ~207-210 say "Canonical agent definition"), not SKILL.md. Separately, each `composition/*.agent.yaml` file carries its own header comment "# Canonical Agent Definition" (unrelated to SKILL.md). SKILL.md's own diff in this commit is about withdrawing the C3+ approval and adding an Execution Directory note — it never contained a "canonical" composition label.
**Consequence:** A reader fact-checking this specific claim in SKILL.md will not find it, and may conclude the issue is unreliable or waste time searching the wrong file.
**Mitigation:** Change "SKILL.md labeled" to "PLAYBOOK.md labeled" (and optionally note the composition files' own "# Canonical Agent Definition" self-headers as a second source of the same claim).

### S-013-02: Verify command omits the file the "canonical" claim lives in [MAJOR]

**Original claim:** "run `git diff c07033ce^ c07033ce -- skills/nuclear-sop/composition/ skills/nuclear-sop/agents/ skills/nuclear-sop/SKILL.md`"
**Inversion:** What if the reader runs exactly this command to verify the "canonical" claim? `PLAYBOOK.md` — the file that actually carries the "(canonical format)" → "(derived artifacts)" relabel per REM-13's own "Affected files" list — is not in the diff's pathspec, so it will not appear in the output.
**Consequence:** The provided verification path is incomplete for the specific claim it's meant to support; compounds S-013-01.
**Mitigation:** Add `skills/nuclear-sop/PLAYBOOK.md` to the pathspec: `... skills/nuclear-sop/SKILL.md skills/nuclear-sop/PLAYBOOK.md`.

### S-013-03: "full stop-work in the agent file" overstates the original state [MAJOR]

**Original claim:** "The skill's own prompt-injection guard (its SEC-001 rule) shipped at three different strengths: full stop-work in the agent file, log-and-proceed in the composition prompt, and absent entirely from the composition YAML's forbidden actions."
**Inversion:** What if a reader assumes `agents/sop-executor.md` needed no fix and only the two composition copies did? Per `evidence-c07033ce.md`, the agent file itself had a self-contradiction — STOP-WORK instruction immediately followed by "and proceed with full STAR protocol unchanged" — that the *same* remediation commit deleted (fix spec item 2: "`agents/sop-executor.md` line ~142 → delete the tail"). So the reference source was not clean "full stop-work" pre-fix either.
**Consequence:** Understates the scope of what the maintainer patch touched; a reader skimming the diff for "the fix" might treat the agents/ copy as untouched baseline and skip reviewing its own change.
**Mitigation:** Reword to: "...shipped at three different strengths: stop-work in the agent file undercut by a contradictory tail telling the executor to proceed anyway, log-and-proceed in the composition prompt, and absent entirely from the composition YAML's forbidden actions."

### S-013-04: Dense single-paragraph defect list [MINOR]

The "What was wrong" paragraph packs 5 distinct defects (SEC-001 strength, verifier content/line-count loss, sop-brief loss, sop-capture loss, canonical mislabel) into one ~140-word sentence-run. A 4-5 line bullet list (one defect per line) would let the PR author's AI agent map each bullet directly to a diff hunk instead of re-parsing prose.

### S-013-05: Unexplained "worktracker" label [MINOR]

"Tracking: worktracker `projects/PROJ-032-nuclear-sop-review/work/BUG-013-composition-drift`..." uses "worktracker" as an unglossed label. The path itself resolves fine for a contributor who clones the repo, so this is low-impact, but a one-word gloss ("internal tracking id:") removes any ambiguity for a reader with zero framework context.

## Recommendations

- **MUST fix (Critical):** S-013-01 — correct file attribution for the "canonical" label.
- **SHOULD fix (Major):** S-013-02 — add PLAYBOOK.md to the verify command; S-013-03 — reword to acknowledge the agent file's own contradictory tail was also fixed.
- **MAY fix (Minor):** S-013-04 — bulletize "What was wrong"; S-013-05 — gloss "worktracker."

## Scoring Impact

| Dimension | Impact | Rationale |
|-----------|--------|-----------|
| Evidence Quality | Negative | S-013-01, S-013-03: two claims diverge from the cited ground truth |
| Actionability | Negative | S-013-02: the one verification command given doesn't cover the full claim set |
| Completeness | Neutral | Core diagnosis (four representations, drift categories, fix mechanism) is otherwise complete |
| Traceability | Neutral | Tracking footer (BUG-013, REM-13, branch) verified correct |
