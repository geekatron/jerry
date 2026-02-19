# Jerry Skill Pattern Research

> **PS ID:** work-026
> **Entry ID:** e-001
> **Topic:** Jerry Skill Architecture Patterns
> **Date:** 2026-01-30
> **Researcher:** ps-researcher v2.2.0

---

## L0: Executive Summary (ELI5)

Jerry skills are like specialized teams with well-defined roles and workflows. Each skill (like problem-solving, NASA SE, and orchestration) is a collection of expert agents who work together following proven patterns. The architecture uses three key principles:

1. **Clear Identity** - Every skill and agent knows exactly what they do, like job descriptions
2. **Structured Workflows** - Step-by-step playbooks and templates ensure consistency
3. **Constitutional Compliance** - Built-in rules prevent common mistakes (like agents spawning other agents recursively)

Think of it like a professional kitchen: each skill is a station (pastry, grill, salad), each agent is a chef with expertise, and the playbooks are standardized recipes. The SKILL.md is the menu board showing what's available, and templates are the recipe cards ensuring consistent output.

**Key Finding:** All three skills follow the same architectural patterns, making it easy to create new skills by following established conventions.

---

## L1: Technical Analysis (Software Engineer)

### 1. Skill Structure Patterns

#### 1.1 SKILL.md Organization

All three skills follow an identical YAML frontmatter + Markdown content structure:

**Universal YAML Frontmatter Schema:**

```yaml
---
name: "{skill-name}"
description: "{one-line purpose + key capabilities + activation context}"
version: "X.Y.Z"
allowed-tools: [Read, Write, Edit, Glob, Grep, Bash, Task, WebSearch, WebFetch]
activation-keywords:
  - "{keyword-1}"
  - "{keyword-2}"
  - "{keyword-N}"
---
```

| Skill | Name | Version | Keyword Count |
|-------|------|---------|---------------|
| problem-solving | `problem-solving` | 2.1.0 | 16 |
| nasa-se | `nasa-se` | 1.1.0 | 31 |
| orchestration | `orchestration` | 2.1.0 | 10 |

**Common Markdown Sections (All Skills):**

| Section | Purpose | Present In |
|---------|---------|------------|
| **Document Audience (Triple-Lens)** | L0/L1/L2 reading guide | ✅ All 3 |
| **Purpose** | Skill mission and capabilities | ✅ All 3 |
| **When to Use This Skill** | Activation criteria | ✅ All 3 |
| **Available Agents** | Agent registry table | ✅ All 3 |
| **Invoking an Agent** | 3 invocation methods | ✅ All 3 |
| **Orchestration Flow** | Multi-agent coordination | ✅ All 3 |
| **State Passing Between Agents** | State key registry | ✅ All 3 |
| **Tool Invocation Examples** | Concrete tool usage | ✅ All 3 |
| **Mandatory Persistence (P-002)** | File output requirement | ✅ All 3 |
| **Constitutional Compliance** | Jerry Constitution mapping | ✅ All 3 |
| **Quick Reference** | Common workflows table | ✅ All 3 |
| **Agent Details** | Links to agent specs | ✅ All 3 |

**Skill-Specific Sections:**

- **nasa-se:** Disclaimer, NASA Common Technical Processes table, NASA Standards References
- **orchestration:** Workflow Configuration (workflow IDs, pipeline aliases, dynamic paths)

#### 1.2 Agent Registry Pattern

All skills use a standardized agent registry table:

```markdown
| Agent | Role | Output Location |
|-------|------|-----------------|
| {agent-id} | {role-description} | {output-path} |
```

**Examples:**

**problem-solving:**
```markdown
| Agent | Role | Output Location |
|-------|------|-----------------|
| `ps-researcher` | Research Specialist - Gathers information with citations | `docs/research/` |
| `ps-critic` | Quality Evaluator - Iterative refinement with quality scores | `docs/critiques/` |
```

**nasa-se:**
```markdown
| Agent | Role | NASA Processes | Output Location |
|-------|------|----------------|-----------------|
| `nse-requirements` | Requirements Engineer | 1, 2, 11 | `requirements/` |
| `nse-explorer` | Exploration Engineer (Divergent) | 5, 17 | `exploration/` |
```

**orchestration:**
```markdown
| Agent | Role | Output |
|-------|------|--------|
| `orch-planner` | Creates orchestration plan with workflow diagram | `ORCHESTRATION_PLAN.md` |
| `orch-tracker` | Updates execution state after agent completion | `ORCHESTRATION.yaml`, `ORCHESTRATION_WORKTRACKER.md` |
```

**Pattern:** Agent IDs use `{skill-prefix}-{specialty}` format (e.g., `ps-researcher`, `nse-requirements`, `orch-planner`).

---

### 2. Agent Definition Patterns

#### 2.1 YAML Frontmatter Structure

**Universal Agent Metadata Schema:**

```yaml
---
name: "{agent-id}"
version: "X.Y.Z"
description: "{purpose + key features + integration}"
model: opus | sonnet | haiku  # Model selection based on complexity

# Identity Section (Anthropic best practice)
identity:
  role: "{Role Title}"
  expertise:
    - "{expertise-1}"
    - "{expertise-N}"
  cognitive_mode: "divergent | convergent"

# Persona Section (OpenAI GPT-4.1 guide)
persona:
  tone: "{tone}"
  communication_style: "{style}"
  audience_level: "adaptive"

# Capabilities Section
capabilities:
  allowed_tools: [...]
  output_formats: [markdown, yaml]
  forbidden_actions:
    - "Spawn recursive subagents (P-003)"
    - "Override user decisions (P-020)"
    - "Return transient output only (P-002)"

# Guardrails Section (KnowBe4 layered security)
guardrails:
  input_validation: {...}
  output_filtering: {...}
  fallback_behavior: warn_and_retry

# Output Section
output:
  required: true
  location: "{path-template}"
  template: "{template-file}"
  levels: [L0, L1, L2]

# Validation Section
validation:
  file_must_exist: true
  post_completion_checks: [...]

# Constitutional Compliance
constitution:
  reference: "docs/governance/JERRY_CONSTITUTION.md"
  principles_applied: [...]

# Enforcement Tier
enforcement:
  tier: "soft | medium | hard"
  escalation_path: "{escalation-description}"

# Session Context (Agent Handoff) - WI-SAO-002
session_context:
  schema: "docs/schemas/session_context.json"
  schema_version: "1.0.0"
  input_validation: true
  output_validation: true
  on_receive: [...]
  on_send: [...]
---
```

**Observed Variations by Skill:**

| Section | problem-solving | nasa-se | orchestration |
|---------|----------------|---------|---------------|
| `identity.nasa_processes` | ❌ | ✅ | ❌ |
| `identity.belbin_role` | ps-critic only | ❌ | ❌ |
| `guardrails.requirements_count` | ❌ | nse-requirements | ❌ |
| `guardrails.dependency_validation` | ❌ | nse-requirements | ❌ |
| `nasa_standards` | ❌ | ✅ All agents | ❌ |
| `prior_art` | ✅ All agents | ✅ All agents | ✅ All agents |
| `orchestration_guidance` | ps-critic only | ❌ | ✅ All agents |

#### 2.2 Agent Identity Specifications

**Common Identity Fields:**

```yaml
identity:
  role: "{Role Title}"              # Required - agent's job title
  expertise: [...]                  # Required - domain specializations
  cognitive_mode: "divergent | convergent"  # Required - thinking style
```

**Cognitive Modes:**

| Mode | Agents | Characteristics |
|------|--------|-----------------|
| **Divergent** | ps-researcher, nse-explorer | Explore broadly, generate options, discover patterns |
| **Convergent** | ps-critic, ps-analyst, nse-requirements | Narrow down, evaluate, decide |
| **Mixed** | orchestration agents | Context-dependent mode switching |

**Example: ps-researcher Identity:**

```yaml
identity:
  role: "Research Specialist"
  expertise:
    - "Literature review and synthesis"
    - "Web research and source validation"
    - "Library/framework documentation (via Context7)"
    - "Industry best practices analysis"
  cognitive_mode: "divergent"
```

**Example: nse-requirements Identity:**

```yaml
identity:
  role: "Requirements Engineer"
  expertise:
    - "Stakeholder needs elicitation and analysis"
    - "Technical requirements definition (shall statements)"
    - "Bidirectional traceability management"
  cognitive_mode: "convergent"
  nasa_processes:
    - "Process 1: Stakeholder Expectations Definition"
    - "Process 2: Technical Requirements Definition"
    - "Process 11: Requirements Management"
```

#### 2.3 Persona Specifications

**Universal Persona Pattern:**

```yaml
persona:
  tone: "professional | analytical | consultative"
  communication_style: "direct | constructive | consultative"
  audience_level: "adaptive"  # All agents use adaptive L0/L1/L2
```

**L0/L1/L2 Output Requirement:**

All agents MUST produce output at three levels:

```markdown
### L0: Executive Summary (ELI5)
*2-3 paragraphs accessible to non-technical stakeholders.*

### L1: Technical Analysis (Software Engineer)
*Implementation-focused content with specifics.*

### L2: Architectural Implications (Principal Architect)
*Strategic perspective with trade-offs.*
```

**Example from ps-researcher.md:**

```xml
<persona>
**Tone:** Professional and thorough - You write with authority backed by evidence.

**Communication Style:** Consultative - You present findings with context and explain significance, not just raw data.

**Audience Adaptation:** You MUST produce output at three levels:

- **L0 (ELI5):** Accessible executive summary. Use analogies. Answer "What does this mean for the project?"
- **L1 (Software Engineer):** Technical findings with code examples, configuration snippets, and implementation guidance.
- **L2 (Principal Architect):** Strategic implications, trade-offs, risks, and alignment with existing architecture.
</persona>
```

#### 2.4 Capabilities and Guardrails

**Allowed Tools Pattern:**

All agents specify allowed tools with usage patterns:

```yaml
capabilities:
  allowed_tools:
    - Read
    - Write
    - Edit
    - Glob
    - Grep
    - Bash
    - Task
    - WebSearch
    - WebFetch
    # Skill-specific tools
    - mcp__context7__resolve-library-id  # ps-researcher only
    - mcp__context7__query-docs          # ps-researcher only
```

**Forbidden Actions (Constitutional Compliance):**

Standard forbidden actions across all agents:

```yaml
capabilities:
  forbidden_actions:
    - "Spawn recursive subagents (P-003)"
    - "Override user decisions (P-020)"
    - "Return transient output only (P-002)"
    - "Make claims without citations (P-001, P-011)"  # ps/nse-specific
    - "Omit mandatory disclaimer (P-043)"             # nse-specific
```

**Guardrails Pattern:**

```yaml
guardrails:
  input_validation:
    ps_id_format: "^[a-z]+-\\d+(\\.\\d+)?$"
    entry_id_format: "^e-\\d+$"
  output_filtering:
    - no_secrets_in_output
    - all_claims_must_have_citations
  fallback_behavior: warn_and_retry
```

**Advanced Guardrails (nse-requirements):**

```yaml
guardrails:
  requirements_count:
    minimum: 1
    on_empty:
      action: reject
      message: "At least 1 requirement is required..."
      guidance: [...]
    maximum_recommended: 100
    on_exceed:
      action: warn
      allow_override: true
  dependency_validation:
    circular_dependency_check: true
    algorithm: "DFS with visited tracking"
```

#### 2.5 Constitutional Compliance

**Standard Constitutional Compliance Table:**

All agents include a self-critique checklist:

```markdown
| Principle | Enforcement | Agent Behavior |
|-----------|-------------|----------------|
| P-001 (Truth/Accuracy) | Soft | All claims cite sources; uncertainty acknowledged |
| P-002 (File Persistence) | **Medium** | ALL outputs persisted to files |
| P-003 (No Recursion) | **Hard** | Task tool spawns single-level agents only |
| P-004 (Provenance) | Soft | Full citation trail for all findings |
| P-011 (Evidence-Based) | Soft | Recommendations tied to evidence |
| P-022 (No Deception) | **Hard** | Transparent about limitations |

**Self-Critique Checklist (Before Response):**
- [ ] P-001: Are all claims sourced with citations?
- [ ] P-002: Is output persisted to file?
- [ ] P-004: Is the methodology documented?
- [ ] P-011: Are recommendations evidence-based?
- [ ] P-022: Am I transparent about limitations?
```

**Skill-Specific Principles:**

- **nasa-se:** P-040 (Traceability), P-041 (V&V Coverage), P-042 (Risk Transparency), P-043 (Disclaimer)
- **orchestration:** P-010 (Task Tracking)

---

### 3. Orchestration Patterns

#### 3.1 State Passing Mechanisms

**State Key Registry Pattern:**

All skills maintain a state key registry table:

```markdown
| Agent | Output Key | Provides |
|-------|------------|----------|
| {agent-id} | `{agent-id}_output` | {output-summary} |
```

**problem-solving State Keys:**

| Agent | Output Key | Provides |
|-------|------------|----------|
| ps-researcher | `researcher_output` | Research findings, sources |
| ps-analyst | `analyst_output` | Root cause, recommendations |
| ps-architect | `architect_output` | Decision, alternatives |
| ps-critic | `critic_output` | Quality score, improvement areas |

**nasa-se State Keys:**

| Agent | Output Key | Provides |
|-------|------------|----------|
| nse-requirements | `requirements_output` | Requirements baseline, traceability |
| nse-verification | `verification_output` | V&V status, VCRM |
| nse-risk | `risk_output` | Risk register, mitigation status |

**orchestration State Keys:**

Orchestration uses a different pattern - state is tracked in `ORCHESTRATION.yaml` (SSOT):

```yaml
workflow:
  id: "{workflow-id}"
  status: ACTIVE | PAUSED | COMPLETE | FAILED

pipelines:
  {pipeline-id}:
    current_phase: number
    phases:
      - agents:
          - id: "{agent-id}"
            status: PENDING | IN_PROGRESS | COMPLETE | FAILED
            artifact: "{path-to-output}"
```

#### 3.2 Agent Handoff Management

**Session Context Schema (WI-SAO-002):**

All agents validate handoffs using `docs/schemas/session_context.json`:

```yaml
session_context:
  schema_version: "1.0.0"
  session_id: "{uuid}"
  source_agent:
    id: "{agent-id}"
    family: "ps | nse | orch"
    cognitive_mode: "divergent | convergent"
    model: "opus | sonnet | haiku"
  target_agent:
    id: "{target-agent-id}"
  payload:
    key_findings: [...]
    open_questions: [...]
    blockers: []
    confidence: 0.0-1.0
    artifacts:
      - path: "{artifact-path}"
        type: "{artifact-type}"
        summary: "{one-line-summary}"
  timestamp: "{ISO-8601}"
```

**On Receive (Input Validation):**

1. Check `schema_version` matches "1.0.0"
2. Verify `target_agent.id` matches this agent
3. Extract `payload.key_findings` for context
4. Check `payload.blockers` - address before proceeding
5. Use `payload.artifacts` paths as inputs

**On Send (Output Validation):**

1. Populate `key_findings` from work results
2. Calculate `confidence` based on source quality
3. List all `artifacts` with paths
4. Set `timestamp` to current time

#### 3.3 Sequential Chain Example

**Pattern:** Agent A → Agent B → Agent C (order-dependent)

From problem-solving SKILL.md:

```markdown
User Request: "I need to understand why our tests are slow and fix it"

1. ps-researcher → Gather data on test execution patterns
   Output: docs/research/work-024-e-001-test-performance.md

2. ps-analyst → Apply 5 Whys to identify root cause
   Output: docs/analysis/work-024-e-002-root-cause.md

3. ps-architect → Create ADR for proposed solution
   Output: docs/decisions/work-024-e-003-adr-test-optimization.md

4. ps-validator → Verify solution meets constraints
   Output: docs/analysis/work-024-e-004-validation.md
```

#### 3.4 Cross-Pollinated Pipeline Example

**Pattern:** Two parallel pipelines with sync barriers

From orchestration SKILL.md:

```markdown
Pipeline A                    Pipeline B
    │                              │
    ▼                              ▼
┌─────────┐                  ┌─────────┐
│ Phase 1 │                  │ Phase 1 │
└────┬────┘                  └────┬────┘
     │                            │
     └──────────┬─────────────────┘
                ▼
        ╔═══════════════╗
        ║   BARRIER 1   ║  ← Cross-pollination
        ╚═══════════════╝
                │
     ┌──────────┴─────────────────┐
     │                            │
     ▼                            ▼
┌─────────┐                  ┌─────────┐
│ Phase 2 │                  │ Phase 2 │
└─────────┘                  └─────────┘
```

**Barrier Artifact Format:**

```markdown
# Barrier N: {Direction} Cross-Pollination

> **Source Pipeline:** {pipeline}
> **Target Pipeline:** {pipeline}
> **Phase Transition:** {from_phase} -> {to_phase}

## Key Findings
{extracted findings}

## For Target Pipeline
{how to use these findings}
```

#### 3.5 Generator-Critic Loop Example

**Pattern:** Iterative refinement with quality threshold

From ps-critic.md:

```markdown
Iteration 1:
  1. Generator (ps-architect) produces design.md
  2. Orchestrator invokes ps-critic with design.md
  3. ps-critic returns: score=0.65, threshold_met=false
  4. Orchestrator: 0.65 < 0.85, iteration=1 < 3 → REVISE
  5. Orchestrator sends critique to ps-architect

Iteration 2:
  1. Generator (ps-architect) produces design-v2.md
  2. Orchestrator invokes ps-critic with design-v2.md
  3. ps-critic returns: score=0.78, threshold_met=false
  4. Orchestrator: improvement = 0.78-0.65 = 0.13 > 0.10 → REVISE

Iteration 3:
  1. Generator (ps-architect) produces design-v3.md
  2. Orchestrator invokes ps-critic with design-v3.md
  3. ps-critic returns: score=0.88, threshold_met=true
  4. Orchestrator: 0.88 >= 0.85 → ACCEPT
```

**Circuit Breaker Parameters:**

```yaml
circuit_breaker:
  max_iterations: 3
  improvement_threshold: 0.10  # 10% improvement required
  acceptance_threshold: 0.85   # Score to accept without revision
  consecutive_no_improvement_limit: 2
```

---

### 4. Documentation Patterns

#### 4.1 docs/ Structure

**problem-solving:**
```
skills/problem-solving/
└── docs/
    └── ORCHESTRATION.md
```

**nasa-se:**
```
skills/nasa-se/
└── docs/
    ├── NASA-SE-MAPPING.md
    └── ORCHESTRATION.md
```

**orchestration:**
```
skills/orchestration/
└── docs/
    ├── PATTERNS.md
    └── STATE_SCHEMA.md
```

**Pattern:** Each skill has a `docs/` directory for supplementary documentation beyond SKILL.md and PLAYBOOK.md.

#### 4.2 PLAYBOOK.md Pattern

**Observed in:** orchestration skill only (v3.1.0)

**Universal YAML Frontmatter:**

```yaml
---
name: "{skill}-playbook"
description: "{step-by-step guidance summary}"
version: "X.Y.Z"
skill: "{skill-name}"
template: PLAYBOOK_TEMPLATE.md v1.0.0
constitutional_compliance: Jerry Constitution v1.0
patterns_covered: [...]
agents_covered: [...]
---
```

**Triple-Lens Structure:**

```markdown
# L0: The Big Picture (ELI5)
> Metaphors, analogies, decision guides

# L1: How To Use It (Engineer)
> Executable instructions, commands, file paths

# L2: Architecture & Constraints
> Anti-patterns, boundaries, invariants, design rationale
```

**Key Sections:**

1. **Document Overview** - Triple-lens cognitive framework diagram
2. **L0 Sections:**
   - What Is Orchestration? (Conductor Metaphor)
   - Why Does This Matter?
   - When Do I Use This?
   - The Cast of Characters (Agent Families)
3. **L1 Sections:**
   - Quick Start
   - Orchestration Patterns
   - Invocation Methods
   - Workflow: Cross-Pollinated Pipeline
   - Agent Reference
   - Output Locations
   - Common Scenarios
   - Tips and Best Practices
   - Troubleshooting
4. **L2 Sections:**
   - Anti-Pattern Catalog
   - Constraints & Boundaries
   - Invariants
   - State Management
   - Cross-Skill Integration
   - Design Rationale
   - Templates Reference
   - References
   - Quick Reference Card

**Anti-Pattern Catalog Format:**

```markdown
### AP-001: Recursive Subagent Spawning

+===================================================================+
| ANTI-PATTERN: Recursive Subagent Spawning                         |
+===================================================================+
| SYMPTOM:    {what-you-observe}                                    |
| CAUSE:      {root-cause}                                          |
| IMPACT:     {consequences}                                        |
| FIX:        {solution}                                            |
+===================================================================+
```

#### 4.3 RUNBOOK.md Pattern

**Status:** No RUNBOOK.md files found in any of the three skills.

**Hypothesis:** PLAYBOOK.md serves the combined purpose of both playbook (strategic) and runbook (tactical).

#### 4.4 Template Patterns

**problem-solving Templates:**
```
skills/problem-solving/templates/
└── critique.md
```

**nasa-se Templates:**
```
skills/nasa-se/templates/
├── alternative-analysis.md
├── concept-exploration.md
├── qa-report.md
├── review-checklists.md
└── trade-study.md
```

**orchestration Templates:**
```
skills/orchestration/templates/
├── ORCHESTRATION.template.yaml
├── ORCHESTRATION_PLAN.template.md
└── ORCHESTRATION_WORKTRACKER.template.md
```

**Pattern:** Each skill provides templates for its specific artifact types. NASA SE has the most templates (5), reflecting diverse SE work products.

---

### 5. Quality & Validation Patterns

#### 5.1 Validation Section in Agent Frontmatter

**Universal Validation Schema:**

```yaml
validation:
  file_must_exist: true
  post_completion_checks:
    - verify_file_created
    - verify_l0_l1_l2_present
    - verify_citations_present  # ps/nse-specific
```

**Skill-Specific Validations:**

**ps-critic:**
```yaml
validation:
  post_completion_checks:
    - verify_file_created
    - verify_artifact_linked
    - verify_l0_l1_l2_present
    - verify_quality_score_present
    - verify_improvement_recommendations
```

**nse-requirements:**
```yaml
validation:
  file_must_exist: true
  disclaimer_required: true  # NASA-specific
  post_completion_checks:
    - verify_file_created
    - verify_disclaimer_present
    - verify_l0_l1_l2_present
    - verify_requirements_have_rationale
    - verify_traceability_documented
```

#### 5.2 Quality Mechanisms

**ps-critic Quality Evaluation Framework:**

```yaml
evaluation_criteria:
  - name: "Completeness"
    weight: 0.25
  - name: "Accuracy"
    weight: 0.25
  - name: "Clarity"
    weight: 0.20
  - name: "Actionability"
    weight: 0.15
  - name: "Alignment"
    weight: 0.15
```

**Quality Score Calculation:**

```
quality_score = Σ(criterion_score × criterion_weight)
```

**Threshold Interpretation:**

| Score Range | Assessment | Recommendation |
|-------------|------------|----------------|
| 0.85 - 1.00 | EXCELLENT | Accept output |
| 0.70 - 0.84 | GOOD | Accept or minor revision |
| 0.50 - 0.69 | ACCEPTABLE | Revision recommended |
| 0.30 - 0.49 | NEEDS_WORK | Revision required |
| 0.00 - 0.29 | POOR | Major revision required |

**nse-requirements Quality Criteria:**

```markdown
### Requirements Quality Checklist

- [ ] Complete: All necessary requirements defined
- [ ] Consistent: No conflicting requirements
- [ ] Verifiable: Each requirement can be verified
- [ ] Traceable: Each requirement traced to parent need
- [ ] Unambiguous: Single interpretation possible
- [ ] Necessary: Each requirement serves a purpose
```

#### 5.3 Constitutional Compliance Enforcement

**Enforcement Tier Levels:**

| Tier | Behavior | Example |
|------|----------|---------|
| **Soft** | Warn user | P-001 (Truth/Accuracy), P-004 (Provenance) |
| **Medium** | Block completion | P-002 (File Persistence), P-040 (Traceability) |
| **Hard** | Reject operation | P-003 (No Recursion), P-022 (No Deception), P-043 (Disclaimer) |

**Example Enforcement (nse-requirements):**

```yaml
enforcement:
  tier: "medium"
  escalation_path: "Warn on missing traces → Block completion without artifact"
```

---

## L2: Strategic Implications (Principal Architect)

### 1. Cross-Skill Architectural Patterns

#### 1.1 Universal Skill Architecture

**Discovered Pattern:** All three skills share a common architectural blueprint:

```
{SKILL}/
├── SKILL.md                    # Interface Definition (SSOT)
│   ├── YAML Frontmatter        # Metadata
│   ├── Triple-Lens Audience    # L0/L1/L2 reading guide
│   ├── Purpose                 # Mission statement
│   ├── Available Agents        # Agent registry
│   ├── Invocation Methods      # 3 ways to invoke
│   ├── Orchestration Flow      # Multi-agent coordination
│   ├── State Passing           # State key registry
│   ├── Tool Examples           # Concrete usage
│   ├── Constitutional          # Jerry Constitution mapping
│   └── Quick Reference         # Command cheat sheet
│
├── PLAYBOOK.md                 # Implementation Guide (Triple-Lens)
│   ├── L0: Big Picture         # Metaphors, analogies
│   ├── L1: How To              # Executable instructions
│   └── L2: Architecture        # Constraints, anti-patterns
│
├── agents/                     # Agent Definitions
│   ├── {prefix}-agent1.md      # XML + Markdown hybrid
│   │   ├── YAML Frontmatter    # Metadata
│   │   ├── <agent> XML         # Structured specification
│   │   └── Markdown Body       # Human-readable docs
│   └── {prefix}-agentN.md
│
├── templates/                  # Output Templates
│   └── {artifact-type}.md
│
└── docs/                       # Supplementary Docs
    └── {topic}.md
```

**Implication:** New skills can be scaffolded by copying this structure and customizing content.

#### 1.2 Agent Definition Format Evolution

**Discovery:** Agents use a hybrid XML + Markdown format:

```markdown
---
{YAML frontmatter}
---

<agent>

<identity>...</identity>
<persona>...</persona>
<capabilities>...</capabilities>
<guardrails>...</guardrails>
<constitutional_compliance>...</constitutional_compliance>
<invocation_protocol>...</invocation_protocol>
<output_levels>...</output_levels>
<state_management>...</state_management>

</agent>

---

# {Agent Name}

{Markdown content for human readers}
```

**Rationale:**
- **YAML Frontmatter:** Machine-parseable metadata for tooling
- **XML Tags:** Structured sections for LLM parsing (Claude excels at XML)
- **Markdown Body:** Human-readable documentation

**Prior Art:**
- Anthropic's XML preference documented in [Claude 4 Best Practices](https://docs.claude.com/en/docs/build-with-claude/prompt-engineering/claude-4-best-practices)
- XML provides clearer boundaries than Markdown headers for LLM consumption

#### 1.3 L0/L1/L2 Triple-Lens Pattern

**Universal Application:**

| Artifact Type | L0 (ELI5) | L1 (Engineer) | L2 (Architect) |
|---------------|-----------|---------------|----------------|
| **SKILL.md** | Purpose, When to Use | Tool Examples, Invocation | Constitutional, State Passing |
| **PLAYBOOK.md** | Metaphors, Decision Guides | Commands, File Paths | Anti-Patterns, Constraints |
| **Agent Output** | Executive Summary | Technical Details | Strategic Implications |

**Key Insight:** This isn't just documentation structure - it's a cognitive framework for multi-audience communication.

**Example (orchestration PLAYBOOK.md):**

```
+============================================================================+
|                       TRIPLE-LENS COGNITIVE FRAMEWORK                       |
+=============================================================================+
|    L0 (ELI5)          L1 (Engineer)         L2 (Architect)                 |
|    ----------         -------------         --------------                 |
|    WHAT & WHY    ->   HOW (commands)   ->   CONSTRAINTS                    |
|    Metaphors          Invocations           Anti-patterns                  |
```

### 2. State Management Architecture

#### 2.1 State Passing Mechanisms Comparison

| Skill | State Mechanism | SSOT | Format |
|-------|----------------|------|--------|
| **problem-solving** | Output keys in session context | `researcher_output`, `analyst_output` | YAML in session context |
| **nasa-se** | Output keys in session context | `requirements_output`, `verification_output` | YAML in session context |
| **orchestration** | ORCHESTRATION.yaml | ORCHESTRATION.yaml | YAML file (persisted) |

**Key Difference:** Orchestration skill uses **file-based state** (`ORCHESTRATION.yaml`) while ps/nse skills use **context-based state** (session context payload).

**Rationale:**

- **ps/nse:** Short-lived agent chains (researcher → analyst → architect)
  - Context-based state sufficient for <10 agent handoffs
  - Lightweight, no file I/O overhead

- **orchestration:** Long-lived multi-agent workflows
  - File-based state required for checkpoint recovery
  - Survives context compaction
  - Machine-readable for automation

#### 2.2 Session Context Schema Adoption

**Standard Across All Skills:**

```yaml
session_context:
  schema: "docs/schemas/session_context.json"
  schema_version: "1.0.0"
  input_validation: true
  output_validation: true
```

**Validation Actions:**

1. **On Receive:**
   - Validate schema version
   - Verify target agent matches
   - Extract key findings
   - Process blockers

2. **On Send:**
   - Populate key findings
   - Calculate confidence
   - List artifacts
   - Set timestamp

**Implication:** Standardized handoff protocol enables cross-skill agent coordination (e.g., ps-architect → nse-architecture).

### 3. Orchestration Strategy

#### 3.1 P-003 Compliance: No Recursive Subagents

**Constitutional Hard Constraint:**

```
Maximum ONE level of nesting:
  MAIN CONTEXT (Orchestrator) → Worker Agent (end)

FORBIDDEN:
  MAIN CONTEXT → Worker → Sub-Worker → Sub-Sub-Worker
```

**Enforcement Across Skills:**

- **problem-solving:** Agents use Task tool for single-level delegation only
- **nasa-se:** Same single-level constraint
- **orchestration:** Orchestrator coordinates workers directly; workers do NOT spawn others

**Anti-Pattern (orchestration PLAYBOOK.md):**

```
AP-001: Recursive Subagent Spawning

SYMPTOM:    Agents spawning agents spawning agents...
CAUSE:      Orchestrator creates subagent which creates another subagent
IMPACT:     Context window exhausted, untraceable execution
FIX:        Maximum ONE level of nesting
```

**Design Rationale:**

- Prevents context explosion
- Enables checkpointing
- Maintains traceability
- Simplifies debugging

#### 3.2 Workflow Patterns Catalog

**Discovered:** orchestration PLAYBOOK.md documents 8 canonical patterns:

| # | Pattern | Cognitive Mode | Use Case |
|---|---------|---------------|----------|
| 1 | Single Agent | Depends | Direct task, no coordination |
| 2 | Sequential Chain | Convergent | Order-dependent state passing |
| 3 | Fan-Out | Divergent | Parallel independent research |
| 4 | Fan-In | Convergent | Aggregate multiple outputs |
| 5 | Cross-Pollinated | Mixed | Bidirectional pipeline exchange |
| 6 | Divergent-Convergent | Mixed | Explore then converge (diamond) |
| 7 | Review Gate | Convergent | Quality checkpoint (SRR/PDR/CDR) |
| 8 | Generator-Critic | Convergent | Iterative refinement loop |

**Pattern Selection Decision Tree:**

```
START: How many agents?
       |
  +----+----+
  |         |
  v         v
ONE       MULTIPLE
  |         |
  v         v
Pattern 1   Dependencies?
       |
  +----+----+
  |         |
  v         v
 YES        NO
  |         |
  v         v
Pattern 2   Pattern 3/4
  |
  v
Bidirectional?
  |
+----+----+
|         |
v         v
YES       NO
|         |
v         v
Pattern 5  Quality gates?
      |
 +----+----+
 |         |
 v         v
YES       NO
 |         |
 v         v
P7/P8     P6
```

**Strategic Insight:** These 8 patterns form a complete pattern language for multi-agent coordination. New workflows compose these patterns.

#### 3.3 Cognitive Mode Matching

**Discovery:** Agent cognitive modes align with workflow patterns:

**Divergent Agents** (Exploration):
- ps-researcher
- nse-explorer
- Used in: Pattern 3 (Fan-Out), Pattern 6 (Divergent phase)

**Convergent Agents** (Decision):
- ps-critic
- ps-analyst
- nse-requirements
- Used in: Pattern 2 (Sequential), Pattern 4 (Fan-In), Pattern 8 (Generator-Critic)

**Mixed Mode Agents** (Orchestration):
- orch-planner
- orch-tracker
- Used in: Pattern 5 (Cross-Pollinated)

**Implication:** Cognitive mode is a key agent attribute for orchestration planning. Divergent agents should precede convergent agents in workflows.

### 4. Quality & Validation Architecture

#### 4.1 Multi-Layer Validation

**Layer 1: Input Validation (Guardrails)**

```yaml
guardrails:
  input_validation:
    ps_id_format: "^[a-z]+-\\d+(\\.\\d+)?$"
    entry_id_format: "^e-\\d+$"
    requirement_id: "^REQ-NSE-[A-Z]{3}-\\d{3}$"  # nse-specific
  output_filtering:
    - no_secrets_in_output
    - all_claims_must_have_citations
```

**Layer 2: Process Validation (Constitutional)**

```yaml
constitution:
  principles_applied:
    - "P-001: Truth and Accuracy (Soft)"
    - "P-002: File Persistence (Medium)"
    - "P-003: No Recursive Subagents (Hard)"
    - "P-022: No Deception (Hard)"
```

**Layer 3: Output Validation (Post-Completion)**

```yaml
validation:
  post_completion_checks:
    - verify_file_created
    - verify_l0_l1_l2_present
    - verify_citations_present
```

**Layer 4: Quality Assessment (ps-critic)**

```yaml
quality_score = Σ(criterion_score × criterion_weight)
threshold: 0.85
circuit_breaker:
  max_iterations: 3
```

**Implication:** Defense-in-depth validation prevents issues at multiple stages.

#### 4.2 Generator-Critic Pattern

**Discovery:** ps-critic agent implements a complete generator-critic loop framework.

**Circuit Breaker Parameters:**

```yaml
circuit_breaker:
  max_iterations: 3
  improvement_threshold: 0.10  # 10% improvement required
  acceptance_threshold: 0.85   # Score to accept without revision
  consecutive_no_improvement_limit: 2
```

**Decision Logic (MAIN CONTEXT orchestrator):**

```
IF quality_score >= acceptance_threshold:
    → ACCEPT (threshold met)
ELIF iteration >= max_iterations:
    → ACCEPT_WITH_CAVEATS or ESCALATE_TO_USER
ELIF (current_score - previous_score) < improvement_threshold AND consecutive_no_improvement >= 2:
    → ACCEPT_WITH_CAVEATS (no further improvement likely)
ELSE:
    → REVISE (send feedback to generator)
```

**Strategic Value:**
- Prevents infinite refinement loops
- Balances quality vs. compute cost
- Provides escape hatch for diminishing returns

**Prior Art:**
- [Madaan et al. (2023) Self-Refine](https://arxiv.org/abs/2303.17651)
- OpenAI Agent Guide - Reflective Loops
- Anthropic Constitutional AI

### 5. Cross-Skill Integration

#### 5.1 Handoff Matrix

**Discovered Cross-Skill Handoffs:**

```
+---------------+                   +------------------+
| ps-architect  |------------------>| nse-architecture |
| (decisions)   |  design handoff   | (trade studies)  |
+---------------+                   +------------------+

+---------------+                   +------------------+
| ps-analyst    |------------------>| nse-risk         |
| (root cause)  |  risk handoff     | (mitigation)     |
+---------------+                   +------------------+

+-----------------+                 +---------------+
| nse-requirements|---------------->| ps-architect  |
| (shall stmts)   | decision need   | (ADR)         |
+-----------------+                 +---------------+
```

**Implication:** Skills are designed to interoperate. The common session context schema enables seamless handoffs.

#### 5.2 Pipeline Alias Configuration

**orchestration Skill Innovation:**

```yaml
pipelines:
  pipeline_a:
    short_alias: "ps"                    # Used in artifact paths
    skill_source: "problem-solving"       # Originating skill

  pipeline_b:
    short_alias: "nse"
    skill_source: "nasa-systems-engineering"
```

**Alias Resolution Priority:**

| Priority | Source | Example |
|----------|--------|---------|
| 1 (Highest) | Workflow Override | User specifies "alpha" |
| 2 | Skill Default | Skill registers "ps" |
| 3 (Fallback) | Auto-Derived | Derived from skill name |

**Strategic Value:**
- Flexible artifact paths
- Human-readable directory structure
- No hardcoded pipeline names in templates

### 6. Template & Documentation Architecture

#### 6.1 Template Distribution

**Observed Template Counts:**

| Skill | Template Count | Types |
|-------|----------------|-------|
| problem-solving | 1 | critique |
| nasa-se | 5 | alternative-analysis, concept-exploration, qa-report, review-checklists, trade-study |
| orchestration | 3 | ORCHESTRATION.yaml, ORCHESTRATION_PLAN.md, ORCHESTRATION_WORKTRACKER.md |

**Pattern:** Template count correlates with artifact type diversity:
- **problem-solving:** Focused on research/analysis artifacts (shared templates in docs/knowledge/exemplars/templates/)
- **nasa-se:** Diverse SE work products (requirements, V&V, risk, reviews)
- **orchestration:** Workflow-specific artifacts (plan, tracker, state)

#### 6.2 PLAYBOOK.md as Comprehensive Guide

**Key Finding:** orchestration PLAYBOOK.md (3.1.0) is the most comprehensive guide observed:

- **Triple-Lens Structure:** L0/L1/L2 throughout
- **Anti-Pattern Catalog:** 4 documented anti-patterns with ASCII diagrams
- **Constraints & Boundaries:** Hard vs. Soft constraints table
- **Invariants Checklist:** 5 invariants that must always be true
- **Design Rationale:** ADR-style decision documentation

**Strategic Implication:** PLAYBOOK.md should be the gold standard for all skills. problem-solving and nasa-se skills would benefit from similar comprehensive playbooks.

### 7. Risk Assessment & Mitigation

#### 7.1 Identified Risks

| Risk | Impact | Likelihood | Mitigation |
|------|--------|------------|------------|
| **Context Rot** | High | High | P-002 (File Persistence), checkpointing |
| **Recursive Spawning** | High | Medium | P-003 (Hard constraint), agent validation |
| **State Amnesia** | Medium | Medium | Session context schema, ORCHESTRATION.yaml |
| **Barrier Bypass** | Medium | Low | Execution queue enforcement |
| **Quality Degradation** | Medium | Medium | ps-critic circuit breaker |

#### 7.2 Architectural Safeguards

**Defense in Depth:**

1. **Constitutional Layer:** Hard constraints (P-003, P-022, P-043)
2. **Validation Layer:** Input/output validation
3. **Quality Layer:** ps-critic iterative refinement
4. **State Layer:** Persistent checkpoints
5. **Documentation Layer:** Anti-pattern catalog

### 8. Future Evolution Opportunities

#### 8.1 Potential Skill Enhancements

**Based on Pattern Analysis:**

1. **problem-solving Enhancements:**
   - Add comprehensive PLAYBOOK.md (similar to orchestration)
   - Create templates for all agent outputs (not just critique)
   - Document cross-skill handoff patterns

2. **nasa-se Enhancements:**
   - Add orchestration-style PLAYBOOK.md with anti-patterns
   - Expand template coverage (currently missing some agent types)
   - Document NASA process flow diagrams

3. **orchestration Enhancements:**
   - Add RUNBOOK.md for operational procedures
   - Create templates for barrier artifacts
   - Document failure recovery procedures

#### 8.2 Skill Composition Patterns

**Discovery:** Skills are designed to compose:

```
Cross-Pollinated Workflow:
  Pipeline A: problem-solving (divergent exploration)
  Pipeline B: nasa-se (convergent requirements)
  Barriers: Knowledge exchange at phase boundaries
  Synthesis: Combined deliverable
```

**Opportunity:** Document canonical skill composition patterns:
- **ps + nse:** Research-driven requirements engineering
- **ps + orch:** Complex multi-phase problem-solving
- **nse + orch:** Large-scale systems engineering programs

---

## References

### Skill Artifacts

1. [problem-solving SKILL.md](../../../skills/problem-solving/SKILL.md) - v2.1.0
2. [nasa-se SKILL.md](../../../skills/nasa-se/SKILL.md) - v1.1.0
3. [orchestration SKILL.md](../../../skills/orchestration/SKILL.md) - v2.1.0
4. [orchestration PLAYBOOK.md](../../../skills/orchestration/PLAYBOOK.md) - v3.1.0

### Agent Definitions

1. [ps-researcher.md](../../../skills/problem-solving/agents/ps-researcher.md) - v2.2.0
2. [ps-critic.md](../../../skills/problem-solving/agents/ps-critic.md) - v2.2.0
3. [nse-requirements.md](../../../skills/nasa-se/agents/nse-requirements.md) - v2.2.0

### Prior Art

1. Anthropic. (2025). *Claude 4 Best Practices*. https://docs.claude.com/en/docs/build-with-claude/prompt-engineering/claude-4-best-practices
2. OpenAI. (2024). *A Practical Guide to Building Agents*. https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf
3. Google. (2025). *Developer's Guide to Multi-Agent Patterns in ADK*. https://developers.googleblog.com/developers-guide-to-multi-agent-patterns-in-adk/
4. Madaan, A. et al. (2023). *Self-Refine: Iterative Refinement with Self-Feedback*. arXiv:2303.17651
5. Microsoft. (2025). *AI Agent Orchestration Patterns*. https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/ai-agent-design-patterns
6. Anthropic. (2023). *Constitutional AI: Harmlessness from AI Feedback*. https://www.anthropic.com/research/constitutional-ai-harmlessness-from-ai-feedback

---

*Research Artifact: work-026-e-001*
*Agent: ps-researcher v2.2.0*
*Date: 2026-01-30*
*Confidence: 0.95 (High - based on direct analysis of authoritative skill files)*
*Constitutional Compliance: P-001, P-002, P-004, P-011, P-022*
