# Steelman Report: GitHub Issue #352 (BUG-003 — trust-boundary / state-tamper)

## Steelman Context
- **Deliverable:** `snapshots/final/issue-352.md` (live text of GitHub issue #352, geekatron/jerry)
- **Deliverable Type:** GitHub Issue (external communication/specification artifact)
- **Criticality Level:** C4
- **Strategy:** S-003 (Steelman Technique)
- **Steelman By:** adv-executor | **Date:** 2026-08-07

## Summary
**Steelman Assessment:** The issue text is already strong — both substantive claims (verifier authority inversion; fabricated SHA-256 tamper detection) check out exactly against `remediation-register.md` REM-03, the worktracker path resolves on disk, and no internal codenames (H-rule IDs, strategy IDs, hold-point jargon) leak into reader-facing prose. Improvements found are almost entirely presentation/actionability, not correctness.
**Improvement Count:** 0 Critical, 3 Major, 3 Minor
**Original Strength:** High. Core thesis preserved unchanged by this Steelman.
**Recommendation:** Incorporate the 3 Major findings (all reduce "forces a lookup") before downstream critique strategies run.

## Improvement Findings Table

| ID | Description | Severity | Dimension |
|----|-------------|----------|-----------|
| SM-001 | SHA-256 claim has no file citation | Major | Evidence Quality |
| SM-002 | Tracking paths are bare repo-relative + branch name, not clickable | Major | Actionability |
| SM-003 | "Design question" run-on sentence bundles 3 sub-questions | Major | Actionability |
| SM-004 | "execution-state file" never named (`PROCEDURE_STATE.yaml`) | Minor | Evidence Quality |
| SM-005 | Assignees line: two names space-joined, no separator | Minor | Presentation |
| SM-006 | "Blocks merge" reads as if this defect alone gates merge | Minor | Consistency |

## Improvement Details

### SM-001 (Major) — SHA-256 claim lacks a locatable source
**Original:** "the documentation claims the execution-state file carries SHA-256 tamper detection; no such mechanism is implemented anywhere"
**Strengthened:** "`skills/nuclear-sop/templates/PROCEDURE_STATE.template.yaml` and `skills/nuclear-sop/docs/reference.md` both claim a SHA-256 `state_hash` — 'computed after every state write, verified in STAR-STOP before every tool call.' No file under `skills/nuclear-sop/agents/` or `composition/` contains any instruction to compute or verify it."
**Rationale:** Verified against register REM-03 G3. Without a file name, the contributor/agent must re-derive which of ~15 skill files to open; naming the two source files removes that lookup entirely.

### SM-002 (Major) — References are not resolvable without manual reconstruction
**Original:** "`projects/PROJ-032-nuclear-sop-review/work/BUG-003-trust-boundary-state-tamper` (register section REM-03) ... `remediation-register.md` in `.../STORY-004-remediation/` on branch `feat/proj-032-nuclear-sop-review`"
**Strengthened:** Replace bare paths with full GitHub blob URLs once the branch is pushed, e.g. `https://github.com/geekatron/jerry/blob/feat/proj-032-nuclear-sop-review/projects/PROJ-032-nuclear-sop-review/work/BUG-003-trust-boundary-state-tamper/BUG-003-trust-boundary-state-tamper.md` and a `#rem-03-...` anchor into the register.
**Rationale:** Both paths were confirmed to resolve on disk (verified via filesystem check), so the content is accurate — but a GitHub issue reader cannot click a bare `path/on/branch` string. This is the one place the mission's "resolvable references" criterion is only partially met: content exists, but the reference format still requires the reader to manually build a URL and know which branch to check out.

### SM-003 (Major) — Compound design question is hard to action as a checklist
**Original:** "where do the verifier's criteria, expected paths, and the effective risk level come from, if not from the artifact they police — and is the tamper-evidence control going to be implemented for real, or withdrawn from every place the docs claim it?"
**Strengthened:** Split into an enumerated list mirroring the register's own structure: "(1) Where do sop-verifier's acceptance criteria and expected output paths come from, if not the workflow definition? (2) How is the declared risk/criticality level cross-checked against independent signals? (3) Is state-tamper evidence for the execution-state file going to be implemented for real, or withdrawn everywhere it's currently claimed?"
**Rationale:** The single-sentence form conflates 3 independently answerable design questions; a contributor or their agent has to manually decompose it before scoping work. Register REM-03 already carries this exact (a)/(b)/(c) structure — the issue collapsed it for brevity but lost checklist-actionability in the process.

### Minor findings (SM-004..006)
- **SM-004:** Name the file explicitly on first use: "the execution-state file (`PROCEDURE_STATE.yaml`)" — removes ambiguity between the template and the runtime artifact.
- **SM-005:** "Assignees: victorlau1 malcolm-x-evo " → "Assignees: @victorlau1, @malcolm-x-evo" — current rendering could be misread as one garbled username.
- **SM-006:** "Blocks merge of PR #269" → "One of seven open design blockers gating merge of PR #269" — prevents a reader who sees only this issue from concluding fixing BUG-003 alone unblocks the PR (verdict: all seven of #350–#356 must close).

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Neutral | Core defect and question already fully present; SM-001/004 add source specificity only |
| Internal Consistency | 0.20 | Positive | SM-006 removes a scope-of-blocking ambiguity |
| Methodological Rigor | 0.20 | Positive | SM-003 restores the register's decomposed question structure |
| Evidence Quality | 0.15 | Positive | SM-001/004 add resolvable file citations |
| Actionability | 0.15 | Positive | SM-002/003 remove two "forces a lookup" gaps |
| Traceability | 0.10 | Positive | SM-002 makes references click-resolvable |

---
*Blind to other strategies/issues per instructions. No subagents invoked (P-003). Ground truth: remediation-register.md REM-03, pr269-verdict.md, filesystem existence check.*
