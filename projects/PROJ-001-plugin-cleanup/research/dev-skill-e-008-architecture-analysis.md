# Development Skill Architecture Analysis

**Document ID**: dev-skill-e-008-architecture-analysis
**Date**: 2026-01-09
**Author**: ps-analyst (Architecture)

---

## Executive Summary

This architecture analysis maps the 37 patterns identified in the dev-skill research synthesis (e-007) to Jerry's hexagonal architecture layers. The analysis provides a component-level design for the development skill, ensuring clean architecture principles are maintained while supporting the full workflow from task planning through code generation, quality validation, and review.

The development skill architecture follows the Ports & Adapters (Hexagonal) pattern, with clear separation between:
- **Domain Layer**: Pure business logic for development workflows, quality gates, and task management
- **Application Layer**: Use cases implementing CQRS pattern for commands and queries
- **Infrastructure Layer**: Adapters for persistence, external tools, and agent execution
- **Interface Layer**: CLI commands, skill interface, and agent protocol handlers

---

## Hexagonal Architecture Mapping

### Domain Layer Components

The domain layer contains pure business logic with NO external dependencies (stdlib only per Jerry coding standards).

#### Entities

| Entity | Description | Source Patterns |
|--------|-------------|-----------------|
| `WorkItem` | Aggregate root for development tasks | PAT-003-e006 (Agent Task Schema), PAT-001-e006 (DoD Checklist) |
| `QualityGate` | Quality gate configuration and state | PAT-001-e002 (Layered Gate), PAT-005-e002 (Agent Guardrails) |
| `ReviewSession` | Code review session tracking | PAT-001-e004 (Health-Over-Perfection), PAT-003-e004 (Tiered Rigor) |
| `TestSuite` | Test specification and results | PAT-001-e003 (Test-First Protocol), PAT-005-e003 (Layered Test Strategy) |
| `ArchitectureDecision` | ADR record | PAT-005-e004 (ADR-Governed Architecture) |

```
src/development/domain/
├── entities/
│   ├── __init__.py
│   ├── work_item.py              # Task/story/epic aggregate
│   ├── quality_gate.py           # Gate configuration
│   ├── review_session.py         # Review tracking
│   ├── test_suite.py             # Test specification
│   └── architecture_decision.py  # ADR entity
```

#### Value Objects

| Value Object | Description | Source Patterns |
|--------------|-------------|-----------------|
| `TaskStatus` | Enum: backlog, ready, in_progress, review, done, cancelled | PAT-003-e006 |
| `Priority` | Enum: critical, high, medium, low | PAT-003-e006 |
| `RiskTier` | Enum: T1 (low), T2 (medium), T3 (high), T4 (critical) | PAT-003-e004 (Tiered Rigor) |
| `AcceptanceCriterion` | Given-When-Then specification | PAT-004-e003 (BDD as Specification) |
| `SuccessCriterion` | Automated validation rule | PAT-004-e006 (Success Criteria Schema) |
| `DependencyGraph` | DAG of task dependencies | PAT-003-e006 |
| `SnowflakeId` | Coordination-free unique identifier | PAT-004-e005 (Coordination-Free ID) |
| `FileVersion` | Content hash for optimistic concurrency | PAT-003-e005 (Optimistic Concurrency) |

```
src/development/domain/
├── value_objects/
│   ├── __init__.py
│   ├── task_status.py
│   ├── priority.py
│   ├── risk_tier.py
│   ├── acceptance_criterion.py
│   ├── success_criterion.py
│   ├── dependency_graph.py
│   ├── snowflake_id.py
│   └── file_version.py
```

#### Domain Events

| Event | Trigger | Source Patterns |
|-------|---------|-----------------|
| `WorkItemCreated` | New task added | PAT-003-e006 |
| `WorkItemStatusChanged` | Status transition | PAT-003-e006, c-010 (Task Tracking) |
| `TestsGenerated` | Agent generates tests | PAT-001-e003 (Test-First Protocol) |
| `CodeGenerated` | Agent generates code | PAT-001-e003 |
| `QualityGatePassed` | Gate validation succeeded | PAT-001-e002 |
| `QualityGateFailed` | Gate validation failed | PAT-001-e002 |
| `ReviewRequested` | Code ready for review | PAT-001-e004 |
| `ReviewCompleted` | Review finished | PAT-006-e004 (Iterative Feedback) |
| `HumanApprovalRequired` | High-risk action needs approval | PAT-006-e001 (Human-in-the-Loop) |

```
src/development/domain/
├── events/
│   ├── __init__.py
│   ├── work_item_events.py
│   ├── test_events.py
│   ├── quality_events.py
│   └── review_events.py
```

#### Domain Services

| Service | Responsibility | Source Patterns |
|---------|----------------|-----------------|
| `TaskDecompositionService` | Break epics into stories/tasks | PAT-002-e006 (WBS Decomposition), PAT-005-e006 (Vertical Slicing) |
| `QualityGateEvaluator` | Evaluate gate conditions | PAT-001-e002, PAT-003-e002 (SLO-Based Gates) |
| `RiskAssessmentService` | Classify change risk tier | PAT-003-e004 (Tiered Review Rigor) |
| `DependencyResolver` | Topological sort of task DAG | PAT-003-e006 |

```
src/development/domain/
├── services/
│   ├── __init__.py
│   ├── task_decomposition.py
│   ├── quality_gate_evaluator.py
│   ├── risk_assessment.py
│   └── dependency_resolver.py
```

### Application Layer Components

The application layer implements use cases using CQRS pattern. Commands return domain events; queries return DTOs.

#### Commands

| Command | Description | Source Patterns |
|---------|-------------|-----------------|
| `CreateWorkItemCommand` | Create new task/story | PAT-003-e006 |
| `UpdateWorkItemStatusCommand` | Transition status | PAT-003-e006 |
| `GenerateTestsCommand` | Trigger test generation | PAT-001-e003 (Test-First Protocol) |
| `GenerateCodeCommand` | Trigger code generation | PAT-001-e003 |
| `ExecuteQualityGateCommand` | Run gate validation | PAT-001-e002 |
| `RequestReviewCommand` | Submit for code review | PAT-001-e004 |
| `CompleteReviewCommand` | Finish review with verdict | PAT-006-e004 |
| `ApproveHighRiskActionCommand` | Human approval for gated action | PAT-006-e001 |
| `CreateADRCommand` | Create architecture decision record | PAT-005-e004 |

```
src/development/application/
├── commands/
│   ├── __init__.py
│   ├── work_item_commands.py
│   ├── generation_commands.py
│   ├── quality_commands.py
│   ├── review_commands.py
│   └── adr_commands.py
```

#### Queries

| Query | Description | Returns |
|-------|-------------|---------|
| `GetWorkItemQuery` | Retrieve work item by ID | `WorkItemDTO` |
| `ListWorkItemsQuery` | List with filters/pagination | `WorkItemListDTO` |
| `GetReadyTasksQuery` | Tasks ready for execution | `TaskListDTO` |
| `GetQualityGateStatusQuery` | Current gate status | `QualityGateStatusDTO` |
| `GetReviewSessionQuery` | Review session details | `ReviewSessionDTO` |
| `SearchADRsQuery` | Search architecture decisions | `ADRListDTO` |

```
src/development/application/
├── queries/
│   ├── __init__.py
│   ├── work_item_queries.py
│   ├── quality_queries.py
│   ├── review_queries.py
│   └── adr_queries.py
```

#### Command Handlers

| Handler | Ports Used | Source Patterns |
|---------|------------|-----------------|
| `CreateWorkItemHandler` | `IWorkItemRepository`, `IIdGenerator` | PAT-003-e006, PAT-004-e005 |
| `GenerateTestsHandler` | `ICodeGenerationPort`, `ITestRunnerPort` | PAT-001-e003 |
| `GenerateCodeHandler` | `ICodeGenerationPort`, `IQualityGatePort` | PAT-001-e003 |
| `ExecuteQualityGateHandler` | `IQualityGatePort`, `IEventPublisher` | PAT-001-e002 |
| `RequestReviewHandler` | `IReviewRepository`, `IRiskAssessmentPort` | PAT-001-e004, PAT-003-e004 |

```
src/development/application/
├── handlers/
│   ├── commands/
│   │   ├── __init__.py
│   │   ├── work_item_handlers.py
│   │   ├── generation_handlers.py
│   │   ├── quality_handlers.py
│   │   └── review_handlers.py
│   └── queries/
│       ├── __init__.py
│       ├── work_item_query_handlers.py
│       ├── quality_query_handlers.py
│       └── review_query_handlers.py
```

#### Application Services

| Service | Responsibility | Source Patterns |
|---------|----------------|-----------------|
| `DevelopmentWorkflowService` | Orchestrate Red-Green-Refactor | PAT-001-e003 |
| `QualityOrchestrationService` | Coordinate layered gates | PAT-001-e002 |
| `ReviewCoordinationService` | Manage iterative review cycles | PAT-006-e004 |
| `ContextCompactionService` | Pre-rot context management | PAT-004-e001 |

```
src/development/application/
├── services/
│   ├── __init__.py
│   ├── development_workflow.py
│   ├── quality_orchestration.py
│   ├── review_coordination.py
│   └── context_compaction.py
```

#### Ports (Interfaces)

**Secondary Ports (Driven/Output):**

| Port | Purpose | Source Patterns |
|------|---------|-----------------|
| `IWorkItemRepository` | Work item persistence | PAT-001-e005 (Atomic Write) |
| `ICodeGenerationPort` | Agent code generation | PAT-001-e003, PAT-001-e001 (Conductor-Worker) |
| `ITestRunnerPort` | Test execution | PAT-001-e003 |
| `IQualityGatePort` | Quality gate execution | PAT-001-e002 |
| `IReviewRepository` | Review session persistence | PAT-001-e004 |
| `IIdGenerator` | Unique ID generation | PAT-004-e005 |
| `IFileLockPort` | File-level locking | PAT-002-e005 (File-Based Mutual Exclusion) |
| `IContextStorePort` | Context persistence | PAT-008-e001 (Rules-as-Files) |
| `IEventPublisher` | Domain event publication | Standard CQRS |

```
src/development/application/
├── ports/
│   ├── __init__.py
│   ├── repository_ports.py      # IWorkItemRepository, IReviewRepository
│   ├── generation_ports.py      # ICodeGenerationPort
│   ├── execution_ports.py       # ITestRunnerPort, IQualityGatePort
│   ├── infrastructure_ports.py  # IIdGenerator, IFileLockPort
│   └── messaging_ports.py       # IEventPublisher, IContextStorePort
```

### Infrastructure Layer Components

Infrastructure adapters implement the ports defined in the application layer.

#### Persistence Adapters

| Adapter | Implements | Source Patterns |
|---------|------------|-----------------|
| `FileSystemWorkItemAdapter` | `IWorkItemRepository` | PAT-001-e005, PAT-002-e005 |
| `FileSystemReviewAdapter` | `IReviewRepository` | PAT-001-e005 |
| `FileSystemADRAdapter` | `IADRRepository` | PAT-005-e004 |

```
src/development/infrastructure/
├── adapters/
│   ├── persistence/
│   │   ├── __init__.py
│   │   ├── filesystem_work_item_adapter.py
│   │   ├── filesystem_review_adapter.py
│   │   └── filesystem_adr_adapter.py
```

#### External Service Adapters

| Adapter | Implements | Description |
|---------|------------|-------------|
| `ClaudeCodeGenerationAdapter` | `ICodeGenerationPort` | Claude agent for code/test generation |
| `PytestRunnerAdapter` | `ITestRunnerPort` | pytest execution |
| `HypothesisTestAdapter` | `ITestRunnerPort` | Property-based testing (PAT-002-e003) |
| `PreCommitQualityAdapter` | `IQualityGatePort` | Pre-commit hook execution |
| `RuffLinterAdapter` | `IQualityGatePort` | Python linting |
| `CoverageGateAdapter` | `IQualityGatePort` | Coverage threshold validation |

```
src/development/infrastructure/
├── adapters/
│   ├── generation/
│   │   ├── __init__.py
│   │   └── claude_generation_adapter.py
│   ├── testing/
│   │   ├── __init__.py
│   │   ├── pytest_runner_adapter.py
│   │   └── hypothesis_adapter.py
│   ├── quality/
│   │   ├── __init__.py
│   │   ├── precommit_adapter.py
│   │   ├── ruff_adapter.py
│   │   └── coverage_adapter.py
```

#### File System Adapters

| Adapter | Implements | Source Patterns |
|---------|------------|-----------------|
| `PyFileLockAdapter` | `IFileLockPort` | PAT-002-e005 (File-Based Mutual Exclusion) |
| `AtomicWriteAdapter` | Internal | PAT-001-e005 (Atomic Write with Durability) |
| `SnowflakeIdAdapter` | `IIdGenerator` | PAT-004-e005 (Coordination-Free ID) |
| `GitWorktreeAdapter` | `IWorkspaceIsolationPort` | PAT-002-e001, PAT-005-e005 (Workspace Separation) |

```
src/development/infrastructure/
├── adapters/
│   ├── filesystem/
│   │   ├── __init__.py
│   │   ├── filelock_adapter.py
│   │   ├── atomic_write.py
│   │   ├── snowflake_id_adapter.py
│   │   └── git_worktree_adapter.py
```

### Interface Layer Components

The interface layer handles external format translation and provides entry points.

#### CLI Commands

| Command | Description | Source Patterns |
|---------|-------------|-----------------|
| `dev task create` | Create new work item | PAT-003-e006 |
| `dev task list` | List work items | PAT-003-e006 |
| `dev task status` | Update task status | PAT-003-e006 |
| `dev generate tests` | Generate tests for task | PAT-001-e003 |
| `dev generate code` | Generate code for task | PAT-001-e003 |
| `dev gate run` | Execute quality gate | PAT-001-e002 |
| `dev review request` | Submit for review | PAT-001-e004 |
| `dev adr create` | Create ADR | PAT-005-e004 |

```
src/development/interface/
├── cli/
│   ├── __init__.py
│   ├── task_commands.py
│   ├── generation_commands.py
│   ├── quality_commands.py
│   ├── review_commands.py
│   └── adr_commands.py
```

#### Skill Interface

| Interface | Description | Source Patterns |
|-----------|-------------|-----------------|
| `DevSkillHandler` | Natural language command routing | Jerry skill pattern |
| `TaskTemplateParser` | Parse task specifications | PAT-003-e006 |
| `GherkinParser` | Parse acceptance criteria | PAT-004-e003 |

```
src/development/interface/
├── skill/
│   ├── __init__.py
│   ├── dev_skill_handler.py
│   ├── task_template_parser.py
│   └── gherkin_parser.py
```

#### Agent Interfaces

| Interface | Description | Source Patterns |
|-----------|-------------|-----------------|
| `AgentTaskProtocol` | Structured task input/output | PAT-003-e006 |
| `AgentHandoffProtocol` | State handoff between agents | PAT-005-e001 (Explicit State Handoff) |
| `HumanGateProtocol` | Human-in-the-loop interaction | PAT-006-e001 |

```
src/development/interface/
├── agent/
│   ├── __init__.py
│   ├── task_protocol.py
│   ├── handoff_protocol.py
│   └── human_gate_protocol.py
```

---

## Component Interactions

### Sequence Diagram: Test-First Development Workflow

```
User              DevSkill        WorkflowSvc      CodeGenPort      TestRunner      QualityGate
  |                   |                |                |               |               |
  |--[dev task]------>|                |                |               |               |
  |                   |--[parse]------>|                |               |               |
  |                   |                |                |               |               |
  |                   |       [Create WorkItem]         |               |               |
  |                   |<--[WorkItemCreated]-------------|               |               |
  |                   |                |                |               |               |
  |--[dev generate tests]------------->|                |               |               |
  |                   |                |--[GenerateTests]-------------->|               |
  |                   |                |                |               |               |
  |                   |                |<--[TestsGenerated]-------------|               |
  |                   |                |                |               |               |
  |                   |                |--[RunTests]------------------>|               |
  |                   |                |<--[TestsFailed (RED)]---------|               |
  |                   |                |                |               |               |
  |--[dev generate code]-------------->|                |               |               |
  |                   |                |--[GenerateCode]--------------->|               |
  |                   |                |<--[CodeGenerated]-------------|               |
  |                   |                |                |               |               |
  |                   |                |--[RunTests]------------------>|               |
  |                   |                |<--[TestsPassed (GREEN)]-------|               |
  |                   |                |                |               |               |
  |                   |                |--[ExecuteGate]------------------------------>|
  |                   |                |<--[GatePassed]------------------------------ |
  |                   |                |                |               |               |
  |<--[Task Complete]-|<---------------|                |               |               |
```

### Sequence Diagram: Quality Gate Cascade

```
Developer         QualityOrch      PreCommit        Linter          Coverage        Tests
    |                 |                |               |                |              |
    |--[commit]------>|                |               |                |              |
    |                 |                |               |                |              |
    |                 |--[Layer 1: Local]------------->|               |              |
    |                 |<--[secrets-check: PASS]--------|               |              |
    |                 |<--[format-check: PASS]---------|               |              |
    |                 |                |               |                |              |
    |                 |--[Layer 2: Lint]---------------------------->|              |
    |                 |<--[ruff: PASS]------------------------------|              |
    |                 |                |               |                |              |
    |                 |--[Layer 3: Coverage]---------------------------------->|     |
    |                 |<--[80%+ achieved: PASS]-------------------------------|     |
    |                 |                |               |                |              |
    |                 |--[Layer 4: Tests]---------------------------------------------->|
    |                 |<--[All tests pass: PASS]---------------------------------------|
    |                 |                |               |                |              |
    |<--[Gate Cascade PASSED]---------|               |                |              |
```

### Sequence Diagram: Tiered Review with Human-in-the-Loop

```
Developer        RiskAssess       ReviewCoord      ReviewAgent      Human          ADRStore
    |                 |                |                |             |                |
    |--[request review]-------------->|                |             |                |
    |                 |                |                |             |                |
    |                 |<--[assess risk]|                |             |                |
    |                 |--[T3: HIGH]-->|                |             |                |
    |                 |                |                |             |                |
    |                 |                |--[Check ADRs]------------------------------>|
    |                 |                |<--[Relevant ADRs]---------------------------|
    |                 |                |                |             |                |
    |                 |                |--[Agent Review]------------>|             |
    |                 |                |<--[Review Comments]---------|             |
    |                 |                |                |             |                |
    |                 |                |--[Human Gate (T3)]------------------------>|
    |                 |                |<--[Approval]-------------------------------|
    |                 |                |                |             |                |
    |<--[Review Complete: APPROVED]---|                |             |                |
```

### Data Flow Analysis

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              DATA FLOW DIAGRAM                                   │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                  │
│  ┌──────────────┐     ┌──────────────┐     ┌──────────────┐     ┌────────────┐ │
│  │   INTERFACE  │     │  APPLICATION │     │    DOMAIN    │     │INFRASTRUCTURE│
│  │    LAYER     │     │    LAYER     │     │    LAYER     │     │   LAYER    │ │
│  └──────────────┘     └──────────────┘     └──────────────┘     └────────────┘ │
│         │                    │                    │                    │        │
│         │   TaskInput        │                    │                    │        │
│  User ─>├──(JSON/CLI)──────>├──Command DTO──────>├──Entity Ops───────>│        │
│         │                    │                    │                    │        │
│         │                    │                    │   Domain Events    │        │
│         │                    │<───────────────────┼<───────────────────┤        │
│         │                    │                    │                    │        │
│         │                    │   Query DTO        │                    │        │
│         │<───(JSON/CLI)─────┼<───────────────────┤                    │        │
│         │                    │                    │                    │        │
│         │                    │                    │   Port Calls       │        │
│         │                    │                    ├──────────────────>├──┐     │
│         │                    │                    │                    │  │FS   │
│         │                    │                    │                    │  │Git  │
│         │                    │                    │                    │  │Agent│
│         │                    │                    │<──Adapter Response─┤<─┘     │
│         │                    │                    │                    │        │
└─────────────────────────────────────────────────────────────────────────────────┘

Data Transformations:
1. Interface -> Application: Raw input parsed to Command/Query DTOs
2. Application -> Domain: DTOs validated and converted to domain operations
3. Domain -> Infrastructure: Domain calls ports; adapters translate to external systems
4. Infrastructure -> Domain: External responses converted to domain types
5. Domain -> Application: Domain events and query results returned
6. Application -> Interface: DTOs formatted for output (JSON, CLI, etc.)
```

---

## Pattern Application

### Full Pattern Mapping Table

| Pattern | Layer | Component | Implementation Notes |
|---------|-------|-----------|---------------------|
| PAT-001-e001 (Conductor-Worker) | Application | `DevelopmentWorkflowService` | Orchestrates specialized handlers for planning, coding, testing, review |
| PAT-002-e001 (Git Worktree Isolation) | Infrastructure | `GitWorktreeAdapter` | Each parallel agent gets isolated worktree; merge on completion |
| PAT-003-e001 (Handle Pattern) | Infrastructure | `ContextStoreAdapter` | Store large artifacts as files, keep references in context |
| PAT-004-e001 (Pre-Rot Compaction) | Application | `ContextCompactionService` | Trigger at 25% context limit; summarize old turns |
| PAT-005-e001 (Explicit State Handoff) | Interface | `AgentHandoffProtocol` | Typed Command objects with explicit state deltas |
| PAT-006-e001 (Human-in-the-Loop) | Interface | `HumanGateProtocol` | Interrupt for approval on T3/T4 risk actions |
| PAT-007-e001 (Layered Guardrails) | Application | `QualityOrchestrationService` | Input, planning, execution, output guardrails |
| PAT-008-e001 (Rules-as-Files) | Infrastructure | `FileSystemContextAdapter` | Rules stored in `.jerry/rules/`, version controlled |
| PAT-001-e002 (Layered Gate Architecture) | Application | `QualityOrchestrationService` | Local -> PR -> Pre-deploy -> Post-deploy gates |
| PAT-002-e002 (Shift-Left Gates) | Application | `QualityOrchestrationService` | Gate at every stage, not just end |
| PAT-003-e002 (SLO-Based Gates) | Domain | `QualityGateEvaluator` | SLO conditions as gate criteria |
| PAT-004-e002 (DoD as Gate) | Domain | `WorkItem.definition_of_done` | Checklist items validated as gates |
| PAT-005-e002 (Agent Guardrails) | Application | `QualityOrchestrationService` | Separate planning from execution |
| PAT-006-e002 (Auto-Deploy with Rollback) | Infrastructure | ~~`DeploymentAdapter`~~ | **OUT OF SCOPE** - Deferred post-MVP (c-011 compliance) |
| PAT-001-e003 (Test-First Protocol) | Application | `DevelopmentWorkflowService` | HARD CONSTRAINT: tests before code |
| PAT-002-e003 (Property-Based Testing) | Infrastructure | `HypothesisTestAdapter` | Hypothesis for stateful invariants |
| PAT-003-e003 (Multi-Agent Isolation) | Infrastructure | `GitWorktreeAdapter` | Each agent in isolated workspace |
| PAT-004-e003 (BDD as Specification) | Interface | `GherkinParser` | Parse Given-When-Then to tests |
| PAT-005-e003 (Layered Test Strategy) | Domain | `TestSuite` | Unit < Agent < Integration < E2E |
| PAT-006-e003 (Mutation Testing) | Infrastructure | ~~`MutationTestAdapter`~~ | **PHASE 5 BACKLOG** - Enhancement not MVP (c-011) |
| PAT-001-e004 (Health-Over-Perfection) | Domain | `ReviewSession.evaluate()` | Approve if improves health |
| PAT-002-e004 (Data-Driven Resolution) | Domain | `ReviewSession.resolve_conflict()` | Facts > preferences |
| PAT-003-e004 (Tiered Review Rigor) | Domain | `RiskAssessmentService` | T1-T4 based on change risk |
| PAT-004-e004 (Sponsor-First Leadership) | Interface | Review comments | Teaching comments, not just validation |
| PAT-005-e004 (ADR-Governed Architecture) | Domain | `ArchitectureDecision` | Immutable ADRs; new ADR to change |
| PAT-006-e004 (Iterative Feedback) | Application | `ReviewCoordinationService` | Multiple rounds, switch to sync if lengthy |
| PAT-007-e004 (Review Checklists) | Domain | `ReviewSession.checklist` | Domain-specific checklist items |
| PAT-001-e005 (Atomic Write) | Infrastructure | `AtomicWriteAdapter` | Temp file + rename + fsync |
| PAT-002-e005 (File-Based Mutual Exclusion) | Infrastructure | `PyFileLockAdapter` | py-filelock with 30s timeout |
| PAT-003-e005 (Optimistic Concurrency) | Domain | `FileVersion` | Version-based conflict detection |
| PAT-004-e005 (Coordination-Free ID) | Infrastructure | `SnowflakeIdAdapter` | Derived worker ID from host+pid |
| PAT-005-e005 (Workspace Separation) | Infrastructure | `GitWorktreeAdapter` | Parallel agents in separate worktrees |
| PAT-001-e006 (DoD Checklist) | Domain | `WorkItem.definition_of_done` | Verifiable checklist items |
| PAT-002-e006 (WBS Decomposition) | Domain | `TaskDecompositionService` | 100% rule, product-oriented |
| PAT-003-e006 (Agent Task Schema) | Domain | `WorkItem` | Structured inputs, outputs, criteria |
| PAT-004-e006 (Success Criteria Schema) | Domain | `SuccessCriterion` | Validation commands, thresholds |
| PAT-005-e006 (Vertical Slicing) | Domain | `TaskDecompositionService` | Cut through all layers per slice |

---

## Dependency Analysis

### Layer Dependencies (Clean Architecture Compliance)

```
┌─────────────────────────────────────────────────────────────────┐
│                        DEPENDENCY RULES                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Interface Layer                                                 │
│       │                                                          │
│       │ depends on                                               │
│       v                                                          │
│  Application Layer                                               │
│       │                                                          │
│       │ depends on                                               │
│       v                                                          │
│  Domain Layer <─────────────────────────────────────────────┐   │
│       │                                                      │   │
│       │ defines ports (interfaces)                           │   │
│       v                                                      │   │
│  [Ports]                                                     │   │
│       │                                                      │   │
│       │ implemented by                                       │   │
│       v                                                      │   │
│  Infrastructure Layer ───────────────────────────────────────┘   │
│       (adapters)                                                 │
│                                                                  │
│  CRITICAL: Domain Layer has NO external dependencies             │
│            (stdlib only per coding-standards.md)                 │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Import Rules Enforcement

| From Layer | May Import From | MUST NOT Import From |
|------------|-----------------|----------------------|
| Domain | Python stdlib only | Application, Infrastructure, Interface |
| Application | Domain | Infrastructure, Interface |
| Infrastructure | Domain, Application | Interface |
| Interface | All inner layers | - |

### External Library Dependencies

| Layer | Allowed Libraries | Purpose |
|-------|-------------------|---------|
| Domain | None (stdlib only) | Pure business logic |
| Application | None (stdlib only) | Use cases |
| Infrastructure | `filelock`, `hypothesis`, `pytest` | Adapter implementations |
| Interface | `click`, `rich` | CLI presentation |

---

## Technical Decisions Required

The following architecture decisions need formal ADRs before implementation:

### ADR-001: Test-First Protocol Enforcement

**Context**: PAT-001-e003 requires tests before code for all agent-generated code.

**Decision Needed**: How strictly to enforce? Options:
1. Hard constraint (reject code without tests)
2. Soft constraint (warn but allow)
3. Configurable per task type

**Recommended**: Hard constraint for production code; soft for spikes/exploration.

### ADR-006: File Locking Granularity

**Context**: PAT-002-e005 requires file-level locking.

**Decision Needed**: Lock granularity. Options:
1. Per-file locking (fine-grained)
2. Per-directory locking (coarse-grained)
3. Per-entity-type locking (medium)

**Recommended**: Per-file with 30-second timeout and exponential backoff.

### ADR-003: ID Generation Strategy

**Context**: PAT-004-e005 requires coordination-free unique IDs.

**Decision Needed**: ID format. Options:
1. Snowflake-style (64-bit, time-sortable)
2. UUIDv7 (128-bit, time-sortable)
3. Custom hybrid

**Recommended**: Snowflake-style with worker ID derived from hash(hostname+pid).

### ADR-004: Quality Gate Layer Configuration

**Context**: PAT-001-e002 recommends layered gates.

**Decision Needed**: Which layers to implement initially. Options:
1. Full stack (local, PR, pre-deploy, post-deploy, runtime)
2. Minimal (local, PR)
3. Progressive (start minimal, add based on observed failures)

**Recommended**: Progressive approach starting with local + PR.

### ADR-005: Agent Handoff State Format

**Context**: PAT-005-e001 requires explicit state handoff.

**Decision Needed**: State serialization format. Options:
1. JSON with schema validation
2. Protocol Buffers
3. MessagePack

**Recommended**: JSON with JSON Schema validation for readability and debugging.

### ADR-006: Review Rigor Tier Thresholds

**Context**: PAT-003-e004 requires tiered review rigor.

**Decision Needed**: What constitutes each tier. Options:
1. File-count based (T1: <5 files, T2: 5-20, T3: 20-50, T4: >50)
2. Impact-based (T1: docs/config, T2: feature, T3: API/security, T4: core/safety)
3. Combined metrics

**Recommended**: Impact-based with override capability.

---

## Risks and Mitigations

### Risk 1: Domain Layer Contamination

**Risk**: External dependencies creep into domain layer, violating clean architecture.

**Impact**: High - Breaks testability and portability.

**Mitigation**:
- Automated import checking in CI (pre-commit hook)
- Code review checklist item
- Domain tests run without infrastructure

### Risk 2: Lock Contention Under Load

**Risk**: Multiple Claude instances cause lock timeouts and starvation.

**Impact**: Medium - Degraded performance, potential data loss.

**Mitigation**:
- Exponential backoff with jitter (PAT-002-e005)
- Optimistic concurrency for low-contention operations (PAT-003-e005)
- Per-file locking instead of directory-level

### Risk 3: Context Rot in Long Sessions

**Risk**: Agent performance degrades as context fills (PAT-004-e001).

**Impact**: High - Incorrect code generation, missed requirements.

**Mitigation**:
- Pre-rot compaction at 25% of advertised limit
- Handle pattern for large artifacts
- Session checkpointing

### Risk 4: Test-First Bypass

**Risk**: Developers or agents skip test generation step.

**Impact**: High - Defeats purpose of quality gates.

**Mitigation**:
- Hard constraint in workflow service
- QualityGateFailed event blocks code generation
- Audit trail of test-first compliance

### Risk 5: ADR Staleness

**Risk**: ADRs become outdated but still referenced.

**Impact**: Medium - Architectural decisions drift from documentation.

**Mitigation**:
- ADR review as part of major changes
- Superseded status with link to replacement
- Automated ADR consistency checking

### Risk 6: Workspace Isolation Merge Conflicts

**Risk**: Git worktree isolation (PAT-005-e005) leads to complex merges.

**Impact**: Medium - Developer friction, potential lost work.

**Mitigation**:
- Short-lived branches per task
- Automated merge conflict detection before completion
- Human-in-the-loop for conflict resolution (PAT-006-e001)

---

## Implementation Phasing

### Phase 1: Core Domain (Week 1-2)

**Components**:
- Domain entities: `WorkItem`, `QualityGate`, `TestSuite`
- Value objects: `TaskStatus`, `Priority`, `AcceptanceCriterion`, `SuccessCriterion`
- Domain services: `TaskDecompositionService`, `QualityGateEvaluator`

**Patterns Implemented**:
- PAT-003-e006 (Agent Task Schema)
- PAT-001-e006 (DoD Checklist)
- PAT-004-e006 (Success Criteria Schema)

### Phase 2: Application Layer (Week 3-4)

**Components**:
- Commands and handlers for work item lifecycle
- Queries for task retrieval
- `DevelopmentWorkflowService` (test-first orchestration)
- Port definitions

**Patterns Implemented**:
- PAT-001-e003 (Test-First Protocol)
- PAT-001-e002 (Layered Gate Architecture)

### Phase 3: Infrastructure Adapters (Week 5-6)

**Components**:
- `FileSystemWorkItemAdapter` with atomic writes
- `PyFileLockAdapter`
- `SnowflakeIdAdapter`
- `PytestRunnerAdapter`

**Patterns Implemented**:
- PAT-001-e005 (Atomic Write)
- PAT-002-e005 (File-Based Mutual Exclusion)
- PAT-004-e005 (Coordination-Free ID)

### Phase 4: Interface Layer (Week 7-8)

**Components**:
- CLI commands
- Skill handler
- Agent protocols

**Patterns Implemented**:
- PAT-005-e001 (Explicit State Handoff)
- PAT-006-e001 (Human-in-the-Loop Gating)

### Phase 5: Advanced Features (Week 9+)

**Components**:
- `ReviewSession` and review workflow
- `ArchitectureDecision` and ADR management
- `GitWorktreeAdapter` for parallel agents
- Property-based testing integration

**Patterns Implemented**:
- PAT-001-e004 (Health-Over-Perfection)
- PAT-003-e004 (Tiered Review Rigor)
- PAT-005-e004 (ADR-Governed Architecture)
- PAT-002-e003 (Property-Based Testing)
- PAT-002-e001 (Git Worktree Isolation)

---

## Appendix: Directory Structure

```
src/development/
├── __init__.py
├── domain/
│   ├── __init__.py
│   ├── entities/
│   │   ├── __init__.py
│   │   ├── work_item.py
│   │   ├── quality_gate.py
│   │   ├── review_session.py
│   │   ├── test_suite.py
│   │   └── architecture_decision.py
│   ├── value_objects/
│   │   ├── __init__.py
│   │   ├── task_status.py
│   │   ├── priority.py
│   │   ├── risk_tier.py
│   │   ├── acceptance_criterion.py
│   │   ├── success_criterion.py
│   │   ├── dependency_graph.py
│   │   ├── snowflake_id.py
│   │   └── file_version.py
│   ├── events/
│   │   ├── __init__.py
│   │   ├── work_item_events.py
│   │   ├── test_events.py
│   │   ├── quality_events.py
│   │   └── review_events.py
│   └── services/
│       ├── __init__.py
│       ├── task_decomposition.py
│       ├── quality_gate_evaluator.py
│       ├── risk_assessment.py
│       └── dependency_resolver.py
├── application/
│   ├── __init__.py
│   ├── commands/
│   │   ├── __init__.py
│   │   ├── work_item_commands.py
│   │   ├── generation_commands.py
│   │   ├── quality_commands.py
│   │   ├── review_commands.py
│   │   └── adr_commands.py
│   ├── queries/
│   │   ├── __init__.py
│   │   ├── work_item_queries.py
│   │   ├── quality_queries.py
│   │   ├── review_queries.py
│   │   └── adr_queries.py
│   ├── handlers/
│   │   ├── commands/
│   │   │   ├── __init__.py
│   │   │   ├── work_item_handlers.py
│   │   │   ├── generation_handlers.py
│   │   │   ├── quality_handlers.py
│   │   │   └── review_handlers.py
│   │   └── queries/
│   │       ├── __init__.py
│   │       ├── work_item_query_handlers.py
│   │       ├── quality_query_handlers.py
│   │       └── review_query_handlers.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── development_workflow.py
│   │   ├── quality_orchestration.py
│   │   ├── review_coordination.py
│   │   └── context_compaction.py
│   └── ports/
│       ├── __init__.py
│       ├── repository_ports.py
│       ├── generation_ports.py
│       ├── execution_ports.py
│       ├── infrastructure_ports.py
│       └── messaging_ports.py
├── infrastructure/
│   ├── __init__.py
│   └── adapters/
│       ├── __init__.py
│       ├── persistence/
│       │   ├── __init__.py
│       │   ├── filesystem_work_item_adapter.py
│       │   ├── filesystem_review_adapter.py
│       │   └── filesystem_adr_adapter.py
│       ├── generation/
│       │   ├── __init__.py
│       │   └── claude_generation_adapter.py
│       ├── testing/
│       │   ├── __init__.py
│       │   ├── pytest_runner_adapter.py
│       │   └── hypothesis_adapter.py
│       ├── quality/
│       │   ├── __init__.py
│       │   ├── precommit_adapter.py
│       │   ├── ruff_adapter.py
│       │   └── coverage_adapter.py
│       └── filesystem/
│           ├── __init__.py
│           ├── filelock_adapter.py
│           ├── atomic_write.py
│           ├── snowflake_id_adapter.py
│           └── git_worktree_adapter.py
└── interface/
    ├── __init__.py
    ├── cli/
    │   ├── __init__.py
    │   ├── task_commands.py
    │   ├── generation_commands.py
    │   ├── quality_commands.py
    │   ├── review_commands.py
    │   └── adr_commands.py
    ├── skill/
    │   ├── __init__.py
    │   ├── dev_skill_handler.py
    │   ├── task_template_parser.py
    │   └── gherkin_parser.py
    └── agent/
        ├── __init__.py
        ├── task_protocol.py
        ├── handoff_protocol.py
        └── human_gate_protocol.py
```

---

*Architecture analysis completed: 2026-01-09*
*Agent: ps-analyst (Architecture)*
*Source synthesis: dev-skill-e-007*
*Patterns mapped: 37*
*ADRs required: 6*
