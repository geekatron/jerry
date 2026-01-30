# TASK-250: Update ts-parser.md to v2.0 Strategy Pattern

<!--
TEMPLATE: Task
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.6
ENABLER: EN-025 (ts-parser v2.0 + CLI + SKILL.md Integration)
TDD REFERENCE: TDD-FEAT-004 Section 3 (lines 266-458)
-->

---

## Frontmatter

```yaml
id: "TASK-250"
work_type: TASK
title: "Update ts-parser.md to v2.0 Strategy Pattern"
description: |
  Transform ts-parser.md agent definition from v1.2.0 (LLM-only parser)
  to v2.0.0 (Strategy Pattern orchestrator with four roles):
  ORCHESTRATOR, DELEGATOR, FALLBACK, VALIDATOR.

classification: ENABLER
status: DONE
resolution: COMPLETE
priority: CRITICAL
assignee: "Claude"
created_by: "Claude"
created_at: "2026-01-29T18:50:00Z"
updated_at: "2026-01-29T18:50:00Z"

parent_id: "EN-025"

tags:
  - "ts-parser"
  - "strategy-pattern"
  - "agent-transformation"
  - "TDD-Section-3"

effort: 3
acceptance_criteria: |
  - ts-parser.md version updated to 2.0.0
  - Four roles documented: ORCHESTRATOR, DELEGATOR, FALLBACK, VALIDATOR
  - Format detection logic (VTT header, timestamps)
  - Python parser delegation path
  - LLM fallback path for non-VTT formats
  - Output validation before chunking

due_date: null

activity: DEVELOPMENT
original_estimate: 4
remaining_work: 4
time_spent: 0
```

---

## State Machine

**Current State:** `BACKLOG`

---

## Content

### Description

Transform the ts-parser.md agent definition from a simple LLM parser (v1.2.0) to a Strategy Pattern orchestrator (v2.0.0) that can route between Python deterministic parsing and LLM fallback based on input format.

**TDD Reference:** TDD-FEAT-004 Section 3 (lines 266-458)

**Target Specification:**
```yaml
Target Role: ORCHESTRATOR + DELEGATOR + FALLBACK + VALIDATOR
Processing Model: Strategy Pattern with Python delegation
Output: canonical-transcript.json + index.json + chunks/*.json
```

### Acceptance Criteria

- [x] ts-parser.md version header updated to 2.0.0
- [x] ORCHESTRATOR role: Coordinate pipeline based on format and results
- [x] DELEGATOR role: Route to Python parser via Bash tool for VTT files
- [x] FALLBACK role: Maintain LLM parsing for non-VTT and error recovery
- [x] VALIDATOR role: Validate Python parser output schema before chunking
- [x] Format detection documented (WEBVTT header, timestamp patterns)
- [x] Error handling for Python parser failures → fallback to LLM
- [x] Output specification: index.json + chunks/chunk-NNN.json

### Implementation Notes

**Four Roles per TDD Section 3:**

1. **ORCHESTRATOR**
   - Coordinate pipeline based on detected format
   - Decide which path (Python/LLM) based on format
   - Track execution flow for reporting

2. **DELEGATOR**
   - For VTT: Invoke Python parser via Bash tool
   - Command: `python -m src.parser.vtt_parser <file>`
   - Pass output to chunker

3. **FALLBACK**
   - For non-VTT formats (SRT, TXT): Use LLM parsing (same as v1.2.0)
   - For Python parser errors: Fall back to LLM parsing
   - Ensure no data loss path exists

4. **VALIDATOR**
   - Verify Python parser output matches canonical schema
   - Check required fields: segments, metadata
   - Reject malformed output → trigger fallback

**Format Detection Heuristics:**
```
VTT Detection:
- File starts with "WEBVTT" header
- Contains timestamps in format: HH:MM:SS.mmm --> HH:MM:SS.mmm
- Contains voice spans: <v Speaker>text</v>

SRT Detection:
- Contains numeric cue identifiers (1, 2, 3...)
- Timestamps in format: HH:MM:SS,mmm --> HH:MM:SS,mmm

Plain Text:
- No timestamp patterns detected
- Fallback for unrecognized formats
```

### Related Items

- Parent: [EN-025: ts-parser v2.0 + CLI + SKILL.md Integration](./EN-025-skill-integration.md)
- References: [TDD-FEAT-004 Section 3](../docs/design/TDD-FEAT-004-hybrid-infrastructure.md)
- Depends On: [EN-020: Python VTT Parser](../EN-020-python-parser/EN-020-python-parser.md)
- Target File: [skills/transcript/agents/ts-parser.md](../../../../../skills/transcript/agents/ts-parser.md)

---

## Time Tracking

| Metric            | Value           |
|-------------------|-----------------|
| Original Estimate | 4 hours |
| Remaining Work    | 0 hours    |
| Time Spent        | 1 hour        |

---

## Evidence

### Deliverables

| Deliverable | Type | Link |
|-------------|------|------|
| ts-parser.md v2.0 | Agent Definition | skills/transcript/agents/ts-parser.md |

### Verification

- [ ] Version header shows 2.0.0
- [ ] Four roles documented in agent definition
- [ ] Format detection logic present
- [ ] Python invocation command documented
- [ ] Fallback path documented
- [ ] Validator schema check documented

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-01-29 | Created | Initial task creation per EN-025 |
