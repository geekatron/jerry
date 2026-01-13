---
id: wi-sao-028
title: "Full Template Regeneration Capability (Option C)"
status: OPEN
parent: "_index.md"
initiative: sao-init-003-deferred
children: []
depends_on:
  - wi-sao-026
  - wi-sao-027
blocks: []
created: "2026-01-11"
priority: "P3"
estimated_effort: "16h"
entry_id: "sao-028"
source: "WI-SAO-010/011 de-prioritization decision"
token_estimate: 700
---

# WI-SAO-028: Full Template Regeneration Capability (Option C)

> **Status:** OPEN
> **Priority:** LOW (P3)

---

## Description

Implement full regeneration capability from templates, producing deterministic output while preserving customizations.

---

## Context

After WI-SAO-026/027 normalize existing agents, this work item enables regenerating all agents from the composed template with customization preservation.

---

## Acceptance Criteria (Validatable Evidence)

1. Regenerate all 19 agents from template produces identical output
   - **Evidence:** `python3 scripts/compose_agent_template.py --regenerate --family all` matches existing files

2. Customizations preserved via extension files
   - **Evidence:** PS_EXTENSION.md and NSE_EXTENSION.md content injected correctly

3. Template changes propagate deterministically
   - **Evidence:** Modify AGENT_TEMPLATE_CORE.md, regenerate, verify change in all agents

---

## Tasks

- [ ] **T-028.1:** Design regeneration protocol with diff/patch
- [ ] **T-028.2:** Implement customization extraction from existing agents
- [ ] **T-028.3:** Implement merge strategy for template + customizations
- [ ] **T-028.4:** Add --regenerate flag to compose_agent_template.py
- [ ] **T-028.5:** Create regression test suite for regeneration
- [ ] **T-028.6:** Document regeneration workflow in AGENT_MIGRATION_GUIDE.md

---

## Notes

- This is the ultimate goal enabling template-driven agent governance
- Requires WI-SAO-026/027 to be complete first

---

*Source: Extracted from WORKTRACKER.md lines 1548-1573*
