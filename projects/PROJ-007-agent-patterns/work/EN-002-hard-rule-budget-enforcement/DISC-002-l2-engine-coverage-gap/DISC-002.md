# EN-002:DISC-002: L2 Prompt Reinforcement Engine Coverage Gap

> **Type:** discovery
> **Status:** validated
> **Priority:** high
> **Impact:** high
> **Created:** 2026-02-21T22:00:00Z
> **Completed:** 2026-02-21T23:30:00Z
> **Parent:** EN-002
> **Owner:** Claude (PROJ-007 orchestrator)
> **Source:** Source code analysis + C4 adversary tournament

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Core finding |
| [Context](#context) | Background and research question |
| [Finding](#finding) | Engine limitation and L2 marker ecosystem |
| [Evidence](#evidence) | Source documentation |
| [Implications](#implications) | Impact on enforcement quality |
| [Relationships](#relationships) | Related work items |
| [Recommendations](#recommendations) | Actionable next steps |

---

## Summary

The L2 prompt reinforcement engine (`prompt_reinforcement_engine.py`) reads L2-REINJECT markers from `quality-enforcement.md` only — 8 markers covering 10 H-rules. However, 8 additional L2-REINJECT markers exist in other auto-loaded rule files, covering 17 more H-rules. These non-engine markers provide structural emphasis but are NOT re-injected per-prompt. Expanding the engine to read all 9 files would nearly triple L2 coverage (10→27 H-rules).

**Key Findings:**
- Engine reads only `quality-enforcement.md` (line 243, `_find_rules_path` method)
- 8 engine-processed markers = 415 tokens, covering 10 distinct H-rules
- 8 structural markers across 8 other files = 425 tokens, covering 17 additional H-rules
- 4 H-rules (H-04, H-16, H-17, H-18) have NO L2 emphasis at all
- 21 of 31 H-rules lack engine-processed L2 protection — they are vulnerable to context rot

**Validation:** Validated via source code analysis and C4 adversary tournament (0.95 PASS)

---

## Context

### Background

During the HARD rule budget upper boundary derivation, the binding constraint was identified as Enforcement Coverage (Constraint Family B). The L2 re-injection engine's coverage directly determines how many rules survive context rot — the core problem Jerry is designed to solve.

### Research Question

How many HARD rules have per-prompt L2 re-injection protection, and is the current engine limitation architectural or implementational?

### Investigation Approach

1. Read `prompt_reinforcement_engine.py` source code to identify the L2 marker processing path
2. Inventoried all L2-REINJECT markers across all auto-loaded rule files
3. Classified markers as engine-processed vs. structurally-emphasized
4. Assessed whether the limitation is architectural (fundamental) or implementational (fixable)

---

## Finding

### Engine Limitation

The `_find_rules_path` method (line 243) resolves to `quality-enforcement.md` only. The `_extract_l2_markers` method then parses L2-REINJECT HTML comments from that single file.

This is an **implementation gap**, not an architectural constraint. The engine could read all 9 files containing L2-REINJECT markers with a straightforward code change.

### L2 Marker Ecosystem

**Engine-Processed (quality-enforcement.md only):**

| # | Rank | Tokens | H-Rules | Content |
|---|------|--------|---------|---------|
| 1 | 1 | 50 | H-01, H-02, H-03 | Constitutional constraints |
| 2 | 2 | 90 | H-13, H-14 | Quality gate + creator-critic cycle |
| 3 | 2 | 50 | H-31 | Ambiguity clarification |
| 4 | 3 | 25 | H-05, H-06 | UV-only Python |
| 5 | 4 | 30 | *(S-014)* | LLM-as-Judge bias counteraction |
| 6 | 5 | 30 | H-15 | Self-review |
| 7 | 6 | 100 | *(criticality)* | C1-C4 levels, AE rules |
| 8 | 8 | 40 | H-19 | Governance escalation |
| | **Total** | **415** | **10 H-rules** | |

**Structural-Only (not engine-processed):**

| # | File | Tokens | H-Rules |
|---|------|--------|---------|
| 1 | architecture-standards.md | 60 | H-07, H-08, H-09, H-10 |
| 2 | coding-standards.md | 60 | H-11, H-12 |
| 3 | testing-standards.md | 40 | H-20, H-21 |
| 4 | mandatory-skill-usage.md | 50 | H-22 |
| 5 | markdown-navigation-standards.md | 25 | H-23, H-24 |
| 6 | skill-standards.md | 70 | H-25..H-30 |
| 7 | python-environment.md | 50 | H-05, H-06 (duplicate) |
| 8 | mcp-tool-standards.md | 70 | MCP-001, MCP-002 (file-scoped) |
| | **Total** | **425** | **17 additional H-rules** |

**Coverage Summary:**
- H-rules with engine L2: **10** (32%)
- H-rules with structural L2 only: **17** (55%)
- H-rules with NO L2: **4** (13%) — H-04, H-16, H-17, H-18

### Fix Impact

Expanding the engine to read all 9 auto-loaded files:
- L2 budget increase: 415 → 840 tokens (40% increase from 600 declared budget — requires budget update)
- H-rule coverage: 10 → 27 (170% increase)
- Rules with NO L2: 4 → 4 (unchanged — these files don't have markers yet)

---

## Evidence

### Source Documentation

| Evidence ID | Type | Description | Source | Date |
|-------------|------|-------------|--------|------|
| E-001 | Source code | `_find_rules_path` reads only quality-enforcement.md | `prompt_reinforcement_engine.py:243` | 2026-02-21 |
| E-002 | File scan | 16 L2-REINJECT markers across 9 files | Manual inventory | 2026-02-21 |
| E-003 | ADR | L2 budget declared at 600 tokens | `ADR-EPIC002-002` | Baselined |
| E-004 | Derivation | Family B analysis identifying this as binding constraint | `hard-rule-budget-upper-boundary-derivation-r2.md` | 2026-02-21 |

---

## Implications

### Impact on Project

This is the single highest-value fix available:
- **Low effort:** Change engine to glob all auto-loaded rule files instead of hardcoding one file
- **High impact:** Nearly triples L2 coverage, directly addresses the binding constraint identified in the derivation
- **Risk reduction:** Reduces context rot vulnerability for 17 additional H-rules

### Risks Identified

| Risk | Severity | Mitigation |
|------|----------|------------|
| L2 budget overflow (840 > 600 declared) | Medium | Update ADR-EPIC002-002 budget to 850 tokens; still within total enforcement budget |
| Marker quality varies across files | Low | Audit all non-engine markers for quality before enabling |

### Opportunities Created

- Enables the two-tier enforcement model (Tier A: engine L2, Tier B: structural L2 + L3/L5)
- Unblocks principled Tier A/B classification of all HARD rules
- Reduces dependency on L1 session-start loading (the VULNERABLE layer)

---

## Relationships

### Creates

- [TASK-022](../TASK-022-expand-l2-engine/TASK-022.md) - Expand L2 engine to read all rule files

### Informs

- [DISC-001](../DISC-001-hard-rule-budget-no-derivation/DISC-001.md) - Budget derivation (B is binding constraint)
- [DEC-001](../DEC-001-hard-rule-budget-implementation-plan/DEC-001.md) - Implementation plan (engine fix is highest priority)

### Related Artifacts

| Type | Path | Description |
|------|------|-------------|
| Parent | [EN-002](../EN-002.md) | Parent enabler |
| Source code | `src/infrastructure/internal/enforcement/prompt_reinforcement_engine.py` | Engine implementation |
| SSOT | `.context/rules/quality-enforcement.md` | Enforcement architecture definition |

---

## Recommendations

### Immediate Actions

1. Expand engine to read all auto-loaded rule files (TASK-022)
2. Update L2 budget in ADR-EPIC002-002 from 600 to 850 tokens
3. Audit structural L2 markers for quality and consistency

### Long-term Considerations

- Add L2-REINJECT markers for the 4 uncovered H-rules (H-04, H-16, H-17, H-18)
- Consider rank-based marker prioritization if budget becomes constrained

---

## Document History

| Date | Author | Change |
|------|--------|--------|
| 2026-02-21 | Claude (PROJ-007 orchestrator) | Created discovery — validated via source code analysis + C4 tournament |

---

## Metadata

```yaml
id: "EN-002:DISC-002"
parent_id: "EN-002"
work_type: DISCOVERY
title: "L2 Prompt Reinforcement Engine Coverage Gap"
status: VALIDATED
priority: HIGH
impact: HIGH
created_by: "Claude (PROJ-007 orchestrator)"
created_at: "2026-02-21T22:00:00Z"
updated_at: "2026-02-21T23:30:00Z"
completed_at: "2026-02-21T23:30:00Z"
tags: [enforcement, l2-engine, context-rot, prompt-reinforcement]
source: "Source code analysis"
finding_type: GAP
confidence_level: HIGH
validated: true
```
