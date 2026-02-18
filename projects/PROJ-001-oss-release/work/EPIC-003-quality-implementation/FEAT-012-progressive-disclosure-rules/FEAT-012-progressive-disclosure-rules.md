# FEAT-012: Progressive Disclosure Rules Architecture

<!--
TEMPLATE: Feature
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.4
CREATED: 2026-02-16 (Claude)
PURPOSE: Restructure .context/rules/ into tiered progressive disclosure architecture
-->

> **Type:** feature
> **Status:** done
> **Priority:** high
> **Impact:** high
> **Created:** 2026-02-16
> **Due:** ---
> **Completed:** 2026-02-17
> **Parent:** EPIC-003
> **Owner:** —
> **Target Sprint:** —

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Feature overview and value proposition |
| [Benefit Hypothesis](#benefit-hypothesis) | Expected benefits from restructuring |
| [Acceptance Criteria](#acceptance-criteria) | Definition of done and verification criteria |
| [MVP Definition](#mvp-definition) | In-scope vs future work |
| [Children (Stories/Enablers)](#children-storiesenablers) | Enabler inventory and tracking |
| [Progress Summary](#progress-summary) | Overall feature progress |
| [Related Items](#related-items) | Dependencies and hierarchy |
| [History](#history) | Status changes and key events |

---

## Summary

Restructure `.context/rules/` files from a naive token-optimized format (enforcement-only, all context deleted) into a progressive disclosure architecture with three tiers: lean enforcement rules (auto-loaded), rich companion guides (on-demand), and standalone code patterns (on-demand). Apply path scoping to Python-specific rules. Ensure bootstrap script excludes guides from auto-loading.

**Value Proposition:**
- Restores rich educational context (explanations, rationale, code examples) that was naively deleted during EN-702 optimization
- Preserves token efficiency via tiered loading — enforcement rules stay lean, guides load on-demand
- Serves both audiences: Claude gets enforcement rules at session start + rich context when needed; humans get complete documentation
- Applies path scoping so Python-specific rules only load when editing Python files

---

## Benefit Hypothesis

**We believe that** restructuring rules into a progressive disclosure architecture (enforcement + guides + patterns)

**Will result in** improved Claude behavioral compliance without increasing session-start token costs, while restoring the human-readable documentation that was lost during optimization

**We will know we have succeeded when:**
- All 24 HARD rules preserved in lean enforcement files (~5-6K tokens auto-loaded)
- All deleted content (explanations, rationale, code examples) restored in companion guide files
- Every rule file explicitly references its companion guide(s)
- Python-specific rules use path scoping (only load when editing .py files)
- Bootstrap script does NOT symlink `.context/guides/` to `.claude/guides/`
- E2E tests verify cross-reference completeness and guide fidelity
- No regression: every piece of content from pre-optimization rules exists in the new structure

---

## Acceptance Criteria

### Definition of Done

- [ ] All 10 rule files restructured to enforcement-only skeletons
- [ ] All companion guide files created in `.context/guides/` with navigation tables
- [ ] All code pattern files extracted to `.context/patterns/`
- [ ] Path scoping applied to Python-specific rule files
- [ ] Bootstrap script verified to exclude `.context/guides/`
- [ ] E2E tests validate cross-references, fidelity, and completeness
- [ ] All acceptance criteria verified via creator-critic-revision cycle
- [ ] Quality gate passed (>= 0.92)

### Functional Criteria

| # | Criterion | Verified |
|---|-----------|----------|
| AC-1 | All 24 HARD rules (H-01 through H-24) present in enforcement files | [ ] |
| AC-2 | All MEDIUM/SOFT guidance preserved in enforcement files or guides | [ ] |
| AC-3 | Every enforcement file has explicit companion guide references | [ ] |
| AC-4 | All companion guides have navigation tables (H-23/H-24) | [ ] |
| AC-5 | All code examples from original rules exist in `.context/patterns/` | [ ] |
| AC-6 | Python-specific rules use `paths` frontmatter for conditional loading | [ ] |
| AC-7 | `.context/guides/` NOT symlinked by bootstrap script | [ ] |
| AC-8 | Content restored from git history matches original pre-optimization state | [ ] |

### Non-Functional Criteria

| # | Criterion | Verified |
|---|-----------|----------|
| NFC-1 | Auto-loaded enforcement files total <= 6K tokens | [ ] |
| NFC-2 | Guide files load in < 2s when explicitly read | [ ] |
| NFC-3 | All existing tests pass (`uv run pytest`) | [ ] |
| NFC-4 | AE-002 compliance: touches `.context/rules/` = C3 minimum criticality | [ ] |

---

## MVP Definition

### In Scope (MVP)

- Strategy 1: Progressive Disclosure — enforcement rules + guides + patterns
- Strategy 2: Path Scoping — Python-specific rules with `paths` frontmatter
- Strategy 3: Companion Files — explicit references between enforcement and guides
- Bootstrap exclusion — `.context/guides/` not auto-loaded
- Fidelity verification — E2E tests for completeness and cross-references

### Out of Scope (Future)

- Strategy 4: Skill-embedded context (earmarked for FEAT-007)
- A/B testing of rule effectiveness (future empirical evaluation)
- Context rot regression testing (separate evaluation initiative)

---

## Children (Stories/Enablers)

### Story/Enabler Inventory

| ID | Type | Title | Status | Priority | Effort |
|----|------|-------|--------|----------|--------|
| EN-901 | Enabler | Rules File Thinning | done (superseded by EN-701) | high | 5 |
| EN-902 | Enabler | Companion Guide Files | done | high | 8 |
| EN-903 | Enabler | Code Pattern Extraction | done | medium | 5 |
| EN-904 | Enabler | Path Scoping Implementation | done | medium | 3 |
| EN-905 | Enabler | Bootstrap Exclusion & Validation | done | high | 3 |
| EN-906 | Enabler | Fidelity Verification & Cross-Reference Testing | done | critical | 5 |

### Work Item Links

- [EN-901: Rules File Thinning](./EN-901-rules-thinning/EN-901-rules-thinning.md)
- [EN-902: Companion Guide Files](./EN-902-companion-guides/EN-902-companion-guides.md)
- [EN-903: Code Pattern Extraction](./EN-903-pattern-extraction/EN-903-pattern-extraction.md)
- [EN-904: Path Scoping Implementation](./EN-904-path-scoping/EN-904-path-scoping.md)
- [EN-905: Bootstrap Exclusion & Validation](./EN-905-bootstrap-exclusion/EN-905-bootstrap-exclusion.md)
- [EN-906: Fidelity Verification & Cross-Reference Testing](./EN-906-fidelity-verification/EN-906-fidelity-verification.md)

---

## Progress Summary

### Status Overview

```
+------------------------------------------------------------------+
|                   FEATURE PROGRESS TRACKER                        |
+------------------------------------------------------------------+
| Enablers:  [####################] 100% (6/6 completed)            |
| Effort:    [####################] 100% (29/29 points)             |
+------------------------------------------------------------------+
| Overall:   [####################] 100%                             |
+------------------------------------------------------------------+
```

### Progress Metrics

| Metric | Value |
|--------|-------|
| **Total Enablers** | 6 |
| **Completed Enablers** | 6 |
| **Total Effort (points)** | 29 |
| **Completed Effort** | 29 |
| **Completion %** | 100% |

---

## Related Items

### Hierarchy

- **Parent Epic:** [EPIC-003: Quality Framework Implementation](../EPIC-003-quality-implementation.md)

### Related Features

- [FEAT-008: Quality Framework Implementation](../FEAT-008-quality-framework-implementation/FEAT-008-quality-framework-implementation.md) — EN-701/EN-702 performed the original optimization that this feature remediates
- [FEAT-007: Advanced Adversarial Capabilities](../FEAT-007-advanced-adversarial-capabilities/FEAT-007-advanced-adversarial-capabilities.md) — Strategy 4 (skill-embedded context) earmarked for this feature

### Dependencies

| Dependency Type | Item | Description |
|----------------|------|-------------|
| Depends On | EN-702 (FEAT-008) | Git history of pre-optimization rules is the source for content restoration |
| Informs | FEAT-007 | Strategy 4 builds on the tiered architecture established here |

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-02-16 | Claude | pending | Feature created. Addresses naive token optimization from EN-702 that deleted educational content. Implements Strategies 1+2+3 (Progressive Disclosure + Path Scoping + Companion Files). AE-002 auto-escalation: C3 minimum (touches .context/rules/). |
| 2026-02-16 | Claude | pending | Moved from EPIC-002 to EPIC-003. FEAT-012 is implementation work; EPIC-002 is research/design, EPIC-003 is implementation. EN-901 (Rules File Thinning) partially superseded by EN-701 — remaining enablers EN-902–906 are new work. |
| 2026-02-17 | Claude | done | Retroactive closure: all 6 enablers verified as delivered. EN-902: 5 guides (5,002 lines). EN-903: 49 pattern files (6 .py + 41 .md + README + CATALOG). EN-904: 3 rule files path-scoped. EN-905: bootstrap excludes guides. EN-906: 21/21 E2E tests pass (`test_progressive_disclosure_crossrefs.py` + `test_bootstrap_guides_exclusion.py`). |

---

## System Mapping

| System | Mapping |
|--------|---------|
| **Azure DevOps** | Feature |
| **SAFe** | Feature (Program Backlog) |
| **JIRA** | Epic (or custom issue type) |
