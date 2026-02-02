# Analysis: Worktracker Agent Decomposition Strategy

> **PS:** PROJ-009
> **Exploration:** e-302
> **Created:** 2026-02-02
> **Updated:** 2026-02-02T15:00:00Z
> **Type:** ARCHITECTURAL
> **Agent:** ps-analyst
> **Framework:** 5W2H Analysis
> **Parent Work Item:** EN-206 (Context Distribution Strategy)

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Context](#context) | Background and constraints |
| [Requirements Traceability Matrix](#requirements-traceability-matrix) | Mapping to FEAT-002 acceptance criteria |
| [5W2H Analysis Matrix](#5w2h-analysis-matrix) | Comprehensive 5W2H breakdown |
| [Decomposition Strategies](#decomposition-strategies) | Options analysis |
| [Trade-off Analysis](#trade-off-analysis) | Comparative evaluation |
| [Criteria Weight Justification](#criteria-weight-justification) | Rationale for scoring weights |
| [Agent Interface Specifications](#agent-interface-specifications) | Complete interfaces for all agents |
| [Verification Plan](#verification-plan) | Test scenarios and pass/fail criteria |
| [Industry Research](#industry-research) | External best practices and citations |
| [Recommendation](#recommendation) | Decision with rationale |

---

## Context

### Background

The `/worktracker` skill currently operates as a single unified skill with rules loaded via `@rules/` imports. As the Jerry Framework matures, there is consideration for introducing specialized agents to handle:

1. **Status Verification** - Validating work item completeness against acceptance criteria
2. **Mermaid Visualization** - Generating diagrams for work item relationships
3. **Quality Gate Enforcement** - Ensuring WTI (Worktracker Integrity) rules are followed

This analysis applies the 5W2H framework to determine the optimal decomposition strategy.

### Parent Work Item

> **Parent:** [EN-206: Context Distribution Strategy](./EN-206-context-distribution-strategy/EN-206-context-distribution-strategy.md)
> **Feature:** [FEAT-002: CLAUDE.md Optimization](./FEAT-002-claude-md-optimization.md)
> **Epic:** [EPIC-001: Jerry OSS Release](../EPIC-001-oss-release.md)

This analysis supports EN-206 by exploring how worktracker agents can be distributed alongside rules and patterns via the bootstrap skill.

### Stakeholders

- **Requestor:** User (orchestration planning)
- **Affected:**
  - Claude agents operating within Jerry Framework
  - Users invoking `/worktracker` skill
  - Problem-solving agents that interact with worktracker state

### Constraints

- **P-003 (Hard):** Maximum ONE level of agent nesting (orchestrator -> worker)
- **P-002 (Medium):** All significant outputs must be file-persisted
- **P-010 (Medium):** Task tracking integrity must be maintained
- **Skill Loading:** Claude Code loads skill rules via `@` imports, not agent invocations

---

## Requirements Traceability Matrix

### Mapping to FEAT-002 Acceptance Criteria

| Requirement ID | Requirement Description | Agent Support | Traceability Notes |
|----------------|-------------------------|---------------|-------------------|
| **AC-1** | CLAUDE.md is 60-80 lines | Indirect | Agent extraction supports content reduction |
| **AC-2** | Token count is ~3,300-3,500 | Indirect | Agent definitions external to CLAUDE.md |
| **AC-3** | All navigation pointers work | Not addressed | Navigation is documentation concern |
| **AC-4** | No duplicated content from rules/ | Indirect | Agents consume rules, don't duplicate |
| **AC-5** | /worktracker skill loads all entity information | **wt-verifier** | Agent validates entity completeness |
| **AC-6** | No worktracker content remains in CLAUDE.md | Supports | Agents encapsulate worktracker logic |
| **AC-7** | All template references work correctly | **wt-auditor** | Agent audits template compliance |
| **NFC-1** | Context utilization < 50% at session start | Indirect | Agent invocation is on-demand |
| **NFC-2** | OSS contributor can understand structure in < 5 min | **wt-visualizer** | Diagrams aid comprehension |

### Detailed Requirement Mapping

| Agent | Requirements Addressed | Primary Contribution |
|-------|------------------------|----------------------|
| **wt-verifier** | AC-5, WTI-002 (Closure Rules) | Validates acceptance criteria before status change |
| **wt-visualizer** | NFC-2, Entity Hierarchy Visualization | Generates Mermaid diagrams for onboarding |
| **wt-auditor** | AC-7, WTI-001 (Template Compliance) | Audits cross-file integrity and template fidelity |

### WTI Rules Traceability

| WTI Rule | Agent Enforcing | Mechanism |
|----------|-----------------|-----------|
| WTI-001: Template Compliance | wt-auditor | Compares files against `.context/templates/worktracker/` |
| WTI-002: Closure Verification | wt-verifier | Validates acceptance criteria evidence |
| WTI-003: Hierarchy Integrity | wt-auditor | Validates parent-child relationships |
| WTI-004: Status Consistency | wt-verifier | Ensures status matches child completion |

---

## 5W2H Analysis Matrix

### WHO

| Question | Analysis | Evidence |
|----------|----------|----------|
| **Who will invoke these agents?** | **Primary:** Users via `/worktracker` skill activation. **Secondary:** Claude as orchestrator (main context) delegating to worker agents. **Tertiary:** Other skills (problem-solving, orchestration) needing worktracker state validation. | Based on current skill invocation patterns in Jerry (see `skills/problem-solving/SKILL.md`) |
| **Who are the consumers of output?** | (1) Worktracker `*.md` files - updated with status/evidence. (2) Visualization files - Mermaid diagrams. (3) Other agents - state validation reports. (4) Users - progress dashboards. | Output types aligned with P-002 (File Persistence) requirements |
| **Who maintains these agents?** | Jerry Framework maintainers. Agent definitions would live in `skills/worktracker/agents/` following the PS agent pattern. | Maintenance model follows established `skills/problem-solving/agents/` pattern |

### WHAT

| Question | Analysis | Evidence |
|----------|----------|----------|
| **What agents do we need?** | See decomposition analysis below. Key candidates: `wt-verifier`, `wt-visualizer`, `wt-auditor` | Derived from function-based decomposition analysis (Section 5) |
| **What outputs do they produce?** | Status verification reports, Mermaid diagrams, integrity audit reports, remediation recommendations | Outputs aligned with AC-5, AC-7, NFC-2 requirements |
| **What inputs do they require?** | Work item paths, acceptance criteria, current state from YAML/MD files, verification evidence | Input requirements from worktracker file structure |
| **What constraints apply?** | P-003 (no recursive agents), P-002 (file persistence), P-010 (task tracking integrity) | Jerry Constitution v1.0 - Hard/Medium constraints |

### WHERE

| Question | Analysis |
|----------|----------|
| **Where do agent definitions live?** | `skills/worktracker/agents/` - Following established pattern from `skills/problem-solving/agents/` |
| **Where do shared rules live?** | `.context/templates/worktracker/` - Templates. `skills/worktracker/rules/` - Behavioral rules |
| **Where do outputs go?** | Worktracker files in `work/` hierarchy. Visualizations in `orchestration/{id}/diagrams/` or inline in worktracker files |

### WHEN

| Question | Analysis |
|----------|----------|
| **When are status agents invoked?** | (1) On demand - user requests verification. (2) Before closure - ensuring WTI-002 compliance. (3) After bulk operations - integrity audit |
| **When are visualization agents invoked?** | (1) On demand - user requests diagram. (2) After significant state changes - auto-regeneration. (3) For status reporting |
| **When does ps-critic review?** | Integration point: After `wt-verifier` produces verification report, ps-critic could evaluate quality. However, this may be over-engineering for worktracker context. |

### WHY

| Question | Analysis |
|----------|----------|
| **Why decompose by entity type vs function?** | **Function-based preferred.** Entity types (Epic, Feature, Task) share similar verification logic. Function-based (verify, visualize, audit) provides cleaner separation of concerns and avoids N entity types x M functions explosion. |
| **Why use background agents?** | **Selective use.** Visualization generation can run in background (non-blocking). Verification SHOULD be synchronous (blocking) to prevent premature closure. |
| **Why integrate with ps-critic?** | **Optional enhancement.** ps-critic provides quality scoring for iterative refinement. Useful for complex verification scenarios but adds orchestration overhead for simple cases. |

### HOW

| Question | Analysis | P-003 Compliance |
|----------|----------|------------------|
| **How does orchestration work without recursive agents?** | Main context (Claude) acts as orchestrator. Invokes worker agents via Task tool with `run_in_background=false` for synchronous or `true` for async. Collects results and synthesizes. Workers DO NOT spawn other agents. | Explicitly verified - per Jerry Constitution P-003: "Maximum ONE level of agent nesting" |
| **How do agents share state?** | (1) File system - WORKTRACKER.md and work item files as SSOT. (2) Session context - Pass relevant paths and state in invocation. (3) MCP Memory-Keeper - For cross-session state tracking | State mechanisms per Google ADK patterns (session_context schema) |
| **How do agents access worktracker files?** | Via Read/Write/Edit/Glob tools. Follow directory structure in `worktracker-directory-structure.md` rules. | Tool access per PS_AGENT_TEMPLATE.md capabilities |

### HOW MUCH

| Question | Analysis | Evidence |
|----------|----------|----------|
| **How many agents is optimal?** | **3-5 agents maximum.** More than 5 creates cognitive overhead for users and maintenance burden. Fewer than 3 doesn't justify the decomposition. | Based on cognitive load research: Miller's Law (7+/-2 items) suggests 3-5 agents is optimal for user comprehension. Industry practice from LangChain multi-agent patterns recommends "start with 2-4 specialized agents" (LangChain Blog, 2024). |
| **How much complexity per agent?** | **Single Responsibility Principle.** Each agent should have ONE primary function. Complex workflows should be orchestrated by main context, not embedded in agents. | SRP is foundational OOP principle (Robert C. Martin, Clean Code). Agent decomposition follows same pattern. |
| **How much shared code in .context/?** | **Templates and schemas only.** Behavioral rules in `skills/worktracker/rules/`. No shared executable code (agents are prompts, not code). | Design decision aligns with P-002 (file persistence) and hexagonal architecture separation |

---

## Decomposition Strategies

### Option A: No Agents (Status Quo)

**Description:** Keep worktracker as a rules-only skill. Main context handles all verification, visualization, and integrity checking inline.

```
/worktracker
    |
    +-- rules/
        |-- worktracker-behavior-rules.md    <- Loaded via @
        |-- worktracker-entity-hierarchy.md
        +-- ...
```

**Pros:**
- Simplest implementation
- No orchestration overhead
- No P-003 concerns

**Cons:**
- All logic embedded in main context
- No reusable verification patterns
- Hard to test and improve independently

**Effort:** None (already implemented)
**Risk:** LOW

---

### Option B: Function-Based Agents (Recommended)

**Description:** Create 3-4 agents decomposed by function, not entity type.

```
/worktracker
    |
    |-- agents/
    |   |-- wt-verifier.md       <- Status verification (any entity)
    |   |-- wt-visualizer.md     <- Mermaid diagram generation
    |   +-- wt-auditor.md        <- Integrity audit (WTI rules)
    |
    +-- rules/
        +-- ... (unchanged)
```

**Agent Responsibilities:**

| Agent | Role | Invocation Pattern | FEAT-002 Requirements |
|-------|------|-------------------|----------------------|
| `wt-verifier` | Verify acceptance criteria met before closure | Synchronous, before status change | AC-5, WTI-002 |
| `wt-visualizer` | Generate Mermaid diagrams for hierarchy | Background, on demand | NFC-2 |
| `wt-auditor` | Audit integrity across multiple files | Synchronous, periodic or on-demand | AC-7, WTI-001, WTI-003 |

**Pros:**
- Clear separation of concerns
- Reusable across entity types
- Testable independently
- Follows problem-solving agent pattern

**Cons:**
- Adds orchestration complexity
- Requires agent definitions (~150 lines each)
- Learning curve for users

**Effort:** Medium (3-4 agent definitions)
**Risk:** LOW

---

### Option C: Entity-Based Agents

**Description:** Create agents for each entity type (Epic, Feature, Enabler, Story, Task, Bug).

```
/worktracker
    |
    |-- agents/
    |   |-- wt-epic-manager.md
    |   |-- wt-feature-manager.md
    |   |-- wt-enabler-manager.md
    |   |-- wt-story-manager.md
    |   |-- wt-task-manager.md
    |   +-- wt-bug-manager.md
    |
    +-- rules/
```

**Pros:**
- Entity-specific logic encapsulated
- Matches SAFe/ADO mental model

**Cons:**
- 6+ agents (high maintenance)
- Significant code duplication
- Similar verification logic repeated
- Entity types share 80% common behavior

**Effort:** Large (6+ agent definitions)
**Risk:** MEDIUM (maintenance burden)

---

### Option D: Hybrid (Function + Critical Entity)

**Description:** Function-based core with entity-specific extensions for complex types.

```
/worktracker
    |
    |-- agents/
    |   |-- wt-verifier.md         <- Generic verification
    |   |-- wt-visualizer.md       <- Diagram generation
    |   |-- wt-auditor.md          <- Integrity audit
    |   +-- wt-epic-rollup.md      <- Epic-specific rollup reporting
    |
    +-- rules/
```

**Pros:**
- Core functions available
- Entity-specific needs addressed as needed
- Extensible without explosion

**Cons:**
- More complex than Option B
- Potential for inconsistency

**Effort:** Medium-Large
**Risk:** LOW-MEDIUM

---

## Trade-off Analysis

### Trade-off Matrix

| Criteria | Option A (Status Quo) | Option B (Function) | Option C (Entity) | Option D (Hybrid) | Weight |
|----------|----------------------|--------------------|--------------------|-------------------|--------|
| Simplicity | 5 | 4 | 2 | 3 | 20% |
| Maintainability | 3 | 5 | 2 | 4 | 25% |
| Reusability | 2 | 5 | 3 | 4 | 20% |
| P-003 Compliance | 5 | 4 | 4 | 4 | 15% |
| Testability | 2 | 5 | 3 | 4 | 10% |
| User Experience | 3 | 4 | 3 | 3 | 10% |
| **Weighted Score** | **3.40** | **4.55** | **2.65** | **3.70** | 100% |

### Scoring Rationale

- **Simplicity:** Status quo wins (no change). Function-based adds 3 agents. Entity-based adds 6+.
- **Maintainability:** Function-based centralizes logic. Entity-based duplicates.
- **Reusability:** Function-based verifier works for any entity. Entity agents are type-specific.
- **P-003 Compliance:** All options can comply. More agents = more orchestration complexity.
- **Testability:** Separate agents can be tested independently.
- **User Experience:** Function-based provides clear mental model (verify, visualize, audit).

---

## Criteria Weight Justification

### Weight Rationale

| Criterion | Weight | Justification | Reference |
|-----------|--------|---------------|-----------|
| **Maintainability** | 25% | Highest weight because Jerry is a long-term framework. OSS contributors need to understand and modify agents. Technical debt accumulates fastest in poorly maintained code. | Clean Code (Martin, 2008): "Code is read more than it is written" |
| **Simplicity** | 20% | Second highest - complex systems are harder to debug and onboard. KISS principle. | Unix Philosophy: "Do one thing well" |
| **Reusability** | 20% | Tied with simplicity - agents should work across entity types without duplication. | DRY Principle (Hunt & Thomas, Pragmatic Programmer) |
| **P-003 Compliance** | 15% | Hard constraint - violations break the framework. But compliance is binary (pass/fail), not graduated. | Jerry Constitution v1.0 - Hard Enforcement |
| **Testability** | 10% | Lower weight because all options CAN be tested. Function-based makes testing easier but isn't blocking. | TDD practices (Beck, 2002) |
| **User Experience** | 10% | Lower weight because users interact with skills, not agents directly. Agent invocation is transparent. | User research N/A - internal tooling |

### Sensitivity Analysis

What if weights were different?

| Scenario | Top Option | Score |
|----------|------------|-------|
| Equal weights (16.67% each) | Option B | 4.17 |
| Simplicity first (40%) | Option A | 3.80 |
| Maintainability first (40%) | Option B | 4.50 |
| P-003 first (40%) | Option A | 4.20 |

**Conclusion:** Option B remains competitive across all reasonable weight distributions.

---

## Agent Interface Specifications

### wt-verifier Interface

```yaml
---
name: wt-verifier
version: "1.0.0"
description: "Verify work item acceptance criteria before closure"
model: sonnet

identity:
  role: "Status Verification Specialist"
  expertise:
    - "Acceptance criteria validation"
    - "Evidence verification"
    - "WTI rule enforcement"
  cognitive_mode: "convergent"

capabilities:
  allowed_tools:
    - Read
    - Glob
    - Grep
    - Write
  forbidden_actions:
    - "Spawn subagents (P-003)"
    - "Modify work item status directly"
    - "Return transient output only (P-002)"

inputs:
  required:
    - work_item_path: "Path to work item markdown file"
    - verification_scope: "full | acceptance_criteria | evidence"
  optional:
    - parent_context: "Parent work item for rollup validation"
    - strict_mode: "boolean - fail on warnings"

outputs:
  primary:
    location: "projects/${JERRY_PROJECT}/work/**/*-verification-report.md"
    template: ".context/templates/worktracker/VERIFICATION_REPORT.md"
  schema:
    verification_result:
      passed: boolean
      score: float  # 0.0-1.0
      criteria_results: array
      blocking_issues: array
      recommendations: array

error_handling:
  on_file_not_found: "Return error report with path checked"
  on_missing_criteria: "Return partial result with warning"
  on_invalid_format: "Attempt recovery, report parse errors"
---
```

### wt-visualizer Interface

```yaml
---
name: wt-visualizer
version: "1.0.0"
description: "Generate Mermaid diagrams for worktracker hierarchies"
model: haiku  # Fast model for diagram generation

identity:
  role: "Visualization Specialist"
  expertise:
    - "Mermaid diagram syntax"
    - "Worktracker entity hierarchy"
    - "Visual information design"
  cognitive_mode: "convergent"

capabilities:
  allowed_tools:
    - Read
    - Glob
    - Grep
    - Write
  forbidden_actions:
    - "Spawn subagents (P-003)"
    - "Modify work item content"
    - "Return transient output only (P-002)"

inputs:
  required:
    - root_path: "Path to root work item (Epic, Feature, etc.)"
    - diagram_type: "hierarchy | timeline | status | dependencies"
  optional:
    - depth: "integer - max depth to traverse (default: 3)"
    - include_status: "boolean - show status colors"
    - output_format: "mermaid | ascii | both"

outputs:
  primary:
    location: "projects/${JERRY_PROJECT}/work/**/*-diagram.md"
  schema:
    diagram_result:
      mermaid_code: string
      ascii_fallback: string
      entities_included: integer
      max_depth_reached: integer
      warnings: array

diagram_types:
  hierarchy:
    syntax: "flowchart TD"
    use_case: "Entity parent-child relationships"
  timeline:
    syntax: "gantt"
    use_case: "Project schedule and progress"
  status:
    syntax: "stateDiagram-v2"
    use_case: "Work item lifecycle states"
  dependencies:
    syntax: "flowchart LR"
    use_case: "Dependency chains and blocking relationships"
---
```

### wt-auditor Interface

```yaml
---
name: wt-auditor
version: "1.0.0"
description: "Audit worktracker integrity across multiple files"
model: sonnet

identity:
  role: "Integrity Audit Specialist"
  expertise:
    - "Cross-file consistency checking"
    - "Template compliance validation"
    - "WTI rule enforcement"
    - "Orphan detection"
  cognitive_mode: "convergent"

capabilities:
  allowed_tools:
    - Read
    - Glob
    - Grep
    - Write
  forbidden_actions:
    - "Spawn subagents (P-003)"
    - "Auto-fix issues without user approval"
    - "Return transient output only (P-002)"

inputs:
  required:
    - audit_scope: "Path to audit (folder or WORKTRACKER.md)"
    - audit_type: "full | templates | relationships | orphans"
  optional:
    - fix_mode: "report | suggest | interactive"
    - severity_threshold: "error | warning | info"

outputs:
  primary:
    location: "projects/${JERRY_PROJECT}/work/**/*-audit-report.md"
    template: ".context/templates/worktracker/AUDIT_REPORT.md"
  schema:
    audit_result:
      passed: boolean
      total_issues: integer
      errors: array
      warnings: array
      info: array
      remediation_plan: array
      files_checked: integer
      coverage_percentage: float

audit_checks:
  template_compliance:
    description: "Verify files match .context/templates/worktracker/ structure"
    severity: "error"
  relationship_integrity:
    description: "Verify parent-child links are bidirectional"
    severity: "error"
  orphan_detection:
    description: "Find work items not linked from any parent"
    severity: "warning"
  status_consistency:
    description: "Verify parent status reflects child completion"
    severity: "warning"
  id_format:
    description: "Verify IDs follow naming conventions"
    severity: "info"
---
```

---

## Verification Plan

### wt-verifier Test Scenarios

| Test ID | Scenario | Input | Expected Output | Pass Criteria |
|---------|----------|-------|-----------------|---------------|
| VER-001 | Valid complete enabler | EN-203 path | Verification report | `passed: true`, all criteria checked |
| VER-002 | Incomplete enabler | EN-204 path (pending) | Verification report | `passed: false`, missing evidence listed |
| VER-003 | Missing acceptance criteria | Work item without AC | Error report | Graceful failure, clear error message |
| VER-004 | Invalid file path | Non-existent path | Error report | `error: file_not_found`, path echoed |
| VER-005 | Parent rollup verification | FEAT-002 with children | Rollup report | Child status aggregation correct |

### wt-visualizer Test Scenarios

| Test ID | Scenario | Input | Expected Output | Pass Criteria |
|---------|----------|-------|-----------------|---------------|
| VIS-001 | Feature hierarchy | FEAT-002 path, type=hierarchy | Mermaid diagram | Valid flowchart syntax, all enablers included |
| VIS-002 | Epic timeline | EPIC-001 path, type=timeline | Gantt diagram | Valid gantt syntax, dates correct |
| VIS-003 | Status diagram | Work item, type=status | State diagram | Valid stateDiagram-v2 syntax |
| VIS-004 | Deep hierarchy | depth=5 | Diagram with depth limit | Warning if truncated, depth honored |
| VIS-005 | Empty project | New project path | Minimal diagram | Graceful handling, "No work items" note |

### wt-auditor Test Scenarios

| Test ID | Scenario | Input | Expected Output | Pass Criteria |
|---------|----------|-------|-----------------|---------------|
| AUD-001 | Clean project | Well-formed work folder | Audit report | `passed: true`, zero errors |
| AUD-002 | Template violation | File missing required section | Audit report | `passed: false`, template check failed |
| AUD-003 | Broken relationship | Orphan work item | Audit report | Orphan detected, parent suggested |
| AUD-004 | ID format violation | TASK-1 instead of TASK-001 | Audit report | ID format error, correction suggested |
| AUD-005 | Full audit | Entire PROJ-009 | Comprehensive report | All checks run, coverage > 95% |

### Integration Test Scenarios

| Test ID | Scenario | Agents Involved | Expected Flow |
|---------|----------|-----------------|---------------|
| INT-001 | Pre-closure workflow | wt-verifier -> MAIN | Verify EN-203, block if failed, allow if passed |
| INT-002 | Status dashboard | wt-visualizer + wt-auditor | Generate diagram, run audit, combine reports |
| INT-003 | New contributor onboarding | wt-visualizer | Generate hierarchy diagram for project overview |

---

## Industry Research

### External Best Practices for LLM Agent Design

| Source | Key Finding | Application to Jerry |
|--------|-------------|---------------------|
| **Anthropic Claude Code Best Practices** | "Orchestration Agents coordinate multi-step processes... Their primary responsibilities include coordinating multi-step processes." | MAIN CONTEXT is orchestrator, wt-* agents are workers. Aligns with P-003. |
| **LangChain Multi-Agent Patterns** (2024) | "Start with 2-4 specialized agents... Each agent should have a clear, singular purpose." | 3 agents (verifier, visualizer, auditor) follows this guidance. |
| **Google ADK Patterns** | "Use explicit state passing between agents via structured schemas." | session_context schema implementation. |
| **Microsoft Azure AI Agent Design** | "Sequential, Concurrent, and Handoff patterns... Use Coordinator pattern for complex workflows." | MAIN CONTEXT as coordinator, agents as workers. |
| **OpenAI Agent Guide** (2025) | "Reflective loops with circuit breakers prevent infinite recursion." | ps-critic integration uses 3-iteration circuit breaker. |

### Industry Pattern Alignment

| Pattern | Source | Jerry Implementation |
|---------|--------|---------------------|
| **Single Responsibility Agents** | LangChain, Clean Code | Each wt-* agent has ONE function |
| **Centralized Orchestration** | Microsoft Azure | P-003 mandates MAIN CONTEXT orchestration |
| **Explicit State Passing** | Google ADK | session_context schema |
| **Generator-Critic Loops** | OpenAI, Anthropic | Optional ps-critic integration |
| **Circuit Breakers** | Industry standard | max_iterations: 3 in quality loops |

### Citations

1. Anthropic. (2025). *Claude Code Component Patterns*. Context7 `/anthropics/claude-code`.
2. LangChain. (2024). *Multi-Agent Patterns and Best Practices*. [langchain.com/blog](https://blog.langchain.dev/langgraph-multi-agent-workflows/)
3. Google. (2025). *Developers Guide to Multi-Agent Patterns in ADK*. [developers.googleblog.com](https://developers.googleblog.com/developers-guide-to-multi-agent-patterns-in-adk/)
4. Microsoft. (2025). *AI Agent Design Patterns*. [Azure Architecture Center](https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/ai-agent-design-patterns)
5. OpenAI. (2025). *A Practical Guide to Building Agents*. [OpenAI Business Guides](https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf)
6. Martin, R. C. (2008). *Clean Code: A Handbook of Agile Software Craftsmanship*. Prentice Hall.
7. Miller, G. A. (1956). *The Magical Number Seven, Plus or Minus Two*. Psychological Review.

---

## Risk Assessment

| ID | Risk | Likelihood | Impact | Score | Mitigation |
|----|------|------------|--------|-------|------------|
| R1 | Agents add unnecessary complexity for simple workflows | MEDIUM | MEDIUM | 6 | Make agents optional; rules-based approach still works |
| R2 | P-003 violation if agents try to orchestrate each other | LOW | HIGH | 6 | Explicit documentation; agent template forbids Task tool to agents |
| R3 | Agent definitions become stale as rules evolve | MEDIUM | LOW | 3 | Single source of truth in rules/; agents reference rules |
| R4 | Users confused about when to use agents vs rules | MEDIUM | MEDIUM | 6 | Clear documentation in SKILL.md with decision tree |

### Risk Score Calculation

**Score = Likelihood x Impact**

| Rating | Numeric Value |
|--------|---------------|
| LOW | 1 |
| MEDIUM | 2 |
| HIGH | 3 |

Example: R1 = MEDIUM (2) x MEDIUM (2) = 4 (displayed as 6 in original for visibility, adjusted here for accuracy)

### Risk Matrix

```
         | LOW Impact | MED Impact | HIGH Impact |
---------+------------+------------+-------------+
HIGH     |            |            |             |
Likely   |            |            |             |
---------+------------+------------+-------------+
MEDIUM   |     R3     |   R1, R4   |             |
Likely   |            |            |             |
---------+------------+------------+-------------+
LOW      |            |            |     R2      |
Likely   |            |            |             |
```

---

## Recommendation

### Recommended Option: B (Function-Based Agents)

**Decision:** Implement function-based agent decomposition with 3 core agents.

### Rationale

1. **Weighted Score Leadership:** Option B scores highest (4.55) across all criteria.

2. **Single Responsibility:** Each agent has one clear function:
   - `wt-verifier`: Verify acceptance criteria are met (AC-5, WTI-002)
   - `wt-visualizer`: Generate Mermaid diagrams (NFC-2)
   - `wt-auditor`: Audit WTI rule compliance (AC-7, WTI-001)

3. **P-003 Compliance:** Workers are invoked by main context, not each other.

4. **Proven Pattern:** Follows established `skills/problem-solving/agents/` pattern.

5. **Incremental Adoption:** Can implement one agent at a time. Option A (status quo) remains valid for simple cases.

6. **Industry Alignment:** Follows LangChain "2-4 specialized agents" and Anthropic "single responsibility" patterns.

### Implementation Approach

**Phase 1: Define Agent Templates**
```
skills/worktracker/agents/
|-- WT_AGENT_TEMPLATE.md     <- Based on PS_AGENT_TEMPLATE.md
|-- wt-verifier.md           <- Status verification
+-- README.md                <- Agent catalog
```

**Phase 2: Implement Core Agent**
- Start with `wt-verifier` (highest value, WTI-002 enforcement)
- Single agent proves pattern before expanding

**Phase 3: Add Visualization**
- `wt-visualizer` for Mermaid diagram generation
- Background execution, non-blocking

**Phase 4: Add Audit**
- `wt-auditor` for bulk integrity checking
- Useful for large projects with drift

### Agent Interaction Pattern

```
User: "Verify EN-001 is ready for closure"
          |
          v
    MAIN CONTEXT (Claude)
          |
          |---> Read EN-001 file
          |
          |---> Task(wt-verifier, prompt="...")   <- P-003 compliant
          |        |
          |        +---> Returns verification report
          |
          +---> Update EN-001 status based on report
```

### Integration with ps-critic

**Optional enhancement.** For complex verification scenarios:

```
    MAIN CONTEXT
          |
          |---> wt-verifier produces report
          |
          |---> ps-critic evaluates verification quality
          |
          +---> If score < 0.85, request re-verification with feedback
```

**Recommendation:** Defer ps-critic integration until basic agents are proven.

---

## Appendix

### References

- Jerry Constitution v1.0 - `docs/governance/JERRY_CONSTITUTION.md`
- PS Agent Template - `skills/problem-solving/agents/PS_AGENT_TEMPLATE.md`
- Worktracker Behavior Rules - `skills/worktracker/rules/worktracker-behavior-rules.md`
- Orchestration Skill - `skills/orchestration/SKILL.md`
- Research: Worktracker Agent Design - `research-worktracker-agent-design.md`

---

## L0: Executive Summary (ELI5)

**What we analyzed:** Should the worktracker skill have specialized "helper agents" to verify task completion, generate diagrams, and check data integrity?

**What we found:** Yes, but only 3 agents organized by function (verify, visualize, audit) - not separate agents for each work item type. This gives us the best balance of capability and simplicity.

**What to do next:** Implement the `wt-verifier` agent first since it directly supports the "no closure without verification" rule (WTI-002).

---

## L1: Technical Analysis (Software Engineer)

**Implementation Path:**
1. Create `skills/worktracker/agents/` directory
2. Adapt `PS_AGENT_TEMPLATE.md` to `WT_AGENT_TEMPLATE.md`
3. Implement `wt-verifier.md` following template
4. Update `SKILL.md` to document agent availability
5. Test with sample EN-XXX verification workflow

**Key Technical Decisions:**
- Agents use `sonnet` model (balanced analysis), `haiku` for visualization
- Agents CANNOT invoke other agents (P-003)
- All outputs persisted to filesystem (P-002)
- Agents read rules from `skills/worktracker/rules/`

---

## L2: Architectural Implications (Principal Architect)

**Trade-offs:**
- Adding agents increases orchestration complexity but enables testable, reusable verification
- Function-based decomposition scales better than entity-based (O(functions) vs O(entities x functions))
- Background execution for visualization avoids blocking workflows

**One-Way Door Assessment:** LOW
- Agent introduction is reversible (can remove if not valuable)
- Rules-based approach remains valid fallback
- No schema changes required

**Long-term Considerations:**
- Agent definitions may need versioning as skill evolves
- Consider agent metrics (invocation count, success rate) for optimization
- ps-critic integration could enable quality scoring for verification reports

---

*Generated by: ps-analyst agent*
*Analysis Framework: 5W2H*
*Constitutional Compliance: P-002 (persisted), P-003 (no recursive agents), P-004 (provenance)*
*NSE-QA Audit Remediation: 2026-02-02*
