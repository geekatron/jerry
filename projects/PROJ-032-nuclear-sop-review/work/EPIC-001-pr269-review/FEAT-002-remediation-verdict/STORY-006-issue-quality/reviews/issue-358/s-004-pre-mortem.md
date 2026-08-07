# Pre-Mortem Report: GitHub Issue #358 (issue-358.md)

**Strategy:** S-004 Pre-Mortem Analysis (adapted for a ~300-word communication artifact)
**Deliverable:** `.../STORY-006-issue-quality/snapshots/final/issue-358.md` (GitHub issue #358, geekatron/jerry)
**H-16 Note:** No prior S-003 Steelman output was supplied to this execution; proceeding per explicit tournament-executor instructions (blind, single-strategy assignment) rather than halting on an H-16 gate that governs full-tournament sequencing, not this isolated run.
**Failure Scenario:** It is six months from now. PR #269's external contributor (or their AI agent), acting on this issue text alone, either (a) wastes time trying to open a path that isn't a file, (b) runs a verification command that fails on their platform, or (c) is unsure whether they still owe the maintainer a response — because the text left a gap the pre-mortem below anticipates.

## Summary

The issue text is factually accurate against all checked ground truth (three-part "what was wrong," the fix description, the commit SHA, the CI link, and the 89→93 arithmetic all verify cleanly against the evidence pack, remediation register REM-09, and remediation log). No Critical failure causes were found. Two Major/Minor gaps concern resolvability and cross-platform actionability of the verification instructions. **Recommendation: ACCEPT with minor polish** — no factual corrections needed, only tightening of two references.

## Findings Table

| ID | Failure Cause | Category | Likelihood | Severity | Priority |
|----|---------------|----------|------------|----------|----------|
| S-004-01 | Tracking path is a directory, not a resolvable file path | Technical | Medium | Major | P1 |
| S-004-02 | `git diff c07033ce^ ...` caret syntax is not cross-shell portable | Technical | Low | Minor | P2 |
| S-004-03 | Verification command silently assumes the commit is already fetched locally | Process | Low | Minor | P2 |
| S-004-04 | "worktracker" used without definition in the Tracking footer | Assumption | Low | Minor | P2 |

## Finding Details

### S-004-01: Tracking path is a directory, not a resolvable file [MAJOR]

**Failure Cause:** The Tracking line gives `projects/PROJ-032-nuclear-sop-review/work/BUG-009-registration-enforcement-surfaces` as the worktracker reference. On disk this is a **directory**; the actual entity file is `.../BUG-009-registration-enforcement-surfaces/BUG-009-registration-enforcement-surfaces.md`. An agent that tries to read the path literally (e.g., `cat` or a file-read tool call) gets an "is a directory" error and must guess the filename convention before it can resolve the reference.
**Evidence:** Issue line 14 vs. verified filesystem path `projects/PROJ-032-nuclear-sop-review/work/BUG-009-registration-enforcement-surfaces/BUG-009-registration-enforcement-surfaces.md`.
**Likelihood:** Medium — this is the only place in the issue that isn't self-resolving; everything else (the diff command, the CI link) works exactly as written.
**Mitigation:** Append the filename: `.../BUG-009-registration-enforcement-surfaces/BUG-009-registration-enforcement-surfaces.md`.

### S-004-02: Caret syntax in verification command [MINOR]

**Failure Cause:** `git diff c07033ce^ c07033ce -- ...` uses `^` to mean "parent commit." This is standard in POSIX shells (bash/zsh) but `^` is a special escape character in `cmd.exe` and requires quoting in PowerShell, so a Windows contributor pasting the command verbatim into those shells may see a broken command.
**Evidence:** Issue line 11.
**Mitigation:** Use the more portable `c07033ce~1` form, or add a one-word parenthetical ("bash/zsh").

### S-004-03: No fetch/pull instruction before verification [MINOR]

**Failure Cause:** The verification step assumes `c07033ce` is already present in the reader's local clone. Since the maintainer pushed this commit directly to the contributor's branch, a reader who hasn't pulled since won't have it, and `git diff` will fail with "unknown revision" rather than a self-explanatory message.
**Evidence:** Issue line 11 ("on `proj-0039-nuclear-engineer`, run...").
**Mitigation:** Prepend "after pulling the latest `proj-0039-nuclear-engineer`" to the verify instruction.

### S-004-04: Unexplained "worktracker" term [MINOR]

**Failure Cause:** "worktracker" is Jerry-internal vocabulary, used without definition in the Tracking footer. It does not block action (the footer is provenance-only, not part of "what was wrong" / "how to verify"), so impact is cosmetic.
**Evidence:** Issue line 14 ("Tracking: worktracker `projects/...`").
**Mitigation:** Optional — replace with "internal tracking reference" or leave as-is since the footer is explicitly non-actionable.

## Recommendations

- **P1:** S-004-01 — complete the tracking path with its filename.
- **P2 (polish, optional):** S-004-02, S-004-03, S-004-04 — improve verification-command portability and footer clarity; none block understanding or action.

## Scoring Impact

| Dimension | Impact | Rationale |
|-----------|--------|-----------|
| Completeness | Neutral | All required "what/why/how to verify" elements present |
| Internal Consistency | Positive | No contradictions found against ground truth |
| Evidence Quality | Positive | Every claim (registration gaps, misroute, count, commit, CI) verified against source artifacts |
| Actionability | Negative (minor) | S-004-01 forces one extra lookup step |
| Traceability | Positive | Commit, CI run, and register section (REM-09) all correctly cited |

**Overall assessment:** Proceed with monitoring — targeted polish only, no rework required.
