# Chain-of-Verification Report: GitHub issue #359 (BUG-010 / REM-10)

**Strategy:** S-011 Chain-of-Verification
**Deliverable:** `snapshots/final/issue-359.md` (live text of geekatron/jerry issue #359)
**Criticality:** C4 (tournament)
**Date:** 2026-08-07
**Reviewer:** adv-executor (S-011)
**H-16 Compliance:** Not confirmed applied to this artifact by this executor; proceeding per indirect H-16 status of S-011.
**Claims Extracted:** 9 | **Verified:** 7 | **Discrepancies:** 2 (both Major)

## Summary

7 of 9 testable claims (commit hash/branch, seven-fix count, both schema error counts, section-numbering defect, hexagonal-wording defect, reasoning-effort defect, CI link/status) verify exactly against `remediation-register.md` REM-10, `remediation-log.md`, and the `c07033ce` diff. Two claims overstate uniformity across the fix: "output locations declared for all four agents" and the "8 of 8 files valid" figure juxtaposed with a verification command that only checks 4. Both are Major — they could send a verifying reader/agent looking for evidence the text doesn't actually support. Recommendation: **REVISE** (2 corrections, no Critical issues).

## Findings Table

| ID | Claim | Source | Discrepancy | Severity | Affected Dimension |
|----|-------|--------|-------------|----------|--------------------|
| S-011-01 | "project-anchored output locations declared for all four agents" | remediation-register.md REM-10 fix spec item 5; evidence-c07033ce.md sop-verifier.governance.yaml diff | sop-verifier's diff sets `output.required: false` and removes its `location:` field entirely (T1, read-only, returns report as Task response) — it gets *no* declared location, project-anchored or otherwise. Only 3 of 4 agents (sop-brief, sop-executor, sop-capture) received `projects/${JERRY_PROJECT}/...` locations. | Major | Evidence Quality |
| S-011-02 | "(independent re-check after the fix: 8 of 8 files valid)" placed immediately after "all four governance files pass the schema", with the only verify command given re-checking governance files against one schema | remediation-log.md Verification Chain ("schema gate 8/8"); register REM-10 validate step (4 governance.yaml vs `agent-governance-v1.schema.json`; 4 composition `agent.yaml` vs YAML parse + canonical schema — two different checks) | The "8" spans two different validations (4 governance + 4 composition) against two different schemas, but the issue text presents it as corroborating "all four governance files pass the schema." Following the issue's own "How to verify" command (re-validate governance files) reproduces only 4/4, not 8/8 — a reader cannot reconcile the numbers from the instructions given. | Major | Actionability |

## Finding Details

### S-011-01: Overclaims uniform output-location fix across all four agents [MAJOR]

**Claim (from deliverable):** "project-anchored output locations declared for all four agents"
**Source Document:** `remediation-register.md` REM-10 fix specification item 5; confirmed in `evidence-c07033ce.md` diff of `agents/sop-verifier.governance.yaml` (`output: required: false`, no `location:` key; composition twin same) and `agents/sop-brief.governance.yaml` / executor / capture (`location: "projects/${JERRY_PROJECT}/nuclear-sop/{workflow_id}/..."`).
**Independent Verification:** Register: "sop-verifier: no file output (required:false), so declare none." The diff confirms `location` was deleted (not project-anchored, not any-anchored) for sop-verifier; a `note:` field references a *conventional* path (`{workflow_definition_directory}/iv-report-...`) that is not `projects/${JERRY_PROJECT}/`-rooted and is not a schema `output.location`.
**Discrepancy:** The deliverable states all four agents got a project-anchored output location; the source shows three did and the fourth (sop-verifier) correctly and intentionally got none.
**Severity:** Major — an external contributor or agent checking sop-verifier's governance file for the promised project-anchored location will not find one and may conclude the fix is incomplete or the issue text is unreliable.
**Dimension:** Evidence Quality
**Correction:** Replace with: "project-anchored output locations declared for sop-brief, sop-executor, and sop-capture; sop-verifier (T1, read-only) explicitly declares no file output — it returns its report via the Task response, per design."

### S-011-02: "8 of 8 files valid" not reproducible from the given verify command [MAJOR]

**Claim (from deliverable):** "...all four governance files pass the schema (independent re-check after the fix: 8 of 8 files valid)." followed later by "...re-validate the governance files against `docs/schemas/agent-governance-v1.schema.json` (same branch) — zero errors."
**Source Document:** `remediation-log.md` Verification Chain step 3 ("schema gate 8/8"); register REM-10 validate step: governance schema check applies to 4 files, a *separate* YAML-parse + canonical-schema check applies to the 4 `composition/*.agent.yaml` twins.
**Independent Verification:** The "8" is real but is the sum of two distinct checks over two distinct file sets/schemas, not a single re-run of the one command the issue tells the reader to use.
**Discrepancy:** A reader following the issue's own verification instruction gets 4/4, not 8/8, with no indication a second check (composition YAML parse/canonical schema) is needed to reach "8".
**Severity:** Major — undermines the "How to verify" section's self-sufficiency; the reader cannot reproduce the headline number from the given command.
**Dimension:** Actionability
**Correction:** Either drop the "(8 of 8 files valid)" parenthetical, or expand "How to verify" to two commands: one for the 4 `agents/*.governance.yaml` against `agent-governance-v1.schema.json`, one for the 4 `composition/*.agent.yaml` (YAML parse + canonical schema), so the "8/8" figure is reproducible.

## Recommendations

**Major (SHOULD correct):**
- S-011-01: reword the "all four agents" output-location sentence to name the 3 file-writing agents and state sop-verifier's no-location design explicitly.
- S-011-02: either remove "8 of 8" or add the second verification command so the figure is reproducible from the issue text alone.

**Minor (MAY correct):**
- S-011-03: "the reasoning-effort declaration its review tier calls for" — the governance field is `quality_gate_tier` (per ET-M-001), not "review tier." Using the actual field name would let an agent `grep` the YAML successfully; "review tier" returns no hits.

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Neutral | All 7 mechanical-fix items and CI evidence are present and traceable. |
| Internal Consistency | 0.20 | Negative | S-011-02: headline number ("8 of 8") not consistent with the single verify command supplied. |
| Methodological Rigor | 0.20 | Neutral | Claims map cleanly to register/log/diff sources for 7 of 9 checks. |
| Evidence Quality | 0.15 | Negative | S-011-01: "all four agents" overstates diff evidence for sop-verifier. |
| Actionability | 0.15 | Negative | S-011-02: verify instructions don't reproduce the cited figure. |
| Traceability | 0.10 | Positive | Commit hash, CI run link, and worktracker path all verified exact matches to source. |
