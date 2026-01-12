---
id: wi-sao-015
title: "Add Guardrail Validation Hooks"
status: OPEN
parent: "_index.md"
initiative: sao-init-004
children: []
depends_on: []
blocks: []
created: "2026-01-10"
priority: "P2"
estimated_effort: "8h"
entry_id: "sao-015"
source: "OPT-005"
token_estimate: 500
---

# WI-SAO-015: Add Guardrail Validation Hooks

> **Status:** OPEN
> **Priority:** MEDIUM (P2)

---

## Description

Add pre/post validation hooks for constitutional principle enforcement.

---

## Acceptance Criteria

1. Async validation (non-blocking)
2. timeout_ms: 100
3. mode: warn (don't block, just log)
4. Pattern library for common checks

---

## Tasks

- [ ] **T-015.1:** Design guardrail hook interface
- [ ] **T-015.2:** Implement async validation runner
- [ ] **T-015.3:** Create pattern library (PII, secrets)
- [ ] **T-015.4:** Add hooks to agent templates
- [ ] **T-015.5:** Create BDD tests for guardrails

---

*Source: Extracted from WORKTRACKER.md lines 1643-1660*
