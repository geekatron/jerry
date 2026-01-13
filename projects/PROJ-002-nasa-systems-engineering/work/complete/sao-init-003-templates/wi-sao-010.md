---
id: wi-sao-010
title: "Migrate ps-* Agents to Unified Template"
status: COMPLETE
parent: "_index.md"
initiative: sao-init-003
children: []
depends_on:
  - wi-sao-009
blocks: []
related:
  - "../../initiatives/sao-init-003-templates-deferred/wi-sao-026.md"
created: "2026-01-11"
started: "2026-01-11"
completed: "2026-01-11"
priority: "P2"
estimated_effort: "2h"
actual_effort: "2h"
entry_id: "sao-010"
scope_revision: "Option A only (version bump + verification)"
token_estimate: 900
---

# WI-SAO-010: Migrate ps-* Agents to Unified Template

> **Status:** ✅ COMPLETE
> **Started:** 2026-01-11
> **Completed:** 2026-01-11
> **Priority:** MEDIUM (P2) - de-prioritized after Option A

---

## Scope Revision

Option A only (version bump + verification). Option B/C deferred to WI-SAO-026.

---

## Description

Verify all 9 ps-* agents conform to federated template and update versions.

---

## Acceptance Criteria (Validatable Evidence)

1. ✅ All 9 ps-* agents pass conformance check
   - **Evidence:** `python3 scripts/check_agent_conformance.py --family ps` returns 9/9 PASS
   - **Verification:** Executed 2026-01-11, output: "Summary: 9/9 agents conformant"

2. ✅ Behavior tests status documented (not blocking)
   - **Evidence:** BEHAVIOR_TESTS.md reviewed, 11 tests PENDING (LLM-as-a-Judge)
   - **Verification:** Discovery D-010-001 documented

3. ✅ Version field updated to 2.1.0
   - **Evidence:** `grep "^version:" skills/problem-solving/agents/ps-*.md` shows "2.1.0"
   - **Verification:** All 9 agents updated via sed from 2.0.0 → 2.1.0

---

## Discoveries

- **D-010-001:** BEHAVIOR_TESTS.md contains 11 tests, all PENDING. These are LLM-as-a-Judge tests (G-Eval/DeepEval), not automated tests. Require manual execution framework.
  - Severity: INFORMATIONAL
  - Action: Document as known limitation. Future work item for test automation.

---

## Tasks (Option A)

- [x] **T-010.1:** Verify conformance for all 9 ps-* agents ✅
- [x] **T-010.2:** Update version to 2.1.0 in all 9 ps-* agents ✅
- [x] **T-010.3:** Run conformance check and document results ✅
- [x] **T-010.4:** Update worktracker with completion evidence ✅

---

## Deferred to WI-SAO-026

- Option B: Normalize structure to match composed template
- Option C: Full regeneration capability

---

## Completion Summary

- All 9 ps-* agents verified conformant with federated template
- Versions updated: ps-analyst, ps-architect, ps-critic, ps-investigator, ps-reporter, ps-researcher, ps-reviewer, ps-synthesizer, ps-validator
- BEHAVIOR_TESTS.md limitation documented (LLM-as-a-Judge, not automated)

---

*Source: Extracted from WORKTRACKER.md lines 1415-1451*
