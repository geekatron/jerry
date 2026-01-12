# ECW Framework: Comprehensive Lessons Learned

> **Research Date:** 2026-01-07
> **Sources:** 60+ markdown files from docs/knowledge/dragonsbelurkin/
> **Purpose:** Synthesize all learnings from ECW v1-v3 for Jerry Work Tracker implementation
> **Status:** DECISION-GRADE (Validation: 19/19 criteria met)

---

## Executive Summary

Analysis of 60+ ECW artifacts reveals a mature, well-documented framework that evolved through three major versions. The key learnings fall into five categories:

1. **Architectural Patterns** - Blackboard, Event Sourcing, CQRS, Hexagonal
2. **Process Discipline** - 26 Hard Rules, SOPs, Three-Tier Enforcement
3. **Problem-Solving** - 7-Step Meta-Framework, Domain-Specific Playbooks
4. **Agent Orchestration** - 8 Specialized Agents, Capability-Based Self-Selection
5. **Resilience Patterns** - MAPE-K Self-Healing, Circuit Breaker, Consent Enforcement

**Critical Insight:** The ECW framework's sophistication indicates significant investment. Jerry should adopt these patterns wholesale rather than reinventing them.

---

## 1. Architectural Patterns to Adopt

### 1.1 Blackboard Pattern for Agent Orchestration

**Source:** `aspirations/blackboard/*.md` (13 documents)

**What It Is:**
- Shared knowledge repository (blackboard) where agents post and claim signals
- Capability-based self-selection (agents choose tasks matching their skills)
- Alternative to rigid coordinator-worker patterns

**Evidence:**
> "Blackboard re-emerged for LLM systems: 13-57% improvement over master-slave" (ArXiv 2025 research)

**Why It Matters for Jerry:**
- Work Tracker will have multiple agents (analyst, researcher, validator)
- Blackboard enables loose coupling between agents
- Signals survive context compaction (persisted to file/DB)

**Pattern Implementation:**
```
Signal Lifecycle: POSTED → CLAIMED → COMPLETED/FAILED/EXPIRED
Agent Claims: Optimistic locking with version check
Persistence: SQLite event store + file-based signal bridge
```

**What I'd Do Differently:**
- Use Redis Streams instead of filesystem for signal bus
- Implement signal expiration/timeout from day 1
- Monitor signal queue depth continuously

---

### 1.2 Event Sourcing with CloudEvents 1.0

**Source:** `glimmering-brewing-lake.md`, `REVISED-ARCHITECTURE-v3.0.md`

**What It Is:**
- All state changes persisted as immutable events
- State reconstructed by replaying events
- Snapshots for performance optimization

**User Requirement:** "CloudEvents will be our Event Schema"

**CloudEvents Structure:**
```json
{
  "specversion": "1.0",
  "type": "com.jerry.worktracker.task.completed.v1",
  "source": "/jerry/worktracker/tasks/TASK-001",
  "id": "evt-a1b2c3d4",
  "time": "2026-01-07T14:30:00Z",
  "data": { ... }
}
```

**Lessons:**
- Event schema versioning required from day 1
- Snapshots are CACHE, events are TRUTH
- Projections enable optimized read models

**What I'd Do Differently:**
- Define event upgrade/downgrade paths upfront
- Include correlation IDs for distributed tracing
- Plan snapshot frequency based on aggregate size

---

### 1.3 Three Aggregate Roots with Eventual Consistency

**Source:** `AGGREGATE_ROOT_ANALYSIS.md`, user feedback

**Problem:**
> "We tried using Work Tracker (ADO Project) as AR - very slow. We tried Phase (ADO Epic) - also slow."

**Solution (Vernon's Small Aggregates Principle):**

| Aggregate | Contains | Consistency |
|-----------|----------|-------------|
| **Task** (Primary) | Task + Subtasks | Immediate |
| **Phase** (Secondary) | Phase + TaskId refs | Eventual |
| **Plan** (Tertiary) | Plan + PhaseId refs | Eventual |

**Evidence:**
> "70% of aggregates consist of just the root entity plus value-type properties" (Niclas Hedhman study, cited by Vernon)

**Event Flow:**
```
Task.complete() → TaskCompletedEvent → [immediate response]
                                     ↓
                  [async] PhaseProgressProjection recalculates
                                     ↓
                  [async] PlanProgressProjection updates
```

---

### 1.4 Hexagonal Architecture (Ports & Adapters)

**Source:** `work_tracker_architecture_hexagonal_ddd_cqrs_layered_teaching_edition.md`

**Three-Level Explanation:**

| Level | Mental Model |
|-------|--------------|
| **ELI5** | Castle with different gates - same rules inside |
| **Junior** | Ports (interfaces) + Adapters (implementations) |
| **Architect** | Primary/Secondary ports, Capability surfaces, Repository chains |

**Key Principles:**
1. Domain owns abstractions (no external imports)
2. Adapters are thin (logic in domain/application)
3. Different capability surfaces (Public API ≠ Admin API)
4. Repository chain: `IRepository` ← `FileRepository` ← `MarkdownAdapter`

**Architectural Smells to Avoid:**
```
SMELL: "Just this once" logic in adapters
SMELL: Repository returns ORM entities
SMELL: Cross-aggregate writes in one transaction
SMELL: Queries reusing command models
SMELL: Direct calls between bounded contexts
```

---

## 2. Process Discipline: 26 Hard Rules

**Source:** `exemplars/rules/hard-rules.md`

### Critical Rules for Jerry

| Rule | Gate | What It Prevents |
|------|------|-----------------|
| **Rule 9** | Before implementation | TDD: Test FIRST (RED) |
| **Rule 20** | Before integration features | Architectural feasibility proof |
| **Rule 21** | Before claiming "integrated" | E2E tests (not mocks) |
| **Rule 22** | Before commit | Integration proof required |
| **Rule 24** | Before "Complete" status | 90% checkbox threshold |
| **Rule 26** | Before spawning agents | Design review approval |

### Integration Theater (Anti-Pattern)

**Source:** Rules 20-22, Phase 32.G failure

**What Happened:**
- Feature claimed integration with hooks
- Tests passed via mocks
- Real execution failed (hooks can't access MCP context)

**Lesson (LES-030):**
> "Hooks run as subprocesses, cannot access MCP context. Use file-based bridge."

**Prevention:**
- E2E tests in production-like environment
- Integration proof with actual execution evidence
- Document process boundaries explicitly

---

## 3. Standard Operating Procedures (SOPs)

**Source:** `exemplars/rules/sop.md`

### SOP-I: Implementation (MUST ADOPT)

```
SOP-I.1: BDD + TDD approach (Red/Green/Refactor)
SOP-I.2: Test pyramid: unit, integration, system, contract, architecture, E2E
SOP-I.3: NO placeholders, stubs, or FALSE data in tests
SOP-I.4: ALL tests MUST be real and validatable with evidence
SOP-I.5: Edge cases tested alongside happy path
SOP-I.6: Plan for negative, edge cases, and failure scenarios
```

### SOP-DES: Design Artifacts (MUST ADOPT)

Required design artifacts:
- Use Cases + Use Case Diagrams
- Class Diagrams, Component Diagrams
- Activity Diagrams, State Machine Diagrams
- Sequence Diagrams, Communication Diagrams
- JSON Schemas, OpenAPI Specifications
- Playbooks + Runbooks

### SOP-ENF: Design Review Enforcement (MUST ADOPT)

**Four-Tier Enforcement:**

| Tier | Name | Mechanism | Behavior |
|------|------|-----------|----------|
| 1 | ADVISORY | CLAUDE.md | Display reminder |
| 2 | SOFT | Template prompts | Warn, don't block |
| 3 | MEDIUM | Pre-commit hooks | Block commits |
| 4 | **HARD** | Agent-level gate | Refuse to proceed |

**Approval Protocol:**
1. Present DESIGN SUMMARY
2. List proposed artifacts and locations
3. Ask "May I proceed?"
4. WAIT for explicit approval
5. ONLY THEN proceed

---

## 4. Problem-Solving Meta-Framework

**Source:** `frameworks/problemsolving/problem_solving_meta_framework.md`

### 7-Step Universal Framework

```
1. FRAME (5W1H)      ← Explain so a 5-year-old understands
2. CLASSIFY          ← Simple/Complicated/Complex/Chaotic (Cynefin)
3. DIAGNOSE (WHY)    ← 5 Whys / Fishbone / Abduction
4. IDEATE (DIVERGE)  ← No evaluation, no feasibility
5. DECIDE (CONVERGE) ← Tradeoffs: Risk, Cost, Time, Reversibility
6. ACT               ← Execute with monitoring; ready to abort
7. VERIFY & LEARN    ← Confirm outcome; institutionalize learning
```

### Common Failure Modes

| Failure | Consequence |
|---------|-------------|
| Solving before framing | Wrong problem solved perfectly |
| Wrong classification | Wrong approach applied |
| No divergence | Best idea never considered |
| No red team | Blind spots undetected |
| No learning loop | Same mistakes repeated |

### Domain-Specific Playbooks

| Domain | Core Loop | Prior Art |
|--------|-----------|-----------|
| **Software** | TRIAGE → DIAGNOSE → FIX → VERIFY → LEARN | Google SRE |
| **Security** | PREPARE → DETECT → CONTAIN → ERADICATE → RECOVER | NIST 800-61 |
| **Research** | Observe → Hypothesize → Design → Run → Analyze → Conclude | Scientific Method |

---

## 5. Agent Orchestration System

**Source:** `skills/problem-solving/agents/*.md` (8 files)

### 8 Specialized Agents

| Agent | Role | Cognitive Mode |
|-------|------|----------------|
| **ps-researcher** | Deep research, information gathering | Divergent |
| **ps-analyst** | Analysis of gathered information | Convergent |
| **ps-synthesizer** | Cross-document pattern extraction | Meta-analysis |
| **ps-architect** | ADR creation, architectural decisions | Design |
| **ps-investigator** | Failure analysis, debugging | Root cause |
| **ps-validator** | Constraint checking (binary) | Validation |
| **ps-reviewer** | Quality assessment (spectrum) | Quality |
| **ps-reporter** | Status documentation | Reporting |

### Mandatory Persistence (c-009)

> "Every agent output MUST be persisted to file. Transient-only output is forbidden."

**File Locations:**
```
docs/research/{ps-id}-{entry-id}-{topic-slug}.md
docs/analysis/{ps-id}-{entry-id}-{analysis-type}.md
docs/decisions/{ps-id}-{entry-id}-adr-{slug}.md
docs/investigations/{ps-id}-{entry-id}-investigation.md
docs/synthesis/{ps-id}-{entry-id}-synthesis.md
```

### Agent Workflow

```
ps-researcher → ps-analyst → ps-synthesizer → ps-architect
                    ↓              ↓              ↓
                ps-investigator ←──┴──────────────┘
                    ↓
                ps-validator
                    ↓
                ps-reviewer
                    ↓
                ps-reporter
```

---

## 6. Self-Healing Architecture

**Source:** `aspirations/self-healing/*.md` (3 files)

### MAPE-K Control Loop

```
MONITOR → ANALYZE → PLAN → EXECUTE → KNOWLEDGE
   ↓         ↓        ↓        ↓          ↓
Health    Symptom   Strategy  Circuit   Pattern
Monitor   Analyzer  Planner   Breaker   Database
```

### Failure Categories & Recovery

| Category | Example | Recovery Strategy |
|----------|---------|-------------------|
| TRANSIENT | Timeout | Retry with exponential backoff |
| VALIDATION | Invalid status | Normalize input |
| RESOURCE | File not found | Escalate to user |
| CORRUPTION | Checksum mismatch | Repair from backup |
| UNKNOWN | Unexpected error | Escalate with context |

### Four-Level Enforcement (Consent)

| Level | Mechanism | Behavior |
|-------|-----------|----------|
| **ADVISORY** | Recommendations | Display warning |
| **SOFT** | Consent prompts | Ask before proceeding |
| **MEDIUM** | Agent restrictions | Block subagent actions |
| **HARD** | Hook blocks | Refuse to execute |

### Circuit Breaker Pattern

```
CLOSED (normal) → HALF_OPEN (testing) → OPEN (blocked)
      ↑                                       │
      └───────────── after timeout ───────────┘
```

---

## 7. Critical Constraints Discovered

### LES-030: Hook Subprocess Isolation

> "Hooks run as subprocesses, CANNOT access MCP context. Cannot call Task tool or MCP services directly. File-based bridge is required workaround."

**Impact:** Any orchestration via hooks must use two-phase approach:
1. Hook detects/writes signal
2. External process reads signal and executes

### c-015: No Recursive Subagents

> "Task tool filtered at adapter level. Subagents cannot spawn subagents."

**Impact:** Agent depth is limited to 1 level. Orchestrator pattern required.

### c-009: Mandatory Persistence

> "All agent outputs must be persisted to file. Transient-only responses are forbidden."

**Impact:** Every agent invocation must produce a file artifact.

---

## 8. What I'd Do Differently (5W1H Analysis)

### WHO should implement this?
- Jerry framework authors with understanding of ECW patterns
- Must understand DDD, Event Sourcing, CQRS

### WHAT should change from ECW?
1. **Use Task as primary AR** (not Plan or Phase)
2. **Use Redis/message queue** (not filesystem for signals)
3. **Implement backup/health checks from day 1**
4. **Test E2E before claiming integration**
5. **Adopt 26 Hard Rules as gates**

### WHERE should changes be made?
- Domain layer: Small aggregates, strongly typed IDs
- Infrastructure: Message queue, not file signals
- Process: Three-tier enforcement from start

### WHEN should these be implemented?
- Phase 1: Domain model with correct aggregates
- Phase 2: Event sourcing infrastructure
- Phase 3: Self-healing patterns
- Phase 4: Agent orchestration

### WHY make these changes?
- ECW had 128+ failing tests (test isolation)
- Plan/Phase as AR = slow performance (user confirmed)
- File-based signals = eventual consistency issues
- Missing E2E tests = integration theater

### HOW to avoid ECW's mistakes?
1. **Test isolation** - Fresh fixtures per test, no global state
2. **Small aggregates** - Task as AR, not Plan
3. **Event schema versioning** - Plan migrations from day 1
4. **E2E proof required** - Rule 21/22 enforcement
5. **Defense in depth** - Three-tier enforcement

---

## 9. Patterns to Adopt Wholesale

### PAT-048: Three-Tier Enforcement
Soft (template) → Medium (pre-commit) → Hard (agent gate)

### PAT-049: Progressive Thresholds
Research quality: ≥16/19 criteria = DECISION-GRADE

### PAT-051: Pre-Commit Validation
Block commits that violate quality gates

### PAT-052: Agent-Level Gate
Agent refuses to write incomplete artifacts

### PAT-070: Capability-Based Self-Selection
Agents choose signals matching their capabilities

---

## 10. Templates to Adopt

| Template | Purpose | Location |
|----------|---------|----------|
| **ADR** | Architecture decisions | `templates/adr.md` |
| **Analysis** | Deep analysis | `templates/deep-analysis.md` |
| **Investigation** | Root cause analysis | `templates/investigation.md` |
| **Research** | Evidence-based inquiry | `templates/research.md` |
| **Review** | Quality assessment | `templates/review.md` |
| **Synthesis** | Cross-document patterns | `templates/synthesis.md` |

---

## 11. Validation Status

| Category | Status | Score |
|----------|--------|-------|
| W-DIMENSION COVERAGE | ✅ COMPLETE | 6/6 |
| FRAMEWORK APPLICATION | ✅ COMPLETE | 5/5 |
| EVIDENCE & GAPS | ✅ COMPLETE | 4/4 |
| OUTPUT SECTIONS | ✅ COMPLETE | 4/4 |

**Quality Status:** DECISION-GRADE (19/19 criteria met)

---

## 12. References

### Primary ECW Sources
1. `docs/knowledge/dragonsbelurkin/glimmering-brewing-lake.md` (v3 design)
2. `docs/knowledge/dragonsbelurkin/glimmering-brewing-lake-v1.md` (v1 design)
3. `docs/knowledge/dragonsbelurkin/history/REVISED-ARCHITECTURE-v3.0.md`
4. `docs/knowledge/dragonsbelurkin/aspirations/blackboard/*.md` (13 files)
5. `docs/knowledge/dragonsbelurkin/aspirations/self-healing/*.md` (3 files)

### Exemplar Sources
6. `docs/knowledge/exemplars/rules/hard-rules.md`
7. `docs/knowledge/exemplars/rules/sop.md`
8. `docs/knowledge/exemplars/frameworks/problemsolving/*.md`
9. `docs/knowledge/exemplars/architecture/*.md`
10. `docs/knowledge/exemplars/templates/*.md`

### Industry References
11. Vaughn Vernon - *Implementing Domain-Driven Design*
12. Eric Evans - *Domain-Driven Design*
13. CloudEvents Specification 1.0 (CNCF)
14. Google SRE Handbook
15. NIST SP 800-61r2 (Incident Response)

---

*Document Version: 1.0*
*Created: 2026-01-07*
*Author: Claude (Distinguished Systems Engineer persona)*
