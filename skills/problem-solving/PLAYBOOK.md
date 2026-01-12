# Problem-Solving Playbook

> **Version:** 3.0.0
> **Skill:** problem-solving
> **Purpose:** Structured analysis, research, and decision-making through specialized agents
> **Updated:** 2026-01-12 - Triple-lens refactoring (SAO-INIT-007)

---

## Document Overview

```
+============================================================================+
|                       TRIPLE-LENS COGNITIVE FRAMEWORK                       |
+=============================================================================+
|                                                                             |
|    L0 (ELI5)          L1 (Engineer)         L2 (Architect)                 |
|    ----------         -------------         --------------                 |
|    WHAT & WHY    ->   HOW (commands)   ->   CONSTRAINTS                    |
|    Metaphors          Invocations           Anti-patterns                  |
|    Intent             File paths            Boundaries                     |
|    Analogies          Input/Output          Invariants                     |
|                                                                             |
|    "Explains to       "Executable           "Prevents                      |
|     newcomers"         instructions"          mistakes"                    |
|                                                                             |
+=============================================================================+
```

**Target Audience:**
- **L0**: Anyone (stakeholders, newcomers, non-technical)
- **L1**: Engineers invoking problem-solving agents
- **L2**: Architects designing analysis workflows

---

# L0: The Big Picture (ELI5)

> *This section explains WHAT problem-solving does and WHY it matters using metaphors.*

## What Is Problem-Solving?

### The Detective Agency Metaphor

```
+===================================================================+
|                     THE DETECTIVE AGENCY                           |
+===================================================================+
|                                                                   |
|   Think of problem-solving like hiring a detective agency:        |
|                                                                   |
|                    +----------------+                              |
|                    | CASE INTAKE    |                              |
|                    | "We have a     |                              |
|                    |  problem..."   |                              |
|                    +-------+--------+                              |
|                            |                                       |
|              +-------------+-------------+                         |
|              |             |             |                         |
|              v             v             v                         |
|      +------------+  +----------+  +------------+                 |
|      | RESEARCHER |  | ANALYST  |  | ARCHITECT  |                 |
|      | (gathers   |  | (why it  |  | (what to   |                 |
|      |  clues)    |  |  happened)|  |  do next)  |                 |
|      +------------+  +----------+  +------------+                 |
|              |             |             |                         |
|              v             v             v                         |
|         +------+      +------+      +------+                       |
|         |REPORT|      |REPORT|      | ADR  |                       |
|         +------+      +------+      +------+                       |
|                                                                   |
|   Different detectives specialize in different cases:             |
|   - Researcher: gathers evidence, explores options                |
|   - Analyst: finds root cause, understands "why"                  |
|   - Investigator: debugs failures, traces timelines               |
|   - Validator: checks if requirements are met                     |
|   - Architect: makes design decisions, writes ADRs                |
|   - Synthesizer: finds patterns across cases                      |
|   - Reviewer: assesses quality, gives feedback                    |
|   - Reporter: summarizes status, tracks progress                  |
|                                                                   |
+===================================================================+
```

**Plain English:**
Problem-solving is a skill with specialized agents that handle different types of thinking. Instead of one agent doing everything poorly, you get a specialist who excels at that specific task - research, analysis, decision-making, validation, etc.

### Why Does This Matter?

| Without Specialized Agents | With Problem-Solving Skill |
|---------------------------|---------------------------|
| Generic responses, shallow analysis | Deep domain-specific expertise |
| No structured output format | L0/L1/L2 output for all audiences |
| Outputs lost in chat history | Every output persisted to docs/ |
| Unclear "what type of help" | Right agent selected by keywords |
| One-size-fits-all thinking | Divergent (explore) vs convergent (decide) |

### When Do I Use This?

```
AGENT SELECTION GUIDE:
----------------------

WHAT DO YOU NEED?
       |
  +----+----+----+----+----+----+----+----+
  |    |    |    |    |    |    |    |    |
  v    v    v    v    v    v    v    v    v
Explore? Why?  What to Fix?  Check? Patterns? Quality? Status?
  |       |     do?    |      |       |         |       |
  v       v      |     v      v       v         v       v
  ps-     ps-    |    ps-    ps-     ps-       ps-     ps-
  researcher analyst | investigator validator synthesizer reviewer reporter
              v
           ps-architect
```

**Activation Keywords:**

| Keyword | Agent |
|---------|-------|
| "research", "explore", "options" | ps-researcher |
| "analyze", "why", "root cause" | ps-analyst |
| "decide", "ADR", "architecture" | ps-architect |
| "debug", "investigate", "incident" | ps-investigator |
| "validate", "check", "verify" | ps-validator |
| "synthesize", "patterns", "lessons" | ps-synthesizer |
| "review", "quality", "feedback" | ps-reviewer |
| "status", "report", "progress" | ps-reporter |

---

## The Cast of Characters (Agents)

> *Meet the specialists who do the work*

```
+=========================================================================+
|                         THE DETECTIVE ROSTER                             |
+=========================================================================+
|                                                                         |
|    +---------------+    +---------------+    +---------------+          |
|    | ps-researcher |    | ps-analyst    |    | ps-architect  |          |
|    | ------------- |    | ------------- |    | ------------- |          |
|    | The Explorer  |    | The Detective |    | The Planner   |          |
|    | Gathers clues |    | Finds "why"   |    | Decides "what"|          |
|    +---------------+    +---------------+    +---------------+          |
|                                                                         |
|    +---------------+    +---------------+    +---------------+          |
|    | ps-validator  |    | ps-synthesizer|    | ps-reviewer   |          |
|    | ------------- |    | ------------- |    | ------------- |          |
|    | The Auditor   |    | The Connector |    | The Critic    |          |
|    | Checks boxes  |    | Finds patterns|    | Gives feedback|          |
|    +---------------+    +---------------+    +---------------+          |
|                                                                         |
|    +------------------+    +---------------+                            |
|    | ps-investigator  |    | ps-reporter   |                            |
|    | ---------------- |    | ------------- |                            |
|    | The Forensic CSI |    | The Narrator  |                            |
|    | Traces incidents |    | Tells status  |                            |
|    +------------------+    +---------------+                            |
|                                                                         |
+=========================================================================+
```

| Agent | Like a... | Does What | Cognitive Mode |
|-------|-----------|-----------|----------------|
| `ps-researcher` | Library detective | Explores options, gathers information | Divergent |
| `ps-analyst` | Forensic detective | Finds root cause, understands "why" | Convergent |
| `ps-architect` | City planner | Makes design decisions, writes ADRs | Convergent |
| `ps-validator` | Building inspector | Checks if requirements are met | Convergent |
| `ps-synthesizer` | Pattern analyst | Finds connections across documents | Convergent |
| `ps-reviewer` | Editor/critic | Assesses quality, gives feedback | Convergent |
| `ps-investigator` | Crime scene investigator | Debugs failures, traces timelines | Convergent |
| `ps-reporter` | News anchor | Summarizes status, tracks progress | Convergent |

---

## The L0/L1/L2 Output Format

Every agent produces output at three levels:

```
+===================================================================+
|                    THREE-LEVEL OUTPUT FORMAT                       |
+===================================================================+
|                                                                   |
|   +-----------------------------------------------------------+   |
|   | L0 (ELI5)                                                 |   |
|   | "Explain it like I'm 5"                                   |   |
|   | Audience: Non-technical stakeholders, executives          |   |
|   | Content: Plain language summary, key takeaways            |   |
|   +-----------------------------------------------------------+   |
|                              |                                    |
|                              v                                    |
|   +-----------------------------------------------------------+   |
|   | L1 (Engineer)                                             |   |
|   | "Give me the details"                                     |   |
|   | Audience: Software engineers                              |   |
|   | Content: Technical details, code examples, commands       |   |
|   +-----------------------------------------------------------+   |
|                              |                                    |
|                              v                                    |
|   +-----------------------------------------------------------+   |
|   | L2 (Architect)                                            |   |
|   | "What are the implications?"                              |   |
|   | Audience: Principal architects, tech leads                |   |
|   | Content: Strategic implications, trade-offs, risks        |   |
|   +-----------------------------------------------------------+   |
|                                                                   |
+===================================================================+
```

This means you get the right level of detail for your audience with every output.

---

# L1: How To Use It (Engineer)

> *This section provides executable instructions: commands, invocations, file paths.*

## Quick Start

### The 30-Second Version

1. **Describe your problem** - Just say what you need
2. **The right agent activates** - Based on keywords in your request
3. **Output is persisted** - A markdown file is created in `docs/`
4. **You can chain agents** - Sequence multiple agents for complex problems

### Minimal Example

```
User: "Research the best approach for implementing event sourcing in Python"

Claude: [Activates ps-researcher agent]
        [Researches topic with citations]
        [Creates docs/research/work-XXX-event-sourcing.md]
        [Returns L0/L1/L2 summary]
```

---

## Invocation Methods

### Method 1: Natural Language (Recommended)

Just describe what you need. The orchestrator selects the right agent.

```
"Research React vs Vue for our frontend"
-> Activates ps-researcher

"Why are our tests so slow?"
-> Activates ps-analyst (root cause)

"Create an ADR for choosing PostgreSQL"
-> Activates ps-architect

"Check if we meet all the security requirements"
-> Activates ps-validator

"Find patterns across the 3 research documents"
-> Activates ps-synthesizer

"Review the new authentication module"
-> Activates ps-reviewer

"Figure out why the deploy failed yesterday"
-> Activates ps-investigator

"What's the status of Phase 3?"
-> Activates ps-reporter
```

### Method 2: Explicit Agent Request

Name the agent you want:

```
"Use ps-researcher to explore caching options"
"Have ps-analyst do a 5 Whys analysis"
"I need ps-architect for the database decision"
```

### Method 3: Chained Request

Request a sequence:

```
"First research event sourcing options, then create an ADR for our choice"
```

This will:
1. Run ps-researcher -> create research document
2. Run ps-architect -> create ADR referencing the research

---

## Agent Reference

| Agent | When to Use | Keywords | Output Location | Output Format |
|-------|-------------|----------|-----------------|---------------|
| `ps-researcher` | Exploring options | research, explore, compare | `docs/research/` | Research report |
| `ps-analyst` | Root cause analysis | analyze, why, root cause, 5 whys | `docs/analysis/` | Analysis report |
| `ps-architect` | Design decisions | decide, ADR, architecture, design | `docs/decisions/` | ADR |
| `ps-validator` | Requirements check | validate, check, verify, compliance | `docs/analysis/` | Validation report |
| `ps-synthesizer` | Pattern extraction | synthesize, patterns, lessons | `docs/synthesis/` | Pattern catalog |
| `ps-reviewer` | Quality assessment | review, quality, feedback, audit | `docs/reviews/` | Review findings |
| `ps-investigator` | Debugging failures | investigate, debug, incident, failure | `docs/investigations/` | Investigation report |
| `ps-reporter` | Status updates | status, report, progress, dashboard | `docs/reports/` | Status report |

---

## Orchestration Patterns

> See [ORCHESTRATION_PATTERNS.md](../shared/ORCHESTRATION_PATTERNS.md) for complete pattern catalog.

### Pattern 1: Single Agent

For focused tasks, one agent is enough.

```
TOPOLOGY:
---------

User: "Research graph databases for our use case"

  +------------------+
  |  ps-researcher   | --> docs/research/graph-databases.md
  +------------------+
```

### Pattern 2: Sequential Chain

For complex problems, agents work in sequence.

```
TOPOLOGY:
---------

User: "Investigate the API timeout, propose a fix, validate the solution"

  +------------------+    +---------------+    +---------------+
  | ps-investigator  |--->|  ps-architect |--->|  ps-validator |
  +------------------+    +---------------+    +---------------+
         |                       |                     |
         v                       v                     v
  docs/investigations/    docs/decisions/      docs/analysis/
  api-timeout.md          adr-fix.md           validation.md
```

### Pattern 3: Fan-Out (Parallel Research)

For broad exploration, multiple researchers in parallel.

```
TOPOLOGY:
---------

User: "Research caching, message queues, and databases"

  +------------------+
  |  ps-researcher   | --> docs/research/caching-options.md
  +------------------+
  +------------------+
  |  ps-researcher   | --> docs/research/message-queue-options.md
  +------------------+
  +------------------+
  |  ps-researcher   | --> docs/research/database-options.md
  +------------------+
```

### Pattern 4: Fan-In (Synthesis)

After parallel work, synthesize findings.

```
TOPOLOGY:
---------

  docs/research/caching.md ------+
  docs/research/queues.md  ------+--> +------------------+
  docs/research/databases.md ----+    |  ps-synthesizer  |
                                      +------------------+
                                             |
                                             v
                                      docs/synthesis/
                                      patterns.md
```

### Pattern 5: Research -> Decision -> Validation

The full decision workflow.

```
TOPOLOGY:
---------

User: "We need to choose a caching solution"

  +------------------+    +---------------+    +---------------+
  |  ps-researcher   |--->|  ps-architect |--->|  ps-validator |
  |  (explore)       |    |  (decide)     |    |  (verify)     |
  +------------------+    +---------------+    +---------------+
         |                       |                     |
         v                       v                     v
  Research: Redis,       ADR: Choose Redis     Validation:
  Memcached, etc.        with rationale        Constraints met
```

---

## Practical Examples

### Example 1: Technology Selection

**Goal:** Choose between SQLite and PostgreSQL for the project.

```
Step 1: "Research SQLite vs PostgreSQL for embedded vs server use cases"

[ps-researcher activates]
Output: docs/research/work-024-e-001-sqlite-vs-postgres.md

Step 2: "Based on the research, create an ADR recommending the best choice"

[ps-architect activates]
Output: docs/decisions/work-024-e-002-adr-database-selection.md
```

### Example 2: Root Cause Analysis

**Goal:** Understand why tests are flaky.

```
"Analyze why our CI tests are flaky - do a 5 Whys"

[ps-analyst activates]
Output: docs/analysis/work-024-e-003-root-cause.md

Content includes:
- 5 Whys table with evidence
- Root cause: race conditions in test fixtures
- Recommendations with action items
```

### Example 3: Incident Investigation

**Goal:** Investigate production outage.

```
"Investigate the API outage on January 5th at 2:30 PM"

[ps-investigator activates]
Output: docs/investigations/work-024-e-004-investigation.md

Content includes:
- Timeline of events
- 5 Whys analysis
- Ishikawa diagram (6M categories)
- Corrective actions with owners
- FMEA for similar risks
```

### Example 4: Code Review

**Goal:** Review new authentication module.

```
"Review the authentication module for security issues"

[ps-reviewer activates]
Output: docs/reviews/work-024-e-005-security.md

Content includes:
- OWASP Top 10 assessment
- Findings by severity (Critical -> Info)
- Code snippets with recommendations
- Overall assessment: PASS/NEEDS_WORK/FAIL
```

### Example 5: Cross-Document Synthesis

**Goal:** Find patterns across research documents.

```
"Synthesize the 4 research documents from last week into patterns"

[ps-synthesizer activates]
Output: docs/synthesis/work-024-e-006-synthesis.md

Content includes:
- Cross-reference matrix
- Pattern catalog (PAT-XXX)
- Lessons learned (LES-XXX)
- Assumptions identified (ASM-XXX)
```

---

## Output Locations

All artifacts are persisted to your project directory:

```
projects/{PROJECT}/
|-- docs/
|   |-- research/           # ps-researcher output
|   |   |-- work-XXX-topic.md
|   |-- analysis/           # ps-analyst, ps-validator output
|   |   |-- work-XXX-root-cause.md
|   |   |-- work-XXX-validation.md
|   |-- decisions/          # ps-architect output
|   |   |-- work-XXX-adr-topic.md
|   |-- synthesis/          # ps-synthesizer output
|   |   |-- work-XXX-synthesis.md
|   |-- reviews/            # ps-reviewer output
|   |   |-- work-XXX-review.md
|   |-- investigations/     # ps-investigator output
|   |   |-- work-XXX-investigation.md
|   |-- reports/            # ps-reporter output
|   |   |-- work-XXX-status.md
```

---

## Tips and Best Practices

### 1. Be Specific

```
Bad:  "Analyze this"
Good: "Analyze why the database queries are slow using 5 Whys"

Bad:  "Research stuff"
Good: "Research event sourcing patterns in Python, focusing on libraries
       with Postgres support"
```

### 2. Provide Context

```
Bad:  "Create an ADR"
Good: "Create an ADR for choosing Redis as our caching layer.
       We need sub-millisecond latency and support for 100k connections."
```

### 3. Chain When Needed

For complex problems, break into steps:

```
"First, research the options. Then analyze trade-offs.
 Finally, create an ADR with our recommendation."
```

### 4. Reference Previous Work

```
"Based on the research in docs/research/caching-options.md,
 create an ADR for our caching decision."
```

### 5. Ask for Specific Output Level

```
"Generate a phase status report focusing on blockers and risks"
"Do a security review focusing on OWASP Top 10 issues"
"Just give me the L0 summary"
```

---

## Troubleshooting

### "The wrong agent was selected"

Be more explicit:

```
"Use ps-analyst (not ps-researcher) to analyze the trade-offs"
```

### "Output wasn't saved"

This shouldn't happen (P-002 requires persistence), but if it does:

```
"Save the analysis to docs/analysis/my-analysis.md"
```

### "I need more detail at L1 level"

Ask for expansion:

```
"Expand the L1 technical section with more code examples"
```

### "The output is too long"

Ask for summary:

```
"Summarize just the L0 executive summary"
```

### "I want to continue from a previous analysis"

Reference the file:

```
"Continue the investigation from docs/investigations/api-timeout.md
 with the new log data I found"
```

---

# L2: Architecture & Constraints

> *This section documents what NOT to do, boundaries, invariants, and design rationale.*

## Anti-Pattern Catalog

### AP-001: Agent Soup

```
+===================================================================+
| ANTI-PATTERN: Agent Soup                                          |
+===================================================================+
|                                                                   |
| SYMPTOM:    Multiple agents invoked without clear purpose.        |
|             Outputs contradict each other. Confusion about        |
|             which agent to believe.                               |
|                                                                   |
| CAUSE:      Unclear problem statement triggering multiple agents. |
|             "Analyze and research and review this code"           |
|                                                                   |
| IMPACT:     - Redundant work across agents                        |
|             - Contradictory findings                              |
|             - User confusion about next steps                     |
|             - Wasted compute                                      |
|                                                                   |
| FIX:        One clear task per invocation.                        |
|             Chain agents explicitly if needed.                    |
|             "First research, then analyze, then review"           |
|                                                                   |
+===================================================================+
```

**Example (Bad):**
```
"Research and analyze and decide on our caching approach"
# Triggers multiple agents simultaneously with overlapping scope
```

**Example (Good):**
```
"Research caching options"          # Step 1: ps-researcher
"Analyze trade-offs from research"  # Step 2: ps-analyst
"Create ADR based on analysis"      # Step 3: ps-architect
```

---

### AP-002: Orphan Outputs

```
+===================================================================+
| ANTI-PATTERN: Orphan Outputs                                      |
+===================================================================+
|                                                                   |
| SYMPTOM:    Agent outputs not referenced by subsequent agents.    |
|             Each agent starts fresh. Findings not connected.      |
|                                                                   |
| CAUSE:      Not referencing previous outputs in new invocations.  |
|             "Create an ADR" (without mentioning prior research)   |
|                                                                   |
| IMPACT:     - Lost context from earlier work                      |
|             - Decisions not grounded in research                  |
|             - No traceability between artifacts                   |
|                                                                   |
| FIX:        Always reference prior outputs:                       |
|             "Based on docs/research/caching.md, create ADR"       |
|                                                                   |
+===================================================================+
```

**Example (Bad):**
```
Step 1: "Research caching options"
Step 2: "Create an ADR for caching"  # No reference to step 1!
```

**Example (Good):**
```
Step 1: "Research caching options"
Step 2: "Based on docs/research/caching-options.md, create an ADR"
```

---

### AP-003: Analysis Paralysis

```
+===================================================================+
| ANTI-PATTERN: Analysis Paralysis                                  |
+===================================================================+
|                                                                   |
| SYMPTOM:    Endless research without decisions. ps-researcher     |
|             called repeatedly. No ps-architect invocation.        |
|                                                                   |
| CAUSE:      Fear of making wrong decision. "Let's research more." |
|             Not recognizing when enough information exists.       |
|                                                                   |
| IMPACT:     - Decision delay                                      |
|             - Wasted research on diminishing returns              |
|             - Project stalls                                      |
|                                                                   |
| FIX:        Set explicit decision point.                          |
|             "Research until we have 3 viable options, then ADR"   |
|             Use ps-architect to force convergence.                |
|                                                                   |
+===================================================================+
```

**Example (Bad):**
```
"Research caching"
"Research more caching alternatives"
"What about this other caching option?"
"Are there any other options we haven't considered?"
# Never reaches a decision
```

**Example (Good):**
```
"Research caching options - give me top 3 viable choices"
"Based on the research, create ADR selecting one option"
# Forces convergence
```

---

### AP-004: Context Amnesia

```
+===================================================================+
| ANTI-PATTERN: Context Amnesia                                     |
+===================================================================+
|                                                                   |
| SYMPTOM:    Agent asked to continue work but doesn't remember     |
|             prior context. Repeats work already done.             |
|                                                                   |
| CAUSE:      Context compaction occurred. State not persisted.     |
|             Relying on conversation memory instead of files.      |
|                                                                   |
| IMPACT:     - Duplicate work                                      |
|             - Inconsistent findings                               |
|             - User frustration                                    |
|                                                                   |
| FIX:        Always persist outputs to files (P-002).              |
|             Reference files explicitly when continuing.           |
|             "Continue from docs/research/caching.md"              |
|                                                                   |
+===================================================================+
```

---

## Constraints & Boundaries

### Hard Constraints (Cannot Violate)

| ID | Constraint | Rationale |
|----|------------|-----------|
| HC-001 | All agent outputs persisted to files | P-002 File Persistence |
| HC-002 | Outputs include L0/L1/L2 sections | Serves all audience levels |
| HC-003 | ADRs require rationale section | Decisions must be justified |
| HC-004 | Investigations include timeline | Chronology is essential |
| HC-005 | No recursive agent spawning | P-003 Jerry Constitution |

### Soft Constraints (Should Not Violate)

| ID | Constraint | When to Relax |
|----|------------|---------------|
| SC-001 | One agent per invocation | When explicitly chaining |
| SC-002 | Research before decisions | When prior knowledge is sufficient |
| SC-003 | Full L0/L1/L2 output | When user requests specific level |

---

## Invariants

> *Conditions that must ALWAYS be true*

```
INVARIANT CHECKLIST:
--------------------

[X] INV-001: Every agent invocation produces a file artifact
           Violation: Work lost on context compaction

[X] INV-002: ps-architect ADRs contain "Decision" and "Rationale"
           Violation: Decision without justification

[X] INV-003: ps-analyst outputs include root cause identification
           Violation: Analysis without conclusion

[X] INV-004: ps-investigator timelines are chronological
           Violation: Confusing incident reconstruction

[X] INV-005: ps-validator outputs have pass/fail status
           Violation: Validation without conclusion
```

---

## Agent Selection Matrix

> *Detailed guidance for selecting the right agent*

```
AGENT SELECTION MATRIX:
-----------------------

TASK TYPE               | AGENT          | COGNITIVE MODE | OUTPUT
------------------------|----------------|----------------|-------------
Explore options         | ps-researcher  | Divergent      | Research report
Find root cause         | ps-analyst     | Convergent     | Analysis report
Make design decision    | ps-architect   | Convergent     | ADR
Check requirements      | ps-validator   | Convergent     | Validation report
Debug failure           | ps-investigator| Convergent     | Investigation
Find patterns           | ps-synthesizer | Convergent     | Pattern catalog
Assess quality          | ps-reviewer    | Convergent     | Review findings
Track progress          | ps-reporter    | Convergent     | Status report
```

### Cognitive Mode Guidance

```
COGNITIVE MODE SELECTION:
-------------------------

DIVERGENT MODE (Expand)           CONVERGENT MODE (Focus)
-----------------------           ----------------------
ps-researcher                     ps-analyst
                                  ps-architect
"What are the options?"           ps-validator
"What else is out there?"         ps-investigator
"Explore alternatives"            ps-synthesizer
                                  ps-reviewer
                                  ps-reporter

                                  "What's the answer?"
                                  "Make a decision"
                                  "Give me the conclusion"
```

---

## State Management

### Session Context Schema

When chaining agents, pass context:

```yaml
session_context:
  version: "1.0.0"
  session_id: "uuid"
  source_agent: "ps-researcher"
  target_agent: "ps-architect"
  state_output_key: "research_output"
  cognitive_mode: "convergent"
  payload:
    findings: [ ... ]
    prior_artifacts:
      - "docs/research/caching-options.md"
```

### Cross-Skill Handoffs

Problem-solving agents can hand off to NASA SE agents:

| Source Agent | Target Agent | Handoff Context |
|--------------|--------------|-----------------|
| `ps-architect` | `nse-architecture` | Design for trade study |
| `ps-analyst` | `nse-risk` | Root cause for risk register |
| `ps-researcher` | `nse-requirements` | Research for shall statements |

---

## Design Rationale

### Why Specialized Agents?

**Context:** Generic LLM responses lack depth for complex problems.

**Decision:** Create specialized agents with focused prompts.

**Consequences:**
- (+) Deeper domain expertise per task type
- (+) Consistent output formats (L0/L1/L2)
- (+) Clear invocation keywords
- (-) User must select correct agent
- (-) Potential overlap between agents

### Why L0/L1/L2 Output Format?

**Context:** Different audiences need different detail levels.

**Decision:** Every output has three levels.

**Consequences:**
- (+) Executives get summary (L0)
- (+) Engineers get details (L1)
- (+) Architects get implications (L2)
- (-) Outputs are longer

### Why Persist Everything?

**Context:** Context compaction loses conversation state.

**Decision:** All outputs must be persisted to files (P-002).

**Consequences:**
- (+) Survives context compaction
- (+) Creates knowledge repository
- (+) Enables artifact references
- (-) More files to manage

---

## References

- [ORCHESTRATION_PATTERNS.md](../shared/ORCHESTRATION_PATTERNS.md) - 8 canonical patterns
- [AGENT_TEMPLATE_CORE.md](../shared/AGENT_TEMPLATE_CORE.md) - Agent definition format
- [Jerry Constitution](../../docs/governance/JERRY_CONSTITUTION.md) - P-002 File Persistence

---

## Quick Reference Card

| Task | Prompt |
|------|--------|
| Research options | `"Research {topic}"` |
| Root cause | `"Analyze why {problem}"` |
| Make decision | `"Create ADR for {decision}"` |
| Debug failure | `"Investigate {incident}"` |
| Check requirements | `"Validate {requirements} against {criteria}"` |
| Find patterns | `"Synthesize {documents} into patterns"` |
| Review quality | `"Review {artifact} for {aspect}"` |
| Get status | `"Generate status report for {scope}"` |

---

*Playbook Version: 3.0.0*
*Skill: problem-solving*
*Last Updated: 2026-01-12 - Triple-lens refactoring (SAO-INIT-007)*
*Template: PLAYBOOK_TEMPLATE.md v1.0.0*
