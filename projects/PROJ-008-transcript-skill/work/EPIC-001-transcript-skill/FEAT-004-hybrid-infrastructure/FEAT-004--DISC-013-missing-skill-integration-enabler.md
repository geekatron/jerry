# FEAT-004:DISC-013: Missing SKILL.md Integration and ts-parser v2.0 Transformation Enabler

<!--
TEMPLATE: Discovery
VERSION: 1.1.0
SOURCE: ONTOLOGY-v1.md Section 3.4.9, worktracker.md (Discovery File)
CREATED: 2026-01-29
PURPOSE: Document critical gap - hybrid infrastructure components exist but SKILL.md orchestration never updated
-->

> **Type:** discovery
> **Status:** VALIDATED
> **Priority:** CRITICAL
> **Impact:** CRITICAL
> **Created:** 2026-01-29T18:00:00Z
> **Completed:** 2026-01-29T18:30:00Z
> **Parent:** FEAT-004
> **Owner:** Claude
> **Source:** Live test investigation (canonical-transcript.json 923KB)

---

## Frontmatter

```yaml
# =============================================================================
# DISCOVERY WORK ITEM
# Source: ONTOLOGY-v1.md Section 3.4.9 (Discovery Entity Schema)
# Purpose: Document missing enabler for SKILL.md hybrid integration
# =============================================================================

# Identity (inherited from WorkItem)
id: "FEAT-004:DISC-013"
work_type: DISCOVERY
title: "Missing SKILL.md Integration and ts-parser v2.0 Transformation Enabler"

# Classification
classification: TECHNICAL

# State
status: VALIDATED
resolution: REQUIRES_NEW_WORK

# Priority
priority: CRITICAL

# Impact
impact: CRITICAL

# People
assignee: "Claude"
created_by: "Claude"

# Timestamps
created_at: "2026-01-29T18:00:00Z"
updated_at: "2026-01-29T18:30:00Z"
completed_at: "2026-01-29T18:30:00Z"

# Hierarchy
parent_id: "FEAT-004"

# Tags
tags:
  - "skill-integration"
  - "ts-parser-v2"
  - "orchestration-gap"
  - "critical-gap"

# =============================================================================
# DISCOVERY-SPECIFIC PROPERTIES
# =============================================================================

# Finding Classification
finding_type: GAP
confidence_level: HIGH

# Source Information
source: "Live test investigation - canonical-transcript.json 923KB indicates old pipeline used"
research_method: "Timeline analysis, TDD specification comparison, enabler audit"

# Validation
validated: true
validation_date: "2026-01-29T18:30:00Z"
validated_by: "Claude"

# Impact
impact: CRITICAL
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

---

## Summary

**FEAT-004 created all Python infrastructure components (VTT parser, chunker, extractor adaptation) but NEVER created an enabler to integrate them into the SKILL.md orchestration pipeline.** The result: the live test on 2026-01-28 used the OLD agent-only pipeline, producing a 923KB canonical-transcript.json instead of the chunked output specified in the TDD.

**Key Findings:**
- TDD-FEAT-004 Section 3 specifies ts-parser.md v2.0 transformation (ORCHESTRATOR + DELEGATOR + FALLBACK + VALIDATOR)
- TDD-FEAT-004 Section 11 specifies `jerry transcript parse` CLI command
- EN-020..023 created Python components but NO enabler exists for integration
- SKILL.md still shows old pipeline: ts-parser (haiku LLM) → ts-extractor → ts-formatter → ps-critic
- Live test on 2026-01-28 used old pipeline (2 days BEFORE FEAT-004 marked done 2026-01-30)

**Validation:** Timeline analysis confirms live test pre-dates FEAT-004 completion, but even after FEAT-004, the integration was never done.

---

## Context

### Background

During investigation of why the live test output (`/validation/live-output-meeting-006/canonical-transcript.json`) was 923KB with 24,643 lines, we discovered a critical gap in FEAT-004 implementation:

1. **The live test was executed on 2026-01-28**
2. **FEAT-004 was marked done on 2026-01-30**
3. **FEAT-004 enablers (EN-020..023) created Python components**
4. **BUT no enabler was created to wire these components into SKILL.md**

### Research Question

**Why does the live test output show a single 923KB canonical-transcript.json instead of the chunked format (index.json + chunks/*.json) specified in the TDD?**

### Investigation Approach

1. Read TDD-FEAT-004 to understand intended architecture
2. Audit FEAT-004 enablers (EN-020, EN-021, EN-022, EN-023) for integration tasks
3. Compare SKILL.md current state vs. TDD specification
4. Analyze timeline of live test vs. FEAT-004 completion
5. Trace TDD Section 3 (ts-parser.md transformation) to implementation artifacts

---

## Finding

### Gap 1: Missing ts-parser.md v2.0 Transformation

**TDD Specification (Section 3):**
```yaml
Target Role: ORCHESTRATOR + DELEGATOR + FALLBACK + VALIDATOR
Processing Model: Strategy Pattern with Python delegation
Output: canonical-transcript.json + index.json + chunks/*.json
```

**Four Roles Specified:**
1. **ORCHESTRATOR:** Coordinate pipeline based on format and results
2. **DELEGATOR:** Route to Python parser or LLM fallback based on format
3. **FALLBACK:** Maintain LLM parsing for unsupported formats and error recovery
4. **VALIDATOR:** Validate Python parser output before downstream processing

**Current State:**
- ts-parser.md is still v1.2.0 (LLM parser only)
- No Strategy Pattern implementation
- No Python parser delegation

### Gap 2: Missing CLI Integration

**TDD Specification (Section 11):**
```python
# jerry transcript parse <file.vtt> --output-dir <dir> --chunk-size 500
```

**Section 11 specifies:**
- 11.1: Parser Registration (`_add_transcript_namespace()`)
- 11.2: Main Routing (`_handle_transcript()`)
- 11.3: CLIAdapter Method (`cmd_transcript_parse()`)
- 11.4: Bootstrap Wiring (VTTParser factory)

**Current State:**
- CLI `transcript` namespace NOT implemented
- `src/interface/cli/main.py` has no transcript routing

### Gap 3: Missing SKILL.md Orchestration Update

**TDD Section 10.4 (Backward Compatibility):**
```markdown
AFTER (v2.0.0):
  Input: VTT file
  → ts-parser (Orchestrator): Detect format
    IF VTT:
      → Python Parser: Deterministic parse
      → canonical-transcript.json + index.json + chunks/
    ELSE:
      → LLM Parser: Fallback (same as v1.2.0)
```

**Current SKILL.md:**
```markdown
| Agent | Model | Role | Output |
|-------|-------|------|--------|
| `ts-parser` | haiku | Parse VTT/SRT/TXT to canonical JSON | `canonical-transcript.json` |
```

**Gap:** SKILL.md orchestration section not updated to use hybrid pipeline

### Enabler Audit

| Enabler | Scope | Integration Work? |
|---------|-------|-------------------|
| EN-020 | Python VTT Parser | ✓ Code written | **No** |
| EN-021 | Chunking Strategy | ✓ Code written | **No** |
| EN-022 | ts-extractor Adaptation | ✓ Agent def updated | **No** |
| EN-023 | Integration Testing | ✓ Tests written | **No** - Tests use direct Python calls |
| **MISSING** | CLI + ts-parser.md + SKILL.md | - | **YES - CRITICAL GAP** |

### Root Cause Analysis

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         ROOT CAUSE: ENABLER SCOPING GAP                      │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  TDD-FEAT-004 specifies:                                                    │
│  ├── Section 3: ts-parser.md v2.0 transformation                            │
│  ├── Section 11: CLI integration (jerry transcript parse)                   │
│  └── Section 10: SKILL.md orchestration unchanged (internal change)         │
│                                                                              │
│  FEAT-004 Enablers created:                                                 │
│  ├── EN-020: Python Parser Implementation ✓                                 │
│  ├── EN-021: Chunking Strategy ✓                                            │
│  ├── EN-022: Extractor Adaptation ✓                                         │
│  └── EN-023: Integration Testing ✓                                          │
│                                                                              │
│  FEAT-004 Enablers MISSING:                                                 │
│  └── EN-025 (proposed): ts-parser v2.0 + CLI + SKILL.md Integration        │
│                                                                              │
│  The TDD was comprehensive but the enabler decomposition did NOT capture:   │
│  1. ts-parser.md agent definition transformation                            │
│  2. CLI transcript namespace implementation                                 │
│  3. SKILL.md orchestration update (internal implementation change)          │
│                                                                              │
│  This is a DECOMPOSITION GAP where the TDD requirements were not fully      │
│  mapped to executable enablers.                                             │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Evidence

### Source Documentation

| Evidence ID | Type | Description | Source | Date |
|-------------|------|-------------|--------|------|
| E-001 | Live Test Output | canonical-transcript.json 923KB, 24,643 lines | `/validation/live-output-meeting-006/` | 2026-01-28 |
| E-002 | TDD Section 3 | ts-parser.md v2.0 specification | `TDD-FEAT-004.md:266-458` | 2026-01-29 |
| E-003 | TDD Section 11 | CLI Integration specification | `TDD-FEAT-004.md:1882-1969` | 2026-01-29 |
| E-004 | SKILL.md | Still shows haiku LLM for ts-parser | `skills/transcript/SKILL.md:229` | 2026-01-29 |
| E-005 | EN-023 | Integration tests use direct Python calls, not SKILL.md | `EN-023-integration-testing.md:94-145` | 2026-01-29 |
| E-006 | FEAT-004 | Marked done 2026-01-30, but integration never created | `FEAT-004-hybrid-infrastructure.md:17` | 2026-01-30 |

### Timeline Analysis

```
2026-01-28 21:45   Live test executed (canonical-transcript.json created)
                   ↓
2026-01-28 22:00   FEAT-004 created from DISC-009 findings
                   ↓
2026-01-29         EN-020..023 implemented (Python components)
                   ↓
2026-01-30 03:00   FEAT-004 marked done (integration NOT implemented)
                   ↓
2026-01-29         Investigation reveals integration gap
```

**Critical Finding:** Even after FEAT-004 was "complete", the integration work was never done. The Python components exist but are not wired into the SKILL.md pipeline.

---

## Implications

### Impact on Project

1. **Live tests use old pipeline** - All validation tests prior to fix use 99.8% data loss path
2. **FEAT-004 is NOT complete** - Missing critical integration enabler
3. **Blocking EN-019, EN-023, TASK-236** - Test tasks cannot produce correct results until fixed

### Design Decisions Affected

- **Decision:** FEAT-004 completion criteria
  - **Impact:** Feature should be marked "in_progress" until integration done
  - **Rationale:** Python components exist but are not usable via SKILL.md

### Risks Identified

| Risk | Severity | Mitigation |
|------|----------|------------|
| Tests validating wrong pipeline | CRITICAL | Block tests until integration done |
| Continued use of 99.8% data loss path | CRITICAL | Prioritize EN-025 implementation |
| Future confusion about "done" enablers | MEDIUM | Update FEAT-004 status to in_progress |

### Blocking Impact

The following work items should be marked BLOCKED until EN-025 is complete:

| Work Item | Type | Reason |
|-----------|------|--------|
| EN-019 | Live Test | Cannot produce valid hybrid output |
| TASK-236 | E2E Test | Full pipeline test requires integration |
| EN-023 AC-4 | Integration | "ps-critic quality score >= 0.90" requires live execution |

---

## Relationships

### Creates

- **[EN-025](./EN-025-skill-integration/EN-025-skill-integration.md)** (proposed) - ts-parser v2.0 + CLI + SKILL.md Integration

### Blocks

- [EN-019](../FEAT-002-implementation/EN-019-live-skill-invocation/EN-019-live-skill-invocation.md) - Live Skill Invocation
- [TASK-236](./EN-023-integration-testing/TASK-236-full-pipeline-e2e.md) - Full Pipeline E2E Test

### Related Discoveries

- [DISC-009](../FEAT-002-implementation/FEAT-002--DISC-009-agent-only-architecture-limitation.md) - Agent-Only Architecture Limitation (parent discovery)
- [DISC-012](./FEAT-004--DISC-012-cli-integration-gap.md) - CLI Integration Gap in TDD (TDD specification gap)

### Related Artifacts

| Type | Path | Description |
|------|------|-------------|
| Parent | [FEAT-004-hybrid-infrastructure.md](./FEAT-004-hybrid-infrastructure.md) | Parent feature |
| TDD | [TDD-FEAT-004.md](./docs/design/TDD-FEAT-004-hybrid-infrastructure.md) | Technical Design Document |
| SKILL.md | [skills/transcript/SKILL.md](../../../../skills/transcript/SKILL.md) | Current orchestration (outdated) |

---

## Recommendations

### Immediate Actions

1. **Create EN-025: ts-parser v2.0 + CLI + SKILL.md Integration** enabler with tasks:
   - TASK-250: Update ts-parser.md to v2.0 (Strategy Pattern orchestrator)
   - TASK-251: Implement CLI transcript namespace (`jerry transcript parse`)
   - TASK-252: Update SKILL.md orchestration to use hybrid pipeline
   - TASK-253: Integration verification tests

2. **Mark FEAT-004 status as "in_progress"** until EN-025 complete

3. **Mark blocking tasks as BLOCKED**:
   - EN-019, TASK-236

### Long-term Considerations

- Add decomposition validation to feature planning process
- Ensure TDD sections map 1:1 to enablers
- Add "integration enabler" as mandatory for any feature with multiple components

---

## Open Questions

### Questions for Follow-up

1. **Q:** Should the CLI be implemented, or can SKILL.md directly invoke Python via Bash tool?
   - **Investigation Method:** Compare TDD specification vs. simpler direct invocation
   - **Priority:** HIGH - affects implementation approach

2. **Q:** Should we re-run EN-023 integration tests after fix?
   - **Investigation Method:** Analyze which tests need hybrid pipeline vs. direct Python
   - **Priority:** MEDIUM

---

## Document History

| Date | Author | Change |
|------|--------|--------|
| 2026-01-29T18:30:00Z | Claude | Validated discovery, created EN-025 recommendations |
| 2026-01-29T18:00:00Z | Claude | Created discovery based on live test investigation |

---

## Metadata

```yaml
id: "FEAT-004:DISC-013"
parent_id: "FEAT-004"
work_type: DISCOVERY
title: "Missing SKILL.md Integration and ts-parser v2.0 Transformation Enabler"
status: VALIDATED
priority: CRITICAL
impact: CRITICAL
created_by: "Claude"
created_at: "2026-01-29T18:00:00Z"
updated_at: "2026-01-29T18:30:00Z"
completed_at: "2026-01-29T18:30:00Z"
tags: ["skill-integration", "ts-parser-v2", "orchestration-gap", "critical-gap"]
source: "Live test investigation"
finding_type: GAP
confidence_level: HIGH
validated: true
```

---

<!--
DESIGN RATIONALE:

This discovery documents a critical gap in FEAT-004 where the Python infrastructure
was created but never integrated into the SKILL.md orchestration pipeline.

The gap occurred because:
1. TDD-FEAT-004 was comprehensive (2700+ lines)
2. Enabler decomposition created EN-020..023 for components
3. BUT no enabler captured the integration work specified in TDD Sections 3, 10, 11

The fix requires creating EN-025 with specific tasks to:
1. Transform ts-parser.md to v2.0 (Strategy Pattern orchestrator)
2. Implement CLI transcript namespace (or direct Python invocation)
3. Update SKILL.md to use hybrid pipeline

TRACE:
- DISC-009: Root cause discovery (agent-only limitation)
- DISC-012: TDD CLI specification gap (remediated via FL-001)
- DISC-013: This discovery (implementation gap, NOT specification gap)
- EN-025: Created to address this gap
-->
