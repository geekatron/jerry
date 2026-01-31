# TASK-252: Update SKILL.md Orchestration to Use Hybrid Pipeline

<!--
TEMPLATE: Task
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.6
ENABLER: EN-025 (ts-parser v2.0 + CLI + SKILL.md Integration)
TDD REFERENCE: TDD-FEAT-004 Section 10 (lines 1773-1805)
-->

---

## Frontmatter

```yaml
id: "TASK-252"
work_type: TASK
title: "Update SKILL.md Orchestration to Use Hybrid Pipeline"
description: |
  Update SKILL.md to route VTT files through the hybrid pipeline:
  Python Parser → Chunker → ts-extractor (on chunks) → ts-formatter → ps-critic

classification: ENABLER
status: DONE
resolution: COMPLETE
priority: CRITICAL
assignee: "Claude"
created_by: "Claude"
created_at: "2026-01-29T19:00:00Z"
updated_at: "2026-01-29T19:00:00Z"

parent_id: "EN-025"

tags:
  - "skill-md"
  - "orchestration"
  - "hybrid-pipeline"
  - "TDD-Section-10"

effort: 2
acceptance_criteria: |
  - SKILL.md pipeline diagram shows hybrid architecture
  - ts-parser role updated to ORCHESTRATOR + DELEGATOR + FALLBACK + VALIDATOR
  - VTT detection triggers Python parser path
  - Output structure: index.json + chunks/*.json
  - Backward compatibility: non-VTT formats use LLM fallback

due_date: null

activity: DOCUMENTATION
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

Update the SKILL.md orchestration documentation to reflect the hybrid pipeline architecture. Currently SKILL.md shows the OLD pipeline:

```
CURRENT (SKILL.md lines 196-222):
ts-parser (haiku LLM) → ts-extractor → ts-formatter → ps-critic
```

This must be updated to show the NEW hybrid pipeline:

```
TARGET:
ts-parser v2.0 (ORCHESTRATOR)
  → IF VTT: Python Parser → Chunker
  → ELSE: LLM Parser (fallback)
→ ts-extractor (processes chunks)
→ ts-formatter
→ ps-critic
```

**TDD Reference:** TDD-FEAT-004 Section 10 (lines 1773-1805)

### Acceptance Criteria

- [x] Agent Pipeline diagram updated to show hybrid architecture
- [x] Available Agents table updated with ts-parser v2.0 role
- [x] Output Structure section reflects chunked output (index.json + chunks/)
- [x] Orchestration Flow shows format detection and routing
- [x] State Passing shows chunked input/output schema
- [x] Backward compatibility noted for non-VTT formats

### Implementation Notes

**Updates Required:**

1. **Agent Pipeline Diagram (lines ~196-222)**
   - Add format detection branching
   - Show Python parser path for VTT
   - Show LLM fallback path for non-VTT
   - Show chunker in pipeline

2. **Available Agents Table (lines ~228-234)**
   - Change ts-parser role from "Parse VTT/SRT/TXT to canonical JSON"
   - To: "ORCHESTRATOR: Route to Python/LLM parser, validate output, coordinate chunking"
   - Add note about model: "haiku (orchestration), Python (VTT parsing)"

3. **Agent Capabilities Summary (lines ~236-260)**
   - Update ts-parser section to describe v2.0 roles:
     - ORCHESTRATOR: Coordinate pipeline
     - DELEGATOR: Route to Python parser for VTT
     - FALLBACK: LLM for non-VTT
     - VALIDATOR: Verify Python output

4. **Output Structure (lines ~298-320)**
   - Add hybrid output format:
     ```
     transcript-{id}/
     ├── 00-index.md
     ├── 01-summary.md
     ├── canonical/
     │   ├── index.json           # NEW: Chunk index
     │   └── chunks/              # NEW: Chunked segments
     │       ├── chunk-000.json
     │       ├── chunk-001.json
     │       └── ...
     ├── 02-transcript.md
     └── ...
     ```

5. **Orchestration Flow (lines ~322-390)**
   - Update STEP 1: PARSE to show format detection
   - Add chunking step after parsing
   - Update state passing schema

**Target Pipeline Diagram:**
```
TRANSCRIPT SKILL PIPELINE (v2.0 HYBRID)
=======================================

                    USER INPUT (VTT/SRT/TXT)
                           │
                           ▼
    ┌───────────────────────────────────────────────────────┐
    │              ts-parser v2.0 (ORCHESTRATOR)            │
    │          Model: haiku (orchestration only)            │
    └───────────────────────┬───────────────────────────────┘
                            │
           ┌────────────────┴────────────────┐
           │ Format Detection                │
           ▼                                 ▼
    ┌─────────────┐                   ┌─────────────┐
    │ VTT (Python)│                   │ SRT/TXT (LLM)│
    │  DELEGATOR  │                   │  FALLBACK   │
    └──────┬──────┘                   └──────┬──────┘
           │                                 │
           ▼                                 │
    ┌─────────────┐                          │
    │  VALIDATOR  │                          │
    └──────┬──────┘                          │
           │                                 │
           ▼                                 │
    ┌─────────────┐                          │
    │   Chunker   │                          │
    │  (500 segs) │                          │
    └──────┬──────┘                          │
           │                                 │
           └────────────────┬────────────────┘
                            ▼
    ┌───────────────────────────────────────────────────────┐
    │              ts-extractor (sonnet)                    │
    │          Processes chunks or monolithic               │
    └───────────────────────┬───────────────────────────────┘
                            │
                            ▼
    ┌───────────────────────────────────────────────────────┐
    │              ts-formatter (sonnet)                    │
    │          Generates 8-file packet                      │
    └───────────────────────┬───────────────────────────────┘
                            │
                            ▼
    ┌───────────────────────────────────────────────────────┐
    │              ps-critic (sonnet)                       │
    │          Quality validation >= 0.90                   │
    └───────────────────────────────────────────────────────┘
```

### Related Items

- Parent: [EN-025: ts-parser v2.0 + CLI + SKILL.md Integration](./EN-025-skill-integration.md)
- References: [TDD-FEAT-004 Section 10](../docs/design/TDD-FEAT-004-hybrid-infrastructure.md)
- Target File: [skills/transcript/SKILL.md](../../../../../skills/transcript/SKILL.md)
- Depends On: [TASK-250: ts-parser v2.0 transformation](./TASK-250-ts-parser-v2-transformation.md)

---

## Time Tracking

| Metric            | Value           |
|-------------------|-----------------|
| Original Estimate | 2 hours |
| Remaining Work    | 0 hours    |
| Time Spent        | 0.5 hours        |

---

## Evidence

### Deliverables

| Deliverable | Type | Link |
|-------------|------|------|
| SKILL.md update | Documentation | skills/transcript/SKILL.md |

### Verification

- [ ] Pipeline diagram shows hybrid architecture
- [ ] Available Agents table reflects ts-parser v2.0
- [ ] Orchestration flow includes format detection
- [ ] Output structure shows chunked format
- [ ] Backward compatibility documented

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-01-29 | Created | Initial task creation per EN-025 |
