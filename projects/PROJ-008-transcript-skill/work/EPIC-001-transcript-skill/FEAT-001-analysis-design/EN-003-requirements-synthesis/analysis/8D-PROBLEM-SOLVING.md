# 8D Problem Solving Analysis: Transcript Skill Requirements

> **Document ID**: PROJ-008-e-003-8D-ANALYSIS
> **Date**: 2026-01-25
> **Author**: ps-analyst (Claude)
> **Analysis Type**: 8D (Eight Disciplines) Problem Solving
> **Topic**: Systematic Problem Definition for Text-First Transcript Processing

---

## Document Navigation

| Level | Audience | Section |
|-------|----------|---------|
| L0 | Executive / ELI5 | [Executive Summary](#l0-executive-summary-eli5) |
| L1 | Software Engineer | [Technical Analysis (D0-D8)](#l1-technical-analysis-software-engineer) |
| L2 | Principal Architect | [Architectural Perspective](#l2-architectural-perspective-principal-architect) |

---

## L0: Executive Summary (ELI5)

### The Story in Simple Terms

Imagine you're in a meeting and someone takes notes. After the meeting, you want to find all the things people promised to do (action items), important decisions made, and questions that were asked. Today, most tools require you to **record** the meeting first, then they process the recording.

But what if you already have the meeting transcript as a text file? Maybe:
- Someone transcribed it manually
- You got it from a different service
- You're working with old meeting notes
- Your company doesn't allow recording

**The Problem**: No tool today lets you simply upload a text transcript file (like `.vtt` or `.srt` files) and extract useful information from it. Everyone forces you to use their recording feature.

**Our Solution**: Build a "Transcript Skill" that:
1. **Accepts** any VTT or SRT text file (standard caption formats)
2. **Extracts** useful information: speakers, action items, decisions, questions, topics
3. **Presents** the information in a structured, searchable way

### Why This Matters

```
Current Market Reality:
┌─────────────────────────────────────────────────────────────┐
│  Recording App → Transcription → Analysis → Insights        │
│  (YOU MUST USE THEIR RECORDER)                              │
└─────────────────────────────────────────────────────────────┘

Our Approach:
┌─────────────────────────────────────────────────────────────┐
│  ANY Transcript File → Analysis → Insights                  │
│  (BRING YOUR OWN TEXT)                                      │
└─────────────────────────────────────────────────────────────┘
```

### Key Findings

| Finding | Implication |
|---------|-------------|
| **0 competitors** support VTT/SRT import | We have a unique market opportunity |
| **VTT & SRT** are universal formats | Wide compatibility with existing content |
| **NLP libraries** are mature | Technical feasibility is high |
| **Academic research** provides benchmarks | We can measure quality objectively |

### Root Cause (Simple)

Why doesn't this exist? Because companies make money from:
1. Selling recording/storage services
2. Locking users into their ecosystem
3. Charging per-minute of processed audio

A text-first approach doesn't fit their business model.

---

## L1: Technical Analysis (Software Engineer)

### D0: Plan and Prepare

#### Problem Statement Draft

**Initial Problem Hypothesis**: The market lacks a solution for processing existing transcript files (VTT/SRT format) to extract structured meeting intelligence without requiring live recording or proprietary integrations.

#### Emergency Response Assessment

| Question | Assessment |
|----------|------------|
| Is this a safety issue? | No |
| Is immediate containment needed? | No - this is a new capability, not a defect |
| Are customers affected now? | No direct harm - opportunity cost only |

**Conclusion**: Full 8D methodology appropriate; no emergency containment required.

#### Team Assembly Requirements

| Role | Skills Required | Justification |
|------|-----------------|---------------|
| NLP Engineer | spaCy, HuggingFace, entity extraction | Core extraction pipeline |
| Backend Developer | Python, hexagonal architecture | Service implementation |
| Domain Expert | Meeting workflows, enterprise context | Validation of entity types |
| QA Engineer | Test automation, benchmark evaluation | Quality gate enforcement |

#### Resource Allocation

```
Phase 1 (Analysis & Design):  2-3 weeks
Phase 2 (Core Implementation): 4-6 weeks
Phase 3 (Testing & Validation): 2-3 weeks
Total Estimated Effort: 8-12 weeks
```

---

### D1: Form the Team

#### Cross-Functional Team Composition

| Team Member | Role | Responsibility |
|-------------|------|----------------|
| ps-analyst | Problem Analysis | 8D methodology, requirements synthesis |
| ps-researcher | Technical Research | Technology evaluation, benchmarking |
| ps-architect | System Design | Architecture decisions, pattern selection |
| ps-synthesizer | Integration | Combining findings into actionable specs |
| ps-qa | Quality Assurance | Validation criteria, test planning |

#### Team Charter

**Mission**: Define and solve the "text-first transcript processing gap" through systematic analysis, resulting in clear requirements for the Transcript Skill implementation.

**Success Criteria**:
1. Clear problem definition with measurable scope
2. Root cause analysis with evidence-based findings
3. Corrective action plan aligned with technical capabilities
4. Verification criteria traceable to market research

#### Communication Protocols

| Artifact | Update Frequency | Owner |
|----------|------------------|-------|
| 8D Analysis Document | Per discipline completion | ps-analyst |
| WORKTRACKER.md | Daily | All team members |
| Decision Records | As needed | ps-architect |

---

### D2: Define the Problem

#### IS / IS NOT Analysis

```
┌────────────────────────────────────────────────────────────────────────────┐
│                        IS / IS NOT MATRIX                                   │
├────────────────────────┬───────────────────────┬───────────────────────────┤
│       Dimension        │          IS           │         IS NOT            │
├────────────────────────┼───────────────────────┼───────────────────────────┤
│ WHAT                   │                       │                           │
│ - Object affected      │ VTT/SRT transcript    │ Audio/video files         │
│                        │ files                 │                           │
│ - Defect/Gap           │ No import capability  │ Poor transcription        │
│                        │ in market             │ quality                   │
│ - Problem scope        │ Text-to-insight       │ Speech-to-text            │
│                        │ processing            │ conversion                │
├────────────────────────┼───────────────────────┼───────────────────────────┤
│ WHERE                  │                       │                           │
│ - Geographic           │ Global (text formats  │ Region-specific           │
│                        │ are universal)        │ languages (Phase 1)       │
│ - On object            │ At file import stage  │ At recording stage        │
│ - Process step         │ Post-transcription    │ During live meeting       │
│                        │ analysis              │                           │
├────────────────────────┼───────────────────────┼───────────────────────────┤
│ WHEN                   │                       │                           │
│ - First observed       │ Market analysis       │ Recent development        │
│                        │ Jan 2026              │                           │
│ - Lifecycle stage      │ Pre-development       │ Post-release bug          │
│ - Pattern              │ Consistent gap        │ Intermittent issue        │
│                        │ across all 5          │                           │
│                        │ competitors           │                           │
├────────────────────────┼───────────────────────┼───────────────────────────┤
│ EXTENT                 │                       │                           │
│ - How many             │ 100% of competitors   │ Partial support           │
│                        │ lack this             │                           │
│ - How much             │ Zero VTT/SRT import   │ Limited features          │
│                        │ functionality         │                           │
│ - Trend                │ Static (business      │ Improving trend           │
│                        │ model driven)         │                           │
└────────────────────────┴───────────────────────┴───────────────────────────┘
```

#### 5W2H Problem Definition

| Question | Answer | Evidence Source |
|----------|--------|-----------------|
| **WHAT** | Text-first transcript processing capability gap | FEATURE-MATRIX.md: 0/5 competitors support import |
| **WHO** | Users with existing transcripts (enterprise, researchers, archivists) | Market analysis personas |
| **WHERE** | At the system boundary - file ingestion interface | Technical architecture review |
| **WHEN** | When user has transcript but lacks recording | User journey analysis |
| **WHY** | Business models favor recording-first monetization | Competitive analysis |
| **HOW** | No existing workflow supports BYOT (Bring Your Own Transcript) | Feature gap analysis |
| **HOW MUCH** | 100% market gap; $0 solutions exist | Quantitative assessment |

#### Problem Statement (Final)

> **The Transcript Skill must address the market-wide absence of text-first transcript processing, where users with existing VTT/SRT files cannot extract structured meeting intelligence (speakers, action items, decisions, questions, topics) without re-recording or using proprietary integrations. This gap affects 100% of analyzed competitors and represents a unique value proposition for users who possess transcripts but lack compatible processing tools.**

#### Scope Boundaries

```
IN SCOPE:
├── VTT file parsing (WebVTT standard)
├── SRT file parsing (SubRip de facto standard)
├── Speaker identification extraction
├── Standard NER (PERSON, ORG, DATE, GPE, MONEY)
├── Custom entity extraction:
│   ├── ACTION_ITEM
│   ├── DECISION
│   ├── QUESTION
│   └── TOPIC
├── Structured output generation
└── Quality metrics (precision, recall, F1)

OUT OF SCOPE (Phase 1):
├── Audio/video transcription
├── Real-time processing
├── Multi-language support (English only)
├── Proprietary format support
├── Meeting scheduling integration
└── CRM/PM tool integrations
```

---

### D3: Develop Interim Containment Actions

#### Assessment: Containment Needed?

| Factor | Evaluation |
|--------|------------|
| Customer impact severity | None - new capability |
| Revenue at risk | None - pre-release |
| Reputation risk | None - opportunity, not defect |
| Regulatory implications | None |

**Determination**: No interim containment required. This is a greenfield development, not a defect remediation.

#### Development Safeguards (Proactive)

While not containment in the traditional sense, these safeguards prevent scope creep:

| Safeguard | Purpose | Implementation |
|-----------|---------|----------------|
| Format limitation | Prevent feature bloat | Only VTT/SRT in Phase 1 |
| Language scope | Manage complexity | English-only initially |
| Entity type cap | Incremental delivery | 4 custom entities max |
| Integration deferral | Focus on core value | No external integrations |

---

### D4: Identify and Verify Root Causes

#### Potential Root Causes

Using 5-Why analysis on "Why doesn't text-first transcript processing exist?"

```
WHY #1: Why can't users import VTT/SRT files?
└── Answer: No competitor provides this feature.

WHY #2: Why don't competitors provide this feature?
└── Answer: Their business models depend on recording services.

WHY #3: Why do business models depend on recording?
└── Answer: Recording enables:
    ├── Per-minute pricing
    ├── Storage upsells
    └── Ecosystem lock-in

WHY #4: Why is ecosystem lock-in valuable?
└── Answer: Increases switching costs and lifetime value.

WHY #5: Why haven't niche players filled this gap?
└── Answer: Technical complexity and unclear ROI without
    recording revenue.
```

#### Root Cause Fishbone (Ishikawa) Diagram

```
                                    ┌─────────────────────────────────────┐
                                    │  TEXT-FIRST PROCESSING GAP EXISTS   │
                                    └─────────────────────────────────────┘
                                                      │
        ┌─────────────────────────────────────────────┼─────────────────────────────────────────────┐
        │                                             │                                             │
  BUSINESS MODEL                                  TECHNOLOGY                                    MARKET
        │                                             │                                             │
  ┌─────┴─────┐                               ┌───────┴───────┐                             ┌───────┴───────┐
  │           │                               │               │                             │               │
Recording  Per-minute                    NLP complexity   Format                       No demand      Low
revenue    pricing                       barrier         fragmentation                 articulation   awareness
    │                                         │               │                             │               │
    └── Lock-in                               └── Requires    └── VTT vs SRT              └── Users       └── Market
        strategy                                  ML expertise     variations                  adapt to        doesn't
                                                                                              tools           know better

  ┌─────┴─────┐                               ┌───────┴───────┐                             ┌───────┴───────┐
  │           │                               │               │                             │               │
PEOPLE                                    PROCESS                                       ENVIRONMENT
  │                                           │                                             │
Product     Engineering                  No standard      Development                  Enterprise      Compliance
managers    teams lack                   workflow         prioritizes                  restrictions    on recording
prioritize  transcript                   for text-        recording                    on recording
recording   domain                       first            features
            expertise                    analysis
```

#### Verified Root Causes

| Root Cause | Verification Evidence | Confidence |
|------------|----------------------|------------|
| **RC-1**: Business model misalignment | All 5 competitors monetize recording; none offer import | High (100% correlation) |
| **RC-2**: Technical complexity perception | NLP-NER-BEST-PRACTICES.md shows mature libraries exist | Medium (solvable) |
| **RC-3**: Demand not articulated | Market gap exists but users adapt to constraints | Medium (latent demand) |
| **RC-4**: Format standardization gaps | SRT has no official standard (ACADEMIC-LITERATURE-REVIEW.md) | High (documented) |

#### Root Cause Ranking

| Rank | Root Cause | Impact | Addressability | Priority |
|------|------------|--------|----------------|----------|
| 1 | RC-1: Business model misalignment | High | High (we control our model) | **Critical** |
| 2 | RC-4: Format standardization gaps | Medium | High (parsers exist) | **High** |
| 3 | RC-2: Technical complexity | Medium | High (mature NLP tools) | **Medium** |
| 4 | RC-3: Unarticulated demand | Low | Medium (marketing task) | **Low** |

---

### D5: Choose and Verify Permanent Corrective Actions

#### Corrective Action Matrix

| Root Cause | Corrective Action | Owner | Verification Method |
|------------|-------------------|-------|---------------------|
| RC-1: Business model | **CA-1**: Position as text-first tool, not recording platform | Product | Market positioning review |
| RC-4: Format gaps | **CA-2**: Implement robust VTT/SRT parsers with error tolerance | Engineering | Parser test suite (edge cases) |
| RC-2: Complexity | **CA-3**: Use proven NLP stack (spaCy + HuggingFace) | Engineering | Benchmark against academic baselines |
| RC-3: Demand | **CA-4**: Enable "import existing transcript" workflow prominently | UX | User testing, adoption metrics |

#### Detailed Corrective Actions

##### CA-1: Text-First Positioning

```
BEFORE (Competitor Model):
User → Record Meeting → Transcribe → Analyze → Insights

AFTER (Our Model):
User → Import Transcript (VTT/SRT) → Analyze → Insights
         ↓
    OR provide text directly
```

**Implementation**: Architecture must support file-first ingestion without any audio dependencies.

##### CA-2: Robust Format Parsing

**VTT Parser Requirements** (from VTT-SPECIFICATION.md):
- Handle WEBVTT header
- Parse cue identifiers (optional)
- Extract timestamps: `HH:MM:SS.mmm --> HH:MM:SS.mmm`
- Process cue payload (including voice tags `<v Speaker>`)
- Support multi-line cues

**SRT Parser Requirements** (from SRT-SPECIFICATION.md):
- Sequential cue numbering (with gap tolerance)
- Timestamps: `HH:MM:SS,mmm --> HH:MM:SS,mmm` (comma, not period)
- Handle DOS/Unix line endings
- Tolerate common malformations

**Recommended Libraries**:
| Format | Library | Rationale |
|--------|---------|-----------|
| VTT | `webvtt-py` | Mature, handles voice tags |
| SRT | `srt` | Lightweight (~200 LOC), fast |
| Fallback | `pysrt` | Advanced time manipulation |

##### CA-3: NLP Stack Selection

**Recommended Stack** (from NLP-NER-BEST-PRACTICES.md):

```
┌────────────────────────────────────────────────────────────┐
│                    EXTRACTION PIPELINE                      │
├────────────────────────────────────────────────────────────┤
│  Stage 1: Structural Extraction                             │
│  └── Speaker identification (regex, voice tags)            │
│      Libraries: Python re, custom patterns                  │
├────────────────────────────────────────────────────────────┤
│  Stage 2: Standard NER                                      │
│  └── PERSON, ORG, DATE, GPE, MONEY                         │
│      Library: spaCy (en_core_web_trf for accuracy)         │
├────────────────────────────────────────────────────────────┤
│  Stage 3: Domain Entity Extraction                          │
│  └── ACTION_ITEM, DECISION, QUESTION                       │
│      Library: HuggingFace Transformers (fine-tuned)        │
│      OR: LLM-based extraction (GPT-4, Claude)              │
├────────────────────────────────────────────────────────────┤
│  Stage 4: Topic Modeling                                    │
│  └── TOPIC extraction and clustering                        │
│      Library: BERTopic                                      │
├────────────────────────────────────────────────────────────┤
│  Stage 5: Enrichment                                        │
│  └── Cross-reference, deduplication, confidence scoring    │
│      Library: Custom logic                                  │
└────────────────────────────────────────────────────────────┘
```

**Academic Benchmarks to Target** (from ACADEMIC-LITERATURE-REVIEW.md):

| Entity Type | Target F1 | Benchmark Source |
|-------------|-----------|------------------|
| ACTION_ITEM | 0.85+ | ur_BLOOMZ-1b1 achieved 0.94 |
| DECISION | 0.75+ | Limited benchmarks |
| QUESTION | 0.90+ | Sentence classification task |
| SPEAKER | 0.95+ | Structural extraction |

##### CA-4: User Workflow Enablement

**Primary User Journey**:
```
1. User has VTT/SRT file (from any source)
2. User invokes Transcript Skill
3. Skill prompts for file path
4. Skill parses and validates format
5. Skill extracts entities
6. Skill presents structured results
7. User can query/filter/export results
```

**Acceptance Criteria**:
- [ ] Single-command file import
- [ ] Clear error messages for malformed files
- [ ] Progress indication for large files
- [ ] Structured output with confidence scores

#### Verification Plan

| Corrective Action | Verification Criteria | Method |
|-------------------|----------------------|--------|
| CA-1 | No audio processing dependencies | Architecture review, dependency audit |
| CA-2 | 100% valid file parsing, 95%+ malformed tolerance | Test suite with edge cases |
| CA-3 | F1 >= 0.85 for ACTION_ITEM | Benchmark against AMI corpus |
| CA-4 | < 3 steps from file to insights | User journey testing |

---

### D6: Implement and Validate Permanent Corrective Actions

#### Implementation Roadmap

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        IMPLEMENTATION PHASES                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  PHASE 1: Foundation (Weeks 1-2)                                            │
│  ├── CA-2: VTT Parser implementation                                        │
│  ├── CA-2: SRT Parser implementation                                        │
│  └── Unit tests for parsing edge cases                                      │
│                                                                              │
│  PHASE 2: Core Extraction (Weeks 3-6)                                       │
│  ├── CA-3: Speaker identification                                           │
│  ├── CA-3: Standard NER integration (spaCy)                                 │
│  ├── CA-3: Custom entity extraction (ACTION_ITEM, DECISION, QUESTION)       │
│  └── CA-3: Topic modeling (BERTopic)                                        │
│                                                                              │
│  PHASE 3: Integration (Weeks 7-8)                                           │
│  ├── CA-1: Skill interface (Jerry framework integration)                    │
│  ├── CA-4: User workflow implementation                                     │
│  └── End-to-end testing                                                     │
│                                                                              │
│  PHASE 4: Validation (Weeks 9-10)                                           │
│  ├── Benchmark evaluation (AMI corpus)                                      │
│  ├── User acceptance testing                                                │
│  └── Documentation and deployment                                           │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

#### Validation Criteria

| Milestone | Validation Gate | Pass Criteria |
|-----------|-----------------|---------------|
| M1: Parsers complete | Parser test suite | 100% valid files, 95% malformed |
| M2: NER integrated | Entity extraction tests | F1 >= 0.80 for standard entities |
| M3: Custom entities | Domain entity tests | F1 >= 0.75 for ACTION_ITEM |
| M4: Full pipeline | End-to-end tests | Complete workflow < 5 seconds for typical file |
| M5: User validation | UAT | Task success rate >= 90% |

#### Risk Mitigation

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| NLP accuracy below target | Medium | High | Fallback to LLM-based extraction |
| Format edge cases | High | Medium | Extensive test corpus from real-world files |
| Performance issues | Low | Medium | Async processing, progress indication |
| Scope creep | Medium | High | Strict phase gates, feature freeze |

---

### D7: Prevent Recurrence

#### Systemic Prevention Measures

| Prevention | Scope | Implementation |
|------------|-------|----------------|
| **P-1**: Format-first design principle | Architecture | Port/adapter pattern for input formats |
| **P-2**: Benchmark-driven development | Process | Academic benchmarks as acceptance criteria |
| **P-3**: Extensibility for new formats | Architecture | Parser abstraction layer |
| **P-4**: Regular competitive analysis | Process | Quarterly feature matrix updates |

#### Architectural Prevention: Format Abstraction

```
┌─────────────────────────────────────────────────────────────┐
│                      PRIMARY PORT                            │
│              ITranscriptParser Protocol                      │
├─────────────────────────────────────────────────────────────┤
│  + parse(content: str) -> Transcript                        │
│  + validate(content: str) -> ValidationResult               │
│  + get_format() -> TranscriptFormat                         │
└─────────────────────────────────────────────────────────────┘
                              │
            ┌─────────────────┼─────────────────┐
            │                 │                 │
            ▼                 ▼                 ▼
    ┌───────────────┐ ┌───────────────┐ ┌───────────────┐
    │  VTTParser    │ │  SRTParser    │ │  Future:      │
    │  Adapter      │ │  Adapter      │ │  TXTParser    │
    └───────────────┘ └───────────────┘ └───────────────┘
```

**Principle**: Adding a new format should require only a new adapter, no core changes.

#### Process Controls

| Control | Trigger | Action |
|---------|---------|--------|
| Format request triage | New format requested | Evaluate against abstraction pattern |
| Benchmark regression | F1 drops below threshold | Automated alert, investigation spike |
| Competitive drift | Competitor adds import | Update feature matrix, assess response |

#### Knowledge Capture

| Artifact | Purpose | Location |
|----------|---------|----------|
| This 8D Analysis | Problem solving methodology | EN-003-requirements-synthesis/analysis/ |
| Format specifications | Technical reference | EN-002-technical-standards/research/ |
| Benchmark baselines | Quality targets | EN-002-technical-standards/research/ |
| Competitive analysis | Market context | EN-001-market-analysis/research/ |

---

### D8: Recognize Team and Celebrate Success

#### Team Contributions

| Contributor | Contribution | Recognition |
|-------------|--------------|-------------|
| ps-analyst | 8D methodology application, problem definition | Analysis lead |
| ps-researcher | Technical research, benchmark identification | Research excellence |
| EN-001 analysis | Market gap identification | Foundation work |
| EN-002 analysis | Technical feasibility validation | Technical grounding |

#### Success Metrics

| Metric | Target | Measurement Point |
|--------|--------|-------------------|
| Problem clarity | 100% team alignment on definition | D2 completion |
| Root cause identification | All major causes identified | D4 verification |
| Corrective action coverage | 100% root causes addressed | D5 mapping |
| Implementation readiness | Clear roadmap with milestones | D6 completion |
| Prevention sustainability | Architectural controls in place | D7 documentation |

#### Lessons Learned

| Lesson | Category | Application |
|--------|----------|-------------|
| Market gap = opportunity, not defect | Mindset | 8D applies to opportunity definition |
| Academic benchmarks provide objectivity | Quality | Use published metrics for validation |
| Business model analysis reveals true root cause | Analysis | Look beyond technical factors |
| Format fragmentation requires abstraction | Architecture | Design for extensibility early |

---

## L2: Architectural Perspective (Principal Architect)

### Strategic Architecture Implications

#### Market Position via Architecture

The identified market gap (100% recording-first competitors) creates an architectural imperative:

```
STRATEGIC DECISION: Text-First Architecture

Rationale:
1. Market differentiation requires ZERO audio dependencies
2. Extensibility to new text formats must be trivial
3. NLP pipeline must be independently testable/replaceable
4. Integration with Jerry framework follows hexagonal patterns

Architectural Style: Hexagonal Architecture + CQRS
```

#### Bounded Context Mapping

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         TRANSCRIPT SKILL CONTEXT                             │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌───────────────────┐        ┌───────────────────┐                         │
│  │   PARSING         │        │   EXTRACTION      │                         │
│  │   SUBCONTEXT      │        │   SUBCONTEXT      │                         │
│  │                   │        │                   │                         │
│  │ • VTT Parser      │───────►│ • Speaker ID      │                         │
│  │ • SRT Parser      │        │ • Standard NER    │                         │
│  │ • Transcript      │        │ • Custom NER      │                         │
│  │   Model           │        │ • Topic Model     │                         │
│  │                   │        │                   │                         │
│  └───────────────────┘        └───────────────────┘                         │
│           │                            │                                     │
│           │                            ▼                                     │
│           │                   ┌───────────────────┐                         │
│           │                   │   PRESENTATION    │                         │
│           │                   │   SUBCONTEXT      │                         │
│           │                   │                   │                         │
│           └──────────────────►│ • Result Model    │                         │
│                               │ • Query Interface │                         │
│                               │ • Export Formats  │                         │
│                               │                   │                         │
│                               └───────────────────┘                         │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
                                        │
                                        ▼
                         ┌───────────────────────────┐
                         │    JERRY FRAMEWORK        │
                         │    INTEGRATION            │
                         │    (Skills Layer)         │
                         └───────────────────────────┘
```

#### Critical Architectural Decisions

##### ADR-001: Parser Abstraction (from D7 Prevention)

**Context**: Multiple transcript formats exist (VTT, SRT, future: TXT, custom)

**Decision**: Implement ITranscriptParser protocol with format-specific adapters

**Consequences**:
- (+) New formats require only adapter implementation
- (+) Parsing logic is independently testable
- (-) Slight abstraction overhead
- (-) Must maintain consistent Transcript model

##### ADR-002: NLP Pipeline Composition

**Context**: Multiple extraction stages with different tool requirements

**Decision**: Staged pipeline with explicit interfaces between stages

```python
class IExtractionStage(Protocol):
    def process(self, transcript: Transcript) -> ExtractionResult: ...
    def get_entity_types(self) -> set[EntityType]: ...
```

**Consequences**:
- (+) Stages can be swapped/upgraded independently
- (+) Easy to add new entity types
- (+) Parallel processing possible
- (-) Coordination complexity
- (-) Must handle cross-stage dependencies

##### ADR-003: LLM Fallback Strategy

**Context**: Traditional NLP may not achieve target F1 for domain entities

**Decision**: Implement dual-mode extraction with LLM fallback

```
Primary Path: spaCy + HuggingFace (faster, cheaper)
         │
         ▼ (if F1 < threshold)
Fallback Path: LLM-based extraction (GPT-4/Claude)
```

**Consequences**:
- (+) Best-of-both-worlds: speed when possible, accuracy when needed
- (+) Academic benchmarks achievable with LLM path
- (-) Cost implications for LLM usage
- (-) Latency variance between paths

### Performance Considerations

| Operation | Target Latency | Scaling Strategy |
|-----------|----------------|------------------|
| File parsing | < 100ms | Streaming parser |
| Speaker ID | < 500ms | Regex, no ML |
| Standard NER | < 2s | spaCy batching |
| Custom NER | < 5s | HuggingFace batching or LLM |
| Topic modeling | < 3s | Pre-trained BERTopic |
| **Total pipeline** | **< 10s** | Async stages, progress reporting |

### Quality Gate Integration

```
┌─────────────────────────────────────────────────────────────┐
│                    QUALITY GATES                             │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  GATE 1: Parsing Validation                                  │
│  ├── Format detection accuracy: 100%                        │
│  ├── Valid file parsing: 100%                               │
│  └── Malformed file tolerance: 95%                          │
│                                                              │
│  GATE 2: Extraction Accuracy                                 │
│  ├── Speaker ID F1: >= 0.95                                 │
│  ├── Standard NER F1: >= 0.80                               │
│  └── Custom NER F1: >= 0.75                                 │
│                                                              │
│  GATE 3: User Experience                                     │
│  ├── Task completion rate: >= 90%                           │
│  ├── Error message clarity: User testing pass               │
│  └── Response time: < 10s for typical file                  │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### One-Way Door Decisions

| Decision | Reversibility | Risk Mitigation |
|----------|---------------|-----------------|
| Hexagonal architecture | Low | Align with Jerry framework patterns |
| Parser abstraction | Medium | Well-defined interface contracts |
| NLP library selection | Medium | Abstraction allows replacement |
| LLM fallback inclusion | High | Feature flag for enablement |
| Entity type taxonomy | Low | Extensible enum, not closed set |

### Technical Debt Prevention

| Debt Category | Prevention Mechanism |
|---------------|---------------------|
| Format coupling | Port/adapter pattern (ADR-001) |
| NLP tool lock-in | Stage abstraction (ADR-002) |
| Accuracy shortcuts | Benchmark-driven acceptance criteria |
| Test coverage gaps | Quality gate enforcement |

---

## References

### Input Sources

| Source | Type | Key Contribution |
|--------|------|------------------|
| EN-001/FEATURE-MATRIX.md | Market Analysis | Competitive gap identification |
| EN-001/*-analysis.md | Product Analysis | Recording-first paradigm validation |
| EN-002/VTT-SPECIFICATION.md | Technical Spec | VTT format requirements |
| EN-002/SRT-SPECIFICATION.md | Technical Spec | SRT format requirements |
| EN-002/NLP-NER-BEST-PRACTICES.md | Technical Guide | NLP pipeline architecture |
| EN-002/ACADEMIC-LITERATURE-REVIEW.md | Research | Benchmark targets, hallucination rates |

### External References

| Reference | Type | URL/Citation |
|-----------|------|--------------|
| 8D Problem Solving | Methodology | ASQ (American Society for Quality) |
| spaCy Documentation | Library | https://spacy.io/ |
| HuggingFace Transformers | Library | https://huggingface.co/transformers/ |
| BERTopic | Library | https://maartengr.github.io/BERTopic/ |
| AMI Corpus | Benchmark | https://groups.inf.ed.ac.uk/ami/corpus/ |
| WebVTT Standard | W3C | https://www.w3.org/TR/webvtt1/ |

### 8D Methodology Sources

| Source | Contribution |
|--------|--------------|
| ASQ (American Society for Quality) | 8D framework definition |
| Quality-One International | Practical 8D templates |
| Atlassian | 8D in software context |
| Ford Motor Company | Original 8D methodology |

---

## Document History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-01-25 | ps-analyst | Initial 8D analysis complete |

---

## Appendix A: Entity Type Taxonomy

```
ENTITY TAXONOMY
├── STRUCTURAL (Parsing-derived)
│   └── SPEAKER
│       ├── Source: Voice tags, prefix patterns
│       └── Confidence: High (structural)
│
├── STANDARD NER (spaCy/Transformers)
│   ├── PERSON
│   ├── ORG (Organization)
│   ├── DATE
│   ├── GPE (Geo-Political Entity)
│   └── MONEY
│
└── DOMAIN ENTITIES (Custom extraction)
    ├── ACTION_ITEM
    │   ├── Indicators: "will", "should", "need to", "by Friday"
    │   └── Extraction: Pattern + LLM
    │
    ├── DECISION
    │   ├── Indicators: "decided", "agreed", "approved", "we'll go with"
    │   └── Extraction: Pattern + LLM
    │
    ├── QUESTION
    │   ├── Indicators: Interrogative syntax, "?"
    │   └── Extraction: Sentence classification
    │
    └── TOPIC
        ├── Source: BERTopic clustering
        └── Confidence: Variable (semantic)
```

---

## Appendix B: Parser Error Tolerance Matrix

| Error Type | VTT Tolerance | SRT Tolerance | Recovery Strategy |
|------------|---------------|---------------|-------------------|
| Missing header | N/A | N/A | Infer from content |
| Malformed timestamp | Partial | Partial | Skip cue, log warning |
| Missing sequence number | N/A | Full | Auto-generate sequence |
| Encoding issues | Full | Full | Detect and convert |
| Empty cues | Full | Full | Skip silently |
| Overlapping times | Partial | Partial | Accept, flag for review |
| Invalid line endings | Full | Full | Normalize to \n |

---

*End of 8D Problem Solving Analysis*
