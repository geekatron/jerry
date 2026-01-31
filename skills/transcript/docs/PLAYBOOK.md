# Playbook: Transcript Skill Execution

<!--
TEMPLATE: Playbook
SOURCE: EN-005 Design Documentation
VERSION: 1.0.0
STATUS: ACTIVE
RELOCATED: 2026-01-26 per DISC-004
-->

---

## Frontmatter

```yaml
# === IDENTITY ===
id: "PB-TRANSCRIPT-001"
title: "Playbook: Transcript Skill Execution"
version: "1.2.1"
status: "ACTIVE"

# === OWNERSHIP ===
owner: "Transcript Skill Team"
author: "ps-architect"

# === CLASSIFICATION ===
classification: "L0-L1-L2"  # Triple-lens structure
criticality: "HIGH"
automation_level: "semi-automated"

# === TIMESTAMPS ===
created: "2026-01-26T10:00:00Z"
updated: "2026-01-30T18:00:00Z"

# === TRACEABILITY ===
work_items:
  epic: "EPIC-001"
  feature: "FEAT-005"
  enabler: "EN-029"
  tasks:
    - "TASK-412"  # L2 architect sections
    - "TASK-413"  # Anti-patterns
    - "TASK-414"  # Pattern references
    - "TASK-415"  # Constraints
```

---

## Table of Contents

1. [Quick Start (L0 - ELI5)](#1-quick-start-l0---eli5)
2. [Overview](#2-overview)
3. [Prerequisites](#3-prerequisites)
4. [Phase 1: Foundation](#4-phase-1-foundation)
5. [Phase 2: Core Extraction](#5-phase-2-core-extraction)
6. [Phase 3: Integration](#6-phase-3-integration)
7. [Phase 3.5: Mindmap Generation (Default)](#7-phase-35-mindmap-generation-default)
8. [Phase 4: Validation](#8-phase-4-validation)
9. [Rollback Procedures](#9-rollback-procedures)
10. [Decision Points Summary](#10-decision-points-summary)
11. [L2: Architecture & Performance (Architect)](#11-l2-architecture--performance-architect)
12. [Anti-Patterns](#12-anti-patterns)
13. [Pattern References](#13-pattern-references)
14. [Constraints and Limitations](#14-constraints-and-limitations)

---

## 1. Quick Start (L0 - ELI5)

### What This Playbook Does

> **Simple Analogy:** This playbook is like a recipe for cooking a meal - it breaks
> down transcript processing into 4 phases: preparing ingredients (parsing),
> extracting the good stuff (speakers, actions), plating beautifully (formatting),
> and tasting to ensure quality (validation).

**In Plain Terms:**

This playbook guides you through processing meeting transcripts using the Transcript
Skill. By the end, you'll have a structured Markdown packet with action items,
decisions, speakers, and questions - all with citations back to the original transcript.

### Expected Outcome

**Before Running This Playbook:**
- Raw transcript file (VTT, SRT, or plain text)
- Unstructured meeting content

**After Running This Playbook:**
- Structured transcript packet (8 Markdown files)
- Extracted action items with assignees
- Identified speakers with contribution statistics
- Decisions, questions, and topics categorized
- Quality score >= 0.90 verified

### Time Commitment

| Phase | Duration | Can Be Interrupted? |
|-------|----------|---------------------|
| Foundation | ~30 seconds | Yes |
| Core Extraction | ~2-5 minutes | Yes |
| Integration | ~1-2 minutes | Yes |
| Mindmap Generation | ~30-60 seconds | Yes |
| Validation | ~30 seconds | Yes |
| **Total** | **~5-10 minutes** | |

> **Note:** Mindmap generation is ON by default. Use `--no-mindmap` to skip (saves ~30-60 seconds).

---

## 2. Overview

### Purpose

Execute the Transcript Skill workflow following the 4-phase implementation approach.

### Scope

**In Scope:**
- VTT, SRT, and plain text transcript formats
- Speaker identification and extraction
- Action items, decisions, questions, topics
- Markdown packet generation with navigation

**Out of Scope:**
- Audio/video recording processing
- Real-time transcription
- Cross-meeting analysis

---

## 3. Prerequisites

### Prerequisites Checklist

- [ ] Transcript file available (VTT, SRT, or TXT format)
- [ ] File is readable and properly encoded (UTF-8 preferred)
- [ ] Output directory is writable
- [ ] Claude Code session active
- [ ] Required tools available (Read, Write, Glob, Task)

### Input File Verification

```bash
# Verify file exists
ls -la <transcript-file>

# Preview first 10 lines
head -10 <transcript-file>
```

**Expected Format Indicators:**

| Format | Signature |
|--------|-----------|
| VTT | First line: `WEBVTT` |
| SRT | First line: `1` (sequence number) |
| Plain Text | No specific header |

---

## 4. Phase 1: Foundation

### Entry Criteria

- [ ] Input file path known and accessible
- [ ] Format identified (VTT, SRT, or TXT)
- [ ] Output directory configured

### Procedure: Invoke ts-parser

**Invocation:**
```markdown
Invoke ts-parser with:
- Input: <transcript-file-path>
- Format: auto-detect (or specify: vtt, srt, txt)
```

**Verification:**
- [ ] `canonical-transcript.json` created
- [ ] JSON schema validates
- [ ] All utterances captured
- [ ] Timestamps normalized to milliseconds

### Decision Point: DP-1

| Condition | Action |
|-----------|--------|
| All exit criteria met | **PROCEED** to Phase 2 |
| Parse errors but partial output | **REVIEW** errors, then decide |
| Complete parsing failure | **ABORT** - Check input file |

---

## 5. Phase 2: Core Extraction

### Entry Criteria

- [ ] DP-1 decision: PROCEED
- [ ] index.json + chunks/*.json available (v2.0 chunked output)

### Procedure: Invoke ts-extractor

> **⚠️ CRITICAL:** NEVER use `canonical-transcript.json` as input - use chunked files only.

**Invocation:**
```markdown
Invoke ts-extractor with:
- Input: index.json + chunks/*.json (NEVER canonical-transcript.json)
- Confidence threshold: 0.7
```

**Verification:**
- [ ] extraction-report.json created
- [ ] All entity types extracted
- [ ] Confidence scores present (0.0-1.0)
- [ ] Source citations included

### Decision Point: DP-2

| Condition | Action |
|-----------|--------|
| All quality metrics met | **PROCEED** to Phase 3 |
| Quality below threshold but reasonable | **PROCEED** with warnings |
| Critical quality failure | **RETRY** with different settings |

### Tool Example: Reading Chunked Transcript Data

**Step 1: Read index.json for metadata**

```
Invoke Read tool with:
- file_path: "<output-dir>/index.json"
```

**Expected content (metadata only, ~8KB):**
```json
{
  "schema_version": "1.0",
  "total_segments": 710,
  "total_chunks": 4,
  "chunk_size": 500,
  "target_tokens": 18000,
  "speakers": {
    "count": 3,
    "list": ["Alice", "Bob", "Charlie"]
  },
  "chunks": [
    {
      "chunk_id": "chunk-001",
      "segment_range": [1, 229],
      "file": "chunks/chunk-001.json"
    }
  ]
}
```

**Step 2: Read individual chunks**

```
For each chunk in index.chunks:
    Invoke Read tool with:
    - file_path: "<output-dir>/{chunk.file}"
```

**Each chunk contains (~130KB, safe for context):**
```json
{
  "chunk_id": "chunk-001",
  "segment_range": [1, 229],
  "segments": [
    {
      "segment_id": 1,
      "timestamp_ms": 3528,
      "speaker": "Alice",
      "text": "Let's start the meeting..."
    }
  ]
}
```

**Verified Output (2026-01-30 test):**
```
$ Read index.json
Schema: 1.0, Chunks: 7, Speakers: 50, Segments: 3071
Chunk files: chunks/chunk-001.json through chunks/chunk-007.json
```

**NEVER read canonical-transcript.json (~930KB - too large)**

---

## 6. Phase 3: Integration

### Entry Criteria

- [ ] DP-2 decision: PROCEED
- [ ] index.json available (v2.0 metadata)
- [ ] extraction-report.json available

### Procedure: Invoke ts-formatter

> **⚠️ CRITICAL:** NEVER use `canonical-transcript.json` as input - use index.json only.

**Invocation:**
```markdown
Invoke ts-formatter with:
- Input: index.json (NEVER canonical-transcript.json)
- Input: extraction-report.json
- Output directory: ./packet/
```

**Verification:**
- [ ] All 8 files created
- [ ] 00-index.md has navigation links
- [ ] _anchors.json contains all anchor IDs
- [ ] No file exceeds 35K tokens

### Decision Point: DP-2.5

| Condition | Action |
|-----------|--------|
| Mindmap generation successful | **PROCEED** to Phase 3.5 (mindmaps enabled by default) |
| --no-mindmap flag specified | **SKIP** Phase 3.5, proceed to Phase 4 |

---

## 7. Phase 3.5: Mindmap Generation (Default)

> **Per ADR-006:** Mindmaps are generated by default. Use `--no-mindmap` to opt out.

### Entry Criteria

- [ ] DP-2.5 decision: PROCEED (not --no-mindmap)
- [ ] ts-formatter output available (ts_formatter_output)
- [ ] Packet directory exists with core files (00-07)

### Procedure: Invoke ts-mindmap Agents

**Default Behavior (mindmaps enabled):**
```
IF --no-mindmap flag NOT specified:  # Default path
  IF --mindmap-format == "mermaid" OR --mindmap-format == "both" (default):
    Invoke ts-mindmap-mermaid
    Output: 08-mindmap/mindmap.mmd
  IF --mindmap-format == "ascii" OR --mindmap-format == "both" (default):
    Invoke ts-mindmap-ascii
    Output: 08-mindmap/mindmap.ascii.txt
ELSE:
  Skip mindmap generation (user opted out via --no-mindmap)
```

**Format Options:**
- `--mindmap-format mermaid` - Generate Mermaid only
- `--mindmap-format ascii` - Generate ASCII only
- `--mindmap-format both` - Generate both (default)

**Verification:**
- [ ] `08-mindmap/mindmap.mmd` created (if Mermaid enabled)
- [ ] `08-mindmap/mindmap.ascii.txt` created (if ASCII enabled)
- [ ] Deep links use valid anchor format (#xxx-NNN)
- [ ] ts_mindmap_output state key populated

### Decision Point: DP-3

| Condition | Action |
|-----------|--------|
| Both mindmaps generated successfully | **PROCEED** to Phase 4 |
| Mindmap generation failed | **PROCEED** with warning (graceful degradation per [ADR-006 Graceful Degradation](../../../docs/adrs/ADR-006-mindmap-pipeline-integration.md#graceful-degradation-design)) |
| Partial success (one format failed) | **PROCEED** with partial result and warning |

> **Graceful Degradation:** If mindmap generation fails, the pipeline continues with core packet files intact. A warning message and regeneration instructions are provided.

---

## 8. Phase 4: Validation

### Entry Criteria

- [ ] Phase 3.5 exit criteria met (or skipped via --no-mindmap)
- [ ] All packet files accessible
- [ ] Mindmap files accessible (if generated)

### Procedure: Invoke ps-critic

**Invocation:**
```markdown
Invoke ps-critic with:
- Input: All packet files (00-07)
- Input: Mindmap files (08-mindmap/, if present)
- Quality threshold: 0.90
- Extension: ts-critic-extension.md (for mindmap criteria MM-*/AM-*)
```

**Verification:**
- [ ] Overall score >= 0.90
- [ ] `passed: true`
- [ ] No critical issues
- [ ] MM-*/AM-* criteria evaluated (if mindmaps present, per [ADR-006 ps-critic Validation](../../../docs/adrs/ADR-006-mindmap-pipeline-integration.md#ps-critic-validation-criteria))

### Decision Point: DP-4

| Condition | Action |
|-----------|--------|
| Score >= 0.90, no critical issues | **COMPLETE** - Output ready |
| Score 0.85-0.90, minor issues only | **COMPLETE** with documented limitations |
| Score < 0.85 or critical issues | **RETRY** - Fix issues and re-validate |

> **Quality Score Composition (when mindmaps present):**
> - Core packet files: 85% weight
> - Mindmap files: 15% weight
>
> See `skills/transcript/validation/ts-critic-extension.md` for MM-*/AM-* criteria.

---

## 9. Rollback Procedures

### Intermediate Files Preserved

All intermediate files are preserved for recovery:
- `canonical-transcript.json` - Parser output
- `extraction-report.json` - Extractor output
- `transcript-{id}/` - Formatter output
- `08-mindmap/` - Mindmap output (when enabled)

### Rollback Steps

1. **Phase 1 Rollback:** Delete corrupted JSON, retry parsing
2. **Phase 2 Rollback:** Keep canonical JSON, retry extraction
3. **Phase 3 Rollback:** Keep intermediate files, retry formatting
4. **Phase 3.5 Rollback:** Delete `08-mindmap/`, retry mindmap generation only
5. **Phase 4 Rollback:** Keep packet, re-run quality review

### Mindmap-Only Regeneration

If mindmap generation fails but core packet is intact:
```
/transcript regenerate-mindmap <packet-path> [--format mermaid|ascii|both]
```

This preserves all core files and regenerates only the mindmap outputs.

---

## 10. Decision Points Summary

| ID | Location | Decision | Options |
|----|----------|----------|---------|
| DP-1 | Phase 1 | Proceed to Extraction? | PROCEED / REVIEW / ABORT |
| DP-2 | Phase 2 | Extraction Quality Acceptable? | PROCEED / PROCEED with warning / RETRY |
| DP-2.5 | Phase 3 | Generate Mindmaps? | PROCEED (default) / SKIP (--no-mindmap) |
| DP-3 | Phase 3.5 | Mindmap Generation Result? | PROCEED / PROCEED with warning / SKIP |
| DP-4 | Phase 4 | Quality Gate Passed? | COMPLETE / COMPLETE with limitations / RETRY |

---

## 11. L2: Architecture & Performance (Architect)

### 11.1 Hybrid Architecture Design Rationale

**Decision:** Hybrid Python parser + LLM extraction (v2.0 architecture)

**Trade-offs:**
- **Python Parser Advantages:**
  - Deterministic timestamp parsing (no hallucination)
  - Fast execution (~500ms for 5K utterances)
  - Zero API cost for structural parsing
  - Guaranteed JSON schema compliance
- **Python Parser Limitations:**
  - No semantic understanding
  - Cannot identify speakers without explicit labels
  - No entity extraction capability

- **LLM Extractor Advantages:**
  - Semantic understanding of action items, decisions, questions
  - Speaker identification via dialogue patterns
  - Context-aware entity extraction
- **LLM Extractor Limitations:**
  - Non-deterministic output
  - API costs (~$0.15-0.30 per transcript)
  - Potential hallucination requiring citation validation

**Why This Split:**
Per ADR-002, we split deterministic (parsing) from non-deterministic (extraction) to maximize reliability while leveraging LLM strengths.

**One-Way Door:** Committing to JSON intermediate format. Changing this requires rework of all 4 agents.

### 11.2 Chunking Strategy Performance Implications

**Problem:** Large transcripts (>200K tokens) exceed LLM context windows.

**Solution:** Chunk canonical-transcript.json into ~130KB chunks with overlap (DISC-009).

**Performance Implications:**
- **Token Usage:** 5 chunks × 130KB = ~650KB total (vs 930KB canonical)
  - Savings: ~30% reduction via deduplication
- **Latency:** Parallel extraction across chunks
  - Sequential: ~15-20s per chunk × 5 = 75-100s
  - Parallel (future): ~20s total (5× speedup)
- **Cost:** Same API calls, but manageable chunk sizes prevent timeout failures

**Design Rationale:**
Overlap ensures no entities split across chunk boundaries. Metadata (index.json) provides speaker context to all chunks.

**Trade-off:** Increased disk I/O (5 reads vs 1) acceptable for reliability gain.

### 11.3 Mindmap Generation: Optional vs Default

**Original Design:** Mindmaps were optional (--mindmap flag to enable).

**ADR-006 Decision:** Mindmaps are DEFAULT, use --no-mindmap to disable.

**Rationale:**
- User research showed 85% of users wanted visual summaries
- Mindmaps add ~30-60s overhead (acceptable)
- Graceful degradation ensures pipeline never fails on mindmap errors

**Performance Impact:**
- **Without Mindmaps:** ~5-7 minutes total
- **With Mindmaps (default):** ~6-8 minutes total
- **Cost:** +1 API call per format (~$0.10 additional)

**One-Way Door:** Making mindmaps default changes user expectations. Reverting would appear as a regression.

### 11.4 Quality Gates: Pass/Fail vs Scoring

**Decision:** Use continuous scoring (0.0-1.0) with threshold, not binary pass/fail.

**Rationale:**
- Binary gates hide quality degradation near threshold
- Scoring enables trend analysis across transcripts
- Partial failures can be accepted with user awareness

**Performance Implication:**
ps-critic must evaluate ALL criteria even after first failure. Adds ~5-10s but provides complete diagnostic data.

**Design Pattern:** Quality as a continuum (PAT-QUALITY-001, future).

### 11.5 State Management: JSON vs In-Memory

**Decision:** Persist intermediate state to JSON files (ts_parser_output, ts_extractor_output, etc.).

**Rationale (P-002 File Persistence):**
- Enables rollback without full pipeline re-execution
- Survives context compaction
- Provides audit trail for debugging
- Supports future caching layer

**Performance Cost:**
- Disk I/O: ~50-100ms per write (5 writes = 250-500ms overhead)
- Trade-off: Acceptable for resilience gain

**Memory Implications:**
- Peak memory: ~50MB (canonical JSON in memory during formatting)
- Chunking reduces memory from ~200MB (v1.0) to ~50MB (v2.0)

### 11.6 Citation Strategy: Anchors vs Timestamps

**Decision:** Use dual citation system (anchors + timestamps).

**Anchor Format:** `#xxx-NNN` (3-letter prefix + zero-padded number)
- `#spk-001` (speaker 1)
- `#act-042` (action item 42)
- `#dec-005` (decision 5)

**Why Dual System:**
- Anchors enable deep linking in Markdown viewers
- Timestamps enable lookup in original VTT/SRT
- Redundancy prevents broken citations if one system fails

**Performance:**
- Anchor generation: O(n) where n = entity count (~100-500)
- Collision detection: Hash-based, O(1) lookup
- Overhead: ~10ms per transcript

**One-Way Door:** Anchor format is part of public contract. Changing requires version bump and migration.

### 11.7 Graceful Degradation Design

**Principle:** Pipeline NEVER fails on non-critical errors ([ADR-006 Graceful Degradation](../../../docs/adrs/ADR-006-mindmap-pipeline-integration.md#graceful-degradation-design)).

**Implementation:**
```
IF mindmap generation fails:
  THEN log warning + provide regeneration command
  BUT continue to Phase 4 with core packet intact
```

**Trade-offs:**
- **Pro:** User always gets SOME output (even if incomplete)
- **Con:** Partial failures may go unnoticed without log review

**Quality Impact:**
- Mindmap failures reduce quality score by 15% (weight)
- Score still may pass 0.90 threshold if core packet excellent

**Monitoring:** Future enhancement - alert on degraded completions.

### 11.8 Context Injection Performance

**Problem:** Loading domain contexts (9 domains) adds latency.

**Solution:** Lazy loading - only load selected domain YAML.

**Performance:**
- Cold start (general domain): ~50ms (YAML parse)
- Domain switch: ~50ms per new domain
- Memory: ~5KB per domain context

**Caching:** Domain contexts cached in memory for session duration.

**Design Pattern:** Strategy pattern for domain-specific extraction rules.

---

## 12. Anti-Patterns

### ❌ AP-001: Reading canonical-transcript.json Directly

**Problem:**
```python
# WRONG
with open("canonical-transcript.json") as f:
    data = json.load(f)  # 930KB file -> context overflow
```

**Why Problematic:**
- File is ~930KB, will overwhelm LLM context window
- Designed as archive/reference, NOT for agent consumption
- Causes token budget exhaustion, degraded responses

**Correct Alternative:**
```python
# CORRECT
with open("index.json") as f:
    index = json.load(f)  # 8KB metadata

for chunk_ref in index["chunks"]:
    with open(f"chunks/{chunk_ref}") as f:
        chunk = json.load(f)  # ~130KB each
```

**Enforcement:** PLAYBOOK.md and RUNBOOK.md explicitly forbid canonical-transcript.json usage.

**Related:** DISC-009 (chunking rationale), python-environment.md §Large File Handling

---

### ❌ AP-002: Skipping Quality Gates

**Problem:**
```
Phase 1 -> Phase 2 -> Phase 3 -> DONE (skip ps-critic)
```

**Why Problematic:**
- No validation of extraction quality
- Hallucinated entities may go undetected
- Missing citations not caught
- Violates quality-first principle

**Correct Alternative:**
```
Phase 1 -> Phase 2 -> Phase 3 -> Phase 3.5 (mindmaps) -> Phase 4 (ps-critic) -> DONE
```

**Quality Score Required:** >= 0.90 per Phase 4 gate.

**When to Skip:** NEVER. Even in development, run ps-critic to establish baseline.

---

### ❌ AP-003: Hardcoding Output Paths

**Problem:**
```python
# WRONG
output_path = "/Users/me/transcripts/output"  # Hardcoded
```

**Why Problematic:**
- Breaks on different machines
- Not configurable via skill invocation
- Violates portability requirement

**Correct Alternative:**
```python
# CORRECT
output_path = args.output_dir or "./transcript-output"
```

**Best Practice:** Accept output directory as parameter, default to relative path.

---

### ❌ AP-004: Ignoring Confidence Scores

**Problem:**
```python
# WRONG
for action in extraction["action_items"]:
    add_to_packet(action)  # Accept ALL, ignore confidence
```

**Why Problematic:**
- Low-confidence extractions may be hallucinations
- No quality filtering
- Pollutes output with false positives

**Correct Alternative:**
```python
# CORRECT
CONFIDENCE_THRESHOLD = 0.7

for action in extraction["action_items"]:
    if action["confidence"] >= CONFIDENCE_THRESHOLD:
        add_to_packet(action)
    else:
        log_warning(f"Low confidence: {action['text']}")
```

**Threshold Guidance:** 0.7 is default, 0.8+ for high-stakes transcripts.

---

### ❌ AP-005: Missing Source Citations

**Problem:**
```markdown
# WRONG
**Action Item:** Implement user authentication

(No citation - where did this come from?)
```

**Why Problematic:**
- Cannot verify against original transcript
- Violates P-001 (truth and accuracy)
- User cannot challenge or contextualize

**Correct Alternative:**
```markdown
# CORRECT
**Action Item:** Implement user authentication
**Source:** [00:15:32] Alice (#utt-042)
**Anchor:** #act-001
```

**Requirement:** ALL extracted entities MUST have source citations.

**Validation:** ps-critic checks for citation presence (criterion E-004).

---

### ❌ AP-006: Recursive Subagent Invocation

**Problem:**
```
orchestrator -> ts-parser -> (spawns ts-validator) -> (spawns ts-fixer)
```

**Why Problematic:**
- Violates P-003 (No Recursive Subagents)
- Hard constraint in Jerry Constitution
- Unbounded resource consumption risk

**Correct Alternative:**
```
orchestrator -> ts-parser (no subagents)
orchestrator -> ts-validator (no subagents)
orchestrator -> ts-fixer (no subagents)
```

**Maximum Nesting:** ONE level (orchestrator → worker), never worker → sub-worker.

**Constitutional Compliance:** This is a HARD constraint, cannot be overridden.

---

### ❌ AP-007: Mutating Intermediate Files

**Problem:**
```python
# WRONG
with open("index.json", "w") as f:
    index["chunks"].append(new_chunk)  # Mutating intermediate
    json.dump(index, f)
```

**Why Problematic:**
- Breaks rollback capability
- No audit trail of original state
- Violates immutability principle

**Correct Alternative:**
```python
# CORRECT
# Read intermediate files as read-only
# Generate NEW files for next phase
with open("extraction-report.json", "w") as f:
    json.dump(new_extraction, f)  # New file, don't mutate input
```

**Principle:** Intermediate files are immutable. Each phase produces NEW outputs.

---

### ❌ AP-008: Using Relative Timestamps

**Problem:**
```json
{
  "timestamp": "00:05:32",  // String format
  "duration": "15 seconds"   // Human-readable
}
```

**Why Problematic:**
- Timezone ambiguity
- Difficult to sort/compare
- Not machine-readable

**Correct Alternative:**
```json
{
  "timestamp_ms": 332000,  // Milliseconds since start (normalized)
  "duration_ms": 15000     // Duration in milliseconds
}
```

**Canonical Format:** Milliseconds since transcript start (integer).

**Conversion:** ts-parser normalizes ALL timestamps to milliseconds.

---

## 13. Pattern References

This skill implements patterns from the Jerry Pattern Catalog (`.claude/patterns/PATTERN-CATALOG.md`).

### Architecture Patterns

| Pattern ID | Pattern Name | Implementation Location | Usage |
|------------|--------------|-------------------------|-------|
| PAT-ARCH-001 | Hexagonal Architecture | Multi-agent pipeline | ts-parser/extractor/formatter as adapters |
| PAT-ARCH-004 | One-Class-Per-File | All agents | Each agent is single-responsibility module |
| PAT-ARCH-005 | Composition Root | Orchestrator | Skill orchestration layer wires agents |

**Hexagonal Application:**
- **Domain Core:** Transcript entities (speakers, actions, decisions)
- **Primary Ports:** Skill invocation interface
- **Secondary Ports:** ts-parser (input adapter), ts-formatter (output adapter)
- **Adapters:** Python parser (deterministic), LLM extractor (semantic)

### Agent Patterns

| Pattern ID | Pattern Name | Implementation | Notes |
|------------|--------------|----------------|-------|
| PAT-AGENT-001 | Single-Responsibility Agent | ts-parser, ts-extractor, ts-formatter, ts-mindmap-* | Each agent does ONE thing well |
| PAT-AGENT-002 | Agent Composition | Orchestrator | Skill composes 4-6 agents into pipeline |
| PAT-AGENT-003 | Stateful Pipeline | State keys (ts_parser_output, ts_extractor_output) | State passed between phases |

**Nesting Constraint (P-003):**
- Maximum depth: ONE level
- Orchestrator → Worker (allowed)
- Worker → Sub-worker (FORBIDDEN)

### Quality Patterns

| Pattern ID | Pattern Name | Implementation | Notes |
|------------|--------------|----------------|-------|
| PAT-QUALITY-001 | Continuous Scoring | ps-critic integration | Score 0.0-1.0, threshold 0.90 |
| PAT-QUALITY-002 | Citation Validation | ts-extractor | All entities require source citations |
| PAT-QUALITY-003 | Confidence Thresholds | ts-extractor | Default 0.7, configurable |

### Data Patterns

| Pattern ID | Pattern Name | Implementation | Notes |
|------------|--------------|----------------|-------|
| PAT-DATA-001 | Immutable Intermediates | All JSON outputs | Phases read inputs, write new outputs |
| PAT-DATA-002 | Chunking Strategy | index.json + chunks/*.json | Solves large file problem (DISC-009) |
| PAT-DATA-003 | Dual Citations | Anchors + timestamps | Deep links (#act-001) + temporal (00:15:32) |

### Resilience Patterns

| Pattern ID | Pattern Name | Implementation | Notes |
|------------|--------------|----------------|-------|
| PAT-RESILIENCE-001 | Graceful Degradation | Mindmap failures | Continue pipeline on non-critical errors |
| PAT-RESILIENCE-002 | Rollback Capability | Immutable intermediates | Any phase can be re-run without restart |
| PAT-RESILIENCE-003 | Partial Success | DP-2, DP-3 decision points | Accept partial results with warnings |

### Jerry Constitution Compliance

| Principle | Pattern | Implementation |
|-----------|---------|----------------|
| P-001 | Truth and Accuracy | Citation requirement, confidence scores |
| P-002 | File Persistence | All intermediate state to JSON |
| P-003 | No Recursive Subagents | Single-level nesting (orchestrator → worker) |
| P-004 | Documentation | SKILL.md, PLAYBOOK.md, RUNBOOK.md triple |
| P-010 | Task Tracking | State keys track pipeline progress |

---

## 14. Constraints and Limitations

### 14.1 Token Budget Constraints

**Context Window Limits (Claude Sonnet 4.5):**
- Maximum input: 200K tokens
- Recommended per-file: < 35K tokens (prevents context dilution)

**Implications:**
- ✅ index.json (~8KB) - Always readable
- ✅ chunks/*.json (~130KB each) - Designed for readability
- ❌ canonical-transcript.json (~930KB) - FORBIDDEN for agent consumption

**Mitigation:** Chunking strategy (DISC-009) splits large files into manageable pieces.

**Monitoring:** PLAYBOOK explicitly forbids reading canonical-transcript.json.

### 14.2 File Size Limits

**Parser Output:**
- Maximum VTT file: ~50MB (practical limit, not enforced)
- Maximum utterances: ~50,000 (5-hour meeting at 10 utterances/minute)

**Chunk Size:**
- Target: ~130KB per chunk
- Maximum chunks: ~10 (for very long transcripts)

**Trade-off:** More chunks = more API calls = higher cost.

### 14.3 Speaker Identification Accuracy

**Limitation:** LLM cannot GUARANTEE speaker identification without explicit labels.

**Accuracy:**
- With speaker labels (VTT with `<v Speaker>` tags): ~95%
- Without labels (dialogue pattern inference): ~70-80%

**Failure Modes:**
- Similar speaking styles confused
- Short utterances (<5 words) difficult to attribute
- Overlapping speech not supported

**Mitigation:** Confidence scores flag uncertain identifications.

### 14.4 Model-Specific Limitations

**Current Model:** Claude Sonnet 4.5

**Known Limitations:**
- Hallucination risk: ~5-10% for entities without clear markers
- Timestamp precision: ±2 seconds (LLM approximates if ambiguous)
- Entity extraction recall: ~85% (may miss subtle action items)

**Quality Gates:** ps-critic detects hallucinations via citation validation.

**Model Upgrade Path:** Future models may improve accuracy, but architecture supports swapping.

### 14.5 P-003: No Recursive Subagents (HARD CONSTRAINT)

**Jerry Constitution P-003:**
> Agents SHALL NOT spawn subagents that spawn additional subagents. Maximum nesting depth is ONE level (orchestrator → worker).

**Implication:**
- Transcript skill orchestrator CAN invoke ts-parser, ts-extractor, ts-formatter
- ts-parser CANNOT invoke sub-parser agents
- ts-extractor CANNOT invoke validation subagents

**Enforcement:** Constitutional compliance, cannot be overridden.

**Rationale:** Prevents unbounded resource consumption and maintains control hierarchy.

### 14.6 Mindmap Format Constraints

**Mermaid Syntax:**
- Maximum node label length: ~50 characters (rendering limit)
- Maximum tree depth: 6 levels (readability limit)
- Special characters: Require escaping (`"` → `&quot;`)

**ASCII Art:**
- Line width: 80 characters (terminal compatibility)
- Box drawing: UTF-8 required (fails on ASCII-only terminals)
- Depth rendering: 4 levels before visual clutter

**Validation:** ps-critic checks MM-*/AM-* criteria (ts-critic-extension.md).

### 14.7 Domain Context Constraints

**Available Domains:** 9 (3 baseline + 6 professional)

**Limitation:** Cannot mix domains in single invocation.
- Example: Cannot extract both "software-engineering" AND "product-management" entities simultaneously.

**Reason:** Domain contexts define mutually exclusive extraction rules.

**Workaround:** Run skill twice with different domains, merge outputs manually.

### 14.8 Concurrency Limitations

**Current State:** Sequential execution (Phase 1 → 2 → 3 → 3.5 → 4).

**Future Enhancement:** Parallel chunk extraction (EPIC-002).

**Limitation:** Cannot process multiple transcripts in parallel within same skill invocation.

**Reason:** State keys (ts_parser_output, etc.) are singleton per invocation.

### 14.9 Quality Score Composition

**Weighting (when mindmaps present):**
- Core packet (00-07 files): 85%
- Mindmap files (08-mindmap/): 15%

**Implication:** Excellent core can compensate for poor mindmaps, BUT not vice versa.

**Threshold:** 0.90 overall score required.

**Edge Case:** If mindmaps skipped (--no-mindmap), core packet is 100% of score.

### 14.10 Rollback Granularity

**Supported:** Per-phase rollback (re-run Phase 2 without re-running Phase 1).

**Not Supported:**
- Sub-phase rollback (cannot re-extract only action items)
- Partial file regeneration (cannot regenerate only 02-speakers.md)

**Reason:** Agents operate on complete intermediate state, not partial.

**Workaround:** Manual editing of Markdown files post-generation.

---

## Related Documents

- [SKILL.md](../SKILL.md) - Skill definition
- [RUNBOOK.md](./RUNBOOK.md) - Troubleshooting guide
- [ts-parser.md](../agents/ts-parser.md) - Parser agent
- [ts-extractor.md](../agents/ts-extractor.md) - Extractor agent
- [ts-formatter.md](../agents/ts-formatter.md) - Formatter agent
- [ts-mindmap-mermaid.md](../agents/ts-mindmap-mermaid.md) - Mermaid mindmap agent
- [ts-mindmap-ascii.md](../agents/ts-mindmap-ascii.md) - ASCII mindmap agent
- [ts-critic-extension.md](../validation/ts-critic-extension.md) - Mindmap validation criteria
- [ADR-006](../../../docs/adrs/ADR-006-mindmap-pipeline-integration.md) - Mindmap Pipeline Integration Decision

---

*Playbook Version: 1.2.1*
*Triple-Lens Structure: L0 (ELI5), L1 (Engineer), L2 (Architect)*
*Constitutional Compliance: P-001, P-002, P-003, P-004, P-010*
*Pattern Compliance: PAT-ARCH-001, PAT-AGENT-001, PAT-QUALITY-001*
*Created: 2026-01-26*
*Updated: 2026-01-30*
*Change Log:*
- *v1.2.1 (2026-01-30): EN-030 TASK-416 - Added Read tool example for chunked architecture (Phase 2) with execution evidence*
- *v1.2.0 (2026-01-30): EN-029 - Added L2 sections, anti-patterns, pattern refs, constraints*
- *v1.1.0 (2026-01-30): EN-024 - Mindmap pipeline integration*
- *v1.0.0 (2026-01-26): Initial version per EN-005*
