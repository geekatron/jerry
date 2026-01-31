# EN-028: SKILL.md Compliance

<!--
TEMPLATE: Enabler
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.9
CREATED: 2026-01-30 per FEAT-005 Phase 2 (HIGH)
PURPOSE: Bring SKILL.md to PAT-SKILL-001 compliance
-->

> **Type:** enabler
> **Status:** pending
> **Priority:** high
> **Impact:** high
> **Enabler Type:** compliance
> **Created:** 2026-01-30T16:00:00Z
> **Due:** TBD
> **Completed:** -
> **Parent:** FEAT-005
> **Owner:** Claude
> **Effort:** 9h

---

## Summary

Add missing sections to transcript SKILL.md to comply with PAT-SKILL-001 (Universal SKILL.md Structure). This is Phase 2 (HIGH) of the skill compliance remediation.

**Technical Scope:**
- Add "Invoking an Agent" section with 3 methods
- Enhance "State Passing Between Agents" with session_context schema
- Add "Mandatory Persistence (P-002)" section
- Add self-critique checklist to Constitutional Compliance
- Restructure persona sections in agents (move from nested to top-level)

**Gaps Addressed:**
- GAP-S-001: Missing "Invoking an Agent" section (HIGH)
- GAP-S-003: State schema incomplete (HIGH)
- GAP-S-004: Missing "Mandatory Persistence (P-002)" section (HIGH)
- GAP-S-005: Constitutional Compliance incomplete (HIGH)
- GAP-A-002: persona nested incorrectly (HIGH)
- GAP-A-005: output section missing (HIGH)

---

## Problem Statement

Transcript SKILL.md is 60% compliant with PAT-SKILL-001 but missing key sections that prevent:

1. **User Education** - Users don't know 3 canonical invocation methods
2. **Cross-Skill Handoffs** - No session_context schema reference for state passing
3. **Persistence Compliance** - P-002 requirement not explicitly documented
4. **Self-Assessment** - No self-critique checklist for quality validation

---

## Business Value

Complete SKILL.md compliance enables:

1. **User Self-Service** - Clear documentation for all invocation methods
2. **Seamless Integration** - State schema versioning prevents breaking changes
3. **Quality Assurance** - Self-critique checklist ensures consistent outputs
4. **Maintainability** - Standard structure matches other Jerry skills

### Features Unlocked

- User can invoke individual agents via Task tool
- Cross-skill state handoffs (transcript → problem-solving)
- Automated compliance verification

---

## Technical Approach

Add missing PAT-SKILL-001 sections to SKILL.md while preserving existing content.

### Files to Modify

| File | Current Version | Target Version |
|------|-----------------|----------------|
| skills/transcript/SKILL.md | 2.2.0 | 2.3.0 |

### Sections to Add

**Section: Invoking an Agent**

```markdown
## Invoking an Agent

There are three ways to invoke individual agents from the transcript skill:

### Method 1: Task Tool (Recommended)

The orchestrator can use the Task tool to delegate work to a specific agent:

```
Claude: Use the Task tool to invoke ts-extractor with input from ts-parser output at output/index.json
```

### Method 2: Natural Language

For interactive use, describe the agent invocation in natural language:

```
"Run ts-extractor on the parsed transcript at output/index.json to extract entities"
```

### Method 3: Direct Import (Advanced)

For orchestration contexts, agents can be imported directly via the skill's agent registry.
This method is for advanced users building custom workflows.

**Warning:** Direct imports bypass skill-level validation and state management.
```

**Section: Enhanced State Passing**

```markdown
## State Passing Between Agents

### State Key Registry

| Agent | Output Key | Provides | Schema Version |
|-------|------------|----------|----------------|
| ts-parser | `ts_parser_output` | canonical_json_path, index_json_path, chunks_dir | 2.0.0 |
| ts-extractor | `ts_extractor_output` | extraction_report_path, entity_count, confidence_summary | 1.3.0 |
| ts-formatter | `ts_formatter_output` | packet_dir, packet_index_path | 1.1.0 |
| ts-mindmap-* | `ts_mindmap_output` | mindmap_dir, mermaid_files | 1.0.0 |

### Session Context Schema

All transcript agents use the universal session context schema:

```yaml
session_context:
  schema: "docs/schemas/session_context.json"
  schema_version: "1.0.0"
  input_validation: true
  output_validation: true
```

This enables seamless handoffs to other Jerry skills (problem-solving, nasa-se, orchestration).
```

**Section: Mandatory Persistence (P-002)**

```markdown
## Mandatory Persistence (P-002)

All transcript skill agents MUST persist their output to files. This ensures:

1. **Context Rot Resistance** - Findings survive session compaction
2. **Knowledge Accumulation** - Artifacts build project knowledge base
3. **Auditability** - Processing can be traced and reviewed
4. **Collaboration** - Outputs can be shared and referenced

### Output Structure

```
transcript-{id}/
├── canonical/                  # Parser output
│   ├── canonical-transcript.json
│   ├── index.json
│   └── chunks/
├── 00-index.md through 07-topics.md  # Formatted packet
├── 08-mindmap/                 # Mindmap output
└── _anchors.json               # Anchor registry
```

**Rule:** Transient-only output VIOLATES P-002.
```

**Section: Self-Critique Checklist (add to Constitutional Compliance)**

```markdown
### Self-Critique Checklist

Before finalizing significant outputs, verify:

1. **P-001:** Are all extractions based on verifiable transcript content?
2. **P-002:** Are all outputs persisted to files (not just returned)?
3. **P-003:** Am I operating as a worker agent (not spawning subagents)?
4. **P-004:** Do all entities have citations to source segments?
5. **P-022:** Am I being transparent about confidence scores and limitations?
```

---

## Children (Tasks)

### Task Inventory

| ID | Title | Status | Effort | Owner |
|----|-------|--------|--------|-------|
| TASK-407 | Add "Invoking an Agent" section | pending | 1h | Claude |
| TASK-408 | Enhance "State Passing" with session_context | pending | 2h | Claude |
| TASK-409 | Add "Mandatory Persistence (P-002)" section | pending | 1h | Claude |
| TASK-410 | Add self-critique checklist to Constitutional Compliance | pending | 1h | Claude |
| TASK-411 | Restructure persona and add output sections in agents | pending | 2h | Claude |

### Task Links

- [TASK-407: Add Invoking an Agent section](./TASK-407-add-invoking-section.md)
- [TASK-408: Enhance State Passing section](./TASK-408-enhance-state-passing.md)
- [TASK-409: Add Mandatory Persistence section](./TASK-409-add-persistence-section.md)
- [TASK-410: Add self-critique checklist](./TASK-410-add-self-critique.md)
- [TASK-411: Restructure persona and output sections](./TASK-411-restructure-persona-output.md)

---

## Progress Summary

### Status Overview

```
+------------------------------------------------------------------+
|                   ENABLER PROGRESS TRACKER                        |
+------------------------------------------------------------------+
| Tasks:     [....................] 0% (0/5 completed)             |
| Effort:    [....................] 0% (0/9 hours completed)       |
+------------------------------------------------------------------+
| Overall:   [....................] 0%                             |
+------------------------------------------------------------------+
```

### Progress Metrics

| Metric | Value |
|--------|-------|
| **Total Tasks** | 5 |
| **Completed Tasks** | 0 |
| **Total Effort (hours)** | 9 |
| **Completed Effort** | 0 |
| **Completion %** | 0% |

---

## Acceptance Criteria

### Definition of Done

- [ ] SKILL.md has "Invoking an Agent" section with 3 methods documented
- [ ] State Passing section includes session_context schema reference
- [ ] "Mandatory Persistence (P-002)" section added
- [ ] Constitutional Compliance includes self-critique checklist (5+ items)
- [ ] Agent persona sections moved to top-level (not nested under context)
- [ ] Agent output sections added with location templates
- [ ] SKILL.md Compliance Checklist (S-001 through S-051) scores >= 90%

### Technical Criteria

| # | Criterion | Verified |
|---|-----------|----------|
| TC-1 | "Invoking an Agent" section documents Task tool, natural language, direct import | [ ] |
| TC-2 | State schema includes `schema_version: "1.0.0"` | [ ] |
| TC-3 | P-002 section explicitly states transient-only output is forbidden | [ ] |
| TC-4 | Self-critique checklist references P-001, P-002, P-003, P-004, P-022 | [ ] |

---

## Evidence

### Deliverables

| Deliverable | Type | Description | Link |
|-------------|------|-------------|------|
| SKILL.md v2.3.0 | Documentation | Updated with PAT-SKILL-001 sections | skills/transcript/SKILL.md |

### Verification Checklist

- [ ] All acceptance criteria verified
- [ ] All tasks completed
- [ ] SKILL.md Compliance Checklist completed

---

## Risks and Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Breaking existing references | Low | Medium | Preserve all existing section anchors |
| Documentation bloat | Medium | Low | Keep new sections concise with examples |

---

## Dependencies

### Depends On

- [EN-027: Agent Definition Compliance](../EN-027-agent-definition-compliance/EN-027-agent-definition-compliance.md) - Agent YAML must be standardized first

### Enables

- [EN-029: Documentation Compliance](../EN-029-documentation-compliance/EN-029-documentation-compliance.md)
- Users can invoke agents correctly

---

## Related Items

### Hierarchy

- **Parent:** [FEAT-005: Skill Compliance](../FEAT-005-skill-compliance.md)

### Related Items

- **Gap Analysis:** [work-026-e-002](../../../../../docs/analysis/work-026-e-002-transcript-skill-gap-analysis.md) - Section "Dimension 1: SKILL.md Structure Compliance"
- **Pattern Reference:** [work-026-e-003](../../../../../docs/synthesis/work-026-e-003-jerry-skill-compliance-framework.md) - Section 1.1 (PAT-SKILL-001)
- **Checklist Reference:** work-026-e-003 Section 2.1 (Master SKILL.md Compliance Checklist)

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-01-30T16:00:00Z | Claude | pending | Enabler created per FEAT-005 Phase 2 (HIGH). Addresses 6 high-severity gaps in SKILL.md. |

---

## System Mapping

| System | Mapping |
|--------|---------|
| **Azure DevOps** | PBI with ValueArea=Architectural |
| **SAFe** | Enabler (Compliance type) |
| **JIRA** | Story with 'enabler' label |
