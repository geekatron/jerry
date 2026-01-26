# FEAT-001:BUG-001: Enablers and ADRs Not Using Repository Templates

> **Type:** bug
> **Status:** open
> **Priority:** high
> **Impact:** high
> **Created:** 2026-01-26T12:00:00Z
> **Parent:** FEAT-001
> **Owner:** Claude
> **Severity:** medium
> **Category:** structural-gap

---

## Summary

All Enabler files (EN-001 through EN-013) and planned ADRs are NOT using the proper templates defined in the repository:

1. **Enabler Template:** `.context/templates/worktracker/ENABLER.md` (550+ lines)
2. **ADR Template:** `docs/knowledge/exemplars/templates/adr.md` (190 lines, Michael Nygard format with PS integration)

Current enabler files use a simplified format that is missing many required sections.

---

## Root Cause

Claude did not check for existing templates before creating work items. Instead of using the comprehensive templates already defined in the repository, simplified ad-hoc formats were used.

---

## Affected Files

### Enabler Files (All Non-Compliant)
- `EN-001-market-analysis/EN-001-market-analysis.md`
- `EN-002-technical-standards/EN-002-technical-standards.md`
- `EN-003-requirements-synthesis/EN-003-requirements-synthesis.md`
- `EN-004-architecture-decisions/EN-004-architecture-decisions.md`
- `EN-005-design-documentation/EN-005-design-documentation.md`
- `EN-006-context-injection-design/EN-006-context-injection-design.md`
- `EN-007-vtt-parser/EN-007-vtt-parser.md`
- `EN-008-entity-extraction/EN-008-entity-extraction.md`
- `EN-009-mindmap-generator/EN-009-mindmap-generator.md`
- `EN-010-artifact-packaging/EN-010-artifact-packaging.md`
- `EN-011-worktracker-integration/EN-011-worktracker-integration.md`
- `EN-012-skill-interface/EN-012-skill-interface.md`
- `EN-013-context-injection/EN-013-context-injection.md`

### ADR Files (Planned - Not Yet Created)
- All ADRs in EN-004 should use `docs/knowledge/exemplars/templates/adr.md`

---

## Missing Sections in Current Enablers

Compared to `.context/templates/worktracker/ENABLER.md`:

| Section | In Template | In Current Files |
|---------|-------------|------------------|
| Enabler Type field | ✅ | ❌ |
| Frontmatter YAML block | ✅ | ❌ |
| Problem Statement | ✅ | ❌ |
| Business Value | ✅ | ❌ |
| Technical Approach | ✅ | ❌ |
| NFRs Addressed | ✅ | ❌ |
| Evidence section | ✅ | ❌ |
| Implementation Plan | ✅ | ❌ |
| Risks and Mitigations | ✅ | ❌ |
| State Machine Reference | ✅ | ❌ |
| Containment Rules | ✅ | ❌ |
| Invariants | ✅ | ❌ |
| Architecture Runway Impact | ✅ | ❌ |

---

## Templates That Should Be Used

### Worktracker Templates (`.context/templates/worktracker/`)

| Template | For | Location |
|----------|-----|----------|
| ENABLER.md | All EN-* files | `.context/templates/worktracker/ENABLER.md` |
| TASK.md | All TASK-* files | `.context/templates/worktracker/TASK.md` |
| BUG.md | All BUG-* files | `.context/templates/worktracker/BUG.md` |
| DISCOVERY.md | All DISC-* files | `.context/templates/worktracker/DISCOVERY.md` |
| DECISION.md | All DEC-* files | `.context/templates/worktracker/DECISION.md` |
| SPIKE.md | All SPIKE-* files | `.context/templates/worktracker/SPIKE.md` |
| EPIC.md | All EPIC-* files | `.context/templates/worktracker/EPIC.md` |
| FEATURE.md | All FEAT-* files | `.context/templates/worktracker/FEATURE.md` |
| STORY.md | All STORY-* files | `.context/templates/worktracker/STORY.md` |
| IMPEDIMENT.md | All IMP-* files | `.context/templates/worktracker/IMPEDIMENT.md` |

### Problem-Solving Templates (`docs/knowledge/exemplars/templates/`)

| Template | For | Location |
|----------|-----|----------|
| adr.md | Architecture Decision Records | `docs/knowledge/exemplars/templates/adr.md` |
| research.md | Research artifacts | `docs/knowledge/exemplars/templates/research.md` |
| analysis.md | Analysis artifacts | `docs/knowledge/exemplars/templates/analysis.md` |
| synthesis.md | Synthesis artifacts | `docs/knowledge/exemplars/templates/synthesis.md` |
| review.md | Review artifacts | `docs/knowledge/exemplars/templates/review.md` |
| investigation.md | Investigation artifacts | `docs/knowledge/exemplars/templates/investigation.md` |

---

## Recommended Fix

### Option A: Incremental Update (Recommended)
Update files as they become active:
- When EN-004 starts, update to full Enabler template AND reference ADR template
- When creating ADRs, use `docs/knowledge/exemplars/templates/adr.md`
- Update completed enablers (EN-001, EN-002, EN-003) during Phase 3

### Option B: Batch Update
Update all 13 enabler files at once to match template.
- Risk: Large change, potential for errors
- Benefit: Consistency immediately

---

## Acceptance Criteria

- [ ] EN-004 references `docs/knowledge/exemplars/templates/adr.md` explicitly
- [ ] All new ADRs created using the proper template
- [ ] All enablers updated to include `Enabler Type` field
- [ ] Documentation updated to remind Claude to check templates first

---

## Related Items

- **Parent:** [FEAT-001: Analysis & Design](./FEAT-001-analysis-design.md)
- **Related Discovery:** None
- **Related Task:** #44 (Create standalone task files for EN-003)

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-01-26 | Claude | open | Bug identified by user review |

---

## Lessons Learned

**ALWAYS check for existing templates before creating work items:**
1. `.context/templates/worktracker/` for work tracker entities
2. `docs/knowledge/exemplars/templates/` for problem-solving artifacts
