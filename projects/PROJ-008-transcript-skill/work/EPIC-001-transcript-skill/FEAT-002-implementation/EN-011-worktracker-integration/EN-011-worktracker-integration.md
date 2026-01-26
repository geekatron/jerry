# EN-011: Worktracker Integration

<!--
TEMPLATE: Enabler
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.5
-->

> **Type:** enabler
> **Status:** pending
> **Priority:** medium
> **Impact:** medium
> **Created:** 2026-01-26T00:00:00Z
> **Due:** TBD
> **Completed:**
> **Parent:** FEAT-002
> **Owner:** Claude
> **Target Sprint:** Sprint 4
> **Effort Points:** 5
> **Gate:** GATE-6 (Final Review)

---

## Summary

Implement integration between the transcript skill and Jerry worktracker, enabling extracted entities to be converted into work items. Action items become tasks, ideas become stories, and decisions become decision records. Uses suggestion-first approach with human approval.

**Technical Justification:**
- Closes the loop from meeting to action
- Suggestion-first respects user autonomy (DEC-003)
- Deep links maintain provenance to source
- Integration with existing worktracker workflow

---

## Benefit Hypothesis

**We believe that** integrating transcript entities with worktracker

**Will result in** seamless conversion of meeting insights to tracked work

**We will know we have succeeded when:**
- Action items can be converted to tasks
- Ideas can be converted to stories
- Decisions are recorded with rationale
- All work items link back to transcript source
- Human approval received at GATE-6

---

## Acceptance Criteria

### Definition of Done

- [ ] Suggestion generator implemented
- [ ] Task creation from action items working
- [ ] Story creation from ideas working
- [ ] Decision record creation working
- [ ] Deep links to transcript maintained
- [ ] Human approval workflow implemented
- [ ] Integration tests passing
- [ ] ps-critic review passed
- [ ] Human approval at GATE-6

### Technical Criteria

| # | Criterion | Verified |
|---|-----------|----------|
| AC-1 | Action items suggest as tasks | [ ] |
| AC-2 | Ideas suggest as stories | [ ] |
| AC-3 | Decisions create decision records | [ ] |
| AC-4 | Work items link to source transcript | [ ] |
| AC-5 | Human can approve/reject each suggestion | [ ] |
| AC-6 | Batch approval supported | [ ] |
| AC-7 | Work items follow Jerry ontology | [ ] |
| AC-8 | Existing worktracker integration maintained | [ ] |

---

## Children (Tasks)

### Task Inventory

| ID | Title | Status | Owner | Effort | Blocked By |
|----|-------|--------|-------|--------|------------|
| TASK-055 | Create Suggestion Generator Agent | pending | Claude | 2 | EN-010 |
| TASK-056 | Implement Task Creation Flow | pending | Claude | 1 | TASK-055 |
| TASK-057 | Implement Story Creation Flow | pending | Claude | 1 | TASK-055 |
| TASK-058 | Implement Decision Record Flow | pending | Claude | 1 | TASK-055 |

---

## Entity to Work Item Mapping

### Action Item → Task

```yaml
# Input: Action Item Entity
action_item:
  id: action-001
  description: "Send updated budget projections to finance team"
  assignee: speaker-002  # John Smith
  due_date: null
  priority: high
  source_cues: ["cue-045"]

# Output: Suggested Task
task:
  type: task
  title: "Send updated budget projections to finance team"
  description: |
    **From Meeting:** {meeting-title}
    **Speaker:** John Smith
    **Timestamp:** 00:15:30

    Original context: "John, can you send the updated projections by Friday?"

    [View in transcript](../07-mindmap/mindmap.md#action-001)
  owner: null  # For human to assign
  priority: high
  parent: null  # For human to assign to story/enabler
  tags: ["from-transcript", "action-item"]
```

### Idea → Story

```yaml
# Input: Idea Entity
idea:
  id: idea-001
  description: "We could automate the monthly report generation"
  proposer: speaker-003
  related_topic: topic-002
  source_cues: ["cue-078"]

# Output: Suggested Story
story:
  type: story
  title: "Automate monthly report generation"
  description: |
    **Proposed by:** Sarah Johnson
    **From Meeting:** {meeting-title}
    **Related Topic:** Process Improvements

    Original proposal: "What if we automated the monthly report generation?
    It takes about 4 hours each month and follows the same pattern."

    [View in transcript](../03-topics/topics.md#topic-002)
  acceptance_criteria: []  # For human to define
  tags: ["from-transcript", "idea", "automation"]
```

### Decision → Decision Record

```yaml
# Input: Decision Entity
decision:
  id: decision-001
  description: "Approved Q4 budget with 5% increase"
  deciders: [speaker-001, speaker-004]
  rationale: "Market conditions support growth investment"
  related_topic: topic-001
  source_cues: ["cue-120", "cue-121"]

# Output: Decision Record
decision_record:
  id: DEC-{auto}
  title: "Q4 Budget Approval"
  status: DOCUMENTED
  date: 2026-01-25
  context: |
    Discussion during Q4 Planning meeting about budget allocation.
    Key consideration: market conditions and growth opportunities.
  decision: |
    Approved Q4 budget with 5% increase over Q3.
  consequences:
    positive:
      - Additional resources for growth initiatives
    negative:
      - Increased financial exposure
  participants:
    - name: Meeting Host (speaker-001)
    - name: Finance Lead (speaker-004)
  source: "[Meeting transcript](../01-summary.md)"
```

---

## Workflow

```
┌─────────────────────────────────────────────────────────────────┐
│                 WORKTRACKER INTEGRATION FLOW                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│   ┌─────────────────┐                                           │
│   │ Entity          │                                           │
│   │ Extraction      │                                           │
│   │ Output          │                                           │
│   └────────┬────────┘                                           │
│            │                                                     │
│            ▼                                                     │
│   ┌─────────────────┐                                           │
│   │  Suggestion     │                                           │
│   │  Generator      │                                           │
│   └────────┬────────┘                                           │
│            │                                                     │
│            ▼                                                     │
│   ┌─────────────────────────────────────────────────────────┐  │
│   │              08-workitems/suggested-tasks.md             │  │
│   │                                                          │  │
│   │  ## Suggested Tasks (3)                                 │  │
│   │  - [ ] Send updated budget projections (HIGH)           │  │
│   │  - [ ] Schedule follow-up meeting (MEDIUM)              │  │
│   │  - [ ] Update project timeline (LOW)                    │  │
│   │                                                          │  │
│   │  ## Suggested Stories (1)                               │  │
│   │  - [ ] Automate monthly report generation               │  │
│   │                                                          │  │
│   │  ## Decisions to Record (1)                             │  │
│   │  - [ ] Q4 Budget Approval                               │  │
│   └────────────────────────────┬────────────────────────────┘  │
│                                │                                │
│                                ▼                                │
│   ┌─────────────────────────────────────────────────────────┐  │
│   │                    HUMAN REVIEW                          │  │
│   │  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐    │  │
│   │  │ Approve │  │ Reject  │  │  Edit   │  │  Defer  │    │  │
│   │  │   All   │  │   All   │  │ & Save  │  │         │    │  │
│   │  └────┬────┘  └────┬────┘  └────┬────┘  └────┬────┘    │  │
│   └───────┼────────────┼────────────┼────────────┼──────────┘  │
│           │            │            │            │              │
│           ▼            ▼            ▼            ▼              │
│   ┌─────────────┐ ┌─────────┐ ┌─────────┐ ┌─────────────┐     │
│   │ Create in   │ │ Discard │ │ Create  │ │ Keep in     │     │
│   │ WORKTRACKER │ │         │ │ Modified│ │ suggestions │     │
│   └─────────────┘ └─────────┘ └─────────┘ └─────────────┘     │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Related Items

### Hierarchy

- **Parent Feature:** [FEAT-002: Implementation](../FEAT-002-implementation.md)

### Dependencies

| Dependency Type | Item | Description |
|----------------|------|-------------|
| Depends On | EN-010 | Requires packaged artifacts |
| Depends On | DEC-003 | Suggestion-first approach |

### Related Enablers

- Jerry worktracker skill integration

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-01-26 | Claude | pending | Enabler created |

---

## System Mapping

| System | Mapping |
|--------|---------|
| **Azure DevOps** | Product Backlog Item (tagged Integration) |
| **SAFe** | Enabler Story |
| **JIRA** | Task |
