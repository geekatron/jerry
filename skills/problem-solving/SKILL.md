# Problem-Solving Skill

> Domain use case invocation and structured problem decomposition.

---

## Purpose

The Problem-Solving skill provides a structured approach to decomposing complex
problems, invoking domain use cases, and ensuring evidence-based decision making.
It bridges natural language requests to hexagonal core operations.

---

## Commands

### Solve Problem

Decompose and solve a problem using domain use cases.

```
@problem-solving solve <problem_description>
```

**Process:**
1. Analyze the problem statement
2. Identify relevant domain concepts
3. Decompose into sub-problems
4. Map to available use cases
5. Execute use cases in order
6. Synthesize results

**Example:**
```
@problem-solving solve "Track a new feature request for user dashboard"
```

**Output:**
```
Problem Analysis
━━━━━━━━━━━━━━━━

Input: "Track a new feature request for user dashboard"

Domain Concepts Identified:
  - Work Item (aggregate)
  - Feature (work item type)
  - Dashboard (context/tag)

Decomposition:
  1. Create work item with type=feature
  2. Set appropriate priority
  3. Add context tags
  4. Link to related items if any

Use Case Mapping:
  → CreateWorkItem(title, type=feature, tags=[dashboard])

Execution:
  Running: CreateWorkItem...
  Result: WORK-042 created

Solution:
  Created feature request WORK-042: "User dashboard feature"

  Next Steps:
  - Add detailed description
  - Define acceptance criteria
  - Create child tasks for implementation
```

---

### Decompose Problem

Break down a complex problem without executing.

```
@problem-solving decompose <problem_description> [--depth DEPTH]
```

**Arguments:**
- `problem_description`: The problem to decompose
- `--depth`: Decomposition depth (`shallow`, `deep`) (default: `shallow`)

**Example:**
```
@problem-solving decompose "Implement caching for database queries" --depth deep
```

**Output:**
```
Problem Decomposition
━━━━━━━━━━━━━━━━━━━━━

Problem: "Implement caching for database queries"

Level 1 - Major Components:
├── 1. Define caching abstraction (domain)
│   ├── 1.1 Define ICache port interface
│   ├── 1.2 Define cache key value objects
│   └── 1.3 Define cache policies
│
├── 2. Implement cache adapter (infrastructure)
│   ├── 2.1 Choose cache backend (in-memory vs external)
│   ├── 2.2 Implement adapter for chosen backend
│   └── 2.3 Handle serialization/deserialization
│
├── 3. Integrate with repositories (application)
│   ├── 3.1 Create cached repository decorator
│   ├── 3.2 Define cache invalidation rules
│   └── 3.3 Configure TTL policies
│
└── 4. Testing and validation
    ├── 4.1 Unit tests for cache adapter
    ├── 4.2 Integration tests for cached repository
    └── 4.3 Performance benchmarks

Dependencies:
  1 → 2 → 3 → 4 (sequential)
  1.1, 1.2, 1.3 (parallel)

Estimated Complexity: Medium
Recommended Approach: Create PLAN file first

Command to proceed:
  /architect Implement caching for database queries
```

---

### Research Topic

Research a topic with evidence and citations.

```
@problem-solving research <topic> [--depth DEPTH] [--sources SOURCES]
```

**Arguments:**
- `topic`: Topic to research
- `--depth`: Research depth (`quick`, `thorough`) (default: `quick`)
- `--sources`: Source types (`web`, `codebase`, `docs`, `all`) (default: `all`)

**Example:**
```
@problem-solving research "cache invalidation strategies" --depth thorough
```

**Output:**
```
Research: Cache Invalidation Strategies
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## Summary

Cache invalidation is one of the "two hard things in computer science"
(along with naming things and off-by-one errors). Key strategies include
TTL-based expiration, event-driven invalidation, and write-through caching.

## Key Strategies

### 1. Time-To-Live (TTL)
- Set expiration time on cached entries
- Simple but may serve stale data
- Best for: Read-heavy, tolerance for staleness

### 2. Event-Driven Invalidation
- Invalidate cache on relevant domain events
- More complex but ensures consistency
- Best for: Write-heavy, consistency critical

### 3. Write-Through
- Update cache synchronously with write
- Ensures cache always matches source
- Best for: Balanced read/write, consistency required

### 4. Cache-Aside (Lazy Loading)
- Application manages cache explicitly
- Most flexible, most complex
- Best for: Variable access patterns

## Recommendation for Jerry

Given hexagonal architecture:
- Define ICache port in domain
- Implement event-driven invalidation via domain events
- Use TTL as fallback safety net

## References

1. Fowler, M. "Cache Invalidation"
   https://martinfowler.com/bliki/TwoHardThings.html

2. AWS. "Caching Strategies"
   https://docs.aws.amazon.com/...

3. Redis. "Cache Invalidation Patterns"
   https://redis.io/docs/...

## Document Created

Saved to: docs/research/CACHE_INVALIDATION_STRATEGIES.md
```

---

### Invoke Use Case

Directly invoke a domain use case.

```
@problem-solving invoke <use_case> [--args ARGS]
```

**Arguments:**
- `use_case`: Use case name (e.g., `CreateWorkItem`, `CompleteWorkItem`)
- `--args`: JSON arguments for the use case

**Example:**
```
@problem-solving invoke CreateWorkItem --args '{"title": "Add caching", "type": "feature"}'
```

**Output:**
```
Use Case Invocation
━━━━━━━━━━━━━━━━━━━

Use Case: CreateWorkItem
Arguments:
  title: "Add caching"
  type: feature

Validation: ✓ PASS

Execution:
  → Loading repository adapter
  → Creating work item aggregate
  → Persisting to storage
  → Emitting WorkItemCreated event

Result:
  Success: true
  Work Item: WORK-043
  Events: [WorkItemCreated]
```

---

## Problem-Solving Framework

### MECE Decomposition

Decompose problems using Mutually Exclusive, Collectively Exhaustive (MECE):

```
Problem
├── Category A (mutually exclusive from B, C)
│   ├── Sub-problem A1
│   └── Sub-problem A2
├── Category B
│   └── Sub-problem B1
└── Category C
    ├── Sub-problem C1
    └── Sub-problem C2
```

### Evidence-Based Decisions

All recommendations must include:
1. **Citation**: Source of information
2. **Context**: When/why this applies
3. **Trade-offs**: Pros and cons
4. **Confidence**: High/Medium/Low

### Domain Mapping

Map natural language to domain concepts:

| Natural Language | Domain Concept |
|------------------|----------------|
| "track work" | WorkItem aggregate |
| "complete task" | CompleteWorkItem command |
| "list items" | GetWorkItems query |
| "find by status" | GetWorkItemsByStatus query |

---

## Available Use Cases

### Commands (Write Operations)

| Use Case | Description | Arguments |
|----------|-------------|-----------|
| CreateWorkItem | Create new work item | title, type, priority |
| UpdateWorkItem | Update work item | id, fields to update |
| CompleteWorkItem | Mark as completed | id, notes |
| DeleteWorkItem | Remove work item | id |

### Queries (Read Operations)

| Use Case | Description | Arguments |
|----------|-------------|-----------|
| GetWorkItem | Get single item | id |
| GetWorkItems | List items | filters |
| SearchWorkItems | Full-text search | query |
| GetWorkItemSummary | Get summary stats | time_range |

---

## Execution

This skill invokes use cases via:

```bash
python scripts/invoke_use_case.py <use_case> <args>
```

The script:
1. Parses arguments
2. Loads appropriate adapter implementations
3. Constructs use case with dependencies
4. Executes and returns result
