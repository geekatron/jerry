---
name: transcript
description: Parse, extract, and format transcripts (VTT, SRT, plain text) into structured Markdown packets with action items, decisions, questions, and topics. v2.0 uses hybrid Python+LLM architecture for VTT files. Integrates with ps-critic for quality review.
version: "2.2.0"
allowed-tools: Read, Write, Glob, Task, Bash(*)
argument-hint: <file-path> [--output-dir <dir>] [--no-mindmap] [--mindmap-format <mermaid|ascii|both>]

# CONTEXT INJECTION (implements REQ-CI-F-002)
# Enables domain-specific context loading per SPEC-context-injection.md Section 3.1
# Updated: EN-014 TASK-158 - All 9 domains registered
context_injection:
  # Default domain when none specified
  default_domain: "general"

  # Available domain schemas (9 total)
  # See docs/domains/DOMAIN-SELECTION-GUIDE.md for selection flowchart
  domains:
    # Baseline Domains (3)
    - name: "general"
      description: "Baseline extraction - speakers, topics, questions"
      file: "contexts/general.yaml"
      spec: null  # No specialized spec

    - name: "transcript"
      description: "Base transcript entities - extends general"
      file: "contexts/transcript.yaml"
      spec: null  # No specialized spec

    - name: "meeting"
      description: "Generic meetings - action items, decisions, follow-ups"
      file: "contexts/meeting.yaml"
      spec: null  # No specialized spec

    # Professional Domains (6) - From EN-006 Context Injection Design
    - name: "software-engineering"
      description: "Standups, sprint planning, code reviews - commitments, blockers, risks"
      file: "contexts/software-engineering.yaml"
      spec: "docs/domains/SPEC-software-engineering.md"
      target_users: ["Engineers", "Tech Leads", "Scrum Masters"]

    - name: "software-architecture"
      description: "ADR discussions, design sessions - decisions, alternatives, quality attributes"
      file: "contexts/software-architecture.yaml"
      spec: "docs/domains/SPEC-software-architecture.md"
      target_users: ["Architects", "Principal Engineers"]

    - name: "product-management"
      description: "Roadmap planning, feature prioritization - requests, user needs, stakeholder feedback"
      file: "contexts/product-management.yaml"
      spec: "docs/domains/SPEC-product-management.md"
      target_users: ["PMs", "Product Owners", "Business Analysts"]

    - name: "user-experience"
      description: "Research interviews, usability tests - insights, pain points, verbatim quotes"
      file: "contexts/user-experience.yaml"
      spec: "docs/domains/SPEC-user-experience.md"
      target_users: ["UX Researchers", "UX Designers"]
      special_requirements: ["verbatim_quote_preservation"]

    - name: "cloud-engineering"
      description: "Post-mortems, capacity planning - incidents, root causes, action items"
      file: "contexts/cloud-engineering.yaml"
      spec: "docs/domains/SPEC-cloud-engineering.md"
      target_users: ["SREs", "DevOps Engineers", "Platform Engineers"]
      special_requirements: ["blameless_culture"]

    - name: "security-engineering"
      description: "Security audits, threat modeling - vulnerabilities, threats (STRIDE), compliance gaps"
      file: "contexts/security-engineering.yaml"
      spec: "docs/domains/SPEC-security-engineering.md"
      target_users: ["Security Engineers", "AppSec Engineers", "Compliance Officers"]
      special_requirements: ["risk_acceptance_documentation", "stride_support", "cvss_support"]

  # Context files location
  context_path: "./contexts/"

  # Template variables available to agents
  template_variables:
    - name: domain
      source: invocation.domain
      default: "general"
    - name: entity_definitions
      source: context.entity_definitions
      format: yaml
    - name: extraction_rules
      source: context.extraction_rules
      format: list
    - name: prompt_guidance
      source: context.prompt_guidance
      format: text

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

# MANDATORY: CLI Invocation for Parsing (Phase 1)

> **CRITICAL:** For VTT files, you MUST invoke the Python parser via the `jerry` CLI.
> DO NOT use Task agents for parsing. The CLI provides 1,250x cost reduction and deterministic output.

## Phase 1: Parse Transcript (REQUIRED CLI INVOCATION)

**ARGUMENT PARSING RULES:**
1. The FIRST positional argument from user input is the `<file-path>` (the VTT/SRT file)
2. The `--output-dir` flag specifies the output directory (default: `./transcript-output`)
3. **IMPORTANT:** If user provides `--output`, treat it as `--output-dir` (alias)

**For VTT files, Claude MUST execute this bash command:**

```bash
uv run jerry transcript parse "<FILE_PATH>" --output-dir "<OUTPUT_DIR>"
```

Where:
- `<FILE_PATH>` = The ACTUAL file path from the user's invocation (first positional arg)
- `<OUTPUT_DIR>` = The output directory from `--output-dir` or `--output` flag (default: `./transcript-output`)

**Example - user invokes:**
```
/transcript /Users/me/meeting.vtt --output-dir /Users/me/output/
```

**Claude executes:**
```bash
uv run jerry transcript parse "/Users/me/meeting.vtt" --output-dir "/Users/me/output/"
```

**CRITICAL:** Always quote file paths to handle spaces and special characters.

**Expected output:**
- `index.json` - Chunk metadata and speaker summary
- `chunks/chunk-*.json` - Transcript segments in processable chunks
- `canonical-transcript.json` - Full parsed output (for reference only, DO NOT read into context)

## Phase 2+: LLM Agent Orchestration

After Phase 1 CLI parsing completes, continue with LLM agents:
1. **ts-extractor** - Read `index.json` + `chunks/*.json`, produce `extraction-report.json`
2. **ts-formatter** - Read `index.json` + `extraction-report.json`, produce packet files
3. **ts-mindmap-*** - Generate mindmaps (if `--no-mindmap` not set)
4. **ps-critic** - Quality review >= 0.90

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
"/transcript meeting.vtt --domain software-engineering"
```

---

## Domain Selection

The transcript skill supports **9 domain contexts** that customize entity extraction for specific professional contexts. See [DOMAIN-SELECTION-GUIDE.md](./docs/domains/DOMAIN-SELECTION-GUIDE.md) for the complete selection flowchart.

### Available Domains

| Domain | Context File | Use For | Key Entities |
|--------|--------------|---------|--------------|
| `general` | general.yaml | Any transcript (default) | speakers, topics, questions |
| `transcript` | transcript.yaml | Extends general | + segments, timestamps |
| `meeting` | meeting.yaml | Generic meetings | + action_items, decisions, follow_ups |
| `software-engineering` | software-engineering.yaml | Standups, sprint planning | + commitments, blockers, risks |
| `software-architecture` | software-architecture.yaml | ADR discussions, design | + architectural_decisions, alternatives |
| `product-management` | product-management.yaml | Roadmap, prioritization | + feature_requests, user_needs |
| `user-experience` | user-experience.yaml | Research, usability tests | + user_insights, pain_points, verbatim quotes |
| `cloud-engineering` | cloud-engineering.yaml | Post-mortems, capacity | + incidents, root_causes (blameless) |
| `security-engineering` | security-engineering.yaml | Audits, threat modeling | + vulnerabilities, threats (STRIDE), compliance_gaps |

### Specifying a Domain

```
/transcript <file> --domain <domain-name>
```

**Examples:**
```
/transcript standup.vtt --domain software-engineering
/transcript postmortem.vtt --domain cloud-engineering
/transcript user-interview.vtt --domain user-experience
```

If no domain is specified, `general` is used as the default.

---

## Agent Pipeline

```
TRANSCRIPT SKILL PIPELINE (v2.1 HYBRID ARCHITECTURE + MINDMAPS)
===============================================================

                    USER INPUT (VTT/SRT/TXT)
                           │
                           │ /transcript file.vtt [--mindmap-format both]
                           │ /transcript file.vtt --no-mindmap  (to disable)
                           ▼
    ┌───────────────────────────────────────────────────────┐
    │              ts-parser v2.0 (ORCHESTRATOR)            │
    │          Model: haiku (orchestration only)            │
    └───────────────────────┬───────────────────────────────┘
                            │
           ┌────────────────┴────────────────┐
           │ FORMAT DETECTION                │
           ▼                                 ▼
    ┌─────────────┐                   ┌─────────────┐
    │ VTT Format  │                   │ SRT/TXT     │
    │ (Python)    │                   │ (LLM)       │
    └──────┬──────┘                   └──────┬──────┘
           │                                 │
           ▼                                 │
    ┌─────────────┐                          │
    │  Python VTT │  1,250x cost reduction   │
    │   Parser    │  Sub-second parsing      │
    └──────┬──────┘  100% accuracy           │
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
    │          Processes chunks OR monolithic               │
    └───────────────────────┬───────────────────────────────┘
                            │
                            ▼
    ┌───────────────────────────────────────────────────────┐
    │              ts-formatter (sonnet)                    │
    │          Generates 8-file packet per ADR-002          │
    └───────────────────────┬───────────────────────────────┘
                            │
                            │ ts_formatter_output.packet_path
                            ▼
                ┌───────────────────────────┐
                │   --no-mindmap flag set?  │
                └─────────────┬─────────────┘
                              │
           ┌──────────────────┴──────────────────┐
           │ NO (default)                        │ YES
           ▼                                     ▼
    ┌─────────────────────┐              (skip mindmaps)
    │    ts-mindmap-*     │                      │
    │      (sonnet)       │                      │
    │                     │                      │
    │ ┌─────────────────┐ │                      │
    │ │ts-mindmap-mermaid│ │  Output:            │
    │ └─────────────────┘ │  08-mindmap/         │
    │ ┌─────────────────┐ │  mindmap.mmd         │
    │ │ ts-mindmap-ascii│ │  mindmap.ascii.txt   │
    │ └─────────────────┘ │                      │
    └──────────┬──────────┘                      │
               │                                 │
               │ ts_mindmap_output               │
               └──────────────┬──────────────────┘
                              │
                              ▼
    ┌───────────────────────────────────────────────────────┐
    │              ps-critic (sonnet)                       │
    │          Quality validation >= 0.90                   │
    │                                                       │
    │  • Core validation (00-07 files)                      │
    │  • MM-* criteria (if Mermaid mindmap present)         │
    │  • AM-* criteria (if ASCII mindmap present)           │
    └───────────────────────────────────────────────────────┘

COMPLIANCE: Each agent is a WORKER. None spawn subagents.
RATIONALE: DISC-009 - Agent-only architecture caused 99.8% data loss on large files.
MINDMAPS: ADR-006 - Mindmaps ON by default, opt-out via --no-mindmap flag.
```

---

## Available Agents

| Agent | Model | Role | Output |
|-------|-------|------|--------|
| `ts-parser` v2.0 | haiku | **ORCHESTRATOR:** Route VTT→Python, others→LLM. Validate and chunk. | `index.json` + `chunks/*.json` |
| `ts-extractor` | sonnet | Extract speakers, actions, decisions, questions, topics | `extraction-report.json` |
| `ts-formatter` | sonnet | Generate Markdown packet with navigation | `transcript-{id}/` directory |
| `ts-mindmap-mermaid` | sonnet | Generate Mermaid mindmap with deep links (ADR-003) | `08-mindmap/mindmap.mmd` |
| `ts-mindmap-ascii` | sonnet | Generate ASCII art mindmap for terminal display | `08-mindmap/mindmap.ascii.txt` |
| `ps-critic` | sonnet | Validate quality >= 0.90 threshold (includes MM-*/AM-* criteria) | `quality-review.md` |

### Agent Capabilities Summary

**ts-parser v2.0 (Strategy Pattern Orchestrator):**

*Four Roles per TDD-FEAT-004:*
1. **ORCHESTRATOR** - Coordinate pipeline based on format detection
2. **DELEGATOR** - Route VTT to Python parser via Bash tool (1,250x cost reduction)
3. **FALLBACK** - LLM parsing for SRT/TXT formats and error recovery
4. **VALIDATOR** - Verify Python output schema before chunking

*Capabilities:*
- Auto-detect format (VTT header, SRT timestamps, plain text)
- Invoke Python parser for VTT files (deterministic, sub-second)
- Handle encoding detection (UTF-8, Windows-1252, ISO-8859-1)
- Generate chunked output: `index.json` + `chunks/chunk-NNN.json`

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

**ts-mindmap-mermaid (Visualization - Mermaid):**
- Generates Mermaid mindmap syntax from extraction report
- Topic hierarchy with entity grouping
- Deep links to transcript anchors (ADR-003 format)
- Entity symbols: → (action), ? (question), ! (decision), ✓ (follow-up)
- Maximum 50 topics (overflow handling)

**ts-mindmap-ascii (Visualization - ASCII):**
- Generates ASCII art mindmap for terminal display
- UTF-8 box-drawing characters for tree structure
- 80-character line width limit
- Legend at bottom explaining entity symbols
- Terminal-friendly fallback when Mermaid rendering unavailable

**ps-critic (Quality Inspector):**
- Quality score calculation (aggregate >= 0.90)
- Requirements traceability verification
- ADR compliance checking
- Improvement recommendations
- MM-* criteria validation (if Mermaid mindmap present)
- AM-* criteria validation (if ASCII mindmap present)

---

## Invoking the Skill

### Option 1: Slash Command

```
/transcript <file-path> [--output-dir <dir>] [--format <vtt|srt|txt>] [--no-mindmap] [--mindmap-format <format>]
```

**Examples (Default - Mindmaps Generated):**
```
/transcript meeting.vtt                                   # Mindmaps ON by default (both formats)
/transcript standup.srt --output-dir ./docs/meetings/     # With output directory
/transcript notes.txt --format txt                        # Force format detection
```

**Examples (Mindmap Format Selection):**
```
/transcript meeting.vtt --mindmap-format mermaid          # Only Mermaid format
/transcript meeting.vtt --mindmap-format ascii            # Only ASCII format
/transcript meeting.vtt --mindmap-format both             # Both formats (explicit)
```

**Examples (Opt-Out - Disable Mindmaps):**
```
/transcript meeting.vtt --no-mindmap                      # Skip mindmap generation
/transcript meeting.vtt --no-mindmap --output-dir ./docs  # With other options
```

### Option 2: Natural Language

```
"Process the transcript at /path/to/meeting.vtt"
"Extract action items from yesterday's team meeting"
"Analyze the quarterly review transcript and create a summary"
"Process the meeting transcript and generate mindmaps"
"Parse the standup notes without mindmaps"
"Create a Mermaid-only mindmap from the transcript"
```

### Input Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `input_file` | string | Yes | - | Path to transcript file |
| `output_dir` | string | No | `./transcript-output/` | Output directory for packet |
| `format` | string | No | auto-detect | Force format: `vtt`, `srt`, `txt` |
| `confidence_threshold` | float | No | 0.7 | Minimum confidence for extractions |
| `quality_threshold` | float | No | 0.9 | ps-critic quality threshold |
| `--no-mindmap` | flag | No | false | Disable mindmap generation (mindmaps ON by default) |
| `--mindmap-format` | string | No | "both" | Format: `mermaid`, `ascii`, `both` |

---

## Output Structure (ADR-002 + v2.0 Hybrid)

```
transcript-{id}/
├── canonical/                  # v2.0: Hybrid parser output
│   ├── canonical-transcript.json  # Full parsed transcript
│   ├── index.json              # Chunk index with metadata
│   └── chunks/                 # Chunked segments (500 per file)
│       ├── chunk-000.json      # Segments 0-499
│       ├── chunk-001.json      # Segments 500-999
│       └── ...
├── 00-index.md                 # Navigation hub (~2K tokens)
├── 01-summary.md               # Executive summary (~5K tokens)
├── 02-transcript.md            # Full transcript (may split)
├── 03-speakers.md              # Speaker directory
├── 04-action-items.md          # Action items with citations
├── 05-decisions.md             # Decisions with context
├── 06-questions.md             # Open questions
├── 07-topics.md                # Topic segments
├── 08-mindmap/                 # Mindmap directory (default: enabled, per ADR-006)
│   ├── mindmap.mmd             # Mermaid format (if --mindmap-format mermaid or both)
│   └── mindmap.ascii.txt       # ASCII format (if --mindmap-format ascii or both)
└── _anchors.json               # Anchor registry for linking
```

### v2.0 Chunked Structure (index.json)

```json
{
  "total_segments": 3071,
  "chunk_count": 7,
  "chunk_size": 500,
  "target_tokens": 18000,
  "parsing_method": "python",
  "chunks": [
    {
      "file": "chunks/chunk-000.json",
      "start_segment": 0,
      "end_segment": 499,
      "speaker_summary": {"Alice": 120, "Bob": 80}
    }
  ]
}
```

### Chunk Token Budget (v2.1 - EN-026)

| Parameter | Value | Source |
|-----------|-------|--------|
| Claude Code Read limit | 25,000 tokens | GitHub Issue #4002 |
| Target tokens per chunk | 18,000 tokens | 25% safety margin |
| Token counting | tiktoken p50k_base | Best Claude approximation |

**Note:** Prior to v2.1, chunks used segment-based splitting (500 segments per chunk).
v2.1 uses **token-based splitting** to ensure chunks fit within Claude Code's Read tool limits.
This fixes BUG-001 where large transcripts produced chunks exceeding the 25K token limit.

### Token Budget Compliance (ADR-004)

| Limit | Tokens | Action |
|-------|--------|--------|
| Soft | 31,500 | Split at ## heading |
| Hard | 35,000 | Force split |

---

## Agent File Consumption Rules (CRITICAL)

> **MANDATORY:** Agents MUST follow these file consumption rules to prevent context window overflow.
> Violating these rules causes degraded performance and potential failures.

### Files Agents SHOULD Read

| File | Typical Size | Agent | Purpose |
|------|--------------|-------|---------|
| `index.json` | ~8KB | ts-extractor, ts-formatter | Metadata, speaker list, chunk references |
| `chunks/chunk-*.json` | ~130KB each | ts-extractor | Actual transcript data in manageable pieces |
| `extraction-report.json` | ~35KB | ts-formatter, ps-critic | Entity extraction results |
| `packet/*.md` | Variable | ps-critic | Generated Markdown files for quality review |

### Files Agents MUST NEVER Read

| File | Typical Size | Why Forbidden |
|------|--------------|---------------|
| `canonical-transcript.json` | **~930KB** | **TOO LARGE** - will overwhelm context window, cause context rot, degrade agent performance |

### Rationale

The `canonical-transcript.json` file is generated for:
- **Reference/archive purposes** - Human inspection of full parsed output
- **Programmatic access by Python code** - CLI tools that process outside LLM context
- **NOT for LLM agent consumption** - File size exceeds safe context limits

The chunking architecture (DISC-009) was specifically designed to solve the large file problem:
- Each chunk is < 150KB (fits comfortably in context)
- Python parser creates chunks; LLM agents consume chunks
- This prevents the 99.8% data loss experienced with agent-only architecture

### Agent-Specific File Access

| Agent | Reads | Never Reads |
|-------|-------|-------------|
| **ts-parser** | Input VTT/SRT/TXT file | - |
| **ts-extractor** | `index.json`, `chunks/*.json` | `canonical-transcript.json` |
| **ts-formatter** | `index.json`, `extraction-report.json` | `canonical-transcript.json` |
| **ps-critic** | All `packet/*.md` files, `quality-review.md` | `canonical-transcript.json` |

---

## Orchestration Flow

### L1: Step-by-Step Pipeline (v2.0 Hybrid)

```
STEP 1: PARSE + CHUNK (ts-parser v2.0)
──────────────────────────────────────
Input:  Raw transcript file (VTT/SRT/TXT)
Process:
  1. Detect format (VTT header check)
  2. IF VTT:
     - Delegate to Python parser (Bash tool)
     - Validate output schema
     - Chunk to 500-segment files
  3. ELSE (SRT/TXT):
     - Use LLM parsing (fallback)
     - Chunk if large file
Output: index.json + chunks/chunk-NNN.json
Errors: Python failure → fallback to LLM parsing

STEP 2: EXTRACT (ts-extractor)
──────────────────────────────
Input:  index.json + chunks/*.json (NEVER canonical-transcript.json)
Process:
  1. Read index.json for metadata and chunk listing
  2. Process each chunk sequentially for entity extraction
  3. Extract entities with confidence scores and citations
Output: extraction-report.json
Errors: Low confidence extractions → flag for review

STEP 3: FORMAT (ts-formatter)
─────────────────────────────
Input:  index.json + extraction-report.json (NEVER canonical-transcript.json)
Output: packet/ directory (8 files per ADR-002)
Errors: Token overflow → split files automatically (ADR-004)

STEP 3.5: MINDMAP GENERATION (ts-mindmap-*, conditional - ADR-006)
──────────────────────────────────────────────────────────────────
Condition: --no-mindmap flag NOT set (mindmaps ON by default)
Input:  ts_extractor_output.extraction_report_path + ts_formatter_output.packet_path
Process:
  1. IF --no-mindmap flag is NOT set:  # Default behavior
     - IF --mindmap-format == "mermaid" OR "both" (default):
       Invoke ts-mindmap-mermaid
       Output: 08-mindmap/mindmap.mmd
     - IF --mindmap-format == "ascii" OR "both" (default):
       Invoke ts-mindmap-ascii
       Output: 08-mindmap/mindmap.ascii.txt
  2. ELSE:
     - Skip mindmap generation (user opted out)
     - ts_mindmap_output.overall_status = "skipped"
Output: ts_mindmap_output state key
Errors: Graceful degradation - continue with warning, provide regeneration instructions

STEP 4: REVIEW (ps-critic)
──────────────────────────
Input:  All generated files
Output: quality-review.md
Errors: Score < 0.90 → report issues for human review
```

### L2: State Passing Between Agents (v2.0)

| Agent | Output Key | Passed To |
|-------|------------|-----------|
| ts-parser v2.0 | `ts_parser_output` | ts-extractor |
| ts-extractor | `ts_extractor_output` | ts-formatter |
| ts-formatter | `ts_formatter_output` | ts-mindmap-* (if enabled), ps-critic |
| ts-mindmap-* | `ts_mindmap_output` | ps-critic |
| ps-critic | `quality_output` | User/Orchestrator |

**State Schema (v2.0):**
```yaml
ts_parser_output:
  # v2.0 chunked output structure
  canonical_json_path: string
  index_json_path: string           # NEW: Chunk index
  chunks_dir: string                # NEW: chunks/ directory
  chunk_count: integer              # NEW: Number of chunks
  format_detected: vtt|srt|plain
  parsing_method: python|llm        # NEW: Which parser was used
  segment_count: integer
  speaker_count: integer
  validation_passed: boolean        # NEW: Output validation status

ts_extractor_output:
  extraction_report_path: string
  action_count: integer
  decision_count: integer
  question_count: integer
  high_confidence_ratio: float
  chunks_processed: integer         # NEW: For chunked input

ts_formatter_output:
  packet_path: string
  files_created: string[]
  total_tokens: integer
  split_files: integer

ts_mindmap_output:                      # NEW: ADR-006 Section 5.2
  enabled: boolean                      # Was --no-mindmap NOT set?
  format_requested: string              # "mermaid" | "ascii" | "both"
  mermaid:
    path: string | null                 # Path to 08-mindmap/mindmap.mmd
    status: string                      # "complete" | "failed" | "skipped"
    error_message: string | null
    topic_count: integer
    deep_link_count: integer
  ascii:
    path: string | null                 # Path to 08-mindmap/mindmap.ascii.txt
    status: string                      # "complete" | "failed" | "skipped"
    error_message: string | null
    topic_count: integer
    max_line_width: integer             # Should be <= 80
  overall_status: string                # "complete" | "partial" | "failed"

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
- [TDD-FEAT-004](../../projects/PROJ-008-transcript-skill/work/EPIC-001-transcript-skill/FEAT-004-hybrid-infrastructure/docs/design/TDD-FEAT-004-hybrid-infrastructure.md) - Hybrid Infrastructure Technical Design (v2.0 basis)
- [ADR-001](../../projects/PROJ-008-transcript-skill/work/EPIC-001-transcript-skill/FEAT-001-analysis-design/EN-004-architecture-decisions/docs/adrs/adr-001.md) - Agent Architecture
- [ADR-002](../../projects/PROJ-008-transcript-skill/work/EPIC-001-transcript-skill/FEAT-001-analysis-design/EN-004-architecture-decisions/docs/adrs/adr-002.md) - Artifact Structure
- [ADR-006](../../docs/adrs/ADR-006-mindmap-pipeline-integration.md) - Mindmap Pipeline Integration (v2.1 basis)
- [DISC-009](../../projects/PROJ-008-transcript-skill/work/EPIC-001-transcript-skill/FEAT-002-implementation/EN-019-live-skill-invocation/DISC-009-agent-only-architecture-limitation.md) - Agent-Only Architecture Limitation (v2.0 rationale)
- [EN-025](../../projects/PROJ-008-transcript-skill/work/EPIC-001-transcript-skill/FEAT-004-hybrid-infrastructure/EN-025-skill-integration/EN-025-skill-integration.md) - v2.0 Integration Enabler

### Forward Links
- [PLAYBOOK.md](./docs/PLAYBOOK.md) - Execution playbook
- [RUNBOOK.md](./docs/RUNBOOK.md) - Operational procedures
- [VTT Parser](./src/parser/vtt_parser.py) - Python VTT parser (v2.0)
- [Transcript Chunker](./src/chunker/transcript_chunker.py) - Python chunker (v2.0)

---

## Agent Details

For detailed agent specifications, see:

- `agents/ts-parser.md` - Parser/Orchestrator agent definition (v2.0)
- `agents/ts-extractor.md` - Extractor agent definition
- `agents/ts-formatter.md` - Formatter agent definition
- `agents/ts-mindmap-mermaid.md` - Mermaid mindmap agent definition (ADR-006)
- `agents/ts-mindmap-ascii.md` - ASCII mindmap agent definition (ADR-006)
- `skills/problem-solving/agents/ps-critic.md` - Critic agent (shared)

---

*Skill Version: 2.2.0*
*Architecture: Hybrid Python+LLM (Strategy Pattern) + Mindmap Generation*
*Constitutional Compliance: Jerry Constitution v1.0*
*Created: 2026-01-26*
*v2.0: 2026-01-30 per DISC-009 findings (99.8% data loss resolution)*
*v2.1: 2026-01-30 per ADR-006 (Mindmap Pipeline Integration - default ON, opt-out via --no-mindmap)*
*v2.2: 2026-01-29 - Added explicit CLI invocation instructions for Phase 1 parsing (fixes EN-024 verification gap)*
