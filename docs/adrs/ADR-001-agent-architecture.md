# ADR-001: Agent Architecture for Transcript Skill

> **PS:** en004-adr-20260126-001
> **Exploration:** draft-001
> **Created:** 2026-01-26
> **Status:** ACCEPTED
> **Agent:** ps-architect
> **Supersedes:** N/A
> **Superseded By:** N/A

---

## Context

The Transcript Skill needs to process VTT/SRT/TXT transcript files and extract structured information (speakers, action items, decisions, questions). This requires defining an agent architecture that:

1. Handles domain-specific transcript processing tasks
2. Integrates with the existing Jerry framework
3. Maintains quality through review mechanisms
4. Complies with Jerry Constitutional principles (P-002, P-003, P-022)

### Background

The Jerry framework already provides 24+ specialized agents across multiple skills:
- **problem-solving**: 8 agents (ps-researcher, ps-analyst, ps-architect, ps-critic, etc.)
- **nasa-se**: 10 agents for systems engineering processes
- **orchestration**: 3 agents for workflow coordination
- **worktracker**: 2 agents for task management

The Transcript Skill must decide whether to extend existing agents, create fully custom agents, or adopt a hybrid approach.

**Research conducted** (see `research/adr-001-research.md`):
- Jerry Framework agent patterns and templates
- Microsoft Azure AI Agent Design Patterns (Sequential, Concurrent, Handoff)
- Google Cloud Agentic AI Patterns (Multi-Agent Sequential, Review & Critique)
- Requirements from EN-003 (40 requirements, including IR-005 Hexagonal Architecture)

### Constraints

| ID | Constraint | Source |
|----|------------|--------|
| C-001 | Maximum ONE level of agent nesting (orchestrator → worker) | P-003 Jerry Constitution |
| C-002 | All agent outputs must persist to filesystem | P-002 Jerry Constitution |
| C-003 | Must integrate with SKILL.md interface | IR-004 Requirements |
| C-004 | Must follow hexagonal architecture patterns | IR-005 Requirements |
| C-005 | Processing time < 10 seconds for 1-hour transcript | NFR-001 Requirements |
| C-006 | Agent prompts must follow XML tag structure | Anthropic Best Practice |

### Forces

1. **Consistency vs. Customization:** Extending existing Jerry agents ensures consistency but limits domain-specific behavior. Custom agents provide flexibility but may diverge from framework patterns.

2. **Performance vs. Quality:** Rule-based extraction is fast but less accurate. LLM-based extraction is accurate but slower. Need tiered approach per PAT-001.

3. **Simplicity vs. Extensibility:** Fewer agents are simpler to maintain but may become monolithic. More agents provide better separation but increase coordination complexity.

4. **Reuse vs. Domain Isolation:** Reusing ps-* agents leverages proven patterns but mixes domains. Custom agents maintain domain boundaries but duplicate infrastructure.

---

## Options Considered

### Option 1: Extend Existing Jerry Agents (Prompt-Only)

Use existing ps-researcher, ps-analyst, and ps-architect agents with domain-specific prompts for transcript processing.

**Structure:**
```
skills/transcript/
├── SKILL.md (orchestrator)
└── prompts/
    ├── parse-transcript.md      # Prompt for ps-researcher
    ├── extract-entities.md      # Prompt for ps-analyst
    └── format-output.md         # Prompt for ps-architect
```

**Pros:**
- Minimal new code; leverages existing, tested agents
- Automatic compliance with Jerry patterns
- Fast to implement (days, not weeks)
- Consistent with other Jerry skills

**Cons:**
- ps-* agents designed for problem-solving, not data processing pipelines
- No domain isolation; transcript logic mixed with general-purpose agents
- Limited customization; can only tune via prompts
- May confuse agent responsibilities over time

**Fit with Constraints:**
- C-001: PASS - Uses existing orchestration model
- C-002: PASS - ps-* agents already persist outputs
- C-003: PASS - SKILL.md can invoke ps-* agents
- C-004: PARTIAL - No domain layer isolation for transcript entities
- C-005: RISK - LLM-heavy approach may exceed time limits
- C-006: PASS - Prompts can use XML structure

### Option 2: Fully Custom Agents

Create 3+ new agents specific to transcript processing with no dependency on ps-* agents.

**Structure:**
```
skills/transcript/
├── SKILL.md (orchestrator)
├── agents/
│   ├── transcript-parser.md      # Custom parser agent
│   ├── entity-extractor.md       # Custom extraction agent
│   ├── output-formatter.md       # Custom formatting agent
│   └── quality-reviewer.md       # Custom review agent
└── prompts/
    └── (agent-specific prompts)
```

**Pros:**
- Complete domain isolation for transcript logic
- Purpose-built agents optimized for transcript domain
- Full control over agent behavior and tooling
- Clean separation from problem-solving skill

**Cons:**
- Reinvents review/quality patterns that ps-critic already provides
- More code to write, test, and maintain
- May diverge from Jerry conventions over time
- Longer development timeline

**Fit with Constraints:**
- C-001: PASS - Custom orchestrator controls nesting
- C-002: PASS - Custom agents can implement persistence
- C-003: PASS - SKILL.md remains entry point
- C-004: PASS - Domain isolation achieved
- C-005: PASS - Can optimize for performance
- C-006: PASS - Templates follow XML structure

### Option 3: Hybrid Architecture (Recommended)

Create custom domain-specific agents for transcript processing tasks, but reuse Jerry's ps-critic agent for quality assurance.

**Structure:**
```
skills/transcript/
├── SKILL.md (orchestrator)
├── agents/
│   ├── transcript-parser.md      # Custom: VTT/SRT/TXT parsing
│   ├── entity-extractor.md       # Custom: Speaker/action/decision extraction
│   └── output-formatter.md       # Custom: MD/JSON output generation
└── prompts/
    └── (agent-specific prompts)

# Integration with existing Jerry agents:
# - @problem-solving ps-critic for quality review
# - @problem-solving ps-researcher for optional deep analysis
```

**Pros:**
- Domain-specific agents for parsing, extraction, and formatting
- Reuses proven ps-critic review pattern for quality gates
- Balances customization with consistency
- Aligns with PAT-001 (Tiered Extraction Pipeline) from requirements
- Maintains hexagonal architecture (custom domain + existing application)

**Cons:**
- Moderate complexity; cross-skill coordination needed
- Two agent "families" to understand (transcript + ps-*)
- Requires clear documentation of integration points

**Fit with Constraints:**
- C-001: PASS - SKILL.md is orchestrator; ps-critic called as worker
- C-002: PASS - Custom agents implement persistence; ps-critic already persists
- C-003: PASS - SKILL.md remains single entry point
- C-004: PASS - Custom agents form domain layer; ps-critic is application layer
- C-005: PASS - Custom agents can use rule-based defaults
- C-006: PASS - All agents follow XML template structure

---

## Decision

**We will use Option 3: Hybrid Architecture.**

### Rationale

1. **Domain Isolation (C-004):** Custom agents encapsulate transcript-specific logic (parsing VTT voice tags, detecting action item patterns, formatting JSON schema). This creates a clean domain boundary per hexagonal architecture.

2. **Proven Quality Pattern:** The ps-critic agent has demonstrated value in EN-003 (quality score 0.903). Reusing it avoids reinventing quality review logic.

3. **Tiered Extraction (PAT-001):** The entity-extractor agent can implement Rule → ML → LLM tiers internally, meeting both NFR-001 (performance) and NFR-004 (accuracy) requirements.

4. **P-003 Compliance:** The SKILL.md orchestrator invokes custom agents and ps-critic as workers. No agent invokes another agent, maintaining single-level nesting.

5. **Extensibility:** Adding new entity types (e.g., sentiment analysis) requires only extending entity-extractor, not changing the overall architecture.

### Alignment

| Criterion | Score | Notes |
|-----------|-------|-------|
| Constraint Satisfaction | HIGH | All 6 constraints met |
| Risk Level | LOW | Proven patterns, limited new code |
| Implementation Effort | MEDIUM | 3 custom agents + integration |
| Reversibility | HIGH | Can migrate to full custom later |

---

## Consequences

### Positive Consequences

1. **Clean Domain Model:** Transcript parsing and entity extraction logic isolated in custom agents, following IR-005 hexagonal architecture requirement.

2. **Quality Assurance Built-In:** Integration with ps-critic provides automated quality review using proven feedback loop pattern.

3. **Performance Optimized:** Custom agents can implement rule-based extraction as default, meeting NFR-001 (<10s processing).

4. **Framework Consistency:** Reusing ps-critic ensures Transcript Skill follows same quality patterns as other Jerry skills.

5. **Clear Responsibilities:**
   - transcript-parser: Format detection, parsing, normalization
   - entity-extractor: Speaker, action, decision, question extraction
   - output-formatter: Markdown/JSON generation with citations
   - ps-critic: Quality review and feedback

### Negative Consequences

1. **Integration Complexity:** Cross-skill invocation (transcript → problem-solving) requires documentation and testing.

2. **Dual Agent Patterns:** Team must understand both transcript agent conventions and ps-* agent conventions.

### Neutral Consequences

1. **Template Reuse:** Custom agents will use PS_AGENT_TEMPLATE.md structure with transcript-specific modifications.

### Risks

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| ps-critic integration issues | LOW | MEDIUM | Test cross-skill invocation in isolation first |
| Custom agent drift from Jerry patterns | LOW | LOW | Use PS_AGENT_TEMPLATE.md as base |
| Performance regression with ps-critic loop | MEDIUM | LOW | Make critic review optional; threshold-based |
| Context rot in long transcripts | MEDIUM | HIGH | Implement chunking in transcript-parser |

---

## Implementation

### Action Items

| # | Action | Owner | Status |
|---|--------|-------|--------|
| 1 | Create transcript-parser agent (AGENT.md) | ps-architect | Pending |
| 2 | Create entity-extractor agent (AGENT.md) | ps-architect | Pending |
| 3 | Create output-formatter agent (AGENT.md) | ps-architect | Pending |
| 4 | Define inter-agent data contracts (JSON schemas) | ps-architect | Pending |
| 5 | Document ps-critic integration protocol | ps-architect | Pending |
| 6 | Create SKILL.md orchestration logic | ps-architect | Pending |

### Validation Criteria

1. **Unit Test:** Each custom agent processes test transcript correctly
2. **Integration Test:** Full pipeline (parse → extract → format) produces expected output
3. **Quality Test:** ps-critic review passes with score >= 0.90
4. **Performance Test:** 1-hour transcript processed in < 10 seconds (rule-based mode)
5. **Compliance Test:** All agents persist outputs to filesystem (P-002)

---

## Related Decisions

| ADR | Relationship | Notes |
|-----|--------------|-------|
| ADR-002 | DEPENDS_ON | Artifact structure affects agent outputs |
| ADR-003 | RELATED_TO | Bidirectional linking affects citations |
| ADR-004 | RELATED_TO | File splitting may affect agent boundaries |
| ADR-005 | DEPENDS_ON | Agent implementation approach (prompt vs Python) |

---

## References

| # | Reference | Type | Relevance |
|---|-----------|------|-----------|
| 1 | research/adr-001-research.md | Research Artifact | Primary research input |
| 2 | REQUIREMENTS-SPECIFICATION.md | Requirements | FR-001 to FR-015, IR-004, IR-005 |
| 3 | Microsoft AI Agent Design Patterns | Industry | Sequential/Concurrent patterns |
| 4 | Google Agentic AI Patterns | Industry | Review & Critique pattern |
| 5 | PS_AGENT_TEMPLATE.md | Framework | Agent template structure |
| 6 | Jerry Constitution v1.0 | Governance | P-002, P-003, P-022 constraints |
| 7 | SKILL.md (problem-solving) | Framework | ps-critic integration reference |

---

## PS Integration

| Action | Command | Status |
|--------|---------|--------|
| Exploration Entry | `add-entry en004-adr-20260126-001 "Decision: Agent Architecture"` | Done (draft-001) |
| Entry Type | `--type DECISION` | Done |
| Artifact Link | `link-artifact en004-adr-20260126-001 draft-001 FILE "docs/adrs/ADR-001-agent-architecture.md"` | Done |

---

## Appendix A: Agent Responsibilities Matrix

| Agent | Primary Responsibility | Inputs | Outputs |
|-------|----------------------|--------|---------|
| transcript-parser | Parse VTT/SRT/TXT to canonical model | Raw transcript file | Canonical Transcript JSON |
| entity-extractor | Extract speakers, actions, decisions, questions | Canonical Transcript | Entity List JSON |
| output-formatter | Generate MD/JSON output with citations | Entity List | Final output file |
| ps-critic | Review extraction quality | Entity List + Transcript | Quality Report |

## Appendix B: Data Flow Diagram

```
                              ┌─────────────────────────────────────────────────┐
                              │           TRANSCRIPT SKILL (SKILL.md)           │
                              │                  ORCHESTRATOR                    │
                              └───────────────────────┬─────────────────────────┘
                                                      │
                    ┌─────────────────────────────────┼─────────────────────────────────┐
                    │                                 │                                 │
                    ▼                                 ▼                                 ▼
         ┌───────────────────┐           ┌───────────────────┐           ┌───────────────────┐
         │ TRANSCRIPT-PARSER │           │ ENTITY-EXTRACTOR  │           │ OUTPUT-FORMATTER  │
         │     (Custom)      │           │     (Custom)      │           │     (Custom)      │
         ├───────────────────┤           ├───────────────────┤           ├───────────────────┤
         │ - Format detect   │           │ - Rule-based      │           │ - Markdown gen    │
         │ - VTT parsing     │──────────►│ - ML-based (opt)  │──────────►│ - JSON gen        │
         │ - SRT parsing     │  Canonical│ - LLM-based (opt) │  Entity   │ - Citations       │
         │ - TXT parsing     │ Transcript│ - Confidence      │   List    │ - Schema version  │
         │ - Normalization   │   JSON    │ - Citations       │   JSON    │                   │
         └───────────────────┘           └─────────┬─────────┘           └───────────────────┘
                                                   │
                                                   │ Quality Check
                                                   ▼
                                        ┌───────────────────┐
                                        │     PS-CRITIC     │
                                        │ (@problem-solving)│
                                        ├───────────────────┤
                                        │ - Template check  │
                                        │ - Quality score   │
                                        │ - Feedback loop   │
                                        └───────────────────┘
```

---

**Generated by:** ps-architect agent
**Template Version:** 1.0 (Nygard ADR Format)
**Quality Review:** PASSED (0.92) - ps-critic review 2026-01-26
