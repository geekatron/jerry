# TASK-157: Promote SPEC-*.md Files to Skill Documentation

<!--
TEMPLATE: Task
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.6
ENABLER: EN-014 (Domain Context Files Implementation)
DISCOVERY: DISC-005 (EN-006 Artifact Promotion Gap Analysis)
-->

---

## Frontmatter

```yaml
id: "TASK-157"
work_type: TASK
title: "Promote SPEC-*.md Files to Skill Documentation"
description: |
  Copy SPEC-*.md domain documentation files and the DOMAIN-SELECTION-GUIDE
  from EN-006 to the skill's docs/domains/ directory.

classification: ENABLER
status: BACKLOG
resolution: null
priority: MEDIUM
assignee: "Claude"
created_by: "Claude"
created_at: "2026-01-28T21:30:00Z"
updated_at: "2026-01-28T21:30:00Z"

parent_id: "EN-014"

tags:
  - "documentation"
  - "domain-context"
  - "en006-promotion"
  - "DISC-005"

effort: 1
acceptance_criteria: |
  - docs/domains/ folder created in skill
  - All 6 SPEC-*.md files promoted
  - DOMAIN-SELECTION-GUIDE.md created from README flowchart
  - Internal links updated if needed
  - Documentation accessible for skill users and agents

due_date: null

activity: DOCUMENTATION
original_estimate: 2
remaining_work: 2
time_spent: 0
```

---

## State Machine

**Current State:** `BACKLOG`

---

## Content

### Description

Promote the SPEC-*.md domain specification files from EN-006 to the skill's documentation directory. These files provide L0/L1/L2 documentation about each domain that users and agents can reference. Also create a DOMAIN-SELECTION-GUIDE.md from the EN-006 README flowchart.

### Source Artifacts

```
EN-006/docs/specs/domain-contexts/
├── README.md                             → DOMAIN-SELECTION-GUIDE.md
├── 01-software-engineering/
│   └── SPEC-software-engineering.md      → docs/domains/
├── 02-software-architecture/
│   └── SPEC-software-architecture.md     → docs/domains/
├── 03-product-management/
│   └── SPEC-product-management.md        → docs/domains/
├── 04-user-experience/
│   └── SPEC-user-experience.md           → docs/domains/
├── 05-cloud-engineering/
│   └── SPEC-cloud-engineering.md         → docs/domains/
└── 06-security-engineering/
    └── SPEC-security-engineering.md      → docs/domains/
```

### Target Structure

```
skills/transcript/docs/domains/
├── DOMAIN-SELECTION-GUIDE.md       ← Flowchart from README
├── SPEC-software-engineering.md
├── SPEC-software-architecture.md
├── SPEC-product-management.md
├── SPEC-user-experience.md
├── SPEC-cloud-engineering.md
└── SPEC-security-engineering.md
```

### SPEC File Content (L0/L1/L2)

Each SPEC file contains:
- **L0 (ELI5):** Overview for non-technical stakeholders
- **L1 (Engineer):** Entity model, extraction patterns, technical details
- **L2 (Architect):** Design rationale, trade-offs, integration considerations

### DOMAIN-SELECTION-GUIDE.md Content

Extract from EN-006 README:
- Domain selection flowchart (Mermaid diagram)
- When to use each domain
- Domain comparison table
- Default domain (general) behavior

### Acceptance Criteria

- [ ] `skills/transcript/docs/domains/` folder created
- [ ] 6 SPEC files copied:
  - [ ] SPEC-software-engineering.md
  - [ ] SPEC-software-architecture.md
  - [ ] SPEC-product-management.md
  - [ ] SPEC-user-experience.md
  - [ ] SPEC-cloud-engineering.md
  - [ ] SPEC-security-engineering.md
- [ ] DOMAIN-SELECTION-GUIDE.md created with:
  - [ ] Flowchart for domain selection
  - [ ] When-to-use guidance
  - [ ] Domain comparison table
- [ ] Internal links updated (if any point to EN-006 paths)
- [ ] Markdown syntax valid
- [ ] Referenced from SKILL.md or PLAYBOOK.md

### Related Items

- Parent: [EN-014: Domain Context Files Implementation](./EN-014-domain-context-files.md)
- Discovery: [DISC-005: EN-006 Artifact Promotion Gap](../FEAT-002--DISC-005-en006-artifact-promotion-gap.md)
- Blocked By: TASK-150, TASK-151, TASK-152, TASK-153, TASK-154, TASK-155 (domains must exist)
- Blocks: [TASK-158: SKILL.md Update](./TASK-158-skill-md-domain-update.md)
- Source: [EN-006 domain-contexts/](../../FEAT-001-analysis-design/EN-006-context-injection-design/docs/specs/domain-contexts/)

---

## Evidence

### Deliverables

| Deliverable | Type | Link |
|-------------|------|------|
| docs/domains/ folder | Structure | skills/transcript/docs/domains/ |
| DOMAIN-SELECTION-GUIDE.md | Documentation | skills/transcript/docs/domains/DOMAIN-SELECTION-GUIDE.md |
| 6 SPEC files | Documentation | skills/transcript/docs/domains/SPEC-*.md |

### Verification

- [ ] Folder created at correct location
- [ ] All 6 SPEC files present
- [ ] DOMAIN-SELECTION-GUIDE.md has flowchart
- [ ] All markdown valid
- [ ] Links work correctly
- [ ] Reviewed by: (pending)

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-01-28 | Created | Initial task creation per DISC-005 EN-006 artifact promotion |
