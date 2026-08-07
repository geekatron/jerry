# Inversion Report: GitHub Issue #360 (BUG-011 / REM-11)

**Strategy:** S-013 Inversion Technique
**Deliverable:** `snapshots/final/issue-360.md` (live text of geekatron/jerry issue #360)
**Criticality:** C4 (tournament)
**H-16 Compliance:** N/A for this compact single-artifact execution (no prior S-003 pass supplied to this agent)
**Goals Analyzed:** 4 | **Assumptions Mapped:** 5 | **Vulnerable Assumptions:** 2

## Summary

Goal: an external contributor/AI agent with zero repo-governance knowledge must be able to trust and act on this text alone. Inverting "what guarantees this fails" surfaced one **Critical** vulnerability: the issue's own literal "How to verify" grep command does not do what the text says it does — running it against the real branch produces two non-empty (false-positive) matches, directly contradicting the stated "returns nothing" expectation. One **Minor** staleness-of-local-clone assumption and one **Minor** unverifiable-count claim were also found. Recommendation: **REVISE** — fix the verification command before this issue is safe to hand to an agent that will execute it literally.

## Findings Table

| ID | Assumption / Anti-Goal | Type | Confidence | Severity | Evidence | Affected Dimension |
|----|------------------------|------|------------|----------|----------|--------------------|
| S-013-01 | The stated grep command detects leftover `.md` artifacts and returns nothing on the fixed branch | Assumption | High (tested) | Critical | Verified against `skills/nuclear-sop/` in the checked-out branch worktree | Evidence Quality / Actionability |
| S-013-02 | Contributor's local clone already has commit `c07033ce` (and its parent) fetched | Assumption | Medium | Minor | Maintainer pushed directly to contributor's branch; no fetch/pull instruction given | Actionability |
| S-013-03 | "one of seven mechanical fixes" is verifiable by the reader from this issue alone | Assumption | Medium | Minor | No cross-links to sibling issues #357–#363 | Completeness |

## Finding Details

### S-013-01: Verification command contradicts its own stated result [CRITICAL]

**Original Assumption:** The issue tells the reader to run `grep -rn "experience/.*\.md" skills/nuclear-sop/` and states it "returns nothing" as proof the `.yaml` fix is complete.

**Inversion:** What if this assumption is wrong? Tested directly against the branch worktree — it is wrong. The command returns 2 hits:
- `skills/nuclear-sop/agents/sop-capture.md:200` — `` `docs/experience/{entry_id}.yaml` -- persistence location for future sop-brief retrieval (matches behavior-rules.md OE Search Mechanism ...` ``
- `skills/nuclear-sop/examples/c3-adr-workflow-definition.md:126` — `` | `docs/experience/` | Exists or sop-brief will present options per sop-brief.md STEP 4 ... |``

Both are false positives: the unanchored `.*` in the pattern greedily matches across the line to an unrelated `.md` filename (`sop-brief.md`, `behavior-rules.md`) mentioned later in the same sentence — not to a real `docs/experience/*.md` artifact. The underlying fix (all real occurrences are now `.yaml`) is genuinely complete; only the verification command is broken.

**Plausibility:** Certain — reproduced directly, not inferred.
**Consequence:** An external agent instructed to "check that ... returns nothing" and told to act on that result will get a non-empty result and reasonably conclude the maintainer's fix is incomplete or the issue is unverified — false-negative confidence in a fix that actually worked, wasted investigation time, or an erroneous re-opened concern on a closed-should-stay-closed issue.
**Evidence:** Reproduced against the live PR worktree (`skills/nuclear-sop/` tree checked out from the referenced commit).
**Dimension:** Evidence Quality (0.15) / Actionability (0.15).
**Mitigation:** Replace the pattern with one anchored to the actual defect string so it cannot cross line boundaries into unrelated filenames, e.g. `grep -rn "entry_id}\.md" skills/nuclear-sop/` (0 hits expected), or restrict the middle group to non-whitespace/non-backtick characters: `grep -rnE "(experience|oe-entry)[/-][^ \`]*\.md" skills/nuclear-sop/`.
**Acceptance Criteria:** The corrected command, run verbatim against the branch, returns 0 hits — matching the text's claim.

### S-013-02: No fetch/pull step before the diff command [MINOR]

**Original Assumption:** The contributor's local git clone already contains commit `c07033ce`.
**Inversion:** The maintainer pushed this commit directly to the contributor's remote branch (per the issue's own "What this is" line); the contributor's local checkout may predate that push, in which case `git diff c07033ce^ c07033ce -- skills/nuclear-sop/` fails with "unknown revision."
**Consequence:** A stalled/confused first verification attempt; low severity because the error message itself points toward "fetch first."
**Mitigation:** Prepend `git fetch origin proj-0039-nuclear-engineer && git diff c07033ce^ c07033ce -- skills/nuclear-sop/`.

### S-013-03: "seven mechanical fixes" is an unlinked, unverifiable count [MINOR]

**Original Assumption:** The reader can trust "one of seven" without a way to check it.
**Inversion:** If the reader wants to confirm this is 1-of-7 (not 1-of-N), the issue gives no path to do so.
**Consequence:** Minor trust gap; doesn't block acting on this specific issue, only the surrounding-context claim.
**Mitigation:** Add a parenthetical, e.g. "(the other six are #357–#359, #361–#363)."

## Recommendations

- **Critical (MUST fix):** S-013-01 — replace the grep pattern per the mitigation above before merge/close; this is the only reference in the issue a reader is told to *execute and trust the output of*.
- **Minor (MAY fix):** S-013-02 — add a fetch step. S-013-03 — cross-link sibling issues.

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Evidence Quality | 0.15 | Negative | S-013-01: the cited proof-of-fix command is factually wrong when executed |
| Actionability | 0.15 | Negative | S-013-01 (false verification result), S-013-02 (missing fetch step) |
| Completeness | 0.20 | Negative | S-013-03: "seven fixes" claim unlinked |
| Internal Consistency | 0.20 | Neutral | Text is internally consistent otherwise (branch, commit, CI link all cross-check) |
| Methodological Rigor | 0.20 | Neutral | No methodology claims beyond the verification instruction |
| Traceability | 0.10 | Positive | Tracking line correctly resolves to `work/BUG-011-oe-artifact-contract/` |

**Result:** 1 Critical, 2 Minor assumption vulnerabilities. All other factual claims checked against ground truth (commit `c07033ce`, branch `proj-0039-nuclear-engineer`, CI run 31174766440, `.yaml`/workflow_id-primary/Section 11 fix description) were confirmed accurate.
