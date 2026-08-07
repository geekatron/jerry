# Steelman Report: GitHub Issue #356 (BUG-007 — executor command gating)

## Steelman Context
- **Deliverable:** `projects/PROJ-032-nuclear-sop-review/work/EPIC-001-pr269-review/FEAT-002-remediation-verdict/STORY-006-issue-quality/snapshots/final/issue-356.md`
- **Deliverable Type:** GitHub issue text (communication/specification artifact, ~300 words)
- **Criticality Level:** C4 (tournament execution)
- **Strategy:** S-003 (Steelman Technique)
- **Steelman By:** adv-executor | **Date:** 2026-08-07

## Summary

**Steelman Assessment:** The issue accurately restates REM-07's core defect (substring denylist, specific bypassing commands, weaker duplicate of the deterministic enforcement engine) and reproduces the register's redesign question almost verbatim — strong factual fidelity on the parts it states precisely. Its main weakness is scope drift in the motivating paragraph, which reaches beyond REM-07 into territory owned by sibling issues.
**Improvement Count:** 1 Critical, 1 Major, 3 Minor
**Original Strength:** Good — accurate on its narrow claims, correctly severity-tagged, correct blocking status, resolvable worktracker/register references.
**Recommendation:** Incorporate improvements — targeted scope-precision fix plus three low-cost additions materially raise self-containedness and actionability.

## Improvement Findings Table

| ID | Severity | Description | Dimension |
|----|----------|--------------|-----------|
| S-003-01 | Critical | Scope drift: injection-screening gap generalized beyond this issue's actual redesign scope | Internal Consistency / Actionability |
| S-003-02 | Major | No path given for "the existing deterministic security enforcement engine" | Actionability |
| S-003-03 | Minor | Worktracker reference points to a directory, not the entity file | Traceability |
| S-003-04 | Minor | Omits that human review (not SEC-001/002) is the actual primary control | Evidence Quality |
| S-003-05 | Minor | Design question omits 3 of 5 register acceptance-criteria sub-items | Completeness |

## Improvement Details

### S-003-01 (Critical) — Scope drift in the motivating paragraph

**Original:** "the skill's prompt-injection screening likewise covers only one of the several attacker-influenceable inputs (workflow definitions, state files, lessons-learned entries, hold-point logs) that end up driving tool calls."

**Ground truth:** REM-07 (register) and the BUG-007 worktracker entity both scope SEC-001's gap entirely to fields *within* the workflow definition — Action, Target, Expected Result, Sign-off Criterion, Hold Reason, and Sections 2/3/9 prose. State-file poisoning is REM-03/BUG-003 (issue #352); the OE/"lessons-learned" corpus as an injection channel is REM-06/BUG-006 (issue #355). Neither is part of REM-07's redesign question, which correctly says only "*all definition-sourced fields* that drive tool calls" — a narrower claim that directly contradicts the sentence quoted above within the same ~300-word issue.

**Why this matters:** An external contributor or agent reading only this text has no way to know the four-item list mixes this issue's actual scope with two *other* issues' scope. Acting on the broader claim risks out-of-scope rework (or apparent duplication with #352/#355) with no cross-reference to disambiguate.

**Strengthened:** "the skill's prompt-injection screening (SEC-001) checks only the WARNING/CAUTION annotation text inside a workflow-definition step, while the Action, Target, Expected Result, Sign-off Criterion, Hold Reason, and free-text sections of the same definition are equally attacker-controlled and drive tool calls unchecked. (State-file and lessons-learned-corpus injection are tracked separately — issues #352 and #355.)"

---

### S-003-02 (Major) — Unlocated reference to the deterministic engine

**Original:** "the repository already has a deterministic security enforcement engine this duplicates, weaker, at the prompt level."

**Issue:** No path given. Verified: `src/infrastructure/internal/enforcement/security_enforcement_engine.py` (with `security_rules.py` and existing test coverage) is the actual engine, and it is one of the three named options in the issue's own design question ("delegation to the existing deterministic enforcement engine"). A contributor cannot evaluate that option without first finding the file.

**Strengthened:** "...duplicates, weaker, at the prompt level (`src/infrastructure/internal/enforcement/security_enforcement_engine.py`)."

---

## Minor Findings (brief)

- **S-003-03:** `Worktracker: projects/PROJ-032-nuclear-sop-review/work/BUG-007-executor-command-gating` resolves to a directory. Append `/BUG-007-executor-command-gating.md` so the reference resolves to the entity file directly.
- **S-003-04:** The register notes PLAYBOOK.md "overstates machine-side coverage by naming SEC-001/002 'the primary mitigations' when SR-06 human review is the actual primary control." The issue omits this framing entirely, letting a reader over-weight the machine-screening gap relative to human review. Add one clause: "(human review of the workflow definition remains the primary control here)."
- **S-003-05:** The design question captures 2 of REM-07's 5 acceptance-criteria items (gating model, screening scope). It omits: neutralize verbatim payload echo into logs, surface H-05 (uv-only Python) in executor constraints, and narrow/justify sop-brief's and sop-capture's Bash grants. The cited `remediation-register.md` link covers these, so this is Minor rather than Major, but one added clause would let an agent triage full scope without a second file open.

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Positive | S-003-05 closes a scope-visibility gap |
| Internal Consistency | 0.20 | Positive | S-003-01 removes a self-contradiction within the issue |
| Methodological Rigor | 0.20 | Neutral | Redesign-question structure already sound |
| Evidence Quality | 0.15 | Positive | S-003-04 restores correct control hierarchy |
| Actionability | 0.15 | Positive | S-003-02 removes a required lookup |
| Traceability | 0.10 | Positive | S-003-03 sharpens the worktracker pointer |

---
*Downstream: ready for S-002/S-004/S-001/S-007 critique per H-16.*
