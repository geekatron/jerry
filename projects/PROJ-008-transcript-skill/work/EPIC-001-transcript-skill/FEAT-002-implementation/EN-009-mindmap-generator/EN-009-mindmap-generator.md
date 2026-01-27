# EN-009: Mind Map Generator

<!--
TEMPLATE: Enabler
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.5
-->

> **Type:** enabler
> **Status:** pending
> **Priority:** high
> **Impact:** high
> **Created:** 2026-01-26T00:00:00Z
> **Due:** TBD
> **Completed:**
> **Parent:** FEAT-002
> **Owner:** Claude
> **Target Sprint:** Sprint 4
> **Effort Points:** 8
> **Gate:** GATE-5 (Core Implementation Review)

---

## Summary

Implement the mind map generator that transforms extracted entities into visual mind maps. The generator outputs Mermaid diagram format (primary) and ASCII art (fallback), with deep links back to source transcript locations.

**Technical Justification:**
- Visual representation aids comprehension
- Mermaid integrates with markdown renderers
- ASCII fallback ensures universal accessibility
- Deep links enable source verification

---

## Benefit Hypothesis

**We believe that** generating mind maps from extracted entities

**Will result in** improved comprehension and navigation of meeting content

**We will know we have succeeded when:**
- Mind maps accurately represent topic hierarchy
- All entities are linked to their sources
- Mermaid renders correctly in standard viewers
- ASCII version is readable in terminal
- Human approval received at GATE-6

---

## Acceptance Criteria

### Definition of Done

- [ ] Mermaid diagram generator implemented
- [ ] ASCII art generator implemented
- [ ] Topic hierarchy visualization working
- [ ] Entity relationships shown
- [ ] Deep links to source cues embedded
- [ ] Large transcript handling (chunking)
- [ ] Unit tests passing
- [ ] ps-critic review passed
- [ ] Human approval at GATE-6

### Technical Criteria

| # | Criterion | Verified |
|---|-----------|----------|
| AC-1 | Generates valid Mermaid mindmap syntax | [ ] |
| AC-2 | Topics form hierarchical structure | [ ] |
| AC-3 | Speakers connected to their topics | [ ] |
| AC-4 | Action items linked to topics | [ ] |
| AC-5 | Questions and decisions shown | [ ] |
| AC-6 | Deep links to source cues in nodes | [ ] |
| AC-7 | ASCII version readable at 80 chars | [ ] |
| AC-8 | Handles 50+ topics gracefully | [ ] |

---

## Children (Tasks)

### Task Inventory

| ID | Title | Status | Owner | Effort | Blocked By |
|----|-------|--------|-------|--------|------------|
| TASK-046 | Create Mermaid Generator Agent | pending | Claude | 3 | EN-008 |
| TASK-047 | Create ASCII Generator Agent | pending | Claude | 2 | EN-008 |
| TASK-048 | Implement Deep Link Embedding | pending | Claude | 2 | TASK-046 |
| TASK-049 | Create Unit Tests | pending | Claude | 1 | TASK-046..048 |

---

## Output Formats

### Mermaid Mindmap Format

```mermaid
mindmap
  root((Meeting: Q4 Planning))
    Budget Review
      Current Status
        ::icon(fa fa-check)
        [Source: 00:05:00](#cue-010)
      Projections
        [Action: Send updates](#action-001)
    Timeline Discussion
      Q4 Deliverables
        [Question: What's timeline?](#question-001)
      Milestones
        November Launch
        December Review
    Decisions Made
      [DEC-001: Approve budget](#decision-001)
```

### ASCII Art Format

```
                    ┌─────────────────────────┐
                    │   Meeting: Q4 Planning   │
                    └───────────┬─────────────┘
           ┌────────────────────┼────────────────────┐
           │                    │                    │
    ┌──────▼──────┐     ┌──────▼──────┐     ┌──────▼──────┐
    │Budget Review│     │  Timeline   │     │  Decisions  │
    └──────┬──────┘     │ Discussion  │     │    Made     │
           │            └──────┬──────┘     └─────────────┘
    ┌──────┴──────┐            │
    │   Current   │     ┌──────┴──────┐
    │   Status    │     │     Q4      │
    └─────────────┘     │ Deliverables│
                        └─────────────┘

Legend:
  [→] Action Item    [?] Question    [!] Decision
```

---

## Layout Algorithm

### Topic Hierarchy Processing

1. **Root Node**: Meeting title/date
2. **Level 1**: Main topics (by time or importance)
3. **Level 2**: Subtopics and related entities
4. **Level 3**: Action items, questions, decisions

### Node Sizing Rules

- Root: Largest (double brackets)
- Topics: Standard (single brackets)
- Entities: Small (single line)
- Links: Embedded as clickable text

### Overflow Handling

For large transcripts (>50 topics):
1. Show top-level topics only in main map
2. Generate separate detail maps per topic
3. Link detail maps from main map

---

## Related Items

### Hierarchy

- **Parent Feature:** [FEAT-002: Implementation](../FEAT-002-implementation.md)

### Dependencies

| Dependency Type | Item | Description |
|----------------|------|-------------|
| Depends On | EN-016 | Requires ts-formatter output (8-file packet) |
| Depends On | ADR-003 | Deep linking strategy |
| Blocked By | EN-016 | ts-formatter must complete before mind map generation |
| Used By | EN-015 | Validation tests include mind map verification |

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-01-26 | Claude | pending | Enabler created |
| 2026-01-26 | Claude | pending | BUG-001: EN-009 ID retained for Mind Map (ts-formatter renumbered to EN-016). Gate corrected to GATE-5. Dependencies updated. |

---

## System Mapping

| System | Mapping |
|--------|---------|
| **Azure DevOps** | Product Backlog Item (tagged Technical) |
| **SAFe** | Enabler Story |
| **JIRA** | Task |
