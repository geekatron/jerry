# PROJ-013: Diataxis Documentation Framework Skill

> **Status:** In Progress
> **Created:** 2026-02-27
> **GitHub Issue:** [#99](https://github.com/geekatron/jerry/issues/99)
> **Branch:** `feat/proj-013-diataxis-framework`

## Document Sections

| Section | Purpose |
|---------|---------|
| [Overview](#overview) | What this project delivers |
| [Phases](#phases) | Implementation phases with deliverables |
| [Architecture](#architecture) | Skill and agent architecture |
| [Acceptance Criteria](#acceptance-criteria) | From GitHub Issue #99 |

---

## Overview

Implement the `/diataxis` skill -- a four-quadrant documentation framework with specialized agents for tutorials, how-to guides, reference, and explanation using the Diataxis methodology.

**Core deliverables:**
- 6 agents: 4 writers (tutorial, howto, reference, explanation) + classifier + auditor
- Per-quadrant templates and quality criteria
- Routing integration via `mandatory-skill-usage.md`
- Knowledge document and standards rule file
- Sample validation artifacts across all 4 quadrants

---

## Phases

### Phase 1: Foundation
- [x] Create project directory `projects/PROJ-013-diataxis/`
- [ ] Research Diataxis framework -- knowledge document at `docs/knowledge/diataxis-framework.md`
- [ ] Create `skills/diataxis/SKILL.md` with WHAT+WHEN+triggers
- [ ] Register skill in CLAUDE.md and AGENTS.md per H-26
- [ ] Create `skills/diataxis/rules/diataxis-standards.md` (5 required sections)

### Phase 2: Core Agents (Schema Validation Gate)
- [ ] `diataxis-tutorial.md` + `.governance.yaml` (systematic, T2, sonnet)
- [ ] `diataxis-howto.md` + `.governance.yaml` (convergent, T2, sonnet)
- [ ] `diataxis-reference.md` + `.governance.yaml` (systematic, T2, sonnet)
- [ ] `diataxis-explanation.md` + `.governance.yaml` (divergent, T2, opus)
- [ ] `diataxis-classifier.md` + `.governance.yaml` (convergent, T1, haiku)
- [ ] Templates: tutorial, howto, reference, explanation
- [ ] Phase 2 gate: all 5 `.governance.yaml` validate against schema

### Phase 3: Auditor and Integration
- [ ] `diataxis-auditor.md` + `.governance.yaml` (systematic, T2, sonnet)
- [ ] Update `mandatory-skill-usage.md` trigger map (priority 11)
- [ ] Integration testing: routing, classification, template application

### Phase 4: Quality and Validation
- [ ] Adversarial quality review (>= 0.95 threshold, up to 5 iterations)
- [ ] Sample documentation across all 4 quadrants
- [ ] Improve 2+ existing Jerry docs using the skill

---

## Architecture

```
skills/diataxis/
├── SKILL.md
├── agents/
│   ├── diataxis-tutorial.md + .governance.yaml     (systematic, T2, sonnet)
│   ├── diataxis-howto.md + .governance.yaml         (convergent, T2, sonnet)
│   ├── diataxis-reference.md + .governance.yaml     (systematic, T2, sonnet)
│   ├── diataxis-explanation.md + .governance.yaml   (divergent, T2, opus)
│   ├── diataxis-classifier.md + .governance.yaml    (convergent, T1, haiku)
│   └── diataxis-auditor.md + .governance.yaml       (systematic, T2, sonnet)
├── rules/
│   └── diataxis-standards.md
└── templates/
    ├── tutorial-template.md
    ├── howto-template.md
    ├── reference-template.md
    └── explanation-template.md
```

---

## Acceptance Criteria

See [GitHub Issue #99](https://github.com/geekatron/jerry/issues/99) for full acceptance criteria checklist.
