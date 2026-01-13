---
id: wi-sao-024
title: "Audit Agent Template Conformance"
status: COMPLETE
parent: "_index.md"
initiative: sao-init-005
children: []
depends_on: []
blocks: []
created: "2026-01-11"
started: "2026-01-11"
completed: "2026-01-11"
priority: "P2"
estimated_effort: "2h"
actual_effort: "1.5h"
entry_id: "sao-024"
discovered: "2026-01-11 during WI-SAO-002"
token_estimate: 600
---

# WI-SAO-024: Audit Agent Template Conformance

> **Status:** ✅ COMPLETE
> **Started:** 2026-01-11
> **Completed:** 2026-01-11
> **Priority:** MEDIUM (P2)

---

## Description

Create automated conformance check to detect agent template drift. Prevents future structural inconsistencies.

---

## Root Cause

WI-SAO-022 gap exists because there was no automated check ensuring agents match their templates.

---

## Completion Summary

- Created `scripts/check_agent_conformance.py` - validates all 16 agents against their templates
- Created `.pre-commit-config.yaml` - adds conformance check to pre-commit hooks
- Created `docs/governance/AGENT_CONFORMANCE_RULES.md` - documents all conformance rules
- Discovered tech debt: All 8 NSE agents missing `output.template` field (see WI-SAO-025)

---

## Acceptance Criteria

1. ✅ Script to validate agent structure against template (`scripts/check_agent_conformance.py`)
2. ✅ Check runs as pre-commit or CI (`.pre-commit-config.yaml`)
3. ✅ Reports structural deviations with actionable output (text and JSON formats)

---

## Tasks

- [x] **T-024.1:** Define required YAML sections per template
- [x] **T-024.2:** Create conformance check script
- [x] **T-024.3:** Add to pre-commit hooks or CI
- [x] **T-024.4:** Document template conformance rules

---

*Source: Extracted from WORKTRACKER.md lines 1971-1996*
