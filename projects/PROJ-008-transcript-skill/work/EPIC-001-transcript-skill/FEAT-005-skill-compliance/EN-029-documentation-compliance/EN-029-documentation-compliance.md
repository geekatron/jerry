# EN-029: Documentation Compliance

<!--
TEMPLATE: Enabler
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.9
CREATED: 2026-01-30 per FEAT-005 Phase 3 (MEDIUM)
PURPOSE: Bring PLAYBOOK.md to PAT-PLAYBOOK-001 compliance
-->

> **Type:** enabler
> **Status:** pending
> **Priority:** medium
> **Impact:** medium
> **Enabler Type:** compliance
> **Created:** 2026-01-30T16:00:00Z
> **Due:** TBD
> **Completed:** -
> **Parent:** FEAT-005
> **Owner:** Claude
> **Effort:** 9h

---

## Summary

Add anti-pattern catalog and enhance PLAYBOOK.md structure to comply with PAT-PLAYBOOK-001 (Triple-Lens Playbook). This is Phase 3 (MEDIUM) of the skill compliance remediation.

**Technical Scope:**
- Add L2 "Architecture & Constraints" section
- Create anti-pattern catalog with 4+ anti-patterns
- Add constraints and boundaries table
- Declare orchestration pattern (Sequential Chain)
- Add cross-skill integration section

**Gaps Addressed:**
- GAP-D-001: PLAYBOOK.md missing L2 structure (MEDIUM)
- GAP-D-002: Anti-pattern catalog missing (HIGH - included here)
- GAP-D-003: Constraints table missing (MEDIUM)
- GAP-O-001: Orchestration pattern not declared (MEDIUM)

---

## Problem Statement

Transcript PLAYBOOK.md has excellent operational content but lacks:

1. **L2 Architectural Guidance** - No deep-dive for principal architects
2. **Anti-Pattern Documentation** - Known failure modes undocumented
3. **Pattern Declaration** - Uses Sequential Chain but doesn't name it
4. **Constraints Reference** - Hard vs soft limits not clearly documented

---

## Business Value

Complete PLAYBOOK.md compliance enables:

1. **Architect Onboarding** - L2 section provides design rationale
2. **Error Prevention** - Anti-patterns prevent known failure modes
3. **Pattern Reuse** - Explicit pattern declaration enables workflow composition
4. **Clear Boundaries** - Constraints table prevents scope creep

### Features Unlocked

- Architects understand design decisions
- Users avoid documented anti-patterns
- Orchestration workflows can reference patterns by name

---

## Technical Approach

Add PAT-PLAYBOOK-001 L2 sections to PLAYBOOK.md.

### Files to Modify

| File | Current Version | Target Version |
|------|-----------------|----------------|
| skills/transcript/docs/PLAYBOOK.md | 1.1.0 | 1.2.0 |

### Sections to Add

**Section: Anti-Pattern Catalog**

```markdown
## L2: Architecture & Constraints

### Anti-Pattern Catalog

#### AP-T-001: Reading canonical-transcript.json Directly

+===================================================================+
| ANTI-PATTERN: Reading canonical-transcript.json Directly         |
+===================================================================+
| SYMPTOM:    ts-extractor receives ~930KB canonical file as input |
| CAUSE:      Skipping chunked architecture (index + chunks/)      |
| IMPACT:     Context window overflow, 99.8% data loss (DISC-009)  |
| FIX:        ALWAYS use index.json + chunks/*.json                |
+===================================================================+

Diagram:

❌ WRONG:
ts-parser → canonical-transcript.json (930KB)
              ↓
         ts-extractor (FAIL - context overflow)

✅ CORRECT:
ts-parser → index.json (8KB) + chunks/ (130KB each)
              ↓
         ts-extractor (SUCCESS - manageable chunks)

**Reference:** DISC-009 - Large File Context Window Analysis

---

#### AP-T-002: Skipping index.json Metadata

+===================================================================+
| ANTI-PATTERN: Skipping index.json Metadata                       |
+===================================================================+
| SYMPTOM:    Missing speaker list, transcript metadata            |
| CAUSE:      Reading chunks directly without index                |
| IMPACT:     Incomplete entity extraction, missing context        |
| FIX:        ALWAYS read index.json first, then chunks            |
+===================================================================+

---

#### AP-T-003: Stats-Array Mismatch

+===================================================================+
| ANTI-PATTERN: Stats-Array Mismatch                               |
+===================================================================+
| SYMPTOM:    extraction_stats.questions != len(questions)         |
| CAUSE:      Counting "?" syntactically vs extracting semantically|
| IMPACT:     Quality score failure (BUG-002, 4.2x inflation)      |
| FIX:        INV-EXT-001 - Stats MUST equal array lengths         |
+===================================================================+

**Reference:** BUG-002 - Extraction Question Count Discrepancy

---

#### AP-T-004: Transient-Only Output

+===================================================================+
| ANTI-PATTERN: Transient-Only Output                              |
+===================================================================+
| SYMPTOM:    Agent returns results but no file created            |
| CAUSE:      Not persisting to file system                        |
| IMPACT:     Output lost on context compaction (P-002 violation)  |
| FIX:        ALWAYS write output to files                         |
+===================================================================+
```

**Section: Orchestration Pattern Declaration**

```markdown
### Orchestration Pattern

**Pattern Used:** Sequential Chain (Pattern 2)

This workflow follows **Pattern 2: Sequential Chain** from the orchestration catalog.
Each agent depends on the output of the previous agent in strict order.

```
ts-parser → ts-extractor → ts-formatter → ts-mindmap-* → ps-critic
```

**Rationale:**
- Extraction requires parsed transcript
- Formatting requires extraction report
- Mindmaps require formatted packet
- Quality review requires all outputs

**Reference:** orchestration SKILL.md - Pattern 2
```

**Section: Constraints & Boundaries**

```markdown
### Constraints & Boundaries

| Constraint | Type | Limit | Enforcement |
|------------|------|-------|-------------|
| Chunk token limit | Hard | 18,000 tokens | Pipeline aborts |
| Packet file token limit | Soft | 31,500 tokens | Auto-split at heading |
| Packet file token limit | Hard | 35,000 tokens | Force split |
| Quality score threshold | Soft | 0.90 | Warning + continue |
| Subagent recursion | Hard | 0 levels | P-003 violation |
| Canonical file context | Hard | DO NOT READ | 99.8% data loss |
```

---

## Children (Tasks)

### Task Inventory

| ID | Title | Status | Effort | Owner |
|----|-------|--------|--------|-------|
| TASK-412 | Add L2 section structure to PLAYBOOK.md | pending | 1h | Claude |
| TASK-413 | Create anti-pattern catalog (4+ patterns) | pending | 4h | Claude |
| TASK-414 | Declare orchestration pattern (Sequential Chain) | pending | 1h | Claude |
| TASK-415 | Add constraints and boundaries table | pending | 1h | Claude |

### Task Links

- [TASK-412: Add L2 section structure](./TASK-412-add-l2-section.md)
- [TASK-413: Create anti-pattern catalog](./TASK-413-create-anti-patterns.md)
- [TASK-414: Declare orchestration pattern](./TASK-414-declare-pattern.md)
- [TASK-415: Add constraints table](./TASK-415-add-constraints.md)

---

## Progress Summary

### Status Overview

```
+------------------------------------------------------------------+
|                   ENABLER PROGRESS TRACKER                        |
+------------------------------------------------------------------+
| Tasks:     [....................] 0% (0/4 completed)             |
| Effort:    [....................] 0% (0/9 hours completed)       |
+------------------------------------------------------------------+
| Overall:   [....................] 0%                             |
+------------------------------------------------------------------+
```

### Progress Metrics

| Metric | Value |
|--------|-------|
| **Total Tasks** | 4 |
| **Completed Tasks** | 0 |
| **Total Effort (hours)** | 9 |
| **Completed Effort** | 0 |
| **Completion %** | 0% |

---

## Acceptance Criteria

### Definition of Done

- [ ] PLAYBOOK.md has L2 "Architecture & Constraints" section
- [ ] Anti-pattern catalog has 4+ patterns with ASCII box format
- [ ] Orchestration pattern explicitly named (Pattern 2: Sequential Chain)
- [ ] Constraints table documents hard vs soft limits
- [ ] PLAYBOOK.md Compliance Checklist (P-001 through P-034) scores >= 90%

### Technical Criteria

| # | Criterion | Verified |
|---|-----------|----------|
| TC-1 | Anti-patterns include AP-T-001 (canonical file read) | [ ] |
| TC-2 | Anti-patterns include AP-T-003 (stats-array mismatch from BUG-002) | [ ] |
| TC-3 | Pattern declaration references orchestration catalog | [ ] |
| TC-4 | Constraints table distinguishes hard vs soft limits | [ ] |

---

## Evidence

### Deliverables

| Deliverable | Type | Description | Link |
|-------------|------|-------------|------|
| PLAYBOOK.md v1.2.0 | Documentation | Updated with PAT-PLAYBOOK-001 sections | skills/transcript/docs/PLAYBOOK.md |

### Verification Checklist

- [ ] All acceptance criteria verified
- [ ] All tasks completed
- [ ] PLAYBOOK.md Compliance Checklist completed

---

## Risks and Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Anti-pattern list incomplete | Medium | Low | Can add more patterns iteratively |
| Constraint values change | Low | Low | Note effective date in constraints table |

---

## Dependencies

### Depends On

- [EN-028: SKILL.md Compliance](../EN-028-skill-md-compliance/EN-028-skill-md-compliance.md) - SKILL.md patterns inform PLAYBOOK

### Enables

- [EN-030: Documentation Polish](../EN-030-documentation-polish/EN-030-documentation-polish.md)
- Better user guidance on avoiding common mistakes

---

## Related Items

### Hierarchy

- **Parent:** [FEAT-005: Skill Compliance](../FEAT-005-skill-compliance.md)

### Related Items

- **Gap Analysis:** [work-026-e-002](../../../../../docs/analysis/work-026-e-002-transcript-skill-gap-analysis.md) - Section "Dimension 4: Documentation Compliance"
- **Pattern Reference:** [work-026-e-003](../../../../../docs/synthesis/work-026-e-003-jerry-skill-compliance-framework.md) - Section 2.3 (PLAYBOOK.md Compliance Checklist)
- **Anti-Pattern Examples:** [work-026-e-003](../../../../../docs/synthesis/work-026-e-003-jerry-skill-compliance-framework.md) - Section 4.3

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-01-30T16:00:00Z | Claude | pending | Enabler created per FEAT-005 Phase 3 (MEDIUM). Addresses 4 documentation gaps including anti-pattern catalog. |

---

## System Mapping

| System | Mapping |
|--------|---------|
| **Azure DevOps** | PBI with ValueArea=Architectural |
| **SAFe** | Enabler (Compliance type) |
| **JIRA** | Story with 'enabler' label |
