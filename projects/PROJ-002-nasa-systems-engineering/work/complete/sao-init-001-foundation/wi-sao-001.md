---
id: wi-sao-001
title: "Define session_context JSON Schema"
status: COMPLETE
parent: "_index.md"
initiative: sao-init-001
children: []
depends_on: []
blocks:
  - wi-sao-002
created: "2026-01-10"
completed: "2026-01-10"
priority: "P0"
estimated_effort: "4h"
entry_id: "sao-001"
source_gap: "GAP-AGT-003"
risk_mitigation: "M-003 (R-TECH-001)"
token_estimate: 700
---

# WI-SAO-001: Define session_context JSON Schema

> **Status:** ✅ COMPLETE
> **Completed:** 2026-01-10
> **Priority:** CRITICAL (P0)

---

## Description

Define canonical JSON Schema for session_context with required fields for reliable agent chaining.

---

## Acceptance Criteria

1. ✅ JSON Schema defined with required: session_id, source_agent, target_agent, payload
2. ✅ Payload includes: key_findings, open_questions, blockers, confidence
3. ✅ Schema version field for evolution support
4. ✅ TypeScript/Python types generated from schema

---

## Artifacts Created

- `docs/schemas/session_context.json` - JSON Schema Draft-07 specification
- `docs/schemas/SESSION_CONTEXT_GUIDE.md` - Validation utility documentation
- `docs/schemas/types/session_context.ts` - TypeScript type definitions
- `docs/schemas/types/session_context.py` - Python dataclass definitions

---

## Template Updates

- `skills/problem-solving/agents/PS_AGENT_TEMPLATE.md` - Added session_context section
- `skills/nasa-se/agents/NSE_AGENT_TEMPLATE.md` - Added session_context section

---

## Tasks

- [x] **T-001.1:** Draft JSON Schema specification
- [x] **T-001.2:** Add schema to `docs/schemas/session_context.json`
- [x] **T-001.3:** Create validation utility documentation
- [x] **T-001.4:** Update agent templates to reference schema

---

*Source: Extracted from WORKTRACKER.md lines 821-847*
