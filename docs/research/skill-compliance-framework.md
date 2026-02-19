# Skill Compliance Framework

> A 2,646-line compliance framework with 117 checkpoints across 8 orchestration patterns — reusable for any Claude Code skill. Includes gap analysis, Pareto prioritization, and a 4-phase remediation roadmap.

---

## Key Findings

- **8 canonical orchestration patterns** identified across Jerry's top 3 skills (problem-solving, nasa-se, orchestration) with 0.98 confidence
- **117 compliance checkpoints** organized into 12 SKILL.md sections, 5 agent specification sections, and 8 orchestration patterns
- **Pareto principle applies**: fixing 17 HIGH/CRITICAL gaps (20% of work) resolves 80% of compliance issues
- **Transcript skill scored 52% compliance** against the universal pattern catalog — used as the validation case study
- **33-hour remediation estimate** (4 days) to bring a non-compliant skill to 95%+ compliance across 4 phases

---

## Jerry Skill Pattern Synthesis & Compliance Framework

The most comprehensive artifact in the skill architecture domain. This synthesis analyzes the pattern DNA of Jerry's three most mature skills to extract universal blueprints that any Claude Code skill can follow.

??? note "Methodology"
    The synthesis used a **three-phase approach**:

    1. **Pattern Extraction** (ps-researcher): Analyzed problem-solving v2.1.0, nasa-se v1.1.0, and orchestration v2.1.0 to identify shared patterns with ≥2/3 skill convergence
    2. **Gap Analysis** (ps-analyst): Applied 5W2H + Pareto + FMEA frameworks against the transcript skill as validation case study, scoring 5 dimensions with 17 HIGH gaps identified
    3. **Synthesis** (ps-synthesizer): Produced the unified framework with copy-paste checklists, best practices, and prioritized remediation roadmap

    The L0/L1/L2 triple-lens structure ensures the framework is accessible to stakeholders (L0 "sports team" analogy), engineers (L1 checklists), and architects (L2 orchestration patterns).

??? abstract "Key Data: Pattern Catalog"
    **SKILL.md Blueprint (PAT-SKILL-001)** — 12 required sections:

    1. YAML Frontmatter (name, description, version, allowed-tools, activation-keywords)
    2. Document Audience (Triple-Lens with L0/L1/L2 reading guides)
    3. Purpose (mission, capabilities, differentiation)
    4. When to Use (activation criteria, trigger phrases, anti-triggers)
    5. Available Agents (registry table)
    6. Invoking an Agent (3 methods with examples)
    7. Orchestration Flow (multi-agent coordination diagram)
    8. State Passing (state key registry, session_context schema)
    9. Tool Invocation Examples
    10. Constitutional Compliance
    11. Quick Reference
    12. Templates

??? abstract "Key Data: 8 Orchestration Patterns"
    | Pattern | Description | Used By |
    |---------|-------------|---------|
    | Sequential Chain | Agents execute in order, output feeds next | All 3 skills |
    | Fan-Out/Fan-In | Parallel execution with aggregation | orchestration |
    | Creator-Critic-Revision | Iterative quality improvement cycle | problem-solving |
    | Checkpoint Recovery | Resume from persisted state after failure | orchestration |
    | State Handoff | Structured data passing between agents | All 3 skills |
    | Quality Gate | Score-based pass/fail at boundaries | problem-solving |
    | Escalation | Criticality-based strategy activation | problem-solving |
    | Cross-Pollination | Multi-pipeline sync with handoff manifests | orchestration |

??? abstract "Key Data: Compliance Gap Summary"
    | Severity | Count | Example Gaps |
    |----------|-------|-------------|
    | CRITICAL | 5 | Missing YAML frontmatter, no session_context schema, no orchestration pattern declaration |
    | HIGH | 12 | Missing agent YAML headers, no state key registry, incomplete tool examples |
    | MEDIUM | 18 | Missing anti-triggers, incomplete L2 sections, no cross-skill references |
    | LOW | 8 | Missing ASCII diagrams, incomplete quick reference tables |

    **Pareto analysis**: 17 CRITICAL+HIGH gaps = 20% of total gaps but 80% of compliance impact. Estimated remediation: 33 hours across 4 phases.

[:octicons-link-external-16: Full framework (2,646 lines)](https://github.com/geekatron/jerry/blob/main/docs/synthesis/work-026-e-003-jerry-skill-compliance-framework.md)

---

## Supporting Research

### Jerry Skill Pattern Research

The foundational research feeding into the compliance framework — a detailed analysis of patterns across Jerry's three most mature skills.

??? abstract "Key Data"
    - 1,375 lines of pattern analysis
    - Universal YAML frontmatter schema defined
    - Agent specification patterns extracted
    - All 3 mature skills analyzed for convergence points

[:octicons-link-external-16: Skill Pattern Research (1,375 lines)](https://github.com/geekatron/jerry/blob/main/docs/research/internal/work-026-e-001-jerry-skill-patterns.md)

### Transcript Skill Gap Analysis

The validation case study that tested the compliance framework against a real skill, revealing 52% compliance and 17 HIGH/CRITICAL gaps.

??? abstract "Key Data"
    - 1,206 lines of gap analysis
    - 5W2H + Pareto + FMEA frameworks applied
    - 5 compliance dimensions scored
    - 17 HIGH gaps identified with remediation guidance

[:octicons-link-external-16: Gap Analysis (1,206 lines)](https://github.com/geekatron/jerry/blob/main/docs/analysis/work-026-e-002-transcript-skill-gap-analysis.md)

---

## Related Research

- [Claude Code Ecosystem](claude-code-ecosystem.md)
- [Architecture Patterns](architecture-patterns.md)
- [Governance & Constitutional AI](governance-constitutional-ai.md)
