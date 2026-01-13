---
id: wi-sao-027
title: "NSE Agent Structure Normalization (Option B)"
status: OPEN
parent: "_index.md"
initiative: sao-init-003-deferred
children: []
depends_on:
  - "../../complete/sao-init-003-templates/wi-sao-011.md"
blocks:
  - wi-sao-028
created: "2026-01-11"
priority: "P3"
estimated_effort: "10h"
entry_id: "sao-027"
source: "WI-SAO-011 de-prioritization decision"
token_estimate: 700
---

# WI-SAO-027: NSE Agent Structure Normalization (Option B)

> **Status:** OPEN
> **Priority:** LOW (P3)

---

## Description

Normalize nse-* agent structure to match composed template output, enabling deterministic regeneration.

---

## Context

WI-SAO-011 Option A (version bump + verification) completed. This work item captures Option B - aligning the existing agents with the composed template structure so future template changes can be regenerated deterministically.

---

## Acceptance Criteria (Validatable Evidence)

1. All 10 nse-* agents structurally match composed template output
   - **Evidence:** `python3 scripts/compose_agent_template.py --family nse --diff nse-requirements` shows minimal differences

2. Section ordering matches template
   - **Evidence:** Visual inspection of frontmatter and `<agent>` section order

3. NASA SE principles properly integrated
   - **Evidence:** P-040, P-041, P-042, P-043 references present

---

## Tasks

- [ ] **T-027.1:** Audit nse-* agent structure vs composed template
- [ ] **T-027.2:** Normalize section ordering to match template
- [ ] **T-027.3:** Align frontmatter fields with template
- [ ] **T-027.4:** Verify NASA SE principle integration (P-040 to P-043)
- [ ] **T-027.5:** Run conformance and diff validation

---

## Notes

- This is preparatory work for WI-SAO-028 (full regeneration capability)
- Focus on structure, not content accuracy

---

*Source: Extracted from WORKTRACKER.md lines 1522-1547*
