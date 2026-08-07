# S-010 Self-Refine — GitHub Issue #362

| Field | Value |
|-------|-------|
| Strategy | S-010 Self-Refine |
| Deliverable | GitHub issue #362 (`snapshots/final/issue-362.md`) — BUG-013 / REM-13 composition drift |
| Criticality | C4 (tournament) |
| Date | 2026-08-07 |
| Iteration | 1 of 1 (compact communication-artifact review) |

## Summary

The issue is well-scoped and mostly evidence-consistent (branch, commit, CI link, worktracker path, and the five drift sub-defects all check out against `remediation-register.md` REM-13 and the `evidence-c07033ce.md` diff). One claim is factually wrong in a way that misdirects verification: the text attributes the "canonical format" mislabel to `SKILL.md`, but the commit diff shows only `PLAYBOOK.md` carried that literal label change — and the "How to verify" `git diff` command omits `PLAYBOOK.md` entirely, so a reader following the instructions cannot see the evidence for the claim as written. One Major gap (undefined internal artifact names forcing a lookup) and one Minor polish item round out the findings. Not ready to ship as-is; fix S-010-01 before merge/close.

## Findings Table

| ID | Finding | Severity | Evidence | Affected Dimension |
|----|---------|----------|----------|--------------------|
| S-010-01 | "SKILL.md labeled ... canonical" misattributes the file, and the verify command omits the actually-affected file | Critical | Diff shows `-**Composition files (canonical format):**` only in `skills/nuclear-sop/PLAYBOOK.md` (evidence-c07033ce.md); SKILL.md's composition-related hunk is purely additive (new File Structure entry), no canonical→derived text swap present | Evidence Quality / Resolvable References |
| S-010-02 | Named artifacts ("caller-responsibility notice", "context-isolation contract", "runtime self-delegation check") are not defined in-text | Major | Issue body, "What was wrong" paragraph, sentence 2 | Self-Containedness / Actionability |
| S-010-03 | No pointer to the other six FIX-NOW sibling issues for readers wanting the full remediation picture | Minor | Issue says "one of seven mechanical fixes" with no cross-reference | Completeness |

## Finding Details

### S-010-01: File misattribution + incomplete verify command

- **Severity:** Critical
- **Evidence:** `evidence-c07033ce.md` diff hunk for `skills/nuclear-sop/PLAYBOOK.md` line 167: `-**Composition files (canonical format):**` → `+**Composition files (derived artifacts):**` (plus the four "Canonical agent definition" rows in PLAYBOOK.md's References table). The full `skills/nuclear-sop/SKILL.md` diff hunk (same evidence file) contains no such label change — its composition-related edit is a net-new `File Structure` block that never previously listed `composition/` at all.
- **Impact:** The issue tells the reader "SKILL.md labeled the never-loaded composition/ copy 'canonical.'" This is the specific, checkable claim a diligent contributor or their agent would verify first — and the issue's own "How to verify" command (`git diff c07033ce^ c07033ce -- skills/nuclear-sop/composition/ skills/nuclear-sop/agents/ skills/nuclear-sop/SKILL.md`) does not include `PLAYBOOK.md`, so running it will not surface the evidence for the claim as stated. A reader trusting the text and the command together will conclude the claim is unverifiable or hunt in the wrong file.
- **Recommendation:** Change "SKILL.md labeled" to "PLAYBOOK.md labeled" (or "SKILL.md and PLAYBOOK.md," matching the register's affected-files list, if a second pre-fix instance genuinely existed in SKILL.md — verify before choosing wording), and add `skills/nuclear-sop/PLAYBOOK.md` to the git diff path list.

### S-010-02: Undefined internal artifacts force a lookup

- **Severity:** Major
- **Evidence:** "the entire context-isolation contract, and the runtime self-delegation check" — neither term is defined, and both name specific sections (`FC-M-001` isolation contract, `P-003` self-check with HALT per the register) that only appear in `agents/sop-verifier.md`.
- **Impact:** An external contributor's agent cannot judge whether "the isolation-contract text" is safety-critical or cosmetic without opening a file the issue never names. Since the issue's stated action is "nothing to do," this doesn't block acceptance, but it undercuts the "verify it yourself" offer the issue makes.
- **Recommendation:** Add a 4-6 word gloss, e.g. "the entire context-isolation contract (rules for what a delegated Task prompt must not contain)."

## Recommendations

1. **Fix S-010-01** (Critical) — correct the file name and expand the verify command's path list. Blocking.
2. **Address S-010-02** (Major) — one short parenthetical gloss; low effort, improves self-containedness.
3. **Consider S-010-03** (Minor) — one sentence or link to the sibling FIX-NOW issues; optional.

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Neutral | Core drift defects (SEC-001, sop-verifier drops, sop-brief/sop-capture losses) all present and accurate |
| Internal Consistency | 0.20 | Negative | S-010-01: text claim and verify command disagree with each other and with the diff |
| Methodological Rigor | 0.20 | Neutral | N/A (not a methodology deliverable) |
| Evidence Quality | 0.15 | Negative | S-010-01 fails direct diff cross-check |
| Actionability | 0.15 | Negative | S-010-02 forces an out-of-band lookup |
| Traceability | 0.10 | Positive | Commit hash, CI run, worktracker path, and register section all resolve correctly |

## Decision

**Outcome:** Needs revision.

**Rationale:** One Critical evidence/reference error (S-010-01) fails the "resolvable references" and "factual accuracy" bars the mission sets; the verify command as written cannot substantiate the claim it's attached to.

**Next Action:** Revise per S-010-01 before this issue is treated as verified/closeable; S-010-02/03 are optional polish.
