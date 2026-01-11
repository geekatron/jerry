# PS Agent Portfolio Deep Analysis

**PS ID:** init-wt-skills
**Entry ID:** e-001
**Topic:** ps-* Agent Portfolio Deep Analysis
**Author:** ps-researcher agent (v2.0.0)
**Date:** 2026-01-11
**Status:** COMPLETE

---

## L0: Executive Summary (ELI5)

The Jerry framework contains eight specialized AI agents that work together like a team of consultants, each with their own expertise. Think of them as a consulting firm where:

- **ps-researcher** is the librarian who finds and validates information from many sources
- **ps-analyst** is the detective who figures out why problems happen using structured methods
- **ps-synthesizer** is the pattern-finder who connects dots across multiple documents
- **ps-validator** is the quality checker who verifies requirements are met
- **ps-reporter** is the communicator who creates status updates for different audiences
- **ps-architect** is the designer who makes and documents major technical decisions
- **ps-reviewer** is the critic who reviews work quality and finds issues
- **ps-investigator** is the incident responder who figures out what went wrong in failures

All eight agents follow the same "constitution" (a set of rules) that ensures they:
1. Always save their work to files (not just respond in chat)
2. Include citations and evidence for their claims
3. Never spawn too many sub-agents (one level deep only)
4. Present findings at three levels: simple (ELI5), technical (engineer), and strategic (architect)

This design means the agents can hand off work to each other in a pipeline - the researcher finds information, the analyst interprets it, the synthesizer combines patterns, and the reporter communicates results. The entire system is designed to fight "context rot" (AI performance degradation as conversations grow) by persistently storing everything to disk.

---

## L1: Technical Analysis (Software Engineer)

### 1.1 Common Structure Patterns

All 8 agents share an identical document structure with the following sections:

| Section | Purpose | Required |
|---------|---------|----------|
| YAML Frontmatter | Machine-readable metadata (name, version, capabilities, etc.) | YES |
| `<agent>` block | Agent definition containing identity, persona, capabilities | YES |
| `<identity>` | Role, expertise areas, cognitive mode | YES |
| `<persona>` | Tone, communication style, audience adaptation | YES |
| `<capabilities>` | Allowed tools, output formats, forbidden actions | YES |
| `<guardrails>` | Input validation, output filtering, fallback behavior | YES |
| `<constitutional_compliance>` | Constitution principles and self-critique checklist | YES |
| `<invocation_protocol>` | PS context requirements, mandatory persistence steps | YES |
| `<output_levels>` | L0/L1/L2 output structure definitions | YES |
| `<state_management>` | Output key, state schema, upstream/downstream agents | YES |
| Markdown documentation | Purpose, templates, invocation examples, verification | YES |

### 1.2 Capability Matrix

| Agent | Cognitive Mode | Primary Purpose | Unique Specialization |
|-------|---------------|-----------------|----------------------|
| ps-researcher | Divergent | Information gathering | Context7 MCP for library docs, 5W1H framework |
| ps-analyst | Convergent | Root cause & trade-off analysis | 5 Whys, FMEA, Ishikawa, decision matrices |
| ps-synthesizer | Convergent | Cross-document pattern extraction | Thematic analysis (Braun & Clarke), PAT/LES/ASM generation |
| ps-validator | Convergent | Constraint verification | Requirements traceability matrix, binary pass/fail |
| ps-reporter | Convergent | Status reporting | Health indicators, progress metrics, dashboards |
| ps-architect | Convergent | Architectural decisions | ADR (Nygard format), C4, DDD patterns |
| ps-reviewer | Convergent | Quality assessment | Google code review practices, OWASP, severity levels |
| ps-investigator | Convergent | Failure analysis | 5 Whys, Ishikawa, FMEA, corrective actions |

### 1.3 Tool Permissions Matrix

| Tool | researcher | analyst | synthesizer | validator | reporter | architect | reviewer | investigator |
|------|------------|---------|-------------|-----------|----------|-----------|----------|--------------|
| Read | YES | YES | YES | YES | YES | YES | YES | YES |
| Write | YES | YES | YES | YES | YES | YES | YES | YES |
| Edit | YES | YES | YES | YES | YES | YES | YES | YES |
| Glob | YES | YES | YES | YES | YES | YES | YES | YES |
| Grep | YES | YES | YES | YES | YES | YES | YES | YES |
| Bash | YES | YES | YES | YES | YES | YES | YES | YES |
| WebSearch | YES | YES | YES | - | - | YES | - | YES |
| WebFetch | YES | YES | YES | - | - | YES | - | YES |
| Task | YES | - | - | - | - | - | - | - |
| mcp__context7__* | YES | YES | YES | - | - | YES | - | YES |

**Key Observations:**
- **Core tools** (Read, Write, Edit, Glob, Grep, Bash): Universal across all agents
- **Web tools** (WebSearch, WebFetch): Available to research-oriented agents
- **Context7 MCP**: Available to agents that need library/framework documentation
- **Task tool**: Only available to ps-researcher (for single-level delegation per P-003)

### 1.4 Output Locations

| Agent | Output Directory | File Pattern |
|-------|-----------------|--------------|
| ps-researcher | `projects/${JERRY_PROJECT}/research/` | `{ps_id}-{entry_id}-{topic-slug}.md` |
| ps-analyst | `projects/${JERRY_PROJECT}/analysis/` | `{ps_id}-{entry_id}-{analysis-type}.md` |
| ps-synthesizer | `projects/${JERRY_PROJECT}/synthesis/` | `{ps_id}-{entry_id}-synthesis.md` |
| ps-validator | `projects/${JERRY_PROJECT}/analysis/` | `{ps_id}-{entry_id}-validation.md` |
| ps-reporter | `projects/${JERRY_PROJECT}/reports/` | `{ps_id}-{entry_id}-{report-type}.md` |
| ps-architect | `projects/${JERRY_PROJECT}/decisions/` | `{ps_id}-{entry_id}-adr-{slug}.md` |
| ps-reviewer | `projects/${JERRY_PROJECT}/reviews/` | `{ps_id}-{entry_id}-{review-type}.md` |
| ps-investigator | `projects/${JERRY_PROJECT}/investigations/` | `{ps_id}-{entry_id}-investigation.md` |

### 1.5 Constitutional Principles Applied

All agents apply these principles with the following enforcement levels:

| Principle | Enforcement | Universal Behavior |
|-----------|-------------|-------------------|
| P-001 (Truth/Accuracy) | Soft | All claims cite sources/evidence |
| P-002 (File Persistence) | **Medium** | ALL output MUST be persisted to files |
| P-003 (No Recursion) | **Hard** | Task tool spawns single-level only |
| P-004 (Provenance) | Soft | Methodology and sources documented |
| P-011 (Evidence-Based) | Soft | Recommendations tied to evidence |
| P-020 (User Authority) | **Hard** | ADRs marked PROPOSED until user approves |
| P-022 (No Deception) | **Hard** | Transparent about limitations/gaps |

### 1.6 Agent Relationship Diagram (Pipeline)

```
                    ┌─────────────────────────────────────────────────────────────────┐
                    │                     PS AGENT PIPELINE                            │
                    └─────────────────────────────────────────────────────────────────┘

    INFORMATION GATHERING                ANALYSIS & SYNTHESIS                    OUTPUT

    ┌─────────────────┐
    │  ps-researcher  │──────┐
    │   (divergent)   │      │
    │   5W1H, C7      │      │
    └─────────────────┘      │
                             │     ┌─────────────────┐
                             ├────►│   ps-analyst    │──────┐
                             │     │  (convergent)   │      │
                             │     │  5 Whys, FMEA   │      │
                             │     └─────────────────┘      │
                             │                              │
                             │     ┌─────────────────┐      │     ┌─────────────────┐
                             └────►│  ps-synthesizer │──────┼────►│   ps-reporter   │
                                   │  (convergent)   │      │     │  (convergent)   │
                                   │  PAT/LES/ASM    │      │     │  Status/Metrics │
                                   └─────────────────┘      │     └─────────────────┘
                                                            │              │
                                   ┌─────────────────┐      │              │
                                   │   ps-architect  │◄─────┤              │
                                   │  (convergent)   │      │              ▼
                                   │   ADRs, C4      │──────┤     ┌─────────────────┐
                                   └─────────────────┘      │     │  TERMINAL NODE  │
                                          │                 │     │ (reports end)   │
                                          ▼                 │     └─────────────────┘
                                   ┌─────────────────┐      │
                                   │  ps-validator   │◄─────┘
                                   │  (convergent)   │
                                   │  RTM, Evidence  │
                                   └─────────────────┘
                                          │
                                          ▼
                                   ┌─────────────────┐
                                   │   ps-reviewer   │
                                   │  (convergent)   │
                                   │  Code/Design QA │
                                   └─────────────────┘
                                          │
                                          ▼
                                   ┌─────────────────┐
                                   │ ps-investigator │◄──── (triggered by failures)
                                   │  (convergent)   │
                                   │  Incident RCA   │
                                   └─────────────────┘

    LEGEND:
    ────► = data flow / delegation
    ◄──── = can receive from
```

### 1.7 State Management Schema

Each agent outputs a standardized state object that downstream agents can consume:

```yaml
# Common State Schema Pattern
{agent}_output:
  ps_id: "{ps_id}"                    # Problem-solving ID
  entry_id: "{entry_id}"              # Entry/event ID
  artifact_path: "{path_to_file}.md"  # Persisted artifact location
  summary: "{key_finding}"            # Human-readable summary
  confidence: "high|medium|low"       # Confidence level
  next_agent_hint: "{suggested_next}" # Pipeline hint
  # Agent-specific fields follow...
```

**Agent-Specific Extensions:**

| Agent | Additional State Fields |
|-------|------------------------|
| researcher | `sources_count`, `next_agent_hint: "ps-analyst"` |
| analyst | `analysis_type`, `root_cause`, `recommendation` |
| synthesizer | `patterns_generated[]`, `lessons_generated[]`, `themes[]` |
| validator | `validated_count`, `total_count`, `pass_rate`, `gaps[]` |
| reporter | `health_status`, `completion_rate`, `blocker_count` |
| architect | `adr_number`, `decision`, `status: "PROPOSED"` |
| reviewer | `overall_assessment`, `critical_count`, `findings[]` |
| investigator | `severity`, `root_cause`, `corrective_actions[]`, `lessons[]` |

---

## L2: Architectural Implications (Principal Architect)

### 2.1 Design Patterns Employed

#### PAT-001: Agent Definition Template Pattern

**Context:** Need for consistent, machine-parseable agent definitions across portfolio
**Problem:** Ad-hoc agent definitions lead to inconsistent behavior and difficult orchestration
**Solution:** Standardized YAML+Markdown template with required sections
**Consequences:**
- (+) Consistent behavior across all agents
- (+) Machine-parseable for tooling/validation
- (+) Clear contract for new agent creation
- (-) Template changes require updating all agents

**Sources:** All 8 agent definition files follow identical structure

#### PAT-002: Layered Output Level Pattern (L0/L1/L2)

**Context:** Agent outputs need to serve multiple audiences (executives, engineers, architects)
**Problem:** Single-level outputs either oversimplify or overcomplicate for different readers
**Solution:** Mandatory three-level output (L0: ELI5, L1: Technical, L2: Strategic)
**Consequences:**
- (+) Single artifact serves all stakeholders
- (+) Consistent reader experience across agents
- (+) Forces completeness of thought
- (-) Increases output size and generation time

**Sources:** All agents require L0/L1/L2 in output_levels section

#### PAT-003: Constitutional Compliance Pattern

**Context:** Agents need governance without hard-coding rules in each definition
**Problem:** Inconsistent rule enforcement across agents
**Solution:** External constitution reference with per-agent principle mapping and self-critique checklist
**Consequences:**
- (+) Single source of truth for governance (JERRY_CONSTITUTION.md)
- (+) Agents can have different enforcement levels per principle
- (+) Self-critique enables reflection before output
- (-) Constitution changes may not propagate to agent behavior without redefinition

**Sources:** `constitution.reference: "docs/governance/JERRY_CONSTITUTION.md"` in all agents

#### PAT-004: Persistence-First Output Pattern

**Context:** LLM conversations are ephemeral; context rot degrades long sessions
**Problem:** Valuable agent outputs lost when conversation ends
**Solution:** Mandatory file persistence (P-002) with structured output locations
**Consequences:**
- (+) Outputs survive session boundaries
- (+) Enables multi-session workflows
- (+) Creates audit trail
- (-) Requires file system access and cleanup

**Sources:** P-002 enforcement (Medium) + output.location in all agents

#### PAT-005: Single-Level Delegation Pattern

**Context:** Agents may need to spawn sub-agents for subtasks
**Problem:** Unbounded recursion can exhaust resources and create confusion
**Solution:** P-003 (Hard) - Maximum ONE level of agent nesting
**Consequences:**
- (+) Predictable execution depth
- (+) Clear accountability chain
- (+) Resource usage bounded
- (-) Complex tasks may need multiple invocations

**Sources:** P-003 in constitutional_compliance across all agents, Task tool only in ps-researcher

### 2.2 Composition and Orchestration Patterns

#### Upstream/Downstream Relationships

```
┌────────────────────────────────────────────────────────────────────────────┐
│                          AGENT COMPOSITION MATRIX                          │
├───────────────────┬─────────────────────────┬─────────────────────────────┤
│      Agent        │      Can Feed Into      │      Can Receive From       │
├───────────────────┼─────────────────────────┼─────────────────────────────┤
│ ps-researcher     │ analyst, architect,     │ (entry point)               │
│                   │ synthesizer             │                             │
├───────────────────┼─────────────────────────┼─────────────────────────────┤
│ ps-analyst        │ architect, validator,   │ researcher                  │
│                   │ synthesizer             │                             │
├───────────────────┼─────────────────────────┼─────────────────────────────┤
│ ps-synthesizer    │ architect, reporter     │ researcher, analyst         │
├───────────────────┼─────────────────────────┼─────────────────────────────┤
│ ps-architect      │ validator, reviewer     │ researcher, analyst,        │
│                   │                         │ synthesizer                 │
├───────────────────┼─────────────────────────┼─────────────────────────────┤
│ ps-validator      │ reporter, reviewer      │ architect, analyst          │
├───────────────────┼─────────────────────────┼─────────────────────────────┤
│ ps-reviewer       │ reporter, validator     │ architect, researcher       │
├───────────────────┼─────────────────────────┼─────────────────────────────┤
│ ps-reporter       │ (terminal)              │ validator, synthesizer,     │
│                   │                         │ investigator                │
├───────────────────┼─────────────────────────┼─────────────────────────────┤
│ ps-investigator   │ reporter, synthesizer   │ (triggered by failures)     │
└───────────────────┴─────────────────────────┴─────────────────────────────┘
```

#### Fan-Out Opportunities

1. **Research Fan-Out:** ps-researcher can spawn multiple parallel research tasks via Task tool (single-level only)
2. **Synthesis Fan-In:** ps-synthesizer designed to consume outputs from multiple upstream agents
3. **Validation Parallelism:** Multiple constraints can be validated independently by ps-validator

#### Orchestration Support

Agents support orchestration through:
1. **State Schema:** Standardized output key enables orchestrator to read agent results
2. **next_agent_hint:** Explicit suggestion for pipeline continuation
3. **Artifact Linking:** `link-artifact` CLI enables tracking across PS entries
4. **PS Context:** Common context block enables session continuity

### 2.3 Strategic Recommendations for Worktracker Skill Agents

Based on this analysis, the following recommendations apply to designing worktracker skill agents:

#### Recommendation 1: Adopt PAT-001 Template Pattern
Worktracker agents should follow the same YAML+Markdown structure with identical sections. This ensures:
- Consistent behavior with existing ps-* agents
- Reuse of validation and orchestration tooling
- Familiar developer experience

#### Recommendation 2: Implement L0/L1/L2 Output Levels
All worktracker agents should produce three-level output. For worktracker:
- L0: Task status summary for quick check
- L1: Detailed task metadata and history
- L2: Project-level implications and dependencies

#### Recommendation 3: Define Clear Tool Permissions
Based on worktracker needs:
- **Core tools** (Read, Write, Edit, Glob, Grep, Bash): All agents
- **Web tools**: Only if researching external task management patterns
- **Task tool**: Only orchestrator agent (preserve P-003)

#### Recommendation 4: Map to Existing Agent Pipeline
Worktracker agents should integrate with existing ps-* agents:
- wt-reporter can consume ps-reporter outputs
- wt-validator can align with ps-validator constraint checking
- wt-analyst can use ps-analyst for root cause on blocked tasks

#### Recommendation 5: Honor Constitutional Principles
Especially critical for worktracker:
- **P-002 (Persistence):** Work items MUST be persisted to filesystem
- **P-010 (Task Tracking Integrity):** WORKTRACKER.md must reflect actual state
- **P-022 (No Deception):** Task status must be accurate

### 2.4 Knowledge Items Generated

#### PAT-006: Cognitive Mode Alignment Pattern

**Context:** Agents perform different types of cognitive work (exploration vs. synthesis)
**Problem:** Mixing cognitive modes in single agent leads to unfocused outputs
**Solution:** Explicitly declare cognitive_mode (divergent/convergent) per agent
**Consequences:**
- (+) Clear expectation of agent behavior
- (+) Divergent agents explore, convergent agents conclude
- (+) Pipeline design aligns modes with workflow stage
- (-) May need mode-switching for complex tasks

**Quality:** HIGH (pattern found in all 8 agents)
**Sources:** identity.cognitive_mode in all agent definitions

#### LES-001: Terminal Agents Simplify Pipelines

**Context:** Designing agent pipelines
**What Happened:** ps-reporter has no downstream agents (terminal node)
**What We Learned:** Terminal agents prevent infinite delegation loops and provide clear completion points
**Prevention:** Always identify which agents are terminal in a pipeline

**Sources:** ps-reporter state_management shows `next_agent_hint: null`

#### LES-002: Evidence Chain Is Critical for Trust

**Context:** Agent outputs need to be trustworthy
**What Happened:** All 8 agents require evidence citation for claims
**What We Learned:** Without evidence chains, agent outputs are not verifiable and violate P-001/P-004
**Prevention:** Template every agent output section to require evidence references

**Sources:** guardrails.output_filtering, constitutional_compliance in all agents

#### ASM-001: Agent Definitions Are Self-Contained

**Assumption:** Each agent definition file contains everything needed to instantiate the agent
**Context:** Agents reference external templates but don't inline them
**Impact if Wrong:** Agents may fail if templates are missing or changed
**Confidence:** MEDIUM
**Validation Path:** Check that templates exist and match agent expectations

**Sources:** `output.template` references in all agents (e.g., `templates/research.md`)

---

## References

### Agent Definition Files Analyzed

1. `skills/problem-solving/agents/ps-researcher.md`
   - Version: 2.0.0
   - Key insight: Only agent with Task tool; primary entry point for information gathering

2. `skills/problem-solving/agents/ps-analyst.md`
   - Version: 2.0.0
   - Key insight: Specialized in 5 Whys, FMEA, trade-off matrices

3. `skills/problem-solving/agents/ps-synthesizer.md`
   - Version: 2.0.0
   - Key insight: Generates PAT/LES/ASM knowledge items from multiple sources

4. `skills/problem-solving/agents/ps-validator.md`
   - Version: 2.0.0
   - Key insight: Binary pass/fail with Requirements Traceability Matrix

5. `skills/problem-solving/agents/ps-reporter.md`
   - Version: 2.0.0
   - Key insight: Terminal node in pipeline; health indicators and metrics

6. `skills/problem-solving/agents/ps-architect.md`
   - Version: 2.0.0
   - Key insight: Nygard ADR format; status always PROPOSED until user approves

7. `skills/problem-solving/agents/ps-reviewer.md`
   - Version: 2.0.0
   - Key insight: Quality spectrum (not binary); severity levels CRITICAL-INFO

8. `skills/problem-solving/agents/ps-investigator.md`
   - Version: 2.0.0
   - Key insight: Incident-focused; corrective actions with owners and due dates

### Prior Art Citations from Agent Definitions

- Chroma Context Rot Research - https://research.trychroma.com/context-rot
- Anthropic Prompt Engineering - https://docs.claude.com/en/docs/build-with-claude/prompt-engineering/claude-4-best-practices
- Google ADK Multi-Agent Patterns - https://developers.googleblog.com/developers-guide-to-multi-agent-patterns-in-adk/
- Toyota 5 Whys (Ohno, 1988) - https://www.toyota-global.com/company/toyota_traditions/quality/mar_apr_2006.html
- NASA FMEA (Systems Engineering Handbook, 2007) - https://www.nasa.gov/seh
- Braun, V. & Clarke, V. (2006). Using thematic analysis in psychology - https://doi.org/10.1191/1478088706qp063oa
- Michael Nygard's ADR Format (2011) - https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions
- Google Engineering Practices: Code Review - https://google.github.io/eng-practices/review/
- OWASP Top 10 (2021) - https://owasp.org/Top10/
- IEEE 1012-2016 Software Verification and Validation - https://standards.ieee.org/

---

## PS Integration

**Artifact Location:** `projects/PROJ-001-plugin-cleanup/research/init-wt-skills-e-001-ps-agent-portfolio.md`

**Note:** The `link-artifact` CLI does not exist yet (TD-010). This step is intentionally skipped per research task constraints.

---

*Generated by ps-researcher agent v2.0.0*
*Constitutional Compliance: Jerry Constitution v1.0*
*Research completed: 2026-01-11*
