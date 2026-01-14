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

## Worktracker

<worktracker>

| Generic Term (Ontology) | Definition                                 | Relationship (Parent of...)    | SAFe Terminology          | Azure DevOps (Scrum)       | Jira (Standard) | Jira (Adv. Roadmaps) |
|-------------------------|--------------------------------------------|--------------------------------|---------------------------|----------------------------|-----------------|----------------------|
| Strategic Theme         | High-level business goal or category.      | Tags/Labels (Non-hierarchical) | Strategic Theme           | Tag / Value Area           | Label           | Theme                |
| Initiative              | Large-scale endeavor spanning teams/years. | Solution Epic                  | Solution / Large Solution | Custom Initiative          | N/A             | Initiative           |
| Solution Epic           | Major solution capability (6+ months).     | Feature                        | Portfolio Epic            | Epic                       | N/A             | Legend / High Epic   |
| Feature                 | Distinct functionality (1-3 months).       | Story (Unit of Work)           | Feature                   | Feature                    | Epic            | Epic                 | 
| Unit of Work            | Atomic value deliverable (INVEST).         | Task (Effort)                  | User Story                | Product Backlog Item (PBI) | Story           | Story                |
| Enabler                 | Technical work item (non-user value).      | Task (Effort)                  | Enabler Story             | PBI (tagged Arch)          | Task            | Task                 |
| Task (Effort)           | Atomic unit of labor/effort.               | None (Leaf Node)               | Task                      | Task                       | Sub-task        | Sub-task             |

We use the Generic Term (Ontology) for all work items in our project documentation and tracking artifacts. The SAFe Terminology, Azure DevOps (Scrum) and Jira (Standard/Adv. Roadmaps) columns are provided for reference to map our ontology to common frameworks and tools.
`WORKTRACKER.md` is the Global Manifest tracking all Initiatives, Solution Epic, Feature, Unit of Work, Enabler and Task (Effort). It exists in the root of the project folder ({ProjectId} e.g. `PROJ-005-plugin-bugs`). It is a pointer with relationships to all decomposed work items in `work/` folder. 
A folder is created for each Solution Epic (`{SolutionEpicId}-{slug}`) in the `work/` folder. Each Solution Epic folder contains its own `SOLUTION-WORKTRACKER.md` tracking Features, Unit of Work, Enablers and Tasks (Effort) for that Strategic Theme. It is a pointer with relationships to all respective artifacts of the Solution Epic. 
A folder is created for each Feature in the `work/{SolutionEpicId}-{slug}/` folder. Each Feature folder contains its own `FEATURE-WORKTRACKER.md` tracking Unit of Work, Enablers and Tasks (Effort) for that Feature. Each `FEATURE-WORKTRACKER.md` must have and maintain relationships to related artifacts in-order to enable traceability and auditability as well as easier traversal for you - it is a pointer with relationships to all respective artifacts of the Feature. 
A file is created for each Unit of Work and Enabler in the `work/{SolutionEpicId}-{slug}/{FeatureId}-{slug}/` folder. Each Unit of Work and Enabler file contains its own `wi-{UnitOfWorkId}.md` or `en-{EnablerId}.md` tracking Tasks (Effort) for that Unit of Work or Enabler. All Tasks must have verifiable evidence before a Unit of Work or Enabler can be Closed.
A file is created for each Bug, Discovery, Decision and Tech Debt in the `work/{SolutionEpicId}-{slug}/{FeatureId}-{slug}/` folder. Each artifact plays a critical role and must have and maintain relationships to related artifacts in-order to enable traceability and auditability as well as easier traversal for you. We need detailed artifacts in-order at act as evidence in supporting the decision-making process before closing out Tasks, Units of work and Enablers.
Each Unit of Work and Enabler File must be broken down into detailed tasks with verifiable acceptance criteria. Verifiable evidence (citations, references and sources) must be provided to support closing out a Task. Each Unit of Work or Enabler must have and maintain relationships to related artifacts in-order to enable traceability and auditability as well as easier traversal for you.
Task must be broken down into detailed tasks with verifiable acceptance criteria. Verifiable evidence (citations, references and sources) must be provided to support closing out a Task. Each Unit of Work or Enabler must have and maintain relationships to related artifacts in-order to enable traceability and auditability as well as easier traversal for you.

Each Task must be broken down into detailed tasks with verifiable acceptance criteria. Verifiable evidence (citations, references and sources) must be provided to support closing out a Task. Each Unit of Work or Enabler must have and maintain relationships to related artifacts in-order to enable traceability and auditability as well as easier traversal for you.
Technical Debut, Bugs and Discoveries must be documented as individual `td-{UnitOfWorkId}-{slug}.md`, `bug-{UnitOfWorkId}-{slug}.md`, `disc-{UnitOfWorkId}-{slug}.md` files in the `work/{SolutionEpicId}/{FeatureId}/` folder as they are discovered. Each Technical Debut, Bug or Discovery file must have and maintain relationships to related artifacts in-order to enable traceability and auditability as well as easier traversal for you. Each discovery, bug or technical debut must have verifiable evidence before it can be Closed.

Use MCP Memory-Keeper to help you remember and maintain the structure and relationships of the Worktracker system. You don't have to remember everything, just remember to use MCP Memory-Keeper to help you keep track of everything. Try MCP Memory-Keeper first before searching the repository.

Worktracker Directory Structure:
```
projects/
└── {ProjectId} e.g. PROJ-005-plugin-bugs                                                       # Project Context Folder
    ├── PLAN.md                                                                                 # Initial Project Plan and Overview. 
    ├── WORKTRACKER.md                                                                          # Global Manifest tracking all work items. Pointer with relationships to all decomposed work items.
    └── work/                                                                                   # Project Worktracker Decomposition Folder      
        └── {SolutionEpicId}-{slug} e.g. SE-001-plugin-installation-fixes                       # Solution Epic Folder
            ├── SOLUTION-WORKTRACKER.md                                                         # Solution Epic Worktracker tracking Features, Unit of Work, Enablers and Tasks. Pointer with relationships to all respective artifacts of the Solution Epic.
            ├── plans/                                                                          # Folder for plans that we generate while working in the Solution Epic. As we work through the project and enouncter complexity we generate plans to help us navigate the complexity.
            │   └── PLAN-{PlanId}-{slug}.md e.g. PLAN-001-holy-lazer-cats.md                    # Plan that we generate anytime we have to do something complicated. References the respective Strategic Theme, Initiative, Solution Epic, Feature, Unit of Work, Enabler and/or Task. Also referenced by the respective Strategic Theme, Initiative, Solution Epic, Feature, Unit of Work, Enabler and/or Task to easily and effectively traverse.
            └── {FeatureId}-{slug} e.g. FT-001-manifest-validation-fixes                        # Feature Folder
                ├── FEATURE-WORKTRACKER.md                                                      # Feature Worktracker tracking Unit of Work, Enablers and Tasks. Pointer with relationships to all respective artifacts of the Feature.
                ├── dec-{DecisionId}.md e.g. en-001-fix-plugin-json.md                          # Decision File tracking Q&A sessions verbatim + your summaries (what you extract). Acts as Glue for our session to know what we have decided on. Contains relationships to related artifacts.
                ├── en-{EnablerId}.md e.g. en-001-fix-plugin-json.md                            # Enabler File tracking Tasks. Must have verifiable evidence before Enabler can be Closed. Contains relationships to related artifacts.
                ├── wi-{UnitOfWorkId}.md e.g. wi-001-detection-playbook.md                      # Unit of Work File tracking Tasks. Must have verifiable evidence before Unit of Work can be Closed. Contains relationships to related artifacts.
                ├── bug-{BugId}-{slug}.md e.g. bug-001-plugin-json-errors.md                    # Bug File documenting identified bugs. Enablers or Units of Work MUST be created to address documented bugs. Contains relationships to related artifacts.
                ├── disc-{DiscoveryId}-{slug}.md e.g. disc-001-manifest-validation-insights.md  # Discovery File documenting discoveries made. Discoveries MAY lead to creation of Enablers or Units of Work. Contains relationships to related artifacts.
                └── td-{TechDebtWorkId}-{slug}.md e.g. td-001-lack-of-tests.md                  # Technical Debt File documenting technical debt identified. Enablers or Units of Work MUST be created to address documented technical debt. Contains relationships to related artifacts.
```
</worktracker>

<todo>
Required Behavior:
- todo.1. -> Keep a META TODO item (MUST ALWAYS BE ON LIST) reminding you are in project {JerryProjectId}
- todo.2. -> Keep a META TODO item (MUST ALWAYS BE ON LIST) reminding you to update the `*-WORKTRACKER.md` files.
- todo.3. -> Keep a META TODO item (MUST ALWAYS BE ON LIST) reminding you to capture and update decisions in the `dec-*.md` files with detailed updates as YOU and I go through Questions and Answers.
- todo.4. -> Keep a META TODO item (MUST ALWAYS BE ON LIST) reminding you to update your respective Unit of Work and Enabler `*.md` files with detailed updates as you are working/progressing through them.
- todo.5. -> Keep a META TODO item (MUST ALWAYS BE ON LIST) reminding you to document detailed bugs, discoveries and technical debut as they are discovered in their respective `*.md` files.
- todo.6. -> Keep a META TODO item (MUST ALWAYS BE ON LIST) reminding you to Keep your TODO list up to date.                                                                                                                                                                                                                                                
- todo.7. -> Keep a META TODO item (MUST ALWAYS BE ON LIST) reminding you to Keep your TODO list in sync with your `*-WORKTRACKER.md` and Units of Work.  You MUST keep your TODO in sync with the work-tracker.                                                                                                                                                     
- todo.8. -> You MUST keep your TODO in sync with the work-tracker showing the previous Features, current Feature and next Feature -> the current Feature MUST show all Units of Work || Enablers -> the current Unit of Work || Enabler must show all Tasks. TODO List MUST survive compaction and provide high fidelity.
- todo.9. -> You MUST keep your TODO in sync with the orchestration plan showing the previous phase, current phase and next phase -> current phase must show all tasks/subagents
<todo>


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
| `orchestration` | Multi-agent workflow coordination | `skills/orchestration/SKILL.md` |

### Orchestration Skill

For multi-agent workflows requiring cross-pollinated pipelines, sync barriers, or state checkpointing, use the **orchestration** skill. The skill provides:

- **ORCHESTRATION_PLAN.md** - Strategic context with ASCII workflow diagrams
- **ORCHESTRATION_WORKTRACKER.md** - Tactical execution tracking
- **ORCHESTRATION.yaml** - Machine-readable state (SSOT)

Activate with: "orchestration", "multi-agent workflow", "cross-pollinated pipeline", "sync barrier"

See `skills/orchestration/PLAYBOOK.md` for step-by-step workflow guidance.

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
