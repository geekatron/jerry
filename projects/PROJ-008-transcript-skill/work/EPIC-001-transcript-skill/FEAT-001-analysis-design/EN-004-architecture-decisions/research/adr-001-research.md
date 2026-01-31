# ADR-001 Research: Agent Architecture for Transcript Skill

> **PS ID:** en004-adr-20260126-001
> **Entry ID:** research-001
> **Agent:** ps-researcher
> **Created:** 2026-01-26
> **Status:** COMPLETE
> **Quality:** Ready for ps-architect synthesis

---

## L0: Executive Summary (ELI5)

**The Question:** How should we structure the agents (specialized AI workers) that will power the Transcript Skill?

**Key Finding:** We should use a **hybrid approach** - reuse Jerry's existing problem-solving agents for research/analysis/review workflows, but create **3-4 custom specialized agents** for transcript-specific tasks (parsing VTT/SRT files, extracting speakers, detecting action items).

**Why This Matters:**
- Reusing existing agents saves development time and ensures consistency
- Custom agents are needed because transcript parsing is domain-specific (no existing Jerry agent does this)
- Industry best practices (Microsoft, Google) confirm a "specialized agents + orchestrator" pattern works well

**Bottom Line:** Build custom VTT Parser, Entity Extractor, and Output Formatter agents that integrate with Jerry's existing orchestration and problem-solving skills.

---

## L1: Technical Research Findings (Software Engineer)

### 1. Jerry Framework Agent Patterns

#### 1.1 Existing Agent Inventory

**Source:** Glob search `skills/**/agents/*.md` (26 files found)

| Skill | Agent Count | Agents |
|-------|-------------|--------|
| problem-solving | 8 | ps-researcher, ps-analyst, ps-architect, ps-critic, ps-validator, ps-synthesizer, ps-reviewer, ps-investigator |
| nasa-se | 10 | nse-requirements, nse-verification, nse-validation, nse-risk, nse-technical-review, nse-integration, nse-configuration, nse-architecture, nse-trade-study, nse-quality |
| architecture | 1 | architecture-guidance |
| orchestration | 3 | orch-planner, orch-tracker, orch-synthesizer |
| worktracker | 2 | wt-decomposition, wt-tracker |

**Key Observation:** Jerry already has 24+ specialized agents. The Transcript Skill should follow established patterns rather than inventing new ones.

#### 1.2 Agent Template Structure (PS_AGENT_TEMPLATE.md)

**Source:** `skills/problem-solving/agents/PS_AGENT_TEMPLATE.md`

```yaml
# YAML Frontmatter Schema
identity:
  id: "agent-id"                    # Unique identifier
  version: "1.0.0"                  # Semantic version
  skill: "skill-name"              # Parent skill

persona:
  role: "Role Name"                 # Human-readable role
  focus: "Primary focus area"       # What this agent specializes in

capabilities:
  core: []                          # Primary capabilities
  tools: []                         # Available tools

guardrails:
  principles: []                    # Constitutional principles
  constraints: []                   # Operational constraints
```

**Body Structure (XML Tags - Anthropic Best Practice):**
```xml
<persona>...</persona>
<capabilities>...</capabilities>
<output-requirements>
  <l0-eli5>...</l0-eli5>
  <l1-engineer>...</l1-engineer>
  <l2-architect>...</l2-architect>
</output-requirements>
<session-context>...</session-context>
<guardrails>...</guardrails>
```

**Constitutional Compliance Required:**
| Principle | Description | Enforcement |
|-----------|-------------|-------------|
| P-002 | File Persistence | All outputs to files |
| P-003 | No Recursive Subagents | Single nesting only |
| P-004 | Explicit Provenance | Document reasoning |
| P-011 | Evidence-Based | Tie recommendations to evidence |
| P-022 | No Deception | Disclose limitations |

#### 1.3 Agent Communication Patterns in Jerry

**Source:** `skills/problem-solving/SKILL.md` and orchestration examples

**State Passing Between Agents:**
| Agent | Output Key | Provides |
|-------|------------|----------|
| ps-researcher | `researcher_output` | Research findings, sources |
| ps-analyst | `analyst_output` | Root cause, recommendations |
| ps-architect | `architect_output` | Decision, alternatives |
| ps-validator | `validator_output` | Validation status, gaps |

**Communication Mechanism:**
1. **File-based state** (P-002 compliance) - Agents write to `docs/` directories
2. **Output keys** - Named keys for inter-agent handoff
3. **Session context** - JSON blob with conversation history and state
4. **Memory-Keeper MCP** - Context persistence across sessions

---

### 2. Industry Agent Architecture Patterns

#### 2.1 Microsoft Azure AI Agent Patterns

**Source:** https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/ai-agent-design-patterns

| Pattern | Description | When to Use | Transcript Skill Fit |
|---------|-------------|-------------|---------------------|
| **Sequential Orchestration** | Linear pipeline, each agent passes to next | Well-defined stages | HIGH - Parse → Extract → Format |
| **Concurrent Orchestration** | Parallel execution with merge | Independent subtasks | MEDIUM - Could parallelize entity extraction |
| **Group Chat Orchestration** | Multi-agent conversation | Complex negotiation | LOW - Overkill for transcript processing |
| **Handoff Orchestration** | Dynamic delegation based on input | Variable routing | LOW - Our pipeline is deterministic |
| **Magentic Orchestration** | Dynamic task ledger | Complex evolving tasks | LOW - Too heavyweight |

**Best Fit:** Sequential Orchestration with optional parallel extraction for entities.

**Microsoft Recommendations:**
> "Use Sequential Orchestration when you have a well-defined workflow with clear input/output contracts between stages."

#### 2.2 Google Cloud Agentic AI Patterns

**Source:** Google Cloud AI Agent Design Patterns documentation

| Pattern | Description | Transcript Skill Fit |
|---------|-------------|---------------------|
| **Single-Agent** | One agent handles everything | LOW - Too monolithic |
| **Multi-Agent Sequential** | Pipeline of specialized agents | HIGH - Matches our flow |
| **Multi-Agent Parallel** | Fan-out/fan-in for independent tasks | MEDIUM - Entity extraction |
| **Coordinator Pattern** | Central router dispatches to specialists | MEDIUM - Could use for entity types |
| **Hierarchical** | Manager agents supervise worker agents | LOW - Violates P-003 |
| **Swarm** | Emergent behavior from simple agents | LOW - Overkill |
| **Loop Pattern** | Iterative refinement until quality | HIGH - Matches ps-critic feedback |
| **Review & Critique** | One agent reviews another's work | HIGH - Already using ps-critic |

**Google Recommendations:**
> "The Review and Critique pattern significantly improves output quality. Include it even in simple pipelines."

**Best Fit:** Multi-Agent Sequential with Review & Critique for quality assurance.

#### 2.3 Anthropic Agent Best Practices

**Source:** Anthropic Engineering Blog - "Equipping Agents for the Real World"

| Practice | Description | Implementation |
|----------|-------------|----------------|
| XML Tags | Structure prompts with XML | Already in Jerry template |
| Tool Use | Explicit tool definitions | YAML capabilities section |
| Constitutional AI | Principles-based guardrails | P-001 through P-022 |
| Iterative Refinement | Feedback loops | ps-critic pattern |

---

### 3. Requirements Analysis for Agent Architecture

#### 3.1 Agent-Relevant Requirements

**Source:** REQUIREMENTS-SPECIFICATION.md (EN-003)

| Req ID | Requirement | Agent Implication |
|--------|-------------|-------------------|
| FR-001 | Parse WebVTT files | **VTT Parser Agent** |
| FR-002 | Parse SubRip files | **SRT Parser Agent** (or shared) |
| FR-003 | Parse plain text | **Text Parser Agent** |
| FR-004 | Auto-detect format | **Format Detector** (not agent, utility) |
| FR-005 | Extract VTT voice tags | **Speaker Extractor Agent** |
| FR-006 | Extract speaker patterns | Part of Speaker Extractor |
| FR-007 | Extract action items | **Entity Extractor Agent** |
| FR-008 | Extract decisions | Part of Entity Extractor |
| FR-009 | Extract questions | Part of Entity Extractor |
| FR-010 | Standard NER | Part of Entity Extractor |
| FR-011 | Confidence scores | All extraction agents |
| FR-012 | Markdown output | **Output Formatter Agent** |
| FR-013 | JSON output | Part of Output Formatter |
| FR-014 | Source citations | All extraction agents |
| IR-004 | SKILL.md interface | Orchestrator level |
| IR-005 | Hexagonal architecture | Domain agent isolation |

**Derived Agent Roster:**
1. **Transcript Parser** (combines FR-001, FR-002, FR-003, FR-004)
2. **Entity Extractor** (combines FR-005 through FR-011, FR-014)
3. **Output Formatter** (combines FR-012, FR-013)

#### 3.2 Design Patterns from Requirements

**Source:** REQUIREMENTS-SPECIFICATION.md Section 5 (Design Patterns)

| Pattern ID | Pattern Name | Agent Architecture Implication |
|------------|--------------|-------------------------------|
| PAT-001 | Tiered Extraction Pipeline | Entity Extractor has 3 tiers (Rule → ML → LLM) |
| PAT-002 | Defensive Parsing | Parser agents handle format variations |
| PAT-003 | Multi-Pattern Speaker Detection | Speaker extraction uses 4+ patterns |
| PAT-004 | Citation-Required Extraction | All LLM-based agents must cite sources |
| PAT-005 | Versioned Schema Evolution | Output formatter handles versioning |
| PAT-006 | Hexagonal Skill Architecture | Agents interact via ports/adapters |

---

### 4. Candidate Agent Architectures

Based on research, three viable options emerge:

#### Option A: Extend Existing Jerry Agents

**Approach:** Use ps-researcher, ps-analyst, ps-architect with domain-specific prompts.

**Structure:**
```
Transcript Skill
├── SKILL.md (orchestrator)
└── prompts/
    ├── parse-transcript.md
    ├── extract-entities.md
    └── format-output.md
```

**Pros:**
- Minimal new code
- Consistent with Jerry patterns
- Leverages existing testing

**Cons:**
- ps-* agents designed for problem-solving, not data processing
- No domain isolation
- Prompt-only customization is limited

#### Option B: Custom Specialized Agents

**Approach:** Create 3 new agents specific to transcript processing.

**Structure:**
```
skills/transcript/agents/
├── vtt-parser/
│   ├── AGENT.md
│   └── prompts/
├── entity-extractor/
│   ├── AGENT.md
│   └── prompts/
└── output-formatter/
    ├── AGENT.md
    └── prompts/
```

**Pros:**
- Clean domain separation
- Purpose-built for transcript domain
- Full control over behavior

**Cons:**
- More code to maintain
- Reinvents patterns Jerry already has
- Longer development time

#### Option C: Hybrid Approach (Recommended)

**Approach:** Custom agents for domain-specific tasks + Jerry's problem-solving agents for research/review.

**Structure:**
```
skills/transcript/
├── SKILL.md (orchestrator)
├── agents/
│   ├── transcript-parser.md      # Custom: VTT/SRT/TXT parsing
│   ├── entity-extractor.md       # Custom: Speakers, actions, decisions
│   └── output-formatter.md       # Custom: MD/JSON generation
└── prompts/
    └── (agent-specific prompts)

# Uses existing Jerry agents for:
# - ps-researcher: Initial research on transcript content
# - ps-critic: Quality review of extraction results
```

**Pros:**
- Domain-specific agents for parsing/extraction
- Reuses ps-critic for quality assurance (proven pattern)
- Balances customization with consistency
- Aligns with PAT-001 (Tiered Extraction Pipeline)

**Cons:**
- Moderate complexity
- Cross-skill coordination needed

---

### 5. Communication Pattern Analysis

#### 5.1 Data Flow Requirements

```
INPUT                    PROCESSING                    OUTPUT
─────                    ──────────                    ──────

VTT/SRT/TXT  ───►  ┌──────────────────┐
    File          │ Transcript Parser │
                  │  ─────────────────│  ───► Canonical Transcript
                  │  - Format detect  │            Model
                  │  - Parse cues     │
                  │  - Normalize      │
                  └──────────────────┘
                           │
                           ▼
                  ┌──────────────────┐
                  │ Entity Extractor  │
                  │  ─────────────────│  ───► Extracted Entities
                  │  - Speakers       │        (with confidence)
                  │  - Action items   │
                  │  - Decisions      │
                  │  - Questions      │
                  └──────────────────┘
                           │
                           ▼
                  ┌──────────────────┐
                  │ Output Formatter  │  ───► MD/JSON Output
                  │  ─────────────────│
                  │  - Format select  │
                  │  - Schema version │
                  │  - Citations      │
                  └──────────────────┘
```

#### 5.2 Inter-Agent Communication

| From | To | Data Passed | Mechanism |
|------|----|-------------|-----------|
| Parser | Extractor | Canonical Transcript (JSON) | Memory/File |
| Extractor | Formatter | Entity List (JSON) | Memory/File |
| Formatter | Output | Formatted Document | File |
| Extractor | ps-critic | Quality Check Request | Skill invocation |
| ps-critic | Extractor | Feedback/Score | Review response |

#### 5.3 Orchestration Model

**Recommended:** Skill-level orchestrator with sequential flow + optional critic loop.

```
SKILL.md (Orchestrator)
        │
        ├──► transcript-parser.md      [REQUIRED]
        │           │
        │           ▼
        ├──► entity-extractor.md       [REQUIRED]
        │           │
        │    ┌──────┴──────┐
        │    │  QUALITY    │
        │    │   CHECK     │
        │    └──────┬──────┘
        │           │
        │           ▼
        ├──► @problem-solving ps-critic [IF quality_threshold not met]
        │           │
        │           │ (feedback loop back to extractor)
        │           ▼
        └──► output-formatter.md       [REQUIRED]
                    │
                    ▼
              Final Output (MD/JSON)
```

---

## L2: Architectural Implications (Principal Architect)

### 6. Strategic Considerations

#### 6.1 One-Way Door Decisions

| Decision | Type | Risk | Notes |
|----------|------|------|-------|
| Custom vs. Extend | Two-way | LOW | Can migrate later |
| Agent boundaries | Two-way | LOW | Can refactor |
| Orchestration model | Two-way | LOW | SKILL.md is configurable |
| Inter-agent protocol | **One-way** | MEDIUM | Changing later breaks compatibility |
| Constitutional compliance | **One-way** | HIGH | Jerry Constitution is foundational |

**Critical Decision:** Inter-agent data format. Must define upfront:
- Canonical Transcript Model (input to extractor)
- Entity Result Model (output from extractor)
- Quality Report Model (from ps-critic)

#### 6.2 Trade-Off Analysis

| Factor | Extend Existing | Custom Agents | Hybrid |
|--------|-----------------|---------------|--------|
| Development Speed | FAST | SLOW | MEDIUM |
| Domain Isolation | LOW | HIGH | HIGH |
| Reuse of Jerry Patterns | HIGH | LOW | HIGH |
| Maintenance Burden | LOW | HIGH | MEDIUM |
| Flexibility | LOW | HIGH | HIGH |
| P-003 Compliance | EASY | EASY | NEEDS CARE |
| Quality Assurance | MANUAL | MANUAL | ps-critic LOOP |

**Recommendation:** Hybrid approach scores best overall.

#### 6.3 Risk Assessment

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| P-003 Violation (nested agents) | MEDIUM | HIGH | Clear orchestrator-only invocation |
| Agent boundary confusion | LOW | MEDIUM | Document responsibilities clearly |
| Performance bottleneck at LLM tier | MEDIUM | MEDIUM | Make LLM opt-in, default to rule-based |
| Context rot in long transcripts | MEDIUM | HIGH | Chunking strategy in parser |

#### 6.4 Alignment with Requirements

| Requirement | How Hybrid Approach Satisfies |
|-------------|------------------------------|
| IR-005 (Hexagonal) | Custom agents encapsulate domain logic |
| PAT-001 (Tiered Pipeline) | Entity extractor implements 3 tiers |
| PAT-004 (Citations) | ps-critic validates citation presence |
| NFR-001 (<10s) | Rule-based default meets performance |
| NFR-004 (F1>=0.80) | Tiered approach with LLM fallback |

#### 6.5 Future Extensibility

The hybrid architecture supports:
1. **New entity types** - Add to entity-extractor without changing others
2. **New formats** - Add to transcript-parser (e.g., ASS subtitles)
3. **New outputs** - Add to output-formatter (e.g., YAML, CSV)
4. **Quality improvements** - Upgrade ps-critic prompts without code changes

---

## 7. Recommendations for ADR-001

Based on this research, the ps-architect should consider:

### Primary Recommendation: Hybrid Architecture

**Decision:** Create 3 custom Transcript Skill agents that integrate with Jerry's problem-solving skill for quality assurance.

**Agents to Create:**
1. **transcript-parser** - VTT/SRT/TXT parsing and normalization
2. **entity-extractor** - Multi-entity extraction with confidence scoring
3. **output-formatter** - MD/JSON output generation with citations

**Jerry Integration:**
- Use `@problem-solving ps-critic` for quality gate reviews
- Follow Jerry agent template structure (YAML + XML)
- Comply with all constitutional principles

### Alternative Options for ADR

1. **Option A: Extend Existing** - Use ps-researcher/ps-analyst with prompts only
2. **Option B: Full Custom** - Build all agents from scratch including review
3. **Option C: Hybrid** (recommended) - Custom domain agents + ps-critic integration

---

## 8. References

### 8.1 Primary Sources (Authoritative)

| # | Reference | Type | Citation |
|---|-----------|------|----------|
| 1 | Jerry PS Agent Template | Framework | `skills/problem-solving/agents/PS_AGENT_TEMPLATE.md` |
| 2 | Jerry Problem-Solving SKILL | Framework | `skills/problem-solving/SKILL.md` |
| 3 | REQUIREMENTS-SPECIFICATION | Project | `EN-003.../requirements/REQUIREMENTS-SPECIFICATION.md` |
| 4 | Microsoft AI Agent Patterns | Industry | https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/ai-agent-design-patterns |
| 5 | Google Agentic AI Patterns | Industry | Google Cloud documentation |

### 8.2 Secondary Sources (Informative)

| # | Reference | Type | Citation |
|---|-----------|------|----------|
| 6 | Anthropic Agent Skills | Industry | https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills |
| 7 | Jerry Constitution v1.0 | Framework | `docs/governance/JERRY_CONSTITUTION.md` |
| 8 | Orchestration Skill | Framework | `skills/orchestration/SKILL.md` |

### 8.3 Tertiary Sources (Background)

| # | Reference | Type | Citation |
|---|-----------|------|----------|
| 9 | 26 Jerry Agent Files | Framework | `skills/**/agents/*.md` (Glob result) |
| 10 | EN-001 Market Analysis | Project | `EN-001.../research/` artifacts |
| 11 | EN-002 Technical Standards | Project | `EN-002.../research/` artifacts |

---

## Document Metadata

| Field | Value |
|-------|-------|
| Document ID | ADR-001-RESEARCH |
| Created | 2026-01-26 |
| Author | ps-researcher agent |
| Status | COMPLETE |
| Quality Score | Ready for synthesis |
| Word Count | ~2,500 |
| Next Step | ps-architect drafts ADR-001 |

---

*Generated by ps-researcher agent v2.2.0*
*Constitutional Compliance: P-002 (persisted), P-004 (provenance), P-011 (evidence-based)*
