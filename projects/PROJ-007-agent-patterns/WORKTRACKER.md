# PROJ-007: Agent Patterns — Work Tracker

> Work decomposition and progress tracking for PROJ-007.

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Project status overview |
| [Work Items](#work-items) | Entity tracking |

---

## Summary

| Metric | Value |
|--------|-------|
| Project | PROJ-007-agent-patterns |
| Status | IN PROGRESS |
| Created | 2026-02-21 |
| Orchestration | `agent-patterns-20260221-001` |
| Criticality | C4 (Critical) |
| Quality Threshold | >= 0.95 |
| Progress | 98% (Orchestration COMPLETE, EN-002 COMPLETE, EN-001 DONE — PR pending) |

## Work Items

| ID | Type | Title | Status | Parent |
|----|------|-------|--------|--------|
| TASK-001 | Task | Phase 1: Research (4 agents: 3 PS + 1 NSE) | DONE | — |
| TASK-002 | Task | Barrier 1: Research cross-pollination | DONE | — |
| TASK-003 | Task | Phase 2: Analysis (6 agents: 3 PS + 3 NSE) | DONE | — |
| TASK-004 | Task | Barrier 2: Analysis cross-pollination | DONE | — |
| TASK-005 | Task | Phase 3: Synthesis & Design (5 agents: 3 PS + 2 NSE) | DONE | — |
| TASK-006 | Task | Barrier 3: Synthesis cross-pollination + ADR quality gate | DONE | — |
| TASK-007 | Task | Phase 4: Codification (4 agents: 2 PS seq + 2 NSE seq) | DONE | TASK-006 |
| TASK-008 | Task | Barrier 4: Codification cross-pollination + rule file quality gate | DONE | TASK-007 |
| TASK-009 | Task | Phase 5: Review & Quality Gate (5 agents: 3 PS + 2 NSE) | DONE | TASK-008 |
| TASK-010 | Task | C4 Adversary Tournament (10 strategies) | DONE | TASK-009 |
| TASK-011 | Task | Final synthesis + commit | DONE | TASK-010 |

### Barrier 3 Sub-tasks

| ID | Type | Title | Status | Parent |
|----|------|-------|--------|--------|
| TASK-006a | Task | PS-to-NSE handoff (pattern taxonomy + 2 ADRs) | DONE | TASK-006 |
| TASK-006b | Task | NSE-to-PS handoff (V&V plan + integration patterns) | DONE | TASK-006 |
| TASK-006c | Task | ADR quality gate scoring iteration 1 (FAIL: 0.91/0.90) | DONE | TASK-006 |
| TASK-006e | Task | ADR-001 revision (5 items: schema validation, CB traceability, H-07, PR-004/006, MCP coupling) | DONE | TASK-006 |
| TASK-006f | Task | ADR-002 revision (5 items: compound triggers, coverage caveats, LLM threshold, AP temporal, observability scope) | DONE | TASK-006 |
| TASK-006g | Task | ADR quality gate re-scoring iteration 2 | DONE | TASK-006 |
| TASK-006d | Task | Update ORCHESTRATION.yaml barrier-3 status | DONE | TASK-006g |

### Phase 4 Sub-tasks

| ID | Type | Title | Status | Parent |
|----|------|-------|--------|--------|
| TASK-007a | Task | ps-architect-003: Create 2 rule files (agent-development + agent-routing) | DONE | TASK-007 |
| TASK-007b | Task | nse-configuration-001: Config baseline (APB-1.0.0) | DONE | TASK-007 |
| TASK-007c | Task | ps-validator-001: Constitutional compliance validation | DONE | TASK-007 |
| TASK-007d | Task | nse-qa-001: QA audit of all Phase 1-4 deliverables | DONE | TASK-007 |

### Barrier 4 Sub-tasks

| ID | Type | Title | Status | Parent |
|----|------|-------|--------|--------|
| TASK-008a | Task | PS-to-NSE handoff (rule files + validation report) | DONE | TASK-008 |
| TASK-008b | Task | NSE-to-PS handoff (config baseline + QA audit) | DONE | TASK-008 |
| TASK-008c | Task | Rule file quality gate scoring iteration 1 (FAIL: 0.938/0.934) | DONE | TASK-008 |
| TASK-008d | Task | agent-development-standards revision (7 items: CB derivation, H-32 impl note, 15-tool source, CB enforcement, guardrails template, HD-M MUST, confidence calibration) | DONE | TASK-008 |
| TASK-008e | Task | agent-routing-standards revision (7 items: 3-hop derivation, 20-skill derivation, priority rationale, 2-level gap, trigger map migration, failure propagation, FMEA measurability) | DONE | TASK-008 |
| TASK-008f | Task | Rule file quality gate re-scoring iteration 2 (PASS: 0.960/0.958) | DONE | TASK-008d, TASK-008e |
| TASK-008g | Task | Update ORCHESTRATION.yaml barrier-4 status | DONE | TASK-008f |

### Phase 5 Sub-tasks

| ID | Type | Title | Status | Parent |
|----|------|-------|--------|--------|
| TASK-009a | Task | ps-reviewer-001: Design review (APPROVED WITH CONDITIONS) | DONE | TASK-009 |
| TASK-009b | Task | ps-critic-001: Quality scoring (ALL PASS, avg 0.957) | DONE | TASK-009 |
| TASK-009c | Task | ps-reporter-001: Final report (650 lines, 12 sections) | DONE | TASK-009 |
| TASK-009d | Task | nse-reviewer-001: CDR gate review (CONDITIONAL GO) | DONE | TASK-009 |
| TASK-009e | Task | nse-reporter-001: SE report (733 lines, SE health 0.936) | DONE | TASK-009 |

### C4 Tournament Sub-tasks

| ID | Type | Title | Status | Parent |
|----|------|-------|--------|--------|
| TASK-010a | Task | Apply S-001 Red Team + S-011 CoVe to 4 deliverables | DONE | TASK-010 |
| TASK-010b | Task | Tournament verdict: CONDITIONAL PASS at 0.952 (3 conditions) | DONE | TASK-010 |

### Final Synthesis Sub-tasks

| ID | Type | Title | Status | Parent |
|----|------|-------|--------|--------|
| TASK-011a | Task | Create final synthesis document (538 lines, 11 sections) | DONE | TASK-011 |
| TASK-011b | Task | Update ORCHESTRATION.yaml to COMPLETE | DONE | TASK-011 |

### Implementation: EN-001 — Install Deliverables into Framework

| ID | Type | Title | Status | Parent | Criticality |
|----|------|-------|--------|--------|-------------|
| EN-001 | Enabler | Install PROJ-007 Agent Pattern Deliverables into Framework | DONE | PROJ-007 | C3 |
| TASK-012 | Task | Install agent-development-standards.md into .context/rules/ + hardlink | DONE | EN-001 | C3 |
| TASK-013 | Task | Install agent-routing-standards.md into .context/rules/ + hardlink | DONE | EN-001 | C3 |
| TASK-014 | Task | Install ADR-PROJ007-001 (Agent Design) into docs/design/ | DONE | EN-001 | C3 |
| TASK-015 | Task | Install ADR-PROJ007-002 (Routing Framework) into docs/design/ | DONE | EN-001 | C3 |
| TASK-016 | Task | Integrate H-34..H-36 into quality-enforcement.md HARD rule index (compound consolidation) | DONE | EN-001 | C3 |
| TASK-017 | Task | Install pattern taxonomy into docs/knowledge/ | DONE | EN-001 | C2 |
| TASK-018 | Task | Generate agent-definition-v1.schema.json from ADR-001 | DONE | EN-001 | C2 |
| TASK-019 | Task | Update CLAUDE.md navigation table for new rules | DONE | EN-001 | C2 |
| TASK-020 | Task | Update mandatory-skill-usage.md trigger map (Phase 0→1 migration) | DONE | EN-001 | C3 |
| TASK-021 | Task | Final validation + commit + PR | DONE | EN-001 | C3 |

### EN-002 — HARD Rule Budget Enforcement Improvement

| ID | Type | Title | Status | Parent | Criticality |
|----|------|-------|--------|--------|-------------|
| EN-002 | Enabler | Implement HARD Rule Budget Enforcement Improvements | DONE | PROJ-007 | C3 |
| DISC-001 | Discovery | HARD Rule Budget Ceiling Has No Principled Derivation | VALIDATED | EN-002 | — |
| DISC-002 | Discovery | L2 Prompt Reinforcement Engine Coverage Gap | VALIDATED | EN-002 | — |
| DEC-001 | Decision | HARD Rule Budget Implementation Plan (5 decisions) | ACCEPTED | EN-002 | — |
| TASK-022 | Task | Expand L2 engine to read all auto-loaded rule files | DONE | EN-002 | C3 |
| TASK-023 | Task | Consolidate H-25..H-30 into 2 compound rules | DONE | EN-002 | C3 |
| TASK-024 | Task | Consolidate H-07..H-09 into 1 compound rule | DONE | EN-002 | C3 |
| TASK-025 | Task | Classify rules into Tier A/B (L2 markers deferred per DEC-005) | DONE | EN-002 | C3 |
| TASK-026 | Task | Update ceiling 35→25, two-tier model + exception mechanism | DONE | EN-002 | C3 |
| TASK-027 | Task | Add L5 CI enforcement gate for HARD rule ceiling | DONE | EN-002 | C3 |
| TASK-028 | Task | Measure enforcement effectiveness | DONE | EN-002 | C2 |

### Bugs

| ID | Type | Title | Status | Parent |
|----|------|-------|--------|--------|
| BUG-001 | Bug | Orchestration scaffold creates cartesian product of empty directories | PENDING | PROJ-007 |

### Artifact Inventory (33 of 33)

| Phase | Artifacts | Count |
|-------|-----------|-------|
| Phase 1 | 3 PS research + 1 NSE exploration | 4 |
| Barrier 1 | PS→NSE handoff + NSE→PS handoff | 2 |
| Phase 2 | 3 PS analysis + 3 NSE analysis | 6 |
| Barrier 2 | PS→NSE handoff + NSE→PS handoff | 2 |
| Phase 3 | 3 PS synthesis + 2 NSE synthesis | 5 |
| Barrier 3 | PS→NSE handoff + NSE→PS handoff | 2 |
| Phase 4 | 2 PS rule files + 1 PS validation + 1 NSE config + 1 NSE audit | 4 |
| Barrier 4 | PS→NSE handoff + NSE→PS handoff + quality gate report | 3 |
| Phase 5 | 3 PS reviews + 2 NSE reviews | 5 |
| C4 Tournament | Tournament report (10/10 strategies) | 1 |
| Final Synthesis | Project synthesis document | 1 |
| **Total created** | | **33** |
| **Total planned** | | **33** |
