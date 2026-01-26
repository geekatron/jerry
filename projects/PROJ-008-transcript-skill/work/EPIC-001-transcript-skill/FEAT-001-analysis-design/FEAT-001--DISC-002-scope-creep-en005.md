# DISC-002: EN-005 Scope Creep - Implementation Tasks in Design Phase

<!--
TEMPLATE: Discovery
SOURCE: ONTOLOGY-v1.md Section 3.4.8
VERSION: 1.0.0
-->

---

## Frontmatter

```yaml
# === IDENTITY ===
id: "DISC-002"
work_type: DISCOVERY
title: "EN-005 Scope Creep: Implementation Tasks in Design Phase"

# === LIFECYCLE ===
status: RESOLVED
resolution_date: "2026-01-26T14:00:00Z"
resolution: "Option B selected - artifacts relocated to skills/transcript/ per DEC-002 and DISC-004"
severity: HIGH
impact: PROCESS

# === TIMESTAMPS ===
discovered_at: "2026-01-26T12:00:00Z"
discovered_by: "User"

# === HIERARCHY ===
parent_id: "FEAT-001"

# === TAGS ===
tags:
  - "process"
  - "scope-creep"
  - "gate-violation"
```

---

## Discovery Summary

During EN-005 execution, Claude created implementation artifacts (AGENT.md files, SKILL.md) that should have been part of FEAT-002 Implementation, not FEAT-001 Analysis & Design. This bypassed the human review gate (GATE-4) that was intended to approve the design BEFORE implementation began.

---

## L0: What Happened (ELI5)

Imagine you're building a house. The architect should create blueprints (design), then the owner reviews and approves them, THEN construction begins. Instead, Claude created the blueprints AND started building walls before the owner could review the blueprints.

---

## L1: Technical Analysis

### Tasks That Were Misplaced

| Task | What It Created | Should Be In | Actually In |
|------|-----------------|--------------|-------------|
| TASK-001 | TDD-transcript-skill.md | EN-005 (Design) | EN-005 ✓ |
| TASK-002 | TDD-ts-parser.md | EN-005 (Design) | EN-005 ✓ |
| TASK-003 | TDD-ts-extractor.md | EN-005 (Design) | EN-005 ✓ |
| TASK-004 | TDD-ts-formatter.md | EN-005 (Design) | EN-005 ✓ |
| TASK-005 | ts-parser AGENT.md | **FEAT-002** | EN-005 ✗ |
| TASK-006 | ts-extractor AGENT.md | **FEAT-002** | EN-005 ✗ |
| TASK-007 | ts-formatter AGENT.md | **FEAT-002** | EN-005 ✗ |
| TASK-008 | SKILL.md | **FEAT-002** | EN-005 ✗ |
| TASK-009 | PLAYBOOK-en005.md | Debatable | EN-005 |
| TASK-010 | RUNBOOK-en005.md | Debatable | EN-005 |

### Root Cause Analysis (5 Whys)

**Why did implementation tasks end up in EN-005?**
1. Why? → TASK-005 through TASK-008 were created as part of EN-005 task breakdown
2. Why? → The orchestration plan included "AGENT.md creation" as design tasks
3. Why? → Claude conflated "design documentation" with "implementation artifacts"
4. Why? → No clear boundary was established between "specification" and "artifact"
5. Why? → The worktracker templates don't enforce design-vs-implementation boundaries

**Root Cause:** Lack of clear ontological distinction between:
- **Design Specification**: Documents that DESCRIBE what should be built (TDDs)
- **Implementation Artifact**: Files that ARE the built thing (AGENT.md prompts)

### Gate Violation

```
INTENDED FLOW:
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│  EN-005 Design  │────►│    GATE-4       │────►│ FEAT-002 Impl   │
│  (TDD specs)    │     │  Human Review   │     │  (AGENT.md)     │
└─────────────────┘     └─────────────────┘     └─────────────────┘

ACTUAL FLOW:
┌─────────────────────────────────────────┐     ┌─────────────────┐
│  EN-005 Design + Implementation         │────►│    GATE-4       │
│  (TDD specs + AGENT.md + SKILL.md)      │     │  Human Review   │
└─────────────────────────────────────────┘     └─────────────────┘
                                                         │
                                                         ▼
                                            Gate reviews implementation
                                            that should not exist yet
```

---

## L2: Architectural Implications

### Process Debt Incurred

1. **Lost Review Opportunity**: Human could not approve/modify design before implementation
2. **Rework Risk**: If TDD design is rejected, AGENT.md files must be rebuilt
3. **Precedent Risk**: Future phases may repeat this pattern

### Correction Options

| Option | Description | Effort | Risk |
|--------|-------------|--------|------|
| A: Accept | Keep AGENT.md files as-is, document as design artifacts | Low | Sets bad precedent |
| B: Move | Relocate AGENT.md files to FEAT-002, re-gate | Medium | Clean separation |
| C: Rebuild | Delete AGENT.md, recreate in FEAT-002 after GATE-4 | High | Cleanest process |

---

## Impact Assessment

| Dimension | Impact | Notes |
|-----------|--------|-------|
| Schedule | LOW | Work is done, just misplaced |
| Quality | MEDIUM | May have built wrong thing without review |
| Process | HIGH | Gate purpose was undermined |
| Trust | MEDIUM | User expectation of review was not met |

---

## Related Items

- **Decision Needed:** [DEC-002 Design vs Implementation Boundary](./FEAT-001--DEC-002-design-implementation-boundary.md)
- **Parent:** FEAT-001 Analysis & Design
- **Affected:** EN-005, GATE-4, FEAT-002

---

## Resolution

**Status: RESOLVED (2026-01-26)**

**Decision:** Option B selected via DEC-002 - Move artifacts to proper location.

**Actions Taken:**

1. **DEC-002 Confirmed:** User approved relocating implementation artifacts to `skills/transcript/`
2. **DISC-004 Research:** Researched Claude Code best practices for skill/agent file organization
3. **Relocation Complete:** All implementation artifacts moved:
   - `skills/transcript/SKILL.md` - Main skill orchestrator
   - `skills/transcript/agents/ts-parser.md` - Parser agent (flat file per industry standards)
   - `skills/transcript/agents/ts-extractor.md` - Extractor agent
   - `skills/transcript/agents/ts-formatter.md` - Formatter agent
   - `skills/transcript/docs/PLAYBOOK.md` - Execution guide
   - `skills/transcript/docs/RUNBOOK.md` - Troubleshooting guide

4. **Task Files Updated:** TASK-005 through TASK-010 updated with relocation notes
5. **EN-005 Updated:** Added relocation summary section

**Artifacts Remaining in EN-005 (Design Specs):**
- TDD documents (design specifications)
- ps-critic reviews (quality artifacts)
- Task/decision/discovery files (work tracker artifacts)

**Lessons Learned:**
- Clear boundary needed between "design spec" (TDD) and "implementation artifact" (AGENT.md)
- Implementation artifacts belong in `skills/` folder, not work tracker folders
- Future phases should have explicit artifact destination in task definitions

---

*Discovery ID: DISC-002*
*Severity: HIGH*
*Status: RESOLVED*
*Resolution Date: 2026-01-26*
