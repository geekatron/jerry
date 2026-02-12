# ADR-OSS-003: Work Tracker Extraction Strategy

> **Workflow ID:** oss-release-20260131-001
> **Phase:** 2 (ADR Creation)
> **Agent:** ps-architect-003
> **Created:** 2026-01-31
> **Status:** PROPOSED
> **Risk Reference:** RSK-P1-001 (RPN 80 - MEDIUM), RSK-P0-004 (RPN 280 - CRITICAL)
> **Supersedes:** None
> **Depends On:** ADR-OSS-001 (CLAUDE.md Decomposition Strategy)
> **Constitutional Compliance:** P-001 (Truth), P-002 (Persistence), P-011 (Evidence), P-022 (No Deception)

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

Imagine a company's entire employee handbook is embedded in the CEO's welcome letter. Every time a new employee joins, they receive a 50-page "welcome letter" that covers everything from vacation policies to expense procedures to IT security guidelines. This is overwhelming and ineffective.

Now imagine extracting all those policies into separate department handbooks, with the welcome letter simply pointing employees to the right handbook for each topic. The welcome letter becomes crisp and actionable, while detailed policies remain accessible when needed.

Jerry's CLAUDE.md currently has **371 lines** (lines 27-397) of worktracker content embedded directly in it. This represents **40% of the total file** (371 of 914 lines). The worktracker content includes:

- Complete entity hierarchy (78 lines)
- Classification and property matrices (36 lines)
- System mapping tables (88 lines - ADO, SAFe, JIRA)
- Behavioral rules (23 lines)
- Template documentation (57 lines)
- Directory structure examples (89 lines)

This content belongs in the worktracker **skill**, not in the root context file.

### The Solution

We will extract the worktracker content from CLAUDE.md and consolidate it into the `skills/worktracker/` skill, which already has partial rules files. The extraction will:

1. **Remove** 371 lines from CLAUDE.md (40% reduction)
2. **Consolidate** content into existing worktracker skill rules files
3. **Add** a simple pointer in CLAUDE.md: "For worktracker details, invoke `/worktracker`"
4. **Fix** the critical SKILL.md metadata bug (copy-paste error from transcript skill)

### Key Numbers

| Metric | Current | After Extraction | Improvement |
|--------|---------|------------------|-------------|
| CLAUDE.md worktracker lines | 371 | 3-5 (pointer only) | **99% reduction** |
| CLAUDE.md total lines | 914 | ~545 | **40% reduction** |
| Worktracker skill completeness | 32 lines (stub) | ~600 lines (comprehensive) | **Full skill** |
| Skill metadata bug | Present | Fixed | **Risk eliminated** |

### Bottom Line

This extraction is a **prerequisite for ADR-OSS-001** (CLAUDE.md decomposition). Worktracker content represents the single largest extractable section (40%). Without this extraction, CLAUDE.md cannot reach the 60-80 line target. The extraction also resolves RSK-P1-001 (worktracker skill incompleteness) identified during Phase 1 investigation.

---

## Context

### Background

The worktracker system is Jerry's core work tracking mechanism, providing:
- Entity hierarchy mapping (Initiative → Epic → Feature → Story → Task)
- Cross-system mappings (ADO Scrum, SAFe, JIRA)
- Template references for each entity type
- Directory structure conventions

This content accumulated in CLAUDE.md because:
1. Worktracker was critical to every session (needed for context)
2. The skill system matured later in Jerry's development
3. No extraction review was performed as content grew

### Current State Analysis

**CLAUDE.md Worktracker Content (Lines 27-401):**

| Section | Lines | Content |
|---------|-------|---------|
| Entity Hierarchy Tree | 31-78 | ASCII tree showing WorkItem → StrategicItem → ... |
| Hierarchy Levels Table | 80-92 | L0-L5 mapping with owners |
| Classification Matrix | 97-112 | Entity properties (Container, Atomic, Quality Gates) |
| Containment Rules | 114-128 | Parent-child relationships |
| System Mapping Summary | 131-159 | ADO/SAFe/JIRA basic mappings |
| Complete Entity Mapping | 162-177 | Detailed cross-system mapping with Native column |
| ADO Scrum Types | 180-190 | ADO → Canonical mapping |
| SAFe Types | 191-204 | SAFe → Canonical mapping |
| JIRA Types | 205-215 | JIRA → Canonical mapping |
| Worktracker Behavior | 218-241 | Behavioral rules and MCP usage |
| Template Documentation | 244-356 | Two sections (duplicated) with template tables |
| Directory Structure | 360-399 | Full project directory tree |
| **TOTAL** | **~371 lines** | **40% of CLAUDE.md** |

**Worktracker Skill Current State:**

```
skills/worktracker/
├── SKILL.md (32 lines)              ← Stub with WRONG description
└── rules/
    ├── worktracker-entity-rules.md (190 lines)      ← Partial duplicate
    ├── worktracker-folder-structure-and-hierarchy-rules.md
    └── worktracker-template-usage-rules.md
```

**Critical Bug (RSK-P1-001):**
```yaml
# Current SKILL.md metadata (WRONG)
description: Parse, extract, and format transcripts (VTT, SRT, plain text)...
```
This description is copy-pasted from the transcript skill and is completely incorrect.

### Problem Investigation Reference

From `ps-investigator/problem-investigation.md`:

> **Finding: PARTIALLY CONFIRMED - MEDIUM SEVERITY**
>
> The worktracker skill has:
> - **CRITICAL BUG:** Description says "transcripts" instead of "work items"
> - **MISSING:** examples.md file referenced but doesn't exist
> - **INCOMPLETE:** SKILL.md is a stub (32 lines) pointing to rules files
> - **FUNCTIONAL:** Rules files are comprehensive (190+ lines each)

### Constraints

| ID | Constraint | Source | Priority |
|----|------------|--------|----------|
| C-001 | CLAUDE.md must be < 500 lines after all decomposition | ADR-OSS-001 | HARD |
| C-002 | Must not break existing worktracker usage | Jerry behavior | HARD |
| C-003 | Existing rules files must be preserved/enhanced | DRY principle | MEDIUM |
| C-004 | Skill invocation must provide equivalent information | Usability | MEDIUM |
| C-005 | No content loss during extraction | Data integrity | HARD |
| C-006 | Implementation effort < 3 hours | Timeline constraint | SOFT |

### Forces

1. **Consolidation vs Duplication:** CLAUDE.md and worktracker rules already have overlapping content
2. **Skill Load Overhead vs Embedded Convenience:** Skills add one invocation step
3. **DRY vs Discoverability:** Single source of truth vs always-visible content
4. **Immediate Access vs Context Efficiency:** Worktracker rules needed frequently but not always

---

## Options Considered

### Option A: Keep Worktracker in CLAUDE.md (Status Quo)

**Description:** Maintain the current 371 lines of worktracker content in CLAUDE.md.

**Implementation:** None required

**Token Budget:**
```
Worktracker in CLAUDE.md: ~4,000 tokens (always loaded)
Session Start: Contributes to ~85-90% context utilization
```

**Pros:**
- Zero implementation effort
- Worktracker always immediately available
- No skill invocation required

**Cons:**
- **CRITICAL:** 371 lines (40%) blocks ADR-OSS-001 target
- **CRITICAL:** Contributes to context rot (Chroma Research)
- **MEDIUM:** Content duplicated with rules files (DRY violation)
- **MEDIUM:** RSK-P1-001 remains unfixed
- Worktracker content loaded even when not needed (waste)

**Fit with Constraints:**
- C-001: **FAILS** (cannot reach < 500 lines)
- C-002: PASSES
- C-003: FAILS (duplication preserved)
- C-004: N/A
- C-005: PASSES
- C-006: PASSES (zero effort)

**Risk Impact:** RSK-P0-004 remains CRITICAL (RPN 280)

### Option B: Complete Extraction to Skill (RECOMMENDED)

**Description:** Extract all worktracker content from CLAUDE.md to the worktracker skill, consolidating with existing rules files.

**Implementation:**
```
CLAUDE.md (~545 lines after extraction)
├── Single worktracker pointer (3-5 lines):
│   "For work tracking details, invoke `/worktracker`.
│    Skill provides: entity hierarchy, system mappings,
│    templates, directory structure."

skills/worktracker/
├── SKILL.md (~150 lines)                    ← Enhanced with overview, activation
│   ├── Metadata (correct description)
│   ├── Quick Reference Table
│   ├── Agent Definitions (if needed)
│   └── Rule File References
├── rules/
│   ├── worktracker-entity-rules.md (~200 lines)    ← Consolidated
│   │   ├── Entity Hierarchy Tree
│   │   ├── Hierarchy Levels
│   │   ├── Classification Matrix
│   │   └── Containment Rules
│   ├── worktracker-system-mappings.md (~150 lines) ← NEW
│   │   ├── ADO Scrum Mapping
│   │   ├── SAFe Mapping
│   │   └── JIRA Mapping
│   ├── worktracker-behavior-rules.md (~50 lines)   ← NEW
│   │   └── MCP usage, update patterns
│   ├── worktracker-template-usage-rules.md (~100 lines) ← Exists
│   └── worktracker-folder-structure-and-hierarchy-rules.md ← Exists
└── examples.md (~50 lines)                  ← NEW (resolves missing file)
```

**Token Budget:**
```
CLAUDE.md pointer: ~50 tokens (always loaded)
Skill when invoked: ~3,000 tokens (on-demand)
Net Session Start Savings: ~3,950 tokens (99% of worktracker contribution)
```

**Pros:**
- **Enables ADR-OSS-001:** Removes 371 lines (40% reduction)
- **Fixes RSK-P1-001:** Corrects metadata bug
- **Eliminates duplication:** Single source of truth
- **Context efficient:** Loads only when needed
- **Creates complete skill:** examples.md added
- **Maintains discoverability:** Navigation table in CLAUDE.md includes worktracker

**Cons:**
- Requires explicit skill invocation for details
- Migration effort (2-3 hours)
- Users must learn skill pattern

**Fit with Constraints:**
- C-001: **PASSES** (enables < 500 line target)
- C-002: PASSES (skill provides same information)
- C-003: **PASSES** (consolidates, removes duplicates)
- C-004: **PASSES** (equivalent or better)
- C-005: **PASSES** (all content preserved in skill)
- C-006: **PASSES** (2-3 hours)

**Risk Impact:** RSK-P0-004 reduced; RSK-P1-001 CLOSED

### Option C: Hybrid - Keep Summary, Extract Details

**Description:** Keep a condensed 30-40 line summary in CLAUDE.md, extract detailed mappings to skill.

**Implementation:**
```
CLAUDE.md
├── Worktracker Summary (30-40 lines)
│   ├── Simplified hierarchy tree (10 lines)
│   ├── Quick entity table (15 lines)
│   └── "See /worktracker for full mappings" (5 lines)

skills/worktracker/
├── Full details as in Option B
```

**Token Budget:**
```
CLAUDE.md worktracker: ~400 tokens (always loaded)
Skill when invoked: ~2,500 tokens (on-demand)
Net Session Start Savings: ~3,600 tokens (90% reduction)
```

**Pros:**
- Maintains some worktracker visibility in CLAUDE.md
- Still achieves significant reduction (90%)
- Lower cognitive shift for existing users

**Cons:**
- Still contributes ~400 tokens to session start
- May not be enough reduction for ADR-OSS-001 target
- Creates ambiguity: what's in CLAUDE.md vs skill?
- Still has some duplication (summary mirrors skill)

**Fit with Constraints:**
- C-001: **PARTIAL** (may not reach < 100 lines with other content)
- C-002: PASSES
- C-003: PARTIAL (some duplication remains)
- C-004: PASSES
- C-005: PASSES
- C-006: PASSES (2-3 hours)

### Option D: Inline via @ Import

**Description:** Use Claude Code's @ import mechanism to include worktracker content.

**Implementation:**
```markdown
# CLAUDE.md
...
## Worktracker
@skills/worktracker/rules/worktracker-entity-rules.md
@skills/worktracker/rules/worktracker-system-mappings.md
```

**Token Budget:**
```
Same as embedding, but from different files
Still ~4,000 tokens (imports resolved at load)
No reduction in context load
```

**Pros:**
- Modular file structure
- Content in skill location
- Single edit point

**Cons:**
- **CRITICAL:** No context reduction (imports resolve at load)
- **CRITICAL:** Doesn't address context rot
- Uses import hop budget (max 5)
- Imports in code blocks not evaluated

**Fit with Constraints:**
- C-001: **FAILS** (no reduction achieved)
- C-002: PASSES
- C-003: PASSES
- C-004: PASSES
- C-005: PASSES
- C-006: PASSES

---

## Decision

**We will use Option B: Complete Extraction to Skill.**

### Rationale

1. **Prerequisite for ADR-OSS-001:** The CLAUDE.md decomposition strategy targets 60-80 lines. Worktracker content at 371 lines represents the largest single extractable section. Without this extraction, ADR-OSS-001 is blocked.

2. **Dual Risk Resolution:** This decision addresses two risks simultaneously:
   - **RSK-P0-004 (RPN 280 - CRITICAL):** Reduces CLAUDE.md by 40%
   - **RSK-P1-001 (RPN 80 - MEDIUM):** Fixes skill metadata bug, creates examples.md

3. **DRY Principle:** Current state has worktracker content in CLAUDE.md AND in `worktracker-entity-rules.md`. Complete extraction eliminates this duplication.

4. **Skill Pattern Consistency:** Other skills (transcript, problem-solving, orchestration) follow the pattern of comprehensive SKILL.md with supporting rules. Worktracker should follow the same pattern.

5. **Context Efficiency:** Per Chroma Research, loading worktracker content for every session when it's only needed for specific tasks contributes to context rot. On-demand loading is the correct pattern.

### Alignment

| Criterion | Score | Notes |
|-----------|-------|-------|
| Constraint Satisfaction | **HIGH** | Meets all 6 constraints |
| Risk Level | **LOW** | Content preserved; fully reversible |
| Implementation Effort | **M** (2-3 hours) | Extract, consolidate, fix metadata |
| Reversibility | **HIGH** | Can copy back to CLAUDE.md if needed |

---

## L1: Technical Details (Engineer)

### Implementation Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    Worktracker Extraction Architecture                       │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  BEFORE EXTRACTION                                                          │
│  ═══════════════════════════════════════════════════════════════════════   │
│                                                                             │
│  CLAUDE.md (914 lines)                                                      │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │ Lines 1-26    │ Project Overview, Context Rot                        │  │
│  ├───────────────┼──────────────────────────────────────────────────────┤  │
│  │ Lines 27-401  │ <worktracker> BLOCK (371 lines) ◄──────────────────┐ │  │
│  │               │   • Entity Hierarchy (78 lines)                    │ │  │
│  │               │   • Classification Matrix (36 lines)               │ │  │
│  │               │   • System Mappings (88 lines)                     │ │  │
│  │               │   • Behavior Rules (23 lines)                      │ │  │
│  │               │   • Templates (57 lines)                           │ │  │
│  │               │   • Directory Structure (89 lines)                 │ │  │
│  ├───────────────┼──────────────────────────────────────────────────┬─┤  │
│  │ Lines 402-914 │ TODO, Architecture, Workflow, Skills, CLI, etc.  │ │  │
│  └──────────────────────────────────────────────────────────────────┴─┘  │
│                                                                     │      │
│  skills/worktracker/                                                │      │
│  ┌────────────────────────────────────────────┐                    │      │
│  │ SKILL.md (32 lines - BROKEN)               │◄───────────────────┘      │
│  │   Description: "transcripts" (WRONG!)      │  Duplication               │
│  │   References examples.md (MISSING!)        │                            │
│  ├────────────────────────────────────────────┤                            │
│  │ rules/                                     │                            │
│  │   worktracker-entity-rules.md (190 lines)  │◄─ Partial overlap          │
│  │   worktracker-folder-structure-*.md        │                            │
│  │   worktracker-template-usage-*.md          │                            │
│  └────────────────────────────────────────────┘                            │
│                                                                             │
│  AFTER EXTRACTION                                                           │
│  ═══════════════════════════════════════════════════════════════════════   │
│                                                                             │
│  CLAUDE.md (~545 lines)                                                     │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │ Lines 1-26    │ Project Overview, Context Rot                        │  │
│  ├───────────────┼──────────────────────────────────────────────────────┤  │
│  │ Lines 27-30   │ Worktracker Pointer:                                 │  │
│  │               │   "For work tracking: invoke /worktracker            │  │
│  │               │    Provides: entity hierarchy, system mappings,      │  │
│  │               │    templates, directory structure."                  │  │
│  ├───────────────┼──────────────────────────────────────────────────────┤  │
│  │ Lines 31-545  │ TODO, Architecture, Workflow, Skills, CLI, etc.      │  │
│  │               │ (minus 371 lines of worktracker content)             │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
│                                                                             │
│  skills/worktracker/ (COMPLETE)                                             │
│  ┌────────────────────────────────────────────────────────────────────────┐│
│  │ SKILL.md (~150 lines)                                                  ││
│  │   ✓ Correct description: "Work tracking and entity management"        ││
│  │   ✓ Quick reference table                                             ││
│  │   ✓ Activation keywords (correct)                                     ││
│  │   ✓ Rule file references                                              ││
│  ├────────────────────────────────────────────────────────────────────────┤│
│  │ rules/                                                                 ││
│  │   ✓ worktracker-entity-rules.md (~200 lines)  ← Consolidated          ││
│  │   ✓ worktracker-system-mappings.md (~150 lines) ← NEW from CLAUDE.md  ││
│  │   ✓ worktracker-behavior-rules.md (~50 lines) ← NEW from CLAUDE.md    ││
│  │   ✓ worktracker-template-usage-rules.md (~100 lines)                  ││
│  │   ✓ worktracker-folder-structure-and-hierarchy-rules.md               ││
│  ├────────────────────────────────────────────────────────────────────────┤│
│  │ examples/                                                              ││
│  │   ✓ examples.md (~50 lines) ← NEW (creates the missing file)          ││
│  └────────────────────────────────────────────────────────────────────────┘│
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### File Changes Detail

#### 1. CLAUDE.md Changes

**Remove (Lines 27-401):**
```markdown
## Worktracker

<worktracker>
... (entire 371-line block)
</worktracker>
```

**Replace With (3-5 lines):**
```markdown
## Worktracker

For work tracking details, invoke `/worktracker`. The skill provides:
- Entity hierarchy (Initiative → Epic → Feature → Story → Task)
- System mappings (ADO Scrum, SAFe, JIRA)
- Templates for all work item types
- Directory structure conventions

See `skills/worktracker/SKILL.md` for complete documentation.
```

#### 2. SKILL.md Corrections

**Before (WRONG):**
```yaml
name: worktracker
description: Parse, extract, and format transcripts (VTT, SRT, plain text)...
```

**After (CORRECT):**
```yaml
name: worktracker
description: Manage work items using Jerry's entity hierarchy (Initiative → Epic → Feature → Story → Task). Maps to ADO Scrum, SAFe, and JIRA. Provides templates and directory structure conventions.
version: "1.1.0"
allowed-tools: Read, Write, Glob, Task, Edit
activation-keywords:
  - "work tracker"
  - "worktracker"
  - "work-tracker"
  - "update the work tracker"
  - "work items"
  - "entity hierarchy"
  - "WORKTRACKER.md"
  - "/worktracker"
  - "/jerry:worktracker"
```

#### 3. New Rule Files

**worktracker-system-mappings.md (~150 lines):**
Consolidated from CLAUDE.md sections 3 and 4, containing:
- Entity Mapping Table (ADO, SAFe, JIRA columns)
- Mapping Complexity table
- Complete Entity Mapping with Native column
- System-specific type mappings (ADO, SAFe, JIRA subsections)

**worktracker-behavior-rules.md (~50 lines):**
Extracted from CLAUDE.md lines 218-241, containing:
- Canonical model usage statement
- WORKTRACKER.md global manifest behavior
- Folder creation patterns
- MCP Memory-Keeper integration guidance

#### 4. New Examples File

**examples.md (~50 lines):**
Creates the missing file referenced in SKILL.md:
- Creating a new Epic with Features
- Tracking Tasks within an Enabler
- Mapping ADO work items to canonical model
- Updating WORKTRACKER.md after completion

### Content Mapping Matrix

| CLAUDE.md Section | Lines | Target Location | Action |
|-------------------|-------|-----------------|--------|
| Entity Hierarchy Tree | 31-78 | worktracker-entity-rules.md | Merge with existing |
| Hierarchy Levels | 80-92 | worktracker-entity-rules.md | Merge with existing |
| Classification Matrix | 97-112 | worktracker-entity-rules.md | Merge with existing |
| Containment Rules | 114-128 | worktracker-entity-rules.md | Merge with existing |
| System Mapping Summary | 131-159 | worktracker-system-mappings.md | NEW file |
| Complete Entity Mapping | 162-177 | worktracker-system-mappings.md | NEW file |
| ADO/SAFe/JIRA Types | 180-215 | worktracker-system-mappings.md | NEW file |
| Worktracker Behavior | 218-241 | worktracker-behavior-rules.md | NEW file |
| Template Documentation | 244-356 | worktracker-template-usage-rules.md | Already exists, verify |
| Directory Structure | 360-399 | worktracker-folder-structure-*.md | Already exists, verify |

### Implementation Checklist

| # | Task | Effort | Verification |
|---|------|--------|--------------|
| 1 | Fix SKILL.md metadata (description, version, keywords) | 15 min | Read SKILL.md, verify description |
| 2 | Create worktracker-system-mappings.md from CLAUDE.md 131-215 | 30 min | File exists, content complete |
| 3 | Create worktracker-behavior-rules.md from CLAUDE.md 218-241 | 15 min | File exists, content complete |
| 4 | Merge CLAUDE.md entity content with worktracker-entity-rules.md | 30 min | No duplicates, all content present |
| 5 | Verify worktracker-template-usage-rules.md complete | 15 min | Compare with CLAUDE.md 244-302 |
| 6 | Verify worktracker-folder-structure-*.md complete | 15 min | Compare with CLAUDE.md 360-399 |
| 7 | Create examples.md with usage patterns | 30 min | File exists, examples valid |
| 8 | Update SKILL.md with comprehensive content and rule references | 30 min | SKILL.md > 100 lines |
| 9 | Replace CLAUDE.md worktracker block with pointer | 15 min | Block removed, pointer added |
| 10 | Verify skill invocation works | 15 min | `/worktracker` loads correctly |
| 11 | Run `wc -l CLAUDE.md` - verify reduction | 5 min | < 600 lines |

**Total Effort:** 2-3 hours

### Skill Invocation Pattern

After extraction, worktracker usage follows the standard skill pattern:

```
User: "How do I create a new Feature?"

Claude (if worktracker not loaded):
1. Recognizes activation keyword "Feature"
2. Invokes /worktracker skill
3. Reads worktracker-entity-rules.md
4. Provides Feature creation guidance

Claude (if worktracker already loaded):
1. References already-loaded skill content
2. Provides guidance immediately
```

### Integration with TODO Rules

The TODO section in CLAUDE.md (lines 405-438) contains worktracker-related META TODO items. These remain in CLAUDE.md as they govern overall behavior, not worktracker specifics:

```markdown
Keep a META TODO item (MUST ALWAYS BE ON LIST) reminding you to update the respective work tracker `*.md` files.
```

This pointer is appropriate in CLAUDE.md; it references worktracker without duplicating worktracker content.

---

## L2: Strategic Implications (Architect)

### Trade-off Analysis

| Factor | Option A (Keep) | Option B (Extract) | Option C (Hybrid) | Option D (Import) |
|--------|-----------------|-------------------|-------------------|-------------------|
| Context efficiency | Poor | **Excellent** | Good | Poor |
| ADR-OSS-001 enablement | **BLOCKS** | **ENABLES** | Partial | BLOCKS |
| RSK-P1-001 resolution | No | **Yes** | Partial | No |
| DRY compliance | Poor | **Excellent** | Medium | Medium |
| Implementation effort | None | Medium | Medium | Low |
| Reversibility | N/A | **High** | High | High |
| **Recommendation** | Reject | **SELECTED** | Consider | Reject |

### One-Way Door Assessment

| Aspect | Reversibility | Assessment |
|--------|---------------|------------|
| Content extraction | **HIGH** | Content can be copied back to CLAUDE.md |
| SKILL.md enhancement | **HIGH** | Metadata can be reverted |
| New rules files | **HIGH** | Files can be deleted |
| Pointer in CLAUDE.md | **HIGH** | Pointer can be replaced with full content |

**Conclusion:** This is a **TWO-WAY DOOR** decision. All changes are reversible within 30 minutes.

### Failure Mode Analysis

| Failure Mode | Probability | Impact | Detection | Mitigation |
|--------------|-------------|--------|-----------|------------|
| Skill not invoked when needed | LOW | MEDIUM | User feedback | Clear activation keywords; worktracker in skills table |
| Content loss during extraction | LOW | HIGH | Diff review | Content mapping matrix; verification checklist |
| Duplicate content after migration | MEDIUM | LOW | Code review | Delete originals only after verification |
| Missing file references | LOW | MEDIUM | Skill invocation test | Test all rule file references |

### Dependency Chain

```
ADR-OSS-003 (This ADR)
    │
    ├─► Enables ADR-OSS-001 (CLAUDE.md Decomposition)
    │       │
    │       └─► Target: 60-80 lines
    │           └─► Impossible without worktracker extraction
    │
    ├─► Closes RSK-P1-001 (Worktracker metadata bug)
    │
    └─► Reduces RSK-P0-004 (CLAUDE.md bloat)
            └─► 40% reduction from this extraction alone
```

### Industry Pattern Alignment

The extraction follows the **Progressive Disclosure** pattern documented in Builder.io's CLAUDE.md guide:

> "Don't tell Claude all the information you could possibly want it to know. Rather, tell it how to find important information so that it can find and use it, but only when it needs to."

Jerry's skill system is designed precisely for this pattern. Worktracker content should follow the same on-demand loading pattern as:
- `/problem-solving` - Loaded for research/analysis tasks
- `/orchestration` - Loaded for multi-agent workflows
- `/transcript` - Loaded for VTT processing

### Pareto Analysis (80/20)

The worktracker extraction delivers outsized value:

| Investment | Return |
|------------|--------|
| 2-3 hours effort | 40% CLAUDE.md reduction |
| 1 ADR | 2 risks addressed (RSK-P0-004, RSK-P1-001) |
| 4 new/modified files | Complete skill instead of stub |

This is the highest-leverage extraction in the CLAUDE.md decomposition effort.

---

## Consequences

### Positive Consequences

1. **Unblocks ADR-OSS-001:** Primary blocker (40% of content) removed
2. **Closes RSK-P1-001:** Skill metadata bug fixed, examples.md created
3. **Reduces RSK-P0-004:** Significant progress toward CLAUDE.md target
4. **Eliminates duplication:** Single source of truth for worktracker
5. **Creates complete skill:** Worktracker skill becomes comprehensive
6. **Improves context efficiency:** ~3,950 tokens saved at session start

### Negative Consequences

1. **Skill invocation required:** Users must invoke `/worktracker` for details
2. **Learning curve:** Users accustomed to inline content may need adjustment
3. **Migration effort:** 2-3 hours of extraction work required

### Neutral Consequences

1. **Documentation updates:** CONTRIBUTING.md should note skill pattern
2. **Verification needed:** Post-extraction testing required

### Residual Risks

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Users don't know to invoke skill | LOW | MEDIUM | Skills table in CLAUDE.md; clear activation keywords |
| Content drift between CLAUDE.md pointer and skill | LOW | LOW | Pointer is generic; doesn't duplicate specifics |
| New users miss worktracker entirely | LOW | MEDIUM | Onboarding documentation; README references |

---

## Verification Requirements

This ADR links to the following Verification Requirements from the V&V Plan:

| VR ID | Requirement | Verification Method |
|-------|-------------|---------------------|
| VR-011 | All skills have L0 section | Manual inspection of SKILL.md |
| VR-012 | CLAUDE.md < 500 lines | `wc -l CLAUDE.md` in CI |
| VR-016 | Worktracker skill invocable | `/worktracker` invocation test |
| VR-017 | Worktracker skill complete | Content comparison with CLAUDE.md original |

---

## Risk Traceability

| Risk ID | Description | RPN | Treatment |
|---------|-------------|-----|-----------|
| RSK-P0-004 | CLAUDE.md context overflow | 280 | **Directly addressed** - 40% reduction |
| RSK-P1-001 | Worktracker skill metadata error | 80 | **CLOSED by this ADR** |
| RSK-P0-016 | Skills graveyard confusion | 60 | **Improved** - Complete skill instead of stub |

---

## Implementation

### Action Items

| # | Action | Owner | Priority | Due |
|---|--------|-------|----------|-----|
| 1 | Fix SKILL.md metadata (description, version, keywords) | Architecture | P1 | Day 1 |
| 2 | Create worktracker-system-mappings.md | Architecture | P1 | Day 1 |
| 3 | Create worktracker-behavior-rules.md | Architecture | P1 | Day 1 |
| 4 | Consolidate worktracker-entity-rules.md | Architecture | P1 | Day 1 |
| 5 | Create examples.md | Architecture | P1 | Day 1 |
| 6 | Update SKILL.md with comprehensive content | Architecture | P1 | Day 1 |
| 7 | Remove worktracker block from CLAUDE.md | Architecture | P1 | Day 1 |
| 8 | Add worktracker pointer to CLAUDE.md | Architecture | P1 | Day 1 |
| 9 | Verify skill invocation | QA | P1 | Day 1 |
| 10 | Verify CLAUDE.md line count | QA | P1 | Day 1 |

### Validation Criteria

| Criterion | Target | Measurement |
|-----------|--------|-------------|
| CLAUDE.md line count | < 600 lines | `wc -l CLAUDE.md` |
| SKILL.md description | Correct (no "transcript") | Manual inspection |
| New rules files | 2 files exist | `ls skills/worktracker/rules/` |
| examples.md exists | 1 file | `ls skills/worktracker/` |
| Skill invocation | Works | `/worktracker` test |
| Content preserved | 100% | Diff comparison |

---

## Related Decisions

| ADR | Relationship | Notes |
|-----|--------------|-------|
| ADR-OSS-001 | ENABLES | This extraction is prerequisite for 60-80 line target |
| ADR-OSS-002 | INDEPENDENT | Dual-repo sync not affected by worktracker |

---

## References

### Primary Sources

| # | Reference | Type | Relevance |
|---|-----------|------|-----------|
| 1 | ADR-OSS-001 | Decision | Parent decomposition strategy |
| 2 | ps-investigator/problem-investigation.md | Investigation | RSK-P1-001 discovery |
| 3 | phase-1-risk-register.md | Risk | RSK-P0-004, RSK-P1-001 scoring |
| 4 | [Builder.io CLAUDE.md Guide](https://www.builder.io/blog/claude-md-guide) | Best Practice | Progressive disclosure pattern |

### Phase 1 Analysis Sources

| # | Reference | Type | Relevance |
|---|-----------|------|-----------|
| 5 | CLAUDE.md lines 27-401 | Source | Content to extract |
| 6 | skills/worktracker/SKILL.md | Source | Current skill state |
| 7 | skills/worktracker/rules/*.md | Source | Existing rules files |
| 8 | cross-pollination/barrier-2/nse-to-ps/handoff-manifest.md | Manifest | V&V requirements |

---

## Document Control

| Field | Value |
|-------|-------|
| **Document ID** | ADR-OSS-003 |
| **Status** | PROPOSED |
| **Workflow** | oss-release-20260131-001 |
| **Phase** | 2 (ADR Creation) |
| **Agent** | ps-architect-003 |
| **Risk Addressed** | RSK-P1-001 (RPN 80 - MEDIUM), RSK-P0-004 (RPN 280 - CRITICAL contribution) |
| **Decision Type** | Two-Way Door (Reversible) |
| **Implementation Effort** | 2-3 hours |
| **Word Count** | ~4,800 |
| **Constitutional Compliance** | P-001 (Truth), P-002 (Persistence), P-011 (Evidence), P-022 (No Deception) |

---

## Change History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | 2026-01-31 | ps-architect-003 | Initial ADR creation |

---

*This ADR was produced by ps-architect-003 for PROJ-001-oss-release Phase 2.*
*Constitutional Compliance: P-001 (Truth), P-002 (Persistence), P-004 (Provenance), P-011 (Evidence)*
*Template: Michael Nygard ADR Format with Jerry L0/L1/L2 extensions*
