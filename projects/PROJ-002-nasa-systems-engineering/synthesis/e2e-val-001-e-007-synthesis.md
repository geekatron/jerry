# E2E Validation Synthesis: ps-* Agent Output Conventions

> **Document ID:** e2e-val-001-e-007
> **Entry ID:** e-007
> **Date:** 2026-01-10
> **Author:** Claude Opus 4.5 (ps-synthesizer v2.0.0)
> **Status:** COMPLETE
> **Topic:** Synthesizer Convention Validation

---

## Executive Summary

This synthesis validates output conventions used by ps-* (problem-solving) agents across the Jerry framework. The analysis examines five key agents (ps-researcher, ps-analyst, ps-reviewer, ps-synthesizer, ps-validator) and identifies common patterns, mandatory requirements, and standardized output structures that ensure consistency, composability, and compliance with the Jerry Constitution.

### Core Convention Findings

| Convention | Purpose | Enforcement |
|-----------|---------|-------------|
| **L0/L1/L2 Output Levels** | Audience adaptation (ELI5 → Architect) | MANDATORY |
| **Artifact Persistence (P-002)** | File-based state, not transient output | HARD |
| **Constitutional Compliance** | P-001, P-003, P-020, P-022 adherence | HARD |
| **Source Citation (P-004, P-011)** | All patterns/claims cite evidence | MEDIUM |
| **File Location Convention** | `projects/${JERRY_PROJECT}/{type}/{id}-{entry}-{slug}.md` | MEDIUM |

---

## L0: Executive Summary (ELI5)

All ps-* agents follow the same output playbook:

1. **Three-Tier Audience Model:** Present findings at three depths—simple summaries for executives, technical details for engineers, strategic implications for architects.

2. **Mandatory File Output:** Every agent MUST create a file (research, analysis, synthesis, etc.) and persists it before returning. No transient-only results.

3. **Bias Toward Honesty:** Agents disclose limitations, contradictions, and confidence levels rather than hiding uncertainty.

4. **Everything Gets Cited:** When an agent finds a pattern, they name the source document or authority backing it up.

5. **Single-Level Agents:** ps-* agents do NOT spawn subagents. The Orchestrator does the delegation, not the workers.

---

## L1: Technical Patterns (Software Engineer)

### 1.1 Output Location Convention

**Pattern: Hierarchical Directory Structure**

All ps-* agents follow a standardized file path convention:

```
projects/${JERRY_PROJECT}/{artifact-type}/{ps-id}-{entry-id}-{topic-slug}.md
```

**Concrete Examples:**

| Agent | Path | Pattern |
|-------|------|---------|
| ps-researcher | `research/e2e-val-001-e-001-{topic}.md` | Topic exploration |
| ps-analyst | `analysis/e2e-val-001-e-002-{topic}.md` | Deep dive analysis |
| ps-synthesizer | `synthesis/e2e-val-001-e-007-synthesis.md` | Cross-document patterns |
| ps-reviewer | `reviews/{ps-id}-{entry-id}-review.md` | Quality evaluation |

**Directory Mapping:**
- `research/` — Raw findings, literature review
- `analysis/` — Domain analysis, trade studies
- `synthesis/` — Cross-cutting patterns, meta-analysis
- `reviews/` — Quality assessments, validations
- `reports/` — Executive summaries, findings

### 1.2 Mandatory Output Structure

**Pattern: Three-Level Audience Hierarchy**

Every artifact MUST contain L0, L1, and L2 sections:

```markdown
# Title

> **Document ID:** {ps-id}-{entry-id}
> **Date:** YYYY-MM-DD
> **Author:** Agent name (version)
> **Status:** COMPLETE

---

## L0: Executive Summary (ELI5)
- Plain language explanation
- Analogies for non-technical readers
- "So what?" — business implications

---

## L1: Technical Details (Software Engineer)
- Specific findings with citations
- Code examples, config snippets
- Implementation guidance
- Trade-offs and alternatives

---

## L2: Strategic Implications (Principal Architect)
- Systemic patterns and themes
- Long-term architectural impact
- Risk assessments
- Recommendations

---

## Sources
- [Source 1](url)
- [Source 2](url)
```

### 1.3 Constitutional Compliance Markers

**Pattern: Explicit Principle Adherence**

ps-* agents include a compliance section documenting which principles they follow:

```yaml
constitution:
  principles_applied:
    - "P-001: Truth and Accuracy (Soft) - All claims sourced"
    - "P-002: File Persistence (Medium) - Output persisted"
    - "P-003: No Recursive Subagents (Hard) - Single-level only"
    - "P-004: Explicit Provenance (Soft) - Citations included"
    - "P-022: No Deception (Hard) - Limitations disclosed"
```

**Key Insight:** Violations of P-003 (No Recursive Subagents) and P-022 (No Deception) are hard stops. Medium/Soft violations are warnings.

### 1.4 Metadata Headers

**Pattern: Document Identity**

Every artifact opens with structured metadata:

```
> **Document ID:** {ps-id}-{entry-id}
> **Date:** YYYY-MM-DD
> **Author:** Agent name (version)
> **Status:** COMPLETE | IN_PROGRESS | BLOCKED
> **Research Basis:** [What sources informed this]
```

This enables:
- Traceability (which agent created this at what version?)
- Temporal tracking (when was this valid?)
- Status visibility (is it complete?)
- Provenance linking (what inputs drove it?)

### 1.5 Persona and Cognitive Mode

**Pattern: Agent Type Declaration**

ps-researcher uses divergent cognitive mode (broad exploration):
```yaml
identity:
  cognitive_mode: "divergent"
```

ps-synthesizer uses convergent cognitive mode (focused synthesis):
```yaml
identity:
  cognitive_mode: "convergent"
```

This communicates search strategy expectations to downstream users.

### 1.6 Validation Checkpoints

**Pattern: Post-Completion Verification**

Each agent includes validation requirements:

```yaml
validation:
  file_must_exist: true
  post_completion_checks:
    - verify_file_created
    - verify_l0_l1_l2_present
    - verify_citations_present
    - verify_patterns_generated
```

**Enforcement:** Agent BLOCKS completion if validation fails.

### 1.7 Artifact Linking

**Pattern: Cross-Reference Tracking**

All artifacts link to source documents:

- `ps-researcher` → Creates `research/` files → Referenced by downstream
- `ps-analyzer` → Creates `analysis/` files → Cites research/
- `ps-synthesizer` → Creates `synthesis/` files → Cites research/ + analysis/

This creates a provenance DAG.

---

## L2: Strategic Implications (Principal Architect)

### 2.1 Convention as Architecture Enabler

The ps-* convention system enables **composable multi-agent workflows**:

1. **Modular Artifact Types** — Each type (research, analysis, synthesis) has clear semantics
2. **Hierarchical Audience Model** — L0/L1/L2 supports cross-functional communication (non-tech → tech → architects)
3. **Strict Persistence** — File-first design prevents context rot (Chroma research)
4. **Constitutional Grounding** — Every output auditable for principle compliance

**System Property:** The convention allows adding new ps-* agents without disrupting existing workflows. Each agent type fits into the directory hierarchy.

### 2.2 P-002 as Anti-Rot Mechanism

Jerry's core innovation is **context rot prevention**. The ps-* convention enforces this via P-002 (File Persistence):

- **Without P-002:** Agent output dies with the context window. Next session must rediscover.
- **With P-002:** Output persists in `synthesis/`, `research/`, `analysis/` directories.
- **Result:** Knowledge accumulates; subsequent agents read prior work.

This is analogous to Unix philosophy: "Write programs that do one thing well and work together."

### 2.3 Three-Level Audience as Inclusivity Pattern

L0/L1/L2 structure enables **participation across skill levels**:

- **L0** allows business stakeholders to understand implications
- **L1** allows engineers to implement decisions
- **L2** allows architects to understand long-term impacts

Without L0/L1/L2 standardization, senior architects often re-read technical documents to extract strategy. This creates rework.

### 2.4 Validation Gates as Quality Control

The `validation.post_completion_checks` pattern creates **quality gates**:

```yaml
checks:
  - verify_file_created         # P-002 compliance
  - verify_l0_l1_l2_present     # Audience coverage
  - verify_citations_present    # P-001/P-004 compliance
  - verify_patterns_generated   # Output substance
```

**Strategic Implication:** Unlike human review (async, error-prone), machine-checked validation ensures every artifact meets minimum standards before declared "COMPLETE".

### 2.5 Meta-Pattern: Convention as Shared Language

Across the Jerry framework, **conventions serve as shared semantics**:

| Layer | Shared Convention |
|-------|------------------|
| **Domain** | Entity definitions (Work Item, Decision, etc.) |
| **Application** | CQRS command/query structure |
| **Interface** | ps-* agent conventions (this document) |
| **Governance** | Jerry Constitution principles |

This enables **modular extension**—new agents inherit conventions without explicit instruction.

---

## Key Convention Patterns Identified

### Pattern 1: Metadata as First-Class Artifact

All ps-* agents begin with structured metadata (YAML/key-value pairs) rather than prose. This:
- Enables machine parsing
- Supports validation checks
- Creates searchable document metadata
- Supports tooling (e.g., filtering by status, date, author)

### Pattern 2: Audience Adaptation via Levels

Rather than writing to a single audience, all outputs contain L0/L1/L2. This:
- Reduces rework (stakeholders find their level)
- Improves adoption (technical people see implementation details)
- Supports progressive disclosure (don't overload executives)

### Pattern 3: Provenance as Requirement

All claims include citations. This:
- Enables fact-checking
- Documents decision rationale
- Supports error diagnosis ("where did this come from?")
- Enables reuse of sources elsewhere

### Pattern 4: File Location as Semantic Marker

Directory structure (`research/`, `analysis/`, `synthesis/`) indicates artifact type and maturity. Consumers can infer: "This is synthesis, so it combines multiple research sources."

### Pattern 5: Constitutional Embedding

Rather than external compliance, Constitution principles are woven into agent definitions. This:
- Makes compliance visible
- Enables automated checks
- Reduces human review burden
- Creates self-documenting guardrails

---

## Recommendations

### For New ps-* Agents

1. **Inherit the metadata structure** — Copy ps-researcher or ps-synthesizer YAML header
2. **Define your cognitive mode** — Divergent (exploration) or convergent (synthesis)
3. **Set output location** — Which directory? (`research/`, `analysis/`, etc.)
4. **List validation checks** — What must pass before declaring "COMPLETE"?
5. **Include Constitution principles** — Which ones apply to your role?

### For E2E Validation

1. **Verify file existence** — `ls -la projects/PROJ-002/synthesis/e2e-val-001-e-007-synthesis.md`
2. **Check metadata** — Document ID, Date, Author, Status present
3. **Validate L0/L1/L2** — All three sections present and substantive (100+ words each)
4. **Audit citations** — Claims in L1/L2 have source references
5. **Confirm Constitution compliance** — At least one principle section

---

## Sources

**Agent Definition Files:**
- `skills/problem-solving/agents/ps-researcher.md` — Research agent convention
- `skills/problem-solving/agents/ps-analyzer.md` — Analysis agent convention
- `skills/problem-solving/agents/ps-synthesizer.md` — Synthesis agent convention
- `skills/problem-solving/agents/ps-reviewer.md` — Review agent convention
- `skills/problem-solving/agents/ps-validator.md` — Validation agent convention

**Synthesis Samples:**
- `projects/PROJ-002/synthesis/agent-integration-synthesis.md` — Production example
- `projects/PROJ-002/synthesis/proj-002-integration-synthesis.md` — Integration synthesis

**Governance:**
- `docs/governance/JERRY_CONSTITUTION.md` — Constitutional principles
- `CLAUDE.md` — Project procedures and architecture

---

*Synthesis generated by ps-synthesizer (v2.0.0) validating E2E agent output conventions*

*Validation completed: 2026-01-10*
