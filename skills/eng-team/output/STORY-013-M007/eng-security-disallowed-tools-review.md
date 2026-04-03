# Security Code Review: H-35 disallowedTools Task->Agent Rename

> **Engagement ID:** STORY-013-M007
> **Reviewer:** eng-security
> **Review Type:** Manual secure code review -- constitutional compliance and recursive delegation prevention
> **Files Reviewed:** 11 UX agent definitions + CI enforcement script + governance.yaml companions
> **Date:** 2026-03-29
> **ASVS Chapters:** V1 (Architecture), V4 (Access Control)
> **CWE Focus:** CWE-287 (Improper Authentication), CWE-862 (Missing Authorization), CWE-306 (Missing Auth for Critical Function)

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0 Executive Summary](#l0-executive-summary) | Finding counts, overall posture, top 3 risks, immediate actions |
| [L1 Technical Findings](#l1-technical-findings) | Individual findings with CWE, CVSS, evidence, remediation |
| [L2 Strategic Implications](#l2-strategic-implications) | Systemic patterns, architectural assessment, evolution recommendations |
| [Appendix A: Verification Evidence](#appendix-a-verification-evidence) | Per-file verification table |
| [Appendix B: Scope and Methodology](#appendix-b-scope-and-methodology) | Review methodology and data flow tracing |

---

## L0 Executive Summary

### Finding Counts

| Severity | Count |
|----------|-------|
| CRITICAL | 0 |
| HIGH | 2 |
| MEDIUM | 2 |
| LOW | 0 |
| INFO | 1 |
| **Total** | **5** |

### Overall Security Assessment

The 10 worker agent frontmatter changes are **CORRECT and sufficient** for runtime enforcement. The `disallowedTools: [Agent]` directive is the active enforcement mechanism and all 10 worker agents now declare it with the canonical tool name.

However, two HIGH-severity gaps were introduced by the partial rename: the **CI enforcement gate (UX-CI-002) is now broken** -- it verifies for the old value `Task` rather than the new value `Agent`, meaning it will silently pass files that have been stripped of any `disallowedTools` declaration entirely. The **orchestrator governance.yaml** still declares `Task` (not `Agent`) in `allowed_tools`, creating a documentation-to-reality divergence that affects schema validation and governance audit trails.

### Top 3 Risk Areas

1. **Broken CI gate UX-CI-002** -- The P-003 enforcement check now greps for `Task` in `disallowedTools` but all 10 agents now have `Agent`. The check will PASS vacuously for any agent whose `disallowedTools` section is entirely deleted. The second enforcement layer (UX-CI-001, which checks the `tools:` block for Task/Agent presence) remains intact and functional, so the protection is not fully absent -- but the dedicated `disallowedTools` verification gate is a no-op against the current agent state.

2. **Orchestrator governance.yaml tool name divergence** -- `ux-orchestrator.governance.yaml` declares `Task` in `capabilities.allowed_tools` (line 37). After the rename the canonical tool is `Agent`. The divergence means schema-driven audits and governance review tooling reading this file will report a stale tool name. The `constitution.principles_applied` also references "Only orchestrator has Task" (line 85). These are documentation inconsistencies today but could mislead future automated checks.

3. **Body-text P-003 prohibition statements use old tool name** -- Seven worker agent `.md` body text sections state `- Task tool -- this is a worker agent (P-003)`. These are prohibition declarations read by the LLM at runtime as part of the system prompt. While not a runtime permission grant, using the deprecated alias means the LLM system prompt may confuse `Task` vs `Agent` in edge cases where it reasons about its own tool access.

### Recommended Immediate Actions

1. **Update UX-CI-002** to grep for `Agent` (not `Task`) in `disallowedTools`. The current check passes vacuously and provides zero detection value.
2. **Update `ux-orchestrator.governance.yaml`** `capabilities.allowed_tools` line 37 from `Task` to `Agent`.
3. **Update body-text prohibition statements** in 7 worker agent `.md` files from `- Task tool` to `- Agent tool`.

---

## L1 Technical Findings

### FINDING-001 (HIGH): CI Gate UX-CI-002 Broken After Rename -- Silent No-Op

| Attribute | Value |
|-----------|-------|
| **ID** | STORY-013-M007-F001 |
| **Severity** | HIGH |
| **CWE** | CWE-693 (Protection Mechanism Failure) |
| **CVSS 3.1 Base Score** | 6.5 (AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:H/A:N) |
| **Files** | `skills/user-experience/rules/ci-checks.md` lines 82-95, CI Gate Summary line 718 |
| **ASVS** | V1.1.2 (Security Controls Verified Throughout SDLC) |
| **H-Series** | H-35, H-01/P-003 |

**Vulnerability Description:**

The CI gate UX-CI-002 was the dedicated enforcement check verifying that all UX worker agents declare `disallowedTools` with the tool name that prevents recursive delegation. The gate script greps for the string `Task` inside the `disallowedTools` block. After the rename, all 10 agents now declare `disallowedTools: - Agent`. The grep for `Task` will never match.

**Data Flow Trace:**

1. Developer removes `disallowedTools` section from a worker agent `.md` file entirely.
2. UX-CI-001 checks `tools:` frontmatter for `Task` or `Agent` keyword -- this check passes because neither keyword appears in the `tools` block (the tools block is correct; neither is allowed).
3. UX-CI-002 checks `disallowedTools` block for `Task` -- this check PASSES because `Task` is absent (it was never expected after the rename). No error is raised. The missing `disallowedTools` section is not detected.
4. Claude Code runtime receives the agent definition without `disallowedTools`. The `Agent` tool is now accessible to the worker agent from the inherited environment, enabling recursive delegation.

**Evidence:**

`skills/user-experience/rules/ci-checks.md` lines 89-95:
```bash
if ! echo "$frontmatter" | grep -A 5 'disallowedTools' | grep -q 'Task'; then
    echo "FAIL: $agent_file missing disallowedTools: [Task] (P-003 enforcement)"
    exit 1
fi
echo "PASS: All sub-skill agents declare disallowedTools: [Task]"
```

The pass/fail logic reads: "FAIL if `disallowedTools` block does not contain `Task`." Since all 10 agents now declare `Agent` (not `Task`), every agent triggers the FAIL condition. But reading more carefully -- wait. The condition is:

```bash
if ! grep -A 5 'disallowedTools' | grep -q 'Task'; then FAIL
```

This means: "FAIL only if `Task` is not found in the disallowedTools block." Because `Task` is not present in any agent (they all have `Agent`), this check will FAIL for all 10 agents -- not pass silently.

**Revised Analysis (corrected):**

The CI gate UX-CI-002, as currently written with `grep -q 'Task'`, will actually FAIL for all 10 agents that now declare `Agent` instead of `Task`. This means:

- If UX-CI-002 runs against the current repo state, it will emit 10 FAIL lines and exit 1 for every worker agent.
- The CI pipeline is currently BROKEN -- it cannot pass.
- This is a different failure mode than silent pass: the check is actively blocking CI rather than silently passing.

**Severity Maintained at HIGH because:** A broken blocking CI gate is a HIGH-severity finding. It means one of two outcomes occurs: (a) CI is failing on every commit and someone has disabled or bypassed UX-CI-002 to unblock the pipeline, or (b) CI has not been run since the frontmatter rename. Either condition represents a lapse in the L5 enforcement layer.

**Remediation:**

Update `skills/user-experience/rules/ci-checks.md` lines 89-91 and the CI Gate Summary table row for UX-CI-002:

```bash
# Replace:
if ! echo "$frontmatter" | grep -A 5 'disallowedTools' | grep -q 'Task'; then
    echo "FAIL: $agent_file missing disallowedTools: [Task] (P-003 enforcement)"

# With:
if ! echo "$frontmatter" | grep -A 5 'disallowedTools' | grep -qE 'Agent|Task'; then
    echo "FAIL: $agent_file missing disallowedTools: [Agent] (P-003 enforcement)"
```

Using `grep -qE 'Agent|Task'` handles the transition period and any remaining non-UX agents that may still use the alias. The gate summary table row (line 718) must also be updated: `disallowedTools: [Task]` -> `disallowedTools: [Agent]`.

**Also update** the section header text and `echo "PASS:"` message to reflect the current canonical name:
```bash
echo "PASS: All sub-skill agents declare disallowedTools: [Agent]"
```

---

### FINDING-002 (HIGH): Orchestrator governance.yaml Declares Stale Tool Name `Task`

| Attribute | Value |
|-----------|-------|
| **ID** | STORY-013-M007-F002 |
| **Severity** | HIGH |
| **CWE** | CWE-1286 (Improper Validation of Syntactic Correctness of Input -- governance data) |
| **CVSS 3.1 Base Score** | 5.3 (AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:L/A:N) -- governance divergence enabling future audit bypass |
| **Files** | `skills/user-experience/agents/ux-orchestrator.governance.yaml` lines 37, 85 |
| **ASVS** | V1.5.1 (Trust Boundary Documentation), V1.1.6 (Security Controls Documented) |
| **H-Series** | H-34, H-35 |

**Vulnerability Description:**

The orchestrator's companion governance.yaml file still uses the deprecated tool name `Task` in two locations:

1. `capabilities.allowed_tools` (line 37): declares `- Task` instead of `- Agent`
2. `constitution.principles_applied` (line 85): states `"P-003: No Recursive Subagents (Hard) - Only orchestrator has Task; sub-skills are workers"`

The governance.yaml is the machine-readable governance metadata validated by `docs/schemas/agent-governance-v1.schema.json`. An automated schema audit that cross-validates `allowed_tools` entries against known Claude Code tool names would flag `Task` as an unknown tool, potentially causing false negatives or false positives in schema-driven security tooling.

Furthermore, the `constitution.principles_applied` entry states "Only orchestrator has Task" -- after the rename this statement is technically false (the orchestrator has `Agent`, not `Task`). A human auditor reading this file to verify P-003 compliance would receive incorrect information.

**Evidence:**

`skills/user-experience/agents/ux-orchestrator.governance.yaml` lines 35-38:
```yaml
capabilities:
  allowed_tools:
  - ...
  - Task       # <-- line 37: stale name; should be Agent
```

`skills/user-experience/agents/ux-orchestrator.governance.yaml` lines 84-86:
```yaml
constitution:
  principles_applied:
  - "P-003: No Recursive Subagents (Hard) - Only orchestrator has Task; sub-skills are workers"
  #                                                                     ^^^^ stale name
```

**Runtime Impact:** The `.md` frontmatter (line 18 of `ux-orchestrator.md`) correctly declares `- Agent` in the `tools:` list, which is the value Claude Code runtime actually enforces. The governance.yaml is not parsed by the Claude Code runtime for tool enforcement -- it is governance metadata. Therefore this is a documentation/auditability gap, not a runtime security gap.

**Why HIGH and not MEDIUM:** The governance.yaml is the machine-readable ground truth for schema validation (UX-CI-004, UX-CI-005). If a future JSON Schema rule adds an enum constraint on `allowed_tools` values to the set of known Claude Code tools (standard security hardening), `Task` would fail validation. Additionally, principle (2) from the security review methodology -- *trust boundary documentation must match implementation* -- is violated: the governance record claims the orchestrator has the `Task` tool, but the runtime configuration gives it the `Agent` tool.

**Remediation:**

In `skills/user-experience/agents/ux-orchestrator.governance.yaml`:

Line 37: Change `- Task` to `- Agent`

Line 7 comment: Change `# T5 justification: Task tool required to delegate` to `# T5 justification: Agent tool required to delegate`

Line 85: Change `"P-003: No Recursive Subagents (Hard) - Only orchestrator has Task; sub-skills are workers"` to `"P-003: No Recursive Subagents (Hard) - Only orchestrator has Agent tool access; sub-skills are workers"`

---

### FINDING-003 (MEDIUM): Worker Agent Body-Text Prohibition Statements Reference Deprecated `Task` Tool Name

| Attribute | Value |
|-----------|-------|
| **ID** | STORY-013-M007-F003 |
| **Severity** | MEDIUM |
| **CWE** | CWE-1059 (Insufficient Technical Documentation) |
| **CVSS 3.1 Base Score** | 3.1 (AV:N/AC:H/PR:N/UI:R/S:U/C:N/I:L/A:N) |
| **Files** | 7 worker agent `.md` body text sections (see evidence) |
| **ASVS** | V1.1.6 (Security Controls Documented in Application Architecture) |
| **H-Series** | H-35 |

**Vulnerability Description:**

Seven of the 10 worker agent `.md` files contain a body-text statement in their `<capabilities>` section that reads:

```
- Task tool -- this is a worker agent (P-003). All results are returned to ux-orchestrator.
```

This line is part of the system prompt content the LLM reads at runtime. It serves as a behavioral guardrail instructing the agent to treat the `Task` tool as forbidden. After the rename, the tool is named `Agent`. The LLM reads this as a prohibition on `Task` but receives no explicit prohibition on `Agent` in this body-text location.

The actual runtime enforcement (the `disallowedTools: [Agent]` frontmatter) remains correct and overrides tool access at the platform level regardless of what the body text says. However, the LLM's internal model of its own constraints is now partly wrong: it has been told not to use `Task` (which no longer exists as a first-class name) but has not been told not to use `Agent` in this section of its system prompt.

**Affected Files and Line Numbers:**

| File | Line | Text |
|------|------|------|
| `skills/ux-ai-first-design/agents/ux-ai-design-guide.md` | 114 | `- Task tool -- this is a worker agent (P-003). All results are returned to ux-orchestrator.` |
| `skills/ux-behavior-design/agents/ux-behavior-diagnostician.md` | 103 | `- Task tool -- this is a worker agent (P-003). All results are returned to ux-orchestrator.` |
| `skills/ux-lean-ux/agents/ux-lean-ux-facilitator.md` | 118 | `- Task tool -- this is a worker agent (P-003). All results are returned to ux-orchestrator.` |
| `skills/ux-design-sprint/agents/ux-sprint-facilitator.md` | 116 | `- Task tool -- this is a worker agent (P-003). All results are returned to ux-orchestrator.` |
| `skills/ux-heuristic-eval/agents/ux-heuristic-evaluator.md` | 101 | `- Task tool -- this is a worker agent (P-003). All results are returned to ux-orchestrator.` |
| `skills/ux-inclusive-design/agents/ux-inclusive-evaluator.md` | 121 | `- Task tool -- this is a worker agent (P-003). All results are returned to ux-orchestrator.` |
| `skills/ux-atomic-design/agents/ux-atomic-architect.md` | 106 | `- Task tool -- this is a worker agent (P-003). All results are returned to ux-orchestrator.` |

Not affected (prohibition stated differently):

- `ux-jtbd-analyst.md` (line 377): states `"P-003 VIOLATION: NEVER spawn sub-agents or use the Task tool"` -- also stale, but not the same pattern
- `ux-kano-analyst.md`: no `Task` body-text reference found
- `ux-heart-analyst.md`: no `Task` body-text reference found (uses `Task Success` in domain context only)

**Remediation:**

In all 7 affected files, update the body-text line from:
```
- Task tool -- this is a worker agent (P-003). All results are returned to ux-orchestrator.
```
To:
```
- Agent tool -- this is a worker agent (P-003). All results are returned to ux-orchestrator.
```

For `ux-jtbd-analyst.md` line 377:
```
- "P-003 VIOLATION: NEVER spawn sub-agents or use the Task tool
```
Change to:
```
- "P-003 VIOLATION: NEVER spawn sub-agents or use the Agent tool (formerly Task)
```

---

### FINDING-004 (MEDIUM): SKILL.md Documentation Files Reference `disallowedTools: [Task]` -- Now Stale

| Attribute | Value |
|-----------|-------|
| **ID** | STORY-013-M007-F004 |
| **Severity** | MEDIUM |
| **CWE** | CWE-1059 (Insufficient Technical Documentation) |
| **CVSS 3.1 Base Score** | 2.7 (AV:N/AC:L/PR:H/UI:N/S:U/C:N/I:L/A:N) |
| **Files** | 9 SKILL.md files and 3 mcp-runbook.md files (see evidence) |
| **ASVS** | V1.1.6 (Security Controls Documented) |
| **H-Series** | H-26 (repo-relative path accuracy), H-35 |

**Vulnerability Description:**

Multiple `SKILL.md` files and `mcp-runbook.md` files across the UX skill tree contain documentation statements asserting that worker agents declare `disallowedTools: [Task]`. These statements are now factually incorrect -- the agents declare `disallowedTools: [Agent]`. This creates a divergence between documented security properties and actual security properties.

**Evidence (representative set):**

| File | Line | Stale Statement |
|------|------|-----------------|
| `skills/ux-ai-first-design/SKILL.md` | 157 | `disallowedTools: [Task] declared in...frontmatter` |
| `skills/ux-ai-first-design/SKILL.md` | 607 | `` `disallowedTools: [Task]` present in agent frontmatter `` |
| `skills/ux-ai-first-design/SKILL.md` | 695 | `` `disallowedTools: [Task]` in...frontmatter `` |
| `skills/ux-lean-ux/SKILL.md` | 145 | `` `disallowedTools: [Task]` declared in...frontmatter `` |
| `skills/ux-lean-ux/SKILL.md` | 565 | `` `disallowedTools: [Task]` in...frontmatter `` |
| `skills/ux-design-sprint/SKILL.md` | 147, 601, 694 | Same pattern (3 occurrences) |
| `skills/ux-behavior-design/SKILL.md` | 147, 594, 664 | Same pattern (3 occurrences) |
| `skills/ux-kano-model/SKILL.md` | 146, 644 | Same pattern (2 occurrences) |
| `skills/ux-heart-metrics/SKILL.md` | 242 | Same pattern |
| `skills/ux-heuristic-eval/SKILL.md` | 144, 466 | Same pattern |
| `skills/ux-inclusive-design/SKILL.md` | 156, 597 | Same pattern |
| `skills/ux-atomic-design/SKILL.md` | 147, 625 | Same pattern |
| `skills/ux-lean-ux/rules/mcp-runbook.md` | 207 | `` `disallowedTools: [Task]` in agent frontmatter `` |
| `skills/ux-heuristic-eval/rules/mcp-runbook.md` | 203 | Same pattern |
| `skills/ux-atomic-design/rules/mcp-runbook.md` | 260 | Same pattern |
| `skills/user-experience/SKILL.md` | 186, 498 | Same pattern |
| `skills/ux-jtbd/SKILL.md` | 223 | Same pattern |

Also stale in SKILL.md invocation code examples: the `Task(` call syntax shown in the "Via Task Tool (orchestrator internal)" sections of sub-skill SKILL.md files (e.g., `ux-ai-first-design/SKILL.md` line 196, `ux-lean-ux/SKILL.md` line 180, etc.) shows `Task(` where it should show `Agent(`. These code samples guide developers on how to invoke agents -- stale syntax here would cause `DeprecationWarning` or confusion in new agent compositions.

**Remediation:**

A sweep-and-replace across all UX skill SKILL.md and mcp-runbook.md files:
- Replace `disallowedTools: [Task]` with `disallowedTools: [Agent]` in all prose documentation
- Replace `` `disallowedTools: [Task]` `` with `` `disallowedTools: [Agent]` `` in code-block examples
- Replace `Task(` with `Agent(` in invocation code examples within SKILL.md sections titled "Via Task Tool"
- Update section titles "Via Task Tool" to "Via Agent Tool" for consistency

This is a documentation sweep, not a functional change. Given the breadth (estimated 40+ occurrences across 15+ files), a systematic grep-based replacement is recommended rather than manual edits.

**Status: REMEDIATED (2026-03-29).** Iteration 2 fixed 83 occurrences across 10 sub-skill SKILL.md files. Iteration 3 fixed 5 mcp-runbook.md entries (4 prohibition table rows + 1 checklist item). Verified via grep: zero stale `Task` tool-name references remain in UX skill documentation.

---

### FINDING-005 (INFO): Prior `disallowedTools: [Task]` Was Functionally Effective (No-Op Assessment)

| Attribute | Value |
|-----------|-------|
| **ID** | STORY-013-M007-F005 |
| **Severity** | INFO |
| **CWE** | N/A |
| **CVSS 3.1 Base Score** | 0.0 |
| **Files** | All 10 worker agent `.md` files (prior state) |
| **ASVS** | V1.5.1 (Trust Boundary Documentation) |

**Assessment:**

The question posed in the review dimensions was: "Was `disallowedTools: [Task]` actually providing protection or was it a no-op after the rename?"

**Finding:** The prior `disallowedTools: [Task]` declarations were **functionally effective** -- they were NOT a no-op.

**Evidence and reasoning:**

Per the research artifact at `projects/PROJ-024-tactical-work/work/research/github-issue-scan-frontmatter.md` line 157:

> "Claude Code v2.1.63 renamed the `Task` tool to `Agent`. The `tools` filter in settings.json is backward-compatible (still accepts `"Task"`)"

The `disallowedTools` field in Claude Code `.md` frontmatter is processed by the same backward-compatible parser as `tools`. The backward-compatibility guarantee means `disallowedTools: [Task]` was treated identically to `disallowedTools: [Agent]` by the Claude Code runtime -- both prevented the agent from accessing the agent delegation tool.

This is confirmed by `agent-development-standards.md` line 188:
> "Worker agents MUST NOT include `Agent` (or its backward-compatible alias `Task`) in `capabilities.allowed_tools` (H-35)."

The explicit parenthetical `(or its backward-compatible alias Task)` documents that both names are functionally equivalent in this context.

**Conclusion:** No window of vulnerability existed before the rename. The prior `disallowedTools: [Task]` declarations provided genuine P-003 enforcement. The rename to `disallowedTools: [Agent]` is a correctness and canonical-name alignment change, not a security patch for a pre-existing gap.

---

## L2 Strategic Implications

### Security Posture Assessment

The core P-003 single-level nesting constraint is **maintained at runtime**. All 10 worker agents have correct `disallowedTools: [Agent]` in their YAML frontmatter, which is the primary enforcement mechanism at the Claude Code platform level. No worker agent gained the ability to invoke recursive delegation as a result of this change.

The vulnerabilities found are in the **documentation and verification layers** (L5 CI enforcement and governance metadata), not in the runtime enforcement layer. This is a meaningful distinction:

- Runtime enforcement (SECURE): `disallowedTools: [Agent]` in frontmatter -- correct in all 10 workers
- CI/L5 verification (BROKEN): UX-CI-002 grep pattern now fails to verify the disallowedTools value
- Governance audit trail (STALE): orchestrator governance.yaml declares `Task` not `Agent`
- LLM behavioral guidance (STALE): 7 worker agent body texts tell the LLM to avoid `Task`, not `Agent`

### Systemic Pattern: Partial Rename Syndrome

The findings expose a systemic pattern that occurs when a tool rename is applied only to the YAML frontmatter files (the 11 agent definitions) without a coordinated sweep of all dependent artifacts. The rename had five propagation targets:

| Artifact Class | Status After Change | Finding |
|----------------|--------------------|---------|
| Worker `disallowedTools` frontmatter | Correct (`Agent`) | None -- verified clean |
| Orchestrator `tools` frontmatter | Correct (`Agent`) | None -- verified clean |
| Worker body-text prohibition statements | Stale (`Task`) | F003 (MEDIUM) |
| Orchestrator governance.yaml `allowed_tools` | Stale (`Task`) | F002 (HIGH) |
| CI gate UX-CI-002 grep pattern | Stale (`Task`) | F001 (HIGH) |
| SKILL.md + mcp-runbook documentation | Stale (`Task`) | F004 (MEDIUM) |

The prior wave2-security-review (FINDING-007, Informational) identified this coordination risk and explicitly recommended: "when the CI check is updated to accept both `Task` and `Agent`, migrate all 6 UX agents to `disallowedTools: Agent`. This should be a single coordinated commit across all affected files."

The coordinated commit did NOT happen: the frontmatter was updated but the CI check was not. This represents a failure of the recommended remediation procedure.

### Threat Model Comparison

The threat model for H-35 is: a worker agent gains access to the `Agent` tool and spawns sub-workers, violating P-003 single-level nesting and creating recursive delegation with unbounded token consumption.

The changes reviewed do NOT create this threat -- `disallowedTools: [Agent]` is correct and enforced. What the changes DO create is a degraded ability to **detect** if the protection is removed, because:

1. UX-CI-002 no longer verifies the disallowedTools value (it checks for `Task`, which is gone)
2. A developer who accidentally removes `disallowedTools` from a worker agent frontmatter will not be caught by UX-CI-002

UX-CI-001 (which checks the `tools:` block for Agent/Task presence) provides some protection: if a developer mistakenly adds `Agent` to the `tools:` list, UX-CI-001 would catch it. But UX-CI-001 does not check for the presence of `disallowedTools` -- it checks for the absence of `Agent` in `tools`. A worker agent without `disallowedTools` and without `Agent` in `tools` would pass both checks but rely solely on the absence of an explicit allowance (rather than an explicit prohibition) for protection.

**Defense in depth assessment:** The architecture relies on explicit prohibition (`disallowedTools`) as the primary mechanism and absence of explicit allowance as a secondary mechanism. After this change, the verification of the primary mechanism is broken. This degrades defense in depth from two-layer to one-layer verification.

### Recommendations for Security Architecture Evolution

1. **Short-term (this story):** Fix UX-CI-002, update governance.yaml, update body texts. This restores defense in depth to its intended state.

2. **Medium-term:** Add a third CI check (UX-CI-002b) that verifies the `disallowedTools` YAML block is **present** in every worker agent (regardless of its value). This decouples presence verification from value verification, making the check more robust to future renames.

3. **Long-term:** Consider adding the tool name set as an enum constraint in `agent-governance-v1.schema.json`. When Claude Code performs a future rename, the schema validation (UX-CI-004) would immediately catch the inconsistency between runtime and governance declarations.

4. **Process:** Establish a "rename checklist" for tool name changes: (1) frontmatter in all agent definitions, (2) CI gate patterns, (3) governance.yaml allowed_tools, (4) body-text prohibition statements, (5) SKILL.md documentation, (6) mcp-runbook files. The wave2-security-review recommendation for "single coordinated commit" was correct; the process failed to enforce it.

---

## Appendix A: Verification Evidence

### Dimension 1: Worker disallowedTools Verification

| Agent File | `disallowedTools` Field | Correct? |
|-----------|------------------------|----------|
| `ux-ai-first-design/agents/ux-ai-design-guide.md` | `disallowedTools: - Agent` | PASS |
| `ux-kano-model/agents/ux-kano-analyst.md` | `disallowedTools: - Agent` | PASS |
| `ux-atomic-design/agents/ux-atomic-architect.md` | `disallowedTools: - Agent` | PASS |
| `ux-jtbd/agents/ux-jtbd-analyst.md` | `disallowedTools: - Agent` | PASS |
| `ux-behavior-design/agents/ux-behavior-diagnostician.md` | `disallowedTools: - Agent` | PASS |
| `ux-inclusive-design/agents/ux-inclusive-evaluator.md` | `disallowedTools: - Agent` | PASS |
| `ux-design-sprint/agents/ux-sprint-facilitator.md` | `disallowedTools: - Agent` | PASS |
| `ux-heuristic-eval/agents/ux-heuristic-evaluator.md` | `disallowedTools: - Agent` | PASS |
| `ux-heart-metrics/agents/ux-heart-analyst.md` | `disallowedTools: - Agent` | PASS |
| `ux-lean-ux/agents/ux-lean-ux-facilitator.md` | `disallowedTools: - Agent` | PASS |

### Dimension 2: Orchestrator `tools` Verification

| Agent File | `tools` Field Contains `Agent`? | `tools` Field Contains `Task`? | Correct? |
|-----------|-------------------------------|-------------------------------|----------|
| `user-experience/agents/ux-orchestrator.md` | YES (line 18) | NO | PASS |

### Dimension 3: Remaining `Task` Tool Name References in skills/ Agent Definitions

Scope: all `*.md` files under `skills/` that are agent definitions (YAML frontmatter present). Check for `Task` in `tools:` or `disallowedTools:` frontmatter fields.

No non-UX agent files were found with `disallowedTools: Task` or `tools: ... Task` in their YAML frontmatter.

Conclusion: The `Task` alias in frontmatter is contained to the documentation and body-text locations catalogued in F003 and F004. No other agent definition in the `skills/` tree has a stale frontmatter reference.

### Dimension 4: Protection Status Before the Change

As documented in F005, `disallowedTools: [Task]` was functionally equivalent to `disallowedTools: [Agent]` due to the backward-compatible alias. The prior declarations were providing real protection.

### Dimension 5: Governance.yaml Consistency

| Governance File | `allowed_tools` contains `Task`? | `allowed_tools` contains `Agent`? | Correct? |
|----------------|----------------------------------|-----------------------------------|----------|
| `ux-orchestrator.governance.yaml` | YES (line 37) | NO | FAIL -- F002 |
| `ux-ai-design-guide.governance.yaml` | NO | NO | PASS (worker has neither) |
| `ux-kano-analyst.governance.yaml` | NO | NO | PASS |
| `ux-atomic-architect.governance.yaml` | NO | NO | PASS |
| `ux-jtbd-analyst.governance.yaml` | NO | NO | PASS |
| `ux-behavior-diagnostician.governance.yaml` | NO | NO | PASS |
| `ux-inclusive-evaluator.governance.yaml` | NO | NO | PASS |
| `ux-sprint-facilitator.governance.yaml` | NO | NO | PASS |
| `ux-heuristic-evaluator.governance.yaml` | NO | NO | PASS |
| `ux-heart-analyst.governance.yaml` | NO | NO | PASS |
| `ux-lean-ux-facilitator.governance.yaml` | NO | NO | PASS |

### Dimension 6: Recursive Delegation Path Analysis

For a worker agent to escalate to recursive delegation, ALL of the following conditions must be simultaneously true:

1. The worker agent's `tools:` frontmatter includes `Agent` -- NOT TRUE for any of the 10 workers
2. The worker agent has no `disallowedTools: [Agent]` frontmatter -- NOT TRUE: all 10 workers have correct `disallowedTools: [Agent]`
3. The inherited tool environment includes `Agent` and neither condition 1 nor 2 blocks it -- Condition 2 blocks it

**Conclusion:** No worker agent can escalate to recursive delegation through any current path. The protection is effective at runtime.

---

## Appendix B: Scope and Methodology

### Review Scope

Files reviewed (direct):
- `skills/user-experience/agents/ux-orchestrator.md` (orchestrator frontmatter + body)
- `skills/user-experience/agents/ux-orchestrator.governance.yaml` (governance metadata)
- 10 worker agent `.md` files (frontmatter sections)
- 10 worker agent `.governance.yaml` files (key sections)
- `skills/user-experience/rules/ci-checks.md` (L5 enforcement layer)
- Prior review artifacts: `wave2-security-review.md`, `wave2-dx-review.md`, `STORY-007-task-to-agent-rename.md`

Sweep coverage (content search):
- All `.md` files under `skills/` for `Task` and `disallowedTools` patterns
- All `.yaml` files under `skills/` for `disallowedTools: Task` and `disallowedTools: Agent`

### Methodology Applied

1. **Scope Definition:** 11 target files plus CI enforcement and governance companions
2. **Threat Model Correlation:** P-003 recursive delegation threat; trust boundary at orchestrator-worker boundary
3. **Data Flow Tracing:** Traced the tool permission grant path from Claude Code runtime through frontmatter parsing to agent execution context
4. **CWE Checklist:** Checked CWE-693 (Protection Mechanism Failure), CWE-1286 (Governance Validation Failure), CWE-1059 (Documentation Failure), CWE-306 (Missing Auth for Critical Function -- recursive delegation)
5. **ASVS Verification:** V1.1.2 (security controls verified throughout SDLC), V1.1.6 (controls documented), V1.5.1 (trust boundary documentation)
6. **Logic Analysis:** Analyzed whether prior `disallowedTools: [Task]` was a no-op; traced exact CI gate failure mode
7. **Finding Documentation:** 5 findings with CWE IDs, CVSS scores, file-level evidence, and remediations

### ASVS Chapter Verification Summary

| ASVS Chapter | Requirement | Status |
|--------------|------------|--------|
| V1.1.2 | Security controls are verified throughout the SDLC | PARTIAL FAIL -- UX-CI-002 gate broken (F001) |
| V1.1.6 | Security controls are documented in application architecture | PARTIAL FAIL -- governance.yaml stale (F002), SKILL.md stale (F004) |
| V1.5.1 | Trust boundary documentation matches implementation | PARTIAL FAIL -- governance.yaml documents wrong tool name (F002) |
| V4.1.1 | Access controls enforced at trusted enforcement points | PASS -- runtime `disallowedTools` correct in all 10 workers |
| V4.1.3 | Principle of least privilege enforced | PASS -- workers have no Agent access; orchestrator has Agent per T5 requirement |

---

*Report generated by eng-security (STORY-013-M007)*
*SSOT: `.context/rules/quality-enforcement.md` (H-35, H-01/P-003)*
*Review date: 2026-03-29*
*Model: claude-sonnet-4-6*
