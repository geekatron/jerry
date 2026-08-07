# Chain-of-Verification Report: GitHub Issue #354 (BUG-005 / REM-05)

**Strategy:** S-011 Chain-of-Verification
**Deliverable:** `snapshots/final/issue-354.md` (~300-word GitHub issue text)
**Criticality:** C4 (tournament)
**Date:** 2026-08-07
**H-16 Compliance:** Not confirmed applied prior to this execution (indirect for CoVe per template; proceeding per protocol)
**Claims Extracted:** 8 | **Verified:** 7 | **Discrepancies:** 0 material; 2 context gaps flagged as Major/Minor

## Summary

Every testable factual claim in issue #354 — the 2026-06-15 deadline, the lapsed-with-no-ruling status, the two contradictory fallback instructions with different anchor dates, the nonexistent tracking work-item, the eng-team precedent (8-step/10-agent, no hop-ceiling machinery), the worktracker path, and the register file location/branch — was independently verified against the rules file, SKILL.md, the remediation register, the verdict document, and the eng-team skill itself. **All verified TRUE with exact-quote-level precision.** No factual corrections are required. Findings below are actionability/self-containedness gaps, not factual errors. **Recommendation: ACCEPT** (no Critical/Major factual discrepancy found); two Minor-to-Major polish items would reduce lookup burden for the external reader.

## Findings Table

| ID | Claim | Source | Discrepancy | Severity | Affected Dimension |
|----|-------|--------|-------------|----------|---------------------|
| S-011-01 | "the file's two fallback instructions contradict each other ... use different anchor dates" | `skills/nuclear-sop/rules/nuclear-sop-behavior-rules.md` (NS-H-08 line 37; Governance Deadline section ~line 286) | None — VERIFIED. NS-H-08: "remains as written," anchor "skill registration (2026-06-15)." Governance Deadline section (same file): "3-hop mode becomes permanent ... sop-verifier is eliminated," anchor "Phase 1 delivery." Both are in the same file as claimed. | N/A (verified) | — |
| S-011-02 | "cite a tracking work-item that does not exist anywhere" | NS-H-08 cites `TASK-0039-H36-RULING`; register REM-05 G1 confirms "no TASK-0039-H36-RULING worktracker entity ... repo-wide grep matches only the rules file itself" | None — VERIFIED | N/A (verified) | — |
| S-011-03 | eng-team precedent: "predetermined 8-step sequence across 10 worker agents with no hop-ceiling machinery" | `skills/eng-team/SKILL.md` (10-agent roster; "8-step sequential phase-gate workflow"; no H-36/hop text found) | None — VERIFIED | N/A (verified) | — |
| S-011-04 | Worktracker path `projects/PROJ-032-nuclear-sop-review/work/BUG-005-h36-governance-ruling` | Confirmed on-disk: `.../work/BUG-005-h36-governance-ruling/BUG-005-h36-governance-ruling.md` | None — VERIFIED to exist, but the issue text does not repeat the branch qualifier for this path, only for the register citation that follows it (see S-011-05) | Minor | Traceability |
| S-011-05 | Two contradictory fallback instructions, no file paths given in the issue body | Register REM-05 "Affected files": `nuclear-sop-behavior-rules.md`, `SKILL.md`, `PLAYBOOK.md` | Omission, not error: the issue never names the two locations of the contradiction, forcing the reader to open the linked register to find where to fix it | Major | Actionability |
| S-011-06 | "Whatever the ruling: encode it once ... and track it as a real work item" | Verdict conditions-for-merge #2: same, plus "with H-32 GitHub-issue parity" | Minor omission — GitHub-issue parity requirement dropped in the compressed issue text | Minor | Completeness |

## Finding Details

### S-011-04: Worktracker path lacks explicit branch qualifier [MINOR]

**Claim (from deliverable):** "Worktracker: `projects/PROJ-032-nuclear-sop-review/work/BUG-005-h36-governance-ruling` (register section REM-05). Full analysis with candidate designs: `remediation-register.md` in `.../STORY-004-remediation/` on branch `feat/proj-032-nuclear-sop-review`."
**Independent Verification:** The worktracker path resolves correctly, and it lives on the same `feat/proj-032-nuclear-sop-review` branch — but the branch qualifier is grammatically attached only to the second (register) citation.
**Discrepancy:** An external reader working on the PR's own branch (`proj-0039-nuclear-engineer`) could reasonably infer the worktracker path is resolvable on their branch or on `main`, when in fact both paths require checking out `feat/proj-032-nuclear-sop-review`.
**Severity:** Minor — a reader who tries the path on the wrong branch gets a 404, not a wrong-path error; self-correctable.
**Dimension:** Traceability
**Correction:** "Worktracker and full analysis (`remediation-register.md`, section REM-05) both live on branch `feat/proj-032-nuclear-sop-review`: `projects/PROJ-032-nuclear-sop-review/work/BUG-005-h36-governance-ruling` and `.../STORY-004-remediation/remediation-register.md`."

### S-011-05: No file paths given for the two contradictory instructions [MAJOR]

**Claim (from deliverable):** "the file's two fallback instructions contradict each other (one says keep the current mode, the other says revert)."
**Independent Verification:** The two instructions are NS-H-08 (line 37 of `skills/nuclear-sop/rules/nuclear-sop-behavior-rules.md`) and the "Governance Deadline" subsection of the same file's "3-Hop vs. 4-Hop Mode Selection" section (~line 286); the "revert" position is also echoed verbatim in `SKILL.md`'s "H-36 Circuit Breaker Compliance" section.
**Discrepancy:** The issue is factually correct that "the file" contains both instructions, but names neither the file nor the two rule/section IDs. An agent trying to act on this issue directly (without first reading the linked register) cannot locate what to edit.
**Severity:** Major — forces a lookup in `remediation-register.md` before any edit can be attempted, working against the "act from this text alone" goal.
**Dimension:** Actionability
**Correction:** Append: "(`nuclear-sop-behavior-rules.md`: rule NS-H-08 says keep 4-hop; its own Governance Deadline section says revert to 3-hop; SKILL.md repeats the revert position)."

## Recommendations

**Critical:** None.
**Major:** S-011-05 — name the file(s) and the two conflicting rule/section identifiers so the issue is actionable without opening the register first.
**Minor:** S-011-04 — attach the branch qualifier to the worktracker path, not only the register citation. S-011-06 — optionally restore the "with a GitHub issue" clause to fully match the verdict's merge condition, if word budget allows.

## Scoring Impact

| Dimension | Weight | Impact | Rationale |
|-----------|--------|--------|-----------|
| Completeness | 0.20 | Neutral | All core facts (deadline, contradiction, missing tracking item, precedent) present; S-011-06 is a minor compression, not a gap in substance |
| Internal Consistency | 0.20 | Positive | No claim in the issue conflicts with another claim in the issue or with source documents |
| Methodological Rigor | 0.20 | Positive | Every extracted claim traced to an exact source line/section; no unverifiable assertions found |
| Evidence Quality | 0.15 | Positive | 2026-06-15, the two anchor phrases, and the eng-team 8-step/10-agent figures all match source text verbatim |
| Actionability | 0.15 | Negative | S-011-05: missing file/rule pointers force a lookup before a fix can be attempted |
| Traceability | 0.10 | Negative | S-011-04: branch qualifier ambiguity on one of two cited paths |

---
*Execution ID: s-011-cove-issue354-20260807*
