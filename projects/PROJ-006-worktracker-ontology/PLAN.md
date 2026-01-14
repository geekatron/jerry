# PROJ-006: Work Tracker Ontology - Project Plan

> **Project ID:** PROJ-006-worktracker-ontology
> **Status:** IN PROGRESS
> **Created:** 2026-01-13
> **Strategic Contract:** [ORCHESTRATION_PLAN.md](./ORCHESTRATION_PLAN.md)

---

## Executive Summary

This project reverse-engineers a unified **Work Tracker Ontology** from three major project management domains: **ADO Scrum**, **SAFe**, and **JIRA**. The goal is to create a parent ontology with domain entities, relationships, state transitions, and markdown templates for a Claude Code Skill.

---

## Objectives

1. **Research**: Understand domain models across ADO Scrum, SAFe, and JIRA
2. **Analyze**: Extract entities, properties, behaviors, relationships, state machines
3. **Synthesize**: Identify common patterns and map to canonical terms
4. **Design**: Create parent ontology with system mappings
5. **Template**: Generate markdown templates for skill integration
6. **Validate**: Review and quality gate all artifacts

---

## Scope

### In Scope

- ADO Scrum process template domain model
- SAFe framework domain model (Portfolio, Program, Team levels)
- JIRA standard issue types and workflows
- Parent ontology design with mapping rules
- Markdown templates for Claude Code skill

### Out of Scope

- Implementation of Claude Code skill (future project)
- Custom field mappings (beyond standard fields)
- Advanced Roadmaps/Portfolio features

---

## Approach

### Multi-Agent Orchestration

This project uses a multi-agent orchestration approach with parallel research streams converging at sync barriers. See [ORCHESTRATION_PLAN.md](./ORCHESTRATION_PLAN.md) for detailed pipeline visualization.

### Phases

| Phase | Name | Agents | Status |
|-------|------|--------|--------|
| 1 | Parallel Research | ps-researcher x3 | COMPLETED |
| 2 | Parallel Analysis | ps-analyst x3 | COMPLETED |
| 3 | Cross-Domain Synthesis | ps-synthesizer | IN PROGRESS |
| 4 | Ontology Design | nse-architecture, ps-architect | BLOCKED |
| 5 | Template Generation | ps-synthesizer | BLOCKED |
| 6 | Review & Validation | nse-reviews | BLOCKED |

---

## Deliverables

| Deliverable | Description | Location |
|-------------|-------------|----------|
| Domain Models | 3 extracted domain models | `analysis/*.md` |
| Synthesis Report | Cross-domain comparison | `synthesis/CROSS-DOMAIN-SYNTHESIS.md` |
| Parent Ontology | Canonical ontology design | `synthesis/ONTOLOGY-v1.md` |
| ADR | Design decision record | `decisions/ADR-001-ontology-design.md` |
| Templates | Markdown skill templates | `templates/*.md` |

---

## Success Criteria

- [ ] Complete domain models for ADO Scrum, SAFe, and JIRA
- [ ] Identified common entities, relationships, and state machines
- [ ] Parent ontology design with mapping rules
- [ ] Markdown templates ready for skill integration
- [ ] All artifacts reviewed and approved

---

## Risk Register

| Risk | Impact | Likelihood | Mitigation |
|------|--------|------------|------------|
| Incomplete documentation | High | Medium | Use multiple sources |
| Domain ambiguity | Medium | High | Document assumptions |
| Scope creep | High | Medium | Strict phase gates |
| Template complexity | Medium | Low | Iterative refinement |

---

## References

- [ORCHESTRATION_PLAN.md](./ORCHESTRATION_PLAN.md) - Strategic contract and pipeline design
- [WORKTRACKER.md](./WORKTRACKER.md) - Work item tracking manifest
- [work/SE-001/SOLUTION-WORKTRACKER.md](./work/SE-001/SOLUTION-WORKTRACKER.md) - Solution epic details

---

## Change Log

| Date | Change | Author |
|------|--------|--------|
| 2026-01-13 | Initial plan created | Claude |
| 2026-01-13 | Phases 1-2 completed, Phase 3 approved | Claude |
