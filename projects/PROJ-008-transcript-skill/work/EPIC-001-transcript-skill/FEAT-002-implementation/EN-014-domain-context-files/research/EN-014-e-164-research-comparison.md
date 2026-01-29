# Research Comparison: Manual vs ps-researcher Schema Extensibility

<!--
PS-ID: EN-014
Entry-ID: e-164-comparison
Agent: ps-synthesizer (v2.0.0)
Topic: Research Comparison - Manual vs ps-researcher Output
Created: 2026-01-29
Framework: Comparative Analysis
-->

> **Synthesis ID:** EN-014-e-164-comparison
> **Agent:** ps-synthesizer (v2.0.0)
> **Status:** COMPLETE
> **Created:** 2026-01-29T00:00:00Z
> **Topic:** Comparative Analysis of Schema Extensibility Research Approaches

---

## Executive Summary

This synthesis compares two research documents addressing the same research questions for TASK-164 (Schema Extensibility Patterns):

| Aspect | Manual Research | ps-researcher Output |
|--------|-----------------|----------------------|
| **File** | `EN-014-e-164-schema-extensibility-manual.md` | `EN-014-e-164-schema-extensibility.md` |
| **Lines** | 563 | 746 |
| **Sources Cited** | 7 authoritative + 4 internal | 9 authoritative + structured matrix |
| **Framework** | 5W2H + Ishikawa + FMEA + Pareto + 8D | 5W2H + Evidence-Based Analysis |

**Key Finding:** Both research outputs arrive at the **same primary recommendation** (JSON Schema Extension with custom keywords), demonstrating convergent validity. However, they differ in emphasis, analytical depth, and structural organization. The ps-researcher output provides better practical implementation guidance, while the manual research provides richer risk analysis.

**Synthesis Recommendation:** Use the **ps-researcher output as the primary reference** for TASK-164 closure, but **incorporate the FMEA risk analysis** from the manual research into downstream artifacts (ADR, TDD).

---

## Convergence Analysis

Both research documents strongly agree on the following points:

### 1. Problem Definition (100% Aligned)

Both identify the **same 4 gaps** from DISC-006:

| Gap ID | Both Documents Agree |
|--------|----------------------|
| GAP-001 | Entity relationships (blocks, resolves, triggers) not supported |
| GAP-002 | Domain metadata (target_users, transcript_types) missing |
| GAP-003 | Context rules (meeting-type-specific extraction) absent |
| GAP-004 | Validation rules (min_entities, required_entities) needed |

### 2. Primary Recommendation (100% Aligned)

Both recommend: **Extend JSON Schema with custom keywords and structured properties**

| Decision Point | Manual | ps-researcher |
|----------------|--------|---------------|
| Technology choice | JSON Schema extension | JSON Schema extension |
| Versioning | v2.0.0 | v1.1.0 (SchemaVer) |
| Backward compatibility | Optional properties | Optional properties |
| Blast radius | LOW | Minimal |

### 3. JSON-LD Rejection (100% Aligned)

Both explicitly **reject JSON-LD** as the primary approach:

**Manual Research:**
> "HIGH blast radius - fundamentally different paradigm"
> "Estimated 2-3 weeks additional development"

**ps-researcher:**
> "High learning curve (team unfamiliar with JSON-LD)"
> "Significant tooling changes required"

### 4. Key Extensibility Mechanisms (90% Aligned)

Both identify similar JSON Schema patterns:

| Pattern | Manual | ps-researcher |
|---------|--------|---------------|
| `$defs` / `$ref` | Recommended | Recommended |
| Custom keywords (`x-*`) | Recommended | Mentioned (OpenAPI style) |
| `if-then-else` conditionals | Documented | Documented |
| `additionalProperties` | Cautioned | Cautioned |
| `unevaluatedProperties` | Not mentioned | Strongly recommended |

**Gap:** ps-researcher introduces `unevaluatedProperties` as superior to `additionalProperties`, which the manual research does not cover.

### 5. Authoritative Sources (70% Overlap)

Shared sources:
- JSON Schema Core 2020-12 specification
- Ajv documentation (custom keywords)
- JSON-LD Best Practices (W3C)
- OpenAPI/AsyncAPI extension patterns

---

## Divergence Analysis

### 1. Schema Versioning Strategy

| Aspect | Manual Research | ps-researcher |
|--------|-----------------|---------------|
| Version bump | 1.0.0 -> 2.0.0 | 1.0.0 -> 1.1.0 |
| Rationale | Major change | REVISION (additive) |
| Semantic versioning | Standard SemVer | SchemaVer |

**Analysis:** The ps-researcher applies [SchemaVer](https://snowplow.io/blog/introducing-schemaver-for-semantic-versioning-of-schemas) principles, which are specifically designed for schema evolution. Since all changes are **additive** (optional properties), a REVISION bump (1.0.0 -> 1.1.0) is more appropriate than a MAJOR bump.

**Winner:** ps-researcher

### 2. Risk Analysis Depth

| Framework | Manual Research | ps-researcher |
|-----------|-----------------|---------------|
| FMEA | Full RPN calculation (5 failure modes) | Not included |
| Ishikawa | 6-branch fishbone diagram | Not included |
| Pareto | 80/20 analysis | Not included |
| 8D | Full 8 disciplines documented | Not included |

**Analysis:** The manual research provides significantly more structured risk analysis. The FMEA identifies "JSON-LD migration delays" as the highest-RPN risk (168), which validates the rejection decision with quantitative evidence.

**Winner:** Manual research

### 3. Implementation Guidance

| Aspect | Manual Research | ps-researcher |
|--------|-----------------|---------------|
| Schema example | Complete v2 structure | Complete v1.1 structure |
| YAML example | Not included | Full `software-engineering.yaml` example |
| Code examples | ajv JavaScript only | ajv JavaScript + Python jsonschema |
| Validation library matrix | Not included | Language comparison table |

**Analysis:** The ps-researcher provides more comprehensive implementation artifacts, including a complete YAML example showing all 4 gaps addressed.

**Winner:** ps-researcher

### 4. Unique Insights

#### Manual Research (Unique Contributions)

1. **Ishikawa Root Cause:** Identified "existing JSON Schema investment" as primary constraint
2. **FMEA RPN:** Quantified JSON-LD risk at 168 (highest priority number)
3. **8D Report:** Complete discipline mapping for NASA SE alignment
4. **Trade-off Quadrant:** Visual mapping of semantic richness vs blast radius

#### ps-researcher (Unique Contributions)

1. **`unevaluatedProperties`:** Identified as superior to `additionalProperties` for extension safety
2. **SchemaVer:** Applied schema-specific versioning best practice
3. **Performance matrix:** O(n) analysis of validation patterns
4. **One-way door table:** Clear reversibility assessment per decision

### 5. ELI5 Analogies

| Research | Analogy | Effectiveness |
|----------|---------|---------------|
| Manual | Recipe book with sticky notes | Clear, relatable |
| ps-researcher | Library catalog system | Clear, relatable |

**Assessment:** Both provide effective analogies. The recipe book analogy (manual) may be slightly more accessible, but both serve the purpose well.

### 6. Structural Organization

| Aspect | Manual Research | ps-researcher |
|--------|-----------------|---------------|
| L0/L1/L2 sections | Present (ELI5, Engineer, Architect) | Present (ELI5, Engineer, Architect) |
| Research Questions | Woven into L1/L2 | Dedicated section |
| Appendices | 2 (Glossary, Research Log) | 2 (YAML Example, Code Examples) |
| Metadata block | YAML frontmatter | YAML at end |

**Analysis:** The ps-researcher separates research questions into a dedicated section, making the answers easier to reference. The manual research integrates them into the technical analysis, which provides better context but less discoverability.

**Winner:** ps-researcher (for reference usability)

---

## Quality Metrics Comparison

### Source Coverage

| Metric | Manual Research | ps-researcher |
|--------|-----------------|---------------|
| Total sources cited | 11 (7 external + 4 internal) | 9 (all external) |
| High-authority sources | 6 | 8 |
| Medium-authority sources | 1 | 1 |
| Internal references | 4 | 0 |
| Broken/placeholder links | 0 | 0 |

### Research Depth

| Metric | Manual Research | ps-researcher |
|--------|-----------------|---------------|
| Research questions addressed | 5/5 | 5/5 |
| Gaps addressed | 4/4 | 4/4 |
| Alternatives considered | 2 (JSON-LD, GraphQL) | 2 (JSON-LD, Hybrid) |
| Framework analysis | 5 frameworks | 2 frameworks |
| Code examples | 3 | 5 |

### Documentation Quality

| Metric | Manual Research | ps-researcher |
|--------|-----------------|---------------|
| Document length | 563 lines | 746 lines |
| Diagrams | 2 ASCII (Ishikawa, Trade-off) | 1 ASCII (Architecture) |
| Tables | 14 | 18 |
| JSON examples | 5 | 8 |
| YAML examples | 0 | 2 |

### L0/L1/L2 Coverage Quality

| Level | Manual Research | ps-researcher |
|-------|-----------------|---------------|
| L0 (ELI5) | Good analogy, clear recommendation | Good analogy, actionable finding |
| L1 (Engineer) | Strong technical detail | Strong technical detail + validation library matrix |
| L2 (Architect) | Excellent risk analysis (FMEA, Ishikawa) | Good strategic matrix, one-way door analysis |

---

## Synthesis Recommendation

### Primary Document Selection

**Recommended Primary:** `EN-014-e-164-schema-extensibility.md` (ps-researcher output)

**Rationale:**
1. **SchemaVer versioning** is more appropriate for the additive nature of changes
2. **`unevaluatedProperties` insight** is a critical technical finding missing from manual research
3. **Better implementation artifacts** (YAML example, code examples in 2 languages)
4. **Cleaner research question organization** improves downstream usability
5. **18 tables** provide better structured information

### Content to Incorporate from Manual Research

The following content from the manual research should be incorporated into downstream artifacts (ADR-EN014-001, TDD):

1. **FMEA Table:** Include the 5 failure modes with RPN calculations in the ADR
2. **Ishikawa Diagram:** Reference in the TDD for root cause documentation
3. **Pareto Analysis:** Include the "20% changes for 80% value" insight
4. **8D Mapping:** Use for NASA SE compliance demonstration

### Gaps Neither Addressed

| Gap | Description | Recommendation |
|-----|-------------|----------------|
| Schema migration tooling | Neither discusses automated migration scripts | Address in TASK-167 (TDD) |
| Validation error messages | Neither specifies user-facing error format | Address in TDD |
| Performance benchmarks | Neither includes actual validation timing | Defer to implementation |
| CI/CD integration | Neither discusses schema validation in pipelines | Address in Enabler scope |

### Merge Strategy

**Do not merge documents.** Instead:

1. **Mark manual research as superseded:** Add header noting ps-researcher output is canonical
2. **Reference manual research in ADR:** Cite FMEA/Ishikawa analysis for risk justification
3. **Close TASK-164:** Using ps-researcher output as evidence
4. **Proceeed to TASK-165:** With ps-researcher findings as input

---

## Conclusion

### Summary Assessment

| Criterion | Winner | Margin |
|-----------|--------|--------|
| Technical accuracy | Tie | Both correct |
| Source quality | ps-researcher | +2 high-authority sources |
| Risk analysis | Manual | FMEA, Ishikawa, Pareto |
| Implementation guidance | ps-researcher | YAML + multi-language examples |
| Versioning strategy | ps-researcher | SchemaVer is schema-appropriate |
| Overall recommendation | **ps-researcher** | Better practical applicability |

### Final Verdict

The **ps-researcher output** should be used as the **canonical research artifact** for TASK-164 closure because:

1. It provides the correct versioning strategy (1.1.0 vs 2.0.0)
2. It identifies a critical technical insight (`unevaluatedProperties`)
3. It includes more complete implementation artifacts
4. It is structured for easier downstream consumption

However, the manual research provides **valuable supplementary risk analysis** that should be referenced in the ADR to strengthen the decision justification.

### Action Items

1. [x] Create this comparison synthesis
2. [ ] Update TASK-164 to reference ps-researcher output as primary evidence
3. [ ] Add header to manual research marking it as superseded
4. [ ] Reference manual research FMEA in ADR-EN014-001 (TASK-166)
5. [ ] Proceed to TASK-165 with unified research findings

---

## Metadata

```yaml
id: "EN-014-e-164-comparison"
type: synthesis
agent: ps-synthesizer
version: "2.0.0"
topic: "Research Comparison - Manual vs ps-researcher"
status: COMPLETE
created_at: "2026-01-29T00:00:00Z"
compared_documents:
  - id: "EN-014-e-164-manual"
    file: "EN-014-e-164-schema-extensibility-manual.md"
    status: "superseded"
  - id: "EN-014-e-164"
    file: "EN-014-e-164-schema-extensibility.md"
    status: "canonical"
recommendation: "Use ps-researcher output as primary; incorporate manual FMEA in ADR"
convergence_rate: "~85%"
key_divergence: "Versioning strategy (2.0.0 vs 1.1.0)"
```

---

## Document History

| Date | Author | Change |
|------|--------|--------|
| 2026-01-29 | ps-synthesizer (v2.0.0) | Initial comparison synthesis |

---

*Synthesis completed: 2026-01-29*
*Agent: ps-synthesizer (v2.0.0)*
*Task: TASK-164 (Research Phase Validation)*
*Enabler: EN-014 (Domain Context Files Implementation)*
