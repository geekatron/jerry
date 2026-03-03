# Diataxis Audit: diataxis-framework.md

> **File:** `docs/knowledge/diataxis-framework.md`
> **Date:** 2026-02-27
> **Method:** Manual diataxis classification using Section 3/4 heuristics from `skills/diataxis/rules/diataxis-standards.md`

## Classification

**Primary quadrant:** Explanation (understanding-oriented knowledge about the framework)
**Secondary content:** Reference (quality criteria tables, language convention tables)
**Verdict:** NEEDS REVISION -- reference tables mixed into explanation document

## Findings

| # | Type | Severity | Location | Description |
|---|------|----------|----------|-------------|
| 1 | Missing: E-06 scope boundary | Minor | Document level | No explicit scope statement bounding coverage. |
| 2 | QUADRANT-MIX: reference in explanation | Minor | Quality Criteria tables (lines 58-66, 95-103, 128-135, 158-166) | Structured specification tables are reference content. In an explanation doc, criteria should be discussed discursively, with the specification tables linked via cross-reference. |
| 3 | QUADRANT-MIX: reference in explanation | Minor | Language Conventions (lines 80-83, 113-116, 145-147, 177-179) | Prescriptive convention lists are reference content. |
| 4 | Missing: E-04 alternative perspectives | Minor | Document level | No section acknowledging alternative documentation frameworks or perspectives. |
| 5 | EAP-01: Instructional creep | Minor | Writing Principles (lines 70-77, 106-111) | Numbered lists with imperative verbs ("Show the endpoint upfront", "Write around human needs") are procedural instructions, not discursive explanation. |
| 6 | Missing: cross-references | Minor | Document level | No Related section linking to the diataxis standards (reference quadrant) or templates (how-to quadrant). |

## Recommendations

1. **Add scope boundary** per E-06
2. **Add Alternative Perspectives section** per E-04 -- mention other documentation frameworks (DITA, topic-based authoring)
3. **Add Related section** with cross-quadrant links to standards and templates
4. **Note**: Quality criteria tables and Writing Principles are acceptable in a knowledge document since this serves as foundational research, not pure explanation output. The improvement here is adding context to acknowledge the mixing.

## Improvements Applied

- Added scope boundary statement
- Added Alternative Perspectives section discussing other frameworks
- Added Related section with cross-quadrant links
