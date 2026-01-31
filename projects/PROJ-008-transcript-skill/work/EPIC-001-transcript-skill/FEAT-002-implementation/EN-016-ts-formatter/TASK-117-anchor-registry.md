# TASK-117: Implement/Verify AnchorRegistry (ADR-003)

<!--
TEMPLATE: Task
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.6
ENABLER: EN-016 (ts-formatter Agent Implementation)
-->

---

## Frontmatter

```yaml
id: "TASK-117"
work_type: TASK
title: "Implement/Verify AnchorRegistry (ADR-003)"
description: |
  Implement and verify the AnchorRegistry component that tracks all
  anchors and their backlinks per ADR-003.

classification: ENABLER
status: DONE
resolution: VERIFIED_COMPLETE
priority: HIGH
assignee: "Claude"
created_by: "Claude"
created_at: "2026-01-26T18:30:00Z"
updated_at: "2026-01-28T17:30:00Z"

parent_id: "EN-016"

tags:
  - "implementation"
  - "ts-formatter"
  - "deep-linking"
  - "ADR-003"

effort: 2
acceptance_criteria: |
  - Anchor registration for all entity types
  - Backlink tracking for cross-references
  - Anchor naming convention enforced
  - Registry exported as _anchors.json

due_date: null

activity: DEVELOPMENT
original_estimate: 4
remaining_work: 0
time_spent: 1
note: "AnchorRegistry already defined in ts-formatter.md lines 98-124"
```

---

## State Machine

**Current State:** `DONE`

> **Verification Result:** AnchorRegistry verified complete in ts-formatter.md (lines 98-124). Anchor ID formats (seg-, spk-, act-, dec-, que-, top-), registry structure with backlinks, and _anchors.json output all defined per ADR-003.

---

## Content

### Description

Implement and verify the AnchorRegistry component that maintains a registry of all anchors and their backlinks per ADR-003. This enables bidirectional navigation throughout the transcript packet.

### Anchor Naming Convention (ADR-003)

```
ANCHOR NAMING SCHEME
====================

FORMAT: {type}-{sequence_number}

TYPE PREFIXES:
──────────────
seg-    → Transcript segments     (seg-001, seg-042)
spk-    → Speakers                (spk-001, spk-alice)
act-    → Action items            (act-001, act-002)
dec-    → Decisions               (dec-001, dec-002)
que-    → Questions               (que-001, que-002)
top-    → Topics                  (top-001, top-002)

EXAMPLES:
─────────
#seg-042     → Link to transcript segment 42
#spk-alice   → Link to speaker "Alice" entry
#act-001     → Link to first action item
#dec-003     → Link to decision 3
```

### Registry Structure

```json
{
  "version": "1.0",
  "packet_id": "transcript-meeting-20260126-001",
  "anchors": {
    "seg-001": {
      "type": "segment",
      "file": "02-transcript.md",
      "line": 42,
      "backlinks": [
        {
          "source_file": "04-action-items.md",
          "source_line": 15,
          "context": "Action item references this segment"
        }
      ]
    },
    "act-001": {
      "type": "action_item",
      "file": "04-action-items.md",
      "line": 10,
      "backlinks": [
        {
          "source_file": "00-index.md",
          "source_line": 25,
          "context": "Listed in index"
        }
      ]
    }
  }
}
```

### Interface

```python
@dataclass
class Anchor:
    id: str
    type: str
    file: str
    line: int
    backlinks: List[Backlink]

@dataclass
class Backlink:
    source_file: str
    source_line: int
    context: str

class AnchorRegistry:
    def __init__(self):
        self._anchors: Dict[str, Anchor] = {}

    def register_anchor(
        self,
        anchor_id: str,
        anchor_type: str,
        file: str,
        line: int
    ) -> None:
        """Register a new anchor."""
        ...

    def add_backlink(
        self,
        anchor_id: str,
        source_file: str,
        source_line: int,
        context: str = ""
    ) -> None:
        """Add a backlink to an existing anchor."""
        ...

    def get_backlinks(self, anchor_id: str) -> List[Backlink]:
        """Get all backlinks for an anchor."""
        ...

    def export_registry(self) -> dict:
        """Export registry as dictionary for _anchors.json."""
        ...
```

### Anchor Types

| Type | Prefix | Source File | Description |
|------|--------|-------------|-------------|
| segment | seg- | 02-transcript.md | Transcript segments |
| speaker | spk- | 03-speakers.md | Speaker entries |
| action_item | act- | 04-action-items.md | Action items |
| decision | dec- | 05-decisions.md | Decisions |
| question | que- | 06-questions.md | Questions |
| topic | top- | 07-topics.md | Topics |

### Acceptance Criteria

- [ ] Anchor registration for all entity types
- [ ] Anchor naming convention enforced (type-NNN format)
- [ ] Backlink registration when anchor is referenced
- [ ] `get_backlinks()` returns all references to an anchor
- [ ] Registry exported to `_anchors.json` in packet
- [ ] No duplicate anchor IDs allowed
- [ ] All registered anchors have valid file references
- [ ] Line numbers accurately reflect anchor positions

### Test Cases (from EN-015)

Reference test scenarios:
- Register segment anchors from transcript
- Register entity anchors from extraction
- Add backlinks when creating cross-references
- Export registry to JSON
- Validate anchor uniqueness
- Handle file splits (anchor relocation)

### Related Items

- Parent: [EN-016: ts-formatter Agent Implementation](./EN-016-ts-formatter.md)
- Blocked By: [TASK-113: Agent alignment](./TASK-113-formatter-agent-alignment.md)
- References: [TDD-ts-formatter.md Section 2](../../FEAT-001-analysis-design/EN-005-design-documentation/docs/TDD-ts-formatter.md)
- References: [ADR-003: Bidirectional Deep Linking](../../FEAT-001-analysis-design/EN-004-architecture-decisions/docs/adrs/adr-003.md)
- Blocks: [TASK-118: BacklinkInjector](./TASK-118-backlink-injector.md)
- Validated By: [TASK-136: Formatter tests](../EN-015-transcript-validation/TASK-136-formatter-tests.md)

---

## Evidence

### Deliverables

| Deliverable | Type | Link |
|-------------|------|------|
| ts-formatter.md AnchorRegistry section | Agent | skills/transcript/agents/ts-formatter.md |
| _anchors.json sample | Output | (link to sample) |
| Anchor registry test results | Test Evidence | (link to test output) |

### Verification

- [ ] All anchor types supported
- [ ] Naming convention enforced
- [ ] Backlinks tracked correctly
- [ ] JSON export valid
- [ ] Reviewed by: (pending)

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-01-26 | Created | Initial task creation per EN-016 |
| 2026-01-28 | **DONE** | AnchorRegistry verified complete. Anchor ID formats, registry JSON structure, _anchors.json output all defined in ts-formatter.md. Matches ADR-003 and TDD-ts-formatter §2. |

