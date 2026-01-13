# Synthesis: PROJ-003 Agent and Skill Cleanup

| Metadata | Value |
|----------|-------|
| **Document ID** | proj-003-e-006 |
| **PS ID** | proj-003 |
| **Entry Type** | Synthesis |
| **Topic** | Research and Analysis Synthesis |
| **Date** | 2026-01-12 |
| **Author** | ps-synthesizer (v2.0.0) |
| **Status** | Complete |
| **Sources** | proj-003-e-001 through proj-003-e-005 |

---

## Executive Summary

This synthesis integrates findings from five research and analysis documents to provide a unified view of the Jerry Framework agent/skill cleanup project. The analysis identified **23 gaps** between Jerry's current state and industry best practices, with **6 high-severity** issues requiring immediate attention.

**Key Synthesis Findings:**

1. **Plugin Structure Non-Compliance**: The most critical issue is that Jerry's plugin manifest uses non-standard schema and filename (`manifest.json` vs `plugin.json`), and commands are nested in `.claude/commands/` instead of plugin root `commands/`. This breaks standard plugin discovery.

2. **SKILL.md Frontmatter Missing**: Three of four skills lack required YAML frontmatter, preventing Claude from auto-invoking them. Only `problem-solving` has partial compliance.

3. **Agent Organization is Correct**: The hybrid pattern (general agents in `.claude/agents/`, skill agents in `skills/{skill}/agents/`) aligns with industry best practices. No reorganization needed.

4. **Agent Definitions Need Standardization**: General-purpose agents lack YAML frontmatter with model/tool specifications, while ps-* agents follow a more complete template. Standardization is needed.

5. **Hook System is Incomplete**: Only `SessionStart` hook is implemented. `PreToolUse` validation hooks are essential for security and quality gates.

6. **AGENTS.md Registry Incomplete**: The registry lists only 3 framework agents, missing all 8 ps-* agents from the problem-solving skill.

**Recommended Priority Sequence:**
1. Fix plugin manifest (blocks distribution)
2. Add SKILL.md frontmatter (blocks auto-invocation)
3. Move commands to plugin root (blocks command discovery)
4. Standardize agent frontmatter (improves tool enforcement)
5. Complete hook system (improves quality assurance)
6. Update AGENTS.md registry (improves discoverability)

---

## Knowledge Integration

### From Research: Claude Code Best Practices (e-001)

**Key Takeaways:**

| Finding | Impact on Cleanup | Priority |
|---------|------------------|----------|
| Plugin components MUST be at plugin root, not inside `.claude-plugin/` | Commands in wrong location | High |
| Only `plugin.json` belongs in `.claude-plugin/` | Manifest filename incorrect | High |
| SKILL.md requires YAML frontmatter with specific trigger phrases | 3 skills non-compliant | High |
| Agent definitions need `name`, `description`, `model`, `tools` frontmatter | 3 agents non-compliant | Medium |
| Hook events include PreToolUse, PostToolUse, SessionStart, Stop | Incomplete coverage | Medium |
| Use `${CLAUDE_PLUGIN_ROOT}` for portable path references | Hook paths need update | Medium |

**Canonical Directory Structure (e-001 L39-57):**
```
plugin-name/
├── .claude-plugin/
│   └── plugin.json          # ONLY this file inside .claude-plugin/
├── commands/                 # At plugin root, NOT inside .claude/
├── agents/                   # OR .claude/agents/ both valid
├── skills/
│   └── skill-name/
│       ├── SKILL.md
│       ├── scripts/
│       └── references/
├── hooks/
│   └── hooks.json
└── README.md
```

**SKILL.md Schema (e-001 L104-124):**
```yaml
---
name: skill-name
description: This skill should be used when the user asks to "trigger phrase 1",
  "trigger phrase 2". Include exact trigger phrases.
version: 1.0.0
allowed-tools:
  - Read
  - Write
  - Bash
---
```

**Agent Definition Schema (e-001 L129-153):**
```yaml
---
name: agent-name
description: Use this agent when the user asks to "perform X", "analyze Y".
  <example>User: "Review this code for security issues"</example>
  <example>User: "Help me architect this feature"</example>
model: claude-opus-4-5
color: purple
tools:
  - Read
  - Write
  - Edit
---
```

### From Research: Plugins Prior Art (e-002)

**Key Takeaways:**

| Finding | Impact on Cleanup | Priority |
|---------|------------------|----------|
| Plugin ecosystem converged on canonical structure by Dec 2025 | Jerry needs alignment | High |
| Skills use progressive disclosure (metadata first, content on-demand) | Frontmatter essential | High |
| Orchestrator-worker pattern (Opus 4 + Sonnet 4) shows 90.2% improvement | Already adopted | N/A |
| Hook lifecycle covers 8 events; PreToolUse can block operations | Security enhancement | Medium |
| `.github/skills/` is recommended but `skills/` is acceptable | Optional migration | Low |

**Deprecated Patterns (e-002 L206-216):**

| Deprecated | Replacement | Jerry Status |
|------------|-------------|--------------|
| `.claude.json` | `.claude/settings.json` | Compliant |
| `allowedTools` setting | Permission rules | Compliant |
| `@anthropic-ai/claude-code` SDK | `@anthropic-ai/claude-agent-sdk` | N/A |
| Output styles | Plugins or `--system-prompt-file` | Compliant |

**Hook Decision Control (e-002 L144-148):**
- Exit code 0: Allow operation
- Exit code 2: Deny with error message
- JSON output: `{"decision": "allow|deny|ask", "message": "..."}`

### From Research: Architecture Patterns (e-003)

**Key Takeaways:**

| Finding | Impact on Cleanup | Priority |
|---------|------------------|----------|
| Industry favors hybrid agent organization (central orchestration + skill-local specialists) | Jerry already compliant | N/A |
| AGENTS.md convention used by 60,000+ projects | Registry needs expansion | Medium |
| Token economics: multi-agent = ~15x single agent tokens | Reserve for high-value tasks | Info |
| Agent registry should index all agents with metadata | Missing ps-* agents | Medium |
| Single-level agent nesting (orchestrator -> worker) | Already enforced (P-003) | N/A |

**Recommended Architecture (e-003 L347-388):**
```
.claude/
├── agents/
│   ├── REGISTRY.md          # Central agent index
│   ├── orchestrator.md      # Framework orchestrator
│   ├── qa-engineer.md       # Cross-cutting QA
│   └── security-auditor.md  # Cross-cutting security

skills/
├── problem-solving/
│   ├── SKILL.md
│   └── agents/              # Skill-local specialists
│       ├── ps-researcher.md
│       ├── ps-analyst.md
│       └── ...
```

**Decision Matrix (e-003 L428-436):**

| Criterion | Hybrid (Current) | Centralized | Distributed |
|-----------|------------------|-------------|-------------|
| Industry alignment | **High** | Medium | Medium |
| Skill encapsulation | **High** | Low | High |
| Discoverability | High (with registry) | High | Low |
| **Recommendation** | **Preferred** | Acceptable | Not recommended |

### From Analysis: PROJ-001 Knowledge (e-004)

**Key Takeaways:**

| Finding | Impact on Cleanup | Priority |
|---------|------------------|----------|
| Agents live in TWO places (by design): `.claude/agents/` and `skills/{skill}/agents/` | No reorganization needed | Info |
| PS_AGENT_TEMPLATE.md is the canonical template with YAML + XML structure | Use as reference | Medium |
| Worktracker skills lack agents (never created, not lost) | Out of scope for cleanup | N/A |
| Constitutional compliance mandatory: P-002 (persistence), P-003 (single-level), P-022 (no deception) | Verify in agents | Medium |
| One file per concept (ADR-003) | Already followed | N/A |

**Cleanup Scope Clarification (e-004 L218-233):**

**IN SCOPE:**
- Verify `.claude/agents/` contains only general-purpose agents
- Verify `skills/problem-solving/agents/` contains ps-* agents
- Check for duplicate agent definitions between locations
- Ensure agent files follow canonical template structure
- Validate AGENTS.md registry is accurate and complete

**OUT OF SCOPE:**
- Creating missing worktracker agents (greenfield work, not cleanup)
- Restructuring CLAUDE.md (separate initiative)
- Adding path scoping to rules (separate initiative)
- Creating PLAYBOOK.md for worktracker skills (enhancement)

**Constitutional Compliance (e-004 L93-103):**

| Principle | Enforcement | Cleanup Check |
|-----------|-------------|---------------|
| P-001 (Truth/Accuracy) | Soft | Documentation accuracy |
| P-002 (File Persistence) | Medium | Output persistence defined |
| P-003 (No Recursion) | **Hard** | Task tool restrictions |
| P-020 (User Authority) | **Hard** | ADR approval status |
| P-022 (No Deception) | **Hard** | Transparent limitations |

### From Analysis: Gap Analysis (e-005)

**Key Takeaways:**

| Metric | Value |
|--------|-------|
| Total Gaps Identified | 23 |
| High Severity | 6 |
| Medium Severity | 10 |
| Low Severity | 7 |

**Gap Summary by Category:**

| Category | Gap Count | High Severity Issues |
|----------|-----------|---------------------|
| Directory Structure | 5 | GAP-001 (commands), GAP-002 (manifest) |
| SKILL.md Compliance | 5 | GAP-006/007/008 (frontmatter) |
| Agent Definitions | 5 | None (all Medium) |
| Hook System | 5 | None (all Medium/Low) |
| AGENTS.md Registry | 3 | None (all Medium/Low) |

**Immediate Action Items (e-005 L324-332):**
1. Rename `manifest.json` to `plugin.json`
2. Update schema URL to Anthropic standard
3. Convert manifest fields to standard format
4. Move commands from `.claude/commands/` to `commands/`
5. Add YAML frontmatter to all SKILL.md files

---

## Extracted Patterns

### Directory Structure Pattern

**Standard Plugin Structure for Jerry:**

```
jerry/                                 # Plugin root
├── .claude-plugin/
│   └── plugin.json                   # ONLY this file (rename from manifest.json)
│
├── commands/                          # MOVE from .claude/commands/
│   ├── architect.md
│   └── release.md
│
├── .claude/
│   ├── agents/                       # Framework-level agents (keep)
│   │   ├── orchestrator.md
│   │   ├── qa-engineer.md
│   │   ├── security-auditor.md
│   │   └── TEMPLATE.md
│   ├── rules/                        # Configuration rules (keep)
│   └── patterns/                     # Pattern catalog (keep)
│
├── skills/                            # Skill definitions (keep)
│   ├── problem-solving/
│   │   ├── SKILL.md                  # Has frontmatter (partial)
│   │   └── agents/                   # Skill-specific agents (keep)
│   │       ├── ps-researcher.md
│   │       └── ... (8 total)
│   ├── worktracker/
│   │   └── SKILL.md                  # NEEDS frontmatter
│   ├── worktracker-decomposition/
│   │   └── SKILL.md                  # NEEDS frontmatter
│   └── architecture/
│       └── SKILL.md                  # NEEDS frontmatter
│
├── hooks/
│   └── hooks.json                    # Consolidate all hooks here
│
├── scripts/                          # Helper scripts (keep)
│
├── AGENTS.md                         # Expand to include ps-* agents
└── CLAUDE.md
```

### SKILL.md Authoring Pattern

**Required YAML Frontmatter:**

```yaml
---
name: skill-name                       # Required: kebab-case identifier
description: This skill should be used when the user asks to "trigger phrase 1",
  "trigger phrase 2", "trigger phrase 3". Be specific about trigger phrases.
version: 1.0.0                         # Required: semver
allowed-tools:                         # Optional: restrict Claude's tools
  - Read
  - Write
  - Edit
  - Bash
context: fork                          # Optional: run in subagent context
agent: specialist                      # Optional: specify agent type
---

# Skill Title

[Main content Claude follows when skill is active]

## Overview
Brief description of skill capabilities.

## Workflow
1. Step one
2. Step two

## Examples
- Example usage scenario 1
- Example usage scenario 2

## Guidelines
- Best practice 1
- Best practice 2
```

**Description Best Practice:**
- Use third-person format: "This skill should be used when..."
- Include **specific trigger phrases** in quotes
- Avoid vague descriptions like "Use for task management"
- Example: `"create work item", "track task", "list tasks", "update work status"`

### Agent Definition Pattern

**Required YAML Frontmatter:**

```yaml
---
name: agent-name                       # Required: kebab-case identifier
description: Use this agent when the user asks to "perform X", "analyze Y".
  <example>User: "Review this code for security issues"</example>
  <example>User: "Help me architect this feature"</example>
model: claude-opus-4-5                 # Optional: default inherits from parent
color: purple                          # Optional: visual distinction
tools:                                 # Required: principle of least privilege
  - Read
  - Grep
  - Glob
  - Write
  - Edit
  - Task
---

# Agent Title

You are a specialized agent for [domain]. Your responsibilities include:
1. [Specific task]
2. [Specific task]

## Methodology
[How this agent approaches problems]

## Output Format
[Expected output structure]

## Constraints
[Limitations and guardrails]
```

**Best Practices:**
- Include 2-4 concrete `<example>` blocks in description
- Use `model: inherit` unless specific model needed
- Apply principle of least privilege for tools
- Use different colors for multiple agents
- Include constitutional compliance section for ps-* agents

### Hook Configuration Pattern

**Standard hooks/hooks.json:**

```json
{
  "hooks": {
    "SessionStart": [
      {
        "matcher": "*",
        "hooks": [
          {
            "type": "command",
            "command": "python3 ${CLAUDE_PLUGIN_ROOT}/scripts/session_start.py",
            "timeout": 10000
          }
        ]
      }
    ],
    "PreToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "python3 ${CLAUDE_PLUGIN_ROOT}/scripts/pre_tool_use.py",
            "timeout": 5000
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Edit",
        "hooks": [
          {
            "type": "prompt",
            "prompt": "Verify edit maintains architectural constraints from .claude/rules/"
          }
        ]
      }
    ],
    "Stop": [
      {
        "matcher": "*",
        "hooks": [
          {
            "type": "prompt",
            "prompt": "Verify task completion: Work Tracker updated if applicable, tests run if code changed"
          }
        ]
      }
    ]
  }
}
```

**Key Patterns:**
- Use `${CLAUDE_PLUGIN_ROOT}` for portable paths (not `.claude/hooks/`)
- `matcher` uses regex patterns for tool filtering
- `timeout` in milliseconds (default: 60000)
- Hook types: `command` (script) or `prompt` (LLM evaluation)
- Decision control via exit codes (0=allow, 2=deny)

---

## Decision Matrix

### Agent Disposition

| Agent | Current Location | Action | Target Location | Rationale |
|-------|------------------|--------|-----------------|-----------|
| orchestrator | `.claude/agents/orchestrator.md` | **Update** | Same | Add YAML frontmatter |
| qa-engineer | `.claude/agents/qa-engineer.md` | **Update** | Same | Add YAML frontmatter |
| security-auditor | `.claude/agents/security-auditor.md` | **Update** | Same | Add YAML frontmatter |
| TEMPLATE | `.claude/agents/TEMPLATE.md` | **Update** | Same | Align with PS_AGENT_TEMPLATE |
| ps-researcher | `skills/problem-solving/agents/` | **Keep** | Same | Already compliant |
| ps-analyst | `skills/problem-solving/agents/` | **Keep** | Same | Already compliant |
| ps-synthesizer | `skills/problem-solving/agents/` | **Keep** | Same | Already compliant |
| ps-validator | `skills/problem-solving/agents/` | **Keep** | Same | Already compliant |
| ps-reporter | `skills/problem-solving/agents/` | **Keep** | Same | Already compliant |
| ps-architect | `skills/problem-solving/agents/` | **Keep** | Same | Already compliant |
| ps-reviewer | `skills/problem-solving/agents/` | **Keep** | Same | Already compliant |
| ps-investigator | `skills/problem-solving/agents/` | **Keep** | Same | Already compliant |
| PS_AGENT_TEMPLATE | `skills/problem-solving/agents/` | **Keep** | Same | Reference template |

**Note:** No agent reorganization needed. The hybrid pattern is industry-aligned.

### Skill Disposition

| Skill | Current State | Action | Changes Required |
|-------|---------------|--------|------------------|
| problem-solving | Partial frontmatter | **Update** | Add trigger phrases to description |
| worktracker | No frontmatter | **Update** | Add complete YAML frontmatter |
| worktracker-decomposition | No frontmatter | **Update** | Add complete YAML frontmatter |
| architecture | No frontmatter | **Update** | Add complete YAML frontmatter |

### Command Disposition

| Command | Current Location | Action | Target Location | Rationale |
|---------|------------------|--------|-----------------|-----------|
| architect.md | `.claude/commands/` | **Move** | `commands/` | Plugin standard |
| release.md | `.claude/commands/` | **Move** | `commands/` | Plugin standard |

### Hook Disposition

| Hook | Current Location | Action | Changes Required |
|------|------------------|--------|------------------|
| SessionStart | `hooks/hooks.json` | **Keep** | Update path to use `${CLAUDE_PLUGIN_ROOT}` |
| PreToolUse | Not implemented | **Add** | Create validation for Write/Edit |
| PostToolUse | Not implemented | **Add** (optional) | Consider for architecture enforcement |
| Stop | Not implemented | **Add** (optional) | Consider for task completion verification |
| .claude/hooks/*.py | `.claude/hooks/` | **Move** | `scripts/` directory |

### File Disposition

| File | Current State | Action | Changes Required |
|------|---------------|--------|------------------|
| `.claude-plugin/manifest.json` | Non-standard | **Rename** | To `plugin.json`, update schema |
| `.claude/commands/` | Wrong location | **Remove** | After moving contents to `commands/` |
| `.claude/hooks/` | Non-standard | **Remove** | After moving scripts to `scripts/` |
| `AGENTS.md` | Incomplete | **Update** | Add ps-* agents to registry |

---

## Consolidated Recommendations

### Must-Do (Plugin Compliance - P0)

These gaps block standard plugin discovery and skill auto-invocation.

- [ ] **GAP-002**: Rename `.claude-plugin/manifest.json` to `.claude-plugin/plugin.json`
- [ ] **GAP-002**: Update `$schema` to `https://anthropic.com/claude-code/plugin.schema.json`
- [ ] **GAP-002**: Convert `author` from string to object format
- [ ] **GAP-002**: Convert `commands`, `agents`, `hooks` from object/array to path strings
- [ ] **GAP-001**: Create `commands/` directory at plugin root
- [ ] **GAP-001**: Move `architect.md` from `.claude/commands/` to `commands/`
- [ ] **GAP-001**: Move `release.md` from `.claude/commands/` to `commands/`
- [ ] **GAP-006**: Add YAML frontmatter to `skills/worktracker/SKILL.md`
- [ ] **GAP-007**: Add YAML frontmatter to `skills/architecture/SKILL.md`
- [ ] **GAP-008**: Add YAML frontmatter to `skills/worktracker-decomposition/SKILL.md`

### Should-Do (Best Practice - P1)

These gaps improve consistency, security, and discoverability.

- [ ] **GAP-011**: Add YAML frontmatter to `.claude/agents/orchestrator.md`
- [ ] **GAP-012**: Add YAML frontmatter to `.claude/agents/qa-engineer.md`
- [ ] **GAP-013**: Add YAML frontmatter to `.claude/agents/security-auditor.md`
- [ ] **GAP-015**: Add 2-4 `<example>` blocks to each agent description
- [ ] **GAP-010**: Update skill descriptions with specific trigger phrases
- [ ] **GAP-016/017**: Add PreToolUse hooks for Write/Edit validation
- [ ] **GAP-020**: Update hook paths to use `${CLAUDE_PLUGIN_ROOT}`
- [ ] **GAP-004**: Consolidate all hooks into `hooks/hooks.json`
- [ ] **GAP-004**: Move scripts from `.claude/hooks/` to `scripts/`
- [ ] **GAP-021**: Add ps-* agents to AGENTS.md registry
- [ ] **GAP-022**: Document both agent locations in AGENTS.md

### Could-Do (Improvement - P2)

These gaps are nice-to-have improvements for long-term alignment.

- [ ] **GAP-018**: Add PostToolUse hooks for architecture constraint verification
- [ ] **GAP-019**: Add Stop hooks for task completion verification
- [ ] **GAP-005**: Create `.mcp.json` if MCP integration is needed in future
- [ ] **GAP-003**: Consider migrating skills to `.github/skills/` for cross-platform
- [ ] **GAP-009**: Standardize problem-solving SKILL.md frontmatter keys
- [ ] **GAP-014**: Update TEMPLATE.md to match PS_AGENT_TEMPLATE structure
- [ ] **GAP-023**: Consider YAML-formatted REGISTRY.md for programmatic access

---

## Migration Sequence

Recommended order of changes to minimize disruption:

### Phase 1: Plugin Infrastructure (1-2 hours)

**Rationale:** These changes are foundational and unblock plugin discovery.

1. **Rename manifest to plugin.json**
   - Rename `.claude-plugin/manifest.json` to `.claude-plugin/plugin.json`
   - Update schema URL
   - Convert field formats to standard

2. **Create commands directory**
   - Create `commands/` at plugin root
   - Move `architect.md` and `release.md`
   - Remove empty `.claude/commands/`

3. **Update plugin.json paths**
   - Set `commands: "./commands"`
   - Set `agents: ["./agents", "./.claude/agents"]` (or appropriate path)
   - Set `hooks: "./hooks/hooks.json"`

### Phase 2: Skill Frontmatter (1-2 hours)

**Rationale:** Required for skill auto-invocation.

4. **Add worktracker frontmatter**
   ```yaml
   ---
   name: worktracker
   description: This skill should be used when the user asks to "create work item",
     "track task", "list tasks", "update work status", or mentions work/task management.
   version: 1.0.0
   allowed-tools:
     - Read
     - Write
     - Edit
     - Bash
   ---
   ```

5. **Add architecture frontmatter**
   ```yaml
   ---
   name: architecture
   description: This skill should be used when the user asks to "design system",
     "create ADR", "review architecture", or mentions architectural decisions.
   version: 1.0.0
   allowed-tools:
     - Read
     - Write
     - Grep
     - Glob
   ---
   ```

6. **Add worktracker-decomposition frontmatter**
   ```yaml
   ---
   name: worktracker-decomposition
   description: This skill should be used when the user asks to "decompose task",
     "break down work", "create subtasks", or mentions task breakdown.
   version: 1.0.0
   allowed-tools:
     - Read
     - Write
     - Edit
   ---
   ```

### Phase 3: Agent Standardization (2-3 hours)

**Rationale:** Improves tool enforcement and auto-selection.

7. **Add orchestrator frontmatter**
   ```yaml
   ---
   name: orchestrator
   description: Use this agent when the user asks to "coordinate complex tasks",
     "decompose work", "delegate to specialists".
     <example>User: "Help me implement authentication across multiple files"</example>
     <example>User: "Coordinate a refactoring effort"</example>
   model: claude-opus-4-5
   color: purple
   tools:
     - Read
     - Write
     - Edit
     - Glob
     - Grep
     - Task
   ---
   ```

8. **Add qa-engineer frontmatter**
   ```yaml
   ---
   name: qa-engineer
   description: Use this agent when the user asks to "write tests",
     "review test coverage", "design test strategy".
     <example>User: "Write unit tests for this module"</example>
     <example>User: "Review the test coverage for authentication"</example>
   model: inherit
   color: green
   tools:
     - Read
     - Write
     - Edit
     - Bash
     - Grep
   ---
   ```

9. **Add security-auditor frontmatter**
   ```yaml
   ---
   name: security-auditor
   description: Use this agent when the user asks to "security review",
     "audit vulnerabilities", "check for security issues".
     <example>User: "Review this code for security vulnerabilities"</example>
     <example>User: "Audit the authentication implementation"</example>
   model: inherit
   color: red
   tools:
     - Read
     - Grep
     - Glob
   ---
   ```

### Phase 4: Hook System (1-2 hours)

**Rationale:** Improves quality assurance and security.

10. **Update hooks/hooks.json**
    - Add PreToolUse hooks for Write/Edit
    - Update paths to use `${CLAUDE_PLUGIN_ROOT}`
    - Move scripts from `.claude/hooks/` to `scripts/`

11. **Remove .claude/hooks/**
    - Delete empty directory after migration

### Phase 5: Registry Update (30 min)

**Rationale:** Improves agent discoverability.

12. **Update AGENTS.md**
    - Add Framework Agents section (existing)
    - Add Skill-Specific Agents section (new)
    - List all 8 ps-* agents with paths
    - Document agent scopes (global vs skill-local)

---

## Success Criteria

How to validate the cleanup is complete:

### Plugin Structure Validation

- [ ] `.claude-plugin/plugin.json` exists (not `manifest.json`)
- [ ] `plugin.json` uses `$schema: "https://anthropic.com/claude-code/plugin.schema.json"`
- [ ] `plugin.json` has `author` as object, not string
- [ ] `plugin.json` has `commands`, `agents`, `hooks` as path strings
- [ ] `commands/` directory exists at plugin root with `architect.md`, `release.md`
- [ ] `.claude/commands/` directory is removed

### SKILL.md Validation

- [ ] `skills/worktracker/SKILL.md` has YAML frontmatter with `name`, `description`, `version`
- [ ] `skills/architecture/SKILL.md` has YAML frontmatter
- [ ] `skills/worktracker-decomposition/SKILL.md` has YAML frontmatter
- [ ] All skill descriptions include specific trigger phrases in quotes
- [ ] Optional: `allowed-tools` specified for skills that need restrictions

### Agent Validation

- [ ] `.claude/agents/orchestrator.md` has YAML frontmatter with `name`, `description`, `model`, `tools`
- [ ] `.claude/agents/qa-engineer.md` has YAML frontmatter
- [ ] `.claude/agents/security-auditor.md` has YAML frontmatter
- [ ] All agent descriptions include 2-4 `<example>` blocks
- [ ] Tool lists follow principle of least privilege

### Hook Validation

- [ ] `hooks/hooks.json` contains all hook configurations
- [ ] All hook paths use `${CLAUDE_PLUGIN_ROOT}` variable
- [ ] `.claude/hooks/` directory is removed or empty
- [ ] PreToolUse hook exists for Write/Edit operations

### Registry Validation

- [ ] `AGENTS.md` lists all 3 framework agents with correct paths
- [ ] `AGENTS.md` lists all 8 ps-* agents with correct paths
- [ ] All paths in `AGENTS.md` are accurate (files exist)
- [ ] Agent scopes (global vs skill-local) are documented

### Functional Validation

- [ ] Claude can discover and load the plugin
- [ ] Slash commands `/architect` and `/release` work from new location
- [ ] Skills are auto-invoked when trigger phrases are mentioned
- [ ] Agents can be delegated to via Task tool
- [ ] Hooks execute at appropriate lifecycle events

---

## Risk Assessment

### Risk of No Action

| Gap | Risk if Unaddressed | Likelihood | Impact |
|-----|---------------------|------------|--------|
| GAP-001/002 (Plugin structure) | Plugin fails to load with standard tools | High | Critical |
| GAP-006/007/008 (SKILL frontmatter) | Skills never auto-invoked | High | High |
| GAP-011-013 (Agent frontmatter) | Tool restrictions not enforced | Medium | Medium |
| GAP-016-020 (Hooks) | No pre-flight validation | Medium | Medium |
| GAP-021-022 (Registry) | New team members can't discover agents | Low | Low |

### Migration Risks

| Risk | Mitigation |
|------|------------|
| Commands stop working during move | Test after each move |
| Hooks break due to path changes | Use `${CLAUDE_PLUGIN_ROOT}` consistently |
| Skills fail to load with bad frontmatter | Validate YAML syntax before commit |
| Plugin fails to load | Test with `claude-code --debug` |

---

## Sources

| ID | Document | Path | Key Contribution |
|----|----------|------|------------------|
| proj-003-e-001 | Claude Code Best Practices | `research/proj-003-e-001-claude-code-best-practices.md` | Plugin structure, SKILL.md schema, agent format, hooks.json patterns |
| proj-003-e-002 | Plugins Prior Art | `research/proj-003-e-002-plugins-prior-art.md` | Canonical directory structure, deprecated patterns, hook lifecycle events |
| proj-003-e-003 | Architecture Patterns | `research/proj-003-e-003-architecture-patterns.md` | AGENTS.md convention, hybrid agent organization, registry patterns |
| proj-003-e-004 | PROJ-001 Knowledge | `analysis/proj-003-e-004-proj001-knowledge.md` | Agent locations, template patterns, constitutional compliance, scope clarification |
| proj-003-e-005 | Gap Analysis | `analysis/proj-003-e-005-gap-analysis.md` | 23 gaps identified, severity ratings, remediation roadmap |

---

## Document History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | 2026-01-12 | ps-synthesizer | Initial synthesis document |

---

*Synthesis completed per P-001 (Truth and Accuracy), P-002 (File Persistence), and P-004 (Explicit Provenance)*
*Constitutional Compliance: All recommendations traceable to source documents; priorities justified with evidence*
