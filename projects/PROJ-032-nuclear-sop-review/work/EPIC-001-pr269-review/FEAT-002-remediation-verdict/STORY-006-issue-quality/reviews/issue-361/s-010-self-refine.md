# S-010 Self-Refine — Issue #361

| Field | Value |
|-------|-------|
| Strategy | S-010 Self-Refine |
| Deliverable | GitHub issue #361 (geekatron/jerry) — `snapshots/final/issue-361.md` |
| Criticality | C4 (tournament) |
| Iteration | 1 of 1 |

## Summary

Every factual claim in the issue checks out against the remediation register (REM-12), the
remediation log, and the `c07033ce` diff: the three-way state-machine divergence, the
COMPLETED-before-capture/boolean-vs-path completion contract break, the "if accessible"
fail-open verifier check, the branch name, the commit hash, and the CI run link are all
accurate. No Critical (misleading/wrong-path) findings. The gaps are Minor/Major
actionability and concision issues: a "how to verify" command that isn't scoped to just
this fix, one imprecise path reference, and a dense unbroken paragraph.

## Findings Table

| ID | Finding | Severity | Evidence | Dimension |
|----|---------|----------|----------|-----------|
| S-010-01 | Verify command not scoped to this fix alone | Major | `git diff c07033ce^ c07033ce -- skills/nuclear-sop/` also surfaces REM-08/09/10/11/13/14 hunks | Actionability |
| S-010-02 | Worktracker tracking path is a directory, not a file | Minor | Cites `work/BUG-012-state-machine-contract`; actual file is `.../BUG-012-state-machine-contract.md` | Traceability |
| S-010-03 | Title front-loads unexplained internal codes | Minor | "PROJ-032/BUG-012: ..." precedes any gloss of what those codes mean | Completeness |
| S-010-04 | "What was wrong" is one dense run-on paragraph for 3 distinct defects | Minor | Three parenthetical-heavy claims crammed into a single paragraph | Actionability |
| S-010-05 | Redundant "on your branch" | Minor | Appears once naming the branch, again as a trailing clause two sentences later | Internal Consistency |
| S-010-06 | Vague paraphrase of the source artifact | Minor | "the PR's own compliance gate" instead of naming the QG-E6 report | Evidence Quality |

## Finding Details

**S-010-01: Verify command bundles six unrelated clusters**
- **Severity:** Major
- **Evidence:** Commit `c07033ce` implements all seven FIX-NOW clusters (REM-08..14) in one commit; `composition/sop-verifier.prompt.md` and `SKILL.md` are touched by both REM-12 and other clusters (e.g., REM-13's guard restoration also edits `composition/sop-executor.prompt.md`/`.agent.yaml`; REM-08's C3+ rewrite sits in the same `SKILL.md` hunk as the SEC-008 line).
- **Impact:** A contributor or their agent running the given command to "verify" this specific issue gets a diff full of unrelated changes (registration text, schema fixes, nav tables) with no way to isolate the state-machine/completion-contract/SEC-008 changes this issue describes. That undermines the "resolvable references" and "actionability" goals of the issue.
- **Recommendation:** Either scope the diff to the exact files (`templates/PROCEDURE_STATE.template.yaml agents/sop-executor.md agents/sop-capture.md agents/sop-verifier.md composition/sop-verifier.prompt.md` + executor/capture composition twins), or give the precise grep checks the register itself already prescribes for REM-12, e.g. `grep -n "if accessible" skills/nuclear-sop/agents/sop-verifier.md skills/nuclear-sop/composition/sop-verifier.prompt.md` (expect 0 hits) and `grep -n "execution_log_final" skills/nuclear-sop/` (expect only path semantics, no `: true` checks).

**S-010-06: Name the source artifact precisely**
- **Severity:** Minor
- **Evidence:** Register text: "recorded OPEN, RPN-144, REMEDIATION REQUIRED, and a blocking condition for C3+ in the PR's own QG-E6 report." Issue text: "the PR's own compliance gate had flagged as remediation-required."
- **Impact:** "Compliance gate" is accurate in spirit but not a term the PR author's own artifacts use; naming "QG-E6 report" would let them (or their agent) grep straight to it.
- **Recommendation:** Replace "the PR's own compliance gate" with "the PR's own QG-E6 report."

## Recommendations (priority order)

1. **(Major, S-010-01)** Scope the "How to verify" step to REM-12's actual file set or swap in the register's own grep checks so verification isn't diluted by six unrelated clusters.
2. **(Minor, S-010-02)** Append the filename to the worktracker path in the Tracking line.
3. **(Minor, S-010-06)** Say "QG-E6 report" instead of "compliance gate."
4. **(Minor, S-010-04)** Break the three-item "What was wrong" paragraph into an actual markdown list (already numbered (1)(2)(3) inline — promote to bullets).
5. **(Minor, S-010-03 / S-010-05)** Move/gloss the `PROJ-032/BUG-012` codes at the end of the title rather than the start; drop the second "on your branch" clause.

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Neutral | Core what/why/fix/verify/tracking structure present; S-010-03 is a minor gap |
| Internal Consistency | 0.20 | Negative | S-010-05 minor redundancy; no contradictions found |
| Methodological Rigor | 0.20 | Neutral | N/A (communication artifact, not a methodology) |
| Evidence Quality | 0.15 | Negative | S-010-06 — paraphrase weaker than naming the exact source artifact |
| Actionability | 0.15 | Negative | S-010-01 (Major) and S-010-04 are real friction for a reader trying to verify or scan quickly |
| Traceability | 0.10 | Negative | S-010-02 — worktracker reference one segment short of a resolvable file path |

## Decision

**Outcome:** Ready for external/tournament review — no Critical findings; all factual claims verified against the remediation register, remediation log, and the `c07033ce` diff.

**Rationale:** Zero Critical findings after full ground-truth cross-check (branch name, commit hash, CI link, all three technical defects, and the fix description all confirmed accurate). One Major actionability gap (verify-command scope) and five Minor polish items remain.

**Next Action:** Apply S-010-01 (scope the verify command) before other adversarial strategies weigh in; the remaining Minor items can be batched into the same revision pass.
