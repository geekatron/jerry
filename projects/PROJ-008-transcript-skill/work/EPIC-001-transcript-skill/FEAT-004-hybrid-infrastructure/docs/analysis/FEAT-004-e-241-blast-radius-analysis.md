# FEAT-004-e-241: Blast Radius Analysis for Hybrid Infrastructure Transformation

<!--
TEMPLATE: Analysis
VERSION: 1.0
SOURCE: docs/knowledge/exemplars/templates/analysis.md
CREATED: 2026-01-29
PURPOSE: Analyze blast radius for hybrid architecture transformation
-->

> **Document ID:** FEAT-004-e-241
> **PS ID:** FEAT-004
> **Entry ID:** e-241
> **Type:** Analysis (Impact Assessment)
> **Status:** COMPLETE
> **Agent:** ps-analyst v2.0.0
> **Created:** 2026-01-29T22:00:00Z

---

## L0: Executive Summary (ELI5)

Imagine you're renovating a kitchen in a house. Before you start knocking down walls, you need to know: "What else will be affected?" Will removing this wall damage the plumbing? Will it affect the electrical wiring? This is called a "blast radius" - understanding how far the impact of a change spreads.

Our transcript skill has a problem: when it tries to read a really long meeting transcript (like a 5-hour all-hands meeting), it loses 99.8% of the content - like reading a 500-page book and only remembering 1 page! The solution is to add a "helper" (Python) that's really good at the mechanical work (reading and organizing the pages), while our AI assistant (Claude) focuses on understanding and summarizing the content.

**Key Impact Summary:**

| Impact Level | Components Affected | Risk Level |
|--------------|---------------------|------------|
| **MAJOR** | ts-parser.md (role transformation) | HIGH |
| **MODERATE** | SKILL.md, ts-extractor.md | MEDIUM |
| **NEW** | 4 new enablers (EN-020..023) | MEDIUM |
| **EXTEND** | Test infrastructure | LOW |

**Bottom Line:** This is a significant architectural change that transforms how we process transcripts, but with proper phasing and fallback strategies, the risk is manageable.

---

## L1: Technical Analysis (Software Engineer)

### Blast Radius Assessment

#### Component Impact Matrix

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                    BLAST RADIUS HEAT MAP                                         │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                  │
│   ████ CRITICAL IMPACT (Transformation Required)                                │
│   ▓▓▓▓ MODERATE IMPACT (Interface Changes)                                      │
│   ░░░░ LOW IMPACT (Extension Only)                                              │
│   .... NO IMPACT (Unchanged)                                                     │
│                                                                                  │
│   ┌─────────────────────────────────────────────────────────────────────────┐   │
│   │  ORCHESTRATION LAYER                                                     │   │
│   │  ┌──────────────┐  ┌──────────────┐                                     │   │
│   │  │ ▓▓ SKILL.md ▓▓│  │ .... PLAYBOOK │                                    │   │
│   │  │   Pipeline   │  │    Unchanged  │                                     │   │
│   │  │   Update     │  │              │                                     │   │
│   │  └──────────────┘  └──────────────┘                                     │   │
│   └─────────────────────────────────────────────────────────────────────────┘   │
│                                    │                                             │
│                                    ▼                                             │
│   ┌─────────────────────────────────────────────────────────────────────────┐   │
│   │  AGENT LAYER                                                             │   │
│   │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐                   │   │
│   │  │████ ts-parser ███│  │▓▓ ts-extractor▓│  │.... ts-formatter│            │   │
│   │  │  MAJOR ROLE  │  │  MODERATE    │  │   Unchanged  │                   │   │
│   │  │  TRANSFORM   │  │  Interface   │  │              │                   │   │
│   │  └──────────────┘  └──────────────┘  └──────────────┘                   │   │
│   └─────────────────────────────────────────────────────────────────────────┘   │
│                                    │                                             │
│                                    ▼                                             │
│   ┌─────────────────────────────────────────────────────────────────────────┐   │
│   │  NEW INFRASTRUCTURE LAYER (EN-020..023)                                  │   │
│   │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌────────────┐   │   │
│   │  │████ Python   ████│  │████ Chunking ████│  │▓▓ Extractor ▓▓│  │░░ Testing░░│   │
│   │  │   Parser     │  │   Strategy   │  │  Adaptation  │  │   Suite   │   │   │
│   │  │   EN-020     │  │   EN-021     │  │   EN-022     │  │  EN-023   │   │   │
│   │  └──────────────┘  └──────────────┘  └──────────────┘  └────────────┘   │   │
│   └─────────────────────────────────────────────────────────────────────────┘   │
│                                                                                  │
└─────────────────────────────────────────────────────────────────────────────────┘
```

#### Detailed Component Analysis

| Component | File Path | Change Type | Impact | Complexity | Risk |
|-----------|-----------|-------------|--------|------------|------|
| **ts-parser.md** | `skills/transcript/agents/ts-parser.md` | **MAJOR TRANSFORM** | HIGH | HIGH | MEDIUM |
| **SKILL.md** | `skills/transcript/SKILL.md` | MODERATE UPDATE | MEDIUM | MEDIUM | LOW |
| **ts-extractor.md** | `skills/transcript/agents/ts-extractor.md` | MODERATE INTERFACE | MEDIUM | MEDIUM | LOW |
| **ts-formatter.md** | `skills/transcript/agents/ts-formatter.md` | UNCHANGED | NONE | NONE | NONE |
| **EN-020** | NEW | Python VTT Parser | HIGH | HIGH | MEDIUM |
| **EN-021** | NEW | Chunking Strategy | HIGH | MEDIUM | MEDIUM |
| **EN-022** | NEW | Extractor Adaptation | MEDIUM | LOW | LOW |
| **EN-023** | NEW | Integration Testing | MEDIUM | MEDIUM | LOW |
| **Test specs** | `skills/transcript/test_data/` | EXTEND | MEDIUM | MEDIUM | LOW |

### Dependency Graph

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                         DEPENDENCY FLOW DIAGRAM                                  │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                  │
│    ┌─────────────────────────────────────────────────────────────────────────┐  │
│    │  UPSTREAM DEPENDENCIES (Inputs to FEAT-004)                              │  │
│    │                                                                          │  │
│    │  ┌───────────────┐  ┌───────────────┐  ┌───────────────┐               │  │
│    │  │   DISC-009    │  │   DEC-011     │  │   ADR-001     │               │  │
│    │  │ Root Cause    │  │ Role Decision │  │ Agent Arch    │               │  │
│    │  │ 99.8% Loss    │──▶│ Strategy Pat │──▶│ Amendment     │               │  │
│    │  └───────────────┘  └───────────────┘  └───────────────┘               │  │
│    └─────────────────────────────────────────────────────────────────────────┘  │
│                                      │                                           │
│                                      ▼                                           │
│    ┌─────────────────────────────────────────────────────────────────────────┐  │
│    │                         FEAT-004 CORE                                    │  │
│    │                                                                          │  │
│    │     ┌─────────────────────────────────────────────────────────────┐     │  │
│    │     │                  ts-parser.md (Orchestrator)                 │     │  │
│    │     │                                                              │     │  │
│    │     │   ┌───────────────────────────────────────────────────────┐ │     │  │
│    │     │   │                 Strategy Selection                      │ │     │  │
│    │     │   │  ┌─────────────┐         ┌─────────────┐              │ │     │  │
│    │     │   │  │   Python    │         │    LLM      │              │ │     │  │
│    │     │   │  │  Strategy   │    OR   │  Strategy   │              │ │     │  │
│    │     │   │  │  (VTT/SRT)  │         │  (Fallback) │              │ │     │  │
│    │     │   │  └──────┬──────┘         └──────┬──────┘              │ │     │  │
│    │     │   └─────────┼───────────────────────┼──────────────────────┘ │     │  │
│    │     └─────────────┼───────────────────────┼────────────────────────┘     │  │
│    │                   │                       │                               │  │
│    │                   ▼                       ▼                               │  │
│    │     ┌─────────────────────────┐  ┌─────────────────────────┐            │  │
│    │     │      EN-020             │  │   (Current LLM Parser)  │            │  │
│    │     │   Python Parser         │  │      Fallback Only      │            │  │
│    │     │   (webvtt-py)           │  │                         │            │  │
│    │     └───────────┬─────────────┘  └─────────────────────────┘            │  │
│    │                 │                                                        │  │
│    │                 ▼                                                        │  │
│    │     ┌─────────────────────────┐                                         │  │
│    │     │      EN-021             │                                         │  │
│    │     │   Chunking Strategy     │                                         │  │
│    │     │   index.json + chunks/  │                                         │  │
│    │     └───────────┬─────────────┘                                         │  │
│    │                 │                                                        │  │
│    └─────────────────┼────────────────────────────────────────────────────────┘  │
│                      │                                                           │
│                      ▼                                                           │
│    ┌─────────────────────────────────────────────────────────────────────────┐  │
│    │  DOWNSTREAM DEPENDENCIES (Outputs from FEAT-004)                         │  │
│    │                                                                          │  │
│    │  ┌───────────────┐  ┌───────────────┐  ┌───────────────┐               │  │
│    │  │  EN-022       │  │ ts-extractor  │  │ ts-formatter  │               │  │
│    │  │ Extractor     │──▶│ (Chunked     │──▶│ (Unchanged)   │               │  │
│    │  │ Adaptation    │  │  Input)       │  │               │               │  │
│    │  └───────────────┘  └───────────────┘  └───────────────┘               │  │
│    │                                                                          │  │
│    │  ┌───────────────┐                                                      │  │
│    │  │  EN-023       │                                                      │  │
│    │  │ Integration   │                                                      │  │
│    │  │ Testing       │                                                      │  │
│    │  └───────────────┘                                                      │  │
│    └─────────────────────────────────────────────────────────────────────────┘  │
│                                                                                  │
└─────────────────────────────────────────────────────────────────────────────────┘
```

### 5W2H Analysis

| Dimension | Finding | Evidence |
|-----------|---------|----------|
| **WHAT** | Transform ts-parser.md from direct LLM parser to orchestrator using Strategy Pattern. Add Python parsing layer (webvtt-py) with chunking infrastructure. | DEC-011 D-001: "ts-parser.md serves as orchestrator, delegator, fallback, and validator" [FEAT-004-hybrid-infrastructure.md] |
| **WHY** | DISC-009 incident: 99.8% data loss (5 segments extracted from 3,071 in 90K token file). "Lost in the Middle" phenomenon causes >30% accuracy degradation for information in the middle of long contexts. | Liu et al. (2024): "Performance can degrade by more than 30% when information shifts from extremes to middle" [Phase 1 Research, Section RQ-4] |
| **WHO** | **Implementation:** Claude Code agent. **Approval:** User (GATE-5). **Affected:** All transcript skill users processing files >31.5K tokens. | FEAT-004-hybrid-infrastructure.md: "Owner: Claude" |
| **WHEN** | After TDD-FEAT-004 approval (GATE-5). MVP scope: VTT format only. SRT and plain text in future phases. | DEC-011 D-002: "Python format support added incrementally (VTT first via webvtt-py)" |
| **WHERE** | **Agents:** `skills/transcript/agents/ts-parser.md`, `skills/transcript/agents/ts-extractor.md`. **New Python:** `skills/transcript/src/`. **Tests:** `skills/transcript/test_data/`. | FEAT-004-hybrid-infrastructure.md Section "Architecture Overview" |
| **HOW** | Strategy Pattern: Format detection routes to Python parser (VTT/SRT) or LLM fallback (unknown formats). Chunking: 500-segment chunks with index.json overview. | Phase 1 Research Section RQ-1: "Strategy Pattern provides architectural foundation for hybrid LLM/Python systems" [Refactoring Guru citation] |
| **HOW MUCH** | **4 enablers** (EN-020..023). **Estimated 20-25 tasks** based on template decomposition. **Parse cost savings:** $0 (Python) vs $0.27 (LLM). **Speed:** <1s (Python) vs 60s+ (LLM). **Accuracy:** 100% vs 0.2%. | Phase 1 Research Section RQ-6: Cost Analysis table; DISC-009 metrics |

### Ishikawa Root Cause Analysis

```
┌─────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                              ISHIKAWA DIAGRAM: WHY HYBRID IS NEEDED                                  │
├─────────────────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                                      │
│                                              ┌────────────────────┐                                 │
│      METHODS                                 │   PROBLEM:         │                    MACHINES    │
│      ────────                                │   99.8% Data Loss  │                    ─────────   │
│                                              │   in Large         │                                 │
│   LLM-only parsing ──────────────────────────│   Transcripts      │────────────── Python stdlib   │
│   limitations                                │                    │               not leveraged     │
│        │                                     └─────────┬──────────┘                     │          │
│        │                                               │                                │          │
│   No deterministic ────────────────────────────────────┼───────────────────── webvtt-py │          │
│   fallback                                             │                     available  │          │
│        │                                               │                                │          │
│        │                                               │                                │          │
│   ─────┼───────────────────────────────────────────────┼────────────────────────────────┼──────    │
│        │                                               │                                │          │
│        │                                               │                                │          │
│   VTT format ────────────────────────────────────────────────────────────────── No hybrid │          │
│   characteristics                                      │                     architecture │          │
│   well-defined                                         │                                │          │
│        │                                               │                                │          │
│        │                                               │                                │          │
│   ─────┼───────────────────────────────────────────────┼────────────────────────────────┼──────    │
│        │                                               │                                │          │
│        │                                               │                                │          │
│   90K tokens ──────────────────────────────────────────┼───────────────────────────────────────     │
│   exceeds limits                                       │                                           │
│        │                                               │                                           │
│        │                                               │                                           │
│   Lost-in-Middle ──────────────────────────────────────┼────────────── Agent-only design ─────     │
│   phenomenon                                           │               per ADR-001                  │
│        │                                               │                     │                      │
│   ─────┼───────────────────────────────────────────────┼─────────────────────┼──────────────────    │
│        │                                               │                     │                      │
│                                                        │                                            │
│      MATERIALS                      MEASUREMENT             ENVIRONMENT                             │
│      ──────────                     ───────────             ───────────                             │
│                                                                                                      │
│   Legend:                                                                                           │
│   ────── = Causal relationship                                                                      │
│   ────────────────────────────────────────────────────────────────────────────────────────────────  │
│                                                                                                      │
│   ROOT CAUSES IDENTIFIED:                                                                           │
│   ━━━━━━━━━━━━━━━━━━━━━━━                                                                          │
│   1. LLM context window limitations (MATERIALS: 90K tokens > limits)                                │
│   2. Lost-in-Middle phenomenon (MATERIALS: >30% degradation documented)                            │
│   3. No Python preprocessing layer (MACHINES: webvtt-py available but unused)                      │
│   4. Agent-only architecture (ENVIRONMENT: ADR-001 original design)                                │
│   5. No deterministic fallback (METHODS: LLM is probabilistic)                                     │
│                                                                                                      │
└─────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## L2: Architectural Implications (Principal Architect)

### FMEA Risk Assessment

| ID | Failure Mode | Severity (1-10) | Occurrence (1-10) | Detection (1-10) | RPN | Mitigation Strategy |
|----|--------------|-----------------|-------------------|------------------|-----|---------------------|
| FM-001 | Python parser crashes on malformed VTT | 7 | 3 | 2 | **42** | LLM fallback strategy; defensive parsing per PAT-002 |
| FM-002 | Format detection fails to identify VTT | 6 | 2 | 2 | **24** | Multi-pattern detection (WEBVTT header + timestamp pattern) |
| FM-003 | Chunk boundary corrupts semantic meaning | 8 | 4 | 4 | **128** | Segment-boundary chunking (500 segments = natural breaks) |
| FM-004 | Extractor can't handle chunked input | 7 | 3 | 3 | **63** | EN-022 interface adaptation; index-based navigation |
| FM-005 | Backward compatibility breaks | 9 | 2 | 3 | **54** | Incremental migration; maintain LLM parser as fallback |
| FM-006 | webvtt-py library has breaking update | 5 | 2 | 5 | **50** | Pin version in requirements; integration tests |
| FM-007 | Index.json file corruption | 7 | 2 | 2 | **28** | JSON schema validation; atomic writes |
| FM-008 | Encoding detection fails | 6 | 3 | 3 | **54** | charset-normalizer fallback chain (4-5x faster than chardet) |
| FM-009 | Memory exhaustion on large files | 8 | 2 | 3 | **48** | Streaming parse pattern; 100MB memory limit per NFR |
| FM-010 | Lost-in-Middle in chunked extraction | 5 | 3 | 5 | **75** | Each chunk is small enough (15-20K tokens); no middle region |

**RPN Interpretation:**
- **>100 (CRITICAL):** FM-003 - Chunk boundary corruption requires careful attention
- **50-100 (HIGH):** FM-010, FM-004, FM-005, FM-008 - Need mitigation plans
- **<50 (MEDIUM/LOW):** Acceptable with standard practices

**Risk Priority Number (RPN) Formula:** Severity x Occurrence x Detection
- Severity: 1 (minor) to 10 (catastrophic)
- Occurrence: 1 (remote) to 10 (very high)
- Detection: 1 (almost certain) to 10 (undetectable)

### Gap Mapping Matrix: DISC-009 to Implementation

| DISC-009 Finding | Gap Description | Implementation Requirement | Enabler | Priority | Dependencies |
|------------------|-----------------|---------------------------|---------|----------|--------------|
| 99.8% data loss (5/3071 segments) | LLM cannot reliably process all segments in large transcripts | Python parser extracts ALL segments deterministically | **EN-020** | P0 | None |
| Ad-hoc workaround violation | No formal strategy for handling large files | Index + chunk architecture with formal specification | **EN-021** | P0 | EN-020 |
| No scalability solution | Current architecture has hard limits | Chunking enables ANY size transcript | **EN-021** | P0 | EN-020 |
| LLM parsing insufficient | Probabilistic parsing fails at scale | Strategy Pattern: Python primary, LLM fallback | **ts-parser.md** | P0 | EN-020 |
| Extractor assumes full input | Cannot process chunked transcripts | Chunked input interface with index navigation | **EN-022** | P1 | EN-021 |
| No integration testing | End-to-end validation missing | Integration test framework with large file tests | **EN-023** | P1 | EN-020, EN-021, EN-022 |
| Lost-in-Middle phenomenon | Information in middle of context degraded | Chunking prevents middle-position; each chunk is complete context | **EN-021** | P0 | EN-020 |
| 60s+ processing time | Pure LLM parsing is slow | Python parsing <1s for any size file | **EN-020** | P0 | None |
| $0.27/file parsing cost | Token cost for large files | $0 Python parsing cost | **EN-020** | P0 | None |

### Enabler Dependency Analysis

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                        ENABLER DEPENDENCY GRAPH                                  │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                  │
│   PHASE 1: Foundation                                                           │
│   ═══════════════════                                                           │
│                                                                                  │
│   ┌─────────────────────────────────────────────────────────────────────────┐   │
│   │  EN-020: Python Parser Implementation                                    │   │
│   │  ─────────────────────────────────────                                   │   │
│   │  • webvtt-py integration                                                │   │
│   │  • Encoding detection (charset-normalizer)                              │   │
│   │  • Format-specific routing logic                                        │   │
│   │  • Output: canonical-transcript.json                                    │   │
│   │                                                                          │   │
│   │  Estimated Tasks: 6-8                                                   │   │
│   │  Complexity: HIGH                                                       │   │
│   │  Dependencies: None (foundation)                                        │   │
│   └─────────────────────────┬───────────────────────────────────────────────┘   │
│                             │                                                    │
│                             │ BLOCKS                                             │
│                             ▼                                                    │
│   PHASE 2: Chunking                                                             │
│   ═════════════════                                                             │
│                                                                                  │
│   ┌─────────────────────────────────────────────────────────────────────────┐   │
│   │  EN-021: Chunking Strategy                                               │   │
│   │  ─────────────────────────                                               │   │
│   │  • Index file generation (index.json)                                   │   │
│   │  • Chunk file creation (chunk-NNN.json)                                 │   │
│   │  • 500-segment chunk sizing                                             │   │
│   │  • Semantic boundary detection (future)                                 │   │
│   │                                                                          │   │
│   │  Estimated Tasks: 5-6                                                   │   │
│   │  Complexity: MEDIUM                                                     │   │
│   │  Dependencies: EN-020 (needs parsed segments)                           │   │
│   └─────────────────────────┬───────────────────────────────────────────────┘   │
│                             │                                                    │
│                             │ BLOCKS                                             │
│                             ▼                                                    │
│   PHASE 3: Adaptation                                                           │
│   ═══════════════════                                                           │
│                                                                                  │
│   ┌─────────────────────────────────────────────────────────────────────────┐   │
│   │  EN-022: Extractor Adaptation                                            │   │
│   │  ───────────────────────────                                             │   │
│   │  • ts-extractor interface update                                        │   │
│   │  • Index-based navigation logic                                         │   │
│   │  • Chunk selection strategy                                             │   │
│   │  • Result aggregation across chunks                                     │   │
│   │                                                                          │   │
│   │  Estimated Tasks: 4-5                                                   │   │
│   │  Complexity: LOW                                                        │   │
│   │  Dependencies: EN-021 (needs chunked output)                            │   │
│   └─────────────────────────┬───────────────────────────────────────────────┘   │
│                             │                                                    │
│                             │ BLOCKS                                             │
│                             ▼                                                    │
│   PHASE 4: Validation                                                           │
│   ═══════════════════                                                           │
│                                                                                  │
│   ┌─────────────────────────────────────────────────────────────────────────┐   │
│   │  EN-023: Integration Testing                                             │   │
│   │  ──────────────────────────                                              │   │
│   │  • End-to-end pipeline tests                                            │   │
│   │  • Large file validation (meeting-006-all-hands.vtt)                   │   │
│   │  • Fallback path testing                                                │   │
│   │  • Performance benchmarks                                               │   │
│   │                                                                          │   │
│   │  Estimated Tasks: 5-6                                                   │   │
│   │  Complexity: MEDIUM                                                     │   │
│   │  Dependencies: EN-020, EN-021, EN-022 (tests all layers)               │   │
│   └─────────────────────────────────────────────────────────────────────────┘   │
│                                                                                  │
│   TOTAL ESTIMATED TASKS: 20-25                                                  │
│   CRITICAL PATH: EN-020 → EN-021 → EN-022 → EN-023                             │
│                                                                                  │
└─────────────────────────────────────────────────────────────────────────────────┘
```

### Migration Risk Assessment

#### Backward Compatibility Analysis

| Concern | Risk Level | Mitigation | Validation |
|---------|------------|------------|------------|
| Existing small transcripts (<31.5K tokens) | LOW | LLM path still works; Python path produces same output format | Regression tests with existing test files |
| ts-extractor input format change | MEDIUM | Index + chunk format is additive; can detect and handle both formats | Contract tests per EN-022 |
| SKILL.md orchestration changes | LOW | Pipeline steps unchanged; internal implementation different | End-to-end skill invocation tests |
| Output schema compatibility | LOW | canonical-transcript.json schema unchanged | JSON Schema validation |
| Performance regression | LOW | Python parsing is faster; only extractor iteration changes | Performance benchmarks per EN-023 |

#### Rollback Strategy

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                           ROLLBACK DECISION TREE                                 │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                  │
│                    ┌─────────────────────────┐                                  │
│                    │  Hybrid Architecture    │                                  │
│                    │  Deployed               │                                  │
│                    └───────────┬─────────────┘                                  │
│                                │                                                 │
│                                ▼                                                 │
│              ┌─────────────────────────────────┐                                │
│              │  Is Python parser working?      │                                │
│              └─────────────┬──────────┬────────┘                                │
│                            │          │                                          │
│                       YES  │          │ NO                                       │
│                            │          │                                          │
│              ┌─────────────┘          └─────────────┐                           │
│              │                                      │                            │
│              ▼                                      ▼                            │
│   ┌──────────────────────┐           ┌──────────────────────────┐              │
│   │  Continue with       │           │  Automatic LLM Fallback  │              │
│   │  Python Strategy     │           │  ts-parser.md routes     │              │
│   └──────────────────────┘           │  to original LLM parser  │              │
│                                      └───────────┬──────────────┘              │
│                                                  │                              │
│                                                  ▼                              │
│                               ┌──────────────────────────────────┐             │
│                               │  Is fallback sufficient?         │             │
│                               └─────────────┬───────────┬────────┘             │
│                                             │           │                       │
│                                        YES  │           │ NO                    │
│                                             │           │                       │
│                               ┌─────────────┘           └─────────────┐        │
│                               │                                       │         │
│                               ▼                                       ▼         │
│                   ┌──────────────────────┐         ┌──────────────────────┐    │
│                   │  Log issue and       │         │  ROLLBACK:           │    │
│                   │  continue operation  │         │  Revert ts-parser.md │    │
│                   └──────────────────────┘         │  to v1.2.0           │    │
│                                                    └──────────────────────┘    │
│                                                                                 │
│   KEY ROLLBACK ACTIONS:                                                        │
│   ─────────────────────                                                        │
│   1. git revert to pre-FEAT-004 commit                                         │
│   2. Remove skills/transcript/src/ directory                                   │
│   3. Restore ts-parser.md v1.2.0                                               │
│   4. Maintain chunking infra for future retry                                  │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────┘
```

### ts-parser.md Role Transformation

#### Current State (v1.2.0)

```
ts-parser.md (v1.2.0) - DIRECT PARSER
═════════════════════════════════════

┌─────────────────────────────────────────────────────────────────────┐
│  INPUT: Raw transcript file (VTT/SRT/TXT)                          │
│                                                                     │
│  PROCESSING:                                                        │
│  • Format detection (regex-based)                                  │
│  • LLM parsing of entire content                                   │
│  • Timestamp normalization                                          │
│  • Speaker extraction                                               │
│                                                                     │
│  OUTPUT: canonical-transcript.json                                  │
│                                                                     │
│  LIMITATIONS:                                                       │
│  ✗ Context window limits (90K tokens fails)                        │
│  ✗ Lost-in-Middle degradation                                      │
│  ✗ Probabilistic accuracy                                           │
│  ✗ Slow processing (60s+ for large files)                          │
│  ✗ High token cost ($0.27/file)                                    │
└─────────────────────────────────────────────────────────────────────┘
```

#### Future State (v2.0.0 - Post FEAT-004)

```
ts-parser.md (v2.0.0) - ORCHESTRATOR/DELEGATOR/FALLBACK/VALIDATOR
═════════════════════════════════════════════════════════════════

┌─────────────────────────────────────────────────────────────────────┐
│  INPUT: Raw transcript file (VTT/SRT/TXT)                          │
│                                                                     │
│  ROLE 1: ORCHESTRATOR                                               │
│  • Detect format from file content                                 │
│  • Select appropriate strategy                                      │
│  • Coordinate parsing pipeline                                      │
│                                                                     │
│  ROLE 2: DELEGATOR                                                  │
│  • Route VTT → Python parser (EN-020)                              │
│  • Route SRT → Python parser (future)                              │
│  • Route unknown → LLM parser (fallback)                           │
│                                                                     │
│  ROLE 3: FALLBACK                                                   │
│  • If Python parser fails → invoke LLM parser                      │
│  • Maintain original parsing capability                             │
│                                                                     │
│  ROLE 4: VALIDATOR                                                  │
│  • Validate Python parser output schema                            │
│  • Verify segment count matches expectations                        │
│  • Check encoding consistency                                       │
│                                                                     │
│  OUTPUT: canonical-transcript.json (same schema)                   │
│         + index.json + chunks/*.json (new)                          │
│                                                                     │
│  BENEFITS:                                                          │
│  ✓ No context window limits (Python has none)                      │
│  ✓ No Lost-in-Middle (chunks are small)                            │
│  ✓ Deterministic accuracy (100%)                                   │
│  ✓ Fast processing (<1s for any size)                              │
│  ✓ Zero token cost for parsing                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Recommendations for Phase 3 (ps-architect TDD Creation)

### R-1: Prioritize EN-020 Python Parser Foundation

**Rationale:** All other enablers depend on EN-020. Without deterministic parsing, chunking and adaptation have no input.

**TDD Guidance:**
- Define webvtt-py wrapper interface
- Specify encoding detection requirements (charset-normalizer)
- Document output schema (canonical-transcript.json v1.1)
- Define error handling and recovery patterns

**Evidence:** Phase 1 Research Section RQ-3: "webvtt-py provides clean Python API for VTT parsing"

### R-2: Implement Strategy Pattern in ts-parser.md

**Rationale:** DEC-011 D-001 mandates ts-parser.md as orchestrator using Strategy Pattern.

**TDD Guidance:**
- Define IParserStrategy interface
- Specify PythonParserStrategy implementation
- Maintain LLMParserStrategy as fallback
- Document strategy selection logic

**Evidence:** Phase 1 Research Section RQ-1: "Gang of Four Strategy Pattern provides architectural foundation"

### R-3: Specify 500-Segment Chunk Size

**Rationale:** Balance between context efficiency and semantic completeness.

**TDD Guidance:**
- Chunk size: 500 segments (configurable)
- Estimated token count: 10,000-20,000 per chunk
- Index file contains: metadata, speaker counts, chunk pointers
- Chunk boundary: segment boundaries (never mid-segment)

**Evidence:** Phase 1 Research Section RQ-4: "500 segments x 30 tokens/segment = 15,000 tokens (safe margin)"

### R-4: Define Index-Based Navigation for ts-extractor

**Rationale:** ts-extractor needs to understand chunk structure to extract across boundaries.

**TDD Guidance:**
- ts-extractor reads index.json first
- Requests specific chunks as needed
- Aggregates results across chunks
- Maintains citation integrity

**Evidence:** FEAT-004-hybrid-infrastructure.md Section "Architecture Overview" Layer 3

### R-5: Include Fallback Path Testing

**Rationale:** LLM fallback is critical for unknown formats and Python failures.

**TDD Guidance:**
- Test Python parser failure → LLM fallback
- Test unknown format detection → LLM fallback
- Test partial success scenarios
- Measure fallback path performance

**Evidence:** FMEA FM-001, FM-002: LLM fallback mitigates Python parser risks

### R-6: Specify Performance Benchmarks

**Rationale:** FEAT-004 claims significant performance improvements; must validate.

**TDD Guidance:**
- Parse time < 5 seconds for 5-hour transcript (NFC-1)
- Memory usage < 100MB during parsing (NFC-2)
- End-to-end pipeline < 30 seconds (Benefit Hypothesis)
- Token cost = $0 for parsing layer

**Evidence:** FEAT-004-hybrid-infrastructure.md Non-Functional Criteria

---

## References

### Phase 1 Research (FEAT-004-e-240)

1. **Liu, N.F., et al.** (2024). "Lost in the Middle: How Language Models Use Long Contexts." *Transactions of the Association for Computational Linguistics*, 12, 157-173. [https://aclanthology.org/2024.tacl-1.9/](https://aclanthology.org/2024.tacl-1.9/)

2. **Gang of Four Strategy Pattern.** Refactoring Guru. [https://refactoring.guru/design-patterns/strategy](https://refactoring.guru/design-patterns/strategy)

3. **webvtt-py Library.** GitHub. [https://github.com/glut23/webvtt-py](https://github.com/glut23/webvtt-py)

4. **LangChain RecursiveCharacterTextSplitter.** [https://docs.langchain.com/oss/python/langchain/rag](https://docs.langchain.com/oss/python/langchain/rag)

5. **WorkOS Enterprise AI Agent Playbook.** [https://workos.com/blog/enterprise-ai-agent-playbook](https://workos.com/blog/enterprise-ai-agent-playbook)

### Internal References

6. **DISC-009:** Agent-Only Architecture Limitation Discovery (99.8% data loss incident)

7. **DEC-011:** ts-parser Hybrid Role Decision (Strategy Pattern selection)

8. **FEAT-004-hybrid-infrastructure.md:** Feature definition and acceptance criteria

9. **ts-parser.md v1.2.0:** Current agent definition (pre-transformation)

10. **ts-extractor.md v1.2.0:** Current extractor interface

11. **ADR-001-amendment-001:** Python Preprocessing Layer amendment

### Industry Best Practices

12. **charset-normalizer.** "4-5x faster than chardet for encoding detection." [https://github.com/jawah/charset_normalizer](https://github.com/jawah/charset_normalizer)

13. **LangGraph Workflows.** Conditional edges for format routing. [https://docs.langchain.com/oss/python/langgraph/workflows-agents](https://docs.langchain.com/oss/python/langgraph/workflows-agents)

---

## Appendix: Task Estimation

### EN-020: Python Parser Implementation (6-8 tasks)

| # | Task | Complexity | Dependencies |
|---|------|------------|--------------|
| 1 | webvtt-py wrapper design | M | None |
| 2 | Encoding detection integration | M | Task 1 |
| 3 | VTT parsing implementation | M | Task 1, 2 |
| 4 | Output schema compliance | S | Task 3 |
| 5 | Error handling and recovery | M | Task 3 |
| 6 | Unit tests | M | Task 3, 4, 5 |
| 7 | Performance benchmarks | S | Task 3 |
| 8 | Documentation | S | All above |

### EN-021: Chunking Strategy (5-6 tasks)

| # | Task | Complexity | Dependencies |
|---|------|------------|--------------|
| 1 | Index.json schema design | M | EN-020 |
| 2 | Chunk.json schema design | S | Task 1 |
| 3 | Chunking algorithm | M | Task 1, 2 |
| 4 | Boundary handling | M | Task 3 |
| 5 | Unit tests | M | Task 3, 4 |
| 6 | Documentation | S | All above |

### EN-022: Extractor Adaptation (4-5 tasks)

| # | Task | Complexity | Dependencies |
|---|------|------------|--------------|
| 1 | ts-extractor interface update | M | EN-021 |
| 2 | Index navigation logic | M | Task 1 |
| 3 | Chunk selection strategy | M | Task 2 |
| 4 | Result aggregation | M | Task 3 |
| 5 | Integration tests | M | Task 4 |

### EN-023: Integration Testing (5-6 tasks)

| # | Task | Complexity | Dependencies |
|---|------|------------|--------------|
| 1 | Test framework setup | M | EN-020, EN-021, EN-022 |
| 2 | Large file test cases | M | Task 1 |
| 3 | Fallback path tests | M | Task 1 |
| 4 | Performance benchmarks | M | Task 2, 3 |
| 5 | Regression tests | M | Task 2, 3 |
| 6 | Test documentation | S | All above |

---

## Metadata

```yaml
ps_id: "FEAT-004"
entry_id: "e-241"
topic: "Blast Radius Assessment for Hybrid Infrastructure Transformation"
agent: "ps-analyst"
agent_version: "2.0.0"
created_at: "2026-01-29T22:00:00Z"
input_artifact: "FEAT-004-e-240-hybrid-architecture-research.md"
sources_count: 13
analysis_frameworks:
  - "5W2H"
  - "Ishikawa (Fishbone)"
  - "FMEA"
  - "Gap Mapping"
  - "Dependency Analysis"
confidence: "HIGH"
next_phase: "TASK-242 (ps-architect TDD-FEAT-004 creation)"
related_artifacts:
  - "FEAT-004-hybrid-infrastructure.md"
  - "FEAT-004-e-240-hybrid-architecture-research.md"
  - "DISC-009 (agent-only architecture limitation)"
  - "DEC-011 (ts-parser hybrid role)"
  - "ADR-001-amendment-001 (Python preprocessing layer)"
```

---

<!--
DESIGN RATIONALE:

This blast radius analysis provides comprehensive impact assessment for the
hybrid infrastructure transformation. Key findings:

1. IMPACT SCOPE: 4 components significantly affected (ts-parser.md, SKILL.md,
   ts-extractor.md, test infrastructure), 4 new enablers required

2. RISK PROFILE: Highest RPN is FM-003 (chunk boundary corruption) at 128,
   mitigated by segment-boundary chunking strategy

3. DEPENDENCY CHAIN: Linear critical path EN-020 → EN-021 → EN-022 → EN-023
   enables incremental delivery and validation

4. BACKWARD COMPATIBILITY: Maintained through LLM fallback path and unchanged
   output schemas

5. ROLLBACK STRATEGY: Clear decision tree with automatic fallback to LLM
   parser if Python path fails

The analysis supports DEC-011 decisions and provides concrete guidance for
TDD-FEAT-004 creation in Phase 3.

TRACE:
- Input: FEAT-004-e-240-hybrid-architecture-research.md
- Supports: TDD-FEAT-004 creation
- Informs: EN-020..023 implementation specifications
- Validates: DISC-009 → FEAT-004 remediation path
-->
