# EN-702: Rule File Token Optimization

<!--
TEMPLATE: Enabler
VERSION: 1.0.0
SOURCE: ONTOLOGY-v1.md Section 3.4.9
CREATED: 2026-02-14 (Claude)
PURPOSE: Optimize all .context/rules/*.md files to reduce total token consumption
-->

> **Type:** enabler
> **Status:** pending
> **Priority:** critical
> **Impact:** critical
> **Enabler Type:** infrastructure
> **Created:** 2026-02-14
> **Due:** —
> **Completed:** —
> **Parent:** FEAT-008
> **Owner:** —
> **Effort:** 8

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Summary](#summary) | What this enabler delivers |
| [Problem Statement](#problem-statement) | Why this work is needed |
| [Technical Approach](#technical-approach) | How we'll implement it |
| [Design Source](#design-source) | Traceability to EPIC-002 design artifacts |
| [Children (Tasks)](#children-tasks) | Task breakdown |
| [Acceptance Criteria](#acceptance-criteria) | Definition of done |
| [Related Items](#related-items) | Dependencies and hierarchy |
| [History](#history) | Change log |

---

## Summary

Optimize all 10 `.context/rules/*.md` files to reduce total token consumption from ~30K to ~12.5K tokens. Apply HARD/MEDIUM/SOFT tier vocabulary, add rule IDs (H-01 through H-24), remove redundant phrasing, and consolidate related rules. This is the highest-leverage optimization in the entire enforcement framework, as L1 static context accounts for 82.5% of enforcement tokens and is the only layer vulnerable to context rot.

**Value Proposition:**
- Reduces L1 token consumption by ~51.5%, freeing context window for actual work
- Delays context rot onset by reducing baseline token load
- Introduces rule IDs (H-01 through H-24) enabling traceable compliance references
- Applies HARD/MEDIUM/SOFT enforcement tiers for unambiguous enforcement language
- Tags critical content for L2 re-injection via V-024 context reinforcement
- Preserves all existing semantic enforcement while reducing verbosity

**Technical Scope:**
- All 10 `.context/rules/*.md` files (coding-standards, architecture-standards, testing-standards, file-organization, error-handling-standards, tool-configuration, python-environment, project-workflow, mandatory-skill-usage, markdown-navigation-standards)
- CLAUDE.md root context file
- Token budget: total L1 content must not exceed ~12,500 tokens

---

## Problem Statement

Current rule files consume ~25,700 tokens (12.9% of 200K context window). This is excessive and contributes to context rot. EPIC-002 EN-404 designed an optimization plan to reduce this to ~12,476 tokens (6.2%). Specific issues:

1. **Token budget overrun** -- Current L1 content uses 2x the target token budget, accelerating context rot onset from ~20K tokens into the session.
2. **Verbose explanations** -- Many rules include paragraph-length explanations where a single-sentence HARD rule would be more effective and more resistant to context rot.
3. **Redundant content** -- Multiple rule files repeat the same architectural constraints (e.g., layer boundary rules appear in both coding-standards and architecture-standards).
4. **No enforcement tiers** -- Rules do not distinguish between absolute constraints (HARD), advisory guidance (MEDIUM), and aspirational best practices (SOFT), making it unclear which rules Claude must never violate.
5. **No rule IDs** -- Rules cannot be referenced by identifier, making compliance tracking and L2 re-injection targeting impossible.
6. **No L2 tagging** -- Critical rules are not tagged for V-024 per-prompt re-injection, meaning when L1 degrades due to context rot, the most important rules cannot be selectively reinforced.

---

## Technical Approach

1. **Baseline measurement** -- Measure exact token count for each of the 10 rule files and CLAUDE.md using a consistent tokenizer. Document per-file current state.
2. **Content audit** -- For each file, categorize every rule as HARD, MEDIUM, or SOFT. Identify redundant content across files, verbose explanations that can be compressed, and low-value content that can be removed.
3. **Assign rule IDs** -- Assign unique IDs (H-01 through H-24 for HARD rules) to all HARD-tier rules across all files. MEDIUM and SOFT rules get M-xx and S-xx prefixes respectively.
4. **Consolidate and compress** -- Remove cross-file duplication, replace verbose paragraphs with concise one-sentence rules, merge related rules that can be stated as a single constraint.
5. **Apply tier vocabulary** -- Rewrite all rules using consistent HARD/MEDIUM/SOFT language (MUST/SHALL/NEVER for HARD, SHOULD/RECOMMENDED for MEDIUM, MAY/CONSIDER for SOFT).
6. **Tag for L2 re-injection** -- Mark the highest-priority HARD rules for V-024 per-prompt reinforcement using a consistent tagging scheme.
7. **Reference SSOT** -- Replace inline constant definitions with references to EN-701's quality-enforcement.md SSOT file.
8. **Validate token counts** -- Re-measure all files to confirm total is within ~12,500 token budget.
9. **Run test suite** -- Verify `uv run pytest` passes after optimization to confirm no semantic regressions.
10. **Adversarial review** -- Subject optimized rules to Red Team analysis targeting bypass vectors introduced by compression.

---

## Design Source

| Source | Content Used |
|--------|-------------|
| EPIC-002 EN-404 | Rule optimization design, per-file token targets, enforcement tier language |
| ADR-EPIC002-002 | L1 layer specification, token budget target (~12,476), HARD/MEDIUM/SOFT definitions |
| ADR-EPIC002-002 Section L1 | 82.5% token concentration risk, context rot vulnerability |
| Barrier-1 ADV-to-ENF | Adversarial strategy encoding requirements for rules (S-007, S-003, S-010, S-014, S-002, S-013) |
| EN-701 | Quality enforcement SSOT (constants to reference instead of inline) |

---

## Children (Tasks)

| ID | Title | Status | Activity | Agents |
|----|-------|--------|----------|--------|
| TASK-001 | Baseline token measurement for all 10 rule files and CLAUDE.md | pending | RESEARCH | ps-investigator |
| TASK-002 | Content audit: categorize rules by tier, identify redundancy | pending | RESEARCH | ps-investigator |
| TASK-003 | Assign rule IDs (H-01 through H-24, M-xx, S-xx) | pending | DESIGN | ps-architect |
| TASK-004 | Optimize coding-standards.md and architecture-standards.md | pending | DEVELOPMENT | ps-architect |
| TASK-005 | Optimize testing-standards.md and file-organization.md | pending | DEVELOPMENT | ps-architect |
| TASK-006 | Optimize error-handling-standards.md and tool-configuration.md | pending | DEVELOPMENT | ps-architect |
| TASK-007 | Optimize python-environment.md and project-workflow.md | pending | DEVELOPMENT | ps-architect |
| TASK-008 | Optimize mandatory-skill-usage.md and markdown-navigation-standards.md | pending | DEVELOPMENT | ps-architect |
| TASK-009 | Optimize CLAUDE.md root context | pending | DEVELOPMENT | ps-architect |
| TASK-010 | Validate total token count within budget | pending | TESTING | nse-verification |
| TASK-011 | Run `uv run pytest` to verify no regressions | pending | TESTING | nse-verification |
| TASK-012 | Adversarial review of optimized rules for bypass vectors | pending | TESTING | ps-critic |
| TASK-013 | Creator revision based on review findings | pending | DEVELOPMENT | ps-architect |

### Task Dependencies

```
TASK-001 (baseline) ──> TASK-002 (audit) ──> TASK-003 (rule IDs)
                                                    │
                                    ┌───────────────┼───────────────┐
                                    v               v               v
                              TASK-004/005     TASK-006/007     TASK-008/009
                              (optimize)       (optimize)       (optimize)
                                    │               │               │
                                    └───────┬───────┘───────────────┘
                                            v
                                      TASK-010 (validate tokens)
                                            │
                                            v
                                      TASK-011 (pytest)
                                            │
                                            v
                                      TASK-012 (adversarial review) ──> TASK-013 (revision)
```

- TASK-004 through TASK-009 can execute in parallel after TASK-003
- TASK-010 and TASK-011 require all optimization tasks to complete
- TASK-012 requires TASK-010 and TASK-011 to pass before adversarial review

---

## Acceptance Criteria

| # | Criterion | Verified |
|---|-----------|----------|
| AC-1 | All 10 rule files optimized | [ ] |
| AC-2 | Total token count reduced to <= 12,500 tokens | [ ] |
| AC-3 | HARD tier rules explicitly marked with enforcement language (MUST/SHALL/NEVER) | [ ] |
| AC-4 | MEDIUM tier rules explicitly marked with advisory language (SHOULD/RECOMMENDED) | [ ] |
| AC-5 | Rule IDs (H-01 through H-24) assigned to all HARD rules | [ ] |
| AC-6 | No semantic loss from original rules (all constraints preserved) | [ ] |
| AC-7 | All rules maintain markdown navigation standards (NAV-001 through NAV-006) | [ ] |
| AC-8 | `uv run pytest` still passes after optimization | [ ] |
| AC-9 | Critical rules tagged for L2 re-injection via V-024 | [ ] |
| AC-10 | Inline constants replaced with references to EN-701 SSOT | [ ] |
| AC-11 | Adversarial review completed with no unmitigated bypass vectors | [ ] |

---

## Related Items

### Hierarchy

- **Parent Feature:** [FEAT-008: Quality Framework Implementation](../FEAT-008-quality-framework-implementation.md)

### Dependencies

| Type | Item | Description |
|------|------|-------------|
| depends_on | EN-701 | SSOT must exist before rules can reference it for constants |
| depends_on | EPIC-002 EN-404 | Rule optimization design provides per-file targets and strategy |
| blocks | EN-703 | Hook implementation depends on optimized L1 rules being in place |
| blocks | EN-704 | Session context depends on optimized CLAUDE.md |
| related_to | ADR-EPIC002-002 | Token budget targets and 5-layer architecture specification |
| related_to | Barrier-1 ADV-to-ENF | Adversarial strategy encoding must be preserved during optimization |

---

## History

| Date | Author | Status | Notes |
|------|--------|--------|-------|
| 2026-02-14 | Claude | pending | Enabler created with 13-task decomposition. Highest-leverage optimization in the enforcement framework (82.5% of enforcement tokens in L1). Depends on EN-701 SSOT being available for constant references. |
