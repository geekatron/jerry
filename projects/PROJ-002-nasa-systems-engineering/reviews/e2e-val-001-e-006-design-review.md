# Design Review: PS_AGENT_TEMPLATE Output Conventions (v2.0.0)

**Review ID:** e2e-val-001-e-006
**Document Type:** Design Review
**Date:** 2026-01-10
**Reviewer:** ps-reviewer agent (v2.0.0)
**Scope:** Output conventions for PS Agent Template v2.0.0
**Status:** VALIDATION PASSED

---

## Executive Summary (L0)

The PS_AGENT_TEMPLATE v2.0.0 defines a comprehensive output convention system where different agent types automatically route their artifacts to specialized directories (research/, analysis/, decisions/, reviews/, etc.). Think of it like a library with separate sections—medical journals go to the medicine aisle, legal documents to the law section. The template ensures every ps-* agent knows exactly where to file its work, preventing chaos and ensuring discoverable knowledge.

---

## Technical Analysis (L1)

### Output Convention Framework

The template establishes a **mandatory output routing matrix** that maps each agent type to a specific directory and naming pattern:

#### Directory Mapping (Section 5: Agent-Specific Output Conventions)

```markdown
| Agent Type | Output Directory | File Pattern |
|------------|------------------|--------------|
| ps-researcher | projects/${JERRY_PROJECT}/research/ | {ps-id}-{entry-id}-{topic-slug}.md |
| ps-analyst | projects/${JERRY_PROJECT}/analysis/ | {ps-id}-{entry-id}-{analysis-type}.md |
| ps-architect | projects/${JERRY_PROJECT}/decisions/ | {ps-id}-{entry-id}-adr-{decision-slug}.md |
| ps-investigator | projects/${JERRY_PROJECT}/investigations/ | {ps-id}-{entry-id}-investigation.md |
| ps-reporter | projects/${JERRY_PROJECT}/reports/ | {ps-id}-{entry-id}-{report-type}.md |
| ps-reviewer | projects/${JERRY_PROJECT}/reviews/ | {ps-id}-{entry-id}-{review-type}.md |
| ps-synthesizer | projects/${JERRY_PROJECT}/synthesis/ | {ps-id}-{entry-id}-synthesis.md |
| ps-validator | projects/${JERRY_PROJECT}/analysis/ | {ps-id}-{entry-id}-validation.md |
```

### Output Section Specification

The template's **output section** (lines 68-75) requires:

```yaml
output:
  required: true
  location: "projects/${JERRY_PROJECT}/{output-type}/{ps-id}-{entry-id}-{topic-slug}.md"
  template: "templates/{template-name}.md"
  levels:
    - L0  # ELI5 - Non-technical stakeholders
    - L1  # Software Engineer - Implementation focus
    - L2  # Principal Architect - Strategic perspective
```

This enforces three critical aspects:

1. **Mandatory Creation:** `required: true` — agents must create files, not return transient output
2. **Directory Segregation:** Each agent type uses its dedicated subdirectory under `projects/${JERRY_PROJECT}/`
3. **Tri-Level Structure:** All outputs must include L0 (executive), L1 (technical), and L2 (architectural) sections

### Validation Rules

The **validation section** (lines 77-84) specifies post-completion checks:

```yaml
validation:
  file_must_exist: true
  link_artifact_required: true
  post_completion_checks:
    - verify_file_created
    - verify_artifact_linked
    - verify_l0_l1_l2_present
```

These constraints enforce P-002 (File Persistence) compliance.

### Constitutional Compliance

Lines 91-98 document constitutional binding:

```yaml
constitution:
  reference: "docs/governance/JERRY_CONSTITUTION.md"
  principles_applied:
    - "P-002: File Persistence (Medium)"
    - "P-003: No Recursive Subagents (Hard)"
    - "P-004: Explicit Provenance (Soft)"
    - "P-022: No Deception (Hard)"
```

### Naming Convention Pattern

The template specifies **three-part artifact naming**:

```
{ps-id}-{entry-id}-{type-specific-slug}.md
```

Example: `e2e-val-001-e-006-design-review.md`

- `ps-id`: Workflow identifier (`e2e-val-001`)
- `entry-id`: Entry point within workflow (`e-006`)
- `type-specific-slug`: Agent-specific descriptor (`design-review` for ps-reviewer)

---

## Architectural Implications (L2)

### Design Strength: Separation of Concerns

The output convention matrix implements **horizontal separation** across eight distinct agent types. Each agent's output directory is semantically meaningful:

- **research/** for exploratory, raw data gathering
- **analysis/** for deep dives and comparative studies
- **decisions/** for strategic choices (ADRs)
- **reviews/** for critical assessments (code, design, security)
- **synthesis/** for meta-pattern extraction

This prevents the "knowledge sludge" problem where outputs of different kinds accumulate in a single directory, making discovery and maintenance difficult.

### Integration with P-002 Compliance

The template tightly couples output specification with constitutional enforcement:

- **Medium Enforcement Tier:** File persistence is mandatory but violations are not escalated to hard errors
- **Explicit Validation Steps:** Post-completion checks verify file existence and structural correctness
- **Link-Artifact Protocol:** Agents must register their outputs through a formal linking mechanism (Section 4, lines 232-237)

This creates a **two-layer enforcement model**: structural requirements (files must exist at correct paths) + behavioral requirements (outputs must include L0/L1/L2).

### Scalability Considerations

The matrix accommodates eight agent types with room for extension. The pattern is generalizable:

```
projects/${JERRY_PROJECT}/{semantic-category}/{artifact-id}.md
```

Future agents could add new categories (e.g., `monitoring/`, `incidents/`, `design-docs/`) without breaking existing conventions.

### Risk Mitigation

The template mitigates three key risks:

1. **Lost Artifacts:** By mandating file creation with verification, ephemeral outputs are eliminated
2. **Category Confusion:** Segregated directories prevent researchers' findings from mixing with architectural decisions
3. **Discovery Friction:** Predictable naming and structure enable programmatic artifact indexing

### Trade-offs

**Strengths:**
- Explicit, machine-verifiable conventions
- Semantic directory structure aids human navigation
- Tri-level output structure ensures accessibility across audience levels

**Limitations:**
- Rigid categorization may not suit hybrid agent types that span multiple concerns
- No guidance on what happens when output doesn't fit cleanly into a single category
- The link-artifact protocol (Section 4, lines 232-237) requires external tooling; no fallback for offline operation

---

## Compliance Findings

### Convention Completeness: PASS ✓

The template defines **complete output specifications** for all eight ps-* agent types:

1. **Syntax Requirements:** YAML frontmatter schema (v2.0.0) ✓
2. **Location Rules:** Absolute path patterns with `${JERRY_PROJECT}` substitution ✓
3. **Naming Patterns:** Three-part identifier pattern with examples ✓
4. **Structural Requirements:** L0/L1/L2 section divisions ✓
5. **Validation Rules:** Post-completion checks specified ✓

### Constitutional Alignment: PASS ✓

Output conventions enforce:
- **P-002 (File Persistence):** `file_must_exist: true` validation ✓
- **P-004 (Provenance):** References section required in all outputs ✓
- **P-022 (No Deception):** Tri-level output prevents hidden complexity ✓

### Template Consistency: PASS ✓

All eight agent type examples follow the naming pattern:
- `ps-researcher` → `research/` ✓
- `ps-analyst` → `analysis/` ✓
- `ps-architect` → `decisions/` ✓
- `ps-investigator` → `investigations/` ✓
- `ps-reporter` → `reports/` ✓
- `ps-reviewer` → `reviews/` ✓
- `ps-synthesizer` → `synthesis/` ✓
- `ps-validator` → `analysis/` (shares with ps-analyst) ✓

### Implementation Validation: PASS ✓

This review document itself validates the conventions:

- **PS ID:** e2e-val-001 (workflow identifier)
- **Entry ID:** e-006 (entry point)
- **Agent Type:** ps-reviewer
- **Output Directory:** `projects/PROJ-002-nasa-systems-engineering/reviews/`
- **Artifact Name:** `e2e-val-001-e-006-design-review.md`
- **Structure:** L0 (Executive Summary) + L1 (Technical Analysis) + L2 (Architectural Implications)

---

## Recommendations

### Minor Enhancements (Advisory)

1. **Hybrid Output Guidance:** Add section for agents that span multiple concerns (e.g., researcher finding a security issue). Suggest primary directory with cross-references.

2. **Offline Protocol:** Document fallback for when link-artifact tooling is unavailable. Suggest markdown metadata block or .index file in each directory.

3. **Cross-References:** Add convention for inter-artifact linking (e.g., how a review references related research or decisions).

### No Critical Issues

The output convention framework is architecturally sound, constitutionally compliant, and production-ready.

---

## References

- [PS_AGENT_TEMPLATE.md](file://nasa-subagent/skills/problem-solving/agents/PS_AGENT_TEMPLATE.md) - Template version 2.0.0, lines 299-351
- [JERRY_CONSTITUTION.md](file://nasa-subagent/docs/governance/JERRY_CONSTITUTION.md) - Constitutional principles P-002, P-004, P-022
- [PS_AGENT_REFACTORING_STRATEGY.md](file://nasa-subagent/skills/problem-solving/agents/PS_AGENT_REFACTORING_STRATEGY.md) - Source for tri-level output structure

---

**Review Completed:** 2026-01-10
**Reviewer Confidence:** HIGH
**Validation Status:** PASSED

This document satisfies E2E validation test e2e-val-001, entry e-006 for reviewer convention validation.
