# EN-604: Custom Strategy Creation Tooling

<!--
TEMPLATE: Enabler
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.9
CREATED: 2026-02-12 (Claude)
PURPOSE: Implement tooling for teams to define, register, and discover custom adversarial strategies
-->

> **Type:** enabler
> **Status:** pending
> **Priority:** high
> **Impact:** high
> **Enabler Type:** infrastructure
> **Created:** 2026-02-12
> **Due:** —
> **Completed:** —
> **Parent:** FEAT-007
> **Owner:** —
> **Effort:** 8

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | What this enabler delivers |
| [Problem Statement](#problem-statement) | Why this work is needed |
| [Technical Approach](#technical-approach) | How we'll implement it |
| [Children (Tasks)](#children-tasks) | Task breakdown with agent assignments |
| [Task Dependencies](#task-dependencies) | Execution order and parallel opportunities |
| [Acceptance Criteria](#acceptance-criteria) | Definition of done |
| [Agent Assignments](#agent-assignments) | Which agents are used and their roles |
| [Related Items](#related-items) | Dependencies and hierarchy |
| [History](#history) | Change log |

---

## Summary

Implement tooling for teams to define, register, and discover custom adversarial strategies. Design a strategy definition schema, validation rules, and a registration/discovery mechanism. This enabler extends the foundational strategy catalog (FEAT-004) by enabling domain-specific adversarial patterns beyond the default set.

**Value Proposition:**
- Enables teams to codify domain-specific adversarial review patterns as first-class strategies
- Provides a formal schema ensuring all custom strategies meet minimum quality and completeness standards
- Registration and discovery mechanism allows strategies to be shared and reused across projects
- Validation rules prevent incomplete or malformed strategy definitions from entering the catalog
- Integrates with EN-603's automated selector so custom strategies participate in automated selection

**Technical Scope:**
- Strategy definition schema (YAML/JSON) with required and optional fields
- Schema validation rules and error reporting
- Strategy registration mechanism (filesystem-based catalog management)
- Strategy discovery and listing interface
- Integration points with EN-603 strategy selector

---

## Problem Statement

Jerry's initial strategy catalog (FEAT-004) provides 15 foundational adversarial strategies, but real-world usage will demand domain-specific strategies that the default catalog cannot anticipate. Without formal tooling for custom strategy creation:

1. **No extensibility path** -- Teams cannot add strategies tailored to their specific domains (e.g., security-focused, compliance-focused, performance-focused review patterns).
2. **Inconsistent quality** -- Ad hoc strategy definitions lack the structure needed for automated selection and effectiveness measurement.
3. **No discoverability** -- Custom strategies created by one team are invisible to others, preventing knowledge sharing.
4. **Integration gap** -- Without a formal registration mechanism, custom strategies cannot participate in EN-603's automated selection or EN-605's effectiveness tracking.

This enabler must define a strategy schema that balances comprehensiveness with usability, provide validation that catches common errors early, and integrate with the broader strategy ecosystem (selection, metrics, A/B testing).

---

## Technical Approach

1. **Requirements Definition** -- Use nse-requirements to define formal shall-statement requirements for the strategy definition schema. Requirements must cover: minimum required fields, validation rules, naming conventions, and integration constraints.

2. **Schema Design** -- Design the strategy definition schema as a YAML/JSON specification:
   - Required fields: name, description, steps (ordered list), applicability context, expected outcomes
   - Optional fields: author, version, tags, related strategies, effectiveness baseline
   - Validation constraints: non-empty fields, step count limits, valid context references
   - Extensibility: custom metadata fields for domain-specific annotations

3. **Registration/Discovery Implementation** -- Build the mechanism for registering and discovering strategies:
   - Filesystem-based strategy catalog (one strategy per file in a strategies directory)
   - Registration command that validates and copies strategy definition to catalog
   - Discovery command that lists available strategies with filtering (by tag, domain, author)
   - Deregistration command for removing obsolete strategies

4. **Integration Testing** -- Verify that custom strategies integrate correctly with EN-603 (selector) and EN-605 (metrics) components. Test that registered strategies appear in selector recommendations and metrics tracking.

5. **Adversarial Critique** -- Apply adversarial review to the schema design and registration mechanism, challenging completeness, usability, and edge case handling.

---

## Children (Tasks)

| ID | Title | Status | Activity | Agents |
|----|-------|--------|----------|--------|
| TASK-001 | Define shall-statement requirements for strategy definition schema | pending | RESEARCH | nse-requirements |
| TASK-002 | Design strategy definition schema (YAML/JSON specification) | pending | DEVELOPMENT | ps-architect |
| TASK-003 | Implement registration/discovery mechanism | pending | DEVELOPMENT | ps-architect |
| TASK-004 | Integration testing with EN-603 selector and EN-605 metrics | pending | TESTING | nse-integration |
| TASK-005 | Adversarial critique of schema design and registration mechanism | pending | TESTING | ps-critic |

### Task Dependencies

```
TASK-001 (requirements) ──> TASK-002 (schema design) ──> TASK-003 (registration/discovery) ──> TASK-004 (integration testing)
                                                                                                  │
                                                                                                  v
                                                                                           TASK-005 (adversarial critique)
```

- TASK-001 must complete before TASK-002 (requirements inform schema design)
- TASK-002 must complete before TASK-003 (schema defines what gets registered)
- TASK-003 must complete before TASK-004 (integration testing needs working mechanism)
- TASK-005 can begin after TASK-004 to critique the full implementation

---

## Acceptance Criteria

### Functional Criteria

| # | Criterion | Verified |
|---|-----------|----------|
| AC-1 | Formal shall-statement requirements defined for strategy schema | [ ] |
| AC-2 | Strategy definition schema includes all required fields (name, description, steps, context, outcomes) | [ ] |
| AC-3 | Schema validation catches missing required fields with clear error messages | [ ] |
| AC-4 | Schema validation catches malformed values (empty strings, invalid references) | [ ] |
| AC-5 | Registration command validates and adds strategy to catalog | [ ] |
| AC-6 | Discovery command lists strategies with filtering by tag, domain, author | [ ] |
| AC-7 | Deregistration command removes strategy from catalog | [ ] |
| AC-8 | Custom strategies appear in EN-603 selector recommendations after registration | [ ] |
| AC-9 | Custom strategies are tracked by EN-605 effectiveness metrics after registration | [ ] |
| AC-10 | Adversarial critique completed with documented feedback | [ ] |

### Non-Functional Criteria

| # | Criterion | Verified |
|---|-----------|----------|
| NFC-1 | Strategy catalog is filesystem-based (no database dependency) | [ ] |
| NFC-2 | Schema supports extensibility via custom metadata fields | [ ] |
| NFC-3 | All code has type hints and docstrings per coding standards | [ ] |
| NFC-4 | Unit test coverage >= 90% for schema validation and registration | [ ] |
| NFC-5 | No recursive subagent invocations (P-003 compliance) | [ ] |
| NFC-6 | Cross-platform compatibility (macOS, Windows, Linux) | [ ] |

---

## Agent Assignments

| Agent | Skill | Role | Phase |
|-------|-------|------|-------|
| nse-requirements | /nasa-se | Requirements engineer -- formal shall-statement requirements | TASK-001 |
| ps-architect | /problem-solving | Creator -- schema design and registration implementation | TASK-002, TASK-003 |
| nse-integration | /nasa-se | Integration tester -- verify cross-component integration | TASK-004 |
| ps-critic | /problem-solving | Adversarial -- critique schema design and implementation quality | TASK-005 |

---

## Related Items

### Hierarchy

- **Parent Feature:** [FEAT-007: Advanced Adversarial Capabilities](../FEAT-007-advanced-adversarial-capabilities.md)

### Dependencies

| Type | Item | Description |
|------|------|-------------|
| depends_on | EN-601 | Strategy selection research informs schema design for context/applicability fields |
| related | EN-603 | Custom strategies must integrate with automated strategy selector |
| related | EN-605 | Custom strategies must be trackable by effectiveness metrics |
| related | FEAT-004 | Extends the foundational strategy catalog with custom entries |

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-02-12 | Claude | pending | Enabler created with 5-task decomposition. Infrastructure enabler for custom strategy creation tooling. Depends on EN-601 research completion. |
