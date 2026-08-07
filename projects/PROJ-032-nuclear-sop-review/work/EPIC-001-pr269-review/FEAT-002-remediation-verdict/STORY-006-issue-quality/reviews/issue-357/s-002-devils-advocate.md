# Devil's Advocate Report: GitHub Issue #357

**Strategy:** S-002 Devil's Advocate
**Deliverable:** `snapshots/final/issue-357.md` (geekatron/jerry issue #357)
**Criticality:** C4 (tournament execution)
**Date:** 2026-08-07
**Reviewer:** adv-executor (blind, S-002 group)
**H-16 Compliance:** Assumed satisfied by tournament group ordering (self-refine -> steelman -> challenge); no S-003 artifact was available to this blind execution to confirm directly.

## Summary

6 counter-arguments identified (1 Critical, 3 Major, 2 Minor). Every factual claim checked against the remediation register, log, verdict, and the c07033ce diff verified accurate — the issue does not misstate what was fixed. The defects are all in the "zero internal-governance-knowledge" contract the mission requires: an unexplained internal ID leads the title, a "Tracking" pointer aims the reader at a path they likely cannot resolve from their own branch, one of five registration files is cited without the completeness given its four siblings, and the "verify" command covers less ground than the claim it's meant to substantiate. Recommend REVISE.

## Findings Table

| ID | Finding | Severity | Evidence | Affected Dimension |
|----|---------|----------|----------|--------------------|
| S-002-01 | Title leads with unexplained internal codes | Major | `# GitHub issue #357: PROJ-032/BUG-008: nuclear-sop — ...` | Completeness |
| S-002-02 | "Tracking" section points to a likely-unresolvable internal path | Critical | `Tracking:` paragraph, line 14 | Actionability |
| S-002-03 | "the skill trigger map" cited without a path, unlike its 4 siblings in the same sentence | Major | Line 7, "...five files (`CLAUDE.md`, `AGENTS.md`, the skill trigger map, `plugin.json`, `CHANGELOG.md`)" | Completeness |
| S-002-04 | "How to verify" command scope narrower than the claim it verifies | Major | Line 9 claim vs. line 11 command | Internal Consistency |
| S-002-05 | No instruction for how/where to register disagreement | Minor | Line 5, "Nothing for you to do unless you disagree with the fix." | Actionability |
| S-002-06 | Empty `Assignees:` field is dead scaffolding | Minor | Line 3, "Assignees: " | Concision |

## Finding Details

### S-002-01: Title leads with unexplained internal codes [MAJOR]

**Claim Challenged:** The issue title begins `PROJ-032/BUG-008: nuclear-sop — docs claimed "not registered"...`.
**Counter-Argument:** `PROJ-032` and `BUG-008` are the maintainer's private review-project and worktracker IDs. They carry zero meaning to PR #269's author or their AI agent, who have no access to the PROJ-032 review artifacts. Leading the title with them primes the reader with governance jargon before a single self-contained word of explanation, and clutters GitHub search/notification previews with codes the reader can never resolve on their own.
**Evidence:** Title line 1; the body itself later explains the substance in plain language without needing these codes ("docs claimed... both corrected"), proving the codes are not load-bearing for the reader's understanding — they are pure maintainer bookkeeping that leaked into audience-facing text.
**Impact:** First-impression confusion; a diligent contributor may pause to search for "PROJ-032" or "BUG-008" before reading further, wasting a lookup cycle the mission explicitly disallows.
**Dimension:** Completeness (self-containedness)
**Response Required:** Move the codes out of the title (retain them only in the Tracking footer, per S-002-02's fix) or bracket them as clearly non-actionable, e.g. `[internal ref]`.
**Acceptance Criteria:** Title contains no bare internal ID as its first token; a reader unfamiliar with Jerry governance can parse the title's meaning without external context.

### S-002-02: "Tracking" section points to a likely-unresolvable internal path [CRITICAL]

**Claim Challenged:** `Tracking: worktracker projects/PROJ-032-nuclear-sop-review/work/BUG-008-registration-status-truth (register section REM-08 in remediation-register.md, under .../STORY-004-remediation/ on branch feat/proj-032-nuclear-sop-review).`
**Counter-Argument:** This is presented as a citable evidence trail, but it points the contributor at a directory tree and branch (`feat/proj-032-nuclear-sop-review`) that belongs to the maintainer's separate, in-progress internal review project — not to anything on `proj-0039-nuclear-engineer` (the contributor's own branch, correctly used elsewhere in this same issue) or to a GitHub-resolvable URL. Nothing in the text confirms this branch/path is pushed to the public remote, gives a permalink, or tells the reader this is maintainer-only bookkeeping they can safely ignore. An agent instructed to "verify tracking" will attempt to fetch or read a path it cannot locate from its own checkout, and either fail or burn tool calls discovering that it must switch to an unrelated branch of a different work area entirely.
**Evidence:** Compare to the "How to verify" line immediately above it, which correctly scopes its command to `proj-0039-nuclear-engineer` (the contributor's own branch) — the Tracking line breaks that pattern by referencing a different branch with no access instructions.
**Impact:** Sends the reader/agent down a dead-end lookup; undermines trust in the rest of the issue's otherwise-verifiable claims once this one reference fails to resolve.
**Dimension:** Actionability / Resolvable References
**Response Required:** Either (a) drop the Tracking line entirely — it adds no information the contributor can act on — or (b) replace it with a GitHub permalink to the specific file+line on the branch, explicitly labeled "maintainer-internal reference, not required reading."
**Acceptance Criteria:** Every path or branch reference in the issue is either resolvable from the contributor's own clone/fork or is explicitly labeled as internal-only and non-actionable.

### S-002-03: "the skill trigger map" cited without a path [MAJOR]

**Claim Challenged:** "...registered it in five files (`CLAUDE.md`, `AGENTS.md`, the skill trigger map, `plugin.json`, `CHANGELOG.md`)."
**Counter-Argument:** Four of the five items are given exact, code-formatted file paths the reader can open directly; the fifth ("the skill trigger map") is described only by function, forcing the reader to guess or search the repo for which file that is (`.context/rules/mandatory-skill-usage.md`). This is an internal inconsistency within a single sentence — the standard set for self-containedness is applied to 4/5 items and dropped for the 5th.
**Evidence:** Verified: the actual file is `.context/rules/mandatory-skill-usage.md`, confirmed changed in commit c07033ce's trigger-map row.
**Impact:** Minor but avoidable lookup cost; undermines the otherwise strong pattern of precise, backtick-quoted paths elsewhere in the same issue.
**Dimension:** Completeness
**Response Required:** Add the backtick path: `` the trigger map (`.context/rules/mandatory-skill-usage.md`) ``.
**Acceptance Criteria:** All five items in the list carry an explicit file path.

### S-002-04: "How to verify" command scope narrower than the claim it verifies [MAJOR]

**Claim Challenged:** "...the skill is approved for low-risk (C1–C2) use only, stated identically in SKILL.md, PLAYBOOK.md, the rules file, and the reference docs." followed by "How to verify: ... `git diff c07033ce^ c07033ce -- skills/nuclear-sop/SKILL.md skills/nuclear-sop/PLAYBOOK.md`."
**Counter-Argument:** The claim asserts identical treatment across four files; the verify command only lets the reader inspect two of them. A contributor who runs the given command and finds SKILL.md/PLAYBOOK.md consistent has not actually verified "stated identically" — the rules file (`skills/nuclear-sop/rules/nuclear-sop-behavior-rules.md`) and reference docs (`skills/nuclear-sop/docs/reference.md`) are asserted but not checkable via the supplied instructions. (Confirmed by ground truth: both files were in fact touched by c07033ce with matching C1-C2/withdrawn language — so the claim itself is true, but the reader has no way to confirm that from the issue alone.)
**Evidence:** c07033ce diff includes edits to `rules/nuclear-sop-behavior-rules.md` (NS-H-08) and `docs/reference.md` (NS-H-08 reference row) consistent with the claim, but neither path appears in the issue's verify command.
**Impact:** A skeptical reader (or an agent instructed to "verify before trusting") cannot fully substantiate a claim the issue asks them to accept on four-file scope with a two-file check.
**Dimension:** Internal Consistency
**Response Required:** Extend the diff command to all four files, or narrow the prose claim to match the two files actually offered for verification.
**Acceptance Criteria:** The verify command's file list is a superset of every file named in the preceding claim.

## Recommendations

**P0 (MUST resolve before acceptance):**
- S-002-02: Remove or convert the Tracking line to a resolvable/explicitly-internal reference.

**P1 (SHOULD resolve; justify if not):**
- S-002-01: Strip or bracket internal IDs from the title.
- S-002-03: Add the missing file path for "the skill trigger map."
- S-002-04: Align verify-command scope with the four-file claim (or narrow the claim).

**P2 (MAY resolve; acknowledgment sufficient):**
- S-002-05: Add one clause on where to raise disagreement (this issue or PR #269).
- S-002-06: Drop or populate the empty `Assignees:` line.

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Negative | S-002-01, S-002-03: internal codes and missing path force lookups outside the text |
| Internal Consistency | 0.20 | Negative | S-002-04: claim scope (4 files) exceeds verify scope (2 files) |
| Methodological Rigor | 0.20 | Neutral | No factual errors found against ground truth |
| Evidence Quality | 0.15 | Positive | All substantive technical claims independently verified accurate against c07033ce diff, register, and log |
| Actionability | 0.15 | Negative | S-002-02: primary "Tracking" reference likely non-resolvable by the target audience |
| Traceability | 0.10 | Neutral | Commit SHA, CI run link, and issue cross-reference (#353) all verified correct |

**Result:** No fabricated or inaccurate claims found — the issue's factual core is sound. The counter-arguments are entirely about the "zero internal-governance-knowledge" contract: one Critical (a non-resolvable internal pointer presented as verifiable evidence) and three Major findings (internal-ID-first title, one unpathed reference among five, and a verify command that under-covers its own claim). Addressing S-002-02 and S-002-01/03/04 would materially close the gap to the mission's self-containedness bar.
