# Adversarial Strategy Selection -- PROJ-012 Agent Optimization

**Criticality Level:** C3 (Significant)
**Date:** 2026-02-26
**Deliverable:** Governance Migration (single-file agent definition architecture)
**Status:** Strategy set recommended

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [C3 Criticality Requirements](#c3-criticality-requirements) | Required and optional strategies for C3 deliverables |
| [Deliverable Summary](#deliverable-summary) | Scope and impact of PROJ-012 governance migration |
| [Recommended Strategy Set](#recommended-strategy-set) | Selected strategies and execution rationale |
| [Execution Plan](#execution-plan) | Ordered strategy sequence with grouping |
| [H-16 Steelman Ordering](#h-16-steelman-ordering) | Constitutional compliance with steelman-before-critique rule |
| [Success Criteria](#success-criteria) | Quality gate targets and post-completion verification |

---

## C3 Criticality Requirements

Per `.context/rules/quality-enforcement.md` [Criticality Levels](#criticality-levels) section:

**C3 (Significant) scope:**
- Work item affects >1 day to reverse
- Touches >10 files
- Includes API changes or data structure modifications
- Requires all enforcement tiers (HARD + MEDIUM + SOFT)

**C3 required strategy set (per quality-enforcement.md table):**
- **C2 baseline** (inherited): S-007, S-002, S-014
- **C3 additions:** S-004, S-012, S-013
- **Required total:** S-007, S-002, S-014, S-004, S-012, S-013 (6 strategies)

**C3 optional strategies** (may be added per judgment):
- S-001 (Red Team Analysis)
- S-003 (Steelman Technique)
- S-010 (Self-Refine)
- S-011 (Chain-of-Verification)

---

## Deliverable Summary

**Project:** PROJ-012 Agent Optimization
**Feature:** Governance Migration -- Single-File Agent Definition Architecture

### Scope

| Aspect | Details |
|--------|---------|
| Files Modified | 8 primary target files + 58 agent recompose outputs |
| Files Deleted | 58 `.governance.yaml` companion files (removed from compose output) |
| Files Created | 1 new domain service (`GovernanceSectionBuilder`) |
| Tests Passing | 527/527 (100%) |
| Lines Changed | ~2,500 (rule file update + service + adapter + handler) |
| API Changes | Single-file agent definition format (backward-incompatible deprecation of dual-file architecture) |

### Impact Classification

**Criticality indicators (C3 threshold):**
- ✓ Files touched: 66 (exceeds 10-file threshold)
- ✓ API change: Governance data format (moved from separate file to markdown body)
- ✓ Reversibility: Multi-day effort to revert (recreate 58 files, restore dual-file pipeline)
- ✓ Rule file change: `.context/rules/agent-development-standards.md` (AE-002 auto-C3 trigger)
- ✓ Governance impact: Schema deprecation, single-file architecture formalization

**Auto-escalation triggers met:**
- AE-002: Touches `.context/rules/agent-development-standards.md` → Auto-C3

---

## Recommended Strategy Set

**Selection:** Full C3 required set + optional S-003 (Steelman) per H-16

| Strategy | ID | Score | Family | Rationale |
|----------|----|----|--------|-----------|
| Self-Refine | S-010 | 4.00 | Iterative | Foundational self-review; improves candidate pool before group evaluation |
| Steelman Technique | S-003 | 4.30 | Dialectical | Strengthens architectural reasoning before adversarial critique (H-16: MUST precede S-002) |
| Devil's Advocate | S-002 | 4.10 | Role-Based | Attacks assumptions in single-file design (governance XML embedding, schema deprecation) |
| Pre-Mortem Analysis | S-004 | 4.10 | Role-Based | Identifies failure modes in compose pipeline, governance preservation, backward compatibility |
| Constitutional AI Critique | S-007 | 4.15 | Iterative | Verifies P-003 (no subagents), P-020 (user authority in governance), P-022 (honest schema versioning) |
| Chain-of-Verification | S-011 | 3.75 | Structured | Validates governance data preservation across 58 agent recompositions |
| FMEA | S-012 | 3.75 | Structured | Systematic risk analysis: governance loss, XML injection, schema validation failures |
| Inversion Technique | S-013 | 4.25 | Structured | Reverse-engineer failure modes: "How would we lose governance data?" → mitigation checks |
| LLM-as-Judge | S-014 | 4.40 | Iterative | Final quality scoring against 6-dimension rubric (completeness, consistency, rigor, evidence, actionability, traceability) |

**Total selected:** 9 strategies (6 required + 3 optional)
**Excluded:** S-001 (Red Team not needed; no penetration/security angles), S-004+S-012 already provide risk analysis

---

## Execution Plan

**Strategy grouping per standard adversary framework:**

### Group A: Foundation (S-010)
**Self-Refine** — Agent reviews own governance migration work before external critique
- Verify all 58 agents recomposed successfully
- Check governance XML section completeness
- Scan for schema validation errors
- Estimate confidence: high (527/527 tests passing)

### Group B: Strengthening (S-003)
**Steelman Technique** — Strengthen the single-file architectural argument
- Best interpretation: XML embedding reduces complexity vs. companion files
- Single source of truth reduces sync inconsistencies
- Unified agent definition simplifies Claude Code loading
- Assess: Are there genuinely stronger interpretations than current design?

### Group C: Adversarial Attack (S-002, S-004)
**Devil's Advocate** — Attack the single-file design
- Governance data embedded in markdown body; can XML tags be properly escaped?
- Backward compatibility: old dual-file definitions now invalid (breaking change)
- Claim: single-file architecture is premature optimization without measurable benefit

**Pre-Mortem Analysis** — Simulate failure modes
- Failure 1: Governance XML not properly parsed → agents inherit wrong settings
- Failure 2: Schema migration incomplete → validation gaps
- Failure 3: Compose pipeline breaks on edge cases → incomplete recomposition

### Group D: Structural Validation (S-007, S-011)
**Constitutional AI Critique** — Verify governance principles
- P-003: No recursive delegation in governance data (validated)
- P-020: User authority in governance scope (validated)
- P-022: Honest schema deprecation messaging (validated)

**Chain-of-Verification** — Trace governance preservation
- Verify: 58 agents → XML sections generated → stored in definition body → readable by Claude Code
- Check: No governance data lost in recomposition
- Validate: All required governance fields present (version, tool_tier, identity, etc.)

### Group E: Risk Analysis (S-012, S-013)
**FMEA** — Failure modes and effects analysis
| Failure Mode | Cause | Effect | Severity | Recommended Action |
|---|---|---|---|---|
| Governance XML malformed | Manual governance.yaml creation errors | Agent inherits wrong settings | High | Add XML schema validation in GovernanceSectionBuilder |
| Schema version mismatch | Incomplete migration of v1.0 → v1.1 schema | Validation failures on older agents | Medium | Implement version auto-upgrade in PromptTransformer |
| Backward compat break | Dual-file architecture removed from compose | Old tooling fails silently | Medium | Document breaking change in CHANGELOG, migrate all consumers |
| Escape character bugs | XML special chars in governance data | Parse failures | Low | Unit test XML escape scenarios |

**Inversion Technique** — Reverse-engineer failure scenarios
- "How would we guarantee governance data loss?" → Implement anti-patterns (no validation)
- "How would we introduce schema inconsistencies?" → Skip version checks
- Inversions: Apply strict validation, enforce schema versioning, comprehensive test coverage

### Group F: Quality Scoring (S-014) — ALWAYS LAST
**LLM-as-Judge** — Apply 6-dimension rubric (FINAL)

| Dimension | Weight | Evaluation Criteria | Target Score |
|-----------|--------|-------------------|--------------|
| **Completeness** | 0.20 | All 8 target files modified. 58 agents recomposed. All required governance fields present. | 0.95+ |
| **Internal Consistency** | 0.20 | Governance data format consistent across all agents. Schema version aligned. XML escaping uniform. | 0.95+ |
| **Methodological Rigor** | 0.20 | Migration strategy justified. Pre-mortem analysis comprehensive. Test coverage adequate (527/527 passing). | 0.90+ |
| **Evidence Quality** | 0.15 | Test suite validates governance preservation. Recompose output auditable. Schema validation enforced. | 0.95+ |
| **Actionability** | 0.15 | Breaking change documented. Migration path clear. Fallback strategy defined. | 0.90+ |
| **Traceability** | 0.10 | Governance data traceable from source to agent definition. Deprecation timeline clear. | 0.95+ |

**Composite Quality Gate:** >= 0.92 required (H-13)
**Pass criterion:** Weighted average of dimension scores >= 0.92

---

## H-16 Steelman Ordering

Per `.context/rules/quality-enforcement.md` HARD Rule H-16:

> **H-16: Steelman (S-003) MUST be applied before Devil's Advocate (S-002). Canonical review pairing.**

**Implementation:**
- Group B (S-003 Steelman) executes BEFORE Group C (S-002 Devil's Advocate)
- Steelman output feeds directly to Devil's Advocate (strengthened claims for attack)
- This ordering prevents premature rejection of sound architectural decisions

---

## Success Criteria

### Quality Gate (H-13)

| Metric | Target | Verification |
|--------|--------|--------------|
| LLM-as-Judge composite score | >= 0.92 | Final S-014 scoring |
| All required dimensions | >= 0.90 each | Dimension-level rubric |
| Test pass rate | 100% (527/527) | pytest output |
| Governance preservation | 100% (58/58 agents) | Schema validation on all recomposed agents |
| No validation errors | 0 | GovernanceSectionBuilder test suite + PromptTransformer mapping tests |

### Post-Completion Verification (H-34 validation.post_completion_checks)

- [ ] All 58 agents validate against `agent-governance-v1.schema.json`
- [ ] Governance XML sections parse without errors in `.md` files
- [ ] Old dual-file architecture `.governance.yaml` files are not generated in compose output
- [ ] `agent-development-standards.md` v1.3.0 is readable by all tooling that consumes it
- [ ] CHANGELOG documents breaking change and migration path
- [ ] CI passes with updated schema deprecation notices

### Iteration Ceiling (RT-M-010)

Per `agent-routing-standards.md` iteration ceilings:
- **C3 iteration maximum:** 7 iterations (per criticality)
- **Plateau detection:** If quality score delta < 0.01 for 3 consecutive iterations, circuit breaker halts early

---

## References

| Source | Content | Location |
|--------|---------|----------|
| quality-enforcement.md | C3 criticality definition, required strategies, quality gate thresholds | `.context/rules/quality-enforcement.md` |
| quality-enforcement.md | H-16 steelman ordering rule, H-13 quality gate, H-14 revision cycle | `.context/rules/quality-enforcement.md` |
| agent-development-standards.md | v1.3.0 updates (H-34 compound rule), governance schema evolution | `.context/rules/agent-development-standards.md` |
| agent-routing-standards.md | Iteration ceilings (RT-M-010), plateau detection | `.context/rules/agent-routing-standards.md` |
| ADR-EPIC002-001 | Strategy selection, composite scores, family classifications | `docs/design/decisions/ADR-EPIC002-001.md` |

---

**Status:** READY FOR EXECUTION
**Next Step:** Invoke `/adversary` skill with strategy set S-010, S-003, S-002, S-004, S-007, S-011, S-012, S-013, S-014 in documented order.

*Generated by adv-selector agent*
*C3 governance escalation per AE-002*
