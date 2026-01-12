# Problem-Solving Playbook

> **Version:** 3.2.0
> **Skill:** problem-solving
> **Purpose:** Structured analysis, research, and decision-making through specialized agents
> **Updated:** 2026-01-12 - Added 15 L0/L1/L2 real-world examples (WI-SAO-043)

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
| "critique", "improve", "iterate", "polish" | ps-critic |
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
|    +------------------+    +---------------+    +---------------+       |
|    | ps-investigator  |    | ps-reporter   |    | ps-critic     |       |
|    | ---------------- |    | ------------- |    | ------------- |       |
|    | The Forensic CSI |    | The Narrator  |    | Writing Coach |       |
|    | Traces incidents |    | Tells status  |    | Improves work |       |
|    +------------------+    +---------------+    +---------------+       |
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
| `ps-critic` | Writing coach | Evaluates outputs for iterative improvement | Convergent |
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
| `ps-critic` | Iterative refinement | critique, improve, iterate, polish | `projects/${JERRY_PROJECT}/critiques/` | Critique report |
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

### Pattern 6: Generator-Critic Loop (Iterative Refinement)

For quality-sensitive outputs that benefit from iteration.

```
TOPOLOGY:
---------

User: "Create an ADR and polish it until it's excellent"

  +------------------+         +---------------+
  |  ps-architect    |-------->|  ps-critic    |
  |  (generator)     |         |  (evaluator)  |
  +------------------+         +---------------+
         ^                            |
         |     score < 0.85          |
         |     + feedback            |
         +---------------------------+
                    |
                    v (score >= 0.85)
              [ACCEPT OUTPUT]

CIRCUIT BREAKER: max 3 iterations, threshold 0.85
```

**When to Use Generator-Critic:**

| Scenario | Use Generator-Critic? |
|----------|----------------------|
| ADR needs polish | YES - Quality improves with iteration |
| Research synthesis | YES - Completeness matters |
| API schema check | NO - Use ps-validator (binary check) |
| Code review | NO - Use ps-reviewer (find defects) |
| Time-critical task | NO - Iteration adds latency |

**Key Distinctions:**

| Agent | Purpose | Output Type | Iteration? |
|-------|---------|-------------|------------|
| ps-critic | Improve quality | Score (0.0-1.0) + recommendations | YES (loop) |
| ps-validator | Verify constraints | Pass/Fail | NO (one-shot) |
| ps-reviewer | Find defects | Severity ratings | NO (one-shot) |

**Circuit Breaker Logic:**

```
IF score >= 0.85:
    → ACCEPT (threshold met)
ELIF iteration >= 3:
    → ACCEPT_WITH_CAVEATS (max iterations)
ELIF no_improvement for 2 iterations:
    → ACCEPT_WITH_CAVEATS (diminishing returns)
ELSE:
    → REVISE (send feedback to generator)
```

**Example Invocation:**

```
Step 1: "Create an ADR for our authentication approach"
[ps-architect produces ADR draft]

Step 2: "Critique this ADR - score against completeness, clarity, alignment"
[ps-critic evaluates: score=0.72, feedback: "missing security trade-offs"]

Step 3: "Revise the ADR based on the critique"
[ps-architect produces ADR v2]

Step 4: "Critique again"
[ps-critic evaluates: score=0.88 → ACCEPT]
```

**P-003 Compliance Note:**
The MAIN CONTEXT (Claude session) orchestrates the loop. ps-critic only evaluates - it does NOT invoke the next iteration. Agents cannot orchestrate other agents.

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

## Real-World Examples by Domain

> *Concrete scenarios showing how to use each agent in practice. Each example shows L0 (what/why), L1 (how), and L2 (constraints).*

### Software Engineering Examples

#### SE-001: Production Incident Root Cause Analysis

**Domain:** Software Engineering
**Scenario:** Production database response times spiked to 30 seconds causing checkout failures. Need to identify root cause.

##### L0 (ELI5) - What & Why
> Imagine a highway suddenly getting jammed. ps-analyst is like a traffic engineer who rewinds time to find where the jam started. Was it an accident? Road construction? Rush hour? We need to find the bottleneck before it happens again.

##### L1 (Engineer) - How

```
Invocation: "Analyze why database queries are timing out using 5 Whys"

Agent: ps-analyst
Output: docs/analysis/work-XXX-db-timeout-rca.md
```

**Agent Sequence:** `ps-investigator` (timeline) → `ps-analyst` (root cause) → `ps-architect` (fix decision)

##### L2 (Architect) - Constraints

| Constraint | Impact | Mitigation |
|------------|--------|------------|
| Time pressure from outage | May skip evidence gathering | Set minimum evidence threshold |
| Multiple potential causes | Analysis paralysis | Use 5 Whys to force convergence |

**Anti-patterns to avoid:**
- AP-003: Endless investigation without conclusion
- AP-004: Starting fresh without referencing incident timeline

---

#### SE-002: Architecture Decision Record Creation

**Domain:** Software Engineering
**Scenario:** Team needs to choose between PostgreSQL and MongoDB for a new microservice. Both have advocates.

##### L0 (ELI5) - What & Why
> When the team disagrees on which tool to use, ps-architect is like a judge who weighs evidence and writes a verdict. The ADR explains WHAT we decided, WHY we chose it, and WHAT we gave up.

##### L1 (Engineer) - How

```
Step 1: "Research PostgreSQL vs MongoDB for our event-driven microservice"
Agent: ps-researcher → docs/research/db-selection-research.md

Step 2: "Based on docs/research/db-selection-research.md, create ADR
        recommending a database choice"
Agent: ps-architect → docs/decisions/adr-003-database-selection.md

Step 3: "Critique the ADR until it scores 0.85 or higher"
Agent: ps-critic → [iterate until acceptance threshold]
```

##### L2 (Architect) - Constraints

| Constraint | Impact | Mitigation |
|------------|--------|------------|
| Stakeholder disagreement | ADR may be contested | Include dissenting opinions in rationale |
| Reversibility concerns | Team hesitant to commit | Document reversal cost explicitly |

**Anti-patterns to avoid:**
- AP-002: Creating ADR without prior research reference
- AP-003: Researching 10 databases when 3 are sufficient

---

#### SE-003: Code Review with Structured Feedback

**Domain:** Software Engineering
**Scenario:** PR has 2000 lines of changes across authentication module. Need thorough security-focused review.

##### L0 (ELI5) - What & Why
> ps-reviewer is like a book editor who reads your manuscript looking for plot holes. For code, it looks for security bugs, performance issues, and violations of team standards.

##### L1 (Engineer) - How

```
Invocation: "Review the authentication module PR against OWASP Top 10
           and our security guidelines"

Agent: ps-reviewer
Output: docs/reviews/work-XXX-auth-security-review.md

Content includes:
- OWASP assessment checklist
- Findings by severity (CRITICAL → INFO)
- Code snippets with recommendations
- Overall assessment: PASS/NEEDS_WORK/FAIL
```

##### L2 (Architect) - Constraints

| Constraint | Impact | Mitigation |
|------------|--------|------------|
| Large PR size | May miss subtle issues | Request author to split PR |
| Security scope creep | Review becomes audit | Define explicit security boundaries |

**Anti-patterns to avoid:**
- AP-001: Mixing security review with architecture review
- AP-005: Critiquing every finding (reviewer outputs don't iterate)

---

#### SE-004: Technical Debt Assessment

**Domain:** Software Engineering
**Scenario:** Legacy payment service has grown organically for 5 years. Need to assess technical debt before modernization.

##### L0 (ELI5) - What & Why
> Technical debt is like deferred home maintenance - skip painting this year, and next year you need the whole exterior redone. ps-researcher helps survey all the "unpainted walls" so we know how much work we're facing.

##### L1 (Engineer) - How

```
Step 1: "Research technical debt in payment-service/ focusing on
        code complexity, test coverage, and dependency health"
Agent: ps-researcher → docs/research/payment-svc-tech-debt.md

Step 2: "Analyze the research to prioritize debt by risk and effort"
Agent: ps-analyst → docs/analysis/payment-svc-debt-priority.md

Step 3: "Synthesize findings into actionable remediation roadmap"
Agent: ps-synthesizer → docs/synthesis/payment-svc-roadmap.md
```

##### L2 (Architect) - Constraints

| Constraint | Impact | Mitigation |
|------------|--------|------------|
| Business pressure to ship | Debt postponed indefinitely | Quantify risk in business terms |
| No single owner | Diffused accountability | Assign debt items to specific teams |

**Anti-patterns to avoid:**
- AP-002: Creating roadmap without debt inventory
- AP-003: Cataloging every minor code smell

---

#### SE-005: API Design Review

**Domain:** Software Engineering
**Scenario:** New REST API for inventory service needs design review before implementation.

##### L0 (ELI5) - What & Why
> ps-reviewer for APIs is like a building inspector checking blueprints before construction. It's easier to fix a bad design on paper than after the walls are up.

##### L1 (Engineer) - How

```
Invocation: "Review the inventory API design against REST best practices,
           naming conventions, and our API style guide"

Agent: ps-reviewer
Output: docs/reviews/work-XXX-inventory-api-design.md

Content includes:
- REST maturity assessment (Richardson Level)
- Naming convention compliance
- Error handling consistency
- Pagination and filtering patterns
- Security considerations (auth, rate limiting)
```

##### L2 (Architect) - Constraints

| Constraint | Impact | Mitigation |
|------------|--------|------------|
| Breaking changes expensive | Hesitancy to critique | Frame as "better now than later" |
| Multiple consumers | Conflicting requirements | Identify primary consumer first |

**Anti-patterns to avoid:**
- AP-001: Reviewing design AND implementation in same pass
- AP-004: Not referencing prior API designs for consistency

---

### Product Management Examples

#### PM-001: Feature Prioritization Analysis

**Domain:** Product Management
**Scenario:** Three features requested (SSO, mobile app, API v2), budget for one. Need structured prioritization.

##### L0 (ELI5) - What & Why
> When you can only afford one thing, ps-analyst helps compare apples to oranges. It's like a shopping comparison site that scores options on what matters most to you - price, quality, time.

##### L1 (Engineer) - How

```
Step 1: "Research effort estimates and market impact for SSO,
        mobile app, and API v2"
Agent: ps-researcher → docs/research/feature-comparison.md

Step 2: "Analyze trade-offs using weighted scoring: customer impact (40%),
        revenue potential (30%), implementation risk (30%)"
Agent: ps-analyst → docs/analysis/feature-prioritization.md
```

**Output Structure:**
| Feature | Customer Impact | Revenue | Risk | Weighted Score |
|---------|----------------|---------|------|----------------|
| SSO | 8/10 | 6/10 | 3/10 | 6.3 |
| Mobile | 9/10 | 8/10 | 7/10 | 7.9 |
| API v2 | 5/10 | 9/10 | 5/10 | 6.4 |

##### L2 (Architect) - Constraints

| Constraint | Impact | Mitigation |
|------------|--------|------------|
| Stakeholder bias | Weights manipulated to favor pet projects | Document weight rationale |
| Estimation uncertainty | Scores feel arbitrary | Include confidence intervals |

**Anti-patterns to avoid:**
- AP-003: Researching 20 features when deciding between 3
- AP-001: Mixing prioritization with detailed planning

---

#### PM-002: Stakeholder Requirements Elicitation

**Domain:** Product Management
**Scenario:** Five stakeholders have different visions for the new dashboard. Need to synthesize requirements.

##### L0 (ELI5) - What & Why
> When 5 people describe their dream house, ps-synthesizer finds the common themes: "Everyone wants natural light, 3 want a home office, 2 need wheelchair access." It turns chaos into clarity.

##### L1 (Engineer) - How

```
Step 1: "Research stakeholder interview notes to extract
        explicit and implicit requirements"
Agent: ps-researcher → docs/research/dashboard-stakeholder-analysis.md

Step 2: "Synthesize requirements across stakeholders,
        identifying agreements, conflicts, and gaps"
Agent: ps-synthesizer → docs/synthesis/dashboard-requirements.md

Content includes:
- Requirements matrix by stakeholder
- Conflict resolution recommendations
- Priority tiers (Must/Should/Could)
- Assumptions requiring validation
```

##### L2 (Architect) - Constraints

| Constraint | Impact | Mitigation |
|------------|--------|------------|
| Political dynamics | Some voices louder than others | Weight by domain authority |
| Implicit requirements | Missed until late | Use probing questions template |

**Anti-patterns to avoid:**
- AP-004: Not referencing interview notes in synthesis
- AP-002: Requirements doc orphaned from stakeholder input

---

#### PM-003: Competitive Analysis Research

**Domain:** Product Management
**Scenario:** Competitor launched similar feature. Need rapid competitive intelligence.

##### L0 (ELI5) - What & Why
> ps-researcher for competitive analysis is like a scout who watches the opposing team's practice. You learn their plays so you can prepare counter-strategies.

##### L1 (Engineer) - How

```
Invocation: "Research competitor X's new feature focusing on:
           functionality, pricing, user reviews, market positioning"

Agent: ps-researcher
Output: docs/research/competitor-x-analysis.md

Content includes:
- Feature capability matrix (Us vs. Them)
- Pricing comparison
- User sentiment from reviews
- Market positioning analysis
- Strategic recommendations
```

##### L2 (Architect) - Constraints

| Constraint | Impact | Mitigation |
|------------|--------|------------|
| Information asymmetry | May miss internal details | Note confidence level per finding |
| Rapid market changes | Analysis stale quickly | Date-stamp all findings |

**Anti-patterns to avoid:**
- AP-003: Over-researching every competitor feature
- AP-001: Mixing research with strategic response

---

#### PM-004: Sprint Risk Assessment

**Domain:** Product Management
**Scenario:** Sprint has aggressive commitments. PM needs risk visibility for stakeholder communication.

##### L0 (ELI5) - What & Why
> ps-analyst for risks is like a weather forecaster for your project. It spots storm clouds (blockers, dependencies, unknown tech) so you can bring an umbrella.

##### L1 (Engineer) - How

```
Invocation: "Analyze sprint risks including: technical uncertainties,
           dependency risks, capacity concerns, external blockers"

Agent: ps-analyst
Output: docs/analysis/sprint-24-risk-assessment.md

Content includes:
- Risk registry with probability × impact scoring
- Risk mitigation strategies
- Escalation triggers
- Contingency plans
```

##### L2 (Architect) - Constraints

| Constraint | Impact | Mitigation |
|------------|--------|------------|
| Team optimism bias | Risks understated | Use calibrated estimation |
| Risk fatigue | Stakeholders ignore warnings | Focus on top 3 risks |

**Anti-patterns to avoid:**
- AP-003: Analyzing risks for 6 sprints ahead
- AP-001: Mixing risk analysis with mitigation planning

---

#### PM-005: Product Roadmap Validation

**Domain:** Product Management
**Scenario:** Q3 roadmap drafted, need validation against strategy, resources, and dependencies.

##### L0 (ELI5) - What & Why
> ps-validator for roadmaps is like a pre-flight checklist for pilots. Before takeoff, verify everything is in place: fuel, weather, route. Before committing to a roadmap, verify strategy alignment, resource availability, and no blocking dependencies.

##### L1 (Engineer) - How

```
Invocation: "Validate Q3 roadmap against: strategic objectives,
           team capacity, technical dependencies, customer commitments"

Agent: ps-validator
Output: docs/analysis/q3-roadmap-validation.md

Content includes:
- Strategic alignment assessment
- Resource utilization check
- Dependency analysis
- Customer commitment verification
- Overall: PASS / NEEDS_WORK / FAIL
```

##### L2 (Architect) - Constraints

| Constraint | Impact | Mitigation |
|------------|--------|------------|
| Moving goalposts | Strategy changes mid-quarter | Document strategy version |
| Hidden dependencies | Late discovery of blockers | Explicit dependency mapping |

**Anti-patterns to avoid:**
- AP-005: Critiquing the validation (validator output is binary)
- AP-002: Validating without referencing strategic docs

---

### User Experience Examples

#### UX-001: Usability Heuristic Evaluation

**Domain:** User Experience
**Scenario:** New checkout flow redesigned. Need UX review before user testing.

##### L0 (ELI5) - What & Why
> ps-reviewer for UX is like a restaurant critic who evaluates ambiance, service, and food. For interfaces, it evaluates clarity, consistency, and error prevention using established UX principles (Nielsen's heuristics).

##### L1 (Engineer) - How

```
Invocation: "Review checkout flow against Nielsen's 10 usability heuristics,
           focusing on error prevention and user control"

Agent: ps-reviewer
Output: docs/reviews/work-XXX-checkout-ux-review.md

Content includes:
- Heuristic evaluation matrix (10 heuristics × pass/fail)
- Severity ratings for issues (Cosmetic → Catastrophic)
- Annotated screenshots
- Recommendations with priority
```

##### L2 (Architect) - Constraints

| Constraint | Impact | Mitigation |
|------------|--------|------------|
| Evaluator bias | Findings reflect personal preference | Use multiple evaluators |
| Heuristic gaps | Not all issues are heuristic violations | Supplement with user testing |

**Anti-patterns to avoid:**
- AP-005: Iterating on review findings (reviews don't loop)
- AP-001: Mixing heuristic review with visual design review

---

#### UX-002: Design Critique with Feedback Loop

**Domain:** User Experience
**Scenario:** Dashboard mockup needs polish before development handoff. Iteration welcome.

##### L0 (ELI5) - What & Why
> ps-critic for design is like a writing coach who reads your draft and says "this is 70% there - here's how to reach 95%." Unlike a reviewer who finds bugs, the critic helps you improve quality through iteration.

##### L1 (Engineer) - How

```
Step 1: "Critique the dashboard design against clarity,
        information hierarchy, and visual consistency. Score 0-1."
Agent: ps-critic → Score: 0.68, Feedback: "Data hierarchy unclear,
                                           key metrics buried below fold"

Step 2: [Designer revises based on feedback]

Step 3: "Critique again"
Agent: ps-critic → Score: 0.87 → ACCEPT

Circuit breaker: max 3 iterations, threshold 0.85
```

##### L2 (Architect) - Constraints

| Constraint | Impact | Mitigation |
|------------|--------|------------|
| Subjective quality | Hard to define "excellent" | Agree on criteria upfront |
| Designer ego | Feedback feels personal | Frame as "design" critique not "designer" |

**Anti-patterns to avoid:**
- AP-006: Infinite critique loop (use circuit breaker)
- AP-005: Critiquing every mockup (reserve for key designs)

---

#### UX-003: Accessibility Compliance Review

**Domain:** User Experience
**Scenario:** Government contract requires WCAG 2.1 AA compliance. Need audit.

##### L0 (ELI5) - What & Why
> ps-validator for accessibility is like a building inspector checking wheelchair ramps and braille signs. It verifies your interface works for everyone, including users with visual, motor, or cognitive differences.

##### L1 (Engineer) - How

```
Invocation: "Validate checkout flow against WCAG 2.1 AA success criteria"

Agent: ps-validator
Output: docs/analysis/work-XXX-wcag-audit.md

Content includes:
- WCAG 2.1 AA checklist (pass/fail per criterion)
- Violation inventory by type
- Remediation guidance
- Tools used (axe, WAVE, manual testing)
- Overall: PASS / NEEDS_WORK / FAIL
```

##### L2 (Architect) - Constraints

| Constraint | Impact | Mitigation |
|------------|--------|------------|
| Automated tool limits | Some criteria need manual testing | Document test method per criterion |
| Interpretation variance | "Meaningful sequence" is subjective | Reference authoritative interpretations |

**Anti-patterns to avoid:**
- AP-005: Critiquing accessibility findings (validator is binary)
- AP-001: Mixing a11y audit with general UX review

---

#### UX-004: User Journey Mapping

**Domain:** User Experience
**Scenario:** Customer support tickets spike at onboarding. Need to map pain points.

##### L0 (ELI5) - What & Why
> ps-researcher for journeys is like following a customer through a store, noting where they pause, get confused, or ask for help. The journey map reveals friction points invisible from the inside.

##### L1 (Engineer) - How

```
Step 1: "Research user journey for onboarding flow based on:
        support tickets, session recordings, NPS comments"
Agent: ps-researcher → docs/research/onboarding-journey.md

Step 2: "Analyze friction points and categorize by severity and frequency"
Agent: ps-analyst → docs/analysis/onboarding-friction.md

Content includes:
- Journey phases (Discover → Try → Buy → Use)
- Touchpoint inventory
- Pain points with evidence
- Emotion mapping
- Opportunity areas
```

##### L2 (Architect) - Constraints

| Constraint | Impact | Mitigation |
|------------|--------|------------|
| Sample bias | Power users over-represented | Stratify by user segment |
| Memory decay | Users forget early friction | Use contemporaneous data |

**Anti-patterns to avoid:**
- AP-003: Mapping every possible journey variant
- AP-002: Creating friction analysis without journey context

---

#### UX-005: A/B Test Results Synthesis

**Domain:** User Experience
**Scenario:** Three A/B tests completed. Need synthesis to inform design system update.

##### L0 (ELI5) - What & Why
> ps-synthesizer for A/B tests is like a meta-analysis doctor who reads 10 studies and finds what they agree on. Individual tests might be noisy, but patterns across tests reveal truth.

##### L1 (Engineer) - How

```
Invocation: "Synthesize A/B test results for button placement,
           color contrast, and copy length into actionable patterns"

Agent: ps-synthesizer
Output: docs/synthesis/ab-test-patterns.md

Content includes:
- Test summary matrix
- Statistically significant findings
- Pattern catalog (PAT-XXX)
- Design system recommendations
- Caveats and limitations
```

##### L2 (Architect) - Constraints

| Constraint | Impact | Mitigation |
|------------|--------|------------|
| Statistical significance | Small effects may be noise | Report confidence intervals |
| Context sensitivity | Results may not generalize | Note test population |

**Anti-patterns to avoid:**
- AP-002: Creating design system update without test synthesis
- AP-001: Mixing synthesis with new test design

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

### AP-005: Critic-Everything

```
+===================================================================+
| ANTI-PATTERN: Critic-Everything                                   |
+===================================================================+
|                                                                   |
| SYMPTOM:    Using ps-critic for every output regardless of need.  |
|             All outputs go through critique loop even when not    |
|             quality-sensitive.                                    |
|                                                                   |
| CAUSE:      Over-engineering. "More iteration = better quality."  |
|             Not recognizing when one-shot is sufficient.          |
|                                                                   |
| IMPACT:     - Unnecessary latency (3x for each iteration)         |
|             - Wasted tokens on trivial improvements               |
|             - Decision fatigue from constant feedback             |
|                                                                   |
| FIX:        Only use Generator-Critic when:                       |
|             - Output is quality-sensitive (ADRs, docs)            |
|             - Iteration time is acceptable                        |
|             - NOT for validation (use ps-validator)               |
|             - NOT for defect detection (use ps-reviewer)          |
|                                                                   |
+===================================================================+
```

**Example (Bad):**
```
"Research caching options, then critique the research"
"Create status report, then critique the status report"
# Over-critiquing non-quality-sensitive outputs
```

**Example (Good):**
```
"Research caching options"        # One-shot research is fine
"Create ADR, critique until excellent"  # ADRs benefit from polish
```

---

### AP-006: Infinite Critic Loop

```
+===================================================================+
| ANTI-PATTERN: Infinite Critic Loop                                |
+===================================================================+
|                                                                   |
| SYMPTOM:    Generator-Critic loop never terminates. Keeps         |
|             iterating even when improvements are minimal.         |
|                                                                   |
| CAUSE:      No circuit breaker. Threshold too high (0.99).        |
|             Not tracking consecutive no-improvement iterations.   |
|                                                                   |
| IMPACT:     - Infinite loop consuming resources                   |
|             - User waiting forever for "perfect" output           |
|             - Quality plateau not recognized                      |
|                                                                   |
| FIX:        Always use circuit breaker:                           |
|             - max_iterations: 3 (hard limit)                      |
|             - acceptance_threshold: 0.85 (not 0.99)               |
|             - consecutive_no_improvement: 2 (detect plateau)      |
|                                                                   |
+===================================================================+
```

**Circuit Breaker Parameters:**
| Parameter | Value | Purpose |
|-----------|-------|---------|
| max_iterations | 3 | Hard stop after 3 iterations |
| acceptance_threshold | 0.85 | Good enough, not perfect |
| improvement_threshold | 0.10 | Must improve by 10% to continue |
| no_improvement_limit | 2 | Stop after 2 flat iterations |

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
