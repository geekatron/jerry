# TASK-175: Add SV-006 Circular Detection Implementation Details

<!--
TEMPLATE: Task
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.6
ENABLER: EN-014 (Domain Context Files Implementation)
WORKFLOW: EN-014--WORKFLOW-schema-extension.md
ISSUE: nse-qa NC-m-002, DISC-007
-->

---

## Frontmatter

```yaml
id: "TASK-175"
work_type: TASK
title: "Add SV-006 Circular Detection Implementation Details"
description: |
  Address nse-qa NC-m-002 and DISC-007 IMPL-004: Add algorithm/pseudocode for
  SV-006 (circular relationship detection) to TDD Section 5.2.

classification: ENABLER
status: DONE
resolution: COMPLETED
priority: HIGH
assignee: "Claude"
created_by: "Claude"
created_at: "2026-01-29T12:30:00Z"
updated_at: "2026-01-29T12:30:00Z"

parent_id: "EN-014"

tags:
  - "tdd-improvement"
  - "validation"
  - "algorithm"
  - "graph-analysis"
  - "nse-qa-nc-m-002"
  - "disc-007"

effort: 2
acceptance_criteria: |
  - TDD Section 5.2 updated with SV-006 algorithm details
  - Pseudocode or Python implementation sketch provided
  - Algorithm complexity documented (O(V+E))
  - Edge cases documented
  - nse-qa NC-m-002 addressed
  - DISC-007 IMPL-004 addressed

due_date: null

activity: DOCUMENTATION
original_estimate: 2
remaining_work: 0
time_spent: 2
```

---

## State Machine

**Current State:** `DONE`

```
BACKLOG → IN_PROGRESS → DONE
              ↓
           BLOCKED
```

---

## Content

### Description

This task addresses nse-qa NC-m-002 from the TASK-167 quality review and DISC-007:

> **NC-m-002:** Semantic validation rule SV-006 (circular relationship detection)
> lacks implementation details.
>
> **Recommendation:** Provide algorithm or pseudocode for cycle detection.

### Current TDD Content (Section 5.2)

The TDD only states:
```
| SV-006 | Circular relationship detection | Graph analysis |
```

No algorithm, pseudocode, or complexity analysis is provided.

### Required Changes

**Location:** `docs/design/TDD-EN014-domain-schema-v2.md` Section 5.2

**Content to Add:**

```markdown
### SV-006: Circular Relationship Detection

**Problem:** Detect circular relationships in entity relationship graphs to prevent
infinite traversal during extraction.

**Example Circular Relationship:**
```yaml
entities:
  blocker:
    relationships:
      - type: "blocks"
        target: "commitment"  # blocker → commitment

  commitment:
    relationships:
      - type: "triggers"
        target: "action_item"  # commitment → action_item

  action_item:
    relationships:
      - type: "resolves"
        target: "blocker"  # action_item → blocker (CYCLE!)
```

**Algorithm: Depth-First Search (DFS) Cycle Detection**

```python
def sv006_circular_relationships(domain_data: dict) -> list[ValidationError]:
    """
    Detect circular relationships using DFS.

    Algorithm: For each entity, perform DFS and track visited nodes.
    If we encounter a node already in the current path, a cycle exists.

    Complexity: O(V + E) where V = entities, E = relationships
    """
    entities = domain_data.get("entity_definitions", {})
    errors = []

    # Build adjacency list
    graph: dict[str, list[str]] = {}
    for entity_name, entity_def in entities.items():
        graph[entity_name] = []
        for rel in entity_def.get("relationships", []):
            target = rel.get("target")
            if target:
                graph[entity_name].append(target)

    def dfs(node: str, path: set[str], visited: set[str]) -> list[str]:
        """Returns cycle path if found, empty list otherwise."""
        if node in path:
            return list(path) + [node]  # Cycle detected
        if node in visited:
            return []  # Already fully explored

        path.add(node)
        for neighbor in graph.get(node, []):
            cycle = dfs(neighbor, path, visited)
            if cycle:
                return cycle

        path.remove(node)
        visited.add(node)
        return []

    # Check all entities as potential cycle starts
    visited: set[str] = set()
    for entity in graph:
        if entity not in visited:
            cycle = dfs(entity, set(), visited)
            if cycle:
                errors.append(ValidationError(
                    path=f"entity_definitions",
                    rule="SV-006",
                    message=f"Circular relationship detected: {' → '.join(cycle)}",
                    severity="error"
                ))

    return errors
```

**Complexity Analysis:**
- **Time:** O(V + E) - Each vertex and edge visited once
- **Space:** O(V) - Path tracking and visited set

**Edge Cases:**
1. Self-referential: `entity.relationships[].target == entity` → Detected
2. Two-node cycle: A → B → A → Detected
3. Disconnected components → Each component checked independently
4. No relationships → Valid (empty graph)

**Error Message Format:**
```json
{
  "path": "entity_definitions",
  "rule": "SV-006",
  "message": "Circular relationship detected: blocker → commitment → action_item → blocker",
  "severity": "error"
}
```
```

### Dependencies

**Blocked By:** None

**Blocks:**
- TASK-170: TDD Adversarial Review (must address minor issues first)

### Related Discoveries

This task addresses DISC-007 gap:
- **IMPL-004 (SV-006 Algorithm):** Algorithm and pseudocode provided

### Acceptance Criteria

- [ ] TDD Section 5.2 updated with SV-006 algorithm
- [ ] Python pseudocode provided
- [ ] Complexity analysis documented (O(V+E))
- [ ] Example circular relationship shown
- [ ] Edge cases documented
- [ ] Error message format specified
- [ ] nse-qa NC-m-002 addressed

### Related Items

- Parent: [EN-014: Domain Context Files Implementation](./EN-014-domain-context-files.md)
- Issue Source: [en014-task167-iter1-qa.md](./qa/en014-task167-iter1-qa.md) NC-m-002
- Discovery: [DISC-007: TDD Validation Implementation Gap](./EN-014--DISC-007-tdd-validation-implementation-gap.md)
- Blocks: [TASK-170: TDD Adversarial Review](./TASK-170-tdd-adversarial-review.md)

---

## Time Tracking

| Metric            | Value    |
|-------------------|----------|
| Original Estimate | 2 hours  |
| Remaining Work    | 2 hours  |
| Time Spent        | 0 hours  |

---

## Evidence

### Deliverables

| Deliverable | Type | Link | Status |
|-------------|------|------|--------|
| TDD SV-006 Algorithm Details | Markdown | docs/design/TDD-EN014-domain-schema-v2.md | DONE |

### Verification

- [ ] Algorithm documented with pseudocode
- [ ] Complexity analysis included
- [ ] Edge cases covered
- [ ] Error format specified
- [ ] Reviewed by: (self-review)

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-01-29 | Created | Created per DISC-007 IMPL-004 and nse-qa NC-m-002 |
| 2026-01-29 | DONE | Added Section 5.2.2 SV-006 Circular Relationship Detection Algorithm with DFS pseudocode, O(V+E) complexity analysis, edge cases table, and error message format. nse-qa NC-m-002 and DISC-007 IMPL-004 addressed. |
