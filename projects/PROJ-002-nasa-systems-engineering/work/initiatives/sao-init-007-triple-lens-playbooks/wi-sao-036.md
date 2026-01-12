---
id: wi-sao-036
title: "Refactor nasa-se PLAYBOOK.md"
status: OPEN
parent: "_index.md"
initiative: sao-init-007
children: []
depends_on:
  - wi-sao-033
blocks:
  - wi-sao-037
created: "2026-01-12"
last_updated: "2026-01-12"
priority: P1
estimated_effort: "6h"
entry_id: sao-036
token_estimate: 500
---

# WI-SAO-036: Refactor nasa-se PLAYBOOK.md

> **Status:** 📋 OPEN
> **Priority:** P1 (HIGH)
> **Depends On:** WI-SAO-033 (template)
> **Blocks:** WI-SAO-037 (validation)

---

## Description

Apply PLAYBOOK_TEMPLATE.md to refactor `skills/nasa-se/PLAYBOOK.md` with L0/L1/L2 sections using the Mission Control metaphor.

---

## Acceptance Criteria

1. [ ] L0 section added with Mission Control metaphor and launch countdown ASCII
2. [ ] L1 section with all 10 nse-* agent invocations documented
3. [ ] L2 section with NASA-specific anti-patterns (AI as Authority, Skipping Reviews)
4. [ ] Technical review sequence documented (SRR→PDR→CDR→TRR→FRR)
5. [ ] P-043 disclaimer placement guidance
6. [ ] ASCII diagrams in each section

---

## Tasks

- [ ] **T-036.1:** Read existing nasa-se/PLAYBOOK.md
- [ ] **T-036.2:** Apply template structure
- [ ] **T-036.3:** Write L0 section (Mission Control)
- [ ] **T-036.4:** Enhance L1 with 10 agents and review gates
- [ ] **T-036.5:** Write L2 section (NASA anti-patterns)
- [ ] **T-036.6:** Present diff for approval

---

## Verification

| Evidence ID | Type | Description | Status |
|-------------|------|-------------|--------|
| E-036-001 | Content | L0 section with Mission Control | ⏳ |
| E-036-002 | Content | L1 section with 10 agent commands | ⏳ |
| E-036-003 | Content | L2 section with NASA anti-patterns | ⏳ |
| E-036-004 | Content | P-043 disclaimer guidance present | ⏳ |

---

*Source: SAO-INIT-007 plan.md Phase 3*
