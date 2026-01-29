# FEAT-004:DISC-012: CLI Integration Gap in TDD-FEAT-004

<!--
TEMPLATE: Discovery
VERSION: 1.1.0
SOURCE: ONTOLOGY-v1.md Section 3.4.9, worktracker.md (Discovery File)
CREATED: 2026-01-29
PURPOSE: Document critical gap in TDD-FEAT-004 regarding Jerry CLI integration
-->

> **Type:** discovery
> **Status:** VALIDATED
> **Priority:** CRITICAL
> **Impact:** HIGH
> **Created:** 2026-01-29T22:00:00Z
> **Completed:** 2026-01-29T23:55:00Z
> **Parent:** FEAT-004
> **Owner:** Human + Claude
> **Source:** Human Review (TASK-244 Human Approval Gate)
> **Resolution:** FL-001 executed - TDD-FEAT-004 v1.1.0 amended with Section 11

---

## Frontmatter

```yaml
# =============================================================================
# DISCOVERY WORK ITEM
# Source: ONTOLOGY-v1.md Section 3.4.9 (Discovery Entity Schema)
# Purpose: Document CLI integration gap discovered during human TDD review
# =============================================================================

# Identity (inherited from WorkItem)
id: "FEAT-004:DISC-012"
work_type: DISCOVERY
title: "CLI Integration Gap in TDD-FEAT-004"

# Classification
classification: TECHNICAL

# State
status: DOCUMENTED
resolution: null

# Priority
priority: CRITICAL

# Impact
impact: HIGH

# People
assignee: "Claude"
created_by: "Human + Claude"

# Timestamps
created_at: "2026-01-29T22:00:00Z"
updated_at: "2026-01-29T22:00:00Z"
completed_at: "2026-01-29T22:00:00Z"

# Hierarchy
parent_id: "FEAT-004"

# Tags
tags:
  - "cli-integration"
  - "tdd-gap"
  - "feedback-loop"
  - "phase-3-revision"

# =============================================================================
# DISCOVERY-SPECIFIC PROPERTIES
# =============================================================================

# Finding Classification
finding_type: GAP
confidence_level: HIGH

# Source Information
source: "Human review during TASK-244 Human Approval Gate"
research_method: "Human TDD review + Claude cross-reference analysis"

# Validation
validated: true
validation_date: "2026-01-29T22:00:00Z"
validated_by: "Human"

# Impact
impact: HIGH
```

---

## State Machine

**Current State:** `VALIDATED`

```
PENDING -> IN_PROGRESS -> DOCUMENTED -> VALIDATED
                                             ^
                                             |
                                        (current)
```

**Remediation Complete:** Feedback Loop FL-001 executed 2026-01-29T23:55:00Z

---

## Summary

**TDD-FEAT-004 is missing the entire Jerry CLI integration specification that TDD-EN014 established as the reference pattern.** This omission means the hybrid infrastructure has no specification for how users will invoke the Python parser via the CLI, breaking architectural consistency with other TDD documents.

**Key Findings:**
- TDD-FEAT-004 has NO sections covering CLI integration (`jerry transcript parse <file>`)
- TDD-EN014 provides comprehensive CLI integration pattern (Section 10, ~230 lines)
- The gap was identified during human review at TASK-244 (Phase 5 Human Gate)
- Original scoping should have captured this as a decision but context was lost across sessions

**Validation:** Human-identified and validated during TDD review.

---

## Context

### Background

During the TASK-244 Human Approval Gate review of TDD-FEAT-004-hybrid-infrastructure.md, the human reviewer identified that the TDD lacks any reference to Jerry CLI integration. This is a significant omission because:

1. **TDD-EN014 establishes the CLI integration pattern** - It includes a complete Section 10 (~230 lines) covering parser registration, main routing, CLIAdapter methods, bootstrap wiring, and sequence diagrams.

2. **The CLI approach solves dependency problems** - Using the Jerry CLI avoids putting Python code in scripts with external dependencies. The CLI acts as the entry point for the deterministic processing layer.

3. **Architectural consistency** - All TDDs should follow the same pattern for CLI integration to ensure the codebase is coherent and maintainable.

4. **Lost context** - There was reportedly an "explicit prompt" to research CLI integration strategy that should have been captured in a decision document, but context was lost across session rollovers.

### Research Question

**Why was CLI integration omitted from TDD-FEAT-004, and what is required to remediate this gap?**

### Investigation Approach

1. Read TDD-EN014-domain-schema-v2.md to understand the CLI integration pattern
2. Grep TDD-FEAT-004 for CLI-related keywords to confirm the gap
3. Cross-reference with DISC-009 and ADR-001 for architectural context
4. Document the gap and required remediation
5. Request feedback loop to Phase 3 per ORCHESTRATION protocol

---

## Finding

### Gap Analysis: TDD-EN014 vs TDD-FEAT-004

| Component | TDD-EN014 | TDD-FEAT-004 | Gap |
|-----------|-----------|--------------|-----|
| Section 6.2: CLI Integration Sequence Diagram | ✓ Present (lines 1129-1176) | ✗ Missing | CRITICAL |
| Section 10.1: Parser Registration | ✓ Present (lines 1501-1546) | ✗ Missing | CRITICAL |
| Section 10.2: Main Routing | ✓ Present (lines 1556-1586) | ✗ Missing | CRITICAL |
| Section 10.3: CLIAdapter Method | ✓ Present (lines 1600-1682) | ✗ Missing | CRITICAL |
| Section 10.4: Bootstrap Wiring | ✓ Present (lines 1688-1722) | ✗ Missing | CRITICAL |
| CLI Command Specification | `jerry transcript validate-domain` | None specified | CRITICAL |
| Pipeline Position Documentation | ✓ Lines 1492-1500 | ✗ Missing | HIGH |

### What TDD-EN014 Section 10 Contains

TDD-EN014 Section 10: Jerry CLI Integration provides:

1. **Parser Registration** (`src/interface/cli/parser.py`):
   - `_add_transcript_namespace()` function
   - Subparser for `validate-domain` command
   - Argument definitions (`path`, `--schema-version`)

2. **Main Routing** (`src/interface/cli/main.py`):
   - `_handle_transcript()` routing function
   - Command dispatch to adapter methods

3. **CLIAdapter Method** (`src/interface/cli/adapter.py`):
   - `cmd_transcript_validate_domain()` method
   - Query dispatch, result formatting, JSON output support
   - Error handling (FileNotFoundError, etc.)

4. **Bootstrap Wiring** (`src/bootstrap.py`):
   - Factory function `create_domain_validator()`
   - Handler registration with dispatcher

5. **Sequence Diagrams**:
   - CLI Integration Sequence (USER → CLI → ADAPTER → HANDLER → VALIDATOR)
   - Skill Integration Sequence (ORCHESTRATOR → ts-parser → VALIDATOR)

### What TDD-FEAT-004 Should Specify

For the hybrid infrastructure, the TDD should specify:

1. **CLI Command**: `jerry transcript parse <file.vtt|.srt|.txt>`
2. **Parser Registration**: Add `parse` subcommand to transcript namespace
3. **CLIAdapter Method**: `cmd_transcript_parse()` that invokes Python VTT/SRT parser
4. **Bootstrap Wiring**: Factory for VTTParser, handler registration
5. **Sequence Diagrams**: CLI → Python Parser → Canonical JSON → ts-extractor flow

### Root Cause

1. **Context Loss**: The original scoping prompt to research CLI integration strategy was lost across session rollovers. No DEC-* decision document was created to capture this requirement.

2. **Pattern Deviation**: TDD-FEAT-004 was created without referencing TDD-EN014 as the template for CLI integration.

3. **Validation Gap**: The ps-critic quality review (TASK-243) scored 0.97 but did not catch this gap because CLI integration wasn't in the validation criteria checklist.

---

## Evidence

### Source Documentation

| Evidence ID | Type | Description | Source | Date |
|-------------|------|-------------|--------|------|
| E-001 | TDD | TDD-EN014 Section 10 (CLI Integration) | `EN-014-domain-context-files/docs/design/TDD-EN014-domain-schema-v2.md` lines 1492-1723 | 2026-01-29 |
| E-002 | TDD | TDD-FEAT-004 (no CLI sections) | `FEAT-004-hybrid-infrastructure/docs/design/TDD-FEAT-004-hybrid-infrastructure.md` | 2026-01-29 |
| E-003 | Grep | Only 1 mention of parser.py in TDD-FEAT-004 | `grep "CLI\|jerry\|bootstrap\|parser\.py\|adapter\.py"` | 2026-01-29 |
| E-004 | Human | Human review identified gap | TASK-244 Human Approval Gate | 2026-01-29 |

### Reference Material

- **Source:** TDD-EN014-domain-schema-v2.md
- **URL:** `projects/PROJ-008-transcript-skill/work/EPIC-001-transcript-skill/FEAT-002-implementation/EN-014-domain-context-files/docs/design/TDD-EN014-domain-schema-v2.md`
- **Date Accessed:** 2026-01-29
- **Relevance:** Establishes the CLI integration pattern for all transcript skill TDDs

---

## Implications

### Impact on Project

This gap has the following impacts:

1. **TDD-FEAT-004 cannot be approved** without CLI integration specification
2. **Implementation work (EN-020..023) is blocked** until TDD is amended
3. **Architectural inconsistency** between domain validation (EN-014) and hybrid parsing (FEAT-004)

### Design Decisions Affected

- **Decision:** DEC-011 (ts-parser Hybrid Role)
  - **Impact:** The decision mentions Python parser delegation but doesn't specify CLI invocation
  - **Rationale:** CLI integration is a prerequisite for Python parser execution

### Risks Identified

| Risk | Severity | Mitigation |
|------|----------|------------|
| Implementation diverges from architecture | HIGH | Add CLI section to TDD before implementation |
| Developer confusion on entry point | MEDIUM | Document CLI command clearly |
| Lost traceability to original prompt | LOW | Create DEC-012 to capture CLI strategy decision |

---

## Relationships

### Creates

- **Feedback Loop Request**: Return to Phase 3 (ps-architect) for TDD amendment
- **DEC-012** (proposed): CLI Integration Strategy for Hybrid Infrastructure

### Informs

- [TASK-244](./TASK-244-human-approval.md) - Human Approval Gate (REJECTED due to this gap)
- [TDD-FEAT-004](./docs/design/TDD-FEAT-004-hybrid-infrastructure.md) - Requires Section 10 addition

### Related Discoveries

- [DISC-009](../FEAT-002-implementation/FEAT-002--DISC-009-agent-only-architecture-limitation.md) - Agent-Only Architecture Limitation (parent discovery for FEAT-004)
- [DISC-011](../FEAT-002-implementation/FEAT-002--DISC-011-disc009-operational-findings-gap.md) - DISC-009 Operational Findings Gap

### Related Artifacts

| Type | Path | Description |
|------|------|-------------|
| Parent | [FEAT-004-hybrid-infrastructure.md](./FEAT-004-hybrid-infrastructure.md) | Parent feature |
| Reference TDD | [TDD-EN014-domain-schema-v2.md](../FEAT-002-implementation/EN-014-domain-context-files/docs/design/TDD-EN014-domain-schema-v2.md) | CLI integration pattern template |
| ORCHESTRATION | [ORCHESTRATION.yaml](./ORCHESTRATION.yaml) | Workflow state |

---

## Recommendations

### Immediate Actions

1. **REJECT TDD-FEAT-004 at TASK-244** (Human Approval Gate) with feedback documented
2. **Request Feedback Loop** to Phase 3 (ps-architect) per ORCHESTRATION protocol
3. **Update ORCHESTRATION.yaml** with feedback loop state

### TDD Amendment Requirements

The TDD amendment should add:

1. **Section 10: Jerry CLI Integration** (following TDD-EN014 pattern)
   - Section 10.1: Parser Registration (add `parse` command)
   - Section 10.2: Main Routing (`_handle_transcript` update)
   - Section 10.3: CLIAdapter Method (`cmd_transcript_parse`)
   - Section 10.4: Bootstrap Wiring (VTTParser factory)

2. **Section 6.2 Update**: Add CLI Integration Sequence Diagram

3. **Update Section 4 (EN-020)**: Reference CLI entry point in Python Parser spec

### Long-term Considerations

- Create DEC-012 to formally capture CLI integration strategy
- Update ps-critic validation criteria to include CLI integration check
- Ensure future TDDs reference TDD-EN014 Section 10 as the CLI integration template

---

## Open Questions

### Questions for Follow-up

1. **Q:** What was the original prompt about CLI integration strategy that was lost?
   - **Investigation Method:** Review conversation transcripts if available
   - **Priority:** LOW (we can proceed without it)

2. **Q:** Should we create a shared CLI integration template that all TDDs reference?
   - **Investigation Method:** Discuss with human during DEC-012 creation
   - **Priority:** MEDIUM

---

## Document History

| Date | Author | Change |
|------|--------|--------|
| 2026-01-29T23:55:00Z | ps-architect (FL-001) | Status VALIDATED - TDD-FEAT-004 v1.1.0 amended with Section 11 |
| 2026-01-29T22:00:00Z | Claude | Created discovery based on human review feedback |

---

## Metadata

```yaml
id: "FEAT-004:DISC-012"
parent_id: "FEAT-004"
work_type: DISCOVERY
title: "CLI Integration Gap in TDD-FEAT-004"
status: DOCUMENTED
priority: CRITICAL
impact: HIGH
created_by: "Human + Claude"
created_at: "2026-01-29T22:00:00Z"
updated_at: "2026-01-29T22:00:00Z"
completed_at: "2026-01-29T22:00:00Z"
tags: ["cli-integration", "tdd-gap", "feedback-loop", "phase-3-revision"]
source: "Human review during TASK-244"
finding_type: GAP
confidence_level: HIGH
validated: true
```

---

<!--
DISCOVERY VALIDATION:

This discovery documents a critical gap identified during human TDD review.
The gap is validated by:
1. Direct comparison of TDD-EN014 Section 10 (~230 lines) vs TDD-FEAT-004 (0 lines)
2. Grep search confirming only 1 parser-related mention in TDD-FEAT-004
3. Human explicit identification during TASK-244 review

REMEDIATION PATH:
1. Update ORCHESTRATION.yaml with feedback loop
2. Return to Phase 3 (ps-architect) for TDD amendment
3. Add Section 10: Jerry CLI Integration following TDD-EN014 pattern
4. Re-run Phase 4 (ps-critic) validation
5. Return to Phase 5 (Human Approval)
-->
