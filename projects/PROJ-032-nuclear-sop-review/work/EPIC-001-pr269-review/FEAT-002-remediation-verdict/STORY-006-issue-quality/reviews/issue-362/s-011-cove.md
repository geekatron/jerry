# Chain-of-Verification Report: GitHub issue #362 (BUG-013 composition drift)

**Strategy:** S-011 Chain-of-Verification
**Deliverable:** `snapshots/final/issue-362.md` (live text of geekatron/jerry issue #362)
**Criticality:** C4 (tournament)
**Date:** 2026-08-07
**H-16 Compliance:** S-003 Steelman output present in sibling review directory (not read; blindness constraint) -- indirect compliance assumed per protocol
**Claims Extracted:** 9 | **Verified:** 7 | **Discrepancies:** 2 (0 Critical, 1 Major, 1 Minor)

## Summary

Nine testable claims were extracted (fix count, branch/commit identifiers, CI run, three-representation SEC-001 drift description, line-count comparison, tracking path) and checked independently against `remediation-register.md` REM-13, `BUG-013-composition-drift.md`, `evidence-c07033ce.md`'s full diff, and the PR worktree. Seven claims verify exactly; the "How to verify" command is technically executable but its path scope commingles REM-13's fix with six unrelated FIX-NOW clusters bundled into the same commit (Major); the "full stop-work in the agent file" characterization omits that the pre-fix agent file itself carried a self-contradicting tail that also required a targeted fix (Minor). Recommendation: REVISE (2 correctable text changes; no factual claim is false).

## Claim Inventory and Independent Verification

| CL | Claim (issue text) | Source | Result |
|----|--------------------|--------|--------|
| CL-01 | "one of seven mechanical fixes ... in commit `c07033ce`" | remediation-register.md L23-25 (7 FIX-NOW clusters REM-08..14); evidence-c07033ce.md commit header | VERIFIED |
| CL-02 | Branch `proj-0039-nuclear-engineer`, commit `c07033ce` | evidence-c07033ce.md L1; BUG-013 frontmatter | VERIFIED |
| CL-03 | "four representations ... with no precedence rule" | REM-13 Group G5 ("Four unreconciled representations per agent with no precedence rule") | VERIFIED |
| CL-04 | SEC-001 at three strengths: full stop-work (agent file) / log-and-proceed (composition prompt) / absent (composition YAML) | REM-13 G1 and BUG-013 Summary L25 | MATERIAL DISCREPANCY -- see CV-002 |
| CL-05 | Verifier composition prompt 214 lines vs. 324-line agent file; dropped caller-responsibility notice, isolation contract, self-delegation check | REM-13 G3 (verbatim "214 vs 324 lines... CALLER RESPONSIBILITY NOTICE... FC-M-001 Context Isolation Contract... P-003 Runtime Self-Check") | VERIFIED |
| CL-06 | Other copies lost Bash read-only restriction, trigger keywords, deviation-classification rules | REM-13 G2 (Bash), G4 (Triggers list), G5 (deviation classification) | VERIFIED |
| CL-07 | SKILL.md labeled never-loaded `composition/` copy "canonical" | REM-13 G5; PLAYBOOK.md diff L167 "(canonical format)" -> "(derived artifacts)" | VERIFIED |
| CL-08 | Fix: every `composition/` file gets a derived-artifact header; normative source `agents/{name}.md` + `.governance.yaml`, "what `plugin.json` actually loads" | Fix spec item 1; `.claude-plugin/plugin.json` L53-56 lists only `agents/sop-*.md` | VERIFIED (plugin.json confirmed; source note also credits "Claude Code" as a second loader, omitted but not incorrect) |
| CL-09 | Verify command: `git diff c07033ce^ c07033ce -- skills/nuclear-sop/composition/ skills/nuclear-sop/agents/ skills/nuclear-sop/SKILL.md`; CI 15/15 green, run 31174766440 | evidence-c07033ce.md L1-40 (commit stat: 29 files touched across 7 clusters); CI link verbatim match | MINOR DISCREPANCY -- see CV-001 (command is accurate but not scoped to this defect) |

## Findings

### S-011-01: Verification command surfaces six unrelated clusters' changes, not just BUG-013's [MAJOR]

**Claim (from deliverable):** "How to verify: ... run `git diff c07033ce^ c07033ce -- skills/nuclear-sop/composition/ skills/nuclear-sop/agents/ skills/nuclear-sop/SKILL.md`."

**Independent verification:** `evidence-c07033ce.md`'s commit stat shows all 7 FIX-NOW clusters (REM-08..14) landed in the single commit `c07033ce`. REM-13's own affected-files list (register L331) is only `composition/` (8 files) + `agents/sop-executor.md` + `agents/sop-brief.governance.yaml` + `SKILL.md` + `PLAYBOOK.md`. The suggested command's `agents/` glob additionally pulls in `sop-brief.md`, `sop-capture.md`, `sop-capture.governance.yaml`, `sop-executor.governance.yaml`, `sop-verifier.md`, `sop-verifier.governance.yaml` -- six files whose diffs belong to REM-10 (schema/AD-M-011), REM-11 (OE artifact contract), and REM-12 (state-machine reconciliation), not composition drift. The `SKILL.md` scope also pulls in REM-08/REM-09/REM-04 registration and STAR-gate text unrelated to this defect.

**Discrepancy:** The command is real and will run successfully, but a contributor following it to "verify" BUG-013 specifically will see a diff dominated by unrelated schema, OE-contract, and registration changes, with no signal distinguishing which hunks are the composition-drift fix this issue describes.

**Severity:** Major -- could mislead a reader into thinking those unrelated changes are part of this defect, or cause them to miss the actual composition-drift diff inside the noise.

**Dimension:** Actionability

**Correction:** Narrow the command to the files REM-13 actually owns, e.g.:
`git diff c07033ce^ c07033ce -- skills/nuclear-sop/composition/ skills/nuclear-sop/agents/sop-executor.md skills/nuclear-sop/agents/sop-brief.governance.yaml skills/nuclear-sop/SKILL.md skills/nuclear-sop/PLAYBOOK.md`
and add one sentence noting other files under `agents/` changed in the same commit for unrelated fixes (issues #350-#356 territory), so the reader isn't confused by adjacent hunks if they run a broader diff anyway.

### S-011-02: "Full stop-work in the agent file" overstates the pre-fix agent file's correctness [MINOR]

**Claim (from deliverable):** "shipped at three different strengths: full stop-work in the agent file, log-and-proceed in the composition prompt, and absent entirely from the composition YAML's forbidden actions."

**Independent verification:** REM-13 G1 and `BUG-013-composition-drift.md` L25 both describe the agent file's pre-fix state as "log + reject + STOP-WORK, but with the contradictory tail 'and proceed with full STAR protocol unchanged'" -- i.e., the agent file's own STOP-WORK was immediately undercut by an instruction to proceed unchanged. `evidence-c07033ce.md`'s diff (agents/sop-executor.md hunk) confirms this exact tail was deleted as part of the fix.

**Discrepancy:** The issue's two-word gloss "full stop-work" implies the agent file was the clean, correct copy and only the other two needed fixing. In fact all three representations had defects; the agent file's defect was a self-contradiction, not an absence.

**Severity:** Minor -- does not change the reader's required action (nothing to do; already fixed) and doesn't affect verification, but slightly understates how pervasive the drift was.

**Dimension:** Evidence Quality

**Correction:** Replace "full stop-work in the agent file" with "stop-work in the agent file (undercut by a contradictory 'proceed unchanged' tail that was also deleted in the fix)."

## Recommendations

- **Major:** S-011-01 -- rescope the verify command to REM-13's actual file set (or caveat the broader one).
- **Minor:** S-011-02 -- correct the agent-file characterization to acknowledge its own pre-fix contradiction.

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Neutral | No missing sections for the mission's purpose |
| Internal Consistency | 0.20 | Neutral | No contradictions within the issue text itself |
| Methodological Rigor | 0.20 | Negative | S-011-01: verify command not scoped to the claimed defect |
| Evidence Quality | 0.15 | Negative | S-011-02: agent-file strength overstated vs. source |
| Actionability | 0.15 | Negative | S-011-01 directly degrades a reader's ability to verify just this defect |
| Traceability | 0.10 | Positive | Tracking path, register section, and commit/CI citations all resolve and match ground truth exactly |
