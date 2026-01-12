---
id: wi-sao-003
title: "Add Model Field to Agent Frontmatter"
status: COMPLETE
parent: "_index.md"
initiative: sao-init-001
children: []
depends_on: []
blocks: []
created: "2026-01-10"
completed: "2026-01-10"
priority: "P1"
estimated_effort: "2h"
entry_id: "sao-003"
source: "OPT-001"
token_estimate: 600
---

# WI-SAO-003: Add Model Field to Agent Frontmatter

> **Status:** ✅ COMPLETE
> **Completed:** 2026-01-10
> **Priority:** HIGH (P1)

---

## Description

Add explicit `model: opus/sonnet/haiku/auto` field to all agent definitions for consistent behavior.

---

## Acceptance Criteria

1. ✅ All agent templates include `model` field
2. ✅ "auto" value documented as option
3. ✅ All 16 agents updated with model field

---

## Model Assignments

| Model | Agents | Rationale |
|-------|--------|-----------|
| **opus** | ps-researcher, ps-architect, nse-risk, nse-architecture | Complex reasoning |
| **sonnet** | ps-analyst, ps-investigator, ps-reviewer, ps-synthesizer, nse-requirements, nse-verification, nse-reviewer, nse-integration | Balanced |
| **haiku** | ps-reporter, ps-validator, nse-configuration, nse-reporter | Fast/procedural |

---

## Tasks

- [x] **T-003.1:** Update PS_AGENT_TEMPLATE.md with model field
- [x] **T-003.2:** Update NSE_AGENT_TEMPLATE.md with model field
- [x] **T-003.3:** Add model field to all 16 agent definitions

---

*Source: Extracted from WORKTRACKER.md lines 868-887*
