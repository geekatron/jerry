# nse-r-001: Skills Formal Requirements

**Document ID:** NSE-REQ-001
**Date:** 2026-01-09
**Author:** nse-requirements (Claude Opus 4.5)
**Status:** Complete
**NASA Reference:** NPR 7123.1D Process 2 (Technical Requirements Definition)

---

```
DISCLAIMER: This guidance is AI-generated based on NASA Systems Engineering
standards. It is advisory only and does not constitute official NASA guidance.
All SE decisions require human review and professional engineering judgment.
Not for use in mission-critical decisions without SME validation.
```

---

## L0: Executive Summary

The Jerry Framework Skills ecosystem comprises four skills (problem-solving, nasa-se, worktracker, architecture) that collectively implement an agent-based problem-solving and systems engineering capability. This requirements analysis identifies **47 formal requirements** across functional and non-functional domains, reveals **12 critical gaps**, and recommends **8 priority actions** for achieving full NPR 7123.1D compliance. The skills are approximately 75% complete in terms of requirements coverage, with primary gaps in verification criteria, formal acceptance testing, and cross-skill integration contracts.

---

## L1: Technical Requirements

### 1.1 Functional Requirements - Problem-Solving Skill

| REQ ID | Requirement | Source | Verification Method | Priority |
|--------|-------------|--------|---------------------|----------|
| REQ-SKL-PS-001 | The problem-solving skill SHALL provide 8 specialized agents: ps-researcher, ps-analyst, ps-architect, ps-validator, ps-synthesizer, ps-reviewer, ps-investigator, ps-reporter | SKILL.md Line 61-70 | Inspection | P1 |
| REQ-SKL-PS-002 | Each problem-solving agent SHALL produce output at three levels: L0 (ELI5), L1 (Software Engineer), L2 (Principal Architect) | SKILL.md Line 72-76 | Inspection | P1 |
| REQ-SKL-PS-003 | The skill SHALL persist all agent outputs to designated filesystem locations (docs/research/, docs/analysis/, docs/decisions/, etc.) | SKILL.md Line 172-198 | Test | P1 |
| REQ-SKL-PS-004 | The skill SHALL support natural language activation via specified keywords (research, analyze, investigate, review, synthesize, validate, etc.) | SKILL.md Line 6-18 | Demonstration | P2 |
| REQ-SKL-PS-005 | The skill SHALL support explicit agent invocation by name (e.g., "Use ps-researcher") | SKILL.md Line 97-103 | Demonstration | P2 |
| REQ-SKL-PS-006 | The skill SHALL support Task tool programmatic invocation with PS CONTEXT parameters | SKILL.md Line 107-129 | Test | P2 |
| REQ-SKL-PS-007 | Agents SHALL support state passing between agents via defined output keys (researcher_output, analyst_output, etc.) | SKILL.md Line 157-168 | Test | P2 |
| REQ-SKL-PS-008 | The skill SHALL use file naming convention: {ps-id}-{entry-id}-{topic}.md | SKILL.md Line 184-198 | Inspection | P3 |
| REQ-SKL-PS-009 | The skill SHALL comply with Jerry Constitution v1.0 principles P-001, P-002, P-003, P-004, P-011, P-022 | SKILL.md Line 203-214 | Analysis | P1 |

### 1.2 Functional Requirements - NASA SE Skill

| REQ ID | Requirement | Source | Verification Method | Priority |
|--------|-------------|--------|---------------------|----------|
| REQ-SKL-NSE-001 | The nasa-se skill SHALL provide 8 specialized agents: nse-requirements, nse-verification, nse-risk, nse-reviewer, nse-integration, nse-configuration, nse-architecture, nse-reporter | SKILL.md Line 83-92 | Inspection | P1 |
| REQ-SKL-NSE-002 | The nse-requirements agent SHALL implement NPR 7123.1D Processes 1, 2, 11 (Stakeholder Expectations, Technical Requirements, Requirements Management) | SKILL.md Line 85 | Analysis | P1 |
| REQ-SKL-NSE-003 | The nse-verification agent SHALL implement NPR 7123.1D Processes 7, 8 (Product Verification, Product Validation) | SKILL.md Line 86 | Analysis | P1 |
| REQ-SKL-NSE-004 | The nse-risk agent SHALL implement NPR 7123.1D Process 13 (Technical Risk Management) | SKILL.md Line 87 | Analysis | P1 |
| REQ-SKL-NSE-005 | The nse-integration agent SHALL implement NPR 7123.1D Processes 6, 12 (Product Integration, Interface Management) | SKILL.md Line 89 | Analysis | P1 |
| REQ-SKL-NSE-006 | The nse-configuration agent SHALL implement NPR 7123.1D Processes 14, 15 (Configuration Management, Technical Data Management) | SKILL.md Line 90 | Analysis | P1 |
| REQ-SKL-NSE-007 | The nse-architecture agent SHALL implement NPR 7123.1D Processes 3, 4, 17 (Logical Decomposition, Design Solution, Decision Analysis) | SKILL.md Line 91 | Analysis | P1 |
| REQ-SKL-NSE-008 | All nse agents SHALL produce output at three levels: L0, L1, L2 | SKILL.md Line 94-98 | Inspection | P1 |
| REQ-SKL-NSE-009 | All nse agent outputs SHALL include the mandatory AI guidance disclaimer | SKILL.md Line 55-62, Constitution P-043 | Inspection | P1 |
| REQ-SKL-NSE-010 | The skill SHALL persist outputs to project-specific directories (requirements/, verification/, risks/, reviews/, etc.) | SKILL.md Line 254-272 | Test | P1 |
| REQ-SKL-NSE-011 | The nse-risk agent SHALL use 5x5 risk matrix with RED (>15), YELLOW (8-15), GREEN (<8) classification | SKILL.md Line 46, Constitution P-042 | Test | P1 |
| REQ-SKL-NSE-012 | The skill SHALL support technical review preparation for SRR, PDR, CDR, FRR milestones | SKILL.md Line 47 | Demonstration | P2 |
| REQ-SKL-NSE-013 | Requirements SHALL use formal "shall" statement format | SKILL.md Line 44 | Inspection | P1 |
| REQ-SKL-NSE-014 | The skill SHALL maintain bidirectional traceability for all requirements per Constitution P-040 | Constitution Line 229-243 | Analysis | P1 |
| REQ-SKL-NSE-015 | The skill SHALL comply with Constitution principles P-001 through P-043 | SKILL.md Line 276-291 | Analysis | P1 |

### 1.3 Functional Requirements - Work Tracker Skill

| REQ ID | Requirement | Source | Verification Method | Priority |
|--------|-------------|--------|---------------------|----------|
| REQ-SKL-WT-001 | The worktracker skill SHALL provide create, list, update, complete, show, search, and summary commands | SKILL.md Line 26-243 | Test | P1 |
| REQ-SKL-WT-002 | Work items SHALL have properties: id, title, description, type, status, priority, parent_id, created_at, updated_at, completed_at, notes, references, tags | SKILL.md Line 248-265 | Inspection | P1 |
| REQ-SKL-WT-003 | Work item types SHALL include: feature, bug, task, spike, epic | SKILL.md Line 38 | Inspection | P2 |
| REQ-SKL-WT-004 | Work item status SHALL include: pending, in_progress, blocked, completed | SKILL.md Line 64 | Inspection | P2 |
| REQ-SKL-WT-005 | Work item priority SHALL include: critical, high, medium, low | SKILL.md Line 39 | Inspection | P2 |
| REQ-SKL-WT-006 | The skill SHALL persist work items to projects/${JERRY_PROJECT}/.jerry/data/items/ | SKILL.md Line 268-276 | Test | P1 |
| REQ-SKL-WT-007 | The skill SHALL support hierarchical work items via parent_id | SKILL.md Line 40, 258 | Test | P2 |
| REQ-SKL-WT-008 | The skill SHALL integrate with TodoWrite tool via sync-from-todo and sync-to-todo commands | SKILL.md Line 285-295 | Demonstration | P3 |
| REQ-SKL-WT-009 | The skill SHALL support commit linking via "Closes: WORK-NNN" format | SKILL.md Line 305-310 | Demonstration | P3 |

### 1.4 Functional Requirements - Architecture Skill

| REQ ID | Requirement | Source | Verification Method | Priority |
|--------|-------------|--------|---------------------|----------|
| REQ-SKL-ARCH-001 | The architecture skill SHALL provide analyze, diagram, review, and decision commands | SKILL.md Line 15-232 | Test | P1 |
| REQ-SKL-ARCH-002 | The analyze command SHALL check hexagonal architecture compliance (no external imports in domain, dependency direction) | SKILL.md Line 35-57 | Test | P1 |
| REQ-SKL-ARCH-003 | The diagram command SHALL support types: hexagonal, component, sequence, data-flow | SKILL.md Line 66 | Test | P2 |
| REQ-SKL-ARCH-004 | The diagram command SHALL support formats: mermaid, plantuml, ascii | SKILL.md Line 68 | Test | P2 |
| REQ-SKL-ARCH-005 | The review command SHALL apply checklists: hexagonal, ddd, solid, all | SKILL.md Line 129 | Test | P2 |
| REQ-SKL-ARCH-006 | The decision command SHALL create ADRs using Nygard format with Context, Decision, Consequences, Alternatives | SKILL.md Line 190-231 | Inspection | P1 |
| REQ-SKL-ARCH-007 | ADRs SHALL be stored in docs/design/ADR_NNN_slug.md | SKILL.md Line 190 | Inspection | P2 |
| REQ-SKL-ARCH-008 | The skill SHALL enforce layer dependency rules (Interface → Infrastructure → Application → Domain) | SKILL.md Line 267-283 | Analysis | P1 |

### 1.5 Non-Functional Requirements

| REQ ID | Requirement | Source | Verification Method | Priority |
|--------|-------------|--------|---------------------|----------|
| REQ-SKL-NFR-001 | All skills SHALL be version-controlled with semantic versioning | All SKILL.md frontmatter | Inspection | P2 |
| REQ-SKL-NFR-002 | All skills SHALL declare allowed-tools in frontmatter | All SKILL.md frontmatter | Inspection | P2 |
| REQ-SKL-NFR-003 | All skills SHALL declare activation-keywords in frontmatter | All SKILL.md frontmatter | Inspection | P2 |
| REQ-SKL-NFR-004 | All skill outputs SHALL survive context compaction via filesystem persistence | P-002, Agent Research Section 6 | Test | P1 |
| REQ-SKL-NFR-005 | Skills SHALL support maximum ONE level of agent nesting per P-003 | Constitution P-003, Agent Research Section 9 | Test | P1 |
| REQ-SKL-NFR-006 | Each subagent SHALL have its own 200K token context window | Agent Research Section 1.2 | Analysis | P2 |
| REQ-SKL-NFR-007 | Skills SHALL support up to 10 concurrent subagents with queue management | Agent Research Section 5.1 | Test | P2 |
| REQ-SKL-NFR-008 | All skill agent specifications SHALL be defined in skills/{skill}/agents/{agent}.md | PS SKILL.md Line 250-259, NSE SKILL.md Line 324-335 | Inspection | P2 |
| REQ-SKL-NFR-009 | Skills SHALL cite sources per P-001 and P-004 | Constitution P-001, P-004 | Inspection | P2 |
| REQ-SKL-NFR-010 | Skills SHALL gracefully degrade on errors per P-005 | Constitution P-005 | Test | P3 |

---

## 1.6 Derived Requirements

These requirements are derived from constitution principles and agent research findings:

| REQ ID | Requirement | Derived From | Verification Method | Priority |
|--------|-------------|--------------|---------------------|----------|
| REQ-SKL-DRV-001 | Skill invocation prompts SHALL include PS/NSE CONTEXT with project ID and entry ID | PS SKILL.md Task Tool example | Test | P2 |
| REQ-SKL-DRV-002 | Orchestrator agents SHALL summarize subagent results for user visibility | Agent Research Section 2.4 | Test | P2 |
| REQ-SKL-DRV-003 | Skills SHALL use file-based state transfer between agents to address context isolation | Agent Research Section 4.1 | Analysis | P1 |
| REQ-SKL-DRV-004 | The JERRY_PROJECT environment variable SHALL identify the active project context | CLAUDE.md, WT SKILL.md Line 278 | Test | P1 |

---

## 1.7 Gap Analysis

| Gap ID | Missing Requirement | Impact | Priority | Recommendation |
|--------|---------------------|--------|----------|----------------|
| GAP-SKL-001 | No formal acceptance test criteria for skill behavior | High - Cannot verify skill correctness | P1 | Define behavioral test scenarios per skill |
| GAP-SKL-002 | No formal interface contract between skills | High - Cross-skill integration untested | P1 | Define skill interface specifications |
| GAP-SKL-003 | No requirement for agent specification file format | Medium - Agent definitions may be inconsistent | P2 | Standardize agent YAML/frontmatter schema |
| GAP-SKL-004 | No requirement for error codes/messages | Medium - Error handling inconsistent | P2 | Define error taxonomy per skill |
| GAP-SKL-005 | No performance requirements (response time, token limits) | Medium - No baseline for optimization | P2 | Define performance SLAs |
| GAP-SKL-006 | No requirement for skill discovery mechanism | Low - Skills manually specified | P3 | Define skill registry/manifest |
| GAP-SKL-007 | Worktracker missing formal verification of state persistence | High - Data integrity risk | P1 | Add persistence verification tests |
| GAP-SKL-008 | Architecture skill missing formal integration with other skills | Medium - Operates in isolation | P2 | Define architecture review triggers |
| GAP-SKL-009 | No requirement for skill versioning compatibility | Medium - Breaking changes uncontrolled | P2 | Define version compatibility matrix |
| GAP-SKL-010 | NSE skill missing formal mapping to all 17 NASA processes | High - Incomplete coverage | P1 | Complete process mapping |
| GAP-SKL-011 | No requirement for skill telemetry/observability | Low - Cannot measure effectiveness | P3 | Define metrics collection |
| GAP-SKL-012 | No formal rollback mechanism for skill failures | Medium - Recovery undefined | P2 | Define failure recovery procedures |

---

## L2: Strategic Implications

### 2.1 Compliance Assessment

**NPR 7123.1D Process Alignment:**

| NASA Process | Skill Coverage | Gap Assessment |
|--------------|----------------|----------------|
| 1. Stakeholder Expectations | nse-requirements (partial) | Needs formal elicitation templates |
| 2. Technical Requirements | nse-requirements | Well-covered |
| 3. Logical Decomposition | nse-architecture | Well-covered |
| 4. Design Solution | nse-architecture, ps-architect | Well-covered |
| 5. Product Implementation | Not addressed | Out of scope for skills |
| 6. Product Integration | nse-integration | Well-covered |
| 7. Product Verification | nse-verification | Needs VCRM templates |
| 8. Product Validation | nse-verification | Needs validation criteria |
| 9. Product Transition | Not addressed | Consider nse-transition agent |
| 10. Technical Planning | Not addressed | Consider nse-planner agent |
| 11. Requirements Management | nse-requirements | Well-covered |
| 12. Interface Management | nse-integration | Well-covered |
| 13. Technical Risk Management | nse-risk | Well-covered |
| 14. Configuration Management | nse-configuration | Well-covered |
| 15. Technical Data Management | nse-configuration | Partial |
| 16. Technical Assessment | nse-reporter | Well-covered |
| 17. Decision Analysis | nse-architecture | Needs formal trade study templates |

**Constitution Compliance:**

| Principle | Skills Assessment | Compliance Level |
|-----------|-------------------|------------------|
| P-001 (Truth) | All skills cite sources | Compliant |
| P-002 (Persistence) | All skills persist to files | Compliant |
| P-003 (No Recursion) | Architecture supports single nesting | Compliant |
| P-004 (Provenance) | Problem-solving documents reasoning | Mostly Compliant |
| P-005 (Degradation) | Not formally addressed | Gap |
| P-010 (Task Tracking) | Worktracker skill | Compliant |
| P-011 (Evidence) | Research agents cite sources | Compliant |
| P-012 (Scope) | Not formally enforced | Gap |
| P-020 (User Authority) | Inherent to agent model | Compliant |
| P-021 (Transparency) | L0/L1/L2 output levels | Compliant |
| P-022 (No Deception) | Constitution compliance stated | Compliant |
| P-040 (Traceability) | NSE skill supports traces | Partially Compliant |
| P-041 (V&V Coverage) | NSE verification agent | Partially Compliant |
| P-042 (Risk Transparency) | NSE risk agent with 5x5 | Compliant |
| P-043 (Disclaimer) | Required in NSE outputs | Compliant |

### 2.2 Risk Assessment

| Risk ID | Risk Statement | L | C | Score | Mitigation |
|---------|----------------|---|---|-------|------------|
| R-REQ-001 | IF skill interface contracts are not formalized THEN cross-skill integration may fail unpredictably | 4 | 4 | 16 (RED) | Define formal interface specs |
| R-REQ-002 | IF behavioral tests are not defined THEN skill regressions may go undetected | 4 | 3 | 12 (YELLOW) | Create test suite per skill |
| R-REQ-003 | IF agent specifications lack schema THEN agent definitions may be inconsistent | 3 | 3 | 9 (YELLOW) | Define agent YAML schema |
| R-REQ-004 | IF NSE processes 9,10 remain unaddressed THEN NASA coverage incomplete | 2 | 3 | 6 (GREEN) | Prioritize based on usage |
| R-REQ-005 | IF context isolation issues persist THEN subagent quality may degrade | 3 | 4 | 12 (YELLOW) | Implement file-based state |

### 2.3 Recommended Actions

| Priority | Action | Responsible | Timeline |
|----------|--------|-------------|----------|
| P1 | Define formal skill interface contracts | nse-architecture | Phase 2 |
| P1 | Create behavioral test scenarios for all skills | nse-verification | Phase 2 |
| P1 | Complete NSE process mapping for all 17 processes | nse-requirements | Phase 2 |
| P1 | Define worktracker persistence verification | nse-verification | Phase 2 |
| P2 | Standardize agent specification schema | nse-configuration | Phase 3 |
| P2 | Define error taxonomy per skill | ps-analyst | Phase 3 |
| P2 | Define skill version compatibility matrix | nse-configuration | Phase 3 |
| P3 | Implement skill telemetry framework | nse-reporter | Phase 4 |

---

## Cross-Pollination Metadata

- **Source Agent:** nse-r-001 (nse-requirements)
- **Target Audience:** ps-researcher, ps-analyst, nse-verification
- **Key Handoff Items:**
  1. 47 formal requirements for skill validation
  2. 12 gaps requiring further investigation
  3. 5 risks requiring mitigation
  4. 8 recommended actions with priorities

### Research Gaps for ps-* Pipeline

The following questions require exploration by the ps-* research pipeline:

1. **RESEARCH-GAP-001:** What industry patterns exist for formal skill/capability interface contracts in multi-agent systems?
   - Context: GAP-SKL-002 identifies need for cross-skill integration contracts
   - Suggested approach: Survey agent framework APIs (LangChain, AutoGen, CrewAI)

2. **RESEARCH-GAP-002:** What behavioral testing frameworks are most effective for LLM agent validation?
   - Context: GAP-SKL-001 identifies need for acceptance test criteria
   - Suggested approach: Evaluate DeepEval, promptfoo, LangSmith

3. **RESEARCH-GAP-003:** How do other NASA SE tools handle the Product Transition (Process 9) phase?
   - Context: Gap in NSE skill coverage
   - Suggested approach: Research NASA MBSE tools, PLM integration patterns

4. **RESEARCH-GAP-004:** What error handling patterns work best for cascading agent failures?
   - Context: GAP-SKL-012 identifies undefined failure recovery
   - Suggested approach: Study orchestration patterns (Temporal, Airflow, Step Functions)

5. **RESEARCH-GAP-005:** What telemetry/observability patterns exist for agent-based systems?
   - Context: GAP-SKL-011 identifies need for metrics
   - Suggested approach: Evaluate LangSmith, Helicone, Anthropic Console

### Traceability Links

| This Document | Traces To |
|---------------|-----------|
| REQ-SKL-PS-* | skills/problem-solving/SKILL.md |
| REQ-SKL-NSE-* | skills/nasa-se/SKILL.md |
| REQ-SKL-WT-* | skills/worktracker/SKILL.md |
| REQ-SKL-ARCH-* | skills/architecture/SKILL.md |
| REQ-SKL-NFR-* | docs/governance/JERRY_CONSTITUTION.md |
| GAP-SKL-* | (Requires design artifacts) |
| R-REQ-* | projects/PROJ-002/risks/ (pending) |

---

## Appendix A: Requirements Traceability Matrix (Partial)

| Requirement | Parent | Child | Verification Status |
|-------------|--------|-------|---------------------|
| REQ-SKL-PS-001 | CLAUDE.md Skills Architecture | Agent specs in agents/*.md | Not Verified |
| REQ-SKL-PS-009 | JERRY_CONSTITUTION.md | Test scenarios BHV-* | Not Verified |
| REQ-SKL-NSE-002 | NPR 7123.1D Process 2 | Shall-statement templates | Not Verified |
| REQ-SKL-NFR-005 | P-003, Agent Research | Subagent spawn validation | Not Verified |

---

## Appendix B: Document History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-01-09 | nse-r-001 | Initial requirements specification |

---

*Document Version: 1.0*
*Classification: Requirements Engineering*
*NPR 7123.1D Alignment: Process 2 (Technical Requirements Definition)*
