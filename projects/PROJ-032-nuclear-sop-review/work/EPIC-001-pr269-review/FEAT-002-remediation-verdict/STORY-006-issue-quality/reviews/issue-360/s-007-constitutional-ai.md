# Constitutional Compliance Report: GitHub Issue #360 (BUG-011 — OE artifact contract)

**Strategy:** S-007 Constitutional AI Critique (adapted for a ~300-word communication artifact)
**Deliverable:** `projects/PROJ-032-nuclear-sop-review/.../STORY-006-issue-quality/snapshots/final/issue-360.md`
**Criticality:** C4 (tournament)
**Date:** 2026-08-07
**Reviewer:** adv-executor (S-007)
**Constitutional Context:** Principles applied via the mission's explicit criteria (factual accuracy, self-containedness, actionability, resolvable references, honest severity/status, concision) — mapped to P-001 (Truth/Accuracy) and P-022 (No Deception). Ground truth: remediation register REM-11, remediation-log, evidence-c07033ce.md (full diff), pr269-verdict.md.

## Summary

PARTIAL compliance: 0 Critical, 1 Major, 2 Minor. Every substantive factual claim in the issue text (branch, commit, cluster count, the `.yaml`/`.md` contradiction, the unsatisfiable AC-7, the three-way retrieval-protocol drift, the missing Section 11 write, and the CI link) was independently verified against the diff and register and found **accurate**. The one Major finding concerns the verification command's precision, not the issue's factual content. Score: 0.91 (REVISE — one point below PASS on verification-instruction rigor alone). Recommend one targeted edit; otherwise ready.

## Findings Table

| ID | Principle | Tier | Severity | Evidence | Affected Dimension |
|----|-----------|------|----------|----------|--------------------|
| S-007-01 | Actionability / resolvable references (P-001) | MEDIUM | Major | "How to verify" `git diff c07033ce^ c07033ce -- skills/nuclear-sop/` scopes to the whole skill directory | Actionability |
| S-007-02 | Evidence completeness (P-001) | SOFT | Minor | Verify grep `"experience/.*\.md"` omits the `oe-entry-.*\.md` alternation the register's own validate step uses | Evidence Quality |
| S-007-03 | Self-containedness (P-022) | SOFT | Minor | Title/body lead with bare ID `PROJ-032/BUG-011` before any gloss | Completeness |

## Finding Details

### S-007-01: Verify command scope includes six unrelated bundled fixes [MAJOR]

**Principle:** Actionability — a verification instruction given to an external contributor should let them confirm *this issue's* claim without wading through unrelated diffs.
**Location:** "How to verify" paragraph, line 11: `git diff c07033ce^ c07033ce -- skills/nuclear-sop/`
**Evidence:** Commit `c07033ce`'s own message is "fix(nuclear-sop): PROJ-032 maintainer remediation — FIX-NOW clusters REM-08..14" (evidence-c07033ce.md, commit stat). It bundles 7 remediation clusters (registration/status truth, registration surfaces, agent-schema conformance, OE artifact contract, state-machine reconciliation, composition drift, navigation tables) touching 29 files, at least 20 of which are under `skills/nuclear-sop/` and unrelated to the OE `.yaml`/`.md` defect this issue describes (e.g., `SKILL.md` C3+ status rewrite, `composition/sop-verifier.agent.yaml` YAML-parse fix, nav-table additions).
**Impact:** Running the suggested command shows the contributor a large, mixed diff. They cannot tell from the command alone which hunks substantiate *this* issue's claim vs. the six sibling issues tracking the other REM-08..14 clusters from the same commit — undermining the "verify independently" purpose of the section and risking confusion about scope (P-001: the command technically works, but doesn't isolate the evidence it's offered as).
**Remediation:** Scope the diff to the OE-artifact-contract files only, e.g.: `git diff c07033ce^ c07033ce -- skills/nuclear-sop/templates/POST_JOB_BRIEF.template.md skills/nuclear-sop/behavioral-baselines/bb-003-oe-feedback-loop-integrity.md skills/nuclear-sop/examples/c3-adr-workflow-definition.md skills/nuclear-sop/agents/sop-brief.md skills/nuclear-sop/agents/sop-capture.md skills/nuclear-sop/composition/`. Alternatively, keep the broad command but add one sentence: "Note: this commit bundles 7 maintainer fixes tracked in separate issues; the OE-artifact-contract changes are in the files listed above."

### S-007-02: Verify grep pattern narrower than the authoritative validation check [MINOR]

**Principle:** Evidence Quality — a self-verification command should test the full claim it stands in for.
**Location:** "How to verify" paragraph, line 11: `grep -rn "experience/.*\.md" skills/nuclear-sop/`
**Evidence:** REM-11's own fix specification (remediation-register.md, REM-11 item 7) validates with two alternations: `grep -rn "experience/.*\.md\|oe-entry-.*\.md" skills/nuclear-sop/` → 0 hits. The diff confirms a pre-fix instance that the issue's single-pattern grep would **not** have caught on its own: `bb-003-oe-feedback-loop-integrity.md` line ~75 read `capture/oe-entry-{entry_id}.md` (no "experience/" substring) before the fix (evidence-c07033ce.md, bb-003 diff hunk). Post-fix this returns 0 hits either way, so the issue's claim is not currently false — but the given command is a weaker regression check than the one the register itself relies on.
**Remediation:** Add the second alternation to match the register's own validation: `grep -rn "experience/.*\.md\|oe-entry-.*\.md" skills/nuclear-sop/`.

### S-007-03: Bare ID leads the title/tracking before any gloss [MINOR]

**Principle:** Self-containedness (P-022 adjacent — not deceptive, but requires the reader to infer purpose from an opaque code before context arrives).
**Location:** Title: "PROJ-032/BUG-011: nuclear-sop — ..."; Tracking footer: `` worktracker `projects/PROJ-032-nuclear-sop-review/work/BUG-011-oe-artifact-contract` ``
**Evidence:** The title's leading token `PROJ-032/BUG-011` is not glossed anywhere until the final line. It is a real, resolvable worktracker path (verified: `projects/PROJ-032-nuclear-sop-review/work/BUG-011-oe-artifact-contract/BUG-011-oe-artifact-contract.md` exists) — so it is not a broken or fabricated reference — but a reader with zero internal-governance context sees an unexplained code first.
**Impact:** Low — the body immediately below the title explains the defect in plain terms, and the ID is not needed to act on the fix (the issue explicitly says "nothing for you to do"). This is polish, not a blocker.
**Recommendation:** Optional: move the tracking ID to a trailing parenthetical after a plain-language title, e.g., "nuclear-sop: lessons-learned files written as `.yaml` but documented as `.md` (PROJ-032/BUG-011, fixed on your branch)".

## Remediation Plan

**P0 (Critical):** None.
**P1 (Major):** S-007-01 — scope or annotate the `git diff` verify command so it isolates OE-artifact-contract evidence from the other six bundled REM-08..14 fixes.
**P2 (Minor):** S-007-02 — add the `oe-entry-.*\.md` alternation to the verify grep. S-007-03 — consider leading with plain language before the tracking ID (optional).

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Neutral | All required facts (what/why/fix/tracking) present |
| Internal Consistency | 0.20 | Neutral | No contradictions found against ground truth |
| Methodological Rigor | 0.20 | Negative | S-007-01: verify command not scoped to the claim it supports |
| Evidence Quality | 0.15 | Negative | S-007-02: weaker regression grep than the register's own check |
| Actionability | 0.15 | Negative | S-007-01: contributor cannot cleanly isolate relevant diff |
| Traceability | 0.10 | Positive | Tracking line resolves to a real worktracker path and register section, independently verified |

**Constitutional Compliance Score:** 0.91 (1 Major @ −0.05, 2 Minor @ −0.02 each = −0.09; 1.00 − 0.09 = 0.91)
**Threshold Determination:** REVISE (0.85–0.91 band; one targeted edit — narrowing S-007-01 — would clear 0.92 PASS)
