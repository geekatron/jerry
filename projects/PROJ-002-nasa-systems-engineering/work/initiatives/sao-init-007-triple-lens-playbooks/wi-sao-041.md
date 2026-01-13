---
id: wi-sao-041
title: "Create pattern selection decision tree visual"
status: COMPLETE
parent: "_index.md"
initiative: sao-init-007
children: []
depends_on:
  - wi-sao-038
blocks: []
created: "2026-01-12"
last_updated: "2026-01-12"
completed: "2026-01-12"
priority: P2
estimated_effort: "1h"
actual_effort: "30m"
entry_id: sao-041
token_estimate: 350
---

# WI-SAO-041: Create pattern selection decision tree visual

> **Status:** ✅ COMPLETE
> **Priority:** P2 (MEDIUM)
> **Completed:** 2026-01-12
> **Depends On:** WI-SAO-038 (8 patterns documented)

---

## Description

Create a clear ASCII decision tree that helps users select the appropriate orchestration pattern based on their task characteristics. Also provide Mermaid diagram for GitHub/IDE rendering.

---

## Acceptance Criteria

1. [x] Decision tree covers all 8 patterns
2. [x] Questions lead to unambiguous pattern selection
3. [x] ASCII rendering is readable in terminal
4. [x] Included in orchestration PLAYBOOK.md
5. [x] Cross-referenced from other playbooks

---

## Tasks

- [x] **T-041.1:** Review existing decision tree in orchestration playbook
- [x] **T-041.2:** Add Mermaid diagram version to orchestration playbook
- [x] **T-041.3:** Add Mermaid diagram to ORCHESTRATION_PATTERNS.md
- [x] **T-041.4:** Verify cross-references from ps/nse playbooks

---

## Verification

| Evidence ID | Type | Description | Status |
|-------------|------|-------------|--------|
| E-041-001 | Content | ASCII decision tree in orchestration PLAYBOOK | ✅ Complete |
| E-041-002 | Content | Mermaid decision tree in orchestration PLAYBOOK | ✅ Complete |
| E-041-003 | Validation | All 8 patterns reachable | ✅ Complete |
| E-041-004 | Content | Cross-references from other playbooks | ✅ Complete |

---

## Output Summary

### ASCII Decision Tree

**Location:** `skills/orchestration/PLAYBOOK.md` (lines 206-250)

```
START: How many agents?
       |
  +----+----+
  |         |
  v         v
ONE       MULTIPLE
  |         |
  v         v
Pattern 1   Dependencies?
(Single)    |
       +----+----+
       |         |
       v         v
      YES        NO
       |         |
       v         v
   Pattern 2   Pattern 3/4
   (Sequential) (Fan-Out/In)
       ...
```

### Mermaid Decision Tree

**Location:** `skills/orchestration/PLAYBOOK.md` (lines 252-280)
**Location:** `skills/shared/ORCHESTRATION_PATTERNS.md` (lines 622-660)

- Flowchart format for GitHub/IDE rendering
- Color-coded by pattern type
- All 8 patterns reachable via decision nodes

### Cross-References

| Source Playbook | Location | Reference |
|-----------------|----------|-----------|
| problem-solving/PLAYBOOK.md | Line 317 | Links to ORCHESTRATION_PATTERNS.md |
| nasa-se/PLAYBOOK.md | Line 927 | Links to ORCHESTRATION_PATTERNS.md |

### Pattern Reachability

| Pattern | Reachable via Decision Path |
|---------|----------------------------|
| 1. Single Agent | One agent path |
| 2. Sequential Chain | Multiple → Dependencies=Yes |
| 3. Fan-Out | Multiple → Dependencies=No |
| 4. Fan-In | Multiple → Independent=Yes |
| 5. Cross-Pollinated | Sequential → Bidirectional=Yes |
| 6. Diamond | Multiple → Independent=No |
| 7. Review Gate | Sequential → Quality gates=Yes |
| 8. Generator-Critic | Sequential → Iteration=Yes |

---

*Source: SAO-INIT-007 plan.md Pattern Selection Decision Tree*
*Completed: 2026-01-12*
