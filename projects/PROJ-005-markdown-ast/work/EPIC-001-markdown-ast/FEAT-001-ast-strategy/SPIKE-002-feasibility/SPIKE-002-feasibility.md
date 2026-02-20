# SPIKE-002: AST-First Architecture Feasibility Assessment

<!--
TEMPLATE: Spike
VERSION: 0.1.0
SOURCE: ONTOLOGY-v1.md Section 3.4.8
-->

> **Type:** spike
> **Status:** pending
> **Priority:** high
> **Impact:** high
> **Created:** 2026-02-19
> **Parent:** FEAT-001
> **Owner:** --
> **Effort:** 8

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Content](#content) | Research question, hypothesis, scope |
| [Findings](#findings) | Feasibility assessment (populated after research) |
| [Recommendation](#recommendation) | Go/no-go decision (populated after research) |
| [Related Items](#related-items) | Hierarchy and related work |
| [History](#history) | Status changes |

---

## Content

### Research Question

**Question:** Is an AST-first architecture feasible and beneficial for Jerry's markdown manipulation across the full surface, and if so, how should it integrate — as a Jerry CLI extension, hidden Claude-only skills, or a hybrid approach?

### Hypothesis

We hypothesize that:
1. An AST intermediary will reduce token consumption by 30-50% for typical markdown operations (targeted node manipulation vs full-file text replacement)
2. Schema validation at parse time will catch 80%+ of structural errors that currently propagate silently
3. Integration as a Jerry CLI command (`jerry md parse/render/validate`) provides the cleanest architecture
4. Hidden Claude-only skills may be simpler to implement but create a parallel tooling surface that's harder to maintain
5. The strategy makes sense for schema-heavy files (worktracker, templates) but may be overkill for freeform files (research notes, ADR prose)

### Timebox

| Aspect | Value |
|--------|-------|
| Timebox Duration | 8 hours |
| Start Date | TBD |
| Target End Date | TBD |

**Warning:** Do not exceed the timebox. If more research is needed, create a follow-up spike.

### Scope

**In Scope:**
- Feasibility assessment: can SPIKE-001's top-ranked library handle Jerry's full markdown surface?
- Token efficiency analysis: estimate savings for representative operations (update status field, add history row, instantiate template, validate nav table)
- Integration architecture options: (a) Jerry CLI extension, (b) hidden Claude-only skills, (c) hybrid, (d) MCP server
- Schema definition approach: how to define and enforce markdown schemas for different file types
- Migration path: how to transition existing skills from raw text to AST operations
- Risk analysis: what could go wrong, what's the blast radius of a bad parse/render cycle
- Alternative strategies if AST is not viable (e.g., structured YAML/JSON primary with markdown rendering, TOML frontmatter, etc.)

**Out of Scope:**
- Library selection (that's SPIKE-001)
- Actual implementation (future features)
- Performance optimization
- Full schema language design

### Research Approach

1. **Dependency:** Read SPIKE-001 findings for top-ranked library capabilities and limitations.
2. **Token efficiency modeling:** Take 5 representative markdown operations Claude performs today. Estimate tokens consumed via raw text (read full file, find-replace, write full file) vs AST (parse to JSON, modify node, render). Calculate projected savings.
3. **Integration architecture analysis:** Design 4 integration options with trade-off matrices:
   - (a) `jerry md parse|render|validate|query` CLI commands
   - (b) Hidden skills that wrap AST operations for Claude's use
   - (c) Hybrid: CLI for batch/CI operations, skills for interactive Claude use
   - (d) MCP server exposing AST operations as tools
4. **Schema feasibility:** Assess how to define schemas for worktracker entities, skill definitions, rules, templates. Can schemas be expressed as AST node patterns? Can validation be automatic at parse time?
5. **Migration analysis:** Map current skill operations to AST equivalents. Identify: what's easy to migrate, what's hard, what breaks, what improves.
6. **Risk assessment:** Apply S-013 (Inversion) — "How could AST-first fail?" Document failure modes, mitigations, and the cost of reverting.
7. **Alternative strategy assessment:** If AST is infeasible, what else could work? Structured data primary (YAML/JSON) with markdown rendering? Enhanced string templates? Hybrid approaches?
8. **Go/no-go synthesis:** Produce recommendation with evidence, adversarial review artifacts, and confidence level.

---

## Findings

### Summary

_To be populated after research. Depends on SPIKE-001 completion._

### Detailed Findings

_To be populated after research._

### Evidence/References

_To be populated after research._

---

## Recommendation

### Decision

_To be populated after research. Go/no-go with confidence level._

### Recommended Actions

_To be populated after research._

### Follow-up Work Items

| Type | Title | Priority |
|------|-------|----------|
| _TBD_ | _Based on go/no-go: either integration feature or alternative strategy feature_ | _TBD_ |

### Risks/Considerations

- Roundtrip fidelity loss may make AST operations destructive for freeform files
- Token savings may be smaller than estimated if AST JSON representation is verbose
- Schema definition and enforcement adds complexity that may not justify the benefit for low-structure files
- Dual tooling surfaces (CLI + skills) increase maintenance burden
- Migration of existing skills is non-trivial and may introduce regressions during transition

---

## Related Items

- Parent: [FEAT-001: AST Strategy Evaluation & Library Selection](../FEAT-001-ast-strategy.md)
- Depends On: [SPIKE-001: Python Markdown AST Library Landscape](../SPIKE-001-library-landscape/SPIKE-001-library-landscape.md)
- Informs: Go/no-go ADR in decisions/
- Related: PROJ-004 context resilience — AST efficiency gains extend context lifetime

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-02-19 | pending | Spike defined. 8-step research approach. Blocked on SPIKE-001 findings. 8h timebox. |
