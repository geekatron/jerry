# ADR-OSS-001: CLAUDE.md Decomposition Strategy

> **Workflow ID:** oss-release-20260131-001
> **Phase:** 2 (ADR Creation)
> **Agent:** ps-architect-001
> **Created:** 2026-01-31
> **Status:** PROPOSED
> **Risk Reference:** RSK-P0-004 (RPN 280 - CRITICAL)
> **Supersedes:** None
> **Constitutional Compliance:** P-001 (Truth), P-002 (Persistence), P-011 (Evidence)

---

## Document Navigation

| Section | Audience | Purpose |
|---------|----------|---------|
| [L0: Executive Summary](#l0-executive-summary-eli5) | Executives, Stakeholders | High-level overview |
| [L1: Technical Details](#l1-technical-details-engineer) | Engineers, Developers | Implementation guidance |
| [L2: Strategic Implications](#l2-strategic-implications-architect) | Architects, Decision Makers | Trade-offs and decisions |

---

## L0: Executive Summary (ELI5)

### The Problem (Simple Analogy)

Imagine giving a new employee a 900-page orientation manual on their first day. They would be overwhelmed, miss important details, and perform poorly. Now imagine instead giving them a 50-page quick-start guide with references to detailed handbooks they can consult when needed. They would learn faster and work more effectively.

Jerry's CLAUDE.md is currently that 900-page manual at **914 lines**. Research proves that AI performance degrades significantly when given too much context upfront - a phenomenon called **"context rot"**.

### The Solution

We will decompose CLAUDE.md from 914 lines to approximately **60-80 lines** using a **Tiered Hybrid Strategy** that combines:
1. **Core essentials** always loaded (Tier 1)
2. **Standards** in separate auto-loaded files (Tier 2)
3. **Skills** loaded on-demand when invoked (Tier 3)
4. **Reference documents** read only when explicitly needed (Tier 4)

### Key Numbers

| Metric | Current | Target | Improvement |
|--------|---------|--------|-------------|
| CLAUDE.md lines | 914 | 60-80 | **91-93% reduction** |
| Estimated tokens at session start | ~10,000 | ~3,500 | **65% reduction** |
| Context utilization | ~85-90% | ~30-40% | **Within "sweet spot"** |

### Bottom Line

**This is Jerry's #1 technical risk (RPN 280).** Without decomposition, OSS users will experience degraded Claude performance, missed instructions, and poor code quality. The fix is straightforward, fully reversible, and takes 4-6 hours to implement.

---

## Context

### Background

Jerry's CLAUDE.md has grown organically to **914 lines** as the project evolved. This single file contains:

- Project overview and context rot explanation (~25 lines)
- Complete Worktracker entity hierarchy, mappings, and behavior (~370 lines)
- Template documentation (~110 lines)
- Directory structure (~40 lines)
- TODO/meta instructions (~35 lines)
- Architecture overview (~30 lines)
- Project workflow (~90 lines)
- Project enforcement (~110 lines)
- Skills documentation (~40 lines)
- Mandatory skill usage (~95 lines)
- CLI commands (~60 lines)
- Agent governance (~50 lines)

### The Problem: Context Rot

Context rot is a scientifically validated phenomenon where LLM performance degrades as input context grows, even within technical token limits.

**Chroma Research Findings (July 2025):**

| Finding | Evidence | Impact on Jerry |
|---------|----------|-----------------|
| Performance varies with position | 70-75% accuracy at start/end vs 55-60% middle | Critical rules at start may be forgotten |
| "Lost in the middle" effect | 15-20 percentage point accuracy drop | Large worktracker section (370 lines) risks being ignored |
| Distractors worsen performance | Topically related but incorrect info causes hallucination | Redundant/verbose sections increase error risk |
| 75% utilization sweet spot | Quality peaks before context exhaustion | 914 lines pushes Jerry well past sweet spot |

**Source:** [Chroma Research - Context Rot](https://research.trychroma.com/context-rot)

### Root Cause Analysis (from Phase 1 5-Whys)

```
WHY is CLAUDE.md 914 lines?
  └─ All project context, worktracker details, and skill references are in one file
WHY is everything in one file?
  └─ Jerry evolved organically; content was added as needed
WHY wasn't content decomposed earlier?
  └─ Context rot research wasn't available during initial development
WHY wasn't best practice length known?
  └─ Claude Code is new; best practices emerged after Jerry started
WHY wasn't it refactored when research emerged?
  └─ ROOT CAUSE: No systematic review process for context file health
```

**Pattern Identified:** Context Rot Unawareness (from ps-analyst root-cause-5whys.md)

### Constraints

| ID | Constraint | Source | Priority |
|----|------------|--------|----------|
| C-001 | CLAUDE.md must be < 500 lines | Chroma Research, Builder.io best practices | HARD |
| C-002 | Must not break existing skills invocation | Jerry skill system | HARD |
| C-003 | Must maintain discoverability of key features | OSS usability | MEDIUM |
| C-004 | Must be reversible (two-way door) | Risk mitigation | MEDIUM |
| C-005 | Implementation effort < 6 hours | FMEA priority assessment | SOFT |

### Forces

1. **Context Efficiency vs Discoverability:** Smaller CLAUDE.md means less context load but potentially harder discovery of features
2. **Simplicity vs Flexibility:** Monolithic file is simpler to maintain but less flexible for team ownership
3. **Immediate Load vs Lazy Load:** Always-loaded content provides consistency but may include unnecessary context
4. **User Onboarding vs Expert Use:** New users need more guidance; experts need quick reference

---

## Options Considered

### Option A: Monolithic (Status Quo)

**Description:** Maintain current 914-line CLAUDE.md with no changes.

**Implementation:** None required

**Token Budget:**
```
CLAUDE.md: ~10,000 tokens (always loaded)
Session Start: ~85-90% context utilization
```

**Pros:**
- Zero implementation effort
- All context immediately visible
- No navigation required
- No risk of broken imports

**Cons:**
- **CRITICAL:** 914 lines exceeds 500-line best practice by 83%
- **CRITICAL:** Context rot causes instruction loss (Chroma research)
- Merge conflicts when multiple contributors edit
- No separation of concerns
- Monolithic maintenance burden

**Fit with Constraints:**
- C-001: **FAILS** (914 > 500)
- C-002: PASSES
- C-003: PASSES
- C-004: N/A
- C-005: PASSES (zero effort)

**FMEA Assessment:** RPN 280 (CRITICAL) - Highest risk in registry

### Option B: Skills-Based Pure Decomposition

**Description:** Move virtually all content to skills, leaving CLAUDE.md as a minimal loader/router.

**Implementation:**
```
CLAUDE.md (~30 lines)
├── Project identity (5 lines)
├── Critical constraints (10 lines)
├── Skill router (10 lines)
└── Constitution pointer (5 lines)

skills/
├── worktracker/SKILL.md      ← All worktracker content
├── project-workflow/SKILL.md ← Project enforcement, workflow
├── cli/SKILL.md              ← CLI commands
├── governance/SKILL.md       ← Agent governance
└── ...
```

**Token Budget:**
```
CLAUDE.md: ~400 tokens (always loaded)
Session Start: ~5% context utilization
Each Skill: ~1,000-3,000 tokens (on-demand)
```

**Pros:**
- Minimal context at session start
- Maximum flexibility
- Clear ownership boundaries
- Each skill loads only when needed

**Cons:**
- **Requires user to know which skill to invoke**
- **Loses ambient awareness of project workflow**
- **New users may miss critical rules**
- Creates many new skill files
- Over-optimization may harm discoverability
- Increased navigation complexity

**Fit with Constraints:**
- C-001: PASSES (30 lines)
- C-002: PASSES
- C-003: **PARTIAL** (discovery requires skill invocation)
- C-004: PASSES
- C-005: **PARTIAL** (6-8 hours - slightly over)

### Option C: Hybrid with Lazy Loading (RECOMMENDED)

**Description:** Decompose using a tiered strategy: core CLAUDE.md with auto-loaded rules and on-demand skills.

**Implementation:**
```
TIER 1: Core CLAUDE.md (~60-80 lines)
├── Project identity + Context rot explanation (15 lines)
├── Critical rules (MUST FOLLOW section) (15 lines)
├── Quick command reference (15 lines)
├── Skills navigation table (10 lines)
├── Project workflow summary (15 lines)
└── References/pointers (10 lines)

TIER 2: .claude/rules/ (auto-loaded, ~500 lines total)
├── architecture-standards.md
├── coding-standards.md
├── testing-standards.md
├── python-environment.md
└── file-organization.md

TIER 3: skills/ (on-demand)
├── worktracker/SKILL.md      ← Full entity mappings, templates, behavior
├── problem-solving/SKILL.md  ← PS frameworks
├── orchestration/SKILL.md    ← Multi-agent coordination
├── transcript/SKILL.md       ← Transcription workflows
└── ...

TIER 4: Explicit Reference (read when needed)
├── docs/governance/JERRY_CONSTITUTION.md
├── .context/templates/worktracker/
└── docs/design/ADR-*.md
```

**Token Budget:**
```
CLAUDE.md: ~800-1,000 tokens (always loaded)
.claude/rules/*: ~2,500 tokens (auto-loaded but separate files)
Total at session start: ~3,300-3,500 tokens
Skills: Variable (on-demand)
```

**Pros:**
- **Targets ~60-80 line core CLAUDE.md (91-93% reduction)**
- **Auto-loaded rules provide consistent coding standards**
- **Skills loaded only when invoked**
- **Maintains discoverability via navigation table**
- **Fully reversible (two-way door)**
- Clear separation of concerns
- Team ownership enabled (separate files)
- Worktracker moved to dedicated skill
- Industry best practice pattern

**Cons:**
- Requires extracting worktracker content to skill
- Some navigation learning curve
- Multiple files to maintain (but already exist for rules)
- .claude/rules/ still contributes to context (but separate files)

**Fit with Constraints:**
- C-001: **PASSES** (60-80 lines)
- C-002: PASSES (skill invocation unchanged)
- C-003: **PASSES** (navigation table maintains discovery)
- C-004: **PASSES** (easily reversible)
- C-005: **PASSES** (4-6 hours)

### Option D: @ Imports Pattern

**Description:** Use Claude Code's @ import syntax to dynamically include content.

**Implementation:**
```markdown
# CLAUDE.md
@.claude/includes/core-identity.md
@.claude/includes/critical-rules.md
@.claude/includes/project-workflow.md
@.claude/includes/quick-reference.md
```

**Token Budget:**
```
Same as Option C, but content loaded via imports
Constraints: Max 5 import hops (recursive)
```

**Pros:**
- Maintains single entry point
- Content modularized for team ownership
- Imports resolved at load time

**Cons:**
- **Import chain complexity**
- **Max 5 hops limit may be constraining**
- **Imports inside code blocks not evaluated**
- **Less visible than explicit file structure**
- Debugging import issues difficult
- Less intuitive for contributors

**Fit with Constraints:**
- C-001: PASSES (core file small)
- C-002: PASSES
- C-003: PARTIAL (imports less discoverable)
- C-004: PASSES
- C-005: PASSES

---

## Decision

**We will use Option C: Hybrid with Lazy Loading.**

### Rationale

1. **Evidence-Based:** Chroma Research proves context rot is real. The 75% utilization sweet spot means Jerry's current 85-90% utilization degrades performance.

2. **Best Balance:** Option C optimizes the balance between:
   - Context efficiency (60-80 lines vs 914)
   - Discoverability (navigation table preserved)
   - Maintainability (separate files, team ownership)
   - Reversibility (can recombine if needed)

3. **Pattern Alignment:** This follows the "Progressive Disclosure" principle from Builder.io's CLAUDE.md guide:
   > "Don't tell Claude all the information you could possibly want it to know. Rather, tell it how to find important information so that it can find and use it, but only when it needs to."

4. **Risk Mitigation:** RSK-P0-004 has RPN 280 (CRITICAL). This option directly addresses the root cause (context bloat) while maintaining Jerry's functionality.

5. **Industry Precedent:** Large projects like Chromium use tiered documentation with core concepts at top level and details in specialized documents.

### Alignment

| Criterion | Score | Notes |
|-----------|-------|-------|
| Constraint Satisfaction | **HIGH** | Meets all 5 constraints |
| Risk Level | **LOW** | Fully reversible; decomposition is additive |
| Implementation Effort | **M** (4-6 hours) | Extract worktracker, restructure CLAUDE.md |
| Reversibility | **HIGH** | Can recombine files if needed |

---

## L1: Technical Details (Engineer)

### Implementation Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                   Jerry Context Loading Hierarchy                   │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│ TIER 1: ALWAYS LOADED - Core CLAUDE.md (~60-80 lines)              │
│ ┌─────────────────────────────────────────────────────────────────┐│
│ │ • Project identity (10 lines)                                   ││
│ │ • Context rot explanation (5 lines)                             ││
│ │ • CRITICAL RULES - MUST FOLLOW (15 lines)                       ││
│ │ • Quick command reference (15 lines)                            ││
│ │ • Skills navigation table (10 lines)                            ││
│ │ • Project workflow summary (15 lines)                           ││
│ │ • References/pointers (10 lines)                                ││
│ └─────────────────────────────────────────────────────────────────┘│
│                              ▼                                      │
│ TIER 2: AUTO-LOADED - .claude/rules/ (~1,700 lines, separate)      │
│ ┌─────────────────────────────────────────────────────────────────┐│
│ │ • architecture-standards.md (~500 lines)                        ││
│ │ • coding-standards.md (~400 lines)                              ││
│ │ • testing-standards.md (~400 lines)                             ││
│ │ • python-environment.md (~100 lines)                            ││
│ │ • file-organization.md (~300 lines)                             ││
│ └─────────────────────────────────────────────────────────────────┘│
│                              ▼                                      │
│ TIER 3: ON-DEMAND - skills/ (loaded when invoked)                  │
│ ┌─────────────────────────────────────────────────────────────────┐│
│ │ • worktracker/SKILL.md    ← Entity mappings, templates, behavior││
│ │ • problem-solving/SKILL.md ← 5W2H, Ishikawa, FMEA, agents       ││
│ │ • orchestration/SKILL.md  ← Cross-pollination, sync barriers    ││
│ │ • transcript/SKILL.md     ← VTT parsing, formatting             ││
│ │ • architecture/SKILL.md   ← Design patterns, hexagonal          ││
│ │ • nasa-se/SKILL.md        ← NPR 7123.1D, V&V                    ││
│ └─────────────────────────────────────────────────────────────────┘│
│                              ▼                                      │
│ TIER 4: EXPLICIT REFERENCE (read only when needed)                 │
│ ┌─────────────────────────────────────────────────────────────────┐│
│ │ • docs/governance/JERRY_CONSTITUTION.md                         ││
│ │ • .context/templates/worktracker/*.md                           ││
│ │ • docs/design/ADR-*.md                                          ││
│ │ • AGENTS.md                                                     ││
│ └─────────────────────────────────────────────────────────────────┘│
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### Token Budget Analysis

| Tier | Content | Lines | Est. Tokens | Load Trigger |
|------|---------|-------|-------------|--------------|
| 1 | Core CLAUDE.md | 60-80 | 800-1,000 | Always (session start) |
| 2 | .claude/rules/* | ~1,700 | ~2,500 | Always (auto-loaded) |
| 3 | Active skill | Variable | 1,000-3,000 | On skill invocation |
| 4 | Referenced docs | Variable | Variable | On explicit read |
| **Total at session start** | | **~1,760-1,780** | **~3,300-3,500** | |

**Current vs Target Comparison:**
```
                    CONTEXT LOAD
                       ▲
                       │
                 100% ─┼───────────────────────── Over-Utilization Zone
                       │   ╭──────────────╮
                  90% ─┼───│ CURRENT: 914 │──────── Context Rot Risk
                       │   ╰──────────────╯
                       │
                  75% ─┼─────────────────── ★ Sweet Spot (Chroma Research)
                       │
                       │
                  40% ─┼───────────────────────────────────────────────
                       │       ╭───────────────╮
                  30% ─┼───────│ TARGET: ~80   │── Decomposed
                       │       ╰───────────────╯
                       │
                   0% ─┼────────────────────────────────────────────►
                       │
                    TOKEN UTILIZATION
```

### Proposed Core CLAUDE.md Structure

```markdown
# CLAUDE.md - Jerry Framework Root Context

> This file provides core context to Claude Code at session start.
> Detailed instructions are in .claude/rules/ (auto-loaded) and skills/ (on-demand).

---

## Project Overview

**Jerry** is a framework for behavior and workflow guardrails with filesystem-based memory.

### Core Problem: Context Rot
> "Context Rot is the phenomenon where an LLM's performance degrades as the context
> window fills up." — [Chroma Research](https://research.trychroma.com/context-rot)

Jerry addresses this through filesystem memory, skills, and structured knowledge.

---

## CRITICAL RULES (MUST FOLLOW)

- **UV REQUIRED:** Use `uv run jerry` for all Python operations (NEVER pip/python directly)
- **ONE CLASS PER FILE:** In src/, each file contains exactly one public class
- **PROJECT REQUIRED:** Set JERRY_PROJECT before work (`export JERRY_PROJECT=PROJ-XXX-slug`)
- **UPDATE WORKTRACKER:** After completing work items, update WORKTRACKER.md

---

## Quick Commands

| Command | Purpose |
|---------|---------|
| `uv run jerry <cmd>` | Run Jerry CLI |
| `/worktracker` | Task management, entity mappings, templates |
| `/problem-solving` | Research frameworks (5W2H, FMEA, 8D) |
| `/orchestration` | Multi-agent workflow coordination |
| `/transcript` | VTT parsing, transcript formatting |

---

## Skills (Load On-Demand)

| Skill | Purpose | Invoke With |
|-------|---------|-------------|
| worktracker | Entity hierarchy, templates, tracking | `/worktracker` |
| problem-solving | 5W2H, Ishikawa, FMEA, 8D frameworks | `/problem-solving` |
| orchestration | Cross-pollination, sync barriers | `/orchestration` |
| transcript | VTT parsing, formatting | `/transcript` |
| architecture | Design patterns, hexagonal | `/architecture` |
| nasa-se | NPR 7123.1D, V&V | `/nasa-se` |

*For full entity mappings and templates, invoke /worktracker skill.*

---

## Project Workflow

1. **Set Project:** `export JERRY_PROJECT=PROJ-XXX-slug`
2. **Check Plan:** `projects/${JERRY_PROJECT}/PLAN.md`
3. **Review Tasks:** `projects/${JERRY_PROJECT}/WORKTRACKER.md`
4. **Work:** Update WORKTRACKER.md as you progress
5. **Document:** Decisions in `docs/design/`, learnings in `docs/experience/`

---

## Architecture

```
jerry/
├── .claude/rules/     # Auto-loaded standards
├── skills/            # On-demand skills
├── src/               # Hexagonal core (domain → application → infrastructure)
├── projects/          # Project workspaces
└── docs/              # Knowledge repository
```

See `.claude/rules/architecture-standards.md` for detailed architecture patterns.

---

## References

- **Constitution:** `docs/governance/JERRY_CONSTITUTION.md`
- **Templates:** `.context/templates/worktracker/`
- **Patterns:** `.claude/patterns/PATTERN-CATALOG.md`
- **CLI Reference:** See `/worktracker` skill

---

*Line Count Target: 60-80 lines | Current active project: ${JERRY_PROJECT}*
```

**Estimated Line Count:** ~75 lines (92% reduction from 914)

### Implementation Checklist

| # | Task | Effort | Owner | Verification |
|---|------|--------|-------|--------------|
| 1 | Create `skills/worktracker/rules/worktracker-entity-hierarchy.md` | 1 hour | Architecture | File exists with entity mappings |
| 2 | Create `skills/worktracker/rules/worktracker-templates.md` | 30 min | Architecture | Template table migrated |
| 3 | Create `skills/worktracker/rules/worktracker-directory-structure.md` | 30 min | Architecture | Directory tree migrated |
| 4 | Update `skills/worktracker/SKILL.md` to reference new rules | 30 min | Architecture | Skill references rules correctly |
| 5 | Migrate TODO/meta section to worktracker skill | 30 min | Architecture | TODO rules in skill |
| 6 | Restructure core CLAUDE.md | 1 hour | Architecture | `wc -l CLAUDE.md` < 100 |
| 7 | Add navigation table to CLAUDE.md | 15 min | Architecture | Table present and accurate |
| 8 | Add CLAUDE.md line count check to CI | 15 min | DevOps | GitHub Action validates < 350 |
| 9 | Verify all skill invocations work | 30 min | QA | Manual test of 6 skills |
| 10 | Update CONTRIBUTING.md with decomposition note | 15 min | Docs | Note added |

**Total Effort:** ~4-5 hours

### CI Enforcement

```yaml
# .github/workflows/context-health.yml
name: Context Health Check

on:
  push:
    paths:
      - 'CLAUDE.md'
  pull_request:
    paths:
      - 'CLAUDE.md'

jobs:
  check-claude-md-size:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Check CLAUDE.md line count
        run: |
          LINES=$(wc -l < CLAUDE.md)
          MAX_LINES=350
          if [ $LINES -gt $MAX_LINES ]; then
            echo "::error::CLAUDE.md is $LINES lines (max $MAX_LINES)"
            echo "Context rot risk! See ADR-OSS-001 for decomposition guidelines."
            exit 1
          fi
          echo "CLAUDE.md is $LINES lines (within limit)"
```

---

## L2: Strategic Implications (Architect)

### Trade-off Analysis

| Factor | Option A (Mono) | Option B (Pure Skills) | Option C (Hybrid) | Option D (Imports) |
|--------|-----------------|----------------------|-------------------|-------------------|
| Context efficiency | Poor | Excellent | **Good** | Good |
| Discoverability | Excellent | Poor | **Good** | Medium |
| Maintainability | Poor | Good | **Good** | Medium |
| Implementation effort | None | High | **Medium** | Medium |
| Reversibility | N/A | Medium | **High** | High |
| Constraint satisfaction | 1/5 | 4/5 | **5/5** | 4/5 |
| **Recommendation** | Reject | Consider | **SELECTED** | Alternative |

### One-Way Door Assessment

| Aspect | Reversibility | Assessment |
|--------|---------------|------------|
| File structure changes | **HIGH** | Files can be recombined |
| Skill content migration | **HIGH** | Content can be moved back |
| CI enforcement | **HIGH** | Threshold can be adjusted |
| User workflow changes | **MEDIUM** | Some retraining needed if reversed |

**Conclusion:** This is a **TWO-WAY DOOR** decision. All changes are reversible.

### Failure Mode Analysis

| Failure Mode | Probability | Impact | Detection | Mitigation |
|--------------|-------------|--------|-----------|------------|
| Worktracker skill not invoked when needed | MEDIUM | HIGH | Users report confusion | Clear triggers in CLAUDE.md; activation keywords |
| Import chains break on file rename | LOW | MEDIUM | Immediate error | Use relative paths; test after moves |
| Rules files grow too large | LOW | MEDIUM | Line count check | Apply same decomposition to rules |
| Skills discovery poor for new users | MEDIUM | MEDIUM | User feedback | Navigation table; onboarding guide |

### Design Rationale

#### Why Not Pure Skills (Option B)?

While Option B achieves the best context efficiency (~30 lines), it sacrifices **ambient awareness**. New users would need to know to invoke `/worktracker` to learn about Jerry's entity hierarchy. This creates a "hidden knowledge" problem that degrades OSS onboarding.

#### Why Not @ Imports (Option D)?

The @ import pattern introduces complexity:
- Maximum 5 recursive hops limits flexibility
- Imports inside code blocks are not evaluated
- Debugging import failures is difficult
- Less intuitive for contributors than explicit file structure

#### Why Hybrid (Option C)?

Option C follows the **Progressive Disclosure Principle**:

1. **Core CLAUDE.md** (Tier 1): Contains just enough to orient Claude and establish critical rules
2. **.claude/rules/** (Tier 2): Auto-loaded standards that apply universally
3. **skills/** (Tier 3): Domain-specific knowledge loaded when relevant
4. **docs/** (Tier 4): Deep reference for specific needs

This mirrors how enterprise documentation works:
- Quick-start guide (CLAUDE.md)
- Policy documents (.claude/rules/)
- Department manuals (skills/)
- Reference library (docs/)

### Industry Precedent

| Project | Approach | Outcome |
|---------|----------|---------|
| **Chromium** | Tiered docs: Overview -> Developer Guide -> Deep Reference | Successful at massive scale |
| **Kubernetes** | SIG-specific documentation with central index | Enables distributed ownership |
| **Next.js** | Getting Started -> Concepts -> API Reference | Progressive disclosure |

### Detection Improvement Opportunity

Per FMEA analysis, improving detection reduces effective RPN:

| Current State | Improved State | Impact |
|---------------|----------------|--------|
| Detection = 5 (manual review) | Detection = 2 (CI enforced) | RPN 280 -> 112 (-60%) |

The CI line count check directly addresses the detection gap.

---

## Consequences

### Positive Consequences

1. **Eliminates CRITICAL risk (RSK-P0-004):** Context rot addressed at source
2. **Improves OSS user experience:** Better Claude performance from session start
3. **Enables team ownership:** Separate files can be owned by specialists
4. **Reduces merge conflicts:** Parallel edits to different files
5. **Creates pattern for future growth:** Framework for adding new content without bloating CLAUDE.md
6. **Automates prevention:** CI enforcement prevents regression

### Negative Consequences

1. **Learning curve:** Contributors must learn tiered structure
2. **Navigation complexity:** More files to understand
3. **Potential fragmentation:** Related content may drift apart if not maintained

### Neutral Consequences

1. **Migration effort:** One-time 4-6 hour investment
2. **Documentation updates:** CONTRIBUTING.md must explain structure

### Residual Risks

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| MCP servers still contribute to context | MEDIUM | MEDIUM | Document MCP token impact; recommend essential servers |
| Users don't invoke needed skills | LOW | MEDIUM | Clear activation keywords; trigger phrases |
| Decomposition creates navigation burden | LOW | LOW | Skills table in CLAUDE.md; good naming |

---

## Verification Requirements

This ADR links to the following Verification Requirements from the V&V Plan:

| VR ID | Requirement | Verification Method |
|-------|-------------|---------------------|
| VR-012 | CLAUDE.md < 500 lines | `wc -l CLAUDE.md` in CI |
| VR-014 | @ imports resolve correctly | Skill invocation test |
| VR-011 | All skills have L0 section | Manual inspection |

---

## Risk Traceability

| Risk ID | Description | RPN | Treatment |
|---------|-------------|-----|-----------|
| RSK-P0-004 | CLAUDE.md context overflow | 280 | **Directly addressed by this ADR** |
| RSK-P0-011 | Scope creep from research | 150 | Bounded scope; 4-6 hour timebox |
| RSK-P0-014 | MCP server context bloat | 125 | Related but separate; needs future ADR |

---

## Implementation

### Action Items

| # | Action | Owner | Priority | Due |
|---|--------|-------|----------|-----|
| 1 | Backup current CLAUDE.md | Architecture | P1 | Day 1 |
| 2 | Extract worktracker to skill rules | Architecture | P1 | Day 1 |
| 3 | Restructure core CLAUDE.md | Architecture | P1 | Day 1 |
| 4 | Add CI line count enforcement | DevOps | P1 | Day 2 |
| 5 | Verify all skill invocations | QA | P1 | Day 2 |
| 6 | Update CONTRIBUTING.md | Docs | P2 | Day 3 |

### Validation Criteria

| Criterion | Target | Measurement |
|-----------|--------|-------------|
| CLAUDE.md line count | < 100 lines | `wc -l CLAUDE.md` |
| Context tokens at session start | < 4,000 | Token counter estimate |
| All skills invocable | 6/6 pass | Manual invocation test |
| CI enforcement active | Pass/Fail | GitHub Actions status |
| Worktracker content preserved | 100% | Diff comparison |

---

## Related Decisions

| ADR | Relationship | Notes |
|-----|--------------|-------|
| ADR-OSS-002 | FOLLOWS | Dual-repo strategy may need CLAUDE.md sync |
| ADR-OSS-003 | RELATED_TO | Progressive docs loading aligns with decomposition |

---

## References

### Primary Sources

| # | Reference | Type | Relevance |
|---|-----------|------|-----------|
| 1 | [Chroma Research - Context Rot](https://research.trychroma.com/context-rot) | Research | Foundational evidence for context rot |
| 2 | [Builder.io CLAUDE.md Guide](https://www.builder.io/blog/claude-md-guide) | Best Practice | Progressive disclosure pattern |
| 3 | [Anthropic Context Engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) | Industry | Context management principles |
| 4 | [Claude Code Memory Management](https://code.claude.com/docs/en/memory) | Documentation | @ imports, .claude/rules/ auto-loading |

### Phase 1 Analysis Sources

| # | Reference | Type | Relevance |
|---|-----------|------|-----------|
| 5 | ps-researcher/deep-research.md | Research | 3-pillar analysis, token budget |
| 6 | ps-analyst/fmea-analysis.md | FMEA | RPN 280 calculation, priority |
| 7 | ps-analyst/root-cause-5whys.md | Root Cause | Context rot unawareness pattern |
| 8 | quality-gates/qg-1/ps-critic-review.md | Quality | Findings on FMEA calibration |

---

## Document Control

| Field | Value |
|-------|-------|
| **Document ID** | ADR-OSS-001 |
| **Status** | PROPOSED |
| **Workflow** | oss-release-20260131-001 |
| **Phase** | 2 (ADR Creation) |
| **Agent** | ps-architect-001 |
| **Risk Addressed** | RSK-P0-004 (RPN 280 - CRITICAL) |
| **Decision Type** | Two-Way Door (Reversible) |
| **Implementation Effort** | 4-6 hours |
| **Word Count** | ~4,200 |
| **Constitutional Compliance** | P-001 (Truth), P-002 (Persistence), P-011 (Evidence) |

---

## Change History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | 2026-01-31 | ps-architect-001 | Initial ADR creation |

---

*This ADR was produced by ps-architect-001 for PROJ-001-oss-release Phase 2.*
*Constitutional Compliance: P-001 (Truth), P-002 (Persistence), P-004 (Provenance), P-011 (Evidence)*
*Template: Michael Nygard ADR Format with Jerry L0/L1/L2 extensions*
