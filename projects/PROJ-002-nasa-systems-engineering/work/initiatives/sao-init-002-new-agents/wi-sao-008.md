---
id: wi-sao-008
title: "Create nse-qa Agent"
status: COMPLETE
parent: "_index.md"
initiative: sao-init-002
children: []
depends_on: []
blocks: []
created: "2026-01-11"
started: "2026-01-11"
completed: "2026-01-11"
priority: "P2"
estimated_effort: "6h"
entry_id: "sao-008"
belbin_role: "Monitor Evaluator"
token_estimate: 700
---

# WI-SAO-008: Create nse-qa Agent

> **Status:** ✅ COMPLETE
> **Started:** 2026-01-11
> **Completed:** 2026-01-11
> **Priority:** MEDIUM (P2)

---

## Description

Create NASA SE quality assurance agent for artifact validation.

---

## Acceptance Criteria

1. ✅ Agent definition follows NSE_AGENT_TEMPLATE v1.0
2. ✅ Validates NPR 7123.1D compliance
3. ✅ Checks traceability (P-040)
4. ✅ Output: QA reports (qa-report.md template)

---

## Artifacts Created

- `skills/nasa-se/agents/nse-qa.md` - 664 lines, convergent Monitor Evaluator
- `skills/nasa-se/templates/qa-report.md` - QA report template with L0/L1/L2
- `skills/nasa-se/tests/BEHAVIOR_TESTS.md` - 8 BHV-QA-* test cases added
- `skills/nasa-se/SKILL.md` - Updated with nse-qa registration (10 agents total)

---

## QA Checklists

5 checklists implemented:
- REQ-QA: Requirements quality
- VER-QA: Verification matrix quality
- RSK-QA: Risk register quality
- CON-QA: Configuration item quality
- REV-QA: Review report quality

---

## Conformance

**19/19 agents pass conformance check** after nse-qa addition.

---

## Tasks

- [x] **T-008.1:** Draft nse-qa.md agent definition
- [x] **T-008.2:** Define NASA SE quality checklists (5 checklists)
- [x] **T-008.3:** Create NPR compliance validation templates (qa-report.md)
- [x] **T-008.4:** Create BDD tests for QA workflows (8 tests)

---

*Source: Extracted from WORKTRACKER.md lines 1114-1139*
