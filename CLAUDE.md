# CLAUDE.md - Jerry Framework Root Context

> This file provides context to Claude Code at session start.
> It serves as **procedural memory** - loaded once, not maintained in context.

---

## Project Overview

**Jerry** is a framework for behavior and workflow guardrails that helps solve problems
while accruing a body of knowledge, wisdom, and experience.

### Core Problem: Context Rot

> "Context Rot is the phenomenon where an LLM's performance degrades as the context
> window fills up, even when total token count is well within the technical limit."
> — [Chroma Research](https://research.trychroma.com/context-rot)

Jerry addresses this through:
- **Filesystem as infinite memory** - Offload state to files
- **Work Tracker** - Persistent task state across sessions
- **Skills** - Compressed instruction interfaces
- **Structured knowledge** - `docs/` hierarchy for accumulated wisdom

---

## Architecture

```
jerry/
├── .claude/                    # Agent Governance Layer
├── .claude-plugin/             # Distribution Layer
├── skills/                     # Interface Layer (Natural Language)
├── scripts/                    # Execution Layer (CLI Shims)
├── src/                        # Hexagonal Core (Python)
│   ├── domain/                 # Pure Business Logic
│   ├── application/            # Use Cases (CQRS)
│   ├── infrastructure/         # Adapters (Persistence, Messaging)
│   └── interface/              # Primary Adapters (CLI, API)
└── docs/                       # Knowledge Repository
```

### Key Design Principles

1. **Hexagonal Architecture** (Ports & Adapters)
   - Domain has no external dependencies
   - Ports define contracts, adapters implement them
   - Dependency inversion: outer depends on inner

2. **Zero-Dependency Core**
   - Python stdlib only in domain/
   - Libraries allowed in infrastructure/ if pre-installed

3. **CQRS Pattern**
   - Commands: Write operations, return events
   - Queries: Read operations, return DTOs

---

## Working with Jerry

### Project-Based Workflow

Jerry uses isolated project workspaces. Each project has its own `PLAN.md` and `WORKTRACKER.md`.

**Active Project Resolution:**
1. Set `JERRY_PROJECT` environment variable (e.g., `export JERRY_PROJECT=PROJ-001-plugin-cleanup`)
2. If not set, Claude will prompt you to specify which project to work on
3. See `projects/README.md` for the project registry

**Project Structure:**
```
projects/PROJ-{nnn}-{slug}/
├── PLAN.md              # Project implementation plan
├── WORKTRACKER.md       # Work tracking document
└── .jerry/data/items/   # Operational state (work items)
```

### Before Starting Work

1. Set `JERRY_PROJECT` environment variable for your target project
2. Check `projects/${JERRY_PROJECT}/PLAN.md` for current plan
3. Review `projects/${JERRY_PROJECT}/WORKTRACKER.md` for task state
4. Read relevant `docs/knowledge/` for domain context

### During Work

1. Use Work Tracker to persist task state to `projects/${JERRY_PROJECT}/WORKTRACKER.md`
2. Update PLAN.md as implementation progresses
3. Document decisions in `docs/design/`

### After Completing Work

1. Update Work Tracker with completion status
2. Capture learnings in `docs/experience/` or `docs/wisdom/`
3. Commit with clear, semantic messages

### Creating a New Project

1. Check `projects/README.md` for next project number
2. Create directory: `mkdir -p projects/PROJ-{nnn}-{slug}/.jerry/data/items`
3. Create `PLAN.md` and `WORKTRACKER.md`
4. Add entry to `projects/README.md`
5. Set `JERRY_PROJECT` environment variable

---

## Project Enforcement (Hard Rule)

> **Enforcement Level:** HARD
> **Principle:** P-030 - Project Context Required
> **See Also:** `docs/design/ADR-002-project-enforcement.md`

Claude **MUST NOT** proceed with any substantial work without an active project context.
This is a hard constraint enforced via the SessionStart hook.

### Hook Output Format

The `scripts/session_start.py` hook produces structured output that Claude parses:

#### `<project-context>` - Valid Project Active

```
Jerry Framework initialized. See CLAUDE.md for context.
<project-context>
ProjectActive: PROJ-001-plugin-cleanup
ProjectPath: projects/PROJ-001-plugin-cleanup/
ValidationMessage: Project is properly configured
</project-context>
```

**Action:** Proceed with work in the active project context.

#### `<project-required>` - No Project Selected

```
Jerry Framework initialized.
<project-required>
ProjectRequired: true
AvailableProjects:
  - PROJ-001-plugin-cleanup [ACTIVE]
  - PROJ-002-example [DRAFT]
NextProjectNumber: 003
ProjectsJson: [{"id": "PROJ-001-plugin-cleanup", "status": "IN_PROGRESS"}]
</project-required>

ACTION REQUIRED: No JERRY_PROJECT environment variable set.
Claude MUST use AskUserQuestion to help the user select an existing project or create a new one.
DO NOT proceed with any work until a project is selected.
```

**Action:** Use `AskUserQuestion` to help user select or create a project.

#### `<project-error>` - Invalid Project Specified

```
Jerry Framework initialized with ERROR.
<project-error>
InvalidProject: bad-format
Error: Project ID must match pattern PROJ-NNN-slug
AvailableProjects:
  - PROJ-001-plugin-cleanup [ACTIVE]
NextProjectNumber: 002
</project-error>

ACTION REQUIRED: The specified JERRY_PROJECT is invalid.
Claude MUST use AskUserQuestion to help the user select or create a valid project.
```

**Action:** Use `AskUserQuestion` to help user correct the error.

### Required AskUserQuestion Flow

When `<project-required>` or `<project-error>` is received, Claude **MUST**:

1. **Parse** the available projects from the hook output
2. **Present options** via `AskUserQuestion`:
   - List available projects (from `AvailableProjects`)
   - Offer "Create new project" option
3. **Handle response**:
   - If existing project selected → instruct user to set `JERRY_PROJECT`
   - If new project → guide through creation flow
4. **DO NOT** proceed with unrelated work until resolved

Example AskUserQuestion structure:
```yaml
question: "Which project would you like to work on?"
header: "Project"
options:
  - label: "PROJ-001-plugin-cleanup"
    description: "[ACTIVE] Plugin system cleanup and refactoring"
  - label: "Create new project"
    description: "Start a new project workspace"
```

### Project Creation Flow

When user selects "Create new project":

1. **Get project details** via AskUserQuestion:
   - Slug/name (required): e.g., "api-redesign"
   - Description (optional)

2. **Auto-generate ID** using `NextProjectNumber` from hook:
   - Format: `PROJ-{NNN}-{slug}`
   - Example: `PROJ-003-api-redesign`

3. **Create project structure**:
   ```
   projects/PROJ-003-api-redesign/
   ├── PLAN.md              # Implementation plan template
   ├── WORKTRACKER.md       # Work tracking document
   └── .jerry/data/items/   # Operational state
   ```

4. **Update registry**: Add entry to `projects/README.md`

5. **Instruct user**: Set `JERRY_PROJECT=PROJ-003-api-redesign`

---

## Skills Available

| Skill | Purpose | Location |
|-------|---------|----------|
| `worktracker` | Task/issue management | `skills/worktracker/SKILL.md` |
| `architecture` | System design guidance | `skills/architecture/SKILL.md` |
| `problem-solving` | Domain use case invocation | `skills/problem-solving/SKILL.md` |

---

## Agents Available

See `AGENTS.md` for the full registry. Agents are scoped to skills:

| Skill | Agents | Location |
|-------|--------|----------|
| problem-solving | 8 specialists (researcher, analyst, synthesizer, etc.) | `skills/problem-solving/agents/` |

Invoke agents via the `/problem-solving` skill.

---

## Code Standards

See `.claude/rules/coding-standards.md` for enforced rules.

Quick reference:
- Python 3.11+ with type hints
- 100 character line limit
- Domain layer: NO external imports
- All public functions: docstrings required

---

## CLI Commands (v0.1.0)

> **Version**: 0.1.0 (Breaking changes from v0.0.1)
> **Reference**: `ADR-CLI-002-namespace-implementation.md`

Jerry CLI is organized into bounded-context-aligned namespaces:

### Session Namespace

Manage agent sessions for context tracking.

```bash
jerry session start [--name NAME] [--description DESC]  # Start new session
jerry session end [--summary TEXT]                       # End current session
jerry session status                                     # Show session status
jerry session abandon [--reason TEXT]                    # Abandon without summary
```

### Items Namespace

Manage work items (tasks, bugs, stories).

```bash
jerry items list [--status STATUS] [--type TYPE]        # List work items
jerry items show <id>                                    # Show item details
jerry items create <title> [--type TYPE]                # Create item (Phase 4.5)
jerry items start <id>                                   # Start work (Phase 4.5)
jerry items complete <id>                                # Complete item (Phase 4.5)
```

**Note**: `create`, `start`, `complete` commands are deferred to Phase 4.5 (Event Sourcing).

### Projects Namespace

Manage Jerry projects.

```bash
jerry projects context                                   # Show project context
jerry projects list                                      # List all projects
jerry projects validate <project-id>                     # Validate project
```

### Global Options

```bash
jerry --help                                             # Show help
jerry --version                                          # Show version
jerry --json <namespace> <command>                       # JSON output
```

### Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | Error (validation failure, not found, etc.) |
| 2 | Invalid usage (bad arguments) |

---

## Agent Governance (Jerry Constitution)

All agents operating within Jerry MUST adhere to the **Jerry Constitution v1.0**.

**Location:** `docs/governance/JERRY_CONSTITUTION.md`

### Core Principles (Quick Reference)

| ID | Principle | Enforcement |
|----|-----------|-------------|
| P-001 | Truth and Accuracy | Soft |
| P-002 | File Persistence | Medium |
| P-003 | No Recursive Subagents | **Hard** |
| P-010 | Task Tracking Integrity | Medium |
| P-020 | User Authority | **Hard** |
| P-022 | No Deception | **Hard** |

### Hard Principles (Cannot Override)

1. **P-003**: Maximum ONE level of agent nesting (orchestrator → worker)
2. **P-020**: User has ultimate authority; never override user decisions
3. **P-022**: Never deceive users about actions, capabilities, or confidence

### Self-Critique Protocol

Before finalizing significant outputs, agents SHOULD self-critique:

```
1. P-001: Is my information accurate and sourced?
2. P-002: Have I persisted significant outputs?
3. P-004: Have I documented my reasoning?
4. P-010: Is WORKTRACKER updated?
5. P-022: Am I being transparent about limitations?
```

### Behavioral Validation

Constitution compliance is validated via `docs/governance/BEHAVIOR_TESTS.md`:
- 18 test scenarios (golden dataset)
- LLM-as-a-Judge evaluation (industry standard per DeepEval, Datadog)
- Happy path, edge case, and adversarial coverage

**Industry Prior Art:**
- [Anthropic Constitutional AI](https://www.anthropic.com/research/constitutional-ai-harmlessness-from-ai-feedback)
- [OpenAI Model Spec](https://model-spec.openai.com/2025-12-18.html)
- [DeepEval G-Eval](https://deepeval.com/docs/metrics-llm-evals)

---

## References

- [Hexagonal Architecture](https://alistair.cockburn.us/hexagonal-architecture/) - Alistair Cockburn
- [Context Engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) - Anthropic
- [Context Rot Research](https://research.trychroma.com/context-rot) - Chroma
