# FEAT-002:DISC-010: Skill Invocation Failure - TASK-164 Execution

<!--
TEMPLATE: Discovery
VERSION: 1.1.0
SOURCE: ONTOLOGY-v1.md Section 3.4.9, worktracker.md (Discovery File)
CREATED: 2026-01-29
PURPOSE: Document process failure where Claude bypassed required skill invocations
-->

> **Type:** discovery
> **Status:** DOCUMENTED
> **Priority:** HIGH
> **Impact:** HIGH
> **Created:** 2026-01-29T00:00:00Z
> **Completed:** 2026-01-29T00:00:00Z
> **Parent:** FEAT-002
> **Owner:** Claude
> **Source:** User feedback during TASK-164 execution

---

## Frontmatter

```yaml
id: "FEAT-002:DISC-010"
work_type: DISCOVERY
title: "Skill Invocation Failure - TASK-164 Execution"
classification: TECHNICAL
status: DOCUMENTED
resolution: CORRECTIVE_ACTION_DEFINED
priority: HIGH
impact: HIGH
assignee: "Claude"
created_by: "Claude"
created_at: "2026-01-29T00:00:00Z"
updated_at: "2026-01-29T00:00:00Z"
completed_at: "2026-01-29T00:00:00Z"
parent_id: "FEAT-002"
tags:
  - "process-failure"
  - "skill-invocation"
  - "quality-assurance"
  - "audit-trail"
finding_type: GAP
confidence_level: HIGH
source: "User feedback during TASK-164 execution review"
research_method: "Post-incident analysis"
validated: true
validation_date: "2026-01-29T00:00:00Z"
validated_by: "Human"
```

---

## State Machine

**Current State:** `DOCUMENTED`

```
PENDING → IN_PROGRESS → DOCUMENTED → VALIDATED
                            ↑
                       (current)
```

---

## Summary

Claude executed TASK-164 (Schema Extensibility Research) by performing research directly using WebSearch and Context7 tools instead of invoking the required `@problem-solving` skill with `ps-researcher` agent. Additionally, quality reviews (ps-critic, nse-qa) were run as inline Task agents without persisting outputs to reviewable files.

**Key Findings:**
- ps-researcher agent was NOT invoked - research executed manually by Claude
- ps-critic and nse-qa outputs were NOT persisted to files (no audit trail)
- CLAUDE.md requirements for proactive skill usage were violated
- Research document created at wrong path (`docs/research/` vs `research/`)

**Validation:** Human-identified during output review

---

## Context

### Background

TASK-164 required research on JSON Schema extensibility patterns to address 4 gaps identified in DISC-006. The task acceptance criteria specified:
- ps-critic score >= 0.85 (with persisted output)
- nse-qa score >= 0.85 (with persisted output)
- Use of problem-solving frameworks (5W2H, Ishikawa, FMEA)

CLAUDE.md explicitly states:
> "You MUST use @problem-solving for research/analysis tasks"
> "DO NOT WAIT for user to invoke skills - use them proactively"

### Research Question

Why did Claude bypass the required skill invocations and what corrective actions are needed?

### Investigation Approach

1. Review conversation transcript to identify exact execution path
2. Compare expected vs actual workflow
3. Document root cause and corrective actions
4. Define remediation plan with proper skill invocation

---

## Finding

### Process Violations Identified

| Violation ID | Description | Severity | Root Cause |
|--------------|-------------|----------|------------|
| V-001 | ps-researcher not invoked | HIGH | Claude executed research directly instead of via skill |
| V-002 | ps-critic output not persisted | HIGH | Run as inline Task, output in conversation only |
| V-003 | nse-qa output not persisted | HIGH | Run as inline Task, output in conversation only |
| V-004 | Wrong research file path | MEDIUM | Created in `docs/research/` instead of `research/` |
| V-005 | TASK-164 marked DONE prematurely | HIGH | No reviewable artifacts for human verification |

**Key Observations:**

1. **Research Execution Path (Incorrect):**
   ```
   Claude → WebSearch/Context7 (direct) → Write research document
   ```

   **Should Have Been:**
   ```
   Claude → @problem-solving skill → ps-researcher agent → Research document
   ```

2. **Quality Review Path (Incorrect):**
   ```
   Claude → Task tool (inline) → Agent returns text → No file persistence
   ```

   **Should Have Been:**
   ```
   Claude → @problem-solving skill → ps-critic agent → critiques/en014-task164-*.md
   Claude → @problem-solving skill → nse-qa agent → qa/en014-task164-*.md
   ```

3. **File Path Violation:**
   - Created: `EN-014-domain-context-files/docs/research/EN-014-e-164-schema-extensibility.md`
   - Correct: `EN-014-domain-context-files/research/EN-014-e-164-schema-extensibility.md`

### Root Cause Analysis (5 Whys)

```
WHY 1: Why was ps-researcher not invoked?
→ Claude executed WebSearch and Context7 directly

WHY 2: Why did Claude execute tools directly?
→ Defaulted to familiar tool invocation pattern instead of skill invocation

WHY 3: Why did Claude default to direct tools?
→ Skill invocation requires additional orchestration step

WHY 4: Why was the additional step skipped?
→ Insufficient process discipline / lack of pre-execution checklist

WHY 5: Why was there no pre-execution checklist?
→ No explicit checkpoint to verify skill invocation before tool execution

ROOT CAUSE: Missing process gate to verify skill requirements before direct tool execution
```

### Validation

**Human Validation:**
- User identified missing critic outputs: "why where are the outputs from the critic that I can review?"
- User identified skill bypass: "Why didn't you use the ps-researcher to perform the research?"
- User confirmed corrective action required: "Yes Claude, re-do it properly"

---

## Evidence

### Source Documentation

| Evidence ID | Type | Description | Source | Date |
|-------------|------|-------------|--------|------|
| E-001 | Conversation | User question about missing critic outputs | Session transcript | 2026-01-29 |
| E-002 | Conversation | User question about ps-researcher bypass | Session transcript | 2026-01-29 |
| E-003 | File | Research document at wrong path | docs/research/ | 2026-01-29 |
| E-004 | Absence | No files in critiques/ directory | EN-014-domain-context-files/ | 2026-01-29 |
| E-005 | Absence | No files in qa/ directory | EN-014-domain-context-files/ | 2026-01-29 |

### Reference Material

- **Source:** CLAUDE.md
- **Section:** Mandatory Skill Usage (PROACTIVE)
- **Relevance:** Defines requirement for proactive skill invocation

---

## Implications

### Impact on Project

1. **TASK-164 must be re-executed** - Current output lacks proper provenance
2. **Quality review artifacts missing** - No audit trail for human verification
3. **Process trust affected** - Demonstrates need for execution discipline

### Design Decisions Affected

- **Decision:** TASK-164 workflow
  - **Impact:** Must add explicit skill invocation step
  - **Rationale:** Ensures proper agent chain and artifact persistence

### Risks Identified

| Risk | Severity | Mitigation |
|------|----------|------------|
| Pattern may repeat in future tasks | HIGH | Create pre-execution checklist for research tasks |
| Manual research may differ from agent research | MEDIUM | Compare outputs to validate convergence |
| Audit trail gaps in other enablers | LOW | Spot-check prior quality reviews for persistence |

### Opportunities Created

- **Research Comparison:** Can compare manual research vs ps-researcher output to validate consistency
- **Process Improvement:** Opportunity to document explicit skill invocation checklist

---

## Relationships

### Creates

- TASK-164 Remediation Plan (embedded in ORCHESTRATION.yaml)

### Informs

- TASK-165, TASK-166, TASK-167, TASK-168 (blocked by TASK-164 proper completion)
- Future research task execution patterns

### Related Discoveries

- [FEAT-002--DISC-004](./FEAT-002--DISC-004-agent-instruction-compliance-failure.md) - Prior agent compliance issue

### Related Artifacts

| Type | Path | Description |
|------|------|-------------|
| Parent | [FEAT-002-implementation.md](./FEAT-002-implementation.md) | Parent feature |
| Task | [TASK-164](./EN-014-domain-context-files/TASK-164-research-schema-extensibility.md) | Task requiring remediation |
| Manual Research | [docs/research/EN-014-e-164-schema-extensibility.md](./EN-014-domain-context-files/docs/research/EN-014-e-164-schema-extensibility.md) | Incorrectly created research |

---

## Recommendations

### Immediate Actions

1. **Revert TASK-164 status** to IN_PROGRESS
2. **Move manual research** to `research/EN-014-e-164-schema-extensibility-manual.md`
3. **Create remediation workflow** in ORCHESTRATION.yaml
4. **Execute ps-researcher** via @problem-solving skill (fresh, uninfluenced)
5. **Compare research outputs** using ps-synthesizer
6. **Persist quality reviews** to critiques/ and qa/ directories

### Long-term Considerations

- Create pre-execution checklist for research tasks
- Add skill invocation verification to META TODO items
- Consider automation to detect direct tool usage when skill required

---

## Remediation Plan

### Phase 1: Preparation (Update State)

| Step | Action | Artifact |
|------|--------|----------|
| 1.1 | Create this discovery (DISC-010) | FEAT-002--DISC-010-skill-invocation-failure.md |
| 1.2 | Update ORCHESTRATION.yaml with remediation | ORCHESTRATION.yaml |
| 1.3 | Revert TASK-164 status to IN_PROGRESS | TASK-164-research-schema-extensibility.md |
| 1.4 | Move manual research to -manual.md | research/EN-014-e-164-schema-extensibility-manual.md |
| 1.5 | Update deliverable paths | TASK-164, EN-014, ORCHESTRATION.yaml |

### Phase 2: Fresh Research (ps-researcher)

| Step | Action | Artifact |
|------|--------|----------|
| 2.1 | Invoke @problem-solving with ps-researcher | research/EN-014-e-164-schema-extensibility.md |
| 2.2 | ps-researcher creates fresh research (no access to manual) | (new research document) |

### Phase 3: Research Comparison (ps-synthesizer)

| Step | Action | Artifact |
|------|--------|----------|
| 3.1 | Invoke ps-synthesizer with both research documents | research/EN-014-e-164-research-comparison.md |
| 3.2 | Document convergence/divergence of conclusions | (comparison analysis) |

### Phase 4: Quality Reviews (Persisted)

| Step | Action | Artifact |
|------|--------|----------|
| 4.1 | Invoke ps-critic on final research | critiques/en014-task164-iter1-critique.md |
| 4.2 | Invoke nse-qa on final research | qa/en014-task164-iter1-qa.md |
| 4.3 | Verify scores >= 0.85 | (quality gate) |

### Phase 5: Completion

| Step | Action | Artifact |
|------|--------|----------|
| 5.1 | Update TASK-164 status to DONE | TASK-164-research-schema-extensibility.md |
| 5.2 | Update ORCHESTRATION.yaml | ORCHESTRATION.yaml |
| 5.3 | Update EN-014 enabler | EN-014-domain-context-files.md |

---

## Document History

| Date | Author | Change |
|------|--------|--------|
| 2026-01-29 | Claude | Created discovery documenting TASK-164 skill invocation failure |

---

## Metadata

```yaml
id: "FEAT-002:DISC-010"
parent_id: "FEAT-002"
work_type: DISCOVERY
title: "Skill Invocation Failure - TASK-164 Execution"
status: DOCUMENTED
priority: HIGH
impact: HIGH
created_by: "Claude"
created_at: "2026-01-29T00:00:00Z"
updated_at: "2026-01-29T00:00:00Z"
completed_at: "2026-01-29T00:00:00Z"
tags: ["process-failure", "skill-invocation", "quality-assurance", "audit-trail"]
source: "User feedback during TASK-164 execution review"
finding_type: GAP
confidence_level: HIGH
validated: true
```
