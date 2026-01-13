---
id: wi-sao-026
title: "PS Agent Structure Normalization (Option B)"
status: OPEN
parent: "_index.md"
initiative: sao-init-003-deferred
children: []
depends_on:
  - "../../complete/sao-init-003-templates/wi-sao-010.md"
blocks:
  - wi-sao-028
created: "2026-01-11"
priority: "P3"
estimated_effort: "8h"
entry_id: "sao-026"
source: "WI-SAO-010 de-prioritization decision"
token_estimate: 700
---

# WI-SAO-026: PS Agent Structure Normalization (Option B)

> **Status:** OPEN
> **Priority:** LOW (P3)

---

## Description

Normalize ps-* agent structure to match composed template output, enabling deterministic regeneration.

---

## Context

WI-SAO-010 Option A (version bump + verification) completed. This work item captures Option B - aligning the existing agents with the composed template structure so future template changes can be regenerated deterministically.

---

## Acceptance Criteria (Validatable Evidence)

1. All 9 ps-* agents structurally match composed template output
   - **Evidence:** `python3 scripts/compose_agent_template.py --family ps --diff ps-analyst` shows minimal differences

2. Section ordering matches template
   - **Evidence:** Visual inspection of frontmatter and `<agent>` section order

3. Claude Code best practices applied
   - **Evidence:** Review per Claude documentation patterns (Boris Cherny research)

---

## Tasks

- [ ] **T-026.1:** Audit ps-* agent structure vs composed template
- [ ] **T-026.2:** Normalize section ordering to match template
- [ ] **T-026.3:** Align frontmatter fields with template
- [ ] **T-026.4:** Verify Claude Code best practices (research output)
- [ ] **T-026.5:** Run conformance and diff validation

---

## Notes

- This is preparatory work for WI-SAO-028 (full regeneration capability)
- Focus on structure, not content accuracy

---

*Source: Extracted from WORKTRACKER.md lines 1496-1521*
