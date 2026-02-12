# Synthesis: Worktracker Agent Design Proposal

<!--
TEMPLATE: Synthesis
VERSION: 1.0.0
SOURCE: PS Entry e-303 (ps-synthesizer)
CREATED: 2026-02-02 (Claude/ps-synthesizer)
PURPOSE: Consolidate research and analysis into actionable design proposal for worktracker agents
QG-1 REVIEW: PASSED (ps-critic: 0.895 CONDITIONAL, nse-qa: 0.92 CONFORMANT)
-->

> **Type:** synthesis
> **Status:** completed
> **Priority:** high
> **Created:** 2026-02-02T17:00:00Z
> **Parent:** FEAT-002 (CLAUDE.md Optimization)
> **Owner:** Claude (ps-synthesizer)
> **Source Artifacts:**
>   - `research-worktracker-agent-design.md` (Score: 0.88)
>   - `analysis-worktracker-agent-decomposition.md` (Score: 0.91)
> **Combined QG-1 Score:** 0.895 (CONDITIONAL PASS)

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Executive Summary](#executive-summary) | Key decisions and outcomes |
| [Agent Specifications](#agent-specifications) | Complete specs for wt-verifier, wt-visualizer, wt-auditor |
| [Skill Integration Plan](#skill-integration-plan) | How /worktracker invokes agents |
| [Shared Rules](#shared-rules) | Rules to create in `.context/` |
| [Implementation Roadmap](#implementation-roadmap) | Phased delivery plan |
| [File Structure](#file-structure) | Directory layout for new agents |
| [Risk Mitigations](#risk-mitigations) | Validated risks and mitigations |
| [Verification Plan Summary](#verification-plan-summary) | Test scenarios from analysis |
| [References](#references) | Source citations |

---

## Executive Summary

### L0: What We're Building (ELI5)

We're adding three specialized "helper agents" to the worktracker skill - like having three expert assistants who each do one job really well:

1. **wt-verifier**: The "quality checker" who makes sure all acceptance criteria are met before marking work complete
2. **wt-visualizer**: The "diagram maker" who creates pictures showing how work items relate to each other
3. **wt-auditor**: The "inspector" who checks all the files follow the rules and nothing is broken or missing

These helpers follow one important rule: they do their job and report back to the manager (Claude/MAIN CONTEXT) - they never hire their own helpers (P-003 compliance).

### L1: Technical Summary (Software Engineer)

This synthesis consolidates findings from validated research and analysis artifacts to define three worktracker agents following the function-based decomposition pattern (Option B, score 4.55/5.0):

| Agent | Model | Purpose | Primary Requirement |
|-------|-------|---------|---------------------|
| `wt-verifier` | sonnet | Acceptance criteria validation before closure | AC-5, WTI-002 |
| `wt-visualizer` | haiku | Mermaid diagram generation for hierarchy/timeline/status | NFC-2 |
| `wt-auditor` | sonnet | Cross-file integrity auditing and template compliance | AC-7, WTI-001 |

**Key Technical Decisions:**
- Agents are workers invoked by MAIN CONTEXT (P-003 compliant)
- All outputs persisted to filesystem (P-002 compliant)
- Session context schema used for state passing (Google ADK pattern)
- WTI rules (WTI-001 through WTI-006) enforced by agents

### L2: Architectural Implications (Principal Architect)

**Trade-off Analysis Summary:**

The function-based decomposition (Option B) was selected over entity-based (Option C) based on:

| Criterion | Function-Based | Entity-Based | Decision |
|-----------|----------------|--------------|----------|
| Maintainability | O(3 agents) | O(6+ agents) | Function-based scales better |
| Code Reuse | High (same logic, any entity) | Low (duplicated per entity) | Function-based reduces duplication |
| P-003 Risk | Low (clear worker pattern) | Medium (temptation to chain) | Function-based is safer |

**One-Way Door Assessment:** LOW
- Agent addition is reversible (can remove without breaking existing skill)
- Rules-based fallback remains valid
- No schema migrations required

**Long-term Considerations:**
- Agent versioning may be needed as skill evolves
- ps-critic integration deferred until basic agents proven
- Metrics collection (invocation count, success rate) recommended for future iteration

---

## Agent Specifications

### wt-verifier: Status Verification Agent

#### Purpose

Validates that work item acceptance criteria are met and evidence is provided before status transitions to DONE. Enforces WTI-002 (No Closure Without Verification) and WTI-006 (Evidence-Based Closure).

#### YAML Frontmatter

```yaml
---
name: wt-verifier
version: "1.0.0"
description: "Verify work item acceptance criteria before closure"

model: sonnet  # Balanced analysis for verification tasks

identity:
  role: "Status Verification Specialist"
  expertise:
    - "Acceptance criteria validation"
    - "Evidence verification"
    - "WTI rule enforcement"
  cognitive_mode: "convergent"

persona:
  tone: "professional"
  communication_style: "direct"
  audience_level: "adaptive"

capabilities:
  allowed_tools:
    - Read
    - Glob
    - Grep
    - Write
  forbidden_actions:
    - "Spawn subagents (P-003)"
    - "Modify work item status directly"
    - "Return transient output only (P-002)"

guardrails:
  input_validation:
    - work_item_path_exists: true
    - verification_scope_valid: "full | acceptance_criteria | evidence"
  output_filtering:
    - no_false_positives
    - all_failures_documented
  fallback_behavior: warn_and_retry

inputs:
  required:
    - work_item_path: "Absolute path to work item markdown file"
    - verification_scope: "full | acceptance_criteria | evidence"
  optional:
    - parent_context: "Parent work item path for rollup validation"
    - strict_mode: "boolean - fail on warnings (default: false)"

outputs:
  primary:
    location: "projects/${JERRY_PROJECT}/work/**/*-verification-report.md"
  schema:
    verification_result:
      passed: boolean
      score: float  # 0.0-1.0
      work_item_id: string
      verification_scope: string
      criteria_results:
        - criterion_id: string
          criterion_text: string
          verified: boolean
          evidence_link: string | null
          notes: string | null
      blocking_issues: array
      recommendations: array
      timestamp: string  # ISO 8601

error_handling:
  on_file_not_found: "Return error report with path checked"
  on_missing_criteria: "Return partial result with warning"
  on_invalid_format: "Attempt recovery, report parse errors"

wti_rules_enforced:
  - "WTI-002: No Closure Without Verification"
  - "WTI-003: Truthful State (won't mark incomplete as complete)"
  - "WTI-006: Evidence-Based Closure"

constitution:
  reference: "docs/governance/JERRY_CONSTITUTION.md"
  principles_applied:
    - "P-002: File Persistence (Medium)"
    - "P-003: No Recursive Subagents (Hard)"
    - "P-022: No Deception (Hard)"
---
```

#### Verification Checks

| Check Category | Validation | Severity |
|----------------|------------|----------|
| **Acceptance Criteria** | All AC items have checkbox | ERROR |
| **Acceptance Criteria** | At least 80% AC checked | ERROR |
| **Evidence** | Evidence section exists | ERROR |
| **Evidence** | At least one evidence link | WARNING |
| **Status Consistency** | Child items all DONE if parent DONE | ERROR |
| **Template Compliance** | Required sections present | WARNING |

#### Invocation Pattern

```
User: "Verify EN-001 is ready for closure"
          |
          v
    MAIN CONTEXT (Claude)
          |
          |---> Read EN-001 file (understand context)
          |
          |---> Task(
          |       agent: "wt-verifier",
          |       prompt: "Verify acceptance criteria for EN-001",
          |       input: {
          |         work_item_path: "projects/PROJ-001/.../EN-001-*.md",
          |         verification_scope: "full"
          |       }
          |     )
          |        |
          |        +---> Returns: verification-report.md
          |
          +---> Present findings to user
          +---> Update EN-001 status if passed
```

---

### wt-visualizer: Diagram Generation Agent

#### Purpose

Generates Mermaid diagrams for worktracker hierarchies, timelines, status overviews, and dependency chains. Supports NFC-2 (OSS contributor understanding in < 5 minutes).

#### YAML Frontmatter

```yaml
---
name: wt-visualizer
version: "1.0.0"
description: "Generate Mermaid diagrams for worktracker hierarchies"

model: haiku  # Fast model for diagram generation (low complexity)

identity:
  role: "Visualization Specialist"
  expertise:
    - "Mermaid diagram syntax"
    - "Worktracker entity hierarchy"
    - "Visual information design"
  cognitive_mode: "convergent"

persona:
  tone: "accessible"
  communication_style: "educational"
  audience_level: "L0"  # Diagrams should be universally understandable

capabilities:
  allowed_tools:
    - Read
    - Glob
    - Grep
    - Write
  forbidden_actions:
    - "Spawn subagents (P-003)"
    - "Modify work item content"
    - "Return transient output only (P-002)"

guardrails:
  input_validation:
    - root_path_exists: true
    - diagram_type_valid: "hierarchy | timeline | status | dependencies"
  output_filtering:
    - valid_mermaid_syntax
    - no_sensitive_data_in_diagram
  fallback_behavior: warn_and_retry

inputs:
  required:
    - root_path: "Path to root work item (Epic, Feature, etc.)"
    - diagram_type: "hierarchy | timeline | status | dependencies"
  optional:
    - depth: "integer - max depth to traverse (default: 3)"
    - include_status: "boolean - show status colors (default: true)"
    - output_format: "mermaid | ascii | both (default: mermaid)"

outputs:
  primary:
    location: "projects/${JERRY_PROJECT}/work/**/*-diagram.md"
  schema:
    diagram_result:
      diagram_type: string
      mermaid_code: string
      ascii_fallback: string | null
      entities_included: integer
      max_depth_reached: integer
      root_entity_id: string
      warnings: array
      generated_at: string  # ISO 8601

diagram_types:
  hierarchy:
    syntax: "flowchart TD"
    use_case: "Entity parent-child relationships"
    example: |
      flowchart TD
          subgraph Strategic
              Epic --> Feature
          end
          subgraph Delivery
              Feature --> Story
              Feature --> Enabler
          end

  timeline:
    syntax: "gantt"
    use_case: "Project schedule and progress"
    example: |
      gantt
          title Project Timeline
          dateFormat YYYY-MM-DD
          section Phase 1
          Research :done, p1, 2026-02-01, 2d
          Analysis :active, p2, after p1, 3d

  status:
    syntax: "stateDiagram-v2"
    use_case: "Work item lifecycle states"
    example: |
      stateDiagram-v2
          [*] --> pending
          pending --> in_progress : start
          in_progress --> completed : finish

  dependencies:
    syntax: "flowchart LR"
    use_case: "Dependency chains and blocking relationships"
    example: |
      flowchart LR
          EN-001 -->|blocks| EN-002
          EN-002 -->|enables| FEAT-001

constitution:
  reference: "docs/governance/JERRY_CONSTITUTION.md"
  principles_applied:
    - "P-002: File Persistence (Medium)"
    - "P-003: No Recursive Subagents (Hard)"
---
```

#### Mermaid Syntax Guidelines

| Category | Guideline | Source |
|----------|-----------|--------|
| **Direction** | `flowchart TD` for hierarchies, `flowchart LR` for workflows | Official Mermaid docs |
| **States** | Use `stateDiagram-v2` for lifecycles | Official Mermaid docs |
| **Gantt** | Use `done`, `active`, `crit` markers | Official Mermaid docs |
| **Colors** | Use `style` for status indication | Jerry Convention |
| **Subgraphs** | Group by entity category (Strategic, Delivery, Quality) | Jerry Convention |

---

### wt-auditor: Integrity Audit Agent

#### Purpose

Audits worktracker integrity across multiple files, checking template compliance, relationship integrity, orphan detection, and WTI rule adherence. Supports AC-7 (template references work correctly).

#### YAML Frontmatter

```yaml
---
name: wt-auditor
version: "1.0.0"
description: "Audit worktracker integrity across multiple files"

model: sonnet  # Balanced analysis for comprehensive auditing

identity:
  role: "Integrity Audit Specialist"
  expertise:
    - "Cross-file consistency checking"
    - "Template compliance validation"
    - "WTI rule enforcement"
    - "Orphan detection"
  cognitive_mode: "convergent"

persona:
  tone: "professional"
  communication_style: "direct"
  audience_level: "adaptive"

capabilities:
  allowed_tools:
    - Read
    - Glob
    - Grep
    - Write
  forbidden_actions:
    - "Spawn subagents (P-003)"
    - "Auto-fix issues without user approval"
    - "Return transient output only (P-002)"

guardrails:
  input_validation:
    - audit_scope_exists: true
    - audit_type_valid: "full | templates | relationships | orphans"
  output_filtering:
    - no_false_positives
    - all_issues_documented_with_remediation
  fallback_behavior: warn_and_retry

inputs:
  required:
    - audit_scope: "Path to audit (folder or WORKTRACKER.md)"
    - audit_type: "full | templates | relationships | orphans"
  optional:
    - fix_mode: "report | suggest | interactive (default: report)"
    - severity_threshold: "error | warning | info (default: warning)"

outputs:
  primary:
    location: "projects/${JERRY_PROJECT}/work/**/*-audit-report.md"
    template: ".context/templates/worktracker/AUDIT_REPORT.md"
  schema:
    audit_result:
      passed: boolean
      audit_type: string
      audit_scope: string
      total_issues: integer
      errors: array
      warnings: array
      info: array
      remediation_plan:
        - issue_id: string
          description: string
          remediation: string
          effort: string  # low | medium | high
      files_checked: integer
      coverage_percentage: float
      timestamp: string  # ISO 8601

audit_checks:
  template_compliance:
    description: "Verify files match .context/templates/worktracker/ structure"
    severity: "error"
    checks:
      - "Required sections present (Summary, Acceptance Criteria, etc.)"
      - "Frontmatter metadata complete"
      - "Status values valid (pending | in_progress | completed)"

  relationship_integrity:
    description: "Verify parent-child links are bidirectional"
    severity: "error"
    checks:
      - "Parent ID in child matches actual parent"
      - "Parent references child in Children section"
      - "No circular dependencies"

  orphan_detection:
    description: "Find work items not linked from any parent"
    severity: "warning"
    checks:
      - "All items reachable from WORKTRACKER.md"
      - "No files in work/ without parent linkage"

  status_consistency:
    description: "Verify parent status reflects child completion"
    severity: "warning"
    checks:
      - "Parent not DONE if children not all DONE"
      - "Blocked items have blocker documented"

  id_format:
    description: "Verify IDs follow naming conventions"
    severity: "info"
    checks:
      - "Format: {TYPE}-{NNN}-{slug}"
      - "IDs are unique within scope"

wti_rules_enforced:
  - "WTI-001: Real-Time State (files reflect actual state)"
  - "WTI-003: Truthful State (no false completion claims)"
  - "WTI-004: Synchronize Before Reporting"
  - "WTI-005: Atomic State Updates"

constitution:
  reference: "docs/governance/JERRY_CONSTITUTION.md"
  principles_applied:
    - "P-002: File Persistence (Medium)"
    - "P-003: No Recursive Subagents (Hard)"
    - "P-010: Task Tracking Integrity (Medium)"
---
```

---

## Skill Integration Plan

### How /worktracker Invokes Agents

The `/worktracker` skill invokes agents through the MAIN CONTEXT orchestration pattern, maintaining P-003 compliance.

```
                         +------------------------+
                         |       User Request     |
                         |  "Verify EN-001 ready" |
                         +------------------------+
                                     |
                                     v
+------------------------------------------------------------------------+
|                         MAIN CONTEXT (Claude)                          |
|                                                                         |
|  1. Recognize worktracker operation                                     |
|  2. Load skill rules via: @rules/worktracker-behavior-rules.md         |
|  3. Determine appropriate agent                                         |
|  4. Invoke agent via Task tool (P-003 compliant)                        |
|  5. Process agent output                                                |
|  6. Present results to user                                             |
+------------------------------------------------------------------------+
           |                    |                    |
           v                    v                    v
  +----------------+   +------------------+   +----------------+
  |  wt-verifier   |   |  wt-visualizer   |   |  wt-auditor    |
  |    (Worker)    |   |     (Worker)     |   |    (Worker)    |
  +----------------+   +------------------+   +----------------+
           |                    |                    |
           v                    v                    v
  +----------------+   +------------------+   +----------------+
  | verification-  |   |    *-diagram.md  |   | audit-report.md|
  |   report.md    |   |                  |   |                |
  +----------------+   +------------------+   +----------------+
```

### Agent Selection Logic (for MAIN CONTEXT)

| User Intent | Detected Keywords | Agent to Invoke |
|-------------|-------------------|-----------------|
| Verify completion | "verify", "check ready", "validate AC" | wt-verifier |
| Generate diagram | "diagram", "visualize", "show hierarchy" | wt-visualizer |
| Audit integrity | "audit", "check integrity", "find orphans" | wt-auditor |
| Status report | "status of", "progress on" | wt-verifier + wt-visualizer |

### Updated SKILL.md Section (to add)

```markdown
## Worktracker Agents

The worktracker skill includes specialized agents for advanced operations:

| Agent | Purpose | Invocation |
|-------|---------|------------|
| `wt-verifier` | Validate acceptance criteria before closure | "Verify {work-item} is ready for closure" |
| `wt-visualizer` | Generate Mermaid diagrams | "Create a hierarchy diagram for {epic/feature}" |
| `wt-auditor` | Audit cross-file integrity | "Audit the worktracker for {project}" |

### Agent Files

| Agent | Location |
|-------|----------|
| wt-verifier | `skills/worktracker/agents/wt-verifier.md` |
| wt-visualizer | `skills/worktracker/agents/wt-visualizer.md` |
| wt-auditor | `skills/worktracker/agents/wt-auditor.md` |
| Template | `skills/worktracker/agents/WT_AGENT_TEMPLATE.md` |

### P-003 Compliance

Agents are invoked via the Task tool from MAIN CONTEXT. Agents DO NOT invoke other agents.
```

---

## Shared Rules

### Rules to Create in `.context/`

The following shared rule files support agent operations:

#### 1. Worktracker Integrity Rules (WTI)

**Location:** `.context/templates/worktracker/WTI_RULES.md`

```markdown
# Worktracker Integrity (WTI) Rules

## WTI-001: Real-Time State
Work item files MUST reflect the actual state of work. Updates MUST be made immediately after work completion, not batched.

## WTI-002: No Closure Without Verification
Work items MUST NOT transition to DONE/COMPLETED without:
- All acceptance criteria checked (80%+ verified)
- Evidence section populated with at least one link
- Child items all completed (if applicable)

## WTI-003: Truthful State
Work items MUST NOT be marked complete if work is incomplete. Status MUST accurately reflect reality.

## WTI-004: Synchronize Before Reporting
Before generating status reports, agents MUST read current worktracker state to avoid stale information.

## WTI-005: Atomic State Updates
When updating work item status, BOTH the item file AND parent reference MUST be updated atomically.

## WTI-006: Evidence-Based Closure
The Evidence section MUST contain verifiable proof of completion before closure. Links to commits, PRs, test results, or documentation are required.
```

#### 2. Audit Report Template

**Location:** `.context/templates/worktracker/AUDIT_REPORT.md`

```markdown
# Audit Report: {{AUDIT_SCOPE}}

> **Type:** audit-report
> **Generated:** {{TIMESTAMP}}
> **Agent:** wt-auditor
> **Audit Type:** {{AUDIT_TYPE}}
> **Scope:** {{AUDIT_SCOPE}}

---

## Summary

| Metric | Value |
|--------|-------|
| **Files Checked** | {{FILES_CHECKED}} |
| **Coverage** | {{COVERAGE_PCT}}% |
| **Total Issues** | {{TOTAL_ISSUES}} |
| **Errors** | {{ERROR_COUNT}} |
| **Warnings** | {{WARNING_COUNT}} |
| **Info** | {{INFO_COUNT}} |
| **Verdict** | {{PASSED_OR_FAILED}} |

---

## Issues Found

### Errors

| ID | File | Issue | Remediation |
|----|------|-------|-------------|
{{ERROR_TABLE}}

### Warnings

| ID | File | Issue | Remediation |
|----|------|-------|-------------|
{{WARNING_TABLE}}

### Info

| ID | File | Issue | Remediation |
|----|------|-------|-------------|
{{INFO_TABLE}}

---

## Remediation Plan

{{REMEDIATION_PLAN}}

---

## Files Audited

{{FILE_LIST}}
```

#### 3. Verification Report Template

**Location:** `.context/templates/worktracker/VERIFICATION_REPORT.md`

```markdown
# Verification Report: {{WORK_ITEM_ID}}

> **Type:** verification-report
> **Generated:** {{TIMESTAMP}}
> **Agent:** wt-verifier
> **Scope:** {{VERIFICATION_SCOPE}}

---

## Summary

| Metric | Value |
|--------|-------|
| **Work Item** | {{WORK_ITEM_ID}} |
| **Status** | {{CURRENT_STATUS}} |
| **Verification Score** | {{SCORE}}% |
| **Verdict** | {{PASSED_OR_FAILED}} |

---

## Acceptance Criteria Verification

| # | Criterion | Verified | Evidence |
|---|-----------|----------|----------|
{{AC_TABLE}}

---

## Blocking Issues

{{BLOCKING_ISSUES_OR_NONE}}

---

## Recommendations

{{RECOMMENDATIONS_OR_NONE}}

---

## Ready for Closure

**{{YES_NO}}** - {{RATIONALE}}
```

---

## Implementation Roadmap

### Phased Delivery Plan

```
+----------------------------------------------------------------------+
|                    IMPLEMENTATION ROADMAP                             |
+----------------------------------------------------------------------+
|                                                                       |
|  PHASE 1: Foundation (Day 1-2)                                       |
|  +-----------------------------------------------------------------+ |
|  | - Create WT_AGENT_TEMPLATE.md (adapt from PS_AGENT_TEMPLATE)    | |
|  | - Create WTI_RULES.md in .context/                               | |
|  | - Create VERIFICATION_REPORT.md template                         | |
|  | - Create AUDIT_REPORT.md template                                | |
|  +-----------------------------------------------------------------+ |
|                                |                                      |
|                                v                                      |
|  PHASE 2: wt-verifier (Day 3-4)                                      |
|  +-----------------------------------------------------------------+ |
|  | - Implement wt-verifier.md agent definition                      | |
|  | - Test with sample EN-XXX verification                           | |
|  | - Update SKILL.md with agent documentation                       | |
|  +-----------------------------------------------------------------+ |
|                                |                                      |
|                                v                                      |
|  PHASE 3: wt-visualizer (Day 5-6)                                    |
|  +-----------------------------------------------------------------+ |
|  | - Implement wt-visualizer.md agent definition                    | |
|  | - Test hierarchy, timeline, status diagram types                 | |
|  | - Validate Mermaid syntax output                                 | |
|  +-----------------------------------------------------------------+ |
|                                |                                      |
|                                v                                      |
|  PHASE 4: wt-auditor (Day 7-8)                                       |
|  +-----------------------------------------------------------------+ |
|  | - Implement wt-auditor.md agent definition                       | |
|  | - Test full audit on PROJ-001                                    | |
|  | - Validate remediation plan generation                           | |
|  +-----------------------------------------------------------------+ |
|                                |                                      |
|                                v                                      |
|  PHASE 5: Integration (Day 9-10)                                     |
|  +-----------------------------------------------------------------+ |
|  | - Update SKILL.md with agent documentation                       | |
|  | - Create test scenarios (VER-001 through AUD-005)                | |
|  | - Integration testing (INT-001 through INT-003)                  | |
|  | - Documentation review                                           | |
|  +-----------------------------------------------------------------+ |
|                                                                       |
+----------------------------------------------------------------------+
```

### Milestone Criteria

| Phase | Complete When |
|-------|---------------|
| Phase 1 | Templates exist, WTI rules documented |
| Phase 2 | wt-verifier returns valid verification reports |
| Phase 3 | wt-visualizer produces valid Mermaid syntax |
| Phase 4 | wt-auditor identifies known issues in test project |
| Phase 5 | All 18 test scenarios pass, docs updated |

---

## File Structure

### New Files to Create

```
skills/worktracker/
|
+-- agents/                                   # NEW DIRECTORY
|   |
|   +-- WT_AGENT_TEMPLATE.md                 # Template for wt-* agents
|   +-- wt-verifier.md                       # Status verification agent
|   +-- wt-visualizer.md                     # Diagram generation agent
|   +-- wt-auditor.md                        # Integrity audit agent
|   +-- README.md                            # Agent catalog
|
+-- rules/                                   # EXISTING
    +-- ...

.context/templates/worktracker/
|
+-- WTI_RULES.md                             # NEW: WTI rule definitions
+-- VERIFICATION_REPORT.md                   # NEW: Verification report template
+-- AUDIT_REPORT.md                          # NEW: Audit report template
+-- ...
```

### File Responsibilities

| File | Responsibility | Size Estimate |
|------|----------------|---------------|
| `WT_AGENT_TEMPLATE.md` | Base template for wt-* agents | ~200 lines |
| `wt-verifier.md` | Full agent definition | ~300 lines |
| `wt-visualizer.md` | Full agent definition | ~250 lines |
| `wt-auditor.md` | Full agent definition | ~350 lines |
| `WTI_RULES.md` | WTI rule reference | ~50 lines |
| `VERIFICATION_REPORT.md` | Output template | ~75 lines |
| `AUDIT_REPORT.md` | Output template | ~100 lines |

---

## Risk Mitigations

### Validated Risks from Research/Analysis

| ID | Risk | Likelihood | Impact | Mitigation | Status |
|----|------|------------|--------|------------|--------|
| R1 | Agents add unnecessary complexity for simple workflows | MEDIUM | MEDIUM | Make agents optional; rules-based approach still works | MITIGATED |
| R2 | P-003 violation if agents try to orchestrate each other | LOW | HIGH | Explicit forbidden_actions in agent definitions; contract tests | MITIGATED |
| R3 | Agent definitions become stale as rules evolve | MEDIUM | LOW | Agents reference rules via @import; single source of truth | MITIGATED |
| R4 | Users confused about when to use agents vs rules | MEDIUM | MEDIUM | Clear documentation in SKILL.md with decision tree | PLANNED |

### New Mitigations Added

| Mitigation | Implementation |
|------------|----------------|
| **P-003 Contract Test** | Add to `tests/architecture/` to scan agent files for Task tool patterns |
| **Agent Version Tracking** | YAML frontmatter includes version field; increment on changes |
| **Fallback Documentation** | SKILL.md documents when rules-only approach is sufficient |

---

## Verification Plan Summary

### Test Scenario Coverage (from Analysis)

#### wt-verifier Tests

| ID | Scenario | Pass Criteria |
|----|----------|---------------|
| VER-001 | Valid complete enabler | `passed: true`, all criteria checked |
| VER-002 | Incomplete enabler | `passed: false`, missing evidence listed |
| VER-003 | Missing acceptance criteria | Graceful failure, clear error message |
| VER-004 | Invalid file path | `error: file_not_found`, path echoed |
| VER-005 | Parent rollup verification | Child status aggregation correct |

#### wt-visualizer Tests

| ID | Scenario | Pass Criteria |
|----|----------|---------------|
| VIS-001 | Feature hierarchy | Valid flowchart syntax, all enablers included |
| VIS-002 | Epic timeline | Valid gantt syntax, dates correct |
| VIS-003 | Status diagram | Valid stateDiagram-v2 syntax |
| VIS-004 | Deep hierarchy | Warning if truncated, depth honored |
| VIS-005 | Empty project | Graceful handling, "No work items" note |

#### wt-auditor Tests

| ID | Scenario | Pass Criteria |
|----|----------|---------------|
| AUD-001 | Clean project | `passed: true`, zero errors |
| AUD-002 | Template violation | `passed: false`, template check failed |
| AUD-003 | Broken relationship | Orphan detected, parent suggested |
| AUD-004 | ID format violation | ID format error, correction suggested |
| AUD-005 | Full audit | All checks run, coverage > 95% |

#### Integration Tests

| ID | Scenario | Agents Involved | Pass Criteria |
|----|----------|-----------------|---------------|
| INT-001 | Pre-closure workflow | wt-verifier -> MAIN | Block if failed, allow if passed |
| INT-002 | Status dashboard | wt-visualizer + wt-auditor | Combined reports generated |
| INT-003 | New contributor onboarding | wt-visualizer | Hierarchy diagram aids comprehension |

---

## References

### Source Artifacts

| Artifact | Score | Key Contribution |
|----------|-------|------------------|
| `research-worktracker-agent-design.md` | 0.88 | Industry patterns, Mermaid best practices, P-003 compliance |
| `research-worktracker-agent-design-addendum.md` | - | Error handling, testing strategies, WTI rules |
| `analysis-worktracker-agent-decomposition.md` | 0.91 | 5W2H analysis, trade-off matrix, agent interfaces |
| `analysis-worktracker-agent-decomposition-addendum.md` | - | RTM, verification plan, weight justification |

### Critiques

| Critique | Verdict | Score |
|----------|---------|-------|
| `ps-critic-rereview-research-analysis.md` | CONDITIONAL PASS | 0.895 |
| `nse-qa-rereview-research-analysis.md` | CONFORMANT | 0.92 |

### Industry Sources

| Source | Key Finding |
|--------|-------------|
| Anthropic Claude Code | Layered architecture, orchestration agents |
| LangChain Multi-Agent | "2-4 specialized agents" guidance |
| Google ADK Patterns | Explicit state passing schemas |
| Microsoft Azure AI | Coordinator/supervisor pattern |
| OpenAI Agent Guide | Reflective loops with circuit breakers |

### Jerry Framework Sources

| Source | Key Finding |
|--------|-------------|
| Jerry Constitution v1.0 | P-003 (no recursion), P-002 (persistence) |
| PS_AGENT_TEMPLATE.md | YAML frontmatter schema, XML body structure |
| skills/worktracker/SKILL.md | Entity hierarchy, template locations |
| .claude/rules/testing-standards.md | Test pyramid, BDD cycle |

---

## Metadata

```yaml
synthesis_id: "PROJ-001-e-303"
parent_artifacts:
  - "research-worktracker-agent-design.md"
  - "research-worktracker-agent-design-addendum.md"
  - "analysis-worktracker-agent-decomposition.md"
  - "analysis-worktracker-agent-decomposition-addendum.md"
qg1_critiques:
  - "ps-critic-rereview-research-analysis.md"
  - "nse-qa-rereview-research-analysis.md"
combined_qg1_score: 0.895
feat_002_requirements_addressed:
  - "AC-5: /worktracker skill loads all entity information"
  - "AC-7: All template references work correctly"
  - "NFC-2: OSS contributor can understand structure in < 5 minutes"
agents_specified: 3
implementation_phases: 5
estimated_effort_days: 10
created_by: "Claude (ps-synthesizer)"
created_at: "2026-02-02T17:00:00Z"
constitutional_compliance:
  - "P-001: Truth and Accuracy"
  - "P-002: File Persistence"
  - "P-003: No Recursive Subagents"
  - "P-004: Explicit Provenance"
```

---

*Synthesis Version: 1.0.0*
*QG-1 Review: PASSED (Combined Score: 0.895)*
*Constitutional Compliance: Jerry Constitution v1.0*
*Created: 2026-02-02*
