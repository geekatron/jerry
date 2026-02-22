# SPIKE-002: AST-First Architecture Feasibility Assessment

<!--
TEMPLATE: Spike
VERSION: 0.1.0
SOURCE: ONTOLOGY-v1.md Section 3.4.8
-->

> **Type:** spike
> **Status:** completed
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

GO decision — AST-first architecture is feasible and beneficial for Jerry's markdown manipulation, with bounded scope to schema-heavy files. Four integration patterns evaluated; Pattern D (Hybrid: CLI + Skill with shared domain layer) recommended. Token reduction estimated at 15-30% per individual operation, 40-60% for batch operations. 5/6 Jerry markdown patterns schematizable.

### Detailed Findings

- **Integration patterns:** 4 patterns analyzed (A: CLI-only, B: Skill-only, C: MCP server, D: Hybrid). Pattern D recommended for maximum flexibility.
- **Token efficiency:** 15-30% per operation, 40-60% batch. AST JSON is more verbose but enables targeted node manipulation.
- **Schema feasibility:** 5/6 patterns schematizable (worktracker entities, skill definitions, rules, templates, orchestration plans). Freeform prose out of scope.
- **Risk analysis:** S-013 Inversion identified 7 failure modes; S-004 Pre-Mortem identified 6 scenarios. All mitigable.
- **Implementation estimate:** ~1,740 LOC total, 6-week timeline, 10 stories, 37 story points for FEAT-001.

See orchestration artifacts for full details:
- `orchestration/spike-eval-20260219-001/ps/phase-4-arch-research/ps-researcher-002/integration-patterns-research.md`
- `orchestration/spike-eval-20260219-001/ps/phase-5-feasibility/ps-analyst-002/feasibility-analysis.md`
- `orchestration/spike-eval-20260219-001/ps/phase-6-decision/ps-synthesizer-002/go-nogo-recommendation.md`

### Evidence/References

28 evidence-mapped claims across research artifacts. Cross-spike consistency verified by ps-reviewer-001. Full traceability in go-nogo-recommendation.md.

---

## Recommendation

### Decision

**GO** — Adopt AST-first architecture with bounded scope. Confidence: HIGH.

- **Library:** markdown-it-py v4.0.0 + mdformat v1.0.0
- **Integration:** Pattern D (Hybrid: CLI + Skill with shared domain layer)
- **Scope:** Schema-heavy files (worktracker, templates, skills, rules, orchestration)
- **Conditional on:** R-01 proof-of-concept validating mdformat blockquote frontmatter write-back

### Recommended Actions

1. Create R-01 proof-of-concept story for mdformat validation
2. Define FEAT-001 implementation stories (10 stories, 37 SP from go/no-go recommendation)
3. Create ADR documenting the GO decision
4. Begin implementation with domain layer (MarkdownDocument, AST node types)

### Follow-up Work Items

| Type | Title | Priority |
|------|-------|----------|
| Story | R-01 proof-of-concept: mdformat blockquote frontmatter write-back | high |
| Story | Domain layer: MarkdownDocument value object and AST node types | high |
| Story | Custom extensions: blockquote frontmatter, nav table, template placeholder, L2-REINJECT | high |
| Story | CLI integration: `jerry md parse\|render\|validate\|query` | medium |
| ADR | AST-first architecture GO decision | high |

### Risks/Considerations

- R-01 validation is a hard gate — if mdformat can't handle blockquote frontmatter write-back, the NO-GO alternative strategy (structured YAML primary with markdown rendering) should be activated
- Bounded scope means freeform files continue with raw text manipulation
- Migration of existing skills is incremental, not big-bang
- mdformat code renderer reflow behavior needs validation

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
| 2026-02-19 | completed | Spike completed via orchestration `spike-eval-20260219-001`. GO decision — adopt AST-first with markdown-it-py + mdformat, Pattern D hybrid integration. QG2 passed at 0.97. |
