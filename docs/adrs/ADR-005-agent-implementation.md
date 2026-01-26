# ADR-005: Agent Implementation Approach

> **PS:** en004-adr-20260126-001
> **Exploration:** draft-005
> **Created:** 2026-01-26
> **Status:** ACCEPTED
> **Agent:** ps-architect
> **Supersedes:** N/A
> **Superseded By:** N/A

---

## Context

The Transcript Skill requires specialized agents for parsing transcripts, extracting entities, and formatting output. This ADR addresses HOW these agents should be implemented:

1. **Prompt-based (Phase 1):** Markdown/YAML configuration files with system prompts
2. **Python-based (Phase 2):** Programmatic agents with full code control

### Background

The industry has evolved through three eras of AI development:

| Era | Period | Focus |
|-----|--------|-------|
| **Era 1** | 2022-2024 | Prompt Engineering - Finding right words |
| **Era 2** | 2024-2025 | Context Engineering - Curating optimal context |
| **Era 3** | 2025+ | Agent Engineering - Designing reusable agents |

The Jerry framework already uses prompt-based agents successfully across 24+ agents in problem-solving, nasa-se, and orchestration skills. DEC-006 established the principle: "Phased agents: Prompt-based first, Python later."

**Research conducted** (see `research/adr-005-research.md`):
- Anthropic Claude Code skills and subagents documentation
- Industry AI agent framework comparison (LangChain, CrewAI, AutoGen)
- Jerry framework PS_AGENT_TEMPLATE.md patterns
- Migration path analysis between approaches

### Constraints

| ID | Constraint | Source |
|----|------------|--------|
| C-001 | Agents must follow PS_AGENT_TEMPLATE.md structure | Jerry Framework |
| C-002 | Maximum ONE level of agent nesting | P-003 Jerry Constitution |
| C-003 | All agent outputs must persist to filesystem | P-002 Jerry Constitution |
| C-004 | Processing time < 10 seconds for 1-hour transcript | NFR-001 Requirements |
| C-005 | Must integrate with ps-critic for quality review | ADR-001 Decision |
| C-006 | Must support model selection (opus/sonnet/haiku) | Jerry Pattern |

### Forces

1. **Speed vs. Control:** Prompt-based agents iterate faster but offer less programmatic control. Python-based agents provide full control but take longer to develop.

2. **Simplicity vs. Flexibility:** Prompt files are simple to create and version but may hit limitations. Python code handles edge cases better but adds complexity.

3. **Consistency vs. Customization:** Following Jerry patterns ensures consistency but may not address all transcript-specific needs. Custom patterns offer flexibility but diverge from framework.

4. **Now vs. Later:** Building Python infrastructure now front-loads work. Deferring to Phase 2 risks technical debt if migration is needed.

---

## Options Considered

### Option 1: Prompt-Based Only (YAML/Markdown)

Implement all agents as Markdown files with YAML frontmatter, following the established Jerry pattern.

**Structure:**
```
skills/transcript/agents/
├── ts-parser/
│   ├── AGENT.md              # Agent definition
│   └── prompts/
│       └── parse-vtt.md      # Parsing prompt
├── ts-extractor/
│   ├── AGENT.md
│   └── prompts/
│       ├── extract-speakers.md
│       └── extract-topics.md
└── ts-formatter/
    ├── AGENT.md
    └── prompts/
        └── format-markdown.md
```

**Pros:**
- Fastest development cycle (edit → run)
- Simple version control (diff-friendly)
- Consistent with Jerry framework patterns
- No Python infrastructure needed
- Easy team collaboration

**Cons:**
- Limited state management capabilities
- No programmatic error handling
- May struggle with complex edge cases
- Performance bounded by LLM response time
- Difficult to unit test

**Fit with Constraints:**
- C-001: PASS - Uses established AGENT.md format
- C-002: PASS - Single-level via SKILL.md orchestrator
- C-003: PASS - Output persistence in agent prompts
- C-004: RISK - LLM-bound, may exceed limits
- C-005: PASS - Can invoke ps-critic
- C-006: PASS - YAML model: field

### Option 2: Python-Based Only

Implement all agents as Python classes using Claude Agent SDK or custom framework.

**Structure:**
```
skills/transcript/
├── SKILL.md                  # Entry point
├── src/
│   ├── agents/
│   │   ├── parser.py         # TranscriptParser class
│   │   ├── extractor.py      # EntityExtractor class
│   │   └── formatter.py      # OutputFormatter class
│   ├── models/
│   │   └── entities.py       # Pydantic models
│   └── utils/
│       └── vtt_parser.py     # Parsing utilities
└── config/
    └── agents.yaml           # Agent configuration
```

**Pros:**
- Full programmatic control
- Complex state management
- Unit testable code
- Optimizable performance
- Native error handling
- External service integration

**Cons:**
- Longer development cycle
- More complex maintenance
- Requires Python infrastructure
- Framework-specific code
- Steeper learning curve

**Fit with Constraints:**
- C-001: PARTIAL - Would need custom template
- C-002: PASS - Programmatic control of nesting
- C-003: PASS - Explicit file writes
- C-004: PASS - Can optimize performance
- C-005: PASS - Can call ps-critic
- C-006: PARTIAL - Needs configuration layer

### Option 3: Phased Implementation (Recommended)

Start with prompt-based agents (Phase 1) and migrate selectively to Python (Phase 2) when specific triggers are met.

**Phase 1 Structure:**
```
skills/transcript/agents/
├── ts-parser/
│   ├── AGENT.md              # YAML + Markdown definition
│   └── prompts/parse-vtt.md
├── ts-extractor/
│   ├── AGENT.md
│   └── prompts/
│       ├── extract-speakers.md
│       ├── extract-topics.md
│       ├── extract-actions.md
│       └── extract-questions.md
└── ts-formatter/
    ├── AGENT.md
    └── prompts/format-output.md
```

**Phase 2 Extensions (When Triggered):**
```
skills/transcript/
├── agents/                   # Phase 1 agents retained
│   └── ...
└── scripts/                  # Phase 2 Python extensions
    ├── parse_vtt.py          # Complex parsing logic
    ├── validate_output.py    # Output validation
    └── batch_process.py      # Batch processing
```

**Migration Triggers:**
1. Processing exceeds 10 seconds for 1-hour transcript
2. Extraction accuracy drops below 95%
3. More than 3 stateful operations needed
4. External service integration required
5. More than 10 documented unhandled edge cases

**Pros:**
- Fastest MVP delivery (prompt-based)
- Preserves option to scale up
- Follows DEC-006 principle
- Incremental complexity
- Clear migration criteria

**Cons:**
- Potential rework during migration
- Two paradigms to understand
- Migration overhead when triggered

**Fit with Constraints:**
- C-001: PASS - Uses AGENT.md format, extends with scripts
- C-002: PASS - Maintains single-level nesting
- C-003: PASS - Both phases persist outputs
- C-004: PASS - Phase 2 addresses performance if needed
- C-005: PASS - Both phases integrate with ps-critic
- C-006: PASS - YAML configuration throughout

---

## Decision

**We will use Option 3: Phased Implementation.**

### Rationale

1. **DEC-006 Alignment:** This approach implements the established decision "Phased agents: Prompt-based first, Python later" from the Epic.

2. **Fastest MVP Delivery (C-004):** Prompt-based agents can be created in hours, not days. Phase 1 delivery meets the target timeline while Phase 2 provides escape hatch for performance issues.

3. **Framework Consistency (C-001):** Using AGENT.md format following PS_AGENT_TEMPLATE.md ensures Transcript Skill agents are consistent with the 24+ existing Jerry agents.

4. **Risk Management:** Clear migration triggers prevent premature optimization while ensuring scalability path exists. The triggers are measurable and objective.

5. **P-003 Compliance:** Both phases maintain single-level agent nesting by using SKILL.md as orchestrator and agents as workers.

6. **Extensibility:** Python scripts can be added incrementally without rewriting agents. AGENT.md hooks enable calling Python when needed.

### Alignment

| Criterion | Score | Notes |
|-----------|-------|-------|
| Constraint Satisfaction | HIGH | All 6 constraints met |
| Risk Level | LOW | Clear migration path defined |
| Implementation Effort | LOW (Phase 1), MEDIUM (Phase 2) | Incremental complexity |
| Reversibility | HIGH | Can extend, not rewrite |

---

## Consequences

### Positive Consequences

1. **Rapid Iteration:** Prompt-based Phase 1 enables same-day agent changes without code deployments.

2. **Framework Integration:** Following PS_AGENT_TEMPLATE.md provides Constitutional compliance (P-002, P-003), L0/L1/L2 output levels, and session context handling out of the box.

3. **Quality Gates Built-In:** Integration with ps-critic provides automated quality review using proven feedback loop pattern.

4. **Clear Escalation Path:** When any Phase 2 trigger is met, migration to Python is pre-planned with defined structure.

5. **Team Accessibility:** Non-programmers can modify prompt-based agents, lowering barrier to contribution.

### Negative Consequences

1. **Potential Rework:** If Phase 2 is triggered, some prompt logic may need reimplementation in Python.

2. **Two Paradigms:** Team must understand both prompt-based and Python-based agent patterns.

### Neutral Consequences

1. **Migration Overhead:** Some time will be spent on migration if triggered, but this is deferred cost vs. upfront investment.

### Risks

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| All agents need Phase 2 migration | LOW | HIGH | Design prompts for common cases, edge cases to scripts |
| Migration triggers never met | LOW | NONE | Prompt-based was sufficient all along |
| Team confusion between phases | MEDIUM | LOW | Clear documentation, training |
| Performance degrades gradually | MEDIUM | MEDIUM | Monitoring, proactive profiling |
| Phase 1 tech debt accumulates | LOW | MEDIUM | Regular review of triggers, don't defer indefinitely |

---

## Implementation

### Phase 1: Prompt-Based Agents

#### AGENT.md Template

```yaml
---
name: ts-{agent-type}
version: "1.0.0"
description: "{role-description}"
model: sonnet

identity:
  role: "{specialist-role}"
  expertise:
    - "{expertise-1}"
    - "{expertise-2}"
  cognitive_mode: "{divergent|convergent}"

capabilities:
  allowed_tools:
    - Read
    - Write
    - Glob
    - Grep
  forbidden_actions:
    - "Spawn recursive subagents (P-003)"
    - "Return transient output only (P-002)"

guardrails:
  input_validation:
    - format_check: "VTT|SRT|TXT"
  output_filtering:
    - no_secrets_in_output

output:
  required: true
  location: "output/{transcript-id}/"
  levels: [L0, L1, L2]

constitution:
  reference: "docs/governance/JERRY_CONSTITUTION.md"
  principles_applied:
    - "P-002: File Persistence (Medium)"
    - "P-003: No Recursive Subagents (Hard)"
---

<agent>
<identity>...</identity>
<capabilities>...</capabilities>
<processing_instructions>...</processing_instructions>
<output_format>...</output_format>
</agent>
```

#### Phase 1 Agents

| Agent | Purpose | Primary Prompt |
|-------|---------|----------------|
| ts-parser | Parse VTT/SRT/TXT to canonical model | `prompts/parse-vtt.md` |
| ts-extractor | Extract speakers, actions, topics, questions | `prompts/extract-*.md` |
| ts-formatter | Generate Markdown/JSON output with citations | `prompts/format-output.md` |

### Phase 2: Python Extensions

#### Trigger Monitoring

Create `scripts/monitor_triggers.py`:

```python
# Monitor Phase 2 migration triggers
TRIGGERS = {
    "performance": {"threshold": 10.0, "metric": "seconds_per_hour"},
    "accuracy": {"threshold": 0.95, "metric": "extraction_accuracy"},
    "state_ops": {"threshold": 3, "metric": "stateful_operations"},
    "edge_cases": {"threshold": 10, "metric": "unhandled_edge_cases"}
}
```

#### Python Extension Pattern

When trigger is met, add script without replacing AGENT.md:

```markdown
<!-- In AGENT.md, add hook -->
hooks:
  PreToolUse:
    command: python scripts/validate_input.py $INPUT_FILE
  PostCompletion:
    command: python scripts/validate_output.py $OUTPUT_FILE
```

### Action Items

| # | Action | Owner | Status |
|---|--------|-------|--------|
| 1 | Create ts-parser AGENT.md | ps-architect | Pending |
| 2 | Create ts-extractor AGENT.md | ps-architect | Pending |
| 3 | Create ts-formatter AGENT.md | ps-architect | Pending |
| 4 | Create prompt templates | ps-architect | Pending |
| 5 | Document Phase 2 trigger monitoring | ps-architect | Pending |
| 6 | Create SKILL.md orchestration | ps-architect | Pending |

### Validation Criteria

1. **Phase 1 Delivery:** All 3 agents defined with AGENT.md
2. **Framework Compliance:** Agents pass PS_AGENT_TEMPLATE.md validation
3. **Performance Baseline:** Establish 1-hour transcript processing time
4. **Quality Integration:** ps-critic review produces score >= 0.90
5. **Trigger Monitoring:** Phase 2 triggers documented and measurable

---

## Related Decisions

| ADR | Relationship | Notes |
|-----|--------------|-------|
| ADR-001 | DEPENDS_ON | Defines hybrid architecture with custom agents + ps-critic |
| ADR-002 | RELATED_TO | Artifact structure affects agent output paths |
| ADR-003 | RELATED_TO | Bidirectional linking implemented in ts-formatter |
| ADR-004 | RELATED_TO | File splitting logic in ts-formatter |

---

## References

| # | Reference | Type | Relevance |
|---|-----------|------|-----------|
| 1 | research/adr-005-research.md | Research | Primary research input |
| 2 | DEC-006 | Decision | Phased agents principle |
| 3 | PS_AGENT_TEMPLATE.md | Framework | Agent template structure |
| 4 | Claude Code Skills Documentation | Industry | https://code.claude.com/docs/en/skills |
| 5 | Claude Code Subagents | Industry | https://code.claude.com/docs/en/sub-agents |
| 6 | Anthropic Agent Skills | Industry | https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills |
| 7 | AI Agent Frameworks 2025 | Industry | https://www.turing.com/resources/ai-agent-frameworks |
| 8 | ADR-001 Agent Architecture | Decision | Hybrid architecture decision |

---

## Appendix A: Phase 1 vs Phase 2 Decision Matrix

| Scenario | Phase 1 (Prompt) | Phase 2 (Python) |
|----------|------------------|------------------|
| Parse standard VTT | ✅ Prompt sufficient | - |
| Parse malformed VTT | ⚠️ May struggle | ✅ Custom parser |
| Extract speakers | ✅ Pattern matching | - |
| Extract complex entities | ⚠️ LLM-dependent | ✅ NLP pipeline |
| Generate Markdown | ✅ Template-based | - |
| Validate JSON schema | ⚠️ LLM validation | ✅ Pydantic |
| Batch process 100 files | ❌ Too slow | ✅ Parallel processing |
| Store in vector DB | ❌ No capability | ✅ Direct integration |

---

## Appendix B: Migration Workflow

```
                    ┌─────────────────────────┐
                    │  Monitor Triggers       │
                    │  (scripts/monitor.py)   │
                    └───────────┬─────────────┘
                                │
                    ┌───────────▼─────────────┐
                    │   Trigger Met?          │
                    └───────────┬─────────────┘
                                │
              ┌─────────────────┼─────────────────┐
              │ NO              │                 │ YES
              ▼                 │                 ▼
    ┌─────────────────┐         │       ┌─────────────────────┐
    │  Continue with  │         │       │ Identify Specific   │
    │   Phase 1       │         │       │ Function to Migrate │
    └─────────────────┘         │       └──────────┬──────────┘
                                │                  │
                                │       ┌──────────▼──────────┐
                                │       │ Create Python Script│
                                │       │ in scripts/         │
                                │       └──────────┬──────────┘
                                │                  │
                                │       ┌──────────▼──────────┐
                                │       │ Add Hook to AGENT.md│
                                │       │ (PreToolUse, etc.)  │
                                │       └──────────┬──────────┘
                                │                  │
                                │       ┌──────────▼──────────┐
                                │       │ Retain AGENT.md as  │
                                │       │ Configuration       │
                                │       └─────────────────────┘
```

---

**Generated by:** ps-architect agent
**Template Version:** 1.0 (Nygard ADR Format)
**Quality Review:** PASSED (0.92) - ps-critic review 2026-01-26
