# Failure Mode and Effects Analysis (FMEA): Transcript Skill

> **NASA SE Disclaimer**: This analysis follows NPR 8000.4C (Risk Management) and NPR 7123.1D Process 13 (Risk Analysis) methodologies adapted for software development context. While not a flight-critical mission, we apply mission-grade rigor to ensure high-quality deliverables.

---

> **Project ID**: PROJ-008-transcript-skill
> **Entry ID**: e-003
> **Analysis Type**: Failure Mode and Effects Analysis (FMEA)
> **Topic**: Risk Assessment for Text-First Transcript Processing
> **Date**: 2026-01-25
> **Author**: nse-risk agent (Problem-Solving Framework)
> **Version**: 1.0
> **Status**: Complete

---

## Document Navigation

| Level | Audience | Section |
|-------|----------|---------|
| L0 | Executive / ELI5 | [Executive Summary](#l0-executive-summary-eli5) |
| L1 | Software Engineer | [Full Risk Register](#l1-technical-analysis-software-engineer) |
| L2 | Principal Architect | [Risk Portfolio Analysis](#l2-architectural-perspective-principal-architect) |

---

## L0: Executive Summary (ELI5)

### What is FMEA?

Imagine you're building a LEGO castle. Before you start, you think about what could go wrong:
- What if a piece is missing?
- What if the tower falls over?
- What if the drawbridge doesn't open?

FMEA is like making a list of everything that could go wrong with our transcript tool, deciding how bad each problem would be, and making a plan to prevent or fix it.

### Top 5 Risks (Plain English)

| Rank | Risk | What Could Happen | How We'll Prevent It |
|------|------|-------------------|---------------------|
| 1 | **Action Item Detection Fails** | The tool misses important tasks or invents fake ones | Use multiple detection methods; test extensively |
| 2 | **Transcript Files Are Messy** | Files from different apps look different; parser breaks | Build flexible parser that handles variations |
| 3 | **Speaker Names Wrong** | Tool confuses who said what | Use multiple patterns to identify speakers |
| 4 | **Tool Runs Too Slow** | Users get frustrated waiting | Optimize performance; show progress |
| 5 | **Integration Breaks Jerry** | Adding this skill breaks other things | Follow existing patterns; thorough testing |

### Risk Summary Dashboard

```
RISK PORTFOLIO SUMMARY
======================

    RED (Critical)     YELLOW (Watch)      GREEN (Acceptable)
    ──────────────     ──────────────      ──────────────────
    │     0      │     │     5      │      │     15     │
    └────────────┘     └────────────┘      └────────────┘

    Overall Risk Posture: MANAGEABLE

    Highest Risk Component: Action Item Extraction (Score: 12)
    Lowest Risk Component:  CLI Framework (Score: 2)
```

### What This Means

**Good News**: We have NO critical (RED) risks. All identified risks can be managed with proper mitigation.

**Watch Items**: 5 risks need active monitoring during development:
1. Action item detection accuracy
2. Transcript format edge cases
3. Speaker identification complexity
4. NLP model performance
5. LLM hallucination potential

**Bottom Line**: The project is technically feasible with acceptable risk levels if we follow the mitigation strategies outlined in this document.

---

## L1: Technical Analysis (Software Engineer)

### 1. Risk Assessment Methodology

#### 1.1 5x5 Risk Matrix Definition

We use a standard 5x5 risk matrix aligned with NPR 8000.4C:

```
              C O N S E Q U E N C E

           │ 1-Minimal │ 2-Minor │ 3-Moderate │ 4-Major │ 5-Critical │
    ───────┼───────────┼─────────┼────────────┼─────────┼────────────┤
L   5-Almost│    5      │   10    │     15     │   20    │     25     │
I    Certain│  YELLOW   │ YELLOW  │    RED     │   RED   │    RED     │
K   ────────┼───────────┼─────────┼────────────┼─────────┼────────────┤
E   4-Likely│    4      │    8    │     12     │   16    │     20     │
L          │  GREEN    │ YELLOW  │   YELLOW   │   RED   │    RED     │
I   ────────┼───────────┼─────────┼────────────┼─────────┼────────────┤
H   3-Poss- │    3      │    6    │      9     │   12    │     15     │
O    ible  │  GREEN    │  GREEN  │   YELLOW   │ YELLOW  │    RED     │
O   ────────┼───────────┼─────────┼────────────┼─────────┼────────────┤
D   2-Unlik-│    2      │    4    │      6     │    8    │     10     │
     ely   │  GREEN    │  GREEN  │   GREEN    │ YELLOW  │   YELLOW   │
    ────────┼───────────┼─────────┼────────────┼─────────┼────────────┤
    1-Rare  │    1      │    2    │      3     │    4    │      5     │
           │  GREEN    │  GREEN  │   GREEN    │  GREEN  │   YELLOW   │

Risk Level:  GREEN (1-7) = Acceptable
             YELLOW (8-15) = Monitor/Mitigate
             RED (16-25) = Unacceptable - Requires Action
```

#### 1.2 Likelihood Scale

| Level | Name | Definition | Examples |
|-------|------|------------|----------|
| 5 | Almost Certain | >90% probability | Common edge cases, known issues |
| 4 | Likely | 70-90% probability | Frequently encountered conditions |
| 3 | Possible | 30-70% probability | Occasionally encountered |
| 2 | Unlikely | 10-30% probability | Uncommon but documented |
| 1 | Rare | <10% probability | Exceptional circumstances |

#### 1.3 Consequence Scale

| Level | Name | Technical Impact | Schedule Impact | User Impact |
|-------|------|------------------|-----------------|-------------|
| 5 | Critical | System failure, data loss | >4 weeks delay | Complete feature failure |
| 4 | Major | Major feature broken | 2-4 weeks delay | Significant UX degradation |
| 3 | Moderate | Feature partially working | 1-2 weeks delay | Noticeable quality issues |
| 2 | Minor | Minor defects | <1 week delay | Cosmetic issues |
| 1 | Minimal | Negligible impact | No schedule impact | Imperceptible |

---

### 2. Full Risk Register

#### 2.1 VTT/SRT Parser Risks

##### R-001: VTT Format Edge Cases

| Field | Value |
|-------|-------|
| **Risk ID** | R-001 |
| **Component** | VTT Parser |
| **Failure Mode** | Parser fails on non-standard VTT variations |
| **Risk Statement** | If transcript files contain non-standard VTT extensions (e.g., styling, regions, positioning), then the parser may fail or produce incomplete results |
| **Potential Effect** | Incomplete transcript parsing, lost content, user frustration |
| **Root Cause** | VTT spec allows many optional features; vendors implement subsets differently |
| **Likelihood** | 3 - Possible (30-70%) |
| **L Justification** | VTT-SPECIFICATION.md documents many optional features; real-world files vary |
| **Consequence** | 2 - Minor |
| **C Justification** | Parser libraries (webvtt-py) handle most cases; edge cases are recoverable |
| **Score** | 6 (GREEN) |
| **Current Controls** | Use mature webvtt-py library with good spec coverage |
| **Mitigation Actions** | 1. Build test corpus with diverse VTT samples 2. Implement graceful degradation 3. Log parsing anomalies for iteration |
| **Risk Owner** | Engineering |
| **Residual Risk** | 4 (GREEN) after mitigation |

##### R-002: SRT Timestamp Malformation

| Field | Value |
|-------|-------|
| **Risk ID** | R-002 |
| **Component** | SRT Parser |
| **Failure Mode** | Parser rejects files with timestamp variations |
| **Risk Statement** | If SRT files use period instead of comma for milliseconds (00:00:00.000 vs 00:00:00,000), then parsing may fail |
| **Potential Effect** | User cannot process valid transcript files |
| **Root Cause** | SRT has no formal specification; de facto standards vary (SRT-SPECIFICATION.md) |
| **Likelihood** | 4 - Likely (70-90%) |
| **L Justification** | SRT-SPECIFICATION.md confirms this is a common variation |
| **Consequence** | 2 - Minor |
| **C Justification** | Easy to detect and normalize; srt library provides flexibility |
| **Score** | 8 (YELLOW) |
| **Current Controls** | srt library handles some variations |
| **Mitigation Actions** | 1. Pre-process timestamps to normalize format 2. Accept both . and , separators 3. Provide clear error messages for truly malformed files |
| **Risk Owner** | Engineering |
| **Residual Risk** | 4 (GREEN) after mitigation |

##### R-003: Character Encoding Issues

| Field | Value |
|-------|-------|
| **Risk ID** | R-003 |
| **Component** | VTT/SRT Parser |
| **Failure Mode** | Non-UTF8 encoded files fail to parse |
| **Risk Statement** | If transcript files use legacy encodings (Windows-1252, ISO-8859-1), then Unicode decode errors occur |
| **Potential Effect** | Garbled text, parsing failures |
| **Root Cause** | Older transcription tools may not output UTF-8 |
| **Likelihood** | 3 - Possible |
| **L Justification** | Legacy files exist but UTF-8 is now standard |
| **Consequence** | 2 - Minor |
| **C Justification** | Encoding detection libraries can handle this |
| **Score** | 6 (GREEN) |
| **Current Controls** | Python 3 UTF-8 by default |
| **Mitigation Actions** | 1. Use chardet for encoding detection 2. Attempt multiple encodings before failing 3. Document supported encodings |
| **Risk Owner** | Engineering |
| **Residual Risk** | 3 (GREEN) |

---

#### 2.2 Speaker Identification Risks

##### R-004: Missing VTT Voice Tags

| Field | Value |
|-------|-------|
| **Risk ID** | R-004 |
| **Component** | Speaker Identification |
| **Failure Mode** | VTT files lack voice tags (`<v Speaker>`) |
| **Risk Statement** | If VTT files do not contain voice tags (many transcription services omit them), then speaker identification relies on pattern matching |
| **Potential Effect** | Reduced speaker identification accuracy |
| **Root Cause** | Voice tags are optional in VTT spec; not all tools generate them |
| **Likelihood** | 4 - Likely |
| **L Justification** | FEATURE-MATRIX.md shows varied export formats; many omit voice tags |
| **Consequence** | 3 - Moderate |
| **C Justification** | Significantly impacts multi-speaker meeting analysis usefulness |
| **Score** | 12 (YELLOW) |
| **Current Controls** | None - new capability |
| **Mitigation Actions** | 1. Implement fallback patterns (Name:, [Name], ALL CAPS:) 2. Allow user-provided speaker mappings 3. Document limitations clearly |
| **Risk Owner** | Engineering |
| **Residual Risk** | 6 (GREEN) with multi-pattern approach |

##### R-005: Speaker Name Variations

| Field | Value |
|-------|-------|
| **Risk ID** | R-005 |
| **Component** | Speaker Identification |
| **Failure Mode** | Same speaker has multiple name forms |
| **Risk Statement** | If the same speaker appears as "John", "John Smith", and "J. Smith", then analysis treats them as different speakers |
| **Potential Effect** | Fragmented speaker analysis, incorrect attribution |
| **Root Cause** | No normalization of speaker names during transcription |
| **Likelihood** | 4 - Likely |
| **L Justification** | Common in real transcripts; observed in academic corpora |
| **Consequence** | 2 - Minor |
| **C Justification** | Affects analysis quality but doesn't break functionality |
| **Score** | 8 (YELLOW) |
| **Current Controls** | None - new capability |
| **Mitigation Actions** | 1. Implement speaker name normalization 2. Fuzzy matching for similar names 3. Manual speaker mapping option |
| **Risk Owner** | Engineering |
| **Residual Risk** | 4 (GREEN) |

---

#### 2.3 Action Item Detection Risks

##### R-006: Low Precision (False Positives)

| Field | Value |
|-------|-------|
| **Risk ID** | R-006 |
| **Component** | Action Item Extraction |
| **Failure Mode** | Non-action statements classified as action items |
| **Risk Statement** | If the NLP model has low precision, then users receive many irrelevant "action items" reducing trust |
| **Potential Effect** | User loses confidence in tool; abandons usage |
| **Root Cause** | Conversational language is ambiguous; modal verbs don't always indicate commitment |
| **Likelihood** | 4 - Likely |
| **L Justification** | ACADEMIC-LITERATURE-REVIEW.md shows F1 ranges 0.13-0.94 depending on approach |
| **Consequence** | 3 - Moderate |
| **C Justification** | Core value proposition affected; significant UX impact |
| **Score** | 12 (YELLOW) |
| **Current Controls** | None - new capability |
| **Mitigation Actions** | 1. Use confidence thresholds (only show high-confidence items by default) 2. Implement rule + ML hybrid approach 3. Allow user feedback loop for tuning 4. Target F1 >= 0.80 |
| **Risk Owner** | Engineering/NLP |
| **Residual Risk** | 6 (GREEN) with hybrid approach |

##### R-007: Low Recall (Missed Action Items)

| Field | Value |
|-------|-------|
| **Risk ID** | R-007 |
| **Component** | Action Item Extraction |
| **Failure Mode** | Actual action items not detected |
| **Risk Statement** | If the NLP model has low recall, then important commitments are missed, defeating the tool's purpose |
| **Potential Effect** | Users miss critical follow-ups; reduced utility |
| **Root Cause** | Implicit action items, varied linguistic patterns |
| **Likelihood** | 3 - Possible |
| **L Justification** | Pattern-based approaches can achieve good recall; ML adds coverage |
| **Consequence** | 4 - Major |
| **C Justification** | Missing action items directly harms user workflow |
| **Score** | 12 (YELLOW) |
| **Current Controls** | None - new capability |
| **Mitigation Actions** | 1. Prioritize recall in model tuning 2. Multiple extraction strategies in parallel 3. Allow users to flag missed items |
| **Risk Owner** | Engineering/NLP |
| **Residual Risk** | 6 (GREEN) with multi-strategy approach |

##### R-008: Action Item Hallucination

| Field | Value |
|-------|-------|
| **Risk ID** | R-008 |
| **Component** | Action Item Extraction (LLM Path) |
| **Failure Mode** | LLM invents action items not in transcript |
| **Risk Statement** | If using LLM extraction, then hallucinated action items may be generated, creating false work commitments |
| **Potential Effect** | User acts on non-existent commitments; trust destroyed |
| **Root Cause** | LLM hallucination is a known issue (1.5-8.0% rate per ACADEMIC-LITERATURE-REVIEW.md) |
| **Likelihood** | 3 - Possible |
| **L Justification** | GPT-4o: 1.5% rate; smaller models higher; extractive tasks lower risk |
| **Consequence** | 4 - Major |
| **C Justification** | Acting on false information is serious; damages credibility |
| **Score** | 12 (YELLOW) |
| **Current Controls** | None - new capability |
| **Mitigation Actions** | 1. Require transcript span citations for each action item 2. Use extractive (not generative) prompts 3. Implement confidence scoring 4. Validate against source text |
| **Risk Owner** | Engineering/NLP |
| **Residual Risk** | 6 (GREEN) with citation requirement |

---

#### 2.4 Decision Extraction Risks

##### R-009: Implicit Decisions Missed

| Field | Value |
|-------|-------|
| **Risk ID** | R-009 |
| **Component** | Decision Extraction |
| **Failure Mode** | Unstated but understood decisions not captured |
| **Risk Statement** | If decisions are implied but not explicitly stated (e.g., nodding, "sounds good"), then they are missed |
| **Potential Effect** | Incomplete decision record |
| **Root Cause** | Text-only analysis cannot capture non-verbal agreement |
| **Likelihood** | 4 - Likely |
| **L Justification** | Many decisions are implicit in normal conversation |
| **Consequence** | 2 - Minor |
| **C Justification** | Explicit decisions are more important; implicit are nice-to-have |
| **Score** | 8 (YELLOW) |
| **Current Controls** | None - new capability |
| **Mitigation Actions** | 1. Focus on explicit decisions first 2. Document limitation clearly 3. Consider consensus patterns (multiple agreement phrases) |
| **Risk Owner** | Engineering |
| **Residual Risk** | 4 (GREEN) with scope clarity |

---

#### 2.5 Topic Modeling Risks

##### R-010: Topic Coherence Issues

| Field | Value |
|-------|-------|
| **Risk ID** | R-010 |
| **Component** | Topic Detection |
| **Failure Mode** | Generated topics are vague or overlapping |
| **Risk Statement** | If BERTopic produces low-coherence topics, then the meeting structure analysis is unhelpful |
| **Potential Effect** | Users ignore topic feature; reduced value |
| **Root Cause** | Short utterances in transcripts challenge topic models |
| **Likelihood** | 3 - Possible |
| **L Justification** | NLP-NER-BEST-PRACTICES.md notes short text challenges for topic modeling |
| **Consequence** | 2 - Minor |
| **C Justification** | Topic detection is Phase 2 feature; not core MVP |
| **Score** | 6 (GREEN) |
| **Current Controls** | BERTopic designed for short texts |
| **Mitigation Actions** | 1. Aggregate utterances by time window before modeling 2. Use domain-specific embeddings 3. Allow manual topic override |
| **Risk Owner** | Engineering |
| **Residual Risk** | 4 (GREEN) |

---

#### 2.6 CLI Interface Risks

##### R-011: CLI Usability Issues

| Field | Value |
|-------|-------|
| **Risk ID** | R-011 |
| **Component** | CLI Interface |
| **Failure Mode** | Complex or inconsistent command structure |
| **Risk Statement** | If CLI design doesn't follow conventions (POSIX, clig.dev), then users struggle with adoption |
| **Potential Effect** | Poor developer experience; reduced adoption |
| **Root Cause** | Inconsistent design, poor error messages |
| **Likelihood** | 2 - Unlikely |
| **L Justification** | Using click/typer with established patterns; 5W2H outlines design |
| **Consequence** | 2 - Minor |
| **C Justification** | CLI is foundation but fixable post-release |
| **Score** | 4 (GREEN) |
| **Current Controls** | Design based on clig.dev and Heroku CLI Style Guide |
| **Mitigation Actions** | 1. User testing with Developer Dan persona 2. Follow Heroku CLI Style Guide 3. Comprehensive --help documentation |
| **Risk Owner** | Engineering |
| **Residual Risk** | 2 (GREEN) |

##### R-012: Exit Code Inconsistency

| Field | Value |
|-------|-------|
| **Risk ID** | R-012 |
| **Component** | CLI Interface |
| **Failure Mode** | Non-standard exit codes break scripting |
| **Risk Statement** | If exit codes don't follow convention (0=success, 1=error, 2=usage), then pipeline integration fails |
| **Potential Effect** | CI/CD integration broken; scripting unreliable |
| **Root Cause** | Oversight in error handling |
| **Likelihood** | 1 - Rare |
| **L Justification** | Standard practice; easily enforced with tests |
| **Consequence** | 2 - Minor |
| **C Justification** | Easily fixed; detected quickly |
| **Score** | 2 (GREEN) |
| **Current Controls** | Design spec includes exit code standards |
| **Mitigation Actions** | 1. Unit tests for all exit code paths 2. Document exit codes in --help |
| **Risk Owner** | Engineering |
| **Residual Risk** | 2 (GREEN) |

---

#### 2.7 Output Generation Risks

##### R-013: Markdown Rendering Issues

| Field | Value |
|-------|-------|
| **Risk ID** | R-013 |
| **Component** | Output Generation |
| **Failure Mode** | Generated Markdown renders incorrectly |
| **Risk Statement** | If Markdown output contains syntax errors, then rendering in different viewers is broken |
| **Potential Effect** | Poor presentation; manual fixes needed |
| **Root Cause** | Escaping issues, table alignment, special characters |
| **Likelihood** | 2 - Unlikely |
| **L Justification** | Templated output with tested patterns |
| **Consequence** | 1 - Minimal |
| **C Justification** | Cosmetic issue; content still readable |
| **Score** | 2 (GREEN) |
| **Current Controls** | Template-based generation |
| **Mitigation Actions** | 1. Test output in multiple Markdown renderers 2. Use safe escaping for special characters |
| **Risk Owner** | Engineering |
| **Residual Risk** | 2 (GREEN) |

##### R-014: JSON Schema Breaking Changes

| Field | Value |
|-------|-------|
| **Risk ID** | R-014 |
| **Component** | Output Generation |
| **Failure Mode** | JSON output schema changes break consumers |
| **Risk Statement** | If JSON schema evolves without versioning, then downstream integrations fail |
| **Potential Effect** | Breaking changes for API consumers |
| **Root Cause** | No schema versioning policy |
| **Likelihood** | 3 - Possible |
| **L Justification** | Schema will evolve as features are added |
| **Consequence** | 3 - Moderate |
| **C Justification** | Affects integration partners; recovery requires updates |
| **Score** | 9 (YELLOW) |
| **Current Controls** | None - new capability |
| **Mitigation Actions** | 1. Implement JSON Schema versioning from v1 2. Use semantic versioning for breaking changes 3. Document schema in OpenAPI/JSON Schema format |
| **Risk Owner** | Engineering |
| **Residual Risk** | 4 (GREEN) with versioning |

---

#### 2.8 Jerry Framework Integration Risks

##### R-015: Skill Interface Incompatibility

| Field | Value |
|-------|-------|
| **Risk ID** | R-015 |
| **Component** | Jerry Integration |
| **Failure Mode** | Skill doesn't conform to Jerry SKILL.md patterns |
| **Risk Statement** | If skill interface deviates from Jerry conventions, then integration is blocked |
| **Potential Effect** | Cannot deploy as Jerry skill |
| **Root Cause** | Insufficient understanding of Jerry skill patterns |
| **Likelihood** | 2 - Unlikely |
| **L Justification** | Jerry skill patterns are documented; existing skills as exemplars |
| **Consequence** | 3 - Moderate |
| **C Justification** | Rework required; schedule impact |
| **Score** | 6 (GREEN) |
| **Current Controls** | Follow existing skill patterns (worktracker, architecture) |
| **Mitigation Actions** | 1. Review existing Jerry skills before implementation 2. Early integration testing 3. Stakeholder review of SKILL.md |
| **Risk Owner** | Engineering |
| **Residual Risk** | 3 (GREEN) |

##### R-016: Hexagonal Architecture Violations

| Field | Value |
|-------|-------|
| **Risk ID** | R-016 |
| **Component** | Jerry Integration |
| **Failure Mode** | Domain layer has infrastructure dependencies |
| **Risk Statement** | If domain code imports infrastructure (spaCy, file I/O), then architecture tests fail |
| **Potential Effect** | Technical debt; refactoring required |
| **Root Cause** | Developer unfamiliar with hexagonal patterns |
| **Likelihood** | 2 - Unlikely |
| **L Justification** | Architecture rules well-documented; tests enforce boundaries |
| **Consequence** | 2 - Minor |
| **C Justification** | Detected by tests; fixable |
| **Score** | 4 (GREEN) |
| **Current Controls** | Architecture tests in Jerry framework |
| **Mitigation Actions** | 1. Run architecture tests early and often 2. Code review for layer violations |
| **Risk Owner** | Engineering |
| **Residual Risk** | 2 (GREEN) |

---

#### 2.9 Performance Risks

##### R-017: Processing Time Exceeds Targets

| Field | Value |
|-------|-------|
| **Risk ID** | R-017 |
| **Component** | Overall Pipeline |
| **Failure Mode** | Processing takes >10s for typical transcript |
| **Risk Statement** | If pipeline latency exceeds 10s target, then user experience is degraded |
| **Potential Effect** | User frustration; abandonment |
| **Root Cause** | Inefficient NLP processing, model loading time |
| **Likelihood** | 3 - Possible |
| **L Justification** | spaCy model load ~2s; full pipeline needs optimization |
| **Consequence** | 2 - Minor |
| **C Justification** | Progress indication can mitigate; async processing option |
| **Score** | 6 (GREEN) |
| **Current Controls** | Performance targets defined in 5W2H |
| **Mitigation Actions** | 1. Profile and optimize hot paths 2. Lazy model loading 3. Progress bar for long operations 4. Async processing option |
| **Risk Owner** | Engineering |
| **Residual Risk** | 4 (GREEN) |

##### R-018: Memory Exhaustion

| Field | Value |
|-------|-------|
| **Risk ID** | R-018 |
| **Component** | Overall Pipeline |
| **Failure Mode** | Large transcripts exhaust memory |
| **Risk Statement** | If processing very long transcripts (>4 hours), then memory usage may exceed system limits |
| **Potential Effect** | Process crash; data loss |
| **Root Cause** | Loading entire transcript + model + entities in memory |
| **Likelihood** | 2 - Unlikely |
| **L Justification** | MVP targets <500MB for 1-hour transcript; 4-hour is edge case |
| **Consequence** | 3 - Moderate |
| **C Justification** | Crash is bad UX; may lose partial results |
| **Score** | 6 (GREEN) |
| **Current Controls** | Performance targets defined |
| **Mitigation Actions** | 1. Streaming parser for large files 2. Chunked processing with aggregation 3. Memory usage warnings |
| **Risk Owner** | Engineering |
| **Residual Risk** | 3 (GREEN) |

---

#### 2.10 External Dependency Risks

##### R-019: spaCy Model Availability

| Field | Value |
|-------|-------|
| **Risk ID** | R-019 |
| **Component** | NER Pipeline |
| **Failure Mode** | Required spaCy model unavailable or changed |
| **Risk Statement** | If spaCy model (en_core_web_lg) is deprecated or behavior changes, then NER accuracy degrades |
| **Potential Effect** | Broken NER pipeline; regression |
| **Root Cause** | Dependency on external library versioning |
| **Likelihood** | 1 - Rare |
| **L Justification** | spaCy is stable, mature library; models versioned |
| **Consequence** | 3 - Moderate |
| **C Justification** | Would require model migration; testing |
| **Score** | 3 (GREEN) |
| **Current Controls** | Pin dependency versions |
| **Mitigation Actions** | 1. Pin spaCy and model versions 2. Abstract NER interface for swappability 3. Regression tests for NER accuracy |
| **Risk Owner** | Engineering |
| **Residual Risk** | 2 (GREEN) |

##### R-020: LLM API Changes

| Field | Value |
|-------|-------|
| **Risk ID** | R-020 |
| **Component** | LLM Extraction Path |
| **Failure Mode** | LLM API changes break integration |
| **Risk Statement** | If Claude/GPT API changes, then LLM-based extraction fails |
| **Potential Effect** | LLM features unavailable |
| **Root Cause** | Dependency on third-party APIs |
| **Likelihood** | 2 - Unlikely |
| **L Justification** | Major providers maintain backward compatibility |
| **Consequence** | 2 - Minor |
| **C Justification** | LLM is optional enhancement; rule-based fallback exists |
| **Score** | 4 (GREEN) |
| **Current Controls** | LLM is optional; local-first default |
| **Mitigation Actions** | 1. Abstract LLM interface 2. Multiple provider support 3. Graceful degradation to rule-based |
| **Risk Owner** | Engineering |
| **Residual Risk** | 2 (GREEN) |

---

### 3. Risk Summary Tables

#### 3.1 Risk Register Summary

| Risk ID | Component | Failure Mode | L | C | Score | Level | Status |
|---------|-----------|--------------|---|---|-------|-------|--------|
| R-001 | VTT Parser | Format edge cases | 3 | 2 | 6 | GREEN | Accept |
| R-002 | SRT Parser | Timestamp malformation | 4 | 2 | 8 | YELLOW | Mitigate |
| R-003 | Parser | Encoding issues | 3 | 2 | 6 | GREEN | Accept |
| R-004 | Speaker ID | Missing voice tags | 4 | 3 | 12 | YELLOW | Mitigate |
| R-005 | Speaker ID | Name variations | 4 | 2 | 8 | YELLOW | Mitigate |
| R-006 | Action Items | Low precision | 4 | 3 | 12 | YELLOW | Mitigate |
| R-007 | Action Items | Low recall | 3 | 4 | 12 | YELLOW | Mitigate |
| R-008 | Action Items | Hallucination | 3 | 4 | 12 | YELLOW | Mitigate |
| R-009 | Decisions | Implicit decisions | 4 | 2 | 8 | YELLOW | Accept |
| R-010 | Topics | Coherence issues | 3 | 2 | 6 | GREEN | Accept |
| R-011 | CLI | Usability issues | 2 | 2 | 4 | GREEN | Accept |
| R-012 | CLI | Exit codes | 1 | 2 | 2 | GREEN | Accept |
| R-013 | Output | Markdown rendering | 2 | 1 | 2 | GREEN | Accept |
| R-014 | Output | Schema changes | 3 | 3 | 9 | YELLOW | Mitigate |
| R-015 | Jerry | Skill incompatibility | 2 | 3 | 6 | GREEN | Accept |
| R-016 | Jerry | Architecture violations | 2 | 2 | 4 | GREEN | Accept |
| R-017 | Performance | Processing time | 3 | 2 | 6 | GREEN | Accept |
| R-018 | Performance | Memory exhaustion | 2 | 3 | 6 | GREEN | Accept |
| R-019 | Dependencies | spaCy changes | 1 | 3 | 3 | GREEN | Accept |
| R-020 | Dependencies | LLM API changes | 2 | 2 | 4 | GREEN | Accept |

#### 3.2 Risk by Component

```
RISK DISTRIBUTION BY COMPONENT
==============================

Component              Count   Avg Score   Max Score
──────────────────────────────────────────────────────
Action Items             3       12.0        12      ██████████████████ Highest
Speaker Identification   2       10.0        12      ████████████████
Parser (VTT/SRT)         3        6.7         8      ██████████
Output Generation        2        5.5         9      ████████
Topics                   1        6.0         6      ████████
Decisions                1        8.0         8      ████████
Jerry Integration        2        5.0         6      ██████
CLI                      2        3.0         4      ████
Performance              2        6.0         6      ████████
Dependencies             2        3.5         4      ████
──────────────────────────────────────────────────────
Total Risks: 20         Avg: 6.3    Max: 12
```

#### 3.3 5x5 Matrix Visualization (Populated)

```
                            C O N S E Q U E N C E

              │ 1-Minimal │ 2-Minor  │ 3-Moderate │ 4-Major  │ 5-Critical │
    ──────────┼───────────┼──────────┼────────────┼──────────┼────────────┤
L   5-Almost  │           │          │            │          │            │
I    Certain  │           │          │            │          │            │
K   ──────────┼───────────┼──────────┼────────────┼──────────┼────────────┤
E   4-Likely  │           │ R-002    │ R-004      │          │            │
L             │           │ R-005    │ R-006      │          │            │
I   ──────────┼───────────┼──────────┼────────────┼──────────┼────────────┤
H   3-Poss-   │           │ R-001    │ R-014      │ R-007    │            │
O    ible     │           │ R-003    │            │ R-008    │            │
O             │           │ R-010    │            │          │            │
D             │           │ R-017    │            │          │            │
    ──────────┼───────────┼──────────┼────────────┼──────────┼────────────┤
    2-Unlik-  │           │ R-011    │ R-015      │          │            │
     ely      │           │ R-016    │ R-018      │          │            │
              │           │ R-020    │            │          │            │
    ──────────┼───────────┼──────────┼────────────┼──────────┼────────────┤
    1-Rare    │           │ R-012    │ R-019      │          │            │
              │ R-013     │          │            │          │            │
              │           │          │            │          │            │

    Risk Counts: GREEN=15, YELLOW=5, RED=0
```

---

### 4. Mitigation Action Plan

#### 4.1 Priority Mitigations (YELLOW Risks)

| Risk ID | Mitigation | Owner | Target Date | Status |
|---------|------------|-------|-------------|--------|
| R-004 | Implement multi-pattern speaker detection | Eng | Phase 1, Week 2 | Planned |
| R-005 | Build speaker name normalization | Eng | Phase 1, Week 3 | Planned |
| R-006 | Hybrid rule + ML approach | Eng/NLP | Phase 2, Week 2 | Planned |
| R-007 | Multi-strategy extraction | Eng/NLP | Phase 2, Week 2 | Planned |
| R-008 | Citation requirement for LLM extractions | Eng/NLP | Phase 2, Week 3 | Planned |
| R-002 | Timestamp normalization pre-processor | Eng | Phase 1, Week 1 | Planned |
| R-014 | JSON Schema v1 with versioning | Eng | Phase 1, Week 4 | Planned |

#### 4.2 Mitigation Implementation Phases

```
MITIGATION TIMELINE
===================

Phase 1 (Weeks 1-4): Foundation
├── Week 1: R-002 (SRT timestamps)
├── Week 2: R-004 (Speaker patterns)
├── Week 3: R-005 (Name normalization)
└── Week 4: R-014 (Schema versioning)

Phase 2 (Weeks 5-10): Core Extraction
├── Week 5-6: R-006 (Precision), R-007 (Recall)
├── Week 7-8: R-008 (Hallucination mitigation)
└── Week 9-10: Integration testing

Phase 3 (Weeks 11+): Enhancement
└── Continuous improvement based on user feedback
```

---

## L2: Architectural Perspective (Principal Architect)

### 1. Risk Portfolio Analysis

#### 1.1 Systemic Risk Patterns

Three systemic patterns emerge from the FMEA:

```
SYSTEMIC RISK PATTERN #1: NLP Accuracy
======================================
Affects: R-006, R-007, R-008, R-009, R-010

Root Pattern: Extractive NLP on conversational text is inherently
              challenging due to:
              - Implicit information
              - Ambiguous language
              - Context dependency

Architectural Response:
  ┌─────────────────────────────────────────────────────────────┐
  │                  TIERED EXTRACTION STRATEGY                  │
  ├─────────────────────────────────────────────────────────────┤
  │                                                              │
  │  Tier 1: Rule-based (Fast, Deterministic)                   │
  │  └── Patterns, keywords, linguistic markers                 │
  │           │                                                  │
  │           ▼                                                  │
  │  Tier 2: ML-based (Balanced)                                │
  │  └── spaCy NER, fine-tuned classifiers                     │
  │           │                                                  │
  │           ▼                                                  │
  │  Tier 3: LLM-based (High Accuracy, Higher Risk)             │
  │  └── Claude/GPT with citation requirement                   │
  │                                                              │
  │  Each tier provides confidence scores; user chooses level   │
  │                                                              │
  └─────────────────────────────────────────────────────────────┘


SYSTEMIC RISK PATTERN #2: Input Variability
==========================================
Affects: R-001, R-002, R-003, R-004

Root Pattern: Transcript files vary significantly due to:
              - Multiple format variations
              - No enforcement of standards
              - Different transcription tools

Architectural Response:
  ┌─────────────────────────────────────────────────────────────┐
  │               DEFENSIVE PARSING ARCHITECTURE                 │
  ├─────────────────────────────────────────────────────────────┤
  │                                                              │
  │  Input File → Format Detection → Normalization → Canonical  │
  │                     │                              │         │
  │                     ▼                              ▼         │
  │              ┌──────────────┐           ┌──────────────┐    │
  │              │ Error        │           │ Unified      │    │
  │              │ Recovery     │           │ Transcript   │    │
  │              │ & Logging    │           │ Model        │    │
  │              └──────────────┘           └──────────────┘    │
  │                                                              │
  │  Principle: Accept liberally, process consistently          │
  │                                                              │
  └─────────────────────────────────────────────────────────────┘


SYSTEMIC RISK PATTERN #3: Schema Evolution
==========================================
Affects: R-014, R-015

Root Pattern: Output schemas and interfaces will evolve as
              features are added and user feedback incorporated

Architectural Response:
  ┌─────────────────────────────────────────────────────────────┐
  │                 VERSIONED INTERFACE STRATEGY                 │
  ├─────────────────────────────────────────────────────────────┤
  │                                                              │
  │  JSON Output:                                               │
  │  {                                                           │
  │    "version": "1.0",                                        │
  │    "schema": "transcript-skill/v1",                         │
  │    "data": { ... }                                          │
  │  }                                                           │
  │                                                              │
  │  SKILL.md Interface:                                         │
  │  - Version in metadata                                       │
  │  - Backward compatibility guarantees documented              │
  │                                                              │
  │  Breaking changes trigger major version bump                │
  │                                                              │
  └─────────────────────────────────────────────────────────────┘
```

#### 1.2 Risk Correlation Analysis

```
RISK CORRELATION MATRIX
=======================

         R-004  R-005  R-006  R-007  R-008  R-014
R-004     -     HIGH   MED    LOW    LOW    LOW
R-005           -      LOW    LOW    LOW    LOW
R-006                  -      HIGH   MED    MED
R-007                         -      MED    MED
R-008                                -      MED
R-014                                       -

Correlation Clusters:
1. Speaker Cluster: R-004 ↔ R-005 (high correlation)
   - Mitigation synergy: Unified speaker handling module

2. Action Item Cluster: R-006 ↔ R-007 ↔ R-008 (high correlation)
   - Mitigation synergy: Single extraction pipeline with tuning

3. Output Cluster: R-006/R-007/R-008 → R-014 (dependency)
   - Schema must accommodate extraction results
```

### 2. Design Implications from FMEA

#### 2.1 Architectural Decisions Driven by Risk

| Risk Pattern | Architectural Decision | ADR Reference |
|--------------|------------------------|---------------|
| NLP Accuracy | Tiered extraction with confidence scores | ADR-003 (8D Analysis) |
| Input Variability | Canonical transcript model + format adapters | ADR-001 (8D Analysis) |
| Schema Evolution | Versioned output from v1.0 | ADR-004 (new) |
| Hallucination | Citation requirement for LLM extractions | ADR-005 (new) |

#### 2.2 One-Way Door Decisions Affected

| Decision | Risk Influence | Recommendation |
|----------|----------------|----------------|
| Extraction strategy | R-006, R-007, R-008 | Tiered approach is reversible; proceed |
| Output schema | R-014 | Version from start; proceed with caution |
| LLM integration | R-008, R-020 | Abstract interface; proceed with abstraction |

#### 2.3 Performance Implications

```
PERFORMANCE BUDGET WITH RISK ALLOWANCE
======================================

Component               Target    Worst Case    Risk Buffer
──────────────────────────────────────────────────────────────
VTT/SRT Parsing        100ms      500ms         +400ms (R-001/R-002)
Speaker Extraction     200ms      1000ms        +800ms (R-004/R-005)
Standard NER           2000ms     3000ms        +1000ms
Custom NER (rule)      1000ms     2000ms        +1000ms
Custom NER (ML)        3000ms     5000ms        +2000ms (R-006/R-007)
Custom NER (LLM)       5000ms     15000ms       +10000ms (R-008)
Output Generation      100ms      500ms         +400ms
──────────────────────────────────────────────────────────────
Total (rule-based)     3400ms     7000ms        Within 10s target
Total (LLM path)       7400ms     20500ms       May exceed target

Mitigation: Progress indication for LLM path; async option
```

### 3. Risk Monitoring Strategy

#### 3.1 Key Risk Indicators (KRIs)

| KRI | Risk(s) | Threshold | Action |
|-----|---------|-----------|--------|
| Action Item F1 Score | R-006, R-007 | <0.75 | Tune models, add patterns |
| Hallucination Rate | R-008 | >2% | Strengthen citation validation |
| Parse Failure Rate | R-001, R-002 | >5% | Expand edge case handling |
| Speaker Match Rate | R-004, R-005 | <80% | Add pattern detection |
| Processing Time P95 | R-017 | >10s | Optimize pipeline |

#### 3.2 Risk Review Cadence

```
RISK REVIEW SCHEDULE
====================

Weekly (During Development):
- Review any triggered KRIs
- Update mitigation status
- Assess new risks from implementation

Sprint End:
- Update risk scores based on new evidence
- Verify mitigation effectiveness
- Adjust priorities if needed

Phase Transition:
- Comprehensive FMEA review
- Update residual risks
- Document lessons learned
```

### 4. Tradeoff Analysis

#### 4.1 Risk vs. Feature Scope

```
RISK-FEATURE TRADEOFF CURVE
===========================

Risk     │
Score    │        ● Real-time Processing
    25   │      ●
         │    ●   Meeting Summary (LLM)
    20   │  ●
         │●     Action Items (LLM)
    15   ├───────────────────────────────── Risk Threshold (YELLOW)
         │        ● Action Items (ML)
    12   │      ●
         │    ●   Speaker ID (pattern)
    10   │
         │  ●     VTT/SRT Parsing
     5   │●       CLI Interface
         └────────────────────────────────────────
              P0    P1    P2    P3         Priority

Decision: MVP includes everything P0-P1 with YELLOW risk acceptance
          P2+ features (Summary, Real-time) deferred due to risk
```

#### 4.2 Accuracy vs. Risk Tradeoff

| Extraction Method | Accuracy | Risk | Recommendation |
|-------------------|----------|------|----------------|
| Rule-based | 70-75% | LOW | MVP default |
| ML (fine-tuned) | 80-85% | MEDIUM | Phase 2 enhancement |
| LLM (prompted) | 85-90% | MEDIUM-HIGH | Opt-in, with citations |
| LLM (fine-tuned) | 90-94% | HIGH | Future consideration |

### 5. Risk-Informed Requirements

Based on FMEA findings, the following requirements are added/modified:

| Req ID | Requirement | Originating Risk |
|--------|-------------|------------------|
| NFR-001 | Parser SHALL handle both . and , timestamp separators | R-002 |
| NFR-002 | System SHALL detect and convert non-UTF8 encodings | R-003 |
| NFR-003 | Speaker extraction SHALL support 4+ naming patterns | R-004 |
| NFR-004 | Action item extraction SHALL include confidence scores | R-006 |
| NFR-005 | LLM extractions SHALL include source transcript citations | R-008 |
| NFR-006 | JSON output SHALL include schema version | R-014 |
| NFR-007 | Processing SHALL complete in <10s for 1-hour transcript | R-017 |

---

## References

### Input Sources

| Source | Analysis Type | Key Risk Inputs |
|--------|---------------|-----------------|
| 5W2H-ANALYSIS.md | Scope Definition | Component boundaries, performance targets |
| ISHIKAWA-DIAGRAM.md | Root Cause | Systemic patterns, format fragmentation |
| 8D-PROBLEM-SOLVING.md | Corrective Actions | Mitigation strategies, ADR references |
| PARETO-ANALYSIS.md | Prioritization | Risk concentration by feature |
| FEATURE-MATRIX.md | Market Analysis | Competitive gaps, feature risks |
| NLP-NER-BEST-PRACTICES.md | Technical Standards | NLP accuracy benchmarks |
| ACADEMIC-LITERATURE-REVIEW.md | Research | F1 scores, hallucination rates |
| VTT-SPECIFICATION.md | Format Standard | Parsing edge cases |
| SRT-SPECIFICATION.md | Format Standard | Timestamp variations |

### Risk Management Standards

| Standard | Application |
|----------|-------------|
| NPR 8000.4C | NASA Risk Management Program Requirements |
| NPR 7123.1D | NASA Systems Engineering Processes and Requirements |
| ISO 31000:2018 | Risk Management Guidelines |
| IEC 60812:2018 | FMEA Methodology Standard |

### Academic References

| Reference | Risk Input |
|-----------|------------|
| Baruah et al. (2024) | Action item F1 benchmarks (0.13-0.94) |
| Blagec et al. (2025) | Hallucination rates (1.5-8.0%) |
| AMI Corpus | Meeting transcript ground truth |

---

## Appendix A: Risk Assessment Worksheets

### A.1 Blank Risk Assessment Template

```
Risk ID: R-XXX
Component:
Failure Mode:
Risk Statement: If [condition], then [consequence]
Potential Effect:
Root Cause:
Likelihood: (1-5)
L Justification:
Consequence: (1-5)
C Justification:
Score: (L x C)
Current Controls:
Mitigation Actions:
Risk Owner:
Residual Risk:
```

### A.2 Risk Status Codes

| Status | Definition |
|--------|------------|
| Open | Risk identified, not yet addressed |
| Mitigate | Active mitigation in progress |
| Accept | Risk accepted at current level |
| Transfer | Risk transferred to another party |
| Closed | Risk no longer applicable |

---

## Appendix B: Glossary

| Term | Definition |
|------|------------|
| FMEA | Failure Mode and Effects Analysis |
| Likelihood | Probability of failure mode occurrence |
| Consequence | Severity of impact if failure occurs |
| Risk Score | Likelihood x Consequence |
| Mitigation | Action to reduce likelihood or consequence |
| Residual Risk | Risk remaining after mitigation |
| KRI | Key Risk Indicator |

---

## Document History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-01-25 | nse-risk agent | Initial FMEA complete |

---

*End of FMEA Analysis Document*
