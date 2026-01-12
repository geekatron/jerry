---
id: wi-sao-015
title: "Add Guardrail Validation Hooks"
status: NOT_STARTED
parent: "_index.md"
initiative: sao-init-004
children: []
depends_on: []
blocks: []
created: "2026-01-10"
audited: "2026-01-12"
priority: "P2"
estimated_effort: "8h"
entry_id: "sao-015"
source: "OPT-005"
token_estimate: 500
---

# WI-SAO-015: Add Guardrail Validation Hooks

> **Status:** NOT_STARTED
> **Priority:** MEDIUM (P2)
> **Audited:** 2026-01-12

---

## Description

Add pre/post validation hooks for constitutional principle enforcement.

---

## Acceptance Criteria

| AC# | Criterion | Validated? | Evidence |
|-----|-----------|------------|----------|
| AC-015-001 | Async validation (non-blocking) | NOT STARTED | No async runner exists |
| AC-015-002 | timeout_ms: 100 | NOT STARTED | No timeout implementation |
| AC-015-003 | mode: warn (don't block, just log) | NOT STARTED | No warn mode exists |
| AC-015-004 | Pattern library for common checks | NOT STARTED | No pattern library |

---

## Evidence Found (Audit 2026-01-12)

### Agent Templates HAVE Guardrails Sections

22 agent files mention "guardrails":
- All ps-* agents (9 files)
- All nse-* agents (10 files)
- Template files (3 files)

Example from ps-analyst.md:
```yaml
guardrails:
  input_validation:
    - ...
  output_filtering:
    - ...
```

### What DOES NOT Exist

1. **Centralized hook runner** - No async validation infrastructure
2. **Pattern library** - No PII/secrets detection patterns
3. **Hook execution framework** - Guardrails are declarative only
4. **Timeout handling** - No timeout mechanism for validation
5. **Warn mode** - No logging/warning infrastructure

---

## Assessment

The guardrails in agent templates are **declarative documentation** - they describe what SHOULD be validated, but there is **no infrastructure to actually run** these validations automatically.

This work item requires NEW implementation, not just testing.

---

## Tasks

- [ ] **T-015.1:** Design guardrail hook interface - NOT STARTED
- [ ] **T-015.2:** Implement async validation runner - NOT STARTED
- [ ] **T-015.3:** Create pattern library (PII, secrets) - NOT STARTED
- [ ] **T-015.4:** Add hooks to agent templates - NOT STARTED
- [ ] **T-015.5:** Create BDD tests for guardrails - NOT STARTED

---

## Technical Debt

| ID | Description | Severity |
|----|-------------|----------|
| TD-015-001 | Guardrails are declarative-only, no enforcement | MEDIUM |

---

## Discoveries

| ID | Discovery | Impact |
|----|-----------|--------|
| DISC-015-001 | 22 agent files have guardrails sections | Foundation for requirements |
| DISC-015-002 | No hook infrastructure exists | Requires new implementation |
| DISC-015-003 | This is a lower priority (P2) item | Can defer |

---

*Source: Extracted from WORKTRACKER.md lines 1643-1660*
*Audited: 2026-01-12 - Status confirmed as NOT_STARTED*
