# DEC-002: Design vs Implementation Boundary

<!--
TEMPLATE: Decision
SOURCE: ONTOLOGY-v1.md Section 3.4.7
VERSION: 1.0.0
-->

---

## Frontmatter

```yaml
# === IDENTITY ===
id: "DEC-002"
work_type: DECISION
title: "Design vs Implementation Boundary for Transcript Skill"

# === LIFECYCLE ===
status: CONFIRMED
decision_type: ARCHITECTURAL

# === TIMESTAMPS ===
proposed_at: "2026-01-26T12:00:00Z"
proposed_by: "Claude"

# === HIERARCHY ===
parent_id: "FEAT-001"

# === TAGS ===
tags:
  - "process"
  - "boundary"
  - "gate"
```

---

## Decision Context

### Background

DISC-002 identified that TASK-005 through TASK-008 created implementation artifacts (AGENT.md files, SKILL.md) within EN-005 Design Documentation. This raised the question: **What artifacts belong in design phase vs implementation phase?**

### Question

**Where is the boundary between "design documentation" and "implementation artifacts" for prompt-based agents?**

---

## L0: Simple Explanation

Think of building a house:
- **Design Phase**: Blueprints, specifications, material lists
- **Implementation Phase**: Actually building the walls, installing plumbing

For prompt-based agents:
- **Design Phase**: TDDs describing what the agent should do
- **Implementation Phase**: The actual AGENT.md prompt that runs

---

## L1: Technical Analysis

### The Core Question

For prompt-based agents (no code), what constitutes "implementation"?

| Artifact Type | Contains | Executable? | Phase |
|---------------|----------|-------------|-------|
| TDD | Architecture, data contracts, behavior spec | No | Design |
| AGENT.md | Actual prompt that runs in Claude Code | **Yes** | **Implementation** |
| SKILL.md | Orchestration prompt | **Yes** | **Implementation** |
| PLAYBOOK | Execution procedures | No | Design (operational) |
| RUNBOOK | Troubleshooting procedures | No | Design (operational) |

### Key Insight

**AGENT.md files ARE the implementation** for prompt-based agents. They are not "documentation of agents" - they ARE the agents. The prompt IS the code.

```
Traditional Software:
  Design: UML diagrams, API specs
  Implementation: .py, .js, .go files

Prompt-Based Agents:
  Design: TDD documents, behavior specs
  Implementation: AGENT.md prompts
```

---

## L2: Architectural Decision

### Decision Options

| Option | Description | Pros | Cons |
|--------|-------------|------|------|
| **A** | Keep AGENT.md in EN-005 as "design artifacts" | No rework | Conflates design/implementation |
| **B** | Move AGENT.md to FEAT-002, but accept current files | Clean separation | Files already created |
| **C** | Delete AGENT.md, recreate in FEAT-002 after GATE-4 | Cleanest process | Rework |
| **D** | Define AGENT.md as "executable specification" in design | Semantic clarification | May not satisfy process intent |

### Recommendation

**Option B: Move AGENT.md to FEAT-002**

Rationale:
1. Establishes correct ontological boundary going forward
2. Preserves work already done (no rework)
3. Requires human to explicitly approve before "accepting" the implementation
4. Documents the precedent for future projects

---

## Decision Tree

```
                    ┌─────────────────────────────────┐
                    │ Is the artifact executable?     │
                    └──────────────┬──────────────────┘
                                   │
                    ┌──────────────┴──────────────┐
                    │                             │
                    ▼                             ▼
            ┌──────────────┐              ┌──────────────┐
            │     YES      │              │      NO      │
            │ AGENT.md     │              │ TDD, PLAYBOOK│
            │ SKILL.md     │              │ RUNBOOK      │
            └──────┬───────┘              └──────┬───────┘
                   │                             │
                   ▼                             ▼
            ┌──────────────┐              ┌──────────────┐
            │IMPLEMENTATION│              │    DESIGN    │
            │  (FEAT-002)  │              │  (FEAT-001)  │
            └──────────────┘              └──────────────┘
```

---

## Proposed Boundary Definition

### FEAT-001 (Analysis & Design) Artifacts

| Artifact Type | Purpose | Gate |
|---------------|---------|------|
| Requirements Specification | What the system must do | GATE-2 |
| ADRs | Key architectural decisions | GATE-3 |
| TDD Documents | Technical specifications | GATE-4 |
| PLAYBOOK | Execution procedures | GATE-4 |
| RUNBOOK | Troubleshooting procedures | GATE-4 |

### FEAT-002 (Implementation) Artifacts

| Artifact Type | Purpose | Gate |
|---------------|---------|------|
| AGENT.md files | Executable agent prompts | GATE-5 |
| SKILL.md | Executable orchestrator | GATE-5 |
| Test transcripts | Validation inputs | GATE-5 |
| Integration tests | Validation evidence | GATE-6 |

---

## Impact of Decision

### If Option B Accepted

1. **Relocate files**: Move `agents/*/AGENT.md` and `SKILL.md` from EN-005 to EN-007/EN-008/EN-009 in FEAT-002
2. **Update EN-005**: Remove TASK-005 through TASK-008 from EN-005 scope
3. **Update FEAT-002**: Add enablers for agent implementation
4. **GATE-4 Scope**: Review TDDs, PLAYBOOK, RUNBOOK only (not AGENT.md)

### Files to Relocate

```
FROM: EN-005-design-documentation/
  agents/ts-parser/AGENT.md      → FEAT-002/EN-007-ts-parser-impl/
  agents/ts-extractor/AGENT.md   → FEAT-002/EN-008-ts-extractor-impl/
  agents/ts-formatter/AGENT.md   → FEAT-002/EN-009-ts-formatter-impl/
  SKILL.md                       → FEAT-002/EN-010-skill-impl/
```

---

## Questions for Human

1. **Do you agree that AGENT.md files are "implementation" not "design"?**
2. **Should we relocate the files (Option B) or accept them as-is (Option A)?**
3. **What should GATE-4 review scope be?**
   - Option A: All 10 artifacts (including AGENT.md)
   - Option B: Only TDDs + PLAYBOOK + RUNBOOK (6 artifacts)

---

## File Organization Decision

Based on research documented in **[DISC-004](./FEAT-001--DISC-004-skill-file-organization.md)**:

### Industry Standard Confirmed

**Option A: Flat files** is the correct pattern per:
- Claude Code Official Documentation
- Anthropic Engineering Best Practices
- Jerry Framework Existing Conventions

### Target Structure

```
skills/
└── transcript/
    ├── SKILL.md              # Entry point orchestrator
    ├── agents/
    │   ├── ts-parser.md      # Flat file (NOT ts-parser/AGENT.md)
    │   ├── ts-extractor.md   # Flat file
    │   └── ts-formatter.md   # Flat file
    └── docs/
        ├── PLAYBOOK.md       # Execution guide
        └── RUNBOOK.md        # Troubleshooting guide
```

---

## Human Decisions (Confirmed)

| Question | Decision | Date |
|----------|----------|------|
| Are AGENT.md files implementation? | **YES** - Move to `skills/` | 2026-01-26 |
| File naming pattern? | **Option A: Flat files** (e.g., `ts-parser.md`) | 2026-01-26 |
| GATE-4 scope? | **Option B: TDDs + ops docs only** | 2026-01-26 |
| Update acceptance criteria? | **YES** - With evidence | 2026-01-26 |
| Execution order? | EN-005 cleanup → EN-006 → FEAT-002 | 2026-01-26 |

---

## Related Items

- **Discovery:** [DISC-002 Scope Creep](./FEAT-001--DISC-002-scope-creep-en005.md)
- **Discovery:** [DISC-004 File Organization](./FEAT-001--DISC-004-skill-file-organization.md)
- **Affected:** EN-005, GATE-4, FEAT-002

---

*Decision ID: DEC-002*
*Status: CONFIRMED*
*Human Decision Recorded: 2026-01-26*
