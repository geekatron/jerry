# EN-006 5W2H Analysis: Context Injection Mechanism

<!--
TEMPLATE: 5W2H Analysis
SOURCE: Problem-Solving Framework (ps-analyst)
VERSION: 1.0.0
TASK: TASK-031 (DEC-001 Sequential Forward-Feeding)
PHASE: 1
-->

---

## Frontmatter

```yaml
# === IDENTITY ===
id: "en006-5w2h-analysis"
work_type: ANALYSIS
parent_id: "TASK-031"

# === METADATA ===
title: "5W2H Analysis: Context Injection Mechanism"
description: |
  Comprehensive analysis of the Context Injection Mechanism using the 5W2H
  framework (Who, What, When, Where, Why, How, How Much). Applies the selected
  Hybrid Approach (A5) from Phase 0 trade space analysis.

# === AUTHORSHIP ===
created_by: "ps-analyst"
created_at: "2026-01-26"
updated_at: "2026-01-26"

# === TRACEABILITY ===
inputs_from:
  - "docs/research/en006-research-synthesis.md"
  - "docs/research/en006-trade-space.md"
  - "EN-003 REQUIREMENTS-SPECIFICATION.md"
outputs_to: "TASK-032"  # Forward-feeding per DEC-001

requirements_traced:
  - STK-009   # Jerry framework integration
  - IR-004    # SKILL.md interface
  - IR-005    # Hexagonal architecture
  - SK-001    # SKILL.md structure
  - SK-004    # Progressive disclosure
  - MA-001    # Provider-independent design
  - MA-002    # Avoid provider-specific features

# === DECISION REFERENCE ===
decision_ref: "EN-006--DEC-001-phase1-execution-strategy.md"
execution_mode: "SEQUENTIAL_FORWARD_FEEDING"
position_in_chain: 1
```

---

## L0: Executive Summary (ELI5)

### What is This Analysis About?

Imagine you're teaching someone to analyze legal documents. Instead of explaining everything from scratch each time, you give them a "cheat sheet" with legal terms, important patterns, and what to look for. **Context injection** is giving AI agents that "cheat sheet" - domain-specific knowledge that makes them smarter for particular tasks.

### Key Findings

| Dimension | Finding |
|-----------|---------|
| **WHO** | 4 user personas: Domain Experts, Skill Developers, End Users, System Integrators |
| **WHAT** | Hybrid approach: Static files + Dynamic tools + Template variables |
| **WHEN** | 3 loading stages: Skill activation, Analysis start, On-demand retrieval |
| **WHERE** | 5 integration points: SKILL.md, AGENT.md, Session, Tools, Memory |
| **WHY** | Bridge domain knowledge gap - intelligence is not the bottleneck, context is |
| **HOW** | 3-layer architecture: Static → Dynamic → Template resolution |
| **HOW MUCH** | <500ms loading, <2 hours setup time, >=90% test coverage |

### Bottom Line

Context injection transforms generic AI agents into domain-specialized experts by providing the right knowledge at the right time. The Hybrid Approach (A5) scored 8.25/10 in the trade study, combining the best of static files (performance), dynamic tools (freshness), and templates (customization).

---

## L1: Technical Analysis (Software Engineer)

### 1. WHO - Target Users

#### 1.1 Persona Matrix

| Persona | Role | Skill Level | Primary Use Case | Context Needs |
|---------|------|-------------|------------------|---------------|
| **P1: Domain Expert** | Legal analyst, Sales manager, Engineering lead | Non-technical | Analyze transcripts in their domain | Pre-built domain schemas, extraction rules |
| **P2: Skill Developer** | Agent/skill author | Technical | Create new domain contexts | Schema templates, validation tools |
| **P3: End User** | Meeting participant, Reviewer | Mixed | Extract insights from transcripts | Zero-config defaults, progressive enhancement |
| **P4: System Integrator** | CI/CD pipeline, Automation | Technical | Pipeline integration | JSON API, deterministic outputs |

**Source:** [EN-003 REQUIREMENTS-SPECIFICATION.md, Section 2.1]

#### 1.2 Persona-to-Requirement Mapping

```
PERSONA → STAKEHOLDER NEED → REQUIREMENT
=========================================

P1: Domain Expert
├── STK-003: Identify who said what       → FR-005, FR-006 (Speaker extraction)
├── STK-004: Extract action items         → FR-007 (Action extraction)
└── STK-008: Trust extraction results     → FR-011 (Confidence scores)

P2: Skill Developer
├── STK-009: Jerry framework integration  → IR-004 (SKILL.md interface)
└── (NEW) Ease of domain configuration    → [EN-006 derived requirement]

P3: End User
├── STK-007: Results quickly (<10s)       → NFR-001 (Performance)
└── STK-001/002: Process VTT/SRT files    → FR-001, FR-002 (Parsing)

P4: System Integrator
├── STK-010: Pipeline automation          → IR-003 (Exit codes)
└── (NEW) Deterministic testing           → [EN-006 derived requirement]
```

#### 1.3 Stakeholder Expectations (NASA SE Process 1)

| Stakeholder | Expectation | MOE (Measure of Effectiveness) | Target |
|-------------|-------------|--------------------------------|--------|
| Domain Expert | Accurate domain-specific extraction | Extraction F1 score | >= 0.90 |
| Skill Developer | Easy domain configuration | Setup time | < 2 hours |
| End User | Fast processing | Processing time | < 500ms context load |
| System Integrator | Deterministic behavior | Test pass rate | 100% |
| QA Team | Testable context injection | Code coverage | >= 95% |
| Security Team | No sensitive data leakage | Incidents | 0 |
| Operations | Observable context loading | Audit completeness | 100% |

**Source:** [en006-research-synthesis.md, Section L2.3.2]

---

### 2. WHAT - Mechanism Definition

#### 2.1 Selected Approach: Hybrid (A5)

Based on the trade space analysis (8.25/10 score), the Context Injection Mechanism consists of three complementary layers:

```
HYBRID CONTEXT INJECTION MECHANISM
==================================

┌─────────────────────────────────────────────────────────────────────────┐
│                         CONTEXT INJECTION LAYERS                         │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  LAYER 1: STATIC CONTEXT                                                 │
│  ───────────────────────                                                 │
│  Format: YAML/Markdown files                                             │
│  Location: contexts/{domain}.yaml, SKILL.md                              │
│  Content:                                                                │
│  • Domain entity definitions                                             │
│  • Extraction rule schemas                                               │
│  • Prompt guidance templates                                             │
│  Load Time: Skill activation (pre-loaded)                                │
│                                                                          │
│  LAYER 2: DYNAMIC CONTEXT                                                │
│  ────────────────────────                                                │
│  Format: Tool responses (JSON)                                           │
│  Source: MCP-compatible tool calls                                       │
│  Content:                                                                │
│  • User-specific preferences                                             │
│  • Document metadata                                                     │
│  • Previous analysis cache                                               │
│  Load Time: Runtime (on-demand)                                          │
│                                                                          │
│  LAYER 3: TEMPLATE RESOLUTION                                            │
│  ────────────────────────────                                            │
│  Format: {{$variable}} substitution                                      │
│  Location: Prompt templates                                              │
│  Content:                                                                │
│  • Merged static + dynamic context                                       │
│  • User input bindings                                                   │
│  • Computed values                                                       │
│  Load Time: Prompt assembly                                              │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

#### 2.2 Component Inventory

| Component | Type | Description | Location |
|-----------|------|-------------|----------|
| **Domain Schema** | Static | Entity definitions, extraction rules | `contexts/{domain}.yaml` |
| **Skill Context** | Static | SKILL.md sections injected at activation | `SKILL.md` |
| **Agent Persona** | Static | AGENT.md role, goal, backstory | `agents/{agent}.md` |
| **Context Tool** | Dynamic | Fetch runtime context via MCP | Tool definition |
| **Memory Store** | Dynamic | Cross-session persistent context | Memory adapter |
| **Prompt Template** | Template | Variable resolution at runtime | Embedded in prompts |

#### 2.3 Data Structures

**Domain Schema (YAML):**

```yaml
# contexts/legal-domain.yaml
schema_version: "1.0"
domain: "legal"

entity_definitions:
  party:
    description: "Legal entity in contract"
    attributes:
      - name
      - role: [buyer, seller, guarantor]
      - jurisdiction
    extraction_patterns:
      - "{{name}} (the \"{{role}}\")"
      - "{{role}}: {{name}}"

  obligation:
    description: "Contractual obligation"
    attributes:
      - obligor
      - obligee
      - terms
      - deadline

extraction_rules:
  - id: "parties"
    description: "Identify all parties mentioned by name and role"
    priority: 1
    confidence_threshold: 0.85

  - id: "dates"
    description: "Extract all dates in ISO 8601 format"
    priority: 2
    confidence_threshold: 0.90

prompt_guidance: |
  When analyzing legal documents:
  1. Identify parties before analyzing obligations
  2. Cross-reference obligations with party roles
  3. Flag ambiguous terms for human review
```

**Source:** [en006-trade-space.md, Section 2.1]

#### 2.4 Interface Contracts

| Interface | Protocol | Format | Direction |
|-----------|----------|--------|-----------|
| `IContextProvider` | Port | Context object | Outbound |
| `ISchemaValidator` | Port | Validation result | Inbound |
| `ContextToolAdapter` | Adapter | JSON/MCP | Bidirectional |
| `MemoryAdapter` | Adapter | Key-value | Bidirectional |

---

### 3. WHEN - Trigger Conditions

#### 3.1 Context Loading Timeline

```
CONTEXT LOADING LIFECYCLE
=========================

Time ──────────────────────────────────────────────────────────►

┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   INSTALL   │    │   ACTIVATE  │    │   ANALYZE   │    │  COMPLETE   │
│    TIME     │    │    TIME     │    │    TIME     │    │    TIME     │
└──────┬──────┘    └──────┬──────┘    └──────┬──────┘    └──────┬──────┘
       │                  │                  │                  │
       ▼                  ▼                  ▼                  ▼
  ┌──────────┐      ┌──────────┐      ┌──────────┐      ┌──────────┐
  │ Domain   │      │ SKILL.md │      │ Document │      │ Memory   │
  │ Schema   │      │ Sections │      │ Context  │      │ Persist  │
  │ Validate │      │ Injected │      │ Loaded   │      │ Results  │
  └──────────┘      └──────────┘      └──────────┘      └──────────┘
       │                  │                  │                  │
  STATIC ◄───────────────►│◄── HYBRID ──────►│◄─── DYNAMIC ────►│
```

#### 3.2 Trigger Conditions Matrix

| Scenario | Trigger | Layer Activated | Context Loaded |
|----------|---------|-----------------|----------------|
| **T1: Skill Activation** | User invokes transcript skill | Layer 1 (Static) | SKILL.md, default domain schema |
| **T2: Domain Selection** | User specifies `--domain legal` | Layer 1 (Static) | Domain-specific schema |
| **T3: Document Load** | Transcript file provided | Layer 2 (Dynamic) | Document metadata, format detection |
| **T4: Entity Extraction** | Extraction command executed | Layer 2 (Dynamic) | Previous extractions, user preferences |
| **T5: Cross-Reference** | Related document referenced | Layer 2 (Dynamic) | External document context |
| **T6: Prompt Assembly** | LLM invocation | Layer 3 (Template) | All variables resolved |
| **T7: Session End** | User exits | Layer 2 (Dynamic) | Results persisted to memory |

#### 3.3 Trigger Frequency Analysis

| Trigger | Frequency | Latency Budget | Caching Strategy |
|---------|-----------|----------------|------------------|
| T1: Skill Activation | Once per session | 500ms | Preload at startup |
| T2: Domain Selection | Rarely | 200ms | Lazy load on demand |
| T3: Document Load | Per document | 300ms | Per-document cache |
| T4: Entity Extraction | Multiple per document | 100ms | Incremental |
| T5: Cross-Reference | Rare | 500ms | Optional prefetch |
| T6: Prompt Assembly | Per LLM call | 50ms | Template cache |
| T7: Session End | Once per session | 1000ms | Async persist |

---

### 4. WHERE - Integration Points

#### 4.1 Architecture Integration Diagram

```
CONTEXT INJECTION INTEGRATION POINTS
====================================

                 ┌─────────────────────────────────────────────────┐
                 │                  JERRY FRAMEWORK                 │
                 └────────────────────────┬────────────────────────┘
                                          │
        ┌─────────────────────────────────┼─────────────────────────────────┐
        │                                 │                                 │
        ▼                                 ▼                                 ▼
┌───────────────┐               ┌───────────────┐               ┌───────────────┐
│   SKILL.md    │               │   AGENT.md    │               │  CLAUDE.md    │
│ ────────────  │               │ ────────────  │               │ ────────────  │
│               │               │               │               │               │
│ Integration   │◄──────────────►│ Agent        │◄──────────────►│ Framework    │
│ Point 1 (IP1) │               │ Point 2 (IP2)│               │ Point 3 (IP3)│
│               │               │               │               │               │
│ Skill-level   │               │ Agent-level   │               │ Session-level │
│ context       │               │ persona       │               │ context       │
│               │               │               │               │               │
└───────┬───────┘               └───────┬───────┘               └───────┬───────┘
        │                               │                               │
        └───────────────────────────────┼───────────────────────────────┘
                                        │
                                        ▼
                        ┌───────────────────────────────┐
                        │     CONTEXT INJECTION PORT     │
                        │     (IContextProvider)         │
                        └───────────────┬───────────────┘
                                        │
                ┌───────────────────────┼───────────────────────┐
                │                       │                       │
                ▼                       ▼                       ▼
        ┌───────────────┐       ┌───────────────┐       ┌───────────────┐
        │ Static Adapter │       │Dynamic Adapter│       │ Memory Adapter│
        │ (Filesystem)   │       │ (MCP Tools)   │       │ (Key-Value)   │
        └───────────────┘       └───────────────┘       └───────────────┘
                │                       │                       │
                ▼                       ▼                       ▼
        ┌───────────────┐       ┌───────────────┐       ┌───────────────┐
        │ Integration   │       │ Integration   │       │ Integration   │
        │ Point 4 (IP4) │       │ Point 5 (IP5) │       │ Point 6 (IP6) │
        │ contexts/*.yaml│       │ MCP Servers   │       │ memory-keeper │
        └───────────────┘       └───────────────┘       └───────────────┘
```

#### 4.2 Integration Point Details

| IP | Name | Location | Type | Protocol | Jerry Pattern |
|----|------|----------|------|----------|---------------|
| IP1 | SKILL.md Context | `skills/transcript/SKILL.md` | File | Markdown/YAML | Progressive Disclosure |
| IP2 | AGENT.md Persona | `skills/transcript/agents/*.md` | File | Markdown | Agent Definition |
| IP3 | Session Context | CLAUDE.md hierarchy | File | Markdown | Context Engineering |
| IP4 | Domain Schemas | `skills/transcript/contexts/` | File | YAML | Configuration |
| IP5 | MCP Context Tools | MCP Server definitions | Protocol | JSON-RPC | MCP Standard |
| IP6 | Memory Store | memory-keeper MCP | Service | MCP | Persistence |

#### 4.3 Hexagonal Architecture Alignment

```
HEXAGONAL ARCHITECTURE - CONTEXT INJECTION LAYER
================================================

                    ┌─────────────────────────────────────┐
                    │          INTERFACE LAYER            │
                    │     (Primary Adapters - Driving)    │
                    ├─────────────────────────────────────┤
                    │ • CLI Adapter                       │
                    │ • SKILL.md Interface                │
                    │ • Agent Invocation                  │
                    └──────────────────┬──────────────────┘
                                       │
                                       ▼
┌──────────────────────────────────────────────────────────────────────────┐
│                         APPLICATION LAYER                                 │
│                      (Use Cases - Commands/Queries)                       │
├──────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │                    CONTEXT INJECTION PORT                        │    │
│  │                    (IContextProvider)                            │    │
│  │  ─────────────────────────────────────────────────────────────  │    │
│  │  + load_static_context(domain: str) -> Context                  │    │
│  │  + load_dynamic_context(document_id: str) -> Context            │    │
│  │  + resolve_template(template: str, context: Context) -> str     │    │
│  │  + validate_context(context: Context) -> ValidationResult       │    │
│  └─────────────────────────────────────────────────────────────────┘    │
│                                                                          │
└──────────────────────────────────────────────────────────────────────────┘
                                       │
                                       ▼
                    ┌─────────────────────────────────────┐
                    │      INFRASTRUCTURE LAYER           │
                    │   (Secondary Adapters - Driven)     │
                    ├─────────────────────────────────────┤
                    │ • FilesystemContextAdapter          │
                    │ • MCPToolContextAdapter             │
                    │ • MemoryKeeperAdapter               │
                    │ • SchemaValidationAdapter           │
                    └─────────────────────────────────────┘
```

**Source:** [EN-003 IR-005: Hexagonal architecture requirement]

---

### 5. WHY - Value Proposition

#### 5.1 Problem Statement

From [Anthropic Context Engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents):

> "**Intelligence is not the bottleneck - context is.**"
> "The best AI agents aren't the smartest; they're the ones with the best context loaded at the right time."

#### 5.2 Value Drivers

| Driver | Without Context Injection | With Context Injection | Improvement |
|--------|---------------------------|------------------------|-------------|
| **Domain Accuracy** | Generic extraction (F1: 0.60) | Domain-specific (F1: 0.90) | **+50%** |
| **Setup Time** | Manual prompt engineering (4+ hours) | Schema configuration (<2 hours) | **-50%** |
| **Consistency** | Variable across sessions | Deterministic | **100%** |
| **Testability** | Hard to test (dynamic prompts) | Schema-validated | **+High** |
| **Extensibility** | Requires code changes | Configuration-only | **+High** |

#### 5.3 ROI Analysis

```
RETURN ON INVESTMENT: CONTEXT INJECTION
=======================================

COSTS (One-Time):
┌─────────────────────────────────────────┐
│ Development effort:     40 hours       │
│ Testing effort:         20 hours       │
│ Documentation:          10 hours       │
│ ────────────────────────────────────── │
│ TOTAL COST:             70 hours       │
└─────────────────────────────────────────┘

BENEFITS (Per Domain):
┌─────────────────────────────────────────┐
│ Prompt engineering saved: 4 hours/domain│
│ Debugging saved:          2 hours/domain│
│ Testing saved:            3 hours/domain│
│ ────────────────────────────────────── │
│ TOTAL SAVED:              9 hours/domain│
└─────────────────────────────────────────┘

BREAK-EVEN: 70 / 9 ≈ 8 domains
```

#### 5.4 EN-003 Requirement Fulfillment

| EN-003 Requirement | How Context Injection Addresses |
|--------------------|---------------------------------|
| STK-009 (Jerry integration) | Hexagonal architecture with Jerry ports/adapters |
| IR-004 (SKILL.md interface) | Context defined in SKILL.md frontmatter |
| IR-005 (Hexagonal architecture) | IContextProvider port + multiple adapters |
| MA-001 (Model-agnostic) | Context format independent of LLM provider |
| MA-002 (No vendor-specific) | Uses standard YAML/JSON, no Claude-specific features |
| SK-004 (Progressive disclosure) | Context loaded in stages (<500 lines each) |

---

### 6. HOW - Implementation Approach

#### 6.1 Implementation Workflow

```
CONTEXT INJECTION IMPLEMENTATION FLOW
=====================================

    ┌─────────────────────────────────────────────────────────────────────┐
    │  STEP 1: SKILL ACTIVATION                                            │
    │  ─────────────────────────                                           │
    │                                                                      │
    │  User: "Use the transcript skill for legal analysis"                 │
    │                                                                      │
    │  ┌──────────────────┐                                                │
    │  │ Load SKILL.md    │                                                │
    │  │ context section  │                                                │
    │  └────────┬─────────┘                                                │
    │           │                                                          │
    │           ▼                                                          │
    │  ┌──────────────────┐     ┌──────────────────┐                       │
    │  │ Detect domain:   │────►│ Load domain      │                       │
    │  │ "legal"          │     │ schema YAML      │                       │
    │  └──────────────────┘     └────────┬─────────┘                       │
    │                                    │                                 │
    └────────────────────────────────────┼─────────────────────────────────┘
                                         ▼
    ┌─────────────────────────────────────────────────────────────────────┐
    │  STEP 2: DOCUMENT CONTEXT LOADING                                    │
    │  ────────────────────────────────                                    │
    │                                                                      │
    │  User: "Analyze contract.vtt"                                        │
    │                                                                      │
    │  ┌──────────────────┐     ┌──────────────────┐                       │
    │  │ Parse document   │────►│ Detect format    │                       │
    │  │ metadata         │     │ (VTT)            │                       │
    │  └────────┬─────────┘     └────────┬─────────┘                       │
    │           │                        │                                 │
    │           ▼                        ▼                                 │
    │  ┌──────────────────┐     ┌──────────────────┐                       │
    │  │ Load previous    │     │ Load user        │                       │
    │  │ analysis (if any)│     │ preferences      │                       │
    │  └────────┬─────────┘     └────────┬─────────┘                       │
    │           └────────────────────────┘                                 │
    │                        │                                             │
    └────────────────────────┼─────────────────────────────────────────────┘
                             ▼
    ┌─────────────────────────────────────────────────────────────────────┐
    │  STEP 3: TEMPLATE RESOLUTION                                         │
    │  ───────────────────────────                                         │
    │                                                                      │
    │  Template:                                                           │
    │  ┌────────────────────────────────────────────────────────────────┐ │
    │  │ {{$domain_context}}                                            │ │
    │  │                                                                │ │
    │  │ Analyze the following transcript for {{$domain}} patterns:     │ │
    │  │ {{$transcript_content}}                                        │ │
    │  │                                                                │ │
    │  │ Focus on: {{$extraction_rules}}                                │ │
    │  └────────────────────────────────────────────────────────────────┘ │
    │                                                                      │
    │  Resolved:                                                           │
    │  ┌────────────────────────────────────────────────────────────────┐ │
    │  │ When analyzing legal documents:                                │ │
    │  │ 1. Identify parties before analyzing obligations               │ │
    │  │ 2. Cross-reference obligations with party roles                │ │
    │  │                                                                │ │
    │  │ Analyze the following transcript for legal patterns:           │ │
    │  │ [Contract discussion transcript content...]                    │ │
    │  │                                                                │ │
    │  │ Focus on: parties, obligations, dates                          │ │
    │  └────────────────────────────────────────────────────────────────┘ │
    │                                                                      │
    └─────────────────────────────────────────────────────────────────────┘
```

#### 6.2 Sequence Diagram

```
CONTEXT INJECTION SEQUENCE
==========================

    User          CLI           Skill        Context        Static       Dynamic
     │             │             │           Provider        Adapter      Adapter
     │             │             │             │              │            │
     │──invoke────►│             │             │              │            │
     │             │──activate──►│             │              │            │
     │             │             │──load───────►──request────►│            │
     │             │             │             │◄──domain─────┤            │
     │             │             │◄──static────┤              │            │
     │             │             │             │              │            │
     │──document──►│             │             │              │            │
     │             │──analyze───►│             │              │            │
     │             │             │──load───────►──request─────────────────►│
     │             │             │             │◄──metadata────────────────┤
     │             │             │◄──dynamic───┤              │            │
     │             │             │             │              │            │
     │             │             │──resolve────►              │            │
     │             │             │◄──prompt────┤              │            │
     │             │             │             │              │            │
     │             │◄──result────┤             │              │            │
     │◄──output────┤             │             │              │            │
     │             │             │             │              │            │
```

#### 6.3 Implementation Phases

| Phase | Component | Description | Dependencies |
|-------|-----------|-------------|--------------|
| **P1** | `IContextProvider` Port | Define interface contract | None |
| **P2** | `FilesystemContextAdapter` | Load YAML schemas | P1 |
| **P3** | `SchemaValidationAdapter` | JSON Schema validation | P1 |
| **P4** | `TemplateResolver` | Variable substitution | P2 |
| **P5** | `MCPToolContextAdapter` | MCP protocol support | P1 |
| **P6** | `MemoryKeeperAdapter` | Cross-session persistence | P1, P5 |

---

### 7. HOW MUCH - Impact Assessment

#### 7.1 Performance Impact

| Metric | Target | Mitigation |
|--------|--------|------------|
| Context loading latency | < 500ms | Pre-load static, lazy-load dynamic |
| Memory footprint | < 50MB additional | Stream large contexts |
| Disk I/O | Minimal | Cache parsed schemas |
| LLM token overhead | < 2000 tokens | Compress context, use templates |

#### 7.2 Complexity Impact

| Aspect | Impact Level | Justification |
|--------|--------------|---------------|
| Code complexity | Medium | New adapter pattern, but well-isolated |
| Configuration complexity | Low | YAML-based, human-readable |
| Testing complexity | Medium | Need to test multiple context combinations |
| Maintenance complexity | Low | Schema changes don't require code changes |

#### 7.3 Effort Estimate

| Component | Development | Testing | Documentation | Total |
|-----------|-------------|---------|---------------|-------|
| Port interface | 4h | 2h | 2h | 8h |
| Filesystem adapter | 8h | 4h | 2h | 14h |
| Validation adapter | 6h | 4h | 2h | 12h |
| Template resolver | 6h | 4h | 2h | 12h |
| MCP adapter | 12h | 6h | 2h | 20h |
| Memory adapter | 8h | 4h | 2h | 14h |
| **TOTAL** | **44h** | **24h** | **12h** | **80h** |

#### 7.4 Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Schema format changes | Medium | Low | Version schemas, backward compatibility |
| MCP protocol evolution | Low | Medium | Abstract behind adapter |
| Performance degradation | Low | Medium | Caching strategy, lazy loading |
| Context bloat | Medium | Medium | Size limits, compaction strategy |

---

## L2: Architecture Implications (Principal Architect)

### 1. Strategic Trade-offs

#### 1.1 Static vs Dynamic Loading

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Default loading strategy | **Hybrid** | Best of both: speed (static) + freshness (dynamic) |
| Schema format | **YAML** | Human-readable, sufficient for structure (no Pydantic runtime) |
| Validation approach | **JSON Schema + runtime Pydantic** | Schema for structure, Pydantic for type safety |
| Memory persistence | **File-based** | Aligned with Jerry P-002 (file persistence) |

#### 1.2 One-Way Door Decisions

| Decision | Reversibility | Impact | Recommendation |
|----------|---------------|--------|----------------|
| YAML for schema format | Easy | Medium | **Accept** - human-friendly |
| IContextProvider port interface | Medium | High | **Define carefully** - API stability |
| MCP compatibility | Medium | High | **Accept** - industry standard |
| Template variable syntax (`{{$var}}`) | Easy | Low | **Accept** - Semantic Kernel compatible |

### 2. Design Principles Applied

Based on [en006-research-synthesis.md, Section L2]:

| Principle | Application |
|-----------|-------------|
| **Schema-First Design** | Define context schema YAML before adapter implementation |
| **Hybrid Loading** | Static SKILL.md + dynamic MCP tools |
| **MCP Compatibility** | Design adapters for future MCP migration |
| **Stakeholder-Driven MOEs** | Context loading < 500ms per NASA SE Process 1 |
| **Progressive Disclosure** | Load context in stages (<500 lines per stage) |
| **Provider Agnostic** | No vendor-specific features in context format |
| **Auditable Context** | Full traceability of context loading |

### 3. Future Evolution Path

```
CONTEXT INJECTION EVOLUTION ROADMAP
===================================

Phase 1 (Current):          Phase 2 (Q2 2026):       Phase 3 (Q4 2026):
─────────────────           ──────────────────       ──────────────────
Hybrid without MCP          MCP-aware hybrid         Full MCP integration
                            adapter layer            native MCP server

┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│ • YAML schemas  │───►│ • MCP Resources │───►│ • Native MCP    │
│ • File-based    │    │   (context)     │    │   server        │
│ • Tool adapters │    │ • MCP Prompts   │    │ • Discoverable  │
│                 │    │   (templates)   │    │   context       │
│                 │    │ • MCP Tools     │    │ • Cross-agent   │
│                 │    │   (dynamic)     │    │   sharing       │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

**Source:** [en006-trade-space.md, Section 4]

---

## Forward-Feeding Output

### Summary for TASK-032 (Ishikawa & Pareto Analysis)

This 5W2H analysis provides the following inputs for root cause and prioritization analysis:

| 5W2H Dimension | Key Finding for TASK-032 |
|----------------|--------------------------|
| **WHAT** | Hybrid mechanism (static + dynamic + templates) - analyze failure modes for each layer |
| **WHO** | 4 personas with different needs - prioritize by persona impact |
| **HOW** | 3-layer architecture - root cause analysis per layer |
| **WHERE** | 6 integration points - failure mode analysis per integration |
| **HOW MUCH** | 80h effort - identify 20% features delivering 80% value |

### Scope Definition for Ishikawa Categories

Based on the 5W2H analysis, the Ishikawa root cause categories map as follows:

| Ishikawa Category | 5W2H Source | Focus Area |
|-------------------|-------------|------------|
| **People** | WHO section | User personas, skill levels, training needs |
| **Process** | HOW section | Implementation workflow, loading sequence |
| **Technology** | WHAT section | Hybrid layers, adapters, interfaces |
| **Environment** | WHERE section | Integration points, Jerry framework |
| **Materials** | WHAT section | Context schemas, templates, data quality |
| **Methods** | HOW section | Design patterns, validation approaches |

---

## References

### Primary Sources

1. Anthropic. (2025). *Effective Context Engineering for AI Agents*. https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents

2. Model Context Protocol. (2025). *MCP Specification 2025-11-25*. https://modelcontextprotocol.io/specification/2025-11-25

3. NASA. (2024). *NASA Systems Engineering Processes and Requirements (NPR 7123.1D)*. https://nodis3.gsfc.nasa.gov/displayDir.cfm?Internal_ID=N_PR_7123_001D_

### Internal Sources

4. EN-006 Research Synthesis. `docs/research/en006-research-synthesis.md`

5. EN-006 Trade Space Analysis. `docs/research/en006-trade-space.md`

6. EN-003 Requirements Specification. `REQUIREMENTS-SPECIFICATION.md`

7. DEC-001 Phase 1 Execution Strategy. `EN-006--DEC-001-phase1-execution-strategy.md`

---

## History

| Date | Version | Author | Notes |
|------|---------|--------|-------|
| 2026-01-26 | 1.0.0 | ps-analyst | Initial 5W2H analysis |

---

*Document ID: en006-5w2h-analysis*
*Task: TASK-031*
*Phase: 1 (Requirements & Analysis)*
*DEC-001 Position: Step 1 of 3 (Forward-Feeding to TASK-032)*
*Workflow: en006-ctxinj-20260126-001*
