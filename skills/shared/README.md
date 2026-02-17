# skills/shared - Shared Skill Infrastructure

> **Purpose:** Common templates, patterns, and contracts used across multiple Jerry skills.
> **Version:** 1.0.0
> **Last Updated:** 2026-02-16

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Overview](#overview) | What this directory contains |
| [Contents](#contents) | File-by-file reference |
| [Usage](#usage) | How to use these resources |
| [For Skill Authors](#for-skill-authors) | Creating new skills |
| [Constitutional Compliance](#constitutional-compliance) | Governance principles |

---

## Overview

The `skills/shared/` directory contains reusable infrastructure that multiple Jerry skills depend on:

- **Agent Templates** - Federated core template for agent definitions
- **Orchestration Patterns** - 8 canonical multi-agent workflow patterns
- **Playbook Template** - Triple-lens structure for skill documentation
- **Cross-Skill Contracts** - Handoff schemas for ps-* <-> nse-* agent chaining

**Key Insight:** This directory enables **composition over duplication**. Instead of copying boilerplate across skills, skills reference and compose from these shared resources.

---

## Contents

### AGENT_TEMPLATE_CORE.md

**Purpose:** Federated core template containing ~73% shared content for all Jerry agents.

**Based On:**
- PS_AGENT_TEMPLATE v2.0 (problem-solving agents)
- NSE_AGENT_TEMPLATE v1.0 (nasa-se agents)
- Jerry Constitution v1.0

**Extension Points:** 9 placeholders that domain extensions (PS_EXTENSION.md, NSE_EXTENSION.md) populate:
- `DOMAIN_NAME_PREFIX` - Agent name prefix (ps, nse)
- `DOMAIN_IDENTITY_EXTENSION` - Additional identity fields
- `DOMAIN_FORBIDDEN_ACTIONS` - Domain-specific forbidden actions
- `DOMAIN_INPUT_VALIDATION` - Domain-specific ID validation patterns
- `DOMAIN_OUTPUT_FILTERING` - Additional output filtering rules
- `DOMAIN_VALIDATION_FIELDS` - Domain-specific validation fields
- `DOMAIN_REFERENCES` - Domain references (prior_art OR nasa_standards)
- `DOMAIN_PRINCIPLES` - Additional constitution principles
- `DOMAIN_XML_SECTIONS` - Domain-specific XML sections

**Usage:** Use the composition script to generate complete agent templates:

```bash
python3 scripts/compose_agent_template.py --domain {ps|nse} --output {output-path}
```

**Sections:**
- YAML frontmatter schema v1.0 (identity, persona, capabilities, guardrails, output, validation)
- XML-structured agent body (Anthropic best practice)
- Constitutional compliance checklist
- Invocation protocol
- State management (Google ADK pattern)
- Output levels (L0/L1/L2)

---

### ORCHESTRATION_PATTERNS.md

**Purpose:** Canonical reference for 8 multi-agent orchestration patterns in Jerry.

**Version:** 1.1.0

**Source:** SAO-INIT-007 Deep Research (DISCOVERY-008)

**Patterns Covered:**
1. **Single Agent** - Direct invocation, no coordination
2. **Sequential Chain** - Linear workflow with state handoff
3. **Fan-Out (Parallel)** - Independent parallel execution
4. **Fan-In (Aggregation)** - Synthesize multiple outputs
5. **Cross-Pollinated Pipeline** - Bidirectional barrier synchronization
6. **Divergent-Convergent (Diamond)** - Explore options → select best
7. **Review Gate** - Quality checkpoint before progression
8. **Generator-Critic Loop** - Iterative refinement with circuit breaker

**Each Pattern Includes:**
- **L0 (ELI5):** Metaphor and plain English explanation
- **L1 (Engineer):** Topology diagram, invocation examples, use cases
- **L2 (Architect):** Anti-patterns, state management, cognitive mode, design rationale

**Usage:** Reference this document when designing multi-agent workflows. See `skills/orchestration/SKILL.md` for orchestration skill details.

**Decision Tree:** Provides pattern selection guidance based on task characteristics (single/multi-agent, dependent/independent, quality gates, iteration).

**Constitutional Compliance:** All patterns comply with P-002 (file persistence), P-003 (single-level nesting), P-010 (worktracker), P-022 (transparency).

---

### PLAYBOOK_TEMPLATE.md

**Purpose:** Template for creating skill playbooks with triple-lens structure.

**Version:** 1.0.0

**Target Audiences:**
- **L0 (ELI5):** Stakeholders, newcomers, non-technical users
- **L1 (Engineer):** Developers executing the skill
- **L2 (Architect):** Workflow designers, system architects

**Sections:**
- **L0: The Big Picture** - Metaphors, what/why, activation keywords, agent portfolio
- **L1: How To Use It** - Quick start, invocation methods, agent reference, common workflows, output locations, tips, troubleshooting
- **L2: Architecture & Constraints** - Anti-pattern catalog, constraints/boundaries, invariants, state management, cross-skill integration, design rationale

**Usage:** Copy this template when creating a new skill's PLAYBOOK.md. Replace all `{placeholders}` with skill-specific content.

**Triple-Lens Benefits:**
- **Progressive disclosure** - Users read only what they need for their role
- **Consistent structure** - All playbooks follow the same navigation pattern
- **Multi-audience** - One document serves newcomers, engineers, and architects

---

### contracts/CROSS_SKILL_HANDOFF.yaml

**Purpose:** Interface contract for cross-skill handoffs between Problem-Solving (ps-*) and NASA Systems Engineering (nse-*) agent families.

**Version:** 1.0.0

**Format:** OpenAPI 3.0-inspired schema

**Skill Families:**
- **ps (Problem-Solving):** ps-researcher, ps-analyst, ps-architect, ps-critic, ps-validator, ps-synthesizer, ps-reviewer, ps-investigator, ps-reporter
- **nse (NASA SE):** nse-requirements, nse-verification, nse-risk, nse-reviewer, nse-integration, nse-configuration, nse-architecture, nse-explorer, nse-qa, nse-reporter

**Handoff Patterns:**

**PS → NSE** (Research/Analysis to SE Artifacts):
- HANDOFF-001: Research to Requirements
- HANDOFF-002: Analysis to Risk Assessment
- HANDOFF-003: Architecture Decision to Design
- HANDOFF-004: Validation to Verification
- HANDOFF-005: Synthesis to Requirements
- HANDOFF-006: Review to Technical Review
- HANDOFF-007: Investigation to Risk

**NSE → PS** (SE Artifacts to Analysis):
- HANDOFF-101: Requirements to Research (TBDs/TBRs)
- HANDOFF-102: Risk to Analysis (High risks)
- HANDOFF-103: Review Findings to Investigation
- HANDOFF-104: Exploration to Synthesis
- HANDOFF-105: QA Findings to Review
- HANDOFF-106: Architecture to Critique

**Session Context Schema v1.0.0:**
- `schema_version` - Version for evolution support
- `session_id` - Unique session identifier
- `source_agent` - Source agent (id, family, cognitive_mode, model)
- `target_agent` - Target agent (id, family)
- `payload` - Key findings, open questions, blockers, confidence, artifacts, context
- `timestamp` - ISO-8601 timestamp

**Validation Rules:**
- **On receive:** Schema version check, cross-skill detection, session identity check, source agent validation, payload validation, cognitive mode translation
- **On send:** Populate key findings, calculate confidence, list artifacts (P-002), set timestamp, add traceability (P-040 for NSE targets)

**Cognitive Mode Translation:**
- **Divergent → Convergent:** Narrowing (prioritize by confidence, extract actionable items, summarize alternatives)
- **Convergent → Divergent:** Expansion (identify gaps, enumerate alternatives, add context breadth)

**Testing:** Unit tests (schema validation, cross-skill detection, translation mapping), integration tests (end-to-end chains, bidirectional cycles), contract tests (schema evolution, cognitive mode boundaries, traceability preservation).

---

## Usage

### For Skill Authors

When creating a new skill:

1. **Use AGENT_TEMPLATE_CORE.md** - Compose agent definitions using the core template + domain extension
2. **Reference ORCHESTRATION_PATTERNS.md** - Select appropriate pattern for multi-agent workflows
3. **Copy PLAYBOOK_TEMPLATE.md** - Create skill playbook with triple-lens structure
4. **Implement CROSS_SKILL_HANDOFF.yaml** - If your skill needs to hand off to ps-* or nse-* agents

### For Agent Designers

When creating a new agent:

1. Determine domain (ps, nse, orch, etc.)
2. Create domain extension file if it doesn't exist
3. Run composition script: `python3 scripts/compose_agent_template.py --domain {domain}`
4. Replace all `{placeholders}` with agent-specific content
5. Validate against constitution (P-002, P-003, P-004, P-022)
6. Register agent in skill's SKILL.md agent table

### For Orchestration Designers

When designing a multi-agent workflow:

1. Review ORCHESTRATION_PATTERNS.md decision tree
2. Select pattern based on task characteristics
3. Use session context schema (v1.0.0) for state handoff
4. Apply cognitive mode translation if crossing divergent/convergent boundary
5. Verify constitutional compliance (P-002, P-003, P-010, P-022)

---

## For Skill Authors

### Creating a New Skill

1. **Create skill directory:** `skills/{skill-name}/`
2. **Create SKILL.md:** Copy structure from `skills/problem-solving/SKILL.md` or `skills/orchestration/SKILL.md`
   - Include triple-lens audience table
   - Add navigation table (H-23/H-24)
   - Document purpose, capabilities, when to use
   - List available agents/commands
   - Add constitutional compliance section
3. **Create PLAYBOOK.md (optional):** Copy `skills/shared/PLAYBOOK_TEMPLATE.md` if skill needs workflow examples
4. **Create agents (if applicable):** Use `skills/shared/AGENT_TEMPLATE_CORE.md` with domain extension
5. **Create templates (if applicable):** Add skill-specific templates to `skills/{skill-name}/templates/`
6. **Update skills registry:** Add skill to `CLAUDE.md` skill table

### Extending Shared Resources

If you need to extend shared resources:

- **Agent template:** Create a new extension file (e.g., `ORCH_EXTENSION.md`) and update composition script
- **Orchestration patterns:** Propose new pattern via ADR in `docs/decisions/`
- **Playbook template:** Propose changes via ADR (affects all skills)
- **Cross-skill handoff:** Add new handoff pattern to `contracts/CROSS_SKILL_HANDOFF.yaml`

---

## Constitutional Compliance

Shared resources adhere to the **Jerry Constitution v1.0**:

| Principle | Requirement | Implementation |
|-----------|-------------|----------------|
| P-002: File Persistence | All outputs persisted | Agent template enforces output location and file validation |
| P-003: No Recursive Subagents | Single-level nesting only | Orchestration patterns document P-003 compliance per pattern |
| P-004: Explicit Provenance | Reasoning documented | Agent template includes provenance checklist |
| P-022: No Deception | Transparent limitations | Playbook template includes anti-pattern catalog |
| H-23: Navigation Tables | Required for 30+ line docs | All shared docs include navigation tables |
| H-24: Anchor Links | Required in nav tables | All section names use correct anchor syntax |

**Self-Critique Checklist:**
- [ ] P-002: Does agent template enforce file output?
- [ ] P-003: Do orchestration patterns respect single-level nesting?
- [ ] P-004: Do templates include provenance/reasoning sections?
- [ ] P-022: Are limitations and anti-patterns documented?
- [ ] H-23: Do all docs over 30 lines have navigation tables?
- [ ] H-24: Are anchor links correct in navigation tables?

---

## References

- Agent Template ADR: `docs/decisions/wi-sao-009-adr-unified-template-architecture.md`
- Orchestration Patterns Source: SAO-INIT-007 Deep Research (DISCOVERY-008)
- Session Context Schema: `docs/schemas/session_context.json`
- Jerry Constitution: `docs/governance/JERRY_CONSTITUTION.md`
- Quality Enforcement SSOT: `.context/rules/quality-enforcement.md`

---

*Directory Version: 1.0.0*
*Last Updated: 2026-02-16*
*Constitutional Compliance: Jerry Constitution v1.0*
