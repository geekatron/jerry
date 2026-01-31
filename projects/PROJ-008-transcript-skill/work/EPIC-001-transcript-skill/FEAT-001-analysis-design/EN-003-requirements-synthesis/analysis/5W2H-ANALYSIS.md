# 5W2H Analysis: Transcript Skill Requirements Scope Definition

> **Project**: PROJ-008-transcript-skill
> **Entry ID**: e-003
> **Analysis Type**: 5W2H Framework Analysis
> **Topic**: Transcript Skill Requirements Scope Definition
> **Date**: 2026-01-25
> **Author**: ps-analyst (Problem-Solving Analyst Agent)

---

## L0: Executive Summary (ELI5)

**What is this?**
We're building a smart tool that reads meeting transcripts (those text files you get after Zoom/Teams calls) and automatically finds the important stuff: who said what, what tasks were assigned, what decisions were made, and what questions were asked.

**Why does it matter?**
Right now, if you have a transcript file from a meeting, you have to read through the whole thing to find the action items. That takes forever! Existing tools either don't work with transcript files at all, or they cost hundreds of dollars per month. We're building something that works locally, costs nothing, and respects your privacy.

**How does it work?**
Think of it like a very smart highlighter. The tool reads your transcript file, understands who's talking, and uses AI to spot important things like "John will send the report by Friday" (action item) or "We decided to use React for the frontend" (decision). Then it gives you a nice summary.

**Bottom Line**: A free, privacy-respecting tool that turns messy meeting transcripts into organized, actionable summaries in seconds.

---

## L1: Technical Analysis (Software Engineer Perspective)

### 1. WHAT: Core Functionality Definition

#### 1.1 Primary Capabilities

| Capability | Description | Priority |
|------------|-------------|----------|
| **VTT/SRT Parsing** | Parse WebVTT and SRT transcript formats with full spec compliance | P0 (Critical) |
| **Speaker Identification** | Extract and normalize speaker labels from various formats | P0 (Critical) |
| **Action Item Detection** | Identify commitments, tasks, and follow-ups | P0 (Critical) |
| **Decision Extraction** | Locate explicit decisions and conclusions | P1 (High) |
| **Question Detection** | Find questions (answered and unanswered) | P1 (High) |
| **Topic Segmentation** | Identify topic shifts and meeting structure | P2 (Medium) |
| **Summary Generation** | Produce meeting summaries at multiple granularities | P2 (Medium) |

#### 1.2 Input Format Support

```
┌─────────────────────────────────────────────────────────────────┐
│                     INPUT FORMAT MATRIX                         │
├─────────────────┬───────────────┬───────────────┬──────────────┤
│ Format          │ Specification │ Parser        │ MVP Priority │
├─────────────────┼───────────────┼───────────────┼──────────────┤
│ WebVTT (.vtt)   │ W3C Standard  │ webvtt-py     │ P0           │
│ SRT (.srt)      │ De facto std  │ srt (lib)     │ P0           │
│ Plain Text      │ Various       │ Custom regex  │ P1           │
│ JSON Transcript │ Custom schema │ json stdlib   │ P2           │
└─────────────────┴───────────────┴───────────────┴──────────────┘
```

#### 1.3 Entity Types to Extract

**Standard NER Entities:**
- `PERSON` - People mentioned in the transcript
- `ORG` - Organizations, companies, teams
- `DATE` - Dates, times, deadlines
- `MONEY` - Budget amounts, costs
- `PRODUCT` - Product names, software tools

**Custom Domain Entities:**
- `ACTION_ITEM` - Tasks, commitments, follow-ups
- `DECISION` - Explicit decisions made
- `QUESTION` - Questions asked (with answered/unanswered status)
- `TOPIC` - Discussion topics and segments
- `BLOCKER` - Identified impediments or blockers

#### 1.4 Output Formats

```
┌─────────────────────────────────────────────────────────────────┐
│                     OUTPUT FORMAT OPTIONS                       │
├─────────────────┬───────────────────────────────────────────────┤
│ Format          │ Use Case                                      │
├─────────────────┼───────────────────────────────────────────────┤
│ Markdown        │ Human-readable summaries, documentation       │
│ JSON            │ Programmatic consumption, pipeline integration│
│ YAML            │ Configuration-friendly, agent memory          │
│ Plain Text      │ Simple CLI output, piping                     │
└─────────────────┴───────────────────────────────────────────────┘
```

### 2. WHY: Market Gap and Value Proposition

#### 2.1 Competitive Landscape Analysis

Based on EN-001 Market Analysis research:

| Tool | VTT Import | SRT Import | Local Processing | Free Tier | Privacy |
|------|------------|------------|------------------|-----------|---------|
| Otter.ai | No | No | No | Limited | Cloud |
| Fireflies.ai | No | No | No | Limited | Cloud |
| tl;dv | No | No | No | Limited | Cloud |
| Grain | No | No | No | Limited | Cloud |
| Pocket | No | No | No | Limited | Cloud |
| **Our Tool** | **Yes** | **Yes** | **Yes** | **Full** | **Local** |

#### 2.2 Identified Market Gaps

1. **Format Gap**: No existing tool accepts VTT/SRT files as input
2. **Privacy Gap**: All competitors require cloud upload of sensitive meeting data
3. **Cost Gap**: AI-powered features locked behind $20-150+/month subscriptions
4. **Integration Gap**: Existing tools don't integrate with developer workflows (CLI, CI/CD)
5. **Flexibility Gap**: No customization of extraction rules or output formats

#### 2.3 User Pain Points (from POCKET-analysis.md)

```
┌─────────────────────────────────────────────────────────────────┐
│                    USER PAIN POINT HIERARCHY                    │
├─────────────────────────────────────────────────────────────────┤
│ P1. "I have transcript files but no way to analyze them"        │
│ P2. "I don't want to upload sensitive meetings to cloud"        │
│ P3. "Existing tools are too expensive for occasional use"       │
│ P4. "I need to extract action items but manual review takes hrs"│
│ P5. "I want to integrate transcript analysis into my workflow"  │
└─────────────────────────────────────────────────────────────────┘
```

### 3. WHERE: Deployment Context

#### 3.1 Execution Environments

```
┌─────────────────────────────────────────────────────────────────┐
│                   DEPLOYMENT TOPOLOGY                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐      │
│  │   Local CLI  │    │   CI/CD      │    │   Claude     │      │
│  │   Terminal   │    │   Pipeline   │    │   Code       │      │
│  └──────┬───────┘    └──────┬───────┘    └──────┬───────┘      │
│         │                   │                   │               │
│         └───────────────────┴───────────────────┘               │
│                             │                                   │
│                    ┌────────┴────────┐                         │
│                    │ Transcript Skill │                         │
│                    │  (Python Core)   │                         │
│                    └────────┬────────┘                         │
│                             │                                   │
│              ┌──────────────┴──────────────┐                   │
│              │       Local Filesystem       │                   │
│              │  (Transcripts, Outputs)      │                   │
│              └─────────────────────────────┘                   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

#### 3.2 Integration Points

| Integration | Method | Priority |
|-------------|--------|----------|
| Claude Code Skill | SKILL.md + Python CLI | P0 |
| Terminal/Shell | Standalone CLI binary | P0 |
| CI/CD Pipelines | Exit codes, JSON output | P1 |
| Jerry Framework | Work Tracker integration | P1 |
| VS Code | Extension (future) | P3 |

### 4. WHEN: Usage Triggers and Timing

#### 4.1 Primary Use Cases

```
┌─────────────────────────────────────────────────────────────────┐
│                    USAGE TRIGGER MATRIX                         │
├──────────────────────┬──────────────────────────────────────────┤
│ Trigger              │ Expected Workflow                        │
├──────────────────────┼──────────────────────────────────────────┤
│ Post-meeting         │ User downloads transcript from Zoom/     │
│                      │ Teams, runs skill to extract action items│
├──────────────────────┼──────────────────────────────────────────┤
│ Batch processing     │ Process multiple archived transcripts    │
│                      │ for retrospective analysis               │
├──────────────────────┼──────────────────────────────────────────┤
│ Pipeline integration │ Automated extraction as part of CI/CD    │
│                      │ or documentation workflow                │
├──────────────────────┼──────────────────────────────────────────┤
│ Research/Analysis    │ Analyze meeting patterns, extract        │
│                      │ decisions for ADR documentation          │
└──────────────────────┴──────────────────────────────────────────┘
```

#### 4.2 Timing Considerations

- **Latency Target**: < 5 seconds for typical transcript (< 1 hour meeting)
- **Throughput**: Support batch processing of 100+ files
- **Async Support**: Non-blocking for large file processing

### 5. WHO: User Personas

#### 5.1 Primary Personas

```
┌─────────────────────────────────────────────────────────────────┐
│                     PERSONA: Developer Dan                      │
├─────────────────────────────────────────────────────────────────┤
│ Role: Software Engineer                                         │
│ Context: Attends 5-10 meetings/week, uses CLI daily             │
│ Pain: Loses track of action items from sprint planning          │
│ Need: Quick extraction of tasks assigned to him                 │
│ Skill: High (comfortable with CLI, JSON, scripting)             │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                     PERSONA: Manager Maria                      │
├─────────────────────────────────────────────────────────────────┤
│ Role: Engineering Manager                                       │
│ Context: Runs daily standups, weekly 1:1s, retrospectives       │
│ Pain: Manual note-taking during meetings is distracting         │
│ Need: Automated meeting summaries with decisions highlighted    │
│ Skill: Medium (uses terminal occasionally)                      │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                     PERSONA: Analyst Alex                       │
├─────────────────────────────────────────────────────────────────┤
│ Role: Business Analyst / Product Manager                        │
│ Context: Reviews stakeholder meetings, creates requirements     │
│ Pain: Transcript files from vendors/clients sit unprocessed     │
│ Need: Extract requirements, decisions, questions from transcripts│
│ Skill: Low-Medium (prefers simple commands)                     │
└─────────────────────────────────────────────────────────────────┘
```

#### 5.2 Secondary Personas

- **Claude Code Users**: Developers using Claude Code who want skill-based transcript analysis
- **Documentation Writers**: Technical writers extracting meeting content for docs
- **Researchers**: Analyzing meeting patterns and communication dynamics

### 6. HOW: Technical Approach

#### 6.1 Architecture Overview

Based on NLP-NER-BEST-PRACTICES.md and ACADEMIC-LITERATURE-REVIEW.md:

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    PROCESSING PIPELINE ARCHITECTURE                     │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  INPUT                STAGE 1              STAGE 2              STAGE 3 │
│  ─────                ───────              ───────              ─────── │
│                                                                         │
│  ┌─────────┐    ┌──────────────┐    ┌──────────────┐    ┌────────────┐ │
│  │  VTT/   │───►│  Structural  │───►│  Standard    │───►│  Domain    │ │
│  │  SRT    │    │  Extraction  │    │  NER         │    │  Extraction│ │
│  │  File   │    │              │    │              │    │            │ │
│  └─────────┘    └──────────────┘    └──────────────┘    └────────────┘ │
│                        │                   │                   │        │
│                        ▼                   ▼                   ▼        │
│                 ┌────────────┐      ┌────────────┐      ┌────────────┐ │
│                 │• Parse VTT │      │• PERSON    │      │• ACTION    │ │
│                 │• Parse SRT │      │• ORG       │      │• DECISION  │ │
│                 │• Extract   │      │• DATE      │      │• QUESTION  │ │
│                 │  Speakers  │      │• MONEY     │      │• TOPIC     │ │
│                 │• Chunk     │      │• PRODUCT   │      │• BLOCKER   │ │
│                 │  Segments  │      │            │      │            │ │
│                 └────────────┘      └────────────┘      └────────────┘ │
│                                                                         │
│                                    STAGE 4                              │
│                                    ───────                              │
│                                                                         │
│                              ┌──────────────┐    ┌──────────────┐      │
│                              │  Enrichment  │───►│   Output     │      │
│                              │              │    │   Generation │      │
│                              └──────────────┘    └──────────────┘      │
│                                     │                   │               │
│                                     ▼                   ▼               │
│                              ┌────────────┐      ┌────────────┐        │
│                              │• Topic     │      │• Markdown  │        │
│                              │  Modeling  │      │• JSON      │        │
│                              │• Sentiment │      │• YAML      │        │
│                              │• Summary   │      │• Text      │        │
│                              └────────────┘      └────────────┘        │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

#### 6.2 Technology Stack

**MVP Stack (Rule-Based + Lightweight ML):**

| Layer | Technology | Rationale |
|-------|------------|-----------|
| **Parsing** | `srt` library, `webvtt-py` | Lightweight, well-tested, zero dependencies |
| **NER** | spaCy `en_core_web_sm` | Fast, accurate, offline-capable |
| **Pattern Matching** | spaCy EntityRuler | Customizable domain patterns |
| **Topic Modeling** | BERTopic (optional) | State-of-art for short texts |
| **CLI** | `click` or `typer` | Modern CLI UX, follows best practices |

**Production Stack (Enhanced Accuracy):**

| Layer | Technology | Rationale |
|-------|------------|-----------|
| **NER** | HuggingFace Transformers | Fine-tuned models for meetings |
| **Action Items** | Fine-tuned classifier | F1 = 0.94 achievable per literature |
| **Summarization** | LLM (Claude/GPT) | High-quality abstractive summaries |
| **Quality** | Hallucination detection | Per academic benchmarks |

#### 6.3 Speaker Identification Patterns

From NLP-NER-BEST-PRACTICES.md:

```python
# VTT Voice Tag Pattern
VTT_VOICE_PATTERN = r'<v\s+([^>]+)>([^<]*)</v>'
# Matches: <v John Smith>Hello everyone</v>

# Prefix Pattern (common in transcripts)
PREFIX_PATTERN = r'^([A-Z][a-zA-Z\s\.]+):\s*(.+)'
# Matches: John Smith: Hello everyone

# Bracket Pattern
BRACKET_PATTERN = r'^\[([^\]]+)\]\s*(.+)'
# Matches: [John Smith] Hello everyone

# All Caps Pattern
ALLCAPS_PATTERN = r'^([A-Z][A-Z\s]+):\s*(.+)'
# Matches: JOHN SMITH: Hello everyone
```

#### 6.4 CLI Design Principles

Based on CLI best practices research (clig.dev, Heroku Style Guide):

```
┌─────────────────────────────────────────────────────────────────┐
│                    CLI DESIGN PRINCIPLES                        │
├─────────────────────────────────────────────────────────────────┤
│ 1. Human-First: Readable output by default, machine output opt-in│
│ 2. Conventions: Follow POSIX, support --help, -v/--verbose      │
│ 3. Progress: Show progress for long operations                  │
│ 4. Errors: Actionable messages with suggestions                 │
│ 5. Composable: Support stdin/stdout piping                      │
│ 6. Exit Codes: 0 = success, 1 = error, 2 = invalid usage        │
│ 7. Colors: Use sparingly, respect NO_COLOR env var              │
│ 8. Config: Support config files, env vars, CLI args (in order)  │
└─────────────────────────────────────────────────────────────────┘
```

**Proposed CLI Interface:**

```bash
# Basic usage
transcript analyze meeting.vtt

# Specify output format
transcript analyze meeting.vtt --format json

# Extract specific entities
transcript analyze meeting.vtt --entities action-items,decisions

# Batch processing
transcript analyze ./transcripts/*.vtt --output ./summaries/

# Pipeline integration
cat meeting.vtt | transcript analyze --format json | jq '.action_items'
```

### 7. HOW MUCH: Scope and Complexity

#### 7.1 MVP Scope Definition

```
┌─────────────────────────────────────────────────────────────────┐
│                      MVP SCOPE (v0.1.0)                         │
├─────────────────────────────────────────────────────────────────┤
│ INPUT FORMATS:                                                  │
│   ✓ VTT (WebVTT)                                               │
│   ✓ SRT (SubRip)                                               │
│   ✓ Plain text (simple speaker: text format)                   │
│                                                                 │
│ ENTITY EXTRACTION:                                              │
│   ✓ Speakers (identification and normalization)                │
│   ✓ Action Items (with assignee and deadline when present)     │
│   ✓ Decisions (explicit decisions)                             │
│   ✓ Questions (flagged as answered/unanswered)                 │
│   ✓ Standard NER (PERSON, ORG, DATE)                           │
│                                                                 │
│ OUTPUT FORMATS:                                                 │
│   ✓ Markdown (default)                                         │
│   ✓ JSON (for programmatic use)                                │
│   ✓ Plain text                                                 │
│                                                                 │
│ CLI FEATURES:                                                   │
│   ✓ Single file processing                                     │
│   ✓ Basic filtering (--entities flag)                          │
│   ✓ Output format selection                                    │
│   ✓ Help and version commands                                  │
│                                                                 │
│ OUT OF SCOPE FOR MVP:                                           │
│   ✗ Topic modeling                                             │
│   ✗ Sentiment analysis                                         │
│   ✗ LLM-based summarization                                    │
│   ✗ Batch processing                                           │
│   ✗ Custom entity rules (config file)                          │
│   ✗ Real-time processing                                       │
└─────────────────────────────────────────────────────────────────┘
```

#### 7.2 Complexity Assessment

| Component | Complexity | Effort Estimate | Risk |
|-----------|------------|-----------------|------|
| VTT Parser | Low | 1-2 days | Low (well-documented spec) |
| SRT Parser | Low | 1 day | Low (use existing library) |
| Speaker Extraction | Medium | 2-3 days | Medium (format variations) |
| Action Item Detection | High | 3-5 days | High (NLP accuracy) |
| Decision Extraction | Medium | 2-3 days | Medium (pattern complexity) |
| Question Detection | Low | 1-2 days | Low (linguistic patterns) |
| CLI Interface | Medium | 2-3 days | Low (established patterns) |
| Output Formatting | Low | 1-2 days | Low |
| Testing & Documentation | Medium | 3-4 days | Low |

**Total MVP Estimate**: 15-25 developer days

#### 7.3 Performance Targets

| Metric | Target | Measurement |
|--------|--------|-------------|
| Parse Time (1hr transcript) | < 1 second | Benchmark test |
| Entity Extraction (1hr) | < 5 seconds | Benchmark test |
| Memory Usage | < 500 MB | Peak memory |
| Action Item F1 | > 0.80 | Test dataset |
| Decision F1 | > 0.75 | Test dataset |

#### 7.4 Risk Matrix

```
┌─────────────────────────────────────────────────────────────────┐
│                        RISK MATRIX                              │
├────────────────────────┬───────────┬───────────┬───────────────┤
│ Risk                   │ Likelihood│ Impact    │ Mitigation    │
├────────────────────────┼───────────┼───────────┼───────────────┤
│ NLP accuracy too low   │ Medium    │ High      │ Rule fallback │
│ Format variations      │ High      │ Medium    │ Robust parsing│
│ Performance issues     │ Low       │ Medium    │ Caching       │
│ Dependency conflicts   │ Low       │ High      │ Minimal deps  │
│ Scope creep            │ High      │ High      │ Strict MVP    │
└────────────────────────┴───────────┴───────────┴───────────────┘
```

---

## L2: Architectural Perspective (Principal Architect)

### Architecture Decision Drivers

#### 1. Key Quality Attributes

| Attribute | Priority | Rationale |
|-----------|----------|-----------|
| **Accuracy** | Critical | Core value proposition depends on extraction quality |
| **Privacy** | Critical | Local processing is a key differentiator |
| **Extensibility** | High | Custom entities, new formats, plugin architecture |
| **Performance** | High | Developer experience depends on fast feedback |
| **Maintainability** | High | Long-term viability, community contributions |
| **Portability** | Medium | Cross-platform support (macOS, Linux, Windows) |

#### 2. Architectural Trade-offs

```
┌─────────────────────────────────────────────────────────────────┐
│                   TRADE-OFF ANALYSIS                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ACCURACY ◄────────────────────────────────► PERFORMANCE       │
│     │                                               │           │
│     │  Decision: Tiered approach                    │           │
│     │  - MVP: Fast rule-based + small models        │           │
│     │  - Pro: Optional LLM integration              │           │
│     │                                               │           │
│  SIMPLICITY ◄──────────────────────────────► EXTENSIBILITY     │
│     │                                               │           │
│     │  Decision: Plugin architecture                │           │
│     │  - Core: Simple, focused functionality        │           │
│     │  - Extensions: Custom extractors via plugins  │           │
│     │                                               │           │
│  LOCAL ◄───────────────────────────────────► CLOUD FEATURES    │
│     │                                               │           │
│     │  Decision: Local-first with opt-in cloud      │           │
│     │  - Default: 100% local processing             │           │
│     │  - Optional: LLM calls for enhanced features  │           │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

#### 3. Hexagonal Architecture Application

```
┌─────────────────────────────────────────────────────────────────┐
│                 HEXAGONAL ARCHITECTURE MAPPING                  │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│                    ┌─────────────────┐                         │
│                    │   CLI Adapter   │ ◄── Primary Adapter     │
│                    │   (typer/click) │                         │
│                    └────────┬────────┘                         │
│                             │                                   │
│                    ┌────────┴────────┐                         │
│                    │   Application   │ ◄── Use Cases           │
│                    │   Commands      │                         │
│                    │   & Queries     │                         │
│                    └────────┬────────┘                         │
│                             │                                   │
│         ┌───────────────────┼───────────────────┐              │
│         │                   │                   │              │
│  ┌──────┴──────┐    ┌──────┴──────┐    ┌──────┴──────┐       │
│  │   Domain    │    │   Domain    │    │   Domain    │       │
│  │  Transcript │    │   Entity    │    │   Output    │       │
│  │   Parsing   │    │  Extraction │    │  Formatting │       │
│  └──────┬──────┘    └──────┬──────┘    └──────┬──────┘       │
│         │                   │                   │              │
│  ┌──────┴──────┐    ┌──────┴──────┐    ┌──────┴──────┐       │
│  │ VTT Adapter │    │spaCy Adapter│    │   JSON      │       │
│  │ SRT Adapter │    │HF Adapter   │    │   Markdown  │       │
│  │ Text Adapter│    │Rule Adapter │    │   Adapter   │       │
│  └─────────────┘    └─────────────┘    └─────────────┘       │
│        ▲                   ▲                   ▲              │
│        │                   │                   │              │
│        └───────────────────┴───────────────────┘              │
│                    Secondary Adapters                          │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

#### 4. Domain Model (Core Entities)

```python
# Domain Value Objects
@dataclass(frozen=True)
class TranscriptSegment:
    """Immutable segment from transcript."""
    start_time: timedelta
    end_time: timedelta
    speaker: str | None
    text: str

@dataclass(frozen=True)
class ExtractedEntity:
    """Immutable extracted entity."""
    entity_type: EntityType
    text: str
    confidence: float
    source_segment: TranscriptSegment
    metadata: dict[str, Any]

# Domain Aggregate
class Transcript:
    """Aggregate root for transcript processing."""
    segments: list[TranscriptSegment]
    entities: list[ExtractedEntity]
    metadata: TranscriptMetadata

    def extract_entities(self, extractors: list[IEntityExtractor]) -> None:
        """Apply extractors to populate entities."""
        ...
```

#### 5. One-Way Door Decisions

| Decision | Type | Reversibility | Rationale |
|----------|------|---------------|-----------|
| Python as core language | One-way | Low | Ecosystem, spaCy, team skills |
| Local-first architecture | One-way | Low | Core differentiator, privacy |
| Hexagonal architecture | Two-way | High | Clean boundaries, testable |
| spaCy for NER MVP | Two-way | High | Can swap for HF Transformers |
| CLI-first interface | Two-way | Medium | Can add API/GUI later |

#### 6. Performance Implications

**Memory Management:**
- Stream parsing for large files (avoid loading entire transcript)
- Lazy entity extraction (on-demand processing)
- Model caching (load spaCy model once per session)

**CPU Optimization:**
- Batch NER processing (group segments for efficiency)
- Parallel extraction for independent entity types
- Early termination for filtered entity requests

**Latency Budget:**

```
┌─────────────────────────────────────────────────────────────────┐
│              LATENCY BUDGET (1hr transcript, ~10K words)        │
├─────────────────────────────────────────────────────────────────┤
│ Phase                    │ Target    │ Max       │ Strategy    │
├──────────────────────────┼───────────┼───────────┼─────────────┤
│ File I/O + Parsing       │ 50ms      │ 200ms     │ Streaming   │
│ Speaker Extraction       │ 100ms     │ 500ms     │ Regex       │
│ Standard NER             │ 1000ms    │ 2000ms    │ Batching    │
│ Domain Entity Extraction │ 2000ms    │ 3000ms    │ Caching     │
│ Output Generation        │ 50ms      │ 200ms     │ Templates   │
├──────────────────────────┼───────────┼───────────┼─────────────┤
│ TOTAL                    │ 3200ms    │ 5900ms    │             │
└─────────────────────────────────────────────────────────────────┘
```

---

## Evidence Summary

| Dimension | Key Finding | Source | Confidence |
|-----------|-------------|--------|------------|
| **WHAT** | VTT/SRT parsing + 5-7 entity types | EN-002 specs | High |
| **WHY** | No existing tool supports VTT/SRT import | EN-001 FEATURE-MATRIX | High |
| **WHERE** | CLI + Claude Code skill | Requirements | High |
| **WHEN** | Post-meeting processing, batch | User research | Medium |
| **WHO** | Developers, managers, analysts | Persona analysis | Medium |
| **HOW** | 4-stage pipeline, spaCy/rules MVP | NLP-NER-BEST-PRACTICES | High |
| **HOW MUCH** | 15-25 dev days, 3 input formats, 5-7 entities | Estimation | Medium |

---

## References

### Primary Research Sources (EN-001)
| Reference | Type | Key Insight |
|-----------|------|-------------|
| FEATURE-MATRIX.md | Analysis | Competitive feature comparison |
| POCKET-analysis.md | Analysis | User pain points, pricing model |
| OTTER-analysis.md | Analysis | AI features, market position |
| FIREFLIES-analysis.md | Analysis | Integration patterns |
| GRAIN-analysis.md | Analysis | Video-focused features |
| TLDV-analysis.md | Analysis | Meeting recording workflow |

### Technical Standards Sources (EN-002)
| Reference | Type | Key Insight |
|-----------|------|-------------|
| VTT-SPECIFICATION.md | Standard | W3C WebVTT spec compliance |
| SRT-SPECIFICATION.md | Standard | De facto SRT format, Python libraries |
| NLP-NER-BEST-PRACTICES.md | Best Practices | Pipeline architecture, tech stack |
| ACADEMIC-LITERATURE-REVIEW.md | Research | Benchmarks, F1 scores, hallucination rates |

### External References
| Reference | Type | Key Insight |
|-----------|------|-------------|
| [clig.dev](https://clig.dev) | Guide | CLI design principles |
| [Heroku CLI Style Guide](https://devcenter.heroku.com/articles/cli-style-guide) | Guide | CLI UX patterns |
| [W3C WebVTT](https://www.w3.org/TR/webvtt1/) | Specification | Official VTT standard |
| [spaCy Documentation](https://spacy.io/usage) | Documentation | NER implementation |
| [BERTopic](https://maartengr.github.io/BERTopic/) | Documentation | Topic modeling |

### Academic Citations
| Citation | Finding | Relevance |
|----------|---------|-----------|
| ur_BLOOMZ-1b1 fine-tuning | F1 = 0.94 for action items | Accuracy target |
| AMI Corpus | 100 hours meeting data | Training/evaluation |
| QMSum Dataset | 232 meetings | Summarization benchmark |
| GPT-4o Hallucination Study | 1.5% rate | Quality baseline |

---

## Appendix A: Glossary

| Term | Definition |
|------|------------|
| **VTT** | WebVTT (Web Video Text Tracks) - W3C standard for timed text |
| **SRT** | SubRip Text - De facto standard subtitle format |
| **NER** | Named Entity Recognition - ML task to identify entities in text |
| **BERTopic** | Topic modeling technique using BERT embeddings |
| **Action Item** | Task or commitment requiring follow-up |
| **Hexagonal Architecture** | Ports and adapters pattern for clean separation |

---

## Appendix B: Related Work Tracker Items

| ID | Type | Title | Status |
|----|------|-------|--------|
| EN-001 | Enabler | Market Analysis & Competitive Research | Complete |
| EN-002 | Enabler | Technical Standards Research | Complete |
| EN-003 | Enabler | Requirements Synthesis | In Progress |
| EN-004 | Enabler | Requirements Validation | Pending |

---

*Document generated by ps-analyst agent as part of the Problem-Solving framework.*
*Analysis timestamp: 2026-01-25*
