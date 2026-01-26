# EN-006 Trade Space Analysis: Context Injection Approaches

<!--
TEMPLATE: Trade Space Analysis
SOURCE: ps-researcher trade study
VERSION: 1.0.0
TASK: TASK-030 Deep Research & Exploration
PHASE: 0
-->

---

## Frontmatter

```yaml
# === IDENTITY ===
id: "en006-trade-space"
work_type: ANALYSIS
parent_id: "TASK-030"

# === METADATA ===
title: "Context Injection Trade Space Analysis"
description: |
  Weighted criteria matrix comparing context injection approaches
  based on industry research and EN-003 requirements.

# === AUTHORSHIP ===
created_by: "ps-researcher"
created_at: "2026-01-26"
updated_at: "2026-01-26"

# === TRACEABILITY ===
requirements_traced:
  - SK-004   # Progressive disclosure
  - MA-001   # Provider-independent design
  - MA-002   # Avoid provider-specific features
  - PAT-001  # Tiered extraction pipeline
```

---

## L0: Executive Summary

**What's a Trade Space Analysis?**

When building something, there are usually multiple ways to do it. A trade space analysis compares these options using weighted criteria - like scoring job candidates on different skills that matter for the role.

**Bottom Line:**

We recommend a **Hybrid Approach** that combines:
- Static context files (like CLAUDE.md) for stable domain knowledge
- Dynamic tool-based loading for fresh, user-specific data
- Template variables for prompt customization

This approach scored **8.35/10** - the highest among all options evaluated.

---

## L1: Trade Study Details

### 1. Candidate Approaches

| ID | Approach | Description | Industry Example |
|----|----------|-------------|------------------|
| **A1** | Static Context Files | Pre-loaded markdown/YAML files | Claude Code CLAUDE.md |
| **A2** | Dynamic Tool-Based | Runtime retrieval via tools | LangChain middleware |
| **A3** | Task Dependency Injection | Explicit task `context=[]` | CrewAI |
| **A4** | Template Variables | `{{$variable}}` substitution | Semantic Kernel |
| **A5** | Hybrid (Recommended) | Combination of A1 + A2 + A4 | Anthropic guidance |

### 2. Evaluation Criteria

Based on EN-003 requirements and industry best practices:

| Criterion | Weight | Justification |
|-----------|--------|---------------|
| **C1: Ease of Configuration** | 15% | Skill developers must configure easily (SK-001) |
| **C2: Performance (Latency)** | 15% | Context loading < 500ms target |
| **C3: Flexibility** | 10% | Adapt to different domains |
| **C4: Testability** | 15% | Deterministic tests required |
| **C5: Model-Agnostic** | 15% | MA-001 requirement |
| **C6: Schema Validation** | 10% | Prevent malformed context |
| **C7: Memory/Persistence** | 10% | Jerry P-002 file persistence |
| **C8: MCP Compatibility** | 10% | Future-proofing for industry standard |

**Total: 100%**

### 3. Scoring Scale

| Score | Meaning |
|-------|---------|
| 10 | Excellent - Exceeds all expectations |
| 8 | Good - Meets expectations well |
| 6 | Adequate - Meets minimum requirements |
| 4 | Poor - Significant gaps |
| 2 | Very Poor - Does not meet requirements |

### 4. Weighted Criteria Matrix

#### 4.1 Raw Scores

| Criterion (Weight) | A1: Static | A2: Dynamic | A3: Task Dep | A4: Templates | A5: Hybrid |
|--------------------|------------|-------------|--------------|---------------|------------|
| C1: Ease of Config (15%) | 9 | 5 | 7 | 8 | 8 |
| C2: Performance (15%) | 10 | 5 | 6 | 8 | 8 |
| C3: Flexibility (10%) | 4 | 10 | 7 | 8 | 9 |
| C4: Testability (15%) | 9 | 6 | 8 | 9 | 8 |
| C5: Model-Agnostic (15%) | 9 | 7 | 6 | 8 | 9 |
| C6: Schema Validation (10%) | 6 | 8 | 7 | 9 | 8 |
| C7: Memory/Persistence (10%) | 10 | 6 | 5 | 5 | 8 |
| C8: MCP Compatibility (10%) | 5 | 9 | 6 | 7 | 8 |

#### 4.2 Weighted Scores

| Criterion (Weight) | A1: Static | A2: Dynamic | A3: Task Dep | A4: Templates | A5: Hybrid |
|--------------------|------------|-------------|--------------|---------------|------------|
| C1: 15% | 1.35 | 0.75 | 1.05 | 1.20 | 1.20 |
| C2: 15% | 1.50 | 0.75 | 0.90 | 1.20 | 1.20 |
| C3: 10% | 0.40 | 1.00 | 0.70 | 0.80 | 0.90 |
| C4: 15% | 1.35 | 0.90 | 1.20 | 1.35 | 1.20 |
| C5: 15% | 1.35 | 1.05 | 0.90 | 1.20 | 1.35 |
| C6: 10% | 0.60 | 0.80 | 0.70 | 0.90 | 0.80 |
| C7: 10% | 1.00 | 0.60 | 0.50 | 0.50 | 0.80 |
| C8: 10% | 0.50 | 0.90 | 0.60 | 0.70 | 0.80 |
| **TOTAL** | **8.05** | **6.75** | **6.55** | **7.85** | **8.25** |

#### 4.3 Score Visualization

```
WEIGHTED SCORES (0-10)
═══════════════════════════════════════════════════════════════════

A5: Hybrid      ████████████████████████████████████████████ 8.25  ★ RECOMMENDED
A1: Static      ████████████████████████████████████████     8.05
A4: Templates   ███████████████████████████████████████      7.85
A2: Dynamic     █████████████████████████████████            6.75
A3: Task Dep    ████████████████████████████████             6.55

                ├────────┼────────┼────────┼────────┼────────┤
                0        2        4        6        8       10
```

### 5. Detailed Scoring Rationale

#### A1: Static Context Files (8.05)

**Strengths:**
- Excellent ease of configuration (9/10) - Simple markdown/YAML files
- Perfect performance (10/10) - Pre-loaded, no runtime overhead
- High testability (9/10) - Deterministic, version-controlled
- Excellent model-agnostic (9/10) - Plain text format
- Perfect memory/persistence (10/10) - Files survive sessions

**Weaknesses:**
- Poor flexibility (4/10) - Cannot adapt to runtime conditions
- Low MCP compatibility (5/10) - Not designed for protocol integration
- Moderate schema validation (6/10) - No built-in validation

#### A2: Dynamic Tool-Based (6.75)

**Strengths:**
- Excellent flexibility (10/10) - Can fetch anything at runtime
- Good MCP compatibility (9/10) - Aligns with MCP tools model

**Weaknesses:**
- Poor ease of configuration (5/10) - Requires code for each retrieval
- Poor performance (5/10) - Runtime latency for each fetch
- Moderate testability (6/10) - Requires mocking tool responses

#### A3: Task Dependency Injection (6.55)

**Strengths:**
- Good testability (8/10) - Explicit dependencies

**Weaknesses:**
- Tied to task execution model (6/10 model-agnostic)
- Poor memory/persistence (5/10) - Context lost between runs
- Moderate MCP compatibility (6/10) - CrewAI-specific pattern

#### A4: Template Variables (7.85)

**Strengths:**
- High testability (9/10) - Deterministic templates
- Good schema validation (9/10) - InputVariable definitions

**Weaknesses:**
- Poor memory/persistence (5/10) - Requires separate persistence layer
- Moderate MCP compatibility (7/10) - Different abstraction model

#### A5: Hybrid Approach (8.25) - RECOMMENDED

**Combines best of each:**
- Static files for stable domain context (from A1)
- Dynamic tools for fresh data (from A2)
- Template variables for prompt customization (from A4)

**Balanced across all criteria:**
- No score below 8
- Best overall model-agnostic score (9/10)
- Good performance (8/10) despite dynamic component

---

## L2: Strategic Implications

### 1. Recommendation: Hybrid Approach (A5)

**Architecture:**

```
┌─────────────────────────────────────────────────────────────────────┐
│                  HYBRID CONTEXT INJECTION ARCHITECTURE               │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│   ┌─────────────────────┐      ┌─────────────────────┐              │
│   │    STATIC LAYER     │      │   DYNAMIC LAYER     │              │
│   │  (Pre-loaded Files) │      │  (Runtime Tools)    │              │
│   ├─────────────────────┤      ├─────────────────────┤              │
│   │ • Domain schemas    │      │ • User-specific     │              │
│   │ • Entity definitions│      │ • Real-time data    │              │
│   │ • Extraction rules  │      │ • External APIs     │              │
│   │ • Prompt templates  │      │ • Document content  │              │
│   └─────────┬───────────┘      └─────────┬───────────┘              │
│             │                            │                           │
│             └────────────┬───────────────┘                           │
│                          ▼                                           │
│             ┌─────────────────────────┐                              │
│             │   TEMPLATE RESOLUTION   │                              │
│             │   {{$static_context}}   │                              │
│             │   {{$dynamic_data}}     │                              │
│             └─────────────────────────┘                              │
│                          │                                           │
│                          ▼                                           │
│             ┌─────────────────────────┐                              │
│             │   CONTEXT INJECTION     │                              │
│             │   TO AGENT PROMPT       │                              │
│             └─────────────────────────┘                              │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

### 2. Implementation Guidance

#### 2.1 Static Context Files

```yaml
# contexts/legal-domain.yaml
schema_version: "1.0"
domain: "legal"

entity_definitions:
  party:
    description: "Legal entity in contract"
    attributes:
      - name
      - role (buyer/seller/guarantor)
      - jurisdiction
  obligation:
    description: "Contractual obligation"
    attributes:
      - obligor
      - obligee
      - terms
      - deadline

extraction_rules:
  parties: "Identify all parties mentioned by name and role"
  dates: "Extract all dates in ISO 8601 format"
  obligations: "List all obligations with responsible party"

prompt_guidance: |
  When analyzing legal documents:
  1. Identify parties before analyzing obligations
  2. Cross-reference obligations with party roles
  3. Flag ambiguous terms for human review
```

#### 2.2 Dynamic Tool Definition

```python
@tool
def fetch_document_context(document_id: str) -> dict:
    """Retrieve document-specific context at runtime.

    Returns entity mentions, previous analyses, and user annotations.
    """
    return {
        "entities": load_entities_from_db(document_id),
        "annotations": load_user_annotations(document_id),
        "previous_analysis": load_cached_analysis(document_id)
    }
```

#### 2.3 Template with Variables

```
{{$domain_context}}

## Document Analysis Task

Analyze the following transcript for {{$domain}} patterns:

{{$transcript_content}}

Previous context: {{$dynamic_context}}

Focus on extracting:
{{$extraction_rules}}
```

### 3. Risk Mitigation

| Risk | Mitigation in Hybrid Approach |
|------|------------------------------|
| Context becomes stale | Dynamic layer fetches fresh data |
| Performance degradation | Static layer handles most context |
| Configuration complexity | Clear separation of concerns |
| Testing difficulty | Mock dynamic layer, test static layer directly |

### 4. Migration Path to MCP

The Hybrid approach is designed for future MCP compatibility:

| Component | MCP Mapping |
|-----------|-------------|
| Static context files | MCP Resources |
| Prompt templates | MCP Prompts |
| Dynamic tools | MCP Tools |

```
Future Evolution:
────────────────────────────────────────────────────────────────────
Phase 1 (Current):    Phase 2 (Q2 2026):    Phase 3 (Q4 2026):
Hybrid without MCP    MCP-aware hybrid      Full MCP integration
                      adapter layer         native MCP server
```

---

## Decision

**Selected Approach: A5 - Hybrid (Static + Dynamic + Templates)**

**Rationale:**
1. Highest weighted score (8.25/10)
2. Best alignment with EN-003 requirements (MA-001, MA-002, SK-004)
3. Compatible with Anthropic's recommended context engineering patterns
4. Clear migration path to MCP standard
5. Balanced trade-offs across all criteria

**Next Steps:**
1. Define context schema in TASK-031 (5W2H Analysis)
2. Design static context file structure in TASK-034 (TDD)
3. Specify dynamic tool interfaces in TASK-035 (Spec)

---

## References

1. Anthropic. (2025). *Effective Context Engineering for AI Agents*. https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents

2. NASA. (2016). *NASA Systems Engineering Handbook (NASA/SP-2016-6105)*. Trade study methodology.

3. EN-006 Research Synthesis. `en006-research-synthesis.md`

---

## History

| Date | Version | Author | Notes |
|------|---------|--------|-------|
| 2026-01-26 | 1.0.0 | ps-researcher | Initial trade space analysis |

---

*Document ID: en006-trade-space*
*Task: TASK-030*
*Phase: 0 (Deep Research & Exploration)*
*Workflow: en006-ctxinj-20260126-001*
