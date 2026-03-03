# Diataxis Audit: skill-development-best-practices.md

> **File:** `docs/knowledge/skill-development-best-practices.md`
> **Date:** 2026-02-27
> **Method:** Manual diataxis classification using Section 3/4 heuristics from `skills/diataxis/rules/diataxis-standards.md`

## Classification

**Primary quadrant:** Reference (structured field tables, specification-oriented content)
**Secondary content:** How-to (registration steps, checklists), Explanation (design rationale)
**Verdict:** NEEDS REVISION -- multi-quadrant mixing throughout

## Findings

| # | Type | Severity | Location | Description |
|---|------|----------|----------|-------------|
| 1 | QUADRANT-MIX: how-to in reference | Major | Registration Requirements (lines 346-353) | Imperative instructions ("MUST be registered in...") embedded in what is otherwise a reference document. This is a how-to guide section. |
| 2 | QUADRANT-MIX: explanation in reference | Minor | Progressive Disclosure (lines 37-45) | "Design implication" paragraph explains *why* to structure content a certain way -- explanation content in a reference-oriented doc. |
| 3 | QUADRANT-MIX: how-to in reference | Major | Gap Analysis Template (lines 399-432) | Template usage instructions ("Use this to evaluate...") are procedural how-to content. |
| 4 | QUADRANT-MIX: explanation in reference | Minor | File Reference Rules (lines 309-318) | "Rationale:" paragraph explains *why* full paths are needed -- explanation content. |
| 5 | QUADRANT-MIX: how-to in reference | Minor | Pre-Ship Checklist (lines 357-394) | Checklist format is procedural (action-oriented), better suited to a how-to guide. |
| 6 | Anti-pattern: RAP-03 | Minor | Description Field section (lines 72-91) | Good/Bad examples with narrative explanation -- reference should describe, not teach. |
| 7 | Missing: E-06 scope boundary | Minor | Document level | No explicit scope statement bounding what this document covers and excludes. |

## Recommendations

1. **Add scope boundary** at document top per E-06
2. **Add quadrant classification comments** to sections that mix quadrants, guiding future editors
3. **Add cross-reference Related section** linking to the how-to guide (howto-register-skill) and the diataxis standards (reference)
4. **Mark how-to sections** with comments noting the content belongs in a companion how-to guide

## Improvements Applied

- Added scope boundary statement
- Added diataxis quadrant classification comments to mixed sections
- Added Related section with cross-quadrant links
