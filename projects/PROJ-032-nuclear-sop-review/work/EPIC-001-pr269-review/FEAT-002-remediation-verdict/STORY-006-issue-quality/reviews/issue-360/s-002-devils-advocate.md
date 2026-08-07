# Devil's Advocate Report: GitHub Issue #360 (BUG-011 / REM-11 — OE artifact contract)

**Strategy:** S-002 Devil's Advocate (adapted for a ~300-word communication artifact)
**Deliverable:** `projects/PROJ-032-nuclear-sop-review/.../STORY-006-issue-quality/snapshots/final/issue-360.md`
**Criticality:** C4 (tournament)
**Date:** 2026-08-07
**Reviewer:** adv-executor (S-002)
**H-16 Compliance:** N/A — executor invoked directly for this tournament lane; no prior S-003 output supplied in context.

## Summary

1 counter-argument identified (1 Critical). The issue's factual claims about the fix content (extensions, retrieval protocol, Section 11 step, commit, CI) all check out against the actual post-fix branch content. But the one executable instruction the issue gives the reader — the verification grep — is empirically false on the real branch: it claims the command "returns nothing" when it actually returns two hits. Recommend REVISE (single line fix).

## Findings Table

| ID | Finding | Severity | Evidence | Affected Dimension |
|----|---------|----------|----------|--------------------|
| S-002-01 | "How to verify" grep command is factually false as written | Critical | Issue line 11: `grep -rn "experience/.*\.md" skills/nuclear-sop/` claimed to return nothing. Run against the actual `proj-0039-nuclear-engineer` worktree at the post-fix state, it returns 2 hits: `examples/c3-adr-workflow-definition.md:126` ("`docs/experience/` \| Exists or sop-brief will present options per sop-brief.md STEP 4...") and `agents/sop-capture.md:200` ("`docs/experience/{entry_id}.yaml` -- ... matches behavior-rules.md OE Search Mechanism..."). Both are false positives: the greedy `.*` spans past the `.yaml` extension to an unrelated `.md` filename mentioned later in the same line (`sop-brief.md`, `behavior-rules.md`). | Evidence Quality / Actionability |

## Finding Details

### S-002-01: Verification command claim is false on the actual branch [CRITICAL]

**Claim Challenged:** "How to verify: ... check that `grep -rn "experience/.*\.md" skills/nuclear-sop/` returns nothing."

**Counter-Argument:** This is the one piece of the issue an external agent is explicitly told to *execute* to confirm the fix. It fails on the real repository state. An agent following the instruction literally will get 2 lines of output where it was promised silence — a direct contradiction between the issue's claim and the observable outcome, on the artifact's single verification step.

**Evidence:** Verified directly against the branch checkout: `grep -rn "experience/.*\.md" skills/nuclear-sop/` returns:
```
examples/c3-adr-workflow-definition.md:126:| `docs/experience/` | Exists or sop-brief will present options per sop-brief.md STEP 4 OE path handling |
agents/sop-capture.md:200:2. `docs/experience/{entry_id}.yaml` -- persistence location for future sop-brief retrieval (matches behavior-rules.md OE Search Mechanism Glob pattern)
```
Note the register's own fix-spec validation command (REM-11 item 7) is narrower and correctly scoped: `grep -rn "experience/.*\.md\|oe-entry-.*\.md"` still has the same greedy-match weakness, but that internal artifact was never meant to be handed to an external reader as a literal command — this issue text is.

**Impact:** An agent or contributor running the literal command will see unexpected output and reasonably conclude either (a) the fix is incomplete, or (b) the issue's claims elsewhere (extension unification, "returns nothing") cannot be trusted — undermining confidence in the rest of an otherwise accurate issue. Best case, it costs the reader a manual investigation to realize the hits are false positives; worst case, it triggers unnecessary pushback or a reopened investigation on an already-fixed defect.

**Dimension:** Evidence Quality (the verification claim doesn't match reality); Actionability (the instruction doesn't work as given).

**Response Required:** Replace the grep pattern with one that cannot match an unrelated trailing `.md` filename, and/or tell the reader what a hit would mean.

**Acceptance Criteria:** Revised command returns zero hits on the actual fixed branch, e.g. anchor the extension to the entry-ID token: `grep -rn 'experience/{entry_id}\.md\|oe-entry-.*\.md' skills/nuclear-sop/` (still same weakness) — better: `grep -rnE 'docs/experience/\{?[a-zA-Z_]*entry_id\}?\.md|oe-entry-.*\.md' skills/nuclear-sop/`, or simplest and robust: instruct the reader to check that no OE write/read path ends in `.yaml` being written as `.md`, e.g. `grep -rn '\.yaml\.md\|entry_id}\.md' skills/nuclear-sop/` — or just drop the illustrative command and say "confirm `docs/experience/{entry_id}.yaml` is the only extension referenced for OE entries across the skill's templates, baselines, and examples."

## Recommendations

- **P0 (S-002-01):** Fix or remove the "How to verify" grep command before this issue is treated as closed/verified. Suggested minimal fix: append a caveat — "(hits referencing other `.md` files like `sop-brief.md` in the same line are false positives; look only for entry-ID/OE-path patterns ending in `.md`)" — or replace with a command that doesn't false-positive on the current tree (see Acceptance Criteria above).

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Neutral | All substantive fix claims (extension unification, retrieval protocol, Section 11 step, commit, CI) verified accurate against the branch. |
| Internal Consistency | 0.20 | Negative | The issue's own "returns nothing" claim contradicts the observable command output (S-002-01). |
| Methodological Rigor | 0.20 | Negative | The one verification step offered was not itself verified against the real tree before publishing. |
| Evidence Quality | 0.15 | Negative | S-002-01: the cited verification evidence is wrong. |
| Actionability | 0.15 | Negative | S-002-01: the given command does not do what it claims for a reader trying to act on it. |
| Traceability | 0.10 | Positive | Tracking section correctly resolves to the actual worktracker path and register section (verified: `work/BUG-011-oe-artifact-contract/`). |

## Execution Statistics
- **Total Findings:** 1
- **Critical:** 1
- **Major:** 0
- **Minor:** 0
- **Protocol Steps Completed:** 5 of 5 (adapted scope)
