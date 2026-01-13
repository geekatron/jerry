# WI-SAO-052: Agent Enhancement Evaluation Rubric

**Document ID:** WI-SAO-052-RUBRIC
**Date:** 2026-01-12
**Status:** COMPLETE
**Pattern:** Review Gate (Pattern 7) - Gate Criteria Definition

---

## Executive Summary

This rubric defines the evaluation criteria for the Generator-Critic enhancement loop in Phase 3. All agents must achieve a weighted score ≥0.85 to pass the enhancement gate.

**Key Parameters:**
- **8 Evaluation Dimensions** covering context engineering, persona, orchestration, and documentation
- **Acceptance Threshold:** 0.85 (per Anthropic circuit breaker standard)
- **Max Iterations:** 3 (circuit breaker to prevent infinite loops)
- **Escalation:** Human review if threshold not met after 3 iterations

---

## 1. Rubric Dimensions

### 1.1 Dimension Overview

| ID | Dimension | Weight | Source Standard |
|----|-----------|--------|-----------------|
| D-001 | YAML Frontmatter | 10% | Anthropic ANT-001 |
| D-002 | Role-Goal-Backstory | 15% | Anthropic ANT-002 |
| D-003 | Guardrails | 15% | Anthropic ANT-003 |
| D-004 | Tool Descriptions | 10% | Anthropic ANT-004 |
| D-005 | Session Context | 15% | Jerry session_context v1.0.0 |
| D-006 | L0/L1/L2 Coverage | 15% | Jerry Triple-Lens |
| D-007 | Constitutional Compliance | 10% | Jerry Constitution P-002, P-003, P-022 |
| D-008 | Domain-Specific | 10% | NASA SE / Family-specific |

**Total Weight:** 100%

### 1.2 Dimension Details

#### D-001: YAML Frontmatter (10%)

**What it measures:** Structured metadata in YAML frontmatter block.

| Score | Criteria |
|-------|----------|
| 0.0-0.2 | No frontmatter present |
| 0.3-0.4 | Basic frontmatter (name, version only) |
| 0.5-0.6 | Includes identity section |
| 0.7-0.8 | Includes identity, capabilities, output sections |
| 0.9-1.0 | Complete frontmatter with all sections: identity, persona, capabilities, guardrails, output, validation, session_context |

**Required Fields:**
- `name`, `version`, `description`
- `model` (opus/sonnet/haiku)
- `identity` (role, expertise, cognitive_mode)
- `capabilities` (allowed_tools, forbidden_actions)

---

#### D-002: Role-Goal-Backstory (15%)

**What it measures:** Clear persona definition per Anthropic best practices.

| Score | Criteria |
|-------|----------|
| 0.0-0.2 | No persona/identity section |
| 0.3-0.4 | Basic role statement only |
| 0.5-0.6 | Role + expertise listed |
| 0.7-0.8 | Full identity block with role, expertise, cognitive_mode |
| 0.9-1.0 | Complete persona with identity, tone, communication style, audience adaptation |

**Required Elements:**
- **Role:** One-line identity (e.g., "Research Specialist")
- **Expertise:** 3-5 areas of specialization
- **Cognitive Mode:** divergent or convergent
- **Tone:** professional, casual, technical
- **Communication Style:** consultative, direct, narrative

**Example (0.9 score):**
```yaml
identity:
  role: "Research Specialist"
  expertise:
    - "Literature review and synthesis"
    - "Web research and source validation"
    - "Library documentation research"
  cognitive_mode: "divergent"

persona:
  tone: "professional"
  communication_style: "consultative"
  audience_level: "adaptive"
```

---

#### D-003: Guardrails (15%)

**What it measures:** Input validation, output filtering, and fallback behavior.

| Score | Criteria |
|-------|----------|
| 0.0-0.2 | No guardrails section |
| 0.3-0.4 | Basic constraints mentioned in text |
| 0.5-0.6 | Structured guardrails section with input validation |
| 0.7-0.8 | Input validation + output filtering documented |
| 0.9-1.0 | Complete guardrails with input validation, output filtering, fallback behavior, and error handling |

**Required Elements:**
- **Input Validation:** Regex patterns for IDs, format checks
- **Output Filtering:** No secrets, mandatory fields
- **Fallback Behavior:** What to do when blocked
- **Error Handling:** Explicit failure modes

**Example (0.9 score):**
```yaml
guardrails:
  input_validation:
    project_id:
      format: "^PROJ-\\d{3}$"
      on_invalid: reject
    entry_id:
      format: "^e-\\d+$"
  output_filtering:
    - no_secrets_in_output
    - all_claims_must_have_citations
  fallback_behavior: warn_and_retry
```

---

#### D-004: Tool Descriptions (10%)

**What it measures:** Quality of tool documentation and usage examples.

| Score | Criteria |
|-------|----------|
| 0.0-0.2 | No tool documentation |
| 0.3-0.4 | Tool list only |
| 0.5-0.6 | Tool list with purpose |
| 0.7-0.8 | Tool table with purpose and usage pattern |
| 0.9-1.0 | Complete tool documentation with table + 2-3 concrete examples |

**Required Elements:**
- **Tool Table:** Tool name, purpose, usage pattern
- **Examples:** 2-3 concrete invocation examples
- **Forbidden Actions:** Explicit list of prohibited tool uses

**Example (0.9 score):**
```markdown
| Tool | Purpose | Usage Pattern |
|------|---------|---------------|
| Read | Read files | Reading source docs |
| Write | Create files | **MANDATORY** for output |
| WebSearch | Search web | Finding industry sources |

**Examples:**
1. To find existing research: `Read("docs/research/")`
2. To create output: `Write("docs/research/topic.md", content)`
```

---

#### D-005: Session Context (15%)

**What it measures:** Multi-agent handoff support per session_context schema v1.0.0.

| Score | Criteria |
|-------|----------|
| 0.0-0.2 | No session context support |
| 0.3-0.4 | state_output_key defined |
| 0.5-0.6 | state_output_key + next_agent_hint |
| 0.7-0.8 | Session context section with schema reference |
| 0.9-1.0 | Complete session_context with input validation, output validation, on_receive, on_send handlers |

**Required Elements:**
- **state_output_key:** Standard key name (e.g., `researcher_output`)
- **schema_version:** "1.0.0"
- **On Receive:** Validation actions for incoming context
- **On Send:** Output structure with key_findings, confidence, artifacts, timestamp

**Example (0.9 score):**
```yaml
session_context:
  schema: "docs/schemas/session_context.json"
  schema_version: "1.0.0"
  input_validation: true
  output_validation: true
  on_receive:
    - validate_session_id
    - check_schema_version
    - extract_key_findings
  on_send:
    - populate_key_findings
    - calculate_confidence
    - list_artifacts
    - set_timestamp
```

---

#### D-006: L0/L1/L2 Coverage (15%)

**What it measures:** Triple-lens output level support.

| Score | Criteria |
|-------|----------|
| 0.0-0.2 | No mention of output levels |
| 0.3-0.4 | One level mentioned |
| 0.5-0.6 | L0 and L1 defined |
| 0.7-0.8 | All three levels defined with descriptions |
| 0.9-1.0 | Complete L0/L1/L2 with descriptions, examples, and output templates |

**Required Elements:**
- **L0 (ELI5):** Metaphors, WHAT/WHY (50-100 words)
- **L1 (Engineer):** Commands, HOW (200-400 words)
- **L2 (Architect):** Anti-patterns, CONSTRAINTS (300-500 words)
- **Output Template:** Structured template showing all levels

**Example (0.9 score):**
```markdown
### L0: Executive Summary (ELI5)
*2-3 paragraphs for non-technical stakeholders.*
Answer: "What does this mean for the project?"

### L1: Technical Analysis (Software Engineer)
*Implementation-focused content with specifics.*
- Code snippets and configuration examples
- Step-by-step guidance

### L2: Architectural Implications (Principal Architect)
*Strategic perspective with trade-offs.*
- Alternative approaches considered
- Risk assessment
- Anti-patterns to avoid
```

---

#### D-007: Constitutional Compliance (10%)

**What it measures:** Adherence to Jerry Constitution principles.

| Score | Criteria |
|-------|----------|
| 0.0-0.2 | No constitutional reference |
| 0.3-0.4 | Constitution mentioned in text |
| 0.5-0.6 | Principles listed (P-002, P-003, P-022) |
| 0.7-0.8 | Compliance table with agent behavior mapping |
| 0.9-1.0 | Complete constitutional_compliance section with self-critique checklist |

**Required Principles:**
- **P-002:** File Persistence (Medium enforcement)
- **P-003:** No Recursive Subagents (Hard enforcement)
- **P-022:** No Deception (Hard enforcement)

**Example (0.9 score):**
```markdown
## Constitutional Compliance

| Principle | Enforcement | Agent Behavior |
|-----------|-------------|----------------|
| P-002 | Medium | ALL outputs persisted to docs/ |
| P-003 | **Hard** | Task tool spawns single-level only |
| P-022 | **Hard** | Transparent about limitations |

**Self-Critique Checklist:**
- [ ] P-002: Will output be persisted?
- [ ] P-003: No recursive agent spawning?
- [ ] P-022: Am I being transparent?
```

---

#### D-008: Domain-Specific (10%)

**What it measures:** Family-specific standards compliance.

| Family | Criteria |
|--------|----------|
| **ps-*** | Problem-solving methodology, 5W1H framework |
| **nse-*** | NASA SE alignment (NPR 7123.1), review gates, ADIT |
| **orch-*** | Orchestration patterns, workflow diagrams, state schemas |
| **core** | Delegation protocol, specialist registry |

| Score | Criteria |
|-------|----------|
| 0.0-0.2 | No domain-specific content |
| 0.3-0.4 | Basic domain mention |
| 0.5-0.6 | Domain methodology referenced |
| 0.7-0.8 | Domain methodology documented with guidance |
| 0.9-1.0 | Complete domain section with templates, examples, and domain-specific guardrails |

---

## 2. Scoring Scale

### 2.1 Per-Dimension Scoring

| Score Range | Label | Description |
|-------------|-------|-------------|
| 0.00-0.19 | Absent | Missing or severely deficient |
| 0.20-0.39 | Minimal | Present but largely incomplete |
| 0.40-0.59 | Partial | Adequate foundation, significant gaps |
| 0.60-0.79 | Adequate | Good quality, minor gaps |
| 0.80-0.89 | Good | Meets standards, minor improvements possible |
| 0.90-1.00 | Excellent | Exemplary, reference quality |

### 2.2 Weighted Score Calculation

```
weighted_score = Σ(dimension_score × weight) / Σ(weights)

weighted_score = (D001 × 0.10) + (D002 × 0.15) + (D003 × 0.15) +
                 (D004 × 0.10) + (D005 × 0.15) + (D006 × 0.15) +
                 (D007 × 0.10) + (D008 × 0.10)
```

### 2.3 Acceptance Criteria

| Weighted Score | Decision | Action |
|----------------|----------|--------|
| ≥0.85 | **ACCEPT** | Enhancement complete |
| 0.70-0.84 | **ITERATE** | Rerun Generator-Critic |
| <0.70 | **ESCALATE** | Human review required |

**Circuit Breaker:**
- Maximum iterations: 3
- If <0.85 after 3 iterations: Escalate to human review

---

## 3. Baseline Scores

### 3.1 ps-researcher.md (Exemplar)

| Dimension | Score | Justification |
|-----------|-------|---------------|
| D-001 YAML Frontmatter | 0.95 | Complete frontmatter with all sections |
| D-002 Role-Goal-Backstory | 0.90 | Full identity and persona blocks |
| D-003 Guardrails | 0.85 | Input/output validation present |
| D-004 Tool Descriptions | 0.75 | Table present, few examples |
| D-005 Session Context | 0.90 | Complete session_context section |
| D-006 L0/L1/L2 Coverage | 0.90 | All levels with descriptions |
| D-007 Constitutional | 0.90 | Compliance table + self-critique |
| D-008 Domain-Specific | 0.85 | 5W1H framework documented |

**Weighted Score:** 0.875 ✅ **PASS**

### 3.2 nse-requirements.md (Exemplar)

| Dimension | Score | Justification |
|-----------|-------|---------------|
| D-001 YAML Frontmatter | 0.95 | Complete frontmatter |
| D-002 Role-Goal-Backstory | 0.90 | Full persona with NASA context |
| D-003 Guardrails | 0.90 | Extensive input validation |
| D-004 Tool Descriptions | 0.70 | Table present, needs examples |
| D-005 Session Context | 0.90 | Complete validation section |
| D-006 L0/L1/L2 Coverage | 0.90 | All levels with templates |
| D-007 Constitutional | 0.90 | P-040, P-041, P-043 added |
| D-008 Domain-Specific | 0.95 | NASA methodology, ADIT, traces |

**Weighted Score:** 0.888 ✅ **PASS**

### 3.3 orchestrator.md (Needs Enhancement)

| Dimension | Score | Justification |
|-----------|-------|---------------|
| D-001 YAML Frontmatter | 0.00 | No frontmatter |
| D-002 Role-Goal-Backstory | 0.65 | Persona present but unstructured |
| D-003 Guardrails | 0.30 | Constraints section only |
| D-004 Tool Descriptions | 0.40 | Specialist table, no tool table |
| D-005 Session Context | 0.20 | Handoff protocol but no schema |
| D-006 L0/L1/L2 Coverage | 0.00 | No L0/L1/L2 sections |
| D-007 Constitutional | 0.35 | Constraints mention but no compliance section |
| D-008 Domain-Specific | 0.50 | Delegation protocol present |

**Weighted Score:** 0.285 ❌ **NEEDS ENHANCEMENT**

---

## 4. Rubric Validation

### 4.1 Discrimination Power

| Agent | Baseline Score | Quality Tier | Validated? |
|-------|----------------|--------------|------------|
| ps-researcher.md | 0.875 | Exemplar | ✅ High quality correctly identified |
| nse-requirements.md | 0.888 | Exemplar | ✅ High quality correctly identified |
| orchestrator.md | 0.285 | Needs Work | ✅ Low quality correctly identified |

**Score Spread:** 0.603 (0.888 - 0.285)
**Discrimination:** ✅ Rubric effectively differentiates quality levels

### 4.2 Threshold Validation

At 0.85 threshold:
- Exemplar agents (ps-researcher, nse-requirements) pass
- Deficient agents (orchestrator) fail
- Partial agents require iteration

**Threshold Verdict:** ✅ 0.85 is appropriate

---

## 5. Scoring Template

### 5.1 Agent Evaluation Form

```markdown
# Agent Evaluation: {agent_name}

**Evaluator:** {evaluator}
**Date:** {date}
**Iteration:** {1|2|3}

## Dimension Scores

| ID | Dimension | Weight | Score | Weighted |
|----|-----------|--------|-------|----------|
| D-001 | YAML Frontmatter | 10% | {0.0-1.0} | {score×0.10} |
| D-002 | Role-Goal-Backstory | 15% | {0.0-1.0} | {score×0.15} |
| D-003 | Guardrails | 15% | {0.0-1.0} | {score×0.15} |
| D-004 | Tool Descriptions | 10% | {0.0-1.0} | {score×0.10} |
| D-005 | Session Context | 15% | {0.0-1.0} | {score×0.15} |
| D-006 | L0/L1/L2 Coverage | 15% | {0.0-1.0} | {score×0.15} |
| D-007 | Constitutional | 10% | {0.0-1.0} | {score×0.10} |
| D-008 | Domain-Specific | 10% | {0.0-1.0} | {score×0.10} |

**WEIGHTED TOTAL:** {sum}

## Decision

- [ ] ACCEPT (≥0.85)
- [ ] ITERATE (<0.85, iteration <3)
- [ ] ESCALATE (<0.70 or iteration=3)

## Justification

{Brief explanation of scores and decision}

## Improvement Areas (if iterating)

1. {Specific improvement needed}
2. {Specific improvement needed}
```

---

## 6. Generator-Critic Loop Integration

### 6.1 Enhancement Workflow

```
┌─────────────────────────────────────────────────────────────────┐
│               GENERATOR-CRITIC ENHANCEMENT LOOP                   │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│   ┌──────────────┐                                              │
│   │  Generator   │ ◄─────────────────────────┐                  │
│   │  (Enhance    │                           │                  │
│   │   Agent)     │                           │                  │
│   └──────┬───────┘                           │                  │
│          │                                   │                  │
│          ▼                                   │                  │
│   ┌──────────────┐                           │                  │
│   │   Critic     │                           │                  │
│   │  (Score      │                           │                  │
│   │   Agent)     │                           │                  │
│   └──────┬───────┘                           │                  │
│          │                                   │                  │
│          ▼                                   │                  │
│   ┌──────────────────────┐                   │                  │
│   │ weighted_score ≥0.85? │                  │                  │
│   └──────┬───────────────┘                   │                  │
│          │                                   │                  │
│          ├─── YES ─► ACCEPT ─► Next Agent    │                  │
│          │                                   │                  │
│          └─── NO ──┬─► iteration < 3? ──YES──┘                  │
│                    │                                            │
│                    └─► NO ──► ESCALATE (Human Review)           │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 6.2 Circuit Breaker Parameters

```yaml
circuit_breaker:
  max_iterations: 3
  quality_threshold: 0.85
  escalation_threshold: 0.70
  escalation_action: human_review
  improvement_minimum: 0.05  # Must improve by 5% each iteration
```

---

## 7. Evidence Summary

| Evidence ID | Description | Status |
|-------------|-------------|--------|
| E-052-001 | 8 dimensions defined | ✅ Complete |
| E-052-002 | Scoring guide created | ✅ Complete |
| E-052-003 | Baseline scores recorded | ✅ Complete |
| E-052-004 | Rubric discriminates quality | ✅ Validated |

---

## References

- WI-SAO-049: Research Synthesis (rubric framework preview)
- WI-SAO-050: Gap Analysis (identified dimensions)
- WI-SAO-051: Compliance Check (standard weighting)
- Anthropic context engineering best practices
- Jerry Constitution v1.0

---

*Rubric Complete: 2026-01-12*
*Ready for: Phase 3 Generator-Critic Enhancement*
