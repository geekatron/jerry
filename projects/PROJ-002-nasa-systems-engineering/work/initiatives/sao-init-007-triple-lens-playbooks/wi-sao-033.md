---
id: wi-sao-033
title: "Create PLAYBOOK_TEMPLATE.md"
status: OPEN
parent: "_index.md"
initiative: sao-init-007
children: []
depends_on:
  - wi-sao-038
blocks:
  - wi-sao-034
  - wi-sao-035
  - wi-sao-036
created: "2026-01-12"
last_updated: "2026-01-12"
priority: P1
estimated_effort: "4h"
entry_id: sao-033
token_estimate: 600
---

# WI-SAO-033: Create PLAYBOOK_TEMPLATE.md

> **Status:** 📋 OPEN
> **Priority:** P1 (HIGH)
> **Depends On:** WI-SAO-038 (8 patterns documented)
> **Blocks:** WI-SAO-034, WI-SAO-035, WI-SAO-036

---

## Description

Create a standardized playbook template with L0/L1/L2 sections and ASCII diagram placeholders. This template will be used to refactor all three skill playbooks consistently.

---

## Acceptance Criteria

1. [ ] Template file exists at `skills/shared/PLAYBOOK_TEMPLATE.md`
2. [ ] Contains L0 section with metaphor placeholder and ASCII diagram skeleton
3. [ ] Contains L1 section with command/invocation structure
4. [ ] Contains L2 section with anti-pattern catalog structure
5. [ ] Each section has ≥1 ASCII diagram placeholder
6. [ ] Template references the 8 orchestration patterns from WI-SAO-038

---

## Tasks

- [ ] **T-033.1:** Create `skills/shared/` directory if not exists
- [ ] **T-033.2:** Write L0 section template with metaphor structure
- [ ] **T-033.3:** Write L1 section template with command tables
- [ ] **T-033.4:** Write L2 section template with anti-pattern format
- [ ] **T-033.5:** Add ASCII diagram skeletons for each section
- [ ] **T-033.6:** Validate template completeness

---

## Verification

| Evidence ID | Type | Description | Status |
|-------------|------|-------------|--------|
| E-033-001 | Artifact | File exists at skills/shared/PLAYBOOK_TEMPLATE.md | ⏳ |
| E-033-002 | Content | L0 section present with metaphor structure | ⏳ |
| E-033-003 | Content | L1 section present with command structure | ⏳ |
| E-033-004 | Content | L2 section present with anti-pattern structure | ⏳ |
| E-033-005 | Content | ASCII diagrams present in each section | ⏳ |

---

*Source: SAO-INIT-007 plan.md Phase 1*
