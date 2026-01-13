# ADR-PROJ003-001: Agent and Skill Cleanup Strategy

| Metadata | Value |
|----------|-------|
| **Status** | Proposed |
| **Date** | 2026-01-12 |
| **Deciders** | User, ps-architect |
| **Project** | PROJ-003-agents-cleanup |
| **Related** | proj-003-e-001 through proj-003-e-006 |

---

## Context

### Problem Statement

The Jerry Framework has evolved organically, resulting in a plugin structure that deviates from Claude Code industry standards. This deviation causes:

1. **Plugin discovery failures** - Non-standard `manifest.json` filename and schema prevent standard Claude Code tooling from recognizing Jerry as a valid plugin
2. **Skill auto-invocation failures** - Missing YAML frontmatter in 3 of 4 skills prevents Claude from automatically activating skills when users mention trigger phrases
3. **Inconsistent agent definitions** - Framework agents lack the standardized frontmatter that ps-* agents follow, creating maintenance burden and reducing tool enforcement

A comprehensive gap analysis (proj-003-e-005) identified **23 gaps** between Jerry's current state and Claude Code best practices, with **6 high-severity** issues requiring immediate remediation.

### Current State

**Plugin Structure:**
```
jerry/
├── .claude-plugin/
│   └── manifest.json          # NON-STANDARD (should be plugin.json)
├── .claude/
│   ├── commands/              # WRONG LOCATION (should be at root)
│   │   ├── architect.md
│   │   └── release.md
│   ├── agents/
│   │   ├── orchestrator.md    # MISSING YAML frontmatter
│   │   ├── qa-engineer.md     # MISSING YAML frontmatter
│   │   └── security-auditor.md # MISSING YAML frontmatter
│   └── hooks/                 # NON-STANDARD location
├── skills/
│   ├── problem-solving/
│   │   ├── SKILL.md           # Partial frontmatter (trigger phrases missing)
│   │   └── agents/            # 8 ps-* agents (COMPLIANT)
│   ├── worktracker/
│   │   └── SKILL.md           # MISSING YAML frontmatter
│   ├── worktracker-decomposition/
│   │   └── SKILL.md           # MISSING YAML frontmatter
│   └── architecture/
│       └── SKILL.md           # MISSING YAML frontmatter
└── AGENTS.md                  # INCOMPLETE (missing ps-* agents)
```

**Gap Summary by Category:**

| Category | Gap Count | High Severity Issues |
|----------|-----------|---------------------|
| Directory Structure | 5 | GAP-001 (commands), GAP-002 (manifest) |
| SKILL.md Compliance | 5 | GAP-006/007/008 (frontmatter) |
| Agent Definitions | 5 | None (all Medium) |
| Hook System | 5 | None (all Medium/Low) |
| AGENTS.md Registry | 3 | None (all Medium/Low) |

### Research Summary

Research across five documents (proj-003-e-001 through proj-003-e-005) established:

1. **Canonical Plugin Structure** (proj-003-e-001): Plugin components MUST be at plugin root. Only `plugin.json` belongs inside `.claude-plugin/`. Commands live in `commands/`, not `.claude/commands/`.

2. **SKILL.md Schema** (proj-003-e-001): Skills require YAML frontmatter with `name`, `description` (including specific trigger phrases), `version`, and optional `allowed-tools` for Claude to auto-invoke them.

3. **Agent Definition Schema** (proj-003-e-001): Agents require YAML frontmatter with `name`, `description` (with example invocations), `model`, `color`, and `tools` for proper tool enforcement.

4. **Hybrid Agent Organization** (proj-003-e-003): Industry favors the hybrid pattern Jerry already uses - general agents in `.claude/agents/`, skill-specific agents in `skills/{skill}/agents/`. **No reorganization needed.**

5. **Plugin Ecosystem Convergence** (proj-003-e-002): By December 2025, the Claude Code plugin ecosystem standardized on canonical structure. Jerry needs alignment to participate.

### Constraints

- **Backward Compatibility**: Existing skill invocations via `/problem-solving` must continue working
- **Minimal Disruption**: Changes should be sequenced to minimize broken functionality during migration
- **Constitutional Compliance**: All changes must maintain P-002 (File Persistence), P-003 (Single-Level Nesting), P-022 (No Deception)
- **Zero External Dependencies**: Jerry's domain layer must remain stdlib-only

### Stakeholders

| Stakeholder | Concern |
|-------------|---------|
| Framework Users | Skills/commands continue working |
| Jerry Maintainers | Clear, standardized structure |
| Plugin Ecosystem | Standard plugin discovery |
| Claude Code | Auto-invocation of skills and agents |

---

## Decision

### Core Decision

We will **align Jerry's plugin structure with Claude Code industry standards** through a phased migration that:

1. **Renames and restructures plugin manifest** from `manifest.json` to `plugin.json` with standard schema
2. **Relocates commands** from `.claude/commands/` to `commands/` at plugin root
3. **Adds YAML frontmatter** to all 4 SKILL.md files with specific trigger phrases
4. **Standardizes agent definitions** by adding YAML frontmatter to 3 framework agents
5. **Expands AGENTS.md registry** to include all 11 agents (3 framework + 8 ps-*)
6. **Preserves hybrid agent organization** - no agent file moves required

The hybrid agent architecture (`.claude/agents/` for framework agents, `skills/{skill}/agents/` for specialists) is **retained** as it aligns with industry best practices.

### Decision Rationale

| Factor | Decision Impact |
|--------|-----------------|
| Industry Alignment | Standard plugin structure enables ecosystem participation |
| Auto-Invocation | SKILL.md frontmatter enables Claude to activate skills automatically |
| Tool Enforcement | Agent frontmatter enables principle of least privilege |
| Discoverability | Complete AGENTS.md enables team onboarding |
| Low Risk | No agent reorganization = minimal breaking changes |

The synthesis (proj-003-e-006) confirmed that Jerry's agent organization is already correct. The gaps are in **metadata and configuration**, not **file location**.

### Alternatives Considered

#### Option A: Centralized Agent Repository

- **Description:** Move all agents (including ps-*) to `.claude/agents/` for a single source of truth
- **Pros:**
  - Single location for all agents
  - Simpler AGENTS.md registry
- **Cons:**
  - Breaks skill encapsulation (ps-* agents are tightly coupled to problem-solving skill)
  - Contradicts industry hybrid pattern (60,000+ projects use hybrid)
  - Requires updating all ps-* agent references
- **Decision:** Rejected - breaks encapsulation, contradicts industry consensus

#### Option B: Distributed Agent Repository

- **Description:** Move framework agents to their respective skills, eliminate `.claude/agents/`
- **Pros:**
  - Complete skill encapsulation
  - Each skill fully self-contained
- **Cons:**
  - Framework agents (orchestrator, qa-engineer, security-auditor) are cross-cutting, not skill-specific
  - Would require artificial skill creation for framework agents
  - Poor discoverability
- **Decision:** Rejected - framework agents are genuinely cross-cutting

#### Option C: Status Quo with Documentation

- **Description:** Keep current structure, document workarounds
- **Pros:**
  - Zero migration effort
  - No risk of breaking changes
- **Cons:**
  - Plugin discovery remains broken (High impact)
  - Skill auto-invocation fails (High impact)
  - Growing technical debt
- **Decision:** Rejected - high-severity gaps remain unresolved

#### Option D: Hybrid with Standardization (SELECTED)

- **Description:** Keep agent locations, standardize metadata and plugin structure
- **Pros:**
  - Addresses all 6 high-severity gaps
  - Minimal file moves (only commands/)
  - Industry-aligned plugin structure
  - Preserves working agent organization
- **Cons:**
  - Requires frontmatter additions to multiple files
  - Estimated 6-9 hours of work
- **Decision:** **Accepted** - best risk/reward ratio

### Scope

#### In Scope

- Rename `.claude-plugin/manifest.json` to `.claude-plugin/plugin.json`
- Update plugin.json schema and field formats
- Move commands from `.claude/commands/` to `commands/`
- Add YAML frontmatter to 4 SKILL.md files
- Add YAML frontmatter to 3 framework agents
- Update hooks/hooks.json paths to use `${CLAUDE_PLUGIN_ROOT}`
- Expand AGENTS.md to list all 11 agents
- Add PreToolUse hooks for Write/Edit validation

#### Out of Scope

- Creating worktracker agents (greenfield work, not cleanup)
- Restructuring CLAUDE.md (separate initiative)
- Adding path scoping to rules (separate initiative)
- Creating PLAYBOOK.md for worktracker skills (enhancement)
- Migrating skills to `.github/skills/` (low priority, optional)

---

## Implementation Plan

### Phase 1: Plugin Infrastructure (1-2 hours)

**Duration:** 1-2 hours
**Rationale:** These changes are foundational and unblock plugin discovery.

**Changes:**
- [ ] Rename `.claude-plugin/manifest.json` to `.claude-plugin/plugin.json`
- [ ] Update `$schema` to `https://anthropic.com/claude-code/plugin.schema.json`
- [ ] Convert `author` from string to object format: `{"name": "...", "url": "..."}`
- [ ] Convert `commands`, `agents`, `hooks` from nested objects to path strings
- [ ] Create `commands/` directory at plugin root
- [ ] Move `architect.md` from `.claude/commands/` to `commands/`
- [ ] Move `release.md` from `.claude/commands/` to `commands/`
- [ ] Remove empty `.claude/commands/` directory
- [ ] Update plugin.json with new paths

**Validation:**
```bash
# Plugin file exists with correct name
test -f .claude-plugin/plugin.json

# Commands directory exists at root
test -d commands && test -f commands/architect.md

# Old location removed
test ! -d .claude/commands
```

### Phase 2: Skill Frontmatter (1-2 hours)

**Duration:** 1-2 hours
**Rationale:** Required for skill auto-invocation.

**Changes:**
- [ ] Add YAML frontmatter to `skills/worktracker/SKILL.md`:
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
- [ ] Add YAML frontmatter to `skills/architecture/SKILL.md`:
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
- [ ] Add YAML frontmatter to `skills/worktracker-decomposition/SKILL.md`:
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
- [ ] Update `skills/problem-solving/SKILL.md` description with specific trigger phrases

**Validation:**
```bash
# Each SKILL.md has frontmatter
for skill in worktracker architecture worktracker-decomposition; do
  head -1 skills/$skill/SKILL.md | grep -q "^---" && echo "$skill: OK"
done
```

### Phase 3: Agent Standardization (2-3 hours)

**Duration:** 2-3 hours
**Rationale:** Improves tool enforcement and auto-selection.

**Changes:**
- [ ] Add YAML frontmatter to `.claude/agents/orchestrator.md`:
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
- [ ] Add YAML frontmatter to `.claude/agents/qa-engineer.md`:
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
- [ ] Add YAML frontmatter to `.claude/agents/security-auditor.md`:
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
- [ ] Update `.claude/agents/TEMPLATE.md` to align with PS_AGENT_TEMPLATE structure

**Validation:**
```bash
# Each agent has frontmatter with required fields
for agent in orchestrator qa-engineer security-auditor; do
  grep -q "^name:" .claude/agents/$agent.md && echo "$agent: OK"
done
```

### Phase 4: Hook System (1-2 hours)

**Duration:** 1-2 hours
**Rationale:** Improves quality assurance and security.

**Changes:**
- [ ] Update `hooks/hooks.json` to use `${CLAUDE_PLUGIN_ROOT}` for all paths
- [ ] Add PreToolUse hook for Write/Edit operations:
  ```json
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
  ]
  ```
- [ ] Create `scripts/pre_tool_use.py` validation script if needed
- [ ] Move any scripts from `.claude/hooks/` to `scripts/`
- [ ] Remove empty `.claude/hooks/` directory

**Validation:**
```bash
# hooks.json uses portable paths
grep -q '\${CLAUDE_PLUGIN_ROOT}' hooks/hooks.json && echo "Paths: OK"

# PreToolUse hook exists
grep -q '"PreToolUse"' hooks/hooks.json && echo "PreToolUse: OK"
```

### Phase 5: Registry Update (30 minutes)

**Duration:** 30 minutes
**Rationale:** Improves agent discoverability.

**Changes:**
- [ ] Update `AGENTS.md` to include Framework Agents section with paths
- [ ] Add Skill-Specific Agents section listing all 8 ps-* agents:
  - ps-researcher
  - ps-analyst
  - ps-synthesizer
  - ps-validator
  - ps-reporter
  - ps-architect
  - ps-reviewer
  - ps-investigator
- [ ] Document agent scopes (global vs skill-local)
- [ ] Verify all paths are accurate (files exist)

**Validation:**
```bash
# AGENTS.md lists all agents
grep -c "\.md" AGENTS.md  # Should show 11+ agent references
```

---

## Consequences

### Positive

| Benefit | Impact |
|---------|--------|
| Plugin discovery works | Claude Code standard tooling recognizes Jerry |
| Skill auto-invocation enabled | Users mention trigger phrases, skills activate automatically |
| Tool enforcement via frontmatter | Agents restricted to declared tools (principle of least privilege) |
| Complete agent registry | Team members can discover all 11 agents |
| Industry alignment | Jerry participates in broader plugin ecosystem |
| Reduced maintenance burden | Standardized patterns across all agents/skills |

### Negative

| Tradeoff | Mitigation |
|----------|------------|
| Migration effort (~6-9 hours) | Phased approach minimizes risk per phase |
| Commands change location | Update documentation, test after move |
| Frontmatter maintenance overhead | Templates provide copy-paste patterns |
| Potential for YAML syntax errors | Validate YAML before commit |

### Risks

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Commands stop working during move | Medium | High | Move one at a time, test immediately |
| Hooks break due to path changes | Medium | Medium | Use `${CLAUDE_PLUGIN_ROOT}` consistently |
| SKILL.md YAML syntax errors | Low | High | Validate YAML syntax before commit |
| Plugin fails to load after changes | Low | Critical | Test with `claude-code --debug` after each phase |
| Existing workflows disrupted | Low | Medium | No agent reorganization = minimal workflow impact |

---

## Validation

### Success Criteria

**Plugin Structure:**
- [ ] `.claude-plugin/plugin.json` exists (not `manifest.json`)
- [ ] `plugin.json` uses standard Anthropic schema
- [ ] `commands/` directory at root with `architect.md`, `release.md`
- [ ] `.claude/commands/` directory removed

**SKILL.md Compliance:**
- [ ] All 4 SKILL.md files have YAML frontmatter
- [ ] All frontmatter includes `name`, `description`, `version`
- [ ] All descriptions include specific trigger phrases in quotes

**Agent Compliance:**
- [ ] All 3 framework agents have YAML frontmatter
- [ ] All frontmatter includes `name`, `description`, `model`, `tools`
- [ ] All descriptions include 2-4 `<example>` blocks

**Hook Compliance:**
- [ ] All hook paths use `${CLAUDE_PLUGIN_ROOT}`
- [ ] PreToolUse hook configured for Write/Edit
- [ ] `.claude/hooks/` directory removed or empty

**Registry Compliance:**
- [ ] AGENTS.md lists all 11 agents with paths
- [ ] All paths in AGENTS.md resolve to existing files

**Functional Validation:**
- [ ] Plugin loads successfully in Claude Code
- [ ] `/architect` and `/release` commands work from new location
- [ ] Skills auto-invoke when trigger phrases mentioned
- [ ] Agents can be delegated to via Task tool

### Rollback Plan

If migration causes critical issues:

1. **Phase 1 Rollback:** Rename `plugin.json` back to `manifest.json`, move commands back to `.claude/commands/`
2. **Phase 2 Rollback:** Remove YAML frontmatter from SKILL.md files (content unaffected)
3. **Phase 3 Rollback:** Remove YAML frontmatter from agent files (content unaffected)
4. **Phase 4 Rollback:** Revert `hooks/hooks.json` to previous state
5. **Phase 5 Rollback:** Revert AGENTS.md changes

Each phase is independently reversible. Git commits should be made at phase boundaries.

---

## References

| ID | Document | Purpose |
|----|----------|---------|
| proj-003-e-001 | research/proj-003-e-001-claude-code-best-practices.md | Plugin structure, SKILL.md schema, agent format, hooks.json patterns |
| proj-003-e-002 | research/proj-003-e-002-plugins-prior-art.md | Canonical directory structure, deprecated patterns, hook lifecycle |
| proj-003-e-003 | research/proj-003-e-003-architecture-patterns.md | AGENTS.md convention, hybrid agent organization, registry patterns |
| proj-003-e-004 | analysis/proj-003-e-004-proj001-knowledge.md | Agent locations, template patterns, constitutional compliance |
| proj-003-e-005 | analysis/proj-003-e-005-gap-analysis.md | 23 gaps identified, severity ratings, remediation roadmap |
| proj-003-e-006 | synthesis/proj-003-e-006-synthesis.md | Integrated synthesis with decision matrix and migration sequence |

---

## Document History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | 2026-01-12 | ps-architect | Initial ADR based on proj-003-e-006 synthesis |

---

*ADR created per P-001 (Truth and Accuracy), P-002 (File Persistence), P-004 (Explicit Provenance)*
*All decisions traceable to source documents proj-003-e-001 through proj-003-e-006*
