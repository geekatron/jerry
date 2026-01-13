# WI-SAO-048: Internal Research - PROJ-001/002 Knowledge Bases

> **Work Item:** WI-SAO-048
> **Initiative:** SAO-INIT-008 (Agent Skill Enhancement)
> **Date:** 2026-01-12
> **Status:** COMPLETE
> **Objective:** Extract relevant patterns, lessons learned, and optimization findings from Jerry's internal project knowledge bases to inform agent enhancement.

---

## Executive Summary

This research document synthesizes findings from two major Jerry Framework projects to inform agent skill enhancement:

- **PROJ-001-plugin-cleanup**: Established the architectural foundation with Hexagonal Architecture, Event Sourcing, CQRS, and graph-ready identity patterns
- **PROJ-002-nasa-systems-engineering**: Developed multi-agent orchestration patterns, prompting strategies, and persona compatibility research

**Key Insights:**

1. **Architecture Patterns**: Jerry uses Hexagonal Architecture with strict layer dependencies (domain -> application -> infrastructure -> interface), CloudEvents 1.0 for event sourcing, and strongly-typed VertexId hierarchy for graph-ready entities

2. **Multi-Agent Orchestration**: 8 canonical patterns defined (Single Agent, Sequential Chain, Fan-Out, Fan-In, Cross-Pollinated Pipeline, Divergent-Convergent Diamond, Review Gate, Generator-Critic Loop)

3. **Context Engineering**: Evolution from "prompt engineering" to systematic context management using Write/Select/Compress/Isolate taxonomy

4. **Optimization Opportunities**: 8 GO decisions including explicit model fields, Generator-Critic loops, checkpointing, parallel execution, guardrail hooks, orchestrator agents, nse-explorer agent, and two-phase prompting

5. **L0/L1/L2 Framework**: Triple-lens documentation approach provides cognitive scaffolding at three levels (ELI5 metaphors, Engineer implementation, Architect patterns/anti-patterns)

---

## 1. PROJ-001 Architecture Patterns

### 1.1 Hexagonal Architecture (Ports and Adapters)

**Source:** `PROJ-001-e-006-unified-architecture-canon.md`

The Jerry Framework adopts strict hexagonal architecture with the following layer dependencies:

| Layer | Can Import From | Cannot Import From |
|-------|-----------------|-------------------|
| `domain/` | stdlib ONLY | application, infrastructure, interface |
| `application/` | domain | infrastructure, interface |
| `infrastructure/` | domain, application | interface |
| `interface/` | domain, application, infrastructure | - |

**Directory Structure:**
```
src/
├── domain/           # Pure business logic, NO external deps
│   ├── aggregates/
│   ├── value_objects/
│   ├── events/
│   ├── ports/        # Interfaces (contracts)
│   └── exceptions.py
├── application/      # Use cases, orchestration
│   ├── commands/
│   ├── queries/
│   ├── handlers/
│   └── dtos/
├── infrastructure/   # Adapters implementing ports
│   ├── persistence/
│   ├── event_store/
│   └── messaging/
└── interface/        # Primary adapters (CLI, API)
    ├── cli/
    └── api/
```

**Key Insight:** Dependency inversion means domain defines ports (interfaces), infrastructure implements adapters, and the composition root wires everything together.

### 1.2 CQRS Pattern

**Commands:**
- Immutable frozen dataclasses
- Handler loads aggregate via repository
- Aggregate validates and raises domain events
- Handler saves aggregate (events appended)

**Queries:**
- Return DTOs, never domain entities
- Read from projections (eventually consistent)
- Projections built by consuming events

```python
# Command Pattern
@dataclass(frozen=True)
class CreateTaskCommand:
    title: str
    description: str
    priority: Priority

# Query Pattern
class ListTasksQueryHandler:
    def handle(self, query: ListTasksQuery) -> TaskListResult:
        return self._projection_store.query(query.filters)
```

### 1.3 Event Sourcing

**CloudEvents 1.0 Envelope:**
```json
{
  "specversion": "1.0",
  "type": "com.jerry.task.completed.v1",
  "source": "/jerry/tasks/TASK-ABC123",
  "id": "EVT-a1b2c3d4",
  "time": "2026-01-07T14:30:00Z",
  "subject": "TASK-ABC123",
  "datacontenttype": "application/json",
  "data": { ... }
}
```

**Key Components:**
- `IEventStore`: Append-only event log with optimistic concurrency (`expected_version`)
- `ISnapshotStore`: Performance optimization (snapshot every 10 events)
- `AggregateRoot`: Base class with `_raise_event()`, `_apply()`, `collect_events()`

### 1.4 Port/Adapter Design

**Primary Ports (Driving):**
- Define use case interfaces
- Called by external actors (CLI, API, sub-agents)
- Examples: `ICreateTaskUseCase`, `ICompleteTaskUseCase`

**Secondary Ports (Driven):**
- Define infrastructure contracts
- Implemented by adapters
- Examples: `IRepository`, `IEventStore`, `IGraphStore`

### 1.5 Composition Root Pattern

All dependency wiring happens in a single location (`src/bootstrap.py`):

```python
def create_query_dispatcher() -> QueryDispatcher:
    # Create infrastructure adapters
    repository = FilesystemProjectAdapter()
    environment = OsEnvironmentAdapter()

    # Create handlers with injected dependencies
    handler = GetProjectContextHandler(repository=repository, environment=environment)

    # Configure dispatcher
    dispatcher = QueryDispatcher()
    dispatcher.register(GetProjectContextQuery, handler.handle)

    return dispatcher
```

**Rule:** Adapters NEVER instantiate their own dependencies.

### 1.6 Identity Patterns (VertexId Hierarchy)

Graph-ready strongly typed identifiers:

| ID Type | Format | Example |
|---------|--------|---------|
| PlanId | `PLAN-{uuid8}` | `PLAN-a1b2c3d4` |
| PhaseId | `PHASE-{uuid8}` | `PHASE-e5f6g7h8` |
| TaskId | `TASK-{uuid8}` | `TASK-ABC12345` |
| SubtaskId | `TASK-{parent}.{seq}` | `TASK-ABC123.1` |
| EventId | `EVT-{uuid}` | `EVT-a1b2c3d4` |

**Benefits:** Type safety, self-documenting code, graph primitive compatibility.

---

## 2. PROJ-002 Agent Research

### 2.1 Eight Optimization Options (All GO Decisions)

**Source:** `skills-agents-optimization-synthesis.md`

| Option ID | Description | Priority | Risk Level | Decision |
|-----------|-------------|----------|------------|----------|
| OPT-001 | Add explicit model field to agent frontmatter | High | GREEN | **GO** |
| OPT-002 | Implement Generator-Critic loops | High | RED->YELLOW | **GO** (with circuit breaker) |
| OPT-003 | Add checkpointing mechanism | P1 | YELLOW | **GO** |
| OPT-004 | Add parallel execution primitives | P1 | RED->YELLOW | **GO** (with isolation) |
| OPT-005 | Add guardrail validation hooks | P1 | YELLOW | **GO** |
| OPT-006 | Create orchestrator agents | High | YELLOW | **GO** |
| OPT-007 | Add nse-explorer agent | Critical | YELLOW | **GO** |
| OPT-008 | Implement two-phase prompting | High | GREEN | **GO** |

### 2.2 Eighteen Architecture Gaps

**Gap Severity Distribution:**
```
Critical:  ███ (3)     17%   [GAP-AGT-003, GAP-006, GAP-COORD]
High:      ████████ (8) 44%   [GAP-SKL-001/002, GAP-AGT-004/007/009, GAP-001/002/008]
Medium:    █████ (5)   28%   [GAP-SKL-003, GAP-AGT-005/008, GAP-003/005]
Low:       ██ (2)      11%   [GAP-004, GAP-010]
```

**Critical Gaps:**
- **GAP-AGT-003**: All nse-* agents are convergent-only; no divergent exploration capability (Belbin Plant/Resource Investigator gap)
- **GAP-006**: No formal session_context contract prevents reliable agent chaining
- **GAP-COORD**: No parallel execution or checkpointing compared to LangGraph/ADK competitors

### 2.3 Thirty Risk Register Items

**Risk Profile:**

| Risk Category | RED | YELLOW | GREEN | Residual After Mitigation |
|---------------|-----|--------|-------|---------------------------|
| Implementation | 2 | 8 | 4 | 0 RED, 4 YELLOW, 10 GREEN |
| Technical | 1 | 9 | 6 | 0 RED, 5 YELLOW, 11 GREEN |

**Pre-Implementation Mitigations Required:**
- **M-001**: Context isolation (copy-on-spawn, no shared state) for parallel races
- **M-002**: Circuit breaker (max_iterations=3, improvement threshold) for infinite loops
- **M-003**: Schema validation (JSON Schema at agent boundaries) for schema incompatibility

### 2.4 Context Engineering Patterns

**Source:** `agent-research-005-prompting-strategies.md`

**Evolution:** "Prompt engineering" has evolved to "Context Engineering" - the systematic design of context windows.

**Four Strategic Categories (Write/Select/Compress/Isolate):**

| Category | Purpose | Techniques |
|----------|---------|------------|
| **Write** | Add context to window | System prompts, tool results, templates |
| **Select** | Choose what to include | RAG, semantic search, context prioritization |
| **Compress** | Reduce token count | Summarization, context compaction |
| **Isolate** | Sandbox sensitive context | Multi-agent isolation, memory segmentation |

**System Prompt Structure (RIGOR Framework):**
1. Role/Identity
2. Goals/Objectives
3. Capabilities/Constraints
4. Instructions/Procedures
5. Guardrails/Safety
6. Output Format
7. Examples (multishot)

### 2.5 Multi-Agent Orchestration Patterns

**Source:** `agent-research-002-multi-agent-patterns.md`

**Seven Primary Industry Patterns:**

| Pattern | Use Case | Framework Support |
|---------|----------|-------------------|
| Sequential Pipeline | Linear workflows with dependencies | CrewAI, LangGraph |
| Hierarchical/Supervisor | Complex tasks with delegation | CrewAI hierarchical, LangGraph |
| Network (Peer-to-Peer) | Dynamic collaboration | AutoGen GroupChat |
| Orchestrator-Worker | Fan-out/fan-in parallelism | Google ADK, Microsoft Magentic-One |
| Generator-Critic | Iterative refinement | Google ADK LoopAgent |
| Parallel (Map-Reduce) | Independent parallel tasks | LangGraph parallel branches |
| Human-in-the-Loop | High-stakes decisions | All frameworks |

### 2.6 Claude Code Agent Mechanics

**Source:** `agent-research-001-claude-code-mechanics.md`

**Task Tool Parameters:**
- `subagent_type`: "explore" (Haiku, read-only), "plan" (with resumption), general-purpose
- `prompt`: Instructions for subagent
- `description`: For TodoWrite tracking
- `resume`: Continue background tasks
- `run_in_background`: Non-blocking execution

**Single Nesting Constraint (P-003):**
- Maximum ONE level of agent nesting (orchestrator -> worker)
- Subagents cannot spawn their own subagents
- Prevents recursive explosion of context

**Context Passing Model:**
> "Subagents currently start with zero context"

- Must explicitly pass relevant information in prompt
- No automatic inheritance of parent context
- File-based communication preferred for large context

**Parallel Execution:**
- Max 10 concurrent subagents
- Batched processing for >10 tasks
- Independent Task calls in single message run parallel

### 2.7 Persona Compatibility Research

**Source:** `agent-research-004-persona-compatibility.md`

**High Synergy Combinations:**
| Persona A | Persona B | Synergy Type |
|-----------|-----------|--------------|
| Researcher | Analyst | Gather-Synthesize |
| Generator | Critic | Create-Evaluate |
| Planner | Executor | Design-Implement |
| Orchestrator | Specialists | Coordinate-Execute |
| Divergent Thinker | Convergent Thinker | Ideate-Synthesize |

**Anti-Patterns to Avoid:**
- **Role Overlap**: Generalist + Generalist = redundancy
- **Role Drift**: Agents evolving toward similar behavior
- **Circular Validation**: Agents reinforcing each other's errors
- **Error Cascade**: One mistake propagating to all agents

**Belbin Team Roles for AI:**
| Belbin Role | AI Agent Equivalent | Function |
|-------------|---------------------|----------|
| Plant | Creative/Ideation Agent | Generates novel ideas |
| Resource Investigator | Research Agent | Explores opportunities |
| Coordinator | Orchestrator Agent | Clarifies goals, delegates |
| Monitor Evaluator | Critic/Validator Agent | Evaluates options |
| Completer Finisher | QA/Polish Agent | Ensures quality |

---

## 3. SAO-INIT-007 Triple-Lens Lessons

### 3.1 L0/L1/L2 Framework

**Source:** `sao-init-007-triple-lens-playbooks/_index.md`

The Triple-Lens framework provides cognitive scaffolding at three levels:

| Level | Name | Audience | Content Type |
|-------|------|----------|--------------|
| **L0** | ELI5 | Newcomers | Metaphors, analogies, WHAT and WHY |
| **L1** | Engineer | Practitioners | Commands, snippets, HOW |
| **L2** | Architect | Experts | Anti-patterns, boundaries, CONSTRAINTS |

### 3.2 What Worked

1. **Metaphor-First Documentation**: L0 metaphors (e.g., "relay race" for Sequential Chain, "brainstorming then voting" for Diamond pattern) dramatically improve comprehension

2. **ASCII Diagrams**: Visual topology representations in L1 sections bridge understanding gaps

3. **Anti-Pattern Sections**: L2 anti-patterns prevent common mistakes (e.g., "unbounded parallelism without barriers causes race conditions")

4. **Session Context Schema**: Formalized handoff contract (v1.0.0) enables reliable agent chaining:
```yaml
session_context:
  version: "1.0.0"
  session_id: "uuid-v4"
  source_agent: "agent-name"
  target_agent: "agent-name"
  state_output_key: "key_name"
  cognitive_mode: "convergent|divergent"
  payload: { ... }
```

5. **Agent State Output Keys**: Standardized output keys (research_output, analysis_output, etc.) with next_hint suggestions

### 3.3 What Did Not Work Initially

1. **L1-Heavy Documentation**: Original playbooks were command-focused but lacked intent explanation

2. **Missing Generator-Critic**: Initial refactoring missed ps-critic agent documentation

3. **No Concrete Examples**: Abstract patterns without domain-specific examples (SE, PM, UX)

4. **@ Symbol Confusion**: Clarified that @ symbol is NOT for agent invocation

### 3.4 Key Discoveries

- **DISCOVERY-008**: 8 orchestration patterns identified
- **DISCOVERY-009**: Session context schema v1.0.0 formalized
- **DISCOVERY-012**: Critical documentation gaps (Generator-Critic, concrete examples)

---

## 4. Orchestration Patterns

### 4.1 Eight Canonical Patterns

**Source:** `skills/shared/ORCHESTRATION_PATTERNS.md`

```
BASIC PATTERNS                    ADVANCED PATTERNS
1. SINGLE AGENT                   5. CROSS-POLLINATED PIPELINE
2. SEQUENTIAL CHAIN               6. DIVERGENT-CONVERGENT (Diamond)
3. FAN-OUT (Parallel)             7. REVIEW GATE
4. FAN-IN (Aggregate)             8. GENERATOR-CRITIC LOOP
```

### 4.2 Pattern Usage Distribution (Recommended)

| Pattern | Frequency | Typical Use Case |
|---------|-----------|------------------|
| Single Agent | 40% | Simple, single-domain tasks |
| Sequential Chain | 25% | Linear workflows with dependencies |
| Fan-Out/Fan-In | 15% | Parallel exploration with synthesis |
| Generator-Critic | 10% | Quality-critical outputs |
| Review Gate | 5% | NASA technical reviews, quality checkpoints |
| Cross-Pollinated | 3% | Multi-skill family collaboration |
| Diamond | 2% | Solution space exploration |

### 4.3 Enhancement Opportunities

1. **Cross-Pollinated Pipeline**: Currently underutilized; high potential for ps-* and nse-* skill family integration

2. **Generator-Critic Loop**: Circuit breaker parameters need tuning:
```yaml
circuit_breaker:
  max_iterations: 3
  quality_threshold: 0.85
  escalation: human_review
```

3. **Review Gate**: NASA review types (SRR, PDR, CDR, TRR, FRR, etc.) need nse-reviewer integration

### 4.4 Cross-Skill Handoff Matrix

```
PROBLEM-SOLVING -> NASA SE
ps-architect (design) -----> nse-architecture (formal architecture)
ps-analyst (root cause) ---> nse-risk (risk assessment)
ps-validator (check) ------> nse-verification (V&V matrix)

NASA SE -> PROBLEM-SOLVING
nse-requirements ---------> ps-architect (design to requirements)
nse-verification (gaps) --> ps-investigator (investigate gaps)
nse-reviewer (RIDs) ------> ps-analyst (analyze RID root cause)
```

### 4.5 Pattern Selection Decision Tree

```
IF task is simple AND single-domain:
    -> Use Pattern 1 (Single Agent)

ELSE IF task has dependencies (order matters):
    -> Use Pattern 2 (Sequential Chain)

ELSE IF tasks are independent AND need parallel exploration:
    -> Use Pattern 3+4 (Fan-Out then Fan-In)

ELSE IF cross-skill family collaboration needed:
    -> Use Pattern 5 (Cross-Pollinated Pipeline)

ELSE IF solution space exploration needed:
    -> Use Pattern 6 (Diamond)

ELSE IF quality checkpoint required:
    -> Use Pattern 7 (Review Gate)

ELSE IF iterative refinement needed:
    -> Use Pattern 8 (Generator-Critic Loop)
```

---

## 5. Synthesis: Key Actionable Insights

### 5.1 Agent Enhancement Priorities

| Priority | Enhancement | Rationale |
|----------|-------------|-----------|
| **P0** | Implement session_context schema validation | Foundation for reliable agent chaining |
| **P1** | Add nse-explorer agent (divergent mode) | Fill critical Belbin Plant/Resource Investigator gap |
| **P1** | Add orchestrator agents (ps-orchestrator, nse-orchestrator) | Enable hierarchical workflows |
| **P1** | Implement Generator-Critic loops with circuit breaker | Quality assurance for design outputs |
| **P2** | Add parallel execution primitives (max 5 concurrent) | Performance parity with competitors |
| **P2** | Add checkpointing mechanism | Recovery and resumption capability |
| **P3** | Unify agent templates (superset schema) | Reduce maintenance burden |

### 5.2 Documentation Improvements

1. **All playbooks MUST have L0/L1/L2 sections**
2. **Include ASCII topology diagrams in L1**
3. **Document at least 3 anti-patterns per playbook in L2**
4. **Provide 5+ concrete examples per domain**
5. **Standardize state output keys with next_hint suggestions**

### 5.3 Architecture Compliance

1. **Maintain hexagonal layer boundaries** (domain has no external deps)
2. **Use composition root for all wiring** (no adapter self-instantiation)
3. **Apply CloudEvents 1.0 for all domain events**
4. **Respect P-003**: Maximum ONE level of agent nesting

### 5.4 Context Engineering Best Practices

1. **Write system prompts with RIGOR structure** (Role, Instructions, Goals, Output, Rules)
2. **Use multishot prompting** for complex patterns
3. **Apply Chain-of-Thought** for reasoning tasks
4. **Use XML structured prompting** for Claude (preferred over JSON)
5. **Implement state handoff schemas** for multi-agent workflows

### 5.5 Risk Mitigations

| Risk | Mitigation |
|------|------------|
| Parallel race conditions | Context isolation (copy-on-spawn) |
| Infinite Generator-Critic loops | Circuit breaker (max 3 iterations) |
| Schema incompatibility | JSON Schema validation at boundaries |
| Non-atomic checkpoints | Write-ahead logging |
| Orchestrator bottleneck | Async delegation |

---

## 6. Sources

### PROJ-001 Documents
| Document | Path |
|----------|------|
| Unified Architecture Canon | `projects/PROJ-001-plugin-cleanup/synthesis/PROJ-001-e-006-unified-architecture-canon.md` |

### PROJ-002 Documents
| Document | Path |
|----------|------|
| Skills-Agents Optimization Synthesis | `projects/PROJ-002-nasa-systems-engineering/synthesis/skills-agents-optimization-synthesis.md` |
| Agent Research 001: Claude Code Mechanics | `projects/PROJ-002-nasa-systems-engineering/research/agent-research-001-claude-code-mechanics.md` |
| Agent Research 002: Multi-Agent Patterns | `projects/PROJ-002-nasa-systems-engineering/research/agent-research-002-multi-agent-patterns.md` |
| Agent Research 004: Persona Compatibility | `projects/PROJ-002-nasa-systems-engineering/research/agent-research-004-persona-compatibility.md` |
| Agent Research 005: Prompting Strategies | `projects/PROJ-002-nasa-systems-engineering/research/agent-research-005-prompting-strategies.md` |

### SAO-INIT-007 Documents
| Document | Path |
|----------|------|
| Triple-Lens Initiative Index | `projects/PROJ-002-nasa-systems-engineering/work/initiatives/sao-init-007-triple-lens-playbooks/_index.md` |
| Orchestration Patterns Reference | `skills/shared/ORCHESTRATION_PATTERNS.md` |

### External References
| Reference | URL |
|-----------|-----|
| Hexagonal Architecture | https://alistair.cockburn.us/hexagonal-architecture/ |
| Context Engineering (Anthropic) | https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents |
| CloudEvents 1.0 | https://cloudevents.io/ |
| Belbin Team Roles | https://www.belbin.com/about/belbin-team-roles |
| CrewAI Documentation | https://docs.crewai.com/ |
| LangGraph Multi-Agent | https://langchain-ai.github.io/langgraph/tutorials/multi_agent/ |
| Google ADK Multi-Agent | https://google.github.io/adk-docs/agents/multi-agents/ |

---

*Document ID: WI-SAO-048-RESEARCH*
*Generated: 2026-01-12*
*Status: COMPLETE*
