# Artifact Integrity Investigation Plan

> **Investigation ID:** INV-ARTIFACT-INTEGRITY-001
> **Created:** 2026-01-12
> **Pattern:** Prioritized Deep Parallel (Fan-Out/Fan-In with Barriers)
> **Orchestration Skill:** v2.1.0

---

## Investigation Objective

Verify that all recently created artifacts (WI-SAO-016, 017, 018) and pre-existing agent/skill definitions are **real and integrated**, not **hollow shells** with:
- Unresolved `$ref` references
- Non-existent file paths
- Placeholder tokens in non-template files
- Tool permissions that don't match agent capabilities
- Cross-references that don't resolve

---

## Workflow Architecture

```
                            ┌─────────────────────────────┐
                            │     MAIN CONTEXT            │
                            │   (Conductor/Orchestrator)  │
                            └─────────────┬───────────────┘
                                          │
                    ╔═════════════════════╧═════════════════════╗
                    ║            PHASE 1: PRIORITY TIER          ║
                    ║         (3 Agents - Deep Parallel)         ║
                    ╚═════════════════════╤═════════════════════╝
                                          │
          ┌───────────────────────────────┼───────────────────────────────┐
          │                               │                               │
          ▼                               ▼                               ▼
   ┌──────────────┐               ┌──────────────┐               ┌──────────────┐
   │ ps-validator │               │ps-investigator│               │  qa-engineer │
   │              │               │              │               │              │
   │ INV-001:     │               │ INV-002:     │               │ INV-003:     │
   │ Schema $ref  │               │ File Paths   │               │ Tool Perms   │
   │ Integrity    │               │ Existence    │               │ Alignment    │
   └──────┬───────┘               └──────┬───────┘               └──────┬───────┘
          │                               │                               │
          └───────────────────────────────┼───────────────────────────────┘
                                          │
                    ╔═════════════════════╧═════════════════════╗
                    ║          BARRIER 1: SYNTHESIS              ║
                    ║    Aggregate Phase 1, Identify Patterns    ║
                    ╚═════════════════════╤═════════════════════╝
                                          │
          ┌───────────────────────────────┼───────────────────────────────┐
          │                               │                               │
          ▼                               ▼                               ▼
   ┌──────────────┐               ┌──────────────┐               ┌──────────────┐
   │ps-investigator│               │ ps-validator │               │  qa-engineer │
   │              │               │              │               │              │
   │ INV-004:     │               │ INV-005:     │               │ INV-006:     │
   │ Cross-Artifact│               │ Placeholder  │               │ Capability   │
   │ Consistency  │               │ Detection    │               │ Claims       │
   └──────┬───────┘               └──────┬───────┘               └──────┬───────┘
          │                               │                               │
          └───────────────────────────────┼───────────────────────────────┘
                                          │
                    ╔═════════════════════╧═════════════════════╗
                    ║          BARRIER 2: FINAL SYNTHESIS        ║
                    ║      ps-reporter Creates Final Report      ║
                    ╚═════════════════════════════════════════════╝
```

---

## Phase Definitions

### Phase 1: Priority Tier (Critical Validation)

| ID | Workstream | Agent | Target | Output |
|----|------------|-------|--------|--------|
| INV-001 | Schema Reference Integrity | ps-validator | All `$ref` in YAML contracts | `INV-001-schema-refs.md` |
| INV-002 | File Existence Validation | ps-investigator | All `path:`, `reference:` values | `INV-002-file-existence.md` |
| INV-003 | Tool Permission Alignment | qa-engineer | TOOL_REGISTRY ↔ Agent files | `INV-003-tool-perms.md` |

**Concurrency:** 3 parallel agents
**Duration Target:** ~5 minutes

### Barrier 1: Synthesis Checkpoint

- Aggregate findings from Phase 1
- Identify patterns and connected issues
- Determine if Phase 2 scope needs adjustment

### Phase 2: Deep Dive (Comprehensive Validation)

| ID | Workstream | Agent | Target | Output |
|----|------------|-------|--------|--------|
| INV-004 | Cross-Artifact Consistency | ps-investigator | Contracts ↔ Schemas ↔ Agents | `INV-004-cross-artifact.md` |
| INV-005 | Placeholder Detection | ps-validator | `{PLACEHOLDER}` in non-templates | `INV-005-placeholders.md` |
| INV-006 | Capability Claim Validation | qa-engineer | Agent claims vs implementation | `INV-006-capabilities.md` |

**Concurrency:** 3 parallel agents
**Duration Target:** ~5 minutes

### Barrier 2: Final Synthesis

- ps-reporter creates comprehensive report
- All findings consolidated
- Recommendations for remediation

---

## Artifacts to Investigate

### Recently Created (WI-SAO-016, 017, 018)

| Artifact | Type | Size | Schema Refs? |
|----------|------|------|--------------|
| `TOOL_REGISTRY.yaml` | Registry | 22KB | No |
| `PS_SKILL_CONTRACT.yaml` | Contract | 33KB | Yes (50+) |
| `NSE_SKILL_CONTRACT.yaml` | Contract | 49KB | Yes (60+) |
| `CROSS_SKILL_HANDOFF.yaml` | Contract | 29KB | Yes (20+) |
| `SCHEMA_VERSIONING.md` | Doc | 6KB | N/A |
| `session_context.json` | Schema | 12KB | Yes (10+) |

### Pre-existing (Baseline Validation)

| Category | Count | Pattern |
|----------|-------|---------|
| Core agents | 4 | `.claude/agents/*.md` |
| PS agents | 9 | `skills/problem-solving/agents/*.md` |
| NSE agents | 10 | `skills/nasa-se/agents/*.md` |
| Orch agents | 3 | `skills/orchestration/agents/*.md` |
| **Total** | **26** | |

---

## Validation Criteria

### INV-001: Schema Reference Integrity

```yaml
pass_criteria:
  - Every `$ref: "#/components/schemas/X"` has a matching definition
  - No orphaned schema definitions (defined but never referenced)
  - External refs (`$ref: "file.yaml#/path"`) resolve to existing files
```

### INV-002: File Existence Validation

```yaml
pass_criteria:
  - Every `path:` value resolves to existing file or valid template variable
  - Every `contract_reference:` points to existing file
  - Every `output_location:` uses valid template syntax
```

### INV-003: Tool Permission Alignment

```yaml
pass_criteria:
  - Every agent in TOOL_REGISTRY has corresponding .md file
  - Tool permissions in registry match agent capabilities
  - No tools listed that don't exist in Claude Code
```

### INV-004: Cross-Artifact Consistency

```yaml
pass_criteria:
  - Agent counts match across: TOOL_REGISTRY, Contracts, AGENTS.md
  - Version numbers consistent across related documents
  - Schema versions match between schema files and references
```

### INV-005: Placeholder Detection

```yaml
pass_criteria:
  - No `{PLACEHOLDER}` tokens in non-template files
  - Template files clearly marked with `.template.` or `TEMPLATE`
  - All `${VAR}` variables are documented environment variables
```

### INV-006: Capability Claim Validation

```yaml
pass_criteria:
  - Agents claiming "creates X" actually have output patterns for X
  - Agents claiming "validates Y" have validation logic described
  - No aspirational claims without implementation
```

---

## Output Structure

```
validation/artifact-integrity/
├── INVESTIGATION_PLAN.md          # This file
├── phase-1/
│   ├── INV-001-schema-refs.md     # ps-validator output
│   ├── INV-002-file-existence.md  # ps-investigator output
│   └── INV-003-tool-perms.md      # qa-engineer output
├── barrier-1-synthesis.md         # Phase 1 aggregation
├── phase-2/
│   ├── INV-004-cross-artifact.md  # ps-investigator output
│   ├── INV-005-placeholders.md    # ps-validator output
│   └── INV-006-capabilities.md    # qa-engineer output
└── ARTIFACT-INTEGRITY-REPORT.md   # Final synthesis
```

---

## Execution Protocol

1. **Pre-flight:** Verify all target artifacts exist
2. **Phase 1:** Launch 3 parallel agents (INV-001, 002, 003)
3. **Barrier 1:** Wait for all Phase 1 agents, synthesize
4. **Phase 2:** Launch 3 parallel agents (INV-004, 005, 006)
5. **Barrier 2:** Wait for all Phase 2 agents, synthesize
6. **Report:** ps-reporter creates final report
7. **Update:** Update WORKTRACKER with findings

---

*Plan Version: 1.0*
*Created: 2026-01-12*
*Investigation ID: INV-ARTIFACT-INTEGRITY-001*
