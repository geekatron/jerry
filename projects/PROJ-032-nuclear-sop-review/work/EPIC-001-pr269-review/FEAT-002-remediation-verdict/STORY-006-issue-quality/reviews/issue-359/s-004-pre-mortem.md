# Pre-Mortem Report: GitHub Issue #359 (BUG-010 / REM-10)

**Strategy:** S-004 Pre-Mortem Analysis
**Deliverable:** `snapshots/final/issue-359.md` (live text of geekatron/jerry issue #359)
**Criticality:** C4 (tournament)
**H-16 Note:** Executed as a blind strategy lane per orchestration design; S-003 Steelman output not available to this agent. Findings below are stated as direct observations, not H-16-chained critique.
**Failure Scenario:** PR #269's external contributor (or their AI agent) reads issue #359, tries to independently confirm the "fix changed" claims by inspecting the four agent definition files, finds `sop-verifier.governance.yaml` has *no* output-location field at all, concludes the maintainer's fix report is wrong or incomplete, and either re-opens a dispute or distrusts every other claim in the remediation register — even though the actual fix is correct and the register text (not the code) is the only thing that erred.

## Summary

One Critical and two Minor/Major failure causes identified via prospective hindsight against ground truth (`evidence-c07033ce.md` diff, `remediation-register.md` REM-10, `remediation-log.md`). The Critical finding is a genuine factual inaccuracy in the issue text (not the code): it claims a uniform outcome across four agents when one agent's outcome is materially different by design. Recommendation: **REVISE** — one line must change before this issue can be trusted as a standalone record of what happened.

## Findings Table

| ID | Failure Cause | Category | Likelihood | Severity | Priority |
|----|---------------|----------|------------|----------|----------|
| S-004-01 | "project-anchored output locations declared for all four agents" is false for sop-verifier | Evidence Quality | High | Critical | P0 |
| S-004-02 | "How to verify" only re-validates governance files; doesn't cover composition-file schema or the unparseable-YAML claim | Actionability | Medium | Major | P1 |
| S-004-03 | "8 of 8 files valid" appears right after a sentence that names only 4 files, with no explanation of the other 4 | Completeness | Medium | Minor | P2 |

## Finding Details

### S-004-01: False claim of uniform output-location fix across all four agents [CRITICAL]

**Failure Cause:** Line 9 states: *"project-anchored output locations declared for all four agents."* Ground truth (`evidence-c07033ce.md` diff of `sop-verifier.governance.yaml`) shows the opposite for `sop-verifier`: its output block changes from `required: true` / `location: "{workflow_definition_directory}/iv-report-{step_id}-{YYYYMMDD}.md"` to `required: false` with **no location field at all**, because sop-verifier is T1 (read-only) and cannot write files — its report is returned as Task response content. Only sop-brief, sop-executor, and sop-capture received a `projects/${JERRY_PROJECT}/...`-anchored location.
**Category:** Evidence Quality (claim contradicted by the cited fix commit itself).
**Likelihood:** High — this is exactly the kind of claim an external contributor's AI agent would mechanically re-verify by reading the four governance files (the issue explicitly invites that: "run `git diff ...`").
**Severity:** Critical — sends the verifying agent down a wrong path: it will find a *missing* field where the text promises a *declared* one, and may reasonably conclude the maintainer's fix (or fix report) is unreliable, undermining trust in the six other accurate claims in the same paragraph.
**Evidence:** `evidence-c07033ce.md` lines ~826-830 (`sop-verifier.governance.yaml` diff); `remediation-register.md` REM-10 fix spec item 5 ("sop-verifier: no file output (required:false), so declare none").
**Mitigation:** Replace with: *"project-anchored output locations declared for sop-brief, sop-executor, and sop-capture; sop-verifier (T1, read-only) now correctly declares `required: false` since it returns its report as Task response content rather than writing a file."*
**Acceptance Criteria:** Edited issue text no longer asserts a location was declared for sop-verifier; text explicitly names the read-only exception.

### S-004-02: Verification instructions don't cover the claim's full scope [MAJOR]

**Failure Cause:** "How to verify" offers two paths: (a) `git diff c07033ce^ c07033ce -- .../agents/ .../composition/`, or (b) "re-validate the governance files against `docs/schemas/agent-governance-v1.schema.json` — zero errors." Path (b) only covers 4 of the 8 files counted in "8 of 8 files valid" — the 4 `composition/*.agent.yaml` files validate against a *different* schema (`agent-canonical-v1.schema.json`, per each file's own header comment) and aren't mentioned at all. The single most vivid defect in the issue — `composition/sop-verifier.agent.yaml` being unparseable YAML — is also not confirmable via path (b); a reader following only that instruction cannot verify the primary claim being tracked.
**Category:** Actionability / Methodological Rigor.
**Likelihood:** Medium — depends on whether the reader tries path (a) (diff, which does show the fix) or stops at path (b).
**Severity:** Major — doesn't send the reader to a wrong conclusion, but forces an extra lookup (which schema applies to which file) to fully substantiate the "8 of 8" figure.
**Evidence:** `evidence-c07033ce.md` composition file header: `# Schema: docs/schemas/agent-canonical-v1.schema.json`; REM-10 fix spec validate step distinguishes governance-schema and `yaml.safe_load` checks for composition files.
**Mitigation:** Extend the verify line: *"...or re-validate the four `agents/*.governance.yaml` files against `docs/schemas/agent-governance-v1.schema.json`, and confirm the four `composition/*.agent.yaml` files parse cleanly and validate against `docs/schemas/agent-canonical-v1.schema.json` — zero errors across all 8."*
**Acceptance Criteria:** Verify section names both schemas and both file sets that make up the "8."

### S-004-03: Unexplained jump from "four" to "8 of 8" [MINOR]

**Failure Cause:** The sentence names "all four governance files," then parenthetically cites "8 of 8 files valid" with no mention that the other four are the `composition/*.agent.yaml` twins. Minor because the register/log are one click away and the number itself is correct.
**Mitigation:** "...all four governance files pass the schema, and their four `composition/*.agent.yaml` twins now parse and validate too (independent re-check: 8/8 files valid)."

## Recommendations

- **P0:** S-004-01 — correct the sop-verifier claim before this issue is cited as evidence in any merge decision.
- **P1:** S-004-02 — extend verify instructions to name both schemas/file sets.
- **P2:** S-004-03 — one clause to explain the "8" (low cost, bundle with P0/P1 edit pass).

## Scoring Impact

| Dimension | Impact | Rationale |
|-----------|--------|-----------|
| Evidence Quality | Negative | S-004-01: central claim contradicted by the cited commit |
| Actionability | Negative | S-004-02: verify path doesn't substantiate the full claim |
| Completeness | Negative (minor) | S-004-03: unexplained figure |
| Internal Consistency | Neutral | Rest of the "what changed" paragraph is internally consistent and matches ground truth |
| Traceability | Positive | Tracking block correctly cites worktracker path, register section, and branch |

## Execution Statistics
- **Total Findings:** 3
- **Critical:** 1 | **Major:** 1 | **Minor:** 1
- **Protocol Steps Completed:** 6 of 6
