---
id: wi-sao-020
title: "Add Agent-Specific Output Conventions to Template"
status: COMPLETE
parent: "_index.md"
initiative: sao-init-001
children: []
depends_on: []
blocks: []
created: "2026-01-10"
started: "2026-01-10"
completed: "2026-01-10"
priority: "P1"
estimated_effort: "2h"
entry_id: "sao-020"
source: "User feedback on lost research material (context compaction)"
token_estimate: 900
---

# WI-SAO-020: Add Agent-Specific Output Conventions to Template

> **Status:** ✅ COMPLETE
> **Started:** 2026-01-10
> **Completed:** 2026-01-10
> **Priority:** HIGH (P1)

---

## Trigger Statement

"output_directory is relevant to the type of agent - they do not all output to research/"

---

## Description

Update PS_AGENT_TEMPLATE.md to document agent-specific output directory and artifact naming conventions. Audited ps-* agents show each has distinct output paths.

---

## Acceptance Criteria

1. [x] Reference table of agent output directories added to template
2. [x] Artifact naming conventions documented per agent type
3. [x] Persistence requirements section enhanced
4. [x] All 8 ps-* agent conventions captured accurately

---

## Agent Output Conventions (Audit Results)

| Agent | Output Directory | Artifact Naming |
|-------|------------------|-----------------|
| ps-researcher | `projects/${JERRY_PROJECT}/research/` | `{ps-id}-{entry-id}-{topic-slug}.md` |
| ps-analyst | `projects/${JERRY_PROJECT}/analysis/` | `{ps-id}-{entry-id}-{analysis-type}.md` |
| ps-architect | `projects/${JERRY_PROJECT}/decisions/` | `{ps-id}-{entry-id}-adr-{decision-slug}.md` |
| ps-investigator | `projects/${JERRY_PROJECT}/investigations/` | `{ps-id}-{entry-id}-investigation.md` |
| ps-reporter | `projects/${JERRY_PROJECT}/reports/` | `{ps-id}-{entry-id}-{report-type}.md` |
| ps-reviewer | `projects/${JERRY_PROJECT}/reviews/` | `{ps-id}-{entry-id}-{review-type}.md` |
| ps-synthesizer | `projects/${JERRY_PROJECT}/synthesis/` | `{ps-id}-{entry-id}-synthesis.md` |
| ps-validator | `projects/${JERRY_PROJECT}/analysis/` | `{ps-id}-{entry-id}-validation.md` |

---

## Tasks

- [x] **T-020.1:** Audit all 8 ps-* agents for output conventions
- [x] **T-020.2:** Add output convention reference table to PS_AGENT_TEMPLATE.md
- [x] **T-020.3:** Enhance persistence requirements section
- [x] **T-020.4:** Update generic placeholder with convention guidance

---

*Source: Extracted from WORKTRACKER.md lines 929-959*
