# Red Team Report: GitHub Issue #363 (BUG-014 nav tables)

**Strategy:** S-001 Red Team Analysis
**Deliverable:** `snapshots/final/issue-363.md` (live text of geekatron/jerry issue #363)
**Criticality:** C4 (tournament)
**Threat Actor:** A resource-constrained reader — the external PR #269 author or their AI agent — who acts on this issue text alone, without independently re-deriving the facts, and who may scan only the title or run the given commands literally rather than cross-checking every clause.
**H-16:** Not gated for S-001 in this invocation (executed directly per orchestrator instruction); no S-003 output supplied.

## Summary

Core facts (commit `c07033ce`, CI run 31174766440, file list, worktracker/issue mapping REM-14→BUG-014→#363, 23/25-template and 3/5-template claims) were verified byte-for-byte against the remediation register, remediation log, and the actual pre/post-fix diff and are **accurate**. The defects found are structural/framing, not fabrication: the verification command silently mixes in six unrelated fixes, the title's "(fixed)" tag contradicts the body's "stays open" instruction, and one line count is off by one. **Recommendation: REVISE** (Critical + Major findings below; no rewrite of the core narrative needed).

## Findings

| ID | Finding | Severity |
|----|---------|----------|
| S-001-01 | Verify command's diff bundles 6 unrelated fixes into the same files | Critical |
| S-001-02 | Title "(fixed on your branch)" contradicts body's "stays open" | Major |
| S-001-03 | Example file line count off by one (559 vs. 560) | Minor |
| S-001-04 | Tracking footer exposes unexplained internal path/ID jargon | Minor |
| S-001-05 | `git diff c07033ce^` depends on commit surviving future rebase | Minor |

### S-001-01: Verify command output is not scoped to this issue's fix [CRITICAL]

**Evidence:** The issue's "How to verify" step tells the reader to run `git diff c07033ce^ c07033ce -- skills/nuclear-sop/templates/ skills/nuclear-sop/examples/ skills/nuclear-sop/SKILL.md skills/nuclear-sop/PLAYBOOK.md skills/nuclear-sop/docs/reference.md`. Commit `c07033ce` is one squashed commit implementing **all seven** FIX-NOW clusters (REM-08..14), not just REM-14. Direct inspection of the diff confirms every one of those five paths also carries unrelated changes: `SKILL.md` and `docs/reference.md` both get the nav-table row *and* the C3+-approval-withdrawal rewrite (REM-08/REM-04); `PLAYBOOK.md` gets nav rows *and* the same C3+ withdrawal text; `examples/c3-adr-workflow-definition.md` gets the nav table *and* two `.md`→`.yaml` extension fixes (REM-11); `templates/` gets nav tables *and* `PROCEDURE_STATE.template.yaml`/`POST_JOB_BRIEF.template.md` contract changes (REM-11/REM-12).
**Why this matters:** The issue frames itself as one isolated, low-stakes "mechanical fix... nothing for you to do." Running the literal verify command instead surfaces a substantive, contestable change (C3+ approval withdrawn) with no signpost that it belongs to a different issue (#357/#360/#361). A reader or agent could reasonably (a) assume the C3+ withdrawal is part of "nothing to disagree with," or (b) post a dispute about it on the wrong issue thread.
**Fix:** Either scope the command to just the added block (e.g. append `| grep -B2 -A20 "^+## Document Sections"`), or add one sentence: "Note: commit `c07033ce` also contains fixes for issues #357, #360, #361 in these same files — only the `## Document Sections` table additions belong to this issue."

### S-001-02: Title/body status contradiction risks wrong auto-action [MAJOR]

**Evidence:** Title ends "(fixed on your branch)"; body says "this issue stays open only until PR #269's disposition is decided."
**Why this matters:** An agent or triage tool that scans issue titles in bulk (a common pattern for large PR review backlogs) may treat "(fixed)" as a closure signal and auto-close, overriding the body's explicit open-until-disposition condition — the opposite of the intended, deliberately conservative close-only-after-merge policy.
**Fix:** Change the title suffix to "(fix applied on your branch — issue stays open pending PR disposition)" or drop the parenthetical from the title and state status only in the body.

### S-001-03: Off-by-one line count (Minor)

**Evidence:** Issue states `c3-adr-workflow-definition.md` was "559 lines" pre-fix. Diff hunk `@@ -4,6 +4,23 @@` adds 17 net lines; current file is 577 lines; 577 − 17 = 560, not 559.
**Fix:** Correct to 560, or drop the exact count if not independently re-verified.

### S-001-04: Unexplained internal tracking codes (Minor)

**Evidence:** Footer cites `register section REM-14`, `EPIC-001-pr269-review`, `FEAT-002-remediation-verdict`, `STORY-004-remediation` with no gloss. (Confirmed the branch/path is publicly resolvable, so not a dead link — but the codes are meaningless to a reader with zero governance context, violating the stated self-containedness mission even though no action depends on them.)
**Fix:** Add a 3-word parenthetical ("internal maintainer reference only") or drop the path, keeping just the worktracker line and issue number.

### S-001-05: Verify command has no fallback if history is rewritten (Minor)

**Evidence:** `git diff c07033ce^ c07033ce` requires both the commit and its parent to remain reachable on `proj-0039-nuclear-engineer`; a future rebase/force-push of that branch (common during a multi-issue rework cycle) would break the command with no guidance offered.
**Fix:** Add a one-line fallback: "If this commit is no longer on the branch, compare via the GitHub PR Files tab filtered to the paths above."

## Scoring Impact

| Dimension | Impact | Rationale |
|-----------|--------|-----------|
| Evidence Quality | Negative | S-001-01, S-001-03 |
| Actionability | Negative | S-001-01, S-001-02 |
| Internal Consistency | Negative | S-001-02 |
| Completeness | Neutral | Core facts otherwise complete |
| Traceability | Positive | REM-14→BUG-014→#363 chain fully verified |

---
*S-001 execution complete. 5 findings (1 Critical, 1 Major, 3 Minor). Fresh-context review; no other strategy outputs consulted.*
