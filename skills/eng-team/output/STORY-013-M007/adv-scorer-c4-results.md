# Quality Score Report: M-007 disallowedTools Task->Agent Rename (UX Agent Definitions)

## L0 Executive Summary

**Score:** 0.865/1.00 | **Verdict:** REVISE | **Weakest Dimension:** Internal Consistency (0.82)

**One-line assessment:** The declared 5-layer deliverable scope is well-executed with rigorous dual-security review and all HIGH findings remediated, but 9 sub-skill SKILL.md files and 3 mcp-runbook.md files retain stale `Task tool` and `disallowedTools: [Task]` references (eng-security F-004, acknowledged open), creating repository-level documentation inconsistency that prevents the deliverable from reaching the C4 threshold of 0.95.

---

## Scoring Context

- **Deliverable:** M-007 disallowedTools Task->Agent rename across UX agent definitions (26 files across 5 layers)
- **Deliverable Type:** Code Modification (agent definition files, CI rules, governance YAML)
- **Criticality Level:** C4 (Critical)
- **Quality Threshold:** 0.95 (C4, user-specified — higher than standard 0.92 for governance changes)
- **Scoring Strategy:** S-014 (LLM-as-Judge)
- **SSOT Reference:** `.context/rules/quality-enforcement.md`
- **Strategy Findings Incorporated:** Yes — 2 reports (eng-security: 5 findings, red-vuln: 6 findings)
- **Scored:** 2026-03-29T00:00:00Z

---

## Score Summary

| Metric | Value |
|--------|-------|
| **Weighted Composite** | 0.865 |
| **Threshold** | 0.95 (C4, user-specified) |
| **Verdict** | REVISE |
| **Strategy Findings Incorporated** | Yes — 11 total (5 eng-security + 6 red-vuln) |

---

## Dimension Scores

| Dimension | Weight | Score | Weighted | Evidence Summary |
|-----------|--------|-------|----------|-----------------|
| Completeness | 0.20 | 0.85 | 0.170 | Declared 5-layer scope fully complete; F-004 (sub-skill SKILL.md + mcp-runbook stale refs, ~12 files) acknowledged open |
| Internal Consistency | 0.20 | 0.82 | 0.164 | Declared deliverable files are mutually consistent; sub-skill SKILL.md files contradict actual frontmatter values |
| Methodological Rigor | 0.20 | 0.88 | 0.176 | Layer-priority ordering (runtime first), dual security review (eng-security ASVS + red-vuln PTES/OWASP A04), H-16 ordering satisfied |
| Evidence Quality | 0.15 | 0.90 | 0.135 | Per-finding CWE/CVSS/ASVS evidence, file/line citations, schema source confirmation, blast radius quantification |
| Actionability | 0.15 | 0.88 | 0.132 | Remediated items have exact grep patterns and line numbers; open items have explicit effort estimates and future-work classification |
| Traceability | 0.10 | 0.88 | 0.088 | CI gates reference H-34(b)/H-01 inline; security findings reference CWE+ASVS; open findings documented in two persistent reports |
| **TOTAL** | **1.00** | | **0.865** | |

---

## Detailed Dimension Analysis

### Completeness (0.85/1.00)

**Evidence:**

Layer 1 (10 worker frontmatter): All 10 files confirmed `disallowedTools: - Agent` per eng-security Appendix A verification table. Passes UX-CI-002 criteria.

Layer 2 (orchestrator frontmatter): `skills/user-experience/agents/ux-orchestrator.md` line 18 confirmed `- Agent` in `tools:` list. Grep for `Task` in this file returns zero matches.

Layer 3 (2 governance YAMLs): `ux-orchestrator.governance.yaml` line 37 now reads `- Agent` (eng-security F-002 remediated). Line 7 comment updated to `# T5 justification: Agent tool required`. Line 85 now reads `Only orchestrator has Agent`. `ux-jtbd-analyst.governance.yaml` confirmed `Agent` in forbidden_actions (line 33: "NEVER spawn recursive subagents or use the Agent tool") and constitution (line 58: "Worker agent; no Agent tool access").

Layer 4 (body text, 9 worker .md files): `ux-ai-design-guide.md` line 114 confirmed `- Agent tool -- this is a worker agent (P-003)`. The other 8 workers in scope verified via eng-security finding F-003 (which identified 7 originally stale; 3 were not affected). The body-text update is confirmed present in the accessible worker agent files.

Layer 5 (3 docs): `ci-checks.md` UX-CI-002 section (lines 68-95) now greps for `Agent` not `Task`. CI Gate Summary table row for UX-CI-002 (line 718) correctly states `All sub-skills declare disallowedTools: [Agent]`. `SKILL.md` (skills/user-experience/SKILL.md) lines 186 and 498 confirmed `disallowedTools: [Agent]`. `ux-routing-rules.md` has zero `Task` matches (only `Task success` in HEART metric domain context, which is correct).

**Gaps:**

F-004 (eng-security MEDIUM, acknowledged open): Sub-skill SKILL.md files retain stale references. Verified: `ux-ai-first-design/SKILL.md` line 607 still states `` `disallowedTools: [Task]` present in agent frontmatter ``; line 144 says "invoked by the ux-orchestrator via the Task tool"; line 193 says "invokes the agent via the Task tool". Same pattern confirmed in `ux-behavior-design/SKILL.md` (lines 134, 177, 594, 655) and `ux-lean-ux/SKILL.md` (lines 132, 145, 177, 556, 565). `ux-lean-ux/rules/mcp-runbook.md` line 207 states `disallowedTools: [Task]`. The eng-security report identified approximately 40+ occurrences across 15+ files. These are outside the declared 3-file Layer 5 scope but create repository-level documentation inconsistency.

The 3-file Layer 5 scope definition was narrow by choice — the task description confirms this scope. However, the documentation inconsistency gap is real and material for a C4 deliverable where governance documentation must match implementation.

**Improvement Path:**

Extend Layer 5 scope to cover all sub-skill SKILL.md files and mcp-runbook.md files (estimated 40+ occurrences, scriptable via grep-and-replace). This would likely raise Completeness to 0.93-0.95 and also improve Internal Consistency.

---

### Internal Consistency (0.82/1.00)

**Evidence:**

Within the declared deliverable files, consistency is high:
- `ux-orchestrator.md` `tools: [Agent]` is consistent with `ux-orchestrator.governance.yaml` `allowed_tools: [Agent]`
- `ux-orchestrator.governance.yaml` constitution (line 85: "Only orchestrator has Agent") is consistent with `.md` body (line 120: "Sub-skill agents do NOT have the Agent tool")
- All 10 worker `.md` frontmatter `disallowedTools: [Agent]` is consistent with CI gate UX-CI-002 checking for `Agent`
- SKILL.md line 186 stating `disallowedTools: [Agent]` is consistent with actual frontmatter values
- ux-routing-rules.md Agent invocation section uses `Agent(` syntax consistently

**Gaps:**

Repository-level inconsistency: `ux-ai-first-design/SKILL.md` line 607 asserts `` `disallowedTools: [Task]` present in agent frontmatter `` while the actual frontmatter (`ux-ai-design-guide.md`) contains `disallowedTools: - Agent`. This is a direct factual contradiction within the same repository. An auditor reading `ux-ai-first-design/SKILL.md` would conclude the agent uses `[Task]`; reading the agent definition they would find `[Agent]`. Same contradiction exists in `ux-lean-ux/SKILL.md` (line 145: `` `disallowedTools: [Task]` declared in ux-lean-ux-facilitator.md frontmatter ``).

The inconsistency exists between in-scope files and out-of-scope files, but both categories are in the same repository. At C4 criticality, governance documentation inconsistency of this kind (sub-skill SKILL.md claiming the wrong value for the security-critical `disallowedTools` field) represents a meaningful consistency gap.

**Improvement Path:**

Same as Completeness: extend Layer 5 sweep to sub-skill SKILL.md and mcp-runbook files. Alternatively, if the narrow Layer 5 scope is intentional for this story, file a dedicated worktracker item for F-004 remediation.

---

### Methodological Rigor (0.88/1.00)

**Evidence:**

Priority-ordered layer execution: Runtime enforcement (Layers 1-2) addressed before documentation layers (3-5). This is the correct priority ordering for security-critical changes — it ensures the actual enforcement mechanism is correct before documentation is updated.

Dual independent security review: eng-security applied ASVS V1.1.2, V1.1.6, V1.5.1 and CWE-693, CWE-1286, CWE-1059 analysis with CVSS 3.1 scores. red-vuln applied PTES Vulnerability Analysis, OWASP A04 (Insecure Design), and attack path analysis with blast radius assessment. Both reviewers reached consistent conclusions about the alias enforcement status and HIGH findings.

H-16 compliance: adv-selector plan confirms Steelman (S-003) at position 2 before Devil's Advocate (S-002) at position 3.

HIGH findings remediated: eng-security F-001 (CI gate broken), F-002 (governance.yaml stale) — both confirmed remediated per current file state. CI gate UX-CI-002 now greps for `Agent`; governance.yaml now has `Agent` throughout.

Five-layer decomposition: The task specification correctly identified all propagation targets (frontmatter, governance, body text, CI rules, documentation). The partial-rename syndrome diagnosis in eng-security L2 precisely identifies why this pattern of failure occurs.

**Gaps:**

F-006 (red-vuln Medium, open): `validate-agent-frontmatter.py` lacks a check for deprecated `Task` in `disallowedTools` and for `Agent` presence in non-T5 `tools:` lists. This means the CI detection layer (L5 global, not UX-specific) remains incomplete. The UX-specific CI (UX-CI-002) is repaired, but the global L5 validator cannot catch regressions across other skills.

F-003 (red-vuln Medium, documented future work): 79 non-UX worker agents rely solely on allowlist-based enforcement rather than explicit `disallowedTools: [Agent]`. Defense-in-depth improvement documented but not implemented.

**Improvement Path:**

Implement F-006 CI check in `validate-agent-frontmatter.py` (1 developer-hour per red-vuln estimate). Address F-004 documentation sweep. These would raise Methodological Rigor to approximately 0.92-0.93.

---

### Evidence Quality (0.90/1.00)

**Evidence:**

eng-security provides per-finding CWE mapping (CWE-693, CWE-1286, CWE-1059), CVSS 3.1 base scores with vector notation, ASVS chapter verification summary, and a per-file verification table (Appendix A) with Pass/Fail status for all 11 agent files and all governance YAML files.

red-vuln provides a 6-finding inventory with CVSS v3.1 estimates, exploitability/impact assessments, attack path analysis (AP-001 through AP-003), blast radius quantification, and an evidence collection table citing git commit hashes and schema file locations.

The backward-compatibility confirmation ("The subagent spawning tool was renamed from 'Task' to 'Agent' in v2.1.63. Both names work as aliases." from `docs/schemas/claude-code-frontmatter-v1.schema.json`) is a strong factual anchor cited by both reviewers.

**Gaps:**

The F-003 assessment (79 non-UX workers rely on allowlist) has limited verification evidence — the count of 79 is stated but not independently verified by line-level enumeration. The statement "A similar audit of all 79 non-UX workers has not been performed in this engagement" (red-vuln F-003) is honest but means this gap is partially unverified.

**Improvement Path:**

Enumerate all non-UX worker agents lacking `disallowedTools` and provide a file list in the F-003 evidence section. This is a low-effort verification step that would move Evidence Quality to 0.92-0.93.

---

### Actionability (0.88/1.00)

**Evidence:**

Remediated items have exact code-level instructions with line numbers:
- eng-security F-001 remediation: exact `grep -qE 'Agent|Task'` pattern provided (ci-checks.md lines 89-91)
- eng-security F-002 remediation: exact line numbers in governance.yaml (lines 37, 7, 85) with before/after values
- eng-security F-003 remediation: exact text substitution (`Task tool` -> `Agent tool`) with file/line table for all 7 affected files

Open items have classified effort estimates:
- F-006 (red-vuln): "1 developer-hour in validate-agent-frontmatter.py" with exact Python code snippet
- F-004 (eng-security): "systematic grep-based replacement, estimated 40+ occurrences across 15+ files"
- F-003 (red-vuln): "medium — 79 file edits, but mechanical. Could be scripted."

Short/medium/long-term architecture recommendations (eng-security L2) provide a roadmap beyond this story.

**Gaps:**

The open findings (F-003, F-004, F-006) are documented in security reports but not yet linked to worktracker entities. A C4 deliverable with documented-open medium findings should have corresponding worktracker items with priority, owner, and target date. The security reports recommend actions but do not establish ownership or timeline.

**Improvement Path:**

Create worktracker stories for F-004 (documentation sweep), F-006 (global CI check), and optionally F-003 (defense-in-depth). This formalizes the "future work" classification and prevents these items from being lost in report archives.

---

### Traceability (0.88/1.00)

**Evidence:**

CI gates include inline source annotations (HTML comments) referencing H-34(b), H-01, RT-M-004, and synthesis-validation.md for each gate. The CI gate summary table includes a `Source` column mapping every gate to its authoritative rule.

Security findings reference: CWE IDs, ASVS chapter/requirement codes, H-series rule references (H-34, H-35, H-01), CVSS vector notation, and git commit hashes for prior state.

adv-selector plan references `quality-enforcement.md` with explicit line number citations for the strategy catalog and criticality levels.

The ux-orchestrator.governance.yaml includes inline comments explaining tool tier justification (line 7) and reasoning_effort rationale (line 9).

**Gaps:**

F-004 and F-006 open findings do not have worktracker entity IDs, meaning the traceability chain from finding to remediation tracking is incomplete. Future auditors reading the security reports cannot identify which worktracker story captures the remediation plan.

The Layer 4 body-text changes (9 worker .md files) are listed in the task scope but the specific line-level confirmation for all 9 is only available through the eng-security verification table — not directly verifiable from the deliverable files themselves without reading each agent's `<capabilities>` section individually.

**Improvement Path:**

Add worktracker entity IDs to open findings in security reports. Create a traceability matrix mapping each open finding ID to its worktracker story.

---

## Improvement Recommendations (Priority Ordered)

| Priority | Dimension | Current | Target | Recommendation |
|----------|-----------|---------|--------|----------------|
| 1 | Completeness + Internal Consistency | 0.85 / 0.82 | 0.93 / 0.92 | Execute F-004 documentation sweep: grep-replace `disallowedTools: [Task]` -> `disallowedTools: [Agent]`, `Task tool` -> `Agent tool`, `Via Task Tool` -> `Via Agent Tool` across all sub-skill SKILL.md and mcp-runbook.md files (~40+ occurrences, scriptable). Directly addresses the most significant factual inconsistency in the deliverable. |
| 2 | Methodological Rigor + Traceability | 0.88 / 0.88 | 0.92 / 0.92 | Create worktracker stories for F-004, F-006, and F-003 with owners and target dates. Link story IDs back to the security reports. This converts "acknowledged future work" into tracked commitments. |
| 3 | Methodological Rigor | 0.88 | 0.92 | Implement F-006 CI check in `validate-agent-frontmatter.py`: add deprecation warning for `Task` in `disallowedTools` and error if `Agent` appears in non-T5 `tools:` list (1 developer-hour per red-vuln estimate, exact Python code provided). |
| 4 | Evidence Quality | 0.90 | 0.93 | Enumerate the 79 non-UX worker agents for F-003 by listing file paths, providing verification that none currently have `Agent` in `tools:`. This closes the unverified-count gap in the red-vuln report. |
| 5 | Completeness | 0.85 | 0.95 | After completing P1-P4, re-score. If the sub-skill SKILL.md sweep (P1) is complete and worktracker items are created (P2), the composite score would likely reach 0.92-0.95 range. |

---

## Critical Findings Status (from adv-executor reports)

| Finding ID | Severity | Source | Status | Score Impact |
|------------|----------|--------|--------|--------------|
| eng-security F-001 | HIGH | eng-security | REMEDIATED | No block — remediated |
| eng-security F-002 | HIGH | eng-security | REMEDIATED | No block — remediated |
| eng-security F-003 | MEDIUM | eng-security | OPEN (F-004) | Reduces Completeness, Internal Consistency |
| eng-security F-004 | MEDIUM | eng-security | OPEN (future work) | Reduces Completeness, Internal Consistency |
| red-vuln F-002 | Medium | red-vuln | REMEDIATED | No block — remediated |
| red-vuln F-003 | Medium | red-vuln | OPEN (by design) | Documented, architectural |
| red-vuln F-006 | Medium | red-vuln | OPEN (future work) | Reduces Methodological Rigor |

No CRITICAL findings exist from either security review. Both HIGH findings (eng-security F-001, F-002) are confirmed remediated. Three MEDIUM findings remain open and documented as future work.

**Verdict qualification:** Score is below the 0.95 C4 threshold without critical blockers. The primary gap is documentation completeness (F-004 sub-skill SKILL.md sweep). This is addressable without architectural changes.

---

## Leniency Bias Check

- [x] Each dimension scored independently before computing composite
- [x] Evidence documented for each score (specific file paths, line numbers, confirmed grep results)
- [x] Uncertain scores resolved downward: Completeness scored 0.85 not 0.90 because F-004 gap is material at C4 criticality; Internal Consistency scored 0.82 not 0.87 because factual contradiction in sub-skill SKILL.md is a genuine inconsistency not merely a documentation lag
- [x] First-draft calibration not applicable here (this is a code modification deliverable, not a first draft)
- [x] No dimension scored above 0.95; Evidence Quality at 0.90 is the highest, justified by per-finding CWE/CVSS/ASVS citations with file/line evidence from two independent reviewers
- [x] Threshold of 0.95 (C4 user-specified) is stricter than standard 0.92; scoring reflects this higher bar

---

## Session Context (Handoff Schema)

```yaml
verdict: REVISE
composite_score: 0.865
threshold: 0.95
weakest_dimension: internal_consistency
weakest_score: 0.82
critical_findings_count: 0
high_findings_remediated: 2
medium_findings_open: 3
iteration: 1
improvement_recommendations:
  - "Execute F-004 documentation sweep across all sub-skill SKILL.md and mcp-runbook.md files (~40+ occurrences)"
  - "Create worktracker stories for F-004, F-006, F-003 with owners and target dates"
  - "Implement F-006 CI check in validate-agent-frontmatter.py (1 developer-hour)"
  - "Enumerate 79 non-UX worker agents to close F-003 unverified count"
```

---

*Report generated by adv-scorer (S-014 LLM-as-Judge)*
*SSOT Reference: `.context/rules/quality-enforcement.md` [Quality Gate, Dimensions, Weights]*
*Strategy Findings: `skills/eng-team/output/STORY-013-M007/eng-security-disallowed-tools-review.md`, `skills/eng-team/output/STORY-013-M007/red-vuln-agent-tool-access.md`*
*Constitutional Compliance: P-001 (evidence-based), P-002 (persisted to file), P-003 (no subagents spawned), P-022 (no inflation — leniency bias check completed)*
*Date: 2026-03-29*
*Model: claude-sonnet-4-6*
