# Steelman Report: GitHub Issue #360 (BUG-011 / REM-11 — OE artifact `.yaml`/`.md` contract)

## Steelman Context
- **Deliverable:** `.../STORY-006-issue-quality/snapshots/final/issue-360.md`
- **Deliverable Type:** Communication artifact (GitHub issue text for an external PR contributor + their agent)
- **Strategy:** S-003 (Steelman Technique), adapted for a ~300-word artifact
- **Steelman By:** adv-executor | **Date:** 2026-08-07

## Summary

**Steelman Assessment:** The narrative content (what was wrong, what changed, why it matters) is factually accurate against the remediation register, log, and commit evidence, and is well self-contained — no unexplained governance jargon gates understanding. The one load-bearing defect is in the "How to verify" reproduction step: the exact grep command given does not do what the issue implies it does.
**Improvement Count:** 1 Critical, 0 Major, 1 Minor
**Original Strength:** High — narrative claims (7 fixes, `.yaml` vs `.md` split across template/baseline/example, three-way retrieval-protocol drift, unimplemented Attachments-write promise) all verified true against `remediation-register.md` REM-11, the `c07033ce` diff, and the live post-fix worktree.
**Recommendation:** Targeted fix to the verification command; issue is otherwise ready.

## Findings

| ID | Severity | Finding | Section |
|----|----------|---------|---------|
| S-003-01 | Critical | "How to verify" grep command does not return nothing when actually run — both over-matches (false positive) and under-matches (misses the sibling `.md` pattern) | How to verify |
| S-003-02 | Minor | "workflow-ID-primary search protocol" is stated without a one-clause gloss of what "primary" means in practice | What the fix changed |

---

### S-003-01: Verification command is unreliable (Critical)

**Original text:**
> **How to verify:** on `proj-0039-nuclear-engineer`, run `git diff c07033ce^ c07033ce -- skills/nuclear-sop/`, and check that `grep -rn "experience/.*\.md" skills/nuclear-sop/` returns nothing.

**Evidence — this command does NOT return nothing when run against the actual post-fix worktree** (verified directly against the PR branch checkout):

```
skills/nuclear-sop/examples/c3-adr-workflow-definition.md:126:| `docs/experience/` | Exists or sop-brief will present options per sop-brief.md STEP 4 OE path handling |
skills/nuclear-sop/agents/sop-capture.md:200:2. `docs/experience/{entry_id}.yaml` -- persistence location for future sop-brief retrieval (matches behavior-rules.md OE Search Mechanism Glob pattern)
```

Both are false positives: the unanchored `.*` greedily matches across table-cell/parenthetical boundaries to an unrelated `.md` filename later on the same line (`sop-brief.md`, `behavior-rules.md`), not to the OE-entry extension itself. A contributor or their agent who runs the command exactly as instructed gets non-empty output contradicting the issue's implied "clean" result — the single most concrete, executable claim in the issue is the one that fails on execution. This is also incomplete in the other direction: it only searches for the literal substring `experience/`, so it cannot catch the sibling defect pattern `capture/oe-entry-{entry_id}.md`, which was part of the same fix (per REM-11 and the `bb-003`/`sop-capture.md` diffs) but contains no `experience/` substring.

**Rationale:** Critical because the verification step is the one piece of the issue an agent is most likely to execute literally and trust the output of; a wrong result here either produces false alarm (agent thinks the fix regressed) or false confidence (agent doesn't notice the check was never checking the right thing).

**Suggested fix:** Replace the command with a path-character-anchored pattern that cannot cross line boundaries into unrelated filenames, and include both known filename shapes:

```
grep -rnE '(experience/|oe-entry-)[A-Za-z0-9_{}.-]+\.md' skills/nuclear-sop/
```

(Verified locally: returns zero matches against the post-fix worktree, where the original command returns two false-positive matches.)

---

### S-003-02: "workflow-ID-primary" left unglossed (Minor)

**Original text:**
> `.yaml` and the workflow-ID-primary search protocol are now the single convention everywhere...

**Analysis:** Accurate (matches REM-11 G2: rules define `workflow_id` as the primary retrieval key, with `workflow_type` as a post-read filter only), but a reader unfamiliar with the skill has no way to tell what changed in practice from this phrase alone — it names the fixed convention without saying what the old, wrong behavior was.

**Suggested fix:** Add a four-word parenthetical: "...workflow-ID-primary search protocol (not workflow-type-only) are now the single convention everywhere..." — makes the before/after concrete without adding a sentence.

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Neutral | Narrative fully covers the defect and fix; gap is isolated to one command |
| Internal Consistency | 0.20 | Neutral | No contradictions found elsewhere in the text |
| Methodological Rigor | 0.20 | Negative (pre-fix) | Verification instruction was not itself tested against the actual branch |
| Evidence Quality | 0.15 | Positive | All narrative claims independently confirmed against register/log/diff |
| Actionability | 0.15 | Negative (pre-fix) | A literal-execution agent gets a misleading result from the one command given |
| Traceability | 0.10 | Positive | Tracking block correctly resolves to `BUG-011-oe-artifact-contract` / REM-11 |
