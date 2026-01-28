# TASK-002: Create ASCII Generator Agent

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
id: "TASK-002"
work_type: TASK

# === CORE METADATA ===
title: "Create ASCII Generator Agent"
description: |
  Implement the ASCII art mindmap generator as a fallback visualization
  for environments that don't support Mermaid rendering. Uses box-drawing
  characters to create hierarchical tree structures readable in any
  terminal or plain text viewer.

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
  - "ascii"
  - "visualization"
  - "mindmap"
  - "fallback"
  - "accessibility"

# === DELIVERY ITEM PROPERTIES ===
effort: 2
acceptance_criteria: |
  - Generates readable ASCII tree structure
  - Works within 80-character width constraint
  - Uses Unicode box-drawing characters
  - Legend explains entity symbols
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

Create the ASCII mindmap generator agent (`ts-mindmap-ascii`) that:

1. **Consumes** ts-formatter output (8-file packet from EN-016)
2. **Transforms** extracted entities into ASCII tree structure
3. **Outputs** plain text diagram readable in any environment

### Input Requirements

Same as TASK-001 (Mermaid generator):
- Extraction report JSON from ts-extractor
- Topic segmentation from ts-extractor
- 8-file packet structure from ts-formatter

### Output Specification

**File:** `07-mindmap/mindmap.ascii.txt`

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
    │ [→] Action  │     │ Deliverables│
    └─────────────┘     │ [?] Question│
                        └─────────────┘

Legend:
  [→] Action Item    [?] Question    [!] Decision    [*] Speaker
```

### Acceptance Criteria

- [ ] **AC-1:** Generates valid ASCII tree using box-drawing characters (┌ ─ ┐ │ └ ┴ ┬ ├ ┤)
- [ ] **AC-2:** Root node is centered and double-boxed
- [ ] **AC-3:** Child nodes connect with proper branching lines
- [ ] **AC-4:** All content fits within 80-character width
- [ ] **AC-5:** Entity symbols in legend ([→] action, [?] question, [!] decision)
- [ ] **AC-6:** Handles overflow by truncating with ellipsis (...)
- [ ] **AC-7:** Speaker names shown with [*] prefix
- [ ] **AC-8:** Works with up to 50 topics (degrades gracefully beyond)
- [ ] **AC-9:** File is valid UTF-8 encoding
- [ ] **AC-10:** Readable in monospace font terminal

### Implementation Notes

**Agent Definition Location:** `skills/transcript/agents/ts-mindmap-ascii.md`

**Key Design Decisions:**
- Per ADR-005: Prompt-based implementation (no Python code)
- Uses Unicode box-drawing (U+2500 block) for portability
- 80-char width ensures terminal compatibility
- Legend at bottom explains symbols

**Box-Drawing Characters:**
```
┌ U+250C  ─ U+2500  ┐ U+2510
│ U+2502  ┼ U+253C  │ U+2502
├ U+251C  ┬ U+252C  ┤ U+2524
└ U+2514  ┴ U+2534  ┘ U+2518
▼ U+25BC (downward arrow for branches)
```

### Related Items

- **Parent:** [EN-009](./EN-009-mindmap-generator.md)
- **Blocked By:** [EN-016](../EN-016-ts-formatter/EN-016-ts-formatter.md) (ts-formatter must complete first)
- **Blocks:** [TASK-004](./TASK-004-unit-tests.md)
- **Related:** [TASK-001](./TASK-001-mermaid-generator.md) (Mermaid version)

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
| Agent definition | Markdown | skills/transcript/agents/ts-mindmap-ascii.md |
| Sample output | Text | skills/transcript/test_data/outputs/sample-mindmap.ascii.txt |

### Verification

- [ ] Acceptance criteria verified
- [ ] ASCII renders correctly in terminal
- [ ] Width constraint validated (80 chars)
- [ ] Reviewed by: {REVIEWER}

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-01-28 | Created | Per DEC-003:AI-004 - enabler-scoped numbering |
