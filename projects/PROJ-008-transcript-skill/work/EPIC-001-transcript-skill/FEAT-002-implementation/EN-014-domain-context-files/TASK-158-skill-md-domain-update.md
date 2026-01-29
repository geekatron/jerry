# TASK-158: Update SKILL.md with 6 New Domains

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
id: "TASK-158"
work_type: TASK
title: "Update SKILL.md with 6 New Domains"
description: |
  Update the SKILL.md context_injection section to include all 8 available
  domains (2 existing + 6 from EN-006 promotion).

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
  - "implementation"
  - "skill-definition"
  - "en006-promotion"
  - "DISC-005"

effort: 0.5
acceptance_criteria: |
  - SKILL.md context_injection.available_domains updated with 8 domains
  - Domain descriptions added for all 6 new domains
  - domain_selection_guide reference added
  - PLAYBOOK.md updated if domain invocation documented there
  - Skill loads all 8 domains correctly at runtime

due_date: null

activity: DEVELOPMENT
original_estimate: 1
remaining_work: 1
time_spent: 0
```

---

## State Machine

**Current State:** `BACKLOG`

---

## Content

### Description

Update the SKILL.md file's context_injection section to register all 8 available domains. Currently only `general` and `transcript` are listed. After EN-006 promotion, 6 additional domains will be available.

### Current SKILL.md Context Injection Section

```yaml
context_injection:
  context_path: "./contexts/"
  default_domain: "general"
  available_domains:
    - name: "general"
      description: "..."
    - name: "transcript"
      description: "..."
```

### Target SKILL.md Context Injection Section

```yaml
context_injection:
  context_path: "./contexts/"
  default_domain: "general"
  domain_selection_guide: "./docs/domains/DOMAIN-SELECTION-GUIDE.md"
  available_domains:
    - name: "general"
      description: "Baseline domain for any transcript type"
      file: "general.yaml"
    - name: "transcript"
      description: "Core transcript entities (action, decision, question)"
      file: "transcript.yaml"
    - name: "meeting"
      description: "Meeting-specific extensions (attendee, agenda)"
      file: "meeting.yaml"
    - name: "software-engineering"
      description: "Software engineering standups, planning, retrospectives"
      file: "software-engineering.yaml"
      spec: "./docs/domains/SPEC-software-engineering.md"
    - name: "software-architecture"
      description: "Architecture discussions, ADRs, design reviews"
      file: "software-architecture.yaml"
      spec: "./docs/domains/SPEC-software-architecture.md"
    - name: "product-management"
      description: "Product planning, roadmaps, prioritization"
      file: "product-management.yaml"
      spec: "./docs/domains/SPEC-product-management.md"
    - name: "user-experience"
      description: "UX research, design critiques, usability"
      file: "user-experience.yaml"
      spec: "./docs/domains/SPEC-user-experience.md"
    - name: "cloud-engineering"
      description: "DevOps/SRE, incidents, deployments"
      file: "cloud-engineering.yaml"
      spec: "./docs/domains/SPEC-cloud-engineering.md"
    - name: "security-engineering"
      description: "Security discussions, threat modeling, compliance"
      file: "security-engineering.yaml"
      spec: "./docs/domains/SPEC-security-engineering.md"
```

### Acceptance Criteria

- [ ] `available_domains` expanded to 8 entries (was 2)
- [ ] Each new domain has:
  - [ ] `name` matching the domain identifier
  - [ ] `description` (brief, 1-line)
  - [ ] `file` pointing to contexts/*.yaml
  - [ ] `spec` pointing to docs/domains/SPEC-*.md
- [ ] `domain_selection_guide` reference added
- [ ] PLAYBOOK.md updated if domain invocation is documented
- [ ] YAML syntax valid
- [ ] Skill parses correctly after update

### Related Items

- Parent: [EN-014: Domain Context Files Implementation](./EN-014-domain-context-files.md)
- Discovery: [DISC-005: EN-006 Artifact Promotion Gap](../FEAT-002--DISC-005-en006-artifact-promotion-gap.md)
- Blocked By: TASK-150..155 (domain files must exist), TASK-157 (SPEC files must exist)
- Blocks: [TASK-159: Domain Load Validation](./TASK-159-domain-load-validation.md)
- Updates: [SKILL.md](../../../../../skills/transcript/SKILL.md)

---

## Evidence

### Deliverables

| Deliverable | Type | Link |
|-------------|------|------|
| Updated SKILL.md | Implementation | skills/transcript/SKILL.md |
| PLAYBOOK.md update | Implementation | skills/transcript/docs/PLAYBOOK.md (if needed) |

### Verification

- [ ] SKILL.md has 8 domains listed
- [ ] Each domain has name, description, file, spec
- [ ] YAML syntax valid
- [ ] domain_selection_guide reference present
- [ ] Reviewed by: (pending)

---

## History

| Date | Status | Notes |
|------|--------|-------|
| 2026-01-28 | Created | Initial task creation per DISC-005 EN-006 artifact promotion |
