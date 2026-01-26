# EN-012: Skill CLI Interface

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

Implement the transcript skill CLI interface that enables users to invoke the skill via natural language or slash commands. The interface handles input validation, orchestrates the processing pipeline, and provides progress feedback.

**Technical Justification:**
- User-facing entry point to the skill
- Follows Jerry skill conventions
- Provides progress feedback for long operations
- Handles errors gracefully with actionable messages

---

## Benefit Hypothesis

**We believe that** implementing a clean CLI interface

**Will result in** intuitive skill invocation with clear feedback

**We will know we have succeeded when:**
- Users can invoke skill via `/transcript`
- Progress is visible during processing
- Errors provide actionable guidance
- Output location is clearly communicated
- Human approval received at GATE-6

---

## Acceptance Criteria

### Definition of Done

- [ ] Skill definition (SKILL.md) created
- [ ] CLI command handler implemented
- [ ] Input validation working
- [ ] Progress reporting implemented
- [ ] Error handling with user guidance
- [ ] Integration tests passing
- [ ] ps-critic review passed
- [ ] Human approval at GATE-6

### Technical Criteria

| # | Criterion | Verified |
|---|-----------|----------|
| AC-1 | `/transcript process <file>` command works | [ ] |
| AC-2 | Validates VTT file exists and is valid | [ ] |
| AC-3 | Shows progress percentage during processing | [ ] |
| AC-4 | Reports output packet location on completion | [ ] |
| AC-5 | Handles errors with actionable messages | [ ] |
| AC-6 | Supports `--output-dir` option | [ ] |
| AC-7 | Supports `--verbose` for detailed output | [ ] |
| AC-8 | Follows Jerry skill conventions | [ ] |

---

## Children (Tasks)

### Task Inventory

| ID | Title | Status | Owner | Effort | Blocked By |
|----|-------|--------|-------|--------|------------|
| TASK-059 | Create SKILL.md Definition | pending | Claude | 1 | EN-010 |
| TASK-060 | Implement Command Handler | pending | Claude | 2 | TASK-059 |
| TASK-061 | Implement Progress Reporting | pending | Claude | 1 | TASK-060 |
| TASK-062 | Implement Error Handling | pending | Claude | 1 | TASK-060 |

---

## CLI Interface Specification

### Commands

```bash
# Primary command: Process a VTT file
/transcript process <file.vtt> [options]

# Options:
#   --output-dir <path>    Output directory (default: ./{session-id}-transcript-output/)
#   --verbose              Show detailed progress
#   --entities <list>      Comma-separated entity types to extract (default: all)
#   --no-mindmap           Skip mind map generation
#   --no-workitems         Skip worktracker suggestions

# Alternative invocations:
"Process this transcript: path/to/meeting.vtt"
"Analyze the meeting transcript meeting.vtt"
```

### Progress Output

```
╭─────────────────────────────────────────────────────────────────╮
│                    Transcript Processing                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Input: meeting-2026-01-25.vtt                                  │
│  Status: Processing...                                           │
│                                                                  │
│  [████████████░░░░░░░░░░░░░░░░░░] 40%                           │
│                                                                  │
│  ✓ VTT Parsing              Complete                            │
│  ✓ Speaker Identification   Complete                            │
│  ◐ Entity Extraction        In Progress (Topics)                │
│  ○ Mind Map Generation      Pending                             │
│  ○ Artifact Packaging       Pending                             │
│  ○ Worktracker Integration  Pending                             │
│                                                                  │
╰─────────────────────────────────────────────────────────────────╯
```

### Completion Output

```
╭─────────────────────────────────────────────────────────────────╮
│                 Transcript Processing Complete                   │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ✓ All stages completed successfully                            │
│                                                                  │
│  Summary:                                                        │
│  - Speakers identified: 4                                        │
│  - Topics extracted: 12                                          │
│  - Action items: 7                                               │
│  - Questions: 15                                                 │
│  - Ideas: 3                                                      │
│  - Decisions: 2                                                  │
│                                                                  │
│  Output: ./meeting-2026-01-25-transcript-output/                │
│  Index:  ./meeting-2026-01-25-transcript-output/00-index.md     │
│                                                                  │
│  Next steps:                                                     │
│  - Review suggested work items: 08-workitems/suggested-tasks.md │
│  - Explore mind map: 07-mindmap/mindmap.mmd                     │
│                                                                  │
╰─────────────────────────────────────────────────────────────────╯
```

### Error Output

```
╭─────────────────────────────────────────────────────────────────╮
│                         Error                                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ✗ Failed to parse VTT file                                     │
│                                                                  │
│  Error: Invalid timestamp format at line 42                      │
│         Expected: HH:MM:SS.mmm --> HH:MM:SS.mmm                 │
│         Found:    00:15:30 -> 00:15:35                           │
│                                                                  │
│  Suggestions:                                                    │
│  1. Verify the file is valid WebVTT format                      │
│  2. Check for missing or malformed headers                      │
│  3. Use a VTT validator tool to identify issues                 │
│                                                                  │
│  For more details, run with --verbose                           │
│                                                                  │
╰─────────────────────────────────────────────────────────────────╯
```

---

## SKILL.md Structure

```markdown
# Transcript Skill

> Process meeting transcripts to extract structured entities and generate mind maps.

## Invocation

- `/transcript process <file.vtt>`
- "Process this transcript: <file>"
- "Analyze the meeting transcript <file>"

## Capabilities

1. **VTT Parsing** - Parse WebVTT transcript files
2. **Entity Extraction** - Extract speakers, topics, questions, action items, ideas, decisions
3. **Mind Map Generation** - Create visual mind maps linking concepts
4. **Artifact Packaging** - Bundle outputs into navigable transcript packets
5. **Worktracker Integration** - Suggest work items from meeting content

## Options

| Option | Description | Default |
|--------|-------------|---------|
| `--output-dir` | Output directory | `./{session-id}-transcript-output/` |
| `--verbose` | Detailed progress | false |
| `--entities` | Entity types to extract | all |
| `--no-mindmap` | Skip mind map | false |
| `--no-workitems` | Skip work items | false |

## Examples

Process a VTT file with default settings:
```
/transcript process meeting.vtt
```

Process with custom output directory:
```
/transcript process meeting.vtt --output-dir ./transcripts/q4-planning/
```

Extract only action items and decisions:
```
/transcript process meeting.vtt --entities action_items,decisions
```
```

---

## Related Items

### Hierarchy

- **Parent Feature:** [FEAT-002: Implementation](../FEAT-002-implementation.md)

### Dependencies

| Dependency Type | Item | Description |
|----------------|------|-------------|
| Depends On | EN-007 | VTT parser must be complete |
| Depends On | EN-008 | Entity extraction must be complete |
| Depends On | EN-010 | Artifact packaging must be complete |

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-01-26 | Claude | pending | Enabler created |

---

## System Mapping

| System | Mapping |
|--------|---------|
| **Azure DevOps** | Product Backlog Item (tagged UI) |
| **SAFe** | Enabler Story |
| **JIRA** | Task |
