# Security Code Review: STORY-011 + STORY-013 Implementation
<!-- REVIEWER: eng-security | DATE: 2026-03-28 | METHODOLOGY: Manual code review, data flow tracing, ASVS V1/V4/V5 verification -->

## Document Sections

| Section | Purpose |
|---------|---------|
| [L0 Executive Summary](#l0-executive-summary) | Finding counts, overall assessment, top risks, immediate actions |
| [L1 Technical Findings](#l1-technical-findings) | Individual findings with CWE, CVSS, evidence, remediation |
| [L2 Strategic Implications](#l2-strategic-implications) | Systemic patterns, architecture posture, recommendations |
| [ASVS Verification Status](#asvs-verification-status) | Chapter-level ASVS 5.0 coverage |
| [Review Scope and Methodology](#review-scope-and-methodology) | Files reviewed, focus areas, data flow traces |

---

## L0 Executive Summary

### Finding Counts by Severity

| Severity | Count |
|----------|-------|
| Critical | 0 |
| High | 1 |
| Medium | 3 |
| Low | 3 |
| Informational | 2 |
| **Total** | **9** |

### Overall Security Assessment

The STORY-011 and STORY-013 changes represent a **controlled, well-structured expansion of tool access** from T2 to T3 across multiple agents. The implementation is largely correct. No critical vulnerabilities were identified. One high-severity finding concerns the `pm-pmm` SKILL.md granting the `Agent` tool to a skill whose worker agents explicitly deny it -- a trust boundary inconsistency that creates a privilege escalation path. Three medium findings relate to incomplete citation guardrails, an undeclared `allowed_tools` on an upgraded agent, and `disallowedTools: Task` entries that reference the deprecated alias rather than the canonical `Agent` tool name.

### Top 3 Risk Areas

1. **pm-pmm SKILL.md `Agent` tool exposure (High):** The skill-level `allowed-tools` field contains `Agent`, but the P-003 compliance section explicitly states workers cannot use it. If the SKILL.md is used as a permission manifest (e.g., by a future orchestrator or CI validator), this inconsistency means a worker agent could gain delegation capability, violating H-35/P-003.

2. **T3 agents missing `all_claims_must_have_citations` guardrail (Medium):** Multiple newly-upgraded T3 agents (`nse-reporter`, `orch-planner`, `orch-synthesizer`, `orch-tracker`) that now have WebSearch/WebFetch access do not declare `all_claims_must_have_citations` in `output_filtering`. Per agent-development-standards AD-M-006 and T3 tier constraints, external data access requires citation guardrails. Unverifiable external claims in status reports and orchestration plans could propagate unsourced information downstream.

3. **`disallowedTools: Task` not updated to `Agent` on 6 UX workers (Medium):** The `ux-heart-analyst` and `ux-kano-analyst` (changed in this PR) plus 4 pre-existing UX agents declare `disallowedTools: Task`. H-35 states workers MUST NOT include `Agent` (or its backward-compatible alias `Task`) -- meaning `Task` remains functionally equivalent and enforcement is not broken. However, the CI check at `skills/user-experience/rules/ci-checks.md` explicitly greps for `Task` as the expected value, meaning updating to `Agent` could break the CI gate. This is a documentation/standards drift issue requiring coordinated resolution.

### Recommended Immediate Actions

1. Remove `Agent` from `pm-pmm/SKILL.md` `allowed-tools` field or document precisely why it must remain and who has authority to invoke it. (High -- do before merge)
2. Add `all_claims_must_have_citations` to `output_filtering` in governance.yaml for `nse-reporter`, `orch-planner`, `orch-synthesizer`, and `orch-tracker`. (Medium -- do before merge)
3. Decide and document the `disallowedTools: Task` vs `disallowedTools: Agent` migration policy for UX agents as a follow-on issue. Do not change in this PR without updating CI checks simultaneously.

---

## L1 Technical Findings

### FINDING-001: `pm-pmm` SKILL.md grants `Agent` tool at skill level while P-003 denies it to workers

| Attribute | Value |
|-----------|-------|
| **ID** | SEC-001 |
| **Severity** | High |
| **CWE** | CWE-862 (Missing Authorization) |
| **CVSS 3.1 Base Score** | 6.5 (AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:N) |
| **File** | `skills/pm-pmm/SKILL.md`, line 5 |
| **ASVS** | V1.5.2 (Trust Boundaries), V4.1.1 (Access Control Design) |

**Evidence:**

`skills/pm-pmm/SKILL.md` line 5:
```yaml
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Agent, WebSearch, WebFetch
```

`skills/pm-pmm/SKILL.md` lines 210-214 (P-003 Compliance section):
```
- Agents CANNOT invoke other agents.
- Agents CANNOT spawn subagents.
- Agents do NOT have the Task tool.
```

**Data Flow Trace:**

The skill-level `allowed-tools` field is the runtime permission manifest for the skill. Worker agents under this skill operate with permissions derived from this field (or their own frontmatter if it overrides). The P-003 compliance section asserts workers have no Task/Agent access, but the SKILL.md permission manifest says `Agent` is allowed. If any consumer (orchestrator, CI validator, or future runtime enforcement layer) reads SKILL.md `allowed-tools` to determine what the skill can do, `Agent` is present -- contradicting the constitutional constraint H-35 that workers MUST NOT have Agent/Task access.

**Analysis:**

This is the classic dual-authority problem: a higher-level manifest grants a capability, while a lower-level policy denies it. The correct resolution depends on which authority is consulted at runtime. Current agents likely respect their own frontmatter `disallowedTools`, so practical exploitation would require a misconfigured or newly-added worker agent that omits its own `disallowedTools` declaration. The SKILL.md field is the "floor" permission that could be inherited.

The `Agent` tool was presumably added to support orchestrator-level invocation (the SKILL.md main context does need `Agent` to invoke worker agents). However, granting it at the SKILL.md level grants it to the entire skill surface. The correct pattern (consistent with all other skills reviewed) is to restrict `Agent` to orchestrator agents and explicitly forbid it from worker frontmatters via `disallowedTools: Agent`.

**Recommendation:**

Option A (preferred): Remove `Agent` from `allowed-tools` in `SKILL.md`. The main context (Claude session) inherits Agent capability from its own session-level tool grants, not from the SKILL.md manifest. SKILL.md `allowed-tools` should reflect what worker agents within the skill may use.

Option B: If `Agent` must remain for a specific architectural reason, add a comment explaining which agent (orchestrator role) requires it, and verify that all 5 worker agents have `disallowedTools: Agent` in their individual frontmatters.

---

### FINDING-002: `nse-reporter` upgraded to T3 but governance.yaml has no `allowed_tools` and no citation guardrail

| Attribute | Value |
|-----------|-------|
| **ID** | SEC-002 |
| **Severity** | Medium |
| **CWE** | CWE-284 (Improper Access Control) |
| **CVSS 3.1 Base Score** | 4.3 (AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:L/A:N) |
| **File** | `skills/nasa-se/agents/nse-reporter.governance.yaml` |
| **ASVS** | V1.2.1 (Least Privilege), V5.4.1 (Unintended Data Exposure) |

**Evidence:**

`nse-reporter.md` frontmatter (line 5):
```yaml
tools: Read, Write, Glob, Grep, WebSearch, WebFetch
```

`nse-reporter.governance.yaml` -- no `capabilities.allowed_tools` key exists anywhere in the file. The `capabilities` block contains only `forbidden_actions`.

`nse-reporter.governance.yaml` `output_filtering` (lines 40-47):
```yaml
output_filtering:
- no_secrets_in_output
- mandatory_disclaimer_on_all_outputs
- prominently_display_RED_items
- include_risk_status_in_all_reports
- report_traceability_metrics
- report_verification_progress
- flag_inconsistencies_between_data_sources
```

`all_claims_must_have_citations` is absent.

**Data Flow Trace:**

`nse-reporter` is a T3 agent with WebSearch and WebFetch access. When generating status reports (NPR 7123.1D Process 16), the agent can call WebSearch to look up NASA standards references, metric benchmarks, or program context. Without a citation guardrail in `output_filtering`, there is no governance-layer enforcement preventing the agent from inserting web-retrieved factual claims into official-looking SE status reports without attribution. The mandatory disclaimer partially mitigates this (it marks all output as AI-generated), but does not provide per-claim sourcing.

**Analysis:**

Per agent-development-standards.md Tool Security Tiers: "T3 agents MUST include citation guardrails in `guardrails.output_filtering`." The `nse-reporter` governance.yaml `output_filtering` meets domain-specific requirements but is missing the T3-mandatory `all_claims_must_have_citations` entry.

Additionally, no `capabilities.allowed_tools` is declared. While the `.md` frontmatter is the authoritative runtime list, the governance.yaml `allowed_tools` is the machine-readable declaration for schema validation. Its absence means the T3 designation in `tool_tier: T3` is unverified against an explicit tool list -- creating a documentation gap that affects CI schema validation.

**Recommendation:**

Add to `nse-reporter.governance.yaml`:
```yaml
capabilities:
  allowed_tools:
  - Read
  - Write
  - Glob
  - Grep
  - WebSearch
  - WebFetch
  forbidden_actions:
  - Spawn recursive subagents (P-003)
  - Override user decisions (P-020)
  - Misrepresent capabilities, findings, or confidence (P-022)
  - Make go/no-go decisions (advisory only)
  - Override domain status assessments
  - Hide adverse information
  - Minimize serious issues
```

And add `all_claims_must_have_citations` to `output_filtering`.

---

### FINDING-003: Three orchestration agents upgraded to T3 without citation guardrails in governance.yaml

| Attribute | Value |
|-----------|-------|
| **ID** | SEC-003 |
| **Severity** | Medium |
| **CWE** | CWE-284 (Improper Access Control) |
| **CVSS 3.1 Base Score** | 4.3 (AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:L/A:N) |
| **Files** | `skills/orchestration/agents/orch-planner.md`, `orch-synthesizer.md`, `orch-tracker.md` |
| **ASVS** | V1.2.1 (Least Privilege), V5.4.1 (Unintended Data Exposure) |

**Evidence:**

All three agents have WebSearch and WebFetch added to their frontmatter `tools` field:

`orch-planner.md` line 5: `tools: Read, Write, Edit, Glob, Grep, Bash, WebSearch, WebFetch`
`orch-synthesizer.md` line 5: `tools: Read, Write, Edit, Glob, Grep, Bash, WebSearch, WebFetch`
`orch-tracker.md` line 5: `tools: Read, Write, Edit, Glob, Grep, Bash, WebSearch, WebFetch`

None of these agents have a companion `*.governance.yaml` file (confirmed by the file list provided). The `.md` bodies contain `output_filtering` sections inside `<guardrails>` blocks, but these are LLM-visible prose, not machine-validated governance declarations. The prose sections state "No secrets in output" but do not include a citation guardrail.

**Data Flow Trace:**

`orch-planner` and `orch-synthesizer` are particularly sensitive: they produce ORCHESTRATION_PLAN.md and final synthesis documents that downstream agents treat as authoritative. If either agent uses WebSearch to look up "orchestration best practices" or "quality gate thresholds" during plan creation and inserts retrieved content without citation, those uncited claims propagate into every agent handoff that references the plan.

`orch-tracker` is less risky for content injection but still has write access to ORCHESTRATION.yaml -- a state file. WebFetch access combined with YAML write access creates a path where an agent could fetch an external URL and write its content to state.

**Analysis:**

These three agents were upgraded in STORY-013 batch. Each gains a meaningful external data access channel (WebSearch/WebFetch) without a corresponding governance-layer citation guardrail. This is the same issue as SEC-002 but affects three agents.

The lack of `.governance.yaml` files for orchestration agents is a pre-existing gap (not introduced in this PR) but becomes more significant when T3 tools are added to agents without machine-readable governance.

**Recommendation:**

For each of the three agents, add citation guardrails to the `<guardrails>` `output_filtering` section in the `.md` body:
- `all_claims_from_websearch_must_cite_source`
- `no_external_content_in_state_files` (for `orch-tracker` specifically)

If `.governance.yaml` files are created for orchestration agents (recommended as a follow-on), include `all_claims_must_have_citations` in `output_filtering`.

---

### FINDING-004: `adv-executor` P-003 self-check references deprecated `Task` tool name

| Attribute | Value |
|-----------|-------|
| **ID** | SEC-004 |
| **Severity** | Low |
| **CWE** | CWE-693 (Protection Mechanism Failure) -- documentation |
| **CVSS 3.1 Base Score** | 2.7 (AV:N/AC:L/PR:H/UI:N/S:U/C:N/I:L/A:N) |
| **File** | `skills/adversary/agents/adv-executor.md`, lines 338-343 |
| **ASVS** | V1.5.1 (Trust Boundary Documentation) |

**Evidence:**

`adv-executor.md` lines 338-343:
```markdown
3. **Direct tool use only** -- This agent may ONLY use: Read, Write, Edit, Glob, Grep
4. **Single-level execution** -- This agent operates as a worker invoked by the main context

If any step in this agent's process would require spawning another agent, HALT and return an error:
"P-003 VIOLATION: adv-executor attempted to spawn a subagent. This agent is a worker and MUST NOT invoke other agents."
```

Line 338 lists only the **pre-STORY-011 tool set** (`Read, Write, Edit, Glob, Grep`) without the newly-added tools (`WebSearch, WebFetch, Context7`).

The agent's runtime frontmatter (line 5) correctly shows:
```yaml
tools: Read, Write, Edit, Glob, Grep, WebSearch, WebFetch
```

**Analysis:**

The P-003 self-check is an LLM-visible safety assertion. Its tool list is stale: it mentions only the T2 tools and omits the three T3 additions from STORY-011. This creates a semantic inconsistency where the self-check could cause the agent to wrongly flag its own legitimate use of WebSearch as a violation or, alternatively, fail to provide accurate guidance about its actual capabilities. Neither outcome is a P-003 violation per se, but it degrades the self-check's protective value.

**Recommendation:**

Update line 338 to:
```
3. **Direct tool use only** -- This agent may ONLY use: Read, Write, Edit, Glob, Grep, WebSearch, WebFetch, mcp__context7__resolve-library-id, mcp__context7__query-docs
```

---

### FINDING-005: `diataxis-explanation` `<capabilities>` block not updated after T2 to T3 upgrade

| Attribute | Value |
|-----------|-------|
| **ID** | SEC-005 |
| **Severity** | Low |
| **CWE** | CWE-693 (Protection Mechanism Failure) -- documentation |
| **CVSS 3.1 Base Score** | 2.3 (AV:N/AC:L/PR:H/UI:N/S:U/C:N/I:L/A:N) |
| **File** | `skills/diataxis/agents/diataxis-explanation.md`, lines 52-60 |
| **ASVS** | V1.5.1 (Trust Boundary Documentation) |

**Evidence:**

`diataxis-explanation.md` frontmatter (line 8):
```yaml
tools: Read, Write, Edit, Glob, Grep, WebSearch, WebFetch
```

`diataxis-explanation.md` `<capabilities>` section (lines 52-60):
```markdown
<capabilities>
Available tools: Read, Write, Edit, Glob, Grep

Tool usage patterns:
- Read design decisions, ADRs, and architectural documents for context
- Search for related concepts and cross-references across the codebase
- Write the explanation to the specified output path
- Read existing docs to understand what needs deeper explanation
</capabilities>
```

The frontmatter grants T3 tools (`WebSearch`, `WebFetch`, `Context7` via mcpServers), but the `<capabilities>` section still lists only T2 tools and contains no usage patterns for the new tools.

**Analysis:**

This is a documentation-tool mismatch. The LLM-visible `<capabilities>` section is the agent's self-description of what it can do. After the T3 upgrade, the agent will have access to WebSearch and WebFetch at runtime (per frontmatter), but its own guidance section tells it these tools are not available. This could cause the agent to under-utilize legitimate tools or cause confusion if it attempts WebSearch and then checks its own capability list.

The `mcpServers: context7: true` entry in frontmatter is also unmentioned in the `<capabilities>` section. The agent's guardrail at line 118 ("Reject paths containing `../` sequences") is positive and unrelated to this finding.

**Recommendation:**

Update the `<capabilities>` section to:
```markdown
<capabilities>
Available tools: Read, Write, Edit, Glob, Grep, WebSearch, WebFetch, Context7 (MCP)

Tool usage patterns:
- Read design decisions, ADRs, and architectural documents for context
- Search for related concepts and cross-references across the codebase
- Write the explanation to the specified output path
- Read existing docs to understand what needs deeper explanation
- WebSearch: look up external context for design rationale, historical background, or framework comparisons when the codebase does not contain sufficient context
- WebFetch: retrieve specific documentation URLs referenced in architectural decisions
- Context7: look up current library or framework documentation when explaining technology choices
</capabilities>
```

---

### FINDING-006: `ux-behavior-diagnostician` governance.yaml declares T3 but `.md` frontmatter has no WebSearch/WebFetch

| Attribute | Value |
|-----------|-------|
| **ID** | SEC-006 |
| **Severity** | Low |
| **CWE** | CWE-284 (Improper Access Control) -- tier-tool mismatch |
| **CVSS 3.1 Base Score** | 2.7 (AV:N/AC:L/PR:H/UI:N/S:U/C:L/I:N/A:N) |
| **File** | `skills/ux-behavior-design/agents/ux-behavior-diagnostician.governance.yaml` and `ux-behavior-diagnostician.md` |
| **ASVS** | V1.2.1 (Least Privilege) |

**Evidence:**

`ux-behavior-diagnostician.governance.yaml` line 9:
```yaml
tool_tier: T3
```

`ux-behavior-diagnostician.governance.yaml` lines 31-36:
```yaml
capabilities:
  allowed_tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash
```

WebSearch, WebFetch, and Context7 are absent from `allowed_tools`. The `.md` frontmatter for this agent was not included in the changed files list for STORY-013 (confirming it is not actually receiving T3 tools in the `.md` frontmatter at this time).

**Analysis:**

The governance.yaml declares `tool_tier: T3` but the `allowed_tools` list contains only T2 tools (Read, Write, Edit, Glob, Grep, Bash). Per the T3 tier definition: "T2 + WebSearch, WebFetch, Context7." A T3 declaration without those tools is either:

(a) Aspirational -- the tier was set to T3 in preparation for a future `.md` update, or
(b) A mismatch -- the tier should remain T2 since the actual tools granted are T2.

Either way, a schema validator checking the governance.yaml will see `tool_tier: T3` and potentially expect WebSearch/WebFetch in `allowed_tools`. The CI gate could either pass (if it only validates tier declaration) or flag a mismatch (if it cross-checks tier against tools). The current state is ambiguous.

**Recommendation:**

Choose one:
- If web tools are intentional: add WebSearch, WebFetch to the `.md` frontmatter `tools` field to match the T3 governance declaration.
- If web tools are not needed: change `tool_tier` back to `T2` in the governance.yaml.

The `ux-behavior-diagnostician` agent per its `.md` body is a convergent diagnostic agent that applies the Fogg B=MAP model to existing product context. It does not appear to require external web research for its core methodology. T2 seems appropriate.

---

### FINDING-007: `disallowedTools: Task` on UX agents references deprecated alias instead of canonical `Agent`

| Attribute | Value |
|-----------|-------|
| **ID** | SEC-007 |
| **Severity** | Informational |
| **CWE** | CWE-1188 (Initialization of a Resource with an Insecure Default) -- process |
| **CVSS 3.1 Base Score** | 0.0 (informational only) |
| **Files** | `ux-heart-analyst.md` (line 22), `ux-kano-analyst.md` (line 28), and 4 pre-existing UX agents |
| **ASVS** | V1.5.1 (Trust Boundary Documentation) |

**Evidence:**

`ux-heart-analyst.md` lines 21-23:
```yaml
disallowedTools:
  - Task
```

`ux-kano-analyst.md` lines 27-29:
```yaml
disallowedTools:
  - Task
```

H-35 from agent-development-standards.md states: "Worker agents (invoked via Agent tool) MUST NOT include `Agent` (or its backward-compatible alias `Task`) in the official `tools` frontmatter field."

H-35 enforces the constraint via disallowedTools. The current value (`Task`) is the backward-compatible alias. The canonical tool name in the current framework is `Agent`.

The CI check at `skills/user-experience/rules/ci-checks.md` lines 89-91 explicitly greps for `Task`:
```bash
if ! echo "$frontmatter" | grep -A 5 'disallowedTools' | grep -q 'Task'; then
```

**Analysis:**

`Task` is a valid backward-compatible alias and H-35 acknowledges it. Enforcement is not broken. However, the two new agents in this PR (`ux-heart-analyst`, `ux-kano-analyst`) introduced `disallowedTools: Task` at a point when the canonical name has shifted to `Agent`. This perpetuates the deprecated alias in new code.

The CI check being hardcoded to `Task` means a global rename to `Agent` would require simultaneous CI check update -- this is a coordination risk rather than a security vulnerability.

**Recommendation:**

This is informational. No security risk exists today. Track as a follow-on cleanup item: when the CI check is updated to accept both `Task` and `Agent`, migrate all 6 UX agents to `disallowedTools: Agent`. This should be a single coordinated commit across all affected files.

---

### FINDING-008: `adv-executor` governance.yaml `forbidden_actions` uses NPT-014 legacy format (not NPT-009)

| Attribute | Value |
|-----------|-------|
| **ID** | SEC-008 |
| **Severity** | Informational |
| **CWE** | N/A (compliance standard) |
| **File** | `skills/adversary/agents/adv-executor.governance.yaml`, lines 52-58 |
| **ASVS** | V1.5.1 |

**Evidence:**

`adv-executor.governance.yaml` lines 52-58:
```yaml
forbidden_actions:
- Spawn recursive subagents (P-003)
- Override user decisions (P-020)
- Return transient output only (P-002)
- Select strategies (adv-selector responsibility)
- Score deliverables with S-014 rubric (adv-scorer responsibility)
- Inflate or minimize findings (P-022)
```

The NPT-009 format (from agent-development-standards ADR-002) requires:
`"{PRINCIPLE} VIOLATION: NEVER {action} -- Consequence: {impact}"`

The current entries use the NPT-014 legacy format: `"{description} ({principle-reference})"`.

The governance.yaml does not declare `capabilities.forbidden_action_format`. Per agent-development-standards, omission implies NPT-014 legacy.

**Analysis:**

The STORY-011 change added `all_claims_must_have_citations` to `output_filtering` (correct for T3), but did not upgrade the `forbidden_actions` to NPT-009 format. This is an improvement opportunity, not a security vulnerability. New agents added in STORY-013 batch (e.g., `ux-kano-analyst`, `ux-heart-analyst`, `ux-behavior-diagnostician`) all correctly use NPT-009 format -- making the `adv-executor` an outlier.

**Recommendation:**

Upgrade `forbidden_actions` to NPT-009 format and add `capabilities.forbidden_action_format: NPT-009-complete`:
```yaml
forbidden_actions:
- "P-003 VIOLATION: NEVER spawn recursive subagents -- Consequence: agent hierarchy violation breaks orchestrator-worker topology and causes uncontrolled token consumption."
- "P-020 VIOLATION: NEVER override user decisions -- Consequence: unauthorized actions erode trust and may cause irreversible changes."
- "P-002 VIOLATION: NEVER return output to transient context only -- Consequence: work product lost on session end; downstream agents cannot access results."
- "P-022 VIOLATION: NEVER inflate or minimize findings -- Consequence: deceptive severity classification undermines quality gate integrity."
```

---

### FINDING-009: `adv-executor` composition YAML `output_filtering` missing citation guardrail added to governance.yaml

| Attribute | Value |
|-----------|-------|
| **ID** | SEC-009 |
| **Severity** | Informational |
| **CWE** | CWE-1022 (Incomplete Implementation) |
| **CVSS 3.1 Base Score** | 0.0 (informational) |
| **File** | `skills/adversary/composition/adv-executor.agent.yaml` |
| **ASVS** | V1.5.1 |

**Evidence:**

`adv-executor.governance.yaml` `output_filtering` (line 29):
```yaml
- all_claims_must_have_citations
```

`adv-executor.agent.yaml` `guardrails.output_filtering` (lines 43-47):
```yaml
output_filtering:
- findings_must_have_severity
- findings_must_have_evidence
- no_vague_findings
```

The `all_claims_must_have_citations` entry added to `governance.yaml` in STORY-011 is not present in `adv-executor.agent.yaml`.

**Analysis:**

The `adv-executor.agent.yaml` is the canonical agent definition per its schema comment (`Schema: docs/schemas/agent-canonical-v1.schema.json`). If this file is consumed by a registry or CI validator separately from `governance.yaml`, the citation guardrail is absent from the canonical definition. These two files should remain in sync. The governance.yaml is authoritative per H-34, but the canonical agent YAML is also machine-consumed.

**Recommendation:**

Add `all_claims_must_have_citations` to `guardrails.output_filtering` in `adv-executor.agent.yaml` to mirror the governance.yaml change.

---

## L2 Strategic Implications

### Security Posture Assessment

The overall security posture of these changes is **acceptable with targeted remediation**. The T3 expansion is architecturally justified: adv-executor legitimately needs Context7 for strategy template validation against current framework documentation; explanation writers need WebSearch for design rationale research; orchestration agents need WebFetch for cross-referencing external specifications. These tool grants follow the principle of least privilege at the skill level.

The single high-severity finding (FINDING-001, pm-pmm `Agent` tool) is the most urgent. It is also the simplest to fix: one field deletion in one file.

### Systemic Vulnerability Patterns

**Pattern 1: Governance-frontmatter synchronization lag.** Three of the nine findings stem from governance files (`.governance.yaml` or `<capabilities>` prose sections) that were not updated synchronously with frontmatter tool changes. This suggests the dual-file architecture (H-34) creates a maintenance burden that is not systematically enforced by CI. The CI gate validates schema structure but does not cross-check that `allowed_tools` in governance.yaml matches `tools` in frontmatter. A dedicated CI check for this would close the gap.

**Pattern 2: T3 citation guardrail adoption gap.** Four agents upgraded to T3 in this batch lack `all_claims_must_have_citations` in their governance output_filtering. The rule is stated in agent-development-standards.md but is not mechanically enforced by CI. This is a MEDIUM finding pattern, not an architectural flaw -- but it recurred four times in one PR, suggesting the checklist for "T3 upgrade" tasks does not include this step.

**Pattern 3: Deprecated alias perpetuation.** New code written in this PR introduces `disallowedTools: Task` rather than `disallowedTools: Agent`. The CI check enforces `Task`, creating a feedback loop that makes `Agent` feel wrong. A migration plan (updating CI check + all affected agents atomically) would resolve this permanently.

### Comparison with Threat Model Predictions

These changes expand the external attack surface of the framework in a controlled way. The primary threat introduced by T3 upgrades is information injection: an agent uses WebSearch to retrieve content that is adversarially crafted or simply wrong and then inserts it into a trusted output (a strategy report, an orchestration plan, an explanation document). The citation guardrail requirement in T3 agents directly mitigates this threat by making provenance visible. FINDING-002 and FINDING-003 are gaps in this mitigation layer.

No credential exposure paths were identified. No path traversal risks were introduced -- the `diataxis-explanation` agent explicitly rejects `../` in output paths (a positive control). No new SQL injection or OS command injection surfaces exist (the framework does not have these attack surfaces).

### Recommendations for Security Architecture Evolution

1. **Add a CI check:** Verify that agents with `tool_tier: T3` in governance.yaml have `all_claims_must_have_citations` in `output_filtering`. This would have caught FINDING-002 and FINDING-003 mechanically.

2. **Add a CI cross-check:** Verify `allowed_tools` in governance.yaml matches `tools` in `.md` frontmatter. Catches FINDING-006 (tier-tool mismatch).

3. **Create a "T3 upgrade checklist":** When upgrading an agent from T2 to T3, the task should explicitly include: (a) add citation guardrail to governance.yaml output_filtering, (b) update `<capabilities>` prose in .md body, (c) verify `allowed_tools` in governance.yaml matches new frontmatter, (d) update any self-check tool lists in the agent body.

4. **Migrate `disallowedTools` from `Task` to `Agent` as a single coordinated operation.** Update `skills/user-experience/rules/ci-checks.md` to accept both, then migrate all 6 agents, then tighten the CI check to `Agent` only.

---

## ASVS Verification Status

| Chapter | Scope | Status | Notes |
|---------|-------|--------|-------|
| V1 (Architecture, Design) | Trust boundary documentation, least privilege, component isolation | PARTIAL PASS | FINDING-001 (pm-pmm Agent tool), FINDING-006 (tier-tool mismatch) violate V1 controls |
| V2 (Authentication) | N/A | NOT APPLICABLE | No authentication mechanisms in scope |
| V3 (Session Management) | N/A | NOT APPLICABLE | No session state in reviewed files |
| V4 (Access Control) | Authorization checks at every agent boundary, worker agent tool restrictions | PARTIAL PASS | FINDING-001 is a V4 finding; H-35 enforcement otherwise satisfactory |
| V5 (Validation, Sanitization) | Input validation in guardrails, output filtering | PASS with gaps | Citation guardrail gaps (FINDING-002, FINDING-003); diataxis path traversal control is positive |
| V6 (Cryptography) | N/A | NOT APPLICABLE | No cryptographic operations in scope |
| V7 (Error Handling and Logging) | Fallback behavior declarations, blocker propagation | PASS | All reviewed agents declare fallback behaviors |
| V8 (Data Protection) | Secrets exclusion from output, PII handling | PASS | All agents declare `no_secrets_in_output` |
| V9 (Communication) | External data source handling (WebSearch/WebFetch) | PARTIAL PASS | Citation guardrail gaps affect communication security (provenance of external data) |

---

## Review Scope and Methodology

### Files Reviewed

| File | Change Type | Review Depth |
|------|-------------|--------------|
| `skills/adversary/agents/adv-executor.md` | T2 to T3 (tools + mcpServers added) | Full read |
| `skills/adversary/agents/adv-executor.governance.yaml` | T3 + citation guardrail | Full read |
| `skills/adversary/SKILL.md` | allowed-tools expanded | Full read |
| `skills/adversary/composition/adv-executor.agent.yaml` | Canonical agent updated | Full read |
| `skills/nasa-se/agents/nse-reporter.md` | WebSearch added | Full read |
| `skills/nasa-se/agents/nse-reporter.governance.yaml` | Pre-existing (T3 context) | Full read |
| `skills/diataxis/agents/diataxis-explanation.md` | WebSearch/WebFetch/Context7 added | Full read |
| `skills/diataxis/agents/diataxis-explanation.governance.yaml` | T2 to T3 | Full read |
| `skills/ux-behavior-design/agents/ux-behavior-diagnostician.governance.yaml` | T2 to T3 | Full read |
| `skills/orchestration/agents/orch-planner.md` | WebSearch/WebFetch added | Full read |
| `skills/orchestration/agents/orch-synthesizer.md` | WebSearch/WebFetch added | Full read |
| `skills/orchestration/agents/orch-tracker.md` | WebSearch/WebFetch added | Full read |
| `skills/pm-pmm/SKILL.md` | allowed-tools field added | Full read |
| `skills/ux-heart-metrics/agents/ux-heart-analyst.md` | T2 to T3 (tools added) | Full read |
| `skills/ux-heart-metrics/agents/ux-heart-analyst.governance.yaml` | T2 to T3 | Full read |
| `skills/ux-kano-model/agents/ux-kano-analyst.md` | T2 to T3 (tools added) | Full read |
| `skills/ux-kano-model/agents/ux-kano-analyst.governance.yaml` | T2 to T3 | Full read |

### Focus Areas Addressed

1. **Tier-tool consistency:** governance.yaml `tool_tier` vs. frontmatter `tools` vs. `allowed_tools` list -- FINDINGS-002, FINDING-006
2. **Citation guardrails on T3 agents:** All T3 agents checked for `all_claims_must_have_citations` -- FINDING-002, FINDING-003
3. **adv-executor expanded attack surface documentation:** Self-check currency, capability documentation -- FINDING-004, FINDING-005, FINDING-009
4. **Principle of least privilege:** Verified no unnecessary tools added, identified `Agent` overclaim -- FINDING-001
5. **H-35 compliance (no Agent tool in workers):** All worker frontmatters verified, `disallowedTools` reviewed -- FINDING-007
6. **`disallowedTools: Task` vs `Agent` question:** Surveyed all UX agents, found systemic pattern -- FINDING-007

### Data Flow Traces Performed

- **adv-executor T3 expansion:** Traced WebSearch/WebFetch/Context7 from frontmatter through `<p003_self_check>` and governance.yaml `allowed_tools`. Found self-check stale.
- **nse-reporter WebSearch addition:** Traced external data access through `<guardrails>` and governance.yaml `output_filtering`. Found missing citation guardrail.
- **orch-planner/synthesizer/tracker WebSearch addition:** Traced external data access through `<guardrails>` prose sections. Found no citation guardrail, no governance.yaml.
- **pm-pmm `Agent` tool:** Traced from SKILL.md `allowed-tools` field through P-003 compliance section and individual worker frontmatters. Found contradiction.
- **diataxis-explanation Context7 addition:** Traced from frontmatter `mcpServers: context7: true` through `<capabilities>` prose section and governance.yaml. Found capabilities section stale.
- **ux-behavior-diagnostician T3 tier:** Cross-referenced governance.yaml `tool_tier: T3` against `allowed_tools` list and `.md` frontmatter tools. Found tier-tool mismatch.

### CWE Top 25 2025 Checks Performed

| CWE | Check | Result |
|-----|-------|--------|
| CWE-862 (Missing Authorization) | Worker agents checked for `Agent` tool access | FINDING-001 identified |
| CWE-284 (Improper Access Control) | T3 tier declarations cross-checked against tool grants | FINDINGS-002, -003, -006 identified |
| CWE-693 (Protection Mechanism Failure) | Self-check and capability documentation currency | FINDINGS-004, -005 identified |
| CWE-798 (Hardcoded Credentials) | All files scanned for API keys, tokens, secrets | None found |
| CWE-22 (Path Traversal) | Input validation for file path parameters | Positive control found in diataxis-explanation (`../` rejection) |
| CWE-79 (XSS) | N/A -- framework agents do not render HTML output | Not applicable |
| CWE-89 (SQL Injection) | N/A -- no database interactions | Not applicable |

---

*Review completed: 2026-03-28*
*Reviewer: eng-security (Security Code Review Specialist)*
*Methodology: Manual code review, data flow tracing, ASVS V1/V4/V5/V8/V9 verification, CWE Top 25 2025 checklist*
*SSDF Practice: PW.7 (Review and analyze human-readable code to identify vulnerabilities)*
*Confidence: High (L0/L1 findings) | Medium (L2 systemic patterns -- limited to reviewed files; broader codebase not in scope)*
