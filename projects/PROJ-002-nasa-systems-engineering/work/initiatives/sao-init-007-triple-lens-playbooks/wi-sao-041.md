---
id: wi-sao-041
title: "Create pattern selection decision tree visual"
status: OPEN
parent: "_index.md"
initiative: sao-init-007
children: []
depends_on:
  - wi-sao-038
blocks: []
created: "2026-01-12"
last_updated: "2026-01-12"
priority: P2
estimated_effort: "1h"
entry_id: sao-041
token_estimate: 350
---

# WI-SAO-041: Create pattern selection decision tree visual

> **Status:** 📋 OPEN
> **Priority:** P2 (MEDIUM)
> **Depends On:** WI-SAO-038 (8 patterns documented)

---

## Description

Create a clear ASCII decision tree that helps users select the appropriate orchestration pattern based on their task characteristics.

---

## Decision Tree in plan.md

```
START: What type of task?
        │
   ┌────┴────┐
   ▼         ▼
Single?   Multi-agent?
   │         │
   ▼         ▼
PATTERN 1   Dependencies?
            │
       ┌────┴────┐
       ▼         ▼
      Yes        No
       │          │
       ▼          ▼
   PATTERN 2   PATTERN 3/4
   ...
```

---

## Acceptance Criteria

1. [ ] Decision tree covers all 8 patterns
2. [ ] Questions lead to unambiguous pattern selection
3. [ ] ASCII rendering is readable in terminal
4. [ ] Included in orchestration PLAYBOOK.md
5. [ ] Cross-referenced from other playbooks

---

## Tasks

- [ ] **T-041.1:** Review existing decision tree in plan.md
- [ ] **T-041.2:** Verify all 8 patterns reachable
- [ ] **T-041.3:** Integrate into orchestration PLAYBOOK.md
- [ ] **T-041.4:** Add cross-references from ps/nse playbooks

---

## Verification

| Evidence ID | Type | Description | Status |
|-------------|------|-------------|--------|
| E-041-001 | Content | Decision tree in orchestration PLAYBOOK | ⏳ |
| E-041-002 | Validation | All 8 patterns reachable | ⏳ |

---

*Source: SAO-INIT-007 plan.md Pattern Selection Decision Tree*
