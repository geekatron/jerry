# TASK-003: Implement Deep Link Embedding

<!--
TEMPLATE: Task
VERSION: 0.1.0
SOURCE: ONTOLOGY-v1.md Section 3.4.6
CREATED: 2026-01-28 per DEC-003:AI-004
-->

---

## Frontmatter

```yaml
# === IDENTITY ===
id: "TASK-003"
work_type: TASK

# === CORE METADATA ===
title: "Implement Deep Link Embedding"
description: |
  Implement bidirectional deep linking between mindmap nodes and their
  source transcript locations. Each entity node (action, decision, question)
  must link back to its citation anchor, and the transcript must have
  backlinks to the mindmap visualization.

# === CLASSIFICATION ===
classification: ENABLER

# === LIFECYCLE STATE ===
status: BACKLOG
resolution: null

# === PRIORITY ===
priority: HIGH

# === PEOPLE ===
assignee: "Claude"
created_by: "Claude"

# === TIMESTAMPS ===
created_at: "2026-01-28T14:00:00Z"
updated_at: "2026-01-28T14:00:00Z"

# === HIERARCHY ===
parent_id: "EN-009"

# === TAGS ===
tags:
  - "deep-linking"
  - "citations"
  - "navigation"
  - "adr-003"
  - "traceability"

# === DELIVERY ITEM PROPERTIES ===
effort: 2
acceptance_criteria: |
  - All entity nodes have clickable links to source
  - Anchor format follows ADR-003 specification
  - Links resolve correctly in rendered markdown
  - Bidirectional: transcript links back to mindmap
due_date: null

# === TASK-SPECIFIC PROPERTIES ===
activity: DEVELOPMENT
original_estimate: 4
remaining_work: 4
time_spent: 0
```

---

## Content

### Description

Implement deep linking per ADR-003 (Bidirectional Deep Linking Strategy):

1. **Forward Links:** Mindmap nodes → Source transcript segments
2. **Backlinks:** Transcript entities → Mindmap visualization
3. **Anchor Format:** Consistent `#entity-type-NNN` pattern

### ADR-003 Compliance

Per ADR-003 (Bidirectional Deep Linking):

```
CITATION ANCHOR FORMAT
─────────────────────────────────────
Type        | Pattern              | Example
─────────────────────────────────────
Action Item | #action-{NNN}        | #action-001
Decision    | #decision-{NNN}      | #decision-003
Question    | #question-{NNN}      | #question-007
Topic       | #topic-{NNN}         | #topic-002
Speaker     | #speaker-{name}      | #speaker-alice
Segment     | #seg-{NNN}           | #seg-042
─────────────────────────────────────
```

### Link Format in Mermaid

```mermaid
mindmap
  root((Meeting))
    Topic 1
      [Action: Send report](#action-001)
      [Decision: Approve budget](#decision-001)
```

### Link Format in ASCII

```
    ┌─────────────────┐
    │    Topic 1      │
    └────────┬────────┘
             │
    ┌────────┴────────┐
    │ [→] Send report │
    │ See: #action-001│
    └─────────────────┘
```

### Acceptance Criteria

- [ ] **AC-1:** All action item nodes link to `#action-{NNN}` anchors
- [ ] **AC-2:** All decision nodes link to `#decision-{NNN}` anchors
- [ ] **AC-3:** All question nodes link to `#question-{NNN}` anchors
- [ ] **AC-4:** Topic nodes link to `#topic-{NNN}` anchors
- [ ] **AC-5:** Links resolve when mindmap rendered with source transcript
- [ ] **AC-6:** Backlink section added to transcript entities pointing to mindmap
- [ ] **AC-7:** Link IDs match between extraction report and mindmap output
- [ ] **AC-8:** Invalid/missing anchors logged as warnings (not errors)
- [ ] **AC-9:** ASCII version includes anchor references in text form
- [ ] **AC-10:** Link format validated against ADR-003 specification

### Implementation Notes

**Integration Points:**
- ts-extractor provides entity IDs in extraction report
- ts-formatter creates anchor points in transcript files
- ts-mindmap generators consume IDs and create links

**Validation Logic:**
1. Parse extraction report for all entity IDs
2. Generate link for each entity in mindmap
3. Verify anchor exists in source (warning if missing)
4. Add backlink comment in transcript file

**Backlink Format (in transcript):**
```markdown
<!-- BACKLINKS -->
<!-- Visualized in: 07-mindmap/mindmap.mmd#action-001 -->
```

### Related Items

- **Parent:** [EN-009](./EN-009-mindmap-generator.md)
- **Blocked By:** [TASK-001](./TASK-001-mermaid-generator.md) (needs base Mermaid output first)
- **Blocks:** [TASK-004](./TASK-004-unit-tests.md)
- **Reference:** [ADR-003](../../FEAT-001-analysis-design/EN-004-architecture-decisions/docs/adrs/adr-003.md) (Bidirectional Linking)

---

## Time Tracking

| Metric            | Value |
|-------------------|-------|
| Original Estimate | 4 hours |
| Remaining Work    | 4 hours |
| Time Spent        | 0 hours |

---

## Evidence

### Deliverables

| Deliverable | Type | Link |
|-------------|------|------|
| Deep link logic | Agent update | skills/transcript/agents/ts-mindmap-*.md |
| Link validation tests | Test | skills/transcript/test_data/validation/mindmap-link-tests.yaml |

### Verification

- [ ] Acceptance criteria verified
- [ ] All links resolve correctly
- [ ] Backlinks present in transcript files
- [ ] ADR-003 compliance verified
- [ ] Reviewed by: {REVIEWER}

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-01-28 | Created | Per DEC-003:AI-004 - enabler-scoped numbering |
