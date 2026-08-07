# Devil's Advocate Report: GitHub Issue #362 (BUG-013 composition drift)

**Strategy:** S-002 Devil's Advocate
**Deliverable:** `snapshots/final/issue-362.md` (live text of geekatron/jerry issue #362)
**Criticality:** C4 (tournament)
**H-16 Compliance:** Assumed satisfied by tournament group ordering (steelman group precedes challenge group); no S-003 output visible to this blind execution.

## Summary

3 counter-arguments confirmed against ground truth (2 Critical, 3 Minor). The issue's core narrative (four drifted representations, SEC-001 weakened to log-and-proceed, verifier isolation contract dropped) checks out against the diff and `plugin.json`. But one specific factual claim — which file mislabeled `composition/` as "canonical" — misattributes the defect to the wrong file, and the issue's own "How to verify" command excludes the file where that exact fix actually landed. An external contributor following the verification instructions literally will not find that claim substantiated. Recommend REVISE: fix the file attribution and either add `PLAYBOOK.md` to the verify command or drop the claim.

## Findings Table

| ID | Finding | Severity | Evidence |
|----|---------|----------|----------|
| S-002-01 | "SKILL.md labeled ... 'canonical'" misattributes the file | Critical | evidence-c07033ce.md diff |
| S-002-02 | Verify command omits the file where that claim's fix actually landed | Critical | issue text + diff scope |
| S-002-03 | "full stop-work in the agent file" hides a pre-existing self-contradiction the same commit removed | Minor | evidence-c07033ce.md sop-executor.md diff |
| S-002-04 | "runtime self-delegation check" undersells the restored guardrail's scope | Minor | evidence-c07033ce.md sop-verifier.prompt.md diff |
| S-002-05 | "what `plugin.json` actually loads" is stated for both `.md` and `.governance.yaml`, but plugin.json's agent list only enumerates the `.md` paths | Minor | plugin.json |

## Finding Details

### S-002-01: Wrong file blamed for the "canonical" mislabel [CRITICAL]

**Claim Challenged:** "Meanwhile SKILL.md labeled the never-loaded `composition/` copy 'canonical.'"
**Counter-Argument:** This is the wrong file. The diff shows exactly one occurrence of the label being changed: `PLAYBOOK.md` line ~167, `**Composition files (canonical format):**` → `**Composition files (derived artifacts):**`. `SKILL.md`'s changes in this commit (registration status, C3+ status, file structure, references) never contain the word "canonical" as a mislabel — the only "canonical" strings added to SKILL.md describe the `agent-canonical-v1.schema.json` schema name, an unrelated, correct usage.
**Impact:** An external contributor who greps `SKILL.md`'s history for "canonical" to confirm this specific claim will find nothing, undermining confidence in the rest of the issue.
**Response Required:** Change "SKILL.md" to "PLAYBOOK.md" in the "What was wrong" paragraph.

### S-002-02: Verify command can't substantiate the claim it's attached to [CRITICAL]

**Claim Challenged:** "How to verify: ... run `git diff c07033ce^ c07033ce -- skills/nuclear-sop/composition/ skills/nuclear-sop/agents/ skills/nuclear-sop/SKILL.md`."
**Counter-Argument:** The remediation register's own "Affected files" list for this cluster names `PLAYBOOK.md` explicitly, and that is where the "(canonical format)" → "(derived artifacts)" edit actually is. The given command's path list (`composition/`, `agents/`, `SKILL.md`) never touches `PLAYBOOK.md`, so it cannot show the one change the "canonical" sentence is describing — compounding S-002-01 rather than offsetting it.
**Impact:** A contributor who runs exactly the suggested command to sanity-check the issue will see real SEC-001/isolation-contract restorations (those claims verify fine) but will not find any "canonical" text change anywhere in the diff they ran, since it isn't in scope.
**Response Required:** Add `skills/nuclear-sop/PLAYBOOK.md` to the `git diff` path list (or drop the "canonical" sentence if it isn't being kept).

### S-002-03: "full stop-work in the agent file" implies that file was already clean [MINOR]

**Claim Challenged:** "The skill's own prompt-injection guard (its SEC-001 rule) shipped at three different strengths: full stop-work in the agent file, log-and-proceed in the composition prompt, and absent entirely from the composition YAML's forbidden actions."
**Counter-Argument:** `agents/sop-executor.md`'s pre-fix SEC-001 text ended "...invoke STOP-WORK (D-2) **and proceed with full STAR protocol unchanged**" — a self-contradiction (stop work, then proceed unchanged) that this same commit deleted. Describing the `.md` file simply as "full stop-work" implies it was the clean reference copy the other two were resynced from, when it too needed a one-line fix.
**Response Required:** Optional tightening only (Minor): note the agent file's own tail was also corrected, not just the composition copies. Acknowledgment sufficient given "What the fix changed" already covers the substance.

### S-002-04: Restored guardrail is broader than "self-delegation check" [MINOR]

**Claim Challenged:** "...dropped the caller-responsibility notice, the entire context-isolation contract, and the runtime self-delegation check."
**Counter-Argument:** The restored block (composition/sop-verifier.prompt.md, "P-003 Runtime Self-Check") enforces four things: no Task-tool invocation, no Write/Edit/Bash at all (T1 read-only), no instructing the orchestrator to delegate, and single-level execution. "Self-delegation check" names only one of four checks and omits the read-only enforcement half entirely.
**Response Required:** Acknowledgment sufficient; optionally reword to "runtime self-check (no delegation, no writes)".

### S-002-05: "what plugin.json actually loads" overstates governance.yaml's role [MINOR]

**Claim Challenged:** "the normative source is `agents/{name}.md` plus `agents/{name}.governance.yaml`, which is what `plugin.json` actually loads."
**Counter-Argument:** Verified `.claude-plugin/plugin.json`'s `agents` array on the PR branch: it lists only the four `agents/sop-*.md` paths. `.governance.yaml` files are not referenced anywhere in plugin.json — they're a same-name companion file loaded by Claude Code's governance validation convention, not by plugin.json's manifest. The sentence attaches "what plugin.json actually loads" to both files when it's only true of the `.md` file.
**Response Required:** Acknowledgment sufficient; the overall conclusion (agents/ pair is normative, composition/ is derived) is unaffected.

## Recommendations

- **P0:** S-002-01, S-002-02 — correct the file attribution and either extend the verify command to include `PLAYBOOK.md` or remove the unverifiable claim. Both are concrete, checkable text edits.
- **P2:** S-002-03, S-002-04, S-002-05 — optional wording tightenings; none block acceptance.

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Neutral | Core drift narrative and fix scope are covered |
| Internal Consistency | 0.20 | Negative | S-002-01/02: the "canonical" claim and its own verify instructions point at different, non-overlapping files |
| Methodological Rigor | 0.20 | Neutral | — |
| Evidence Quality | 0.15 | Negative | S-002-01: a specific, named-file factual claim does not match the diff |
| Actionability | 0.15 | Negative | S-002-02: the prescribed verify command cannot confirm one of the issue's own claims |
| Traceability | 0.10 | Positive | Tracking footer correctly distinguishes the PR branch from the review branch and cites a resolvable register path |
