---
name: transcript
description: Parse, extract, and format transcripts (VTT, SRT, plain text) into structured Markdown packets with action items, decisions, questions, and topics. Integrates with ps-critic for quality review.
version: "1.0.0"
allowed-tools: Read, Write, Glob, Task
activation-keywords:
  - "transcript"
  - "meeting notes"
  - "parse vtt"
  - "parse srt"
  - "extract action items"
  - "extract decisions"
  - "analyze meeting"
  - "/transcript"
---

# Transcript Skill

> **Version:** 1.0.0
> **Framework:** Jerry Transcript Processing
> **Constitutional Compliance:** Jerry Constitution v1.0 (P-002, P-003, P-020)

---

## Document Audience (Triple-Lens)

This SKILL.md serves multiple audiences:

| Level | Audience | Sections to Focus On |
|-------|----------|---------------------|
| **L0 (ELI5)** | New users, stakeholders | Purpose, When to Use, Quick Reference |
| **L1 (Engineer)** | Developers using the skill | Invoking the Skill, Agent Pipeline |
| **L2 (Architect)** | Workflow designers | Architecture, State Management |

---

## Purpose

The Transcript Skill transforms raw meeting transcripts into structured, navigable knowledge packets. It addresses the **#1 user pain point**: manual extraction of action items, decisions, and key information from meetings.

### Key Capabilities

- **Multi-Format Parsing** - VTT, SRT, and plain text transcript formats
- **Semantic Extraction** - Action items, decisions, questions, topics with confidence scores
- **Speaker Identification** - 4-pattern detection chain for reliable attribution
- **Structured Output** - Claude-optimized Markdown packets under 35K tokens
- **Bidirectional Linking** - Every entity linked to its source in the transcript
- **Quality Review** - Integrated ps-critic evaluation (>= 0.90 threshold)

---

## When to Use This Skill

Activate when:

- Processing a meeting transcript from Zoom, Teams, or other platforms
- Extracting action items and decisions from recorded meetings
- Converting VTT/SRT subtitle files to structured notes
- Analyzing plain text meeting notes
- Generating navigable meeting documentation

**Example Invocations:**
```
"Process this meeting transcript: /path/to/meeting.vtt"
"Extract action items from the quarterly review"
"/transcript analyze-meeting.srt"
"Parse the team standup notes and find all decisions"
```

---

## Agent Pipeline

```
TRANSCRIPT SKILL PIPELINE
=========================

                    USER INPUT
                        │
                        │ Transcript file (VTT/SRT/TXT)
                        │
                        ▼
    ┌─────────────────────────────────────────────────────────┐
    │              SKILL.md ORCHESTRATOR                       │
    │          (P-003: Single-level nesting)                   │
    └─────────────────────────────────────────────────────────┘
                        │
        ┌───────────────┼───────────────┬───────────────┐
        │               │               │               │
        ▼               ▼               ▼               ▼
    ┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐
    │ts-parser │    │ts-extractor│  │ts-formatter│  │ps-critic │
    │ (haiku) │───►│ (sonnet)  │───►│ (sonnet)  │───►│ (sonnet) │
    └─────────┘    └─────────┘    └─────────┘    └─────────┘
         │               │               │               │
         ▼               ▼               ▼               ▼
    Canonical      Extraction       Packet          Quality
    JSON           Report           Files           Report

COMPLIANCE: Each agent is a WORKER. None spawn subagents.
```

---

## Available Agents

| Agent | Model | Role | Output |
|-------|-------|------|--------|
| `ts-parser` | haiku | Parse VTT/SRT/TXT to canonical JSON | `canonical-transcript.json` |
| `ts-extractor` | sonnet | Extract speakers, actions, decisions, questions, topics | `extraction-report.json` |
| `ts-formatter` | sonnet | Generate Markdown packet with navigation | `transcript-{id}/` directory |
| `ps-critic` | sonnet | Validate quality >= 0.90 threshold | `quality-review.md` |

### Agent Capabilities Summary

**ts-parser (Reception Desk):**
- Auto-detect format from file content
- Parse VTT voice tags, SRT speaker prefixes
- Normalize timestamps to milliseconds
- Handle encoding detection (UTF-8, Windows-1252, ISO-8859-1)

**ts-extractor (Research Analyst):**
- 4-pattern speaker detection chain (PAT-003)
- Tiered extraction: Rule → ML → LLM (PAT-001)
- Confidence scoring (0.0-1.0) for all entities
- Mandatory citations for every extraction (PAT-004)

**ts-formatter (Publishing House):**
- ADR-002 packet structure (8 files)
- ADR-004 file splitting at semantic boundaries (31.5K soft limit)
- ADR-003 anchor registry and bidirectional backlinks
- Token counting and limit enforcement

**ps-critic (Quality Inspector):**
- Quality score calculation (aggregate >= 0.90)
- Requirements traceability verification
- ADR compliance checking
- Improvement recommendations

---

## Invoking the Skill

### Option 1: Slash Command

```
/transcript <file-path> [--output <dir>] [--format <vtt|srt|txt>]
```

**Examples:**
```
/transcript meeting.vtt
/transcript standup.srt --output ./docs/meetings/
/transcript notes.txt --format txt
```

### Option 2: Natural Language

```
"Process the transcript at /path/to/meeting.vtt"
"Extract action items from yesterday's team meeting"
"Analyze the quarterly review transcript and create a summary"
```

### Input Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `input_file` | string | Yes | - | Path to transcript file |
| `output_dir` | string | No | `./transcript-output/` | Output directory for packet |
| `format` | string | No | auto-detect | Force format: `vtt`, `srt`, `txt` |
| `confidence_threshold` | float | No | 0.7 | Minimum confidence for extractions |
| `quality_threshold` | float | No | 0.9 | ps-critic quality threshold |

---

## Output Structure (ADR-002)

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

### Token Budget Compliance (ADR-004)

| Limit | Tokens | Action |
|-------|--------|--------|
| Soft | 31,500 | Split at ## heading |
| Hard | 35,000 | Force split |

---

## Orchestration Flow

### L1: Step-by-Step Pipeline

```
STEP 1: PARSE (ts-parser)
─────────────────────────
Input:  Raw transcript file (VTT/SRT/TXT)
Output: canonical-transcript.json
Errors: Format detection failure → warn and default to plain text

STEP 2: EXTRACT (ts-extractor)
──────────────────────────────
Input:  canonical-transcript.json
Output: extraction-report.json
Errors: Low confidence extractions → flag for review

STEP 3: FORMAT (ts-formatter)
─────────────────────────────
Input:  canonical-transcript.json + extraction-report.json
Output: transcript-{id}/ packet directory
Errors: Token overflow → split files automatically

STEP 4: REVIEW (ps-critic)
──────────────────────────
Input:  All generated files
Output: quality-review.md
Errors: Score < 0.90 → report issues for human review
```

### L2: State Passing Between Agents

| Agent | Output Key | Passed To |
|-------|------------|-----------|
| ts-parser | `ts_parser_output` | ts-extractor |
| ts-extractor | `ts_extractor_output` | ts-formatter |
| ts-formatter | `ts_formatter_output` | ps-critic |
| ps-critic | `quality_output` | User/Orchestrator |

**State Schema:**
```yaml
ts_parser_output:
  canonical_json_path: string
  format_detected: vtt|srt|plain
  segment_count: integer
  speaker_count: integer

ts_extractor_output:
  extraction_report_path: string
  action_count: integer
  decision_count: integer
  question_count: integer
  high_confidence_ratio: float

ts_formatter_output:
  packet_path: string
  files_created: string[]
  total_tokens: integer
  split_files: integer

quality_output:
  quality_score: float
  passed: boolean
  issues: string[]
  recommendations: string[]
```

---

## Error Handling

| Error | Detection | Recovery |
|-------|-----------|----------|
| File not found | OS exception | Return clear error message |
| Unknown format | Auto-detect fails | Fallback to plain text parser |
| Encoding error | Decode exception | Try UTF-8, Windows-1252, ISO-8859-1 |
| Token overflow | Count > soft limit | Split at semantic boundary |
| Low confidence | score < threshold | Include in "uncertain" section |
| Quality failure | score < 0.90 | Report issues for human review |

---

## Constitutional Compliance

| Principle | Enforcement | Skill Behavior |
|-----------|-------------|----------------|
| P-002 (File Persistence) | Medium | All outputs written to files |
| P-003 (No Recursion) | **Hard** | Orchestrator → workers only, no nesting |
| P-020 (User Authority) | **Hard** | User controls input/output paths |
| P-022 (No Deception) | **Hard** | Honest reporting of confidence and errors |

### P-003 Compliance Diagram

```
Claude Code (Main Context)
    │
    └──► Transcript Skill (SKILL.md)
            │
            ├──► ts-parser (WORKER)      ✓ No subagents
            ├──► ts-extractor (WORKER)   ✓ No subagents
            ├──► ts-formatter (WORKER)   ✓ No subagents
            └──► ps-critic (WORKER)      ✓ No subagents

COMPLIANT: Exactly ONE level of agent nesting
```

---

## Quick Reference

### Common Workflows

| Need | Command | Output |
|------|---------|--------|
| Process VTT | `/transcript meeting.vtt` | Packet directory |
| Analyze SRT | `/transcript subtitles.srt` | Packet with extractions |
| Extract actions | "Find action items in transcript" | 04-action-items.md |
| Get decisions | "What was decided in the meeting?" | 05-decisions.md |

### Quality Thresholds

| Metric | Target | Source |
|--------|--------|--------|
| Extraction precision | > 85% | NFR-003 |
| Extraction recall | > 85% | NFR-003 |
| Confidence threshold | >= 0.7 | NFR-008 |
| Quality score | >= 0.90 | DEC-001-006 |

---

## Related Documents

### Backlinks
- [TDD-transcript-skill.md](../../projects/PROJ-008-transcript-skill/work/EPIC-001-transcript-skill/FEAT-001-analysis-design/EN-005-design-documentation/docs/TDD-transcript-skill.md) - Architecture overview
- [ADR-001](../../projects/PROJ-008-transcript-skill/work/EPIC-001-transcript-skill/FEAT-001-analysis-design/EN-004-architecture-decisions/docs/adrs/adr-001.md) - Agent Architecture
- [ADR-002](../../projects/PROJ-008-transcript-skill/work/EPIC-001-transcript-skill/FEAT-001-analysis-design/EN-004-architecture-decisions/docs/adrs/adr-002.md) - Artifact Structure

### Forward Links
- [PLAYBOOK.md](./docs/PLAYBOOK.md) - Execution playbook
- [RUNBOOK.md](./docs/RUNBOOK.md) - Operational procedures

---

## Agent Details

For detailed agent specifications, see:

- `agents/ts-parser.md` - Parser agent definition
- `agents/ts-extractor.md` - Extractor agent definition
- `agents/ts-formatter.md` - Formatter agent definition
- `skills/problem-solving/agents/ps-critic.md` - Critic agent (shared)

---

*Skill Version: 1.0.0*
*Constitutional Compliance: Jerry Constitution v1.0*
*Created: 2026-01-26*
*Relocated: 2026-01-26 per DISC-004*
