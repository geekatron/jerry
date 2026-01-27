# TASK-118: Implement/Verify BacklinkInjector (IR-004)

<!--
TEMPLATE: Task
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.6
ENABLER: EN-016 (ts-formatter Agent Implementation)
-->

---

## Frontmatter

```yaml
id: "TASK-118"
work_type: TASK
title: "Implement/Verify BacklinkInjector (IR-004)"
description: |
  Implement and verify the BacklinkInjector component that populates
  backlinks sections in all output files per IR-004.

classification: ENABLER
status: BACKLOG
resolution: null
priority: HIGH
assignee: "Claude"
created_by: "Claude"
created_at: "2026-01-26T18:30:00Z"
updated_at: "2026-01-26T18:30:00Z"

parent_id: "EN-016"

tags:
  - "implementation"
  - "ts-formatter"
  - "backlinks"
  - "IR-004"

effort: 1
acceptance_criteria: |
  - Backlinks section injected at end of each file
  - Section shows all references to anchors in that file
  - Links formatted with context
  - Section hidden/collapsed by default (optional)

due_date: null

activity: DEVELOPMENT
original_estimate: 2
remaining_work: 2
time_spent: 0
```

---

## State Machine

**Current State:** `BACKLOG`

---

## Content

### Description

Implement and verify the BacklinkInjector component that populates the "Referenced By" (backlinks) sections in all output files. This completes the bidirectional linking per IR-004.

### Backlinks Section Format

```markdown
---

## Referenced By

This section lists all documents that reference content in this file.

| From | Anchor | Context |
|------|--------|---------|
| [04-action-items.md](04-action-items.md#act-001) | #seg-042 | Action item cites this segment |
| [05-decisions.md](05-decisions.md#dec-001) | #seg-087 | Decision cites this segment |
| [00-index.md](00-index.md) | #seg-001 | Listed in index navigation |

---
```

### Alternative Format (Collapsible)

```markdown
---

<details>
<summary>Referenced By (3 references)</summary>

| From | Anchor | Context |
|------|--------|---------|
| [04-action-items.md](04-action-items.md#act-001) | #seg-042 | Action item cites this segment |
| [05-decisions.md](05-decisions.md#dec-001) | #seg-087 | Decision cites this segment |
| [00-index.md](00-index.md) | #seg-001 | Listed in index navigation |

</details>

---
```

### Interface

```python
class BacklinkInjector:
    def __init__(self, registry: AnchorRegistry):
        self._registry = registry

    def inject_backlinks(
        self,
        files: Dict[str, str],
        registry: AnchorRegistry
    ) -> Dict[str, str]:
        """Inject backlinks sections into all files."""
        for filename, content in files.items():
            backlinks = self._get_backlinks_for_file(filename, registry)
            if backlinks:
                section = self._format_backlink_section(backlinks)
                files[filename] = content + section
        return files

    def _get_backlinks_for_file(
        self,
        filename: str,
        registry: AnchorRegistry
    ) -> List[BacklinkEntry]:
        """Get all backlinks targeting anchors in this file."""
        ...

    def _format_backlink_section(
        self,
        backlinks: List[BacklinkEntry]
    ) -> str:
        """Format backlinks as markdown section."""
        ...
```

### Backlinks Processing Flow

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                       BACKLINK INJECTION FLOW                                │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  1. COLLECT                                                                  │
│     ┌────────────────────────────────────────────────────────────────┐      │
│     │ For each file in packet:                                        │      │
│     │   For each anchor in that file:                                 │      │
│     │     Collect all backlinks from AnchorRegistry                   │      │
│     └────────────────────────────────────────────────────────────────┘      │
│                              │                                               │
│                              ▼                                               │
│  2. GROUP                                                                    │
│     ┌────────────────────────────────────────────────────────────────┐      │
│     │ Group backlinks by target file:                                 │      │
│     │   02-transcript.md: [backlinks targeting this file]             │      │
│     │   04-action-items.md: [backlinks targeting this file]           │      │
│     └────────────────────────────────────────────────────────────────┘      │
│                              │                                               │
│                              ▼                                               │
│  3. FORMAT                                                                   │
│     ┌────────────────────────────────────────────────────────────────┐      │
│     │ For each file with backlinks:                                   │      │
│     │   Create "Referenced By" section                                │      │
│     │   Format as markdown table                                      │      │
│     └────────────────────────────────────────────────────────────────┘      │
│                              │                                               │
│                              ▼                                               │
│  4. INJECT                                                                   │
│     ┌────────────────────────────────────────────────────────────────┐      │
│     │ Append backlinks section to end of each file                    │      │
│     │ (before final --- separator)                                    │      │
│     └────────────────────────────────────────────────────────────────┘      │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Acceptance Criteria

- [ ] Backlinks section appended to each file with references
- [ ] Section titled "Referenced By"
- [ ] Table format with From, Anchor, Context columns
- [ ] Links are valid markdown relative paths
- [ ] Context field populated from AnchorRegistry
- [ ] Files with no backlinks have no section (or empty note)
- [ ] Section placement at end of file, before closing separator
- [ ] Collapsible format (optional, configurable)

### Test Cases (from EN-015)

Reference test scenarios:
- File with multiple backlinks → table populated
- File with no backlinks → no section or empty note
- Backlinks from multiple source files
- Backlinks to multiple anchors in same file
- Context text formatting

### Related Items

- Parent: [EN-016: ts-formatter Agent Implementation](./EN-016-ts-formatter.md)
- Blocked By: [TASK-117: AnchorRegistry](./TASK-117-anchor-registry.md)
- References: [TDD-ts-formatter.md Section 5](../../FEAT-001-analysis-design/EN-005-design-documentation/docs/TDD-ts-formatter.md)
- References: [ADR-003: Bidirectional Deep Linking](../../FEAT-001-analysis-design/EN-004-architecture-decisions/docs/adrs/adr-003.md)
- Validated By: [TASK-136: Formatter tests](../EN-015-transcript-validation/TASK-136-formatter-tests.md)

---

## Evidence

### Deliverables

| Deliverable | Type | Link |
|-------------|------|------|
| ts-formatter.md BacklinkInjector section | Agent | skills/transcript/agents/ts-formatter.md |
| Sample backlinks section | Output | (link to sample) |
| Backlink injection test results | Test Evidence | (link to test output) |

### Verification

- [ ] Backlinks sections generated correctly
- [ ] Table format valid
- [ ] Links resolve correctly
- [ ] Context populated
- [ ] Reviewed by: (pending)

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-01-26 | Created | Initial task creation per EN-016 |

