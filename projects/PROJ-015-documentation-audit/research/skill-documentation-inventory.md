# Skill Documentation Inventory — PROJ-015

> Comprehensive inventory of all 15 Jerry skills and their user-facing documentation coverage across all 4 Diataxis quadrants.
> **Generated:** 2026-03-02
> **Task:** TASK-015-003 (Inventory all 15 skills for user-facing documentation coverage)

## Document Sections

| Section | Purpose |
|---------|---------|
| [Coverage Summary](#coverage-summary) | Quick view of all 15 skills x 4 quadrants |
| [Coverage by Quadrant](#coverage-by-quadrant) | Aggregate coverage per Diataxis quadrant |
| [Supporting Documentation](#supporting-documentation) | Playbooks, knowledge base, runbooks, research |
| [Gap Analysis](#gap-analysis) | Missing documentation by priority |

---

## Coverage Summary

| # | Skill | SKILL.md Type | Tutorial | How-To | Reference | Explanation | Playbook | Knowledge | Runbook | Agents |
|---|-------|---------------|----------|--------|-----------|------------|----------|-----------|---------|--------|
| 1 | `/adversary` | Reference | -- | Yes | Yes | -- | -- | -- | -- | 3 |
| 2 | `/ast` | Reference | -- | Yes | Yes | -- | -- | -- | -- | 0 |
| 3 | `/bootstrap` | Ref+HowTo | -- | Yes | Yes | -- | -- | -- | -- | 0 |
| 4 | `/diataxis` | Ref+HowTo | -- | Yes | Yes | -- | -- | Yes | -- | 6 |
| 5 | `/eng-team` | Reference | -- | Yes | Yes | -- | -- | -- | -- | 10 |
| 6 | `/nasa-se` | Reference | -- | Yes | Yes | -- | -- | -- | -- | 10 |
| 7 | `/orchestration` | Ref+HowTo | -- | Yes | Yes | -- | Yes | -- | -- | 3 |
| 8 | `/problem-solving` | Reference | -- | Yes | Yes | -- | Yes | -- | -- | 9 |
| 9 | `/prompt-engineering` | Ref+HowTo | -- | Yes | Yes | -- | -- | -- | -- | 3 |
| 10 | `/red-team` | Reference | -- | Yes | Yes | -- | -- | -- | -- | 11 |
| 11 | `/saucer-boy` | Ref+Expl | -- | Yes | Yes | Yes | -- | Yes | -- | 1 |
| 12 | `/saucer-boy-framework-voice` | Ref+Expl | -- | Yes | Yes | Yes | -- | -- | -- | 3 |
| 13 | `/transcript` | Ref+HowTo | -- | Yes | Yes | -- | Yes | -- | Yes | 5 |
| 14 | `/worktracker` | Reference | -- | Yes | Yes | -- | -- | -- | -- | 3 |
| 15 | `/architecture` | Reference | -- | Yes | Yes | -- | -- | -- | -- | 0 |

---

## Coverage by Quadrant

| Quadrant | Skills Covered | Coverage % | Strongest | Weakest |
|----------|---------------|------------|-----------|---------|
| **Tutorial** | 0 / 15 | **0%** | None | All 15 skills lack tutorials |
| **How-To** | 14 / 15 | 93% | All except `/saucer-boy` | `/architecture` needs more |
| **Reference** | 15 / 15 | 100% | `/problem-solving`, `/nasa-se`, `/eng-team`, `/red-team` | None critical |
| **Explanation** | 2 / 15 | **13%** | `/saucer-boy`, `/saucer-boy-framework-voice` | 13 skills lack explanations |

---

## Supporting Documentation

### Playbooks (4 of 15 skills)

| Playbook | Skill | Location |
|----------|-------|----------|
| problem-solving.md | `/problem-solving` | `docs/playbooks/problem-solving.md` |
| orchestration.md | `/orchestration` | `docs/playbooks/orchestration.md` |
| transcript.md | `/transcript` | `docs/playbooks/transcript.md` |
| PLUGIN-DEVELOPMENT.md | General (skill creation) | `docs/playbooks/PLUGIN-DEVELOPMENT.md` |

### Knowledge Base (3 skill-specific)

| Knowledge Doc | Skill | Location |
|---------------|-------|----------|
| diataxis-framework.md | `/diataxis` | `docs/knowledge/diataxis-framework.md` |
| saucer-boy-persona.md | `/saucer-boy` | `docs/knowledge/saucer-boy-persona.md` |
| agent-pattern-taxonomy.md | General | `docs/knowledge/agent-pattern-taxonomy.md` |

### Runbooks (1 of 15 skills)

| Runbook | Skill | Location |
|---------|-------|----------|
| getting-started.md | General (not skill-specific) | `docs/runbooks/getting-started.md` |

### Research (12 research pages, cross-skill)

Research pages in `docs/research/` provide deep-dive coverage but are not linked from individual skill documentation. Topics: negative-prompting, adversarial strategies, architecture patterns, context management, governance, single-vs-multi-agent, and more.

---

## Gap Analysis

### Critical Gaps (Block Adoption)

| Priority | Gap | Impact | Affected Skills |
|----------|-----|--------|-----------------|
| **P1** | Zero tutorials | New users must navigate reference docs with no guided learning path | All 15 skills |
| **P2** | 87% explanation gap | Users understand *what* but not *why* — reduces conceptual understanding and correct usage | 13 of 15 skills |
| **P3** | Zero worked examples | No end-to-end demonstrations showing realistic agent workflows | All 15 skills |

### High Priority Gaps (Improve UX)

| Priority | Gap | Impact | Affected Skills |
|----------|-----|--------|-----------------|
| **P4** | 73% playbook gap | 11 skills lack dedicated playbooks for operational guidance | 11 of 15 skills |
| **P5** | 93% runbook gap | Only 1 general runbook exists; no skill-specific operational procedures | 14 of 15 skills |

### Recommended Tutorial Priority (Top 5)

Based on skill complexity, user-facing importance, and agent count:

| Rank | Skill | Rationale |
|------|-------|-----------|
| 1 | `/problem-solving` | Most-used skill, 9 agents, entry point for new users |
| 2 | `/orchestration` | Complex multi-agent coordination, high learning curve |
| 3 | `/worktracker` | Required for all project work (H-04), foundational |
| 4 | `/eng-team` | 10 agents, complex security methodology |
| 5 | `/prompt-engineering` | Newest skill, operationalizes PROJ-014 findings |
