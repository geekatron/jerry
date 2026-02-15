# ORCHESTRATION_PLAN.md

> **Document ID:** PROJ-001-ORCH-PLAN-FEAT009
> **Project:** PROJ-001-oss-release
> **Workflow ID:** feat009-adversarial-20260215-001
> **Status:** ACTIVE
> **Version:** 1.0
> **Created:** 2026-02-15
> **Updated:** 2026-02-15

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Executive Summary](#executive-summary) | High-level overview and objectives |
| [Workflow Architecture](#workflow-architecture) | Pipeline structure and phase diagram |
| [Phase Definitions](#phase-definitions) | Detailed phase breakdown with enablers |
| [Adversarial Review Protocol](#adversarial-review-protocol) | Creator-critic-revision cycle specification |
| [Phase Gate Protocol](#phase-gate-protocol) | Gate criteria and transition rules |
| [Agent Registry](#agent-registry) | Agent assignments by phase |
| [State Management](#state-management) | Paths, checkpoints, artifact structure |
| [Execution Constraints](#execution-constraints) | Constitutional and resource limits |
| [Success Criteria](#success-criteria) | Definition of done for FEAT-009 |
| [Risk Mitigations](#risk-mitigations) | Identified risks and countermeasures |
| [Resumption Context](#resumption-context) | Recovery and session continuity |

---

## Executive Summary

**FEAT-009 creates adversarial strategy templates and the `/adversary` skill for the Jerry quality framework.**

EPIC-002 selected 10 adversarial strategies (S-001 through S-014, excluding 5). EPIC-003/FEAT-008 implemented the enforcement architecture. FEAT-009 provides the operational templates that agents use to EXECUTE those strategies, plus a dedicated `/adversary` skill for invocation.

FEAT-009 produces:
- Canonical template format standard (8-section structure)
- 10 adversarial strategy templates (one per selected strategy from ADR-EPIC002-001)
- `/adversary` skill with SKILL.md, PLAYBOOK.md, and 3 specialized agents
- Integration updates to 4 existing agent/skill files
- E2E integration tests validating template compliance and skill invocation

**Criticality:** C2 (Standard) -- 3-10 files per enabler, reversible within 1 day, module-level impact.

**Pattern:** Sequential 7-Phase Pipeline with Parallel Fan-Out + Adversarial Review per enabler.

**Scale:** 1 pipeline, 7 phases, 12 enablers (EN-801 through EN-812), 36 execution groups, 46 effort points.

---

## Workflow Architecture

### Pipeline Diagram

```
+-----------------------------------------------------------------------+
|          FEAT-009: Adversarial Strategy Templates & /adversary Skill    |
|          Pattern: Sequential + Fan-Out + Adversarial Review            |
+-----------------------------------------------------------------------+
|                                                                        |
|  PHASE 1: FOUNDATION (Parallel)                                 6 pts |
|  +------------+    +------------+                                      |
|  |  EN-801    |    |  EN-802    |   Fan-out: parallel execution        |
|  |  Template  |    |  /adversary|                                      |
|  |  Format    |    |  Skeleton  |                                      |
|  |  (3 pts)   |    |  (3 pts)   |                                      |
|  +------------+    +------------+                                      |
|        |                 |                                             |
|        v                 v                                             |
|  ==========================================  GATE 1  ==============   |
|                                                                        |
|  PHASE 2: TIER 1 STRATEGY TEMPLATES (Parallel 3-way)           11 pts |
|  +------------+  +------------+  +------------+                        |
|  |  EN-803    |  |  EN-804    |  |  EN-805    |  Fan-out: 3 parallel   |
|  |  S-014     |  |  S-010     |  |  S-007     |                        |
|  |  LLM Judge |  |  Self-     |  |  Const.    |                        |
|  |  (5 pts)   |  |  Refine    |  |  AI        |                        |
|  |            |  |  (3 pts)   |  |  (3 pts)   |                        |
|  +------------+  +------------+  +------------+                        |
|        |              |              |                                  |
|        v              v              v                                  |
|  ==========================================  GATE 2  ==============   |
|                                                                        |
|  PHASE 3: TIER 2 STRATEGY TEMPLATES (Parallel)                  6 pts |
|  +------------+    +------------+                                      |
|  |  EN-806    |    |  EN-807    |   Fan-out: parallel execution        |
|  |  S-002     |    |  S-003     |                                      |
|  |  Devil's   |    |  Steelman  |                                      |
|  |  Advocate  |    |            |                                      |
|  |  (3 pts)   |    |  (3 pts)   |                                      |
|  +------------+    +------------+                                      |
|        |                 |                                             |
|        v                 v                                             |
|  ==========================================  GATE 3  ==============   |
|                                                                        |
|  PHASE 4: TIER 3 RISK STRATEGY TEMPLATES (Sequential)           5 pts |
|  +--------------------------------------+                              |
|  |  EN-808                              |                              |
|  |  S-004 Pre-Mortem + S-012 FMEA       |                              |
|  |  + S-013 Inversion (3 templates)     |                              |
|  |  (5 pts)                             |                              |
|  +--------------------------------------+                              |
|        |                                                               |
|        v                                                               |
|  ==========================================  GATE 4  ==============   |
|                                                                        |
|  PHASE 5: TIER 4 SECURITY STRATEGY TEMPLATES (Sequential)       3 pts |
|  +--------------------------------------+                              |
|  |  EN-809                              |                              |
|  |  S-001 Red Team + S-011 CoVe         |                              |
|  |  (2 templates)                       |                              |
|  |  (3 pts)                             |                              |
|  +--------------------------------------+                              |
|        |                                                               |
|        v                                                               |
|  ==========================================  GATE 5  ==============   |
|                                                                        |
|  PHASE 6: ADVERSARY SKILL AGENTS (Sequential)                   5 pts |
|  +--------------------------------------+                              |
|  |  EN-810                              |                              |
|  |  adv-selector + adv-executor         |                              |
|  |  + adv-scorer (3 agents)             |                              |
|  |  (5 pts)                             |                              |
|  +--------------------------------------+                              |
|        |                                                               |
|        v                                                               |
|  ==========================================  GATE 6  ==============   |
|                                                                        |
|  PHASE 7: INTEGRATION (Parallel)                                 8 pts |
|  +------------+    +------------+                                      |
|  |  EN-811    |    |  EN-812    |   Fan-out: parallel execution        |
|  |  Agent     |    |  Integ.   |                                      |
|  |  Extensions|    |  Testing  |                                      |
|  |  (3 pts)   |    |  (5 pts)   |                                      |
|  +------------+    +------------+                                      |
|        |                 |                                             |
|        v                 v                                             |
|  ==========================================  GATE 7  ==============   |
|                                                                        |
|  +--------------------------------------+                              |
|  |         FINAL SYNTHESIS              |                              |
|  |  Integration Report + Lessons        |                              |
|  +--------------------------------------+                              |
|                                                                        |
+-----------------------------------------------------------------------+
```

### Adversarial Cycle Per Enabler

```
+----------+    +----------+    +----------+    +----------+
| CREATOR  |--->| CRITIC   |--->| REVISION |--->| CRITIC   |
| (build)  |    | (iter 1) |    | (fix)    |    | (iter 2) |
+----------+    +----------+    +----------+    +----------+
                                                     |
                                               >=0.92? ---> PASS
                                               <0.92?  ---> iter 3 or ESCALATE
```

---

## Phase Definitions

### Phase 1: Foundation

| Property | Value |
|----------|-------|
| **Enablers** | EN-801 (Template Format), EN-802 (Skill Skeleton) |
| **Execution** | Parallel |
| **Total Effort** | 6 points |
| **Groups** | G1-G5 |
| **Gate** | Gate 1 |

**EN-801: Template Format Standard**
- Create `.context/templates/adversarial/TEMPLATE-FORMAT.md`
- Define canonical 8-section template structure: Identity, Purpose, Prerequisites, Execution Protocol, Output Format, Scoring Rubric, Examples, Integration
- Establish naming conventions, section requirements, mandatory fields
- All subsequent templates (EN-803 through EN-809) MUST conform to this format
- Adversarial strategies: S-014 (LLM-as-Judge), S-003 (Steelman)

**EN-802: /adversary Skill Skeleton**
- Create `skills/adversary/SKILL.md` with skill metadata, purpose, invocation protocol
- Create `skills/adversary/PLAYBOOK.md` with execution workflows
- Create `skills/adversary/agents/` directory structure
- Define agent slots: adv-selector, adv-executor, adv-scorer (implemented in Phase 6)
- Adversarial strategies: S-007 (Constitutional AI), S-010 (Self-Refine)

### Phase 2: Tier 1 Strategy Templates

| Property | Value |
|----------|-------|
| **Enablers** | EN-803 (S-014), EN-804 (S-010), EN-805 (S-007) |
| **Execution** | Parallel (3-way fan-out) |
| **Total Effort** | 11 points |
| **Groups** | G6-G10 |
| **Gate** | Gate 2 |
| **Dependencies** | Phase 1 (EN-801 TEMPLATE-FORMAT.md must exist) |

**EN-803: S-014 LLM-as-Judge Template** (effort: 5)
- 6-dimension weighted rubric (Completeness, Internal Consistency, Methodological Rigor, Evidence Quality, Actionability, Traceability)
- Scoring protocol with calibration examples
- Dimension-level rubrics with 5-point scales
- Anti-leniency bias instructions
- Adversarial strategies: S-014 (LLM-as-Judge), S-013 (Inversion)

**EN-804: S-010 Self-Refine Template** (effort: 3)
- Self-review checklist with systematic pass-through protocol
- Iterative improvement loop specification
- Completion criteria and diminishing-returns detection
- Adversarial strategies: S-010 (Self-Refine), S-003 (Steelman)

**EN-805: S-007 Constitutional AI Template** (effort: 3)
- Principle-by-principle review protocol against `.context/rules/`
- HARD/MEDIUM/SOFT tier compliance checking
- Violation categorization (critical, major, minor)
- Adversarial strategies: S-007 (Constitutional AI), S-002 (Devil's Advocate)

### Phase 3: Tier 2 Strategy Templates

| Property | Value |
|----------|-------|
| **Enablers** | EN-806 (S-002), EN-807 (S-003) |
| **Execution** | Parallel |
| **Total Effort** | 6 points |
| **Groups** | G11-G15 |
| **Gate** | Gate 3 |
| **Dependencies** | Phase 2 |

**EN-806: S-002 Devil's Advocate Template** (effort: 3)
- Strongest counterargument construction protocol
- Bias detection and assumption challenging
- Dialectical tension resolution
- Adversarial strategies: S-002 (Devil's Advocate), S-003 (Steelman)

**EN-807: S-003 Steelman Template** (effort: 3)
- Charitable reconstruction before critique protocol
- Strongest-version articulation of the argument
- Fair evaluation after steelmanning
- Adversarial strategies: S-003 (Steelman), S-002 (Devil's Advocate)

### Phase 4: Tier 3 Risk Strategy Templates

| Property | Value |
|----------|-------|
| **Enablers** | EN-808 (S-004 + S-012 + S-013) |
| **Execution** | Sequential |
| **Total Effort** | 5 points |
| **Groups** | G16-G18 |
| **Gate** | Gate 4 |
| **Dependencies** | Phase 3 |

**EN-808: Tier 3 Risk Strategy Templates** (effort: 5)
- S-004 Pre-Mortem Analysis template: failure mode anticipation, likelihood/impact scoring
- S-012 FMEA template: systematic failure enumeration, severity/occurrence/detection ratings, RPN calculation
- S-013 Inversion template: "what would make this fail?" protocol, anti-pattern identification
- All 3 templates MUST conform to EN-801 TEMPLATE-FORMAT.md
- Adversarial strategies: S-004 (Pre-Mortem), S-012 (FMEA), S-013 (Inversion)

### Phase 5: Tier 4 Security Strategy Templates

| Property | Value |
|----------|-------|
| **Enablers** | EN-809 (S-001 + S-011) |
| **Execution** | Sequential |
| **Total Effort** | 3 points |
| **Groups** | G19-G21 |
| **Gate** | Gate 5 |
| **Dependencies** | Phase 4 |

**EN-809: Tier 4 Security Strategy Templates** (effort: 3)
- S-001 Red Team Analysis template: adversarial attack surface identification, vulnerability probing protocol
- S-011 Chain-of-Verification (CoVe) template: claim extraction, independent verification, consistency checking
- All 10 strategy templates complete after this phase (S-001, S-002, S-003, S-004, S-007, S-010, S-011, S-012, S-013, S-014)
- Adversarial strategies: S-001 (Red Team), S-011 (CoVe)

### Phase 6: Adversary Skill Agents

| Property | Value |
|----------|-------|
| **Enablers** | EN-810 (3 agents) |
| **Execution** | Sequential |
| **Total Effort** | 5 points |
| **Groups** | G22-G24 |
| **Gate** | Gate 6 |
| **Dependencies** | Phase 5 + EN-802 (all templates + skill skeleton) |

**EN-810: Adversary Skill Agents** (effort: 5)
- **adv-selector agent:** Maps criticality level (C1-C4) to required/optional strategy sets per `quality-enforcement.md` SSOT. Selects strategies based on enabler context.
- **adv-executor agent:** Loads appropriate template by strategy ID, executes template protocol against deliverable, produces structured critique output.
- **adv-scorer agent:** Applies S-014 LLM-as-Judge rubric with 6 weighted dimensions, computes weighted composite score, renders pass/fail verdict.
- Dependencies: EN-801 (format), EN-802 (skill scaffold), EN-803-EN-809 (all 10 templates)
- Adversarial strategies: S-014 (LLM-as-Judge), S-007 (Constitutional AI)

### Phase 7: Integration

| Property | Value |
|----------|-------|
| **Enablers** | EN-811 (Agent Extensions), EN-812 (Integration Testing) |
| **Execution** | Parallel |
| **Total Effort** | 8 points |
| **Groups** | G25-G29 |
| **Gate** | Gate 7 |
| **Dependencies** | Phase 6 |

**EN-811: Agent Extensions** (effort: 3)
- Update `skills/problem-solving/agents/ps-critic.md` with template references
- Update `skills/problem-solving/agents/ps-reviewer.md` with template references
- Update `skills/nasa-se/agents/nse-reviewer.md` with template references
- Update `skills/problem-solving/agents/ps-architect.md` with template references
- Update `CLAUDE.md` with `/adversary` skill entry in Quick Reference table
- Adversarial strategies: S-003 (Steelman), S-010 (Self-Refine)

**EN-812: Integration Testing** (effort: 5)
- Template format compliance tests: all 10 templates pass TEMPLATE-FORMAT.md validation
- Strategy ID validation: all strategy IDs match `quality-enforcement.md` SSOT
- Skill invocation tests: `/adversary` skill loads and dispatches correctly
- Agent reference tests: 4 updated agents correctly reference templates
- Criticality-based selection tests: C1-C4 mapping produces correct strategy sets
- Adversarial strategies: S-012 (FMEA), S-011 (CoVe)

---

## Adversarial Review Protocol

### Cycle Structure

Each enabler undergoes a minimum of 2 adversarial iterations:

| Step | Agent | Action | Output |
|------|-------|--------|--------|
| 1 | Creator (ps-architect) | Build initial artifact | Template/code/content |
| 2 | Critic (ps-critic) iter 1 | Apply adversarial strategy | Critique with score |
| 3 | Creator (ps-architect) | Revise based on critique | Revised artifact |
| 4 | Critic (ps-critic) iter 2 | Re-evaluate revised artifact | Final score |

### Quality Scoring Rubric (S-014 LLM-as-Judge)

| Dimension | Weight | Description |
|-----------|--------|-------------|
| Completeness | 0.20 | All required sections present, no gaps |
| Internal Consistency | 0.20 | No contradictions, terminology consistent |
| Methodological Rigor | 0.20 | Protocol steps are precise, reproducible |
| Evidence Quality | 0.15 | Examples and calibration data present |
| Actionability | 0.15 | Agent can execute without ambiguity |
| Traceability | 0.10 | Links to SSOT, design sources, strategy IDs |

**Passing threshold:** Weighted composite score >= 0.92

### Strategy Assignments

| Enabler | Primary Strategy | Secondary Strategy |
|---------|-----------------|-------------------|
| EN-801 | S-014 LLM-as-Judge | S-003 Steelman |
| EN-802 | S-007 Constitutional AI | S-010 Self-Refine |
| EN-803 | S-014 LLM-as-Judge | S-013 Inversion |
| EN-804 | S-010 Self-Refine | S-003 Steelman |
| EN-805 | S-007 Constitutional AI | S-002 Devil's Advocate |
| EN-806 | S-002 Devil's Advocate | S-003 Steelman |
| EN-807 | S-003 Steelman | S-002 Devil's Advocate |
| EN-808 | S-004 Pre-Mortem | S-012 FMEA + S-013 Inversion |
| EN-809 | S-001 Red Team | S-011 CoVe |
| EN-810 | S-014 LLM-as-Judge | S-007 Constitutional AI |
| EN-811 | S-003 Steelman | S-010 Self-Refine |
| EN-812 | S-012 FMEA | S-011 CoVe |

### Escalation Rules

| Condition | Action |
|-----------|--------|
| Score >= 0.92 after iter 2 | PASS -- proceed to next group |
| Score 0.85-0.91 after iter 2 | Iter 3 with different strategy |
| Score < 0.85 after iter 2 | ESCALATE to user (P-020) |
| Score < 0.85 after iter 3 | BLOCK -- user decision required |

---

## Phase Gate Protocol

### Gate Criteria (All Gates)

| Check | Description |
|-------|-------------|
| Quality Score | All enablers in phase >= 0.92 |
| Format | All templates conform to TEMPLATE-FORMAT.md |
| Strategy IDs | All strategy IDs match quality-enforcement.md SSOT |
| Git | Clean working tree, committed |

### Gate-Specific Criteria

| Gate | Additional Criteria |
|------|-------------------|
| Gate 1 | TEMPLATE-FORMAT.md exists with 8 sections; /adversary skill scaffold exists with SKILL.md + PLAYBOOK.md + agents/ |
| Gate 2 | 3 Tier 1 templates (S-014, S-010, S-007) follow TEMPLATE-FORMAT.md; strategy IDs match SSOT |
| Gate 3 | 2 Tier 2 templates (S-002, S-003) follow TEMPLATE-FORMAT.md |
| Gate 4 | 3 Tier 3 templates (S-004, S-012, S-013) follow TEMPLATE-FORMAT.md |
| Gate 5 | 2 Tier 4 templates (S-001, S-011) follow TEMPLATE-FORMAT.md; all 10 strategy templates complete |
| Gate 6 | 3 agents (adv-selector, adv-executor, adv-scorer) reference correct templates; criticality-based selection works for C1-C4 |
| Gate 7 | 4 existing agents updated with template references; E2E tests pass; CLAUDE.md updated; all 12 enablers >= 0.92 |

### Gate Transition Rules

```
IF all_enablers_in_phase.quality_score >= 0.92
   AND format_compliance_check(TEMPLATE-FORMAT.md)
   AND strategy_id_validation(quality-enforcement.md)
   AND git_committed
THEN
   gate.status = PASSED
   next_phase.status = READY
   checkpoint.create()
ELSE
   gate.status = BLOCKED
   identify_failing_enablers()
   trigger_remediation_or_escalation()
```

---

## Agent Registry

### Phase 1 Agents

| Agent ID | Role | Enabler | Skill |
|----------|------|---------|-------|
| en801-creator | Creator | EN-801 | problem-solving |
| en801-critic | Critic | EN-801 | problem-solving |
| en802-creator | Creator | EN-802 | problem-solving |
| en802-critic | Critic | EN-802 | problem-solving |

### Phase 2 Agents

| Agent ID | Role | Enabler | Skill |
|----------|------|---------|-------|
| en803-creator | Creator | EN-803 | problem-solving |
| en803-critic | Critic | EN-803 | problem-solving |
| en804-creator | Creator | EN-804 | problem-solving |
| en804-critic | Critic | EN-804 | problem-solving |
| en805-creator | Creator | EN-805 | problem-solving |
| en805-critic | Critic | EN-805 | problem-solving |

### Phase 3 Agents

| Agent ID | Role | Enabler | Skill |
|----------|------|---------|-------|
| en806-creator | Creator | EN-806 | problem-solving |
| en806-critic | Critic | EN-806 | problem-solving |
| en807-creator | Creator | EN-807 | problem-solving |
| en807-critic | Critic | EN-807 | problem-solving |

### Phase 4 Agents

| Agent ID | Role | Enabler | Skill |
|----------|------|---------|-------|
| en808-creator | Creator | EN-808 | problem-solving |
| en808-critic | Critic | EN-808 | problem-solving |

### Phase 5 Agents

| Agent ID | Role | Enabler | Skill |
|----------|------|---------|-------|
| en809-creator | Creator | EN-809 | problem-solving |
| en809-critic | Critic | EN-809 | problem-solving |

### Phase 6 Agents

| Agent ID | Role | Enabler | Skill |
|----------|------|---------|-------|
| en810-creator | Creator | EN-810 | problem-solving |
| en810-critic | Critic | EN-810 | problem-solving |

### Phase 7 Agents

| Agent ID | Role | Enabler | Skill |
|----------|------|---------|-------|
| en811-creator | Creator | EN-811 | problem-solving |
| en811-critic | Critic | EN-811 | problem-solving |
| en812-creator | Creator | EN-812 | problem-solving |
| en812-critic | Critic | EN-812 | problem-solving |

### Synthesis Agents

| Agent ID | Role | Phase | Skill |
|----------|------|-------|-------|
| orch-synthesizer | Synthesizer | Final | orchestration |

---

## State Management

### Path Configuration

```
projects/PROJ-001-oss-release/work/EPIC-003-quality-implementation/
+-- orchestration/
|   +-- feat009-adversarial-20260215-001/  # Workflow artifacts
|   |   +-- ORCHESTRATION_PLAN.md          # This document
|   |   +-- ORCHESTRATION.yaml            # SSOT for workflow state
|   |   +-- impl/                         # Pipeline artifacts
|   |   |   +-- phase-1-foundation/
|   |   |   |   +-- ps-architect/         # EN-801, EN-802 creator
|   |   |   |   +-- ps-critic/            # EN-801, EN-802 critic
|   |   |   +-- phase-2-tier1-templates/
|   |   |   |   +-- ps-architect/         # EN-803, EN-804, EN-805
|   |   |   |   +-- ps-critic/
|   |   |   +-- phase-3-tier2-templates/
|   |   |   |   +-- ps-architect/         # EN-806, EN-807
|   |   |   |   +-- ps-critic/
|   |   |   +-- phase-4-tier3-templates/
|   |   |   |   +-- ps-architect/         # EN-808
|   |   |   |   +-- ps-critic/
|   |   |   +-- phase-5-tier4-templates/
|   |   |   |   +-- ps-architect/         # EN-809
|   |   |   |   +-- ps-critic/
|   |   |   +-- phase-6-skill-agents/
|   |   |   |   +-- ps-architect/         # EN-810
|   |   |   |   +-- ps-critic/
|   |   |   +-- phase-7-integration/
|   |   |       +-- ps-architect/         # EN-811, EN-812
|   |   |       +-- ps-critic/
|   |   +-- barriers/
|   |   |   +-- gate-1/ through gate-7/
|   |   +-- synthesis/
```

### Checkpoint Strategy

Checkpoints are created at each phase gate:

| Checkpoint | Trigger | Contents |
|------------|---------|----------|
| CP-001 | Gate 1 passed | EN-801 + EN-802 artifacts, quality scores |
| CP-002 | Gate 2 passed | EN-803 + EN-804 + EN-805 template artifacts |
| CP-003 | Gate 3 passed | EN-806 + EN-807 template artifacts |
| CP-004 | Gate 4 passed | EN-808 (3 templates) artifacts |
| CP-005 | Gate 5 passed | EN-809 (2 templates) artifacts, all 10 templates verified |
| CP-006 | Gate 6 passed | EN-810 (3 agents) artifacts |
| CP-007 | Gate 7 passed | EN-811 + EN-812 integration artifacts |

---

## Execution Constraints

### Constitutional Constraints (HARD)

| Constraint | Source | Enforcement |
|------------|--------|-------------|
| Max 1 level agent nesting | P-003 | Orchestrator -> worker only |
| All state to filesystem | P-002 | ORCHESTRATION.yaml is SSOT |
| User authority on gates | P-020 | Escalation on gate failures |
| No deception | P-022 | Transparent quality scores |

### Resource Constraints (SOFT)

| Constraint | Value | Rationale |
|------------|-------|-----------|
| Max concurrent agents | 3 | Phase 2 has 3-way fan-out |
| Max barrier retries | 2 | Circuit breaker for stuck gates |
| Checkpoint frequency | Per phase | Balance recovery vs. overhead |

### Python Environment (HARD)

| Rule | Command |
|------|---------|
| Run tests | `uv run pytest tests/` |
| Run linting | `uv run ruff check src/` |
| Run CLI | `uv run jerry <command>` |
| NEVER use | `python`, `pip`, `pip3` directly |

---

## Success Criteria

### FEAT-009 Definition of Done

- [ ] EN-801: TEMPLATE-FORMAT.md created with 8-section canonical structure
- [ ] EN-802: /adversary skill scaffold created (SKILL.md, PLAYBOOK.md, agents/)
- [ ] EN-803: S-014 LLM-as-Judge template created and passes format validation
- [ ] EN-804: S-010 Self-Refine template created and passes format validation
- [ ] EN-805: S-007 Constitutional AI template created and passes format validation
- [ ] EN-806: S-002 Devil's Advocate template created and passes format validation
- [ ] EN-807: S-003 Steelman template created and passes format validation
- [ ] EN-808: S-004 Pre-Mortem, S-012 FMEA, S-013 Inversion templates created
- [ ] EN-809: S-001 Red Team, S-011 CoVe templates created; all 10 templates complete
- [ ] EN-810: 3 skill agents created (adv-selector, adv-executor, adv-scorer)
- [ ] EN-811: 4 existing agents updated with template references; CLAUDE.md updated
- [ ] EN-812: E2E integration tests passing (format compliance, ID validation, invocation)
- [ ] All 12 enablers pass adversarial review (>= 0.92)
- [ ] All 7 phase gates passed
- [ ] Final synthesis document produced

### Quality Metrics Target

| Metric | Target |
|--------|--------|
| Average enabler quality score | >= 0.92 |
| Minimum enabler quality score | >= 0.88 |
| Template format compliance | 100% (10/10 templates) |
| Strategy ID SSOT match | 100% (10/10 strategies) |

---

## Risk Mitigations

| # | Risk | Likelihood | Impact | Mitigation |
|---|------|-----------|--------|------------|
| R1 | Template format too rigid for diverse strategies | Medium | Medium | EN-801 format includes optional sections; review with S-003 Steelman |
| R2 | Strategy templates too abstract to be actionable | Medium | High | Calibration examples required in each template; S-014 scoring on Actionability (0.15 weight) |
| R3 | Agent extensions break existing skill behavior | Low | High | EN-811 uses S-003 Steelman + S-010 Self-Refine; integration tests in EN-812 |
| R4 | Criticality-based selection logic incorrect | Medium | High | EN-810 validated against SSOT C1-C4 tables; EN-812 tests all 4 levels |
| R5 | Template proliferation creates maintenance burden | Low | Medium | Consistent format (EN-801) enables automated validation |
| R6 | Scoring rubric dimensions not calibrated | Medium | Medium | EN-803 includes calibration examples; cross-checked against EPIC-002 research |
| R7 | Context rot during 7-phase execution | High | Medium | Phase gates create natural checkpoints; session resumption protocol |
| R8 | /adversary skill naming conflicts with existing skills | Low | Low | Unique name verified against skills/ directory |

---

## Resumption Context

### For Session Recovery

If resuming this workflow in a new session:

1. **Read ORCHESTRATION.yaml** -- check `resumption.current_state` and `next_actions`
2. **Check git status** -- verify working tree state
3. **Read latest checkpoint** -- restore from last phase gate
4. **Identify current group** -- find first non-COMPLETE group in execution_queue
5. **Continue execution** -- pick up from identified group

### Files to Read on Resume

```
projects/PROJ-001-oss-release/work/EPIC-003-quality-implementation/orchestration/feat009-adversarial-20260215-001/ORCHESTRATION.yaml
projects/PROJ-001-oss-release/work/EPIC-003-quality-implementation/orchestration/feat009-adversarial-20260215-001/impl/{current_phase}/{current_agent}/
.context/rules/quality-enforcement.md
```

### Source Material for Implementors

| Source | Path | Purpose |
|--------|------|---------|
| Strategy Research | `projects/PROJ-001-oss-release/work/EPIC-002-quality-enforcement/FEAT-004-adversarial-strategy-research/research-15-adversarial-strategies.md` | Detailed strategy descriptions |
| Quality SSOT | `.context/rules/quality-enforcement.md` | Strategy IDs, criticality levels, threshold |
| FEAT-008 Reference | `projects/PROJ-001-oss-release/work/EPIC-003-quality-implementation/orchestration/` | Format and pattern reference |

---

*DISCLAIMER: This file was generated by the orch-planner agent (v2.2.0). All state transitions must be validated before execution.*
*Generated by orch-planner agent v2.2.0*
*Last Updated: 2026-02-15*
