---
id: sao-init-007
title: "Triple-Lens Playbook Refactoring"
type: initiative_index
status: IN_PROGRESS
parent: "../../WORKTRACKER.md"
children:
  - wi-sao-033.md
  - wi-sao-034.md
  - wi-sao-035.md
  - wi-sao-036.md
  - wi-sao-037.md
  - wi-sao-038.md
  - wi-sao-039.md
  - wi-sao-040.md
  - wi-sao-041.md
  - wi-sao-042.md
  - wi-sao-043.md
  - wi-sao-044.md
  - wi-sao-045.md
related:
  - plan.md
created: "2026-01-12"
last_updated: "2026-01-12"
source: "/architect command - triple-lens cognitive framework"
rationale: "Playbooks lack L0 (metaphors) and L2 (anti-patterns) documentation. Engineers struggle with WHAT and WHY, only have HOW."
work_items_total: 13
work_items_complete: 11
work_items_in_progress: 0
token_estimate: 1200
---

# SAO-INIT-007: Triple-Lens Playbook Refactoring

> **Status:** 🔄 IN_PROGRESS (11/13 work items complete)
> **Created:** 2026-01-12
> **Reopened:** 2026-01-12 (DISCOVERY-012: Critical documentation gaps)
> **Detailed Plan:** [plan.md](plan.md)

---

## Rationale

Current playbooks are L1-heavy (commands, snippets) but lack:
- **L0 (ELI5):** Metaphors explaining WHAT and intent
- **L2 (Architect):** Anti-patterns, boundaries, constraints

This creates a cognitive gap where newcomers struggle to understand intent and architects discover boundaries through trial and error.

---

## Summary

| Work Item | Status | Priority | Description |
|-----------|--------|----------|-------------|
| WI-SAO-033 | ✅ COMPLETE | P1 | Create PLAYBOOK_TEMPLATE.md |
| WI-SAO-034 | ✅ COMPLETE | P1 | Refactor orchestration PLAYBOOK.md |
| WI-SAO-035 | ✅ COMPLETE | P1 | Refactor problem-solving PLAYBOOK.md |
| WI-SAO-036 | ✅ COMPLETE | P1 | Refactor nasa-se PLAYBOOK.md |
| WI-SAO-037 | ✅ COMPLETE | P2 | Validate all examples executable |
| WI-SAO-038 | ✅ COMPLETE | P1 | Document 8 orchestration patterns in template |
| WI-SAO-039 | ✅ COMPLETE | P2 | Add workflow scenario compositions |
| WI-SAO-040 | ✅ COMPLETE | P3 | Validate session context schema v1.0.0 |
| WI-SAO-041 | ✅ COMPLETE | P2 | Create pattern selection decision tree visual |
| WI-SAO-042 | ✅ COMPLETE | P1 | Research & document Generator-Critic patterns |
| WI-SAO-043 | ✅ COMPLETE | P1 | Add L0/L1/L2 concrete examples (5+ each domain) |
| WI-SAO-044 | 📋 OPEN | P2 | Document @ symbol agent invocation |
| WI-SAO-045 | 📋 OPEN | P1 | Verify nse-* Generator-Critic applicability |

---

## Dependencies

```
WI-SAO-038 ──> WI-SAO-033 ──> WI-SAO-034 ──> WI-SAO-037
                         ──> WI-SAO-035 ──> WI-SAO-037
                         ──> WI-SAO-036 ──> WI-SAO-037
WI-SAO-039 ──> WI-SAO-034, WI-SAO-035, WI-SAO-036
WI-SAO-041 ──> WI-SAO-038
```

---

## Success Criteria

| Criterion | Target | Status |
|-----------|--------|--------|
| L0 Coverage | 3/3 playbooks | ✅ Complete |
| L1 Coverage | All invocations | ✅ Complete |
| L2 Coverage | ≥3 anti-patterns per playbook | ✅ Complete |
| ASCII Diagrams | ≥1 per L0/L1/L2 | ✅ Complete |
| Pattern Coverage | 8/8 patterns documented | ✅ Complete |
| Placeholders | 0 | ✅ Complete |

---

## Key Documents

| Document | Purpose |
|----------|---------|
| [plan.md](plan.md) | Comprehensive implementation plan (v2.0.0) |
| [ORCHESTRATION_PATTERNS.md](../../../skills/shared/ORCHESTRATION_PATTERNS.md) | 8 patterns reference (WI-SAO-038 output) |
| DISCOVERY-008 | 8 orchestration patterns identified |
| DISCOVERY-009 | Session context schema v1.0.0 formalized |

---

## Evidence Requirements

| Evidence ID | Type | Verification | Status |
|-------------|------|--------------|--------|
| E-033-001 | Artifact | PLAYBOOK_TEMPLATE.md exists | ✅ Complete |
| E-034-001 | Artifact | orchestration/PLAYBOOK.md has L0/L1/L2 | ✅ Complete |
| E-035-001 | Artifact | problem-solving/PLAYBOOK.md has L0/L1/L2 | ✅ Complete |
| E-036-001 | Artifact | nasa-se/PLAYBOOK.md has L0/L1/L2 | ✅ Complete |
| E-037-001 | Test | All examples execute without error | ✅ Complete |
| E-038-001 | Artifact | 8 patterns documented with ASCII diagrams | ✅ Complete |
| E-039-001 | Artifact | ≥5 workflow scenarios documented | ✅ Complete |

---

## Initiative Reopened (2026-01-12)

**DISCOVERY-012: Critical Documentation Gaps Identified**

The following gaps were discovered during user review:

| Gap ID | Severity | Description |
|--------|----------|-------------|
| GAP-012-001 | **CRITICAL** | Generator-Critic loop not documented in problem-solving PLAYBOOK |
| GAP-012-002 | **CRITICAL** | ps-critic agent usage and integration missing |
| GAP-012-003 | **HIGH** | No concrete L0/L1/L2 examples for real-world scenarios |
| GAP-012-004 | **MEDIUM** | @ symbol agent invocation not documented |
| GAP-012-005 | **HIGH** | nse-* Generator-Critic applicability not verified |

**Root Cause:** Initial playbook refactoring focused on structure (L0/L1/L2 lens) but missed functional completeness (all agent interactions).

**New Work Items Added:**
- WI-SAO-042: Research & document Generator-Critic patterns (P1)
- WI-SAO-043: Add L0/L1/L2 concrete examples (P1)
- WI-SAO-044: Document @ symbol agent invocation (P2)
- WI-SAO-045: Verify nse-* Generator-Critic applicability (P1)

---

## New Success Criteria (Phase 2)

| Criterion | Target | Status |
|-----------|--------|--------|
| Generator-Critic documented | Full pattern with examples | ✅ Complete |
| L0/L1/L2 Examples | ≥5 per domain (SE, PM, UX) | ✅ Complete |
| @ Symbol documented | Usage guide with examples | 📋 Open |
| nse-* Applicability | Research complete | 📋 Open |

---

*Source: /architect command invocation 2026-01-12*
*Plan Version: 2.0.0 (meta-enhanced via ps-* pipeline)*
*Reopened: 2026-01-12 (DISCOVERY-012)*
