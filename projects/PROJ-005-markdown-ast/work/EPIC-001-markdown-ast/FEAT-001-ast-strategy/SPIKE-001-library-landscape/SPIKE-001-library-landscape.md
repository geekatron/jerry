# SPIKE-001: Python Markdown AST Library Landscape

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
> **Effort:** 12

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Content](#content) | Research question, hypothesis, scope |
| [Evaluation Framework](#evaluation-framework) | Scoring criteria and weights |
| [Findings](#findings) | Library evaluations (populated after research) |
| [Recommendation](#recommendation) | Decision and recommended actions (populated after research) |
| [Related Items](#related-items) | Hierarchy and related work |
| [History](#history) | Status changes |

---

## Content

### Research Question

**Question:** What Python markdown AST libraries exist, how do they compare against Jerry's specific requirements, and should we adopt one, adapt one, or build from scratch?

### Hypothesis

We hypothesize that:
1. At least 5 mature Python markdown AST libraries exist with varying levels of AST access
2. The mdast/remark ecosystem (JavaScript) is the gold standard, but Python equivalents exist
3. Jerry's markdown dialect (blockquote frontmatter, navigation tables, template placeholders) may require custom extensions regardless of library choice
4. An existing library with extension points will outperform building from scratch on cost/time/maintenance

### Timebox

| Aspect | Value |
|--------|-------|
| Timebox Duration | 12 hours |
| Start Date | TBD |
| Target End Date | TBD |

**Warning:** Do not exceed the timebox. If more research is needed, create a follow-up spike.

### Scope

**In Scope:**
- Identify 5+ Python markdown AST libraries (e.g., markdown-it-py, mistune, marko, commonmark.py, mdformat, pymarkdownlnt, mdit-py-plugins, others)
- Evaluate each library against Jerry-specific requirements (see Evaluation Framework)
- Test each library against real Jerry markdown samples (worktracker entity, skill definition, rule file, template)
- Assess extension/plugin ecosystems for custom syntax handling
- Evaluate build-from-scratch option: effort estimate, architecture sketch, maintenance burden
- Use Context7 for latest library documentation
- Use Web Search for latest releases, community activity, and benchmarks
- All findings must include evidence: sources, references, citations, version numbers

**Out of Scope:**
- JavaScript/Node.js libraries (Python-only constraint)
- Performance benchmarking at scale (basic parse/render timing only)
- Full integration architecture (that's SPIKE-002)
- Schema definition language design

### Research Approach

1. **Library discovery:** Web Search for "Python markdown AST parser 2025 2026", Context7 for documentation of known libraries. Target 5+ candidates.
2. **Feature inventory:** For each library, document: AST format (tree structure), extension API, roundtrip fidelity (parse->render preserves formatting), GFM support, table support, frontmatter handling, code block handling, plugin ecosystem.
3. **Jerry compatibility testing:** Take 4 representative Jerry markdown files (worktracker entity, skill definition, rule file with L2-REINJECT comments, template with placeholders). Parse each with each library. Document: what parses correctly, what breaks, what requires extensions.
4. **Extension assessment:** For each library, assess: can blockquote frontmatter be parsed as structured data? Can navigation tables be queried? Can template placeholders (`{{VAR}}`) be preserved through roundtrip? Can HTML comments (L2-REINJECT) be accessed?
5. **Build-from-scratch analysis:** Estimate effort to build a minimal Jerry-specific markdown AST parser. Define: what subset of markdown do we need? What's the grammar? How much of CommonMark do we need? What's the ongoing maintenance cost?
6. **Scoring:** Apply evaluation framework weights to produce composite scores.
7. **Synthesis:** Produce feature matrix, ranked recommendations, and trade-off analysis.

---

## Evaluation Framework

### Scoring Dimensions

| Dimension | Weight | Description |
|-----------|--------|-------------|
| AST Quality | 0.20 | Richness of AST, node types, position info, metadata |
| Roundtrip Fidelity | 0.20 | Parse -> render preserves original formatting and content |
| Extension API | 0.15 | Ability to add custom syntax (frontmatter, placeholders, etc.) |
| Jerry Compatibility | 0.15 | Works with blockquote frontmatter, nav tables, L2-REINJECT, Mermaid |
| Maintenance & Community | 0.10 | Active development, releases, contributors, issue response time |
| Python API Ergonomics | 0.10 | Clean API, type hints, documentation quality |
| Performance | 0.05 | Parse/render speed (basic timing only) |
| License Compatibility | 0.05 | Compatible with Jerry's Apache-2.0 license |

### Scoring Scale

| Score | Meaning |
|-------|---------|
| 5 | Excellent — meets or exceeds requirements |
| 4 | Good — meets requirements with minor gaps |
| 3 | Adequate — functional but notable limitations |
| 2 | Poor — significant gaps, heavy workarounds needed |
| 1 | Inadequate — fundamentally incompatible |

### Jerry Markdown Samples (Test Files)

| Sample | File | Key Challenges |
|--------|------|----------------|
| Worktracker entity | `EPIC-001-context-resilience.md` | Blockquote frontmatter, navigation table, progress ASCII art, history table |
| Skill definition | `skills/orchestration/SKILL.md` | Multi-level navigation, agent tables, code blocks, complex structure |
| Rule file | `.context/rules/quality-enforcement.md` | HTML comments (L2-REINJECT), deeply nested tables, anchor links |
| Template | `.context/templates/worktracker/EPIC.md` | `{{PLACEHOLDER}}` syntax, YAML code blocks, HTML comments with metadata |

---

## Findings

### Summary

_To be populated after research._

### Library Evaluations

_To be populated after research. One subsection per library._

### Feature Matrix

_To be populated after research. Comparative table across all dimensions._

### Build-from-Scratch Assessment

_To be populated after research._

### Evidence/References

_To be populated after research. All sources with URLs, version numbers, access dates._

---

## Recommendation

### Decision

_To be populated after research._

### Recommended Actions

_To be populated after research._

### Follow-up Work Items

| Type | Title | Priority |
|------|-------|----------|
| _TBD_ | _To be defined based on findings_ | _TBD_ |

### Risks/Considerations

- Libraries may have stale development (last release > 1 year)
- Roundtrip fidelity is rarely perfect — some formatting loss is common
- Jerry's blockquote frontmatter is non-standard and may not parse natively in any library
- Template placeholder syntax (`{{VAR}}`) may conflict with some parsers
- Build-from-scratch sounds expensive but Jerry's markdown subset may be small enough to be tractable

---

## Related Items

- Parent: [FEAT-001: AST Strategy Evaluation & Library Selection](../FEAT-001-ast-strategy.md)
- Informs: [SPIKE-002: AST-First Architecture Feasibility](../SPIKE-002-feasibility/SPIKE-002-feasibility.md)
- Related: `.context/templates/` — Template files define the markdown schemas
- Related: `skills/worktracker/rules/` — Worktracker rules define structural expectations

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-02-19 | pending | Spike defined. 7-step research approach with weighted evaluation framework. 12h timebox. |
