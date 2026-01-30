# TASK-240: Pipeline State Research

<!--
TEMPLATE: Research
VERSION: 1.0.0
SOURCE: .context/templates/worktracker/TASK.md
TASK: EN-024:TASK-240
-->

---

## Frontmatter

```yaml
id: "EN-024:TASK-240:RESEARCH"
title: "Current Pipeline State Analysis"
version: "1.0.0"
status: "COMPLETE"
created_at: "2026-01-28T00:00:00Z"
completed_at: "2026-01-28T00:00:00Z"
author: "Claude"
parent_task: "EN-024:TASK-240"
```

---

## Executive Summary

This research documents the current state of the transcript skill pipeline to identify integration points for optional mindmap generation. The analysis covers the 4-stage architecture, state passing mechanisms, and the existing (but not integrated) mindmap agents.

**Key Finding:** The mindmap agents (ts-mindmap-mermaid, ts-mindmap-ascii) exist and are fully implemented per EN-009, but they are NOT wired into the pipeline orchestration. This is the integration gap that EN-024 addresses.

---

## 1. Current Pipeline Architecture

### 1.1 Pipeline Overview (L0 - ELI5)

The transcript skill is like a factory assembly line:
1. **Reception Desk (ts-parser)** - Takes your raw meeting recording and organizes it
2. **Research Analyst (ts-extractor)** - Finds all the important stuff (actions, decisions)
3. **Publishing House (ts-formatter)** - Makes beautiful documents from the findings
4. **Quality Inspector (ps-critic)** - Checks everything meets standards

**Current Gap:** There's a "Visualization Department" (mindmap agents) that exists but isn't connected to the assembly line.

### 1.2 Pipeline Flow Diagram (L1 - Engineer)

```
CURRENT PIPELINE (4-Stage)
==========================

USER INPUT (VTT/SRT/TXT)
         │
         ▼
┌─────────────────────────────────────────────────────────────┐
│                    SKILL.md ORCHESTRATOR                     │
│                 (Constitutional: P-003 compliant)            │
└─────────────────────────────────────────────────────────────┘
         │
         │ Sequential Execution
         ▼
    ┌─────────┐     ┌─────────────┐     ┌─────────────┐     ┌──────────┐
    │ts-parser│────▶│ts-extractor │────▶│ts-formatter │────▶│ps-critic │
    │ (haiku) │     │  (sonnet)   │     │  (sonnet)   │     │ (sonnet) │
    └─────────┘     └─────────────┘     └─────────────┘     └──────────┘
         │               │                    │                   │
         ▼               ▼                    ▼                   ▼
    canonical-      extraction-          transcript-{id}/     quality-
    transcript.json report.json          (8 files)            review.md


EXISTING BUT NOT INTEGRATED
===========================

                    ┌─────────────────┐     ┌────────────────┐
                    │ts-mindmap-mermaid│    │ts-mindmap-ascii│
                    │    (sonnet)      │    │    (sonnet)    │
                    └─────────────────┘     └────────────────┘
                            │                       │
                            ▼                       ▼
                    08-mindmap/              08-mindmap/
                    mindmap.mmd              mindmap.ascii.txt
```

### 1.3 Architectural Analysis (L2 - Architect)

**Constitutional Compliance:**
- P-003 enforced: Single-level nesting (orchestrator → workers)
- P-002 enforced: All outputs persisted to files
- P-020 enforced: User controls input/output paths

**Performance Characteristics:**
| Agent | Model | Typical Duration | Token Consumption |
|-------|-------|------------------|-------------------|
| ts-parser | haiku | ~30 seconds | ~2K tokens |
| ts-extractor | sonnet | ~2-5 minutes | ~10K tokens |
| ts-formatter | sonnet | ~1-2 minutes | ~15K tokens |
| ps-critic | sonnet | ~30 seconds | ~5K tokens |
| **Total** | - | **~5-10 minutes** | **~32K tokens** |

**Mindmap Addition Impact (estimated):**
| Agent | Model | Est. Duration | Est. Token Consumption |
|-------|-------|---------------|----------------------|
| ts-mindmap-mermaid | sonnet | ~30-45 seconds | ~3K tokens |
| ts-mindmap-ascii | sonnet | ~30-45 seconds | ~3K tokens |
| **Total (both)** | - | **~1 minute** | **~6K tokens** |

---

## 2. State Passing Mechanisms

### 2.1 Current State Schema

From SKILL.md Section "L2: State Passing Between Agents":

```yaml
# Stage 1: ts-parser output
ts_parser_output:
  canonical_json_path: string      # Path to canonical-transcript.json
  format_detected: vtt|srt|plain   # Detected format
  segment_count: integer           # Number of utterances
  speaker_count: integer           # Distinct speakers found

# Stage 2: ts-extractor output
ts_extractor_output:
  extraction_report_path: string   # Path to extraction-report.json
  action_count: integer            # Action items found
  decision_count: integer          # Decisions found
  question_count: integer          # Questions found
  high_confidence_ratio: float     # % of entities with conf > 0.85

# Stage 3: ts-formatter output
ts_formatter_output:
  packet_path: string              # Path to transcript-{id}/ directory
  files_created: string[]          # List of created files
  total_tokens: integer            # Token count across all files
  split_files: integer             # Number of split files (if any)

# Stage 4: ps-critic output
quality_output:
  quality_score: float             # 0.0-1.0 aggregate score
  passed: boolean                  # Score >= threshold
  issues: string[]                 # List of issues found
  recommendations: string[]        # Improvement suggestions
```

### 2.2 Mindmap Agent State Schemas (Existing)

From ts-mindmap-mermaid.md and ts-mindmap-ascii.md:

```yaml
# Mermaid mindmap output
ts_mindmap_mermaid_output:
  packet_id: string
  mindmap_path: string             # Path to 08-mindmap/mindmap.mmd
  topic_count: integer
  action_item_count: integer
  decision_count: integer
  question_count: integer
  speaker_count: integer
  deep_link_count: integer         # Number of #anchor references
  overflow_handled: boolean        # True if >50 topics truncated
  status: "complete"|"failed"

# ASCII mindmap output
ts_mindmap_ascii_output:
  packet_id: string
  ascii_path: string               # Path to 08-mindmap/mindmap.ascii.txt
  topic_count: integer
  action_item_count: integer
  decision_count: integer
  question_count: integer
  speaker_count: integer
  max_line_width: integer          # Should be <= 80
  overflow_handled: boolean
  status: "complete"|"failed"
```

### 2.3 Input Requirements for Mindmap Agents

Both mindmap agents require:

| Input | Source | Required |
|-------|--------|----------|
| `extraction_report_path` | ts_extractor_output | Yes |
| `packet_directory` | ts_formatter_output.packet_path | Yes |
| `packet_id` | ts_formatter_output | Yes |
| `meeting_title` | extraction_report.metadata.title | Yes |

**Key Insight:** Mindmap agents need BOTH extractor output (for entities) AND formatter output (for packet path and anchors). This means they must run AFTER ts-formatter, not in parallel.

---

## 3. Output Structure Analysis

### 3.1 Current Packet Structure (ADR-002)

```
transcript-{id}/
├── 00-index.md          # Navigation hub (~2K tokens)
├── 01-summary.md        # Executive summary (~5K tokens)
├── 02-transcript.md     # Full transcript (may split)
├── 03-speakers.md       # Speaker directory
├── 04-action-items.md   # Action items with citations
├── 05-decisions.md      # Decisions with context
├── 06-questions.md      # Open questions
├── 07-topics.md         # Topic segments
└── _anchors.json        # Anchor registry for linking
```

### 3.2 Mindmap Output Structure (After Integration)

```
transcript-{id}/
├── ... (existing 8 files) ...
├── _anchors.json
└── 08-mindmap/                    # NEW: Mindmap directory
    ├── mindmap.mmd                # Mermaid format (if enabled)
    └── mindmap.ascii.txt          # ASCII format (if enabled)
```

### 3.3 Directory Naming Analysis

**IMPORTANT UPDATE (2026-01-30):** See [DISC-001](../EN-024--DISC-001-mindmap-directory-numbering-discrepancy.md) for full analysis.

**Current ts-formatter Implementation (Flat Structure):**
- `07-topics.md` uses index 07 for topics

**Original Mindmap Agent References:**
- `08-mindmap/` also used 07 (CONFLICT!)

**Resolution:** The mindmap output directory is now `08-mindmap/` to avoid numbering confusion:
- `07-topics.md` - Topics file (unchanged)
- `08-mindmap/` - Mindmap directory (CORRECTED)

**Root Cause:** ADR-002 proposed a hierarchical structure with `08-mindmap/`, but ts-formatter implemented a flat structure where 07 was already used for topics. This discrepancy was discovered during EN-024 integration work.

---

## 4. Integration Points Identified

### 4.1 Pipeline Insertion Point

```
INTEGRATION POINT ANALYSIS
==========================

OPTION A: After ts-extractor, parallel with ts-formatter
  ts-parser → ts-extractor ┬→ ts-formatter → ps-critic
                           └→ ts-mindmap-*

  ❌ REJECTED: Mindmaps need packet_path from formatter

OPTION B: After ts-formatter, before ps-critic ✓ SELECTED
  ts-parser → ts-extractor → ts-formatter → [ts-mindmap-*] → ps-critic
                                                 │
                                   (conditional on --mindmap flag)

  ✅ SELECTED:
  - Mindmaps have access to formatter output (packet_path)
  - ps-critic can validate mindmap files if present
  - Clean sequential flow with optional step

OPTION C: After ps-critic
  ts-parser → ts-extractor → ts-formatter → ps-critic → [ts-mindmap-*]

  ❌ REJECTED: ps-critic cannot validate mindmaps
```

### 4.2 State Passing for Mindmaps

Required additions to SKILL.md state schema:

```yaml
# New: Combined mindmap output (for passing to ps-critic)
ts_mindmap_output:
  enabled: boolean                 # Was --mindmap flag used?
  mermaid:
    path: string | null            # null if format != "mermaid" or "both"
    status: "complete"|"failed"|"skipped"
    error_message: string | null
  ascii:
    path: string | null            # null if format != "ascii" or "both"
    status: "complete"|"failed"|"skipped"
    error_message: string | null
  topic_count: integer
  deep_link_count: integer
```

### 4.3 ps-critic Integration Points

Current ps-critic validates:
- Packet file completeness
- Token limits per file
- Anchor registry validity
- Citation accuracy

**Required Additions (when mindmaps present):**
- Mermaid syntax validation (MM-001 through MM-007)
- ASCII format validation (AM-001 through AM-005)
- Deep link validity in mindmaps
- Conditional scoring (80% core + 20% mindmap when enabled)

---

## 5. PLAYBOOK.md Impact Analysis

### 5.1 Current Phase Structure

| Phase | Content | Duration |
|-------|---------|----------|
| 1. Foundation | ts-parser | ~30 seconds |
| 2. Core Extraction | ts-extractor | ~2-5 minutes |
| 3. Integration | ts-formatter | ~1-2 minutes |
| 4. Validation | ps-critic | ~30 seconds |

### 5.2 Proposed Phase Structure (with Mindmap)

| Phase | Content | Duration |
|-------|---------|----------|
| 1. Foundation | ts-parser | ~30 seconds |
| 2. Core Extraction | ts-extractor | ~2-5 minutes |
| 3. Integration | ts-formatter | ~1-2 minutes |
| **3.5. Visualization** | **ts-mindmap-* (if --mindmap)** | **~30-60 seconds** |
| 4. Validation | ps-critic | ~30 seconds |

### 5.3 Decision Point Addition

New decision point DP-2.5 needed:

| Condition | Action |
|-----------|--------|
| Mindmap generation successful | PROCEED to Phase 4 |
| Mindmap generation failed | PROCEED with warning (partial result) |
| --mindmap not specified | SKIP to Phase 4 |

---

## 6. Key Findings

### 6.1 Confirmed Facts

| Finding | Evidence |
|---------|----------|
| Mindmap agents exist and are complete | ts-mindmap-mermaid.md, ts-mindmap-ascii.md |
| Agents are NOT in pipeline | SKILL.md pipeline diagram shows 4 stages only |
| State schemas are defined | Agent files specify output keys |
| Output directory is reserved | ADR-002 specifies 08-mindmap/ |
| ps-critic has NO mindmap validation | ps-critic.md shows no MM-* or AM-* criteria |

### 6.2 Integration Gaps Identified

| Gap ID | Description | Resolution |
|--------|-------------|------------|
| GAP-001 | No --mindmap parameter in SKILL.md | Add to Input Parameters (TASK-243) |
| GAP-002 | No --mindmap-format parameter | Add with mermaid/ascii/both options (TASK-243) |
| GAP-003 | Pipeline doesn't invoke mindmap agents | Update orchestration flow (TASK-244) |
| GAP-004 | ps-critic missing mindmap validation | Add MM-*/AM-* criteria (TASK-245) |
| GAP-005 | PLAYBOOK.md missing Phase 3.5 | Add visualization phase (TASK-247) |
| GAP-006 | RUNBOOK.md missing mindmap troubleshooting | Add section (TASK-247) |
| GAP-007 | No ADR for pipeline integration | Create ADR-006 (TASK-242) |

### 6.3 Risks and Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| Mindmap failure blocks pipeline | HIGH | Graceful degradation (partial result + warning) |
| ps-critic scoring changes affect existing tests | MEDIUM | Conditional scoring (only when mindmaps present) |
| Token budget exceeded with mindmaps | LOW | Mindmaps are separate files, not in 35K limit |

---

## 7. Recommendations

### 7.1 Implementation Order

1. **ADR-006** (TASK-242) - Document architectural decision first
2. **SKILL.md Parameters** (TASK-243) - Add --mindmap and --mindmap-format
3. **Pipeline Orchestration** (TASK-244) - Wire up conditional invocation
4. **ps-critic Update** (TASK-245) - Add validation criteria
5. **Integration Tests** (TASK-246) - Verify all scenarios
6. **Documentation** (TASK-247) - Update PLAYBOOK.md and RUNBOOK.md
7. **Quality Review** (TASK-248) - Final ps-critic validation

### 7.2 State Passing Design

```yaml
# RECOMMENDED: Unified mindmap state for ps-critic
ts_mindmap_output:
  enabled: true
  format_requested: "both"         # From --mindmap-format parameter
  mermaid:
    path: "transcript-{id}/08-mindmap/mindmap.mmd"
    status: "complete"
    topic_count: 15
    deep_link_count: 42
  ascii:
    path: "transcript-{id}/08-mindmap/mindmap.ascii.txt"
    status: "complete"
    topic_count: 15
    max_line_width: 78
  overall_status: "complete"|"partial"|"failed"
  error_messages: []
```

### 7.3 Failure Handling Design

```
FAILURE SCENARIO: Mindmap generation fails

1. Capture error message and status
2. Set ts_mindmap_output.overall_status = "failed"
3. Continue pipeline execution (DO NOT ABORT)
4. Log warning in ps-critic output:
   "⚠️ Mindmap generation failed: {error_message}"
5. Include regeneration instructions:
   "To regenerate mindmaps: /transcript --regenerate-mindmap <packet-path>"
```

---

## 8. Evidence and References

### 8.1 Source Files Analyzed

| File | Location | Key Content |
|------|----------|-------------|
| SKILL.md | skills/transcript/SKILL.md | Pipeline architecture, state schemas |
| ts-formatter.md | skills/transcript/agents/ts-formatter.md | Packet structure, output keys |
| ts-mindmap-mermaid.md | skills/transcript/agents/ts-mindmap-mermaid.md | Mermaid output specification |
| ts-mindmap-ascii.md | skills/transcript/agents/ts-mindmap-ascii.md | ASCII output specification |
| PLAYBOOK.md | skills/transcript/docs/PLAYBOOK.md | Phase structure, decision points |
| ADR-002 | docs/adrs/ADR-002-artifact-structure.md | Packet structure standard |

### 8.2 Cross-References

- **EN-009**: Mind Map Generator (completed) - Agents implemented
- **EN-024**: Mindmap Pipeline Integration (this enabler) - Integration work
- **DEC-001 (EN-024)**: Pipeline integration requirements - User decisions

---

## Document History

| Date | Author | Change |
|------|--------|--------|
| 2026-01-28 | Claude | Initial research completed |
| 2026-01-30 | Claude | Updated Section 3.3: Corrected 07-mindmap/ to 08-mindmap/ per [DISC-001](../EN-024--DISC-001-mindmap-directory-numbering-discrepancy.md) |

---

*Research Complete: EN-024:TASK-240*
*Quality Verification: All source files read and analyzed*
*Next Task: TASK-241 Analysis (5W2H + Ishikawa)*
