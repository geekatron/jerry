# Aggregate Root Analysis for Work Tracker v3.0

> **Research Date:** 2026-01-07
> **Status:** COMPLETE
> **Decision:** Task-level Aggregate Root with Phase and Plan as separate ARs

---

## 1. Executive Summary

Based on research from authoritative DDD sources (Vernon, Evans, Young) and analysis of the previous ECW framework's lessons learned, we recommend:

| Aggregate Root | Contains | Consistency |
|----------------|----------|-------------|
| **Task** (Primary AR) | Task entity + Subtasks | Immediate |
| **Phase** (Secondary AR) | Phase entity + Task IDs (references only) | Eventual |
| **Plan** (Tertiary AR) | Plan entity + Phase IDs (references only) | Eventual |

This addresses the user's stated problem: *"We tried using Work Tracker (ADO Project) as AR - very slow. We tried Phase (ADO Epic) - also slow."*

---

## 2. Problem Statement (5W1H)

### WHO is affected?
- Claude Code instances managing large work trackers
- Users experiencing slow response times on task operations

### WHAT is the problem?
- Large aggregate roots cause performance degradation
- Concurrent modifications cause lock contention
- Full aggregate loading creates N+1 query problems

### WHERE does it manifest?
- Task completion operations (load entire Plan/Phase)
- Subtask check/uncheck operations
- Progress calculations (lock escalation)

### WHEN did it start?
- ECW v2.x with Plan as primary aggregate root
- Worsened as trackers grew beyond ~50 tasks

### WHY does it matter?
- Context rot is exacerbated by slow tool operations
- User experience degrades with larger projects
- System cannot scale horizontally

### HOW is it manifesting?
- Previous Claude session reported "very slow" with Plan AR
- Also reported "quite slow" with Phase AR

---

## 3. Research Findings

### 3.1 Vaughn Vernon's Four Rules for Aggregate Design

**Source:** *Implementing Domain-Driven Design* (2013), "Effective Aggregate Design" series

1. **Model True Invariants in Consistency Boundaries**
   - Only include entities that MUST remain transactionally consistent
   - Ask: "What business rule requires these entities to change together?"

2. **Design Small Aggregates**
   - Start with single entity per aggregate
   - Only add entities when true invariants require them
   - *"70% of aggregates consist of just the root entity plus value-type properties"* (Niclas Hedhman study)

3. **Reference Other Aggregates by Identity**
   - Never hold direct object references to other aggregates
   - Store only IDs/keys
   - Prevents accidental modification of other aggregates

4. **Use Eventual Consistency Outside the Boundary**
   - Cross-aggregate coordination via domain events
   - Accept temporary inconsistency

### 3.2 Vernon's ProjectOvation Case Study

Vernon's "Effective Aggregate Design" series uses a Scrum project management system identical to our hierarchy:

**Initial (Failed) Design:**
```
Project ← Release ← Sprint ← BacklogItem ← Task
(All in one aggregate)
```
**Result:** Severe performance degradation, high contention, transaction failures

**Refactored (Successful) Design:**
```
Aggregate 1: BacklogItem (contains Task children)
Aggregate 2: Sprint (references BacklogItem IDs)
Aggregate 3: Release (references Sprint IDs)
```

**Key Quote:**
> "A large-cluster Aggregate will never perform or scale well. It is more likely to become a nightmare leading only to failure."

### 3.3 The Cascading Delete Test

A practical rule for aggregate boundaries:

> "When considering aggregate structure, ask: should deleting the root delete all its children?"

Applied to Jerry Work Tracker:
- Delete Task → Should delete Subtasks ✓ (same aggregate)
- Delete Phase → Should delete Tasks? **Maybe** (could be eventual)
- Delete Plan → Should delete Phases? **Maybe** (could be eventual)

### 3.4 Eric Evans' Evolved Perspective (QCon 2009)

> "Aggregates turned out to be one of the most difficult patterns to apply... A much more useful view at aggregates is to look at them as **consistency boundaries for transactions, distributions and concurrency**."

This shifts focus from "what belongs together logically" to "what must change together atomically."

---

## 4. Analysis: Task vs Phase vs Plan as Aggregate Root

### 4.1 Option Analysis

| Level | As AR? | Pros | Cons |
|-------|--------|------|------|
| **Plan** | NO | Strong consistency | Lock contention, N+1 queries, cannot scale |
| **Phase** | MAYBE | Smaller than Plan | Still causes contention across tasks |
| **Task** | YES | Minimal contention, scales horizontally | Cross-task invariants need eventual consistency |

### 4.2 Invariants Analysis

**Question:** What business rules require immediate consistency?

| Invariant | Scope | Requires Same AR? |
|-----------|-------|-------------------|
| "Subtask completion affects task progress" | Task ← Subtask | YES |
| "All subtasks must be checked to complete task" | Task ← Subtask | YES |
| "Phase progress = average of task progress" | Phase ← Task | NO (derived) |
| "Plan progress = average of phase progress" | Plan ← Phase | NO (derived) |
| "Task must belong to exactly one phase" | Task → Phase | NO (referential) |

**Conclusion:** Only Task ↔ Subtask requires immediate consistency.

### 4.3 Recommended Aggregate Structure

```
┌─────────────────────────────────────────────────────────────────┐
│                    AGGREGATE ROOT: TASK                          │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │  Task                                                       │ │
│  │  ├── TaskId (strongly typed)                               │ │
│  │  ├── PhaseId (reference to Phase AR)                       │ │
│  │  ├── title, description, status                            │ │
│  │  ├── verification, evidence_refs[]                         │ │
│  │  └── subtasks: List[Subtask]  ◄── Child entities           │ │
│  │       ├── SubtaskId                                        │ │
│  │       ├── title                                            │ │
│  │       └── checked: bool                                    │ │
│  └────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                    AGGREGATE ROOT: PHASE                         │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │  Phase                                                      │ │
│  │  ├── PhaseId (strongly typed)                              │ │
│  │  ├── PlanId (reference to Plan AR)                         │ │
│  │  ├── title, description, status                            │ │
│  │  ├── task_ids: List[TaskId]  ◄── References only!          │ │
│  │  └── progress: float (derived via projection)              │ │
│  └────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                    AGGREGATE ROOT: PLAN                          │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │  Plan                                                       │ │
│  │  ├── PlanId (strongly typed)                               │ │
│  │  ├── InitiativeId (reference)                              │ │
│  │  ├── title, description, status                            │ │
│  │  ├── phase_ids: List[PhaseId]  ◄── References only!        │ │
│  │  └── progress: float (derived via projection)              │ │
│  └────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

---

## 5. Event Flow for Eventual Consistency

### 5.1 Task Completion Flow

```
1. User: "mark task 5.3 complete"
2. Load Task aggregate (small, fast)
3. Task.complete() validates:
   - All subtasks checked
   - Evidence attached (if required)
4. Task emits: TaskCompletedEvent
5. Persist Task (single small transaction)

--- EVENTUAL CONSISTENCY BOUNDARY ---

6. EventHandler receives TaskCompletedEvent
7. Load Phase aggregate
8. Phase recalculates progress from task projections
9. Phase emits: PhaseProgressUpdatedEvent
10. Persist Phase

--- EVENTUAL CONSISTENCY BOUNDARY ---

11. EventHandler receives PhaseProgressUpdatedEvent
12. Load Plan aggregate
13. Plan recalculates progress from phase projections
14. Plan emits: PlanProgressUpdatedEvent
15. Persist Plan
```

### 5.2 CloudEvents Format (Per User Requirement)

```json
{
  "specversion": "1.0",
  "type": "com.jerry.worktracker.task.completed.v1",
  "source": "/jerry/worktracker/tasks/TASK-001",
  "id": "evt-a1b2c3d4",
  "time": "2026-01-07T14:30:00Z",
  "datacontenttype": "application/json",
  "data": {
    "task_id": "TASK-001",
    "phase_id": "PHASE-001",
    "completed_by": {"type": "CLAUDE", "id": "main"},
    "subtasks_completed": 5,
    "evidence_count": 2
  }
}
```

---

## 6. Strongly Typed Identity Objects (Per User Requirement)

```python
# domain/value_objects/identifiers.py

from dataclasses import dataclass
from typing import NewType
import uuid

@dataclass(frozen=True)
class TaskId:
    """Strongly typed Task identifier."""
    value: str

    def __post_init__(self):
        if not self.value:
            raise ValueError("TaskId cannot be empty")

    @classmethod
    def generate(cls) -> "TaskId":
        return cls(f"TASK-{uuid.uuid4().hex[:8].upper()}")

    def __str__(self) -> str:
        return self.value

@dataclass(frozen=True)
class PhaseId:
    """Strongly typed Phase identifier."""
    value: str

    @classmethod
    def generate(cls) -> "PhaseId":
        return cls(f"PHASE-{uuid.uuid4().hex[:8].upper()}")

@dataclass(frozen=True)
class PlanId:
    """Strongly typed Plan identifier."""
    value: str

    @classmethod
    def generate(cls) -> "PlanId":
        return cls(f"PLAN-{uuid.uuid4().hex[:8].upper()}")

@dataclass(frozen=True)
class SubtaskId:
    """Strongly typed Subtask identifier - scoped to parent Task."""
    task_id: TaskId
    sequence: int

    def __str__(self) -> str:
        return f"{self.task_id.value}.{self.sequence}"
```

---

## 7. Performance Comparison (Projected)

| Operation | Plan as AR | Phase as AR | Task as AR |
|-----------|-----------|-------------|------------|
| Complete single task | O(n) load all | O(m) load phase | O(1) load task |
| Check subtask | O(n) | O(m) | O(1) |
| Concurrent task updates | Blocked | Partially blocked | Parallel |
| Horizontal scaling | Not possible | Limited | Full support |

Where:
- n = total tasks in plan
- m = tasks in phase
- O(1) = single task + subtasks only

---

## 8. References

### Primary Sources
1. **Vaughn Vernon** - *Implementing Domain-Driven Design* (2013)
2. **Vaughn Vernon** - "Effective Aggregate Design" (3-part series)
   - https://www.dddcommunity.org/library/vernon_2011/
3. **Eric Evans** - *Domain-Driven Design* (2003)
4. **Eric Evans** - QCon London 2009: "What I've Learned About DDD Since the Book"

### Secondary Sources
5. **Martin Fowler** - DDD Aggregate (bliki)
   - https://martinfowler.com/bliki/DDD_Aggregate.html
6. **Microsoft Learn** - Domain Events Design and Implementation
7. **Niclas Hedhman** - Aggregate sizing study (cited by Vernon)

### ECW Lessons Learned
8. `docs/knowledge/dragonsbelurkin/glimmering-brewing-lake.md` (v3.0 Strategic Design)
9. `docs/knowledge/dragonsbelurkin/history/REVISED-ARCHITECTURE-v3.0.md`

---

## 9. Decision Record

**Decision:** Implement three Aggregate Roots (Task, Phase, Plan) with eventual consistency.

**Rationale:**
- Evidence from Vernon's ProjectOvation case study
- User's direct experience with performance issues
- Alignment with "small aggregates" principle

**Consequences:**
- Cross-aggregate operations require domain events
- Progress calculations are eventually consistent
- More complex event handling infrastructure

**Status:** APPROVED FOR IMPLEMENTATION

---

*Document Version: 1.0*
*Last Updated: 2026-01-07*
