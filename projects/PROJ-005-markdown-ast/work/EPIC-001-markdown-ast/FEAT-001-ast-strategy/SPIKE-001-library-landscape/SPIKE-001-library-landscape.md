# SPIKE-001: Python Markdown AST Library Landscape

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

7 Python markdown AST libraries evaluated (markdown-it-py, mistletoe, marko, mistune, mdformat, pyromark, commonmark.py) plus MyST-Parser as supplementary. Research conducted via Web Search and Context7 with 35 citations. Full findings in orchestration artifacts.

### Library Evaluations

See `orchestration/spike-eval-20260219-001/ps/phase-1-research/ps-researcher-001/library-landscape-research.md` for detailed per-library evaluations.

### Feature Matrix

See `orchestration/spike-eval-20260219-001/ps/phase-2-analysis/ps-analyst-001/library-feature-matrix.md` for weighted composite scores:

| Library | Composite Score |
|---------|----------------|
| markdown-it-py + mdformat | 4.20 |
| mistletoe | 3.75 |
| marko | 3.40 |
| mdformat (standalone) | 3.35 |
| mistune | 3.10 |
| pyromark | 1.75 |
| commonmark.py | 1.55 |

### Build-from-Scratch Assessment

Build-from-scratch estimated at 2,380-3,320 LOC. Not recommended — existing library with extensions is significantly lower effort (~470 LOC for recommended stack).

### Evidence/References

35 citations across research artifacts. See phase-1-research for full reference list with URLs, version numbers, and access dates.

---

## Recommendation

### Decision

**ADOPT:** markdown-it-py v4.0.0 + mdformat v1.0.0 — highest composite score (4.20), best extension API, roundtrip fidelity via mdformat, active maintenance.

### Recommended Actions

1. Proceed to SPIKE-002 feasibility assessment (completed — GO decision)
2. Begin FEAT-001 implementation with R-01 proof-of-concept validation
3. Implement 4 custom extensions (~470 LOC): blockquote frontmatter parser, navigation table handler, template placeholder preserver, L2-REINJECT comment accessor

### Follow-up Work Items

| Type | Title | Priority |
|------|-------|----------|
| SPIKE-002 | AST-First Architecture Feasibility Assessment | high (completed) |
| Story | R-01 proof-of-concept: mdformat blockquote frontmatter write-back | high |
| Story | Implement markdown-it-py custom extensions | high |

### Risks/Considerations

- Roundtrip fidelity requires mdformat — markdown-it-py alone doesn't render
- Jerry's blockquote frontmatter requires custom extension (not natively supported)
- Template placeholder syntax (`{{VAR}}`) needs preservation through parse/render cycle
- mdformat code renderer may reflow content — needs validation (R-01)

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
| 2026-02-19 | completed | Spike completed via orchestration `spike-eval-20260219-001`. 7 libraries evaluated, 35 citations. Recommendation: markdown-it-py + mdformat (composite 4.20). QG1 passed at 0.96. |
