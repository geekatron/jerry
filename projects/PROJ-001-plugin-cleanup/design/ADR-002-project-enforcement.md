# ADR-002: Project Enforcement at Session Start

**Status**: PROPOSED
**Date**: 2026-01-09
**Author**: Claude (Opus 4.5)
**Project**: PROJ-001-plugin-cleanup

---

## Context

### Problem Statement

When starting a new Claude Code session within the Jerry Framework, there is no mechanism to enforce that the `JERRY_PROJECT` environment variable is set. This leads to:

1. **Context Confusion**: Claude operates without knowing which project context to use
2. **Lost Work**: Tasks and progress aren't tracked in the correct WORKTRACKER.md
3. **Inconsistent Behavior**: Different sessions may operate on different implicit projects
4. **User Friction**: Users must remember to set the variable manually before each session

### 5W1H Analysis

| Dimension | Analysis |
|-----------|----------|
| **WHAT** | A hard enforcement mechanism that validates JERRY_PROJECT at session start and guides users through project selection/creation |
| **WHY** | The multi-project isolation implemented in Phase 1-5 is useless without enforcement; tasks get lost, context gets confused |
| **WHO** | Every Claude Code session operating within Jerry; both new and experienced users |
| **WHERE** | In the plugin hook system (SessionStart) and CLAUDE.md behavioral rules |
| **WHEN** | At session initialization, before any work begins |
| **HOW** | Two-layer enforcement: Hook (deterministic detection) + Claude behavior (agentic interaction) |

---

## Decision Drivers

1. **Determinism**: Hooks must produce consistent, predictable output
2. **User Experience**: Interactive project selection should be conversational, not CLI-based
3. **Plugin Architecture**: Must follow Claude Code plugin conventions
4. **Architectural Purity**: Must follow Hexagonal Architecture, DDD, CQRS patterns
5. **Testability**: Must be comprehensively testable at all layers
6. **Fail-Safe**: Must handle edge cases and failures gracefully

---

## Alternatives Considered

### Option A: Pure Hook Enforcement (Rejected)

**Description**: SessionStart hook blocks session if JERRY_PROJECT is not set (exit code 2).

**Pros**:
- Simple implementation
- Guaranteed enforcement

**Cons**:
- No interactive recovery - user must restart session
- Poor user experience
- Cannot guide user through project selection
- Hooks cannot be interactive

**Decision**: REJECTED - UX is unacceptable

### Option B: CLAUDE.md Instruction Only (Rejected)

**Description**: Add instructions to CLAUDE.md telling Claude to check the variable and ask if missing.

**Pros**:
- No code changes required
- Flexible

**Cons**:
- Soft enforcement - Claude may not always follow
- No structured data about available projects
- Claude must scan filesystem each time

**Decision**: REJECTED - Not reliable enough for "hard" enforcement

### Option C: MCP Server for Project Management (Considered)

**Description**: Create an MCP server that manages project state and provides tools for project selection.

**Pros**:
- Rich tooling capabilities
- Can maintain state across sessions
- First-class integration

**Cons**:
- Higher complexity
- Requires MCP server deployment
- Overkill for this use case

**Decision**: DEFERRED - May consider for future enhancements

### Option D: Two-Layer Enforcement (Selected)

**Description**: Combine deterministic hook detection with agentic Claude interaction.

**Layer 1 - SessionStart Hook (Deterministic)**:
- Check if `JERRY_PROJECT` environment variable is set
- Scan `projects/` directory for available projects
- Output structured data for Claude to consume
- Always exit 0 (success) - never block the session

**Layer 2 - CLAUDE.md Hard Rule (Agentic)**:
- Parse hook output for structured signals
- If `ProjectRequired` signal present, MUST use AskUserQuestion
- Cannot proceed with ANY work until project is selected
- Handle both existing project selection and new project creation

**Pros**:
- Best of both worlds: deterministic detection + interactive recovery
- Follows plugin conventions (hooks/hooks.json at root)
- Testable at multiple layers
- Graceful failure handling
- Good user experience

**Cons**:
- Two-layer complexity
- Requires coordination between hook and Claude behavior

**Decision**: SELECTED

---

## Detailed Design

### Plugin Directory Structure

```
jerry/                           # Plugin root
├── .claude-plugin/
│   └── manifest.json           # Plugin manifest (references hooks)
├── hooks/
│   └── hooks.json              # Hook configuration (SessionStart)
├── scripts/
│   ├── session_start.py        # Entry point (Interface Layer)
│   ├── domain/                 # Domain Layer (pure, no deps)
│   │   ├── __init__.py
│   │   ├── project_id.py       # ProjectId Value Object
│   │   ├── project_info.py     # ProjectInfo Entity
│   │   ├── project_status.py   # ProjectStatus Enum
│   │   ├── validation.py       # ValidationResult Value Object
│   │   └── errors.py           # Domain exceptions
│   ├── application/            # Application Layer (use cases)
│   │   ├── __init__.py
│   │   ├── ports.py            # IProjectRepository, IEnvironmentProvider
│   │   └── queries.py          # ScanProjects, ValidateProject, GetNextNumber
│   ├── infrastructure/         # Infrastructure Layer (adapters)
│   │   ├── __init__.py
│   │   ├── filesystem.py       # FilesystemProjectAdapter
│   │   └── environment.py      # OsEnvironmentAdapter
│   └── tests/                  # Test suites
│       ├── unit/
│       ├── integration/
│       ├── e2e/
│       ├── contract/
│       └── architecture/
└── projects/                   # Project workspaces
```

### Hook Output Format

```xml
<!-- When JERRY_PROJECT is set and valid -->
<project-context>
ProjectActive: PROJ-001-plugin-cleanup
ProjectPath: projects/PROJ-001-plugin-cleanup/
ValidationMessage: Project is properly configured
</project-context>

<!-- When JERRY_PROJECT is not set -->
<project-required>
ProjectRequired: true
AvailableProjects:
  - PROJ-001-plugin-cleanup [ACTIVE]
  - PROJ-002-feature-x [DRAFT]
NextProjectNumber: 003
ProjectsJson: [{"id": "PROJ-001-plugin-cleanup", "status": "IN_PROGRESS"}]
</project-required>

ACTION REQUIRED: No JERRY_PROJECT environment variable set.
Claude MUST use AskUserQuestion to help the user select an existing project or create a new one.
DO NOT proceed with any work until a project is selected.
```

### CLAUDE.md Hard Rule

```markdown
## Project Enforcement (Hard Rule)

IF the SessionStart hook outputs `<project-required>`:

1. You MUST immediately use AskUserQuestion with:
   - Option to select from existing projects (listed in hook output)
   - Option to create a new project

2. IF user selects existing project:
   - Inform them to set: `export JERRY_PROJECT={selected_id}`
   - DO NOT proceed until they confirm the variable is set

3. IF user wants to create a new project:
   - Ask for project name (will become the slug)
   - Generate ID using NextProjectNumber from hook output
   - Guide them through: mkdir, PLAN.md, WORKTRACKER.md creation
   - Inform them to set the environment variable

4. You CANNOT proceed with ANY other work until a project is active.
```

---

## Edge Cases and Failure Scenarios

| Scenario | Hook Behavior | Claude Behavior |
|----------|---------------|-----------------|
| JERRY_PROJECT set, project exists | Output `<project-context>` | Proceed normally |
| JERRY_PROJECT set, project missing | Output `<project-error>` | Use AskUserQuestion to help fix |
| JERRY_PROJECT not set, projects exist | Output `<project-required>` with list | Use AskUserQuestion for selection |
| JERRY_PROJECT not set, no projects | Output `<project-required>` with empty list | Guide user to create first project |
| projects/ directory missing | Output error, suggest creation | Guide user to create directory |
| Permission denied on projects/ | Output error message | Inform user of permission issue |
| Malformed project directory name | Ignore and continue scanning | Show only valid projects |
| WORKTRACKER.md corrupted | Log warning, mark status UNKNOWN | Show project with warning |
| Hook timeout | Claude sees no hook output | Fall back to scanning manually |

---

## Test Strategy

### Coverage Matrix

| Layer | Test Type | Coverage Target | Key Scenarios |
|-------|-----------|-----------------|---------------|
| Domain | Unit | 100% | Value object validation, entity creation, enum values |
| Application | Unit | 100% | Query execution, port interactions, error handling |
| Infrastructure | Integration | 90% | Filesystem operations, environment access, error recovery |
| Interface | E2E | 85% | Full hook flow, output format, exit codes |
| Cross-cutting | Contract | 100% | Output format matches Claude consumption spec |
| Cross-cutting | Architecture | 100% | Dependency direction, layer isolation |

### Test Categories

1. **Happy Path**: Normal successful operations
2. **Edge Cases**: Boundary conditions, unusual but valid inputs
3. **Negative Tests**: Invalid inputs, missing resources
4. **Failure Scenarios**: I/O errors, permissions, corruption
5. **Boundary Tests**: Min/max values, empty collections

---

## Security Considerations

1. **Path Traversal**: Validate project IDs don't contain `..` or absolute paths
2. **Injection**: Sanitize all inputs before shell execution
3. **Information Disclosure**: Don't leak sensitive info in hook output
4. **Denial of Service**: Handle large project counts gracefully

---

## References

### Industry Sources

- [Claude Code Hooks Reference](https://code.claude.com/docs/en/hooks) - Official documentation
- [Context7 Plugin Structure](https://github.com/anthropics/claude-code/blob/main/plugins/plugin-dev/skills/plugin-structure/SKILL.md) - Plugin conventions
- [Claude Code Hooks Mastery](https://github.com/disler/claude-code-hooks-mastery) - Community best practices
- [Hexagonal Architecture](https://alistair.cockburn.us/hexagonal-architecture/) - Alistair Cockburn

### Internal References

- `WORKTRACKER.md` - Phase 6: Project Enforcement tasks
- `CLAUDE.md` - Framework documentation
- `docs/governance/JERRY_CONSTITUTION.md` - Behavioral principles

---

## Decision

**Selected**: Option D - Two-Layer Enforcement

**Rationale**: This approach provides deterministic detection via hooks while allowing interactive, conversational recovery via Claude's AskUserQuestion tool. It follows Claude Code plugin conventions, maintains architectural purity, and provides excellent user experience.

---

## Consequences

### Positive

- Users cannot accidentally work without project context
- Interactive project selection improves UX
- Follows established plugin patterns
- Comprehensively testable
- Graceful failure handling

### Negative

- Two-layer complexity requires coordination
- CLAUDE.md rule is "soft" enforcement (relies on Claude following instructions)
- Initial setup requires creating hook infrastructure

### Mitigations

- Clear documentation of the two-layer architecture
- Add behavior test to BEHAVIOR_TESTS.md to validate Claude compliance
- Comprehensive test coverage to catch regressions

---

## Implementation Plan

See `WORKTRACKER.md` Phase 6 for detailed task breakdown (ENFORCE-001 through ENFORCE-016).
