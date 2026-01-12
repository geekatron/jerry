# Analysis: Gap Analysis - Current State vs Best Practices

| Metadata | Value |
|----------|-------|
| **Document ID** | proj-003-e-005 |
| **PS ID** | proj-003 |
| **Entry Type** | Analysis |
| **Topic** | Gap Analysis - Current State vs Best Practices |
| **Date** | 2026-01-12 |
| **Author** | ps-analyst (v2.0.0) |
| **Status** | Complete |

---

## Executive Summary

This gap analysis identifies **23 gaps** between Jerry Framework's current agent/skill structure and industry best practices documented in proj-003-e-001 through proj-003-e-004.

**Severity Distribution:**

| Severity | Count | Critical Areas |
|----------|-------|----------------|
| High | 6 | Plugin manifest schema, SKILL.md frontmatter, command placement |
| Medium | 10 | Agent definitions, hook system, directory structure |
| Low | 7 | Documentation, naming conventions, feature completeness |

**Key Findings:**

1. **Directory Structure**: Commands in `.claude/commands/` should be at plugin root level (`commands/`)
2. **Plugin Manifest**: Current `manifest.json` uses non-standard schema; should be `plugin.json`
3. **SKILL.md Compliance**: `worktracker` and `architecture` skills lack required YAML frontmatter
4. **Agent Definitions**: General agents lack YAML frontmatter; inconsistent with ps-* agents
5. **Hook System**: Partial implementation - `hooks/hooks.json` exists but incomplete lifecycle coverage
6. **AGENTS.md Registry**: Missing skill-specific agents (ps-*) from registry

**Estimated Remediation Effort:**
- Immediate (Critical): 2-4 hours
- Short-term (High Priority): 4-8 hours
- Long-term (Alignment): 8-16 hours

---

## Gap Inventory

### 1. Directory Structure Gaps

| Gap ID | Component | Current State | Best Practice | Severity | Priority | Source |
|--------|-----------|---------------|---------------|----------|----------|--------|
| GAP-001 | Commands Directory | `.claude/commands/` | `commands/` at plugin root | **High** | Immediate | e-001 L39-57 |
| GAP-002 | Plugin Manifest | `.claude-plugin/manifest.json` | `.claude-plugin/plugin.json` | **High** | Immediate | e-001 L41, e-002 L50-51 |
| GAP-003 | Skills Location | `skills/` at project root | Correct; optionally `.github/skills/` | Low | Long-term | e-002 L230-234 |
| GAP-004 | Hooks Directory | `hooks/hooks.json` + `.claude/hooks/` | `hooks/hooks.json` only | Medium | Short-term | e-001 L51, e-002 L64 |
| GAP-005 | MCP Configuration | Not found | `.mcp.json` at plugin root | Low | Long-term | e-001 L52 |

**5W1H Analysis - GAP-001:**
- **WHO**: All slash command files (`architect.md`, `release.md`)
- **WHAT**: Commands nested inside `.claude/` instead of plugin root
- **WHERE**: `.claude/commands/` vs `commands/`
- **WHEN**: Immediate - affects plugin discovery
- **WHY**: Non-compliance causes commands to be undiscoverable by standard plugin loaders
- **HOW**: Move `*.md` files from `.claude/commands/` to `commands/`

**5W1H Analysis - GAP-002:**
- **WHO**: Plugin manifest file
- **WHAT**: Non-standard filename and schema
- **WHERE**: `.claude-plugin/manifest.json` vs `.claude-plugin/plugin.json`
- **WHEN**: Immediate - breaks plugin loading
- **WHY**: Standard plugin discovery looks for `plugin.json`, not `manifest.json`
- **HOW**: Rename file; update to use standard schema `https://anthropic.com/claude-code/plugin.schema.json`

---

### 2. SKILL.md Compliance Gaps

| Gap ID | Component | Current State | Best Practice | Severity | Priority | Source |
|--------|-----------|---------------|---------------|----------|----------|--------|
| GAP-006 | worktracker SKILL.md | No YAML frontmatter | Required frontmatter with name, description, allowed-tools | **High** | Immediate | e-001 L104-124 |
| GAP-007 | architecture SKILL.md | No YAML frontmatter | Required frontmatter schema | **High** | Immediate | e-001 L104-124 |
| GAP-008 | worktracker-decomposition SKILL.md | No YAML frontmatter | Required frontmatter schema | **High** | Immediate | e-001 L104-124 |
| GAP-009 | problem-solving SKILL.md | Has frontmatter; custom keys | Standard keys + optional custom | Low | Long-term | e-001 L104-124 |
| GAP-010 | Trigger Phrases | Generic descriptions | Specific trigger phrases in description | Medium | Short-term | e-001 L126 |

**Current vs Expected Frontmatter:**

```yaml
# Current (worktracker/SKILL.md) - MISSING
# No frontmatter present

# Expected (per e-001 L104-124)
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

**5W1H Analysis - GAP-006/007/008:**
- **WHO**: `worktracker`, `architecture`, `worktracker-decomposition` skills
- **WHAT**: Missing required YAML frontmatter
- **WHERE**: First lines of each SKILL.md file
- **WHEN**: Immediate - affects auto-invocation
- **WHY**: Without frontmatter, Claude cannot auto-select skills based on task context
- **HOW**: Add compliant YAML frontmatter to each file; use third-person description with trigger phrases

---

### 3. Agent Definition Gaps

| Gap ID | Component | Current State | Best Practice | Severity | Priority | Source |
|--------|-----------|---------------|---------------|----------|----------|--------|
| GAP-011 | orchestrator.md | No YAML frontmatter | YAML frontmatter with model, tools, description | Medium | Short-term | e-001 L129-159, e-002 L157-175 |
| GAP-012 | qa-engineer.md | No YAML frontmatter | YAML frontmatter required | Medium | Short-term | e-001 L129-159 |
| GAP-013 | security-auditor.md | No YAML frontmatter | YAML frontmatter required | Medium | Short-term | e-001 L129-159 |
| GAP-014 | TEMPLATE.md | Informal template | Canonical template with frontmatter | Low | Long-term | e-004 L69-85 |
| GAP-015 | Agent `<example>` Blocks | Not present | 2-4 example invocation scenarios | Medium | Short-term | e-001 L134-135 |

**Current vs Expected Agent Format:**

```yaml
# Current (orchestrator.md) - No frontmatter
# Orchestrator Agent
> The "Conductor" - Coordinates...
**Recommended Model**: Opus 4.5
...

# Expected (per e-001 L129-153)
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

# Orchestrator Agent
...
```

**5W1H Analysis - GAP-011/012/013:**
- **WHO**: General-purpose agents in `.claude/agents/`
- **WHAT**: Missing YAML frontmatter with standardized fields
- **WHERE**: First lines of each agent `.md` file
- **WHEN**: Short-term - needed for consistent tool restrictions
- **WHY**: Frontmatter enables model specification, tool restrictions, and proper auto-selection
- **HOW**: Add YAML frontmatter following e-001 L129-153 pattern

---

### 4. Hook System Gaps

| Gap ID | Component | Current State | Best Practice | Severity | Priority | Source |
|--------|-----------|---------------|---------------|----------|----------|--------|
| GAP-016 | Hook Coverage | Only `SessionStart` | All lifecycle events | Medium | Short-term | e-002 L112-142 |
| GAP-017 | PreToolUse Hooks | Referenced in manifest, not in hooks.json | Should be in hooks.json | Medium | Short-term | e-001 L165-199 |
| GAP-018 | PostToolUse Hooks | Not implemented | Recommend for Edit/Write analysis | Low | Long-term | e-002 L137-140 |
| GAP-019 | Stop Hook | Not implemented | Recommend for task completion verification | Low | Long-term | e-001 L195-200 |
| GAP-020 | Hook Path References | Uses Python files in `.claude/hooks/` | Should use `${CLAUDE_PLUGIN_ROOT}` | Medium | Short-term | e-002 L72-73, L129 |

**Current hooks/hooks.json:**
```json
{
  "hooks": {
    "SessionStart": [/* only hook implemented */]
  }
}
```

**Recommended hooks/hooks.json (per e-001 L165-215, e-002 L121-142):**
```json
{
  "hooks": {
    "PreToolUse": [{
      "matcher": "Write|Edit",
      "hooks": [{
        "type": "command",
        "command": "python3 ${CLAUDE_PLUGIN_ROOT}/scripts/pre_tool_use.py",
        "timeout": 5000
      }]
    }],
    "PostToolUse": [{
      "matcher": "Edit",
      "hooks": [{
        "type": "prompt",
        "prompt": "Verify edit result maintains architectural constraints"
      }]
    }],
    "SessionStart": [{
      "matcher": "*",
      "hooks": [{
        "type": "command",
        "command": "python3 ${CLAUDE_PLUGIN_ROOT}/scripts/session_start.py",
        "timeout": 10000
      }]
    }],
    "Stop": [{
      "matcher": "*",
      "hooks": [{
        "type": "prompt",
        "prompt": "Verify task completion: Work Tracker updated, tests run if code changed"
      }]
    }]
  }
}
```

---

### 5. AGENTS.md Registry Gaps

| Gap ID | Component | Current State | Best Practice | Severity | Priority | Source |
|--------|-----------|---------------|---------------|----------|----------|--------|
| GAP-021 | Skill Agents | ps-* agents not listed | All agents should be indexed | Medium | Short-term | e-003 L368-388, e-004 L39-65 |
| GAP-022 | Agent Paths | Uses `.claude/agents/` only | Should list both locations | Medium | Short-term | e-004 L176-201 |
| GAP-023 | Registry Format | Informal markdown | Consider YAML-formatted REGISTRY.md | Low | Long-term | e-003 L367-388 |

**Current AGENTS.md:**
- Lists only 3 agents: orchestrator, qa-engineer, security-auditor
- Does not reference ps-* agents in `skills/problem-solving/agents/`

**Expected (per e-003 L367-388, e-004 L354-401):**
```markdown
## Framework Agents

| Agent | Path | Role |
|-------|------|------|
| orchestrator | `.claude/agents/orchestrator.md` | Task coordination |
| qa-engineer | `.claude/agents/qa-engineer.md` | Testing specialist |
| security-auditor | `.claude/agents/security-auditor.md` | Security review |

## Skill-Specific Agents

### Problem-Solving Skill

| Agent | Path | Role |
|-------|------|------|
| ps-researcher | `skills/problem-solving/agents/ps-researcher.md` | Research Specialist |
| ps-analyst | `skills/problem-solving/agents/ps-analyst.md` | Analysis Specialist |
| ps-architect | `skills/problem-solving/agents/ps-architect.md` | Architecture Decisions |
| ps-validator | `skills/problem-solving/agents/ps-validator.md` | Constraint Verification |
| ps-synthesizer | `skills/problem-solving/agents/ps-synthesizer.md` | Pattern Extraction |
| ps-reviewer | `skills/problem-solving/agents/ps-reviewer.md` | Quality Reviews |
| ps-investigator | `skills/problem-solving/agents/ps-investigator.md` | Failure Analysis |
| ps-reporter | `skills/problem-solving/agents/ps-reporter.md` | Status Reporting |
```

---

### 6. Plugin Manifest Schema Gaps

| Gap ID | Component | Current State | Best Practice | Severity | Priority | Source |
|--------|-----------|---------------|---------------|----------|----------|--------|
| GAP-002 | Filename | `manifest.json` | `plugin.json` | **High** | Immediate | e-001 L41, e-002 L51 |

**Current manifest.json Analysis:**

| Field | Current | Standard | Status |
|-------|---------|----------|--------|
| `$schema` | Custom URL | `https://anthropic.com/claude-code/plugin.schema.json` | Non-compliant |
| `name` | "jerry" | "jerry" | OK |
| `version` | "0.1.0" | "0.1.0" | OK |
| `description` | Present | Required | OK |
| `author` | String | Object `{name, email?, url?}` | Non-compliant |
| `commands` | Array of objects | Path string `"./commands"` | Non-compliant |
| `agents` | Array of objects | Path array `["./agents"]` | Non-compliant |
| `hooks` | Object with keys | Path string `"./hooks/hooks.json"` | Non-compliant |
| `skills` | Array of objects | Not standard; discovered from directories | Non-standard |

**Expected plugin.json (per e-001 L61-89):**
```json
{
  "$schema": "https://anthropic.com/claude-code/plugin.schema.json",
  "name": "jerry",
  "version": "0.1.0",
  "description": "Framework for behavior and workflow guardrails with knowledge accrual",
  "author": {
    "name": "Jerry Framework Contributors"
  },
  "license": "MIT",
  "repository": {
    "type": "git",
    "url": "https://github.com/geekatron/jerry"
  },
  "keywords": ["workflow", "guardrails", "knowledge-management"],
  "commands": "./commands",
  "agents": ["./agents", "./skills/problem-solving/agents"],
  "hooks": "./hooks/hooks.json"
}
```

---

### 7. Deprecated Pattern Usage

| Gap ID | Component | Current State | Best Practice | Severity | Priority | Source |
|--------|-----------|---------------|---------------|----------|----------|--------|
| - | Tool names | Using current names | OK (Read, Write, etc.) | - | - | e-001 L362 |
| - | Skills location | `skills/` | OK (`.github/skills/` is recommended, not required) | - | - | e-002 L214 |
| - | Settings file | `.claude/settings.json` | OK (correct location) | - | - | e-002 L207-209 |

**No deprecated patterns detected.** Jerry's codebase avoids known deprecated patterns:
- Uses `Read` not `View` (e-001 L362)
- Uses `.claude/settings.json` not `.claude.json` (e-002 L207)
- Does not use removed `allowedTools`/`ignorePatterns` settings

---

## Remediation Roadmap

### Immediate Actions (Critical Gaps - Hours 1-4)

- [ ] **GAP-002**: Rename `.claude-plugin/manifest.json` to `.claude-plugin/plugin.json`
- [ ] **GAP-002**: Update schema URL to `https://anthropic.com/claude-code/plugin.schema.json`
- [ ] **GAP-002**: Convert manifest fields to standard format (author object, path strings)
- [ ] **GAP-001**: Move `architect.md` and `release.md` from `.claude/commands/` to `commands/`
- [ ] **GAP-006/007/008**: Add YAML frontmatter to `worktracker/SKILL.md`
- [ ] **GAP-006/007/008**: Add YAML frontmatter to `architecture/SKILL.md`
- [ ] **GAP-006/007/008**: Add YAML frontmatter to `worktracker-decomposition/SKILL.md`

### Short-term Actions (High Priority - Hours 5-12)

- [ ] **GAP-011/012/013**: Add YAML frontmatter to `orchestrator.md`
- [ ] **GAP-011/012/013**: Add YAML frontmatter to `qa-engineer.md`
- [ ] **GAP-011/012/013**: Add YAML frontmatter to `security-auditor.md`
- [ ] **GAP-015**: Add `<example>` blocks to agent descriptions
- [ ] **GAP-010**: Update skill descriptions with specific trigger phrases
- [ ] **GAP-016/017**: Consolidate hooks into `hooks/hooks.json`
- [ ] **GAP-020**: Update hook paths to use `${CLAUDE_PLUGIN_ROOT}`
- [ ] **GAP-004**: Remove `.claude/hooks/` directory (move logic to scripts/)
- [ ] **GAP-021/022**: Update AGENTS.md with complete registry including ps-* agents

### Long-term Actions (Alignment - Hours 13-28)

- [ ] **GAP-018/019**: Add PostToolUse and Stop hooks for quality assurance
- [ ] **GAP-005**: Create `.mcp.json` if MCP integration needed
- [ ] **GAP-003**: Consider moving skills to `.github/skills/` for cross-platform
- [ ] **GAP-009**: Standardize problem-solving SKILL.md frontmatter keys
- [ ] **GAP-014**: Update TEMPLATE.md to canonical format with YAML frontmatter
- [ ] **GAP-023**: Consider YAML-formatted REGISTRY.md for programmatic access

---

## Impact Assessment

### Risk of No Action

| Gap | Risk if Unaddressed |
|-----|---------------------|
| GAP-001/002 | Plugin may not load correctly with standard loaders; breaks distribution |
| GAP-006/007/008 | Skills cannot be auto-invoked; users must explicitly request |
| GAP-011-013 | Agent tool restrictions not enforced; model selection ignored |
| GAP-016-020 | No validation hooks; quality gates bypass-able |
| GAP-021-022 | New team members cannot discover available agents |

### Expected Benefits

| Benefit | Gaps Addressed |
|---------|----------------|
| **Standard Plugin Loading** | GAP-001, GAP-002 |
| **Auto-invocation of Skills** | GAP-006, GAP-007, GAP-008, GAP-010 |
| **Consistent Agent Behavior** | GAP-011, GAP-012, GAP-013, GAP-015 |
| **Complete Agent Discovery** | GAP-021, GAP-022, GAP-023 |
| **Quality Assurance via Hooks** | GAP-016, GAP-017, GAP-018, GAP-019, GAP-020 |
| **Cross-platform Portability** | GAP-003, GAP-020 |

---

## Compliance Checklist

After remediation, validate:

### Plugin Structure
- [ ] `.claude-plugin/plugin.json` exists with standard schema
- [ ] `commands/` directory at plugin root contains all commands
- [ ] `agents/` or `.claude/agents/` properly referenced in plugin.json
- [ ] `hooks/hooks.json` contains all hook configurations
- [ ] `skills/` directory contains SKILL.md files with frontmatter

### SKILL.md Files
- [ ] All skills have YAML frontmatter with `name`, `description`, `version`
- [ ] Descriptions include specific trigger phrases
- [ ] `allowed-tools` specified for skills that need restrictions

### Agent Files
- [ ] All agents have YAML frontmatter with `name`, `description`, `model`, `tools`
- [ ] Descriptions include 2-4 `<example>` blocks
- [ ] Tool lists follow principle of least privilege

### Hook System
- [ ] `hooks/hooks.json` covers SessionStart, PreToolUse at minimum
- [ ] All paths use `${CLAUDE_PLUGIN_ROOT}` variable
- [ ] No duplicate hooks between `hooks.json` and other locations

### Registry
- [ ] AGENTS.md lists all agents (framework + skill-specific)
- [ ] All paths are accurate and files exist
- [ ] Agent scopes (global vs skill-local) documented

---

## Sources

| ID | Document | Key Findings Used |
|----|----------|-------------------|
| proj-003-e-001 | Claude Code Best Practices | Plugin structure, SKILL.md schema, agent format, hooks.json |
| proj-003-e-002 | Plugins Prior Art | Canonical directory structure, deprecated patterns, hook lifecycle |
| proj-003-e-003 | Architecture Patterns | AGENTS.md convention, hybrid agent organization |
| proj-003-e-004 | PROJ-001 Knowledge | Agent locations, template patterns, constitutional compliance |

---

## Document History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | 2026-01-12 | ps-analyst | Initial gap analysis document |

---

*Analysis completed per P-001 (Truth and Accuracy), P-002 (File Persistence), and P-004 (Explicit Provenance)*
*Constitutional Compliance: All gaps traceable to research sources; severity justified with evidence*
