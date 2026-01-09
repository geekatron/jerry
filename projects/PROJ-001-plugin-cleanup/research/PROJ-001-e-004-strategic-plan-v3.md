# Strategic Plan Extraction: Work-Tracker v3.0

> **PS ID:** PROJ-001
> **Entry ID:** e-004
> **Date:** 2026-01-09
> **Source:** `docs/knowledge/dragonsbelurkin/glimmering-brewing-lake-v3.md`
> **Researcher:** ps-researcher agent (v2.0.0)

---

## L0: Executive Summary

Work-Tracker v3.0 represents a **ground-up architectural rewrite** of the work-tracker skill, moving from v2.1.0's mixed architecture (with 128+ failing tests) to a pure Domain-Driven Design implementation. The strategic vision centers on:

1. **Pure DDD with 4 Bounded Contexts**: Work Management, Knowledge Capture, Identity & Access, and Reporting
2. **Event Sourcing**: All state changes persisted as immutable CloudEvents 1.0 for complete audit trails
3. **CQRS**: Complete separation of command (write) and query (read) paths
4. **Hexagonal Architecture**: Ports & Adapters pattern isolating domain from infrastructure
5. **Sub-agent Permission Model**: First-class support for Claude sub-agents with restricted permissions

**Key Strategic Decision**: Breaking changes are acceptable to achieve architectural purity. Migration tools will bridge v2.x to v3.0.

---

## L1: Technical Analysis

### 1. 5W1H Analysis Framework

#### WHO is affected?
| Stakeholder | Role | Impact |
|------------|------|--------|
| Claude Code instances | Primary | Track multi-phase work across sessions |
| Users (humans) | Secondary | Review work progress, grant consent |
| Future maintainers | Tertiary | Maintain skill codebase |

#### WHAT is the problem?
- **128+ failing tests** due to global state pollution (test isolation)
- **46 migration tests** expecting deprecated scripts
- **Event sourcing infrastructure** defined but never activated
- **Mixed architecture patterns**: Pre-Hexagonal and Hexagonal code coexisting
- **JSON SSOT works** but markdown sync has edge case failures

#### WHERE is it happening?
| Location | Purpose |
|----------|---------|
| `.claude/skills/work-tracker/` | Skill implementation |
| `.ecw/plans/` | JSON state files (SSOT) |
| `docs/plans/` | Markdown derived views |
| `tests/` | Comprehensive but failing test suite |

#### WHEN did it start?
- **D-040** (Hexagonal Architecture) introduced new patterns
- **Rapid iteration** left legacy scripts incompletely deprecated
- **Test isolation issues** accumulated over Initiative 16-19

#### WHY does it matter?
- Unreliable tests undermine confidence in changes
- Mixed architectures create maintenance burden
- Missing event sourcing prevents audit trails
- Users experience inconsistent behavior

#### HOW is it manifesting?
- `pytest` suite: **151 failures** out of 5204 (97.1% pass rate)
- `wt.py` commands fail on edge cases
- Markdown regeneration loses data in specific scenarios

---

### 2. Bounded Contexts Definition

#### 2.1 Work Management Bounded Context
**Aggregate Root:** Plan

```
ENTITIES:
- Initiative (references Plans)
- Plan (contains Phases)
- Phase (contains Tasks)
- Task (contains Subtasks)
- Subtask

VALUE OBJECTS:
- CanonicalId (UUID)
- DisplayId (human-readable)
- Actor (who performed action)
- BlockingInfo (blocking reason + metadata)
- Percentage (0-100 progress)
- TimeMetadata (created/modified timestamps)

DOMAIN EVENTS:
- PlanCreated, PhaseAdded, TaskAdded
- TaskStatusChanged, PhaseCompleted
- TaskBlocked, TaskUnblocked
```

**State Machines:**
- Initiative: DRAFT -> ACTIVE -> (PAUSED) -> COMPLETE -> ARCHIVED
- Phase: PENDING -> IN_PROGRESS -> (BLOCKED) -> COMPLETE
- Task: PENDING -> IN_PROGRESS -> (BLOCKED/SKIPPED) -> COMPLETE
- Subtask: PENDING <-> COMPLETE (checked/unchecked)

#### 2.2 Evidence Bounded Context
**Aggregate Root:** Evidence

```
5W1H EVIDENCE MODEL:
- WHO: Actor (who captured evidence)
- WHAT: string (what was captured)
- WHEN: DateTime (when captured)
- WHERE: string (file path if applicable)
- WHY: string (why this evidence matters)
- HOW: string (how evidence was obtained)

EVIDENCE TYPES:
- COMMAND_OUTPUT (shell command + output)
- FILE_REFERENCE (artifact file reference)
- MANUAL_NOTE (manual verification note)
- TEST_RESULT (test execution result)
- BUILD_ARTIFACT (build output reference)
- SCREENSHOT (visual evidence)
```

#### 2.3 Identity & Access Bounded Context
**Aggregate Root:** ConsentState

```
ENTITIES:
- ConsentState (blanket/per-item approval)
- ConsentDecision (audit trail)

VALUE OBJECTS:
- AgentContext (current actor + permissions)
- Permission (CRUD + COMPLETE + CONSENT + DELEGATE)

CONSENT MODES:
- PER_ITEM: Each completion requires explicit approval
- BLANKET: Auto-approve completions
- SESSION_BLANKET: Blanket approval with expiry

PERMISSION MODEL:
| Operation | Main Agent | Sub-agent |
|-----------|------------|-----------|
| CREATE    | YES        | YES       |
| READ      | YES        | YES       |
| WRITE     | YES        | YES       |
| COMPLETE  | YES        | NO        |
| DELETE    | YES        | NO        |
| CONSENT   | NO (Human) | NO        |
| DELEGATE  | YES        | NO        |
```

#### 2.4 Knowledge Capture Bounded Context
**Aggregate Root:** KnowledgeItem (Abstract)

```
KNOWLEDGE TYPES:
- Lesson (what happened, root cause, prevention)
- Pattern (context, problem, solution, consequences)
- Decision (ADR: decision, rationale, alternatives)
- Assumption (assumption text, validation status)
- Discovery (research finding, source, impact)
- Question (open question, answer when resolved)
```

#### 2.5 Context Map (Relationships)

```
Work Management <-----> Knowledge Capture
      |                       |
      | publishes events      | references
      v                       v
  Reporting            Evidence
      ^                       ^
      |                       |
      | queries               | attaches to
      |                       |
Identity & Access ------------+
  (guards completions)
```

**Relationship Types:**
- **Published Language**: Events shared via Event Bus
- **Customer-Supplier**: Work Management supplies events to Reporting
- **Conformist**: Reporting conforms to Work Management's event schema
- **Anti-Corruption Layer**: ADO Integration (external system)

---

### 3. Integration Strategies

#### 3.1 ADO (Azure DevOps) Integration via Anti-Corruption Layer

**Entity Mappings:**
| Work-Tracker | ADO Type | Notes |
|--------------|----------|-------|
| Initiative | Epic | Top-level grouping |
| Plan | Feature | Deliverable container |
| Phase | (Tags/Custom.Phase) | No direct equivalent |
| Task | Task | Work item |
| Subtask | (Description checklist) | No direct equivalent |
| Evidence | Attachment | File + comment |

**Status Mappings:**
| Work-Tracker | ADO (Agile) | Notes |
|--------------|-------------|-------|
| DRAFT | New | Not yet started |
| PENDING | New | Default initial state |
| IN_PROGRESS | Active | Work has started |
| BLOCKED | Active + "blocked" tag | Use tag for disambiguation |
| SKIPPED | Removed | Work item removed |
| COMPLETE | Closed | Reason: Completed |
| ARCHIVED | Removed/Closed + "archived" | Soft delete |

**Required Custom ADO Fields:**
| Field | Type | Purpose |
|-------|------|---------|
| Custom.CanonicalId | GUID | WT primary key |
| Custom.DisplayId | String | WT human-readable ID |
| Custom.BlockedReason | String | Why blocked |
| Custom.BlockedBy | Identity | Who blocked |
| Custom.BlockedAt | DateTime | When blocked |
| Custom.VerificationCriteria | HTML | Acceptance criteria |
| Custom.Phase | Picklist | Phase grouping |
| Custom.SyncEnabled | Boolean | ADO sync active |

#### 3.2 ACL Architecture Components

```
DOMAIN LAYER (Protected)
    |
    v
SECONDARY PORTS (Interfaces)
    |
    v
+-----------------------------------+
|     ANTI-CORRUPTION LAYER         |
|                                   |
|  FACADE: AdoIntegrationFacade     |
|    - Simplified API               |
|    - Orchestrates sync            |
|    - Circuit breaker              |
|                                   |
|  ADAPTERS:                        |
|    - InitiativeAdoAdapter (Epic)  |
|    - PlanAdoAdapter (Feature)     |
|    - TaskAdoAdapter (Task)        |
|    - EvidenceAdoAdapter (Attach)  |
|    - LinkAdapter (Relations)      |
|                                   |
|  TRANSLATORS:                     |
|    - EntityTranslator             |
|    - StatusTranslator             |
|    - IdentityTranslator           |
|    - PatchDocumentBuilder         |
+-----------------------------------+
    |
    v
AZURE DEVOPS (External System)
```

**Conflict Resolution Strategies:**
| Strategy | Behavior | Use Case |
|----------|----------|----------|
| LOCAL_WINS | Local overwrites ADO | WT is source of truth |
| REMOTE_WINS | ADO overwrites local | ADO is source of truth |
| MERGE | Field-level merge | Both systems valid |
| MANUAL | Human decision | Complex conflicts |
| LAST_WRITE_WINS | Most recent timestamp | Simple resolution |

---

### 4. Knowledge Architecture

#### Layer 1: Filesystem
- **JSON SSOT**: `.ecw/plans/*.json` - Single Source of Truth
- **Markdown Views**: `docs/plans/*.md` - Derived, regenerable
- **Event Log**: Append-only event store
- **State Files**: Projections for read optimization

#### Layer 2: Graph + Vector (Future Enhancement)
- Entity relationships via domain events
- Cross-reference via related_work_items
- Knowledge linking to work items

#### Layer 3: AI Integration
- Claude sub-agents with restricted permissions
- Natural language command parsing
- Context-aware progress reporting

#### Wisdom Capture Approach
1. **Lessons**: Captured from task completion experiences
2. **Patterns**: Documented from recurring solutions
3. **Decisions**: ADRs for significant architectural choices
4. **Assumptions**: Tracked with validation status
5. **Discoveries**: Research findings with sources

---

### 5. Gap Analysis

#### 5.1 Current State vs Desired State

| Aspect | Current (v2.1.0) | Desired (v3.0) | Gap |
|--------|------------------|----------------|-----|
| Architecture | Mixed (pre/post Hexagonal) | Pure Hexagonal | HIGH |
| Test Pass Rate | 97.1% (151 failures) | 100% | MEDIUM |
| Event Sourcing | Defined, not active | Active, SSOT | HIGH |
| CQRS | Partial | Complete separation | MEDIUM |
| Sub-agent Support | Ad-hoc | First-class permissions | HIGH |
| ADO Integration | None | Full ACL | NEW |
| Knowledge Capture | Basic | Structured 6 types | MEDIUM |

#### 5.2 Implementation Gaps by Priority

**P0 (Critical):**
- Domain layer with zero external dependencies
- Event sourcing as primary storage
- Sub-agent permission enforcement
- User consent for completions

**P1 (High):**
- Middleware pipeline for cross-cutting concerns
- CLI with structured + NL commands
- Evidence attachment before completion
- Markdown regeneration from events

**P2 (Medium):**
- ADO Anti-Corruption Layer
- Knowledge capture types
- Migration tool for v2.x data

---

### 6. Recommendations

#### 6.1 Architecture Decisions (ADRs)

| ADR | Decision | Rationale | Confidence |
|-----|----------|-----------|------------|
| ADR-001 | Ground-up rewrite | v2.x technical debt too high | HIGH |
| ADR-002 | 4 Bounded Contexts | Clear separation, independent evolution | HIGH |
| ADR-003 | Event Sourcing primary | Complete audit trail, time travel | HIGH |
| ADR-004 | CQRS separate dispatchers | Different concerns, optimizations | HIGH |
| ADR-005 | Middleware pipeline | Composable cross-cutting concerns | MEDIUM |
| ADR-006 | Sub-agent restrictions | Safety, SOP compliance | HIGH |
| ADR-007 | Dual CLI (structured + NL) | Claude prefers NL, humans prefer structured | MEDIUM |
| ADR-008 | JSON as SSOT | Markdown regeneration causes data loss | HIGH |
| ADR-009 | Phase entity (no ADO equiv) | WT concept, use tags in ADO | MEDIUM |
| ADR-010 | ACL for ADO integration | Isolate external system | HIGH |

#### 6.2 Risk Mitigations

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| Scope creep | High | Medium | Strict phase gates, defer non-essential |
| Event schema changes | Medium | High | Version events from day 1 |
| Breaking changes | Medium | Certain | Document all, provide migration guide |
| Test coverage gaps | High | Low | BDD-first, no untested code |
| Context limit | Medium | Medium | Frequent checkpoints, detailed handoffs |

---

### 7. Timeline/Roadmap

#### Phase 1: Foundation & Domain Model (Week 1-2)
- Value objects (identifiers, status, actor)
- AggregateRoot base class
- Initiative, Plan, Evidence aggregates
- Domain events (CloudEvents 1.0)
- Secondary ports (interfaces)

#### Phase 2: Application Layer (Week 2-3)
- Dispatcher implementation
- Middleware pipeline (auth, validation, transaction)
- Command handlers (write operations)
- Query handlers (read operations)
- DTOs and primary ports

#### Phase 3: Infrastructure Layer (Week 3-4)
- FileEventStore adapter
- JsonRepository adapter
- MarkdownAdapter (derived views)
- Projection handlers
- InMemoryEventBus

#### Phase 4: Interface Layer (Week 4-5)
- CLI main entry point
- Subcommand groups
- Natural language parser
- Output formatters
- Sub-agent context handling

#### Phase 5: Integration & Testing (Week 5-6)
- BDD feature tests
- Integration tests
- E2E CLI tests
- Architectural tests (no dependency violations)
- Performance benchmarks

#### Phase 6: Migration & Documentation (Week 6)
- Migration tool v2 -> v3
- Updated SKILL.md
- Updated CLAUDE.md SOPs
- ADRs documentation

#### Dependencies Between Phases
```
Phase 1 (Domain) <- Phase 2 (Application) <- Phase 3 (Infrastructure)
                                               |
                                               v
                         Phase 4 (Interface) <- Phase 5 (Testing)
                                               |
                                               v
                                         Phase 6 (Migration)
```

#### Success Criteria
| Criterion | Target |
|-----------|--------|
| Test Pass Rate | 100% |
| Domain Test Coverage | > 95% |
| Dependency Violations | 0 |
| Event Sourcing Active | All state changes |
| CQRS Separation | Complete |
| CLI Parity | All v2.x commands |
| Documentation | Complete |
| Migration | v2.x data preserved |

---

## L2: Strategic Vision

### Long-Term Vision

Work-Tracker v3.0 establishes the foundation for a **behavior and workflow guardrails framework** that:

1. **Solves Context Rot**: By offloading state to filesystem (JSON SSOT, event logs), Claude agents maintain consistent context across sessions without degradation from context window pressure.

2. **Enables Autonomous Sub-agent Work**: With a proper permission model, main Claude agents can safely delegate work to sub-agents while maintaining control over critical operations (completion, deletion, consent).

3. **Provides Complete Audit Trail**: Event sourcing ensures every state change is recorded, enabling time-travel debugging, compliance auditing, and state reconstruction.

4. **Integrates with Enterprise Systems**: The ACL pattern allows Work-Tracker to sync with Azure DevOps (and potentially other systems) without polluting the clean domain model.

5. **Captures Organizational Wisdom**: The Knowledge Capture bounded context transforms ad-hoc learnings into structured, searchable, linkable knowledge assets.

### Trade-offs Accepted

| Trade-off | Accepted Downside | Benefit Gained |
|-----------|-------------------|----------------|
| Ground-up rewrite | Lost familiarity, migration needed | Clean architecture, no legacy debt |
| Event sourcing | Storage overhead, complexity | Complete audit trail, time travel |
| CQRS separation | Eventual consistency | Optimized read/write paths |
| Sub-agent restrictions | Reduced parallelization | Safety, SOP compliance |
| JSON as SSOT | Two-step sync to markdown | No data loss on regeneration |

### Implications for Jerry Framework

Work-Tracker v3.0 becomes the **reference implementation** for Jerry's skill architecture:

1. **Hexagonal Pattern**: Other skills should follow the same ports/adapters structure
2. **Event Sourcing**: Jerry's core should adopt event-based state management
3. **Permission Model**: Agent governance applies to all Jerry skills
4. **Knowledge Integration**: Work items link to knowledge items across the framework

### Key Wisdom for Implementation

1. **Start small, verify often** - Implement one aggregate fully before moving to the next
2. **Honor the boundaries** - Domain layer has NO external dependencies
3. **Prioritize user experience** - Claude agents are primary users
4. **Preserve audit trail** - Every state change is an event
5. **Document as you go** - Update WORKTRACKER.md with every task change
6. **Respect the user** - Consent is sacred, never bypass it
7. **Prepare for compaction** - Context limit is real, plan for it
8. **The ACL is your shield** - ADO concepts must not leak into domain

---

## References

### Source Documents
- `docs/knowledge/dragonsbelurkin/glimmering-brewing-lake-v3.md` (410KB, 4732 lines)

### External References
- [Hexagonal Architecture - Alistair Cockburn](https://alistair.cockburn.us/hexagonal-architecture/)
- [Domain-Driven Design - Eric Evans (2003)](https://www.domainlanguage.com/ddd/)
- [ADO REST API Documentation](https://learn.microsoft.com/en-us/rest/api/azure/devops/wit/)
- [Anti-Corruption Layer Pattern - Microsoft Azure](https://learn.microsoft.com/en-us/azure/architecture/patterns/anti-corruption-layer)
- [Cockburn Use Case Template](https://www.cs.otago.ac.nz/coursework/cosc461/uctempla.htm)
- [Context Rot Research - Chroma](https://research.trychroma.com/context-rot)

---

*Generated by ps-researcher agent (v2.0.0)*
*Extraction completed: 2026-01-09*
