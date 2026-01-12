---
id: wi-sao-060
title: "Enhance nse-reviewer Agent"
status: OPEN
parent: "_index.md"
initiative: sao-init-008
children: []
depends_on:
  - wi-sao-052
blocks:
  - wi-sao-062
  - wi-sao-066
created: "2026-01-12"
last_updated: "2026-01-12"
priority: P1
estimated_effort: "4-6h"
entry_id: sao-060
token_estimate: 500
---

# WI-SAO-060: Enhance nse-reviewer Agent

> **Status:** 📋 OPEN
> **Priority:** P1 (High - NASA technical review capability)
> **Pipeline Pattern:** Pattern 8 (Generator-Critic Loop)

---

## Description

Enhance the nse-reviewer agent definition. Responsible for NASA technical reviews (SRR, PDR, CDR, etc.), entrance/exit criteria checking, and RFA generation.

---

## Target File

`skills/nasa-se/agents/nse-reviewer.md`

---

## Tasks

Same structure as WI-SAO-053 (Generator-Critic Loop), applied to nse-reviewer.md.

### NASA SE-Specific Enhancements

- Complete technical review type catalog (SRR→PFAR)
- Entrance/exit criteria templates per review type
- RFA/RID generation format
- Review board process guidance

### Technical Review Types

Verify all are documented:
- MCR (Mission Concept Review)
- SRR (System Requirements Review)
- SDR (System Design Review)
- PDR (Preliminary Design Review)
- CDR (Critical Design Review)
- SIR (System Integration Review)
- TRR (Test Readiness Review)
- SAR (System Acceptance Review)
- ORR (Operational Readiness Review)
- FRR (Flight Readiness Review)
- PLAR (Post-Launch Assessment Review)
- PFAR (Post-Flight Assessment Review)
- CERR (Critical Events Readiness Review)

### Orchestration Metadata

- state_output_key: "review_output"
- cognitive_mode: "convergent"
- next_hint: "(conditional)" - depends on review outcome

---

## Verification

| Evidence ID | Type | Description | Status |
|-------------|------|-------------|--------|
| E-060-001 | Score | Baseline rubric score | ⏳ Pending |
| E-060-002 | Score | Final rubric score | ⏳ Pending |
| E-060-003 | Artifact | Enhanced nse-reviewer.md | ⏳ Pending |

---

*Source: SAO-INIT-008 plan.md*
