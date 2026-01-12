---
id: wi-sao-033
title: "Create PLAYBOOK_TEMPLATE.md"
status: COMPLETE
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
completed: "2026-01-12"
priority: P1
estimated_effort: "4h"
actual_effort: "1h"
entry_id: sao-033
token_estimate: 600
---

# WI-SAO-033: Create PLAYBOOK_TEMPLATE.md

> **Status:** ✅ COMPLETE
> **Priority:** P1 (HIGH)
> **Completed:** 2026-01-12
> **Depends On:** WI-SAO-038 (8 patterns documented)
> **Blocks:** WI-SAO-034, WI-SAO-035, WI-SAO-036

---

## Description

Create a standardized playbook template with L0/L1/L2 sections and ASCII diagram placeholders. This template will be used to refactor all three skill playbooks consistently.

---

## Acceptance Criteria

1. [x] Template file exists at `skills/shared/PLAYBOOK_TEMPLATE.md`
2. [x] Contains L0 section with metaphor placeholder and ASCII diagram skeleton
3. [x] Contains L1 section with command/invocation structure
4. [x] Contains L2 section with anti-pattern catalog structure
5. [x] Each section has ≥1 ASCII diagram placeholder
6. [x] Template references the 8 orchestration patterns from WI-SAO-038

---

## Tasks

- [x] **T-033.1:** Create `skills/shared/` directory if not exists (already existed)
- [x] **T-033.2:** Write L0 section template with metaphor structure
- [x] **T-033.3:** Write L1 section template with command tables
- [x] **T-033.4:** Write L2 section template with anti-pattern format
- [x] **T-033.5:** Add ASCII diagram skeletons for each section
- [x] **T-033.6:** Validate template completeness

---

## Verification

| Evidence ID | Type | Description | Status |
|-------------|------|-------------|--------|
| E-033-001 | Artifact | File exists at skills/shared/PLAYBOOK_TEMPLATE.md | ✅ Complete |
| E-033-002 | Content | L0 section present with metaphor structure | ✅ Complete |
| E-033-003 | Content | L1 section present with command structure | ✅ Complete |
| E-033-004 | Content | L2 section present with anti-pattern structure | ✅ Complete |
| E-033-005 | Content | ASCII diagrams present in each section | ✅ Complete |
| E-033-006 | Content | References ORCHESTRATION_PATTERNS.md | ✅ Complete |

---

## Output Artifact

**File:** `skills/shared/PLAYBOOK_TEMPLATE.md`

**Structure:**
```
PLAYBOOK_TEMPLATE.md
├── Document Overview (Triple-Lens Framework diagram)
├── L0: The Big Picture (ELI5)
│   ├── The Metaphor (boxed placeholder)
│   ├── Why Does This Matter (comparison table)
│   ├── When Do I Use This (decision tree)
│   └── Cast of Characters (agent portfolio diagram)
├── L1: How To Use It (Engineer)
│   ├── Quick Start (30-second version)
│   ├── Invocation Methods (3 methods)
│   ├── Agent Reference (table)
│   ├── Orchestration Patterns (decision tree + table)
│   ├── Common Workflows (2 workflow templates)
│   ├── Output Locations (directory tree)
│   ├── Tips and Best Practices
│   └── Troubleshooting
├── L2: Architecture & Constraints
│   ├── Anti-Pattern Catalog (3 AP slots with boxed format)
│   ├── Constraints & Boundaries (hard/soft tables)
│   ├── Invariants (checklist)
│   ├── State Management (schema + keys table)
│   ├── Cross-Skill Integration (handoff diagram)
│   └── Design Rationale (ADR-style)
└── Appendices (reference card)
```

**Size:** ~6KB (comprehensive template)

---

*Source: SAO-INIT-007 plan.md Phase 1*
*Completed: 2026-01-12*
