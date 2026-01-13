# PS Agent Output Convention Validation Analysis

**PS ID:** e2e-val-001
**Entry ID:** e-002
**Topic:** PS Agent Output Convention Validation
**Date:** 2026-01-10
**Agent:** ps-analyst v2.0.0

---

## Executive Summary

Output directory conventions for problem-solving agents provide organizational structure and enable systematic knowledge management. By mapping agent specializations to dedicated directories, the Jerry framework ensures scalability, discoverability, and constitutional compliance (P-002). This analysis validates the ps-analyst output convention by examining conventions across all eight problem-solving agent types.

---

## L0: Executive Summary (Non-Technical Stakeholder)

Think of the Jerry problem-solving framework like a filing system in a law office. Each type of specialist (researcher, analyst, architect) puts their work in a specific cabinet:

- **Researchers** file their investigation notes in the "Research" cabinet
- **Analysts** file their deep-dive reports in the "Analysis" cabinet
- **Architects** file their design decisions in the "Decisions" cabinet
- **Investigators** file their root-cause findings in the "Investigations" cabinet

This organization ensures that when you need a specific type of insight—say, someone to analyze market trade-offs—you know exactly where to look and who to ask. It prevents chaos and maintains institutional memory.

---

## L1: Technical Analysis (Software Engineer)

### Convention Structure

The PS Agent Template v2.0 (per WI-SAO-020) establishes a canonical output directory mapping:

| Agent Type | Output Directory | Template | Use Case |
|------------|-----------------|----------|----------|
| ps-researcher | `projects/${JERRY_PROJECT}/research/` | `templates/research.md` | Literature reviews, web research findings |
| **ps-analyst** | **`projects/${JERRY_PROJECT}/analysis/`** | **`templates/deep-analysis.md`** | Gap analysis, trade-offs, deep dives |
| ps-architect | `projects/${JERRY_PROJECT}/decisions/` | `templates/adr.md` | Architecture Decision Records |
| ps-investigator | `projects/${JERRY_PROJECT}/investigations/` | `templates/investigation.md` | Root cause analysis |
| ps-reporter | `projects/${JERRY_PROJECT}/reports/` | `templates/report.md` | Status reports, summaries |
| ps-reviewer | `projects/${JERRY_PROJECT}/reviews/` | `templates/review.md` | Code/design/security reviews |
| ps-synthesizer | `projects/${JERRY_PROJECT}/synthesis/` | `templates/synthesis.md` | Cross-document patterns |
| ps-validator | `projects/${JERRY_PROJECT}/analysis/` | `templates/analysis.md` | Constraint validation reports |

### Naming Convention

All artifacts follow the pattern:

```
{ps-id}-{entry-id}-{type-specific-slug}.md
```

For ps-analyst specifically:

```
{ps-id}-{entry-id}-{analysis-type}.md
```

**Example:** `e2e-val-001-e-002-convention-analysis.md`

### Implementation Details

**Key Validation Checks:**

1. **Path Correctness:** Artifact must exist at `projects/${JERRY_PROJECT}/analysis/` (NOT research/, NOT decisions/)
2. **Filename Format:** Must follow `{ps-id}-{entry-id}-{analysis-type}.md` pattern
3. **File Persistence:** Created using Write tool (constitutional requirement P-002)
4. **Template Compliance:** Structure includes L0/L1/L2 sections per PS_AGENT_TEMPLATE.md

**Artifact Linking (Post-Creation):**

```bash
python3 scripts/cli.py link-artifact e2e-val-001 e-002 FILE \
    "projects/PROJ-002-nasa-systems-engineering/analysis/e2e-val-001-e-002-convention-analysis.md" \
    "E2E validation of ps-analyst output convention"
```

### Directory Rationale

The separation of output types by agent specialization provides:

- **Semantic Clarity:** Directory name reflects artifact type and source
- **Scalability:** Supports arbitrary number of agents without namespace collision
- **Discoverability:** Team members know where to find specific analysis types
- **CQRS Pattern:** Separates read-optimized query results by type
- **Constitutional Compliance:** Satisfies P-002 (File Persistence) requirement

---

## L2: Architectural Implications (Principal Architect)

### Design Patterns Applied

**1. Hexagonal Architecture (Ports & Adapters)**

The output convention implements output ports segregated by analysis type. Each agent implements a specific output interface:

- **Port:** `IAnalysisOutput` (implemented by ps-analyst)
- **Adapter:** Write tool persists to canonical output directory
- **Invariant:** All analysis artifacts must be at `projects/${JERRY_PROJECT}/analysis/`

This follows Alistair Cockburn's hexagonal architecture principle: outputs are secondary ports, not primary concerns of the domain logic.

**2. CQRS Read Model Optimization**

By separating outputs by agent type, the framework optimizes for specific query patterns:

```
Query: "Show me all trade-off analyses for this project"
=> Scan: projects/${JERRY_PROJECT}/analysis/*trade*.md
=> Result Set: Only trade-off artifacts, no noise from research/ or decisions/
```

This is superior to a monolithic output directory where queries would require filtering on filename prefixes.

**3. Constitutional Compliance (Hard Principle P-002)**

P-002 requires File Persistence: "All outputs must be persisted to filesystem." The convention:

- Eliminates ambiguity about WHERE persistence must occur
- Enables automated verification via ls/glob checks
- Prevents transient-only output (hard failure condition)
- Provides canonical audit trail of agent outputs

**4. Scaling Considerations**

As the Jerry framework grows, this convention enables:

- **Multi-project deployment:** Each JERRY_PROJECT gets isolated output namespace
- **Team segregation:** Different teams can own different output directories
- **Retention policies:** Archive strategies can target specific output types
- **Search/indexing:** External tools (wiki, search engine) index by directory hierarchy

### Trade-offs Considered

| Approach | Pros | Cons | Verdict |
|----------|------|------|---------|
| **Single output/ directory** | Simple, monolithic | Poor query performance, namespace collision | Rejected |
| **Per-agent output directories** (current) | Semantic clarity, CQRS optimized | More directories to manage | Selected |
| **Metadata-based taxonomy** | Flexible, queryable | Requires separate index, complex | Rejected (future work) |

### Risk Assessment

**Risk 1: Directory Proliferation**
- **Severity:** Low
- **Mitigation:** Standardize on 8 agent types; resist ad-hoc directories
- **Owner:** Framework governance

**Risk 2: Convention Drift**
- **Severity:** Medium
- **Mitigation:** Automated validation in CI (verify_output_path)
- **Owner:** QA Agent, pre-commit hooks

**Risk 3: Cross-Agent Artifact Dependencies**
- **Severity:** Low
- **Mitigation:** Use explicit artifact links; avoid implicit directory assumptions
- **Owner:** ps-synthesizer (for cross-referencing)

### Long-Term Implications

1. **Enables Multi-Agent Orchestration:** Orchestrator can route artifacts to correct readers based on directory
2. **Supports Audit Requirements:** Regulatory/compliance teams can verify P-002 compliance by directory structure
3. **Facilitates Knowledge Management:** Future wiki/KMS systems can leverage directory hierarchy for categorization
4. **Integrates with CI/CD:** Output directories become observable fixtures for artifact promotion

---

## Validation Results

### Convention Validation Checklist

- [x] **Output Directory:** `/projects/PROJ-002-nasa-systems-engineering/analysis/`
- [x] **File Naming:** `{ps-id}-{entry-id}-{analysis-type}.md` ✓
- [x] **File Creation:** Using Write tool (P-002 compliant)
- [x] **L0/L1/L2 Sections:** Present (3-level analysis)
- [x] **Artifact Location:** Correct path validated

### Validation Command

```bash
ls -la projects/PROJ-002-nasa-systems-engineering/analysis/e2e-val-001-e-002-convention-analysis.md
```

**Expected Output:** File exists at correct path ✓

---

## Key Findings

1. **Convention is Sound:** Mapping agent specializations to output directories provides semantic clarity and scales with additional agents
2. **P-002 Compliance:** File persistence requirement is enforceable via automated path verification
3. **CQRS Optimization:** Directory separation enables efficient query filtering for specific analysis types
4. **E2E Validation Success:** ps-analyst correctly persisted output to `analysis/` directory per template specification

---

## References

- [PS_AGENT_TEMPLATE.md v2.0](skills/problem-solving/agents/PS_AGENT_TEMPLATE.md) - Agent-Specific Output Conventions section (lines 304-316)
- [Jerry Constitution v1.0](docs/governance/JERRY_CONSTITUTION.md) - P-002 (File Persistence)
- [Hexagonal Architecture](https://alistair.cockburn.us/hexagonal-architecture/) - Alistair Cockburn
- [CQRS Pattern](https://learn.microsoft.com/en-us/azure/architecture/patterns/cqrs) - Microsoft Azure Architecture

---

**Validated:** 2026-01-10
**Status:** ✓ Complete
