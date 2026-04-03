# Wave 2 DX Review: STORY-011 + STORY-013 Tool Access Changes

> **Reviewed:** 2026-03-28
> **Reviewer:** ps-reviewer (convergent)
> **Scope:** Developer experience assessment of tool access expansions across multiple agents

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Verdict Summary](#verdict-summary) | Pass/fail per review question |
| [Finding: Stale Tool List in P-003 Self-Check](#finding-stale-tool-list-in-p-003-self-check) | adv-executor body contradicts frontmatter |
| [Finding: Stale Capabilities Disclaimer in ux-heart-analyst](#finding-stale-capabilities-disclaimer-in-ux-heart-analyst) | Body says T2, frontmatter is T3 |
| [Finding: adv-executor governance YAML missing allowed_tools sync note](#finding-adv-executor-governance-yaml-missing-allowed_tools-sync-note) | Minor discoverability gap |
| [Finding: pm-pmm allowed-tools format deviation](#finding-pm-pmm-allowed-tools-format-deviation) | Inconsistency with skill-standards.md YAML array convention |
| [Finding: disallowedTools: Task vs Agent — stale alias throughout UX sub-skills](#finding-disallowedtools-task-vs-agent--stale-alias-throughout-ux-sub-skills) | Clarity issue post STORY-007 rename |
| [Finding: orch-planner governance YAML not updated to T5](#finding-orch-planner-governance-yaml-not-updated-to-t5) | Tier in YAML does not match effective capabilities |
| [Positive Observations](#positive-observations) | What was done well |
| [Metrics Summary](#metrics-summary) | Aggregate counts |
| [Recommendations](#recommendations) | Prioritized action list |

---

## Verdict Summary

| Review Question | Verdict | Notes |
|-----------------|---------|-------|
| 1. Frontmatter changes formatted consistently with other agents in same skill? | PASS with concerns | adv-executor and orch-planner frontmatter are clean; ux-heart-analyst uses YAML array format for `tools` which is internally consistent with itself but differs from the inline-comma format used in orch-planner and adv-executor |
| 2. `allowed-tools` format in pm-pmm SKILL.md consistent with other SKILL.md files? | FAIL | pm-pmm uses inline comma-separated `allowed-tools`; skill-standards.md examples show this is acceptable but the value includes `Agent` which contradicts P-003 docs in the same file |
| 3. Governance YAML changes follow same patterns as other T3 agents? | PASS with concerns | adv-executor governance YAML follows T3 pattern correctly; orch-planner governance YAML declares T4 but frontmatter now reflects T4+web capabilities |
| 4. Would a developer reading these files understand why web access was added? | FAIL | adv-executor body still says allowed tools are "Read, Write, Edit, Glob, Grep" at line 338; no rationale comment added for the T3 upgrade in either frontmatter or governance YAML |
| 5. `disallowedTools: Task` vs `disallowedTools: Agent` — confusing after STORY-007 rename? | FAIL | All 6+ UX worker agents use `disallowedTools: Task` including the CI check script. STORY-007 renamed Task to Agent in allowed-tools lists but did not update disallowedTools declarations |

---

## Finding: Stale Tool List in P-003 Self-Check

| Attribute | Value |
|-----------|-------|
| **Severity** | HIGH |
| **Location** | `skills/adversary/agents/adv-executor.md:338` |
| **Category** | Correctness / Documentation Accuracy |

**Description:** The P-003 Runtime Self-Check section of adv-executor.md explicitly lists the agent's allowed tools as "Read, Write, Edit, Glob, Grep" — the pre-STORY-013 T2 set. The frontmatter at line 5 now declares `tools: Read, Write, Edit, Glob, Grep, WebSearch, WebFetch`. These two statements directly contradict each other. A developer reading the body text would conclude the agent cannot use web search, while the frontmatter enables it at runtime.

**Evidence:**
```
Line 5:   tools: Read, Write, Edit, Glob, Grep, WebSearch, WebFetch
Line 338: 3. **Direct tool use only** — This agent may ONLY use: Read, Write, Edit, Glob, Grep
```

**Recommendation:** Update line 338 to match the frontmatter:
```
3. **Direct tool use only** — This agent may ONLY use: Read, Write, Edit, Glob, Grep, WebSearch, WebFetch, mcp__context7__resolve-library-id, mcp__context7__query-docs
```
Also add a brief inline comment in the P-003 self-check noting why web access is granted (e.g., "Context7 enables current library docs for strategy template research").

**References:** P-022 (No Deception), P-001 (Truth/Accuracy)

---

## Finding: Stale Capabilities Disclaimer in ux-heart-analyst

| Attribute | Value |
|-----------|-------|
| **Severity** | HIGH |
| **Location** | `skills/ux-heart-metrics/agents/ux-heart-analyst.md:100-101` |
| **Category** | Correctness / Documentation Accuracy |

**Description:** The `<capabilities>` section explicitly declares "WebSearch / WebFetch -- this is a T2 agent. The HEART methodology is self-contained in the agent definition; no external web research is required." However, STORY-013 added `WebSearch` and `WebFetch` to the frontmatter `tools` array (lines 17-18), making the agent T3 in capability. The body text now actively contradicts the runtime configuration and gives a developer an incorrect mental model of what the agent can do.

**Evidence:**
```yaml
# Frontmatter (lines 14-20):
tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - WebSearch    # Added by STORY-013
  - WebFetch     # Added by STORY-013
```
```markdown
# Body (lines 100-101):
- WebSearch / WebFetch -- this is a T2 agent. The HEART methodology is self-contained
  in the agent definition; no external web research is required.
```

**Recommendation:** Update the `<capabilities>` section to reflect T3 status and document the reason for web access. Example replacement:
```markdown
- WebSearch / WebFetch -- available for HEART benchmark research (industry studies,
  published UX metric benchmarks). Use when no prior artifact provides baseline data.
  Context7 available for framework documentation lookup.
```
Also update the governance YAML `tool_tier` field if a `.governance.yaml` exists for this agent (not found in the spot-check, suggesting one may not exist yet).

**References:** P-022 (No Deception), agent-development-standards.md AD-M-005

---

## Finding: adv-executor governance YAML missing allowed_tools sync note

| Attribute | Value |
|-----------|-------|
| **Severity** | MEDIUM |
| **Location** | `skills/adversary/agents/adv-executor.governance.yaml:42-50` |
| **Category** | Discoverability |

**Description:** The `capabilities.allowed_tools` list in adv-executor.governance.yaml correctly includes WebSearch, WebFetch, and the two Context7 MCP tools (consistent with the frontmatter). However, there is no comment or rationale explaining why a strategy executor — an agent whose primary job is following pre-loaded templates — needs external web access. Comparing with adv-scorer.governance.yaml (T2, no web access), a developer maintaining the adversary skill would reasonably ask "why does adv-executor need web access but adv-scorer does not?" without finding an answer.

**Evidence:** The governance YAML at line 41-57 lists the tools without any inline explanation. The adv-scorer.governance.yaml for comparison has no web tools and makes the contrast visible.

**Recommendation:** Add a comment block above the `allowed_tools` list:
```yaml
capabilities:
  # T3: WebSearch/WebFetch and Context7 added (STORY-013) to support
  # strategy execution against deliverables that reference external libraries
  # or frameworks. adv-scorer (T2) does not need web access.
  allowed_tools:
  - Read
  ...
```

**References:** agent-development-standards.md AD-M-010 (MCP tool declaration guidance)

---

## Finding: pm-pmm allowed-tools format deviation

| Attribute | Value |
|-----------|-------|
| **Severity** | MEDIUM |
| **Location** | `skills/pm-pmm/SKILL.md:5` |
| **Category** | Consistency |

**Description:** The pm-pmm SKILL.md uses the inline comma-separated format for `allowed-tools`:
```
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Agent, WebSearch, WebFetch
```
The value includes `Agent` (the T5 orchestration tool). The P-003 compliance section at line 213 explicitly states "Agents do NOT have the Task tool" — but does not mention that SKILL.md-level `allowed-tools` is distinct from per-agent frontmatter `tools`. This creates a discoverability risk: a developer reading the SKILL.md header might conclude that worker agents have Agent/Task access, contradicting the P-003 diagram two sections later.

The confusion is compounded because `allowed-tools` in SKILL.md is a Jerry-specific routing field (not a Claude Code runtime field), while `tools` in agent `.md` frontmatter is a Claude Code runtime enforcement field. These fields have different semantics that are not surfaced anywhere in the SKILL.md.

**Recommendation:** Either:
(a) Add an inline comment after `allowed-tools` clarifying this is the SKILL-level routing field, not per-agent enforcement:
```yaml
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Agent, WebSearch, WebFetch
# ^ SKILL.md routing hint only. Worker agents declare tools individually in agents/*.md
```
Or (b) remove `Agent` from the SKILL.md `allowed-tools` since no worker agent has it, and the orchestrator is the MAIN CONTEXT, not a pm-pmm agent.

**References:** skill-standards.md (SKILL.md frontmatter standards), H-34 (agent definition schema)

---

## Finding: disallowedTools: Task vs Agent — stale alias throughout UX sub-skills

| Attribute | Value |
|-----------|-------|
| **Severity** | MEDIUM |
| **Location** | All 6+ UX sub-skill agent files; `skills/user-experience/rules/ci-checks.md:72-95` |
| **Category** | Consistency / Maintainability |

**Description:** STORY-007 renamed the `Task` tool alias to `Agent` in allowed-tools declarations across the framework. However, `disallowedTools` declarations in all UX sub-skill worker agents still use `Task` (not `Agent`). The CI check script at `skills/user-experience/rules/ci-checks.md:89-91` also still greps for `Task` specifically. The documented rationale in agent-development-standards.md (H-35) reads: "Worker agents MUST NOT include `Agent` (or its backward-compatible alias `Task`) in the official `tools` frontmatter field."

The backward-compatible alias means the runtime behaviour is identical — `disallowedTools: Task` and `disallowedTools: Agent` both work. However, the inconsistency causes cognitive friction:

- Six ux-* agent files declare `disallowedTools: Task`
- The ux-orchestrator's forbidden agent tool is listed as `Task` in its P-003 diagram
- New developers reading agent-development-standards.md will see "Agent" as the canonical name and look for `disallowedTools: Agent` to verify P-003 compliance

Files confirmed using `disallowedTools: Task`:
- `skills/ux-heart-metrics/agents/ux-heart-analyst.md:22`
- `skills/ux-kano-model/agents/ux-kano-analyst.md:27`
- `skills/ux-design-sprint/agents/ux-sprint-facilitator.md:27`
- `skills/ux-behavior-design/agents/ux-behavior-diagnostician.md:24`
- `skills/ux-jtbd/agents/ux-jtbd-analyst.md:19`
- `skills/ux-heuristic-eval/agents/ux-heuristic-evaluator.md:20`
- `skills/ux-lean-ux/agents/ux-lean-ux-facilitator.md:21`
- `skills/ux-inclusive-design/agents/ux-inclusive-evaluator.md:26`
- `skills/ux-atomic-design/agents/ux-atomic-architect.md:23`
- `skills/ux-ai-first-design/agents/ux-ai-design-guide.md:27`

**Recommendation:** Update all `disallowedTools: - Task` declarations to `disallowedTools: - Agent` for consistency with the canonical name in agent-development-standards.md. Update the CI check script grep pattern from `Task` to `Agent` (or `Agent|Task` as a transitional expression). Document this as a clean-up story so it is tracked. This is a low-risk change because the alias behaviour is identical at runtime.

**References:** agent-development-standards.md H-35 (retired as H-34 sub-item), H-34

---

## Finding: orch-planner governance YAML not updated to T5

| Attribute | Value |
|-----------|-------|
| **Severity** | LOW |
| **Location** | `skills/orchestration/agents/orch-planner.governance.yaml:6` |
| **Category** | Consistency |

**Description:** The `orch-planner.governance.yaml` declares `tool_tier: T4`. However, the `orch-planner.md` frontmatter now declares `tools: Read, Write, Edit, Glob, Grep, Bash, WebSearch, WebFetch` with `mcpServers: memory-keeper: true`. Per agent-development-standards.md Tool Security Tiers, T4 is "T2 + Memory-Keeper" and T3 is "T2 + WebSearch, WebFetch, Context7". The current orch-planner has both Persistent (T4) and External (T3) capabilities, which would classify it as a hybrid that arguably should be described as T4+web or noted as an exception. The inconsistency is low-risk because the governance YAML tier is metadata, not runtime enforcement, but it will cause confusion when the schema validator runs a tier consistency check.

Note: if WebSearch/WebFetch were already present in orch-planner before STORY-013 (and only memory-keeper was the T4 elevator), then the YAML tier may have always been an approximation. Verification of the full STORY-011/013 diff would clarify whether this is a pre-existing condition or a STORY-013 regression.

**Evidence:** `orch-planner.governance.yaml:6` states `tool_tier: T4`. The frontmatter includes both Memory-Keeper (T4 marker) and WebSearch/WebFetch (T3 marker).

**Recommendation:** Update `tool_tier` in the governance YAML to whichever tier best describes the highest capability enabled. Per the tiering model, T4 already includes T2 tools, but T3 (external) is an independent branch. Add a comment noting the combined tier rationale:
```yaml
tool_tier: T4  # T4 (Memory-Keeper) + external access (T3). Combined: T4 with web.
```
Or create a clear precedent in the tier table for agents with both T3 and T4 capabilities.

**References:** agent-development-standards.md Tool Security Tiers

---

## Positive Observations

| # | Observation |
|---|-------------|
| 1 | adv-executor frontmatter is clean and minimal — exactly the right fields, no non-standard YAML keys. The mcpServers block is well-formed. |
| 2 | adv-executor.governance.yaml correctly declares Context7 MCP tool names in `allowed_tools` using the canonical identifiers from mcp-tool-standards.md. No other governance YAML in the spot-check was this precise. |
| 3 | ux-heart-analyst uses YAML array format for `tools` instead of inline comma string — this is the preferred format per the Claude Code official field spec and provides better diff readability. |
| 4 | pm-pmm SKILL.md has an unusually thorough P-003 compliance section including ASCII diagram and explicit "Agents do NOT have the Task tool" statement. The intent is clearly correct even if the SKILL.md `allowed-tools` field creates ambiguity. |
| 5 | The `disallowedTools` pattern for UX workers is architecturally correct and uniformly applied across 10 agents — the consistency across the skill is commendable even if the value needs updating from `Task` to `Agent`. |
| 6 | orch-planner.md frontmatter is clean. The WebSearch/WebFetch tools are clearly declared. The mcpServers block uses the simple `memory-keeper: true` form consistently with other orchestration agents. |

---

## Metrics Summary

| Metric | Value |
|--------|-------|
| Files Reviewed | 5 agent/SKILL files + 2 governance YAMLs + 1 CI check script |
| Critical Issues | 0 |
| High Issues | 2 |
| Medium Issues | 3 |
| Low Issues | 1 |
| Positive Observations | 6 |
| Overall Assessment | PASS_WITH_CONCERNS |

---

## Recommendations

Ordered by priority:

| Priority | Action | Effort | Risk |
|----------|--------|--------|------|
| 1 | Update `adv-executor.md:338` P-003 self-check tool list to match frontmatter | 5 min | Zero |
| 2 | Update `ux-heart-analyst.md` `<capabilities>` section to reflect T3 status and document web access rationale | 15 min | Zero |
| 3 | Update all 10 UX sub-skill agents: `disallowedTools: - Task` -> `disallowedTools: - Agent`; update CI check grep pattern | 30 min | Zero (backward-compatible alias) |
| 4 | Clarify pm-pmm SKILL.md `allowed-tools: Agent` — either add comment distinguishing SKILL routing from per-agent enforcement, or remove `Agent` from the list | 10 min | Low |
| 5 | Add rationale comment to `adv-executor.governance.yaml` explaining why T3 vs T2 (adv-scorer comparison) | 5 min | Zero |
| 6 | Resolve orch-planner `tool_tier: T4` vs effective T3+T4 capabilities — update governance YAML with comment or create tier precedent | 10 min | Low |

Items 1 and 2 are the most DX-impacting because they create directly contradictory statements within the same file — a developer relying on the body text to understand an agent's capabilities will receive incorrect information.
