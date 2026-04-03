# PROJ-022: /user-experience Skill — Work Tracker

> **Project:** PROJ-022-user-experience-skill
> **Status:** ACTIVE
> **Created:** 2026-03-03
> **GitHub Issue:** [#138](https://github.com/geekatron/jerry/issues/138) *(tracks the decision to build the skill, not implementation status; GH #138 CLOSED reflects decision approval, not implementation completion)*

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | Project overview and progress |
| [Epics](#epics) | Top-level work decomposition |
| [EPIC-001 Foundation](#epic-001-foundation-parent-orchestrator) | Parent skill, orchestrator agent, rules, templates |
| [EPIC-002 Wave 1](#epic-002-wave-1-heuristic-eval--jtbd) | `/ux-heuristic-eval` + `/ux-jtbd` |
| [EPIC-003 Wave 2](#epic-003-wave-2-lean-ux--heart-metrics) | `/ux-lean-ux` + `/ux-heart-metrics` |
| [EPIC-004 Wave 3](#epic-004-wave-3-atomic-design--inclusive-design) | `/ux-atomic-design` + `/ux-inclusive-design` |
| [EPIC-005 Wave 4](#epic-005-wave-4-behavior-design--kano-model) | `/ux-behavior-design` + `/ux-kano-model` |
| [EPIC-006 Wave 5](#epic-006-wave-5-design-sprint--ai-first-design) | `/ux-design-sprint` + `/ux-ai-first-design` (COND) |
| [EPIC-007 Integration](#epic-007-integration-and-validation) | Cross-framework testing, purple team |
| [EPIC-008 Registration](#epic-008-registration-and-documentation) | CLAUDE.md, AGENTS.md, trigger map |
| [Active Work](#active-work) | Current in-progress items |

---

## Summary

| Metric | Value |
|--------|-------|
| Total Epics | 8 |
| Epics Complete | 0 |
| Total Features | 26 |
| Features Complete | 0 |
| Total Artifacts | ~72 |
| Quality Gate | C4 >= 0.95 |

---

## Epics

| Epic | Title | Status | Dependencies | Features |
|------|-------|--------|-------------|----------|
| EPIC-001 | Foundation: Parent Orchestrator | NOT STARTED | None | 4 |
| EPIC-002 | Wave 1: Heuristic Eval + JTBD | NOT STARTED | EPIC-001 | 4 |
| EPIC-003 | Wave 2: Lean UX + HEART Metrics | NOT STARTED | EPIC-002 | 4 |
| EPIC-004 | Wave 3: Atomic Design + Inclusive Design | NOT STARTED | EPIC-003 | 4 |
| EPIC-005 | Wave 4: Behavior Design + Kano Model | NOT STARTED | EPIC-004 | 2 |
| EPIC-006 | Wave 5: Design Sprint + AI-First Design | NOT STARTED | EPIC-005 | 4 |
| EPIC-007 | Integration and Validation | NOT STARTED | EPIC-002 | 2 |
| EPIC-008 | Registration and Documentation | NOT STARTED | EPIC-001 | 2 |

---

## EPIC-001: Foundation: Parent Orchestrator

> **Status:** NOT STARTED | **Dependencies:** None

### Features

| Feature | Title | Status | Artifacts |
|---------|-------|--------|-----------|
| FEAT-001 | Parent SKILL.md + Orchestrator Agent | NOT STARTED | 3 |
| FEAT-002 | Routing and Governance Rules | NOT STARTED | 5 |
| FEAT-003 | Templates | NOT STARTED | 2 |
| FEAT-004 | Kickoff Signoff | NOT STARTED | 1 |

### FEAT-001: Parent SKILL.md + Orchestrator Agent

| Artifact | Output Path | Status |
|----------|------------|--------|
| Parent SKILL.md | `skills/user-experience/SKILL.md` | NOT STARTED |
| Orchestrator agent definition | `skills/user-experience/agents/ux-orchestrator.md` | NOT STARTED |
| Orchestrator governance YAML | `skills/user-experience/agents/ux-orchestrator.governance.yaml` | NOT STARTED |

### FEAT-002: Routing and Governance Rules

| Artifact | Output Path | Status |
|----------|------------|--------|
| Routing rules (lifecycle-stage triage) | `skills/user-experience/rules/ux-routing-rules.md` | NOT STARTED |
| Synthesis validation (3-tier confidence) | `skills/user-experience/rules/synthesis-validation.md` | NOT STARTED |
| Wave progression rules | `skills/user-experience/rules/wave-progression.md` | NOT STARTED |
| MCP coordination registry | `skills/user-experience/rules/mcp-coordination.md` | NOT STARTED |
| CI checks (P-003 enforcement) | `skills/user-experience/rules/ci-checks.md` | NOT STARTED |

### FEAT-003: Templates

| Artifact | Output Path | Status |
|----------|------------|--------|
| Kickoff signoff template | `skills/user-experience/templates/kickoff-signoff-template.md` | NOT STARTED |
| Wave signoff template | `skills/user-experience/templates/wave-signoff-template.md` | NOT STARTED |

### FEAT-004: Kickoff Signoff

| Artifact | Output Path | Status |
|----------|------------|--------|
| KICKOFF-SIGNOFF.md (completed) | `skills/user-experience/work/KICKOFF-SIGNOFF.md` | NOT STARTED |

---

## EPIC-002: Wave 1: Heuristic Eval + JTBD

> **Status:** NOT STARTED | **Dependencies:** EPIC-001 (KICKOFF-SIGNOFF.md)

### Features

| Feature | Title | Status | Artifacts |
|---------|-------|--------|-----------|
| FEAT-005 | `/ux-heuristic-eval` Sub-Skill | NOT STARTED | 5 |
| FEAT-006 | `/ux-jtbd` Sub-Skill | NOT STARTED | 5 |
| FEAT-007 | Wave 1 Cross-Framework Testing | NOT STARTED | 1 |
| FEAT-008 | Wave 1 Signoff | NOT STARTED | 1 |

### FEAT-005: `/ux-heuristic-eval` Sub-Skill

> Agent: `ux-heuristic-evaluator` | Tier: T3 | Mode: Systematic | Model: Haiku (benchmark-gated, escalate to Sonnet)

| Artifact | Output Path | Status |
|----------|------------|--------|
| SKILL.md | `skills/ux-heuristic-eval/SKILL.md` | NOT STARTED |
| Agent definition | `skills/ux-heuristic-eval/agents/ux-heuristic-evaluator.md` | NOT STARTED |
| Governance YAML | `skills/ux-heuristic-eval/agents/ux-heuristic-evaluator.governance.yaml` | NOT STARTED |
| Heuristic evaluation rules + MCP runbook | `skills/ux-heuristic-eval/rules/heuristic-evaluation-rules.md`, `skills/ux-heuristic-eval/rules/mcp-runbook.md` | NOT STARTED |
| Report template | `skills/ux-heuristic-eval/templates/heuristic-report-template.md` | NOT STARTED |

### FEAT-006: `/ux-jtbd` Sub-Skill

> Agent: `ux-jtbd-analyst` | Tier: T3 | Mode: Divergent | Model: Sonnet

| Artifact | Output Path | Status |
|----------|------------|--------|
| SKILL.md | `skills/ux-jtbd/SKILL.md` | NOT STARTED |
| Agent definition | `skills/ux-jtbd/agents/ux-jtbd-analyst.md` | NOT STARTED |
| Governance YAML | `skills/ux-jtbd/agents/ux-jtbd-analyst.governance.yaml` | NOT STARTED |
| JTBD methodology rules | `skills/ux-jtbd/rules/jtbd-methodology-rules.md` | NOT STARTED |
| Templates (job statement + switch interview) | `skills/ux-jtbd/templates/job-statement-template.md`, `skills/ux-jtbd/templates/switch-interview-guide.md` | NOT STARTED |

### FEAT-007: Wave 1 Cross-Framework Testing

| Artifact | Output Path | Status |
|----------|------------|--------|
| Cross-framework test results (JTBD->Sprint, LeanUX->HEART) | `skills/user-experience/work/wave-1-cross-framework-tests.md` | NOT STARTED |

### FEAT-008: Wave 1 Signoff

| Artifact | Output Path | Status |
|----------|------------|--------|
| WAVE-1-SIGNOFF.md | `skills/user-experience/work/WAVE-1-SIGNOFF.md` | NOT STARTED |

---

## EPIC-003: Wave 2: Lean UX + HEART Metrics

> **Status:** NOT STARTED | **Dependencies:** EPIC-002 (WAVE-1-SIGNOFF.md)

### Features

| Feature | Title | Status | Artifacts |
|---------|-------|--------|-----------|
| FEAT-009 | `/ux-lean-ux` Sub-Skill | NOT STARTED | 5 |
| FEAT-010 | `/ux-heart-metrics` Sub-Skill | NOT STARTED | 4 |
| FEAT-011 | Wave 2 Cross-Framework Testing | NOT STARTED | 1 |
| FEAT-012 | Wave 2 Signoff | NOT STARTED | 1 |

### FEAT-009: `/ux-lean-ux` Sub-Skill

> Agent: `ux-lean-ux-facilitator` | Tier: T3 | Mode: Systematic | Model: Sonnet

| Artifact | Output Path | Status |
|----------|------------|--------|
| SKILL.md | `skills/ux-lean-ux/SKILL.md` | NOT STARTED |
| Agent definition | `skills/ux-lean-ux/agents/ux-lean-ux-facilitator.md` | NOT STARTED |
| Governance YAML | `skills/ux-lean-ux/agents/ux-lean-ux-facilitator.governance.yaml` | NOT STARTED |
| Lean UX rules + MCP runbook | `skills/ux-lean-ux/rules/lean-ux-methodology-rules.md`, `skills/ux-lean-ux/rules/mcp-runbook.md` | NOT STARTED |
| Templates (hypothesis backlog + assumption map) | `skills/ux-lean-ux/templates/hypothesis-backlog-template.md`, `skills/ux-lean-ux/templates/assumption-map-template.md` | NOT STARTED |

### FEAT-010: `/ux-heart-metrics` Sub-Skill

> Agent: `ux-heart-analyst` | Tier: T2 | Mode: Systematic | Model: Sonnet

| Artifact | Output Path | Status |
|----------|------------|--------|
| SKILL.md | `skills/ux-heart-metrics/SKILL.md` | NOT STARTED |
| Agent definition | `skills/ux-heart-metrics/agents/ux-heart-analyst.md` | NOT STARTED |
| Governance YAML | `skills/ux-heart-metrics/agents/ux-heart-analyst.governance.yaml` | NOT STARTED |
| HEART methodology rules | `skills/ux-heart-metrics/rules/heart-methodology-rules.md` | NOT STARTED |

> Note: HEART GSM template bundled into methodology rules (single deliverable).

### FEAT-011: Wave 2 Cross-Framework Testing

| Artifact | Output Path | Status |
|----------|------------|--------|
| Cross-framework test results | `skills/user-experience/work/wave-2-cross-framework-tests.md` | NOT STARTED |

### FEAT-012: Wave 2 Signoff

| Artifact | Output Path | Status |
|----------|------------|--------|
| WAVE-2-SIGNOFF.md | `skills/user-experience/work/WAVE-2-SIGNOFF.md` | NOT STARTED |

---

## EPIC-004: Wave 3: Atomic Design + Inclusive Design

> **Status:** NOT STARTED | **Dependencies:** EPIC-003 (WAVE-2-SIGNOFF.md)

### Features

| Feature | Title | Status | Artifacts |
|---------|-------|--------|-----------|
| FEAT-013 | `/ux-atomic-design` Sub-Skill | NOT STARTED | 5 |
| FEAT-014 | `/ux-inclusive-design` Sub-Skill | NOT STARTED | 6 |
| FEAT-015 | Wave 3 Cross-Framework Testing | NOT STARTED | 1 |
| FEAT-016 | Wave 3 Signoff | NOT STARTED | 1 |

### FEAT-013: `/ux-atomic-design` Sub-Skill

> Agent: `ux-atomic-architect` | Tier: T3 | Mode: Systematic | Model: Sonnet

| Artifact | Output Path | Status |
|----------|------------|--------|
| SKILL.md | `skills/ux-atomic-design/SKILL.md` | NOT STARTED |
| Agent definition | `skills/ux-atomic-design/agents/ux-atomic-architect.md` | NOT STARTED |
| Governance YAML | `skills/ux-atomic-design/agents/ux-atomic-architect.governance.yaml` | NOT STARTED |
| Atomic design rules + MCP runbook | `skills/ux-atomic-design/rules/atomic-design-rules.md`, `skills/ux-atomic-design/rules/mcp-runbook.md` | NOT STARTED |
| Component inventory template | `skills/ux-atomic-design/templates/component-inventory-template.md` | NOT STARTED |

### FEAT-014: `/ux-inclusive-design` Sub-Skill

> Agent: `ux-inclusive-evaluator` | Tier: T3 | Mode: Systematic | Model: Sonnet

| Artifact | Output Path | Status |
|----------|------------|--------|
| SKILL.md | `skills/ux-inclusive-design/SKILL.md` | NOT STARTED |
| Agent definition | `skills/ux-inclusive-design/agents/ux-inclusive-evaluator.md` | NOT STARTED |
| Governance YAML | `skills/ux-inclusive-design/agents/ux-inclusive-evaluator.governance.yaml` | NOT STARTED |
| Inclusive design rules + MCP runbook | `skills/ux-inclusive-design/rules/inclusive-design-rules.md`, `skills/ux-inclusive-design/rules/mcp-runbook.md` | NOT STARTED |
| Persona spectrum template | `skills/ux-inclusive-design/templates/persona-spectrum-template.md` | NOT STARTED |
| Accessibility report template | `skills/ux-inclusive-design/templates/accessibility-report-template.md` | NOT STARTED |

### FEAT-015: Wave 3 Cross-Framework Testing

| Artifact | Output Path | Status |
|----------|------------|--------|
| Cross-framework test results | `skills/user-experience/work/wave-3-cross-framework-tests.md` | NOT STARTED |

### FEAT-016: Wave 3 Signoff

| Artifact | Output Path | Status |
|----------|------------|--------|
| WAVE-3-SIGNOFF.md | `skills/user-experience/work/WAVE-3-SIGNOFF.md` | NOT STARTED |

---

## EPIC-005: Wave 4: Behavior Design + Kano Model

> **Status:** NOT STARTED | **Dependencies:** EPIC-004 (WAVE-3-SIGNOFF.md)

### Features

| Feature | Title | Status | Artifacts |
|---------|-------|--------|-----------|
| FEAT-017 | `/ux-behavior-design` Sub-Skill | NOT STARTED | 5 |
| FEAT-018 | `/ux-kano-model` Sub-Skill | NOT STARTED | 5 |

> Note: Wave 4 signoff bundled into EPIC-006 entry criteria validation.

### FEAT-017: `/ux-behavior-design` Sub-Skill

> Agent: `ux-behavior-diagnostician` | Tier: T2 | Mode: Convergent | Model: Sonnet

| Artifact | Output Path | Status |
|----------|------------|--------|
| SKILL.md | `skills/ux-behavior-design/SKILL.md` | NOT STARTED |
| Agent definition | `skills/ux-behavior-design/agents/ux-behavior-diagnostician.md` | NOT STARTED |
| Governance YAML | `skills/ux-behavior-design/agents/ux-behavior-diagnostician.governance.yaml` | NOT STARTED |
| Fogg behavior rules | `skills/ux-behavior-design/rules/fogg-behavior-rules.md` | NOT STARTED |
| B=MAP diagnosis template | `skills/ux-behavior-design/templates/bmap-diagnosis-template.md` | NOT STARTED |

### FEAT-018: `/ux-kano-model` Sub-Skill

> Agent: `ux-kano-analyst` | Tier: T2 | Mode: Convergent | Model: Sonnet

| Artifact | Output Path | Status |
|----------|------------|--------|
| SKILL.md | `skills/ux-kano-model/SKILL.md` | NOT STARTED |
| Agent definition | `skills/ux-kano-model/agents/ux-kano-analyst.md` | NOT STARTED |
| Governance YAML | `skills/ux-kano-model/agents/ux-kano-analyst.governance.yaml` | NOT STARTED |
| Kano methodology rules | `skills/ux-kano-model/rules/kano-methodology-rules.md` | NOT STARTED |
| Templates (survey + feature priority) | `skills/ux-kano-model/templates/kano-survey-template.md`, `skills/ux-kano-model/templates/feature-priority-template.md` | NOT STARTED |

---

## EPIC-006: Wave 5: Design Sprint + AI-First Design

> **Status:** NOT STARTED | **Dependencies:** EPIC-005 (WAVE-4-SIGNOFF.md)

### Features

| Feature | Title | Status | Artifacts |
|---------|-------|--------|-----------|
| FEAT-019 | `/ux-design-sprint` Sub-Skill | NOT STARTED | 5 |
| FEAT-020 | `/ux-ai-first-design` Sub-Skill (CONDITIONAL) | NOT STARTED | 5 |
| FEAT-021 | Wave 4 Signoff | NOT STARTED | 1 |
| FEAT-022 | Wave 5 Signoff | NOT STARTED | 1 |

### FEAT-019: `/ux-design-sprint` Sub-Skill

> Agent: `ux-sprint-facilitator` | Tier: T3 | Mode: Systematic | Model: Opus

| Artifact | Output Path | Status |
|----------|------------|--------|
| SKILL.md | `skills/ux-design-sprint/SKILL.md` | NOT STARTED |
| Agent definition | `skills/ux-design-sprint/agents/ux-sprint-facilitator.md` | NOT STARTED |
| Governance YAML | `skills/ux-design-sprint/agents/ux-sprint-facilitator.governance.yaml` | NOT STARTED |
| Design sprint rules + MCP runbook | `skills/ux-design-sprint/rules/design-sprint-rules.md`, `skills/ux-design-sprint/rules/mcp-runbook.md` | NOT STARTED |
| Sprint day templates (Day 1-4) | `skills/ux-design-sprint/templates/sprint-day-*.md` | NOT STARTED |

### FEAT-020: `/ux-ai-first-design` Sub-Skill (CONDITIONAL)

> Agent: `ux-ai-design-guide` | Tier: T3 | Mode: Divergent | Model: Opus
> **Condition:** Enabler DONE + WSM >= 7.80

| Artifact | Output Path | Status |
|----------|------------|--------|
| SKILL.md | `skills/ux-ai-first-design/SKILL.md` | NOT STARTED |
| Agent definition | `skills/ux-ai-first-design/agents/ux-ai-design-guide.md` | NOT STARTED |
| Governance YAML | `skills/ux-ai-first-design/agents/ux-ai-design-guide.governance.yaml` | NOT STARTED |
| AI-first design rules + MCP runbook | `skills/ux-ai-first-design/rules/ai-first-design-rules.md`, `skills/ux-ai-first-design/rules/mcp-runbook.md` | NOT STARTED |
| AI interaction spec template | `skills/ux-ai-first-design/templates/ai-interaction-spec-template.md` | NOT STARTED |

### FEAT-021: Wave 4 Signoff

| Artifact | Output Path | Status |
|----------|------------|--------|
| WAVE-4-SIGNOFF.md | `skills/user-experience/work/WAVE-4-SIGNOFF.md` | NOT STARTED |

### FEAT-022: Wave 5 Signoff

| Artifact | Output Path | Status |
|----------|------------|--------|
| WAVE-5-SIGNOFF.md | `skills/user-experience/work/WAVE-5-SIGNOFF.md` | NOT STARTED |

---

## EPIC-007: Integration and Validation

> **Status:** NOT STARTED | **Dependencies:** EPIC-002 (minimum)

### Features

| Feature | Title | Status | Artifacts |
|---------|-------|--------|-----------|
| FEAT-023 | Cross-Framework Handoff Testing | NOT STARTED | 2 |
| FEAT-024 | Purple Team Security Testing | NOT STARTED | 1 |

### FEAT-023: Cross-Framework Handoff Testing

| Artifact | Output Path | Status |
|----------|------------|--------|
| Canonical sequence tests (JTBD->Sprint, LeanUX->HEART) | `skills/user-experience/work/cross-framework-handoff-tests.md` | NOT STARTED |
| Failure mode documentation | `skills/user-experience/work/failure-mode-documentation.md` | NOT STARTED |

### FEAT-024: Purple Team Security Testing

| Artifact | Output Path | Status |
|----------|------------|--------|
| Purple team test results (MCP OAuth, P-003, credential, synthesis, wave bypass) | `skills/user-experience/work/purple-team-results.md` | NOT STARTED |

---

## EPIC-008: Registration and Documentation

> **Status:** NOT STARTED | **Dependencies:** EPIC-001

### Features

| Feature | Title | Status | Artifacts |
|---------|-------|--------|-----------|
| FEAT-025 | Framework Registration | NOT STARTED | 3 |
| FEAT-026 | Metrics Plan | NOT STARTED | 1 |

### FEAT-025: Framework Registration

| Artifact | Output Path | Status |
|----------|------------|--------|
| CLAUDE.md skill table update | `CLAUDE.md` | NOT STARTED |
| AGENTS.md registry (11 agents) | `AGENTS.md` | NOT STARTED |
| Trigger map update | `.context/rules/mandatory-skill-usage.md` | NOT STARTED |

### FEAT-026: Metrics Plan

| Artifact | Output Path | Status |
|----------|------------|--------|
| Post-launch metrics measurement plan | `skills/user-experience/rules/metrics-plan.md` | NOT STARTED |

---

## Active Work

No items currently in progress. Begin with EPIC-001 Foundation.

---

*Last Updated: 2026-03-03*
